"""
Assignment 3: build the index (`main.py index`).

Corpus: THE FINALS Community Wiki (https://www.thefinals.wiki), text under
CC BY-SA 4.0. We download the pages for every gadget, weapon and
specialization, the build, game-mode and arena pages, through the wiki's
MediaWiki API, into corpus/ (git-ignored).

Pipeline, one function per step so server.py's add_document can reuse it:

    download_page(title)            -> corpus/pages/<title>.json   (raw HTML + url + revision)
    extract_sections(path)          -> (meta, [{"section", "text"}])
    chunk_file(path, design)        -> [chunk dicts with source, section, url]
    embed_and_store(chunks, design) -> embeds only chunks without a saved vector
    index_file(path)                -> chunk + embed + store one file in every design

Two chunkings are implemented (only "section" is embedded, see DESIGNS):
    "fixed"   - 250-word windows (40-word overlap) over the whole page, ignoring structure
    "section" - follows the wiki's sections: short neighbouring sections are merged
                (up to ~250 words) and long ones split on line boundaries; each chunk
                is prefixed with the page title and the section name(s) it covers

Vectors are written to ChromaDB (index/chroma) after every batch, so a crash or
the free-tier daily limit loses nothing: rerunning embeds only what is missing.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import threading
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
PAGES_DIR = CORPUS_DIR / "pages"
HOLDOUT_DIR = CORPUS_DIR / "holdout"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_cache.jsonl"  # one {"key", "vector"} per line
MANIFEST = INDEX_DIR / "manifest.json"

WIKI = "https://www.thefinals.wiki"
API_CANDIDATES = [f"{WIKI}/api.php", f"{WIKI}/w/api.php"]
USER_AGENT = "daiist-assignment-3 student RAG project (educational; CC BY-SA attribution kept)"
LICENSE = "CC BY-SA 4.0, THE FINALS Community Wiki contributors"

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 20
DESIGNS = ("section",)  # chunkings that get embedded
# "fixed" (250-word windows) is implemented in chunk_file but not embedded: both chunkings
# together are ~875 chunks, which with the evaluation's query embeddings breaks the free
# tier's ~1,000/day. The retrieval designs compared in evaluate.py all reuse "section".
FIXED_WORDS, FIXED_OVERLAP = 250, 40
SECTION_MAX_WORDS = 250  # small neighbouring sections are merged up to this size
DAILY_EMBED_LIMIT = 1000  # free tier, see SETUP.md

# Page titles as they appear in the wiki's links (checked on 2026-11-25).
PAGES = {
    "hub": ["Loadout", "Builds", "Specializations", "Gadgets", "Weapons"],
    "specialization": [
        "Cloaking_Device", "Evasive_Dash", "Grappling_Hook", "True_Sight",
        "Dematerializer", "Guardian_Turret", "Healing_Beam", "Shockwave",
        "Charge_'N'_Slam", "Goo_Gun", "Mesh_Shield", "Winch_Claw",
    ],
    "gadget": [
        # Light
        "Breach_Charge", "Gateway", "Glitch_Grenade", "Gravity_Vortex", "Infuser",
        "Mimic_Device", "Nullifier", "Thermal_Bore", "Tracking_Dart", "Translocator",
        "Vanishing_Bomb",
        # Medium
        "APS_Turret", "Breach_Drill", "Data_Reshaper", "Defibrillator", "Gas_Mine",
        "Glitch_Trap", "Hover_Pad", "Jump_Pad", "Zipline",
        # Heavy
        "Anti-Gravity_Cube", "Barricade", "C4", "Dome_Shield", "Healing_Emitter",
        "Lockbolt", "Pyro_Mine", "RPG-7",
        # Shared
        "Sonar_Grenade", "Proximity_Sensor", "Explosive_Mine", "Flashbang",
        "Frag_Grenade", "Gas_Grenade", "Goo_Grenade", "Pyro_Grenade", "Smoke_Grenade",
    ],
    "weapon": [
        # Light
        "93R", "ARN-220", "Dagger", "LH1", "M11", "M26_Matter", "Recurve_Bow",
        "SH1900", "SR-84", "Sword", "Throwing_Knives", "V9S", "XP-54",
        # Medium
        "AKM", "CB-01_Repeater", "Cerberus_12GA", "Chimera-XB", "CL-40", "Dual_Blades",
        "FAMAS", "FCAR", "Model_1887", "P90", "Pike-556", "R_.357", "Riot_Shield",
        # Heavy
        ".50_Akimbo", "BFR_Titan", "Flamethrower", "KS-23", "Lewis_Gun",
        "M134_Minigun", "M60", "MGL32", "SA1216", "ShAK-50", "Sledgehammer", "Spear",
    ],
    "game_mode": ["Cashout", "Ranked_Cashout", "Quick_Cash", "Team_Deathmatch", "Power_Shift"],
    "arena": [
        "Monaco", "Seoul", "Skyway_Stadium", "Las_Vegas", "Horizon", "Kyoto",
        "Fortune_Stadium", "Bernal", "Las_Vegas_Stadium", "NOZOMI_CITADEL",
        "Fangwai_City", "Galaxy_Estates",
    ],
}
# Downloaded but NOT indexed: the add-document demo adds it later to answer
# a question the corpus cannot answer at first.
HOLDOUT = ["Point_Break"]


def log(*args) -> None:
    """Everything goes to stderr: server.py imports this module and stdout is its protocol."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download

