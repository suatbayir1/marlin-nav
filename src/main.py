# Orchestrator: Sistem akışını yöneten ana giriş noktası
# src/main.py

import argparse
import time
from typing import Optional

from scripts.eval_metrics import MetricsEvaluator
from src.core.exceptions import DSLSyntaxError
from src.core.logger import get_logger
from src.execution.action_runner import ActionRunner
from src.execution.environment import ThorEnvironment
from src.execution.task_allocator import TaskAllocator
from src.feedback.error_handler import DynamicFeedbackHandler
from src.memory.chromadb_client import VectorDatabaseClient
from src.memory.context_builder import ContextBuilder
from src.memory.state_tracker import StateTracker
from src.planner.dsl_generator import DSLGenerator
from src.planner.llm_agent import LLMAgent
from src.validator.domain_manager import DomainManager
from src.validator.dsl_parser import DSLToPDDLParser, WorldState
from src.validator.fast_downward_api import FastDownwardValidator


class HybridPlanningOrchestrator:
    """
    LLM + PDDL + RAG Hibrit Çoklu-Ajan Görev Planlama Mimarisinin
    uçtan uca PEFA (Proposal-Execution-Feedback-Adjustment) kontrolcüsü.
    """

    def __init__(self, dry_run: bool = True, scene: str = "FloorPlan1", agent_count: int = 2, provider: Optional[str] = None, model_name: Optional[str] = None):
        self.logger = get_logger("Orchestrator")
        self.dry_run = dry_run
        self.scene = scene
        self.agent_count = agent_count

        self.db_client = VectorDatabaseClient(persist_directory="./chroma_db")
        self.context_builder = ContextBuilder(db_client=self.db_client)
        self.state_tracker = StateTracker(db_client=self.db_client)

        if self.db_client.collection.count() == 0:
            self.logger.info("ChromaDB boş bulundu, Wiki (.md) bilgileri yükleniyor...")
            self.context_builder.ingest_wiki_knowledge()

        # LLM Ajanını başlat (CLI parametresi varsa config'i ezer)
        self.logger.info(f"Yerel LLM bağlantısı kuruluyor... (Sağlayıcı: {provider or 'Config Varsayılanı'})")
        self.llm_agent = LLMAgent()
        if provider:
            self.llm_agent.provider = provider
        if model_name:
            self.llm_agent.model_name = model_name

        self.dsl_generator = DSLGenerator(llm_agent=self.llm_agent, context_builder=self.context_builder)

        self.domain_manager = DomainManager()
        self.domain_path = self.domain_manager.save_domain_file()
        self.dsl_parser = DSLToPDDLParser(domain_manager=self.domain_manager)
        self.validator = FastDownwardValidator()

        self.task_allocator = TaskAllocator()
        self.feedback_handler = DynamicFeedbackHandler(state_tracker=self.state_tracker, max_retries=3)

        self.env: Optional[ThorEnvironment] = None
        self.runner: Optional[ActionRunner] = None
        self.metrics = MetricsEvaluator()

    def build_sample_kitchen_world(self) -> WorldState:
        world = WorldState(
            agents={"Robot1", "Robot2"},
            locations={"kitchen", "countertop", "fridge"},
            items={"apple"}
        )
        world.add_fact("at-agent", "Robot1", "kitchen")
        world.add_fact("hand-empty", "Robot1")
        world.add_fact("at-agent", "Robot2", "kitchen")
        world.add_fact("hand-empty", "Robot2")
        world.add_fact("at-object", "apple", "countertop")
        world.add_fact("openable", "fridge")
        world.add_fact("closed", "fridge")
        return world

    def run_episode(self, episode_id: str, task_instruction: str, world_state: WorldState) -> bool:
        self.logger.info("=" * 65)
        self.logger.info(f"EPISODE BAŞLADI [{episode_id}] | Görev: '{task_instruction}'")
        self.feedback_handler.reset()

        state_summary = self.state_tracker.record_world_state(world_state, note="Initial State")
        current_feedback: Optional[str] = None
        valid_on_first_try = False
        episode_success = False
        executed_step_count = 0
        last_ru = {}

        if not self.dry_run:
            self.env = ThorEnvironment(scene=self.scene, agent_count=self.agent_count)
            self.env.start()
            self.runner = ActionRunner(self.env)

        try:
            for attempt in range(1, self.feedback_handler.max_retries + 1):
                self.logger.info(f"--- PEFA Döngüsü Deneme {attempt}/{self.feedback_handler.max_retries} ---")

                try:
                    self.logger.info(f"Ollama {self.llm_agent.model_name} üzerinden DSL üretiliyor. Lütfen bekleyin...")
                    dsl_steps = self.dsl_generator.generate_structured_plan(
                        task_instruction=task_instruction,
                        current_state=state_summary,
                        error_feedback=current_feedback
                    )
                except DSLSyntaxError as syn_err:
                    self.logger.warning(f"DSL Sözdizimi Hatası: {syn_err}")
                    packet = self.feedback_handler.handle_syntax_error(str(syn_err))
                    current_feedback = packet.llm_adjustment_prompt
                    continue
                except Exception as e:
                    self.logger.error(f"LLM API Hatası: {e}")
                    return False

                self.logger.info(f"LLM {len(dsl_steps)} adımlı Pythonic DSL üretti:")
                for s in dsl_steps:
                    self.logger.info(f"   -> {s.raw_line}")

                try:
                    grounded_actions, problem_path = self.dsl_parser.translate_plan(
                        dsl_steps=dsl_steps,
                        initial_state=world_state,
                        problem_name=episode_id
                    )
                except DSLSyntaxError as parse_err:
                    self.logger.warning(f"PDDL Çeviri Hatası: {parse_err}")
                    packet = self.feedback_handler.handle_syntax_error(str(parse_err))
                    current_feedback = packet.llm_adjustment_prompt
                    continue

                val_result = self.validator.validate_plan(
                    grounded_actions=grounded_actions,
                    initial_state=world_state,
                    domain_path=self.domain_path,
                    problem_path=problem_path,
                    raise_on_error=False
                )

                if not val_result.is_valid:
                    self.logger.warning(f"PDDL Doğrulama Reddetti: {val_result.message}")
                    packet = self.feedback_handler.handle_pddl_validation_error(val_result)
                    current_feedback = packet.llm_adjustment_prompt
                    continue

                cap_ok, cap_msg, cap_pred = self.task_allocator.verify_team_capabilities(grounded_actions)
                if not cap_ok:
                    self.logger.warning(f"Yetenek Uyuşmazlığı: {cap_msg}")
                    packet = self.feedback_handler.handle_execution_error(cap_msg, cap_pred or "(capability-error)")
                    current_feedback = packet.llm_adjustment_prompt
                    continue

                if attempt == 1:
                    valid_on_first_try = True

                self.logger.info(f"PDDL & Yetenek Doğrulaması BAŞARILI: {val_result.message}")
                last_ru = self.task_allocator.compute_robot_utilization(grounded_actions)
                executed_step_count = len(grounded_actions)

                if self.dry_run:
                    self.logger.info("[DRY-RUN EXECUTION] Doğrulanmış adımlar simüle ediliyor...")
                    for act in grounded_actions:
                        self.logger.info(f"   [EXEC] {act.to_pddl_sexpr()}")
                    if val_result.final_state:
                        state_summary = self.state_tracker.record_world_state(
                            val_result.final_state,
                            note="Post-Execution Verified State"
                        )
                    episode_success = True
                    break
                else:
                    self.logger.info("[LIVE AI2-THOR EXECUTION] Komutlar 3D simülasyona gönderiliyor...")
                    exec_ok, exec_msg, exec_pred = self.runner.execute_plan(grounded_actions)
                    if not exec_ok:
                        self.logger.warning(f"AI2-THOR Yürütme Hatası: {exec_msg}")
                        packet = self.feedback_handler.handle_execution_error(
                            exec_msg, exec_pred or "(thor-exec-error)"
                        )
                        current_feedback = packet.llm_adjustment_prompt
                        continue

                    if val_result.final_state:
                        state_summary = self.state_tracker.record_world_state(
                            val_result.final_state,
                            note="Post-THOR Execution State"
                        )
                    episode_success = True
                    break

            record = self.metrics.log_episode(
                episode_id=episode_id,
                task_instruction=task_instruction,
                success=episode_success,
                optimal_path_length=6.0,
                actual_path_length=float(executed_step_count) if episode_success else 0.0,
                pddl_attempts=attempt,
                pddl_valid_on_first_try=valid_on_first_try,
                robot_utilization=last_ru
            )
            report_path = self.metrics.save_report()
            self.logger.info(f"EPISODE TAMAMLANDI | Başarı (SR): {record.success} | SPL: {record.spl} | RU: {record.robot_utilization}")
            self.logger.info(f"Deney raporu kaydedildi: {report_path}")
            return episode_success

        finally:
            if self.env:
                time.sleep(1.5)
                self.env.stop()


def main():
    parser = argparse.ArgumentParser(description="Hybrid LLM-PDDL-RAG Multi-Agent Planner")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Belirtilirse AI2-THOR Unity 3D penceresini başlatır (varsayılan: dry-run)."
    )
    parser.add_argument(
        "--provider",
        type=str,
        default=None,
        choices=["mock", "ollama", "openai"],
        help="LLM sağlayıcısını zorla değiştirir (örn: ollama)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="LLM modelini zorla değiştirir (örn: mistral, llama3)"
    )
    parser.add_argument(
        "--task",
        type=str,
        default="Pick up the apple from the countertop and put it inside the fridge.",
        help="Doğal dil görev talimatı."
    )
    args = parser.parse_args()

    orchestrator = HybridPlanningOrchestrator(
        dry_run=not args.live,
        provider=args.provider,
        model_name=args.model
    )
    initial_world = orchestrator.build_sample_kitchen_world()
    orchestrator.run_episode(
        episode_id="ep_001",
        task_instruction=args.task,
        world_state=initial_world
    )


if __name__ == "__main__":
    main()