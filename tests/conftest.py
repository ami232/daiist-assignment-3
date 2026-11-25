"""Shared test helpers. No test here calls the Gemini API or spends quota."""

import hashlib
import math
import re

import pytest

DIM = 64


def fake_embed(texts: list[str], task: str) -> list[list[float]]:
    """Deterministic bag-of-words embedding: each word adds 1 to a hashed slot.

    Texts that share words end up close in cosine distance, which is all the
    retrieval tests need. `task` is ignored, as it does not change meaning here.
    """
    vectors = []
    for text in texts:
        v = [0.0] * DIM
        for word in re.findall(r"\w+", text.lower()):
            slot = int(hashlib.md5(word.encode()).hexdigest(), 16) % DIM
            v[slot] += 1.0
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        vectors.append([x / norm for x in v])
    return vectors


class CountingEmbedder:
    """fake_embed that records which texts it was asked to embed."""

    def __init__(self, fail_on_call: int | None = None):
        self.calls: list[list[str]] = []
        self.fail_on_call = fail_on_call

    def __call__(self, texts: list[str], task: str) -> list[list[float]]:
        self.calls.append(list(texts))
        if self.fail_on_call is not None and len(self.calls) == self.fail_on_call:
            raise RuntimeError("simulated quota error")
        return fake_embed(texts, task)


def make_chunk(source: str, location: str, text: str) -> dict:
    """A chunk as index.py stores it, built by hand for tests."""
    digest = hashlib.sha1(f"{source}|{location}|{text}".encode()).hexdigest()[:12]
    return {"id": f"{source}-{digest}", "source": source, "location": location, "articles": location, "text": text}


@pytest.fixture
def embedder():
    return CountingEmbedder()
