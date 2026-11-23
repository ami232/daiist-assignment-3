"""
Retrieval designs over the ChromaDB index (used by evaluate.py, and later by server.py).

A  baseline   : question as asked -> dense search
B  translated : Gemini Flash rewrites the question into German legal terms -> dense search
C  hybrid     : B's German query -> BM25 + dense, combined with reciprocal rank fusion (RRF)
D  diverse    : C's ranking, at most MAX_PER_DOC chunks per document in the final top k

Optional JSON caches for translations and query embeddings make reruns free.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections import Counter
from pathlib import Path

from google import genai
from google.genai import errors, types

import index
from api_key import load_api_key

TRANSLATE_MODEL = "gemini-3.8-flash"
DENSE_POOL = 50  # dense candidates fed into RRF
RRF_K = 60
MAX_PER_DOC = 2  # design D: at most this many chunks per document in the final top k

# Chosen design for server.py and agent.py: B at k=5. Main metric is "holding" (expected Rn./§ or the
# judgment's Leitsatz), since the agent can answer and cite from a Leitsatz; B leads there
# (91% overall, 71% multi-all at k=5) with fewer words than C. A, C, D stay in the evaluation.
DEFAULT_DESIGN = "B"
DEFAULT_K = 5

TRANSLATE_PROMPT = """You turn a landlord's question about German service charges (Betriebskosten, \
Nebenkostenabrechnung) into a German search query for a corpus of German statutes (BGB Mietrecht, \
BetrKV, HeizkostenV, CO2KostAufG) and BGH judgments.

Rules:
- Write one German query of 1-3 sentences, using the legal terms a statute or BGH judgment would use \
(e.g. Umlage, Betriebskosten, Vermieter, Mieter, Abrechnung, Wohnfläche).
- Keep every fact from the question. Do not answer it.
- Do not add § numbers, statute names or case numbers that are not in the question.
- Output only the query, no explanation.

