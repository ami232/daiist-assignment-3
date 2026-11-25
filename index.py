"""
Assignment 3: build the index (`main.py index`).

Downloads six public-domain National Weather Service documents into corpus/,
extracts and cleans the text page by page, chunks it by numbered section,
embeds every chunk with Gemini and stores it in ChromaDB under index/.
(The two retrieval designs compared in evaluate.py, vector and hybrid search,
share these chunks, so the corpus is embedded only once.)

Each vector is saved as soon as it comes back, and only chunks without a
saved vector are embedded, so a crash or the daily quota loses nothing.
server.py imports chunk_file() and embed_and_store() for add_document.
"""

import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import chromadb
import httpx
from google import genai
from google.genai import types
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CONFIG_FILE = INDEX_DIR / "config.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors keep index/ small; plenty for ~1,000 chunks
BATCH_SIZE = 20

SECTION_MAX_WORDS = 300  # longer sections are split into parts of this size
SECTION_MIN_WORDS = 30   # shorter sections (a heading and one line) are merged into the next one

DESIGNS = ["sections"]   # chunking designs that get embedded

# source id -> (title, date, url). The source id is what citations and eval/questions.csv use.
DOCUMENTS = {
    "NWSI-10-513": ("NWS Instruction 10-513, WFO Winter Weather Products Specification", "2024-11-06",
                    "https://www.weather.gov/media/directives/010_pdfs/pd01005013curr.pdf"),
    "NWSI-10-514": ("NWS Instruction 10-514, National Winter Weather Products Specification", "2025-03-18",
                    "https://www.weather.gov/media/directives/010_pdfs/pd01005014curr.pdf"),
    "NWSI-10-515": ("NWS Instruction 10-515, WFO Non-Precipitation Weather Products Specification", "2025-05-16",
                    "https://www.weather.gov/media/directives/010_pdfs/pd01005015curr.pdf"),
    "NWSI-10-1605": ("NWS Instruction 10-1605, Storm Data Preparation", "2021-07-26",
                     "https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf"),
    "WinterStorms-2008": ("Winter Storms: The Deceptive Killers (NWS/FEMA/Red Cross preparedness guide)", "2008-06",
                          "https://www.weather.gov/media/safety/Winter_Storms2008.pdf"),
    "WSSI-Guide-2025": ("The Winter Storm Severity Index: A Guide for Users (NWS Weather Prediction Center)", "2025",
                        "https://origin-east-www-wpc.woc.noaa.gov/wwd/wssi/WSSI_user_guide_2025.pdf"),
}


def log(*args) -> None:
    """Log to stderr: server.py imports this module and its stdout carries MCP messages."""
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- download

def download_corpus() -> list[Path]:
    CORPUS_DIR.mkdir(exist_ok=True)
    paths = []
    for source, (_, _, url) in DOCUMENTS.items():
        path = CORPUS_DIR / f"{source}.pdf"
        if not path.exists():
            log(f"Downloading {source} ...")
            response = httpx.get(url, follow_redirects=True, timeout=120)
            response.raise_for_status()
            path.write_bytes(response.content)
        paths.append(path)
    return paths


# ---------------------------------------------------------------- extract and clean

