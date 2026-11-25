"""
Assignment 3: build the index (`uv run python main.py index`).

1. Download 15 OWASP Cheat Sheets (CC BY-SA 4.0) at a fixed commit into corpus/.
2. Clean the Markdown and split it into sections by its headings.
3. Chunk it two ways, to compare designs in evaluate.py:
     fixed     250-word windows with 50 words of overlap, ignoring the structure
     sections  one chunk per section (long sections split at paragraphs), with the
               document title and section path added in front of the text it embeds
4. Embed every chunk that has no saved vector yet, and store the chunks in index/.

server.py's add_document tool imports chunk_file() and embed_and_store() from here.
"""

import csv
import hashlib
import json
import re
import urllib.request
from pathlib import Path

import rag

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
TO_ADD = CORPUS / "to_add"        # downloaded but NOT indexed: used to demo the add-document tool

COMMIT = "05861f28ed88269db390afeb67486abc0adfc076"   # OWASP/CheatSheetSeries, 25 Nov 2026
RAW = f"https://raw.githubusercontent.com/OWASP/CheatSheetSeries/{COMMIT}/cheatsheets/{{name}}.md"
PAGE = "https://cheatsheetseries.owasp.org/cheatsheets/{name}.html"
DOCUMENTS = [
    "Authentication_Cheat_Sheet",
    "Password_Storage_Cheat_Sheet",
    "Forgot_Password_Cheat_Sheet",
    "Multifactor_Authentication_Cheat_Sheet",
    "Session_Management_Cheat_Sheet",
    "Cross-Site_Request_Forgery_Prevention_Cheat_Sheet",
    "Cross_Site_Scripting_Prevention_Cheat_Sheet",
    "SQL_Injection_Prevention_Cheat_Sheet",
    "Input_Validation_Cheat_Sheet",
    "File_Upload_Cheat_Sheet",
    "HTTP_Headers_Cheat_Sheet",
    "Content_Security_Policy_Cheat_Sheet",
    "Server_Side_Request_Forgery_Prevention_Cheat_Sheet",
    "Secrets_Management_Cheat_Sheet",
    "Logging_Cheat_Sheet",
]
EXTRA = ["OAuth2_Cheat_Sheet"]
DESIGNS = ["sections", "fixed"]          # "sections" first: it is the default design
FIXED_SIZE, FIXED_OVERLAP = 250, 50      # words
MAX_SECTION_WORDS = 300                  # longer sections are split at paragraph breaks
MIN_SECTION_WORDS = 60                   # shorter sections are joined to the next one
SKIP_SECTIONS = {"references", "additional resources", "related articles", "further reading",
                 "table of contents", "external references", "other cheatsheets", "resources"}


