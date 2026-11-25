# Said Who? An attribution checker for teachers

Armand Hubler · Student ID 19095 · BBADBA 5A · Assignment 3

## Use case

"Adam Smith said greed is good." Smith never wrote that. The line comes from the 1987 film Wall Street. Essays are full of quotes like this, and a teacher marking them often has no time to open the book and check.

Said Who? does that check. The teacher types a claim or a question about a thinker, and the tool returns one of three verdicts: **said it**, **said something different** or **not in these texts**. Each verdict comes with a short quote and a citation, so the teacher can find the paragraph in seconds.

A normal chatbot is the wrong tool here. A language model learned from the same internet where these false quotes spread, so from memory it tends to repeat them. It also cannot show where its answer comes from. With retrieval (RAG), every verdict points to a real passage, and a new book only needs to be added to the index, with no retraining.

Mistakes do not all cost the same:

| If the tool says… | …and it is wrong, then | How bad |
| :---- | :---- | :---- |
| said it | a false quote passes as true | bad |
| said something different | a student loses marks for a correct claim | worst |
| not in these texts | the teacher looks it up by hand (5–10 min) | small |

This shaped the whole design. When the passages are unclear, the tool should say "not in these texts". The teacher always makes the final call on the mark.

## Corpus

I picked five classic texts that students quote a lot and often get wrong. They also argue with each other about trade, property and the state, which gives good two-thinker questions. In one line each: Mill asks when society may limit a person's freedom; Marx and Engels see history as a fight between classes; Paine says everyone is owed money because land became private property; Bastiat says every policy has effects you see and effects you don't; Smith explains why people trade.

