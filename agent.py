"""
Assignment 3: tu agente (`main.py ask "pregunta"` ejecuta `python agent.py "pregunta"`).

Arnés propio con LangChain `create_agent` sobre Gemini:
  - Herramientas: las de server.py, por MCP (arrancamos el servidor como lo haría tu editor).
  - System prompt: AGENTS.md, tal cual.
  - Aprobación humana antes de que add_document se ejecute (se pide en el terminal;
    sin terminal interactivo, p. ej. en la evaluación, se deniega).
  - Límite de llamadas: máx. config.MAX_TOOL_CALLS herramientas y config.MAX_MODEL_CALLS
    llamadas al modelo por pregunta (middleware de LangChain).
  - Guardarraíl extra (elegido): VALIDACIÓN DE CITAS. Cada cita [doc_id, p. N] de la
    respuesta tiene que corresponder a un fragmento que search devolvió en ESTA pregunta.
    Si falta alguna cita o hay una inventada, se le pide al modelo UNA corrección; si
    sigue mal, la respuesta se bloquea y se sustituye por el rechazo.

evaluate.py usa la clase Harness (una sola sesión MCP para todas las preguntas).
"""

from __future__ import annotations

import asyncio
import sys
import time
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

import config
from retrieval import citation_is_valid, find_citations, parse_hits

ROOT = Path(__file__).resolve().parent
# Los modelos Gemini 3.x ignoran temperature y lo avisan en cada llamada: el aviso es
# inofensivo (solo significa que las respuestas pueden variar entre ejecuciones).
warnings.filterwarnings("ignore", message=".*uses fixed sampling defaults.*")
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------------------
# Piezas sueltas (fáciles de probar por separado)
# --------------------------------------------------------------------------------------
def is_refusal(answer: str) -> bool:
    return config.REFUSAL_PHRASE.lower() in answer.strip().lower()[:300]


def check_citations(answer: str, retrieved: list[dict]) -> list[str]:
    """Guardarraíl de citas. Devuelve la lista de problemas (vacía = OK)."""
    if is_refusal(answer):
        return []
    cites = find_citations(answer)
    if not cites:
        return ["la respuesta no tiene ninguna cita [doc_id, p. N]"]
    bad = sorted({f"[{d}, p. {p}]" for d, p in cites if not citation_is_valid(d, p, retrieved)})
    return [f"la cita {b} no corresponde a ningún fragmento devuelto por search" for b in bad]


def cli_approve(path: str) -> bool:
    """Aprobación humana para add_document. Sin terminal interactivo => NO."""
    if not sys.stdin.isatty():
        print(f"[aprobación] add_document({path!r}) denegado: no hay nadie para aprobarlo.", file=sys.stderr)
        return False
    answer = input(f"\n[APROBACIÓN] El agente quiere AÑADIR al índice el fichero:\n    {path}\n"
                   f"Esto gasta cuota de embeddings y cambia el índice. ¿Lo apruebas? [s/N] ")
    return answer.strip().lower() in {"s", "si", "sí", "y", "yes"}


def build_model():
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    load_api_key()
    return ChatGoogleGenerativeAI(model=config.CHAT_MODEL, temperature=0, max_retries=6)


def message_text(msg) -> str:
    """El contenido de Gemini puede venir como lista de bloques; nos quedamos con el texto."""
    text = getattr(msg, "text", None)
    if isinstance(text, str):
        return str(text)
    content = msg.content
    if isinstance(content, list):
        return "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return str(content)


