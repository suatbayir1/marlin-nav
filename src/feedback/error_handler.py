# Yürütme/PDDL hatalarını Error Predicates formatına çevirip Planner'a iletir
# src/feedback/error_handler.py

from dataclasses import dataclass
from typing import Optional

from src.memory.state_tracker import StateTracker
from src.validator.fast_downward_api import ValidationResult


@dataclass
class FeedbackPacket:
    """
    PDDL veya AI2-THOR katmanından gelen hatayı Central Planner (LLM)
    için yapılandırılmış geri bildirime dönüştüren veri paketi.
    """
    source: str                 # "SYNTAX", "PDDL_VALIDATOR" veya "AI2THOR_EXECUTION"
    error_predicate: str        # Örn: "(closed fridge) -> Precondition (opened fridge) failed"
    raw_message: str            # Ham hata açıklaması
    llm_adjustment_prompt: str  # LLM'e doğrudan iletilecek düzeltme talimatı


class DynamicFeedbackHandler:
    """
    PEFA (Proposal-Execution-Feedback-Adjustment) döngüsündeki
    Feedback -> Adjustment geçişini yönetir.
    Hataları Error Predicate'e çevirir, RAG hafızasını günceller ve LLM'i yönlendirir.
    """

    def __init__(self, state_tracker: Optional[StateTracker] = None, max_retries: int = 3):
        self.state_tracker = state_tracker
        self.max_retries = max_retries
        self.attempt_history: list[FeedbackPacket] = []

    def handle_syntax_error(self, error_msg: str) -> FeedbackPacket:
        """AST ayrıştırıcıdan gelen DSL sözdizimi hatalarını işler."""
        predicate = "(dsl-syntax-error)"
        llm_msg = (
            f"[SYNTAX ERROR] {error_msg}. "
            f"Output ONLY valid Pythonic DSL calls like Robot1.navigate(\"target\")."
        )
        packet = FeedbackPacket(
            source="SYNTAX",
            error_predicate=predicate,
            raw_message=error_msg,
            llm_adjustment_prompt=llm_msg
        )
        self.attempt_history.append(packet)
        return packet

    def handle_pddl_validation_error(self, val_result: ValidationResult) -> FeedbackPacket:
        """
        PDDL motorundan (Symbolic Validator) dönen ön koşul ihlalini işler,
        RAG hafızasına kısıtı kaydeder ve LLM için düzeltme prompt'u üretir.
        """
        predicate = val_result.error_predicate or "(pddl-precondition-failed)"
        raw_msg = val_result.message

        if self.state_tracker:
            self.state_tracker.record_discovered_constraint(
                constraint_text=raw_msg,
                predicate=predicate
            )

        llm_msg = (
            f"[SYMBOLIC PDDL VALIDATION FAILED]\n"
            f"- Failed Action: {val_result.failed_action}\n"
            f"- Reason: {raw_msg}\n"
            f"- Error Predicate: {predicate}\n"
            f"- Instruction: Insert the missing prerequisite action(s) before {val_result.failed_action} "
            f"(for example, open a closed receptacle before putting an object inside)."
        )

        packet = FeedbackPacket(
            source="PDDL_VALIDATOR",
            error_predicate=predicate,
            raw_message=raw_msg,
            llm_adjustment_prompt=llm_msg
        )
        self.attempt_history.append(packet)
        return packet

    def handle_execution_error(self, raw_error_msg: str, error_predicate: str) -> FeedbackPacket:
        """
        AI2-THOR simülasyonu sırasında oluşan fiziksel hataları (ör. engel, erişilemeyen nesne)
        işler ve LLM'in planı dinamik olarak güncellemesini sağlar.
        """
        if self.state_tracker:
            self.state_tracker.record_discovered_constraint(
                constraint_text=raw_error_msg,
                predicate=error_predicate
            )

        llm_msg = (
            f"[SIMULATION EXECUTION FAILED]\n"
            f"- Details: {raw_error_msg}\n"
            f"- Error Predicate: {error_predicate}\n"
            f"- Instruction: Revise the plan to recover from this physical constraint "
            f"(e.g., navigate closer, search another location, or reassign another robot)."
        )

        packet = FeedbackPacket(
            source="AI2THOR_EXECUTION",
            error_predicate=error_predicate,
            raw_message=raw_error_msg,
            llm_adjustment_prompt=llm_msg
        )
        self.attempt_history.append(packet)
        return packet

    def reset(self):
        """Yeni bir görev (episode) başlarken deneme geçmişini sıfırlar."""
        self.attempt_history.clear()


# Adım 9 Entegrasyon Testi
if __name__ == "__main__":
    from src.memory.chromadb_client import VectorDatabaseClient
    from src.validator.dsl_parser import WorldState
    from src.validator.fast_downward_api import ValidationResult

    print("1. StateTracker ve DynamicFeedbackHandler başlatılıyor...")
    db = VectorDatabaseClient(persist_directory="./chroma_db")
    tracker = StateTracker(db_client=db)
    fb_handler = DynamicFeedbackHandler(state_tracker=tracker, max_retries=3)

    # Başlangıç durumunu RAG'a kaydet
    world = WorldState(
        agents={"Robot1"},
        locations={"kitchen", "countertop", "fridge"},
        items={"apple"}
    )
    world.add_fact("at-agent", "Robot1", "kitchen")
    world.add_fact("at-object", "apple", "countertop")
    world.add_fact("closed", "fridge")

    saved_summary = tracker.record_world_state(world, note="Initial Kitchen State")
    print(f"\n2. RAG Hafızasına Kaydedilen Başlangıç Durumu:\n   {saved_summary}")

    # Örnek PDDL hatasını simüle et ve FeedbackPacket üret
    mock_val_error = ValidationResult(
        is_valid=False,
        message="Adım 4 PDDL Doğrulama Hatası [(put Robot1 apple fridge)]: 'fridge' kapalı durumda!",
        failed_step_index=4,
        failed_action="(put Robot1 apple fridge)",
        error_predicate="(closed fridge) -> Precondition (opened fridge) failed"
    )

    packet = fb_handler.handle_pddl_validation_error(mock_val_error)
    print("\n3. LLM'e Gönderilecek Dynamic Feedback Paketi:")
    print(packet.llm_adjustment_prompt)