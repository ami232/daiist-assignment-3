"""
Assignment 3: build the index (`main.py index`). May be index.ipynb instead.

Download the corpus (into corpus/, git-ignored), extract, clean and chunk it
with source and location metadata, embed with Gemini, and store everything in
index/. Save each vector as you get it and embed only chunks without one.

Write the per-file steps as functions (e.g. `chunk_file(path)`,
`embed_and_store(chunks)`): server.py's add-document tool imports them.
"""

import hashlib
import json
import re
import sys
import time
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup
from google import genai
from google.genai import errors, types

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
VECTORS = INDEX_DIR / "vectors.jsonl"      # every vector from Gemini, saved as soon as it arrives

# The corpus: three EU laws from EUR-Lex. "articles" is how many Articles each has (a sanity check).
DOCUMENTS = [
    {"source": "gdpr", "celex": "32016R0679", "articles": 99, "title": "General Data Protection Regulation (EU) 2016/679"},
    {"source": "dga", "celex": "32022R0868", "articles": 38, "title": "Data Governance Act (EU) 2022/868"},
    {"source": "ffd", "celex": "32018R1807", "articles": 9, "title": "Free Flow of Non-Personal Data Regulation (EU) 2018/1807"},
]
# Not in the base corpus: evaluate.py adds it with add_document to answer an unanswerable question.
EXTRA_DOCUMENT = {"source": "open_data", "celex": "32019L1024", "articles": 21, "title": "Open Data Directive (EU) 2019/1024"}
TITLES = {d["source"]: d["title"] for d in DOCUMENTS + [EXTRA_DOCUMENT]}
URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH = 10            # chunks per request
PAUSE = 15            # seconds between requests (free-tier rate limit)

# Two retrieval designs, each stored in its own Chroma collection:
#   "article": one chunk per Article (structure-based)
#   "fixed":   450-word windows with 50 words of overlap
DESIGNS = ["article", "fixed"]
CHOSEN = "article"    # the design the server uses, chosen from eval/retrieval.csv
MAX_WORDS = 450
OVERLAP = 50


def log(*args):
    """Print to stderr: the MCP server's stdout is reserved for the protocol."""
    print(*args, file=sys.stderr, flush=True)


# ---------- 1. Download ----------

