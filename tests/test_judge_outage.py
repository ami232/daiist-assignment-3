"""Judge service failures cannot become grades; saved verdicts resume unchanged."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import evaluate


class JudgeOutageTests(unittest.IsolatedAsyncioTestCase):
    def fixtures(self):
        questions = [{"id": "synthetic", "question": "Synthetic question", "kind": "single",
                      "reference_answer": "Synthetic reference"}]
        answers = {"synthetic": {"question": "Synthetic question", "answer": "Synthetic answer", "trace": []}}
        structured = SimpleNamespace(ainvoke=AsyncMock())
        model = MagicMock()
        model.with_structured_output.return_value = structured
        return questions, answers, structured, model

    async def test_daily_quota_stops_without_short_retries(self):
        questions, answers, structured, model = self.fixtures()
        structured.ainvoke.side_effect = RuntimeError("429 Generate content requests per day limit exceeded")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(evaluate, "EVAL", root), \
                    patch.object(evaluate, "ChatGoogleGenerativeAI", return_value=model), \
                    patch.object(evaluate, "load_api_key", return_value="synthetic-key"), \
                    patch.object(evaluate.asyncio, "sleep", AsyncMock()) as sleep:
                with self.assertRaisesRegex(ValueError, "Daily judge quota exhausted"):
                    await evaluate.grade_answers(questions, answers, root, {}, "synthetic-rubric", "synthetic-model")
                sleep.assert_not_awaited()
            self.assertEqual(structured.ainvoke.await_count, 1)
            self.assertFalse((root / "judge_results.jsonl").exists())

    async def test_repeated_service_failure_is_logged_without_a_grade(self):
        questions, answers, structured, model = self.fixtures()
        structured.ainvoke.side_effect = RuntimeError("503 unavailable")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch.object(evaluate, "EVAL", root), \
                    patch.object(evaluate, "ChatGoogleGenerativeAI", return_value=model), \
                    patch.object(evaluate, "load_api_key", return_value="synthetic-key"), \
                    patch.object(evaluate.asyncio, "sleep", AsyncMock()):
                with self.assertRaisesRegex(ValueError, "completed verdicts are saved"):
                    await evaluate.grade_answers(questions, answers, root, {}, "synthetic-rubric", "synthetic-model")
            self.assertEqual(structured.ainvoke.await_count, 3)
            self.assertFalse((root / "judge_results.jsonl").exists())
            self.assertEqual(len((root / "judge_errors.jsonl").read_text().splitlines()), 3)

    async def test_transient_failure_then_success_is_cached(self):
        questions, answers, structured, model = self.fixtures()
        verdict = evaluate.JudgeVerdict(correct=1, supported=1, refusal="not_applicable", reason="Synthetic explanation")
        structured.ainvoke.side_effect = [RuntimeError("429 quota"), {
            "parsed": verdict, "raw": SimpleNamespace(usage_metadata={"input_tokens": 10,
                "output_tokens": 5, "total_tokens": 15}),
        }]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / "run"
            run.mkdir()
            with patch.object(evaluate, "EVAL", root), \
                    patch.object(evaluate, "ChatGoogleGenerativeAI", return_value=model) as constructor, \
                    patch.object(evaluate, "load_api_key", return_value="synthetic-key"), \
                    patch.object(evaluate.asyncio, "sleep", AsyncMock()):
                first = await evaluate.grade_answers(questions, answers, run, {}, "synthetic-rubric", "synthetic-model")
                resumed = await evaluate.grade_answers(questions, answers, run, {}, "synthetic-rubric", "synthetic-model")
                self.assertEqual(constructor.call_count, 1)
            self.assertEqual(first, resumed)
            self.assertEqual(structured.ainvoke.await_count, 2)
            self.assertEqual(len((run / "judge_results.jsonl").read_text().splitlines()), 1)
            self.assertEqual(json.loads((root / "judge_results.jsonl").read_text())["correct"], 1)


if __name__ == "__main__":
    unittest.main()
