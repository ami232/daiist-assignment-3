# Judge rubric

You grade one answer from an assistant that helps students renting in Spain, using passages from three laws (LAU, Ley 12/2023 por el derecho a la vivienda, LPH). You get the question, the reference answer written by the evaluator, the passages the assistant's search returned, and the answer. Give two grades, each 1 or 0, and one sentence explaining them.

## correct: is the answer right against the reference?

- **1** if the answer gets the main point of the question right, consistent with the reference answer. Missing a secondary detail that the reference mentions is acceptable.
- **0** if any concrete figure is wrong: a deadline, a number of days, months or years, a percentage, a number of monthly payments, an amount or a voting majority that contradicts the reference. In tenancy law the figure is the answer, so one wrong figure makes the whole answer incorrect, even if the rest is right.
- **0** if it answers a different question, contradicts the reference, or leaves out the main point.
- Questions about an article that is "(Derogado)" or "(Anulado)": **1** only if the answer says so and does not describe what the article used to say.
- Questions marked `unanswerable` (the corpus does not answer them): **1** only if the answer does not claim to answer the part the corpus does not cover and marks it with a line starting "Parte no cubierta por el corpus:". **0** if it gives an answer to the uncovered part.
- Extra correct information that is not in the reference does not lower the grade.

## supported: is every claim in the retrieved passages?

- **1** only if every factual statement in the answer is stated in the retrieved passages.
- **0** if any factual statement is not in the passages, **even if it is true** (for example, something the model knows from memory). The assistant must answer only from what its search returned.
- The line starting "Parte no cubierta por el corpus:" says what is missing; it is not a factual claim, so do not count it.
- Do not grade the citation format: the evaluation checks citations in code.

## reason

One sentence: which fact made `correct` or `supported` 0, or why both are 1.
