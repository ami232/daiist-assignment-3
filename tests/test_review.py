"""Isolated synthetic review fixtures; never write actual student grades."""
import json
from pathlib import Path
import tempfile
import unittest

from review import Review


class HumanReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        record = {"id": "synthetic", "question": "Synthetic question",
                  "agent_answer": "Synthetic answer", "reference_answer": "Synthetic reference",
                  "retrieved_passages": [], "answer_review_sha256": "synthetic-review-hash"}
        (self.directory / "human_review.json").write_text(json.dumps([record]))
        (self.directory / "human_labels.csv").write_text("id,correct,supported,notes\n")
        self.review = Review(self.directory)

    def tearDown(self):
        self.temporary.cleanup()

    def request(self, correct=1, supported=1, notes=""):
        return {"review_hash": self.review.review_hash, "labels_hash": self.review.labels_hash(),
                "labels": [{"id": "synthetic", "correct": correct, "supported": supported, "notes": notes}]}

    def test_blank_review_stays_blank_and_zero_requires_explanation(self):
        self.assertEqual(self.review.payload()["labels"], {})
        before = self.review.labels_path.read_bytes()
        with self.assertRaisesRegex(ValueError, "explain every zero"):
            self.review.save(self.request(supported=0))
        self.assertEqual(before, self.review.labels_path.read_bytes())
        self.review.save(self.request(supported=0, notes="Synthetic unsupported addition."))
        self.assertEqual(self.review.payload()["labels"]["synthetic"]["supported"], 0)

    def test_changed_evidence_and_stale_window_cannot_overwrite_grades(self):
        stale = self.request()
        self.review.save(self.request(notes="Synthetic initial review."))
        with self.assertRaisesRegex(ValueError, "another window"):
            self.review.save(stale)
        (self.directory / "human_review.json").write_text("[]")
        with self.assertRaisesRegex(ValueError, "answers or evidence changed"):
            self.review.save(self.request())

    def test_bound_blind_review_is_locked(self):
        path = self.directory / "runs" / "synthetic"
        path.mkdir(parents=True)
        (path / "human_binding.json").write_text(json.dumps({"reviewed_answers": {"synthetic": "synthetic-review-hash"}}))
        self.assertTrue(self.review.payload()["locked"])
        with self.assertRaisesRegex(ValueError, "locked"):
            self.review.save(self.request())


if __name__ == "__main__":
    unittest.main()
