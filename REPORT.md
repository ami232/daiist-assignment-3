# Assignment 3 Report

- **Name**: Arturo Velilla
- **Student ID**: 19455
- **Group**: BBADBA 5B

## Use case

The target is Student pilots studying the knowledge behind a go/no-go decision: weight and balance, aircraft performance and density altitude, aeromedical factors, emergency procedures and weather hazards.

They use it to study and to prepare a decision, for example whether a hot, high, heavy departure is reasonable, how long to wait after diving, or what to do if ice develops on the engine. The assistant is a study aid, its target is not to make the final call.

**What a wrong answer costs compared with "I don't know":** A confident wrong answer about a takeoff distance, speed, waiting time or an icing hazard can lead to an accident, so it is the most expensive outcome. "I don't know, check the manual or ask your instructor" costs a few minutes. The system is therefore built to refuse whenever the retrieved passages do not support an answer, and every claim must carry a page citation the user can check.

## Corpus

Selected chapters of three FAA handbooks. All are works of the US Government and in the public domain, they contain no personal data. The full books total about 600,000 words, far more than the free embedding quota allows, so I kept the chapters that matter for a go / no-go decision.

| Document (source id) | Chapters kept | URL | Edition | Licence | Words indexed |
|---|---|---|---|---|---|
| Pilot's Handbook of Aeronautical Knowledge (FAA-H-8083-25C) | 10 Weight and Balance, 11 Aircraft Performance, 17 Aeromedical Factors | faa.gov/regulations_policies/handbooks_manuals/aviation/phak | 2023 | Public domain (US Gov.) | 33,599 |
| Airplane Flying Handbook (FAA-H-8083-3C) | 18 Emergency Procedures | faa.gov/regulations_policies/handbooks_manuals/aviation/airplane_handbook | 2021 | Public domain (US Gov.) | 10,989 |
| Aviation Weather Handbook (FAA-H-8083-28B) | 18 Visibility, 19 Turbulence, 20 Icing, 22 Thunderstorms | faa.gov/regulationspolicies/handbooksmanuals/aviation/faa-h-8083-28-aviation-weather-handbook | 2026 | Public domain (US Gov.) | 13,736 |
| Total | 8 chapters |  |  |  | 58,324 |

Added later through the add-document tool: Pilot's Handbook chapter 15, Airspace (4,998 words, 37 chunks), cut from the same PDF.

## Ingestion

`index.py` downloads the PDFs into `corpus/`, extracts only the chosen page ranges, cleans and chunks the text, embeds it with `gemini-embedding-2` (768 dimensions) and stores it in ChromaDB in `index/`. Each chunk id is a hash of its design, source, chapter and text, so `main.py index` only embeds chunks that do not already have a saved vector, and vectors are saved after every batch of 50.

### Extraction and cleaning

- **Font-based extraction (pypdf).** For every text fragment I read its font family and size. Body text is the most common (family, size) in the document; a heading is bold text in another family at body size or larger, or the body font set larger. Everything else is dropped: figure labels, axis numbers, captions and running headers.
- **Location.** The printed page number (e.g. `11-4`) is read from the page footer or the Weather Handbook's running header ("Chapter 20, Icing 20-2").
- **Cleaning.** Split line ends are joined, "[Figure 11-2]" references removed, and words that pypdf splits ("f reezing", "w ith", "containin g") rejoined. Two pieces are joined only when the joined word appears elsewhere in the same handbook and one piece is not a common word on its own.

### Extraction problems fixed

1. **Glued words in the Airplane Flying Handbook** ("factorsthat mayinterfere witha"). The spaces between words are set in a different font (Times-Roman) from the words (Times New Roman), so my body-font filter dropped them. Fix: keep whitespace fragments whatever their font.
2. **My first split-word repair broke real words.** A regex that joined a single letter to the next word turned "Earth's gravitational" into "Earth'sgravitational". Fix: the vocabulary-based rule above.
3. **A page that crashed pypdf.** PDF page 448 of the Pilot's Handbook (a dense figure) raised `LimitReachedError`; I raised pypdf's parsing budget.
4. **Missing page numbers.** Page numbers are printed at the bottom, after the body text, and a back-fill bug left most Airplane Flying Handbook chunks without one. Fixed; only two figure-only pages (18-7, 18-8) still have none.

**Known limitation.** Tables drawn as figures are dropped with the other figure text. This causes the q09 failure (Figure 17-1, time of useful consciousness).

### Chunks and metadata

Two designs are built side by side, each in its own ChromaDB collection:

- **fixed**: 150-word windows with a 30-word overlap, ignoring structure. 487 chunks, 69–150 words.
- **section**: one chunk per handbook section; sections over 350 words are split at sentence boundaries into about 250-word pieces, and sections under 40 words are merged into the next. The chapter and section heading are prefixed to the embedded text. 290 chunks, 35–369 words (mean 201).

Metadata on every chunk: `source` (handbook id), `title`, `chapter`, `section`, `page` (printed page or span, e.g. "11-3 to 11-4"), `pages` (every page it covers), `words`, `file_hash` and `design`.

## Test set

I wrote 33 questions in `eval/questions.csv` from the handbook text, before tuning anything, phrased the way a student pilot would ask them rather than copying the handbook's wording. Unanswerable questions stay on topic, and each was checked by searching the indexed text for its key terms.

| Kind | Count | What it tests |
|---|---|---|
| single | 21 | One passage answers it; covers every chapter. |
| multi | 6 | Needs two passages, often from two handbooks. |
| unanswerable | 6 | On-topic but not in the corpus: VFR minimums, Class D airspace, wake turbulence, drone rules, a Piper Archer's takeoff roll, private-pilot hour requirements. |
| Total | 33 |  |

**Example 1 (single, q04):** "My main tires are inflated to 36 psi. Above what speed could they start hydroplaning on a wet runway?" Expected `FAA-H-8083-25C`, p. 11-14. Reference: 9 × √36 = about 54 knots, and hydroplaning can continue below that speed. It tests whether the agent applies a formula from the text correctly.

**Example 2 (multi, q24):** "My engine starts running rough on a humid 15 °C day. Could it be carburetor ice, and if it keeps losing power and I have to land off-airport, what should I do with the engine?" Expected `FAA-H-8083-28B` p. 20-7 and `FAA-H-8083-3C` p. 18-4. It needs the icing chapter of one handbook and the emergency chapter of another.

## Retrieval

Hit rate over the 27 answerable questions, with the same query embedding for both designs. A result is a hit when its source matches and its pages include the expected page. **hit@k**: at least one expected passage in the top k. **all@k**: every expected passage (both, for multi questions) in the top k.

| Design | Chunks | hit@1 | hit@3 | hit@5 | all@1 | all@3 | all@5 | Words added (top 5) |
|---|---|---|---|---|---|---|---|---|
| fixed (150 w, 30 overlap) | 487 | 0.96 | 0.96 | 0.96 | 0.74 | 0.81 | 0.85 | 747 |
| section | 327 (290 corpus + 37 added Airspace chapter) | 0.93 | 0.93 | 1.00 | 0.70 | 0.81 | 0.93 | 1,125 |

**Design chosen: section, with k = 5.** The agent reads the top 5 results, and at k = 5 the section design finds every expected passage (1.00 against 0.96) and both passages of a two-passage question far more often (0.93 against 0.85). Fixed chunks are slightly better at k = 1 and 3 and add about a third fewer words to the prompt (747 against 1,125), but about 375 extra words per question is cheap compared with missing half of a two-passage answer. Section chunks also cite more precisely, because each one carries its heading.

## Tools and subagent

`server.py` (MCP, stdio, server name `corpus`) loads the committed index at startup and never re-embeds the corpus.

### Tool descriptions

**search(query)**: "Search the FAA pilot-training corpus and return the 5 most relevant passages." The description then lists the eight chapters and tells the model to search once per part of a two-part question, and explains the citation format `[FAA-H-8083-25C, p. 11-4]`, which answers must copy exactly.

**add_document(path)**: "Add one local document (.pdf, .txt or .md) to the searchable corpus." It runs the same pipeline from `index.py` (imported, not rewritten) and reports "already indexed", "added" or "replaced" with the chunk count. The description tells the model to call it only when the user asks to add that file.

### One search result

`search("rime ice clear ice dangerous comparison")`, first of 5 results (text shortened):

```text
Result 1 [FAA-H-8083-28B, p. 20-2]  (score 0.853)
Aviation Weather Handbook - Chapter 20: Icing - 20.3.2 Clear Icing
Clear ice (or glaze ice) is a glossy, clear, or translucent ice formed by the
relatively slow freezing of large, supercooled water droplets. [...] Clear icing
is a more hazardous ice type for many reasons. It tends to form horns near the
top and bottom of the airfoil [...]
```

### Subagent

