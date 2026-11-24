"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (chunking x search
   mode) on the answerable questions -> eval/retrieval.csv
2. End to end: runs the agent on every question -> eval/answers.jsonl
   (resumable: questions already answered are skipped; delete the file to rerun)
3. Code checks: refusal, citations present, citations valid (returned by
   search), expected article cited.
4. LLM judge with a rubric and the retrieved text as evidence -> eval/judge.jsonl
5. Agreement between the judge and eval/human_labels.csv.
6. Summary -> eval/summary.json, eval/results.csv
"""

from __future__ import annotations

import csv
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
HUMAN = EVAL / "human_labels.csv"

DESIGNS = [("article", "dense"), ("article", "hybrid"), ("fixed", "dense"), ("fixed", "hybrid")]
KS = (1, 3, 5)
JUDGE_MODELS = ("gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-lite-latest")

RUBRIC = """You grade an answer from a Spanish labour-law assistant for HR staff.
You get the question, a reference answer written by an expert, the assistant's
answer, and the passages the assistant retrieved (its only allowed evidence).

Grade two things, each 1 or 0:

correct
  1 if the answer states the key facts of the reference (numbers, durations,
    amounts, conditions) without contradicting it. Extra correct detail is fine.
    Missing a secondary detail is fine; missing or getting wrong the main figure
    is not.
  For an UNANSWERABLE question (reference says the corpus does not cover it):
    1 only if the assistant declines ("El corpus no cubre esta pregunta" or
    equivalent) and does not give a substantive answer from outside knowledge.
  For an answerable question, a refusal is 0.

