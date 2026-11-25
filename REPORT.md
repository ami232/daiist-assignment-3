# Assignment 3 Report

- **Name**: Emilia Granja
- **Student ID**: 18875
- **Group**: BBADBA 5B 

## Use case

*Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".*

The agent answers questions from the quality and regulatory team of a small food company in Spain that sells packaged food in the EU and does not have its own lawyer. Before new labels go to print, or when marketing wants to put a claim on the packaging like "source of fibre" or "vitamin C contributes to the normal function of the immune system", the team asks the agent what the label must, may or may not say. They use the response to review the draft label, and the reference to open the article and verify it themselves or forward it to an advisor.

A wrong answer costs much more than "I don't know". If the agent says an allergen does not need to be emphasised in the list of ingredients, or that a health claim is allowed when it is not, the company can print thousands of labels that break the law, which means relabelling or destroying the stock and possibly a recall with fines from the food safety authorities, and with allergens there is also a real health risk for consumers. "I don't know" only costs time, since the team has to read the regulation themselves or pay someone for an hour of work.

This is why the agent is built to refuse rather than guess, every answer has to cite a passage that search actually returned, and when the corpus does not cover the question the agent says so instead of answering from memory. Also, the citation-check guardrail in agent.py blocks any answer that cites a passage search did not return, or that cites nothing and is not a refusal, and only in that case the team sees a message telling them to check the regulation directly or ask a regulatory expert.

## Corpus

*Table: document, URL, date, licence, words.*

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| Regulation (EU) No 1169/2011, food information to consumers (REG_1169_2011) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32011R1169 | 25 Oct 2011 | EUR-Lex: reuse allowed with acknowledgement (Decision 2011/833/EU) | 22,521 |
| Regulation (EC) No 1924/2006, nutrition and health claims (REG_1924_2006) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32006R1924 | 20 Dec 2006 | same | 9,456 |
| Regulation (EU) No 432/2012, permitted health claims (REG_432_2012) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32012R0432 | 16 May 2012 | same | 15,190 |
| Commission Notice, Q&A on Regulation 1169/2011, 2018/C 196/01 (QA_NOTICE_2018) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52018XC0608(01) | 8 Jun 2018 | same | 5,491 |
| Commission Notice on allergen information, 2017/C 428/01 (ALLERGEN_NOTICE_2017) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52017XC1213(01) | 13 Dec 2017 | same | 2,326 |
| Commission Notice on QUID, 2017/C 393/05 (QUID_NOTICE_2017) | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52017XC1121(01) | 21 Nov 2017 | same | 4,315 |
| **Total** | | | | **59,299** |

Added later in the demo: Commission Implementing Regulation (EU) No 828/2014 (gluten-free statements), 30 Jul 2014, from the Publications Office (Cellar), 10 chunks.

The corpus is six documents from EUR-Lex with 59,299 words in total, the three EU regulations on food information and on nutrition and health claims, and three Commission notices that explain how to apply them. I added the official guidance and not only the law because the regulations say what is required, but the notices answer the practical questions a quality and regulatory team actually has, like how to emphasise allergens.

## Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

Every document goes through the same pipeline in index.py, which turns the EUR-Lex page into chunks with one vector each in ChromaDB.

1.  Extract: BeautifulSoup reads the EUR-Lex HTML and removes the scripts and the footnotes with their markers, and also the page headers using their CSS classes, then it keeps one line for each block of text and drops a line when it repeats the one before.
2.  Cleaning: Non-breaking and thin spaces become normal spaces and repeated whitespace is collapsed, and a separate rule removes the space that EUR-Lex leaves before punctuation.
3.  Split into sections: In the regulations a new section starts at every "Article N" or "ANNEX" line and the next short line is kept as its heading, while chapter and title lines are skipped because they are only layout. In the notices a section starts at a numbered heading or question like "2.1. Legibility" or "3.2.4. Can ...?", counted only from the first "1.", and the table of contents entries that end with a page number are skipped. Each section gets a location like Article 21, Annex II, Section 3.1 or Preamble, which is the label the agent cites.
4.  Chunk: Two designs are built so they can be compared:
    - Structure: one chunk per article, annex or guidance section, and a section longer than 350 words is split into windows of 300 words with 50 words of overlap, labelled "(part n)".
    - Fixed: windows of 200 words with 40 words of overlap over the whole document, ignoring the sections, so a window can be labelled "Article 20 to Article 22".
5.  Embed and store: Every chunk's text starts with a header like "[REG_1169_2011, Article 9: List of mandatory particulars]", so the embedding sees it, and the model gets the source and location as the citation label. The chunks are embedded with gemini at 768 dimensions, to keep index/ under the 90 MB limit, in batches of 20, and they are stored in ChromaDB with cosine distance. Each batch is saved as soon as it arrives and only chunks without a saved vector are embedded, so reaching the daily quota never loses work. Additionally, chunks that a processing fix no longer produces are deleted, which is why the index never holds two versions of the same document.

