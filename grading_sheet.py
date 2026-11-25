import csv, json
from pathlib import Path

ROOT = Path(__file__).parent
rows = list(csv.DictReader(open(ROOT / "eval" / "questions.csv", encoding="utf-8", newline="")))
answers = {a["id"]: a for a in json.loads((ROOT / "eval" / "answers.json").read_text(encoding="utf-8"))}

errors = [i for i, a in answers.items() if a["answer"].startswith("ERROR")]
no_search = [i for i, a in answers.items() if not any(l.startswith("call search(") for l in a["trace"])]
out = [f"# Grading sheet\n\nerrors: {errors or 'none'}  |  answered without calling search: {no_search or 'none'}\n"]
out.append("Grade in eval/human_labels.csv (id,correct,supported,notes). "
           "correct=1: matches the reference (or a proper refusal). supported=1: every claim is in the retrieved passages.\n")
for r in rows:
    a = answers[r["id"]]
    out.append(f"\n---\n\n## {r['id']} ({r['kind']})\n\n**Question:** {r['question']}\n\n**Reference:** {r['reference_answer']}\n")
    out.append(f"**Agent answer:**\n\n{a['answer']}\n")
    searches = [l for l in a["trace"] if l.startswith("call search(")]
    out.append(f"**Searches:** {len(searches)}  ({a['seconds']} s)\n")
    for l in searches:
        out.append(f"- `{l}`")
    passages = [l.removeprefix('result ') for l in a["trace"] if l.startswith("result ")]
    out.append("\n<details><summary>Retrieved passages</summary>\n\n" + "\n\n=====\n\n".join(passages) + "\n\n</details>\n")
(ROOT / "eval" / "grading_sheet.md").write_text("\n".join(out), encoding="utf-8")
print(f"Wrote eval/grading_sheet.md  (errors: {errors or 'none'}; no search: {no_search or 'none'})")
