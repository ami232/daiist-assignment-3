# Assignment 3 Report

- **Name**: Paula Candiles Puente
- **Student ID**: 18670
- **Group**: BBADBA 5B

## Use case

**Who asks.** A university student (for example, a Spanish bachelor's student) who is thinking about applying for an Erasmus+ grant ("beca Erasmus") to study for a semester or a year at another European university. They ask before applying and while preparing to leave. 

Typical questions: 
- Am I eligible? 
- How long can I go? 
- How is the monthly grant calculated? 
- Is there extra support if I have fewer opportunities?
- What is a learning agreement, and what happens if I change courses? 
- Will my credits be recognised? 
- Do I pay tuition at the host university?

**What they do with the answer.** They decide if they want to applu and when, plan their budget and choose courses, so they act on the answer directly.

**What a wrong answer costs.** A wrong answer can make a student apply for a period that is not eligible, count on money they will not receive, change courses without updating the learning agreement and lose recognition of their credits.

Each of these costs money or a semester and is hard to undo. 

- "I don't know, ask your university's international office" costs one email. 

So the assistant must refuse rather than guess, and must cite the rule it relies on so the student can check it.

**Scope.** The corpus holds the European rules that apply in every country. Amounts in euros set by a national agency (SEPIE in Spain) or a university, and each university's own deadlines and selection criteria, are not in it as they are private dicuments. 

The assistant should send those questions to the student's home university rather than answer them.

## Corpus

All four documents are published by the European Commission and are reusable under its reuse policy (Commission Decision 2011/833/EU): content owned by the EU is licensed under **CC BY 4.0** (see the [legal notice](https://commission.europa.eu/legal-notice_en)). 

None contains personal data (this is really important). 

The Erasmus+ **name and logo are trademarks and are not covered by the licence**, but only the text is used here.

| Document | URL | Date | Licence | Words |
|---|---|---|---|---|
| Erasmus+ Programme Guide 2026: Part A (pp. 4–36), Key Action 1 and Higher Education mobility (pp. 39–72), Part D Glossary (pp. 443–456) | [PDF](https://erasmus-plus.ec.europa.eu/sites/default/files/2025-11/programme-guide-2026_en.pdf) | Version 1, 12/11/2025 | CC BY 4.0 | 39,140 |
| Erasmus Charter for Higher Education 2021–2027: Annotated Guidelines | [PDF](https://erasmus-plus.ec.europa.eu/sites/default/files/charter-annotated-guidelines-feb2020_en.pdf) | February 2020 | CC BY 4.0 | 10,880 |
| Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) | [web page](https://erasmus-plus.ec.europa.eu/resources-and-tools/mobility-and-learning-agreements/learning-agreements/studies-agreement-guidelines-ka131) | accessed 12/11/2026 | CC BY 4.0 | 3,269 |
| Erasmus+ Student Charter | [web page](https://erasmus-plus.ec.europa.eu/resources-and-tools/erasmusplus-student-charter) | accessed 12/11/2026 | CC BY 4.0 | 1,781 |
| **Total** | | | | **55,070** |

Only the **student-relevant parts** of the Programme Guide are kept, because if not it is too long (the full guide has **456 pages and about 199,000 words**, mostly about youth, sport, schools and funding for organisations).
 
Indexing all of it would **add noise and cost more than the free tier's ~1,000 embeddings a day**. Word counts are the raw extracted text, before cleaning.

## Ingestion

To build the index I run one command: `uv run python main.py index`. 

### Step 1: Download

The script downloads the four documents from the European Commission website into a `corpus/` folder. This folder is not uploaded to GitHub. If a file is already there, it is not downloaded again.

### Step 2: Take the text out

**PDFs.** I only keep the pages that matter to a student:

- Programme Guide, pages 4–36: general rules, who can take part and which countries are eligible.
- Programme Guide, pages 39–72: student mobility in higher education, including the rules on grants.
- Programme Guide, pages 443–456: the glossary.
- ECHE Guidelines from page 5 onwards, because pages 1–4 are only the cover and the table of contents.

The PDF gives the text line by line, so the script joins the lines back into paragraphs. It also spots the titles: in the Programme Guide they are lines in CAPITAL LETTERS, and in the ECHE Guidelines they are numbered, like "2.2 During Mobility".

**Web pages.** For the Learning Agreement guidelines and the Student Charter I only keep the main text. I remove the menus, the "On this page" and "Related links" lists, a photo credit and the "Last updated" line, but I keep that date for the metadata. 

For every paragraph, the script remembers **which page it was on and which title it was under**, so each answer can later say exactly where it comes from (really important).

### Step 3: Clean the text

PDF text is messy, so the script:

- removes page numbers;
- removes the header that repeats on every page of the ECHE Guidelines;
- fixes words the PDF split badly, like "forward -looking" → "forward-looking";
- turns the different bullet symbols into a simple "-".

### Problems I found and fixed

**1. Footnotes mixed into the text.** The Programme Guide has many footnotes. When the PDF was read, the footnote text ended up in the middle of the normal text, and the footnote numbers stuck to the words, like "funds.63". 

I made the script find the footnotes: they are lines at the bottom of the page that start with a number, where that same number also appears stuck to a word earlier on the page. **The script deletes those lines and the little numbers.** After the fix, there are no "word.63"-style numbers left in any chunk.

There is one small case **I did not fix**. When a footnote number comes right after another number, for example "Regions 13 and 14" with footnote 78, it becomes "1478". I left it because a rule for this could also break real numbers.

**2. Table cells taken for titles.** The grant tables (pages 63–72) have some cells in capital letters, like "786 EUR PER MONTH" or "MOBILITY". The script **thought they were section titles**, so the text after them got the wrong label. Now a line in capitals only counts as a title **if it doesn't start with a number and has at least two words.**

I also fixed **titles that were glued together**. For example, "PRIORITIES OF THE ERASMUS+ PROGRAMME" followed by "INCLUSION AND DIVERSITY" used to **become one long title**. Now it becomes "PRIORITIES OF THE ERASMUS+ PROGRAMME > INCLUSION AND DIVERSITY".

**3. One vector instead of twenty.** The first time I saved the index, the Gemini model gave back one vector for a whole group of 20 chunks instead of one for each. I changed the way the texts are sent and added a check: if the number of vectors doesn't match the number of chunks, the script stops and saves nothing.

### How many words

After cleaning, the corpus has **51,878 words**:

| Document | Words after cleaning |
|---|---|
| Programme Guide 2026 (chosen pages) | 36,867 |
| ECHE Guidelines | 10,395 |
| Learning Agreement guidelines | 2,891 |
| Student Charter | 1,725 |

### Step 4: Cut into chunks

I tried two ways of cutting the text, so that later I can compare them and keep the one that finds the right answer more often. Each one is saved separately.

| Way | How it cuts | Chunks | Words per chunk |
|---|---|---|---|
| **Fixed** | A new chunk every 150 words, with 25 words repeated between neighbouring chunks so nothing is lost at the edges. It ignores the titles. | 415 | 100–150 (150 on average) |
| **Structure** | Follows the sections of the document: a chunk never mixes two sections and has up to about 250 words. Very long paragraphs are split at the end of a sentence, and tiny pieces are joined to the chunk before them. Each chunk starts with its document name and section title, so it is clear what it talks about. | 289 | 9–284 (180 on average) |

### What each chunk keeps (metadata)

- the document it comes from (for example `programme_guide_2026`) and its full title;
- the link to the original document and its date;
- the page where it starts and ends (only for PDFs);
- the section title;
- a ready-made citation, for example *"p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY"* or *"Filling in the learning agreement > Duration"*;
- which of the two ways it was cut with, its position in the document and its number of words.

### Step 5: Turn into vectors and save

Each chunk is turned into a vector with Google's `gemini-embedding-2` model (768 numbers per chunk) and saved in a ChromaDB database in `index/`, which takes 13 MB.

- The chunks are sent in groups of 20, and each group is saved as soon as it's ready. If something fails, at most one group is lost.
- If I run the script again, it only processes chunks that are new or changed, and it deletes old chunks that no longer exist. This matters because the free plan only allows about 1,000 embeddings a day.
- If the daily limit is reached, the script stops cleanly and continues the next day from where it stopped.

Building both ways used **704 embeddings**: 415 + 289.

### Step 6: A change I made later (found while writing the test set)

My first idea was to **delete the footnotes**, because they were breaking the sentences (see "Problems I found and fixed" above). I thought they were just extra details that got in the way.

While writing the test set, I found out this was a mistake, for two reasons:

1. **Some footnotes were not deleted at all.** When the footnote number had a space before it ("can be 65:" instead of "funds.63"), my script didn't recognise it, so the footnote stayed in the middle of the text.
2. **Footnotes contain important rules for students.** For example, the rule that medicine students (and other one-cycle programmes) can be on Erasmus for **up to 24 months** instead of 12 only appears in footnote 67. If I had deleted it, the assistant could never answer that question, or worse, it would say "12 months" to a medicine student.

So I changed my approach: **the footnotes are now kept, but moved to the end of their page** as a separate paragraph, like *"Note 67: In one-cycle study programmes, such as medicine, students can be mobile for up to 24 months."* The little numbers are still removed from the middle of the sentences, so the text reads well. I also fixed the "1478" case from before: it now reads "Regions 13 and 14" again, and the footnote is kept as Note 78.

After the change I checked that no real numbers were damaged: all the grant amounts and rules used in the test set are still exactly as in the documents.

**What changed in the numbers:**

| | Before | After |
|---|---|---|
| Words after cleaning | 51,878 | 53,335 |
| Footnotes kept | 0 (deleted) | 82 |
| Chunks with the **fixed** way | 415 | 427 |
| Chunks with the **structure** way | 289 | 296 |
| Size of `index/` | 13 MB | 16 MB |

To avoid paying again for chunks that didn't change, I made the script reuse the stored vector when a chunk's text is the same. Rebuilding the index used **414 embeddings** instead of 723: 60 for the structure way, where most chunks stayed the same, and 354 for the fixed way, because its 150-word windows move when text is added.

After rebuilding, I tested the medicine question again and the chunk with "up to 24 months" came first.

## Test set

### How I wrote it

The brief asks for questions written from the documents. I did it together with Claude (an AI assistant), in this way:

1. **First, I chose three topics** that matter most to a student applying for an Erasmus+ grant:
   - **Eligibility and duration:** who can go, and for how long.
   - **Grant money:** how much you get, and what extra support exists.
   - **Learning agreement and credits:** what you sign, and how your courses are recognised.
2. **These three topics were the starting point for the questions.** Based on them, Claude read the relevant parts of the documents and gave me a **pool of 35 candidate questions**, each with the page or section where the answer is and a short correct answer.
3. **I reviewed every question** against the documents and approved them before they were saved in `eval/questions.csv`.

I also decided the size (35 questions, a bit more than the minimum of 30, in case I need to drop a weak one later) and the mix of kinds. After the evaluation I changed one question and added another, so my final test set has **36 questions** (see "A mistake in my test set" below).

### Kinds of questions

| Kind | How many | What it tests |
|---|---|---|
| **Single** | 23 | The answer is in one place in the documents. |
| **Multi** | 7 | The answer needs two passages together. For example, one page says which group Germany is in, and another says how much you get when moving between groups. |
| **Unanswerable** | 6 | The question is about Erasmus, but the answer is **not** in the documents. The assistant must say it doesn't know and send the student to the right place, instead of guessing. |

The unanswerable questions are on purpose very close to the topic, because those are the dangerous ones. For example, the Programme Guide mentions a deadline of **19 February**, but that deadline is for universities asking for money, not for students. A bad assistant could give that date to a student who asks "When is my university's deadline?".

### A mistake in my test set (found by the evaluation)

One of my "unanswerable" questions was **u05**: *"When will the first Erasmus grant payment reach my bank account?"*. I thought the documents didn't say anything about payments. But when I ran the evaluation, the assistant answered it, and when I checked, it was **right**: the Student Charter says *"You are entitled to receive a pre-financing payment within 30 calendar days following the signature of the agreement by both parties [...] and no later than the start date of the mobility period."*

So the mistake was in my test set, not in the assistant. I fixed it in two steps:

1. I changed u05 into a normal "single" question, **q23**, with the Student Charter as its source.
2. To keep 6 unanswerable questions, I added a new one, **u07**: *"Can my Erasmus grant be paid into a bank account outside Spain, for example a German one?"*. Before adding it, I checked that no document mentions bank accounts at all, so I don't repeat the same mistake.

This taught me that an "unanswerable" question has to be checked against **all** the documents, not just the one I expect.

### Why some questions are in Spanish

**5 of the 36 questions are in Spanish** (q02, q08, q16, q18 and m01). The assistant should be able to answer in **both English and Spanish**, because:

- The users I have in mind are Spanish university students applying for a "beca Erasmus", and many of them will naturally ask in Spanish.
- The documents are only in English.

So I need to test whether a question in Spanish still finds the right English passage and gets a correct answer. If it doesn't, Spanish students would get worse answers than English speakers, which would not be fair for my use case.

### Examples

**Example 1 (multi, in Spanish):**
- **Question:** *"Estudio en España y me voy a Alemania. ¿Qué tramo de beca me corresponde y de cuánto es?"*
- **Where the answer is:** Programme Guide, p. 67 (Germany is in Group 1) and p. 68 (Spain is in Group 2, and the grant ranges).
- **Correct answer:** Going from Group 2 to Group 1 means the **higher range**: between **348 and 674 EUR per month**.
- **Why it is a good test:** the assistant has to combine two passages, and the question is in a different language from the documents.

**Example 2 (unanswerable):**
- **Question:** *"When is the Erasmus application deadline at my university?"*
- **What the assistant should say:** that the documents don't include student deadlines, because each university sets its own, and that the student should ask their international office.
- **Why it is a good test:** the documents mention a "19 February" deadline that is **not** for students, so this checks that the assistant doesn't give a wrong date that looks right.

## Retrieval

### What I tested

Before the assistant writes an answer, it **searches** the documents and picks the chunks that seem most related to the question. If the chunk with the answer isn't among them, the answer will be wrong, however good the AI model is. So before building the assistant, I checked how good the search is.

For each of my questions that have an answer (29 at first, 30 after the change to my test set described above), I checked whether **the chunk with the answer is among the results the search gives back**. I measured it in three ways:

- **hit@1:** the right chunk is the **first** result.
- **hit@3:** the right chunk is in the **first 3** results.
- **hit@5:** the right chunk is in the **first 5** results.

I compared the two ways of cutting the text from the Ingestion section: **fixed** (every 150 words) and **structure** (following the sections of the document).

### First results

| | Fixed | Structure |
|---|---|---|
| Right chunk is 1st | 16 of 29 | 21 of 29 |
| Right chunk in first 3 | 22 of 29 | 27 of 29 |
| Right chunk in first 5 | 26 of 29 | 28 of 29 |
| Spanish questions: right chunk in first 3 | 3 of 5 | 5 of 5 |

### A correction I made: "misses" that were not really misses

When I looked at the questions that failed, I saw that some of them were **not real failures**. Sometimes the search found a **different page that also has the correct answer**.

For example, for *"Do I have to pay tuition at the host university?"*, my test set said the answer is in the ECHE Guidelines, p. 8. But the Programme Guide, p. 43, **also** says that students don't pay tuition fees. The search found p. 43 first, and because I had only written down p. 8, it was counted as a miss even though the information was correct.

I had two options:
- **Option A:** add the other correct pages to the test set.
- **Option B:** leave the test set as it was.

I chose **Option A**, because the results become fairer: finding a correct page should always count as a success. What I want to measure is whether the search finds **correct information**, not whether it finds the exact page I happened to write down.

I didn't add pages blindly. I **checked each one against the text**, and only added it if it really contained the full answer:

| Question | Page added | Why |
|---|---|---|
| q05 Short stay abroad | Learning Agreement guidelines, "Learning agreement types and mobility duration" | It also says 5–30 days with an online part |
| q16 Tuition fees | Programme Guide p. 43 and Student Charter | Both say no tuition fees |
| q17 Who signs the learning agreement | ECHE Guidelines p. 15 | It says the three parties sign before the mobility |
| q21 ECTS per year | ECHE Guidelines p. 8 and Learning Agreement guidelines | Both say 60 ECTS |

I **rejected** four other pages, because they only had part of the answer or talked about something different. For example, Programme Guide p. 58 also mentions "3 ECTS", but for a different kind of programme (Blended Intensive Programmes), so it doesn't answer q06.

### Final results

These results include the correction above and the new question q23 (the old u05, see the Test set section), so they use **30 questions**.

| | Fixed | Structure |
|---|---|---|
| Right chunk is 1st | 18 of 30 (60%) | **26 of 30 (87%)** |
| Right chunk in first 3 | 25 of 30 (83%) | **28 of 30 (93%)** |
| Right chunk in first 5 | 28 of 30 (93%) | **29 of 30 (97%)** |
| **Spanish** questions: right chunk is 1st | 3 of 5 | **5 of 5** |
| Words added to the prompt (first 5 chunks) | 749 | 891 |

**Structure wins at every level.** The biggest difference is with **Spanish questions**: with structure, all 5 find the right English chunk as the very first result. I think the reason is that every structure chunk starts with its document name and section title (for example, "Eligibility criteria for student mobility"), which gives the search a clear hint about what the chunk is about.

The only cost is that structure chunks are a bit longer: the assistant reads about **891 words** per question instead of 749, roughly 19% more. For a much better search, I think that's worth it.

### What still fails

1. **"What counts as green travel?"** This is the only question where nothing correct appears in the first 5. The answer is in the **glossary** at the end of the Programme Guide, where one chunk mixes many short definitions, so the search doesn't see that it's about green travel.
2. **Three multi questions** (m04, m05, m07) only find **one of the two pieces** of information they need. For example, for the 3-week programme question, the search finds the daily amounts (p. 69) but not the rule about 5–30 days (p. 54). The agent may fix this later by searching more than once.

### My choice

I use **structure** and give the assistant the **first 5 results**. With 5 results, the right chunk is there for 29 of 30 questions, compared with 28 with 3. It also gives the multi questions a better chance of getting both pieces of information they need.

## Tools and subagent

### The two tools

My MCP server ([server.py](server.py)) is called `corpus` and has two tools. The description of each tool is what the AI reads to decide when and how to use it, so I wrote them carefully.

**`search(query, k=5)`**

> Search the official European Commission rules on Erasmus+ grants for university students: the Erasmus+ Programme Guide 2026 (who can take part, student mobility for studies and traineeships, durations, grant amounts and top-ups, glossary), the Erasmus Charter for Higher Education guidelines, the Learning Agreement for Studies guidelines and the Erasmus+ Student Charter.
>
> Use it for any question about Erasmus+ eligibility, duration, money, learning agreements, credit recognition or students' rights. Questions may be in English or Spanish; the documents are in English. It does NOT contain national amounts (e.g. SEPIE in Spain) or any university's own deadlines, places or selection criteria.
>
> Returns the k most relevant passages (default 5, max 10), numbered [1]..[k], each with document title, page or section, date, URL and the passage text. Cite them by number and by document + page/section.

I made the description say clearly **what is not in the documents**, so the AI knows when it should say "I don't know" instead of searching forever or guessing.

**`add_document(path)`**

> Add a document to the Erasmus+ search index so search can find it. `path` is a file inside this project folder: .pdf, .html, .txt or .md. The file is extracted, cleaned and chunked with the same pipeline as the original corpus (index.py), embedded and stored. Its id is the file name.
>
> If the document is already indexed and unchanged, nothing is embedded and nothing is duplicated. If a file with the same name was indexed before but its content changed, its old chunks are replaced by the new ones.
>
> Returns how many chunks were embedded, reused, already present and removed.

For safety, `add_document` only accepts files **inside the project folder**, so the AI can't read random files on my computer. When I tested it with `/etc/hosts`, it answered *"Refused: /etc/hosts is outside the project folder."*

### One search result

I asked in Spanish: *"¿Cuántos meses de Erasmus puedo hacer en total durante el grado?"*. This is the first result:

```
[1] Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY, 2025-11-12 (version 1)
source: programme_guide_2026 | url: https://erasmus-plus.ec.europa.eu/sites/default/files/2025-11/programme-guide-2026_en.pdf | relevance: 0.75
- during the third cycle as doctoral candidate (doctoral level or EQF level 8). The duration of a traineeship by
recent graduates counts towards the 12 months maximum of the cycle during which they apply for the traineeship. [...]
Note 66: Prior experience under the Erasmus+ Programme and/or as Erasmus Mundus scholarship holders counts
towards the 12 months per study cycle.
Note 67: In one-cycle study programmes, such as medicine, students can be mobile for up to 24 months.
```

Each result starts with a **citation line** (document, page, section, date) that the AI can copy into its answer, plus the link to the original document. This result also shows that keeping footnotes was worth it: Notes 66 and 67 contain important rules about the 12-month limit.

### The subagent

The subagent is in `.claude/agents/corpus-researcher.md`. It can **only** use the `search` tool, so it can't add documents or do anything else. Its instructions say:

1. **Always search before answering**, never answer from memory, because Erasmus+ rules change every year.
2. If the question has **several parts**, search once for each part. I added this rule because in my retrieval test, questions that needed two passages often found only one.
3. **Every rule, number or amount needs a citation** (document + page or section).
4. If the documents don't answer the question, **say so and don't guess**, and tell the student where to ask: SEPIE or their university for exact amounts, their international office for deadlines, places and selection.
5. If the documents give a **range** and not an exact amount, give the range and explain who sets the exact amount.
6. **Answer in the language of the question**, English or Spanish.
7. **Be short**: direct answer first, then details.

### Transcript from my editor (Claude Code)

I asked my multi question in Spanish. Claude Code passed it to the `corpus-researcher` subagent, which searched the documents and returned this answer (shortened):

> **Me:** Answer this question: *Estudio en España y me voy a Alemania. ¿Qué tramo de beca me corresponde y de cuánto es?*
>
> *Claude Code delegated the question to the `corpus-researcher` subagent.*
>
> **Subagent:**
> **Respuesta breve:** Si estudias en España y te vas a Alemania, te corresponde el **tramo superior ("Higher range EU grant")**. La Comisión fija para este tramo una horquilla de **348 a 674 EUR al mes**. El importe exacto dentro de esa horquilla lo decide SEPIE, en algunos casos junto con tu universidad. Los documentos no dan esa cifra.
>
> 1. **Grupos de países según el coste de vida** (Programme Guide 2026, pp. 67-68): Alemania está en el Grupo 1 (coste de vida más alto) (p. 67) y España en el Grupo 2 (coste de vida medio) (p. 68).
> 2. **Qué tramo se aplica** (p. 68): de España (Grupo 2) a Alemania (Grupo 1) es el caso "from Group 2 to Group 1 countries", así que se aplica el tramo superior, 348-674 EUR/mes: el tramo medio que aplique la Agencia Nacional "plus at least 50 EUR".
> 3. **Quién fija la cantidad exacta:** las cantidades mensuales "will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs" y se publican en sus webs (p. 67). Todos los estudiantes que van al mismo grupo de países reciben lo mismo, salvo los complementos (p. 72).
> 4. **Complementos** (p. 68): +250 EUR/mes para estudiantes con menos oportunidades; +150 EUR/mes solo para prácticas; y si tu universidad está en una región ultraperiférica, como Canarias, la cuantía es de 786 EUR/mes (p. 69).
>
> **Lo que los documentos no dicen:** la cuantía exacta que SEPIE fija para el tramo Grupo 2 → Grupo 1, los criterios en España para ser "estudiante con menos oportunidades", y los plazos, plazas y pagos de tu universidad. Consúltalo con SEPIE o con la oficina internacional de tu universidad.
>
> Fuente: Erasmus+ Programme Guide 2026 (versión 1, 12-11-2025), pp. 67-69 y 72.

**What I checked:** I compared every fact with the documents, and all of them are correct and on the cited pages, including the Canary Islands, which the Programme Guide lists as an outermost region. The answer **follows the rules I gave the subagent**:
- It answered in Spanish.
- It cited pages.
- It gave the EU **range** instead of inventing an exact amount.
- It clearly said what the documents don't cover, and where to ask instead.

This matches the expected answer in my test set (m01).

## Adding a document

### What happens if a document is already indexed

The `add_document` tool uses the same steps as the rest of my index (`index.py`). Each chunk gets an id that includes a fingerprint (a hash) of its text, so the tool can tell if a document is new, the same, or changed:

- **Already indexed and unchanged:** nothing is added and no embeddings are used. When I tried to add the Student Charter again, the tool answered *"Already indexed and unchanged: nothing was added"*.
- **Same file name but the content changed:** the old chunks are deleted and replaced by the new ones, so there are no duplicates or old versions.
- **New document:** its chunks are embedded and stored.

### The question and the document

I chose my unanswerable question **u01**: *"What exact monthly amount does SEPIE pay Spanish students going to Italy in 2026/27?"*. It is one of the most important questions for my users, and the European documents can't answer it, because they only give minimum and maximum amounts for the whole EU.

The document that answers it is SEPIE's **"Información sobre financiación de los proyectos Erasmus+ gestionados por el SEPIE – Convocatoria 2026"** (version of 22/07/2026), from [sepie.es](https://www.sepie.es/educacion-superior/convocatoria.html). On page 10 it gives the amounts that SEPIE sets for Spain:

| Destination | Examples | SEPIE amount |
|---|---|---|
| Group 1 (higher living costs) | Germany, France, **Italy** | 350–674 € per month |
| Group 2 (medium) | Portugal, Greece | 300–606 € per month |
| Group 3 (lower) | Poland, Romania | 250–550 € per month |

**A licence problem.** At the start of the project I decided to use only public documents with a licence that allows reuse. SEPIE's [legal notice](https://www.sepie.es/aviso_legal.html) says its content cannot be reproduced or distributed without permission. My `index/` folder is uploaded to GitHub with the text of the chunks, so I could not keep this document in it. My solution was to add it **only on my computer** for this test, and to **remove it again afterwards**, so none of SEPIE's text is committed. In this report I only quote the amounts, as a short citation.

### Adding it

I asked the assistant: *"Please add the file corpus/sepie/infofinanciacioneplus2026_julio.pdf to the index."* Before the tool ran, the approval step asked for permission, and I said yes. The tool added **49 chunks** from SEPIE's document.

### Before and after

**Before** (from my evaluation run):

> *I do not know the exact monthly amount. The European Commission does not set the specific grant amounts for students; instead, it defines minimum and maximum ranges, and the exact amounts are determined by the National Agencies (such as SEPIE in Spain) [...] Higher range EU grant: Between 348 and 674 EUR per month (Programme Guide 2026, p. 68).*

**After adding the document: no change!** The assistant gave the **same answer**, word for word. It searched only once, in English (*"Erasmus+ grant amounts for students 2026/27"*), and all the results came from the English Programme Guide.

### What I found: the search prefers the language of the question

From the start I wanted my assistant to answer in **both English and Spanish**. With only English documents, Spanish questions worked well: in my retrieval test, all 5 Spanish questions found the right English passage as the very first result.

But when I added a **Spanish** document, I found the opposite problem. I tested the same search in both languages:

- **English question:** the 15 best results were **all** from the English Programme Guide. SEPIE's chunks didn't appear at all.
- **Spanish question** (*"¿Cuánto paga el SEPIE al mes a un estudiante que se va a Italia en 2026/27?"*): the 14 best results were **all** from SEPIE, and the first one was exactly the right table.

So the search prefers documents **in the same language as the question**. An English question never reached the Spanish document.

### How I fixed it

1. **First try: a soft rule.** I added to `AGENTS.md`: *"If the question is about Spain, also search in Spanish."* I also updated the description of the `search` tool, which said that all documents were in English. **It didn't work:** the assistant still searched only once, in English. This matches what I saw in my evaluation, where the assistant almost never searches twice.
2. **Second try: a firm rule with an example.** I changed it to: *"you MUST make at least two searches: one in English and one in Spanish, keeping words like 'SEPIE' in both. Example: 'SEPIE grant amount Italy' and 'importe ayuda SEPIE Italia estudiantes'."* **This worked.**

**After the fix**, the assistant searched twice (*"importe ayuda SEPIE estudiantes Erasmus 2026/27 Italia"* and then in English) and answered:

> *For Spanish students going to Italy (which is classified as a Group 1 country with higher living costs) in the 2026/27 academic year, the monthly grant amount for long-term mobility is set within the range of **350 € to 674 € per month** (infofinanciacioneplus2026 julio, p. 10). [...] the specific amount you will receive within that range is determined by SEPIE and your home university based on their own criteria (Programme Guide 2026, p. 67).*

| | Before | After adding SEPIE and the fix |
|---|---|---|
| Answer | "I do not know"; EU range 348–674 € | **350–674 € per month for Italy, set by SEPIE**; the exact amount is chosen by each university |
| Documents used | Programme Guide only | SEPIE's document + Programme Guide |

This is the real, complete answer: SEPIE does not pay one single amount, but sets a range for each group of countries, and each Spanish university chooses its exact amount inside it.

**Afterwards** I removed SEPIE's 49 chunks from the index (it went back to 296 chunks). I kept the "search in both languages" rule, because it is true for any Spanish document that is added in the future, and it doesn't cause any problem with the current English documents.

**What I learned:** adding a document is not enough. The assistant also has to **search in the right way** to find it, and a soft instruction was not enough to change its behaviour; it needed a clear, firm rule.

## Harness and guardrails

The "harness" is the program around the AI that controls what it can do. Mine is in [agent.py](agent.py). When someone asks a question (`uv run python main.py ask "..."`), it:

1. gives the AI my rules from `AGENTS.md`;
2. connects it to my search tool, so it can look things up in the documents;
3. lets it search and write an answer;
4. checks the answer before showing it.

The AI model is Google's **Gemini** (`gemini-3-flash-preview`). If it is overloaded or doesn't answer, a smaller model (`gemini-3.1-flash-lite`) takes over automatically.

### My rules (AGENTS.md)

`AGENTS.md` is like the instructions you give a new employee before they start answering questions. It has 10 rules, and each one says **why** it exists. The most important ones:

| Rule | Why |
|---|---|
| **Always search before answering**, never answer from memory. | Erasmus+ rules change every year, and students act on the answer. |
| **If the question has two parts, search twice.** | In my retrieval test, one search often found only half of the answer. |
| **Only say what the documents say.** | If something is not in the documents, the student can't check it. |
| **Cite every fact**, always in the same format, e.g. *(Programme Guide 2026, p. 54)*. | The student must be able to check it, and my code needs a fixed format to check the citations automatically. |
| **If the documents don't have the answer, say "I don't know"** and tell the student where to ask (SEPIE or their university). | A wrong answer can cost a student money or a semester. "Ask your international office" costs one email. |
| **Be careful with information that looks right but is for someone else.** For example, the 19 February deadline in the Guide is for universities, not students. | These are the most dangerous mistakes, because they sound correct. |
| **If the documents only give a range, give the range** and say who sets the exact amount. | The EU only sets minimum and maximum amounts, not each student's real grant. |
| **Answer in the student's language** (English or Spanish). | My users are Spanish students, but the documents are in English. |

### Approval before adding a document

The assistant has a second tool, `add_document`, which adds a new file to the documents it searches. This changes every future answer, so **a person must say yes first**. Before the tool runs, the program asks:

```
The assistant wants to add this document to the index:
  corpus/erasmus/student_charter_en.html
Allow? [y/N]
```

Only "y" (or "yes", "sí") lets it run. Anything else, or no answer, means no.

I tested it by asking the assistant to add a document while nobody was at the keyboard to answer. It was blocked, and the assistant replied: *"The document was not added to the index because the action was not approved."*

### Limits

So the assistant can't get stuck or spend too much:

- at most **6 searches** and **10 AI calls** per question;
- at most **60 seconds** per request to Gemini, and **3 minutes** per question.

I added the time limits after a real problem. During the evaluation, one request to Gemini never got an answer, and the program waited for more than 35 minutes. Now it gives up, moves on, and tries that question again later.

### My extra guardrail: the citation check

**The idea.** The most dangerous mistake for my users is a **fake citation**: the assistant says *"page 72 says you get travel money"*, and the student trusts it because it looks official. So after every answer, my code checks each citation: **did the search really return this page or section?**

- If yes, the answer is shown normally.
- If not, the answer is still shown, but with a warning:

```
⚠️ Citation check: this answer may not be reliable.
  - (Programme Guide 2026, pp. 71-72): p. 72 was not retrieved
Check these points in the original documents before relying on them.
```

It also warns when an answer gives facts and numbers but cites **nothing at all**.

**False alarms I had to fix.** The first version of the check made mistakes in 3 of the first 10 answers, even though those answers were correct:

1. The assistant wrote *(Programme Guide 2026, p. 54, **Note 67**)*. My code thought "67" was a **page** number, but it's a footnote number.
2. The assistant put two sources in one bracket: *(Programme Guide 2026, p. 54**;** Learning Agreement guidelines, "...")*. My code thought both were from the Programme Guide.

I fixed both: numbers after "Note" are now ignored, and a bracket with ";" is split into separate citations. After the fix, those 3 answers no longer get a warning, and a test with an invented page (p. 99) is still caught.

This mattered to me, because a guardrail that gives too many false alarms is also bad: students would learn to ignore the warning.

**One case where it fired for real (q12).** I asked: *"How much individual support do I get per day on a short-term physical mobility?"*. The main answer was correct and well cited: 79 € per day up to day 14, then 56 € per day (p. 69–70). But at the end, the assistant added an extra point:

> *Travel support: You may also be eligible for a travel grant depending on the distance to your destination and whether you use sustainable means of transport (Programme Guide 2026, pp. 71-72).*

The search **never returned page 72**. The last page it saw was pp. 70–71, which is about **staff** mobility, not students. So the assistant cited a page it had never read, for a claim that wasn't in the passages it was given. The check caught it and added the warning, so a student would know to double-check that point before relying on it.

## Evaluation

I ran my assistant on all **36 questions** of my test set and checked the answers in three ways: with **code**, with an **AI judge**, and **by hand** (20 answers).

### 1. Code checks

Some things can be checked automatically, without an AI:

| Check | Result |
|---|---|
| Unanswerable questions where the assistant said "I don't know" | **6 of 6** |
| Answerable questions where it wrongly said "I don't know" | **0 of 30** |
| Answerable answers with at least one citation | **30 of 30** |
| Answers where my citation check found a citation that was never retrieved | **1** (q12, see Harness section) |

### 2. The AI judge

A second Gemini model reads each answer next to my reference answer and the passages the assistant found, and gives two grades:

- **correct (1/0):** does the answer give the key facts of my reference answer without contradicting them? For unanswerable questions: does it say it doesn't know, without inventing anything?
- **supported (1/0):** is **every** claim in the answer in the retrieved passages? If any claim is not there, it's 0, **even if it is true**.

**The judge's result: full marks for all 36 answers** (30 of 30 correct, 0 unsupported, 6 of 6 correct refusals).

### 3. My own grading, and how much I agree with the judge

I graded 20 answers myself (all 6 unanswerable, all 7 multi, and 7 single) **before** looking at the judge's grades.

| | My grades | Judge (same 20) | We agree |
|---|---|---|---|
| **correct** | 18 of 20 | 20 of 20 | **18 of 20 (90%)** |
| **supported** | 9 of 20 | 20 of 20 | **9 of 20 (45%)** |

**Why we disagree.** In **every** disagreement, I said 0 and the judge said 1. **The judge is too generous**:

- **m03:** *"I did 5 months, can I do a 9-month traineeship?"* The answer starts with *"Yes, you can potentially do a 9-month traineeship"* and only later says that just 7 months are left. I graded it wrong, because a student who reads only the first line gets the wrong answer. The judge only saw the correct part.
- **m04:** the 3-week programme question. The answer gives the daily rates but never says the total (1,498 €), which was the point of the question.
- **"supported":** many answers add things that are true but **not in the passages**, e.g. that SEPIE is Spain's National Agency, or *"contact the Agencia Tributaria"*. My rubric says that is 0. The judge ignored this rule every time.
- **q12:** my citation check caught a claim about travel support citing a page the assistant never saw, and the judge still graded it as supported.

**Two things that made the judge weaker:**
1. The main judge model was overloaded every time, so **all 36 grades came from the smaller backup model** (`gemini-3.1-flash-lite`), which is weaker than the assistant it grades.
2. It is from the **same family** (Gemini) as the assistant, so it may tend to accept its style of answer.

**A problem in my process (my own mistake).** The first time I graded, my grading sheet only showed the page names of the passages, not their text, because of a bug in my code that saved the passage text empty. The judge didn't see the text either. After fixing the bug, I re-ran the judge and **re-checked my "supported" grades with the real text**. That's why my agreement on "supported" went from 85% (without text) to 45% (with text): with the text in front of me, I saw many small claims that are not in the passages.

### Results

| | Result | Checked by |
|---|---|---|
| **Correct answers** | 30 of 30 according to the judge; **18 of 20** in my own grading | judge / me |
| **Unsupported answers** | 0 according to the judge; **11 of 20** in my own grading | judge / me |
| **Correct refusals** (unanswerable → "I don't know") | **6 of 6** | code |
| **Wrong refusals** (answerable → "I don't know") | **0 of 30** | code |

**What I conclude:** the assistant is good at **refusing** when it should (6 of 6) and **never refuses** when it shouldn't (0 of 30), and its main facts are usually right. But it often **adds extra claims** that are not in the passages, and sometimes puts a misleading sentence first. **An AI judge alone would have told me everything was perfect**: my own grading and my citation check are what showed the real problems.

## Failures

I grouped the problems I found by their cause. My counts come from my own grading of 20 answers, my citation check, and my retrieval test.

### Failures in the answers

| Cause | How many | Questions | Example |
|---|---|---|---|
| **1. My assistant adds advice or background facts that are not in the passages** | **8** | u01, u03, u04, u06, u07, m01, m02, m04 | *"SEPIE is Spain's National Agency"*, *"contact the Agencia Tributaria"*, *"each university sets its own criteria"* |
| **2. It concludes more than the passage says** | **2** | q03, q16 | q16 says students *"must keep paying tuition at their home university"*, which is not in the passages |
| **3. Its first sentence is misleading** | **1** | m03 | it starts with *"Yes, you can do a 9-month traineeship"*, then says only 7 months are left |
| **4. It doesn't finish the calculation** | **1** | m04 | it gives the daily rates, but not the total for 21 days (1,498 €) |
| **5. It cites a page it never saw** | **1** | q12 | travel support "(pp. 71-72)": my citation check caught it |

**The surprise in cause 1: my own rules caused most of it.** Rule 5 of my `AGENTS.md` tells the assistant: *"if the documents don't answer, tell the student where to ask: SEPIE or their university's international office"*. But my rule 3 says *"only say what the search results say"*. The documents don't say that SEPIE is Spain's National Agency, or that the international office handles selection. So **my two rules contradict each other**, and the assistant followed rule 5. The advice is true and helpful for a student, but by my own rubric it is "unsupported".

### Failures in the search

| Cause | How many | Questions |
|---|---|---|
| **6. The right passage is not in the first 5** (glossary: many definitions in one chunk) | **1** | q13 green travel |
| **7. Only one of the two passages is found** for a two-part question | **3** | m04, m05, m07 |
| **8. My assistant almost never searches twice** (1.06 searches per question on average), even though my rule 2 tells it to | all questions | — |
| **9. English questions don't reach Spanish documents** (see "Adding a document") | — | u01 with SEPIE |

Causes 7 and 8 are linked: if my assistant searched once per part of the question, it would probably find the second passage.

### What I would fix first

1. **Solve the conflict between my rules (cause 1, 8 answers).** For example, I would add a short official document about *where to ask* (SEPIE's role, the international office) to the corpus, so the advice becomes "supported"; or allow one fixed sentence of referral advice that doesn't count as a claim. This fixes the biggest group of failures with a small change.
2. **Make the first sentence match the conclusion, and finish calculations (causes 3 and 4).** I would add a rule: *"Start with the final answer to the question; if the question asks how much, give the total."* These are the most dangerous failures, because a student may only read the first line or skip the maths.
3. **Force a second search for two-part questions (causes 7 and 8).** My soft rule is ignored; my SEPIE test showed that a firm rule with an example works.
4. **Split the glossary into one chunk per definition (cause 6).**

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
