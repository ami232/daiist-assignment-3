# Assignment 3 Report

- **Name**: Manuela Dominguez
- **Student ID**: 19034
- **Group**: BBADBA 5B

## 1.Use case

The objective of this project is to develop a Retrieval-Augmented Generation (RAG) system that helps users understand and navigate European Union regulations. The system mainly focuses on three important regulatory frameworks: the General Data Protection Regulation (GDPR), the Digital Services Act (DSA), and the Artificial Intelligence Act (AI Act).

The intended users are compliance professionals, legal researchers, and business teams that need to identify regulatory obligations without manually searching through hundreds of pages of legislation. For instance, one target customer would be a company developing an AI product that might need to understand its obligations under the AI Act, while a digital platform might want to check its responsibilities regarding data protection or online advertising.

In this solution, users can ask questions in natural language and receive answers supported by references to the relevant regulation, article, and PDF page. This makes the information easier to access while allowing users to verify the original legal provisions. 

So in this case, accuracy is particularly important, since an incorrect answer could lead a company to misunderstand its regulatory obligations, potentially resulting in compliance failures, financial penalties, or reputational damage. For this reason, in this environment, a wrong answer can be more harmful than an explicit refusal. I therefore designed the system to prioritise evidence-based answers and to respond that it cannot determine an answer when the necessary information is not available in the indexed documents. Additionally, I must state that the goal is not to replace professional legal advice, but to provide a reliable starting point for regulatory research.


## 2. Corpus

