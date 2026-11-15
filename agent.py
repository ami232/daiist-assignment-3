"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Ask for approval before add_document runs; add a
call limit and one guardrail of your choice. Print the answer with citations.

Guardrails: (1) approval by the user before add_document runs, (2) a limit of
MAX_TOOL_CALLS tool calls per question, (3) add_document may only read files
inside this project folder, (4) a coverage check after every search: a cheap
model must quote, word for word, the passage that answers the question; the quote
is verified in code. Verdicts are "sí", "parcial" or "no"; if every search of a
question is "no", the final answer is a fixed refusal.

For evaluate.py: `ask_many(questions)` / `ask(question)` return, per question,
the answer, the tool trace (with the full text returned by the tools), tokens
and seconds.
"""

import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent
# Free tier: about 20 requests per day per model. When a model runs out of its
# daily quota (or is not available to this key) the next one in the list is used.
AGENT_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-2.5-flash",
]
MODEL = AGENT_MODELS[0]  # kept for scripts that report "the" model
MAX_TOOL_CALLS = 6
RETRY_DELAYS = (10, 20, 30)  # seconds (max 30), for 503 / 429 from the model API
MODEL_TIMEOUT = 90  # seconds per model call; the client's own retries are off (max_retries=1)
TRANSIENT = ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "overloaded", "high demand",
             "timeout", "Timeout", "DEADLINE_EXCEEDED")
APPROVAL_TOOLS = {"add_document"}
DAILY_QUOTA = ("PerDay", "per day", "limit: 0", "NOT_FOUND")
_unusable: set[str] = set()  # models out of daily quota in this process

# Coverage check: one extra call to a cheap model after every search.
COVERAGE_MODEL = "gemini-3.5-flash-lite"
COVERAGE_MODELS = [COVERAGE_MODEL] + [m for m in AGENT_MODELS if m != COVERAGE_MODEL]
MIN_QUOTE_CHARS = 20  # a shorter "quote" (e.g. one word) would prove nothing
REFUSAL = "No consta en los documentos del corpus."
_HEAD = """Eres un verificador. Decide si alguno de estos pasajes, extraídos de normas españolas de prevención de riesgos laborales, responde a la pregunta.

Pregunta: {question}

Pasajes:
{passages}
"""
_NEED = """- Escribe primero en "need", en una sola frase, qué dato exacto pide la pregunta (por ejemplo: quién debe hacer algo; a partir de qué número; si algo está permitido; una cifra vigente hoy; qué medida concreta para un caso concreto). Si la pregunta tiene varias partes, nombra cada una.
"""
_QUOTE = """- "quote" es una frase copiada carácter a carácter del pasaje "passage" (sin parafrasear, sin puntos suspensivos)."""
# Versions of the coverage prompt, compared with coverage_eval.py.
COVERAGE_PROMPTS = {
    # v1: binary, "responds literally".
    "v1": _HEAD + """
Reglas:
- covered=true SOLO si algún pasaje responde literalmente a lo que se pregunta (o a una de las partes de la pregunta, si tiene varias).
- Un pasaje sobre un tema cercano o general NO cuenta. Si la pregunta pide algo concreto (una cifra actual, un permiso, una medida para un caso concreto) y el pasaje no lo dice expresamente, covered=false.
- Si covered=true, "passage" es el número del pasaje y "quote" una frase copiada carácter a carácter de ese pasaje que contiene la respuesta (sin parafrasear, sin puntos suspensivos).
- Si covered=false, "passage" es null y "quote" es "".

Responde solo con JSON: {{"covered": true/false, "passage": <número o null>, "quote": "<cita literal>"}}""",
    # v2: name the exact datum first; "yes" only if a passage contains that datum.
    "v2": _HEAD + """
