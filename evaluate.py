"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

Six stages. Each one saves its results in eval/, so a rerun skips finished work.

  STAGE=1  retrieval   hit rate at k = 1, 3, 5 for both chunking designs
  STAGE=2  agent       agent.run() on every question          -> answers.jsonl, to_grade.md
  STAGE=3  code checks citations valid? refused? right source? -> code_checks.csv
  STAGE=4  LLM judge   correct / supported, strict rubric      -> judge.csv
  STAGE=5  agreement   judge against eval/human_labels.csv     -> agreement.csv
  STAGE=6  summary     counts, cost, list of failures          -> summary.md

  STAGE=1 uv run python main.py evaluate      one stage
  uv run python main.py evaluate              all stages (STAGE=all)

SEARCH_DESIGN (article|fixed) chooses the design the agent searches in stage 2.
Query embeddings are cached in index/query_cache.json, so stage 1 costs no quota
the second time.
"""

import csv
import json
import os
import re
import sys
from pathlib import Path

import agent
import index

EVAL = Path(__file__).resolve().parent / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
KS = (1, 3, 5)
MIN_HUMAN_LABELS = 20

RUBRIC = """You grade the answer of an assistant that answers questions about EU railway rules
for a maintenance engineer. Be STRICT. Use only the material below, not your own knowledge.

correct:
- Answerable question: 1 only if EVERY key fact and number of the reference answer is present
  in the answer and NONE is wrong. A partial answer is 0. A refusal is 0.
- Unanswerable question: 1 only if the answer says the corpus does not cover the question and
  does not invent any value or rule. Otherwise 0.

supported:
- 1 only if EVERY claim in the answer is stated in the retrieved passages. One claim that is
  not in the passages makes it 0.
- Naming a law, an authority or a document that is NOT in the retrieved passages is an
  unsupported claim (0), even when it is only offered as a pointer to where to look.
- Only two things are not claims: the closing note about original texts and legal advice,
  and a generic "check the consolidated text on EUR-Lex".
- A refusal that states no rule and names nothing outside the passages is supported (1).

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one or two sentences"}"""


# ----------------------------------------------------------------------------
# Small helpers: read and write the files in eval/
# ----------------------------------------------------------------------------

def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_questions() -> list[dict]:
    return [row for row in read_csv(QUESTIONS) if row["question"].strip()]


def read_answers() -> dict[str, dict]:
    """The agent's saved answers, by question id."""
    if not ANSWERS.is_file():
        return {}
    lines = ANSWERS.read_text(encoding="utf-8").splitlines()
    return {row["id"]: row for row in map(json.loads, filter(None, lines))}


def is_quota_error(error: BaseException) -> bool:
    """True for a 429 / quota error, also when asyncio has wrapped it in an ExceptionGroup."""
    text = str(error)
    if "429" in text or "RESOURCE_EXHAUSTED" in text or "quota" in text.lower():
        return True
    return any(is_quota_error(inner) for inner in getattr(error, "exceptions", ()))


def percent(part: int, total: int) -> str:
    return f"{100 * part / total:.0f}%" if total else "n/a"


# ----------------------------------------------------------------------------
# Stage 1: retrieval
# ----------------------------------------------------------------------------

def expected_passages(question: dict) -> list[tuple[str, str]]:
    """[(doc_id, section), ...] that answer the question, without repeats."""
    sources = [s.strip() for s in question["expected_source"].split(";")]
    locations = [s.strip() for s in question["expected_location"].split(";")]
    passages = []
    for doc_id, location in zip(sources, locations):
        section = agent.section_of(location)  # "Annex, 4.2.8.6(1)-(2)" -> "Annex, 4.2.8.6"
        if (doc_id, section) not in passages:
            passages.append((doc_id, section))
    return passages


def chunk_matches(chunk: dict, passage: tuple[str, str]) -> bool:
    """Section-level match: same document, and the section is one the chunk covers."""
    doc_id, section = passage
    return chunk["doc_id"] == doc_id and section in chunk["sections"].split("; ")


