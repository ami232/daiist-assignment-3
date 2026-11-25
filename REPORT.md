# Assignment 3 Report

- **Name**: Tomás Roschge
- **Student ID**: 19045
- **Group**: BBADBA 5A 

## Use case

The person who asks is a regular airline passenger in the EU after suffering a flight cancelation, delay, lost baggage, denied boarding, or a lack of assistance for a passenger with reduced mobility. The passenger asks in plain language what they are entitled to in their situation, and they use the answer to decide whether and how to make their claim to the airline: how much money, within what period of time, hotels, new tickets, or whatever applies in that case.

A wrong answer is costly. A wrong amount of compensation stated in the answer can lead the passenger to ask for too much and get rejected, or worse, claim too little and lose money. For example, 400 € instead of 250 € depends only on whether the flight is over 1,500 km. Also, a wrong deadline might make the passenger lose the right to compensation entirely: a damaged suitcase must be reported within 7 days.

"I don't know", by contrast, costs the passenger's time: getting in contact with the airline or the national enforcement body. This is what drives the design: the assistant only answers from the legal texts, and cites every claim for the passenger to be able to check it, and it refuses to answer when it doesn't find the explicit answer in the documents.

The motivation behind this was a recent experience. My flight from Madrid to Buenos Aires got delayed 7 hours the day before, and at the airport there was a guy making a WhatsApp group in order for the passengers to claim 600€. I didn't listen to him, and ended up doing the claim later on my own. I got 300€ as compensation for missing the initial deadline; it would've been 600€ if I would've done it on time. Having an assistant like this would have made it much easier, as the reason on why I didn't make the claim on time was due to the fact that I had to fill up an extensive form to get in contact with the airline.


## Corpus

The corpus is the EU law on air passenger rights: the three regulations a passenger can rely on, plus the European Commission's two most recent interpretative guidelines, which explain how the regulations apply in practice and summarise the Court of Justice's case law. All five are official English texts from EUR-Lex.

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| Regulation (EC) No 261/2004: denied boarding, cancellation, long delay | [CELEX:32004R0261](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261) | 11 Feb 2004 | EUR-Lex, reuse authorised (Decision 2011/833/EU) | 4,494 |
| Commission Interpretative Guidelines on Regulation 261/2004 (C/2024/5687) | [CELEX:52024XC05687](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC05687) | 25 Sep 2024 | same | 22,533 |
| Regulation (EC) No 2027/97: air carrier liability for passengers and baggage, consolidated with Regulation 889/2002 | [CELEX:01997R2027-20020530](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:01997R2027-20020530) | 9 Oct 1997 (consolidated 30 May 2002) | same | 2,494 |
| Regulation (EC) No 1107/2006: disabled persons and persons with reduced mobility | [CELEX:32006R1107](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32006R1107) | 5 Jul 2006 | same | 5,659 |
| Commission Interpretative Guidelines on Regulation 1107/2006 (C/2024/5992) | [CELEX:52024XC05992](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52024XC05992) | 4 Oct 2024 | same | 20,517 |
| **Total** | | | | **55,697** |

The regulations give the rules (amounts, deadlines, conditions), and the guidelines show how those rules are read today, for example what counts as an extraordinary circumstance. Without the guidelines, many realistic questions could not be answered. The texts are public legislation and contain no personal data. EUR-Lex allows reuse provided the source is acknowledged.

One limitation: the consolidated version of 2027/97 is, in EUR-Lex's own words, "a documentation tool", not the legally binding text.

## Ingestion

**Extraction.** `index.py` downloads the official English HTML of each document by its CELEX number. It uses the Publications Office content API, as eur-lex.europa.eu blocks scripted downloads. The HTML is parsed with BeautifulSoup into the document's own legal units, using the CSS classes of the Official Journal format and the numbering in the text:

- each article: "Article 7";
- each recital: "Recital (12)";
- each numbered guideline section: "Section 4.3.2";
- each annex: "Annex I";
- the preamble.

