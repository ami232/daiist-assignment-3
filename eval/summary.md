# Evaluation summary

## Retrieval (hit rate on answerable questions)

| design | method | hit@1 | hit@3 | hit@5 | all passages@5 | words in prompt |
|---|---|---|---|---|---|---|
| articles | vector | 0.741 | 0.963 | 1.0 | 0.963 | 989 |
| articles | bm25 | 0.037 | 0.037 | 0.037 | 0.037 | 219 |
| articles | hybrid | 0.63 | 0.926 | 1.0 | 0.963 | 1032 |
| fixed200 | vector | 0.667 | 0.926 | 0.963 | 0.889 | 1079 |
| fixed200 | bm25 | 0.037 | 0.037 | 0.074 | 0.074 | 192 |
| fixed200 | hybrid | 0.556 | 0.926 | 0.963 | 0.889 | 1078 |

Agent uses: articles / vector / k=5

## End to end

| result | count |
|---|---|
| correct | 26 |
| incorrect | 1 |
| unsupported | 0 |
| correct refusals | 5 |
| wrong refusals | 0 |
| answered unanswerable | 1 |
| invalid citations | 0 |
| guardrail fired | 0 |

## Judge vs human

- no human labels yet

## Failure hints (confirm each by reading the case)

- retrieval miss: 1
- unsupported claim (answered an unanswerable question): 1

## Cost per question

- 5689 tokens, 6.0 s on average (max 11.7 s), 33 questions
