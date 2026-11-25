"""
Assignment 3: write each label as readable Markdown, for writing the test set.
`uv run python export_readable.py`

One file per label in readable/ (git-ignored), with each indexed section under
a heading that is exactly its `location` in the index. The `source` for
eval/questions.csv is the file name without .md. No API calls.
"""

import json
from pathlib import Path

from download import HELD_BACK_DIR, LABELS, label_path
from index import chunk_file, label_sections, section_title

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "readable"


def export(path: Path) -> Path:
    label = json.loads(path.read_text(encoding="utf-8"))
    meta = chunk_file(path)[0]["metadata"]
    held_back = path.parent == HELD_BACK_DIR
    lines = [
        f"# {meta['brand']} ({meta['generic']})",
        "",
        f"- source: `{meta['source']}`" + ("  (HELD BACK: not in the index until add_document)" if held_back else ""),
        f"- manufacturer: {meta['manufacturer']} | {meta['product_type']}",
        f"- label: {meta['url']} (version {meta['version']})",
        "",
    ]
    for field, text in label_sections(label):
        lines += [f"## {section_title(field)}", "", text, ""]
    out = OUT_DIR / f"{meta['source']}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    for entry in LABELS:
        print(export(label_path(entry)).relative_to(ROOT))
