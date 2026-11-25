"""Guardrails through real create_agent and middleware; the model is a scripted fake."""

import asyncio
import unittest
from unittest import mock

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import tool

import agent

PASSAGE_ID = "32004R0261:B:article-7:1"
CALLS = []


@tool
def search(query: str) -> str:
    """Stand-in for the MCP search tool."""
    CALLS.append(("search", query))
    return f"[{PASSAGE_ID}] Regulation (EC) No 261/2004 (legislation; Original text)\nLocation: Article 7\nEUR 250 ..."


@tool
def add_document(path: str) -> str:
    """Stand-in for the MCP add_document tool: records that it ran."""
    CALLS.append(("add_document", path))
    return "Added."


class ScriptedModel(GenericFakeChatModel):
    """A chat model that replays fixed messages and accepts tools, like a real one."""

    def bind_tools(self, tools, **kwargs):
        return self


def scripted(*messages):
    return ScriptedModel(messages=iter(messages))


def call(name, args, n=1):
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": f"call-{n}"}])


def run(model, question="q", approve=agent.deny_all, limit=agent.MODEL_CALL_LIMIT):
    built = agent.build_agent([search, add_document], approve=approve, model_call_limit=limit, model=model)
    return asyncio.run(agent.ask(built, question))


class TestApproval(unittest.TestCase):
    def setUp(self):
        CALLS.clear()

    def test_denied_add_document_never_runs(self):
        result = run(scripted(call("add_document", {"path": "corpus/holdout/32011R0181.html"}),
                              AIMessage(content="NOT IN CORPUS: the file was not added.")))
        self.assertNotIn("add_document", [name for name, _ in CALLS])
        self.assertTrue(result["guardrails"]["add_document_denied"])

    def test_approved_add_document_runs(self):
        run(scripted(call("add_document", {"path": "x.html"}), AIMessage(content="NOT IN CORPUS: done.")),
            approve=lambda c: True)
        self.assertEqual(CALLS, [("add_document", "x.html")])

    def test_no_terminal_means_denied(self):
        with mock.patch("sys.stdin") as stdin:
            stdin.isatty.return_value = False
            self.assertFalse(agent.ask_person({"args": {"path": "corpus/holdout/32011R0181.html"}}))

    def test_anything_but_y_means_denied(self):
        with mock.patch("sys.stdin") as stdin, mock.patch("builtins.input", return_value="yes please"):
            stdin.isatty.return_value = True
            self.assertFalse(agent.ask_person({"args": {"path": "x.html"}}))
        with mock.patch("sys.stdin") as stdin, mock.patch("builtins.input", side_effect=EOFError):
            stdin.isatty.return_value = True
            self.assertFalse(agent.ask_person({"args": {"path": "x.html"}}))

    def test_search_needs_no_approval(self):
        run(scripted(call("search", {"query": "compensation"}), AIMessage(content=f"EUR 250 [{PASSAGE_ID}]")),
            approve=lambda c: self.fail("search must not ask for approval"))
        self.assertEqual(CALLS[0][0], "search")


class TestModelCallLimit(unittest.TestCase):
    def test_runaway_loop_is_stopped(self):
        endless = [call("search", {"query": f"try {n}"}, n) for n in range(20)]
        result = run(scripted(*endless), limit=3)
        self.assertTrue(result["guardrails"]["model_call_limit_hit"])
        self.assertEqual(result["model_calls"], 4)  # 3 real model calls + the limit's closing message
        self.assertTrue(result["answer"].startswith("WITHHELD"))  # and it never reaches the user as an answer


class TestCitationCheck(unittest.TestCase):
    def test_cited_and_retrieved_passes(self):
        result = run(scripted(call("search", {"query": "compensation"}), AIMessage(content=f"EUR 250 [{PASSAGE_ID}].")))
        self.assertTrue(result["guardrails"]["citation_check"]["passed"])
        self.assertEqual(result["answer"], f"EUR 250 [{PASSAGE_ID}].")

    def test_invented_citation_is_withheld(self):
        result = run(scripted(call("search", {"query": "compensation"}),
                              AIMessage(content="EUR 600 [32004R0261:B:article-99:1].")))
        self.assertFalse(result["guardrails"]["citation_check"]["passed"])
        self.assertTrue(result["answer"].startswith("WITHHELD"))
        self.assertIn("EUR 600", result["raw_answer"])  # kept for evaluation, never shown

    def test_uncited_claim_is_withheld_but_marker_reply_is_not(self):
        self.assertFalse(agent.check_citations("You get EUR 250.", {})[0])
        self.assertTrue(agent.check_citations("NOT IN CORPUS: bus rights are not covered.", {})[0])
        self.assertTrue(agent.check_citations("NEED DETAILS: how long was the flight?", {})[0])


class TestCitationParsing(unittest.TestCase):
    """Cases found in the evaluation, where the first single-id pattern skipped citations instead of checking them."""

    RETURNED = {"32004R0261:A:w011:1": "...", "52024XC05687:A:w016:1": "...", "32004R0261:A:w016:1": "..."}

    def test_several_ids_in_one_bracket_are_all_read(self):  # q06 was withheld as "no citations"
        answer = "It applies to frequent-flyer tickets [32004R0261:A:w011:1, 52024XC05687:A:w016:1]."
        self.assertEqual(agent.extract_citations(answer), ["32004R0261:A:w011:1", "52024XC05687:A:w016:1"])
        self.assertTrue(agent.check_citations(answer, self.RETURNED)[0])

    def test_one_unreturned_id_in_a_shared_bracket_is_caught(self):  # q20: w16:1 next to a real id
        passed, reason = agent.check_citations("EUR 250 [32004R0261:A:w016:1, 32004R0261:A:w16:1].", self.RETURNED)
        self.assertFalse(passed)
        self.assertIn("32004R0261:A:w16:1", reason)

    def test_malformed_ids_are_checked_not_skipped(self):
        for bad in ("[32015R2302]", "[32004R0261:A:article-8]", "[`32004R0261:A:w020:2`]"):  # q27, q11, q03
            with self.subTest(bad=bad):
                self.assertFalse(agent.check_citations(f"Some claim {bad}.", self.RETURNED)[0])

    def test_semicolons_and_backticks(self):
        answer = "Care [`32004R0261:A:w016:1`; `32004R0261:A:w011:1`]."
        self.assertEqual(agent.extract_citations(answer), ["32004R0261:A:w016:1", "32004R0261:A:w011:1"])
        self.assertTrue(agent.check_citations(answer, self.RETURNED)[0])

    def test_ordinary_bracket_text_is_not_a_citation(self):
        self.assertEqual(agent.extract_citations("Signed [signatory] on [date]; reply [y/N]."), [])
        self.assertFalse(agent.check_citations("You get EUR 250 [see Article 7].", self.RETURNED)[0])


if __name__ == "__main__":
    unittest.main()
