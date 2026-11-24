# Answers to grade

Grade at least 20 answers in `eval/human_labels.csv` (`id,correct,supported,notes`) before the judge runs. The judge does not run until 20 grades are there.

- **correct** (1/0): the key figures and facts match the reference (rounding and hedging are fine). Every part of the question must be answered; a partial answer is 0. Unanswerable: 1 only if it says the corpus does not cover it and gives no substitute figure.
- **supported** (1/0): every figure and claim is in the retrieved passages below (not only in the reference or in your memory). A plain refusal is 1.
- **notes**: why, for every 0.

## q01 (single)

**Question:** Approximately how many electric cars were on the road in China at the end of 2025?

**Reference:** Around 44 million electric cars.

**Answer:**

> An estimated 44 million electric cars were on Chinese roads at the end of 2025 (GEVO2026, pp. 18-19). This represented around 13% of the total car stock in China (GEVO2026, pp. 18-19).

**Cited passages (1):**

- `Source: GEVO2026, pp. 18-19 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Close to 55% of new cars sold in China were electric in 2025`

> More than 13 million electric cars were sold in China in 2025, maintaining its position as the world’s largest electric car market, accounting for six out of ten electric cars sold globally. Monthly electric car sales exceeded a 50% sales share in 11 out of 12 months of 2025 – up from only 5 months in 2024. This lifted the electric car sales share to almost 55%. As a result, an estimated 44 million electric cars were on Chinese roads at the end of 2025, representing around 13% of the total car stock, up from 1 in 10 in 2024. Growth in electric car sales in China has been extremely rapid over the past five years: from 2020-24, the annual growth rate in electric cars exceeded 75% and the sales share increased by around 10 percentage points on average each year. By contrast, in 2025, electric car sales grew less than 20% and the sales share rose by only about 6 percentage points. However, China remains by far the largest electric car market and has one of the highest sales shares of any country.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2026, pp. 13-14 | Global EV Outlook 2026 (2026) | Executive summary · Trade plays an important role in the EV industry`

> China remains the world’s largest EV manufacturing hub, accounting for nearly 75% of electric cars produced in 2025. Almost 22 million electric cars were produced globally in 2025 – a more than 25% increase on the previous year. Intense domestic competition in China is squeezing profit margins, pushing manufacturers to seek higher profits overseas. Chinese electric car exports doubled to a record high of over 2.5 million in 2025, as production outstripped domestic demand. In 2024, China overtook the European Union to become the largest exporter of cars; in 2025, more than 35% of China’s car exports were EVs, up from 20% in 2024. Imports from China accounted for 55% of electric car sales in 2025 in countries outside Europe and the United States, up from less than 5% just 5 years earlier. More than half of electric cars sold in Southeast Asia in 2025 were by Chinese brands, while one-third came from a Vietnamese manufacturer.

- `Source: GEVO2026, p. 235 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Rising local EV production in EMDEs and tightening trade policies challenge Chinese imports`

> In 2025, nearly two-thirds of electric car sales in EMDEs other than China were Chinese imports. By 2030, in the STEPS, although Chinese exports to other EMDEs grow more than 70% from 2025 levels, to exceed 1.2 million units, their share in these markets falls below 40%, as local output grows. By 2035, exports to EMDEs could reach around 1.6 million units – one-fifth of China’s total exports – but make up only 25% of total EMDE sales

- `Source: GEVO2025, p. 26 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · Electric car sales are expected to exceed 20 million in 2025, representing one-quarter of total car sales`

> For the full year 2025, electric car sales are expected to increase by 25% globally, which is similar to the growth rate from the 2024. As a result, electric car sales top 20 million worldwide. While sales volumes may be impacted by economic and policy uncertainties, more than one in four cars sold in 2025 is expected to be electric. Building on strong sales in the first quarter of 2025, China is expected to sell over 14 million electric cars across the full year – more than were sold globally in 2023. Sales of both electric and conventional cars are supported by the extension of the trade-in scheme for older vehicles. The sales share of electric cars in China is expected to reach around 60% in 2025. The European Commission announced in March 2025 that OEMs would be given flexibilities in meeting the 2025 CO2 targets for cars and vans. On this basis, OEMs now only need to achieve the 15% emissions reduction target (compared to the 2021 baseline) on average over 2025-2027. This announcement was made in response to auto industry claims that the 2025 target would be unachievable, and would thus incur significant financial penalties that would damage the already struggling European auto industry. As yet, it is unclear how different OEMs will approach meeting the 3-year average target, in terms of the degree of under-performance that could be accepted in 2025 but would then need to be compensated for in the following 2 years.

- `Source: GEVO2025, p. 10 | Global EV Outlook 2025 (2025) | Executive summary · Electric car sales continue to break records globally, particularly in China and other emerging economies`

> Electric car sales exceeded 17 million globally in 2024, reaching a sales share of more than 20%. Just the additional 3.5 million electric cars sold in 2024 compared with the previous year is more than the total number of electric cars sold worldwide in 2020. China maintained its lead, with electric cars accounting for almost half of all car sales in 2024; the over 11 million electric cars sold in China last year were more than global sales just 2 years earlier. As a result of continued strong growth, 1 in 10 cars on Chinese roads is now electric. Europe saw sales stagnate in 2024 as subsidy schemes and other supportive policies waned, but the sales share of electric cars remained around 20% as stronger sales in some countries compensated for lower sales in others. In the United States, electric car sales grew by about 10% year-on-year, reaching more than 1 in 10 cars sold.

</details>

## q02 (single)

**Question:** What proportion of new cars purchased in Southeast Asia in 2025 were electric?

**Reference:** Close to 20% of new car sales in 2025.

**Answer:**

> Across Southeast Asia, electric cars represented close to one in five cars sold, or nearly 20%, in 2025 (GEVO2026, pp. 25-26).

**Cited passages (1):**

- `Source: GEVO2026, pp. 25-26 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · In Southeast Asia, electric car sales more than doubled in 2025`

> In 2025, Southeast Asia saw one of the world’s largest increases in electric car deployment, with sales more than doubling year-on-year to more than half a million. Across the region, electric cars represented close to one in five cars sold. However, trends were uneven: Viet Nam, Indonesia and Thailand led the EV sales growth in the region, supported by strong policy incentives, the expansion of domestic manufacturing and favourable trade conditions for imports, particularly from China. On the other hand, electric sales shares remained somewhat lower in Malaysia and the Philippines, despite growing rapidly. Sales in Viet Nam more than doubled in 2025, promoting the country to Southeast Asia’s largest electric car market, with nearly 40% of new car sales being electric, above levels seen in most European countries. Policy support for electric car purchases has primarily been provided through registration fee exemptions for BEVs since 2022. The domestic EV maker VinFast has captured nearly the entire market, and its small affordable models have been key enablers of mass-market adoption. In 2025, the price-competitiveness of best-selling EV models VF3 and VF5 helped them outsell conventional rivals in similar size segments.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2026, p. 26 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · In Southeast Asia, electric car sales more than doubled in 2025`

> In 2025, electric car sales in Thailand increased by 70% from 2024 levels, reaching roughly 140 000, nearly one-quarter of total new car sales. As a result, the country represented the second-largest electric car market in the region. The EV3.5 scheme that came into force in January 2024 continued to boost adoption through purchase subsidies, excise tax breaks and import duty reliefs. In addition, the EV3.0 scheme drove an increase in Thai-made electric car sales, by requiring manufacturers to register their domestic electric car production before January 2026 in exchange for the import duty exemptions. Thai-made electric cars represented 20% of the market in 2025, up from about 5% the year before. Despite policy settings shifting to support domestic production, Chinese-made electric cars still represented three-quarters of the Thai market in 2025 (see Chapter 7).

- `Source: GEVO2026, pp. 26-27 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · In Southeast Asia, electric car sales more than doubled in 2025`

> In Indonesia, electric car sales more than doubled in 2025, reaching 15% of new car sales. Key policy support measures were VAT and import duty exemptions for battery electric cars. In anticipation of the tariff exemption for battery electric car imports coming to an end in December 2025, manufacturers ramped up imports towards the end of the year, resulting in about half of 2025 sales taking place in the last quarter. About 75% of 2025 sales were imports from China, while the rest were cars produced domestically by Chinese carmakers (mostly by Wuling) – supported by a wide range of manufacturing incentives – and imports from neighbouring countries such as Viet Nam and Thailand. As industrial and trade policies shift the focus towards local production, the importance of imports in Indonesia’s electric car market is set to wane in 2026.

- `Source: GEVO2026, pp. 209-210 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Southeast Asia’s outlook is brightened by strong local manufacturing and EV policies`

> Other Southeast Asian markets are set to continue to rely primarily on registration tax incentives. Viet Nam supports EV adoption through registration fee rebates and already shows strong price competitiveness for electric cars. As a result, sales shares are projected to reach nearly 75% by 2035 in the CPS. Ongoing discussions to extend the rebate end date from 2027 to the end of 2030, amid the oil price pressures resulting from the Middle East crisis, further strengthen uptake in the STEPS, with sales shares exceeding 80% by 2035. Similarly, Singapore focuses on hefty tax exemptions or surcharges to drive its road transport transition, supporting EV sales shares of close to 80% by 2035 in the STEPS, while price premiums constrain uptake in the CPS. Overall, the evolving policy, industry and market landscape across Southeast Asia supports a strong regional outlook. In the STEPS, electric car sales in Southeast Asia reach 40% of total car sales by 2030 and approach 60% by 2035, up from close to 20% in 2025. In the CPS, where policies expire as scheduled and upfront affordability weighs on uptake, sales shares remain lower, standing around 35% by 2035.

- `Source: GEVO2026, p. 12 | Global EV Outlook 2026 (2026) | Executive summary · Policies and affordability will continue to shape the EV outlook in key markets`

> Policies and price dynamics are poised to drive EV sales in particular in Southeast Asia, where the share of electric car sales is projected to increase by up to three times by 2035. Imports of affordable electric cars from China have brought down prices and driven up EV sales in many emerging markets in recent years. For example, in Thailand, electric car prices have been on par with those of ICE cars for the past 2 years. In Indonesia, the average price premium for electric cars declined from over 50% in 2024 to around 40% in 2025. Some countries are looking to tighten import rules to support the development of domestic manufacturing, which may affect affordability in the future. Viet Nam is the only country in the region that has a sizeable domestic EV manufacturer offering EVs at prices comparable to those of ICE cars. As a result, Viet Nam could reach an electric car sales share of over 80%, the highest of any Southeast Asian country in 2035.

</details>

## q03 (single)

**Question:** How many electric cars were sold in India in 2025 and what was their year-on-year growth rate?

**Reference:** 165000 electric cars were sold in 2025, an increase of 75% year on year.

**Answer:**

> Electric car sales in India increased by 75% year-on-year in 2025 to reach 165,000, representing nearly 4% of total car sales (GEVO2026, pp. 27-28).

**Cited passages (1):**

- `Source: GEVO2026, pp. 27-28 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales in India remain modest but are starting to pick up`

> Despite being the second-largest car market in the Asia Pacific region, India’s electric car sales remained below levels seen in Viet Nam and Thailand. However, sales started to pick up in 2025, increasing 75% year-on-year to reach 165 000, representing nearly 4% of total car sales. Roughly 60% of electric car sales were produced in India by domestic automakers Tata and Mahindra. Mahindra introduced two new electric models in 2025, and saw electric car sales increase fivefold compared to 2024. Besides local automakers building up sales, more brands started to sell electric cars in India, with the number of electric models available increasing from 33 to 45 between 2024 and 2025. Following the announcement by the Indian government in 2024 of the Scheme to Promote Manufacturing of Electric Passenger Cars in India (SPMEPCI), the final requirements were announced in June 2025. The SPMEPCI will allow selected automakers to import higher-priced CBUs at a minimum import value of USD 35 000 with a reduced import rate of 15%, compared with duties of up to 110% for non-eligible imports, for a period of five years. While several automakers expressed interest, decisions to participate were delayed in 2025, with companies citing uncertainty related to the ongoing European Union-India free trade agreement negotiations and Chinese restrictions on rare-earth magnet exports, which raised concerns about meeting the scheme’s localisation requirements.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2026, p. 45 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales are expected to grow 10% in 2026, but uncertainties are high`

> Market and policy fundamentals for 2026 point towards growth in electric car sales, but data on low sales figures in the first quarter of 2026 suggest that the rate of growth is likely to be more moderate than previously expected. China has scaled back incentives, and in the United States, manufacturers are reassessing electrification strategies. In Europe and Southeast Asia, demand is being driven by a combination of policy action and the improving affordability of electric cars. Overall, global electric car sales are expected to reach around 23 million, representing growth of approximately 10%.

- `Source: GEVO2026, pp. 204-205 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · India’s EV policy support targets commercial fleets, as electrification of 2/3-wheelers and cars gains momentum`

> Although India does not offer direct purchase subsidies for electric cars, it supports their adoption through other measures, primarily various tax reductions. India also promotes domestic EV and battery production through Production Linked Incentive schemes for the automotive and battery industries. In addition, the government also has a plan to attract global EV manufacturers to invest in electric car manufacturing in India (see Chapter 7). Recent market dynamics show strong momentum, with electric car sales in India increasing by around 80% last year and reaching a 4% sales share for the first time in 2025. The increasing momentum and improving affordability of electric cars continues in the STEPS, with electric LDVs reaching a sales share of nearly 25%, or over 2 million cars and vans, by 2035 in this scenario, up from 3% in 2025, with nearly all EV sales being BEVs – in line with historical trends. In the CPS, the share increases only slightly to 5% by 2035 as EV policies are not assumed to continue after their specified periods, and deployment of charging infrastructure struggles to expand.

- `Source: GEVO2026, p. 11 | Global EV Outlook 2026 (2026) | Executive summary · Electric cars are poised to make up a greater share of total car sales in 2026`

> Global electric car sales are expected to grow to 23 million in 2026, representing 28% of total car sales. Europe is poised for the largest growth among major markets, with sales projected to increase by around 20% in 2026, such that one in three cars sold are electric. In China, electric car sales are set to grow across 2026, albeit at a slower rate than in previous years, to reach almost 60% of total car sales. Sales across Asia Pacific countries other than China are expected to grow by over 50%, while sales in Latin America are projected to rise by 45%. The wider economic impacts of the conflict in the Middle East might temper overall car sales. In many regions, however, there is upside potential to the 2026 EV forecast depending, in part, on how, when and which policies are enacted amid the current energy crisis.

- `Source: GEVO2026, p. 205 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · India’s EV policy support targets commercial fleets, as electrification of 2/3-wheelers and cars gains momentum`

> Across all vehicle modes, excluding 2/3Ws, EVs represent 1 in 4 vehicles sold in India in 2035 in the STEPS, up from less than 1 in 30 in 2025. In the CPS, 1 in 20 vehicles sold is electric by 2035. When 2/3Ws are included, stated policies imply that almost every second vehicle sold by 2035 is electric. In the CPS, the share reaches 15% by 2035.

</details>

## q04 (single)

**Question:** Under the Current Policies Scenario and the Stated Policies Scenario, what share of new car and van sales in China is projected to be electric by 2035?

**Reference:** Electric cars and vans are projected to account for more than 90% of new car and van sales in China by 2035 in both scenarios.

**Answer:**

> Under both the Current Policies Scenario (CPS) and the Stated Policies Scenario (STEPS), electric cars and vans in China are projected to reach more than 90% of total sales by 2035 (GEVO2026, p. 196).

**Cited passages (2):**

- `Source: GEVO2026, p. 196 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Vehicle outlook by region`

> In the CPS and STEPS, electric cars and vans reach more than 90% of total sales by 2035, up from close to 55% in 2025. This trajectory is supported by continuous improvements in affordability and by policy frameworks that continue to tighten. In the short term, the new energy vehicle (NEV) credit target under the Dual Credit System will rise from 38% in 2025 to 58% in 2027, further encouraging manufacturers to electrify their line-ups. Long-term industry commitment is underscored by the China Society of Automotive Engineers’ Industrial Roadmap 3.0, which sets EV sales shares targets for new LDVs of at least 80% by 2035 and 85% by 2040. To ensure that charging infrastructure grows in line with EV uptake, the government has announced a 3-year plan for 2025-27 to meet the demand of more than 80 million EVs by end of 2027, prioritising faster chargers, expanding charging in rural areas and improving vehicle grid integration. In addition to direct supply and demand-side measures supporting EV deployment, China’s 15th Five-Year Plan emphasises enhancing energy security through diversification away from fossil fuels, supports system-wide electrification and the construction of zero-emission transportation corridors. Over the past decade, sales of electric 2/3Ws have grown significantly, and by 2025, 50% of 2/3Ws were electric. In the STEPS, continued momentum, combined with further declines in battery prices, pushes the electric share of the 2/3W sales share close tor 95% by 2035.

- `Source: GEVO2026, pp. 196-197 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Vehicle outlook by region`

> The EV sales share across all vehicle types in China reaches over 90% by 2035 in both the CPS and the STEPS. This aligns with China’s priorities to reduce fossil fuel imports, enhancing energy security, while also delivering co-benefits for air pollution reduction and supporting climate neutrality by 2060.

<details><summary>Other retrieved passages (3)</summary>

- `Source: GEVO2026, p. 235 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Rising local EV production in EMDEs and tightening trade policies challenge Chinese imports`

> In 2025, nearly two-thirds of electric car sales in EMDEs other than China were Chinese imports. By 2030, in the STEPS, although Chinese exports to other EMDEs grow more than 70% from 2025 levels, to exceed 1.2 million units, their share in these markets falls below 40%, as local output grows. By 2035, exports to EMDEs could reach around 1.6 million units – one-fifth of China’s total exports – but make up only 25% of total EMDE sales

- `Source: GEVO2026, p. 201 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · European policies continue to support the transition to EVs, while introducing some flexibilities`

> Electric car sales also rise in the rest of Europe on aggregate, on the back of impressive momentum in large markets such as Türkiye. Although support varies a lot at the national level, strong policies in some countries drive Europe’s sales share of electric cars and vans to around 90% in 2035 in the CPS and close to 85% in the STEPS, up from around 25% today.

- `Source: GEVO2026, pp. 228-229 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Special focus: Manufacturing and trade outlook for electric cars and batteries`

> However, diversification remains limited, with China still the largest source of demand and production in 2035. By then, it supplies nearly 90% of AAM, about three-quarters of CAM and two-thirds of batteries. Most diversification is driven by advanced economies, accounting for almost 10% of AAM, 20% of CAM and about 25% of battery output in 2035, with the European Union and United States together providing almost 10% of CAM and 20% of battery production. EMDEs other than China produce nearly 5% of AAM and CAM by 2035, and increase their battery and electric car output share to about 6% and 10% respectively – about six and five times their 2025 shares. Electric car production also rises in advanced economies, reducing China’s share to just below 60% in 2035. Nevertheless, while EV production expands in advanced economies, the share of demand met by domestic manufacturing does not increase. Despite more stringent trade measures, such as EU countervailing duties on Chinese-made battery electric cars, tariff reinstatements in Brazil and Mexico and new levies in Türkiye, Chinese exports continue to dominate global trade by 2035 in the STEPS. With unmatched capacity and low production costs across the EV supply chain, China’s exports are projected to grow, with over one in four electric cars sold in advanced economies made in China by 2035 (6 million) – up from 15% (just over 900 000) in 2025.

</details>

## q05 (single)

**Question:** Under the Stated Policies Scenario, how much annual EV battery deployment is projected worldwide in 2030 and 2035?

**Reference:** Annual global EV battery deployment is projected to reach almost 3 TWh in 2030 and almost 5 TWh in 2035.

**Answer:**

> Under the Stated Policies Scenario (STEPS), worldwide EV battery deployment is projected to reach almost 3 TWh in 2030 and almost 5 TWh in 2035 (GEVO2026, p. 220).

**Cited passages (1):**

- `Source: GEVO2026, pp. 220-221 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · EV battery deployment more than triples by 2035`

> Global EV battery demand grows strongly as EV sales continue to expand, including in emerging markets. By 2030, EV battery deployment is expected to reach almost 3 TWh in both the CPS and STEPS, up from around 1.2 TWh in 2025. By 2035, deployment rises further, reaching around 4 TWh in the CPS and almost 5 TWh in the STEPS. To put this in perspective, on average, a single month of EV sales in 2035 would exceed the entire annual deployment of 2021. Electric cars continue to drive EV battery demand, but the importance of other modes, and particularly of electric trucks, is expected to grow. In both the CPS and STEPS, electric trucks are projected to account for around 10% of total EV battery deployment in 2030 and 2035, up from 8% in 2025. The gap between current and stated policies and the NZE Scenario is significant, with EV battery deployment reaching around 9 TWh by 2035 in the NZE Scenario – almost double the level in the STEPS that same year.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2026, p. 221 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · EV battery deployment more than triples by 2035`

> China, the European Union and the United States are expected to remain the main drivers of EV battery deployment, but their combined share is set to decline over the coming years as deployment in EMDEs grows. In the STEPS, the share of EMDEs in global EV battery deployment rises from around 6% in 2025 to about 15% by 2035, driven primarily by EV uptake in Southeast Asia, India and Latin America. In contrast, the United States sees the sharpest decline in share under the CPS, falling from around 10% in 2025 to less than 5% in both 2030 and 2035, reflecting slower growth relative to other markets.

- `Source: GEVO2026, pp. 199-200 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · European policies continue to support the transition to EVs, while introducing some flexibilities`

> Maximum amount of “low-carbon” crude steel demand implied by the proposed Automotive Package, near-zero emissions steel demand commitments and announced projects in the European Union Current publicly announced demand commitments and offtake agreements for near-zero emissions steel in the European Union amount to almost 6 Mt, of which around 1 Mt is linked to automotive manufacturers and suppliers. However, the majority of agreements have been signed without publicly disclosed volumes, and so actual demand could be higher. The proposed Automotive Package therefore has the potential to expand demand for “low-carbon” steel for this industry beyond current commitments. However, the final impact of the proposed package in de-risking “low-carbon” steel projects remains uncertain. In the low-demand case, which considers the more stringent end-point emissions intensity, the estimated induced demand for “low-carbon” steel exceeds the roughly 6 Mt of near-zero emissions steel capacity currently announced in the European Union. In the high-demand case, the package could stimulate demand at a scale sufficient to support the advancement of a broader pipeline of projects, including some currently at earlier stages of development. However a more lenient threshold for “low-carbon” steel that would increase the volume of steel eligible for credits, – while delivering the same emissions reductions – could weaken the business case for more innovative projects deploying deep decarbonisation technologies.

- `Source: GEVO2026, pp. 92-93 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Electric vehicle battery deployment grew by almost 30% in 2025`

