"""Storage, caching, resume and add_document on a temp index; the Gemini call is a fake."""

import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import index

HOLDOUT = index.CORPUS_DIR / index.DOCUMENTS["32011R0181"]["file"]


def fake_vector(text):
    digest = hashlib.sha256(text.encode()).digest()
    return [(digest[i % 32] - 128) / 128 for i in range(index.EMBEDDING_DIMENSIONS)]


class FakeEmbedder:
    """Counts texts embedded; can fail on a chosen call to simulate quota or network loss."""

    def __init__(self, fail_on_call=None):
        self.calls, self.texts, self.fail_on_call = 0, 0, fail_on_call

    def __call__(self, texts):
        self.calls += 1
        if self.calls == self.fail_on_call:
            raise RuntimeError("429 RESOURCE_EXHAUSTED (simulated)")
        self.texts += len(texts)
        return [fake_vector(t) for t in texts]


class StoreTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.db = index.open_index(self.tmp)  # creates chroma.sqlite3, so require_index passes
        self.cache = index.get_collection(self.db, "embedding_cache")
        self.collection = index.design_collection(self.db, "B")
        doc = index.extract_document(index.CORPUS_DIR / index.DOCUMENTS["32004R0261"]["file"])
        self.chunks = index.chunk_document(doc, "B")
        patcher = mock.patch.object(index, "PACE_SECONDS", 0)
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestCacheAndResume(StoreTestCase):
    def test_second_run_embeds_nothing(self):
        fake = FakeEmbedder()
        with mock.patch.object(index, "embed_texts", fake):
            first = index.embed_and_store(self.chunks, self.collection, self.cache)
            second = index.embed_and_store(self.chunks, self.collection, self.cache)
        self.assertEqual(first, len(self.chunks))
        self.assertEqual(second, 0)
        self.assertEqual(fake.texts, len(self.chunks))

    def test_interrupted_run_resumes_without_restarting(self):
        with mock.patch.object(index, "BATCH_SIZE", 5), mock.patch.object(index, "embed_texts", FakeEmbedder(fail_on_call=3)):
            with self.assertRaises(RuntimeError) as failure:
                index.embed_and_store(self.chunks, self.collection, self.cache)
        self.assertIn("saved", str(failure.exception))
        self.assertEqual(self.cache.count(), 10)  # the two batches before the failure were kept
        resumed = FakeEmbedder()
        with mock.patch.object(index, "BATCH_SIZE", 5), mock.patch.object(index, "embed_texts", resumed):
            new = index.embed_and_store(self.chunks, self.collection, self.cache)
        self.assertEqual(new, len(self.chunks) - 10)
        self.assertEqual(self.collection.count(), len(self.chunks))

    def test_cache_key_depends_on_model_size_and_text(self):
        base = index.cache_key("title: x | text: y")
        self.assertNotEqual(base, index.cache_key("title: x | text: z"))
        with mock.patch.object(index, "EMBEDDING_DIMENSIONS", 1536):
            self.assertNotEqual(base, index.cache_key("title: x | text: y"))
        with mock.patch.object(index, "EMBEDDING_MODEL", "other-model"):
            self.assertNotEqual(base, index.cache_key("title: x | text: y"))

    def test_misaligned_batch_is_rejected(self):
        response = mock.Mock(embeddings=[mock.Mock(values=[0.0] * index.EMBEDDING_DIMENSIONS)])
        client = mock.Mock()
        client.models.embed_content.return_value = response
        with mock.patch.object(index, "gemini_client", return_value=client):
            with self.assertRaises(RuntimeError):
                index.embed_texts(["one", "two"])


class TestAddDocument(StoreTestCase):
    def state(self):
        got = self.collection.get(include=["embeddings"])
        return sorted(got["ids"]), sorted(tuple(round(x, 6) for x in v) for v in got["embeddings"])

    def test_duplicate_changes_nothing_and_embeds_nothing(self):
        with mock.patch.object(index, "embed_texts", FakeEmbedder()):
            first = index.index_file(HOLDOUT, design="B", index_dir=self.tmp)
        before = self.state()
        fake = FakeEmbedder()
        with mock.patch.object(index, "embed_texts", fake):
            second = index.index_file(HOLDOUT, design="B", index_dir=self.tmp)
        self.assertEqual(first["status"], "added")
        self.assertEqual(second["status"], "already_indexed")
        self.assertEqual(fake.calls, 0)
        self.assertEqual(self.state(), before)

    def test_changed_content_under_same_id_is_refused(self):
        with mock.patch.object(index, "embed_texts", FakeEmbedder()):
            index.index_file(HOLDOUT, design="B", index_dir=self.tmp)
        before = self.state()
        changed = self.tmp / "changed" / HOLDOUT.name
        changed.parent.mkdir()
        changed.write_text(HOLDOUT.read_text(encoding="utf-8").replace("120 minutes", "90 minutes"), encoding="utf-8")
        fake = FakeEmbedder()
        with mock.patch.object(index, "embed_texts", fake):
            result = index.index_file(changed, design="B", index_dir=self.tmp)
        self.assertEqual(result["status"], "refused_changed_content")
        self.assertEqual(fake.calls, 0)
        self.assertEqual(self.state(), before)


if __name__ == "__main__":
    unittest.main()
