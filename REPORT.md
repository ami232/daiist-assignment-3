# Assignment 3 Report

- **Name**: Pilar Guerrero
- **Student ID**: 20373
- **Group**: BBADBA 5A

## Use case

This RAG tool is built as an assistant for the founder or compliance lead of an EU startup that builds AI or online-platform products. In a small team like a startup there is usually no legal team, so this person is the one who has to answer questions like "can we launch this feature?" or "do we need an impact assessment for this?" before a lawyer is involved. They use the answer to decide whether a feature can launch as designed, which documents or assessments they need to prepare, and whether the question is serious enough to call a lawyer.

The two possible mistakes have assymetric costs. If the assistant answers wrongly, the founder might launch something that is not compliant, or believe they are covered when they aren't. According to the corpus itself, fines go up to 7% of global turnover under the AI Act for prohibited practices and 3% for other obligations such as the high-risk rules (Art. 99), 4% under the GDPR (Art. 83) and 6% under the DSA (Art. 52 and 74), and on top of that there are blocked launches and reputational damage. A wrong "no" also has a cost, because the startup might drop or delay a feature that was actually allowed, which in a competitive field like AI can mean falling behind. If instead the assistant says the corpus doesn't cover the question and recommends asking counsel, the cost is only some time and a lawyer's fee, which is small compared with a fine calculated on turnover. Therefore the assistant should prefer refusing over guessing, and every claim has to cite the passage it comes from so the founder can check it.

## Corpus

| Document | URL | Date (OJ publication) | Licence | Words |
|---|---|---|---|---|
| AI Act, Regulation (EU) 2024/1689 | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | 12 July 2024 | © European Union; reuse authorised with attribution (Commission Decision 2011/833/EU) | ~90,500 |
| GDPR, Regulation (EU) 2016/679 | https://eur-lex.europa.eu/eli/reg/2016/679/oj | 4 May 2016 | Same | ~55,000 |
| Digital Services Act, Regulation (EU) 2022/2065 | https://eur-lex.europa.eu/eli/reg/2022/2065/oj | 27 October 2022 | Same | ~64,100 |
| **Total** | | | | **~209,600** |

These are the English Official Journal versions, which I downloaded as XHTML from the EU Publications Office (CELLAR) and committed in `corpus/`.

## Ingestion

In the corpus  every recital, article and annex has its own anchor (`rct_32`, `art_7`, `anx_III`), so `index.py` uses those to separate the three documents into one unit per recital, article and annex. This way we split the recital in a way that is logical. The result is 509 recitals, 305 articles and 13 annexes (the annexes are only in the AI Act), so 827 units. I left out the preamble citations, signatures and footnotes, since they don't answer any question.

The extraction problem I had to fix was that list points like "(a)" or "1." sit in their own table cell, so plain text extraction gave "(a)" on one line and its text on the next, which separated the point from what it says. A function called `clean_lines()` merges them back together, so the text reads "(a) the relevant design choices;". I also removed the footnote markers like "(1)" that appear in the middle of sentences, so they don't pollute the embeddings or get confused with point numbers.

I chunked by this structure, so there is one chunk per recital, article or annex, and any unit longer than 600 words is split at paragraph boundaries. Each chunk starts with a citation header, for example `GDPR, Article 7 — Conditions for consent`, and says which part it is if the unit was split, so the embedding knows what the text is and the agent can cite it directly. Every chunk also carries its metadata: `source` (AI Act, GDPR or DSA), `location` (Article 7, Recital 32, Annex III), `type` (article, recital or annex), `title` (the article heading), `part` and `parts`, and the `file` it came from.

I considered removing the recitals, because they add a lot of chunks, but decided to keep them. Even though they are not binding, they often hold the practical answer, for example GDPR Recital 32 is the one that says pre-ticked boxes are not consent, and as later proof three of my test questions are answered by a recital. The result is 900 chunks with an average of 229 words, embedded with `gemini-embedding-2` at 768 dimensions and stored in ChromaDB, which keeps `index/` at 17 MB. The 600-word limit is also what made the whole index fit in the free tier's 1,000 embeddings a day.