Extraction problem I fixed: EUR-Lex lays out lettered points as two-cell table rows, for example "(a) the name of the food;" in Article 9(1) of Regulation 1169/2011, and a plain get_text() put the "(a)" and its text on separate lines, so the letter lost its content. I fixed it by joining each table row into one paragraph before the text is read, so now every point is one line and stays in the same chunk as its letter.

**Chunk metadata.** Each chunk stores its source and location, like REG_1169_2011 and Section 3.1 (part 2), which together are the citation label, and also its title, url, heading, design and number of words, which is what it adds to the prompt. Additionally, the id is a SHA-1 of the chunk's design, source, location and text, so the same chunk is never embedded twice, and the covers field lists every section a fixed window's words come from, which the hit rate needs.

**Number of chunks.**

| Document | Sections | Structure chunks | Fixed chunks |
| --- | --- | --- | --- |
| REG_1169_2011 | 71 | 118 | 141 |
| REG_1924_2006 | 30 | 50 | 59 |
| REG_432_2012 | 4 | 63 | 95 |
| QA_NOTICE_2018 | 42 | 44 | 35 |
| ALLERGEN_NOTICE_2017 | 11 | 13 | 15 |
| QUID_NOTICE_2017 | 6 | 19 | 27 |
| **Total** | **164** | **307** | **372** |

REG_432_2012 has only 4 sections but 15,190 words, because almost all of it is the Annex, a long table of permitted claims, so most of its 63 chunks are parts of the Annex and a hit on any of them says little, which is why the retrieval section separates precise and broad questions. The Q&A notice is the opposite, its 42 sections are short, so the structure design gives it more chunks than the fixed design (44 against 35).


## Test set

*How you wrote it, counts by kind, two examples.*

The test set has 40 questions, 28 single, 6 multi and 6 unanswerable, and I graded 20 of the agent's answers myself so I could compare my grades with the LLM judge.

I wrote the questions from the point of view of the quality and regulatory team, as label situations they would actually check, and many of them use a number just above or below a legal threshold, like 3.2 g of fat for "low fat" where the limit is 3 g, or 18% of energy from protein for "high protein" where the limit is 20%, so the agent has to apply the condition and not only find the right article. For every question I wrote down which passage should answer it in expected_source and expected_location, and a short reference answer taken from that passage, which is what both the judge and I grade against. All six documents are covered.

The multi questions need two passages to be answered and they list both separated by ";", in five of them both passages are in the same regulation and only q05 needs two documents. The unanswerable questions are close to the topic of the corpus, so the agent cannot just see that they are off topic. Some ask about other laws, like organic food or pesticide residues, and others ask for a detail the corpus does not give, like the gluten-free threshold, which the guidance only refers to in another regulation. This is why they have no expected source and their reference answer says what is missing.

| Kind | Questions | Graded by me | What it tests |
| --- | --- | --- | --- |
| single | 28 | 8 | one passage answers it |
| multi | 6 | 6 | needs two passages and the answer has to combine them |
| unanswerable | 6 | 6 | the corpus does not cover it, so the agent should say so |
| **Total** | **40** | **20** | |

**Example 1 (multi, q05).** "Can a yogurt containing 4 g of sugar per 100 g be labelled "low sugar", and what nutritional information must it provide?" Expected: [REG_1924_2006, Annex]; [REG_1169_2011, Article 30]. Reference answer: yes, if the other conditions are met, because solid foods with no more than 5 g of sugar per 100 g meet the threshold, and the nutrition declaration has to include energy, fat, saturated fat, carbohydrates, sugars, protein and salt.

**Example 2 (unanswerable, q23).** "What is the exact maximum gluten concentration in mg/kg allowed for a product to be labelled "gluten-free"?" Expected: none. Reference answer: the guidance refers to Regulation 828/2014 but does not give the number, so that regulation would be needed. This question is a trap, because the model probably knows the number from its training, so it checks that the agent says the corpus does not cover it instead of answering from memory.

## Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

I chose the structure design with k = 5. To compare the designs, evaluate.py embeds each question once and takes the top 5 chunks from both designs, only from the six original documents, and a question counts as a hit at k when one of its expected passages is in the top k (for fixed windows any section in the covers field counts).

| Design | hit@1 | hit@3 | hit@5 | multi, both passages @1 / @3 / @5 | words added @1 / @3 / @5 |
| --- | --- | --- | --- | --- | --- |
| structure | 88% | 97% | 100% | 0% / 33% / 67% | 242 / 720 / 1,169 |
| fixed | 82% | 91% | 97% | 17% / 17% / 17% | 200 / 598 / 988 |