def _api_get(params: dict) -> dict:
    import httpx

    last_error = None
    for api in API_CANDIDATES:
        try:
            r = httpx.get(api, params={**params, "format": "json", "formatversion": 2},
                          headers={"User-Agent": USER_AGENT}, timeout=30, follow_redirects=True)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/json"):
                API_CANDIDATES[:] = [api] + [a for a in API_CANDIDATES if a != api]  # remember the one that works
                return r.json()
            last_error = f"{api} -> HTTP {r.status_code}"
        except httpx.HTTPError as e:
            last_error = f"{api} -> {type(e).__name__}: {e}"
    raise RuntimeError(f"Wiki API unreachable ({last_error})")


def download_page(title: str, folder: Path = PAGES_DIR) -> Path | None:
    """Fetch one page's rendered HTML via the MediaWiki parse API. Skips pages already downloaded."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (re.sub(r"[^\w.\-']", "_", title) + ".json")
    if path.exists():
        return path
    data = _api_get({"action": "parse", "page": title, "prop": "text|revid|displaytitle", "redirects": 1})
    if "error" in data:
        log(f"  skip {title}: {data['error'].get('info', data['error'])}")
        return None
    p = data["parse"]
    page_title = p["title"]
    doc = {
        "title": BeautifulSoup_text(p.get("displaytitle") or page_title),
        "page": page_title,
        "url": f"{WIKI}/wiki/{page_title.replace(' ', '_')}",
        "revid": p.get("revid"),
        "fetched": date.today().isoformat(),
        "license": LICENSE,
        "html": p["text"],
    }
    path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    time.sleep(0.4)  # be polite to a community wiki
    return path


def BeautifulSoup_text(html: str) -> str:
    from bs4 import BeautifulSoup
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)


# --------------------------------------------------------------------------- extract & clean

DROP_SELECTORS = [
    "script", "style", "noscript", ".mw-editsection", ".navbox", ".toc", "#toc",
    "sup.reference", ".reference", ".references", ".mw-references-wrap", ".gallery",
    "figure", "img", ".noprint", ".mw-empty-elt", ".thumb", ".hatnote",
]
# Not useful for choosing a loadout, and "History" (the patch changelog) holds old numbers
# that would contradict the current stats.
SKIP_SECTIONS = {"gallery", "references", "navigation", "see also", "external links", "videos", "media",
                 "history", "cosmetics", "item mastery", "trivia"}


def _clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _table_text(table) -> str:
    """Tables carry the stats (damage, time to kill...). Leading rows made only of <th> are
    headers; merged header cells (colspan) are expanded so each value keeps its full label,
    e.g. "Head: Light (175 HP) Bullets to kill 1; Light (175 HP) Time to kill (s) 0.000; ..."."""
    rows = table.find_all("tr")
    header_rows = []
    for row in rows:
        cells = row.find_all(["th", "td"])
        if cells and all(c.name == "th" for c in cells) and len(cells) > 1:
            header_rows.append(row)
        else:
            break
    labels: list[str] = []
    for row in header_rows:
        expanded = []
        for c in row.find_all(["th", "td"]):
            expanded += [c.get_text(" ", strip=True)] * int(c.get("colspan") or 1)
        if not labels:
            labels = expanded
        else:
            # a second header row fills the columns under the first one (the first column
            # is usually the row-label column, so align from the right)
            offset = len(labels) - len(expanded)
            for i, text in enumerate(expanded):
                j = i + max(offset, 0)
                if j < len(labels):
                    labels[j] = f"{labels[j]} {text}".strip()
    lines = []
    for row in rows[len(header_rows):]:
        cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
        if not any(cells):
            continue
        if labels and len(cells) == len(labels) and len(cells) > 2:
            lines.append(f"{cells[0]}: " + "; ".join(f"{l} {v}" for l, v in zip(labels[1:], cells[1:]) if v))
        else:
            cells = [c for c in cells if c]
            lines.append(": ".join(cells) if len(cells) == 2 else " | ".join(cells))
    return "\n".join(lines)


def _element_text(el) -> str:
    if el.name is None:
        from bs4 import Comment
        return "" if isinstance(el, Comment) else str(el).strip()
    if el.name == "table":
        return _table_text(el)
    if el.name in ("ul", "ol"):
        return "\n".join("- " + li.get_text(" ", strip=True) for li in el.find_all("li", recursive=False))
    if el.name == "aside" or "portable-infobox" in (el.get("class") or []):
        pairs = []
        for item in el.select(".pi-item"):
            label, value = item.select_one(".pi-data-label"), item.select_one(".pi-data-value")
            if label and value:
                pairs.append(f"{label.get_text(' ', strip=True)}: {value.get_text(' ', strip=True)}")
            elif item.get_text(strip=True):
                pairs.append(item.get_text(" ", strip=True))
        return "\n".join(pairs)
    if el.find(["table", "ul", "ol", "aside"]):
        return "\n".join(t for t in (_element_text(c) for c in el.children) if t)
    return el.get_text(" ", strip=True)


def _heading_of(el) -> tuple[int, str] | None:
    if el.name in ("h2", "h3", "h4"):
        h = el
    elif el.name == "div" and "mw-heading" in (el.get("class") or []):
        h = el.find(["h2", "h3", "h4"])
    else:
        return None
    if h is None:
        return None
    return int(h.name[1]), h.get_text(" ", strip=True)


def html_to_sections(html: str) -> list[dict]:
    """Walk the page top to bottom; every h2/h3/h4 starts a new section ('Usage', 'Usage > Tips')."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    root = soup.select_one(".mw-parser-output") or soup
    for sel in DROP_SELECTORS:
        for tag in root.select(sel):
            tag.decompose()

    sections, stack, buf = [], [(1, "Overview")], []  # stack of (heading level, name)

    def flush():
        text = _clean("\n".join(buf))
        path = [n for _, n in stack]
        name = " > ".join(path)
        if text and path[0].lower() not in SKIP_SECTIONS:
            sections.append({"section": name, "text": text})
        buf.clear()

    from bs4 import Comment

    for el in root.children:
        if isinstance(el, Comment):  # e.g. the parser's "NewPP limit report"
            continue
        heading = _heading_of(el) if getattr(el, "name", None) else None
        if heading:
            flush()
            level, name = heading
            while stack and stack[-1][0] >= level:  # pages sometimes skip a level (h2 -> h4)
                stack.pop()
            if level == 2 or not stack or stack[0][1] == "Overview":
                stack = [s for s in stack if s[1] != "Overview"]
            stack.append((level, name))
            continue
        text = _element_text(el) if getattr(el, "name", None) else str(el).strip()
        if text:
            buf.append(text)
    flush()
    return sections


