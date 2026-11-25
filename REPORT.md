# Assignment 3 Report

- **Name**: Sarah-Ghislaine Coste
- **Student ID**: 19863
- **Group**: BBADBA 5B

## Use case

The idea comes from my own experience with the French bac (end of highschool exams). In literature and philosophy we had to know the set books really well, quote them in our exams, and explain how two authors disagree. Since French texts would be harder for an English-speaking grader to check, I moved the idea to an English equivalent: a student revising for the A-level Politics exam (UK education system). In the "Core Political Ideas" part of the course, students have to know a list of "key thinkers", including Hobbes, Locke, Mill and Wollstonecraft.

The student asks things like "what did Locke say about property?", "give me a quote from Mill on free speech" or "how do Hobbes and Locke differ?", and then uses the answer in an essay or to to study for an oral/written exam.

Here, a wrong answer is much worse than "I don't know". Examiners know these books, so a made-up quote, a quote given to the wrong author, or an idea from a different book earn enalties or loses marks. And the student can't tell it's wrong, because it sounds right. "The course texts don't cover this", on the other hand, just sends them back to the book for a few minutes, which is much better than quoting wrong. So the whole system follows one rule: answer only from the texts, quote them exactly, say where the quote comes from, and otherwise say you don't know.

## Corpus

| Document | URL | Date | Licence | Words indexed |
|---|---|---|---|---|
| Hobbes, *Leviathan*, chapters XIII–XXI | https://standardebooks.org/ebooks/thomas-hobbes/leviathan | 1651 (accessed 23 Nov 2026) | Public domain; Standard Ebooks edition under CC0 1.0 | 28,684 |
| Locke, *Second Treatise of Government* | https://standardebooks.org/ebooks/john-locke/two-treatises-of-government | 1689 (accessed 23 Nov 2026) | Public domain; CC0 1.0 | 53,389 |
| Mill, *On Liberty* | https://standardebooks.org/ebooks/john-stuart-mill/on-liberty | 1859 (accessed 23 Nov 2026) | Public domain; CC0 1.0 | 46,565 |
| **Total (main index)** | | | | **128,638** |
| Wollstonecraft, *A Vindication of the Rights of Woman*, chapter XII "On National Education" (added later) | https://standardebooks.org/ebooks/mary-wollstonecraft/a-vindication-of-the-rights-of-woman | 1792 (accessed 23 Nov 2026) | Public domain; CC0 1.0 | 9,757 |

All four authors died a very long time ago (between 1679 and 1873), so their books are public domain everywhere, and there's no personal data in them. I picked books written in English on purpose, because a translation of Rousseau or Kant can still be under copyright through the translator. I left out the other thinkers on the syllabus for A-level exams (Rawls, Friedan, Rand and Nozick are still under copyright), and Burke and Oakeshott would have made the corpus too big for the free embedding limit. For the same reason I only kept the Leviathan chapters about the state of nature, the laws of nature and the commonwealth.

## Ingestion

`index.py` (run by `main.py index`) downloads each book from Standard Ebooks, pulls out the text, cleans it, cuts it into chunks and embeds them.

I only keep the actual chapters, so things like the title page, introductions, endnotes and colophon are skipped. The cleaning removes footnote numbers that were stuck to words (Locke's "law²" came out as "law2") and some invisible formatting characters. There were hundreds of those in the files.

One bug I had to fix: my first version added a space around every word in italics, so you'd get "*civitas* ." instead of "*civitas*.". That sounds tiny, but it would have broken the exact-quote check, which is the most important check for my use case. I noticed it while checking my test questions against the text. After the fix, only the 57 chunks that had changed needed to be embedded again, because each chunk's id is based on its text.

Chunks are whole paragraphs grouped up to about 200 words (300 max), and they never cross into the next chapter. If a paragraph is longer than 300 words, it's split at the end of a sentence. That gives 715 chunks (about 177 words each). Each chunk knows its book, its chapter and its paragraph number in that chapter, which gives citations like "Locke, Second Treatise, Chapter II, paragraph 5" (the system writes "paragraph" with the ¶ sign, which is why you'll see it in the copied search results and transcript below). I would have liked to use Locke's usual section numbers, but this edition doesn't have them, and its paragraphs don't line up with them, so I used chapter + paragraph instead of making numbers up.

