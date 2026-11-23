"""
Assignment 3: evaluation (run with `main.py evaluate`).

It goes through 7 steps. Every step saves its results in eval/, so if
something crashes I can run it again and it carries on where it stopped.

  1. Retrieval   checks if search finds the right article: hit rate at k = 1, 3 and 5,
                 for both chunking designs, plus how many words end up in the prompt
                 -> eval/retrieval_results.csv, eval/retrieval_detail.csv
  2. Agent       runs the agent on every question in eval/questions.csv
                 -> eval/answers.csv, eval/evidence.json
  3. Code checks the things code can check by itself: are the citations real,
                 was the right article retrieved and cited, did it refuse when it should
                 -> eval/code_checks.csv
  4. Grading     makes eval/grading_sheet.md, which I read to grade 20+ answers by hand.
                 It has no judge verdicts in it, so they can't influence me.
                 I write my grades in eval/human_labels.csv
  5. Judge       an LLM judge grades the answers with a rubric and the retrieved text.
                 It only runs after human_labels.csv has MIN_HUMAN grades, so it can't
                 affect my grades. Then it compares itself with me
                 -> eval/judge_verdicts.csv, eval/judge_disagreements.csv
  6. Summary     writes eval/summary.md and eval/failures.csv. The failure causes are
                 only suggestions, I check them by hand
  7. Demo        adds a document that answers one of the unanswerable questions and
                 shows the answer before and after. It uses a temporary COPY of the
                 index, so the real one doesn't change -> eval/add_document_demo.md

Flags: --redo (throw away the saved answers and verdicts), --skip-demo, --force-demo.
"""


from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

import agent
import index
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
KS = (1, 3, 5)
MIN_HUMAN = 20
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.1-flash-lite")

RUBRIC = """\
correct (1 or 0): is the answer right when compared with the REFERENCE ANSWER?
  - 1 if it states the key facts of the reference (the numbers, durations, amounts, dates and
    conditions that the question depends on) and does not contradict it.
  - Omitting a minor secondary detail is fine. For long lists, covering the main items is enough,
    but a wrong or invented item makes it 0. Missing a key number, deadline or condition is 0.
  - For a question needing two passages, both parts must be present.
  - For a question the corpus cannot answer: 1 only if the answer clearly says the indexed documents
    do not cover it and presents no substantive answer as fact; 0 if it answers anyway.
  - If the answer refuses although the reference gives an answer: 0.
supported (1 or 0): is EVERY factual claim in the answer found in the RETRIEVED PASSAGES?
  - Paraphrase is fine. A claim that is true but appears nowhere in the passages counts as
    unsupported (0). A proper refusal counts as supported (1).
"""

JUDGE_PROMPT = """You are a strict grader for a question-answering system over EU regulations.

RUBRIC
{rubric}
QUESTION
{question}

REFERENCE ANSWER (what a correct answer says; for unanswerable questions, what the assistant should say)
{reference}

ANSWER TO GRADE
{answer}

RETRIEVED PASSAGES (the only evidence the assistant had)
{evidence}

Reply with ONLY a JSON object: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}}"""

ANSWER_FIELDS = ["id", "kind", "question", "answer", "refused", "guardrail", "withheld_answer", "retrieved",
                 "search_queries", "tool_calls", "input_tokens", "output_tokens", "seconds", "error"]
CITED = re.compile(r"(GDPR|Data Act|Data Governance Act),\s*Article\s+(\d+)")


# --------------------------------------------------------------------------- small helpers

def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locs = [s.strip() for s in q["expected_location"].split(";") if s.strip()]
    return list(zip(sources, locs))


def parse_pairs(text: str) -> set[tuple[str, str]]:
    """'GDPR, Article 33; Data Act, Article 5' -> {('GDPR','Article 33'), ...}"""
    return {(s, f"Article {n}") for s, n in CITED.findall(text or "")}


def log(*a) -> None:
    print(*a, flush=True)


# --------------------------------------------------------------------------- 1. retrieval

def covered_pairs(metas: list[dict]) -> set[tuple[str, str]]:
    out = set()
    for m in metas:
        for loc in (m.get("locations") or m["location"]).split("; "):
            out.add((m["source"], loc))
    return out


