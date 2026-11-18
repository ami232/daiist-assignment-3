"""
Find a Gemini chat model that answers quickly with your key and can call tools.
    uv run python try_models.py
Each model gets one plain question and one question where it should call a tool, 20 s limit each.
"""

import time

from google import genai
from google.genai import types

from api_key import load_api_key

MODELS = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-3.6-flash",
          "gemini-3.7-flash", "gemini-2.5-flash-lite", "gemini-flash-latest", "gemini-3.8-flash"]

client = genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(
    timeout=20000, retry_options=types.HttpRetryOptions(attempts=1)))

search = types.FunctionDeclaration(
    name="search", description="Search the labour-law documents.",
    parameters=types.Schema(type="OBJECT", properties={"query": types.Schema(type="STRING")}, required=["query"]))


def attempt(model: str, contents: str, tools=None) -> tuple[str, float]:
    started = time.time()
    try:
        response = client.models.generate_content(
            model=model, contents=contents,
            config=types.GenerateContentConfig(tools=tools) if tools else None)
        parts = response.candidates[0].content.parts if response.candidates else []
        called = any(getattr(p, "function_call", None) for p in parts or [])
        return ("calls the tool" if called else "answered without the tool" if tools else "ok"), time.time() - started
    except Exception as error:  # noqa: BLE001 - we want to see every failure
        return f"FAILED: {str(error)[:90]}", time.time() - started


for model in MODELS:
    plain, t1 = attempt(model, "Di hola en una palabra")
    tool, t2 = attempt(model, "Busca en los documentos cuántos días de vacaciones hay.", [types.Tool(function_declarations=[search])])
    print(f"{model:<24} plain: {plain} ({t1:.1f}s) | tool: {tool} ({t2:.1f}s)", flush=True)