## Test set

I wrote 35 questions from the documents before tuning anything: 23 single (9 GDPR, 8 AI Act, 6 DSA), 6 multi, which all combine two laws because that is the realistic situation for a startup whose product touches more than one regulation, and 6 unanswerable. To fit the use case I phrased them the way a founder would ask them ("our signup form", "our CV-screening tool") rather than with legal citations, and I wrote the expected source and location in the same format as the chunk metadata so the hit rate can be checked automatically. I used Claude to help me navigate the articles and check that the locations were correct. The unanswerable questions are deliberately close to the topic, so the corpus contains passages that look relevant but don't actually answer them.

An example of a single question is s01, "Can I use pre-ticked boxes on our signup form to get consent for marketing?", which is answered by GDPR Recital 32: silence, pre-ticked boxes or inactivity do not count as consent. An example of an unanswerable one is u06, "Do we need user consent before setting analytics cookies on our website?" The GDPR defines what valid consent is, so the corpus looks like it answers this, but the obligation to ask comes from ePrivacy Article 5(3), which isn't in the corpus, and this became later the add-document demo.

## Retrieval

I compared two designs over the same vectors, so the second design cost no extra embeddings. The first is plain vector search with cosine similarity, and the second is a hybrid that takes the top 30 from vector search and the top 30 from BM25 keyword search and merges them with reciprocal rank fusion. Hit rate is the share of the 29 answerable questions where a chunk with the expected source and location is in the top k.

| Design | hit@1 | hit@3 | hit@5 | words added @5 |
|---|---|---|---|---|
| vector | 62.1% | 96.6% | 96.6% | 1,376 |
| hybrid | 37.9% | 55.2% | 75.9% | 1,491 |

These numbers are on the original 900-chunk corpus. After the add-document demo the index has 922 chunks, and re-running `main.py evaluate` (as in the committed `eval/summary.json`) gives the same vector hit rates with 1,399 words added, and hybrid 79.3% at k = 5.

The result was very clear and I chose vector as the best since it wins at every k and also adds fewer words to the prompt. I expected hybrid to help, because legal text has exact terms that keyword search should catch, and maybe for a user who already knows the regulations and uses their terms it would. For my questions it didn't, and the reason is the use case itself afterall as i defined in my test set founders ask in everyday words while the law uses legal terms, so BM25 ended up matching common words instead of rleevants and pushing the right passages down. 

## Tools and subagent

The `search(query, k=5)` tool has this description:

```
Search EU digital-regulation law: the AI Act (Regulation 2024/1689), the GDPR
(Regulation 2016/679) and the Digital Services Act (Regulation 2022/2065), plus any
documents added later with add_document. Sources currently in the index: <listed at startup>.

Use it for any question about what these laws require, allow or prohibit, e.g.
consent, data subject rights, high-risk or prohibited AI, transparency, platform
duties, fines and deadlines. Ask in plain words, without naming a law unless the user
did; search again with different wording or a narrower question if the passages do
not answer it.

Returns the k (default 5, max 10) most relevant passages. Each starts with
"Cite as: <law>, <Article N | Recital N | Annex N>" and its type: articles and
annexes are binding law, recitals only explain how to read them. The texts are
the versions published in 2016-2024; later amendments, guidance and enforcement
decisions are not included unless added.
```

The `add_document(path)` tool has this description, and it uses the same files as the index so an added document goes through exactly the same pipeline as the corpus:

```
Add a document to the searchable corpus: a EUR-Lex regulation (.html/.xhtml, split
into recitals, articles and annexes), a PDF (split by page) or a .txt/.md file.

`path` is a file on this machine, absolute or relative to the project folder.
The file is chunked with the same pipeline as the corpus, embedded and stored.
If the same file with the same content is already indexed, nothing is added.
If a file with the same name is indexed with different content, its old
chunks are replaced by the new version.

Returns what happened: chunks added or replaced, and the citation name to use.
```

