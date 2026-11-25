# Assignment 3 Report

- **Name**:María Román Gallego
- **Student ID**: 19991
- **Group**:BBADBA 5A

## Use case

**Who asks.** A person launching their own cosmetics brand: usually the founder of a small company, with no legal team and no regulatory experience. Most likely they will be the "responsible person" of Article 4, so the obligations fall on them. The important point is that they cannot check the answer against the law. If the system gives them a statement with a citation, they believe it, because that is why they use it.

**What they do with the answer.** They decide what to do before selling and when to start, and those decisions cost money:

- whether to commission the safety report and find an assessor with the right qualifications;
- printing labels and packaging with certain texts and claims;
- notifying the product in the CPNP portal;
- producing the first batch and fixing the launch date;
- whether or not to hire a consultant.

**What happens if the system is wrong.** If it says "yes, you can sell" and that is not true, the person acts with confidence: they do not ask anyone, and they print, produce and launch. The mistake shows up late, when the money is already spent:

- labels have to be reprinted or unsupported claims withdrawn;
- corrective measures, withdrawal or recall of the product (Article 5) and informing the authorities are needed;
- if the product is not safe, the harm reaches consumers.

If it says "I don't know", the person loses some time and has to find the answer elsewhere, for example by asking a consultant or by reading Annexes II and III, which are not in the corpus. That cost is small and recoverable.

**Why a wrong answer costs more than "I don't know".**

1. *It is invisible.* An "I don't know" warns the person that they must check. A wrong "yes" looks exactly like a correct one, and the person has no way to notice the difference.
2. *It is irreversible and arrives late.* It happens after the money is spent and after exposure to authorities and consumers, not before.
3. *The user pays, not the system.* The system does not suffer the consequences of being wrong.
4. *The blind spots of the corpus make it worse.* With only four documents, the questions that most tempt a false "yes" are the ones the corpus does not cover: limits for specific substances, other countries, taxes. An answer that looks complete can hide obligations that are outside the five retrieved passages.

## Corpus

| Document | URL | Date | Licence | Words indexed |
|---|---|---|---|---|
| Regulation (EC) No 1223/2009 on cosmetic products ("Reg 1223/2009") | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32009R1223 | 30 Nov 2009 | EU reuse policy (Commission Decision 2011/833/EU): reuse allowed with credit to the source | 33,073 |
| Regulation (EU) No 655/2013 on common criteria for claims on cosmetic products ("Reg 655/2013") | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32013R0655 | 10 Jul 2013 | same | 1,542 |
| Commission Implementing Decision 2013/674/EU, guidelines on Annex I of Reg 1223/2009 (cosmetic product safety report) ("Decision 2013/674") | https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32013D0674 | 25 Nov 2013 | same | 12,660 |
| Guide to Using CPNP, Cosmetic Products Notification Portal, for Responsible Persons and Distributors ("CPNP guide") | https://ec.europa.eu/docsroom/documents/29563/attachments/1/translations/en/renditions/pdf | Last update 24 May 2017 | Commission document: CC BY 4.0 under the Commission's reuse policy (no other licence is stated in the document) | 15,462 |
| **Total** | | | | **62,737** |

Word counts are the words that end up in the index (after cleaning).

**Why Annexes II and III of Reg 1223/2009 are not indexed.** They are about 40,000 words of tables (the lists of prohibited and restricted substances) that almost nobody asks about in normal sentences, and indexing them would have used up the free embedding quota of Gemini. The price is that the agent has to say "I don't know" for questions about specific substances. Note that Article 19 refers to Annexes III to VI for the precautions of use that must appear on the label, so questions about those precautions may also be answered incompletely. (This choice was proposed by the AI assistant that helped build the index; I reviewed it and I agree with it. See "AI use".)

**Why these four documents.** Each one covers a decision of the person launching the brand: Reg 1223/2009 gives the general obligations (responsible person, safety report, notification, labelling); Reg 655/2013 says which claims can be printed; Decision 2013/674 explains how the safety report is made and who signs it; and the CPNP guide explains how to notify the product in the portal.

