"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Two tools over the food-safety index built by index.py:
- search(query): the best-matching chunks, each with a citation to copy;
- add_document(path): runs a file through index.py's pipeline and stores it.

It loads the committed index/ and never re-embeds the corpus: the only Gemini
calls are one embedding per new query (cached) and the chunks of an added file.
Nothing is printed to stdout (it carries the protocol); logs go to stderr.
"""

import json
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

import index

mcp = MCPServer("corpus", log_level="WARNING")

ROOT = Path(__file__).resolve().parent
ALLOWED_SUFFIXES = {".pdf", ".txt", ".md", ".html", ".htm"}
MAX_FILE_MB = 20


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def search(query: str, k: int = 5) -> str:
    """Search the food-safety corpus: the FDA Food Code 2022 (Chapters 1-7: definitions,
    management and personnel, food, equipment, water and plumbing, physical facilities,
    poisonous or toxic materials), the FDA Employee Health and Personal Hygiene Handbook,
    and the FDA HACCP manual for food service and retail operators.

    Use it for any question about how a restaurant or other food establishment must
    handle food, employees, equipment or premises: temperatures and times, cooking,
    cooling, holding, date marking, sick workers, handwashing, cleaning and sanitizing,
    HACCP. Search again with different words (e.g. the Food Code's own terms such as
    "TCS food", "PIC", "ready-to-eat") if the first results do not answer the question.

    Returns up to k (default 5, max 10) passages, best first. Each starts with a
    citation such as [food_code_2022, §3-501.16, p. 93] that must be copied exactly
    when citing it, then its similarity score (0-1) and the passage text.
    """
    k = max(1, min(int(k), 10))
    try:
        results = index.search(query, k=k)
    except Exception as error:  # noqa: BLE001 - tell the model, don't crash the server
        return f"Search failed: {type(error).__name__}: {error}"
    if not results:
        return "No passages found."
    parts = []
    for r in results:
        heading = f" ({r['heading']})" if r.get("heading") else ""
        parts.append(f"{r['cite']} score={r['score']:.3f}{heading}\n{r['text']}")
    return "\n\n---\n\n".join(parts)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))
def add_document(path: str) -> str:
    """Add one document to the food-safety index so search can find it.

    `path` is a PDF, .txt, .md or .html file inside this project folder (for example
    corpus/new_guidance.pdf). The file is extracted, cleaned, chunked, embedded with
    Gemini and stored, exactly like the built-in corpus.

    If the same file content is already indexed, nothing changes. If a different
    version of a document with the same file name is indexed, its old chunks are
    replaced. Returns JSON with status (added, replaced or already_indexed), the
    source name to cite and the number of chunks. Only use it when the user asks
    to add a document; it changes the index for everyone.
    """
    file = Path(path).expanduser()
    file = (ROOT / file if not file.is_absolute() else file).resolve()
    # Guardrail: only files from this project, of a known type and size, can be indexed,
    # so the tool cannot be used to read and expose arbitrary files on the machine.
    if ROOT not in file.parents:
        return json.dumps({"status": "refused", "reason": f"{path} is outside the project folder {ROOT}"})
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return json.dumps({"status": "refused", "reason": f"file type {file.suffix!r} is not supported"})
    if not file.is_file():
        return json.dumps({"status": "error", "reason": f"no file at {file}"})
    if file.stat().st_size > MAX_FILE_MB * 1e6:
        return json.dumps({"status": "refused", "reason": f"file is larger than {MAX_FILE_MB} MB"})
    try:
        result = index.add_file(file)
    except index.QuotaExhausted:
        return json.dumps({"status": "error", "reason": "the Gemini daily embedding limit is used up; try after it resets"})
    except Exception as error:  # noqa: BLE001
        return json.dumps({"status": "error", "reason": f"{type(error).__name__}: {error}"})
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()  # stdio
