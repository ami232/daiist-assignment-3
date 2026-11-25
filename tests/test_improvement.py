"""Regression checks for semantic rejection and bounded provider recovery."""
import unittest
from unittest.mock import AsyncMock, patch
from answer_guardrails import AnswerDraft, CitedClaim, guard_answer, dated_evidence_issues
from model_recovery import invoke_with_recovery, transient_error


class ImprovementTests(unittest.IsolatedAsyncioTestCase):
    def test_old_dated_example_cannot_answer_latest_year(self):
        trace = [{"tool": "search", "status": "success", "result": {"results": [
            {"id": "one", "citation": "[book | 1]", "text": "Operating cash in 2010 was $10."}]}}]
        draft = AnswerDraft(status="supported", answer_claims=[CitedClaim(text="In 2010, cash was $10.", citations=["[book | 1]"])])
        self.assertTrue(dated_evidence_issues("What was its cash in the most recent fiscal year?", draft, trace, "2026-11-24"))
        self.assertEqual(dated_evidence_issues("What is the current ratio?", draft, trace, "2026-11-24"), [])
        draft.status = "unanswerable"
        draft.answer_claims = []
        draft.missing_information = "The retrieved passages do not establish the latest year's cash."
        self.assertEqual(dated_evidence_issues("What was cash in the latest year?", draft, trace, "2026-11-24"), [])

    async def test_valid_citation_cannot_bypass_failed_support_audit(self):
        trace = [{"tool": "search", "status": "success", "result": {"results": [
            {"id": "one", "citation": "[book | 1]", "text": "Example company ratio is 0.6."}]}}]
        bad = AnswerDraft(status="supported", answer_claims=[CitedClaim(
            text="The industry median is 0.6.", citations=["[book | 1]"])])
        repair = AsyncMock(return_value=bad)
        audit = AsyncMock(return_value=["A company example does not establish an industry median"])
        result = await guard_answer(bad, trace, repair, audit=audit)
        self.assertTrue(result["guardrail_blocked"])
        self.assertEqual(audit.await_count, 2)
        self.assertEqual(repair.await_count, 1)
        self.assertNotIn("median", result["answer"])

    async def test_one_supported_correction_is_released(self):
        trace = [{"tool": "search", "status": "success", "result": {"results": [
            {"id": "one", "citation": "[book | 1]", "text": "Example company ratio is 0.6."}]}}]
        bad = AnswerDraft(status="supported", answer_claims=[CitedClaim(text="Industry median 0.6", citations=["[book | 1]"])])
        good = AnswerDraft(status="supported", answer_claims=[CitedClaim(text="The source example company has a ratio of 0.6.", citations=["[book | 1]"])])
        result = await guard_answer(bad, trace, AsyncMock(return_value=good),
                                  audit=AsyncMock(side_effect=[["Unsupported benchmark"], []]))
        self.assertFalse(result["guardrail_blocked"])
        self.assertEqual(result["correction_attempts"], 1)

    async def test_temporary_outage_is_retried_and_recorded(self):
        operation = AsyncMock(side_effect=[RuntimeError("503 high demand"), "ok"])
        events = []
        with patch("model_recovery.asyncio.sleep", AsyncMock()):
            self.assertEqual(await invoke_with_recovery(operation, events, "fixture"), "ok")
        self.assertEqual(operation.await_count, 2)
        self.assertTrue(events[0]["retry"])

    async def test_daily_quota_is_not_retried(self):
        operation = AsyncMock(side_effect=RuntimeError("429 GenerateRequestsPerDay"))
        with self.assertRaises(RuntimeError):
            await invoke_with_recovery(operation, [], "fixture")
        self.assertEqual(operation.await_count, 1)
        self.assertFalse(transient_error(RuntimeError("400 invalid key")))


if __name__ == "__main__":
    unittest.main()
