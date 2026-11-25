"""Pipeline tests use synthetic vectors in temporary databases, never the corpus index."""
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from index import add_document, chunk_sections, embed_and_store
from retrieval import DIMENSIONS, Store, bm25_scores, search


def section(source, text, location="1.1"):
    return {"source": source, "document_title": source, "section_title": location,
            "location": location, "url": "https://example.test/"+source,
            "license": "Synthetic test fixture", "text": text}


class FakeEmbedder:
    def __init__(self, fail_after=None):
        self.calls = []
        self.fail_after = fail_after

    def __call__(self, text, title=None, role="document"):
        if self.fail_after is not None and len(self.calls) >= self.fail_after:
            raise ConnectionError("Synthetic interruption")
        self.calls.append((role, text))
        vector = np.zeros(DIMENSIONS, dtype=np.float32)
        vector[0] = 1
        if "lexical-target" in text:
            vector[1] = 0.5
        return vector, 10


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.store = Store(self.root / "test.sqlite3")

    def tearDown(self):
        self.directory.cleanup()

    def register(self, sections):
        chunks = chunk_sections(sections)
        for source in {chunk["source"] for chunk in chunks}:
            self.store.put_document(source, source, source, [chunk for chunk in chunks if chunk["source"] == source])
        return chunks

    def test_chunking_covers_text_without_crossing_sections(self):
        texts = [" ".join(f"word{i}" for i in range(901)), "separate section"]
        chunks = chunk_sections([section("same-book", text, str(i)) for i, text in enumerate(texts)])
        self.assertEqual(len({chunk["id"] for chunk in chunks}), len(chunks))
        for location, text in enumerate(texts):
            selected = [chunk for chunk in chunks if chunk["location"] == str(location)]
            covered = set()
            for chunk in selected:
                self.assertLessEqual(chunk["word_count"], 400)
                self.assertEqual(chunk["text"].split(), text.split()[chunk["word_start"]:chunk["word_end"]])
                covered.update(range(chunk["word_start"], chunk["word_end"]))
            self.assertEqual(covered, set(range(len(text.split()))))

    def test_interrupted_embedding_run_resumes_without_repeating_successes(self):
        chunks = self.register([section("book", " ".join(f"word{i}" for i in range(900)))])
        interrupted = FakeEmbedder(fail_after=1)
        with self.assertRaises(RuntimeError):
            embed_and_store(chunks, self.store, interrupted, delay=0)
        self.assertEqual(self.store.status()["embedded_chunks"], 1)
        resumed = FakeEmbedder()
        progress = embed_and_store(chunks, self.store, resumed, delay=0)
        self.assertEqual(len(resumed.calls), len(chunks)-1)
        self.assertEqual(progress["remaining"], 0)
        unused = FakeEmbedder(fail_after=0)
        self.assertEqual(embed_and_store(chunks, self.store, unused, delay=0)["new_vectors"], 0)

    def test_designs_reuse_vectors_and_hybrid_can_change_ranking(self):
        chunks = self.register([section("semantic-first", "general funding concepts"),
                                section("keyword-first", "lexical-target liquidity")])
        embed_and_store(chunks, self.store, FakeEmbedder(), delay=0)
        query_embedder = FakeEmbedder()
        dense = search("liquidity", store=self.store, embedder=query_embedder, design="dense")
        hybrid = search("liquidity", store=self.store, embedder=query_embedder, design="hybrid")
        self.assertEqual(dense["results"][0]["source"], "semantic-first")
        self.assertEqual(hybrid["results"][0]["source"], "keyword-first")
        self.assertEqual(len(query_embedder.calls), 1)
        self.assertTrue(hybrid["query_embedding_cache_hit"])
        for result in hybrid["results"]:
            self.assertEqual(result["citation"], f"[{result['source']} | {result['location']}]")
        reopened = Store(self.store.path, create=False)
        search("liquidity", store=reopened, embedder=FakeEmbedder(fail_after=0))

    def test_incomplete_index_does_not_silently_search_a_subset(self):
        self.register([section("book", "cash and working capital")])
        unused = FakeEmbedder()
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            search("cash", store=self.store, embedder=unused)
        self.assertEqual(unused.calls, [])

    def test_renaming_identical_document_does_not_add_or_embed_it_twice(self):
        path = self.root / "original.txt"
        path.write_text("A synthetic financial reference with cash information.")
        first = add_document(path, self.store, FakeEmbedder())
        renamed = self.root / "renamed.txt"
        renamed.write_bytes(path.read_bytes())
        second = add_document(renamed, self.store, FakeEmbedder(fail_after=0))
        self.assertEqual(first["source"], second["source"])
        self.assertTrue(second["document_already_indexed"])
        self.assertEqual(second["new_vectors"], 0)
        self.assertEqual(self.store.status()["documents"], 1)

    def test_keyword_search_gives_unmatched_documents_no_score(self):
        self.assertEqual(bm25_scores("absent", [{"title": "", "text": "cash"}]).tolist(), [0.0])

    def test_server_rejects_paths_outside_corpus(self):
        import server
        with self.assertRaisesRegex(ValueError, "corpus"):
            server.add_document(str(Path(__file__).resolve()))


if __name__ == "__main__":
    unittest.main()