# --------------------------------------------------------------------------------------
# El arnés
# --------------------------------------------------------------------------------------
class Harness:
    def __init__(self, approve=cli_approve, model=None):
        self.approve = approve
        self.model = model
        self.trace: list[dict] = []

    async def __aenter__(self) -> "Harness":
        from langchain.agents import create_agent
        from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        from api_key import load_api_key

        self._stack = AsyncExitStack()
        # MCP no hereda el entorno: pasamos la key y la carpeta del índice explícitamente.
        env = {"RAG_INDEX_DIR": str(config.INDEX_DIR)}
        key = load_api_key(required=False)
        if key:
            env["GEMINI_API_KEY"] = key
        params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=env)
        try:
            read, write = await self._stack.enter_async_context(stdio_client(params))
            self.session = await self._stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()
            mcp_tools = (await self.session.list_tools()).tools
            self.tools = [self._wrap(t) for t in mcp_tools]
            self.agent = create_agent(
                self.model or build_model(),
                tools=self.tools,
                system_prompt=SYSTEM_PROMPT,
                middleware=[
                    ToolCallLimitMiddleware(run_limit=config.MAX_TOOL_CALLS, exit_behavior="continue"),
                    ModelCallLimitMiddleware(run_limit=config.MAX_MODEL_CALLS, exit_behavior="end"),
                ],
            )
        except BaseException:
            await self._stack.aclose()   # cierra el servidor MCP si algo falla al arrancar
            raise
        return self

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    def _wrap(self, mcp_tool):
        """Convierte una herramienta MCP en una herramienta de LangChain que además
        (1) pide aprobación si es add_document y (2) apunta todo en self.trace."""
        from langchain_core.tools import StructuredTool

        name = mcp_tool.name

        async def call(**kwargs) -> str:
            if name == "add_document":
                approved = self.approve(kwargs.get("path", ""))
                self.trace.append({"tool": name, "args": kwargs, "approved": approved})
                if not approved:
                    return ("DENEGADO: el usuario no ha aprobado añadir este documento. No lo vuelvas a "
                            "intentar; explica que hace falta su aprobación.")
            result = await self.session.call_tool(name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            self.trace.append({"tool": name, "args": kwargs, "result": text,
                               "error": bool(getattr(result, "is_error", getattr(result, "isError", False)))})
            return text

        return StructuredTool.from_function(
            coroutine=call, name=name, description=mcp_tool.description or name,
            args_schema=mcp_tool.input_schema,
        )

    def retrieved(self) -> list[dict]:
        """Fragmentos que search devolvió durante la pregunta actual."""
        hits = []
        for step in self.trace:
            if step["tool"] == "search" and "result" in step:
                hits += parse_hits(step["result"])
        return hits

    async def ask(self, question: str) -> dict:
        self.trace = []
        t0 = time.time()
        result = await self.agent.ainvoke({"messages": [{"role": "user", "content": question}]})
        messages = result["messages"]
        answer = message_text(messages[-1])

        # Guardarraíl de citas: una oportunidad de corregir; si no, se bloquea.
        guardrail = {"fired": False, "problems": [], "blocked": False}
        problems = check_citations(answer, self.retrieved())
        if problems:
            # Guardamos el texto original: hace falta para el análisis de fallos y el REPORT.
            guardrail.update(fired=True, problems=problems, original_answer=answer)
            fix = (f"GUARDARRAÍL: tu respuesta no cumple las reglas: {'; '.join(problems)}. "
                   f"Reescríbela usando SOLO citas [doc_id, p. N] que aparezcan en los resultados de "
                   f"search (puedes buscar otra vez), o, si no tienes base en ellos, empieza la respuesta "
                   f"con «{config.REFUSAL_PHRASE}».")
            result = await self.agent.ainvoke({"messages": messages + [{"role": "user", "content": fix}]})
            messages = result["messages"]
            answer = message_text(messages[-1])
            guardrail["second_answer"] = answer
            still = check_citations(answer, self.retrieved())
            if still:
                guardrail.update(blocked=True, problems=problems + still)
                answer = (f"{config.REFUSAL_PHRASE} con fuentes verificables. "
                          f"(Respuesta bloqueada por el guardarraíl de citas: {'; '.join(still)}.)")

        usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        for m in messages:
            for k in usage:
                usage[k] += (getattr(m, "usage_metadata", None) or {}).get(k, 0) or 0
        return {
            "question": question,
            "answer": answer,
            "refusal": is_refusal(answer),
            "citations": sorted({f"[{d}, p. {p}]" for d, p in find_citations(answer)}),
            "retrieved": self.retrieved(),
            "trace": self.trace,
            "tool_calls": sum(1 for s in self.trace if "result" in s or "approved" in s),
            "guardrail": guardrail,
            "seconds": round(time.time() - t0, 2),
            **usage,
        }


async def ask_once(question: str) -> dict:
    async with Harness() as h:
        return await h.ask(question)


def run_agent(question: str) -> dict:
    """Versión síncrona: devuelve la respuesta y la traza de herramientas."""
    return asyncio.run(ask_once(question))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Uso: python agent.py "tu pregunta"')
    # En Windows, con la salida redirigida, un carácter raro (→, emojis) no debe tumbar el programa.
    sys.stdout.reconfigure(errors="replace")
    out = run_agent(" ".join(sys.argv[1:]))
    print(out["answer"])
    print("\nFuentes consultadas:")
    titles = {(h["doc_id"]): h["title"] for h in out["retrieved"]}
    for c in out["citations"]:
        doc = c[1:].split(",")[0]
        print(f"  {c} {titles.get(doc, '')}")
    if not out["citations"]:
        print("  (ninguna cita)")
    g = out["guardrail"]
    if g["fired"]:
        print(f"\n[guardarraíl de citas] {'BLOQUEADA' if g['blocked'] else 'corregida'}: {'; '.join(g['problems'])}")
        print("\n--- Primera respuesta del agente (la que paró el guardarraíl) ---")
        print(g.get("original_answer", ""))
        print("--- Fin de la primera respuesta (arriba del todo está la respuesta final) ---")
    print(f"\n[{out['tool_calls']} llamadas a herramientas · {out['total_tokens']} tokens · {out['seconds']} s]")


if __name__ == "__main__":
    main()
