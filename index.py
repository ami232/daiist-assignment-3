"""
Assignment 3: build the index (`main.py index`).

Corpus: the TTS Handbook, the employee handbook of the Technology
Transformation Services (US General Services Administration). It is a US
government work, in the public domain and dedicated CC0 1.0. We read it from
the archived GitHub repository at a pinned commit, so it never changes under us.

Pipeline, one function per step so server.py can reuse them:

    download_corpus()        fetch the pages into corpus/ (git-ignored)
    clean_file(path)         Markdown page -> (title, clean text, redactions)
    chunk_file(path, design) clean text -> chunks with source and location
    embed_and_store(chunks, collection)
                             embed only chunks without a saved vector, store
                             them in ChromaDB in index/, batch by batch
    retrieve(query, k, design)
                             the k closest chunks with their citations;
                             design "structure-diverse" caps results at 2
                             chunks per page

Two chunking designs are built, so the evaluation can compare them:

    structure  one chunk per heading section; sections under 60 words are
               merged with the next ones under the same top heading, long
               sections split at paragraphs (max 300 words, 40 words of
               overlap); each chunk starts with its heading path
    fixed      200-word windows with 40 words of overlap, ignoring headings

Library functions log to stderr, never stdout: server.py imports them, and an
MCP server's stdout carries the protocol.
"""

import hashlib
import html
import json
import random
import re
import sys
import time
from datetime import date
from pathlib import Path

import chromadb
import httpx
from google import genai
from google.genai import errors as genai_errors
from google.genai import types

from api_key import load_api_key

# ============================================================================
# Settings
# ============================================================================

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
HOLDOUT_DIR = CORPUS_DIR / "holdout"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
MANIFEST_PATH = INDEX_DIR / "corpus_manifest.json"
QUERY_CACHE_PATH = INDEX_DIR / "query_vectors.json"

REPO = "18F/handbook"
COMMIT = "c220f93896b39e9e4ab0f486a1d5bf346ac06e3e"  # last commit, 4 June 2026
RAW_URL = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/pages/{{source}}.md"
PAGE_URL = f"https://github.com/{REPO}/blob/{COMMIT}/pages/{{source}}.md"
LICENCE = "Public domain (US government work) and CC0 1.0"

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 20  # texts per request; we save after every batch
EMBED_BUDGET = 900  # max texts embedded in one run (free tier: about 1,000 a day)
MAX_RETRIES = 5
TEXTS_PER_MINUTE = 90  # the free tier allows 100 embedded texts a minute; keep a margin

DESIGNS = ("structure", "fixed")
COLLECTIONS = {"structure": "tts-structure", "fixed": "tts-fixed"}
# Retrieval designs: (collection's chunking design, max chunks per page or None).
# "structure-diverse" reuses the structure vectors but keeps at most 2 chunks
# per page in the results, so one page cannot fill every slot.
RETRIEVAL_DESIGNS = {
    "structure": ("structure", None),
    "fixed": ("fixed", None),
    "structure-diverse": ("structure", 2),
}
DIVERSE_CANDIDATES = 3  # fetch k x 3 candidates before applying the per-page cap

# The design chosen from the retrieval evaluation (hit@5 90% with 598 words,
# against 93% with 942 words for fixed): used by server.py and the agent.
SEARCH_DESIGN = "structure-diverse"
SEARCH_K = 5

STRUCTURE_MAX_WORDS = 300
FIXED_WINDOW_WORDS = 200
OVERLAP_WORDS = 40
MIN_SECTION_WORDS = 5  # a heading with less body text than this is skipped
MERGE_MIN_WORDS = 60  # a smaller section is merged with the ones after it

SEPARATOR = " › "  # between levels of a heading path