Reglas:
""" + _NEED + """- covered=true SOLO si algún pasaje contiene ese dato exacto (o el de una de las partes, si hay varias). No basta con que el pasaje trate el mismo tema ni con una regla general cercana de la que habría que deducirlo.
- Si covered=true, "passage" es el número del pasaje y "quote" la frase que contiene ese dato.
""" + _QUOTE + """
- Si covered=false, "passage" es null y "quote" es "".

Responde solo con JSON: {{"need": "<dato que pide la pregunta>", "covered": true/false, "passage": <número o null>, "quote": "<cita literal>"}}""",
    # v3: v2 with three outcomes.
    "v3": _HEAD + """
Reglas:
""" + _NEED + """- "verdict" es una de estas tres:
  - "sí": algún pasaje contiene ese dato exacto (o el de una de las partes, si hay varias).
  - "parcial": algún pasaje trata directamente lo que se pregunta, pero no da el dato completo o lo da desactualizado (por ejemplo, importes en pesetas cuando se pregunta por la cifra de hoy).
  - "no": ningún pasaje contiene el dato. Un pasaje sobre un tema cercano, o una regla general de la que habría que deducir la respuesta, es "no", no "parcial".
- Con "sí" o "parcial", "passage" es el número del pasaje y "quote" la frase más relevante.
""" + _QUOTE + """
- Con "no", "passage" es null y "quote" es "".

Responde solo con JSON: {{"need": "<dato que pide la pregunta>", "verdict": "sí" | "parcial" | "no", "passage": <número o null>, "quote": "<cita literal>"}}""",
    # v4: three outcomes; the model points to a sentence by number and the code
    # extracts the quote (no copying), plus multi-part, false-premise and outdated rules.
    "v4": """Eres un verificador. Decide si alguno de estos pasajes, extraídos de normas españolas de prevención de riesgos laborales, responde a la pregunta. Cada pasaje está dividido en frases numeradas.

Pregunta: {question}

Pasajes:
{passages}

Reglas:
""" + _NEED + """- "verdict" es una de estas tres:
  - "sí": una frase contiene el dato exacto que pide la pregunta (todas sus partes, si tiene varias). También es "sí" si una frase desmiente la premisa de la pregunta (por ejemplo, la pregunta da por hecho que algo lo hace una persona u organismo y la frase dice que lo hace otro): señala esa frase.
  - "parcial": (a) la pregunta tiene varias partes y alguna frase responde al menos una, pero no todas; o (b) una frase trata directamente lo que se pregunta, pero el dato está incompleto o desactualizado (por ejemplo, importes en pesetas cuando se pregunta por la cifra de hoy).
  - "no": ninguna frase contiene el dato ni desmiente la premisa. Un pasaje sobre un tema cercano, o una regla general de la que habría que deducir la respuesta, es "no", no "parcial".
- Con "sí" o "parcial", "passage" es el número del pasaje y "sentence" el número de la frase que mejor lo demuestra.
- Con "no", "passage" y "sentence" son null.

