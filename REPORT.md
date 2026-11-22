# Assignment 3 Report
 
* Name: Manuela Calle
* Student ID: 18754
* Group: BBADBA 5A
 
## Use case
 
The users are hotel managers and compliance officers who need to decide whether a guest-facing AI tool is allowed under EU law. Examples are a booking chatbot, personalised offers, emotion analysis of reviews and CV screening. They use the answer to decide what AI to build, buy or disclose to guests. The question can start with the manager, but the decision has to hold up later in front of an auditor, a regulator, a shareholder or an unhappy guest, and it may reach the CEO or the chief data officer.
 
A wrong answer is expensive. Deploying a prohibited practice can mean fines of up to 35 million euros or 7% of worldwide turnover, and skipping a duty such as chatbot disclosure up to 15 million euros or 3% (AI Act, Article 99). When the system is unsure and says "I don't know", the cost is only time and a call to a lawyer to clear doubts. Because of this gap, the system is built to answer only from the text, cite where, and refuse when it's unsure of the answer. 
## Corpus
 
| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| AI Act (Regulation (EU) 2024/1689) | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689 | 2024-06-13 | Reuse under Commission Decision 2011/833/EU (CC BY 4.0) | 52,242 |
| GDPR (Regulation (EU) 2016/679) | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679 | 2016-04-27 | Reuse under Commission Decision 2011/833/EU (CC BY 4.0) | 29,682 |
| Commission Guidelines on the definition of an AI system (C(2025) 5053) | https://ec.europa.eu/newsroom/dae/redirection/document/112455 | 2025-07-29 | Reuse under Commission Decision 2011/833/EU (CC BY 4.0) | 5,455 |
| **Total** | | | | **87,379** |
 
All three are public EU documents with no personal data. I left out the recitals (the long "whereas" introductions). They are not legally binding, and the free embedding limit of about 1,000 texts a day could not cover two chunking designs over the full text. The cost is that anything explained only in a recital cannot be answered.
 
## Ingestion
 
I extract the text from each PDF page by page and keep the page number as a label. Then I clean it by removing Official Journal headers and footers, printed page numbers, tables of contents, footnotes, soft hyphens and the recitals. The page number stays in the metadata even though it is removed from the text.
 
One extraction problem was that page headers landed in the middle of articles and broke the "Article N" lines that the structure detection depends on. To solve this, I wrote a list of patterns in `index.py` matching the repeated header and footer lines seen in the corpus (for example "OJ L, 12.7.2024 EN" and the "ELI: http://..." links). During cleaning, every line that matches one of these patterns is deleted before the text is split into articles. 

There are two chunking designs. Design A cuts fixed windows of 350 words with 50 words of overlap. Design B cuts by structure, one chunk per article or section, and only splits at paragraph breaks if the unit is longer than 450 words. Each chunk carries this metadata: source document, article, annex or section, page, chapter and word count, and that metadata becomes the citation. Design A has 291 chunks (AI Act 174, GDPR 99, guidelines 18) and Design B has 345 chunks (AI Act 196, GDPR 131, guidelines 18). In total 636 chunks were embedded with Gemini. The assistant uses only Design B. It was chosen by the retrieval numbers below (hit@5 of 0.96 against 0.86), because with legal texts, where citations and exact language matter, a passage should not be cut off, and the RAG should find the full article following the text's natural structure. 
 
## Test set
 
I wrote 35 questions from the documents before tuning anything. Each has an expected source and location and a short reference answer. There are 22 where one passage answers it, 6 where two passages are needed, sometimes from two documents, and 7 unanswerable close to the topic but not in the corpus, for example Spain's data authority or the Spanish age of consent.
 
Examples:
* q01 (single): "Do we have to tell guests that they are talking to an AI chatbot?" Expected source is AI Act Article 50.
* q23 (multi): "Our booking chatbot collects guests' personal data. What do the AI Act and the GDPR each require us to tell guests?" Expected sources are AI Act Article 50 and GDPR Article 13.
## Retrieval
 
Hit@k is the share of the 28 answerable questions where the right passage is in the top k results. For multi questions every needed passage must appear.
 
| Design | hit@1 | hit@3 | hit@5 | words in prompt at k=5 |
|---|---|---|---|---|
| A fixed, vector | 0.679 | 0.821 | 0.857 | 1,748 |
| A fixed, hybrid | 0.571 | 0.750 | 0.857 | 1,750 |
| B structure, vector | 0.714 | 0.857 | 0.964 | 1,723 |
| B structure, hybrid | 0.607 | 0.929 | 0.964 | 1,754 |
 
