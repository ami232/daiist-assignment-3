import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DOCS = {
    "money_laundering_regs_2017": "uksi/2017/692",
    "payment_services_regs_2017": "uksi/2017/752",
    "electronic_money_regs_2011": "uksi/2011/99",
}

OUT = Path("corpus/raw")
OUT.mkdir(parents=True, exist_ok=True)

total = 0
for name, path in DOCS.items():
    url = f"https://www.legislation.gov.uk/{path}/data.xml"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (course assignment)"})
    data = urllib.request.urlopen(req, timeout=60).read()
    (OUT / f"{name}.xml").write_bytes(data)
    text = " ".join(ET.fromstring(data).itertext())
    words = len(text.split())
    total += words
    print(f"{name}: {words:,} words")

print(f"TOTAL: {total:,} words (need at least 50,000)")