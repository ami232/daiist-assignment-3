# Assignment 3 Report

- **Name**: Sofia Serantes Vázquez
- **Student ID**: 19523
- **Group**: BBADBA 5A 

## Use case

The users are HR and People Analytics staff in a company operating in the EU. They ask whether a planned use of AI or employee data is allowed and what they must do, for example “does an employer have to tell workers before using an AI system to monitor them?” or “what must we tell candidates about pay?”. They use the answer to decide whether to launch, change or stop an HR process, and to know which article to check with legal. The agent answers from three EUR-Lex documents (AI Act, GDPR and Pay Transparency Directive) retrieved at question time. It covers the EU text only, not national law.

A wrong answer is costly: a false “yes, you can” can lead to a prohibited practice, for example workplace emotion recognition, AI Act Article 5, or a GDPR / AI Act breach with fines. A false “no” blocks a legitimate project. “I don’t know” costs only a delay and a consultation with a lawyer, so the assistant must refuse when the documents do not cover the question and must cite every claim so HR can check the source.

## Corpus

 
| Document | URL | Date | Licence | Words (full act) | Words in scope |
|---|---|---|---|---|---|
| AI Act, Regulation (EU) 2024/1689 (Chapters I, II, III, IV, XII and Annex III only) | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | 13 June 2024 (OJ 12.7.2024) | EUR-Lex reuse policy (Commission Decision 2011/833/EU), source acknowledged | 91,544 | 25,547 |
| GDPR, Regulation (EU) 2016/679 (all articles) | https://eur-lex.europa.eu/eli/reg/2016/679/oj | 27 April 2016 (OJ 4.5.2016) | same | 55,812 | 29,466 |
| Pay Transparency Directive (EU) 2023/970 (all articles) | https://eur-lex.europa.eu/eli/dir/2023/970/oj | 10 May 2023 (OJ 17.5.2023) | same | 14,235 | 5,603 |
| **Total** | | | | **161,591** | **60,616** |
 
Total in scope: 60,616 words (minimum 50,000). Scope decision: the corpus covers the parts of the law HR uses most. Recitals, national (e.g. Spanish) law and the AI Act chapters on general-purpose models, sandboxes, governance and final provisions are left out. The documents contain no personal data. The word counts come from uv run python index.py --chunks-only.
 
The three PDFs are committed in data/ instead of being downloaded by index.py, because EUR-Lex blocks scripted downloads and main.py index must run with no manual steps. 

## Ingestion

