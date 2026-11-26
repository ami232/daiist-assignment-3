"""
Configuración compartida del Assignment 3 (la leen index.py, retrieval.py,
server.py, agent.py y evaluate.py).

Todo lo que es una DECISIÓN TUYA está aquí, en un único sitio:
  - qué diseño de chunking y de búsqueda usa el servidor (CHOSEN_*), que
    eliges con los números de `main.py evaluate`;
  - cuántos fragmentos devuelve la búsqueda (TOP_K);
  - la frase de rechazo, que tiene que coincidir con la que pongas en AGENTS.md.
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# --- Carpetas -----------------------------------------------------------------
CORPUS_DIR = ROOT / "corpus"   # PDFs y JSON descargados (git-ignored: llevan datos personales)
# El índice se puede redirigir con una variable de entorno: demo_add_document.py
# trabaja sobre una COPIA del índice para no tocar el que entregas.
INDEX_DIR = Path(os.environ.get("RAG_INDEX_DIR", ROOT / "index"))
CHROMA_DIR = INDEX_DIR / "chroma"            # base de datos vectorial (ChromaDB)
QUERY_CACHE = INDEX_DIR / "query_cache.json"  # embeddings de preguntas ya vistas
EVAL_DIR = ROOT / "eval"

# --- Modelos de Gemini ----------------------------------------------------------
# Embeddings: gemini-embedding-2 (cuota gratuita ~1.000 textos/día, ver SETUP.md).
EMBED_MODEL = os.environ.get("GEMINI_EMBED_MODEL", "gemini-embedding-2")
EMBED_DIM = 768        # 768 en vez de 3072: índice 4 veces más pequeño, misma calidad práctica
EMBED_BATCH = 20       # textos por petición (cada texto cuenta para la cuota diaria)
# Modelo del agente y del juez. Comprueba tus límites en https://ai.dev/rate-limit
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite")
# >>> DECISIÓN TUYA: el juez. <<< Empezaste con gemini-3.6-flash, pero su cuota gratuita
# (20 peticiones al día) no llegaba para las 31 respuestas. gemini-3.1-flash-lite tiene 500
# al día y NO es el modelo del agente (un modelo no debe corregirse a sí mismo).
# Sus notas antiguas siguen en judge.jsonl; comparar_jueces.py compara los dos jueces.
JUDGE_MODEL = os.environ.get("GEMINI_JUDGE_MODEL", "gemini-3.1-flash-lite")
EARLIER_JUDGE_MODEL = "gemini-3.6-flash"

# --- Diseños de chunking ----------------------------------------------------------
# Cada diseño de chunking cuesta un índice completo de embeddings. Ambos tienen un
# tamaño parecido (~300 palabras) para que la comparación mida la ESTRUCTURA y no
# el tamaño.
CHUNK_DESIGNS = {
    # Ventanas de tamaño fijo que ignoran la estructura del pliego.
    "fixed300": {"kind": "fixed", "words": 300, "overlap": 30},
    # Un fragmento por cláusula/apartado del pliego; los largos se parten y los
    # muy cortos se unen al siguiente.
    "struct": {"kind": "struct", "max_words": 350, "min_words": 60},
}

# Métodos de búsqueda que compara evaluate.py (no gastan embeddings extra):
#   dense  = similitud de embeddings
#   bm25   = palabras clave (BM25)
#   hybrid = fusión de ambos rankings (Reciprocal Rank Fusion)
SEARCH_METHODS = ["dense", "bm25", "hybrid"]

# >>> TU DECISIÓN: rellénala con los números de eval/retrieval.md <<<
CHOSEN_DESIGN = os.environ.get("RAG_DESIGN", "struct")
CHOSEN_METHOD = os.environ.get("RAG_METHOD", "dense")
CHOSEN_TENDER_FILTER = True   # filtrar por licitación cuando la pregunta nombra una
TOP_K = 5

# --- Contrato con AGENTS.md -------------------------------------------------------
# El agente debe citar así: [doc_id, p. N]   ej. [cartagena_pcap, p. 14]
# y, si el corpus no cubre la pregunta, empezar la respuesta con REFUSAL_PHRASE.
# Si cambias la frase aquí, cámbiala también en AGENTS.md.
REFUSAL_PHRASE = "El corpus no cubre esta pregunta"

# Límites del agente (guardarraíles de coste)
MAX_TOOL_CALLS = 6     # búsquedas por pregunta
MAX_MODEL_CALLS = 10   # llamadas al modelo por pregunta
