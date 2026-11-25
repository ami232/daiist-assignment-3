# Evaluation summary

35 answers (28 answerable, 7 unanswerable), 35 judged, 26 graded by hand.

## Code checks

- Correct refusals (unanswerable refused): 7/7
- Wrong refusals (answerable refused): 0/28
- Answers with every quote verbatim in the retrieved text: 35/35 (106 quotes)
- Answers with every citation pointing to a retrieved passage: 35/35
- Answerable answers with no citation: 0
- Answers flagged by the quote guardrail: 0; guardrail asked for a rewrite: 3
- Expected passage(s) retrieved by the agent: 24/28 (at least one: 27)

## LLM judge

- Answerable, correct: 28/28
- Answerable, unsupported (a claim not in the retrieved text): 0/28
- Unanswerable, correct refusal: 7/7
- All answers, correct and supported: 35/35

## Judge vs human

- correct: agree on 25/26 (96%), Cohen's kappa 0.0
- supported: agree on 22/26 (85%), Cohen's kappa 0.0
- Disagreements: q25 (human 1/0, judge 1/1), q28 (human 0/1, judge 1/1), q29 (human 1/0, judge 1/1), q32 (human 1/0, judge 1/1), q33 (human 1/0, judge 1/1)

## Failures (suggested cause)


## Cost per question

- Tokens: mean 4,883 (input 4,680, output 203), max 17,025
- Seconds: median 7.9, mean 16.5, max 113.4
- Model calls: mean 2.2; searches: mean 1.3
- Judge tokens per answer: mean 2,285
