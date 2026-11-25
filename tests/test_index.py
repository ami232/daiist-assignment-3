"""Tests for the ingestion pipeline in index.py (offline: fake embedder, real ChromaDB)."""

import pytest

import index
from conftest import CountingEmbedder, make_chunk

BOE_PAGE_END = "último párrafo.\nBOLETÍN OFICIAL DEL ESTADO\nLEGISLACIÓN CONSOLIDADA\nPágina 4"


# --- cleaning -----------------------------------------------------------------

def test_clean_joins_words_hyphenated_across_lines():
    assert index.clean("el arren-\ndatario paga") == "el arrendatario paga"


def test_clean_collapses_spaces_within_a_line():
    assert index.clean("a   b\t c") == "a b c"


def test_clean_removes_the_boe_page_footer():
    assert index.clean(BOE_PAGE_END) == "último párrafo."


def test_clean_removes_the_boe_disclaimer():
    text = "Madrid, 24 de noviembre de 1994.\nEste documento es de carácter informativo y no tiene valor jurídico."
    assert index.clean(text) == "Madrid, 24 de noviembre de 1994."


def test_index_pages_are_recognised_by_their_dot_leaders():
    assert index.is_index_page("Artículo 1. Ámbito de aplicación. ............................ 10")
    assert not index.is_index_page("Artículo 36. Fianza.\n1. A la celebración del contrato...")


# --- labelling every word with its page and article --------------------------------

UNITS = [
    {"text": "Ley de prueba.\nArtículo 1. Objeto.\nEsta ley regula", "location": "p. 5"},
    {"text": "los alquileres.\nArtículo 2. Fianza.\nUna mensualidad.", "location": "p. 6"},
]


def test_label_words_tracks_page_and_article():
    labelled = index.label_words(UNITS)
    assert labelled[0] == ("Ley", "p. 5", None)  # before the first article
    assert ("alquileres.", "p. 6", "Artículo 1") in labelled  # article 1 continues on p. 6
    assert labelled[-1] == ("mensualidad.", "p. 6", "Artículo 2")


def test_label_words_recognises_articles_numbered_in_words_and_bis():
    units = [{"text": "Artículo noveno.\nTexto.\nArtículo 9 bis. Otro.\nTexto.", "location": "p. 1"}]
    assert {a for _, _, a in index.label_words(units)} == {"Artículo noveno", "Artículo 9 bis"}


def test_label_words_recognises_disposiciones():
    units = [{"text": "Disposición transitoria primera. Contratos.\nTexto.", "location": "p. 1"}]
    assert {a for _, _, a in index.label_words(units)} == {"Disposición transitoria primera"}


def test_a_line_that_cites_an_article_is_not_a_heading():
    units = [{"text": "Artículo 1. Objeto.\nArtículo 36 de esta ley se aplica.", "location": "p. 1"}]
    assert {a for _, _, a in index.label_words(units)} == {"Artículo 1"}


# --- fixed-size chunking --------------------------------------------------------

def labelled(n: int, page: str = "p. 1", article: str | None = "Artículo 1") -> list[tuple]:
    return [(f"w{i}", page, article) for i in range(n)]


def test_chunk_fixed_slides_a_window_with_overlap():
    chunks = index.chunk_fixed(labelled(450), source="LAU", size=200, overlap=50)
    assert [len(c["text"].split()) for c in chunks] == [200, 200, 150]
    assert chunks[1]["text"].split()[0] == "w150"  # starts `size - overlap` words later
    assert chunks[-1]["text"].split()[-1] == "w449"  # nothing at the end is lost


def test_chunk_fixed_crosses_pages_and_is_located_where_it_starts():
    words = labelled(150, "p. 5", "Artículo 1") + labelled(150, "p. 6", "Artículo 2")
    first = index.chunk_fixed(words, source="LAU", size=200, overlap=50)[0]
    assert first["location"] == "Artículo 1, p. 5"
    assert first["articles"] == "Artículo 1 | Artículo 2"


def test_chunk_before_any_article_is_located_by_page_only():
    chunk = index.chunk_fixed(labelled(10, "p. 3", None), source="LAU", size=200, overlap=50)[0]
    assert chunk["location"] == "p. 3"


def test_chunk_ids_are_unique_and_stable():
    first = index.chunk_fixed(labelled(450), source="LAU", size=200, overlap=50)
    again = index.chunk_fixed(labelled(450), source="LAU", size=200, overlap=50)
    assert len({c["id"] for c in first}) == len(first)
    assert [c["id"] for c in first] == [c["id"] for c in again]


# --- one chunk per article -----------------------------------------------------------

def test_chunk_by_article_makes_one_chunk_per_article():
    chunks = index.chunk_by_article(index.label_words(UNITS), source="LAU", max_words=500)
    assert [c["location"] for c in chunks] == ["p. 5", "Artículo 1, p. 5", "Artículo 2, p. 6"]
    assert chunks[1]["text"] == "Artículo 1. Objeto. Esta ley regula los alquileres."


