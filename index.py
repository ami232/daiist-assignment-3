"""
Assignment 3: build the index (`main.py index`).

Extracts, cleans and chunks the four core EU passenger-rights documents in
corpus/core/, embeds the chunks with Gemini and stores them in ChromaDB under
index/. Two chunking designs are indexed side by side so evaluate.py can
compare them: A (fixed word windows) and B (article/section-aware chunks).

    uv run python main.py index              # embed only chunks without a saved vector
    uv run python index.py --estimate        # count chunks and embeddings, no API calls

The held-out bus regulation (corpus/holdout/) is never indexed here; it is
added later through server.py's add_document tool, which imports
extract_document, chunk_document and embed_and_store from this file.
"""

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
MANIFEST = CORPUS_DIR / "manifest.json"
INDEX_DIR = ROOT / "index"

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSIONS = 768
BATCH_SIZE = 100
PACE_SECONDS = 61  # free tier caps embed requests per minute; wait between batches instead of retrying
RETRY_ATTEMPTS = 5

# The two retrieval designs being compared. Both are stored; evaluate.py measures them.
DESIGNS = {
    "A": {"kind": "window", "size": 200, "overlap": 40},
    "B": {"kind": "structure", "max_words": 450, "min_words": 25},
}
# The design search uses. Chosen from eval/retrieval.json (see REPORT.md -> Retrieval):
# A has higher hit@1 (0.88 vs 0.81), better multi-evidence@3 (5/7 vs 3/7) and smaller
# prompts (627 words at top-3 vs 919). Both designs stay stored so the comparison reruns.
SEARCH_DESIGN = "A"
DESIGN_IS_PROVISIONAL = False

CORE_IDS = ["32004R0261", "52024XC05687", "32021R0782", "32015L2302"]
HOLDOUT_IDS = ["32011R0181"]
REUSE_TERMS = "https://eur-lex.europa.eu/content/legal-notice/legal-notice.html?locale=en"

# Edition facts read from each document's first page and Official Journal header.
DOCUMENTS = {
    "32004R0261": {
        "file": "core/32004R0261.pdf",
        "title": "Regulation (EC) No 261/2004 (air passenger rights)",
        "doc_type": "legislation",
        "published": "2004-02-17",
        "edition": "Original text, OJ L 46, 17.2.2004 (not consolidated)",
        "skip_locations": [],
    },
    "52024XC05687": {
        "file": "core/52024XC05687.pdf",
        "title": "Commission Interpretative Guidelines on Regulation (EC) No 261/2004 (2024)",
        "doc_type": "guidance",
        "published": "2024-09-25",
        "edition": "Commission Notice C/2024/5687, OJ C, 25.9.2024",
        "skip_locations": [],
    },
    "32021R0782": {
        "file": "core/32021R0782.pdf",
        "title": "Regulation (EU) 2021/782 (rail passenger rights)",
        "doc_type": "legislation",
        "published": "2021-05-17",
        "edition": "Original text, OJ L 172, 17.5.2021 (not consolidated)",
        "skip_locations": ["Annex IV"],  # correlation table: lists every article, answers nothing
    },
    "32015L2302": {
        "file": "core/32015L2302.pdf",
        "title": "Directive (EU) 2015/2302 (package travel)",
        "doc_type": "legislation",
        "published": "2015-12-11",
        "edition": "Original text, OJ L 326, 11.12.2015 (not consolidated)",
        "skip_locations": ["Annex III"],  # correlation table
    },
    "32011R0181": {
        "file": "holdout/32011R0181.html",
        "title": "Regulation (EU) No 181/2011 (bus and coach passenger rights)",
        "doc_type": "legislation",
        "published": "2011-02-28",
        "edition": "Original text, OJ L 55, 28.2.2011 (not consolidated)",
        "skip_locations": [],
    },
}

# Running headers and footers. In these PDFs pypdf puts the page's header line
# after its body text and before its footnotes, so it marks where notes start.
HEADER_LINE = re.compile(
    r"^(?:\d{1,2}\.\d{1,2}\.\d{4}\s*L \d+/\d+\s*Official Journal of the European Union\s*EN"
    r"|EN L \d+/\d+ Official Journal of the European Union \d{1,2}\.\d{1,2}\.\d{4}"
    r"|EN \d{1,2}\.\d{1,2}\.\d{4} Official Journal of the European Union L \d+/\d+"
    r"|(?:\d+/\d+ )?ELI: http://data\.europa\.eu/eli/C/\d+/\d+/oj(?: \d+/\d+)?)$"
)
EXTRA_HEADER_LINE = re.compile(r"^(?:EN )?OJ C, \d{1,2}\.\d{1,2}\.\d{4}(?: EN)?$")

