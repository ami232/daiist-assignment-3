import unittest

from agent import REFUSAL, citation_ids, guard_answer


class CitationGuardTests(unittest.TestCase):
    first = "PG-0123456789abcd"
    second = "PG-1123456789abcd"
    unknown = "PG-2123456789abcd"

    def test_single_grouped_and_mixed_citations(self):
        known = {self.first, self.second}
        for answer in (f"[{self.first}][{self.second}]", f"[{self.first}, {self.second}]",
                       f"[{self.first}] [{self.second}, {self.first}]"):
            with self.subTest(answer=answer):
                self.assertEqual(citation_ids(answer), known)
                self.assertEqual(guard_answer(answer, known), (answer, None))

    def test_one_valid_citation_cannot_hide_a_bad_group_member(self):
        known = {self.first, self.second}
        for member in (self.unknown, "malformed", ""):
            answer = f"Claim [{self.first}]. Another claim [{self.second}, {member}]."
            with self.subTest(member=member):
                self.assertEqual(guard_answer(answer, known), (REFUSAL, "missing or unknown citation"))

    def test_refusal_and_missing_evidence(self):
        self.assertEqual(guard_answer(REFUSAL, {}), (REFUSAL, None))
        self.assertEqual(guard_answer("A claim without a citation.", {}), (REFUSAL, "missing or unknown citation"))
