"""Assignment 3: build the index (`main.py index`).

Downloads the corpus into corpus/, extracts and chunks it with two designs
(structure-based and fixed windows), embeds every chunk with Gemini and saves
the vectors in index/. Only chunks without a saved vector are embedded.
The functions chunk_file, embed_and_store and add_to_index are imported by server.py.
"""

import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
VECTORS_FILE = INDEX_DIR / "vectors.jsonl"
CONFIG_FILE = INDEX_DIR / "config.json"
EMBED_MODEL = "gemini-embedding-2"
BATCH_SIZE = 10
DESIGNS = ("structure", "fixed")
STRUCT_MAX_WORDS = 300
RECITAL_GROUP_WORDS = 200
FIXED_WORDS = 400
FIXED_OVERLAP = 50

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}
EDPB = "https://www.edpb.europa.eu"
SOURCES = {
    "GDPR": {
        "file": "GDPR.html",
        "urls": ["https://publications.europa.eu/resource/celex/32016R0679"],
    },
    "EDPB-05-2020-consent": {
        "file": "EDPB-05-2020-consent.pdf",
        "urls": [
            EDPB + "/system/files/2021-05/edpb_guidelines_202005_consent_en.pdf",
            EDPB + "/system/files/documents/files/file1/edpb_guidelines_202005_consent_en.pdf",
        ],
        "page": EDPB + "/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en",
        "hint": "202005_consent",
    },
    "EDPB-09-2022-breach-notification": {
        "file": "EDPB-09-2022-breach-notification.pdf",
        "urls": [
            EDPB + "/system/files/documents/2023-04/edpb_guidelines_202209_personal_data_breach_notification_v2.0_en.pdf",
            EDPB + "/system/files/2023-04/edpb_guidelines_202209_personal_data_breach_notification_v2.0_en.pdf",
        ],
        "page": EDPB + "/our-work-tools/our-documents/guidelines/guidelines-92022-personal-data-breach-notification-under_en",
        "hint": "personal_data_breach_notification",
    },
}


# ---------------------------------------------------------------- download

def _get(url: str):
    headers = {**HEADERS, "Accept": "application/xhtml+xml, text/html, application/pdf, */*", "Accept-Language": "eng"}
    response = httpx.get(url, headers=headers, follow_redirects=True, timeout=120)
    response.raise_for_status()
    return response


def download_source(spec: dict, dest: Path) -> bool:
    candidates = list(spec["urls"])
    if "page" in spec:
        try:
            soup = BeautifulSoup(_get(spec["page"]).text, "html.parser")
            for a in soup.find_all("a", href=True):
                if spec["hint"] in a["href"] and a["href"].lower().endswith(".pdf"):
                    candidates.insert(0, urljoin(spec["page"], a["href"]))
        except Exception as error:  # noqa: BLE001
            print(f"  could not read {spec['page']}: {error}", file=sys.stderr)
    for url in candidates:
        try:
            response = _get(url)
            if len(response.content) > 20000:
                dest.write_bytes(response.content)
                return True
        except Exception as error:  # noqa: BLE001
            print(f"  could not download {url}: {error}", file=sys.stderr)
    return False


def ensure_corpus() -> None:
    CORPUS_DIR.mkdir(exist_ok=True)
    for name, spec in SOURCES.items():
        dest = CORPUS_DIR / spec["file"]
        if dest.is_file():
            continue
        print(f"Downloading {name} ...")
        if not download_source(spec, dest):
            raise SystemExit(
                f"\nCould not download {name}. Open one of these in your browser, save the file as\n"
                f"  {dest}\nand run the command again:\n  " + "\n  ".join(spec["urls"])
            )


# ---------------------------------------------------------------- extraction

def clean(text: str) -> str:
    text = text.replace("\u00ad", "").replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def words_in(text: str) -> int:
    return len(text.split())