> Electric vehicles (EVs) remained the primary source of global battery deployment, accounting for more than 70% of the total in 2025, slightly down from almost 80% in 2024. In 2025, EV battery deployment reached 1.2 TWh, an increase of almost 30% compared to 2024, and more than 7 times greater than in 2020. Light-duty vehicles remained the dominant segment, representing more than 85% of the 2025 EV battery deployment. However, the fastest growth came from electric trucks, for which battery demand more than doubled – largely thanks to a sharp acceleration in sales in the People’s Republic of China (hereafter, “China”) (see One in four trucks sold in China in 2025 was electric). As a result, electric trucks accounted for about 8% of global EV battery deployment in 2025, up from less than 5% in 2024. Regionally, EV battery deployment expanded in China (60% of global) and the European Union (almost 15%) in 2025, while it stagnated in the United States (10%). Growth in emerging markets and developing economies (EMDEs) other than China also continued – they represented 6% of global EV battery deployment in 2025, highlighting the increasingly global nature of road transport electrification.

- `Source: GEVO2026, pp. 235-236 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Global battery project pipeline largely meets 2030 demand`

> The committed battery project pipeline is sufficient to meet global deployment needs by 2030 across all regions, with substantial short-term overcapacity projected in China and the United States. Although building manufacturing capacity is only the first step – new facilities can take more than 5 years from the start of operations to near nominal output – the pipeline remains robust, indicating that producers are well positioned to supply the batteries needed for transport electrification and for stationary storage systems supporting power grids worldwide. Among all regions, Chinese, Korean and Japanese producers are expected to remain the dominant players in battery manufacturing through this decade, although Japan’s global share of installed battery manufacturing capacity is expected to decline based on current project announcements.

</details>

## q06 (single)

**Question:** Approximately how many electric car models were available worldwide in 2025 and what share of all available car models did they represent?

**Reference:** Nearly 1000 electric car models, representing about 40% of all available car models in 2025.

**Answer:**

> Nearly 1 000 electric car models were available worldwide in 2025, representing about 40% of all available car models (GEVO2026, pp. 32-33).

**Cited passages (1):**

- `Source: GEVO2026, pp. 32-33 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · The number of electric car models keeps growing, in contrast to conventional car models`

> Some 2 500 car models were available worldwide in 2025. Nearly 1 000 of these were electric cars, about 40% of the total, up from about 35% in 2024. Counting both battery electric and plug-in hybrid electric models, the number of electric car models has more than doubled in the past five years. In 2025, the number of electric car models available worldwide increased by slightly more than 25%, a larger increase than the just over 15% seen in 2024. Hybrid model availability also continued to expand, rising by over 10% year-on-year to more than 200 models in 2025. By contrast, the number of internal combustion engine (ICE) car models remained constant in 2025 – the only powertrain category to do so. The total number of electric car models could exceed 1 100 in 2026, based on recent original equipment manufacturer (OEM) announcements, growing at around 15% compared to the previous year. BEVs continue to account for around 65% of all electric car models, a share that has remained broadly stable since 2015. Looking forward, the share of PHEVs in total electric car models is expected to decline from around 35% in 2026 to around 30% by the end of the decade.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2025, pp. 39-40 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Available electric car models could number more than 1 000 by 2026`

> The number of available models for electric cars increased 15% year-on-year to reach nearly 785 in 2024. While today there are 50% fewer electric models than ICE and hybrid electric vehicle (HEV) models, this gap is narrowing and is expected to shrink to around 30% by 2027 based on announcements by OEMs. While its EV sales share remained largely unchanged, Europe saw the fastest increase in model availability over the past year, with a jump from 290 models to more than 360. The growth seen in 2024 is expected to almost double by 2026: As stricter emissions standards come into force in the European Union, more than 140 additional models are due to enter the market. For example, Volkswagen and Stellantis have announced plans to introduce about 35 new electric models between them by 2026. The share of larger cars and SUVs among EV models coming onto the market continues to expand. In 2024, 70% of available EV models were large (segments E to F) cars, SUVs or pick-ups, compared to 65% in 2023. Nevertheless, there are signs that this share is levelling out in some markets. In Europe, 23 additional small electric models (segments A and B) are expected to join the 33 small models currently on the market. The United States has the lowest number of small electric models available, and nearly 90% of models available today are large cars or SUVs.

- `Source: GEVO2026, p. 37 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Just five models represent around 20% of global battery electric car sales`

> While model availability shapes consumer choice, greater availability is not necessary reflected in EV purchase decisions; instead, buyers often tend to pick one of a relatively small number of very popular models. In 2025, 630 battery electric car models were available globally, yet sales remained highly concentrated across a small group of best-selling models. In 2025, just five models accounted for about 20% of global battery electric car sales: the Tesla Model Y made up nearly 8% of total battery electric car sales, followed by the Tesla Model 3 (3.6%), Geely Geome Xingyuan (3.5%), Wuling HongGuang Mini (3.1%), and BYD Seagull (3.0%). As a result, just 1% of available BEV models captured one-fifth of the entire global market. The top-selling 35 models accounted for around half of global battery electric car sales. Nevertheless, as EV adoption grows, automakers tend to offer a greater range of electric car models, which leads to a diversification of consumer choice. As recently as 2020, only two models accounted for about 20% of global battery electric car sales. Sales are also concentrated in terms of where their manufacturers are headquartered. Chinese manufacturers accounted for more than half of the total BEV models available, and of global BEV sales in 2025. Manufacturers headquartered in Europe accounted for nearly one-fifth of models sold, followed by those based in United States, which made up nearly 10% (see Chapter 7 for the latest manufacturing and trade trends).

- `Source: GEVO2026, p. 34 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Model availability continues to shift towards larger vehicle segments`

> In China, growth in the number of electric car models, especially large models, was the main driver of an expansion in car model availability last year. The total number of available car models increased by around 10% in 2025 to more than 1 100, while the number of electric models increased around 25%. As of the end of 2025, there were nearly 700 electric car models available, 60% more than the number of conventional car models. Among major global automotive markets, such as China, Europe, the United States and Japan, China is the only market with more electric than conventional models, reflecting that competition among Chinese OEMs is increasingly focused on EVs. Despite the number of large and SUV EV models growing over 25% in 2025 in China, their share of total electric car sales only increased by one percentage point, to reach more than 60%, although 2025 sales were 25 percentage points higher than 2020 levels. Among the three major electric car markets, Europe recorded the fastest growth in electric car model availability in 2025. The total number of electric car models increased by nearly 35%, reflecting an uptick in model launches ahead of the introduction of the more stringent 2025 EU CO2 target. At the same time, Europe continued to have the highest number of conventional car models available, with 580 ICE models and nearly 100 hybrid models in 2025. Large cars and SUVs accounted for almost three-quarters of EV and conventional vehicle models in

- `Source: GEVO2026, pp. 35-36 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Model availability continues to shift towards larger vehicle segments`

> 2025. However, the availability of small EVs in Europe has improved significantly in recent years and is set to expand further in response to upcoming EU policy developments (see Box 1.1). The United States has the highest share of large models within its EV line-up: over 85% of electric models are large cars or SUVs, compared with roughly three-quarters in Europe and China. This is also reflected in sales, with large cars and SUVs accounting for over 80% of all car sales in the United States. Among all available car models in 2025, ICE models accounted for about 60%, electric for nearly 30%, and hybrid around 10%. Compared to 2024, model availability across ICEs, EVs and HEVs remained broadly unchanged in 2025. This follows recent policy changes and past uncertainty around fuel economy and emissions standards. Box 1.1 Small, affordable battery electric cars gain traction amid EU policy shifts Since 2024, against the backdrop of evolving EU CO2 emission targets, carmakers have added more affordable battery electric car models to their line-ups to enable wider adoption and comply with the increasing stringency of emission targets. A handful of small, mass-market models have entered the EU market, including Renault’s 4 and 5, Hyundai’s Inster, BYD’s Seagull and Leapmotor’s T03. As a result, the sales share of small battery electric cars increased in 2025 – reversing five years of declining shares – and capturing nearly one-tenth of the electric car market.

</details>

## q07 (single)

**Question:** What was the approximate global average driving range of battery electric cars in 2025?

**Reference:** Almost 380 kilometres.

**Answer:**

> The global average range of battery electric cars is almost 380 km (GEVO2026, p. 38).

**Cited passages (1):**

- `Source: GEVO2026, p. 38 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · The average range of battery electric cars is plateauing`

> Vehicle range remains one of the key considerations for potential electric car buyers. The average battery electric car range is currently almost 380 km, and this has plateaued in recent years. The average range of small and medium-sized cars increased by about 7% and 5% in 2025, but global electric car sales have become increasingly concentrated in larger segments, with large cars and SUVs accounting for almost 70% of the global EV market in 2025. Sales-weighted battery electric car range rose by roughly 10% between 2020 and 2025. At the same time, public charging infrastructure has expanded rapidly, including along long-distance corridors, helping to reduce range anxiety. As electric car markets partially shifted from high-income early adopters to include a wider range of consumers, including those with lower incomes, the greater availability of affordable, shorter-range models in electric car sales contributed to the plateauing of global average driving ranges. This may indicate a consumer or carmaker preference to balance range with overall vehicle costs. Extending vehicle range by increasing battery capacity involves trade-offs. Larger battery packs can increase vehicle weight, partly offsetting gains in range, and cost. As charging infrastructure expands and fast-charging battery capabilities improve, incremental increases in battery size yield diminishing returns.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2025, p. 44 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · No change to average range of battery electric cars in 2024`

> The sales-weighted average range (hereafter, “average range”) of battery electric cars globally remained the same in 2024, at about 340 km under on-road conditions. The average range was significantly lower for small cars, at just above 150 km, while medium and large cars, as well as SUVs, all maintained ranges above 350 km. As market competition intensifies, the fact that average range has stabilised in the past year could indicate that carmakers have found an optimal balance between range performance and vehicle manufacturing costs. This levelling-off of driving range also offers energy and environmental benefits, as longer ranges also require larger batteries, which increase vehicle energy consumption and demand for critical minerals. In the United States and Europe, the average electric range increased by less than 5%, primarily driven by the growing interest in electric SUVs, which continued to dominate the EV market – exceeding 75% of sales in the United States and reaching around 60% in Europe. Across Europe, the average range of a battery SUV car reached almost 400 km under on-road conditions. Nevertheless, this falls short of the 500 km that respondents to a recent survey stated as their range preference. Meanwhile, in China, the average range remained stable as EV producers prioritised cost-cutting in the face of strong domestic competition.

- `Source: GEVO2026, p. 39 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Today’s average range can accommodate the vast majority of daily driving needs`

> In many markets, average daily driving distances are around 40 km, equivalent to roughly one-tenth of the average battery electric car range. Daily driving needs are higher in some markets – for example, the average daily driving distance in the United States is around 65 km. Even for more intensive use cases, battery electric car ranges are sufficient for daily needs. Taxi drivers’ typical distances, which average between 150 and 250 km per day, are roughly half of the average battery electric car driving range. There is a clear relationship between battery electric car price and driving range. Lower-priced models generally have smaller batteries and thus offer shorter ranges, while longer-range vehicles tend to sit at the higher end of the price spectrum. Nevertheless, cost is not purely range-driven, as other features increasingly shape model positioning. In recent years, carmakers have also focused on software capabilities, charging speed and autonomous driving functions to attract new consumers (see Chapter 8).

- `Source: GEVO2026, p. 93 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Electric vehicle battery deployment grew by almost 30% in 2025`

> In 2025, the average battery size of batteryelectric cars remained broadly stable in the European Union and China, at close to 70 kWh and below 60 kWh, respectively. By contrast, average plug-in hybrid electric car battery sizes increased by almost 10% in China, to reach more than 25 kWh, and by almost 15% in the European Union, reaching just over 20 kWh. In the United States, average battery sizes for both batteryelectric and plug-in hybrid electric cars grew at a similar pace of around 5%, reaching 90 kWh for batteryelectric cars and less than 20 kWh for plug-in hybrid electric cars.

- `Source: GEVO2026, pp. 16-17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> The electric car market reached new highs in 2025, growing by 20% from 2024 to exceed 20 million sales, in line with expectations in the 2025 edition of the Global EV Outlook. The sales share of electric cars in the overall car market increased to 25%. This marked the fifth consecutive year in which annual electric car sales increased by about 3.5 million, a trend that began in 2021 after the Covid-19 pandemic. As a result, about 5% of the global car stock is now electrified, displacing 1.2 million barrels of oil per day in 2025 (see Annex A). In particular, 2025 saw a boost for battery electric cars. The share of battery electric cars in total electric car sales increased to 65%, reversing the trend seen in the 2 years prior. While 2024 saw a strong increase in extended-range electric vehicles (EREVs), this did not continue in 2025, dropping to less than 7% of total electric car sales, after rising to 7.5% in 2024.

</details>

## q08 (single)

**Question:** Before government incentives were applied, what share of battery electric cars sold in China in 2025 were cheaper than comparable conventional cars?

**Reference:** Nearly 70% of battery electric cars sold in China in 2025.

**Answer:**

> In 2025, nearly 70% of battery electric cars sold in China were cheaper than their internal combustion engine equivalents even before government incentives (GEVO2026, p. 51).

**Cited passages (2):**

- `Source: GEVO2026, p. 51 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · In China, the price-competitiveness of electric cars continued to grow`

> Looking ahead, intense price competition in China’s electric car market is likely to persist. In 2026, tighter policy support – including reduced purchase tax exemptions and stricter trade-in incentives – is expected to increase price pressure on carmakers. However, in most cases, affordability is no longer dependent on policy support: in 2025, even before government incentives, nearly 70% of BEVs sold in China were already cheaper than their ICE equivalents, up from around 50% in 2021.

- `Source: GEVO2026, pp. 50-51 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · In China, the price-competitiveness of electric cars continued to grow`

> In China, the price-competitiveness of electric cars made major progress in all segments. Most noticeably, the affordability of small electric models displaced essentially all ICE alternatives in the small-sized car market in 2025. Medium-sized cars, accounting for nearly 30% of new car sales, remained the most difficult segment to electrify. Their diverse uses, from daily commuting to longer-distance travel, limit opportunities for cost reductions through smaller batteries, while their market positioning constrains the ability to justify higher price premiums, unlike larger SUVs. Despite this, their relative affordability improved significantly in 2025, with the average price premium paid for a battery electric model falling below 15%, down from about 20% the previous year. As a result, electric models exceeded a 40% sales share in this segment, although this remained the lowest adoption rate across all car sizes in China. In the SUV segment, which accounted for almost half of all car sales in 2025, BEVs reached price parity with ICE models for the first time. Plug-in hybrid SUVs remained cheaper than their ICE equivalents, although extended-range electric SUVs continued to sell at a roughly 60% premium, reflecting their higher-end positioning. Improved price-competitiveness contributed to rapid electrification in this segment, with adoption rates over 55% in 2025, albeit contributing to the shift of Chinese electric cars towards larger and heavier vehicles.

<details><summary>Other retrieved passages (3)</summary>

- `Source: GEVO2025, p. 51 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Price-competitive electric cars in China are driving rapid electrification across all segments`

> Electric car affordability improved in all car segments in China thanks to falling battery pack prices, a high level of supply chain vertical integration and fierce competition within the Chinese EV market. Overall, in 2024, close to two-thirds of the battery electric cars sold in China were cheaper than their ICE equivalents, up from half in 2021 and just 10% in 2018.

- `Source: GEVO2026, pp. 64-65 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · Tax exemptions dominate government support in China but will tighten from 2026`

> Government spending in China accounted for nearly 60% of the global total in 2025. Scrappage and trade-in schemes were largely continued in 2025, with 18.3 million applications filed in 2024 and 2025, accounting for nearly 40% of car sales over the same period. The 10% purchase tax exemption for electric cars remains the primary source of government financial support for buyers. In 2025, the purchase tax exemption represented more than 90% of Chinese government support, in the form of foregone revenue. However,starting from January 2026, policy updates reducing access to new energy vehicle (NEV) purchase incentives are expected to significantly reduce government spending. Firstly, the preferential purchase tax policy for NEVs entered a new phase in 2026, in which the full exemption has been replaced with a 50% tax reduction, linked to vehicle energy consumption for BEVs and electric range for PHEVs, reducing both the scope of eligibility and levels of support. Similarly, trade-in and scrappage schemes are moving away from a fixed subsidy amount to price-capped and energy-efficiency-linked incentives, further reducing per-vehicle government spending in 2026.

- `Source: GEVO2026, pp. 60-61 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · Resale values in China are taking a hit from new, cheaper models`

> In 2024, the levels of electriccar resale value retention were lower than the overall levels in China – about 46% for 3-year-old electric cars, compared to around 55% across the broader usedcar market. By late 2025, average BEV and PHEV resale values had fallen to 42%, a similar percentage point decrease as in the overall used car market, where levels declined to just above 50%. There are several reasons for the difference in depreciation rates between electric and ICE cars in China. Rapid advances in battery technology have quickly made newer electric models far more attractive, accelerating the depreciation of older electric cars. While electric cars generally require less routine maintenance than conventional cars, concerns about battery health and the potential cost of major repairs make the purchase of an older electric car less appealing. So much so that it is estimated that around 80% of usedcar dealers in China now refuse to accept BEVs that are more than 5 years old.

</details>

## q09 (single)

**Question:** How much battery capacity was deployed in electric vehicles worldwide in 2025 and how much did deployment grow from 2024?

**Reference:** Global EV battery deployment reached 1.2 TWh in 2025, growing by almost 30% from 2024.

**Answer:**

> Global electric vehicle battery deployment reached 1.2 TWh in 2025 (GEVO2026, p. 92). Deployment grew by almost 30% compared to 2024 (GEVO2026, p. 92).

**Cited passages (1):**

- `Source: GEVO2026, pp. 92-93 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Electric vehicle battery deployment grew by almost 30% in 2025`

> Electric vehicles (EVs) remained the primary source of global battery deployment, accounting for more than 70% of the total in 2025, slightly down from almost 80% in 2024. In 2025, EV battery deployment reached 1.2 TWh, an increase of almost 30% compared to 2024, and more than 7 times greater than in 2020. Light-duty vehicles remained the dominant segment, representing more than 85% of the 2025 EV battery deployment. However, the fastest growth came from electric trucks, for which battery demand more than doubled – largely thanks to a sharp acceleration in sales in the People’s Republic of China (hereafter, “China”) (see One in four trucks sold in China in 2025 was electric). As a result, electric trucks accounted for about 8% of global EV battery deployment in 2025, up from less than 5% in 2024. Regionally, EV battery deployment expanded in China (60% of global) and the European Union (almost 15%) in 2025, while it stagnated in the United States (10%). Growth in emerging markets and developing economies (EMDEs) other than China also continued – they represented 6% of global EV battery deployment in 2025, highlighting the increasingly global nature of road transport electrification.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2026, pp. 220-221 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · EV battery deployment more than triples by 2035`

> Global EV battery demand grows strongly as EV sales continue to expand, including in emerging markets. By 2030, EV battery deployment is expected to reach almost 3 TWh in both the CPS and STEPS, up from around 1.2 TWh in 2025. By 2035, deployment rises further, reaching around 4 TWh in the CPS and almost 5 TWh in the STEPS. To put this in perspective, on average, a single month of EV sales in 2035 would exceed the entire annual deployment of 2021. Electric cars continue to drive EV battery demand, but the importance of other modes, and particularly of electric trucks, is expected to grow. In both the CPS and STEPS, electric trucks are projected to account for around 10% of total EV battery deployment in 2030 and 2035, up from 8% in 2025. The gap between current and stated policies and the NZE Scenario is significant, with EV battery deployment reaching around 9 TWh by 2035 in the NZE Scenario – almost double the level in the STEPS that same year.

- `Source: GEVO2026, pp. 235-236 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Global battery project pipeline largely meets 2030 demand`

> The committed battery project pipeline is sufficient to meet global deployment needs by 2030 across all regions, with substantial short-term overcapacity projected in China and the United States. Although building manufacturing capacity is only the first step – new facilities can take more than 5 years from the start of operations to near nominal output – the pipeline remains robust, indicating that producers are well positioned to supply the batteries needed for transport electrification and for stationary storage systems supporting power grids worldwide. Among all regions, Chinese, Korean and Japanese producers are expected to remain the dominant players in battery manufacturing through this decade, although Japan’s global share of installed battery manufacturing capacity is expected to decline based on current project announcements.

- `Source: GEVO2026, p. 15 | Global EV Outlook 2026 (2026) | Executive summary · Technology advances and AI are reshaping the automotive industry, led by the EV industry`

> Technological advances are improving EV charging times and creating opportunities to reduce peak demand on the grid. New power-electronics materials, battery cell technologies and battery pack architectures are enabling charging systems that are more efficient, higher voltage – and therefore faster. The first 1 000-volt models came out in 2025, and announcements of charging times of under 10 minutes have continued into 2026. The number of electric cars able to use chargers above 250 kW represents less than 5% of the vehicle stock, but sales are growing alongside the expansion of ultra-fast and megawatt-scale chargers. As EV deployment and charging speeds increase, grid capacity constraints could become more pronounced in some regions. With no change to current policies, electricity demand from EVs could exceed 1 500 TWh by 2035 – growing around sixfold from 2025 levels. While impressive, this would increase total global electricity demand in 2035 by only about 4%. The impacts vary by region: across Europe, EV deployment in road transport increases total electricity demand by more than 10% in 2035, compared with an increase of under 6% in China. Measures such as smart charging, which reduces peak demand by shifting charging loads, or vehicle-to-grid (V2G) – which allows EVs to feed electricity back to the grid – can offer additional flexibility. The first commercial offers for V2G for private EV owners appeared in 2025, although there are few V2G-capable models available, the regulatory landscape for V2G remains fragmented, and standards are not yet clear. Battery innovation is likely to continue: patents related to batteries account for nearly half of all energy-sector patents.

- `Source: GEVO2026, p. 191 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Vehicle outlook by mode`

> By 2035, the fleet of EVs across all vehicle types except two/three-wheelers (2/3Ws) exceeds 450 million globally in the CPS – more than five times as many EVs as there were at the end of 2025. CO2 and fuel economy standards, especially for new light-duty vehicles (LDVs), are the main driver of rising EV sales outside of the People’s Republic of China (hereafter, “China”). In China and a few other emerging markets, the competitive economics of EVs already support continued adoption in the CPS. Elsewhere, however, EV sales stall, particularly in regions with limited policy support or inadequate charging infrastructure. In the STEPS, EV deployment follows a trajectory similar to in the CPS, but with higher growth, especially in regions outside Europe and China – EVs across all vehicle types increase by around six times, without counting two-and three-wheelers (2/3Ws). Overall, the majority of EV market expansion – from 21 million electric cars today to 55 million electric cars by 2035 – takes place in emerging markets and developing economies (EMDEs), highlighting the critical role these economies will play in the coming decade. In this scenario, the stock of EVs (excluding 2/3Ws) increases at an average rate of about 20% per year. More than 90% of these vehicles are electric cars, a share similar to that observed in 2025. In contrast, the NZE Scenario sees a significantly faster expansion of the EV fleet (excluding 2/3Ws) by 2035, reaching close to 800 million.

</details>

## q10 (single)

**Question:** What share of global EV battery deployment used lithium iron phosphate chemistry in 2025?

**Reference:** More than 55% of global EV battery deployment in 2025.

**Answer:**

> In 2025, lithium iron phosphate (LFP) batteries accounted for over 55% of electric vehicle batteries deployed globally, an increase from nearly 50% in 2024 (GEVO2026, p. 96).