Question: {question}"""


# ---------------------------------------------------------------- caching

class JsonCache:
    """A dict persisted to a JSON file after every write."""

    def __init__(self, path: Path | None):
        self.path = path
        self.data = json.loads(path.read_text(encoding="utf-8")) if path and path.is_file() else {}

    def get(self, key):
        return self.data.get(key)

    def put(self, key, value) -> None:
        self.data[key] = value
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")


def _key(*parts: str) -> str:
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()[:20]


_client: genai.Client | None = None


def client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


# ---------------------------------------------------------------- query side

def translate(question: str, cache: JsonCache | None = None) -> dict:
    """German legal query for a question: {"query", "input_tokens", "output_tokens", "seconds"}."""
    key = _key(TRANSLATE_MODEL, "thinking=low", TRANSLATE_PROMPT, question)
    if cache and (hit := cache.get(key)):
        return hit
    for attempt in range(6):
        try:
            started = time.time()
            response = client().models.generate_content(
                model=TRANSLATE_MODEL,
                contents=TRANSLATE_PROMPT.format(question=question),
                # a one-line rewrite needs little reasoning: "low" cut 9 s / ~1,000 tokens to 3 s / ~50 in a test
                config=types.GenerateContentConfig(temperature=0, thinking_config=types.ThinkingConfig(thinking_level="low")),
            )
            usage = response.usage_metadata
            result = {
                "query": (response.text or "").strip(),
                "input_tokens": usage.prompt_token_count or 0,
                "output_tokens": (usage.candidates_token_count or 0) + (getattr(usage, "thoughts_token_count", 0) or 0),
                "seconds": round(time.time() - started, 2),
            }
            break
        except errors.ClientError as error:
            if error.code != 429:
                raise
            index.log(f"translation rate limited, waiting {20 * (attempt + 1)}s")
            time.sleep(20 * (attempt + 1))
    else:
        raise RuntimeError("translation still rate limited")
    if cache:
        cache.put(key, result)
    return result


def embed_query(text: str, cache: JsonCache | None = None) -> list[float]:
    key = _key(index.EMBED_MODEL, "RETRIEVAL_QUERY", text)
    if cache and (hit := cache.get(key)):
        return hit
    vector = index.embed_texts(client(), [text], task="RETRIEVAL_QUERY")[0]
    if cache:
        cache.put(key, [round(v, 7) for v in vector])
    return vector


# ---------------------------------------------------------------- corpus side

class Corpus:
    """All stored chunks plus a BM25 index over their text."""

    STOP = set("der die das den dem des ein eine einer eines einem einen und oder zu zum zur im in an am auf "
               "für von mit bei nach ist sind wird werden wurde kann können nicht auch als dass sich es er sie "
               "wie so nur noch bis aus über vom durch hat haben sein war".split())

    def __init__(self, collection=None):
        self.collection = collection or index.get_collection()
        got = self.collection.get(include=["documents", "metadatas"])
        self.ids, self.docs, self.metas = got["ids"], got["documents"], got["metadatas"]
        self.pos = {cid: i for i, cid in enumerate(self.ids)}
        self._build_bm25()

    @classmethod
    def tokens(cls, text: str) -> list[str]:
        return [t for t in re.findall(r"\w+", text.lower()) if len(t) > 1 and t not in cls.STOP]

    def _build_bm25(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.tf = [Counter(self.tokens(d)) for d in self.docs]
        self.len = [sum(tf.values()) for tf in self.tf]
        self.avg_len = sum(self.len) / len(self.len)
        df = Counter(t for tf in self.tf for t in tf)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def bm25(self, query: str) -> list[int]:
        """Chunk positions ranked by BM25 score (only chunks sharing at least one term)."""
        terms = [t for t in self.tokens(query) if t in self.idf]
        scores = []
        for i, tf in enumerate(self.tf):
            s = 0.0
            for t in terms:
                f = tf.get(t, 0)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg_len))
            if s > 0:
                scores.append((s, i))
        return [i for _, i in sorted(scores, reverse=True)]

    def dense(self, vector: list[float], n: int) -> list[int]:
        res = self.collection.query(query_embeddings=[vector], n_results=min(n, len(self.ids)), include=[])
        return [self.pos[cid] for cid in res["ids"][0]]

    @staticmethod
    def rrf(*rankings: list[int], k: int = RRF_K) -> list[int]:
        score: dict[int, float] = {}
        for ranking in rankings:
            for rank, i in enumerate(ranking, 1):
                score[i] = score.get(i, 0.0) + 1 / (k + rank)
        return sorted(score, key=score.get, reverse=True)

    def diversify(self, ranked: list[int], k: int, max_per_doc: int) -> list[int]:
        """Walk the ranking, skipping chunks whose document already has max_per_doc chunks in the top k."""
        chosen: list[int] = []
        per_doc: Counter = Counter()
        for i in ranked:
            doc = self.metas[i]["doc_id"]
            if per_doc[doc] < max_per_doc:
                chosen.append(i)
                per_doc[doc] += 1
                if len(chosen) == k:
                    break
        return chosen

    def result(self, positions: list[int], k: int) -> list[dict]:
        return [{"id": self.ids[i], "text": self.docs[i], **self.metas[i]} for i in positions[:k]]


def search(corpus: Corpus, question: str, design: str = DEFAULT_DESIGN, k: int = DEFAULT_K,
           translations: JsonCache | None = None, embeddings: JsonCache | None = None) -> dict:
    """Top-k chunks for a question under design 'A', 'B' or 'C', plus the query actually used."""
    if design == "A":
        query, translation = question, None
    else:
        translation = translate(question, translations)
        query = translation["query"]
    vector = embed_query(query, embeddings)
    if design in ("A", "B"):
        positions = corpus.dense(vector, k)
    elif design == "C":
        positions = Corpus.rrf(corpus.dense(vector, DENSE_POOL), corpus.bm25(query))
    elif design == "D":
        ranked = Corpus.rrf(corpus.dense(vector, DENSE_POOL), corpus.bm25(query))
        positions = corpus.diversify(ranked, k, MAX_PER_DOC)
    else:
        raise ValueError(f"unknown design {design!r}")
    return {"query": query, "translation": translation, "chunks": corpus.result(positions, k)}
