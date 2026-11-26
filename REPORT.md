# Gift-shop supply-chain assistant

Jimena Navarro Del Águila · DAIIST Assignment 3

## Business and problem

The use case is a small online shop selling curated gift boxes. Products and packaging come from different suppliers, so one missing item can prevent completion of an otherwise ready box. The two priority problems are supplier delays and the Christmas demand peak. This is a hypothetical business scenario; no actual company sales, supplier records or delivery promises were provided.

The owner or operations manager uses the assistant to research contingency planning and seasonal inventory decisions. A wrong answer could lead to missed Christmas deliveries, cancelled orders, lost sales or unnecessary stock. A refusal is preferable to an invented supplier arrival date or stock target, although unnecessary refusal can delay a useful planning decision.

The assistant searches public guidance and produces cited explanations. It does not track parcels, contact suppliers, place orders or calculate an optimal Christmas purchase quantity from missing inputs.

## Test questions and references

The final set contains 30 gift-shop questions and reference answers, plus the supplementary missing-document case q36 used in the add-document experiment. There are **31 questions: 20 single-passage, five multi-passage and six unanswerable**. Source locations are recorded in `eval/questions.csv`.

The questions cover forecast uncertainty, Christmas inventory, supplier alternatives, logistics and information sharing. The unanswerable cases require private order details, unknown future demand or an unindexed publication. They test whether the assistant recognises missing evidence instead of inventing an answer.

AI supported implementation, clarification and wording. Jimena provided the 30 core question/reference pairs and reports doing most of the substantive work. The retained q36 case is an AI-assisted engineering example. Creation records and the assistance statement are retained in `eval/user_supplied/` and `eval/question_provenance.json`.

## Corpus and ingestion

| Source | Clean words | Role and reuse basis |
|---|---:|---|
| Introduction to Operations Management, Seneca/LibreTexts | 30,852 | Forecasting, seasonal inventory, supplier coordination; CC BY-NC, credits retained |
| FEMA Supply Chain Resilience Guide, April 2019 | 11,671 | Dependencies, continuity, outreach and exercises; U.S. federal text, third-party images excluded |
| UK Critical Imports and Supply Chains Strategy, January 2024 | 14,598 | Diversification, shocks and visibility; Open Government Licence v3.0 |
| **Total** | **57,121** | **Three public sources; noncommercial academic use** |

The documents support planning principles, not a ready-made gift-shop operating plan. FEMA targets emergency managers; UK national policy is not Spanish law or a retailer-specific requirement. Source URLs, credits and exclusions are in `CORPUS_NOTICES.md` and `corpus/SOURCES.json`.

PDF extraction retains original PDF page locations. HTML extraction uses the article body and hierarchical headings, excluding website navigation. Whitespace, ligatures and repeated headers are cleaned. Navigation contamination was one extraction issue fixed by selecting the article container. Every chunk retains text, a deterministic ID, source and location.

Gemini Embedding 2 supplies 768-dimensional vectors saved in SQLite. Exact cosine search uses saved vectors; the MCP server never re-embeds the corpus at startup. The small design uses 300 words/60 overlap (337 chunks); large uses 600/120 (254 chunks). The 591 chunk references share 416 unique embedded texts. Rebuilding unchanged text makes zero new corpus embedding calls. New queries may need cached-or-new query embeddings.

## Current retrieval comparison

The denominator is 25 answerable questions. Unanswerable questions have no gold passage and are excluded. Multi-passage success requires all labelled source/location pairs; valid source identity is not semantic entailment.

| Design | Hit@1 | Hit@3 | Hit@5 | Mean passage words at k=5 |
|---|---:|---:|---:|---:|
| small | 48.0% | 68.0% | 92.0% | 883.0 |
| large | 52.0% | 76.0% | 88.0% | 1131.9 |

The small design at k=5 is now selected: **23/25** hits versus **22/25** for large. Small returns one additional complete labelled-evidence match and uses **22.0% less context**. Large performs better at k=1 and k=3, but the system uses k=5 and its documented selection rule prioritises Hit@5. This changes the earlier assisted-set choice of large; the new questions produce different results. The partial large-chunk answer run is preserved and is not treated as a completed comparison of semantic accuracy. This is a development-set selection; the small sample does not establish a universally optimal design.

## MCP tools, harness and safeguards

