"""
Re-apply the citation guardrail (version 2) to the answers already saved in eval/answers.jsonl.

    uv run python eval/reapply_guardrail.py

No model call: it only re-checks each saved draft_answer against the passages that run retrieved.
The result of the first version (exact match) is kept in answer_v1 and guardrail_fired_v1;
answer, citations, guardrail_fired, invalid_citations and refused become the version 2 result.
Safe to run twice: the v1 fields are written only the first time.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import agent  # noqa: E402
import evaluate  # noqa: E402

answers = evaluate.read_answers()
changed = []
for row in answers.values():
    row.setdefault("answer_v1", row["answer"])
    row.setdefault("guardrail_fired_v1", list(row["guardrail_fired"]))
    if not row["draft_answer"]:  # the model wrote nothing: there is no draft to check again
        continue
    checked = agent.apply_citation_guardrail(row["draft_answer"], row["retrieved_chunks"])
    other_guardrails = [name for name in row["guardrail_fired_v1"] if name != "citation_check"]
    row["answer"] = checked["answer"]
    row["citations"] = checked["citations"]
    row["invalid_citations"] = checked["invalid_citations"]
    row["guardrail_fired"] = other_guardrails + (["citation_check"] if checked["fired"] else [])
    row["refused"] = evaluate.is_refusal(row["answer"], row["draft_answer"])
    if row["answer"] != row["answer_v1"]:
        changed.append(row["id"])

evaluate.ANSWERS.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in answers.values()), encoding="utf-8")
evaluate.write_to_grade(evaluate.read_questions(), answers)
print(f"{len(answers)} answers re-checked; answer changed from v1 to v2 for {len(changed)}: {', '.join(changed) or 'none'}")
print("eval/answers.jsonl and eval/to_grade.md rewritten.")
