# Assignment 3 Report
 
- **Name**: Joao Paulo Tobar Prado
- **Student ID**: 19398
- **Group**: BBADBA 5A
## Use case
 
The assistant is for junior pharmacists who need to look up facts in FDA drug labels while helping customers: dosing, contraindications, interactions, pregnancy and counseling points. They use the answer either to reply to the customer at the counter or to decide that the question needs to go to the supervising pharmacist.
 
The costs of the two kinds of mistake are very different. A wrong dose or a missed interaction can harm a patient, while "I don't know" only costs a few minutes and a referral. A refusal is therefore far cheaper than a wrong answer, which is why rule 3 in AGENTS.md tells the agent to say when the labels don't cover a question.
 
I limited the corpus to FDA labels from openFDA because they are public, licensed CC0, contain no personal data and share one consistent section structure. I rejected two alternatives: an "equivalent medicine abroad" tool for travellers, because most of that data is proprietary, and mixing in EMA labels, which would have broken the single consistent structure.
 
I chose this use case because it is a setting where retrieval clearly beats a general chatbot. The answers already exist in an authoritative document, the label, but those documents are long: a prescription label can run to 25,000 words, which is too much to search by hand with a customer waiting. A junior pharmacist does not need the model's opinion. They need the exact label wording, quickly, with a citation they can check and show their supervisor. The use case also has a natural "I don't know": many counter questions (alcohol, grapefruit, combining two OTC painkillers) are not covered by the labels at all. That makes it a good test of whether the agent refuses instead of filling gaps from general knowledge, which is the behaviour that matters most when a wrong answer can harm someone.
 
## Corpus
 
