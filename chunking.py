
import bisect
import hashlib
import json
import re
from pathlib import Path

PROCESSED_DIR = Path("data/processed")

EXPECTED_ARTICLES = {
    "GDPR": 99,
    "DSA": 93,
    "AI_ACT": 113,
}

CHUNK_SIZE = 450
OVERLAP = 40

ARTICLE_PATTERN = re.compile(
    r"(?m)^[ \t]*Article[ \t]+(\d+)[ \t]*$"
)

WORD_PATTERN = re.compile(r"\S+")


def extract_articles(records, source):
    # Combine pages while remembering their positions.
    parts = []
    page_starts = []
    page_numbers = []
    offset = 0

    for record in records:
        page_starts.append(offset)
        page_numbers.append(record["page"])

        part = record["text"] + "\n"
        parts.append(part)
        offset += len(part)

    full_text = "".join(parts)

    def get_page(position):
        index = bisect.bisect_right(
            page_starts, position
        ) - 1
        return page_numbers[max(0, index)]

    # Only accept article headings in numerical order.
    headings = []
    expected_next = 1

    for match in ARTICLE_PATTERN.finditer(full_text):
        number = int(match.group(1))

        if number == expected_next:
            headings.append({
                "article": number,
                "start": match.start(),
            })
            expected_next += 1

        if expected_next > EXPECTED_ARTICLES[source]:
            break

    if len(headings) != EXPECTED_ARTICLES[source]:
        raise ValueError(
            f"{source}: found {len(headings)} articles; "
            f"expected {EXPECTED_ARTICLES[source]}"
        )

    articles = []

    for i, heading in enumerate(headings):
        start = heading["start"]

        if i + 1 < len(headings):
            end = headings[i + 1]["start"]
        else:
            # Stop before the annexes, if present.
            remaining = full_text[start:]
            annex = re.search(
                r"(?m)^[ \t]*ANNEX(?:[ \t]+[IVX]+)?[ \t]*$",
                remaining
            )
            end = (
                start + annex.start()
                if annex
                else len(full_text)
            )

        text = full_text[start:end].strip()

        articles.append({
            "source": source,
            "article": heading["article"],
            "page_start": get_page(start),
            "page_end": get_page(max(start, end - 1)),
            "text": text,
            "_start": start,
        })

    return articles, get_page


def chunk_article(article, get_page):
    text = article["text"]
    words = list(WORD_PATTERN.finditer(text))

    chunks = []
    step = CHUNK_SIZE - OVERLAP

    for start_word in range(0, len(words), step):
        end_word = min(start_word + CHUNK_SIZE, len(words))

        start_char = words[start_word].start()
        end_char = words[end_word - 1].end()

        chunk_text = text[start_char:end_char]

        absolute_start = article["_start"] + start_char
        absolute_end = article["_start"] + end_char - 1

        page_start = get_page(absolute_start)
        page_end = get_page(absolute_end)

        # Stable ID: same content and location = same ID.
        fingerprint = hashlib.sha256(
            (
                f"{article['source']}|"
                f"{article['article']}|"
                f"{start_word}|{chunk_text}"
            ).encode("utf-8")
        ).hexdigest()[:16]

        chunks.append({
            "id": fingerprint,
            "source": article["source"],
            "article": article["article"],
            "page_start": page_start,
            "page_end": page_end,
            "location": f"Article {article['article']}",
            "text": chunk_text,
        })

        if end_word == len(words):
            break

    return chunks


def build_chunks():
    all_chunks = []

    for source in EXPECTED_ARTICLES:
        path = PROCESSED_DIR / f"{source.lower()}.json"

        with path.open(encoding="utf-8") as file:
            records = json.load(file)

        articles, get_page = extract_articles(records, source)

        source_chunks = []

        for article in articles:
            source_chunks.extend(
                chunk_article(article, get_page)
            )

        all_chunks.extend(source_chunks)

        word_count = sum(
            len(article["text"].split())
            for article in articles
        )

        print(
            f"{source}: {len(articles)} articles, "
            f"{word_count:,} words, "
            f"{len(source_chunks)} chunks"
        )

    output = PROCESSED_DIR / "chunks.json"

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(f"\nTOTAL CHUNKS: {len(all_chunks)}")
    print(f"Saved to: {output}")

    if len(all_chunks) > 850:
        print(
            "WARNING: More than 850 chunks. "
            "Review chunk size before embedding."
        )

    return all_chunks


if __name__ == "__main__":
    build_chunks()