# Letter-spacing artefacts in the 2024 guidelines PDF ("air car rier").
SPACING_FIXES = {"car rier": "carrier", "car riage": "carriage", "REGUL ATION": "REGULATION",
                 "LexUriSer v": "LexUriServ", "dela yed": "delayed"}

# Personal names: case references keep their case number and ECLI, not the parties.
CASE_PARTIES = re.compile(r"((?:Joined )?Cases? C-\d+/\d+(?:(?:,| and) C-\d+/\d+)*),\s*[^,]+?\s*,\s*((?:ECLI:)?EU:)")  # one source note reads "ECLI:EU:2009:716"
JUDGMENT_PARTIES = re.compile(r"(Judgment of the Court of Justice of \d{1,2} \w+ \d{4}),.*?,\s*(C-\d+/\d+)")
NAMED_CASES = {r"the\s+Sturgeon\s+case": "the case", r"The\s+Folkerts\s+case": "The case"}
SIGNATURE_KEEP = re.compile(r"^(?:Done at .*|For the .*|The President|\[signatory\])$")


# 1. Corpus files: verify what is on disk against the manifest, download only what is missing.

def load_manifest():
    """The manifest's per-document facts (URLs, checksums), keyed by CELEX id."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return manifest["retrieved_on"], {d["celex"]: d for d in manifest["documents"]}


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ensure_corpus(ids):
    """Make sure each document is on disk with the manifest's checksum."""
    _, manifest = load_manifest()
    for celex in ids:
        path = CORPUS_DIR / DOCUMENTS[celex]["file"]
        if not path.exists():
            print(f"Downloading {celex} from {manifest[celex]['download_url']} ...")
            request = urllib.request.Request(manifest[celex]["download_url"],
                                             headers={"Accept": "application/pdf, text/html"})
            with urllib.request.urlopen(request, timeout=60) as response:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(response.read())
        if file_sha256(path) != manifest[celex]["sha256"]:
            raise SystemExit(f"{path} does not match the manifest checksum. Not indexing a different edition.")


def document_metadata(path):
    """Metadata for a file: the known edition facts if it is one of ours, else what the file says."""
    path = Path(path)
    retrieved_on, manifest = load_manifest()
    source = path.stem.split(".")[0]
    known = DOCUMENTS.get(source, {})
    return {
        "source": source,
        "title": known.get("title", path.stem),
        "doc_type": known.get("doc_type", "unknown"),
        "published": known.get("published", "unknown"),
        "edition": known.get("edition", "unknown"),
        "source_url": manifest.get(source, {}).get("source_url", ""),
        "retrieved_on": retrieved_on if source in manifest else "unknown",
        "reuse_terms": REUSE_TERMS if source in manifest else "unknown",
        "sha256": file_sha256(path),
        "skip_locations": known.get("skip_locations", []),
    }


# 2. Cleaning: page furniture out, footnotes apart, hyphenation and names repaired.

def clean_page(text):
    """Split one PDF page into body lines and footnote lines, without headers."""
    lines = [" ".join(line.split()) for line in text.split("\n")]
    lines = [re.sub(r"\(\s+(\d+)\s+\)", r"(\1)", line) for line in lines]  # rail PDF typesets "( 1 )"
    header_at = [i for i, line in enumerate(lines) if HEADER_LINE.match(line)]
    body, notes = (lines[: header_at[-1]], lines[header_at[-1] + 1:]) if header_at else (lines, [])
    body = [line for line in body if line and not EXTRA_HEADER_LINE.match(line)]
    for wrong, right in SPACING_FIXES.items():
        body = [line.replace(wrong, right) for line in body]
        notes = [line.replace(wrong, right) for line in notes]
    return body, [line for line in notes if line]


