# Assignment 3 Report

- **Name**: Diana de Lorenzo
- **Student ID**: 20119
- **Group**: BBADBA 5B

## Use case

**Who asks.** The product and marketing team of a small Spanish niche
perfume brand, before launching or relabelling a fragrance. They ask
questions such as: which fragrance allergens must be on the label and from
what concentration, whether an ingredient is allowed and up to what level,
whether the box can say "hypoallergenic", or what the safety report must
contain.

**What they do with the answer.** They decide the text of the label, the
formula and the marketing claims, or they escalate the question.

**What a wrong answer costs.** If the assistant answers wrongly, the brand can
get into serious trouble. The product can be withdrawn and the whole stock
relabelled, which is a large cost for the brand: for one batch of ~5,000
units, tens of thousands of euros. But the biggest cost is not the product:
customer loyalty and the brand's image can fall, and sales with them. There
can also be fines from the health and consumer authorities. And if a customer
has an allergic reaction, it becomes a huge problem: lawsuits, trials and
compensation.

**What "I don't know" costs.** The team asks an external regulatory
consultant instead: about **€100** and **2–3 days** of waiting.

**So a wrong answer is hundreds of times worse than "I don't know".** The
assistant should only answer when the documents clearly support it, cite the
exact article or annex entry so the team can check it, and otherwise say it
does not know.

## Corpus

| Document | URL | Date | Licence | Words |
|---|---|---|---|---:|
| Regulation (EC) No 1223/2009 on cosmetic products, consolidated text (articles + Annexes I–X, incl. fragrance allergens in Annex III) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02009R1223-20250501 | consolidated 1 May 2025 | EU legal texts, free reuse (Commission Decision 2011/833/EU) | ~71,700 |
| Commission Implementing Decision 2013/674/EU, guidelines on Annex I (cosmetic product safety report) | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013D0674 | 25 Nov 2013 | same | ~12,400 |
| Commission Regulation (EU) No 655/2013, common criteria for claims | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013R0655 | 10 Jul 2013 | same | ~1,500 |
| **Total** | | | | **~85,600** |

Downloaded by `index.py` from the EU Publications Office (the same texts as
EUR-Lex). No personal data. I use the **consolidated** regulation because the
original 2009 text has been amended many times (for example, the list of
fragrance allergens to label was extended in 2023): an assistant on the old
text would give outdated answers, which is exactly the wrong answer this use
case cannot afford.

## Ingestion

**Extract.** `index.py` downloads the three texts as XHTML from the EU
Publications Office (EUR-Lex blocks scripted downloads) and walks them in
order, tracking where it is from the headings: chapter, article and article
title, annex, part and section. Front matter (titles, the list of amending acts,
recitals) is dropped; so are Annex IX and X (repealed directives and a
correlation table).

**Clean.** Consolidated texts carry amendment markers (`▼M12`, `►C3`) and
deleted entries (`—————`): removed. Footnote markers and non-breaking spaces
are normalised. Each row of the substance tables (Annexes II to VI) becomes one
readable line that names every column, e.g. *"ANNEX III entry 84. Chemical
name/INN: …; Common ingredient name: Linalool; CAS number: 78-70-6; … Other:
The presence of the substance must be indicated in the list of ingredients …
when its concentration exceeds 0,001 % in leave-on products …"*. Rows that
only continue an entry (another product type or limit) are appended to it.

**Extraction problems I fixed.**
- *Lost paragraph numbers.* The consolidated text keeps "1." and "(a)" outside
  the paragraph, so chunks could not be cited as Article 19(1)(g). They are now
  put back in front of their paragraph.
- *Lost one-paragraph points.* When a point is a single paragraph, the text sits
  directly in a `<div>` with no `<p>`; the first version skipped it, and
  Article 5(1) ("Responsible persons shall ensure compliance with…") and
  Article 19(5) (language of the label) were missing. Fixing it recovered about
  3,000 words.
- *Footnotes glued to an entry.* The notes under a table came as one cell and
  were appended to the last substance (a 1,400-word "entry"); they are now their
  own blocks, split at sentence ends.
- *Pictures.* Annex VII's symbols are images; each section keeps a block with
  its title so it can still be found.

**Chunk.** Two designs, compared in Retrieval:
- `fixed`: 200-word windows with 40 words of overlap over the running text,
  blind to structure — **681 chunks**.
- `structure`: never across two articles, sections or annexes; long ones split
  at paragraph boundaries (max 250 words); substance entries grouped but never
  split; every chunk starts with *"<document>, <location>:"* — **568 chunks**.