# The HR pages we index (62). Left out on purpose:
#   training-and-development/intro-to-github and pra-for-user-research: not HR.
#   general-information-and-resources/employee-resources-policies/transit-benefit:
#     held back for the add_document demo (see HOLDOUT).
PAGES = [
    "about-us/centers-of-excellence/operations/conduct-and-norms",
    "about-us/code-of-conduct",
    "general-information-and-resources/employee-resources-policies/benefits-links",
    "general-information-and-resources/employee-resources-policies/daily-checkin",
    "general-information-and-resources/employee-resources-policies/deaf-hoh",
    "general-information-and-resources/employee-resources-policies/employment-verification",
    "general-information-and-resources/employee-resources-policies/hosting-non-government-speakers",
    "general-information-and-resources/employee-resources-policies/supporting-deaf-hoh-colleagues",
    "general-information-and-resources/employee-resources-policies/veterans-service-members",
    "general-information-and-resources/employee-resources-policies/work-schedules",
    "general-information-and-resources/reasonable-accommodations",
    "getting-started/classes/benefits",
    "getting-started/classes/travel-101",
    "getting-started/equipment",
    "hiring-staying-or-changing-jobs/assignee-detail",
    "hiring-staying-or-changing-jobs/external-details",
    "hiring-staying-or-changing-jobs/fair-and-equitable-hiring-practices",
    "hiring-staying-or-changing-jobs/gsa-details",
    "hiring-staying-or-changing-jobs/hiring",
    "hiring-staying-or-changing-jobs/hiring-authorities",
    "hiring-staying-or-changing-jobs/leaving-tts",
    "hiring-staying-or-changing-jobs/promotions",
    "hiring-staying-or-changing-jobs/resume",
    "hiring-staying-or-changing-jobs/term-extensions",
    "hiring-staying-or-changing-jobs/ttsjobs",
    "performance-management/dates",
    "performance-management/employee-resources",
    "performance-management/end-of-year/hrlinks-steps",
    "performance-management/index",
    "performance-management/mid-year",
    "performance-management/mid-year/hrlinks-steps",
    "performance-management/supervisor-resources",
    "training-and-development/conferences-events-training",
    "training-and-development/details-professional-development",
    "training-and-development/external-speaking-request-playbook",
    "training-and-development/idp",
    "training-and-development/index",
    "training-and-development/olu",
    "training-and-development/working-groups-and-guilds-101",
    "travel-and-leave/advanced-sick-leave",
    "travel-and-leave/fmla",
    "travel-and-leave/going-out-of-office",
    "travel-and-leave/july-13-travel-guidance",
    "travel-and-leave/leave",
    "travel-and-leave/overtime",
    "travel-and-leave/paid-parental-leave",
    "travel-and-leave/travel-and-leave-policies/first-time-travel-complete-concur-profile",
    "travel-and-leave/travel-and-leave-policies/first-time-travel-get-in-concur",
    "travel-and-leave/travel-and-leave-policies/first-time-travel-get-in-concur-pre-olu",
    "travel-and-leave/travel-and-leave-policies/first-time-travel-travel-card",
    "travel-and-leave/travel-and-leave-policies/moving",
    "travel-and-leave/travel-and-leave-policies/travel-guide-2-book-travel",
    "travel-and-leave/travel-and-leave-policies/travel-guide-3-travel",
    "travel-and-leave/travel-and-leave-policies/travel-guide-4-reimbursement",
    "travel-and-leave/travel-and-leave-policies/travel-guide-a-amended-authorizations",
    "travel-and-leave/travel-and-leave-policies/travel-guide-b-after-hours-emergency-travel-authorizations",
    "travel-and-leave/travel-and-leave-policies/travel-guide-email-templates",
    "travel-and-leave/travel-and-leave-policies/travel-guide-faq",
    "travel-and-leave/travel-and-leave-policies/unofficial-foreign-travel",
    "travel-and-leave/travel-and-leave-policies/working-while-traveling",
    "travel-and-leave/travel-guide-table-of-contents",
    "travel-and-leave/voluntary-leave-transfer-program",
]
HOLDOUT = ["general-information-and-resources/employee-resources-policies/transit-benefit"]

# Team mailboxes are not personal data; first.last@gsa.gov addresses are.
ROLE_MAILBOXES = {"privacy.office", "tts.agreements"}


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# ============================================================================
# 1. Download
# ============================================================================

def local_path(source: str, holdout: bool = False) -> Path:
    """corpus/travel-and-leave__leave.md for source travel-and-leave/leave."""
    folder = HOLDOUT_DIR if holdout else CORPUS_DIR
    return folder / (source.replace("/", "__") + ".md")


def source_from_path(path: Path) -> str:
    """The inverse of local_path: the file name gives back the page's source."""
    return Path(path).stem.replace("__", "/")


