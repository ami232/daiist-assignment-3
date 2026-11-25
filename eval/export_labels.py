"""Turn grading_sheet.xlsx into human_labels.csv and check it.
Run from the eval folder:  python export_labels.py
"""
import csv
from openpyxl import load_workbook

ws = load_workbook("grading_sheet.xlsx").active
rows, problems = [], []
for r in ws.iter_rows(min_row=2, values_only=True):
    qid, correct, supported, notes = r[0], r[6], r[7], r[8]
    if correct is None and supported is None:
        continue  # not graded yet
    c, s = str(correct).strip(), str(supported).strip()
    notes = (notes or "").strip()
    if c not in ("0", "1") or s not in ("0", "1"):
        problems.append(f"{qid}: correct/supported must be 0 or 1")
    if ("0" in (c, s)) and not notes:
        problems.append(f"{qid}: has a 0 but no note")
    rows.append([qid, c, s, notes])

with open("human_labels.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "correct", "supported", "notes"])
    w.writerows(rows)

print(f"wrote {len(rows)} labelled rows to human_labels.csv")
if len(rows) < 20:
    print("warning: fewer than 20 rows labelled")
for p in problems:
    print("fix:", p)