def gdpr_units(path: Path) -> list[dict]:
    """GDPR from EUR-Lex HTML: one unit per recital and per article."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    paras = [clean(p.get_text(" ", strip=True)) for p in soup.find_all("p")]
    paras = [p for p in paras if p]
    units: list[dict] = []
    state, recital_no, article_no = "pre", 0, 0
    current = None
    want_title = skip_next = False
    pending = None

    def finish():
        nonlocal current
        if current is None:
            return
        text = "\n".join(current["lines"]).strip()
        if text:
            if current["kind"] == "recital":
                label = f"Recital {current['no']}"
                units.append({"kind": "recital", "location": label, "locations": [label],
                              "title": "", "text": f"({current['no']}) {text}"})
            else:
                label = f"Article {current['no']}"
                title = f"{label} - {current['title']}"
                units.append({"kind": "article", "location": label, "locations": [label],
                              "title": title, "text": text})
        current = None

    for p in paras:
        if state == "pre":
            m = re.match(r"^\(1\)\s*(.*)$", p)
            if m:
                state, recital_no = "recitals", 1
                current = {"kind": "recital", "no": 1, "title": "", "lines": [m.group(1)] if m.group(1) else []}
            continue
        if state == "recitals":
            if p.upper().startswith("HAVE ADOPTED"):
                finish()
                state = "articles"
                continue
            m = re.match(rf"^\({recital_no + 1}\)\s*(.*)$", p)
            if m:
                finish()
                recital_no += 1
                current = {"kind": "recital", "no": recital_no, "title": "",
                           "lines": [m.group(1)] if m.group(1) else []}
                continue
            current["lines"].append(p)
            continue
        # articles
        if p.startswith("Done at Brussels"):
            break
        m = re.fullmatch(r"Article (\d+)", p)
        if m and int(m.group(1)) == article_no + 1:
            finish()
            article_no += 1
            current = {"kind": "article", "no": article_no, "title": "", "lines": []}
            want_title = True
            continue
        if current is None:
            continue
        if want_title:
            current["title"] = p
            want_title = False
            continue
        if re.fullmatch(r"(CHAPTER|SECTION|Section) [IVX\d]+", p):
            skip_next = True
            continue
        if skip_next:
            skip_next = False
            continue
        if re.fullmatch(r"\(\w{1,4}\)|\d+\.|[—–-]", p):
            pending = p
            continue
        if pending:
            p, pending = f"{pending} {p}", None
        current["lines"].append(p)
    finish()
    n_rec = sum(u["kind"] == "recital" for u in units)
    n_art = sum(u["kind"] == "article" for u in units)
    print(f"  GDPR parsed: {n_rec} recitals (expected 173), {n_art} articles (expected 99)", file=sys.stderr)
    return units


def pdf_pages(path: Path) -> list[tuple[int, list[str]]]:
    """(page number, cleaned lines) for every page, without headers, footers and TOC dots."""
    reader = PdfReader(str(path))
    raw = [(i + 1, (page.extract_text() or "")) for i, page in enumerate(reader.pages)]
    counts: dict[str, int] = {}
    for _, text in raw:
        for line in {line.strip() for line in text.splitlines()}:
            counts[line] = counts.get(line, 0) + 1
    limit = max(3, int(0.3 * len(raw)))
    pages = []
    for number, text in raw:
        lines = []
        for line in text.splitlines():
            s = clean(line)
            if not s or re.fullmatch(r"\d{1,3}", s) or "...." in s:
                continue
            if counts.get(line.strip(), 0) >= limit and len(s) < 120:
                continue
            lines.append(s)
        pages.append((number, lines))
    return pages


HEADING = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,3})(\.?)\s+([A-Z][^\n]{2,100})$")


def heading_of(line: str):
    """(number, title) if the line looks like a section title, else None. Footnotes and numbered paragraphs are not titles."""
    m = HEADING.match(line)
    if not m or line.endswith((".", ",", ";", ":")) or line[-1].isdigit():
        return None
    num, dot, title = m.group(1), m.group(2), m.group(3)
    if "." in num or title.isupper() or (dot and len(title) <= 70 and "," not in title and len(title.split()) <= 10):
        return num, title
    return None


def heading_ok(cur: tuple, cand: tuple) -> bool:
    """A heading number must follow the previous one (1, 1.1, 1.2, 2 ...). Footnote numbers do not."""
    for k in range(1, len(cur) + 2):
        expected = cur[k - 1] + 1 if k <= len(cur) else 1
        if len(cand) == k and cand[:k - 1] == cur[:k - 1] and cand[k - 1] == expected:
            return True
    return False


def pdf_units(path: Path) -> tuple[list[dict], list[dict]]:
    """Returns (structure units = sections, flow units = pages)."""
    pages = pdf_pages(path)
    flow = []
    for number, lines in pages:
        text = "\n".join(lines).strip()
        if text:
            flow.append({"kind": "page", "location": f"p. {number}", "locations": [f"p. {number}"],
                         "title": "", "text": text})
    sections: list[dict] = []
    current = {"num": "Intro", "title": "", "pages": [], "lines": []}

    def close():
        if words_in(" ".join(current["lines"])) > 0:
            sections.append(dict(current))

    cur_num: tuple = ()
    for number, lines in pages:
        for line in lines:
            found = heading_of(line)
            if found:
                close()
                current = {"num": found[0], "title": found[1], "pages": [number], "lines": []}
                continue
            current["lines"].append(line)
            if number not in current["pages"]:
                current["pages"].append(number)
    close()
    merged: list[dict] = []
    for sec in sections:
        small = words_in(" ".join(sec["lines"])) < 80
        if merged and small:
            prev = merged[-1]
            if sec["title"]:
                prev["lines"].append(f"{sec['num']} {sec['title']}")
            prev["lines"] += sec["lines"]
            prev["pages"] += [n for n in sec["pages"] if n not in prev["pages"]]
            prev["nums"].append(sec["num"])
        else:
            sec["nums"] = [sec["num"]]
            merged.append(sec)
    units = []
    for s in merged:
        first, last = min(s["pages"]), max(s["pages"])
        label = f"Section {s['nums'][0]}" if s["nums"][0] != "Intro" else "Introduction"
        pages_label = f"p. {first}" if first == last else f"p. {first}-{last}"
        locations = [label] + [f"Section {n}" for n in s["nums"][1:]] + [f"p. {n}" for n in range(first, last + 1)]
        units.append({"kind": "section", "location": f"{label} ({pages_label})", "locations": locations,
                      "title": f"{label} {s['title']}".strip(), "text": "\n".join(s["lines"])})
    return units, flow


def text_units(text: str) -> tuple[list[dict], list[dict]]:
    """Plain text or html: parts of about 300 words."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n|\n", text) if p.strip()]
    units, cur, count = [], [], 0
    for para in paragraphs + [None]:
        if para is None or (count >= 300 and cur):
            if cur:
                n = len(units) + 1
                units.append({"kind": "part", "location": f"Part {n}", "locations": [f"Part {n}"],
                              "title": "", "text": "\n".join(cur)})
            cur, count = [], 0
        if para is not None:
            cur.append(para)
            count += words_in(para)
    return units, units


