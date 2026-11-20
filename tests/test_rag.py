"""Storage, retrieval, server and harness plumbing, with a fake embedder. `uv run pytest`

Spends no Gemini quota: vectors are hashed bags of words, stored in a temporary Chroma.
"""

import hashlib

import pytest

import index as ix
import rag

DIM = 64


def fake_embed(texts, kind="document", titles=None):
    vectors = []
    for text in texts:
        v = [0.0] * DIM
        for word in rag.tokens(text):
            v[int(hashlib.md5(word.encode()).hexdigest(), 16) % DIM] += 1.0
        vectors.append(v if any(v) else [1.0] + [0.0] * (DIM - 1))
    return vectors


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setattr(ix, "CHROMA_DIR", tmp_path / "chroma")
    monkeypatch.setattr(ix, "_chroma", None)
    monkeypatch.setattr(ix, "embed_texts", fake_embed)
    monkeypatch.setattr(rag, "QUERY_CACHE", tmp_path / "query_cache.sqlite")
    rag._corpora.clear()
    yield
    monkeypatch.setattr(ix, "_chroma", None)


@pytest.fixture(scope="module")
def leta():
    source = next(s for s in ix.SOURCES if s.id == "LETA")
    return ix.load_document(ix.fetch(source))


def article_chunks(leta, n=None):
    meta, blocks = leta
    chunks = ix.chunk_document(meta, blocks, "article")
    return chunks[:n] if n else chunks


# --- embed_and_store -------------------------------------------------------- #

def test_only_missing_chunks_are_embedded(store, leta):
    chunks = article_chunks(leta, 20)
    collection = ix.open_collection("article")
    assert ix.embed_and_store(chunks, collection) == {"added": 20, "skipped": 0, "pending": 0}
    assert ix.embed_and_store(chunks, collection) == {"added": 0, "skipped": 20, "pending": 0}
    assert collection.count() == 20
    stored = collection.get(ids=[chunks[0].id], include=["metadatas", "documents"])
    assert stored["metadatas"][0]["location"] == chunks[0].location
    assert stored["documents"][0] == chunks[0].text


def test_quota_stops_cleanly_and_a_rerun_resumes(store, leta, monkeypatch):
    monkeypatch.setattr(ix, "EMBED_BATCH", 5)
    calls = []

    def first_batch_then_quota(texts, kind="document", titles=None):
        calls.append(len(texts))
        if len(calls) > 1:
            raise ix.QuotaExhausted("429 PerDay")
        return fake_embed(texts)

    chunks = article_chunks(leta, 12)
    collection = ix.open_collection("article")
    result = ix.embed_and_store(chunks, collection, embed=first_batch_then_quota)
    assert result == {"added": 5, "skipped": 0, "pending": 7, "error": "quota"}
    assert collection.count() == 5                   # the first batch was saved before the quota ran out
    assert ix.embed_and_store(chunks, collection) == {"added": 7, "skipped": 5, "pending": 0}


def test_prune_removes_chunks_the_chunking_no_longer_makes(store, leta):
    chunks = article_chunks(leta, 10)
    collection = ix.open_collection("article")
    ix.embed_and_store(chunks, collection)
    assert ix.prune(chunks[:6], collection, {chunks[0].boe_id}) == 4
    assert collection.count() == 6


def test_retry_delay_reads_google_hint_and_spots_daily_quota():
    assert ix._retry_delay(Exception("... 'retryDelay': '37s' ...")) == 37
    assert ix._retry_delay(Exception("Quota exceeded: EmbedContentRequestsPerDay")) is None


# --- duplicate policy (index_file, used by add_document) ------------------- #

COT = ix.CORPUS_DIR / "BOE-A-2026-7296.xml"


def _set_stored_date(collection, boe_id, date):
    stored = collection.get(where={"boe_id": boe_id}, include=["metadatas"])
    collection.update(ids=stored["ids"], metadatas=[{**m, "updated": date} for m in stored["metadatas"]])


def test_duplicate_policy(store):
    first = ix.index_file(COT)
    assert first["status"] == "added" and first["source"] == "COT2026"
    assert first["added"] == first["chunks"] > 0
    collection = ix.open_collection("article")

    assert ix.index_file(COT)["status"] == "already"

    _set_stored_date(collection, first["boe_id"], "2000-01-01")           # stored copy is older
    replaced = ix.index_file(COT)
    assert replaced["status"] == "replaced" and replaced["added"] == first["chunks"]
    assert collection.count() == first["chunks"]

    _set_stored_date(collection, first["boe_id"], "2999-01-01")           # stored copy is newer
    assert ix.index_file(COT)["status"] == "older"
    assert collection.count() == first["chunks"]


# --- retrieval -------------------------------------------------------------- #

def test_dense_and_hybrid_find_the_article(store, leta):
    collection = ix.open_collection("article")
    chunks = article_chunks(leta)
    ix.embed_and_store(chunks, collection)
    target = next(c for c in chunks if c.location == "Artículo 11")

    dense = rag.retrieve(target.text, "B_article", k=3)
    assert dense[0].id == target.id and dense[0].rank == 1
    hybrid = rag.retrieve("trabajador autónomo económicamente dependiente concepto", "C_article_hybrid", k=5)
    assert any(h.covers("LETA", "Artículo 11") for h in hybrid)
    assert [h.rank for h in hybrid] == [1, 2, 3, 4, 5]


