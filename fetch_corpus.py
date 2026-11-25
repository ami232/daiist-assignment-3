"""Download the EUR-Lex HTML texts. Run once: `uv run python main.py fetch`.

EUR-Lex content may be reused under Commission Decision 2011/833/EU (attribution: (c) European Union,
https://eur-lex.europa.eu). If EUR-Lex answers with a bot-check page instead of the law, open the URL
printed below in a browser, 'Save page as' HTML, and put the file at the printed path."""
import re
import sys

import requests

from config import CORPUS, ROOT

URLS = ["https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{c}",
        "https://publications.europa.eu/resource/celex/{c}"]


def fetch_all(only: list[str] | None = None) -> int:
    bad = 0
    for doc_id, meta in CORPUS.items():
        if only and doc_id not in only:
            continue
        out = ROOT / meta["dir"] / f"{doc_id}.html"
        out.parent.mkdir(exist_ok=True)
        if out.exists() and len(re.findall(rb"Article\s+\d+", out.read_bytes())) >= 40:
            print(f"ok (cached) {out}")
            continue
        for u in URLS:
            url = u.format(c=meta["celex"])
            try:
                r = requests.get(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html",
                                               "Accept-Language": "en"}, timeout=90)
            except requests.RequestException as e:
                print(f"  {url}: {e}")
                continue
            if r.ok and len(re.findall(rb"Article\s+\d+", r.content)) >= 40:
                out.write_bytes(r.content)
                print(f"saved {out} ({len(r.content)//1000} kB)")
                break
            print(f"  {url}: HTTP {r.status_code}, {len(r.content)} bytes (not the law text)")
        else:
            bad += 1
            print(f"!! could not fetch {doc_id}. Save {URLS[0].format(c=meta['celex'])} manually as {out}")
    return bad


if __name__ == "__main__":
    sys.exit(fetch_all(sys.argv[1:] or None))