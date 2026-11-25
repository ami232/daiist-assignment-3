"""Reproducible Python-reference RAG pipeline shared by index.ipynb and server.py.

SQLite persists text and (when a key is supplied) Gemini float32 embeddings.
No embedding call occurs on import, server startup or repeated indexing.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sqlite3
import sys
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES_DIR = ROOT / 'source_docs'
INDEX_DIR = Path(os.environ.get('RAG_INDEX_DIR', str(ROOT / 'index'))).resolve()
DB_NAME = 'corpus.sqlite3'
EMBED_MODEL = 'gemini-embedding-2'
EMBED_DIMS = 768
CHAT_MODEL = 'gemini-3.5-flash-lite'   # agent (agent.py)
JUDGE_MODEL = 'gemini-3.5-flash-lite'  # LLM judge (evaluation_core.py)
WORD_RE = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*|\d+(?:\.\d+)?")
TOPIC_RE = re.compile(r'^### TOPIC: ([a-z0-9_-]+)\s*$', re.M)
ACCEPTED_TYPES = {'.md', '.txt', '.pdf', '.html', '.htm'}


def get_conn(db_path: Path | None = None) -> sqlite3.Connection:
    """Create/load the persisted index. No network or embedding API calls."""
    path = db_path or (INDEX_DIR / DB_NAME)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=DELETE')
    conn.execute('PRAGMA busy_timeout=30000')
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS chunks (
          id TEXT PRIMARY KEY, source TEXT NOT NULL, location TEXT NOT NULL,
          url TEXT NOT NULL, filepath TEXT NOT NULL, text TEXT NOT NULL,
          n_words INTEGER NOT NULL, vector BLOB, embedding_model TEXT
        );
        CREATE INDEX IF NOT EXISTS chunks_source_idx ON chunks(source, location);
        CREATE TABLE IF NOT EXISTS documents (
          filepath TEXT PRIMARY KEY, sha256 TEXT NOT NULL,
          source TEXT NOT NULL, url TEXT NOT NULL, n_chunks INTEGER NOT NULL
        );
    ''')
    return conn


def clean_text(text: str) -> str:
    """Remove control characters, page noise and soft hyphenation, keep code indents."""
    text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\u00ad', '')
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)  # PDF line-break hyphenation
    text = re.sub(r'[\t ]+\n', '\n', text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return ''.join(ch for ch in text if ch in '\n\t' or ord(ch) >= 32).strip()


def read_document(path: Path) -> list[tuple[str, str]]:
    """Return (location, text) sections from text, HTML or paginated PDF."""
    suffix = path.suffix.lower()
    if suffix not in ACCEPTED_TYPES:
        raise ValueError(f'Unsupported document format: {suffix}; allowed {sorted(ACCEPTED_TYPES)}')
    if suffix == '.pdf':
        from pypdf import PdfReader
        sections = []
        for i, page in enumerate(PdfReader(str(path)).pages, 1):
            extracted = clean_text(page.extract_text() or '')
            if extracted:
                sections.append((f'page:{i}', extracted))
        return sections
    text = path.read_text(encoding='utf-8-sig')
    if suffix in {'.html', '.htm'}:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        text = soup.get_text('\n', strip=True)
    matches = list(TOPIC_RE.finditer(text))
    if not matches:
        return [('section:full-text', clean_text(text))]
    sections = []
    for i, match in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        body = clean_text(text[match.end():end])
        if body:
            sections.append((f'topic:{match.group(1)}', body))
    return sections


def split_section(text: str, max_words: int = 390, overlap_words: int = 45) -> list[str]:
    """Paragraph-aware chunks with modest overlap, preserving code where possible."""
    if max_words <= overlap_words or overlap_words < 0:
        raise ValueError('max_words must exceed nonnegative overlap_words')
    paras = [p.strip('\n') for p in re.split(r'\n\s*\n', text) if p.strip()]
    units = []
    for p in paras:
        if len(p.split()) <= max_words:
            units.append(p)
        else:
            # Break unusually long prose paragraphs at physical lines if possible.
            lines = p.splitlines()
            if len(lines) > 1 and max(len(line.split()) for line in lines) < max_words:
                working = []
                for line in lines:
                    if len(' '.join(working + [line]).split()) > max_words and working:
                        units.append('\n'.join(working)); working = []
                    working.append(line)
                if working:
                    units.append('\n'.join(working))
            else:
                words = p.split()
                for start in range(0, len(words), max_words):
                    units.append(' '.join(words[start:start+max_words]))
    chunks, current = [], []
    for unit in units:
        if current and len((' '.join(current) + ' ' + unit).split()) > max_words:
            saved = '\n\n'.join(current)
            chunks.append(saved)
            # Carry short context from the immediately preceding chunk.
            # The next paragraph itself may be almost max_words long; keep
            # only as much overlap as fits the strict max-word budget.
            space_for_overlap = max(0, max_words - len(unit.split()))
            tail = saved.split()[-min(overlap_words, space_for_overlap):] if overlap_words and space_for_overlap else []
            current = [' '.join(tail)] if tail else []
        current.append(unit)
    if current:
        chunks.append('\n\n'.join(current))
    return [c for c in chunks if len(c.split()) >= 5]


def manifest_map() -> dict[str, dict]:
    manifest = SOURCES_DIR / 'manifest.json'
    if not manifest.exists():
        return {}
    return {item['file']: item for item in json.loads(manifest.read_text(encoding='utf-8'))}


def chunk_file(path: str | Path, *, max_words: int = 390,
               overlap_words: int = 45) -> list[dict]:
    """Extract a document into stable, cited chunks; used by both ingestion paths."""
    path = Path(path).expanduser().resolve(strict=True)
    manifest = manifest_map().get(path.name) if path.parent == SOURCES_DIR.resolve() else None
    source = manifest['source'] if manifest else path.stem
    url = manifest['url'] if manifest else path.as_uri()
    if not manifest and path.suffix.lower() in {'.md', '.txt'}:
        # Optional provenance line in user-provided notes (still untrusted).
        header = path.read_text(encoding='utf-8-sig')[:1000]
        provenance = re.search(r'^Source URL:\s*(https?://\S+)', header, flags=re.M)
        if provenance:
            url = provenance.group(1)
    stable_filepath = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    chunks = []
    for location, section in read_document(path):
        for i, part in enumerate(split_section(section, max_words, overlap_words)):
            # A section's identifier is stable across separate runs.
            identity = f'{source}\0{location}\0{i}\0{part}'
            chunk_id = hashlib.sha256(identity.encode('utf-8')).hexdigest()[:20]
            chunks.append(dict(id=chunk_id, source=source, location=location,
                               url=url, filepath=stable_filepath, text=part,
                               n_words=len(part.split())))
    return chunks


def _fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def store_chunks(chunks: list[dict], *, conn: sqlite3.Connection | None = None,
                 replace_file: bool = False) -> dict:
    """Persist chunks atomically, reusing existing vectors for identical IDs."""
    own = conn is None
    conn = conn or get_conn()
    if not chunks:
        if own:
            conn.close()
        raise ValueError('No indexable text (at least five words) found; original index preserved')
    stable_path = chunks[0]['filepath']  # portable across checkouts
    path = Path(stable_path)
    if not path.is_absolute():
        path = ROOT / path
    digest = _fingerprint(path)
    old = conn.execute('SELECT sha256 FROM documents WHERE filepath=?', (stable_path,)).fetchone()
    if old and old['sha256'] == digest:
        pending = conn.execute("""SELECT COUNT(*) FROM chunks WHERE filepath=? AND (vector IS NULL OR embedding_model IS NULL OR embedding_model != ? OR length(vector) != ?)""",
            (stable_path, EMBED_MODEL, EMBED_DIMS * 4)).fetchone()[0]
        if own: conn.close()
        return {'chunks': len(chunks), 'pending': pending, 'skipped': True}
    if replace_file:
        # Remove ONLY obsolete IDs. Identical chunk IDs keep their Gemini
        # vectors even if the file's other sections were edited.
        new_ids = {item['id'] for item in chunks}
        existing_ids = [r[0] for r in conn.execute(
            'SELECT id FROM chunks WHERE filepath=?', (stable_path,))]
        for old_id in existing_ids:
            if old_id not in new_ids:
                conn.execute('DELETE FROM chunks WHERE id=?', (old_id,))
    for item in chunks:
        conn.execute('''INSERT OR IGNORE INTO chunks
            (id,source,location,url,filepath,text,n_words)
            VALUES (:id,:source,:location,:url,:filepath,:text,:n_words)''', item)
    conn.execute('''INSERT INTO documents(filepath,sha256,source,url,n_chunks)
           VALUES(?,?,?,?,?) ON CONFLICT(filepath) DO UPDATE SET
           sha256=excluded.sha256,source=excluded.source,url=excluded.url,n_chunks=excluded.n_chunks''',
           (stable_path, digest, chunks[0]['source'], chunks[0]['url'], len(chunks)))
    conn.commit()
    pending = conn.execute("""SELECT COUNT(*) FROM chunks
        WHERE filepath=? AND (vector IS NULL OR embedding_model IS NULL
        OR embedding_model != ? OR length(vector) != ?)""",
        (stable_path, EMBED_MODEL, EMBED_DIMS * 4)).fetchone()[0]
    if own: conn.close()
    return {'chunks': len(chunks), 'pending': pending, 'skipped': False}


def _embed_text(client, text: str, *, query: bool) -> list[float]:
    """Gemini Embedding 2 asymmetric text convention, documented by Google."""
    from google.genai import types
    if query:
        contents = f'task: search result | query: {text}'
    else:
        contents = text
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=contents,
        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIMS),
    )
    if not result.embeddings or not result.embeddings[0].values:
        raise RuntimeError('Gemini returned an empty embedding')
    return result.embeddings[0].values


def _embed_document_batch(client, documents: list[str]) -> list[list[float]]:
    """Gemini 2 must receive a *Content per text*; strings alone form one multimodal input.

    Official Google cookbook demonstrates Content(parts=[Part.from_text(...)])
    for separate vectors. Do not send a raw list of strings for Gemini 2.
    """
    from google.genai import types
    contents = [types.Content(parts=[types.Part.from_text(text=doc)]) for doc in documents]
    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=contents,
        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIMS),
    )
    if not response.embeddings or len(response.embeddings) != len(documents):
        raise RuntimeError(f'Gemini returned {len(response.embeddings or [])} embeddings for '
                           f'{len(documents)} documents; batch was NOT persisted')
    embeddings = [emb.values for emb in response.embeddings]
    if any(not values or len(values) != EMBED_DIMS for values in embeddings):
        raise RuntimeError('Gemini embedding dimension mismatch; no vectors saved')
    return embeddings


def embed_and_store(chunks: list[dict] | None = None, *, conn: sqlite3.Connection | None = None,
                    max_new: int | None = None, batch_size: int = 12,
                    pause_seconds: float = 4.0) -> dict:
    """Batch Gemini Embedding 2; commit every returned vector immediately.

    A 429/503 error retries with bounded exponential backoff. Already persisted
    IDs are never sent again on rerun. Each text still counts toward quota.
    """
    from api_key import load_api_key
    from google import genai
    import numpy as np
    key = load_api_key()
    own = conn is None
    conn = conn or get_conn()
    allowed_ids = {row['id'] for row in chunks} if chunks is not None else None
    all_pending = conn.execute("""SELECT id,source,location,text FROM chunks
        WHERE vector IS NULL OR embedding_model IS NULL
           OR embedding_model != ? OR length(vector) != ?
        ORDER BY source,location,id""",
        (EMBED_MODEL, EMBED_DIMS * 4)).fetchall()
    pending = [row for row in all_pending if allowed_ids is None or row['id'] in allowed_ids]
    if max_new is not None:
        pending = pending[:max_new]
    client = genai.Client(api_key=key)
    finished = 0
    try:
        for start in range(0, len(pending), batch_size):
            batch = pending[start:start+batch_size]
            texts = [f"title: {row['source']} / {row['location']} | text: {row['text']}" for row in batch]
            for attempt in range(7):
                try:
                    vectors = _embed_document_batch(client, texts)
                    break
                except Exception as e:
                    error = str(e).lower()
                    transient = any(term in error for term in ('429','resource_exhausted','rate limit','quota exceeded',
                                                                  '503','unavailable','502','504','deadline exceeded'))
                    if not transient or attempt == 6:
                        raise
                    delay = min(60, 5 * (2 ** attempt))
                    print(f'Gemini temporarily throttled batch: {type(e).__name__}; retrying after {delay}s',
                          file=sys.stderr, flush=True)
                    time.sleep(delay)
            for row, values in zip(batch, vectors):
                vec = np.asarray(values, dtype='<f4')
                conn.execute('UPDATE chunks SET vector=?, embedding_model=? WHERE id=?',
                             (vec.tobytes(), EMBED_MODEL, row['id']))
                conn.commit()  # Crash loses no previously returned vector.
                finished += 1
            print(f'Embedded and saved {finished}/{len(pending)} new chunks', flush=True)
            if pause_seconds and start + batch_size < len(pending):
                time.sleep(pause_seconds)
    finally:
        if own: conn.close()
    return {'embedded': finished, 'pending_before': len(pending), 'model': EMBED_MODEL,
            'batch_size':batch_size}


def build_index(*, require_gemini: bool = False, max_new: int | None = None) -> dict:
    """Ingest bundled PSF-licensed documents and resume embedding from saved vectors."""
    from api_key import load_api_key
    manifest = manifest_map()
    if len(manifest) < 3:
        raise RuntimeError('At least 3 bundled documents are required')
    conn = get_conn()
    document_results = []
    for name in sorted(manifest):
        chunks = chunk_file(SOURCES_DIR / name)
        document_results.append({'source': manifest[name]['source'], **store_chunks(chunks, conn=conn, replace_file=True)})
    count = conn.execute('SELECT COUNT(*) FROM chunks').fetchone()[0]
    saved = available_vectors(conn)[1]
    conn.close()
    result = {'documents': len(document_results), 'source_words': sum(row['words'] for row in manifest.values()),
              'chunks': count, 'saved_gemini_vectors': saved, 'files': document_results}
    if load_api_key(required=False):
        result['embedding'] = embed_and_store(max_new=max_new)
    elif require_gemini and saved < count:
        raise RuntimeError('Chunks were saved, but missing Gemini embeddings require GEMINI_API_KEY. See SETUP.md.')
    elif saved < count:
        result['warning'] = f'No Gemini key: {count - saved} vectors are pending. Re-run index with a key.'
    conn = get_conn()
    result['saved_gemini_vectors'] = available_vectors(conn)[1]
    conn.close()
    return result


def add_document_pipeline(path: str | Path) -> dict:
    """Idempotent ingestion of a user-approved local file; uses same pipeline as index.ipynb."""
    path = Path(path).expanduser().resolve(strict=True)
    allowed = (ROOT / 'incoming').resolve()
    if not path.is_file() or not path.is_relative_to(allowed):
        raise ValueError(f'Only regular files inside {allowed} may be indexed')
    if path.suffix.lower() not in ACCEPTED_TYPES:
        raise ValueError(f'File format not supported: {path.suffix}')
    if path.stat().st_size > 5 * 1024 * 1024:
        raise ValueError('Document larger than the 5 MB safety limit')
    chunks = chunk_file(path)
    if not chunks:
        raise ValueError('Document contains no indexable text; existing indexed version preserved')
    conn = get_conn()
    result = store_chunks(chunks, conn=conn, replace_file=True)
    conn.close()
    if result['pending']:
        result['embedding'] = embed_and_store(chunks=chunks)
    return {'file': path.name, **result}


def _tokens(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def _bm25(query: str, rows: list[sqlite3.Row]) -> list[float]:
    """Actual Okapi BM25 over persisted chunk text (not a placeholder overlap score)."""
    docs = [_tokens(row['text']) for row in rows]
    n = len(docs)
    if not n:
        return []
    avgdl = sum(map(len, docs)) / n
    freqs = [Counter(d) for d in docs]
    document_freq = Counter(t for freq in freqs for t in freq)
    qterms = set(_tokens(query))
    k1, b = 1.5, 0.75
    scores = []
    for doc, freq in zip(docs, freqs):
        score = sum(math.log1p((n-document_freq[t]+0.5)/(document_freq[t]+0.5)) *
                    freq[t] * (k1+1)/(freq[t] + k1*(1-b+b*len(doc)/max(avgdl, 1)))
                    for t in qterms if freq[t])
        scores.append(score)
    return scores


@lru_cache(maxsize=256)
def _query_embedding(query: str) -> tuple[float, ...]:
    from api_key import load_api_key
    from google import genai
    client = genai.Client(api_key=load_api_key())
    return tuple(_embed_text(client, query, query=True))


def available_vectors(conn: sqlite3.Connection | None = None) -> tuple[int, int]:
    own = conn is None
    conn = conn or get_conn()
    n, v = conn.execute("""SELECT COUNT(*), COALESCE(SUM(CASE WHEN vector IS NOT NULL AND embedding_model=? AND length(vector)=? THEN 1 ELSE 0 END), 0) FROM chunks""", (EMBED_MODEL, EMBED_DIMS * 4)).fetchone()
    if own: conn.close()
    return int(n), int(v)


def retrieve(query: str, k: int = 5, design: str = 'hybrid', *,
             conn: sqlite3.Connection | None = None) -> list[dict]:
    """Compare lexical, structure-aware BM25 or Gemini+BM25 RRF retrieval.

    Hybrid refuses to *pretend* vectors exist: if missing, it uses section BM25
    and reports 'section_bm25_fallback' in each result's `design` field.
    """
    import numpy as np
    if not query.strip():
        raise ValueError('Query may not be blank')
    if design not in {'bm25', 'section_bm25', 'hybrid', 'dense'}:
        raise ValueError('Unknown retrieval design')
    own = conn is None
    conn = conn or get_conn()
    rows = conn.execute('SELECT * FROM chunks').fetchall()
    if not rows:
        if own: conn.close()
        return []
    base = _bm25(query, rows)
    qterms = set(_tokens(query))
    topic_scores = []
    for row, sc in zip(rows, base):
        loc_tokens = set(_tokens(row['location'].replace('topic:', '').replace('-', ' ').replace('_', ' ')))
        source_tokens = set(_tokens(row['source'].replace('_', ' ')))
        topic_scores.append(sc + 4.0 * len(qterms & loc_tokens) + 0.55 * len(qterms & source_tokens))
    applied = design
    from api_key import load_api_key
    vectors_ok = all(row['vector'] is not None and row['embedding_model'] == EMBED_MODEL and len(row['vector']) == EMBED_DIMS * 4 for row in rows)
    can_query_embed = bool(load_api_key(required=False))
    if design in ('hybrid','dense') and vectors_ok and can_query_embed:
        vec = np.asarray(_query_embedding(query), dtype=np.float32)
        vnorm = max(float(np.linalg.norm(vec)), 1e-12)
        arr = np.stack([np.frombuffer(row['vector'], dtype='<f4') for row in rows])
        cos = (arr @ vec) / (np.maximum(np.linalg.norm(arr, axis=1), 1e-12) * vnorm)
        if design == 'dense':
            scores = cos.tolist()
        else:
            # Reciprocal rank fusion robust to different similarity score scales.
            lexical_order = sorted(range(len(rows)), key=lambda i: topic_scores[i], reverse=True)
            vector_order = np.argsort(-cos).tolist()
            rank_lex = {i: rank for rank, i in enumerate(lexical_order, 1)}
            rank_dense = {i: rank for rank, i in enumerate(vector_order, 1)}
            scores = [1/(60+rank_lex[i]) + 1/(60+rank_dense[i]) for i in range(len(rows))]
    elif design in ('hybrid','dense'):
        applied = 'section_bm25_fallback'
        scores = topic_scores
    else:
        scores = base if design == 'bm25' else topic_scores
    ranked = sorted(range(len(rows)), key=lambda i: (-float(scores[i]), rows[i]['id']))
    # Diversify across distinct source sections before repeating a section.
    # Critical for multi-passage questions: five near-duplicate chunks from one
    # section can hide the complementary second source completely.
    unique, repeated, seen = [], [], set()
    for i in ranked:
        key = (rows[i]['source'], rows[i]['location'])
        if key not in seen:
            unique.append(i); seen.add(key)
        else:
            repeated.append(i)
    # Truly unmodified BM25 baseline; diversity is part of structured/hybrid designs.
    winners = (ranked if design == 'bm25' else unique + repeated)[:max(0, k)]
    result = [{**{col: row[col] for col in ('id','source','location','url','text','n_words')},
               'score': round(float(scores[i]), 6), 'design': applied}
              for i in winners for row in [rows[i]]]
    if own: conn.close()
    return result


def selected_design() -> str:
    choice = ROOT / 'eval' / 'selected_retrieval.json'
    if choice.exists():
        try:
            design = json.loads(choice.read_text(encoding='utf-8'))['design']
            if design in {'bm25', 'section_bm25', 'hybrid'}:
                return design
        except (ValueError, KeyError):
            pass
    return 'hybrid'


def search_citations(query: str, k: int = 5) -> str:
    matches = retrieve(query, k=k, design=selected_design())
    if not matches:
        return 'The local corpus index is empty. No evidence available.'
    blocks = []
    for hit in matches:
        blocks.append(f"[CITE:{hit['id']}] Source: {hit['source']} | Location: {hit['location']} | URL: {hit['url']}\n" +
                      f"Retrieval: {hit['design']} ({hit['score']:.4f})\nExcerpt:\n{hit['text']}")
    return '\n\n---\n\n'.join(blocks)


def index_summary() -> dict:
    conn = get_conn()
    count, vec = available_vectors(conn)
    documents = [dict(x) for x in conn.execute('SELECT source,n_chunks FROM documents ORDER BY source')]
    conn.close()
    return {'chunks': count, 'gemini_vectors': vec, 'documents': documents}