def stage_1_retrieval() -> None:
    import server  # server.retrieve(query, k, design) is the function the search tool uses

    questions = [q for q in read_questions() if q["kind"] != "unanswerable"]

    # A test question whose expected section is in no chunk can never be hit: report it.
    known = set()
    for design in index.DESIGNS:
        for meta in index.get_collection(design).get(include=["metadatas"])["metadatas"]:
            known.update((meta["doc_id"], section) for section in meta["sections"].split("; "))
    for question in questions:
        for passage in expected_passages(question):
            if passage not in known:
                print(f"WARNING {question['id']}: no chunk has the section {passage}; check expected_location.")

    results = []
    for question in questions:
        expected = expected_passages(question)
        for design in index.DESIGNS:
            try:
                top = server.retrieve(question["question"], max(KS), design)  # the query embedding is cached
            except index.QuotaExhausted:
                print("Stage 1 stopped: the embedding quota is used up. Rerun later; finished queries are cached.")
                sys.exit(0)
            found_at = {}  # passage -> rank of the first chunk that matches it
            for rank, chunk in enumerate(top, 1):
                for passage in expected:
                    if chunk_matches(chunk, passage) and passage not in found_at:
                        found_at[passage] = rank
            first_hit = min(found_at.values(), default=None)
            row = {
                "id": question["id"],
                "kind": question["kind"],
                "design": design,
                "expected": "; ".join(f"{doc_id}: {section}" for doc_id, section in expected),
                "first_hit_rank": first_hit or "",
            }
            for k in KS:
                row[f"hit@{k}"] = int(first_hit is not None and first_hit <= k)
            row["passages_expected"] = len(expected)
            row["passages_found@5"] = len(found_at)
            row["all_found@5"] = int(len(found_at) == len(expected))
            row["words@5"] = sum(index.n_words(chunk["text"]) for chunk in top)
            row["top5"] = " | ".join(f"[{chunk['doc_id']}, {chunk['location']}]" for chunk in top)
            results.append(row)
    write_csv(EVAL / "retrieval_results.csv", results)

    summary = []
    for design in index.DESIGNS:
        rows = [row for row in results if row["design"] == design]
        multi = [row for row in rows if row["kind"] == "multi"]
        line = {"design": design, "questions": len(rows)}
        for k in KS:
            line[f"hit@{k}"] = round(sum(row[f"hit@{k}"] for row in rows) / len(rows), 3)
        line["multi_questions"] = len(multi)
        line["multi_all@5"] = round(sum(row["all_found@5"] for row in multi) / len(multi), 3) if multi else ""
        line["words@5"] = round(sum(row["words@5"] for row in rows) / len(rows))
        summary.append(line)
    write_csv(EVAL / "retrieval_summary.csv", summary)

    print(f"\nRetrieval on {len(questions)} answerable questions (section-level match)")
    print(f"{'design':<9}| hit@1 | hit@3 | hit@5 | multi all@5 | words@5")
    for line in summary:
        print(f"{line['design']:<9}| {line['hit@1']:.2f}  | {line['hit@3']:.2f}  | {line['hit@5']:.2f}  | {line['multi_all@5']:<11} | {line['words@5']}")
    for design in index.DESIGNS:
        misses = [row["id"] for row in results if row["design"] == design and not row["hit@5"]]
        partial = [row["id"] for row in results if row["design"] == design and row["hit@5"] and not row["all_found@5"]]
        print(f"{design}: no hit in top 5: {', '.join(misses) or 'none'}; hit but not all passages: {', '.join(partial) or 'none'}")


# ----------------------------------------------------------------------------
# Stage 2: the agent answers every question
# ----------------------------------------------------------------------------

