# Assignment 3 Report

- **Name**: Javier Corredera
- **Student ID**: 19654
- **Group**: BBADBA 5B

## Use case

The assistant helps a junior financial analyst understand financial statements, cash flow, liquidity, debt and financial ratios. Its scope is explanations, cited formulas and interpretation of ratios already supplied by the user. It does not derive company ratios from raw financial inputs. An incorrect formula or an old example presented as a current company fact could mislead an analyst's screening decision; an explicit evidence gap lets the analyst seek the missing statements.

When evidence is incomplete, the assistant must name the missing company, period or figure. It may add cited concepts labelled General background, but may not substitute historical or unrelated figures for the requested answer. These scope and refusal choices were confirmed by the student.

## Corpus

| Document | Source | Edition/date | Licence | Retained words |
|---|---|---|---|---:|
| Accounting in the Finance World | [Book](https://2012books.lardbucket.org/books/accounting-in-the-finance-world/) | Archived 2012-12-29 | CC BY-NC-SA 3.0 | 26,275 |
| Accounting for Managers | [Book](https://2012books.lardbucket.org/books/accounting-for-managers/) | Archived 2012-12-29 | CC BY-NC-SA 3.0 | 34,984 |
| Financial Management for Small Businesses, 2nd OER Edition | [Book](https://openbooks.lib.msu.edu/financialmanagement/) | 2021-01-28 | CC BY 4.0 (downloaded edition) | 22,378 |

The retained corpus contains 83,637 words in 78 sections from three documents. The two Lardbucket books credit anonymous authors at the original licensor's request. The MSU book credits Lindon J. Robison, Steven D. Hanson and J. Roy Black. The downloaded MSU edition states CC BY 4.0; the current catalogue states CC BY-NC 4.0, so the collection is used for noncommercial coursework with attribution. Full attribution and licence details are saved in `corpus_manifest.json` and `index/ATTRIBUTION.txt`. These historical textbooks do not supply current company accounts or current reporting requirements.

## Ingestion

`prepare_corpus.py` extracts the selected HTML sections, removes navigation and author biographies, and retains headings, tables, MathML and image alternative text. Formula extraction was a concrete issue: equations omitted by a plain text extraction were recovered from MathML and image descriptions. Images without descriptions are recorded as a limitation rather than reconstructed.

The shared ingestion pipeline uses approximately 400 whitespace-word chunks with 50-word overlap, without crossing source-section boundaries. The saved index contains 272 chunks and 768-dimensional `gemini-embedding-2` vectors. Each passage has stable identity, source/section information, word offsets and a citation label. Documents are content-addressed: identical bytes reuse the saved index even after a rename; changed bytes create a separate version. Vectors are persisted individually in SQLite so interrupted embedding resumes; startup does not re-embed the corpus. Both the index command and `add_document` use this ingestion implementation.

## Test set

The student supplied 30 questions and reference answers in the collaboration chat before retrieval tuning. Evidence was checked against the actual saved passages; revisions and the original drafts are recorded in `eval/question_provenance.json`. Classification follows the final chunk boundaries: 16 single-passage, 9 multi-passage and 5 unanswerable questions. The initial questions, provenance and hashes are frozen under `eval/question_sets/initial/`.

Examples include q06, asking why the quick ratio differs from the current ratio and which asset it excludes, and q03, asking for Southwest Airlines' most recent operating cash flow. The latter is deliberately unanswerable because the book contains a 2010 example rather than the requested current statements. Gold evidence was not changed in response to retrieval results.

## Retrieval

Dense retrieval uses cosine similarity over the saved embeddings. Hybrid retrieval combines dense and BM25 rankings using equal-weight reciprocal rank fusion (constant 60, top 50 candidates per ranking). Both use the same corpus and chunks; parameters were initial defaults rather than tuned on this test set.

| Design | k | Any evidence hit | All required evidence hit | Evidence recall |
|---|---:|---:|---:|---:|
| dense | 1 | 72% | 48% | 60% |
| dense | 3 | 92% | 76% | 84% |
| dense | 5 | 92% | 88% | 90% |
| hybrid | 1 | 40% | 24% | 32% |
| hybrid | 3 | 84% | 76% | 80% |
| hybrid | 5 | 88% | 84% | 86% |

These rates use the 25 answerable questions. Any-evidence hit means at least one annotated passage is retrieved; all-required-evidence hit requires every annotated passage. Unanswerable questions are excluded from retrieval hit-rate denominators. The student chose dense after reviewing these measurements: it returned all required passages within five results for 22/25 questions, compared with 21/25 for hybrid. Detailed rankings are saved in `eval/retrieval_results.jsonl`.

Across all 30 original retrieval queries, the top five passages contributed a mean of 1,696.3 whitespace words for dense retrieval and 1,775.7 for hybrid (medians 1,764.5 and 1,833). These are passage-text words, excluding metadata and instructions; they are not token counts. Details are saved in `eval/retrieval_evidence_volume.json`. Actual agent queries may differ from the original questions and their returned passages are preserved in the answer traces.

## Tools and subagent

The stdio MCP server exposes `search(query)` and `add_document(path)`. Search returns five citation-first passages and the same retrieval data as structured content. Adding a document previews the file and requires approval through the harness; noninteractive evaluation denies additions.

The Claude profile in `.claude/agents/corpus-researcher.md` permits only `mcp__corpus__search`. The native Copilot adapter in `.github/agents/corpus-researcher-copilot.agent.md` permits only `corpus/search`; the actual editor tool picker was checked to confirm that all other tools, including `add_document`, were deselected.

Actual excerpt from the second VS Code Copilot interaction (Auto routed to MAI Code 2 Flash). The full unedited exports are `eval/copilot_transcript_attempt1.json` and `eval/copilot_transcript_attempt2.json`.

**User:**
> Use only the corpus search tool, with at most three searches. Answer briefly and cite the exact source/location labels returned by search. If the evidence is missing, say what is missing. Do not add or edit files.
>
> Why would I use the quick ratio instead of the current ratio, and which current asset does it leave out?

**Search 1:** `quick ratio versus current ratio excludes which current asset inventory`

**Returned citation:** `[financial-management-small-businesses | Chapter 6, learning goals: Quick (QK) ratio]`

**Search 2:** `acid-test quick ratio formula inventory excluded current liabilities`

**Returned citation:** `[financial-management-small-businesses | Chapter 6, learning goals: Quick (QK) ratio]`

**Search 3:** `What is the quick ratio? inventory inventory is excluded`

**Returned citation:** `[financial-management-small-businesses | Chapter 6, learning goals: Quick (QK) ratio]`

**Copilot final response:**
> I cannot provide a source-cited answer because the retrieved passages were not accessible with exact `[source | location]` labels. Please run the search again; the evidence needed to explain the comparison and identify the excluded asset was not usable.

Each search returned relevant passages with exact citation labels. Despite this, the editor model declined. The readable-result revision was tested and the server restarted before the second interaction; it did not resolve the refusal. This is a genuine failed answer demonstration, not a successful cited answer.

## Adding a document

The duplicate policy is content-based: identical bytes reuse/resume the existing document, including after a rename; changed bytes produce a separate version.

For the before/after demonstration, the student explicitly approved the supplemental `southwest-2025-cash-flow-facts.md` fact sheet. It compiles numeric observations from Southwest's [2025 Form 10-K, page 88](https://www.sec.gov/Archives/edgar/data/92380/000009238026000004/luv-20251231.htm), with original wording offered under CC0; this does not relicense the source filing. The note, source attribution, exact approved file hash and approval response are preserved under `eval/add_document_demo/`.

Before addition, the saved q03 answer declined to supply the latest fiscal-year figures and discussed only the textbook's 2010 example. After addition, the same question and answering model reported 2025 operating cash inflow of $1,842 million, a $4,278 million cash decrease, and net investing and financing outflows of $1,429 million and $4,691 million. It explicitly corrected the question's premise that cash changed only a little. The new facts were cited to the added passage.

The real MCP `add_document` call used the shared pipeline and embedded one new chunk. The demo index contains 273 chunks; the graded baseline remains at 272 and its corpus fingerprint is unchanged. `add_document_demo.py` creates the isolated copy, obtains an approval callback tied to the exact file hash, saves the tool trace, and stores the after-index checkpoint. Its preview mode makes no model calls. The raw before/after answers and actual addition trace are saved in `eval/add_document_demo/`.

The after-answer passed the successful-search and citation-identity checks with three citations. A primary provider error was recovered through the permitted correction attempt, so its reported token usage is incomplete. This single demonstration establishes the observed behavior on q03; it is not a new aggregate accuracy measurement or a change to the frozen test set.

## Harness and guardrails

The LangChain harness reads `AGENTS.md`, searches before answering and treats source text as evidence rather than instructions. It permits at most three MCP calls, five primary model calls and one correction call without tools. Every `add_document` invocation requires an approval callback; it is denied by default during noninteractive evaluation.

The extra guardrail checks that citations identify passages actually returned by search and that substantive answer claims carry citations. An invalid draft receives one correction attempt and then a transparent refusal if still invalid. This checks citation identity and required fields, not semantic entailment; human review and the separate judge assess whether claims are supported.

In the fixed answer run, q07 triggered the identity gate: the model named the MSU Profit margin subsection in a citation label that was not actually returned by search. Its correction retained that label, so the displayed answer was a technical refusal. The trace and both guardrail events are preserved in `eval/answers.jsonl`.

There were also three primary runtime errors among the fixed 30 displayed attempts: q08 and q20 encountered rate limits, and q30 encountered a deadline timeout. Repair produced drafts but the attempts ended in guardrail fallbacks. They remain in the end-to-end denominator because those are the answers the student reviewed; they were not replaced after human grading. The runtime evidence is recorded in `eval/runtime_failures.json`. Earlier attempts that ended in service errors without any structured draft were preserved separately rather than presented for review.

## Evaluation

The answering model was `gemini-3.1-flash-lite`; the final judge model was `gemini-3.5-flash-lite`. The final run scores all 30 fixed displayed answers. The student completed 20 reviews before the judge and their CSV was bound to exact question/answer/evidence hashes. Binding is preserved in `eval/runs/f0fa6c5df158007be127/human_binding.json`; the original blind labels remain unchanged.

The rubric scores correctness and support independently. A supported refusal can be correct when the requested company, period or figure is absent; a refusal is incorrect when essential evidence is available. A citation alone does not establish support. Every substantive financial claim must be established by the retrieved passages, respecting company and date. Unsupported additions can fail support even when the main explanation is correct.

| Measure | Final judge, all 30 | Student, reviewed 20 |
|---|---:|---:|
| Correct and adequate | 25/30 | 14/20 |
| Supported | 29/30 | 16/20 |
| Both grades pass | 25/30 | 11/20 |

The judge identified 5 correct refusals and 5 wrong refusals. Requiring both judge grades, a successful search, valid citation identities and an unblocked final answer gives a judge-assessed reliability rate of 25/30 (83.3%). This is a judge-based estimate, not independently verified reliability over all 30 answers.

On the same 20 human-reviewed answers, correctness agreement was 18/20 (90%), support agreement was 15/20 (75%), and agreement on both fields simultaneously was 14/20 (70%). In the correctness confusion table, two human-negative answers passed the judge. In support, all four human-negative cases passed the judge, while one human-positive refusal received a support failure from the judge. The individual disagreements are q03, q04, q05, q09, q15 and q20. Full reasons, the independent confusion tables and original human notes are saved in `eval/summary.json`, `eval/judge_results.jsonl` and `eval/human_labels.csv`.

Earlier judge attempts are retained in the run cache. Provider 503/504 errors affected the first model; a second model reached a provider-reported 20-request daily free-tier limit. The final lighter model was selected by complete-request availability, not by accuracy or agreement. All published final verdicts use that one model. Temporary failures are logged separately; a daily quota now stops short retries. The final `main.py evaluate` rerun uses the saved valid verdicts rather than making new model calls.

For the fixed answering attempts, mean recorded latency was 7.97 seconds. Mean reported generation usage was 7,381.4 tokens over the 27 attempts with complete metadata; the three interrupted primary executions are excluded from that token mean. The final judge averaged 4,533.4 reported tokens and 11.61 seconds per saved verdict. Embedding usage is unavailable. These recorded invocation means exclude some earlier failed runs, availability checks, superseded judge work and waiting between separate runs, so they do not represent the entire development cost or wall-clock time.

The unchanged official `check.py` passed its live key, index, test-set, MCP and answering checks. All 39 local tests passed. The separate cached evaluation rerun verifies the completed evaluation path without additional model calls.

## Failures

The following primary categories were confirmed by the student after reviewing their own notes and the saved execution traces. The ten cases are the union of judge/code failures and human–judge disagreements, so this count has a different basis from the judge's five incorrect answers. Each case has one primary category; operational errors are also noted where relevant.

| Primary cause | Count | Questions | Basis |
|---|---:|---|---|
| Retrieval miss | 2 | q02, q04 | The required limitations/estimation-evidence passages were absent from the returned set. |
| Unsupported claim | 3 | q03, q05, q09 | Overbroad claims about what the collection lacks, or background claims beyond the returned evidence. |
| Wrong refusal | 4 | q07, q08, q20, q30 | Answerable requests ended in refusals; q07/q20 had relevant evidence, while q08/q20/q30 also had provider errors. |
| Wrong/incomplete answer from a relevant passage | 1 | q15 | The student's review required the book-specific EBIT and asset-basis qualifications omitted by the answer; the judge accepted it. |
| Bad test question | 0 | — | No case was confirmed in this category. |

For q08, the trace shows a rate-limit error before any search. It is therefore an operational refusal rather than evidence of a ranking miss. Q20 combines a primary rate limit with an invalid citation correction; q30 records a deadline error and fallback. These causes matter when deciding which component to improve.

The human support concerns in q03, q05, q09 and q15 were all accepted by the judge. In q03, for example, the response claimed that the documents contain no financial information after 2010 even though the retrieved HQN example contains later financial statements. Q15 is a more borderline disagreement about omitted qualifications, as the student noted. The judge also failed support for the bare refusal in q20, which the student treated as supported because it adds no unsupported financial claim.

The student's first priority is to constrain the assistant to what the actual passages show, use precise statements about missing evidence, and tighten the judge's claim-support assessment. Provider recovery follows, so a technical failure does not appear as an evidence-based refusal. Citation copying and retrieval coverage are additional issues documented by the cases. These are proposed next improvements; the measured answers, frozen test set and blind grades have not been rewritten after seeing results.

## Decision

Student's conclusion, supplied in the collaboration chat:

> I wouldn't let a junior analyst rely on it yet, so I agree with keeping it as a demo: only 11 of 20 answers passed both checks, and the errors (claiming the books say nothing when they do, or dropping a key detail) are the kind a newer analyst would trust and miss. The first fix is to make the assistant only say what the retrieved passages actually show, and to tighten the AI judge, since it passed all four answers I marked unsupported; retrying after errors like Q08's rate limit comes next, so a technical failure no longer looks like a refusal.

The release decision is therefore to keep the system as a demonstration rather than a tool a junior analyst can rely on. Any demonstrated output needs direct checking against the displayed source passages. The judge's 25/30 estimate does not override the student's 11/20 both-pass result on the reviewed subset. The measured token and latency figures, including their limits, are reported in the Evaluation section above.

## AI use

Codex assisted with implementation, corpus preparation, evidence checking, retrieval measurement, debugging, tests and factual report drafting. The student supplied the 30 evaluation questions and reference answers in the chat and selected the use case, scope, version policy, guardrail behavior, scoring policy and retrieval design. VS Code Copilot was used for the actual search-only helper interactions preserved above. Gemini supplies embeddings and agent/judge model calls.

The student completed 20 blind human reviews in the local review page. These were bound to the exact answer/evidence hashes before any current-run judge results were generated. The student confirmed the primary failure categories and supplied the deployment conclusion and improvement priorities in their own words; that response is preserved in `eval/student_analysis_confirmation.json`. No human ratings or successful editor transcript have been fabricated.

## Focused improvement round (25 November 2026)

After the original submission, the student requested one focused improvement round and authorized AI assessment of the revised answers. The original 30 answers, 20 blind human grades, bindings, judge results and failure analysis above are retained unchanged. Historical implementation descriptions above refer to that baseline. The revised system adds:

- A mandatory MCP search on the original question before generation, with eight dense results instead of five. Follow-up searches share the original three-call budget.
- Instructions to keep evidence-gap statements specific to retrieved passages, omit unnecessary company-data disclaimers on conceptual questions, and preserve source-specific formula qualifications.
- A separate model audit of claim support, including uncited absence statements and claims about benchmarks. An audit failure or invalid citation receives the same single correction opportunity, followed by another check. Audit unavailability fails closed. This probabilistic audit is not proof of entailment.
- Bounded retries for temporary service errors. Primary generation can execute twice, with five model calls per execution and the shared three-tool limit. Correction and audit requests allow at most three transport attempts. Daily-quota errors are not retried in a loop. Retries and support audits are saved, and usage after an interrupted call is marked incomplete.

`gemini-3.1-flash-lite`, used for the original answers, returned repeated HTTP 503 errors. An availability-only probe succeeded for `gemini-3.5-flash-lite`, which is therefore used for all revised answers. Failed initial attempts and the probe are retained under `eval/improvement_round/`. This model change is a confound: any observed gain cannot be attributed to the code changes alone.

The revised answers are evaluated on the same known 30 questions. A paired AI reviewer applies the same stricter support instructions to both baseline and revised answers, alternating A/B order and receiving each answer's own retrieved passages. It sees the fixed reference answers but neither human labels nor previous verdicts. The original human grades are not copied onto new answers. There is no new human–judge agreement estimate. The reviewer and answerer share the same provider/model family, so correlated errors remain possible. This is a development comparison, not a new blind or held-out evaluation.

Run `python improvement_round.py` to resume this separate round. Once complete, `python main.py evaluate` verifies the saved comparison, provenance, unchanged corpus and original human bindings without making new model calls. `python improvement_round.py --verify` performs the same verification. The original evidence remains under `eval/runs/f0fa6c5df158007be127/`; saved baseline code is under `eval/improvement_round/baseline_code/`.

Preflight checks exposed an additional problem: the model-only audit accepted a dated 2010 example as the answer to a latest-year question. The final candidate therefore also has a conservative deterministic freshness gate for explicit latest/current-data requests: if none of the retrieved passage text contains a year at least as recent as the previous calendar year, a requested-answer claim must be replaced by an explicit gap, with any historical figures confined to labelled background. Generic questions about the current ratio do not activate this gate. A recent year is only a necessary check, not proof that the requested company/period is present; the semantic audit still has to check the association. Preliminary candidate outputs are retained in `development_preflight*` rather than presented as final results. These preliminary runs were stopped during infrastructure debugging; their outputs are not the final comparison.

Repeated provider failures prompted a final orchestration change before the full comparison: ordinary questions use LangChain structured query planning, a second MCP search for the general principle, and direct structured answer generation. They do not depend on model tool routing. Query-plan failure falls back to the mandatory original search. Interactive document-addition requests retain the tool-calling graph and the application approval callback. All paths share the three-MCP-call limit and single correction policy. This final candidate is frozen for the complete comparison.


### Measured comparison

All 30 revised answers and all 30 paired reviews are saved. The same stricter AI instructions were applied to both versions; the first column below preserves the original published judge rather than silently replacing it.

| Measure | Original published judge, baseline | Paired AI review, baseline | Paired AI review, revised |
|---|---:|---:|---:|
| Correct and adequate | 25/30 | 25/30 | 26/30 |
| Supported | 29/30 | 29/30 | 27/30 |
| Both pass | 25/30 | 25/30 | 26/30 |
| Wrong refusals | 5 | 5 | 3 |

Requiring both paired AI grades, successful search, valid citations and no guardrail block gives 25/30 for the baseline and 26/30 for the revised version. Cases changing from failing to passing both AI criteria: q07, q08, q20, q30. Cases changing from passing to failing: q03, q15, q26. These are AI estimates on known questions, not new human-validated accuracy.

The original student human-review result remains **11/20 passing both on the baseline only**. The revised answers have no human labels or human–judge agreement figure. The stricter reviewer is also imperfect: it still accepted the baseline q03 support claim despite the original student's contrary evidence-based assessment. Its scores therefore do not override the student's review or establish production readiness.

The initial original-question dense search with eight results contains all annotated evidence for 23/25 answerable questions, compared with 22/25 at five results in the original experiment. This larger retrieval budget and the additional reformulated query are deliberate development changes, not an equal-budget retrieval victory. The corpus, annotations and initial dense-versus-hybrid measurements remain unchanged.

Mean recorded invocation latency is 7.97 seconds for the baseline and 25.20 seconds for the revised answers. Mean reported generation usage for complete-metadata attempts is 7,381.4 tokens (27 baseline answers) and 21,338.2 tokens (8 revised answers). Revised usage includes reported query-planning, answer, audit and correction calls. Provider-interrupted calls, separately saved no-draft service attempts, probes, preflights and embedding tokens remain incompletely counted; these figures are not the full cost of development. Request pacing also adds waiting time. The extra audit and evidence impose a measurable cost.

The supplemental failure categories are {"unsupported_claim": 1, "wrong_refusal": 3}. Individual reasons and traces are in `eval/improvement_round/failure_analysis.csv`, `answers.jsonl` and `paired_reviews.jsonl`. These categories were assigned by Codex from the AI verdicts and traces and are not new student grades. In q03 the deterministic freshness gate blocked a 2010 figure from being presented as current; the final technical fallback was still inadequate. Q15's final answer was blocked when its support audit hit a provider rate limit. Such fail-closed behavior prevents unverified output but remains an end-to-end failure.

Following an observed 15-request/minute free-tier limit, shared pacing of 0.2 requests/second was added after 26 answers had been saved. Those outputs were retained; the transport change and earlier answering-code hash are recorded in `provenance.json`. Two concurrent question tasks share the pacer, and no new human labels were created. This transport revision occurred before paired judging and did not change the answer prompts, retrieval policy, models or scoring criteria.

The revised code passes all **44 local tests** and the **unchanged official checker**, including a live MCP search and answer. `main.py evaluate` verifies the saved original human bindings and the supplemental comparison; the ZIP is also checked without an API key. The original student deployment decision remains a demonstration only. This round adds measured progress and exposes remaining failures; it does not claim that the assistant is ready for independent analyst use.

The round is **mixed rather than a clear overall win**: four failures improve and three cases regress, giving one additional both-pass answer in the paired AI review. The support score drops from 29/30 to 27/30, and mean invocation latency rises from 7.97 to 25.20 seconds. The token mean is higher and covers only eight complete-metadata revised attempts, so it is an incomplete cost comparison. These tradeoffs and the model change prevent a claim of a robust overall reliability improvement. The updated system remains a demonstration, with both versions and all observed results preserved.

A Codex AI spot-check disputes the q26 unsupported-claim ruling: retrieved section 7.3 expressly says that the company continues to report the historical $7,000 figure, which is the sentence the judge rejected. The paired verdict, AI-assigned category and aggregate scores are retained unchanged; `codex_spot_check.json` and the CSV annotation record the disagreement. Thus the three reported regressions are **AI-assessed**, and q26 is not an established factual regression. This is another reason not to treat automated scores as ground truth.
