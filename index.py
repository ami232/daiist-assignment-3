import hashlib
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

import httpx
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHUNKS_FILE = INDEX_DIR / "chunks.jsonl"
CHROMA_DIR = INDEX_DIR / "chroma"
DOCUMENTS_FILE = INDEX_DIR / "documents.json"  # doc_id -> title, file hash, chunks
COLLECTION = "corpus"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # Gemini's recommended smaller size; keeps index/ small
EMBED_BATCH = 20  # texts per API call (each text counts towards the daily quota)
EMBED_TEXTS_PER_MINUTE = 90  # stay under the free tier's per-minute limit (about 100 texts)


CORPUS = [
    {
        "doc_id": "food-code-2026",
        "title": "FDA Food Code 2026",
        "url": "https://www.fda.gov/media/194741/download",
        "file": "fda-food-code-2026.pdf",
    },
    {
        "doc_id": "haccp-operators-manual",
        "title": "Managing Food Safety: HACCP Manual for Operators (FDA, 2006)",
        "url": "https://www.fda.gov/media/71976/download",
        "file": "haccp-operators-manual.pdf",
    },
    {
        "doc_id": "haccp-regulators-manual",
        "title": "Managing Food Safety: HACCP Manual for Regulators (FDA, 2006)",
        "url": "https://www.fda.gov/media/72067/download",
        "file": "haccp-regulators-manual.pdf",
    },
]

MAX_WORDS = 350  # a chunk is cut at a line break once it passes this length
MIN_WORDS = 40  # a shorter tail is merged into the chunk before it

# Parts of the Food Code that would only add noise: lists of page numbers,
# a bibliography, and a list of what changed since the last edition.
FOOD_CODE_SKIPPED_PARTS = ("Contents", "Index", "Previous Editions", "Annex 2", "Summary of Changes")

# Acronyms that must stay upper case when the Food Code's *DEFINED TERMS are lowered.
KEEP_UPPER = {"HACCP", "USDA", "FDA", "EPA", "CFR", "ROP", "CIP", "PIC", "U.S.", "PHS"}


# ---------------------------------------------------------------- download


def download_corpus() -> list[Path]:
    """Download each corpus PDF into corpus/ unless it is already there."""
    CORPUS_DIR.mkdir(exist_ok=True)
    paths = []
    for doc in CORPUS:
        path = CORPUS_DIR / doc["file"]
        if not path.exists():
            print(f"Downloading {doc['title']}...", file=sys.stderr)
            response = httpx.get(doc["url"], follow_redirects=True, timeout=120,
                                 headers={"User-Agent": "Mozilla/5.0 (corpus indexer)"})
            response.raise_for_status()
            path.write_bytes(response.content)
        paths.append(path)
    return paths


# ---------------------------------------------------------------- extraction


def extract_pages(path: Path) -> list[str]:
    """The raw text of every page, in order (page 1 is the PDF's first page)."""
    return [page.extract_text() or "" for page in PdfReader(path).pages]


def is_food_code(pages: list[str]) -> bool:
    return any(p.lstrip().startswith("FDA Food Code") for p in pages[:20])


# ---------------------------------------------------------------- cleaning


