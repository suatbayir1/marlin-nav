# Geçmiş state ve wiki.md'leri birleştirip LLM'e bağlam sunar
import os
from pathlib import Path

try:
    from .chromadb_client import VectorDatabaseClient
except ImportError:
    from chromadb_client import VectorDatabaseClient

class ContextBuilder:
    def __init__(self, db_client: VectorDatabaseClient, wiki_base_dir: str = None):
        """
        RAG tabanlı bağlam oluşturucu. Statik Wiki kurallarını ve dinamik ortam
        durumlarını (state history) birleştirerek LLM prompt'u için hazırlar.
        """
        self.db = db_client
        self.wiki_dir = self._resolve_wiki_path(wiki_base_dir)

    def _resolve_wiki_path(self, custom_path: str = None) -> Path:
        """Wiki klasörünün yolunu (wiki/ veya data/wiki/) otomatik bulur."""
        project_root = Path(__file__).resolve().parents[2]

        if custom_path:
            candidate = Path(custom_path).expanduser()
            if not candidate.is_absolute():
                candidate = project_root / candidate
            if candidate.exists():
                return candidate.resolve()

        candidates = [
            project_root / "data/wiki",
            project_root / "wiki",
            Path.cwd() / "data/wiki",
            Path.cwd() / "wiki",
        ]
        for path in candidates:
            if path.exists() and path.is_dir():
                return path.resolve()
        return (project_root / "data/wiki").resolve()

    def ingest_wiki_knowledge(self) -> int:
        """
        ai2thor_api ve pddl_mappings klasörlerindeki tüm .md dosyalarını okur
        ve ChromaDB vektör veritabanına kaydeder (upsert).
        """
        subfolders = {
            "ai2thor_api": "api_documentation",
            "pddl_mappings": "pddl_mapping"
        }

        documents = []
        metadatas = []
        ids = []

        for folder_name, doc_type in subfolders.items():
            target_dir = self.wiki_dir / folder_name
            if not target_dir.exists():
                print(f"Uyarı: {target_dir} klasörü bulunamadı, atlanıyor.")
                continue

            for md_file in sorted(target_dir.glob("*.md")):
                content = md_file.read_text(encoding="utf-8").strip()
                if not content:
                    continue

                action_name = md_file.stem  # Örn: "MoveAhead"
                doc_id = f"{doc_type}_{action_name}"

                documents.append(content)
                metadatas.append({
                    "type": doc_type,
                    "action_name": action_name,
                    "source": str(md_file)
                })
                ids.append(doc_id)

        if not documents:
            print("Yüklenecek .md dosyası bulunamadı. Klasör yolunu kontrol edin.")
            return 0

        # 'add' yerine 'upsert' kullanıyoruz; böylece scripti tekrar çalıştırırsan
        # "Duplicate ID" hatası vermez, mevcut kayıtları günceller.
        self.db.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Toplam {len(documents)} Wiki (.md) belgesi ChromaDB'ye başarıyla işlendi.")
        return len(documents)

    def build_context(self, task_instruction: str, current_state: str = "", n_results: int = 4) -> str:
        """
        Kullanıcı talimatına en uygun AI2-THOR aksiyonlarını, PDDL ön koşullarını
        ve varsa geçmiş durum kayıtlarını RAG üzerinden çekip tek bir metin haline getirir.
        """
        search_query = f"{task_instruction} {current_state}".strip()
        retrieved_docs = self.db.query_context(query_text=search_query, n_results=n_results)

        context_sections = ["### RETRIEVED ENVIRONMENT RULES & PDDL MAPPINGS (RAG) ###"]
        if retrieved_docs:
            for idx, doc in enumerate(retrieved_docs, start=1):
                context_sections.append(f"--- Reference {idx} ---\n{doc}")
        else:
            context_sections.append("No relevant documentation found in memory.")

        if current_state:
            context_sections.append(f"\n### CURRENT & HISTORICAL ENVIRONMENT STATE ###\n{current_state}")

        return "\n\n".join(context_sections)


# Adım 3 Test Bloğu
if __name__ == "__main__":
    print("1. ChromaDB istemcisi başlatılıyor...")
    project_root = Path(__file__).resolve().parents[2]
    db_client = VectorDatabaseClient(persist_directory=str(project_root / "chroma_db"))

    print("2. Wiki dosyaları okunuyor ve vektör veritabanına gömülüyor...")
    builder = ContextBuilder(db_client=db_client)
    loaded_count = builder.ingest_wiki_knowledge()

    if loaded_count > 0:
        sample_task = "Move forward to the kitchen and pick up the apple."
        print(f"\n3. Örnek Sorgu Test Ediliyor: '{sample_task}'\n")
        context_output = builder.build_context(
            task_instruction=sample_task,
            current_state="Agent1 is at kitchen_entrance. Apple is on the countertop.",
            n_results=3
        )
        print(context_output)