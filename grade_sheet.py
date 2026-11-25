"""Writes eval/answers_to_grade.md: question, reference, the agent's answer and the passages
it retrieved, for grading by hand. It does NOT show any judge verdict.
Usage: uv run python grade_sheet.py"""
import csv
import json
from pathlib import Path

EVAL = Path(__file__).resolve().parent / "eval"
qs = {r["id"]: r for r in csv.DictReader((EVAL / "questions.csv").open(encoding="utf-8")) if r.get("id")}
lines = [
    "# Answers to grade by hand",
    "",
    "For each one write a row in `eval/human_labels.csv`: `id,correct,supported,notes`.",
    "- **correct** 1/0: agrees with the REFERENCE on everything that matters (or is a proper refusal for an unanswerable question).",
    "- **supported** 1/0: every claim in the answer is in the RETRIEVED passages.",
    "- **notes**: why, for every 0.",
    "",
]
for line in (EVAL / "answers.jsonl").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    a = json.loads(line)
    q = qs.get(a["id"], {})
    passages = "\n\n".join(t["result"] for t in a["trace"] if t["tool"] == "search")
    lines += [
        f"---", f"## {a['id']} ({q.get('kind', '?')})", "",
        f"**Question:** {a['question']}", "",
        f"**Reference:** {q.get('reference_answer', '')}", "",
        f"**Agent answer:**", "", a["answer"], "",
        f"**Retrieved passages:**", "", "```", passages[:5000], "```", "",
    ]
(EVAL / "answers_to_grade.md").write_text("\n".join(lines), encoding="utf-8")
print("wrote eval/answers_to_grade.md")
