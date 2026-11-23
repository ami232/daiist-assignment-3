"""
Corpus download and text extraction (step 1). index.py and server.py import from here.

Statutes: gesetze-im-internet.de XML (one zip per law).
Judgments: rechtsprechung-im-internet.de XML (one zip per decision, BGH VIII ZR).

Each document becomes a list of *units* (one § or one Randnummer) with source and
location metadata, saved as corpus/text/<doc_id>.jsonl plus a readable .txt.
"""

from __future__ import annotations

import io
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
RAW = CORPUS / "raw"
TEXT = CORPUS / "text"
UA = {"User-Agent": "corpus-builder/0.1 (student project)"}

# doc_id -> (gesetze-im-internet slug, first §, last §) ; None = whole law
STATUTES = {
    "BGB": ("bgb", "§ 535", "§ 580a"),
    "BetrKV": ("betrkv", None, None),
    "HeizkostenV": ("heizkostenv", None, None),
    "CO2KostAufG": ("co2kostaufg", None, None),
}

# BGH VIII. Zivilsenat decisions, pinned to their rechtsprechung-im-internet.de file id.
# Chosen from a screen of 942 VIII ZR decisions (2014 - May 2026, Nov 2024 - Dec 2025 not screened).
JUDGMENTS = {
    "VIII ZR 137/15": "jb-KORE312802016",  # "die Betriebskosten" suffices as Umlagevereinbarung
    "VIII ZR 36/14": "jb-JURE140012684",   # implied change of the Umlagevereinbarung
    "VIII ZR 254/17": "jb-KORE308112019",  # Verwaltungskostenpauschale void (§ 556 Abs. 4)
    "VIII ZR 93/15": "jb-KORE312712016",   # formal validity: adjusted Gesamtkosten suffice
    "VIII ZR 249/15": "jb-KORE300602017",  # 12-month deadline despite missing WEG resolution
    "VIII ZR 209/15": "jb-KORE313462016",  # Einwendungsausschluss covers non-billable costs
    "VIII ZR 379/20": "jb-KORE317382022",  # smoke detector rental not billable
    "VIII ZR 117/21": "jb-KORE307522022",  # waste-sorting checks; smoke detector maintenance billable
    "VIII ZR 107/20": "jb-KORE312732021",  # tree felling = Gartenpflege
    "VIII ZR 62/19": "jb-KORE300202020",   # caretaker emergency flat fee = Verwaltungskosten
    "VIII ZR 220/17": "jb-KORE301092018",  # actual floor area, not contract area
    "VIII ZR 79/16": "jb-KORE301452017",   # Grundsteuer, mixed use: no Vorwegabzug
    "VIII ZR 151/20": "jb-KORE300612022",  # missing heat meter -> § 12 HeizkostenV deduction
    "VIII ZR 230/21": "jb-KORE310492023",  # Wirtschaftlichkeitsgebot, pre-existing contracts, burden
    "VIII ZR 47/25": "jb-KORE303652026",   # § 556c not applicable to switch from tenant stoves
    "VIII ZR 9/14": "jb-KORE302612015",    # hot water costs with high vacancy
    "VIII ZR 118/19": "jb-KORE308812020",  # Belegeinsicht includes payment receipts
}
# Kept out of the base index; added later through the add_document tool.
HOLDOUT = {"VIII ZR 6/24": "jb-KORE303622026"}  # no duty to get comparison quotes; objectively overpriced
PORTAL = "https://www.rechtsprechung-im-internet.de/jportal/docs/bsjrs/{}.zip"

BLOCK_TAGS ={"P", "DT", "DD", "LA", "row", "TITLE", "BR", "p", "br", "li", "tr", "dd"}