Numbered lists that EUR-Lex lays out as tables are flattened into one line per item.

**Chunking.** I compared two designs, both with a 300-word cap:

| | Design A: structure | Design B: fixed size |
|---|---|---|
| Rule | One chunk per article, guideline section or annex. Recitals are put together up to 300 words, sections under 50 words are merged into the next one, and longer sections are split at paragraph boundaries, each repeating its heading. | The same text cut every 300 words, ignoring structure. |
| reg_261_2004 | 26 | 15 |
| guidelines_261_2004 | 96 | 64 |
| reg_2027_97 | 13 | 8 |
| reg_1107_2006 | 31 | 19 |
| guidelines_1107_2006 | 92 | 60 |
| **Total chunks** | **258** | **166** |

**Metadata.** Every chunk carries:

- `doc_id` (e.g. `reg_261_2004`);
- the document title;
- `location`: the unit it comes from, e.g. "Article 5 (part 1/2)" or "Section 4.4.3 to Section 4.4.4";
- `locations`: every unit the chunk covers;
- the design;
- the word count;
- the EUR-Lex URL.

`location` is what the agent cites as `[source_id, location]`, and `locations` is what the code uses to check citations and to measure hit rate.

**An extraction problem: footnotes (fixed):** The selected guidelines put a lot of content on its footnotes: 188 in the guidelines on 261/2004 and 79 in those on 1107/2006. These include the Court of Justice cases and some numbers. In HTML format, they sit at the end of the document, far from the referenced sentence, so dividing by chunks would have lost them. The parser now does the following:

- removes each footnote from the end of the document;
- leaves a marker where it is cited;
- appends the footnote text to the chunk that cites it.

The older format (261/2004) needed its own rule, because its notes are plain "(1) OJ C…" lines after the signature, cited as "Commission(1)" in the text. This mattered because, for example, in q01 (lost baggage), the only passage that gives the current liability limit (1,288 SDR), is footnote 74 of the guidelines on 1107/2006. Without implementing the fix the agent could not have cited it.

**Embedding.** Chunks are embedded with `gemini-embedding-2` (3,072 dimensions) and stored in ChromaDB with cosine distance, one collection per design. Documents and queries get different task prompts: `title: {source} | text: {chunk}` for documents, `task: search result | query: {q}` for queries. The free tier allows about 1,000 embeddings a day, so vectors are saved batch by batch, and a run embeds only chunks that have no saved vector yet. The committed index is 39 MB.


## Test set

I came up with questions a normal traveller would have regarding the kinds of problems that the model is aimed to target. The final 35 questions are in `eval/questions.csv`. After I came up with them, I asked Claude to check the entirety of the documents and contrast with the questions I had already wrote to analyze if it was worth it adding or changing some to cover important cases. Each answerable question has:
- its expected source and section, written as in the chunk metadata so code can check retrieval and citations;
- a short reference answer.

The set was committed before any tuning. q35 was added later for the add-document demo. 

| single | multi | unanswerable | total |
|---|---|---|---|
| 19 | 9 | 7 | 35 |

The answerable questions cover the entirety of the five documents, whilst the unanswerable ones sit next to the corpus and ask about themes such as trains, ferry, pets, US rules, insurance, printed boarding passes, and other irrelevant topics (for this model).

**Examples**
- *Multi, q05:* "My flight is delayed 5 hours and I will miss my connection. What can I ask the airline for?" It needs two passages: [reg_261_2004, Article 6] for the refund and care, and [guidelines_261_2004, Section 4.4.8] for compensation when you reach the final destination 3+ hours late.
- *Unanswerable, q34:* "What is the maximum weight allowed for checked baggage on European flights?" Search returns baggage passages, but none gives a weight limit, so the agent must refuse.


## Retrieval

I measured both designs on the 28 answerable questions with the same queries. A hit means that one of the top-k chunks covers an expected source and section. For multi questions, `all@5` means the top 5 contain every expected section.

