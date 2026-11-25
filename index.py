"""
Assignment 3: build the index (`main.py index`).

Downloads the corpus (download.py), splits each FDA label into its sections,
cleans them, chunks each section into pieces of at most CHUNK_WORDS words and
embeds them with Gemini into a ChromaDB collection in index/. Every chunk
carries its source (label file), brand and generic name, and location (label
section). Vectors are saved batch by batch and only chunks without a saved
vector are embedded, so a crash or the daily quota loses nothing.

server.py's add-document tool imports chunk_file() and index_file().
"""

import hashlib
import json
import re
import sys
import time
from pathlib import Path

import chromadb
from google import genai
from google.genai import errors, types

from api_key import load_api_key
from download import DAILYMED_URL, NON_TEXT_FIELDS, download_corpus

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
COLLECTION = "labels"

EMBED_MODEL = "gemini-embedding-2"
DIMENSIONS = 768
EMBED_BATCH = 50
CHUNK_WORDS = 150
MIN_SECTION_WORDS = 5  # a parent section left with fewer words after removing its subsections is just a heading

# Sections left out of the index, with the reason.
DROPPED_SECTIONS = {
    "clinical_studies": "trial results; not needed to dispense or counsel",
    "spl_medguide": "patient Medication Guide; repeats the label in plain language",
    "clinical_pharmacology": "mechanism and pharmacokinetics; the actionable advice is in other sections",
    "mechanism_of_action": "part of clinical pharmacology",
    "pharmacodynamics": "part of clinical pharmacology",
    "pharmacokinetics": "part of clinical pharmacology",
    "pharmacogenomics": "part of clinical pharmacology",
    "nonclinical_toxicology": "animal studies",
    "carcinogenesis_and_mutagenesis_and_impairment_of_fertility": "part of nonclinical toxicology",
    "animal_pharmacology_and_or_toxicology": "animal studies",
}

# Location names shown to the user and used in eval/questions.csv. Fields not
# listed fall back to their name in title case.
SECTION_TITLES = {
    "boxed_warning": "Boxed Warning",
    "indications_and_usage": "Indications and Usage",
    "dosage_and_administration": "Dosage and Administration",
    "dosage_forms_and_strengths": "Dosage Forms and Strengths",
    "contraindications": "Contraindications",
    "warnings_and_cautions": "Warnings and Precautions",
    "warnings": "Warnings",
    "precautions": "Precautions",
    "adverse_reactions": "Adverse Reactions",
    "drug_interactions": "Drug Interactions",
    "drug_and_or_laboratory_test_interactions": "Drug/Laboratory Test Interactions",
    "laboratory_tests": "Laboratory Tests",
    "use_in_specific_populations": "Use in Specific Populations",
    "pregnancy": "Pregnancy",
    "risks": "Pregnancy Risks",
    "teratogenic_effects": "Teratogenic Effects",
    "nonteratogenic_effects": "Nonteratogenic Effects",
    "labor_and_delivery": "Labor and Delivery",
    "nursing_mothers": "Nursing Mothers",
    "pediatric_use": "Pediatric Use",
    "geriatric_use": "Geriatric Use",
    "microbiology": "Microbiology",
    "overdosage": "Overdosage",
    "references": "References",
    "recent_major_changes": "Recent Major Changes",
    "description": "Description",
    "how_supplied": "How Supplied",
    "storage_and_handling": "Storage and Handling",
    "information_for_patients": "Patient Counseling Information",
    "spl_patient_package_insert": "Patient Information",
    "instructions_for_use": "Instructions for Use",
    "active_ingredient": "Active Ingredient",
    "inactive_ingredient": "Inactive Ingredients",
    "purpose": "Purpose",
    "do_not_use": "Do Not Use",
    "ask_doctor": "Ask a Doctor Before Use",
    "ask_doctor_or_pharmacist": "Ask a Doctor or Pharmacist Before Use",
    "when_using": "When Using This Product",
    "stop_use": "Stop Use and Ask a Doctor",
    "pregnancy_or_breast_feeding": "Pregnancy or Breast-feeding",
    "keep_out_of_reach_of_children": "Keep Out of Reach of Children",
    "questions": "Questions",
    "spl_unclassified_section": "Other Information",
}

# Bullet glyphs and look-alike characters in the label text, mapped to plain ones.
CHAR_FIXES = str.maketrans({
    "•": "-", "∘": "-", "∙": "-", "■": "-", "❏": "-", "●": "-", "\xb7": "-",
    "‑": "-", "–": "-", "’": "'", "“": '"', "”": '"', "\xa0": " ",
})


class QuotaExhausted(RuntimeError):
    """The daily embedding quota ran out; rerun after it resets."""


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.translate(CHAR_FIXES)).strip()


def section_title(field: str) -> str:
    return SECTION_TITLES.get(field, field.replace("_", " ").title())


def label_sections(label: dict) -> list[tuple[str, str]]:
    """The label's indexable sections as (field, cleaned text), in label order.

    Skips metadata, tables (their text is already flattened into the section
    text) and DROPPED_SECTIONS. openFDA also repeats subsections as fields of
    their own (pregnancy inside use_in_specific_populations, drug_interactions
    inside precautions, do_not_use inside warnings). Each subsection is kept
    under its own, more precise name and its text is cut out of the parent, so
    nothing is embedded twice; parents left with only a heading are skipped.
    """
    sections = [(field, clean(" ".join(map(str, value))))
                for field, value in label.items()
                if isinstance(value, list) and field not in NON_TEXT_FIELDS
                and not field.endswith("_table") and field not in DROPPED_SECTIONS]
    sections = [(field, text) for field, text in sections if text]
    result = []
    for field, text in sections:
        remainder = text
        for other in sorted({o for _, o in sections if o != text and o in text}, key=len, reverse=True):
            remainder = remainder.replace(other, " ")
        remainder = clean(remainder)
        if len(remainder.split()) >= MIN_SECTION_WORDS:
            result.append((field, remainder))
    return result


