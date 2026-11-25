# Assignment 3 Report

- **Name**: Ignacio Fierro Botin
- **Student ID**: 20206
- **Group**: BBADBA A

## Use case

EU based members of a company’s data team ask the virtual assistant various questions before starting a project. Some examples of questions include, can they use this particular set of data? How quickly must they notify the user of a data breach? Can they send the data to a supplier outside the EU? Can the company be legally required to store the data locally? Based on the answers provided by the virtual assistant, the data team decides if they should create a project brief.

If the virtual assistant gives an incorrect response such as “with a 7 day deadline”, the data team will miss the 72 hour deadline imposed by GDPR and the company will be fined up to 10 million euros or 2% of the company’s worldwide annual turnover. Before guessing the virtual assistant should say “I don’t know.”

## Corpus

| Document                                                         | URL                                                                       | Date        | Licence              | Words      |
|------------------------------------------------------------------|---------------------------------------------------------------------------|-------------|----------------------|------------|
| General Data Protection Regulation (EU) 2016/679 (`gdpr`)        | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679 | 27 Apr 2016 | EUR-Lex reuse notice |   53,019   |
| Data Governance Act (EU) 2022/868 (`dga`)                        | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R0868 | 30 May 2022 | EUR-Lex reuse notice |   26,435   |
| Free Flow of Non-Personal Data Regulation (EU) 2018/1807 (`ffd`) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32018R1807 | 14 Nov 2018 | EUR-Lex reuse notice |   26,435   |
| **Total**                                                        |                                                                           |             |                      | **85,572** |

