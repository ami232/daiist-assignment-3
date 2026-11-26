"""Reproduce candidate corpus extraction. This command never embeds documents.

Source selection is proposed for Jimena's review. Text only: no images, logos
or linked third-party content are copied into the retrieval corpus.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
SOURCES = [
    {
        "source": "operations",
        "title": "Introduction to Operations Management",
        "url": "https://storage.downloads.libretexts.org/pdf/biz-117227/Full.pdf?response-content-disposition=inline%3B+filename%3D%22Full.pdf%22&v=e9bd74226976581b60b1a72e465ea8bf-2",
        "landing_url": "https://biz.libretexts.org/Bookshelves/Management/Introduction_to_Operations_Management",
        "raw": "operations.pdf",
        "candidate": "operations-libretexts.pdf",
        "path": "corpus/operations.md",
        "license": "CC BY-NC 4.0, with source adaptation attribution retained; noncommercial academic use only",
        "license_url": "https://creativecommons.org/licenses/by-nc/4.0/",
        "attribution": "Mary Drane and Hamid Faramarzi / Seneca College; LibreTexts adaptation. Original source credits retained in the PDF. Detailed licensing: PDF pages 135–138.",
        "date": "2026-05-05 PDF compilation",
        "first_page": 9,
        "last_page": 134,
        "scope": "Operations, forecasting, supply chains, quality, capacity and facility planning.",
        "exclusions": "PDF pages 1–8: front matter including undeclared-licence contents; pages 135–138: duplicated licensing lists. Images and video embeds not ingested.",
    },
    {
        "source": "fema",
        "title": "Supply Chain Resilience Guide",
        "url": "https://www.fema.gov/sites/default/files/2020-07/supply-chain-resilience-guide.pdf",
        "landing_url": "https://www.fema.gov/sites/default/files/2020-07/supply-chain-resilience-guide.pdf",
        "raw": "fema.pdf",
        "candidate": "fema-resilience.pdf",
        "path": "corpus/fema.md",
        "license": "U.S. federal government-authored guidance: public-domain basis in the U.S.; excludes third-party images and linked works",
        "license_url": "https://www.loc.gov/legal/security-copyright-and-privacy/understanding-copyright/",
        "attribution": "Federal Emergency Management Agency, Supply Chain Resilience Guide, April 2019. No endorsement implied.",
        "date": "2019-04",
        "first_page": 3,
        "last_page": 44,
        "scope": "Disaster supply-chain mapping, dependencies, stakeholder coordination and exercises. Written for emergency managers, not specifically online retailers.",
        "exclusions": "Cover, intentionally blank pages, repeated headers/footers, images and linked third-party works.",
    },
    {
        "source": "uk-strategy",
        "title": "Critical imports and supply chains strategy",
        "url": "https://www.gov.uk/government/publications/uk-critical-imports-and-supply-chains-strategy/critical-imports-and-supply-chains-strategy-html-version",
        "landing_url": "https://www.gov.uk/government/publications/uk-critical-imports-and-supply-chains-strategy",
        "raw": "uk-strategy.html",
        "candidate": "uk-strategy.html",
        "path": "corpus/uk-strategy.md",
        "license": "Open Government Licence v3.0, except otherwise stated; text only",
        "license_url": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        "attribution": "Department for Business and Trade, Critical imports and supply chains strategy, Crown copyright 2024, Open Government Licence v3.0. No endorsement implied.",
        "date": "2024-01-17",
        "scope": "Supply-chain vulnerability, diversification, visibility and resilience. UK policy context is not Spanish law or live commercial intelligence.",
        "exclusions": "Site navigation, images, scripts, forms and footnote backlinks.",
    },
]


def clean(text: str) -> str:
    text = text.replace("\x00", "").replace("\ufb01", "fi").replace("\ufb02", "fl")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if re.match(r"^\d+(?:\.\d+)*\s+https://biz\.libretexts\.org/", line):
            continue
        if line in {
            "Supply Chain Resilience Guide",
            "This page intentionally left blank",
        }:
            continue
        lines.append(line)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def download(source: dict, raw_directory: Path) -> Path:
    path = raw_directory / source["raw"]
    if not path.exists():
        cached = ROOT / "corpus" / "candidates" / source["candidate"]
        if cached.exists():
            shutil.copy2(cached, path)
        else:
            response = httpx.get(source["url"], follow_redirects=True, timeout=60)
            response.raise_for_status()
            path.write_bytes(response.content)
    return path


def prepare() -> list[dict]:
    raw_directory = ROOT / "corpus" / "raw"
    raw_directory.mkdir(parents=True, exist_ok=True)
    manifest = []
    for source in SOURCES:
        path = download(source, raw_directory)
        sections = []
        if path.suffix == ".pdf":
            reader = PdfReader(path)
            for number in range(source["first_page"], source["last_page"] + 1):
                text = clean(reader.pages[number - 1].extract_text() or "")
                if text:
                    sections.append((f"PDF page {number}", text))
        else:
            soup = BeautifulSoup(path.read_text(), "html.parser")
            body = soup.select_one(".gem-c-govspeak")
            if body is None:
                raise ValueError(
                    "GOV.UK article container not found; do not ingest site navigation."
                )
            for element in body.select("script, style, img, svg, .footnote-backref"):
                element.decompose()
            heading, fragments = "Introduction", []
            outline = {}
            for element in body.find_all(["h2", "h3", "h4", "p", "li"]):
                if element.name.startswith("h"):
                    if fragments:
                        sections.append(
                            (f"section: {heading}", clean(" ".join(fragments)))
                        )
                    level = int(element.name[1])
                    outline = {
                        key: value for key, value in outline.items() if key < level
                    }
                    outline[level] = element.get_text(" ", strip=True)
                    heading, fragments = " / ".join(outline.values()), []
                elif (
                    element.name == "p"
                    and element.find_parent("li")
                    or element.name == "li"
                    and element.find_parent("li")
                ):
                    continue
                else:
                    fragments.append(element.get_text(" ", strip=True))
            if fragments:
                sections.append((f"section: {heading}", clean(" ".join(fragments))))
        # Attribution is in SOURCES.json/CORPUS_NOTICES.md, not duplicated as retrieval evidence.
        output = (
            "\n\n".join(
                f"<!-- source-location: {location} -->\n{text}"
                for location, text in sections
            )
            + "\n"
        )
        (ROOT / source["path"]).write_text(output)
        manifest.append(
            {
                **source,
                "words": sum(len(text.split()) for _, text in sections),
                "locations": len(sections),
                "raw_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "clean_sha256": hashlib.sha256(output.encode()).hexdigest(),
                "privacy_review": "Public reference publications; no private customer, employee, order or shipment records. Public bibliographic attribution may name authors.",
            }
        )
    (ROOT / "corpus" / "SOURCES.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    )
    return manifest


if __name__ == "__main__":
    manifest = prepare()
    print(
        json.dumps(
            {
                "total_words": sum(d["words"] for d in manifest),
                "documents": [
                    {key: d[key] for key in ["source", "words", "locations"]}
                    for d in manifest
                ],
            },
            indent=2,
        )
    )