| | Design A: structure | Design B: fixed size |
|---|---|---|
| hit@1 | 0.607 | 0.607 |
| hit@3 | **0.964** | 0.857 |
| hit@5 | **0.964** | 0.893 |
| all@5 (multi) | **0.857** | 0.786 |
| Words added to the prompt (top 5) | ~1,100 | ~1,680 |
| Sections per hit chunk | 1.15 | 2.16 |

At k=5, A misses only q07 (waiting on board before take-off). B also misses q04 and q20. Similarity scores cannot tell answerable questions from unanswerable ones: with A, the best unanswerable question scores 0.721 and the worst answerable one 0.713. So refusals are left to the agent, not to a score threshold.

**Design Choice: A.** Model A retrieves better from k=3 on and adds 1/3 fewer words to the prompt. Each chunk is close to a complete unit from the guidelines, so a citation points to the exact article or section that the passenger needs to check. The agent's `search` returns the top 5 chunks of design A.


## Tools and subagent

`server.py` is an MCP server (stdio) with two tools. Their full descriptions and a complete search result are in `eval/search_example.md`.

| Tool | Description (summary) |
|---|---|
| `search(query)` | Searches the EU air passenger rights corpus (lists the five documents and what each covers) and returns the 5 most relevant design-A passages. Tells the model to write the query in English, search again if the passages do not answer, and cite as source_id + location. If no passage covers the question, the corpus does not answer it. |
| `add_document(path)` | Adds one EUR-Lex HTML file: parses, chunks and embeds it the same way as the corpus, and stores it permanently. Adding the same file again is safe. Returns the new source_id, the chunks added and the sections they cover, or an error. |

**One search result** (query: "flight cancelled less than 7 days before departure compensation"), first passage shortened:

```text
[1] source_id: reg_261_2004 | location: Article 5 (part 1/2) | similarity: 0.780
sections: Article 5
document: Regulation (EC) No 261/2004 on compensation and assistance to air passengers ...
url: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261
Article 5 – Cancellation
1. In case of cancellation of a flight, the passengers concerned shall: ...
(iii) they are informed of the cancellation less than seven days before ... re-routing ...
[2] reg_261_2004 | Article 7 | 0.770    [3] guidelines_261_2004 | Section 4.4.3 to Section 4.4.4 | 0.762 ...
```

Each passage gives the agent what it needs to cite and what the code needs to check the citation: `source_id`, `location` and `sections`.

**Subagent.** `.claude/agents/corpus-researcher.md` defines a Claude Code subagent whose only tool is `mcp__corpus__search`. Its instructions are a short version of AGENTS.md:
- search first, at most 4 times;
- answer only from the passages;
- cite `[source_id, location]` after every claim;
- refuse with the fixed sentence when the passages do not cover the question;
- answer in about 150 words.

**Transcript** (`eval/subagent_transcript.md`). Asked "My flight from Madrid to Lisbon was cancelled 3 days before departure. What compensation can I get?"

The subagent:

- ran 2 searches in parallel, one on the cancellation rules and one on the amounts;
- answered with 250 euros for flights of 1,500 km or less, plus the exceptions (re-routing within the time limits, the 50 % reduction, extraordinary circumstances);
- cited 3 sections, all of them among the passages it retrieved;
- said that its sources do not give the Madrid–Lisbon distance, instead of assuming it. This is good: we don't want the LLM to use knowledge it already has as it can bias the responses.


## Adding a document

**Already indexed.** Each chunk's id is built from its document, its design and a hash of its text. When `add_document` gets a file whose chunks are already in that index, it skips them: therefore nothing is embedded or stored twice. The demo log shows this, because the document had been embedded in an earlier run: "90 chunks: 0 newly embedded, 90 were already in the index". The same check stops a re-run of `index.py` from spending embedding quota on chunks that are already embedded.

**Demo** (`eval/add_document_demo.md`). It ran on a copy of the index (`index/chroma_with_reg_2026_2202`), so the base test set still sees the original corpus.

