"""
Assignment 3: LangChain agent.

    main.py ask "question"  →  python agent.py "question"

Uses the same search function as server.py (imported from index.py),
Gemini as the LLM, and AGENTS.md as the system prompt.

Guardrails:
  - Human approval before add_document runs.
  - Pre-retrieval score check: refuse without calling the LLM when the best
    cosine-similarity score is below SCORE_THRESHOLD.
"""

import sys
from pathlib import Path

from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from api_key import load_api_key
from index import search_index, chunk_file, embed_and_store

ROOT = Path(__file__).resolve().parent

SCORE_THRESHOLD = 0.25          # cosine-similarity floor for the top result
LLM_MODEL = "gemini-3.5-flash-lite"


# ---------------------------------------------------------------------------
# Tools (wrapping the same functions the MCP server exposes)
# ---------------------------------------------------------------------------

@tool
def search(query: str) -> str:
    """Search the music-copyright corpus for passages about copyright
    registration, royalties, sound recordings, musical compositions,
    performance rights, mechanical rights and related legal rules.
    Returns up to 5 text chunks with source citations."""
    results = search_index(query, k=5)
    if not results:
        return "No relevant passages found in the corpus."
    parts = []
    for r in results:
        parts.append(
            f"[{r['source']}, {r['location']}] (score: {r['score']:.3f})\n"
            f"{r['text']}"
        )
    return "\n\n---\n\n".join(parts)


@tool
def add_document(path: str) -> str:
    """Add a new PDF document to the corpus index.  Requires user approval."""
    fp = Path(path)
    if not fp.exists():
        return f"Error: file not found: {path}"
    print(f"\nThe agent wants to add document: {path}", file=sys.stderr)
    try:
        approval = input("Allow adding this document? (y/n): ")
    except EOFError:
        approval = "n"
    if approval.strip().lower() != "y":
        return "Document addition was rejected by the user."
    chunks = chunk_file(fp, design="structure")
    n = embed_and_store(chunks, "structure_chunks")
    return f"Added {n} chunks from {fp.name} to the index."


# ---------------------------------------------------------------------------
# Agent entry point
# ---------------------------------------------------------------------------

def ask(question: str, interactive: bool = True) -> dict:
    """Run the agent.  Returns a dict with answer, tool_calls, chunks, etc.

    When *interactive* is False the add_document tool is omitted and
    no approval prompt is shown (used by evaluate.py).
    """
    api_key = load_api_key()

    # --- Guardrail: pre-check retrieval score ---
    pre_results = search_index(question, k=5)
    if not pre_results or pre_results[0]["score"] < SCORE_THRESHOLD:
        answer = (
            "I don't have enough relevant information in my corpus to answer "
            "this question reliably. Please consult a music lawyer or your "
            "collecting society for guidance."
        )
        return {
            "answer": answer,
            "tool_calls": [{"tool": "search", "input": {"query": question}}],
            "chunks": pre_results,
            "refused": True,
            "guardrail": "low_score",
        }

    # --- Build the agent ---
    system_prompt = ""
    agents_md = ROOT / "AGENTS.md"
    if agents_md.exists():
        system_prompt = agents_md.read_text(encoding="utf-8")

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=api_key,
        temperature=0.1,
    )

    tools = [search, add_document] if interactive else [search]

    graph = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    # Retry on transient API errors (503, rate limits)
    import time as _time
    last_err = None
    for attempt in range(3):
        try:
            result = graph.invoke({"messages": [{"role": "user", "content": question}]})
            break
        except Exception as e:
            last_err = e
            if "503" in str(e) or "UNAVAILABLE" in str(e) or "429" in str(e):
                wait = 5 * (attempt + 1)
                print(f"  Retrying in {wait}s ({e.__class__.__name__}) …", file=sys.stderr)
                _time.sleep(wait)
            else:
                raise
    else:
        raise last_err  # type: ignore[misc]

    # Extract the final answer from the last AI message
    answer_text = ""
    tool_calls_log = []
    for msg in result.get("messages", []):
        if not hasattr(msg, "type"):
            continue
        if msg.type == "ai" and msg.content:
            content = msg.content
            # content may be a string or a list of content blocks
            if isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, str):
                        parts.append(block)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block["text"])
                answer_text = "\n".join(parts)
            else:
                answer_text = content
        if msg.type == "tool":
            tool_calls_log.append(
                {"tool": getattr(msg, "name", ""), "input": {}}
            )

    return {
        "answer": answer_text,
        "tool_calls": tool_calls_log,
        "chunks": pre_results,
        "refused": False,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py \"your question\"", file=sys.stderr)
        sys.exit(1)
    question = " ".join(sys.argv[1:])
    out = ask(question)
    print(out["answer"])
