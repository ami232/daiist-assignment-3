# Assignment 3 Report

- **Name**: Edgar Andres Bran Valle
- **Student ID**: 18789
- **Group**: BBADBA 5B 

## Use case
A compliance analyst at an investment bank needs to check what the firm is allowed to do under the MiFID II, MiFIR, and PRIIPs regulations before advising or selling products/services to potential clients.  They use the agent's answer to decide what the firm is able to do and use the information to quote the cited article in the compliance file. A wrong answer can lead the firm to break the compliance rules and potentially face fines, client damage claims, and lawsuits. An "I don't know" answer by the agent only costs the analyst time to look for the information elsewhere instead of facing large repercussions. A wrong answer is far more damaging than a refusal. 

## Corpus

Four EU legal acts on investment services and retail investment products, in English, from EUR-Lex. All are under the EUR-Lex reuse policy (Commission Decision 2011/833/EU: reuse authorised, with acknowledgement of the source), and none contains personal data. The PDFs are committed in `corpus/`, because EUR-Lex blocks scripted downloads with a bot challenge.

| Document (source name) | URL | Date | Licence | Pages | Words |
|---|---|---|---|---|---|
| Directive 2014/65/EU, MiFID II (`MiFID II`) | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32014L0065 | 15 May 2014 | EUR-Lex reuse (Decision 2011/833/EU) | 148 | 75,950 |
| Regulation (EU) No 600/2014, MiFIR (`MiFIR`) | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32014R0600 | 15 May 2014 | EUR-Lex reuse (Decision 2011/833/EU) | 65 | 36,478 |
| Delegated Regulation (EU) 2017/565 (`MiFID II Delegated Regulation`) | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0565 | 25 April 2016 | EUR-Lex reuse (Decision 2011/833/EU) | 83 | 47,080 |
| Regulation (EU) No 1286/2014, PRIIPs (`PRIIPs`) | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32014R1286 | 26 November 2014 | EUR-Lex reuse (Decision 2011/833/EU) | 23 | 13,891 |
| **Total** | | | | **319** | **173,399** |

The word counts are after cleaning (headers, footers and page numbers removed). Each act is the original text as published in the Official Journal, not a consolidated version, so later amendments (for example the 2021 MiFID II "quick fix") are not in the corpus.

Held back for the add-document demo (see *Adding a document*): Delegated Regulation (EU) 2017/653, the PRIIPs regulatory technical standards (`PRIIPs RTS`), https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0653, 8 March 2017, same licence.

## Ingestion

**Extract and clean** (`index.py`).
- pypdf extracts the text page by page.
- Cleaning normalises Unicode (NFKC), removes soft hyphens, re-joins words hyphenated across lines and collapses whitespace.
- It drops page numbers, running headers and footers (lines that repeat at the top or bottom of 30%+ of pages), and the Official Journal header line wherever pypdf places it.

**Structure.**
- A new section starts at every line that is exactly `Article N` or `ANNEX …`.
- When a document gives its articles titles, the title on the next line is added to the location, e.g. `Article 25 (Assessment of suitability and appropriateness and reporting to clients)`. PRIIPs has no article titles; this is detected per document.
- Text before Article 1 is labelled `Recitals`.

**Chunking: two designs** (see *Retrieval*).
- `sections`: one chunk per article. Articles longer than 350 words are split on sentence boundaries. The embedded text is prefixed with `source - heading`, so each chunk carries the article it belongs to.
- `words150`: fixed windows of 150 words with a 30-word overlap, ignoring structure, with no prefix.

**Chunk metadata.**
- `source`: the document name, as used in citations.
- `location`: the article with its title and page range, e.g. `Article 16 (Organisational requirements), pp. 49-50`. A `words150` window that crosses two articles is labelled `Article 3 to Article 4`.
- Chunk number and word count.
- Documents added with `add_document` also store their file's SHA-256 and path.
- Search results show the citation tag `[source | location]`.

**Embedding and storage.**
- Chunks are embedded with `gemini-embedding-2` at 768 dimensions, normalised to unit length, as `RETRIEVAL_DOCUMENT`; questions are embedded as `RETRIEVAL_QUERY`.
- Vectors are written to ChromaDB (cosine distance) in `index/` after every batch of 50. A rerun embeds only chunks without a saved vector, and query vectors are cached in `index/query_vectors.json`.
- `index/` is 34 MB.

**Number of chunks.**

