# Evaluation summary

## Retrieval (answerable questions)

| design | k | hit rate | multi complete | words in prompt |
|---|---|---|---|---|
| vector | 1 | 0.97 | 0.0 | 198 |
| vector | 3 | 1.0 | 0.333 | 593 |
| vector | 5 | 1.0 | 0.667 | 989 |
| bm25 | 1 | 0.697 | 0.0 | 199 |
| bm25 | 3 | 0.788 | 0.333 | 596 |
| bm25 | 5 | 0.909 | 0.333 | 994 |
| hybrid | 1 | 0.909 | 0.0 | 197 |
| hybrid | 3 | 1.0 | 0.5 | 592 |
| hybrid | 5 | 1.0 | 0.833 | 987 |

## End to end

- questions: 40
- correct: 39
- unsupported: 1
- answerable correct: 33
- answerable: 33
- correct refusals: 7
- unanswerable: 7
- wrong refusals: 0
- answered unanswerable: 0
- invalid citation answers: 0
- answers with numbers not in evidence: 5
- guardrail fired: 2
- expected passage retrieved: 33
- avg seconds: 26.8
- avg input tokens: 6144
- avg output tokens: 131

## Failures by cause

- refused, but added a detail from outside the evidence: 1

## Judge against my grades

- graded answers compared: 24
- agreement on correct: 0.958 (kappa 0.0)
- agreement on supported: 0.958 (kappa 0.647)
- q34 correct: I said 1, judge said 0. Judge: The answer is not supported because it cites section numbers and subparts that do not appear in the evidence.
- q35 supported: I said 0, judge said 1. Judge: The answer correctly identifies that the information is missing from the corpus and properly explains that the noise exposure table is in Subpart D, which is outside the provided text.
