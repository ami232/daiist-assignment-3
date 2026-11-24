import csv
import re
from pathlib import Path

from pypdf import PdfReader


CORPUS = Path(__file__).resolve().parent / "corpus"
OUTPUT = CORPUS / "pages.csv"

# Each entry contains the first and last printed page we want to keep.
GUIDES = {
    "HSG76": (4, 143),
    "HSG136": (4, 49),
    "L117": (5, 37),
}

HEADERS = {
    "Health and Safety",
    "Executive",
    "Health and Safety Executive",
    "Warehousing and storage: A guide to health and safety",
    "A guide to workplace transport safety",
    "Rider-operated lift trucks",
}


def clean_page(raw_text):
    """Remove repeated headers and page numbers, keeping the text line order."""
    lines = []

    for line in (raw_text or "").splitlines():
        line = re.sub(r"\bPage\s+\d+\s+of\s+\d+\b", "", line)
        line = line.replace("\x98", "•").replace("\u00ad", "")
        line = " ".join(line.split())

        if line and line not in HEADERS:
            lines.append(line)

    return "\n".join(lines)


def extract_page(pdf_page, guide, page_number):
    """Return the cleaned text and a review note for unusual pages."""
    if guide == "HSG76" and page_number == 140:
        text = clean_page(pdf_page.extract_text(extraction_mode="plain"))
        note = "Rotated table. Check row and column relationships against the PDF."
    else:
        text = clean_page(pdf_page.extract_text(extraction_mode="layout"))
        note = ""

        if not text:
            print(f"Retrying {guide}, page {page_number} in plain mode...")
            text = clean_page(pdf_page.extract_text(extraction_mode="plain"))
            note = "Used plain extraction. Check reading order against the PDF."

    if not text:
        raise ValueError(f"No readable text found in {guide}, page {page_number}.")

    return text, note


def main():
    rows = []
    total_words = 0

    for guide, (first_page, last_page) in GUIDES.items():
        pdf_path = CORPUS / f"{guide.lower()}.pdf"

        if not pdf_path.is_file():
            raise FileNotFoundError(f"Missing PDF: {pdf_path}")

        reader = PdfReader(pdf_path)
        guide_words = 0

        for page_number in range(first_page, last_page + 1):
            # Printed page 1 is at index 0 in these three PDFs.
            pdf_page = reader.pages[page_number - 1]
            text, note = extract_page(pdf_page, guide, page_number)

            guide_words += len(re.findall(r"[A-Za-z]+(?:[-’'][A-Za-z]+)*", text))
            rows.append((guide, page_number, text, note))

        total_words += guide_words
        page_count = last_page - first_page + 1
        print(f"{guide}: {page_count} pages, {guide_words:,} words")

    # Write only after all three guides have been extracted successfully.
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["guide_id", "printed_page", "text", "review_note"])
        writer.writerows(rows)

    print(f"Saved {len(rows)} pages and {total_words:,} words to {OUTPUT.name}")


if __name__ == "__main__":
    main()