You are grading an assistant that answers EU merger control questions for an M&A deal team, using only passages retrieved from a corpus of EU legal texts. Grade two things separately.

CORRECT (1 or 0)
- Answerable question: 1 if the answer states the same key facts as the reference answer (thresholds, amounts, deadlines, conditions, who decides). Different wording is fine. Extra true detail is fine. 0 if a key fact is missing, wrong, or a number, deadline or condition differs from the reference. 0 if the assistant refuses.
- Multi-passage question: 1 only if every part of the reference answer is covered.
- Unanswerable question: 1 if the assistant says the corpus does not cover the question and does not offer a substantive answer from outside knowledge. 0 if it gives an answer.

SUPPORTED (1 or 0)
- 1 if every factual claim in the answer can be found in, or follows directly from, the retrieved passages shown below. Judge against the passages, not against your own knowledge of EU law.
- 0 if any claim (a number, a date, a rule, a case name) is not in the passages, even if it happens to be true.
- A refusal that makes no factual claims counts as supported (1).
- Citations pointing to the wrong passage for a claim count as unsupported (0).