def load_document(path: Path) -> tuple[list[dict], list[dict]]:
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        if "gdpr" in path.stem.lower():
            units = gdpr_units(path)
            return units, units
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        return text_units(clean(soup.get_text("\n")))
    if suffix == ".pdf":
        return pdf_units(path)
    if suffix in (".txt", ".md"):
        return text_units(clean(path.read_text(encoding="utf-8", errors="ignore")))
    raise ValueError(f"Unsupported file type {suffix}. Use .pdf, .html, .txt or .md")


# ---------------------------------------------------------------- chunking

def embed_text(chunk: dict) -> str:
    return f"{chunk['source']} | {chunk['location']}\n{chunk['text']}"


def make_chunk(source: str, design: str, n: int, location: str, locations: list[str], text: str) -> dict:
    chunk = {"id": f"{source}::{design}::{n:04d}", "source": source, "location": location,
             "locations": locations, "text": text}
    chunk["hash"] = hashlib.sha1(embed_text(chunk).encode("utf-8")).hexdigest()
    return chunk


def pack(paragraphs: list[str], max_words: int) -> list[str]:
    pieces, cur, count = [], [], 0
    for para in paragraphs:
        words = para.split()
        if len(words) > max_words:
            if cur:
                pieces.append("\n".join(cur))
                cur, count = [], 0
            for i in range(0, len(words), max_words):
                pieces.append(" ".join(words[i:i + max_words]))
            continue
        if count + len(words) > max_words and cur:
            pieces.append("\n".join(cur))
            cur, count = [], 0
        cur.append(para)
        count += len(words)
    if cur:
        pieces.append("\n".join(cur))
    return pieces


