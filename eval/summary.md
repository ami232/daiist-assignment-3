# Evaluation summary

Agent `gemini-3.8-flash`, judge `gemini-3-flash-preview / gemini-3.5-flash / gemini-3.6-flash`, design `structural` + `dense`.

## Retrieval

| design | method | hit@1 | hit@3 | hit@5 | all@5 (multi) | words@5 |
|---|---|---|---|---|---|---|
| structural | dense | 0.741 | 0.963 | 1.0 | 0.963 | 1365 |
| structural | hybrid | 0.407 | 0.704 | 0.926 | 0.778 | 1511 |
| fixed | dense | 0.519 | 0.852 | 0.852 | 0.741 | 1500 |
| fixed | hybrid | 0.407 | 0.63 | 0.704 | 0.556 | 1500 |

## End to end

- correct: 34/34
- unsupported: 0
- correct refusals: 7/7
- wrong refusals: 0
- answers with invalid citations: 0
- citation guardrail fired on: none
- cost per question: 5560 input + 245 output tokens, 22.9 s

| id | kind | judge correct | judge supported | refusal | citations | invalid | cites expected | reason |
|---|---|---|---|---|---|---|---|---|
| q01 | single | 1 | 1 | 0 | 4 | 0 | 1 | The assistant accurately provides the key minimum own funds and leverage ratio requirements specified in the reference answer, fully supported by CRR Article 92(1) in the retrieved passages. |
| q02 | single | 1 | 1 | 0 | 5 | 0 | 1 | The assistant accurately provides the core rules and limits from Article 395(1) CRR as specified in the reference answer, and all cited claims are fully supported by the retrieved passages. |
| q03 | single | 1 | 1 | 0 | 1 | 0 | 1 | The assistant correctly states that a Tier 2 instrument must have an original maturity of at least five years based on Article 63(g) of the CRR, which is fully supported by the retrieved passages. |
| q04 | single | 1 | 1 | 0 | 10 | 0 | 1 | The assistant correctly states the main rules (prior supervisory permission and the 5-year restriction), provides accurate additional regulatory detail, and all cited conditions and articles are fully supported by the retrieved passages. |
| q05 | single | 1 | 1 | 0 | 9 | 0 | 1 | The assistant provides a complete and accurate breakdown of CET1 capital elements, fully supported by the retrieved CRR articles. |
| q06 | single | 1 | 1 | 0 | 3 | 0 | 1 | The assistant accurately states the general EUR 5 million requirement and the EUR 1 million exception for particular categories of credit institutions, fully supported by CRD Article 12 in the retrieved passages. |
| q07 | single | 1 | 1 | 0 | 5 | 0 | 1 | The answer accurately states the key limit of 60 working days and the conditions for suspending the clock when requesting further information, fully supported by CRD Article 22 in the retrieved passages. |
| q08 | single | 1 | 1 | 0 | 2 | 0 | 1 | The assistant accurately states the general 100% cap on variable remuneration relative to fixed salary, as well as the potential 200% cap with shareholder approval, citing CRD Article 94(1)(g) as supported by the retrieved text. |
| q09 | single | 1 | 1 | 0 | 5 | 0 | 1 | The assistant correctly states the main rule (at least 40% deferred over at least 4 to 5 years) and all additional details provided are fully supported by the retrieved text of CRD Article 94(1). |
| q10 | single | 1 | 1 | 0 | 1 | 0 | 1 | The assistant correctly states the standard 3% cap in Common Equity Tier 1 capital along with the exception for higher buffers under Commission authorization, all of which is fully supported by the retrieved text. |
| q11 | single | 1 | 1 | 0 | 3 | 0 | 1 | The assistant accurately answers the question based on Article 76(3) of the CRD, matching the reference answer and fully supported by the retrieved text. |
| q12 | single | 1 | 1 | 0 | 2 | 0 | 1 | The answer correctly identifies that the management body must review the risk strategies and policies at least every two years pursuant to Article 76(1) of the CRD, which is fully supported by the retrieved passages. |
| q13 | single | 1 | 1 | 0 | 3 | 0 | 1 | The assistant accurately answers the question based on the retrieved passages from CRD Articles 97 and 99, capturing both the proportionality principle and the annual update requirement. |
| q14 | single | 1 | 1 | 0 | 1 | 0 | 1 | The assistant correctly states the 6-month time limit for informing an applicant of authorisation under MiFID II Article 7(3), which is fully supported by the retrieved passages. |
| q15 | single | 1 | 1 | 0 | 4 | 0 | 1 | The answer accurately states the fine limits (at least EUR 5 000 000 or up to 10% of annual turnover) as well as additional details, all of which are fully supported by the retrieved passages. |
| q16 | single | 1 | 1 | 0 | 4 | 0 | 1 | The assistant's answer accurately captures all the key elements required by Article 25(2) of MiFID II, fully matching the reference answer and supported by the retrieved passages. |
| q17 | single | 1 | 1 | 0 | 16 | 0 | 1 | The assistant correctly identifies all key factors for best execution and the rule regarding specific client instructions, fully aligned with the reference answer and supported by the retrieved passages. |
| q18 | single | 1 | 1 | 0 | 3 | 0 | 1 | The assistant accurately explains the requirements under Article 23 of MiFID II regarding conflicts of interest disclosures, fully matching the reference answer and supported by the retrieved passages. |
| q19 | single | 1 | 1 | 0 | 3 | 0 | 1 | The assistant accurately identifies the core requirements that advertising must be fair, clear, not misleading, and clearly identifiable as such, fully supported by the retrieved passages. |
| q20 | single | 1 | 1 | 0 | 2 | 0 | 1 | The assistant correctly states the rules under MiFID II Article 5(4) regarding the location of an investment firm's head office relative to its registered office or place of business, which accurately answers the question and is fully supported by the retrieved text. |
| q21 | single | 1 | 1 | 0 | 1 | 0 | 1 | The assistant correctly states that institutions must maintain a net stable funding ratio of at least 100% under CRR Article 428b(2), which matches the reference answer and is fully supported by the retrieved passages. |
| q22 | multi | 1 | 1 | 0 | 5 | 0 | 1 | The assistant accurately identifies the 10% threshold for a large exposure and the 25% limit, providing fully supported details directly from CRR Articles 392 and 395(1). |
| q23 | multi | 1 | 1 | 0 | 2 | 0 | 1 | The assistant correctly identifies the 2.5% capital conservation buffer mentioned in the reference and provides additional supported details about the combined buffer requirement. |
| q24 | multi | 1 | 1 | 0 | 4 | 0 | 1 | The assistant correctly identifies the directorship limits and the possibility of an additional non-executive directorship, with all facts and citations supported by the provided passages. |
| q25 | multi | 1 | 1 | 0 | 6 | 0 | 1 | The assistant correctly identifies the restrictions on distributions, the requirement to calculate the MDA, and the obligation to notify the supervisor and submit a conservation plan, all of which are supported by the retrieved CRD articles. |
| q26 | multi | 1 | 1 | 0 | 2 | 0 | 1 | The assistant correctly identifies the 3% minimum leverage ratio and the use of Tier 1 capital, both of which are explicitly stated in the retrieved passages (CRR Articles 92 and 429). |
| q27 | multi | 1 | 1 | 0 | 3 | 0 | 1 | The assistant correctly identifies the EUR 5 million requirement for banks and the reference to Directive (EU) 2019/2034 for investment firms, all of which are supported by the provided passages. |
| q28 | unanswerable | 1 | 1 | 1 | 0 | 0 | 0 | The assistant correctly identified that the provided documents do not contain the specific minimum default probability value, which matches the reference answer. |
| q29 | unanswerable | 1 | 1 | 1 | 0 | 0 | 0 | The assistant correctly identified that the provided corpus does not contain the specific reporting timelines under DORA, which aligns with the reference answer. |
| q30 | unanswerable | 1 | 1 | 1 | 0 | 0 | 0 | The assistant correctly declined to answer as the provided passages from MiFID II do not contain the specific trade reporting requirements of MiFIR, which matches the reference answer. |
| q31 | unanswerable | 1 | 1 | 1 | 0 | 0 | 0 | The assistant correctly identifies that the provided corpus does not contain the answer to the question, which matches the reference answer. |
| q32 | unanswerable | 1 | 1 | 1 | 0 | 0 | 0 | The assistant correctly identified that the provided corpus does not contain the specific monetary threshold for money laundering checks in one-time operations, which aligns with the reference answer. |
| q33 | unanswerable | 1 | 1 | 1 | 0 | 0 | 0 | The assistant correctly stated that the corpus does not cover the question, which aligns with the reference answer and the provided passages. |
| q34 | unanswerable | 1 | 1 | 1 | 0 | 0 | 0 | The assistant correctly states that the corpus does not contain the specific risk-weight percentages for residential mortgages, which aligns with the reference answer. |

## Judge vs human

- correct: 0.971 agreement over 34 answers, kappa 0.0; disagreements: q23
- supported: 1.0 agreement over 34 answers, kappa None; disagreements: none
