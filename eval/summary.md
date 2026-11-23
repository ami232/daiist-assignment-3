# Evaluation summary

Agent model `gemini-3.5-flash-lite`, design `article` (best by retrieval numbers: `fixed`), judge `gemini-3.1-flash-lite`. Questions answered: 37/37.

## Code checks

- Citations valid: 37/37
- Expected article retrieved: 26/29; cited: 23/29
- Correct refusals: 8/8; wrong refusals: 3/29
- Citation guard fired: 0

## Judge verdicts

- single: correct 17/19, supported 18/19
- multi: correct 8/10, supported 9/10
- unanswerable: correct 8/8, supported 8/8
- all: correct 33/37, supported 35/37
- Unsupported answers: 2

## Agreement with my grades

- Graded by me: 37
- correct: 36/37 agree (kappa 0.874)
- supported: 36/37 agree (kappa 0.654)
- both fields agree: 35/37  (disagreements: eval/judge_disagreements.csv)

## Cost per question

- Input tokens (avg): 5258; output tokens (avg): 186
- Seconds (avg): 8.0; tool calls (avg): 1.2
