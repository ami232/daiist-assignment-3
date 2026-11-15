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

Version 1 used the original BOE text. Version 2 (the one I deliver) uses the **consolidated** (updated) text from the BOE open-data API, downloaded on 15 Nov 2026. The manifest `index/corpus_manifest.json` stores the download date, the update date and a hash (sha256) of each file.

| Document | URL | Published | Consolidated up to | Licence | Words (approx.) |
| :--- | :--- | :--- | :--- | :--- | :---: |
| Ley 31/1995 | https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-1995-24292 | 8 Nov 1995 | 6 Nov 2026 | BOE reuse terms | 41,117 |
| RD 39/1997 | https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-1997-1853 | 17 Jan 1997 | 15 Oct 2026 | BOE reuse terms | 36,205 |
| RD 1627/1997 | https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-1997-22614 | 24 Oct 1997 | 18 Dec 2025 | BOE reuse terms | 17,182 |
| RD 1215/1997 | https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-1997-17824 | 18 Jul 1997 | 18 Dec 2025 | BOE reuse terms | 13,807 |
| Ley 32/2006 | https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2006-18205 | 18 Oct 2006 | 18 Dec 2025 | BOE reuse terms | 6,891 |
| **Total** | | | | | **115,202** |

The word counts come from stripping the XML tags, so they include metadata and may include older versions of articles that the consolidated format keeps. They are not comparable with the 58,682 words of version 1, and they overstate the real text.

- **Why these**: they refer to each other, so some questions need two passages.
- **Licence**: BOE content can be reused if the source is cited and the meaning is not changed. Source: https://www.boe.es/informacion/aviso_legal/index.php
- **Personal data**: none, they are laws.
- **Why I changed the corpus**: in version 1 the original text was missing later articles (for example the "recurso preventivo", Art. 32 bis) and the fines table was still in pesetas. The consolidated text fixes this. It also shows that the promoter notice of RD 1627/1997 (Art. 18) is repealed and replaced by the opening communication (Art. 19), and that the fines articles of Ley 31/1995 (Art. 46-52) are repealed, so the corpus has no fine amounts.
- **Limitation**: the corpus is only as current as the dates above. Laws change, so it must be downloaded again from time to time.
- **Versions**: version 1 is saved in the git tag `baseline-v1`. Version 2 is the branch I deliver.

## Ingestion

- **Steps** (`index.py`): download the XML through the API (it needs the header `Accept: application/xml`), read it, clean the spaces, cut it into chunks, embed each chunk with Gemini `gemini-embedding-2` and store it in ChromaDB. The script reads both formats, the consolidated one and the original one, which `add_document` still uses.
- **Two designs**: `article` (one chunk per article, 334 chunks, 9 of them short stubs of repealed articles) and `fixed` (windows of 150 words with 30 words of overlap, 576 chunks).
- **Metadata**: each chunk has its norm (`source`) and article (`location`), and its text starts with them, so the citation travels with the text.
- **Stable index**: chunk ids are deterministic and, after indexing, old chunks are removed, so no text from an older version stays in the index.
- **Extraction problems I fixed**: (1) in version 1, additional provisions and annexes sat under group headings and were attached to the previous article; now each one has its own location. (2) In version 2, a bug in how the annex of Ley 32/2006 was read in the consolidated format.

## Test set

45 questions in three sets:

| Set | File | Questions | Should refuse |
| :--- | :--- | :---: | :---: |
| Dev | `eval/questions.csv` | 30 | 6 |
| Held-out (my own) | `eval/heldout_questions.txt` | 9 | 3 |
| Fresh (written after the coverage check) | `eval/fresh_questions.txt` | 6 | 2 |

The dev set has 19 simple questions, 5 that need two passages and 6 that the corpus cannot answer.

**How I wrote them**: Claude suggested the format. I wrote the questions, Claude corrected and improved them, and then I checked them against the BOE text and changed 5. The 9 held-out and 6 fresh questions were written before seeing any answer.

- **Example, answerable**: "¿Quién designa al coordinador de seguridad y salud durante la ejecución de la obra?" Expected: the promoter (RD 1627/1997, Art. 3).
- **Example, unanswerable**: "¿Qué carnet o formación específica necesita un operador de grúa torre?" Expected: "No consta en los documentos del corpus".
- **References changed by the new corpus**: q05, h05 and h08. I checked each one in the consolidated text and listed them in `eval/reference_changes.md`. For example, q05 now expects "the promoter notice (Art. 18) is repealed; the opening communication (Art. 19) is filed only by contractors, before the work starts".

The dev questions come from the same text as the corpus, so they are easier than real questions. That is why I also use the held-out and fresh sets.

## Retrieval

Is the right article in the top k results? (34 answerable questions: 24 dev, 6 held-out, 4 fresh)

| Design | top 1 | top 3 | top 5 |
| :--- | :---: | :---: | :---: |
| `article` | 0.676 | 0.853 | 0.912 |
| `fixed` | 0.529 | 0.647 | 0.824 |

