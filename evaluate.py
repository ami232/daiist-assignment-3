"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 on the answerable questions for three
   designs over the same 150-word chunks (no re-embedding needed):
     - vector:  cosine similarity on Gemini embeddings (what server.py uses)
     - hybrid:  vector + BM25 keyword ranking, fused with reciprocal rank fusion
     - filter:  vector, restricted to the labels whose drug names the question mentions
   A hit is a retrieved chunk whose (source, location) matches an expected one.
   For multi questions "all@k" also requires every expected passage.
2. End to end: the agent's answers in eval/answers.jsonl (answer_questions.py
   fills in any missing ones first), with code checks for citations and refusals.
3. LLM judge: eval/judge_verdicts.csv (graded in a Claude chat with the rubric
   in REPORT.md, from eval/answers.md), and agreement with eval/human_labels.csv.
4. Cost and latency per question, per answer model.

Writes eval/results.json and eval/summary.md. Spends embedding quota only for
questions not yet in index/query_cache.json; the held-back Eliquis label is
excluded from retrieval so add_document does not change these numbers.
"""

import csv
import json
import math
import os
import re
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from agent import invalid_citations
from index import INDEX_DIR, embed_texts, get_collection

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge_verdicts.csv"
HUMAN = EVAL / "human_labels.csv"
QUERY_CACHE = INDEX_DIR / "query_cache.json"
HELD_BACK = {"eliquis"}
KS = (1, 3, 5)
POOL = 50     # candidates per ranking before fusion
RRF_K = 60    # standard reciprocal-rank-fusion constant
CITATION = re.compile(r"\[([a-z_]+), ([^\]]+)\]")
REFUSAL = re.compile(
    r"(do(es)? not (contain|cover|include|address|mention|provide|list|specify)|"
    r"not (covered|included|available|in the (corpus|labels?))|no information|cannot (answer|find|provide)|"
    r"(don't|do not) have|isn't covered|aren't covered)", re.I)


def split(value: str) -> list[str]:
    return [v.strip() for v in (value or "").split(";") if v.strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    """(source, location) pairs, paired by position as in validate_questions.py."""
    sources, locs = split(q["expected_source"]), split(q["expected_location"])
    if len(sources) == len(locs):
        return list(zip(sources, locs))
    return [(sources[0], l) for l in locs]


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]


# ---------- retrieval ----------

def query_vectors(texts: list[str]) -> dict:
    cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8")) if QUERY_CACHE.is_file() else {}
    missing = [t for t in dict.fromkeys(texts) if t not in cache]
    for start in range(0, len(missing), 50):
        batch = missing[start:start + 50]
        cache.update(zip(batch, embed_texts(batch, task_type="RETRIEVAL_QUERY")))
        QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return cache


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.docs = [Counter(tokens(d)) for d in docs]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / len(self.lens)
        df = Counter(t for d in self.docs for t in d)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.k1, self.b = k1, b

    def rank(self, query: str) -> list[int]:
        q = set(tokens(query))
        scores = []
        for i, d in enumerate(self.docs):
            s = 0.0
            for t in q & d.keys():
                tf = d[t]
                s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
            scores.append(s)
        return sorted(range(len(scores)), key=lambda i: -scores[i])


def drug_names(metas: list[dict]) -> dict:
    """Lower-case name -> set of sources: file name, each brand name, each active ingredient word."""
    names = defaultdict(set)
    stop = {"and", "sodium", "potassium", "hydrochloride", "magnesium", "dihydrate", "oral", "susp", "ds"}
    for m in metas:
        words = {m["source"]} | set(tokens(m["brand"])) | set(tokens(m["generic"]))
        for w in words - stop:
            if len(w) > 3:
                names[w].add(m["source"])
    return names


def retrieval(questions: list[dict]) -> dict:
    collection = get_collection()
    saved = collection.get(include=["documents", "metadatas", "embeddings"])
    keep = [i for i, m in enumerate(saved["metadatas"]) if m["source"] not in HELD_BACK]
    docs = [saved["documents"][i] for i in keep]
    metas = [saved["metadatas"][i] for i in keep]
    vecs = [saved["embeddings"][i] for i in keep]
    norms = [math.sqrt(sum(x * x for x in v)) for v in vecs]
    bm25 = BM25(docs)
    names = drug_names(metas)

    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    qvecs = query_vectors([q["question"] for q in answerable])

    def vector_rank(qv, allowed=None):
        qn = math.sqrt(sum(x * x for x in qv))
        sims = [(sum(a * b for a, b in zip(qv, v)) / (qn * n), i) for i, (v, n) in enumerate(zip(vecs, norms))
                if allowed is None or metas[i]["source"] in allowed]
        return [i for _, i in sorted(sims, reverse=True)]

    def designs(q):
        qv = qvecs[q["question"]]
        vec = vector_rank(qv)
        fused = defaultdict(float)
        for ranking in (vec[:POOL], bm25.rank(q["question"])[:POOL]):
            for r, i in enumerate(ranking):
                fused[i] += 1 / (RRF_K + r + 1)
        hybrid = sorted(fused, key=lambda i: -fused[i])
        mentioned = set().union(*[names[t] for t in set(tokens(q["question"])) if t in names] or [set()])
        filtered = vector_rank(qv, mentioned) if mentioned else vec
        return {"vector": vec, "hybrid": hybrid, "filter": filtered}

    results = {d: {"any": {k: 0 for k in KS}, "all": {k: 0 for k in KS}, "words": [], "by_kind": defaultdict(lambda: {k: 0 for k in KS})}
               for d in ("vector", "hybrid", "filter")}
    per_question = {}
    for q in answerable:
        want = {(s, l) for s, l in expected_pairs(q)}
        per_question[q["id"]] = {}
        for name, ranking in designs(q).items():
            got = [(metas[i]["source"], metas[i]["location"], metas[i]["field"]) for i in ranking[:max(KS)]]
            first = next((r + 1 for r, (s, loc, f) in enumerate(got) if (s, loc) in want or (s, f) in want), None)
            per_question[q["id"]][name] = first
            for k in KS:
                found = {p for p in want for s, loc, f in got[:k] if p in ((s, loc), (s, f))}
                results[name]["any"][k] += bool(found)
                results[name]["all"][k] += found == want
                results[name]["by_kind"][q["kind"]][k] += bool(found)
            results[name]["words"].append(sum(len(docs[i].split()) for i in ranking[:max(KS)]))

    n = len(answerable)
    kinds = Counter(q["kind"] for q in answerable)
    summary = {}
    for name, r in results.items():
        summary[name] = {
            "hit_rate": {k: round(r["any"][k] / n, 3) for k in KS},
            "all_found_rate": {k: round(r["all"][k] / n, 3) for k in KS},
            "hit_rate_by_kind": {kind: {k: round(v[k] / kinds[kind], 3) for k in KS} for kind, v in r["by_kind"].items()},
            "mean_words_top5": round(statistics.mean(r["words"])),
        }
    return {"questions": n, "designs": summary, "first_hit_rank": per_question}


# ---------- end to end ----------

def ensure_answers(questions: list[dict]) -> dict:
    answers = {r["id"]: r for r in map(json.loads, ANSWERS.read_text(encoding="utf-8").splitlines())} if ANSWERS.is_file() else {}
    if any(q["id"] not in answers for q in questions):
        print("Some questions have no saved answer; running answer_questions.py.", file=sys.stderr)
        subprocess.run([sys.executable, "answer_questions.py"], cwd=ROOT)
        answers = {r["id"]: r for r in map(json.loads, ANSWERS.read_text(encoding="utf-8").splitlines())}
    return answers


def code_checks(q: dict, a: dict) -> dict:
    answer = a["answer"] or ""
    cited = CITATION.findall(answer)
    refused = bool(REFUSAL.search(answer))
    return {
        "searched": any(t["tool"] == "search" for t in a["trace"]),
        "citations": len(cited),
        "invalid_citations": invalid_citations(answer, a["trace"]),  # agent.py's citation guardrail
        "cites_expected_source": bool({s for s, _ in cited} & set(split(q["expected_source"]))),
        "refused": refused,
    }


def agreement(judge: dict, human: dict) -> dict:
    ids = sorted(set(judge) & set(human))
    out = {"graded_by_both": len(ids)}
    for col in ("correct", "supported"):
        pairs = [(judge[i][col].strip(), human[i][col].strip()) for i in ids if human[i][col].strip() in ("0", "1")]
        if not pairs:
            continue
        agree = sum(j == h for j, h in pairs) / len(pairs)
        pj = sum(j == "1" for j, _ in pairs) / len(pairs)
        ph = sum(h == "1" for _, h in pairs) / len(pairs)
        chance = pj * ph + (1 - pj) * (1 - ph)
        out[col] = {"n": len(pairs), "agreement": round(agree, 3),
                    "cohen_kappa": round((agree - chance) / (1 - chance), 3) if chance < 1 else None,
                    "disagreements": [i for i in ids if human[i][col].strip() in ("0", "1") and judge[i][col].strip() != human[i][col].strip()]}
    return out


def main() -> None:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        questions = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    kind = {q["id"]: q["kind"] for q in questions}

    print("Retrieval...", file=sys.stderr)
    ret = retrieval(questions)

    answers = ensure_answers(questions)
    judge = {r["id"]: r for r in read_csv(JUDGE)}
    human = {r["id"]: r for r in read_csv(HUMAN) if (r.get("correct") or "").strip()}

    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if a is None:
            continue
        c = code_checks(q, a)
        j = judge.get(q["id"], {})
        rows.append({"id": q["id"], "kind": q["kind"], "model": a["model"], **c,
                     "judge_correct": j.get("correct"), "judge_supported": j.get("supported"),
                     "judge_notes": j.get("notes", ""), "tokens": a["tokens"]["total"], "seconds": a["seconds"]})

    def count(pred, subset=rows):
        return sum(1 for r in subset if pred(r))

    unans = [r for r in rows if r["kind"] == "unanswerable"]
    ans = [r for r in rows if r["kind"] != "unanswerable"]
    results = {
        "answered": len(rows),
        "code_checks": {
            "no_search": count(lambda r: not r["searched"]),
            "answerable_without_citation": count(lambda r: r["citations"] == 0, ans),
            "answers_with_invalid_citation": count(lambda r: r["invalid_citations"]),
            "answerable_citing_expected_source": count(lambda r: r["cites_expected_source"], ans),
            "correct_refusals": count(lambda r: r["refused"], unans),
            "missed_refusals": count(lambda r: not r["refused"], unans),
            "wrong_refusals": count(lambda r: r["refused"], ans),
        },
        "judge": {
            "graded": count(lambda r: r["judge_correct"] in ("0", "1")),
            "correct": count(lambda r: r["judge_correct"] == "1"),
            "unsupported": count(lambda r: r["judge_supported"] == "0"),
            "correct_refusals": count(lambda r: r["judge_correct"] == "1", unans),
            "wrong_refusals": count(lambda r: r["refused"] and r["judge_correct"] == "0", ans),
            "by_kind": {k: {"n": count(lambda r: r["kind"] == k), "correct": count(lambda r: r["kind"] == k and r["judge_correct"] == "1"),
                            "unsupported": count(lambda r: r["kind"] == k and r["judge_supported"] == "0")}
                        for k in ("single", "multi", "unanswerable")},
            "by_model": {m: {"n": count(lambda r: r["model"] == m), "correct": count(lambda r: r["model"] == m and r["judge_correct"] == "1"),
                             "unsupported": count(lambda r: r["model"] == m and r["judge_supported"] == "0")}
                         for m in dict.fromkeys(r["model"] for r in rows)},
            "failures": [{"id": r["id"], "kind": r["kind"], "model": r["model"], "correct": r["judge_correct"],
                          "supported": r["judge_supported"], "notes": r["judge_notes"],
                          "first_hit_rank_vector": ret["first_hit_rank"].get(r["id"], {}).get("vector")}
                         for r in rows if r["judge_correct"] == "0" or r["judge_supported"] == "0"],
        },
        "agreement_with_human": agreement(judge, human) if human else "eval/human_labels.csv has no grades yet",
        "cost": {m: {"n": len(v), "mean_tokens": round(statistics.mean(r["tokens"] for r in v)),
                     "mean_seconds": round(statistics.mean(r["seconds"] for r in v), 1),
                     "median_seconds": round(statistics.median(r["seconds"] for r in v), 1)}
                 for m, v in [(m, [r for r in rows if r["model"] == m]) for m in dict.fromkeys(r["model"] for r in rows)] + [("all", rows)]},
        "retrieval": ret,
        "per_question": rows,
    }
    (EVAL / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    write_summary(results)
    print((EVAL / "summary.md").read_text(encoding="utf-8"))


def write_summary(r: dict) -> None:
    ret = r["retrieval"]
    lines = ["# Evaluation summary", "", f"## Retrieval ({ret['questions']} answerable questions)", "",
             "| Design | hit@1 | hit@3 | hit@5 | all@5 (multi needs both) | words in top 5 |", "|---|---|---|---|---|---|"]
    for name, d in ret["designs"].items():
        h = d["hit_rate"]
        lines.append(f"| {name} | {h[1]:.0%} | {h[3]:.0%} | {h[5]:.0%} | {d['all_found_rate'][5]:.0%} | {d['mean_words_top5']} |")
    lines += ["", "Hit@5 by kind: " + "; ".join(f"{n}: " + ", ".join(f"{k} {v[5]:.0%}" for k, v in d["hit_rate_by_kind"].items())
                                          for n, d in ret["designs"].items()), ""]
    c, j = r["code_checks"], r["judge"]
    lines += [f"## End to end ({r['answered']} answers)", "", "Code checks: " + ", ".join(f"{k.replace('_', ' ')} {v}" for k, v in c.items()), "",
              "Citation guardrail (agent.py), applied to the saved answers, would reject: "
              + (", ".join(f"{x['id']} {x['invalid_citations']}" for x in r["per_question"] if x["invalid_citations"]) or "none"), "",
              f"Judge ({j['graded']} graded): correct {j['correct']}, unsupported {j['unsupported']}, "
              f"correct refusals {j['correct_refusals']}, wrong refusals {j['wrong_refusals']}", "",
              "| Kind | n | correct | unsupported |", "|---|---|---|---|"]
    lines += [f"| {k} | {v['n']} | {v['correct']} | {v['unsupported']} |" for k, v in j["by_kind"].items()]
    lines += ["", "| Model | n | correct | unsupported |", "|---|---|---|---|"]
    lines += [f"| {k} | {v['n']} | {v['correct']} | {v['unsupported']} |" for k, v in j["by_model"].items()]
    lines += ["", "Failures:"] + [f"- {f['id']} ({f['kind']}, {f['model']}): correct {f['correct']}, supported {f['supported']}; "
                                   f"first expected passage at vector rank {f['first_hit_rank_vector']}. {f['notes']}" for f in j["failures"]]
    a = r["agreement_with_human"]
    lines += ["", "## Agreement with human labels", ""]
    if isinstance(a, str):
        lines.append(a)
    else:
        lines.append(f"Graded by both: {a['graded_by_both']}")
        for col in ("correct", "supported"):
            if col in a:
                lines.append(f"- {col}: {a[col]['agreement']:.0%} agreement, kappa {a[col]['cohen_kappa']}, disagree on {', '.join(a[col]['disagreements']) or 'none'}")
    lines += ["", "## Cost per question", "", "| Model | n | mean tokens | mean s | median s |", "|---|---|---|---|---|"]
    lines += [f"| {m} | {v['n']} | {v['mean_tokens']} | {v['mean_seconds']} | {v['median_seconds']} |" for m, v in r["cost"].items()]
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