| Document | `sections` | `words150` |
|---|---|---|
| MiFID II | 291 | 633 |
| MiFIR | 145 | 304 |
| MiFID II Delegated Regulation | 191 | 393 |
| PRIIPs | 65 | 116 |
| **Total** | **692** (mean 251 words) | **1,446** (mean 149 words) |

The add-document demo later added 92 `sections` chunks for the PRIIPs RTS.

**Extraction problem fixed: false article headings.**
- *The problem.* The first heading pattern accepted any line starting with "Article N" or a number followed by text. Numbered paragraphs ("1. This Regulation establishes uniform requirements…") and cross-references at the start of a line ("Article 114 of the Treaty on the Functioning of the European Union…", "Article 4(1)(52) of Directive 2014/65/EU;") became new sections, and so did the Official Journal header ("31.3.2017 L 87/1 …").
- *The size of it.* MiFIR has 55 articles but produced 109 headings; the Delegated Regulation produced 240 headings for 91 articles.
- *Why it matters.* The location of every chunk after a false heading was wrong, so citations would have pointed to a paragraph or a cross-referenced act instead of the real article.
- *The fix.* A heading must be a line that is exactly `Article N` (optionally with a letter, e.g. `Article 4a`) or `ANNEX …`.
- *The result.* MiFIR now has 56 sections (55 articles plus Recitals) and the Delegated Regulation 96 (91 articles plus annexes and recitals). Every article in MiFIR, MiFID II and the Delegated Regulation now carries its title.

## Test set

**How it was written.**
- Since the documents where very large I started from reading summaries of the articles provided by AI in the four PDFs (KID rules, suitability, best execution, reporting deadlines) and asked what a compliance analyst would need to check before advising or selling to a retail client.
- The questions were drafted and later checked with AI for assignment compliance and model coherence. 

**Unanswerable questions.** I chose topics just outside the corpus, so they are close to its subject, not obviously off-topic:
- *Mentioned but not detailed in the corpus:* the summary risk indicator (q34) and the performance scenarios (q35), which PRIIPs leaves to the technical standards; and the CFD leverage limits (q38), where MiFIR only gives ESMA the power to intervene.
- *Later amendments:* the 2021 MiFID II quick fix (q39) and sustainability preferences (q37).
- *Law that is not in the corpus:* fines imposed by the Spanish CNMV (q36) and MiCA (q40).

**When it was written.** `eval/questions.csv` was committed on 21 November, before the evaluation ran the same day, and no question has been changed since (see the git history).

**Counts.**

| Kind | Questions |
|---|---|
| single (one passage) | 26 |
| multi (two passages) | 7 |
| unanswerable | 7 |
| **Total** | **40** |

By expected source: PRIIPs 14, MiFID II 13, MiFID II Delegated Regulation 9, MiFIR 4. Each multi-passage question counts once per source.

**Two examples.**

| id | Kind | Question | Expected | Reference answer |
|---|---|---|---|---|
| q13 | single | How long must recordings of client telephone conversations be kept? | MiFID II, Article 16 | Five years, and up to seven years if the competent authority requests it. |
| q27 | multi | What information must we collect from a client before giving investment advice, and what must the recommendation satisfy? | MiFID II, Article 25; MiFID II Delegated Regulation, Article 54 | Knowledge and experience, financial situation including ability to bear losses, and objectives including risk tolerance; the recommendation must meet the objectives, be financially bearable and understood, and nothing is recommended if nothing is suitable. |

## Retrieval

**Method.**
- For each of the 33 answerable questions, the top-k chunks are compared with `expected_source` and `expected_location`. A hit is the right document and the right article (or an overlapping page range).
- *hit@k*: at least one expected passage is among the top k. *all@k*: every expected passage is (this matters for the multi-passage questions).
- Only the four original documents are searched, so the demo document cannot skew the comparison.
- Code: `evaluate.py`; results: `eval/retrieval.csv`.

**Three designs.** Two chunkings, plus hybrid search on the better one. The hybrid search is reciprocal rank fusion of the vector ranking and a BM25 keyword ranking, and needs no extra embeddings.

| Design | hit@1 | hit@3 | hit@5 | all@5 | Words added to the prompt (k=1 / 3 / 5) |
|---|---|---|---|---|---|
| `words150`, vector | 0.58 | 0.88 | 0.91 | 0.79 | 150 / 450 / 750 |
| **`sections`, vector** | **0.76** | **0.94** | **0.97** | **0.88** | 260 / 813 / 1,339 |
| `sections`, hybrid | 0.58 | 0.94 | 0.97 | 0.85 | 282 / 851 / 1,395 |

