# Evaluation summary

## Retrieval (answerable questions)

| design | hit@1 | hit@3 | hit@5 | multi: both found @5 | words added (k=5) |
|---|---|---|---|---|---|
| dense | 0.625 | 0.969 | 1.0 | 3/6 | 1122 |
| bm25 | 0.375 | 0.531 | 0.562 | 1/6 | 1031 |
| hybrid | 0.531 | 0.656 | 0.781 | 1/6 | 1145 |
| hybrid_articles_only | 0.625 | 0.844 | 0.938 | 2/6 | 1344 |

## End to end

- Correct on answerable questions (judge): 32/32
- Correct refusals on unanswerable questions: 6/6
- Answered an unanswerable question: 0/6
- Wrong refusals on answerable questions: 0/32
- Answers with an unsupported claim (judge): 1/38
- Answers with an invalid citation: 1
- Citation guardrail fired: 1
- Average per question: 4433 tokens, 7.4 s, about $0.00187 at paid-tier prices

## Failures by cause

- unsupported claim: 1

## Judge vs your labels

- correct: 91% agreement on 22 answers (Cohen's kappa 0.0); disagree on q18, q28
- supported: 96% agreement on 22 answers (Cohen's kappa 0.0); disagree on q30