`search(query)` returns passages, exact citation IDs, sources and locations. `add_document(path)` uses the shared ingestion pipeline and accepts only registered corpus files with provenance/reuse metadata. Unchanged texts reuse saved embeddings; changed registered sources replace their active chunks.

The LangChain/Gemini harness loads `AGENTS.md`, searches the original question over actual stdio MCP and can search missing aspects separately. The gift-shop scenario is in the system instructions. Every substantive factual claim needs an exact returned citation. Missing/invalid IDs cause refusal; equivalent bracket syntax can be normalised but IDs are never silently repaired. Citation identity does not prove support.

Additional controls are approval before document addition, registered-path restrictions, six model calls/eight tool attempts, and a named-missing-source guard. Retrieved text is untrusted evidence, not instructions. General guidance must not be presented as a retailer-specific prediction. Model sampling is provider-fixed; request pacing and bounded transient retries respect endpoint limits. Credentials remain local and are excluded from the archive.

The authenticated editor subagent is restricted to `mcp__corpus__search`. Its genuine earlier infrastructure/inventory session is reproduced below and remains relevant to this business. It is not presented as a newly rerun Christmas-specific conversation.

## Current answers, judge and cost

Current run: `b21556362ea6bc2e`. All 31 answers are actual outputs from the revised gift-shop prompt. The original 36-case run and its corrections remain separate historical evidence.

The real judge completed **31/31** verdicts: **29/31 correct** and **30/31 supported**. These are model judgments, not definitive ground truth.

Mean recorded agent usage is **4134.4 input**, **370.8 output** and **4505.3 total tokens per question**. Mean elapsed time is **6.15 seconds**. These describe saved successful outputs, not monetary cost, separate judge usage or all failed attempts.

## Human review and AI evaluation: separate evidence

The original human review and the updated gift-shop AI evaluation are reported separately. Original ratings have not been replaced or transferred to revised answers.

| Evidence | Original human-reviewed run | Revised gift-shop AI run |
|---|---|---|
| Run ID | `5c1ef6b35bf29617` | `b21556362ea6bc2e` |
| Saved agent answers | 36 | 31 |
| Human review | 20 original answers; reported by Jimena and transcribed with provenance | No human review claimed for revised answers |
| AI judge | Gemini, original run | Claude fallback after Gemini service failures |
| Human–judge agreement | 85% correctness; 90% support; 80% both | Not measured; original agreement does not apply |
| Purpose | Evidence of the original human review | Automated assessment of the updated scenario and answers |

The original human grades and their exact run binding are preserved in `eval/human_labels.csv`, `eval/human_labels_run.txt` and `eval/generic_baseline/`. Jimena reported independently reviewing the same sample and obtaining matching results. The ratings were transcribed from the reported review. The AI review was already visible, so blind independence is not claimed. The newer run has real AI judgments but is not labelled human-validated. Editorial corrections are also distinct from both measured runs.

The figures describe different outputs and different judge models. They are not a controlled before/after accuracy comparison. This separation preserves the original review without implying that revised answers were rated by a human.

## Recorded agent outputs

Judge provider/model: **claude-haiku-4-5-20251001,claude-opus-5[1m]**. Gemini service failures prevented the configured judge from completing. The fallback Claude judge used the same rubric, actual saved answers and evidence, without tools or human labels. Raw responses and usage are saved under the run’s `claude_judge/` directory. These scores are not directly comparable to the historical Gemini-judged baseline.

These are the original saved outputs, including a failure discussed below. They have not been edited to improve the benchmark.

### s03: What should I check about a backup packaging supplier before my usual supplier runs into delays?

Based on the indexed guidance, when evaluating backup suppliers or alternate supply sites before delays occur, you should check:

* **Potential delays, cost increases, and transport options** associated with second- and third-tier backup sites [chunk:ccc348aa5ce732328cb17e89b550133fd76daecba5f8d202b368ac5ffd19e692].
* **Alternative facilities** that can be used to reroute supplies if needed [chunk:ccc348aa5ce732328cb17e89b550133fd76daecba5f8d202b368ac5ffd19e692].
* **Specialized capabilities or needs** of the distribution points (such as reliance on automation or information technology) [chunk:ccc348aa5ce732328cb17e89b550133fd76daecba5f8d202b368ac5ffd19e692].
* **Legal or regulatory restrictions** that could impede transferring supply operations or servicing specific destinations [chunk:ccc348aa5ce732328cb17e89b550133fd76daecba5f8d202b368ac5ffd19e692].
* **Alternative modes of distribution** and delivery services available [chunk:ccc348aa5ce732328cb17e89b550133fd76daecba5f8d202b368ac5ffd19e692].

