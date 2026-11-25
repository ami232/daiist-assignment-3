"""Ingestion checks: extraction, cleaning, ranges and chunking. `uv run pytest`

Uses the BOE files in corpus/ (downloaded on first use). Spends no Gemini quota.
"""

import csv

import pytest

import index as ix


@pytest.fixture(scope="module")
def docs():
    return {meta.source: (source, meta, blocks) for source, meta, blocks in ix.load_corpus()}


def blocks_of(docs, source):
    return docs[source][2]


def find(docs, source, location):
    return next(b for b in blocks_of(docs, source) if b.location == location)


# --- extraction and cleaning ------------------------------------------------ #

def test_editorial_notes_are_stripped(docs):
    for source, (_, _, blocks) in docs.items():
        for b in blocks:
            assert "Ref. BOE-" not in b.text, (source, b.location)
            assert "Téngase en cuenta" not in b.text, (source, b.location)


def test_only_the_current_version_is_kept(docs):
    # Art. 38 ter was rewritten by RDL 13/2022 (in force 2023): the current text talks about
    # a "cuota reducida" for twelve months, and appears once, not once per historical version.
    art = find(docs, "LETA", "Artículo 38 ter")
    assert art.text.startswith("Artículo 38 ter. Reducciones en la cotización")
    assert "cuota reducida" in art.text
    assert art.text.count("Artículo 38 ter.") == 1


def test_headings_give_the_path_without_amendment_notes(docs):
    art = find(docs, "LETA", "Artículo 38 ter")
    assert art.path.startswith("TÍTULO V Fomento y promoción del trabajo autónomo > CAPÍTULO II")
    assert "Se añade" not in art.path


def test_disposiciones_do_not_inherit_the_last_titulo(docs):
    assert find(docs, "LETA", "Disposición adicional primera").path == ""


def test_repealed_stubs_are_dropped(docs):
    locations = {b.location for b in blocks_of(docs, "LETA")}
    assert {"Artículo 31", "Artículo 31 bis", "Artículo 32", "Artículo 32 bis"}.isdisjoint(locations)
    assert "Artículo 38 ter" in locations


def test_odd_block_ids_still_give_readable_locations(docs):
    # The BOE id of "Artículo 38 ter" is "a3-5": locations must come from the block title.
    assert find(docs, "LETA", "Artículo 38 ter").block_id == "a3-5"


def test_tables_are_rendered_as_rows(docs):
    art18 = find(docs, "COT2026", "Artículo 18")
    assert "Tramo 1 | ≥ 1.166,70 y ≤ 1.300 | 950,98 | 1.300,00" in art18.text


# --- ranges ------------------------------------------------------------------ #

def test_block_ranges(docs):
    def locations(source):
        return [b.location for b in blocks_of(docs, source)]

    assert locations("LGSS")[0] == "Artículo 305" and locations("LGSS")[-1] == "Artículo 350"
    assert locations("RGAT")[0] == "Artículo 2" and locations("RGAT")[-1] == "Artículo 29"
    assert find(docs, "RF", "Artículo 1").text.startswith("Artículo 1. Obligación de expedir")  # the Reglamento's
    assert locations("COT2026") == ["Artículo 18", "Artículo 19"]


def test_locations_are_unique_per_source(docs):
    for source, (_, _, blocks) in docs.items():
        locations = [b.location for b in blocks]
        assert len(locations) == len(set(locations)), source


def test_corpus_size(docs):
    words = sum(len(b.text.split()) for s, m, bl in docs.values() if not s.held_out for b in bl)
    assert words >= 50_000
    assert sum(not s.held_out for s, _, _ in docs.values()) >= 3


# --- chunking --------------------------------------------------------------- #

@pytest.mark.parametrize("design", list(ix.DESIGNS))
def test_chunks_have_full_metadata_and_stable_ids(docs, design):
    for source, meta, blocks in docs.values():
        first = ix.chunk_document(meta, blocks, design)
        again = ix.chunk_document(meta, blocks, design)
        assert [c.id for c in first] == [c.id for c in again]
        assert len({c.id for c in first}) == len(first)
        for c in first:
            assert c.source == source.id and c.boe_id == source.boe_id
            assert c.location and c.locations and c.url.startswith("https://www.boe.es/")
            assert c.updated[:2] == "20" and c.n_words == len(c.text.split())
            assert all(isinstance(v, (str, int)) for v in c.metadata().values())


def test_article_chunks_respect_max_words(docs):
    cfg = ix.DESIGNS["article"]
    for _, meta, blocks in docs.values():
        for c in ix.chunk_document(meta, blocks, "article"):
            assert c.n_words <= cfg.max_words + 10, (c.source, c.location, c.n_words)  # "(parte i/n)" slack


def test_article_chunks_cover_every_block_once_per_part(docs):
    _, meta, blocks = docs["LGSS"]
    chunks = ix.chunk_document(meta, blocks, "article")
    assert {c.location for c in chunks} == {b.location for b in blocks}
    long_one = [c for c in chunks if c.location == "Artículo 308"]
    assert len(long_one) > 1 and all("(parte" in c.text.split("\n")[0] for c in long_one)


def test_fixed_windows_overlap_and_cover_the_document(docs):
    cfg = ix.DESIGNS["fixed"]
    _, meta, blocks = docs["RF"]
    chunks = ix.chunk_document(meta, blocks, "fixed")
    total = sum(len(b.text.split()) for b in blocks)
    assert all(c.n_words <= cfg.size for c in chunks)
    step = cfg.size - cfg.overlap
    assert (len(chunks) - 1) * step + chunks[-1].n_words == total


# --- outline ---------------------------------------------------------------- #

def test_outline_lists_every_location(docs, tmp_path):
    path = tmp_path / "outline.csv"
    ix.write_outline(list(docs.values()), path)
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == sum(len(bl) for _, _, bl in docs.values())
    assert {"source": "LETA", "location": "Artículo 38 ter"}.items() <= next(
        r for r in rows if r["location"] == "Artículo 38 ter").items()
