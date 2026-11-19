# Evaluation summary

## Retrieval (answerable questions; a multi question needs every expected passage)

| design | hit@1 | hit@3 | hit@5 |
|---|---|---|---|
| fixed | 42% | 65% | 81% |
| structured | 23% | 69% | 81% |
| structured+filter | 23% | 69% | 81% |

## End to end (32 questions answered)

- Correct (judge): 97%
- Supported by retrieved text (judge): 100%
- Rightly refused (unanswerable questions refused): 6/6
- Made things up (unanswerable but answered): 0/6
- Wrongly refused (answerable but refused): 1/26
- Cited the expected document (answerable, not refused): 25/25
- Guardrail blocked an answer: 1/32

## Cost per question

- Agent tokens: 5068 on average
- Agent time: 10.1 s on average
- Model calls: 2.2, tool calls: 1.3 on average
- Judge tokens: 3025 on average

## Judge vs your grades (22 answers)

- Agreement on correct: 91%
- Agreement on supported: 100%
- Disagreements: q02, q30
