"""Read-only search and approval-gated document ingestion over MCP stdio."""
from mcp.server.mcpserver import MCPServer
from rag_core import add_document_pipeline, search_citations
import json
import sys

mcp = MCPServer('corpus', log_level='WARNING')


@mcp.tool()
def search(query: str) -> str:
    """Search the indexed Python 3.13 reference corpus. Return the five most
    relevant verbatim passages, each with a [CITE:id], source, section and URL.
    Use this before factual answers; an absent topic is not proof of a rule.
    """
    return search_citations(query, k=5)


@mcp.tool()
def add_document(path: str) -> str:
    """Add an explicitly approved local .md/.txt/.pdf/.html document under
    incoming/ to the Python documentation index, via the shared ingestion
    pipeline. Identical files are skipped; changed files replace old chunks.
    Embedding spends Gemini API quota. NEVER call without user permission.
    """
    try:
        return json.dumps(add_document_pipeline(path), ensure_ascii=False)
    except Exception as exc:
        print(f'Add-document error: {type(exc).__name__}: {exc}', file=sys.stderr)
        return json.dumps({'error': f'{type(exc).__name__}: {exc}'})


if __name__ == '__main__':
    mcp.run()  # stdout reserved exclusively for MCP messages
