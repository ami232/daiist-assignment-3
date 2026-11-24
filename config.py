"""
Every setting the pipeline depends on, in one place.

index.py, server.py, agent.py and evaluate.py all read from here, so a model name,
a chunk size or the chosen retrieval design can never disagree between stages.
Each choice is argued for in REPORT.md.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"          # downloaded originals (committed: their licences allow it)
INDEX_DIR = ROOT / "index"            # ChromaDB + chunk files + cached query vectors (committed)
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_vectors.json"
EVAL_DIR = ROOT / "eval"

# --- Models (free tier, Default Gemini Project) -------------------------------
EMBED_MODEL = "gemini-embedding-2"     # 100 requests/min, 30K tokens/min, 1,000 texts/day
AGENT_MODEL = "gemini-3.5-flash-lite"  # 15 requests/min, 500/day
JUDGE_MODEL = "gemini-3.1-flash-lite"  # a different model, so the agent is not graded by itself
# If Google answers 503 "high demand" for the judge, evaluate.py moves to the next model.
# Each verdict records the model that gave it (eval/judge.jsonl, column judge_model in results.csv).
JUDGE_FALLBACKS = ["gemini-3.1-flash-lite-preview", "gemini-3.5-flash-lite"]

# Free-tier pacing (kept a little under the published limits).
EMBED_TOKENS_PER_MIN = 25_000
EMBED_REQUESTS_PER_MIN = 80
CHAT_REQUESTS_PER_MIN = 12

# --- Chunking designs compared in evaluate.py --------------------------------
# "fixed":     sliding windows of FIXED_WORDS words, FIXED_OVERLAP words shared with the
#              previous window, ignoring the legal structure.
# "structure": one chunk per article / annex / pliego section; sections longer than
#              STRUCT_MAX_WORDS are split at paragraph boundaries. Each chunk starts with
#              a header naming its document and location.
FIXED_WORDS = 220
FIXED_OVERLAP = 40
STRUCT_MAX_WORDS = 380
DESIGNS = ["fixed", "structure"]

# Retrieval settings used by server.py (set from the numbers in eval/retrieval_summary.csv).
CHOSEN_DESIGN = "structure"
CHOSEN_METHOD = "vector"   # "vector" or "hybrid" (vector + BM25 keyword search, fused by rank)
TOP_K = 5

# --- Agent guardrails ----------------------------------------------------------
MAX_TOOL_CALLS = 4          # searches per question before the agent must answer
MAX_MODEL_CALLS = 8         # model calls per question
REFUSAL = "El corpus no cubre esta pregunta."   # exact sentence AGENTS.md asks for

# --- The corpus -----------------------------------------------------------------
DOCUMENTS = [
    {
        "id": "reg_ue_2019_33",
        "title": "Reglamento Delegado (UE) 2019/33 (consolidado 18-01-2025)",
        "kind": "eu",
        "date": "2025-01-18 (consolidated version)",
        "urls": [
            "https://eur-lex.europa.eu/eli/reg_del/2019/33/2025-01-18/spa/pdf",
            "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:02019R0033-20250118",
        ],
        "licence": "CC BY 4.0 (Commission Decision 2011/833/EU). © European Union, https://eur-lex.europa.eu",
    },
    {
        "id": "pliego_doca_rioja",
        "title": "Pliego de condiciones de la DOCa Rioja",
        "kind": "pliego",
        "date": "2023-06-07 (amendment AM10)",
        "urls": [
            "https://www.mapa.gob.es/es/alimentacion/temas/calidad-diferenciada/pliegodecondicionesdocariojamodificado_tcm30-680343.pdf",
            "https://riojawine.com/wp-content/uploads/2023/07/pliego-de-condiciones-de-la-doca-rioja-en-vigor.pdf",
        ],
        "licence": "Official act, not subject to copyright (Ley de Propiedad Intelectual art. 13); MAPA allows reuse citing the source",
    },
    {
        "id": "ley_24_2003_vina_vino",
        "title": "Ley 24/2003 de la Viña y del Vino (consolidada)",
        "kind": "boe",
        "date": "2025-04-02 (last consolidation)",
        "urls": ["https://www.boe.es/buscar/pdf/2003/BOE-A-2003-13864-consolidado.pdf"],
        "licence": "Fuente de los datos: Agencia Estatal Boletín Oficial del Estado (BOE reuse conditions); LPI art. 13",
    },
    {
        "id": "ley_6_2015_dop_igp",
        "title": "Ley 6/2015 de Denominaciones de Origen e IGP supraautonómicas (consolidada)",
        "kind": "boe",
        "date": "2022-12-24 (last consolidation)",
        "urls": ["https://www.boe.es/buscar/pdf/2015/BOE-A-2015-5288-consolidado.pdf"],
        "licence": "Fuente de los datos: Agencia Estatal Boletín Oficial del Estado (BOE reuse conditions); LPI art. 13",
    },
    {
        "id": "rd_1363_2011_etiquetado",
        "title": "Real Decreto 1363/2011 de etiquetado de productos vitivinícolas (consolidado)",
        "kind": "boe",
        "date": "2026-03-13 (last consolidation)",
        "urls": ["https://www.boe.es/buscar/pdf/2011/BOE-A-2011-17174-consolidado.pdf"],
        "licence": "Fuente de los datos: Agencia Estatal Boletín Oficial del Estado (BOE reuse conditions); LPI art. 13",
    },
]

# The document added later through the add_document tool (not part of the base index).
EXTRA_DOCUMENTS = [
    {
        "id": "pliego_do_ribera_del_duero",
        "title": "Pliego de condiciones de la DO Ribera del Duero",
        "kind": "pliego",
        "urls": [
            "https://www.mapa.gob.es/es/alimentacion/temas/calidad-diferenciada/ribera_del_duero_2023_07_31_tcm30-210154.pdf",
            "https://www.riberadelduero.es/sites/default/files/2020-12/PLIEGO%20DE%20CONDICIONES%20DOP%20RIBERA%20DEL%20DUERO_DOUE%2006-03-20.pdf",
        ],
        "licence": "Official act, not subject to copyright (Ley de Propiedad Intelectual art. 13); MAPA allows reuse citing the source",
    },
]
