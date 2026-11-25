"""Provider outages must not become a completed blind-review answer set."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

import evaluate


class OutageTests(unittest.IsolatedAsyncioTestCase):
    async def test_network_failure_is_not_a_completed_answer(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            question = {"id": "synthetic", "question": "Synthetic question"}
            outage = {"primary_runtime_error": "ClientConnectorDNSError",
                      "primary_runtime_error_detail": "Cannot connect to host",
                      "draft": None, "guardrail_blocked": True}
            with patch.object(evaluate, "run_agent", AsyncMock(return_value=outage)):
                with self.assertRaisesRegex(ValueError, "no answer was finalised"):
                    await evaluate.generate_answers([question], directory, "dense", "2026-11-24")
            self.assertFalse((directory / "answers.jsonl").exists())
            self.assertTrue((directory / "generation_errors.jsonl").exists())

    async def test_outage_is_preserved_and_resume_retries_same_question(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / "run"
            directory.mkdir()
            questions = [{"id": "synthetic", "question": "Synthetic question", "reference_answer": "Synthetic reference"}]
            outage = {"primary_runtime_error": "GoogleAPIError", "primary_runtime_error_detail": "503 high demand",
                      "trace": [{"tool": "search", "status": "success"}], "usage": {"reported_model_calls": 0},
                      "draft": None, "guardrail_blocked": True, "answer": "Synthetic technical fallback"}
            with patch.object(evaluate, "run_agent", AsyncMock(return_value=outage)) as call:
                with self.assertRaisesRegex(ValueError, "no answer was finalised"):
                    await evaluate.generate_answers(questions, directory, "dense", "2026-11-24")
                self.assertEqual(call.await_count, 1)
            self.assertFalse((directory / "answers.jsonl").exists())
            saved = json.loads((directory / "generation_errors.jsonl").read_text())
            self.assertEqual(saved["id"], "synthetic")
            valid = {"question": "Synthetic question", "answer": "Synthetic answer", "trace": []}
            with patch.object(evaluate, "EVAL", root), patch.object(evaluate, "run_agent", AsyncMock(return_value=valid)) as call, \
                    patch.object(evaluate, "code_checks", return_value={}), patch.object(evaluate, "answer_review_hash", return_value="synthetic-hash"):
                answers = await evaluate.generate_answers(questions, directory, "dense", "2026-11-24")
                self.assertEqual(call.await_count, 1)
                self.assertEqual(answers["synthetic"]["answer"], "Synthetic answer")
            self.assertTrue((root / "human_review.json").exists())


if __name__ == "__main__":
    unittest.main()