## Ingestion

**Extraction.** `pypdf` extracts the text of each PDF page by page. The PDF page number (1-based) is kept for every word, so a chunk can say "p. 12".

**Cleaning.** Four things are done to the extracted text:

1. repeated headers and footers are removed (described below);
2. headings that the extractor split over two lines ("Article" / "4") are joined into "Article 4";
3. lines that only look like a heading are rejected: articles come in order, so a cross-reference such as "see Article 25" that falls alone on a line and breaks that order is not treated as a new article;
4. words split by a hyphen at the end of a line are joined when the next line starts in lower case.

**One extraction problem fixed: repeated headers and footers.** It is like photocopying a book in which every page has the title at the top and the page number at the bottom. If everything is copied one after the other, those lines end up in the middle of sentences, and the search engine thinks they are part of the content. The chunk then sounds like "title of the regulation" instead of what it really says. For this reason the code deletes the short lines at the top or bottom of a page that repeat on many pages (at least 30% of the pages; digits are ignored when comparing, so a changing page number does not matter).

*What is still not fixed.* Some of these lines survive inside the chunks: "EN L 315/102 Official Journal of the European Union 26.11.2013" appears inside Section 4.4 of Decision 2013/674, and "N E9 0 0 2 . 2 1 . 2 2" appears inside Article 4 of Reg 1223/2009. I did not investigate the exact cause. Since digits are ignored by the rule, a changing page number cannot be the reason; probably `pypdf` writes these lines differently from page to page (scrambled letters and spaces), so they do not look identical, or they were not among the first or last three lines of their page. The extra words are few, but they are noise in the chunks. The extraction also leaves spaces inside some words and some hyphenated words that are not joined ("confor- mity").

**Chunking.** Two designs were built so they could be compared with numbers (see Retrieval):

- `structure`: one chunk per Article, Annex or numbered section; long sections are split into windows of about 250 words with 40 words of overlap, and tiny ones are merged. For the CPNP guide, whose numbered lines are instructions and not titles, chunks are made by page. 323 chunks.
- `fixed`: windows of about 150 words with 30 words of overlap over the whole document, ignoring its structure. 524 chunks.

**Chunk metadata.** Every chunk carries its document, its location (for example "Article 4, p. 12"), its pages and all the headings it touches. Without them the agent could not say where an answer comes from. The citation guardrail checks that the `[document | location]` the agent cites belongs to a chunk it really retrieved, which is only possible if each chunk has its label. The person launching the brand can also go to the original text to check it. And the evaluation needs the label to know whether the right chunk was found.

**Why two designs.** We did not know in advance which one would work better with these texts. `structure` respects that an article is a complete idea and keeps its name, but long articles are split and short ones are merged, so some chunks can mix topics. `fixed` is finer, but it can cut an idea in half and does not follow the limits of an article. Instead of betting on one, we measured both with the 32 questions and decided with the retrieval numbers.

## Test set

**How I wrote it.** I used a helper script (`questions_helper.py`) to see the titles of the articles and to read the text of each one. For every question I noted the document, the location and a reference answer. I wrote the questions the way someone launching a brand who does not know the law would ask them ("my face cream", "I import my cosmetics"), without copying the words of the article, to check that the system finds the idea and not just the same word.

**Counts by kind.** 32 questions: 20 `single` (one passage answers it), 6 `unanswerable` (the corpus does not cover it) and 6 `multi` (two passages from different places are needed).

**Why unanswerable questions.** I made them to check that the agent answers reliably: if I ask something it does not know, it should not invent it, which shows that everything it answers is based on evidence.

**Why multi-passage questions.** To answer them the assistant has to search in two different places, not just one: it has to find two pieces of text, one from each source, and combine them in a single answer that cites both. In a normal question, one piece of text and one citation are enough.

