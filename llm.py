"""LLM helpers shared by agent.py and evaluate.py: Gemini, with Groq as fallback.

Model names starting with "groq:" go to Groq (OpenAI-compatible API, key in
GROQ_API_KEY or .env); everything else goes to Gemini.
"""

from __future__ import annotations

import os
import time

from api_key import ENV_FILE, load_api_key

# Fast model for query translation.
FAST_MODEL = os.environ.get("FAST_MODEL", "gemini-3.5-flash-lite")
# Judge: a stronger Gemini than the agent's flash-lite. gemini-3.5-flash allows
# only 20 requests a day on the free tier; gemini-3-flash-preview has its own quota.
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3-flash-preview")
GEMINI_FALLBACKS = {"gemini-3-flash-preview": ["gemini-3.6-flash"]}  # tried before Groq
GROQ_FALLBACK = os.environ.get("GROQ_FALLBACK_MODEL", "groq:openai/gpt-oss-120b")
GEMINI_FALLBACK = "gemini-3-flash-preview"


def groq_key() -> str | None:
    """GROQ_API_KEY from the environment, else from .env (same rules as api_key.py)."""
    key = (os.environ.get("GROQ_API_KEY") or "").strip()
    if not key and ENV_FILE.is_file():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            name, _, value = line.strip().partition("=")
            if name.strip() == "GROQ_API_KEY":
                key = value.strip().strip('"').strip("'")
    if key:
        os.environ["GROQ_API_KEY"] = key
    return key or None


def _groq(prompt: str, model: str, system: str | None, json_mode: bool) -> tuple[str, dict]:
    from langchain_groq import ChatGroq
    if not groq_key():
        raise RuntimeError("No GROQ_API_KEY for the Groq fallback.")
    kw = {"model_kwargs": {"response_format": {"type": "json_object"}}} if json_mode else {}
    llm = ChatGroq(model=model.removeprefix("groq:"), temperature=0, max_retries=3, **kw)
    msgs = ([("system", system)] if system else []) + [("human", prompt)]
    r = llm.invoke(msgs)
    u = r.usage_metadata or {}
    return (r.content or "").strip(), {"model": model, "input_tokens": u.get("input_tokens", 0),
                                       "output_tokens": u.get("output_tokens", 0)}

_client = None


def client():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=load_api_key())
    return _client


def generate(prompt: str, model: str = FAST_MODEL, system: str | None = None,
             json_mode: bool = False, thinking: str | None = "low") -> tuple[str, dict]:
    """Call the model with retries on 429/503; after repeated failures falls
    back (Gemini -> Groq, Groq -> Gemini). Returns (text, usage)."""
    if model.startswith("groq:"):
        try:
            return _groq(prompt, model, system, json_mode)
        except Exception:  # noqa: BLE001 - Groq down or out of quota: try Gemini
            model = GEMINI_FALLBACK
    from google.genai import types
    cfg = types.GenerateContentConfig(
        system_instruction=system,
        temperature=0,
        response_mime_type="application/json" if json_mode else None,
        thinking_config=types.ThinkingConfig(thinking_level=thinking) if thinking and "lite" not in model else None,
    )
    last = None
    chain = [model] + GEMINI_FALLBACKS.get(model, [])
    for attempt in range(4 * len(chain)):
        m = chain[min(attempt // 4, len(chain) - 1)]
        try:
            r = client().models.generate_content(model=m, contents=prompt, config=cfg)
            u = r.usage_metadata
            return (r.text or "").strip(), {
                "model": m,
                "input_tokens": u.prompt_token_count or 0,
                "output_tokens": (u.candidates_token_count or 0) + (u.thoughts_token_count or 0),
            }
        except Exception as e:  # noqa: BLE001
            last = e
            msg = str(e)
            if "per day" in msg.lower() or "PerDay" in msg:
                if m == chain[-1]:
                    break  # daily quota on the last Gemini model: go to Groq
                continue
            if any(code in msg for code in ("429", "503", "500", "UNAVAILABLE", "RESOURCE_EXHAUSTED")):
                time.sleep(min(30, 5 * (attempt + 1)))
                continue
            raise
    if groq_key():
        return _groq(prompt, GROQ_FALLBACK, system, json_mode)
    raise RuntimeError(f"Gemini failed after retries: {last}")


TRANSLATE_PROMPT = """Rewrite this question from a driver as a short search query in Spanish,
using the legal vocabulary of Spanish traffic law (Ley de Tráfico, Reglamento General de
Circulación, Reglamento General de Conductores). Output only the query, one line.

Question: {q}"""


def to_spanish_query(question: str) -> tuple[str, dict]:
    return generate(TRANSLATE_PROMPT.format(q=question), model=FAST_MODEL, thinking=None)
