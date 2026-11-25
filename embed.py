"""Gemini embeddings with retry, normalisation and a query cache (saves the daily quota)."""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import threading
import time

from config import EMBED_DIM, EMBED_MODEL, INDEX_DIR, get_key


_qlock = threading.Lock()


class QuotaExhausted(RuntimeError):
    pass


_client = None


def _gemini():
    global _client
    if _client is None:
        from google import genai
        key = get_key()
        if not key:
            raise RuntimeError("No API key: see SETUP.md")
        _client = genai.Client(api_key=key)
    return _client


def _norm(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


_mode: str | None = None      # "batch": one embedding per Content in a list; "single": one call per text


def _call(contents, opts: dict) -> list[list[float]]:
    """One API call with retries. Drops options the model rejects (mutates opts)."""
    from google.genai import types
    for attempt in range(1, 6):
        try:
            r = _gemini().models.embed_content(model=EMBED_MODEL, contents=contents,
                                               config=types.EmbedContentConfig(**opts))
            return [_norm(list(e.values)) for e in r.embeddings]
        except Exception as e:                      # noqa: BLE001
            msg = str(e)
            flat = msg.lower().replace("_", "")
            bad = [o for o in list(opts) if o.replace("_", "") in flat]
            if "INVALID_ARGUMENT" in msg and bad:   # model does not accept this option: drop it
                for o in bad:
                    opts.pop(o, None)
                print(f"embed: dropped unsupported option(s) {bad}", file=sys.stderr)
                continue
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                if attempt == 5 or "per day" in flat:
                    raise QuotaExhausted("Embedding quota used up. Saved vectors are kept; re-run later.") from e
                time.sleep(15 * attempt)
            elif attempt == 5:
                raise
            else:
                time.sleep(2 * attempt)
    raise RuntimeError("unreachable")


def embed(texts: list[str], task: str = "RETRIEVAL_DOCUMENT", batch: int = 50) -> list[list[float]]:
    """One vector per text. gemini-embedding-2 merges a plain list of strings into ONE embedding, so the
    first multi-text call probes with 2 Content objects to find out whether the model returns one vector
    per Content; if not, we fall back to one call per text."""
    global _mode
    from google.genai import types
    opts = {"task_type": task, "output_dimensionality": EMBED_DIM}
    wrap = lambda ts: [types.Content(parts=[types.Part(text=t)]) for t in ts]       # noqa: E731
    out: list[list[float]] = []
    i = 0
    while i < len(texts):
        part = texts[i:i + batch]
        if _mode is None and len(part) >= 2:
            probe = _call(wrap(part[:2]), opts)
            _mode = "batch" if len(probe) == 2 else "single"
            print(f"embed: mode = {_mode}", file=sys.stderr)
            if _mode == "batch":
                out += probe
                i += 2
                continue
        if _mode == "batch":
            vecs = _call(wrap(part), opts)
            if len(vecs) != len(part):
                raise RuntimeError(f"expected {len(part)} embeddings, got {len(vecs)}")
        else:
            vecs = []
            for t in part:
                v = _call([t], opts)
                if len(v) != 1:
                    raise RuntimeError(f"expected 1 embedding, got {len(v)}")
                vecs += v
        out += vecs
        i += len(part)
    return out


def embed_query(q: str) -> list[float]:
    """Cached on disk so repeated evaluation runs do not spend quota."""
    path = INDEX_DIR / "query_cache.json"
    key = hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{q}".encode()).hexdigest()[:24]
    with _qlock:                                    # parallel searches must not corrupt the cache file
        cache = json.loads(path.read_text()) if path.exists() else {}
        if key not in cache:
            cache[key] = embed([q], "RETRIEVAL_QUERY")[0]
            INDEX_DIR.mkdir(exist_ok=True)
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(cache))
            tmp.replace(path)
        return cache[key]