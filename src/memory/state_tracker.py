# Obje pozisyonlarındaki değişiklikleri RAG'a kaydeder
# src/memory/state_tracker.py

from datetime import datetime
from typing import Any, Dict, List, Optional

from src.memory.chromadb_client import VectorDatabaseClient
from src.validator.dsl_parser import WorldState


class StateTracker:
    """
    Ortamın başlangıç durumunu ve yürütme sırasındaki durum geçişlerini
    (H = {s_1, s_2, ..., s_t}) takip ederek ChromaDB RAG hafızasını günceller.
    """

    def __init__(self, db_client: VectorDatabaseClient):
        self.db = db_client
        self.history: List[Dict[str, Any]] = []
        self.step_counter: int = 0

    def record_world_state(self, world_state: WorldState, note: str = "State snapshot") -> str:
        """
        Sembolik WorldState nesnesini okunabilir durum metnine çevirir,
        geçmiş listesine (H) ekler ve ChromaDB'ye kaydeder.
        """
        self.step_counter += 1
        timestamp = datetime.now().strftime("%H:%M:%S")

        facts_text = ", ".join(f"({' '.join(p)})" for p in sorted(world_state.predicates))
        summary = f"[t={self.step_counter} | {timestamp}] ({note}) World Facts: {facts_text}"

        self.history.append({
            "step": self.step_counter,
            "timestamp": timestamp,
            "note": note,
            "summary": summary
        })

        # ChromaDB'de hem zaman damgalı geçmiş kaydı tut hem de güncel durumu (current_world_state) güncelle
        self.db.collection.upsert(
            documents=[summary],
            metadatas=[{
                "type": "state_history",
                "step": self.step_counter,
                "note": note
            }],
            ids=[f"state_t{self.step_counter}"]
        )

        self.db.collection.upsert(
            documents=[summary],
            metadatas=[{
                "type": "current_state",
                "step": self.step_counter
            }],
            ids=["current_world_state"]
        )

        return summary

    def record_thor_metadata_update(self, metadata: Dict[str, Any], action_desc: str) -> str:
        """
        AI2-THOR simülasyon adımından dönen metadata'dan önemli nesne durumlarını
        (ör. açık/kapalı kapaklar, tutulan nesneler) çıkarıp RAG hafızasına yazar.
        """
        self.step_counter += 1
        timestamp = datetime.now().strftime("%H:%M:%S")

        observed_states: List[str] = []
        objects = metadata.get("objects", [])
        if not objects and "agents" in metadata and metadata["agents"]:
            objects = metadata["agents"][0].get("objects", [])

        for obj in objects:
            obj_type = obj.get("objectType", "Unknown")
            if obj.get("isPickedUp"):
                observed_states.append(f"{obj_type} is currently held by agent")
            if obj.get("openable"):
                status = "opened" if obj.get("isOpen") else "closed"
                observed_states.append(f"{obj_type} is {status}")

        obs_text = "; ".join(observed_states[:15]) if observed_states else "No notable state changes"
        summary = f"[t={self.step_counter} | {timestamp}] After '{action_desc}': {obs_text}"

        self.history.append({
            "step": self.step_counter,
            "timestamp": timestamp,
            "note": action_desc,
            "summary": summary
        })

        self.db.collection.upsert(
            documents=[summary],
            metadatas={
                "type": "thor_state_update",
                "step": self.step_counter
            },
            ids=[f"thor_state_t{self.step_counter}"]
        )
        return summary

    def record_discovered_constraint(self, constraint_text: str, predicate: str):
        """
        Doğrulama veya yürütme sırasında keşfedilen yeni bir çevresel kısıtı
        (örn. 'Fridge is closed') RAG hafızasına kalıcı bilgi olarak ekler.
        """
        self.step_counter += 1
        doc_id = f"discovered_constraint_{self.step_counter}"
        full_text = f"Environmental Constraint Discovered: {constraint_text} | PDDL Predicate: {predicate}"

        self.db.collection.upsert(
            documents=[full_text],
            metadatas=[{
                "type": "environmental_constraint",
                "predicate": predicate
            }],
            ids=[doc_id]
        )

    def get_latest_state_summary(self) -> str:
        """En son kaydedilen çevresel durum özetini döndürür."""
        if not self.history:
            return "No prior state history recorded."
        return self.history[-1]["summary"]