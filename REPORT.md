# Assignment 3 Report

- **Name**: Vittorio Fialdini
- **Student ID**: 18843
- **Group**: BBADBA 5A

## Use case

**Who asks:** the compliance team of a medium-sized EU cocoa importer. Under the EU Deforestation Regulation (EUDR) the importer is an *operator*. Before each shipment the team must run due diligence and file a due diligence statement. They ask questions such as "Which cocoa products are covered?", "Do we still need farm coordinates for a low-risk country?" or "How long can customs hold a shipment?", and they act on the answer directly.

**What a wrong answer costs:** a wrong answer can lead to a non-compliant shipment being stopped and confiscated. Expected cost = 3% chance of a check × one 13 t container × £3,842/t (ICE London cocoa) ÷ 0.833 £/€ ≈ **€1,800**.

The 3% is an approximation. Article 16(8) requires annual checks to cover at least 3% of *operators*, and I use that as the chance that a given *shipment* is checked. The real chance depends on how the authority selects operators and shipments, and on the country's risk class.

**What "I don't know" costs:** one hour of the team's own research at €51.60/h (Eurostat 2025, professional services, euro area) = **€51.60**.

A wrong answer therefore costs about 35 times a refusal. The assistant is only worth using if its error rate on answered questions stays below **51.6 / 1,798.7 = 2.9%** (break-even). The whole system is tuned to refuse when in doubt.

## Corpus

