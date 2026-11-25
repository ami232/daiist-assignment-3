# Evaluation summary

Chat model `gemini-3.5-flash-lite`, embeddings `gemini-embedding-2` (768 d), active retrieval `structure` / `dense` / `articles`, top 5.

## Retrieval (answerable questions)

| design | mode | scope | hit@1 | hit@3 | hit@5 | multi: all passages @5 | chunks |
|---|---|---|---|---|---|---|---|
| fixed | dense | all | 0.769 | 0.923 | 0.923 | 0.167 | 458 |
| fixed | dense | articles | 0.885 | 0.923 | 0.923 | 0.667 | 370 |
| fixed | hybrid | all | 0.615 | 0.808 | 0.885 | 0.5 | 458 |
| fixed | hybrid | articles | 0.692 | 0.885 | 0.885 | 0.5 | 370 |
| structure | dense | all | 0.769 | 0.962 | 0.962 | 0.5 | 366 |
| structure | dense | articles | 0.846 | 0.962 | 0.962 | 0.5 | 322 |
| structure | hybrid | all | 0.462 | 0.808 | 0.808 | 0.333 | 366 |
| structure | hybrid | articles | 0.538 | 0.808 | 0.808 | 0.333 | 322 |

## End to end (32 questions graded)

| metric | value |
|---|---|
| correct (judge) | 0.938 |
| supported by retrieved text (judge) | 0.969 |
| answerable: correct | 0.962 |
| answerable: wrongly refused | 0.0 |
| unanswerable: correctly refused (code) | 0.667 |
| made something up (answered an unanswerable, or unsupported claim) | 0.094 |
| all citations valid (code) | 1.0 |
| cited the expected source and location (code, answerable) | 0.962 |
| citation guardrail retried / blocked | 1 / 0 |

## Cost per question (agent)

- input tokens: 4466.47, output tokens: 231.19
- seconds: mean 14.38, max 71.63
- search calls: 1.31
- judge tokens per question: 1989.09

## Judge vs human

Not computed yet: fill in eval/human_labels.csv.

## Failures (eval/failures.csv)

- unsupported claim: 3

Check each row by hand and relabel any that are really a bad test question.