The corpus has 14 indexed labels totalling about 145,600 words. A 15th label, Eliquis (about 20,300 words), is held back for the add-document demo. All labels come from the openFDA drug/label endpoint. `download.py` fetched them on 2026-11-17 and pinned each one by set_id and version. The licence is CC0 1.0 (https://open.fda.gov/license/).
 
| Document | Product (manufacturer) | Type | Label effective date | Words | Source URL |
|---|---|---|---|---|---|
| flanax | Flanax, naproxen sodium (Belmora LLC) | OTC | 2026-01-06 | 948 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2c099d45-f03a-4161-a6af-8fe5965f2748 |
| aleve | Aleve, naproxen sodium (Bayer HealthCare) | OTC | 2025-12-04 | 971 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1266393e-b55e-4e34-9710-0b87209f4158 |
| advil | Advil, ibuprofen (Haleon) | OTC | 2026-07-29 | 965 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=1f01c10a-9434-91a4-2ee4-352315a6b610 |
| tylenol | Tylenol Extra Strength, acetaminophen (Kenvue) | OTC | 2026-01-27 | 662 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=4961695d-72f3-533a-e063-6294a90a5a29 |
| naproxen | Naproxen (Granules Pharmaceuticals) | Rx | 2026-10-08 | 14,401 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=c1cb9bb9-fbae-5e5c-e053-2995a90a0d21 |
| celebrex | Celebrex, celecoxib (Viatris) | Rx | 2024-11-22 | 19,798 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2d6675e4-5859-4be2-8037-a20ce9f707aa |
| jantoven | Jantoven, warfarin sodium (Upsher-Smith) | Rx | 2026-10-28 | 11,900 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=19a69a72-ac5d-45d5-a94d-a5aaecbe4730 |
| plavix | Plavix, clopidogrel (Sanofi-Aventis) | Rx | 2025-05-30 | 9,841 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=de8b0b67-eb25-4684-83b5-7ad785314227 |
| amoxil | Amoxil, amoxicillin oral suspension (DirectRx) | Rx | 2025-01-22 | 4,658 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=ec7dd735-dc92-3d29-e053-2a95a90af549 |
| augmentin | Augmentin, amoxicillin/clavulanate (Allegis Holdings) | Rx | 2026-10-26 | 8,613 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=04a31a42-d79e-bbb4-e063-6394a90a63ee |
| zithromax | Zithromax, azithromycin (Pfizer) | Rx | 2026-07-24 | 15,783 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=db52b91e-79f7-4cc1-9564-f2eee8e31c45 |
| cipro | Cipro, ciprofloxacin (Bayer HealthCare Pharmaceuticals) | Rx | 2026-03-02 | 24,657 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=888dc7f9-ad9c-4c00-8d50-8ddfd9bd27c0 |
| bactrim | Bactrim, sulfamethoxazole/trimethoprim (Sun Pharmaceutical) | Rx | 2024-12-30 | 8,211 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=f59d0c04-9c66-4d53-a0e1-cb55570deb62 |
| prilosec | Prilosec, omeprazole magnesium (Covis Pharma) | Rx | 2024-03-19 | 24,200 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=b6761f84-53ac-4745-a8c8-1e5427d7e179 |
| eliquis (held back) | Eliquis, apixaban (E.R. Squibb & Sons) | Rx | 2026-08-17 | 20,321 | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=e9481622-7cc6-418a-acb6-c5450daae9b0 |
 
All labels were downloaded on 2026-11-17 under CC0 1.0. Set IDs and versions are in `corpus/manifest.csv`.
 
The corpus mixes two very different kinds of document. The four OTC labels (Flanax, Aleve, Advil and Tylenol) are short, about 1,000 words each. The ten prescription labels run from about 5,000 to 25,000 words. I originally wanted Naprosyn and Coumadin, but neither is in openFDA (both return 404), so the corpus uses generic naproxen from Granules and Jantoven (warfarin) instead. openFDA's own disclaimer says its data is not meant for clinical decisions, which is one more reason the assistant is a lookup aid for trainees and not a source of final clinical advice.
 
## Ingestion
 
Extraction is simple because openFDA delivers each label as JSON, with one field per label section, so no PDF parsing is needed. The cleaning step (`clean` and `CHAR_FIXES` in `index.py`) normalises whitespace and fixes odd characters.
 
Some sections are dropped before chunking: clinical_studies, spl_medguide, clinical_pharmacology (with its pharmacokinetics, pharmacodynamics and mechanism subsections) and nonclinical_toxicology (with its subsections). Everything else is kept, including the patient leaflets, the counseling section (information_for_patients), description and how_supplied.
 
These sections describe trial results, pharmacokinetic curves, animal toxicology and molecular mechanisms. That material is written for prescribers and regulators, not for a pharmacist answering a customer, and none of the test questions needs it. It is also the bulk of the long prescription labels, so keeping it would have cost a large share of the free-tier embedding quota. Worse, it would compete with the useful sections at search time: a question about "naproxen and pregnancy" could pull a trial table or an animal study into the top 5 instead of the dosing or warning passage. The medication guide (spl_medguide) mostly restates the warnings and counseling points in patient language, which are already covered by information_for_patients and the warning sections.
 
All chunks use a single size: 150 words, kept within one section and split between sentences where possible. Each chunk starts with a "Brand (generic), Section:" header so it can be found by drug name even when the passage itself never names the drug.
 
I used a single chunk size because of the free-tier embedding quota: each chunk size means embedding the whole corpus again, and comparing several sizes was not affordable. That is also why the three retrieval designs below all reuse the same chunks. I chose 150 words because the facts pharmacists ask about are short and local, such as a maximum daily dose, a contraindication or a timing rule, and usually sit within one or two sentences. Small chunks keep each fact close to its own section header, so a dosing limit is less likely to be mixed with a neighbouring indication. 150 words also fits the OTC labels well, where whole sections are often shorter than that, and it keeps the prompt small: 5 passages add only about 580 words.
 
The main extraction problem I fixed is that openFDA repeats subsections inside their parent sections. For example, drug_interactions appears again inside precautions, and pregnancy inside use_in_specific_populations. Left as-is, the same text would be embedded twice and could fill the top results with duplicates. The indexer therefore cuts the subsection text out of the parent, so every passage is embedded only once.
 
Each chunk stores the following metadata: source, brand, generic name, manufacturer, product type, location (the section title), field (the openFDA field name), part, set_id, version, the DailyMed URL, and a content hash so that an unchanged chunk is not re-embedded. The index holds 725 chunks from the 14 labels (821 after adding Eliquis). They are embedded with gemini-embedding-2 at 768 dimensions and stored in ChromaDB with cosine distance, which takes about 12 MB.
 
## Test set
 
The test set has 46 questions written from the labels: 31 single-passage, 8 multi-passage and 7 unanswerable. `validate_questions.py` checks that every expected source and location exists in the chunk metadata, and locations use the openFDA field names. The unanswerable questions stay close to the topic so that the agent can't refuse just because a question looks off-topic. They cover Eliquis (not indexed), Cipro with alcohol, Plavix with grapefruit, alternating Advil and Tylenol, Prilosec with levothyroxine, and Aleve with sumatriptan.
 
Two examples:
 
- **Single (q01):** "What is the maximum number of Advil Liqui-Gels an adult can take in 24 hours?" The answer is 6 capsules in 24 hours, from [advil, dosage_and_administration].
- **Multi (q34):** "A customer on warfarin wants an OTC pain reliever. What do the Tylenol and Advil labels say?" A complete answer needs both [tylenol, ask_doctor_or_pharmacist] and [advil, warnings].
## Retrieval
 
I measured retrieval on the 39 answerable questions, using the question text as the query (`evaluate.py`, numbers in `eval/summary.md`). A hit is a top-k chunk that matches an expected (source, location) pair, and "all@5" means every expected passage of a multi question appears in the top 5. All three designs use the same 150-word chunks, so comparing them needed no re-embedding.
 
| Design | hit@1 | hit@3 | hit@5 | all@5 | words in top 5 |
|---|---|---|---|---|---|
| vector (cosine, current) | 77% | 97% | 97% | 87% | 581 |
| hybrid (vector + BM25, reciprocal rank fusion) | 64% | 85% | 90% | 80% | 581 |
| metadata filter (vector, only the labels named in the question) | 77% | 97% | 97% | 87% | 575 |
 
Hybrid search did worse than plain vector search, especially on multi questions, where hit@5 fell from 100% to 75%. It lost the expected passage completely on q08, q12, q33 and q39. The metadata filter gave exactly the same numbers as plain vector search. Every question names its drug, and the "Brand (generic), Section:" header already steers the vectors to the right label, so filtering by label adds nothing. The only question that plain vector search missed at k=5 was q30. With 5 passages per search, each search adds about 580 words to the prompt.
 
I chose plain vector search. It matched or beat both alternatives on every measure: hybrid search was worse at every k and lost four expected passages completely, and the metadata filter gave identical results while adding a step that has to guess which labels a question names. A filter that guesses wrong would hide the right label altogether, which is a worse failure than ranking it lower. Vector search is also the simplest design to run and explain, and the "Brand (generic), Section:" header already gives it the drug-name steering that the filter was meant to add.
 
## Tools and subagent
 
The MCP server exposes two tools. `search(query)` returns the 5 best passages, each headed `[source, location]` plus the product name. Its description lists the 14 drugs by brand and active ingredient, tells the model to name the drug in the query, and tells it to search each drug separately when a question involves two drugs.
 
The `search` tool's description (its docstring in `server.py`), which is what the model reads:

```text
Search FDA drug labels (openFDA) for passages that answer a pharmacy question.

The corpus holds the labels of: Flanax, Aleve and prescription naproxen
(naproxen), Advil (ibuprofen), Celebrex (celecoxib), Tylenol
(acetaminophen), Jantoven (warfarin), Plavix (clopidogrel), Amoxil
(amoxicillin), Augmentin (amoxicillin/clavulanate), Zithromax
(azithromycin), Cipro (ciprofloxacin), Bactrim
(sulfamethoxazole/trimethoprim) and Prilosec (omeprazole), plus any label
added later. Use it for dosing, contraindications, warnings, interactions,
special populations and counseling points. Name the drug (brand or active
ingredient) in the query; for a question about two drugs, search each one.

Returns the 5 most relevant passages, each headed by its citation
[source, location] (label file and label section) and the product name.
```
 
`add_document(path)` takes the path to an openFDA label JSON file and runs it through `index_file` from `index.py`, which it imports instead of reimplementing. If the document is already indexed, unchanged chunks keep their vectors and only new or changed chunks are embedded. The tool returns the number of chunks added, reused and removed. Query embeddings are cached in `index/query_cache.json` to save quota.
 
Here is one search result, as printed by `check.py` for q01:
 
```
[advil, Dosage and Administration] Advil (ibuprofen) ... do not exceed 6 capsules in 24 hours
```
 
The subagent `.claude/agents/corpus-researcher.md` is set up as a label-lookup assistant for junior pharmacists in training. It can use only the search tool. Its instructions tell it to search each drug's label separately, cite every claim to the label and section it came from, and keep each fact in its own section. It answers in a fixed structure (Answer, What the label says, At the counter, Escalate) and refers to the supervising pharmacist when the labels don't cover a question or the question involves a contraindication, interaction, pregnancy or dosing decision.
 
The subagent's definition:
 
```markdown
---
name: corpus-researcher
description: Answers junior pharmacists' questions from 14 FDA drug labels (Advil, Aleve, Flanax, naproxen, Celebrex, Tylenol, Jantoven/warfarin, Plavix, Amoxil, Augmentin, Zithromax, Cipro, Bactrim, Prilosec), plus Eliquis (apixaban), added later with add_document, with section citations. Use it for dosing, warnings, contraindications, interactions or pregnancy questions about these drugs. Not for drugs outside this list.
tools: mcp__corpus__search
---
 
You support junior pharmacists in training while they help customers at the counter. They need a fast, reliable answer, but they are also learning to read drug labels themselves. Answer from the labels only, show them where the answer sits in the label, and make clear when a question should go to the supervising pharmacist.
 
Your only source is the FDA labels you can reach through the search tool. Your own medical knowledge is not a source: if the retrieved passages don't say it, don't say it, even if it seems well known.
 
## How to search
1. Search before you answer. Use short queries that name the drug and the topic, e.g. `Cipro antacid` or `Jantoven INR monitoring`.
2. If the question involves two drugs (a customer on one drug asking about another, or a comparison), search each drug's label separately. Answer only once you have a passage from each label. Don't answer for one drug from the other drug's label.
3. If the results miss, rephrase once or twice (brand vs generic name, section name such as "Contraindications" or "Drug Interactions"). Stop after three searches without a relevant passage.
 
## How to answer
Use this structure and keep it short; the trainee may be reading it with a customer waiting.
 
**Answer:** One or two sentences that directly answer the question, e.g. "No, Cipro should not be taken with milk alone."
 
**What the label says:** The key facts as bullets: doses, maximums, timing, warnings, "ask a doctor" instructions. Cite each one with the source and section exactly as the search result labels it, e.g. [cipro, Dosage and Administration].
 
**At the counter:** One or two practical points the trainee can pass on or act on, taken only from the label (e.g. a patient counseling point, a "stop use and ask a doctor" sign). Skip this section if the label offers nothing practical.
 
**Escalate:** Include this line whenever the question involves a contraindication, a drug interaction, pregnancy or breastfeeding, a child under the label's age limit, kidney or liver impairment, a boxed warning, or any decision to dispense, combine drugs or change a dose: "Confirm with the supervising pharmacist before advising the customer."
 
## Accuracy rules
- Every claim must come from a passage you actually retrieved, cited to the label and section it came from.
- Keep each fact attached to its own section and indication. Don't move a limit or warning from one indication or section to another, and don't merge two labels into one statement.
- Note the difference between OTC labels (Advil, Aleve, Flanax, Tylenol) and prescription labels when it matters. An OTC "ask a doctor" instruction and an Rx contraindication are not the same thing.
- Do no arithmetic or clinical inference beyond simple restatement. If the label doesn't give a number, don't calculate one.
- Don't soften or drop warnings to make the answer shorter. If a label gives a maximum dose or an age limit, include it.
 
## When the corpus doesn't cover the question
- Say plainly that the available labels don't cover it, and name what you searched for.
- Don't guess or fill the gap with general knowledge, and don't offer a "probably" answer.
- Tell the trainee to check with the supervising pharmacist or the full prescribing information.
- If a covered label holds something related but not what was asked (e.g. a missed-dose rule for a different drug), don't present it as the answer.
 
## Tone
Write for a colleague in training: clear, plain, never condescending. Use the label's own terms (e.g. "contraindicated", "ask a doctor before use") so the trainee learns the vocabulary, and briefly explain a term only if the label itself explains it.
```
 
Two of the rules come straight from the evaluation failures: searching each drug's label separately targets q34, and keeping each fact in its own section targets q29.
 
I ran the subagent once from Claude Code on q34, the question the agent failed. The full transcript, with every retrieved passage, is in `eval/subagent_transcript.md`; below, the passages are folded.

**Subagent transcript (corpus-researcher)**

Run from Claude Code in this repository (claude-opus-5-5), which loaded the project's `corpus` MCP server from `.mcp.json` and the agent from `.claude/agents/corpus-researcher.md`. Finished in 27.5 s.

**User → Claude Code:** Delegate this question to the corpus-researcher subagent and return its answer unchanged.

**Claude Code → corpus-researcher:** A customer on warfarin wants an OTC pain reliever. What do the Tylenol and Advil labels say?

**corpus-researcher → `mcp__corpus__search` (1):** `{"query": "Tylenol warfarin ask a doctor or pharmacist"}`

<details><summary>Returned: [tylenol, Ask a Doctor or Pharmacist Before Use], [tylenol, Ask a Doctor Before Use], [jantoven, Drug Interactions], [tylenol, Do Not Use], [tylenol, Pregnancy or Breast-feeding]</summary>

```text
[tylenol, Ask a Doctor or Pharmacist Before Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are taking the blood thinning drug warfarin

[tylenol, Ask a Doctor Before Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Ask a Doctor Before Use: Ask a doctor before use if you have liver disease

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: Because bleeding risk is increased when these drugs are used concomitantly with warfarin, closely monitor patients receiving any such drug with warfarin. Table 3: Drugs that Can Increase the Risk of Bleeding Drug Class Specific Drugs Anticoagulants argatroban, dabigatran, bivalirudin, desirudin, heparin, lepirudin Antiplatelet Agents aspirin, cilostazol, clopidogrel, dipyridamole, prasugrel, ticlopidine Nonsteroidal Anti-Inflammatory Agents celecoxib, diclofenac, diflunisal, fenoprofen, ibuprofen, indomethacin, ketoprofen, ketorolac, mefenamic acid, naproxen, oxaprozin, piroxicam, sulindac Serotonin Reuptake Inhibitors citalopram, desvenlafaxine, duloxetine, escitalopram, fluoxetine, fluvoxamine, milnacipran, paroxetine, sertraline, venlafaxine, vilazodone 7.4 Antibiotics and Antifungals There have been reports of changes in INR in patients taking warfarin and antibiotics or antifungals, but clinical pharmacokinetic studies have not shown consistent effects of these agents on plasma concentrations of warfarin. Closely monitor INR when starting or stopping any antibiotic or antifungal in patients taking warfarin.

[tylenol, Do Not Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Do Not Use: Do not use - with any other drug containing acetaminophen (prescription or nonprescription). If you are not sure whether a drug contains acetaminophen, ask a doctor or pharmacist. - if you are allergic to acetaminophen or any of the inactive ingredients in this product

[tylenol, Pregnancy or Breast-feeding] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Pregnancy or Breast-feeding: If pregnant or breast-feeding, ask a health professional before use.
```

</details>

**corpus-researcher → `mcp__corpus__search` (2):** `{"query": "Advil ibuprofen anticoagulant warfarin ask a doctor"}`

<details><summary>Returned: [advil, Ask a Doctor or Pharmacist Before Use], [advil, Ask a Doctor Before Use], [tylenol, Ask a Doctor or Pharmacist Before Use], [advil, Warnings], [advil, Do Not Use]</summary>

```text
[advil, Ask a Doctor or Pharmacist Before Use] Advil (ibuprofen)
Advil (ibuprofen), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are under a doctor's care for any serious condition taking aspirin for heart attack or stroke, because ibuprofen may decrease this benefit of aspirin taking any other drug

[advil, Ask a Doctor Before Use] Advil (ibuprofen)
Advil (ibuprofen), Ask a Doctor Before Use: Ask a doctor before use if stomach bleeding warning applies to you you have problems or serious side effects from taking pain relievers or fever reducers you have a history of stomach problems, such as heartburn you have high blood pressure, heart disease, liver cirrhosis, kidney disease, asthma, or had a stroke you are taking a diuretic

[tylenol, Ask a Doctor or Pharmacist Before Use] TYLENOL Extra Strength (acetaminophen)
TYLENOL Extra Strength (acetaminophen), Ask a Doctor or Pharmacist Before Use: Ask a doctor or pharmacist before use if you are taking the blood thinning drug warfarin

[advil, Warnings] Advil (ibuprofen)
Advil (ibuprofen), Warnings: Warnings Allergy alert: Ibuprofen may cause a severe allergic reaction, especially in people allergic to aspirin. Symptoms may include: hives facial swelling asthma (wheezing) shock skin reddening rash blisters If an allergic reaction occurs, stop use and seek medical help right away. Stomach bleeding warning: This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you are age 60 or older have had stomach ulcers or bleeding problems take a blood thinning (anticoagulant) or steroid drug take other drugs containing prescription or nonprescription NSAIDs [aspirin, ibuprofen, naproxen, or others] have 3 or more alcoholic drinks every day while using this product take more or for a longer time than directed Heart attack and stroke warning: NSAIDs, except aspirin, increase the risk of heart attack, heart failure, and stroke. These can be fatal.

[advil, Do Not Use] Advil (ibuprofen)
Advil (ibuprofen), Do Not Use: Do not use if you have ever had an allergic reaction to any other pain reliever/fever reducer right before or after heart surgery
```

</details>

**corpus-researcher → `mcp__corpus__search` (3):** `{"query": "Jantoven NSAIDs acetaminophen interaction bleeding"}`

<details><summary>Returned: [jantoven, Drug Interactions], [jantoven, Drug Interactions], [jantoven, Warnings and Precautions], [jantoven, Drug Interactions], [jantoven, Drug Interactions]</summary>

```text
[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: Because bleeding risk is increased when these drugs are used concomitantly with warfarin, closely monitor patients receiving any such drug with warfarin. Table 3: Drugs that Can Increase the Risk of Bleeding Drug Class Specific Drugs Anticoagulants argatroban, dabigatran, bivalirudin, desirudin, heparin, lepirudin Antiplatelet Agents aspirin, cilostazol, clopidogrel, dipyridamole, prasugrel, ticlopidine Nonsteroidal Anti-Inflammatory Agents celecoxib, diclofenac, diflunisal, fenoprofen, ibuprofen, indomethacin, ketoprofen, ketorolac, mefenamic acid, naproxen, oxaprozin, piroxicam, sulindac Serotonin Reuptake Inhibitors citalopram, desvenlafaxine, duloxetine, escitalopram, fluoxetine, fluvoxamine, milnacipran, paroxetine, sertraline, venlafaxine, vilazodone 7.4 Antibiotics and Antifungals There have been reports of changes in INR in patients taking warfarin and antibiotics or antifungals, but clinical pharmacokinetic studies have not shown consistent effects of these agents on plasma concentrations of warfarin. Closely monitor INR when starting or stopping any antibiotic or antifungal in patients taking warfarin.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: 7 DRUG INTERACTIONS Concomitant use of drugs that increase bleeding risk, antibiotics, antifungals, botanical (herbal) products, and inhibitors and inducers of CYP2C9, 1A2, or 3A4. ( 7 ) Consult labeling of all concurrently used drugs for complete information about interactions with JANTOVEN or increased risks for bleeding. ( 7 ) 7.1 General Information Drugs may interact with JANTOVEN through pharmacodynamic or pharmacokinetic mechanisms. Pharmacodynamic mechanisms for drug interactions with JANTOVEN are synergism (impaired hemostasis, reduced clotting factor synthesis), competitive antagonism (vitamin K), and alteration of the physiologic control loop for vitamin K metabolism (hereditary resistance). Pharmacokinetic mechanisms for drug interactions with JANTOVEN are mainly enzyme induction, enzyme inhibition, and reduced plasma protein binding. It is important to note that some drugs may interact by more than one mechanism.

[jantoven, Warnings and Precautions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Warnings and Precautions: Bleeding is more likely to occur within the first month. Risk factors for bleeding include high intensity of anticoagulation (INR >4.0), age greater than or equal to 65, history of highly variable INRs, history of gastrointestinal bleeding, hypertension, cerebrovascular disease, anemia, malignancy, trauma, renal impairment, certain genetic factors [see Clinical Pharmacology (12.5) ], certain concomitant drugs [see Drug Interactions (7) ], and long duration of warfarin therapy. Perform regular monitoring of INR in all treated patients. Those at high risk of bleeding may benefit from more frequent INR monitoring, careful dose adjustment to desired INR, and a shortest duration of therapy appropriate for the clinical condition. However, maintenance of INR in the therapeutic range does not eliminate the risk of bleeding. Drugs, dietary changes, and other factors affect INR levels achieved with JANTOVEN therapy.

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: 7.5 Botanical (Herbal) Products and Foods More frequent INR monitoring should be performed when starting or stopping botanicals. Few adequate, well-controlled studies evaluating the potential for metabolic and/or pharmacologic interactions between botanicals and JANTOVEN exist. Due to a lack of manufacturing standardization with botanical medicinal preparations, the amount of active ingredients may vary. This could further confound the ability to assess potential interactions and effects on anticoagulation. Some botanicals may cause bleeding events when taken alone (e.g., garlic and Ginkgo biloba) and may have anticoagulant, antiplatelet, and/or fibrinolytic properties. These effects would be expected to be additive to the anticoagulant effects of JANTOVEN. Conversely, some botanicals may decrease the effects of JANTOVEN (e.g., co-enzyme Q 10 , St. John's wort, ginseng). Some botanicals and foods can interact with JANTOVEN through CYP450 interactions (e.g., echinacea, grapefruit juice, ginkgo, goldenseal, St. John's wort).

[jantoven, Drug Interactions] Jantoven (warfarin sodium)
Jantoven (warfarin sodium), Drug Interactions: Table 2: Examples of CYP450 Interactions with Warfarin Enzyme Inhibitors Inducers CYP2C9 amiodarone, capecitabine, cotrimoxazole, etravirine, fluconazole, fluvastatin, fluvoxamine, metronidazole, miconazole, oxandrolone, sulfinpyrazone, tigecycline, voriconazole, zafirlukast aprepitant, bosentan, carbamazepine, phenobarbital, rifampin CYP1A2 acyclovir, allopurinol, caffeine, cimetidine, ciprofloxacin, disulfiram, enoxacin, famotidine, fluvoxamine, methoxsalen, mexiletine, norfloxacin, oral contraceptives, phenylpropanolamine, propafenone, propranolol, terbinafine, thiabendazole, ticlopidine, verapamil, zileuton montelukast, moricizine, omeprazole, phenobarbital, phenytoin, cigarette smoking CYP3A4 alprazolam, amiodarone, amlodipine, amprenavir, aprepitant, atorvastatin, atazanavir, bicalutamide, cilostazol, cimetidine, ciprofloxacin, clarithromycin, conivaptan, cyclosporine, darunavir/ritonavir, diltiazem, erythromycin, fluconazole, fluoxetine, fluvoxamine, fosamprenavir, imatinib, indinavir, isoniazid, itraconazole, ketoconazole, lopinavir/ritonavir, nefazodone, nelfinavir, nilotinib, oral contraceptives, posaconazole, ranitidine, ranolazine, ritonavir, saquinavir, telithromycin, tipranavir, voriconazole, zileuton armodafinil, amprenavir, aprepitant, bosentan, carbamazepine, efavirenz, etravirine, modafinil, nafcillin, phenytoin, pioglitazone, prednisone, rifampin, rufinamide 7.3 Drugs that Increase Bleeding Risk Examples of drugs known to increase the risk of bleeding are presented in Table 3.
```

</details>

**corpus-researcher → Claude Code (final report):**

**Answer:** Both labels say to talk to a professional first, but they say different things. Tylenol (acetaminophen) says "Ask a doctor or pharmacist before use if you are taking the blood thinning drug warfarin." Advil (ibuprofen) has a stomach bleeding warning that is specifically higher-risk if you take a blood thinning (anticoagulant) drug. Neither OTC label tells the customer to go ahead on their own.

**What the label says:**

*Tylenol (OTC)*
- "Ask a doctor or pharmacist before use if you are taking the blood thinning drug warfarin." [tylenol, Ask a Doctor or Pharmacist Before Use]
- "Ask a doctor before use if you have liver disease." [tylenol, Ask a Doctor Before Use]
- Do not use with any other drug containing acetaminophen, whether prescription or nonprescription. If unsure whether a drug contains acetaminophen, ask a doctor or pharmacist. [tylenol, Do Not Use]

*Advil (OTC)*
- Stomach bleeding warning: "This product contains an NSAID, which may cause severe stomach bleeding. The chance is higher if you… take a blood thinning (anticoagulant) or steroid drug." Other listed risk factors: age 60 or older, past stomach ulcers or bleeding problems, other NSAIDs, 3 or more alcoholic drinks every day, or taking more or for longer than directed. [advil, Warnings]
- "Ask a doctor before use if stomach bleeding warning applies to you." [advil, Ask a Doctor Before Use]
- "Ask a doctor or pharmacist before use if you are… taking any other drug." [advil, Ask a Doctor or Pharmacist Before Use]

*Jantoven (warfarin, Rx label), from the customer's own drug*
- Table 3, "Drugs that Can Increase the Risk of Bleeding," lists ibuprofen under Nonsteroidal Anti-Inflammatory Agents. The label says: "Because bleeding risk is increased when these drugs are used concomitantly with warfarin, closely monitor patients receiving any such drug with warfarin." [jantoven, Drug Interactions]
- I did not find acetaminophen in the Jantoven passages I retrieved. That only means the search did not turn it up. It does not show there is no interaction, and the Tylenol label itself still says to ask first.

**At the counter:**
- Both labels send this customer to a doctor or pharmacist before use, so neither one is a simple "just take it" product here. Advil's warning names blood thinners directly.
- If Tylenol is being considered, check that the customer is not already taking another product that contains acetaminophen [tylenol, Do Not Use].

**Escalate:** Confirm with the supervising pharmacist before advising the customer. This is a drug interaction question with warfarin, and both OTC labels say "ask a doctor or pharmacist before use."

*Claude Code returned this report to the user unchanged.*
 
## Adding a document
 
The demo is run by `add_document_demo.py`, with output in `eval/add_document_demo.md`. The held-back document is `corpus/held_back/eliquis.json` (Eliquis/apixaban, Bristol-Myers Squibb), added through the MCP add_document tool. The first add embedded 96 chunks. Adding the same document again embedded 0 chunks, reused 96 and removed 0, so re-adding a document creates no duplicates and spends no quota.
 
My policy for re-adding a document is no duplicates. Unchanged chunks keep their saved vectors, only new or changed chunks are embedded, and chunks that a newer version of the label no longer contains are removed. This means re-adding an updated version of a label also works: the index ends up matching the new label, and stale text never sits next to the new text. For drug labels this matters, because an old dose or warning left in the index could be retrieved and cited as if it were current. The comment on `add_document` in `server.py` states this policy.
 
Adding Eliquis turned two refusals into cited answers. Before the add, the agent refused q40 ("What is the usual Eliquis dose for atrial fibrillation?"), saying the corpus did not contain Eliquis and referring the user to the pharmacist. Afterwards it answered 5 mg twice daily, or 2.5 mg twice daily for patients with at least two of: age 80 or older, weight 60 kg or less, or serum creatinine of 1.5 mg/dL or more, citing [eliquis, Dosage and Administration]. Likewise, q41 (a missed Eliquis dose) went from a refusal to a cited answer: take the missed dose as soon as possible on the same day, then resume twice-daily dosing without doubling up. Both runs used gemini-3.5-flash-lite.
 
## Harness and guardrails
 
AGENTS.md gives the agent three rules:
 
1. **The labels are the only source.** Every statement must come from a passage the search tool returned. The model's general medical knowledge does not count, however confident it is.
2. **Every claim carries its citation.** Each fact is tagged `[source, location]` so the pharmacist can open the label section and check it, and so the evaluation can check it too.
3. **Gaps are stated, not filled.** When the labels don't answer the question, the agent says so and refers the pharmacist to their supervisor instead of guessing, because a referral costs minutes and a wrong answer can cost a patient's health.

`add_document` needs human approval because it changes the index. It is listed in NEEDS_APPROVAL, so `agent.py` asks "Allow? [y/N]" in the terminal and denies the call when no one can answer. `answer_questions.py` always denies it, so every evaluation answer comes from the starting index. LangChain middleware also caps each question at 8 model calls and 6 tool calls. For reliability, I added a model fallback: `ask` moves from gemini-3.8-flash to gemini-3.5-flash and then to gemini-3.5-flash-lite when it receives a 503 or 429 error, or gets no answer within 75 seconds. In the final `check.py` run, both gemini-3.8-flash and gemini-3.5-flash hung, and gemini-3.5-flash-lite answered.
 
The extra guardrail is a citation check, `invalid_citations()` in `agent.py`. After the agent answers, every `[source, location]` citation in the answer is compared with the citation headings of the passages its searches actually returned. If any citation was not returned, whether invented, misspelled or merged, the whole answer is rejected. The user then sees "Answer withheld: it cited ..., which the label search did not return", followed by advice to look it up in the label directly or ask the supervising pharmacist. The rejected text is kept in the result (`guardrail.rejected_answer`) so it can be inspected later.
 
I chose this check over the two alternatives (requiring at least one citation, or requiring dosing answers to cite a Dosage section) because it enforces AGENTS.md rule 2 directly. The point of a citation is that the pharmacist can open the label and check the claim; a citation that points at nothing the agent retrieved can't be checked, so it looks verified when it isn't. For a pharmacist, that is worse than no answer.
 
The guardrail fires on q33 (Bactrim and Celebrex contraindications). That answer cited `[bactrim, Contraindications, celebrex, Contraindications]`, two citations merged into one bracket, which matches no returned passage even though both passages were retrieved. The guardrail would have withheld it. `evaluate.py` applies the same function to every saved answer and reports q33 as the only one it rejects (`eval/summary.md`). The 46 evaluation answers were produced before the guardrail existed, so the results in this report are unfiltered.
 
There is a trade-off: q33's content was correct, so here the guardrail rejects a good answer over a format error. It is strict on purpose. A withheld answer costs the pharmacist a lookup or a referral, while an uncheckable citation undermines the one thing that makes the answers safe to use. The guardrail would not have caught q34, because that answer cited a Jantoven passage it really did retrieve; that failure needs the one-drug-per-search fix described under Failures.
 
## Evaluation
 
The code checks in `evaluate.py` found that every answer searched before answering, and that every answerable answer had at least one citation and cited its expected source. One answer (q33) had a malformed citation. All 7 unanswerable questions were refused, and no answerable question was refused. Refusals are detected with a regular expression that looks for phrases such as "does not contain", "not covered" or "no information".
 
The LLM judge was a separate Claude chat (Claude Opus 5.5), given `eval/answers.md`, which holds each question, its reference answer, the agent's answer and the passages it retrieved. This was a manual step, not an automated call. The judge returned id, correct, supported and notes for each question, which I saved as `eval/judge_verdicts.csv` for `evaluate.py` to read. The rubric was:
 
- One row per question, q01–q46, with no missing or merged ids.
- **correct:** 1 or 0 against the reference answer. A proper refusal on an unanswerable question counts as 1.
- **supported:** 1 or 0. It is 1 only if every claim in the answer appears in the retrieved passages under that answer, not in the judge's own knowledge.
- **notes:** a short reason for every 0, in double quotes.

The judge marked 45 of 46 answers correct and found 1 unsupported answer (q29). All 7 unanswerable questions were correctly refused, and there were no wrong refusals. By question kind: single questions were 31/31 correct with 1 unsupported, multi questions 7/8 correct, and unanswerable questions 7/7.
 
To check the judge, I graded 30 answers myself (q01–q30) in `eval/human_labels.csv`, using the same rubric. On `correct`, I agreed with the judge on all 30 (100%). On `supported`, I agreed on 29 of 30 (96.7%). The one disagreement was q29, which the judge marked unsupported because the 1,250 mg/day cap it presents as the gout limit belongs to the preceding section of the label; I marked it supported. On review, I side with the judge. It was stricter than I was, but in a pharmacy setting a dose limit taken from the wrong indication has to count as unsupported, so the final results use the judge's verdict. I kept my original grade in `eval/human_labels.csv`, because the human grades are meant to be made before reading the judge's verdicts; changing q29 afterwards would have inflated the agreement to 100%.
 
Cohen's kappa is not informative here. `evaluate.py` reports it as 0.0 for `supported`, despite 96.7% agreement, and as None for `correct`. On q01–q30 both of us gave a 1 for `correct` on every question, so kappa is undefined, and for `supported` I gave a 1 on every question while the judge gave a 0 only once. Kappa measures agreement beyond what chance would produce, and when one rater uses only one grade, chance already explains almost all the agreement. The percentages are the more useful figure.
 
The human check has two limits. First, q01–q30 are all single-passage questions, so it covers none of the multi or unanswerable questions, and it does not include q34, the only answer the judge marked incorrect. The judge's verdicts on multi questions and refusals are therefore unchecked. Second, I am a data analysis student, not a pharmacist, so my grades check the answers against the reference answers and retrieved passages, not against clinical expertise. Grading the remaining 16 questions, ideally by someone with pharmacy training, would be the next step.
 
### Models that produced the answers
 
The 46 test questions were answered by three different Gemini models. This was not planned. I meant to use `gemini-3.8-flash` for every question, but the free tier allows only **20 requests per day per model**, and the agent needs about two model calls per question, so the run was spread over several days. `answer_questions.py` saves each answer as soon as it is ready and skips questions already answered, so a stopped run loses nothing. Each saved answer records the model that wrote it (`model` in `eval/answers.jsonl`).
 
| Questions | Model | Answered on | Kinds |
|---|---|---|---|
| q01–q22 | `gemini-3.8-flash` | 18–19 Nov | 22 single |
| q23–q32 | `gemini-3.5-flash` | 23–24 Nov | 9 single, 1 multi |
| q33–q46 | `gemini-3.5-flash-lite` | 24 Nov | 7 multi, 7 unanswerable |
 
I ended up with three models in three steps:
 
1. **`gemini-3.8-flash` (q01–q22).** I answered 16 questions on 18 November and reached 22 on 19 November. Questions q17–q22 were slow because the model often returned `503 UNAVAILABLE` ("high demand"). On 20 and 23 November it returned 503 on every attempt at q23. Failed requests still count toward the daily quota, so the retries used up all 20 requests without answering anything.
2. **`gemini-3.5-flash` (q23–q32).** On 23 November I switched the remaining questions to this model. It answered q23–q25 that day and q26–q32 on 24 November, then hit its daily quota (`429 RESOURCE_EXHAUSTED`) at q33.
3. **`gemini-3.5-flash-lite` (q33–q46).** The deadline was the next day, so waiting for quotas to reset was not an option. Going back to `gemini-3.8-flash` gave another 503 and then a 429. `gemini-3.7-flash` and `gemini-3.6-flash` had already used their daily quotas (the error reported the `GenerateRequestsPerDayPerProjectPerModel-FreeTier` limit of 20), and `gemini-2.5-flash` returned 404 for my key. `gemini-3.5-flash-lite` still had quota and answered the last 14 questions without errors.

The runs also differ in other ways. `agent.py` asks for `temperature=0`, but `gemini-3.5-flash-lite` uses fixed sampling and ignores this setting (the client library warns about it), so its answers may not be repeatable. Cost and latency per question also varied by model, according to `eval/answers.jsonl`:
 
| Model | Questions | Mean s | Median s | Mean tokens | Mean model calls | Mean searches |
|---|---|---|---|---|---|---|
| `gemini-3.8-flash` | 22 | 151.0 | 21.9 | 2,961 | 2.09 | 1.09 |
| `gemini-3.5-flash` | 10 | 58.2 | 46.9 | 4,061 | 2.30 | 1.30 |
| `gemini-3.5-flash-lite` | 14 | 4.1 | 2.8 | 3,352 | 2.29 | 1.50 |
 
The `gemini-3.8-flash` mean is pushed up by the slow, overloaded requests on q17–q22, so its median is more typical.
 
Most importantly, the models are tied to question kinds. The questions were answered in file order, so every single question except one went to the two flash models, while all the unanswerable questions and 7 of the 8 multi questions went to `gemini-3.5-flash-lite`. Results by question kind are therefore also results by model. The judge had to be a fourth model, different from all three answer models, which is why I used Claude.
 
This means the results by question kind cannot be read as a clean comparison. If multi questions look harder than single ones (7/8 correct against 31/31), I can't tell whether that is because multi questions are harder, or because they were answered by the smallest model, or both. The same confound runs the other way for the refusals: the 7/7 correct refusals all came from `gemini-3.5-flash-lite`, so they show that model refuses well, not that every model in the fallback chain does. Both judge failures also came from the two later models, but with only 46 questions, one or two failures per model is too few to rank the models. A fair comparison would rerun all 46 questions on one model, ideally in shuffled order so no kind is tied to a model or a day.
 
For the decision, the safe reading is to treat the results as those of the weakest model in the chain. The fallback in `agent.py` means a real user could be served by any of the three models depending on load, so the system's quality is bounded by `gemini-3.5-flash-lite`, which also ignores `temperature=0`. That is acceptable for the results seen here, but it argues for pinning a single model in any real deployment.
 
## Failures
 
The judge flagged 2 of the 46 answers:
 
- **q29** (single, gemini-3.5-flash) was correct but unsupported. It presents the 1,250 mg/day cap as the gout limit, but in the passage that cap belongs to section 2.4 (pain), not section 2.5 (gout). Both subsections sit in the same 150-word chunk, which was retrieved at rank 1, so the problem was in how the model used it.
- **q34** (multi, gemini-3.5-flash-lite) was incorrect. The agent searched for "warfarin Advil ibuprofen interactions", which returned only Jantoven, naproxen and Celebrex passages and never the Advil label, so it answered the Advil half from the Jantoven label. The question text on its own retrieves the Advil passage at rank 1, so the search engine can find it; the miss came from the agent's wording, where "warfarin" pulled in the warfarin label.

The code checks found one more problem: q33 merged two citations into one bracket (`[bactrim, Contraindications, celebrex, Contraindications]`). The content was right, but the citation format was broken. Both judge failures came from the two later models.
 
Classified by cause, the failures are:
 
| Cause | Count | Questions |
|---|---|---|
| Retrieval miss | 1 | q34 |
| Unsupported claim | 1 | q29 |
| Wrong answer from the right passage | 0 | – |
| Wrong refusal | 0 | – |
| Bad test question | 0 | – |
 
That is 2 failures of 2 different kinds. q29 could also be read as a wrong answer from the right passage, since the model misread a passage it had. I classify it as an unsupported claim because the judge still scored the answer correct: the main answer was right, and only the extra claim that 1,250 mg is the gout maximum has no support in the text. q34 is not a bad test question, because the Advil label really does contain the blood-thinner warning. Separately, q33's merged citation is not a judge failure but a format issue, which the citation guardrail now catches.
 
The first thing to fix is the q34 pattern, a multi question where the agent searched for both drugs in one query and never retrieved one of the labels. It is the only failure that produced an incorrect answer, and multi questions involving two drugs are exactly the interaction questions where a wrong answer is most dangerous. The fix is to tell the agent, in the tool description and AGENTS.md, to put only one drug name in each search, so a two-drug question always triggers one search per label. A later guardrail could enforce this by rejecting an answer that names a drug but cites no passage from that drug's label. The q29 pattern comes second. It could be fixed by splitting chunks at numbered subsections (2.4, 2.5) so numbers from different indications never share a chunk, or by a prompt rule to state a number only together with the indication it belongs to; the subagent's rule to keep each fact in its own section is a first step.
 
## Decision
 
Across all 46 questions, the average cost was 3,319 tokens and 2.3 model calls per question. Median latency was 16.6 s; the mean of 86 s is inflated by the 503 overloads. By model, `gemini-3.8-flash` used 2,961 tokens with a median of 21.9 s, `gemini-3.5-flash` used 4,061 tokens with a median of 46.9 s, and `gemini-3.5-flash-lite` used 3,352 tokens with a median of 2.8 s. On the free tier's 20 requests per day per model, the agent can answer only about 10 questions a day per model, so it is not usable as a real service on the free tier.
 
The results to weigh are 45/46 correct answers, 1 unsupported answer, 7/7 correct refusals, no wrong refusals and a retrieval hit@5 of 97%, plus my agreement with the judge.
 
I would let junior pharmacists rely on it as a label-lookup aid, but not as a decision-maker. It is good at finding the right passage and quoting it with a citation, and it refused every question the labels don't cover, which is the most important behaviour for this use case. What it should not do on its own is decide whether to dispense, combine drugs or change a dose. The evidence supports this split: 45 of 46 answers were correct, but q34 shows that half of an answer can come from the wrong label, and it happened on a two-drug interaction question, the riskiest kind. Checking the citation is what catches that: q34 cited a Jantoven passage for a claim about Advil, which a pharmacist opening the cited section would notice immediately.
 
In practice, the pharmacist asks the agent when unsure about a label fact (a dose, interaction, contraindication, pregnancy warning or counseling point). It is not for patients directly, not for unsupervised use, and not for drugs outside the indexed labels.
 
The safeguards would be:
 
- **Supervisor sign-off for high-risk questions.** Any answer about an interaction, contraindication, pregnancy or dosing for a special population ends with an instruction to confirm with the supervising pharmacist, as the subagent's instructions already require.
- **Checking every citation.** The pharmacist checks each cited label section before passing anything to the customer, so a claim from the wrong label (q34) or the wrong subsection (q29) can be caught by a person.
- **The citation guardrail.** Answers whose citations can't be checked are withheld before they reach the pharmacist.
- **Referral when the labels are silent.** When the labels don't cover a question, the agent refers to the supervising pharmacist instead of guessing, as it did on all 7 unanswerable questions.
- **A single pinned model on a paid tier.** The free tier's quota makes it unusable at a real counter, and the fallback chain makes quality depend on server load.

My grades agreed with the judge's on 30 of 30 `correct` verdicts and 29 of 30 `supported` verdicts, which supports the judge's results for single questions. The multi and unanswerable questions, including the one incorrect answer, were not human-checked, so those results rest on the judge alone. That is one more reason to keep a pharmacist in the loop for interaction questions.
 
## AI use
 
The use case and idea was fully original and decided by myself, my other contributions include:
- Corpus selection: using FDA/openFDA labels only, rejecting the travellers' "equivalent medicine abroad" tool and EMA labels, dropping drugs.com after catching that it gave wrong information, confirming the 14 labels and holding Eliquis back for the add-document demo
- Trimming down word count from documents: choosing which sections to drop (clinical studies, medication guide, clinical pharmacology, nonclinical toxicology) and which to keep (patient leaflets, counseling text, tables)
- Chunking: one chunk size only, to protect the free-tier quota, with 150-word chunks kept within one section
- Presentation choices: showing both brand name and active ingredient, ignoring discontinued brand names, and mentioning the openFDA disclaimer only as a short note
- Running the agent: spreading the run over several days on gemini-3.8-flash, then switching to gemini-3.5-flash and gemini-3.5-flash-lite as quotas ran out
- Design decisions: choosing plain vector search, no duplicates when a document is re-added, the citation guardrail and the support-tool framing (with the pharmacist checking every citation) from options suggested by Claude Code
- Evaluation: using a separate Claude chat as the judge, running it and saving its verdicts, grading 30 answers myself (q01–q30), and siding with the judge on q29 while keeping my original grade
- Failures and model analysis: choosing the classification and fix-first priority from evidence prepared with Claude

AI was used as follows:
- Claude Code (Claude Opus) wrote the code (download, index, server and agent scripts, `answer_questions.py`, `validate_questions.py`, `evaluate.py`, `add_document_demo.py`, the model fallback and the citation guardrail), the factual draft of "Models that produced the answers" and the draft notes for this report. The judge rubric is based on a format suggested by Claude Code.
- Claude (chat, Claude Opus 5.5) drafted the 46 test questions, acted as the LLM judge, wrote the subagent file, and turned the draft notes and my decisions into the prose of this report.