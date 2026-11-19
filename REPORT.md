# Assignment 3 Report

- **Name**: Alejandra Hernandez
- **Student ID**: 20122
- **Group**: BBADBA 5A 

## Use case

A pharmacy assistant in a community pharmacy in Spain. Patients taking blood thinnersask them questions at the counter, such as “I forgot a dose, what do I do?” or “Can I take ibuprofen with it?” With the answer and with the citation to the official EMA leaflet, they answer the patient or decide to send them to the pharmacist or doctor. Th cost of a wrong answer vs "I don’t know, is that a wrong answer can cause major bleeding or a stroke. “I don’t know” only costs a few minutes while the assistant asks the pharmacist. So the system must refuse rather than guess.

## Corpus

| Document | URL | Date | Licence | Words (raw / after cleaning) |
|---|---|---|---|---|
| Eliquis (apixaban), EMA product information | https://www.ema.europa.eu/en/documents/product-information/eliquis-epar-product-information_en.pdf | 25 March 2026 | EMA content may be reproduced provided the source is acknowledged | 68,262 / 37,185 |
| Xarelto (rivaroxaban), EMA product information | https://www.ema.europa.eu/en/documents/product-information/xarelto-epar-product-information_en.pdf | 27 July 2026 | same | 104,262 / 57,412 |
| Pradaxa (dabigatran), EMA product information | https://www.ema.europa.eu/en/documents/product-information/pradaxa-epar-product-information_en.pdf | 4 September 2026 | same | 63,320 / 35,242 |
| **Total** | | | | **235,844 / 129,839** |

Dates are the creation dates of the PDF files published by EMA (the documents themselves only link to the EMA website for the revision date). No personal data: these are official regulatory documents about medicines, not about patients.

## Ingestion

Extraction
`index.py` downloads the three PDFs from EMA into `corpus/` (git-ignored) and reads them page by page with `pypdf`, so every piece of text keeps its page number.

Cleaning
Words split by a hyphen at a line end are joined, repeated spaces and empty lines are collapsed, and lines that only hold a page number are removed.

Structure
The code walks the text line by line and tracks three things: the *part* (SmPC = technical sheet, Annex II, Labelling, or patient Leaflet), the *product* (e.g. "Eliquis 2.5 mg film-coated tablets") and the *section* (e.g. "4.2 Posology"). A numbered line only counts as a heading if its number goes forward, so numbers inside tables are not mistaken for headings.