**Cited passages (1):**

- `Source: GEVO2026, p. 96 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Lithium iron phosphate now accounts for over half of the EV market, driven by China and emerging markets`

> In 2025, LFP batteries accounted for over 55% of EV batteries deployed globally, up from nearly 50% in 2024. Deployment remains heavily concentrated in China, but uptake is also expanding rapidly in other EMDEs. LFP batteries now power two-thirds of all electric car sales in these economies – double the share in 2023 – driven by imports of Chinese-manufactured vehicles and batteries. LFP batteries can reduce EV production costs, but their deployment remains mainly concentrated in China, where Chinese companies lead in LFP battery and materials production and innovation. In the European Union, LFP batteries accounted for more than 10% of EV battery demand in 2025, a similar level to 2024. Nearly all of these batteries were imported from China, either directly (30%) or embedded in LFP-equipped EVs (nearly 70%). In the United States, the share of LFP in EV batteries almost halved in 2025 from an already low base in 2024, reflecting higher tariffs on Chinese imports and more stringent sourcing requirements linked to the EV tax credit that was available until the third quarter of 2025. In 2025, over 50 GWh of battery manufacturing capacity, belonging to companies such as LG Energy Solution (LGES) and Ford, was reallocated toward LFP production. This underscores efforts to onshore this technology, albeit largely targeting the battery energy storage market, which is increasingly attracting the attention of battery producers that invested in the

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2026, p. 97 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Lithium iron phosphate now accounts for over half of the EV market, driven by China and emerging markets`

> United States over the past years. Battery stationary storage accounted for one-third of battery deployment in the United States in 2025, and its role is growing as deployments expand across power grids and data centres. Efforts to onshore LFP battery production represent an important first step to diversifying supplies, but the underlying supply chain remains a critical constraint. Production of LFP cathode materials and their precursors is still almost entirely concentrated in China (Figure 7.15), which holds the associated manufacturing capacity and the technical expertise. Some diversification options are being developed, such as Korean and Japanese producers investing in the technology, as well as an LFP production base being built in Indonesia. However, changing this structural imbalance will require substantial investments and stronger international co-operation across the entire battery value chain.

- `Source: GEVO2026, pp. 92-93 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Electric vehicle battery deployment grew by almost 30% in 2025`

> Electric vehicles (EVs) remained the primary source of global battery deployment, accounting for more than 70% of the total in 2025, slightly down from almost 80% in 2024. In 2025, EV battery deployment reached 1.2 TWh, an increase of almost 30% compared to 2024, and more than 7 times greater than in 2020. Light-duty vehicles remained the dominant segment, representing more than 85% of the 2025 EV battery deployment. However, the fastest growth came from electric trucks, for which battery demand more than doubled – largely thanks to a sharp acceleration in sales in the People’s Republic of China (hereafter, “China”) (see One in four trucks sold in China in 2025 was electric). As a result, electric trucks accounted for about 8% of global EV battery deployment in 2025, up from less than 5% in 2024. Regionally, EV battery deployment expanded in China (60% of global) and the European Union (almost 15%) in 2025, while it stagnated in the United States (10%). Growth in emerging markets and developing economies (EMDEs) other than China also continued – they represented 6% of global EV battery deployment in 2025, highlighting the increasingly global nature of road transport electrification.

- `Source: GEVO2026, p. 100 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · *`

> Today’s record low battery prices are partly sustained by losses incurred further upstream in the supply chain, particularly among producers of cathode active materials (CAMs). Cathode active material is the single most important component influencing battery cell production costs, accounting for 40-50% for NMC batteries and 25-30% for LFP batteries. Yet many of the leading CAM producers have been operating at a significant loss since 2023. This challenging market environment is not limited to NMC material producers, whose demand outlook has been dampened by the rapid rise of LFP batteries in recent years. LFP producers in China are also experiencing sustained losses, with the exception of Hunan Yuneng, the world’s largest LFP material supplier. These conditions are unlikely to be sustainable in the long term. They could trigger consolidation in the LFP material market, increasing its market concentration, or lead to greater pricing power among remaining producers. Either outcome could exert upward pressure on battery prices.

- `Source: GEVO2026, pp. 220-221 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · EV battery deployment more than triples by 2035`

> Global EV battery demand grows strongly as EV sales continue to expand, including in emerging markets. By 2030, EV battery deployment is expected to reach almost 3 TWh in both the CPS and STEPS, up from around 1.2 TWh in 2025. By 2035, deployment rises further, reaching around 4 TWh in the CPS and almost 5 TWh in the STEPS. To put this in perspective, on average, a single month of EV sales in 2035 would exceed the entire annual deployment of 2021. Electric cars continue to drive EV battery demand, but the importance of other modes, and particularly of electric trucks, is expected to grow. In both the CPS and STEPS, electric trucks are projected to account for around 10% of total EV battery deployment in 2030 and 2035, up from 8% in 2025. The gap between current and stated policies and the NZE Scenario is significant, with EV battery deployment reaching around 9 TWh by 2035 in the NZE Scenario – almost double the level in the STEPS that same year.

</details>

## q11 (single)

**Question:** According to the 2026 report, approximately what proportion of nominal capacity can the latest sodium-ion batteries retain at minus 40 degrees Celsius?

**Reference:** Around 90% of nominal capacity at minus 40 degrees Celsius.

**Answer:**

> The latest generation of sodium-ion batteries can retain around 90% of their nominal capacity at temperatures as low as -40°C (GEVO2026, p. 100).

**Cited passages (2):**

- `Source: GEVO2026, pp. 100-101 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Sodium-ion batteries are entering the scale-up phase`

> The first sodium-ion battery-powered electric car was introduced in China only in late 2023, but the technology is now being scaled up by leading battery producers such as CATL and BYD. Sodium-ion batteries perform significantly better at low temperatures than lithium-ion batteries, particularly LFP chemistries. The latest generation of sodium-ion batteries can retain around 90% of nominal capacity at temperatures as low as -40°C, and can operate at temperatures as high as 70°C. For the largest battery manufacturers, who can maintain multiple supply chains in parallel, expertise and production capacity for sodium-ion batteries can also help to reduce exposure to lithium price spikes. Despite recent progress, sodium-ion batteries remain constrained by lower energy density than lithium-ion technologies, limiting their competitiveness with LFP batteries at current lithium prices. The latest sodium-ion cells can reach up to 175 Wh/kg, compared with up to 205 Wh/kg for the latest generation of LFP batteries and 265 Wh/kg for lithium nickel cobalt manganese oxide (NMC) batteries. Their disadvantage is even greater in terms of volumetric energy density (Wh/l), which translates into a driving range of up to 350 km for an average SUV equipped with a sodium-ion battery, compared with a range of 400-600 km for lithium-ion batteries under average weather conditions.

- `Source: GEVO2026, p. 100 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · *`

> Today’s record low battery prices are partly sustained by losses incurred further upstream in the supply chain, particularly among producers of cathode active materials (CAMs). Cathode active material is the single most important component influencing battery cell production costs, accounting for 40-50% for NMC batteries and 25-30% for LFP batteries. Yet many of the leading CAM producers have been operating at a significant loss since 2023. This challenging market environment is not limited to NMC material producers, whose demand outlook has been dampened by the rapid rise of LFP batteries in recent years. LFP producers in China are also experiencing sustained losses, with the exception of Hunan Yuneng, the world’s largest LFP material supplier. These conditions are unlikely to be sustainable in the long term. They could trigger consolidation in the LFP material market, increasing its market concentration, or lead to greater pricing power among remaining producers. Either outcome could exert upward pressure on battery prices.

<details><summary>Other retrieved passages (3)</summary>

- `Source: GEVO2026, p. 101 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Sodium-ion batteries are entering the scale-up phase`

> Sodium-ion batteries are therefore expected to be better suited for small-range electric cars, light commercial vehicles operating in urban areas, two-and three-wheelers, industrial equipment such as forklifts, and battery stationary storage. They can also help reduce range losses in cold weather when used in hybrid EV battery packs combining lithium-ion and sodium-ion chemistries. Global supply chains for sodium-ion batteries are also far less developed than for lithium-ion batteries, limiting the near-term prospect of large-scale deployment. For example, the supply chain of hard carbon – the anode active material used in sodium-ion batteries as a substitute for graphite – is still poorly developed today and largely concentrated in China. Battery manufacturing capacity is also significantly smaller. Current sodium-ion battery cell manufacturing capacity is equal to just over 1% of that of lithium-ion cells, and announced projects for 2030 amount to only about 7% of the committed lithium-ion manufacturing capacity for the same year.

- `Source: GEVO2026, pp. 93-94 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Battery prices continued to decrease, albeit unevenly`

> Average battery prices declined by 8% in 2025, supported by continued improvements in manufacturing efficiency, advances and shifts in battery chemistries and technology, and intensifying global market competition (see Battery manufacturing and trade for more details). Relatively low critical mineral prices also contributed to downward cost pressure, although lithium and cobalt experienced notable price increases over the year. The recent increase in lithium and cobalt prices – if sustained – could put upward pressure on battery costs as stockpiles of minerals purchased at lower prices are being drained. Lithium prices at the beginning of 2026 were more than twice as high as in the same period in 2025, even though they remained around 70% lower than their 2022 peak. Several factors contributed to this rise, including faster-than-anticipated demand growth – particularly from the battery energy storage sector –, relatively low inventories in China and temporary supply disruptions, such as the suspension of operations at CATL’s Jianxiawo lithium mine. If these upward price trends persist, they could exert upward pressure on lithium-ion battery prices and reinforce the current momentum behind sodium-ion batteries, which offer lower ranges but do not rely on lithium. This effect could nevertheless be tempered by existing long-term contracts for lithium supply and vertical integration among major battery producers.

- `Source: GEVO2026, pp. 235-236 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Global battery project pipeline largely meets 2030 demand`

> The committed battery project pipeline is sufficient to meet global deployment needs by 2030 across all regions, with substantial short-term overcapacity projected in China and the United States. Although building manufacturing capacity is only the first step – new facilities can take more than 5 years from the start of operations to near nominal output – the pipeline remains robust, indicating that producers are well positioned to supply the batteries needed for transport electrification and for stationary storage systems supporting power grids worldwide. Among all regions, Chinese, Korean and Japanese producers are expected to remain the dominant players in battery manufacturing through this decade, although Japan’s global share of installed battery manufacturing capacity is expected to decline based on current project announcements.

</details>

## q12 (single)

**Question:** How large was the global electric car fleet at the end of 2024?

**Reference:** Almost 58 million electric cars.

**Answer:**

> At the end of 2024, the global electric car fleet had reached almost 58 million, representing about 4% of the total passenger car fleet (GEVO2025, p. 16).

**Cited passages (1):**

- `Source: GEVO2025, p. 16 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · More than 20% of new cars sold worldwide were electric`

> The rapid growth in electric car sales over the past 5 years has had a significant impact on the global car fleet: At the end of 2024, the electric car fleet had reached almost 58 million, about 4% of the total passenger car fleet and more than triple the total electric car fleet in 2021. Notably, the global stock of electric cars displaced over 1 million barrels per day of oil consumption in 2024. Of course, the stock of electric cars is not spread evenly across the world – in China, for example, around one in ten cars on the road is now electric, whereas in Europe the ratio is closer to one in twenty.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2025, p. 15 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · More than 20% of new cars sold worldwide were electric`

> Electric car sales topped 17 million worldwide in 2024, rising by more than 25%. Just the additional 3.5 million cars sold in 2024 compared to 2023 outnumber total electric car sales in the whole of 2020. China maintained its lead among major markets, with electric car sales exceeding 11 million – more than were sold worldwide just 2 years earlier. Global sales were slightly tempered by stagnating growth in Europe, as subsidies were phased out or reduced in several major markets, and as the EU CO2 targets for cars remained the same between 2023 and 2024. Electric car sales continued to increase in the United States although growth was about one-quarter that of the previous year. Significantly, outside of these three major markets, there was a record increase in sales of nearly 40% to reach 1.3 million, closing in on the United States’ sales of 1.6 million electric cars.

- `Source: GEVO2025, p. 10 | Global EV Outlook 2025 (2025) | Executive summary · Electric car sales continue to break records globally, particularly in China and other emerging economies`

> Electric car sales exceeded 17 million globally in 2024, reaching a sales share of more than 20%. Just the additional 3.5 million electric cars sold in 2024 compared with the previous year is more than the total number of electric cars sold worldwide in 2020. China maintained its lead, with electric cars accounting for almost half of all car sales in 2024; the over 11 million electric cars sold in China last year were more than global sales just 2 years earlier. As a result of continued strong growth, 1 in 10 cars on Chinese roads is now electric. Europe saw sales stagnate in 2024 as subsidy schemes and other supportive policies waned, but the sales share of electric cars remained around 20% as stronger sales in some countries compensated for lower sales in others. In the United States, electric car sales grew by about 10% year-on-year, reaching more than 1 in 10 cars sold.

- `Source: GEVO2026, pp. 16-17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> The electric car market reached new highs in 2025, growing by 20% from 2024 to exceed 20 million sales, in line with expectations in the 2025 edition of the Global EV Outlook. The sales share of electric cars in the overall car market increased to 25%. This marked the fifth consecutive year in which annual electric car sales increased by about 3.5 million, a trend that began in 2021 after the Covid-19 pandemic. As a result, about 5% of the global car stock is now electrified, displacing 1.2 million barrels of oil per day in 2025 (see Annex A). In particular, 2025 saw a boost for battery electric cars. The share of battery electric cars in total electric car sales increased to 65%, reversing the trend seen in the 2 years prior. While 2024 saw a strong increase in extended-range electric vehicles (EREVs), this did not continue in 2025, dropping to less than 7% of total electric car sales, after rising to 7.5% in 2024.

- `Source: GEVO2026, p. 191 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Vehicle outlook by mode`

> By 2035, the fleet of EVs across all vehicle types except two/three-wheelers (2/3Ws) exceeds 450 million globally in the CPS – more than five times as many EVs as there were at the end of 2025. CO2 and fuel economy standards, especially for new light-duty vehicles (LDVs), are the main driver of rising EV sales outside of the People’s Republic of China (hereafter, “China”). In China and a few other emerging markets, the competitive economics of EVs already support continued adoption in the CPS. Elsewhere, however, EV sales stall, particularly in regions with limited policy support or inadequate charging infrastructure. In the STEPS, EV deployment follows a trajectory similar to in the CPS, but with higher growth, especially in regions outside Europe and China – EVs across all vehicle types increase by around six times, without counting two-and three-wheelers (2/3Ws). Overall, the majority of EV market expansion – from 21 million electric cars today to 55 million electric cars by 2035 – takes place in emerging markets and developing economies (EMDEs), highlighting the critical role these economies will play in the coming decade. In this scenario, the stock of EVs (excluding 2/3Ws) increases at an average rate of about 20% per year. More than 90% of these vehicles are electric cars, a share similar to that observed in 2025. In contrast, the NZE Scenario sees a significantly faster expansion of the EV fleet (excluding 2/3Ws) by 2035, reaching close to 800 million.

</details>

## q13 (single)

**Question:** Approximately what share of new cars sold in the United Kingdom in 2024 were electric?

**Reference:** Nearly 30% of new car sales in 2024.

**Answer:**

> In 2024, electric car sales in the United Kingdom reached a share of nearly 30%, which was an increase from 24% in 2023 (GEVO2025, p. 17). Additionally, the 2026 edition notes that electric cars accounted for 1 in 4 new cars sold in the UK in 2024 (GEVO2026, pp. 21-22).

**Cited passages (2):**

- `Source: GEVO2025, p. 17 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · In Europe, electric car sales stagnated in 2024 as policy support waned in major car markets`

> In the United Kingdom – the second-largest car market in Europe – electric car sales reached a share of nearly 30%, up from 24% in 2023. The year 2024 was the first under the Vehicle Emissions Trading Scheme, which required 22% of all new registrations to be BEV or fuel cell electric vehicle (FCEV). When accounting for the scheme’s flexibilities, which allows OEMs to borrow credits from future years, they were able to comply with a battery electric car sales share of close to 20%. Norway reached near-total electrification of sales, with 88% of car sales being battery electric and just under 3% plug-in hybrid. As a result of the growing stock of electric cars, Norway’s oil consumption for road in 2024 decreased by 12% compared to 2021. From April 2025, a tax increase on conventional internal combustion engine (ICE) cars and PHEVs is expected to further increase the battery electric share towards meeting the Norwegian government’s 2025 goal of 100% zero-emissions car sales. In Denmark, the electric sales share increased by 10 percentage points to reach 56%, with nearly 100 000 electric cars sold.

- `Source: GEVO2026, pp. 21-22 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales saw strong growth in Europe in 2025, thanks to policy support`

> In the United Kingdom, electric car sales increased by more than 25%, accounting for over 1 in 3 new cars sold in 2025 – a significant increase from 1 in 4 new cars in 2024. Nearly half a million electric car sales were battery electric, representing 23% of all new cars sold. This fell short of the target set under the Vehicle Emissions Trading Schemes, which aimed for zero-emission cars (battery electric and fuel cell) to reach 28% of new registrations in 2025. However, manufacturers were still able to comply with the targets by using the scheme’s flexibilities introduced in 2025, such as borrowing credits from future years and earning extra credits. To further support sales, in July 2025 the government introduced a new subsidy for eligible battery electric cars priced below GBP 37 000 (USD 47 400). More than one-quarter of battery electric car sales were eligible for this subsidy in 2025.

<details><summary>Other retrieved passages (3)</summary>

- `Source: GEVO2026, p. 17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> Market developments varied across regions. In the People’s Republic of China (hereafter, “China”), growth slowed slightly partly as a result of its trade-in scheme being temporary halted, but the country still accounted for more than half of the global increase in electric car sales in 2025. Europe experienced an upswing in sales following a step change in the EU CO2 standards, with sales rising 30% to more than 4 million after having stagnated in 2024. In the United States, the sales share of electric cars remained relatively stable at just below 10%, despite several policy shifts, including the ending of tax credits, which resulted in sales falling significantly in the last quarter of the year. Meanwhile, outside of these major car markets, sales continued to expand rapidly.

- `Source: GEVO2025, p. 33 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · China and the European Union remained the world’s largest EV exporters, while Mexico ramped up exports to the United States`

> Global electric car exports surged by nearly 20% in 2024, reaching about 3.2 million electric cars and accounting for almost 20% of global sales, a share similar to that seen in 2023 and 2022. As with manufacturing, China accounted for the largest share, with 40% of global exports, or nearly 1.25 million electric cars.

- `Source: GEVO2026, pp. 16-17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> The electric car market reached new highs in 2025, growing by 20% from 2024 to exceed 20 million sales, in line with expectations in the 2025 edition of the Global EV Outlook. The sales share of electric cars in the overall car market increased to 25%. This marked the fifth consecutive year in which annual electric car sales increased by about 3.5 million, a trend that began in 2021 after the Covid-19 pandemic. As a result, about 5% of the global car stock is now electrified, displacing 1.2 million barrels of oil per day in 2025 (see Annex A). In particular, 2025 saw a boost for battery electric cars. The share of battery electric cars in total electric car sales increased to 65%, reversing the trend seen in the 2 years prior. While 2024 saw a strong increase in extended-range electric vehicles (EREVs), this did not continue in 2025, dropping to less than 7% of total electric car sales, after rising to 7.5% in 2024.

</details>

## q14 (single)

**Question:** What share of the US electric car market did Tesla hold in 2024?

**Reference:** 38% of US electric car sales in 2024.

**Answer:**

> Tesla held a market share of 38% in the US electric car market in 2024 (GEVO2025, p. 18).

**Cited passages (1):**

- `Source: GEVO2025, p. 18 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · The market share of electric cars continued to expand in the United States`

> In the United States, electric car sales increased to 1.6 million in 2024, with the sales share growing to more than 10%. However, growth in electric car sales slowed down significantly in 2024, increasing by just 10% compared to 40% in 2023. In spite of this, electric car sales did boost the overall car market, as sales of conventional cars stagnated. A total of 24 new electric car models were launched in 2024, increasing model availability by 15% compared to 2023, providing consumers with more choices and further increasing competition. While the Tesla Model Y and Model 3 have been the two best-selling models in the United States since 2020, the 110 new models that have entered the market since then have driven the market share of Tesla down from 60% in 2020 to 38% in 2024. Furthermore, 2024 was the first year in which Tesla saw a drop in sales in the United States, while other OEMs saw sales increase by 20% on aggregate.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2025, p. 53 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Limited availability of affordable models hinders US electric car sales growth`

> In 2024 in the United States, about one in five electric SUVs (including pick-up trucks) was sold at a lower price than the average conventional SUV. This is particularly significant given that SUVs account for three-quarters of total car sales in the United States. Progress on battery electric car affordability has fluctuated in recent years. In 2023, the average purchase price premium of battery electric SUVs noticeably decreased to 25% from 50% in 2022, largely as a result of Tesla repeatedly slashing prices in an attempt to maintain its market lead in the United States. However, despite further price reductions to the Tesla Model Y SUV in 2024, Tesla’s market share fell around 10% year-on-year. This decline outweighed the impact of the late price cuts, leaving the average price premium of battery electric SUVs in the United States unchanged from the previous year. The contrast with conventional models is stark: in 2024, only 2 battery electric models (3% of battery electric car models) were priced below USD 30 000, compared to more than 50 ICE models (20% of available ICE models). In the short term, Honda and Volkswagen have recently announced they will launch “affordable” compact electric SUVs, bringing to market a handful of models under the USD 30 000 mark. However, most of the BEV model releases expected by 2026 that have been announced with launch prices are in the premium car category, with over 70% anticipated to have a purchase price of more than USD 50 000.

- `Source: GEVO2025, p. 15 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · More than 20% of new cars sold worldwide were electric`

> Electric car sales topped 17 million worldwide in 2024, rising by more than 25%. Just the additional 3.5 million cars sold in 2024 compared to 2023 outnumber total electric car sales in the whole of 2020. China maintained its lead among major markets, with electric car sales exceeding 11 million – more than were sold worldwide just 2 years earlier. Global sales were slightly tempered by stagnating growth in Europe, as subsidies were phased out or reduced in several major markets, and as the EU CO2 targets for cars remained the same between 2023 and 2024. Electric car sales continued to increase in the United States although growth was about one-quarter that of the previous year. Significantly, outside of these three major markets, there was a record increase in sales of nearly 40% to reach 1.3 million, closing in on the United States’ sales of 1.6 million electric cars.