**Three examples (one of each kind).**

- q13 (`single`): "My cosmetic contains an ingredient classified as possibly causing cancer, where do I declare that when I notify it?" Source: CPNP guide, p. 20. Reference answer: "In the Carcinogenic, Mutagenic or toxic for Reproduction (CMR) section of the Product details tab, answering Yes if the product contains CMR substances of category 1A or 1B under Part 3 of Annex VI to Regulation 1272/2008, and then identifying each one by INCI/Chemical/IUPAC name, CAS or EC number." I chose it because I feel it is very important to know the ingredients, and if the agent cannot explain it, then the right thing is to say so and not make things up, because in the end we are dealing with the medical condition and health of a great many people.
- q21 (`unanswerable`): "What do I need to do to sell my cosmetics in the United Kingdom now that it is outside the EU?" Reference answer: "I don't know: the corpus does not cover this." I chose it because a person launching a brand would ask it naturally, and the four documents only talk about the EU. The assistant has to say "I don't know". If it made up an answer, the founder would believe it and prepare labels and paperwork with rules that are not the UK's. She would find out late, when she had already spent money, and that is the most expensive kind of mistake.
- q30 (`multi`): "Who is allowed to sign off my cosmetic's safety assessment and what proof of their qualifications has to be in the report?" Sources: Reg 1223/2009 (Article 10) and Decision 2013/674 (Section 4.4). Reference answer: "The assessor must hold a university diploma or formal qualification in pharmacy, toxicology, medicine or a similar discipline, or a course recognised as equivalent by a Member State (Article 10); the report must list the assessor's name and address, be dated and signed, and include proof of the qualification, i.e. a copy of the diploma and, where needed, proof of equivalence (Section 4.4)." I chose it because the answer is split across two documents. Article 10 of the Regulation says who can sign: someone with a university degree in pharmacy, toxicology, medicine or something similar. Section 4.4 of the Decision says what proof goes in the report: the assessor's name and address, date, signature and a copy of the diploma. The two have to be put together. With only one, the founder would know who can sign but not what to attach, or the other way round.

## Retrieval

I compared the two chunking designs on the 32 test questions. A "hit@k" means the expected passage is among the first k results for the question as written in `questions.csv`.

| Design | hit@1 | hit@3 | hit@5 | Words sent to the model per request |
|---|---|---|---|---|
| `structure` (one chunk per Article/Annex/section) | 0.65 | 0.81 | 1.00 | 1,062 |
| `fixed` (~150-word windows) | 0.54 | 0.81 | 0.92 | 750 |

**My choice: `structure`.** It finds the right chunk better: the correct chunk is always among the first 5 results (1.00 against 0.92 for `fixed`) and it puts it first more often (0.65 against 0.54). It costs about 312 more words per request (1,062 against 750), which means somewhat more cost and slowness, but it is worth it, because if the right chunk is missing the assistant may give a wrong answer or say "I don't know" when there was an answer.

## Tools and subagent

**The MCP server (`server.py`, name `corpus`)** has two tools. The model reads their descriptions, so the descriptions say what the corpus is, when to use each tool and what comes back.

- `search(query)`: "Search the EU cosmetics-regulation corpus and return the most relevant passages." It lists the four documents (and says that Annexes II and III of Reg 1223/2009 are NOT indexed), says to use it for any question about what someone must do before or while placing a cosmetic product on the EU market, and not for other topics or for the limit of one specific ingredient. Argument: `query`, in English. It returns up to 5 passages, best first, each starting with `[n] source | location (score)`, and tells the model to cite source and location and to say that the corpus does not answer instead of guessing.
- `add_document(path)`: "Add one new document to the search index, so that search can find it afterwards." It reads a local PDF, .txt or .md file inside the project folder, splits it, embeds it and stores it; the document is cited under its file name without the extension. Adding the same file twice changes nothing. It uses embedding quota, so it should only be called when the user wants the document added. It returns how many passages the file has and how many were newly added, or a clear error (file not found, unsupported type, outside the project folder, quota used up).