Extraction problem I fixed: repeated text
Each EMA document repeats almost the same SmPC and leaflet for every strength and form (2.5 mg, 5 mg, children's granules...). Without a fix, the top 5 search results were often the same paragraph five times. The code removes any paragraph (8+ words) that already appeared earlier in the same document: 95,919 words (about 40%) were removed. I also skip the Labelling part (carton and blister text, 10,086 words), which never answers a question.

Known imperfection
Numbered sub-documents inside the leaflet (the patient alert card, and the children's Instructions for Use with steps "1.", "2."...) are sometimes read as leaflet sections 1-6, so a few chunks get a wrong section label.

Chunk metadata
Every chunk carries: `source` (eliquis / xarelto / pradaxa), `page`, `location` (part + section, e.g. `SmPC 4.2`), a `header` with the product name, and an `id` that is a hash of its text (so unchanged text is never embedded twice).

Chunks.
Two designs, both about 300 words per chunk: *fixed* = 520 chunks; *structured* = 604 chunks. Embedded with `gemini-embedding-2` (768 dimensions) and stored in ChromaDB in `index/chroma` (22.3 MB). Vectors are saved after every batch of 50, and `main.py index` embeds only chunks without a saved vector. The work was spread over two days because of the free quota (about 1,000 embeddings a day).

## Test set

I wrote 32 questions from the three documents before comparing any retrieval design. For each question I read the relevant section (with a small helper, `peek.py`, that prints any section of a medicine), chose one concrete fact (a dose, a prohibition, an "if... then" rule), and phrased the question the way a patient or customer would ask at the counter, not with the words of the PDF.

| Kind | Count |
|---|---|
| single (one passage) | 20 |
| multi (two passages, usually comparing two medicines) | 6 |
| unanswerable (on topic but not in the documents) | 6 |
| **Total** | **32** |

Questions cover dosing (4.2), contraindications (4.3), warnings (4.4), interactions (4.5), pregnancy (4.6), side effects (4.8), overdose (4.9), storage, and the patient leaflet. For the unanswerable questions I searched all pages of the three PDFs for the key words (edoxaban, price, alcohol, ginkgo, generic, tattoo) and confirmed none appear. One of them (edoxaban / Lixiana) is used later for the before/after demo.

Two examples:
- **q02 (single):** "My father had an eye operation last week, can he start taking Eliquis?" → No: recent eye, brain or spinal surgery is a contraindication (eliquis, SmPC 4.3).
- **q22 (multi):** "After an overdose, can dialysis remove Xarelto or Pradaxa?" → Rivaroxaban is not expected to be dialysable; dabigatran can be dialysed (xarelto + pradaxa, SmPC 4.9).

## Retrieval

Hit rate on the 26 answerable questions (a hit means the expected document *and* section are in the top k; a multi question needs both of its passages). Every question was embedded once and the same vectors were used for all designs.

| design | hit@1 | hit@3 | hit@5 | words per chunk | words added to the prompt (5 chunks) |
|---|---|---|---|---|---|
| fixed (300-word windows, 50 overlap) | **42%** | 65% | 81% | 299 | ~1,495 |
| structured (by section, header line) | 23% | **69%** | 81% | 231 | ~1,155 |
| structured + medicine filter | 23% | 69% | 81% | 231 | ~1,155 |

Choice: structured
The server returns 5 chunks to the agent, so hit@5 is the number that matters, and there the two designs tie (81%). Structured is slightly better at k=3, adds about 23% fewer words to the prompt, and each

## Tools and subagent

Tools
 (`server.py`, MCP over stdio, registered as `corpus` in `.mcp.json` and `.vscode/mcp.json`). The docstring is what the model reads:

- `search(query)`: "Search the official EMA product information (SmPC and patient leaflet) of the anticoagulants in the corpus: Eliquis (apixaban), Xarelto (rivaroxaban) and Pradaxa (dabigatran), plus any document added later. Use it for any question about these medicines: doses, missed doses, kidney or liver problems, contraindications, interactions, pregnancy, side effects, overdose, storage... Returns the 5 most relevant passages. Each starts with a citation such as [eliquis p.4 SmPC 4.2]; cite it after every claim. If no passage answers the question, the corpus does not cover it: say so." Only the query is embedded; the corpus vectors are loaded from `index/`.
- `add_document(path)`: "Add a PDF of product information to the searchable corpus... only chunks that are not stored yet are embedded... Changes the index: only call it when the user asks."

One search result
(from `check.py`, query "I forgot my Eliquis last night, can I take two tablets this morning?"):

```
[eliquis p.143 Leaflet 3] (distance 0.169)
Eliquis | Eliquis 2.5 mg film-coated tablets | Leaflet 3 How to take Eliquis
- Changing from treatment with anticoagulant containing vitamin K antagonist (e.g., warfarin) to Eliquis ...
... If you forget to take Eliquis - If you miss a morning dose, take it as soon as you remember ... A missed evening dose can only be taken during the same evening. Do not take two doses the next morning ...
```

Subagent
(`.claude/agents/corpus-researcher.md`): its only tool is `search`, listed under both names (`mcp__corpus__search` for Claude Code, `corpus/search` for VS Code). Its instructions: short queries with the medicine and topic, at most 3 searches; read every passage to the end; answer only from the passages; cite every claim; never transfer a fact between medicines; otherwise use the fixed refusal sentence; at most 5 sentences, in the language of the question.

Problems I had to fix to make it work in Copilot:
1. The `corpus` MCP server was not running the first time, so the subagent had no tools and

## Adding a document

If the document is already indexed
Every chunk's id is a hash of its text. `add_document` runs the file through the same pipeline as `index.py` (it imports `chunk_file` and `embed_and_store`), then embeds only chunks whose id is not stored yet. So the same file twice embeds nothing and answers "already indexed and unchanged". If a file with the same name has changed (e.g. a new EMA version of the leaflet), its old chunks are deleted and only the new ones are embedded, so the index always holds the latest version without duplicates.

Demo
Unanswerable question q27: "What is the dose of edoxaban (Lixiana) for atrial fibrillation?" Document added: the EMA product information of Lixiana (edoxaban), downloaded to `corpus/lixiana.pdf`, which produced 72 new chunks.

- Before:
"The product information in the corpus does not cover this; please ask the pharmacist or doctor." (1 search, no sources)
- Add:
the agent asked for approval before running `add_document`. When I answered `n`, nothing was added; with `y`, the document was added.
- After:
"For the prevention of stroke and systemic embolism in non-valvular atrial fibrillation, the recommended dose is 60 mg edoxaban once daily [lixiana p.3 SmPC 4.2]. The recommended dose is 30 mg once daily in patients with one or more of: moderate or severe renal impairment (CrCl 15–50 mL/min), low body weight ≤ 60 kg, or concomitant use of ciclosporin, dronedarone, erythromycin or ketoconazole [lixiana p.3 SmPC 4.2]."
- Adding it again:
"'lixiana' is already indexed and unchanged… Nothing was embedded."

Note: the evaluation results in `eval/` were produced before Lixiana was added, so q27 counts there as a correct refusal.

## Harness and guardrails

`agent.py` uses LangChain `create_agent` on Gemini (`gemini-3.5-flash-lite`), starts `server.py` over MCP, and sends `AGENTS.md` as the system prompt.

AGENTS.md rules =
(each with its reason in the file): (1) answer only from the search results; (2) cite every claim; (3) use a fixed refusal sentence when the corpus does not cover the question; (4) never apply a fact about one medicine to another; (5) copy numbers exactly, never calculate; (6) end patient-specific answers with "Confirm with the pharmacist or doctor"; (7) answer in the language of the question; (8) use add_document only when the user asks.

Approval step (in code, not in the prompt)=
Before `add_document` runs, the terminal asks "Approve? [y/N]". Only "y" lets it run; with no terminal (evaluation, GitHub Actions) it is refused automatically. When I answered "n", the document was not added; with "y" it was added. This does not depend on the model obeying rule 8.

Call limits =
At most 8 model calls and 6 tool calls per question (LangChain middleware), against loops and quota burn.

My extra guardrail: citation check = 
After the agent answers, the code checks that every citation label in the answer is one that `search` actually returned in that run. An invented citation, or an answer with no citation that is not a refusal, is replaced by the refusal sentence.

- A case where it fired correctly (q04, pregnancy and Eliquis):
the model cited `[eliquis p.13 SmPC 4.6]`, but the passage had been returned as `[eliquis p.13 SmPC 4.5]` (the chunk spans 4.5 and 4.6 and is labelled with its first section). The guardrail blocked it, and the user got the refusal. Safe, but it turned a correct answer into a wrong refusal.
- Two bugs it had, which I found through the evaluation:
(1) the model often put two labels in one bracket, `[eliquis p.12 SmPC 4.5, eliquis p.44 SmPC 4.5]`, which my first version read as one unknown label, so it blocked 10 of 32 good answers; after splitting brackets, it blocks 1 of 32. (2) It also blocked the agent's message after `add_document` ("the document was not added"), because that message has no citation; it now skips index operations.

## Evaluation

`main.py evaluate` runs the agent on all 32 questions, then checks what code can check and sends the rest to an LLM judge.

Code checks:
whether the answer is a refusal (fixed sentence, no citation) and whether that was right for the question kind; whether every citation label was really returned by `search` in that run; whether the answer cites the expected document.

Judge rubric
(Gemini, temperature 0, with the retrieved passages as evidence):
- *correct*: for answerable questions, 1 if the key fact a patient needs is right and nothing is wrong; missing secondary details is fine; a wrong number, wrong medicine or a refusal is 0. For unanswerable questions, 1 only if it refuses without adding content of its own (the standard refusal and "confirm with the pharmacist or doctor" are part of a refusal).
- *supported*: 1 if every factual claim is in the retrieved passages.

My grades vs the judge
(22 answers, graded before reading the verdicts): agreement 91% on *correct*, 100% on *supported*. Disagreements: **q02**, where I graded the answer wrong because it says Eliquis can be "restarted as soon as possible" after surgery and never says that recent eye surgery is a contraindication; the judge accepted it because the sentence is in the retrieved text. And **q30**: [your reason in one sentence]. The judge is too lenient on exactly the kind of answer that is dangerous: true sentences that do not answer the question.

Results
(after fixing the guardrail bug described above):

| | result |
|---|---|
| Correct (judge) | 97% (31/32) |
| Supported by retrieved text (judge) | 100% |
| Rightly refused (unanswerable) | 6/6 |
| Made things up (unanswerable but answered) | 0/6 |
| Wrongly refused (answerable) | 1/26 |
| Cited the expected document | 25/25 |

First run, before the fix: 53% correct, 13/26 wrong refusals, because my citation guardrail blocked 10 good answers.

## Failures

Failures counted from my own grades and the judge's together:

| question | what happened | cause |
|---|---|---|
| q02 (eye surgery, Eliquis) | Said Eliquis can be restarted after surgery; never said recent eye surgery is a contraindication | **Retrieval miss**: the search "Eliquis eye surgery operation" did not return SmPC 4.3, so the agent answered from a 4.4 passage about restarting after surgery |
| q04 (pregnancy, Eliquis) | Refused | **Wrong refusal**: the answer was right, but it cited the chunk's second section (4.6) while the chunk was labelled with its first (4.5), so my guardrail blocked it |
| q30 | [your view] | [your category] |

By cause: retrieval miss 1, wrong refusal 1, wrong answer from the right passage 0 in the evaluation (1 in the Copilot transcript: the missed-dose rules merged), unsupported claim 0, bad test question 0. Not counted as a failure: q25 answered in Spanish to an English question (rule 7), with correct facts.

Retrieval alone missed at k=5 on q02, q08, q10, q16 and q24, but the agent recovered on four of them by writing its own queries. Only q02 stayed wrong.

What to fix first: q02
Because it is the dangerous one. A "can patient X take medicine Y" question should always also search the contraindications (SmPC 4.3) of that medicine; this could be a rule in AGENTS.md or a second, automatic search in the harness. Second: label each chunk with every section it contains, so a correct citation like q04's is not blocked.

## Decision

Not as the only source, but yes as a lookup aid =
A pharmacy assistant could use it to find the right passage of the official leaflet quickly, read it, and answer the patient. It should not be used as a source of answers to repeat without reading the citation.

Why: it never made things up on the unanswerable questions (0/6) and every claim was supported (100%), so a refusal can be trusted. But q02 shows the dangerous case: a true, cited sentence that does not answer the question ("can he take it after eye surgery?"), and the LLM judge missed it. A 97% score from the judge overestimates the quality on exactly the questions where a mistake costs most.

Safeguards:
(1) the assistant opens the cited passage before answering; (2) for "can this patient take it?" questions, always check SmPC 4.3 (contraindications), by rule or with an automatic second search; (3) keep the citation guardrail and the refusal sentence; (4) human spot checks, since the judge alone is not enough.

Cost and latency per question:
5,068 agent tokens and 10.1 s on average (2.2 model calls, 1.3 searches), plus 3,025 tokens for the judge during evaluation. Everything ran on the Gemini free tier (gemini-3.5-flash-lite for the agent and the judge, gemini-embedding-2 for embeddings).

## AI use

I used Claude (Anthropic) as a step-by-step tutor throughout. Claude wrote the code (index.py, server.py, agent.py, evaluate.py, peek.py) and explained it; I ran and tested it, and fixed the errors with its help. For the test set, Claude showed me the sections and proposed options for each question; I chose which fact to test, which answer was correct, and checked the unanswerable ones were not in the documents. The use case, the chunking choices (removing duplicates, skipping labelling), the AGENTS.md rules and the judge rubric were my decisions from options Claude explained. Claude drafted parts of this report from my work; I reviewed and edited them.
