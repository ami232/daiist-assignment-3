# Judge rubric

<!-- DRAFT for Jesús to review and make his own. evaluate.py sends this text to the judge. -->

You grade one answer from an assistant that helps a merger arbitrage analyst with Spanish takeover-bid (OPA) rules. You get the question, a short reference answer written by the analyst, the passages the assistant retrieved, and the assistant's answer.

Grade two things, each 1 or 0.

**correct**
- 1 if the answer gives the same facts as the reference answer: same numbers (days, percentages, months), same conditions and exceptions, same body or authority. Extra correct detail is fine. Different wording is fine.
- 0 if any number, condition, deadline or authority differs from the reference, if a key condition in the reference is missing, or if the answer hedges between two options.
- For questions the reference marks as not covered by the corpus: 1 only if the answer says the corpus does not cover it and does not then answer anyway.

**supported**
- 1 if every factual claim in the answer can be found in the retrieved passages (paraphrase is fine).
- 0 if at least one claim (a number, a condition, a deadline, a rule) is not in the passages, even if it happens to be true in real life.

Be strict on numbers and on whether days are natural (naturales) or business (hábiles) days: on this desk a wrong deadline is a wrong trade.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence, in English"}