def extract_sections(path: str | Path) -> tuple[dict, list[dict]]:
    """Return (meta, sections) for a downloaded wiki page or any .html/.md/.txt/.pdf file."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".json":
        doc = json.loads(path.read_text(encoding="utf-8"))
        meta = {k: doc[k] for k in ("title", "url", "revid", "fetched", "license") if k in doc}
        return meta, html_to_sections(doc["html"])
    meta = {"title": path.stem.replace("_", " "), "url": path.resolve().as_uri(), "license": "user-added file"}
    if suffix in (".html", ".htm"):
        return meta, html_to_sections(path.read_text(encoding="utf-8", errors="replace"))
    if suffix in (".md", ".txt"):
        sections, name, buf = [], "Overview", []
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^#{1,4}\s+(.*)", line)
            if m:
                if _clean("\n".join(buf)):
                    sections.append({"section": name, "text": _clean("\n".join(buf))})
                name, buf = m.group(1).strip(), []
            else:
                buf.append(line)
        if _clean("\n".join(buf)):
            sections.append({"section": name, "text": _clean("\n".join(buf))})
        return meta, sections
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return meta, [{"section": f"page {i}", "text": _clean(p.extract_text() or "")}
                      for i, p in enumerate(reader.pages, 1) if (p.extract_text() or "").strip()]
    raise ValueError(f"Unsupported file type {suffix!r}: use .json (wiki page), .html, .md, .txt or .pdf")


# --------------------------------------------------------------------------- chunk

def _chunk_id(design: str, source: str, section: str, text: str) -> str:
    return hashlib.sha1(f"{design}|{source}|{section}|{text}".encode()).hexdigest()[:20]


def _split_words(text: str, size: int, overlap: int) -> list[str]:
    words = text.split()
    if len(words) <= size:
        return [text]
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]


def chunk_file(path: str | Path, design: str = "section") -> list[dict]:
    """Chunk one file. Every chunk carries source (page title), section, url and position."""
    meta, sections = extract_sections(path)
    source = meta["title"]
    base = {"source": source, "url": meta.get("url", ""), "file": Path(path).name}
    chunks = []

    if design == "fixed":
        # Ignore structure: one stream of words, remembering which section each word came from.
        words, owners = [], []
        for s in sections:
            w = s["text"].split()
            words += w
            owners += [s["section"]] * len(w)
        step = FIXED_WORDS - FIXED_OVERLAP
        for n, start in enumerate(range(0, max(len(words) - FIXED_OVERLAP, 1), step)):
            text = " ".join(words[start:start + FIXED_WORDS])
            section = owners[start] if owners else "Overview"
            chunks.append({**base, "section": section, "position": n, "text": text})
    elif design == "section":
        # 1) split sections longer than the limit on line boundaries (table rows stay whole)
        pieces = []
        for s in sections:
            current = []
            for line in s["text"].split("\n"):
                if current and len(" ".join(current + [line]).split()) > SECTION_MAX_WORDS:
                    pieces.append({"section": s["section"], "text": "\n".join(current)})
                    current = []
                current.append(line)
            if current:
                pieces.append({"section": s["section"], "text": "\n".join(current)})
        # a single line longer than the limit (rare): fall back to word windows
        flat = []
        for p in pieces:
            if len(p["text"].split()) > SECTION_MAX_WORDS + 50:
                flat += [{"section": p["section"], "text": t} for t in _split_words(p["text"], SECTION_MAX_WORDS, 30)]
            else:
                flat.append(p)
        # 2) merge consecutive small pieces so tiny sections don't each cost an embedding
        merged = []
        for p in flat:
            last = merged[-1] if merged else None
            if last and len(last["text"].split()) + len(p["text"].split()) <= SECTION_MAX_WORDS:
                if p["section"] not in last["sections"]:
                    last["sections"].append(p["section"])
                last["text"] += "\n\n" + (p["text"] if p["section"] == last["sections"][-1] and len(last["sections"]) == 1
                                           else f"[{p['section']}]\n{p['text']}")
            else:
                merged.append({"sections": [p["section"]], "text": p["text"]})
        for n, m in enumerate(merged):
            section = " / ".join(m["sections"])
            text = f"Page: {source}\nSection: {section}\n\n{m['text']}"
            chunks.append({**base, "section": section, "position": n, "text": text})
    else:
        raise ValueError(f"unknown design {design!r}; choose from {DESIGNS}")

    for c in chunks:
        c["id"] = _chunk_id(design, c["source"], c["section"], c["text"])
    # identical repeated text inside one page would collide; keep the first
    seen, unique = set(), []
    for c in chunks:
        if c["id"] not in seen:
            seen.add(c["id"])
            unique.append(c)
    return unique


# --------------------------------------------------------------------------- embed & store

class DailyQuotaExceeded(RuntimeError):
    pass


_genai_client = None


def genai_client():
    global _genai_client
    if _genai_client is None:
        from google import genai
        from api_key import load_api_key
        _genai_client = genai.Client(api_key=load_api_key())
    return _genai_client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """One Gemini call for a batch of texts, retrying on per-minute limits."""
    from google.genai import errors, types

    # gemini-embedding-2 is multimodal: a plain list of strings is read as ONE document made
    # of several parts (one vector back). Each text must be its own Content to get one vector each.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            result = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                if len(texts) == 1:
                    raise RuntimeError(f"expected 1 embedding, got {len(vectors)}")
                log(f"  batch returned {len(vectors)} vectors for {len(texts)} texts; embedding one by one")
                return [embed_texts([t])[0] for t in texts]
            return vectors
        except errors.APIError as e:
            message = str(e)
            if e.code == 429:
                if "PerDay" in message or "per day" in message.lower():
                    raise DailyQuotaExceeded(message) from e
                wait = 30 * (attempt + 1)
                log(f"  rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            if e.code in (500, 502, 503, 504):
                time.sleep(10 * (attempt + 1))
                continue
            raise
    raise RuntimeError("Gemini embedding kept failing after 6 attempts")


_chroma_client = None
_chroma_lock = threading.Lock()


def collection(design: str):
    """One shared ChromaDB client per process: opening several at once from parallel searches failed."""
    global _chroma_client
    import chromadb

    with _chroma_lock:
        if _chroma_client is None:
            CHROMA_DIR.mkdir(parents=True, exist_ok=True)
            _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        return _chroma_client.get_or_create_collection(f"finals_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed only chunks without a saved vector; store each batch as soon as it returns."""
    col = collection(design)
    existing = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([c["text"] for c in batch])
        col.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in ("source", "section", "url", "file", "position")} for c in batch],
        )
        log(f"  [{design}] embedded {min(i + EMBED_BATCH, len(todo))}/{len(todo)}")
    return len(todo)


