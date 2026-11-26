"""Shared, resumable retrieval and ingestion; no network calls at import time."""

from __future__ import annotations

import json
import re
import time
from collections.abc import Callable
from pathlib import Path

from api_key import load_api_key
from ingestion import VectorStore, digest

ROOT = Path(__file__).resolve().parent


def read_config(root: Path = ROOT, *, approved: bool = True) -> dict:
    path = root / "corpus_config.json"
    if not path.exists():
        raise ValueError(
            "Choose your corpus and designs in corpus_config.json (see the example)."
        )
    config = json.loads(path.read_text())
    if approved and not (
        config.get("student_approved") is True
        or config.get("execution_authorized") is True
    ):
        raise ValueError(
            "Corpus/design decisions need Jimena’s approval in corpus_config.json."
        )
    return config


def read_policy(root: Path = ROOT) -> dict:
    path = root / "policy_config.json"
    if not path.exists():
        raise ValueError(
            "Complete policy_config.json using the example and your own decisions."
        )
    policy = json.loads(path.read_text())
    if not (
        policy.get("student_approved") is True
        or policy.get("execution_authorized") is True
    ):
        raise ValueError(
            "Refusal, guardrail and judge policies need Jimena’s review first."
        )
    if not policy.get("agent_model") or not policy.get("judge_model"):
        raise ValueError("Set agent_model and judge_model explicitly.")
    if not 1 <= policy.get("max_model_calls", 0) <= 12:
        raise ValueError("max_model_calls must be between 1 and 12.")
    if policy.get("extra_guardrail") != "citation_allowlist":
        raise ValueError(
            "Implemented extra_guardrail: citation_allowlist. Review before selecting it."
        )
    if not policy.get("refusal_text") or not policy.get("judge_rubric"):
        raise ValueError("Supply your refusal text and judge rubric.")
    return policy


def missing_named_sources(question: str, config: dict) -> list[str]:
    """Refuse a named, registered publication that is absent from the active corpus.

    This is a source-identity check, not general semantic entailment detection.
    Unknown publication names still require the model/judge to identify the gap.
    """
    active = {document["source"] for document in config["documents"]}
    requested = set()
    for document in config.get("documents", []) + config.get(
        "additional_documents", []
    ):
        if any(
            re.search(
                r"(?<!\w)" + re.escape(alias) + r"(?!\w)", question, re.IGNORECASE
            )
            for alias in document.get("aliases", [])
        ):
            requested.add(document["source"])
    return sorted(requested - active)


def selected_design(config: dict) -> dict:
    name = config.get("selected_design")
    for design in config["designs"]:
        if design["name"] == name:
            return design
    raise ValueError("Set selected_design to one of your configured designs.")


def vector_model(config: dict) -> str:
    """Dimension is part of the cache namespace, preventing silent vector reuse."""
    return f"{config['embedding_model']}|dimensions={config.get('embedding_dimensions', 'default')}|retrieval-format=v2"


def embedder(config: dict, task: str) -> Callable[[str], list[float]]:
    from google import genai
    from google.genai import types

    client = None
    last_request = 0.0

    def embed(text: str) -> list[float]:
        nonlocal client, last_request
        if client is None:
            client = genai.Client(api_key=load_api_key())
        options = {}
        content = text
        if config["embedding_model"].removeprefix("models/") == "gemini-embedding-2":
            content = (
                f"task: search result | query: {text}"
                if task == "RETRIEVAL_QUERY"
                else f"title: none | text: {text}"
            )
        else:
            options["task_type"] = task
        if config.get("embedding_dimensions"):
            options["output_dimensionality"] = config["embedding_dimensions"]
        from google.genai.errors import APIError

        for attempt in range(4):
            delay = config.get("embedding_min_interval_seconds", 0.75) - (
                time.monotonic() - last_request
            )
            if delay > 0:
                time.sleep(delay)
            last_request = time.monotonic()
            try:
                response = client.models.embed_content(
                    model=config["embedding_model"],
                    contents=content,
                    config=types.EmbedContentConfig(**options),
                )
                break
            except APIError as error:
                message = str(error).lower()
                minute_limit = "per minute" in message or "perminute" in message
                if error.code != 429 or not minute_limit or attempt == 3:
                    raise
                time.sleep(2 ** (attempt + 1))
        if not response.embeddings or not response.embeddings[0].values:
            raise RuntimeError(
                "Gemini returned no embedding; no index changes were activated."
            )
        return response.embeddings[0].values

    return embed


