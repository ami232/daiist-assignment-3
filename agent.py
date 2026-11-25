"""
Assignment 3: the harness. `main.py ask "your question"` runs `python agent.py "question"`.

LangChain `create_agent` on Gemini, with the tools from server.py reached over MCP and
AGENTS.md as the system prompt.

Guardrails, in the order they fire:
  1. scope guard   - refuses predictions, verdicts and motive-hunting BEFORE retrieving;
  2. call limit    - at most MAX_TOOL_CALLS tool calls per question;
  3. approval      - add_document never runs without a typed yes (denied when not a TTY);
  4. citation check- an answer citing a document that was never retrieved is replaced
                     by a refusal, because that is fabrication.

evaluate.py imports answer(), which returns the answer, the citations, the tool trace,
token counts and wall time.

    uv run python agent.py "¿Qué exige el artículo primero sobre las candidaturas?"
    uv run python agent.py --list-models      # if the chat model name is wrong
"""

from __future__ import annotations

import argparse
import asyncio
import os
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENTS_MD = ROOT / "AGENTS.md"

# Override with GEMINI_CHAT_MODEL if this id is wrong for your project;
# `python agent.py --list-models` prints what your key can actually see.
# gemini-2.5-flash is 404 for keys created recently ("no longer available to new
# users"), and the full gemini-3.x flash models answer 503 on the free tier. The
# -latest aliases track whatever is actually being served, and flash-lite is the
# one the free tier reliably serves. Override with GEMINI_CHAT_MODEL.
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-flash-lite-latest")
MAX_TOOL_CALLS = 6
EVIDENCE_CHARS = 12000      # per tool call, kept for the judge
REFUSAL = "NO CONSTA EN EL CORPUS"

CITATION = re.compile(r"\[([^\[\]]{5,200})\]")
DOC_ID = re.compile(r"\b((?:BOCG|DSCD)-[\w-]+)\b")

# Deliberately narrow. A false refusal is itself a failure category in the evaluation,
# so these patterns aim at precision, not recall: they catch questions that ask the tool
# to predict, to judge, or to impute a motive, and leave ordinary "why" questions alone
# ("¿por qué se modificó el artículo?" is answerable from the record; "¿por qué mintió?"
# is not a question about the record at all).
OUT_OF_SCOPE = (
    (re.compile(r"\b(qué har[áa]n?|volver[áa]n?|piensan? presentar|en el futuro|"
                r"predic|pronóstic|quién ganará|will they|going to)\b", re.I),
     "una predicción sobre el futuro"),
    (re.compile(r"\b(fue una (buena|mala)|fue (justa|injusta|acertada)|es (justo|injusto)|"
                r"deber[íi]an?|merece la pena|qué opinas|te parece|valora si)\b", re.I),
     "un juicio de valor"),
    (re.compile(r"\b(minti[óo]|engañ[óo]|hip[óo]crita|intenci[óo]n (real|oculta)|"
                r"motivo (real|oculto)|en realidad quer[íi]a)\b", re.I),
     "una atribución de intenciones"),
)

SCOPE_REFUSAL = (
    f"{REFUSAL}\n\n"
    "Esta herramienta solo informa de lo que consta en el expediente parlamentario del "
    "Proyecto de Ley Orgánica 121/000001: qué dice cada versión del texto, qué cambió entre "
    "fases y qué se dijo en el debate del Pleno. La pregunta pide {reason}, que no puede "
    "sostenerse citando el registro. Reformúlala sobre lo que consta: qué se aprobó, en qué "
    "fase, y quién dijo qué."
)


# --------------------------------------------------------------------------
# Guardrail 1: scope
# --------------------------------------------------------------------------

def scope_guard(question: str) -> str | None:
    """Refuse before retrieving when the question cannot be answered from any passage."""
    for pattern, reason in OUT_OF_SCOPE:
        if pattern.search(question):
            return SCOPE_REFUSAL.format(reason=reason)
    return None


# --------------------------------------------------------------------------
# The MCP bridge
# --------------------------------------------------------------------------

