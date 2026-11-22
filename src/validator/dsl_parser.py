# Pythonic DSL -> PDDL Problem dosyası çevirici
# src/validator/dsl_parser.py

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

from src.core.exceptions import DSLSyntaxError
from src.planner.dsl_generator import DSLStep
from src.validator.domain_manager import DomainManager


@dataclass
class WorldState:
    """
    AI2-THOR ortamının sembolik PDDL başlangıç durumunu temsil eder.
    İleride AI2-THOR metadata'sından otomatik doldurulacaktır.
    """
    agents: Set[str] = field(default_factory=set)
    locations: Set[str] = field(default_factory=set)
    items: Set[str] = field(default_factory=set)
    predicates: Set[Tuple[str, ...]] = field(default_factory=set)

    def add_fact(self, *predicate: str):
        self.predicates.add(tuple(predicate))

    def has_fact(self, *predicate: str) -> bool:
        return tuple(predicate) in self.predicates


@dataclass
class GroundedPDDLAction:
    """DSL adımının karşılığı olan somut PDDL aksiyon çağrısı."""
    action_name: str
    parameters: List[str]
    source_dsl: str

    def to_pddl_sexpr(self) -> str:
        return f"({self.action_name} {' '.join(self.parameters)})"


class DSLToPDDLParser:
    """
    Pythonic DSL adımlarını (DSLStep) PDDL aksiyon dizisine ve
    Fast Downward uyumlu problem.pddl dosyasına çevirir.
    """

    def __init__(self, domain_manager: DomainManager):
        self.domain_manager = domain_manager

    def translate_plan(
        self,
        dsl_steps: List[DSLStep],
        initial_state: WorldState,
        problem_name: str = "ai2thor-task"
    ) -> Tuple[List[GroundedPDDLAction], Path]:
        """
        1. Her DSLStep'i konum takibi yaparak PDDL aksiyonuna dönüştürür.
        2. Başlangıç durumu (init) ve çıkarılan hedeflerle (goal) problem.pddl oluşturur.
        """
        grounded_actions: List[GroundedPDDLAction] = []
        goal_predicates: List[Tuple[str, ...]] = []

        # Ajanların plan boyunca anlık konumlarını takip etmek için kopya sözlük
        agent_locations: Dict[str, str] = {}
        for pred in initial_state.predicates:
            if pred[0] == "at-agent" and len(pred) == 3:
                agent_locations[pred[1]] = pred[2]

        for step in dsl_steps:
            agent = step.agent_id
            action = step.action
            args = step.args

            if agent not in initial_state.agents:
                raise DSLSyntaxError(f"Tanımsız robot ajan: '{agent}'")

            current_loc = agent_locations.get(agent, "unknown_location")

            if action == "navigate":
                if len(args) != 1:
                    raise DSLSyntaxError(f"navigate tek parametre almalıdır: {step.raw_line}")
                target_loc = args[0]
                grounded_actions.append(
                    GroundedPDDLAction("navigate", [agent, current_loc, target_loc], step.raw_line)
                )
                agent_locations[agent] = target_loc

            elif action == "open":
                if len(args) != 1:
                    raise DSLSyntaxError(f"open tek parametre almalıdır: {step.raw_line}")
                target_loc = args[0]
                grounded_actions.append(
                    GroundedPDDLAction("open", [agent, target_loc], step.raw_line)
                )

            elif action == "close":
                if len(args) != 1:
                    raise DSLSyntaxError(f"close tek parametre almalıdır: {step.raw_line}")
                target_loc = args[0]
                grounded_actions.append(
                    GroundedPDDLAction("close", [agent, target_loc], step.raw_line)
                )
                goal_predicates.append(("closed", target_loc))

            elif action == "pickup":
                if len(args) != 1:
                    raise DSLSyntaxError(f"pickup tek parametre almalıdır: {step.raw_line}")
                item = args[0]
                grounded_actions.append(
                    GroundedPDDLAction("pickup", [agent, item, current_loc], step.raw_line)
                )
                goal_predicates.append(("holding", agent, item))

            elif action == "put":
                if len(args) != 1:
                    raise DSLSyntaxError(f"put tek parametre almalıdır: {step.raw_line}")
                target_loc = args[0]
                # Ajanın elinde tuttuğu son nesneyi bul
                held_item = self._infer_held_item(grounded_actions, agent)
                grounded_actions.append(
                    GroundedPDDLAction("put", [agent, held_item, target_loc], step.raw_line)
                )
                # Nesne hedefe konulduğunda artık elde tutma hedefini kaldırıp yeni konumu hedef yap
                goal_predicates = [g for g in goal_predicates if not (g[0] == "holding" and g[2] == held_item)]
                goal_predicates.append(("at-object", held_item, target_loc))

            elif action == "search":
                if len(args) != 2:
                    raise DSLSyntaxError(f"search iki parametre almalıdır (area, object): {step.raw_line}")
                area, item = args
                grounded_actions.append(
                    GroundedPDDLAction("search", [agent, area, item], step.raw_line)
                )
                goal_predicates.append(("searched", area, item))

            elif action in ("toggle_on", "toggle_off"):
                if len(args) != 1:
                    raise DSLSyntaxError(f"{action} tek parametre almalıdır: {step.raw_line}")
                item = args[0]
                pddl_act = "toggle-on" if action == "toggle_on" else "toggle-off"
                grounded_actions.append(
                    GroundedPDDLAction(pddl_act, [agent, item, current_loc], step.raw_line)
                )
                if action == "toggle_on":
                    goal_predicates.append(("is-on", item))

        problem_path = self._write_problem_file(
            problem_name=problem_name,
            initial_state=initial_state,
            goal_predicates=goal_predicates
        )
        return grounded_actions, problem_path

    @staticmethod
    def _infer_held_item(actions_so_far: List[GroundedPDDLAction], agent: str) -> str:
        """Ajanın önceki pickup adımında aldığı nesneyi bulur."""
        for act in reversed(actions_so_far):
            if act.action_name == "pickup" and act.parameters[0] == agent:
                return act.parameters[1]
        return "unknown_item"

    def _write_problem_file(
        self,
        problem_name: str,
        initial_state: WorldState,
        goal_predicates: List[Tuple[str, ...]]
    ) -> Path:
        """Fast Downward için geçerli problem.pddl dosyasını oluşturur."""
        agents_str = " ".join(sorted(initial_state.agents))
        locs_str = " ".join(sorted(initial_state.locations))
        items_str = " ".join(sorted(initial_state.items))

        init_lines = [f"    ({' '.join(p)})" for p in sorted(initial_state.predicates)]
        goal_lines = [f"      ({' '.join(g)})" for g in dict.fromkeys(goal_predicates)]

        if not goal_lines:
            goal_lines = ["      (hand-empty Robot1)"]

        problem_pddl = f"""(define (problem {problem_name})
        (:domain {self.domain_manager.DOMAIN_NAME})

        (:objects
            {agents_str} - agent
            {locs_str} - location
            {items_str} - item
        )

        (:init
        {chr(10).join(init_lines)}
        )

        (:goal
            (and
        {chr(10).join(goal_lines)}
            )
        )
        )
        """
        problem_path = self.domain_manager.output_dir / "problem.pddl"
        problem_path.write_text(problem_pddl.strip() + "\n", encoding="utf-8")
        return problem_path


