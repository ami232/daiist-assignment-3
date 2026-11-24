"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it and stores it.

It loads index/ at startup and never re-embeds the corpus: the only embeddings it asks
Gemini for are new search queries (cached in index/query_vectors.json) and the chunks of a
document added with add_document. Nothing is printed to stdout, which carries the MCP
protocol; logs go to stderr. The docstrings below are the tool descriptions the model reads.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

import config
import index
import retrieval

mcp = MCPServer("corpus", log_level="WARNING")

# Loaded once at startup from the committed index.
RETRIEVER = retrieval.Retriever(config.CHOSEN_DESIGN, config.CHOSEN_METHOD)
QUERY_CACHE = index.load_query_cache()
ALLOWED_SUFFIXES = {".pdf", ".txt", ".md", ".html", ".htm"}
index.log(f"corpus server: {len(RETRIEVER.ids)} chunks, design={RETRIEVER.design}, method={RETRIEVER.method}")


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish and EU wine regulations for passages that answer a question.

    The corpus holds: EU Delegated Regulation 2019/33 (wine labelling, traditional terms,
    sugar terms, allergens), the specification ("pliego de condiciones") of DOCa Rioja
    (ageing rules for Crianza/Reserva/Gran Reserva, grape varieties, yields, labelling,
    bottling), Ley 24/2003 de la Viña y del Vino (infringements and fines), Ley 6/2015 on
    supra regional PDOs/PGIs (Consejos Reguladores, infringements, fines) and Real Decreto
    1363/2011 on Spanish wine labelling. Other denominations (for example Ribera del Duero),
    rules outside the EU, prices and market data are not in it unless added later.

    Use it before answering any question about these rules; write the query in Spanish
    with the key terms (for example "Gran Reserva tinto Rioja meses barrica"). Call it again with
    a different query if a question has two parts.

    Returns the 5 most relevant passages, each headed by the citation to copy into the
    answer, in the form [source, location], for example [pliego_doca_rioja, Sección 3.c].
    """
    query = query.strip()
    if not query:
        return "Empty query."
    vector = index.embed_query(query, QUERY_CACHE)
    hits = RETRIEVER.search(query, vector, config.TOP_K)
    return retrieval.format_results(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document (PDF, TXT, MD or HTML file on this computer) to the corpus.

    The file goes through the same pipeline as the base corpus: text extraction, cleaning,
    splitting into articles or sections with their location, chunking, Gemini embeddings,
    storage in the index. Its source name is the file name without extension.

    If the same file (same content hash) is already indexed, nothing is embedded and the
    tool says so. If a different version of a document with the same name is indexed, its
    old chunks are replaced. Returns what was done and how many chunks were stored.
    Use only when the user explicitly asks to add a document.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = (config.ROOT / file).resolve()
    if not file.is_file():
        return f"Error: no file at {file}."
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Error: unsupported file type {file.suffix}. Use PDF, TXT, MD or HTML."

    known = {d["id"]: d for d in config.DOCUMENTS + config.EXTRA_DOCUMENTS}
    doc_id = file.stem.lower().replace(" ", "_").replace("-", "_")
    doc = dict(known.get(doc_id, {"id": doc_id, "title": file.stem}))
    doc.setdefault("urls", [str(file)])

    sha = index.file_sha256(file)
    collection = RETRIEVER.collection
    same_file = collection.get(where={"file_sha256": sha}, include=["metadatas"])
    if same_file["ids"]:
        source = same_file["metadatas"][0]["source"]
        return (f"Already indexed: this exact file is in the index as '{source}' "
                f"({len(same_file['ids'])} chunks). Nothing was embedded.")

    old = collection.get(where={"source": doc["id"]}, include=[])
    chunks = index.chunk_file(file, config.CHOSEN_DESIGN, doc)
    if not chunks:
        return f"Error: no text could be extracted from {file.name}."
    if old["ids"]:
        collection.delete(ids=old["ids"])
    try:
        embedded = index.embed_and_store(chunks, collection)
    except index.QuotaExhausted:
        RETRIEVER.reload()
        return ("Error: the daily embedding quota ran out while adding the document. The chunks "
                "embedded so far are saved; call add_document again after the quota resets.")
    RETRIEVER.reload()
    action = f"Replaced the previous version of '{doc['id']}' ({len(old['ids'])} old chunks removed)" if old["ids"] \
        else f"Added '{doc['id']}'"
    return (f"{action}: {len(chunks)} chunks stored ({embedded} embedded), located by "
            f"{chunks[0]['metadata']['location'].split()[0].lower()}. It is now searchable.")


if __name__ == "__main__":
    mcp.run()  # stdio