- **I chose `article`**: it wins at every k. On the 24 dev questions alone it finds the right article in the top 5 every time (24/24, the same as in version 1).
- **Weak point**: on my 6 answerable held-out questions, both designs find the right article in the top 5 only 3 times. Retrieval is clearly worse on questions I did not use while building the system.
- **Words added to the prompt**: each search returns 5 chunks. `article` chunks are longer than the 150-word `fixed` windows, so each search puts more text in the prompt. I did not measure tokens in version 2 (in version 1 the average was 4,598 input tokens per question).
- **Why `fixed` fails more**: in version 1 it missed 5 questions in the top 5 (q07, q11, q12, q26, q27). Four need two passages, so the five results fill up with windows of the same article and the second norm does not fit. The fifth (q07) is a long article cut into windows. This is my explanation and I did not test it further.

## Tools and subagent

- **`search(query)`**: returns the 5 closest chunks with norm, article and score. It loads the saved index and never re-embeds the corpus.
- **`add_document(path)`**: cuts and embeds a new file with the same code as `index.py` and adds it to the index.
- **Subagent** (`.claude/agents/corpus-researcher.md`): it can only use `search`. Its instructions: search every question in Spanish, answer only from the passages, cite norm and article, give figures only if they appear in a passage, and if the passages do not answer, say "No consta en los documentos del corpus".
- **Transcript from my editor** (done with the version 1 index; the tools and the subagent did not change in version 2): I asked "¿Quién designa al coordinador de seguridad y salud durante la ejecución de la obra?". The subagent called `search` once and got 5 passages (RD 1627/1997 Arts. 3, 9, 2 and 14, and Ley 32/2006 Art. 3). It answered "Lo designa el promotor" and cited Art. 3.2 (when), Art. 2.1.f and Ley 32/2006 Art. 3.d (who the coordinator is) and Art. 3.4 (the promoter is not released). I checked each citation against the BOE.

## Adding a document

(Done with the version 1 index. The tool did not change in version 2.)

- **Already indexed**: I asked the agent to add `corpus/BOE-A-1997-22614.xml` (RD 1627/1997), which is already in the index. After my approval it answered that the document was already indexed and added nothing. No embeddings were used and the index did not change.
- **Unanswerable question**: "¿Qué carnet o formación específica necesita un operador de grúa torre?"
- **Before**: "No consta en los documentos del corpus" (correct refusal).
- **Document added**: RD 836/2003 (45 new chunks), after my approval.
- **After**: correct answer from Art. 7 and Annex VI: the carné de gruista, 200 hours of course (50 theory and 150 practice), valid five years and in all of Spain. I checked every number in the XML.
- Afterwards I restored the original index.

## Harness and guardrails

- **Agent** (`agent.py`): LangChain on Gemini, tools over MCP, `AGENTS.md` as system prompt.
- **Rules in `AGENTS.md`** (each has its reason in the file): (1) search before answering; (2) answer only from the results; (3) cite every claim; (4) say "No consta en los documentos del corpus" if not covered; (5) never invent numbers, deadlines or articles; (6) search again if two passages are needed; (7) say if passages conflict; (8) do not call `add_document` unless asked; (9) answer briefly in the user's language. After my own tests I added (10) yes or no only if a passage says so; (11) apply rules step by step; (12) nearby is not covered; (13) cite the article that states the claim; (14) say "in the passages consulted" when reporting an absence; (15) cite annexes without invented point numbers; and in version 2 (16) the coverage check below.
- **Coverage check (new in version 2)**: in version 1 the agent answered when it should refuse (alcohol tests, heat waves), using nearby articles. A score threshold does not work (irrelevant passages score 0.75-0.77, relevant ones 0.79-0.81). So after each search, a small model (`gemini-3.5-flash-lite`) reads the passages and says YES, PARTIAL or NO to "does any passage answer the question?". The code, not the model, extracts the quote from the numbered sentences. If the result is NO for every search, the code forces the fixed refusal "No consta en los documentos del corpus" plus what was searched, and throws away the model's own text. If the check fails (quota, timeout), it does not refuse. I tuned the prompt in four versions (v1-v4) on the dev set and then tested it on the fresh questions: 0 wrongly covered and 0 wrong refusals among the 4 answerable.
- **Approval step**: before `add_document` runs, the agent asks "Allow? [y/N]" and does nothing unless I type `y`. It asked in the tower-crane test and in the already-indexed test.
- **Extra guardrails**: at most 6 tool calls per question, and `add_document` can only read files inside the project folder.
- **Case where the folder guard was tested**: I called the check directly: `/etc/hosts` gives False and `corpus/BOE-A-1997-22614.xml` gives True. In two live runs asking to add `/etc/hosts`, the model refused by itself before calling any tool, so the code guard did not need to fire. The guard is a second layer in case the model does not refuse.