- `Source: GEVO2026, p. 17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> Market developments varied across regions. In the People’s Republic of China (hereafter, “China”), growth slowed slightly partly as a result of its trade-in scheme being temporary halted, but the country still accounted for more than half of the global increase in electric car sales in 2025. Europe experienced an upswing in sales following a step change in the EU CO2 standards, with sales rising 30% to more than 4 million after having stagnated in 2024. In the United States, the sales share of electric cars remained relatively stable at just below 10%, despite several policy shifts, including the ending of tax credits, which resulted in sales falling significantly in the last quarter of the year. Meanwhile, outside of these major car markets, sales continued to expand rapidly.

- `Source: GEVO2026, p. 217 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Incumbent automakers in the United States and Europe scale back targets as EV policy shifts and profitability takes a hit`

> Honda has cancelled three EV models planned for production in the United States, and is expecting losses of around USD 16 billion for restructuring its EV business. Nissan has also postponed the start of production of two electric SUVs at an assembly plant in the United States to 2028. Tesla has now lost is position as the top-selling BEV maker in the world to China’s BYD, with its battery electric car sales dropping 9% to 1.6 million in 2025, a 3-year low. If including PHEVs, BYD overtook Tesla in EV sales as early as 2022. Tesla has now decided to discontinue the production of both its Model X and Model S, shifting its focus to robots and AI. Another US-headquartered EV maker, Rivian, announced it would look for ways to reduce costs and bring its electric car models to mass market, as they can no longer depend on EV tax credits.

</details>

## q15 (single)

**Question:** How many electric cars were manufactured worldwide in 2024 and what proportion were produced in China?

**Reference:** 17.3 million electric cars were manufactured worldwide in 2024, with China accounting for more than 70%.

**Answer:**

> A total of 17.3 million electric cars were produced worldwide in 2024 (GEVO2025, p. 31). China produced 12.4 million of these cars, accounting for more than 70% of global production (GEVO2025, p. 31).

**Cited passages (1):**

- `Source: GEVO2025, p. 31 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Steady growth in global electric car production masks differences at the regional level`

> A total 17.3 million electric cars were produced worldwide in 2024, about one-quarter more than in 2023, largely as a result of increased production in China, which reached 12.4 million electric cars. China remains the world’s electric car manufacturing hub, accounting for more than 70% of global production in 2024. Production in China has been increasingly shaped by the expansion of domestic manufacturers. In 2024, Chinese OEMs accounted for more than 80% of domestic production, up from roughly two-thirds in 2021. Despite the numerous recently announced foreign direct investment plans from Chinese OEMs, their overseas production has yet to ramp up. Electric car production by Chinese OEMs operating outside China accounted for less than 2% of their global output in 2024. In the world’s second-largest electric car manufacturing region, the European Union, production stagnated at 2.4 million cars in 2024, but surpassed domestic sales by more than 5%. Domestic carmakers were behind nearly 80% of the region’s total output, but there were contrasting trends among EU OEMs. While German OEMs marked a 5% year-on-year increase in their EU output, other EU OEMs (Stellantis and Renault) saw their regional production drop by over 15%, producing about 420 000 electric cars, or less than 20% of the region’s output. Meanwhile, there was a sixfold increase in EU production by US OEMs between 2021 and 2024, predominantly led by Tesla and Ford. This contributed to the share of foreign OEMs in EU production reaching about 20% in 2024.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GEVO2025, p. 12 | Global EV Outlook 2025 (2025) | Executive summary · Global trade of electric cars is growing as manufacturers eye new markets`

> China continues to be the world’s EV manufacturing hub and is responsible for more than 70% of global production. Car manufacturers headquarted in China predominantly cater to the domestic market, accounting for around 80% of domestic sales in 2024 and almost all of the 25% growth in global EV production. In the European Union, production stalled at 2.4 million electric cars in 2024. North America saw contrasting trends: US production declined whereas Mexico’s output doubled, supported by comparatively low manufacturing costs. Roughly 70% of Mexico’s output was from US-headquartered manufacturers. Production also increased by 15% in Asia Pacific countries other than China, reaching about 1 million electric cars, mostly from incumbent carmakers from Japan and Korea. Global trade of electric cars increased 20% in 2024; imports now represent almost one-fifth of global electric car sales. At 40% (nearly 1.25 million electric cars),China accounted for the largest share of global exports in 2024. The European Union also remained a net exporter of electric cars: exports reached over 800 000, mostly destined for other European countries (such as the United Kingdom) and North America. EU imports were below 700 000, of which 60% came from China. The United States remained a net importer of electric cars; imports increased by nearly 40% in 2024, while exports fell by nearly 15%.

- `Source: GEVO2025, p. 15 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · More than 20% of new cars sold worldwide were electric`

> Electric car sales topped 17 million worldwide in 2024, rising by more than 25%. Just the additional 3.5 million cars sold in 2024 compared to 2023 outnumber total electric car sales in the whole of 2020. China maintained its lead among major markets, with electric car sales exceeding 11 million – more than were sold worldwide just 2 years earlier. Global sales were slightly tempered by stagnating growth in Europe, as subsidies were phased out or reduced in several major markets, and as the EU CO2 targets for cars remained the same between 2023 and 2024. Electric car sales continued to increase in the United States although growth was about one-quarter that of the previous year. Significantly, outside of these three major markets, there was a record increase in sales of nearly 40% to reach 1.3 million, closing in on the United States’ sales of 1.6 million electric cars.

- `Source: GEVO2026, pp. 13-14 | Global EV Outlook 2026 (2026) | Executive summary · Trade plays an important role in the EV industry`

> China remains the world’s largest EV manufacturing hub, accounting for nearly 75% of electric cars produced in 2025. Almost 22 million electric cars were produced globally in 2025 – a more than 25% increase on the previous year. Intense domestic competition in China is squeezing profit margins, pushing manufacturers to seek higher profits overseas. Chinese electric car exports doubled to a record high of over 2.5 million in 2025, as production outstripped domestic demand. In 2024, China overtook the European Union to become the largest exporter of cars; in 2025, more than 35% of China’s car exports were EVs, up from 20% in 2024. Imports from China accounted for 55% of electric car sales in 2025 in countries outside Europe and the United States, up from less than 5% just 5 years earlier. More than half of electric cars sold in Southeast Asia in 2025 were by Chinese brands, while one-third came from a Vietnamese manufacturer.

- `Source: GEVO2025, p. 33 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · China and the European Union remained the world’s largest EV exporters, while Mexico ramped up exports to the United States`

> Global electric car exports surged by nearly 20% in 2024, reaching about 3.2 million electric cars and accounting for almost 20% of global sales, a share similar to that seen in 2023 and 2022. As with manufacturing, China accounted for the largest share, with 40% of global exports, or nearly 1.25 million electric cars.

</details>

## q16 (single)

**Question:** What was the approximate volume of global electric car exports in 2024 and how much did it increase from the previous year?

**Reference:** About 3.2 million electric cars were exported in 2024, an increase of nearly 20% from 2023.

**Answer:**

> Global electric car exports reached about 3.2 million vehicles in 2024, representing an increase of nearly 20% from the previous year (GEVO2025, p. 33).

**Cited passages (2):**

- `Source: GEVO2025, pp. 33-34 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · China and the European Union remained the world’s largest EV exporters, while Mexico ramped up exports to the United States`

> In 2024, the European Union saw its exports grow 9% year-on-year to nearly 830 000 electric cars. The key destination markets for EU-made electric cars remained unchanged, with other European countries accounting for almost 60% of exports (40% to the United Kingdom), followed by North America, accounting for about one-quarter of EU exports. The European Union remained a net exporter of electric cars in 2024, despite importing about 680 000 electric cars. While imports from China remained steady in 2024 at more than 400 000 electric cars (60% of EU imports), the share of Chinese OEMs in imports from China grew to two-thirds in 2024, up from 50% in the previous year. The Chinese OEM Geely accounted for almost 40% of these imports, mainly through its brand Volvo Cars, while Tesla’s share decreased from 30% to 20% as more than half of its EU sales in 2024 were produced at its German assembly plant. Other European countries rely significantly on imports, primarily from the European Union. The majority of production elsewhere in Europe is based in the United Kingdom and Türkiye, but these countries were responsible for less than 15% of regional sales in 2024. China was the second-largest trade partner for electric cars, accounting for more than one-quarter of the 840 000 electric cars imported by non-EU European countries in 2024.

- `Source: GEVO2025, p. 33 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · China and the European Union remained the world’s largest EV exporters, while Mexico ramped up exports to the United States`

> Global electric car exports surged by nearly 20% in 2024, reaching about 3.2 million electric cars and accounting for almost 20% of global sales, a share similar to that seen in 2023 and 2022. As with manufacturing, China accounted for the largest share, with 40% of global exports, or nearly 1.25 million electric cars.

<details><summary>Other retrieved passages (3)</summary>

- `Source: GEVO2025, pp. 34-35 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Chinese exports are increasingly driven by domestic OEMs as their destinations diversify`

> While it remains the world’s largest exporter of electric cars, China experienced a noticeable slowdown in export growth in 2024. According to the China Association of Automobile Manufacturers (CAAM), the country exported over 1.15 million electric cars in 2023, marking a staggering 80% growth from 2022. However, in 2024, annual export growth fell to just 7%, split unevenly across destination markets. Several factors contributed to this slowdown. Firstly, the increase in trade restrictions resulting from tariff hikes in major export markets prompted Chinese OEMs to frontload their exports before such tariffs came into force. In Brazil for example, although Chinese imports saw strong year-on-year growth, with an increase of 120% in 2024, they dropped sharply by a factor of eight in the second half of the year following the reinstatement of tariffs. Europe remained the most important export market for Chinese-made electric cars, but weakening demand, reluctance of European consumers to buy Chinese EV brands and new countervailing duties in the European Union led the share of value attributed to Europe in total Chinese EV exports to fall from over 70% in 2021 to roughly 40% in 2024. As a result, Chinese exports increasingly shifted towards emerging markets such as Mexico (+370%), Southeast Asia (+10%), Russian Federation (hereafter: Russia) and countries in the Caspian Sea region.

- `Source: GEVO2025, p. 12 | Global EV Outlook 2025 (2025) | Executive summary · Global trade of electric cars is growing as manufacturers eye new markets`

> China continues to be the world’s EV manufacturing hub and is responsible for more than 70% of global production. Car manufacturers headquarted in China predominantly cater to the domestic market, accounting for around 80% of domestic sales in 2024 and almost all of the 25% growth in global EV production. In the European Union, production stalled at 2.4 million electric cars in 2024. North America saw contrasting trends: US production declined whereas Mexico’s output doubled, supported by comparatively low manufacturing costs. Roughly 70% of Mexico’s output was from US-headquartered manufacturers. Production also increased by 15% in Asia Pacific countries other than China, reaching about 1 million electric cars, mostly from incumbent carmakers from Japan and Korea. Global trade of electric cars increased 20% in 2024; imports now represent almost one-fifth of global electric car sales. At 40% (nearly 1.25 million electric cars),China accounted for the largest share of global exports in 2024. The European Union also remained a net exporter of electric cars: exports reached over 800 000, mostly destined for other European countries (such as the United Kingdom) and North America. EU imports were below 700 000, of which 60% came from China. The United States remained a net importer of electric cars; imports increased by nearly 40% in 2024, while exports fell by nearly 15%.

- `Source: GEVO2025, p. 36 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Chinese exports are increasingly driven by domestic OEMs as their destinations diversify`

> Inventory build-up by Chinese OEMs also contributed to the slowdown in Chinese export growth. In 2023, sales of Chinese-made electric cars outside China fell short by 275 000 cars compared to CAAM’s reported exports. This led to clogged destination seaports, particularly in Europe and Brazil, and limited the capacity for additional imports in 2024 until excess inventory was cleared. However, this stockpile helped sustain overseas sales growth of 35% for Chinese-made electric cars in 2024, while exports grew only 7%. Chinese OEMs accounted for 70% of 2024 total electric car exports from China, up from 55% in 2023. To sustain their export momentum, Chinese OEMs are investing in expanding shipping capacity through roll-on/roll-off (Ro-Ro) car carriers. In 2025, BYD commissioned the world’s largest Ro-Ro vessel, bringing its total shipping capacity to more than 30 000 electric cars. Meanwhile, a leading Chinese car shipping company, COSCO Shipping Car Carriers, announced plans to expand its fleet to handle up to 700 000 cars annually. Despite the 2024 export slowdown, this surge in shipping capacity positions Chinese OEMs for renewed growth, playing a crucial role in facilitating exports from China and emerging manufacturing hubs like Southeast Asia.

</details>

## q17 (single)

**Question:** How much did global lithium demand grow in 2025 and what total volume did it reach?

**Reference:** Global lithium demand grew by 23% in 2025 to more than 275 kilotonnes of lithium.

**Answer:**

> Global lithium demand grew by 23% year-on-year in 2025, reaching a total volume of more than 275 kt (GCMO2026, p. 140).

**Cited passages (1):**

- `Source: GCMO2026, p. 140 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · China and energy storage: keywords for sustained lithium demand growth`

