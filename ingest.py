
import json
import re
from pathlib import Path

import pymupdf

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

DOCUMENTS = {
    "CELEX_32016R0679_EN_TXT.pdf": "GDPR",
    "CELEX_32022R2065_EN_TXT.pdf": "DSA",
    "OJ_L_202401689_EN_TXT.pdf": "AI_ACT",
}


def clean_text(text):
    # Remove null characters and unusual spacing.
    text = text.replace("\x00", "")
    text = text.replace("\u00a0", " ")

    # Join words split across lines by hyphens.
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Normalize spaces without removing paragraph breaks.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_documents():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    total_words = 0

    for filename, source in DOCUMENTS.items():
        pdf_path = RAW_DIR / filename

        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)

        records = []

        with pymupdf.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = clean_text(
                    page.get_text("text", sort=True)
                )

                if not text:
                    continue

                records.append({
                    "source": source,
                    "page": page_number,
                    "text": text,
                })

        output_path = PROCESSED_DIR / f"{source.lower()}.json"

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=2)

        words = sum(len(record["text"].split()) for record in records)
        total_words += words

        print(f"{source}: {len(records)} pages, {words:,} words")
        print(f"Saved: {output_path}")

    print(f"\nTOTAL: {total_words:,} words")


if __name__ == "__main__":
    extract_documents()