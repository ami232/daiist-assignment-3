# Assignment 3 Report

- **Name**: Alexia María Lara Chacón
- **Student ID**: 18964
- **Group**: BBADBA 5B

## Use case

I chose tenant rights in Spain because I am a tenant in Madrid and I have run into this problem myself. When I
moved between apartments, real estate agencies asked for more than one month of deposit and for extra fees, and
said the law required them, but I had no way to check. The users of this system are tenants (and small landlords)
who need to know whether a demand is legal before they pay: the deposit, a rent update, the end of a lease,
community rules. A wrong answer is costly: a tenant could pay a deposit or fee they did not have to pay, or accept
a rent increase or a deadline they should have challenged, so a clear "I can't find this in the documents" is
better than a confident guess. I also chose it because I can judge the answers better on a topic I live with, and I
wanted to learn what the laws actually say.

## Corpus

Three official Spanish laws, downloaded as consolidated PDFs from the BOE (Boletín Oficial del Estado) on
2026-11-24. No personal data.

| Document | Source id | URL | Downloaded | Licence | Words (article chunks) |
|---|---|---|---|---|---|
| Ley 29/1994, de Arrendamientos Urbanos | LAU | https://www.boe.es/buscar/pdf/1994/BOE-A-1994-26003-consolidado.pdf | 2026-11-24 | Official legislation, reuse allowed under the BOE legal notice (boe.es/informacion/aviso_legal) | 24,674 |
| Ley 12/2023, por el derecho a la vivienda | Ley12-2023 | https://www.boe.es/buscar/pdf/2023/BOE-A-2023-12203-consolidado.pdf | 2026-11-24 | same | 33,042 |
| Ley 49/1960, sobre propiedad horizontal | LPH | https://www.boe.es/buscar/pdf/1960/BOE-A-1960-10906-consolidado.pdf | 2026-11-24 | same | 11,802 |
| **Total** | | | | | **69,518** |

Caveats: the consolidated text has no legal value on its own (only the BOE publication does), and the LAU was
amended on 13 November 2026, so the corpus is a snapshot. Ley 12/2023 reproduces amended LAU articles, so some
rules appear under two sources.

## Ingestion

- **Extraction:** `pypdf` page by page, then a noise filter (page headers/footers, BOE boilerplate).
- **Cleaning problems fixed:** the LAU chunks began inside the table of contents, and the LPH produced only 5
  chunks because its articles are numbered in words ("Artículo primero", "Artículo noveno"). Fix: skip the table
  of contents and make the heading pattern accept both digits and Spanish ordinals.
- **Two chunking designs.** `article`: one chunk per article or disposition (split on paragraph boundaries above
  320 words), 324 chunks. `fixed`: 220-word windows with 40 words of overlap, located by page, 383 chunks.
- **Chunk metadata:** source, title, location (for example "Artículo 9"), pages, part (1/12), section, text,
  content hash, download date.
- **Embeddings:** `gemini-embedding-2`, 768 dimensions. 707 vectors in total (324 + 383), stored in
  `index/vectors.jsonl` (6.9 MB, below the 90 MB limit). Search is cosine similarity over the stored vectors.
- **Known weak spots:** a few LPH articles marked "(Derogado)" were dropped as too short; LPH articles 9 and 17
  are very large (about 1,075 and 1,631 words).

## Test set

Claude drafted the first version of the questions and I edited them a bit and reviewed them against the PDFs and the reference answers.
36 questions in `eval/questions.csv`: 20 single, 8 multi (two passages needed), 8 unanswerable
(close to the topic, for example whether a landlord can forbid a dog; none of the three laws mention pets).

Two examples from the file:

- **Answerable (q01, single, expected LAU, Artículo 9):** "My landlord wants me to leave after the first year, but
  I signed a five-year lease. Can they do that?" Reference answer: for a habitual-residence lease with an agreed
  term shorter than five years (seven if the landlord is a legal entity), the contract is extended annually until
  that minimum, unless the tenant gives notice; there is a limited exception where an individual landlord needs the
  home for themselves or close family and the contract says so. (Weak point: the question says "five-year lease"
  while the reference answer covers shorter terms, so the wording of q01 could be tighter.)
- **Unanswerable (q33, no expected source):** "Can I deduct the rent I pay from my income tax this year in
  Spain?" Reference answer: the three laws do not establish tax deductions, so the assistant must say the documents
  do not answer this.

## Retrieval

