"""Small tests for the two answer guardrails in agent.py (no API calls, no quota).

Run: uv run python tests/test_guardrails.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent import check_citations, check_numbers, citation_valid  # noqa: E402

RETRIEVED = {
    "Reg 2015/2283, Article 11",
    "Reg 432/2012, Annex (Linoleic acid; Live yoghurt cultures; Magnesium)",
    "Reg 1924/2006, Article 10",
}


def test_paragraph_label_matches_retrieved_article():
    assert citation_valid("Reg 2015/2283, Article 11(1)", RETRIEVED)
    assert citation_valid("Reg 1924/2006, Article 10(2)(a)", RETRIEVED)
    assert citation_valid("Reg 1924/2006, Article 10, paragraph 2", RETRIEVED)


def test_still_strict_on_act_and_article():
    assert not citation_valid("Reg 2015/2283, Article 12(1)", RETRIEVED)      # other article
    assert not citation_valid("Reg 2015/2283, Article 1(1)", RETRIEVED)       # 1 is not 11
    assert not citation_valid("Reg 1925/2006, Article 11(1)", RETRIEVED)      # other act


def test_too_general_label_still_fails():
    # a nutrient row was retrieved; citing the whole Annex is too general and must be repaired
    assert not citation_valid("Reg 432/2012, Annex", RETRIEVED)
    assert citation_valid("Reg 432/2012, Annex (Magnesium)", RETRIEVED)
    _, bad = check_citations("Claim ... [Reg 432/2012, Annex].", RETRIEVED)
    assert bad == ["Reg 432/2012, Annex"]


def test_q25_case():
    answer = ("EFSA adopts its opinion within nine months [Reg 2015/2283, Article 11(1)].")
    cites, bad = check_citations(answer, RETRIEVED)
    assert cites == ["Reg 2015/2283, Article 11(1)"] and bad == []


def test_numbers_in_passages_pass():
    passages = "The Authority shall adopt its opinion ... less than 3 mg of monacolins ... x-height of 1,2 mm"
    assert check_numbers("It must be less than 3 mg [Reg 2022/860, Article 1]; x-height 1.2 mm.", passages) == []


def test_number_from_table_row_passes_only_for_that_row():
    passages = "Vitamin C (mg) | 80\nVitamin E (mg) | 12"
    assert check_numbers("The reference value for vitamin C is 80 mg.", passages) == []
    assert check_numbers("For vitamin C, 15 % of the value is 12 mg.", passages) == ["12 mg", "15 %"]


def test_number_not_in_passages_is_flagged():
    passages = "The claim may be used only for food which is at least a source of EPA and DHA."
    assert check_numbers("A source of EPA and DHA means 40 mg per 100 g.", passages) == ["100 g", "40 mg"]
    # a number the user gave in the question is not flagged
    assert check_numbers("Your 40 mg dose is a source of EPA and DHA.", passages, "We have 40 mg per dose") == []


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} tests passed")
