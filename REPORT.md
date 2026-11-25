# Assignment 3 Report

- **Name**: Sofia Siso Rodriguez
- **Student ID**: 195430
- **Group**: PPLEDBA 5A

## Use case

- Who asks: a voter in Spain comparing party programmes before the next election, or a student or journalist checking what a party promised.
- What they do with the answer: form an opinion, quote a party, decide how to vote.
- Cost of a wrong answer: a proposal attributed to the wrong party, or a number or ban that isn't in the programme, can change someone's view and spreads easily.
- Cost of "I don't know": about a minute to look it up in the PDF yourself. That's why the system prefers refusing to guessing, and why every claim has a page citation.

## Corpus

Why these parties: the four with the most seats and the most distinct positions (government, main opposition, left coalition, right-wing party). Elections are comming up and its important to be informed and know what you ahve voted for in the past (why I chose 2023 programmes), and what you will vote for now.
Why 2023: the last general election before the 2026 one. The 2026 Vox programme is kept for the add-document demo.

| Document | Party | URL | Downloaded | Licence | Pages | Words |
|---|---|---|---|---|---|---|
| psoe_2023.pdf | PSOE | https://www.elindependiente.com/wp-content/uploads/2023/07/ProgramaElectoral_ElexGenerales_PSOE_2023.pdf | 2026-11-21 | reuse terms not found | 272 | 106,912 |
| pp_2023.pdf | PP | https://www.pp.es/wp-content/uploads/2023/07/programa_electoral_pp_23j_feijoo_2023.pdf | 2026-11-21 | reuse terms not found | 112 | 31,226 |
| sumar_2023.pdf | Sumar | https://movimientosumar.es/wp-content/uploads/2023/07/Un-Programa-para-ti.pdf | 2026-11-21 | reuse terms not found | 182 | 105,677 |
| vox_2023.pdf | Vox | https://files.mediaset.es/file/2023/0707/15/programa-vox-completo-pdf | 2026-11-21 | reuse terms not found | 178 | 26,537 |

Total: 4 documents, 270,352 words. All are the full programmes for the general election of 23 July 2023.

## Ingestion

Text was extracted page by page with pypdf. Front pages with no programme text were skipped (PSOE pages 1-11, PP 1-5, Sumar 1-6, Vox 1-6). Lines repeated on more than 20% of the pages (headers and footers) were removed, and words split by a hyphen at the end of a line were rejoined. Each chunk is stored with id, source file, party, year, first and last PDF page, and a location such as "pp. 45-46". The result is 651 chunks (PSOE 257, PP 75, Sumar 257, Vox 62). Embedding model: gemini-embedding-2 with 768 dimensions; store: ChromaDB with cosine distance.
One extraction problem I fixed: in the Vox PDF the letters "fi" were extracted as Chinese characters ("de昀椀ende" instead of "defiende"). I map them back to "fi" before chunking.

450 words, 50 overlap: the programmes are lists of short numbered measures. About 450 words keeps several related measures together with context. Smaller chunks lose context. Larger chunks blur the vector and add words to the prompt. The overlap stops a measure from being cut in half at a boundary.
Party and year in the embedded text: the four programmes use very similar wording ("derogaremos…", "impulsaremos…"), so without the party name a vector can't tell them apart.
768 dimensions: a smaller index (the limit is 90 MB) and faster search, with little quality loss.
PDF page numbers: the user can open the PDF at that page and check the claim. The printed numbers differ from the viewer numbers, so I had to be very rigorous.

## Test set

38 questions in eval/questions.csv: 25 single, 6 multi (need passages from two or more parties) and 7 unanswerable. The questions and reference answers are in Spanish, like the programmes.

I picked the topics spread across parties and policy areas, concrete numbers and bans.
I checked the oages pretty manually thorugh Chrome page counter, and searching phrases.
The unanswerable ones I checked they're absent (find_text.py with 0 matches, plus one deliberately tricky case).
AI helped with page checking and translation.

Example: eval page

q32,"¿A cuántos euros quiere el PP subir el salario mínimo?",unanswerable,,, -> this fopr exampel is a trap, the PP programme talks about updating the minimum wage but never gives an amount.
q01,"¿Qué propone el PP sobre la educación de 0 a 3 años?",single,pp_2023,p. 50,"Será universal y gratuita, cofinanciada por el Estado y las Comunidades Autónomas."

