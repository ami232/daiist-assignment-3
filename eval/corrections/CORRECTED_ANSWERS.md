# Corrected answers

These revised answer artifacts address known failures. They do not replace original benchmark outputs or their grades. Raw provider reruns of q16/q23/q25/q27 are preserved in answers.json; q25/q27 add an explicit sourced inventory-cost tradeoff. q15 is an editorial correction following the full-set judge. No human validation of revised artifacts is claimed.

## q15: Why might a forecast for a product group be more accurate than one for an individual size and colour?

The textbook states that forecasts tend to be more accurate for groups of items than for individual items. Its example compares a model-level forecast with forecasts for each specific colour and size combination. It does not establish a causal or statistical explanation for that difference in this passage. [chunk:7d6a2232a652d08b58b7f65905e29de0a842b4574c42778c5da92d6c306707da]

- [chunk:7d6a2232a652d08b58b7f65905e29de0a842b4574c42778c5da92d6c306707da] operations — PDF page 36; words 1-334

## q16: How should we distinguish a demand trend from a seasonal pattern?

Based on the indexed documents, demand patterns can be distinguished as follows:

* **Trend:** A trend is a consistent upward or downward movement of demand over time, which may be related to a product's life cycle [chunk:7d6a2232a652d08b58b7f65905e29de0a842b4574c42778c5da92d6c306707da].
* **Seasonal pattern:** Seasonal patterns involve generally predictable changes in demand that recur every year, heavily influencing products such as fashion items and sporting goods [chunk:7d6a2232a652d08b58b7f65905e29de0a842b4574c42778c5da92d6c306707da]. 

**Assistant Scope and Limitations:** 
This distinction is based on general definitions from educational operations management literature. The static corpus does not contain retailer-specific inventory, sales history, or demand data, and cannot determine which specific pattern applies to your current products.

- [chunk:7d6a2232a652d08b58b7f65905e29de0a842b4574c42778c5da92d6c306707da] operations — PDF page 36; words 1-334

## q23: Which six types of economic shock does the UK strategy identify?

The UK strategy identifies the following six types of economic shocks:

1. Geopolitical [chunk:30670a6976d49350cf222688974d30b4fbb2d6597fc0710b2e52377f57f3373e]
2. Environmental [chunk:30670a6976d49350cf222688974d30b4fbb2d6597fc0710b2e52377f57f3373e]
3. Financial [chunk:30670a6976d49350cf222688974d30b4fbb2d6597fc0710b2e52377f57f3373e]
4. Health [chunk:30670a6976d49350cf222688974d30b4fbb2d6597fc0710b2e52377f57f3373e]
5. Fiscal [chunk:30670a6976d49350cf222688974d30b4fbb2d6597fc0710b2e52377f57f3373e]
6. Technological [chunk:30670a6976d49350cf222688974d30b4fbb2d6597fc0710b2e52377f57f3373e]

*Assistant scope:* This categorization reflects the government-level framework in the indexed UK strategy document and does not constitute a guarantee against supply-chain disruption or delivery failure for an individual online retailer.

- [chunk:30670a6976d49350cf222688974d30b4fbb2d6597fc0710b2e52377f57f3373e] uk-strategy — section: Priority 3: building the UK’s response to global supply chain shocks / Summary / Spotlight: what is a supply chain shock?; words 1-53

## q25: Combine forecasting assumptions with inventory guidance: why should a stock plan allow for uncertainty instead of assuming a perfect long-range forecast?

Based on the indexed supply chain guidance, a stock plan must allow for uncertainty rather than assuming a perfect long-range forecast for several key reasons:

* **Forecast Imperfection and Error:** Forecasts are rarely, if ever, perfect, and firms need to expect and understand that some error will always exist [chunk:7d6a2232a652d08b58b7f65905e29de0a842b4574c42778c5da92d6c306707da]. 
* **Horizon Decay:** Forecast accuracy decreases as the time horizon increases; the farther away the forecast is from the current date, the more uncertainty it contains [chunk:7d6a2232a652d08b58b7f65905e29de0a842b4574c42778c5da92d6c306707da]. Risk and uncertainty are central to forecasting, making it good practice to indicate the degree of uncertainty attached [chunk:19529a560cf5055ce3f999a71a4c3ad0692a08716e8d45a5c4342c797248db75].
* **Severe Financial and Competitive Consequences of Error:** Overestimating demand can leave a firm with excess costs and cash shortages (such as inability to pay vendors or utility providers, forcing layoffs), while underestimating demand can cause stockouts where competitors capture market share [chunk:19529a560cf5055ce3f999a71a4c3ad0692a08716e8d45a5c4342c797248db75].
* **Challenge of Anticipating Customer Behavior:** Retailers and distributors carry inventory precisely because it is a challenge to anticipate exact customer behavior and balance the cost of holding inventory with providing high customer service [chunk:68f062aa95a04d437f4494a098999edaca20ff91ac03f9df23a71113e72131d8].

