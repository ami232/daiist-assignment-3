"""Ingestion and retrieval helpers in index.py. Offline: no API calls, no network."""

import httpx

import index


def words(n: int, prefix: str) -> str:
    return " ".join(f"{prefix}{i}" for i in range(n))


def test_loc_match_is_a_prefix_match_at_a_word_boundary():
    assert index.loc_match("PART 1", "PART 1 Requirements for a class C0 Unmanned aircraft system")
    assert not index.loc_match("PART 1", "PART 12 Requirements for a class C6")
    assert index.loc_match("uas.open.020", "UAS.OPEN.020 UAS operations in subcategory A1")
    assert index.loc_match("Article 14", "Article 14")
    assert not index.loc_match("Article 14(5)", "Article 14")


def test_chunk_sections_overlap_20_percent_and_never_cross_sections():
    sections = [{"location": "A", "text": words(400, "a")}, {"location": "B", "text": words(50, "b")}]
    chunks = index.chunk_sections(sections, 150)
    a = [c["text"].split() for c in chunks if c["location"] == "A"]
    b = [c["text"].split() for c in chunks if c["location"] == "B"]
    assert [c[0] for c in a] == ["a0", "a120", "a240", "a360"]  # a new window every 120 words
    assert all(len(c) <= 150 for c in a + b)
    assert a[0][-30:] == a[1][:30]                               # 30 words (20%) shared
    assert a[-1][-1] == "a399"                                   # the end of the section is covered
    assert all(w.startswith("a") for c in a for w in c)          # no words from section B
    assert b == [words(50, "b").split()]                         # a short section is one chunk


def test_html_sections_glue_list_labels_and_split_on_legal_headings(tmp_path):
    html = """<html><body>
      <p class="modref">&#9660;M1</p>
      <p>Article 4</p><p>Open category of UAS operations</p>
      <p>(a)</p><p>the UAS belongs to one of the classes;</p>
      <p>UAS.OPEN.020 UAS operations in subcategory A1</p><p>(1)</p><p>be conducted with an unmanned aircraft.</p>
      <p>PART 2</p><p>Requirements for a class C1 Unmanned aircraft system</p>
      <p>A class C1 UAS shall comply with the following.</p>
    </body></html>"""
    f = tmp_path / "reg.html"
    f.write_text(html, encoding="utf-8")
    secs = index.html_sections(f)
    locations = [s["location"] for s in secs]
    assert locations[0] == "Article 4"
    assert "UAS.OPEN.020 UAS operations in subcategory A1" in locations
    assert any(loc.startswith("PART 2 Requirements for a class C1") for loc in locations)
    assert "(a) the UAS belongs to one of the classes;" in secs[0]["text"]
    assert "▼M1" not in " ".join(s["text"] for s in secs)


def test_clean_rejoins_hyphenated_words_and_spaces():
    assert index.clean("the regu- lation   applies\n") == "the regulation applies"


def test_download_skips_a_source_it_cannot_fetch(tmp_path, monkeypatch):
    monkeypatch.setattr(index, "CORPUS_DIR", tmp_path)
    src = {"source": "X", "url": "https://example.invalid/x", "file": "x.html"}

    class Empty:
        content = b""

        def raise_for_status(self):
            pass

    monkeypatch.setattr(index.httpx, "get", lambda *a, **k: Empty())
    assert index.download(src) is None
    assert not (tmp_path / "x.html").exists()

    def offline(*a, **k):
        raise httpx.ConnectError("offline")

    monkeypatch.setattr(index.httpx, "get", offline)
    assert index.download(src) is None

    (tmp_path / "x.html").write_bytes(b"x" * index.MIN_FILE_BYTES)
    assert index.download(src) == tmp_path / "x.html"  # a full-size cached file is used as it is


def test_bm25_ranks_documents_with_the_query_terms_first(monkeypatch):
    rows = {"light": ("ensure that a green flashing light is activated at night",
                      {"source": "Reg 2019/947", "location": "UAS.OPEN.060"}),
            "mass": ("have a maximum take-off mass of less than 250 g",
                     {"source": "Reg 2019/945", "location": "PART 1"})}

    class FakeCollection:
        def get(self, ids=None, where=None, include=()):
            ids = ids or [i for i in rows if not where or rows[i][1]["source"] in where["source"]["$in"]]
            return {"ids": ids, "documents": [rows[i][0] for i in ids], "metadatas": [rows[i][1] for i in ids]}

    monkeypatch.setattr(index, "collection", lambda design: FakeCollection())
    monkeypatch.setattr(index, "_BM25", {})
    assert index.bm25_ranking("Do I need a light to fly at night?", "test") == ["light", "mass"]
    assert index.bm25_ranking("What is the maximum take-off mass?", "test")[0] == "mass"
    top = index.retrieve_bm25("What is the maximum take-off mass?", "test", k=1)
    assert [(h["source"], h["location"]) for h in top] == [("Reg 2019/945", "PART 1")]
    # restricted to some sources, the other documents are never ranked
    assert index.bm25_ranking("What is the maximum take-off mass?", "test", sources=["Reg 2019/947"]) == ["light"]
