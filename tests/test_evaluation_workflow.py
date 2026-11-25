import csv
from contextlib import redirect_stderr
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import numpy as np

import evaluate
from evaluation_support import (answer_review_hash, code_checks, compare_labels,
    corpus_fingerprint, load_human_labels, verify_human_binding)
from index import chunk_sections
from retrieval import DIMENSIONS, Store
from retrieval_evaluation import FIELDS


def answer():
    return {"question": "Synthetic question", "answer": "Synthetic answer [book | 1]",
            "guardrail_blocked": False, "draft": {"status": "supported"},
            "trace": [{"tool": "search", "status": "success", "result": {"results": [
                {"id": "fixture", "source": "book", "location": "1", "citation": "[book | 1]", "text": "Synthetic evidence"}]}}]}


class EvaluationTests(unittest.TestCase):
    def test_correctness_and_support_are_compared_separately(self):
        human = {"q": {"correct": 1, "supported": 0}}
        judge = {"q": {"correct": 1, "supported": 1}}
        result = compare_labels(human, judge)
        self.assertEqual(result["correct_agreement"], 1)
        self.assertEqual(result["supported_agreement"], 0)
        self.assertEqual(result["both_fields_agreement"], 0)

    def test_no_overlap_is_unknown_not_zero_agreement(self):
        self.assertIsNone(compare_labels({}, {})["correct_agreement"])

    def test_blank_grades_do_not_count_as_human_review(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"labels.csv"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["id", "correct", "supported", "notes"])
                writer.writeheader()
                writer.writerow({"id": "q1", "correct": "", "supported": "", "notes": ""})
            with self.assertRaisesRegex(ValueError, "own 0/1 grades"):
                load_human_labels(path, {"q1"}, minimum=1)

    def test_negative_human_grade_needs_explanation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"labels.csv"
            path.write_text("id,correct,supported,notes\nq1,0,1,\n")
            with self.assertRaisesRegex(ValueError, "explain every zero"):
                load_human_labels(path, {"q1"}, minimum=1)

    def test_binding_detects_changed_displayed_answer_or_evidence(self):
        record = answer()
        binding = {"labels_sha256": "labels", "rubric_sha256": "rubric",
                   "reviewed_answers": {"q1": answer_review_hash(record)}}
        verify_human_binding(binding, {"q1": {}}, {"q1": record}, "rubric", "labels")
        record["trace"][0]["result"]["results"][0]["text"] = "Different evidence"
        with self.assertRaisesRegex(ValueError, "not bound"):
            verify_human_binding(binding, {"q1": {}}, {"q1": record}, "rubric", "labels")

    def test_query_cache_does_not_change_corpus_fingerprint(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory)/"test.sqlite3")
            before = corpus_fingerprint(store)
            vector = np.zeros(DIMENSIONS)
            vector[0] = 1
            store.save_vector("query-cache", vector, "query")
            self.assertEqual(before, corpus_fingerprint(store))
            chunks = chunk_sections([{"source": "fixture", "document_title": "Fixture", "section_title": "Section",
                "location": "1", "url": "https://example.test", "license": "Synthetic fixture", "text": "Synthetic passage"}])
            store.put_document("fixture", "bytes", "Fixture", chunks)
            self.assertNotEqual(before, corpus_fingerprint(store))
            unembedded = corpus_fingerprint(store)
            store.save_vector(chunks[0]["embedding_key"], vector, "document")
            self.assertNotEqual(unembedded, corpus_fingerprint(store))

    def test_judge_never_receives_human_grades_or_discarded_drafts(self):
        record = answer()
        record["human_grade"] = "secret_human_grade"
        record["draft"] = {"discarded": "secret_discarded_draft"}
        question = {"question": "Synthetic", "kind": "single", "reference_answer": "Reference"}
        payload = json.dumps(evaluate.judge_payload(question, record))
        self.assertNotIn("secret_human_grade", payload)
        self.assertNotIn("secret_discarded_draft", payload)

    def test_discarded_invalid_claim_is_not_counted_as_displayed(self):
        record = answer()
        record["answer"] = "I could not produce a verified cited answer."
        record["guardrail_blocked"] = True
        record["draft"] = {"status": "supported", "invalid_citation": "[invented | 99]"}
        checks = code_checks(record)
        self.assertTrue(checks["citation_identity_valid"])
        self.assertTrue(checks["guardrail_blocked"])