Responde solo con JSON: {{"need": "<dato que pide la pregunta>", "verdict": "sí" | "parcial" | "no", "passage": <número o null>, "sentence": <número o null>}}""",
}
SENTENCE_VERSIONS = {"v4"}  # the model returns a sentence number, the code extracts the quote
COVERAGE_VERSION = "v4"  # fewest errors on the 39 dev questions, and no false coverage (coverage_eval.py)


def model_unusable(error: str) -> bool:
    """True if the error means this model cannot be used again today (daily quota
    exhausted, no free quota at all, or model not found). Per-minute 429s are not."""
    return any(t in error for t in DAILY_QUOTA)


def next_model(models: list[str], unusable: set[str]) -> str | None:
    return next((m for m in models if m not in unusable), None)


def _api_key() -> str:
    from api_key import resolve_api_key

    key, _ = resolve_api_key()
    if not key:
        raise SystemExit("No Gemini API key found (see SETUP.md).")
    return key


def ask_user_approval(tool_name: str, args: dict) -> bool:
    """Default approval: ask on the terminal; deny when nobody can answer."""
    if not sys.stdin.isatty():
        print(f"[denied] {tool_name}({args}): no terminal to ask for approval", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {tool_name}({args}). Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes", "s", "si", "sí")


def _text(content) -> str:
    """Gemini may return a string or a list of content blocks."""
    if isinstance(content, str):
        return content
    parts = []
    for block in content or []:
        parts.append(block if isinstance(block, str) else block.get("text", ""))
    return "".join(parts)


def _inside_project(path_str: str) -> bool:
    try:
        p = Path(path_str).expanduser().resolve()
        return p == ROOT or ROOT in p.parents
    except Exception:
        return False


def _split_passages(result: str) -> dict[int, str]:
    """The search result as {passage number: text}, from its "[n] source, location" headers."""
    parts = re.split(r"(?m)^\[(\d+)\] ", result)
    return {int(parts[i]): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


_SENTENCE_END = re.compile(r"(?<=[.;:])\s+(?=[\"«(¿¡]?[A-ZÁÉÍÓÚÑ0-9])")


def _sentences(passage: str) -> list[str]:
    """A passage split into sentences: by line, then after . ; : before a capital or a digit.

    The first line (the "source, location (score)" header) is left out."""
    out, carry = [], ""
    for line in passage.splitlines()[1:]:
        for s in _SENTENCE_END.split(line):
            s = (carry + " " + s).strip() if carry else s.strip()
            carry = ""
            if len(s) < 15:  # an enumerator ("1.", "a)") or a bare heading joins the next sentence
                carry = s
            elif s:
                out.append(s)
    if carry:
        out.append(carry)
    return out


def _numbered(passages: dict[int, str]) -> str:
    """The passages for the v4 prompt: header line, then (k) before each sentence."""
    blocks = []
    for n, text in sorted(passages.items()):
        head = text.splitlines()[0] if text else ""
        body = "\n".join(f"  ({k}) {s}" for k, s in enumerate(_sentences(text), start=1))
        blocks.append(f"[{n}] {head}\n{body}")
    return "\n\n".join(blocks)


def _norm(s: str) -> str:
    """Lower case, no whitespace: for a literal comparison that ignores spacing and case."""
    return re.sub(r"\s+", "", s or "").casefold()


def _parse_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"no JSON in coverage reply: {text[:200]!r}")
    return json.loads(m.group(0))


def _level(data: dict) -> str:
    """The model's verdict as "sí", "parcial" or "no" (v1/v2 answer covered: true/false)."""
    if "verdict" in data:
        v = str(data.get("verdict") or "").strip().casefold()
        return {"si": "sí", "sí": "sí", "yes": "sí", "parcial": "parcial", "partial": "parcial"}.get(v, "no")
    return "sí" if data.get("covered") is True else "no"


