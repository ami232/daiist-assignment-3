import csv
from pathlib import Path
import tempfile
import unittest

from retrieval_evaluation import FIELDS, coverage_at_k, expected_evidence, load_questions


class RetrievalEvaluationTests(unittest.TestCase):
    def test_multi_requires_all_passages_even_from_one_section(self):
        question = {"expected_source": "book", "expected_location": "12.1@0:400;12.1@350:750"}
        first = {"source": "book", "location": "12.1", "passage_location": "12.1@0:400"}
        second = {"source": "book", "location": "12.1", "passage_location": "12.1@350:750"}
        self.assertEqual(len(expected_evidence(question)), 2)
        partial = coverage_at_k(question, [first, second], 1)
        self.assertEqual(partial, {"hit_any": 1, "hit_all": 0, "evidence_recall": 0.5})
        self.assertEqual(coverage_at_k(question, [first, second], 3)["hit_all"], 1)
        wrong = {**first, "passage_location": "12.1@700:902"}
        self.assertEqual(coverage_at_k(question, [wrong], 1)["hit_any"], 0)

    def test_unanswerable_is_not_a_retrieval_miss(self):
        question = {"expected_source": "", "expected_location": ""}
        self.assertIsNone(coverage_at_k(question, [], 5)["hit_any"])

    def test_incomplete_set_is_rejected_before_any_api_call(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"questions.csv"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
            with self.assertRaisesRegex(ValueError, "still being authored"):
                load_questions(path)


if __name__ == "__main__":
    unittest.main()