**Design chosen: `sections` with vector search.** The agent and the server use it, with k = 5.
- It has the best hit rate at every k: 0.76 against 0.58 at k = 1, and at k = 5 it finds a right passage for 32 of 33 questions.
- `words150` adds fewer words to the prompt, but finds the right passage less often. A 150-word window often cuts an article in half and carries no article title, while a `sections` chunk keeps the article together and is embedded with its title.
- Hybrid search matches vector search at k = 3 and 5 but is clearly worse at k = 1, so it adds nothing here.
- The cost of `sections` is about 1,340 words of context at k = 5, which is small for the model.
- The one question missed even at k = 5 is q23 (expected: Delegated Regulation, Article 56). It retrieves MiFID II Annex II on professional clients instead, which arguably also answers the question.

## Tools and subagent

**MCP server** (`server.py`, registered as `corpus` in `.mcp.json` and `.vscode/mcp.json`). It loads `index/` at startup, never re-embeds the corpus, and writes nothing to stdout. The tool descriptions are the docstrings the model reads:

`search(query)`:
```text
Search EU investment-services legislation and return the most relevant passages.

The corpus holds the English texts of MiFID II (Directive 2014/65/EU), the
MiFID II Delegated Regulation (EU) 2017/565, MiFIR (Regulation 600/2014) and
the PRIIPs Regulation (1286/2014), split by article, plus any document added
with add_document. It does not hold national law, supervisors' guidance or
later amendments.

Use this for every factual question about these rules, before answering.
Phrase `query` as a specific question or keywords; search again with other
wording if the first results do not answer it.

Returns up to 5 passages. Each starts with a citation tag
`[source | location]` (document name, then section and page). Cite a passage
by copying its tag exactly.
```

`add_document(path)`:
```text
Add one document (PDF, HTML, TXT or MD file on this machine) to the corpus.

`path` is the file's path. The file is extracted, chunked, embedded and
stored with the same pipeline as the rest of the corpus, after which search
can find it. The document is named after the file. If a document with that
name is already indexed with identical content, nothing changes; if its
content changed, its old passages are replaced.

Returns what happened: added, replaced or unchanged, with chunk counts.
```

**One search result.** The first two of the five passages for q13, "How long must recordings of client telephone conversations be kept?":
```text
[MiFID II | Article 16 (Organisational requirements), p. 49] (score 0.819)
6. An investment firm shall arrange for records to be kept of all services, activities and transactions undertaken by it which shall be sufficient to enable the competent authority to fulfil its supervisory tasks and to perform the enforcement actions under this Directive, Regulation (EU) No 600/2014, Directive 2014/57/EU and Regulation (EU) No 596/2014, and in particular to ascertain that the investment firm has complied with all obligations including those with respect to clients or potential clients and to the integr …

[MiFID II Delegated Regulation | Article 76 (Recording of telephone conversations or electronic communications), pp. 64-65] (score 0.817)
7. Investment firms shall demonstrate the policies, procedures and management oversight of the recording rules to the relevant competent authorities upon request. 8. Before investment firms provide investment services and activities relating to the reception, transmission and execution of orders to new and existing clients, firms shall inform the client of the following: (a) that the conversations and communications are being recorded; and (b) that a copy of …
```

