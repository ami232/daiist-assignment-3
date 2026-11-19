# Assignment 3 Report

- **Name**: Manuela Carreira Rodríguez
- **Student ID**: 18766
- **Group**: BBADBA 5B

## Use case

**Who asks:** Nurses and pharmacy technicians working in a hospital ward who need to check the official information about a medicine before giving it to a patient. They might need to know things like the maximum dose, whether the dose needs to change if the patient has kidney problems, if the medicine should be avoided in certain cases, whether it interacts with other medications the patient is taking, or what to do if a dose is missed.

**What they do with the answer:** They check this information against the patient's prescription to see if the dose is correct and can be given as prescribed, or if they need to speak to the pharmacist or doctor first.

**Cost of a wrong answer vs "I don't know":** If the system gives the wrong answer, it could put the patient at risk. For example, an incorrect dose of warfarin could cause bleeding, metformin could cause lactic acidosis in patients with kidney failure, or combining sertraline with an MAOI could lead to serotonin syndrome. On the other hand, if the system says it doesn't know, the nurse or pharmacy technician just needs to spend a few extra minutes checking the official label or asking the pharmacist. That's why it's much better for the system to say it doesn't know than to give incorrect information. If the answer isn't in the available documents, it shouldn't guess. It should also include sources for its answers so the user can quickly check that the information is correct.

## Corpus

The system uses six official FDA drug labels, which were downloaded through the openFDA drug-label API. These labels are public domain because they are US federal government documents, so they can be used freely. The openFDA data is also available under CC0, and none of the documents contain personal information. Each label has its own `set_id`, which makes sure that every time we run `main.py index`, the system downloads the exact same documents instead of different versions.