**Assistant Scope & Limitations:** 
This guidance is drawn from general emergency management and supply chain resilience literature (such as FEMA guidelines) intended for broader logistical planning. A static corpus cannot supply live performance records, current shipping schedules, or specific lead times for your particular packaging supplier. Checking these factors helps inform contingency planning, but no recommendation can guarantee uninterrupted delivery or prevent disruption.

### s26: Why is my early Christmas forecast uncertain, and what cost should I weigh if I carry extra stock because of that uncertainty?

Based on the indexed operations source, forecasts are generally uncertain because they are rarely 100% accurate, and forecast accuracy tends to decrease as the time horizon increases (meaning the farther away the forecast is from the current date, the more uncertainty it contains) [chunk:7964c4b98ebc389ad912fae279b7fe0b0b6b608b4563a3e0d8efd9b10976d155]. Additionally, anticipating exact customer behaviour is a challenge, and demand patterns can be affected by trends, cycles, seasonal factors, irregular variations, and random variations [chunk:57a3b1d922c8d9fb054d936f76ac7da2c4c099995bcfb000747d7f990d447e39][chunk:7964c4b98ebc389ad912fae279b7fe0b0b6b608b4563a3e0d8efd9b10976d155].

When deciding to carry extra stock to manage this uncertainty, distributors and retailers try to balance customer service (providing excellent service with few or no disappointed customers) with the **cost of keeping large inventories on hand**, which can cause extra costs and inefficiencies when inventory is stored across multiple locations [chunk:57a3b1d922c8d9fb054d936f76ac7da2c4c099995bcfb000747d7f990d447e39]. 

**Assistant Scope & Limitations:** 
As an evidence assistant, I cannot access your live sales data, live supplier lead times, or current inventory levels. A static corpus cannot supply those specific retail facts, and these general principles do not guarantee delivery or prevent disruption.

### s21: Will my current packaging order arrive before I start packing Christmas boxes?

I don't know from the indexed documents. The corpus does not provide enough evidence to answer this question.

## Failure analysis and decision

The original development review found a reversed seasonal relationship, an incomplete inventory tradeoff, two unnecessary refusals, and an unsupported aggregation explanation. Those original outputs, actual reruns, edited corrections and separate passing judge results are preserved in `eval/corrections/`. They are known-case improvements, not a replacement for the new run’s scores.

Current code can check citation identity and refusal behaviour. Each current semantic failure below is the judge’s provisional diagnosis, to inspect against the references. Retrieval misses can occur even when a plausible answer is generated. A proper refusal when retrieval misses evidence can be reasonable locally while still exposing a corpus-level retrieval failure.

Mechanical checks found 0 refusal(s) on answerable questions: none. Refusal counts and valid-citation counts for this run are recorded in eval/gift_shop_summary.json. Citation identity does not establish semantic support.

- **s03 — wrong_answer_from_right_passage:** The answer answers about distribution-point backup sites, licensing restrictions and distribution modes, omitting the reference's material points (secondary contracts, ease of switching sources, suppliers' business continuity plans/capacity) that are present in the retrieved page 26 'Supply Source' passage; the statements it does make are grounded.
- **s27 — retrieval_miss:** The risk half is answered correctly from the supplier-diversity passages, but the 'what to check' half only offers country-level transport/regulatory feasibility and generic risk-appetite language, missing the reference's concrete checks (backup agreement, ease of switching, whether the alternative can cover the shortfall); the claims made are nonetheless traceable to the retrieved uk-strategy chunks.
- **s28 — retrieval_miss:** Both parts are addressed consistently with the reference (supplier reliability checks plus EDI exchanges including ASNs and shipment status), but the closing paragraph's claims about safety stock, stockout protection and higher carrying costs are not stated in the cited chunks bb1662b7/e9b5b6a1 or any retrieved passage. Secondary flag: **unsupported_claim**.

