"""
Búsqueda sobre el índice (la usan server.py y evaluate.py).

Tres métodos sobre la MISMA colección de fragmentos:
  - dense : embedding de la pregunta vs. embeddings de los fragmentos (similitud coseno, ChromaDB)
  - bm25  : coincidencia de palabras clave (Okapi BM25, implementado aquí abajo)
  - hybrid: fusiona los dos rankings con Reciprocal Rank Fusion (RRF)

Y un filtro opcional por licitación: si la pregunta nombra una (p. ej. "Cartagena"),
solo se buscan fragmentos de esa licitación.

Los embeddings de las preguntas se guardan en index/query_cache.json: repetir una
pregunta (evaluación, check.py) no gasta cuota, y el servidor puede contestar
preguntas ya vistas aunque no tenga la API key.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
import threading
import unicodedata
from collections import Counter

import config

# Una cita es "doc_id, p. N" dentro de corchetes. El modelo a veces agrupa varias en el
# mismo corchete ("[cartagena_pcap, p. 21, enisa_pcap, p. 31]" o con ";"): las contamos todas.
BRACKET_RE = re.compile(r"\[([^\[\]]{3,300})\]")
CITE_PAIR_RE = re.compile(r"([a-z0-9_]+),\s*p(?:ág)?\.?\s*(\d+)(?:\s*[-–]\s*\d+)?", re.I)


def find_citations(text: str) -> list[tuple[str, int]]:
    """Todas las citas (doc_id, página) de un texto, también las agrupadas en un corchete."""
    return [(d, int(p)) for group in BRACKET_RE.findall(text) for d, p in CITE_PAIR_RE.findall(group)]

STOPWORDS = set("""
a al algo algunas algunos ante antes como con contra cual cuales cuando de del desde donde dos
el ella ellas ellos en entre era es esa esas ese eso esos esta estas este esto estos fue ha han
hasta hay la las le les lo los mas me mi mis muy ni no nos o os otra otras otro otros para pero
poco por porque que quien se sea segun ser si sin sobre su sus tambien te tiene tienen todo
todos tu un una uno unos y ya cual cuanto cuantos cuantas qué cuál cómo
""".split())


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"\w+", normalize(text)) if len(t) > 1 and t not in STOPWORDS]


class BM25:
    """Okapi BM25: puntúa un fragmento por las palabras de la pregunta que contiene,
    dando más peso a palabras raras en el corpus (IDF) y normalizando por longitud."""

    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tfs = [Counter(tokenize(d)) for d in docs]
        self.lens = [sum(tf.values()) for tf in self.tfs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter(t for tf in self.tfs for t in tf)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query: str) -> list[float]:
        q = tokenize(query)
        out = []
        for tf, length in zip(self.tfs, self.lens):
            s = 0.0
            for t in q:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            out.append(s)
        return out


# --------------------------------------------------------------------------------------
# Embedding de la pregunta (con caché en disco)
# --------------------------------------------------------------------------------------
_cache: dict | None = None
_cache_lock = threading.Lock()


def _cache_key(query: str) -> str:
    return f"{config.EMBED_MODEL}|{config.EMBED_DIM}|{query.strip()}"


def load_query_cache() -> dict:
    global _cache
    with _cache_lock:
        if _cache is None:
            try:
                _cache = json.loads(config.QUERY_CACHE.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                _cache = {}
        return _cache


def embed_query(query: str) -> list[float] | None:
    """Vector de la pregunta. None si no está en caché y no hay API key / cuota."""
    cache = load_query_cache()
    key = _cache_key(query)
    if key in cache:
        return cache[key]
    try:
        from index import embed_texts, query_text_for_embedding

        vector = embed_texts([query_text_for_embedding(query)])[0]
    except Exception as e:  # noqa: BLE001 - sin key o sin cuota: seguimos solo con BM25
        log(f"[retrieval] No pude embeber la pregunta ({type(e).__name__}: {str(e)[:120]}). Uso solo BM25.")
        return None
    # El agente puede lanzar varias búsquedas A LA VEZ (p. ej. una por licitación) y el
    # servidor las atiende en hilos paralelos: el candado evita que dos hilos escriban la
    # caché al mismo tiempo, y un fallo al guardarla nunca debe romper la búsqueda.
    with _cache_lock:
        cache[key] = vector
        try:
            tmp = config.QUERY_CACHE.with_name(f"query_cache.{os.getpid()}.{threading.get_ident()}.tmp")
            tmp.write_text(json.dumps(cache), encoding="utf-8")
            tmp.replace(config.QUERY_CACHE)   # escritura atómica: nunca queda un JSON a medias
        except OSError as e:
            log(f"[retrieval] No pude guardar la caché de preguntas ({e}); sigo sin guardarla.")
    return vector


# --------------------------------------------------------------------------------------
# El buscador
# --------------------------------------------------------------------------------------
class Retriever:
    def __init__(self, design: str | None = None):
        from index import get_collection

        self.design = design or config.CHOSEN_DESIGN
        self.collection = get_collection(self.design)
        self.reload()

    def reload(self) -> None:
        """Lee todos los fragmentos (texto + metadatos) para BM25 y los filtros."""
        data = self.collection.get(include=["documents", "metadatas"])
        self.ids = data["ids"]
        self.texts = data["documents"]
        self.metas = data["metadatas"]
        self.pos = {cid: i for i, cid in enumerate(self.ids)}
        # BM25 indexa también el título del documento y el apartado
        self.bm25 = BM25([f"{m['title']} {m['section']} {t}" for t, m in zip(self.texts, self.metas)])
        self.tenders = {}
        for m in self.metas:
            if m.get("tender_key"):
                self.tenders.setdefault(m["tender_key"], {"buyer": m["buyer"], "tender_id": m["tender_id"],
                                                          "aliases": m["aliases"].split("|")})

    # --- filtro por licitación --------------------------------------------------------
    def detect_tender(self, text: str) -> str | None:
        """Devuelve la licitación que nombra el texto (si nombra exactamente una)."""
        t = normalize(text)
        found = {key for key, info in self.tenders.items()
                 if key in t or any(normalize(a) in t for a in info["aliases"])}
        return found.pop() if len(found) == 1 else None

    def _allowed(self, tender: str | None) -> list[int]:
        if not tender:
            return list(range(len(self.ids)))
        return [i for i, m in enumerate(self.metas) if m.get("tender_key") == tender]

    # --- métodos ---------------------------------------------------------------------
    def dense(self, query: str, k: int, tender: str | None = None) -> list[tuple[int, float]]:
        vector = embed_query(query)
        if vector is None or not self.ids:
            return []
        res = self.collection.query(
            query_embeddings=[vector], n_results=min(k, len(self.ids)),
            where={"tender_key": tender} if tender else None, include=["distances"],
        )
        return [(self.pos[cid], 1 - dist) for cid, dist in zip(res["ids"][0], res["distances"][0])]

    def keyword(self, query: str, k: int, tender: str | None = None) -> list[tuple[int, float]]:
        scores = self.bm25.scores(query)
        allowed = self._allowed(tender)
        ranked = sorted(allowed, key=lambda i: scores[i], reverse=True)
        return [(i, scores[i]) for i in ranked[:k] if scores[i] > 0]

    def hybrid(self, query: str, k: int, tender: str | None = None, pool: int = 30, c: int = 60) -> list[tuple[int, float]]:
        """Reciprocal Rank Fusion: score = sum 1/(c + rango) en cada lista."""
        fused = Counter()
        for ranking in (self.dense(query, pool, tender), self.keyword(query, pool, tender)):
            for rank, (i, _) in enumerate(ranking, 1):
                fused[i] += 1 / (c + rank)
        return fused.most_common(k)

    def search(self, query: str, k: int = config.TOP_K, method: str | None = None,
               tender: str | None = None, auto_filter: bool | None = None) -> tuple[list[dict], str | None]:
        """Devuelve (fragmentos, licitación usada como filtro)."""
        method = method or config.CHOSEN_METHOD
        auto_filter = config.CHOSEN_TENDER_FILTER if auto_filter is None else auto_filter
        if tender:
            tender = self.detect_tender(tender) or (tender if tender in self.tenders else None)
        elif auto_filter:
            tender = self.detect_tender(query)
        ranking = {"dense": self.dense, "bm25": self.keyword, "hybrid": self.hybrid}[method](query, k, tender)
        if method == "dense" and not ranking:      # sin embedding: plan B
            ranking = self.keyword(query, k, tender)
        hits = []
        for i, score in ranking:
            m = self.metas[i]
            hits.append({"id": self.ids[i], "text": self.texts[i], "score": round(float(score), 4), **m})
        return hits, tender


def format_hits(query: str, hits: list[dict], tender: str | None) -> str:
    """Texto que devuelve la herramienta search. Cada bloque dice CÓMO citarlo."""
    if not hits:
        return (f"No hay fragmentos para «{query}». "
                f"Si la pregunta no está cubierta, responde: «{config.REFUSAL_PHRASE}».")
    head = f"{len(hits)} fragmentos para «{query}»" + (f" (filtrados por la licitación «{tender}»)" if tender else "")
    blocks = [head]
    for n, h in enumerate(hits, 1):
        pages = f"{h['page_start']}" if h["page_start"] == h["page_end"] else f"{h['page_start']}-{h['page_end']}"
        blocks.append(
            f"[{n}] Cita: [{h['doc_id']}, p. {h['page_start']}]\n"
            f"Documento: {h['title']}\n"
            f"Apartado: {h['section'] or '(sin título)'} | Páginas: {pages}\n"
            f"Texto: {h['text']}"
        )
    return "\n\n---\n\n".join(blocks)


HIT_RE = re.compile(r"\[\d+\] Cita: \[([a-z0-9_]+), p\. (\d+)\]\nDocumento: ([^\n]*)\nApartado: ([^\n]*) \| Páginas: (\d+)(?:-(\d+))?\nTexto: (.*?)(?=\n\n---\n\n|\Z)", re.S)


def parse_hits(tool_output: str) -> list[dict]:
    """Inversa de format_hits: el agente y la evaluación recuperan qué fragmentos vio el modelo."""
    out = []
    for m in HIT_RE.finditer(tool_output):
        out.append({"doc_id": m.group(1), "page_start": int(m.group(5)), "page_end": int(m.group(6) or m.group(5)),
                    "title": m.group(3), "section": m.group(4), "text": m.group(7).strip()})
    return out


def citation_is_valid(doc_id: str, page: int, retrieved: list[dict]) -> bool:
    return any(h["doc_id"] == doc_id and h["page_start"] <= page <= h["page_end"] for h in retrieved)
