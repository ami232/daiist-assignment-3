import chromadb
from google import genai
from google.genai import types

from api_key import load_api_key
from index import INDEX_DIR, COLLECTION_NAME, MODEL, DIMENSIONS


def search(query, k=5):
    """Retrieve the k most relevant document chunks."""

    db = chromadb.PersistentClient(
        path=str(INDEX_DIR)
    )

    collection = db.get_collection(
        name=COLLECTION_NAME
    )

    client = genai.Client(
        api_key=load_api_key()
    )

    response = client.models.embed_content(
        model=MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            output_dimensionality=DIMENSIONS
        ),
    )

    query_vector = response.embeddings[0].values

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []

    for chunk_id, text, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append({
            "id": chunk_id,
            "text": text,
            "source": metadata["source"],
            "article": metadata["article"],
            "page_start": metadata["page_start"],
            "page_end": metadata["page_end"],
            "distance": distance,
        })

    return retrieved


if __name__ == "__main__":

    question = (
        "What is the deadline for notifying "
        "a personal data breach under the GDPR?"
    )

    print(f"\nQuestion: {question}\n")

    results = search(question, k=5)

    for rank, result in enumerate(results, start=1):
        print(f"{'=' * 55}")
        print(f"RANK {rank}")
        print(
            f"Source: {result['source']} | "
            f"Article: {result['article']} | "
            f"Page: {result['page_start']}"
        )
        print(f"Distance: {result['distance']:.4f}")
        print(f"Text: {result['text'][:350]}...\n")