`.claude/agents/corpus-researcher.md` can use only `mcp__corpus__search`. Its instructions: search before answering (one search per part, at most 4); answer only from the passages; cite each claim exactly as the result header shows it; if nothing supports an answer, start with "The corpus does not cover this." and name the right source (14 CFR, the POH/AFM or an instructor); keep it short and end hazard answers with a reminder to confirm with the POH/AFM, a briefing or an instructor.

**Transcript** (Claude Code, question q22). Every claim is cited to pages 11-4, 11-5, 11-15 to 11-16 or 11-16. When the main agent also asked about propeller efficiency, the subagent said no retrieved passage covered it instead of making something up.

```text
❯ Use the corpus-researcher subagent to answer this question: Why does my plane need so much more runway on a hot day at a high-elevation airport?

● corpus-researcher(Density altitude runway question)
  Backgrounded agent (↓ to manage · ctrl+o to expand)

I've given your question to the corpus-researcher agent, and it's working in the background now. It will search the handbooks for two things: how heat and high elevation raise density altitude, and how density altitude lengthens the takeoff run. I'll pass along its cited answer as soon as it finishes.

Message from @corpus-researcher:

On a hot day at a high-elevation airport the air is thin, which pilots call high density altitude. Thin air hurts the takeoff in two ways. The plane needs a higher true airspeed before it can lift off, and the engine makes less thrust, so it accelerates more slowly to that speed [FAA-H-8083-25C, p. 11-15 to 11-16].

Why heat and elevation thin the air: high elevation, low pressure, high temperature and high humidity all raise density altitude [FAA-H-8083-25C, p. 11-4]. Air density drops as temperature rises, and pressure falls quickly with height [FAA-H-8083-25C, p. 11-5]. The plane performs as though it were at the density altitude, whatever its actual altitude [FAA-H-8083-25C, p. 11-4].

Why the takeoff run gets longer:
- Faster liftoff speed: the plane lifts off at the same indicated airspeed as at sea level, but its true airspeed is higher because the air is less dense [FAA-H-8083-25C, p. 11-15 to 11-16].
- Speed matters a lot: takeoff distance varies with the square of takeoff speed, so a small increase in speed adds a lot of runway [FAA-H-8083-25C, p. 11-15 to 11-16].
- Less power: an unsupercharged piston engine starts losing power as soon as it is above standard sea level [FAA-H-8083-25C, p. 11-15 to 11-16].

The handbook gives an example. At 5,000 feet pressure altitude, a 790-foot ground run on a standard day becomes about 1,000 feet when it is 20 °C hotter than standard [FAA-H-8083-25C, p. 11-4]. The most critical takeoffs combine high weight, high altitude, high temperature and unfavorable wind, and you have to work out takeoff distance from the AFM/POH data [FAA-H-8083-25C, p. 11-16].

When I briefed the agent, I asked it to also cover propeller efficiency. None of the passages it retrieved discuss that, so this answer doesn't cover it.

Before you fly, check your aircraft's POH/AFM takeoff distance for the actual pressure altitude and temperature, get a current weather briefing, and confirm with your instructor.

Agent "Density altitude runway question" finished · 23s
```

## Adding a document

**Already indexed.** A document's source name is its file name. If a file with the same name and identical content (same SHA-256) is already indexed, nothing is embedded and the tool answers "already indexed", so no quota is wasted. If the name matches but the content changed, the new chunks are embedded and the old ones deleted ("replaced"), so the index never holds two versions of one document.

**Demo.** q29, "What are the vertical limits of Class D airspace around a towered airport, and what do I need to do before I enter it?" (unanswerable). The document added is Pilot's Handbook chapter 15, Airspace (PDF pages 376–387, `PHAK-ch15-Airspace.pdf`), requested through the agent and approved at the approval step.

|  | **Agent output** |
|---|---|
| Before | "The corpus does not cover this. The regulations and airspace classifications you are asking about are found in 14 CFR and the Aeronautical Information Manual (AIM), which are outside the scope of the FAA handbooks in this corpus." |
| Add (approved) | Tool: "Added: 'PHAK-ch15-Airspace' -> 37 chunks, 37 newly embedded." Agent: "I have successfully added PHAK-ch15-Airspace.pdf to the corpus. It has been indexed into 37 chunks and is now available for searching." |
| After | "Class D airspace generally extends from the surface up to 2,500 feet above the airport elevation (charted in MSL) [PHAK-ch15-Airspace, p. 15-2]. Unless otherwise authorized, you must establish two-way radio communications with the ATC facility providing air traffic services prior to entering the airspace and maintain those communications while within it [PHAK-ch15-Airspace, p. 15-2]." |
| Same file again | `{'status': 'already indexed', 'chunks': 37, 'embedded': 0}` |