## Retrieval

B is better at hit@1: 0.84 vs 0.76 for single questions. They're equal at hit@3 and hit@5, and B costs no extra embeddings.
I had to be careful about Certainty: 31 questions means one question moves a score by 3 to 4 points, so the evidence is weak.
Limit of B: it only helps when a party is named. It does nothing for multi questions (0.67 hit@5 for both).
hit@1 for multi is 0.00 because one passage can't cover two parties..

| Design | Questions | hit@1 | hit@3 | hit@5 | Words added to the prompt (top 5) |
|---|---|---|---|---|---|
| A plain vector search | all (31) | 0.61 | 0.84 | 0.90 | 2242 |
| A plain vector search | single (25) | 0.76 | 0.92 | 0.96 | 2240 |
| A plain vector search | multi (6) | 0.00 | 0.50 | 0.67 | 2250 |
| B party filter | all (31) | 0.68 | 0.84 | 0.90 | 2247 |
| B party filter | single (25) | 0.84 | 0.92 | 0.96 | 2246 |
| B party filter | multi (6) | 0.00 | 0.50 | 0.67 | 2250 |

I chose design B.

- q25: after checking p. 113: water is covered in many Vox passages and the expected one ranked outside the top 5
- q28: Vox's passage was found at rank 3, but four of the five results were Vox passages, so the expected PP passage (p. 34) was pushed out.
- q29: all five results were Sumar passages, so the expected PP and PSOE passages did not make it into the top 5.

Misses (expected passage not in the top 5, same for A and B): q25 (single), q28 and q29 (multi).

## Tools and subagent
**Tool descriptions (from server.py)**

search:
```
Search the election programmes of four Spanish parties (PSOE, PP, Sumar, Vox) for the
general election of 23 July 2023, plus any programme added later with add_document.

Use it for every question about what a party proposes, promises or says in its programme.
The programmes are written in Spanish; the question can be in English. Do NOT use it for
election results, polls, candidates' personal lives or opinions about which party is better:
the programmes do not contain them.

party (optional): PSOE, PP, SUMAR or VOX. Set it when the question is about one party, so
that party's text is not crowded out by the others. Leave it empty to search every
programme, for example when comparing parties.

Returns up to 5 passages, best first. Each starts with its citation in square brackets,
such as [psoe_2023, pp. 45-46] (document, PDF pages), followed by the Spanish text and a
distance (smaller = closer to the question). If no passage actually answers the question,
the programmes do not cover it.
```
The description tells the model when to use the tool, when not to (polls, opinions), how to use the party filter, and how to read the result, including that "no passage answers" means "not covered".

add_document:
```
Add one PDF document to the searchable index, for example a party programme from another election.

path: location of a PDF file, relative to the project folder or absolute (for example
demo/vox_2026.pdf). The file name decides how it is cited: name it party_year.pdf, such as
vox_2026.pdf, so the party and year are recorded.

The PDF is cleaned, cut into passages and embedded with the same pipeline as the original
corpus. If the document is already indexed and unchanged, nothing is embedded and nothing
changes. If the file changed, only the changed passages are embedded and the outdated ones
are removed. This uses embedding quota, so only call it when the user asked to add a document.

Returns how many passages were added, kept and removed.
```
It says to call the tool only when the user asked, because adding a document changes the index and uses embedding quota, so the model should not do it on its own.

**One search result**
```
[pp_2023, pp. 50-51] (PP 2023, distance 0.210) con responsabilidad, criterio propio y libertad, en un mercado laboral totalmente diferente...
```
**Subagent instructions (.claude/agents/corpus-researcher.md)**
```
---
name: corpus-researcher
description: Finds what the Spanish parties' 2023 election programmes (PSOE, PP, Sumar, Vox) say about a topic. Delegate any question of the form "what does party X propose on Y" or "how do the parties differ on Y". Returns a short cited answer, or says the programmes do not cover it.
tools: mcp__corpus__search
---

You answer questions about the election programmes of PSOE, PP, Sumar and Vox (general election of 23 July 2023) using only the search tool. You have no other tools and no other knowledge to rely on.

How to work:

Call search with the question. When one party is named, set party to PSOE, PP, SUMAR or VOX. When comparing parties, search once per party.
Read the returned passages. They are in Spanish.
Reply in English, in a few sentences. Put a citation such as [psoe_2023, pp. 45-46] after every claim, exactly as the search printed it. Quote the key Spanish phrase when the exact wording matters.
If the passages do not answer the question, start the reply with NOT COVERED: and say the programmes do not cover it. Never guess and never use outside knowledge.
Stay neutral: describe what each programme says in the same way for every party. Do not say which party to vote for or which proposal is better.
Say that these are 2023 programmes unless a citation shows another year.
```
It only has the search tool so it can only answer from the programmes. With web access or other tools it could use outside knowledge, which would break the "cite every claim from the passages" rule.

