"""
Ayuda para ELEGIR el corpus (no forma parte del pipeline): busca licitaciones en el feed
de datos abiertos de la PLACSP y te da el bloque listo para pegar en TENDERS (index.py).

    uv run python buscar_licitaciones.py --texto ciberseguridad --cpv 72
    uv run python buscar_licitaciones.py --texto "limpieza" --cpv 90 --paginas 10
    uv run python buscar_licitaciones.py --texto ciberseguridad --mostrar 3   # bloque para index.py

Solo lista licitaciones sujetas a regulación armonizada (publicadas también en TED) que
tienen PCAP y PPT. El feed trae ~350 licitaciones por página, de las más recientes a las
más antiguas.
"""

import argparse
import json
import re
import xml.etree.ElementTree as ET

import httpx

FEED = "https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3.atom"
TED_API = "https://api.ted.europa.eu/v3/notices/search"
NS = {"a": "http://www.w3.org/2005/Atom",
      "cbc": "urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2",
      "cac": "urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2",
      "cacx": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2",
      "cbcx": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2"}
STATUS = {"PUB": "en plazo", "EV": "en evaluación", "ADJ": "adjudicada", "RES": "resuelta", "PRE": "anuncio previo"}
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}


def entries(pages: int):
    url = FEED
    for _ in range(pages):
        root = ET.fromstring(httpx.get(url, headers=UA, timeout=120).content)
        for e in root.findall("a:entry", NS):
            cfs = e.find("cacx:ContractFolderStatus", NS)
            if cfs is None:
                continue
            get = lambda p: cfs.findtext(p, namespaces=NS)  # noqa: E731
            yield {
                "tender_id": get("cbc:ContractFolderID"),
                "status": get("cbcx:ContractFolderStatusCode"),
                "buyer": get("cacx:LocatedContractingParty/cac:Party/cac:PartyName/cbc:Name"),
                "title": (e.findtext("a:title", namespaces=NS) or "").replace("\n", " ").strip(),
                "amount": get("cac:ProcurementProject/cac:BudgetAmount/cbc:TaxExclusiveAmount"),
                "deadline": get("cac:TenderingProcess/cac:TenderSubmissionDeadlinePeriod/cbc:EndDate"),
                "sara": get("cac:TenderingProcess/cbc:OverThresholdIndicator") == "true",
                "cpv": [x.text for x in cfs.iter(f"{{{NS['cbc']}}}ItemClassificationCode")],
                "pcap": get("cac:LegalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:URI"),
                "ppt": get("cac:TechnicalDocumentReference/cac:Attachment/cac:ExternalReference/cbc:URI"),
                "placsp": e.find("a:link", NS).get("href"),
            }
        nxt = [l.get("href") for l in root.findall("a:link", NS) if l.get("rel") == "next"]
        if not nxt:
            break
        url = nxt[0]


def find_ted(tender_id: str) -> str:
    body = {"query": f'internal-identifier-proc="{tender_id}" AND notice-type=cn-standard',
            "fields": ["publication-number"], "limit": 1}
    try:
        notices = httpx.post(TED_API, json=body, timeout=60).json().get("notices", [])
        return notices[0]["publication-number"] if notices else ""
    except Exception:  # noqa: BLE001
        return ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--texto", default="", help="palabra en el título o el órgano")
    ap.add_argument("--cpv", default="", help="prefijo CPV, p. ej. 72 (servicios TI) o 79 (servicios a empresas)")
    ap.add_argument("--paginas", type=int, default=5)
    ap.add_argument("--mostrar", type=int, default=0, help="nº de la lista para imprimir su bloque TENDERS")
    args = ap.parse_args()

    found = []
    for t in entries(args.paginas):
        if not (t["sara"] and t["pcap"] and t["ppt"]):
            continue
        if args.cpv and not any(c and c.startswith(args.cpv) for c in t["cpv"]):
            continue
        if args.texto and args.texto.lower() not in (t["title"] + " " + (t["buyer"] or "")).lower():
            continue
        if any(f["tender_id"] == t["tender_id"] and f["buyer"] == t["buyer"] for f in found):
            continue
        found.append(t)

    for n, t in enumerate(found, 1):
        print(f"{n:3}. [{STATUS.get(t['status'], t['status'])}] {t['tender_id']} · {t['buyer'][:55]} · "
              f"{float(t['amount'] or 0):,.0f} € · plazo {t['deadline']}\n     {t['title'][:110]}")
    if args.mostrar:
        t = found[args.mostrar - 1]
        key = re.sub(r"[^a-z0-9]+", "_", t["buyer"].lower())[:12].strip("_")
        block = {"key": key, "tender_id": t["tender_id"], "buyer": t["buyer"], "title": t["title"][:90],
                 "aliases": [key, t["tender_id"].lower()], "placsp": t["placsp"],
                 "pcap": t["pcap"], "ppt": t["ppt"], "ted": find_ted(t["tender_id"])}
        print("\nPega esto en TENDERS (index.py) y revisa key, title y aliases:\n")
        print(json.dumps(block, ensure_ascii=False, indent=4) + ",")
        if not block["ted"]:
            print("\n(No encontré el anuncio en TED: búscalo en ted.europa.eu y pon su número en 'ted'.)")


if __name__ == "__main__":
    main()
