# Evaluation summary

Agent model `gemini-3.5-flash-lite`, judge model `gemini-3.1-flash-lite`, server design `B_structure` with k=5.

## Retrieval (answerable questions; multi = both passages retrieved)

| design | hit@1 | hit@3 | hit@5 | single hit@5 | multi all@5 | multi any@5 | words@3 | words@5 |
|---|---|---|---|---|---|---|---|---|
| A_fixed | 62% | 81% | 85% | 95% | 50% | 100% | 990 | 1651 |
| B_structure | 54% | 96% | 100% | 100% | 100% | 100% | 802 | 1341 |
| B_structure+hybrid | 58% | 92% | 92% | 95% | 83% | 100% | 805 | 1333 |

Cross-check on questions whose reference contains figures: a hit if the expected lines were retrieved OR a retrieved chunk from the right filing contains the reference figure (the same fact printed in another place).

| design | figure hit@1 | figure hit@3 | figure hit@5 |
|---|---|---|---|
| A_fixed | 69% | 81% | 81% |
| B_structure | 69% | 100% | 100% |
| B_structure+hybrid | 69% | 88% | 88% |

Best by hit@5, then hit@3, hit@1 and fewer words: **B_structure**.

## End to end

- Answered questions: 32 of 32
- Graded (by you or the judge): 32 of 32
- Answerable, correct: 100% (26/26 graded)
- Answerable, every claim supported: 96%
- Unanswerable, correctly refused: 6/6
- Answerable but refused (wrong refusals or misses): 0/26
- Graded answers with an unsupported claim: 1
- Citations valid (code check): 100%; expected passage retrieved by the agent: 100%
- Guardrail: 0 repaired, 0 blocked

Final grades use your label where you graded the answer, else the judge's.

## Judge vs your grades

- Compared on 20 answers.
- correct: agreement 90%, Cohen's kappa 0.0; disagreements: q19, q29
- supported: agreement 95%, Cohen's kappa 0.0; disagreements: q01

## Failures

| category | count | questions |
|---|---|---|
| retrieval miss | 0 |  |
| wrong answer from the right passage | 0 |  |
| unsupported claim | 1 | q01 |
| wrong refusal | 0 |  |
| bad test question | 0 |  |

Auto-classified from the code checks; override in eval/failure_overrides.csv (columns id, category, note).

## Cost per question

- Agent: mean 5,781 tokens (median 4,826, max 12,265), mean 5.1s (median 3.3s, max 28.5s), mean 2.1 model calls.
- Input tokens are 98% of the total (the retrieved passages dominate).
- Judge: mean 3,457 tokens per question.
- One question end to end, agent plus judge: about 9,238 tokens; plus 1 query embedding.

## Before and after adding a document

Question q27: What were Goldman Sachs' Asset & Wealth Management net revenues in the third quarter of 2026?

**Before** (refused): The indexed filings do not cover this. They cover annual financial data for Goldman Sachs' Asset & Wealth Management segment for the years ended December 31, 2025, 2024, and 2023 [GS_10K_FY2025#mdna034].

**Added** corpus/GS_10Q_Q3_2026/raw.htm via agent: added: GS_10Q_Q3_2026, 58 passages (0 newly embedded). It is now searchable.

Approval log: evaluate.py approved add_document('corpus/GS_10Q_Q3_2026/raw.htm') for the before/after demo

**After** (answered): Goldman Sachs' Asset & Wealth Management net revenues were $5,051 million ($5.05 billion) for the third quarter of 2026 [GS_10Q_Q3_2026#mdna019, GS_10Q_Q3_2026#mdna037]. By component, this comprised $3,587 million in Management and other fees, $587 million in Incentive fees, $827 million in Private banking and lending, and $50 million in Investments [GS_10Q_Q3_2026#mdna036].

Sources after: [GS_10Q_Q3_2026#mdna019] Goldman Sachs 10-Q 2026 · MD&A · Asset & Wealth Management · lines 148-155 of item_2_mdna.txt; [GS_10Q_Q3_2026#mdna037] Goldman Sachs 10-Q 2026 · MD&A · Asset & Wealth Management · lines 408-417 of item_2_mdna.txt; [GS_10Q_Q3_2026#mdna036] Goldman Sachs 10-Q 2026 · MD&A · Asset & Wealth Management · lines 378-407 of item_2_mdna.txt

## Held-out filing (Goldman Q3 2026 10-Q, never used to build or tune)

Asked after the 10-Q was added, with nothing changed.

| id | kind | refused | expected passage retrieved | judge correct | judge supported |
|---|---|---|---|---|---|
| h01 | single | 0 | 1 | 1 | 1 |
| h02 | single | 0 | 1 | 1 | 1 |
| h03 | single | 0 | 1 | 1 | 1 |
| h04 | single | 0 | 1 | 1 | 1 |
| h05 | unanswerable | 1 |  | 1 | 1 |

5/5 judged correct.
