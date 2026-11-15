# Assignment 3 Report

- **Name**:
- **Student ID**:
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case

The assistant is built specifically for a startup founder when it's smaller coprotations or or compliance lead of an EU startup that builds AI or online-platform products. Especially in smaller teams like a startup   there is usually legal team, so this person is the one who has to answer questions like "can we launch this feature?" or "do we need an impact assessment for this?" before a lawyer is involved. They use the answer to decide on legality of feature  launches as designed, which documents or assessments they need to prepare, and whether the question is serious enough to call a lawyer.

The two possible mistakes don't cost the same. If the assistant answers wrongly, the founder might launch something that is not compliant, or believe they are covered when they aren't. The cost of that can be very high. According to the corpus itself fines go up to 7% of global turnover under the AI Act for prohibited practices (Art. 99), 4% under the GDPR (Art. 83) and 6% under the DSA (Art. 52 and 74). On top of the fines there exists the possibility of blocked launches and the reputational damage which would need to be quantified but adds to the total cost. On the other side a wrong no"also has a cost, because the startup might have to drop or delay a feature that was actually allowed. In a competitive environment like AI this might mean falling behind which is costly and again is a cost that varies on case per case basis and needs further understanidng of the situation to be qunatified. 

Alternatively in the case of rerouting to a lawyer, if the assistant says "the corpus doesn't cover this, ask counsel", the cost is only some time and a lawyer's fee, a few hundred euros for a short consultation. That is small compared with a fine calculated on turnover.

## Corpus

| Document | URL | Date (OJ publication) | Licence | Words |
|---|---|---|---|---|
| AI Act, Regulation (EU) 2024/1689 | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | 12 July 2024 | © European Union; reuse authorised with attribution (Commission Decision 2011/833/EU) | ~90,500 |
| GDPR, Regulation (EU) 2016/679 | https://eur-lex.europa.eu/eli/reg/2016/679/oj | 4 May 2016 | Same | ~55,000 |
| Digital Services Act, Regulation (EU) 2022/2065 | https://eur-lex.europa.eu/eli/reg/2022/2065/oj | 27 October 2022 | Same | ~64,100 |
| **Total** | | | | **~209,600** |

English Official Journal versions, downloaded as XHTML from the EU Publications Office (CELLAR) by `index.py`. Legislation contains no personal data.

## Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

## Test set

*How you wrote it, counts by kind, two examples.*

## Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

## Tools and subagent

*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