def parse_footnotes(note_lines, page):
    """Footnote lines -> {number: {"text", "page"}}. A new note starts with "(n) "."""
    notes, current = {}, None
    for line in note_lines:
        match = re.match(r"^\((\d+)\)\s+(.*)$", line)
        if match:
            current = int(match.group(1))
            notes[current] = {"text": match.group(2), "page": page}
        elif current is not None:
            notes[current]["text"] += " " + line
    return notes


def repair_hyphenation(lines):
    """Join words split across lines ("posi-" + "tions", or a soft hyphen U+00AD).

    Keep the hyphen only when the hyphenated form also appears unbroken in the
    same document ("non-scheduled"); otherwise it was a typesetting break.
    Returns the repaired lines and how many breaks were joined and kept.
    """
    hyphenated = set(re.findall(r"\b\w+-\w+\b", "\n".join(line["text"] for line in lines)))
    lines, joined, kept = [dict(line) for line in lines], 0, 0
    for i in range(len(lines) - 1):
        left = re.search(r"(\w+)(-| ?\xad)$", lines[i]["text"])
        right = re.match(r"^(\w+)(.*)$", lines[i + 1]["text"])
        if not (left and right) or (left.group(2) == "-" and not right.group(1)[0].islower()):
            continue
        if left.group(2) == "-" and f"{left.group(1)}-{right.group(1)}" in hyphenated:
            lines[i]["text"] += right.group(1)
            kept += 1
        else:
            lines[i]["text"] = lines[i]["text"][: left.start(2)] + right.group(1)
            joined += 1
        lines[i + 1]["text"] = right.group(2).strip()
    lines = [{**line, "text": line["text"].replace("\xad", "")} for line in lines]  # stray soft hyphens
    return [line for line in lines if line["text"]], joined, kept


def remove_personal_names(text):
    """Drop party names from case references; case numbers and ECLIs stay for citation."""
    text = CASE_PARTIES.sub(r"\1, \2", text)
    text = JUDGMENT_PARTIES.sub(r"\1, \2", text)
    for named, neutral in NAMED_CASES.items():
        text = re.sub(named, neutral, text)
    return text


# 3. Locations: which article, recital, annex or section each line belongs to.

def tag_legislation(lines):
    """Give each line of an EU act its location: Preamble, Recital (n), Article n, Annex X."""
    tagged, location, zone, next_recital, annex = [], "Preamble", "preamble", 1, None
    titles, pending_title = {}, False
    in_chapter_heading = False
    for line in lines:
        text = line["text"]
        if re.fullmatch(r"CHAPTER [IVX]+", text) or (in_chapter_heading and text.isupper()):
            in_chapter_heading = True  # "CHAPTER IV" and its title
            continue
        in_chapter_heading = False
        recital = re.match(r"^\((\d+)\)\s", text)
        article = re.fullmatch(r"Article (\d+[a-z]?)", text)
        annex_start = re.fullmatch(r"ANNEX ([IVX]+)", text)
        if zone == "preamble" and recital and int(recital.group(1)) == next_recital:
            location, next_recital = f"Recital ({next_recital})", next_recital + 1
        elif text.startswith("HAVE ADOPTED THIS"):
            location, zone = "Preamble", "articles"
        elif annex_start:
            annex, zone = annex_start.group(1), "annex"
            location, pending_title = f"Annex {annex}", True
        elif article and zone in ("articles", "annex"):
            number = article.group(1)
            location = f"Annex {annex}, Article {number}" if zone == "annex" else f"Article {number}"
            pending_title = True
        elif text.startswith("Done at "):
            location, zone = "Signatures", "signatures"
        elif pending_title:
            titles[location], pending_title = text, False
        if zone == "signatures" and not SIGNATURE_KEEP.match(text):
            text = "[signatory]"  # the signatories' names are not needed to answer anything
        tagged.append({**line, "text": text, "location": location})
    for line in tagged:
        title = titles.get(line["location"])
        line["heading"] = f"{line['location']} — {title}" if title else line["location"]
    return tagged


def is_next_section(current, candidate):
    """True if a numbered heading can follow the current one (3.2.6 -> 3.3, 4, or 3.2.7)."""
    if candidate == current + (1,):
        return True
    for depth in range(1, len(current) + 1):
        if candidate == current[: depth - 1] + (current[depth - 1] + 1,):
            return True
    return False