def split_words(text: str, max_words: int = CHUNK_WORDS) -> list[str]:
    """Split text into pieces of at most max_words words, breaking between sentences where possible."""
    pieces, current = [], []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        words = sentence.split()
        if current and len(current) + len(words) > max_words:
            pieces.append(" ".join(current))
            current = []
        while len(words) > max_words:  # a sentence longer than a chunk (lists, flattened tables)
            pieces.append(" ".join(words[:max_words]))
            words = words[max_words:]
        current += words
    if current:
        pieces.append(" ".join(current))
    return pieces


def chunk_file(path: str | Path) -> list[dict]:
    """Chunk one openFDA label JSON file into {id, text, metadata} dicts. No API calls."""
    path = Path(path)
    label = json.loads(path.read_text(encoding="utf-8"))
    openfda = label.get("openfda", {})
    brand = (openfda.get("brand_name") or [path.stem])[0]
    generic = (openfda.get("generic_name") or [""])[0].lower()
    name = f"{brand} ({generic})" if generic else brand

    chunks = []
    for field, text in label_sections(label):
        section = section_title(field)
        for part, piece in enumerate(split_words(text)):
            chunk_text = f"{name}, {section}: {piece}"
            chunks.append({
                "id": f"{path.stem}:{field}:{part}",
                "text": chunk_text,
                "metadata": {
                    "source": path.stem,
                    "brand": brand,
                    "generic": generic,
                    "manufacturer": (openfda.get("manufacturer_name") or [""])[0],
                    "product_type": (openfda.get("product_type") or [""])[0],
                    "location": section,
                    "field": field,
                    "part": part,
                    "set_id": label.get("set_id", ""),
                    "version": label.get("version", ""),
                    "url": DAILYMED_URL.format(set_id=label.get("set_id", "")),
                    "hash": hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()[:16],
                },
            })
    return chunks


def get_collection():
    client = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"))
    return client.get_or_create_collection(COLLECTION, configuration={"hnsw": {"space": "cosine"}})


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT", retries: int = 5) -> list[list[float]]:
    """Embed a batch of texts with Gemini, waiting out per-minute limits; raises QuotaExhausted on the daily one."""
    client = genai.Client(api_key=load_api_key())
    config = types.EmbedContentConfig(task_type=task_type, output_dimensionality=DIMENSIONS)
    for attempt in range(retries):
        try:
            # One Content per text: a plain list of strings is embedded as the parts of a single item.
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            response = client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            if len(response.embeddings) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(response.embeddings)}")
            return [e.values for e in response.embeddings]
        except errors.ClientError as error:
            if error.code != 429:
                raise
            if "PerDay" in str(error) or attempt == retries - 1:
                raise QuotaExhausted(str(error)) from error
            print(f"Rate limited; waiting 60 s ({attempt + 1}/{retries})", file=sys.stderr)
            time.sleep(60)
    raise RuntimeError("unreachable")


def embed_and_store(chunks: list[dict], collection) -> int:
    """Embed the chunks in batches and store each batch as soon as it returns. Returns how many were embedded."""
    for start in range(0, len(chunks), EMBED_BATCH):
        batch = chunks[start:start + EMBED_BATCH]
        vectors = embed_texts([c["text"] for c in batch])
        collection.upsert(ids=[c["id"] for c in batch], embeddings=vectors,
                          documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        print(f"  embedded {start + len(batch)}/{len(chunks)}", file=sys.stderr)
    return len(chunks)


def index_file(path: str | Path, collection=None) -> dict:
    """Chunk one label and bring its chunks in the index up to date.

    Chunks whose text is unchanged keep their saved vector; new or changed
    ones are embedded; chunks of this source that no longer exist are deleted.
    """
    collection = collection or get_collection()
    chunks = chunk_file(path)
    source = Path(path).stem
    saved = collection.get(where={"source": source}, include=["metadatas"])
    saved_hash = {i: m["hash"] for i, m in zip(saved["ids"], saved["metadatas"])}
    todo = [c for c in chunks if saved_hash.get(c["id"]) != c["metadata"]["hash"]]
    stale = sorted(set(saved_hash) - {c["id"] for c in chunks})
    if stale:
        collection.delete(ids=stale)
    embedded = embed_and_store(todo, collection) if todo else 0
    return {"source": source, "chunks": len(chunks), "embedded": embedded, "reused": len(chunks) - embedded,
            "deleted": len(stale)}


def main() -> None:
    paths = download_corpus()
    collection = get_collection()
    totals = {"chunks": 0, "embedded": 0, "reused": 0, "deleted": 0}
    for path in paths:
        try:
            result = index_file(path, collection)
        except QuotaExhausted:
            pending = sum(1 for p in paths for _ in chunk_file(p)) - collection.count()
            raise SystemExit(f"Daily embedding quota reached while indexing {path.name}. "
                             f"About {pending} chunks still need a vector; run `main.py index` again "
                             f"after the reset (09:00 in Spain). Saved vectors are kept.")
        print(f"{result['source']:10} {result['chunks']:4} chunks ({result['embedded']} embedded, "
              f"{result['reused']} reused, {result['deleted']} deleted)", file=sys.stderr)
        for key in totals:
            totals[key] += result[key]
    print(f"Index: {totals['chunks']} chunks from {len(paths)} labels, {totals['embedded']} embedded now, "
          f"{collection.count()} in {INDEX_DIR.relative_to(ROOT)}/chroma.")


if __name__ == "__main__":
    main()