*Assistant scope limitation:* Note that this response reflects general principles from the indexed educational text; specific stock levels, carrying costs, and demand patterns for an individual retailer cannot be derived from this static corpus.

Inventory can buffer uncertain demand and supplier shortages or late deliveries, but larger buffers increase holding costs. Balance that cost against service levels rather than treating extra stock as free insurance. [chunk:68f062aa95a04d437f4494a098999edaca20ff91ac03f9df23a71113e72131d8]

- [chunk:7d6a2232a652d08b58b7f65905e29de0a842b4574c42778c5da92d6c306707da] operations — PDF page 36; words 1-334
- [chunk:19529a560cf5055ce3f999a71a4c3ad0692a08716e8d45a5c4342c797248db75] operations — PDF page 31; words 1-600
- [chunk:68f062aa95a04d437f4494a098999edaca20ff91ac03f9df23a71113e72131d8] operations — PDF page 54; words 1-409

## q27: Why should supplier contingency planning consider both supporting infrastructure and inventory buffers?

Supplier contingency planning must consider both supporting infrastructure and inventory buffers because supply chain nodes depend directly on underlying physical and utility systems to function, while inventory and resupply mechanisms determine how long operations can be sustained when those systems are disrupted [chunk:e064861390e58599d4ea3df3aa21d380ed324d7d36ab35a8dbb0bcd74f771f23][chunk:5eb1211e45bfca85c0f428708c6f22814858387f625c79382720600af68e5877]. 

Specifically:
* **Supporting Infrastructure:** Supply chain nodes (such as manufacturing facilities, warehouses, and distribution centers) rely on critical infrastructure systems—including electric power, refined fuels, natural gas, water, wastewater, transportation routes, and communications [chunk:44fd5ab5603ea338456730c4986a1bed054645f17127fa7aba75425a0ba04088][chunk:5eb1211e45bfca85c0f428708c6f22814858387f625c79382720600af68e5877]. Analyzing these dependencies helps identify resilience gaps, such as comparing a utility's estimated recovery time against a facility's on-site backup power and fuel capacity [chunk:5eb1211e45bfca85c0f428708c6f22814858387f625c79382720600af68e5877].
* **Inventory Buffers:** Planning requires reviewing standard inventory supplies, storage facilities (including any specialized power or temperature requirements), resupply intervals, and Just-In-Time restock options [chunk:e064861390e58599d4ea3df3aa21d380ed324d7d36ab35a8dbb0bcd74f771f23]. Inventory buffers and adaptable restock options help mitigate short-term breaks in the supply chain when disruptions occur [chunk:e064861390e58599d4ea3df3aa21d380ed324d7d36ab35a8dbb0bcd74f771f23].

*Assistant Scope & Limitations:* This assistant provides evidence-based logistics guidance drawn from indexed reference documents. It cannot evaluate a retailer’s current inventory levels, specific supplier arrangements, or delivery speeds, and no planning measure can guarantee zero disruption.

The textbook adds that extra inventory can buffer supplier shortages or late deliveries, but must be balanced against the cost of holding stock and the desired customer service level. [chunk:68f062aa95a04d437f4494a098999edaca20ff91ac03f9df23a71113e72131d8]

- [chunk:e064861390e58599d4ea3df3aa21d380ed324d7d36ab35a8dbb0bcd74f771f23] fema — PDF page 27; words 1-312
- [chunk:44fd5ab5603ea338456730c4986a1bed054645f17127fa7aba75425a0ba04088] fema — PDF page 16; words 1-418
- [chunk:5eb1211e45bfca85c0f428708c6f22814858387f625c79382720600af68e5877] fema — PDF page 17; words 1-334
- [chunk:68f062aa95a04d437f4494a098999edaca20ff91ac03f9df23a71113e72131d8] operations — PDF page 54; words 1-409

