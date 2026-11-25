# Add-document demo

Question: **What is the EU threshold for concession contracts from 2026?**

Document added: `docs_to_add/reg_2025_2151.html` (Delegated Regulation (EU) 2025/2151, concession threshold for 2026-2027, CELEX 32025R2151, © European Union).

Run on a temporary copy of `index/` (INDEX_DIR), so the committed index is unchanged and the main evaluation still counts this question as unanswerable. Design structure, mode vector, k=5, agent model gemini-3.5-flash-lite.

## Before

> The corpus does not cover this. 
> 
> Concession contracts are governed by Directive 2014/23/EU, which is not part of the corpus. Please consult Directive 2014/23/EU or the applicable national procurement law to check the threshold for concession contracts.

- Searches: `concession contracts threshold 2026`
- Retrieved: [dir_2014_24 | Article 4], [reg_2025_2152 | Article 1], [dir_2014_24 | Article 92], [dir_2014_24 | Article 6], [dir_2014_24 | Article 13]
- Citations: none
- Refused: True
- Citation guardrail: did not fire

## add_document

First call: `doc_id reg_2025_2151: added 6 chunks to the 'structure' collection.`

Second call with the same file: `already indexed, nothing changed (doc_id reg_2025_2151, 6 chunks).`

## After

> The corpus does not cover concession contracts in detail, as Directive 2014/23/EU on concessions is outside the main directives indexed here. However, the search index contains Delegated Regulation (EU) 2025/2151, which amends Directive 2014/23/EU regarding thresholds for the years 2026–2027 [reg_2025_2151 | Article 1]:
> 
> The threshold for concession contracts is **EUR 5,404,000**, applying from **1 January 2026** (replacing the previous amount of EUR 5,538,000) [reg_2025_2151 | Article 1, reg_2025_2151 | Article 2].
> 
> For specific rules on concession procedures, please consult Directive 2014/23/EU and national procurement law.

- Searches: `threshold concession contracts 2026`
- Retrieved: [reg_2025_2151 | Article 1], [reg_2025_2151 | Recital 3], [reg_2025_2151 | Article 2], [reg_2025_2151 | Recital 2], [reg_2025_2151 | Recital 1]
- Citations: [reg_2025_2151 | Article 1]
- Refused: False
- Citation guardrail: did not fire