Use the assistant as a human-reviewed planning aid. Keep citations visible and allow refusals. Do not let it autonomously choose suppliers, promise Christmas arrival or set purchase quantities. For a real stock decision, the owner would need demand history, forecast uncertainty, supplier lead times, cash/storage constraints and service targets. These inputs were not supplied.

## Before and after adding a document

The actual isolated SBA experiment is retained in `eval/before_after.json`. Before addition, the assistant refused a question about the absent guide. After the approved 252-word public introduction was added through MCP, it answered the five numbered sections plus the worksheets appendix with new citations. One new embedding was required because the page is identical under both chunk designs. The temporary corpus had 57,373 words and 338/255 chunks; the three-source baseline was preserved. This tests the add-document mechanism, not a Christmas shipment prediction.

## Checks and scope

The 21 offline engineering tests pass, including four regression tests for stale results and cross-run label leakage. The unchanged instructor checker and its extended evaluation path are checked against the packaged project. `main.py evaluate` integrates the actual saved Claude judgments and recomputes the original human agreement separately, with content hashes preventing stale result reuse. The original corpus can be indexed again with zero new embeddings. The real search-subagent transcript and actual before/after experiment are included. 

The assistance and provenance records are retained. Historical human agreement applies only to the original answers; no human–judge agreement is claimed for the updated run.

## Editor-subagent transcript

### Actual Claude Code session

Authenticated session: `a3bf9c42-efab-49bc-84bd-dd8ee669c9f9`. Configured subagent: `corpus-researcher`. The raw child trace contains only `mcp__corpus__search` tool calls (14). The parent delegated through its actual Agent tool. This is an excerpt from real events; full parent/child JSONL is included.

**User request:** Research question: Why should supplier contingency planning consider both supporting infrastructure (e.g. utilities, transport/logistics networks, IT/communications, facilities that suppliers depend on) and inventory buffers (e.g. safety stock, buffer inventory, stockpiles)?

Requirements:
- Use ONLY the mcp__corpus__search tool. Do not read, write, or modify any files. Do not add documents to the corpus.
- Run multiple distinct searches to retrieve evidence for BOTH aspects separately: (a) supporting infrastructure dependencies in supplier/business continuity planning, and (b) inventory buffers / safety stock as a contingency measure. Also search for anything linking the two.
- Cite exact chunk IDs in the form [chunk:ID] for every claim.
- For each piece of evidence, state the source location (source ID and page/word location as returned by the tool).
- Explicitly state limitations: what the corpus does and does not support, where retrieval scores were weak, and whether the corpus directly answers the "why both" framing or whether that connection is your synthesis.
- If the passages do not support part of the question, say the corpus cannot answer that part.

Return a structured answer with: (1) short direct answer, (2) evidence on supporting infrastructure with citations and locations, (3) evidence on inventory buffers with citations and locations, (4) why both together, (5) limitations.

**Actual search calls:**

- `mcp__corpus__search({"query": "supplier contingency planning supporting infrastructure dependencies utilities transport IT"})`
- `mcp__corpus__search({"query": "safety stock buffer inventory stockpile contingency measure supply disruption"})`
- `mcp__corpus__search({"query": "business continuity plan dependency on power, water, telecommunications, fuel"})`
- `mcp__corpus__search({"query": "community lifelines critical infrastructure restoration after disaster"})`
- `mcp__corpus__search({"query": "just-in-time lean inventory vulnerability holding stock cost trade-off"})`
- `mcp__corpus__search({"query": "stockpiling critical goods government reserves pros and cons"})`
- `mcp__corpus__search({"query": "safety stock reorder point lead time demand variability calculation"})`
- `mcp__corpus__search({"query": "single point of failure node link flow dependency analysis supply chain mapping"})`
- `mcp__corpus__search({"query": "how long can a facility operate without resupply days of supply on hand during outage"})`
- `mcp__corpus__search({"query": "warehouse storage facility power requirements refrigeration cold chain backup generator"})`
- `mcp__corpus__search({"query": "cyber attack IT systems failure disrupting supply chain operations"})`
- `mcp__corpus__search({"query": "diversifying suppliers alternative sourcing mitigation building resilience options"})`
- `mcp__corpus__search({"query": "planning considerations checklist supply chain logistics planning emergency managers section overview"})`
- `mcp__corpus__search({"query": "purpose audience of this guide intended for whom publication date"})`