**Subagent** (`.claude/agents/corpus-researcher.md`). Its only tool is `mcp__corpus__search`:
```markdown
---
name: corpus-researcher
description: Answers questions about EU investment-services rules from the indexed legal texts: MiFID II (Directive 2014/65/EU), the MiFID II Delegated Regulation (EU) 2017/565, MiFIR (Regulation 600/2014) and the PRIIPs Regulation (1286/2014), plus any document added with add_document. Delegate to it any question on investor protection, suitability and appropriateness, inducements, costs and charges disclosure, best execution, record-keeping, client reporting, transparency and transaction reporting, product intervention, or PRIIPs key information documents, when the answer must be cited to the article.
tools: mcp__corpus__search
---

You support a compliance analyst at an investment firm who checks what the firm must do under MiFID II, MiFIR and PRIIPs before advising or selling to retail clients. A wrong answer can lead the firm to break the rules and face fines, client damages claims or a product ban, so an honest "not covered" is better than a guess. Your only source is the `search` tool of the corpus server.

1. Search before answering. Search again with different wording (article topic, defined terms such as "retail client", "inducement", "key information document") if the first results do not answer the question. For a question that combines two rules, search for each part separately.
2. Answer only from the passages the search returned. Do not add rules, numbers or dates from memory, even if you believe they are correct: the analyst must be able to show the exact article behind every claim.
3. Cite every factual sentence with the passage tag copied exactly as the tool printed it, e.g. `[MiFID II | Article 16 (Organisational requirements), pp. 49-50]`. Never invent, shorten or merge tags.
4. If the passages do not contain the answer, reply exactly: `The corpus does not cover this question.` You may then add one cited sentence on what the corpus covers nearby, labelled as context ("For context, the corpus covers ..."), never presented as the answer. National law, supervisors' practice, later amendments and other regulations (e.g. MiCA) are usually not covered.
5. If only part of the question is answered, answer that part with citations and say clearly which part is not covered, so the analyst knows what to look up elsewhere.
6. Be concise: start with a one- or two-sentence direct answer, then the supporting points, each cited. Use more detail only when the question has several parts. End with the list of sources you cited.
```

**Transcript from Claude Code** (in GitHub Codespaces, 23 November). The full export is in `eval/subagent_transcript.txt`. Claude Code delegated to `corpus-researcher`, which searched the corpus and answered with exact citation tags; Claude Code then passed on the answer. The subagent's search calls are collapsed in this export view. The transcript was recorded with an earlier version of the subagent's instructions, before the use-case paragraph, the context labelling and the answer-length rule shown above were added.
```text
❯ Use the corpus-researcher subagent to answer: When must a suitability
  statement be given to a retail client?

● corpus-researcher(Suitability statement timing question)
  ⎿  Backgrounded agent (↓ to manage · ctrl+o to expand)

● The corpus-researcher subagent is now searching the corpus for this question.
  I'll share its answer, with citations, as soon as it finishes.

✻ Cooked for 5s · done 6:18 PM

› Message from corpus-researcher
  **Answer**

  **Timing.** When a firm gives investment advice, it must give the client a
  statement on suitability in a durable medium before the transaction is made.
  The statement must set out the advice given and how that advice meets the
  retail client's preferences, objectives and other characteristics [MiFID II |
  Article 25 (Assessment of suitability and appropriateness and reporting to
  clients), p. 62]. The Delegated Regulation also says the firm must give the
  retail client a report outlining the advice and explaining how the
  recommendation suits the client. That explanation covers the investment term
  required, the client's knowledge and experience, the client's attitude to risk
  and capacity for loss, and whether the client is likely to need a periodic
  review [MiFID II Delegated Regulation | Article 54 (Assessment of suitability
  and suitability reports), pp. 51-52]. Recital 83 asks firms to judge "in good
  time" by the client's need for enough time to read and understand information
  before deciding to invest [MiFID II | Recitals, p. 15].

  **Distance communication exception.** Sometimes the agreement to buy or sell
  is concluded by a means of distance communication that prevents giving the
  statement beforehand. In that case the firm may give the written statement in
  a durable medium immediately after the client is bound by any agreement, but
  only if both of these conditions are met:
  - (a) the client has agreed to receive the statement without undue delay after
  the transaction is concluded; and
  - (b) the firm has offered the client the option of delaying the transaction
  to receive the statement in advance.

  [MiFID II | Article 25 (Assessment of suitability and appropriateness and
  reporting to clients), pp. 62-63]

  **Periodic suitability.**
  - Where a firm provides portfolio management, or has told the client it will
  carry out a periodic suitability assessment, the periodic report must contain
  an updated statement of how the investment meets the client's preferences,
  objectives and other characteristics [MiFID II | Article 25 (Assessment of
  suitability and appropriateness and reporting to clients), pp. 62-63].
  - After the first report, later reports may cover only changes in the services
  or instruments and/or in the client's circumstances [MiFID II Delegated
  Regulation | Article 54 (Assessment of suitability and suitability reports),
  pp. 51-52].
  - Firms that provide a periodic suitability assessment must review the
  suitability of their recommendations at least once a year, and more often
  depending on the client's risk profile and the type of instruments [MiFID II
  Delegated Regulation | Article 54 (Assessment of suitability and suitability
  reports), p. 52].
  - Those firms must also disclose three things: how often and how far the
  assessment goes (including what triggers it), how far information already
  collected will be reassessed, and how an updated recommendation will be
  communicated [MiFID II Delegated Regulation | Article 52 (Information about
  investment advice), p. 49].

  The search results give no fixed deadline (number of days) for "without undue
  delay". They also say nothing about national rules or later amendments to
  these provisions.

  **Sources cited**
  - [MiFID II | Article 25 (Assessment of suitability and appropriateness and
  reporting to clients), p. 62]
  - [MiFID II | Article 25 (Assessment of suitability and appropriateness and
  reporting to clients), pp. 62-63]
  - [MiFID II Delegated Regulation | Article 54 (Assessment of suitability and
  suitability reports), pp. 51-52]
  - [MiFID II Delegated Regulation | Article 54 (Assessment of suitability and
  suitability reports), p. 52]
  - [MiFID II Delegated Regulation | Article 52 (Information about investment
  advice), p. 49]
  - [MiFID II | Recitals, p. 15]

● A suitability statement must be given before the transaction is made. When a
  firm gives investment advice, it must provide the statement in a durable
  medium. The statement sets out the advice and how it meets the retail client's
  preferences, objectives and other characteristics [MiFID II | Article 25
  (Assessment of suitability and appropriateness and reporting to clients), p.
  62]. The report must also explain how the recommendation suits the client,
  including the client's attitude to risk and capacity for loss [MiFID II
  Delegated Regulation | Article 54 (Assessment of suitability and suitability
  reports), pp. 51-52].

  Exception for distance communication: sometimes the agreement is concluded by
  a means of distance communication that prevents giving the statement
  beforehand. The firm may then give it immediately after the client is bound,
  but only if both of these are true:
  - the client agreed to receive it without undue delay after the transaction;
  - the firm offered the client the option of delaying the transaction to get
    the statement first.

  [MiFID II | Article 25 (Assessment of suitability and appropriateness and
  reporting to clients), pp. 62-63]

  Ongoing advice: this applies where the firm provides portfolio management or
  has promised a periodic suitability assessment.
  - Each periodic report must contain an updated suitability statement [MiFID II
    | Article 25 (Assessment of suitability and appropriateness and reporting
    to clients), pp. 62-63].
  - Suitability must be reviewed at least once a year [MiFID II Delegated
    Regulation | Article 54 (Assessment of suitability and suitability reports),
    p. 52].

  Not covered by the corpus: a fixed deadline in days for "without undue delay",
  national rules and later amendments.

✻ Cooked for 5s · done 6:18 PM

● Agent "Suitability statement timing question" finished · 22s
```

