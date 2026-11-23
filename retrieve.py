"""Retrieval over the saved index. Shared by server.py and evaluate.py."""

from google import genai

from api_key import load_api_key
from index import embed_texts, get_collection

DEFAULT_DESIGN = "section"
_client = None


def _gemini():
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def retrieve(query: str, k: int = 5, design: str = DEFAULT_DESIGN) -> list[dict]:
    """The k chunks closest to the query: text, source, location and distance (lower = closer)."""
    vector = embed_texts(_gemini(), [query])[0]
    found = get_collection(design).query(
        query_embeddings=[vector], n_results=k, include=["documents", "metadatas", "distances"]
    )
    return [
        {"text": text, "source": meta["source"], "location": meta["location"], "distance": dist}
        for text, meta, dist in zip(found["documents"][0], found["metadatas"][0], found["distances"][0])
    ]