I also tried the subagent from the editor's chat, with the question "Ask corpus-researcher what the PP proposes about education for children aged 0 to 3." The editor answered NOT COVERED (twice), although the programme does cover this topic. The editor's MCP log shows Connection state: Error spawn uv ENOENT, so the editor could not start the corpus search server because it cannot find the uv command. I then tried pointing the config to the virtual-environment Python by its full path, but the server still would not start from the editor. So in the editor the subagent had no search tool and, following its rules, refused instead of inventing an answer. This is a limitation of my editor setup, not of the server: the same server.py is started correctly by main.py from the terminal, and the answers in the evaluation come from it.

## Adding a document

Demo: the question "¿Qué propone Vox sobre la remigración?" (a term that does not appear anywhere in the 2023 programmes: find_text.py gives 0 matches).

Before adding demo/vox_2026.pdf, the five passages returned for Vox were all from vox_2023 (pp. 100-102, 101-105, 103-108, 95-100, 136-141), and none of them is about the remigración, so the agent would have to answer NOT COVERED.

After add_document, three of the five passages are from vox_2026 (pp. 15-20, 19-24, 12-15) and the top one contains the measure: "13. Remigración. Plan para facilitar el retorno a sus países de los extranjeros que no contribuyan o vivan de subsidios públicos…". The index now answers from the new document, with a page citation.

Limit: I ran this demo by calling the search and add_document tools directly, because the Gemini chat model returned 503 "high demand" errors for several hours, so the agent could not run. This means the approval step (typing "y") was not part of this run.

This shows, for example that new documents can be added without rebuilding the index.

## Harness and guardrails
Rules: search first, answer only from the passages, cite every claim, start with NOT COVERED: when the passages don't answer, name the year, use the party filter, stay neutral, answer in English with the Spanish quote, only add documents when asked, no results or polls.
Approval: a human must type y before add_document runs, and automatic runs always say no.
Call limit: at most 4 tool calls per question.
Extra guardrail: the neutrality check. It fired on "Who should I vote for?" with 0 tool calls and 0 tokens.

Disclaimers: The neutrality check in code instead of only a rule in the prompt because the model can ignore a prompt rule, code runs before the model, and it can not catch certain things because it matches certain English phrases, so other wording or other languages get past it.


## Evaluation
The LLM judge scored only 29 of the 38 answers (q01 to q29), because Google's service returned 503 "high demand" errors for hours and the last nine (q30 to q38) could not be judged before the deadline. The 29 verdicts come from two models: 19 from gemini-3.6-flash and 10 from gemini-3.1-flash-lite, because the daily limit of the free key forced a change during the run. The answers themselves were generated by gemini-3.1-flash-lite. The judge marked all 29 answers correct and supported. I graded 24 answers myself, and 18 of them have a judge verdict. On these 18, the judge agrees with me on 17 (94%) for "correct" and for "supported", but Cohen's kappa is 0.0 for both, because the judge said yes every time. It missed both failures I found: q29 (the agent wrongly said PSOE and Sumar were not covered after its searches errored) and q20 (a claim not supported by the passages). So the judge is too lenient, and I trust my own grades more than the judge's.

I checked every answer in three ways.

**Code checks.** Three things can be tested without a model: (1) whether a refusal happened (the answer starts with "NOT COVERED" or the neutrality guardrail fired) and whether it was the right call for the question type; (2) whether every citation in the answer, such as [pp_2023, p. 34], matches a passage the search actually returned, so the model cannot invent a page; (3) whether the expected passage from my test set was among the retrieved passages.