- **Question (q35):** "Can the airline refuse to let me board, or charge me extra, because I printed my boarding pass at home?"
- **Before:** the agent says "I can't answer this from my sources.", cites nothing and points to the airline or the national enforcement body. This is correct as the corpus says nothing about printed boarding passes.
- **Added:** Regulation (EU) 2026/2202, the reform amending 261/2004 (`corpus/32026R2202.html`, 90 chunks). `add_document` paused for approval first.
- **After:** "No, the airline cannot deny you boarding on the grounds that you used your own printed version of a digitally issued boarding pass… [and] cannot charge you an additional fee…", cited as [reg_2026_2202, Article 1]. The citation check passed.

**Limits.**
- The answer leaves out that the reform applies only from 23 October 2027. If a passenger consulted the agent before that it would have no way of knowing, so the answer is correct for the text but incomplete for the passenger.
- The citation says "Article 1" because the amending act writes the new articles (e.g. 11b) inside its own Article 1. The citation is valid, but it is less precise than it could be.

## Harness and guardrails

`agent.py` runs a LangChain `create_agent` on `gemini-3.5-flash-lite`. It gets the MCP tools over stdio and uses `AGENTS.md` as its system prompt.

**AGENTS.md rules.** Each rule comes with its reason, written for the passenger.

| # | Rule | Why |
|---|---|---|
| 1 | Search before every answer (in English, each part of the question, max 4) | The rules with which the passenger can rely and claim on depend on details found only in the passages |
| 2 | Answer only from the passages | A wrong amount or deadline can lose a claim |
| 3 | Cite `[source_id, location]` after every claim, copied from the results | The passenger and the code must find the exact text to support their claim to the airline |
| 4 | If not covered, start with "I can't answer this from my sources." | A confident wrong answer is worse than no answer |
| 5 | Give the concrete amount, deadline and exception, in ~150 words | Travellers need the number and the condition |
| 6 | Use `add_document` only when the user asks | It changes the index for every future answer |
| 7 | Information, not legal advice: say what the case depends on | Only the passenger knows the complete facts and the airline will act according to them |

**Approval step.**
- `add_document` pauses before it runs (`HumanInTheLoopMiddleware`), and the user must approve or reject it at the terminal.
- With no terminal, as in the evaluation, the call is rejected. The demo approves it explicitly.
- `ToolCallLimitMiddleware` caps `search` at 4 calls per question. In the final run the agent used 1 search on 28 questions, 2 on 4 and 3 on 3.

**Extra guardrail: citation check.**
- After the agent answers, code checks every `[source_id, location]` in the answer against the passages that `search` returned in that run.
- An answer that has an invented citation, or no citation and no refusal, is sent back once with the problem.
- If the second answer still fails, it is replaced by a refusal.

**Case where it fired** (`eval/guardrail_case.md`). Asked "What kinds of questions can you help me with?", the agent made one search about scope. It then listed its topics citing Article 1 of each regulation and Article 10 of 261/2004, none of which that search had returned, meaning that these were stated based on the agent's own knowledge instead of the passages retrieved. The check rejected it as the draft was wrong. The corrected answer cites only retrieved sections, but it is narrower: it no longer mentions baggage or reduced-mobility passengers. The single search had returned only passages about 261/2004, so the agent could not cite the other regulations, even though the corpus does cover them.

**Limit.** In the final evaluation the guardrail passed all 35 answers without firing. It checks that a cited passage was retrieved, not that the passage says what the claim says. For example, q01, q03, q04 and q07 passed with claims that I found unsupported and that contained invented or wrong information.

## Evaluation

`evaluate.py` runs the agent on all 35 questions, then checks each answer with code and with an LLM judge, and compares the judge with grades I personally gave each answer.

**Code checks** (no LLM)

| Check | Result |
|---|---|
| Unanswerable questions refused | 7/7 (0 answered anyway) |
| Wrong refusals on answerable questions | 1/28 (q11) |
| Expected passage among retrieved ones | 28/28 |
| Answer cites the expected source and section | 23/28 |
| All citations valid (retrieved in that run) | 35/35 |