**Subagent’s actual final answer:**

## 1. Short direct answer

The corpus supports both halves of the question, but from an **emergency-management / national-strategy perspective rather than a retailer's supplier-contingency-plan perspective**.

- Supporting infrastructure matters because supply chain nodes (supplier plants, warehouses, distribution centres) *depend on* separate systems — electric power, fuel, water, wastewater, communications, transport routes — and those dependencies must be analysed separately from the nodes themselves [chunk:5eb1211e45bfca85c0f428708c6f22814858387f625c79382720600af68e5877] [chunk:44fd5ab5603ea338456730c4986a1bed054645f17127fa7aba75425a0ba04088].
- Inventory buffers matter because stock on hand, resupply intervals and stockpiles determine how long demand can be met while the supply chain is broken [chunk:e064861390e58599d4ea3df3aa21d380ed324d7d36ab35a8dbb0bcd74f771f23] [chunk:7e15ca974ecc31f068dd7c8eeca714eacd3110f685dd615c4bb9bae28610f635].

The single clearest "both" statement in the corpus lists them together as parallel mitigation actions: "prioritizing stabilization of critical supply chain infrastructure, reviewing stockpile options, and identifying alternate supply chains for emergencies when needed" (FEMA, PDF page 8) [chunk:7e15ca974ecc31f068dd7c8eeca714eacd3110f685dd615c4bb9bae28610f635].

Corpus sources retrieved: `fema` (a FEMA guide for emergency managers on supply chain resilience, supporting CPG 101), `uk-strategy` (a UK government critical imports / supply chains strategy), `operations` (an open-licensed operations/supply-chain textbook, LibreTexts, CC BY-NC 4.0).

---

## 2. Evidence on supporting infrastructure

**Nodes vs. the infrastructure they depend on — an explicit analytical distinction.**
"Distinguish between the nodes that comprise a supply chain (such as manufacturing facilities and hospitals) and the infrastructure that those nodes depend on (such as electric power, water systems, and transportation). The distinction is important, as the two groups of systems/nodes need analysis from different perspectives." The passage then gives the resilience-gap test: compare a utility's expected restoration time against the node's on-site backup power endurance; "If power restoration recovery time objectives are longer than the length of time that the supply chain node can operate on backup without significant impact to operations, then there is a resilience gap." Source `fema`, PDF page 17 (words 1–334), score 0.742 [chunk:5eb1211e45bfca85c0f428708c6f22814858387f625c79382720600af68e5877].

**Which infrastructure systems to look at.**
"Identify infrastructure systems supporting supply chain operations… emergency managers should identify the infrastructure dependencies of key nodes, along with their physical locations. Utility service providers, their geographic service areas, critical utility system nodes, and transportation routes/mechanisms are especially important… Electric power, refined fuels, natural gas, water, wastewater, and communications are the infrastructure systems most likely to be dependencies." Same passage notes some dependencies are themselves supply chains (diesel, gasoline), and that concentration is high — "It is common for 80 percent of key goods and services serving a densely populated area to depend on seven or fewer distribution centers." Source `fema`, PDF page 16 (words 1–418), score 0.742 [chunk:44fd5ab5603ea338456730c4986a1bed054645f17127fa7aba75425a0ba04088].

**Planning must cover nodes *and* their infrastructure — with a concrete example.**
Analysis "should address both the supply chain nodes (e.g., manufacturing sites, storage facilities, distribution facilities, customers' receiving sites), as well as the infrastructure on which these nodes depend. For example, it is important to include the power infrastructure that provides service to a key tunnel along a main supply route, as without power the tunnel may need to be closed due to inoperable ventilation systems." Source `fema`, PDF page 25 (words 1–391), score 0.804 [chunk:6614699e0c38cab127668bb3b70c0e9a6a07c897a9b561766cbcda55d8faed83].

**Interdependence and cascading failure.**
The Energy, Communications and Transportation lifelines each "support the whole community's response efforts by enabling all other community lifelines," and "secondary supply chain problems can result from broken lifelines. For example, a break in the power grid can lead to a surge in generator and fuel demand," affecting prices and generator supply. Source `fema`, PDF page 12 (words 1–417), score 0.690–0.819 across queries [chunk:1249f85218cdd433d820a070120e6f42b9d4fae9f66e5a73a141601a8a1fd91c].