## Evaluation

- **One model**: all 45 answers come from one model (`gemini-3.5-flash-lite`), so the run is consistent. It ignores temperature, so a new run can differ slightly.
- **Code checks**: every citation in an answer must appear in the retrieved passages (norm and article); a refusal is recognised by the phrase "No consta en los documentos"; an answer with no citation that is not a refusal is flagged. The code does not check that the content matches the citation.
- **Judge rubric**: an AI judge (`gemini-3.1-flash-lite`) sees the question, the reference answer, the retrieved passages and the answer. It gives `correct` (matches the reference, or refuses properly) and `supported` (every claim is backed by the passages).
- **My grades**: I reviewed all 45 answers. Where I doubted, I checked the consolidated BOE text, and I corrected one of my own grades (h05, the judge was right). I wrote my grades after seeing the judge's verdicts, so the agreement below is **not blind**.

| My grades | Correct | Supported by the text |
| :--- | :---: | :---: |
| Dev (30) | 28/30 | 30/30 |
| Held-out (9) | 6/9 | 9/9 |
| Fresh (6) | 6/6 | 6/6 |
| **Total (45)** | **40/45** | **45/45** |

- **Judge and me agree**: 44/45 on "correct" (the judge was too soft on h04) and 45/45 on "supported".
- **Dev, refusals**: 5 of 6 proper refusals. It still answers the alcohol-test question (q14).
- **Caution on "supported"**: a forced refusal claims nothing, so it counts as supported. The 45/45 is partly because the system now refuses more.
- **Fresh set**: only 6 questions, so it proves little.

**Version 1 against version 2 on the dev set**

| | v1 | v2 |
| :--- | :---: | :---: |
| Correct | 28/30 | 28/30 |
| Supported | 29/30 | 30/30 |
| Proper refusals (of 6) | 4/6 | 5/6 |
| Answered when it should refuse | 2 | 1 (q14) |
| Wrong refusals (of 24) | 0 | 1 (q05) |

The scores are almost equal, and the comparison is **not clean**: the corpus, the models, three references and the verifier all changed between the two runs. Only q05, q28 and q30 changed verdict. I cannot say which change caused what.

**How to run it again**: the repo includes the answers and judge results in `eval/` (`answers_v2.json`, `judge_v2.json`, `results_v2.csv`, `summary_v2.json`). To run it: `uv run python evaluate.py --tag v2 --sets dev,heldout,fresh --model gemini-3.5-flash-lite --judge-model gemini-3.1-flash-lite`. It needs a Gemini API key in `.env`, which is not in the repo.

## Failures

5 of 45 answers are not correct:

| Cause | Count | Questions |
| :--- | :---: | :--- |
| Answered when it should refuse | 1 | q14 (alcohol tests) |
| Wrong refusal (the question had a false premise) | 2 | q05, h04 |
| Right article not retrieved | 2 | h01 (incomplete), h08 |
| Claim not supported | 0 | |

- **q14**: the coverage check takes a nearby article (Art. 22) as an answer.
- **q05 and h04**: the right answer corrects the question ("the old notice no longer exists" / "the coordinator approves the plan"). The check sees no passage that answers the literal question and refuses. This is a weakness of the check.
- **h08**: the agent refuses safely but does not say that Art. 49 is repealed, because the stub of the repealed article was not retrieved.
- **h01**: retrieval did not bring Art. 7 of Ley 32/2006, so the answer is incomplete.
- **Also seen**: in h06 one search used the query "None".

**What to fix first**: (1) improve retrieval on held-out-style questions (for example, query rewriting); (2) let the check recognise a passage that corrects a false premise; (3) test the check with a stronger model than the one that answers.

## Decision

I would let users use it as a **consultation aid** that points to the article, with a person reading the article before acting. I would not let it decide alone.

- **Good**: 40/45 correct, every claim has an article, no claim was unsupported, and the corpus is the current text.
- **Not enough**: held-out retrieval is weak, the fresh test is tiny, it still answers one question it should refuse, and the verifier is a small model. Never use it for fines or dismissals without checking the current BOE.
- **Cost and latency**: for the 45 questions, 110 agent calls, 50 coverage calls, 49 judge calls and 63 embedding calls. The coverage check adds one model call per search. I did not measure tokens or time in version 2. In version 1 it was about 4,600 input and 480 output tokens per question, median 8.7 seconds, without the check. The free tier limits requests per day.

## AI use

I used Claude (chat and Claude Code).

- **Claude helped me with**: the questions, finding and checking information in the BOE, the code (including the coverage check and the consolidated parser), the rules in `AGENTS.md`, the first draft of my grades, ideas to improve the model, checking that I had not missed anything, and the draft of this report.
- **I did**: the use case, the choice of `article`, the 9 held-out and 6 fresh questions (written before seeing any answer), my own review of the grades against the BOE text, the correction of my own grade for h05, and the decision to deliver version 2 and report its limits honestly.