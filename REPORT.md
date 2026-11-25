# Assignment 3 Report

- **Name**: Bernarda Andrade 
- **Student ID**: 19119
- **Group**: BBADBA 5A

## Use case
My users are family caregivers, basically people looking after an older parent or relative who takes a blood thinner like Eliquis, Xarelto or Pradaxa. They have everyday questions: she forgot a dose, can I crush the tablet, can he take aspirin with it, or which signs mean we have to call the doctor. They use the answer to decide if they give the dose, wait, or call the pharmacist or doctor. A wrong answer here is really dangerous, because a double dose or a bad combination can cause a bleed, and a missed dose can cause a stroke. "I don't know, ask your pharmacist" only costs a phone call. So the assistant has to cite everything, say when the documents don't cover something, and never decide a dose for anyone.

## Corpus

## Corpus

I used the official EU product information from the EMA for each medicine. Each PDF has the SmPC, which is for doctors, and the package leaflet, which is for patients. I downloaded them on 23 November 2026. They are © European Medicines Agency and can be reproduced if the source is acknowledged, and there is no personal data in them. I kept Lixiana out of the corpus at the start so I could add it later for the "adding a document" part.

| Document | URL | Version date | Pages | Raw words | Words kept |
|---|---|---|---|---|---|
| Eliquis (apixaban) | https://www.ema.europa.eu/en/documents/product-information/eliquis-epar-product-information_en.pdf | 25 Mar 2026 | 185 | 68,318 | 21,964 |
| Xarelto (rivaroxaban) | https://www.ema.europa.eu/en/documents/product-information/xarelto-epar-product-information_en.pdf | 7 Aug 2026 | 312 | 104,616 | 29,330 |
| Pradaxa (dabigatran) | https://www.ema.europa.eu/en/documents/product-information/pradaxa-epar-product-information_en.pdf | 4 Sep 2026 | 190 | 63,378 | 21,014 |
| **Total** | | | 687 | 236,312 | 72,308 |
| Lixiana (edoxaban), added later | https://www.ema.europa.eu/en/documents/product-information/lixiana-epar-product-information_en.pdf | 14 May 2025 | 67 | – | 7,626 |

## Ingestion

I extracted the text page by page with pypdf and removed the page number line. Then I split each PDF into its SmPC sections and leaflet sections, and I saved the section number, title and page for each one.

