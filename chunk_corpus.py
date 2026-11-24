import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "corpus" / "pages.csv"
OUTPUT = ROOT / "corpus" / "chunks.jsonl"

MAX_WORDS = 220
OVERLAP = 40


def split_page(text):
    words = text.split()
    start = 0

    while start < len(words):
        end = min(start + MAX_WORDS, len(words))
        yield " ".join(words[start:end])

        if end == len(words):
            break

        start = end - OVERLAP


def build_chunks():
    chunks = []
    held_back = []

    with PAGES.open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            source = row["guide_id"]
            page = int(row["printed_page"])

            # Hold flagged pages back until their reading order is verified.
            if row["review_note"].strip():
                held_back.append(f"{source} p.{page}")
                continue

            for number, text in enumerate(split_page(row["text"]), start=1):
                chunks.append({
                    "id": f"{source}-p{page:03d}-c{number:02d}",
                    "source": source,
                    "page": page,
                    "text": text,
                })

    return chunks, held_back


if __name__ == "__main__":
    chunks, held_back = build_chunks()

    with OUTPUT.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"Saved {len(chunks)} chunks to {OUTPUT.name}")
    print("Pages held for review:", ", ".join(held_back) or "none")

    example = next(c for c in chunks if c["source"] == "HSG136" and c["page"] == 26)
    print(f"Example: {example['id']}")
    print(example["text"][:300])