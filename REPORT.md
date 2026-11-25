# Assignment 3 Report

- **Name**: Jimena Sánchez
- **Student ID**: 20104
- **Group**: PPLEDBA 5A

---

## Use case

### Who asks

I built this for a political journalist or an electoral analyst covering the Spanish municipal and regional elections of 23 May 2027 and the general election due by 22 August 2027. Before they publish a claim about the parity law passed in the XV Legislature, they need to know two things: does the parliamentary record actually support it, and in which version of the text?

Take a claim like "small towns are exempt from the parity rule". Is it true? It depends on which text you read. In the text the Congreso finally approved, yes: municipalities of 3,000 residents or fewer are exempt, and those of 3,000 to 5,000 only have to meet a 60/40 rule. But in the bill the Government introduced, and in the Ponencia's report, there is no exemption at all. So the same sentence can be right or wrong depending on the stage, and that is exactly the kind of question I wanted the tool to handle.

### What they do with the answer

For the journalist, the answer feeds a yes-or-no decision: can I back this claim with a primary source? If yes, they click the CVE, check the quotation against the signed PDF, and use it in a fact-check, a briefing note or a graphic. If no, they drop the claim or go and look for it by hand.

That verification step explains two of my design choices, verbatim quotes and a CVE in every citation. It also answers an obvious objection: if the journalist checks the PDF anyway, why do they need the tool? Because the tool's job is to find the right passage, not to replace the PDF. Finding one provision by hand across four documents and about 63,000 words takes around ten minutes, whereas checking a quotation the tool has already found takes about one.

### Why this corpus

The bill, Proyecto de Ley Orgánica 121/000001, amends the LOREG (LO 5/1985) in its *Artículo primero*. In other words, it governs how candidate lists are drawn up for the very elections my user is covering, so claims about it are going to circulate all through the campaign.

I could have indexed just the final text, but the error I most wanted to prevent is confusing one stage of the bill with another, and you cannot test for that with only one version. So the corpus holds the Congreso trail from December 2023 to July 2024: the Government's *proyecto*, the *informe de la ponencia*, the plenary debate and the text finally approved. With all four, the agent can answer both "what did the Government propose, and what was approved?" and "who said what?". I left the Senado stage and the amendments out on purpose, and AGENTS.md states them as boundaries (rule 6).

### What a wrong answer costs

The two kinds of mistake are not equally expensive. If a wrong answer gets published, the best case is a correction. The worst case is a false public claim about a party in the middle of a campaign, which is precisely when it spreads fastest and when the correction never travels as far. On the other hand, "NO CONSTA EN EL CORPUS" costs the journalist about ten minutes with the PDF, and it is always safe to publish.

Not all wrong answers are equally bad either. The worst is a draft reported as law, a *proyecto* article presented as if it had been enacted, because that is a false claim about the law itself. Next is misattribution, a position or a quotation given to the wrong party or deputy. Last, though still costly, is an unsupported detail: something small that is not in the source but ends up copied into a caption.

This ranking is what shaped the design. AGENTS.md rule 4 makes the agent name the *trámite* (the stage of the bill) for every quotation, and the judge scores stage correctness as a separate dimension. Interestingly, the evaluation found no case of the first type. Three of the four unsupported claims (q15, q16, q26) were of the third type: the agent added a deputy's first name that was not in the retrieved text. That looks harmless, but it is exactly the detail a journalist copies without checking. Following the same logic, I treat the three wrong refusals as the cheaper failure.

### Why hallucination is especially easy here

In this corpus, the same article can exist in up to three versions, and the wording changes between them. The rule on substitute candidates is a good example. The *proyecto* and the *ponencia* both say «A las listas de suplentes se aplicarán las reglas contenidas en el anterior apartado», while the approved text applies the alternation rule «en el conjunto de las listas, sin separar titulares y suplentes».

So imagine an answer that mixes a superseded draft with a real debate quotation. It reads exactly like a correct one. And the citation actually makes it worse, because the CVE and the quotation are both real, they just come from the wrong stage. A journalist who clicks through finds the exact words in the signed PDF and, reasonably, stops checking. The CVE check catches invented text, but it cannot catch a wrong *trámite*, which is why rule 4 forces the agent to say which stage every quotation comes from.

There turned out to be a second trap of the same kind, and this is the one the evaluation actually hit. A *preámbulo* describes other laws, so a passage can come from the right document and the right stage and still be about a different norm. In q26 the agent described the list rule correctly, but the passage it cited was about the Castilla-La Mancha and Andalucía electoral laws. This time the claim happened to match this law. Wherever the two differ, though, the same mechanism would produce a false claim behind a citation that looks perfectly valid.

### Non-goals

The agent does not judge whether the policy is good, guess why a party voted the way it did, or predict what anyone will do (AGENTS.md rule 7). That is the journalist's job, and the congreso.es reuse conditions forbid distorting the meaning of the information anyway. It is also not a source for the law in force. The corpus stops at the Congreso in July 2024, with no Senado stage, no BOE text and no later amendments, so it can tell you what the Congreso approved but not what applies today. Anything outside this one Congreso trail gets a stated boundary rather than the nearest match.

---

## Corpus

The corpus is the parliamentary record of one organic law as it went through the Congreso de los Diputados: expediente 121/000001, the *Proyecto de Ley Orgánica de representación paritaria y presencia equilibrada de mujeres y hombres*. Three of the four documents are successive versions of the same legal text, so they can be compared article by article. The fourth is the plenary debate, which records who said what.

Table 1: The four documents of the corpus.

| Document | What it is in the procedure | Date | Words |
|---|---|---|---:|
| *Proyecto de Ley Orgánica* (`BOCG-15-A-1-1`) | the bill as the Government sent it to the Congreso | 15/12/2023 | 12,464 |
| *Informe de la Ponencia* (`BOCG-15-A-1-4`) | the text proposed by a working group of deputies from every group, after the amendments | 25/06/2024 | 14,841 |
| *Diario de Sesiones del Pleno* (`DSCD-15-PL-54`, pp. 4–20 and 32–39) | the plenary debate and the vote on the whole bill | 27/06/2024 | 16,855 |
| *Aprobación definitiva por el Congreso* (`BOCG-15-A-1-8`) | the text the Congreso finally approved | 31/07/2024 | 19,274 |
| | | **Total** | **63,434** |

### What the documents represent

To understand what the agent can and cannot say, it helps to remember how a bill becomes law in Spain, because it does not go straight from proposal to law. The Government's text was published with a period for amendments and sent to the Comisión de Igualdad. A Ponencia, with deputies from every group, studied the amendments and proposed a revised text. The Comisión then issued its dictamen, and the Pleno debated and voted on 27 June 2024. Because it is an organic law, the bill needed an absolute majority of the 350 seats, 176 votes, in a final vote on the whole text. It got 177 in favour and 171 against, out of 348 votes cast, so it passed with one vote to spare. The bill then went to the Senado, and on 23 July 2024 the Congreso approved it definitively under article 90 of the Constitution, which is the step where it decides on whatever the Senado did. The approved text was published on 31 July.

Seen this way, the corpus covers four points along the path, not the whole path. The Comisión's dictamen, the Senado stage and the vote of 23 July are all missing, and that has two consequences I had to keep in mind. First, the agent can say that a change happened between two documents, but not which step made it. If an article reads differently in the *ponencia* and in the approved text, all the record shows is that it changed after 25 June. It could have been the Comisión, the Pleno or the Senado. That is why my test questions ask between which documents something changed, and never who changed it. Second, the approved text is not the law as published in the BOE. It is the closest thing to the law in force that the corpus has, but it is still not the same thing.