def retrieval_stage(questions: list[dict]) -> str:
    log("\n== 1. Retrieval: hit rate at k ==")
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    vectors = {q["id"]: index.embed_query(q["question"]) for q in answerable}
    rows, detail = [], []
    for design in index.DESIGNS:
        col = index.open_collection(design)
        per = {}   # (kind, k) -> [hits, n]
        words = {k: [] for k in KS}
        for q in answerable:
            res = col.query(query_embeddings=[vectors[q["id"]]], n_results=max(KS))
            metas, docs = res["metadatas"][0], res["documents"][0]
            need = set(expected_pairs(q))
            first = next((r for r in range(1, len(metas) + 1) if need <= covered_pairs(metas[:r])), None)
            detail.append({"design": design, "id": q["id"], "kind": q["kind"], "first_hit_rank": first or ""})
            for k in KS:
                hit = first is not None and first <= k
                for key in ((q["kind"], k), ("all", k)):
                    h = per.setdefault(key, [0, 0])
                    h[0] += hit
                    h[1] += 1
                words[k].append(sum(len(d.split()) for d in docs[:k]))
        for (kind, k), (h, n) in sorted(per.items(), key=lambda x: (x[0][0], x[0][1])):
            rows.append({"design": design, "kind": kind, "k": k, "hit_rate": round(h / n, 3), "hits": h, "n": n,
                         "avg_words_added": round(sum(words[k]) / len(words[k])) if kind == "all" else ""})
    write_csv(EVAL / "retrieval_results.csv", rows, ["design", "kind", "k", "hit_rate", "hits", "n", "avg_words_added"])
    write_csv(EVAL / "retrieval_detail.csv", detail, ["design", "id", "kind", "first_hit_rank"])

    log(f"{'design':10s} {'kind':8s} " + " ".join(f"hit@{k:<3d}" for k in KS) + "  words in prompt (k=1/3/5)")
    scores = {}
    for design in index.DESIGNS:
        for kind in ("all", "single", "multi"):
            rs = {r["k"]: r for r in rows if r["design"] == design and r["kind"] == kind}
            w = " / ".join(str(next(r["avg_words_added"] for r in rows if r["design"] == design and r["kind"] == "all" and r["k"] == k)) for k in KS) if kind == "all" else ""
            log(f"{design:10s} {kind:8s} " + " ".join(f"{rs[k]['hit_rate']:<6.3f}" for k in KS) + f"  {w}")
        a = {r["k"]: r["hit_rate"] for r in rows if r["design"] == design and r["kind"] == "all"}
        scores[design] = (a[3], a[5], -next(r["avg_words_added"] for r in rows if r["design"] == design and r["kind"] == "all" and r["k"] == 5))
    best = max(scores, key=scores.get)
    log(f"Best by hit@3, then hit@5, then fewer words: '{best}'.  index.CHOSEN_DESIGN is '{index.CHOSEN_DESIGN}'.")
    if best != index.CHOSEN_DESIGN:
        log("  -> If you choose by these numbers, set CHOSEN_DESIGN in index.py to the winner and rerun with --redo.")
    return best


# --------------------------------------------------------------------------- 2. agent run

def config_fingerprint() -> dict:
    rules = hashlib.sha1((ROOT / "AGENTS.md").read_bytes()).hexdigest()[:10]
    return {"design": index.CHOSEN_DESIGN, "model": agent.MODEL, "agents_md": rules}


