"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through ingest.py's pipeline, embeds it
  and stores it.

Loads the committed index/ (never re-embeds the corpus: only the query of each
search, and the new chunks of an added document, are embedded). Prints nothing
to stdout, which carries the MCP protocol; logs go to stderr.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

from ingest import QuotaExhausted, add_document as ingest_add_document, log
from retrieval import DEFAULT_K, SERVED_DESIGN, SERVED_METHOD, SIMILARITY_FLOOR, indexed_acts, search as retrieve

ROOT = Path(__file__).resolve().parent

mcp = MCPServer("corpus", log_level="WARNING")


def format_hits(query: str, hits: list[dict]) -> str:
    acts = f"Indexed acts (all part of the corpus): {', '.join(indexed_acts())}"
    if not hits:
        return f"{acts}\nNo passages found for: {query}"
    lines = [acts, f"{len(hits)} passages for: {query}", ""]
    for i, h in enumerate(hits, 1):
        score = f"similarity {h['score']:.3f}" if h.get("score") is not None else "keyword match"
        lines.append(f"[{i}] {h['doc']} {h['location']} ({score})")
        lines.append(h["text"])
        lines.append("")
    lines.append("Cite passages as '<regulation> <location>', e.g. 'GDPR Article 33(1)'. "
                 "If none of them answers the question, say the corpus does not cover it.")
    return "\n".join(lines)


@mcp.tool()
def search(query: str) -> str:
    """Search EU data and AI legislation: the GDPR (Regulation 2016/679), the AI Act
    (Regulation 2024/1689) and the Data Act (Regulation 2023/2854), plus any act added
    with add_document. Only the binding articles and annexes are indexed, not the recitals.

    Use it for any question about obligations, deadlines, fines, definitions or rights
    under these laws. Write the query as a natural-language question or topic in English;
    call it again with other wording, or once per regulation, if the first results miss.

    Returns the list of acts currently indexed (documents added later appear there and are
    part of the corpus), then the most relevant passages, each with its citation (act,
    article and paragraph, e.g. "GDPR Article 33(1)"), a similarity score and the legal text.
    A passage that is only loosely related does not answer the question.
    """
    try:
        hits = retrieve(query, design=SERVED_DESIGN, method=SERVED_METHOD, k=DEFAULT_K)
    except QuotaExhausted as e:
        return f"Search unavailable: {e} Do not answer from memory; tell the user to try again later."
    except Exception as e:  # noqa: BLE001 - e.g. a transient 503 from the embedding API
        log(f"search failed: {type(e).__name__}: {e}")
        return (f"Search failed ({type(e).__name__}); this is temporary. Try the search again once; "
                "if it fails again, do not answer from memory.")
    if hits and hits[0]["score"] is not None and hits[0]["score"] < SIMILARITY_FLOOR:
        return (f"No relevant passages found for: {query} (best similarity {hits[0]['score']:.3f} is below "
                f"{SIMILARITY_FLOOR}). The indexed legislation does not appear to cover this question.")
    return format_hits(query, hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one EU legal act to the searchable index. `path` is an EUR-Lex HTML file
    (the "HTML" version of an act on eur-lex.europa.eu) inside this repository,
    e.g. "corpus/raw/L_2022333EN.01008001.xml.html".

    The file goes through the same pipeline as the initial corpus: articles and
    annexes are parsed with their locations, chunked, embedded and stored.
    If the act (same CELEX number) is already indexed with identical text, nothing
    is done; if its text changed, the outdated passages are replaced.

    Returns what happened: added / replaced / already indexed, and how many
    passages were stored and embedded.
    """
    file = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    if ROOT not in file.parents:
        return f"Refused: {path} is outside the project folder. Only files inside the repository can be added."
    if file.suffix.lower() not in (".html", ".htm"):
        return f"Refused: {file.name} is not an HTML file. add_document expects an EUR-Lex HTML act."
    if not file.is_file():
        return f"Not found: {path}"
    try:
        report = ingest_add_document(file, designs=[SERVED_DESIGN])
    except QuotaExhausted as e:
        return f"Stopped: {e} The passages embedded so far are saved; call add_document again later to finish."
    except ValueError as e:
        return f"Not added: {e}"
    r = report["designs"][SERVED_DESIGN]
    log(f"add_document {file.name}: {r}")
    status = r["status"]
    if status == "already indexed":
        return f"{report['doc']} (CELEX {report['celex']}) is already indexed with identical text; nothing was changed."
    extra = f", {r['removed_outdated']} outdated passages removed" if r.get("removed_outdated") else ""
    return (f"{report['doc']} (CELEX {report['celex']}): {status}. {r['chunks']} passages stored, "
            f"{r['new_embeddings']} newly embedded{extra}. It is now searchable with the search tool.\n"
            f"Title: {report['title']}")


if __name__ == "__main__":
    mcp.run()  # stdio
