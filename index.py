"""
Assignment 3: build the index (`main.py index`).

Downloads three 10-K filings (Ralph Lauren, PVH, Tapestry) into corpus/,
keeps Item 1 (Business), Item 1A (Risk Factors) and Item 7 (MD&A), chunks them
with metadata, embeds with Gemini and stores vectors in index/ (ChromaDB).
Only chunks without a saved vector are embedded.

server.py imports chunk_file() and embed_and_store().
"""

import os
import re
import sys
import time
from pathlib import Path
import hashlib
import json

import chromadb
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
HEADERS = {"User-Agent": "Beatriz Cruces TU_EMAIL@ejemplo.com"}  # la SEC lo exige: pon tu email

EMBEDDING_MODEL = "gemini-embedding-2"
CHUNK_WORDS = int(os.environ.get("CHUNK_WORDS", 250))  # diseño A=250; prueba B con 120
OVERLAP_WORDS = CHUNK_WORDS // 5
COLLECTION = f"tenk_w{CHUNK_WORDS}"  # una colección por diseño de chunking

CORPUS = {
    "RL": {
        "company": "Ralph Lauren",
        "fiscal_year_end": "2026-03-28",
        "url": "https://www.sec.gov/Archives/edgar/data/1037038/000162828026037074/rl-20260328.htm",
    },
    "PVH": {
        "company": "PVH",
        "fiscal_year_end": "2026-02-01",
        "url": "https://www.sec.gov/Archives/edgar/data/78239/000007823926000021/pvh-20260201.htm",
    },
    "TPR": {
        "company": "Tapestry",
        "fiscal_year_end": "2026-06-27",
        "url": "https://www.sec.gov/Archives/edgar/data/1116132/000111613226000018/tpr-20260627.htm",
    },
}

# (nombre de sección, patrón del encabezado). Los terminadores delimitan el final.
SECTIONS = [
    ("Item 1. Business", r"item\s*1\s*\.\s*business"),
    ("Item 1B (end)", r"item\s*1b\s*\."),
    ("Item 1A. Risk Factors", r"item\s*1a\s*\.\s*risk\s*factors"),
    ("Item 7. MD&A", r"item\s*7\s*\.\s*management.{0,3}s\s+discussion"),
    ("Item 7A (end)", r"item\s*7a\s*\."),
]
KEEP = {"Item 1. Business", "Item 1A. Risk Factors", "Item 7. MD&A"}
END_OF = {
    "Item 1. Business": r"item\s*1a\s*\.\s*risk\s*factors",
    "Item 1A. Risk Factors": r"item\s*1b\s*\.|item\s*2\s*\.\s*properties",
    "Item 7. MD&A": r"item\s*7a\s*\.|item\s*8\s*\.\s*financial",
}
START_OF = {name: pat for name, pat in SECTIONS if name in KEEP}


# ---------- download and extraction ----------

def download(ticker):
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{ticker}.htm"
    if not path.exists():  # si ya lo bajaste a mano, se usa tal cual
        response = requests.get(CORPUS[ticker]["url"], headers=HEADERS, timeout=60)
        response.raise_for_status()
        path.write_bytes(response.content)
        time.sleep(0.2)  # la SEC pide no pasar de 10 peticiones/s
    return path


