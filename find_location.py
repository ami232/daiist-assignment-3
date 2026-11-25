"""
Helper for writing eval/questions.csv: which chunk holds a phrase from a filing?

    uv run python find_location.py "net capital expenditures"

Prints the source and location to put in expected_source / expected_location.
Searches the saved index only (exact text match, no embeddings, costs no quota).
"""

import sys

from index import get_collection

phrase = " ".join(sys.argv[1:]).strip().lower()
if not phrase:
    sys.exit('Give a phrase: uv run python find_location.py "a few words from the filing"')

data = get_collection().get(include=["documents", "metadatas"])
hits = [(m, d) for d, m in zip(data["documents"], data["metadatas"]) if phrase in " ".join(d.lower().split())]
if not hits:
    sys.exit("Not found. Try fewer words; tables and line breaks can split a phrase.")
for m, d in hits[:10]:
    start = " ".join(d.lower().split()).find(phrase)
    print(f"{m['source']}  |  {m['location']}\n   ...{d[max(0, start - 80):start + 120]}...\n")
if len(hits) > 10:
    print(f"({len(hits) - 10} more matches; use a longer phrase)")
