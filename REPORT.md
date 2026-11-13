# Assignment 3 Report

- **Name**: Lucia Bell
- **Student ID**: 19177
- **Group**: BBADBA 5B

## Use case

- **Who asks**: a health-and-safety technician or site manager at a construction company in Spain.
- **What they do with the answer**: decide which duties and documents to require on a site, and quote the article.
- **A wrong answer** can mean a fine, a stopped site or liability after an accident. A confident wrong answer is worse than no answer, because the user acts on it.
- **"I don't know"** costs a few minutes to check the BOE.
- **So the design is**: answer only from the retrieved text, cite norm and article, and refuse when the corpus does not cover the question.

## Corpus

| Document | URL | Date | Licence | Words |
| :--- | :--- | :--- | :--- | :---: |
| Ley 31/1995 | https://www.boe.es/diario_boe/xml.php?id=BOE-A-1995-24292 | 8 Nov 1995 | BOE reuse terms | 22,237 |
| RD 39/1997 | https://www.boe.es/diario_boe/xml.php?id=BOE-A-1997-1853 | 17 Jan 1997 | BOE reuse terms | 13,423 |
| RD 1627/1997 | https://www.boe.es/diario_boe/xml.php?id=BOE-A-1997-22614 | 24 Oct 1997 | BOE reuse terms | 11,118 |
| RD 1215/1997 | https://www.boe.es/diario_boe/xml.php?id=BOE-A-1997-17824 | 18 Jul 1997 | BOE reuse terms | 6,538 |
| Ley 32/2006 | https://www.boe.es/diario_boe/xml.php?id=BOE-A-2006-18205 | 18 Oct 2006 | BOE reuse terms | 5,366 |
| **Total** | | | | **58,682** |

- **Why these**: they refer to each other, so some questions need two passages.
- **Licence**: BOE content can be reused if the source is cited and the meaning is not changed. Source: https://www.boe.es/informacion/aviso_legal/index.php
- **Personal data**: none, they are laws.
- **Limitation I found late**: this BOE address gives the *original* text, not the updated one. Some later articles are missing (for example the "recurso preventivo") and the fines table is still in pesetas.

## Ingestion

- **Steps** (`index.py`): download the XML, read it, clean the spaces, cut it into chunks, embed each chunk with Gemini `gemini-embedding-2` and store it in ChromaDB.
- **Two designs**: `article` (one chunk per article, 291 chunks) and `fixed` (windows of 150 words with 30 words of overlap, 488 chunks).
- **Metadata**: each chunk has its norm (`source`) and article (`location`), and its text starts with them, so the citation travels with the text.
- **Extraction problem I fixed**: additional provisions and annexes sit under group headings, so at first they were attached to the previous article. Now each one has its own location.

## Test set

30 questions in `eval/questions.csv`: 19 simple, 5 that need two passages and 6 that the corpus cannot answer.

**How I wrote them**: Claude suggested the format. I wrote the questions, Claude corrected and improved them, and then I checked them against the BOE text and changed 5.

- **Example, answerable**: "¿Quién designa al coordinador de seguridad y salud durante la ejecución de la obra?" Expected: the promoter (RD 1627/1997, Art. 3).
- **Example, unanswerable**: "¿Qué carnet o formación específica necesita un operador de grúa torre?" Expected: "No consta en los documentos del corpus".

They come from the same text as the corpus, so they are easier than real questions. That is why I also tested with new questions (see Evaluation).

## Retrieval

Is the right article in the top k results? (24 answerable questions)

| Design | top 1 | top 3 | top 5 |
| :--- | :---: | :---: | :---: |
| `article` | 0.79 | 0.96 | 1.00 |
| `fixed` | 0.50 | 0.75 | 0.79 |

- **I chose `article`**: it wins at every k.
- **Words added to the prompt**: each search returns 5 chunks. With `article` that is up to about 1,750 words; with `fixed` it is 5 x 150 = 750 words. In the whole run the agent used on average 4,598 input tokens per question.
- **Why `fixed` fails**: it missed 5 questions in the top 5 (q07, q11, q12, q26, q27). Four need two passages, so the five results fill up with windows of the same article and the second norm does not fit. The fifth (q07) is a long article cut into windows. This is my explanation and I did not test it further. Only 24 questions, so the sample is small.

## Tools and subagent

- **`search(query)`**: returns the 5 closest chunks with norm, article and score. It loads the saved index and never re-embeds the corpus.
- **`add_document(path)`**: cuts and embeds a new file with the same code as `index.py` and adds it to the index.
- **One search result** (query "designacion coordinador seguridad salud ejecucion obra promotor"): `RD 1627/1997, Artículo 3 (score 0.801)`, with the text of Art. 3, including "el promotor, antes del inicio de los trabajos o tan pronto como se constate dicha circunstancia, designará un coordinador...".
- **Subagent** (`.claude/agents/corpus-researcher.md`): it can only use `search`. Its instructions: search every question in Spanish, answer only from the passages, cite norm and article, give figures only if they appear in a passage, and if the passages do not answer, say "No consta en los documentos del corpus".
- **Transcript from my editor**: I asked "¿Quién designa al coordinador de seguridad y salud durante la ejecución de la obra?". The subagent called `search` once and got 5 passages (RD 1627/1997 Arts. 3, 9, 2 and 14, and Ley 32/2006 Art. 3). It answered "Lo designa el promotor" and cited Art. 3.2 (when), Art. 2.1.f and Ley 32/2006 Art. 3.d (who the coordinator is) and Art. 3.4 (the promoter is not released). I checked each citation against the BOE.

