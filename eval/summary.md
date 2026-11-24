# Evaluation summary

Agent model: `gemini-3.5-flash-lite` · judge: `gemini-3-flash-preview, gemini-3.8-flash, gemini-3.5-flash` (fallback order) · embeddings: `gemini-embedding-2` (768 d) · design served: `articles`

## Retrieval (answerable questions)

| design | hit@1 | hit@3 | hit@5 | all expected passages@5 (all answerable) | words in prompt @5 |
|---|---|---|---|---|---|
| articles | 0.759 | 0.966 | 1.0 | 0.931 | 1427 |
| fixed200 | 0.69 | 0.828 | 0.897 | 0.793 | 1070 |

## End to end (35 questions: 29 answerable, 6 unanswerable)

| metric | value |
|---|---|
| judged correct | 34/35 |
| judged supported | 31/35 |
| correct refusals (code) | 6/6 |
| answered an unanswerable question (code) | 0/6 |
| wrong refusals (code) | 0/29 |
| citations valid (code) | 35/35 |
| expected passage retrieved by the agent (code) | 29/29 |
| expected passage cited (code) | 29/29 |
| citation guard retried / blocked | 0 / 0 |
| mean tokens per question | 6427 |
| mean seconds per question | 45.2 |

## Suggested failure causes (check each by hand)

- **unsupported claim** (3): q04, q07, q25
- **unsupported claim (answered an unanswerable question)** (1): q32

## Judge vs human

- **correct**: 95% agreement on 20 answers (Cohen's κ = 0.0); disagreements: q04
- **supported**: 80% agreement on 20 answers (Cohen's κ = 0.0); disagreements: q04, q07, q25, q32