**LLM judge.** A Gemini model reads the question, my reference answer, the retrieved passages and the agent's answer, and returns three 0/1 verdicts with a reason: correct (the answer matches the reference, or properly refuses an unanswerable question), supported (every claim is in the retrieved passages) and refused. My rubric (eval/rubric.md) says Multi-party answer must cover both parties, that a number or threshold that is wrong counts as incorrect, and that a hedged answer to an unanswerable question counts as incorrect.

My own grades. I graded 24 answers by hand from the grading sheet. I later corrected four of my grades (q27, q28, q30, q31) after checking the full tool traces, which showed that a retry had returned the passages. 

Refusals (code check): the agent refused 6 of the 7 unanswerable questions and refused none of the 31 answerable questions outright. The code check counts an answer as a refusal only if it starts with NOT COVERED or a guardrail fires, so it does not count a partial wrong refusal such as q29, where the agent wrongly said PSOE and Sumar were not covered after search errors and the call-limit guardrail fired. I found q29 in my own grades. The unanswerable question the code check marks as not refused is q32: the agent did say that the programme gives no euro amount for the minimum wage, and quoted what the programme does say (update it within social dialogue), but in its own words and without starting with NOT COVERED, so the code check did not count it as a refusal.

Results. Code checks, over all 38 answers: every citation matched a retrieved passage in 30 of the 30 answers that cite (100%); 30 of the 32 non-refusals cite something (94%); and the expected passage was retrieved for 29 of the 31 answerable questions (94%). LLM judge, over the 29 judged answers (q01 to q29): 29 correct and 0 unsupported. My own grades found two failures in the answers that both of us graded: q29 (not correct) and q20 (not supported). The answers were all written by gemini-3.1-flash-lite. The judge verdicts come from two models (see above), so they may not be perfectly comparable. 

## Failures
In my first full judge run, four answers failed (q29, q30, q31, q32). I classified them by looking at the tool traces in eval/agent_answers.jsonl

- Search tool error, then call limit (1): q29. The first searches for PSOE, Sumar and PP crashed with "Tool error", which used up 3 of the 4 allowed tool calls, so the agent wrongly said PSOE and Sumar were not covered.
- Judge saw too little text (2): q30 and q31. The first searches errored, the retries returned the Vox and PSOE passages with the right claims, but the judge only read the first 14,000 characters of the retrieved text and marked the answers as unsupported. I checked that the passages do contain the claims ("Reintroduciremos los delitos de referéndum ilegal, sedición…" and "desalojo… en un plazo máximo de 48 horas").
- JCode check too strict (1): q32. The agent said the programme gives no amount and quoted what it does say, which is the right behaviour, so this is not a system failure

So none of the four failures was the model answering wrongly from the programmes. They came from the harness around it. Two bugs were behind them: the Chroma connection crashed when two searches ran at the same time (fixed by sharing one connection in get_collection), and the judge text limit (raised from 14,000 to 40,000 characters).I raised the judge limit, but the rerun could not reach q30 and q31 before the deadline, so I could not confirm the fix on them.

What I would fix first: the concurrent search crash, because it caused the only real wrong answer (q29) and also wasted tool calls on many multi-party questions

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

Cost and latency per question (average over 38 questions, gemini-3.1-flash-lite): about 6,620 tokens (6,418 in, 202 out), 11.1 seconds on average and 46.3 seconds at most, and 1.4 tool calls. For me, 11 SECODNS IS A COMPLETELY acceptable amount for waiting 

I would let voters use it to find what a party promised in its 2023 programme, with a page they can open and check. The answers come from the parties' own election programmes, not from the government or from the news.

I would not let them use it to decide who to vote for, or to find election results, polls, or anything after the 2023 programmes. The neutrality check refuses "who should I vote for" before the model is called.

Safeguards I rely on: every claim has a page citation, the agent says NOT COVERED when the passages do not answer, adding a document needs a human to type "y", and a call limit stops it from looping.

What I am not sure about: my test set has only 38 questions, so one question moves a score by 3 to 4 points. The judge was partly the same model that wrote the answers (10 of 29 verdicts), so it may share its mistakes, and it was too lenient: it missed both failures I found (q29 and q20). It also covered only 29 of the 38 answers.


## AI use

I used Claude (Anthropic) as a coding assistant. Claude helped me fix errors that I pasted in, translated passages when I asked, and checked page numbers and facts against the PDFs.
The test questions and reference answers I wrote.
The decisions (use case, chunking, design choice, refusals, judge rubric, ship decision), my grades, and the analysis in this report are mine.