I also realised while reading it that the law is much broader than its title. Apart from candidate lists, it changes rules on company boards, the Tribunal Constitucional, the Consejo General del Poder Judicial and professional associations. It even includes a provision on how the budget-stability objectives are approved if the Senado rejects them, which several opposition speakers in the debate criticised as having nothing to do with the bill. So a claim about "the parity law" could be about any of these, and a question about one of them can look out of scope when it is not. That is exactly what happened in q07, as I explain later.

### The document held back

The record also includes `BOCG-15-A-1-2`, *Enmiendas e índice de enmiendas*: 110 amendments filed by the groups and published on 7 May 2024. In real-world terms, they show what each group wanted to change before the negotiation. For a fact-checker, though, they are probably the most dangerous text in the whole trail, because most of them quote the wording they propose. The document is full of text that reads like the law but is not the law, and most of it was never adopted. At 58,146 words, it is 92% of the size of the other four documents together.

I kept it out of the base corpus and saved it for the add-document demonstration. This means the retrieval and answer evaluations were measured on the four documents above. Only the add-document experiment and the subagent transcript come from the five-document index, and both say so.

### Brief requirements

The corpus has four documents and 63,434 words, so it meets the minimum of three documents and 50,000 words. All four are official publications, freely available on congreso.es, and its [aviso legal](https://www.congreso.es/es/cem/aviso-legal) allows reuse as long as (a) the content is not altered, (b) its sense is not distorted, (c) the source is cited and (d) the date of the last update is given. These conditions are not just a formality here, because they shaped the system. Conditions (c) and (d) are why every answer cites its document and date, (a) is why provisions are always quoted verbatim, and (b) is why the agent reports positions without characterising them.

As for personal data, the only personal data in the corpus are the names of deputies and Government members acting in their official role, either as members of the Ponencia or as speakers in the debate. With each passage I keep only the speaker as the record names them, their group and their role.

Finally, every BOCG and *Diario de Sesiones* publication carries a *Código de Verificación Electrónica* (CVE) that identifies the electronically signed original. Every citation includes it, so anyone can check a quotation against the signed source rather than having to trust my index.

---

## Ingestion

The pipeline lives in `index.py` as a set of importable functions. I did it this way because the add-document tool in `server.py` needs to run a new document through exactly the same steps, and I did not want two copies of the same logic drifting apart. In short, it takes a PDF from congreso.es, turns it into chunks that each know where they came from, embeds them with Gemini and stores them in ChromaDB under `index/`.

Table 2: The ingestion pipeline.

| Step | Function | What it does |
|---|---|---|
| fetch | `fetch` | downloads the PDF with a descriptive User-Agent (congreso.es answers 403 to a bare client) and caches it in `corpus/` |
| extract | `load_document` | reads each page with pypdf, keeps only the pages that belong to this bill, and sets the cover and *sumario* aside for metadata |
| clean | `clean_page` | removes the running head and the CVE line, repairs hyphenated words and rebuilds paragraphs |
| chunk | `chunk_file` | picks a chunking strategy by document type and attaches metadata to every chunk |
| embed and store | `embed_and_store` | embeds only chunks with no cached vector and writes them into Chroma |

### Source and location

For this use case, the most important requirement is that every chunk carries its source and location, because a citation the journalist cannot trace back to a page is useless to them. The source fields are `doc_id`, `titulo`, `tramite`, `genero`, `fecha`, `cve`, `url` and `expediente`. The location fields are `page`, `page_to`, `seccion`, `seccion_titulo`, `ordinal` and `location_label`. Debate chunks also record the speaker (`interviniente`, `grupo`), and `chunk_strategy`, `content_sha256` and `superseded` are there for bookkeeping. `location_label` is the citation a person actually reads, for example `BOCG-15-A-1-8 · Artículo primero · p. 12-13`, and it is also what the evaluation scores against.

Some of this metadata was harder to get than I expected. The *Diario de Sesiones* records the whole plenary session, not just this bill, so I only keep pages 4–20 and 32–39, which contain this bill's debate and vote. The cover and *sumario* are not indexed, but I still read them, because in the debate a speaker's group only appears in the *sumario*. Reading it from there resolved all 14 speakers. The amendments had a different problem: the group comes right after each heading with no punctuation around it, so I match it against the group names found in the corpus. That resolved all 110, including the 23 that Socialista and Plurinacional SUMAR signed jointly.

### Chunking

I built two chunking strategies so that the retrieval evaluation had something to compare.

Table 3: Chunking strategies.

| Strategy | Rule | Chunks | Mean words | Max words |
|---|---|---:|---:|---:|
| `fixed_200` | 200-word windows, 40-word overlap, no structure | 398 | 199.0 | 200 |
| `structured` | one chunk per article, disposición, amendment or speaker turn; longer units split at 400 words with 60 words of overlap | 309 | 228.4 | 400 |

My reasoning for the structured strategy was simple: it should follow the units a journalist actually cites. Nobody quotes "words 1,400 to 1,600 of the BOCG"; they quote *Artículo primero*, or what a named deputy said. So `structured` follows the 107 structural sections of the four documents. When a unit is too long and has to be split, each piece gets its position in the label, for example `preámbulo (8/21)`. That little suffix later turned out to cause two of the three broken citations, which I come back to in *Failures*.

### Defects found along the way

Three extraction defects turned up, and what they had in common is that everything looked fine. None of them raised an error, and the word counts stayed plausible the whole time. The damage was in the structure.

The first was about headings. Paragraphs were rebuilt by joining lines until one ended in punctuation, but legal headings such as `CAPÍTULO I` do not end in punctuation, so they were swallowed by the paragraph above them. As a result, only 5 of the 18 articles in the approved text were being detected, and one of the missing ones was *Artículo primero*, the single most important provision in the corpus. The fix was to end the paragraph whenever a structural heading appears. The second was a regex problem: `Artículo decimotercero` matched an earlier alternative in the ordinals pattern and got cut to `Artículo decimo`, which merged six articles under one label until a missing word boundary (`\b`) was added. The third was about pages. Every piece of a long section cited the first page of the section, so a journalist checking the citation would not have found the quotation where it said it was.

A fourth defect, in the embeddings, was the most worrying, and it was found by simple arithmetic. Chunks were being embedded in batches of 16 by passing a list of strings to `embed_content`. In `google-genai` 2.34.0, though, a plain list of strings is read as the parts of one single content, so the API returned one vector per batch, an embedding of sixteen passages mixed together. The loop that stored them paired keys with vectors using `zip`, which stops at the shorter list. So it saved that one blurred vector under the first chunk and silently threw away the other fifteen, while the log happily kept printing `144/398`. What gave it away was a count: after nine batches, the cache held exactly nine vectors. If nobody had noticed, the index would have held about 44 vectors for 707 chunks, and every retrieval number in this report would have been measuring noise. The fix sends one `Content` per text, and, more importantly, the pipeline now raises an error whenever the number of vectors returned differs from the number sent, so this can never fail silently again.

### Embedding

I use `gemini-embedding-2` at 768 dimensions, which is lower than the default, to keep `index/` well under its 90 MB limit. After the reduction each vector is re-normalised, because the reduced output is no longer unit length and cosine similarity assumes it is. Chunks are embedded as `RETRIEVAL_DOCUMENT` and questions as `RETRIEVAL_QUERY`, so the model knows which side of the match each text is on.

The quota was a real constraint. The free tier allows about 1,000 embeddings a day, and a cold build of both strategies needs 707. So every vector is cached on the SHA-256 of its text and saved after every batch. That way, re-chunking reuses every chunk whose text did not change, a crash or the daily limit loses nothing, and the pipeline simply waits and retries when the API returns a rate-limit error (HTTP 429).

---

## Test set

`eval/questions.csv` holds 32 questions: 20 `single`, 6 `multi` and 6 `unanswerable`, which is above the required 30, 5 and 5. The format follows `eval/README.md`.

Every question comes from a specific passage that was read in full, and its `expected_source` and `expected_location` were copied from the chunk metadata, so they match what the retriever actually returns. I also checked that every expected pair (document and section) really exists in the index. This matters more than it seems: it means that when retrieval misses, it is always the retriever's fault and never a typo in the test set. Finally, I reviewed the whole set and replaced four debate questions of the form "what did group X say?", because they were too vague to grade (see *AI use*).

### What each kind tests

The 20 `single` questions each ask for one provision or one intervention: 13 in the approved text, 4 in the *proyecto* and 3 in the debate. They test whether the agent can find the right passage, quote it and name its stage.

The 6 `multi` questions need two passages, and this is where I put most of the weight. Four of them are stage comparisons on *Artículo primero*: three compare the *proyecto* with the approved text (q21, q23, q24), and one compares the *ponencia* with the approved text (q22). I over-sampled these on purpose, since version confusion is the risk this whole corpus is built around. The other two combine two provisions of the approved text (q25), or the approved text and the debate (q26).

The 6 `unanswerable` questions are near misses rather than obvious rejects. Each one sits just outside one stated boundary: the amendments, the Senado, the BOE publication, a constitutional challenge, an autonomic parliament and the Comisión stage.

### Two examples

q21 is a good example of why the `multi` questions are hard. It asks *¿Cambió la regla sobre las listas de suplentes entre el proyecto de ley y el texto finalmente aprobado?* The *proyecto* gives substitutes a rule of their own («A las listas de suplentes se aplicarán las reglas contenidas en el anterior apartado»), and the approved text replaces it with «La regla anterior se aplicará en el conjunto de las listas, sin separar titulares y suplentes». With only one of the two passages, the agent can give a confident and wrong answer. q23 and q24 are even harder, because their answer is "no": the *proyecto* simply does not contain what the approved text added later. To answer, the agent has to treat an absence as evidence, and, as it turned out, q23 is one of the wrong refusals.

q27, the first unanswerable question, is the hardest kind of near miss. It asks *¿Qué texto proponía la enmienda número 24 del Grupo Parlamentario Vasco (EAJ-PNV)?* The *Diario de Sesiones* names amendment 24 and records its vote (25 in favour, 296 against and 26 abstentions), so retrieval does find passages about that exact amendment. What it never finds is the amendment's text, which is in `BOCG-15-A-1-2`. So the agent faces the difficult situation where it has found something relevant that still does not answer the question. q07 turned out to be the mirror image: an answerable question that mentions the Senado, which the agent wrongly refused.

### Order and weaknesses

The order of the questions matters in two places. q01 is the question `check.py` sends through the server and the agent, so I kept it short and unambiguous. It is easy for a person, but, as *Retrieval* shows, not for the retriever. q27 is the first unanswerable question, which is the one the add-document demonstration uses, so it had to be the question the held-back document answers.

Looking back, two questions are weaker than I intended. q13 expects the chair's turns in the debate, a label that covers 78 chunks, so almost any chunk from the debate counts as a hit. And q24 is labelled `multi` but only really asks about the *proyecto*. I list both under *Failures*.

---

## Retrieval

I compared four designs. Only the first two cost embeddings; the other two add a filter or a lexical ranking on top of the winning index, which is what let me fit the whole comparison inside one day's quota.

Table 4: The four retrieval designs.

| | Design | What it tests |
|---|---|---|
| A | `fixed_200`, dense | baseline with no structure |
| B | `structured`, dense | does chunking on articles and speaker turns help? |
| C | B + `tramite` filter | does restricting the search to one stage fix version confusion? |
| D | B + hybrid BM25 and dense, fused with reciprocal rank fusion (RRF) | does exact word matching help with article names and legal phrases? |

Hit rate is measured on the 26 answerable questions at k = 1, 3 and 5. A retrieved chunk counts as a hit when it comes from the expected document and covers the expected section. For the `multi` questions I report two versions: strict, where every expected passage has to be in the top k, and lenient, where one is enough.

Before any of the comparisons made sense, a measurement bug had to be fixed. `fixed_200` first scored 0.000 at every k, which is not a weak baseline but an impossible one. The scoring rule checked whether the expected section name appeared in the chunk's label, and a fixed-window chunk has no section, only a page, so it could never score however good the retrieval was. For chunks without a section, the rule now checks whether the chunk's pages overlap the expected section's pages. Without this fix, the report would have claimed that structure lifts hit rate from 0% to 73%, which is simply false.

Table 5: Hit rate by design (four-document corpus, 707 chunks).

| Design | hit@1 | hit@3 | hit@5 | multi strict@5 | Words sent at k = 5 |
|---|---:|---:|---:|---:|---:|
| A `fixed_200`, dense | 0.154 | 0.308 | 0.423 | 0.167 | ~995 |
| B `structured`, dense | 0.269 | 0.577 | **0.731** | **0.333** | ~1,142 |
| C `structured` + `tramite` filter | **0.346** | 0.538 | 0.654 | 0.167 | ~1,142 |
| D `structured` + hybrid (RRF) | 0.308 | **0.654** | 0.692 | **0.333** | ~1,142 |

### What the results show

The first thing the table shows is that structure clearly helps. B beats A at every k, going from 0.423 to 0.731 at k = 5, for only about 15% more text in the prompt, and on `single` questions the gap is even bigger, 0.850 against 0.500. This makes sense to me: a fixed window cuts provisions in half and mixes the end of one article with the start of the next, which blurs exactly the passages the questions are about.

Design C confused me at first. It has the best hit@1 of all four, but its strict multi score is as bad as the baseline's. Why would a filter help and hurt at the same time? The answer was in how the evaluation applies it. The filter is not chosen by the model; a keyword rule infers it from the question, and the first cue that matches wins. That causes two separate problems. q21, q23 and q24 all mention "el proyecto", so they get filtered to the *proyecto* alone, which means they can never retrieve the approved text they are supposed to be compared with. And q13, which is about the plenary vote, mentions "proyecto de ley orgánica" and misses at every k, simply because the bill's own name contains the cue. So I would not read C as a verdict on filters in general. What these numbers show is that a filter imposed by a rule hurts. They say very little about a filter the model chooses for each query.

I also had a hypothesis going in, and it did not survive. I expected the stage comparisons to fail under A and B and to recover under C. In fact, on q21–q24 strict@5 is 1/4 for A, 2/4 for B, 1/4 for C and 2/4 for D, while lenient@5 is 3/4 or 4/4 for every design. In plain terms, retrieval almost always finds one version of an article, but usually not both. And that is exactly the situation where a fluent, well-cited, wrong answer becomes easy to produce.

There is also something hit rate does not capture, which I only noticed by looking at q01. These scores embed the user's question exactly as written, but the agent never searches that way: it writes its own query and can set its own filter. Embedded as written, q01 (*¿Cuándo entra en vigor la ley orgánica de representación paritaria?*) does not retrieve its passage in the top 5 under any design. Yet in the evaluation run, the agent searched for «entrada en vigor», filtered to `aprobacion_definitiva`, and found the right *disposición final* at rank 1. So hit rate measures the retriever on the user's wording, not on what the agent's own searches actually find. Measuring those searches directly is the next thing I would add.

### Chosen design

In the end I chose B, with the filter left as an option. I decided on hit@5 and strict multi@5, because the agent reads the top five chunks by default, and the questions this corpus exists for need both stages inside that window. On both measures, B is the best or tied for best. `evaluate.py` actually names C, because it ranks designs by hit@1, but I think that is the wrong criterion here, since C costs 8 points of hit@5 and halves the multi score. So `server.py` loads B and exposes `tramite` as an optional argument the model sets for each query. That way, it keeps C's precision on one-stage questions without its blind spot on the others, and q01 suggests the model uses it well. D is the clearest improvement left on the table, with better hit@1 and hit@3 and the same multi score, so hybrid search is the first thing I would build next.

All figures above come from the four-document corpus, before the add-document demonstration. They are saved in `eval/retrieval_summary_4docs.csv`, with per-question results in `eval/retrieval_4docs.csv`, and `uv run python eval/retrieval_4docs.py` reproduces them from the committed index by leaving out `BOCG-15-A-1-2`.

### Adding a document made retrieval worse

I expected adding a relevant document to make the index better, or at least not worse. The add-document demonstration added the amendments, 209 chunks, which means 68% more `structured` chunks and almost double the words, so I re-ran the same retrieval evaluation to see what had changed.

Table 6: `structured` before and after adding the amendments.

| Index | hit@1 | hit@3 | hit@5 |
|---|---:|---:|---:|
| 4 documents | 0.269 | 0.577 | **0.731** |
| 5 documents | 0.154 | 0.385 | **0.500** |

Hit@5 fell 23 points. An amendment chunk is now the top result for 18 of the 32 questions, and six answerable questions lost their hit at k = 5 (q02, q04, q10, q11, q21 and q22) while none gained one. Two of those six are stage comparisons, which are precisely the questions this corpus is for.

Once I looked at the amendments, the reason was obvious. Of the 110 amendments, 78 contain their proposed wording in quotation marks, and most of that wording is a modified version of an article in the bill. To an embedding model, these are near-duplicates of the very articles the test set asks about: the same vocabulary, but none of the authority. Similarity simply cannot tell "the law says X" apart from "a rejected amendment proposed changing X".

This has two consequences. The first is that adding a document can make an index worse. The tool made the corpus able to answer q27, which it really could not answer before, but at the same time it lost six answers it used to find, and nothing in the pipeline reported it. For a journalist, a tool that quietly gets worse at questions it used to answer is a real risk. The second is that the committed index can no longer reproduce the A/B comparison. `add_document` only writes to the active strategy, so `fixed_200` still holds four documents while `structured` holds five, and re-running `main.py evaluate` gives the five-document figures. The fix would be to index into every strategy, or to evaluate against a fixed snapshot of the corpus.

On the positive side, this is the strongest argument I have for the `tramite` and `genero` filters. The amendments have their own values for both, so either filter excludes them completely. The numbers agree: on the five-document index, the filtered design reaches 0.538 at k = 5 and the hybrid 0.615, compared with 0.500 for plain `structured`.

One last idea I tested was whether the agent could refuse based on similarity alone, and it cannot. On the four-document index, the mean top-1 similarity is 0.728 for answerable questions and 0.713 for unanswerable ones, and every unanswerable score (0.678 to 0.763) falls inside the range of the answerable ones (0.644 to 0.856). Because the unanswerable questions are near misses, they retrieve passages that really are related, so the score cannot separate "this is the answer" from "this is about the same topic". The refusal has to come from the model actually reading the text, which is what rule 5 asks it to do.

---

## Tools and subagent

### The MCP server

`server.py` exposes two tools over stdio, and it imports `index.py` instead of reimplementing any part of it.

The first tool, `search(query, tramite="", genero="", grupo="", k=5)`, returns the closest chunks. Each one comes with its citation (`[doc_id · localización · p. N · CVE:…]`), its trámite and date, the speaker's group if it comes from the debate, the URL of the signed PDF, the similarity score and the verbatim text. The filters are optional, and the model decides for each query whether to use them. I think of the tool's description as the agent's map of the corpus. It names the four documents, warns that the same article exists in several versions, and lists what the corpus does not cover: the Senado, the amendments, other bills, autonomic parliaments and anything after July 2024. Since the model reads it before every call, it is the cheapest way I found to improve refusals. Its weakness is that it does not change when the index changes, which I come back to in *Adding a document*.

The second tool, `add_document(path)`, runs a PDF through the same pipeline as the original build, rejects anything that is not a PDF or sits outside the project, and reports how many embeddings it spent. What it does with a document that is already indexed is explained in *Adding a document*. The server itself does not ask for approval. That is the client's job: the `agent.py` harness asks, and the subagent cannot call this tool at all.

I checked that the server works over MCP. Started the way `.mcp.json` starts it (`uv run server.py`), it completes the handshake and lists both tools in 0.4 s, and `check.py` calls `search` through it successfully. This is a real result, cut to its first fragment:

```
5 fragmentos para "¿Cuándo entra en vigor la ley orgánica de representación paritaria?"
  ·  índice: structured  ·  filtros: ninguno

[1] [BOCG-15-A-1-8 · preámbulo (1/21) · p. 1-2 · CVE:BOCG-15-A-1-8]
    trámite: aprobacion_definitiva  ·  fecha: 2024-07-31  ·  similitud: 0.772
    https://www.congreso.es/public_oficiales/L15/CONG/BOCG/A/BOCG-15-A-1-8.PDF
    «XV LEGISLATURA Serie A: PROYECTOS DE LEY 31 de julio de 2024 Núm. 1-8 Pág. 1 ...»
```

It is the q01 problem from *Retrieval* again. Searched exactly as written, the question returns the cover page of the approved text instead of the *Disposición final decimoquinta* that actually answers it.

### The subagent

`.claude/agents/corpus-researcher.md` defines a subagent whose only tool is `mcp__corpus__search`, so it cannot read files or add documents. Its seven rules follow AGENTS.md: search before answering and use the `tramite` filter for one-stage questions, search once per trámite when comparing stages, cite every factual sentence, quote legal wording verbatim, name the trámite, reply exactly `NO CONSTA EN EL CORPUS` when the results do not contain the answer, and report without characterising.

I ran it from Claude Code (the full transcript is at the end of this section) and asked what changed in artículo 44 bis between the Ponencia's report and the approved text. It made two searches with the same query, one filtered to `informe_ponencia` and the other to `aprobacion_definitiva`. It then quoted both versions in full, labelled each with its trámite, and listed four real differences: the Basque Juntas Generales added to apartado 1, the substitutes rule reworded, a new apartado 3 that lets the autonomous communities use their own systems, and the renumbering of the apartados on the Senado and the Junta Electoral. I checked it against `index/chunks.jsonl`, and both quotations are literal, both labels resolve, all four differences are real, and it adds no name, figure or judgement that is not in the retrieved text. What impressed me most is that, without being asked, it also said what it had not checked (whether the changes to artículos 187 and 206 were already in the *ponencia*) and which search would settle it.

This transcript is more interesting when you compare it with the evaluation, because it is the same kind of question the main agent wrongly refused twice. In q22 the agent made one search with no filter, and in q23 it searched twice, but both times only in the *proyecto*. The subagent searched once per stage, because its instructions tell it to, and AGENTS.md, which the main agent uses, has no such rule. One transcript cannot prove that this is the cause. But it fits the retrieval finding that one stage is usually found and the second one is not, and the fix would cost a single line in AGENTS.md, which re-running q21–q24 would test.

Two things about the transcript are worth knowing. It was captured on the five-document index, but the amendments did not get in the way, because both searches were filtered by trámite, which excludes them. It also comes from a later session than the evaluation. In the session that produced the evaluation, Claude Code connected to the server before `index/` existed, the handshake timed out against an empty index, and since Claude Code does not retry a failed MCP server mid-session, the subagent could not start. The server itself was fine. So, for anyone running this from a clean clone: build the index before opening the editor.

**Pregunta**

> ¿Qué cambió en el artículo cuarenta y cuatro bis de la LOREG entre el Informe de la Ponencia
> y el texto aprobado definitivamente?

**Llamadas a la herramienta (2)**

| # | `query` | `tramite` | `k` | resultados |
|---|---|---|---:|---:|
| 1 | `artículo 44 bis LOREG candidaturas composición equilibrada proporción mujeres hombres` | `informe_ponencia` | 6 | 6 |
| 2 | `artículo 44 bis LOREG candidaturas composición equilibrada proporción mujeres hombres` | `aprobacion_definitiva` | 6 | 6 |

**Respuesta del subagente**

> Entre el Informe de la Ponencia y el texto aprobado definitivamente, el artículo cuarenta y
> cuatro bis pasó de cuatro a cinco apartados: se añadieron las Juntas Generales de los
> Territorios Históricos vascos al ámbito del apartado 1, se reformuló la regla sobre suplentes,
> se incorporó un nuevo apartado 3 que permite a las comunidades autónomas y Juntas Generales
> establecer otros sistemas de elaboración de listas, y se renumeraron los apartados sobre el
> Senado y la Junta Electoral.
>
> En el **informe de ponencia** (25/06/2024) el precepto decía: «Artículo cuarenta y cuatro bis.
> 1\. Las candidaturas que se presenten para las elecciones de diputados y diputadas al Congreso,
> municipales, de miembros de los consejos insulares y de los cabildos insulares, diputados y
> diputadas al Parlamento Europeo y miembros de las Asambleas Legislativas de las Comunidades
> Autónomas deberán tener una composición paritaria de mujeres y hombres, integrándose las listas
> por personas de uno y otro sexo ordenados de forma alternativa. 2. A las listas de suplentes se
> aplicarán las reglas contenidas en el anterior apartado. 3. Cuando las candidaturas para el
> Senado se agrupen en listas, de acuerdo con lo dispuesto en el artículo 171, tales listas
> deberán tener igualmente una composición paritaria de mujeres y hombres, tal y como se establece
> en el apartado 1. 4. La Junta Electoral solo aceptará aquellas candidaturas que cumplan este
> precepto tanto para los candidatos como para los suplentes.»
> [BOCG-15-A-1-4 · Artículo primero · p. 13 · CVE:BOCG-15-A-1-4]
>
> En el texto de **aprobación definitiva** (31/07/2024) la redacción es: «Artículo cuarenta y
> cuatro bis. 1. Las candidaturas que se presenten para las elecciones de diputados y diputadas al
> Congreso, municipales, de miembros de los consejos insulares y de los cabildos insulares,
> diputados y diputadas al Parlamento Europeo y miembros de las Asambleas Legislativas de las
> comunidades autónomas y Juntas Generales de los Territorios Históricos vascos deberán tener una
> composición paritaria de mujeres y hombres, integrándose las listas por personas de uno y otro
> sexo ordenados de forma alternativa. 2. La regla anterior se aplicará en el conjunto de las
> listas, sin separar titulares y suplentes. 3. En las elecciones de miembros de las Asambleas
> Legislativas de las comunidades autónomas y Juntas Generales de los Territorios Históricos
> vascos, las leyes reguladoras de sus respectivos regímenes electorales podrán establecer otros
> sistemas de elaboración de listas siempre que su objetivo sea favorecer la representación
> paritaria y la presencia equilibrada de mujeres y hombres en dichas candidaturas. 4. Cuando las
> candidaturas para el Senado se agrupen en listas, de acuerdo con lo dispuesto en el artículo
> 171, tales listas deberán tener igualmente una composición paritaria de mujeres y hombres, tal y
> como se establece en el apartado 1. 5. La Junta Electoral solo aceptará aquellas candidaturas
> que cumplan este precepto tanto para las personas candidatas como para las suplentes.»
> [BOCG-15-A-1-8 · Artículo primero (1/2) · p. 12 · CVE:BOCG-15-A-1-8]
>
> Nota adicional de encuadre: en la aprobación definitiva el Artículo primero aparece además
> dividido en apartados «Uno», «Dos» y «Tres», incluyendo modificaciones del artículo 187.2 y del
> artículo doscientos seis de la LOREG. No he verificado en esta consulta si esas dos
> modificaciones adicionales ya figuraban en el informe de ponencia; haría falta una búsqueda
> específica sobre los artículos 187 y 206 en el trámite `informe_ponencia`.
---

## Adding a document

### What happens if the document is already indexed

The brief asks what should happen if the document is already in the index, and my answer depends on the document's identity and its content, never on its file name. Identity comes from the CVE stamp printed on every page, so the trámite and the genre are read from the PDF itself rather than guessed from what the file happens to be called. Content is the SHA-256 of the extracted, cleaned text.

Table 7: What `add_document` does with a document it has seen before.

| Case | What happens |
|---|---|
| same document, identical content | nothing is embedded, no quota is spent, and the tool says so |
| same document, different content | indexed as a revised edition; the previous chunks are marked `superseded` and excluded from search, but not deleted |
| new document | indexed; the tool reports the document, its chunk count and the embeddings spent |

The middle case is the one I thought about most. The obvious option would be to delete the old version, but comparing versions is the whole point of this corpus, so throwing away a superseded edition would destroy exactly what the tool exists to check. That is why old chunks are marked rather than deleted.

### The demonstration

The demonstration, saved in `eval/before_after.md`, adds the held-back amendments (`BOCG-15-A-1-2`, 209 chunks) and asks q27: *¿Qué texto proponía la enmienda número 24 del Grupo Parlamentario Vasco (EAJ-PNV)?* Before the document was added, the agent answered with no tool calls, in 2.1 s:

```
NO CONSTA EN EL CORPUS
Buscaba el texto de la enmienda número 24 del Grupo Parlamentario Vasco (EAJ-PNV). El corpus
únicamente contiene el proyecto del Gobierno, el informe de la ponencia, la aprobación
definitiva y el debate en Pleno, pero no incluye las enmiendas presentadas por los grupos.
```

After the document was added, it answered with one tool call, in 22.5 s:

```
La enmienda número 24 del Grupo Parlamentario Vasco (EAJ-PNV) proponía la supresión del
artículo undécimo del proyecto de ley relativo a la modificación de la Ley 2/1974, sobre
Colegios Profesionales [BOCG-15-A-1-2 · ENMIENDA NÚM. 24 (1/3) · p. 29-30 · CVE:BOCG-15-A-1-2].
```

It then quoted the amendment and its *justificación* verbatim, where the Grupo Vasco argued that «el Estado carece de competencia para la regulación de los órganos de gobierno de los colegios profesionales».

At first sight this looks like a clean success, and the "after" answer really is one: once the document is indexed, the same question gets a precise, quoted and correctly cited answer on the first search. But when I looked more closely, the "before" refusal is weaker evidence than it seems, because the agent did not search at all. It was right only because AGENTS.md and the tool description say the amendments are not in the corpus, not because it looked. That is the same zero-search pattern that caused the wrong refusal in q07.

### The description goes out of date

This led me to a problem I had not anticipated. Adding a document changes the index, but not the agent's description of it. After the demonstration, AGENTS.md and the `search` description still list four documents and still say the amendments are out of scope. The agent answered q27 anyway, because search returned the amendment and rule 1 tells it to answer from what search returns. But now its instructions contradict its own index, and with a different question it could just as easily trust the description and refuse something the index can answer. I decided not to edit AGENTS.md, because the whole evaluation ran under it and changing it now would make the results impossible to reproduce. A production version, though, should rebuild the corpus description from the manifest every time a document is added.

### The approval had to be given twice

The first run of the demonstration also taught me something about the approval guardrail. The answer before and after was the same refusal, because the document was never actually added. `demo()` passes `approve=True`, which opens the harness's approval gate, and yet the model made no tool calls and replied «necesito tu aprobación explícita». The reason is rule 8, which tells it never to call `add_document` without approval in the conversation itself. It only went ahead once the prompt also stated the approval. So the approval guardrail is really two separate locks, one in the code and one in the model, and in this run the model's lock held even after the code's lock had been opened.

---

## Harness and guardrails

### The system prompt

`agent.py` loads AGENTS.md from the file at every run and uses it as the system prompt. It has eight rules, and each one comes with the reason behind it, because my assumption was that a model that knows why a rule exists will apply it better in the cases the rule does not spell out. Three of the rules come straight from the licence.

Table 8: AGENTS.md rules derived from the corpus licence.

| Rule | What it requires | Licence condition |
|---|---|---|
| 2 | cite every factual sentence, copying the reference exactly | (c) and (d): cite the source and its date |
| 3 | quote legal provisions verbatim | (a): do not alter the content |
| 7 | report, do not characterise | (b): do not distort its sense |

Of the rest, four carry most of the weight. Rule 1 says to answer only from what `search` returns, and rule 4 to always name the trámite and never present the *proyecto* as the law in force. Rule 5 asks for exactly `NO CONSTA EN EL CORPUS` when the text does not answer the question; I chose a fixed phrase on purpose so that code could count refusals instead of guessing at them. Rule 8 forbids calling `add_document` without explicit approval in the conversation.

### The agent

The agent is a LangChain `create_agent` running on `gemini-flash-lite-latest` at temperature 0, with both tools reached over MCP. The tool names and descriptions come from the server's live tool list, so the server's docstrings are the only description the model reads, and the harness only wraps the tools to put its own checks in front of them. While checking this, I noticed one gap: the wrapper does not pass `grupo` through, so the harness agent cannot filter the debate by parliamentary group, even though the server and the subagent can.

### Four guardrails

The four guardrails fire in a fixed order. The first is a scope guard. Before any retrieval, it refuses questions that ask for a prediction, a value judgement or a motive, since no quotation can answer those, and it does so without spending a single token. I tuned it for precision rather than recall, because a wrong refusal is itself a failure in this evaluation. It catches «¿qué harán?» or «¿fue una buena ley?», but lets through questions like *¿Cuándo entrará en vigor?* or *¿Se aplicará en las elecciones de 2027?*, which the record does answer. On a 13-question probe, it refused all 6 intended cases and none of the other 7.

The second is a limit of 6 tool calls per question. It is enforced inside the tool wrapper, so a seventh call returns a message telling the model to answer with what it already has, or with `NO CONSTA EN EL CORPUS`. The third is the approval required by the brief: `add_document` never runs without a typed yes in the terminal, and when there is no terminal it is denied by default, so it can never hang `check.py` or a CI run. The fourth, my additional guardrail, is a citation check. If an answer cites a document that was never retrieved for that question, it is replaced by a refusal, because a citation to evidence the agent never saw is fabrication. There is a `--no-citation-check` flag to measure its effect, but I did not run that comparison, and since the check never fired, it would not have shown any difference.

That leads to an honest point about the guardrails: none of the four fired during the 32-question evaluation. No question asked for a prediction or a judgement, no answer used more than four of its six calls, no document was added, and no answer cited a document it had not retrieved. That does not show that the guardrails work; it shows that the test set never reached them. The only one I actually saw act was the approval lock in the add-document demonstration.

### What the citation check cannot see

The more I looked at the citation check, the more limited it seemed. It asks whether the cited document was retrieved, but not whether the cited passage exists, or whether it supports the claim. Of the 41 citations in the run, 38 resolve to a real chunk and 3 do not. q15 merged two neighbouring chunks into one label, `El señor DE LOS SANTOS GONZÁLEZ (1/4 y 2/4) · pp. 13-14`, which matches no chunk. q25 dropped the split marker, citing `Disposición transitoria primera · p. 26` instead of `Disposición transitoria primera (1/2) · p. 26`. And q31, an unanswerable question answered with zero searches, cited `[Proyecto de Ley Orgánica 121/000001]`, which is the bill's procedural number and not a document at all. That last one is an invented citation, and the check misses it because it only recognises `BOCG-` and `DSCD-` identifiers.

q15 and q25 are not fabrications, since the documents are real and were retrieved, but they do break rule 2, which asks the model to copy the reference exactly. q31 exposes a real blind spot. And q26, which cites a real, resolvable chunk that happens to be about a different law, shows the deeper limit. In the end, the check only guarantees that the cited document was seen, not that the passage exists or that it supports what the answer says.

---

## Evaluation

I ran the agent on all 32 questions and graded the answers in three layers. Code checks everything that can be checked mechanically, an LLM judge grades what needs to be read, and I graded all 32 answers by hand to see how far the judge can be trusted.

### What code checked

Code checks that every citation parses and resolves to a real chunk, that the cited document was retrieved for that question, and whether the answer is a refusal. For an `unanswerable` question, a refusal is simply correct.

Table 9: Code checks (no judge involved).

| Check | Result |
|---|---|
| citations emitted | 41 across 32 answers |
| citations that resolve to a real chunk | **38 / 41 (92.7%)** |
| citations naming a real document that was never retrieved | **0** |
| answerable questions whose expected document was retrieved | **25 / 26** |
| refusals detected by the fixed phrase | **8** |
| unanswerable questions refused | 5 of 6 by the fixed phrase, 6 of 6 in substance |
| answerable questions wrongly refused | **3 of 26** (q07, q22, q23) |
| refusals that did not open with the fixed phrase | **1** (q07) |

Even the refusal count needed a second look. The original detector checked whether the answer started with `NO CONSTA EN EL CORPUS`. q07 put a paragraph of explanation first, so it was logged as a normal answer, which made both the refusals and the wrong refusals one lower than they really were. This was the sixth bug, and it surfaced while I was preparing the manual grading. The fix recomputes refusals from the stored answers, looking for the phrase anywhere in the text, which costs no API calls. I also kept a separate `refusal_leads` column, so that it stays visible that q07 broke rule 5's requirement that the phrase come first.

Even then, one refusal still escapes. q31 declined correctly («El corpus no cubre los parlamentos autonómicos») without using the phrase at all, so 1 of the 9 real refusals is invisible to the detector. The lesson I take from this is that a metric that depends on the model following a wording rule can only be as reliable as the model's obedience to that rule. The fabricated-citation count has the same kind of blind spot. Its 0 is true as stated, but it does not count q31's invented reference, because that reference contains no `BOCG-` or `DSCD-` identifier. So that 0 means there were no citations to real but unretrieved documents, not that there were no fabricated citations.

### The judge

The judge sees the question, its `kind`, the reference answer, the full retrieved text and the agent's answer, and scores three binary dimensions, returning 0 whenever it is unsure. An answer is `correct` if it matches the reference or properly refuses an unanswerable question. It is `supported` if every claim appears in the retrieved text, even if it is true in the outside world. And it is `stage_correct` if it does not present a draft provision as enacted law. By default, the judge runs on the same model as the agent, `gemini-flash-lite-latest`. Getting a judge I could trust took three runs.

Table 10: Judge scores across three runs.

| Run | Evidence shown | Rubric | correct | supported | stage |
|---|---|---|---:|---:|---:|
| 1 | 2,000 characters per tool call | original | 0.938 | 0.875 | 0.969 |
| 2 | full (about 3.8× more) | original | **1.000** | **1.000** | **1.000** |
| 3 | full | anchored to ground truth | 0.906 | 0.812 | 0.906 |

In run 1, the judge was working through a keyhole. It only saw roughly the first one or two of the five retrieved chunks, so it marked valid citations as unsupported. Run 2 fixed that and gave a perfect score on every dimension, and my reaction was that it was too good to be true. It was. It had scored `correct=1` on an answer whose entire text was `ERROR: ExceptionGroup: unhandled errors in a TaskGroup`, and on two refusals of questions that were marked as answerable. Run 3 changed only the rubric. It now states that refusing a `single` or `multi` question is a failure, that an empty retrieval means the agent did not search, that an `ERROR:` answer is a system failure, and that names and numbers must be checked literally, using the example of a first name that is not in the text. With that, its zeros finally matched what the code checks had found. What strikes me is that the judge, on a weak model, did not reason its way to the ground truth it already had in front of it; it had to be told. If I had stopped at run 2, this report would claim a flawless system.

But anchoring the rubric came at a cost, which I only saw afterwards. Run 3 is more accurate, but it is also less independent. Its three `correct` zeros are the three wrong refusals, which the rubric itself defines as failures and which code had already counted. Its `supported` instructions name the first-name failure, which I added after finding it. And its three `stage_correct` zeros are the same three refusals, so it never flagged an actual stage confusion, although there was none to flag. In other words, on the failures I already knew about, the judge mostly confirms what it was told to look for.

### My own grades against the judge

I graded all 32 answers from `eval/grading_worksheet.md`, which leaves out the judge's verdicts. I had the question, the reference, the answer, the citations and the size of the evidence in front of me, and whenever something looked doubtful I went back to `index/chunks.jsonl` and checked the wording against the source.

Table 11: Agreement between my grades and the judge.

| Dimension | n | Raw agreement | Cohen's κ | Judge | Mine |
|---|---:|---:|---:|---:|---:|
| `correct` | 32 | **1.000** | **1.000** | 0.906 (29/32) | 0.906 (29/32) |
| `supported` | 32 | **0.969** | **0.904** | 0.812 (26/32) | 0.781 (25/32) |

These numbers look very good, but I think they should be read as an upper bound. My grading was not blind: I already knew about the invented first names and the wrong refusals from the earlier analysis, and I marked them accordingly, although I did not open `eval/judge.csv` until my own labels were written. The judge was not blind either, since its rubric encodes the same findings. So the κ really means that an informed reader and an informed judge end up in the same place, and on `correct` the perfect score is largely built in by the rubric.

The judge and I disagree on exactly one score, but the case where we agree turned out to be more interesting. On q31, the judge scored `supported=1` and I scored 0, because the agent attached `[Proyecto de Ley Orgánica 121/000001]`, which is not a document, to an answer it gave with zero searches. On q26, we both scored `supported=0`, but for different reasons. The judge failed it only for the invented first name «Blanca», which its rubric had told it to look for. It completely missed the bigger problem, that the list rule was cited to a *preámbulo* passage about two other laws (see *Failures*). The claim itself is true, so `correct=1` is right for both of us. I should add that I first graded it `correct=0`, because I misread the article as requiring something other than alternation, and only corrected my label after re-reading *Artículo primero*.

So what is the judge worth? I would say it is useful for failures that look like failures, partly because it was told what they look like. Where it falls short is the reason, not the score. On the two cases its rubric did not anticipate, it missed an invented reference, and it failed q26 for a reason that would not have caught the same mistake without the first name. A matching score does not mean the judge saw the same problem, and that is why I think a human still needs to read the answers whose citations look the most convincing.

---

## Failures

I classified every failure into the five categories in the brief (`retrieval_miss`, `wrong_from_right_passage`, `unsupported_claim`, `wrong_refusal` and `bad_question`) and ranked them by what they would cost the journalist. My calls agree with the causes `evaluate.py` proposes in `eval/failures.csv`, with two additions: q31, which the judge passed and the file therefore leaves out, and the secondary causes I noted for q07 and q22. None of the failures was a stage confusion.

Table 12: Every failure, by cost to the journalist.

| Question | Kind | Final cause | What happened | Cost to the journalist |
|---|---|---|---|---|
| q26 | multi | `unsupported_claim` | stated this law's list rule citing a *preámbulo* passage about two other laws; also invented a first name | highest: a resolvable citation that does not support the claim |
| q15 | single | `unsupported_claim` | added the first name «Arsenio», which is not in the corpus | high: a wrong detail ready for a caption |
| q16 | single | `unsupported_claim` | added the first name «Ana», which is not in the retrieved text | high: same mechanism, right by luck |
| q31 | unanswerable | `unsupported_claim` | refused correctly in substance, but attached an invented citation | medium: a reference that cannot be checked |
| q22 | multi | `wrong_refusal` (retrieval cause) | its exact-phrase search missed the approved *Artículo primero* | low: ten minutes with the PDF |
| q23 | multi | `wrong_refusal` | searched only the *proyecto* and refused instead of reporting an absence | low |
| q07 | single | `wrong_refusal` (partly `bad_question`) | refused without searching, because the question names the Senado | low |

### Unsupported claims

At first the three invented first names looked like three separate failures, but they are really one. In each case, the record names a deputy only by surname, and the model adds a first name that is not in the retrieved text: «Arsenio de los Santos González» (q15), «Ana Redondo García» (q16) and «Blanca Aguirre Gil de Biedma» (q26). Every question that required naming a person produced one, so the rate is 3 out of 3. My best explanation is that the model is filling in a half-remembered public figure from its training data. q16 shows why it does not matter whether the guess happens to be right. «Ana» is correct, and it even appears elsewhere in the corpus, just not in what the agent retrieved, and nothing in the output tells it apart from «Arsenio». So it is not that the system gets names right two times out of three; it is that none of the three can be verified from what it retrieved.

The answer that worries me most, though, is q26, because it passes every automated check except the one for the first name. q26 asked what the approved text says about how candidate lists are composed. The agent answered that it «establece el modelo de "listas cremallera"... de modo que los de un sexo ocupen los puestos pares y los del otro los impares», citing `BOCG-15-A-1-8 · preámbulo (8/21) · p. 5`. The citation resolves, the document and trámite are right, and the wording follows the source closely. This is the source:

> «...deben citarse las leyes electorales de la Comunidad Autónoma de **Castilla-La Mancha** y de
> la Comunidad Autónoma de **Andalucía**, que consagraron el modelo de las llamadas "listas
> cremallera", en las que... las candidaturas que presenten los partidos políticos, federaciones,
> coaliciones o agrupaciones de electores, alternan mujeres y hombres, ocupando los de un sexo los
> puestos pares y los del otro...»
> [BOCG-15-A-1-8 · preámbulo (8/21) · p. 5 · CVE:BOCG-15-A-1-8]

Reading it carefully, the passage describes two regional laws, as background. This law's own rule is in *Artículo primero*, the new artículo 44 bis, which the same agent quoted correctly in three other answers (q08, q09 and q24): candidate lists «de composición paritaria», with people of each sex «ordenados de forma alternativa». (The 60/40 rule only applies to municipalities of 3,000 to 5,000 residents and to the lists for provincial deputies.) Alternation and the odd/even zipper list are the same rule, so the claim is true, but only by luck. What the agent really did was present a description of another law as if it were this one, and wherever the two laws differ, the same move would produce a false claim behind a citation that looks valid. The citation was real, the label resolved, the document and trámite were right, so every check passed. Without «Blanca», nothing would have flagged it, and the only way to catch it is to read page 5.

Rule 4 does not cover this case. Rule 4 protects against confusing stages of this text, whereas q26 confuses this law with other laws described inside it. Both errors have the same shape, though: the right document, but the wrong text. So instead of keeping `stage_confusion`, which had zero instances, and adding a seventh category next to it, I would merge them into one, `wrong_source_text`, with q26 as its only instance. The fix would be a rule of its own: when a passage describes a law other than the one being asked about, the agent should say whose law it is, or not use it.

### Citation defects

Table 13: The three citations that do not resolve.

| Question | Emitted | Real label |
|---|---|---|
| q15 | `DE LOS SANTOS GONZÁLEZ (1/4 y 2/4) · pp. 13-14` | `(1/4) · p. 13-14` and `(2/4) · p. 14` |
| q25 | `Disposición transitoria primera · p. 26` | `Disposición transitoria primera (1/2) · p. 26` |
| q31 | `[Proyecto de Ley Orgánica 121/000001]` | none: the bill's procedural number, not a document |

q15 merges two real labels, and q25 drops the suffix. In both cases, the quoted text is real and verbatim; the reader just cannot paste the reference back and land on it. Here I think the fault is mine rather than the model's. `(1/2)` is an artefact of my chunking, it does not appear anywhere in the PDF, and moving the part number out of `location_label` into separate metadata would fix both. q31 is a different kind of problem: an invented reference attached to a refusal made without searching.

### Wrong refusals

The three wrong refusals are all cheap for the journalist, but each one happened for a different reason. What they have in common is that the agent made up its mind before it had looked everywhere the answer could be.

q07 was refused on wording alone, without any search. The question, *¿Qué ocurre si el Senado rechaza los objetivos de estabilidad presupuestaria?*, is answered by the approved text's *Disposición transitoria tercera*. But it names the Senado, which AGENTS.md and the tool description both list as out of scope, so the agent refused with zero tool calls. The scope guard did not fire, so this is not a problem with the guard's keyword list; it is rule 6 being applied too broadly. The bill really is broader than its title, since *Disposición final cuarta* amends the Ley Orgánica 2/2012 de Estabilidad Presupuestaria. And part of the fault is mine: a fairer question would not have named the chamber.

q22 was a retrieval miss, but under the agent's own query. It searched for the literal phrase «sin separar titulares y suplentes», and dense retrieval returned five chunks, none of which was the approved *Artículo primero* that contains it. What I find interesting is that this is the opposite of q01. There, rewriting the question into a short query fixed retrieval; here, it broke it, because the user's full question does retrieve both passages in the top 5. Exact-phrase matching is precisely what design D would add. The agent also claimed to have searched «en todos los documentos del expediente» after making a single call, which tells me its account of its own process cannot be trusted.

q23 searched only one stage and refused to report an absence. Asked whether the Government's bill included the Basque Juntas Generales, the agent searched twice, both times only in the *proyecto*, correctly found nothing, and then refused. But that absence was the answer, and the approved text, which it never searched, adds them. As I noted in *Tools and subagent*, the subagent's rule of one search per stage is the piece that is missing here.

### No stage confusion

Across the eight stage-sensitive questions (q09–q12 on the *proyecto*, and q21–q24 comparing stages), the agent never presented a draft provision as if it were enacted law. The judge's three `stage_correct` zeros are the three wrong refusals, and that was the judge's own choice, since the rubric only forces zeros for `ERROR:` answers. On this evidence, rule 4 and the trámite in every citation did what they were designed to do. That said, eight chances is not many, and the related error in q26 still got through.

### Weaknesses in the test set

Three of my questions are weaker than I intended. q07 is partly a bad question, for the reasons above. q13 expects a label that covers 78 chunks, so almost any chunk from the debate counts as a hit, which slightly inflates the hit rate. And q24 is labelled `multi`, but it only really asks about the proyecto.

---

## Decision

So, would I let a journalist rely on this system? For one task yes, and for three no. I would let them use it to find out what a given version of this text says, at which stage and in what words, which is what I built it for. I would not let them rely on it for a person's name, for a claim that something is absent from the record, or for what the law requires, unless they open the article it cites.

The reason it splits like this goes back to the asymmetry in the use case. A wrong published claim means a correction or a false claim about a party, while "NO CONSTA" costs ten minutes. Looking at Table 12, the expensive failures are concentrated in two places, naming people and passages about other laws. Outside those two, every answer to an answerable question was either supported or a refusal, and refusals are the cheap kind of failure.

### What it does well

By my grades, 29 of the 32 answers are correct and 25 of 32 are fully supported (the judge says 29 and 26). The expected document was retrieved for 25 of the 26 answerable questions, 38 of the 41 citations resolve to a real chunk, and none cites a document that was not retrieved. The agent quotes verbatim, names the trámite, and across the eight stage-sensitive questions it never presented a draft as enacted law. And since every citation carries the CVE of the signed original, a journalist can check any quotation in about a minute.

### Where it cannot be relied on

The first limit is names, and here I would not even say "use with care"; I would say not at all. The failure rate is 3 out of 3, every invented name is plausible and wrapped in a correct citation, and one of them («Ana») happens to be right in a way that nothing in the output distinguishes from the wrong ones. Until the rule I propose in *Failures* is added and measured again, every name has to be read off the PDF.

The second limit is absence. Three of the 26 answerable questions were wrongly refused, two of them stage comparisons, and on very little evidence: q07 without searching, q22 after one search while claiming to have searched everything, and q23 after searching only one of the two stages. On top of that, a refusal is not always recognisable as one (q31). So when this system says "the corpus says nothing about X", that might only mean that one search did not find it, or that no search was run at all, and it should never be published as a finding.

The third limit is what the law requires, if the article itself is not opened, and this was the one I did not expect. q26 gave a fluent, correctly staged and resolvably cited answer whose evidence came from two other laws, and every guardrail let it through. A *preámbulo* exists precisely to cite other laws, so retrieval over legislation will keep returning passages about some other statute, and nothing in the text marks the difference. For any question of the form "what does this law require?", the answer has to come from the articles themselves, and the agent does not have that rule yet.

### Cost

Per question, the median is 6.7 s and 6,628 tokens; the mean is 24.8 s and 10,145 tokens, and the 90th percentile is 66.5 s. For 100 questions, that comes to about 1.01 million tokens and 41 minutes, for the agent only, not counting the judge. Tokens grow with the number of searches (q15, with four, used 26,645), but time does not: two of the three slowest answers, q21 at 116 s and q04 at 108 s, made only one search each, which most likely reflects latency on the free tier. At this scale, cost is not what decides whether to use the system; the pattern of failures is.

### Caveats

There are three caveats I would keep in mind when reading these numbers. First, the test set is small. With 26 answerable questions, each one moves a rate by about 4 points, so the figures show the shape of the failures more reliably than their exact rates. Second, the model was the weakest available. Every answer came from `gemini-flash-lite-latest`, the only model the free tier would serve (`gemini-2.5-flash` returned 404 for new keys, and the full `gemini-3.x` flash models returned 503), so these results are a floor for the architecture rather than a ceiling. Third, the judge is the weakest instrument in the whole evaluation. It runs on the same model as the agent, it only agreed with the code checks once its rubric was anchored, and it missed the two cases its rubric did not anticipate (q31, and the real reason q26 fails). I trust the code checks considerably more.

If I had to keep one finding from all of this for a future version, it would be that last one: the judge's score is least trustworthy exactly where the citation looks most convincing. That is also why my answer to whether a journalist can rely on this system is yes for quotation by stage, and no for names, absences and what the law requires.

---

## AI use

Claude Code (Claude Opus 5.5) was used. Specifically:

**Written by Claude:** the code in `index.py`, `server.py`, `agent.py`, `evaluate.py` and the rules in `AGENTS.md`.

**Six bugs were found by Claude during the evaluation run**, each of which would have falsified a
number in this report: the silent embedding-batch truncation, the unscoreable `fixed_200` hit
rate, the citation resolver that ignored the CVE suffix, the 2,000-character evidence cap that
starved the judge, the demo that never added its document, and the refusal detector that only
counted the fixed phrase when it opened the answer. They are described in the sections above
because the fact that five of the six were *measurement* bugs rather than system bugs is the main
thing this exercise taught me: a RAG evaluation can report confident numbers that mean nothing at
all. The last of them surfaced during the manual grading pass.