def agent_stage(questions: list[dict], redo: bool) -> list[dict]:
    log("\n== 2. Agent answers ==")
    answers_path, meta_path, ev_path = EVAL / "answers.csv", EVAL / "answers_meta.json", EVAL / "evidence.json"
    fp = config_fingerprint()
    old = json.loads(meta_path.read_text()) if meta_path.exists() else None
    if redo or (old and old != fp):
        if old and old != fp:
            log(f"Cached answers were made with {old}; now {fp}. Re-running all questions.\n"
                f"  (Your human_labels.csv refer to the OLD answers: regrade if you keep the new ones.)")
        for p in (answers_path, ev_path, EVAL / "judge_verdicts.csv"):
            p.unlink(missing_ok=True)
    meta_path.write_text(json.dumps(fp))
    rows = {r["id"]: r for r in read_csv(answers_path) if not r.get("error")}
    evidence = json.loads(ev_path.read_text()) if ev_path.exists() else {}

    for q in questions:
        if q["id"] in rows:
            continue
        result, error = None, ""
        for attempt in range(3):
            try:
                result = agent.ask(q["question"], approve=lambda path: False)   # never add documents while evaluating
                error = ""
                break
            except Exception as e:  # noqa: BLE001
                error = f"{type(e).__name__}: {str(e)[:200]}"
                log(f"  {q['id']} attempt {attempt + 1} failed: {error}")
                time.sleep(20 * (attempt + 1))
        if result is None:
            rows[q["id"]] = {"id": q["id"], "kind": q["kind"], "question": q["question"], "error": error}
        else:
            searches = [s for s in result["tool_trace"] if s["tool"] == "search"]
            rows[q["id"]] = {
                "id": q["id"], "kind": q["kind"], "question": q["question"], "answer": result["answer"],
                "refused": int(result["refused"]), "guardrail": result["guardrail"] or "",
                "withheld_answer": result["withheld_answer"] or "",
                "retrieved": "; ".join(dict.fromkeys(result["retrieved"])),
                "search_queries": " | ".join(str(s["args"].get("query", "")) for s in searches),
                "tool_calls": len(result["tool_trace"]), "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"], "seconds": result["seconds"], "error": "",
            }
            evidence[q["id"]] = "\n\n---\n\n".join(s["result"] for s in searches)
            log(f"  {q['id']} [{q['kind']}] {'REFUSED' if result['refused'] else 'answered'} "
                f"{result['seconds']}s  guardrail={result['guardrail'] or '-'}")
        ordered = [rows[x["id"]] for x in questions if x["id"] in rows]
        write_csv(answers_path, ordered, ANSWER_FIELDS)
        ev_path.write_text(json.dumps(evidence, indent=1))
    failed = [r["id"] for r in rows.values() if r.get("error")]
    if failed:
        log(f"  {len(failed)} questions failed after retries ({', '.join(failed)}): run again to retry them.")
    return [rows[q["id"]] for q in questions if q["id"] in rows]


# --------------------------------------------------------------------------- 3. code checks

def code_check(q: dict, row: dict) -> dict:
    answer = row.get("answer", "") or ""
    refused = bool(int(row.get("refused") or 0))
    retrieved = parse_pairs(row.get("retrieved", ""))
    cited = {(s, f"Article {n}") for s, n in CITED.findall(answer)}
    need = set(expected_pairs(q))
    answerable = q["kind"] != "unanswerable"
    return {
        "id": q["id"], "kind": q["kind"], "refused": int(refused),
        "refusal_ok": int(refused != answerable),                      # refuse iff unanswerable
        "n_cited": len(cited),
        "citations_valid": int(refused or (bool(cited) and cited <= retrieved)),
        "expected_retrieved": int(need <= retrieved) if answerable else "",
        "expected_cited": int(need <= cited) if answerable else "",
        "guardrail_fired": int(bool(row.get("guardrail"))),
    }


def code_stage(questions: list[dict], rows: list[dict]) -> list[dict]:
    log("\n== 3. Code checks ==")
    by_id = {r["id"]: r for r in rows}
    checks = [code_check(q, by_id[q["id"]]) for q in questions if q["id"] in by_id and not by_id[q["id"]].get("error")]
    write_csv(EVAL / "code_checks.csv", checks, list(checks[0]))
    ans = [c for c in checks if c["kind"] != "unanswerable"]
    una = [c for c in checks if c["kind"] == "unanswerable"]
    log(f"  valid citations (answers that cite): {sum(c['citations_valid'] for c in checks)}/{len(checks)}")
    log(f"  expected article retrieved: {sum(c['expected_retrieved'] for c in ans)}/{len(ans)}   "
        f"expected article cited: {sum(c['expected_cited'] for c in ans)}/{len(ans)}")
    log(f"  correct refusals (unanswerable): {sum(c['refused'] for c in una)}/{len(una)}   "
        f"wrong refusals (answerable): {sum(c['refused'] for c in ans)}/{len(ans)}")
    log(f"  citation guard fired: {sum(c['guardrail_fired'] for c in checks)} times")
    return checks


# --------------------------------------------------------------------------- 4. grading sheet

