"""
Measure the coverage check on its own, without the agent.

    uv run python coverage_eval.py --version v1 --set dev
    uv run python coverage_eval.py --version v3 --set heldout
    uv run python coverage_eval.py --version v3 --set dev --model gemini-3.5-flash

For each question: search the corpus with the question itself (as server.py's
`search` tool does, using its query cache), run agent.check_coverage on the 5
passages, REPS times (flash-lite ignores the temperature), and compare with the
expected verdict:

- dev (eval/questions.csv): kind `unanswerable` -> "no"; every other -> "sí" or "parcial".
- heldout (eval/heldout_questions.txt): from eval/heldout_labels.csv, a row whose
  `expected` says "Expected refusal" -> "no"; every other -> "sí" or "parcial".

A false refusal is "no" where an answer was expected; a false coverage is "sí" or
"parcial" where "no" was expected. The model is pinned (no fallback to another
model), and the run stops cleanly if its daily quota runs out.
Writes eval/coverage_<version>[_heldout][_<model>].json.
"""

import argparse
import asyncio
import csv
import json
import sys
import time
from pathlib import Path

import agent
import server

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
PAUSE = 4  # seconds between model calls, to stay under the per-minute limit
# Query embeddings go to a cache of their own, so a run never modifies index/.
CACHE = EVAL / "coverage_query_cache.json"
if not CACHE.exists():
    CACHE.write_text(server.QUERY_CACHE.read_text(encoding="utf-8"), encoding="utf-8")
server.QUERY_CACHE = CACHE


def dev_questions() -> list[dict]:
    with (EVAL / "questions.csv").open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    return [{"id": r["id"], "question": r["question"],
             "expected": "no" if r["kind"].strip().lower() == "unanswerable" else "answer"} for r in rows]


def heldout_questions() -> list[dict]:
    with (EVAL / "heldout_labels.csv").open(newline="", encoding="utf-8") as f:
        labels = list(csv.DictReader(f))
    return [{"id": r["id"], "question": r["question"],
             "expected": "no" if "expected refusal" in r["expected"].lower() else "answer"} for r in labels]


def search_text(question: str) -> str:
    """The same text server.py's `search` tool returns for this query."""
    hits = server.retrieve(question)
    return "\n\n".join(f"[{i}] {h['source']}, {h['location']} (score {h['score']})\n{h['text']}"
                       for i, h in enumerate(hits, start=1))


def wrong(expected: str, level: str | None) -> str:
    if level is None:
        return "sin comprobar"
    if expected == "answer" and level == "no":
        return "FALSO RECHAZO"
    if expected == "no" and level != "no":
        return "FALSA COBERTURA"
    return ""


async def run(version: str, which: str, model: str, reps: int) -> dict:
    questions = dev_questions() if which == "dev" else heldout_questions()
    key = agent._api_key()
    cached_before = len(server._load_cache())
    rows, calls, stopped = [], {}, None
    for q in questions:
        result = search_text(q["question"])
        row = {**q, "verdicts": []}
        for _ in range(reps):
            if stopped:
                break
            v = await agent.check_coverage(q["question"], result, key, version=version, models=[model])
            for m in v["calls"]:
                calls[m] = calls.get(m, 0) + 1
            row["verdicts"].append({k: v[k] for k in ("level", "claimed", "need", "passage", "sentence", "quote",
                                                      "quote_found", "tokens", "seconds", "error")})
            if v["quota_exhausted"]:
                stopped = f"daily quota of {model} exhausted at {q['id']}: {v['error'][:300]}"
            await asyncio.sleep(PAUSE)
        rows.append(row)
        if stopped:
            break
    embeds = len(server._load_cache()) - cached_before
    return {"version": version, "set": which, "model": model, "reps": reps, "calls": calls,
            "embedding_calls": embeds, "stopped": stopped, "rows": rows}


def report(out: dict) -> None:
    reps = out["reps"]
    print(f"\n{out['version']} on {out['set']} with {out['model']}, {reps} run(s) per question\n")
    head = f"{'id':<5} {'esperado':<9}" + "".join(f" {'veredicto ' + str(i + 1):<14}" for i in range(reps))
    print(head + " coinciden  error")
    fr = [0] * reps
    fc = [0] * reps
    fc_unans = [0] * reps
    agree = 0
    for r in out["rows"]:
        levels = [v["level"] for v in r["verdicts"]]
        marks = []
        for i, lv in enumerate(levels):
            w = wrong(r["expected"], lv)
            fr[i] += w == "FALSO RECHAZO"
            fc[i] += w == "FALSA COBERTURA"
            marks.append(w)
        same = len(set(levels)) == 1 and len(levels) == reps
        agree += same
        exp = "no" if r["expected"] == "no" else "sí/parcial"
        cells = "".join(f" {str(lv) + (' ✗' if m else ''):<14}" for lv, m in zip(levels, marks))
        cells += "".join(f" {'-':<14}" for _ in range(reps - len(levels)))
        print(f"{r['id']:<5} {exp:<9}{cells} {'sí' if same else 'NO':<10} "
              f"{'; '.join(sorted(set(m for m in marks if m)))}")
    n = len(out["rows"])
    print(f"\nFalsos rechazos por pasada: {fr}   Falsas coberturas por pasada: {fc}")
    print(f"Veredictos iguales en las {reps} pasadas: {agree}/{n}")
    print(f"Llamadas al modelo: {out['calls']}; embeddings nuevos: {out['embedding_calls']}")
    if out["stopped"]:
        print(f"PARADO: {out['stopped']}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--version", required=True, choices=sorted(agent.COVERAGE_PROMPTS))
    p.add_argument("--set", default="dev", choices=["dev", "heldout"])
    p.add_argument("--model", default=agent.COVERAGE_MODEL)
    p.add_argument("--reps", type=int, default=2)
    a = p.parse_args()
    start = time.time()
    out = asyncio.run(run(a.version, a.set, a.model, a.reps))
    out["seconds"] = round(time.time() - start, 1)
    name = f"coverage_{a.version}" + ("_heldout" if a.set == "heldout" else "")
    if a.model != agent.COVERAGE_MODEL:
        name += "_" + a.model
    path = EVAL / f"{name}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    report(out)
    print(f"Saved {path.relative_to(ROOT)} ({out['seconds']} s)")
    if out["stopped"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