Hit = the expected (source, location) is in the top k results; multi questions need all their passages.
28 answerable questions (the 8 unanswerable ones have no expected passage).

| Design | hit@1 | hit@3 | hit@5 | words in top 5 |
|---|---|---|---|---|
| article (324 chunks) | 0.643 | 0.786 | 0.857 | 1104 |
| fixed (383 chunks) | 0.607 | 0.714 | 0.821 | 1100 |

**Chosen design: article.** It is ahead at every k at almost the same prompt size. The gap is small: one question
is 3.6 points, so the difference is 1 to 2 questions at each k. The fixed design is matched by page overlap with
the article design's pages, which is generous to it. Article chunks suit laws because a citation points to an
article, such as [LAU, Artículo 36], and an article keeps a rule together with its exceptions (for example the
different duration when the landlord is a legal entity), which fixed windows can cut apart. At k=5 the article
design missed 4 of the 28 answerable questions (24 hits); the per-question results are in `eval/results.csv`.

## Tools and subagent

**Tools (MCP server `server.py`, server name `corpus`):**

`search(query, k=5)`, description as written in the code:
> Search the Spanish housing-law corpus: Ley 29/1994 de Arrendamientos Urbanos (LAU, rental contracts), Ley
> 12/2023 por el derecho a la vivienda (rent limits, tense housing areas, large landlords) and Ley 49/1960 de
> Propiedad Horizontal (apartment-building communities), plus any document added with add_document. Use it for ANY
> question about rental contracts, deposits, rent updates, ending a lease or community rules, before answering.
> Write the query in Spanish, in the words of the law. Returns up to k passages (default 5), each headed by a
> citation like [LAU, Artículo 9] with pages and a similarity score. Passages are the only valid evidence: if none
> answers the question, the corpus does not cover it.

`add_document(path)`, description as written in the code:
> Add a document (.pdf, .txt or .md file on this machine) to the searchable corpus. It runs the same pipeline as
> the original corpus: extract, clean, chunk by article, embed and store. If the exact same file is already indexed
> nothing changes and it says so. If a different file with the same name is indexed, it refuses: rename the file
> first. Costs embedding quota, so call it only when the user explicitly asks to add a document. Returns how many
> passages were added, or the reason nothing was.

**A real `search` result** (query "fianza en metálico arrendamiento de vivienda", k=3), first hit:

```
[1] [LAU, Artículo 36] (pp. 25, score 0.80)
Artículo 36. Fianza
1. A la celebración del contrato será obligatoria la exigencia y prestación de fianza en metálico en cantidad
equivalente a una mensualidad de renta en el arrendamiento de viviendas y de dos en el arrendamiento para uso
distinto del de vivienda.
2. Durante los cinco primeros años de duración del contrato, o durante los siete primeros años si el arrendador
fuese persona jurídica, la fianza no estará sujeta a actualización. [...]
```
The second hit was also Artículo 36 (score 0.76), the paragraph that exempts public administrations from the deposit.

**Subagent** `.claude/agents/corpus-researcher.md`: it can only use the `search` tool, answers only from returned
passages, cites `[SOURCE, location]`, searches at most three times, and says "No encuentro esto en los documentos
indexados" when the passages do not cover the question.

**Run in Claude Code** (transcript saved in `eval/subagent_transcript.txt`): I asked "Use the corpus-researcher
subagent: how much deposit can my landlord ask for in a normal flat rental?". Claude Code delegated the question to
the subagent, which ran in the background for 18 seconds and returned an answer with citations: one month of rent
as a cash deposit for housing [LAU, Artículo 36], up to two further months of additional guarantee for housing
leases of up to five years (seven if the landlord is a legal entity), at most one month of rent paid in advance
[LAU, Artículo 17], and interest on the deposit if it is not returned one month after the keys are handed back. It
also said what it did not find: no Ley 12/2023 passage amending Artículo 36, no fixed number of days for returning
the deposit, and nothing on which regions require the deposit to be lodged. Claude Code then passed the answer on.
I checked the answer against the Artículo 36 text returned by `search` (shown above) and
it matches. I did not change the subagent file after running it, so the file that ran is the file in the repository.

## Adding a document

