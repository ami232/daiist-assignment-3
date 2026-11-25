"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the 5 most relevant label passages, each with a citation.
- add_document(path): runs a DailyMed SPL XML label through index.py's
  pipeline (chunk_file + embed_and_store) and stores it.

Duplicate policy for add_document:
  - identical label already indexed -> nothing embedded, says so;
  - same drug, different label version -> old version's chunks deleted, new
    version indexed, so two versions never give conflicting instructions.

Loads index/ at startup and never re-embeds the corpus. Logs go to stderr:
stdout carries the MCP protocol.
"""

import os

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")  # keep chromadb quiet

from pathlib import Path  # noqa: E402

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402  (message reaches the model)

import index  # noqa: E402

ROOT = Path(__file__).resolve().parent
DESIGN = index.DEFAULT_DESIGN
K = 5

mcp = MCPServer("corpus", log_level="WARNING")
collection = index.get_collection(DESIGN)  # load the committed index once, at startup
index.log(f"corpus server: {collection.count()} chunks in design '{DESIGN}'")


def indexed_drugs() -> list[str]:
    metadatas = collection.get(include=["metadatas"])["metadatas"]
    return sorted({m["source"] for m in metadatas})


def citation(hit: dict) -> str:
    """Short citation the agent should copy into its answer, e.g. [warfarin 7.3]."""
    return f"[{hit['source']} {hit['section']}]" if hit["section"] else f"[{hit['source']}]"


def format_hit(rank: int, hit: dict) -> str:
    header, _, body = hit["text"].partition("\n")
    version = hit["version_date"]
    version = f"{version[:4]}-{version[4:6]}-{version[6:]}" if len(version) == 8 else version
    return (
        f"--- Result {rank}  cite as {citation(hit)}  (similarity {hit['score']:.2f})\n"
        f"Source: {header}; label version {version}; {hit['url']}\n"
        f"{body}"
    )


@mcp.tool()
def search(query: str) -> str:
    """Search official FDA prescribing information (DailyMed drug labels) for medicines that
    elderly heart patients commonly take: warfarin (Jantoven), apixaban (Eliquis), amiodarone
    (Pacerone), metoprolol (Lopressor), atorvastatin (Lipitor) and digoxin (Lanoxin), plus any
    label added later with add_document.

    Use it for every question about these drugs: dosing, missed doses, contraindications,
    boxed warnings, side effects, drug interactions, use in older adults or with kidney/liver
    problems, overdose, monitoring, and what the Medication Guide tells patients. For a
    question about two drugs (e.g. an interaction), search for each drug or each side of the
    question separately. Write the query in plain words, e.g. "warfarin amiodarone interaction
    INR monitoring".

    Returns the 5 most relevant passages, best first. Each has a citation to copy into the
    answer (e.g. [warfarin 7.3] = warfarin label, section 7.3), the label version, a DailyMed
    link and a similarity score. The first line lists which drugs are indexed. If no passage
    actually answers the question, the labels do not cover it: say so instead of guessing.
    """
    query = query.strip()
    if not query:
        raise ToolError("query is empty")
    hits = index.search(query, k=K, design=DESIGN)
    lines = [f"Indexed drug labels: {', '.join(indexed_drugs())}. Top {len(hits)} passages for: {query!r}"]
    lines += [format_hit(rank, hit) for rank, hit in enumerate(hits, 1)]
    return "\n\n".join(lines)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one FDA drug label to the searchable index, so search can answer questions about it.

    `path` is a local DailyMed SPL XML file (the "Download: XML" file of a label on
    dailymed.nlm.nih.gov), absolute or relative to the project folder. The label is split
    into its numbered sections, embedded with Gemini and stored with the rest of the corpus,
    using the same pipeline as the original index.

    If this exact label version is already indexed, nothing is embedded and the reply says
    so. If an older or different version of the same drug's label is indexed, its chunks are
    replaced by the new version. Returns the drug, label version and number of chunks added.
    This changes the shared index, so it needs the user's approval before it runs.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    file = file.resolve()
    if not file.is_file():
        raise ToolError(f"No file at {file}")

    try:
        chunks = index.chunk_file(file, DESIGN)
    except (ValueError, SyntaxError) as error:  # wrong type, or not parseable XML
        raise ToolError(f"Could not read {file.name} as a DailyMed SPL label: {error}") from error
    meta = chunks[0]["metadata"]
    source, version = meta["source"], meta["version_date"]
    new_ids = {c["id"] for c in chunks}

    existing = collection.get(where={"source": source}, include=["metadatas"])
    old_ids = set(existing["ids"])
    old_versions = {m["version_date"] for m in existing["metadatas"]}

    if old_ids and old_versions == {version} and old_ids == new_ids:
        return (f"Already indexed: {meta['brand']} ({source}) label version {version}, "
                f"{len(old_ids)} chunks. Nothing was embedded.")

    replaced = old_ids - new_ids  # old version, or chunks a changed chunker no longer makes
    if replaced:
        collection.delete(ids=sorted(replaced))
    added, kept = index.embed_and_store(chunks, DESIGN)
    index.log(f"add_document: {source} v{version}: {added} added, {kept} kept, {len(replaced)} removed")

    note = ""
    if old_versions and old_versions != {version}:
        note = f" Replaced the previously indexed version(s) {', '.join(sorted(old_versions))} ({len(replaced)} chunks removed)."
    return (f"Indexed {meta['brand']} ({source}) label version {version} from {file.name}: "
            f"{added} chunks embedded and stored, {kept} were already present.{note} "
            f"Search now covers: {', '.join(indexed_drugs())}.")


if __name__ == "__main__":
    mcp.run()  # stdio
