
import json
import csv
import time
from pathlib import Path
from evaluate import judge, summarize

p = Path("eval/agent_results.json")
results = json.loads(p.read_text())

human = list(csv.DictReader(
    open("eval/human_labels.csv")
))

assert len(human) >= 20, "Finish human grading first"

for r in results:

    if r.get("label") != "pending":
        continue

    print("Grading", r["id"], flush=True)

    refused = "I don't know based on the available documents" in r["answer"]

    if refused:
        grade = {
            "label": (
                "correct_refusal"
                if r["kind"] == "unanswerable"
                else "wrong_refusal"
            ),
            "reason": "Automatically checked refusal."
        }

    else:
        grade = judge(
            r["question"],
            r["reference_answer"],
            r["answer"],
            r["evidence"]
        )

    r["label"] = grade["label"]
    r["reason"] = grade["reason"]
    r["refused"] = refused

    p.write_text(json.dumps(results, indent=2))

    time.sleep(1)

summary = summarize(results)

by_id = {r["id"]: r for r in results}

correct_agree = 0
supported_agree = 0
both_agree = 0

for h in human:

    r = by_id[h["id"]]

    judge_correct = int(
        r["label"] in ["correct", "correct_refusal"]
    )

    judge_supported = int(
        r["label"] in ["correct", "correct_refusal"]
    )

    c = judge_correct == int(h["correct"])
    s = judge_supported == int(h["supported"])

    correct_agree += c
    supported_agree += s
    both_agree += c and s

summary["human_graded"] = len(human)

summary["correctness_agreement"] = (
    correct_agree / len(human)
)

summary["support_agreement"] = (
    supported_agree / len(human)
)

summary["joint_agreement"] = (
    both_agree / len(human)
)

Path("eval/summary.json").write_text(
    json.dumps(summary, indent=2)
)

print(json.dumps(summary, indent=2))