def chunk_structure(source: str, units: list[dict]) -> list[dict]:
    """One chunk per article or section (split if long); neighbouring recitals are grouped."""
    chunks: list[dict] = []
    group: list[dict] = []

    def add(location, locations, text):
        chunks.append(make_chunk(source, "structure", len(chunks), location, locations, text))

    def flush():
        if not group:
            return
        number = lambda u: u["location"].split()[-1]
        location = group[0]["location"] if len(group) == 1 else f"Recitals {number(group[0])}-{number(group[-1])}"
        locations = [loc for u in group for loc in u["locations"]]
        add(location, locations, "\n".join(u["text"] for u in group))
        group.clear()

    for unit in units:
        if unit["kind"] == "recital":
            group.append(unit)
            if sum(words_in(u["text"]) for u in group) >= RECITAL_GROUP_WORDS:
                flush()
            continue
        flush()
        pieces = pack(unit["text"].split("\n"), STRUCT_MAX_WORDS)
        for i, piece in enumerate(pieces, 1):
            location = unit["location"] if len(pieces) == 1 else f"{unit['location']} (part {i}/{len(pieces)})"
            text = f"{unit['title']}\n{piece}" if unit["title"] else piece
            add(location, unit["locations"], text)
    flush()
    return chunks


def chunk_fixed(source: str, units: list[dict]) -> list[dict]:
    """Windows of FIXED_WORDS words with overlap, over the flow of units."""
    words: list[tuple[str, int]] = []
    for idx, unit in enumerate(units):
        body = f"{unit['title']}\n{unit['text']}" if unit["title"] else unit["text"]
        words.extend((w, idx) for w in body.split())
    chunks: list[dict] = []
    step = FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, len(words), step):
        window = words[start:start + FIXED_WORDS]
        if len(window) < 40 and chunks:
            break
        idxs = sorted({i for _, i in window})
        locations: list[str] = []
        for i in idxs:
            for loc in units[i]["locations"]:
                if loc not in locations:
                    locations.append(loc)
        first, last = units[idxs[0]]["location"], units[idxs[-1]]["location"]
        location = first if first == last else f"{first} to {last}"
        text = " ".join(w for w, _ in window)
        chunks.append(make_chunk(source, "fixed", len(chunks), location, locations, text))
        if start + FIXED_WORDS >= len(words):
            break
    return chunks


def chunk_file(path: Path, source: str | None = None) -> dict[str, list[dict]]:
    """Extract, clean and chunk one file with both designs: {design: [chunks]}."""
    path = Path(path)
    source = source or path.stem
    structure_units, flow_units = load_document(path)
    return {"structure": chunk_structure(source, structure_units),
            "fixed": chunk_fixed(source, flow_units)}


# ---------------------------------------------------------------- storage

def get_design() -> str:
    if CONFIG_FILE.is_file():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8")).get("design", "structure")
    return "structure"


def chunks_file(design: str) -> Path:
    return INDEX_DIR / f"chunks_{design}.jsonl"