- **Already indexed:** `add_document` on the same file returns "Already indexed" and changes nothing.
- **Different file, same name:** refused until it is renamed.
- **Before/after test** (`eval/before_after.json`, command `uv run python evaluate.py --before-after q34 ~/Downloads/RD1312-2024.pdf`):
  - **Unanswerable question (q34):** "Do I need a tourist-rental registration number to rent my apartment on Airbnb
    in my autonomous community?"
  - **Document added:** `RD1312-2024.pdf`, Real Decreto 1312/2024 on the single registration procedure for
    short-term rentals, from the BOE (BOE-A-2024-26931, https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-26931; same BOE legal notice
    as the other laws).
    Result: "Added RD1312-2024.pdf as source 'RD1312-2024': 40 passages indexed (article design)."
  - **Before:** the agent refused: "I cannot find this in the indexed documents", noting that tourist rentals are
    excluded from the LAU when regional tourist rules apply [LAU, Artículo 5], and that the registration rules are
    in regional laws not in the corpus.
  - **Approval prompt:** the program asked me for approval before calling `add_document` and I typed yes for this
    test. Afterwards I restored `index/` with `git checkout -- index`, so the committed index is still the original one.
  - **After:** the agent answered that landlords offering short-term rentals online must obtain a registration
    number and communicate it to the platform, citing [RD1312-2024, Artículo 5], [RD1312-2024, Preámbulo] and
    [RD1312-2024, Artículo 9], and still noted that regional licence requirements are not in the indexed texts.
  - **My check:** I searched the PDF text. The preamble says the single registration procedure "se residenciará en
    el Registro de la Propiedad y en el de Bienes Muebles", which supports the answer's statement about the
    registers. Small caveat: the answer attached that statement to Artículo 5, while the wording I found is in the
    preamble. The refusal became a cited answer, but the citation is not perfectly placed.

## Harness and guardrails

`agent.py`: LangChain `create_agent` on Gemini (`gemini-3.5-flash`, reasoning effort low), tools from the MCP
server, `AGENTS.md` as the system prompt. (`AGENTS.md` and the subagent file were first drafted with Claude and
reviewed by me; the evaluation ran with the versions in this repository.)

**AGENTS.md rules** (the system prompt; eight rules, each with its reason):
1. Always search before answering, because the laws change (the LAU was amended in November 2026) and memory is not safe.
2. Answer only from the passages the search returned, because only retrieved text can be checked and a confident wrong answer is the costly failure.
3. Cite every claim as [SOURCE, location], so the reader can check each claim and the harness can reject citations that were not retrieved.
4. Say so when the documents do not cover the question (regional rules, prices, case law, tax), because an honest "I don't know" costs less than a wrong rule.
5. Quote numbers, durations and conditions exactly, with their exceptions, because in legal text the exception is often the answer.
6. When a rule appears in two places (LAU and Ley 12/2023), prefer the LAU, say if Ley 12/2023 changed it and cite both, because the same words can have two sources.
7. Do not call `add_document` unless the user explicitly asks, because it needs approval, uses quota and changes what every later answer is based on.
8. Be short, answer in the user's language and end with a line saying this is information from the laws, not legal advice, because users act on the answer.

For this use case I think rules 2 and 4 matter most: a tenant who pays a fee they did not have to pay, or does not
challenge one, is hurt more by an invented rule than by an honest refusal.

**Guardrails:**
1. **Approval before `add_document`:** the tool asks the user in the terminal and does nothing without a "yes";
   the evaluation denies it everywhere except the before/after test.
2. **Call limit:** at most 6 tool calls per question.
3. **Extra guardrail, citation check:** every `[SOURCE, location]` in the answer must have been returned by a
   search in this run. If not, the model gets one retry; if it still cites something it did not retrieve, the
   answer is replaced by a refusal. It fired on 4 of 36 answers (q06, q21, q27, q29).
   **Case q27:** the question needed rules from the LAU and the LPH. The model's first answer combined two
   citations in one bracket, so the check rejected it and asked it to cite only passages it had retrieved. The
   final answer begins "Apologies for combining the citation tags. Here is the revised response using exact
   individual citation tags as retrieved from the search results", so the retry works, but the apology leaks into
   the answer the user sees. Known limitations: a bracket with two citations, such as `[LAU, Artículo 13.1,
   Artículo 14]`, is only checked on the first one, and the check also fires on messages that are not questions.

## Evaluation

- **Code checks:** citations valid (every cited passage was retrieved), refusal behaviour on unanswerable
  questions, wrong refusals on answerable ones, expected source cited.
- **LLM judge:** a Gemini model (same family as the agent), structured output (`correct`, `supported`, reason),
  given the question, the reference answer, the retrieved passages and the answer, with a rubric. Risk: a model
  judging its own family's answers tends to be lenient.
