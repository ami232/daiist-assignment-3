# PostgreSQL backup and recovery decisions

**Author** Javier Sánchez Esquivel

**Student ID and group** Pending

## Use case

A data engineer needs to decide whether a proposed backup can recover the right part of a PostgreSQL installation. An application team might need one database back while other applications keep running. An incident commander might need to recover an entire cluster to a time before an operator error. Confusing these objectives can leave the team with a backup that cannot perform the required restore. A refusal sends the engineer to the manual or their own runbook. The assistant supplies evidence for a human decision.

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

The [evaluation set](eval/questions.csv) contains 18 single-passage questions, six two-passage questions and six unanswerable questions. Javier wrote q01 about choosing a recovery scope for one tenant or the whole cluster. Codex drafted q02–q30 and the reference answers, and Javier chose to use the recommendations. The brief calls for student-written questions. This set uses AI drafting for 29 of its 30 items.

Question q21 requires the backup-combination instructions and the verification guidance together. Question q26 asks how long a specific company’s last restore drill took, which a general PostgreSQL manual cannot establish. The set was recorded before the retrieval comparison. Some topics, including q14 and q30, were used in earlier implementation checks.

## Retrieval

The first design ranks passages by cosine similarity between normalized Gemini embeddings. The second combines this ranking with BM25 using reciprocal rank fusion. Exact tokens such as pg_verifybackup or a configuration parameter can complement a semantic match. Both designs use the same stored vectors.

The evaluator measures the proportion of answerable questions retrieving any required section and all required sections among the first one, three and five results. All required sections matter for a question combining two facts. Section-level matches can overstate useful evidence for a long section such as Options. The evaluator also records the actual number of passage words sent at five results. It selects by all-sections hit rate at five, then at three, then the simpler dense design. Scores and final selection await the student-authored set. The initial assistant uses dense retrieval.

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

Question q30 asked which lines the Manifest-Checksum covers and which algorithm it uses. On a copy of the base index the agent refused. After adding a held-out excerpt from PostgreSQL's backup manifest specification, it identified all preceding lines and SHA256 and cited the new passage PG-02f23d6d53ab0b. The initial addition created one vector. The repeated addition created zero. The production index still contains only the original documents. This demonstration used an AI-suggested question. [Recorded answers and traces](eval/addition_demo.json)

## Harness and guardrails

LangChain runs Gemini with [AGENTS.md](AGENTS.md) as its system prompt and connects to server.py over stdio. The harness requires a terminal confirmation showing the resolved path before an addition, bounds each run to five model calls and records the evidence supplied by search. Its citation guard converts an answer containing an unknown passage ID into the standard refusal. A controlled check using a fabricated identifier triggered that guard. Checking that a passage supports a particular claim still requires a reader or judge.

## Evaluation and decision

The evaluator checks refusals and citation membership in code. The Gemini judge uses the reference to assess correctness and the cited evidence to assess support. The blind packet presents answers, reference answers and passages for personal grading. The evaluator reuses the saved answers when calculating human agreement, so the human and the judge assess the same responses.

The full evaluation, failure counts, mean token usage and latency, and agreement with at least 20 personal grades are pending. The live verification question and document-addition experiment establish that these paths run. They provide too little evidence to recommend operational reliance on this assistant.

## AI use

Javier chose the PostgreSQL topic and supplied the first test question. Codex implemented the prototype, drafted the 29 additional questions Javier selected, and prepared the report. Gemini supplied embeddings and agent responses. GitHub Copilot ran the search-only subagent. Student grading remains outstanding.
