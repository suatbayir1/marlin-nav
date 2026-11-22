# Doğrulanmış aksiyonları AI2-THOR API'sine iletir ve metadata toplar
# src/execution/action_runner.py

from typing import List, Tuple, Optional
from src.core.exceptions import SimulationExecutionError
from src.execution.environment import ThorEnvironment
from src.validator.dsl_parser import GroundedPDDLAction


class ActionRunner:
    """
    Doğrulanmış PDDL aksiyonlarını AI2-THOR API'sine iletir.
    Gerçek dünya (simülasyon) fiziksel yürütmesini (execution) yönetir ve 
    hata/başarı metadata'larını RAG/Feedback döngüsüne aktarır.
    """

    # PDDL aksiyon adlarını AI2-THOR API method adlarına eşleyen sözlük
    ACTION_MAP = {
        "navigate": "MoveAhead",  # Not: Normalde Pathfinding (GetReachablePositions vb.) gerektirir, basitleştirildi.
        "pickup": "PickupObject",
        "put": "PutObject",
        "open": "OpenObject",
        "close": "CloseObject",
        "toggle-on": "ToggleObjectOn",
        "toggle-off": "ToggleObjectOff",
        "search": "LookDown" # Search aksiyonu için sembolik bir eşleştirme
    }

    def __init__(self, environment: ThorEnvironment):
        self.env = environment

    def execute_plan(self, grounded_actions: List[GroundedPDDLAction]) -> Tuple[bool, str, Optional[str]]:
        """
        Tüm aksiyonları sırayla simülasyona gönderir. 
        İlk başarısız adımda durur ve ExecutionError mesajı döner.
        """
        if not self.env.controller:
            raise SimulationExecutionError("Çevre (Environment) başlatılmamış. Lütfen önce env.start() çağırın.")

        for step_idx, action in enumerate(grounded_actions, start=1):
            success, msg = self._execute_single_action(action)
            
            if not success:
                error_feedback = (
                    f"Execution Failed at Step {step_idx}: [{action.to_pddl_sexpr()}]. "
                    f"Simulation Engine Error: {msg}"
                )
                error_predicate = f"(execution-failed {action.action_name} {' '.join(action.parameters)})"
                return False, error_feedback, error_predicate
                
        return True, "All actions executed successfully in AI2-THOR.", None

    def _execute_single_action(self, action: GroundedPDDLAction) -> Tuple[bool, str]:
        """Tek bir eylemi Thor API'sine uygun formata çevirir ve adım atar."""
        
        agent_name = action.parameters[0] # Örn: "Robot1"
        agent_id = self.env.get_agent_internal_id(agent_name)
        
        thor_action_name = self.ACTION_MAP.get(action.action_name)
        
        if not thor_action_name:
            return False, f"Bilinmeyen aksiyon eşleştirmesi: {action.action_name}"

        # API Parametrelerini Hazırlama
        step_params = {
            "action": thor_action_name,
            "agentId": agent_id
        }
        
        # Obje etkileşimi gerektiren aksiyonlar için objectId bulunması gerekir.
        # AI2-THOR'da objeler "Apple|-00.12|+00.85|-00.32" gibi spesifik ID'ler taşır.
        # Gerçek uygulamada metadata'dan visible_objects taraması yapılmalı.
        # Biz burada PDDL argümanını (Örn: 'apple') sembolik olarak gönderiyoruz,
        # 'objectId' gerektiren aksiyonlarda bunu Thor'un objectType aramasıyla simüle edeceğiz.
        
        if action.action_name in ["pickup", "open", "close", "toggle-on", "toggle-off"]:
            target_item = action.parameters[1]
            # Basit bir objectId eşleştirme simülasyonu (İlk görünen nesneyi bul):
            target_object_id = self._find_object_id_by_type(target_item, agent_id)
            if not target_object_id:
                return False, f"Görüş alanında etkileşime girilecek '{target_item}' bulunamadı."
            step_params["objectId"] = target_object_id

        # Simülasyon Adımı (Step)
        try:
            event = self.env.controller.step(**step_params)
            self.env.last_metadata = event.metadata
            
            if not event.metadata["lastActionSuccess"]:
                return False, event.metadata["errorMessage"]
                
            return True, "Success"
            
        except Exception as e:
            return False, str(e)
            
    def _find_object_id_by_type(self, object_type: str, agent_id: int) -> Optional[str]:
        """
        O anki ajanın gördüğü nesneler arasından (veya sahnedeki tüm nesnelerden) 
        istenen tipe (Örn: 'apple' -> 'Apple') uyan ilk nesnenin 'objectId'sini döndürür.
        """
        if not self.env.last_metadata:
            return None
            
        # Ajanın metadata'sına erişim (Çoklu ajanda 'agents' listesi döner)
        try:
            objects = self.env.last_metadata["agents"][agent_id]["objects"]
        except KeyError:
            # Tekil ajan durumunda veya farklı bir API versiyonunda doğrudan root'ta olabilir
            objects = self.env.last_metadata.get("objects", [])

        search_type = object_type.lower()
        
        for obj in objects:
            if obj["objectType"].lower() == search_type:
                return obj["objectId"]
                
        return None

# Adım 8 Canlı Simülasyon Testi
if __name__ == "__main__":
    import time

    print("AI2-THOR 3D Simülasyon Penceresi Başlatılıyor...")
    env = ThorEnvironment(scene="FloorPlan1", agent_count=2)

    try:
        env.start()
        runner = ActionRunner(env)

        # Örnek doğrulanan PDDL aksiyonları
        demo_actions = [
            GroundedPDDLAction("navigate", ["Robot1", "start", "forward"], 'Robot1.navigate("forward")'),
            GroundedPDDLAction("navigate", ["Robot2", "start", "forward"], 'Robot2.navigate("forward")'),
            GroundedPDDLAction("search", ["Robot1", "kitchen", "apple"], 'Robot1.search("kitchen", "apple")'),
        ]

        for act in demo_actions:
            print(f"Çalıştırılıyor: {act.to_pddl_sexpr()}")
            ok, msg = runner._execute_single_action(act)
            print(f"  -> Sonuç: {ok} ({msg})")
            time.sleep(1.0)  # Hareketi gözünle görebilmen için 1 saniye bekle

        input("\nSimülasyon çalışıyor! Pencereyi kapatmak için terminalde ENTER tuşuna bas...")

    finally:
        env.stop()