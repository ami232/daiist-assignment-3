"""Rebuild the paired comparison from the two sets of saved answers and judge verdicts."""
import csv
import json

from agent import REFUSAL, guard_answer
from evaluate import EVAL, EXPERIMENT, expected, read_csv, report_agreement


def read_json(folder, filename):
    return json.loads((folder / filename).read_text(encoding="utf-8"))


def measurements(question, run, verdict):
    searches = [event for event in run["trace"] if event["tool"] == "search"]
    locations = {p["id"]: (p["source"], p["location"]) for p in run["passages"]}
    required = expected(question)
    first = {locations[key] for key in searches[0]["ids"]} if searches else set()
    return {
        "correct": int(verdict["correct"]),
        "supported": int(verdict["supported"]),
        "refused": int(run["answer"] == REFUSAL),
        "first_search_all_sections": int(required <= first) if required else "",
        "all_searches_all_sections": int(required <= set(locations.values())) if required else "",
        "searches": len(searches),
        "seconds": run["seconds"],
        "input_tokens": run["input_tokens"],
        "output_tokens": run["output_tokens"],
    }


def main():
    questions = read_csv(EVAL / "questions.csv")
    question_ids = [q["id"] for q in questions]
    pairs = [{"id": q["id"], "kind": q["kind"]} for q in questions]
    baseline = read_json(EVAL, "summary.json")
    revised = read_json(EXPERIMENT, "summary.json")
    if any(baseline[k] != revised[k] for k in ("n", "design", "agent_model", "judge_model")):
        raise ValueError("The run size, search design and models must match for this comparison")
    labels = read_csv(EVAL / "human_labels.csv")
    if report_agreement(labels, read_json(EVAL, "judge.json")) != baseline["human_agreement"]:
        raise ValueError("The original grades no longer reproduce the baseline agreement")
    for name, folder in (("baseline", EVAL), ("experiment", EXPERIMENT)):
        answers = read_json(folder, "answers.json")
        verdicts = read_json(folder, "judge.json")
        if [a["id"] for a in answers] != question_ids or set(verdicts) != set(question_ids):
            raise ValueError(f"{name} answers and verdicts must cover the complete question set")
        lookup = read_json(folder, "retrieval.json")
        fixed_hits = {r["id"]: r["ids"] for r in lookup["per_question"] if r["design"] == lookup["selected"]}
        for q, a, pair in zip(questions, answers, pairs, strict=True):
            key = q["id"]
            if q["question"] != a["question"]:
                raise ValueError(f"{name} {key} used a different question")
            if name == "experiment":
                first = a["trace"][0]
                if first["tool"] != "search" or first["query"] != q["question"]:
                    raise ValueError(f"{key} did not start with the original question")
                if key in fixed_hits and first["ids"] != fixed_hits[key]:
                    raise ValueError(f"{key} first search differs from the fixed-query benchmark")
                evidence = {p["id"] for p in a["passages"]}
                if guard_answer(a["raw_answer"], evidence) != (a["answer"], a["guardrail"]):
                    raise ValueError(f"{key} saved answer differs from the citation guard decision")
            row = measurements(q, a, verdicts[key])
            pair.update({f"{name}_{metric}": value for metric, value in row.items()})

    with (EXPERIMENT / "comparison.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(pairs[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(pairs)


if __name__ == "__main__":
    main()