DROP_LINE = [
    re.compile(r"^NWSI \d+-\d+ [A-Z]+ \d{1,2}, \d{4}$"),          # running page header
    re.compile(r"^(A-|[A-Z]-)?\d{1,3}$"),                          # page numbers (12, A-4)
    re.compile(r"\.{5,}|…{2,}"),                                   # table-of-contents dot leaders
    re.compile(r"^Website: https://www\.wpc\.ncep\.noaa\.gov"),    # repeated slide footer
    re.compile(r"^(OPR|Certified by|Contact|WSSI Project Lead)\b"),  # staff names
    re.compile(r"Digitally signed by|^Date: \d{4}\.\d\d\.\d\d|^[A-Z]+\.[A-Z]+\.[A-Z]+\.\d+"),  # signature block
    re.compile(r"^(Director|Date|[A-Z][a-z]+ [A-Z][a-z]+ Date)$"),
    re.compile(r"\.indd \d+ \d+/\d+/\d{4}"),                       # printer slug in the 2008 guide
]
EMAIL = re.compile(r"\S+@\S+\.\w+")
# "6.3.2 Issuance Criteria", "3 Blizzard (Z). A winter storm ..." (Storm Data event types)
HEADING = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,3})\.?\s+([A-Z][A-Za-z/&,()'’ -]{2,80}?)(?:\.\s|$)")


def clean_text(text: str) -> str:
    """Fix what pypdf gets wrong in these PDFs."""
    text = unicodedata.normalize("NFKC", text)           # ligatures: "ﬁ" -> "fi"
    text = re.sub(r"(fi|fl|ff) (?=[a-z])", r"\1", text)  # the guide's "ofﬁ ce" -> "office"
    text = text.replace("​", "").replace("ϒ", "•")
    text = EMAIL.sub("[email removed]", text)            # no personal data in the index
    return text


def extract_lines(path: Path) -> list[tuple[int, str, str]]:
    """Return (page, section, line) for every kept line of a PDF, TXT or MD file.

    The section is the last numbered heading seen (e.g. "6.3"); in appendices it
    is "App-D" for Appendix D, and "App-A-3" for item 3 of Appendix A (Blizzard in Storm Data).
    Documents without numbered headings get the section "p<page>".
    """
    if path.suffix.lower() == ".pdf":
        pages = [page.extract_text() or "" for page in PdfReader(path).pages]
    else:
        pages = [path.read_text(encoding="utf-8", errors="replace")]

    rows, section, appendix = [], "", ""
    for page_no, raw in enumerate(pages, start=1):
        for line in clean_text(raw).splitlines():
            line = " ".join(line.split())
            if not line or any(p.search(line) for p in DROP_LINE):
                continue
            appendix_match = re.match(r"^APPENDIX ([A-Z])\b", line)
            heading = HEADING.match(line)
            if appendix_match:
                appendix = appendix_match.group(1)
                section = f"App-{appendix}"
            elif heading and len(heading.group(2).split()) <= 10:
                number = heading.group(1)
                section = f"App-{appendix}-{number}" if appendix else number
            rows.append((page_no, section or f"p{page_no}", line))
    return rows


def source_id(path: Path) -> str:
    return Path(path).stem


# ---------------------------------------------------------------- chunk

def make_chunk(source: str, design: str, words: list[tuple[int, str, str]]) -> dict:
    text = " ".join(w for _, _, w in words)
    text = re.sub(r"(\w)- (\w)", r"\1\2", text)  # words hyphenated across lines
    pages = sorted({p for p, _, _ in words})
    sections = list(dict.fromkeys(s for _, s, _ in words))
    numbered = not sections[0].startswith("p")
    page_text = f"p. {pages[0]}" if pages[0] == pages[-1] else f"pp. {pages[0]}-{pages[-1]}"
    citation = f"{source}, section {sections[0]}, {page_text}" if numbered else f"{source}, {page_text}"
    return {
        "id": hashlib.sha1(f"{design}|{source}|{text}".encode()).hexdigest()[:16],
        "text": text,
        "source": source,
        "title": DOCUMENTS.get(source, (source,))[0],
        "page": pages[0],
        "pages": "|" + "|".join(map(str, pages)) + "|",
        "section": sections[0],
        "sections": "|" + "|".join(sections) + "|",
        "citation": citation,
        "design": design,
        "words": len(text.split()),
    }


def to_words(rows):
    return [(p, s, w) for p, s, line in rows for w in line.split()]


def chunk_sections(source: str, rows) -> list[dict]:
    """One chunk per numbered section (or per page when there are none).

    Long sections are cut into parts of SECTION_MAX_WORDS words; very short ones
    (a heading with one line) are merged into the next section.
    """
    groups, current = [], []
    for row in rows:
        if current and row[1] != current[-1][1] and len(to_words(current)) >= SECTION_MIN_WORDS:
            groups.append(current)
            current = []
        current.append(row)
    if current:
        groups.append(current)

    chunks = []
    for group in groups:
        words = to_words(group)
        for i in range(0, len(words), SECTION_MAX_WORDS):
            chunks.append(make_chunk(source, "sections", words[i:i + SECTION_MAX_WORDS]))
    return chunks


def chunk_file(path: Path, design: str = "sections") -> list[dict]:
    rows = extract_lines(Path(path))
    if not rows:
        raise ValueError(f"No text could be extracted from {path}")
    return chunk_sections(source_id(path), rows)


# ---------------------------------------------------------------- embed and store

_client = None


def gemini() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch, waiting and retrying when the free tier says slow down."""
    for attempt in range(8):
        try:
            result = gemini().models.embed_content(
                model=EMBED_MODEL,
                # one Content per text: a plain list would be embedded as ONE multi-part input
                contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM),
            )
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if ("429" not in message and "RESOURCE_EXHAUSTED" not in message) or attempt == 7:
                raise
            if "PerDay" in message:
                raise RuntimeError("Daily embedding quota used up. Run again after 09:00 (Spain).") from error
            wait = 15 * (attempt + 1)
            log(f"Rate limited, waiting {wait}s ...")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def embed_query(query: str) -> list[float]:
    return embed([query], task="RETRIEVAL_QUERY")[0]


def collection(design: str):
    client = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"))
    return client.get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed only the chunks without a saved vector, saving each batch at once."""
    store = collection(design)
    existing = set(store.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), BATCH_SIZE):
        batch = todo[i:i + BATCH_SIZE]
        vectors = embed([c["text"] for c in batch])
        store.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: v for k, v in c.items() if k not in ("id", "text")} for c in batch],
        )
        log(f"  [{design}] saved {min(i + BATCH_SIZE, len(todo))}/{len(todo)} new vectors")
    return len(todo)


def chosen_design() -> str:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())["design"]
    return "sections"


def main() -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    paths = download_corpus()
    stats = {}
    for design in DESIGNS:
        all_chunks = []
        for path in paths:
            chunks = chunk_file(path, design)
            all_chunks += chunks
            stats.setdefault(design, {})[path.stem] = {"chunks": len(chunks), "words": sum(c["words"] for c in chunks)}
        log(f"{design}: {len(all_chunks)} chunks, {sum(c['words'] for c in all_chunks)} words")
        (INDEX_DIR / f"chunks_{design}.jsonl").write_text(
            "\n".join(json.dumps(c, ensure_ascii=False) for c in all_chunks) + "\n", encoding="utf-8"
        )
        added = embed_and_store(all_chunks, design)
        log(f"{design}: embedded {added} new chunks, {len(all_chunks) - added} already saved")
    (INDEX_DIR / "stats.json").write_text(json.dumps(stats, indent=2))
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps({"design": "sections"}, indent=2))
    print(f"Index ready in {INDEX_DIR.relative_to(ROOT)}/ (search uses design: {chosen_design()})")


if __name__ == "__main__":
    main()