def read_chunks(design: str) -> list[dict]:
    path = chunks_file(design)
    if not path.is_file():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_chunks(design: str, chunks: list[dict]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    with chunks_file(design).open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def load_vectors() -> dict[str, list[float]]:
    vectors: dict[str, list[float]] = {}
    if VECTORS_FILE.is_file():
        with VECTORS_FILE.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    vectors[row["h"]] = row["v"]
    return vectors


def get_client():
    from google import genai
    return genai.Client(api_key=load_api_key())


def embed_one(client, text: str) -> list[float]:
    """One call per text: gemini-embedding-2 merges a list of texts into one embedding."""
    import numpy as np

    for attempt in range(6):
        try:
            response = client.models.embed_content(model=EMBED_MODEL, contents=text)
            arr = np.asarray(response.embeddings[0].values, dtype=np.float32)
            arr = arr / (np.linalg.norm(arr) or 1.0)
            return [round(float(x), 5) for x in arr]
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message:
                if attempt == 5 or "perday" in message.lower().replace(" ", "").replace("_", ""):
                    raise RuntimeError(
                        "Gemini quota reached. Vectors already embedded are saved; "
                        "run the command again later (the daily quota resets at 09:00 Spain time)."
                    ) from error
                wait = 15 * (attempt + 1)
                print(f"  rate limit, waiting {wait} s ...", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("embedding failed")


def embed_texts(client, texts: list[str]) -> list[list[float]]:
    """Embed texts one by one, return L2-normalised vectors."""
    out = []
    for text in texts:
        out.append(embed_one(client, text))
        time.sleep(0.3)
    return out


def embed_and_store(chunks: list[dict], client=None) -> int:
    """Embed only the chunks without a saved vector; save each batch at once."""
    INDEX_DIR.mkdir(exist_ok=True)
    have = load_vectors()
    missing, seen = [], set()
    for chunk in chunks:
        if chunk["hash"] not in have and chunk["hash"] not in seen:
            missing.append(chunk)
            seen.add(chunk["hash"])
    if not missing:
        return 0
    client = client or get_client()
    done = 0
    with VECTORS_FILE.open("a", encoding="utf-8") as f:
        for i in range(0, len(missing), BATCH_SIZE):
            batch = missing[i:i + BATCH_SIZE]
            for chunk, vector in zip(batch, embed_texts(client, [embed_text(c) for c in batch])):
                f.write(json.dumps({"h": chunk["hash"], "v": vector}) + "\n")
            f.flush()
            done += len(batch)
            print(f"  embedded {done}/{len(missing)}", file=sys.stderr)
            time.sleep(1)
    return done


def add_to_index(path: str) -> str:
    """Used by server.py: add one file to the active design. Skips documents already indexed."""
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        return f"File not found: {file}"
    source = file.stem
    design = get_design()
    existing = read_chunks(design)
    count = sum(c["source"] == source for c in existing)
    if count:
        return f"'{source}' is already indexed ({count} chunks). Nothing was changed."
    try:
        new_chunks = chunk_file(file, source)[design]
    except ValueError as error:
        return str(error)
    if not new_chunks:
        return f"No text could be extracted from {file.name}."
    known = {c["hash"] for c in existing}
    if all(c["hash"] in known for c in new_chunks):
        return "The same content is already indexed under another name. Nothing was changed."
    embed_and_store(new_chunks)
    write_chunks(design, existing + new_chunks)
    return f"Added '{source}': {len(new_chunks)} chunks ({design} design) are now searchable."


# ---------------------------------------------------------------- main

def main() -> None:
    ensure_corpus()
    INDEX_DIR.mkdir(exist_ok=True)
    by_design: dict[str, list[dict]] = {d: [] for d in DESIGNS}
    total_words = 0
    for name, spec in SOURCES.items():
        path = CORPUS_DIR / spec["file"]
        print(f"Chunking {name} ...")
        structure_units, flow_units = load_document(path)
        total_words += sum(words_in(u["text"]) for u in flow_units)
        by_design["structure"] += chunk_structure(name, structure_units)
        by_design["fixed"] += chunk_fixed(name, flow_units)
    print(f"\nCorpus: {len(SOURCES)} documents, about {total_words:,} words.")
    if total_words < 50000 or len(SOURCES) < 3:
        print("WARNING: the assignment needs at least 3 documents and 50,000 words.")
    for design in DESIGNS:
        write_chunks(design, by_design[design])
        print(f"Design '{design}': {len(by_design[design])} chunks")
    if not CONFIG_FILE.is_file():
        CONFIG_FILE.write_text(json.dumps({"design": "structure"}), encoding="utf-8")
    client = get_client()
    for design in DESIGNS:
        new = embed_and_store(by_design[design], client)
        print(f"Design '{design}': {new} new vectors embedded.")
    print("Index ready.")


if __name__ == "__main__":
    main()