# ---------------------------------------------------------------- download
def download(names: list[str], folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for name in names:
        path = folder / f"{name}.md"
        if not path.exists():
            with urllib.request.urlopen(RAW.format(name=name), timeout=60) as response:
                path.write_bytes(response.read())
            rag.log(f"downloaded {path.relative_to(ROOT)}")


# ---------------------------------------------------------------- clean and split
def clean(markdown: str) -> str:
    """Markdown -> plain text. Code is kept as written: the HTML-tag remover must not touch it,
    or examples like `<iframe>` vanish (a bug we hit: "in a `<frame>`" became "in a ``")."""
    text = re.sub(r"<!--.*?-->", "", markdown, flags=re.S)                    # HTML comments
    segments = re.split(r"(^\s*```.*?^\s*```|^\s*~~~.*?^\s*~~~)", text, flags=re.S | re.M)
    for i in range(0, len(segments), 2):                                       # even = prose, odd = code block
        prose = segments[i]
        prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", prose)                       # images
        prose = re.sub(r"\[([^\]]+)\]\((?:[^()]|\([^)]*\))*\)", r"\1", prose)   # [text](url) -> text
        prose = re.sub(r"^\s*\[[^\]]+\]:\s*\S+.*$", "", prose, flags=re.M)      # [1]: http://... definitions
        prose = re.sub(r"<br\s*/?>", " ", prose)
        pieces = re.split(r"(`[^`\n]+`)", prose)                                 # odd = inline code: keep
        segments[i] = "".join(p if j % 2 else re.sub(r"</?[a-zA-Z][^>]*>", "", p) for j, p in enumerate(pieces))
    text = "".join(segments).replace("\u00a0", " ").replace("\u2011", "-")   # odd spaces and hyphens
    return re.sub(r"\n{3,}", "\n\n", text).strip()


HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def split_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """(document title, [(section path, body)]) from the Markdown headings.

    Lines inside ``` code blocks are never headings: many code samples contain
    '# comments' that would otherwise start fake sections.
    """
    title, path, body, sections, in_code = "", [], [], [], False

    def flush():
        content = "\n".join(body).strip()
        if content and not any(p.lower() in SKIP_SECTIONS for p in path):
            sections.append((" > ".join(path) or "Introduction", content))
        body.clear()

    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_code = not in_code
        match = None if in_code else HEADING.match(line)
        if match:
            level, name = len(match.group(1)), match.group(2).strip()
            if level == 1:
                title = title or name
                continue
            flush()
            path = path[: level - 2] + [name]
        else:
            body.append(line)
    flush()
    return title, sections


def paragraphs(body: str) -> list[str]:
    """Blank-line paragraphs, keeping each code block in one piece."""
    out, current, in_code = [], [], False
    for line in body.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_code = not in_code
        if not line.strip() and not in_code:
            if current:
                out.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        out.append("\n".join(current))
    return out


def words(text: str) -> int:
    return len(text.split())


# ---------------------------------------------------------------- chunk
def chunk_file(path: Path | str, design: str = "sections", url: str | None = None) -> list[dict]:
    """Clean one Markdown or text file and cut it into chunks with source and location metadata."""
    path = Path(path)
    raw = path.read_text(encoding="utf-8", errors="replace")
    title, sections = split_sections(clean(raw))
    source = path.stem
    meta = {"source": source, "title": title or source.replace("_", " "),
            "url": url or PAGE.format(name=source), "design": design,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    pieces = chunk_fixed(sections) if design == "fixed" else chunk_sections(sections)
    chunks = []
    for n, (location, located_in, text) in enumerate(pieces, 1):
        header = f"{meta['title']} > {location}\n\n" if design == "sections" else ""
        chunks.append({**meta, "id": f"{source}:{n:03d}", "location": location, "sections": located_in,
                       "words": words(text), "text": text, "embed_text": header + text})
    return chunks


def chunk_sections(sections: list[tuple[str, str]]) -> list[tuple[str, list[str], str]]:
    out, carry, carry_paths = [], "", []
    for location, body in sections:
        body = (carry + "\n\n" + body).strip() if carry else body
        located_in = carry_paths + [location]
        if words(body) < MIN_SECTION_WORDS:              # a heading with one line: join it to the next
            carry, carry_paths = body, located_in
            continue
        carry, carry_paths = "", []
        piece = []
        for para in paragraphs(body):
            if piece and words("\n\n".join(piece + [para])) > MAX_SECTION_WORDS:
                out.append((location, located_in, "\n\n".join(piece)))
                piece = []
            if words(para) > MAX_SECTION_WORDS * 1.5:       # one huge paragraph: cut it by words
                tokens = para.split()
                for i in range(0, len(tokens), MAX_SECTION_WORDS):
                    out.append((location, located_in, " ".join(tokens[i:i + MAX_SECTION_WORDS])))
            else:
                piece.append(para)
        if piece:
            out.append((location, located_in, "\n\n".join(piece)))
    if carry:
        out.append((carry_paths[-1], carry_paths, carry))
    return out


def chunk_fixed(sections: list[tuple[str, str]]) -> list[tuple[str, list[str], str]]:
    tagged = [(w, location) for location, body in sections for w in body.split()]
    out, step = [], FIXED_SIZE - FIXED_OVERLAP
    for start in range(0, max(len(tagged) - FIXED_OVERLAP, 1), step):
        window = tagged[start:start + FIXED_SIZE]
        located_in = list(dict.fromkeys(location for _, location in window))
        out.append((located_in[0], located_in, " ".join(w for w, _ in window)))
    return out


# ---------------------------------------------------------------- embed and store
def embed_and_store(chunks: list[dict], design: str = "sections") -> int:
    """Embed the chunks that have no saved vector, then store them in index/<design>/.

    Chunks of the same source replace the ones already stored. Returns how many were new.
    """
    new = sum(not rag.has_vector(c["embed_text"]) for c in chunks)
    rag.embed([c["embed_text"] for c in chunks])
    sources = {c["source"] for c in chunks}
    kept = [c for c in rag.read_chunks(design) if c["source"] not in sources]
    rag.write_chunks(design, kept + chunks)
    return new


def main() -> None:
    download(DOCUMENTS, CORPUS)
    download(EXTRA, TO_ADD)
    stats = {"commit": COMMIT, "documents": [], "designs": {}}
    for name in DOCUMENTS:
        title, sections = split_sections(clean((CORPUS / f"{name}.md").read_text(encoding="utf-8")))
        stats["documents"].append({"source": name, "title": title, "url": PAGE.format(name=name),
                                   "words": sum(words(body) for _, body in sections)})
    total = sum(d["words"] for d in stats["documents"])
    rag.log(f"{len(DOCUMENTS)} documents, {total:,} words after cleaning")

    for design in DESIGNS:
        chunks = [c for name in DOCUMENTS for c in chunk_file(CORPUS / f"{name}.md", design)]
        added = [c for c in rag.read_chunks(design) if c.get("added")]     # keep documents added later
        todo = sum(not rag.has_vector(c["embed_text"]) for c in chunks)
        rag.log(f"design {design}: {len(chunks)} chunks, {todo} still to embed")
        stats["designs"][design] = {"chunks": len(chunks),
                                    "avg_words": round(sum(c["words"] for c in chunks) / len(chunks), 1)}
        rag.write_chunks(design, chunks + added)
        rag.embed([c["embed_text"] for c in chunks])
    # the test questions' vectors too: evaluate.py reuses them, and the search tool answers
    # them without needing the API key (check.py starts the server with no environment)
    questions = ROOT / "eval" / "questions.csv"
    if questions.is_file():
        with questions.open(newline="", encoding="utf-8") as f:
            rag.embed([r["question"] for r in csv.DictReader(f) if r["question"].strip()], task="RETRIEVAL_QUERY")
    (rag.INDEX_DIR / "stats.json").write_text(json.dumps(stats, indent=2))
    if not rag.CONFIG.exists():
        rag.CONFIG.write_text(json.dumps(rag.DEFAULT_CONFIG, indent=2))
    rag.log("index ready")


if __name__ == "__main__":
    main()
