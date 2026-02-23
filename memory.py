import chromadb
from sentence_transformers import SentenceTransformer

_client = chromadb.PersistentClient(path="./chroma_db")
_model = SentenceTransformer("all-MiniLM-L6-v2")


def _collection(user_id: int):
    return _client.get_or_create_collection(f"user_{user_id}")


def add(user_id: int, text: str):
    col = _collection(user_id)
    idx = str(col.count())
    col.add(
        ids=[idx],
        embeddings=[_model.encode(text).tolist()],
        documents=[text],
    )


def search(user_id: int, query: str, k: int = 5) -> list[str]:
    col = _collection(user_id)
    if col.count() == 0:
        return []
    results = col.query(
        query_embeddings=[_model.encode(query).tolist()],
        n_results=min(k, col.count()),
    )
    return results["documents"][0]