def test_source_filter(store, leta):
    ix.embed_and_store(article_chunks(leta, 30), ix.open_collection("article"))
    assert rag.retrieve("cotización", "B_article", k=5, sources=["RF"]) == []
    assert all(h.meta["source"] == "LETA" for h in rag.retrieve("cotización", "C_article_hybrid", sources=["LETA"]))


def test_query_vectors_are_cached(store, monkeypatch):
    calls = []
    monkeypatch.setattr(ix, "embed_texts", lambda texts, kind="document", titles=None: calls.append(1) or fake_embed(texts))
    first = rag.embed_query("¿Qué es la tarifa plana?")
    assert rag.embed_query("¿Qué es la tarifa plana?") == first
    assert len(calls) == 1


def test_format_hits_carries_citation_date_url_and_notice(store, leta):
    ix.embed_and_store(article_chunks(leta, 15), ix.open_collection("article"))
    text = rag.format_hits(rag.retrieve("derechos profesionales", "B_article", k=2))
    assert text.startswith("[1] Cita: [LETA, Artículo")
    assert "texto consolidado a " in text and "https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409#" in text
    assert text.endswith(rag.BOE_NOTICE)


def test_hits_and_citation_parsing():
    hit = rag.Hit("x", "", {"source": "LETA", "location": "Artículo 1", "locations": "Artículo 1; Artículo 2"}, 1.0)
    assert hit.covers("LETA", "Artículo 2") and not hit.covers("LGSS", "Artículo 2")
    assert not hit.covers("LETA", "Artículo 2 bis")
    text = "Sí [LETA, Artículo 38 ter] [LGSS, Artículo 308]. Ver [1] y otra vez [LETA, Artículo 38 ter]."
    assert rag.citations_in(text) == [("LETA", "Artículo 38 ter"), ("LGSS", "Artículo 308")]
    assert rag.spanish_date("2026-09-02") == "2 de septiembre de 2026"


# --- server and harness plumbing ------------------------------------------- #

def test_add_document_rejects_bad_paths_without_raising():
    import server

    assert server.add_document("C:/Windows/win.ini").startswith("Error:")
    assert server.add_document("../outside.xml").startswith("Error:")
    assert server.add_document("corpus/no-such-file.xml").startswith("Error:")
    assert server.add_document("corpus/BOE-A-2026-7296.meta.xml").startswith("Error:")
    assert server.add_document("index/outline.csv").startswith("Error:")
    assert server._resolve("corpus/BOE-A-2026-7296.xml") == COT.resolve()


def test_search_rejects_an_empty_query():
    import server

    assert server.search("   ").startswith("Error:")


def test_sources_are_parsed_from_search_output(store, leta):
    import agent

    ix.embed_and_store(article_chunks(leta, 15), ix.open_collection("article"))
    hits = rag.retrieve("derechos", "B_article", k=3)
    sources = agent.sources_in(rag.format_hits(hits))
    assert list(sources) == list(dict.fromkeys(h.citation for h in hits))   # parts of one article share it
    assert all(url.startswith("https://www.boe.es/") for url in sources.values())


def test_expected_pairs():
    import evaluate

    row = {"id": "q", "expected_source": "LETA;LGSS", "expected_location": "Artículo 1;Artículo 305"}
    assert evaluate.expected_pairs(row) == [("LETA", "Artículo 1"), ("LGSS", "Artículo 305")]
    row = {"id": "q", "expected_source": "RF", "expected_location": "Artículo 6;Artículo 7"}
    assert evaluate.expected_pairs(row) == [("RF", "Artículo 6"), ("RF", "Artículo 7")]
    for q in evaluate.read_questions():                 # every row of the test set parses
        if q["kind"] != "unanswerable":
            assert evaluate.expected_pairs(q)


# --- citation validator (agent.py guardrail 3), with a scripted fake model --- #

def _run_scripted(replies):
    import asyncio

    from langchain.agents import create_agent
    from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
    from langchain_core.messages import AIMessage
    from langchain_core.tools import tool

    import agent

    class Scripted(GenericFakeChatModel):
        def bind_tools(self, tools, **kwargs):
            return self

    @tool
    def search(query: str) -> str:
        """Fake search."""
        return "[1] Cita: [LETA, Artículo 1] · Ley · texto consolidado a 2 de septiembre de 2026\ntexto\nBOE: https://www.boe.es/x#a1"

    usage = {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15}
    script = [AIMessage("", tool_calls=[{"name": "search", "args": {"query": "q"}, "id": "c1"}], usage_metadata=usage)]
    script += [AIMessage(text, usage_metadata=usage) for text in replies]
    fake = create_agent(Scripted(messages=iter(script)), tools=[search], middleware=[agent.validate_citations])
    return asyncio.run(agent.ask(fake, "¿Quién es autónomo?"))


def test_citation_validator_repairs_once():
    result = _run_scripted(["Es autónomo quien... [LETA, Artículo 99]", "Es autónomo quien... [LETA, Artículo 1]"])
    assert result["citation_guardrail"] == "repaired"
    assert result["answer"].endswith("[LETA, Artículo 1]")
    assert result["citations"] == ["[LETA, Artículo 1]"]


def test_citation_validator_refuses_after_second_failure():
    import agent

    result = _run_scripted(["Sin citas.", "Sigue sin citas [LGSS, Artículo 308]."])
    assert result["citation_guardrail"] == "refused"
    assert result["answer"] == agent.REFUSAL


def test_valid_answers_and_refusals_pass_untouched():
    import agent

    assert _run_scripted(["Sí [LETA, Artículo 1]."])["citation_guardrail"] is None
    assert _run_scripted([agent.REFUSAL])["citation_guardrail"] is None
