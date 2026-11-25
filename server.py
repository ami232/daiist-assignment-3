import json
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import SOURCES, chunk_file, embed_and_store, log, source_of
from retrieval import DESIGN, HYBRID, TOP_K, Retriever

mcp = MCPServer("corpus", log_level="WARNING")
retriever = Retriever(DESIGN, HYBRID)
BOOK_PAGE = {source["id"]: f"https://www.gutenberg.org/ebooks/{source['gutenberg']}" for source in SOURCES}


def citation(chunk):
    return {
        "chunk_id": chunk["id"],
        "cite_as": f"{chunk['author']}, {chunk['work']} ({chunk['year']}), {chunk['location']}",
        "author": chunk["author"],
        "work": chunk["work"],
        "year": chunk["year"],
        "location": chunk["location"],
        "similarity": chunk["similarity"],
        "url": BOOK_PAGE.get(chunk["source"], ""),
        "text": chunk["text"],
    }


@mcp.tool()
def search(query: str) -> str:
    """Search a corpus of public-domain texts in political economy and philosophy for passages.

    The corpus starts with: Mill, On Liberty (1859), chapters I-II; Marx and Engels,
    Manifesto of the Communist Party (1848, 1888 translation); Paine, Agrarian Justice (1797);
    Bastiat, That Which Is Seen, and That Which Is Not Seen (1850); Smith, The Wealth of Nations
    (1776), Book I chapter II and Book IV chapter II. Documents added later with add_document are
    searched too; each result's cite_as names the work it comes from. Use it to check whether one of these
    thinkers said something, or what they wrote on a topic. For a question about two thinkers,
    search once for each.

    Returns a JSON list of the 5 best passages, best first, each with chunk_id, cite_as
    (author, work, year, section and paragraph), similarity (0-1, how close in meaning) and the
    exact text. If no passage really answers the query, the corpus does not cover it.
    """
    return json.dumps([citation(chunk) for chunk in retriever.search(query, k=TOP_K)], ensure_ascii=False)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a plain-text (.txt) document to the corpus index, so search can find it.

    The file is cleaned, chunked and embedded like the rest of the corpus; its name is its
    source id (e.g. corpus/bastiat-government.txt). If the same text is already indexed nothing
    is embedded; if a different text with the same name is indexed, it is treated as a new
    edition and its old chunks are replaced. Returns a JSON summary of what happened.
    """
    file = Path(path)
    if file.suffix != ".txt" or not file.is_file():
        return json.dumps({"status": "error", "reason": f"{path} is not an existing .txt file"})

    global retriever
    source = source_of(file)["id"]
    chunks = chunk_file(file, DESIGN)
    store = retriever.store
    old = store.get(where={"source": source}, include=["documents"])
    old_texts = dict(zip(old["ids"], old["documents"]))

    if old_texts == {c["id"]: c["text"] for c in chunks}:
        return json.dumps({"status": "skipped", "source": source, "reason": "this text is already indexed", "chunks": len(chunks)})
    status = "added"
    if old_texts:
        # new edition replaces old
        store.delete(ids=list(old_texts))
        status = "replaced"
    embedded = embed_and_store(chunks, DESIGN)
    retriever = Retriever(DESIGN, HYBRID)  # rebuild keyword index
    log(f"add_document: {status} {source}, {embedded} chunks embedded")
    return json.dumps({"status": status, "source": source, "chunks": len(chunks), "embedded": embedded})


if __name__ == "__main__":
    mcp.run()
