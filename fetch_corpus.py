"""Download the SEC corpus into corpus/ and count its words.

    uv run python fetch_corpus.py            # download what is missing, then count
    uv run python fetch_corpus.py --force    # download everything again
    uv run python fetch_corpus.py --count    # only count what is already in corpus/

index.py can import download_corpus() so `main.py index` needs no manual step
(corpus/ is git-ignored, so the grader's machine has to download it too).

Every source is written by the U.S. Securities and Exchange Commission (sec.gov,
investor.gov). Works created by the US government are not protected by copyright.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
TARGET_WORDS = 50_000
PAUSE_SECONDS = 0.5  # stay well under the SEC's request-rate limit
DEFAULT_CONTACT = "marta.bermejo.v@gmail.com"  

BD = "https://www.sec.gov/about/divisions-offices/division-trading-markets/broker-dealers/"
INV = "https://www.investor.gov/"

# (slug, title, url). Slugs become file names and the "source" in chunk metadata.
DOCS: list[tuple[str, str, str]] = [
    # Regulation Best Interest and Form CRS (sec.gov)
    ("reg-bi-compliance-guide", "Regulation Best Interest: Small Entity Compliance Guide",
     "https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/regulation-best-interest"),
    ("form-crs-compliance-guide", "Form CRS Relationship Summary: Small Entity Compliance Guide",
     "https://www.sec.gov/info/smallbus/secg/form-crs-relationship-summary"),
    ("staff-bulletin-care-obligations",
     "Staff Bulletin: Standards of Conduct for Broker-Dealers and Investment Advisers, Care Obligations",
     BD + "staff-bulletin-standards-conduct-broker-dealers-investment-advisers-care-obligations"),
    ("staff-bulletin-conflicts-of-interest",
     "Staff Bulletin: Standards of Conduct for Broker-Dealers and Investment Advisers, Conflicts of Interest",
     BD + "staff-bulletin-standards-conduct-broker-dealers-investment-advisers-conflicts-interest"),
    ("staff-bulletin-account-recommendations",
     "Staff Bulletin: Standards of Conduct for Broker-Dealers and Investment Advisers, Account Recommendations for Retail Investors",
     BD + "staff-bulletin-standards-conduct-broker-dealers-investment-advisers-account-recommendations-retail"),
    ("reg-bi-faq", "Regulation Best Interest: Frequently Asked Questions",
     "https://www.sec.gov/tm/faq-regulation-best-interest"),
    ("form-crs-faq", "Form CRS: Frequently Asked Questions",
     "https://www.sec.gov/investment/form-crs-faq"),
    ("staff-statement-form-crs-disclosures",
     "Staff Statement Regarding Form CRS Disclosures (December 17, 2021)",
     "https://www.sec.gov/newsroom/speeches-statements/staff-statement-form-crs-disclosures-121721"),
    # Investor education (investor.gov). Only pages with real text: the hub pages (Types of Fraud,
    # How to Avoid Fraud, Investment Products...) are mostly lists of links and would add noise.
    ("inv-five-questions", "Five Questions to Ask Before You Invest",
     INV + "introduction-investing/getting-started/five-questions-ask-you-invest"),
    ("inv-understanding-fees", "Understanding Fees",
     INV + "introduction-investing/getting-started/understanding-fees"),
    ("inv-working-with-professional", "Working with an Investment Professional",
     INV + "introduction-investing/getting-started/working-investment-professional"),
    ("inv-common-scams", "Common Scams",
     INV + "additional-resources/spotlight/common-scams"),
    ("inv-crypto-assets", "Crypto Assets",
     INV + "additional-resources/spotlight/crypto-assets"),
]


def user_agent(url: str) -> str:
    """sec.gov asks bots to declare a contact email; investor.gov's firewall rejects an email in the header."""
    host = urlparse(url).hostname or ""
    if host.endswith("sec.gov") and not host.endswith("investor.gov"):
        # sec.gov answers 403 to requests without an email. The grader's machine will not have
        # SEC_CONTACT set, so the default below must be a real address of yours.
        contact = os.getenv("SEC_CONTACT", "").strip() or DEFAULT_CONTACT
        if contact == DEFAULT_CONTACT and "CHANGE_ME" in contact:
            print("WARNING: replace DEFAULT_CONTACT in fetch_corpus.py with your own email.", file=sys.stderr)
        return f"DAIIST coursework RAG project {contact}".strip()
    return "DAIIST coursework RAG project"