**One `search` call (from `check.py`).** For a question about a non-compliant product, the first result is:

```
[1] Reg 1223/2009 | Article 26, p. 18 (score 0.79)
Article 26 Non-compliance by distributors…
```

**The subagent (`.claude/agents/corpus-researcher.md`).** It is limited to one tool, `mcp__corpus__search` (the line `tools: mcp__corpus__search`). Its instructions are:

```
You answer questions about EU cosmetics rules using only the `search` tool of the `corpus` MCP server. You have no other source.

1. Call `search` first, every time, even if you think you know the answer.
2. Answer only with what the returned passages say. Add nothing from memory.
3. Cite every claim as [source | location], copied from the passage header, for example [Reg 1223/2009 | Article 4, p. 7].
4. If the passages do not answer the question, reply exactly: I don't know: the corpus does not cover this.
5. If the first search misses, search again with other words (at most twice more). For a question with several parts, search each part separately.
6. Keep the answer to 2 to 5 sentences.
```

The MCP server is registered for Claude Code in `.mcp.json` (stdio, `uv run server.py`).

Transcript (Claude Code v2.1.332 in the terminal, project folder, 25 Nov 2026, 18:34-18:35; detailed view with Ctrl+O; the main model is Claude Opus 5.5):

```
> Use the corpus-researcher subagent to answer this question: My face cream lasts more than 30 months before it goes off, do I still need to print an expiry date on the label?

corpus-researcher(Expiry date labelling question)
  Backgrounded agent
  Prompt:
    Question from someone launching a cosmetics brand in the EU: "My face cream lasts more than 30 months before it goes off, do I still need to print an expiry date on the label?"

    Search the corpus for the labelling rules on date of minimum durability for products with a durability over 30 months, and what must be shown instead (e.g. period-after-opening symbol). Return a 2-5 sentence answer with [source | location] citations copied from passage headers, or the exact refusal sentence if the corpus does not cover it.

Message from corpus-researcher
  No. Under Regulation 1223/2009 you don't have to show a date of minimum durability on cosmetic products whose minimum durability is more than 30 months [Reg 1223/2009 | Article 19 (part 2), p. 15]. Instead, the label must say how long the product is safe to use after it has been opened [Reg 1223/2009 | Article 19 (part 2), p. 15]. You show this with the symbol in point 2 of Annex VII, followed by the period in months and/or years [Reg 1223/2009 | Article 19 (part 3), p. 15]. You can leave out this period-after-opening only where durability after opening is not relevant, which the regulation describes as single-use products, products not at risk of deterioration, or products that do not open [Reg 1223/2009 | Article 19 (part 3), p. 15; Reg 1223/2009 | Preamble (part 17), p. 4-5]. The cosmetic product safety report should also list the data that justify the minimum durability and, when applicable, the period-after-opening and why it was chosen [Decision 2013/674 | Section 3.2.3, p. 5].

(main model's reply)
  No, you don't need an expiry date. Regulation 1223/2009 doesn't require a date of minimum durability on cosmetic products that keep for more than 30 months [Reg 1223/2009 | Article 19 (part 2), p. 15]. Instead, the label must say how long the product stays safe to use after it has been opened [Reg 1223/2009 | Article 19 (part 2), p. 15]. You show this with the symbol in point 2 of Annex VII (the period-after-opening symbol), followed by the number of months and/or years [Reg 1223/2009 | Article 19 (part 3), p. 15]. You can only leave this out where the time after opening doesn't matter, such as single-use products, products that can't deteriorate, or products that don't open [Reg 1223/2009 | Article 19 (part 3), p. 15; Reg 1223/2009 | Preamble (part 17), p. 4-5]. Your safety report should also include the data that justify the product's shelf life and the period-after-opening you chose, with the reason for it [Decision 2013/674 | Section 3.2.3, p. 5].

Agent "Expiry date labelling question" finished - 7s
```

