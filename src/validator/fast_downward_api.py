# PDDL Engine'i çalıştırıp Formal Verification yapar
# src/validator/fast_downward_api.py

import copy
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from src.core.exceptions import PlanValidationError
from src.validator.dsl_parser import GroundedPDDLAction, WorldState


@dataclass
class ValidationResult:
    """Sembolik PDDL doğrulama sonucunu ve varsa hata predikatını taşır."""
    is_valid: bool
    message: str
    failed_step_index: Optional[int] = None
    failed_action: Optional[str] = None
    error_predicate: Optional[str] = None
    final_state: Optional[WorldState] = None


class FastDownwardValidator:
    """
    Topraklanmış PDDL aksiyon dizisini domain ön koşullarına (S |= P) göre
    sembolik olarak doğrular ve opsiyonel olarak Fast Downward motorunu çalıştırır.
    """

    def __init__(self, fast_downward_bin: Optional[str] = None):
        self.fd_binary = fast_downward_bin or shutil.which("fast-downward.py")

    def validate_plan(
        self,
        grounded_actions: List[GroundedPDDLAction],
        initial_state: WorldState,
        domain_path: Optional[Path] = None,
        problem_path: Optional[Path] = None,
        raise_on_error: bool = True
    ) -> ValidationResult:
        """
        1. Varsa harici PDDL dosyalarının varlığını kontrol eder.
        2. Her bir PDDL aksiyonunun ön koşullarını (preconditions) mevcut durum S
           üzerinde doğrular ve etkilerini (effects) uygulayarak S' durumuna geçer.
        """
        if not grounded_actions:
            result = ValidationResult(
                is_valid=False,
                message="Doğrulanacak aksiyon listesi boş.",
                error_predicate="(empty-plan)"
            )
            if raise_on_error:
                raise PlanValidationError(result.message)
            return result

        # Durum uzayını kopyala (orijinal initial_state bozulmasın)
        current_state = copy.deepcopy(initial_state)

        for idx, action in enumerate(grounded_actions, start=1):
            is_ok, err_msg, err_pred = self._verify_and_apply_step(action, current_state)
            if not is_ok:
                result = ValidationResult(
                    is_valid=False,
                    message=f"Adım {idx} PDDL Doğrulama Hatası [{action.to_pddl_sexpr()}]: {err_msg}",
                    failed_step_index=idx,
                    failed_action=action.to_pddl_sexpr(),
                    error_predicate=err_pred,
                    final_state=current_state
                )
                if raise_on_error:
                    raise PlanValidationError(f"{result.message} | Error Predicate: {err_pred}")
                return result

        # Eğer sistemde Fast Downward kuruluysa problem çözülebilirliğini de teyit et
        if self.fd_binary and domain_path and problem_path:
            fd_ok, fd_msg = self._run_external_fast_downward(domain_path, problem_path)
            if not fd_ok:
                result = ValidationResult(
                    is_valid=False,
                    message=f"Fast Downward Solver Hatası: {fd_msg}",
                    error_predicate="(unsolvable-pddl-problem)",
                    final_state=current_state
                )
                if raise_on_error:
                    raise PlanValidationError(result.message)
                return result

        return ValidationResult(
            is_valid=True,
            message=f"Plan sembolik olarak GEÇERLİ ({len(grounded_actions)} adım doğrulandı).",
            final_state=current_state
        )

    def _verify_and_apply_step(
        self,
        action: GroundedPDDLAction,
        state: WorldState
    ) -> tuple[bool, str, Optional[str]]:
        """
        Tek bir PDDL aksiyonu için S |= Precondition kontrolü yapar ve
        başarılıysa S' = (S - Del) U Add geçişini uygular.
        """
        name = action.action_name
        p = action.parameters

        if name == "navigate":
            agent, from_loc, to_loc = p
            if not state.has_fact("at-agent", agent, from_loc):
                return False, f"{agent} başlangıç konumu '{from_loc}' üzerinde değil.", f"(not (at-agent {agent} {from_loc}))"
            state.predicates.discard(("at-agent", agent, from_loc))
            state.add_fact("at-agent", agent, to_loc)
            return True, "OK", None

        if name == "open":
            agent, loc = p
            if not state.has_fact("at-agent", agent, loc):
                return False, f"{agent}, '{loc}' konumunda değil.", f"(not (at-agent {agent} {loc}))"
            if not state.has_fact("openable", loc):
                return False, f"'{loc}' açılabilir (openable) bir nesne değil.", f"(not (openable {loc}))"
            if not state.has_fact("closed", loc):
                return False, f"'{loc}' zaten açık.", f"(not (closed {loc}))"
            state.predicates.discard(("closed", loc))
            state.add_fact("opened", loc)
            return True, "OK", None

        if name == "close":
            agent, loc = p
            if not state.has_fact("at-agent", agent, loc):
                return False, f"{agent}, '{loc}' konumunda değil.", f"(not (at-agent {agent} {loc}))"
            if not state.has_fact("opened", loc):
                return False, f"'{loc}' açık olmadığı için kapatılamaz.", f"(not (opened {loc}))"
            state.predicates.discard(("opened", loc))
            state.add_fact("closed", loc)
            return True, "OK", None

        if name == "pickup":
            agent, item, loc = p
            if not state.has_fact("at-agent", agent, loc):
                return False, f"{agent}, '{loc}' konumunda değil.", f"(not (at-agent {agent} {loc}))"
            if not state.has_fact("at-object", item, loc):
                return False, f"'{item}' nesnesi '{loc}' konumunda bulunamadı.", f"(not (at-object {item} {loc}))"
            if not state.has_fact("hand-empty", agent):
                return False, f"{agent} eli dolu olduğu için '{item}' alamaz.", f"(not (hand-empty {agent}))"
            state.predicates.discard(("at-object", item, loc))
            state.predicates.discard(("hand-empty", agent))
            state.add_fact("holding", agent, item)
            return True, "OK", None

        if name == "put":
            agent, item, loc = p
            if not state.has_fact("at-agent", agent, loc):
                return False, f"{agent}, '{loc}' konumunda değil.", f"(not (at-agent {agent} {loc}))"
            if not state.has_fact("holding", agent, item):
                return False, f"{agent} elinde '{item}' tutmuyor.", f"(not (holding {agent} {item}))"
            if state.has_fact("openable", loc) and not state.has_fact("opened", loc):
                return (
                    False,
                    f"'{loc}' kapalı (closed) durumda! İçine '{item}' koymadan önce açılmalıdır.",
                    f"(closed {loc}) -> Precondition (opened {loc}) failed"
                )
            state.predicates.discard(("holding", agent, item))
            state.add_fact("hand-empty", agent)
            state.add_fact("at-object", item, loc)
            return True, "OK", None

        if name == "search":
            agent, loc, item = p
            if not state.has_fact("at-agent", agent, loc):
                return False, f"{agent}, arama yapmak için '{loc}' konumunda değil.", f"(not (at-agent {agent} {loc}))"
            state.add_fact("searched", loc, item)
            return True, "OK", None

        if name == "toggle-on":
            agent, item, loc = p
            if not state.has_fact("at-agent", agent, loc):
                return False, f"{agent}, '{loc}' konumunda değil.", f"(not (at-agent {agent} {loc}))"
            if not state.has_fact("toggleable", item):
                return False, f"'{item}' açılıp kapatılabilir (toggleable) değil.", f"(not (toggleable {item}))"
            state.add_fact("is-on", item)
            return True, "OK", None

        if name == "toggle-off":
            agent, item, loc = p
            if not state.has_fact("at-agent", agent, loc):
                return False, f"{agent}, '{loc}' konumunda değil.", f"(not (at-agent {agent} {loc}))"
            if not state.has_fact("is-on", item):
                return False, f"'{item}' zaten kapalı.", f"(not (is-on {item}))"
            state.predicates.discard(("is-on", item))
            return True, "OK", None

        return False, f"Domain içinde tanımsız PDDL aksiyonu: '{name}'", f"(unknown-action {name})"

    def _run_external_fast_downward(self, domain_path: Path, problem_path: Path) -> tuple[bool, str]:
        """Sistemde fast-downward.py kuruluysa subprocess ile resmi plan doğrulaması yapar."""
        cmd = [
            self.fd_binary,
            str(domain_path),
            str(problem_path),
            "--search",
            "astar(lmcut())"
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if proc.returncode == 0 and "Solution found!" in proc.stdout:
                return True, "Fast Downward Solution found!"
            return False, proc.stderr or proc.stdout[-300:]
        except Exception as e:
            return False, str(e)


# Adım 7 Entegrasyon Testi: Hatalı Planı Yakalama ve Feedback ile Düzeltme
if __name__ == "__main__":
    from src.memory.chromadb_client import VectorDatabaseClient
    from src.memory.context_builder import ContextBuilder
    from src.planner.dsl_generator import DSLGenerator
    from src.planner.llm_agent import LLMAgent
    from src.validator.domain_manager import DomainManager
    from src.validator.dsl_parser import DSLToPDDLParser

    db = VectorDatabaseClient(persist_directory="./chroma_db")
    generator = DSLGenerator(LLMAgent(), ContextBuilder(db))
    domain_mgr = DomainManager()
    domain_path = domain_mgr.save_domain_file()
    parser = DSLToPDDLParser(domain_mgr)
    validator = FastDownwardValidator()

    world = WorldState(
        agents={"Robot1"},
        locations={"kitchen", "countertop", "fridge"},
        items={"apple"}
    )
    world.add_fact("at-agent", "Robot1", "kitchen")
    world.add_fact("hand-empty", "Robot1")
    world.add_fact("at-object", "apple", "countertop")
    world.add_fact("openable", "fridge")
    world.add_fact("closed", "fridge")

    task = "Pick up the apple from the countertop and put it inside the fridge."
    state_desc = "Robot1 is in kitchen. Apple is on countertop. Fridge is closed."

    print("=== 1. DENEME: İLK LLM PLANI DOĞRULANIYOR ===")
    dsl_steps_v1 = generator.generate_structured_plan(task, state_desc)
    actions_v1, problem_path = parser.translate_plan(dsl_steps_v1, world)
    result_v1 = validator.validate_plan(actions_v1, world, domain_path, problem_path, raise_on_error=False)

    print(f"Geçerli mi? : {result_v1.is_valid}")
    print(f"Mesaj      : {result_v1.message}")
    print(f"Predikat   : {result_v1.error_predicate}\n")

    if not result_v1.is_valid:
        print("=== 2. DENEME: HATA PREDIKATI LLM'E GERİ BESLENİYOR (DYNAMIC FEEDBACK) ===")
        dsl_steps_v2 = generator.generate_structured_plan(
            task_instruction=task,
            current_state=state_desc,
            error_feedback=f"{result_v1.message} ({result_v1.error_predicate})"
        )
        actions_v2, problem_path_v2 = parser.translate_plan(dsl_steps_v2, world)
        result_v2 = validator.validate_plan(actions_v2, world, domain_path, problem_path_v2, raise_on_error=False)

        print(f"Geçerli mi? : {result_v2.is_valid}")
        print(f"Mesaj      : {result_v2.message}")
        print("Son Durum Predikatları:", sorted(result_v2.final_state.predicates))