| Document | Source (openFDA `set_id`) | Label date | Licence | Words (after cleaning) |
|---|---|---|---|---|
| Metformin hydrochloride ER tablets | [ec43efb2-8a50-4bac-9576-f4303841a497](https://api.fda.gov/drug/label.json?search=set_id:"ec43efb2-8a50-4bac-9576-f4303841a497") | 2026-11-10 | Public domain | 6,710 |
| Warfarin sodium tablets | [61ab23a7-bc67-4777-854a-bf43c788a69a](https://api.fda.gov/drug/label.json?search=set_id:"61ab23a7-bc67-4777-854a-bf43c788a69a") | 2026-11-09 | Public domain | 8,685 |
| Atorvastatin calcium tablets | [8cc6240a-58d3-4bca-aa1e-662228957f75](https://api.fda.gov/drug/label.json?search=set_id:"8cc6240a-58d3-4bca-aa1e-662228957f75") | 2026-11-12 | Public domain | 10,742 |
| Lisinopril tablets | [dd015c18-1ea6-44e3-9186-8d2f8444d874](https://api.fda.gov/drug/label.json?search=set_id:"dd015c18-1ea6-44e3-9186-8d2f8444d874") | 2026-11-12 | Public domain | 7,725 |
| Sertraline hydrochloride tablets | [687ebdc4-6946-454e-8d46-3207488ccf32](https://api.fda.gov/drug/label.json?search=set_id:"687ebdc4-6946-454e-8d46-3207488ccf32") | 2026-11-05 | Public domain | 12,913 |
| Amoxicillin capsules | [987786a1-d748-4b42-abb5-62a2f38ef195](https://api.fda.gov/drug/label.json?search=set_id:"987786a1-d748-4b42-abb5-62a2f38ef195") | 2026-11-13 | Public domain | 5,266 |
| **Total** | 6 documents | | | **52,041** |

I chose these six medicines because they are commonly used in hospitals and cover situations where medication errors can be especially risky, such as blood thinners, dose adjustments for patients with kidney problems, pregnancy, and interactions with antidepressants or antibiotics. There is also a seventh drug label for apixaban (`docs_to_add/apixaban.json`, 18,608 words), but it is not included in the original corpus. We only use it to show how the `add_document` function works.

## Ingestion

Code: `index.py` (`download_corpus` → `load_document` → `chunk_file` → `embed_and_store`).

- **Extract:** Each drug label from openFDA comes as a JSON file, with different fields for each section, such as `dosage_and_administration`, `contraindications`, and `drug_interactions`. I keep 30 text sections in the same order as the original label and remove fields that are not useful for the actual text. These include `*_table` (HTML versions of tables already included in the text), `package_label_principal_display_panel`, `spl_product_data_elements` (ingredient lists), and the patient Medication Guide.

- **Clean:** I remove any HTML, replace bullet symbols and non-breaking spaces, and clean up extra spaces so the text is easier to process.

- **Chunk (chosen design, "structure"):** I first divide the label by sections. Then I split each section into sentences and group them into chunks of up to 220 words. This way, each chunk only contains information from one section, rather than mixing different topics.

- **Metadata on every chunk:** Each chunk includes `source` (the drug name), `section` (for example, "Drug Interactions"), `position` (where the chunk appears within that section), `file`, `doc_hash` (the file's SHA-256 hash), and `words` (the word count). Each chunk also gets its own ID using `source:section_key:position`, such as `warfarin:drug_interactions:2`. This is the same ID the agent uses when citing its sources.

- **Embedding:** I use `gemini-embedding-001` with 768 dimensions to avoid making the `index/` folder too large. Chunks use `RETRIEVAL_DOCUMENT` and questions use `RETRIEVAL_QUERY`. The vectors are L2-normalised and stored in ChromaDB (`index/chroma`) using cosine distance. Before embedding a chunk, I add a short header like "Warfarin drug label. Section: Drug Interactions." so the drug name and section are included in the vector. The vectors are saved in batches of 20, and when I run `main.py index` again, it only embeds chunks that haven't already been stored.

- **Number of chunks:** The "structure" method creates 301 chunks, while the alternative "fixed" method creates 276. The index takes up 11 MB, or 13 MB after adding apixaban.

**Extraction problems I fixed:**

1. **Duplicated sections.** I noticed that openFDA includes some of the same information in different fields. For example, `pregnancy`, `pediatric_use`, and `geriatric_use` are already included in `use_in_specific_populations`. The same happens with `mechanism_of_action` and `pharmacokinetics`, which are also part of `clinical_pharmacology`. If I kept all of these, the system would store the same information more than once. This could make the top 5 search results show repeated passages instead of different relevant ones, and it would also make the hit-rate harder to evaluate. To fix this, I made `load_document` check whether the normalised text of a section was already included in a longer section. If it was, the duplicate was removed. In total, this removed 26 duplicated sections, which represented **8,695 words (14% of the original text)**.

2. **Wrong documents.** At first, my search using `openfda.generic_name:"METFORMIN HYDROCHLORIDE"` was bringing back medicines that contained more than one active ingredient, such as sitagliptin with metformin, amoxicillin with clavulanate, and lisinopril with hydrochlorothiazide. These were not the labels I wanted. I fixed this by using the exact-match field, `openfda.generic_name.exact`, sorting the results to get the most recent labels, and then saving their `set_id`s so the system would always use the same documents.

**Remaining noise:** There is still some repeated information in the labels because the "Highlights" section summarises details that appear again in the full sections. There are also references to other parts of the label, such as "[see Warnings and Precautions (5.1)]". I decided to leave these because they don't prevent the system from finding the right information, even though they add some repetition.

## Test set

`eval/questions.csv` contains **37 questions** that I wrote after reading the drug labels, before making any changes or tuning the system. I divided them into three types to test how well the system handles different situations:

| kind | count | what it tests |
|---|---|---|
| single | 22 | Questions that only need one piece of information from one section, such as doses, contraindications, monitoring, or overdoses. |
| multi | 8 | Questions that need information from two passages, usually from two different drug labels, like warfarin and sertraline. |
| unanswerable | 7 | Questions that sound related to the medicines but cannot be answered using the available documents. For example, questions about other drugs, prices, different formulations, crushing tablets, vaccine interactions, or equivalent statin doses. |

For each question, `expected_source` tells us which drug label should contain the answer, and `expected_location` tells us which section to look at. These match the metadata stored with the chunks. When a question needs more than one source or section, I separate them using `;`.

Two examples:

- **m01 (multi):** *A patient on warfarin is starting sertraline. What do the two labels say about this combination?*  
  This question needs information from both `sertraline;warfarin`, specifically from `Drug Interactions;Drug Interactions`. The expected answer is that taking sertraline with warfarin can increase the risk of bleeding, so INR should be monitored carefully. The warfarin label also recommends checking INR more frequently when starting or stopping other medications.

- **u04 (unanswerable):** *How long is amoxicillin oral suspension stable in the fridge after it is reconstituted?*  
  This is a good example of a question that sounds relevant but cannot actually be answered with the documents I included. The amoxicillin label in the corpus is for capsules, not oral suspension, so it doesn't include instructions about reconstitution or how long the suspension lasts in the fridge. In this case, the correct response is for the system to say that the information is not available instead of trying to guess.

## Retrieval

In `evaluate.py`, I measure how well the system finds the right information for the 30 answerable questions. To count as a hit, a chunk from the expected drug **and** the expected section needs to appear in the top k results. For multi questions, I check whether at least one of the expected passages appears. I also use "both @5" to see whether all the required passages are included in the top 5.

I compared four different designs by combining two ways of splitting the text with two search methods. The first search method is dense retrieval, and the second is hybrid, which combines dense retrieval with BM25 keyword search using Reciprocal Rank Fusion (RRF).

Results using the six-document corpus (`eval/retrieval_results.csv`):

| design | chunks | hit@1 | hit@3 | hit@5 | multi: both @5 | words added to prompt (top 5) |
|---|---|---|---|---|---|---|
| fixed 220-word windows + dense | 276 | 0.733 | 0.867 | 0.967 | 0.75 | 1,087 |
| fixed + hybrid | 276 | 0.700 | 0.933 | 0.967 | 0.625 | 1,087 |
| **structure (sections) + dense** | 301 | **0.767** | **0.933** | **1.000** | **0.875** | **923** |
| structure + hybrid | 301 | 0.667 | 0.900 | 1.000 | 0.625 | 936 |

**Chosen: structure + dense.**

I decided to use structure + dense because it gave the best overall results. It performed better or equally well in every metric, and it also added the fewest words to the prompt, which makes it more efficient.

One problem I found with fixed chunks was in q14, which asks about the 36-hour gap between sacubitril/valsartan and lisinopril. The correct answer didn't appear in the top 5 because the fixed window split the contraindication into two parts. This showed me why keeping the original sections together was important.

I also expected hybrid search to improve the results, but it didn't. BM25 gave more importance to chunks that repeated the drug name or common words like "dose", even when they weren't the most useful passages. This was especially noticeable in multi questions, where the percentage of questions with both passages in the top 5 dropped from 0.875 to 0.625.

The chosen design still missed the expected section at hit@1 for q02, q06, q07, q11, q19, m03, and m06. However, most of these aren't actual failures to find the information. The labels often repeat the same fact in different sections. For example, in q02, the eGFR contraindication also appears in "Dosage and Administration", and that section was ranked first. Since my evaluation only counts the section I originally marked as expected, the hit@1 score is a bit stricter than the system's actual ability to find the correct answer.

After testing `add_document`, I regenerated `retrieval_results.csv` with apixaban included in the index. This increased the number of structure chunks to 406. The dense retrieval results stayed the same, while

## Tools and subagent

`server.py` uses MCP through stdio and provides two tools. It loads the existing `index/`, so it doesn't need to create the embeddings for all the documents again. It only embeds the new question when someone makes a search.

**`search(query)`:** This tool searches through the official FDA drug labels. Its description is generated when the server starts, so it always shows which medicines are currently included in the corpus.

> Search a collection of official FDA drug labels. The medicines currently included are amoxicillin, atorvastatin, lisinopril, metformin, sertraline, and warfarin. The documents contain information about doses, contraindications, warnings, drug interactions, side effects, pregnancy, children, elderly patients, kidney and liver problems, overdoses, pharmacology, and storage. The tool should be used before answering any question about a medicine, even if that medicine is not currently listed, because new documents can be added. Search queries should be short, specific, and include the drug name. If the first search doesn't find the answer, try again using different words. The tool returns the five most relevant passages, each with its own citation ID, such as [warfarin:drug_interactions:2], along with the drug name, file, and section. These IDs should be included when answering.

**`add_document(path)`:** This tool allows me to add new documents to the corpus. It accepts openFDA `.json` labels, as well as `.pdf`, `.txt`, and `.md` files. It uses `index.add_file`, which is the same process used by `main.py index`, so I didn't have to write the indexing process again. After adding a document, it returns a short summary confirming what was added.

**Example of a search result:**

For the query "warfarin target INR non-valvular atrial fibrillation", one of the five results was:

```
[warfarin:dosage_and_administration:3] Source: Warfarin FDA drug label (warfarin.json) | Section: Dosage and Administration
In patients with non-valvular AF that is persistent or paroxysmal and at an intermediate risk of ischemic stroke ... long-term anticoagulation with warfarin is recommended ... therapy with warfarin to a target INR of 2.5 (range, 2.0 to 3.0) is recommended ...
```

**Subagent**

I also created a subagent in `.claude/agents/corpus-researcher.md`. The idea was to have an agent that could only use the corpus search tool, instead of looking for information anywhere else.

I gave it access to `tools: [corpus/search, mcp__corpus__search]`, which are the tool names used by Copilot and Claude Code.

The subagent has a few rules. It can search up to three times, using short questions that include the medicine's name. It must answer in 2–6 sentences, only using information found in the retrieved passages, and it has to cite the passage IDs. If the documents don't contain the answer, it should respond with "The corpus does not cover this." It also shouldn't give advice for individual patients.

**Transcript from my editor**

I tested the subagent using GitHub Copilot in VS Code, in Agent mode, with the `corpus` MCP server running.

```
User: Use the corpus-researcher subagent (defined in .claude/agents/corpus-researcher.md) to answer this question: What should be done if a patient taking lisinopril develops swelling of the face, lips or tongue?

GitHub Copilot: I'll have the corpus-researcher check the lisinopril label passages, then I'll answer from those results with their exact citation IDs.

Search lisinopril label

The subagent couldn't reach the search tool, so I'm checking the corpus directly now to keep the answer grounded in the label and preserve exact citations.

Ran `search`
Completed with input: {
  "query": "lisinopril what to do face lips tongue swelling angioedema"
}

Swelling of the face, lips, or tongue may be angioedema. Report it immediately and take no more lisinopril until you have consulted the prescribing physician. [lisinopril:information_for_patients:1] Tongue involvement can obstruct the airway; the label says to promptly discontinue lisinopril and provide appropriate treatment and monitoring until symptoms have completely and sustainably resolved. [lisinopril:warnings_and_cautions:2]
```

**What I learned from this test and the problem I found**

The test showed that Copilot tried to send the question to the subagent, as I wanted, but the subagent couldn't access the `search` tool. Because of this, the main Copilot agent ended up searching the corpus itself.

The final answer was correct and included the right citations, but the problem was that it didn't actually come from the subagent. So even though the answer looked successful, the part I wanted to test wasn't working properly.

I tried three different ways of writing the tool permissions:

1. **`tools: mcp__corpus__search`:** I used the tool name from Claude Code, but the subagent still couldn't access it. Copilot's main agent did the search instead.

2. **`tools: mcp__corpus__search, corpus/search`:** This time, the subagent answered "The corpus does not cover this." This was wrong because the lisinopril label does contain information about angioedema. The problem was that the subagent couldn't search, so it assumed the answer wasn't available. This happened because its instructions told it to refuse when it couldn't find information, without distinguishing between an unsuccessful search and not having access to the tool.

3. **`tools: ['corpus/search', 'mcp__corpus__search']`:** I tried listing both tool names in brackets, but the result was the same as the first attempt. The subagent couldn't search, and Copilot had to do it.

From these tests, I realised that giving a subagent access to a tool is not as simple as putting its name in the configuration file. Claude Code and Copilot use different names for MCP tools (`mcp__corpus__search` and `corpus/search`), and in my case, Copilot wasn't making the tool available to the subagent.

The biggest issue was the second attempt, because the subagent gave a confident refusal even though the information was actually in the corpus. In a medical setting, this is important because the system needs to distinguish between information that doesn't exist in the documents and information it couldn't search for.

If I had more time, I would first test that the subagent can actually access the search tool before relying on its answers. I would also change its instructions so that, if the search tool isn't available, it says **"I could not search"** instead of **"The corpus does not cover this."** That way, a technical problem wouldn't be confused with missing information.

## Adding a document

**Already indexed?**

To keep track of the documents that have already been added, I use `index/documents.json`, which stores each document together with its SHA-256 hash. This lets the system check whether a file is new or if it has already been indexed.

- **Same name and same content:** If the document is already there and hasn't changed, the system doesn't create any new embeddings. It just returns "Already indexed … Nothing changed." This is useful because it avoids storing the same chunks twice and helps me stay within the limit of 1,000 embeddings per day.

- **Same name but different content:** If a document has been updated, for example when a newer version of a drug label is added, the system removes the old chunks and indexes the new ones. This way, it doesn't end up using information from two different versions of the same label.

**Demo**

I tested this using `uv run python add_document_demo.py`, and saved the results in `eval/add_document_demo.md`.

For the demo, I used question **u01**: *What is the recommended dose of apixaban for non-valvular atrial fibrillation?*

Apixaban was a good example because its label wasn't included in the original six documents. I used the FDA label stored in `docs_to_add/apixaban.json`, which creates 105 chunks when indexed.

| step | result |
|---|---|
| 1. Before | The system searched but only found information about warfarin, so it answered: "The corpus does not cover this." |
| 2. Add request, no approval | I tried adding the document without approving it, and the tool blocked the request: "Not added: the user did not approve adding this document." |
| 3. Add request, I typed `y` | After I approved it, the system added the file and returned: "Added 'apixaban' from apixaban.json: 105 chunks, 18608 words." |
| 4. Same file again | I tried adding the exact same file a second time. The system recognised it was already indexed and returned: "Already indexed: 'apixaban' (105 chunks) has the same content. Nothing changed." |
| 5. After | This time, the system could answer the question using the apixaban label. It gave the usual dose of 5 mg twice daily and explained when the dose should be reduced to 2.5 mg twice daily, with citations from the document. |

**A problem I found during the first test**

The first time I ran the demo, I found a problem that I hadn't expected. Even after successfully adding apixaban to the corpus, the agent still responded **"The corpus does not cover this"**, without even trying to search.

I saved this first attempt in `eval/add_document_demo_first_try.md`.

After looking into it, I realised that the problem was the description of the search tool. It still listed only the six medicines from the original corpus, so the agent assumed that apixaban wasn't available, even though I had already added it.

To fix this, I changed the tool description so that it is created using the documents currently in the index whenever the server starts. This means the list of available medicines can now reflect what has actually been indexed.

I also added a clearer instruction to the search tool and to rule 1 in `AGENTS.md`: the agent must search before answering **any question about a medicine**, even if that medicine doesn't appear in the list.

This test helped me realise that adding a document to the database isn't enough if the agent doesn't know it should look for it. The information was already there, but the agent wasn't using it because it relied too much on the tool description. After changing this, the system was able to search for apixaban and answer the question using the new label.

## Harness and guardrails

## Harness and guardrails

In `agent.py`, I use LangChain's `create_agent` with **gemini-3.1-flash-lite** and temperature set to 0. The agent connects to the tools in `server.py` through MCP, and I use `AGENTS.md` as the system prompt to tell it how it should behave.

**AGENTS.md rules**

I wrote nine rules for the agent, and included the reason for each one in the file:

1. **Always search first:** The agent has to use the search tool before answering any question, even if the medicine isn't in the current list.
2. **Only use information from the corpus:** It shouldn't add facts from its own knowledge or make guesses.
3. **Cite every claim:** Each piece of information needs a citation using the exact chunk ID returned by the search tool.
4. **Refuse when the answer isn't available:** If the passages don't contain the answer after a maximum of three searches, it must say exactly "The corpus does not cover this."
5. **Answer what is available:** If only part of the question can be answered, it should explain that part and clearly say what information is missing.
6. **Keep numbers accurate:** Doses, units, ranges, and patient groups must be copied exactly from the source.
7. **No patient-specific decisions:** The agent shouldn't decide what treatment an individual patient needs. It should refer them to the prescriber or pharmacist.
8. **Keep answers short:** Responses should be between 2 and 6 sentences.
9. **Only add documents when requested:** The agent can only use `add_document` if the user specifically asks it to.

**Approval step**

I also added an approval step before the agent can add a new document. The `add_document` tool is wrapped so that, before it runs, the terminal displays the file path and asks `Approve? [y/N]`.

If I type `y`, the document can be added. Any other response blocks the action and sends the message "Not added: the user did not approve" back to the model.

If there is no terminal available, like during evaluation or when running `check.py`, the request is automatically refused. I tested this in step 2 of the add-document demo, where the system correctly blocked the action without approval.

**Call limits and reliability**

To stop the agent from making too many requests, I set a maximum of 6 model calls and 4 tool calls per question using `ModelCallLimitMiddleware` and `ToolCallLimitMiddleware`.

I also added `ModelRetryMiddleware` and `ModelFallbackMiddleware` because I kept getting 503 "high demand" errors from Gemini during the evaluation. These help the system handle API problems instead of failing immediately.

**Extra guardrail: checking citations in the code**

Apart from the instructions in `AGENTS.md`, I wanted an extra check that doesn't depend only on the model following the rules.

After the agent generates an answer, my code looks at all the citation IDs it used and checks whether those exact IDs were actually returned by `search` during that question.

If the agent cites a passage it never retrieved, or gives an answer with facts but no citations, the system blocks the answer and replaces it with "The corpus does not cover this. (An answer was drafted but blocked …)".

Normal refusals are allowed, and the check also allows responses that are only confirming that a document was added. I keep the original answer in `eval/answers.jsonl` under `draft`, so I can still see what the model tried to say.

**Problems I found while testing**

The first time I ran the evaluation, this guardrail blocked three answers: q02, q03, and q06.

At first, it looked like the agent had used invalid citations, but after checking the answers, I realised the problem was actually in my code. The model sometimes included more than one citation inside the same brackets, like this:

`[metformin:contraindications:1, metformin:dosage_and_administration:3]`

My original parser only expected one citation per bracket, so it treated these answers as invalid even though the citations were correct.

The same thing happened during the first add-document demo. In step 3, the guardrail blocked the message confirming that the document had been added, even though that message wasn't making any medical claims.

I fixed both problems. The citation parser now separates multiple IDs inside the same brackets, and the citation check is skipped when the agent has only added a document. I also made `evaluate.py` check the saved drafts again, so I didn't need to spend more API calls repeating the same tests.

**Final result**

In the final evaluation, the guardrail was triggered **0 times**. All the answers only used citations from passages that had actually been retrieved.

This means it didn't catch any real hallucinations in my test set, so I can't say that it has already proven effective at stopping them. However, I still think it's a useful extra safety measure because it can block unsupported citations if they appear in the future.

One thing I learned from this part is that **the safety checks also need to be tested**. In my first run, the guardrail was blocking correct answers because of a mistake in the parser. So even though its purpose is to make the system safer, it can create new problems if it isn't working properly.


## Evaluation

I ran the evaluation using `uv run python main.py evaluate`, which tests the agent on all 37 questions. The answers are saved in `eval/answers.jsonl`, the judge's results in `eval/judgments.csv`, the results for each question in `eval/results.csv`, and the overall summary in `eval/summary.md`.

**Checks done in code**

I included several automatic checks to see whether the agent was following the rules. The code checks if the agent refused to answer, whether it used the exact refusal sentence, if its answer includes citations, and whether those citations actually came from passages retrieved during that run.

It also checks if the answer cites the expected document and whether the agent's searches found the expected section. This helps me understand where a mistake happened. I also recorded the number of searches, tokens used, and time taken for each question.

**LLM judge**

I used `gemini-3.5-flash-lite` to evaluate the answers. This is a newer and larger model than the one I used for the agent. I originally tried using the bigger Flash models, but they kept returning 503 errors throughout the day, so I used this one instead.

The judge receives the question, my reference answer, the passages retrieved by the agent, and the agent's final answer. It then gives two scores:

- **correct:** A score of 1 means the answer includes the same important information as the reference, such as the correct doses, numbers, or yes/no answer, without contradicting it. For questions that cannot be answered from the corpus, the agent gets 1 only if it refuses. It gets 0 if an important fact is missing or wrong, if it refuses a question it could have answered, or if it answers something that isn't covered by the corpus.

- **supported:** A score of 1 means all factual claims in the answer are supported by the passages the agent retrieved. If the agent refuses to answer, that also counts as supported. Otherwise, the score is 0.

**Results (37 questions)**

| outcome | count |
|---|---|
| correct and supported (answerable) | **30 / 30** |
| wrong | 0 |
| unsupported | 0 |
| wrong refusal | 0 |
| correct refusal (unanswerable) | **7 / 7** |
| answered an unanswerable question | 0 |

The automatic checks also showed that all 30 answerable questions included citations, all 37 responses used only valid citation IDs, and all 30 answerable responses cited an expected document.

**Agreement with the judge**

I also wanted to compare the judge's results with my own evaluation. I graded all 37 answers myself in `eval/human_labels.csv` before looking at the judge's scores. To do this, I used `eval/grading_sheet.md`, which shows each question, the agent's answer, and only the passages it actually cited.

The agreement was:

- **correct:** 97% (36 out of 37 questions).
- **supported:** 100% (37 out of 37 questions).

**The one disagreement: m01**

The only question where I disagreed with the judge was **m01**, about a patient taking warfarin who starts sertraline.

The judge gave the answer `correct = 1`, but I gave it `correct = 0`.

The reason is that the question specifically asks what **both drug labels** say about this combination. The reference explains that the sertraline label warns about an increased risk of bleeding and recommends careful INR monitoring. It also says that the warfarin label recommends more frequent INR checks when starting or stopping other medications.

The agent only searched once. Its search results did include a passage from the warfarin label, `warfarin:drug_interactions:4`, which mentions sertraline among the medicines that can increase bleeding risk. However, when I looked at the final answer, I noticed that **all the citations came from the sertraline label**.

The information the agent gave was correct, and everything it said was supported by the passages. That's why I agreed with the judge on `supported = 1`.

The problem is that it didn't fully answer the question. It covered the sertraline part but left out the specific recommendation from the warfarin label about more frequent INR monitoring when starting or stopping other drugs.

I think the judge was a little too generous here because it accepted an answer that only covered one side of a two-part question. I also realised that my automatic check had a similar limitation. It marked the expected document check as passed because it only required the answer to cite **one** of the expected sources, instead of all of them.

So, according to my own grading, the agent actually answered **29 out of 30 answerable questions correctly**, rather than 30 out of 30.

I also noticed another issue with **u01**: the agent correctly refused to answer, but it did so **without searching first**. Even though the final response matched the reference, it still didn't follow the rule that requires searching before every answer.

## Failures

According to the LLM judge, the system had 0 failures. However, when I reviewed the answers myself, I found **one failure in m01**, where the agent didn't fully answer a question that required information from two drug labels.

The agent had actually retrieved a relevant passage from the warfarin Drug Interactions section (`warfarin:drug_interactions:4`), but it didn't use it in the final answer. Instead, it only answered using information from the sertraline label. It also didn't try searching again to find more information about warfarin.

I classified this as a **wrong answer from the right passage**, because the information was available, but the agent didn't use everything it needed to answer the question properly.

While testing, I also found other problems. Some were fixed, while others still need work.

| problem | where | cause | status |
|---|---|---|---|
| Incomplete multi-part answer | m01 | The agent found a warfarin passage but ignored it. It only searched once, and neither the judge nor my code check noticed the missing part. | Not fixed. I would require a separate search for each drug in multi questions and check that every expected source is cited. |
| Subagent couldn't use `search` in Copilot | Editor transcript | Claude Code and Copilot use different names for MCP tools, so the subagent couldn't access the search tool. It even gave a wrong refusal in one test. | Not fixed in Copilot. The main agent had to search instead. |
| Correct refusal for the wrong reason | u01 during evaluation | The agent refused without searching because the tool description only listed the original six medicines. | Fixed by making the tool description dynamic and updating rule 1. I ran u02–u07 again, and all of them searched before refusing. |
| Agent didn't search after adding a document | First add-document demo | The agent still relied on the old tool description and assumed apixaban wasn't available. | Fixed by updating the tool description and search instructions. |
| Guardrail blocked correct answers | q02, q03, q06 in the first run, and demo step 3 | My citation parser didn't handle multiple citation IDs inside the same brackets. | Fixed by updating the parser. |
| Search tool crashed | m03 and m04 in the first run | ChromaDB couldn't open the index while another process was using it. | Added a retry in `retrieval.search` and ran both questions again. |
| Retrieval missed the answer | q14 with fixed chunks | The fixed window split the contraindication, so the correct passage didn't appear in the top 5. | Avoided by choosing section-based chunks. |
| Some answers took too long | Maximum of 272 seconds | Gemini kept returning 503 errors, which caused repeated attempts. | Added fallback models, but the API demand problem is still outside my control on the free tier. |

**What I would fix first**

If I continued working on this project, there are two main things I would focus on.

The first is **improving how multi-part questions are evaluated**. Right now, my code only checks whether the agent cited at least one expected source. That is not enough when the question specifically asks for information from two different labels.

I would change this so that the answer needs to cite **every expected source**, not just one. I would also make the judge's instructions clearer, so that it gives `correct = 0` whenever an important part of a multi question is missing.

The m01 example showed me why this matters. The answer was supported and sounded correct, but it didn't include everything the question asked for. Both the automatic check and the judge still accepted it.

The second thing I would improve is **the test set**. Even though the results were very good, I think part of the reason is that many of my questions were quite straightforward. Most of them ask for information that is written almost exactly the same way in the drug labels, so the agent doesn't have to do much beyond finding and repeating the right passage.

To test the system more properly, I would add harder questions. For example, questions involving dose calculations, information that seems different across sections, questions asking for decisions about a specific patient (which the agent should refuse), and different ways of asking the same question.

Finally, I would also make the search requirement an automatic check in the code, instead of relying only on the instructions in `AGENTS.md`. This would prevent cases like u01, where the agent gave the correct refusal but skipped the search completely.

Overall, **the main thing I learned is that getting the right final answer doesn't always mean the system worked correctly**. Sometimes it found the right information but didn't use all of it, and other times it gave the right response without following the process I had designed. That's why I think checking how the answer was produced is just as important as checking the answer itself.

## Decision

**Would I let users rely on it?**

I wouldn't let someone use this system as the only source for making a medical decision. However, I do think it could be useful as a **tool to quickly find information, as long as the user checks the original source before acting on it**.

The main advantage is that it can find relevant information in official drug labels much faster than someone reading through the entire document. It also gives exact doses, includes citations, and is supposed to refuse when the information isn't available.

In my evaluation of 37 questions, the agent didn't give any incorrect or unsupported medical claims. However, I did find one incomplete answer, m01, where it only explained what one of the two drug labels said. This is something I would take seriously in a hospital, because someone reading the answer might assume they have all the information they need, even though an important part is missing.

Also, one mistake in 37 questions doesn't mean the system is almost always going to be right. The actual error rate could still be several percent, especially because my test questions were relatively easy. I also found a case where the agent refused without searching, which shows that it doesn't always follow the process I gave it.

Because of this, I would only use the system under certain conditions.

- **What I would use it for:** Helping nurses and pharmacy technicians quickly find information in the official labels of the medicines included in the corpus. For example, checking maximum doses, contraindications, interactions, and monitoring requirements, without having to go through a label that might be 10,000 words long.

- **Safeguards I would keep:** Every answer must include citations, and the user should open the original passage before making any decision about a dose. New drug labels should only be added with human approval. I would also keep the citation guardrail active, make sure that questions about specific patients are referred to a pharmacist, and run the evaluation again whenever a label is added or updated.

**Cost per question**

Across the 37 questions, the system used around **4,000 tokens per question**. On average, about 3,890 were input tokens, mostly from the system prompt and the five retrieved passages, and around 120 were output tokens.

It also used around 1–2 query embeddings and made an average of 1.11 searches per question.

**Latency**

The median response time was **12 seconds**, while the average was **39 seconds**. The slowest answer took **272 seconds**.

The biggest delays came from Gemini returning 503 "high demand" errors and having to retry the request. This was mainly a problem with the free API tier, rather than the retrieval system itself.

Creating the embeddings for the original corpus required **577 embeddings**, but that only had to be done once.

Overall, I think the project works well as a way to make official drug information easier and faster to find. But I wouldn't consider it ready to make clinical decisions on its own. The evaluation showed that even when the answers look correct and have citations, the system can still leave out important information or skip a required step. For me, its best use would be **helping healthcare staff find and check information, not replacing their judgment or the pharmacist's advice**.

## AI use

I used Claude to help me with this assignment. It wrote most of the code, including `index.py`, `retrieval.py`, `server.py`, `agent.py`, `evaluate.py`, and `add_document_demo.py`. It also helped me write `AGENTS.md`, set up the subagent, create the test questions, and prepare the first draft of this report.

I decided to follow Claude's suggestions for the use case and how to build the system, but I was also involved in testing and checking that everything worked. I ran all the commands myself, reviewed the questions and reference answers using the original FDA labels, and approved the new document when the system asked for permission in the terminal.

I also did the human evaluation myself by going through the answers and filling in `eval/human_labels.csv`, rather than just relying on the automatic judge.

For the actual system, I used `gemini-3.1-flash-lite` as the agent's model and `gemini-3.5-flash-lite` to evaluate its answers.