**Judge rubric.** The judge is `gemini-3.5-flash`, a larger model than the agent. What it does:
1. Sees the question, the reference answer, the passages retrieved by the agent, and the final answer.
2. Returns two 0/1 scores:
- **Correct**: measures whether the answer has the key facts stated in the reference answer. For unanswerable questions, it is expected to decline.
- **Supported**: Every factual claim the agent makes appears exactly in the passages that were retrieved. 

After comparing the first runs with my labels, I adjusted the rubric so that a refusal with an added explanation, or pointing to the airline or the enforcement body would still count as declining. Before that, the judge failed all 7 correct refusals made by the agent just by the fact it told the passenger to contact said entities.

The free tier allows 20 flash calls a day, so the 20 answers I graded were judged first. 19 of them got flash. q34 and 11 of the remaining 15 answers fell back to `gemini-3.5-flash-lite`.

**Agreement with my 20 labels** (q01–q13, q29–q35)

| Run | correct: agreement / kappa | supported: agreement / kappa |
|---|---|---|
| 1: flash-lite, original rubric | 0.60 / 0.05 | 0.60 / −0.23 |
| 2: same, re-run | 0.55 / 0.02 | 0.45 / −0.38 |
| Final: flash, adjusted rubric | 0.65 / 0.24 | 0.75 / −0.09 |

- **correct:** the judge was way stricter than me. It marked q01, q04, q05, q06, q08 and q13 wrong for missing one fact of the reference answer, where I accepted them: the core idea of the response was correct. Its q34 verdict is a flash-lite error: the answer does start with the refusal.
- **supported:** the judge missed all 4 unsupported claims I found (q01, q03, q04, q07) and flagged q08, which I accepted. The ones I flagged were because the agent had claimed or assumed stuff that were not explicitly stated in the guidelines.
- Runs 1 and 2 used the same model and rubric, yet the verdicts changed on 4 of 35 answers.
- Overall, the judge was stricter when it didn't matter and not sufficiently strict when it did. Therefore, I wouldn't trust the judge to analyze the overall performance of the agent as it didn't present the situation criteria a normal human (me) would.

**Results**

| | Judge (35) | Me (20) |
|---|---|---|
| Correct, answerable | 16/28 | 11/13 |
| Unsupported, answerable | 1/28 (q08) | 4/13 (q01, q03, q04, q07) |
| Correct refusals | 6/7 (code: 7/7) | 7/7 |
| Wrong refusals | 1 (q11) | 1 (q11) |

**Cost per question:**
- 12.9 s on average (median 8.1 s);
- about 6,800 agent tokens (median 5,100) plus about 3,900 judge tokens;
- 1.29 searches.

## Failures

A question counts as failed if I or the judge marked it wrong or unsupported. Where we disagree, I use my own decision. Each failure has one main cause.

| Cause | Count | Questions |
|---|---|---|
| Unsupported claim | 4 | q01, q03, q04, q07 |
| Incomplete answer from the right passage | 4 | q14, q19, q23, q28 |
| Wrong refusal | 1 | q11 |
| Bad test question (outdated reference answer) | 1 | q06 |
| Retrieval miss | 0 | – |
| Judge error (not an agent failure) | 1 | q34 |

- **Unsupported claims:** Each answer refers to a real retrieved passage from the guidelines, but adds something that the passage does not say. For example, for q03 the agent invented a 14-day window; for q07 it assumes that the waiting time that triggers assistance keeps growing for longer distances, which is not stated in the guidelines. ("longer thresholds for longer flights"). The citation guardrail didn't catch this, because it only focuses on the fact that the cited passage was retrieved, not on the accuracy of the claim itself.

- **Incomplete answers:** (judged only by the judge). The passage was retrieved and cited, but a key fact was left out: q14 the public-authority strike exception, q23 the written reasons within 5 working days, q28 the 2-year court deadline. A reason it occurred to me on why this might happen is that for claims that require longer explanations and deal with a variety of factors, the ~150-word limit in rule 5 probably pushes the model to drop some of these conditions.

