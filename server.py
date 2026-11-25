"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""
"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import ROOT, chunk_file, embed_and_store, get_collection, retrieve

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5


@mcp.tool()
def search(query: str, party: str = "") -> str:
    """Search the election programmes of four Spanish parties (PSOE, PP, Sumar, Vox) for the
    general election of 23 July 2023, plus any programme added later with add_document.

    Use it for every question about what a party proposes, promises or says in its programme.
    The programmes are written in Spanish; the question can be in English. Do NOT use it for
    election results, polls, candidates' personal lives or opinions about which party is better:
    the programmes do not contain them.

    party (optional): PSOE, PP, SUMAR or VOX. Set it when the question is about one party, so
    that party's text is not crowded out by the others. Leave it empty to search every
    programme, for example when comparing parties.

    Returns up to 5 passages, best first. Each starts with its citation in square brackets,
    such as [psoe_2023, pp. 45-46] (document, PDF pages), followed by the Spanish text and a
    distance (smaller = closer to the question). If no passage actually answers the question,
    the programmes do not cover it.
    """
    parties = [party] if party.strip() else None
    hits = retrieve(query, k=TOP_K, parties=parties)
    if not hits:
        known = sorted({m["party"] for m in get_collection().get(include=["metadatas"])["metadatas"]})
        return f"No passages found for party {party!r}. Parties in the index: {', '.join(known) or 'none'}."
    blocks = []
    for number, hit in enumerate(hits, start=1):
        citation = f"[{hit['source']}, {hit['location']}]"
        blocks.append(
            f"Passage {number} {citation}  ({hit['party']} {hit['year']}, distance {hit['distance']:.3f})\n"
            f"{hit['text']}"
        )
    return "\n\n".join(blocks)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one PDF document to the searchable index, for example a party programme from another election.

    path: location of a PDF file, relative to the project folder or absolute (for example
    demo/vox_2026.pdf). The file name decides how it is cited: name it party_year.pdf, such as
    vox_2026.pdf, so the party and year are recorded.

    The PDF is cleaned, cut into passages and embedded with the same pipeline as the original
    corpus. If the document is already indexed and unchanged, nothing is embedded and nothing
    changes. If the file changed, only the changed passages are embedded and the outdated ones
    are removed. This uses embedding quota, so only call it when the user asked to add a document.

    Returns how many passages were added, kept and removed.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        raise ValueError(f"No file at {file}. Give the path of a PDF relative to the project folder.")
    if file.suffix.lower() != ".pdf":
        raise ValueError(f"{file.name} is not a PDF. Only PDF documents can be added.")
    chunks, dropped = chunk_file(file)
    if not chunks:
        raise ValueError(f"No text could be extracted from {file.name} (a scanned PDF without a text layer?).")
    result = embed_and_store(chunks)
    return (
        f"{chunks[0]['source']} ({chunks[0]['party']} {chunks[0]['year']}): {len(chunks)} passages. "
        f"Added {result['new']}, already stored {result['already_stored']}, removed {result['removed']}. "
        f"Pages left out as covers, contents or near-empty: {sum(dropped.values())}."
    )


if __name__ == "__main__":
    mcp.run()  # stdio