This is one search result, from `check.py`:

```
[1] Cite as: GDPR, Recital 32 | type: recital
Consent should be given by a clear affirmative act establishing a freely given, specific,
informed and unambiguous indication of the data subject's agreement…
```

The subagent, `.claude/agents/corpus-researcher.md`, only has the `mcp__corpus__search` tool, so it cannot answer from anything other than the corpus. Its instructions are to search first and search again with different wording if the first results don't answer the question, to answer only from the returned passages, to cite every claim as `(GDPR, Article 7)`, to say when a point comes only from a recital, to use the exact refusal phrase when the corpus doesn't cover something, and to stay under about 200 words. This is one transcript from Claude Code:

```
User: We're building a customer-support chatbot for our startup. Do we have to tell users they're talking to an AI?

[Transcript excerpt, subagent on Haiku: passage text omitted, only the "Cite as" lines of each result shown.]

corpus-researcher → mcp__corpus__search: {"query": "must users be told they are interacting with an AI system chatbot"}
Tool result: [1] AI Act, Recital 132 | [2] AI Act, Article 50 | [3] AI Act, Recital 134 | [4] AI Act, Recital 137 | [5] AI Act, Recital 119

corpus-researcher → mcp__corpus__search: {"query": "transparency obligations for AI systems intended to interact directly with natural persons"}
Tool result: [1] AI Act, Article 50 | [2] AI Act, Recital 132 | [3] AI Act, Recital 137 | [4] AI Act, Recital 134 | [5] AI Act, Recital 133

corpus-researcher → answer:
Yes, in general you must tell users they are talking to an AI, unless it is obvious to a reasonably well-informed, observant and circumspect person in the circumstances and context of use. Providers must design and develop AI systems intended to interact directly with natural persons so that those persons are informed of this (AI Act, Article 50(1)). Recital 132 says that where the system's nature is not obvious, users should be notified, and that vulnerable groups (for example by age or disability) should be considered when doing so (AI Act, Recital 132).

The disclosure must be clear and distinguishable and given at the latest at the time of the first interaction, in an accessible format (AI Act, Article 50(5)). The corpus does not say how to word the notice or where in the interface it must appear beyond that.

The corpus does not say whether your startup is a "provider" or a "deployer" under the Act, or whether the chatbot is otherwise regulated. The Article 50(1) duty sits on providers, so if you build the bot yourselves you should assume it applies. Compliance with Article 50 does not make the use lawful under other EU or national law (AI Act, Recital 137).

Practical reading: a chatbot that answers support questions should show an "AI assistant" label at the start of the chat unless it is plainly obvious from context. The corpus does not define "obvious" further, so treat that exception narrowly.
```


## Adding a document

To avoid duplicated added documents if the same file with identical content is added again, nothing is embedded and the tool answers that it is already indexed. If a file with the same name but different content is added, the old chunks are replaced by the new ones, because the most likely reason is an updated version of the same document and keeping both would give contradictory answers. 
 This is what happened when I added the same file a second time:

```
[add_document] Already indexed: ePrivacy_Directive.html (22 chunks, cited as 'ePrivacy Directive'). Nothing added.
```

The unanswerable question I chose was u06, "Do we need user consent before setting analytics cookies on our website?", and the document I added was the ePrivacy Directive 2002/58/EC, which became 22 chunks. 

Before adding it, the agent could not state the rule as it was not included. In the evaluation it answered "generally yes" from GDPR Recital 30, which reaches a plausible conclusion through the wrong reasoning, and in the demo it said the corpus "does not cover this fully" and then answered from the GDPR consent rules (Recitals 32 and 40 and Article 7). After adding it, the answer was:

