import chromadb
from app.config import settings

class VectorService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(name="student_bios")

    def upsert_student_bio(self, student_id: int, bio_notes: str, metadata: dict):
        if not bio_notes:
            self.delete_student_bio(student_id)
            return
        self.collection.upsert(
            documents=[bio_notes],
            metadatas=[metadata],
            ids=[str(student_id)]
        )

    def delete_student_bio(self, student_id: int):
        try:
            self.collection.delete(ids=[str(student_id)])
        except Exception:
            pass

    def search_similar_students(self, query: str, limit: int = 3):
        return self.collection.query(
            query_texts=[query],
            n_results=limit
        )

vector_service = VectorService()