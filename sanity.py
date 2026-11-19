"""
Part 3e: sanity check of the index. Not part of the final system.

Asks a few questions in Spanish and prints the 3 closest chunks of each design,
so YOU can judge whether the right article comes back. Uses 6 embeddings.
Run:  uv run python sanity.py
"""

import index as ix

QUESTIONS = [
    "¿Cuántos días de vacaciones tengo al año?",
    "¿Cuál es el salario mínimo interprofesional diario en 2026?",
    "¿Cuántas horas de trabajo al año marca el convenio?",
    "¿Cuánto dura el periodo de prueba?",
    "¿Cuántos días de preaviso tengo que dar si quiero dejar el trabajo?",
    "¿Cuál es el salario por hora de un soldador en Alemania?",  # NOT in the corpus
]


def top(chunks, matrix, query_vector, k=3):
    scores = matrix @ query_vector            # unit vectors: dot product = cosine similarity
    best = scores.argsort()[::-1][:k]
    return [(float(scores[i]), chunks[i]) for i in best]


def main(client=None) -> None:
    client = client or ix.make_client()
    indexes = {d: ix.load_index(d) for d in ("A", "B")}
    for d, (chunks, _) in indexes.items():
        print(f"design {d}: {len(chunks)} chunks with a vector")
    for question in QUESTIONS:
        print(f"\n=== {question}")
        q = ix.embed_query(question, client)
        for d, (chunks, matrix) in indexes.items():
            print(f"  design {d}")
            for score, c in top(chunks, matrix, q):
                body = c["text"].split("\n", 1)[-1].replace("\n", " ")
                print(f"    {score:.3f}  {c['source']:<9} {c['location']:<28} {body[:90]}...")


if __name__ == "__main__":
    main()