I chose by highest hit@5, then hit@3, then hit@1, because the agent reads five passages. The winner is **structure-based chunks with hybrid search**. Structure beat fixed-size by 11 points at k=5. Hybrid is worse at hit@1 (0.607 against 0.714) but better at hit@3. With only 28 answerable questions one question is worth 3.6 points, so the differences between vector and hybrid are small and I should not oversell them. The five passages add about 1,750 words to the prompt for every design.
 
## Tools and subagent
 
`server.py` is an MCP server with two tools.
 
**search** (description the model reads): "Search the EU AI Act, the GDPR and the Commission guidelines on the AI system definition (plus any document added later) and return the 5 most relevant passages. Use it for any question about what these EU texts say... Returns numbered passages. Each has its citation in square brackets (source, article / annex / section, page), a relevance score and the text. Cite with exactly that bracket. These texts are EU law only: national laws and guidance from other bodies are not in the index, so an empty or off-topic result means the corpus does not cover the question."
 
**add_document** (description): "Add one document to the searchable index: reads the file at `path`, splits it into chunks, embeds them and stores them, so that later searches can cite it... If the very same file is already indexed, nothing is changed and the tool says so. If a file with the same name but different content is indexed, its old chunks are replaced by the new ones... This changes the shared index: use it only when the user asked to add a document."
 
One search result (query "transparency obligation AI system interaction natural persons chatbot", first of five):
 
```
[1] cite as [ai_act, Article 50(1)-(3)] | AI Act (Regulation (EU) 2024/1689) | Article 50(1)-(3) - Transparency obligations for providers and deployers of certain AI systems | PDF page 82 | score 0.033
1. Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system, unless this is obvious ...
```
 
**Subagent.** `.claude/agents/corpus-researcher.md` has access only to the `search` tool, so it cannot change the index. Its instructions: search first with short legal queries and search again if needed, answer only from the passages received, cite every claim with the exact bracket, keep conditions and exceptions, say the documents do not cover it when they do not, be short, and end with "This is a reading of the text, not legal advice."
 
Transcript from my editor:

```
> Do we have to tell guests that they are talking to an AI chatbot?

● corpus-researcher
  ⎿ mcp__corpus__search(query: "transparency obligation AI system interacts directly with natural persons informed")
    5 passages for: transparency obligation AI system interacts directly with natural persons informed
    [1] cite as [ai_act, Article 50(1)-(3)]  | Article 50(1)-(3) - Transparency obligations for providers and deployers ... | PDF page 82
    [2] cite as [ai_act, Article 50(4)-(7)]  | Article 50(4)-(7) - Transparency obligations for providers and deployers ... | PDF page 82
    [3] cite as [ai_act, Annex XII(1)-(2)]   | Annex XII(1)-(2) - Transparency information referred to in Article 53(1), point (b) ...
    [4] cite as [ai_act, Article 26(11)-(12)] | Article 26(11)-(12) - Obligations of deployers of high-risk AI systems | PDF page 69
    [5] cite as [ai_act, Article 5(1)]       | Article 5(1) - Prohibited AI practices | PDF page 51

  Answer:
  Under the AI Act, yes, in most cases, but the text puts this duty on the provider (whoever builds
  the chatbot), not directly on the hotel as deployer.

  - The rule: Providers must make sure that AI systems meant to interact directly with people are
    designed so that those people are told they are dealing with an AI system [ai_act, Article 50(1)-(3)].
  - Exception: The duty does not apply if it is "obvious from the point of view of a natural person who
    is reasonably well-informed, observant and circumspect, taking into account the circumstances and
    the context of use" [ai_act, Article 50(1)-(3)]. It also does not apply to systems authorised by law
    for criminal-law enforcement purposes [ai_act, Article 50(1)-(3)].
  - When and how: Guests must get the information "in a clear and distinguishable manner at the latest
    at the time of the first interaction". It must also meet the applicable accessibility requirements
    [ai_act, Article 50(4)-(7)].
  - Duties that do fall on the deployer:
    - If the chatbot also does emotion recognition or biometric categorisation, the hotel itself must
      tell guests that the system is running [ai_act, Article 50(1)-(3)].
    - If the system counts as a high-risk system under Annex III and makes or helps make decisions about
      people, the hotel must tell them it is being used [ai_act, Article 26(11)-(12)].
    - Article 50 does not replace other transparency duties for deployers under EU or national law
      [ai_act, Article 50(4)-(7)]. National laws are not in the indexed documents.

  This search only covered the AI Act. I did not search the GDPR's rules on informing guests about how
  their personal data is processed.

  This is a reading of the text, not legal advice.
```
 
