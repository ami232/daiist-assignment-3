# End-to-end evaluation

Agent: `gemini-3.5-flash-lite`, at most 3 searches and 6 model calls per question. Judge: `gemini-3.5-flash-lite` (the API ignores temperature 0 for it, so verdicts are not fully deterministic; they are saved and reused). 32 of 32 questions answered.

## Code checks

| kind | n | citations valid | refusal check passed | expected page retrieved | expected page cited | number warnings |
|---|---|---|---|---|---|---|
| single | 20 | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) | 0 |
| multi | 6 | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) | 1 |
| unanswerable | 6 | 6/6 (100%) | 6/6 (100%) | - | - | 0 |
| all | 32 | 32/32 (100%) | 32/32 (100%) | 26/26 (100%) | 26/26 (100%) | 1 |

A refusal is an answer that starts with "The corpus does not". Of the 6 refusals, 1 use the exact phrase "The corpus does not cover this" asked for in AGENTS.md (format only, not counted as a failure).

Refusals: answered: 26 (q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26); correct refusal: 6 (q27, q28, q29, q30, q31, q32)

Number warnings (numbers in the answer that no retrieved passage contains; computed figures are flagged too): q23 [8]

## Results (judge, all questions)

| kind | n | correct | supported | correct and supported |
|---|---|---|---|---|
| single | 20 | 20/20 (100%) | 20/20 (100%) | 20/20 (100%) |
| multi | 6 | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| unanswerable | 6 | 6/6 (100%) | 6/6 (100%) | 6/6 (100%) |
| all | 32 | 32/32 (100%) | 32/32 (100%) | 32/32 (100%) |

## Results (human grades)

| kind | n | correct | supported |
|---|---|---|---|
| single | 20 | 19/20 (95%) | 20/20 (100%) |
| multi | 6 | 6/6 (100%) | 6/6 (100%) |
| unanswerable | 6 | 6/6 (100%) | 6/6 (100%) |
| all | 32 | 31/32 (97%) | 32/32 (100%) |

## Agreement between the judge and the human grades

| criterion | n | agreement | Cohen's kappa | both 1 | both 0 | human 1, judge 0 | human 0, judge 1 |
|---|---|---|---|---|---|---|---|
| correct | 32 | 31/32 (97%) | 0.00 | 31 | 0 | 0 | 1 |
| supported | 32 | 32/32 (100%) | - | 32 | 0 | 0 | 0 |

Disagreements:

- q13 correct: human 0 (Gives nearly 30% and 25% (1 in 4) for the United Kingdom in 2024 without resolving the discrepancy. Both figures are supported by the retrieved passages.); judge 1 (The answer provides the correct figure of nearly 30% for the UK electric car sales share in 2024, matching the reference answer.)

## Judge on planted wrong answers

Answers written to contain the errors that matter in this use case, judged with the passages their base question retrieved. The expected grades are set by construction: each answer was written to fail in a known way (see DECISIONS.md, section 12).

| id | base | planted error | expected c/s | judge c/s | agrees |
|---|---|---|---|---|---|
| t01 | q30 | wrong country (another country's 2025 share given for Spain) | 0/0 | 0/0 | yes |
| t02 | q13 | wrong year (the 2023 share given for 2024) | 0/0 | 0/0 | yes |
| t03 | q03 | wrong metric (sales growth given as sales share; growth missing) | 0/0 | 0/0 | yes |
| t04 | q04 | forecast given as an actual value | 0/0 | 0/0 | yes |
| t05 | q14 | invented figure | 0/0 | 0/0 | yes |
| t06 | q18 | right figure plus an unsupported claim | 1/0 | 0/0 | no |
| t07 | q31 | missed refusal (the 2025 decline given as the 2026 change) | 0/0 | 0/0 | yes |
| t08 | q09 | partial answer (growth left out) | 0/1 | 0/1 | yes |

correct: agreement 7/8 (88%); expected 0s the judge also gave 0: 7/7 (100%).

supported: agreement 8/8 (100%); expected 0s the judge also gave 0: 7/7 (100%).

Agreement on real answers (human grades) and planted answers (expected grades) together:

| criterion | n | agreement | Cohen's kappa |
|---|---|---|---|
| correct | 40 | 38/40 (95%) | 0.84 |
| supported | 40 | 40/40 (100%) | 1.00 |

## Cost and latency per question

| | mean | median | max |
|---|---|---|---|
| agent seconds | 28 | 29 | 86 |
| agent input tokens | 6,454 | 4,923 | 15,628 |
| agent output tokens | 106 | 98 | 176 |
| agent total tokens | 6,560 | 5,012 | 15,804 |
| model calls | 2 | 2 | 4 |
| searches | 1 | 1 | 3 |
| judge total tokens | 2,285 | 2,112 | 3,447 |
| judge seconds | 29 | 7 | 344 |

Token counts are as reported by the Gemini API (free tier, so no money was spent). Agent seconds include waiting for the free-tier rate limit (12 requests a minute shared by 3 questions asked at the same time), so they overstate the latency of a single question.

## Answers to look at (any check, judge verdict or human grade is 0)

| id | kind | status | expected retrieved | expected cited | judge c/s | human c/s | number warnings |
|---|---|---|---|---|---|---|---|
| q13 | single | answered | 1/1 | 1/1 | 1/1 | 0/1 | - |