## Adding a document

**Already indexed.**
- `add_document` names a document after its file (mapped to a short source name, e.g. `PRIIPs RTS`) and stores the file's SHA-256 with its chunks.
- Same name and same content: nothing changes and nothing is re-embedded. The tool answers that the document is already indexed with identical content.
- Same name but changed content: the old chunks are deleted and the new ones embedded, so no outdated passages remain.
- In every case, chunks that already have a saved vector are never embedded again.

**The demo** (full record: `eval/add_document_demo.md`).
- *The question:* q34, "How is the summary risk indicator class from 1 to 7 calculated for a PRIIP?". It is unanswerable in the evaluated corpus, because PRIIPs Article 8 leaves the method to regulatory technical standards.
- *The document added:* Delegated Regulation (EU) 2017/653, the PRIIPs RTS (`reserve/CELEX_32017R0653_EN_TXT.pdf`), added through the agent. I asked `main.py ask` to add the file, approved the call at the `Allow? [y/N]` prompt, and the 52-page document became 92 chunks.

*Before* (evaluation run):
> The provided corpus does not contain the specific calculation methodology for the summary risk indicator class (1 to 7) for a PRIIP. It notes that the methodology underpinning the presentation of risk and reward is to be specified in regulatory technical standards [PRIIPs | Article 8, p. 13].

*After* (with the PRIIPs RTS indexed; the MRM class table is shortened here):
> The Summary Risk Indicator (SRI) for a PRIIP is determined by applying the methodology for the presentation of risk set out in Annex II and the technical aspects for the presentation of the SRI set out in Annex III [PRIIPs RTS | Article 3 (‘What are the risks and what could I get in return?’ section), pp. 6-7]. Market risk is measured by the annualised volatility corresponding to the value-at-risk (VaR) at a confidence level of 97,5 % over the recommended holding period [PRIIPs RTS | ANNEX II (METHODOLOGY FOR THE PRESENTATION OF RISK), p. 15]. The PRIIP is assigned a Market Risk Measure (MRM) class from 1 (VEV < 0,5 %) to 7 (VEV > 80 %) [PRIIPs RTS | ANNEX II (METHODOLOGY FOR THE PRESENTATION OF RISK), p. 15]. … The SRI is presented in the key information document using a numerical scale from 1 to 7, where 1 is the lowest risk class and 7 is the highest [PRIIPs RTS | ANNEX III (PRESENTATION OF SRI), p. 26].

