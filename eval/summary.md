# Evaluation summary

## Retrieval (answerable questions)

| design | hit@1 | hit@3 | hit@5 | single hit@5 | multi hit@5 | words added (top 5) |
|---|---|---|---|---|---|---|
| fixed | 0.41 | 0.62 | 0.75 | 0.84 | 0.43 | 1527 |
| article | 0.56 | 0.78 | 0.91 | 0.96 | 0.71 | 1019 |
| article_hybrid | 0.31 | 0.47 | 0.59 | 0.68 | 0.29 | 1153 |
| article_bm25 | 0.16 | 0.22 | 0.25 | 0.32 | 0.00 | 1186 |
| article_routed | 0.56 | 0.78 | 0.91 | 0.96 | 0.71 | 1019 |

Served design: article. Answerable questions: 32.

## End to end

- Questions: 40 (32 answerable, 8 unanswerable)
- Correct (judge): 29/32 answerable
- Unsupported answers (judge): 2/40
- Correct refusals: 7/8 unanswerable
- Wrong refusals: 1/32 answerable
- Citations all valid: 40/40; guardrail fired on 1
- Expected article retrieved by the agent: 31/32; cited: 29/32

## Judge vs human

- Graded by hand: 20
- Agreement on correct: 16/20
- Agreement on supported: 19/20

## Failures (first guess by code)

- wrong answer from the right passage: 1
- wrong refusal: 1
- retrieval miss: 1
- answered an unanswerable question (unsupported claim): 1

## Cost per question

- Mean 5354 input + 143 output tokens, 1.4 tool calls
- Mean 7.2 s, max 45.5 s