## Harness and guardrails

`agent.py` uses LangChain `create_agent` on `gemini-3.5-flash-lite` (fallback `gemini-3.1-flash-lite`), loads `server.py`'s tools over MCP and uses `AGENTS.md` as the system prompt.

### AGENTS.md rules

1. Search before answering, once per part of a question, at most 4 searches.
2. Answer only from the passages: no numbers, limits or procedures from the model's own knowledge.
3. Cite every claim exactly as the search result shows it; never cite a page that was not retrieved.
4. If the passages do not answer the question, start with "The corpus does not cover this." and name the source that would. A partial answer must say which part is missing.
5. Regulations (14 CFR, AIM) and specific aircraft figures are out of scope unless a passage states them.
6. For hazards, end with a reminder to confirm with the POH/AFM, a weather briefing or an instructor.
7. Call add_document only when the user explicitly asks to add a specific file.
8. Be concise: direct answer first, then details.

### Approval step and limits

- **Approval:** `HumanInTheLoopMiddleware` interrupts before every `add_document` call and shows the tool and its path; the user types y to approve. Without a terminal (evaluation, check.py) the call is rejected; the demo approves it in code and records the approval.
- **Call limits:** at most 4 tool calls and 8 model calls per question.
- **Resilience:** the free-tier models often answer 503 "high demand", so the agent retries twice and then falls back to a second model. The Gemini SDK's own retries are off, because together with mine they once made one answer take 849 seconds.

### Extra guardrail: citation check

After the agent answers, code checks every citation against the passages actually returned by search in that run. A citation that matches no retrieved passage is removed and flagged; an answer left with no valid citation that is not a refusal is replaced by the refusal. I chose it because an invented citation makes an invented fact look verified, which is the most dangerous failure for this use case.

**Where it fired, and a lesson.** In the first full run it fired on 6 answers (q05, q06, q19, q21, q22, q25), but every one was a false positive: the model wrote two pages in one bracket, `[FAA-H-8083-25C, p. 11-7, 11-18]`, and my parser treated that as one invalid page. It removed good citations from five answers and turned the correct q25 answer (thunderstorm attitude and turbulence distance) into a wrong refusal. I fixed it to check each page in a citation, re-applied the check to the saved raw answers and re-judged them; after the fix it fires on no answer. The first run is kept in `eval/summary_guardrail_v1.json`.

## Evaluation

### Code checks

- Refusal: does the answer start with "The corpus does not cover this."? This gives correct refusals, wrong refusals (on answerable questions) and missed refusals.
- Citations: every citation must match a passage retrieved in that run; also whether the expected source is cited and whether the expected passage was retrieved.
- Number of searches, whether the guardrail fired, tokens and seconds.

### LLM judge and rubric

The judge gets the question, the reference answer, the retrieved passages and the agent's answer, and returns JSON with two 0/1 grades and a reason:

- **correct**: 1 if the answer gives the key facts of the reference with nothing contradicting it, or properly refuses an unanswerable question; 0 if a key fact is missing or wrong, it answers an unanswerable question, or it refuses an answerable one.
- **supported**: 1 if every factual claim is stated in, or directly follows from, the retrieved passages (a refusal counts as supported); 0 if any claim is not, even if it is true.

The judge was meant to be `gemini-3.1-flash-lite`, a different model from the agent. It was overloaded for every request, so 25 of the 33 grades came from `gemini-3.5-flash-lite`, the agent's own model, and 8 from `gemini-flash-lite-latest`. The judge is therefore largely grading its own model's answers.

### Agreement with the human labels

| Field | Agreement | Cohen's kappa | Disagreements |
|---|---|---|---|
| correct | 0.97 (32/33) | 0.65 | q26: labels say it misses the key 2,000 ft fact; judge passed it |
| supported | 0.88 (29/33) | 0.00 | q06, q11, q24, q27: labels mark unsupported extra details; judge passed all four |

The judge gave supported = 1 to every answer, so kappa is 0: it never caught an unsupported detail. It agrees well on correctness but is too lenient on support, probably because it grades its own model's answers.

### Results (33 questions)

| Measure | Judge | Human labels | First run (guardrail v1) |
|---|---|---|---|
| Correct | 0.97 (32/33) | 0.94 (31/33) | 0.94 |
| Supported | 1.00 (33/33) | 0.85 (28/33) | 0.94 |
| Correct refusals (unanswerable) | 6/6 | 6/6 | 6/6 |
| Wrong refusals (answerable) | 1/27 (q09) | 1/27 (q09) | 2/27 (q09, q25) |
| Missed refusals | 0/6 | 0/6 | 0/6 |
| Citations valid (code) | 1.00 |  | 0.82 |

