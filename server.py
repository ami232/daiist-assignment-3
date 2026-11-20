"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ (Chroma) on first use and never re-embeds the corpus: only the
query is embedded, and that vector is cached. Prints nothing to stdout (it
carries the protocol); logs go to stderr. Docstrings become the tool
descriptions the model reads.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
import rag

logging.basicConfig(level=logging.WARNING, stream=sys.stderr, format="%(name)s: %(message)s")
log = logging.getLogger("server")

ALLOWED_DIR = ix.ROOT          # add_document only reads files inside this repository (corpus/ included)

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Busca en la legislación estatal española para autónomos (texto consolidado del BOE).

    El corpus contiene: Estatuto del trabajo autónomo (LETA, Ley 20/2007), Ley General
    de la Seguridad Social títulos IV y V (LGSS: RETA, cotización, incapacidad temporal,
    cese de actividad), Reglamento de facturación (RF, RD 1619/2012) y Reglamento de
    gestión e inspección tributaria, título II (RGAT, RD 1065/2007: alta censal,
    domicilio fiscal, NIF, libros registro), más los documentos añadidos con add_document.

    Úsala antes de responder cualquier pregunta sobre derechos u obligaciones de un
    autónomo; puedes llamarla varias veces con otras palabras. Escribe la consulta en
    español y con términos de la norma (p. ej. "reducción de cuotas inicio de actividad").

    Devuelve los 5 fragmentos más relevantes. Cada uno lleva su cita lista para copiar
    con el formato [FUENTE, Ubicación] (p. ej. [LETA, Artículo 38 ter]), el título de la
    norma, la fecha de consolidación del texto, el texto y el enlace al BOE. Termina con
    el aviso de que el texto consolidado es informativo.
    """
    query = (query or "").strip()
    if not query:
        return "Error: la consulta está vacía. Escribe qué quieres buscar."
    try:
        return rag.format_hits(rag.retrieve(query))
    except ix.QuotaExhausted:
        return "Error: se ha agotado la cuota de la API de embeddings de Gemini. Inténtalo más tarde."
    except Exception as error:  # noqa: BLE001 - an MCP tool reports errors, it doesn't raise them
        log.exception("search failed")
        return f"Error al buscar: {type(error).__name__}: {error}"


def _resolve(path: str) -> Path:
    """The file to add, as an absolute path inside the repository; ValueError otherwise."""
    candidate = Path(path.strip().strip('"'))
    candidate = (candidate if candidate.is_absolute() else ALLOWED_DIR / candidate).resolve()
    if not candidate.is_relative_to(ALLOWED_DIR):
        raise ValueError(f"solo se pueden añadir ficheros dentro de {ALLOWED_DIR.name}/ (p. ej. corpus/…)")
    if not candidate.is_file():
        raise ValueError(f"no existe el fichero {candidate.relative_to(ALLOWED_DIR)}")
    if candidate.suffix.lower() != ".xml" or candidate.name.endswith(".meta.xml"):
        raise ValueError("solo se admite el XML de texto consolidado del BOE (corpus/<BOE-id>.xml)")
    return candidate


@mcp.tool()
def add_document(path: str) -> str:
    """Añade al índice una norma en XML de texto consolidado del BOE y la deja disponible para search.

    `path` es la ruta del fichero dentro del repositorio, p. ej.
    "corpus/BOE-A-2026-7296.xml" (descargado de la API de datos abiertos del BOE; si
    hay un .meta.xml al lado, de él se toman el título y la fecha de consolidación).
    El fichero pasa por el mismo proceso que el resto del corpus (limpieza, troceado
    por artículos, embeddings) y solo se generan embeddings para los fragmentos nuevos.

    Si la norma ya está indexada con la misma fecha de consolidación no hace nada; si
    el fichero es una versión más reciente, sustituye la anterior; si es más antigua,
    no cambia nada. Modifica el índice: úsala solo cuando el usuario lo pida.

    Devuelve un resumen en una línea (norma, fragmentos añadidos y omitidos) o un
    mensaje que empieza por "Error:".
    """
    try:
        file = _resolve(path or "")
        result = ix.index_file(file)
    except ValueError as error:
        return f"Error: {error}"
    except ix.QuotaExhausted:
        return "Error: se ha agotado la cuota de la API de embeddings de Gemini. Inténtalo más tarde."
    except Exception as error:  # noqa: BLE001 - unparseable XML and the like
        log.exception("add_document failed")
        return f"Error: no se ha podido indexar {path}: {type(error).__name__}: {error}"

    name = f"{result['source']} ({result['boe_id']}, consolidado a {rag.spanish_date(result['updated'])})"
    if result["status"] == "already":
        return f"{name} ya estaba indexado con esta versión: no se ha añadido nada ({result['chunks']} fragmentos)."
    if result["status"] == "older":
        return (f"{name} no se ha añadido: el índice ya tiene una versión más reciente "
                f"(consolidada a {rag.spanish_date(result['stored_updated'])}).")
    verb = "Sustituido por la versión nueva" if result["status"] == "replaced" else "Añadido"
    line = f"{verb}: {name}. {result['added']} fragmentos nuevos, {result['skipped']} omitidos (ya estaban)."
    if result["pending"]:
        line += f" Quedan {result['pending']} sin indexar por la cuota de embeddings: vuelve a llamar más tarde."
    return line


if __name__ == "__main__":
    mcp.run()  # stdio
