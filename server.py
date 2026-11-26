"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Two tools over the saved index:

- search(query): the best passages for a question, each with a citation label.
- add_document(path): runs one more file through index.py's pipeline, embeds it
  and keeps it, so search finds it from then on.

The index in index/ is loaded once, at startup: this server never re-embeds the
corpus. Only a question (one embedding) or a document you add costs API calls.
stdout carries the MCP protocol, so everything we log goes to stderr.
"""

import os
import sys
import threading

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

import index

TOP_K = int(os.environ.get("RAG_TOP_K", index.DEFAULT_K))
MODE = os.environ.get("RAG_MODE", index.DEFAULT_MODE)

_lock = threading.Lock()
_index = index.Index()   # loads index/chunks_<design>.jsonl + vectors (+ added/ documents); no API call
index.log(f"corpus server: {len(_index.chunks)} chunks, design={_index.design}, mode={MODE}, k={TOP_K}")

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool(annotations=ToolAnnotations(title="Search the drone-regulation corpus", read_only_hint=True,
                                      open_world_hint=False))
def search(query: str) -> str:
    """Search the drone-regulation corpus and return the best-matching passages.

    The corpus holds the EU rules for flying drones: Implementing Regulation (EU) 2019/947 (the
    open, specific and certified categories, remote pilots, registration, geographical zones),
    Delegated Regulation (EU) 2019/945 (what a drone must meet: classes C0 to C6, remote
    identification, CE marking, noise), Regulation (EU) 2021/664 (U-space airspace and its
    services) and Regulation (EU) No 376/2014 (reporting of accidents and incidents), in the
    consolidated English versions, plus any file added with add_document.

    Use it for every question about what these rules say; never answer such a question from
    memory. Write the query as the question itself or as the key terms you need; article numbers
    and section codes such as UAS.OPEN.030 work too. For a question with several parts, search
    once per part.

    Returns up to 5 passages. Each starts with a citation label in square brackets, for example
    [Reg. 2019/947, UAS.OPEN.030], then its location and its text. Cite a passage by copying its
    label exactly. If no passage answers the question, the corpus does not cover it.
    """
    try:
        with _lock:
            current = _index
        hits = current.search(query, k=TOP_K, mode=MODE)
        return index.format_hits(query, hits)
    except Exception as error:  # noqa: BLE001 - tell the model the search failed, not that nothing matched
        index.log(f"search failed: {type(error).__name__}: {error}")
        return f"ERROR: the search failed ({type(error).__name__}: {error}). This does not mean the corpus lacks the answer."


@mcp.tool(annotations=ToolAnnotations(title="Add a document to the corpus", read_only_hint=False,
                                      destructive_hint=False, idempotent_hint=True, open_world_hint=False))
def add_document(path: str) -> str:
    """Add one more document (PDF, HTML or text file) to the corpus so that search can find it.

    Give the path of a file on this computer. The file is read, cleaned, cut into chunks along its
    articles or sections, embedded and stored in the index; it is searchable straight away. This
    changes the shared index and uses embedding quota, so call it only when the user explicitly
    asks for a file to be added.

    Adding the same file again (identical content) does nothing. A file with the same name but
    different content replaces the earlier version. A name used by a base corpus document is
    refused. Returns one line saying what happened, for example how many chunks were indexed.
    """
    global _index
    message = index.add_document(path)
    try:
        fresh = index.Index()   # pick up the new chunks (an error above leaves the old index in place)
        with _lock:
            _index = fresh
    except Exception as error:  # noqa: BLE001
        index.log(f"could not reload the index: {type(error).__name__}: {error}")
    return message


if __name__ == "__main__":
    mcp.run()  # stdio
