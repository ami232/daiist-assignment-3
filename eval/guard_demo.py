"""
Assignment 3: show the citation guard firing. `uv run python eval/guard_demo.py`

Takes a real answer and trace from eval/answers.jsonl, then runs the same
citation_guard that agent.py applies to every answer on three versions of it:
the real answer, the answer with one citation changed to a passage that search
did not return, and the answer with its citations removed. No API calls.
Writes eval/guard_demo.md.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent import citation_guard  # noqa: E402

ANSWERS = ROOT / "eval" / "answers.jsonl"
OUT = ROOT / "eval" / "guard_demo.md"
QID = "q07"
FAKE = "[RD1066-2007, Artículo 22]"  # a real article that search did not return for this question


def main() -> None:
    rows = {r["id"]: r for r in map(json.loads, ANSWERS.read_text(encoding="utf-8").splitlines())}
    row = rows[QID]
    real = row["raw_answer"]
    first = re.search(r"\[[^\[\]]+\]", real).group(0)
    cases = [
        ("Real answer", real),
        (f"One citation changed to {FAKE}", real.replace(first, FAKE, 1)),
        ("Citations removed", re.sub(r"\s*\[[^\[\]]+\]", "", real)),
    ]

    lines = [
        "# Citation guard demo",
        "",
        f"Question {QID}: {row['question']}",
        "",
        "Passages search returned in this run: "
        + ", ".join(f"[{d}, {loc}]" for d, loc in row["citations"]["retrieved"]),
        "",
    ]
    for title, answer in cases:
        shown, report = citation_guard(answer, row["trace"], row.get("approvals"))
        lines += [
            f"## {title}",
            "",
            f"Guard fired: **{report['fired']}**" + (f" ({report['reason']})" if report["fired"] else ""),
            "",
            "Answer the user sees:",
            "",
            "> " + shown.strip().replace("\n", "\n> "),
            "",
        ]
        print(f"{title}: fired={report['fired']}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