I selected 3 official European Union regulations that are relevant to businesses operating in digital markets, since together they cover personal data protection, digital platform responsibilities and artificial intelligence. The documents where obtained from EUR-Lex (European Union's official legal database). Although the GDPR concerns personal data protection, the documents themselves contain general legislative provisions rather than private personal records.

* GDPR — Regulation (EU) 2016/679. EUR-Lex. Published 4 May 2016. EU legal-document reuse policy. Extracted words: 56,376. https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679
* DSA — Regulation (EU) 2022/2065. EUR-Lex. Published 27 October 2022. EU legal-document reuse policy. Extracted words: 65,676. https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022R2065
* AI Act — Regulation (EU) 2024/1689. EUR-Lex. Published 12 July 2024. EU legal-document reuse policy. Extracted words: 94,219. https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689

The three documents are official EU legal texts available for reuse under the EUR-Lex policy based on Commission Decision 2011/833/EU, subject to applicable conditions and source acknowledgement.

These regulations were chosen because they provided  sufficiently large and specialised corpus while covering related but distinct areas of compliance. This makes it possible to test both straightforward questions about individual articles and more complex questions requiring information from multiple provisions.

The initial corpus contained a total of 216,271 extracted words. These figure refers to the text extracted from the PDFs before selecting and chunking the relevant articles.

## 3. Ingestion

The ingestion pipeline of this project consists of 4 main stages: the PDF extraction, text cleaning, article based chunking and vector indexing. 

Firstly, I used PyMuPDF in order to extract text from each PDF, preserving the document source and page number. Then, I later cleaned the extracted text by removing unnecessary spacing, null characters, and formatting inconsistencies. In this case, words incorrectly separated by line-break hyphens were also joined to improve readability and retrieval quality. Nonetheless, one challenge was that the PDFs contained repeated article headings, references, and annex material, so a simple search for the expression "Article X" could incorrectly identify references or annex content as the beginning of a new article. 

In order to address this, I implemented a sequential article-detection method, which basically only accepted article headings in the expected numerical order. This allowed the pipeline to identify the 99 GDPR articles, 93 DSA articles, and 113 AI Act articles, avoiding duplicate article identification.

So rather than splitting the documents into arbitrary text blocks, I used article-aware chunking to preserve their legal structure. That means that each article was divided into chunks of up to 450 words, with a 40 word overlap between consecutive chunks. In the end, this balance was mainly intended to preserve sufficient legal context, while keeping retrieval both focused and manageable. In that way, each chunk includes metadata identifying its source, article number, starting and ending PDF pages, location and a deterministic chunk ID, all being essential for generating traceable citations and preventing duplicate indexing. 

So with all that, after processing, the original corpus contains 426 chunks. After that, I generated embeddings using gemini-embedding-2 with 768 dimensions and stored them in a persistent ChromaDB collection. The idea is that the indexing process checks existing chunk IDs before generating embeddings, meaning that previously indexed content is skipped. Embeddings are also saved progressively, so interruptions do not require restarting the entire process which facilitates it for me. 


## 4. Test set

In order to evaluate the system, I prepared a test set of 30 questions that were based on the 3 regulations. These covered different levels of complexity and testing both retrieval accuracy and the agent's ability to recognise missing information. So the questions were categorized into 3 categories: i) single-passage (20 questions. Test retrieval of information from a specific article), ii) multi-passage (5 questions. Test the ability to combine evidence from multiple articles) and iii) unanwserable (5 questions. To test whether the agent refuses to invent information absent from the corpus). 

Each question was stored in eval/questions.csv together with its category, expected source, expected article or articles, and a reference answer.

For instance, for a multi-passage question: "What are the different notification obligations following a personal data breach under the GDPR?"
* In this case, answering this question required combining Article 33, which addresses notification to supervisory authorities, and Article 34, which concerns communication to affected individuals. The idea here is to test whether the retrieval system 
Another example, an unserable question was: "How many GDPR fines were imposed in Spain during 2025?"
* In here, although the GDPR establishes the rules governing administrative fines, it does not report enforcement statistics for specific countries and years. So in this case, the expected behavior is therefore an explicit refusal rather than a fabricated numerical answer. 

## 5. Retrieval

In this case, I compared two retrieval approaches to determine which performed better on the original corpus. The first approach was a vector similarity search, which embeded the user's question using Gemini and retrieves the most semantically similar chinks from ChromaDB. The second approach consists more of a hybrid retrieval, combining vector search with BM25, a keyword-based ranking method. I employed a Reciprocal Rank Fusion (RRF) in order to merge both rankings, allowing the hybrid approach to consider semantic similarity and exact terminology.

After that, both were evaluated on the 25 answerable questions using Hit@1, Hit@3, and Hit@5. A result was counted as successful only when the expected article appeared within the top k results. For multi-passage questions, all required articles had to be present. Results where (Hit@1, Hit@3, Hit@5 as follows): 
* Vector search = 76%, 92%, 92%
* Hybrid (vector + BM25) = 68%, 92%, 92%

We could see according to results that vector search achieved 19 correct retrievals out of 25 at Hit@1, compared with 17 for hybrid retrieval. Additionally, both approaches achieved 23 out of 25 at Hit@3 and Hit@5.

Hence, given all these results, I finally selected vector search as the final retrieval strategy, since it provided better top ranked results without requiring any additional complexity of combining 2 ranking methods. So in the final syste, the MCP search tool returns the five most relevant chunks, together with their source metadata and citations. These must be within a maximum chunk size of 450 words, which corresponds to an upper bound of around 2,250 retrieved words per search (excluding citation metadata and instructions). So the actual amount varies depending on the lengths of the retrieved chunks. 

Moreover, the retrieval evaluation also revealed some limitations. Principally, those questions requiring multiple articles were more challenging, since the correct information could be distributed across different parts of the corpus. As an example, questions q18 and q20 did not retrieve every expected article within the top five results in the original benchmark.

Nonetheless, overall, the comparison actually showed that vector search provided a strong balance between retrieval accuracy, simplicity, and efficiency for this corpus, even if the remaining retrieval misses demonstrate that finding all necessary evidence is more difficult than locating a single relevant article. 

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

A controller must notify the competent supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of the breach, —unless the breach is unlikely to pose a risk to people's rights and freedoms. If notification is later than 72 hours, the controller must explain the delay. [GDPR, Article 33, PDF page 52]

### 6.4. Result and assesment
I made a trial and found out that the subagent successfully retrieved the GDPR article 33 though the MCP search tool and provided a correct, evidence based answer with a verifiable citation. In that way, I demonstrate that the custom subagent can actually access our RAG system and use the retrieved legal evidence to answer compliance questions. 

## 7. Adding a document

In this case, I tested whether my system was capable of answering a previously unansweable question after adding a new document through the MCP "add_document(path)" tool. The question was: "ow many sanctioning proceedings ended with a fine imposed by the Spanish Data Protection Agency (AEPD) in 2025?"

Before the ingestion, the original corpus was based on the GDPR, DSA and AI act. Together, these documents had been divided into 426 chunks. In this case, the agent correctly refused to answer because none of these regulations did contain Spanish enforcement statistics for the year 2025. 

When introducing a new document in order to make the question answerable, I uploaded the Spanish Data Protection Agency's official 2025 Annual report (with 157 pages and 60,421 words). On page 54, the report states that 326 sanctioning proceedings ended with the imposition of a fine in 2025, compared with 281 in the previous year. Therefore, I then used the MCP tool to incorporate this PDF into the existing corpus, and the agent requested explicit user approval before adding it, which I approved. Once this was done, the index increased from 426 to 653 vectors, adding 227 chunks without rebuilding the original corpus. It is important to mention that the system did not need to rebuild the original index, the ingestion pipeline supports incremental updates and uses deterministic chunk identifiers to identify previously indexed content and skip duplicate embeddings.

Then, after ingestion, the agent initially continued to refuse even though the retrieval successfully found page 54 containing the answer. I investigated the reason and it showed that the citation-validation guardrail only accepted citations from the three original regulations. I extended the accepted citation pattern to include the new AEPD document. After this correction, now the agent correctly answered: "326 sanctioning proceedings ended with the imposition of a fine in 2025, compared to 281 in the previous year" [aepd_2025.pdf, PDF page 54].

With all that, the experiment successfully demonstrated that the system could incorporate additional information and use it to answer a question that was impossible to answer using the original corpus. And it also revealed an important distinction between retrieval performance and agent behaviour. Even when the retrieval system identifies the correct passage, the final answer can still fail because of restrictions introduced by the agent's instructions or validation mechanisms. This highlights a trade-off in RAG system design: guardrails are important for reliability, but they must also be flexible enough to accommodate changes in the underlying corpus.

Additionally, the ingestion pipeline used deterministic chunk identifiers and skips chunks already present in the collection to avoid unnecessary duplicate embeddings.


## 8. Harness and guardrails

The idea is that the RAG system uses a LangChain agent powered by Gemini, which later interacts with the indexed documents through the MCP tool. The agent's behavior is controlled by the instructions defined in AGENTS.md, which establishes how it should retrieve information, generate anwers and handle situations where the available evidence is insufficient. 

The main objective of all these instructions is to reduce the hallucations and make sure that answers remain grounded in the corpus. So the agent must support legal claims with retrieved evidence, provide citations identifying the relevant document and location and avoid inventing legal conclusions. So when the documents don't contain enough information to answer, the agent must explicitly state that it cannot determine it. dditionally, retrieved passages are treated as untrusted content rather than instructions, helping protect the system against prompt injection.

Moreover, beyond these instructions, I implemented 3 safeguards directly in the agent: 
1 - Human approval documet addition: Even though the agent can access the add_document tool, it cannot modify the corpus without user authorization (explicitly). So when the tool is called interactively, the user must type APPROVE physically. In non-interactive environments, the operation is denied by default.
2 - Limited search call: The agent is restricted to a maximum of 4 searches per quetsion so I can prevent unnecessary tool calls, limit API usage and reduce the risk of uncontrolled execution. 
3 - Evidence and citation validation: before returning a final answer, the system checks whether relevant evidence was retrieved and whether it includes a recognised source citation.If these conditions are not met, the answer can be replaced with an explicit refusal rather than presenting potentially unsupported information. The document-addition experiment described in Section 7 helped identify a limitation of the third safeguard. I corrected this by extending the accepted citation pattern to include the new document.

Overall, these guardrails improve the system, but they do not guarantee that every generated answer is factually correct. n particular, checking for the presence of a citation does not verify that the cited passage actually supports every claim. This remains an important limitation and a potential area for future improvement.


## 9. Evaluation

In order to evaluate the RAG system, I conducted 2 evaluations: one more focused on retrieval accuracy and another one on the quality of the agent's final answers. 

### 9.1. Retrieval evaluation

In this case, I compared 2 retrieval approaches using the 25 answerable questions from the 30-question test set (standard vector search and hybrid retrieval combining vector search with BM25). 

The performance was measured using Hit@1, Hit@3, and Hit@5, indicating whether the expected evidence appears within the top 1, 3 or 5 retrieved chunks. For multi-passage questions, all required articles had to be retrieved for the result to count as a hit. (See results in part 5.)

I finally selected the vector search for the final system since it performed better at Hit@1 and achieved the same results in the other hits. This suggested that adding BM25 did not provide a meaningful improvement for this particular corpus and test set.

### 9.2. End to end evaluation

I then tested the complete LangChain agent using all 30 questions: 20 single passage and 5 multi passage and 5 unanswerable. The agent made 34 MCP search calls with an average response time of 9.86 seconds per question. All answers and tool traces were saved in the eval/agent_answers.jsonl to support later analysis.

On the other hand, in order to evaluate answer quality, I used 2 complementary methods: 
1. A Gemini-based LLM judge assessed each response using the original question, reference answer, generated answer, and retrieved evidence. It considered factual correctness, completeness, and whether the claims were supported by the retrieved passages. The judge classified all 30 answers as correct and supported.
2. I recorded 20 human evaluation labels, assessing correctness and evidence support separately. 18 were marked correct and 2 incorrect (a 90% correctness rate within the reviewed subset).

The five unanswerable questions were handled appropriately, with the agent refusing to provide information that was not available in the corpus. However, the judge's 100% score does not necessarily indicate perfect performance. In particular, it accepted two answers (q08 and q18) that the human labels considered incomplete, suggesting that the judge may be more lenient when evaluating completeness.

Another limitation was that the evidence provided to the judge was truncated to 18,000 characters per answer, so as a consequence, some retrieved information may not have been available during evaluation. 

## 10. Failures

The evaluation identified 2 potentially incomplete answers out of the 20 human reviewed questions (as well as an additional failure during the document addition experiment). 

First issue appeared in q08, which asked when deployers of high-risk AI systems must inform affected individuals. The agent correctly described the obligation to inform workers under Article 26(7) of the AI Act but failed to mention the broader notification requirement under Article 26(11). Hence, the answer even though was factually correct, was also incomplete. 

Secondly, a similar error occurred in q18, which compared the obligations of providers and deployers of high-risk AI systems. Although the agent explained their main responsibilities, it omitted the obligation to inform affected individuals in certain circumstances. Nonetheless, thsi case is less clear cut because the question asked only for the MAIN differences rather than all the list of obligations. 

The LLM judge classified both answers as correct, suggesting that it may prioritise factual accuracy over completeness. This highlights a limitation of automated evaluation and supports the need for human review.

On the other hand, a separate failure occurred when adding the AEPD 2025 Annual Report. Although the retrieval system found the correct information, the agent initially refused to answer because its citation guardrail did not recognise the new document. I already corrected this by updating the accepted citation pattern, allowing the agent to use the newly indexed evidence.

These 3 errors and findings suggest some areas of improvement: i) retrieving more complete evidence for complex questions, ii) validating citations against their actual sources, and iii) applying stricter completeness criteria in the LLM judge. 