# Formulas published only as images, transcribed by hand from the image in the XML zip.
IMAGE_TEXT = {"bgbl1_2021_j4964-1_0010.jpg": "B = Q / Hi [Formel aus Bild übertragen]"}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def fetch(url: str, retries: int = 3) -> bytes:
    for attempt in range(retries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        except Exception as error:  # noqa: BLE001
            log(f"fetch failed ({attempt + 1}/{retries}) {url}: {error}")
            time.sleep(3)
    raise RuntimeError(f"could not download {url}")


def unzip_xml(data: bytes) -> bytes:
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        name = next(n for n in zf.namelist() if n.lower().endswith(".xml"))
        return zf.read(name)


# ---------------------------------------------------------------- text helpers

def _render(el: ET.Element) -> str:
    """Flatten an XML fragment to text, keeping paragraphs, list items and table rows apart."""
    if el.tag == "row":
        cells = [" ".join(_render(c).split()) for c in el.iter("entry")]
        return "\n" + " | ".join(cells) + "\n"
    if el.tag == "IMG":
        return " " + IMAGE_TEXT.get(el.get("SRC", ""), "[Bild, nicht extrahiert]") + " "
    parts = [el.text or ""]
    for child in el:
        parts.append(_render(child))
        parts.append(child.tail or "")
    text = "".join(parts)
    if el.tag in BLOCK_TAGS:
        text = "\n" + text + "\n"
    if el.tag == "DT":
        text = "\n" + text.strip() + " "
    return text


def clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    lines = [" ".join(line.split()) for line in text.split("\n")]
    out, blank = [], False
    for line in lines:
        if not line:
            blank = True
            continue
        out.append(line)
        blank = False
    # glue "1." list labels to their item text
    joined = "\n".join(out)
    joined = re.sub(r"\n(\d+[a-z]?\.|[a-z]\))\n", r"\n\1 ", joined)
    return joined.strip()


# ---------------------------------------------------------------- statutes

def download_statute(doc_id: str) -> Path:
    slug = STATUTES[doc_id][0]
    dest = RAW / slug / f"{slug}.xml"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(unzip_xml(fetch(f"https://www.gesetze-im-internet.de/{slug}/xml.zip")))
    return dest


def extract_statute(doc_id: str, xml_path: Path) -> list[dict]:
    _, first, last = STATUTES[doc_id]
    root = ET.parse(xml_path).getroot()
    norms = root.findall("norm")
    head = norms[0].find("metadaten")
    version = "; ".join(" ".join(s.itertext()).strip() for s in head.iter("standkommentar"))
    build = root.get("builddate", "")[:8]
    units, inside = [], first is None
    for norm in norms[1:]:
        meta = norm.find("metadaten")
        enbez = (meta.findtext("enbez") or "").strip()
        if enbez == first:
            inside = True
        if inside and enbez.startswith(("§", "Anlage", "Anhang")):
            content = norm.find("textdaten/text/Content")
            body = clean(_render(content)) if content is not None else ""
            if body and body != "-" and "(weggefallen)" not in body[:20]:
                units.append({
                    "doc_id": doc_id,
                    "doc_type": "statute",
                    "location": f"{enbez} {doc_id}",
                    "title": (meta.findtext("titel") or "").strip(),
                    "text": body,
                    "version": version,
                    "retrieved": build,
                    "url": f"https://www.gesetze-im-internet.de/{STATUTES[doc_id][0]}/",
                })
        if enbez == last:
            break
    return units


# ---------------------------------------------------------------- judgments

JUDG_SECTIONS = [  # (xml tag, label, keep?)
    ("leitsatz", "Leitsatz", True),
    ("tenor", "Tenor", True),
    ("tatbestand", "Tatbestand", True),
    ("entscheidungsgruende", "Entscheidungsgründe", True),
    ("gruende", "Gründe", True),
]


def download_judgment(file_id: str, folder: Path = RAW / "bgh") -> Path:
    dest = folder / f"{file_id}.xml"
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(unzip_xml(fetch(PORTAL.format(file_id))))
        time.sleep(1)  # the portal rate-limits
    return dest


def _rn_blocks(section: ET.Element) -> list[tuple[str | None, str]]:
    """Split a judgment section into (Randnummer, text). Rn. sit in <dl class="RspDL"><dt>n</dt><dd>…</dd>."""
    blocks: list[tuple[str | None, str]] = []
    # <dl> nested inside a <dd> (quoted clauses) is already part of its parent's text
    nested = {id(d) for dd in section.iter("dd") for d in dd.iter("dl")}
    for dl in section.iter("dl"):
        if id(dl) in nested:
            continue
        dt, dd = dl.find("dt"), dl.find("dd")
        if dd is None:
            continue
        rn = " ".join("".join(dt.itertext()).split()) if dt is not None else None
        text = clean(_render(dd))
        if not text:
            continue
        lines = text.split("\n")
        if not rn and len(text.split()) < 25 and all(len(line.split()) <= 3 for line in lines):
            continue  # judges' signatures
        if not rn and blocks and blocks[-1][0]:
            blocks[-1] = (blocks[-1][0], blocks[-1][1] + "\n" + text)  # unnumbered paragraph continues the Rn.
            continue
        blocks.append((rn or None, text))
    if not blocks:
        text = clean(_render(section))
        if text:
            blocks.append((None, text))
    # sections without Rn. (Leitsatz, Tenor) come as several <dl>: keep them as one unit
    if all(rn is None for rn, _ in blocks) and len(blocks) > 1:
        blocks = [(None, "\n".join(t for _, t in blocks))]
    return blocks


def extract_judgment(xml_path: Path) -> list[dict]:
    root = ET.parse(xml_path).getroot()
    az = " ".join((root.findtext(".//aktenzeichen") or "").split())
    date = (root.findtext(".//entsch-datum") or "").strip()
    doktyp = (root.findtext(".//doktyp") or "").strip()
    doc_id = f"BGH {az}"
    headline = clean(_render(root.find(".//titelzeile"))) if root.find(".//titelzeile") is not None else ""
    date_iso = f"{date[:4]}-{date[4:6]}-{date[6:8]}" if len(date) == 8 else date
    units = []
    for tag, label, keep in JUDG_SECTIONS:
        section = root.find(f".//{tag}")
        if section is None or not keep:
            continue
        for rn, text in _rn_blocks(section):
            units.append({
                "doc_id": doc_id,
                "doc_type": "judgment",
                "location": f"{doc_id}, Rn. {rn}" if rn else f"{doc_id}, {label}",
                "title": f"{doktyp} vom {date_iso}: {headline}",
                "section": label,
                "text": text,
                "decision_date": date_iso,
                "url": f"https://www.rechtsprechung-im-internet.de/jportal/?quelle=jlink&docid={xml_path.stem.removeprefix('jb-')}&psml=bsjrsprod.psml",
            })
    return units


# ---------------------------------------------------------------- output

def save(doc_id: str, units: list[dict]) -> Path:
    TEXT.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^A-Za-z0-9]+", "_", doc_id).strip("_")
    with (TEXT / f"{stem}.jsonl").open("w", encoding="utf-8") as f:
        for u in units:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")
    txt = TEXT / f"{stem}.txt"
    txt.write_text("\n\n".join(f"[{u['location']}] {u.get('title', '')}\n{u['text']}" for u in units), encoding="utf-8")
    return txt


