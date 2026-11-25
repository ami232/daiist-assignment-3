"""Re-check `supported` grades: shows the agent's answer next to the text of the articles it cited.

    uv run python regrade.py q13 q14 q15      # only these ids
    uv run python regrade.py --reference      # every row whose note mentions "reference" and supported=0
    uv run python regrade.py --zero           # every row with supported=0
"""

import csv
import json
import re
import sys
from pathlib import Path

EVAL = Path(__file__).resolve().parent / "eval"
LABELS = EVAL / "human_labels.csv"
FIELDS = ["id", "correct", "supported", "notes"]
CITATION = re.compile(r"\[([^\[\]]+?),\s*([^\[\]]+?)\]")
BLOCK = re.compile(r"^\[\d+\]\s+\[([^\[\]]+?),\s*([^\[\]]+?)\]", re.M)


def base_location(location):
    return re.split(r"(?<=\d)\.\d|,\s*\d|\s+(?:apartado|párrafo|letra|apdo)\b", location)[0].strip()


def read_labels():
    with LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def write_labels(rows):
    with LABELS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in sorted(rows.values(), key=lambda r: r["id"]):
            writer.writerow({k: r.get(k, "") for k in FIELDS})


def cited_passages(answer, trace):
    wanted = {(s.strip(), base_location(l)) for s, l in CITATION.findall(answer)}
    shown, seen = [], set()
    for call in trace:
        if call["tool"] != "search":
            continue
        text = call["result"]
        heads = list(BLOCK.finditer(text))
        for i, m in enumerate(heads):
            key = (m.group(1).strip(), base_location(m.group(2).strip()))
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            block = text[m.start():end].strip()
            if key in wanted and block not in seen:
                seen.add(block)
                shown.append(block)
    return shown


def main():
    args = sys.argv[1:]
    labels = read_labels()
    answers = {r["id"]: r for r in map(json.loads, filter(str.strip, (EVAL / "answers.jsonl").open(encoding="utf-8")))}
    if "--zero" in args:
        ids = [i for i, r in labels.items() if r.get("supported") == "0"]
    elif "--reference" in args:
        ids = [i for i, r in labels.items() if r.get("supported") == "0" and "reference" in r.get("notes", "").lower()]
    else:
        ids = [a for a in args if a in labels]
    ids = sorted(ids)
    print(f"{len(ids)} rows to re-check: {', '.join(ids)}\n")

    for n, qid in enumerate(ids, 1):
        row, ans = labels[qid], answers[qid]
        print("=" * 78)
        print(f"[{n}/{len(ids)}] {qid}   your grade now: correct={row['correct']} supported={row['supported']}")
        print(f"YOUR NOTE: {row.get('notes', '')}\n")
        print(f"AGENT ANSWER:\n{ans['answer']}\n")
        print("TEXT OF THE ARTICLES IT CITED (from the search results):")
        for p in cited_passages(ans["answer"], ans["trace"]) or ["(none of its citations matches a retrieved passage)"]:
            print("-" * 60)
            print(p)
        print("-" * 60)
        print("supported = 1 only if EVERY claim in the answer appears in the text above.")
        while True:
            new = input(f"supported now (1/0, Enter keeps {row['supported']}, q quit)? ").strip().lower()
            if new in {"", "0", "1", "q"}:
                break
        if new == "q":
            break
        if new:
            row["supported"] = new
        if row["supported"] == "0" or new:
            note = input("note in your own words (what exactly is / is not in the article; Enter keeps old): ").strip()
            if note:
                row["notes"] = note
            while row["supported"] == "0" and (not row.get("notes", "").strip() or row["notes"].strip() == "0"):
                row["notes"] = input("  a 0 needs a reason: ").strip()
        write_labels(labels)
    print(f"\nSaved to {LABELS}.")


if __name__ == "__main__":
    main()
