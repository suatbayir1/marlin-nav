# Sadece vektör veritabanı bağlantısı ve sorguları yönetir
import os
import chromadb
from chromadb.utils import embedding_functions

class VectorDatabaseClient:
    def __init__(self, persist_directory="./chroma_db", collection_name="ai2thor_knowledge"):
        """
        ChromaDB istemcisini başlatır. Veritabanını diske kaydeder (persist) 
        böylece her seferinde verileri baştan yüklemek zorunda kalmayız.
        """
        try:
            self.client = chromadb.PersistentClient(path=persist_directory)
        except Exception as exc:
            raise RuntimeError(
                f"ChromaDB istemcisi başlatılamadı: {exc}"
            ) from exc
        
        # Varsayılan olarak all-MiniLM-L6-v2 modelini kullanır (hafif ve hızlıdır).
        # Daha sonra Türkçe veya farklı modeller için değiştirilebilir.
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Koleksiyonu oluşturur (varsa alır)
        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_fn
            )
        except KeyError as exc:
            raise RuntimeError(
                "ChromaDB koleksiyon yapılandırması eski veya uyumsuz. "
                f"Depoyu silip yeniden oluşturun: rm -rf {persist_directory}"
            ) from exc

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        """
        Wiki (.md) belgelerini veya ortam durumlarını vektör veritabanına ekler.
        
        :param documents: Metin içeriklerinin listesi (Örn: MoveAhead.md'nin içi).
        :param metadatas: Her belge için üst veriler (Örn: {"type": "action", "name": "MoveAhead"}).
        :param ids: Her belge için benzersiz kimlikler (Örn: "doc_MoveAhead").
        """
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Başarıyla {len(documents)} belge veritabanına eklendi.")
        except Exception as e:
            print(f"Belgeler eklenirken hata oluştu: {e}")

    def query_context(self, query_text: str, n_results: int = 3) -> list[str]:
        """
        Verilen bir doğal dil komutuna veya duruma en yakın (alakalı) belgeleri getirir.
        Bu fonksiyon, RAG modülünde LLM'e context (bağlam) sağlamak için kullanılacaktır.
        
        :param query_text: Kullanıcının komutu (Örn: "Buzdolabındaki elmayı al").
        :param n_results: Getirilecek en alakalı belge sayısı.
        :return: Alakalı metinlerin listesi.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        if results and results['documents']:
            # İlk sorgunun sonuçlarını dönüyoruz
            return results['documents'][0]
        return []

    def update_document(self, id: str, document: str, metadata: dict):
        """
        Var olan bir belgeyi (özellikle ortam durumlarını / state updates) günceller.
        """
        self.collection.update(
            ids=[id],
            documents=[document],
            metadatas=[metadata]
        )
        print(f"Belge güncellendi: {id}")
        
    def delete_collection(self):
        """Koleksiyonu siler (Testler için faydalı olabilir)."""
        self.client.delete_collection(name=self.collection.name)
        print("Koleksiyon silindi.")

# Test için ufak bir kullanım örneği:
# if __name__ == "__main__":
    # db = VectorDatabaseClient()
    # db.add_documents(
    #     documents=["Elma buzdolabının içinde.", "Kitap masanın üzerinde."],
    #     metadatas=[{"item": "apple"}, {"item": "book"}],
    #     ids=["state_apple", "state_book"]
    # )
    # print(db.query_context("Elma nerede?"))