Reflection: It searched once, cited Article 50(1)-(3), 50(4)-(7) and 26(11)-(12), all really retrieved. It noticed the disclosure duty falls on the provider, not the hotel as deployer. The weakness is that it did not check the GDPR side.
 
## Adding a document
 
If the identical file is already indexed, nothing changes and the tool replies "Already indexed ... Nothing was changed." If a file has the same name but different content, the old chunks are replaced by the new ones. I tested the first case by adding the same file twice.
 
**Unanswerable question (q34):** "Does the ban on emotion recognition at work also cover job candidates during hiring?" The AI Act only says "workplace and education institutions".
 
**Document added:** the Commission Guidelines on prohibited AI practices (C(2025) 5052, https://ec.europa.eu/newsroom/dae/redirection/document/112367, 60,706 words, 222 chunks), added through the tool with approval.
 
**Before:** the answer said the indexed documents do not explicitly state whether the ban covers candidates, then listed related rules (Article 5(1) and the recruitment area of Annex III).
 
**After:** "Yes, the ban on emotion recognition in the workplace also covers job candidates." It cited the guidelines, Section 7.2.2, para (254), which says the notion of workplace applies to candidates during selection and hiring. Before the addition none of the retrieved passages came from this guideline. After it, Sections 7, 7.1, 7.2.2 and 7.2.3 of the new document were retrieved. The evaluation removes the document afterwards, so the committed index is the three-document baseline.
 
## Harness and guardrails
 
`agent.py` uses LangChain `create_agent` with `AGENTS.md` as the system prompt and the MCP tools from `server.py`.
 
**AGENTS.md rules** (each has its reason written next to it in the file): 1) answer only from search results, 2) cite every claim with the exact bracket and never cite what was not retrieved, 3) say when the corpus does not cover the question and stop, 4) search again before giving up and combine passages, 5) keep to what the text says including exceptions, 6) no legal advice, 7) add documents only on request, 8) be short.
 
**Approval step.** Before `add_document` runs, the tool asks the person "Approve? [y/N]". With no person present the answer is no. Reason: adding a document changes the shared index for everyone.
 
**Search limit.** At most 6 searches per question, as a safety net against loops, cost and the free-tier quota. Most questions needed one to three searches. The risk is that a limit that is too low causes a wrong refusal.
 