def split_header(page: str, food_code: bool) -> tuple[str, str, list[str]]:
    """Remove the running header and page number at the top of a page."""
    lines = [line.rstrip() for line in page.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    part, label = "", ""
    if food_code and lines and lines[0].startswith("FDA Food Code"):
        part = re.sub(r"^FDA Food Code \d{4}\s*", "", lines.pop(0)).strip()
    if lines and re.fullmatch(r"\s*[ivxlc\d]+\s*", lines[0]):
        label = lines.pop(0).strip()
    return part, label, lines


def clean_line(line: str) -> str:
    # Degree signs printed as a superscript "o" come out as a letter: 68oC (155oF).
    line = re.sub(r"(\d)\s?[oº]\s?([CF])\b", r"\1°\2", line)
    # Defined terms are written *FOOD, *TIME/TEMPERATURE CONTROL FOR SAFETY FOOD.
    line = re.sub(r"\*([A-Z][A-Z0-9/'’\-]*(?:\s+[A-Z][A-Z0-9/'’\-]*)*)", _lower_defined_term, line)
    line = line.replace("*", "")
    # Priority markers (superscript P and Pf) after a clause: "... 15 seconds for: P".
    line = re.sub(r"(?<=[.,;:)])\s+P[fF]?(?=\s|$)", "", line)
    # Bullets from a symbol font come out as a private-use character.
    line = line.replace("", "•")
    return re.sub(r"\s+", " ", line).strip()


def _lower_defined_term(match: re.Match) -> str:
    words = match.group(1).split()
    return " ".join(w if w in KEEP_UPPER else w.lower() for w in words)


def is_noise(line: str) -> bool:
    """Table-of-contents lines with dot leaders, rules of underscores, and empty lines."""
    return not line or bool(re.search(r"\.{5,}|…{2,}|^_{5,}$", line))


JOINED_WORDS: Counter = Counter()  # every repair made, for checking by hand


def build_vocabulary(all_lines: list[str]) -> Counter:
    return Counter(w.lower() for line in all_lines for w in re.findall(r"[A-Za-z]+", line))


COMMON_WORDS = set("a i an and are as at be by do for in is it of off on or out set so the to up use was way".split())


def is_word(token: str, vocab: Counter) -> bool:
    """A token that is a word by itself: common, or seen at least 5 times in the document."""
    token = token.lower()
    if token in COMMON_WORDS:
        return True
    return len(token) > 1 and vocab[token] >= 5


def fix_split_words(line: str, vocab: Counter) -> tuple[str, int]:
    """Join words that pypdf split in two, such as "specif ic" or "restri cting"."""
    tokens = line.split(" ")
    out, fixes, i = [], 0, 0
    while i < len(tokens):
        a = tokens[i]
        if i + 1 < len(tokens) and a.isalpha() and re.fullmatch(r"[a-z]+[.,;:)]?", tokens[i + 1]):
            b = tokens[i + 1].rstrip(".,;:)")
            joined = (a + b).lower()
            if vocab[joined] >= 2 and not is_word(b, vocab):
                out.append(a + tokens[i + 1])
                JOINED_WORDS[f"{a} {b}"] += 1
                fixes += 1
                i += 2
                continue
        out.append(a)
        i += 1
    return " ".join(out), fixes


# ---------------------------------------------------------------- headings

FC_SECTION = re.compile(r"^(\d-\d{3}\.\d{2})\s+([A-Z].{2,150}?)\.?$")
# "Chapter 1 – Introduction", "Annex 3 - Hazard Analysis", "Annex 4", "Glossary";
# not "Chapter 3." (end of a sentence) nor "Annex 2 of this Manual ..." (a reference).
MANUAL_PART = re.compile(r"^((?:Chapter|Annex)\s+\d+)\s*(?:[–-]\s*([A-Z][^.]*))?$|^(Glossary)$")
MANUAL_SKIPPED_PARTS = ("Paperwork Reduction",)
# Documents without Chapter/Annex lines, such as the Bad Bug Book, use numbered
# headings: "1. Organism", "2. Disease", ... "9. Other Resources". A "1." heading
# starts a new chapter, whose name is the line just before it ("Salmonella species").
NUMBERED_HEADING = re.compile(r"^(\d{1,2})\.\s+([A-Z][A-Za-z /-]{2,40}):?$")


def is_title_case(text: str) -> bool:
    words = [w for w in re.findall(r"[A-Za-z]+", text) if len(w) > 3]
    return bool(words) and sum(w[0].isupper() for w in words) / len(words) >= 0.6


def food_code_heading(line: str) -> str | None:
    """'3-401.11 Raw Animal Foods' for a section heading line, else None."""
    match = FC_SECTION.match(line)
    if match and is_title_case(match.group(2)):
        return f"{match.group(1)} {match.group(2).rstrip('.')}"
    return None


def manual_heading(line: str) -> str | None:
    """An all-capitals line such as 'WHAT ARE THE SEVEN HACCP PRINCIPLES?'."""
    letters = re.sub(r"[^A-Za-z]", "", line)
    if 8 <= len(letters) and letters.isupper() and len(line) <= 90:
        return line.title().replace("Haccp", "HACCP").replace("Ccp", "CCP")
    return None


# ---------------------------------------------------------------- chunking


def chunk_file(path: str | Path, doc_id: str | None = None, title: str | None = None) -> list[dict]:
    """Extract, clean and chunk one PDF. Each chunk carries its source and location."""
    path = Path(path)
    doc_id = doc_id or path.stem.lower()
    title = title or path.stem.replace("-", " ")
    pages = extract_pages(path)
    food_code = is_food_code(pages)

    # 1. Split each page into header and clean lines.
    page_lines: list[tuple[int, str, str, list[str]]] = []
    for number, raw in enumerate(pages, start=1):
        part, label, lines = split_header(raw, food_code)
        cleaned = [clean_line(line) for line in lines]
        page_lines.append((number, part, label, [line for line in cleaned if not is_noise(line)]))

    # 2. Repair words that pypdf split in two, using the document's own vocabulary.
    vocab = build_vocabulary([line for *_, lines in page_lines for line in lines])
    split_word_fixes = 0
    for _, _, _, lines in page_lines:
        for i, line in enumerate(lines):
            lines[i], n = fix_split_words(line, vocab)
            split_word_fixes += n

    # 3. Walk through the lines, starting a new block at each heading.
    blocks: list[dict] = []  # each block: part, section, lines [(page, label, text)]
    part = ""
    has_parts = any(MANUAL_PART.match(line) for *_, lines in page_lines for line in lines)
    for number, page_part, label, lines in page_lines:
        if food_code:
            if page_part:
                part = page_part
            if part.startswith(FOOD_CODE_SKIPPED_PARTS) or not part:
                continue
        for line in lines:
            heading = None
            if food_code:
                heading = food_code_heading(line)
            elif not has_parts:
                numbered = NUMBERED_HEADING.match(line)
                if numbered:
                    heading = f"{numbered.group(1)}. {numbered.group(2).strip().capitalize()}"
                    if numbered.group(1) == "1" and blocks and blocks[-1]["lines"]:
                        # The chapter name is the line just before "1. Organism".
                        part = blocks[-1]["lines"].pop()[2]
            else:
                part_match = MANUAL_PART.match(line)
                if part_match:
                    name, subtitle, glossary = part_match.groups()
                    part = glossary or (f"{name} – {subtitle.strip()}" if subtitle else name)
                    continue
                if not part or any(s in part for s in MANUAL_SKIPPED_PARTS):
                    continue  # cover page and table of contents, or a skipped annex
                heading = manual_heading(line)
            same_part = bool(blocks) and blocks[-1]["part"] == part
            if heading or not same_part:
                section = heading or (blocks[-1]["section"] if same_part else part)
                blocks.append({"part": part, "section": section, "lines": []})
            blocks[-1]["lines"].append((number, label, line))

    # 4. Merge short neighbouring sections of the same part, then cut each
    #    block into chunks of at most about MAX_WORDS words.
    blocks = merge_short_blocks(blocks)
    chunks = []
    for block in blocks:
        for piece in split_block(block["lines"]):
            chunks.append(make_chunk(doc_id, title, block["part"], block["section"], piece))

    print(f"{path.name}: {len(pages)} pages, {len(chunks)} chunks, "
          f"{sum(c['words'] for c in chunks):,} words, {split_word_fixes} split words joined", file=sys.stderr)
    return chunks


def block_words(block: dict) -> int:
    return sum(len(text.split()) for _, _, text in block["lines"])


def merge_short_blocks(blocks: list[dict]) -> list[dict]:
    """Merge a section into the one before it when both fit in MAX_WORDS together."""
    merged: list[dict] = []
    for block in blocks:
        previous = merged[-1] if merged else None
        if (previous and previous["part"] == block["part"]
                and block_words(previous) + block_words(block) <= MAX_WORDS):
            if block["section"] != previous["section"]:
                previous["section"] += "; " + block["section"]
            previous["lines"].extend(block["lines"])
        else:
            merged.append({**block, "lines": list(block["lines"])})
    return merged


def split_block(lines: list[tuple[int, str, str]]) -> list[list[tuple[int, str, str]]]:
    """Group a block's lines into pieces of at most about MAX_WORDS words."""
    pieces, current, words = [], [], 0
    for line in lines:
        current.append(line)
        words += len(line[2].split())
        ends_sentence = line[2].endswith((".", ";", ":"))
        if (words >= MAX_WORDS and ends_sentence) or words >= 1.3 * MAX_WORDS:
            pieces.append(current)
            current, words = [], 0
    if current:
        if pieces and words < MIN_WORDS:
            pieces[-1].extend(current)
        else:
            pieces.append(current)
    return pieces


def join_lines(lines: list[str]) -> str:
    """Join lines into running text, repairing words and references broken at line ends."""
    text = ""
    for line in lines:
        if text.endswith("-") and (line[:1].isdigit() or line[:1].islower()):
            text += line  # "3-" + "401.13" or "Risk-" + "based"
        else:
            text += (" " if text else "") + line
    return text


def make_chunk(doc_id: str, title: str, part: str, section: str, piece: list[tuple[int, str, str]]) -> dict:
    body = join_lines([text for _, _, text in piece])
    context = " > ".join(dict.fromkeys(x for x in (title, part, section) if x))
    text = f"[{context}]\n{body}"
    return {
        "id": f"{doc_id}:{hashlib.sha1(text.encode()).hexdigest()[:12]}",
        "doc_id": doc_id,
        "title": title,
        "part": part,
        "section": section,
        "page_start": piece[0][0],
        "page_end": piece[-1][0],
        "page_label": piece[0][1],
        "words": len(body.split()),
        "text": text,
    }


# ---------------------------------------------------------------- embedding


class DailyQuotaExhausted(RuntimeError):
    """The free tier's daily embedding quota is used up; try again tomorrow."""


_client = None


def gemini_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def document_text(chunk: dict) -> str:
    # gemini-embedding-2 takes the retrieval task inside the text, not as task_type.
    return f"title: {chunk['title']} | text: {chunk['text']}"


def query_text(query: str) -> str:
    return f"task: search result | query: {query}"


_sent: list[tuple[float, int]] = []  # (time, number of texts) of recent calls


def wait_for_rate_limit(n_texts: int) -> None:
    """Sleep until sending n_texts more keeps us under EMBED_TEXTS_PER_MINUTE."""
    while True:
        now = time.monotonic()
        _sent[:] = [(t, n) for t, n in _sent if now - t < 60]
        if sum(n for _, n in _sent) + n_texts <= EMBED_TEXTS_PER_MINUTE:
            _sent.append((now, n_texts))
            return
        time.sleep(60 - (now - _sent[0][0]) + 0.5)


def retry_delay(message: str) -> float:
    """The wait Gemini asks for in a 429 error ("retryDelay": "37s"), else 60 s."""
    match = re.search(r"retryDelay['\"]?:\s*['\"]?(\d+(?:\.\d+)?)s", message)
    return float(match.group(1)) + 1 if match else 60.0


def embed_texts(texts: list[str]) -> list[list[float]]:
    """One vector per text. Waits on the per-minute rate limit, stops on the daily one."""
    from google.genai import errors, types

    # Each text must be its own Content: a plain list of strings would be
    # embedded as a single, combined vector.
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    for attempt in range(10):
        wait_for_rate_limit(len(texts))
        try:
            result = gemini_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Gemini returned {len(vectors)} vectors for {len(texts)} texts")
            return vectors
        except errors.APIError as error:
            message = str(error)
            if error.code == 429 and "PerDay" in message:
                raise DailyQuotaExhausted(message) from error
            if error.code in (429, 500, 503) and attempt < 9:
                wait = retry_delay(message) if error.code == 429 else 2 ** attempt * 5
                if attempt == 0:
                    print(f"  Gemini said: {message[:400]}", file=sys.stderr)
                print(f"  {error.code} from Gemini, waiting {wait:.0f}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def embed_query(query: str) -> list[float]:
    return embed_texts([query_text(query)])[0]


# Food Code Annex 3 ("Public Health Reasons") repeats the heading of almost every
# rule and explains why it exists, so it often outranks the rule itself. Its
# chunks are pushed down by this much cosine similarity; they still come first
# when they match clearly better. Chosen by hit rate in evaluate.py.
ANNEX3_PENALTY = 0.05
SEARCH_POOL = 30  # candidates fetched before re-ranking


def ranked_search(collection, vector: list[float], k: int, where: dict | None = None,
                  annex3_penalty: float = ANNEX3_PENALTY) -> list[dict]:
    """The k best chunks for a query vector, rule text before Annex 3 explanations."""
    result = collection.query(query_embeddings=[vector], n_results=max(k, SEARCH_POOL), where=where,
                              include=["documents", "metadatas", "distances"])
    hits = [{"id": i, "text": t, "meta": m, "score": 1 - d} for i, t, m, d in
            zip(result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0])]
    hits.sort(key=lambda h: h["score"] - annex3_penalty * h["meta"].get("part", "").startswith("Annex 3"),
              reverse=True)
    return hits[:k]


def get_collection():
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(COLLECTION, configuration={"hnsw": {"space": "cosine"}})


def chunk_metadata(chunk: dict) -> dict:
    return {key: chunk[key] for key in
            ("doc_id", "title", "part", "section", "page_start", "page_end", "page_label", "words")}


def embed_and_store(chunks: list[dict], collection=None) -> int:
    """Embed the chunks that have no saved vector yet and store them in ChromaDB."""
    collection = collection or get_collection()
    ids = [c["id"] for c in chunks]
    stored = set(collection.get(ids=ids, include=[])["ids"]) if ids else set()
    missing = [c for c in chunks if c["id"] not in stored]
    if not missing:
        return 0
    print(f"Embedding {len(missing)} new chunks ({len(stored)} already stored)...", file=sys.stderr)
    done = 0
    for start in range(0, len(missing), EMBED_BATCH):
        batch = missing[start:start + EMBED_BATCH]
        vectors = embed_texts([document_text(c) for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[chunk_metadata(c) for c in batch],
        )
        done += len(batch)
        print(f"  {len(stored) + done}/{len(chunks)} stored", file=sys.stderr)
    return done


def remove_stale(chunks: list[dict], collection) -> int:
    """Delete stored corpus chunks that the current chunking no longer produces."""
    current = {c["id"] for c in chunks}
    corpus_ids = [d["doc_id"] for d in CORPUS]
    stored = collection.get(where={"doc_id": {"$in": corpus_ids}}, include=[])["ids"]
    stale = [i for i in stored if i not in current]
    if stale:
        collection.delete(ids=stale)
    return len(stale)


# ---------------------------------------------------------------- document registry


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_documents() -> dict:
    return json.loads(DOCUMENTS_FILE.read_text(encoding="utf-8")) if DOCUMENTS_FILE.exists() else {}


def register_document(doc_id: str, title: str, path: str | Path, n_chunks: int) -> None:
    """Record that a document is fully indexed, with the hash of its file."""
    documents = load_documents()
    documents[doc_id] = {"title": title, "file": Path(path).name,
                         "sha256": file_sha256(path), "chunks": n_chunks}
    INDEX_DIR.mkdir(exist_ok=True)
    DOCUMENTS_FILE.write_text(json.dumps(documents, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def doc_id_for(path: str | Path) -> str:
    """'Bad-Bug-Book-2nd-Edition-(PDF).pdf' -> 'bad-bug-book-2nd-edition-pdf'."""
    return re.sub(r"[^a-z0-9]+", "-", Path(path).stem.lower()).strip("-")


def pdf_title(path: str | Path) -> str:
    """The title stored in the PDF, else one made from the file name."""
    try:
        title = (PdfReader(path).metadata or {}).get("/Title") or ""
    except Exception:  # noqa: BLE001 - a bad metadata block should not stop indexing
        title = ""
    if title and not title.lower().startswith(("microsoft word", "untitled")):
        return title.strip()
    return Path(path).stem.replace("-", " ").replace("_", " ")


# ---------------------------------------------------------------- main


def build_chunks() -> list[dict]:
    chunks = []
    for doc, path in zip(CORPUS, download_corpus()):
        chunks.extend(chunk_file(path, doc["doc_id"], doc["title"]))
    return chunks


def write_chunks(chunks: list[dict]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    with CHUNKS_FILE.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    all_chunks = build_chunks()
    write_chunks(all_chunks)
    sizes = sorted(c["words"] for c in all_chunks)
    print(f"\n{len(all_chunks)} chunks, {sum(sizes):,} words; "
          f"median {sizes[len(sizes) // 2]} words, max {sizes[-1]}. Written to {CHUNKS_FILE.relative_to(ROOT)}.")

    collection = get_collection()
    removed = remove_stale(all_chunks, collection)
    if removed:
        print(f"Removed {removed} stored chunks that the current chunking no longer produces.")
    try:
        embedded = embed_and_store(all_chunks, collection)
    except DailyQuotaExhausted:
        print(f"\nThe daily embedding quota is used up. {collection.count()} chunks are stored; "
              f"run `main.py index` again after the reset (09:00 in Spain) to embed the rest.")
        sys.exit(1)
    for doc in CORPUS:
        n = sum(c["doc_id"] == doc["doc_id"] for c in all_chunks)
        register_document(doc["doc_id"], doc["title"], CORPUS_DIR / doc["file"], n)
    print(f"Embedded {embedded} new chunks. index/chroma holds {collection.count()} chunks.")
