# Evaluation summary

Agent model: `gemini-3.5-flash-lite` · judge: `gemini-3-flash-preview, gemini-3.8-flash` (fallback order) · embeddings: `gemini-embedding-2` (768 d) · design served: `articles`

## Retrieval (answerable questions)

| design | hit@1 | hit@3 | hit@5 | all passages@5 (multi) | words in prompt @5 |
|---|---|---|---|---|---|
| articles | 0.793 | 1.0 | 1.0 | 0.931 | 1427 |
| fixed200 | 0.759 | 0.897 | 1.0 | 0.862 | 1074 |

## End to end (35 questions: 29 answerable, 6 unanswerable)

| metric | value |
|---|---|
| judged correct | 4/4 |
| judged supported | 4/4 |
| correct refusals (code) | 6/6 |
| answered an unanswerable question (code) | 0/6 |
| wrong refusals (code) | 1/29 |
| citations valid (code) | 35/35 |
| expected passage retrieved by the agent (code) | 29/29 |
| expected passage cited (code) | 28/29 |
| citation guard retried / blocked | 0 / 0 |
| mean tokens per question | 6429 |
| mean seconds per question | 46.5 |

## Suggested failure causes (check each by hand)

- **not judged** (31): q01, q04, q05, q07, q08, q09, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q28, q29, q30, q31, q32, q33, q34, q35

## Judge vs human

- eval/human_labels.csv has no grades yet.