class Retriever:
    def __init__(self, root: Path = ROOT, query_embed=None):
        self.root = root
        self.config = read_config(root)
        database = root / "index" / "vectors.sqlite3"
        if not database.exists():
            raise ValueError("No saved index. Run main.py index first.")
        self.store = VectorStore(database)
        self.query_embed = query_embed
        self.model = vector_model(self.config)
        self.store.db.execute(
            "CREATE TABLE IF NOT EXISTS queries (id TEXT PRIMARY KEY, vector TEXT NOT NULL)"
        )
        self.store.db.commit()

    def close(self):
        self.store.db.close()

    def query_vector(self, query: str) -> list[float]:
        key = digest(self.model + "\0RETRIEVAL_QUERY\0" + query)
        row = self.store.db.execute(
            "SELECT vector FROM queries WHERE id=?", (key,)
        ).fetchone()
        if row:
            return json.loads(row[0])
        if self.query_embed is None:
            self.query_embed = embedder(self.config, "RETRIEVAL_QUERY")
        vector = self.query_embed(query)
        # Validate using the same numeric constraints as stored document vectors.
        import math

        if not vector or not all(math.isfinite(v) for v in vector) or not any(vector):
            raise ValueError("Invalid query embedding")
        with self.store.db:
            self.store.db.execute(
                "INSERT OR IGNORE INTO queries VALUES (?, ?)", (key, json.dumps(vector))
            )
        return vector

    def search(self, query: str, design: str | None = None, k: int = 5) -> dict:
        query = query.strip()
        if not query or len(query) > 8000:
            raise ValueError("Query must contain 1–8000 characters.")
        if not 1 <= k <= 10:
            raise ValueError("k must be between 1 and 10")
        chosen = design or selected_design(self.config)["name"]
        if chosen not in {d["name"] for d in self.config["designs"]}:
            raise ValueError("Unknown retrieval design")
        count = self.store.db.execute(
            "SELECT count(*) FROM chunks WHERE design=?", (chosen,)
        ).fetchone()[0]
        if not count:
            raise ValueError(
                f"Design {chosen!r} has no saved chunks. Run main.py index."
            )
        items = self.store.search(chosen, self.model, self.query_vector(query), k)
        for item in items:
            item["citation"] = f"[chunk:{item['id']}]"
        return {
            "query": query,
            "design": chosen,
            "chunks": items,
            "context_words": sum(len(c["text"].split()) for c in items),
        }


def add_document(path: str, root: Path = ROOT, document_embed=None) -> dict:
    """Only explicitly registered, provenance-reviewed corpus files can be added."""
    config = read_config(root)
    requested = Path(path)
    resolved = (
        (root / requested).resolve()
        if not requested.is_absolute()
        else requested.resolve()
    )
    if not resolved.is_relative_to((root / "corpus").resolve()):
        raise ValueError(
            "Only files under corpus/ may be indexed; arbitrary local files are blocked."
        )
    from index import prepare, validate_document, write_json

    registered = config.get("documents", []) + config.get("additional_documents", [])
    document = next(
        (d for d in registered if (root / d["path"]).resolve() == resolved), None
    )
    if document is None:
        raise ValueError(
            "Register this file with its source, URL, licence and privacy review in additional_documents first."
        )
    validate_document(document, root)
    if not (root / "index" / "manifest.json").exists():
        raise ValueError("Build the initial index before using add_document.")
    proposed = dict(config)
    proposed["documents"] = [
        d for d in config["documents"] if d["source"] != document["source"]
    ] + [document]
    proposed["additional_documents"] = [
        d
        for d in config.get("additional_documents", [])
        if d["source"] != document["source"]
    ]
    total, designs = prepare(proposed, root)
    store = VectorStore(root / "index" / "vectors.sqlite3")
    try:
        calls = store.add_many(
            designs,
            vector_model(config),
            document_embed or embedder(config, "RETRIEVAL_DOCUMENT"),
        )
    finally:
        store.db.close()
    summary = {
        "words": total,
        "chunks": {name: len(items) for name, items in designs.items()},
        "new_embedding_calls": calls,
    }
    write_json(root / "corpus_config.json", proposed)
    write_json(
        root / "index" / "manifest.json", {"config": proposed, "summary": summary}
    )
    return {
        "source": document["source"],
        "status": "indexed" if calls else "already_indexed_or_cached",
        **summary,
    }


CITATION_PATTERN = re.compile(r"\[chunk:([0-9a-f]{64})\]")


def normalize_citations(answer: str) -> str:
    """Canonicalise bracket syntax only; never repair or invent an ID."""

    def replace(match):
        body = match.group(1).strip()
        if not (
            re.match(r"^(?:chunk|cite|citation|source):", body, re.IGNORECASE)
            or re.match(r"^[0-9a-f]{32,}", body)
        ):
            return match.group(0)
        ids = [
            re.sub(
                r"^(?:chunk|cite|citation|source):\s*",
                "",
                part.strip(),
                flags=re.IGNORECASE,
            )
            for part in body.split(",")
        ]
        if not ids or not all(re.fullmatch(r"[0-9a-f]{64}", value) for value in ids):
            return match.group(0)
        return "".join(f"[chunk:{value}]" for value in ids)

    return re.sub(r"\[([^\]]*)\]", replace, answer)


def citation_check(answer: str, retrieved: list[dict]) -> dict:
    canonical = normalize_citations(answer)
    ids = CITATION_PATTERN.findall(canonical)
    allowed = {c["id"] for c in retrieved}
    invalid = sorted(set(ids) - allowed)
    markers = re.findall(r"\[([^\]]*)\]", canonical)
    malformed = [
        f"[{body}]"
        for body in markers
        if (
            re.match(r"^(?:chunk|cite|citation|source):", body, re.IGNORECASE)
            or re.match(r"^[0-9a-f]{32,}", body)
        )
        and not CITATION_PATTERN.fullmatch(f"[{body}]")
    ]
    return {
        "cited_ids": sorted(set(ids)),
        "invalid_ids": invalid,
        "malformed": malformed,
        "valid": bool(ids) and not invalid and not malformed,
    }