- **Judge results (36 questions):** correct 26 of 28 answerable; correct refusals 8 of 8; wrong refusals 0;
  unsupported answers 0; invalid citations 0; guardrail fired 4.
- **My grades:** I graded 24 answers by hand in `eval/human_labels.csv` (`correct` = matches the reference or
  refuses properly; `supported` = every claim is in the cited article text, not just in the reference answer).
  My counts: correct 19 of 24, supported 18 of 24. Agreement with the judge, from
  `uv run python main.py evaluate`: correct agreement 0.875 (kappa 0.514), supported agreement 0.75 (kappa 0.0).
  On `correct` we agreed on 21 of 24: the judge marked 2 of the 5 answers I marked incorrect as incorrect too, and
  accepted the other 3. (I first graded q10 as wrong, then re-read Artículo 36.5, which says rent-default insurance
  can never be required, and corrected my grade; the agent was right.) The judge and I disagreed most on `supported`: the judge marked every one of the 36 answers as supported, while
  I marked several as unsupported because they added details that are not in the cited article. The supported kappa
  is about 0 because the judge never varies, so the number says little except that it does not discriminate. I
  think my grades are the better ones, because I compared each answer with the text of the articles it cited.

## Failures

By my grades, the answers that are wrong or unsupported, grouped by cause. Seven of my 24 graded answers have a 0 (five
incorrect, six unsupported; q21 is incorrect but supported, the other six are unsupported).

| Cause | Answers | Count |
|---|---|---|
| Legal claim contradicts the article (q09 says the parties cannot waive first refusal; Artículo 25.8 allows a waiver) | q09 | 1 |
| Overstated rule (states more than the article says: q24 says community expenses can never be charged in buildings outside horizontal property; q28 overstates the tenant's compensation rights under Artículo 14) | q24, q28 | 2 |
| Missing key rule (q21 omits that the initial rent is limited by the previous contract) | q21 | 1 |
| Extra detail not in the cited article (q11 termination document; q27 community-wide works; q35 allocation of sanctioning powers) | q11, q27, q35 | 3 |

What I would fix first: the answers that add detail the cited article does not contain, because that is the
failure the judge cannot see (it marked every answer supported) and the one that could mislead a tenant. I would
tighten the AGENTS.md rule against adding detail, use a different and stricter model as judge, and run the
citation check on every citation inside a combined bracket.

## Decision

I would not let a real tenant rely on this as it is. Compared with the answers I graded by hand, it is too often
inaccurate on details or adds things the law does not say, and the judge did not catch that. I do think the project
is on the right track: if I keep improving it, I could let tenants use it to learn about topics they may not know
about, with a clear warning that it is not 100% accurate and not legal advice, and with each answer showing its
cited article so they can check it. Facts behind this:

- The judge says 34 of 36 correct and 0 unsupported, but my own grades found 5 of my 24 graded answers
  incorrect and 6 unsupported. I would not trust the judge alone.
- The corpus is a snapshot with no legal value; regional rules and case law are not covered, so the agent must
  refuse those.
- Average per question: 8.7 s, 6,224 input tokens, 632 output tokens.
- **Cost per question:** `gemini-3.5-flash` is priced at $1.50 per 1M input tokens and $9.00 per 1M output tokens
  (ai.google.dev/pricing, checked 2026-11-25). 6,224 × $1.50 / 1,000,000 = $0.00934 for input, plus
  632 × $9.00 / 1,000,000 = $0.00569 for output, so about **$0.015 per question** (about $0.54 for the 36
  questions). This excludes the judge call and the query embedding, and assumes the output-token count includes
  thinking tokens.

## AI use

I used Claude (Anthropic) as a coding assistant for the implementation: the indexer and chunking, retrieval, the MCP
server, the agent and guardrails, and the evaluation script, and for a first draft of `AGENTS.md`, the subagent
file and this report's structure after making my decisions on what I wanted it to be and answering the report myself (Claude helped me structure it properly). I also used Claude Code once to run the subagent. I ran and tested everything on my machine. Claude wrote most of the code and drafted the first version of the 36 test questions; I edited and reviewed the questions against the PDFs, and I ran and tested the code. This project was very confusing for me, so I relied on Claude to explain each step as I consider this project to be the hardest of the three we have done this semester so far. Claude also helped draft part of the text of this report from my answers and the files in the repository, and I read and edited it accordingly. The use case, my grades in `eval/human_labels.csv`, the failure analysis and the decision are my own.