**Metadata** on every chunk: `source` (document), `location` (article and title,
annex entry or entries, guideline section), `file`, `entries` (annex reference
numbers), `sha` (for added documents). Vectors: `gemini-embedding-2`, 768
dimensions, stored in ChromaDB in `index/`, saved batch by batch; a rerun only
embeds chunks without a vector and deletes chunks that no longer exist.

## Test set

32 questions in `eval/questions.csv`, written as the brand's product and
marketing team would ask them, before tuning anything: **22 single**, **5
multi** (two passages, usually an article plus an annex entry) and **5
unanswerable** (close to the topic but outside EU law: IFRA standards, US FDA,
China, Spanish fees, private cruelty-free certificates). Each has the expected
source and location as in the chunk metadata and a short reference answer.

| id | kind | question | expected location | reference answer |
|---|---|---|---|---|
| q23 | multi | If our perfume contains linalool, must we declare it on the label and from what concentration? | Article 19; ANNEX III, entry 84 | Yes, in the list of ingredients when it exceeds 0,001 % in leave-on products (0,01 % rinse-off). |
| q28 | unanswerable | What specific limits does IFRA set for certain fragrance ingredients in category 4 perfumes? | — | The corpus does not cover it: EU law only, no IFRA standards. |

While checking the questions against the text I changed three: q17 (the
open-jar symbol is a picture in Annex VII; its meaning is written in
Article 19), q18 (the corpus never says "hourglass", only "the symbol in point 3
of Annex VII or the words 'best used before the end of'") and q27 (made
specific: musk ketone, Annex III entry 97).

## Retrieval

On the 27 answerable questions (`eval/retrieval.csv`). *hit@k*: at least one
expected passage in the top k; *all@5*: every expected passage (matters for the
multi questions); words = what the top 5 add to the prompt.

| Design | hit@1 | hit@3 | hit@5 | all@5 | words @5 |
|---|---:|---:|---:|---:|---:|
| **structure + vector (chosen)** | **0.70** | **0.89** | **0.93** | **0.81** | **913** |
| structure + hybrid (vector + BM25) | 0.70 | 0.85 | 0.93 | 0.81 | 945 |
| fixed + vector | 0.59 | 0.74 | 0.85 | 0.74 | 985 |
| fixed + hybrid | 0.52 | 0.78 | 0.93 | 0.78 | 997 |

**Choice: structure chunking with vector search, k = 5.** Structure beats
fixed windows at every k (+11 points at hit@1, +15 at hit@3) and adds the
fewest words to the prompt. Hybrid search did not help on structure chunks: my
questions use common names ("linalool"), not CAS numbers, so exact keyword
matching adds little; it only helped the fixed windows at k = 5. With the
chosen design, two questions have no expected passage in the top 5 (q20, whose
expected section is "Evidential support" while other claims criteria were
retrieved, and q21), and three multi questions miss one of their two passages
(q24 and q27 miss the article, q26 misses section 3.8). Only q21 and q26 led to
a wrong answer (see Failures).

## Tools and subagent

**`search(query)`** — *"Search the EU cosmetics law corpus: Regulation (EC) No
1223/2009 on cosmetic products (consolidated May 2025: articles on safety,
responsible person, product information file, notification, animal testing,
labelling and claims, plus the annexes listing prohibited and restricted
substances, fragrance allergens, colorants, preservatives, UV filters and
packaging symbols), Implementing Decision 2013/674/EU (guidelines on the
cosmetic product safety report) and Regulation (EU) No 655/2013 (criteria for
product claims). Use it for any question about what EU cosmetics law requires
or allows. Phrase the query with the terms the law uses … Returns the 5 most
relevant passages, numbered, each headed by "source | location" … cite those
exactly. The corpus covers EU law only."*

**`add_document(path)`** — *"Add one document to the corpus index so search can
find it. `path` is a local file (.pdf, .html/.xhtml or .txt) … extracted,
chunked with the same pipeline as the corpus (index.py) and embedded with
Gemini. If exactly the same file is already indexed, nothing is done; if a file
with the same name but different content is indexed, its old passages are
replaced. Returns what was done and how many passages were added."*

**One search result** (query "linalool labelling concentration leave-on", first of 5):

```
[1] Regulation (EC) No 1223/2009 (consolidated 2025-05-01) | ANNEX III, entries 80-84
… ANNEX III entry 84. Chemical name/INN: 1,6-Octadien-3-ol, 3,7-dimethyl-;
Common ingredient name: Linalool; CAS number: 78-70-6; EC number: 201-134-4;
Other: The presence of the substance must be indicated in the list of
ingredients referred to in Article 19(1)(g) when its concentration exceeds:
— 0,001 % in leave-on products — 0,01 % in rinse-off products
```