def stage_2_agent() -> bool:
    """Returns False if it had to stop early (quota), so later stages wait."""
    design = os.environ.get("SEARCH_DESIGN", "article")
    questions = read_questions()
    done = read_answers()
    other = {row["design"] for row in done.values()} - {design}
    if other:
        print(f"Stage 2 stopped: eval/answers.jsonl holds answers made with SEARCH_DESIGN={other.pop()}, not {design}.")
        print("Set SEARCH_DESIGN to match, or delete eval/answers.jsonl to start again.")
        return False

    for question in questions:
        if question["id"] in done:
            continue
        try:
            result = agent.run(question["question"])  # add_document is denied: nobody to ask
        except Exception as error:  # noqa: BLE001 - the model's quota error has no single type
            if not is_quota_error(error):
                raise
            print(f"Stage 2 stopped at {question['id']}: the model's quota is used up (429).")
            break
        if any("quota" in call.get("message", "") for call in result["tool_trace"]):
            print(f"Stage 2 stopped at {question['id']}: the embedding quota is used up, the search could not run.")
            break
        row = {"id": question["id"], "kind": question["kind"], "design": design, **result}
        with ANSWERS.open("a", encoding="utf-8") as f:  # saved at once: an interruption loses nothing
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        done[question["id"]] = row
        print(f"{question['id']} ({question['kind']}): {len(result['tool_trace'])} tool calls, {result['seconds']}s, guardrails {result['guardrail_fired'] or 'none'}")

    write_to_grade(questions, done)
    missing = len(questions) - len(done)
    print(f"Stage 2: {len(done)} of {len(questions)} answers in eval/answers.jsonl" + (f"; {missing} missing, rerun to continue." if missing else "."))
    return missing == 0


def retrieved_citations(answer: dict) -> list[str]:
    """Every passage the agent's searches returned, as [doc_id, location], without repeats."""
    seen = []
    for chunk in answer["retrieved_chunks"]:
        citation = f"[{chunk['doc_id']}, {chunk['location']}]"
        if citation not in seen:
            seen.append(citation)
    return seen


