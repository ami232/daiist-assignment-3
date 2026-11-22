"""
Assignment 3: build the index (`uv run python main.py index`).

Reads every PDF in corpus/, cleans it, splits it along its own structure
(GDPR: recitals and articles; EDPB guidelines: numbered sections and paragraphs),
embeds each chunk with Gemini and stores text, citation and vector in index/
(ChromaDB). Vectors are saved batch by batch, and a chunk that already has a
vector is never embedded again.

    uv run python index.py --dry-run          # count chunks and embeddings needed, embed nothing
    uv run python index.py                    # index everything in corpus/ (default design)
    uv run python index.py --design struct120 # second design: smaller chunks, own collection

server.py imports chunk_file, embed_and_store, index_file, get_collection and embed_query.
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
MANIFEST = INDEX_DIR / "sources.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 20

# Retrieval designs: name -> maximum words per chunk. Each design has its own
# ChromaDB collection, so both can live in index/ side by side.
DESIGNS = {"struct250": 250, "struct120": 120}
DEFAULT_DESIGN = "struct250"

SOURCE_TITLES = {
    "gdpr": "GDPR (Regulation (EU) 2016/679)",
    "edpb_consent": "EDPB Guidelines 05/2020 on consent",
    "edpb_breach": "EDPB Guidelines 9/2022 on personal data breach notification",
}


class QuotaExhausted(RuntimeError):
    """The daily embedding quota is used up. Everything embedded so far is saved."""


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# 1. Extract and clean
# --------------------------------------------------------------------------

def read_pages(path: Path) -> list[tuple[int, str]]:
    import logging

    from pypdf import PdfReader

    logging.getLogger("pypdf").setLevel(logging.ERROR)  # silence "SymbolSetEncoding" font warnings
    reader = PdfReader(str(path))
    return [(n, page.extract_text() or "") for n, page in enumerate(reader.pages, 1)]


def is_running_header(line: str) -> bool:
    """Page headers, page numbers and table-of-contents lines carry no content."""
    s = line.strip()
    if re.match(r"^adopted\s+\d+$", s, re.I):  # EDPB running header: "Adopted 11"
        return True
    if "Official Journal of the European Union" in s and re.search(r"L\s*119/\d+", s):
        return True  # EUR-Lex header: "4.5.2016 L 119/12 Official Journal ... EN"
    if re.fullmatch(r"table of contents", s, re.I):
        return True
    if re.search(r"\.{5,}", s):  # dot leaders of a table of contents
        return True
    return False


# Footnotes at the foot of a page would otherwise be glued onto the last paragraph.
FOOT_PAREN = re.compile(
    r"^\(\d{1,3}\)\s+(OJ\b|Position of the European Parliament|Directive|Regulation \(|Council|"
    r"Commission|Decision|Judgment|Opinion|Recommendation|Case\b)"
)


def cut_footnotes(lines: list[str], style: str, expected: int) -> tuple[list[str], int]:
    """Drop the footnote block (everything from its first line to the end of the page)."""
    if style == "paren":
        for i, line in enumerate(lines):
            # A footnote starts "(1) OJ C 229 ...", or "(4) Directive ... (OJ L 281, ...)": it cites the
            # Official Journal within its first lines. A recital that merely opens with "Directive" does not.
            tail = []
            for nxt in lines[i + 1 : i + 5]:
                if re.match(r"^\(\d{1,3}\)\s", nxt.strip()):
                    break  # the next numbered item (footnote or recital) is not part of this one
                tail.append(nxt.strip())
            window = " ".join([line.strip()] + tail)
            if FOOT_PAREN.match(line.strip()) and re.search(r"\(OJ [LC]|\bOJ [LC] \d|not yet published", window):
                return lines[:i], expected
        return lines, expected
    if style == "num":
        for i, line in enumerate(lines):
            m = re.match(r"^(\d{1,3})\s+\S", line.strip())
            if i == 0 or not m or not expected <= int(m.group(1)) <= expected + 2:
                continue
            # Footnotes close the page. A numbered paragraph below this line means it is a heading
            # ("1 Introduction"), not footnote 1.
            if any(re.match(r"^\d{1,3}\.\s+\S", l.strip()) for l in lines[i + 1 :]):
                continue
            for foot in lines[i:]:
                m2 = re.match(r"^(\d{1,3})\s+\S", foot.strip())
                if m2 and expected <= int(m2.group(1)) <= expected + 2:
                    expected = int(m2.group(1)) + 1
            return lines[:i], expected
    return lines, expected


def detect_kind(pages: list[list[str]]) -> str:
    flat = [l.strip() for page in pages for l in page]
    if sum(1 for l in flat if re.fullmatch(r"Article \d+", l)) >= 5:
        return "legislation"
    if sum(1 for l in flat if re.match(r"^\d{1,3}\.\s+\S", l)) >= 20:
        return "guidelines"
    return "plain"


def tidy(text: str) -> str:
    text = text.replace("­", "")
    text = re.sub(r"([a-z])-\s+([a-z])", r"\1\2", text)  # re- + use -> reuse (line-end hyphenation)
    return re.sub(r"\s+", " ", text).strip()


def clean_lines(pages: list[tuple[int, str]]) -> tuple[str, list[tuple[int, str]]]:
    """Return the document kind and its content lines as (page, text)."""
    per_page = [[l for l in text.split("\n") if not is_running_header(l)] for _, text in pages]
    kind = detect_kind(per_page)
    style = {"legislation": "paren", "guidelines": "num"}.get(kind, "")
    expected, out = 1, []
    for (n, _), lines in zip(pages, per_page):
        lines, expected = cut_footnotes(lines, style, expected)
        out += [(n, l.strip()) for l in lines if l.strip()]
    return kind, out


# --------------------------------------------------------------------------
# 2. Parse into blocks along the document's own structure
#    block = {label, heading, group, kind, num, page, text}
#    label is the citation unit: "Article 33", "Recital 87", "Section 3.1.2", "Page 4"
# --------------------------------------------------------------------------

def split_numbered(lines: list[tuple[int, str]], pattern: str):
    """Split lines at sequential numbered starts (1, 2, 3...). Returns [(num or None, lines)]."""
    parts, expected, current = [], 1, None
    for page, text in lines:
        m = re.match(pattern, text)
        if m and int(m.group(1)) == expected:
            expected += 1
            current = (expected - 1, [(page, text)])
            parts.append(current)
        elif current is None:
            current = (None, [(page, text)])
            parts.append(current)
        else:
            current[1].append((page, text))
    return parts


def parse_legislation(lines):
    blocks, recitals_done = [], False
    in_body, expected_recital = False, 1
    chapter, cur, article, skip_next = "", None, None, None

    def flush_recital():
        nonlocal cur
        if cur:
            cur["text"] = tidy(" ".join(t for _, t in cur.pop("lines")))
            blocks.append(cur)
        cur = None

    def flush_article():
        nonlocal article
        if not article:
            return
        parts = split_numbered(article["lines"], r"^(\d{1,3})\.\s+\S")
        word = "paragraph"
        if len(parts) == 1 and parts[0][0] is None:
            parts, word = split_numbered(article["lines"], r"^\((\d{1,3})\)\s+\S"), "point"
        for num, part_lines in parts:
            blocks.append({
                "label": f"Article {article['num']}", "heading": article["title"], "group": chapter,
                "kind": word, "num": num, "page": part_lines[0][0],
                "text": tidy(" ".join(t for _, t in part_lines)),
            })
        article = None

    for page, text in lines:
        if skip_next:  # the title line that follows CHAPTER / Section / Article
            title = text
            if skip_next == "chapter":
                chapter = f"{chapter} - {title}"
            elif skip_next == "article":
                article["title"] = title
            skip_next = None
            continue
        if re.match(r"^Done at (Brussels|Strasbourg)", text):
            break
        if not in_body:
            if re.match(r"^(HAVE|HAS) ADOPTED", text):
                flush_recital()
                in_body = True
                continue
            m = re.match(r"^\((\d{1,3})\)\s+\S", text)
            if m and int(m.group(1)) == expected_recital:
                flush_recital()
                expected_recital += 1
                cur = {"label": f"Recital {m.group(1)}", "heading": "", "group": "Recitals",
                       "kind": "recital", "num": None, "page": page, "lines": [(page, text)]}
            elif cur:
                cur["lines"].append((page, text))
            continue
        m = re.fullmatch(r"CHAPTER ([IVX]+)", text)
        if m:
            flush_article()
            chapter, skip_next = f"Chapter {m.group(1)}", "chapter"
            continue
        if re.fullmatch(r"Section \d+", text):
            flush_article()
            skip_next = "section"
            continue
        m = re.fullmatch(r"Article (\d+)", text)
        if m:
            flush_article()
            article = {"num": m.group(1), "title": "", "lines": []}
            skip_next = "article"
            continue
        if article is not None:
            article["lines"].append((page, text))
    flush_recital()
    flush_article()
    return blocks


ROMAN = {"I": 1, "V": 5, "X": 10}


def roman_to_int(s: str) -> int:
    total = 0
    for i, ch in enumerate(s):
        v = ROMAN[ch]
        total += -v if i + 1 < len(s) and ROMAN[s[i + 1]] > v else v
    return total


def is_next(prev: list[int], new: list[int]) -> bool:
    """Is `new` (3.1.2) the section that follows `prev` in a numbered outline?"""
    if not prev:
        return new in ([0], [1])
    if new == prev + [1]:
        return True
    return any(len(new) == k + 1 and new[:k] == prev[:k] and new[k] == prev[k] + 1 for k in range(len(prev)))


def fix_case(title: str) -> str:
    if title.isupper():
        title = title.title().replace("Gdpr", "GDPR").replace("Eu ", "EU ").replace("Eea", "EEA")
    return title


def parse_guidelines(lines):
    blocks = []
    roman = letter = sub = 0           # sequence counters for I./A./1. style headings
    prev_nums: list[int] = []          # for 3.1.2 style headings
    labels: dict[str, str] = {}        # level -> label part
    titles: list[str] = []
    expected_para = 1
    section = None                     # (label, heading) or None before the first heading
    cur = None

    def flush():
        nonlocal cur
        if cur and section and cur["lines"]:
            cur["text"] = tidy(" ".join(t for _, t in cur["lines"]))
            if cur["text"]:
                blocks.append({k: v for k, v in cur.items() if k != "lines"})
        cur = None

    def start(num, page):
        nonlocal cur
        flush()
        cur = {"label": section[0], "heading": section[1], "group": section[2], "kind": "paragraph",
               "num": num, "page": page, "lines": []}

    def set_section(label_parts, title):
        nonlocal section
        flush()
        label = ".".join(label_parts)
        section = (f"Section {label}", fix_case(title), " > ".join(fix_case(t) for t in titles))

    for page, text in lines:
        s = text.strip()
        m = re.match(r"^(\d{1,3})\.\s+(\S.*)$", s)
        if m and int(m.group(1)) == expected_para and section:
            expected_para += 1
            start(int(m.group(1)), page)
            cur["lines"].append((page, s))
            continue
        m = re.match(r"^([IVX]{1,6})\.\s+([A-Z][A-Z0-9 \-–—,’'()/:]+)$", s)
        if m and roman_to_int(m.group(1)) == roman + 1:
            roman, letter, sub = roman + 1, 0, 0
            labels = {"r": m.group(1)}
            titles = [m.group(2)]
            set_section([m.group(1)], m.group(2))
            continue
        m = re.match(r"^([A-H])\.\s+(\S.{1,100})$", s)
        if m and roman and ord(m.group(1)) - 64 == letter + 1 and not s.endswith("."):
            letter, sub = letter + 1, 0
            labels = {"r": labels.get("r", ""), "l": m.group(1)}
            titles = titles[:1] + [m.group(2)]
            set_section([v for v in (labels["r"], labels["l"]) if v], m.group(2))
            continue
        m = re.match(r"^(\d+(?:\.\d+){0,3})\s+([A-Za-z‘’“][^.]{1,120})$", s)
        if m and len(m.group(2)) <= 80:  # headings are short; a list item or wrapped sentence is not
            nums = [int(x) for x in m.group(1).split(".")]
            if is_next(prev_nums, nums):
                prev_nums = nums
                title = re.sub(r"(?<=[A-Za-z)’”?])\d{1,3}$", "", m.group(2)).strip()  # footnote marker
                titles = titles[: len(nums) - 1] + [title]
                set_section([m.group(1)], title)
                continue
        m = re.match(r"^(\d{1,2})\.\s+([A-Z].{1,75})$", s)
        if m and roman and int(m.group(1)) == sub + 1 and not s.endswith("."):
            sub += 1
            labels["s"] = m.group(1)
            titles = titles[:2] + [m.group(2)]
            set_section([v for v in (labels.get("r"), labels.get("l"), m.group(1)) if v], m.group(2))
            continue
        if section:
            if cur is None:
                start(None, page)
            cur["lines"].append((page, s))
    flush()
    return blocks


def parse_plain(lines):
    """Fallback for documents with no recognisable structure: one section per page."""
    by_page: dict[int, list[str]] = {}
    for page, text in lines:
        by_page.setdefault(page, []).append(text)
    return [
        {"label": f"Page {p}", "heading": "", "group": "", "kind": "page", "num": None, "page": p,
         "text": tidy(" ".join(t))}
        for p, t in by_page.items()
    ]


# --------------------------------------------------------------------------
# 3. Pack blocks into chunks of at most max_words, never across a section
# --------------------------------------------------------------------------

def words(text: str) -> int:
    return len(text.split())


def split_sentences(text: str, max_words: int) -> list[str]:
    sentences = re.split(r"(?<=[.;:?!])\s+(?=[A-Z(‘“'\"0-9])", text)
    parts, current = [], []
    for sentence in sentences:
        if current and words(" ".join(current)) + words(sentence) > max_words:
            parts.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        parts.append(" ".join(current))
    return parts


def pack(blocks: list[dict], max_words: int) -> list[dict]:
    pieces = []  # blocks, with oversize ones split into parts
    for b in blocks:
        parts = split_sentences(b["text"], max_words) if words(b["text"]) > max_words else [b["text"]]
        for i, part in enumerate(parts):
            pieces.append({**b, "text": part, "part": i + 1, "parts": len(parts)})

    groups: list[list[dict]] = []
    for piece in pieces:
        last = groups[-1] if groups else None
        if (last and last[0]["label"] == piece["label"]
                and sum(words(p["text"]) for p in last) + words(piece["text"]) <= max_words):
            last.append(piece)
        else:
            groups.append([piece])

    per_label: dict[str, int] = {}
    for g in groups:
        per_label[g[0]["label"]] = per_label.get(g[0]["label"], 0) + 1
    seen: dict[str, int] = {}

    chunks = []
    for g in groups:
        first = g[0]
        label = first["label"]
        seen[label] = seen.get(label, 0) + 1
        nums = [p["num"] for p in g if p["num"] is not None]
        if per_label[label] == 1:
            location = label
        elif nums:
            word = first["kind"] if first["kind"] in ("paragraph", "point") else "paragraph"
            rng = f"{nums[0]}" if nums[0] == nums[-1] else f"{nums[0]}-{nums[-1]}"
            location = f"{label}, {word}{'s' if nums[0] != nums[-1] else ''} {rng}"
            if len(g) == 1 and first["parts"] > 1:
                location += f" (part {first['part']} of {first['parts']})"
        else:
            location = f"{label} (part {seen[label]} of {per_label[label]})"
        chunks.append({
            "location": location, "section": label, "heading": first["heading"], "group": first["group"],
            "page": min(p["page"] for p in g),
            "text": " ".join(p["text"] for p in g),
        })
    return chunks


# --------------------------------------------------------------------------
# 4. chunk_file: one document -> chunks with citation metadata
# --------------------------------------------------------------------------

def source_name(path) -> str:
    return Path(path).stem


def file_sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def chunk_file(path, design: str = DEFAULT_DESIGN) -> list[dict]:
    path = Path(path)
    source = source_name(path)
    title = SOURCE_TITLES.get(source, source.replace("_", " "))
    kind, lines = clean_lines(read_pages(path))
    parse = {"legislation": parse_legislation, "guidelines": parse_guidelines}.get(kind, parse_plain)
    chunks = pack(parse(lines), DESIGNS[design])
    for i, c in enumerate(chunks):
        context = f"{c['location']} - {c['heading']}" if c["heading"] else c["location"]
        c["source"], c["title"], c["kind"] = source, title, kind
        c["words"] = words(c["text"])
        # What gets embedded carries its own citation, so "Article 33" or "notify" finds it.
        c["embed_text"] = f"{title} | {context}\n{c['text']}"
        sha = hashlib.sha1(c["embed_text"].encode()).hexdigest()[:8]
        c["id"] = f"{source}-{design}-{i:04d}-{sha}"
    return chunks


# --------------------------------------------------------------------------
# 5. Embed and store (ChromaDB in index/)
# --------------------------------------------------------------------------

def get_collection(design: str = DEFAULT_DESIGN):
    import chromadb
    from chromadb.config import Settings

    INDEX_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    # Gemini vectors are unit length, so Chroma's default distance ranks like cosine.
    return client.get_or_create_collection(f"chunks_{design}")


def gemini_client():
    from google import genai

    from api_key import load_api_key

    return genai.Client(api_key=load_api_key())


# Free-tier limits for gemini-embedding-2 (AI Studio > Rate Limit): 100 requests and 30K tokens per minute.
RPM_BUDGET, TPM_BUDGET = 80, 26_000
_sent: list[tuple[float, int]] = []  # (time, estimated tokens) of requests in the last minute


def _pace(tokens: int) -> None:
    """Wait until sending `tokens` more stays inside the per-minute budgets."""
    while True:
        now = time.time()
        while _sent and now - _sent[0][0] > 60:
            _sent.pop(0)
        if len(_sent) < RPM_BUDGET and sum(t for _, t in _sent) + tokens <= TPM_BUDGET:
            break
        time.sleep(1)
    _sent.append((time.time(), tokens))


def embed_one(text: str, client) -> list[float]:
    """One text, one vector. (gemini-embedding-2 merges a list of texts into a single vector.)"""
    _pace(len(text) // 4 + 1)
    delay = 5
    for attempt in range(6):
        try:
            response = client.models.embed_content(model=EMBED_MODEL, contents=text)
            return list(response.embeddings[0].values)
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "PerDay" in message or "per day" in message.lower():
                raise QuotaExhausted(message) from error
            if ("429" in message or "RESOURCE_EXHAUSTED" in message or "503" in message) and attempt < 5:
                log(f"  rate limited, waiting {delay}s ...")
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


def embed_texts(texts: list[str], client=None) -> list[list[float]]:
    client = client or gemini_client()
    return [embed_one(t, client) for t in texts]


def embed_query(text: str, client=None) -> list[float]:
    return embed_texts([text], client)[0]


def embed_and_store(chunks: list[dict], design: str = DEFAULT_DESIGN, client=None) -> tuple[int, int]:
    """Embed the chunks that have no saved vector and store them. Returns (embedded, skipped)."""
    collection = get_collection(design)
    have = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in have]
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i : i + EMBED_BATCH]
        vectors = embed_texts([c["embed_text"] for c in batch], client)
        collection.add(  # saved to disk now: a crash or the daily limit loses nothing
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[
                {"source": c["source"], "title": c["title"], "location": c["location"], "section": c["section"],
                 "heading": c["heading"], "group": c["group"], "page": c["page"], "words": c["words"]}
                for c in batch
            ],
        )
        done += len(batch)
        log(f"  embedded {done}/{len(todo)}")
    return done, len(chunks) - len(todo)


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.is_file() else {}


def save_manifest(manifest: dict) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def index_file(path, design: str = DEFAULT_DESIGN, client=None) -> str:
    """Index one document. Same file already indexed: skipped. Same name, new content: replaced."""
    path = Path(path)
    if not path.is_file():
        return f"File not found: {path}"
    source, sha = source_name(path), file_sha(path)
    manifest = load_manifest()
    key = f"{design}:{source}"
    if manifest.get(key, {}).get("sha256") == sha:
        return f"{source}: already indexed ({manifest[key]['chunks']} chunks), nothing to do."
    chunks = chunk_file(path, design)
    if not chunks:
        return f"{source}: no text could be extracted from this file."
    status = "added"
    if key in manifest:  # same name, different content: drop the old chunks first
        get_collection(design).delete(where={"source": source})
        status = "replaced (the content changed)"
    embedded, reused = embed_and_store(chunks, design, client)
    manifest[key] = {"sha256": sha, "chunks": len(chunks)}
    save_manifest(manifest)
    return f"{source}: {status}, {len(chunks)} chunks ({embedded} embedded, {reused} already had a vector)."


# --------------------------------------------------------------------------
# main.py index
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Build the index from corpus/.")
    parser.add_argument("--design", choices=sorted(DESIGNS), default=DEFAULT_DESIGN)
    parser.add_argument("--dry-run", action="store_true", help="count chunks and embeddings needed; embed nothing")
    args = parser.parse_args()

    files = sorted(CORPUS_DIR.glob("*.pdf"))
    if not files:
        log(f"No PDFs in {CORPUS_DIR}. Put the corpus there first.")
        return 1

    if args.dry_run:
        collection = get_collection(args.design)
        total_new = 0
        print(f"Design {args.design} (max {DESIGNS[args.design]} words per chunk)\n")
        for f in files:
            chunks = chunk_file(f, args.design)
            have = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
            new = len(chunks) - len(have)
            total_new += new
            avg = sum(c["words"] for c in chunks) / max(len(chunks), 1)
            print(f"{f.name:22} {len(chunks):4} chunks, {avg:5.0f} words on average, {new:4} still to embed")
        print(f"\nEmbeddings needed now: {total_new}. Free tier: about 1,000 a day (check https://ai.dev/rate-limit).")
        return 0

    for f in files:
        print(index_file(f, args.design))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except QuotaExhausted:
        log("\nDaily embedding quota used up. Everything embedded so far is saved: run the same "
            "command again after 09:00 (Spain) and it continues where it stopped.")
        raise SystemExit(1)
