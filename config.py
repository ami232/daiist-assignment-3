"""
Shared settings for every stage. Change things here, not in the scripts.

Use case: a student pilot preparing for the FAA private-pilot knowledge test
and for real flights asks questions about weather, airspace and aeromedical
factors. (Write the full use case in REPORT.md.)
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"            # downloaded PDFs (git-ignored)
EXTRA_DIR = CORPUS_DIR / "extra"        # documents kept OUT of the first index, for the add-document demo
INDEX_DIR = ROOT / "index"              # committed
CHROMA_DIR = INDEX_DIR / "chroma"
DOCS_REGISTRY = INDEX_DIR / "documents.json"
QUERY_CACHE = INDEX_DIR / "query_cache.json"
EVAL_DIR = ROOT / "eval"

# ---------------------------------------------------------------------------
# Corpus. All FAA handbooks are U.S. Government works: public domain, no
# personal data. doc_id is what goes in eval/questions.csv `expected_source`;
# the printed page label (e.g. 15-3) is what goes in `expected_location`.
# Check the word total that `main.py index` prints: it must be >= 50,000.
# ---------------------------------------------------------------------------
FAA = "https://www.faa.gov/sites/faa.gov/files"
PHAK = "Pilot's Handbook of Aeronautical Knowledge (FAA-H-8083-25C, 2023)"

CORPUS = [
    {"doc_id": "phak-ch12", "title": f"{PHAK}, Ch. 12 Weather Theory", "url": f"{FAA}/14_phak_ch12.pdf"},
    {"doc_id": "phak-ch13", "title": f"{PHAK}, Ch. 13 Aviation Weather Services", "url": f"{FAA}/15_phak_ch13.pdf"},
    {"doc_id": "phak-ch15", "title": f"{PHAK}, Ch. 15 Airspace", "url": f"{FAA}/17_phak_ch15.pdf"},
    {"doc_id": "phak-ch17", "title": f"{PHAK}, Ch. 17 Aeromedical Factors", "url": f"{FAA}/19_phak_ch17.pdf"},
    {"doc_id": "phak-ch16", "title": f"{PHAK}, Ch. 16 Navigation", "url": f"{FAA}/18_phak_ch16.pdf"},
    {"doc_id": "phak-ch11", "title": f"{PHAK}, Ch. 11 Aircraft Performance", "url": f"{FAA}/13_phak_ch11.pdf"},
]
LICENCE = "Public domain (U.S. Government work, 17 U.S.C. 105)"

# Not indexed by `main.py index`. Downloaded into corpus/extra/ so you can add
# it later with the add_document tool (README step 8: before/after).
EXTRA_DOCS = [
    {"doc_id": "phak-ch14", "title": f"{PHAK}, Ch. 14 Airport Operations", "url": f"{FAA}/16_phak_ch14.pdf"},
]

# ---------------------------------------------------------------------------
# Chunking designs. Each one is its own Chroma collection and costs one full
# set of embeddings. Retrieval methods (vector / hybrid) cost nothing extra.
# ---------------------------------------------------------------------------
CHUNKINGS = {
    # Fixed windows of words that ignore the document's structure.
    "fixed": {"kind": "fixed", "size": 200, "overlap": 40},
    # Split at detected headings; long sections are windowed, tiny ones merged.
    "section": {"kind": "section", "max_words": 300, "overlap": 40, "min_words": 40},
}
METHODS = ["vector", "hybrid"]          # hybrid = vector + BM25, fused with reciprocal rank

# The design server.py and agent.py use. Choose it from eval/retrieval_summary.csv.
ACTIVE_CHUNKING = os.environ.get("RAG_CHUNKING", "section")
ACTIVE_METHOD = os.environ.get("RAG_METHOD", "vector")
SEARCH_K = 5                            # chunks returned by the search tool

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
EMBED_MODEL = os.environ.get("GEMINI_EMBED_MODEL", "gemini-embedding-2")
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-flash-latest")
JUDGE_MODEL = os.environ.get("GEMINI_JUDGE_MODEL", CHAT_MODEL)
EMBED_BATCH = 1

# ---------------------------------------------------------------------------
# Agent contract. AGENTS.md must tell the model to use exactly these, because
# the guardrail and the evaluation check them in code.
#   citation:  [doc_id p.PAGE]   e.g. [phak-ch15 p.15-3]
#   refusal:   the answer starts with REFUSAL_PREFIX
# ---------------------------------------------------------------------------
REFUSAL_PREFIX = "The corpus does not cover this"
MAX_AGENT_STEPS = 12                    # LangGraph recursion limit = call limit