| Design | precise hit@1 / @3 / @5 (n = 18) | broad hit@1 / @3 / @5 (n = 16) |
| --- | --- | --- |
| structure | 78% / 94% / 100% | 100% / 100% / 100% |
| fixed | 67% / 83% / 94% | 100% / 100% / 100% |

The multi columns are only over 6 questions, so 67% means 4 questions. A precise question has an expected location with at most 2 chunks, and a broad one has more, like the Annex of REG_432_2012, where any chunk counts as a hit.

Structure has a higher hit rate at every k, and as the second table shows all the difference comes from the precise questions, since both designs find the broad ones every time. It is also much better with the multi questions, it finds both passages for 4 of the 6 at k = 5 while fixed only gets 1, and its chunks have the same labels the agent cites, so the citation-check guardrail can check them directly. The downside is that it adds about 18% more words to the prompt (1,169 against 988 at k = 5), but I think it is worth it.

I chose k = 5 instead of 3 because every question gets at least one expected passage and the multi questions get both passages 4 times out of 6 instead of 2. This costs 449 more words per search, however a missed passage can mean a wrong answer for the team, which is much worse than a longer prompt.

## Tools and subagent

*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

**Tool descriptions.** My MCP server has two tools. The first one, search(query), looks for the 5 passages most similar to the question in the six documents and gives each one a label like [REG_1169_2011, Article 21] and a similarity score, and its description tells the model to cite that label for every claim and to say the corpus does not cover something instead of answering from memory. It also tells the model to search again with other words if the results are not enough, and to do one search for each part of a question. The second one, add_document(path), adds a new file (.html, .pdf, .txt or .md) to the corpus using the same steps as index.py, and its description says to only use it when the user asks for it.

**One search result.** As an example, this is the first passage the search found for q36, which asks what salt content should appear on a food with 0.32 g of sodium per 100 g. I copied it from eval/grading_sheet.md, which only keeps the label and the text, but when the agent gets it from search it also comes with "cite as [QA_NOTICE_2018, Section 3.2.4]", the similarity score and the name of the document.

```
[QA_NOTICE_2018, Section 3.2.4] Relevant provisions: Annex I, point 11 Yes, the equivalent salt content must always be derived from the total sodium content of the food product by using the formula: salt = sodium × 2,5.
```

**Subagent instructions.** I also have a subagent called corpus-researcher (in .claude/agents/corpus-researcher.md), which only has the search tool and is used whenever a question is about what an EU food label must, may or may not say. Its instructions have five rules, basically it has to search before answering (at most five times), answer only from the passages and not from memory, and cite every claim with the label. If the corpus only covers part of the question it has to say which part is missing, and the answers should be short, with the yes/no or the rule first and then the conditions.

### Transcript: Claude Code delegating to the `corpus-researcher` subagent

**User:** use the subagent corpus-researcher to answer: Is a nutrition declaration mandatory for a beer with 5% alcohol?

**Claude Code → subagent `corpus-researcher`** ("Beer nutrition declaration question"):

> Answer this question from the corpus, with citations: Is a nutrition declaration mandatory for a beer with 5% alcohol?
>
> Search the corpus, cite every claim with the label shown in the results (e.g. [REG_1169_2011, Article X]), and say clearly if any part of the question is not covered. Include in your report the queries you ran and the passage labels you relied on.

*Subagent finished (its own transcript, with the searches, is under `/tasks`).*

<details><summary>Claude Code's first reply (in Spanish)</summary>

El subagente ha terminado. Esto es lo que encontró en el corpus.

Respuesta: no, por norma general no es obligatoria
Una cerveza de 5% está por encima del umbral de 1,2% de alcohol. Por eso no tiene que llevar declaración nutricional ni lista de ingredientes [REG_1169_2011, Article 16].

Matices que da el corpus:

