"""
Assignment 3: servidor MCP. Tu editor y agent.py lo arrancan; a mano: `uv run server.py`.

Dos herramientas:
  - search(query, licitacion?)  -> fragmentos con su cita [doc_id, p. N]
  - add_document(path)          -> pasa un fichero por el pipeline de index.py y lo guarda

Reglas del enunciado que cumple:
  - Carga index/ al arrancar y NUNCA re-embebe el corpus (solo embebe la pregunta).
  - No escribe nada en stdout (por ahí va el protocolo MCP); todo el log va a stderr.
  - Las descripciones de las herramientas (lo que lee el modelo) están en *_DESCRIPTION.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import config
from index import METADATA_KEYS, chunk_file, delete_doc_chunks, embed_and_store, file_sha256, get_collection
from retrieval import Retriever, format_hits

ALLOWED_SUFFIXES = {".pdf", ".txt", ".md", ".html", ".htm", ".json"}
MAX_FILE_MB = 25


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


retriever = Retriever(config.CHOSEN_DESIGN)
log(f"[corpus] índice '{config.CHOSEN_DESIGN}' cargado: {len(retriever.ids)} fragmentos, "
    f"búsqueda '{config.CHOSEN_METHOD}'")


def _tender_list() -> str:
    if not retriever.tenders:
        return "(índice vacío: ejecuta `main.py index`)"
    return "; ".join(f"«{k}» = {v['buyer']}, expte. {v['tender_id']}" for k, v in sorted(retriever.tenders.items()))


SEARCH_DESCRIPTION = f"""Busca en un corpus de pliegos REALES de licitaciones públicas españolas de
ciberseguridad (servicios SOC/MDR), descargados de la Plataforma de Contratación del Sector
Público (PCAP = cláusulas administrativas: plazos, solvencia, garantías, criterios de
adjudicación, penalidades...; PPT = prescripciones técnicas: servicios, perfiles, SLAs,
herramientas) y de sus anuncios en TED (DOUE).

Licitaciones disponibles: {_tender_list()}.

Úsala SIEMPRE antes de responder cualquier pregunta sobre estas licitaciones; puedes
llamarla varias veces con consultas distintas (p. ej. una por licitación al comparar).
Argumentos:
  - query: la consulta en español, con las palabras que esperas encontrar en el pliego.
  - licitacion (opcional): clave de la licitación para buscar SOLO en ella
    (p. ej. "cartagena"). Si la omites y la consulta nombra una, se filtra sola.
Devuelve hasta {config.TOP_K} fragmentos; cada uno trae la cita exacta que debes usar,
con el formato [doc_id, p. N], el documento, el apartado y las páginas."""

ADD_DESCRIPTION = f"""Añade un documento nuevo al índice del corpus: lo extrae, lo limpia, borra los
datos personales, lo trocea, calcula sus embeddings con Gemini y lo guarda, de modo que
search ya lo encuentre. Úsala solo cuando el usuario pida explícitamente añadir un
fichero. Argumento: path, ruta a un fichero {", ".join(sorted(ALLOWED_SUFFIXES))} dentro de
la carpeta del proyecto. Si el mismo contenido ya está indexado no hace nada (no gasta
cuota); si es una versión nueva de un documento con el mismo nombre, sustituye la
anterior. Devuelve el doc_id que debes usar en las citas y cuántos fragmentos se añadieron."""

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool(description=SEARCH_DESCRIPTION)
def search(query: str, licitacion: str = "") -> str:
    hits, tender = retriever.search(query, tender=licitacion or None)
    return format_hits(query, hits, tender)


@mcp.tool(description=ADD_DESCRIPTION)
def add_document(path: str) -> str:
    # 1. Validar la ruta (guardarraíl en el servidor: solo ficheros del proyecto, tipos conocidos)
    p = Path(path).expanduser()
    p = (config.ROOT / p).resolve() if not p.is_absolute() else p.resolve()
    if not p.is_file():
        return f"ERROR: no existe el fichero {p}."
    if not p.is_relative_to(config.ROOT):
        return f"ERROR: por seguridad solo se aceptan ficheros dentro de {config.ROOT}. Copia el fichero ahí."
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"ERROR: formato {p.suffix} no soportado. Usa {', '.join(sorted(ALLOWED_SUFFIXES))}."
    if p.stat().st_size > MAX_FILE_MB * 1e6:
        return f"ERROR: el fichero pesa más de {MAX_FILE_MB} MB."

    # 2. ¿Ya está indexado? Comparamos el hash del contenido, no el nombre.
    col = get_collection(config.CHOSEN_DESIGN)
    sha = file_sha256(p)
    same = col.get(where={"file_sha256": sha}, limit=1, include=["metadatas"])
    if same["ids"]:
        doc_id = same["metadatas"][0]["doc_id"]
        return f"YA INDEXADO: este contenido ya está en el índice como «{doc_id}». No se ha hecho nada."

    # 3. Pipeline de index.py (importado, no reescrito)
    chunks = chunk_file(p, design=config.CHOSEN_DESIGN)
    if not chunks:
        return "ERROR: no se pudo extraer texto del fichero (¿es un PDF escaneado sin texto?)."
    doc_id = chunks[0]["doc_id"]
    # Primero se guarda lo nuevo y SOLO DESPUÉS se borra la versión anterior: si la API falla
    # (cuota, red), el documento antiguo sigue en el índice en vez de desaparecer.
    result = embed_and_store(chunks, config.CHOSEN_DESIGN)
    new_ids = [c["id"] for c in chunks]
    stored = set(col.get(ids=new_ids, include=[])["ids"])
    if stored:   # los fragmentos que no cambiaron de texto pasan a apuntar al fichero nuevo
        col.update(ids=[c["id"] for c in chunks if c["id"] in stored],
                   metadatas=[{k: c[k] for k in METADATA_KEYS} for c in chunks if c["id"] in stored])
    replaced = 0
    if not result["pending"]:
        replaced = delete_doc_chunks(config.CHOSEN_DESIGN, doc_id, keep_ids=set(new_ids))
    retriever.reload()

    redacted = {k: v for k, v in chunk_file.last_redactions.items() if v}
    msg = [f"AÑADIDO: «{p.name}» como doc_id «{doc_id}»: {result['new']} fragmentos nuevos."]
    if replaced:
        msg.append(f"Sustituye a una versión anterior ({replaced} fragmentos borrados).")
    if result["pending"]:
        msg.append(f"AVISO: {result['pending']} fragmentos sin embedding (cuota diaria agotada); "
                   f"vuelve a llamar mañana para completarlo. Mientras, se conserva la versión anterior.")
    if redacted:
        msg.append(f"Datos personales tachados: {redacted}.")
    msg.append(f"Cítalo como [{doc_id}, p. N].")
    return " ".join(msg)


if __name__ == "__main__":
    mcp.run()  # stdio
