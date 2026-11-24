"""The add_document MCP tool in server.py, on a temporary index with fake embeddings. Offline."""

import random

import pytest
from mcp.server.mcpserver.exceptions import ToolError

import index
import server


@pytest.fixture
def tmp_index(tmp_path, monkeypatch):
    monkeypatch.setattr(index, "INDEX_DIR", tmp_path / "index")
    monkeypatch.setattr(index, "embed",
                        lambda texts, task="RETRIEVAL_DOCUMENT": [[random.random() for _ in range(8)] for _ in texts])
    return tmp_path


def chunk_ids(source: str) -> set[str]:
    return set(index.collection(index.CHOSEN_DESIGN).get(where={"source": source})["ids"])


def test_a_missing_file_is_an_error(tmp_index):
    assert server.add_document(str(tmp_index / "nope.pdf")).startswith("Error: no file")


def test_an_unsupported_file_type_is_an_error(tmp_index):
    f = tmp_index / "notes.docx"
    f.write_bytes(b"x")
    assert server.add_document(str(f)).startswith("Error: unsupported file type")


def test_same_content_is_a_no_op_and_changed_content_replaces_the_chunks(tmp_index):
    f = tmp_index / "rules.txt"
    f.write_text("First rule about drones.\n\nSecond rule about pilots and remote identification.", encoding="utf-8")

    assert server.add_document(str(f)).startswith("Added 'rules.txt': 2 chunks")
    before = chunk_ids("rules.txt")
    assert len(before) == 2

    assert server.add_document(str(f)).endswith("Nothing changed.")
    assert chunk_ids("rules.txt") == before

    f.write_text("A new rule about night flights.", encoding="utf-8")
    assert server.add_document(str(f)).startswith("Replaced 'rules.txt': 1 chunks")
    after = chunk_ids("rules.txt")
    assert len(after) == 1 and not after & before


def test_search_failures_are_tool_errors_with_a_reason(monkeypatch):
    def no_key(query):
        raise RuntimeError("No GEMINI_API_KEY found.")

    monkeypatch.setattr(index, "retrieve", no_key)
    with pytest.raises(ToolError, match="Put the key in .env"):
        server.search("max height")

    def offline(query):
        raise ConnectionError("network unreachable")

    monkeypatch.setattr(index, "retrieve", offline)
    with pytest.raises(ToolError, match="ConnectionError: network unreachable"):
        server.search("max height")
