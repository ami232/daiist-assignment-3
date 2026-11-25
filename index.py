import re
import sys
import time
from pathlib import Path

import chromadb
import httpx
import pandas as pd
from google import genai
from google.genai import errors, types

from api_key import load_api_key

CORPUS = Path("corpus")
INDEX = Path("index")
GUTENBERG = "https://www.gutenberg.org/cache/epub/{0}/pg{0}.txt"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # keeps index small
BATCH = 20  # saved after each batch

DESIGNS = ["paragraph", "fixed"]
MIN_WORDS = 80
MAX_WORDS = 300
FIXED_WORDS = 150

SOURCES = [
    {
        "id": "mill-on-liberty",
        "author": "John Stuart Mill",
        "work": "On Liberty",
        "year": 1859,
        "part": "Chapters I-II",
        "edition": "Walter Scott Publishing Co., with an introduction by W. L. Courtney (left out)",
        "gutenberg": 34901,
        "start": r"CHAPTER I\.",
        "end": r"CHAPTER III\.",
    },
    {
        "id": "marx-engels-manifesto",
        "author": "Karl Marx and Friedrich Engels",
        "work": "Manifesto of the Communist Party",
        "year": 1848,
        "part": "Preamble",
        "edition": "English edition of 1888, translated by Samuel Moore, edited by Engels",
        "gutenberg": 61,
        "start": r"A spectre is haunting Europe.*",
        "end": None,
    },
    {
        "id": "paine-agrarian-justice",
        "author": "Thomas Paine",
        "work": "Agrarian Justice",
        "year": 1797,
        "part": "Full text",
        "edition": "The Writings of Thomas Paine, vol. III, ed. M. D. Conway, Putnam 1895 (editor's note left out)",
        "gutenberg": 31271,
        "start": r"AUTHOR'S INSCRIPTION\.",
        "end": r"XXIX\. THE EIGHTEENTH FRUCTIDOR\.",
    },
    {
        "id": "bastiat-seen-unseen",
        "author": "Frédéric Bastiat",
        "work": "That Which Is Seen, and That Which Is Not Seen",
        "year": 1850,
        "part": "Introduction",
        "edition": "Essays on Political Economy, 3rd (People's) edition, Putnam 1874",
        "gutenberg": 15962,
        "start": r"That Which Is Seen, and That Which Is Not Seen",
        "end": r"Government\.",
    },
    {
        "id": "smith-wealth-b1c2",
        "author": "Adam Smith",
        "work": "The Wealth of Nations",
        "year": 1776,
        "part": "Book I, Chapter II",
        "edition": "Project Gutenberg #3300",
        "gutenberg": 3300,
        "start": r"This division of labour, from which so many advantages are derived, is not",
        "end": r"CHAPTER III\.",
    },
    {
        "id": "smith-wealth-b4c2",
        "author": "Adam Smith",
        "work": "The Wealth of Nations",
        "year": 1776,
        "part": "Book IV, Chapter II",
        "edition": "Project Gutenberg #3300",
        "gutenberg": 3300,
        "start": r"By restraining, either by high duties, or by absolute prohibitions, the",
        "end": r"CHAPTER III\.",
    },
    # held back for add_document
    {
        "id": "bastiat-government",
        "author": "Frédéric Bastiat",
        "work": "Government",
        "year": 1848,
        "part": "Full essay",
        "edition": "Essays on Political Economy, 3rd (People's) edition, Putnam 1874",
        "gutenberg": 15962,
        "start": r"Government\.",
        "end": r"What Is Money\?",
        "held_back": True,
    },
]


def download(gutenberg_id):
    path = CORPUS / "gutenberg" / f"pg{gutenberg_id}.txt"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        response = httpx.get(GUTENBERG.format(gutenberg_id), follow_redirects=True, timeout=60)
        response.raise_for_status()
        path.write_text(response.text, encoding="utf-8")
    return path.read_text(encoding="utf-8").splitlines()


def extract(source):
    lines = [line.strip() for line in download(source["gutenberg"])]
    first = next(i for i, line in enumerate(lines) if line.startswith("*** START OF"))
    last = next(i for i, line in enumerate(lines) if line.startswith("*** END OF"))
    start = max(i for i in range(first, last) if re.fullmatch(source["start"], lines[i]))  # last match skips contents
    end = next((i for i in range(start + 1, last) if source["end"] and re.fullmatch(source["end"], lines[i])), last)
    return "\n".join(lines[start:end])


def is_heading(text):
    capitals = text.isupper() and len(text.split()) <= 25 and not text.endswith("!")  # "UNITE!" is text
    return capitals or bool(re.match(r"[IVX]+\.--|_[A-C]\. .+_$", text))


def is_footnote(text):
    return text == "FOOTNOTES:" or bool(re.match(r"\[(\d+|Illustration)|\* ", text))


def paragraphs(text, first_section):
    rows, section, after_heading = [], first_section, False
    for block in re.split(r"\n\s*\n", text):
        block = " ".join(block.split())
        if not block or is_footnote(block):
            continue
        if is_heading(block):
            name = block.strip("_.,: ")
            section = f"{section}. {name}" if after_heading else name
            after_heading = True
            continue
        after_heading = False
        block = re.sub(r"\[\d+\]", "", block).replace("_", "")  # drop footnote marks, italics
        rows.append({"section": section, "paragraph": len(rows) + 1, "text": block})
    return rows