Otras normas. La exención se aplica "sin perjuicio" de otras disposiciones de la UE que exijan la declaración [REG_1169_2011, Article 16]. La guía de la Comisión añade que también la puede exigir una medida nacional [QA_NOTICE_2018, Section 3.6.1].
Declaraciones (claims). Si el producto lleva una declaración nutricional o de propiedades saludables, el etiquetado nutricional pasa a ser obligatorio [REG_1169_2011, Article 49].
Aplicar esto a la cerveza es una deducción del subagente, que lo avisó. Une dos pasajes, pero ninguno lo dice textualmente para bebidas alcohólicas. El equipo debería confirmarlo antes de dar por buena esa regla.
Qué declaraciones puede llevar una cerveza. Ninguna de propiedades saludables. Las únicas declaraciones nutricionales permitidas se refieren a la reducción del contenido de alcohol o de energía [REG_1924_2006, Article 4 (part 2)].
Si se pone de forma voluntaria. Debe seguir las reglas de la declaración obligatoria. En bebidas alcohólicas puede limitarse solo al valor energético [QA_NOTICE_2018, Section 3.6.1].
Lo que sí es obligatorio aunque no se haya preguntado: el grado alcohólico, con como máximo un decimal seguido de "% vol" [REG_1169_2011, Article 28]. Para cervezas de hasta 5,5% vol la tolerancia es de ±0,5% vol [REG_1169_2011, Annex XII].
Lo que el corpus no cubre
Si hoy existe una norma posterior que lo exija. El Artículo 16 pedía a la Comisión un informe para el 13 de diciembre de 2014 y, si procedía, una propuesta legislativa sobre información nutricional obligatoria para bebidas alcohólicas [REG_1169_2011, Article 16]. El corpus no recoge qué pasó después. El equipo debe consultar la normativa vigente antes de aprobar la etiqueta.
Las normas nacionales sobre declaraciones de alcohol o energía reducidos o nulos que permite el Reglamento 1924/2006.
Por qué la respuesta está construida así: sigue las reglas 3 y 4 de AGENTS.md. Responde la parte que el corpus respalda, con citas, y separa lo que no se puede determinar. Así no se da por vigente una exención que podría haber cambiado desde 2014.

</details>

**User:** pero en ingles

**Claude Code:**

> **Answer: no, as a general rule it is not mandatory**
>
> A beer at 5% is above the 1.2% alcohol threshold, so it does not have to carry a nutrition declaration or a list of ingredients [REG_1169_2011, Article 16].
>
> Caveats from the corpus:
>
> - Other rules. The exemption applies "without prejudice to" other EU provisions that require a nutrition declaration [REG_1169_2011, Article 16]. The Commission guidance adds that a national measure can also require one [QA_NOTICE_2018, Section 3.6.1].
> - Claims. If the product carries a nutrition or health claim, nutrition labelling becomes mandatory [REG_1169_2011, Article 49]. Applying this to beer is the subagent's own conclusion, and it said so. It comes from reading two passages together, and neither one says it word for word for alcoholic drinks. The team should confirm it before relying on it.
> - Which claims a beer may carry. It may not carry any health claims. The only nutrition claims allowed are about a reduction in alcohol or energy content [REG_1924_2006, Article 4 (part 2)].
> - If given voluntarily. The declaration must follow the rules for the mandatory one. For alcoholic drinks it may be limited to the energy value alone [QA_NOTICE_2018, Section 3.6.1].
> - What is mandatory, even though you didn't ask: the alcoholic strength, as a figure with no more than one decimal place followed by "% vol" [REG_1169_2011, Article 28]. For beers up to 5.5% vol the tolerance is ±0.5% vol [REG_1169_2011, Annex XII].
>
> **What the corpus does not cover**
>
> - Whether a later rule now requires it. Article 16 asked the Commission for a report by 13 December 2014 and, if appropriate, a legislative proposal on mandatory nutrition information for alcoholic drinks [REG_1169_2011, Article 16]. The corpus has nothing on what happened after that. The team needs to check the current rules before approving the label.
> - National rules on claims about reduced or zero alcohol or energy, which Regulation 1924/2006 allows.
>
> Why the answer is built this way: it follows rules 3 and 4 in AGENTS.md. It answers the part the corpus supports, with citations, and keeps apart what can't be determined from it. That way the answer doesn't present an exemption from 2014 as still current when it may have changed.



## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

If a document is already indexed with the same content, add_document embeds nothing, and if a file with the same name has different content, the old chunks are replaced by the new ones. I also fixed a bug with REG_432_2012, which only has 2 articles, so add_document treated it as a guidance notice and chunked it differently than index.py, and now it uses the same information as index.py for the corpus documents.

For the demo I used q23, about the maximum gluten level for "gluten-free", because the allergen notice refers to Regulation 828/2014 but does not give the number. So I added Commission Implementing Regulation (EU) No 828/2014, which I got from Cellar because EUR-Lex blocked the download, and after I approved add_document it was split into 10 chunks.

Before adding the document, the agent answered:

> Based on the provided search results, the corpus does not contain the exact numeric threshold (in mg/kg) for the "gluten-free" claim set out in Commission Implementing Regulation (EU) No 828/2014, although the guidance mentions that products must meet the requirements of that Regulation to use the statement "gluten-free" or "very low gluten" [ALLERGEN_NOTICE_2017, Section 3.1 (part 1)].
>
> The corpus does not cover the specific maximum concentration value in mg/kg.

After adding it, the same question got:

> The statement "gluten-free" may only be made where the food as sold to the final consumer contains no more than **20 mg/kg** of gluten [REG_828_2014, Annex].

The agent went from saying the corpus does not cover it to giving the exact number with a citation to the new document, and when I added the same file again nothing was embedded because it was already indexed.

## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
