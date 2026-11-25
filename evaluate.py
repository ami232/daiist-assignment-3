"""
Assignment 3: evaluation (`main.py evaluate`).

  1. Retrieval: hit rate at k = 1, 3, 5 for each design in index/, and the words
     the top-k chunks add to the prompt. Each question is embedded once (cached).
     A hit means a retrieved chunk covers an expected location (see testset.py).
  2. End to end: the agent answers every question (design index.CHOSEN_DESIGN;
     add_document is refused, as nobody is there to approve it). It runs
     "patient": one model, waiting out per-minute rate limits. Answers are
     cached in eval/answers.jsonl and re-run only when the question, AGENTS.md,
     the model or the agent's settings change, so a run stopped by the daily
     quota carries on where it left off.
  3. Code checks: refusals (agent.REFUSAL), valid citations, whether the
     agent's own searches found the expected passage, and guardrail firings.
  4. LLM judge: your rubric (eval/judge_rubric.md) with the question, the
     reference answer and the retrieved text as evidence -> correct, supported,
     reason. Verdicts are cached in eval/judge.jsonl.
  5. Agreement between the judge and your own grades in eval/human_labels.csv.
  6. Results: correct, unsupported, correct refusals, wrong refusals; cost and
     latency per question; and eval/failures.csv for you to classify.

Writes to eval/: retrieval.csv, answers.jsonl, answers_for_grading.md,
judge.jsonl, results.csv, failures.csv, summary.md.

    uv run python main.py evaluate                    # everything
    uv run python evaluate.py --retrieval-only        # hit rates only (cheap)
    uv run python evaluate.py --answers-only          # answers to grade, no judge yet
    uv run python evaluate.py --fresh                 # ignore cached answers and verdicts
    uv run python evaluate.py --demo q05 page.html    # add a document: answer before/after
"""

import argparse
import asyncio
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import agent as ag
import index as ix
import server
import testset as ts

EVAL = ix.ROOT / "eval"
RUBRIC = EVAL / "judge_rubric.md"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "judge.jsonl"
K_VALUES = (1, 3, 5)
# A different model from the agent's, so the judge isn't grading its own answers
# (and it uses a separate free daily quota). JUDGE_MODEL overrides it.
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.1-flash-lite")
GOOD = ("correct", "correct refusal")


class DailyQuota(RuntimeError):
    """No quota left for today (or none at all for this model): stop the run."""


def kind(row: dict) -> str:
    return row["kind"].strip().lower()


def sha(*parts) -> str:
    return hashlib.sha256("\x1f".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:16]


def is_daily_quota(error: Exception) -> bool:
    """Daily quota used up, or no free quota at all for the model ("limit: 0")."""
    return isinstance(error, ix.QuotaExhausted) or ag.out_of_quota(error)


def short_error(text: str) -> str:
    """A Gemini error in a few words (see agent.reason); anything else, its first line."""
    known = ag.reason(RuntimeError(text))
    return text.strip().splitlines()[0][:150] if known.startswith("RuntimeError: ") else known


def stop_message(error: Exception, saved: str, what: str = "") -> str:
    then = ("choose another model (`uv run python agent.py --test-models`), then run the same command again"
            if "limit: 0" in str(error) else "run the same command again after the reset to carry on")
    return f"  Stopped: {what}{ag.reason(error)}. The {saved} so far are saved; {then}."


def read_jsonl(path: Path) -> dict[str, dict]:
    """The latest record per key."""
    records = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
                records[record["key"]] = record
            except (ValueError, KeyError):
                continue
    return records


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def compact_jsonl(path: Path, keep: set[str]) -> None:
    """Drop records no current question uses, so the committed file stays small."""
    records = read_jsonl(path)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for k, r in records.items() if k in keep),
                    encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


# ==========================================================================
# Expected passages and hits
# ==========================================================================
_resolved = {}


