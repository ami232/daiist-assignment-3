# Judge audit (v1 run)

An audit of the 26 judge verdicts in `eval/judge.jsonl` against the evidence the judge saw (the question, the reference answer and the retrieved passages in `eval/answers.jsonl`). It was done by Claude during the final review (see REPORT.md, AI use). It is not part of my grades in `eval/human_labels.csv`.

Method: every claim in each answer was checked against the retrieved passages, and each answer against its reference, using the rubric in `evaluate.py`.

## Findings

| # | Question(s) | Judge verdict | Finding | Type |
|---|---|---|---|---|
| 1 | q01–q06, q09, q11–q20, q22–q24, q26 (21) and q07, q08, q10, q21 (4) | 21 *supported*, 4 *unsupported* | The same closing sentence (the corpus versions, added by AGENTS.md rule 6) is in 25 of the 26 judged answers. The judge marked it unsupported in 4 and accepted it in 21. Whichever reading is right, the verdicts contradict each other. | Inconsistent |
| 2 | q21 | correct 1, supported 0 | The reason is wrong. It says the answer cites Regulations 2019/947 and 2019/945, which "were not provided". The answer cites only EASA `AMC1 UAS.OPEN.30(1)`, the regulations are only named in the version sentence, and Reg 2019/945 `PART 2` and `PART 3` were retrieved. | Factual error |
| 3 | q23 | correct 1 | The reference gives the C5 low-speed mode limit (5 m/s, Reg 2019/945 `PART 16`, never retrieved). The answer says the corpus does not specify it and gives the STS-01 ground-speed limit instead. Under "misses its key point" this could be a 0. | Disputable |
| 4 | q15 | supported 1 | The answer glosses Article 20's "do not comply with Delegated Regulation (EU) 2019/945" as "without a class label". The gloss is reasonable but not in the passage. | Disputable, minor |

No other verdict conflicts with its evidence. q26 (correct 0) is the only answer the judge marked wrong, and the audit agrees: the answer says the rules don't cover the second part of the question.

## v2 run

The same check on the six outcomes that changed in v2: five judge verdicts (`eval/v2/judge.jsonl`) and one code check. The other 21 judged answers keep the verdicts they had in v1, correct and supported.

| Question | v1 → v2 | Finding |
|---|---|---|
| q07, q08, q10, q21 | unsupported → correct | Each search result now carries a `Version:` line (`consolidated text of 4 April 2022`, `consolidated text of 9 August 2020`, `Issue 1 of 9 October 2019`), so the closing version sentence is in the evidence. Every fact is cited to a retrieved passage. |
| q26 | wrong → correct | The single search returned `UAS.OPEN.050`; the answer states point (7) (everyone involved is informed of the risks and explicitly agrees) and cites it. |
| q32 | answered unanswerable → correct refusal | Graded in code: the answer now starts with "The corpus does not cover". The content is the same as in v1 ("without undue delay", `UAS.SPEC.040`). |

q23 and q15 stay disputable for the same reasons as in v1. No changed verdict conflicts with its evidence.