def html_to_text(path):
    soup = BeautifulSoup(path.read_bytes(), "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    for tag in soup.find_all(style=re.compile(r"display:\s*none")):  # cabecera XBRL oculta
        tag.decompose()
    for cell in soup.find_all(["td", "th"]):  # tablas: celdas separadas por " | "
        cell.append(" | ")
    return " ".join(soup.get_text(" ").split())


def extract_sections(text):
    """Devuelve {sección: texto}. El índice del 10-K repite los encabezados, así que de
    todas las coincidencias se elige la que tiene más texto hasta el siguiente final."""
    found = {}
    for name, start_pat in START_OF.items():
        best = ""
        for m in re.finditer(start_pat, text, flags=re.I):
            end = re.search(END_OF[name], text[m.end():], flags=re.I)
            body = text[m.end(): m.end() + end.start()] if end else ""
            if len(body) > len(best):
                best = body
        if len(best.split()) > 500:  # menos que eso: era el índice o una referencia cruzada
            found[name] = best
    return found


# ---------- chunking ----------

def chunk_words(words, size, overlap):
    for start in range(0, max(len(words) - overlap, 1), size - overlap):
        yield " ".join(words[start:start + size])


def chunk_file(path, ticker=None, size=None, overlap=None):
    """Extrae, limpia y trocea un archivo. Cada chunk lleva fuente y localización.
    Para un 10-K conocido usa sus secciones; para cualquier otro archivo, el texto entero."""
    size = size or CHUNK_WORDS
    overlap = overlap if overlap is not None else size // 5
    path = Path(path)
    text = html_to_text(path) if path.suffix in {".htm", ".html"} else path.read_text(errors="ignore")
    ticker = ticker or path.stem
    meta = CORPUS.get(ticker, {"company": ticker, "fiscal_year_end": "unknown"})
    sections = extract_sections(text) if ticker in CORPUS else {}
    sections = sections or {"Document": text}
    chunks = []
    for section, body in sections.items():
        for i, chunk_text in enumerate(chunk_words(body.split(), size, overlap)):
            chunks.append({
                "id": f"{ticker}|{section}|w{size}|{i}",
                "text": chunk_text,
                "metadata": {
                    "ticker": ticker,
                    "company": meta["company"],
                    "fiscal_year_end": meta["fiscal_year_end"],
                    "section": section,
                    "chunk_number": i,
                    "source": path.name,
                },
            })
    return chunks


# ---------- embeddings and storage ----------

def get_client():
    return genai.Client(
        api_key=load_api_key(),
        http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(
            attempts=5, initial_delay=60, max_delay=60, exp_base=1, jitter=0,
            http_status_codes=[429, 500, 502, 503, 504])),
    )


def embed_texts(client, texts):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
    )
    return [e.values for e in result.embeddings]


def doc_text(chunk):
    m = chunk["metadata"]
    return f"title: {m['company']} - {m['section']} | text: {chunk['text']}"


def query_text(question):
    return f"task: search result | query: {question}"


def get_collection():
    db = chromadb.PersistentClient(path=str(INDEX_DIR))
    return db.get_or_create_collection(
        name=COLLECTION, configuration={"hnsw": {"space": "cosine"}}, embedding_function=None)


def embed_and_store(chunks, collection=None, batch_size=20):
    """Embebe solo los chunks sin vector guardado y los guarda tras cada lote."""
    collection = collection or get_collection()
    existing = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    print(f"{len(chunks)} chunks, {len(existing)} ya indexados, {len(todo)} por embeber")
    if not todo:
        return 0
    client = get_client()
    for start in range(0, len(todo), batch_size):
        batch = todo[start:start + batch_size]
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=embed_texts(client, [doc_text(c) for c in batch]),
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )  # guardado ya: si se cae o se acaba la cuota, no se pierde nada
        print(f"  guardados {min(start + batch_size, len(todo))}/{len(todo)}")
    return len(todo)
# ---------- registro de documentos (nombre -> huella) ----------

REGISTRY = INDEX_DIR / "documents.json"


def file_hash(path):
    """Huella (SHA-256) del contenido del archivo: cambia si cambia una sola coma."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_registry():
    return json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}


def register_document(path, n_chunks):
    registry = load_registry()
    registry[Path(path).name] = {"sha256": file_hash(path), "chunks": n_chunks}
    INDEX_DIR.mkdir(exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=2))

def main():
    collection = get_collection()
    for ticker in CORPUS:
        path = download(ticker)
        chunks = chunk_file(path, ticker)
        by_section = {}
        for c in chunks:
            by_section[c["metadata"]["section"]] = by_section.get(c["metadata"]["section"], 0) + 1
        print(f"{ticker}: {by_section}")
        embed_and_store(chunks, collection)
        register_document(path, len(chunks))
    print("index/ holds", collection.count(), "chunks in", COLLECTION)


if __name__ == "__main__":
    main()