def expected(row: dict) -> list[list[tuple[str, tuple | None]]]:
    """Per needed passage, its alternatives as (source, resolved location)."""
    parts = []
    for alternatives in ts.expected_parts(row):
        resolved = []
        for source, location in alternatives:
            if (source, location) not in _resolved:
                _resolved[(source, location)] = ts.resolve_location(source, location)
            resolved.append((source, _resolved[(source, location)]))
        parts.append(resolved)
    return parts


def covers(parts, chunks: list[dict], question_kind: str) -> bool:
    """single: any expected place is among the chunks; multi: every needed passage is."""
    found = [any(ts.chunk_matches(c, source, res) for c in chunks for source, res in alts) for alts in parts]
    return bool(found) and (any(found) if question_kind == "single" else all(found))


def first_hit(parts, ranked: list[dict], question_kind: str) -> int | None:
    for k in range(1, len(ranked) + 1):
        if covers(parts, ranked[:k], question_kind):
            return k
    return None


# ==========================================================================
# 1. Retrieval
# ==========================================================================
def retrieval(rows: list[dict]) -> tuple[list[dict], dict]:
    answerable = [r for r in rows if kind(r) != "unanswerable"]
    per_question, summary = [], {}
    for design in ix.DESIGNS:
        if ix.collection(design).count() == 0:
            print(f"  design {design!r} is not in index/; skipped")
            continue
        ranks = {}
        for r in answerable:
            hits = ix.search(r["question"], k=max(K_VALUES), design=design, where={"origin": "corpus"})
            rank = first_hit(expected(r), hits, kind(r))
            ranks[r["id"]] = (kind(r), rank, [sum(h["words"] for h in hits[:k]) for k in K_VALUES])
            per_question.append({"id": r["id"], "kind": kind(r), "design": design, "hit_rank": rank or "",
                                 **{f"words_top{k}": w for k, w in zip(K_VALUES, ranks[r["id"]][2])},
                                 "top5": " ; ".join(f"[{h['source']}, {h['location']}]" for h in hits)})
        if not ranks:
            continue
        table = {}
        for subset in ("all", "single", "multi"):
            chosen = [v for v in ranks.values() if subset == "all" or v[0] == subset]
            if chosen:
                table[subset] = {"n": len(chosen),
                                 **{f"hit@{k}": sum(1 for _, rank, _ in chosen if rank and rank <= k) / len(chosen)
                                    for k in K_VALUES}}
        table["words"] = {f"top{k}": sum(v[2][i] for v in ranks.values()) / max(len(ranks), 1)
                          for i, k in enumerate(K_VALUES)}
        summary[design] = table
        print(f"  design {design!r}: hit@1 {table['all']['hit@1']:.0%}, hit@3 {table['all']['hit@3']:.0%}, "
              f"hit@5 {table['all']['hit@5']:.0%} over {table['all']['n']} answerable questions")
    return per_question, summary


# ==========================================================================
# 2. End to end: the agent's answers
# ==========================================================================
def agent_key(question: str) -> str:
    agents_md = ag.AGENTS_MD.read_text(encoding="utf-8") if ag.AGENTS_MD.is_file() else ""
    return sha(question.strip(), agents_md, ag.MODEL, ag.REFUSAL, ag.BLOCK_UNCITED, ag.MAX_TOOL_CALLS,
               ag.MAX_MODEL_CALLS, ix.CHOSEN_DESIGN, server.TOP_K)


