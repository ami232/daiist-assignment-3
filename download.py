"""
Assignment 3: download the corpus from openFDA. `uv run python download.py`

Fetches each FDA drug label in LABELS from the openFDA drug/label endpoint by
its set_id and saves the raw JSON in corpus/ (held-back labels in
corpus/held_back/, so the index stage skips them until add-document is used).
Labels already on disk are not downloaded again. Also writes
corpus/manifest.csv with the facts the report's corpus table needs.

index.py calls download_corpus(), so `main.py index` needs no manual step.
"""

import csv
import json
import sys
import time
from datetime import date
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
HELD_BACK_DIR = CORPUS_DIR / "held_back"
MANIFEST = CORPUS_DIR / "manifest.csv"

API_URL = "https://api.fda.gov/drug/label.json"
DAILYMED_URL = "https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid={set_id}"
LICENCE = "CC0 1.0 (openFDA, https://open.fda.gov/license/)"

# One label per drug, pinned by set_id. `version` is the label version chosen on
# 2026-11-17; openFDA only serves the latest one, so a mismatch means FDA has
# updated the label since and its text may differ.
LABELS = [
    # Anti-inflammatories and pain relief
    {"file": "flanax", "set_id": "2c099d45-f03a-4161-a6af-8fe5965f2748", "version": "14"},
    {"file": "aleve", "set_id": "1266393e-b55e-4e34-9710-0b87209f4158", "version": "16"},
    {"file": "naproxen", "set_id": "c1cb9bb9-fbae-5e5c-e053-2995a90a0d21", "version": "12"},
    {"file": "advil", "set_id": "1f01c10a-9434-91a4-2ee4-352315a6b610", "version": "37"},
    {"file": "celebrex", "set_id": "2d6675e4-5859-4be2-8037-a20ce9f707aa", "version": "13"},
    {"file": "tylenol", "set_id": "4961695d-72f3-533a-e063-6294a90a5a29", "version": "1"},
    # Anticoagulants and antiplatelets
    {"file": "jantoven", "set_id": "19a69a72-ac5d-45d5-a94d-a5aaecbe4730", "version": "14"},
    {"file": "plavix", "set_id": "de8b0b67-eb25-4684-83b5-7ad785314227", "version": "5"},
    # Antibiotics (Amoxil and Augmentin are only available as repackager labels)
    {"file": "amoxil", "set_id": "ec7dd735-dc92-3d29-e053-2a95a90af549", "version": "3"},
    {"file": "augmentin", "set_id": "04a31a42-d79e-bbb4-e063-6394a90a63ee", "version": "5"},
    {"file": "zithromax", "set_id": "db52b91e-79f7-4cc1-9564-f2eee8e31c45", "version": "49"},
    {"file": "cipro", "set_id": "888dc7f9-ad9c-4c00-8d50-8ddfd9bd27c0", "version": "32"},
    {"file": "bactrim", "set_id": "f59d0c04-9c66-4d53-a0e1-cb55570deb62", "version": "18"},
    # Stomach protection
    {"file": "prilosec", "set_id": "b6761f84-53ac-4745-a8c8-1e5427d7e179", "version": "8"},
    # Held back for the add-document demo
    {"file": "eliquis", "set_id": "e9481622-7cc6-418a-acb6-c5450daae9b0", "version": "39", "held_back": True},
]

# Fields that are metadata or images, not label text.
NON_TEXT_FIELDS = {"set_id", "id", "version", "effective_time", "openfda",
                   "spl_product_data_elements", "package_label_principal_display_panel"}


def label_path(entry: dict) -> Path:
    folder = HELD_BACK_DIR if entry.get("held_back") else CORPUS_DIR
    return folder / f"{entry['file']}.json"


def fetch_label(set_id: str, retries: int = 4) -> str:
    """Return the raw JSON text of one openFDA label, retrying on rate limits and server errors."""
    params = {"search": f'set_id:"{set_id}"', "limit": 1}
    for attempt in range(retries):
        response = httpx.get(API_URL, params=params, timeout=60)
        if response.status_code in (429, 500, 502, 503, 504) and attempt < retries - 1:
            time.sleep(2 ** attempt)
            continue
        response.raise_for_status()
        results = response.json().get("results", [])
        if len(results) != 1:
            raise ValueError(f"openFDA returned {len(results)} labels for set_id {set_id}")
        return json.dumps(results[0], indent=2, ensure_ascii=False)
    raise RuntimeError("unreachable")


def word_count(label: dict) -> int:
    return sum(len(str(text).split())
               for field, value in label.items()
               if field not in NON_TEXT_FIELDS and not field.endswith("_table") and isinstance(value, list)
               for text in value)


def manifest_row(entry: dict, label: dict, downloaded: str) -> dict:
    openfda = label.get("openfda", {})
    return {
        "document": entry["file"],
        "brand_name": ", ".join(openfda.get("brand_name", [])),
        "generic_name": ", ".join(openfda.get("generic_name", [])),
        "manufacturer": ", ".join(openfda.get("manufacturer_name", [])),
        "product_type": ", ".join(openfda.get("product_type", [])),
        "held_back": bool(entry.get("held_back")),
        "set_id": label["set_id"],
        "version": label.get("version", ""),
        "effective_time": label.get("effective_time", ""),
        "url": DAILYMED_URL.format(set_id=label["set_id"]),
        "downloaded": downloaded,
        "licence": LICENCE,
        "words": word_count(label),
    }


def download_corpus() -> list[Path]:
    """Download every label in LABELS that is not on disk yet; return the paths of the indexable ones."""
    HELD_BACK_DIR.mkdir(parents=True, exist_ok=True)
    previous = {}
    if MANIFEST.is_file():
        with MANIFEST.open(newline="", encoding="utf-8") as f:
            previous = {row["document"]: row for row in csv.DictReader(f)}

    rows = []
    for entry in LABELS:
        path = label_path(entry)
        if path.is_file():
            downloaded = previous.get(entry["file"], {}).get("downloaded", "")
        else:
            path.write_text(fetch_label(entry["set_id"]), encoding="utf-8")
            downloaded = date.today().isoformat()
            print(f"Downloaded {path.relative_to(ROOT)}", file=sys.stderr)
            time.sleep(0.3)  # stay well under openFDA's rate limit
        label = json.loads(path.read_text(encoding="utf-8"))
        if label.get("version") != entry["version"]:
            print(f"WARNING: {entry['file']} is version {label.get('version')}, "
                  f"expected {entry['version']}; FDA has updated this label.", file=sys.stderr)
        rows.append(manifest_row(entry, label, downloaded))

    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    indexed = [r for r in rows if not r["held_back"]]
    print(f"Corpus: {len(indexed)} labels, {sum(r['words'] for r in indexed):,} words "
          f"(+{len(rows) - len(indexed)} held back). Manifest: {MANIFEST.relative_to(ROOT)}", file=sys.stderr)
    return [label_path(e) for e in LABELS if not e.get("held_back")]


if __name__ == "__main__":
    download_corpus()
