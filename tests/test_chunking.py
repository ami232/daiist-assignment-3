import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from chunking import html_lines, parse_structured, article_chunks, fixed_chunks, parse_file

HTML = """<html><body>
<p>Recital text before the law.</p>
<p>CHAPTER I</p><p>General provisions</p>
<p>Article 1</p><p>Subject matter</p>
<p>1. This Regulation lays down rules.</p>
<p>Article 2</p><p>Definitions</p>
<table><tr><td><p>(1)</p></td><td><p>‘thing’ means a <a>thing</a> ;</p></td></tr>
<tr><td><p>(2)</p></td><td><p>‘other’ means other;</p></td></tr></table>
<p>Article 3</p><p>Breach</p><p>1. The controller shall notify within 72 hours.</p>
<p>Done at Brussels, 1 January 2020.</p>
<p>ANNEX I</p><p>List of things</p><p>1. First thing.</p>
</body></html>"""

def test_parse(tmp_path):
    p = tmp_path / "demo.html"; p.write_text(HTML)
    doc_id, title, secs = parse_file(p)
    assert doc_id == "demo"
    assert [s.location for s in secs] == ["Article 1", "Article 2", "Article 3", "Annex I"]
    assert secs[1].lines[0].startswith("(1) ‘thing’ means a thing;")      # marker merged, spacing fixed
    assert secs[2].chapter.startswith("CHAPTER I – General")
    assert "Done at" not in secs[2].text and "Recital" not in " ".join(s.text for s in secs)

def test_chunks():
    lines = ["Article 1", "Title"] + [f"({i}) " + "word " * 100 for i in range(1, 9)] + ["Article 2", "T2", "1. short."]
    secs = parse_structured(lines)
    ch = article_chunks("d", "Doc", secs, max_words=300)
    assert [c.location for c in ch][:2] == ["Article 1 (part 1/4)", "Article 1 (part 2/4)"]
    assert ch[-1].location == "Article 2" and ch[-1].text.startswith("Doc — Article 2: T2")
    fx = fixed_chunks("d", "Doc", secs, size=150, overlap=30)
    assert fx[0].base_locs == ["Article 1"] and any(len(c.base_locs) > 1 for c in fx)

def test_duplicate_toc_keeps_longest():
    secs = parse_structured(["Article 1", "Title", "Article 1", "Title", "1. real body text here."])
    assert len(secs) == 1 and "real body" in secs[0].text