The chunks are embedded with `gemini-embedding-2`, with the author and chapter added in front of the text, and saved in ChromaDB (`index/chroma`, 11.8 MB) as soon as each batch comes back. Running the index again only embeds chunks that don't have a vector yet. Small surprise along the way: if you send this model a plain list of texts, it gives you back one embedding for the whole list, so each text has to be sent separately.

## Test set

`eval/questions.csv` has 35 questions: 20 single, 8 multi and 7 unanswerable. They were drafted with AI help from the texts, and I reviewed and approved them.

The single questions follow the ideas the course lists for each thinker (Mill's harm principle, Locke's limited government, Hobbes on human nature, etc.) plus other well-known passages. The multi questions compare two thinkers (for example on the state of nature or on when people can stop obeying) or link two chapters of the same book.

The unanswerable questions stay close to the topic on purpose. Three are about course thinkers who aren't in the corpus (Rawls, Burke, Nozick), and one is about Wollstonecraft, which only becomes answerable after I add her chapter. The last three are traps, because the model probably "knows" the answer from elsewhere: Hobbes on miracles (a Leviathan chapter I didn't include), Locke's "blank slate" (from a different book) and Mill's higher and lower pleasures (also a different book). A script checked that every expected location exists and every quote in my reference answers is really in the text.

Two examples:

| id | question | kind | expected | reference |
|---|---|---|---|---|
| q03 | According to Hobbes, what is the life of man like when there is no common power to keep everyone in awe? | single | Hobbes, Leviathan, Chapter XIII, paragraph 9 | A war of every man against every man… the life of man "solitary, poor, nasty, brutish, and short". |
| q21 | Hobbes and Locke both describe a 'state of nature'. How do their descriptions differ? | multi | Hobbes XIII paragraph 9; Locke II paragraph 5 | Hobbes: a war of all against all. Locke: a state of liberty but not of licence, governed by the law of nature. |

## Retrieval

I tested retrieval on the 28 answerable questions. A question is a hit if the right paragraph shows up in the top k results (for multi questions, both paragraphs have to show up). All the designs reuse the same saved vectors, so trying them didn't cost any extra embedding of the corpus.

| Design | hit@1 | hit@3 | hit@5 | multi: both @5 | multi: at least one @5 | words added @3 / @5 |
|---|---|---|---|---|---|---|
| vector (cosine) | 0.61 | 0.75 | 0.75 | 0.13 | 0.75 | 558 / 916 |
| hybrid (BM25 + vector) | 0.46 | 0.61 | 0.64 | 0.13 | 0.75 | 559 / 961 |
| vector + author filter | 0.61 | 0.75 | 0.75 | 0.13 | 0.75 | 558 / 916 |
| hybrid + author filter | 0.46 | 0.61 | 0.68 | 0.25 | 0.88 | 570 / 950 |
| **per-author vector** | **0.61** | **0.79** | **0.82** | **0.38** | **0.88** | 558 / 927 |

(These are from before I added Wollstonecraft. After adding her, the vector and per-author numbers stay exactly the same. The hybrid ones move a little, e.g. hybrid + author filter goes to 0.64 at k = 5, because keyword scores depend on every document in the index. The current numbers are in `eval/retrieval_summary.csv`.)

For single questions, plain vector search is basically perfect (0.85 at k = 1, 1.00 at k = 3). I thought hybrid search would help with exact phrases, but it actually did worse. Keyword search loves words like "people", "life" and "power", and those are everywhere in 17th-century writing. The author filter didn't change anything, because vector search was already finding the right author.

The weak spot was the comparison questions. If you search "Hobbes and Locke on the state of nature", the results fill up with Locke (he uses that phrase constantly) and Hobbes gets pushed out. So after seeing these numbers I added a per-author design: if the question names two authors, it searches each one separately and mixes their best results. It's a general rule, not something tuned to specific questions, but I did add it after seeing the test results.

