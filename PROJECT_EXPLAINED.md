# Assignment 3: settings, decisions and what changes when you move them

Study reference for the current gift-box-shop project. This explains the implemented system and measured evidence; it is not a substitute for your own report reasoning. Business numbers below are explicitly invented examples, not shop records. Study controls do not change production settings.

## 1. What was built

A RAG assistant: question → search public documents through MCP → retrieve passages → generate a cited answer or refuse → check citation identity → separately judge correctness and support.

RAG means retrieval-augmented generation. We did not train new model weights, fit a supplier-delay classifier or build a numerical demand-forecasting model. There is no project learning rate, epoch count, 80/20 train/test split or supplier-failure probability cutoff. Gemini embeddings encode text meaning; cosine similarity ranks passages. LangChain runs the agent; MCP connects it to search and approved document addition. SQLite saves vectors so corpus text is not embedded again on each query.

The scenario is a hypothetical curated gift-box shop. Missing packaging or a product can hold up a complete box; Christmas demand makes shortages and leftover stock important. The corpus has no actual sales, contracts, supplier lead times, parcel tracking or current quotes.

## 2. The two measured retrieval designs

- Small: maximum 300 words, 60-word overlap (20%), 337 chunks.
- Large: maximum 600 words, 120-word overlap (20%), 254 chunks.
- Both together contain 591 chunk references and share 416 unique document embeddings.

A maximum is not an average: current small chunks average about 185.5 words, because pages/sections can be shorter. Chunks do not cross the retained page/section boundaries.

Measured on the same 25 answerable questions:

- k=1: small 12/25 = 48%; large 13/25 = 52%.
- k=3: small 17/25 = 68%; large 19/25 = 76%.
- k=5: small 23/25 = 92%; large 22/25 = 88%.

At k=5, mean passage context is 883 words for small and 1,131.92 for large. Small therefore gives one extra complete labelled-location hit (+4 percentage points) and about 22% less context. The documented selection rule prioritises Hit@5, then Hit@3, then lower context, so the current technical default is **small at k=5**.

Large wins at k=1 and k=3. If the system used a different k or different questions, the design decision could change. The earlier 39-question assisted set favoured large; it is a different benchmark, not a controlled before/after improvement. Only two retrieval designs received the full measured comparison; 300 words is not a proven universal optimum.

A possible explanation is that focused chunks match the question more precisely, while larger chunks preserve more context but combine topics. The benchmark establishes which design worked better here; it does not isolate a universal causal explanation.

## 3. What k controls

k is the number of passages returned **per search**, not per entire agent run. Follow-up searches can add more passages. Raising k reuses document embeddings; it does not re-embed the corpus.

For small chunks, k=3→5 increased retrieval hits from 17 to 23: six more cases, or +24 percentage points. Mean passage text increased 532.48→883 words: +350.52 words, or +65.8%.

That is not a measured +24-point increase in answer accuracy or +65.8% increase in total token cost. The full prompt includes instructions and question text, and the agent may make further model/tool calls. More context can supply missing evidence but also add distraction; answer correctness must be evaluated separately.

The allowed k range is 1–10. It is an input-validation bound, not a confidence rule. We measured k=1,3,5; k=7 or k=10 has no measured accuracy result here.

## 4. Overlap and chunk-size sensitivity

Overlap repeats boundary text so a useful explanation is less likely to be split apart. The next window moves by `stride = maximum words − overlap`.

At 300/60, stride is 240: on an illustrative long page, windows would cover words 1–300, 241–540, 481–780. At 300/90, stride becomes 210 and more text repeats.

Actual structural recalculations on this corpus, without embedding or answer-generation calls:

- 150 words / 30 overlap: 556 chunks.
- 300 / 0: 331 chunks.
- 300 / 30: 334 chunks.
- 300 / 60: 337 chunks (current).
- 300 / 90: 339 chunks.
- 600 / 120: 254 chunks.

Therefore 300→150 at 20% overlap increases actual chunk count 337→556 (+65%), not 100%. Increasing overlap 60→90 changes 337→339 chunks (+0.6%), while repeated indexed text rises 62,521→65,401 words (+4.6%). Unique corpus content remains 57,121 words.

Changing windows also changes text identities. With the current cache, adding 300/90 would require 92 new unique document embeddings, even though it adds only two net chunks. The already indexed 300/60 and 600/120 designs require zero new corpus embeddings if reused unchanged. Cache-dependent counts are recorded in eval/parameter_sensitivity.json.

More overlap may protect cross-boundary context but increases duplication and can consume k with similar passages. Less overlap reduces repetition but can split connected evidence. The 20% overlap was a reasonable starting heuristic, not a separately optimised accuracy threshold. The new structural calculations do not supply accuracy results for the untested alternatives.