- **Wrong refusal:** On q11 (doors closed early at the gate) the passages on denied boarding were correctly retrieved, but the agent refused to answer stating it didn't have information on the subject.

- **Bad reference answer from my part:** The reference answer for q06 says that the compensation should be 1,000 SDR. The agent said it was 1,288 SDR, which is correct after the updated limits from the 2024 guidelines. The reference was the one outdated, not the answer.

- **No retrieval misses** in the agent run: the expected passage was retrieved 28/28. q07 missed in the plain retrieval test, but the agent's own query found it.

## Decision

**I wouldn't recommend it as a completely reliable tool that the passenger can solely trust to make a claim to the airline, but I would use it to speed up the process of understanding the basics of its situation and recommend having the guidelines at hand to check what the passages actually say**

The thing is that the prominent error is that the agent sometimes takes the answer beyond the basics, and that is where it gets it wrong. Because it wants to improve it, it tends to hallucinate. However, it always retrieves the correct passages and states the most important facts as they are; the basics are there, the recommendation or further explanation not so much. 

What I mean is that it will never tell a passenger "You have no right to compensation" when they actually do, which is the critical point, but it can say "if your trip was longer, they can pay you more". This second situation, in reality, would not hurt the passenger: knowing it can make a claim about a compensation, it will get in contact with the airline; if it claims for more money, the worst thing that can happen is that the airline tells them that it is less than what they are asking for. Therefore, the effect is not "I could have claimed money but I didn't because of what the agent told me", but "I thought I would get more, but I still got what I had the right to get". The core of the issue is solved.

At this point, I would recommend users to use it for finding the exact passages on the guidelines that apply to the text, and trust in that more than in the response itself. 

***What I would choose to fix first:  unsupported claims***. They are, without a doubt, the most dangerous failure for a passenger within the ones found. Neither the guardrail nor the judge detects them (judge missed all 4 of them). I would put a claim-level guardrail that tests each sentence against the cited passage, using a second model or matching by exact quote. After that, the second prioritised fix would be to relax the word limit so that the agent is not forced to skip some conditions on long answers.

**Other safeguards:**
- Every answer shows the cited passage and its EUR-Lex link next to the answer, plus a line saying to check the amount or deadline there before claiming.
- The application date of each document goes into its metadata, so that rules that are not in force yet (as in the add-document demo) are flagged.

**Cost and latency per question:**
- 12.9 s on average (median 8.1 s);
- about 6,800 agent tokens and 1.3 searches.

That is acceptable for someone preparing a claim, typically is not in a hurry. The judge adds about 3,900 tokens, but only during evaluation, not for users. With the free tier, the daily limits (about 1,000 embeddings, and 20 judge calls on flash) matter more than the price.

## AI use

**Claude Code (Claude Opus) was used throughout, as a coding and writing assistant.**

- **Code:** it wrote `index.py`, `server.py`, `agent.py`, `evaluate.py` and the subagent definition, and it ran the indexing and evaluation commands. It also debugged problems on the way: EUR-Lex blocking scripted downloads, the footnote formats, and the free-tier quotas.
- **Test set:** it drafted how the final questions would look like in terms of specificity after I wrote them, and suggested some more to cover every topic in the guidelines.
- **AGENTS.md:** it wrote the wording of the rules, from the behaviour I asked for.
- **Evidence files:** it extracted the subagent transcript, the search example and the guardrail case from the logs.

**My own work:**
- the use case and the choice of corpus;
- the two chunking designs and the choice of design A;
- the themes and first draft of the questions
- answering only from sources, the citation guardrail and the 4-search limit;
- the judge model, and the rubric change after comparing it with my labels;
- the 20 human grades, which I gave before reading the judge's verdicts;
- the failure classification and what to fix first;
- the ship decision.

**Gemini is part of the system, not a writing aid.** `gemini-embedding-2` creates the embeddings, `gemini-3.5-flash-lite` runs the agent, and `gemini-3.5-flash` (falling back to flash-lite) is the judge.
