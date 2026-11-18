# Evaluation summary (34 questions: 26 answerable, 8 unanswerable)

- Agent `gemini-3.5-flash-lite`, judge `gemini-3-flash-preview`
- Judge: correct 32/34, with unsupported claims 0
- Correct refusals 6/8; wrong refusals 0/26
- Code-check failures: {'guard_repaired': 3, 'refused_as_expected': 2}
- Failures by (automatic) cause: {'wrong answer from right passage': 2, 'unsupported claim': 1, 'unsupported claim (should have refused)': 4}
- Per question: 2.47 model calls, 1.44 tool calls, 6074 input + 220 output tokens, 4.3 s; cost set PRICE_IN_PER_M / PRICE_OUT_PER_M
- Agreement judge vs my labels on 34 answers: correct 94%, supported 91%, both 85%