Retrieved 18 November 2026 (details in [corpus/SOURCES.md](corpus/SOURCES.md)). The legal texts come from the EU Publications Office (Cellar) API, because EUR-Lex blocks scripted downloads.

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| Regulation (EU) 2023/1115 (EUDR), consolidated text incl. Reg. 2024/3234, 2025/2650 and Delegated Reg. 2026/2102 | https://publications.europa.eu/resource/celex/02023R1115-20260918 | 18 Sep 2026 | EUR-Lex reuse with attribution (Decision 2011/833/EU) | 19,688 |
| Commission Notice: Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | https://publications.europa.eu/resource/celex/52026XC03896 | 20 Jul 2026 | EUR-Lex reuse with attribution (Decision 2011/833/EU) | 19,069 |
| Commission FAQ: Implementation of the EUDR, version 5 | [CIRCABC](https://webgate.ec.europa.eu/circabc-ewpp/d/d/workspace/SpacesStore/4dc28987-bc5a-4b71-bd46-a13b611f3ebb/download) | Apr 2026 | CC BY 4.0 (Commission Decision C(2019) 1655) | 44,456 |
| **Total** | | | | **83,213** |
| *Added later:* Implementing Regulation (EU) 2025/1093, country risk list (`corpus/to_add/`) | https://publications.europa.eu/resource/celex/32025R1093 | 22 May 2025 | EUR-Lex reuse with attribution | 1,177 |

No personal data. The consolidated text has no legal effect; the FAQ and Guidance are not legally binding. The assistant flags this whenever an answer rests on them.

## Ingestion

[index.py](index.py) runs four steps:

1. **Download** the missing documents.
2. **Extract** one *unit* per natural legal unit:
   - the consolidated act (HTML): one unit per article and annex, paragraphs kept apart;
   - the Guidance (Official Journal HTML): one unit per numbered heading;
   - the FAQ (PDF, via `pypdf`): one unit per numbered question, with its page number.
3. **Clean** each unit:
   - remove consolidation markers (`►M1`, `◄`);
   - remove footnote numbers;
   - join PDF hyphenation artefacts (`non -deforestation`);
   - fix spaces before punctuation;
   - render tables one row per line, cells joined by ` | `.
4. **Chunk** in two designs, then **embed** with `gemini-embedding-2` (768 dimensions). Each batch of 50 is saved to ChromaDB as soon as it arrives, and chunks that already have a vector are never embedded again.

**Extraction problem fixed:** the FAQ PDF opens with a table of contents that lists every question with dot leaders and a page number. A naive per-question split produced every question twice: once as an empty title with the wrong page from the contents, once with its real text. The extractor now finds the last contents entry and starts the body after it. PDF lines are not paragraphs either, so lines are rejoined and re-split at sentence ends into paragraph-sized blocks.

**Chunk metadata:** each chunk carries:
- `source` (EUDR / Guidance / FAQ);
- `file` and `doc_title`;
- `location` (e.g. `Article 9(1)`, `Guidance §4(e)`, `FAQ 1.3, p. 13`);
- `unit_title`;
- `covers`: every unit the chunk contains, used for hit-rate scoring.

The citation the assistant must use (`Cite as: [...]`) is built from `source` and `location`.

**Number of chunks:**

| Design | Rule | Chunks |
|---|---|---|
| structure | one chunk per unit; units over 350 words split at paragraph boundaries, and the location names the paragraphs held, e.g. `EUDR Article 25(1)–(2)` | 377 |
| fixed | 150-word windows, 30-word overlap, ignoring structure; cited by the unit of the first word | 606 |
| added | the benchmarking act, added with `add_document` (structure design) | 8 |

## Test set

I wrote 38 questions in [eval/questions.csv](eval/questions.csv) from the documents before tuning anything. Each question is phrased the way the compliance team would ask it, and each has a reference answer and an expected location.

| Kind | Count |
|---|---|
| single | 25 |
| multi (two passages) | 7 |
| unanswerable | 6 |
| **Total** | **38** |

The unanswerable questions stay close to the topic so the assistant is tempted to guess, for example:
- Ghana's risk class: the list is not in the base corpus;
- the Dutch competent authority;
- the number of checks made in 2025;
- whether the EUDR requires the Living Income Differential.

**Examples**

- **q28 (multi):** *"For cocoa from a low-risk country, which due diligence steps can we skip, and do we still need the farm coordinates?"* Expected: EUDR Article 13 + FAQ 1.28. Reference: risk assessment and mitigation (Art. 10–11) can be skipped if the risk of circumvention or mixing is negligible, but geolocation is still required.
- **q33 (unanswerable):** *"Is Ghana classified as a low-risk country under the EUDR?"* Reference: the corpus does not contain the country list (it is in Implementing Regulation (EU) 2025/1093). The assistant should refuse. This question is also used for the add-document test.

## Retrieval

Scoring: hit rate on the 32 answerable questions. A hit at k means one of the top k chunks covers the expected location. For multi questions, any of the expected passages counts as a hit, and "all passages @5" is reported separately. Source: [eval/retrieval_summary.csv](eval/retrieval_summary.csv).

| Design | hit@1 | hit@3 | hit@5 | multi: all passages @5 | words in prompt @1 / @3 / @5 |
|---|---|---|---|---|---|
| fixed (150 words) | 0.562 | 0.719 | 0.750 | 4/7 | 150 / 450 / 750 |
| fixed + BM25 hybrid | 0.469 | 0.625 | 0.656 | 3/7 | 150 / 450 / 750 |
| **structure** | **0.688** | **0.844** | **0.938** | 2/7 | 183 / 605 / 1,028 |
| structure + BM25 hybrid | 0.438 | 0.625 | 0.719 | 2/7 | 172 / 628 / 1,029 |

**Chosen design: structure chunking, vector search only, k = 5.**

- **It wins clearly at every k**: +19 points at hit@5 over fixed windows. Its only misses at k = 5 are q02 and q29.
- **Its chunks map onto citable units**, so the cited article or FAQ question is exactly what the team will open.
- **The cost** is about 280 more words per prompt at k = 5, which is cheap.

**Trade-off: multi-passage questions.** Structure chunking finds *both* passages of a multi question in the top 5 only 2/7 times, against 4/7 for fixed windows. I accepted this for two reasons:
- The agent searches again when the first passages are not enough: 1.43 searches per multi question against 1.16 per single question.
- End to end, 5 of 7 multi questions were answered correctly. The other 2 failed because of the citation guardrail, not retrieval (see Failures).

**Hybrid BM25 made both designs worse.** A likely reason: the questions' keywords ("cocoa", "operator", "due diligence") occur in a large share of the chunks, so the keyword ranking adds noise and pushes the right passage down.

## Tools and subagent

**MCP server** ([server.py](server.py)) with two tools.

`search(query)`:
> Search the EU Deforestation Regulation (EUDR) corpus: the consolidated Regulation (EU) 2023/1115 (articles and annexes, as amended up to 18 September 2026), the Commission's 2026 Guidance document and the Commission's FAQ (version 5, April 2026), plus any document added with add_document. Use it for any question about EUDR obligations of operators, traders and importers (for example cocoa importers): scope and product codes, due diligence, geolocation, due diligence statements, dates of application, checks and penalties. Search again with other words if the passages do not answer the question. Returns the 5 most relevant passages, each starting with "Cite as: [...]", the citation to put after every claim taken from it, followed by the document title and the passage text.

If the daily embedding quota is used up, `search` falls back to BM25 keyword search and says so in the result.

`add_document(path)`:
> Add a document to the EUDR corpus so that search can find it: an HTML (e.g. EUR-Lex), PDF, Markdown or text file on this computer, given by its file path. The file is cleaned, cut into passages with their location, embedded and stored in the index. If the same content is already indexed, nothing is embedded again. If a file with the same name but different content was added before, its old passages are replaced by the new version. Returns how many passages were added and how they are cited, or why the file was not added.

`add_document` imports `chunk_file()` and `embed_and_store()` from `index.py`; it does not reimplement them.

**One search result** (first passage returned for *"simplified due diligence low risk country Article 13 risk assessment mitigation"*):

```
[1] Cite as: [Guidance §4(e)]
Document: Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896) | Simplified due diligence, i.e. sourcing from low-risk countries
Similarity: 0.828
Operators sourcing from low-risk countries are required to exercise due diligence in line with Article 8, fulfil information requirements of Article 9 and establish a due diligence system in line with Article 12.
However, in accordance with Article 13, they are not required to fulfil the obligations under Article 10 and Article 11 where, after having assessed: (i) the complexity of the relevant supply chain; and (ii) the risk of circumvention or mixing with products of unknown origin, or origin in high-risk or standard-risk countries or parts thereof, they have ascertained th[…]
```

**Subagent** ([.claude/agents/corpus-researcher.md](.claude/agents/corpus-researcher.md)). Its only tool is `mcp__corpus__search`. Instructions:

> You research the EUDR corpus for the compliance team of a medium-sized EU cocoa importer. They act on your answer, and a wrong answer can get a shipment confiscated, so a clear "not covered" is better than a guess.
> 1. Search the corpus with the `search` tool before answering. If the passages do not answer the question, search again with other words, at most three searches.
> 2. Answer only from the passages returned. Do not add facts, dates, numbers or country classifications from your own knowledge.
> 3. Put the exact citation shown after "Cite as:" in square brackets after every claim, e.g. [EUDR Article 25(1)–(2)] or [FAQ 10.2, p. 94].
> 4. If the passages do not answer the question, reply starting with "The corpus does not cover this." and say in one sentence what is missing.
> 5. Say when the answer rests only on the FAQ or the Guidance (non-binding Commission views).
> 6. Reply with a short answer of at most 150 words.

**Transcript from Claude Code** (question q28). The raw event stream is in [eval/subagent_transcript.jsonl](eval/subagent_transcript.jsonl); passages are truncated here.

> **User:** Use the corpus-researcher subagent to answer: For cocoa from a low-risk country, which due diligence steps can we skip, and do we still need the farm coordinates?
>
> **Main agent → `Agent`:** `{"subagent_type": "corpus-researcher", "prompt": "For cocoa from a low-risk country, which due diligence steps can we skip, and do we still need the farm coordinates?"}`
>
> **Subagent → `mcp__corpus__search`:** `{"query": "simplified due diligence low risk country Article 13 risk assessment mitigation"}`
>
> **Subagent → `mcp__corpus__search`:** `{"query": "geolocation of plots of land required for products from low-risk countries"}`
>
> **Tool results:** 10 passages, among them [Guidance §4(e)], [EUDR Article 13], [FAQ 5.1 (part 2/2), p. 62], [FAQ 1.1 (part 2/2), p. 12] …
>
> **Subagent (final answer):**
> You can skip risk assessment (Article 10) and risk mitigation (Article 11), but you still need the farm coordinates.
>
> **What you can skip:** You don't have to do Articles 10 and 11 once you have checked two things: how complex the supply chain is, and the risk of circumvention or of mixing with cocoa of unknown, standard-risk or high-risk origin. You must also have confirmed that all the cocoa was produced in low-risk countries [EUDR Article 13]. If the authority asks, you must show documents proving that risk is negligible [EUDR Article 13].
>
> **What you cannot skip:** You still exercise due diligence under Article 8, collect the Article 9 information and keep a due diligence system under Article 12 [Guidance §4(e)].
>
> **Coordinates:** The Commission says you still collect the geolocation of the plots of land [FAQ 5.1 (part 2/2), p. 62]. This rests on the FAQ and Guidance, which are not legally binding.
>
> **When the exemption ends:** If you learn of information pointing to non-compliance, you must do Articles 10 and 11 in full and tell the authority at once [EUDR Article 13].
>
> *(59.5 s)*

The subagent followed its rules:
- it searched twice with rephrased queries;
- every citation appears as a "Cite as:" line in the results;
- it flagged the non-binding basis.

The reference points to FAQ 1.28; the subagent found the same rule in FAQ 5.1 instead. One search also returned `[Benchmarking Low Risk Countries]`, because the live index includes the added document (see the next section). The evaluation runs excluded it.

## Adding a document

**Already indexed:** the server keeps a registry ([index/added_documents.json](index/added_documents.json)) of each added file's SHA-256 hash, its chunk ids and the date it was added.
- **Same content again:** nothing is embedded, and the tool says when the file was added and how many passages it has. No quota is used.
- **Same file name, new content:** the old passages are deleted first, then the new version is indexed. An updated act therefore never sits in the index twice.
- **Unsupported or empty file:** refused with a reason.

**Demo** ([eval/add_document_demo.json](eval/add_document_demo.json)) with the unanswerable question q33 and Implementing Regulation (EU) 2025/1093 (country risk list). In the demo, `evaluate.py` calls the tool's function (`server.add_document()`) directly, as the person running the evaluation, not through the agent. The approval prompt therefore does not appear here; it is shown in the next section.

| Step | Output |
|---|---|
| Before | "The corpus does not cover whether Ghana is classified as a low-risk country; please consult the latest implementing acts published by the European Commission or check with your national competent authority. All countries were initially assigned a standard level of risk on 29 June 2023 [EUDR Article 29(2)]." |
| `add_document` | "Added eudr_country_benchmarking_2025-1093.html: 8 passages indexed, cited for example as [Benchmarking preamble (part 1/3)] …" |
| Add again | "Already indexed: eudr_country_benchmarking_2025-1093.html was added on 2026-11-19 11:56 with 8 passages. Nothing was embedded." |
| After | "Yes, Ghana is classified as a low-risk country under the EUDR [Benchmarking Low Risk Countries]. Under Commission Implementing Regulation (EU) 2025/1093 establishing the country risk list, Ghana is included among the countries considered to present a low risk [Benchmarking Annex, Benchmarking Low Risk Countries]." |

After the document was added, the first search returned the list of low-risk countries, which includes Ghana, at rank 5. The answer is correct and cited.

The demo also shows two small rule breaks:
- The "before" refusal does not start with exactly "The corpus does not cover this." (the harness accepts the "The corpus does not cover…" prefix), and it adds a true but unrequested fact.
- The "after" answer puts two citations in one bracket, against AGENTS.md rule 3. The citation check splits the bracket and accepts both, because both were retrieved.

## Harness and guardrails

[agent.py](agent.py) uses LangChain `create_agent` on `gemini-3.5-flash-lite` (temperature 0). The tools come from `server.py` over MCP stdio, and [AGENTS.md](AGENTS.md) is the system prompt.

**AGENTS.md rules**, each with its reason in the file:
1. Search before every answer, at most three searches.
2. Answer only from the returned passages: no dates, numbers, codes or country classes from memory.
3. Cite every claim with the exact "Cite as:" citation, one per bracket.
4. If not covered, begin with exactly "The corpus does not cover this." plus one sentence on where to look; no partial guess.
5. If partly covered, answer that part and say what is missing.
6. Say when the answer rests only on the FAQ or Guidance (not binding).
7. At most 150 words, direct answer first.
8. Use `add_document` only when the user asks for a specific file.

**Guardrails run by the harness**, so the model cannot skip them:

1. **Approval before `add_document`:** a `wrap_tool_call` middleware intercepts the call and asks `Allow add_document({...})? [y/N]`. Without a keyboard (check.py, evaluation) the answer is no. The model receives "The user refused this tool call. Do not try to add the document another way."
2. **Call limits:** at most 6 model calls and 4 tool calls per question, against runaway loops.
3. **Citation check (extra guardrail):** every bracketed citation in the final answer must match a `Cite as:` key that a search returned *in this run*, and an answer that is not a refusal must cite at least one passage. Shortened forms (`FAQ 1.3` for `FAQ 1.3, p. 13`), `(part n/m)` labels and paragraphs inside a retrieved range (`Article 12(3)` within `Article 12(1)–(4)`) are accepted. Otherwise the draft is **withheld** and replaced by a refusal telling the team to check the sources. Runs that called `add_document` are exempt: the reply then shows the tool's own result (see below). The reasoning: a wrong answer costs about 35 refusals, so an answer that cannot show its source is not worth showing.

**A case where the guardrail fired (q06, "Can we use a mass balance chain of custody for our cocoa?").** The draft was right: "No, mass balance chains of custody are not allowed [FAQ 1.4, p. 14]". But it also cited `[FAQ 5.1, p. 14]`, a mix of two retrieved FAQ question numbers and a page that no search had returned. The check flagged that citation as invalid and withheld the whole answer. The guardrail did what it was built to do, since it cannot tell a mislabelled citation from an invented one. Here it cost a correct answer (see Failures).

**The approval step in use** (`main.py ask "Please add the file corpus/to_add/eudr_country_benchmarking_2025-1093.html to the corpus"`, run in a terminal; the seconds include the time spent at the prompt):

Answered `n`:

```
  Allow add_document({'path': 'corpus/to_add/eudr_country_benchmarking_2025-1093.html'})? [y/N] n
  call add_document({'path': 'corpus/to_add/eudr_country_benchmarking_2025-1093.html'})
Not added: you declined the add_document call.

(25.0 s, 2102 input + 61 output tokens, 2 model calls)
```

Answered `y`:

```
  Allow add_document({'path': 'corpus/to_add/eudr_country_benchmarking_2025-1093.html'})? [y/N] y
  call add_document({'path': 'corpus/to_add/eudr_country_benchmarking_2025-1093.html'})
Already indexed: eudr_country_benchmarking_2025-1093.html was added on 2026-11-19 11:56 with 8 passages. Nothing was embedded.

(24.3 s, 2188 input + 77 output tokens, 2 model calls)
```

With `n`, the call never reached the server. With `y`, it ran, and because the file's hash matches the registry the tool embedded nothing. Afterwards the registry still lists the file once, with the same 8 passages and its original date. Pressing Ctrl+D at the prompt also counts as "no" and prints "Not added: you declined the add_document call."

**How the upload reply was fixed.** In my first version both runs above printed the guardrail's refusal ("The corpus does not cover this. An answer was drafted, but … withheld"), whether I approved or not, and Ctrl+D at the prompt crashed the run with an `EOFError`. The cause was that the citation guardrail and AGENTS.md rule 4 assume every reply answers an EUDR question: a reply must either cite a passage or open with the refusal sentence, and a reply about an upload has nothing to cite. Three changes in [agent.py](agent.py):

1. **Runs that called `add_document` are exempt from the citation rule.** The harness shows the tool's own result instead of the model's draft, so the user sees what really happened. A cited EUDR answer in the same run is still shown after it.
2. **A declined call is reported in plain words:** "Not added: you declined the add_document call."
3. **End of input (Ctrl+D) or Ctrl+C at the prompt counts as "no"** instead of crashing.

None of this changes the evaluation, because no test question adds a document: rerunning `main.py evaluate` gives the same numbers.

## Evaluation

[evaluate.py](evaluate.py) runs the agent on all 38 questions against the original corpus only (`base_only=True`).

**Code checks:**

| Check | Result |
|---|---|
| Is it a refusal? (starts with "The corpus does not cover") | n/a |
| All citations valid (retrieved in this run) | 34/38 |
| Answerable questions where the expected passage was cited | 30/32 |
| Drafts withheld by the guardrail | 4 |

Code also decides the support of refusals: a refusal makes no factual claims, so it counts as supported.

**LLM judge:** `gemini-3.1-flash-lite`, a different model from the agent, temperature 0, structured output. It sees the question, the reference answer, every passage retrieved in that run and the answer. Rubric (v2):

- **Correct:** states the substance of the reference and nothing that contradicts it. Missing minor detail is fine; a wrong or missing key fact (date, number, yes/no, obligation) is not. A refusal of an answerable question is not correct. For unanswerable questions, only a refusal is correct, optionally with a pointer to where to look.
- **Supported:** each factual claim is checked one by one against the passages. Qualifiers ("higher", "only"), definitions and conclusions drawn from a definition must be in the passages too. A claim from general knowledge fails even if it is true. Disclaimers and advice are not claims. The two criteria are judged separately.

**The rubric needed two revisions** before it agreed with my grades, measured on my 20 hand grades in [eval/human_labels.csv](eval/human_labels.csv), made from [eval/grading_sheet.md](eval/grading_sheet.md) before I read the verdicts:

| Judge version | Correct: agreement (κ) | Supported: agreement (κ) | What changed |
|---|---|---|---|
| v1 | 95% (0.86) | 75% (−0.14) | n/a (first version) |
| v2 | 100% (1.00) | 80% (−0.11) | criteria judged separately; qualifiers and definitions must be in the passages |
| v2 + refusal support in code (final) | **100% (1.00)** | **90% (0.00)** | the judge marked refusals (q06, q14) as "unsupported" |

**Why κ = 0 despite 90% agreement on "supported":** in my 20 graded answers the judge marked *every* answer supported. With no variation on the judge's side, Cohen's κ is 0 by construction: the agreement is no better than a rater who always says "supported". The two disagreements are the cases where I found an unsupported claim and the judge did not:
- **q08:** "Member States can set *higher* fines". FAQ 10.2 only says they have discretion to set the level.
- **q31:** "SMEs *including medium enterprises*". No retrieved passage defines SMEs.

Both are subtle qualifiers. **The judge is reliable on correctness but too lenient on support**, so support still needs a human spot check.

**Results** (final run, 38 questions; [eval/summary.json](eval/summary.json), [eval/results.csv](eval/results.csv)):

| Outcome | single | multi | unanswerable | Total |
|---|---|---|---|---|
| Correct | 23 | 5 | – | **28** |
| Wrong (substantive answer that is wrong) | 0 | 0 | 0 | **0** |
| Correct refusal | – | – | 6 | **6** |
| Wrong refusal | 2 | 2 | – | **4** |
| Unsupported (judge) | | | | **1** (q26) |
| Unsupported (my grades) | | | | **2** (q08, q31) |

All 6 unanswerable questions were refused. No answer was wrong.

**Compared with the first full run** ([eval/run1_summary.json](eval/run1_summary.json)): 23 correct, 10 wrong refusals and 11 withheld drafts, with an expected cost of €20.37 per question. The agent's drafts and search traces are identical in run 1 and the final run: same model, same AGENTS.md, all 38 match. Everything that changed is in the code that checks and grades the drafts. There were four changes, made in this order:

1. **Citation matcher loosened** (run 1 → `judge_v1`). In run 1 the guardrail rejected 6 drafts whose citations pointed at a retrieved passage but were written differently from its "Cite as:" key:
   - the `(part n/m)` label dropped: `FAQ 5.1, p. 62` for `FAQ 5.1 (part 2/2), p. 62` (q23, q28);
   - a sub-point of a retrieved paragraph: `EUDR Article 2(13)(a)` for `EUDR Article 2(13)` (q02);
   - several citations in one bracket: `EUDR Article 4(2), 12(1)–(2)` (q21);
   - other written forms of retrieved FAQ citations (q16, q30).

   The matcher now accepts these forms, but still rejects citations to passages no search returned. Applied to the same drafts, it withheld only 4 (q06, q14, q27, q29), each with a citation that was genuinely not retrieved. All 6 freed drafts were judged correct.
2. **Refusal detection loosened** (same step). Run 1 counted a reply as a refusal only if it began with exactly "The corpus does not cover this." Now any reply beginning "The corpus does not cover" counts.
   - **q33** ("The corpus does not cover whether Ghana…") had been scored as a substantive answer and is now a correct refusal.
   - **q38** had been withheld for citing nothing and is now passed through as the agent's own refusal.
3. **Judge rubric v1 → v2.** A refusal with a pointer to where to look now counts as correct (q36). Qualifiers and definitions must be in the passages. q15's support verdict went from 0 to 1.
4. **Support of refusals decided in code.** The judge had marked the refusals q14, q27 and q29 as unsupported. A refusal makes no claims, so code now marks them supported.

Together, changes 1 and 2 cut wrong refusals from 10 to 4 and the expected cost from €20.37 to €13.58 per question. Changes 3 and 4 raised agreement with my grades (see the judge table above). All four changes were made after seeing these test results, so the final numbers are somewhat optimistic for new questions.

## Failures

Each failure from the final run, classified by cause:

| Cause | Count | Questions | What happened |
|---|---|---|---|
| Wrong refusal | 4 | q06, q14, q27, q29 | The draft was **correct** and cited the expected passage, but carried **one** citation that no search had returned, so the guardrail withheld it. q06 and q29 cited a wrong FAQ number or page (`FAQ 5.1, p. 14`, `FAQ 1.7, p. 18`). q14 and q27 cited a sub-point, `EUDR Article 25(2)(b)–(c)`, outside the retrieved range. |
| Unsupported claim | 3 | q08, q31 (my grades); q26 (judge) | A qualifier or definition not in the passages: "higher" fines; "including medium enterprises". In q26 the answer is correct (three due diligence steps, from 30 December 2026 for medium enterprises), but it adds two parentheticals from the model's own knowledge. It says information collection includes "geolocation of the plots of production in Côte d'Ivoire", and it spells out compliance as "produced on land without forest conversion after 31 December 2020, and in accordance with local legislation". The cited passage [Guidance §4 (part 1/2)] only says "comply with Article 3"; none of the retrieved passages mention geolocation or 31 December 2020. I checked this by hand: the judge saw all 9,847 characters of evidence, and its verdict is right. |
| Retrieval miss | 0 | – | q02 and q29 missed the top 5 in the retrieval stage, but the agent searched again and found the passage. |
| Wrong answer from the right passage | 0 | – | |
| Bad test question | 0 | – | |

**What to fix first: the citation guardrail's all-or-nothing behaviour.** It caused every wrong refusal, and each of those drafts was correct. Two fixes, in order:
1. **Repair before withholding:** send the draft back once with the list of retrieved citations and ask the model to correct or drop the invalid ones.
2. **Smaller change:** drop only the sentence that carries the invalid citation, if the rest still cites a valid passage.

Turning the 4 wrong refusals into correct answers would cut the expected cost from €13.58 to €8.15 per question, without letting any uncited claim through.

**Second: the unsupported qualifiers**, which are the most dangerous failure for this team: a "higher" fine is exactly the kind of detail they would act on. Possible fixes:
- an AGENTS.md rule to quote rather than paraphrase limits and definitions;
- a stricter support judge;
- human review of every answer about penalties.

## Decision

**Yes, but only as a cited research aid, not as an answer the team acts on unchecked.**

What speaks for it:
- In 38 questions it gave **0 wrong answers** and refused all 6 questions the corpus cannot answer.
- Expected cost per question is **€13.58** against €51.60 for doing the research by hand.

Why that is not yet proof that it is safe:
- With 0 errors in 28 answered questions, the 95% upper bound on the error rate is about 3/28 ≈ **11%** (rule of three). That is well above the 2.9% break-even.
- Showing the error rate is below break-even would take roughly 100+ answered questions with no errors.
- Two to three answers contained an unsupported qualifier.

**Use it for:** scope and product codes, due diligence steps, geolocation, dates, information requirements. These are questions where the answer is a passage the team can open and read.

**Do not rely on it alone for:** penalty amounts, country classifications or anything that decides whether to ship. A refusal also only means the corpus does not cover the topic; the team should then go to the competent authority or a lawyer.

**Safeguards:**
1. The citation guardrail stays on: no answer is shown without a retrieved citation.
2. Every answer is checked against the cited passage before acting. The cited passage is an exact article or FAQ question, so this takes seconds.
3. The corpus is updated with `add_document`, with approval, when the Commission publishes new acts or a new FAQ version.

**Cost and latency per question** (final run, 38 questions):

| Measure | Value |
|---|---|
| Latency | 7.5 s mean (3.0–15.9 s) |
| Tokens | 4,993 input + 182 output ≈ 5,200 |
| Model calls / searches | 2.3 / 1.3 |
| API cost | free Gemini tier (`gemini-3.5-flash-lite` agent, `gemini-3.1-flash-lite` judge, `gemini-embedding-2`); query embeddings cached in `index/query_cache.json` |
| Claude Code subagent (one question) | 59.5 s, $0.25 |

## AI use

I used Claude Code as a coding assistant to write and debug the indexing, server, harness and evaluation code, and to review the project against the assignment. It also helped me write the report by turning my bullet points into paragraphs; I checked every number against the files in `eval/` and edited the text. The analysis and decisions in the report, the test questions, the reference answers and the 20 human grades are my own.
