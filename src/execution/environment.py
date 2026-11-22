# thor_env.py'nin refactor edilmiş hali (Sadece simülasyonu başlatır/kapatır)
# src/execution/environment.py

from typing import Any, Dict, Optional
from ai2thor.controller import Controller

from src.core.exceptions import SimulationExecutionError


class ThorEnvironment:
    """
    AI2-THOR (The House of Interactions) simülasyon ortamını başlatır ve yönetir.
    Çoklu ajan (Multi-Agent) desteği ile yapılandırılmıştır.
    """

    def __init__(self, scene: str = "FloorPlan1", agent_count: int = 2, grid_size: float = 0.25):
        self.scene = scene
        self.agent_count = agent_count
        self.grid_size = grid_size
        self.controller: Optional[Controller] = None
        self.last_metadata: Optional[Dict[str, Any]] = None

    def start(self):
        """Simülasyon motorunu (Unity backend) başlatır."""
        try:
            self.controller = Controller(
                agentMode="default",
                visibilityDistance=1.5,
                scene=self.scene,
                gridSize=self.grid_size,
                snapToGrid=True,
                renderDepthImage=False,
                renderInstanceSegmentation=False,
                width=600,
                height=600,
                fieldOfView=90
            )

            if self.agent_count > 1:
                event = self.controller.step(
                    action="Initialize",
                    agentCount=self.agent_count,
                    gridSize=self.grid_size
                )
                self.last_metadata = event.metadata
            else:
                self.last_metadata = self.controller.last_event.metadata

            print(f"AI2-THOR Başlatıldı: {self.scene} | Ajan Sayısı: {self.agent_count}")

        except Exception as e:
            raise SimulationExecutionError(f"AI2-THOR başlatılamadı: {e}")

    def reset(self, scene: Optional[str] = None):
        """Ortamı başlangıç durumuna sıfırlar."""
        if not self.controller:
            self.start()
            return

        target_scene = scene or self.scene
        self.controller.reset(target_scene)

        if self.agent_count > 1:
            event = self.controller.step(action="Initialize", agentCount=self.agent_count)
            self.last_metadata = event.metadata
        else:
            self.last_metadata = self.controller.last_event.metadata

    def stop(self):
        """Simülasyonu güvenli bir şekilde kapatır."""
        if self.controller:
            self.controller.stop()
            self.controller = None
            print("AI2-THOR simülasyonu durduruldu.")

    def get_agent_internal_id(self, agent_name: str) -> int:
        """
        'Robot1' -> 0, 'Robot2' -> 1 eşleştirmesini yapar.
        AI2-THOR API'si ajanları 0, 1, 2 şeklinde indeksler.
        """
        try:
            return int(agent_name.replace("Robot", "")) - 1
        except ValueError:
            return 0