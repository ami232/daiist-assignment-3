
import csv
import json
from pathlib import Path

INPUT = Path("eval/agent_answers.jsonl")
OUTPUT = Path("eval/human_review.csv")
LABELS = Path("eval/human_labels.csv")

records = [
    json.loads(line)
    for line in INPUT.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

fields = [
    "id",
    "kind",
    "question",
    "reference_answer",
    "agent_answer",
    "retrieved_evidence",
]

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for record in records:
        evidence = "\n\n".join(
            entry.get("result", "")
            for entry in record["tool_trace"]
            if entry.get("tool") == "search"
        )

        writer.writerow({
            "id": record["id"],
            "kind": record["kind"],
            "question": record["question"],
            "reference_answer": record["reference_answer"],
            "agent_answer": record["answer"],
            "retrieved_evidence": evidence,
        })

if not LABELS.exists():
    with LABELS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "correct", "supported", "notes"])

print(f"Prepared {len(records)} answers for human review.")
print(f"Review file: {OUTPUT}")
print(f"Labels file: {LABELS}")