The main problem I had to fix was the size. The raw PDFs had 236,000 words, which would have been around 1,600 chunks (236,000 words divided into chunks of about 150 words each). That was way more than the free tier allowed, which was about 1,000 embeddings a day. Most of it was the same text repeated, because every PDF repeated the SmPC and the leaflet for each strength (2.5 mg, 5 mg, 15 mg, 20 mg and the children's versions). So I removed Annex II, the box and blister labels and the list of country contacts at the end of the leaflet. I only kept the SmPC sections a caregiver would actually need (1 to 3, all of 4, and 6.3 to 6.6), so I dropped section 5, which was clinical trials and pharmacology. Then I removed paragraphs that were repeated word for word between strengths. That left 72,308 words.

I tried two chunking designs. The fixed one used windows of 300 words with an overlap of 50 words, which gave 290 chunks. The section one made one chunk per section, split it at 250 words if it was longer, and added the section title to the text that got embedded. That gave 461 chunks.

I gave each chunk metadata: the source, whether it was the SmPC or the leaflet, the product (like Eliquis 2.5 mg tablets), the section, the page, the design, the file hash and the word count. I also saved a ready citation for each one, so the agent could show exactly where the answer came from, for example the Pradaxa package leaflet, section 3 "How to take Pradaxa", page 157. 

For embeddings I used Gemini's embedding model with 768 dimensions and stored everything in ChromaDB with cosine similarity. I only embedded new chunks and saved the query vectors, so running it again didn't use more quota.



## Test set

I wrote 39 questions the way a caregiver would ask them, I used help from my parents and they reviewd the questions because they are PHD doctors. This helped me have an actual reference of possible questions. Each one had a reference answer and where the answer was, like section 3 of the Xarelto leaflet. I wrote them before running any retrieval, so I wasn't tuning the system to the questions. 25 were single questions, where one passage answered it. 7 were multi questions, where you needed passages from two medicines or two sections. 7 were unanswerable: they were close to the topic but not in the documents, like alcohol, grapefruit, paracetamol, price, supplements, travel, and Lixiana before I added it.

One single example was q03: "My dad takes Xarelto 20 mg once a day and missed this morning's tablet. What should he do?" The answer was in section 3 of the Xarelto leaflet: take it as soon as he remembers and never more than one tablet a day.

One multi example was q26: "My mother takes Eliquis and my father takes Pradaxa for atrial fibrillation. What are the rules for a missed dose for each?" This needed section 3 of both the Eliquis and the Pradaxa leaflets, and the two rules were different.

## Retrieval
## Retrieval

I measured the hit rate on the 32 answerable questions. A multi question only counted as a hit if all of its expected passages were in the top k.

| Design | hit@1 | hit@3 | hit@5 | Words added to the prompt (top 5) |
|---|---|---|---|---|
| fixed + dense | 0.41 | 0.69 | 0.75 | 1,496 |
| **section + dense (chosen)** | 0.53 | **0.88** | **0.94** | **834** |
| fixed + hybrid (BM25 + dense) | 0.56 | 0.69 | 0.78 | 1,498 |
| section + hybrid | **0.59** | 0.78 | 0.91 | 884 |

I chose section + dense because it found the right passage in the top 5 for 94% of the questions, and it added about half the words to the prompt compared with fixed chunks. I think sections worked better because a leaflet section like "3. How to take Xarelto" was exactly what people asked about, while fixed windows cut sections in the middle. Hybrid search got the right passage first more often, because exact words like "dronedarone" matched. But it pushed other right passages out of the top 3 and top 5. Since the agent read all 5 passages, hit@5 mattered more to me than hit@1.

## Tools and subagent


### Tool descriptions (docstrings in `server.py`, which the model reads)

**`search(query)`**

> Search the official EU product information (EMA SmPC and package leaflet) for the blood thinners Eliquis (apixaban), Xarelto (rivaroxaban) and Pradaxa (dabigatran), plus any document added later.
>
> Use it for any question about these medicines: dosing, missed doses, how to take them, interactions with other medicines, warnings, side effects, overdose, surgery, storage. Write the query as a plain question or keywords and include the medicine name.
>
> Returns the 5 best passages, each headed by its citation: [source | SmPC or Package leaflet | product | section | page]. If no passage answers the question, the corpus does not cover it.

**`add_document(path)`**

> Add a PDF (EMA product information) to the searchable index.
>
> `path` is a file path, absolute or relative to the project folder. The file is extracted, cleaned, chunked, embedded and stored, so later searches can find it. If the same file is already indexed, nothing is done. If a different version of a document with the same name is indexed, its old passages are replaced. Returns what was indexed: source name, words kept and number of passages.

### One search result

`search("Can Pradaxa capsules be opened?")` returns 5 passages (section design, dense search). The first two:

```text
[pradaxa | SmPC | Pradaxa 75 mg hard capsules | 4.2 Posology and method of administration | p. 6]
VKA to dabigatran etexilate: The VKA should be stopped. Dabigatran etexilate can be given as soon as the INR is < 2.0. Method of administration This medicinal product is for oral use. The capsules can be taken with or without food. The capsules should be swallowed as a whole with a glass of water, to facilitate delivery to the stomach. Patients should be instructed not to open the capsule as this may increase the risk of bleeding (see sections 5.2 and 6.6).

[pradaxa | Package leaflet | Pradaxa 75 mg hard capsules | 3. How to take Pradaxa | p. 157]
Pradaxa can be taken with or without food. The capsule should be swallowed whole with a glass of water, to ensure delivery to the stomach. Do not break, chew, or empty the pellets from the capsule since this may increase the risk of bleeding. Instructions for opening the blisters [...]
```

### Subagent instructions (`.claude/agents/corpus-researcher.md`)

Tools: `mcp__corpus__search` only.

> You answer questions from family caregivers using only the `search` tool, which returns passages from the official EMA product information for Eliquis, Xarelto and Pradaxa.
>
> 1. Search first. Include the medicine name in the query. If the first results do not answer the question, search once or twice more with different wording (for example the leaflet's terms: "forget to take", "crushed", "other medicines").
> 2. Answer only from the returned passages, in plain language, in a few sentences.
> 3. After every claim, copy the passage's citation exactly as returned, e.g. `[pradaxa | Package leaflet | Pradaxa 75 mg hard capsules | 3. How to take Pradaxa | p. 157]`.
> 4. Never mix medicines: a rule for one does not apply to another. Say when a passage is for children or for a specific strength or condition.
> 5. If the passages do not answer the question, reply: "The product information I have does not cover this." and suggest asking a doctor or pharmacist. Do not guess or use outside knowledge.
> 6. Do not tell anyone to start, stop or change a dose beyond what the passage says.

### Transcript: `corpus-researcher` subagent in Claude Code

**User:** Can my father take his Xarelto 20 mg on an empty stomach?

**corpus-researcher:**

> No. Based on the product information, your father should not take Xarelto 20 mg on an empty stomach. It needs to be taken with food.
>
> - The patient leaflet says: "You must take Xarelto together with a meal. Swallow the tablet(s) preferably with water." The same section names one 20 mg tablet once a day as the usual adult dose to prevent stroke and blood clots. [xarelto | Package leaflet | Xarelto 15 mg film-coated tablets | 3. How to take Xarelto | p. 256]
> - The prescriber information for adults also says "The tablets are to be taken with food." [xarelto | SmPC | Xarelto 15 mg film-coated tablets | 4.2 Posology and method of administration | p. 58]
> - If he has trouble swallowing the tablet whole, it can be crushed and mixed with water or apple puree just before he takes it. For the 15 mg and 20 mg tablets, he should eat food right after the crushed dose. [xarelto | SmPC | Xarelto 15 mg film-coated tablets | 4.2 Posology and method of administration | p. 58] He should talk to his doctor before trying this. [xarelto | Package leaflet | Xarelto 15 mg film-coated tablets | 3. How to take Xarelto | p. 256]
>
> The leaflet for the lower 2.5 mg strength says that tablet "can be taken with or without food." [xarelto | Package leaflet | Xarelto 2.5 mg film-coated tablets | 3. How to take Xarelto | p. 239] That is only for the 2.5 mg tablet. It does not apply to his 20 mg tablet.
>
> These passages are filed under the 15 mg product heading, but they talk about the 20 mg dose directly. If you aren't sure how this applies to your father, ask his doctor or pharmacist.

A first attempt at the same question failed: the editor was still running the starter version of `server.py`, so all three of the subagent's searches returned "Error executing tool search". The subagent replied that it could not answer without passages and would not guess, and pointed to section 3 of the leaflet and the doctor or pharmacist. After reconnecting the `corpus` server, the run above succeeded.

## Adding a document

When I used the add document tool, it first checked if the file was already in the index. If it was the same file, it didn't change anything and just said that Lixiana was already indexed with the same content and nothing was changed. If it was a new version of a document that was already there, it deleted the old passages and replaced them with the new ones.

My unanswerable question was q36: "My mother takes Lixiana and forgot her dose this morning. What should she do?" Before adding the document, the agent said the product information didn't cover Lixiana and to ask a doctor or pharmacist. Then I added the Lixiana PDF, which was 7,626 words and 50 passages. After that it answered that she should take the tablet straight away, continue the next day as usual, and not take a double dose on the same day. It cited the Lixiana package leaflet, section 3 "How to take Lixiana", page 63.

The first time I tried this it didn't work. Even after adding Lixiana, the agent still refused and didn't even search. The rules file said it covered "three blood thinners", so it decided Lixiana wasn't its job. I changed the rules so it also covered documents added later, and so it always searched before saying a medicine wasn't covered. The 39 test answers were made before this change, and only the "after" answer used the new rules.

Adding the document also changed retrieval a little. The index went from 461 to 511 chunks. Section + dense stayed at 0.94 hit@5, but section + hybrid went down from 0.91 to 0.88, because the new leaflet's words competed in the keyword search.

## Harness and guardrails

The rules file was the system prompt, and it had 8 rules and a reason. The agent had to search first and only answer from the passages, and cite every claim exactly. If something wasn't covered, it had to start with "The product information I have does not cover this". It could never use one medicine's rule for another, and it had to say when a passage was for children or a specific strength. It could never make a personal dose decision, it had to put emergencies first, and it could only add a document when the user asked for it.

For the approval step, every time the agent tried to add a document, the program stopped and asked the person at the keyboard if they allowed it. If they didn't say yes, or there was nobody there, the document wasn't added and the agent was told not to try again. I also limited it to 6 model calls and 4 searches per question, so it couldn't get stuck in a loop.

My extra guardrail was a citation check in the code. Every citation in the answer had to match one that the search actually returned. If the answer had a citation that didn't exist, or had no citation and wasn't a refusal, the answer was blocked and replaced with a safe refusal.

It fired on q20: "Is there an antidote that reverses Pradaxa in an emergency bleed?" The model actually wrote the right answer (idarucizumab), but it merged two pages into one citation, the Pradaxa SmPC section 4.9 "Overdose" pages 20 and 7 together. That citation didn't exist in the search results, so the caregiver got the blocked message instead. The guardrail did what it was supposed to, because it couldn't tell a merged citation from a made up one, but in this case it cost a correct answer.

## Evaluation

The code checks looked at four things: whether all the citations were ones that were retrieved, whether the answer cited the expected source, whether unanswerable questions got a refusal and answerable ones didn't, and whether the guardrail fired.

For the judge I used Gemma 4 (31B). It's a different model family from the agent, so it wouldn't favour its own answers. It gave a yes or no on two things. Correct meant the answer agreed with the reference on everything that mattered for the caregiver's decision; a missing safety point or a contradiction counted as wrong, and for unanswerable questions correct meant it refused. Supported meant every fact in the answer was in the retrieved passages, and a refusal counted as supported.

I graded all 39 answers myself before I looked at the judge's results. The judge and I agreed on correct 94.9% of the time (37/39) and on supported 97.4% of the time (38/39). We disagreed on three. On q10, the judge wanted it to say "tell the doctor first" and I was fine with the answer. On q17, the judge accepted an answer that was incomplete. On q31, the judge missed a reasoning mistake and marked it supported. So the judge was stricter than me once and more lenient twice, and q31 showed why a human check was still needed.

| Result (39 questions) | |
|---|---|
| Answerable, correct and supported | 23 / 32 |
| Unsupported answers | 0 |
| Correct refusals (unanswerable) | 7 / 7 |
| Wrong refusals (answerable but refused) | 6 |
| Answers whose citations were all valid | 33 / 39 |

## Failures

9 answerable questions failed. The biggest cause, with 6 questions (q18, q20, q23, q24, q27 and q28), was the citation guardrail blocking a right answer. In all of them the model merged two citations into one, so the check didn't recognise it.

2 questions were incomplete: the right section was found, but not the paragraph with the missing fact. q17 didn't say to contact the doctor, and q29 missed the Eliquis rule of stopping 48 hours before surgery.

1 question, q31, was wrong reasoning from the right passage. It said the 2.5 mg dose depended on her creatinine, but the mother's age and weight already met two of the criteria, so the lower dose applied either way.

There were no retrieval misses at the section level and nothing was made up. The guardrail also fired on q35 (paracetamol, unanswerable), because the model refused with "does not cover whether" instead of the exact sentence. It was still a refusal, so no harm was done.

The first thing I would fix is the citation check. If it split merged citations and checked each part, those 6 correct answers would have gone through, so correct answers would go from 23/32 to about 29/32 without making the guardrail weaker. After that I would retrieve more chunks (8 instead of 5) for long sections like surgery and side effects.

## Decision

## Decision

I would let caregivers use it to look up what the official leaflet says: how to take the medicine, what to do after a missed dose, how to store it, and which signs need a doctor. I would not let them rely on it for dose decisions, because q31 showed it could get the dose criteria wrong even with the right passage. The safeguard is the citation guardrail. In 39 questions it gave 0 unsupported answers, and every answer could be checked against the leaflet page it cited. The downside is that it refused too much, which the merged citation fix would solve. Every answer also ended by telling them to follow the prescriber or pharmacist.

On average each question used 3,985 input tokens and 201 output tokens with Gemini 3.5 Flash Lite, plus one query embedding, which was saved when I ran it again. With Google's standard paid prices ($0.30 per 1M input tokens, $2.50 per 1M output tokens and $0.20 per 1M embedding tokens), that was about $0.0017 per question, or about $1.70 for 1,000 questions. Embedding the whole corpus once (72,308 words, about 95,000 tokens) would cost about $0.02 per design. I used the free tier, so it actually cost me $0. If the token counts left out the model's thinking tokens, which Google bills as output, the real cost would be a bit higher.

The median time per question was 18 seconds and the mean was 59.6 seconds. The mean was high because of rate limit retries from the API; one question took 1,188 seconds.

## AI use

I used Claude Code (Claude Opus) during this assignment. It wrote the code for indexing, retrieval, the tools, the agent and the evaluation, and it wrote the subagent file and the rules file, based on the use case and the documents I chose. It also helped me with parts of the report like the tool descriptions and the costs and efficiency calculations of gemini agent. 