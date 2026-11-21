# Assignment 3 Report

- **Name**: Diana de Lorenzo
- **Student ID**: 20119
- **Group**: BBADBA 5B

## Use case

**Who asks.** The product and marketing team of a small Spanish niche
perfume brand, before launching or relabelling a fragrance. They ask
questions such as: which fragrance allergens must be on the label and from
what concentration, whether an ingredient is allowed and up to what level,
whether the box can say "hypoallergenic", or what the safety report must
contain.

**What they do with the answer.** They decide the text of the label, the
formula and the marketing claims, or they escalate the question.

**What a wrong answer costs.** If the assistant answers wrongly, the brand can
get into serious trouble. The product can be withdrawn and the whole stock
relabelled, which is a large cost for the brand: for one batch of ~5,000
units, tens of thousands of euros. But the biggest cost is not the product:
customer loyalty and the brand's image can fall, and sales with them. There
can also be fines from the health and consumer authorities. And if a customer
has an allergic reaction, it becomes a huge problem: lawsuits, trials and
compensation.

**What "I don't know" costs.** The team asks an external regulatory
consultant instead: about **€100** and **2–3 days** of waiting.

**So a wrong answer is hundreds of times worse than "I don't know".** The
assistant should only answer when the documents clearly support it, cite the
exact article or annex entry so the team can check it, and otherwise say it
does not know.

## Corpus

| Document | URL | Date | Licence | Words |
|---|---|---|---|---:|
| Regulation (EC) No 1223/2009 on cosmetic products, consolidated text (articles + Annexes I–X, incl. fragrance allergens in Annex III) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02009R1223-20250501 | consolidated 1 May 2025 | EU legal texts, free reuse (Commission Decision 2011/833/EU) | ~71,700 |
| Commission Implementing Decision 2013/674/EU, guidelines on Annex I (cosmetic product safety report) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013D0674 | 25 Nov 2013 | same | ~12,400 |
| Commission Regulation (EU) No 655/2013, common criteria for claims | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013R0655 | 10 Jul 2013 | same | ~1,500 |
| **Total** | | | | **~85,600** |

Downloaded by `index.py` from the EU Publications Office (the same texts as
EUR-Lex). No personal data. I use the **consolidated** regulation because the
original 2009 text has been amended many times (for example, the list of
fragrance allergens to label was extended in 2023): an assistant on the old
text would give outdated answers, which is exactly the wrong answer this use
case cannot afford.

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