**Observed cascade (Hurricane Irma, 2017).**
"Resupply of the Miami metropolitan area was complicated by widespread electrical outages and fuel shortages… resupply of groceries and other key resources into Miami required the resupply of fuel and the restoration of electricity or emergency backup to truck stops along Interstate 95." Source `fema`, PDF page 13 (words 1–148), score 0.781 [chunk:04642b373a813ec063289858f22998a8d72c3a812e86df2a3621a95cf66f083f].

**IT/communications specifically.**
Distribution points may have "reliance on automation and information technology" (`fema`, PDF page 26, words 1–342) [chunk:d4b56b31bb8050678949c59a7cb8bb53eaba08ae9a99c9272ac16cc67e8b0dfd]. "Transportation operators often rely heavily on information technology and communications to direct their movements and deliveries. Consider what, if any, plans exist to address loss of these normal capabilities." (`fema`, PDF page 30, words 1–306) [chunk:dbf5419b12b256a798a044d6c7c70126552c09bd8852baf25b7d099b4bbf2745]. On hidden IT dependencies: "a jurisdiction cannot prioritize restoration of a commercial cargo port's cloud-based terminal operating system unless they know the data center that stores it. Not all infrastructure owners know where their offsite data physically resides." (`fema`, PDF page 37, words 1–355) [chunk:8db92c53b3babcf086822a2b0156180458a7f0f5e714aa2aedf04a3af136616c].

**Single points of failure.** On energy service lines: "when a single service line to a key facility identifies a single point of failure" (`fema`, PDF page 36, words 1–324) [chunk:8a49b0dab66844cc109ca4afeda36f835ff00fce73ad173d9d5094c75c00a8f4].

**Policy-level framing (UK).** "The government recognises that critical imports and resilient supply chains are reliant upon a broader business ecosystem effectively functioning. This includes access to finance, energy, skills, infrastructure and transport networks" (`uk-strategy`, Priority 2 / Ensuring a supportive business ecosystem, words 1–37) [chunk:58fcb97f0451b15ebb1b56c35038a1a7949e82cc5604b7d0b80695efcb77d6dd]. "Most supply chains rely upon multiple modes of transport and transfer between modes at ports, airports, rail freight interchanges, and warehousing" (`uk-strategy`, Priority 2 / Transport, words 1–90) [chunk:2eafa302c559dd2c6a9197e4e2653db14afe6f2ec76f7be995c78309e176739d]. The UK has also mapped "global transport route chokepoints… and possible alternative routes to protect supply" (`uk-strategy`, Priority 1 / Building insights and analytical capability, words 1–396) [chunk:aa65dd56e2679597de1a0bf01da8d6361750bfa2e8c8e7de36effde782c696bd].

---

## 3. Evidence on inventory buffers

**Inventory as an explicit contingency planning item.**
"During logistics planning, emergency managers should review standard inventory supply, resupply intervals, storage facilities or compartments and their power requirements, and Just-In-Time restock options during emergency scenarios. Just-In-Time resupply adaptability may mitigate short-term breaks in the supply chain." The same checklist covers invoking "government-managed emergency stockpiles for food, water, and healthcare," reviewing resupply intervals, seasonal influxes, temperature-sensitive stock, and — notably — "secondary power source options… Backup generators. Fuel for the generators." It also flags a downside: "purely commercial interests may adversely harm restoration of the normal supply chain (e.g., hoarding supplies out of concern for shortages, exacerbating the shortages)," and asks of stockpile activation "Will this help or harm recovery of supply chains?" Source `fema`, PDF page 27 (words 1–312), score 0.802 on the logistics-planning query [chunk:e064861390e58599d4ea3df3aa21d380ed324d7d36ab35a8dbb0bcd74f771f23].

**A worked buffer example (Alaska).**
After assessing supply chains that could be "cut off… for several weeks or months," the State "explored procuring shelf-stable meals for 40,000 survivors for seven days… identified the need to store medical supplies, cold-climate water purification systems, and generators," and "Recent catastrophic logistics planning shows that Alaska has seven days of food available following a disruption to the supply chain." Source `fema`, PDF page 8 (words 1–489), score 0.661 [chunk:7e15ca974ecc31f068dd7c8eeca714eacd3110f685dd615c4bb9bae28610f635].