@asynccontextmanager
async def mcp_session():
    """Start server.py over stdio, exactly as an editor would."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


class Harness:
    """Holds the per-question state the guardrails need."""

    def __init__(self, approve: bool | None = None) -> None:
        self.calls: list[dict] = []
        self.search_output: list[str] = []
        self.retrieved_doc_ids: set[str] = set()
        self.approve = approve          # None = ask; True/False = decided in advance
        self.guardrail: str | None = None

    def over_limit(self) -> bool:
        return len(self.calls) >= MAX_TOOL_CALLS

    def record(self, name: str, arguments: dict, result: str, seconds: float) -> None:
        self.calls.append(
            {"tool": name, "args": arguments, "seconds": round(seconds, 2),
             # The judge grades "supported" against this text, so it must hold what the
             # model actually read. At 2000 chars a k=5 search was cut to its first
             # chunk or two and valid citations were scored unsupported.
             "result_chars": len(result), "result": result[:EVIDENCE_CHARS]}
        )

    # Guardrail 3 -------------------------------------------------------
    def ask_approval(self, path: str) -> tuple[bool, str]:
        if self.approve is not None:
            return self.approve, "preaprobado" if self.approve else "denegado por configuración"
        if not sys.stdin.isatty():
            return False, "sin terminal interactiva: denegado por defecto"
        print(
            f"\n  El agente quiere añadir «{path}» al índice.\n"
            f"  Esto gasta cuota de embeddings y modifica el índice compartido.",
            file=sys.stderr,
        )
        try:
            reply = input("  ¿Autorizas add_document? [s/N] ").strip().lower()
        except EOFError:
            return False, "sin entrada: denegado"
        return (reply in {"s", "si", "sí", "y", "yes"}), f"respuesta del usuario: {reply or '(vacío)'}"


def build_tools(session, harness: Harness, descriptions: dict[str, str]):
    """Wrap the MCP tools as LangChain tools.

    The names and descriptions come from the live MCP listing, so server.py's docstrings
    stay the single source of truth for what the model reads; only the signatures are
    mirrored here, so that the approval gate can sit in front of add_document.
    """
    from langchain_core.tools import StructuredTool

    async def call(name: str, arguments: dict) -> str:
        started = time.monotonic()
        if harness.over_limit():
            message = (f"Límite de {MAX_TOOL_CALLS} llamadas alcanzado. "
                       f"Responde con lo que ya tienes, o con {REFUSAL}.")
            harness.record(name, arguments, message, time.monotonic() - started)
            harness.guardrail = harness.guardrail or "call_limit"
            return message
        result = await session.call_tool(name, arguments)
        text = "\n".join(getattr(part, "text", "") for part in result.content).strip()
        harness.record(name, arguments, text, time.monotonic() - started)
        return text

    async def search(query: str, tramite: str = "", genero: str = "", k: int = 5) -> str:
        text = await call("search", {"query": query, "tramite": tramite, "genero": genero, "k": k})
        harness.search_output.append(text)
        harness.retrieved_doc_ids.update(DOC_ID.findall(text))
        return text

    async def add_document(path: str) -> str:
        allowed, why = harness.ask_approval(path)
        if not allowed:
            harness.guardrail = "approval_denied"
            message = f"Permiso denegado para añadir «{path}» ({why}). El documento NO se ha indexado."
            harness.record("add_document", {"path": path}, message, 0.0)
            return message
        return await call("add_document", {"path": path})

    return [
        StructuredTool.from_function(
            coroutine=search, name="search", description=descriptions.get("search", "")),
        StructuredTool.from_function(
            coroutine=add_document, name="add_document", description=descriptions.get("add_document", "")),
    ]


# --------------------------------------------------------------------------
# Guardrail 4: citations must point at something that was actually retrieved
# --------------------------------------------------------------------------

def check_citations(text: str, harness: Harness) -> tuple[list[str], list[str]]:
    """Return (citations found, citations naming a document never retrieved)."""
    citations = [c.strip() for c in CITATION.findall(text)]
    fabricated = []
    for citation in citations:
        cited = set(DOC_ID.findall(citation))
        if cited and not cited <= harness.retrieved_doc_ids:
            fabricated.append(citation)
    return citations, fabricated


# --------------------------------------------------------------------------
# Answering
# --------------------------------------------------------------------------

def _usage(messages) -> dict:
    totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    for message in messages:
        usage = getattr(message, "usage_metadata", None) or {}
        for key in totals:
            totals[key] += int(usage.get(key, 0) or 0)
    return totals


async def answer_async(question: str, approve: bool | None = None, validate: bool = True) -> dict:
    from langchain.agents import create_agent
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    started = time.monotonic()
    harness = Harness(approve=approve)
    base = {
        "question": question, "citations": [], "tool_calls": harness.calls,
        "retrieved_doc_ids": [], "model": CHAT_MODEL,
        "tokens": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
    }

    # Guardrail 1, before any retrieval or any token is spent.
    refusal = scope_guard(question)
    if refusal:
        return {**base, "answer": refusal, "guardrail": "scope", "refused": True,
                "seconds": round(time.monotonic() - started, 2)}

    load_api_key()
    system_prompt = AGENTS_MD.read_text(encoding="utf-8")

    async with mcp_session() as session:
        listing = await session.list_tools()
        descriptions = {t.name: (t.description or "").strip() for t in listing.tools}
        tools = build_tools(session, harness, descriptions)
        model = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0.0)
        agent = create_agent(model, tools, system_prompt=system_prompt)
        state = await agent.ainvoke(
            {"messages": [{"role": "user", "content": question}]},
            config={"recursion_limit": 2 * MAX_TOOL_CALLS + 4},
        )

    messages = state["messages"]
    text = messages[-1].content
    if isinstance(text, list):   # Gemini can return content as parts
        text = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in text)
    text = (text or "").strip()

    citations, fabricated = check_citations(text, harness)
    if validate and fabricated:
        harness.guardrail = "fabricated_citation"
        text = (f"{REFUSAL}\n\nSe ha bloqueado la respuesta: citaba {', '.join(fabricated[:3])}, "
                f"que no aparece en los fragmentos recuperados. No se puede publicar una cita "
                f"que no procede del registro.")
        citations = []

    return {
        **base,
        "answer": text,
        "citations": citations,
        "fabricated_citations": fabricated,
        "retrieved_doc_ids": sorted(harness.retrieved_doc_ids),
        "guardrail": harness.guardrail,
        "refused": REFUSAL in text,
        "tokens": _usage(messages),
        "seconds": round(time.monotonic() - started, 2),
    }


def answer(question: str, approve: bool | None = None, validate: bool = True) -> dict:
    """Synchronous entry point. evaluate.py calls this."""
    return asyncio.run(answer_async(question, approve=approve, validate=validate))


def list_models() -> int:
    from google import genai

    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    for model in client.models.list():
        actions = getattr(model, "supported_actions", None) or []
        if not actions or "generateContent" in actions:
            print(f"  {model.name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Answer one question from the corpus.")
    parser.add_argument("question", nargs="*", help="the question")
    parser.add_argument("--list-models", action="store_true", help="list models your key can use")
    parser.add_argument("--yes", action="store_true", help="pre-approve add_document (for the demo)")
    parser.add_argument("--no-citation-check", action="store_true", help="disable guardrail 4, to measure it")
    parser.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = parser.parse_args()

    if args.list_models:
        return list_models()
    if not args.question:
        parser.error('agent.py needs a question: agent.py "your question"')

    try:
        result = answer(
            " ".join(args.question),
            approve=True if args.yes else None,
            validate=not args.no_citation_check,
        )
    except Exception as error:  # noqa: BLE001 - one clear line beats a traceback here
        name = type(error).__name__
        print(f"The agent could not answer: {name}: {error}", file=sys.stderr)
        if "model" in str(error).lower() or "404" in str(error):
            print("Is CHAT_MODEL right? Run: uv run python agent.py --list-models", file=sys.stderr)
        return 1

    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(result["answer"])
    if result["citations"]:
        print("\nCitas:")
        for citation in result["citations"]:
            print(f"  [{citation}]")
    print(
        f"\n({len(result['tool_calls'])} llamadas · {result['tokens']['total_tokens']} tokens · "
        f"{result['seconds']}s" + (f" · guardarraíl: {result['guardrail']}" if result["guardrail"] else "") + ")",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