I went with per-author search, k = 5. It's the best on everything at no extra cost, and k = 5 instead of 3 adds about 370 words to the prompt but finds the second passage more often (0.25 compared to 0.38).

## Tools and subagent

`server.py` is an MCP server. It loads the saved index when it starts and never re-embeds the corpus. It has two tools:

- **`search(query)`** returns the 5 best passages, each with its citation. Its description tells the model what's in the corpus, to always search before answering, to put the author's name in the query, and to search each author separately when comparing. It also says that a similarity below about 0.65 usually means the corpus doesn't cover the question.
- **`add_document(path)`** adds a new document. It reuses the functions from `index.py` instead of rewriting them, and then refreshes the search so the new text is findable right away. It only accepts files inside `corpus/`. I tried `/etc/passwd`, my assignment 2 `.env` file and `main.py`, and it refused all three.

Here's one search result (from `check.py`):

```
[1] Hobbes, Leviathan (1651) | Chapter XIII: Of the Natural Condition of Mankind as Concerning Their Felicity and Misery, ¶1 (similarity 0.84)
Nature hath made men so equal, in the faculties of the body and mind; as that though there be found one man sometimes manifestly stronger in body, or of quicker mind than another, yet when all is reckoned together, the difference between man and man, is not so considerable, …
```

The subagent (`.claude/agents/corpus-researcher.md`) can only use `search`. Its instructions: always search first, search each author separately when comparing (4 searches max), answer only from what comes back, cite every claim, copy quotes exactly, say "The course texts don't cover this" otherwise, and keep it under 150 words.

I used it from the Claude Code desktop app. Here's a shortened transcript (the full one is in `eval/subagent_transcript.md`):

> **User:** Use the corpus-researcher subagent to answer: How do Hobbes and Locke differ on the state of nature?
>
> **Claude Code → corpus-researcher:** "How do Hobbes and Locke differ on the state of nature? Compare them on: what the state of nature is like (war vs. liberty/peace), whether there is a law of nature binding people in it and what it requires, natural rights (Hobbes's right to all things vs. Locke's life, liberty, estate), property, who enforces the law of nature (Locke's executive power), and why people leave it for civil society. Use only the course texts…"
>
> **corpus-researcher → search** ×4: "Hobbes state of nature war of every man against every man, right of nature to all things, no property no mine and thine" (top: Hobbes XIII ¶13, XIV ¶4, XIII ¶9); "Hobbes law of nature seek peace, precept of reason, why men enter commonwealth for security"; "Locke state of nature perfect freedom and equality, law of nature reason, life health liberty possessions, executive power to punish" (top: Locke II ¶1–2, VII ¶11); "Locke property labour, why men quit state of nature and join civil society to preserve property, inconveniences".
>
> **corpus-researcher:** Hobbes calls it war: "a war... of every man, against every man", and life there is "solitary, poor, nasty, brutish, and short" (XIII ¶8–9). Locke calls it "a state of perfect freedom" and "equality" (II ¶1–2), "a state of liberty, yet... not a state of licence" (II ¶5). [… law of nature, rights, property, enforcement, why people leave, each with quotes and citations …]
>
> **Claude Code (to the user):** a comparison table built from those quotes, then: "Paragraph numbers: … Locke is normally cited by section number (§) … From memory rather than the corpus, the usual equivalents are roughly: … §4, §6, §27, §87, §124." and "the subagent didn't find Locke's phrase 'the executive power of the law of nature' … it isn't confirmed from the corpus here."

What I took from this:

1. The subagent did its job. It searched twice per author, and all 18 of its quotes are really in the text at the paragraphs it cited (I checked this with code).
2. But only the subagent sticks to the books. The main assistant added some of its own knowledge when it passed the question on (like "Locke's executive power"), and later it added Locke's section numbers from memory. It did say they were from memory, but nobody checked them against the text.
3. One miss. The subagent said it couldn't find the phrase "executive power of the law of nature", but it is in the corpus (Locke II paragraph 12, VI paragraph 23, VII paragraph 13). The search just didn't bring it up. At least it said "not found" instead of pretending.

## Adding a document