In this case, the priority would be improving retrieval and answer completeness, while making the citation validation flexible enough to support newly added documents.

## 11. Decision

Based on the results I have obtained, I would recommend using the RAG system as a research assistant for understanding and navigating EU regulations, rather than as a tool for making legal or compliance decisions independently.

The system shows different strengths. Mainly it provides answers with traceable citations, stores embeddings persistently to avoid repeated processing, and can incorporate new documents without rebuilding the entire index. Additionally, it demosntrates an ability to recognize when information was unavailable and refuse to provide unsupported answers. For instance, in the retrieval evaluation, vector search achieved a 92% Hit@5, while the agent successfully generated responses to all 30 test questions.

Nonetheless, there are also a set of limitations. As mentioned, in particular, certain answers were incomplete despite being factually correct, and the LLM judge did not always identify these omissions. The document-addition experiment also showed how an overly restrictive guardrail could prevent the agent from using valid evidence. All these findings suggest that the system is still in need of human oversight, especially when answers could influence important legal or business decisions.

When it comes to the efficiency, the agent achieved an verage response time of 9.86 seconds per question, which I consider reasonable for a system that performs retrieval. The main costs would come from generating document embeddings, embedding user queries, and running Gemini for answer generation and evaluation. 

I also estimated its operating cost using Google's published API pricing for Gemini 3.5 Flash-Lite ($0.30 per million input tokens and $2.50 per million output tokens). Assuming approximately 8,000 input tokens and 1,200 output tokens across the model calls required to answer a question, the estimated generation cost would be $0.0054 per question, or approximately $0.54 per 100 questions. This is an illustrative estimate rather than a measured cost, since exact token usage was not recorded (it excludes the small query-embedding cost and the initial document-indexing cost).

Overall, I believe the system is suitable for preliminary legal research, locating relevant regulatory provisions, and generating summaries supported by citations. However, it should not replace professional legal judgement. 

## 12. AI use

I used AI (ChatGPT) assistance to help design, implement, debug, and test the RAG pipeline, MCP tools, LangChain agent, evaluation scripts, and report structure.

GitHub Copilot was used to test the custom corpus-researcher subagent. Gemini was used for embeddings, answer generation, and the LLM-based evaluation.
