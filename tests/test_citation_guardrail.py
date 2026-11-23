"""
The citation guardrail of agent.py, tested without any API call.

    uv run python tests/test_citation_guardrail.py

It parses a search result written by hand in server.py's format, then checks
that an answer citing only retrieved passages passes and that an answer with a
citation the search never returned is replaced with a refusal.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent import apply_citation_guardrail, extract_citations, parse_search_results  # noqa: E402

SEARCH_RESULT = """Search results for: who is responsible for maintaining a vehicle
Index: "article" chunks; 2 of 600 stored passages shown, best match first.
To cite a passage, copy its Citation line exactly: [doc_id, location].

=== Result 1 of 2 ===
Citation: [Dir_2016_798, Article 14(3)]
Document: Directive (EU) 2016/798 on railway safety (recast)
Source: https://publications.europa.eu/resource/celex/32016L0798
Similarity: 0.7312
Text:
3. The maintenance system shall be composed of the following functions:
(a) a management function to supervise and coordinate the maintenance functions [note 1]

=== Result 2 of 2 ===
Citation: [Reg_2019_779, Annex II, II(5)-(6)]
Document: Commission Implementing Regulation (EU) 2019/779 on certification of entities in charge of maintenance (ECM)
Source: https://publications.europa.eu/resource/celex/32019R0779
Similarity: 0.6540
Text:
5. To keep the maintenance file updated throughout the lifecycle of a vehicle, the organisation shall have procedures
"""

GOOD = (
    "The maintenance system has four functions, starting with a management function [Dir_2016_798, Article 14(3)]. "
    "The ECM must keep the maintenance file updated [Reg_2019_779, Annex II, II(5)-(6)]."
)
FORGED = (
    "The maintenance system has four functions [Dir_2016_798, Article 14(3)]. "
    "Each vehicle must be inspected every 12 months [Dir_2016_798, Article 99(4)]."
)
MERGED = "Both acts deal with the maintenance file [Dir_2016_798, Article 14(3); Reg_2019_779, Annex II, II(5)-(6)]."
REFUSAL = "The corpus does not cover this question. Check the consolidated act on EUR-Lex."


def main() -> None:
    chunks = parse_search_results(SEARCH_RESULT)
    assert [(c["doc_id"], c["location"]) for c in chunks] == [
        ("Dir_2016_798", "Article 14(3)"),
        ("Reg_2019_779", "Annex II, II(5)-(6)"),
    ], chunks
    assert chunks[0]["score"] == 0.7312 and chunks[0]["text"].endswith("[note 1]")
    print(f"parsed {len(chunks)} passages:", [f"[{c['doc_id']}, {c['location']}]" for c in chunks])

    good = apply_citation_guardrail(GOOD, chunks)
    assert not good["fired"] and good["answer"] == GOOD and len(good["citations"]) == 2
    print("\n1. answer citing only retrieved passages -> passes:", [f"[{c['doc_id']}, {c['location']}]" for c in good["citations"]])

    forged = apply_citation_guardrail(FORGED, chunks)
    assert forged["fired"] and forged["invalid_citations"] == ["[Dir_2016_798, Article 99(4)]"]
    assert "12 months" not in forged["answer"] and forged["citations"] == []
    print("\n2. answer with a forged citation -> guardrail fires")
    print("   invalid :", forged["invalid_citations"])
    print("   answer  :", forged["answer"])

    merged = apply_citation_guardrail(MERGED, chunks)
    assert not merged["fired"] and len(merged["citations"]) == 2
    print("\n3. two retrieved citations in one bracket -> passes")

    nothing = apply_citation_guardrail(GOOD, [])
    assert nothing["fired"] and len(nothing["invalid_citations"]) == 2
    print("\n4. citations but no search was run -> guardrail fires:", nothing["invalid_citations"])

    refusal = apply_citation_guardrail(REFUSAL, chunks)
    assert not refusal["fired"] and refusal["citations"] == []
    print("\n5. a refusal without citations -> passes unchanged")

    assert extract_citations("see [note 1] and [image not extracted]") == []
    print("\n6. '[note 1]' and '[image not extracted]' are not read as citations")
    print("\nAll citation guardrail checks passed.")


if __name__ == "__main__":
    main()