By kind (judge): single 0.95 (20/21), multi 1.00 (6/6), unanswerable 1.00 (6/6).

## Failures

Six of 33 answers fail at least one human grade:

| Cause | Count | Questions | What happened |
|---|---|---|---|
| Retrieval miss | 2 | q09, q26 | q09: the 3–5 minute figure is in the Figure 17-1 table, which extraction drops, so the agent refused (a wrong refusal caused at ingestion). q26: a page-17-4 chunk was retrieved, but not the Histotoxic Hypoxia section with the "one ounce = 2,000 ft" fact, so the answer misses it. |
| Unsupported claim | 4 | q06, q11, q24, q27 | Correct core answer plus one detail not in the passages: longer takeoff/landing distances (q06), sinus advice applied to the ears (q11), a wrong venturi temperature drop (q24: 20–25 °C instead of about 39 °C), and inferred reasoning about flying into cloud (q27). |
| Wrong answer from the right passage | 0 |  |  |
| Wrong refusal (agent) | 0 |  | Both wrong refusals have other root causes: q09 is counted above, q25 was the guardrail bug (fixed). |
| Bad test question | 0 |  |  |

**What to fix first.**

1. **Unsupported details** (4 cases, the biggest group). Add a claim-level check, comparing each sentence's numbers and key terms with the cited passage, and make the judge stricter or use a different model, since it missed all four.
2. **Tables inside figures** (q09). Keep figure text when it forms a table and index it as its own chunk with the figure caption. This needs a re-index, about 300 embeddings.
3. **Pages with several sections** (q26). Evaluate retrieval at section level rather than page level, so a wrong chunk on the right page counts as a miss.

## Decision

**Would I let users rely on it? Not yet.** The foundation is sound: it refused all 6 unanswerable questions, made no missed refusals, and every citation pointed to a passage it really retrieved. But 4 of 33 answers (12%) added a detail the handbook does not say, and one of them was a wrong number (q24: a carburetor temperature drop of 20–25 °C instead of about 39 °C). For student pilots a confident wrong number is exactly the costly outcome, and the citation next to it makes it look verified. The judge also missed all four, so I cannot yet monitor this automatically.

**What must change before I would ship it:**

1. A claim-level check: every number and limit in the answer must appear in the passage it cites, otherwise the sentence is removed or the answer refuses.
2. Index tables inside figures (q09) and evaluate retrieval at section level rather than page level (q26).
3. A stricter judge on a different model, and a larger test set. Ship threshold: no unsupported numbers and at most about 5% unsupported claims.

**For what, once those are fixed:** a study aid for explaining concepts and finding the right handbook page (performance, weight and balance, aeromedical factors, emergencies, weather hazards). Never the final word for a real flight, for regulations or for a specific aircraft's figures, which it refuses by design.

**Safeguards even then:** citations stay mandatory and checked in code, so the user can open the page, and any number used for a real flight must be confirmed on the cited page or in the POH/AFM; the agent already ends hazard answers with this reminder.

**Cost and latency per question** (agent on `gemini-3.5-flash-lite`, free tier):

| Measure | Mean | Range |
|---|---|---|
| Agent tokens | 4,863 | 3,504 – 9,083 |
| Seconds | 14.0 | 2.1 – 142.8 (spikes come from 503 retries) |
| Searches (= query embeddings) | 1.2 | 1 – 2 |
| Judge tokens (evaluation only) | 2,548 |  |

On the free tier the binding limits are requests per day, not cost: `gemini-3.5-flash` allows only 20 requests a day, which is why the agent runs on flash-lite, and embeddings are about 1,000 a day.

## AI use

I used Claude Code (Claude Opus 5.5) throughout:

- **Code:** it wrote `index.py`, `server.py`, `agent.py`, `evaluate.py`, the subagent file and the first draft of `AGENTS.md`, ran the pipeline, and debugged the extraction problems, the batch-embedding bug and the citation-guardrail bug.
- **Suggestions I chose from:** it suggested five use cases, and I chose the student-pilot one; it proposed the chapter selection, and I approved it.

**Mine:** I wrote all 33 test questions and reference answers in `eval/questions.csv`. As I am not an aviation expert, Claude helped me choose the topics and specifics to ask about (what the chapters cover and which on-topic subjects are missing from the corpus); the questions, expected pages and reference answers are mine. I also chose the use case, the section retrieval design and the ship decision.
