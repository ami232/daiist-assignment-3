# How eval/human_labels.csv was graded

**Grader:** Claude (Anthropic), used as a second, independent grader at the student's request. Reviewed by Tomas Lock. The grades were written before the judge (Gemini 3.5 Flash) had produced any verdict, from `eval/grading_sheet.md` only. "Judge vs human agreement" in `eval/summary.json` is therefore agreement between two different AI graders, not between the judge and a person; see REPORT.md.

**Answers graded:** all 38, from the run after the call-limit and refusal fixes.

**Rules applied**

- **correct = 1** if the answer gives the reference answer's key facts: the same numbers, units and conditions, and the specific thing the question asks for. Extra correct detail is fine. Omitting a secondary exception was tolerated when the answer stays on the safe side (q29). For an unanswerable question, 1 only if the answer says the documents do not cover it and presents no rule as the answer.
- **supported = 1** if every factual claim is in the retrieved passages shown in the grading sheet, cited or not. An embellishment beyond the passage (q22), or a claim attached to a passage that does not say it (q26), gives 0.
- The sentence "the version of the Food Code adopted by your state or city is what applies" is required by rule 8 of AGENTS.md. It was treated as a mandated caveat, not as a claim that needs a passage. The judge may treat it differently, which would show up as disagreements on `supported`.

**Totals:** correct 35/38 (0: q24, q37, q38); supported 36/38 (0: q22, q26).
