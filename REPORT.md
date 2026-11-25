# Assignment 3 Report

- **Name**: María Consolación Fernández
- **Student ID**: 20098
- **Group**: BBADBA 5B

## 1. Use case and corpus

**Use case.** I built an assistant for security, risk and compliance staff at a company that adopts AI features and has to document how it manages cyber and AI risk. They ask "what does NIST actually say about X?" (the functions of CSF 2.0, what GOVERN 1.1 requires, how SP 800-61r3 structures incident response, what an SSDF practice asks for) and then paste the answer into a policy, a vendor questionnaire or an audit response.

A wrong answer is worse than "I don't know" here. A made-up requirement or a misattributed page ends up in a document that an auditor or a customer will check against NIST's text, while "I don't know" costs one lookup in the PDF. So the assistant must cite page-level evidence for every claim and must refuse when the five documents do not cover the question (for example EU AI Act penalties, CIRCIA deadlines or password rules).

**Corpus.** Five publications of the US National Institute of Standards and Technology. They are works of the US federal government, not subject to copyright (17 U.S.C. §105), and contain no personal data beyond the authors' names on the cover. Page numbers in this project are **PDF page numbers** (page 1 = cover), not the ones printed in the margin.

| Document | URL | Date | Licence | Words (cleaned) |
|---|---|---|---|---|
| NIST AI 100-1, AI Risk Management Framework 1.0 | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf | 2023-01 | US gov. work, public domain | 15,398 |
| NIST AI 600-1, Generative AI Profile | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf | 2024-07 | same | 20,620 |
| NIST CSWP 29, Cybersecurity Framework 2.0 | https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf | 2024-02 | same | 8,951 |
| NIST SP 800-61 Rev. 3, Incident Response | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf | 2025-04 | same | 13,180 |
| NIST SP 800-218, SSDF Version 1.1 | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf | 2022-02 | same | 13,734 |
| **Total** | | | | **71,883** |

This is above the minimum of three documents and 50,000 words.

## 2. Ingestion: what the chunking does and what fails

`index.py` downloads the PDFs into `corpus/`, extracts each page with pypdf, cleans it and cuts it into **426 chunks** of about 220 words with 40 words of overlap (92 AI RMF, 123 GAI Profile, 52 CSF, 78 SP 800-61r3, 81 SSDF; about 8.8 MB of index). Each chunk keeps its source, title, URL, section (the last numbered heading seen) and page range, so every answer can be cited with the source id and the pages (for example nist-csf-2.0, pp. 9-10). The embedded text is the passage prefixed with its title and section, and vectors (`gemini-embedding-2`, 768 dimensions) are stored in ChromaDB.

**Why overlap.** A key sentence can fall exactly on the cut between two chunks. Without overlap, each chunk holds half of it: the embedding of each half is weaker, the keyword match is split across two chunks, and if only one is retrieved the model sees half a requirement and may invent the rest. With a 40-word overlap, the end of one chunk is repeated at the start of the next, so a sentence shorter than that appears whole in at least one of them. The price is a bit more than 18% extra chunks and some duplicated results. It does not help when the passage is longer than the overlap.

**Why cut at the end of a sentence.** Ending a chunk on a sentence boundary (when one is within 35 words) keeps ideas whole, so a chunk does not end mid-requirement. It also gives cleaner text for the embedding and for the model to quote.

**Why about 220 words.** A requirement such as GOVERN 1.1 usually fits in one chunk of that size. Chunks of about 100 words would split a requirement from its context. Chunks of about 500 words would mix several subcategories, blur the embedding, fill the prompt with irrelevant text (about 2,500 words at k = 5 instead of about 1,100) and make the page citation less precise. I did not re-index with 100 or 500 words, so this is a reasoned choice, not a measured one.

**Own finding.** The chunk for GOVERN 1.1 (pp. 27-28) mixes the introduction and subcategories 1.1 to 1.4, and is cut right before 1.5. Subcategories are short sentences, so 220 words do not isolate them. The question about GOVERN 1.1 still worked because the chunk contains the requirement, but a more precise chunk would be better.

**Noise that remained.** Measured over the five documents after chunking: "Continued on next page" appears 11 times, "Categories Subcategories" 15 times, "(Continued)" 11 times, and 2 capitalised words stay split by a line-break hyphen (for example "GOV- ERN"). I also did not fix the glued word "relevantcontext" that is in the AI RMF PDF itself (p. 18).

**Bug found and fixed.** When indexing on the day of submission, `index.py` failed: with `gemini-embedding-2`, sending a list of texts returned a single vector instead of one per text. Now each text is sent as its own content and the code checks that the number of vectors matches the number of texts.

**Extraction problems fixed.** (1) The AI RMF is justified text and splits words across lines ("re-" / "quires"). I rejoin them but keep the hyphen in real compounds ("high-risk"). (2) SP 800-61r3 and the CSF repeat a running header and page number on every page. Lines repeated on at least 30% of pages, bare page numbers and dot leaders are removed.