**Duplicates.** Every chunk has an id made from its document, chapter, paragraphs and a hash of its text. So if you add a document that's already in the index, nothing gets embedded and nothing is doubled. When I tried adding Mill again, the tool said: "Already indexed: Mill, On Liberty (1859) (258 chunks). Nothing was embedded." If a file has changed, only the new or changed chunks are embedded and the old ones are deleted. I chose this because embeddings cost quota, and duplicate chunks would push other passages out of the top 5.

**Before and after.** For this test I used q30, one of my unanswerable questions: *"According to Wollstonecraft, should boys and girls be educated together in day schools?"*

- **Before:** the agent searched once, found nothing from Wollstonecraft and answered: "The course texts don't cover this. The corpus contains only Hobbes (*Leviathan* XIII–XXI), Locke (*Second Treatise of Government*), and Mill (*On Liberty*)." That's the right answer at that point.
- **Adding it:** I asked the agent to add `corpus/wollstonecraft_ch12.xhtml` (her chapter "On national education", 9,757 words). It stopped and asked me first (`Allow? [y/N]`). I typed y, and it embedded 54 chunks, so the index went from 715 to 769 chunks.
- **After:** same question, new answer: "Yes, according to Wollstonecraft, boys and girls should be educated together in elementary day schools established by government", with a quote ("absolutely free and open to all classes") and citations to Chapter XII, paragraphs 43 and 46–47. All five passages it retrieved were from her chapter, and the quote check passed.

So the agent goes from "I don't know" to a cited answer, without re-embedding the rest of the corpus. One small thing: for this answer flash-lite was busy, so the backup model (`gemini-3.6-flash`) answered. The output is saved in `eval/.q30_after.log`. The 35 evaluation answers are from before Wollstonecraft was added.

## Harness and guardrails

My own agent, `agent.py`, is what `main.py ask` runs. It's built with LangChain's `create_agent` on `gemini-3.5-flash-lite` (with `gemini-3.5-flash` as a backup). It gets the tools from `server.py` and uses `AGENTS.md` as its instructions.

Why flash-lite?
I started with `gemini-3.5-flash`, with flash-lite as a backup. But in my first evaluation run, 23 of the 35 answers came from the backup. It turned out the free tier only allows **20 requests a day** for `gemini-3.5-flash`, and one answer takes 2 or 3 requests, so the main model ran out after about 8 questions. So I switched everything to flash-lite and ran the evaluation again with that model only. That way all the answers come from the same model, and anyone running `check.py` with a free key gets the model I tested. The downside is that flash-lite is smaller, so it might be a bit weaker. The first (mixed) run is kept in `eval/answers_run1_mixed_models.jsonl`.

`AGENTS.md` has seven rules, each with a reason:
1. always search first
2. only use what the search returned (no facts, dates or section numbers from memory)
3. cite everything
4. quote exactly
5. say "The course texts don't cover this" when they don't
6. search each thinker separately when comparing
7. only add documents when the user asks. 
Rule 2 is basically there because of what the main assistant did in the subagent test.

Approval step
Before `add_document` runs, the agent stops and asks in the terminal "The agent wants to run add_document(...). Allow? [y/N]". If nobody's there to answer (like during the evaluation or `check.py`), it's refused. I tested it by asking the agent to add the Wollstonecraft chapter: it printed `[guardrail] approval: add_document refused` and told me the document wasn't added.

Limits
Max 6 tool calls and 8 model calls per question. Google also kept answering "503 high demand" while I was working, so the agent waits (5, 10, then 20 seconds) and tries again before switching to the backup. LangChain doesn't retry that error by default, so I had to add my own rule. My first version also did it in the wrong order (backup first, retries after).

My extra guardrail: a quote and citation check.
This comes straight from my use case. After the agent answers, code checks that every quote (3+ words) is really in the passages the search returned, word for word (ignoring quote-mark style, capitals and punctuation), and that every "Chapter X, paragraph n" citation matches one of those passages. If something's wrong, the agent is told exactly what and gets one chance to fix it (it can search again). If it's still wrong, the answer is shown with a warning: "⚠ Could not verify in the course texts". In the final evaluation run it fired 3 times out of 35, and all three were real mistakes:

- q05: the agent quoted Hobbes as "where a covenant is made, then to break it is unjust", but the text says "when a covenant is made".
- q14: it dropped a word from Locke: "still must be with his own consent" instead of "still it must be with his own consent".
- q26: it quoted "the original compact", which isn't anywhere in the corpus. It just made it up.

Each time, the agent fixed its answer after the warning, so in the end all 35 answers passed (106 quotes, all word for word). These are exactly the kind of small misquotes a student wouldn't notice but an examiner would.

The guardrail also had some false alarms while I was building it. It got confused by commas in chapter titles (like "Of the Causes, Generation, and Definition of a Commonwealth"), by the scholarly "[t]he" convention (a bracketed letter meaning the capital was changed), and by answers that mixed curly and straight quote marks. In my first run, 5 of its 6 warnings were false alarms like these, which meant 5 unnecessary rewrites. I fixed all three problems before the final run.

## Evaluation

`evaluate.py` runs all 35 questions through the agent, checks every answer with code, then has an LLM judge grade it. The results are in `eval/results.csv` and `eval/summary.md`.

**Code checks** (these are exact, no AI involved):

| Check | Result |
|---|---|
| Unanswerable questions refused | 7 / 7 |
| Answerable questions wrongly refused | 0 / 28 |
| Answers where every quote is word for word in the passages | 35 / 35 (106 quotes) |
| Answers where every citation points to a retrieved passage | 35 / 35 |
| Expected passage(s) retrieved by the agent | 24 / 28 (at least one: 27 / 28) |
| Guardrail asked for a rewrite | 3 (q05, q14, q26, all fixed) |

**LLM judge.** The judge gets the question, my reference answer, the retrieved passages and the agent's answer, and gives two scores: correct (does it say the main point of the reference, or refuse properly when it should?) and supported (is every claim in the retrieved passages?). The judge was supposed to be a stronger model than the agent, so the agent wouldn't be grading itself. That only half worked. `gemini-3-flash-preview` judged q01–q21 and then hit its free limit of 20 a day. Then `gemini-3.5-flash` was overloaded ("503 high demand") for hours on the 25th, so with the deadline coming I let flash-lite, the agent's own model, judge q22–q35. Each verdict records which model gave it (`eval/judge.jsonl`).

The rubric (in `evaluate.py`), shortened:

> correct: for an answerable question, 1 if the answer states the main point of the reference answer (wording may differ, extra true detail is fine) and contradicts nothing in it, 0 if it misses the main point, gets it wrong or refuses. For an unanswerable question, 1 if it says the course texts don't cover it and doesn't go on to answer from general knowledge.
>
> supported: 1 if every factual claim and quotation can be found in the retrieved passages, 0 if any claim, name, date, section number or quotation isn't in them, even if it is true.

The judge gave 35 / 35 correct and 35 / 35 supported.

**Me vs the judge.** I graded 26 answers by hand without looking at the judge first (`eval/human_labels.csv`).

| | Agree | Cohen's kappa |
|---|---|---|
| correct | 25 / 26 (96%) | 0.0 |
| supported | 22 / 26 (85%) | 0.0 |

The agreement looks high, but the kappa of 0 shows what's really going on: the judge never gave a single 0, so it agrees with me only when the answer is fine anyway. On all 5 answers I marked down, it disagreed with me:

- q28 (I said wrong): the question links Locke's origin of property (labour) to the limits on the legislative. The answer never mentions labour, because Chapter V wasn't retrieved. The judge said it "accurately explains" the connection.
- q25 (I said unsupported): it says Hobbes's liberty is bounded entirely by the sovereign, but the passage it retrieved (Chapter XXI, paragraph 10) says some commands can be refused.
- q29, q32, q33 (I said unsupported): each one refused correctly, but then added a fact from memory: Rawls "is a later thinker", the blank slate is in Locke's Essay, and higher and lower pleasures are in Utilitarianism (1861). The rubric says a claim not in the passages is unsupported "even if it is true". The judge said q32 had no "unverified outside information", which is just wrong.

