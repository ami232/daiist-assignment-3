"""Ingestion on the real corpus files: cleaning, names, locations, chunking. No network.

    uv run python -m unittest discover tests
"""

import re
import unittest

import index

NAMES = r"Sturgeon|McDonagh|Wallentin|Folkerts|Pešková|Cachafeiro|Garrido|COX|McDOWELL|SASSOLI|ZACARIAS|SCHULZ|SCHMIT|BUZEK|MARTONYI"


class TestCleaning(unittest.TestCase):
    def test_hyphen_break_is_joined(self):
        lines = [{"text": "the legal posi-", "page": 3}, {"text": "tions of Spain", "page": 3}]
        repaired, joined, kept = index.repair_hyphenation(lines)
        self.assertEqual(repaired[0]["text"], "the legal positions")
        self.assertEqual((joined, kept), (1, 0))

    def test_real_hyphen_is_kept(self):
        lines = [{"text": "a non-scheduled flight and a non-", "page": 1}, {"text": "scheduled service", "page": 1}]
        repaired, joined, kept = index.repair_hyphenation(lines)
        self.assertIn("non-scheduled service", " ".join(l["text"] for l in repaired))
        self.assertEqual(kept, 1)

    def test_soft_hyphen_with_space_is_joined(self):
        lines = [{"text": "be obliged to pay compen \xad", "page": 1}, {"text": "sation if", "page": 1}]
        repaired, _, _ = index.repair_hyphenation(lines)
        self.assertEqual(repaired[0]["text"], "be obliged to pay compensation")

    def test_header_splits_body_from_footnotes(self):
        page = ("end of the body text\n17.2.2004 L 46/2Official Journal of the European UnionEN\n"
                "(1) OJ C 103 E, 30.4.2002, p. 225.\n(2) OJ C 241,\n7.10.2002, p. 29.")
        body, notes = index.clean_page(page)
        self.assertEqual(body, ["end of the body text"])
        self.assertEqual(index.parse_footnotes(notes, 2)[2]["text"], "OJ C 241, 7.10.2002, p. 29.")

    def test_case_party_names_removed_identifiers_kept(self):
        text = ("(74) Joined Cases C-402/07 and C-432/07, Sturgeon\nand Others, ECLI:EU:C:2009:716. "
                "Judgment of the Court of Justice of 30 April 2002, Club Tour v Alberto Carlos Lobo Gonçalves Garrido "
                "and Club Med Viagens Lda, C-400/00, ECLI:EU:C:2002:272. Case C-74/19, Transportes, EU:C:2020:460. "
                "ruling in the\nSturgeon case (74)")
        cleaned = index.remove_personal_names(text)
        self.assertNotRegex(cleaned, NAMES)
        for kept in ("C-402/07", "ECLI:EU:C:2009:716", "C-400/00", "EU:C:2020:460"):
            self.assertIn(kept, cleaned)


class TestRealCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs, cls.chunks = index.build_corpus(index.CORE_IDS)
        cls.holdout = index.extract_document(index.CORPUS_DIR / index.DOCUMENTS["32011R0181"]["file"])

    def test_corpus_size(self):
        self.assertGreaterEqual(len(self.docs), 3)
        words = sum(d["words"] + d["footnote_words"] for d in self.docs)
        self.assertGreaterEqual(words, 50_000)

    def test_holdout_not_in_baseline_chunks(self):
        for design, chunks in self.chunks.items():
            self.assertNotIn("32011R0181", {c["source"] for c in chunks}, design)

    def test_chunks_never_mix_documents(self):
        for chunks in self.chunks.values():
            for chunk in chunks:
                self.assertTrue(chunk["id"].startswith(chunk["source"] + ":"))

    def test_every_chunk_has_citation_metadata(self):
        for design, chunks in self.chunks.items():
            for c in chunks:
                for key in ("id", "source", "title", "edition", "location", "first_page", "last_page", "design", "content_hash"):
                    self.assertIn(key, c, f"{design} {c['id']} lacks {key}")
                self.assertEqual(c["design"], design)

    def test_ids_unique_and_stable(self):
        again = index.build_corpus(index.CORE_IDS)[1]
        for design, chunks in self.chunks.items():
            ids = [c["id"] for c in chunks]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual([(c["id"], c["content_hash"]) for c in chunks],
                             [(c["id"], c["content_hash"]) for c in again[design]])

    def test_no_names_headers_or_toc_in_chunks(self):
        text = "\n".join(c["text"] for chunks in self.chunks.values() for c in chunks)
        self.assertNotRegex(text, NAMES)
        self.assertNotRegex(text, r"\d+/36 ELI:|\. \. \. \.|car rier|\xad")
        # the correlation tables' column headers: the tables themselves are excluded, mentions of them are not
        self.assertNotRegex(text, r"Regulation \(EC\) No 1371/2007\s+This Regulation|Directive 90/314/EEC\s+This Directive")

    def test_exception_stays_with_its_article(self):
        article5 = [c for c in self.chunks["B"] if c["source"] == "32004R0261" and c["location"] == "Article 5"]
        self.assertEqual(len(article5), 1)
        self.assertIn("extraordinary circumstances", article5[0]["text"])
        self.assertIn("1. In case of cancellation", article5[0]["text"])

    def test_split_parts_repeat_their_heading(self):
        for c in self.chunks["B"]:
            part = int(c["id"].rsplit(":", 1)[1])
            if part > 1 and not c["location"].startswith(("Recital", "Preamble", "Signatures")):
                self.assertTrue(c["text"].startswith("["), c["id"])

    def test_footnote_case_ids_travel_with_chunks(self):
        section = [c for c in self.chunks["B"] if c["location"] == "Section 5.2.3"]
        self.assertTrue(any("Notes:" in c["text"] and "ECLI" in c["text"] for c in section))

    def test_html_uses_articles_not_pages(self):
        chunks = index.chunk_document(self.holdout, "B")
        self.assertTrue(all("first_page" not in c for c in chunks))
        self.assertIn("Article 19", {c["location"] for c in chunks})
        article19 = next(c for c in chunks if c["location"] == "Article 19")
        self.assertRegex(article19["text"], r"more than 120 minutes")


if __name__ == "__main__":
    unittest.main()
