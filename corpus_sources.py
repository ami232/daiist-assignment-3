"""Corpus sources: Spanish anti-doping law, as published in the BOE.

Every text is downloaded from the BOE open-data API for consolidated legislation
(https://www.boe.es/datosabiertos/), which returns the norm split into blocks
(article, chapter, annex...). BOE texts are legal provisions and official acts,
excluded from copyright by art. 13 of the Spanish Intellectual Property Law, and
the BOE allows their reuse citing the source.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{id}/texto"

# Indexed from the start.
SOURCES = {
    "LO_11_2021": {
        "boe_id": "BOE-A-2021-21650",
        "title": "Ley Orgánica 11/2021, de lucha contra el dopaje en el deporte",
    },
    "RD_792_2023": {
        "boe_id": "BOE-A-2023-21845",
        "title": "Real Decreto 792/2023, Reglamento de desarrollo de la LO 11/2021 (consolidado)",
    },
    "CMA_2021": {
        "boe_id": "BOE-A-2023-3345",
        "title": "Código Mundial Antidopaje (publicado por Resolución del CSD de 1 de febrero de 2023)",
    },
}

# Held out: added later through the add-document tool (assignment step 8).
HELD_OUT = {
    "LISTA_2026": {
        "boe_id": "BOE-A-2025-25042",
        "title": "Lista de sustancias y métodos prohibidos en el deporte para 2026",
    },
}


def xml_path(name: str) -> Path:
    return CORPUS_DIR / f"{name}.xml"


def download(name: str, boe_id: str, force: bool = False) -> Path:
    """Download one norm's consolidated XML into corpus/ unless it is already there."""
    path = xml_path(name)
    if path.exists() and not force:
        return path
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    response = httpx.get(
        API.format(id=boe_id),
        headers={"Accept": "application/xml"},
        timeout=60,
        follow_redirects=True,
    )
    response.raise_for_status()
    path.write_bytes(response.content)
    return path


if __name__ == "__main__":
    for name, meta in {**SOURCES, **HELD_OUT}.items():
        p = download(name, meta["boe_id"])
        print(f"{name:12s} {meta['boe_id']}  {p.stat().st_size/1e3:8.0f} KB  -> {p.relative_to(ROOT)}")
