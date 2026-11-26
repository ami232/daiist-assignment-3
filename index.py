"""
Assignment 3: construir el índice (`uv run python main.py index`).

Pipeline, en este orden (cada paso es una función que puedes leer por separado):

  1. download_sources()  descarga los pliegos de la PLACSP y los anuncios de TED a corpus/
  2. extract_pages()     PDF -> texto por página (TED: JSON -> texto por secciones)
  3. redact()            borra datos personales (firmas, nombres, emails, teléfonos, DNI)
  4. clean_pages()       quita cabeceras/pies repetidos, índices, guiones de fin de línea...
                         (prepare_pages() hace 3 + 4 + una segunda pasada de redact)
  5. chunk_pages()       trocea con uno de los diseños de config.CHUNK_DESIGNS
  6. embed_and_store()   pide a Gemini los embeddings SOLO de los fragmentos que aún no
                         tienen vector y los guarda en ChromaDB (index/chroma) lote a lote

server.py importa `chunk_file()` y `embed_and_store()` para su herramienta add_document,
así que esas dos funciones son la "API" de este módulo.

Volver a ejecutarlo es barato: un fragmento ya guardado (mismo texto -> mismo id) no se
vuelve a mandar a Gemini. Si se acaba la cuota diaria, guarda lo hecho y para; mañana
lo vuelves a ejecutar y sigue donde se quedó.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

import config

# ======================================================================================
# 1. EL CORPUS
# ======================================================================================
# >>> DECISIÓN TUYA: qué licitaciones forman el corpus. <<<
# Cada licitación aporta 3 documentos: PCAP (cláusulas administrativas), PPT
# (prescripciones técnicas), ambos de la PLACSP, y su anuncio en TED.
# Para cambiar de licitaciones usa buscar_licitaciones.py y pega aquí sus datos.
PLACSP_LICENCE = "Reutilización permitida (Ley 37/2007 de reutilización de la información del sector público); fuente: PLACSP"
TED_LICENCE = "Reutilización libre (política de reutilización de la Comisión, Decisión 2011/833/UE; aviso legal de TED)"

TENDERS = [
    {
        "key": "cartagena",
        "tender_id": "SE2026/44",
        "buyer": "Ayuntamiento de Cartagena",
        "title": "Servicio de SOC/MDR y herramientas de ciberseguridad",
        "aliases": ["cartagena", "se2026/44"],
        "placsp": "https://contrataciondelestado.es/wps/poc?uri=deeplink:detalle_licitacion&idEvl=CeV3JsRvMYNeKgd8LfVV9g%3D%3D",
        "pcap": "https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=3RvTg%2BqJGplpqK%2BNayOJdmu3brxMJj85yHdub21Tk8IRUVsFr1wAigfAsquMfDh9lBaZNGbs4SxQbAtLZnFB2c83c%2Bb8gBCF4jisIX8LfHOHAj0WEJrB5sP7amrh2jBD",
        "ppt": "https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=4LNw9X8Oth%2BSn9NbTkZ4FS6sIE23mzU7WXFZ56WAvbF1G%2BlP4OQLs1MxqFW16iI7xeK%2BjNty6lM6gGPDyy6wJX7drdkgQxKh8ayOdg%2BOlwGHAj0WEJrB5sP7amrh2jBD",
        "ted": "649174-2026",
    },
    {
        "key": "enisa",
        "tender_id": "56/2026",
        "buyer": "Empresa Nacional de Innovación, S.M.E., S.A. (ENISA)",
        "title": "Servicios de ciberseguridad y SOC",
        "aliases": ["enisa", "empresa nacional de innovación", "empresa nacional de innovacion", "56/2026"],
        "placsp": "https://contrataciondelestado.es/wps/poc?uri=deeplink:detalle_licitacion&idEvl=xUNZ%2BpKYdSrVGIpKDxgsAQ%3D%3D",
        "pcap": "https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=9ETPlYBON0QDBMg/Qhi65LuaWFeo/yh0sxRjsJQIi9I23eR5bxfQbFmYrhtwrA6xiOf5PEsipiU7Qc1eWPlT2bG9QfRLddT5kTx4EkNbrTqCx2e6p7hqtlp2aFupgHMr",
        "ppt": "https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=47dHKqAqtfJ1wQ0TG75owUHSgz94ch%2BQdgK4Ni1EKa/Fn5t09e5eP/7%2BHUMzKwCqXx5FiJeMlcwnb6%2BXDhu8vvAFA9Kll/3leo9p7zi5FHht/o8fNevwsujgRzaBbugn",
        "ted": "530695-2026",
    },
    {
        "key": "giss",
        "tender_id": "2026/7028",
        "buyer": "Gerencia de Informática de la Seguridad Social (GISS)",
        "title": "Servicios de seguridad de los sistemas de información",
        "aliases": ["giss", "seguridad social", "gerencia de informática", "gerencia de informatica", "2026/7028"],
        "placsp": "https://contrataciondelestado.es/wps/poc?uri=deeplink:detalle_licitacion&idEvl=Q1an2EUNSnL%2B3JAijKO%2Bkg%3D%3D",
        "pcap": "https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=utdJKrcIIi8TnaqXvWAbH6rIIccFdesQyEoNK3OwOZWh6ayu5tQXrTM7Ellxz2qtMvT/tGixw9fore9Gnhnf402jEM6FdBnnUZRaT5ybWWjfdyQgZAdTm3EfcUAC7CJ6",
        "ppt": "https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=4Olo7kYgFvEES5uZIJmlCdK2/Qrpoei5GZTfHej2T75bfV%2BsuxKUo7kvgBuuBPt6bwuwEw2f9qdtYb4ExfoogqlYTMRd9VRC8R9/oCOZn6Q//q7NB2iMZvNyf0xrJmjt",
        "ted": "809807-2026",
    },
]

DOC_TYPES = {
    "pcap": "Pliego de Cláusulas Administrativas Particulares (PCAP)",
    "ppt": "Pliego de Prescripciones Técnicas (PPT)",
    "ted": "Anuncio de licitación en TED (DOUE)",
}

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
TED_API = "https://api.ted.europa.eu/v3/notices/search"


def log(*args) -> None:
    """Todo el registro va a stderr: server.py importa este módulo y su stdout es MCP."""
    print(*args, file=sys.stderr, flush=True)


def source_docs() -> list[dict]:
    """Lista plana de documentos del corpus con sus metadatos."""
    docs = []
    for t in TENDERS:
        for kind in ("pcap", "ppt", "ted"):
            ext = "json" if kind == "ted" else "pdf"
            docs.append({
                "doc_id": f"{t['key']}_{kind}",
                "doc_type": kind.upper(),
                "title": f"{DOC_TYPES[kind]} — {t['title']} ({t['buyer']}, expte. {t['tender_id']})",
                "tender_key": t["key"],
                "tender_id": t["tender_id"],
                "buyer": t["buyer"],
                "aliases": "|".join(t["aliases"]),
                "url": f"https://ted.europa.eu/es/notice/-/detail/{t['ted']}" if kind == "ted" else t[kind],
                "download": t["ted"] if kind == "ted" else t[kind],
                "licence": TED_LICENCE if kind == "ted" else PLACSP_LICENCE,
                "path": config.CORPUS_DIR / f"{t['key']}_{kind}.{ext}",
                "origin": "sources",
            })
    return docs


# ======================================================================================
# 2. DESCARGA
# ======================================================================================
def http_get(url: str, tries: int = 4) -> bytes:
    import httpx

    last = None
    for attempt in range(tries):
        try:
            r = httpx.get(url, headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=90)
            # EUR-Lex y TED responden 202 a los scripts (control anti-bots): reintentamos.
            if r.status_code == 200 and r.content:
                return r.content
            last = f"HTTP {r.status_code}"
        except httpx.HTTPError as e:
            last = repr(e)
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"No se pudo descargar {url[:90]}...: {last}")


# Campos del anuncio de TED que convertimos en texto. NO pedimos ningún campo de
# personas de contacto (organisation-person-*, *-email, *-touchpoint-*): así el dato
# personal ni siquiera llega a nuestro disco.
TED_SECTIONS = {
    "Datos del anuncio": ["publication-number", "publication-date", "notice-type", "procedure-type",
                          "legal-basis", "buyer-name", "internal-identifier-proc"],
    "Objeto del contrato": ["title-proc", "description-proc", "main-classification-proc",
                            "place-of-performance-city-proc"],
    "Valor estimado": ["estimated-value-proc", "estimated-value-cur-proc", "estimated-value-lot"],
    "Lotes y duración": ["identifier-lot", "title-lot", "description-lot", "contract-duration-period-lot",
                         "renewal-description-lot", "option-description-lot", "framework-agreement-lot"],
    "Criterios de selección": ["selection-criterion-lot", "selection-criterion-name-lot",
                               "selection-criterion-description-lot"],
    "Criterios de adjudicación": ["award-criterion-type-lot", "award-criterion-name-lot",
                                  "award-criterion-description-lot", "award-criterion-number-lot"],
    "Plazos y presentación de ofertas": ["deadline-receipt-tender-date-lot", "deadline-receipt-tender-time-lot",
                                         "electronic-submission-lot", "submission-url-lot", "document-url-lot"],
    "Garantías y condiciones": ["guarantee-required-lot", "guarantee-required-description-lot",
                                "contract-conditions-description-lot", "additional-information-lot", "eu-funds-name"],
}


def fetch_ted_notice(publication_number: str) -> dict:
    """Pide el anuncio a la API de búsqueda de TED (la web bloquea scripts; la API no)."""
    import httpx

    fields = [f for group in TED_SECTIONS.values() for f in group]
    body = {"query": f"publication-number={publication_number}", "fields": fields, "limit": 1}
    for attempt in range(4):
        r = httpx.post(TED_API, json=body, timeout=60)
        if r.status_code == 200 and r.json().get("notices"):
            return r.json()["notices"][0]
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"TED no devolvió el anuncio {publication_number}: HTTP {r.status_code}")


def download_sources(docs: list[dict]) -> None:
    config.CORPUS_DIR.mkdir(exist_ok=True)
    for d in docs:
        if d["path"].exists():
            continue
        log(f"  descargando {d['doc_id']} ...")
        try:
            if d["doc_type"] == "TED":
                notice = fetch_ted_notice(d["download"])
                d["path"].write_text(json.dumps(notice, ensure_ascii=False, indent=1), encoding="utf-8")
            else:
                data = http_get(d["download"])
                if not data.startswith(b"%PDF"):
                    raise RuntimeError("la respuesta no es un PDF")
                d["path"].write_bytes(data)
        except Exception as e:  # noqa: BLE001 - seguimos con el resto; main() decide
            log(f"  ! {d['doc_id']}: {e}")


# ======================================================================================
# 3. EXTRACCIÓN: devuelve una lista de páginas (texto)
# ======================================================================================
def extract_pages(path: Path) -> list[str]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        return [(p.extract_text() or "") for p in PdfReader(str(path)).pages]
    if suffix == ".json":
        return [ted_json_to_text(json.loads(path.read_text(encoding="utf-8")))]
    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        return [soup.get_text("\n")]
    if suffix in (".txt", ".md"):
        return [path.read_text(encoding="utf-8", errors="ignore")]
    raise ValueError(f"Formato no soportado: {suffix}. Usa PDF, TXT, MD, HTML o JSON de TED.")


def _ted_value(value) -> str:
    """Los campos de TED vienen como texto, listas o {idioma: valor}: lo aplanamos."""
    if isinstance(value, dict):
        if {"value", "unit"} <= value.keys():
            return f"{value['value']} {value['unit']}"
        for lang in ("spa", "eng"):
            if lang in value:
                return _ted_value(value[lang])
        return _ted_value(next(iter(value.values()), ""))
    if isinstance(value, list):
        return "; ".join(_ted_value(v) for v in value if v not in (None, ""))
    return str(value)


# Etiquetas en español: las preguntas serán en español, y así BM25 y los embeddings
# encuentran "plazo de presentación" aunque el campo se llame deadline-receipt-tender.
TED_LABELS = {
    "publication-number": "Número de publicación en el DOUE/TED",
    "publication-date": "Fecha de publicación en TED",
    "notice-type": "Tipo de anuncio",
    "procedure-type": "Tipo de procedimiento",
    "legal-basis": "Base jurídica (CELEX)",
    "buyer-name": "Poder adjudicador",
    "internal-identifier-proc": "Número de expediente",
    "title-proc": "Título del procedimiento",
    "description-proc": "Descripción del procedimiento",
    "main-classification-proc": "Código CPV principal",
    "place-of-performance-city-proc": "Lugar de ejecución",
    "estimated-value-proc": "Valor estimado total (sin IVA)",
    "estimated-value-cur-proc": "Moneda",
    "estimated-value-lot": "Valor estimado por lote",
    "identifier-lot": "Lotes",
    "title-lot": "Título de cada lote",
    "description-lot": "Descripción de cada lote",
    "contract-duration-period-lot": "Duración del contrato por lote",
    "renewal-description-lot": "Prórrogas",
    "option-description-lot": "Opciones",
    "framework-agreement-lot": "Acuerdo marco",
    "selection-criterion-lot": "Códigos de criterios de selección",
    "selection-criterion-name-lot": "Criterios de selección",
    "selection-criterion-description-lot": "Criterios de selección (solvencia)",
    "deadline-receipt-tender-date-lot": "Fecha límite de presentación de ofertas",
    "deadline-receipt-tender-time-lot": "Hora límite de presentación de ofertas",
    "electronic-submission-lot": "Presentación electrónica",
    "submission-url-lot": "Dirección de presentación de ofertas",
    "document-url-lot": "Dirección de los pliegos",
    "guarantee-required-lot": "Garantía exigida",
    "guarantee-required-description-lot": "Descripción de la garantía",
    "contract-conditions-description-lot": "Condiciones de ejecución",
    "additional-information-lot": "Información adicional",
    "eu-funds-name": "Fondos de la UE",
}
TED_VALUES = {"open": "abierto", "cn-standard": "anuncio de licitación", "price": "precio",
              "quality": "calidad", "cost": "coste", "required": "obligatoria", "none": "no",
              "DAY": "días", "MONTH": "meses", "YEAR": "años"}


def _es(value: str) -> str:
    for en, es in TED_VALUES.items():
        value = re.sub(rf"\b{en}\b", es, value)
    return value


def ted_json_to_text(notice: dict) -> str:
    """Un anuncio de TED es una sola 'página'; cada grupo de campos es un apartado."""
    parts = []
    for section, fields in TED_SECTIONS.items():
        lines = []
        if section == "Criterios de adjudicación":
            # Si TED da tipo, descripción y peso con la misma longitud, los emparejamos.
            types_ = notice.get("award-criterion-type-lot") or []
            desc = notice.get("award-criterion-description-lot") or []
            if isinstance(desc, dict):
                desc = desc.get("spa") or desc.get("eng") or []
            weights = notice.get("award-criterion-number-lot") or []
            if types_ and len(types_) == len(desc) == len(weights):
                for i, (t, d, w) in enumerate(zip(types_, desc, weights), 1):
                    lines.append(f"Criterio {i} ({_es(t)}, ponderación {w} puntos): {d}")
            else:
                lines += [f"Tipos de criterio: {_es(_ted_value(types_))}",
                          f"Descripción de los criterios: {_ted_value(desc)}",
                          f"Ponderaciones (puntos): {_ted_value(weights)}"]
        else:
            for f in fields:
                if notice.get(f) not in (None, "", [], {}):
                    lines.append(f"{TED_LABELS.get(f, f)}: {_es(_ted_value(notice[f]))}")
        if lines:
            parts.append(f"{section.upper()}\n" + "\n".join(lines))
    return "\n\n".join(parts)


# ======================================================================================
# 4. LIMPIEZA
# ======================================================================================
TOC_LINE = re.compile(r"\.{5,}|…{3,}")                       # "Objeto ........... 6"
PAGE_NUMBER = re.compile(r"^(p[áa]g(ina)?\.?\s*)?\d{1,3}(\s*(de|/)\s*\d{1,3})?$", re.I)
# Versalitas mal extraídas: "D ESCRIPCIÓN" -> "DESCRIPCIÓN", "J efe" -> "Jefe". Solo consonantes
# sueltas (A, E, I, O, U, Y son palabras en español y no se tocan).
SMALL_CAPS = re.compile(r"\b([B-DF-HJ-NP-TV-XZ]) ([A-ZÁÉÍÓÚÑ]{2,}|[a-záéíóúñ]{2,})")
HYPHEN_BREAK = re.compile(r"([a-záéíóúñü])-\n\s*([a-záéíóúñü])")    # "sis-\ntemas" -> "sistemas"


def _line_key(line: str) -> str:
    """Normaliza una línea para detectar cabeceras/pies repetidos (los números cambian)."""
    return re.sub(r"\d+", "#", re.sub(r"\s+", " ", line.strip().lower()))


def clean_pages(pages: list[str]) -> list[str]:
    # Líneas que se repiten en muchas páginas = cabeceras y pies (nº de expediente,
    # "Código Seguro de Verificación", bloque de firma...). Las quitamos todas.
    n = len(pages)
    counts = Counter()
    for p in pages:
        counts.update({_line_key(l) for l in p.splitlines() if l.strip()})
    threshold = max(3, int(0.4 * n))
    boiler = {k for k, c in counts.items() if n >= 4 and c >= threshold}

    cleaned = []
    for p in pages:
        p = HYPHEN_BREAK.sub(r"\1\2", p)
        out = []
        for line in p.splitlines():
            s = re.sub(r"[ \t]+", " ", line).strip()
            if not s or _line_key(s) in boiler or TOC_LINE.search(s) or PAGE_NUMBER.match(s):
                continue
            out.append(SMALL_CAPS.sub(r"\1\2", s))
        cleaned.append("\n".join(out))
    return cleaned


# ======================================================================================
# 5. DATOS PERSONALES
# ======================================================================================
_NAME_WORD = r"(?:[A-ZÁÉÍÓÚÑ][a-záéíóúñü]+|[A-ZÁÉÍÓÚÑ]{2,})"
REDACTIONS = [
    # (tipo, patrón, reemplazo)
    ("firma", re.compile(r"(?im)^\s*(firmado|firmada)\s+(electr[óo]nicamente\s+)?por\b.*$"), "[FIRMA]"),
    ("firma", re.compile(r"(?m)^\s*Fdo\.?:?\s+.*$"), "[FIRMA]"),
    ("nombre", re.compile(rf"\b(D\.ª|Dª|Dña\.?|D\.|Don|Doña|Sr\.|Sra\.)\s+{_NAME_WORD}(?:\s+(?:de\s+(?:la\s+|los\s+)?)?{_NAME_WORD}){{1,4}}"), r"\1 [NOMBRE]"),
    ("email", re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+"), "[EMAIL]"),
    ("telefono", re.compile(r"(?<![\w.,/-])(?:\+34 ?)?[6789](?: ?\d){8}(?![\w,/-])"), "[TELÉFONO]"),
    ("dni", re.compile(r"\b(\d{8} ?-?[A-HJ-NP-TV-Z]|[XYZ]\d{7}[A-Z])\b"), "[DNI]"),
]
# Bloque "FIRMADO POR" + nombre en la línea siguiente (formato de la sede de Cartagena)
SIGNED_BY_BLOCK = re.compile(rf"(?im)^\s*firmado por\s*\n\s*{_NAME_WORD}(?:\s+{_NAME_WORD}){{1,4}}\s*$")


def redact(text: str) -> tuple[str, Counter]:
    """Sustituye datos personales por etiquetas. Devuelve el texto y cuántos de cada tipo."""
    found = Counter()
    text, n = SIGNED_BY_BLOCK.subn("[FIRMA]", text)
    found["firma"] += n
    for kind, pattern, repl in REDACTIONS:
        text, n = pattern.subn(repl, text)
        found[kind] += n
    return text, found


# ======================================================================================
# 6. CHUNKING
# ======================================================================================
ORDINAL = (r"(PRIMER[AO]|SEGUND[AO]|TERCER[AO]|CUART[AO]|QUINT[AO]|SEXT[AO]|S[EÉ]PTIM[AO]|OCTAV[AO]|"
           r"NOVEN[AO]|D[EÉ]CIM[AO]|UND[EÉ]CIM[AO]|DUOD[EÉ]CIM[AO]|D[EÉ]CIMO\w*|VIG[EÉ]SIM[AO]\w*|TRIG[EÉ]SIM[AO]\w*)")
# Títulos "fuertes": casi seguro que abren una cláusula.
STRONG_HEADINGS = [
    re.compile(r"^(CL[AÁ]USULA|ANEXO|AP[EÉ]NDICE|T[IÍ]TULO|CAP[IÍ]TULO|DOCUMENTO)\s+[\dIVXL]+\b", re.I),
    re.compile(rf"^{ORDINAL}(\s+{ORDINAL})?\s*\.?\s*[-–]"),                 # "TERCERA.- ..."
    re.compile(r"^[IVXL]{1,5}\s*[.\-–]+\s*[A-ZÁÉÍÓÚÑ]"),                     # "I.- DATOS GENERALES"
]
# Títulos numerados: también pueden ser párrafos numerados ("2.5. El desconocimiento...").
NUMBERED_HEADING = re.compile(r"^\d{1,2}(\.\d{1,2}){0,4}\.?\s*[-–.)]?\s*[A-ZÁÉÍÓÚÑ¿(]")  # "4.1. PRESUPUESTO"


def is_heading(line: str, next_line: str = "") -> bool:
    """¿Es esta línea el título de una cláusula/apartado?

    Reglas: es corta y (a) empieza como un título fuerte ("QUINTA.-", "ANEXO II"), o
    (b) empieza numerada ("4.1.") y la línea siguiente NO empieza en minúscula (si
    empieza en minúscula era un párrafo numerado que sigue abajo), o (c) es casi
    toda mayúsculas.
    """
    s = line.strip()
    if not s or len(s) > 100 or s.endswith((",", ";")):
        return False
    if any(p.match(s) for p in STRONG_HEADINGS):
        return True
    continues = bool(next_line) and next_line.strip()[:1].islower()
    if NUMBERED_HEADING.match(s):
        return not continues
    letters = [c for c in s if c.isalpha()]
    upper = sum(c.isupper() for c in letters) / max(len(letters), 1)
    return len(letters) >= 8 and len(s.split()) >= 2 and upper > 0.85 and not continues


def _lines_with_pages(pages: list[str]) -> list[tuple[int, str]]:
    return [(i + 1, l) for i, p in enumerate(pages) for l in p.splitlines() if l.strip()]


def _sections(pages: list[str]) -> list[dict]:
    """Agrupa las líneas en apartados: [{heading, lines:[(page, text)]}]."""
    lines = _lines_with_pages(pages)
    sections = [{"heading": "", "lines": []}]
    for i, (page, text) in enumerate(lines):
        nxt = lines[i + 1][1] if i + 1 < len(lines) else ""
        if is_heading(text, nxt):
            sections.append({"heading": text[:120], "lines": []})
        sections[-1]["lines"].append((page, text))
    return [s for s in sections if s["lines"]]


def chunk_struct(pages: list[str], max_words: int, min_words: int) -> list[dict]:
    """Diseño estructural: un fragmento por apartado del pliego.

    Apartados demasiado cortos se juntan con el siguiente; apartados largos se parten
    en trozos de <= max_words palabras repitiendo el título del apartado delante.
    """
    chunks: list[dict] = []
    pending = None  # apartado corto esperando a unirse con el siguiente
    for sec in _sections(pages):
        words = [(p, w) for p, line in sec["lines"] for w in line.split()]
        if pending:
            words = pending["words"] + words
            heading = pending["heading"] or sec["heading"]
            pending = None
        else:
            heading = sec["heading"]
        if len(words) < min_words:
            pending = {"heading": heading, "words": words}
            continue
        n_parts = -(-len(words) // max_words)        # división redondeando hacia arriba
        size = -(-len(words) // n_parts)             # trozos de tamaño parecido
        for i in range(0, len(words), size):
            part = words[i:i + size]
            prefix = f"[{heading}] (continuación)\n" if i and heading else ""
            chunks.append({"section": heading, "page_start": part[0][0], "page_end": part[-1][0],
                           "text": prefix + " ".join(w for _, w in part)})
    if pending:
        if chunks and len(pending["words"]) < min_words:
            chunks[-1]["text"] += " " + " ".join(w for _, w in pending["words"])
            chunks[-1]["page_end"] = pending["words"][-1][0]
        else:
            w = pending["words"]
            chunks.append({"section": pending["heading"], "page_start": w[0][0], "page_end": w[-1][0],
                           "text": " ".join(x for _, x in w)})
    return chunks


def chunk_fixed(pages: list[str], words: int, overlap: int) -> list[dict]:
    """Diseño de referencia: ventanas de N palabras con solape, sin mirar la estructura."""
    stream, heading_at = [], []
    current = ""
    for sec in _sections(pages):
        current = sec["heading"] or current
        for page, line in sec["lines"]:
            for w in line.split():
                stream.append((page, w))
                heading_at.append(current)
    chunks, step = [], max(words - overlap, 1)
    for i in range(0, max(len(stream) - overlap, 1), step):
        part = stream[i:i + words]
        if not part:
            break
        chunks.append({"section": heading_at[i], "page_start": part[0][0], "page_end": part[-1][0],
                       "text": " ".join(w for _, w in part)})
    return chunks


def chunk_pages(pages: list[str], design: str) -> list[dict]:
    d = config.CHUNK_DESIGNS[design]
    if d["kind"] == "struct":
        return chunk_struct(pages, d["max_words"], d["min_words"])
    return chunk_fixed(pages, d["words"], d["overlap"])


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare_pages(path: Path) -> tuple[list[str], Counter]:
    """Extraer + anonimizar + limpiar. Devuelve las páginas limpias y el recuento de datos tachados.

    Anonimizamos ANTES de limpiar para que el recuento incluya las firmas que se repiten en
    el pie de cada página (la limpieza luego quita esas líneas repetidas).
    """
    total = Counter()
    redacted = []
    for p in extract_pages(path):
        p, found = redact(p)
        total.update(found)
        redacted.append(p)
    # Segunda pasada: la limpieza une palabras partidas a final de línea
    # ("dpd@ayto-\ncartagena.es") y pueden aparecer datos que antes no casaban.
    out = []
    for p in clean_pages(redacted):
        p, found = redact(p)
        total.update(found)
        out.append(p)
    return out, total


def chunk_file(path: str | Path, meta: dict | None = None, design: str | None = None) -> list[dict]:
    """Pipeline completo para UN fichero -> lista de fragmentos con metadatos.

    `meta` trae los metadatos del documento (doc_id, título, licitación...). Si no se
    pasa (caso de add_document), se deducen del nombre del fichero.
    """
    path = Path(path)
    pages, redacted = prepare_pages(path)
    chunk_file.last_redactions = redacted  # para el registro de anonimización
    return make_chunks(pages, dict(meta or default_meta(path)), design or config.CHOSEN_DESIGN, file_sha256(path))


def make_chunks(pages: list[str], meta: dict, design: str, sha: str) -> list[dict]:
    """Páginas ya limpias -> fragmentos con id estable y todos los metadatos.

    El id depende del texto: mismo texto => mismo id => no se vuelve a pagar su embedding.
    """
    out, seen = [], Counter()
    for c in chunk_pages(pages, design):
        if len(c["text"].split()) < 5:
            continue
        digest = hashlib.sha1(f"{meta['doc_id']}|{c['text']}".encode()).hexdigest()[:12]
        seen[digest] += 1
        cid = f"{design}:{meta['doc_id']}:{digest}" + (f"-{seen[digest]}" if seen[digest] > 1 else "")
        out.append({
            "id": cid,
            "text": c["text"],
            "doc_id": meta["doc_id"],
            "doc_type": meta.get("doc_type", ""),
            "title": meta["title"],
            "tender_key": meta.get("tender_key", ""),
            "tender_id": meta.get("tender_id", ""),
            "buyer": meta.get("buyer", ""),
            "aliases": meta.get("aliases", ""),
            "url": meta.get("url", ""),
            "section": c["section"],
            "page_start": c["page_start"],
            "page_end": c["page_end"],
            "words": len(c["text"].split()),
            "design": design,
            "file_sha256": sha,
            "origin": meta.get("origin", "add_document"),
        })
    return out


chunk_file.last_redactions = Counter()


def default_meta(path: Path) -> dict:
    """Metadatos para un fichero suelto (add_document): doc_id = nombre del fichero."""
    stem = re.sub(r"[^a-z0-9_]+", "_", unicodedata.normalize("NFKD", path.stem.lower()).encode("ascii", "ignore").decode()).strip("_")
    return {"doc_id": stem or "documento", "doc_type": path.suffix.lstrip(".").upper(),
            "title": path.name, "url": path.name, "origin": "add_document"}


# ======================================================================================
# 7. EMBEDDINGS Y ALMACENAMIENTO (ChromaDB)
# ======================================================================================
class DailyQuotaExceeded(RuntimeError):
    """La cuota diaria gratuita de Gemini se ha agotado (se reinicia a las 09:00 en España)."""


_genai_client = None


def genai_client():
    global _genai_client
    if _genai_client is None:
        from google import genai

        from api_key import load_api_key

        from google.genai import types

        # Timeout de 2 minutos por petición: si Gemini se queda colgado, mejor un error
        # (que se reintenta) que un programa parado sin decir nada.
        _genai_client = genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(timeout=120_000))
    return _genai_client


def document_text_for_embedding(chunk: dict) -> str:
    # gemini-embedding-2 no tiene task_type: el tipo de tarea va como prefijo en el texto.
    title = f"{chunk['title']} | apartado: {chunk['section']}" if chunk.get("section") else chunk["title"]
    return f"title: {title} | text: {chunk['text']}"


def query_text_for_embedding(query: str) -> str:
    return f"task: search result | query: {query}"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Un único lote de textos -> un vector por texto. Reintenta si Gemini dice 429."""
    from google.genai import errors, types

    # Ojo: si se pasan strings sueltos, gemini-embedding-2 devuelve UN vector para todo
    # el lote. Envolviendo cada texto en su propio Content se obtiene uno por texto.
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            resp = genai_client().models.embed_content(
                model=config.EMBED_MODEL,
                contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=config.EMBED_DIM),
            )
            vectors = [list(e.values) for e in resp.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Gemini devolvió {len(vectors)} vectores para {len(texts)} textos")
            return vectors
        except errors.ClientError as e:
            if e.code != 429:
                raise
            if "perday" in str(e).lower().replace(" ", "").replace("_", ""):
                raise DailyQuotaExceeded(str(e)[:300]) from e
            wait = min(60, 10 * (attempt + 1))
            log(f"    límite por minuto de Gemini; espero {wait}s ...")
            time.sleep(wait)
    raise DailyQuotaExceeded("Gemini sigue devolviendo 429 tras varios reintentos")


def get_collection(design: str):
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(
        name=design, configuration={"hnsw": {"space": "cosine"}}, embedding_function=None
    )


METADATA_KEYS = ["doc_id", "doc_type", "title", "tender_key", "tender_id", "buyer", "aliases", "url",
                 "section", "page_start", "page_end", "words", "design", "file_sha256", "origin"]


def embed_and_store(chunks: list[dict], design: str | None = None) -> dict:
    """Embebe SOLO los fragmentos cuyo id no está ya en ChromaDB y los guarda lote a lote.

    Así, si se corta (error, cuota diaria), lo ya pagado queda guardado.
    Devuelve {'new': n embebidos ahora, 'existing': n que ya estaban, 'pending': n sin hacer}.
    """
    design = design or (chunks[0]["design"] if chunks else config.CHOSEN_DESIGN)
    col = get_collection(design)
    ids = [c["id"] for c in chunks]
    existing = set()
    for i in range(0, len(ids), 500):
        existing.update(col.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    done = 0
    try:
        for i in range(0, len(todo), config.EMBED_BATCH):
            batch = todo[i:i + config.EMBED_BATCH]
            vectors = embed_texts([document_text_for_embedding(c) for c in batch])
            col.upsert(
                ids=[c["id"] for c in batch],
                embeddings=vectors,
                documents=[c["text"] for c in batch],
                metadatas=[{k: c[k] for k in METADATA_KEYS} for c in batch],
            )
            done += len(batch)
            log(f"    {design}: {len(existing) + done}/{len(chunks)} fragmentos con vector")
    except DailyQuotaExceeded as e:
        log(f"  ! Cuota diaria de embeddings agotada ({e.__class__.__name__}). Lo hecho está guardado; "
            f"vuelve a ejecutar `main.py index` mañana (se reinicia a las 09:00 en España).")
        return {"new": done, "existing": len(existing), "pending": len(todo) - done, "quota": True}
    return {"new": done, "existing": len(existing), "pending": 0, "quota": False}


def delete_doc_chunks(design: str, doc_id: str, keep_ids: set[str] | None = None) -> int:
    """Borra los fragmentos de un documento (menos keep_ids). Sirve para versiones nuevas."""
    col = get_collection(design)
    old = col.get(where={"doc_id": doc_id}, include=[])["ids"]
    stale = [i for i in old if not keep_ids or i not in keep_ids]
    if stale:
        col.delete(ids=stale)
    return len(stale)


# ======================================================================================
# 8. PROGRAMA PRINCIPAL
# ======================================================================================
def export_chunks_csv(design: str) -> int:
    """index/chunks_<diseño>.csv: para leer los fragmentos y escribir tus preguntas."""
    col = get_collection(design)
    data = col.get(include=["documents", "metadatas"])
    rows = sorted(zip(data["ids"], data["documents"], data["metadatas"]),
                  key=lambda r: (r[2]["doc_id"], r[2]["page_start"], r[0]))
    with (config.INDEX_DIR / f"chunks_{design}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "doc_id", "page_start", "page_end", "section", "words", "text"])
        for cid, doc, m in rows:
            w.writerow([cid, m["doc_id"], m["page_start"], m["page_end"], m["section"], m["words"], doc])
    return len(rows)


def main() -> None:
    config.INDEX_DIR.mkdir(exist_ok=True)
    docs = source_docs()
    log("1/3 Descargando el corpus en corpus/ ...")
    download_sources(docs)

    log("2/3 Extrayendo, limpiando, anonimizando y troceando ...")
    stats, chunks_by_design = [], {d: [] for d in config.CHUNK_DESIGNS}
    for d in docs:
        if not d["path"].exists():
            have = get_collection(config.CHOSEN_DESIGN).get(where={"doc_id": d["doc_id"]}, limit=1, include=[])["ids"]
            if have:
                log(f"  ! {d['doc_id']} no se pudo descargar, pero ya está en el índice: lo conservo.")
                continue
            raise SystemExit(f"No tengo {d['doc_id']} ni en corpus/ ni en el índice. Revisa la conexión y repite.")
        pages, redacted = prepare_pages(d["path"])
        sha = file_sha256(d["path"])
        for design in config.CHUNK_DESIGNS:
            chunks_by_design[design] += make_chunks(pages, d, design, sha)
        stats.append({
            "doc_id": d["doc_id"], "title": d["title"], "url": d["url"], "licence": d["licence"],
            "pages": len(pages), "words": sum(len(p.split()) for p in pages),
            **{f"redacted_{k}": v for k, v in redacted.items()},
        })

    log("3/3 Embeddings (solo los fragmentos nuevos) y guardado en index/chroma ...")
    pending = 0
    for design, chunks in chunks_by_design.items():
        # Borra fragmentos viejos de estos documentos (p. ej. si cambió un pliego).
        by_doc: dict[str, set] = {}
        for c in chunks:
            by_doc.setdefault(c["doc_id"], set()).add(c["id"])
        for doc_id, keep in by_doc.items():
            removed = delete_doc_chunks(design, doc_id, keep)
            if removed:
                log(f"  {design}: borrados {removed} fragmentos obsoletos de {doc_id}")
        result = embed_and_store(chunks, design)
        pending += result["pending"]
        log(f"  {design}: {len(chunks)} fragmentos; {result['new']} embebidos ahora, "
            f"{result['existing']} ya estaban, {result['pending']} pendientes")
        export_chunks_csv(design)
        if result["quota"]:
            break

    # Estadísticas del corpus -> te sirven para la tabla del REPORT.
    keys = sorted({k for s in stats for k in s})
    order = ["doc_id", "title", "url", "licence", "pages", "words"] + [k for k in keys if k.startswith("redacted_")]
    with (config.INDEX_DIR / "corpus_stats.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=order, restval=0)
        w.writeheader()
        w.writerows(stats)
    total_words = sum(s["words"] for s in stats)
    log(f"\nCorpus: {len(stats)} documentos, {total_words:,} palabras (tras limpiar). "
        f"Detalle en index/corpus_stats.csv")
    for design, chunks in chunks_by_design.items():
        log(f"  {design}: {len(chunks)} fragmentos, media {sum(c['words'] for c in chunks) / max(len(chunks), 1):.0f} palabras")
    if pending:
        log(f"\nQuedan {pending} fragmentos sin vector. Repite `main.py index` cuando se renueve la cuota.")
    else:
        log("\nÍndice completo.")


if __name__ == "__main__":
    main()