**Fuel stockpiling.** "Fuel access, stockpile, and re-supply procedures are crucial for supply chain recovery… Consider stockpiling emergency fuel. Identify when, how, and who will receive emergency fuel." Source `fema`, PDF page 30 (words 1–306) [chunk:dbf5419b12b256a798a044d6c7c70126552c09bd8852baf25b7d099b4bbf2745].

**Mandated stockpiles at policy level.** "Government requires specific sectors such as defence to maintain stockpiles of goods critical to the provision of national security. MOD has also put in place a £2 million Supply Chain Contingency Fund…" Source `uk-strategy`, Priority 3 / Direct government intervention (words 1–299), score 0.711 [chunk:d2dfd93cc25acc8a00a2cdb17704e86aad332a4b694d9c271d9068d76d7a05df].

**Buffer stock explicitly tied to supplier risk (the closest firm-level statement in the corpus).**
"A manufacturer may carry large amounts of inventory if they have some uncertainty or risk in their supply base. If suppliers have some risk of shortages, work stoppages, poor quality or late deliveries then more stock may be carried." The same passage names the cost side: "Distributors and retailers may try and balance the cost of keeping large inventories on hand with providing excellent customer service," and "inventory may be stored at many locations along the supply chain. This causes extra cost and inefficiencies." Source `operations`, PDF page 54 (words 1–409), score 0.683 [chunk:68f062aa95a04d437f4494a098999edaca20ff91ac03f9df23a71113e72131d8].

---

## 4. Why both together

The corpus supports this connection at three levels, though the explicit "both, because…" argument is partly my synthesis:

1. **Directly stated as paired actions.** Mitigation examples are listed as "prioritizing stabilization of critical supply chain infrastructure, reviewing stockpile options, and identifying alternate supply chains for emergencies" — infrastructure and buffers side by side in one sentence [chunk:7e15ca974ecc31f068dd7c8eeca714eacd3110f685dd615c4bb9bae28610f635] (`fema`, PDF page 8).

2. **Buffers are themselves infrastructure-dependent — so neither works alone.** The inventory checklist requires reviewing "storage facilities or compartments and their power requirements," "temperature-sensitive stock," and "secondary power source options" [chunk:e064861390e58599d4ea3df3aa21d380ed324d7d36ab35a8dbb0bcd74f771f23]. Distribution points may need "cold chain/refrigeration" and IT [chunk:d4b56b31bb8050678949c59a7cb8bb53eaba08ae9a99c9272ac16cc67e8b0dfd]. In Miami, stock existed but could not move without fuel and power at truck stops [chunk:04642b373a813ec063289858f22998a8d72c3a812e86df2a3621a95cf66f083f]. In the FEMA strategic overview, "sources of supply remained sufficient to fulfill survivor needs. But the loss of critical infrastructure, the surge in demand, and limited distribution capabilities… seriously complicated existing distribution capacity" (`fema`, PDF page 3, words 1–437) [chunk:7e63a7958eac84467e6c131bc06d3b1a6ba7a53916bc29ab4240b472761905df]. That is the strongest corpus evidence that inventory alone is not a sufficient contingency.

3. **The duration logic.** FEMA's resilience-gap test compares *how long the infrastructure will be down* against *how long the node can keep operating* — stated for backup power and refuelling endurance [chunk:5eb1211e45bfca85c0f428708c6f22814858387f625c79382720600af68e5877], and expressed in inventory terms by Alaska's "seven days of food available following a disruption" [chunk:7e15ca974ecc31f068dd7c8eeca714eacd3110f685dd615c4bb9bae28610f635]. Infrastructure analysis sizes the *outage duration*; buffers determine the *coverable duration*. **Note: the corpus never states this symmetry for inventory in so many words — FEMA applies the explicit gap test to backup power, not to safety stock. The generalisation to inventory buffers is my synthesis of the two passages above.**