| Text | Source id | Published | Link | Words |
| :---- | :---- | :---- | :---- | ----: |
| Mill, On Liberty, ch. I–II | mill-on-liberty | 1859 | [Gutenberg 34901](https://www.gutenberg.org/ebooks/34901) | 22,292 |
| Marx & Engels, Manifesto of the Communist Party | marx-engels-manifesto | 1848 (Eng. 1888) | [Gutenberg 61](https://www.gutenberg.org/ebooks/61) | 11,421 |
| Paine, Agrarian Justice | paine-agrarian-justice | 1797 (ed. 1895) | [Gutenberg 31271](https://www.gutenberg.org/ebooks/31271) | 7,430 |
| Bastiat, That Which Is Seen, and That Which Is Not Seen | bastiat-seen-unseen | 1850 (Eng. 1874) | [Gutenberg 15962](https://www.gutenberg.org/ebooks/15962) | 17,466 |
| Smith, Wealth of Nations, Book I ch. II | smith-wealth-b1c2 | 1776 | [Gutenberg 3300](https://www.gutenberg.org/ebooks/3300) | 1,574 |
| Smith, Wealth of Nations, Book IV ch. II | smith-wealth-b4c2 | 1776 | [Gutenberg 3300](https://www.gutenberg.org/ebooks/3300) | 8,334 |
| **In the index** | | | | **68,517** |
| *Kept out for the add_document test:* Bastiat, Government | bastiat-government | 1848 (Eng. 1874) | [Gutenberg 15962](https://www.gutenberg.org/ebooks/15962) | 4,059 |

I used only the chapters students actually quote, such as Smith's butcher and baker and the "invisible hand". Whole books would add noise to search and cost more embeddings. Since I am not a philosopher or an economist, an LLM helped me choose these chapters. All editions are from before 1929 and every author, translator and editor died long ago, so all texts are public domain. I removed the Project Gutenberg licence text. There is no personal data.

## Ingestion

index.py downloads each book from Project Gutenberg and keeps only the part between a start line (for example "CHAPTER I.") and an end line. This also drops the editors' introductions. That matters for this use case: an editor's sentence stored as Mill's would be a misattribution made by the tool itself. The text is then split into numbered paragraphs (¶1, ¶2…) with their section names. Footnotes and formatting marks are removed.

Two bugs only showed up when I read the cleaned text:

- Mill's start line also appeared in the table of contents, so the first chunks were a list of chapter titles. Fix: use the last match, not the first.
- The Manifesto's last line, "WORKING MEN OF ALL COUNTRIES, UNITE!", is in capitals, so the code took it for a section title. Fix: a line ending in "!" is normal text.

I built two chunking designs to compare:

| Design | How chunks are cut | Chunks |
| :---- | :---- | ----: |
| paragraph | one paragraph per chunk; under 80 words joins the next, over 300 is split | 424 |
| fixed | 150-word windows that never cross a section title | 457 |

Each chunk keeps its author, work, year, section and paragraph numbers, plus a citation built once at indexing time, so every answer cites a passage in the same form. The chunk id shows where it starts: mill-on-liberty-p9-w3450 means On Liberty, paragraph 9, word 3,450. A teacher with a paper copy can go straight there. The chunks are embedded with gemini-embedding-2 (768 dimensions) and stored in ChromaDB. Vectors are written to disk every 20 chunks, so hitting the free tier's daily limit loses almost nothing.

## Test set

There are 36 questions. Each has the paragraph that answers it and a short reference answer, and all were fixed before I tuned anything. An LLM helped me find key paragraphs and suggested themes per author; I wrote the questions around those themes and checked every question, paragraph and answer myself.

| Kind | Count | Meaning |
| :---- | ----: | :---- |
| single | 20 | one passage answers it |
| multi | 8 | two thinkers, one passage each |
| unanswerable | 8 | near the corpus, but no passage answers it |

Many questions are traps, written the way a student gets it wrong. "Did Bastiat curse machines?" is one: Bastiat quotes people who curse machines, then replies "to curse machines is to curse the spirit of humanity!" A fast reader could take the first part as his view, so the right verdict is said something different.

Refusing is the cheap mistake, but only if the tool refuses in the right places. So the unanswerable questions sit close to the corpus: another chapter of the same book (Smith's pin factory), the Government essay I kept out, thinkers who are not in the corpus (Keynes, Hayek), a modern policy ("Would Paine support Finland's basic income experiment?"), and a request for an opinion ("Who was right about free trade, Smith or Marx?").

The hardest multi question is q25: **Where do Mill and Marx & Engels each say a society's dominant moral ideas come from?** The two are usually seen as opposites, yet both tie the dominant morality to the ruling class.

One of my own questions turned out weak. q26, "How do Bastiat and Paine each look at money that the state collects from citizens?", is too open for a said it / said something different verdict, and it comes back in the failures. With only 36 questions, every number below is rough. A tool teachers depend on would need hundreds of real claims taken from student essays.

## Retrieval

For the 28 answerable questions I measured hit@k: is the expected paragraph among the top k results? For multi questions both paragraphs must be there. I tested both chunk designs with two search methods. Dense search ranks chunks by embedding similarity, so it matches meaning. Hybrid search also runs BM25 keyword search and merges the two rankings with reciprocal rank fusion, which helps when a question has exact words like "fifteen pounds" (Paine). Hybrid reuses the same vectors, so it cost no extra embeddings.

| Chunking | Search | hit@1 | hit@3 | hit@5 | Both thinkers in top 5 | Prompt words added | Best similarity, answerable / unanswerable |
| :---- | :---- | ----: | ----: | ----: | ----: | ----: | :---- |
| paragraph | dense | 50% | 71% | 75% | 38% | 776 | 0.78 / 0.69 |
| paragraph | hybrid | 46% | 68% | 75% | 25% | 831 | 0.77 / 0.67 |
| fixed | dense | 54% | 64% | 79% | 25% | 727 | 0.76 / 0.67 |
| **fixed** | **hybrid** | 46% | **75%** | **82%** | **38%** | 748 | 0.74 / 0.65 |

One question is worth 3.6 points here, so small gaps mean little. To see how much, I resampled the 28 questions 1,000 times with replacement (bootstrap) and used the same samples for every design. Fixed + hybrid gets 82% at hit@5, with a 95% interval of 68% to 96%. Its lead over paragraph + dense is +7 points, but that interval runs from −7 to +21, so the lead could be chance. In short, the four designs are close.

I picked **fixed chunks + hybrid search, k = 5**. It is best at hit@3 and hit@5, ties for best on two-thinker questions, and sends less text than both paragraph designs. Its weak hit@1 is not a problem, because the agent reads all five results.

The last column ruled out an easy shortcut. The best similarity is only a bit higher for answerable questions (0.74) than for unanswerable ones (0.65). That is too close for a rule like "below 0.7, refuse". So the model decides when to refuse after reading the passages, and the rules and code checks back it up.

## Tools and subagent

server.py is an MCP server, and it is the model's only way into the index. The model cannot read my code; all it knows about each tool is its description. So the search description has to tell it what is in the corpus.

| Tool | What its description tells the model |
| :---- | :---- |
| search(query) | It searches public-domain political economy and philosophy texts, including documents added later. For two thinkers, search once for each. It returns the 5 best passages, each with chunk_id, cite_as, similarity and exact text. If none really answers, the corpus does not cover it. |
| add_document(path) | It cleans, chunks and embeds a .txt file the same way as the rest. If that exact text is already indexed, nothing happens. If the name matches but the text is different, it counts as a new edition and replaces the old chunks. |

Example: searching "Adam Smith greed self-interest butcher" returns smith-wealth-b1c2-p2-w450 first (Adam Smith, The Wealth of Nations (1776), Book I, Chapter II, ¶2, similarity 0.745), with "It is not from the benevolence of the butcher, the brewer, or the baker that we expect our dinner, but from their regard to their own interest." The fifth result has a higher similarity (0.683) than the third and fourth. That is hybrid ranking: keywords move results, not only similarity.

The subagent, .claude/agents/corpus-researcher.md, has access to search and nothing else. Its instructions: one search per thinker, nothing from memory, the same verdict card as the harness, "not in these texts" when no passage fits, and never say who is right. I ran it in Claude Code on a claim from a made-up essay. It took about 18 seconds and 11,000 tokens. Transcript from the session log, passages shortened:

```text
> corpus-researcher: A student's essay says: "Bastiat said machines are bad for
  workers because they throw people out of work." Check this attribution.

  search(query="Bastiat machines throw workers out of work")
  → 5 results:
    bastiat-seen-unseen-p129-w0    VIII.--Machinery, ¶129-133          0.800
        "\"A curse on machines! Every year, their increasing power devotes millions
        of workmen to pauperism, by depriving them of work, and therefore of wages
        and bread. A curse on machines!\" This is the cry which is raised by vulgar
        prejudice, and echoed in the journals. But to curse machines is to curse
        the spirit of humanity! ..."
    bastiat-seen-unseen-p135-w300  VIII.--Machinery, ¶135-138          0.758
    bastiat-seen-unseen-p74-w300   V.--Public Works, ¶74-77            0.758
    bastiat-seen-unseen-p29-w750   II.--The Disbanding of Troops, ¶29-30   0.719
    bastiat-seen-unseen-p240-w150  XII.--He Who Has a Right to Work Has a
                                   Right to Profit, ¶240-244           0.718
```

Its reply:

**Verdict:** said something different  
**Answer:** Bastiat quotes the view that machines put workers out of work, but only so he can reject it.  
**Source:** Frédéric Bastiat, That Which Is Seen, and That Which Is Not Seen (1850), VIII.--Machinery, ¶129-133 [bastiat-seen-unseen-p129-w0]  
**Quote:** "This is the cry which is raised by vulgar prejudice... But to curse machines is to curse the spirit of humanity!" [bastiat-seen-unseen-p129-w0]  
**Why this verdict:** The essay treats a view Bastiat calls "vulgar prejudice" as his own, when the passage argues against it.

Only one thinker is named, so one search was enough, and it used no other tool. Both parts of the quote appear word for word in the chunk, it stays under 25 words, and the reply adds nothing about Bastiat that the passage does not say.

## Adding a document

add_document first looks at what is already stored under the file's name. Same text: skip it and spend no quota. Different text: delete the old chunks and index the new ones, so search never mixes two editions. Two editions of one paragraph would fill two of the five result slots and could push the second thinker out of a comparison question.

The test was q31: **Who said that government is the great fiction through which everybody tries to live at the expense of everybody else?** The line is from Bastiat's Government, the essay I kept out. Before adding it, the agent said "not in these texts", which was correct at that point. Then I asked it to add the file, and the harness stopped for my approval:

Allow add_document({'path': 'corpus/bastiat-government.txt'})? [y/N] y  
add_document: added bastiat-government, 27 chunks embedded

To my surprise, the agent still refused, although search now put the right passage at the top. The reason: AGENTS.md, the search description and the refusal text all listed the original works, and Government was not on the list. The model believed the list over the passage. I changed all three to say that added documents count. After that, I asked twice and got the same answer both times:

**Verdict:** said it  
**Source:** Frédéric Bastiat, Government (1848), Full essay, ¶44-46 [bastiat-government-p44-w1350]  
**Quote:** "Government is the great fiction, through which everybody endeavours to live at the expense of everybody else." [bastiat-government-p44-w1350]

So adding a document means more than updating the index: every piece of text that tells the model what the corpus holds must change with it. The full log is in eval/add_document_demo.md.

I then deleted the 27 Government chunks again. The committed index is the one the evaluation used (457 fixed chunks), and q31 stays unanswerable on a rerun. To repeat the test, run main.py index (it saves corpus/bastiat-government.txt but does not index it) and ask the agent to add that file, which costs 27 embeddings.

## Harness and guardrails

agent.py is a LangChain agent. Its system prompt is AGENTS.md, and it gets its tools from the MCP server. AGENTS.md has nine rules, and each rule says why it exists, so the model can handle cases I did not foresee. The key ones: search before answering, cite every claim by chunk_id, quote at most 25 words exactly (a paraphrase in quotation marks is itself a misattribution), and say "not in these texts" when unsure. Two more keep it neutral: never say which thinker is right, and give both thinkers the same format and space.

add_document only runs if I type "y" at the prompt; any other input blocks it. In the evaluation nobody types, so it is always blocked, and the corpus cannot change in the middle of a test run. Each question gets at most 6 model calls, which stops loops.

The prompt alone cannot force the model to follow a rule, so the two rules that matter most are also checked in code:

1. **Quote check.** Every quote must appear word for word in the chunk it cites, or the harness deletes it.
2. **Refusal rewrite.** When the verdict is "not in these texts", the harness throws away the model's wording and prints a fixed refusal that lists what the corpus covers.

The second check comes from a real failure. In the add_document test, the model refused but wrote "The corpus does not cover Bastiat's essay Government (1848) where this quote appears". That still names the author, from memory, which rule 1 forbids and the teacher cannot verify. In the evaluation it rewrote all 9 refusals. The quote check deleted nothing in the evaluation. In the demo it once deleted a book title in quotation marks, so titles are now allowed. I prefer a strict check with a rare false alarm to one that lets a fake quote through.

## Evaluation

All 36 questions went through the agent. The headline numbers:

| Result | Value |
| :---- | :---- |
| Correct, by the judge | 34 / 36 (94%), 95% interval 86%–100% |
| Supported by the passages, by the judge | 34 / 36 (94%) |
| By kind (correct) | single 20/20 · multi 6/8 · unanswerable 8/8 |
| Unanswerable questions refused | 8 / 8, no invented answer |
| Answerable questions refused by mistake | 1 (q25) |
| Judge agrees with my 23 grades | 23 / 23 |
| Answers with a quote over 25 words | 10 / 36 |
| Average cost per question | 5,517 tokens, 26.8 s |

I graded the answers in three ways.

**Code checks** cover what can be checked exactly:

| Check | single (20) | multi (8) | unanswerable (8) |
| :---- | ----: | ----: | ----: |
| every cited chunk_id came from a search | 20 | 8 | 8 |
| refused exactly when it should | 20 | 7 | 8 |
| cited the expected document | 20 | 6 | n/a |
| retrieved the expected paragraph | 19 | 0 | n/a |
| every quote ≤ 25 words | 14 | 4 | 8 |

The 0/8 on multi questions is less bad than it looks. The agent writes its own queries and never retrieved both expected paragraphs, but in 6 of the 8 it found other passages that make the same point. Two problems are real. Ten answers quote more than 25 words, which breaks rule 4. And on q35 the model refused without searching: the refusal was right, but it skipped rule 1.

**An LLM judge** grades meaning. It is gemini-3.5-flash, a stronger model than the agent's gemini-3.5-flash-lite, at temperature 0. It writes its reasoning first, then gives two yes/no grades. *Correct*: the verdict and main claim match my reference, and answering only one side of a two-thinker question counts as wrong. *Supported*: nothing in the answer goes beyond the retrieved text. A true fact from the model's memory still fails, because the teacher has no passage to check it against.

**My own grades** came last. I graded 23 answers before opening the judge's output, and we agreed on all 23. That sounds perfect, but only 3 of the 23 were failures (q20, q25, q26). The judge flagged the same three for the same reasons, but three failures say little about how it handles many. Agreement also only shows that the judge grades like me, not that the answers are right.

All the numbers are rough. 20/20 on single questions does not mean zero errors: with 20 questions, a true error rate up to about 15% could still give a clean score. It is also a single run, and the model's answers change a little each time. Files: eval/results.csv, eval/judge.json, eval/human_labels.csv, eval/summary.json.

## Failures

Three answers failed:

| Question | Kind | Cause | What happened |
| :---- | :---- | :---- | :---- |
| q25 | multi | retrieval miss | Mill's passage on morality and class never came back from search, so the agent refused the whole question, though it had the Marx & Engels half |
| q26 | multi | wrong answer from the right passage | it found the right Bastiat passage but quoted another one; the question is also too open (borderline bad test question) |
| q20 | single | unsupported claim | it added a true fact about Paine that none of the retrieved passages contain |

No answer to an unanswerable question was invented, and no citation was fake.

Two-thinker questions are the weak spot: two of the three failures are multi. The failures also differ in cost. q25 is the cheap kind; the teacher just checks the book. q20 is the risky kind. A fact from memory slipped into the answer sentence, outside quotation marks, where no check looks. It happened to be true, but this is exactly how misattributions start.

My process has a weak point too. The retrieval design and the AGENTS.md edits were picked while I was looking at these same 36 questions, so the scores are probably a bit too kind. A fair test would use a new set of claims, ideally from real essays, run once after all choices are made.

Fixes, in order:

1. Allow partial answers. For q25 the right reply was "Marx & Engels: said it; Mill: not in these texts", but today one missing side turns everything into a refusal.
2. Search again for a thinker when their best passage has a low score.
3. Cut quotes to 25 words in code.
4. Check the answer sentences against the passages, not only the quotes. That would have caught q20.

## Decision

Yes, for one job: a first check on claims about a single thinker. It should never change a mark unless the teacher reads the quote first.

Why yes: all 20 single-thinker answers were correct, all 8 unanswerable questions were refused with nothing invented, and every citation pointed to a real passage. A confident wrong verdict is the expensive mistake, and it did not happen on this set.

Where to be careful:

- **Two-thinker answers** are only a hint until partial answers work.
- **"Not in these texts"** means "check by hand", not "the student is wrong". The corpus covers parts of five books, so a real quote from another chapter of Mill gets the same verdict.
- **"Said something different"** should never lower a mark by itself, because a wrong one is the costliest error.
- **The user matters.** A teacher who knows Mill will spot a strange verdict. A new teaching assistant is more likely to trust it, so for them reading the quote is a must. The citation makes that a few seconds of work.

Cost: 5,517 tokens and 26.8 seconds per question on average; two-thinker questions take more because they need two or three searches. The full test set used about 199,000 tokens and stayed inside the free tier. Half a minute is slow for a chat, but much faster than finding a paragraph in a book.

To run it at a school, I would record the prompt version and model with every answer, and rerun the 36 questions after any change to AGENTS.md or the tool descriptions. The add_document test showed that a few words there can change behaviour, so a change only stays if it clearly scores better.

## AI use

I used Claude Code as a coding partner. It wrote most of the Python (index.py, retrieval.py, server.py, agent.py, evaluate.py), building on the class examples one step at a time, and I asked it to explain each part before moving on. What it built followed my choices: the corpus, the two chunking designs I compared, hybrid search with k = 5, the verdict format, the guardrails and how add_document treats duplicates. I am not a specialist in these texts, so I also asked an LLM to point me to the key chapters and to suggest themes and ideas for questions; I wrote the questions from those and checked each one against its paragraph and reference answer. My 23 human grades were done before I looked at the judge. Claude ran the bootstrap intervals, and I checked each number against the files in eval/. I wrote this report myself and only used AI to check it for grammar mistakes. In short, the AI sped up the building; the use case, the decisions and the conclusions are mine.
