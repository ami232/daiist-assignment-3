"""Offline engineering tests. Synthetic vectors are never submission evidence."""

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from agent import AgentRunner, enforce_citations
from evaluate import (
    evidence_hit,
    matches,
)
from index import build
from ingestion import VectorStore, digest
from runtime import Retriever, add_document, citation_check, vector_model


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "corpus").mkdir()
        (self.root / "index").mkdir()
        documents = []
        for name in ["one", "two", "three"]:
            path = self.root / "corpus" / f"{name}.txt"
            path.write_text(("word " * 18000).strip())
            documents.append(
                {
                    "path": str(path.relative_to(self.root)),
                    "source": name,
                    "url": "https://example.org/" + name,
                    "license": "synthetic-test-only",
                    "no_personal_data_confirmed": True,
                }
            )
        self.config = {
            "student_approved": True,
            "documents": documents,
            "embedding_model": "synthetic-test-only",
            "selected_design": "large",
            "designs": [
                {"name": "large", "words": 18000, "overlap": 0},
                {"name": "small", "words": 9000, "overlap": 0},
            ],
        }
        self.save_config()
        self.policy = {"refusal_text": "Not in the documents."}

    def tearDown(self):
        self.directory.cleanup()

    def save_config(self):
        (self.root / "corpus_config.json").write_text(json.dumps(self.config))

    def initial_index(self):
        from index import prepare

        _, designs = prepare(self.config, self.root)
        store = VectorStore(self.root / "index" / "vectors.sqlite3")
        store.add_many(designs, vector_model(self.config), lambda _: [1, 0])
        store.db.close()
        (self.root / "index" / "manifest.json").write_text("{}")

    def test_dry_run_never_needs_key_or_embeddings(self):
        result = build(self.config, dry_run=True, root=self.root)
        self.assertEqual(result["words"], 54000)
        self.assertEqual(result["chunks"], {"large": 3, "small": 6})
        self.assertFalse((self.root / "index" / "vectors.sqlite3").exists())

    def test_query_cache_and_reload_use_saved_vectors(self):
        self.initial_index()
        calls = []
        first = Retriever(self.root, query_embed=lambda q: calls.append(q) or [1, 0])
        result = first.search("same question", k=1)
        first.close()
        second = Retriever(
            self.root, query_embed=lambda q: self.fail("query should be cached")
        )
        self.assertEqual(
            second.search("same question", design="small", k=1)["chunks"][0]["score"], 1
        )
        second.close()
        self.assertEqual(calls, ["same question"])
        self.assertTrue(
            citation_check(result["chunks"][0]["citation"], result["chunks"])["valid"]
        )

    def test_add_document_noop_and_changed_file(self):
        self.initial_index()
        document = {
            "path": "corpus/four.txt",
            "source": "four",
            "url": "https://example.org/four",
            "license": "synthetic-test-only",
            "no_personal_data_confirmed": True,
        }
        self.config["additional_documents"] = [document]
        self.save_config()
        (self.root / "corpus/four.txt").write_text("new evidence")
        result = add_document(document["path"], self.root, lambda _: [0, 1])
        self.assertEqual(
            result["new_embedding_calls"], 1
        )  # both designs share identical text
        repeated = add_document(
            document["path"], self.root, lambda _: self.fail("must not embed twice")
        )
        self.assertEqual(repeated["new_embedding_calls"], 0)
        (self.root / "corpus/four.txt").write_text("changed evidence")
        add_document(document["path"], self.root, lambda _: [0, 1])
        store = VectorStore(self.root / "index" / "vectors.sqlite3")
        for design in ["small", "large"]:
            rows = store.db.execute(
                "SELECT text FROM chunks WHERE source=? AND design=?", ("four", design)
            ).fetchall()
            self.assertEqual(rows, [("changed evidence",)])
        store.db.close()

    def test_denies_unregistered_and_outside_files(self):
        self.initial_index()
        with self.assertRaisesRegex(ValueError, "Only files"):
            add_document(
                "../private.txt", self.root, lambda _: self.fail("must not transmit")
            )
        with self.assertRaisesRegex(ValueError, "Register"):
            add_document(
                "corpus/unregistered.txt",
                self.root,
                lambda _: self.fail("must not transmit"),
            )
        (self.root / "corpus/link.txt").symlink_to(self.root.parent / "outside.txt")
        with self.assertRaisesRegex(ValueError, "Only files"):
            add_document(
                "corpus/link.txt", self.root, lambda _: self.fail("must not transmit")
            )

    def test_atomic_activation_across_designs(self):
        self.initial_index()
        store = VectorStore(self.root / "index" / "vectors.sqlite3")
        original = store.db.execute(
            "SELECT * FROM chunks ORDER BY design,id"
        ).fetchall()

        def embed(text):
            if text == "fail":
                raise RuntimeError("synthetic quota failure")
            return [1, 1]

        new = lambda text: {
            "id": digest(text),
            "source": "new",
            "location": "text",
            "text": text,
        }
        with self.assertRaises(RuntimeError):
            store.add_many(
                {"large": [new("success")], "small": [new("fail")]}, "new-model", embed
            )
        self.assertEqual(
            store.db.execute("SELECT * FROM chunks ORDER BY design,id").fetchall(),
            original,
        )
        self.assertEqual(
            store.db.execute(
                "SELECT count(*) FROM vectors WHERE model=?", ("new-model",)
            ).fetchone()[0],
            1,
        )
        store.db.close()

    def test_citation_guardrail_is_identity_only(self):
        chunk = {"id": "a" * 64}
        for answer in [
            "Uncited assertion.",
            "[chunk:" + "b" * 64 + "]",
            "[chunk:fake]",
        ]:
            safe, check = enforce_citations(answer, [chunk], self.policy)
            self.assertEqual(safe, self.policy["refusal_text"])
            self.assertTrue(check["triggered"])
        text = "A claim [chunk:" + "a" * 64 + "]"
        self.assertEqual(enforce_citations(text, [chunk], self.policy)[0], text)
        self.assertEqual(
            enforce_citations(self.policy["refusal_text"], [], self.policy)[0],
            self.policy["refusal_text"],
        )

    def test_grouped_and_bare_citations_validate_every_exact_id(self):
        first, second = "a" * 64, "b" * 64
        chunks = [{"id": first}, {"id": second}]
        for marker in [
            f"[chunk:{first}, chunk:{second}]",
            f"[chunk:{first}, {second}]",
            f"[{first}]",
            f"[cite: {first}, {second}]",
        ]:
            answer, check = enforce_citations("Claim " + marker, chunks, self.policy)
            self.assertFalse(check["triggered"])
            self.assertIn(f"[chunk:{first}]", answer)
        for marker in [f"[chunk:{first}, {'c' * 64}]", f"[{first}, {'b' * 63}]"]:
            answer, check = enforce_citations(marker, chunks, self.policy)
            self.assertTrue(check["triggered"])
            self.assertEqual(answer, self.policy["refusal_text"])

    def test_named_source_guard_does_not_confuse_similar_documents(self):
        from runtime import missing_named_sources

        config = {
            "documents": [{"source": "fema", "aliases": ["FEMA"]}],
            "additional_documents": [
                {"source": "sba", "aliases": ["SBA", "Small Business Administration"]}
            ],
        }
        self.assertEqual(
            missing_named_sources("What does the SBA guide say?", config), ["sba"]
        )
        self.assertEqual(missing_named_sources("What does FEMA say?", config), [])
        self.assertEqual(missing_named_sources("What are supplier risks?", config), [])
        config["documents"].append(config["additional_documents"].pop())
        self.assertEqual(
            missing_named_sources("What does the SBA guide say?", config), []
        )

    def test_gold_matching_requires_two_locations_and_page_boundaries(self):
        q = {
            "id": "q",
            "kind": "multi",
            "expected_source": "one;one",
            "expected_location": "PDF page 4;PDF page 9",
        }
        first = {"source": "one", "location": "PDF page 4; words 1-100"}
        wrong = {"source": "one", "location": "PDF page 40; words 1-100"}
        second = {"source": "one", "location": "PDF page 9; words 1-100"}
        self.assertFalse(matches(wrong, "one", "PDF page 4"))
        self.assertFalse(evidence_hit(q, [first, wrong]))
        self.assertTrue(evidence_hit(q, [first, second]))

    def test_harness_denies_write_before_mcp_call(self):
        runner = object.__new__(AgentRunner)
        runner.trace = []
        runner.policy = {"max_tool_calls": 8}
        runner.approval = lambda _: False

        class Session:
            async def call_tool(self, *args):
                raise AssertionError("approval must run first")

        runner.session = Session()
        tool = SimpleNamespace(
            name="add_document",
            description="Add approved document",
            input_schema={
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        )
        result = asyncio.run(runner.wrap(tool).ainvoke({"path": "corpus/x.txt"}))
        self.assertIn("Human approval denied", result)
        self.assertEqual(runner.trace[0]["status"], "denied")


if __name__ == "__main__":
    unittest.main()