> Lithium demand continued to expand rapidly in 2025, reaching more than 275 kt. This represents a 23% year-on-year increase: a slight moderation from growth in 2024, but still well above the growth rates seen in most other commodity markets. The expansion reflects the continued acceleration of electrification. Demand from EVs rose by 20% to 170 kt, while demand from battery storage reached 30 kt. China accounted for about 90% of the increase in global lithium demand, followed by Korea (+4.2 kt) and Central Europe (+1.4 kt), where battery material production capacity is being developed.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GCMO2026, p. 145 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · In a context of surging lithium demand, the project pipeline highlights the continued need for new mines, as well as opportunities for diversification on the refining side`

> Lithium demand is set to continue rising strongly over the next two decades. In the STEPS, demand in 2040 is 3.5-times higher than in 2025 and around 14 times higher than in 2020. EVs remain the main source of growth as their deployment continues to expand across major markets. At the same time, energy storage is becoming an increasingly important source of demand growth. In the STEPS, lithium demand from energy storage rises to around 70 kt in 2040 and reaches 90 kt in 2050, around three times today’s level. In the HDS, demand from storage reaches 120 kt in 2050, underlining the growing role of batteries in power systems with rising shares of variable renewables.

- `Source: GCMO2026, pp. 141-142 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Increasing lithium refining concentration`

> Global lithium refining output grew rapidly in 2025, with Chinese output expanding by close to 40% year-on-year due to the ramp-up of new capacity, such as Ganfengs’s new Dazhou plant (7.2 kt of capacity each), as well as increased utilisation. Some new capacity also emerged in the United States, Korea, Indonesia and Australia but has yet to ramp up, as average utilisation rates remain well below those of China. Overall, this led to increased concentration in lithium refining output, with China’s share rising from 70% in 2024 to 75% in 2025. The first half of 2026 was marked by the start of the first lithium refining plant in Africa, with the ramp-up of a China-owned Zhejiang Huayou factory in Zimbabwe. The plant, at a total investment cost of USD 400 million, is designed to refine about 6.5 kt in the form of sulphate, which can then be further refined overseas into carbonate or hydroxide and then battery chemicals. Market conditions remained uneven across products. Lithium hydroxide, a chemical used in nickel-rich chemistries, continued to perform less strongly than carbonate, due to the rise of LFP chemistries. This continued to weigh on hydroxide refineries, as well as those converting carbonate into hydroxide, and led to curtailments outside China, including at Australia’s Kemerton plant.

- `Source: GCMO2026, p. 141 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Growing strains on hard-rock lithium supplies`

> Hard-rock ore, and particularly spodumene, is increasingly becoming the dominant source of lithium supply compared with brine-based resources. The market for hard-rock ores tightened significantly over the course of 2025, due to strong feedstock demand and mining supply constraints. In 2025, lithium chemical output grew by 32%, whereas mined output grew by 18%. In 2025, Argentina saw faster growth output than the historical major producers, Chile, China and Australia. New entrants are reshaping the supply landscape, particularly in Africa: mined output from the continent grew by 44%, helping diversify supply but also involving challenges related to infrastructure and logistics. While three regions, the South American “lithium triangle”, China and Australia, account for the majority of lithium supplies today, African nations now represent 14% of global supplies, a 26-fold increase from 2020. While contributing to the diversification of mining supply, this trend could, however, reinforce the dominance of the top refining country, as over 65% of new lithium mining capacity on the continent is owned by companies headquartered in China. With the rise of regional output, the importance of small-scale mining is slowly expanding, bringing its own challenges. This year, significant steps were also taken to increase European output. In 2025, Finland’s Keliber mine began operating, with a planned annual capacity of 2.5 kt before 2030, sufficient to meet 90% of European demand for cathode production in the short term. France is also accelerating strategic mining projects, such as the Allier hard-rock lithium and Alsace brine projects.

- `Source: GCMO2026, p. 142 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Recycling and market maturity`

> Secondary supply continues to scale rapidly, with recycled volumes increasing by over 40% year-on-year in 2025. However, it still accounts for only around 5% of total supply, highlighting both its growing importance and its current limitations in materially contributing to overall supply growth. The lithium market is gradually becoming more structured, as reflected in record trading volumes for lithium futures and the development of forward pricing tools. Downstream players are increasingly securing long-term supply, as illustrated by recent deals involving MinRes and POSCO, as well as Pilbara Minerals and Canmax.

</details>

## q18 (single)

**Question:** Was the global nickel market in surplus or deficit in 2025 and by approximately how much?

**Reference:** The global nickel market had a surplus of around 200 kilotonnes in 2025.

**Answer:**

> The global nickel market was in a surplus of approximately 200 kt in 2025 (GCMO2026, p. 148).

**Cited passages (2):**

- `Source: GCMO2026, p. 148 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · The nickel market is well supplied in the short term, but policy and cost pressures are emerging in the leading producer, Indonesia`

> The nickel market remained in a 200 kt surplus in 2025, keeping prices subdued throughout the year. Global production increased by 9% year-on-year in mined output and 7% in refined output, driven primarily by Indonesia, which remains the world’s largest producer of both mined and refined nickel. Outside Indonesia, persistently low prices continued to weigh on output, with production in the rest of the world declining by over over 10%% in mined production and just under 3% in refined production. At the same time, global nickel demand rose by almost 3% in 2025 to 3.5 Mt, largely supported by growth in nickel use in battery applications, particularly in nickel-rich chemistries for EVs. The global nickel market has become increasingly concentrated in Indonesia, which now accounts for almost two-thirds of mined supply and just under half of refined output. This reflects structural advantages, including a large laterite resource base, an integrated processing ecosystem, strong state support focused on industrial policy, Chinese capital and technology, economies of scale and access to relatively low-cost coal-based energy. As a result, policy developments in Indonesia are increasingly shaping global market dynamics. Despite continued physical oversupply, nickel prices began to rise towards the end of 2025 and into early 2026 following a series of policy announcements in Indonesia.

- `Source: GCMO2026, pp. 148-149 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · The nickel market is well supplied in the short term, but policy and cost pressures are emerging in the leading producer, Indonesia`

> Indonesia’s mined nickel output is governed by production quotas (RKAB), introduced in 2023 as three-year allocations. This framework was revised in October 2025, shortening quotas to one year and requiring companies to reapply for quotas covering 2026 and 2027. Shortly after, Indonesia’s Minister of Energy and Natural Resources announced plans to curb nickel output in 2026 to support prices and government revenues. These measures followed the revocation of in September 2025 due to non-compliance with rehabilitation or production requirements. Taken together, these developments tightened expectations around future supply availability and contributed to a 20% increase in nickel prices between December 2025 and mid-2026. As policies increasingly restrict access to domestic ore and aim to support higher prices and royalties, Indonesian smelters have increasingly turned to imported feedstock, importing almost 300 kt of nickel metal equivalent from the Philippines in 2025, up by almost 50% from 2024. The Philippines is the world’s second-largest holder of nickel reserves, largely limonite ore, which feeds into high-pressure acid leaching (HPAL) processing facilities and enables the production of battery-grade intermediates. Co-operation between the two countries was recently formalised through the IndoPhil Nickel Corridor, which aims to provide stable feedstock supply for Indonesia’s expanding HPAL capacity.

<details><summary>Other retrieved passages (3)</summary>

- `Source: GCMO2026, p. 153 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Despite robust demand growth, the nickel market is expected to remain well supplied, although Indonesia’s policy shifts could alter the outlook`

> The nickel market is expected to remain in surplus over the next few years, with excess supply persisting before 2030 despite continued demand growth. Based on announced projects, Indonesia continues to drive production expansion, accounting for over 100% of the supply growth in mining and 80% in refining to 2030 in the base case. Indonesia’s production share is set to rise further to almost 75% in mining and around half in refining by 2035, from almost two-thirds and 45% today, respectively, reflecting structural advantages. At the same time, demand continues to grow at a robust pace. By 2035, batteries are expected to account for 30% of total nickel consumption, accounting for almost two-thirds of demand growth. China, Indonesia, Japan and Korea represent the bulk of incremental demand as battery manufacturing and downstream capacity continue to expand. Although the shift towards LFP chemistries moderates nickel demand relative to last year’s Outlook, nickel-rich chemistries are expected to retain an important role, particularly for battery makers outside China and in markets such as North America and Europe, where consumers prefer long-range vehicles.

- `Source: GCMO2026, pp. 153-154 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Despite robust demand growth, the nickel market is expected to remain well supplied, although Indonesia’s policy shifts could alter the outlook`

> Supply gaps start to emerge beyond in the late 2020s in the base case, with a 1.9 Mt gap emerging by 2040. The high-production case closes over 60% of this shortfall but depends on sustained expansion in a limited number of jurisdictions, mainly Indonesia. Despite this, a number of projects remain on hold or under care and maintenance. In addition, almost 2 Mt of early-stage mining projects exist across Indonesia, Australia, North America and Latin America, which could provide additional supply if economic conditions support development and help narrow supply gaps. However, many projects in geographically diverse regions have struggled to emerge or recover following prolonged periods of low prices, given persistent and structural challenges. Higher energy and operating costs, stricter environmental standards, smaller project scale and slower ramp-up profiles limit competitiveness at prevailing prices. Both brownfield expansions and greenfield developments outside today’s dominant producers require higher incentive prices to proceed.

- `Source: GCMO2026, p. 154 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Despite robust demand growth, the nickel market is expected to remain well supplied, although Indonesia’s policy shifts could alter the outlook`

> The largest concentration risks in the nickel market are closely linked to the battery value chain, where supply disruptions or policy shifts can have outsized impacts on the availability of battery-grade nickel products. Battery production requires nickel sulphate, which can be produced either from Class I nickel metal or from nickel intermediates, such as MHP and nickel matte. While Indonesia has rapidly expanded production of these intermediates and is expected to account for just over 70% of the global market by 2035, China is expected to remain the dominant supplier of nickel sulphate, accounting for 70% of the market by 2035.

</details>

## q19 (single)

**Question:** What happened to cobalt metal prices in the first quarter of 2026 compared with the previous year?

**Reference:** Cobalt metal prices approached USD 58000 per tonne in the first quarter of 2026, more than three times their level a year earlier.

**Answer:**

> In the first quarter of 2026, cobalt metal prices approached USD 58 000 per tonne, reaching more than three times the level of the previous year (GCMO2026, p. 156). This upward price pressure was driven by supply tightness in intermediate feedstocks following export controls and quota systems implemented in the Democratic Republic of the Congo (GCMO2026, p. 156).

**Cited passages (1):**

- `Source: GCMO2026, p. 156 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · The cobalt market is expected to shift into deficit from 2026 due to DRC export restrictions, with the outlook increasingly shaped by policy developments in the DRC and Indonesia`

> In 2025, mined cobalt production stood at around 320 kt, similar to production levels in 2024. However, trade in cobalt intermediates (unrefined cobalt), particularly cobalt hydroxide, saw a notable reduction following the introduction of export controls by the Democratic Republic of the Congo (DRC), the world’s largest mined cobalt supplier. Following several years of oversupply and depressed prices, the DRC implemented an export ban on cobalt, including cobalt hydroxide, the country’s prevalent export form, in early 2025. Later in 2025, this was followed by a quota system capping cobalt exports at 96 600 tonnes, less than half of 2024 production volumes. These measures led to supply tightness in intermediate feedstocks and contributed to upward pressure on prices. Cobalt metal prices approached USD 58 000 per tonne in the first quarter of 2026, more than three times as high as the previous year. However, refined cobalt inventories remained elevated, resulting in differing price dynamics between intermediates and refined products. In early 2026, prices of cobalt hydroxide approached those of cobalt metal. Strong demand growth from the batteries and electronics sectors in 2025 widened the price premium of cobalt sulphate and cobalt tetroxide over cobalt metal. Meanwhile, Indonesia has emerged as a significant alternative supplier, producing cobalt as a by-product of nickel operations. Its share of global production has increased from around 1.5% in 2020 to approximately 15% in 2025.

<details><summary>Other retrieved passages (4)</summary>

- `Source: GCMO2026, p. 162 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · China’s lead in refining persists as diversification prospects remain limited`

> China remains the leading cobalt refiner, accounting for more than 75% of the market in 2025, a share that remains broadly unchanged through the projection period. Limited new refining projects in geographically diverse regions are in sight, keeping China’s refining dominance intact in the near to medium term. Chinese refineries have dealt with shortages in cobalt intermediates due to administrative delays in DRC quota allocation, though the impact has been contained given that quota allocations have been directed primarily to Chinese-invested DRC operations. For cobalt sulphate, a key precursor for EV batteries, the market is set to grow by almost 60% by 2035, with few operations outside China and Indonesia. In January 2026, Morocco’s Managem planned to switch its cobalt metal production in Bou Azzer to sulphate, with a capacity estimated at 6 kt per annum, of which 1.2 kt is contained cobalt. In the long term, operations such as Umicore’s Kokkola cobalt refinery in Finland will continue to contribute almost 2.5 kt per annum. Secondary cobalt supply is projected to over double by 2035 to almost 45 kt, though volumes remain insufficient to close the demand gap from primary sources. China lifted its ten-year ban on black mass imports on 1 August 2025, redirecting secondary feedstock to Chinese refiners and reinforcing its downstream position. A combination of policy actions incentivising higher recycling of consumer and EV batteries is projected to raise the secondary share of total supply to 15% by 2035 in the STEPS.

- `Source: GCMO2026, pp. 160-161 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Mined supply of cobalt is increasingly shaped by policy developments in the top suppliers`

> Near-term mined supply is driven by DRC policy implementation and Indonesian ramp-up, but intermediate markets are expected to be tight while export controls remain in place. In 2025, large-scale miners in the DRC posted strong production results. CMOC produced 117 kt from Tenke Fungurume and KFM, while Glencore’s production from KCC and Mutanda totalled 36 kt. However, export quotas limited the material reaching the market: KCC and Mutanda did not export cobalt in Q4 2025, and while CMOC’s cobalt production was up 0.3% year-on-year, sales were down 92% year-on-year. For 2026, CMOC received 31 200 tonnes of the total quota of 96 000 tonnes, including the DRC’s strategic quota to be distributed by ARECOMS to projects of national strategic importance, while Glencore received 22 800 tonnes. The currently published 2026 quota levels are insufficient to meet projected intermediate supply requirements, which may be further constrained by administrative delays in physical exports.

- `Source: GCMO2026, p. 161 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Mined supply of cobalt is increasingly shaped by policy developments in the top suppliers`

> This has tightened hydroxide availability and increased competition for intermediate feedstocks, limiting the ability of refining capacity to respond to growing demand. While Indonesia is expected to provide incremental supply, its contribution is subject to constraints. Indonesia’s 2026 RKAB quota tightening and rising sulphur costs have disrupted HPAL feedstock availability and increased cost pressures. At the same time, quota-driven tightness on nickel supply supports nickel prices, which in turn underpins the economics of cobalt produced as a by-product. As Indonesian nickel production drives cobalt supply expansion over the long term, cobalt markets become increasingly linked to nickel markets, with almost 50% of global cobalt projected to be produced as a by-product of nickel by 2035 in the base case.

- `Source: GCMO2026, p. 160 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · The cobalt market transitions to deficit from 2026under persistent DRC export constraints, with adequate supply contingent on responses from Indonesia and other producers`

> Cobalt demand growth continues to be led by EVs, with cobalt use for EV batteries rising by nearly two-thirds through 2040 in the STEPS, even though cobalt demand for EV batteries has been revised down compared with last year's Outlook due to shifts in battery chemistry choices. The rapid rise of LFP batteries continues to weigh on cobalt demand growth. However, this effect is partially offset by changes within nickel-cobalt-manganese (NCM) chemistries compared with previous expectations. In particular, NCM 622 and NCM 532, both more cobalt-intensive than higher-nickel chemistries such as NCM 811, are maintaining stronger market shares in premium EV segments, especially in Europe and North America, where energy density requirements, vehicle performance considerations and original equipment manufacturer product cycles continue to support cobalt-bearing cathodes. As a result, battery chemistry developments have a mixed impact on cobalt demand, with the growth of LFP reducing demand while the persistence of cobalt-intensive NCM chemistries provides an important source of support.

</details>

## q20 (single)

**Question:** Under the Stated Policies Scenario, how is global graphite demand expected to change between 2025 and 2035?

**Reference:** Global graphite demand is expected to almost double between 2025 and 2035.

**Answer:**

> Under the Stated Policies Scenario (STEPS), global graphite demand is expected to almost double from 2025 to 2035, driven primarily by strong growth in demand for electric vehicle and storage batteries (GCMO2026, p. 171).

**Cited passages (2):**

- `Source: GCMO2026, p. 171 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Demand`

> Graphite demand is set to almost double from 2025 to 2035 in the STEPS, mainly driven by strong growth in demand for EV and storage batteries. In the long term, material choice and technology substitution will play a role in shaping demand for battery-grade graphite, as silicon, lithium metal and hard carbon are set to progressively increase their market shares and substitute graphite. Demand is expected to remain concentrated in China, which accounted for two-thirds of demand in 2025. Outside China, new graphite demand is expected to come mainly from new battery projects in Asia, North America and Europe. Electrification of steel is driving demand growth for graphite electrodes, set to increase by around 50% from 2025 to 2035, though surplus production capacity is expected to persist into the 2030s, while other uses such as refractories, foundries and recarburising are expected to overall increase by 30%.

- `Source: GCMO2026, p. 171 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Concentration risks call for strong action and policy support for diversification`

> The global graphite market remains broadly well supplied through 2030, with ample idle synthetic production capacity that could be mobilised in China in response to market signals. However, new demand comes not only from batteries but increasingly from non-battery applications, notably electrodes for electric arc furnaces, as well as graphite use in other industrial and strategic sectors. Several of these applications require specific graphite grades that are not readily interchangeable with battery-grade material, underscoring the emerging risks of grade-specific tightness.

<details><summary>Other retrieved passages (3)</summary>

- `Source: GCMO2026, pp. 164-166 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · New synthetic graphite production in China drives supply growth…`

> China Japan India United States Indonesia Canada Other Demand Battery-grade supply and demand growth Natural spherical Synthetic battery anodes Spherical and synthetic supply growth 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025 High power Medium power Low power USD/tonne Natural Synthetic High power Medium power Low power In 2025, global graphite demand increased by around 6% year-on-year, driven almost entirely by the battery sector, where demand rose by over 14%, reflecting continued growth in EV and stationary storage deployment. By contrast, demand from non-battery applications remained broadly stable. Despite the strong demand growth, the graphite market remained oversupplied across all major segments of the supply chain, with sustained downward pressure on prices. New supply was mainly driven by the growth of synthetic graphite, which increased by 22% in 2025, while natural spherical graphite supply decreased by 3%.

- `Source: GCMO2026, p. 172 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Supply`

> From 2025 to 2035, total graphite supply is expected to grow by over 50% in the base case, driven by new battery-grade supply (both natural spherical and synthetic) from China. Mined supply, however, is expected to decrease in China, offset by new flake mine developments in other regions, mainly Africa, Canada and Brazil. In Canada, Nouveau Monde Graphite confirmed the final investment decision for its Matawinie Mine project, which is expected to produce around 100 kt per year of graphite starting before 2030. New graphite mine developments are expected to deliver significant progress in mined supply diversification, decreasing China’s share from 80% in 2025 to 53% in 2035. However, the country is expected to retain a strong hold on refined graphite markets, with its share of battery-grade graphite supply decreasing only from 94% to 91% in the next decade.

- `Source: GCMO2026, p. 173 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Box 2.1 Strategic importance of specialised graphite beyond batteries`

> While these non-battery applications account for a relatively small share of total graphite volumes, they are highly specification-sensitive and mission-critical. Demand for specialised graphite is expected to increase steadily over the next decade, driven by rising defence expenditure, expansion of aerospace and space systems, expansion of nuclear capacity, and the scaling-up of semiconductor manufacturing. This creates strategic exposure, as supply chains for high-grade graphite remain highly concentrated, and capacity for specialised grades is significantly more difficult to substitute or scale than bulk battery materials.

</details>

## q21 (multi)

**Question:** How did the share of electric cars in the global passenger car fleet change between the end of 2024 and 2025?

**Reference:** The share increased from about 4% at the end of 2024 to about 5% in 2025, a rise of roughly 1 percentage point.

**Answer:**

> At the end of 2024, the electric car fleet accounted for about 4% of the total global passenger car fleet (GEVO2025, p. 16). By 2025, this share had increased to about 5% of the global car stock (GEVO2026, pp. 16–17), representing an increase of 1 percentage point.

**Cited passages (2):**

- `Source: GEVO2025, p. 16 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · More than 20% of new cars sold worldwide were electric`

> The rapid growth in electric car sales over the past 5 years has had a significant impact on the global car fleet: At the end of 2024, the electric car fleet had reached almost 58 million, about 4% of the total passenger car fleet and more than triple the total electric car fleet in 2021. Notably, the global stock of electric cars displaced over 1 million barrels per day of oil consumption in 2024. Of course, the stock of electric cars is not spread evenly across the world – in China, for example, around one in ten cars on the road is now electric, whereas in Europe the ratio is closer to one in twenty.

- `Source: GEVO2026, pp. 16-17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> The electric car market reached new highs in 2025, growing by 20% from 2024 to exceed 20 million sales, in line with expectations in the 2025 edition of the Global EV Outlook. The sales share of electric cars in the overall car market increased to 25%. This marked the fifth consecutive year in which annual electric car sales increased by about 3.5 million, a trend that began in 2021 after the Covid-19 pandemic. As a result, about 5% of the global car stock is now electrified, displacing 1.2 million barrels of oil per day in 2025 (see Annex A). In particular, 2025 saw a boost for battery electric cars. The share of battery electric cars in total electric car sales increased to 65%, reversing the trend seen in the 2 years prior. While 2024 saw a strong increase in extended-range electric vehicles (EREVs), this did not continue in 2025, dropping to less than 7% of total electric car sales, after rising to 7.5% in 2024.

<details><summary>Other retrieved passages (3)</summary>

- `Source: GEVO2026, p. 11 | Global EV Outlook 2026 (2026) | Executive summary · Electric cars are poised to make up a greater share of total car sales in 2026`

> Global electric car sales are expected to grow to 23 million in 2026, representing 28% of total car sales. Europe is poised for the largest growth among major markets, with sales projected to increase by around 20% in 2026, such that one in three cars sold are electric. In China, electric car sales are set to grow across 2026, albeit at a slower rate than in previous years, to reach almost 60% of total car sales. Sales across Asia Pacific countries other than China are expected to grow by over 50%, while sales in Latin America are projected to rise by 45%. The wider economic impacts of the conflict in the Middle East might temper overall car sales. In many regions, however, there is upside potential to the 2026 EV forecast depending, in part, on how, when and which policies are enacted amid the current energy crisis.

- `Source: GEVO2026, p. 45 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales are expected to grow 10% in 2026, but uncertainties are high`

> Market and policy fundamentals for 2026 point towards growth in electric car sales, but data on low sales figures in the first quarter of 2026 suggest that the rate of growth is likely to be more moderate than previously expected. China has scaled back incentives, and in the United States, manufacturers are reassessing electrification strategies. In Europe and Southeast Asia, demand is being driven by a combination of policy action and the improving affordability of electric cars. Overall, global electric car sales are expected to reach around 23 million, representing growth of approximately 10%.

- `Source: GEVO2025, p. 10 | Global EV Outlook 2025 (2025) | Executive summary · Electric car sales continue to break records globally, particularly in China and other emerging economies`

> Electric car sales exceeded 17 million globally in 2024, reaching a sales share of more than 20%. Just the additional 3.5 million electric cars sold in 2024 compared with the previous year is more than the total number of electric cars sold worldwide in 2020. China maintained its lead, with electric cars accounting for almost half of all car sales in 2024; the over 11 million electric cars sold in China last year were more than global sales just 2 years earlier. As a result of continued strong growth, 1 in 10 cars on Chinese roads is now electric. Europe saw sales stagnate in 2024 as subsidy schemes and other supportive policies waned, but the sales share of electric cars remained around 20% as stronger sales in some countries compensated for lower sales in others. In the United States, electric car sales grew by about 10% year-on-year, reaching more than 1 in 10 cars sold.

</details>

## q22 (multi)

**Question:** How did China's annual electric car sales growth in 2025 compare with its growth in 2024?

**Reference:** Electric car sales in China grew by almost 40% in 2024 but by less than 20% in 2025.

**Answer:**

> Electric car sales in China increased by almost 40% year-on-year in 2024 (GEVO2025, p. 16). By contrast, in 2025, electric car sales grew by less than 20% (GEVO2026, p. 19).

**Cited passages (3):**

- `Source: GEVO2025, pp. 16-17 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · Almost half of China’s car sales were electric in 2024, representing almost two-thirds of electric cars sold globally`

> In recent years, sales of plug-in hybrid electric cars have been growing faster than sales of battery electric cars in China. The share of plug-in hybrid electric vehicle (PHEV) sales, excluding extended-range EVs (EREVs), in China’s total electric car sales has risen from about 15% in 2020 to nearly 30% in 2024. Meanwhile, the share of EREVs has more than quadrupled since 2020, surpassing 10% in 2024. The acceleration of PHEV sales in China led the share of electric car sales that are battery electric to fall from 80% in 2020 to below 60% in 2024, though in absolute terms battery electric car sales increased sevenfold over the same period, demonstrating their continued appeal to new customers.

- `Source: GEVO2025, p. 16 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · Almost half of China’s car sales were electric in 2024, representing almost two-thirds of electric cars sold globally`

> Electric car sales in China increased by almost 40% year-on-year in 2024, further driving up China’s share of global electric car sales. In 2021, China accounted for half of global electric car sales; this share grew to almost two-thirds in 2024. On a monthly basis, sales of electric cars have overtaken conventional car sales in the country since July 2024, bringing the share of electric car sales close to 50% for the full year. In China, 2024 marks the fourth consecutive year in which the electric car sales share grew by approximately 10 percentage points year-on-year. The growth in China reflects in no small part the growing price competitiveness of battery electric cars with conventional cars in the country. In addition, China’s electric car market benefitted from the introduction of a trade-in scheme in April 2024. The scheme, which is part of a wider economic stimulus package, applies to the purchase of conventional and electric cars alike, but with different levels of financial support. Following a retroactive increase, the scheme offers CNY 20 000 (Yuan renminbi) (USD 2 750) for consumers that replace an older vehicle (conventional or electric) with a new electric car, and CNY 15 000 (USD 2 050) for replacement with a new conventional vehicle. In 2024, about 6.6 million consumers applied for the incentive, 60% of whom bought an electric car. As such, more than one-third of the over 11 million new electric car sales in the country benefitted from this incentive.

- `Source: GEVO2026, pp. 18-19 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Close to 55% of new cars sold in China were electric in 2025`

> More than 13 million electric cars were sold in China in 2025, maintaining its position as the world’s largest electric car market, accounting for six out of ten electric cars sold globally. Monthly electric car sales exceeded a 50% sales share in 11 out of 12 months of 2025 – up from only 5 months in 2024. This lifted the electric car sales share to almost 55%. As a result, an estimated 44 million electric cars were on Chinese roads at the end of 2025, representing around 13% of the total car stock, up from 1 in 10 in 2024. Growth in electric car sales in China has been extremely rapid over the past five years: from 2020-24, the annual growth rate in electric cars exceeded 75% and the sales share increased by around 10 percentage points on average each year. By contrast, in 2025, electric car sales grew less than 20% and the sales share rose by only about 6 percentage points. However, China remains by far the largest electric car market and has one of the highest sales shares of any country.

<details><summary>Other retrieved passages (5)</summary>

- `Source: GEVO2025, p. 10 | Global EV Outlook 2025 (2025) | Executive summary · Electric car sales continue to break records globally, particularly in China and other emerging economies`

> Electric car sales exceeded 17 million globally in 2024, reaching a sales share of more than 20%. Just the additional 3.5 million electric cars sold in 2024 compared with the previous year is more than the total number of electric cars sold worldwide in 2020. China maintained its lead, with electric cars accounting for almost half of all car sales in 2024; the over 11 million electric cars sold in China last year were more than global sales just 2 years earlier. As a result of continued strong growth, 1 in 10 cars on Chinese roads is now electric. Europe saw sales stagnate in 2024 as subsidy schemes and other supportive policies waned, but the sales share of electric cars remained around 20% as stronger sales in some countries compensated for lower sales in others. In the United States, electric car sales grew by about 10% year-on-year, reaching more than 1 in 10 cars sold.

- `Source: GEVO2025, p. 15 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · More than 20% of new cars sold worldwide were electric`

> Electric car sales topped 17 million worldwide in 2024, rising by more than 25%. Just the additional 3.5 million cars sold in 2024 compared to 2023 outnumber total electric car sales in the whole of 2020. China maintained its lead among major markets, with electric car sales exceeding 11 million – more than were sold worldwide just 2 years earlier. Global sales were slightly tempered by stagnating growth in Europe, as subsidies were phased out or reduced in several major markets, and as the EU CO2 targets for cars remained the same between 2023 and 2024. Electric car sales continued to increase in the United States although growth was about one-quarter that of the previous year. Significantly, outside of these three major markets, there was a record increase in sales of nearly 40% to reach 1.3 million, closing in on the United States’ sales of 1.6 million electric cars.

- `Source: GEVO2026, pp. 46-47 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Strong growth expected in Europe and emerging markets in 2026`

> In China, the world’s largest EV market, sales are expected to reach more than 14 million, growing by close to 8% year-on-year. This level of growth reflects weaker performance in the early months of the year, partly driven by the introduction of caps to trade-in incentives (scrappage schemes). At the same time, long-standing purchase tax exemptions for new energy vehicles (NEVs) are being phased out (see Q1 sales). However, the market share of electric cars is expected to grow to close to 60%, despite a weak overall car market, supported by a highly competitive domestic industry and extensive model availability. In Europe, electric car sales are set to maintain robust momentum in 2026. Policy support is strengthening in key markets, with Germany reintroducing incentives and Spain advancing its Plan Auto+ programme. In the United Kingdom, the mandated share of zero-emission vehicles rises to 33% under the Vehicle Emissions Trading Schemes, up from 28% in 2025.At the same time, increased competition, including from Chinese manufacturers, is expanding consumer choice, particularly in more affordable segments. As a result, European EV sales are expected to reach 5 million, marking an increase of close to 20%.

- `Source: GEVO2026, p. 235 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Rising local EV production in EMDEs and tightening trade policies challenge Chinese imports`

> In 2025, nearly two-thirds of electric car sales in EMDEs other than China were Chinese imports. By 2030, in the STEPS, although Chinese exports to other EMDEs grow more than 70% from 2025 levels, to exceed 1.2 million units, their share in these markets falls below 40%, as local output grows. By 2035, exports to EMDEs could reach around 1.6 million units – one-fifth of China’s total exports – but make up only 25% of total EMDE sales

- `Source: GEVO2026, p. 11 | Global EV Outlook 2026 (2026) | Executive summary · Electric cars are poised to make up a greater share of total car sales in 2026`

> Global electric car sales are expected to grow to 23 million in 2026, representing 28% of total car sales. Europe is poised for the largest growth among major markets, with sales projected to increase by around 20% in 2026, such that one in three cars sold are electric. In China, electric car sales are set to grow across 2026, albeit at a slower rate than in previous years, to reach almost 60% of total car sales. Sales across Asia Pacific countries other than China are expected to grow by over 50%, while sales in Latin America are projected to rise by 45%. The wider economic impacts of the conflict in the Middle East might temper overall car sales. In many regions, however, there is upside potential to the 2026 EV forecast depending, in part, on how, when and which policies are enacted amid the current energy crisis.

</details>

## q23 (multi)

**Question:** How did the electric share of new car sales in Europe change between 2024 and 2025?

**Reference:** The share increased from about 20% in 2024 to 28% in 2025, an increase of roughly 8 percentage points.

**Answer:**

> In Europe, about one in five new cars sold was electric in 2024 (GEVO2025, p. 17), maintaining the sales share of the previous year (GEVO2025, p. 17). By 2025, the electric car sales share across the region rose to 28% (GEVO2026, p. 21). This represents an increase of approximately 8 percentage points, computed from these figures.

**Cited passages (3):**

- `Source: GEVO2026, p. 21 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales saw strong growth in Europe in 2025, thanks to policy support`

> Electric car sales increased by more than 30% in Europe in 2025, reversing the relative stagnation seen since 2022. Across the region, electric car sales numbered 1 million more in 2025 than in the previous year, reaching a total of 4.2 million, or 28% of all new cars sold. In the European Union, electric car sales totalled almost 3 million and the EV sales share reached just under 27%. Additionally, 24 of the 27 EU member states recorded an increase in electric car sales shares, compared with just 13 the previous year. In more than half of these countries, the sales share rose by more than 5 percentage points. The increase in EU electric car sales was the result of policy design, notably the step change in the EU CO2 standards that came into effect in 2025, targeting an emissions reduction of 15% compared to 2021 levels. Towards the end of 2025, the European Commission proposed the Automotive Package, aimed at further increasing regulatory flexibility for 2030 and 2035 while supporting EU industrial competitiveness by promoting vehicles that are made in the European Union as well as electrifying company fleets (see Chapter 9).

- `Source: GEVO2025, p. 17 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · In Europe, electric car sales stagnated in 2024 as policy support waned in major car markets`

