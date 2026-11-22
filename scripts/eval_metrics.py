# Yürütme sonrası SR, SPL, ve RU metriklerini hesaplar
# scripts/eval_metrics.py

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class EpisodeRecord:
    """Tek bir deney senaryosunun (episode) kantitatif sonuç kaydı."""
    episode_id: str
    task_instruction: str
    success: bool
    optimal_path_length: float
    actual_path_length: float
    spl: float
    pddl_attempts: int
    pddl_valid_on_first_try: bool
    robot_utilization: Dict[str, float] = field(default_factory=dict)


class MetricsEvaluator:
    """
    Tez deneyleri için SR, SPL, Plan Validity ve Robot Utilization (RU)
    metriklerini toplar ve raporlar.
    """

    def __init__(self, output_file: str = "logs/experiment_results.json"):
        self.output_path = Path(output_file)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.records: List[EpisodeRecord] = []

    @staticmethod
    def calculate_spl(success: bool, optimal_length: float, actual_length: float) -> float:
        """SPL = S * (L_optimal / max(P_actual, L_optimal)) formülünü hesaplar."""
        if not success:
            return 0.0
        denominator = max(actual_length, optimal_length, 1e-6)
        return round(optimal_length / denominator, 4)

    def log_episode(
        self,
        episode_id: str,
        task_instruction: str,
        success: bool,
        optimal_path_length: float,
        actual_path_length: float,
        pddl_attempts: int,
        pddl_valid_on_first_try: bool,
        robot_utilization: Dict[str, float]
    ) -> EpisodeRecord:
        spl = self.calculate_spl(success, optimal_path_length, actual_path_length)
        record = EpisodeRecord(
            episode_id=episode_id,
            task_instruction=task_instruction,
            success=success,
            optimal_path_length=optimal_path_length,
            actual_path_length=actual_path_length,
            spl=spl,
            pddl_attempts=pddl_attempts,
            pddl_valid_on_first_try=pddl_valid_on_first_try,
            robot_utilization=robot_utilization
        )
        self.records.append(record)
        return record

    def summarize(self) -> Dict[str, float]:
        """Tüm deneylerin ortalama SR, SPL ve Plan Validity özetini döner."""
        n = len(self.records)
        if n == 0:
            return {"total_episodes": 0, "SR": 0.0, "SPL": 0.0, "First_Try_Plan_Validity": 0.0}

        sr = sum(1 for r in self.records if r.success) / n
        avg_spl = sum(r.spl for r in self.records) / n
        first_try_valid = sum(1 for r in self.records if r.pddl_valid_on_first_try) / n

        return {
            "total_episodes": n,
            "SR": round(sr, 4),
            "SPL": round(avg_spl, 4),
            "First_Try_Plan_Validity": round(first_try_valid, 4)
        }

    def save_report(self) -> Path:
        payload = {
            "summary": self.summarize(),
            "episodes": [asdict(r) for r in self.records]
        }
        self.output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return self.output_path