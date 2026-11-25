import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from agent import ToolBridge
from answer_guardrails import AnswerDraft, BLOCKED_ANSWER, CitedClaim, guard_answer, render_answer, validate_draft


def evidence():
    return [{"tool": "search", "status": "success", "result": {"results": [
        {"id": "fixture-1", "citation": "[test-book | 1.1]", "text": "Synthetic test evidence"}]}}]


class CitationTests(unittest.IsolatedAsyncioTestCase):
    async def test_invalid_citation_gets_one_correction(self):
        invalid = AnswerDraft(status="supported", answer_claims=[CitedClaim(text="Synthetic claim", citations=["[invented | 99]"])])
        calls = []
        async def repair(previous, issues):
            calls.append(issues)
            return AnswerDraft(status="supported", answer_claims=[CitedClaim(text="Synthetic claim", citations=["[test-book | 1.1]"])])
        result = await guard_answer(invalid, evidence(), repair)
        self.assertEqual(len(calls), 1)
        self.assertFalse(result["guardrail_blocked"])
        self.assertIn("[test-book | 1.1]", result["answer"])

    async def test_second_invalid_answer_is_blocked_without_leaking_claim(self):
        invalid = AnswerDraft(status="supported", answer_claims=[CitedClaim(text="Unsupported $999 claim", citations=[])])
        calls = []
        async def repair(previous, issues):
            calls.append(issues)
            return invalid
        result = await guard_answer(invalid, evidence(), repair)
        self.assertEqual(len(calls), 1)
        self.assertTrue(result["guardrail_blocked"])
        self.assertEqual(result["answer"], BLOCKED_ANSWER)
        self.assertNotIn("999", result["answer"])

    async def test_pure_missing_information_can_have_no_factual_claims(self):
        draft = AnswerDraft(status="unanswerable", missing_information="The requested current period is absent from the retrieved documents.")
        async def repair(*args):
            self.fail("Valid refusal should not require correction")
        result = await guard_answer(draft, evidence(), repair)
        self.assertFalse(result["guardrail_blocked"])

    async def test_background_is_labelled_and_must_be_cited(self):
        draft = AnswerDraft(status="unanswerable", missing_information="Current company data is absent.",
                            general_background=[CitedClaim(text="Synthetic background", citations=["[test-book | 1.1]"])])
        self.assertEqual(validate_draft(draft, evidence()), [])
        self.assertIn("General background:", render_answer(draft))
        draft.general_background[0].citations = []
        self.assertIn("Factual claim has no citation", validate_draft(draft, evidence()))

    async def test_no_search_is_not_treated_as_grounded(self):
        draft = AnswerDraft(status="unanswerable", missing_information="Missing data")
        self.assertIn("No successful search before the answer", validate_draft(draft, []))

    async def test_inline_and_list_citations_render_once(self):
        draft = AnswerDraft(status="supported", answer_claims=[CitedClaim(
            text="Synthetic explanation [test-book | 1.1], [test-book | 1.1].",
            citations=["[test-book | 1.1]"])])
        self.assertEqual(validate_draft(draft, evidence()), [])
        self.assertEqual(render_answer(draft), "Synthetic explanation. [test-book | 1.1]")


class FakeSession:
    def __init__(self):
        self.calls = []
    async def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        return SimpleNamespace(content=[SimpleNamespace(text=json.dumps({"results": []}))], is_error=False)


class ApprovalTests(unittest.IsolatedAsyncioTestCase):
    async def test_denial_happens_before_remote_add_tool(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"approved-scope.txt"
            path.write_text("Synthetic reference document")
            session = FakeSession()
            reviews = []
            def deny(review):
                reviews.append(review)
                return False
            bridge = ToolBridge(session, approval=deny, allowed_root=directory)
            await bridge.invoke("add_document", {"path": str(path)})
            self.assertEqual(session.calls, [])
            self.assertEqual(bridge.trace[0]["status"], "approval_denied")
            self.assertEqual(reviews[0]["chunks"], 1)

    async def test_explicit_approval_allows_exact_requested_tool(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"reference.txt"
            path.write_text("Synthetic reference")
            session = FakeSession()
            bridge = ToolBridge(session, approval=lambda review: True, allowed_root=directory)
            await bridge.invoke("add_document", {"path": str(path)})
            self.assertEqual(session.calls, [("add_document", {"path": str(path)})])
            self.assertTrue(bridge.trace[0]["approval_granted"])

    async def test_tool_budget_does_not_allow_extra_remote_calls(self):
        session = FakeSession()
        bridge = ToolBridge(session, max_calls=2)
        for _ in range(3):
            await bridge.invoke("search", {"query": "synthetic"})
        self.assertEqual(len(session.calls), 2)
        self.assertEqual(bridge.trace[-1]["status"], "call_limit")


if __name__ == "__main__":
    unittest.main()