The EUR-Lex legal notice (https://eur-lex.europa.eu/content/legal-notice/legal-notice.html) allows legal documents published there to be reused, under Commission Decision 2011/833/EU. Source: © European Union, https://eur-lex.europa.eu. The documents are laws and contain no personal data; the signature block with the Presidents' names is dropped during ingestion.

index.py tries to download the pages. EUR-Lex blocked the scripted download from my network, so I saved the four HTML pages from the browser into corpus/. When the download fails and the document is already in index/, main.py index keeps the stored chunks.

## Ingestion

- Extract: BeautifulSoup reads the HTML page and takes the innermost paragraphs and table cells in order.
- Clean: whitespace is normalised, and the page menu, the Official Journal banner, the signatures and the footnotes are dropped.
- One extraction problem I fixed: EUR-Lex puts list markers and their text in separate table cells, so Article 6(1) comes out as the separate lines "(a)", "the data subject has given consent...". A line that is only a marker is now glued to the text after it. Footnote marks inside sentences ("...of the Council (4) seeks...") are removed too.
- Chunk: the text is split into units (Preamble, Recital n, Article n, Annex n). The article design makes one chunk per Article (split between paragraphs above 450 words; recitals grouped up to 450 words). The fixed design uses 450-word windows with 50 words of overlap.
- Metadata on every chunk: source, title, location (for example "Article 33"), locations, heading, words.
- Embed and store: gemini-embedding-2 (768 dimensions), each vector saved to index/vectors.jsonl as it arrives so only chunks without a saved vector are embedded; chunks and vectors are stored in ChromaDB in index/chroma.
- Number of chunks: article 306 (gdpr 193, dga 92, ffd 21), fixed 219 (gdpr 136, dga 67, ffd 16). The build found exactly 99, 38 and 9 Articles, the real counts of the three laws.

## Test set

30 questions in eval/questions.csv, drafted from the three laws: 20 single, 5 multi (two passages) and 5 unanswerable. The unanswerable ones are close to the topic (cookies, the AI Act, the Data Act, standard contractual clauses, high-value datasets), so a model that knows EU law is tempted to answer them.

| id  | kind         | question                                                                                                                    | expected         | reference answer                                                                                  |
|-----|--------------|-----------------------------------------------------------------------------------------------------------------------------|------------------|---------------------------------------------------------------------------------------------------|
| q04 | single       | How quickly must we respond when a person exercises one of their data protection rights, and can that deadline be extended? | gdpr, Article 12 | Within one month; extendable by two further months, and the person must be told within one month. |
| q26 | unanswerable | Do we need a visitor's consent before placing analytics cookies on their device?                                            | (none)           | The corpus does not cover this (cookie rules are in the ePrivacy Directive).                      |

## Retrieval

A hit at k means one of the top k chunks comes from the expected document and covers the expected Article (25 answerable questions, dense search).

| design  | hit@1 | hit@3 | hit@5 | words added to the prompt (k=5) |
|---------|-------|-------|-------|---------------------------------|
| article | 0.68  | 0.92  | 1.00  | 1652                            |
| fixed   | 0.64  | 0.92  | 0.96  | 2250                            |

- Design I chose: article. It is equal or better at every k (0.68 against 0.64 at k=1, 0.92 for both at k=3, 1.00 against 0.96 at k=5), it adds fewer words to the prompt (1,652 against 2,250) and each chunk is one Article, so it can be cited exactly. A fixed window covers several Articles, which also makes a hit easier to get, so the real gap is probably larger than these numbers show.

## Tools and subagent

- search(query): searches the corpus and returns the 5 most relevant passages, each starting with its citation tag, for example [gdpr | Article 33]. The description tells the model what the corpus contains, when to use the tool and how to cite.
- add_document(path): runs an EUR-Lex HTML file through the same pipeline as the corpus (imported from index.py) and stores it. The description says it must only be called when the user asks.

One search result (the passages the agent retrieved for q26, tags only): [gdpr | Article 7], [gdpr | Recitals 31-34], [gdpr | Article 8], [gdpr | Article 6], [gdpr | Recitals 40-42]. The first passage begins:

[gdpr | Article 7] General Data Protection Regulation (EU) 2016/679, Article 7 Conditions for consent
1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data.

The subagent .claude/agents/corpus-researcher.md can only use mcp__corpus__search. Its instructions: search once per part of the question, answer in at most 100 words, end every factual sentence with the citation tag, reply "The corpus does not cover this question." when the passages do not answer, never answer from memory.


## Adding a document

If the file's content is already indexed, add_document changes nothing and embeds nothing. If the same source is indexed with different content, the new version replaces the old one. Vectors already saved in index/vectors.jsonl are never requested again.

main.py evaluate adds the Open Data Directive (EU) 2019/1024, asks the question again, and removes the document afterwards.

Question q28: Which thematic categories of high-value datasets must public sector bodies make available free of charge?

add_document, first call: Added 'open_data': 51 chunks stored, 51 newly embedded.
add_document, second call: 'open_data' is already indexed with the same content (51 chunks). Nothing changed.

Before: The corpus does not cover this question.

After: The thematic categories of high-value datasets are [open_data | Annex I]: 1. Geospatial 2. Earth observation and environment 3. Meteorological 4. Statistics 5. Companies and company ownership 6. Mobility. The Commission adopts implementing acts to identify specific datasets within these categories that must be made available free of charge [open_data | Article 14(1)]. This requirement is subject to specific exceptions, including for libraries, museums, archives, and cases where it could cause budget-related hardship or distortions of competition [open_data | Article 14(3), (4), (5)].

## Harness and guardrails

agent.py uses LangChain create_agent with Gemini (gemini-3.1-flash-lite), the two MCP tools of server.py, and AGENTS.md as system prompt. The rules in AGENTS.md, each with its reason: search first; answer only from the results; cite every claim; say when the corpus does not cover the question; copy numbers exactly; do not add documents unprompted; be brief.

- Approval: HumanInTheLoopMiddleware pauses the run before add_document; the harness asks "Approve? [y/N]" and rejects the call if the answer is no or nobody is at the keyboard.
- Call limit: at most 6 model calls per question (ModelCallLimitMiddleware).

I do a citation check on every guardrail. If an answer includes citations, I verify if they are relevant to the passage(s) the search returned. If they are, I include the answer. Otherwise, I include the sentence ‘I’m sorry, but I cannot answer this’ or something similar.  This check ensures users don’t create and use memory citations. It cannot determine the validity of the citation.

A case where the guardrail fired:

Question: Do we need a visitor's consent before placing analytics cookies on their device?
Retrieved: [gdpr | Article 7], [gdpr | Recitals 31-34], [gdpr | Article 8], [gdpr | Article 6], [gdpr | Recitals 40-42]
Answer shown: The corpus does not cover this question. (A draft answer was withheld: its citations could not be verified.)

The model retrieved the GDPR's general consent rules and drafted an answer from them, although nothing in the corpus is about cookies. The check withheld the draft and the user got the refusal.

## Evaluation

The agent answered all 30 questions (eval/answers.json).

- Code checks (eval/results.csv): is it a refusal; are all citations passages that were retrieved; does it cite the expected Article; did the guardrail fire.
- LLM judge (the same model, gemini-3.1-flash-lite) with this rubric: correct = the answer states the key facts of the reference and contradicts none (for an unanswerable question: it refuses and does not answer anyway); supported = every claim is in the retrieved passages.
- Labels: 20 answers are graded in eval/human_labels.csv (5 unanswerable, 5 two-passage, 10 single). I suggested a grade for each and then I reviewed and confirmed them. I had already seen the judge's reasons for the three failed questions when I did this, so the labels are not fully independent of the judge.

| measure                                                      | value |
|--------------------------------------------------------------|-------|
| correct (answerable questions)                               | 22/25 |
| unsupported (answer has a claim that is not in the passages) | 0/25  |
| wrong refusals (answerable questions refused)                | 3/25  |
| correct refusals (unanswerable questions)                    | 5/5   |
| citations valid (code check)                                 | 30/30 |
| guardrail fired                                              | 5/30  |

The system never stated something that was not in the retrieved text and it refused all five unanswerable questions. Every one of its three errors is a refusal of a question it could have answered. Limits: 30 questions, a judge from the same model family as the agent and answers that vary slightly between runs.

## Failures

| id  | kind   | outcome       | cause          | judge's reason                                                                                                                                                                                                                                                                       |
|-----|--------|---------------|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| q18 | single | wrong refusal | wrong refusal  | The answer incorrectly claims the corpus does not cover the question, as the retrieved passages clearly state in Article 4 that data localisation requirements are prohibited unless justified on grounds of public security.                                                        |
| q20 | single | wrong refusal | retrieval miss | The corpus contains the relevant information in the Free Flow of Non-Personal Data Regulation (EU) 2018/1807, Recital 10, which explains that the regulation applies to non-personal data and provides for a coherent set of rules with the GDPR without requiring separate storage. |
| q23 | multi  | wrong refusal | wrong refusal  | The answer incorrectly states that the corpus does not cover the question, even though Articles 46 and 49 of the provided GDPR text clearly outline options for international data transfers in the absence of an adequacy decision.                                                 |

Counts by cause: wrong refusal 2 (q18, q23), retrieval miss 1 (q20), wrong answer from the right passage 0, unsupported claim 0, bad test question 0.

In questions 20 and 23 the agent prepared answers, but citation checks blocked them because citations in the draft answers did not match those in the search results. Thus the main obstacle is the ‘guardrail’. In order to avoid providing answers without support, the agent is too strict and rejects answerable questions. In this case, this is the lesser error.

I would increase tolerance of the citation check. At present, if more than one recital is retrieved, the check requires each recital to be individually cited. Similarly, if more than one article is cited in the same bracket, the check requires each article to be individually cited. I would also add keyword search functionality to locate articles, not just recitals.

## Decision

I’d let the data team use it to find what part of the law most closely addresses their query, and read the relevant sections with the citations. On the test set, it correctly identified the answers to 22 of the 25 answerable questions, refused to provide answers to the 5 unanswerable questions, and didn’t make any uncorroborated assertions. I would definitely not recommend relying on the answer to make any material decision, in particular, when material consequences, such as fines, may be imposed as a result of the decision. Prior to any further roll out, more examples of unanswerable questions should be included in the corpus.

Cost per question: 3,797 tokens on average (maximum 4,301) and 19.2 seconds on average (maximum 85.7, which includes rate-limit waits on the free tier).

## AI use

I used Claude (Anthropic) to help me write the code, draft the test questions, then tell me what structure to follow for this report. I checked the questions against EUR-Lex, graded the 20 answers myself and wrote the retrieval choice, failure analysis and decision in the report from my own results.