What the demo shows:
- *Before:* the agent declined and pointed to where the answer would be (the technical standards).
- *After:* it answered from the new document with exact citations, at 8,477 tokens and 10 s.
- *Note:* the "before" answer declined in its own words, not with the exact refusal sentence, so the code check counted it as an answered unanswerable question (see *Failures*).

## Harness and guardrails

**Harness** (`agent.py`).
- A LangChain `create_agent` on Gemini (`gemini-3.1-flash-lite`).
- Its tools are those of `server.py`, reached over MCP (stdio).
- Its system prompt is `AGENTS.md`.
- `main.py ask` prints the answer and the list of cited sources.
- It returns the answer, the tool trace, the tokens and the seconds to `evaluate.py`.

**`AGENTS.md` rules**, each with its reason in the file:
1. Search before answering, every time.
2. Answer only from the search results.
3. Cite every claim with the exact `[source | location]` tag.
4. When the corpus does not cover the question, reply exactly `The corpus does not cover this question.` A nearby rule may be added only when labelled as context.
5. Label partial answers.
6. Add documents only when asked.
7. Be brief.

The rules start by stating the use case (a compliance analyst, and the cost of a wrong answer), so the model knows why refusing beats guessing.

**Approval step.**
- `HumanInTheLoopMiddleware` pauses every `add_document` call until a person answers `Allow? [y/N]` at the terminal. A "no" is passed back to the model as a rejected tool call.
- With no terminal (evaluation, `check.py`), the call is denied automatically, so the evaluation can never change the corpus.

**Call limits.** At most 8 model calls and 5 searches per question.

**Extra guardrail: citation verification.**
- After the agent answers, code checks that every `[source | location]` tag in the answer was actually returned by `search` in this conversation, and that an answer that is not a refusal cites something.
- If the check fails, the agent gets one chance to rewrite the answer. If the rewrite still fails, the answer is replaced by the refusal sentence, so no answer with an unverifiable citation ever reaches the analyst.

**A case where it fired.** For "How long must recordings of client telephone conversations be kept?":
- The first draft cited `[MiFID II | Article 16 (Organisational requirements), p. 50]` and `[MiFID II Delegated Regulation | Article 76 (…), p. 65]`, but search had returned `pp. 49-50` and `pp. 64-65`.
- The guardrail rejected the shortened tags, and the rewrite used the exact ones.
- It fired on 19 of the 40 evaluation questions. The rewrite passed in 15; in 4 (q10, q14, q28, q33) it failed again and the answer was withheld. Those 4 are exactly the wrong refusals in *Failures*.

## Evaluation

The agent answered all 40 questions (`eval/answers.jsonl`), with `add_document` always denied. Each answer was then checked in code and graded by an LLM judge, and I graded all 40 myself.

**Code checks** (`evaluate.py`, `eval/results.csv`).
- *Citations valid:* every `[source | location]` tag in the answer was returned by search. Result: 0 invalid citations in 40 answers; the guardrail makes this hold by construction.
- *Has a citation:* any answer that is not a refusal cites at least one passage.
- *Cites the expected article.*
- *Refusal:* the answer contains the exact refusal sentence. For unanswerable questions, correctness is decided by this check, not by the judge.

