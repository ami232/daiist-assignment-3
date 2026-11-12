
from pathlib import Path
import re
import pymupdf

DATA_DIR = Path("data/raw")

total_words = 0

for pdf_path in sorted(DATA_DIR.glob("*.pdf")):
    doc = pymupdf.open(pdf_path)

    page_count = len(doc)
    word_count = 0

    for page in doc:
        text = page.get_text("text", sort=True)
        words = re.findall(r"\b[\w]+(?:[-’'][\w]+)*\b", text)
        word_count += len(words)

    total_words += word_count

    print(f"\nDocument: {pdf_path.name}")
    print(f"Pages: {page_count}")
    print(f"Words: {word_count:,}")

print("\n------------------------------")
print(f"TOTAL WORDS: {total_words:,}")
print(f"Minimum required: 50,000")
print(f"Requirement met: {total_words >= 50000}")