```
Yes, user consent is generally required before setting analytics cookies.

Under the ePrivacy Directive, storing information or gaining access to information already stored in a
user's terminal equipment (such as a device or browser) is only allowed on condition that the user has
given their consent, after being provided with clear and comprehensive information (ePrivacy Directive,
Article 5(3)).

The only exceptions [...] are if the storage or access is:
* For the sole purpose of carrying out the transmission of a communication [...], or
* Strictly necessary in order for the provider of an information society service explicitly requested
  by the subscriber or user to provide that service (ePrivacy Directive, Article 5(3)).
[...]
Sources: ePrivacy Directive, Article 5
```


## Harness and guardrails

The harness is a LangChain `create_agent` on `gemini-3.5-flash-lite`, with the MCP tools loaded from `server.py` and `AGENTS.md` as the system prompt. `AGENTS.md` has seven rules, each with its reason. The agent has to search before answering, because the model's own memory of EU law may be outdated or wrong, and answer only from the search results, so every answer can be traced back to the text. It has to cite every claim as (Law, Article N), so the founder can open the official text and check it, and use an exact refusal phrase when the corpus doesn't cover something, so that a refusal can be detected by code instead of being hidden in a vague answer. It has to say when a point comes only from a recital, because recitals explain but don't bind, point to a lawyer for decisions with real consequences, because the cost of a wrong answer here is a fine on turnover, and state that the texts are as adopted, without later amendments.

For the approval step in adding a document it only runs if a human types `y`, while with no terminal to ask the answer is no. I put the approval on `add_document` and not on `search` because adding a document changes what every future answer is based on and spends quota, while a search changes nothing. There ix also limits of 6 tool calls and 8 model calls per question, so a confused agent can't loop and burn the quota.

```
The agent wants to run add_document with {'path': 'corpus/ePrivacy_Directive.html'}. Allow? [y/N] y
  embedded 22/22
```

My extra guardrail is a citation check. After the model answers, code checks that every "(Law, Article N)" in the answer was actually returned by search in that run, and that an answer that isn't a refusal cites at least one passage, and if either check fails the answer is withheld and replaced by the refusal. I chose it because in my use case the citation is what the founder trusts, and a citation that wasn't retrieved is a claim from the model's memory dressed up to look checked. It fired on u04, the question about the EU-US Data Privacy Framework: the draft was a correct refusal but cited GDPR Article 46, which search had not returned, so the check withheld it and showed the clean refusal instead.

## Evaluation

I graded every answer in two ways. The first is simple checks done by code, with no AI involved. The code checks whether the answer is a refusal by looking for the exact refusal sentence, whether every article the answer cites was actually returned by the search, whether the expected passage was found and cited, and whether the guardrail stepped in.

The second is a judge, which is another AI model. It reads the question, my reference answer, the assistant’s answer and the passages the search returned, and gives two scores. Correct is 1 if the answer reaches the same conclusion as my reference answer and includes all its key points. It is 0 if it leaves out a point or refuses a question the corpus can answer, and 1 if it refuses a question the corpus can’t answer. Supported is 1 if everything the answer says about the law is written in the passages it found. A plain refusal counts as supported, because it doesn’t claim anything.

I used a different model as the judge than the one that answers the questions, so it isn’t grading its own work. It was gemini-3-flash-preview.
| Result (35 questions) | |
|---|---|
| Correct (judge) | 82.9% (29/35) |
| Unsupported (judge) | 5 answers (16.7% of non-refusals); 7 by my grades |
| Correct refusals | 5/6 (u06 was answered) |
| Wrong refusals | 0/29 |

I graded all 35 answers myself to based on my understanding before comparing with the judge:

| | Agreement | Kappa |
|---|---|---|
| correct | 82.9% | 0.30 |
| supported | 71.4% | 0.00 |