def download(doc):
    """Save the document's HTML page in corpus/ and return its path."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{doc['source']}.html"
    if not path.exists():
        url = URL.format(celex=doc["celex"])
        response = httpx.get(url, headers={"User-Agent": "Mozilla/5.0 (student project)"},
                             follow_redirects=True, timeout=90)
        if response.status_code != 200 or "Article 1" not in response.text:
            raise RuntimeError(f"Could not download {url}. Open it in a browser and save it as {path}.")
        path.write_bytes(response.content)
    return path


# ---------- 2. Extract and clean ----------

BLOCK_TAGS = ["p", "td", "th", "li", "h1", "h2", "h3"]


def clean(text):
    text = re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()
    return re.sub(r"\s+([,.;:)])", r"\1", text)          # "Committee ," -> "Committee,"


def read_blocks(path):
    """The visible text of an EUR-Lex HTML page as a list of paragraphs."""
    soup = BeautifulSoup(Path(path).read_bytes(), "html.parser")
    for tag in soup(["script", "style", "head", "nav"]) + soup.find_all(attrs={"role": "navigation"}):
        tag.decompose()                                    # the page menu is not part of the law
    for link in soup.find_all("a", href=True):
        if "#ntr" in link["href"]:                         # footnote marks inside sentences, like "(4)"
            link.decompose()
    blocks = []
    for tag in soup.find_all(BLOCK_TAGS):
        if not tag.find(BLOCK_TAGS):                       # innermost blocks only, so nothing is read twice
            text = clean(" ".join(tag.stripped_strings))
            if text:
                blocks.append(text)
    return blocks


# ---------- 3. Split into units with a location ----------

ARTICLE = re.compile(r"^Article (\d+[a-z]?)$")
RECITAL = re.compile(r"^\((\d+)\)$")
ANNEX = re.compile(r"^ANNEX( [IVX]+)?$")
DIVISION = re.compile(r"^(CHAPTER|TITLE|Section|SECTION) [IVXLC\d]+$")
MARKER = re.compile(r"^(\(\w{1,4}\)|\d{1,3}\.|[—–-])$")     # a list marker alone: "(a)", "1.", "-"


def is_title(text):
    """A heading line: short, not a numbered paragraph, no sentence punctuation at the end."""
    return (0 < len(text) < 200 and not re.match(r"^(\d+\.|\()", text) and not text.endswith((".", ";", ":", ","))
            and not ARTICLE.match(text) and not ANNEX.match(text) and not DIVISION.match(text))


def split_units(blocks):
    """Turn the paragraphs of a legal act into units: Preamble, Recital n, Article n, Annex n."""
    units = []
    state = "front"            # front -> recitals -> articles -> end (signatures); annex after "ANNEX"
    recital_number = 0
    marker = ""
    i = 0

    def start(label, heading=""):
        units.append({"label": label, "heading": heading, "paragraphs": []})

    while i < len(blocks):
        block = blocks[i]
        following = blocks[i + 1] if i + 1 < len(blocks) else ""
        i += 1
        if ANNEX.match(block) and state != "front":
            state, marker = "annex", ""
            start("Annex" + block[5:], following if is_title(following) else "")
            i += 1 if is_title(following) else 0
        elif ARTICLE.match(block) and state != "annex":
            state, marker = "articles", ""
            start(block, following if is_title(following) else "")
            i += 1 if is_title(following) else 0
        elif state == "front":
            if not units and not re.match(r"^(REGULATION|DIRECTIVE|DECISION) .*\d", block):
                continue                                   # the Official Journal banner above the title
            if block == "Whereas:":
                state = "recitals"
            else:
                if not units:
                    start("Preamble")
                units[-1]["paragraphs"].append(block)
        elif state == "recitals" and RECITAL.match(block) and int(block[1:-1]) == recital_number + 1:
            recital_number += 1
            start(f"Recital {recital_number}")
        elif state == "recitals" and block.startswith(("HAVE ADOPTED", "HAS ADOPTED")):
            state = "between"                              # until the first Article
        elif state == "articles" and block.startswith("Done at "):
            state = "end"                                  # signatures and footnotes: skipped
        elif state == "articles" and DIVISION.match(block):
            i += 1 if is_title(following) else 0           # "CHAPTER II" and its title belong to no Article
        elif state in ("end", "between"):
            continue
        elif MARKER.match(block):
            marker = block                                 # "(a)" is in its own table cell: glue it to its text
        else:
            units[-1]["paragraphs"].append(f"{marker} {block}".strip())
            marker = ""
    return [u for u in units if u["paragraphs"] and "correlation table" not in u["heading"].lower()]


# ---------- 4. Chunk ----------

def words(text):
    return len(text.split())


def chunk_article(units):
    """One chunk per Article (split between paragraphs if over MAX_WORDS); recitals grouped."""
    chunks = []
    for unit in units:
        text = "\n".join(unit["paragraphs"])
        last = chunks[-1] if chunks else None
        if unit["label"].startswith("Recital"):
            text = f"({unit['label'].split()[1]}) {text}"
            if last and last["locations"][0].startswith("Recital") and words(last["text"]) + words(text) <= MAX_WORDS:
                last["text"] += "\n" + text                # add this recital to the current group
                last["locations"].append(unit["label"])
                continue
        if words(text) <= MAX_WORDS:
            chunks.append({"locations": [unit["label"]], "heading": unit["heading"], "text": text})
            continue
        part = []                                          # a long Article: cut between paragraphs
        for paragraph in unit["paragraphs"] + [None]:
            if part and (paragraph is None or words(" ".join(part + [paragraph])) > MAX_WORDS):
                chunks.append({"locations": [unit["label"]], "heading": unit["heading"], "text": "\n".join(part)})
                part = []
            if paragraph:
                part.append(paragraph)
    for chunk in chunks:
        first, last = chunk["locations"][0], chunk["locations"][-1]
        chunk["location"] = first if first == last else f"Recitals {first.split()[1]}-{last.split()[1]}"
    return chunks


def chunk_fixed(units):
    """Fixed windows of MAX_WORDS words with OVERLAP words of overlap, ignoring the structure."""
    all_words, labels = [], []
    for unit in units:
        unit_words = " ".join([unit["label"] + ".", unit["heading"]] + unit["paragraphs"]).split()
        all_words += unit_words
        labels += [unit["label"]] * len(unit_words)
    chunks = []
    for start in range(0, len(all_words), MAX_WORDS - OVERLAP):
        if start > 0 and len(all_words) - start <= OVERLAP:
            break                                              # the tail is already in the previous window
        covered = list(dict.fromkeys(labels[start:start + MAX_WORDS]))       # units in this window, in order
        location = covered[0] if len(covered) == 1 else f"{covered[0]} to {covered[-1]}"
        chunks.append({"locations": covered, "location": location, "heading": "",
                       "text": " ".join(all_words[start:start + MAX_WORDS])})
    return chunks


def chunk_file(path, design=CHOSEN):
    """Extract, clean and chunk one file. Every chunk carries its source and location."""
    path = Path(path)
    source = re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_")
    title = TITLES.get(source, path.stem)
    units = split_units(read_blocks(path))
    if not units:
        raise ValueError(f"{path.name} does not look like an EU legal act saved as HTML from EUR-Lex.")
    chunks = chunk_article(units) if design == "article" else chunk_fixed(units)
    for number, chunk in enumerate(chunks):
        chunk["id"] = f"{source}-{number:04d}-{hashlib.sha1(chunk['text'].encode()).hexdigest()[:8]}"
        chunk["meta"] = {"source": source, "title": title, "location": chunk["location"],
                         "locations": "|".join(chunk["locations"]), "heading": chunk["heading"],
                         "words": words(chunk["text"])}
        # gemini-embedding-2 expects documents in this format
        chunk["embed_text"] = f"title: {title}, {chunk['location']} {chunk['heading']} | text: {chunk['text']}"
    return chunks


# ---------- 5. Embed with Gemini ----------

_saved = None       # text hash -> vector, loaded from index/vectors.jsonl
_gemini = None


def saved_vectors():
    global _saved
    if _saved is None:
        _saved = {}
        if VECTORS.exists():
            for line in VECTORS.read_text(encoding="utf-8").splitlines():
                key, vector = json.loads(line)
                _saved[key] = vector
    return _saved


def key_of(text):
    return hashlib.sha1(text.encode()).hexdigest()


def embed_texts(texts):
    """Return one vector per text. Only texts without a saved vector are sent to Gemini."""
    global _gemini
    saved = saved_vectors()
    new = list(dict.fromkeys(t for t in texts if key_of(t) not in saved))
    for start in range(0, len(new), BATCH):
        batch = new[start:start + BATCH]
        if _gemini is None:
            _gemini = genai.Client(api_key=load_api_key())
        # One Content per text: a plain list of strings would be merged into ONE embedding by this model.
        contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in batch]
        while True:
            try:
                result = _gemini.models.embed_content(
                    model=EMBED_MODEL, contents=contents,
                    config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM))
                break
            except errors.APIError as error:
                if error.code not in (429, 500, 503):
                    raise
                if "PerDay" in str(error):
                    raise SystemExit("STOPPED: today's free embedding quota is used up. All vectors so far are "
                                     "saved. Run the same command again after 09:00 (Spain).")
                log(f"  Gemini answered {error.code}, waiting 60 seconds...")
                time.sleep(60)
        INDEX_DIR.mkdir(exist_ok=True)
        with VECTORS.open("a", encoding="utf-8") as file:          # saved before the next request
            for text, embedding in zip(batch, result.embeddings):
                saved[key_of(text)] = [round(x, 6) for x in embedding.values]
                file.write(json.dumps([key_of(text), saved[key_of(text)]]) + "\n")
        if len(new) > BATCH:
            log(f"  embedded {min(start + BATCH, len(new))} of {len(new)}")
            time.sleep(PAUSE)
    return [saved[key_of(t)] for t in texts]


def embed_query(query):
    return embed_texts([f"task: question answering | query: {query}"])[0]


# ---------- 6. Store in ChromaDB ----------

_chroma = None


def collection(design=CHOSEN):
    global _chroma
    if _chroma is None:
        _chroma = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"),
                                            settings=chromadb.Settings(anonymized_telemetry=False))
    return _chroma.get_or_create_collection(design, embedding_function=None,
                                            configuration={"hnsw": {"space": "cosine"}})


def close_store():
    """Close index/chroma so another process (the MCP server) can open it."""
    global _chroma
    if _chroma is not None:
        _chroma.close()
        _chroma = None


def stored_ids(source, design=CHOSEN):
    return collection(design).get(where={"source": source}, include=[])["ids"]


def remove_document(source, design=CHOSEN):
    ids = stored_ids(source, design)
    if ids:
        collection(design).delete(ids=ids)


def embed_and_store(chunks, design=CHOSEN):
    """Embed the chunks (only those without a saved vector) and store them. Returns how many were new."""
    source = chunks[0]["meta"]["source"]
    before = len(saved_vectors())
    vectors = embed_texts([c["embed_text"] for c in chunks])
    if set(stored_ids(source, design)) != {c["id"] for c in chunks}:
        remove_document(source, design)                    # an older version of this document is replaced
        collection(design).add(ids=[c["id"] for c in chunks], embeddings=vectors,
                               documents=[c["text"] for c in chunks], metadatas=[c["meta"] for c in chunks])
    return len(saved_vectors()) - before


# ---------- 7. Search ----------

def search(query, k=5, design=CHOSEN):
    """The k chunks closest to the query, each with its text and metadata."""
    col = collection(design)
    if col.count() == 0:
        return []
    result = col.query(query_embeddings=[embed_query(query)], n_results=k, include=["documents", "metadatas"])
    return [{"text": text, **meta} for text, meta in zip(result["documents"][0], result["metadatas"][0])]


def format_results(hits):
    """What the search tool returns: each chunk starts with the tag used to cite it."""
    return "\n\n---\n\n".join(
        f"[{h['source']} | {h['location']}] {h['title']}, {h['location']} {h['heading']}\n{h['text']}" for h in hits)


# ---------- 8. main.py index ----------

def build_index():
    total = 0
    for doc in DOCUMENTS:
        try:
            path = download(doc)
        except (RuntimeError, httpx.HTTPError) as error:
            if not stored_ids(doc["source"]):
                raise
            log(f"{doc['source']}: no download ({error}); keeping the chunks already in index/")
            continue
        for design in DESIGNS:
            chunks = chunk_file(path, design)
            new = embed_and_store(chunks, design)
            log(f"{doc['source']:<5} {design:<8} {len(chunks):>4} chunks, {new} newly embedded")
        units = split_units(read_blocks(path))
        found = sum(1 for u in units if u["label"].startswith("Article"))
        if found != doc["articles"]:
            log(f"WARNING: found {found} Articles in {doc['source']}, expected {doc['articles']}")
        n = sum(words(" ".join(u["paragraphs"])) for u in units)
        total += n
        print(f"{doc['source']}: {n} words")
    print(f"Total: {total} words in {len(DOCUMENTS)} documents. Index ready in index/.")


if __name__ == "__main__":
    build_index()