## 5. Embedding variables and similarity

Each embedding has 768 coordinates. Those are learned text-representation features, not 768 hand-selected business variables. A compatible 1,536-dimensional representation would double raw coordinate storage and comparison work; 3,072 would quadruple it. Accuracy, provider cost and end-to-end time do not necessarily change in those proportions. A dimension/model-format change needs a compatible new index and cannot reuse the old vectors as if they were unchanged.

768 was a compact engineering choice; this project did not compare dimensions experimentally. Do not claim that 768 beat 1,536 or 3,072.

Cosine similarity compares vector directions and ranks evidence. A score of 0.80 is not 80% confidence that an answer is correct. The implemented retriever has **no minimum cosine-score cutoff**: it returns the top k. Even the highest-ranked passages may be insufficient, so the agent still needs to judge whether they answer the question.

If a numeric score cutoff were added, raising it could remove weak evidence but also useful evidence, causing more false refusals. Lowering it could admit irrelevant text. Neither effect has been measured for a cutoff in this project; there is no justified 0.7 or 0.8 deployment threshold here.

## 6. Actual guards and operational limits

- **Citation allowlist:** a non-refusal needs at least one valid returned ID, with no malformed or unknown citation markers. One malformed ID can cause refusal. The code checks identity, not every factual claim's meaning. Loosening the check may reduce some false refusals but weakens traceability.
- **Evidence/refusal rule:** answer only what the indexed evidence supports; otherwise use the refusal. There is no numeric uncertainty probability behind this rule. A known named publication missing from the baseline is refused by a source-identity guard.
- **Six logical model calls:** bounds agent work. Raising 6→8 increases the permitted logical-call ceiling by 33.3%, not actual usage or accuracy by 33.3%. If an answer stops early, the limit does not affect it. Retries can add provider requests beyond logical agent-call counts.
- **Eight tool attempts:** limits search/add-document loops. More attempts may allow useful follow-up searches, but also more work and cost. Approval-denied attempts still consume the tool-attempt budget.
- **Model pacing 4.3 seconds:** about 14 request starts/minute per runner. It was chosen as headroom under the endpoint limit observed during implementation, not a universal provider guarantee. Reducing it can cause throttling; increasing it can lengthen runs. Parallel clients still share service quotas.
- **Embedding pacing 0.75 seconds:** nominally up to 80 starts/minute per embedder. This is not a global cross-client rate limiter and does not determine answer quality.
- **Bounded retries:** transient failures can be retried with waits. Permanent errors or daily quota failures are not replaced with fictional results. More retries trade a better chance of completing a temporary failure against latency/additional requests, not better reasoning per successful response.
- **Timeouts:** Gemini judge requests use a 90-second timeout; the Claude CLI judge subprocess has a 360-second batch timeout. Longer timeouts allow more waiting, not a guarantee of success. The successful fallback is preserved because Gemini returned repeated service errors.
- **Document writes:** explicit human approval and a registered, provenance-reviewed file under corpus/ are required. That is a yes/no permission gate, not a confidence cutoff.
- **Input bounds:** question/search query length is 1–8,000 characters; add-document path length is 1–1,000. Chunk validation requires words > overlap >= 0. These reject invalid inputs, not risky business decisions.

The agent uses pretrained gemini-3.5-flash-lite. The configured Gemini judge could not complete reliably, so actual saved judgments came from authenticated Claude Code. Raw model-usage records are retained. There was no controlled judge-model quality comparison; availability motivated the fallback. Sampling is provider-fixed in the configured agent; no tuned temperature experiment is claimed.

## 7. Correctness, support and citation validity are different

Correctness requires all material parts of the question to be answered accurately against the reference/evidence. Support requires every material factual claim to follow from retrieved evidence. They are graded independently, with explicit binary true/false judgments; these are rubric decisions, not calibrated confidence values.

A true but incomplete answer can pass support and fail correctness. That happened for s03 and s27: backup-supplier checks were omitted. An answer can address the question but add an unsupported extra claim; s28 was marked correct but unsupported for extra inventory/safety-stock/carrying-cost claims absent from its retrieved passages.

The citation guard passed for all 25 non-refusal answers, but one still failed support. This demonstrates why valid IDs do not prove entailment. A stricter judge changes measurement, not the already-generated answer.

## 8. Current results and percentage sensitivity

The set has 31 cases: 20 single-passage, five multi-passage and six unanswerable. Thirty question/reference pairs were supplied; the extra q36 case keeps the actual add-document experiment attached to the test set. Twenty-five questions are answerable; six unanswerable cases do not enter the retrieval Hit@k denominator.

