Attention: Students should complete this by the end of the semester.Please Note: This assignment is due at the end of the semester.

**Name:** Adam Baroudi  
**Student ID:** 19379  
**Group:** BBADBA 5A

## 1. Use Case

I chose to create a Retrieval-Augmented Generation (RAG) system and focus it on the topic of aviation safety. This system is primarily intended to facilitate the access of reliable information by official aviation documents to the trainee pilots, aviation safety officers and aircraft maintenance personnel.

Users can type queries and get answers back, along with information and citations from the documents—instead of having to scroll through hundreds of pages.

So I decided on aviation, because information can be dangerous in this field! An incorrect response to any of the aircraft maintenance, weight distribution or flight safety questions may be part of an unsafe decision.

So, to me, the "I don't know" system is much superior to giving an off-base answer with confidence. The system should focus on getting the answer right and be reliable, not necessarily cover all the questions.

## 2. Corpus

To use for my document collection, I used three documents that are freely available from the Federal Aviation Administration (FAA) that are handbooks.

The first one was the Pilot's Handbook of Aeronautical Knowledge, which had five hundred and twenty-two pages, and two hundred and seventy-two, nine hundred and thirty-one words. The second was the Aviation Maintenance Technician Handbook, which had 698 pages and 354,839 words. The third document was Aircraft Weight and Balance Handbook which was 114 pages and 39,290 words long.

The original document collection consisted of 1,334 pages and 667,060 words, well in excess of the minimum of 50,000 words.

Because of the free API restrictions of Gemini, however, I took the indexed corpus to about 60,000 words by filtering for relevant pages within all three documents. This facilitated the indexing process and ensured that the key aviation topics were covered.

The documents which were selected are those that contain educational and technical information about aviation safety, aircraft operations, aerodynamics, aircraft maintenance, and weight and balance.

In the USA, FAA government material tends to be in the public domain. But including verification of third-party copyrighted content and personal details on selected pages is still a problem.

## 3. Document Ingestion and Indexing

The system has been developed using Python and Google Colab. The project files are saved to Google Drive, so that any work would not be lost when the Colab session disconnected.

First, I downloaded the PDF files and then used PyMuPDF to recover the text. The extracted text was then cleaned by removing unnecessary white space, and split into small chunks of around 400 words with an overlap of 50 words.

The justification for why an overlap was used was that if it was broken down into two chunks, then there was a risk of losing key information in the explanation.

The chunks included the original document name and PDF page number which enabled the system to offer citations and verify the information presented by the user.

I have created embeddings of 768 dimensions and stored the vectors in ChromaDB using Gemini. SHA-256 was used to hash each chunk, giving it a unique id. This enabled the system to identify the already indexed chunks and prevent duplicate embeddings.

The corpus was split into 222 chunks in the three documents.

The most difficult part of the indexing process was Geminis API limitations. To address this, I tweaked the indexing process to create and store embeddings on an individual basis and added delays and retries between requests.

This made it possible to save the system's progress if an API call failed.

## 4. Evaluation Test Set

The evaluation dataset was comprised of 35 questions, including 21 single-passage, seven multi-passage and seven unanswerable questions.

Single pass questions asked for information which is located in one particular passage. Multi-passage questions involved using information from multiple pages or documents.

The system was tested to determine if it would be able to refuse to answer when there was not enough information to answer the question.

For instance, one of the answerable questions was on the four forces acting on an airplane, and an unanswerable question was about the current state of the runway at Madrid airport.

The questions were created using an AI tool and information from the original documents. For each of the answerable questions there was an expected, page number, reference answer.

A drawback of this is that a few corpus pages were chosen after the evaluation questions were developed. This may have positively influenced the retrieval results, meaning that the evaluation is not completely independent.

## 5. Retrieval Methods and Results

I implemented two different retrieval methods: semantic search and hybrid search. Semantic search retrieves information based on the meaning of a query, with the help of embeddings. Hybrid search - a combination of semantic similarity and keyword search. In my implementation, 70% of the retrieval score was due to semantic similarity and 30% was due to keyword matching.

I did the two tests with the 28 questions I could answer. For semantic search, the hit rate at k=1 was 35.71%, the hit rate at k=3 was 71.43%, and the hit rate at k=5 was 78.57%. For hybrid search, the hit rate at k=1 was 50%, the hit rate at k=3 was 82.14%, and the hit rate at k=5 was 92.86%.

It is clear from the results that at each retrieval level, hybrid search yields better results. For k=5, hybrid search was able to retrieve the expected passages for 26 of the 28 questions while semantic search retrieved 22 of the 28 questions. This is an improvement of 14.29 percentage points. On the basis of these results, I had decided to take the hybrid search as the best retrieval method.

I think it did better on the hybrid search, because it does have an understanding of what the question means as well as being able to find specific terms related to aviation. If there was more than one passage, both passages had to be retrieved for the question to be a successful retrieval.

## 6. MCP Server and Tools

I developed an MCP server that provides two main tools: search and add_document. The search tool is provided with a question and returns relevant information from the vector database. It will return the original text, document name, page number and retrieval score. This enables the users to cross-check the source of information instead of just taking the AI-generated answer for granted.

The add_document tool can be used for adding new PDF documents to the already existing database. Rather than developing its own ingestion process, it imports and utilizes the original ingestion pipeline. The system will avoid re-embedding the same chunk if it is already embedded to prevent redundant embeddings and API usage. The tool also won't let you access files outside the project folder and only will accept files that are valid PDF.