**LLM judge.** `gemini-3.1-flash-lite` (temperature 0, JSON output) gets the question, the reference answer, the passages the agent retrieved as evidence, and the agent's answer. It returns `correct`, `supported` and a one-sentence reason (`eval/judge.jsonl`). My rubric:
```text
You grade an assistant's answer to a question about EU investment-services
legislation (MiFID II, its Delegated Regulation, MiFIR, PRIIPs).

CORRECT (0 or 1)
- correct = 1 when the answer covers every key point of the reference answer.
  Small details may be missing.
- If a whole part of a multi-part question is missing, correct = 0.
- Extra detail is fine as long as it is accurate and does not contradict the
  reference.
- Question the corpus cannot answer (the reference says so): correct = 1 only
  if the answer clearly says the corpus does not cover it ("The corpus does not cover this question."). It may
  add one cited sentence about what the corpus covers nearby.
- An answer that presents a related rule as if it were the answer is correct = 0.
  It is correct = 1 only if it first says the corpus does not cover the question
  and labels the related rule as context, not as the answer.
- A refusal to a question the corpus can answer is always correct = 0.

SUPPORTED (0 or 1)
- supported = 1 when every claim is backed by the evidence passages. A faithful
  paraphrase is fine; exact wording is not needed.
- A claim is unsupported when the answer attributes a passage to a different
  subject, law, authority or date than the passage itself has, even if the
  words appear in the passage.
- A claim is unsupported if the passage it cites does not say it, even when a
  different evidence passage does.
- A refusal makes no factual claims, so it is supported = 1.

Give a one-sentence reason.
```

**Agreement with my grades** (`eval/human_labels.csv`, graded from `eval/grading_sheet.md` before I read any verdict):