def source_of(path):
    stem = Path(path).stem
    known = {source["id"]: source for source in SOURCES}
    return known.get(stem, {"id": stem, "author": "unknown", "work": stem, "year": 0, "part": "Full text", "edition": "unknown"})


def make_chunk(source, paras, text, suffix=""):
    first, last = paras[0]["paragraph"], paras[-1]["paragraph"]
    return {
        "id": f"{source['id']}-p{first}{suffix}",
        "text": text,
        "source": source["id"],
        "author": source["author"],
        "work": source["work"],
        "year": source["year"],
        "edition": source["edition"],
        "section": paras[0]["section"],
        "para_start": first,
        "para_end": last,
        "location": f"{paras[0]['section']}, ¶{first}" + (f"-{last}" if last > first else ""),
    }


def words_in(group):
    return sum(len(r["text"].split()) for r in group)


def paragraph_chunks(source, rows):
    groups = []
    for row in rows:
        if groups and groups[-1][0]["section"] == row["section"] and words_in(groups[-1]) < MIN_WORDS:
            groups[-1].append(row)
        else:
            groups.append([row])
    # short section ends join previous
    for i in range(len(groups) - 1, 0, -1):
        if words_in(groups[i]) < MIN_WORDS and groups[i][0]["section"] == groups[i - 1][0]["section"]:
            groups[i - 1] += groups.pop(i)
    chunks = []
    for group in groups:
        words = " ".join(r["text"] for r in group).split()
        parts = -(-len(words) // MAX_WORDS)  # rounded up
        size = -(-len(words) // parts)
        for k in range(parts):
            suffix = f"-{k + 1}" if parts > 1 else ""
            chunks.append(make_chunk(source, group, " ".join(words[k * size:(k + 1) * size]), suffix))
    return chunks


def fixed_chunks(source, rows):
    chunks = []
    for section in dict.fromkeys(r["section"] for r in rows):
        words = [(word, r) for r in rows if r["section"] == section for word in r["text"].split()]
        starts = list(range(0, len(words), FIXED_WORDS))
        # short last window joins previous
        if len(starts) > 1 and len(words) - starts[-1] < FIXED_WORDS // 3:
            starts.pop()
        for i, start in enumerate(starts):
            end = starts[i + 1] if i + 1 < len(starts) else len(words)
            window = words[start:end]
            paras = list({id(r): r for _, r in window}.values())
            chunks.append(make_chunk(source, paras, " ".join(w for w, _ in window), f"-w{start}"))
    return chunks


def chunk_file(path, design):
    source = source_of(path)
    rows = paragraphs(Path(path).read_text(encoding="utf-8"), source["part"])
    return paragraph_chunks(source, rows) if design == "paragraph" else fixed_chunks(source, rows)


def log(message):
    print(message, file=sys.stderr, flush=True)  # stdout carries MCP messages


def embed(texts, task):
    client = genai.Client(api_key=load_api_key())
    config = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    contents = [types.Content(parts=[types.Part(text=text)]) for text in texts]  # one vector per text
    for attempt in range(5):
        try:
            result = client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            assert len(vectors) == len(texts), f"{len(texts)} texts but {len(vectors)} vectors"
            return vectors
        except errors.ClientError as error:
            # 429 = rate limit, wait
            if error.code != 429:
                raise
            log("Gemini rate limit, waiting 60 s")
            time.sleep(60)
    raise SystemExit("Still rate limited, so the daily quota is probably used up. Saved vectors are kept; run again after 09:00 Spain time.")


def collection(design):
    client = chromadb.PersistentClient(path=str(INDEX), settings=chromadb.Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(design, configuration={"hnsw": {"space": "cosine"}}, embedding_function=None)


def embed_and_store(chunks, design):
    store = collection(design)
    saved = set(store.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in saved]  # never embed twice
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        store.add(
            ids=[c["id"] for c in batch],
            embeddings=embed([c["text"] for c in batch], "RETRIEVAL_DOCUMENT"),
            documents=[c["text"] for c in batch],
            metadatas=[{k: v for k, v in c.items() if k not in ("id", "text")} for c in batch],
        )
        log(f"{design}: saved {min(i + BATCH, len(todo))}/{len(todo)} new vectors")
    return len(todo)


def main():
    for source in SOURCES:
        (CORPUS / f"{source['id']}.txt").write_text(extract(source), encoding="utf-8")
    files = [CORPUS / f"{s['id']}.txt" for s in SOURCES if not s.get("held_back")]

    rows = [{"source": f.stem, **row} for f in files for row in paragraphs(f.read_text(encoding="utf-8"), source_of(f)["part"])]
    pd.DataFrame(rows).to_csv(CORPUS / "paragraphs.csv", index=False)

    for design in DESIGNS:
        chunks = [chunk for f in files for chunk in chunk_file(f, design)]
        words = pd.Series([len(c["text"].split()) for c in chunks])
        print(f"{design:9s} {len(chunks):4d} chunks, words per chunk: median {words.median():.0f}, min {words.min()}, max {words.max()}")
        new = embed_and_store(chunks, design)
        print(f"{design:9s} {new} chunks embedded now, {collection(design).count()} in index/")


if __name__ == "__main__":
    main()