def tag_guidance(lines):
    """Give each line of the guidelines its numbered section; drop the cover and table of contents."""
    tagged, current, location, heading, started = [], (), None, None, False
    for line in lines:
        text = line["text"]
        if not started:
            if text != "1. INTRODUCTION":
                continue  # cover page and table of contents, which match every query
            started = True
        match = re.match(r"^(\d+(?:\.\d+)*)\.\s+([A-Z‘].*)$", text)
        if match:
            number = tuple(int(n) for n in match.group(1).split("."))
            if is_next_section(current, number):
                current = number
                location = f"Section {match.group(1)}"
                heading = f"{location} — {match.group(2)}"
        tagged.append({**line, "location": location, "heading": heading})
    return tagged


# 4. Extraction: PDF and HTML through one interface, returning the same kind of dict.

def extract_pdf(path, doc):
    """Lines (with page and location) and footnotes of an Official Journal PDF."""
    from pypdf import PdfReader

    lines, footnotes = [], {}
    for page_number, page in enumerate(PdfReader(path).pages, start=1):
        body, notes = clean_page(page.extract_text())
        lines += [{"text": text, "page": page_number} for text in body]
        footnotes.update(parse_footnotes(notes, page_number))
    lines, joined, kept = repair_hyphenation(lines)
    lines = [{**line, "text": remove_personal_names(line["text"])} for line in lines]
    tagged = tag_guidance(lines) if doc["doc_type"] == "guidance" else tag_legislation(lines)
    return tagged, footnotes, {"hyphen_breaks_joined": joined, "hyphen_breaks_kept": kept}


def html_location(element):
    """The location of an HTML paragraph, from the nearest EUR-Lex subdivision id."""
    for parent in element.parents:
        ident = parent.get("id") or "" if hasattr(parent, "get") else ""
        if re.fullmatch(r"rct_\d+", ident):
            return f"Recital ({ident[4:]})"
        if re.fullmatch(r"art_\d+[a-z]?", ident):
            return f"Article {ident[4:]}"
        if ident.startswith("anx_"):
            return f"Annex {ident[4:]}"
        if ident.startswith("fnp_"):
            return "Final provisions"
        if ident.startswith(("pbl_", "cit_", "enc_")):
            return "Preamble"
        if ident.startswith(("cpt_", "tis_")):
            return None  # chapter and section headings
    return "Preamble"