async def check_coverage(question: str, result: str, key: str, version: str | None = None,
                         models: list[str] | None = None) -> dict:
    """Ask a cheap model whether a passage answers the question and verify its quote.

    Returns {"checked", "level", "covered", "claimed", "need", "passage", "quote",
    "quote_found", "model", "calls", "tokens", "seconds", "error", "quota_exhausted"}.
    level is "sí", "parcial" or "no"; a "sí" or "parcial" whose quote is not in the
    named passage becomes "no". checked=False means there was no check (quota,
    timeout, bad reply): the caller must then not refuse.
    """
    start = time.time()
    version = version or COVERAGE_VERSION
    models = models or COVERAGE_MODELS
    verdict = {"checked": False, "version": version, "level": None, "covered": None, "claimed": None,
               "need": "", "passage": None, "quote": "", "quote_found": None, "model": None,
               "calls": [], "tokens": {"input": 0, "output": 0}, "seconds": 0.0, "error": None,
               "quota_exhausted": False, "sentence": None}
    passages = _split_passages(result)
    if not passages:
        verdict["error"] = "search returned no numbered passages"
        return verdict
    by_sentence = version in SENTENCE_VERSIONS
    prompt = COVERAGE_PROMPTS[version].format(
        question=question,
        passages=_numbered(passages) if by_sentence
        else "\n\n".join(f"[{n}] {text}" for n, text in sorted(passages.items())))
    reply = None
    # Same fallback and retry logic as the agent: next model on daily quota, wait on 503/429.
    while reply is None and (name := next_model(models, _unusable)) is not None:
        verdict["model"] = name
        model = ChatGoogleGenerativeAI(model=name, api_key=key, temperature=0,
                                       timeout=MODEL_TIMEOUT, max_retries=1)
        switch = False
        for attempt in range(len(RETRY_DELAYS) + 1):
            try:
                verdict["calls"].append(name)
                reply = await model.ainvoke(prompt)
                break
            except Exception as e:
                verdict["error"] = f"{type(e).__name__}: {e}"
                if model_unusable(verdict["error"]):
                    _unusable.add(name)
                    print(f"[coverage] {name}: daily quota exhausted or unavailable, switching model",
                          file=sys.stderr)
                    switch = True
                    break
                if attempt < len(RETRY_DELAYS) and any(t in verdict["error"] for t in TRANSIENT):
                    print(f"[coverage] {name} busy, retrying in {RETRY_DELAYS[attempt]}s", file=sys.stderr)
                    await asyncio.sleep(RETRY_DELAYS[attempt])
                    continue
                break
        if not switch:
            break
    verdict["seconds"] = round(time.time() - start, 1)
    if reply is None:
        verdict["quota_exhausted"] = next_model(models, _unusable) is None
        verdict["error"] = verdict["error"] or "all coverage models are out of daily quota"
        return verdict
    usage = getattr(reply, "usage_metadata", None) or {}
    verdict["tokens"] = {"input": usage.get("input_tokens", 0), "output": usage.get("output_tokens", 0)}
    try:
        data = _parse_json(_text(reply.content))
    except Exception as e:
        verdict["error"] = f"unreadable coverage reply: {e}"
        return verdict
    verdict["checked"], verdict["error"] = True, None
    verdict["claimed"] = _level(data)
    verdict["need"] = str(data.get("need") or "")
    verdict["quote"] = str(data.get("quote") or "")
    try:
        verdict["passage"] = int(data.get("passage")) if data.get("passage") is not None else None
    except (TypeError, ValueError):
        verdict["passage"] = None
    verdict["level"] = verdict["claimed"]
    if by_sentence:
        # The quote is taken by the code from the sentence the model points to; the
        # model copies nothing. A missing or out-of-range number means no proof: "no".
        try:
            k = int(data.get("sentence"))
        except (TypeError, ValueError):
            k = None
        verdict["sentence"] = k
        sents = _sentences(passages.get(verdict["passage"], ""))
        verdict["quote"] = sents[k - 1] if k is not None and 1 <= k <= len(sents) else ""
        if verdict["claimed"] != "no":
            verdict["quote_found"] = bool(verdict["quote"])
            if not verdict["quote_found"]:
                verdict["level"] = "no"
    elif verdict["claimed"] != "no":
        # The model may only claim (partial) coverage with a quote that really is in the passage it names.
        q, text = _norm(verdict["quote"]), _norm(passages.get(verdict["passage"], ""))
        verdict["quote_found"] = len(q) >= MIN_QUOTE_CHARS and q in text
        if not verdict["quote_found"]:
            verdict["level"] = "no"
    verdict["covered"] = verdict["level"] == "sí"
    return verdict


