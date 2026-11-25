# Assignment 3 Report — Shipwreck-law assistant

- **Name:** Matias Viguera Barrientos
- **Student ID:** 18542
- **Group:** BBADBA 5A

## Use case

The idea for this project came from a question I could imagine asking myself as a PADI Advanced Open Water Diver. If I’m diving off the Spanish coast and I find old coins in a wreck, can I keep them, or do I have to report what I found? A small salvage company could have a similar question before spending time and money searching for a boat it might need permission to look for. What interested me about this use case is that someone could actually act on the answer. If the assistant says it doesn’t know, the diver can still check with the authorities, but if it confidently says they can take the coins, they might already have taken them by the time they find out it was wrong. The stakes are concrete. Under Ley 16/1985, a finder who doesn't report a find loses the reward of half its appraised value, and the objects go straight to the authorities (Art. 44.3–44.4). The finder can also be fined up to €60,101.21, and an excavation without a permit can cost up to €150,253.03 (Art. 76).

## Corpus

I used four legal texts from the *Boletín Oficial del Estado* (BOE), Spain’s official gazette. Together they cover different parts of the same problem. A question about an object found underwater can depend on what the object is, where it was found and what the person wants to do with it.

| Document | Source | Date | Parts included | Licence | Words |
|---|---|---|---|---|---:|
| UN Convention on the Law of the Sea (UNCLOS), Spanish ratification | [BOE-A-1997-3296](https://www.boe.es/diario_boe/txt.php?id=BOE-A-1997-3296) | BOE 14 Feb 1997 | Ratification instrument and Spain’s declarations, preamble, Parts I–VII, Article 149 and Part XVI, including Article 303 | Official text, no copyright; BOE reuse with attribution | 19,984 |
| UNESCO 2001 Convention on the Protection of the Underwater Cultural Heritage | [BOE-A-2009-3787](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2009-3787) | BOE 5 Mar 2009 | Full convention and all 36 rules in the annex | Official text, no copyright; BOE reuse with attribution | 8,122 |
| Ley 16/1985 del Patrimonio Histórico Español | [BOE-A-1985-12534](https://www.boe.es/buscar/act.php?id=BOE-A-1985-12534) | BOE 29 Jun 1985; consolidated text in force on 18 Nov 2026 | Full consolidated law | Official text, no copyright; BOE reuse with attribution | 15,609 |
| Ley 14/2014 de Navegación Marítima | [BOE-A-2014-7877](https://www.boe.es/buscar/act.php?id=BOE-A-2014-7877) | BOE 25 Jul 2014; consolidated text in force on 18 Nov 2026 | Preliminary title, Title I on navigation in Spanish waters and Title VI on maritime accidents, including salvage and sunken goods | Official text, no copyright; BOE reuse with attribution | 10,360 |
| **Total** | | | | | **54,075** |

The source texts are in Spanish, while the questions and answers are in English. I chose this setup because a diver visiting Spain might ask a question in English but still need to check the wording of the Spanish article. The corpus uses the consolidated wording as of 18 November 2026. The texts contain no personal data, and the index keeps each document's name and BOE link so the user can check the original.

## Ingestion

`index.py` downloads the four documents as XML into `corpus/`. It splits them into individual articles and treats each rule in the UNESCO annex as its own unit. Each unit keeps its location in the original document, including its title, chapter or section where available.

One issue was that the consolidated laws contained previous versions of the same article. Keeping all of them could give the assistant two different answers to the same question. The parser keeps the wording in force on the corpus date and removes editorial notes such as “Se modifica por…”. It also converts article numbers written in words into digits. For example, “Artículo cuarenta y cuatro” becomes “Artículo 44”, which makes the citations consistent across the four documents.

Another issue came up with the two treaties. The first extraction returned no usable articles because the XML contained smaller `<texto>` elements inside cross-references. The parser had selected one of those instead of the document body. Selecting the `<texto>` element with the most paragraphs fixed the extraction.

I compared two ways of splitting the documents into chunks:

- **`article`** keeps each article together and splits articles longer than 300 words at paragraph boundaries.
- **`fixed`** uses 150-word windows with 30 words of overlap. A window can contain the end of one article and the beginning of another.

Each chunk stores its source, article, location, link, document hash, position, word count and chunking design. Fixed windows also record every article they overlap. The original corpus produced 459 article-based chunks and 452 fixed-window chunks.

The chunks are embedded with `gemini-embedding-2` using 768 dimensions and stored in ChromaDB under `index/`. The pipeline saves each batch as it finishes and checks which chunks already have vectors. This mattered with the free-tier quota because an interrupted run could continue from where it stopped.

## Test set

The test set in `eval/questions.csv` contains 32 questions. There are 21 single-passage questions, six that need two passages and five that the original corpus cannot answer. Each answerable question has a reference answer and the source and article expected to support it.

I had a couple possible questions, but I also asked ChatGPT to help me with topics that could be things a diver can think. I wanted them to sound like something a diver or a salvage company would actually ask. For example, q09 says the company wants to use sonar and has no plans to lift the boat. That detail matters because it tests whether the assistant understands that searching for something and recovering it are two separate decisions.

| ID | Type | Question | Expected evidence and answer |
|---|---|---|---|
| q09 | Single | We want to use sonar to find a fishing boat that sank last winter in Spain’s territorial sea. We don’t own it and won’t lift anything. Who can approve the search, and can we get exclusive search rights? | Ley 14/2014, Article 376. The Spanish Navy can authorise the search. Since the company does not own the boat, any permission it receives is non-exclusive. |
| q25 | Multi | We’re planning to study a historic wreck in a country’s contiguous zone. How far from the baseline can that zone reach, and can a country that has joined the international heritage agreement require approval for our work there? | UNCLOS, Article 33, and UNESCO 2001, Article 8. The zone can extend up to 24 nautical miles. The country can regulate and authorise the work, and if it does, it must require the annex rules to be followed. |

For the unanswerable questions, I kept the topic close to the rest of the corpus. Asking about a US court ruling on a shipwreck, for example, gives the assistant plenty of related material to retrieve. The test is whether it recognises that none of the four original texts tells it what that court decided.

## Retrieval

I compared both designs on the 27 answerable questions, using each question as written. A hit means that at least one expected article appeared in the first `k` results. For the six multi-passage questions, I also measured whether **both** expected passages appeared in the top five.

| Design | Hit@1 | Hit@3 | Hit@5 | Both passages in top 5 on multi questions | Average words in top 5 |
|---|---:|---:|---:|---:|---:|
| `article` | 0.74 | 0.96 | 1.00 | 5/6 | 835 |
| `fixed` | 0.63 | 0.78 | 0.85 | 5/6 | 745 |

I went with one chunk per article and `k = 5`. With that setup, at least one expected article appeared in the first five results for all 27 questions, compared to 23 out of 27 with fixed windows. Both designs found both passages in five of the six multi-passage questions, so for me the extra 90 words per search were worth it for the improvement across the full test set.

## Tools and subagent

`server.py` exposes two MCP tools. The descriptions tell the agent what each tool does, when to use it and what it will get back.
 
**`search(query)`**
 
> Search four legal texts, in Spanish, on shipwrecks and objects found underwater: Spain's Historical Heritage Law (Ley 16/1985: archaeological finds, permits, fines), Spain's Maritime Navigation Law (Ley 14/2014: salvage, sunken ships and goods, extraction), the UNESCO 2001 Convention on the Protection of the Underwater Cultural Heritage, and the UN Convention on the Law of the Sea (UNCLOS: sea zones, archaeological objects at sea).
>
> Use it for any question about who owns a wreck or a find, reporting duties, permits, salvage rewards, fines or sea zones. The query can be in English, Spanish legal terms (e.g. "hallazgo casual", "buque naufragado") often match better.
>
> Returns the 5 most similar passages, best first. Each has a "Cite as" label (document and article) to cite it by, its location, a link to the official text, and the passage itself in Spanish.
 
**`add_document(path)`**
 
> Add a document to the searchable index: a BOE XML, PDF, HTML, Markdown or text file at `path` on this computer. It is split into articles, pages or sections, embedded and stored, so later searches can find it.
>
> Use it only when the user asks to add a specific file. If the same content is already indexed, nothing is embedded again. If a document with the same name but different content is indexed, its old passages are replaced by the new ones.
>
> Returns what was added: the document's name, how many sections and words it has, and the label to cite its passages by.
 
`add_document` imports `index_file` from `index.py`, so a new file goes through the same parsing, chunking and embedding as the original corpus. The server loads `index/` at startup and never re-embeds the corpus.
 
For example, when searching “Can I keep old coins I find in a shipwreck off the Spanish coast?”, the first of the five results was:
 
```text
Result 1 (similarity 0.74)
Cite as: [Ley 16/1985, Artículo 44]
Location: Ley 16/1985, de 25 de junio, del Patrimonio Histórico Español › Título V. Del Patrimonio Arqueológico › Artículo 44
Link: https://www.boe.es/buscar/act.php?id=BOE-A-1985-12534#acuarentaycuatro
Artículo cuarenta y cuatro
1. Son bienes de dominio público todos los objetos y restos materiales que posean los valores que son propios del Patrimonio Histórico Español y sean descubiertos como consecuencia de excavaciones, remociones de tierra u obras de cualquier índole o por azar. El descubridor deberá comunicar a la Administración competente su descubrimiento en el plazo máximo de treinta días e inmediatamente cuando se trate de hallazgos casuales. […]
```
 
The Claude Code subagent is defined in `.claude/agents/corpus-researcher.md`. It has access only to `search`. Its instructions:
 
1. Search with the user's question. If the results don't contain the answer, search again using Spanish legal terms, for example «hallazgo casual», «buque naufragado» or «extracción». Use at most three searches.
2. Answer in English in two to four sentences, using only what the search results say. Cite every claim with the "Cite as" label of the result it comes from, written exactly as given, for example [Ley 14/2014, Artículo 374].
3. If the results don't answer the question, reply "The documents don't cover this." and nothing else. If they answer only part of it, answer that part with citations and say which part the documents don't cover.
4. Never answer from your own knowledge, and never cite an article that wasn't in your search results.
Here is the transcript from the Claude Code session in VS Code:
 
```text
User: Use the corpus-researcher subagent to answer: Can I keep old coins I find in a shipwreck off the Spanish coast?
 
Agent: Keeping shipwreck coins question  (delegated to corpus-researcher)
  IN: A recreational diver asks: "Can I keep old coins I find in a shipwreck off the Spanish coast?"
      Search the corpus (use Spanish terms too, e.g. «hallazgo casual», «dominio público», «objetos arqueológicos»,
      «buque naufragado», «patrimonio cultural subacuático», «extracción», «premio») and cover: who owns such finds,
      whether the finder can keep them, any duty to report/hand over, any finder's reward, and any relevant UNESCO 2001
      rules on commercial exploitation. Return a short answer where every claim carries its exact "Cite as" label [...]
  Finished
 
Subagent report:
  Short answer: no. Under Spanish law the diver can't keep the coins, but reporting the find properly can earn a cash reward.
  - Who owns them: Objects with historical-heritage value found by chance belong to the public domain [...] and the Civil
    Code treasure rule (art. 351) does not apply to them [Ley 16/1985, Artículo 44]. A chance find («hallazgo casual») is
    any discovery of such objects made by chance [Ley 16/1985, Artículo 41]. Sunken Spanish state vessels and their cargo
    are state public-domain property [...] [Ley 14/2014, Artículo 382].
  - Reporting and handing over: For a chance find, the finder must tell the competent authority «inmediatamente»
    (immediately) [...] [Ley 16/1985, Artículo 44].
  - Permits: Lifting sunken ships or goods in Spanish internal waters or the territorial sea needs prior authorisation from
    the Navy [Ley 14/2014, Artículo 377]. Searching for them also needs Navy authorisation [Ley 14/2014, Artículo 376]. [...]
  - Finder's reward: The finder and the owner of the place where the object was found are entitled to a cash reward of half
    the legally appraised value, split equally between them [Ley 16/1985, Artículo 44]. [...]
  - UNESCO 2001: Underwater cultural heritage shall not be commercially exploited [UNESCO 2001, Artículo 2]. It must not be
    traded, sold, bought or bartered as commercial goods [UNESCO 2001, Norma 2]. [...]
  Key quote: «Son bienes de dominio público todos los objetos y restos materiales que posean los valores que son propios
  del Patrimonio Histórico Español» [Ley 16/1985, Artículo 44].
  Gaps: The documents don't cover whether ordinary coins with no historical or archaeological value fall under these
  rules, or the amount of any fine.
 
Final answer (main agent): No, you can't keep them. Under Spanish law, old coins with historical value found in a wreck
belong to the state, but reporting them can earn you a cash reward. [same points and citations as the report]
```
 
One part of the response shows a limitation. The subagent said the documents did not cover the amount of a fine, even though Article 76 of Ley 16/1985 deals with fines. It hadn’t retrieved that article. What it could reasonably say was that the passages it found didn’t establish the fine. Saying that about the whole corpus went further than its search justified.

## Adding a document

If a document is already indexed: `add_document` fingerprints the document's text. Identical content is skipped and nothing is embedded again. A document with the same name but different content has its old passages replaced, so the index never holds two versions of the same document.

For this test I used q32, “What did the US court decide about ownership of the Atocha treasure found off Florida?” The original corpus covered shipwrecks but did not include the US court ruling.

Before adding the document, the assistant searched for “Atocha” and answered:

```text
The documents don't cover this.
```

I then added the 1978 Fifth Circuit opinion, *Treasure Salvors, Inc. v. Unidentified Wrecked and Abandoned Sailing Vessel*, saved in `added/atocha_5th_circuit_1978.html`. The file contains 7,882 words. [Source of the opinion](https://law.resource.org/pub/us/case/reporter/F2/569/569.F2d.330.76-2151.html)

```text
The assistant wants to run add_document with
{'path': 'added/atocha_5th_circuit_1978.html'}. Allow it? [y/N] Y

corpus_article: embedded 32/32 new chunks
corpus_fixed: embedded 66/66 new chunks
```

After adding the document, the assistant searched again and returned:

```text
The US courts confirmed Treasure Salvors, Inc. and Armada Research Corp.
in their sole title and right to immediate possession of the Nuestra Señora
de Atocha, rejecting claims by the United States government
[atocha_5th_circuit_1978, Inicio].
```

The full outputs are in `eval/demo_before.txt`, `eval/demo_add.txt` and `eval/demo_after.txt`. The evaluation results below are from the original four-document corpus, when q32 was still unanswerable.

## Harness and guardrails

`agent.py` uses LangChain’s `create_agent` with `gemini-3.5-flash-lite`. It connects to the MCP server and reads `AGENTS.md` as its system prompt. The rules in that file cover eight decisions:

1. Search before answering and try Spanish legal terms if the first results are insufficient.
2. Use the retrieved passages as the evidence for the answer.
3. Cite each claim using the exact `Cite as` label returned by the tool.
4. Say “The documents don’t cover this” when the search provides no answer.
5. If only part of a question can be answered, answer that part and identify the gap.
6. Answer briefly in English and include a short Spanish quote with its meaning.
7. Add a reminder to report a find before acting when the user is considering a real action.
8. Use `add_document` only when the user asks to add a specific file.

Adding a document changes what future users can retrieve, so the harness asks for approval before the tool runs. If there is no interactive terminal to give approval, the request is rejected. The harness also limits each question to eight model calls and four searches, and retries temporary Gemini errors with backoff.

The extra guardrail checks citations. After the model answers, the code compares the citations in its answer with the labels returned by its searches. If it cites an article it never retrieved, or gives a substantive answer without a citation, it gets one retry. If the retry also fails, the harness replaces the answer with a refusal.

The guardrail fired during the Atocha demo. After adding the file, the assistant confirmed the action without a citation. The guardrail rejected that confirmation, and on the retry the assistant returned a cited but off-topic answer about Article 373 of Ley 14/2014. The file had already been added successfully. I would change the check so a simple confirmation can go through without a citation. It didn’t fire on any of the 32 evaluation questions.

## Evaluation

`main.py evaluate` runs the evaluation and saves the outputs under `eval/`. The code checks refusals, whether cited articles were retrieved, and whether an expected article was retrieved and cited. The LLM judge then evaluates the answerable responses against the reference answer and the retrieved evidence.

Results of the code checks: all 32 answers cited only articles their searches had returned, the expected article was retrieved and cited in 25 of the 27 answerable questions (all but q20 and q21), and the citation check didn't have to block any answer.

The judge's rubric scores two things separately:

- Correct = 1 only if the response states every key fact of the reference answer and contradicts none. A missing or wrong key fact (a number, a deadline, an owner, a yes/no) makes it 0, and every part of a multi-part question must be right.
- Supported = 1 only if every factual claim is in the retrieved evidence, even if the claim is true. Faithful translations count, the closing disclaimer and "the documents don't cover" statements are not claims. The judge writes its reason before its verdict.
An answer can get one of these right and still fail the other. For example, it can give the correct deadline for the boat in the question but then claim that the same deadline applies to every shipwreck.

I initially used `gemini-3.5-flash` as the judge, but its daily quota ran out after a few answers. The full set was then evaluated using `gemini-3.5-flash-lite`, the same model as the agent. The separate grading sheet contains 27 assessments of the answerable questions, with scores for correctness and support and a written reason for each zero. I graded this assessments, later I would ask ChatGPT to evaluate if my gradings were correct and made sense.

| Result | Automated evaluation (judge + code) | Grading sheet |
|---|---:|---:|
| Correct answers to answerable questions | 24/27 (89%) | 21/27 (78%) |
| Fully supported answers to answerable questions | 26/27 (96%) | 20/27 (74%) |
| Correct refusals on unanswerable questions | 5/5 | — |
| Wrong refusals on answerable questions | 0/27 | 0/27 |

Across all 32 questions, the automated evaluation marked 29/32 correct and 31/32 supported, including the five refusals scored by code. On the 27 answerable questions, the judge and the grading sheet agreed on correctness 24/27 times (89%) and on support 21/27 times (78%).

All nine scoring disagreements went in the same direction. The judge gave credit where the grading sheet did not. Six disagreements were about support (q03, q04, q05, q14, q22 and q23), and three were about correctness (q20, q25 and q27). In this test, the judge was especially likely to accept an answer that got the main point right but missed a condition or made a claim broader than its citation justified.

## Failures

The grading sheet flagged 11 of the 27 answerable questions on correctness, support or both. I assigned one main cause to each question so that an answer failing both checks would only be counted once.

| ID | What went wrong | Main cause | Did the AI judge flag it? |
|---|---|---|---|
| q02 | It lists the paperwork but leaves out the destination and who sets the deadline, both of which appear in the reference answer. | Incomplete answer from the right passage | Yes |
| q03 | It says “all archaeological items” and misses the exception in Article 44.5. | Unsupported generalisation | No |
| q04 | It cites Article 45 for the answer but adds details about distance and conservation that come from Article 42.2. | Claim supported by a different article than the one cited | No |
| q05 | It gives the fine but leaves out the condition that the conduct is treated as an administrative offence if it is not a crime. | Unsupported generalisation | No |
| q14 | It retrieves UNESCO Rule 1 but changes the conditions under which lifting an object can be justified. | Wrong answer from the right passage | Correctness only |
| q20 | It answers from UNESCO Article 12 and misses UNCLOS Article 149, leaving out the country of origin as a separate basis for a claim. | Retrieval miss | No |
| q21 | It says ownership is not lost simply because an object sank, misses the expected UNCLOS article on identifiable owners and shifts to whether the find can be sold. | Retrieval miss | Yes |
| q22 | It retrieves Article 42 on permission but uses a definition from Article 41, which it did not retrieve. | Unsupported claim | No |
| q23 | It says “any shipwreck” even though the provision has an exception for state vessels. | Unsupported generalisation | No |
| q25 | It gives the distance and says approval can be required, but leaves out the requirement to follow the annex rules. | Incomplete answer from the right passages | No |
| q27 | It says Spain can decline to lead the consultations but leaves out who then chooses the coordinator. | Incomplete answer from the right passages | No |

What stood out to me was that finding the right article didn’t always lead to a complete answer. I counted five failures involving an unsupported or incorrectly cited claim, four wrong or incomplete answers from the right passages, and two retrieval misses. There were no wrong refusals, and I didn’t assign any failure primarily to a bad test question, although q02 is debatable because the user asks specifically about paperwork and the reference also expects a destination and deadline. For me, q25 is the clearest example of the issue with the answers: the assistant found both articles, gave the right distance and explained that approval could be required, but still left out a condition the reference considered important. The AI judge gave it full credit. The first change I’d test is asking the assistant to check each part of the question and look for conditions or exceptions in the passages before it gives its final answer.

The two retrieval misses suggest a separate change. When the retrieval evaluation used the original English question, the expected article ranked first for q20 and second for q21. In the actual conversations, the agent rewrote the searches in Spanish and missed those articles. I’d test searching with the user’s original wording first and using the Spanish query as a second search when needed.

## Decision

The agent used an average of 2.3 model calls and 5,364 tokens per question. The median response time was 4.7 seconds, compared with a mean of 16.5 seconds because some requests took much longer. The judge used about 2,750 additional tokens per answer it graded. The project ran within the free tier used for this assignment.

I would use this assistant as a starting point if I wanted to find the article that applies to my situation. It recognised all five questions that the original documents couldn’t answer, which is something I’d want if I were asking about a real find. What would stop me from relying on it for a final decision is that only 16 of the 27 answerable responses received full marks for both correctness and support on the grading sheet. If I were the diver, I’d want to see the exact passage next to the answer, with a link to the original, so I could check whether the summary had left out a condition. For a decision like lifting something from a wreck, I’d still confirm it with the relevant authority before acting.

## AI use

I used Claude to help select the legal corpus and build the assistant, including writing and optimizing the code for the indexing pipeline, the MCP server, and the overall system. I also used it to refine the subagent instructions and turn my design decisions such as handling partial answers, Spanish quotes, citations, and refusals into concrete rules the agent could follow.

I used ChatGPT to brainstorm realistic diver and salvage scenarios for the test set, review my manual grading sheet, and polish the writing in this report. It also helped cross-check my draft against the saved evaluation outputs, for example, that review caught an error in my initial description of q21, where the assistant actually did state that sinking alone does not remove ownership before missing the key article and shifting to commercial exploitation.