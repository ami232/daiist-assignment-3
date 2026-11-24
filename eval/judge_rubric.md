# Judge rubric

Return two independent verdicts: `correct` and `supported`.

- `correct`: The answer conveys all key facts in the reference answer without
  contradicting them. A paraphrase or extra accurate detail is acceptable.
  Required numbers, limits, units, and conditions must be present and accurate;
  omitting a required number is incorrect. For a multi-part question, every
  requested part must be answered correctly; a partly correct answer is
  incorrect. For an unanswerable question, a clear refusal that says the corpus
  does not cover it is correct; guessing is not.
- `supported`: Every factual or advisory claim in the answer is explicitly
  supported by the retrieved passages, and its citation points to the passage
  that supports it. A citation that is missing, invalid, or points to an
  unrelated passage fails this verdict. Extra advice not stated or entailed by
  the retrieved passages also fails, even if it is sensible or likely true.
  Exception: a generic reminder to check current official sources or consult
  an instructor for a real flight is not a factual claim and does not fail
  `supported`.