## Adding a document

- **Already indexed**: I asked the agent to add `corpus/BOE-A-1997-22614.xml` (RD 1627/1997), which is already in the index. After my approval it answered that the document was already indexed (49 chunks) and added nothing. No embeddings were used and the index did not change.
- **Unanswerable question**: "¿Qué carnet o formación específica necesita un operador de grúa torre?"
- **Before**: "No consta en los documentos del corpus" (correct refusal).
- **Document added**: RD 836/2003 (45 new chunks), after my approval.
- **After**: correct answer from Art. 7 and Annex VI: the carné de gruista, 200 hours of course (50 theory and 150 practice), valid five years and in all of Spain. I checked every number in the XML.
- Afterwards I restored the original index.

## Harness and guardrails

- **Agent** (`agent.py`): LangChain on Gemini, tools over MCP, `AGENTS.md` as system prompt.
- **Rules in `AGENTS.md`** (each has its reason in the file): (1) search before answering; (2) answer only from the results; (3) cite every claim; (4) say "No consta en los documentos del corpus" if not covered; (5) never invent numbers, deadlines or articles; (6) search again if two passages are needed; (7) say if passages conflict; (8) do not call `add_document` unless asked; (9) answer briefly in the user's language. After my own tests I added (10) yes or no only if a passage says so; (11) apply rules step by step; (12) nearby is not covered; (13) cite the article that states the claim; (14) say "in the passages consulted" when reporting an absence; (15) cite annexes without invented point numbers.
- **Approval step**: before `add_document` runs, the agent asks "Allow? [y/N]" and does nothing unless I type `y`. It asked in the tower-crane test and in the already-indexed test.
- **Extra guardrails**: at most 6 tool calls per question, and `add_document` can only read files inside the project folder.
- **Case where the folder guard was tested**: I called the check directly: `/etc/hosts` gives False and `corpus/BOE-A-1997-22614.xml` gives True. In two live runs asking to add `/etc/hosts`, the model refused by itself before calling any tool, so the code guard did not need to fire. The guard is a second layer in case the model does not refuse.

## Evaluation

- **Code checks**: every citation in an answer must appear in the retrieved passages; a refusal is recognised by the phrase "No consta en los documentos"; an answer with no citation that is not a refusal is flagged.
- **Judge rubric**: an AI judge (`gemini-3.1-flash-lite`) sees the question, the reference answer, the retrieved passages and the answer. It gives `correct` (matches the reference, or refuses properly) and `supported` (every claim is backed by the passages).
- **My grades**: the first draft was written with Claude's help, and then I checked it against the BOE.

| Result (30 questions) | Value |
| :--- | :---: |
| Correct (judge and me) | 28/30 |
| Supported by the text (judge and me) | 29/30 |
| Correct on the 24 answerable | 24/24 |
| Proper refusals (of 6) | 4/6 |
| Wrong refusals | 0 |
| Citations found in the retrieved text | 100% |
| Judge and me agree on "correct" | 30/30 |
| Judge and me agree on "supported" | 28/30 |

- **New questions**: six everyday questions gave 4 good and 2 bad. For example, it said "yes" to dismissing a worker who refuses to wear a helmet, which the law does not say. I added rules 10-15 and a larger model, and these were fixed.
- **My own 9 questions**: 8/9 correct, 9/9 supported. The miss was the maximum fine, answered with the old pesetas table.
- **Limit**: the 30 answers come from a mix of models, because the free tier runs out of requests each day. Also, the judge and my grades both started from AI, so their agreement is weak evidence.

## Failures

| Cause | Count |
| :--- | :---: |
| Right article not found | 0 |
| Wrong answer from the right article | 0 (1 in the extra tests) |
| Claim not supported | 1 |
| Wrong refusal | 0 |
| Answered when it should refuse | 2 (q14 alcohol tests, q30 heat wave) |

In q14 and q30 the agent used nearby articles that do not really answer, and presented them as the answer.

**What to fix first**: (1) use the updated texts; (2) add a check in code: "does any passage really answer the question? If not, refuse" (a score threshold does not work: irrelevant passages score 0.75-0.77 and relevant ones 0.79-0.81); (3) use one larger model for the whole evaluation.

## Decision

I would let users use it as a **consultation aid** that points to the article, with a person reading the article before acting. I would not let it decide alone.

- **Good**: 28/30 correct, no wrong refusals, every claim has an article.
- **Not enough**: the test is easy, it sometimes answers when it should refuse, and the corpus is the original text. Never use it for fines or dismissals without checking the current BOE.
- **Cost and latency**: about 4,600 input and 480 output tokens per question, median 8.7 seconds. With the larger model, 4,700-11,400 input tokens and 11-143 seconds.

## AI use

I used Claude (chat and Claude Code).

- **Claude helped me with**: the questions, finding and checking information in the BOE, the code, the rules in `AGENTS.md`, the first draft of my grades, ideas to improve the model, checking that I had not missed anything, and the draft of this report.
- **I did**: the use case, the choice of `article`, the 9 extra questions (written before seeing any answer), checking the citations against the BOE and the numbers with `grep`, and the decision in the Decision section.