def coverage_note(v: dict) -> str:
    """The verdict as the agent reads it, appended to the search result."""
    if not v["checked"]:
        return ""
    if v["level"] == "sí":
        return f"\n\nCOMPROBACIÓN DE COBERTURA: SÍ: pasaje {v['passage']}. Cita: «{v['quote']}»"
    if v["level"] == "parcial":
        return (f"\n\nCOBERTURA PARCIAL (pasaje {v['passage']}, «{v['quote']}»): responde solo lo que "
                "dicen los pasajes y di expresamente qué falta.")
    return ("\n\nCOMPROBACIÓN DE COBERTURA: NO. Ningún pasaje responde la pregunta. "
            "Debes responder 'No consta en los documentos del corpus' y decir qué se buscó.")


def _wrap_tools(mcp_tools, session, trace: list, approve, question: str = "", key: str = "") -> list:
    """Wrap the MCP tools so every call is traced, limited and guarded."""
    calls = {"n": 0}
    wrapped = []
    for t in mcp_tools:
        name = t.name

        async def run(_name=name, **kwargs) -> str:
            entry = {"tool": _name, "args": kwargs, "result": None, "blocked": None}
            trace.append(entry)
            if calls["n"] >= MAX_TOOL_CALLS:
                entry["blocked"] = "call limit"
                entry["result"] = ("Tool call limit reached. Answer now with what you already have, "
                                   "or say the corpus does not cover the question.")
                return entry["result"]
            calls["n"] += 1
            if _name == "add_document" and not _inside_project(str(kwargs.get("path", ""))):
                entry["blocked"] = "path outside project"
                entry["result"] = "Blocked: add_document may only read files inside the project folder."
                return entry["result"]
            if _name in APPROVAL_TOOLS and not approve(_name, kwargs):
                entry["blocked"] = "not approved"
                entry["result"] = "The user did not approve this action. Do not retry it."
                return entry["result"]
            res = await session.call_tool(_name, kwargs)
            entry["result"] = "".join(getattr(c, "text", "") for c in res.content)
            if _name == "search" and question and key:
                try:
                    v = await check_coverage(question, entry["result"], key)
                except Exception as e:  # a failed check must never block the answer
                    v = {"checked": False, "error": f"{type(e).__name__}: {e}"}
                entry["coverage"] = v
                if not v["checked"]:
                    print(f"[coverage] no check for {kwargs.get('query')!r}: {v['error']}", file=sys.stderr)
                return entry["result"] + coverage_note(v)
            return entry["result"]

        wrapped.append(StructuredTool.from_function(
            coroutine=run, name=name, description=t.description or name, args_schema=getattr(t, "input_schema", None) or t.inputSchema))
    return wrapped