def remove_source(source: str, design: str, keep_ids: set[str] = frozenset()) -> int:
    """Delete a document's chunks (except keep_ids). Used when a page changed or was re-added."""
    col = collection(design)
    ids = [i for i in col.get(where={"source": source}, include=[])["ids"] if i not in keep_ids]
    if ids:
        col.delete(ids=ids)
    return len(ids)


def index_file(path: str | Path) -> dict:
    """Chunk, embed and store one file in every design. Re-adding an unchanged file embeds nothing;
    a changed file replaces that document's old chunks."""
    report = {}
    for design in DESIGNS:
        chunks = chunk_file(path, design)
        source = chunks[0]["source"] if chunks else Path(path).stem
        removed = remove_source(source, design, keep_ids={c["id"] for c in chunks})
        new = embed_and_store(chunks, design)
        report[design] = {"source": source, "chunks": len(chunks), "embedded": new, "replaced": removed}
    return report


# --------------------------------------------------------------------------- query embeddings (cached)

_query_cache: dict[str, list[float]] | None = None
_query_lock = threading.Lock()


def _load_query_cache() -> dict[str, list[float]]:
    cache = {}
    if QUERY_CACHE.exists():
        for line in QUERY_CACHE.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                cache[row["key"]] = row["vector"]
            except (ValueError, KeyError):
                continue  # a damaged line costs one re-embedding, never a crash
    return cache