class EvaluationStagingTests(unittest.IsolatedAsyncioTestCase):
    async def test_incomplete_questions_stop_before_retrieval_or_model_calls(self):
        args = SimpleNamespace(retrieval_only=False, answers_only=False, bind_human_labels=False, design=None)
        with patch.object(evaluate, "Store"), \
             patch.object(evaluate, "load_questions", side_effect=ValueError("Incomplete student questions")), \
             patch.object(evaluate, "prepare_retrieval") as retrieval, \
             patch.object(evaluate, "generate_answers", new_callable=AsyncMock) as agent, \
             patch.object(evaluate, "grade_answers", new_callable=AsyncMock) as judge:
            with self.assertRaisesRegex(ValueError, "Incomplete student questions"):
                await evaluate.evaluate(args)
            retrieval.assert_not_called()
            agent.assert_not_called()
            judge.assert_not_called()

    async def test_full_staged_workflow_is_blind_and_resumable_with_synthetic_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            eval_dir = root/"eval"
            eval_dir.mkdir()
            questions_path, human_path, rubric_path = (eval_dir/name for name in ("questions.csv", "human_labels.csv", "judge_rubric.json"))
            store = Store(root/"index.sqlite3")
            chunks = chunk_sections([{"source": "fixture", "document_title": "Fixture", "section_title": f"Section {i}",
                "location": str(i), "url": "https://example.test", "license": "Synthetic fixture", "text": "Synthetic evidence"} for i in (1, 2)])
            store.put_document("fixture", "synthetic", "Fixture", chunks)
            vector = np.zeros(DIMENSIONS)
            vector[0] = 1
            for chunk in chunks:
                store.save_vector(chunk["embedding_key"], vector, "document")
            questions = []
            for i in range(30):
                kind = "single" if i < 20 else "multi" if i < 25 else "unanswerable"
                questions.append({"id": f"q{i+1:02}", "question": f"Synthetic question {i+1}", "kind": kind,
                    "expected_source": "" if kind == "unanswerable" else "fixture",
                    "expected_location": "" if kind == "unanswerable" else "1@0:2;2@0:2" if kind == "multi" else "1@0:2",
                    "reference_answer": "Synthetic reference"})
            with questions_path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(questions)
            human_path.write_text("id,correct,supported,notes\n")
            rubric_path.write_text(json.dumps({"scoring_policy": "Synthetic independent scores"}))
            (root/"project_config.json").write_text(json.dumps({"agent_model": "synthetic-model", "selected_retrieval_design": "dense"}))
            for name in ("AGENTS.md", "agent.py", "answer_guardrails.py", "retrieval.py", "server.py"):
                (root/name).write_text("Synthetic behavior fixture")
            passages = [{**c, "citation": f"[{c['source']} | {c['location']}]",
                         "passage_location": f"{c['location']}@{c['word_start']}:{c['word_end']}"} for c in chunks]
            agent_calls, judge_calls = [], []
            async def fake_agent(question, **kwargs):
                agent_calls.append(question)
                unanswered = int(question.rsplit(" ", 1)[-1]) > 25
                return {"question": question, "answer": "Synthetic missing information" if unanswered else "Synthetic answer [fixture | 1]",
                    "trace": [{"tool": "search", "status": "success", "result": {"results": passages}}],
                    "draft": {"status": "unanswerable" if unanswered else "supported"}, "guardrail_blocked": False,
                    "usage_complete": True, "usage": {"input_tokens": 5, "output_tokens": 2, "total_tokens": 7}, "seconds": 0.01}
            class FakeJudge:
                def with_structured_output(self, *args, **kwargs):
                    return self
                async def ainvoke(self, messages):
                    payload = json.loads(messages[-1].content)
                    judge_calls.append(payload)
                    return {"parsed": evaluate.JudgeVerdict(correct=1, supported=1,
                        refusal="correct" if payload["kind"] == "unanswerable" else "not_applicable", reason="Synthetic verdict"),
                        "raw": SimpleNamespace(usage_metadata={"input_tokens": 5, "output_tokens": 2, "total_tokens": 7})}
            args = SimpleNamespace(retrieval_only=False, answers_only=True, bind_human_labels=False, design=None)
            with patch.multiple(evaluate, ROOT=root, EVAL=eval_dir, QUESTIONS=questions_path, HUMAN=human_path, RUBRIC=rubric_path), \
                 patch.object(evaluate, "Store", return_value=store), \
                 patch.object(evaluate, "prepare_retrieval", return_value={"metrics": []}), \
                 patch.object(evaluate, "run_agent", side_effect=fake_agent), \
                 patch.object(evaluate, "load_api_key", return_value="synthetic-key"), \
                 patch.object(evaluate, "ChatGoogleGenerativeAI", return_value=FakeJudge()), redirect_stderr(io.StringIO()):
                result = await evaluate.evaluate(args)
                self.assertEqual(result["status"], "answers_ready_for_blind_human_review")
                self.assertEqual(len(agent_calls), 30)
                self.assertEqual(judge_calls, [])
                args.answers_only = False
                with self.assertRaisesRegex(ValueError, "Human review is incomplete"):
                    await evaluate.evaluate(args)
                self.assertEqual(judge_calls, [])
                with human_path.open("a") as stream:
                    for q in questions[:20]:
                        stream.write(f"{q['id']},1,1,\n")
                args.bind_human_labels = True
                bound = await evaluate.evaluate(args)
                self.assertEqual(bound["graded_answers"], 20)
                self.assertEqual(judge_calls, [])
                args.bind_human_labels = False
                summary = await evaluate.evaluate(args)
                self.assertEqual(summary["reliable"], 30)
                self.assertEqual(summary["human_judge_agreement"]["correct_agreement"], 1)
                self.assertEqual(len(judge_calls), 30)
                await evaluate.evaluate(args)
                self.assertEqual(len(judge_calls), 30)
                self.assertEqual(len(agent_calls), 30)
                self.assertTrue(all("human" not in payload for payload in judge_calls))


if __name__ == "__main__":
    unittest.main()
