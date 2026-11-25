"""Re-run evaluate.py's retrieval stage on the corpus as it was before add_document:
the same index, with BOCG-15-A-1-2 (the demo document) dropped from every collection."""
import sys
import numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
import evaluate as ev

DROP = "BOCG-15-A-1-2"
_orig = ev.load_strategy
def load_four(strategy):
    store = _orig(strategy)
    if not store:
        return store
    keep = [i for i, m in enumerate(store["metadatas"]) if m.get("doc_id") != DROP]
    print(f"  {strategy}: {len(store['ids'])} -> {len(keep)} chunks", file=sys.stderr)
    texts = [store["texts"][i] for i in keep]
    return {"ids": [store["ids"][i] for i in keep], "texts": texts,
            "metadatas": [store["metadatas"][i] for i in keep],
            "vectors": store["vectors"][keep],
            "bm25": ev.BM25([ev.tokenize(t) for t in texts])}
ev.load_strategy = load_four

rows = ev.read_questions()
detail, summary, best = ev.evaluate_retrieval(rows)
ev.write_csv(ev.EVAL_DIR / "retrieval_4docs.csv", detail)
ev.write_csv(ev.EVAL_DIR / "retrieval_summary_4docs.csv", summary)
