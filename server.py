"""
Assignment 3: MCP server over the Congreso de los Diputados corpus.

Your editor and agent.py start it; by hand: `uv run server.py`.

The corpus is the complete parliamentary trail of Proyecto de Ley Orgánica
121/000001, "de representación paritaria y presencia equilibrada de mujeres y
hombres" (XV Legislatura) — the Government's bill, the Ponencia's report, the
text finally approved, and the plenary debate of 27 June 2024. Its Artículo
primero amends the LOREG, so the law governs candidate lists for the May 2027
elections.

Two tools: search() reads the committed index; add_document() runs a new PDF
through index.py's pipeline. The index is loaded, never rebuilt: the server
embeds queries and newly added documents only.

Nothing may go to stdout — it carries the MCP protocol. All logging is stderr.
"""

from __future__ import annotations

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as pipeline

ROOT = Path(__file__).resolve().parent
ACTIVE_STRATEGY = pipeline.DEFAULT_STRATEGY   # set from the retrieval evaluation
MAX_RESULTS = 10

mcp = MCPServer("corpus", log_level="WARNING")


def log(message: str) -> None:
    """Log to stderr. Anything on stdout corrupts the MCP stream."""
    print(message, file=sys.stderr, flush=True)


def _grupo_variants(grupo: str) -> list[str]:
    """Every stored `grupo` value that counts as this group."""
    stored = set()
    try:
        collection = pipeline._collection(ACTIVE_STRATEGY)
        for metadata in collection.get(include=["metadatas"]).get("metadatas") or []:
            value = metadata.get("grupo") or ""
            if value and grupo.lower() in value.lower():
                stored.add(value)
    except Exception:  # noqa: BLE001 - fall back to an exact match
        pass
    return sorted(stored) or [grupo]


def _citation(metadata: dict) -> str:
    """The exact string the model must copy into its answer."""
    return f"[{metadata.get('location_label', metadata.get('doc_id', '?'))} · CVE:{metadata.get('cve', '?')}]"


def _where(tramite: str, genero: str, doc_id: str, grupo: str = "") -> dict | None:
    clauses: list[dict] = [{"superseded": False}]
    if tramite:
        clauses.append({"tramite": tramite})
    if genero:
        clauses.append({"genero": genero})
    if doc_id:
        clauses.append({"doc_id": doc_id})
    if grupo:
        # Chroma has no substring match, so a jointly signed amendment
        # ("Socialista; Plurinacional SUMAR") is matched with $in over both forms.
        clauses.append({"grupo": {"$in": _grupo_variants(grupo)}})
    return clauses[0] if len(clauses) == 1 else {"$and": clauses}


@mcp.tool()
def search(query: str, tramite: str = "", genero: str = "", grupo: str = "", k: int = 5) -> str:
    """Busca en el expediente parlamentario del Proyecto de Ley Orgánica 121/000001,
    "de representación paritaria y presencia equilibrada de mujeres y hombres"
    (Congreso de los Diputados, XV Legislatura).

    El corpus contiene cuatro documentos oficiales del Congreso:
      - BOCG-15-A-1-1  proyecto           el texto presentado por el Gobierno (15/12/2023)
      - BOCG-15-A-1-4  informe_ponencia   el informe de la Ponencia (25/06/2024)
      - BOCG-15-A-1-8  aprobacion_definitiva  el texto aprobado definitivamente (31/07/2024)
      - DSCD-15-PL-54  debate_pleno       el debate y la votación del Pleno (27/06/2024)

    Úsala para cualquier pregunta sobre qué dice una versión concreta del texto, qué
    cambió entre una fase y otra, o qué dijo un diputado en el debate. El mismo
    artículo existe en varias versiones, así que conviene filtrar por `tramite`
    cuando la pregunta se refiere a una fase concreta.

    NO cubre: el Senado, otras leyes, otros expedientes, parlamentos autonómicos,
    las enmiendas presentadas, ni nada posterior a julio de 2024. Si la pregunta
    cae fuera de ese ámbito, dilo en vez de responder con lo más parecido.

    Args:
        query: la pregunta o los términos de búsqueda, en español.
        tramite: filtro opcional: proyecto | informe_ponencia | aprobacion_definitiva | debate_pleno.
        genero: filtro opcional: norma (textos legales) | debate (intervenciones).
        grupo: filtro opcional por grupo parlamentario, para intervenciones del debate:
            Socialista | Popular en el Congreso | VOX | Plurinacional SUMAR | Republicano |
            Junts per Catalunya | Euskal Herria Bildu | Vasco (EAJ-PNV) | Mixto. Basta el
            nombre, aunque la intervención esté firmada junto a otro grupo.
        k: número de fragmentos a devolver (1-10, por defecto 5).

    Returns:
        Los fragmentos más próximos, cada uno con su cita verificable
        [documento · localización · página · CVE], su trámite, su fecha, su URL y su
        texto literal. Cita SIEMPRE la referencia que acompaña a cada fragmento.
    """
    k = max(1, min(int(k), MAX_RESULTS))
    try:
        collection = pipeline._collection(ACTIVE_STRATEGY)
        if collection.count() == 0:
            return ("El índice está vacío. Ejecuta `uv run python main.py index` y vuelve a "
                    "intentarlo. No hay ningún fragmento sobre el que responder.")
        vector = pipeline.embed_texts([query], task_type="RETRIEVAL_QUERY", log=log)[0]
        results = collection.query(
            query_embeddings=[vector.tolist()],
            n_results=k,
            where=_where(tramite, genero, "", grupo),
            include=["documents", "metadatas", "distances"],
        )
    except Exception as error:  # noqa: BLE001 - report it to the model, don't crash the server
        log(f"search failed: {type(error).__name__}: {error}")
        return f"La búsqueda falló: {type(error).__name__}: {error}"

    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]
    if not documents:
        filters = ", ".join(f for f in (tramite, genero, grupo) if f) or "ninguno"
        return (f'Sin resultados para "{query}" (filtros: {filters}). '
                f"El corpus puede no cubrir esta pregunta.")

    filters = ", ".join(f for f in (tramite, genero, grupo) if f) or "ninguno"
    lines = [f'{len(documents)} fragmentos para "{query}"  ·  índice: {ACTIVE_STRATEGY}  ·  filtros: {filters}', ""]
    for position, (text, metadata, distance) in enumerate(zip(documents, metadatas, distances), start=1):
        lines += [
            f"[{position}] {_citation(metadata)}",
            f"    trámite: {metadata.get('tramite', '?')}"
            + (f"  ·  grupo: {metadata['grupo']}" if metadata.get("grupo") else "")
            + f"  ·  fecha: {metadata.get('fecha', '?')}"
            f"  ·  similitud: {1 - float(distance):.3f}",
            f"    {metadata.get('url', '')}",
            f"    «{text.strip()}»",
            "",
        ]
    return "\n".join(lines)


