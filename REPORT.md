# Assignment 3 Report

- **Name**: Manuela Dominguez
- **Student ID**: 19034
- **Group**: BBADBA 5B

## 1.Use case

*Who asks, what they do with the answer, and what a wrong answer costs compared with "I don't know".*

## 2. Corpus

*Table: document, URL, date, licence, words.*

## 3. Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

## 4. Test set

*How you wrote it, counts by kind, two examples.*

## 5. Retrieval

*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

## 6. Tools and subagent

### 6.1. MCP Tools
The MCP server exposes 3 main tools: 
1. Search (query): which retrieves the five most relevant passages from the indexed GDPR, AI Act and DSA regulations. This returns additionally their source, the article, the PDF page and the chunk ID. 
2. add_document (path): in charge of extracting, chunking, and storing an additional PDF in ChromaDB. In here, already indexed chunks are skipped in order to prevent any duplicate embeddings. 

### 6.2. Subagent configuration
I configured a specialized subagent called "corpus researcher" in ".claude/agents/corpus-researcher.md". So the idea is that the agent is restricted to the "mcp__corpus__search" tool, and in its instructions they require evidence based answers, citations for factual legal claims and explicit refusals when the available documents do not contain enough information.

### 6.3. Copilot Subagent Transcript

**Environment:** GitHub Copilot in VS Code (GitHub Codespaces)

**Tool used:** `mcp__corpus__search` (confirmed in Copilot)

**User:**

What is the deadline for notifying a personal data breach under the GDPR? Use the corpus search tool and cite the relevant article.

**Subagent:**

A controller must notify the competent supervisory authority **without undue delay and, where feasible, within 72 hours of becoming aware of the breach**—unless the breach is unlikely to pose a risk to people's rights and freedoms. If notification is later than 72 hours, the controller must explain the delay. [GDPR, Article 33, PDF page 52]

### 6.4. Result and assesment
I made a trial and found out that the subagent successfully retrieved the GDPR article 33 though the MCP search tool and provided a correct, evidence based answer with a verifiable citation. In that way, I demonstrate that the custom subagent can actually access our RAG system and use the retrieved legal evidence to answer compliance questions. 

## 7. Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## 8. Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

## 9. Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## 10. Failures

*Failed questions by cause, with counts, and what to fix first.*

## 11. Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## 12. AI use

*What you used and how, or "none".*
