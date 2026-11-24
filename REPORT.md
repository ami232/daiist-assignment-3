# Assignment 3 Report

- **Name**: Javier López-Usero Fernández
- **Student ID**: 18633
- **Group**: BBADBA 5B

The sections follow the order of the brief (items 1–9), then Limitations, Reproducibility and AI use. Every number below can be recomputed from the committed files; `tests/test_report_numbers.py` checks them.

## 1. Use case

Drone pilots and operators in the EU ask what the EU rules allow before they fly, buy or register a drone: height and distance limits, which subcategory (A1/A2/A3) and class (C0–C6) applies, registration, pilot competency and authorisations. They act on the answer directly, by flying, buying a drone or registering.

A wrong answer can mean an illegal or unsafe flight, a fine or an accident. "I don't know" only costs the pilot a call to the national aviation authority. So the assistant must refuse rather than guess, and every claim must be traceable to an article the pilot can check.

## 2. Corpus

| Document | URL | Version / date | Licence | Words |
|---|---|---|---|---|
| Commission Implementing Regulation (EU) 2019/947 (operation of unmanned aircraft) | [EUR-Lex CELEX 02019R0947-20220404](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02019R0947-20220404) | consolidated 04/04/2022 | EU legal text; reuse free of charge under the Commission reuse policy (Decision 2011/833/EU), source acknowledged | 19,100 |
| Commission Delegated Regulation (EU) 2019/945 (UAS and third-country operators) | [EUR-Lex CELEX 02019R0945-20200809](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02019R0945-20200809) | consolidated 09/08/2020 | same as above | 20,428 |
| EASA AMC & GM to Part-UAS, Issue 1 (ED Decision 2019/021/R, Annex II) | [EASA PDF](https://www.easa.europa.eu/sites/default/files/dfu/AMC%20&%20GM%20to%20Part-UAS%20%E2%80%94%20Issue%201.pdf) | Issue 1, 9 October 2019 (61 pages) | © EASA; reproduction authorised provided the source is acknowledged | 16,807 |
| **Total** | | | | **56,335** |

All three are public, contain no personal data, and are written for exactly this audience. Word counts are after extraction and cleaning; `main.py index` logs them per document. In the final review, a fresh download and extraction of all three gave these counts and the same chunks as the committed index, so nothing had to be embedded again. The counts can also be rebuilt from the chunks stored in `index/` (removing the overlap between consecutive chunks), which gives the same numbers in the 150- and 400-word indexes; `tests/test_report_numbers.py` does that. Added later for the add-document demo: Regulation (EU) 2021/664 on U-space (6,150 words), see [Adding a document](#adding-a-document).

## 3. Ingestion

`index.py` downloads the three files into `corpus/` (a source that can't be downloaded is skipped with a warning and its stored vectors are kept) and splits each one along its own legal structure before chunking:

- **EUR-Lex HTML** (both regulations): text is split at each `Article N`, `ANNEX`, `PART`, `CHAPTER`, `SECTION`, `Appendix` heading and at each annex point such as `UAS.OPEN.020 UAS operations in subcategory A1`. Headings like `PART 2` take their title from the next line, so the location reads `PART 2 Requirements for a class C1 Unmanned aircraft system`.
- **EASA PDF**: text is split at each AMC/GM heading (for example `AMC1 UAS.OPEN.020(1) and (2) …`), and the page number is added to the location. Table-of-contents pages and the repeated header/footer lines (`Annex II to ED Decision 2019/021/R`, `Page x of y`) are dropped.
- **Cleaning**: EUR-Lex amendment markers (▼M1…) and scripts are removed, words hyphenated across PDF lines are rejoined, and whitespace is normalised.
- **Chunking**: word windows of 150 or 400 words with 20% overlap (step 120 or 320), built *inside* each section, so a chunk never mixes two articles.

**Extraction problem fixed:** in the EUR-Lex HTML, list labels such as `(a)` or `(1)` sit alone on their own line. A plain line-by-line split left them as orphan fragments, separated from the rule they introduce. The extractor now glues a lone label to the line that follows, so `(a) weather conditions` stays one unit.

**Known leftovers:** a few EASA headings keep PDF spacing artefacts (for example `GM1 UAS.SPEC.1 00 The u se of certified equipment`). The A2 guidance headings come out of the PDF as `AMC1 UAS.OPEN.30(1)` rather than `030`. They are kept as extracted, so citations match the stored locations.

**Chunk metadata:** `source` (for example `Reg 2019/947`), `title`, `location` (article / UAS point / AMC-GM heading + page), `chunk` index and `file_hash` (SHA-256 of the file, used by `add_document`). The embedded text is `source | location` followed by the chunk, so headings help retrieval. Embeddings: `gemini-embedding-2`, 768 dimensions, cosine distance, ChromaDB in `index/chroma` (13.0 MB, as `check.py` measures it; limit 90 MB). Each chunk's id is a hash of its source, design, position and text. Vectors are saved batch by batch, and only chunks whose id has no saved vector are embedded, so re-running `main.py index` costs nothing.

| Design | Reg 2019/947 | Reg 2019/945 | EASA AMC/GM | Total |
|---|---|---|---|---|
| `w150` (150 words) | 184 | 192 | 168 | **544** (+58 from Reg 2021/664) |
| `w400` (400 words) | 94 | 94 | 95 | **283** |

## 4. Test set

32 questions in `eval/questions.csv`: **20 single**, **6 multi** (two passages) and **6 unanswerable**.

Examples:
- *Single* (q05): "How far from residential areas must I stay when flying in subcategory A3?" Expected answer: `Reg 2019/947, UAS.OPEN.040`, at least 150 m horizontally from residential, commercial, industrial or recreational areas.
- *Multi* (q21): "I fly a C2 drone in A2: how close can I get to people with low speed mode, and how fast can it go in that mode?" Expected answer: `Reg 2019/947 UAS.OPEN.030` plus `Reg 2019/945 PART 3`, down to 5 m, with low-speed mode limited to 3 m/s.
- *Unanswerable* (q27): "How much does it cost to register as a UAS operator in Spain?" Fees are set nationally and are not in the corpus.

I wrote the 32 questions myself, working from a summary of the most important regulations. I covered the most restrictive topics and the ones pilots deal with daily. The unanswerable questions stay close to the topic: national fees, fines, UK rules, wind limits, U-space services and authorisation deadlines.

The test set has not changed since the first evaluation run (commit `08f7fe1`, 15 November 2026). Every later experiment in this report (the extra retrieval metrics, BM25 and the hybrid, the second judge pass and v2) used it as it is.

## 5. Retrieval

All metrics are over the 26 answerable questions and use the saved query vectors (`eval/query_vectors.json`), so comparing designs costs no embeddings. Every design searches only the three corpus documents; the 58 U-space chunks added for the demo (see [Adding a document](#adding-a-document)) are left out, because only the `w150` index has them. The metrics:

- **hit@k**: at least one expected passage (same source, location matching at a word boundary) is in the top k;
- **all@k**: every expected passage is in the top k. It differs from hit@k only for the 6 multi questions;
- **MRR@5**: the mean of 1 / rank of the first expected passage, counting 0 if none is in the top 5.

| Design | hit@1 | hit@3 | hit@5 | all@5 | MRR@5 | Words added to the prompt (top 5) |
|---|---|---|---|---|---|---|
| **`w150`** (150-word chunks) | **0.846** | **1.000** | **1.000** | 0.846 | **0.917** | **638** |
| `w400` (400-word chunks) | 0.808 | 0.962 | 1.000 | **0.885** | 0.894 | 1,236 |
| `bm25` (keywords only, `w150` chunks) | 0.462 | 0.654 | 0.731 | 0.615 | 0.562 | 627 |
| `w150+bm25` (hybrid) | 0.654 | 0.846 | 0.923 | 0.769 | 0.754 | 636 |

By question kind (`eval/retrieval.csv` has every column for every kind):

| Design | Single (20): hit@1 | Single: MRR@5 | Multi (6): hit@5 | Multi: all@3 | Multi: all@5 |
|---|---|---|---|---|---|
| `w150` | 0.850 | 0.925 | 1.000 | 0.167 | 0.333 |
| `w400` | 0.800 | 0.887 | 1.000 | 0.333 | 0.500 |
| `bm25` | 0.550 | 0.618 | 0.667 | 0.167 | 0.167 |
| `w150+bm25` | 0.650 | 0.758 | 1.000 | 0.167 | 0.333 |

**Chosen design: `w150`.** It is better at k = 1 and k = 3, ties at k = 5, ranks the first right passage higher (MRR@5 0.917 against 0.894), and adds about half as many words to each prompt. The price is multi-passage retrieval: `w400` returns both passages of a multi question more often (all@5 0.500 against 0.333 on the multi questions). I keep `w150` and accept that trade-off.

For a multi question, hit@k counts a hit if *either* expected passage is retrieved, which overstates retrieval for those 6 questions; all@k counts a hit only when every expected passage is in the top k. all@1 is 0 for every multi question by construction, since a chunk never spans two sections. At k = 5, `w150` finds both passages for 2 of 6 (q24, q26) and `w400` for 3 of 6 (q21, q22, q24). With `w150` the top 5 misses `PART 3` in q21, `UAS.OPEN.070` in q22, `PART 16` in q23 and `Article 14` in q25.

**Hybrid search, tested and rejected.** I also tried adding a keyword search. The search the system uses compares meanings, so a question and a rule can match even when they use different words. Keyword search (BM25) only counts the words they share. On its own, keyword search found a right passage in the top 5 for only 19 of the 26 questions (hit@5 0.731), because pilots ask in everyday words and the rules are written in legal language. Combining the two searches was worse than the meaning search alone on every metric: the right passage ended up lower in the list (MRR@5 0.754 against 0.917). Testing it cost nothing, because it reused the saved embeddings, and `w150` with meaning search stays. (Technical details: BM25 with k1 = 1.5 and b = 0.75 over source, location and text; the two rankings were combined by reciprocal rank fusion, with k = 60, over the top 50 of each.)

## 6. MCP server

`server.py` loads the committed index and never re-embeds the corpus. Both tools run the code in `index.py`.

**`search(query)`**: "Search the EU drone (UAS) rules: Regulation 2019/947 (how drones may be flown: open/specific/certified categories, A1/A2/A3 subcategories, operator registration, remote pilot competency, operational authorisations, standard scenarios), Regulation 2019/945 (drone classes C0-C6, manufacturer duties, product requirements, remote ID) and EASA's AMC/GM guidance to Part-UAS. Use it for any question about operating, buying or building a drone in the EU. Returns the 5 most relevant passages. Each one starts with the exact citation to copy, [source, location] (article, UAS point or AMC/GM heading), and its document's version."

One search result as the v1 evaluation run received it (q05, third of five passages; the text is shortened with "…"):

```text
[3] Reg 2019/947, UAS.OPEN.040 UAS operations in subcategory A3 (score 0.781)
UAS operations in subcategory A3 shall comply with all of the following conditions: (1) be conducted
in an area where the remote pilot reasonably expects that no uninvolved person will be endangered …
(2) be conducted at a safe horizontal distance of at least 150 metres from residential, commercial,
industrial or recreational areas; …
```

From v2 on (section 9), the same passage starts with the citation to copy and the version. The only bracket the model sees is the citation itself, not a passage number, and the version note is in the retrieved text:

```text
Passage 3 (score 0.781). Cite as: [Reg 2019/947, UAS.OPEN.040 UAS operations in subcategory A3]. Version: consolidated text of 4 April 2022.
```

If the search fails (no API key, network or quota), the tool returns an MCP error that says why, so the agent sees the cause instead of a crashed server.

**`add_document(path)`**: "Add a local document (.pdf, .html or .txt) to the drone-rules index so search can find it. The file is extracted, chunked and embedded with the same pipeline as the corpus. The source name is the file name. If that file is already indexed with identical content nothing happens; if its content changed, the old chunks are replaced. Returns what was done and how many chunks were added."

**Already indexed?** `add_document` imports the pipeline from `index.py` and uses the file name as the source. If chunks with that source already exist and their `file_hash` equals the SHA-256 of the file, nothing happens ("already indexed with the same content"). If the content changed, the old chunks are deleted and the file is re-indexed, so an updated document never sits next to its stale version. New chunks go into the chosen `w150` index only, and only chunks without a saved vector are embedded. The same file under a different name would be indexed twice; the name is the identity. The tests in `tests/test_server.py` cover a missing file, an unsupported type, a re-add with the same content and a re-add with changed content.

## 7. Agents

### Subagent

`.claude/agents/corpus-researcher.md`, limited to `mcp__corpus__search`:

```text
You research EU drone rules using only the `search` tool.
- Search first, every time. If the results don't answer the question, search again with other words (max 3 searches).
- Answer only from the returned passages. No outside knowledge, no national rules.
- Cite every claim as `[source, location]`, copied exactly from the search result.
- If the passages don't answer it, reply "The corpus does not cover this." and stop.
- Keep it short: a direct answer in a few sentences or bullets.
```

**Transcript from Claude Code** (CLI 2.1.330 in headless mode, run on 23 November 2026 from a clean clone of this repo; the `corpus` server loaded from `.mcp.json`). Passage texts are left out below; `eval/subagent_transcript.txt` has the complete log, nothing shortened.

```text
$ claude -p "Use the corpus-researcher subagent to answer this question: Do I need to register a 300 g drone to fly it in the open category?" --allowedTools "Agent,Task,mcp__corpus__search"
  (Claude Code 2.1.330, model claude-opus-5-5; MCP server "corpus" from .mcp.json: connected)

● Agent(subagent_type="corpus-researcher")
  prompt: "Question: Do I need to register a 300 g drone to fly it in the open category (EU rules, Regulations 2019/947 and 2019/945)? …"
  ⎿ mcp__corpus__search(query="UAS operator registration open category MTOM 250 g kinetic energy 80 J sensor personal data toy")
  ⎿ mcp__corpus__search(query="operator registration number displayed on unmanned aircraft")
  ⎿ mcp__corpus__search(query="C1 class remote pilot online training theoretical knowledge examination subcategory A1")
     results for "UAS operator registration open category …": [1] Reg 2019/947, Article 14 (0.843); [2] Reg 2019/947, Article 14 (0.816); [3] Reg 2019/947, PART A UAS OPERATIONS IN THE ‘OPEN’ CATEGORY (0.816); [4] Reg 2019/947, ANNEX (0.804); [5] Reg 2019/947, Article 4 (0.797) (passage text omitted)
     results for "operator registration number displayed o…": [1] Reg 2019/947, Article 14 (0.709); [2] Reg 2019/947, Article 14 (0.706); [3] Reg 2019/945, PART 2 Requirements for a class C1 Unmanned aircraft system (0.701); [4] Reg 2019/947, Article 14 (0.694); [5] Reg 2019/945, Article 40 (0.691) (passage text omitted)
     results for "C1 class remote pilot online training th…": [1] Reg 2019/947, UAS.OPEN.020 UAS operations in subcategory A1 (0.819); [2] Reg 2019/947, UAS.OPEN.020 UAS operations in subcategory A1 (0.813); [3] Reg 2019/947, ANNEX (0.796); [4] Reg 2019/947, UAS.OPEN.030 UAS operations in subcategory A2 (0.782); [5] Reg 2019/947, PART A UAS OPERATIONS IN THE ‘OPEN’ CATEGORY (0.782) (passage text omitted)
  ⎿ mcp__corpus__search(query="class C0 MTOM less than 250 g; class C1 MTOM less than 900 g; subcategory A3 remote pilot training")
     results for "class C0 MTOM less than 250 g; class C1 …": [1] Reg 2019/947, UAS.OPEN.040 UAS operations in subcategory A3 (0.852); [2] Reg 2019/947, UAS.OPEN.020 UAS operations in subcategory A1 (0.848); [3] Reg 2019/947, UAS.OPEN.040 UAS operations in subcategory A3 (0.837); [4] Reg 2019/945, PART 4 Requirements for a class C3 Unmanned aircraft system (0.837); [5] Reg 2019/947, UAS.OPEN.020 UAS operations in subcategory A1 (0.832) (passage text omitted)
  ⎿ corpus-researcher report:
    **Yes. A 300 g drone flown in the open category requires you, the operator, to register.** It is over the 250 g threshold, so its class, its camera and any other feature do not change that.

    **(1) The Article 14 registration triggers**
    - In the open category, UAS operators must register when they fly an unmanned aircraft that (i) has an MTOM of 250 g or more, or could transfer more than 80 J of kinetic energy to a person on impact, or (ii) "is equipped with a sensor able to capture personal data, unless it complies with Directive 2009/48/EC" [Reg 2019/947, Article 14].
    - Any drone flown in the specific category triggers registration, whatever its mass [Reg 2019/947, Article 14].
    - Some of the terms you asked about are not in the returned text:
      - The Article 14 passage names only "Directive 2009/48/EC". It does not use the word "toy".
      - It says "personal data" but does not mention GDPR.
    - A 300 g drone already meets criterion (i), so the camera and toy questions don't affect it.

    **(2) Operator vs. drone, and certified drones**
    - Registration is for the operator, not the aircraft. Operators register in the Member State where they live (natural persons) or have their principal place of business (legal persons). An operator cannot be registered in more than one Member State at a time [Reg 2019/947, Article 14].
    - Member States issue a unique registration number for operators and for any UAS that requires registration [Reg 2019/947, Article 14].
    - Drones whose design is subject to certification are the exception. Their owner must register the aircraft itself, with a nationality and registration mark that follows ICAO Annex 7 [Reg 2019/947, Article 14].

    **(3) Does the class matter for a 300 g drone?**
    - No. Article 14 bases registration on mass, energy and sensor, not on class [Reg 2019/947, Article 14].
    - Class does decide which subcategory you can fly in. A1 is open to C0 and C1 drones (C1 needs active, up-to-date direct remote ID and geo-awareness). Privately built drones only qualify for A1 if they are under 250 g and slower than 19 m/s [Reg 2019/947, UAS.OPEN.020 UAS operations in subcategory A1].
    - The returned passages do not give the C0 and C1 mass limits (under 250 g and under 900 g), so I can't confirm them from the corpus.

    **(4) Related obligations**
    - **Showing the number:** operators must display their registration number on every aircraft that meets the Article 14(5) conditions [Reg 2019/947, Article 14].
    - **Remote ID:** a C1 drone must let you upload the operator registration number and must broadcast it during flight [Reg 2019/945, PART 2 Requirements for a class C1 Unmanned aircraft system].
    - **Pilot competency, A1 with C1:** you need an online training course and an online theory exam. The exam has 40 multiple-choice questions and you need at least 75% to pass. It covers air safety, airspace restrictions, aviation regulation, human performance limitations, operational procedures, UAS general knowledge, privacy and data protection, insurance, and security [Reg 2019/947, UAS.OPEN.020 UAS operations in subcategory A1].
    - **Pilot competency, A3:** the same online training and exam, plus familiarity with the manufacturer's instructions [Reg 2019/947, UAS.OPEN.040 UAS operations in subcategory A3].
    - **A2:** this also requires a certificate of remote pilot competency [Reg 2019/947, UAS.OPEN.030 UAS operations in subcategory A2].

    **Not covered by the corpus:** the exact C0 and C1 class mass limits, any "toy" wording, any mention of GDPR, and national procedures or fees for registering.

● Claude Code answer:
  **Yes. You have to register to fly a 300 g drone in the open category.** I checked this with the corpus-researcher agent against EU Regulations 2019/947 and 2019/945.

  **Why:** Under Article 14 of Reg. 2019/947, you must register if your drone:
  - weighs 250 g or more (maximum take-off mass), or could hit a person with more than 80 J of energy, **or**
  - has a sensor that can capture personal data, such as a camera, unless it meets the EU Toy Safety Directive (2009/48/EC).

  A 300 g drone is over the 250 g limit, so you must register whether or not it has a camera.

  **Key points:**
  - **You register, not the drone.** You register as the *operator* in the EU country where you live, or where your business is based, and only in one country at a time. You get one registration number that covers all your drones. The exception is drones whose design has to be certified, which are registered as aircraft.
  - **Put your number on the drone.** It must be shown on every drone that needs registration. If the drone is class C1, you also upload the number so the drone broadcasts it in flight (remote ID).
  - **The drone's class decides where you can fly, not whether you register.**
    - A C1 drone can fly in subcategory A1.
    - A home-built drone can only fly in A1 if it is under 250 g and slower than 19 m/s.
  - **You also need pilot training.**
    - For A1 (with a C1 drone) or A3: an online course and an online exam with 40 multiple-choice questions, pass mark 75%.
    - For A2: you also need a certificate of remote pilot competency.

  **Not in the regulations:** how to register and what it costs. That depends on your country's aviation authority, for example AESA in Spain. The searched text also didn't give the exact C0 and C1 weight limits.

  (2 turns, 28.7 s, $0.49 of Claude usage; the subagent made 4 search calls)
```

The subagent made 4 searches, although its instructions allow at most 3. In Claude Code that limit is only an instruction, while `agent.py` enforces it with middleware. The subagent's report cites the regulation for each rule and lists what the corpus does not cover. The main session's closing answer adds details that are not in the passages: "such as a camera", the name "EU Toy Safety Directive" (the passage names only Directive 2009/48/EC, as the subagent pointed out) and "AESA in Spain".

### Harness and guardrails

`agent.py` is a LangChain `create_agent` on `gemini-3.1-flash-lite` (temperature 0). It gets its tools from `server.py` over MCP and uses `AGENTS.md` as the system prompt. The rules are: search before answering (at most 3 searches, and since v2 again for any part of a multi-part question the passages don't cover); answer only from the passages; cite every claim as `[source, location]` (since v2: copy the text after "Cite as:", one citation per bracket); start with "The corpus does not cover this." when the passages don't answer; no national rules; mention the corpus version when dates matter; only add documents when the user asks with a path; be short.

- **Approval step:** a `wrap_tool_call` middleware intercepts every `add_document` call and asks `Allow? [y/N]` in the terminal. With no terminal (evaluation, `check.py`) the answer is no, and the agent receives "The user did not approve adding this document."
- **Call limits:** at most 6 model calls and 3 `search` calls per agent run. A 4th search is blocked and the agent gets "Tool call limit exceeded" (q23 requested 4; 3 ran). The citation retry is a second run with fresh limits.
- **Extra guardrail, citation check:** every `[source, location]` in the answer must match a passage that `search` returned in *this* run, with the same source and a location that matches at a word boundary. If any citation fails, the agent is told which ones and gets one retry; if the retry still fails, the answer is replaced by a refusal. Since v2, a bracket that holds several citations separated by `;` is split and each one is checked.

In the v1 run it fired on **10 of 32** questions. All 10 passed after the retry, and none had to be replaced by a refusal. Example, q25 ("My drone weighs 600 g. Do I need to register, and could it qualify as class C1?"): the first draft cited `[Reg 2019/947, Article 14(5)(a)(i)]` and `[Reg 2019/945, Part 2(1)]`. Those are finer than any location the index stores, so they could not be checked against a returned passage. The retry cited `[Reg 2019/947, Article 14]` and `[Reg 2019/945, PART 2 Requirements for a class C1 Unmanned aircraft system]`, which match.

Why the 10 first drafts failed, from the notes in `eval/answers.jsonl` (q17 had two problems):

| Problem in the first draft | Questions |
|---|---|
| Two citations in one bracket, `[A, x; B, y]` | 3 (q01, q05, q17) |
| The passage number used as the source, `[5, AMC1 UAS.OPEN.30(1)]` | 3 (q04, q14, q21) |
| A location finer than the stored one, `Article 14(5)(a)(i)` | 2 (q17, q25) |
| Two locations after one source | 1 (q28) |
| No citation at all: a refusal that didn't start with the exact phrase | 2 (q29, q31) |

Seven of the 11 problems are about the citation's format, not its content: two citations in one bracket, the passage number as the source, two locations after one source. The cheapest prevention is in the search output rather than in the prompt: start each passage with the exact citation to copy (`Cite as: [source, location]`) instead of a bare number, and let the check split `[A, x; B, y]` into two citations. v2 does both (section 9), and the check did not fire once in its 32 runs.

## 8. Evaluation

This section reports the v1 run (`eval/`), which my grades refer to; section 9 compares it with v2. The agent answered all 32 questions (`eval/answers.jsonl`).

**Code checks:**
- *refused*: the answer starts with "The corpus does not cover";
- *citations valid*: every citation matches a returned passage;
- *retrieved expected*: at least one expected passage was returned.

Refusals are graded in code: correct if the question is unanswerable, wrong otherwise.

**LLM judge** (same Gemini model, temperature 0, JSON output). It grades the 26 answers to answerable questions that are not refusals. It sees the question, the reference answer, the retrieved passages and the answer, and grades two things:
- *correct* = 1 if the answer states the same rule as the reference (extra correct detail is fine); 0 if it contradicts the reference, misses the key point, or refuses although the reference gives an answer.
- *supported* = 1 if every factual claim appears in the retrieved passages; 0 if any number, condition or exception is not in them, even if it is true.

### Results

| Outcome | Single (20) | Multi (6) | Unanswerable (6) | **All (32)** |
|---|---|---|---|---|
| Correct | 17 | 4 | – | **21** |
| Unsupported | 3 | 1 | – | **4** |
| Wrong | 0 | 1 | – | **1** |
| Wrong refusal | 0 | 0 | – | **0** |
| Correct refusal | – | – | 5 | **5** |
| Answered an unanswerable question | – | – | 1 | **1** |

**Retrieval inside the agent runs** (the *retrieved expected* check, on the agent's own search queries): at least one expected passage was retrieved for 25 of the 26 answerable questions, and every expected passage for 22. q04 retrieved none of its expected passages and answered from the EASA guidance on the same rule (`AMC1` and `GM1 UAS.OPEN.30(1)`). q21, q23 and q26 each missed one of their two passages, so only 3 of the 6 multi questions (q22, q24, q25) had both.

With 32 questions every rate is uncertain, so each comes with a 95% Wilson interval (`eval/summary.json`, `analysis.rates_wilson95`):

| Rate | Value | 95% interval |
|---|---|---|
| Handled correctly (correct answers + correct refusals) | 26 / 32 = 0.812 | 0.647–0.911 |
| Correct, of the 26 answerable | 21 / 26 = 0.808 | 0.621–0.915 |
| Unsupported, of the 26 answerable | 4 / 26 = 0.154 | 0.061–0.335 |
| Refused, of the 6 unanswerable | 5 / 6 = 0.833 | 0.436–0.970 |
| Citations valid | 32 / 32 = 1.000 | 0.893–1.000 |

### Agreement with my grades

I graded 20 answers myself (q01–q20, `eval/human_labels.csv`).

| | Agreement with the judge | Cohen's kappa |
|---|---|---|
| *correct* | **100%** (20 / 20) | undefined |
| *supported* | **85%** (17 / 20) | 0.00 |

All 20 are single-passage questions. The three disagreements are q07, q08 and q10. I graded them *supported*. The judge graded them *unsupported* because of the closing sentence naming the corpus versions, which comes from AGENTS.md rule 6 rather than from a retrieved passage. In my grading I treat that sentence as a disclaimer required by rule 6, not as a factual claim, so it does not make an answer unsupported. I applied this to all 20 answers; the judge applies the rubric literally, but only to 4 of the 25 answers that contain the note.

Kappa measures agreement beyond chance. For *correct* it is undefined: the judge and I gave all 20 answers a 1, so there is no variation to agree on. For *supported* it is 0.00: I gave all 20 a 1, so 85% is exactly the agreement that chance alone gives when the judge says 1 for 17 of 20. All 20 are single-passage questions the judge marked correct, so these figures cannot show whether the judge catches a wrong answer. The one wrong answer (q26) and the multi and unanswerable questions are in q21–q32, which I have not graded; `eval/grading_sheet.md` lists them without the judge's verdicts.

All four "unsupported" answers (q07, q08, q10 and q21) were flagged only for the version sentence that AGENTS.md rule 6 adds. I kept rule 6, the judge rubric and the strict refusal check unchanged. The aim of the evaluation is to show how the system behaves, not to raise its score: strict rules that produce both positive and negative cases explain more than rules changed until every case passes.

### How far the judge can be trusted

- **Self-preference.** The judge is the same model as the agent (`gemini-3.1-flash-lite`), so it may favour answers written the way it writes.
- **Inconsistent on the version sentence.** The sentence is in 27 of the 32 answers and in 25 of the 26 judged ones. The judge marked only 4 of those 25 unsupported (q07, q08, q10, q21).
- **Audit of all 26 verdicts** (`eval/judge_audit.md`): every claim in each answer was checked against the retrieved passages and the reference. Besides the inconsistency above, one reason is factually wrong (q21: it says the answer cites Regulations 2019/947 and 2019/945, which "were not provided"; the answer cites only EASA `AMC1 UAS.OPEN.30(1)`, the two regulations are named only in the version sentence, and Reg 2019/945 `PART 2` and `PART 3` were retrieved). Two verdicts are disputable: q23 is marked correct although it gives the STS-01 ground-speed limit instead of the C5 low-speed limit in the reference, and q15 is marked supported although it glosses "do not comply with Delegated Regulation (EU) 2019/945" as "without a class label". No other verdict conflicts with its evidence.
- **Stability.** A second pass over all 26 judged answers (same model and prompt, temperature 0, eight days after the first; `eval/judge_rerun.jsonl`) changed no verdict: 0 of 26 flipped. The judge is reproducible, so its inconsistency on the version sentence is systematic, not noise: both passes flag the same 4 answers.

### Refusals and the version note

- **Refusals.** Five of the six unanswerable questions were refused with the exact phrase (q27–q31). q32 was refused in other words ("The corpus does not specify a set number of days…"), which the prefix check does not count; see Failures. Two answers to answerable questions refuse part of the question inside the answer: q23 says the corpus does not give the C5 low-speed limit, and q26 says the rules don't cover what people taking part must do.
- **Version note.** Rule 6 asks for a note on the corpus versions when the answer depends on dates or transition periods; the agent added one to 27 of the 32 answers, including answers that do not depend on dates, such as q05 (150 m from residential areas in A3). That note is the whole difference between my *supported* grades and the judge's.

### Adding a document

**Unanswerable question (q31):** "What services must a U-space service provider offer to drone operators?"
**Document added:** `eval/extra/reg_2021_664_u-space.html`, Commission Implementing Regulation (EU) 2021/664 on a regulatory framework for the U-space (58 chunks).

- **Before:** "The corpus does not cover this."
- **After:** the four mandatory services (network identification, geo-awareness, UAS flight authorisation and traffic information), each cited to `[reg_2021_664_u-space.html, Article 3]`, plus Article 7 on providing them in all phases of the operation. The full answer is in `eval/add_document_demo.md`.

These 58 chunks are now part of the committed `w150` index, so q31 would be answerable if the agent were re-run. The evaluation results above use the answer from before the document was added. The retrieval evaluation leaves these chunks out; with them included, the dense designs' hit@k, all@k and MRR@5 are the same.

## 9. Failures and decision

### Failures

| Question | Kind | Outcome | Cause |
|---|---|---|---|
| q07 | single | unsupported | unsupported claim |
| q08 | single | unsupported | unsupported claim |
| q10 | single | unsupported | unsupported claim |
| q21 | multi | unsupported | unsupported claim |
| q26 | multi | wrong | retrieval miss |
| q32 | unanswerable | answered unanswerable | bad test question |

| Cause | Count |
|---|---|
| Unsupported claim | 4 |
| Retrieval miss | 1 |
| Bad test question | 1 |
| Wrong answer from the right passage | 0 |
| Wrong refusal | 0 |

What each failure shows:
- **q07, q08, q10 and q21:** the core facts are cited to the right passages. The sentence the judge flagged is the closing version note that AGENTS.md rule 6 asks for. By my grading convention that note is not a factual claim, so these four are failures for the judge, not real errors.
- **q26:** the agent searched once, with its own query, and `UAS.OPEN.050` point (7) (everyone involved in an A2 or A3 operation must be informed of the risks and explicitly agree) was not among the results. The agent then said the rules don't cover that part. With the question text as the query, the `w150` retrieval evaluation does return `UAS.OPEN.050` in the top 5. Searching once is the norm: 29 of the 32 runs made a single search.
- **q32:** the agent replied "The corpus does not specify a set number of days…" and cited `UAS.SPEC.040`, which says the authority issues the authorisation "without undue delay". The code only counts answers starting "The corpus does not cover" as refusals. I classify it as a bad test question: the corpus does answer it (no fixed number of days, only "without undue delay"), so it should not have been labelled unanswerable.

### What to fix first

1. **The test set.** I would add harder, more complex questions (several rules at once, conditions and exceptions) to push the system to its limits and find the limitations it would have in real use. 32 questions, most of them answered correctly, don't show where it breaks.
2. **Key term definitions.** The answers don't define key terms before giving the evidence (my notes on q02, q03, q07, q08 and q10). I would build a glossary of ambiguous terms, such as "open category", "toy" or "uninvolved person", so the agent detects them and gives their definition, and the pilot can interpret the rule.
3. **A more trustworthy evaluation.** I graded 20 answers, all single-passage questions. I would grade the rest thoroughly and ask a professional, such as a drone instructor or an aviation lawyer, to grade more answers. Time constraints prevented this here.

### v2: testing fixes for the failures in the table

After this analysis, a second version targeted the failure modes in the table, keeping the test set, the model, rule 6, the judge rubric and the strict refusal check unchanged (commit `99dfbf4`, details in `eval/v2/README.md`):
- `search` starts each passage with the citation to copy and the document's version (section 6), so the version note is in the retrieved text and the only bracket in each header is the citation, not a passage number;
- AGENTS.md asks for another search when a multi-part question isn't fully covered, and for one citation per bracket;
- the citation check splits `[A, x; B, y]` and checks each citation.

v2 answered all 32 questions on the same three documents and was judged with the same rubric (`eval/v2/`):

| | v1 | v2 |
|---|---|---|
| Correct | 21 | 26 |
| Unsupported | 4 | 0 |
| Wrong | 1 | 0 |
| Correct refusal | 5 | 6 |
| Answered an unanswerable question | 1 | 0 |
| Handled correctly (95% interval) | 26 / 32 (0.647–0.911) | 32 / 32 (0.893–1.000) |
| Citations valid | 32 / 32 | 32 / 32 |
| Citation check fired | 10 | 0 |
| Searches (runs with a single search) | 38 (29) | 35 (29) |
| Multi questions with both passages retrieved in the run | 3 of 6 | 5 of 6 |
| Tokens per question, mean / median | 4,367 / 3,294 | 3,534 / 3,345 |

Six questions changed, all from a failure to a pass, and none the other way:
- q07, q08, q10 and q21 are now *supported*: the version note the judge flagged is in the retrieved text.
- q26 now names the consent rule: its single search, worded slightly differently ("…operator ensure people taking part" instead of "…operator requirements for people taking part"), returned `UAS.OPEN.050`. The multi-part rule did not make the agent search more (29 of the 32 runs still made one search), so this fix came from the query wording, not from the rule.
- q32 now starts with "The corpus does not cover", so the code counts it as a correct refusal. The content is the same ("without undue delay"), so by my reading it is still a bad test question.

What v2 does not show: the judge is still the same model, it is a single run on the same 32 questions, and its seconds are not comparable with v1, because the Gemini API was overloaded during the v2 run (median 45.4 s, inflated by retry waits). v2 also does none of the three fixes above, which remain to be done.

By the rule I set before running it (keep v2 only if it improves with no regression and `check.py` passes), v2 is the shipped configuration: `check.py --evaluate` passed on a fresh clone. The tables before this subsection stay the v1 results, which my grades refer to.

### Cost and latency

Per question, over the 32 runs in `eval/answers.jsonl` (agent tokens; the judge's tokens were not logged):

| | Mean | Median |
|---|---|---|
| Tokens (input + output) | 4,367 (4,057 + 310) | 3,294 |
| Seconds | 55.6 | 15.3 |

Three runs took over 100 s: q04 (802 s), q10 (237 s) and q03 (105 s). They are most likely free-tier rate-limit waits, which are not logged, so they cannot be subtracted exactly. Without those three runs the mean is 21.9 s; the median is the typical case. The evaluation run made 37 searches (38 requested, 1 blocked), each one query embedding.

**In money.** The project ran on the free tier, which costs nothing within its daily limits. At the paid-tier prices of the Gemini Developer API ([pricing page](https://ai.google.dev/gemini-api/docs/pricing), checked 23 November 2026: Gemini 3.1 Flash-Lite $0.25 per million input tokens and $1.50 per million output tokens; Gemini Embedding 2 $0.20 per million tokens), the mean question costs $0.001479 in model tokens plus at most $0.0000033 for its query embeddings (counting 2 tokens per word, since their tokens are not logged). At the ECB reference rate of 1.0990 USD per euro (20 November 2026) that is **€0.0013 per question, or €1.35 per 1,000 questions**. v2 costs €1.08 per 1,000 at the same prices: it needs no citation retries, although every passage now carries a version line.

### Decision

**Would I let users rely on it?** Yes: as a way to find and read the EU rule that applies, not as a replacement for the pilot's judgement. On the 32 questions, 26 were handled correctly (21 correct answers and 5 correct refusals; 0.812, 95% interval 0.647–0.911), and every citation pointed to a passage that was actually retrieved. The four "unsupported" answers were flagged only for the version note. The one real error was q26, which left out the consent rule for people taking part in A2; q32 is a test-question problem (see Failures). The safeguard is the pilot. They have the knowledge the assistant lacks to interpret ambiguous terms, and each answer cites the article they can open and check before flying.

## Limitations

- **Small test set.** 26 answerable questions, 6 multi and 6 unanswerable give wide intervals (the refusal rate of 5/6 has a 95% interval of 0.436–0.970). A difference of one or two questions between two designs is within noise.
- **One author.** I wrote the questions, the reference answers and the 20 grades, and nobody else checked them.
- **My grades cover only single-passage questions**, all 20 marked correct by the judge, so the agreement figures cannot show whether the judge catches wrong answers.
- **The judge** is the same model as the agent, is inconsistent on the version sentence (4 of 25, the same 4 in both passes) and gives one wrong reason (q21).
- **Refusals are detected by a fixed opening phrase**, which misses a refusal in other words (q32) and partial refusals inside an answer (q23, q26).
- **Corpus versions.** Regulation 2019/947 as consolidated on 4 April 2022, Regulation 2019/945 as consolidated on 9 August 2020 and EASA's Issue 1 of 2019. Later amendments and guidance issues are not in the corpus, so an answer can be out of date; rule 6 makes the agent say which versions it used.
- **The committed index includes the U-space document** added for the demo, so re-running the agent today would answer q31, which the test set labels unanswerable.
- **Latency was measured on the free tier**, where rate-limit waits are part of the time and are not logged; the judge's tokens are not in the cost.
- **v2 is one run**, judged by the same model, and its latency was measured while the API was overloaded.
- **The subagent's 3-search limit** is only an instruction in Claude Code (it made 4 searches); only `agent.py` enforces its limits.
- **Re-indexing a changed source.** `main.py index` embeds chunks it has not stored yet but does not delete old ones, so if a source's text changed, its old and new chunks would sit side by side. `add_document` replaces them; `main.py index` does not.

## Reproducibility

```bash
uv sync                                    # Python 3.12 and the locked dependencies (uv.lock)
cp .env.example .env                       # paste your key: server.py, started over MCP, only sees .env
uv run python main.py index                # embeds only chunks without a saved vector: none, if the sources are unchanged
uv run python main.py ask "your question"  # one agent run
uv run python main.py evaluate             # rebuilds every file in eval/ from the cached results, no API calls
uv run python check.py                     # the course's checker
uv run pytest                              # offline tests, including the numbers in this report
uv run ruff check .
```

Which run produced which numbers:

| Numbers | Produced by | Code |
|---|---|---|
| Answers, tokens, seconds, citation-check notes (`eval/answers.jsonl`), judge verdicts (`eval/judge.jsonl`), query vectors | the v1 evaluation run, agent and judge on Gemini | commit `08f7fe1`, 15 November 2026 |
| Retrieval tables (`eval/retrieval.csv`) | `main.py evaluate` from the saved query vectors and `index/` | the submitted commit, offline |
| Outcomes, rates and intervals, kappa, refusal and version-note counts, guardrail patterns, cost (`eval/summary.json`, `eval/failures.csv`) | `main.py evaluate` from the cached v1 results and `eval/human_labels.csv` | the submitted commit, offline |
| My grades and notes (`eval/human_labels.csv`) and failure causes | me | commits `0b00c9a` and `525a3a0` |
| Second judge pass (`eval/judge_rerun.jsonl`), `judge_stability` in `eval/summary.json` | `evaluate.py --rejudge`, same rubric and prompt as v1, on 23 November 2026 | judge prompt and rubric of `08f7fe1`, retry settings of `2edbfbc` |
| Judge audit (`eval/judge_audit.md`) | Claude, reading each verdict against its evidence | commit `1651be2` |
| v2 answers and verdicts (`eval/v2/answers.jsonl`, `eval/v2/judge.jsonl`) | `EVAL_DIR=eval/v2` run of `evaluate.py` on 23 November 2026, on the three corpus documents | agent at commit `c2d0ff7` |
| v2 summary (`eval/v2/summary.json`, `failures.csv`, `retrieval.csv`) | the same command, from the cached v2 results | the submitted commit, offline |
| Subagent transcript (`eval/subagent_transcript.txt`) | Claude Code 2.1.330, `claude -p` | run on commit `be2c828` |

Answers and verdicts are cached, so `main.py evaluate` only calls Gemini for questions that have no cached answer or verdict; delete a line in `eval/answers.jsonl` or `eval/judge.jsonl` to redo it. `uv run python evaluate.py --rejudge` judges every answer a second time into `eval/judge_rerun.jsonl` (26 judge calls), and `EVAL_DIR=<folder> uv run python evaluate.py` writes a complete new run into another folder without touching the v1 results.

## AI use

AI wrote the code.

Claude (Anthropic) was also used to review the repository, to build a grading page and to walk me through the answers one by one (with neutral summaries of each answer and its passages) while I gave my own grades and failure causes, to make `evaluate.py` keep the hand-filled `cause` column when it re-runs, and to draft the factual parts of this report from the files in `eval/` and `index/`. Claude also turned my notes for the analysis sections (test set, evaluation, failures, decision) into sentences. At my request it produced the subagent transcript by running the Claude Code CLI on a clean clone of this repo with my Gemini key, and it rewrote the ship decision and the evaluation framing from my earlier notes, so they agree with the use case.

In a final review pass, Claude:
- added all@k, MRR@5 and per-kind rows to the retrieval evaluation, made every design search the same three documents, and tested BM25 and a BM25+dense hybrid as further designs, all from the saved vectors;
- added the analysis in `eval/summary.json` (outcomes by kind, Wilson intervals, Cohen's kappa, refusal and version-note counts, why the citation check fired, cost at paid-tier prices), and wrote the paragraphs of this report that present it;
- audited the 26 judge verdicts (`eval/judge_audit.md`) and ran the judge a second time over all of them to measure its stability;
- made `index.py` skip a source it can't download, made `search` errors say why, and added offline tests (`tests/`, run with pytest) and a linter (ruff);
- built a grading sheet for q21–q32 without the judge's verdicts (`eval/grading_sheet.md`);
- built v2 (the citation header with the version, the multi-part search rule, the split citation check), ran it on all 32 questions into `eval/v2/`, and applied my adoption rule;
- re-ran `main.py index`, `main.py evaluate` and `check.py` on fresh clones, reordered this report along the brief, added the Limitations and Reproducibility sections, and added `tests/test_report_numbers.py`, which recomputes the numbers in this report from the committed files.

I wrote the test set myself and graded 20 answers myself. I chose the cause of each failure, the decision to keep rule 6 and the strict checks, the `w150` design, what to fix first and the ship decision.

I reviewed the analysis Claude added in the final review pass and had the hybrid-search paragraph rewritten in plainer words.