@mcp.tool()
def add_document(path: str) -> str:
    """Añade un documento PDF del Congreso al índice, pasándolo por el mismo pipeline
    de index.py (extracción, limpieza, troceado con metadatos, embedding y guardado).

    El documento se identifica por su propio sello CVE, de modo que el expediente,
    el trámite y el género se deducen del PDF y no del nombre del fichero.

    Qué ocurre si ya está indexado:
      - mismo documento, mismo contenido  -> no se hace nada y no se gasta cuota;
      - mismo documento, contenido distinto -> se indexa como edición revisada y los
        fragmentos anteriores se marcan como superados, pero NO se borran, porque el
        objeto de este corpus es precisamente comparar versiones;
      - documento nuevo -> se indexa.

    Gasta cuota de embeddings (unos 1.000 textos al día en el nivel gratuito), así
    que pide confirmación antes de usarla.

    Args:
        path: ruta al PDF, relativa a la raíz del proyecto, p. ej. "corpus/BOCG-15-A-1-2.PDF".

    Returns:
        Qué se hizo: identificador del documento, número de fragmentos y cuántos
        embeddings se han gastado.
    """
    try:
        candidate = Path(path)
        resolved = (candidate if candidate.is_absolute() else ROOT / candidate).resolve()
        if not str(resolved).startswith(str(ROOT)):
            return f"Ruta rechazada: {path} queda fuera del proyecto."
        if resolved.suffix.lower() != ".pdf":
            return f"Ruta rechazada: {resolved.name} no es un PDF."
        if not resolved.is_file():
            return f"No existe el fichero: {resolved.relative_to(ROOT)}"

        chunks = pipeline.chunk_file(resolved, strategy=ACTIVE_STRATEGY)
        if not chunks:
            return f"{resolved.name} no produjo ningún fragmento; ¿es un PDF de texto?"

        doc_id = chunks[0].metadata["doc_id"]
        content_hash = chunks[0].metadata["content_sha256"]
        status = pipeline.document_status(doc_id, content_hash, ACTIVE_STRATEGY)

        if status == "identical":
            # Still record it: the chunks may be in Chroma while chunks.jsonl and the
            # manifest have never heard of them.
            pipeline.record_added_document(chunks, ACTIVE_STRATEGY)
            return (f"{doc_id} ya está indexado con este mismo contenido "
                    f"({len(chunks)} fragmentos). No se ha gastado ningún embedding.")

        collection = pipeline._collection(ACTIVE_STRATEGY)
        superseded = 0
        if status == "revised":
            existing = collection.get(where={"doc_id": doc_id}, include=["metadatas"])
            ids = existing.get("ids") or []
            metadatas = existing.get("metadatas") or []
            stale = [(i, m) for i, m in zip(ids, metadatas) if m.get("content_sha256") != content_hash]
            if stale:
                collection.update(
                    ids=[i for i, _ in stale],
                    metadatas=[{**m, "superseded": True} for _, m in stale],
                )
                superseded = len(stale)

        result = pipeline.embed_and_store(chunks, strategy=ACTIVE_STRATEGY, log=log)
        pipeline.record_added_document(chunks, ACTIVE_STRATEGY)
        note = f" Se han marcado como superados {superseded} fragmentos de la edición anterior." if superseded else ""
        return (f"Indexado {doc_id} ({status}): {result['chunks']} fragmentos, "
                f"{result['embedded']} embeddings nuevos, índice «{ACTIVE_STRATEGY}».{note}")
    except Exception as error:  # noqa: BLE001 - report it to the model, don't crash the server
        log(f"add_document failed: {type(error).__name__}: {error}")
        return f"No se pudo añadir el documento: {type(error).__name__}: {error}"


if __name__ == "__main__":
    log(f"corpus server: índice «{ACTIVE_STRATEGY}» en {pipeline.CHROMA_DIR}")
    mcp.run()  # stdio