4. **Buffers do not remove the dependency; diversification and infrastructure work address different failure modes.** The corpus treats supplier diversity ("Lack of supplier diversity in critical supply chains presents a risk to resilience", `uk-strategy`, Priority 4, words 1–44 [chunk:b888e0e4411e2e433ce2dffe6f0ea7cda8b0d0c3f6bba8bfe9dea1dc09d149d2]) and stockpiling [chunk:d2dfd93cc25acc8a00a2cdb17704e86aad332a4b694d9c271d9068d76d7a05df] as separate instruments. It also notes buffers can backfire through hoarding [chunk:e064861390e58599d4ea3df3aa21d380ed324d7d36ab35a8dbb0bcd74f771f23] and carry real cost [chunk:68f062aa95a04d437f4494a098999edaca20ff91ac03f9df23a71113e72131d8] — which is why they are not a substitute for fixing dependencies.

---

## 5. Limitations

- **Audience/scope mismatch.** The richest evidence (`fema`) is written for *emergency managers at state/local/tribal/territorial level* working with the private sector, not for a retailer writing supplier contingency plans — its stated purpose is to support CPG 101 emergency operations planning [chunk:c6a0ea2ab63371b4eb8db53f17bbce74c381f309fe462e4102cf14c16f0d2e11] (`fema`, PDF page 7). The `uk-strategy` document is national government policy on critical imports [chunk:9c293a4850dc9b8f563c6e4412fd27de84970864427aa039ad48c148b33db5ed]. Applying either to a single buying organisation's supplier contingency plan is an extrapolation, not something the sources state.
- **No retailer-specific conclusions.** I found nothing in the corpus about any specific retailer, its suppliers, stock levels, supplier performance, current delays, prices or disruption probabilities. The corpus cannot answer those.
- **No safety-stock mechanics.** Searches for safety stock, reorder point and lead-time variability returned no formula or sizing guidance — the operations textbook chunks returned were about forecasting methods (moving averages, exponential smoothing, `operations` PDF pages 38, 41, 43) and inventory turnover / days of supply (`operations`, PDF page 63) [chunk:e93c7311c15da47f4ac8129552099dccbb672593b0b41d2ff942bed3916cf8cd], with scores ~0.63–0.64, i.e. weak and off-target. **The corpus does not support any claim about how large a buffer should be.**
- **"Safety stock" terminology is absent.** The corpus uses "inventory," "stockpile," "days of supply," "buffer" only loosely; the nearest explicit risk-driven buffering statement is the textbook line about carrying more stock when the supply base is risky [chunk:68f062aa95a04d437f4494a098999edaca20ff91ac03f9df23a71113e72131d8].
- **The "why both" framing is partly synthesis.** The corpus lists infrastructure stabilisation and stockpile review together [chunk:7e15ca974ecc31f068dd7c8eeca714eacd3110f685dd615c4bb9bae28610f635] and shows stock being unusable without working lifelines [chunk:7e63a7958eac84467e6c131bc06d3b1a6ba7a53916bc29ab4240b472761905df] [chunk:04642b373a813ec063289858f22998a8d72c3a812e86df2a3621a95cf66f083f]. It does *not* contain a passage that argues "contingency plans must cover both X and Y because…". The duration/gap argument in section 4, point 3 is my inference.
- **Cyber/IT risk is thin.** A targeted cyber-attack search returned no passage on cyber threats to suppliers; top hits (scores 0.67–0.69) were about MOD supply-chain monitoring and transport resilience, not IT failure [chunk:9a47a31ac368fb4cfdd7948d0a3ac800a01ccaedb6354c33aaf2c69dfa724f95]. IT/communications appear only as operational dependencies [chunk:dbf5419b12b256a798a044d6c7c70126552c09bd8852baf25b7d099b4bbf2745] [chunk:8db92c53b3babcf086822a2b0156180458a7f0f5e714aa2aedf04a3af136616c].
- **Supplier-side business continuity plans** are mentioned only as a question to ask — "What plans and capabilities do suppliers have as part of their business continuity plans?" (`fema`, PDF page 26) [chunk:d4b56b31bb8050678949c59a7cb8bb53eaba08ae9a99c9272ac16cc67e8b0dfd]. The corpus gives no template or required contents for a supplier BCP.
- **Dates.** No explicit publication dates appeared in the retrieved chunks. `fema` cites CPG 101 v2.0 (2010) and the FEMA Strategic Plan 2018–2022 and references Hurricane Irma (2017) and Hurricane Maria (2017), so it post-dates 2018. `uk-strategy` cites 2021–2022 survey data and a Q3 2023 trade figure, so it post-dates late 2023. Treat both as potentially out of date relative to today (2026-11-26).