All 5 disagreements were judged by flash-lite, so part of this may be the model being too kind to its own answers. But the pattern is clear: the judge can't be trusted alone. It misses exactly the subtle problems that matter for this use case.

Cost per question (all on the free tier, so it cost me nothing):

- tokens: mean 4,883 (4,680 in, 203 out), max 17,025 (q26, with the rewrite)
- time: median 7.9 seconds, mean 16.5, max 113 (waiting out "busy" errors)
- model calls: mean 2.2, searches: mean 1.3
- judge: about 2,100 tokens per answer

Most of the input tokens are the five retrieved passages plus `AGENTS.md`, so k = 5 is the main cost.

## Failures

I put each failure into one of the five categories from the brief (based on my grading, the code checks and the judge):

| Category | Count | Questions | What happened |
|---|---|---|---|
| Unsupported claim | 3 | q29, q32, q33 | It said "the course texts don't cover this" correctly, then added a fact from its own knowledge (Rawls "is a later thinker", Locke's Essay, Mill's Utilitarianism). Breaks rule 2 of `AGENTS.md`. |
| Retrieval miss | 2 | q25, q28 | Comparison questions where one of the two key passages didn't come back. q28 never got Locke's Chapter V on labour, so half the answer is missing. q25 never got Hobbes's Chapter XXI, paragraph 18, and overstated the passage it did get. |
| Wrong answer from the right passage | 0 | | |
| Wrong refusal | 0 | | |
| Bad test question | 0 | | |

So 5 of the 35 answers failed, 30 passed.

Two things that weren't failures but are worth saying:
- The guardrail caught three misquotes (q05, q14, q26: a wrong word, a missing word and an invented phrase). They were fixed in the rewrite, so the student never saw them.
- In q08 and q27 the expected passage wasn't retrieved, but another passage said the same thing, so the answers were still right.

What these tell me:

1. The quote guardrail works. Misquoting is the worst error for this use case, and it's the one that's under control: 106 quotes, all word for word.
2. Comparison questions are the weak spot. Both retrieval misses are multi questions. Even with per-author search, only about 0.38 of them get both passages in the top 5.
3. Refusals leak outside knowledge. The facts it added were true, but rule 5 is supposed to send the student back to the book, not give them unchecked facts. The guardrail doesn't catch this, because there are no quotes to check.

What I'd fix first: retrieval for comparison questions, because it causes wrong answers, which is worse than an extra (true) fact in a refusal.

## Decision

Would I let students use it?
Yes, but only for one-thinker questions and finding quotes, not yet for comparisons.

- For single-thinker questions the judge marked all 20 correct, and so did I for the 11 I graded. Every quote is checked word for word, and every answer has a citation the student can look up. That's good enough for revision, which is what it's for.
- For comparison questions, 2 of the 8 had real problems (q25, q28). A student could easily put a half-answer into an essay without noticing.

What I'd fix next:

1. Retrieve more passages for comparison questions (e.g. 5 per author instead of 5 in total), or let the agent search again when one author only has one passage.
2. Extend the guardrail to refusals: if the answer says "the texts don't cover this", flag any book titles, names or dates that aren't in the passages.
3. Don't trust the LLM judge on its own. In my evaluation it never gave a 0, so it would have hidden all the problems I found by hand. A real version needs a stronger judge that isn't the agent's own model, plus human spot checks.

Safeguards if students use it now: the quote check stays on (it's the main reason I trust the quotes), every answer keeps its citations so the student can check the book, and comparison answers should come with a note telling the student to check both thinkers in the text before using them in an essay.

Cost and latency: about 4,900 tokens and 8 seconds (median) per question, free on the Gemini free tier (details under Evaluation).

## AI use

I used Claude (Claude Code, by Anthropic) for this assignment, kind of like a tutor. It explained some steps and suggested options, however I made the decisions: the use case, the books, the chunking budget, the search design, the extra guardrail and the test questions. It was also used in this report to bring cohrerency and correct synthax and grammar mistakes. Gemini is used inside the system itself, for the embeddings, the agent and the judge.