**Subagent** (`.claude/agents/corpus-researcher.md`, tool: `mcp__corpus__search`
only): search before answering, search again with the law's own terms if
needed; answer only from the passages in two to six sentences, numbers and
conditions exactly as written; cite every claim with the passage header; if the
passages do not answer, reply exactly "The corpus does not cover this
question." and use no other knowledge (IFRA, national rules, non-EU law).

**Transcript from my editor (VS Code, GitHub Copilot, agent mode):**

*[PENDING: paste the Copilot transcript here]*

## Adding a document

**Already indexed.** `add_document` hashes the file. If exactly the same file
is already in the index, it adds nothing ("already indexed; nothing changed"),
so the same text is not retrieved twice and does not get extra weight. If a
file with the same name but different content is indexed, the old passages are
replaced by the new version and the tool says how many it replaced, so a
person can check whether the old version still matters (for example, as
history). Both cases were tested.

**The demo** (`demo_add_document.py`, full log in `eval/add_document_demo.md`):
q29, *"What labelling requirements does the US FDA impose to sell a perfume in
the United States?"*, with the FDA *Cosmetics Labeling Guide*
(https://www.fda.gov/cosmetics/cosmetics-labeling-regulations/cosmetics-labeling-guide,
US government work, public domain; 114 passages).

| Step | Result |
|---|---|
| Before | "The corpus does not cover this question." |
| Add, approval refused | Nothing added. |
| Add, approval given | 114 passages added. |
| After, same AGENTS.md | Still refuses, **without searching**: rule 5 says the corpus is EU law only. |
| After, one line added to the system prompt ("the corpus now also contains the FDA Cosmetics Labeling Guide") | Searches and answers: FD&C Act and FP&L Act; required statements in English; fragrance may be declared as "fragrance"; required information prominent and not obscured — each cited to the guide's sections. |
| Same file again | "already indexed (114 passages); nothing changed." |

**Lesson:** adding a document is not enough; the description of the corpus in
the assistant's rules must be updated too, or the agent trusts the rules and
does not even search. Afterwards the FDA passages were removed again so the
index matches the test set, where q29 is unanswerable.

## Harness and guardrails

**AGENTS.md** (the system prompt of `agent.py`, also read by the editor's
agent), each rule with its reason: (1) search before answering, every time;
(2) answer only from the search results; (3) cite every claim with the exact
passage header; (4) if the corpus does not cover it, reply exactly "The corpus
does not cover this question."; (5) no other sources (IFRA, national rules,
non-EU law); (6) keep numbers and their conditions exactly as written; (7) add
documents only when the user asks; (8) be short.

**Approval.** `add_document` is wrapped so it only runs after a person types
"y" at the terminal; with nobody at the terminal (evaluation) it is refused.
In the demo the refused call added nothing; the approved one added 114
passages. **Call limits:** at most 6 model calls and 4 tool calls per question.

**Extra guardrail: citation check.** After the model answers, `agent.py`
compares every `[source | location]` it cites with the passages search
actually returned in that run. If a citation was never returned, or a
non-refusal cites nothing, the answer is withheld and replaced by the refusal.
Why: in this use case an invented or mis-copied citation is the dangerous
case, because the team trusts the citation when it prints a label.

**Where it fired.**
- *First run (too strict):* it withheld **8 correct answers** (q04, q06, q09,
  q15, q20, q22, q25, q26) because the model put several citations in one
  bracket (`[A | Article 4; Article 5]`) or added a point number
  (`Evidential support (1)`). I kept that run (`eval/answers_run1_strict_guardrail.jsonl`)
  and changed the parser to split those, while still requiring every cited
  passage to be one that search returned.
- *Final run:* it fired once, on **q22**: the model shortened the location to
  "ANNEX I, 6. Exposure to the cosmetic product", which search never returned
  under that name. The answer was right, so this is a false positive (a wrong
  refusal, see Failures), but it is the cheap kind of error for this use case.
- It also turned the agent's message after an approved `add_document` into a
  refusal (no citation to check); confirmations of added files are now exempt.

## Evaluation

**Code checks** (`evaluate.py`, per answer): refused or not (exact refusal
sentence); number of citations; citations valid (the guardrail did not fire);
cites the expected source; correct refusal (refused an unanswerable question);
wrong refusal (refused an answerable one); tokens and seconds.

**Judge** (`gemini-3.1-flash-lite`, temperature 0, JSON output) gets the
question, my reference answer, the retrieved passages and the answer. Rubric:
- `correct` = 1 if the answer gives the same rule, number and condition as the
  reference (other wording and extra correct detail are fine; a missing key
  condition or a different number is 0). A correct legal point the reference
  omits is not penalised. An unanswerable question is correct only if the
  assistant says the corpus does not cover it; refusing an answerable one is 0.