# Adım 6 Entegrasyon Testi
if __name__ == "__main__":
    from src.memory.chromadb_client import VectorDatabaseClient
    from src.memory.context_builder import ContextBuilder
    from src.planner.dsl_generator import DSLGenerator
    from src.planner.llm_agent import LLMAgent

    # 1. LLM Planner'dan DSL adımlarını al
    db = VectorDatabaseClient(persist_directory="./chroma_db")
    generator = DSLGenerator(LLMAgent(), ContextBuilder(db))
    task = "Pick up the apple from the countertop and put it inside the fridge."
    state_desc = "Robot1 is in kitchen. Apple is on countertop. Fridge is closed."
    dsl_steps = generator.generate_structured_plan(task, state_desc)

    # 2. Başlangıç Dünya Durumunu (WorldState) tanımla
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

    # 3. PDDL Domain ve Problem dosyalarını üret
    domain_mgr = DomainManager()
    domain_file = domain_mgr.save_domain_file()

    parser = DSLToPDDLParser(domain_mgr)
    grounded_actions, problem_file = parser.translate_plan(dsl_steps, world)

    print(f"1. Domain dosyası kaydedildi : {domain_file}")
    print(f"2. Problem dosyası kaydedildi: {problem_file}\n")

    print("=== TOPRAKLANMIŞ (GROUNDED) PDDL AKSİYON DİZİSİ ===")
    for idx, act in enumerate(grounded_actions, start=1):
        print(f"{idx}. {act.to_pddl_sexpr()}   <-- [{act.source_dsl}]")

    print("\n=== ÜRETİLEN PROBLEM.PDDL İÇERİĞİ ===")
    print(problem_file.read_text(encoding="utf-8"))