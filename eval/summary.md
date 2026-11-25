# Evaluation summary

Generated 2026-11-25 13:21 by `main.py evaluate`. Agent model: `gemini-flash-lite-latest`, judge model: `gemini-flash-lite-latest`. Retrieval used by the agent: design `structure`, method `hybrid`, k = 5.

## Retrieval (answerable questions)

| design | method | hit@1 | hit@3 | hit@5 | multi_both@5 | words@1 | words@3 | words@5 | chunks |
|---|---|---|---|---|---|---|---|---|---|
| fixed | dense | 0.914 | 0.914 | 0.943 | 0.714 | 200 | 599 | 999 | 343 |
| fixed | bm25 | 0.829 | 0.914 | 0.943 | 0.857 | 200 | 600 | 1000 | 343 |
| fixed | hybrid | 0.914 | 0.971 | 0.971 | 0.857 | 200 | 600 | 1000 | 343 |
| structure | dense | 0.914 | 0.943 | 0.971 | 0.571 | 193 | 566 | 964 | 323 |
| structure | bm25 | 0.8 | 0.886 | 0.943 | 0.857 | 199 | 567 | 962 | 323 |
| structure | hybrid | 0.914 | 1.0 | 1.0 | 0.857 | 202 | 588 | 965 | 323 |

## End to end

| metric | value |
|---|---|
| correct (all questions) | 42/42 (100%) |
| correct on answerable | 35/35 (100%) |
| supported (every claim in retrieved text) | 42/42 (100%) |
| unsupported answers | 0/42 (0%) |
| correct refusals (unanswerable refused) | 6/7 (86%) |
| unanswerable judged correct (refused or said not covered) | 7/7 (100%) |
| wrong refusals (answerable refused) | 0/35 (0%) |
| searched before answering | 42/42 (100%) |
| all citations valid | 42/42 (100%) |
| citation guardrail fired | 3/42 (7%) |
| expected passage among agent's retrieved (answerable) | 35/35 (100%) |


### By kind

| kind | n | correct | supported |
|---|---|---|---|
| single | 28 | 28 | 28 |
| multi | 7 | 7 | 7 |
| unanswerable | 7 | 7 | 7 |

## Judge vs. your grades

| field | n | agreement | cohen_kappa |
|---|---|---|---|
| correct | 22 | 91% | 0.0 |
| supported | 22 | 100% | None |


### Disagreements

| id | field | human | judge | human_notes | judge_explanation |
|---|---|---|---|---|---|
| q29 | correct | 0 | 1 | Says Yes, performance fees are allowed for qualified clients, but never states that §205(a)(1) generally prohibits them: misses the key half of the two-part answer although IAA:80b-5#1 was retrieved | The answer correctly and fully addresses both parts of the question, covering the general prohibition/allowance for performance fees and the qualified client requirement, and every factual claim is directly supported by the provided evidence. |
| q34 | correct | 0 | 1 | Only covers the marketing-rule ban on 'reviewed by the SEC'; never answers 'the SEC approved us' (§208(a)) or that stating registration is allowed. 80b-8 was never retrieved: one search only | The assistant correctly states that performance results cannot be advertised as approved or reviewed by the SEC, matching the reference answer and supported by the evidence. |

## Failures by cause

(none)


Details in eval/failures.csv (fill `manual_cause` where the automatic cause is wrong, e.g. `bad test question`).

## Cost per question

| measure | mean | median | max |
|---|---|---|---|
| agent tokens per question (input+output) | 5884 | 4388 | 21647 |
| agent seconds per question | 16.5 | 5.2 | 250.83 |
| judge tokens per judged question | 2373 |  |  |
| searches per question | 1.2 |  | 3 |