Observation: the main model did not forward the question as it was. It rewrote it into a longer prompt with hints ("date of minimum durability ... period-after-opening symbol") that came from the main model's own knowledge, not from the corpus. The subagent only has the `search` tool, but what it searches for can be steered by the prompt it receives.

**Why the subagent has only `search`.** `search` only reads, while `add_document` changes the index. If the subagent could change it without anyone seeing, it could add a wrong or unreliable document and contaminate all future answers. With only `search` it cannot break anything.

**When to use the subagent instead of asking Claude Code directly.** When I want an answer that comes only from the four documents and with a citation: the subagent can only answer with the chunks it finds and has to cite them, so I can check every fact. Claude Code, on the other hand, can rewrite the question with its own ideas and mix what it knows from memory with what the documents say.

## Adding a document

Data from the run of 25 Nov 2026, 18:48-18:50 (agent `gemini-3.5-flash-lite`; the index was backed up first and restored afterwards).

Unanswerable question used: q22, "Do I need FDA approval before selling my skincare line in the United States?"
Document added: corpus/fda_premarket_approval.txt (194 words; FDA page "Does the FDA approve cosmetics before they go on the market?", content current as of 06/16/2022, https://www.fda.gov/industry/fda-basics-industry/does-fda-approve-cosmetics-they-go-market), copied from the web page.

BEFORE
$ uv run python main.py ask "Do I need FDA approval before selling my skincare line in the United States?"
I don't know: the corpus does not cover this.
[gemini-3.5-flash-lite | 3.3s | 3968 in / 32 out tokens | tools: search({'query': 'FDA approval United States skincare line'}) | guardrails: none]

ADDING (approval step)
$ uv run python main.py ask "Please add the file corpus/fda_premarket_approval.txt to your search index."
The agent wants to run add_document({'path': 'corpus/fda_premarket_approval.txt'}). Allow? [y/N] y
[structure] 1 chunks, 0 already stored, 1 to embed
  [structure] stored 1/1
I don't know: the corpus does not cover this. (A draft answer had no citation of a passage I retrieved, so I am not giving it.)
[gemini-3.5-flash-lite | 31.9s | 2449 in / 45 out tokens | tools: add_document(...) | guardrails: uncited answer replaced by a refusal]

AFTER
$ uv run python main.py ask "Do I need FDA approval before selling my skincare line in the United States?"
Cosmetic products and ingredients are not subject to FDA premarket approval authority, with the exception of color additives (other than those intended for use as coal-tar hair dyes) [fda_premarket_approval | p. 1]. Instead, companies and individuals who market cosmetics have a legal responsibility for the safety of their products and ingredients, and the FDA's authority is post-market [fda_premarket_approval | p. 1].
[gemini-3.5-flash-lite | 14.93s | 4154 in / 110 out tokens | tools: search({'query': 'FDA approval United States skincare'}) | guardrails: none]

SAME FILE ADDED AGAIN
The agent wants to run add_document({'path': 'corpus/fda_premarket_approval.txt'}). Allow? [y/N] y
[structure] 1 chunks, 1 already stored, 0 to embed
I don't know: the corpus does not cover this. (A draft answer had no citation of a passage I retrieved, so I am not giving it.)
[gemini-3.5-flash-lite | 4.85s | 2441 in / 60 out tokens | tools: add_document(...) | guardrails: uncited answer replaced by a refusal]

Notes:
- Already-indexed file: nothing is embedded again (chunks are identified by content; "1 already stored, 0 to embed"), so no quota is used and no duplicates appear.
- The citation guardrail fired twice, on the replies right after add_document: the agent's draft had no [source | location] citation (it was not answering a content question), so the code replaced it with a refusal. That message is misleading right after a successful add (false positive). The draft text is not saved by main.py, so its content is not known.
- The index was restored from a backup afterwards so that q22 stays unanswerable in the committed index.

**Why "already indexed, nothing happens" (idempotent).** If the file is already there, nothing happens (`1 already stored, 0 to embed`) because then no chunks are duplicated and no quota is spent, and the command can be repeated safely. An error, on the other hand, would make it harder to repeat or automate.

**Why the agent asks for my approval before `add_document`.** Adding a document changes what the assistant takes as true. A wrong document would contaminate its answers, and that decision must be taken by a person, not by the agent.

## Harness and guardrails

**Instructions (`AGENTS.md`).** The first draft of the 8 rules in `AGENTS.md` was written by Claude (see "AI use"); I reviewed them and gave my own opinion below. The evaluation was run with these 8 rules as they are.

**The rule I think is most important: rule 2, "answer only with what the retrieved passages say".** The most expensive mistake is an invented "yes, you can sell", and the founder has no way to notice that it is false. If the assistant answers from memory, the citations and the "I don't know" stop being useful. In the unanswerable questions I graded (q21, q22, q23 and q24) the assistant refused instead of filling in with what it knew, and that is this rule working.

**Two changes I would make (not applied, so that the evaluation still matches the rules it was run with):**

- Rule 8: add "answer only what is asked". In several normal questions (q02, q05, q10, q20) the assistant added sentences or sources that the question did not ask for. In q10 and q20 the extra sentence was exactly the one that was doubtful for `supported`.
- Rule 2 or 3: add "do not change the strength of the sentence". In q05 and q31 the text said "should" and the assistant wrote "must", which turns a recommendation into an obligation.

**Guardrails in the code (`agent.py`).** There are three.

1. **Approval before `add_document`.** The agent asks me `[y/N]` before running it. Adding a document changes what the assistant takes as true; a wrong document would contaminate its answers, and that decision must be taken by a person, not by the agent.
2. **Limit of 6 tool calls per question.** It stops an agent that cannot find an answer from searching forever, spending the free quota and the person's time. In the runs I saw, the agent never needed more than two searches, so 6 leaves plenty of margin.
3. **Citation check.** After the agent answers, the code checks that the answer cites a passage that was really retrieved in that run; if not, it replaces the answer with "I don't know: the corpus does not cover this." I think this is better than trusting rule 3 of `AGENTS.md`, because that rule is only a request to the model, which can forget it or invent a citation, while the code checks every time without depending on the model obeying. But it only verifies that the citation matches a retrieved passage, not that what the answer says is true.

**A case where the citation check fired (25 Nov, after adding `fda_premarket_approval.txt`).** I asked the agent to add the file. It only called `add_document` and did not search, and the code replaced its draft with the refusal plus "(A draft answer had no citation of a passage I retrieved, so I am not giving it.)". My opinion: the guardrail did well, because the agent did not make any search, so no passage had been retrieved in that run and the code could not check any citation: it discarded an answer it could not verify. The side effect is a misleading message, since the file was in fact in the index (see Failures, point 3).

## Evaluation

Run: `uv run python main.py evaluate` (design `structure`; agent `gemini-3.5-flash-lite`, judge `gemini-3.5-flash-lite`, 32 questions, 32 answered without error, no tool error). The agent runs with approval for `add_document` denied.

**Three kinds of checks.**
1. Code checks (no model): whether the answer is a refusal, whether it cites a passage that was really retrieved, whether it cites the expected source/location, and whether the expected passage was among the retrieved ones (`expected_in_retrieved`).
2. LLM judge with my rubric (`eval/judge_rubric.md`): `correct` (key facts of the reference answer) and `supported` (every claim written in the retrieved passages). I need both because they check different things. The code checks objective things: whether the expected chunk was retrieved and whether the agent cited a chunk it had really retrieved. So it tells me where something failed (q17 and q18 came out with `retrieved: False`), but not whether what the answer says is true. The judge reads the meaning and scores whether the answer is correct and supported, but it can be wrong: in q17 it accepted as correct a refusal that the code did detect. With only one of the two checks there would be gaps.
3. My own grades: I graded 22 of the 32 answers by hand in `eval/human_labels.csv` before seeing the judge's verdicts.

**Results.**

| What is measured | Result |
|---|---|
| Answerable questions (26) | judge: 25 correct, 25 correct and supported, 0 unsupported, 0 without a valid citation |
| Wrong refusals (said "I don't know" although the reference gives an answer) | 2 (q17, q18) |
| Unanswerable questions (6) | 6 correct refusals, 0 answered anyway |
| Cause of failures (code) | 30 ok; 2 "wrong refusal: retrieval miss" |
| Judge against my grades (22 graded) | `correct`: 20 of 22 agree (90.9%); `supported`: 22 of 22 (100%) |
| Per question | mean 5.7 s (max 13.1 s); mean 5,375 input and 128 output tokens; 1.34 tool calls |

Note: the judge counts 25 of 26 as correct, but the code finds 2 wrong refusals. The difference is q17, where the judge accepted a refusal as correct although the reference answer gives an answer (see Failures). Counting both wrong refusals as wrong, the answerable questions are 24 of 26.

**Notes on the runs.** The first full run used agent `gemini-3.5-flash-lite` and judge `gemini-3.1-flash-lite`; some questions had 503 "high demand" retries and one judge call hung for more than 10 minutes because it had no timeout, so a 60 s timeout was added to `evaluate.py`. In the second judge run (with my rubric) `gemini-3.1-flash-lite` returned 503 on q01 and q02 after 6 retries (about 5 minutes per question), so the judge was switched to `gemini-3.5-flash-lite`, the same model as the agent (a limitation, see below). The reported results use `gemini-3.5-flash-lite` for the judge (the default of `evaluate.py`). The rubric was revised once after the first results: the judge accepted 2 refusals of answerable questions (q17, q18), so I added a rule (a refusal when the reference answer gives an answer is `correct` 0; whether a question is answerable is decided only by the reference answer). The verdicts of the first rubric are kept in `eval/judge_first_rubric.jsonl`; the full rubric is in `eval/judge_rubric.md`. In the end the judge was right on q18 and wrong on q17.

**Disagreements between the judge and me.** q17: I graded `correct` 0, the judge 1 (its reason says the reference answer "indicates the question is unanswerable", which is false: the judge misread). q18: I graded `correct` 1, the judge 0; the judge is right: it was a slip of mine (I marked a refusal as correct), left unchanged and disclosed here.

**What works well.** The 6 unanswerable questions were refused correctly and none was invented. In the 26 answerable questions there was no sentence unsupported by the passages and no invalid citation. It is also fast: 5.7 s on average and little more than one search per question.

**What works less well.** It said "I don't know" in 2 questions that did have an answer (q17 and q18). Both are `single` questions whose answer is in the same place (CPNP guide, p. 45): q17 ("where can I see the history of changes?", answer: the "Versions" tab) and q18 ("Can I get a PDF copy of my product's notification?", answer: a button on the product tabs). In both the agent answered "I don't know" and `expected_in_retrieved` is `False`: the chunk of p. 45 was not among those it retrieved.

**Why this does not contradict hit@5 = 1.00.** The hit@5 is measured by searching with the question exactly as it is in `questions.csv`, but the agent does not search with that sentence: it rewrites it with its own words (for example "FDA approval United States skincare"). With other words, the chunk of p. 45 can fall outside the first 5 although with the original question it did come in. They are two different tests: one measures the search engine and the other the complete agent.
**Judge and agent are the same model (`gemini-3.5-flash-lite`).** The judge can have the same faults as the agent and not see them, or be too soft with answers that look like its own. It shows in q17, where the judge accepted as correct a refusal that I marked as incorrect. That is why the judge has to be compared with my grades (20 of 22) and the 100% of `supported` should not be trusted without that comparison.
**How I graded and what could have influenced me.** I decided the 22 grades by myself, reading the retrieved passages. Before grading I had seen the judge's aggregate totals (for example that it gave most answers as correct). That did influence me: in the end it is being a bit biased, and the first reaction when grading is going to be a 1. However, I always made sure that it was not the bias that pushed me towards that classification. So the 90.9% agreement is not a fully independent comparison.

## Failures

**What the code found.** The mechanical cause classification over the 32 questions: 30 `ok` and 2 `wrong refusal: retrieval miss` (q17 and q18, both from CPNP guide p. 45; the agent answered "I don't know" because the chunk was not among those it retrieved, see Evaluation).

**Problems found (7).**

1. q17 and q18: the agent searches with its own words and does not retrieve the chunk (CPNP guide p. 45), even though with the question as written the chunk is found (hit@5 = 1.00). Two different tests: the search engine and the complete agent.
2. The judge misread q17 (it accepted a refusal as correct) and it is the same model as the agent.
3. After a successful `add_document`, the citation check can give a misleading "I don't know" (the file is in the index, but the agent had not searched yet).
4. The chunks still have noise: running headers and footers that survive the cleaning, and spaces inside words from the PDF extraction.
5. The main Claude Code model rewrites the question with its own ideas before handing it to the subagent.
6. The Gemini free-tier quota and the 503 "high demand" errors make the system unreliable (the judge had to change model, see Evaluation).
7. Style problems I saw while grading: extra sentences or sources that the question did not ask for (q02, q05, q10, q20; in q10 and q20 the extra sentence was the one that was doubtful for `supported`), and "should" changed into "must" (q05, q31).

**What I would fix first: number 7, the style.** A "don't know" too many (points 1 and 3) costs the founder time, but it is noticed and corrected. A "must" where the text says "should", or an extra sentence without support, looks like a good answer and can lead her to act on an obligation that does not exist.

**How I would fix it.** I would add to rule 8 of `AGENTS.md`: "answer only what is asked and keep the same strength as the text: if it says 'should', write 'should'". Then I would grade q05, q10, q20 and q31 again, which is where I saw it. (Not applied, so that the evaluation still matches the rules it was run with.)

## Decision

**Would I let the founder use it? Yes, with conditions.** I would let her use it because it refused the 6 unanswerable questions correctly, it had no answer unsupported by the passages, and it got 24 of 26 answerable questions right. But only as a help to find rules with their citation, not to decide whether she can start selling, because the test is small and the expensive error is a false "yes, you can sell".

**What it would be good for, and what not.** It would be good for finding where a rule is and what it says, for example who the responsible person is, what goes on the label or how to notify, always with the citation to check it. It would not be good for deciding whether she can sell, because the Annexes II and III (prohibited and restricted substances), the rules of other countries and taxes are missing. Also, 2 of the 26 answerable questions ended in "I don't know" because of search failures.

**Cost and latency per question.** Mean 5.7 s (max 13.1 s); about 5,375 input tokens and 128 output tokens; 1.34 tool calls. The free tier of Gemini has limits per minute and per day, and sometimes returns 503 errors.

**Safeguards I would add.**

- A fixed notice in every answer: "This does not cover Annexes II and III or other countries; check the citation in the original text before acting."
- Citations always visible, and keep the guardrail that replaces with "I don't know" any answer whose citation does not match a retrieved chunk.
- A final review: before launching the product, a cosmetics professional should review it, and the assistant should remind her of that.

## AI use

I used AI for a few things. Everything is listed here.

**Claude (Claude Sonnet 5.5 in a Claude Code session; Claude Opus 5.5 was the main model in the Claude Code demo):**

- It translated my answers from Spanish to English, so it was easier for me to explain all the technical parts.
-It helped me to fix errors according to the evaluation, where the model I was usuing could not proceed and was working too slow, therefore it suggested using another model to evaluate the questions and my agent.