def extract_html(path, doc):
    """Lines (with article locations, no pages) and footnotes of a EUR-Lex HTML act."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(Path(path).read_text(encoding="utf-8"), "html.parser")
    lines, footnotes, pending, titles = [], {}, "", {}
    for p in soup.find_all("p"):
        classes = p.get("class") or []
        text = re.sub(r"\(\s*(\*?\d+)\s*\)", r"(\1)", " ".join(p.get_text(" ").split()))
        if not text or "oj-hd-date" in classes or "oj-hd-lg" in classes or "oj-hd-oj" in classes:
            continue
        if "oj-note" in classes:
            match = re.match(r"^\((\d+)\)\s*(.*)$", text)
            if match:
                footnotes[int(match.group(1))] = {"text": remove_personal_names(match.group(2)), "page": None}
            continue
        location = html_location(p)
        if "oj-signatory" in classes and not SIGNATURE_KEEP.match(text):
            text = "[signatory]"
        if "oj-sti-art" in classes:
            titles[location] = text
        if re.fullmatch(r"\([a-z0-9]+\)|\d+\.|—", text):
            pending = text + " "  # a list marker cell: glue it to the cell that follows
            continue
        lines.append({"text": remove_personal_names(pending + text), "page": None, "location": location})
        pending = ""
    for line in lines:
        title = titles.get(line["location"])
        line["heading"] = f"{line['location']} — {title}" if title else line["location"]
    return lines, footnotes, {"hyphen_breaks_joined": 0, "hyphen_breaks_kept": 0}


def extract_document(path):
    """Extract one PDF or HTML file into {metadata..., "lines": [...], "footnotes": {...}}."""
    path = Path(path)
    doc = document_metadata(path)
    if path.suffix.lower() == ".pdf":
        lines, footnotes, repairs = extract_pdf(path, doc)
    elif path.suffix.lower() in (".html", ".htm"):
        lines, footnotes, repairs = extract_html(path, doc)
    else:
        raise ValueError(f"Unsupported file type {path.suffix!r}: only .pdf and .html are indexed.")
    lines = [line for line in lines if line["location"] and line["location"] not in doc["skip_locations"]]
    doc.update({"lines": lines, "footnotes": footnotes, "repairs": repairs})
    doc["words"] = sum(len(line["text"].split()) for line in lines)
    doc["footnote_words"] = sum(len(note["text"].split()) for note in footnotes.values())
    return doc


# 5. Chunking: two designs, never mixing documents.

def notes_for(text, first_page, last_page, footnotes):
    """The footnotes a chunk refers to, so case numbers travel with the sentence citing them."""
    lines = []
    for number in dict.fromkeys(int(n) for n in re.findall(r"(?<=\S )\((\d+)\)", text)):
        note = footnotes.get(number)
        if note and (note["page"] is None or first_page <= note["page"] <= last_page + 1):
            lines.append(f"({number}) {note['text']}")
    return "\nNotes: " + " ".join(lines) if lines else ""


def make_chunk(doc, design, slug, part, lines, prefix=""):
    """One chunk dict from consecutive lines of one document."""
    pages = [line["page"] for line in lines if line["page"] is not None]
    locations = list(dict.fromkeys(line["location"] for line in lines))
    body = prefix + "\n".join(line["text"] for line in lines)
    text = body + notes_for(body, min(pages, default=0), max(pages, default=0), doc["footnotes"])
    chunk = {
        "id": f"{doc['source']}:{design}:{slug}:{part}",
        "source": doc["source"],
        "title": doc["title"],
        "edition": doc["edition"],
        "doc_type": doc["doc_type"],
        "sha256": doc["sha256"],
        "design": design,
        "location": locations[0] if len(locations) == 1 else f"{locations[0]} to {locations[-1]}",
        "locations": " | ".join(locations),
        "heading": lines[0]["heading"],
        "text": remove_personal_names(text),
    }
    if pages:
        chunk["first_page"], chunk["last_page"] = min(pages), max(pages)
    chunk["content_hash"] = hashlib.sha256(chunk["text"].encode()).hexdigest()[:16]
    return chunk


def chunk_windows(doc, size, overlap):
    """Design A: fixed windows of `size` words with `overlap`, like the notebook's chunk_document."""
    words = [(word, line) for line in doc["lines"] for word in line["text"].split()]
    chunks = []
    for n, start in enumerate(range(0, max(len(words) - overlap, 1), size - overlap)):
        window = words[start: start + size]
        lines = []  # regroup the window's words by line so pages and locations stay exact
        for word, line in window:
            if lines and lines[-1]["source_line"] is line:
                lines[-1]["text"] += " " + word
            else:
                lines.append({**line, "text": word, "source_line": line})
        chunks.append(make_chunk(doc, "A", f"w{n:03d}", 1, lines))
    return chunks


def location_slug(location):
    return re.sub(r"[^a-z0-9.]+", "-", location.lower()).strip("-")


def can_split_before(previous, line):
    """Split points for design B: never inside a list, never after a lead-in ending with ':'."""
    if re.match(r"^(\([a-z]+\)|\([ivx]+\)|—|–|-)\s", line["text"]):
        return False  # lettered points and indents stay with the paragraph that introduces them
    if previous["text"].endswith(":"):
        return False
    return bool(re.match(r"^(\d+\.\s|\(\d+\)\s)", line["text"]) or previous["text"].endswith("."))


def chunk_structure(doc, max_words, min_words):
    """Design B: one chunk per article/section; long ones split at paragraph boundaries.

    Consecutive recitals are packed together up to max_words. Every later part
    of a split article repeats its heading, so an exception paragraph (for
    example Article 5(3) of the air regulation) still says which provision it qualifies.
    """
    units = []  # (key, lines): one unit per location, all recitals in one unit
    for line in doc["lines"]:
        key = "Recitals" if line["location"].startswith("Recital") else line["location"]
        if units and units[-1][0] == key:
            units[-1][1].append(line)
        else:
            units.append((key, [line]))
    merged = []  # a bare heading ("2. SCOPE ...") joins the unit after it instead of being a chunk alone
    for key, lines in units:
        if merged and sum(len(line["text"].split()) for line in merged[-1][1]) < min_words:
            lines = merged.pop()[1] + lines  # the unit keeps its own key; the bare heading rides along
        merged.append((key, lines))
    units = merged

    chunks, used_slugs = [], Counter()
    for key, lines in units:
        segments = [[lines[0]]]
        for previous, line in zip(lines, lines[1:]):
            starts_recital = key == "Recitals" and line["location"] != previous["location"]
            if starts_recital or (key != "Recitals" and can_split_before(previous, line)):
                segments.append([line])
            else:
                segments[-1].append(line)
        parts, current = [], []
        for segment in split_long_segments(segments, max_words):
            words = sum(len(line["text"].split()) for line in current + segment)
            if current and words > max_words:
                parts.append(current)
                current = []
            current = current + segment
        parts.append(current)
        for n, part in enumerate(parts, start=1):
            continued = n > 1 and key != "Recitals"
            prefix = f"[{part[0]['heading']}, continued]\n" if continued else ""
            slug = location_slug(key if key != "Recitals" else part[0]["location"])
            used_slugs[slug] += 1  # "Preamble" occurs twice in an act; keep ids unique and stable
            chunks.append(make_chunk(doc, "B", slug, used_slugs[slug], part, prefix))
    return chunks


