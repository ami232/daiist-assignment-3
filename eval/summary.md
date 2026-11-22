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

## Retrieval with the agent's own (Spanish) search queries

| design | method | hit@1 | hit@3 | hit@5 |
|---|---|---|---|---|
| articles | vector | 0.667 | 0.926 | 0.963 |
| articles | bm25 | 0.519 | 0.852 | 0.889 |
| articles | hybrid | 0.778 | 0.926 | 0.926 |
| fixed200 | vector | 0.778 | 0.963 | 0.963 |
| fixed200 | bm25 | 0.519 | 0.815 | 0.926 |
| fixed200 | hybrid | 0.852 | 0.926 | 0.963 |

Agent uses: articles / vector / k=5

## End to end

| result | count |
|---|---|
| correct | 26 |
| incorrect | 1 |
| unsupported | 9 |
| correct refusals | 5 |
| wrong refusals | 0 |
| answered unanswerable | 1 |
| invalid citations | 0 |
| guardrail fired | 0 |

## Judge vs human

- correct: 91% agreement over 33 answers (kappa -0.042); disagree on q06, q10, q25
- supported: 82% agreement over 33 answers (kappa 0.421); disagree on q14, q15, q22, q25, q28, q33

## Failure hints (confirm each by reading the case)

- unsupported claim: 6
- wrong answer from the right passage: 1
- retrieval miss: 1
- unsupported claim (answered an unanswerable question): 1

## Cost per question

- 5703 tokens, 2.7 s on average (max 6.5 s), 33 questions
