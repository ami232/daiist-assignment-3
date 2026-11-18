"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

Stages (default: all of them, in this order):
  retrieval  hit rate at k = 1/3/5 for each retrieval design   -> eval/retrieval.json, retrieval_by_question.csv
  answers    run the agent on every question (resumable)       -> eval/answers.json, answers_for_grading.csv
  judge      code checks + LLM judge + agreement with my       -> eval/judge.json, summary.json/.md, failures.csv
             own labels in eval/human_labels.csv

    uv run python evaluate.py --stage answers   # then grade 20+ answers yourself in human_labels.csv
    uv run python evaluate.py --stage judge     # only now read the judge's verdicts
    uv run python evaluate.py --demo            # add_document before/after (changes the index, then restores it)

Designs compared: "article" (one chunk per article), "fixed" (150-word windows), each with dense
search only and with dense + BM25 merged by reciprocal rank fusion ("+bm25").
A hit means the chunk's cited source AND location (what a user would see) is the expected one;
a question that needs two passages is a hit at k only when both are in the top k.
"""

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

import index as ix

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS, HUMAN_LABELS = EVAL / "questions.csv", EVAL / "human_labels.csv"
RETRIEVAL_JSON, RETRIEVAL_CSV = EVAL / "retrieval.json", EVAL / "retrieval_by_question.csv"
ANSWERS, GRADING_CSV = EVAL / "answers.json", EVAL / "answers_for_grading.csv"
JUDGE_JSON, SUMMARY_JSON, SUMMARY_MD = EVAL / "judge.json", EVAL / "summary.json", EVAL / "summary.md"
FAILURES_CSV, DEMO_JSON = EVAL / "failures.csv", EVAL / "demo.json"

JUDGE_MODEL = os.environ.get("GEMINI_JUDGE_MODEL", "gemini-3.8-flash")
KS = (1, 3, 5)
DEPTH = 10            # how deep retrieval ranks are recorded
BATCH = 4             # questions per agent run (results are saved after every batch)
PAUSE = 6             # seconds between questions: stays under the free-tier request limits
# Price per million tokens of the agent model (see Google's Gemini pricing page); 0 = not set.
PRICE_IN_PER_M, PRICE_OUT_PER_M = 0.0, 0.0
DEMO_ID, DEMO_SOURCE = "q27", "RD 1312/2024"


# ----------------------------------------------------------------- helpers

def _n(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\xa0", " ")).strip().lower()


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in q["expected_location"].split(";") if l.strip()]
    return [(_n(s), _n(l)) for s, l in zip(sources, locations)]


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# --------------------------------------------------------------- retrieval

STOPWORDS = set("""a al algo ante con como cual cuales cuando cuanto cuantos cuanta cuantas de del desde donde el ella
ellos en entre es esta este esto ha han hay la las le les lo los mas me mi mis no o para pero por que quien se si sin
sobre su sus un una uno unos unas y ya puede pueden debe deben ser son sea cada tiene tienen""".split())
SUFFIXES = sorted("""amientos amiento aciones acion uciones ucion idades idad mente ables able ores ador ados adas ando
iendo ar er ir os as es a o s""".split(), key=len, reverse=True)


def tokens(text: str) -> list[str]:
    """Lower-case, accent-free words, no stopwords, crude Spanish suffix stripping."""
    text = "".join(c for c in unicodedata.normalize("NFD", text.lower()) if not unicodedata.combining(c))
    out = []
    for word in re.findall(r"[a-z0-9]+", text):
        if word in STOPWORDS or len(word) < 2:
            continue
        for suffix in SUFFIXES:
            if word.endswith(suffix) and len(word) - len(suffix) >= 4:
                word = word[: -len(suffix)]
                break
        out.append(word)
    return out


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.lengths, self.tf = [], []
        df = Counter()
        for doc in docs:
            toks = tokens(doc)
            self.lengths.append(len(toks))
            self.tf.append(Counter(toks))
            df.update(set(toks))
        self.n = len(docs)
        self.avg = sum(self.lengths) / max(self.n, 1)
        self.idf = {w: math.log(1 + (self.n - c + 0.5) / (c + 0.5)) for w, c in df.items()}

    def rank(self, query: str, top: int = 50) -> list[int]:
        words = tokens(query)
        scores = []
        for i, (tf, length) in enumerate(zip(self.tf, self.lengths)):
            s = 0.0
            for w in words:
                f = tf.get(w)
                if f:
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            scores.append((s, i))
        return [i for s, i in sorted(scores, reverse=True)[:top] if s > 0]


def rrf(*rankings: list[int], k: int = 60) -> list[int]:
    score = Counter()
    for ranking in rankings:
        for pos, idx in enumerate(ranking, 1):
            score[idx] += 1 / (k + pos)
    return [idx for idx, _ in score.most_common()]


def first_rank(order: list[int], items: list, pairs: list, depth: int = DEPTH):
    """Rank at which ALL expected (source, location) pairs are present, or None."""
    ranks = []
    for source, location in pairs:
        r = next((pos for pos, idx in enumerate(order[:depth], 1)
                  if _n(items[idx][0]["source"]) == source and _n(items[idx][0]["location"]) == location), None)
        if r is None:
            return None
        ranks.append(r)
    return max(ranks)


def retrieval_stage(questions: list[dict]) -> dict:
    from server import embed_query          # same query embeddings (and cache) the agent's search uses

    designs = {}
    for design in ix.DESIGNS:
        col = ix.get_collection(design)
        if col.count() == 0:
            log(f"design {design!r} has no embedded chunks yet: skipped (run `index.py --designs={design}`)")
            continue
        data = col.get(include=["documents", "metadatas"])
        items = list(zip(data["metadatas"], data["documents"]))
        text = [f"{m['location']} {m.get('section', '')} {d}" for m, d in items]
        designs[design] = {"col": col, "ids": {cid: i for i, cid in enumerate(data["ids"])},
                           "items": items, "bm25": BM25(text)}

    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    ranks = {f"{d}{s}": {} for d in designs for s in ("", "+bm25")}
    for n, q in enumerate(answerable, 1):
        vector = embed_query(q["question"])
        pairs = expected_pairs(q)
        for design, d in designs.items():
            res = d["col"].query(query_embeddings=[vector], n_results=min(50, d["col"].count()), include=[])
            dense = [d["ids"][cid] for cid in res["ids"][0]]
            lexical = d["bm25"].rank(q["question"])
            for name, order in ((design, dense), (design + "+bm25", rrf(dense, lexical))):
                ranks[name][q["id"]] = (first_rank(order, d["items"], pairs),
                                        sum(d["items"][i][0]["words"] for i in order[:5]))
        if n % 10 == 0:
            log(f"retrieval: {n}/{len(answerable)} questions")

    kinds = {q["id"]: q["kind"] for q in answerable}
    summary = {"questions": len(answerable), "designs": {}}
    rows = []
    for name, per_q in ranks.items():
        entry = {"words@5": round(sum(w for _, w in per_q.values()) / len(per_q))}
        for scope, ids in (("all", list(per_q)), ("single", [i for i in per_q if kinds[i] == "single"]),
                           ("multi", [i for i in per_q if kinds[i] == "multi"])):
            for k in KS:
                hits = sum(1 for i in ids if per_q[i][0] is not None and per_q[i][0] <= k)
                entry[f"{scope}_hit@{k}"] = round(hits / len(ids), 3) if ids else None
        summary["designs"][name] = entry
        for i, (rank, words) in per_q.items():
            rows.append({"design": name, "id": i, "kind": kinds[i], "rank_of_all_expected": rank or "", "words@5": words})
    save_json(RETRIEVAL_JSON, summary)
    write_csv(RETRIEVAL_CSV, ["design", "id", "kind", "rank_of_all_expected", "words@5"], rows)

    print(f"\nRETRIEVAL on {len(answerable)} answerable questions (hit = expected source+location in top k)")
    print(f"{'design':<16}{'hit@1':>7}{'hit@3':>7}{'hit@5':>7}   {'single@5':>8}{'multi@5':>8}{'words@5':>9}")
    for name, e in summary["designs"].items():
        print(f"{name:<16}{e['all_hit@1']:>7.2f}{e['all_hit@3']:>7.2f}{e['all_hit@5']:>7.2f}   "
              f"{e['single_hit@5']:>8.2f}{e['multi_hit@5']:>8.2f}{e['words@5']:>9}")
    best = max(summary["designs"].items(), key=lambda kv: (kv[1]["all_hit@5"], kv[1]["all_hit@3"], kv[1]["all_hit@1"]))
    print(f"best by hit@5: {best[0]}. The server uses design {ix.DEFAULT_DESIGN!r} with dense search "
          "(change DEFAULT_DESIGN in index.py or add BM25 to server.py if another row wins clearly).")
    return summary


# ------------------------------------------------------------- end to end

def answers_stage(questions: list[dict], rerun: bool = False) -> dict:
    from agent import deny_all, run

    answers = load_json(ANSWERS, {})
    todo = [q for q in questions if rerun or q["id"] not in answers or answers[q["id"]].get("error")]
    log(f"answers: {len(questions) - len(todo)} already saved, {len(todo)} to run")
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        results = run([q["question"] for q in batch], approve=deny_all, pause=PAUSE)
        for q, r in zip(batch, results):
            answers[q["id"]] = r.to_dict()
        save_json(ANSWERS, answers)
        log(f"answers: {min(start + BATCH, len(todo))}/{len(todo)} done")
        if start + BATCH < len(todo):
            time.sleep(PAUSE)
    errors = [i for i, a in answers.items() if a.get("error")]
    if errors:
        log(f"WARNING: {len(errors)} answers ended in an error ({', '.join(errors)}); run again to retry them")
    write_grading_sheet(questions, answers)
    return answers


def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    """What I grade by hand: question, reference, answer, citations. No judge verdicts here."""
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if a:
            rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                         "reference_answer": q["reference_answer"], "answer": a["answer"],
                         "cited": "; ".join(f"[{s}, {l}]" for s, l in a["citations"])})
    write_csv(GRADING_CSV, ["id", "kind", "question", "reference_answer", "answer", "cited"], rows)


def code_checks(q: dict, a: dict) -> dict:
    """Everything code can verify: errors, citations, refusals, expected passages."""
    checks = {"no_error": not a["error"], "citations_valid": not a["invalid_citations"],
              "guard": a["guard"] or "none"}
    if q["kind"] == "unanswerable":
        checks["refused_as_expected"] = a["refused"]
    else:
        pairs = expected_pairs(q)
        retrieved = {(_n(s), _n(l)) for s, l in a["retrieved"]}
        cited = {(_n(s), _n(l)) for s, l in a["citations"]}
        checks["not_wrongly_refused"] = not a["refused"]
        checks["expected_retrieved"] = all(p in retrieved for p in pairs)
        checks["expected_cited"] = (not a["refused"]) and all(p in cited for p in pairs)
    return checks


# ------------------------------------------------------------------- judge

JUDGE_PROMPT = """You grade the answer of an assistant that answers questions about Spanish rental and tourist-rental law \
using only retrieved passages.