**Extra guardrail: citation check.** The code records every passage a search returned. Every `[source, Article N]` in the answer must match one of them. If not, the model gets one retry. If it still cites something it never received, the citation is replaced by "[citation removed: not in the search results]" and a warning is added. Reason: an invented legal citation is worse than none. It checks that the cited passage was retrieved, not that it supports the claim (the judge's "supported" grade covers that).
 
**Case where it fired:** in the real run of 35 questions it never fired (0 retries, 0 removals), because the agent only cited passages it received. To show that it works, I ran a deliberate test (not a real case): I gave the guardrail functions an answer that cites one retrieved passage and one that was never retrieved (GDPR Article 83, as if the model cited it from memory).

```
Retrieved passages: ['ai_act, Annex XII', 'ai_act, Article 26', 'ai_act, Article 5', 'ai_act, Article 50']

Answer given to the guardrail:
Yes, guests must be told they are talking to an AI system [ai_act, Article 50(1)-(3)]. Breaking this rule can lead to fines of up to 20 million euros [gdpr, Article 83].

check_citations found: ['[gdpr, Article 83]']

After strip_citations:
Yes, guests must be told they are talking to an AI system [ai_act, Article 50(1)-(3)]. Breaking this rule can lead to fines of up to 20 million euros [citation removed: not in the search results].

(Warning: some citations could not be verified and were removed.)
```

The valid citation stays and the invented one is caught and removed. In the real agent, the model would first get one retry to fix the answer before the citation is removed; this test skips the retry because it calls the functions directly. One limitation shows here: the guardrail removes the citation but not the claim itself, so "fines of up to 20 million euros" stays in the text, now visibly marked as unverified.
 
## Evaluation
 
The agent (`gemma-4-31b-it`) answered all 35 questions. A different model (`gemma-4-26b-a4b-it`) acted as judge, so it does not grade its own work. I used Gemma because the free Gemini tier allows only about 20 generation requests a day.
 
**Code checks:** whether every citation matches a retrieved passage, whether the agent refused on unanswerable questions, and whether it wrongly refused an answerable one.
 
**Judge rubric** (two grades, 0 or 1):
* correct. For answerable questions, the answer states the key facts of the reference answer and contradicts none, and a refusal is 0. For unanswerable questions, 1 only if it says the indexed documents do not cover the question.
* supported. 1 if every factual claim is in the retrieved passages, even a true claim counts as 0 if the passages do not contain it. Closing lines like "not legal advice" do not count.

**Agreement with the judge.** I graded 26 answers myself before seeing the judge's verdicts. We agreed on 26 of 26 (100%) for both correct and supported. This is weaker evidence than it sounds. For "correct" the kappa of 1.0 rests on a single shared failure (q34). For "supported" we both gave 1 to all 26, so there is no variation and kappa is undefined (the script prints 1.0 as a default). High agreement on an easy set does not prove the judge would catch failures.
 
**Results (35 questions):**
* Correct: 34 of 35
* Answerable correct: 28 of 28
* Unanswerable correctly refused: 6 of 7
* Wrong refusals: 0
* Unsupported claims: 0
* Invalid citations: 0
## Failures
 
One question failed, q34. The agent did not refuse cleanly. It said the text does not define "workplace" and then listed related rules, which implied an answer. The judge and I both marked it incorrect.
 
| Cause | Count |
|---|---|
| Retrieval miss | 0 |
| Wrong answer from the right passage | 0 |
| Unsupported claim | 1 |
| Wrong refusal | 0 |
| Bad test question | 0 |
 
I'd say q34 is an unsupported claim because it implied an answer to an unanswerable question. However, the other possibility would be a bad test question, because the AI Act does touch the topic (Article 5(1)(f) and Annex III) and my own reference answer admits the text is ambiguous.
 
What to fix first: I'd add harder unanswerable questions that sound answerable and review q34's wording, then add questions with exceptions or conflicting articles. I'd like for the agent to be better tested so I can implement improvements, like making it search both the AI Act and the GDPR when a question involves guest data, and then measure whether they work.
 
## Decision
 
For now, I wouldn't let hotel management rely on the assistant because although it's very accurate on this test set, the set is small and fairly easy and most questions ask for one article by topic. We only consider three EU texts, no national law such as Spain's or other types of documents that would affect decision making and that a lawyer would take into account. I'd say it's reasonable to use it as a research aid that points to the right articles, using a lawyer for real decisions.
 
**Cost and latency per question:** about 5,900 input tokens and 650 output tokens, with 1 to 3 searches. Average time was 111 seconds (90th percentile 178 seconds), mostly free-tier rate-limit waiting. On Gemini Flash it took 4 to 10 seconds.
 
## AI-use disclosure
 
I used Claude (Claude Code and chat) throughout this assignment.

**Code.** Claude wrote the code: `index.py` (extraction, cleaning, the two chunking designs, embedding, hybrid search), `server.py` (the two MCP tools), `agent.py` (the LangChain harness and its three guardrails) and `evaluate.py` (retrieval metrics, code checks, the LLM judge, agreement with my grades and the add-document demo). Claude also drafted `AGENTS.md` and the subagent file `.claude/agents/corpus-researcher.md`.

**Test set.** Claude drafted the 35 questions and their reference answers from the documents. I read all 35 and kept them as they were.

**Running and setup.** Claude helped me apply the work to my GitHub fork, run the check workflow, run the subagent for the transcript in this report, and compute the agreement between my grades and the judge. It also helped me implement the deliberate guardrail test since it never needed to fire in the real run. 

**Report.** I wrote this report. Claude gave me a first draft of the factual parts (the numbers and the descriptions of the code), which I rewrote in my own words, and fixed formatting. The use case, the reflections, the failure classification, what to fix first and the decision are written by me.

**What is mine.** The use case is my own idea: I chose hotels because my thesis is about automating hotel touchpoints, so the question of which guest-facing AI tools are allowed under EU law matters directly for my work. I suggested building the corpus around the AI Act and the GDPR; Claude chose the specific documents and versions (including the Commission guidelines on the AI system definition and, for the add-document demo, the guidelines on prohibited practices). I graded 26 answers myself in `eval/human_labels.csv` before looking at the judge's verdicts. The classification of the q34 failure, what to fix first, and the decision are my own.

**Learning.** I used Claude, including Claude voice mode, to understand the concepts of the class, such as RAG, embeddings, chunking, LangChain and MCP. Claude also explained the code to me: what each file does (`index.py`, `server.py`, `agent.py`, `evaluate.py`, `main.py`, `AGENTS.md` and the subagent file) and how the files work together, so I could explain my own choices in the written comprehension check. 
