import re

from rank_bm25 import BM25Okapi

from index import collection, embed

RRF_K = 60  # standard fusion constant

# chosen in evaluate.py
DESIGN = "fixed"
HYBRID = True
TOP_K = 5


def tokens(text):
    return re.findall(r"[a-z]+", text.lower())


class Retriever:
    def __init__(self, design, hybrid=False):
        self.design = design
        self.hybrid = hybrid
        self.store = collection(design)
        everything = self.store.get(include=["documents"])
        self.ids = everything["ids"]
        # keyword search for hybrid
        self.bm25 = BM25Okapi([tokens(d) for d in everything["documents"]]) if hybrid else None

    def search(self, query, k=5, vector=None):
        vector = vector or embed([query], "RETRIEVAL_QUERY")[0]
        found = self.store.query(query_embeddings=[vector], n_results=len(self.ids), include=["documents", "metadatas", "distances"])
        chunks = [
            {"id": i, "text": d, **m, "similarity": round(1 - dist, 3)}
            for i, d, m, dist in zip(found["ids"][0], found["documents"][0], found["metadatas"][0], found["distances"][0])
        ]
        if self.hybrid:
            vector_rank = {c["id"]: rank for rank, c in enumerate(chunks)}
            keyword_rank = {self.ids[i]: rank for rank, i in enumerate(self.bm25.get_scores(tokens(query)).argsort()[::-1])}
            # reciprocal rank fusion
            chunks.sort(key=lambda c: -(1 / (RRF_K + vector_rank[c["id"]]) + 1 / (RRF_K + keyword_rank[c["id"]])))
        return chunks[:k]