def html_to_markdown(html: str) -> str:
    """Keep the main content, drop navigation and scripts, keep headings as # lines."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "noscript", "svg", "button"]):
        tag.decompose()
    # sec.gov has <main>; investor.gov has no <main> and its #main-content is an empty anchor, so
    # take the first candidate that really holds text.
    candidates = [soup.find("main"), soup.find("article"), soup.select_one("#content"),
                  soup.find(id="main-content"), soup.body, soup]
    main = next((c for c in candidates if c is not None and len(c.get_text(" ", strip=True).split()) > 50), soup)
    text = markdownify(str(main), heading_style="ATX", strip=["a", "img"])
    text = re.sub(r"^#+[ \t]*$", "", text, flags=re.M)  # empty headings left by the page template
    # The staff bulletins mark their sections with a bold line, not a heading: promote those lines.
    text = re.sub(r"^\*\*([^*\n]{3,120})\*\*[ \t]*$", r"### \1", text, flags=re.M)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def save_document(slug: str, title: str, url: str, body: str) -> Path:
    header = (
        "---\n"
        f"title: {json.dumps(title)}\n"
        f"source_url: {url}\n"
        f"retrieved: {datetime.date.today().isoformat()}\n"
        "publisher: U.S. Securities and Exchange Commission\n"
        "licence: US government work (public domain)\n"
        "---\n\n"
    )
    path = CORPUS_DIR / f"{slug}.md"
    path.write_text(header + body + "\n", encoding="utf-8")
    return path


def download_corpus(force: bool = False) -> list[tuple[str, str]]:
    """Download every document that is not in corpus/ yet. Returns [(slug, error)] for failures."""
    CORPUS_DIR.mkdir(exist_ok=True)
    failures: list[tuple[str, str]] = []
    for slug, title, url in DOCS:
        if (CORPUS_DIR / f"{slug}.md").exists() and not force:
            continue
        try:
            headers = {"User-Agent": user_agent(url), "Accept": "text/html"}
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            path = save_document(slug, title, url, html_to_markdown(response.text))
            print(f"saved {path.name}")
        except Exception as error:  # noqa: BLE001 - report and carry on with the others
            failures.append((slug, f"{type(error).__name__}: {error}"))
            print(f"FAILED {slug}: {error}", file=sys.stderr)
        time.sleep(PAUSE_SECONDS)
    return failures


def count_words() -> int:
    files = sorted(CORPUS_DIR.glob("*.md")) if CORPUS_DIR.is_dir() else []
    total = 0
    print(f"\n{'document':<45}{'words':>8}")
    print("-" * 53)
    for path in files:
        text = path.read_text(encoding="utf-8")
        body = text.split("---", 2)[2] if text.startswith("---") else text
        words = len(body.split())
        total += words
        flag = "  <- short, check it" if words < 300 else ""
        print(f"{path.stem:<45}{words:>8}{flag}")
    print("-" * 53)
    print(f"{'TOTAL (' + str(len(files)) + ' documents)':<45}{total:>8}")
    if total < TARGET_WORDS:
        print(f"\nBelow the {TARGET_WORDS:,} words required: add more pages to DOCS.")
    elif total < TARGET_WORDS * 1.1:
        print("\nOver the minimum but with little margin; aim for about 10% more.")
    else:
        print(f"\nOver the {TARGET_WORDS:,} words required.")
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="download everything again")
    parser.add_argument("--count", action="store_true", help="only count the words already in corpus/")
    args = parser.parse_args()
    if not args.count:
        failures = download_corpus(force=args.force)
        if failures:
            print(f"\n{len(failures)} download(s) failed; run again or check the URLs.", file=sys.stderr)
    count_words()


if __name__ == "__main__":
    main()