The agreement percentages look fine, but this is actually a bit decieveing because almost every answer gets a 1, so we both  agree most of the time by chance, and kappa removes that. My reading is that the judge is reliable for refusals, where we agreed on all six, partly reliable for correctness, and not reliable for support probably because its not a very deep reasoning model. Of the 7 answers I found unsupported it caught only one (u06), and it accepted every multi-question answer, where I found 4 unsupported, so this is the part of the evaluation I would trust least without a human but it also depends on how good at reasoining the modelis. A better model might have had better matches.

## Failures

I classified the failures using the human grades

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 2 | s08, m04 |
| Wrong answer from the right passage | 3 | s16, m01, m03 |
| Unsupported claim | 2 | m06, u06 |
| Wrong refusal | 0 | – |
| Bad test question | 0 | – |

In terms of retrieval misses, there were two. In s08 the search found Recital 44 but not Article 5, and the answer presented fatigue monitoring as a safety exception. In m04 GDPR Article 9 was never retrieved, so the claim about religion and health data had nothing behind it so not supported.

Three answers were wrong even though the agent had the right passage. s16 missed the Article 25(2) exception for practices already covered by the GDPR or consumer law. m01 applied logging requirements that only apply to biometric identification to a CV-screening tool. m03 had Article 27 but didn't conclude that credit scoring needs a fundamental-rights impact assessment.

The last two added claims that weren't in the passages. m06 said the two laws are enforced by separate regulators, and applied the SME rule even though the question never said the company was an SME. u06 should have refused, but answered from GDPR Recital 30 instead. As a note, `eval/failures.csv` lists the judge's 9 failures with more detailed labels.

The main pattern is that retrieval is rarely the problem. Most failures happen when the agent writes the answer, either missing a condition in a passage it already had or adding something from memory. They are also concentrated in multi questions, which are 4 of my 7 failures.

The first thing I would fix is to run one search per law for multi questions, since m04 failed precisely because the second law's passage never came back. After that I would add a rule to `AGENTS.md` asking the agent to list every condition and exception in the article it cites, which would address s16 and m03.

## Decision

I would let founders rely on it as a first-pass research tool, not as the final answer. I would trust it to tell them which articles apply to their feature and what those articles say, and to tell them when the corpus doesn't cover their question, but not to make a launch decision on its own. So it can be useful to naviaget the law but not a single source of truth. This is mainly because retrieval is strong (96.6% hit@3), it never refused an answerable question and it refused 5 of the 6 unanswerable ones. However, 7 of 35 answers had claims I could not support from the passages, mostly in questions that combine two laws, and the judge can't detect them reliably. Given that a wrong answer can cost a percentage of global turnover, a 20% rate of unsupported claims is too high to act on directly.

The safeguard however is the citation. Every claim cites an article that the citation check confirms was retrieved, so the founder reads the cited articles before acting so it is useful in terms of directingthe founder to teh correct place but maybe the reaosning especially at high stakes shoudl still be left to the founder..

On cost, each question took on average 5,667 tokens and 4.3 seconds on gemini-3.5-flash-lite, with 1.2 searches each adding about 1,376 words of passages to the prompt, plus one embedding per new question. Everything ran on the free tier, but its limits of 1,000 embeddings a day and, for some models, only 20 requests a day mean a real deployment would need a paid tier, and with it a stronger model might reduce the generation failures.

## AI use

I worked in VS Code with Claude Code and walked through the assignment with its assistance. We discussed the key decisions in conversation, such as the 600-word chunk limit given the embedding quota, keeping the recitals, the duplicate rule, the citation-check guardrail and the judge rubric, and I made them. For the code, Claude Code wrote the functions following the approach we agreed on, and I reviewed it. I wrote the test questions with Claude's help to navigate the articles, and then checked every expected location and reference answer against the corpus. I graded all 35 answers myself for the comparison with the judge. For the report, I asked it to draft a write-up from my notes and our conversations, revised it with my own thoughts and decisions, and asked it to check the grammar and structure.
