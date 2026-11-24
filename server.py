"""MCP tools for the PostgreSQL documentation research assistant."""
import json

from mcp.server.mcpserver import MCPServer

import retrieval
from index import add_file

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search PostgreSQL 17.12 backup, recovery and standby documentation. Returns five passages with citation ID, source, section, URL and text. Supply one natural-language query."""
    return json.dumps(retrieval.search(query), ensure_ascii=False)


@mcp.tool()
def add_document(path: str) -> str:
    """Index an approved local UTF-8 text or Markdown document, using headings for citations. An unchanged document is skipped. Changed content replaces the same source name."""
    return json.dumps(add_file(path), ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