**With more time** I would cut by structure (at every "GOVERN x.y") instead of by word count, and clean the remaining noise.

## Test set

The test set has 33 questions in `eval/questions.csv`: 18 single-passage, 8 multi-passage
(four of them across two documents) and 7 unanswerable. Each has the expected source and
page and a short reference answer. The unanswerable questions stay close to the corpus
topic (for example CIRCIA reporting deadlines, EU AI Act penalties, TLS versions in the
SSDF, SOC 2 mapping to the CSF).

- Single: "Why is GOVERN drawn at the center of the CSF 2.0 Functions wheel?" (CSF, p. 9).
- Multi: "Which CSF 2.0 Function sits at the center of its wheel, and which AI RMF function
  is described as cross-cutting?" (CSF p. 9; AI RMF pp. 25 and 27).

The questions were drafted by Claude from passages it read in the PDFs, with page numbers. I used them as they were and did not rewrite them. I did not re-check every expected page against the PDFs myself, which is a limitation: the two expected-page mismatches found by the code check (q10 and q23, see section 6) may be errors in the questions rather than retrieval failures.

## 3. Retrieval: the decision

I compared three designs over the same chunks and vectors: `dense` (cosine over Gemini vectors), `bm25` (keywords) and `hybrid` (reciprocal-rank fusion of both, k = 60). A hit means every expected passage (source and page) is in the top k. There are 26 answerable questions.

| Design | Hit@1 | Hit@3 | Hit@5 | Multi-passage questions @5 | Avg. words in prompt @5 |
|---|---|---|---|---|---|
| dense | 0.654 | 0.846 | 0.846 | 4/8 | 1,047 |
| bm25 | 0.385 | 0.577 | 0.615 | 5/8 | 1,031 |
| hybrid | 0.462 | 0.731 | 0.808 | 5/8 | 1,046 |

**My choice: dense.** It has the best hit rate at k = 5 (0.846 vs 0.808) and a much better hit@1 (0.654 vs 0.462). The cost in prompt words is about the same, because every design returns 5 chunks of similar size. Hybrid does better only on two-passage questions (5/8 vs 4/8), a difference of one question out of eight, which is too small to base a decision on. For my use case, getting the right passage first matters more, since users copy what they read.

**What I used in the evaluation.** The MCP tool was set to `hybrid` with k = 5, so the evaluation ran with hybrid, which is **not** the design I would choose from these numbers. I did not re-run the evaluation with dense; this is a limitation of the results below.

## 4. Tools, subagent, add_document and guardrails

`server.py` exposes two tools over MCP (stdio), registered as `corpus`:

- **`search(query)`** returns the 5 most relevant passages, best first, each with its citation tag (source and location), the section and a score.
- **`add_document(path)`** adds a local `.pdf/.txt/.md/.html` file to the index. It decides before embedding anything. The same content already indexed (SHA-256) does nothing and says "Already indexed". The same name with different content replaces the old chunks. A new file is chunked, embedded, stored and made searchable at once. Files over 40,000 words are refused to protect the 1,000-embeddings-a-day quota.

**Guardrails:**

- Human approval before `add_document` (`HumanInTheLoopMiddleware`); with no terminal the answer is no.
- A limit of 8 model calls per run (`ModelCallLimitMiddleware`); it triggered once (q08).
- A path allowlist (`corpus/` and `extra/`), checked in the agent before asking a human and again in the server, in case a poisoned passage tries to make the agent index `.env` or `~/.ssh`.

**`/etc/passwd` test.** I asked the agent twice to add `/etc/passwd`. Both times the model refused by itself, without calling any tool (0 tool calls), citing rule 7 of `AGENTS.md` and the allowed folders, so the code-level guardrail did not need to fire. I then tested the allowlist function directly:

```
check_add_path('/etc/passwd')            -> Refused: add_document only reads files inside corpus/, extra/
check_add_path('../.env')                -> Refused: add_document only reads files inside corpus/, extra/
check_add_path('corpus/nist-csf-2.0.pdf') -> accepted
```

**Subagent transcript:** not completed before the deadline.
**Demo of q27 (adding SP 800-63B):** not completed before the deadline. q27 stays unanswerable in the evaluation, and the agent refused it correctly.

## 5. Evaluation

`evaluate.py` ran all 33 questions through the agent: 18 single-passage, 8 multi-passage and 7 unanswerable.

- 33 answers, of which 7 are refusals (q27 to q33). q08 hit the call limit.
- Average per question: about 7,769 input tokens, 182 output tokens and 10.6 seconds.

**Code checks.**

- The agent searched: 33/33.
- Has a citation or is a refusal: 32/33 (q08 hit the call limit and gave no answer).
- Within the call limit: 32/33.
- Expected passage retrieved: 24/26 answerable questions (misses: q10, q23).
- All cited tags among the retrieved chunks: 24/33. Of the 9 failures, 8 are tag-format problems (a single page where a range was retrieved, or merged ranges: q09, q20, q21, q23, q25, q29, q32, q33) and 1 is real: q19 cites AI RMF p. 42, which was not retrieved.