**Extraction.** pypdf reads each PDF page by page, so every chunk keeps its page numbers. The cleaner removes the Official Journal running headers and footers (several layouts, including the AI Act's `ELI: http://data.europa.eu/eli/reg/2024/1689/oj 46/144` footer), cuts the footnotes at the bottom of each page, removes footnote markers split over three lines, normalises non-breaking hyphens and spaces, and rejoins words hyphenated across lines. The recitals are dropped: the text starts after "HAVE ADOPTED THIS REGULATION/DIRECTIVE".
 
**Structure and chunking.** Regular expressions find chapters, sections, articles and annexes. Articles outside the chosen scope are discarded. The chosen design makes one chunk per article, split at numbered paragraphs when the article exceeds 300 words, and a short last piece (under 50 words) is merged into the previous chunk. Each chunk starts with a header line (law > chapter > section, article title) so the embedding knows its context, e.g. `GDPR > Chapter III – Rights of the data subject > Section 4 … / Article 22: Automated individual decision-making, including profiling`

**Extraction problem fixed.** The PDFs have repeated headers and footers on every page, pypdf extracts them as normal text in the middle of the article often between two halves of a sentence. Some examples are:
- GDPR: `4.5.2016 L 119/32 Official Journal of the European Union EN`
- Pay Transparency: `EN Official Journal of the European Union L 132/42 17.5.2023`
- AI Act: `OJ L, 12.7.2024 EN plus the footer ELI: http://data.europa.eu/eli/reg/2024/1689/oj 46/144`

This matters because it generates noise. The noise ended up inside the chunks, for example in Article 26 of the AI Act. This has three effects: it breaks sentences in two, it adds meaningless words to the embedding and it would create false matches for keyword search since "Official Journal" appears on every page.  

The issue was fixed useing `clean_page`, it drops these lines with a pattern for each layout. There were three different layouts and the header words appear in a different order in each law. After cleaning, a search through all the 319 chunks found no header or footer lines left. The only "Official Journal" mentions left are legal text such as "published in the Official Journal". 

**Metadata per chunk.** source, doc_title, url, kind, number, title, chapter, section, location (for example:"Article 26(1)-(4)"), pages (for example: "67-68"), words and a content hash. Chunks are embedded with `gemini-embedding-2` (768 dimensions, task type `RETRIEVAL_DOCUMENT`; queries use `RETRIEVAL_QUERY`) and stored in `ChromaDB` with cosine distance, one collection per design. Vectors are saved after every batch of 50 in `index/vectors.jsonl`, keyed by a hash of the chunk text, so `main.py index` only embeds chunks without a saved vector. The index is about 19 MB.

**Number of chunks.**
 
| Design | AI Act | GDPR | Pay Transparency | Total |
|---|---|---|---|---|
| articles (chosen) | 119 | 157 | 43 | **319** |
| windows (200 words, 40 overlap) | 160 | 184 | 35 | **379** |

## Test set

30 questions in `eval/questions.csv`: **17 single, 7 multi, 6 unanswerable**.
 
| Kind | AI Act | GDPR | Pay Transparency | Two laws |
|---|---|---|---|---|
| single | 8 | 4 | 5 | |
| multi | 1 (Art. 6 + Annex III) | | | 6 (5 AI Act + GDPR, 1 Pay Transparency + GDPR) |
| unanswerable | | | | 6 (no expected source) |

The questions were written before running any retrieval evaluation. First, I went through all the articles and HR/People Analytics would need were analysed and went through. From AI Act: Art. 3 (provider vs deployer), 4 (AI literacy), 5 (emotion recognition ban), 6 + Annex III (high-risk), 14 (human oversight), 25 (putting your logo on a tool), 26 (log retention), 50 (chatbot transparency). From GDPR: Art. 12 (deadline to answer), 15 (copy of the HR file), 17 (deleting a CV), 30 (records of processing). From Pay Transparency:Art. 5 (pay-history question), 7 (pay information and gag clauses), 9 (reporting dates), 10 (joint pay assessment).

The process was first writing one question per article with an HR language rather than using law's words. For example, “software that reads employees’ facial expressions” instead of “emotion recognition”, and “how much they earn in their current job” instead of “pay history”. The I thought of different situations an HR would use the agent, some of this situations are: an AI tool that auto-rejects CVs (Annex III + GDPR Art. 22), what to do before a performance-scoring tool goes live (AI Act Art. 26(7) + GDPR Art. 35), reusing pay-gap data for an attrition model (Pay Transparency Art. 12 + GDPR Art. 5), what to tell candidates (AI Act Art. 26(11) + GDPR Art. 13), maximum fines (AI Act Art. 99 + GDPR Art. 83).

Thee reference answers were written by me with the article and paragraph. 

For the unanswerable questions I chose questiosn that HR would ask on the same topic but that are not on the corpus.The unanswerable topics I chose were the following:Spanish law (q26, q27, q30), excluded AI Act chapters (q28, q29) and application dates (q09).

I checked each one against the indexed text to make sure the corpus does not answer it. Here are two examples, one that can be answered and the other unanserable:
- q21:“We’re about to switch on an AI tool that scores employee performance. What do we need to do before it goes live?”
  - Source: ai_act;gdpr. Location: Article 26;Article 35.
  - Reference: inform workers’ representatives and affected workers before use (AI Act 26(7)), and carry out a DPIA (GDPR 35(1), (3)(a)).
- q28:“We fine-tuned an open-source LLM for HR use. Do we need to publish a summary of the data it was trained on?”
  - No source
  - Reference: the corpus doesn’t cover general-purpose AI model obligations (AI Act Chapter V excluded), so the assistant should say it doesn’t know.

The corrections made after checking the answers were that q09 changed to unanswerable because Art. 113 is outside the corpus; q04 changed to multi; q20 reduced to the two passages it uses; q14’s reference reworded to what Art. 30(5) says; “none” changed to empty for unanswerable rows.

## Retrieval

Three configurations were compared with `main.py evaluate`. A question is a hit when all its expected passages (source + article/annex) are in the top k; 24 answerable questions, unanswerable ones excluded.
 
| Design | hit@1 | hit@3 | hit@5 | multi hit@5 (both passages) | avg words added at k=5 | mean top-1 distance (answerable / unanswerable) |
|---|---|---|---|---|---|---|
| **articles** (one chunk per article, vector) | **0.542** | **0.708** | **0.792** | **0.286** (2/7) | 993 | 0.232 / 0.267 |
| windows (200 words, 40 overlap, vector) | 0.542 | 0.708 | 0.750 | 0.143 (1/7) | 1,000 | 0.279 / 0.297 |
| articles + BM25 (hybrid, rank fusion) | 0.417 | 0.583 | 0.708 | 0.286 (2/7) | 991 | 0.242 / 0.285 |
 
Numbers: `eval/retrieval_summary.csv`. The hybrid configuration fuses the vector ranking and a BM25 keyword ranking with Reciprocal Rank Fusion (score = Σ 1/(60 + rank)) and costs no extra embeddings. The chosen configuration is articles + vector search (`ACTIVE_DESIGN = "articles"`, `ACTIVE_MODE = "vector"`).

**Choice** I chose articles + vector search. At k=1 and k=3 it ties with windows (0.542 and 0.708 both). At k=5 it’s better: 0.792 vs 0.750, which is one more question (19 vs 18 out of 24). On multi questions it finds both passages in 2 of 7, vs 1 of 7 for windows. Its top-1 distance is lower (0.232 vs 0.279), so the best result is closer to the question.
Every chunk is one article so citations are exact and it needs fewer chunks for about the same words in the prompt. 
With only 24 answerable questions, one question is about 4 percentage points. The difference between articles and windows is a single question, so it’s weak evidence. The two designs differ in two ways: where chunks are cut, and the header line that only article chunks have.

The hybrid model was the worst on every hit rate: hit@1 0.417 vs 0.542, and hit@5 0.708 vs 0.792. I wrote the questions in everyday HR language, not the law’s words. Keyword search rewards exact word matches so it pushed up chunks that shared common words like “employees” or “AI system” and pushed the right articles down. Embeddings match meaning across different wording so vector search alone did better.

Mean top-1 distance shows that 0.232 for answerable questions and 0.267 for unanswerable ones. The gap is too small to set a rule like “refuse if distance > X” without wrongly refusing many real questions.So refusals can’t come from the retriever they must come from the agent reading the passages and deciding they don’t answer the question. That’s why `AGENTS.md` has the refusal rule.

Only 2 of 7 multi questions get both passages in the top 5, because one search rarely brings back articles from two different laws. That’s why rule 1 of `AGENTS.md` asks the agent to search once per law or per part of the question.

## Tools and subagent
**MCP server** (`server.py`, server name `corpus`): loads `index/` at start-up, never re-embeds the corpus, logs only to stderr.
 
- `search(query, source="")`. Tool description (docstring):
  > Search EU law for HR and people-analytics questions: the AI Act (definitions, prohibited practices, high-risk AI systems incl. Annex III employment uses, provider/deployer obligations, transparency, penalties), the GDPR (all articles), and the Pay Transparency Directive (all articles). Recitals, national (e.g. Spanish) law and the AI Act chapters on general-purpose AI models, sandboxes, governance and final provisions are NOT included. Use it before answering any question about these laws. For a question with several parts (e.g. AI Act and GDPR), call it once per part. … Returns the 5 most relevant passages, each with a citation [source, Article/Annex, page] and a distance (lower = closer match).
  A `source` filter also matches documents added later about the same law (`ai_act` matches `ai_act_final_provisions`).
- `add_document(path)`. Tool description:
  > Add a document (PDF or .txt) to the searchable index. The file is extracted, cleaned and chunked by article (or by page if it has no articles), embedded and stored, so `search` can find it right away. The file name without extension becomes its source name in citations. If the same file was already added with the same content, nothing changes; if its content changed, the old version is replaced.
  It imports `chunk_file` and `embed_and_store` from `index.py`, so the pipeline is not rewritten.
**One search result** (q01, first of 5):
```text
Result 1 [ai_act, Article 3(1)-(6), p. 46] (distance 0.1975)
AI Act > Chapter I – GENERAL PROVISIONS
Article 3: Definitions (part 1/10)
For the purposes of this Regulation, the following definitions apply:
(1) 'AI system' means a machine-based system that is designed to operate with varying levels of autonomy …
```
**Subagent**:`.claude/agents/corpus-researcher.md` declares tools: mcp__corpus__search, so Claude Code gives it no other tool. Its instructions: search before answering, once per law or part of the question; answer only from the returned passages; cite every claim as [source, Article N]; otherwise reply “The documents I have do not cover this.”

**Transcript from Claude Code** (v2.1.322):
❯ Use the corpus-researcher subagent: does an employer have to tell workers     
  before using an AI system to monitor them?                                    

⏺ corpus-researcher(Employer AI monitoring notice)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

⏺ The corpus-researcher subagent is now searching the AI Act and the GDPR
  separately for this question. I'll send you its answer, with citations, when
  it finishes.

✻ Brewed for 7s · done 4:31 PM

› Message from corpus-researcher
  ANSWER

  Yes. Under the AI Act, an employer that uses a high-risk AI system at the
  workplace must inform workers' representatives and the affected workers before
  putting the system into service or using it [ai_act, Article 26]. AI systems
  used to monitor and evaluate the performance and behaviour of workers count as
  high-risk [ai_act, Annex III]. Under the GDPR, workers must also receive
  information about the processing of their personal data [gdpr, Article 13]
  [gdpr, Article 14].

  REASONING (brief)

  1. Is workplace monitoring high-risk? Yes. Annex III, point 4(b) lists AI
  systems used "to monitor and evaluate the performance and behaviour of persons
  in such [work-related] relationships" [ai_act, Annex III].

  2. Who must be told, and when? Article 26(7) says that "before putting into
  service or using a high-risk AI system at the workplace," employers must
  inform workers' representatives and the affected workers. This follows Union
  and national rules and practice on informing workers [ai_act, Article 26].

  3. Individual notice when the system supports decisions. Deployers of Annex
  III high-risk systems that make, or help make, decisions about people must
  tell those people that the system is being used [ai_act, Article 26].

  4. Emotion recognition is banned, not just subject to notice. Using AI to
  infer the emotions of a person in the workplace is prohibited, except for
  medical or safety reasons [ai_act, Article 5]. Outside that ban, anyone using
  an emotion recognition or biometric categorisation system must tell the people
  exposed to it that it is operating [ai_act, Article 50].

  5. GDPR. When personal data are collected from workers, the employer must
  provide the required information at the time of collection. This includes the
  purposes, the legal basis and, where it applies, the existence of automated
  decision-making, with meaningful information about the logic involved and the
  likely consequences [gdpr, Article 13]. If the data come from somewhere else,
  the employer must provide similar information, at the latest within one month
  [gdpr, Article 14]. Processing must be transparent [gdpr, Article 5]. Member
  States may set more specific rules for employee data. These rules must include
  safeguards on transparency and on monitoring systems at the workplace [gdpr,
  Article 88].

  LIMITS

  - Article 26(7) covers high-risk systems only. For a monitoring tool that is
  not high-risk, the passages show only the GDPR duties to inform, plus the
  Article 50 duty if emotion recognition or biometric categorisation is
  involved.
  - The corpus does not include national (e.g. Spanish) rules on informing
  workers' representatives, which Article 26(7) and GDPR Article 88 refer to. It
  also has no recitals and no AI Act application dates, so it cannot say from
  what date Article 26 applies.
  - I did not retrieve the text of GDPR Article 22. It is mentioned only through
  the cross-reference in Articles 13(2)(f) and 14(2)(g).

  CITATIONS RETRIEVED

  - [ai_act, Article 26] (paras 7 and 11 are relevant; paras 1-6, 8-10 and 12
  also came up)
  - [ai_act, Annex III] (point 4(b) employment monitoring; point 1(c) emotion
  recognition)
  - [ai_act, Article 5] (para 1(f) workplace emotion recognition ban)
  - [ai_act, Article 50] (para 3 notice for emotion recognition and biometric
  categorisation)
  - [ai_act, Article 3] (definition 39, emotion recognition system)
  - [ai_act, Article 13] (provider transparency to deployers; not central)
  - [gdpr, Article 13]
  - [gdpr, Article 14]
  - [gdpr, Article 5]
  - [gdpr, Article 88]

⏺ Yes. Under the AI Act, an employer must inform workers' representatives and
  the affected workers before it puts a high-risk AI system into service or uses
  it at the workplace [ai_act, Article 26]. AI systems that monitor and
  evaluate the performance and behaviour of workers are classed as high-risk
  [ai_act, Annex III]. The GDPR also requires the employer to give workers
  information about how their personal data are processed [gdpr, Article 13]
  [gdpr, Article 14].

  Why:
  - Monitoring is high-risk. Annex III, point 4(b) covers AI used "to monitor
    and evaluate the performance and behaviour of persons" in work relationships
    [ai_act, Annex III].
  - Notice comes before use. Article 26(7) requires the notice before the system
    is put into service or used, following Union and national rules on
    informing workers [ai_act, Article 26].
  - People affected by decisions must be told. If the system makes or helps make
    decisions about a person, the employer must also tell that person the
    system is being used [ai_act, Article 26].
  - GDPR information duties. When data are collected from the worker, the
    employer must give the information at that moment. It includes the purposes,
    the legal basis and, where it applies, automated decision-making and the
    logic behind it [gdpr, Article 13]. If the data come from elsewhere, the
    information must be given within one month at the latest [gdpr, Article 14].
    Processing must be transparent [gdpr, Article 5]. Member States may set
    more specific rules for employee data, with safeguards on transparency and
    on workplace monitoring systems [gdpr, Article 88].
  - Emotion recognition is banned at work. Using AI to infer a worker's emotions
    is prohibited, except for medical or safety reasons. Telling workers does
    not make it allowed [ai_act, Article 5]. Where emotion recognition or
    biometric categorisation is allowed, the people exposed to it must be told
    it is operating [ai_act, Article 50].

  Limits:
  - Article 26(7) applies only to high-risk systems. For a monitoring tool that
    is not high-risk, the documents show only the GDPR duties, plus Article 50
    if emotion recognition or biometric categorisation is involved.
  - The documents do not include Spanish or other national rules on informing
    workers' representatives, even though Article 26 and GDPR Article 88 refer
    to them. They also have no recitals and no AI Act application dates.
  - The text of GDPR Article 22 was not retrieved. It appears only as a
    cross-reference inside Articles 13 and 14.

  HR should check the cited articles before making any decision. I can give you
  a more detailed explanation of any of these points.

✻ Crunched for 8s · done 4:31 PM

⏺ Agent "Employer AI monitoring notice" finished · 23s

## Adding a document
**If the document is already indexed.** A document is identified by its file name (source). Adding the same file with identical content changes nothing and the tool says so. If the content changed, the old chunks that no longer exist are deleted and only new or changed chunks are embedded, so no quota is wasted.
 
**Before and after.** Unanswerable question: q09, "From what date do the high-risk AI rules apply to the HR tools we use?" (the answer is in AI Act Art. 113, Chapter XIII, outside the corpus). Document added: `extra/ai_act_final_provisions.txt`, AI Act Chapter XIII (Articles 102–113) extracted from the same EUR-Lex PDF (same licence): 16 chunks, 16 embeddings.

| Step | Result |
|---|---|
| 1. Before adding | `The documents I have do not cover this` (correct refusal) |
| 2. Add through the agent | approval prompt → `y` → `Added ai_act_final_provisions, 16 chunks, 16 embedded` |
| 3. Add the same file again |`The document extra/ai_act_final_provisions.txt has been verified and is already indexed in the system.` (no new embeddings)|
| 4. After, original AGENTS.md rule 5 | `The documents I have do not cover this` |
| 5. After, rule 5 made conditional | `The documents I have do not cover this`, although search returned `[ai_act_final_provisions, Article 113]` as result 1 (agent's query: `application date high risk AI systems HR tools date`, source `ai_act`) |
| 6. After removing "application dates" from rule 5 | ✍️ paste the answer |

## Harness and guardrails

`agent.py`: LangChain `create_agent` on gemini-3.5-flash-lite, with the tools from `server.py` over MCP (stdio) and `AGENTS.md` as the system prompt.
 
**AGENTS.md rules.** Research before answering, with one search per law or per part of the question; answer only from the search results; a brief explanation with a longer one on request; every claim cited as [source, Article N] (annexes as [ai_act, Annex III]) using only articles that appeared in the results; the exact sentence "The documents I have do not cover this" when the passages do not answer; and a list of what the corpus does not contain (recitals, national law, general-purpose AI, governance…) so the agent refuses on those topics unless a document added later answers them.

**Approval step.** `add_document` is wrapped in HumanInTheLoopMiddleware: in the terminal the user must type yes; with no terminal (evaluation, check.py) it is rejected. Shown in step 2 of the demo.
 
**Limits.** At most 6 tool calls and 10 model calls per question.
 
**Extra guardrail: citation check.** Every citation in the answer must match a passage that search returned in that run, and an answer that is not a refusal must cite at least one. On a violation the agent gets one chance to rewrite; if it fails again the answer is withheld and replaced by the refusal sentence.
 
**A case where it fired.** In the 30-question evaluation it fired 0 times: every citation was valid.

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

Claude Code (Opus 5.5) helped with code (index, retrieval, server, agent, evaluation), including debugging the ChromaDB concurrency crash and the free-tier rate limits, drafted the subagent file, and compiled the tables and numbers in this report from the files in `eval/`. I reviewed, ran and tested all code locally. The use case, corpus scope, chunking and retrieval choice, refusal rules, judge rubric, test set, my own grades, the analysis and the ship decision are mine. 