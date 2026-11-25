"""
Shared settings for every script (index.py, retrieve.py, server.py, agent.py, evaluate.py).

Keeping them in ONE place means that if you change a model name or a chunk
size, every script sees the same value.
"""

import os
from pathlib import Path

# --- Folders --------------------------------------------------------------
ROOT = Path(__file__).resolve().parent   # the repo folder
CORPUS_DIR = ROOT / "corpus"             # downloaded drug labels (git-ignored)
EXTRA_DIR = CORPUS_DIR / "extra"         # labels downloaded but NOT indexed (for the add-document demo)
INDEX_DIR = ROOT / "index"               # ChromaDB lives here (committed to git)
EVAL_DIR = ROOT / "eval"                 # test set + evaluation results

# --- The corpus -----------------------------------------------------------
# Each entry: short name used in citations -> openFDA search that finds its label.
# These are the official FDA "prescribing information" labels of anticoagulants
# (blood thinners). openFDA publishes them as JSON, already split into sections.
DRUGS = {
    "ELIQUIS": 'openfda.brand_name:"ELIQUIS"',        # apixaban
    "XARELTO": 'openfda.brand_name:"XARELTO"',        # rivaroxaban
    "PRADAXA": 'openfda.brand_name:"PRADAXA"',        # dabigatran
    "WARFARIN": 'openfda.generic_name:"WARFARIN SODIUM"',  # warfarin (generic label)
    "LOVENOX": 'openfda.brand_name:"LOVENOX"',        # enoxaparin
}

# Downloaded into corpus/extra/ but NOT indexed by main.py index.
# You add it later with the add_document tool, to answer an "unanswerable" question.
EXTRA_DRUGS = {
    "SAVAYSA": 'openfda.brand_name:"SAVAYSA"',        # edoxaban
}

# Which label sections we keep. These are the top-level sections a nurse or
# doctor actually looks things up in. We skip sub-keys (e.g. "pregnancy") because
# openFDA repeats them inside "use_in_specific_populations" -> duplicates.
SECTIONS = [
    "boxed_warning",
    "indications_and_usage",
    "dosage_and_administration",
    "dosage_forms_and_strengths",
    "contraindications",
    "warnings_and_cautions",
    "warnings",                      # older labels use this instead of warnings_and_cautions
    "adverse_reactions",
    "drug_interactions",
    "use_in_specific_populations",
    "overdosage",
    "clinical_pharmacology",
    "how_supplied",
    "patient_counseling_information",
    "clinical_studies",              # trial results; added because the 5 labels were 49,236 words without it
]

# --- Models -----------------------------------------------------------------
EMBED_MODEL = "gemini-embedding-2"   # the model named in SETUP.md
# Chat model for the agent and the judge. If Google renames/retires it, change it
# here (see the model list at https://ai.dev/rate-limit) or set GEMINI_CHAT_MODEL in .env.
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite")  # same model as in class

# --- Retrieval designs we compare --------------------------------------------
FIXED_WORDS = 200      # design "fixed": every chunk is a 200-word window
FIXED_OVERLAP = 40     # ...and consecutive windows share 40 words
SECTION_MAX_WORDS = 300  # design "sections": one chunk per label subsection, split if longer than this

# The three designs. "sections_hybrid" re-uses the "sections" vectors (no new embeddings).
DESIGNS = ["fixed", "sections", "sections_hybrid"]

# The design the server and agent use. Set this AFTER `main.py evaluate`,
# to whichever design wins on hit rate (that's the "choose by the numbers" step).
CHOSEN_DESIGN = "sections_hybrid"

TOP_K = 5   # how many chunks the search tool returns
