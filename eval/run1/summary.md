# Evaluation summary

## Retrieval (answerable questions)

| design | hit@1 | hit@3 | hit@5 | single hit@5 | multi hit@5 | words added (top 5) |
|---|---|---|---|---|---|---|
| fixed | 0.41 | 0.62 | 0.75 | 0.84 | 0.43 | 1527 |
| article | 0.56 | 0.78 | 0.91 | 0.96 | 0.71 | 1019 |
| article_hybrid | 0.31 | 0.47 | 0.59 | 0.68 | 0.29 | 1153 |
| article_routed | 0.56 | 0.78 | 0.91 | 0.96 | 0.71 | 1019 |

Served design: article_routed. Answerable questions: 32.

## End to end

- Questions: 40 (32 answerable, 8 unanswerable)
- Correct (judge): 25/32 answerable
- Unsupported answers (judge): 0/40
- Correct refusals: 6/8 unanswerable
- Wrong refusals: 2/32 answerable
- Citations all valid: 40/40; guardrail fired on 2
- Expected article retrieved by the agent: 31/32; cited: 27/32

## Judge vs human

- Graded by hand: 0
- No human labels yet


## Failures (first guess by code)

- wrong answer from the right passage: 4
- wrong refusal: 2
- answered an unanswerable question (unsupported claim): 2
- retrieval miss: 1

## Cost per question

- Mean 4235 input + 138 output tokens, 1.2 tool calls
- Mean 7.2 s, max 48.8 s