def download_corpus() -> None:
    """Fetch every page once; afterwards the local copy is used."""
    HOLDOUT_DIR.mkdir(parents=True, exist_ok=True)
    jobs = [(s, False) for s in PAGES] + [(s, True) for s in HOLDOUT]
    fetched = 0
    with httpx.Client(timeout=30, follow_redirects=True) as http:
        for source, holdout in jobs:
            path = local_path(source, holdout)
            if path.exists():
                continue
            for attempt in range(3):
                try:
                    response = http.get(RAW_URL.format(source=source))
                    response.raise_for_status()
                    path.write_text(response.text, encoding="utf-8")
                    fetched += 1
                    break
                except httpx.HTTPError as error:
                    if attempt == 2:
                        raise RuntimeError(f"Could not download {source}: {error}") from error
                    time.sleep(2 ** attempt)
    log(f"corpus: {len(jobs)} pages ({fetched} downloaded now, {len(jobs) - fetched} already here)")


# ============================================================================
# 2. Clean
# ============================================================================

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_LINE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
# The lookbehind stops team mailboxes such as kc-payroll.finance@gsa.gov from
# matching on their "payroll.finance" tail.
PERSONAL_EMAIL = re.compile(r"(?<![\w.-])([a-z]+)\.([a-z]+)@gsa\.gov\b", re.IGNORECASE)
# "Firstname Lastname at someone@..." or "Firstname Lastname (someone@...)",
# possibly across a line break.
NAME_BEFORE_EMAIL = re.compile(r"\b([A-Z][a-z]+)\s+([A-Z][a-z]+)(?=\s+(?:at\s+)?\(?[\w.+-]+@)")
NOT_A_SURNAME = {"Team", "Office", "Desk", "Service", "Services", "Group", "Center",
                 "Coordinator", "Specialist", "Support", "Operations", "Ops"}


def redact_personal_data(text: str) -> tuple[str, dict]:
    """Remove staff members' own emails and their names.

    A first.last@gsa.gov address belongs to one person. We remove it, and
    every "Firstname Lastname" with that last name in the same page. Team
    mailboxes such as tts-travel@gsa.gov are kept: they are the contact
    point an employee needs. Only counts are logged, never the names.
    """
    counts = {"emails": 0, "names": 0}
    last_names = set()

    def replace_email(match: re.Match) -> str:
        if f"{match.group(1)}.{match.group(2)}".lower() in ROLE_MAILBOXES:
            return match.group(0)
        last_names.add(match.group(2).capitalize())
        counts["emails"] += 1
        return "[staff contact removed]"

    text = PERSONAL_EMAIL.sub(replace_email, text)
    for last in last_names:
        text, n = re.subn(rf"\b[A-Z][a-z]+\s+{last}\b", "[staff member]", text)
        counts["names"] += n

    # A person's name written next to a team mailbox ("email Jane Doe at
    # team@gsa.gov") is personal data too, even though the mailbox is not.
    def replace_name(match: re.Match) -> str:
        if match.group(2) in NOT_A_SURNAME:
            return match.group(0)  # "Events Team (tts-events@gsa.gov)" stays
        counts["names"] += 1
        return "[staff member]"

    text = NAME_BEFORE_EMAIL.sub(replace_name, text)
    return text, counts