> In the United Kingdom – the second-largest car market in Europe – electric car sales reached a share of nearly 30%, up from 24% in 2023. The year 2024 was the first under the Vehicle Emissions Trading Scheme, which required 22% of all new registrations to be BEV or fuel cell electric vehicle (FCEV). When accounting for the scheme’s flexibilities, which allows OEMs to borrow credits from future years, they were able to comply with a battery electric car sales share of close to 20%. Norway reached near-total electrification of sales, with 88% of car sales being battery electric and just under 3% plug-in hybrid. As a result of the growing stock of electric cars, Norway’s oil consumption for road in 2024 decreased by 12% compared to 2021. From April 2025, a tax increase on conventional internal combustion engine (ICE) cars and PHEVs is expected to further increase the battery electric share towards meeting the Norwegian government’s 2025 goal of 100% zero-emissions car sales. In Denmark, the electric sales share increased by 10 percentage points to reach 56%, with nearly 100 000 electric cars sold.

- `Source: GEVO2025, p. 17 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · In Europe, electric car sales stagnated in 2024 as policy support waned in major car markets`

> About one in five new cars sold on the European market was electric in 2024, maintaining the sales share of the previous year. The electric sales share increased in 2024 in 14 out of 27 EU member states, while it either stalled or decreased in the rest, including in several larger markets, such as Germany and France, largely as a result of subsidies being phased out or reduced. In Germany, subsidies ceased at the end of 2023, while France has progressively reduced its subsidy over the years. At the start of 2024, France limited the amount of environmental bonus available to higher-income car buyers and reduced the number of vehicles eligible for the subsidy. Besides subsidies, the policy design of the European Union CO2 standards may also have held back further growth of the electric car market in 2024. As new targets come into effect every 5 years, car makers had no incentive to push sales of electric cars further in 2024 (in anticipation of strengthened targets in 2025). This is in contrast to markets such as the United Kingdom, where annually increasing targets move original equipment manufacturers (OEMs) towards electrification each year. In March 2025, the European Commission published its Industrial Action Plan for the European automotive sector, in which it proposed to amend the CO2 emission performance standards for cars and vans, granting them additional flexibilities by averaging their performance over a 3-year period.

<details><summary>Other retrieved passages (5)</summary>

- `Source: GEVO2026, p. 22 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales saw strong growth in Europe in 2025, thanks to policy support`

> Across Europe, the share of BEVs in electric car sales has increased steadily over the past few years, supported by emission standards that favour zero-emission vehicles, in particular the EU CO2 standards. The BEV share in electric car sales rose from 55% in 2020 to nearly 70% in 2025. As a result, Europe and China reached similar shares of BEVs in EVs in 2025, with Europe ending the year slightly higher. Overall, electric cars now represent about 5% of the European car fleet. Norway leads, with more than one-third of the car stock being electric. Within the European Union, only Denmark has a stock share above 20%, reflecting the lag between rapid sales uptake and stock turnover.

- `Source: GEVO2026, p. 201 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · European policies continue to support the transition to EVs, while introducing some flexibilities`

> Electric car sales also rise in the rest of Europe on aggregate, on the back of impressive momentum in large markets such as Türkiye. Although support varies a lot at the national level, strong policies in some countries drive Europe’s sales share of electric cars and vans to around 90% in 2035 in the CPS and close to 85% in the STEPS, up from around 25% today.

- `Source: GEVO2026, p. 17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> Market developments varied across regions. In the People’s Republic of China (hereafter, “China”), growth slowed slightly partly as a result of its trade-in scheme being temporary halted, but the country still accounted for more than half of the global increase in electric car sales in 2025. Europe experienced an upswing in sales following a step change in the EU CO2 standards, with sales rising 30% to more than 4 million after having stagnated in 2024. In the United States, the sales share of electric cars remained relatively stable at just below 10%, despite several policy shifts, including the ending of tax credits, which resulted in sales falling significantly in the last quarter of the year. Meanwhile, outside of these major car markets, sales continued to expand rapidly.

- `Source: GEVO2026, p. 11 | Global EV Outlook 2026 (2026) | Executive summary · Electric cars are poised to make up a greater share of total car sales in 2026`

> Global electric car sales are expected to grow to 23 million in 2026, representing 28% of total car sales. Europe is poised for the largest growth among major markets, with sales projected to increase by around 20% in 2026, such that one in three cars sold are electric. In China, electric car sales are set to grow across 2026, albeit at a slower rate than in previous years, to reach almost 60% of total car sales. Sales across Asia Pacific countries other than China are expected to grow by over 50%, while sales in Latin America are projected to rise by 45%. The wider economic impacts of the conflict in the Middle East might temper overall car sales. In many regions, however, there is upside potential to the 2026 EV forecast depending, in part, on how, when and which policies are enacted amid the current energy crisis.

- `Source: GEVO2025, p. 26 | Global EV Outlook 2025 (2025) | 1. Trends in electric car markets · Electric car sales are expected to exceed 20 million in 2025, representing one-quarter of total car sales`

> The new phase of the CO2 targets in the European Union is expected to drive up electric car sales, although the new flexibilities mean OEMs have less of an incentive to bring lower-priced electric cars to market this year. Given that a purchase premium for electric cars persists in Europe, the phase-out of EV purchase subsidies in some European countries could place downward pressure on sales, but there are signs to the contrary. At the end of 2024, the electric car purchase subsidy in the Netherlands came to an end, but electric car sales in the country in the first quarter of 2025 were about 10% higher than during the same period of 2024. In Italy, direct purchase subsidies for electric cars are no longer being renewed after 2024, though the government does aim to support the domestic production of EVs. In the first three months of 2025, electric car sales in Italy were up almost 50%. Over the course of the year, electric car sales are expected to reach around 4 million across Europe. In line with this, the share of electric cars sales would increase several percentage points compared to 2024, to around 25%. The increase in electric car sales across Europe is boosted by the UK Vehicle Emissions Trading Scheme, which sets the target of 28% battery electric car sales in 2025.

</details>

## q24 (multi)

**Question:** Was the global average battery price reduction in 2025 larger or smaller than in 2024, and what were the reported annual declines?

**Reference:** The reduction was smaller in 2025: average battery prices fell by 8%, compared with a decline of more than 25% in 2024.

**Answer:**

> The corpus reports that average battery prices declined by 8% in 2025 (GEVO2026, p. 93), whereas the global average battery pack price fell by more than 25% in 2024 compared to 2023 levels (GEVO2025, p. 47). Therefore, the global average battery price reduction was smaller in 2025 than in 2024.

**Cited passages (2):**

- `Source: GEVO2026, pp. 93-94 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Battery prices continued to decrease, albeit unevenly`

> Average battery prices declined by 8% in 2025, supported by continued improvements in manufacturing efficiency, advances and shifts in battery chemistries and technology, and intensifying global market competition (see Battery manufacturing and trade for more details). Relatively low critical mineral prices also contributed to downward cost pressure, although lithium and cobalt experienced notable price increases over the year. The recent increase in lithium and cobalt prices – if sustained – could put upward pressure on battery costs as stockpiles of minerals purchased at lower prices are being drained. Lithium prices at the beginning of 2026 were more than twice as high as in the same period in 2025, even though they remained around 70% lower than their 2022 peak. Several factors contributed to this rise, including faster-than-anticipated demand growth – particularly from the battery energy storage sector –, relatively low inventories in China and temporary supply disruptions, such as the suspension of operations at CATL’s Jianxiawo lithium mine. If these upward price trends persist, they could exert upward pressure on lithium-ion battery prices and reinforce the current momentum behind sodium-ion batteries, which offer lower ranges but do not rely on lithium. This effect could nevertheless be tempered by existing long-term contracts for lithium supply and vertical integration among major battery producers.

- `Source: GEVO2025, p. 47 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Falling battery pack prices and intensifying competition underpin progress in electric car affordability`

> Today, electric cars often have a lower total cost of ownership than ICE cars over the vehicle lifetime, due to reduced fuel and maintenance expenses. However, reducing the purchase price gap will be key to broader uptake. In Europe, for example, respondents to a 2023 survey by the European Commission identified the price of battery electric cars as the main barrier to adoption. While battery electric car prices generally fell in 2024, the price gap with ICE cars remains in most regions. Electric car affordability has made significant strides over the past decade, primarily driven by falling battery prices, intensifying market competition and carmakers reaching economies of scale. In 2024, despite the global average battery size growing slightly, the global average battery pack price fell more than 25% compared with 2023 levels. This resulted in a global drop in electric car manufacturing costs that was reflected in the price of electric cars.

<details><summary>Other retrieved passages (5)</summary>

- `Source: GEVO2025, p. 13 | Global EV Outlook 2025 (2025) | Executive summary · Competition and declining battery prices are improving affordability, though progress is uneven`

> Low critical mineral prices and increasing competition between battery manufacturers drove down battery pack prices in all markets in 2024, albeit with significant variations. In China, prices fell by about 30%, compared with 10-15% in Europe and the United States. The faster pace of cost reductions in China – enabled by strong competition, increasing manufacturing efficiency and supply chain integration, and access to a skilled workforce – is increasing the competitive advantage of Chinese battery manufacturers.

- `Source: GEVO2026, p. 95 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Battery prices continued to decrease, albeit unevenly`

> Over the past few years, the average battery price has decreased across all regions, but regional price disparities have widened. In 2025, battery pack prices in China were 30% lower than in North America, and 35% lower than in Europe, compared to a respective 20% and 25% in 2022.

- `Source: GEVO2026, p. 49 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · Electric car prices fell in major markets, but the lack of low-cost models still limits affordability in some`

> In Germany, the introduction of new affordable models brought down the average BEV price in 2025, even though the price of medium-sized models actually rose. New affordable models and battery cost declines together reduced the average BEV price by around 5%, with pricing strategies and other factors bringing the total year-on-year decrease to about 6%. In the United States, the average retail price of a battery electric car fell nearly 2% in 2025. Most of the price decline can be explained by battery price reductions, while the remainder was driven by pricing strategies and non-battery manufacturing cost changes.

- `Source: GEVO2026, pp. 48-49 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · Electric car prices fell in major markets, but the lack of low-cost models still limits affordability in some`

> The upfront price of electric cars compared to their internal combustion engine (ICE) equivalents remains a barrier to wider adoption. Over the past decade, declining battery manufacturing costs and the introduction of new affordable models mean the price-competitiveness of electric cars has made significant strides. However, the shift towards larger batteries and larger vehicle segments in many markets over the past 5 years has limited the impact of these cost reductions on purchase prices. In 2025, the sales-weighted average purchase price of electric cars declined across almost all segments across the three markets covered in this section – the People’s Republic of China (hereafter, “China”), Germany and the United States. Across all three, a decrease in battery cell prices and manufacturers’ pricing strategies contributed to cost declines, although new model entries in each market had differing effects on average battery electric vehicle (BEV) prices. In China, while prices fell within most segments, the introduction of new models put upward pressure on average BEV prices, as many of these were SUVs. The rising share of SUVs and increasing average battery sizes would have led to a roughly 3% increase in prices, but this effect was more than offset by declining battery cell prices (Figure 5.4), as well as non-battery component cost declines and carmakers’ aggressive pricing strategies in the increasingly competitive electric vehicle (EV) market. The overall result was a net drop of more than 10% in average BEV prices in 2025.

- `Source: GEVO2025, p. 48 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Falling battery pack prices and intensifying competition underpin progress in electric car affordability`

> However, the trend towards falling prices has been uneven across markets, due to differences in carmakers’ pricing strategies, and in market maturity and the level of competition. For example, in China, the sales-weighted average (hereafter, “average”) price of a battery electric SUV fell almost 10% year-on-year in 2024, partly due to the 30% decline in the battery pack price. Similarly, in the United States, a 15% decline in battery prices contributed to a 3% drop in the average purchase price of electric SUVs in 2024. In contrast, in Germany, the price of electric SUVs slightly increased in 2024, despite their battery pack prices declining 20%. This suggests that the battery pack price is not the only factor influencing EV prices: other component manufacturing costs, trim levels and carmakers’ pricing strategies also play a significant role.

</details>

## q25 (multi)

**Question:** For a 2025 battery supply-chain assessment, what were global EV battery deployment and global lithium demand, and how quickly did each grow year on year?

**Reference:** EV battery deployment reached 1.2 TWh in 2025, up almost 30%; lithium demand exceeded 275 kilotonnes, up 23%.

**Answer:**

> In 2025, global EV battery deployment reached 1.2 TWh, representing a year-on-year growth rate of almost 30% compared to 2024 (GEVO2026, pp. 92–93). Global lithium demand reached more than 275 kt in 2025, which was a 23% increase year on year (GCMO2026, p. 140).

**Cited passages (2):**

- `Source: GEVO2026, pp. 92-93 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Electric vehicle battery deployment grew by almost 30% in 2025`

> Electric vehicles (EVs) remained the primary source of global battery deployment, accounting for more than 70% of the total in 2025, slightly down from almost 80% in 2024. In 2025, EV battery deployment reached 1.2 TWh, an increase of almost 30% compared to 2024, and more than 7 times greater than in 2020. Light-duty vehicles remained the dominant segment, representing more than 85% of the 2025 EV battery deployment. However, the fastest growth came from electric trucks, for which battery demand more than doubled – largely thanks to a sharp acceleration in sales in the People’s Republic of China (hereafter, “China”) (see One in four trucks sold in China in 2025 was electric). As a result, electric trucks accounted for about 8% of global EV battery deployment in 2025, up from less than 5% in 2024. Regionally, EV battery deployment expanded in China (60% of global) and the European Union (almost 15%) in 2025, while it stagnated in the United States (10%). Growth in emerging markets and developing economies (EMDEs) other than China also continued – they represented 6% of global EV battery deployment in 2025, highlighting the increasingly global nature of road transport electrification.

- `Source: GCMO2026, p. 140 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · China and energy storage: keywords for sustained lithium demand growth`

> Lithium demand continued to expand rapidly in 2025, reaching more than 275 kt. This represents a 23% year-on-year increase: a slight moderation from growth in 2024, but still well above the growth rates seen in most other commodity markets. The expansion reflects the continued acceleration of electrification. Demand from EVs rose by 20% to 170 kt, while demand from battery storage reached 30 kt. China accounted for about 90% of the increase in global lithium demand, followed by Korea (+4.2 kt) and Central Europe (+1.4 kt), where battery material production capacity is being developed.

<details><summary>Other retrieved passages (7)</summary>

- `Source: GEVO2026, pp. 220-221 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · EV battery deployment more than triples by 2035`

> Global EV battery demand grows strongly as EV sales continue to expand, including in emerging markets. By 2030, EV battery deployment is expected to reach almost 3 TWh in both the CPS and STEPS, up from around 1.2 TWh in 2025. By 2035, deployment rises further, reaching around 4 TWh in the CPS and almost 5 TWh in the STEPS. To put this in perspective, on average, a single month of EV sales in 2035 would exceed the entire annual deployment of 2021. Electric cars continue to drive EV battery demand, but the importance of other modes, and particularly of electric trucks, is expected to grow. In both the CPS and STEPS, electric trucks are projected to account for around 10% of total EV battery deployment in 2030 and 2035, up from 8% in 2025. The gap between current and stated policies and the NZE Scenario is significant, with EV battery deployment reaching around 9 TWh by 2035 in the NZE Scenario – almost double the level in the STEPS that same year.

- `Source: GEVO2026, pp. 16-17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> The electric car market reached new highs in 2025, growing by 20% from 2024 to exceed 20 million sales, in line with expectations in the 2025 edition of the Global EV Outlook. The sales share of electric cars in the overall car market increased to 25%. This marked the fifth consecutive year in which annual electric car sales increased by about 3.5 million, a trend that began in 2021 after the Covid-19 pandemic. As a result, about 5% of the global car stock is now electrified, displacing 1.2 million barrels of oil per day in 2025 (see Annex A). In particular, 2025 saw a boost for battery electric cars. The share of battery electric cars in total electric car sales increased to 65%, reversing the trend seen in the 2 years prior. While 2024 saw a strong increase in extended-range electric vehicles (EREVs), this did not continue in 2025, dropping to less than 7% of total electric car sales, after rising to 7.5% in 2024.

- `Source: GEVO2026, p. 45 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales are expected to grow 10% in 2026, but uncertainties are high`

> Market and policy fundamentals for 2026 point towards growth in electric car sales, but data on low sales figures in the first quarter of 2026 suggest that the rate of growth is likely to be more moderate than previously expected. China has scaled back incentives, and in the United States, manufacturers are reassessing electrification strategies. In Europe and Southeast Asia, demand is being driven by a combination of policy action and the improving affordability of electric cars. Overall, global electric car sales are expected to reach around 23 million, representing growth of approximately 10%.

- `Source: GEVO2026, p. 14 | Global EV Outlook 2026 (2026) | Executive summary · Trade plays an important role in the EV industry`

> Around one-quarter of electric cars produced in 2025 were traded between countries. Electric car exports from the European Union grew 25% in 2025, but imports also rose by around 35% year-on-year to more than 900 000; China accounted for almost 60% of these imports. Imports to the United States fell slightly in 2025, with the largest share coming from Mexico.In the first quarter of 2026, electric car exports from China more than doubled compared with the same period in 2025, offsetting weaker domestic sales. Yet Chinese exports could face headwinds in 2026 as inventories build up: in 2025, exports are estimated to have exceeded overseas sales by more than 25%. China accounted for over 80% of battery cell production in 2025 and even higher shares of production of the active materials in EV batteries. Nearly all battery cells used worldwide are supplied by companies headquartered in China, Korea or Japan, and the market share of Chinese producers is growing especially fast in the European Union, having almost doubled since 2023. However, narrow profit margins are putting pressure on some battery manufacturers, and tightening access to advanced manufacturing production tax credits in the United States could challenge Korean and Japanese battery manufacturers that are heavily exposed to the US market. Despite lithium-ion battery manufacturing capacity growing faster in the European Union and the United States than in China last year, China is set to remain the largest producer of batteries and battery materials to 2035 based on stated policies.

- `Source: GCMO2026, p. 145 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · In a context of surging lithium demand, the project pipeline highlights the continued need for new mines, as well as opportunities for diversification on the refining side`

> Lithium demand is set to continue rising strongly over the next two decades. In the STEPS, demand in 2040 is 3.5-times higher than in 2025 and around 14 times higher than in 2020. EVs remain the main source of growth as their deployment continues to expand across major markets. At the same time, energy storage is becoming an increasingly important source of demand growth. In the STEPS, lithium demand from energy storage rises to around 70 kt in 2040 and reaches 90 kt in 2050, around three times today’s level. In the HDS, demand from storage reaches 120 kt in 2050, underlining the growing role of batteries in power systems with rising shares of variable renewables.

- `Source: GCMO2026, p. 145 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Lithium recycling to rise 25-fold, moderating mining needs`

> Secondary lithium production from recycling reaches around 250 kt in 2050, around 25 times higher than today, as larger volumes of end-of-life batteries become available and collection and processing systems improve. In the HDS, which assumes stronger recycling rates, secondary supply rises further to around 560 kt in 2050. This growing contribution from recycling does not remove the need for large-scale investment in new supply, but it helps ease pressure on primary production and improve supply security over time.

- `Source: GCMO2026, p. 141 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Growing strains on hard-rock lithium supplies`

> Hard-rock ore, and particularly spodumene, is increasingly becoming the dominant source of lithium supply compared with brine-based resources. The market for hard-rock ores tightened significantly over the course of 2025, due to strong feedstock demand and mining supply constraints. In 2025, lithium chemical output grew by 32%, whereas mined output grew by 18%. In 2025, Argentina saw faster growth output than the historical major producers, Chile, China and Australia. New entrants are reshaping the supply landscape, particularly in Africa: mined output from the continent grew by 44%, helping diversify supply but also involving challenges related to infrastructure and logistics. While three regions, the South American “lithium triangle”, China and Australia, account for the majority of lithium supplies today, African nations now represent 14% of global supplies, a 26-fold increase from 2020. While contributing to the diversification of mining supply, this trend could, however, reinforce the dominance of the top refining country, as over 65% of new lithium mining capacity on the continent is owned by companies headquartered in China. With the rise of regional output, the importance of small-scale mining is slowly expanding, bringing its own challenges. This year, significant steps were also taken to increase European output. In 2025, Finland’s Keliber mine began operating, with a planned annual capacity of 2.5 kt before 2030, sufficient to meet 90% of European demand for cathode production in the short term. France is also accelerating strategic mining projects, such as the Allier hard-rock lithium and Alsace brine projects.

</details>

## q26 (multi)

**Question:** What price did lithium carbonate reach during its early-2026 rebound, and how could sodium-ion battery capability help manufacturers manage exposure to such price spikes?

**Reference:** Lithium carbonate reached about USD 20000 per tonne of lithium carbonate equivalent in early 2026. Maintaining sodium-ion expertise and production capacity can help battery manufacturers reduce exposure to lithium price spikes.

**Answer:**

> Lithium carbonate prices rebounded sharply in early 2026, nearly doubling to about USD 20,000 per tonne of lithium carbonate equivalent (GCMO2026, p. 140). Large battery manufacturers who maintain multiple supply chains in parallel can use sodium-ion battery expertise and production capacity to reduce their exposure to such lithium price spikes, as sodium-ion chemistries do not rely on lithium (GEVO2026, pp. 100-101).

**Cited passages (3):**

- `Source: GCMO2026, p. 140 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Lithium prices back on the rise`

> Lithium prices rebounded sharply in early 2026, with lithium carbonate prices nearly doubling over a short period to about USD 20 000 per tonne of lithium carbonate equivalent. This reflected tightening upstream supply conditions caused by overseas bans on ore exports by Zimbabwe, as well as tighter permitting in China’s Jiangxi region. Restocking by downstream cathode buyers also added to price pressure. This marked a recovery from two years of weak market conditions, when oversupply and destocking pushed prices down. Current prices remain moderate compared with the peaks observed in 2022, when they reached USD 80 000 per tonne of lithium carbonate equivalent. A fall back in lithium prices remains possible, which could typically be caused by a resumption of lepidolite mining in China, a stabilisation of lithium ore trade flows or a rise in inventories at cathode production plants.

- `Source: GEVO2026, pp. 100-101 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Sodium-ion batteries are entering the scale-up phase`

> The first sodium-ion battery-powered electric car was introduced in China only in late 2023, but the technology is now being scaled up by leading battery producers such as CATL and BYD. Sodium-ion batteries perform significantly better at low temperatures than lithium-ion batteries, particularly LFP chemistries. The latest generation of sodium-ion batteries can retain around 90% of nominal capacity at temperatures as low as -40°C, and can operate at temperatures as high as 70°C. For the largest battery manufacturers, who can maintain multiple supply chains in parallel, expertise and production capacity for sodium-ion batteries can also help to reduce exposure to lithium price spikes. Despite recent progress, sodium-ion batteries remain constrained by lower energy density than lithium-ion technologies, limiting their competitiveness with LFP batteries at current lithium prices. The latest sodium-ion cells can reach up to 175 Wh/kg, compared with up to 205 Wh/kg for the latest generation of LFP batteries and 265 Wh/kg for lithium nickel cobalt manganese oxide (NMC) batteries. Their disadvantage is even greater in terms of volumetric energy density (Wh/l), which translates into a driving range of up to 350 km for an average SUV equipped with a sodium-ion battery, compared with a range of 400-600 km for lithium-ion batteries under average weather conditions.