async def ask_many(questions: list[str], approve=ask_user_approval) -> list[dict]:
    """Answer several questions with one server process. Returns one dict each."""
    system_prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    key = _api_key()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")],
                                   cwd=str(ROOT), env=dict(os.environ))
    results = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            for question in questions:
                start = time.time()
                answer, error, tokens, trace = "", None, {"input": 0, "output": 0}, []
                used, tried = None, []
                llm_calls: dict[str, int] = {}  # model calls made by the agent, per model
                while (name := next_model(AGENT_MODELS, _unusable)) is not None:
                    used = name
                    tried.append(name)
                    model = ChatGoogleGenerativeAI(model=name, api_key=key, temperature=0,
                                                   timeout=MODEL_TIMEOUT, max_retries=1)
                    switch = False
                    for attempt in range(len(RETRY_DELAYS) + 1):
                        trace = []  # a retry starts from a clean trace and a fresh call counter
                        agent = create_agent(model, _wrap_tools(mcp_tools, session, trace, approve,
                                                                question, key),
                                             system_prompt=system_prompt)
                        try:
                            out = await agent.ainvoke({"messages": [("user", question)]},
                                                      config={"recursion_limit": 25})
                            msgs = out["messages"]
                            llm_calls[name] = llm_calls.get(name, 0) + sum(1 for m in msgs if getattr(m, "type", "") == "ai")
                            answer = _text(msgs[-1].content).strip()
                            usage = [getattr(m, "usage_metadata", None) or {} for m in msgs]
                            tokens = {"input": sum(u.get("input_tokens", 0) for u in usage),
                                      "output": sum(u.get("output_tokens", 0) for u in usage)}
                            error = None
                            break
                        except Exception as e:  # keep going: one failure must not stop an evaluation
                            error = f"{type(e).__name__}: {e}"
                            llm_calls[name] = llm_calls.get(name, 0) + 1  # at least the failed call
                            if model_unusable(error):
                                _unusable.add(name)
                                print(f"{name}: daily quota exhausted or unavailable, switching model",
                                      file=sys.stderr)
                                switch = True
                                break
                            if attempt < len(RETRY_DELAYS) and any(t in error for t in TRANSIENT):
                                print(f"{name} busy, retrying in {RETRY_DELAYS[attempt]}s", file=sys.stderr)
                                await asyncio.sleep(RETRY_DELAYS[attempt])
                                continue
                            break
                    if not switch:
                        break
                if used is None:
                    error = "all models in AGENT_MODELS are out of daily quota"
                # Enforced in code: if every search was checked and every verdict is "no"
                # (not "parcial"), the answer is the fixed refusal, whatever the model wrote.
                checks = [e.get("coverage") for e in trace if e["tool"] == "search" and not e["blocked"]]
                refused = bool(checks) and not error and all(
                    c and c["checked"] and c["level"] == "no" for c in checks)
                if refused:
                    searched = ", ".join(f"«{e['args'].get('query')}»" for e in trace if e["tool"] == "search")
                    answer = f"{REFUSAL}\n\nSe buscó en el corpus: {searched}."
                coverage = {
                    "checks": len(checks),
                    "unchecked": sum(1 for c in checks if not (c and c["checked"])),
                    "forced_refusal": refused,
                    "tokens": {k: sum((c or {}).get("tokens", {}).get(k, 0) for c in checks)
                               for k in ("input", "output")},
                    "seconds": round(sum((c or {}).get("seconds", 0) for c in checks), 1),
                }
                results.append({"question": question, "answer": answer, "trace": trace,
                                "tokens": tokens, "seconds": round(time.time() - start, 1),
                                "model": used, "models_tried": tried, "error": error, "llm_calls": llm_calls,
                                "coverage": coverage})
    return results


def ask(question: str, approve=ask_user_approval) -> dict:
    return asyncio.run(ask_many([question], approve))[0]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    r = ask(" ".join(sys.argv[1:]))
    if r["error"]:
        raise SystemExit(f"Agent failed: {r['error']}")
    print(r["answer"])
    searched = [e["args"].get("query") for e in r["trace"] if e["tool"] == "search"]
    print(f"\n[{r['model']}; {len(r['trace'])} tool call(s); searches: {searched}; "
          f"{r['tokens']['input']}+{r['tokens']['output']} tokens; {r['seconds']} s]")
    for e in r["trace"]:
        v = e.get("coverage")
        if e["tool"] != "search" or v is None:
            continue
        if not v["checked"]:
            print(f"[coverage {e['args'].get('query')!r}: NOT CHECKED ({v['error']})]")
            continue
        print(f"[coverage {v['version']} {e['args'].get('query')!r}: {v['level']} (model said {v['claimed']}, "
              f"quote found={v['quote_found']}); passage={v['passage']}; quote={v['quote']!r}; "
              f"{v['model']}; {v['tokens']['input']}+{v['tokens']['output']} tokens; {v['seconds']} s]")
    c = r["coverage"]
    print(f"[coverage total: {c['checks']} check(s), {c['unchecked']} unchecked; forced refusal: "
          f"{c['forced_refusal']}; extra {c['tokens']['input']}+{c['tokens']['output']} tokens; "
          f"extra {c['seconds']} s]")


if __name__ == "__main__":
    main()