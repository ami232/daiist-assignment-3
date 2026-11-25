"""
Shared settings for every stage (index, server, agent, evaluate).

Everything that two files must agree on lives here, so the index and the
search tool can never drift apart (same model, same dimensions, same paths).
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Where the committed index lives. The add-document demo points this at a
# temporary copy so the committed index (and the evaluation) stay unchanged.
INDEX_DIR = Path(os.environ.get("RAG_INDEX_DIR", ROOT / "index")).resolve()
CORPUS_DIR = ROOT / "corpus"
EVAL_DIR = ROOT / "eval"

# --- Embeddings -------------------------------------------------------------
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIMS = 768          # recommended size; Gemini normalises truncated vectors
EMBED_BATCH = 50          # texts per request (each text counts against the daily quota)

# gemini-embedding-2 takes the task as a text prefix instead of a task_type.
QUERY_PREFIX = "task: question answering | query: "


def document_prefix(title: str) -> str:
    return f"title: {title} | text: "


# --- Chat models (agent and judge) -------------------------------------------
# "-latest" aliases keep working when Google retires a model version.
# Override with an environment variable if your free tier lists another one.
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-flash-lite-latest")
JUDGE_MODEL = os.environ.get("GEMINI_JUDGE_MODEL", "gemini-flash-lite-latest")

# --- Retrieval defaults -------------------------------------------------------
DESIGNS = ["fixed", "structure"]      # the two chunkings compared in evaluate.py
METHODS = ["dense", "bm25", "hybrid"]  # search methods (no re-embedding needed)
DEFAULT_RETRIEVAL = {"design": "structure", "method": "hybrid", "k": 5}
RETRIEVAL_CONFIG = INDEX_DIR / "config.json"

REFUSAL = "The corpus does not cover this"


def retrieval_config() -> dict:
    """The design and method the server uses. evaluate.py writes the winner here."""
    config = dict(DEFAULT_RETRIEVAL)
    if RETRIEVAL_CONFIG.is_file():
        config.update(json.loads(RETRIEVAL_CONFIG.read_text(encoding="utf-8")))
    return config