**LLM judge.** The judge could not be run before the deadline: Gemini returned `503 UNAVAILABLE` (high demand) for `gemini-3.8-flash` (the default) and for `gemini-3.5-flash`. The answers are saved, so `uv run python main.py evaluate` runs only the judging step once the service recovers. The judge's counts, the agreement with my grades and kappa are therefore **not reported here**.

**My grading.** The grades in `eval/human_labels.csv` were first proposed by Claude from the questions, the references, the agent's answers and the list of retrieved citations in `eval/grading_sheet.md`. I adopted them and wrote them into the file without seeing any judge verdict, because the judge had not run. I changed one decision: q19 is correct but I set `supported = 0`, because it cites AI RMF p. 42, which was not retrieved, even though the content is on pp. 26-27, which were. My use case says a misattributed page is one of the worst errors, so I applied the strict criterion. By these grades, 24 of the 26 answerable questions are correct and supported, q19 is correct but unsupported, q08 is the failure (no answer), and all 7 unanswerable ones are refused correctly. These grades are therefore not fully independent of the AI, and I report them as such.

## 6. Failures

**q08** ("How many risks unique to or exacerbated by generative AI does the GAI Profile define?"). The agent ran out of calls (8/8) and gave no answer. The expected pages (pp. 8-9 of the GAI Profile) were only partly among the retrieved chunks: pp. 7-8 cover p. 8, and no retrieved chunk covers p. 9. The agent kept searching instead of answering, which makes it a call-limit/loop problem and a wrong refusal. I did not open the PDF to check whether the question is badly posed because the number may be spread over several passages, so I classify it as a wrong refusal and leave open that the question is a contributing factor.

**Citations not among the retrieved chunks (q09, q19, q20, q21, q23, q25).** Most look like citation format, not unsupported claims. The page was covered by a retrieved range but the tag differs: a merged range (q09 "pp. 11-12, 8"; q21 "pp. 11-14"), or a single page for a retrieved range (q20 and q25 "p. 25" vs "pp. 24-25"; q23 "p. 15" vs "pp. 15-16"). The one real case is **q19**, which cites AI RMF p. 42, a page that was not retrieved, although the content is on pp. 26-27, which were.

**Expected passage not retrieved (q10, q23).** The code check found that the expected page was not among the retrieved chunks. In both cases the agent's answer matched the reference, and the pages it cited were retrieved. This suggests that the expected page in `questions.csv` may be off by one page, rather than a real retrieval failure, but I did not open the PDFs to confirm it, so I count them as possible bad test questions, not confirmed ones.

**Refusals with a citation (q29, q32, q33).** I consider them correct. They refuse and only cite pages that were covered by retrieved chunks, to explain what the documents do cover. The code flags them only because the tag is a single page where a range was retrieved. q31 also refuses correctly and then lists the Protect categories from CSF p. 20, which is true but not requested.

**Minor:** q10 omits "anthropomorphizing" from the Human-AI Configuration definition, though the rest is right.

**Classification.** Confirmed retrieval misses: 0 (q10 and q23 are flagged by the code, but are probably wrong expected pages). Bad answer from a good passage: 0 (q10 partly). Unsupported claim: 1 (q19, p. 42). Wrong refusal: 1 (q08). Possible bad test questions: 2 (q10, q23), not confirmed.

**What I would fix first:** the call limit and the loop in q08 (stop and answer with what has been found), then make citations exact (the same tag format as the retrieved chunks), because users copy them. After that I would check the expected pages of q10 and q23 in the PDFs.

## 7. Decision

I would not let an auditor rely on this without checking. It is useful for **finding the passage** quickly: by my grades, 24 of 26 answerable questions were right and supported, and all unanswerable ones were refused. It is not safe for **copying without checking**, because one answer never appeared (q08), one citation pointed to a page that was not retrieved (q19) and the evaluation is small (33 questions), ran with hybrid retrieval instead of the design I prefer, and was graded without the judge, using grades first proposed by the AI.

**Safeguards I would add:**

- Always show the page and check that each cited tag was actually retrieved.
- Stop the loop and answer with a refusal when the call limit is near.
- A notice in every answer: "Check the quote against the PDF page before using it in an audit document."

**Cost and speed.** About 7,769 input and 182 output tokens per question, and 10.6 seconds on average. With the standard paid-tier price of Gemini 3.5 Flash-Lite (US$0.30 per million input tokens and US$2.50 per million output tokens, from Google's Gemini API pricing page, https://ai.google.dev/pricing), one question costs about 7,769 / 1,000,000 × 0.30 + 182 / 1,000,000 × 2.50 ≈ US$0.0028, or about US$2.8 per 1,000 questions. On the free tier it is free. This counts only the agent's tokens, not the judge or the query embeddings. The index cost about 426 embeddings, within the 1,000-a-day free quota.