async def answer_all(rows: list[dict], fresh: bool, model=None) -> tuple[dict[str, dict], bool]:
    """Answers by question id, and whether every question got one."""
    cache = {} if fresh else read_jsonl(ANSWERS)
    answers, todo = {}, []
    for r in rows:
        key = agent_key(r["question"])
        if key in cache and not cache[key].get("error"):
            answers[r["id"]] = cache[key]
        else:
            todo.append((r, key))
    print(f"  {len(answers)} cached, {len(todo)} to run with {ag.MODEL} "
          f"(rate limits are waited out, so a question can take a few minutes)")
    complete = True
    if todo:
        async with ag.CorpusAgent(model=model, interactive=False, patient=True) as agent:
            for n, (r, key) in enumerate(todo, start=1):
                print(f"  [{n}/{len(todo)}] {r['id']} ... ", end="", flush=True)
                try:
                    result = await agent.ask(r["question"])
                except Exception as error:  # noqa: BLE001 - record it and carry on, unless out of quota
                    if is_daily_quota(error):
                        print("\n" + stop_message(error, "answers"))
                        complete = False
                        break
                    result = {"question": r["question"], "error": f"{type(error).__name__}: {error}"}
                failed = result.get("tool_errors") or []
                if any(is_daily_quota(Exception(f)) for f in failed):
                    print("\n" + stop_message(Exception(failed[0]), "answers", "search (Gemini embeddings): "))
                    complete = False
                    break
                if failed and not result.get("retrieved") and not result.get("error"):
                    # Every search failed, so the answer says nothing about the documents: run it again later.
                    result["error"] = (failed[0] if failed[0].lower().startswith("search failed")
                                       else f"search failed: {failed[0]}")[:300]
                record = {"key": key, "id": r["id"], **result}
                append_jsonl(ANSWERS, record)
                answers[r["id"]] = record
                state = (f"error: {short_error(record['error'])}" if record.get("error")
                         else "refused" if record["refused"] else "answered")
                fired = " (citation check fired)" if record.get("guardrail") else ""
                print(f"{state}{fired}, {record.get('seconds', '?')} s")
    compact_jsonl(ANSWERS, {agent_key(r["question"]) for r in rows})
    return answers, complete and all(r["id"] in answers and not answers[r["id"]].get("error") for r in rows)


def chunk_texts(ids: list[str]) -> dict[str, str]:
    if not ids:
        return {}
    got = ix.collection(ix.CHOSEN_DESIGN).get(ids=ids, include=["documents"])
    return dict(zip(got["ids"], got["documents"]))


def evidence(answer: dict) -> str:
    chunks = answer.get("retrieved") or []
    texts = chunk_texts([c["id"] for c in chunks])
    return "\n\n".join(f"{c['label']}\n{texts.get(c['id'], '(text no longer in the index)')}" for c in chunks) \
        or "(the assistant retrieved nothing)"


def write_grading_sheet(rows: list[dict], answers: dict) -> None:
    lines = ["# Answers to grade", "",
             "Grade at least 20 of these in `eval/human_labels.csv` (columns: id, correct, supported, notes) "
             "**before** you look at `eval/judge.jsonl` or `eval/results.csv`.", "",
             "- `correct` = 1 if the answer is right against the reference answer (or a proper refusal).",
             "- `supported` = 1 if every claim in it is in the retrieved text shown under it.",
             "- `notes`: why, for every 0.", ""]
    for r in rows:
        a = answers.get(r["id"])
        if not a or a.get("error"):
            continue
        lines += [f"## {r['id']} ({kind(r)})", "", f"**Question:** {r['question']}", "",
                  f"**Reference answer:** {r['reference_answer']}", "", "**Agent's answer:**", "",
                  "> " + a["answer"].replace("\n", "\n> "), ""]
        if a.get("guardrail"):
            lines += [f"*The citation check replaced a draft that {a['guardrail']['reason']}.*", ""]
        lines += ["<details><summary>Retrieved text</summary>", "", evidence(a), "", "</details>", ""]
    (EVAL / "answers_for_grading.md").write_text("\n".join(lines), encoding="utf-8")


# ==========================================================================
# 4. LLM judge
# ==========================================================================
JUDGE_PROMPT = """{rubric}

---
Question ({kind}): {question}

Reference answer: {reference}

Retrieved text (the only evidence the assistant had):
{evidence}

Assistant's answer:
{answer}
---
Grade the assistant's answer with the rubric above. Give correct (1 or 0),
supported (1 or 0) and a one-sentence reason."""


def rubric_text() -> str:
    text = RUBRIC.read_text(encoding="utf-8") if RUBRIC.is_file() else ""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()