QUESTION:
{question}

REFERENCE (the correct answer; for a question the documents cannot answer, what the assistant should say):
{reference}

ANSWER TO GRADE:
{answer}

RETRIEVED PASSAGES (the only evidence the assistant had):
{evidence}

Rubric:
- correct = 1 if the answer agrees with the reference in substance: every number, deadline, majority and amount in the \
reference is present and right and nothing contradicts it. Extra correct detail is fine. If the documents cannot answer \
the question, correct = 1 only if the answer refuses (it starts with "No puedo responder con los documentos \
disponibles.") and does not state a legal rule as fact. Refusing a question that has an answer is correct = 0.
- supported = 1 if every factual claim of the answer appears in the retrieved passages (check each number). A claim that \
comes from general knowledge, or from a passage that was not retrieved, makes it 0. A plain refusal is supported = 1.

Reply with JSON only: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}}"""


def call_judge(prompt: str, retries: int = 4) -> str:
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(timeout=90_000))  # ms
    for attempt in range(retries):
        try:
            res = client.models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"))
            return res.text
        except Exception as error:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            wait = 20 * (attempt + 1)
            log(f"judge failed ({type(error).__name__}: {str(error)[:100]}); retry in {wait}s")
            time.sleep(wait)


def judge_one(q: dict, a: dict) -> dict:
    evidence = "\n\n".join(t["output"] for t in a["tool_trace"] if t["tool"] == "search")[:14000] or "(nothing retrieved)"
    prompt = JUDGE_PROMPT.format(question=q["question"], reference=q["reference_answer"],
                                 answer=a["answer"], evidence=evidence)
    text = call_judge(prompt)
    match = re.search(r"\{.*\}", text, re.S)
    data = json.loads(match.group(0)) if match else {}
    return {"correct": int(bool(int(data.get("correct", 0)))), "supported": int(bool(int(data.get("supported", 0)))),
            "reason": str(data.get("reason", ""))[:300]}


def judge_stage(questions: list[dict], answers: dict) -> dict:
    judged = load_json(JUDGE_JSON, {})
    for n, q in enumerate(questions, 1):
        a = answers.get(q["id"])
        if not a:
            continue
        digest = hashlib.sha1((a["answer"] + json.dumps(a["tool_trace"], ensure_ascii=False)).encode()).hexdigest()[:12]
        if judged.get(q["id"], {}).get("digest") == digest:
            continue
        log(f"judge: {q['id']} ({n}/{len(questions)})")
        try:
            judged[q["id"]] = {**judge_one(q, a), "digest": digest}
        except Exception as error:  # noqa: BLE001
            log(f"judge could not grade {q['id']}: {type(error).__name__}: {str(error)[:120]}")
            continue
        save_json(JUDGE_JSON, judged)
        time.sleep(3)
    return judged


# --------------------------------------------------- agreement with my labels

def read_human_labels() -> dict:
    labels = {}
    if HUMAN_LABELS.is_file():
        with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                i = (row.get("id") or "").strip()
                c, s = (row.get("correct") or "").strip(), (row.get("supported") or "").strip()
                if i and c in ("0", "1") and s in ("0", "1"):
                    labels[i] = {"correct": int(c), "supported": int(s), "notes": row.get("notes", "")}
    return labels


def agreement(judged: dict, human: dict) -> dict:
    ids = [i for i in human if i in judged]
    out = {"n": len(ids), "disagreements": []}
    if not ids:
        return out
    for field in ("correct", "supported"):
        same = [i for i in ids if human[i][field] == judged[i][field]]
        out[f"{field}_agreement"] = round(len(same) / len(ids), 3)
        out["disagreements"] += [{"id": i, "field": field, "human": human[i][field], "judge": judged[i][field],
                                  "judge_reason": judged[i]["reason"]} for i in ids if i not in same]
    out["both_agreement"] = round(sum(1 for i in ids if all(human[i][f] == judged[i][f]
                                                              for f in ("correct", "supported"))) / len(ids), 3)
    return out


# ------------------------------------------------------- summary, failures

def classify(q: dict, a: dict, correct: int, supported: int, checks: dict) -> str:
    """Automatic first guess at the cause of a failure ('' = no failure). A human decides 'bad test question'."""
    if q["kind"] == "unanswerable":
        return "" if (a["refused"] and correct and supported and checks["no_error"]) else \
            ("error" if a["error"] else "unsupported claim (should have refused)")
    if a["error"]:
        return "error"
    if a["refused"]:
        return "retrieval miss" if not checks["expected_retrieved"] else "wrong refusal"
    if not supported:
        return "unsupported claim"
    if not correct:
        return "retrieval miss" if not checks["expected_retrieved"] else "wrong answer from right passage"
    return ""


def report_stage(questions: list[dict], answers: dict, judged: dict) -> None:
    human = read_human_labels()
    agree = agreement(judged, human)
    rows, causes, totals = [], Counter(), Counter()
    flags = Counter()
    for q in questions:
        a, j = answers.get(q["id"]), judged.get(q["id"])
        if not a or not j:
            continue
        checks = code_checks(q, a)
        for name, ok in checks.items():
            if name != "guard" and not ok:
                flags[name] += 1
        if a["guard"]:
            flags[f"guard_{a['guard']}"] += 1
        h = human.get(q["id"])
        source = "human" if h else "judge"
        correct, supported = (h or j)["correct"], (h or j)["supported"]
        answerable = q["kind"] != "unanswerable"
        totals["answerable" if answerable else "unanswerable"] += 1
        totals["judge_correct"] += j["correct"]
        totals["judge_unsupported"] += 1 - j["supported"]
        totals["refused_correctly" if (not answerable and a["refused"]) else
               "refused_wrongly" if (answerable and a["refused"]) else "answered"] += 1
        cause = classify(q, a, correct, supported, checks)
        if cause:
            causes[cause] += 1
            rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"], "auto_cause": cause,
                         "verdict_from": source, "correct": correct, "supported": supported,
                         "failed_code_checks": ", ".join(k for k, v in checks.items() if k != "guard" and not v),
                         "answer": a["answer"][:300].replace("\n", " "), "human_cause": "", "fix": ""})
    write_csv(FAILURES_CSV, ["id", "kind", "question", "auto_cause", "verdict_from", "correct", "supported",
                             "failed_code_checks", "answer", "human_cause", "fix"], rows)

    graded = [answers[q["id"]] for q in questions if q["id"] in answers]
    n = max(len(graded), 1)
    avg = lambda key: sum(a[key] for a in graded) / n  # noqa: E731
    tin, tout = avg("input_tokens"), avg("output_tokens")
    cost = (tin * PRICE_IN_PER_M + tout * PRICE_OUT_PER_M) / 1e6
    try:
        from agent import AGENT_MODEL
    except Exception:  # noqa: BLE001
        AGENT_MODEL = "?"
    summary = {
        "agent_model": AGENT_MODEL, "judge_model": JUDGE_MODEL, "questions": len(graded),
        "answerable": totals["answerable"], "unanswerable": totals["unanswerable"],
        "judge_correct": totals["judge_correct"], "judge_unsupported": totals["judge_unsupported"],
        "correct_refusals": totals["refused_correctly"], "wrong_refusals": totals["refused_wrongly"],
        "code_check_failures": dict(flags), "failure_causes_auto": dict(causes),
        "avg_model_calls": round(avg("model_calls"), 2), "avg_tool_calls": round(sum(len(a["tool_trace"]) for a in graded) / n, 2),
        "avg_input_tokens": round(tin), "avg_output_tokens": round(tout), "avg_seconds": round(avg("seconds"), 2),
        "cost_per_question_usd": round(cost, 6) if (PRICE_IN_PER_M or PRICE_OUT_PER_M) else "set PRICE_IN_PER_M / PRICE_OUT_PER_M",
        "agreement_with_human_labels": agree,
    }
    save_json(SUMMARY_JSON, summary)

    lines = [f"# Evaluation summary ({len(graded)} questions: {totals['answerable']} answerable, "
             f"{totals['unanswerable']} unanswerable)", "",
             f"- Agent `{AGENT_MODEL}`, judge `{JUDGE_MODEL}`",
             f"- Judge: correct {totals['judge_correct']}/{len(graded)}, with unsupported claims {totals['judge_unsupported']}",
             f"- Correct refusals {totals['refused_correctly']}/{totals['unanswerable']}; "
             f"wrong refusals {totals['refused_wrongly']}/{totals['answerable']}",
             f"- Code-check failures: {dict(flags) or 'none'}",
             f"- Failures by (automatic) cause: {dict(causes) or 'none'}",
             f"- Per question: {summary['avg_model_calls']} model calls, {summary['avg_tool_calls']} tool calls, "
             f"{summary['avg_input_tokens']} input + {summary['avg_output_tokens']} output tokens, "
             f"{summary['avg_seconds']} s; cost {summary['cost_per_question_usd']}"]
    if agree["n"]:
        lines.append(f"- Agreement judge vs my labels on {agree['n']} answers: correct {agree['correct_agreement']:.0%}, "
                     f"supported {agree['supported_agreement']:.0%}, both {agree['both_agreement']:.0%}")
    else:
        lines.append("- Agreement with my labels: not computed (eval/human_labels.csv has no graded rows)")
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n" + "\n".join(lines))
    if len(human) < 20:
        print(f"\nNOTE: only {len(human)} graded rows in eval/human_labels.csv; the brief asks for 20+.")
    if agree["disagreements"]:
        print("\nWhere the judge and I disagree (check each by hand, for the report):")
        for d in agree["disagreements"]:
            print(f"  {d['id']} {d['field']}: me={d['human']} judge={d['judge']}  ({d['judge_reason']})")
    print(f"\nFailures to classify (add human_cause, fix): eval/{FAILURES_CSV.name} ({len(rows)} rows)")


# -------------------------------------------------------------------- demo

def demo(keep: bool = False) -> None:
    """add_document before/after: the unanswerable question q27 and RD 1312/2024."""
    from agent import ask_user_approval, deny_all, run

    async def always_yes(path: str) -> bool:
        return True

    question = next(q for q in read_questions() if q["id"] == DEMO_ID)["question"]
    path = ix.download_corpus(include_held_back=True)[DEMO_SOURCE]
    rel = path.relative_to(ROOT).as_posix()
    col = ix.get_collection(ix.DEFAULT_DESIGN)
    if col.get(where={"source": DEMO_SOURCE}, include=[])["ids"]:
        log(f"{DEMO_SOURCE} is already indexed: the 'before' answer would not be a before. "
            f"Remove it first (col.delete) or rerun with a clean index.")
        return
    before_count = col.count()

    def show(title: str, r) -> None:
        print(f"\n=== {title} ===\n{r.answer}\ncitations: {r.citations}  retrieved: {len(r.retrieved)} passages  "
              f"guard: {r.guard or '-'}")

    before = run([question], approve=deny_all)[0]
    show("BEFORE adding the document", before)

    print(f"\nNow the agent will ask to add {rel}. Answer y to approve.")
    added = run([f"Añade al índice este documento: {rel}"], approve=ask_user_approval)[0]
    show("ADDING (the approval prompt is the guardrail)", added)
    after_count = col.count()

    after = run([question], approve=deny_all)[0]
    show("AFTER adding the document", after)

    again = run([f"Añade al índice este documento: {rel}"], approve=always_yes)[0]
    show("ADDING IT A SECOND TIME (already indexed)", again)

    save_json(DEMO_JSON, {"question": question, "document": rel, "chunks_before": before_count,
                          "chunks_after": after_count, "before": before.to_dict(), "add": added.to_dict(),
                          "after": after.to_dict(), "add_again": again.to_dict()})
    print(f"\nindex chunks: {before_count} -> {after_count}. Saved eval/{DEMO_JSON.name}")
    if keep:
        print(f"--keep: {DEMO_SOURCE} stays in the index.")
    else:
        col.delete(where={"source": DEMO_SOURCE})
        print(f"Removed {DEMO_SOURCE} from the index again so that `main.py evaluate` stays reproducible "
              f"({col.count()} chunks).")


# -------------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stage", choices=["all", "retrieval", "answers", "judge"], default="all")
    parser.add_argument("--rerun", action="store_true", help="answer every question again, not only the missing ones")
    parser.add_argument("--demo", action="store_true", help="add_document before/after demo")
    parser.add_argument("--keep", action="store_true", help="with --demo: leave the added document in the index")
    args = parser.parse_args()
    if args.demo:
        demo(args.keep)
        return

    questions = read_questions()
    EVAL.mkdir(exist_ok=True)
    if args.stage in ("all", "retrieval"):
        retrieval_stage(questions)
    answers = load_json(ANSWERS, {})
    if args.stage in ("all", "answers"):
        answers = answers_stage(questions, args.rerun)
        print(f"\nAnswers saved in eval/{ANSWERS.name}; to grade by hand, open "
              f"eval/{GRADING_CSV.name} and fill eval/human_labels.csv BEFORE reading the judge.")
    if args.stage in ("all", "judge"):
        if not answers:
            raise SystemExit("No answers yet: run `uv run python evaluate.py --stage answers` first.")
        judged = judge_stage(questions, answers)
        report_stage(questions, answers, judged)


if __name__ == "__main__":
    main()
