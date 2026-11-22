# Çoklu ajan sisteminde görevleri Robot1 ve Robot2'ye paylaştırır
# src/execution/task_allocator.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from src.validator.dsl_parser import GroundedPDDLAction


@dataclass
class AgentProfile:
    """Heterojen robot takımındaki her bir ajanın fiziksel yetenek profili."""
    agent_id: str
    role: str
    capabilities: Set[str] = field(default_factory=set)


class TaskAllocator:
    """
    Heterojen robot takımlarında aksiyon-yetenek uyumluluğunu denetler
    ve Robot Utilization (RU) metriklerini hesaplar.
    """

    DEFAULT_PROFILES: Dict[str, AgentProfile] = {
        "Robot1": AgentProfile(
            agent_id="Robot1",
            role="Mobile Manipulator",
            capabilities={"navigate", "search", "pickup", "put", "open", "close", "toggle-on", "toggle-off"}
        ),
        "Robot2": AgentProfile(
            agent_id="Robot2",
            role="Mobile Visual Sensor",
            capabilities={"navigate", "search"}
        )
    }

    def __init__(self, profiles: Optional[Dict[str, AgentProfile]] = None):
        self.profiles = profiles or self.DEFAULT_PROFILES

    def verify_team_capabilities(
        self,
        grounded_actions: List[GroundedPDDLAction]
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Plandaki her aksiyonun atandığı robotun yetenek kümesinde (capabilities)
        yer alıp almadığını kontrol eder.
        """
        for idx, act in enumerate(grounded_actions, start=1):
            agent_id = act.parameters[0]
            profile = self.profiles.get(agent_id)

            if not profile:
                return (
                    False,
                    f"Adım {idx}: '{agent_id}' için tanımlı robot profili bulunamadı.",
                    f"(unknown-agent {agent_id})"
                )

            if act.action_name not in profile.capabilities:
                return (
                    False,
                    f"Adım {idx}: '{agent_id}' ({profile.role}) '{act.action_name}' yeteneğine sahip değil! "
                    f"Bu görevi manipülasyon yeteneği olan bir robota atayın.",
                    f"(capability-mismatch {agent_id} {act.action_name})"
                )

        return True, "Tüm aksiyonlar robot yetenekleriyle uyumlu.", None

    def compute_robot_utilization(
        self,
        grounded_actions: List[GroundedPDDLAction]
    ) -> Dict[str, float]:
        """
        Her bir ajanın toplam plan içindeki iş yükü dağılımını ve
        aktif robot kullanım oranını (RU) hesaplar.
        """
        total_steps = len(grounded_actions)
        if total_steps == 0:
            return {"active_agent_ratio": 0.0}

        counts: Dict[str, int] = {agent_id: 0 for agent_id in self.profiles}
        for act in grounded_actions:
            agent_id = act.parameters[0]
            counts[agent_id] = counts.get(agent_id, 0) + 1

        active_agents = sum(1 for c in counts.values() if c > 0)
        total_agents = max(len(self.profiles), 1)

        utilization = {
            "active_agent_ratio": round(active_agents / total_agents, 3)
        }
        for agent_id, count in counts.items():
            utilization[f"{agent_id}_share"] = round(count / total_steps, 3)

        return utilization