def gemini_judge():
    from pydantic import BaseModel, Field

    class Verdict(BaseModel):
        correct: int = Field(ge=0, le=1, description="1 if the answer is correct by the rubric, else 0")
        supported: int = Field(ge=0, le=1, description="1 if every claim is in the retrieved text, else 0")
        reason: str = Field(description="one sentence")

    return ag.gemini_model(JUDGE_MODEL, patient=True).with_structured_output(Verdict, include_raw=True)


def judge_one(judge, prompt: str) -> dict:
    """One verdict, waiting out per-minute limits."""
    import time
    for attempt in range(5):
        try:
            out = judge.invoke(prompt)
            break
        except Exception as error:  # noqa: BLE001
            if is_daily_quota(error):
                raise DailyQuota(str(error)) from error
            if attempt == 4 or not ag._retryable(error):
                raise
            time.sleep(min(60, 10 * 2 ** attempt))
    parsed, raw = out.get("parsed"), out.get("raw")
    usage = getattr(raw, "usage_metadata", None) or {}
    if parsed is None:
        return {"error": f"unparseable verdict: {getattr(raw, 'text', '')[:200]}"}
    return {"correct": int(parsed.correct), "supported": int(parsed.supported), "reason": parsed.reason,
            "input_tokens": usage.get("input_tokens", 0), "output_tokens": usage.get("output_tokens", 0)}


def judge_all(rows: list[dict], answers: dict, fresh: bool, judge=None) -> tuple[dict[str, dict], bool]:
    rubric = rubric_text()
    if not rubric:
        print("  No rubric yet: write it in eval/judge_rubric.md to run the judge.")
        return {}, False
    cache = {} if fresh else read_jsonl(VERDICTS)
    verdicts, keys, complete = {}, set(), True
    for r in rows:
        a = answers.get(r["id"])
        if not a or a.get("error"):
            continue
        key = sha(rubric, JUDGE_MODEL, r["question"], r["reference_answer"], a["answer"],
                  [c["id"] for c in a.get("retrieved") or []])
        keys.add(key)
        if key in cache and not cache[key].get("error"):
            verdicts[r["id"]] = cache[key]
            continue
        prompt = JUDGE_PROMPT.format(rubric=rubric, kind=kind(r), question=r["question"],
                                     reference=r["reference_answer"], evidence=evidence(a), answer=a["answer"])
        try:
            judge = judge or gemini_judge()
            verdict = judge_one(judge, prompt)
        except DailyQuota as error:
            print(stop_message(error, "verdicts"))
            complete = False
            break
        except Exception as error:  # noqa: BLE001
            verdict = {"error": f"{type(error).__name__}: {error}"}
        record = {"key": key, "id": r["id"], "model": JUDGE_MODEL, **verdict}
        append_jsonl(VERDICTS, record)
        verdicts[r["id"]] = record
        print(f"  judged {r['id']}: " + (record.get("error") or f"correct={record['correct']} supported={record['supported']}"))
    compact_jsonl(VERDICTS, keys)
    return verdicts, complete


# ==========================================================================
# 5. Agreement with your grades
# ==========================================================================
def human_labels() -> dict[str, dict]:
    if not HUMAN.is_file():
        return {}
    with HUMAN.open(newline="", encoding="utf-8-sig") as f:
        labels = {}
        for r in csv.DictReader(f):
            qid = (r.get("id") or "").strip()
            try:
                labels[qid] = {"correct": int(r["correct"]), "supported": int(r["supported"]),
                               "notes": r.get("notes", "")}
            except (KeyError, TypeError, ValueError):
                continue
        return labels


def agreement(labels: dict, verdicts: dict) -> dict:
    result = {}
    for field in ("correct", "supported"):
        pairs = [(labels[q][field], v[field]) for q, v in verdicts.items() if q in labels and "error" not in v]
        n = len(pairs)
        if not n:
            continue
        observed = sum(h == j for h, j in pairs) / n
        p_h, p_j = sum(h for h, _ in pairs) / n, sum(j for _, j in pairs) / n
        chance = p_h * p_j + (1 - p_h) * (1 - p_j)
        kappa = (observed - chance) / (1 - chance) if chance < 1 else 1.0
        result[field] = {"n": n, "agreement": observed, "kappa": kappa,
                         "disagree": [q for q, v in verdicts.items() if q in labels and "error" not in v
                                      and labels[q][field] != v[field]]}
    return result


