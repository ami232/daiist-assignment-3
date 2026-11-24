"""The harness's citation check and refusal detection in agent.py. Offline."""

import agent

PASSAGES = [("Reg 2019/947", "UAS.OPEN.010 General provisions"), ("Reg 2019/947", "Article 14")]


def test_a_citation_that_matches_a_returned_passage_passes():
    assert agent.check_citations("Max 120 m [Reg 2019/947, UAS.OPEN.010 General provisions].", PASSAGES) == []


def test_a_shorter_location_matches_at_a_word_boundary():
    assert agent.check_citations("Max 120 m [Reg 2019/947, UAS.OPEN.010].", PASSAGES) == []


def test_passage_numbers_finer_locations_and_wrong_sources_fail():
    assert agent.check_citations("Max 120 m [1, 3].", PASSAGES)
    assert agent.check_citations("Register [Reg 2019/947, Article 14(5)(a)(i)].", PASSAGES)
    assert agent.check_citations("Register [Reg 2019/945, Article 14].", PASSAGES)


def test_an_answer_without_citations_fails():
    assert agent.check_citations("You need to register.", PASSAGES) == ["the answer has no [source, location] citations"]


def test_a_refusal_needs_no_citation():
    assert agent.check_citations("The corpus does not cover this.", []) == []


def test_citations_merged_in_one_bracket_are_checked_one_by_one():
    assert agent.check_citations("120 m [Reg 2019/947, UAS.OPEN.010; Reg 2019/947, Article 14].", PASSAGES) == []
    problems = agent.check_citations("120 m [Reg 2019/947, UAS.OPEN.010; Reg 2019/947, Article 99].", PASSAGES)
    assert len(problems) == 1 and "Article 99" in problems[0]


def test_refusal_detection_is_the_exact_prefix():
    assert "The corpus does not cover this.".startswith(agent.REFUSED_PREFIX)
    assert "The corpus does not cover the specific fines.".startswith(agent.REFUSED_PREFIX)
    # q32: a refusal in other words is not detected; REPORT.md discusses this case
    assert not "The corpus does not specify a set number of days.".startswith(agent.REFUSED_PREFIX)


def test_passages_in_reads_both_search_result_formats():
    v1 = "[1] Reg 2019/947, UAS.OPEN.010 General provisions (score 0.829)\n(1) text"
    v2 = ("Passage 1 (score 0.829). Cite as: [Reg 2019/947, UAS.OPEN.010 General provisions]. "
          "Version: consolidated text of 4 April 2022.\n(1) text")
    expected = [("Reg 2019/947", "UAS.OPEN.010 General provisions")]
    assert agent.passages_in(v1) == expected
    assert agent.passages_in(v2) == expected