def test_chunk_by_article_splits_long_articles():
    chunks = index.chunk_by_article(labelled(250, "p. 5", "Artículo 9"), source="LAU", max_words=100)
    assert [len(c["text"].split()) for c in chunks] == [100, 100, 50]
    assert {c["location"] for c in chunks} == {"Artículo 9, p. 5"}


# --- vector cache -----------------------------------------------------------------

def test_vector_cache_persists_between_instances(tmp_path):
    db = tmp_path / "vectors.sqlite"
    index.VectorCache(db).put_many([("k1", [0.5, 0.25])])
    assert index.VectorCache(db).get(["k1", "missing"]) == {"k1": [0.5, 0.25]}


def test_embed_texts_only_embeds_texts_without_a_saved_vector(tmp_path):
    cache = index.VectorCache(tmp_path / "v.sqlite")
    embed = CountingEmbedder()
    index.embed_texts(["a", "b"], index.DOC_TASK, embed_fn=embed, cache=cache)
    vectors = index.embed_texts(["a", "b", "c"], index.DOC_TASK, embed_fn=embed, cache=cache)
    assert embed.calls == [["a", "b"], ["c"]]
    assert len(vectors) == 3


def test_embed_texts_keeps_finished_batches_when_a_later_batch_fails(tmp_path):
    cache = index.VectorCache(tmp_path / "v.sqlite")
    embed = CountingEmbedder(fail_on_call=2)
    with pytest.raises(RuntimeError):
        index.embed_texts(["a", "b", "c", "d"], index.DOC_TASK, embed_fn=embed, cache=cache, batch_size=2)
    keys = [index.cache_key(t, index.DOC_TASK) for t in "abcd"]
    assert sorted(cache.get(keys)) == sorted(keys[:2])


def test_embed_texts_refuses_a_batch_with_the_wrong_number_of_vectors(tmp_path):
    """gemini-embedding-2 once merged a list of strings into ONE vector; never cache that."""
    cache = index.VectorCache(tmp_path / "v.sqlite")
    one_vector_per_batch = lambda texts, task: [[1.0, 0.0]]  # noqa: E731
    with pytest.raises(ValueError, match="2 texts"):
        index.embed_texts(["a", "b"], index.DOC_TASK, embed_fn=one_vector_per_batch, cache=cache)
    assert cache.get([index.cache_key(t, index.DOC_TASK) for t in "ab"]) == {}


# --- storing in ChromaDB ------------------------------------------------------------

def three_chunks() -> list[dict]:
    return [make_chunk("LAU", f"Artículo {i}, p. 1", f"texto del artículo {i} " * 5) for i in range(3)]


def test_embed_and_store_adds_chunks_with_metadata(tmp_path, embedder):
    collection = index.open_collection("fixed", path=tmp_path / "chroma")
    added = index.embed_and_store(three_chunks(), collection, embed_fn=embedder, cache=index.VectorCache(tmp_path / "v.sqlite"))
    stored = collection.get(include=["metadatas"])
    assert added == 3
    assert {m["source"] for m in stored["metadatas"]} == {"LAU"}
    assert sorted(m["location"] for m in stored["metadatas"]) == ["Artículo 0, p. 1", "Artículo 1, p. 1", "Artículo 2, p. 1"]


def test_embed_and_store_skips_chunks_already_in_the_collection(tmp_path, embedder):
    collection = index.open_collection("fixed", path=tmp_path / "chroma")
    cache = index.VectorCache(tmp_path / "v.sqlite")
    index.embed_and_store(three_chunks(), collection, embed_fn=embedder, cache=cache)
    assert index.embed_and_store(three_chunks(), collection, embed_fn=embedder, cache=cache) == 0
    assert collection.count() == 3


# --- add_document's pipeline ------------------------------------------------------------

def test_index_file_skips_a_document_that_is_already_indexed(tmp_path, embedder):
    doc = tmp_path / "notas.txt"
    doc.write_text("Artículo 1. Objeto.\nAlgo sobre alquileres. " * 40)
    kw = dict(path_index=tmp_path / "idx", embed_fn=embedder)
    first = index.index_file(doc, **kw)
    second = index.index_file(doc, **kw)
    assert first["status"] == "added" and first["chunks"] > 0
    assert second["status"] == "already indexed" and second["chunks"] == 0


def test_index_file_replaces_the_old_chunks_of_a_changed_document(tmp_path, embedder):
    doc = tmp_path / "notas.txt"
    doc.write_text("Texto antiguo. " * 40)
    kw = dict(path_index=tmp_path / "idx", embed_fn=embedder)
    index.index_file(doc, **kw)
    doc.write_text("Texto nuevo que sustituye al antiguo. " * 40)
    result = index.index_file(doc, **kw)
    collection = index.open_collection(index.CHOSEN_DESIGN, path=tmp_path / "idx" / "chroma")
    texts = collection.get(where={"source": "notas"})["documents"]
    assert result["status"] == "updated"
    assert all("Texto nuevo" in t for t in texts)