- `supported` = 1 if every factual claim is in the retrieved passages. A pure
  refusal makes no claim, so it is supported = 1.

**Results** (32 questions, `eval/results.csv`, `eval/summary.json`):

| | Count |
|---|---:|
| Correct (judge) | **28 / 32** |
| Answered with content | 27 (24 correct) |
| Unsupported answers (judge) | **0** |
| Correct refusals | 4 / 5 unanswerable |
| Wrong refusals | 1 (q22) |
| Unanswerable answered anyway | 1 (q32) |
| Guardrail fired | 1 |
| Tokens / seconds per question | 3,830 / 29.7 s |

**Agreement with my grades** (`eval/human_labels.csv`, all 32, graded before
reading the judge): **91 % on correct** (disagree on q04, q17, q32), **72 % on
supported**. The supported disagreements are mine: I gave 0 to seven answers
(q04, q08, q10, q11, q15, q16, q19) because they added detail I had not checked
in the passages. Checking them afterwards, every added claim is literally in
the retrieved text (e.g. q15, "based on the perception of the average end
user", 655/2013 Annex 1(2)). Lesson: "not verified" is not "unsupported"; I
left the grades as I first gave them so the agreement figure stays honest.

## Failures

Failures = the five answers I graded incorrect. None of the other answers has
an unsupported claim (checked above).

| Question | Cause | Why |
|---|---|---|
| q21 | Retrieval miss | It did not retrieve section 3, Part A of the guidelines, where the full list of contents of the safety report is. |
| q26 | Retrieval miss | It retrieved the claims passage but not section 3.8 (toxicological profile) of 2013/674; the question needed both. |
| q17 | Wrong answer from the right passage | It found Article 19 and explained the symbol but did not complete the answer: 12M means 12 months after opening. |
| q22 | Wrong refusal | Section 3.6 was retrieved and the model had started to answer; the citation guardrail blocked it. |
| q32 | Bad test question | Classified as unanswerable, but Article 20 does give useful information: there is no mandatory private certificate, and it sets the conditions for claims about animal testing. |

**Counts:** retrieval miss 2, wrong answer from the right passage 1, wrong
refusal 1, bad test question 1, unsupported claim 0.

**What to fix first: retrieval.** It is the most frequent failure (2 of 5),
and in q21 and q26 the agent did not find all the information, especially when
the answer needs more than one part of the regulation. I would try a larger k
(8), a second search when the question names several elements, and a check
that every needed part was retrieved before answering. Second, the citation
check: q22 shows the agent can find the information and answer, but a
guardrail that is too strict blocks a valid answer, so it should accept a
shortened citation that clearly matches a retrieved passage. Last, the test
set: q17 should be phrased around what the regulation actually says, and q32
should no longer be unanswerable.

## Decision

**Yes, but as a support and lookup tool, never as the final authority on
regulatory questions.**

I would use it for informative, fairly direct questions: what must appear on
the label, the concentration limits of specific ingredients, the general
obligations of the EU Regulation, and orientation on cosmetic claims.

I would not rely on its answers directly when the question needs several
articles or annexes combined, when exceptions or complex legal requirements
must be interpreted, when the answer can affect whether a product or a campaign
is legal, or when the assistant does not find all the passages it needs or
answers incompletely.

**Safeguard:** every regulatory statement must carry a verifiable citation of
the regulation (the citation guardrail enforces this), and answers about
claims, labelling and safety must be reviewed by a person from the regulatory
team before they are used commercially. If it does not find enough evidence,
it must say so and not complete the answer on its own; for this use case that
costs about €100 and 2–3 days with a consultant, against a recall.

**Cost and latency:** 3,830 tokens and 29.7 s per question on average
(`gemini-3.1-flash-lite` for the agent; one query embedding per search with
`gemini-embedding-2`), all within the free tier. Most of the time is starting
the MCP server and the Gemini calls; the larger flash models were overloaded
(503) during the project, which is a reliability risk for a real deployment.

## AI use

Claude Code (Anthropic) wrote the code (`index.py`, `retrieval.py`,
`server.py`, `agent.py`, `evaluate.py`, `demo_add_document.py`), found and
sized the corpus, and produced the factual tables of this report from the
pipeline's outputs. Claude explained each concept and proposed options; I made
the decisions: the use case and its costs, the corpus topic, the chunking
designs to compare and the design chosen by the numbers, the rules, the judge
rubric, the duplicate-document policy, the failure classification and the
deployment decision. I wrote the test questions and reference answers and
graded the 32 answers myself; Claude checked the questions against the
documents, translated my answers into English and formatted them. I reviewed
the code and the final text and can explain every decision.
