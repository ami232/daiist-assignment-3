"""
Helper for writing the test set: print one section of one medicine, as indexed.

    uv run python peek.py eliquis "SmPC 4.2"
    uv run python peek.py pradaxa "Leaflet 3"
    uv run python peek.py xarelto            # list the sections it has

Reads corpus/chunks_structured.jsonl (written by `main.py index`). No Gemini calls.
"""

import json
import sys
from pathlib import Path

CHUNKS = Path(__file__).resolve().parent / "corpus" / "chunks_structured.jsonl"

chunks = [json.loads(line) for line in CHUNKS.read_text(encoding="utf-8").splitlines()]
source = sys.argv[1].lower() if len(sys.argv) > 1 else "eliquis"
wanted = sys.argv[2] if len(sys.argv) > 2 else None
mine = [c for c in chunks if c["source"] == source]

if not wanted:
    print(f"Sections in {source} (location, page, header):")
    for c in mine:
        print(f"  {c['location']:<30} p.{c['page']:<4} {c['header'][:90]}")
else:
    hits = [c for c in mine if wanted in c["locations"]]
    for c in hits:
        print(f"\n===== {source} | {c['location']} | page {c['page']} =====\n{c['text']}")
    print(f"\n({len(hits)} chunk(s) of {source} in {wanted})")