- `Source: GEVO2026, p. 100 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · *`

> Today’s record low battery prices are partly sustained by losses incurred further upstream in the supply chain, particularly among producers of cathode active materials (CAMs). Cathode active material is the single most important component influencing battery cell production costs, accounting for 40-50% for NMC batteries and 25-30% for LFP batteries. Yet many of the leading CAM producers have been operating at a significant loss since 2023. This challenging market environment is not limited to NMC material producers, whose demand outlook has been dampened by the rapid rise of LFP batteries in recent years. LFP producers in China are also experiencing sustained losses, with the exception of Hunan Yuneng, the world’s largest LFP material supplier. These conditions are unlikely to be sustainable in the long term. They could trigger consolidation in the LFP material market, increasing its market concentration, or lead to greater pricing power among remaining producers. Either outcome could exert upward pressure on battery prices.

<details><summary>Other retrieved passages (7)</summary>

- `Source: GCMO2026, p. 142 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Recycling and market maturity`

> Secondary supply continues to scale rapidly, with recycled volumes increasing by over 40% year-on-year in 2025. However, it still accounts for only around 5% of total supply, highlighting both its growing importance and its current limitations in materially contributing to overall supply growth. The lithium market is gradually becoming more structured, as reflected in record trading volumes for lithium futures and the development of forward pricing tools. Downstream players are increasingly securing long-term supply, as illustrated by recent deals involving MinRes and POSCO, as well as Pilbara Minerals and Canmax.

- `Source: GCMO2026, p. 8 | Global Critical Minerals Outlook 2026 (2026) | Executive summary · Executive summary`

> Critical mineral investment declined by 9% in 2025, ending several years of growth. Amid rising geopolitical tensions and price volatility, investors became more cautious despite strong underlying demand. Battery metals saw the sharpest pullback, with capital spending falling by more than 20% – the largest decline in over a decade – and lithium companies cutting investment by around 40%. By contrast, spending by copper-focused companies increased by 8%, reflecting confidence in copper's long-term prospects. Exploration spending also declined by more than 10%, with modest growth in spending on uranium and steady spending on copper offset by around 45% declines in lithium and nickel. Most regions recorded lower exploration spending, although Asia Pacific bucked the trend with a 20% increase. Merges and acquisitions rebounded in 2025, with strong demand for high-quality copper assets driving a 20% increase in overall deal value compared with 2024. Venture capital investment also recovered, increasingly targeting artificial intelligence (AI) technologies that could improve the efficiency of mineral exploration and resource extraction. Public finance is increasingly being deployed to accelerate critical mineral investment. Governments are taking a more active role in reducing project risks and mobilising private capital. Public finance commitments in advanced economies reached around USD 65 billion in 2025, over four times higher than in 2023. However, a considerable gap remains between commitments and actual disbursements, which will ultimately determine their impact on supply diversification.

- `Source: GCMO2026, p. 145 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Lithium recycling to rise 25-fold, moderating mining needs`

> Secondary lithium production from recycling reaches around 250 kt in 2050, around 25 times higher than today, as larger volumes of end-of-life batteries become available and collection and processing systems improve. In the HDS, which assumes stronger recycling rates, secondary supply rises further to around 560 kt in 2050. This growing contribution from recycling does not remove the need for large-scale investment in new supply, but it helps ease pressure on primary production and improve supply security over time.

- `Source: GCMO2026, pp. 141-142 | Global Critical Minerals Outlook 2026 (2026) | 2. Outlook for key minerals: Part 1 · Increasing lithium refining concentration`

> Global lithium refining output grew rapidly in 2025, with Chinese output expanding by close to 40% year-on-year due to the ramp-up of new capacity, such as Ganfengs’s new Dazhou plant (7.2 kt of capacity each), as well as increased utilisation. Some new capacity also emerged in the United States, Korea, Indonesia and Australia but has yet to ramp up, as average utilisation rates remain well below those of China. Overall, this led to increased concentration in lithium refining output, with China’s share rising from 70% in 2024 to 75% in 2025. The first half of 2026 was marked by the start of the first lithium refining plant in Africa, with the ramp-up of a China-owned Zhejiang Huayou factory in Zimbabwe. The plant, at a total investment cost of USD 400 million, is designed to refine about 6.5 kt in the form of sulphate, which can then be further refined overseas into carbonate or hydroxide and then battery chemicals. Market conditions remained uneven across products. Lithium hydroxide, a chemical used in nickel-rich chemistries, continued to perform less strongly than carbonate, due to the rise of LFP chemistries. This continued to weigh on hydroxide refineries, as well as those converting carbonate into hydroxide, and led to curtailments outside China, including at Australia’s Kemerton plant.

- `Source: GEVO2026, pp. 93-94 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Battery prices continued to decrease, albeit unevenly`

> Average battery prices declined by 8% in 2025, supported by continued improvements in manufacturing efficiency, advances and shifts in battery chemistries and technology, and intensifying global market competition (see Battery manufacturing and trade for more details). Relatively low critical mineral prices also contributed to downward cost pressure, although lithium and cobalt experienced notable price increases over the year. The recent increase in lithium and cobalt prices – if sustained – could put upward pressure on battery costs as stockpiles of minerals purchased at lower prices are being drained. Lithium prices at the beginning of 2026 were more than twice as high as in the same period in 2025, even though they remained around 70% lower than their 2022 peak. Several factors contributed to this rise, including faster-than-anticipated demand growth – particularly from the battery energy storage sector –, relatively low inventories in China and temporary supply disruptions, such as the suspension of operations at CATL’s Jianxiawo lithium mine. If these upward price trends persist, they could exert upward pressure on lithium-ion battery prices and reinforce the current momentum behind sodium-ion batteries, which offer lower ranges but do not rely on lithium. This effect could nevertheless be tempered by existing long-term contracts for lithium supply and vertical integration among major battery producers.

- `Source: GEVO2026, p. 101 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Sodium-ion batteries are entering the scale-up phase`

> Sodium-ion batteries are therefore expected to be better suited for small-range electric cars, light commercial vehicles operating in urban areas, two-and three-wheelers, industrial equipment such as forklifts, and battery stationary storage. They can also help reduce range losses in cold weather when used in hybrid EV battery packs combining lithium-ion and sodium-ion chemistries. Global supply chains for sodium-ion batteries are also far less developed than for lithium-ion batteries, limiting the near-term prospect of large-scale deployment. For example, the supply chain of hard carbon – the anode active material used in sodium-ion batteries as a substitute for graphite – is still poorly developed today and largely concentrated in China. Battery manufacturing capacity is also significantly smaller. Current sodium-ion battery cell manufacturing capacity is equal to just over 1% of that of lithium-ion cells, and announced projects for 2030 amount to only about 7% of the committed lithium-ion manufacturing capacity for the same year.

- `Source: GEVO2025, p. 13 | Global EV Outlook 2025 (2025) | Executive summary · Competition and declining battery prices are improving affordability, though progress is uneven`

> Low critical mineral prices and increasing competition between battery manufacturers drove down battery pack prices in all markets in 2024, albeit with significant variations. In China, prices fell by about 30%, compared with 10-15% in Europe and the United States. The faster pace of cost reductions in China – enabled by strong competition, increasing manufacturing efficiency and supply chain integration, and access to a skilled workforce – is increasing the competitive advantage of Chinese battery manufacturers.

</details>

## q27 (unanswerable)

**Question:** Which car manufacturer sold the most electric cars in Spain in 2025?

**Reference:** The corpus does not identify the best-selling electric car manufacturer in Spain in 2025; the assistant should state that it cannot determine the answer from the available documents.

**Answer:**

> The corpus does not cover which specific car manufacturer sold the most electric cars in Spain in 2025. It only notes that Spain experienced 80% electric car sales growth in 2025 supported by purchase subsidies (GEVO2026, p. 21).

**Cited passages (1):**

- `Source: GEVO2026, p. 21 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales saw strong growth in Europe in 2025, thanks to policy support`

> In Germany, the largest electric car market in Europe, electric car sales increased by 50% in 2025, to reach a record high of 850 000. This rebound was supported not only by preferential tax treatment for electric company cars, but also by the wider availability of more affordable models, which contributed to a fall in the average battery electric vehicle (BEV) price of around 6% in 2025. Around 30% of cars sold in Germany in 2025 were electric, just slightly below the 31% sales share achieved in 2022. In France, battery electric car sales increased by almost 15% in 2025 while PHEV sales decreased by 25%. As a result, the electric sales share remained similar to 2024 levels, representing around 25% of total car sales. Impressive sales growth in Italy (+65%), Poland (+125%) and Spain (+80%) was supported by the reintroduction or continuation of EV purchase subsidies in 2025.

<details><summary>Other retrieved passages (6)</summary>

- `Source: GEVO2026, pp. 46-47 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Strong growth expected in Europe and emerging markets in 2026`

> In China, the world’s largest EV market, sales are expected to reach more than 14 million, growing by close to 8% year-on-year. This level of growth reflects weaker performance in the early months of the year, partly driven by the introduction of caps to trade-in incentives (scrappage schemes). At the same time, long-standing purchase tax exemptions for new energy vehicles (NEVs) are being phased out (see Q1 sales). However, the market share of electric cars is expected to grow to close to 60%, despite a weak overall car market, supported by a highly competitive domestic industry and extensive model availability. In Europe, electric car sales are set to maintain robust momentum in 2026. Policy support is strengthening in key markets, with Germany reintroducing incentives and Spain advancing its Plan Auto+ programme. In the United Kingdom, the mandated share of zero-emission vehicles rises to 33% under the Vehicle Emissions Trading Schemes, up from 28% in 2025.At the same time, increased competition, including from Chinese manufacturers, is expanding consumer choice, particularly in more affordable segments. As a result, European EV sales are expected to reach 5 million, marking an increase of close to 20%.

- `Source: GEVO2026, p. 17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> Market developments varied across regions. In the People’s Republic of China (hereafter, “China”), growth slowed slightly partly as a result of its trade-in scheme being temporary halted, but the country still accounted for more than half of the global increase in electric car sales in 2025. Europe experienced an upswing in sales following a step change in the EU CO2 standards, with sales rising 30% to more than 4 million after having stagnated in 2024. In the United States, the sales share of electric cars remained relatively stable at just below 10%, despite several policy shifts, including the ending of tax credits, which resulted in sales falling significantly in the last quarter of the year. Meanwhile, outside of these major car markets, sales continued to expand rapidly.

- `Source: GEVO2026, p. 45 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales are expected to grow 10% in 2026, but uncertainties are high`

> Market and policy fundamentals for 2026 point towards growth in electric car sales, but data on low sales figures in the first quarter of 2026 suggest that the rate of growth is likely to be more moderate than previously expected. China has scaled back incentives, and in the United States, manufacturers are reassessing electrification strategies. In Europe and Southeast Asia, demand is being driven by a combination of policy action and the improving affordability of electric cars. Overall, global electric car sales are expected to reach around 23 million, representing growth of approximately 10%.

- `Source: GEVO2026, pp. 13-14 | Global EV Outlook 2026 (2026) | Executive summary · Trade plays an important role in the EV industry`

> China remains the world’s largest EV manufacturing hub, accounting for nearly 75% of electric cars produced in 2025. Almost 22 million electric cars were produced globally in 2025 – a more than 25% increase on the previous year. Intense domestic competition in China is squeezing profit margins, pushing manufacturers to seek higher profits overseas. Chinese electric car exports doubled to a record high of over 2.5 million in 2025, as production outstripped domestic demand. In 2024, China overtook the European Union to become the largest exporter of cars; in 2025, more than 35% of China’s car exports were EVs, up from 20% in 2024. Imports from China accounted for 55% of electric car sales in 2025 in countries outside Europe and the United States, up from less than 5% just 5 years earlier. More than half of electric cars sold in Southeast Asia in 2025 were by Chinese brands, while one-third came from a Vietnamese manufacturer.

- `Source: GEVO2026, p. 37 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Just five models represent around 20% of global battery electric car sales`

> While model availability shapes consumer choice, greater availability is not necessary reflected in EV purchase decisions; instead, buyers often tend to pick one of a relatively small number of very popular models. In 2025, 630 battery electric car models were available globally, yet sales remained highly concentrated across a small group of best-selling models. In 2025, just five models accounted for about 20% of global battery electric car sales: the Tesla Model Y made up nearly 8% of total battery electric car sales, followed by the Tesla Model 3 (3.6%), Geely Geome Xingyuan (3.5%), Wuling HongGuang Mini (3.1%), and BYD Seagull (3.0%). As a result, just 1% of available BEV models captured one-fifth of the entire global market. The top-selling 35 models accounted for around half of global battery electric car sales. Nevertheless, as EV adoption grows, automakers tend to offer a greater range of electric car models, which leads to a diversification of consumer choice. As recently as 2020, only two models accounted for about 20% of global battery electric car sales. Sales are also concentrated in terms of where their manufacturers are headquartered. Chinese manufacturers accounted for more than half of the total BEV models available, and of global BEV sales in 2025. Manufacturers headquartered in Europe accounted for nearly one-fifth of models sold, followed by those based in United States, which made up nearly 10% (see Chapter 7 for the latest manufacturing and trade trends).

- `Source: GEVO2026, p. 31 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Eurasian and Middle East regions show continued growth`

> Electric car sales in the Middle East reached around 75 000 in 2025, expanding by more than 40% year-on-year. The United Arab Emirates remained the region’s largest electric car market, accounting for almost 50% of sales, though its share of the regional market has declined from over 60% in 2023 as neighbouring markets have gained momentum. Sales have grown particularly quickly in Qatar and Saudi Arabia, which together now represent nearly 45% of regional demand. Market preferences have also shifted markedly in recent years. When electric car sales first began to scale in 2020, US-manufactured Tesla models accounted for about half of all sales. Today, Tesla’s share has fallen to around 15%, while BYD – which entered the regional market in 2022 – has rapidly expanded to a 60% market share.

</details>

## q28 (unanswerable)

**Question:** What was the average total cost in euros of installing a private 7.4 kW home charger in Madrid in 2025?

**Reference:** The corpus does not provide the average installed cost of a private 7.4 kW home charger in Madrid in 2025; the assistant should state that the information is unavailable.

**Answer:**

> The corpus does not cover this.

**Cited passages (0):**

<details><summary>Other retrieved passages (6)</summary>

- `Source: GEVO2026, p. 53 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · In Europe, new model releases and pricing strategies cut electric car prices after years of increases`

> In Europe, affordability remains the most cited barrier to wider adoption: A 2025 survey of 3 000 EU citizens revealed that many consumers would not be willing to pay more for a BEV than a comparable ICE model. While fewer than 10% of available BEV models in Europe were priced under EUR 30 000, the survey highlighted a willingness-to-pay a median price of around EUR 20 000.

- `Source: GEVO2026, pp. 65-66 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · Electric car sales growth and tax exemptions offset declining subsidies in Europe`

> Despite several countries in Europe having reduced or phased out purchase subsidies in recent years, especially for middle-to high-income households, increasing electric car sales pushed government support to a record high of over USD 11 billion in 2025, up more than 40% from the previous year. Belgium, the Netherlands and Austria all ended their purchase subsidy schemes in December 2024. This followed the end of subsidy programmes in the United Kingdom, Sweden and Finland in 2022, the phase-out of subsidies in Germany in 2023, and a scale-back of subsidies in France in 2023. However, measures in some other European countries also contributed to higher regional spending in 2025. The United Kingdom reinstated purchase subsidies in 2025 with the GBP 650 million (about USD 830 million) “Electric Car Grant”, supporting the sales of a few eligible electric models priced below GBP 37 000 (about USD 47 000). Italy doubled per-vehicle support through the revised “Eco bonus,” which targets lower-income households scrapping older vehicles. In Spain, strong growth in electric car sales increased the fiscal cost of the extended “MOVES III” subsidy programme. The launch of the “NaszEauto” EV subsidy scheme in Poland also contributed to government spending in Europe in 2025, albeit to a negligible extent, as its electric car market remains relatively small.

- `Source: GEVO2026, p. 53 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · In Europe, new model releases and pricing strategies cut electric car prices after years of increases`

> The affordability of electric models made substantial progress in Europe in 2025, with the average price of battery electric cars decreasing for the first time following years of increases. The EU CO2 standards’ 2025 target pushed carmakers to introduce more affordable models to the market, such as the Renault 5 E-Tech, the Hyundai Inster, Tesla’s Model 3 and Model Y (with standard trims), and new Chinese models hit the European market. As a result, in Germany and the United Kingdom, the larger range of model and trim offerings explained about one-third of the year-on-year price decline observed in 2025. The remainder can be explained by the decrease in battery prices and other factors such as original equipment makers (OEMs)’ pricing strategies. However, this price drop would have been more pronounced had there not been a concurrent shift to larger and heavier models. In 2025, the average retail price of battery electric cars would have been roughly 20% lower in Germany and more than 5% lower in the United Kingdom without the increasing transition to SUVs and larger models that has taken place since 2021.

- `Source: GEVO2025, p. 13 | Global EV Outlook 2025 (2025) | Executive summary · Improving charging coverage, capacity and integration is key to growing adoption of electric vehicles`

> Public charging stations have doubled in the past 2 years to keep up with growing EV sales. China and the European Union have maintained a steady pace of charger deployment compared with the number of EVs on the road. However, in both the United States and United Kingdom, which have higher rates of access to home chargers than China, public charger build-out has not kept pace with EV deployment, and the number of electric light-duty vehicles per public charging point increased in 2024. Charging capacity is an important measure of the adequacy of public charging networks. The number of ultra-fast chargers, with power ratings of 150 kilowatts (kW) and above, grew by about 50% in 2024 and now account for nearly 10% of all public fast chargers. Public slow chargers in urban areas are a solution for EV owners without access to home charging, but fast chargers along highways help enable long-distance trips. In Europe, over three-quarters of all highways have a fast-charging station at least every 50 kilometres, compared with less than half of US highways. Globally, public charging capacity for light-duty EVs would need to grow by almost ninefold to 2030 to support EV sales implied by stated policies. Even so, EVs are set to account for only 2.5% of total global electricity demand in 2030.

- `Source: GEVO2025, p. 14 | Global EV Outlook 2025 (2025) | Executive summary · Improving charging coverage, capacity and integration is key to growing adoption of electric vehicles`

> Government efforts to promote interoperability, standardisation, smart charging and vehicle-to-grid integration can ease the transition to EVs for drivers and grid operators. Technologies such as smart chargers and vehicle-to-grid-capable EV models are becoming more available, but new market structures and legal frameworks will be needed for vehicles to maximise the potential benefits for the grid. China and the United Kingdom stand out for policy implementation and demonstration projects in this area. Battery technology innovations in recent years are also enabling safe high-power charging that could be as quick as refuelling a conventional car, but fully realising these advances hinges on deploying adequate infrastructure.

- `Source: GEVO2026, pp. 48-49 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · Electric car prices fell in major markets, but the lack of low-cost models still limits affordability in some`

> The upfront price of electric cars compared to their internal combustion engine (ICE) equivalents remains a barrier to wider adoption. Over the past decade, declining battery manufacturing costs and the introduction of new affordable models mean the price-competitiveness of electric cars has made significant strides. However, the shift towards larger batteries and larger vehicle segments in many markets over the past 5 years has limited the impact of these cost reductions on purchase prices. In 2025, the sales-weighted average purchase price of electric cars declined across almost all segments across the three markets covered in this section – the People’s Republic of China (hereafter, “China”), Germany and the United States. Across all three, a decrease in battery cell prices and manufacturers’ pricing strategies contributed to cost declines, although new model entries in each market had differing effects on average battery electric vehicle (BEV) prices. In China, while prices fell within most segments, the introduction of new models put upward pressure on average BEV prices, as many of these were SUVs. The rising share of SUVs and increasing average battery sizes would have led to a roughly 3% increase in prices, but this effect was more than offset by declining battery cell prices (Figure 5.4), as well as non-battery component cost declines and carmakers’ aggressive pricing strategies in the increasingly competitive electric vehicle (EV) market. The overall result was a net drop of more than 10% in average BEV prices in 2025.

</details>

## q29 (unanswerable)

**Question:** What percentage of new passenger cars sold in Spain is projected to be battery electric in 2040?

**Reference:** The corpus does not provide a Spain-specific projection for the battery electric share of new passenger car sales in 2040; the assistant should not invent a percentage.

**Answer:**

> The corpus does not cover projections for Spain in 2040. It does mention that Spain is advancing its Plan Auto+ programme supporting electric vehicle sales in 2026 (GEVO2026, pp. 46-47).

**Cited passages (1):**

- `Source: GEVO2026, pp. 46-47 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Strong growth expected in Europe and emerging markets in 2026`

> In China, the world’s largest EV market, sales are expected to reach more than 14 million, growing by close to 8% year-on-year. This level of growth reflects weaker performance in the early months of the year, partly driven by the introduction of caps to trade-in incentives (scrappage schemes). At the same time, long-standing purchase tax exemptions for new energy vehicles (NEVs) are being phased out (see Q1 sales). However, the market share of electric cars is expected to grow to close to 60%, despite a weak overall car market, supported by a highly competitive domestic industry and extensive model availability. In Europe, electric car sales are set to maintain robust momentum in 2026. Policy support is strengthening in key markets, with Germany reintroducing incentives and Spain advancing its Plan Auto+ programme. In the United Kingdom, the mandated share of zero-emission vehicles rises to 33% under the Vehicle Emissions Trading Schemes, up from 28% in 2025.At the same time, increased competition, including from Chinese manufacturers, is expanding consumer choice, particularly in more affordable segments. As a result, European EV sales are expected to reach 5 million, marking an increase of close to 20%.

<details><summary>Other retrieved passages (5)</summary>

- `Source: GEVO2026, p. 201 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · European policies continue to support the transition to EVs, while introducing some flexibilities`

> Electric car sales also rise in the rest of Europe on aggregate, on the back of impressive momentum in large markets such as Türkiye. Although support varies a lot at the national level, strong policies in some countries drive Europe’s sales share of electric cars and vans to around 90% in 2035 in the CPS and close to 85% in the STEPS, up from around 25% today.

- `Source: GEVO2026, pp. 199-200 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · European policies continue to support the transition to EVs, while introducing some flexibilities`

> Maximum amount of “low-carbon” crude steel demand implied by the proposed Automotive Package, near-zero emissions steel demand commitments and announced projects in the European Union Current publicly announced demand commitments and offtake agreements for near-zero emissions steel in the European Union amount to almost 6 Mt, of which around 1 Mt is linked to automotive manufacturers and suppliers. However, the majority of agreements have been signed without publicly disclosed volumes, and so actual demand could be higher. The proposed Automotive Package therefore has the potential to expand demand for “low-carbon” steel for this industry beyond current commitments. However, the final impact of the proposed package in de-risking “low-carbon” steel projects remains uncertain. In the low-demand case, which considers the more stringent end-point emissions intensity, the estimated induced demand for “low-carbon” steel exceeds the roughly 6 Mt of near-zero emissions steel capacity currently announced in the European Union. In the high-demand case, the package could stimulate demand at a scale sufficient to support the advancement of a broader pipeline of projects, including some currently at earlier stages of development. However a more lenient threshold for “low-carbon” steel that would increase the volume of steel eligible for credits, – while delivering the same emissions reductions – could weaken the business case for more innovative projects deploying deep decarbonisation technologies.

- `Source: GEVO2026, p. 22 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales saw strong growth in Europe in 2025, thanks to policy support`

> Across Europe, the share of BEVs in electric car sales has increased steadily over the past few years, supported by emission standards that favour zero-emission vehicles, in particular the EU CO2 standards. The BEV share in electric car sales rose from 55% in 2020 to nearly 70% in 2025. As a result, Europe and China reached similar shares of BEVs in EVs in 2025, with Europe ending the year slightly higher. Overall, electric cars now represent about 5% of the European car fleet. Norway leads, with more than one-third of the car stock being electric. Within the European Union, only Denmark has a stock share above 20%, reflecting the lag between rapid sales uptake and stock turnover.

- `Source: GEVO2026, p. 202 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · European policies continue to support the transition to EVs, while introducing some flexibilities`

> Overall, electric sales across all vehicle types (excluding 2/3Ws) in Europe reach over 80% by 2035 in the STEPS, with passenger cars representing the bulk of sales, while the CPS assumes stronger growth at more than 85% under current policies; the impact of flexibilities is not included in the latter scenario.

- `Source: GEVO2026, p. 235 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Rising local EV production in EMDEs and tightening trade policies challenge Chinese imports`

> In 2025, nearly two-thirds of electric car sales in EMDEs other than China were Chinese imports. By 2030, in the STEPS, although Chinese exports to other EMDEs grow more than 70% from 2025 levels, to exceed 1.2 million units, their share in these markets falls below 40%, as local output grows. By 2035, exports to EMDEs could reach around 1.6 million units – one-fifth of China’s total exports – but make up only 25% of total EMDE sales

</details>

## q30 (unanswerable)

**Question:** What percentage of all new cars sold in Spain in 2025 were electric, including both battery electric and plug-in hybrid cars?

**Reference:** The indexed text does not state Spain's electric car sales share in 2025. The reported 80% increase is year-on-year sales growth, not market share; the assistant should state that the requested share is unavailable.

**Answer:**

> The corpus does not state the exact percentage of new cars sold in Spain in 2025 that were electric. It only notes that Spain experienced impressive electric car sales growth of 80% in 2025 supported by the reintroduction or continuation of EV purchase subsidies (GEVO2026, p. 21).

**Cited passages (1):**

- `Source: GEVO2026, p. 21 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales saw strong growth in Europe in 2025, thanks to policy support`

> In Germany, the largest electric car market in Europe, electric car sales increased by 50% in 2025, to reach a record high of 850 000. This rebound was supported not only by preferential tax treatment for electric company cars, but also by the wider availability of more affordable models, which contributed to a fall in the average battery electric vehicle (BEV) price of around 6% in 2025. Around 30% of cars sold in Germany in 2025 were electric, just slightly below the 31% sales share achieved in 2022. In France, battery electric car sales increased by almost 15% in 2025 while PHEV sales decreased by 25%. As a result, the electric sales share remained similar to 2024 levels, representing around 25% of total car sales. Impressive sales growth in Italy (+65%), Poland (+125%) and Spain (+80%) was supported by the reintroduction or continuation of EV purchase subsidies in 2025.

<details><summary>Other retrieved passages (9)</summary>

- `Source: GEVO2026, pp. 32-33 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · The number of electric car models keeps growing, in contrast to conventional car models`

> Some 2 500 car models were available worldwide in 2025. Nearly 1 000 of these were electric cars, about 40% of the total, up from about 35% in 2024. Counting both battery electric and plug-in hybrid electric models, the number of electric car models has more than doubled in the past five years. In 2025, the number of electric car models available worldwide increased by slightly more than 25%, a larger increase than the just over 15% seen in 2024. Hybrid model availability also continued to expand, rising by over 10% year-on-year to more than 200 models in 2025. By contrast, the number of internal combustion engine (ICE) car models remained constant in 2025 – the only powertrain category to do so. The total number of electric car models could exceed 1 100 in 2026, based on recent original equipment manufacturer (OEM) announcements, growing at around 15% compared to the previous year. BEVs continue to account for around 65% of all electric car models, a share that has remained broadly stable since 2015. Looking forward, the share of PHEVs in total electric car models is expected to decline from around 35% in 2026 to around 30% by the end of the decade.

- `Source: GEVO2026, p. 17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> Market developments varied across regions. In the People’s Republic of China (hereafter, “China”), growth slowed slightly partly as a result of its trade-in scheme being temporary halted, but the country still accounted for more than half of the global increase in electric car sales in 2025. Europe experienced an upswing in sales following a step change in the EU CO2 standards, with sales rising 30% to more than 4 million after having stagnated in 2024. In the United States, the sales share of electric cars remained relatively stable at just below 10%, despite several policy shifts, including the ending of tax credits, which resulted in sales falling significantly in the last quarter of the year. Meanwhile, outside of these major car markets, sales continued to expand rapidly.