## 7.

I have a special aviation research subagent in my .claude/agents/ directory – called Subagent I. The subagent is developed to only use the MCP search tool. It's not responsible for retrieving aviation-related information; it's responsible for explaining the information to the user and giving citations of it. The subagent does not have permission to add or modify documents. This separation can minimize risks of unauthorized changes to the knowledge base. It is also taught to deny questions where the information provided in the documents is inadequate. The following configuration was added but has not yet been verified using Copilot or Claude Code: subagent.

## 8.

I created my own LangChain Agent harness and integrated it with the MCP server using LangChain. The agent's system prompt is given as AGENTS.md. This file contains instructions on how the agent should act, how to retrieve information, how to cite and how to refuse questions that are not provided with evidence.

I installed the following two basic guardrails. In the first guardrail a human must explicitly consent to the addition of a new document via the agent. This helps to prevent unauthorized modification of the database. The second guardrail checks the validity of citations. The system first validates the citations that are retrieved in the evidence before presenting an answer back. The system substitutes a refusal if the answer fails to contain the proper or correct citations. This does not ensure that all solutions are true, however, it will minimize the chances of citations being fabricated, and it will promote utilization of the document collection in the system.

## 9.

The aim of an End to End Evaluation was to evaluate the performance of the entire RAG pipeline, not just retrieval accuracy. I developed an evaluation pipeline that classifies answers as correct, incorrect, hallucinations, correct refusals or incorrect refusals. When it was evaluated initially, it had failed all 35 questions with the answer “I don't know based on the available documents”. The seven refusals were appropriate as the question was unanswerable. The remaining 28 refusals occurred for the wrong reason, however—the documents contained required information. The overall results were a success rate of 20% initially. I have studied the issue and found that the embeddings needed were not stored in the vector database. As a result, the agent was not able to obtain evidence relevant to the case. I optimized the indexing process, with a dramatic boost in retrieval performance, and in the end, with hybrid search I managed to reach a hit rate of 92.86% at k=5.

## 10.

11. Opening a file in a text editor.12. Inserting text into a document.

One of the key aspects of the system is its capacity to grow its knowledge by incorporating new information.

Let's look at an example of this. If you take a look at the question, "What is the official title for FAA Advisory Circular 120-92D?

The question at first was posed as an unanswerable one due to the fact that the advisory circular wasn't part of the initial documentation set.

The demonstration could be used to ask a question before adding the document, get human approval, add the document to the existing ingestion pipeline, and then ask the question again.

The aim was to show how the system could learn new things without having to retrain the original language model.

But the actual output before and after could not be verified while preparing this report. Thus, it is not possible to confirm successful completion of this demonstration.

## 11. Failing and technical difficulties

During the making of this project, I had to face and overcome a few technical problems.

The first big issue was that the MCP package and langchain MCP adapter were incompatible. This caused the agent to be unable to execute properly and added some dependency changes in Python.

Secondly, Gemini was experiencing too much traffic on their API and returning the errors of HTTP 503. I solved this by using a model selection and fall back system, so that the system could try other models of Gemini.

The other big problem was the embedding API rate limit. When more than the free tier limit of embedding tokens was used, Gemini returned HTTP 429 errors.

To address this, I added in a few delays, retries, and incremental lifting of embeddings.

The primary system failure was due to the empty vector database. The agent could create responses but wasn't able to find supporting evidence, leading to inaccurate refusals.

This indicates that a language model is not sufficient to build a robust RAG system. Information retrieved is also important with respect to quality and availability.

The distinction in the evaluation framework was targeted at identifying retrieval misses, incorrect interpretation of the relevant passages, unsupported claims and incorrect refusals, as well as problematic evaluation questions.

A detailed classification of the final evaluation was not available, however.

The system was also made to capture the number of input tokens, output tokens and response time for each question. Final average # of tokens consumed and processing time was not confirmed due to lack of final evaluation results report.

## 12. Final Decision and Conclusion

In general, this project gave me a general idea of the operation of Retrieval-Augmented Generation systems and applications of these systems in industries where incorrect information can be serious.

Most importantly, hybrid search was found to be much better than semantic search. The system using the semantic similarity and keyword matching was able to get the desired information for 92.86% of the answerable questions at k=5.

Additionally, I learned that the reliability of a RAG system is dependent on the quality of the documents, the indexing, retrieval, language model and guard rails implemented.

While encouraging retrieval results, I would not be willing to completely depend on this system to make safety-critical decisions by aviation professionals.

Rather, I can only suggest that it be employed as an educational and research aide to be used to efficiently find relevant information. Official documentation and professional judgment should always be used to confirm any significant aviation decision.

If I were to expand on this project, I would make the evaluation process more streamlined, incorporate another set of questions to evaluate, go over the document licensing/personal data issues, and incorporate more sophisticated ways to detect unverifiable claims.

The project highlighted the value of RAG systems, and the limitations of RAG systems, and the need for human supervision.

## 13. AI Assistance Declaration

ChatGPT was used to assist with writing, debugging and troubleshooting the Python code throughout the development of this project. It also helped in drafting evaluation questions and arrangement of the initial report.

For generating embeddings, document-based answers, and implementing LLM evaluation process, Gemini was used.

These AI tools provided me with background information and learning aids during the assignment.
