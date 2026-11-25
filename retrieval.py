"""
Retrieval over the committed index. Shared by server.py (search tool) and evaluate.py.

Loads chunks_<design>.jsonl and the saved vectors; never embeds the corpus.
Only the query is embedded at search time (one call per question).
"""

import json
import sys
from pathlib import Path

import numpy as np

import index as ix


def embed_query(text: str) -> np.ndarray:
    """gemini-embedding-2 has no task_type: the task goes in the text. Truncated dims are normalised by Gemini."""
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    response = client.models.embed_content(
        model=ix.EMBED_MODEL,
        contents=[types.Content(parts=[types.Part(text=f"task: search result | query: {text}")])],
        config=types.EmbedContentConfig(output_dimensionality=ix.EMBED_DIMS))
    return np.array(response.embeddings[0].values, dtype=np.float32)


class Retriever:
    def __init__(self, design: str | None = None, embedder=embed_query):
        self.design = design or ix.load_manifest().get("default_design", ix.DEFAULT_DESIGN)
        self.embedder = embedder
        self.load()

    def load(self) -> None:
        path = ix.INDEX_DIR / f"chunks_{self.design}.jsonl"
        chunks = []
        if path.exists():
            with path.open(encoding="utf-8") as f:
                chunks = [json.loads(line) for line in f if line.strip()]
        vectors = ix.load_vectors()
        self.chunks = [c for c in chunks if c["key"] in vectors]
        missing = len(chunks) - len(self.chunks)
        if missing:
            print(f"retrieval: {missing} chunks have no vector and are ignored", file=sys.stderr)
        matrix = np.array([vectors[c["key"]] for c in self.chunks], dtype=np.float32)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True) if len(matrix) else matrix
        self.matrix = matrix / np.where(norms == 0, 1, norms) if len(matrix) else matrix

    def search(self, query: str, k: int = 5, source: str | None = None) -> list[dict]:
        """Top-k chunks by cosine similarity, optionally restricted to one source (metadata filter)."""
        if not len(self.chunks):
            return []
        q = self.embedder(query)
        q = q / (np.linalg.norm(q) or 1)
        scores = self.matrix @ q
        order = np.argsort(-scores)
        results = []
        for i in order:
            if source and self.chunks[i]["source"] != source:
                continue
            results.append({**self.chunks[i], "score": float(scores[i])})
            if len(results) == k:
                break
        return results

    def search_vector(self, q: np.ndarray, k: int = 5) -> list[dict]:
        """Same as search() with a precomputed query vector (evaluate.py embeds each question once)."""
        q = q / (np.linalg.norm(q) or 1)
        scores = self.matrix @ q
        return [{**self.chunks[i], "score": float(scores[i])} for i in np.argsort(-scores)[:k]]


def format_results(results: list[dict]) -> str:
    """Text the model reads: each chunk with a citation header it can copy."""
    if not results:
        return "No passages found: the index is empty."
    blocks = []
    for n, r in enumerate(results, start=1):
        cite = f"[{r['source']}, {r['location']}]"
        blocks.append(f"[{n}] {cite} (pp. {r['pages']}, score {r['score']:.2f})\n{r['text']}")
    return "\n\n".join(blocks)
