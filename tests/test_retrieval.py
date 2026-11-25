"""Tests for retrieval.py: vector search over a real ChromaDB with the fake embedder."""

import index
import retrieval
from conftest import fake_embed, make_chunk

CHUNKS = [
    make_chunk("LAU", "Artículo 36, p. 25", "La fianza en metálico equivale a una mensualidad de renta."),
    make_chunk("LAU", "Artículo 9, p. 12", "La duración del arrendamiento será libremente pactada por las partes."),
    make_chunk("LPH", "Artículo séptimo, p. 7", "El propietario no podrá realizar actividades molestas o insalubres."),
]


def store(tmp_path, chunks=CHUNKS):
    collection = index.open_collection("fixed", path=tmp_path / "chroma")
    index.embed_and_store(chunks, collection, embed_fn=fake_embed, cache=index.VectorCache(tmp_path / "vectors.sqlite"))


def test_search_returns_the_closest_chunk_with_its_citation(tmp_path):
    store(tmp_path)
    top = retrieval.search("cuánta fianza en metálico", design="fixed", k=1, path_index=tmp_path, embed_fn=fake_embed)[0]
    assert (top["source"], top["location"]) == ("LAU", "Artículo 36, p. 25")
    assert "mensualidad" in top["text"]


def test_search_returns_k_chunks_closest_first(tmp_path):
    store(tmp_path)
    hits = retrieval.search("actividades molestas del propietario", design="fixed", k=3, path_index=tmp_path, embed_fn=fake_embed)
    assert len(hits) == 3 and hits[0]["source"] == "LPH"
    assert hits[0]["distance"] <= hits[1]["distance"] <= hits[2]["distance"]


def test_search_on_an_empty_index_returns_nothing(tmp_path):
    assert retrieval.search("fianza", design="fixed", path_index=tmp_path, embed_fn=fake_embed) == []


def test_format_hits_puts_a_citation_on_every_chunk():
    text = retrieval.format_hits(CHUNKS[:2])
    assert "[LAU, Artículo 36, p. 25]" in text and "[LAU, Artículo 9, p. 12]" in text
    assert "una mensualidad de renta" in text


def test_format_hits_says_when_nothing_was_found():
    assert "No passages found" in retrieval.format_hits([])
