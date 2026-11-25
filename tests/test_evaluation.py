"""Evaluation logic: location matching, question validation, refusal detection, agreement. No network."""

import unittest

import evaluate
import index


def meta(source, locations, first=None, last=None):
    m = {"source": source, "locations": " | ".join(locations)}
    if first is not None:
        m["first_page"], m["last_page"] = first, last
    return m


class TestLocationMatching(unittest.TestCase):
    def test_articles_and_sections(self):
        self.assertTrue(evaluate.location_matches("Article 7", ["Article 7"]))
        self.assertTrue(evaluate.location_matches("Art. 7(1)", ["Article 6", "Article 7"]))
        self.assertFalse(evaluate.location_matches("Article 7", ["Article 17"]))
        self.assertTrue(evaluate.location_matches("Section 4.4", ["Section 4.4.7"]))
        self.assertFalse(evaluate.location_matches("Section 4.4", ["Section 4.40"]))
        self.assertTrue(evaluate.location_matches("Annex I", ["Annex I, Article 32"]))
        self.assertTrue(evaluate.location_matches("Recital 14", ["Recital (14)"]))

    def test_pages(self):
        self.assertTrue(evaluate.location_matches("p. 5", ["Article 7"], 4, 5))
        self.assertFalse(evaluate.location_matches("p. 9", ["Article 7"], 4, 5))
        self.assertFalse(evaluate.location_matches("p. 5", ["Article 7"]))  # HTML has no pages

    def test_right_location_in_wrong_document_is_not_a_hit(self):
        pair = {"source": "32004R0261", "location": "Article 7"}
        self.assertTrue(evaluate.chunk_matches(meta("32004R0261", ["Article 7"]), pair))
        self.assertFalse(evaluate.chunk_matches(meta("32021R0782", ["Article 7"]), pair))
        page_pair = {"source": "32004R0261", "location": "p. 5"}
        self.assertFalse(evaluate.chunk_matches(meta("32015L2302", ["Article 9"], 5, 5), page_pair))


class TestQuestions(unittest.TestCase):
    def test_submitted_questions_are_valid_against_the_real_chunks(self):
        docs, chunks = index.build_corpus(index.CORE_IDS)
        known = {}
        for design_chunks in chunks.values():
            for c in design_chunks:
                known.setdefault(c["source"], []).append((c["locations"].split(" | "), c["first_page"], c["last_page"]))
        rows = evaluate.read_questions()
        self.assertEqual(evaluate.validate_questions(rows, known), [])

    def test_validation_catches_bad_rows(self):
        rows = [{"id": "x1", "question": "?", "kind": "unanswerable", "expected_source": "32004R0261",
                 "expected_location": "", "expected": [], "mapping_ok": True},
                {"id": "x2", "question": "?", "kind": "single", "expected_source": "32004R0261",
                 "expected_location": "Article 99", "expected": [{"source": "32004R0261", "location": "Article 99"}],
                 "mapping_ok": True}]
        problems = evaluate.validate_questions(rows, {"32004R0261": [(["Article 7"], 5, 5)]})
        self.assertTrue(any("x1" in p for p in problems))
        self.assertTrue(any("x2" in p and "Article 99" in p for p in problems))


class TestScoring(unittest.TestCase):
    def test_response_kinds(self):
        self.assertEqual(evaluate.response_kind("NOT IN CORPUS: no bus rules."), "refusal")
        self.assertEqual(evaluate.response_kind("  NEED DETAILS: distance?"), "clarification")
        self.assertEqual(evaluate.response_kind("WITHHELD: blocked."), "withheld")
        self.assertEqual(evaluate.response_kind("You get EUR 250 [x:B:a:1]. Not in corpus: insurance."), "answer")

    def test_failure_classes(self):
        single, unanswerable = {"kind": "single"}, {"kind": "unanswerable"}
        ok = {"correct": True, "supported": True}
        refusal = {"response_kind": "refusal", "expected_evidence_returned": True}
        answer_right_passage = {"response_kind": "answer", "expected_evidence_returned": True}
        answer_no_passage = {"response_kind": "answer", "expected_evidence_returned": False}
        self.assertIsNone(evaluate.failure_class(single, answer_right_passage, ok))
        self.assertEqual(evaluate.failure_class(single, refusal, {"correct": False, "supported": True}), "wrong refusal")
        self.assertEqual(evaluate.failure_class(single, answer_right_passage, {"correct": False, "supported": True}),
                         "wrong answer from the right passage")
        self.assertEqual(evaluate.failure_class(single, answer_no_passage, {"correct": False, "supported": False}),
                         "retrieval miss")
        self.assertEqual(evaluate.failure_class(single, answer_right_passage, {"correct": True, "supported": False}),
                         "unsupported claim")
        self.assertEqual(evaluate.failure_class(unanswerable, answer_no_passage, {"correct": False, "supported": False}),
                         "unsupported claim")

    def test_agreement_counts_only_answers_graded_by_both(self):
        labels = {"q1": {"correct": "1", "supported": "1"}, "q2": {"correct": "0", "supported": "1"},
                  "q3": {"correct": "1", "supported": ""}}
        verdicts = {"q1": {"correct": True, "supported": False}, "q2": {"correct": True, "supported": True}}
        report = evaluate.agreement(labels, verdicts)
        self.assertEqual(report["correct"], {"n": 2, "agree": 1, "rate": 0.5, "human_yes_judge_no": 0, "human_no_judge_yes": 1})
        self.assertEqual(report["supported"]["n"], 2)
        self.assertEqual(report["supported"]["agree"], 1)


if __name__ == "__main__":
    unittest.main()