def word_count(units: list[dict]) -> int:
    return sum(len(u["text"].split()) for u in units)


def build_corpus() -> list[tuple[str, int, int]]:
    """Download (if missing) and extract every base document. Returns (doc_id, units, words)."""
    rows = []
    for doc_id in STATUTES:
        units = extract_statute(doc_id, download_statute(doc_id))
        save(doc_id, units)
        rows.append((doc_id, len(units), word_count(units)))
    for az, file_id in JUDGMENTS.items():
        units = extract_judgment(download_judgment(file_id))
        save(units[0]["doc_id"], units)
        rows.append((units[0]["doc_id"], len(units), word_count(units)))
    for file_id in HOLDOUT.values():  # raw file only, for the add-document demo
        download_judgment(file_id, CORPUS / "holdout")
    return rows


if __name__ == "__main__":
    rows = build_corpus()
    for doc_id, n_units, words in rows:
        print(f"{doc_id:18} {n_units:4} units {words:7,} words")
    print(f"{'TOTAL':18} {sum(r[1] for r in rows):4} units {sum(r[2] for r in rows):7,} words")
    for az, file_id in HOLDOUT.items():
        units = extract_judgment(CORPUS / "holdout" / f"{file_id}.xml")
        print(f"holdout (not in base): BGH {az} {len(units)} units {word_count(units):,} words")
