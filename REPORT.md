# PostgreSQL backup and recovery decisions

**Author** Javier Sánchez Esquivel

**Student ID** 19731

**Group** BBADBA 5B

## Use case

I chose PostgreSQL backup and recovery because the word “restore” can mean two very different things. An application team may need one tenant’s data back while other customers keep working. After an operator error, the team may need the entire cluster as it stood a few minutes earlier. A wrong recommendation could leave the engineer with a backup that cannot perform the recovery. When the documentation gives too little evidence, a refusal costs the engineer a manual lookup.

## Corpus

The corpus uses the PostgreSQL 17.12 release dated 12 November 2026. It contains 12 selections from 11 distinct technical documents. Two selections cover different parts of the server configuration chapter. The table counts whitespace-delimited words once, before passage overlap. Source links point to the pinned edition. The PostgreSQL License permits redistribution of this documentation with its notice. The project includes the full notice in [POSTGRESQL-LICENSE.txt](POSTGRESQL-LICENSE.txt). [Release archive](https://ftp.postgresql.org/pub/source/v17.12/)

| Document or selection | Words | Indexed passages |
| --- | ---: | ---: |
| [Backup and Restore](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/backup.sgml) | 9,229 | 53 |
| [High Availability and Replication](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/high-availability.sgml) | 11,129 | 66 |
| [Reliability and the Write-Ahead Log](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/wal.sgml) | 5,798 | 31 |
| [Server configuration, WAL](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/config.sgml#L2949) | 5,920 | 32 |
| [Server configuration, replication](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/config.sgml#L4435) | 4,187 | 23 |
| [pg_dump](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/ref/pg_dump.sgml) | 6,356 | 35 |
| [pg_dumpall](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/ref/pg_dumpall.sgml) | 2,636 | 17 |
| [pg_restore](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/ref/pg_restore.sgml) | 3,558 | 21 |
| [pg_basebackup](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/ref/pg_basebackup.sgml) | 4,062 | 23 |
| [pg_combinebackup](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/ref/pg_combinebackup.sgml) | 954 | 7 |
| [pg_receivewal](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/ref/pg_receivewal.sgml) | 1,552 | 12 |
| [pg_verifybackup](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/ref/pg_verifybackup.sgml) | 1,020 | 7 |
| **Total** | **56,401** | **327** |

## Ingestion

The index builder verifies the SHA-256 digest of the official release archive and extracts the selected DocBook sections. It removes navigation metadata and indexing terms. An empty cross-reference element can carry the only mention of a tool in a sentence. Extraction restores names such as pg_dumpall from those elements. A parent section ends before its child section is indexed, avoiding double counting.

Each passage remains inside one of 109 source sections. A window contains up to 240 words with a 35-word overlap. The database records its source, section, pinned source link, passage ID and 768-dimensional Gemini embedding. A partial run saves each completed batch of vectors. A document becomes searchable after its full set of passages has been saved. Running the index command again on the same sources created zero new embeddings.

## Test set

I started with a question about one tenant. If an application team wants its own data back, does the tenant have a separate database, or does it share one with other customers? That distinction matters before an engineer can choose a restore procedure. My [final evaluation set](eval/questions.csv) contains 18 single-passage questions, six that require two passages and six the base corpus cannot answer.

Question q21 requires the backup-combination instructions and the verification guidance together. Question q26 asks how long a specific company’s last restore drill took, which a general PostgreSQL manual cannot establish. The set was recorded before the retrieval comparison. Some topics, including q14 and q30, were used in earlier implementation checks.

## Retrieval

The first design ranks passages by cosine similarity between normalized Gemini embeddings. The second combines this ranking with BM25 using reciprocal rank fusion. Exact tokens such as pg_verifybackup or a configuration parameter can complement a semantic match. Both designs use the same stored vectors.

The evaluator measures the proportion of answerable questions retrieving any required section and all required sections among the first one, three and five results. All required sections matter for a question combining two facts. Section-level matches can overstate useful evidence for a long section such as Options. The evaluator also records the actual number of passage words sent at five results. It selects by all-sections hit rate at five, then at three, then the simpler dense design. The comparison used the frozen question set in local commit `4c69bac`. The predeclared rule selected hybrid retrieval.

| Retrieval design | All sections at 1 | All at 3 | All at 5 | Any at 1 | Any at 3 | Any at 5 | Mean passage words at 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dense | 9/24 | 14/24 | 18/24 | 11/24 | 20/24 | 21/24 | 1,004 |
| Dense + BM25 | 8/24 | 14/24 | 23/24 | 12/24 | 20/24 | 23/24 | 1,075 |

At five passages, hybrid retrieval found both designated sections for all six two-passage questions. Dense retrieval did so for three. Hybrid also found the designated section for 17 of 18 single-passage questions, compared with 15 for dense retrieval. This improvement used about 72 additional passage words per search. Both methods missed at least one required section on every two-passage question at three results. The search depth matters for this use case. [Per-question retrieval results](eval/retrieval.json)

These 24 answerable questions target 13 of the corpus's 109 sections. The same questions selected the retrieval design, so these figures describe performance on the development set. An agent can reformulate a question or search more than once during answer generation.

## Tools and subagent

The search tool returned passage PG-94f95c911627cd from the Description section of pg_verifybackup for a question about test restores. The passage explains which integrity checks the tool performs and why the operator should also restore the backup and inspect the result. [Manual section](https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/ref/pg_verifybackup.sgml#L30)

The [corpus-researcher profile](.claude/agents/corpus-researcher.md) grants search access. The following excerpt comes from a GitHub Copilot CLI session on 24 November 2026. The parent delegated the research to corpus-researcher.

> **Prompt** Does pg_verifybackup replace a test restore?
>
> **Subagent tool call** corpus-search, with the query “pg_verifybackup replace test restore verification backup files archive restore distinction”
>
> **Subagent answer, excerpt** “pg_verifybackup does not replace a test restore; it does not perform every check a running server would perform”
>
> **Passage supplied** PG-94f95c911627cd, pg_verifybackup, Description.

## Adding a document

The MCP add_document tool imports the same chunking, embedding and storage pipeline. An unchanged document is skipped. A changed additional document with the same source name atomically replaces its old passages. Names belonging to the pinned corpus are protected.

Question q30 asked which lines the Manifest-Checksum covers and which algorithm it uses. Using the selected hybrid retrieval design on a copy of the base index, the agent refused. After adding a held-out excerpt from PostgreSQL's backup manifest specification, it identified all preceding lines and SHA256 and cited the new passage PG-02f23d6d53ab0b. The initial addition created one vector. The repeated addition created zero. The production index still contains only the original documents. This question and held-out excerpt had already been used in a setup check, so the demonstration illustrates ingestion rather than independent generalization. [Recorded answers and traces](eval/addition_demo.json)

## Harness and guardrails

LangChain runs Gemini with [AGENTS.md](AGENTS.md) as its system prompt and connects to server.py over stdio. The harness requires a terminal confirmation showing the resolved path before an addition, bounds each run to five model calls and records the evidence supplied by search. In the original run, the citation guard rejected four answerable responses that grouped valid IDs inside one pair of brackets. It could also overlook an unknown ID in a group if the answer had a separate valid citation. The revised guard checks every comma-separated member against the passages returned for that question. The same parser supplies the command-line source list and the evaluator's citation checks. Whether the passage supports the claim still needs a reader or judge. [Citation regression tests](test_citations.py)

## End-to-end evaluation

The evaluator checks refusals and passage IDs in code. A separate Gemini call judges correctness against the reference answer and support against the cited passages. The results below describe the original run. My 20 accepted grades apply exclusively to those saved responses.

The Gemini judge rated 25 of 30 answers correct (83.3%). The agent answered 20 questions substantively and refused 10. Of the refusals, six were appropriate and four were on answerable questions. Checking every passage ID in the 20 substantive answers, including IDs appearing in groups, found that all occurred in the respective search traces. [Saved answers](eval/answers.json) · [Evaluation summary](eval/summary.json)

| Question type | Questions | Judge rated correct | Agent refused |
| --- | ---: | ---: | ---: |
| Single passage | 18 | 15 | 3 |
| Two passages | 6 | 4 | 1 |
| Unanswerable | 6 | 6 | 6 |
| **Total** | **30** | **25** | **10** |

The judge rated 27 of 30 answers supported. All three support failures were bare refusals. The rubric gives a bare refusal support credit because it makes no factual claim. The judge applied that rule inconsistently. On q21 it marked the answer supported while its explanation pointed to missing evidence for the rehearsal recommendation. The agent and judge also used the same model, Gemini 3.5 Flash-Lite. The [review packet](eval/blind_review.md) contains the questions, responses, references and retrieved passages.

### Agreement on the 20 graded answers

I finalized the grades for 20 original answers by accepting the scores and reasons in the grading worksheet. The sample covered 12 single-passage, four two-passage and four unanswerable questions. Codex proposed those scores after the automated verdicts were available, which limits what the agreement figures can establish about independent human judgment. [Final labels and reasons](eval/human_labels.csv)

| Measure | Final grades awarding credit | Final grade matched the judge |
| --- | ---: | ---: |
| Correctness | 15 of 20 | 18 of 20 (90%) |
| Support from cited passages | 14 of 20 | 12 of 20 (60%) |

The two correctness disagreements involved explanations that gave the right recovery decision but added a factual error. In q12, the response said an incremental backup contains only changed blocks, although some files are copied in full. In q22, it described logical dumps as text scripts, overlooking archive formats. Support was a separate issue. For example, q20 correctly identified the directory format for a parallel dump. The passage cited for that instruction omitted the specific jobs flag the answer recommended. The final grade therefore gave q20 credit for correctness only.

Mean agent usage was 3,801 input tokens and 145 output tokens per question. Mean latency was 8.90 seconds and median latency was 5.26 seconds. Timing covers answer generation and tool calls after opening the shared MCP session. The token counts exclude embeddings and separate judge calls. These measurements describe one run on this question set.

## Failure analysis

The automated classification counted two retrieval misses (q01 and q21) and three unsupported claims (q03, q05 and q07). It assigned zero cases to wrong refusal, wrong answer from the right passage, or bad test question. The classification checks support and retrieval coverage before checking for a wrong refusal. A trace review explains why four refusals on answerable questions produced those counts.

Four of the 24 answerable questions received the standard refusal. Grouped citations triggered the guard on q01, q03, q05 and q07. Replaying the revised parser on the four original raw responses accepted every cited ID. In q03 the agent had identified the correct parallel dump format before the guard discarded the answer. In q01 a tenant-recovery bullet still lacked a citation. Accepting the group resolves the formatting error but leaves that evidence gap.

On q21 the agent explained how to combine incrementals. Its live searches missed the verification manual that calls for a test restore and checking the recovered data. The answer added recovery steps and omitted the data check in the reference. In the fixed-query benchmark the original wording retrieved both expected sections. This discrepancy motivated using the full user question for the first search.

## Paired experiment on the same 30 questions

I kept the questions, references, index, hybrid top-five search, agent model, judge model and judge rubric fixed. The revised harness sends the exact user question to the MCP search tool before the first model call, supplies those passages to the model and allows focused follow-up searches. It also validates grouped citations. All 30 revised answers were generated afresh and graded by Gemini. My 20 accepted grades remain attached to the original answers at commit `fd3b870`. [Original responses](eval/answers.json) · [Revised responses and traces](eval/experiments/original-first/answers.json) · [Paired results by question](eval/experiments/original-first/comparison.csv)

| Measure | Original | Revised |
| --- | ---: | ---: |
| Judge rated correct | 25/30 (83.3%) | 29/30 (96.7%) |
| Judge rated supported | 27/30 (90.0%) | 30/30 (100%) |
| First search found all required sections, single-passage questions | 15/18 | 17/18 |
| First search found both required sections, two-passage questions | 0/6 | 6/6 |
| All searches together found the required sections, answerable questions | 18/24 | 23/24 |
| Refusals on answerable questions | 4/24 | 0/24 |
| Appropriate refusals on unanswerable questions | 6/6 | 6/6 |
| Substantive answers whose cited IDs all appeared in the trace | 20/20 | 24/24 |

On q21 the first five results included both the combination and verification manuals. The revised answer specified the oldest-to-newest backup order and cited the verification manual for a test restore that checks the database contents. On q03 the revised answer gave the directory format for a parallel dump using two IDs in one bracket. Both IDs resolved, and the answer reached the user. [Revised traces for q03 and q21](eval/experiments/original-first/answers.json)

Five questions gained correctness credit (q01, q03, q05, q07 and q21), and one lost it (q23). The sole revised failure was a wrong answer from the right passage. The response accurately explained the disk-space risk from a disconnected replication client, but confused the default flush timing of `pg_receivewal` with the behavior of `--synchronous`. The original answer correctly identified file closure as the default flush point. The revised answer claimed immediate flushing even though its cited Options passage assigned that behavior to `--synchronous`. The judge flagged the factual error but still awarded support, so the 30/30 support score overstates the evidence. [Revised verdicts](eval/experiments/original-first/judge.json) · [Failure classification](eval/experiments/original-first/summary.json)

Two other cases show the limits of the metrics. On q02 the revised search missed the designated `pg_dump` section, but it found and cited the Backup and Restore chapter's explicit statement that a dump allows other database operations to continue. On q01 all cited IDs resolved and the judge awarded support, although the bullet about capturing global roles and permissions had no citation of its own.

Across 30 completed responses the number of searches went from 39 to 38. Mean input/output tokens went from 3,801/145 to 3,675/131. Median latency fell from 5.26 to 1.99 seconds, and mean latency from 8.90 to 7.72 seconds. The slowest revised response took 67.08 seconds. One interrupted attempt at q10 was restarted from the last checkpoint after roughly 153 seconds. Its elapsed time is outside the completed-response figures. The runs used a local query-embedding cache. Timing varies with API availability, and token totals exclude embeddings and judging.

## Decision

I would use the revised assistant to find manual sections during a recovery rehearsal. The complete first query retrieved both sections on all six two-passage questions, and the revised guard let correctly formatted evidence reach the user. For a production recovery decision, I would verify the cited instructions and rehearse the procedure in an isolated restore. The q23 error shows how a plausible statement about flush timing can be wrong even when the correct passage is on screen. Both changes ran together on questions already used to diagnose the baseline, and the same model generated and judged the answers. The 29/30 result measures the combined change on this set. Performance on fresh scenarios and the contribution of each change to correctness remain open.

## AI use

I chose PostgreSQL backup and recovery, wrote the opening tenant-recovery question and selected the 30 questions used in both runs. I used Codex to brainstorm recovery scenarios and draft the remaining questions and reference answers. Codex also helped with the code by implementing the prototype and testing the citation guard, and helped draft this report. I made the final grading decision on the 20 original answers by accepting the scores Codex proposed. Gemini generated the embeddings, answered the questions and supplied the automated verdicts. GitHub Copilot ran the search-only subagent.