def embed_query(text: str) -> list[float]:
    """Embed a search query, cached in index/query_cache.jsonl so repeated questions cost nothing.
    Appending one line per query under a lock is safe when the agent runs two searches at once
    (rewriting one JSON file from two threads corrupted it in an earlier run)."""
    global _query_cache
    key = hashlib.sha1(f"{EMBED_MODEL}|{text}".encode()).hexdigest()
    with _query_lock:
        if _query_cache is None:
            _query_cache = _load_query_cache()
        if key in _query_cache:
            return _query_cache[key]
    vector = embed_texts([text])[0]
    with _query_lock:
        _query_cache[key] = vector
        with QUERY_CACHE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"key": key, "vector": vector}) + "\n")
    return vector


# --------------------------------------------------------------------------- main

def main() -> None:
    log(f"1/3 Downloading {sum(map(len, PAGES.values()))} pages from {WIKI} (cached in corpus/) ...")
    files, groups = [], {}
    for group, titles in PAGES.items():
        for title in titles:
            path = download_page(title)
            if path:
                files.append(path)
                groups[path.name] = group
    for title in HOLDOUT:
        download_page(title, HOLDOUT_DIR)

    words = 0
    per_group: dict[str, int] = {}
    for f in files:
        _, sections = extract_sections(f)
        n = sum(len(s["text"].split()) for s in sections)
        words += n
        per_group[groups[f.name]] = per_group.get(groups[f.name], 0) + n
    log(f"   {len(files)} pages, {words:,} words: " + ", ".join(f"{g} {n:,}" for g, n in per_group.items()))
    if words < 50_000:
        log("   WARNING: under the 50,000 words the brief asks for.")

    log("2/3 Chunking ...")
    all_chunks = {d: [c for f in files for c in chunk_file(f, d)] for d in DESIGNS}
    for d, cs in all_chunks.items():
        log(f"   {d}: {len(cs)} chunks")

    if os.environ.get("INDEX_DRY_RUN"):
        sample = CORPUS_DIR / "chunks_preview.json"
        sample.write_text(json.dumps(all_chunks, ensure_ascii=False, indent=1), encoding="utf-8")
        log(f"INDEX_DRY_RUN set: stopping before embedding. Chunks written to {sample.relative_to(ROOT)}")
        return
    missing = {d: len(cs) - len(set(collection(d).get(ids=[c["id"] for c in cs], include=[])["ids"])) for d, cs in all_chunks.items()}
    log(f"3/3 Embedding {sum(missing.values())} chunks that have no saved vector yet "
        f"(free tier: about {DAILY_EMBED_LIMIT}/day) ...")
    finished = True
    for d, cs in all_chunks.items():
        col = collection(d)
        stale = set(col.get(include=[])["ids"]) - {c["id"] for c in cs}
        if stale:
            col.delete(ids=list(stale))
            log(f"   [{d}] removed {len(stale)} chunks no longer in the corpus")
        try:
            embed_and_store(cs, d)
        except DailyQuotaExceeded:
            finished = False
            log("   Daily embedding quota reached. Everything embedded so far is saved;")
            log("   run `uv run python main.py index` again after 09:00 (Spain) to finish.")
            break

    MANIFEST.write_text(json.dumps({
        "corpus": WIKI, "license": LICENSE, "snapshot": date.today().isoformat(),
        "pages": len(files), "words": words, "words_per_group": per_group,
        "chunks": {d: len(cs) for d, cs in all_chunks.items()},
        "stored": {d: collection(d).count() for d in DESIGNS},
        "holdout": HOLDOUT, "embed_model": EMBED_MODEL, "complete": finished,
    }, indent=2), encoding="utf-8")
    log(f"Done{'' if finished else ' for today'}: " +
        ", ".join(f"{d} {collection(d).count()}/{len(cs)} stored" for d, cs in all_chunks.items()))


if __name__ == "__main__":
    main()
