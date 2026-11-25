# Assignment 3 Report

- **Name**: Nour Farhat
- **Student ID**: [19299
- **Group**: [BBADBA 5A]

## Use case

**Who asks:** ward nurses, junior doctors and pharmacists who need to check a fact about an anticoagulant (blood thinner) before acting: a dose adjustment, how long to stop a drug before surgery, what to do after a missed dose, how to reverse the effect, or whether the drug is contraindicated.

**What they do with the answer:** they give, hold or adjust a dose, or plan a procedure. The answer must cite the exact section of the official FDA label so they can check it in seconds.

**What a wrong answer costs compared with "I don't know":** anticoagulants have a narrow margin between preventing clots and causing bleeding. A wrong dose, a wrong interruption time or a missed contraindication can cause a major bleed or a stroke. "I don't know" only costs the time to open the full label or call pharmacy. So the system is built to refuse whenever the labels do not clearly answer.

## Corpus

Official FDA prescribing information (drug labels), downloaded as structured JSON from the openFDA drug label API. openFDA data is public domain (CC0; see https://open.fda.gov/terms/) and contains no personal data.

| Document | Drug | URL (DailyMed, by set id) | Label version / date | Licence | Words kept |
|---|---|---|---|---|---|
| ELIQUIS | apixaban | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=41a133ef-e461-48ad-8221-b735bdd0ec25 | v5, 2026-09-24 | Public domain (openFDA) | 16,355 |
| XARELTO | rivaroxaban | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=10db92f9-2300-4a80-836b-673e1ae91610 | v65, 2026-09-10 | Public domain (openFDA) | 21,210 |
| PRADAXA (capsules) | dabigatran | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=ba74e3cd-b06f-4145-b284-5fd6b84ff3c9 | v48, 2025-06-25 | Public domain (openFDA) | 14,832 |
| WARFARIN | warfarin sodium | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=61ab23a7-bc67-4777-854a-bf43c788a69a | v3, 2026-11-09 | Public domain (openFDA) | 7,776 |
| LOVENOX | enoxaparin | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5017a927-2a24-4f27-89f9-27c805bf7d59 | v33, 2026-05-28 | Public domain (openFDA) | 13,800 |
| **Total (indexed by `main.py index`)** | | | | | **73,973** |
| SAVAYSA (added later with `add_document`) | edoxaban | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=e77d3400-56ad-11e3-949a-0800200c9a66 | v28, 2025-07-10 | Public domain (openFDA) | 10,137 |

"Words kept" counts the clinical sections we index (see Ingestion). The labels are committed in `corpus/`, so a fresh clone never downloads a newer version that would need re-embedding.

## Ingestion

**Extract.** openFDA returns each label as JSON, with one field per label section (`dosage_and_administration`, `contraindications`, …). We keep 15 clinical sections (`config.SECTIONS`). We skip the HTML `*_table` fields (they duplicate the table text) and sub-keys such as `pregnancy`, which repeat text already in `use_in_specific_populations`.

**Clean.** Each section's list of strings is joined. Whitespace and bullet characters are normalised, and cross-references written `( 2.1 )` become `(2.1)`.

**Chunk.** Two designs, both from the same cleaned text:
- **sections:** a section arrives as one long string with its subsection headings inline ("2 DOSAGE AND ADMINISTRATION 2.1 Recommended Dose … 2.2 …"). We split it right before each heading of that section (regex `\s(?=2\.\d+\s+[A-Z])`), giving one chunk per subsection (2.1, 2.2, 8.6…). Subsections over 300 words are cut into equal parts, and heading-only pieces are dropped.
- **fixed:** 200-word windows with a 40-word overlap, ignoring the structure.

**Metadata on every chunk:** `source` (e.g. ELIQUIS), `location` (subsection, e.g. `2.3`, or `2.1;2.2` for a fixed window spanning two), `section` name, label `version`, `design`, and word count. Each chunk is stored with a citation header (`[ELIQUIS §2.3] (Dosage And Administration)`) and embedded with Gemini's document format (`title: ELIQUIS - Dosage And Administration | text: …`). Questions are embedded as `task: search result | query: …`.

**Number of chunks:** sections 414 (480 after adding SAVAYSA); fixed 484.

**Problems we fixed:**
1. **Inline subsection headings.** Splitting on any "number + capital letter" would also cut at doses like "2.5 Mg" or at cross-references. We only split on the current section's own numbering (`2.x` inside section 2), and normalise `( 2.1 )` cross-references first.
2. **Wrong document.** A plain openFDA search for `PRADAXA` returned the newest label, which is **PRADAXA Oral Pellets** (children 3 months to 12 years), not the adult capsules. We found this while writing the test set: questions about opening capsules and storage had no answer. We fixed the query to `dosage_forms_and_strengths:"150 mg capsules"` and re-indexed only PRADAXA. Unchanged chunks keep their saved vectors.

## Test set

`eval/questions.csv`: **30 questions: 18 single-passage, 7 multi-passage, 5 unanswerable**, across all five drugs. Questions are phrased the way a clinician would ask. Each `expected_location` was checked against the label text (the answer to q01, for example, appears in §2.1 and §8.6, so both are listed). Unanswerable questions are deliberately close to the topic: a drug not in the corpus (SAVAYSA), a head-to-head trial the labels do not contain, Spanish prices, adherence data, and ESC guidelines. A per-question grading criterion (`eval/grading_criteria.csv`) tells the judge what "correct" and "supported" mean for each question.

Two examples:
- **q01 (single):** *Under what conditions should the standard dose of Eliquis be reduced to 2.5 mg twice daily in patients with nonvalvular atrial fibrillation?* Expected ELIQUIS §2.1;8.6. Reference: 2.5 mg twice daily if at least 2 of age ≥ 80, weight ≤ 60 kg, serum creatinine ≥ 1.5 mg/dL.
- **q20 (multi):** *A patient remembers a missed anticoagulant dose four hours before their next scheduled dose on the same day. How would the recommended action differ depending on whether the patient takes Eliquis or Pradaxa?* Expected ELIQUIS §2.2 + PRADAXA §2.5. Reference: Eliquis, take it as soon as possible the same day; Pradaxa, skip it (not ≥ 6 hours before the next dose); never double.

## Retrieval

Hit rate on the 25 answerable questions (a hit = at least one top-k chunk covers an expected passage). "Both found" = share of the 7 multi questions with *both* passages in the top 5 for a single query.

| Design | hit@1 | hit@3 | hit@5 | multi: both found @5 | Words added to prompt (top 5) |
|---|---|---|---|---|---|
| fixed (200 words, 40 overlap) | 0.76 | **1.00** | **1.00** | 0.57 | 979 |
| sections | 0.64 | 0.92 | 0.96 | 0.57 | 915 |
| sections + hybrid (vector + BM25, Reciprocal Rank Fusion) | **0.88** | 0.92 | 0.96 | 0.57 | **902** |

**Chosen design: sections + hybrid.** It puts the right passage first most often (0.88 vs 0.76), adds the fewest words to the prompt, and cites one exact subsection that a clinician can check, rather than a 200-word window spanning two subsections. Fixed windows have the better hit@5 (1.00 vs 0.96). The one question they rescue is q21, and our guardrail turned that miss into a safe refusal (see Failures). Multi-passage questions only reach both passages in 57% of single queries, but the agent searches once per drug, so in practice 6 of 7 multi questions were answered correctly.

## Tools and subagent

`server.py` (MCP, stdio) exposes two tools. Their docstrings are the descriptions the model reads:

- **`search(query)`:** "Search the official FDA prescribing information (drug labels) of anticoagulants: ELIQUIS (apixaban), XARELTO (rivaroxaban), PRADAXA (dabigatran), WARFARIN and LOVENOX (enoxaparin), plus any label added later with add_document. Use it for any question about these drugs: indications, dosing and dose adjustments (renal/hepatic impairment, age, weight), switching between anticoagulants, stopping before surgery, contraindications, bleeding risk, reversal, drug interactions, pregnancy, overdose, storage. Ask one specific question per call (name the drug). Returns the 5 most relevant passages. Each passage starts with its citation tag, e.g. [ELIQUIS §2.2] … Cite answers with exactly these tags."
- **`add_document(path)`:** adds an openFDA label JSON from inside the project, using `index.py`'s own `chunk_file` and `embed_and_store` (imported, not copied). It refuses paths outside the project or non-JSON files.

**One search result** (q04, query *"Eliquis discontinuation before surgery elective high risk of bleeding timing"*), first of five passages:

> [ELIQUIS §2.3] (Dosage And Administration)
> 2.3 Temporary Interruption for Surgery and Other Interventions ELIQUIS should be discontinued at least 48 hours prior to elective surgery or invasive procedures with a moderate or high risk of unacceptable or clinically significant bleeding … Bridging anticoagulation during the 24 to 48 hours after stopping ELIQUIS and prior to the intervention is not generally required …

**Subagent** (`.claude/agents/corpus-researcher.md`): its only tool is `mcp__corpus__search`. Its instructions: search with a question naming the drug (one search per drug for comparisons), answer only from the results, cite every sentence with the passage's tag, copy doses exactly, reply "The corpus does not cover this." when the results don't answer, at most 6 sentences.

**Transcript from my editor:**

```
User: How long before a high-bleeding-risk surgery should Eliquis be stopped?

Copilot (agent: corpus-researcher): search
Completed with input: {
  "query": "For Eliquis (apixaban), how long before elective surgery or an invasive procedure with moderate or high risk of clinically significant bleeding does the FDA prescribing information say to discontinue it?"
}

Eliquis should be stopped **at least 48 hours before** elective surgery or an invasive procedure with moderate or high risk of clinically significant bleeding. [ELIQUIS §2.3]
```

<img width="372" height="501" alt="Screenshot 2026-11-25 at 15 58 33" src="https://github.com/user-attachments/assets/109c6f8e-426e-4281-8dbf-7075df38a379" />

```

## Adding a document

**When a document is already indexed:** `add_document` compares the label's version (set id + version + date) with what is stored. The same version means nothing is done and nothing is embedded. A different version means the old chunks are deleted and the new ones are stored.

**Unanswerable question:** q26, *"What is the recommended dose of Savaysa for an adult with nonvalvular atrial fibrillation and a creatinine clearance of 70 mL/min?"*. **Document added:** `corpus/extra/SAVAYSA.json` (edoxaban label, 66 chunks).

- **Before** (evaluation run): *"The corpus does not cover this. The Savaysa label is not available in the corpus to check the recommended dose, so please check the full prescribing information or consult a pharmacist."*
- **Adding it:** the agent asked *"The agent wants to run add_document({'path': 'corpus/extra/SAVAYSA.json'}). Allow? [y/N]"*. After approval, 66 chunks were embedded and the index grew from 414 to 480 chunks.
- **After:** *"The recommended dose of SAVAYSA for patients with nonvalvular atrial fibrillation and a creatinine clearance >50 to ≤ 95 mL/min is 60 mg taken orally once daily [SAVAYSA §2.1]."* (≈4,300 tokens, 11 s)
- **Adding it again:** *"SAVAYSA (… v28 (20250710)) is already indexed with 66 chunks. Nothing changed."*

## Harness and guardrails

`agent.py` is a LangChain `create_agent` on `gemini-3.5-flash-lite`. It starts `server.py` over MCP and wraps its two tools as LangChain tools. `AGENTS.md` is the system prompt; its rules, each with a reason, are: search first (one drug per search); answer only from search results; cite every claim with the exact tag; say exactly "The corpus does not cover this." when the results don't answer; copy numbers exactly with units and conditions; no patient-specific decisions; use `add_document` only when the user explicitly asks to add a file (never to answer a question); keep answers short.

1. **Approval step:** `HumanInTheLoopMiddleware` pauses before every `add_document` call and asks y/N in the terminal. With no human present (evaluation, `check.py`), it rejects. **It fired for real:** when I asked the Savaysa question, the agent tried to add the document by itself, against rule 7. The approval prompt stopped it until I answered, and I then tightened rule 7.
2. **Call limit:** `ToolCallLimitMiddleware(run_limit=6)`, so a confused agent cannot loop and burn the quota.
3. **Extra guardrail: citation check.** After the agent answers, code checks that every `[SOURCE §x]` tag it used was actually among the passages it retrieved, and that a non-refusal has at least one citation. Otherwise the answer is withheld and replaced by a refusal. **Case where it fired: q21.** The draft cited `[PRADAXA §2.2]`, which the search had not returned, so the answer was withheld (*"Guardrail: the draft answer cites passages that were never retrieved: [('PRADAXA', '2.2')]"*).

## Evaluation

`evaluate.py` runs the agent on all 30 questions and saves answers, verdicts and question vectors as it goes, so reruns only do missing work.

**Code checks (no LLM):** refusal detection ("does not cover"), and citation validity (every tag must have been retrieved). A refusal is graded by code: correct only for unanswerable questions, always supported. An answer to an unanswerable question is incorrect by code, and an invalid citation makes an answer unsupported by code.

**LLM judge rubric** (Gemini, JSON output, low thinking), plus my per-question criterion from `eval/grading_criteria.csv`:
- **correct = 1** if the answer gives the same key facts as the reference: same drug, same numbers with units and conditions (doses, CrCl thresholds, hours). A missing key condition, a wrong number or the wrong drug gives 0.
- **supported = 1** if every factual claim is found in the retrieved evidence (paraphrase allowed).

**Results** (`eval/evaluation_summary.json`, `eval/results_by_question_type.csv`):

| | Single (18) | Multi (7) | Unanswerable (5) | All (30) |
|---|---|---|---|---|
| Correct | 18 (100%) | 6 (85.7%) | 5 (100%) | **29 (96.7%)** |
| Supported | 100% | 100% | 100% | **100%** |

- Correct answers to answerable questions: **24 / 25**. Unsupported answers: **0**.
- Correct refusals: **5 / 5** (abstention accuracy 100%). Wrong refusals: **1** (q21).

**Agreement with the judge:** `eval/human_labels.csv` holds independent grades for all 30 answers, made without seeing the judge's verdicts. **Correctness: 100% agreement, Cohen's kappa 1.0. Supportedness: 100% agreement; kappa is undefined**, because both graders marked every answer supported, so there is no variation to correct for chance. Caveats: 6 of the 30 (the refusals) are graded by code, so agreement on those is automatic; and the annotations are AI-assisted (see `eval/about_human_labels.md` and AI use), so this compares two AI graders.

## Failures

| Cause | Count | Questions |
|---|---|---|
| Retrieval miss (ending in a safe wrong refusal) | 1 | q21 |
| Wrong answer from the right passage | 0 | |
| Unsupported claim | 0 | |
| Wrong refusal with the passage retrieved | 0 | |
| Bad test question | 0 | |

**q21** (*which of Xarelto and Pradaxa needs parenteral treatment first, and for how long?*): the needed passage, PRADAXA §2.2 (*"after 5 to 10 days of parenteral anticoagulation"*), was not in the top 5 for the hybrid design. The agent still wrote a correct draft from the other Pradaxa passages but cited §2.2, which it had not retrieved, so the guardrail withheld it. The fixed-window design does retrieve §2.2 for this question.

**A failure in my own evaluation code, found and fixed:** the first run reported 5 wrong refusals. In four of them (q10, q12, q22, q24), the agent had grouped several citations in one bracket (`[PRADAXA §2.5, PRADAXA §12.3]`). My citation parser read only one tag per bracket, so the guardrail wrongly blocked correct answers. After fixing the parser, the saved answers were re-checked (the guardrail is plain code, so no new API calls) and only the changed ones were re-graded.

**What to fix first:** retrieval for multi-passage questions. Give the search tool a `drug` filter (Chroma metadata `where`), so a "Pradaxa" query only searches the PRADAXA label, or retrieve more than 5 chunks per query. q21's passage was crowded out by Xarelto chunks.

## Decision

**Would I let users rely on it?** Yes, as a **fast, cited look-up tool for clinicians**, not as a decision-maker. On 30 questions it gave no wrong facts and no unsupported claims, answered 24 of 25 answerable questions correctly, and refused all 5 it could not answer. Its one failure was a refusal, not a wrong dose.

**For what:** checking dosing rules, interruption times, missed doses, contraindications and reversal agents in the five indexed labels.

**With which safeguards:** (1) every answer must carry section citations that the user can open; the citation guardrail blocks answers citing passages that were not retrieved. (2) It refuses rather than guesses. (3) A human approves any change to the corpus. (4) It does not make patient-specific decisions; the label is a reference and the prescriber stays responsible. Before real use, I would test on a much larger set (30 questions is small), verify the grades by a pharmacist, and re-index when labels are updated.

**Cost and latency per question** (30-question run, `gemini-3.5-flash-lite` + `gemini-embedding-2`, free tier): on average **4,004 tokens** and **6.1 seconds** (median 3,540 tokens and 4.9 s; slowest 25.2 s). Each search also uses one embedding call.

## AI use

[REVIEW AND EDIT THIS SECTION SO IT IS ACCURATE]

- **Claude (Anthropic):** wrote and debugged the code (`index.py`, `retrieve.py`, `server.py`, `agent.py`, `evaluate.py`, `config.py`), aligned it with the class RAG notebook, found the PRADAXA label problem, drafted the reference answers from the label text, produced the AI-assisted independent annotations in `eval/human_labels.csv` (documented in `eval/about_human_labels.md`).
- **ChatGPT:** used to polish the wording.
- **Me:** chose the use case and corpus, wrote the test questions and per-question grading criteria, ran the pipeline, chose the retrieval design, ran the add-document demo, and reviewed results.
