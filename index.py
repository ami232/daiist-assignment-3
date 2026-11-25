"""Build/resume the index. Also supports --prepare-only, --status and --max-new N."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time

from prepare_corpus import ROOT, clean_text, parse, prepare
from retrieval import GeminiEmbedder, Store, cached_embedding, embedding_key

CHUNK_WORDS, OVERLAP_WORDS = 400, 50


def chunk_sections(sections, max_words=CHUNK_WORDS, overlap=OVERLAP_WORDS):
    if max_words < 1 or not 0 <= overlap < max_words:
        raise ValueError("Chunk size must be positive; overlap must be smaller")
    chunks = []
    for section in sections:
        spans = list(re.finditer(r"\S+", section["text"]))
        start = 0
        while start < len(spans):
            end = min(start+max_words, len(spans))
            text = section["text"][spans[start].start():spans[end-1].end()]
            title = f"{section['document_title']} — {section['section_title']}"
            identity = json.dumps([section["source"], section["location"], start, end, text], ensure_ascii=False)
            chunks.append({"id": hashlib.sha256(identity.encode()).hexdigest(),
                "source": section["source"], "location": section["location"], "title": title,
                "url": section["url"], "text": text, "word_start": start, "word_end": end,
                "word_count": end-start, "license": section["license"], "embedding_key": embedding_key(text, title)})
            if end == len(spans):
                break
            start = end-overlap
    return chunks


def prepare_base(store):
    sections, manifest = prepare(download=True)
    chunks = chunk_sections(sections)
    for source in manifest["sources"]:
        store.put_document(source["source"], source["file_sha256"], source["title"],
                           [chunk for chunk in chunks if chunk["source"] == source["source"]])
    notice = ["Financial-health reference corpus: source notices", "",
              "Excerpts were selected and cleaned; navigation was removed, glossary",
              "definitions separated, and MathML formulas converted to text.",
              "These transformations were implemented with AI coding assistance.", ""]
    for source in manifest["sources"]:
        notice.extend([source["title"], source["author_attribution"], source["url"],
                       source["license"], source["license_url"], source.get("license_note", ""), ""])
    notice.append("Noncommercial coursework collection. Each source retains its stated licence.")
    (ROOT / "index" / "ATTRIBUTION.txt").write_text("\n".join(notice)+"\n", encoding="utf-8")
    summary = {"documents": manifest["documents"], "sections": manifest["sections"],
               "source_words_without_overlap": manifest["total_words"], "chunks": len(chunks),
               "chunk_words": CHUNK_WORDS, "overlap_words": OVERLAP_WORDS,
               "boundary": "Never cross a source section", "designs": ["dense", "hybrid"], "winner": None}
    (ROOT / "index" / "preparation.json").write_text(json.dumps(summary, indent=2)+"\n")
    return chunks


def embed_and_store(chunks, store=None, embedder=None, max_new=None, delay=0.7):
    store = store or Store()
    pending = [chunk for chunk in chunks if store.vector(chunk["embedding_key"]) is None]
    if pending:
        embedder = embedder or GeminiEmbedder()
    added = 0
    for chunk in pending:
        if max_new is not None and added >= max_new:
            break
        for attempt in range(4):
            try:
                cached_embedding(store, chunk["text"], chunk["title"], embedder=embedder)
                break
            except Exception as error:
                status = getattr(error, "code", None)
                if status in {429, 500, 502, 503, 504} and attempt < 3:
                    print(f"Gemini returned {status}; retrying in {2**(attempt+1)} seconds.", file=sys.stderr, flush=True)
                    time.sleep(2**(attempt+1))
                    continue
                raise RuntimeError(f"Embedding failed ({type(error).__name__}, status {status}). Successful vectors are saved; rerun to resume.") from None
        added += 1
        if added == 1 or added % 10 == 0 or added == len(pending):
            print(f"Saved {added}/{len(pending)} new passage embeddings.", file=sys.stderr, flush=True)
        if delay:
            time.sleep(delay)
    return {"new_vectors": added, "already_saved": len(chunks)-len(pending), "remaining": len(pending)-added}


def chunk_file(path):
    """Extract an added PDF/text/Markdown/HTML file using the same chunker."""
    path = Path(path).expanduser().resolve(strict=True)
    if not path.is_file() or path.suffix.lower() not in {".pdf", ".txt", ".md", ".html", ".htm"}:
        raise ValueError("Provide a PDF, TXT, MD or HTML document")
    fingerprint = hashlib.sha256(path.read_bytes()).hexdigest()
    slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-") or "document"
    source = f"added-{slug}-{fingerprint[:12]}"
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        pages = [(f"page {i}", page.extract_text() or "") for i, page in enumerate(PdfReader(path).pages, 1)]
    elif path.suffix.lower() in {".html", ".htm"}:
        document = parse(path.read_text(encoding="utf-8"))
        content = next((node for node in document.walk() if node.attrs.get("id") == "book-content"), None)
        content = content or next((node for node in document.walk() if node.tag == "main"), None)
        content = content or next((node for node in document.walk() if node.tag == "body"), document)
        pages = [("document", clean_text(content))]
    else:
        pages = [("document", path.read_text(encoding="utf-8"))]
    sections = [{"source": source, "document_title": path.stem, "section_title": location,
                 "location": location, "url": f"local-document:{path.name}#{location.replace(' ', '-')}",
                 "license": "User-supplied: record licence before redistribution", "text": text.strip()}
                for location, text in pages if text.strip()]
    if not sections:
        raise ValueError("No extractable text; scanned PDFs need OCR before adding")
    return source, fingerprint, chunk_sections(sections)


def add_document(path, store=None, embedder=None):
    """Index an approved file; identical bytes reuse or resume an existing document."""
    store = store or Store()
    source, fingerprint, chunks = chunk_file(path)
    existing = store.document_for_fingerprint(fingerprint)
    if existing:
        source, chunks = existing["source"], store.chunks(existing["source"])
    else:
        store.put_document(source, fingerprint, Path(path).name, chunks, kind="added")
    progress = embed_and_store(chunks, store, embedder)
    return {"source": source, "document_already_indexed": existing is not None, "chunks": len(chunks), **progress}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--max-new", type=int)
    args = parser.parse_args()
    if args.max_new is not None and args.max_new < 0:
        parser.error("--max-new cannot be negative")
    store = Store()
    if args.status:
        print(json.dumps(store.status(), indent=2))
        return
    prepare_base(store)
    if not args.prepare_only:
        print(json.dumps(embed_and_store(store.chunks(), store, max_new=args.max_new), indent=2))
    print(json.dumps(store.status(), indent=2))


if __name__ == "__main__":
    main()