# ==========================================================================
# 6. Results
# ==========================================================================
def outcome(question_kind: str, a: dict | None, v: dict | None) -> str:
    if not a or a.get("error"):
        return "error"
    if question_kind == "unanswerable":
        return "correct refusal" if a["refused"] else "answered (should refuse)"
    if a["refused"]:
        return "wrong refusal"
    if not v or v.get("error"):
        return "answered (not judged)"
    if not v["supported"]:
        return "unsupported"
    return "correct" if v["correct"] else "incorrect"


def results_table(rows, answers, verdicts, labels) -> list[dict]:
    table = []
    for r in rows:
        a, v, h = answers.get(r["id"]) or {}, verdicts.get(r["id"]) or {}, labels.get(r["id"]) or {}
        answerable = kind(r) != "unanswerable"
        cites = a.get("citations") or []
        expected_sources = {s for alts in ts.expected_parts(r) for s, _ in alts} if answerable else set()
        table.append({
            "id": r["id"], "kind": kind(r), "outcome": outcome(kind(r), a, v),
            "refused": a.get("refused", ""),
            "citations": " ".join(c["label"] for c in cites),
            "citations_valid": all(c["valid"] for c in cites) if cites else "",
            "cites_expected_source": any(c["label"][1:].split(",")[0] in expected_sources for c in cites)
            if answerable and cites else "",
            "retrieved_expected": covers(expected(r), a.get("retrieved") or [], kind(r))
            if answerable and a and not a.get("error") else "",
            "citation_check_fired": bool(a.get("guardrail")),
            "citation_check_reason": (a.get("guardrail") or {}).get("reason", ""),
            "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
            "judge_reason": v.get("reason", v.get("error", "")),
            "human_correct": h.get("correct", ""), "human_supported": h.get("supported", ""),
            "model_calls": a.get("model_calls", ""), "input_tokens": a.get("input_tokens", ""),
            "output_tokens": a.get("output_tokens", ""), "seconds": a.get("seconds", ""),
            "judge_tokens": (v.get("input_tokens") or 0) + (v.get("output_tokens") or 0) if v else "",
            "model": a.get("model", ""), "error": a.get("error", ""),
            "question": r["question"], "answer": a.get("answer", ""),
        })
    return table


def failures_table(table: list[dict]) -> list[dict]:
    """Every answer that failed by the judge's verdict or by your own grade.
    `cause` and `notes` are yours (retrieval miss, wrong answer from the right
    passage, unsupported claim, wrong refusal, or bad test question); they are
    kept from the existing eval/failures.csv when this is rewritten."""
    keep = ("id", "kind", "outcome", "retrieved_expected", "refused", "citations", "citation_check_reason",
            "judge_correct", "judge_supported", "judge_reason", "human_correct", "human_supported",
            "question", "answer")
    yours = {}
    path = EVAL / "failures.csv"
    if path.is_file():
        with path.open(newline="", encoding="utf-8-sig") as f:
            yours = {r["id"]: r for r in csv.DictReader(f)}
    rows = []
    for t in table:
        by_judge = t["outcome"] not in GOOD
        by_you = 0 in (t.get("human_correct"), t.get("human_supported"))
        if not (by_judge or by_you):
            continue
        failed_by = "judge and you" if by_judge and by_you else "judge" if by_judge else "you (judge passed it)"
        old = yours.get(t["id"], {})
        rows.append({k: t.get(k, "") for k in keep} | {"failed_by": failed_by, "cause": old.get("cause", ""),
                                                       "notes": old.get("notes", "")})
    return rows


def pct(x: float) -> str:
    return f"{x:.0%}"


