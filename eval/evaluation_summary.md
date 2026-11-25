# End-to-end evaluation

2/2 questions answered by the agent (0 not run or failed, see eval/agent_errors.csv); 0 judged.

## Results (judge)

| Group | n | Correct (2) | Partial (1) | Wrong (0) | Fully supported |
|---|---|---|---|---|---|

## Code checks

- Correct refusals (unanswerable refused or withheld): 0/0
- Wrong refusals (answerable refused or withheld): 0/2
- Answers using the exact refusal sentence: 0
- Guardrail fired: 0 
- Citations: 5 total; invalid document 0 answers; invalid section 0; cited but not retrieved 0
- Answers with uncited factual sentences (heuristic): 0
- Expected passage retrieved by the agent's own searches: 2/2

## Failures (automatic proposal, review in eval/failure_analysis.csv)

- retrieval miss: 0 
- wrong answer from the right passage: 0 
- unsupported claim: 0 
- wrong refusal: 0 
- bad test question: 0 
- flagged by the judge as possible bad test questions: none

## Cost and latency per question (actual API usage metadata)

| | mean | median |
|---|---|---|
| input tokens | 4322 | 4322 |
| output tokens | 257 | 257 |
| total tokens | 4578 | 4578 |
| seconds | 299.5 | 299.5 |
| model calls | 2.0 | 2 |
| searches | 1.0 | 1 |

- Answers produced by a fallback model: 1/2 (gemini-3.8-flash)
- Failed agent runs recorded: 0
- Judge: 0 new calls this run, 0 input / 0 output tokens, 0s (cached verdicts cost nothing)
- Seconds are wall-clock and include free-tier retries and fallbacks. No money cost is reported: the free tier is not billed.

## Agreement with your grades

Pending: grade the answers in eval/human_grading_sheet.csv without opening judge_results.csv, then copy id/correct/supported/notes into eval/human_labels.csv.
