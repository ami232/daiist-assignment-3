
import fitz
from pathlib import Path

total = 0

for path in Path("corpus").glob("*.pdf"):
    with fitz.open(path) as doc:
        text = " ".join(page.get_text() for page in doc)
        words = len(text.split())
        total += words

        print(f"{path.name}:")
        print(f"Pages: {len(doc)}")
        print(f"Words: {words:,}")
        print("-" * 40)

print(f"TOTAL WORDS: {total:,}")
print("Word requirement:", "PASS" if total >= 50000 else "FAIL")
