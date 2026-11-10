
"""
Assignment 3 — MCP Server

Exposes the EU Regulatory Compliance RAG
as tools accessible to AI agents.

Tools:
1. search(query): retrieve relevant chunks with citations.
2. add_document(path): index an additional PDF document.

The existing ChromaDB index is loaded without
re-embedding the original corpus.
"""

import sys
from pathlib import Path
from contextlib import redirect_stdout

from mcp.server.mcpserver import MCPServer

from retrieval import search as retrieve_chunks
from index import add_document_to_index, get_collection


mcp = MCPServer("corpus", log_level="WARNING")


# --------------------------------------------------
# SEARCH TOOL
# --------------------------------------------------

@mcp.tool()
def search(query: str) -> str:
    """
    Search the EU regulatory compliance document collection.

    Use this tool to answer questions about the GDPR,
    EU AI Act and Digital Services Act.

    Returns the five most semantically relevant passages
    with their document source, article or section,
    page numbers and citation identifiers.

    The retrieved passages are evidence for answering.
    If they do not contain sufficient information,
    the agent should say it cannot determine the answer.
    """

    results = retrieve_chunks(query, k=5)

    if not results:
        return "No relevant passages found."

    output = []

    for rank, result in enumerate(results, start=1):

        source = result["source"]
        article = result["article"]

        if article == 0:
            location = (
                f"Pages {result['page_start']}-"
                f"{result['page_end']}"
            )
        else:
            location = f"Article {article}"

        citation = (
            f"{source}, {location}, "
            f"PDF page {result['page_start']}"
        )

        output.append(
            f"[Result {rank}]\n"
            f"Citation: {citation}\n"
            f"Chunk ID: {result['id']}\n"
            f"Text:\n{result['text']}"
        )

    return "\n\n---\n\n".join(output)


# --------------------------------------------------
# ADD DOCUMENT TOOL
# --------------------------------------------------

@mcp.tool()
def add_document(path: str) -> str:
    """
    Add a local PDF document to the EU regulatory corpus.

    Provide the absolute or relative file path.
    The document is extracted, cleaned, chunked,
    embedded with Gemini and stored in ChromaDB.

    Already indexed chunks are skipped, preventing
    duplicate embeddings.

    This operation modifies the persistent index
    and uses Gemini embedding API quota.
    """

    pdf_path = Path(path).resolve()

    if not pdf_path.exists():
        return f"Error: file not found: {pdf_path}"

    if not pdf_path.is_file():
        return f"Error: not a file: {pdf_path}"

    if pdf_path.suffix.lower() != ".pdf":
        return "Error: only PDF documents are supported."

    try:
    # Send indexing progress to stderr, not MCP stdout.
        with redirect_stdout(sys.stderr):
            result = add_document_to_index(str(pdf_path))

    except Exception as error:
        print(
            f"Document ingestion failed: {error}",
            file=sys.stderr
        )
        return f"Error adding document: {error}"

    return (
        f"Document: {result['document']}\n"
        f"Chunks extracted: {result['chunks_found']}\n"
        f"New chunks indexed: {result['chunks_added']}\n"
        f"Total vectors: {result['total_vectors']}"
    )


# --------------------------------------------------
# SERVER STARTUP
# --------------------------------------------------

if __name__ == "__main__":
    mcp.run()