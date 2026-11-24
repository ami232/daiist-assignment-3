# Judge rubric

The judge grades one agent answer at a time. It sees the question, its kind (single / multi / unanswerable), the reference answer, the passages the agent retrieved, and the agent's answer. It gives two binary scores, the same two the human labels use, each with a one- or two-sentence reason.

## correct (1 / 0)

**Answerable questions (single, multi)**
- **1** if the answer states every element of the reference answer and contains nothing that contradicts it. Different wording is fine. Extra information is fine as long as it is not wrong.
- **0** if any element of the reference is missing (partial answers score 0), if anything contradicts the reference, or if the agent refused to answer (wrong refusal).
  - For a `multi` question this means both passages' content must be present.
  - A missing condition or exception that the reference mentions counts as a missing element.

**Unanswerable questions**
- **1** if the agent clearly says the indexed legislation does not cover the question. It may add which kind of source would (national law, another EU act, a lawyer), but it must not present an answer as if the corpus supported it.
- **0** if the agent gives a substantive answer to the question as if it were covered, for example an obligation, deadline or amount taken from a nearby passage on a different situation.

## supported (1 / 0)

- **1** if every factual or legal claim in the answer is stated in the retrieved passages. Paraphrase is allowed; inference beyond what the text says is not.
- **0** if at least one claim is not in the retrieved passages, even if it is true in real life, and even if the rest of the answer is right.
- A pure refusal makes no legal claims and scores **1**. General advice such as "consult a lawyer" or "check national law" is not a claim.
- Citations count as claims: a citation to a passage that does not say what the answer attributes to it makes the answer unsupported.

## Notes for the judge
- Judge only against the reference answer and the retrieved passages, not against your own knowledge of EU law.
- When unsure between 1 and 0, choose 0 and explain why in the reason.