def write_to_grade(questions: list[dict], answers: dict[str, dict]) -> None:
    """eval/to_grade.md: what a human needs to grade the answers, without the judge's verdicts."""
    lines = [
        "# Answers to grade",
        "",
        "Grade in eval/human_labels.csv (id, correct, supported, notes) before reading eval/judge.csv.",
    ]
    for question in questions:
        answer = answers.get(question["id"])
        if answer is None:
            continue
        lines += [
            "", f"## {question['id']} ({question['kind']})",
            "", f"**Question:** {question['question']}",
            "", f"**Reference answer:** {question['reference_answer']}",
            "", "**Agent answer:**", "", answer["answer"],
            "", "**Retrieved passages:** " + (", ".join(retrieved_citations(answer)) or "none"),
        ]
    (EVAL / "to_grade.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ----------------------------------------------------------------------------
# Stage 3: what code can check
# ----------------------------------------------------------------------------

def is_refusal(answer_text: str, draft: str) -> bool:
    """Refused = it says the corpus does not cover the question, or a guardrail replaced the draft."""
    return agent.NOT_COVERED.lower() in answer_text.lower() or answer_text != draft


def refusal_counts(questions: list[dict], answers: dict, answer_field: str, fired_field: str) -> dict:
    """The four counts of the v1 / v2 table, for one version of the answers."""
    counts = {"correct refusals": 0, "wrong refusals": 0, "answered unanswerable": 0, "guardrail fired": 0}
    for question in questions:
        answer = answers.get(question["id"])
        if answer is None:
            continue
        refused = is_refusal(answer[answer_field], answer["draft_answer"])
        unanswerable = question["kind"] == "unanswerable"
        counts["correct refusals"] += unanswerable and refused
        counts["wrong refusals"] += not unanswerable and refused
        counts["answered unanswerable"] += unanswerable and not refused
        counts["guardrail fired"] += bool(answer[fired_field])
    return counts


def stage_3_code_checks() -> None:
    questions = read_questions()
    answers = read_answers()
    rows = []
    for question in questions:
        answer = answers.get(question["id"])
        if answer is None:
            continue
        # Citations are checked on the model's own draft, before the citation guardrail replaced anything.
        valid, invalid = agent.check_citations(answer["draft_answer"], answer["retrieved_chunks"])
        refused = is_refusal(answer["answer"], answer["draft_answer"])
        unanswerable = question["kind"] == "unanswerable"
        expected_sources = {s.strip() for s in question["expected_source"].split(";") if s.strip()}
        rows.append({
            "id": question["id"],
            "kind": question["kind"],
            "citations": len(valid) + len(invalid),
            "invalid_citations": "; ".join(invalid),
            "citations_valid": int(not invalid),
            "refused": int(refused),
            "correct_refusal": int(unanswerable and refused),
            "wrong_refusal": int(not unanswerable and refused),
            "answered_unanswerable": int(unanswerable and not refused),
            "cited_expected_source": "" if unanswerable else int(any(c["doc_id"] in expected_sources for c in valid)),
            "guardrail_fired": "; ".join(answer["guardrail_fired"]),
        })
    if not rows:
        print("Stage 3: no answers yet; run stage 2 first.")
        return
    write_csv(EVAL / "code_checks.csv", rows)
    total = lambda column: sum(int(row[column] or 0) for row in rows)  # noqa: E731
    print(f"Stage 3: {len(rows)} answers checked. Citations all valid: {total('citations_valid')}; correct refusals: {total('correct_refusal')}; "
          f"wrong refusals: {total('wrong_refusal')}; answered an unanswerable question: {total('answered_unanswerable')}.")

    # The citation guardrail was relaxed after the first run (v1 exact match, v2 same section).
    # eval/reapply_guardrail.py kept the v1 result of each answer, so both can be compared.
    if all("answer_v1" in answer for answer in answers.values()):
        v1 = refusal_counts(questions, answers, "answer_v1", "guardrail_fired_v1")
        v2 = refusal_counts(questions, answers, "answer", "guardrail_fired")
        write_csv(EVAL / "guardrail_v1_v2.csv", [{"count": name, "v1_exact_match": v1[name], "v2_same_section": v2[name]} for name in v1])
        print(f"\n{'citation guardrail':<24}| v1 exact | v2 same section")
        for name in v1:
            print(f"{name:<24}| {v1[name]:<8} | {v2[name]}")


# ----------------------------------------------------------------------------
# Stage 4: LLM judge
# ----------------------------------------------------------------------------

def judge_prompt(question: dict, answer: dict) -> str:
    passages, seen = [], set()
    for chunk in answer["retrieved_chunks"]:
        if (chunk["doc_id"], chunk["location"]) not in seen:
            seen.add((chunk["doc_id"], chunk["location"]))
            passages.append(f"[{chunk['doc_id']}, {chunk['location']}]\n{chunk['text']}")
    kind = "UNANSWERABLE from the corpus" if question["kind"] == "unanswerable" else "answerable"
    return "\n\n".join([
        RUBRIC,
        f"QUESTION ({kind}):\n{question['question']}",
        f"REFERENCE ANSWER:\n{question['reference_answer']}",
        "RETRIEVED PASSAGES:\n" + ("\n\n".join(passages) or "(none)"),
        f"ASSISTANT ANSWER:\n{answer['answer']}",
    ])


def stage_4_judge() -> bool:
    from google import genai

    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    answers = read_answers()
    path = EVAL / "judge.csv"
    verdicts = read_csv(path)
    judged = {row["id"] for row in verdicts}
    todo = [q for q in read_questions() if q["id"] in answers and q["id"] not in judged]
    for question in todo:
        try:
            response = client.models.generate_content(
                model=agent.MODEL,  # the same model that answered
                contents=judge_prompt(question, answers[question["id"]]),
                config={"response_mime_type": "application/json"},
            )
            verdict = json.loads(response.text)
        except json.JSONDecodeError:
            print(f"{question['id']}: the judge did not return JSON; it will be asked again on the next run.")
            continue
        except Exception as error:  # noqa: BLE001
            if not is_quota_error(error):
                raise
            print(f"Stage 4 stopped on the model quota at {question['id']}: {str(error)[:200]}")
            break
        verdicts.append({
            "id": question["id"],
            "kind": question["kind"],
            "correct": int(verdict["correct"]),
            "supported": int(verdict["supported"]),
            "reason": verdict.get("reason", ""),
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.total_token_count - response.usage_metadata.prompt_token_count,
        })
        write_csv(path, verdicts)  # saved after every verdict
        print(f"{question['id']}: correct={verdict['correct']} supported={verdict['supported']}")
    missing = len(answers) - len(verdicts)
    print(f"Stage 4: {len(verdicts)} verdicts in eval/judge.csv" + (f"; {missing} answers not judged yet, rerun to continue." if missing else "."))
    return missing == 0


# ----------------------------------------------------------------------------
# Stage 5: does the judge agree with the human grades?
# ----------------------------------------------------------------------------

def stage_5_agreement() -> None:
    human = {row["id"]: row for row in read_csv(EVAL / "human_labels.csv") if row["id"].strip() and row["correct"].strip()}
    judge = {row["id"]: row for row in read_csv(EVAL / "judge.csv")}
    both = [i for i in human if i in judge]
    if len(both) < MIN_HUMAN_LABELS:
        print(f"Stage 5 skipped: {len(both)} answers have both a human grade and a judge verdict; {MIN_HUMAN_LABELS} are needed.")
        return
    rows = []
    for i in both:
        rows.append({
            "id": i,
            "human_correct": human[i]["correct"].strip(), "judge_correct": judge[i]["correct"],
            "human_supported": human[i]["supported"].strip(), "judge_supported": judge[i]["supported"],
            "agree_correct": int(human[i]["correct"].strip() == judge[i]["correct"]),
            "agree_supported": int(human[i]["supported"].strip() == judge[i]["supported"]),
            "human_notes": human[i].get("notes", ""), "judge_reason": judge[i]["reason"],
        })
    write_csv(EVAL / "agreement.csv", rows)
    for field in ("correct", "supported"):
        agreed = sum(row[f"agree_{field}"] for row in rows)
        print(f"Stage 5: judge and human agree on `{field}` for {agreed} of {len(rows)} answers ({percent(agreed, len(rows))}).")
        for row in rows:
            if not row[f"agree_{field}"]:
                print(f"  {row['id']} {field}: human {row[f'human_{field}']}, judge {row[f'judge_{field}']}.")
                print(f"      human note:   {row['human_notes'] or '(none)'}")
                print(f"      judge reason: {row['judge_reason']}")


# ----------------------------------------------------------------------------
# Stage 6: summary
# ----------------------------------------------------------------------------

def stage_6_summary() -> None:
    answers = read_answers()
    checks = {row["id"]: row for row in read_csv(EVAL / "code_checks.csv")}
    judge = {row["id"]: row for row in read_csv(EVAL / "judge.csv")}
    ids = [i for i in answers if i in checks and i in judge]
    if not ids:
        print("Stage 6: nothing to summarise yet; stages 2, 3 and 4 come first.")
        return
    n = len(ids)
    count = lambda table, column: sum(int(table[i][column] or 0) for i in ids)  # noqa: E731
    answerable = [i for i in ids if answers[i]["kind"] != "unanswerable"]
    unanswerable = [i for i in ids if answers[i]["kind"] == "unanswerable"]
    correct = count(judge, "correct")
    unsupported = n - count(judge, "supported")

    lines = [
        "# Evaluation summary",
        "",
        "Written by `main.py evaluate` (stage 6) and rewritten on every run: do not edit it by hand.",
        "",
        f"- Questions answered and judged: {n} ({len(answerable)} answerable, {len(unanswerable)} unanswerable)",
        f"- Design searched by the agent: {answers[ids[0]]['design']}; model: {answers[ids[0]]['model']} (also the judge)",
        f"- Correct (judge): {correct} of {n} ({percent(correct, n)})",
        f"- Correct among answerable questions (judge): {sum(int(judge[i]['correct']) for i in answerable)} of {len(answerable)}",
        f"- Unsupported answers (judge, supported = 0): {unsupported} of {n} ({percent(unsupported, n)})",
        f"- Correct refusals (unanswerable and refused): {count(checks, 'correct_refusal')} of {len(unanswerable)}",
        f"- Wrong refusals (answerable but refused): {count(checks, 'wrong_refusal')} of {len(answerable)}",
        f"- Answered an unanswerable question: {count(checks, 'answered_unanswerable')} of {len(unanswerable)}",
        f"- Answers with a citation that was not retrieved (before the guardrail): {n - count(checks, 'citations_valid')}",
        f"- Mean tokens per question: {sum(answers[i]['input_tokens'] for i in ids) / n:,.0f} input, {sum(answers[i]['output_tokens'] for i in ids) / n:,.0f} output",
        f"- Mean seconds per question: {sum(answers[i]['seconds'] for i in ids) / n:.1f}",
    ]

    retrieval = read_csv(EVAL / "retrieval_summary.csv")
    if retrieval:
        lines += ["", "## Retrieval (stage 1)", "", "| " + " | ".join(retrieval[0]) + " |", "|" + "---|" * len(retrieval[0])]
        lines += ["| " + " | ".join(row.values()) + " |" for row in retrieval]

    hits = {row["id"]: row for row in read_csv(EVAL / "retrieval_results.csv") if row["design"] == answers[ids[0]]["design"]}
    lines += [
        "", "## Failures to classify", "",
        "Every answer the judge marked not correct or not supported, or that code flagged.",
        "Classes: retrieval miss, wrong answer from the right passage, unsupported claim, wrong refusal, bad test question.",
        "", "| id | kind | correct | supported | code checks | question-only retrieval hit@5 | judge's reason |", "|---|---|---|---|---|---|---|",
    ]
    for i in ids:
        flags = [name for name in ("wrong_refusal", "answered_unanswerable") if int(checks[i][name])]
        if not int(checks[i]["citations_valid"]):
            flags.append("invalid citation: " + checks[i]["invalid_citations"])
        if checks[i]["guardrail_fired"]:
            flags.append("guardrail: " + checks[i]["guardrail_fired"])
        if int(judge[i]["correct"]) and int(judge[i]["supported"]) and not flags:
            continue
        hit = hits[i]["hit@5"] if i in hits else ""
        reason = judge[i]["reason"].replace("|", "/").replace("\n", " ")
        lines.append(f"| {i} | {answers[i]['kind']} | {judge[i]['correct']} | {judge[i]['supported']} | {'; '.join(flags)} | {hit} | {reason} |")
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[4:15]))
    print("Stage 6: eval/summary.md written.")


def main() -> None:
    stage = os.environ.get("STAGE", "all").strip().lower() or "all"
    if stage not in ("1", "2", "3", "4", "5", "6", "all"):
        raise SystemExit(f"STAGE must be 1..6 or all, not {stage!r}")
    if stage in ("1", "all"):
        stage_1_retrieval()
    if stage in ("2", "all") and not stage_2_agent() and stage == "all":
        return  # stopped early: the later stages wait for the missing answers
    if stage in ("3", "all"):
        stage_3_code_checks()
    if stage in ("4", "all") and not stage_4_judge() and stage == "all":
        return
    if stage in ("5", "all"):
        stage_5_agreement()
    if stage in ("6", "all"):
        stage_6_summary()


if __name__ == "__main__":
    main()