def grading_sheet(questions: list[dict], rows: list[dict]) -> None:
    by_id = {r["id"]: r for r in rows}
    evidence = json.loads((EVAL / "evidence.json").read_text()) if (EVAL / "evidence.json").exists() else {}
    out = ["# Grading sheet\n",
           "Grade at least 20 answers in `eval/human_labels.csv` (columns id, correct, supported, notes) "
           "BEFORE the judge runs.\n",
           "- **correct** = 1 if the answer is right against the reference (or a proper refusal for an unanswerable question).\n"
           "- **supported** = 1 if every claim in the answer is in the retrieved passages shown here.\n"]
    for q in questions:
        r = by_id.get(q["id"])
        if not r or r.get("error"):
            continue
        out.append(f"\n---\n\n## {q['id']} ({q['kind']})\n\n**Question:** {q['question']}\n\n"
                   f"**Reference answer:** {q['reference_answer']}\n\n**Agent answer:**\n\n{r['answer']}\n\n"
                   f"<details><summary>Retrieved passages</summary>\n\n```\n{evidence.get(q['id'], '')}\n```\n</details>\n")
    (EVAL / "grading_sheet.md").write_text("\n".join(out), encoding="utf-8")


def human_labels() -> list[dict]:
    return [r for r in read_csv(EVAL / "human_labels.csv")
            if (r.get("correct") or "").strip() in ("0", "1") and (r.get("supported") or "").strip() in ("0", "1")]


# --------------------------------------------------------------------------- 5. judge

def parse_verdict(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        data = json.loads(m.group(0))
        return {"correct": int(data["correct"]), "supported": int(data["supported"]),
                "reason": str(data.get("reason", ""))[:300]}
    except (ValueError, KeyError, TypeError):
        return None


def judge_stage(questions: list[dict], rows: list[dict]) -> list[dict]:
    log("\n== 5. Judge ==")
    labels = human_labels()
    if len(labels) < MIN_HUMAN:
        log(f"  Skipped: eval/human_labels.csv has {len(labels)} graded answers, need {MIN_HUMAN}.\n"
            f"  Grade from eval/grading_sheet.md first (the judge must not influence your grades), then rerun.")
        return []
    from langchain_google_genai import ChatGoogleGenerativeAI
    load_api_key()
    llm = ChatGoogleGenerativeAI(model=JUDGE_MODEL)
    evidence = json.loads((EVAL / "evidence.json").read_text())
    path = EVAL / "judge_verdicts.csv"
    done = {r["id"]: r for r in read_csv(path)}
    by_id = {r["id"]: r for r in rows}
    for q in questions:
        r = by_id.get(q["id"])
        if q["id"] in done or not r:
            continue
        if r.get("error") or not r.get("answer"):
            done[q["id"]] = {"id": q["id"], "correct": 0, "supported": 0, "reason": "no answer"}
            continue
        prompt = JUDGE_PROMPT.format(rubric=RUBRIC, question=q["question"], reference=q["reference_answer"],
                                     answer=r["answer"], evidence=evidence.get(q["id"]) or "(nothing retrieved)")
        verdict = None
        for attempt in range(4):
            try:
                verdict = parse_verdict(llm.invoke(prompt).text)
                if verdict:
                    break
            except Exception as e:  # noqa: BLE001
                log(f"  judge {q['id']} attempt {attempt + 1}: {type(e).__name__}: {str(e)[:120]}")
            time.sleep(10 * (attempt + 1))
        if not verdict:
            log(f"  judge could not grade {q['id']}; rerun to retry.")
            continue
        done[q["id"]] = {"id": q["id"], **verdict}
        write_csv(path, list(done.values()), ["id", "correct", "supported", "reason"])
        log(f"  {q['id']}: correct={verdict['correct']} supported={verdict['supported']}")
    write_csv(path, list(done.values()), ["id", "correct", "supported", "reason"])
    return list(done.values())


def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(v) / n) * (b.count(v) / n) for v in (0, 1))
    return None if math.isclose(pe, 1.0) else round((po - pe) / (1 - pe), 3)


def agreement(verdicts: list[dict]) -> dict | None:
    v = {r["id"]: r for r in verdicts}
    pairs = [(h, v[h["id"]]) for h in human_labels() if h["id"] in v]
    if not pairs:
        return None
    out = {"n": len(pairs)}
    for field in ("correct", "supported"):
        hs = [int(h[field]) for h, _ in pairs]
        js = [int(j[field]) for _, j in pairs]
        out[field] = {"agree": sum(x == y for x, y in zip(hs, js)), "kappa": kappa(hs, js)}
    out["both"] = sum(all(int(h[f]) == int(j[f]) for f in ("correct", "supported")) for h, j in pairs)
    rows = [{"id": h["id"], "field": f, "human": h[f], "judge": j[f], "human_notes": h.get("notes", ""),
             "judge_reason": j["reason"]} for h, j in pairs for f in ("correct", "supported") if int(h[f]) != int(j[f])]
    write_csv(EVAL / "judge_disagreements.csv", rows, ["id", "field", "human", "judge", "human_notes", "judge_reason"])
    return out