def clean_markdown(raw: str) -> tuple[str, str, dict]:
    """Turn one handbook page into plain text that keeps its Markdown headings.

    Returns (title, text, redaction counts).
    """
    title = ""
    front = FRONT_MATTER.match(raw)
    if front:
        found = TITLE_LINE.search(front.group(1))
        if found:
            title = found.group(1).strip().strip("\"'")
        raw = raw[front.end():]

    text = raw
    # Images carry no text we can use.
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\{%-?\s*image\b.*?%\}", "", text, flags=re.DOTALL)
    # {% slack_channel "parents" %} -> the #parents Slack channel
    # Some pages already write the # inside the tag ("#people-ops"), so it is stripped first.
    text = re.sub(r'\{%-?\s*slack_channel\s+"#?([^"]+)"(?:\s+"[^"]*")?\s*-?%\}', r"the #\1 Slack channel", text)
    # Links keep their text and lose their target, including {% page "..." %} targets.
    text = re.sub(r"\[([^\]]+)\]\((?:[^()]|\([^)]*\))*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", text)  # [text][ref]
    text = re.sub(r"^\s*\[[^\]]+\]:\s*\S+.*$", "", text, flags=re.MULTILINE)  # [ref]: url
    text = re.sub(r"<((?:https?://|mailto:)[^>\s]+)>", r"\1", text)  # <https://...>
    text = text.replace("mailto:", "")
    # HTML: keep the text, turn table cells and blocks into separators.
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</(td|th)>", " | ", text, flags=re.IGNORECASE)
    text = re.sub(r"</(tr|p|div|li|h\d|table|ul|ol)>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</?[a-zA-Z][^>]*>", "", text)
    # Any template tag left ({% alert %}, {% include ... %}, {{ ... }}).
    text = re.sub(r"\{%.*?%\}", "", text, flags=re.DOTALL)
    text = re.sub(r"\{\{.*?\}\}", "", text, flags=re.DOTALL)
    text = html.unescape(text)
    # Markdown table separator rows such as |---|:---:|
    text = re.sub(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$", "", text, flags=re.MULTILINE)
    # Heading anchors such as "## Sick leave {#sick}"
    text = re.sub(r"^(#{1,6}\s.*?)\s*\{#[^}]*\}\s*$", r"\1", text, flags=re.MULTILINE)

    text, counts = redact_personal_data(text)

    text = "\n".join(line.rstrip() for line in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return title, text, counts


def clean_file(path: Path) -> tuple[str, str, dict]:
    raw = Path(path).read_text(encoding="utf-8")
    title, text, counts = clean_markdown(raw)
    return title or source_from_path(path).split("/")[-1].replace("-", " ").capitalize(), text, counts


# ============================================================================
# 3. Chunk
# ============================================================================

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def sections(text: str) -> list[tuple[list[str], str]]:
    """Split clean text into (heading path, body) pairs, in reading order.

    The path is the list of headings above the body, e.g.
    ["Types of leave", "Sick leave"]. Lines inside code fences are never
    treated as headings.
    """
    result, stack, body, in_fence = [], [], [], False

    def flush():
        result.append(([h for _, h in stack], "\n".join(body).strip()))

    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        match = None if in_fence else HEADING.match(line)
        if match:
            flush()
            body = []
            level = len(match.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, match.group(2).strip()))
        else:
            body.append(line)
    flush()
    return result


def pack_paragraphs(body: str, max_words: int, overlap: int) -> list[str]:
    """Split a long body at paragraph boundaries into pieces of about max_words.

    Each new piece starts with the last `overlap` words of the previous one,
    so a sentence cut at the boundary is still readable on both sides. A
    single paragraph longer than max_words is cut into word windows.
    """
    units = []
    for paragraph in re.split(r"\n\s*\n", body):
        words = paragraph.split()
        if not words:
            continue
        if len(words) <= max_words:
            units.append(paragraph.strip())
        else:
            step = max_words - overlap
            units += [" ".join(words[i:i + max_words]) for i in range(0, len(words) - overlap, step)]

    pieces, current, current_words = [], [], 0
    for unit in units:
        n = len(unit.split())
        if current and current_words + n > max_words:
            pieces.append("\n\n".join(current))
            tail = " ".join(pieces[-1].split()[-overlap:])
            current, current_words = ["..." + tail], overlap
        current.append(unit)
        current_words += n
    if current:
        pieces.append("\n\n".join(current))
    return pieces


def make_chunk(text: str, source: str, title: str, location: str, design: str, origin: str, url: str,
               covered: str = "", section_words: str = "{}") -> dict:
    digest = hashlib.sha1(f"{design}|{source}|{location}|{text}".encode()).hexdigest()[:20]
    return {
        "id": f"{design}-{digest}",
        "text": text,
        "metadata": {
            "source": source,
            "title": title,
            "location": location,
            "sections": covered or location,  # every heading path the chunk contains
            "section_words": section_words,  # JSON: words of body text per heading path
            "url": url,
            "design": design,
            "origin": origin,  # "corpus" from index.py, "added" from add_document
            "words": len(text.split()),
        },
    }


def common_prefix(a: list[str], b: list[str]) -> list[str]:
    prefix = []
    for x, y in zip(a, b):
        if x != y:
            break
        prefix.append(x)
    return prefix


def merge_small_sections(units: list[tuple[list[str], str]]) -> list[tuple[list[str], str, list[tuple[list[str], str]]]]:
    """Join sections under MERGE_MIN_WORDS with the sections that follow them.

    The handbook has many tiny sections ("The following practices help us
    collaborate.") whose content sits in the sub-sections below. Alone they
    make near-empty chunks. A small section absorbs the next ones while they
    share the same top-level heading and the total stays under
    STRUCTURE_MAX_WORDS. The merged chunk's path is the headings the parts
    have in common, and each absorbed part keeps its own heading as a line.
    A heading with no body at all is simply dropped: its children carry it
    in their own path. Returns (path, text, [(heading path, body) of every part]).
    """
    merged = []
    buffer_path, buffer_text, buffer_parts = None, "", []

    def words(text: str) -> int:
        return len(text.split())

    for path, body in units:
        if buffer_path is not None:
            same_top = (buffer_path[:1] == path[:1])
            small = words(buffer_text) < MERGE_MIN_WORDS
            fits = words(buffer_text) + words(body) <= STRUCTURE_MAX_WORDS
            if words(buffer_text) < MIN_SECTION_WORDS:
                buffer_path = None  # an empty heading: drop it
            elif same_top and small and fits:
                shared = common_prefix(buffer_path, path)
                if len(shared) < len(buffer_path):  # the buffer's own heading becomes a line
                    buffer_text = SEPARATOR.join(buffer_path[len(shared):]) + "\n" + buffer_text
                own = path[len(shared):]
                part = (SEPARATOR.join(own) + "\n" + body) if own else body
                buffer_path, buffer_text = shared, buffer_text + "\n\n" + part
                buffer_parts.append((path, body))
                continue
            else:
                merged.append((buffer_path, buffer_text, buffer_parts))
        buffer_path, buffer_text, buffer_parts = path, body, [(path, body)]
    if buffer_path is not None and words(buffer_text) >= MIN_SECTION_WORDS:
        merged.append((buffer_path, buffer_text, buffer_parts))
    return merged


def page_units(title: str, text: str) -> list[tuple[list[str], str]]:
    """(heading path, body) per section, with an H1 that repeats the title removed."""
    units = []
    for path, body in sections(text):
        if path and path[0].strip().lower() == title.strip().lower():
            path = path[1:]  # an H1 that repeats the page title adds nothing
        units.append((path, body))
    return units


def as_location(path: list[str]) -> str:
    return SEPARATOR.join(path) or "Introduction"


def chunk_structure(title: str, text: str) -> list[tuple[str, str, str, str]]:
    """Design "structure": (location, chunk text, sections, section_words), one
    per heading section (small sections merged, long ones split at paragraphs).

    `sections` lists every heading path inside the chunk, separated by " | ".
    `section_words` (JSON) says how many body words each path contributes, so
    the evaluation can tell a chunk that holds a section from one that only
    brushes it.
    """
    out = []
    for path, body, parts in merge_small_sections(page_units(title, text)):
        location = as_location(path)
        header = SEPARATOR.join([title] + path)
        covered = " | ".join(as_location(p) for p, _ in parts)
        pieces = pack_paragraphs(body, STRUCTURE_MAX_WORDS, OVERLAP_WORDS)
        for piece in pieces:
            counts: dict[str, int] = {}
            for part_path, part_body in parts:
                n = len(part_body.split())
                if len(pieces) > 1:  # a long section was split: count only what is in this piece
                    if len(parts) == 1:
                        n = len(piece.split())
                    elif not (part_body.strip()[:80] in piece or part_body.strip()[-80:] in piece):
                        continue
                    n = min(n, len(piece.split()))
                counts[as_location(part_path)] = counts.get(as_location(part_path), 0) + n
            out.append((location, f"{header}\n\n{piece}", covered, json.dumps(counts)))
    return out


def chunk_fixed(title: str, text: str) -> list[tuple[str, str, str, str]]:
    """Design "fixed": 200-word windows over the whole page, headings ignored.

    The location is still recorded (the heading in force where the window
    starts), so retrieval can be scored the same way for both designs.
    """
    words, paths, is_body = [], [], []
    for path, body in page_units(title, text):
        location = as_location(path)
        heading_words = path[-1].split() if path else []
        for j, word in enumerate(heading_words + body.split()):
            words.append(word)
            paths.append(location)
            is_body.append(j >= len(heading_words))  # heading words are not counted as content
    if not words:
        return []
    step = FIXED_WINDOW_WORDS - OVERLAP_WORDS
    starts = range(0, max(1, len(words) - OVERLAP_WORDS), step)
    out = []
    for i in starts:
        window = range(i, min(i + FIXED_WINDOW_WORDS, len(words)))
        inside = list(dict.fromkeys(paths[j] for j in window))  # headings the window spans
        counts: dict[str, int] = {}
        for j in window:
            if is_body[j]:
                counts[paths[j]] = counts.get(paths[j], 0) + 1
        out.append((paths[i], " ".join(words[j] for j in window), " | ".join(inside), json.dumps(counts)))
    return out


def chunk_file(path: Path, design: str = "structure", origin: str = "corpus") -> list[dict]:
    """Clean and chunk one file. Each chunk carries source, title, location and url."""
    if design not in DESIGNS:
        raise ValueError(f"design must be one of {DESIGNS}")
    path = Path(path)
    if path.suffix.lower() not in {".md", ".markdown", ".txt"}:
        raise ValueError(f"{path.name}: only Markdown or plain-text files are supported")
    source = source_from_path(path)
    known = source in PAGES or source in HOLDOUT
    url = PAGE_URL.format(source=source) if known else path.name
    title, text, _ = clean_file(path)
    pairs = chunk_structure(title, text) if design == "structure" else chunk_fixed(title, text)
    chunks = {}
    for location, chunk_text, covered, section_words in pairs:
        chunk = make_chunk(chunk_text, source, title, location, design, origin, url, covered, section_words)
        chunks[chunk["id"]] = chunk  # identical text in the same place counts once
    return list(chunks.values())


# ============================================================================
# 4. Embed and store
# ============================================================================

_client = None
_chroma = None
_embedded_this_run = 0
_recent_sends: list[tuple[float, int]] = []  # (time, texts) for the rate limiter


class EmbeddingBudgetExceeded(RuntimeError):
    pass


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def get_collection(design: str = "structure"):
    """The ChromaDB collection holding one design's chunks (created if missing)."""
    global _chroma
    if _chroma is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _chroma.get_or_create_collection(
        COLLECTIONS[design],
        embedding_function=None,  # we always pass Gemini vectors ourselves
        configuration={"hnsw": {"space": "cosine"}},
    )


def wait_for_rate_limit(n: int) -> None:
    """Sleep until sending n more texts keeps us under TEXTS_PER_MINUTE.

    Cheaper than hitting the limit: a 429 wastes a request and then forces
    a long wait anyway.
    """
    while True:
        now = time.time()
        _recent_sends[:] = [(t, k) for t, k in _recent_sends if now - t < 60]
        if sum(k for _, k in _recent_sends) + n <= TEXTS_PER_MINUTE:
            _recent_sends.append((now, n))
            return
        oldest = _recent_sends[0][0]
        time.sleep(60 - (now - oldest) + 0.5)


def retry_delay(error: Exception, attempt: int) -> float:
    """Seconds to wait after an error: what Google asks for, else exponential backoff."""
    asked = re.search(r"retry in ([\d.]+)\s*s", str(error), re.IGNORECASE)
    if asked:
        return float(asked.group(1)) + 1 + random.random()
    return min(60, 2 ** (attempt + 2)) + random.random()  # 4, 8, 16, 32, 60 s, with jitter


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch with Gemini, under the per-minute limit, retrying on errors.

    task_type tells the model which side of the search a text is on:
    RETRIEVAL_DOCUMENT for chunks, RETRIEVAL_QUERY for questions.
    """
    global _embedded_this_run
    if _embedded_this_run + len(texts) > EMBED_BUDGET:
        raise EmbeddingBudgetExceeded(
            f"budget of {EMBED_BUDGET} embeddings per run reached ({_embedded_this_run} used)"
        )
    for attempt in range(MAX_RETRIES):
        wait_for_rate_limit(len(texts))
        try:
            # Each text must be its own Content. A plain list of strings is read
            # by gemini-embedding-2 as ONE document in several parts, and comes
            # back as a single vector.
            response = get_client().models.embed_content(
                model=EMBED_MODEL,
                contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(task_type=task_type),
            )
            _embedded_this_run += len(texts)
            vectors = [e.values for e in response.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"sent {len(texts)} texts, got {len(vectors)} vectors back")
            return vectors
        except genai_errors.APIError as error:
            retryable = error.code in (429, 500, 503)
            if not retryable or attempt == MAX_RETRIES - 1:
                raise
            wait = retry_delay(error, attempt)
            log(f"  embedding error {error.code}, retrying in {wait:.0f}s")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def existing_ids(collection, ids: list[str]) -> set[str]:
    found = set()
    for i in range(0, len(ids), 500):
        found.update(collection.get(ids=ids[i:i + 500], include=[])["ids"])
    return found


def embed_and_store(chunks: list[dict], collection) -> int:
    """Embed the chunks that have no saved vector yet and store them.

    A chunk's id is a hash of its content, so a chunk already in the
    collection is skipped: re-running costs nothing, and a crash or the daily
    limit loses at most one batch. Returns how many chunks were embedded.
    """
    have = existing_ids(collection, [c["id"] for c in chunks])
    missing = [c for c in chunks if c["id"] not in have]
    for i in range(0, len(missing), EMBED_BATCH):
        batch = missing[i:i + EMBED_BATCH]
        vectors = embed_texts([c["text"] for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
        log(f"  {collection.name}: saved {min(i + EMBED_BATCH, len(missing))}/{len(missing)} new vectors")
    return len(missing)


def refresh_metadata(chunks: list[dict], collection) -> int:
    """Update stored metadata that no longer matches the chunker's, without re-embedding.

    The id depends only on the text, so a metadata-only change (such as a new
    field) keeps the id and the vector; only the metadata is rewritten.
    """
    stored = collection.get(ids=[c["id"] for c in chunks], include=["metadatas"])
    current = dict(zip(stored["ids"], stored["metadatas"]))
    changed = [c for c in chunks if c["id"] in current and current[c["id"]] != c["metadata"]]
    for i in range(0, len(changed), 500):
        batch = changed[i:i + 500]
        collection.update(ids=[c["id"] for c in batch], metadatas=[c["metadata"] for c in batch])
    return len(changed)


def section_word_totals(path: Path) -> dict[str, int]:
    """Body words per heading path in a page, used to judge whether a chunk holds a section."""
    title, text, _ = clean_file(path)
    return {as_location(p): len(body.split()) for p, body in page_units(title, text)}


def remove_stale(collection, keep_ids: set[str]) -> int:
    """Delete corpus chunks that the current chunking no longer produces.

    Chunks added through add_document (origin "added") are left alone.
    """
    stored = collection.get(where={"origin": "corpus"}, include=[])["ids"]
    stale = [i for i in stored if i not in keep_ids]
    if stale:
        collection.delete(ids=stale)
    return len(stale)


# ============================================================================
# 5. Search (used by evaluate.py, server.py and the agent)
# ============================================================================

_query_cache: dict | None = None


def embed_query(text: str, cache: bool = True) -> list[float]:
    """Embed a question with task type RETRIEVAL_QUERY.

    With cache=True the vector is saved in index/query_vectors.json, keyed by
    a hash of the model and the text, so the test questions are embedded once
    and every later evaluation run is free. The server passes cache=False:
    real users' questions should not be written into the repository.
    """
    global _query_cache
    key = hashlib.sha1(f"{EMBED_MODEL}|{text}".encode()).hexdigest()[:20]
    if cache:
        if _query_cache is None:
            _query_cache = json.loads(QUERY_CACHE_PATH.read_text()) if QUERY_CACHE_PATH.exists() else {}
        if key in _query_cache:
            return _query_cache[key]
    vector = embed_texts([text], task_type="RETRIEVAL_QUERY")[0]
    if cache:
        _query_cache[key] = vector
        QUERY_CACHE_PATH.write_text(json.dumps(_query_cache))
    return vector


def retrieve(query: str | list[float], k: int = 5, design: str = "structure", cache: bool = True) -> list[dict]:
    """The k chunks closest to the query, best first.

    `query` is the question text, or an already computed query vector.
    `design` is one of RETRIEVAL_DESIGNS. Each result has the chunk's text,
    its metadata, and `score`, the cosine similarity (1 = same direction,
    0 = unrelated).
    """
    chunking, per_page = RETRIEVAL_DESIGNS[design]
    vector = embed_query(query, cache=cache) if isinstance(query, str) else query
    found = get_collection(chunking).query(
        query_embeddings=[vector],
        n_results=k * DIVERSE_CANDIDATES if per_page else k,
        include=["documents", "metadatas", "distances"],
    )
    candidates = [
        {"id": i, "text": doc, **meta, "score": round(1 - distance, 4)}
        for i, doc, meta, distance in zip(
            found["ids"][0], found["documents"][0], found["metadatas"][0], found["distances"][0]
        )
    ]
    if not per_page:
        return candidates
    results, per_source = [], {}
    for chunk in candidates:  # best first; skip a page once it has per_page chunks
        if per_source.get(chunk["source"], 0) < per_page:
            results.append(chunk)
            per_source[chunk["source"]] = per_source.get(chunk["source"], 0) + 1
        if len(results) == k:
            break
    return results


# ============================================================================
# Main: build everything and write the manifest
# ============================================================================

def main() -> int:
    download_corpus()

    pages, all_chunks, redactions = [], {d: [] for d in DESIGNS}, {}
    for source in PAGES:
        path = local_path(source)
        title, text, counts = clean_file(path)
        if counts["emails"] or counts["names"]:
            redactions[source] = counts
        row = {
            "source": source,
            "title": title,
            "url": PAGE_URL.format(source=source),
            "words_raw": len(path.read_text(encoding="utf-8").split()),
            "words_clean": len(text.split()),
        }
        for design in DESIGNS:
            chunks = chunk_file(path, design)
            all_chunks[design] += chunks
            row[f"chunks_{design}"] = len(chunks)
        pages.append(row)

    INDEX_DIR.mkdir(exist_ok=True)
    manifest = {
        "corpus": "TTS Handbook (Technology Transformation Services, US GSA)",
        "repository": f"https://github.com/{REPO}",
        "commit": COMMIT,
        "licence": LICENCE,
        "built": date.today().isoformat(),
        "embedding_model": EMBED_MODEL,
        "pages": len(pages),
        "words_raw": sum(p["words_raw"] for p in pages),
        "words_clean": sum(p["words_clean"] for p in pages),
        "chunks": {d: len(all_chunks[d]) for d in DESIGNS},
        "redactions": redactions,  # counts only, never the personal data itself
        "holdout": HOLDOUT,
        "page_list": pages,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    status = 0
    for design in DESIGNS:
        collection = get_collection(design)
        removed = remove_stale(collection, {c["id"] for c in all_chunks[design]})
        refreshed = refresh_metadata(all_chunks[design], collection)
        if refreshed:
            log(f"{design}: metadata refreshed for {refreshed} chunks (no re-embedding)")
        try:
            added = embed_and_store(all_chunks[design], collection)
        except (EmbeddingBudgetExceeded, genai_errors.APIError) as error:
            log(f"stopped embedding {design}: {error}")
            log("Everything embedded so far is saved. Run `main.py index` again later to finish.")
            status = 1
            added = None
        words = [c["metadata"]["words"] for c in all_chunks[design]]
        print(f"{design:<10} {len(words):>4} chunks, {sum(words) / len(words):.0f} words on average "
              f"(min {min(words)}, max {max(words)}); "
              f"{'?' if added is None else added} embedded now, {removed} stale removed, "
              f"{collection.count()} stored")

    print("=" * 72)
    print(f"{manifest['pages']} pages, {manifest['words_raw']:,} raw words, "
          f"{manifest['words_clean']:,} clean words")
    print(f"redactions: {sum(c['emails'] for c in redactions.values())} emails and "
          f"{sum(c['names'] for c in redactions.values())} names in {len(redactions)} pages")
    print(f"embeddings used this run: {_embedded_this_run} (budget {EMBED_BUDGET})")
    return status


if __name__ == "__main__":
    sys.exit(main())