def split_long_segments(segments, max_words):
    """A paragraph longer than max_words on its own is cut at line boundaries, as a last resort."""
    result = []
    for segment in segments:
        piece, words = [], 0
        for line in segment:
            if piece and words + len(line["text"].split()) > max_words:
                result.append(piece)
                piece, words = [], 0
            piece.append(line)
            words += len(line["text"].split())
        result.append(piece)
    return result


def chunk_document(doc, design):
    """Chunk one extracted document with one of the DESIGNS."""
    settings = DESIGNS[design]
    if settings["kind"] == "window":
        return chunk_windows(doc, settings["size"], settings["overlap"])
    return chunk_structure(doc, settings["max_words"], settings["min_words"])


# 6. Embedding: document and query prefixes as gemini-embedding-2 expects (it has no task_type).

def embedding_text(chunk):
    """The exact text embedded for a chunk: title and location travel with it."""
    return f"title: {chunk['title']} — {chunk['heading']} | text: {chunk['text']}"


def query_text(query):
    return f"task: search result | query: {query}"


def cache_key(text):
    """Same model, size and text -> same vector, so it is never paid for twice."""
    return hashlib.sha256(f"{EMBEDDING_MODEL}|{EMBEDDING_DIMENSIONS}|{text}".encode()).hexdigest()


_client = None


def gemini_client():
    """The Gemini client, created on first use so importing this file costs nothing."""
    global _client
    if _client is None:
        from google import genai
        from google.genai import types

        from api_key import load_api_key

        _client = genai.Client(
            api_key=load_api_key(),
            http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(
                attempts=RETRY_ATTEMPTS, initial_delay=60, max_delay=60, exp_base=1, jitter=0,
                http_status_codes=[429, 500, 502, 503, 504],
            )),
        )
    return _client


def embed_texts(texts):
    """Embed already-prefixed texts in one call. Returns one vector per text."""
    from google.genai import types

    result = gemini_client().models.embed_content(
        model=EMBEDDING_MODEL,
        # One Content per text: a plain list of strings is merged into a single vector.
        contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
        config=types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIMENSIONS),
    )
    vectors = [list(e.values) for e in result.embeddings]
    if len(vectors) != len(texts) or any(len(v) != EMBEDDING_DIMENSIONS for v in vectors):
        raise RuntimeError(f"asked for {len(texts)} embeddings of size {EMBEDDING_DIMENSIONS}, "
                           f"got {len(vectors)}")
    return vectors


# 7. Storage: ChromaDB with our own vectors, and a cache so nothing is embedded twice.

def require_index(index_dir=INDEX_DIR):
    """Stop with a clear message instead of creating an empty database where an index should be."""
    if not (Path(index_dir) / "chroma.sqlite3").exists():
        raise RuntimeError(f"No index in {index_dir}. Run `uv run python main.py index` first.")


def open_index(index_dir=INDEX_DIR):
    import chromadb
    from chromadb.config import Settings

    return chromadb.PersistentClient(path=str(index_dir), settings=Settings(anonymized_telemetry=False))


def get_collection(db, name):
    # embedding_function=None: Chroma must never embed anything itself.
    return db.get_or_create_collection(name=name, configuration={"hnsw": {"space": "cosine"}},
                                       embedding_function=None)


def design_collection(db, design):
    return get_collection(db, f"design_{design.lower()}")