# --------------------------------------------------------------------------- 6. summary + failures

def suggest_cause(q: dict, row: dict, check: dict, verdict: dict | None) -> str:
    answerable = q["kind"] != "unanswerable"
    if not verdict:
        return ""
    if answerable and check["refused"]:
        return "wrong refusal" + (" (retrieval miss?)" if not check["expected_retrieved"] else "")
    if answerable and not check["expected_retrieved"]:
        return "retrieval miss"
    if not answerable and not check["refused"]:
        return "unsupported claim (should have refused)"
    if not int(verdict["supported"]):
        return "unsupported claim"
    if not int(verdict["correct"]):
        return "wrong answer from the right passage"
    return ""


def summary_stage(questions, rows, checks, verdicts, agree, best_design) -> None:
    log("\n== 6. Summary ==")
    by_id = {r["id"]: r for r in rows}
    chk = {c["id"]: c for c in checks}
    ver = {v["id"]: v for v in verdicts}
    ok_rows = [r for r in rows if not r.get("error")]
    n = len(ok_rows)
    lines = [f"# Evaluation summary\n",
             f"Agent model `{agent.MODEL}`, design `{index.CHOSEN_DESIGN}` (best by retrieval numbers: `{best_design}`), "
             f"judge `{JUDGE_MODEL}`. Questions answered: {n}/{len(questions)}.\n"]
    ans = [c for c in checks if c["kind"] != "unanswerable"]
    una = [c for c in checks if c["kind"] == "unanswerable"]
    lines += ["## Code checks\n",
              f"- Citations valid: {sum(c['citations_valid'] for c in checks)}/{len(checks)}",
              f"- Expected article retrieved: {sum(c['expected_retrieved'] for c in ans)}/{len(ans)}; cited: {sum(c['expected_cited'] for c in ans)}/{len(ans)}",
              f"- Correct refusals: {sum(c['refused'] for c in una)}/{len(una)}; wrong refusals: {sum(c['refused'] for c in ans)}/{len(ans)}",
              f"- Citation guard fired: {sum(c['guardrail_fired'] for c in checks)}\n"]
    if verdicts:
        lines.append("## Judge verdicts\n")
        for kind in ("single", "multi", "unanswerable", "all"):
            ids = [q["id"] for q in questions if (kind == "all" or q["kind"] == kind) and q["id"] in ver]
            if ids:
                c = sum(int(ver[i]["correct"]) for i in ids)
                s = sum(int(ver[i]["supported"]) for i in ids)
                lines.append(f"- {kind}: correct {c}/{len(ids)}, supported {s}/{len(ids)}")
        lines.append(f"- Unsupported answers: {sum(1 for v in verdicts if not int(v['supported']))}\n")
    if agree:
        lines += ["## Agreement with my grades\n",
                  f"- Graded by me: {agree['n']}",
                  f"- correct: {agree['correct']['agree']}/{agree['n']} agree (kappa {agree['correct']['kappa']})",
                  f"- supported: {agree['supported']['agree']}/{agree['n']} agree (kappa {agree['supported']['kappa']})",
                  f"- both fields agree: {agree['both']}/{agree['n']}  (disagreements: eval/judge_disagreements.csv)\n"]
    if n:
        lines += ["## Cost per question\n",
                  f"- Input tokens (avg): {sum(int(r['input_tokens']) for r in ok_rows) / n:.0f}; "
                  f"output tokens (avg): {sum(int(r['output_tokens']) for r in ok_rows) / n:.0f}",
                  f"- Seconds (avg): {sum(float(r['seconds']) for r in ok_rows) / n:.1f}; "
                  f"tool calls (avg): {sum(int(r['tool_calls']) for r in ok_rows) / n:.1f}\n"]
    (EVAL / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    log("\n".join(lines))

    fails = []
    mine = {r["id"]: r.get("my_cause", "") for r in read_csv(EVAL / "failures.csv")}   # keep causes I already wrote
    human = {h["id"]: h for h in human_labels()}
    for q in questions:
        c, r, v = chk.get(q["id"]), by_id.get(q["id"]), ver.get(q["id"])
        if not (c and r and v):
            continue
        h = human.get(q["id"])
        eff = {"correct": h["correct"], "supported": h["supported"]} if h else v   # my grade wins over the judge's
        bad = (not int(eff["correct"])) or (not int(eff["supported"])) or (not c["refusal_ok"]) \
            or (not int(v["correct"])) or (not int(v["supported"]))
        if bad:
            fails.append({"id": q["id"], "kind": q["kind"], "question": q["question"], "refused": c["refused"],
                          "expected_retrieved": c["expected_retrieved"],
                          "human_correct": h["correct"] if h else "", "human_supported": h["supported"] if h else "",
                          "human_notes": h.get("notes", "") if h else "",
                          "judge_correct": v["correct"], "judge_supported": v["supported"], "judge_reason": v["reason"],
                          "suggested_cause": suggest_cause(q, r, c, eff), "my_cause": mine.get(q["id"], "")})
    if verdicts:
        write_csv(EVAL / "failures.csv", fails, ["id", "kind", "question", "refused", "expected_retrieved",
                                                 "human_correct", "human_supported", "human_notes", "judge_correct",
                                                 "judge_supported", "judge_reason", "suggested_cause", "my_cause"])
        log(f"  {len(fails)} failed questions (by my grade or the judge's) -> eval/failures.csv. Confirm or change each "
            f"cause in `my_cause`: retrieval miss / wrong answer from the right passage / unsupported claim / "
            f"wrong refusal / bad test question.")


# --------------------------------------------------------------------------- 7. add-document demo

def demo_stage(questions: list[dict], force: bool) -> None:
    log("\n== 7. Add-document demo ==")
    out = EVAL / "add_document_demo.md"
    if out.exists() and not force:
        log("  eval/add_document_demo.md exists (use --force-demo to redo).")
        return
    q = next((x for x in questions if x["kind"] == "unanswerable" and "own territory" in x["question"]), None) \
        or next(x for x in questions if x["kind"] == "unanswerable")
    path = Path(index.download("free_flow", index.EXTRA["free_flow"][1])).resolve()
    shown = path.relative_to(ROOT) if ROOT in path.parents else path
    asked = []
    tmp = Path(tempfile.mkdtemp(prefix="index_copy_"))
    shutil.copytree(index.INDEX_DIR, tmp / "index")
    os.environ["CORPUS_INDEX_DIR"] = str(tmp / "index")           # the server started by the agent reads this
    try:
        before = agent.ask(q["question"], approve=lambda p: False)
        def approve(p):
            asked.append(p)
            return True
        added = agent.ask(f"Please add the document {shown} to the index.", approve=approve)
        after = agent.ask(q["question"], approve=lambda p: False)
    finally:
        os.environ.pop("CORPUS_INDEX_DIR", None)
        shutil.rmtree(tmp, ignore_errors=True)
    md = [f"# Add-document demo\n", f"Question ({q['id']}): **{q['question']}**\n",
          f"Document added: `{path.name}` ({index.EXTRA['free_flow'][0]}), on a temporary copy of the index.\n",
          f"## Before\n\n{before['answer']}\n\nRetrieved: {'; '.join(dict.fromkeys(before['retrieved']))}\n",
          f"## Adding it (approval asked for: {asked or 'nothing'})\n\n{added['answer']}\n",
          f"Tool calls: {[(s['tool'], s['args']) for s in added['tool_trace']]}\n",
          f"## After\n\n{after['answer']}\n\nRetrieved: {'; '.join(dict.fromkeys(after['retrieved']))}\n"]
    out.write_text("\n".join(md), encoding="utf-8")
    log("\n".join(md))


# --------------------------------------------------------------------------- main

def main() -> None:
    EVAL.mkdir(exist_ok=True)
    questions = read_csv(EVAL / "questions.csv")
    if not questions:
        raise SystemExit("eval/questions.csv is empty.")
    redo = "--redo" in sys.argv
    best = retrieval_stage(questions)
    rows = agent_stage(questions, redo)
    checks = code_stage(questions, rows)
    grading_sheet(questions, rows)
    verdicts = judge_stage(questions, rows)
    agree = agreement(verdicts) if verdicts else None
    summary_stage(questions, rows, checks, verdicts, agree, best)
    if "--skip-demo" not in sys.argv:
        demo_stage(questions, "--force-demo" in sys.argv)


if __name__ == "__main__":
    main()