- `Source: GEVO2026, p. 11 | Global EV Outlook 2026 (2026) | Executive summary · Electric cars are poised to make up a greater share of total car sales in 2026`

> Global electric car sales are expected to grow to 23 million in 2026, representing 28% of total car sales. Europe is poised for the largest growth among major markets, with sales projected to increase by around 20% in 2026, such that one in three cars sold are electric. In China, electric car sales are set to grow across 2026, albeit at a slower rate than in previous years, to reach almost 60% of total car sales. Sales across Asia Pacific countries other than China are expected to grow by over 50%, while sales in Latin America are projected to rise by 45%. The wider economic impacts of the conflict in the Middle East might temper overall car sales. In many regions, however, there is upside potential to the 2026 EV forecast depending, in part, on how, when and which policies are enacted amid the current energy crisis.

- `Source: GEVO2026, p. 37 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Just five models represent around 20% of global battery electric car sales`

> While model availability shapes consumer choice, greater availability is not necessary reflected in EV purchase decisions; instead, buyers often tend to pick one of a relatively small number of very popular models. In 2025, 630 battery electric car models were available globally, yet sales remained highly concentrated across a small group of best-selling models. In 2025, just five models accounted for about 20% of global battery electric car sales: the Tesla Model Y made up nearly 8% of total battery electric car sales, followed by the Tesla Model 3 (3.6%), Geely Geome Xingyuan (3.5%), Wuling HongGuang Mini (3.1%), and BYD Seagull (3.0%). As a result, just 1% of available BEV models captured one-fifth of the entire global market. The top-selling 35 models accounted for around half of global battery electric car sales. Nevertheless, as EV adoption grows, automakers tend to offer a greater range of electric car models, which leads to a diversification of consumer choice. As recently as 2020, only two models accounted for about 20% of global battery electric car sales. Sales are also concentrated in terms of where their manufacturers are headquartered. Chinese manufacturers accounted for more than half of the total BEV models available, and of global BEV sales in 2025. Manufacturers headquartered in Europe accounted for nearly one-fifth of models sold, followed by those based in United States, which made up nearly 10% (see Chapter 7 for the latest manufacturing and trade trends).

- `Source: GEVO2026, pp. 16-17 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · One in four new cars sold worldwide was electric in 2025`

> The electric car market reached new highs in 2025, growing by 20% from 2024 to exceed 20 million sales, in line with expectations in the 2025 edition of the Global EV Outlook. The sales share of electric cars in the overall car market increased to 25%. This marked the fifth consecutive year in which annual electric car sales increased by about 3.5 million, a trend that began in 2021 after the Covid-19 pandemic. As a result, about 5% of the global car stock is now electrified, displacing 1.2 million barrels of oil per day in 2025 (see Annex A). In particular, 2025 saw a boost for battery electric cars. The share of battery electric cars in total electric car sales increased to 65%, reversing the trend seen in the 2 years prior. While 2024 saw a strong increase in extended-range electric vehicles (EREVs), this did not continue in 2025, dropping to less than 7% of total electric car sales, after rising to 7.5% in 2024.

- `Source: GEVO2026, pp. 46-47 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Strong growth expected in Europe and emerging markets in 2026`

> In China, the world’s largest EV market, sales are expected to reach more than 14 million, growing by close to 8% year-on-year. This level of growth reflects weaker performance in the early months of the year, partly driven by the introduction of caps to trade-in incentives (scrappage schemes). At the same time, long-standing purchase tax exemptions for new energy vehicles (NEVs) are being phased out (see Q1 sales). However, the market share of electric cars is expected to grow to close to 60%, despite a weak overall car market, supported by a highly competitive domestic industry and extensive model availability. In Europe, electric car sales are set to maintain robust momentum in 2026. Policy support is strengthening in key markets, with Germany reintroducing incentives and Spain advancing its Plan Auto+ programme. In the United Kingdom, the mandated share of zero-emission vehicles rises to 33% under the Vehicle Emissions Trading Schemes, up from 28% in 2025.At the same time, increased competition, including from Chinese manufacturers, is expanding consumer choice, particularly in more affordable segments. As a result, European EV sales are expected to reach 5 million, marking an increase of close to 20%.

- `Source: GEVO2026, p. 45 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales are expected to grow 10% in 2026, but uncertainties are high`

> Market and policy fundamentals for 2026 point towards growth in electric car sales, but data on low sales figures in the first quarter of 2026 suggest that the rate of growth is likely to be more moderate than previously expected. China has scaled back incentives, and in the United States, manufacturers are reassessing electrification strategies. In Europe and Southeast Asia, demand is being driven by a combination of policy action and the improving affordability of electric cars. Overall, global electric car sales are expected to reach around 23 million, representing growth of approximately 10%.

- `Source: GEVO2026, p. 235 | Global EV Outlook 2026 (2026) | Chapter 9. EV and battery outlook · Rising local EV production in EMDEs and tightening trade policies challenge Chinese imports`

> In 2025, nearly two-thirds of electric car sales in EMDEs other than China were Chinese imports. By 2030, in the STEPS, although Chinese exports to other EMDEs grow more than 70% from 2025 levels, to exceed 1.2 million units, their share in these markets falls below 40%, as local output grows. By 2035, exports to EMDEs could reach around 1.6 million units – one-fifth of China’s total exports – but make up only 25% of total EMDE sales

- `Source: GEVO2026, p. 22 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales saw strong growth in Europe in 2025, thanks to policy support`

> Across Europe, the share of BEVs in electric car sales has increased steadily over the past few years, supported by emission standards that favour zero-emission vehicles, in particular the EU CO2 standards. The BEV share in electric car sales rose from 55% in 2020 to nearly 70% in 2025. As a result, Europe and China reached similar shares of BEVs in EVs in 2025, with Europe ending the year slightly higher. Overall, electric cars now represent about 5% of the European car fleet. Norway leads, with more than one-third of the car stock being electric. Within the European Union, only Denmark has a stock share above 20%, reflecting the lag between rapid sales uptake and stock turnover.

</details>

## q31 (unanswerable)

**Question:** By what percentage did global average battery pack prices change over the full year 2026 compared with 2025?

**Reference:** The corpus does not report the full-year change in global average battery pack prices for 2026. The 8% decline refers to 2025 compared with 2024 and cannot answer this question.

**Answer:**

> The corpus does not cover the percentage change in global average battery pack prices over the full year 2026. It notes that average battery prices declined by 8% in 2025 (GEVO2026, pp. 93–94).

**Cited passages (1):**

- `Source: GEVO2026, pp. 93-94 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Battery prices continued to decrease, albeit unevenly`

> Average battery prices declined by 8% in 2025, supported by continued improvements in manufacturing efficiency, advances and shifts in battery chemistries and technology, and intensifying global market competition (see Battery manufacturing and trade for more details). Relatively low critical mineral prices also contributed to downward cost pressure, although lithium and cobalt experienced notable price increases over the year. The recent increase in lithium and cobalt prices – if sustained – could put upward pressure on battery costs as stockpiles of minerals purchased at lower prices are being drained. Lithium prices at the beginning of 2026 were more than twice as high as in the same period in 2025, even though they remained around 70% lower than their 2022 peak. Several factors contributed to this rise, including faster-than-anticipated demand growth – particularly from the battery energy storage sector –, relatively low inventories in China and temporary supply disruptions, such as the suspension of operations at CATL’s Jianxiawo lithium mine. If these upward price trends persist, they could exert upward pressure on lithium-ion battery prices and reinforce the current momentum behind sodium-ion batteries, which offer lower ranges but do not rely on lithium. This effect could nevertheless be tempered by existing long-term contracts for lithium supply and vertical integration among major battery producers.

<details><summary>Other retrieved passages (5)</summary>

- `Source: GEVO2026, p. 95 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · Battery prices continued to decrease, albeit unevenly`

> Over the past few years, the average battery price has decreased across all regions, but regional price disparities have widened. In 2025, battery pack prices in China were 30% lower than in North America, and 35% lower than in Europe, compared to a respective 20% and 25% in 2022.

- `Source: GEVO2025, p. 13 | Global EV Outlook 2025 (2025) | Executive summary · Competition and declining battery prices are improving affordability, though progress is uneven`

> Low critical mineral prices and increasing competition between battery manufacturers drove down battery pack prices in all markets in 2024, albeit with significant variations. In China, prices fell by about 30%, compared with 10-15% in Europe and the United States. The faster pace of cost reductions in China – enabled by strong competition, increasing manufacturing efficiency and supply chain integration, and access to a skilled workforce – is increasing the competitive advantage of Chinese battery manufacturers.

- `Source: GEVO2026, pp. 48-49 | Global EV Outlook 2026 (2026) | Chapter 2. Trends in electric car prices · Electric car prices fell in major markets, but the lack of low-cost models still limits affordability in some`

> The upfront price of electric cars compared to their internal combustion engine (ICE) equivalents remains a barrier to wider adoption. Over the past decade, declining battery manufacturing costs and the introduction of new affordable models mean the price-competitiveness of electric cars has made significant strides. However, the shift towards larger batteries and larger vehicle segments in many markets over the past 5 years has limited the impact of these cost reductions on purchase prices. In 2025, the sales-weighted average purchase price of electric cars declined across almost all segments across the three markets covered in this section – the People’s Republic of China (hereafter, “China”), Germany and the United States. Across all three, a decrease in battery cell prices and manufacturers’ pricing strategies contributed to cost declines, although new model entries in each market had differing effects on average battery electric vehicle (BEV) prices. In China, while prices fell within most segments, the introduction of new models put upward pressure on average BEV prices, as many of these were SUVs. The rising share of SUVs and increasing average battery sizes would have led to a roughly 3% increase in prices, but this effect was more than offset by declining battery cell prices (Figure 5.4), as well as non-battery component cost declines and carmakers’ aggressive pricing strategies in the increasingly competitive electric vehicle (EV) market. The overall result was a net drop of more than 10% in average BEV prices in 2025.

- `Source: GEVO2026, p. 100 | Global EV Outlook 2026 (2026) | Chapter 5. Trends in electric vehicle batteries · *`

> Today’s record low battery prices are partly sustained by losses incurred further upstream in the supply chain, particularly among producers of cathode active materials (CAMs). Cathode active material is the single most important component influencing battery cell production costs, accounting for 40-50% for NMC batteries and 25-30% for LFP batteries. Yet many of the leading CAM producers have been operating at a significant loss since 2023. This challenging market environment is not limited to NMC material producers, whose demand outlook has been dampened by the rapid rise of LFP batteries in recent years. LFP producers in China are also experiencing sustained losses, with the exception of Hunan Yuneng, the world’s largest LFP material supplier. These conditions are unlikely to be sustainable in the long term. They could trigger consolidation in the LFP material market, increasing its market concentration, or lead to greater pricing power among remaining producers. Either outcome could exert upward pressure on battery prices.

- `Source: GEVO2025, p. 48 | Global EV Outlook 2025 (2025) | 2. Trends in the electric car industry · Falling battery pack prices and intensifying competition underpin progress in electric car affordability`

> However, the trend towards falling prices has been uneven across markets, due to differences in carmakers’ pricing strategies, and in market maturity and the level of competition. For example, in China, the sales-weighted average (hereafter, “average”) price of a battery electric SUV fell almost 10% year-on-year in 2024, partly due to the 30% decline in the battery pack price. Similarly, in the United States, a 15% decline in battery prices contributed to a 3% drop in the average purchase price of electric SUVs in 2024. In contrast, in Germany, the price of electric SUVs slightly increased in 2024, despite their battery pack prices declining 20%. This suggests that the battery pack price is not the only factor influencing EV prices: other component manufacturing costs, trim levels and carmakers’ pricing strategies also play a significant role.

</details>

## q32 (unanswerable)

**Question:** By what percentage did global electric car sales change in the second quarter of 2026 compared with the second quarter of 2025?

**Reference:** The initial corpus does not report the actual year-on-year change in global electric car sales for the second quarter of 2026; the assistant should state that it cannot answer from the available documents.

**Answer:**

> The corpus does not cover the percentage change in global electric car sales for the second quarter of 2026. It does report that global electric car sales in the first quarter of 2026 were 8% lower than over the same period in 2025 (GEVO2026, p. 11).

**Cited passages (2):**

- `Source: GEVO2026, p. 11 | Global EV Outlook 2026 (2026) | Executive summary · Electric cars are poised to make up a greater share of total car sales in 2026`

> Global electric car sales are expected to grow to 23 million in 2026, representing 28% of total car sales. Europe is poised for the largest growth among major markets, with sales projected to increase by around 20% in 2026, such that one in three cars sold are electric. In China, electric car sales are set to grow across 2026, albeit at a slower rate than in previous years, to reach almost 60% of total car sales. Sales across Asia Pacific countries other than China are expected to grow by over 50%, while sales in Latin America are projected to rise by 45%. The wider economic impacts of the conflict in the Middle East might temper overall car sales. In many regions, however, there is upside potential to the 2026 EV forecast depending, in part, on how, when and which policies are enacted amid the current energy crisis.

- `Source: GEVO2026, p. 11 | Global EV Outlook 2026 (2026) | Executive summary · Electric cars are poised to make up a greater share of total car sales in 2026`

> Electric car sales broke records in a number of marketsduring the first quarter of 2026. Global sales, at around 3.9 million, were 8% lower than over the same period last year, primarily because of lower sales in China and the United States following key policy changes. However, this overall decline masks strong sales growth in many countries: in Europe, sales were up close to 30% year-on-year; countries in Asia Pacific excluding China saw year-on-year sales growth of 80%, and sales across Latin America were up by 75%. In March 2026, around 30 countries saw record-breaking monthly sales, and a further 60 countries recorded year-on-year sales growth. Preliminary April data shows that monthly electric car sales in China grew to a record high of over 60% of total car sales, even if year-to-date electric car sales remained lower than in 2025.

<details><summary>Other retrieved passages (5)</summary>

- `Source: GEVO2026, p. 45 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Electric car sales are expected to grow 10% in 2026, but uncertainties are high`

> Market and policy fundamentals for 2026 point towards growth in electric car sales, but data on low sales figures in the first quarter of 2026 suggest that the rate of growth is likely to be more moderate than previously expected. China has scaled back incentives, and in the United States, manufacturers are reassessing electrification strategies. In Europe and Southeast Asia, demand is being driven by a combination of policy action and the improving affordability of electric cars. Overall, global electric car sales are expected to reach around 23 million, representing growth of approximately 10%.

- `Source: GEVO2026, p. 10 | Global EV Outlook 2026 (2026) | Executive summary · After another record year for EV sales, attention is turning to the impacts of the energy crisis for global car markets`

> Electric car sales grew by 20% globally to exceed 20 million in 2025, meaning one-quarter of all new cars sold were electric. Europe saw the strongest growth among major electric vehicle (EV) markets, with electric car sales rising by more than 30% to reach 28% of total sales, following an increase in the stringency of the European Union’s CO2 standards for cars. China’s growth in electric car sales slowed slightly, in part due to a temporary halt to its trade-in scheme, but EVs still accounted for nearly 55% of all car sales. In the United States, electric car sales remained relatively stable at just under 10% of car sales, though the end of EV tax credits coincided with a drop in sales at the end of the year. Meanwhile, some emerging markets saw steep increases in electric car sales. In Southeast Asia, annual sales more than doubled to reach a sales share of nearly 20%, led by Viet Nam, Indonesia and Thailand. In Latin America, sales grew by 75%, led by Brazil and Mexico. More than 100 countries recorded electric car sales growth in 2025, and in one-third of these, they represented at least 10% of new car sales. Chinese automakers supplied 60% of global electric car sales in 2025, while European and North American automakers were each responsible for about 15% of global sales.

- `Source: GEVO2025, pp. 10-11 | Global EV Outlook 2025 (2025) | Executive summary · Expected growth in electric car sales is led by China and Europe, alongside a surge in emerging economies`

> Electric car sales in 2025 are expected to exceed 20 million worldwide to represent more than one-quarter of cars sold worldwide. Sales were up 35% year-on-year in the first three months of 2025, with record first-quarter sales in all major markets. In China, the continuation of incentives for replacing older vehicles and falling electric car prices mean electric cars are projected to reach around 60% of total car sales in the country in 2025. Emissions standards in the European Union and the United Kingdom will require higher shares of zero-emission car sales in 2025. Building on more than 20% year-on-year sales growth observed in the first quarter, these policy pushes are expected to drive up electric car sales in Europe in 2025 to reach a sales share of 25%, despite flexibility given to automakers for meeting the 2025 EU emissions reduction target. While the 2025 outlook for electric car sales in the United States is uncertain based on today’s policy direction, sales are currently expected to maintain the 10% growth observed in the first quarter; as consumers take advantage of existing tax credits in view of their potential repeal, electric car sales are projected to reach 11% of total car sales over the full year. In emerging economies other than China, sales are expected to continue growing strongly, increasing by 50% to reach 1 million in 2025.

- `Source: GEVO2026, p. 41 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Europe saw electric car sales increase 30% in the first quarter, while sales in other major EV markets declined`

> Electric car sales in the first quarter (Q1) of 2026 reached approximately 3.9 million globally, 8% lower than the same period last year, marking the first year since 2020 in which Q1 sales were down year-on-year. The decline in sales was driven primarily by lower sales in China, as well as the United States; meanwhile sales grew year-on-year in Europe and the rest of the world. In March 2026, global electric car sales rebounded close to March 2025 levels.

- `Source: GEVO2026, p. 43 | Global EV Outlook 2026 (2026) | Chapter 1. Trends in electric car markets · Europe saw electric car sales increase 30% in the first quarter, while sales in other major EV markets declined`

> In the United States, Q1 2026 electric car sales were a third lower than sales in Q1 2025, reflecting the ending of federal tax credits after Q3 2025. March 2026 sales reached the highest level since the tax credits ended, at around 95 000, though still around 30% lower than sales recorded in March 2025. From the end of Q2 2025 through April 2026, electric cars have represented 6-7% of total car sales in the United States. Across the rest of the world, Q1 2026 sales reached more than 650 000, up almost 70% compared to the same period of 2025. Most of these sales took place in EMDEs other than China.

</details>
