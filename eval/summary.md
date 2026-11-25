# Evaluation summary

## Retrieval

| design | questions | hit@1 | hit@3 | hit@5 | single hit@5 | multi hit@5 | words top1 | top3 | top5 |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 21 | 19% | 38% | 48% | 62% | 38% | 150 | 447 | 747 |
| section | 21 | 14% | 48% | 67% | 75% | 62% | 161 | 472 | 811 |

The agent searches design `section` with k = 5 (index.CHOSEN_DESIGN, server.TOP_K).

## End to end

| outcome | single | multi | unanswerable | total |
|---|---|---|---|---|
| correct | 7 | 9 | 0 | 16 |
| incorrect | 0 | 3 | 0 | 3 |
| unsupported | 0 | 1 | 0 | 1 |
| wrong refusal | 1 | 0 | 0 | 1 |
| correct refusal | 0 | 0 | 9 | 9 |

- Answers with citations: 20; all citations valid in 20 of them.
- Citation check fired on 0 question(s): none.
- The agent's searches found the expected passage for 18 of 21 answerable questions.

## Cost and latency per question

- Agent: 3.1 model calls, 8,148 input + 216 output tokens, 14.2 s (n = 30, model gemini-3.5-flash-lite).
- Judge: 2,771 tokens (n = 30).

## Judge vs your grades

| | answers | agreement | Cohen's kappa | disagree on |
|---|---|---|---|---|
| correct | 30 | 97% | 0.89 | q28 |
| supported | 30 | 93% | 0.47 | q09, q23 |