def cached_vectors(cache, keys):
    """The saved vectors among `keys`, as {key: vector}."""
    found = {}
    for start in range(0, len(keys), 500):
        got = cache.get(ids=keys[start: start + 500], include=["embeddings"])
        found.update({k: list(v) for k, v in zip(got["ids"], got["embeddings"])})
    return found


def embed_with_cache(texts, cache, label="texts"):
    """Vectors for `texts`, embedding only those not in `cache` and saving each batch at once.

    Returns (vectors, number newly embedded). If the API fails midway, what was
    saved stays saved and the next run starts where this one stopped.
    """
    keys = [cache_key(t) for t in texts]
    found = cached_vectors(cache, list(dict.fromkeys(keys)))
    missing = list(dict.fromkeys(k for k in keys if k not in found))
    text_of = dict(zip(keys, texts))
    if missing:
        print(f"  embedding {len(missing)} {label} ({len(keys) - len(missing)} reused from cache)", file=sys.stderr)
    for start in range(0, len(missing), BATCH_SIZE):
        if start and PACE_SECONDS:
            time.sleep(PACE_SECONDS)
        batch = missing[start: start + BATCH_SIZE]
        try:
            vectors = embed_texts([text_of[k] for k in batch])
        except Exception as error:
            raise RuntimeError(
                f"embedding stopped after {start} of {len(missing)} new {label} ({type(error).__name__}: "
                f"{error}). Every earlier batch is saved; run again to continue."
            ) from error
        cache.upsert(ids=batch, embeddings=vectors)  # save now: a crash later loses nothing
        found.update(zip(batch, vectors))
        print(f"  saved {min(start + BATCH_SIZE, len(missing))}/{len(missing)}", file=sys.stderr)
    return [found[k] for k in keys], len(missing)


def chunk_metadata(chunk):
    return {k: v for k, v in chunk.items() if k not in ("id", "text")}


def embed_and_store(chunks, collection, cache):
    """Store chunks with their vectors; embeds only chunks whose exact text has no saved vector."""
    if not chunks:
        return 0
    vectors, new = embed_with_cache([embedding_text(c) for c in chunks], cache, "chunks")
    for start in range(0, len(chunks), 500):
        part = chunks[start: start + 500]
        collection.upsert(ids=[c["id"] for c in part], embeddings=vectors[start: start + 500],
                          documents=[c["text"] for c in part], metadatas=[chunk_metadata(c) for c in part])
    return new


def embed_queries(queries, index_dir=INDEX_DIR):
    """Query vectors, reusing saved ones: repeated evaluation questions cost nothing."""
    cache = get_collection(open_index(index_dir), "query_cache")
    vectors, _ = embed_with_cache([query_text(q) for q in queries], cache, "queries")
    return vectors


def indexed_sources(collection):
    """{source: sha256} of every document stored in a collection."""
    got = collection.get(include=["metadatas"])
    return {m["source"]: m["sha256"] for m in got["metadatas"]}


def index_file(path, design=SEARCH_DESIGN, index_dir=INDEX_DIR):
    """Run one file through the whole pipeline into one design's collection.

    The same file twice changes nothing and embeds nothing. A different file
    under an already indexed document id is refused: the index holds fixed
    editions and never mixes two versions of one document.
    """
    require_index(index_dir)
    db = open_index(index_dir)
    collection, cache = design_collection(db, design), get_collection(db, "embedding_cache")
    sha = file_sha256(path)
    source = Path(path).stem.split(".")[0]
    existing = collection.get(where={"source": source}, include=["metadatas"])
    if existing["ids"]:
        old_sha = existing["metadatas"][0]["sha256"]
        if old_sha == sha:
            return {"status": "already_indexed", "source": source, "chunks_added": 0, "embedded": 0,
                    "chunks_for_source": len(existing["ids"])}
        return {"status": "refused_changed_content", "source": source, "chunks_added": 0, "embedded": 0,
                "indexed_sha256": old_sha, "new_sha256": sha}
    doc = extract_document(path)
    chunks = chunk_document(doc, design)
    embedded = embed_and_store(chunks, collection, cache)
    return {"status": "added", "source": source, "title": doc["title"], "chunks_added": len(chunks),
            "embedded": embedded, "words": doc["words"], "design": design}


