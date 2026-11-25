"""Download and extract a proposed financial-health corpus, without API calls.

Run `python3 prepare_corpus.py` after downloading the files, or add `--download`
to fetch missing files. Original books stay in the git-ignored corpus/ folder.
This step creates sections, not retrieval chunks. Chunking is a later decision.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.request import urlopen
from zipfile import ZipFile
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
BLOCK_TAGS = {"p", "div", "li", "ul", "ol", "section", "header", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "table", "tr"}
SKIP_TAGS = {"script", "style", "nav", "video", "iframe"}
WORD_RE = re.compile(r"\b[\w]+(?:['’−-][\w]+)*\b", re.UNICODE)


@dataclass
class Element:
    tag: str
    attrs: dict[str, str | None] = field(default_factory=dict)
    children: list[Element | str] = field(default_factory=list)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Element):
                yield from child.walk()

    def text(self) -> str:
        if self.tag in SKIP_TAGS or "video" in (self.attrs.get("class") or "").split():
            return ""
        if self.tag in {"annotation", "annotation-xml"}:
            return ""  # Alternate encodings duplicate the visible equation.
        operands = [child for child in self.children if isinstance(child, Element)]
        if self.tag in {"mfrac", "msup", "msub"} and len(operands) == 2:
            operator = {"mfrac": "/", "msup": "^", "msub": "_"}[self.tag]
            return f"({operands[0].text()}) {operator} ({operands[1].text()})"
        if self.tag == "msubsup" and len(operands) == 3:
            return f"({operands[0].text()})_({operands[1].text()})^({operands[2].text()})"
        if self.tag == "msqrt":
            return "sqrt(" + "".join(child.text() for child in operands) + ")"
        if self.tag == "img":
            # Preserve descriptive image alternatives; empty alternatives do
            # not invent the missing content of a diagram or equation.
            alt = (self.attrs.get("alt") or "").strip()
            return f" [Image: {alt}] " if alt else ""
        if self.tag == "br":
            return "\n"
        parts = [child.text() if isinstance(child, Element) else child for child in self.children]
        content = "".join(parts)
        if "glossdef" in (self.attrs.get("class") or "").split():
            return f" ({content.strip()}) "
        if self.tag in {"td", "th"}:
            return re.sub(r"\s+", " ", content).strip() + " | "
        if self.tag == "tr":
            return "\n" + re.sub(r"\s+", " ", content).strip() + "\n"
        return f"\n{content}\n" if self.tag in BLOCK_TAGS else content


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Element(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse(html: str) -> Element:
    parser = DocumentParser()
    parser.feed(html)
    parser.close()
    return parser.root


def clean_text(element: Element) -> str:
    lines = [re.sub(r"[^\S\n]+", " ", line).strip() for line in element.text().splitlines()]
    return "\n".join(line for line in lines if line)


def section_record(source, content, title, chapter, section, url):
    text = clean_text(content)
    if not text:
        raise ValueError(f"No text extracted: {source['source']} / {section}")
    return {
        "source": source["source"],
        "document_title": source["title"],
        "chapter": chapter,
        "location": section,
        "section_title": title,
        "url": url,
        "license": source["license"],
        "text": text,
        "word_count": len(WORD_RE.findall(text)),
        "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "image_count": sum(node.tag == "img" for node in content.walk()),
        "images_without_description": sum(node.tag == "img" and not (node.attrs.get("alt") or "").strip() for node in content.walk()),
    }


def read_lardbucket(source, path):
    records = []
    with ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            # Only individual section files. The archive also contains a
            # combined copy of every chapter, which would double-count text.
            if not re.search(r"/s\d+-\d+-[^/]+\.html$", name):
                continue
            document = parse(archive.read(name).decode("utf-8"))
            content = next((node for node in document.walk() if node.attrs.get("id") == "book-content"), None)
            if content is None:
                raise ValueError(f"Missing book-content in {name}")
            heading = next((node for node in content.walk() if node.tag in {"h1", "h2"}), None)
            if heading is None:
                raise ValueError(f"Missing section heading in {name}")
            title = clean_text(heading)
            numbered = re.match(r"(?:Chapter\s+)?(\d+)(?:\.(\d+))?\s+", title)
            if not numbered:
                raise ValueError(f"Cannot identify location: {name}: {title}")
            chapter = int(numbered[1])
            if chapter not in source["chapters"]:
                continue
            # End-of-chapter exercises are not the reference material needed
            # for this use case. Student evaluation questions stay separate.
            if "end-of-chapter" in title.lower():
                continue
            location = f"{chapter}.{numbered[2]}" if numbered[2] else f"Chapter {chapter} introduction"
            records.append(section_record(source, content, title, chapter, location, source["url"] + Path(name).name))
    return records


def read_htmlbook(source, path):
    document = parse(path.read_text(encoding="utf-8"))
    chapters = [node for node in document.walk() if node.tag == "section" and node.attrs.get("data-type") == "chapter"]
    records = []
    for chapter_number, chapter in enumerate(chapters, start=1):
        if chapter_number not in source["chapters"]:
            continue
        # Preserve subsection boundaries from the exported chapter body.
        # This also keeps the author byline and chapter-number header out.
        blocks = next((node for node in chapter.children if isinstance(node, Element) and "ugc" in (node.attrs.get("class") or "").split()), None)
        if blocks is None:
            blocks = Element("div", children=[node for node in chapter.children if not (isinstance(node, Element) and (node.tag == "header" or "chapter-author" in (node.attrs.get("class") or "").split()))])
        chapter_slug = (chapter.attrs.get("id") or "").removeprefix("chapter-")
        chapter_url = source["url"] + "chapter/" + chapter_slug + "/"
        pending = []
        section_title = "Introduction"
        anchor = ""
        for node in blocks.children + [Element("h1")]:
            if isinstance(node, Element) and node.tag in {"h1", "h2"}:
                if any(isinstance(child, Element) or str(child).strip() for child in pending):
                    location = f"Chapter {chapter_number}, {anchor or 'learning goals'}: {section_title}"
                    records.append(section_record(source, Element("div", children=pending), section_title, chapter_number, location, chapter_url + ("#" + anchor if anchor else "")))
                section_title = clean_text(node)
                anchor = node.attrs.get("id") or ""
                pending = [node] if section_title else []
            else:
                pending.append(node)
    return records


def prepare(download=False):
    config = json.loads((ROOT / "project_config.json").read_text())
    download_dir = ROOT / "corpus" / "downloads"
    download_dir.mkdir(parents=True, exist_ok=True)
    records, summaries, seen = [], [], set()
    for source in config["sources"]:
        path = download_dir / source["filename"]
        if not path.exists():
            if not download:
                raise FileNotFoundError(f"{path.name} is missing. Run with --download.")
            # Atomic save: an interrupted transfer must not look complete.
            temporary = path.with_suffix(path.suffix + ".part")
            with urlopen(source["download_url"], timeout=45) as response, temporary.open("wb") as output:
                while block := response.read(1024 * 1024):
                    output.write(block)
            temporary.replace(path)
        extract = read_lardbucket if source["format"] == "lardbucket_zip" else read_htmlbook
        extracted = extract(source, path)
        retained = []
        for record in extracted:
            if record["text_sha256"] not in seen:
                retained.append(record)
                seen.add(record["text_sha256"])
        if not retained:
            raise ValueError(f"No unique sections in {source['source']}")
        records.extend(retained)
        summaries.append({
            **source,
            "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "selected_section_count": len(retained),
            "word_count": sum(record["word_count"] for record in retained),
            "exact_duplicate_sections_removed": len(extracted) - len(retained),
            "images_without_description": sum(record["images_without_description"] for record in retained),
        })
    total = sum(source["word_count"] for source in summaries)
    if len(summaries) < 3 or total < 50_000:
        raise ValueError(f"Corpus below assignment minimum: {len(summaries)} documents, {total:,} words")
    output_dir = ROOT / "corpus" / "prepared"
    output_dir.mkdir(exist_ok=True)
    (output_dir / "sections.jsonl").write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")
    manifest = {
        "prepared_on": datetime.now(ZoneInfo("Europe/Madrid")).isoformat(),
        "word_count_method": "Unicode word tokens in retained section text, before chunking and without overlap",
        "documents": len(summaries),
        "sections": len(records),
        "total_words": total,
        "sources": summaries,
        "scope_status": config["corpus_scope_status"],
        "limitations": config["corpus_limitations"],
    }
    (ROOT / "corpus_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for source in summaries:
        print(f"{source['title']}: {source['word_count']:,} words / {source['selected_section_count']} sections")
    print(f"Total: {total:,} words across {len(summaries)} documents. No embeddings requested.")
    return records, manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Download missing source files")
    prepare(download=parser.parse_args().download)
