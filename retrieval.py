
import re
from index import get_collection, embed_texts

def search(query, k=5, design="semantic"):

    collection = get_collection()

    if collection.count() == 0:
        return []

    vector = embed_texts([query])[0]

    limit = k if design == "semantic" else k * 5

    results = collection.query(
        query_embeddings=[vector],
        n_results=min(limit, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    keywords = set(re.findall(r"\w+", query.lower()))

    for text, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        semantic_score = 1 - distance

        words = set(re.findall(r"\w+", text.lower()))

        keyword_score = len(keywords & words) / max(len(keywords), 1)

        score = semantic_score

        if design == "hybrid":
            score = 0.7 * semantic_score + 0.3 * keyword_score

        chunks.append({
            "text": text,
            "source": meta["source"],
            "page": meta["page"],
            "citation": f"[{meta['source']}, p. {meta['page']}]",
            "score": float(score)
        })

    chunks.sort(key=lambda x: x["score"], reverse=True)

    return chunks[:k]
