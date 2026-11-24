"""Remove the demo document from the index again, so the committed index and the evaluation stay as before.

    uv run python remove_extra.py
"""
from index import DESIGNS, get_collection

SOURCE = "irs-capital-gains"

for design in DESIGNS:
    store = get_collection(design)
    before = store.count()
    store.delete(where={"source": SOURCE})
    print(f"{design}: {before} -> {store.count()} chunks")