| | First rubric (draft) | My rubric |
|---|---|---|
| correct: agreement (Cohen's κ) | 97.5% (0.93) | 95% (0.86) |
| supported: agreement (κ) | 95% (0.00) | 95% (0.00) |
| Disagreements | correct: q29 · supported: q36, q39 | correct: q23, q29 · supported: q36, q39 |

- *Correct:* the judge agrees with me on 38–39 of 40. Where we differ, it accepted partial answers (q29: one of the two authorities found; q23) that my rubric scores 0.
- *Supported:* κ = 0 because the judge never gave 0, so its 95% agreement is only my base rate. It marked q36 and q39 as supported, though they attribute passages to the wrong authority (EU minimum fines presented as the CNMV's) and the wrong date (a 2017 recital used to describe the 2021 quick fix).
- My rubric added an explicit rule for exactly this kind of misattribution, with generic examples so the agreement is not measured on cases I described to the judge. The judge still did not apply it: it saw those answers as incorrect (no refusal), but not as unsupported.
- **Conclusion: this judge can be trusted for "correct" but not for "supported".** "Supported" needs a human or a stronger model.

**Results** (40 questions; my grades, with the judge in brackets):

| Kind | Correct |
|---|---|
| single | 23 / 26 (judge 24) |
| multi | 2 / 7 (judge 3) |
| unanswerable | 5 / 7 (code check 3) |
| **Total** | **30 / 40 (judge 30)** |

| Outcome | Count |
|---|---|
| Unsupported answers (my grades) | 2 (q36, q39); judge: 0 |
| Correct refusals (unanswerable, exact sentence) | 3 / 7 (q35, q37, q40) |
| Unanswerable answered anyway (code check) | 4 / 7 (q34, q36, q38, q39). I graded q34 and q38 as proper refusals in substance: they declined in their own words, without the exact sentence. |
| Wrong refusals (answerable but refused) | 4 / 33 (q10, q14, q28, q33), all withheld by the citation guardrail |

**Cost.**
- Agent: mean 5,718 tokens per question (median 4,875, max 13,802), and 3.1 s of model time (max 7.6 s). A full `main.py ask`, including starting the MCP server, takes about 7–25 s.
- Judge: about 2,700 tokens per answer.

## Failures

10 of 40 answers failed by my grades. Each is classified from my grading notes and the retrieved passages (`eval/results.csv`, `eval/human_labels.csv`):

| Cause | Count | Questions | What happened |
|---|---|---|---|
| Wrong refusal | 4 | q10, q14, q28, q33 | The right passages were retrieved (PRIIPs Art. 7 even at rank 1 for q10), and the agent had a correct answer. But it cited shortened or merged tags, failed the citation check twice, and the guardrail replaced the answer with the refusal. |
| Retrieval miss | 4 | q23, q29, q31, q32 | One needed article was not retrieved: Delegated Regulation Art. 56 (q23), MiFIR Art. 40 (q29), MiFID II Art. 25(6) (q31), MiFID II Art. 25(4) (q32). Three are multi-passage questions where only one part was found. The agent then answered that part and said the other was not covered: a labelled partial answer, but incomplete. |
| Unsupported claim | 2 | q36, q39 | Unanswerable questions answered with a passage attributed to the wrong authority or date: PRIIPs' EU minimum fines presented as the CNMV's (q36), and a 2017 recital used to describe the 2021 quick fix (q39). |
| Wrong answer from the right passage | 0 | | |
| Bad test question | 0 | | |

Observations:
- *Where the failures concentrate:* multi-passage questions are the weak spot (2 of 7 correct, against 23 of 26 single-passage questions). Every failure among them is either a retrieval miss on the second part or a guardrail refusal.
- *What did not happen:* the agent never invented a citation (0 invalid tags), and it never answered wrongly from a passage it had correctly retrieved.
- *A measurement note:* the code check counted q34 and q38 as unanswerable questions answered anyway. They actually declined in their own words, without the exact refusal sentence, and I graded them as proper refusals. The exact-sentence check is stricter than the behaviour it is meant to measure.

**What to fix first: the citation guardrail.**
- It caused 4 of the 10 failures, and in all 4 the agent had already retrieved the right passage and written a correct answer. So these are answers the system had and then threw away.
- The fix is small and does not weaken the guardrail's purpose: accept a citation whose source and article match a retrieved passage and whose page range overlaps it, so `p. 50` for a passage at `pp. 49-50` passes. Alternatively, have the rewrite step insert the exact tags. An invented article or a wrong source would still be rejected.
- The analyst would then get 4 more correct, cited answers instead of "not covered".

**Second: retrieval for multi-part questions** (3 failures). Search each part of the question separately, or raise k for questions that join two rules. **Third: unanswerable questions near the corpus** (2 failures). Rule 4's context labelling, added after this evaluation, targets exactly q36 and q39, but its effect has not yet been measured.

## Decision

**Yes, but only for single-rule questions, and the analyst always checks the cited article before acting.**

*What it may be used for:* questions answered by one article, such as "How long must call recordings be kept?", "In what language must the KID be written?" or "When must the KID be handed over?".
- On these it answered 23 of 26 correctly.
- Every claim carries a citation to a real retrieved article: 0 invented citations in 40 answers.
- The analyst opens the cited article and confirms the answer before acting on it or quoting it in the compliance file. The answer saves the search for the right article; it does not replace reading it.

*What it is not used for:*
- *Questions that combine two rules* (2 of 7 correct). A missing second part is flagged as "not covered" rather than answered, but the analyst cannot rely on the answer being complete.
- *Questions at the edge of the corpus,* such as national law, later amendments or other regulations. In 2 of 7 unanswerable questions it presented a nearby rule as the answer, with the wrong authority or date. The citation in those answers is real, which is exactly why the analyst must check that the cited article says what the answer claims.

*How to read the answers:*
- "The corpus does not cover this question" means look elsewhere, not that no rule exists.
- With the current guardrail, about 1 in 8 answerable questions (4 of 33) wrongly gets that answer. Fixing the guardrail first (see *Failures*) would cut this.

**Cost and latency per question.**
- Agent: mean 5,718 tokens (median 4,875, max 13,802), on `gemini-3.1-flash-lite` with `gemini-embedding-2` for the query.
- Time: 3.1 s of model time on average (max 7.6 s). A full `main.py ask`, including starting the MCP server, took about 7–25 s.
- Evaluation: each judged answer costs about 2,700 more tokens.
- At these volumes the whole project (indexing about 2,200 chunks, 40 evaluated questions, re-judging and the demo) cost a few cents of API credit out of a 5 euros I had to pay out of my own pocket.

## AI use

I used Claude Code (Anthropic) and an AI assistant throughout, as follows.

- It wrote `index.py`, `server.py`, `agent.py` and `evaluate.py`, and fixed the bugs found along the way: PDF heading detection, batch embedding with `gemini-embedding-2`, passing the API key to the MCP server, and the retrieval comparison skewed by the demo document.
- It ran the indexing, the retrieval comparison, the agent evaluation and the judge, and it set up the cloud environment and the pull requests.
- Claude Code drafted `AGENTS.md`, the judge rubric and the subagent instructions.
- I set the reasons for each rule from my use case, wrote the rubric's rules (what counts as correct, partial and supported), chose generic rubric examples so the agreement is not measured on cases described to the judge, and decided the subagent changes.
-AI provided summaries of the articles. The questions were drafted and later checked with AI for compliance with the assignment. I checked every reference answer and article number against the text.
-Claude Code wrote the factual parts from the evaluation files (tables, counts, cost).
- I chose the design by the numbers.
- I graded all 40 grades in `eval/human_labels.csv`, graded before I read the judge's verdicts.
- Claude also helped with grammar and report formatting. 