def summary_md(retrieval_summary, table, agree, notes) -> str:
    lines = ["# Evaluation summary", ""]
    if retrieval_summary:
        lines += ["## Retrieval", "",
                  "| design | questions | hit@1 | hit@3 | hit@5 | single hit@5 | multi hit@5 | words top1 | top3 | top5 |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for design, t in retrieval_summary.items():
            single, multi, words = t.get("single", {}), t.get("multi", {}), t["words"]
            lines.append(f"| {design} | {t['all']['n']} | {pct(t['all']['hit@1'])} | {pct(t['all']['hit@3'])} | "
                         f"{pct(t['all']['hit@5'])} | {pct(single['hit@5']) if single else '-'} | "
                         f"{pct(multi['hit@5']) if multi else '-'} | {words['top1']:.0f} | {words['top3']:.0f} | "
                         f"{words['top5']:.0f} |")
        lines += ["", f"The agent searches design `{ix.CHOSEN_DESIGN}` with k = {server.TOP_K} "
                      "(index.CHOSEN_DESIGN, server.TOP_K).", ""]
    if table:
        counts = Counter(t["outcome"] for t in table)
        by_kind = {k: Counter(t["outcome"] for t in table if t["kind"] == k) for k in ("single", "multi", "unanswerable")}
        lines += ["## End to end", "", "| outcome | single | multi | unanswerable | total |", "|---|---|---|---|---|"]
        for o in ("correct", "incorrect", "unsupported", "wrong refusal", "correct refusal",
                  "answered (should refuse)", "answered (not judged)", "error"):
            if counts[o]:
                lines.append(f"| {o} | {by_kind['single'][o]} | {by_kind['multi'][o]} | "
                             f"{by_kind['unanswerable'][o]} | {counts[o]} |")
        cited = [t for t in table if t["citations"]]
        fired = [t["id"] for t in table if t["citation_check_fired"]]
        lines += ["", f"- Answers with citations: {len(cited)}; all citations valid in "
                      f"{sum(1 for t in cited if t['citations_valid'] is True)} of them.",
                  f"- Citation check fired on {len(fired)} question(s): {', '.join(fired) or 'none'}.",
                  f"- The agent's searches found the expected passage for "
                  f"{sum(1 for t in table if t['retrieved_expected'] is True)} of "
                  f"{sum(1 for t in table if t['retrieved_expected'] != '')} answerable questions.", ""]
        answered = [t for t in table if t["seconds"] != ""]
        if answered:
            n = len(answered)
            avg = lambda field: sum(float(t[field] or 0) for t in answered) / n  # noqa: E731
            judged = [t for t in table if t["judge_tokens"] != ""]
            lines += ["## Cost and latency per question", "",
                      f"- Agent: {avg('model_calls'):.1f} model calls, {avg('input_tokens'):,.0f} input + "
                      f"{avg('output_tokens'):,.0f} output tokens, {avg('seconds'):.1f} s (n = {n}, model "
                      f"{Counter(t['model'] for t in answered).most_common(1)[0][0]}).",
                      f"- Judge: {sum(t['judge_tokens'] for t in judged) / len(judged):,.0f} tokens "
                      f"(n = {len(judged)})." if judged else "- Judge: not run yet.", ""]
    if agree:
        lines += ["## Judge vs your grades", "", "| | answers | agreement | Cohen's kappa | disagree on |",
                  "|---|---|---|---|---|"]
        for field, a in agree.items():
            lines.append(f"| {field} | {a['n']} | {pct(a['agreement'])} | {a['kappa']:.2f} | "
                         f"{', '.join(a['disagree']) or '-'} |")
        lines.append("")
    if notes:
        lines += ["## Notes", ""] + [f"- {n}" for n in notes] + [""]
    return "\n".join(lines)


# ==========================================================================
# Adding a document: the answer before and after
# ==========================================================================
async def demo(question_id: str, path: str, rows: list[dict], model=None) -> int:
    row = next((r for r in rows if r["id"].strip() == question_id), None)
    if row is None:
        print(f"No question {question_id!r} in eval/questions.csv.")
        return 1
    async with ag.CorpusAgent(model=model, interactive=False, patient=True) as agent:
        before = await agent.ask(row["question"])
    print(f"Before: {before['answer']}\n")
    report = ix.add_document(path)  # running this command is your approval
    print(f"add_document: {report}\n")
    async with ag.CorpusAgent(model=model, interactive=False, patient=True) as agent:
        after = await agent.ask(row["question"])
    print(f"After: {after['answer']}")

    def block(result):
        cites = ", ".join(c["label"] for c in result["citations"]) or "none"
        return ["> " + result["answer"].replace("\n", "\n> "), "", f"Citations: {cites}", ""]

    lines = [f"# Adding a document: {row['id']}", "", f"**Question ({kind(row)}):** {row['question']}", "",
             f"**Document added:** `{Path(path).name}`", "", f"**add_document said:** {report}", "",
             "## Before", ""] + block(before) + ["## After", ""] + block(after)
    (EVAL / "demo_add_document.md").write_text("\n".join(lines), encoding="utf-8")
    print("\nSaved to eval/demo_add_document.md")
    return 0


# ==========================================================================
def main(model=None, judge=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent.")
    parser.add_argument("--retrieval-only", action="store_true", help="only hit rates per design")
    parser.add_argument("--answers-only", action="store_true", help="answers to grade, without the judge")
    parser.add_argument("--fresh", action="store_true", help="ignore cached answers and verdicts")
    parser.add_argument("--demo", nargs=2, metavar=("QUESTION_ID", "FILE"),
                        help="answer a question, add a document, answer again")
    args = parser.parse_args()

    print("== Checking eval/questions.csv")
    if ts.check(need_answers=not args.retrieval_only) != 0:
        print("\nFix the errors in eval/questions.csv first.")
        return 1
    rows, _ = ts.read_questions()
    if not rows:
        return 0
    if args.demo:
        return asyncio.run(demo(args.demo[0], args.demo[1], rows, model))

    notes = []
    print("\n== 1. Retrieval: hit rate per design")
    try:
        per_question, retrieval_summary = retrieval(rows)
    except ix.QuotaExhausted:
        print("  The daily embedding quota is used up; run again after 09:00.")
        return 1
    write_csv(EVAL / "retrieval.csv", per_question)
    if args.retrieval_only:
        (EVAL / "summary.md").write_text(summary_md(retrieval_summary, [], {}, notes), encoding="utf-8")
        print("\nSaved eval/retrieval.csv and eval/summary.md")
        return 0

    print(f"\n== 2. The agent answers every question (design {ix.CHOSEN_DESIGN!r})")
    answers, answered_all = asyncio.run(answer_all(rows, args.fresh, model))
    write_grading_sheet(rows, answers)
    if not answered_all:
        notes.append("Some questions have no answer yet (quota or errors); run `main.py evaluate` again.")
    verdicts, agree = {}, {}
    labels = human_labels()  # also read here so eval/failures.csv lists the failures you found
    if not args.answers_only:
        print("\n== 3. LLM judge")
        verdicts, judged_all = judge_all(rows, answers, args.fresh, judge)
        if rubric_text() and not judged_all:
            notes.append("Some answers have no verdict yet; run `main.py evaluate` again.")
        print("\n== 4. Agreement with your grades")
        agree = agreement(labels, verdicts)
        if len(labels) < 20:
            notes.append(f"eval/human_labels.csv has {len(labels)} graded answers; the brief asks for 20+.")
        print("  " + ("; ".join(f"{f}: {a['agreement']:.0%} of {a['n']}" for f, a in agree.items())
                      or "nothing to compare yet"))

    table = results_table(rows, answers, verdicts, labels)
    write_csv(EVAL / "results.csv", table)
    write_csv(EVAL / "failures.csv", failures_table(table))
    summary = summary_md(retrieval_summary, table, agree, notes)
    (EVAL / "summary.md").write_text(summary, encoding="utf-8")
    print("\n" + summary)
    print("Saved in eval/: retrieval.csv, answers.jsonl, answers_for_grading.md, judge.jsonl, "
          "results.csv, failures.csv, summary.md")
    return 0 if answered_all else 1


if __name__ == "__main__":
    sys.exit(main())