- Correctness: 29/31 = 93.5%.
- Support: 30/31 = 96.8%.
- Both correct and supported: 28/31 = 90.3%.
- Valid citation identity on non-refusals: 25/25 = 100%.
- Refusal on unanswerable cases: 6/6. There were no refusals on the 25 answerable cases.
- Answerable-only correctness: 23/25 = 92%. Its numerical equality with retrieval Hit@5 is coincidental; these are different measurements.

One changed overall correctness/support result changes the rate by 1/31 = 3.23 percentage points. One retrieval hit changes Hit@k by 1/25 = four percentage points. One of five multi-passage cases changes its group rate by 20 percentage points. Small samples are sensitive to a single case.

The reported mean agent usage is 4,134.4 input + 370.8 output = 4,505.3 total tokens/question. Mean recorded elapsed time is 6.15 seconds. These are measured averages of saved results, not future guarantees, monetary prices or cutoffs. Judge usage is separate; cached reruns can reuse saved outputs rather than spend those tokens again.

Original reported human–judge agreement was 17/20 correctness (85%), 18/20 support (90%) and 16/20 both (80%). One disagreement changes those rates by five percentage points. Those grades apply only to the original saved answers, not this run. Current AI results and historical human validation remain separate.

The 21 engineering tests and instructor extended checker pass. Engineering tests check code behaviours, not production answer accuracy. The corpus exceeds the brief's 50,000-word minimum with 57,121 cleaned words; the saved index is below 90 MB. These are assignment/packaging requirements, not learned model thresholds.

The questions were used for development and selecting a design. There is no independent unseen holdout establishing production performance. Do not call 93.5% a probability that a customer's next answer is right, or say a one-question design advantage is statistically conclusive.

## 9. Business forecasting methods in the sources—not a fitted app model

- **Naïve:** next forecast equals previous actual demand. A useful simple benchmark.
- **Simple moving average:** average the most recent m periods. A larger window generally smooths more and reacts more slowly to a new trend; a smaller window reacts faster but can be noisier. The app has no selected/fitted m.
- **Exponential smoothing:** next forecast = previous forecast + α × (previous actual − previous forecast), with 0 <= α <= 1. Higher α weights recent actual demand more heavily. α=0 ignores the latest error; α=1 makes the next forecast equal the latest actual. This α is a forecasting concept, not an app training learning rate or LLM temperature.
- **Seasonal adjustment:** period forecast = period baseline × seasonal index. Use equal-length periods. A seasonal index above 1 means above-baseline demand for that period, not a probability.
- **Forecast error:** actual − forecast. Positive means underforecast; negative means overforecast. Absolute error measures size without direction; squared error penalises large misses more heavily; percentage measures require care when actual demand is zero or very small.

Invented learning example: baseline 200 boxes, seasonal index 1.5 → forecast 300. Raising the index to 1.8 raises the forecast to 360: +60 boxes or +20%. If actual demand is 330, the first forecast has error +30 and the second −30. Raising baseline by 10% while holding the index fixed raises this formula's forecast by 10%. These are arithmetic relationships, not an actual sales estimate.

Invented smoothing example: previous forecast 100, last actual 140. α=0.2 gives 108; α=0.8 gives 132. Larger α responds more to the latest increase. Neither value was fitted or chosen for the real app.

## 10. Business variables without invented business cutoffs

Real inventory planning would need demand history/forecast error, supplier lead-time variability, existing stock, incoming orders, packing capacity, storage/cash constraints, holding cost and customer service targets. The assistant explains why these matter but does not know their values for the shop.

Extra stock can reduce exposure to shortages but ties up cash and increases carrying-cost/leftover-stock exposure. More backup suppliers may reduce dependence but can introduce qualification, coordination, price and delivery tradeoffs. A longer lead time can require earlier action; it does not justify a precise buffer quantity without data and assumptions.

No numeric safety stock, service-level target, delay probability, supplier-switch cutoff, last-order date or Christmas carrier deadline has been set by this project. There is no coded 'buy more if risk >30%' rule. Producing such a rule would require actual business inputs and validation, not just changing a retrieval parameter.

## Explain it back

Try explaining why large wins at lower k but small is chosen at k=5; why 0.8 similarity is not 80% confidence; why a valid citation can accompany an incomplete answer; and which missing data prevent a Christmas shipment promise. Use the measured facts to support your own explanation rather than copy study wording as a personal decision.

Sources: corpus_config.json, policy_config.json, server.py, runtime.py, agent.py, ingestion.py, eval/gift_shop_summary.json, current retrieval/judge records, eval/parameter_sensitivity.json, and the original human-review record. New structural what-ifs do not change the saved 31-case benchmark.