supported
  1 if every factual claim in the answer appears in the retrieved passages
    (paraphrase is fine). 0 if any number, deadline, amount or rule is not in
    them, even if it happens to be true. A pure refusal is supported (1).

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}"""


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def load_questions() -> pd.DataFrame:
    df = pd.read_csv(QUESTIONS, dtype=str).fillna("")
    df["kind"] = df["kind"].str.strip().str.lower()
    return df


def expected_pairs(row) -> list[tuple[str, str]]:
    srcs = [s.strip() for s in row["expected_source"].split(";")]
    locs = [l.strip() for l in row["expected_location"].split(";")]
    if len(srcs) == 1 and len(locs) > 1:
        srcs = srcs * len(locs)
    return list(zip(srcs, locs))


def loc_matches(chunk_location: str, expected: str) -> bool:
    """'Artículo 49, apdo. 1' matches 'Artículo 49' (not 'Artículo 4').
    Fixed-window chunks list several locations separated by ';'."""
    for loc in chunk_location.split(";"):
        loc = loc.strip()
        if loc == expected or loc.startswith(expected + ",") or loc.startswith(expected + " ("):
            return True
    return False


def hit(chunk: dict, pairs) -> set[int]:
    return {i for i, (s, l) in enumerate(pairs) if chunk["source"] == s and loc_matches(chunk["location"], l)}


# --------------------------------------------------------------------------- #
# 1. Retrieval
# --------------------------------------------------------------------------- #

def evaluate_retrieval(df: pd.DataFrame) -> pd.DataFrame:
    import retrieval

    answerable = df[df["kind"] != "unanswerable"]
    retrieval.embed_queries(list(answerable["question"]))
    rows, per_q = [], []
    for design, mode in DESIGNS:
        stats = {f"hit@{k}": [] for k in KS} | {f"all@{k}": [] for k in KS}
        words = []
        for _, q in answerable.iterrows():
            pairs = expected_pairs(q)
            hits = retrieval.search(q["question"], k=max(KS), design=design, mode=mode,
                                    base_only=True)
            words.append(sum(len(h["text"].split()) for h in hits))
            for k in KS:
                found = set().union(*(hit(h, pairs) for h in hits[:k])) if hits else set()
                stats[f"hit@{k}"].append(int(bool(found)))
                stats[f"all@{k}"].append(int(len(found) == len(pairs)))
            first = next((r for r, h in enumerate(hits, 1) if hit(h, pairs)), None)
            per_q.append({"design": f"{design}/{mode}", "id": q["id"], "kind": q["kind"], "first_hit_rank": first})
        sub = answerable["kind"].values
        row = {"design": f"{design}/{mode}", "questions": len(answerable),
               "words_in_prompt@5": round(sum(words) / len(words))}
        for k in KS:
            row[f"hit@{k}"] = round(sum(stats[f"hit@{k}"]) / len(answerable), 3)
        for k in KS:
            multi = [v for v, kind in zip(stats[f"all@{k}"], sub) if kind == "multi"]
            row[f"multi_all@{k}"] = round(sum(multi) / len(multi), 3) if multi else None
        rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(EVAL / "retrieval.csv", index=False)
    pd.DataFrame(per_q).to_csv(EVAL / "retrieval_per_question.csv", index=False)
    return out


# --------------------------------------------------------------------------- #
# 2. Agent answers
# --------------------------------------------------------------------------- #

def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return {r["id"]: r for r in map(json.loads, path.read_text(encoding="utf-8").splitlines()) if r}


def run_agent(df: pd.DataFrame) -> dict[str, dict]:
    import agent
    done = read_jsonl(ANSWERS)
    for _, q in df.iterrows():
        if q["id"] in done:
            continue
        print(f"  agent: {q['id']} {q['question'][:70]}", file=sys.stderr, flush=True)
        try:
            out = agent.run(q["question"], interactive=False)
        except Exception as e:  # noqa: BLE001 - record the failure, keep going
            out = {"question": q["question"], "answer": f"ERROR: {type(e).__name__}: {e}"[:500],
                   "trace": [], "retrieved": [], "guardrail": None,
                   "tokens": {"input": 0, "output": 0}, "seconds": 0}
        out["id"] = q["id"]
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
        done[q["id"]] = out
    return done


# --------------------------------------------------------------------------- #
# 3. Code checks
# --------------------------------------------------------------------------- #

def code_checks(q, ans: dict) -> dict:
    from agent import CITATION_RE, REFUSAL, check_citations
    text = ans["answer"]
    refused = text.strip().startswith(REFUSAL) or "no cubre esta pregunta" in text.lower()
    cites = CITATION_RE.findall(text)
    valid, _ = check_citations(text, set(ans.get("retrieved", [])))
    pairs = expected_pairs(q) if q["kind"] != "unanswerable" else []
    retrieved_ok = any(any(s_title_match(c, s) and loc_in_cite(c, l) for c in ans.get("retrieved", []))
                       for s, l in pairs)
    cited_expected = any(any(s_title_match(c, s) and loc_in_cite(c, l) for c in cites) for s, l in pairs)
    return {
        "refused": int(refused),
        "n_citations": len(cites),
        "citations_valid": int(valid and (refused or bool(cites))),
        "expected_retrieved": int(retrieved_ok) if pairs else None,
        "cited_expected": int(cited_expected) if pairs else None,
        "refusal_correct": int(refused) if q["kind"] == "unanswerable" else None,
        "wrong_refusal": int(refused) if q["kind"] != "unanswerable" else None,
        "guardrail_fired": int(bool(ans.get("guardrail"))),
        "error": int(text.startswith("ERROR")),
    }


_TITLES = None


def s_title_match(citation: str, source: str) -> bool:
    global _TITLES
    if _TITLES is None:
        from index import KNOWN_TITLES
        _TITLES = KNOWN_TITLES
    return citation.startswith(_TITLES.get(source, source))


def loc_in_cite(citation: str, expected_loc: str) -> bool:
    loc = citation.split("), ", 1)[-1] if "), " in citation else citation.split(", ", 1)[-1]
    return loc_matches(loc, expected_loc)


# --------------------------------------------------------------------------- #
# 4. LLM judge
# --------------------------------------------------------------------------- #

def judge_one(q, ans: dict) -> dict:
    from google.genai import errors, types
    from index import genai_client
    evidence = "\n\n".join(t["text"] for t in ans.get("trace", []) if "text" in t)[:30000] or "(nothing retrieved)"
    prompt = (f"QUESTION ({q['kind']}): {q['question']}\n\nREFERENCE ANSWER: {q['reference_answer']}\n\n"
              f"ASSISTANT ANSWER:\n{ans['answer']}\n\nRETRIEVED PASSAGES:\n{evidence}")
    last = None
    for model in JUDGE_MODELS:
        for attempt in range(3):
            try:
                r = genai_client().models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=RUBRIC, temperature=0,
                                                       response_mime_type="application/json"))
                v = json.loads(re.search(r"\{.*\}", r.text, re.S).group(0))
                return {"correct": int(v["correct"]), "supported": int(v["supported"]),
                        "reason": v.get("reason", ""), "judge_model": model}
            except errors.APIError as e:
                last = e
                if e.code in (429, 500, 503):
                    time.sleep(5 * (attempt + 1))
                    continue
                break
            except (ValueError, KeyError, AttributeError) as e:
                last = e
    raise RuntimeError(f"judge failed: {last}")


def run_judge(df: pd.DataFrame, answers: dict) -> dict[str, dict]:
    done = read_jsonl(JUDGE)
    for _, q in df.iterrows():
        if q["id"] in done or q["id"] not in answers:
            continue
        print(f"  judge: {q['id']}", file=sys.stderr, flush=True)
        v = judge_one(q, answers[q["id"]]) | {"id": q["id"]}
        with JUDGE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")
        done[q["id"]] = v
    return done


# --------------------------------------------------------------------------- #
# 5. Agreement with human labels
# --------------------------------------------------------------------------- #

def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def agreement(verdicts: dict) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    out = {"n": 0}
    for col in ("correct", "supported"):
        pairs = [(int(r[col]), verdicts[r["id"]][col]) for r in human
                 if r["id"] in verdicts and str(r.get(col, "")).strip() in {"0", "1"}]
        if pairs:
            h, j = zip(*pairs)
            out["n"] = max(out["n"], len(pairs))
            out[col] = {"agreement": round(sum(x == y for x, y in pairs) / len(pairs), 3),
                        "kappa": kappa(list(h), list(j)),
                        "disagreements": [r["id"] for r in human if r["id"] in verdicts
                                          and str(r.get(col, "")).strip() in {"0", "1"}
                                          and int(r[col]) != verdicts[r["id"]][col]]}
    return out


# --------------------------------------------------------------------------- #
# 6. Summary
# --------------------------------------------------------------------------- #

def failure_hint(q, c: dict, v: dict) -> str:
    """A first guess at the failure cause; the final classification is manual."""
    if q["kind"] == "unanswerable":
        return "" if c["refused"] else "answered an unanswerable question (unsupported claim)"
    if c["refused"]:
        return "wrong refusal" if c["expected_retrieved"] else "retrieval miss (refused)"
    if v.get("correct") and v.get("supported"):
        return ""
    if not c["expected_retrieved"]:
        return "retrieval miss"
    if not v.get("supported"):
        return "unsupported claim"
    return "wrong answer from the right passage"


def main() -> None:
    df = load_questions()
    print("== 1. Retrieval hit rate (answerable questions, base corpus) ==")
    ret = evaluate_retrieval(df)
    print(ret.to_string(index=False))

    print("\n== 2. Agent on every question ==")
    answers = run_agent(df)
    print("\n== 3/4. Code checks and LLM judge ==")
    verdicts = run_judge(df, answers)

    rows = []
    for _, q in df.iterrows():
        a, v = answers[q["id"]], verdicts.get(q["id"], {})
        c = code_checks(q, a)
        rows.append({"id": q["id"], "kind": q["kind"], **c,
                     "judge_correct": v.get("correct"), "judge_supported": v.get("supported"),
                     "judge_reason": v.get("reason", ""),
                     "tokens_in": a["tokens"]["input"], "tokens_out": a["tokens"]["output"],
                     "seconds": a["seconds"], "failure_hint": failure_hint(q, c, v),
                     "answer": a["answer"]})
    res = pd.DataFrame(rows)
    res.to_csv(EVAL / "results.csv", index=False)

    ans = res[res.kind != "unanswerable"]
    una = res[res.kind == "unanswerable"]
    summary = {
        "questions": len(res),
        "retrieval": ret.to_dict(orient="records"),
        "end_to_end": {
            "correct (judge)": int(res.judge_correct.sum()),
            "correct answers to answerable": int(((ans.judge_correct == 1) & (ans.refused == 0)).sum()),
            "answerable": len(ans),
            "unsupported (judge supported=0)": int((res.judge_supported == 0).sum()),
            "correct refusals": int(una.refused.sum()),
            "unanswerable": len(una),
            "wrong refusals": int(ans.refused.sum()),
            "invalid or missing citations (code)": int((res.citations_valid == 0).sum()),
            "cited expected article (code)": int(ans.cited_expected.sum()),
            "guardrail fired": int(res.guardrail_fired.sum()),
            "errors": int(res.error.sum()),
        },
        "by_kind": res.groupby("kind")[["judge_correct", "judge_supported", "refused"]].mean().round(3).to_dict(),
        "cost_per_question": {
            "tokens_in_mean": round(res.tokens_in.mean()), "tokens_out_mean": round(res.tokens_out.mean()),
            "seconds_mean": round(res.seconds.mean(), 1), "seconds_median": round(res.seconds.median(), 1),
        },
        "failure_hints": res[res.failure_hint != ""].groupby("failure_hint")["id"].apply(list).to_dict(),
        "judge_vs_human": agreement(verdicts),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "retrieval"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
