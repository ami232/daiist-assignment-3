"""
Assignment 3: build the index (`main.py index`).

Parses the initial corpus (GDPR, AI Act, Data Act; NIS2 is held out and only
enters through server.py's add_document), chunks it with every design,
embeds only the chunks that have no saved vector, and stores everything in
index/. The pipeline itself lives in ingest.py, which server.py also imports.

    uv run python index.py                       # all designs
    uv run python index.py --designs article paragraph --budget 900
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from ingest import (CHROMA_DIR, DESIGNS, EMBED_DIM, EMBED_MODEL, INDEXED_KINDS, MANIFEST_PATH,
                    QuotaExhausted, chroma, chunk_file, collection, store_chunks)

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "corpus" / "raw"

INITIAL_CORPUS = [
    "L_2016119EN.01000101.xml.html",       # GDPR, Regulation (EU) 2016/679
    "L_202401689EN.000101.fmx.xml.html",   # AI Act, Regulation (EU) 2024/1689
    "L_202302854EN.000101.fmx.xml.html",   # Data Act, Regulation (EU) 2023/2854
]
HELD_OUT = ["L_2022333EN.01008001.xml.html"]  # NIS2, Directive (EU) 2022/2555: added later via add_document


def remove_stale(design: str, files: list[str], keep_ids: set[str], client) -> int:
    """Delete chunks of these files that the current chunking no longer produces."""
    col = collection(design, client)
    stale = []
    for f in files:
        got = col.get(where={"source_file": f}, include=[])
        stale += [i for i in got["ids"] if i not in keep_ids]
    if stale:
        col.delete(ids=stale)
    return len(stale)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--designs", nargs="+", choices=DESIGNS, default=list(DESIGNS))
    parser.add_argument("--budget", type=int, default=None, help="max new texts to embed in this run")
    args = parser.parse_args()

    missing = [f for f in INITIAL_CORPUS if not (RAW / f).is_file()]
    if missing:
        print(f"Missing corpus files in {RAW}: {missing}. See corpus/README.md.", file=sys.stderr)
        return 1

    client = chroma()
    budget = args.budget
    summary, complete = {}, True
    for design in args.designs:
        chunks = []
        for f in INITIAL_CORPUS:
            _, c = chunk_file(RAW / f, designs=[design])
            chunks += c
        print(f"[{design}] {len(chunks)} chunks", flush=True)
        try:
            stats = store_chunks(chunks, budget=budget, client=client)
        except QuotaExhausted as e:
            print(f"[{design}] stopped: {e} Vectors obtained so far are saved; run again to continue.")
            complete = False
            break
        if budget is not None:
            budget -= stats["new"]
        removed = remove_stale(design, INITIAL_CORPUS, {c.id for c in chunks}, client)
        summary[design] = {**stats, "removed_stale": removed, "in_collection": collection(design, client).count()}
        print(f"[{design}] new embeddings: {stats['new']}, stored: {stats['stored']}, "
              f"missing: {stats['missing']}, collection size: {summary[design]['in_collection']}", flush=True)
        if stats["missing"]:
            complete = False

    old = json.loads(MANIFEST_PATH.read_text()) if MANIFEST_PATH.is_file() else {}
    manifest = {
        **old,
        "model": EMBED_MODEL, "dim": EMBED_DIM, "indexed_kinds": list(INDEXED_KINDS),
        "initial_corpus": INITIAL_CORPUS, "held_out": HELD_OUT,
        "designs": {**old.get("designs", {}), **summary},
        "updated": datetime.now().isoformat(timespec="seconds"),
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    print("Index complete." if complete else "Index incomplete: run `main.py index` again after the quota resets (09:00 Spain).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