def search(query, k=5, design=SEARCH_DESIGN, index_dir=INDEX_DIR):
    """The k chunks closest to the query, best first, each with its metadata and score."""
    require_index(index_dir)
    collection = design_collection(open_index(index_dir), design)
    result = collection.query(query_embeddings=embed_queries([query], index_dir), n_results=k,
                              include=["documents", "metadatas", "distances"])
    return [{"id": i, "text": doc, **meta, "score": round(1 - dist, 4)}  # cosine similarity
            for i, doc, meta, dist in zip(result["ids"][0], result["documents"][0],
                                          result["metadatas"][0], result["distances"][0])]


def pages_label(chunk):
    """Where to check a chunk: article/section, plus physical PDF pages for PDFs."""
    if "first_page" not in chunk:
        return chunk["location"]
    first, last = chunk["first_page"], chunk["last_page"]
    return f"{chunk['location']}, PDF p. {first}" if first == last else f"{chunk['location']}, PDF pp. {first}-{last}"


# 8. The index stage.

def build_corpus(ids):
    """Extract every document once and chunk it with every design."""
    docs = [extract_document(CORPUS_DIR / DOCUMENTS[celex]["file"]) for celex in ids]
    chunks = {design: [c for doc in docs for c in chunk_document(doc, design)] for design in DESIGNS}
    return docs, chunks


def print_estimate(docs, chunks, index_dir=INDEX_DIR):
    print(f"{'document':<14}{'words':>8}{'notes':>8}  hyphens joined/kept")
    for doc in docs:
        r = doc["repairs"]
        print(f"{doc['source']:<14}{doc['words']:>8}{doc['footnote_words']:>8}  "
              f"{r['hyphen_breaks_joined']}/{r['hyphen_breaks_kept']}")
    total = sum(d["words"] + d["footnote_words"] for d in docs)
    print(f"total cleaned words (body + footnotes): {total}\n")
    has_index = (index_dir / "chroma.sqlite3").exists()
    cache = get_collection(open_index(index_dir), "embedding_cache") if has_index else None
    for design, design_chunks in chunks.items():
        keys = list(dict.fromkeys(cache_key(embedding_text(c)) for c in design_chunks))
        saved = len(cached_vectors(cache, keys)) if cache else 0
        words = [len(c["text"].split()) for c in design_chunks]
        print(f"design {design} {DESIGNS[design]}: {len(design_chunks)} chunks, "
              f"{sum(words) / len(words):.0f} words on average, {len(keys) - saved} to embed")


def write_corpus_record(docs, chunks, index_dir=INDEX_DIR):
    """index/corpus.json: what was indexed, from which edition, under which terms."""
    record = {
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "designs": DESIGNS,
        "search_design": SEARCH_DESIGN,
        "edition_policy": "Fixed original published editions; not a complete or current-law collection.",
        "documents": [
            {k: doc[k] for k in ("source", "title", "doc_type", "published", "edition", "source_url",
                                 "retrieved_on", "reuse_terms", "sha256", "words", "footnote_words", "repairs")}
            | {"chunks": {d: sum(c["source"] == doc["source"] for c in chunks[d]) for d in DESIGNS}}
            for doc in docs
        ],
    }
    (index_dir / "corpus.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--estimate", action="store_true", help="count chunks and embeddings, call no API")
    args = parser.parse_args()

    ensure_corpus(CORE_IDS)  # the held-out bus regulation is deliberately not indexed here
    docs, chunks = build_corpus(CORE_IDS)
    print_estimate(docs, chunks)
    if args.estimate:
        return

    gemini_client()  # fails now, before index/ is touched, if there is no API key
    INDEX_DIR.mkdir(exist_ok=True)
    db = open_index()
    cache = get_collection(db, "embedding_cache")
    for design, design_chunks in chunks.items():
        collection = design_collection(db, design)
        new = embed_and_store(design_chunks, collection, cache)
        stale = set(collection.get(include=[])["ids"]) - {c["id"] for c in design_chunks}
        if stale:  # chunks from an earlier chunking of the same design
            collection.delete(ids=sorted(stale))
        print(f"design {design}: {collection.count()} chunks stored, {new} newly embedded, {len(stale)} stale removed")
    write_corpus_record(docs, chunks)
    print(f"Index written to {INDEX_DIR}")


if __name__ == "__main__":
    main()
