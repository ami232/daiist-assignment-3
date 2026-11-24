# Failure analysis

This covers every question that failed under the human grades (`eval/human_labels.csv`) **or** the judge's (`eval/verdicts.jsonl`), meaning correct = 0 or supported = 0 in either. That is 14 of 39 questions. Each failure gets exactly one cause.

To decide the cause, I checked from the trace in `eval/answers.jsonl` whether the agent's searches returned a chunk covering the expected passage. For unanswerable questions there is no expected passage, so I looked at how the answer handles the gap. No grades were changed and the agent was not rerun.

## Counts per cause

| Cause | All failures | Failed by the human grades | Failed by the judge only |
|---|---|---|---|
| Retrieval miss | 3 | 3 | 0 |
| Wrong answer from the right passage | 1 | 1 | 0 |
| Unsupported claim | 7 | 3 | 4 |
| Wrong refusal | 3 | 3 | 0 |
| Bad test question | 0 | 0 | 0 |
| **Total** | **14** | **10** | **4** |

## Per question

Grades are given as correct/supported, human first, then judge.

| id | kind | human | judge | cause | reason |
|---|---|---|---|---|---|
| q04 | single | 1/0 | 1/1 | unsupported claim | The expected passage (118/19 Rn. 13) was retrieved, but the answer opens with "bank statements", which 118/19 never mentions; the court says payment receipts (Zahlungsbelege). The question's own wording ("bank statements") primed it. |
| q05 | single | 0/1 | 1/1 | wrong answer from the right passage | 137/15 Rn. 10–13, which contains Rn. 11, was retrieved and cited, but the human grade says the answer misses the Nr. 17 limitation. See the note below. |
| q07 | single | 0/1 | 1/1 | retrieval miss | 209/15 Rn. 25 was retrieved, but the § 242 exception at Rn. 28 never was. The answer can't contain it, and the judge excused the gap for exactly that reason. |
| q21 | single | 1/0 | 1/0 | unsupported claim | § 560 Abs. 4 was retrieved. The answer adds "e.g. by email" and "back payment / 12", which aren't in the passage (general knowledge). |
| q25 | single | 0/1 | 0/1 | retrieval miss | 36/14 was never retrieved in 8 searches, including a search for "VIII ZR 36/14" itself, so the agent deferred to a lawyer instead of saying no. Dense search can't match a case number. |
| q26 | multi | 1/1 | 1/0 | unsupported claim | Judge only. Both holdings were retrieved. "You must separate the rental and maintenance amounts on the invoice" is an inference the passages don't state. |
| q27 | multi | 1/1 | 1/0 | unsupported claim | Judge only. Both holdings were retrieved. "The lease must specifically name garden maintenance or reference § 2 Nr. 10" goes beyond § 556 Abs. 1. |
| q28 | multi | 0/1 | 0/0 | retrieval miss | Both searches covered only the deadline part. The on-call fee part (62/19) was never searched, which breaks rule 6, and 209/15 Rn. 28 (§ 242) was never retrieved, so the decisive exception is missing. |
| q29 | multi | 1/1 | 1/0 | unsupported claim | Judge only. Both expected passages were retrieved. "Only with an express agreement (Umlagevereinbarung)" is stronger than 249/15 says. The term itself comes from AGENTS.md rule 4, not from the passage. |
| q32 | multi | 1/1 | 1/0 | unsupported claim | Judge only. Both expected passages were retrieved. "High vacancies make circulation and distribution losses fall on the remaining users" joins two passages into a causal claim neither makes. |
| q33 | unanswerable | 0/0 | 1/1 | wrong refusal | It doesn't refuse. It answers "no duty to get comparison quotes" from the documents' silence, presented as if the corpus said so. |
| q34 | unanswerable | 0/1 | 0/1 | wrong refusal | Only CO2KostAufG was retrieved. The answer states "no operational step model; 50/50 split under § 8" as the law and never says the documents don't cover the step model. |
| q36 | unanswerable | 1/0 | 1/0 | unsupported claim | It refuses, but pads the refusal with an annual cap, the frequent-access limit and §§ 305 ff. BGB, none of which are in the corpus (general knowledge). |
| q38 | unanswerable | 0/1 | 0/1 | wrong refusal | It leads with "you can claim interest" (from 47/25 Rn. 12, a passage that only mentions "nebst Zinsen") before admitting that the default rules are missing. |

**Check on q05 (your grade, unchanged):** the answer does state the limitation: "this general clause does not automatically cover 'other' operating costs (sonstige Betriebskosten) … the specific cost type must be expressly designated" (citing 137/15 Rn. 5, 10–13). Sonstige Betriebskosten are § 2 Nr. 17, so the substance is there and only the label "Nr. 17" is missing. If that wasn't your reason for the 0, the grade is worth a second look. If it stays at 0, q05 is the only "wrong answer from the right passage".

## What to fix first

1. **Refusals on unanswerable questions.** By your grades, only 3 of 7 unanswerable questions pass cleanly:
   - three are wrong refusals (q33, q34, q38);
   - one refuses but pads the refusal with outside knowledge (q36).

   This is the failure the use case cares most about ("I don't know" beats a confident wrong answer). The AGENTS.md wording added in step 6 didn't fix q33, so more prompt text is unlikely to help.

   The next lever is the harness: for example, an output check that asks the model which sentence of a retrieved passage states the bottom line, and forces a "not covered" lead when none does. Mind the cost: it adds one model call per question.
2. **Retrieval of exceptions and named cases.** There are three misses with three different mechanisms:
   - **q07, q28:** the exception at 209/15 Rn. 28 sits in a chunk that the query for the main rule never ranks. Also, q07's expected location (Rn. 25) counted as a retrieval *hit* in step 4, even though the answer couldn't be complete. The hit-rate metric overstates retrieval wherever the decisive exception sits in a different Rn.
   - **q25:** a search for the case number found nothing. Design C (BM25 + dense) would match "36/14" exactly. That is a reason to revisit C, or to add exact case-number lookup to `search`.
   - **q28:** the agent searched only one of the two parts, so rule 6 isn't enforced. That is a harness problem, not a retrieval one.
3. **Unsupported inferences (lowest priority).** Four of the seven unsupported-claim failures are judge-only, all on multi questions. They are reasonable inferences (q26, q32) or the AGENTS.md term "Umlagevereinbarung" (q29) that you accepted.

   The three that you also failed (q04, q21, q36) are small general-knowledge additions. They matter less than the refusal problem: none of them changes the bottom line of the answer.

## The judge compared with the human grades

The judge agrees with you on 36/39 for correct and 32/39 for supported. The disagreements go in two directions:
- **Too lenient on refusals and gaps.** It passed q33 on both columns, q07 because the missing passage "was not retrieved", and q05.
- **Stricter than you on inferences in multi answers:** q26, q27, q29 and q32.

So it is not reliable as the only grader for the refusal behaviour, which is the behaviour this use case depends on most.
