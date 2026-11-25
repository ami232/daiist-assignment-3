# Answers to grade

For each: `correct` 1/0 (matches the reference, or a proper refusal for unanswerable) and `supported` 1/0 (every claim is in the cited/retrieved passages). Write them into eval/human_labels.csv as `id,correct,supported,notes`, with a note for every 0.

## q01 (single)

**Question:** What were Goldman Sachs' total net revenues for 2025, and how much did they change versus 2024?

**Reference:** $58.28 billion in 2025, 9% higher than 2024.

**Answer:** Goldman Sachs' total net revenues were $58,283 million ($58.28 billion) for 2025, compared to $53,512 million ($53.51 billion) for 2024 [GS_10K_FY2025#mdna007]. This represented an increase of $4,771 million, or 9% higher than 2024 [GS_10K_FY2025#mdna007, GS_10K_FY2025#mdna008].

Searches: ['Goldman Sachs total net revenues 2025 2024']

```
[GS_10K_FY2025#mdna008] Goldman Sachs 10-K 2025 · MD&A · Net Revenues · lines 74-79 of item_7_mdna.txt
If uncertainty and concerns about geopolitical tensions and the economic outlook remain elevated or increase, including those about inflation, central bank policies and changes in international trade policies, it may lead to a decline in asset prices, a decline in market-making activity levels, or a decline in investment banking activity levels, and net revenues and provision for credit losses would likely be negatively impacted. See "Segment Assets and Operating Results — Segment Operating Results" for information about the operating environment and material trends and uncertainties that may impact our results of operations.
2025 versus 2024. Net revenues in the consolidated statements of earnings were $58.28 billion for 2025, 9% higher than 2024, reflecting significantly higher net interest income and investment banking revenues, and higher investment management revenues, partially offset by significantly lower other principal transactions revenues.
Non-Interest Revenues. Investment banking revenues in the consolidated statements of earnings were $9.35 billion for 2025, 21% higher than 2024, due to significantly higher revenues in advisory, reflecting a significant increase in completed mergers and acquisitions volumes, and higher revenues in both debt underwriting and equity underwriting.
Investment management revenues in the consolidated statements of earnings were $11.75 billion for 2025, 11% higher than 2024, primarily due to higher management and other fees, primarily reflecting the impact of higher average assets under supervision.
Commissions and fees in the consolidated statements of earnings were $4.04 billion for 2025, essentially unchanged compared with 2024, primarily reflecting a reduction in revenues related to contract termination obligations in connection with the agreement to transition the Apple Card program to another issuer, offset by higher commissions and fees in Equities, reflecting generally higher market volumes and increased transaction fees.
Market making revenues in the consolidated statements of earnings were $17.99 billion for 2025, 2% lower than 2024, reflecting lower net revenues from intermediation activities, partially offset by slightly higher net revenues from financing activities. The decrease from intermediation activities primarily reflected significantly lower revenues in mortgages and currencies, partially offset
```

```
[GS_10K_FY2025#mdna007] Goldman Sachs 10-K 2025 · MD&A · Net Revenues · lines 52-73 of item_7_mdna.txt
Net Revenues
The table below presents our net revenues by line item.
Year Ended December
$ in millions | 2025 | 2024 | 2023
Investment banking | $9,348 | $7,738 | $6,218
Investment management | 11,749 | 10,596 | 9,532
Commissions and fees | 4,042 | 4,086 | 3,789
Market making | 17,993 | 18,390 | 18,238
Other principal transactions | 1,592 | 4,646 | 2,126
Total non-interest revenues | 44,724 | 45,456 | 39,903
Interest income | 80,373 | 81,397 | 68,515
Interest expense | 66,814 | 73,341 | 62,164
Net interest income | 13,559 | 8,056 | 6,351
Total net revenues | $58,283 | $53,512 | $46,254
In the table above:
•Investment banking consists of revenues (excluding net interest) from financial advisory and underwriting assignments. These activities are included in Global Banking & Markets.
•Investment management consists of revenues (excluding net interest) from providing asset management and wealth advisory services. These activities are included in Asset & Wealth Management.
•Commissions and fees consists of revenues from executing and clearing client transactions on major stock, options and futures exchanges worldwide, as well as over-the-counter (OTC) transactions. Substantially all of these activities are included in Global Banking & Markets.
•Market making consists of revenues (excluding net interest) from client execution activities related to making markets in interest rate products, credit products, mortgages, currencies, commodities and equity products. These activities are included in Global Banking & Markets.
•Other principal transactions consists of revenues (excluding net interest) from our investing activities (primarily included in Asset & Wealth Management) and lending activities (primarily included in Global Banking & Markets).
•See Note 25 to the consolidated financial statements for further information about total non-interest revenues and net interest income.
Operating Environment. During 2025, the operating environment was generally characterized by ongoing geopolitical tensions and continued broad macroeconomic concerns and uncertainties, including those about inflation, central bank policies and changes in international trade policies (including tariffs). Industry-wide investment banking volumes in completed mergers and acquisitions, equity underwriting and debt underwriting each increased compared with 2024. In market making, activity leve
```

## q02 (single)

**Question:** What were the pre-tax earnings of Goldman Sachs' Asset & Wealth Management segment in 2025, and were they up or down on 2024?

**Reference:** $4,127 million in 2025, down from $4,865 million in 2024.

**Answer:** Goldman Sachs' Asset & Wealth Management segment reported pre-tax earnings of $4,127 million in 2025, compared with $4,865 million in 2024, making them down year-on-year [GS_10K_FY2025#mdna034].

Searches: ['Goldman Sachs Asset and Wealth Management pre-tax earnings 2025 2024']

```
[GS_10K_FY2025#mdna034] Goldman Sachs 10-K 2025 · MD&A · Asset & Wealth Management · lines 356-380 of item_7_mdna.txt
The table below presents our average Asset & Wealth Management gross loans.
Year Ended December
$ in millions | 2025 | 2024
Loans | $49,593 | $44,948
The table below presents our Asset & Wealth Management operating results.
Year Ended December
$ in millions | 2025 | 2024 | 2023
Management and other fees | $11,538 | $10,415 | $9,477
Incentive fees | 489 | 393 | 161
Private banking and lending | 3,347 | 2,881 | 2,576
Investments | 1,305 | 2,627 | 1,988
Total net revenues | 16,679 | 16,316 | 14,202
Provision for credit losses | (111) | (280) | (539)
Compensation and benefits expenses | 7,432 | 6,564 | 6,116
Other operating expenses | 5,231 | 5,167 | 6,862
Total operating expenses | 12,663 | 11,731 | 12,978
Pre-tax earnings | 4,127 | 4,865 | 1,763
Provision for taxes | 883 | 1,090 | 365
Net earnings | 3,244 | 3,775 | 1,398
Preferred stock dividends | 151 | 135 | 121
Net earnings to common | $3,093 | $3,640 | $1,277
Average common equity | $24,666 | $24,983 | $28,635
Return on average common equity | 12.5% | 14.6% | 4.5%
In the table above, Management and other fees included fees from alternatives of $2.37 billion for 2025, $2.19 billion for 2024 and $2.14 billion for 2023. In 2026, we announced a target to achieve an annual double-digit percentage growth rate for Management and other fees from alternatives.
In 2026, we announced targets to achieve ROE in the high-teens (approximately 17% to 19%) and pre-tax margin of approximately 30% within the medium term (three-to five-year time horizon from year-end 2025) for Asset & Wealth Management. The ROE for Asset & Wealth Management was 12.5% and the pre-tax margin was 25% for 2025. The net impact of historical principal investments and the related attributed equity and the FDIC special assessment fee reduced the ROE for Asset & Wealth Management by approximately 2.3 percentage points.
```

## q03 (single)

**Question:** What was Goldman Sachs' efficiency ratio in 2025 compared with 2024?

**Reference:** 64.4% in 2025 vs 63.1% in 2024 (operating expenses $37.54 billion, up 11%).

**Answer:** Goldman Sachs' efficiency ratio (defined as total operating expenses divided by total net revenues) was 64.4% for 2025, compared with 63.1% for 2024 [GS_10K_FY2025#mdna003].

Searches: ['Goldman Sachs efficiency ratio 2025 2024']

```
[GS_10K_FY2025#mdna003] Goldman Sachs 10-K 2025 · MD&A · Executive Overview · lines 8-13 of item_7_mdna.txt
Executive Overview
We generated net earnings of $17.18 billion for 2025, compared with $14.28 billion for 2024. Diluted earnings per common share (EPS) was $51.32 for 2025, compared with $40.54 for 2024. ROE was 15.0% for 2025, compared with 12.7% for 2024. Book value per common share was $357.60 as of December 2025, 6.2% higher compared with December 2024.
Net revenues were $58.28 billion for 2025, 9% higher than 2024, reflecting higher net revenues in Global Banking & Markets, partially offset by significantly lower net revenues in Platform Solutions. The increase in net revenues in Global Banking & Markets primarily reflected significantly higher net revenues in Equities, significantly higher Investment banking fees and higher net revenues in Fixed Income, Currency and Commodities (FICC). The decrease in net revenues in Platform Solutions reflected a reduction in net revenues of $2.26 billion from markdowns on the outstanding credit card portfolio related to the transfer of the Apple Card loan portfolio to held for sale and contract termination obligations in connection with the agreement to transition the program to another issuer, which was more than offset by a related reserve reduction in provision for credit losses. Net revenues in Asset & Wealth Management were slightly higher, reflecting higher Management and other fees, higher net revenues in Private banking and lending and, to a lesser extent, higher Incentive fees, largely offset by significantly lower net revenues in Investments.
Provision for credit losses was a net benefit of $1.11 billion for 2025, compared with net provisions of $1.35 billion for 2024. The net benefit for 2025 reflected a net release related to the Apple Card loan portfolio (including a reserve reduction of $2.48 billion related to the transfer of the Apple Card loans to held for sale, partially offset by net charge-offs during the year). Provisions for 2024 reflected net provisions related to the credit card portfolio (primarily driven by net charge-offs).
Operating expenses were $37.54 billion for 2025, 11% higher than 2024, primarily reflecting higher compensation and benefits expenses (reflecting improved operating performance) and higher transaction based expenses. Our efficiency ratio (total operating expenses divided by total net revenues) was 64.4% for 2025, compared with 63.1% for 2024.
During 2025, we retu
```

## q04 (single)

**Question:** Why did Goldman Sachs' Platform Solutions net revenues fall so sharply in 2025?

**Reference:** Net revenues fell to $151 million from $2.13 billion, mainly due to $2.26 billion of markdowns on the credit card portfolio tied to moving the Apple Card loans to held for sale and contract termination obligations for transitioning the program to another issuer.

**Answer:** Platform Solutions net revenues fell from $2.13 billion in 2024 to $151 million in 2025 [GS_10K_FY2025#mdna054]. This $2.26 billion decrease was driven by markdowns on the outstanding credit card portfolio resulting from the transfer of the Apple Card loan portfolio to held for sale, as well as contract termination obligations tied to the agreement to transition the Apple Card program to another issuer [GS_10K_FY2025#mdna054].

Searches: ['Goldman Sachs Platform Solutions net revenues 2025 MD&A']

```
[GS_10K_FY2025#mdna054] Goldman Sachs 10-K 2025 · MD&A · Platform Solutions · lines 649-656 of item_7_mdna.txt
(columns: $ in millions | 2025 | 2024 | 2023)
Preferred stock dividends | 29 | 25 | 23
Net earnings/(loss) to common | $90 | $(799) | $(1,628)
Average common equity | $4,312 | $4,585 | $4,128
Return on average common equity | 2.1% | (17.4)% | (39.4)%
Operating Environment. The operating environment for Platform Solutions is mainly impacted by the economic environment in the U.S., which, during 2025, was generally characterized by concerns about inflation and uncertainty related to changes in international trade policies (including tariffs), a continued low rate of unemployment and a decline in the pace of growth in consumer spending compared with 2024.
In the future, if economic conditions deteriorate, it may lead to a decrease in consumer spending or a deterioration in consumer credit, and net revenues in Platform Solutions would likely be negatively impacted.
2025 versus 2024. Net revenues in Platform Solutions were $151 million for 2025, compared with $2.13 billion in 2024, with the decrease reflecting a reduction in net revenues of $2.26 billion from markdowns on the outstanding credit card portfolio related to the transfer of the Apple Card loan portfolio to held for sale and contract termination obligations in connection with the agreement to transition the program to another issuer, which was more than offset by a related reserve reduction in provision for credit losses.
Provision for credit losses was a net benefit of $1.38 billion for 2025, compared with net provisions of $1.54 billion for 2024. The net benefit for 2025 reflected a reserve reduction of $2.48 billion related to the transfer of the Apple Card loan portfolio to held for sale, partially offset by net charge-offs during the year. Provisions for 2024 reflected net charge-offs related to the credit card portfolio.
```

## q05 (single)

**Question:** What average effective management fee did Goldman Sachs earn on alternative investments AUS in 2025?

**Reference:** 58 basis points in 2025, down from 60 bps in 2024.

**Answer:** Goldman Sachs earned an average effective management fee of 58 basis points on alternative investments AUS in the year ended December 2025 [GS_10K_FY2025#mdna042]. By alternative asset categories within total alternative AUS (which averaged 58 bps overall), the 2025 effective fees were 72 bps for corporate equity, 55 bps for credit, 46 bps for real estate, and 48 bps for hedge funds and other [GS_10K_FY2025#mdna044].

Searches: ['Goldman Sachs alternative investments AUS fee 2025']

```
[GS_10K_FY2025#mdna042] Goldman Sachs 10-K 2025 · MD&A · Asset Class · lines 478-497 of item_7_mdna.txt
(columns: $ in billions | 2025 | 2024 | 2023)
Asset Class
Alternative investments | $376 | $328 | $283
Equity | 853 | 731 | 610
Fixed income | 1,246 | 1,150 | 1,036
Total long-term AUS | 2,475 | 2,209 | 1,929
Liquidity products | 853 | 751 | 749
Total AUS | $3,328 | $2,960 | $2,678
We earn management fees on client assets that we manage and also receive incentive fees based on a percentage of a fund's or a separately managed account's return, or when the return exceeds a specified benchmark or other performance targets. These incentive fees are recognized when it is probable that a significant reversal of such fees will not occur. Our estimated unrecognized incentive fees were $5.24 billion as of December 2025, $4.12 billion as of December 2024 and $3.77 billion as of December 2023. Such amounts are based on the completion of the funds' financial statements, which is generally one quarter in arrears. These fees will be recognized, assuming no decline in fair value, if and when it is probable that a significant reversal of such fees will not occur, which is generally when such fees are no longer subject to fluctuations in the market value of the assets.
The table below presents our average effective management fee (which excludes non-asset-based fees) earned on our AUS by asset class.
Year Ended December
Effective fees (bps) | 2025 | 2024 | 2023
Alternative investments | 58 | 60 | 62
Equity | 54 | 55 | 57
Fixed income | 17 | 17 | 17
Liquidity products | 14 | 15 | 15
Total average effective fee | 31 | 31 | 31
The table below presents details about our monthly average AUS for alternative assets and the average effective management fee we earned on such assets.
Funds & discretionary accounts | Advisory | Total
$ in billions | Direct strategies | Fund of funds | Total | & OCIO accounts | alternative AUS
Year Ended December 2025
```

```
[GS_10K_FY2025#mdna044] Goldman Sachs 10-K 2025 · MD&A · Effective Fees (bps) · lines 504-510 of item_7_mdna.txt
(columns: Year Ended December 2025)
Effective Fees (bps)
Corporate equity | 123 | 64 | 87 | 21 | 72
Credit | 72 | 42 | 72 | 11 | 55
Real estate | 64 | 67 | 65 | 11 | 46
Hedge funds and other | 67 | 72 | 68 | 19 | 48
Total | 82 | 65 | 77 | 17 | 58
Year Ended December 2024
```

## q06 (single)

**Question:** How many employees did Goldman Sachs have at the end of 2025?

**Reference:** 47,400 at period-end 2025, up 2% from 46,500 at end-2024.

**Answer:** Goldman Sachs had 47,400 employees (headcount at period-end) as of December 2025 [GS_10K_FY2025#mdna012].

Searches: ['Goldman Sachs employees headcount end of 2025']

```
[GS_10K_FY2025#mdna012] Goldman Sachs 10-K 2025 · MD&A · Operating Expenses · lines 97-113 of item_7_mdna.txt
Operating Expenses
Our operating expenses are primarily influenced by compensation, headcount and levels of business activity. Compensation and benefits includes salaries, year-end discretionary compensation, amortization of equity awards and other items, such as benefits. Discretionary compensation is significantly impacted by, among other factors, the level of net revenues, net of provision for credit losses, overall financial performance, prevailing labor markets, business mix, the structure of our share-based awards and the external environment.
The table below presents our operating expenses by line item and headcount.
Year Ended December
$ in millions | 2025 | 2024 | 2023
Compensation and benefits | $18,906 | $16,706 | $15,499
Transaction based | 7,997 | 6,724 | 5,698
Market development | 710 | 646 | 629
Communications and technology | 2,170 | 1,991 | 1,919
Depreciation and amortization | 2,182 | 2,392 | 4,856
Occupancy | 958 | 973 | 1,053
Professional fees | 1,770 | 1,652 | 1,623
Other expenses | 2,851 | 2,683 | 3,210
Total operating expenses | $37,544 | $33,767 | $34,487
Headcount at period-end | 47,400 | 46,500 | 45,300
2025 versus 2024. Operating expenses in the consolidated statements of earnings were $37.54 billion for 2025, 11% higher than 2024. Our efficiency ratio was 64.4% for 2025, compared with 63.1% for 2024.
The increase in operating expenses, compared with 2024, primarily reflected higher compensation and benefits expenses (reflecting improved operating performance) and higher transaction based expenses. Net provisions for litigation and regulatory proceedings were $215 million for 2025, compared with $166 million for 2024. In 2025, based on additional information received from the FDIC about the updated estimated cost to the Deposit Insurance Fund resulting from the closures in 2023 of Silicon Valley Bank and Signature Bank, we recognized a reduction of $75 million related to the updated estimated cost of the FDIC special assessment fee, compared with $71 million of expense recognized in 2024.
```

## q07 (single)

**Question:** What were Morgan Stanley Wealth Management's net revenues and pre-tax margin in 2025?

**Reference:** Net revenues of $31.8 billion ($31,754 million, up 12%) with a pre-tax margin of 29.3%.

**Answer:** In 2025, Morgan Stanley Wealth Management's net revenues were $31,754 million [MS_10K_FY2025#mdna042] (or $31.8 billion) [MS_10K_FY2025#mdna002], and its pre-tax margin was 29% (reported as 29.3% in the executive summary) [MS_10K_FY2025#mdna010, MS_10K_FY2025#mdna002].

Searches: ['Morgan Stanley Wealth Management net revenues pre-tax margin 2025']

```
[MS_10K_FY2025#mdna010] Morgan Stanley 10-K 2025 · MD&A · Pre-tax margin by segment 4 · lines 61-77 of item_7_mdna.txt
(columns: $ in millions, except per share data | 2025 | 2024 | 2023)
Pre-tax margin by segment 4
Institutional Securities | 34% | 31% | 19%
Wealth Management | 29% | 27% | 25%
Investment Management | 23% | 19% | 16%
$ in millions, except per share data, worldwide employees and client assets | At December 31, 2025 | At December 31, 2024
Average liquidity resources for three months ended 5 | $385,884 | $345,440
Loans 6 | $289,038 | $246,814
Total assets | $1,420,270 | $1,215,071
Deposits | $415,523 | $376,007
Borrowings | $348,935 | $288,819
Common equity | $101,882 | $94,761
Tangible common equity 3 | $79,147 | $71,604
Common shares outstanding | 1,583 | 1,607
Book value per common share 7 | $64.37 | $58.98
Tangible book value per common share 3,7 | $50.00 | $44.57
Worldwide employees (in thousands) | 83 | 80
Client assets 8 (in billions) | $9,276 | $7,860
```

```
[MS_10K_FY2025#mdna042] Morgan Stanley 10-K 2025 · MD&A · Wealth Management · lines 293-311 of item_7_mdna.txt
Wealth Management
Income Statement Information
% Change
$ in millions | 2025 | 2024 | 2023 | 2025 | 2024
Revenues
Asset management | $18,627 | $16,501 | $14,019 | 13% | 18%
Transactional 1 | 4,588 | 3,864 | 3,556 | 19% | 9%
Net interest | 7,911 | 7,313 | 8,118 | 8% | (10)%
Other 2 | 628 | 742 | 575 | (15)% | 29%
Net revenues | 31,754 | 28,420 | 26,268 | 12% | 8%
Provision for credit losses | 47 | 62 | 131 | (24)% | (53)%
Compensation and benefits | 16,950 | 15,207 | 13,972 | 11% | 9%
Non-compensation expenses | 5,464 | 5,411 | 5,635 | 1% | (4)%
Total non-interest expenses | 22,414 | 20,618 | 19,607 | 9% | 5%
Income before provision for income taxes | 9,293 | 7,740 | 6,530 | 20% | 19%
Provision for income taxes | 2,163 | 1,852 | 1,508 | 17% | 23%
Net income applicable to Morgan Stanley | $7,130 | $5,888 | $5,022 | 21% | 17%
1.Transactional includes Investment banking, Trading, and Commissions and fees revenues.
2.Other includes Investments and Other revenues.
```

```
[MS_10K_FY2025#mdna002] Morgan Stanley 10-K 2025 · MD&A · Executive Summary · lines 9-18 of item_7_mdna.txt
Executive Summary
Overview of Financial Results
Consolidated Results—Full Year Ended December 31, 2025
•The Firm reported net revenues of $70.6 billion and net income applicable to Morgan Stanley of $16.9 billion reflecting strong results across our business segments and demonstrating the strength of our Integrated Firm.
•The Firm delivered ROE of 16.6% and ROTCE of 21.6% (see "Selected Non-GAAP Financial Information" herein).
•The Firm expense efficiency ratio was 68% compared to 71% in the prior year, demonstrating operating leverage while continuing to invest in our businesses.
•At December 31, 2025, the Firm's Standardized Common Equity Tier 1 capital ratio was 15.0%, and its Supplementary Leverage Ratio was 5.4%.
•Institutional Securities net revenues of $33.1 billion, primarily reflecting strong performance in Equity on higher client activity and higher underwriting and Advisory revenues within Investment Banking.
•Wealth Management delivered net revenues of $31.8 billion, primarily reflecting higher Asset management revenues on higher market levels and the cumulative impact of strong fee-based flows. The pre-tax margin was 29.3%. Fee-based asset flows were $160 billion and the business added net new assets of $356 billion.
•Investment Management reported net revenues of $6.5 billion, primarily reflecting higher asset management fees driven by higher average AUM on higher market levels.
```

## q08 (single)

**Question:** How much net new assets did Morgan Stanley Wealth Management bring in during 2025?

**Reference:** $356.3 billion in 2025, up from $251.7 billion in 2024.

**Answer:** Morgan Stanley Wealth Management brought in $356.3 billion of net new assets in 2025 [MS_10K_FY2025#mdna044].

Searches: ['Morgan Stanley Wealth Management net new assets 2025']

```
[MS_10K_FY2025#mdna044] Morgan Stanley 10-K 2025 · MD&A · Annualized weighted average cost of deposits 4 · lines 318-326 of item_7_mdna.txt
(columns: $ in billions | At December 31, 2025 | At December 31, 2024)
Annualized weighted average cost of deposits 4
Period end | 2.51% | 2.73%
Period average | 2.76% | 3.05%
2025 | 2024 | 2023
Net new assets | $356.3 | $251.7 | $282.3
1.Client assets represent those for which Wealth Management is providing services including financial advisor-led brokerage, investment advisory, custody, cash management, and administrative services; self-directed brokerage and investment advisory services; financial and wealth planning services; workplace services, including stock plan administration, and retirement plan services. As part of the Integrated Firm, Wealth Management may provide these services to clients who also use the services of one or more other business segments. See "Advisor-Led Channel" and "Self-Directed Channel" herein for additional information.
2.Margin and other lending represents margin lending arrangements, which allow customers to borrow against the value of qualifying securities and other lending which includes non‐purpose securities-based lending on non‐bank entities.
3.Deposits reflect liabilities sourced from Wealth Management clients and other sources of funding on our U.S. Bank Subsidiaries. Deposits include sweep deposit programs, savings and other deposits, and time deposits.
4.Annualized weighted average represents the total annualized weighted average cost of the various deposit products. Amounts include the effect of related hedging derivatives. The period end cost of deposits is based upon balances and rates as of December 31, 2025 and December 31, 2024. The period average is based on daily balances and rates for the period.
```

## q09 (single)

**Question:** What average fee rate did Morgan Stanley Investment Management earn on equity AUM in 2025?

**Reference:** 69 basis points in 2025 (71 bps in 2024).

**Answer:** Morgan Stanley Investment Management earned an average fee rate of 69 basis points on equity AUM in 2025 [MS_10K_FY2025#mdna061].

Searches: ['Morgan Stanley Investment Management average fee rate equity AUM 2025']

```
[MS_10K_FY2025#mdna061] Morgan Stanley 10-K 2025 · MD&A · Average Fee Rates1 · lines 482-493 of item_7_mdna.txt
Average Fee Rates1
Fee rate in bps | 2025 | 2024 | 2023
Equity | 69 | 71 | 71
Fixed income | 36 | 36 | 35
Alternatives and Solutions | 27 | 28 | 32
Long-term AUM | 40 | 42 | 44
Liquidity and Overlay Services | 12 | 12 | 13
Total | 31 | 32 | 34
1.Based on Asset management revenues, net of waivers, excluding performance-based fees and other non-management fees. For certain non-U.S. funds, it includes the portion of advisory fees that the advisor collects on behalf of third-party distributors. The payment of those fees to the distributor is included in Non-compensation expenses in the income statement.
Asset management and other related fees within the Investment Management segment are primarily generated from Equity, Fixed Income and the following products:
Alternatives and Solutions. Includes products in fund of funds, real estate, infrastructure, private equity and credit strategies and multi-asset portfolios, as well as systematic strategies that create custom investment solutions, including those offered by Parametric.
Liquidity and Overlay Services. Includes liquidity products, as well as overlay services, which represent investment strategies that use passive exposure instruments to obtain, offset or substitute specific portfolio exposures, beyond those provided by the underlying holdings of the fund.
```

## q10 (single)

**Question:** What return on tangible common equity did Morgan Stanley report for 2025?

**Reference:** 21.6% in 2025, up from 18.8% in 2024 (a non-GAAP measure).

**Answer:** Morgan Stanley reported a consolidated Return on Tangible Common Equity (ROTCE) of 21.6% for 2025 [MS_10K_FY2025#mdna009, MS_10K_FY2025#mdna002]. ROTCE is a non-GAAP financial measure [MS_10K_FY2025#mdna019].

Searches: ['Morgan Stanley return on tangible common equity 2025']

```
[MS_10K_FY2025#mdna019] Morgan Stanley 10-K 2025 · MD&A · Return on Tangible Common Equity Goal · lines 150-153 of item_7_mdna.txt
Return on Tangible Common Equity Goal
We have an ROTCE goal of 20%. Our ROTCE goal is a forward-looking statement that is based on a normal market environment and may be materially affected by many factors.
See "Risk Factors" and "Forward-Looking Statements" herein for further information on market and economic conditions and their potential effects on our future operating results.
ROTCE represents a non-GAAP financial measure. For further information on non-GAAP measures, see "Selected Non-GAAP Financial Information" herein.
```

```
[MS_10K_FY2025#mdna009] Morgan Stanley 10-K 2025 · MD&A · Consolidated financial measures · lines 55-60 of item_7_mdna.txt
(columns: $ in millions, except per share data | 2025 | 2024 | 2023)
Consolidated financial measures
Expense efficiency ratio 1 | 68% | 71% | 77%
ROE 2 | 16.6% | 14.0% | 9.4%
ROTCE 2,3 | 21.6% | 18.8% | 12.8%
Pre-tax margin 4 | 31% | 28% | 22%
Effective tax rate | 22.5% | 23.1% | 21.9%
```

```
[MS_10K_FY2025#mdna002] Morgan Stanley 10-K 2025 · MD&A · Executive Summary · lines 9-18 of item_7_mdna.txt
Executive Summary
Overview of Financial Results
Consolidated Results—Full Year Ended December 31, 2025
•The Firm reported net revenues of $70.6 billion and net income applicable to Morgan Stanley of $16.9 billion reflecting strong results across our business segments and demonstrating the strength of our Integrated Firm.
•The Firm delivered ROE of 16.6% and ROTCE of 21.6% (see "Selected Non-GAAP Financial Information" herein).
•The Firm expense efficiency ratio was 68% compared to 71% in the prior year, demonstrating operating leverage while continuing to invest in our businesses.
•At December 31, 2025, the Firm's Standardized Common Equity Tier 1 capital ratio was 15.0%, and its Supplementary Leverage Ratio was 5.4%.
•Institutional Securities net revenues of $33.1 billion, primarily reflecting strong performance in Equity on higher client activity and higher underwriting and Advisory revenues within Investment Banking.
•Wealth Management delivered net revenues of $31.8 billion, primarily reflecting higher Asset management revenues on higher market levels and the cumulative impact of strong fee-based flows. The pre-tax margin was 29.3%. Fee-based asset flows were $160 billion and the business added net new assets of $356 billion.
•Investment Management reported net revenues of $6.5 billion, primarily reflecting higher asset management fees driven by higher average AUM on higher market levels.
```

## q11 (single)

**Question:** What was BlackRock's total AUM at the end of 2025, and how much were total net inflows for the year?

**Reference:** About $14.04 trillion ($14,041,518 million) at December 31, 2025, with total net inflows of $698.3 billion.

**Answer:** At the end of 2025, BlackRock's total assets under management (AUM) were $14,041,518 million ($14.04 trillion) [BLK_10K_FY2025#mdna023]. Total net inflows for the year were $698,261 million ($698.26 billion), which included $567,487 million in long-term net inflows and $130,774 million in cash management net inflows [BLK_10K_FY2025#mdna023].

Searches: ['BlackRock total AUM 2025 net inflows']

```
[BLK_10K_FY2025#mdna023] BlackRock 10-K 2025 · MD&A · Assets Under Management · lines 174-197 of item_7_mdna.txt
(columns: (in millions) | 2025 | 2024 | 2025 | 2024)
ETFs | 5,467,710 | 4,230,375 | 526,711 | 390,433
Non-ETF index | 4,060,333 | 3,531,811 | (95,316) | 35,936
Long-term | 12,960,786 | 10,630,588 | 567,487 | 488,621
Cash management | 1,080,732 | 920,663 | 130,774 | 152,730
Total | $14,041,518 | $11,551,251 | $698,261 | $641,351
(1)Beginning in the first quarter of 2025, BlackRock updated the presentation of the Company's AUM line items. Such line items have been reclassified for 2024 to conform to this new presentation.
(2)Amounts include commodity ETFs and ETPs.
The following table presents the component changes in BlackRock's AUM for 2025 and 2024.
(in millions) | 2025 | 2024
Beginning AUM | $11,551,251 | $10,008,995
Net inflows (outflows):
Long-term | 567,487 | 488,621
Cash management | 130,774 | 152,730
Total net inflows (outflows) | 698,261 | 641,351
Realizations (1) | (33,125) | —
Acquisitions (2) | 120,961 | 73,949
Market change | 1,483,629 | 992,964
FX impact (3) | 220,541 | (166,008)
Total change | 2,490,267 | 1,542,256
Ending AUM | $14,041,518 | $11,551,251
(1)Beginning in the first quarter of 2025, BlackRock updated the presentation of net flows to separately disclose realizations, which represent return of capital/return on investments. Realizations in 2024 have not been recast.
(2)Amount for 2025 included AUM attributable to the HPS and ElmTree Transactions. Amount for 2024 includes AUM attributable to the GIP Transaction and the SpiderRock Advisors transaction in May 2024 (the "SpiderRock Transaction").
(3)Foreign exchange reflects the impact of translating non-US dollar denominated AUM into US dollars for reporting purposes.
BlackRock has historically grown AUM through organic growth and acquisitions. Management believes that the Company will be able to continue to grow AUM organically by focusing on strong investment performance, efficient delivery of beta for index products, client service, developing new products and optimizing distribution capabilities.
```

## q12 (single)

**Question:** What was BlackRock's operating margin in 2025 on a GAAP basis and on an as adjusted basis?

**Reference:** GAAP operating margin 29.1% (down from 37.1%); as adjusted 44.1% (down from 44.5%).

**Answer:** BlackRock's operating margin in 2025 was 29.1% on a GAAP basis and 44.1% on an as adjusted basis [BLK_10K_FY2025#mdna017].

Searches: ['BlackRock operating margin 2025 GAAP as adjusted']

```
[BLK_10K_FY2025#mdna017] BlackRock 10-K 2025 · MD&A · Non-GAAP Financial Measures · lines 92-123 of item_7_mdna.txt
(columns: (in millions) | 2025 | 2024)
Operating income, as adjusted | $9,600 | $8,110
Revenue, GAAP basis | $24,216 | $20,407
Non-GAAP adjustments:
Distribution fees | (1,355) | (1,273)
Investment advisory fees | (1,105) | (898)
Revenue used for operating margin measurement | $21,756 | $18,236
Operating margin, GAAP basis | 29.1% | 37.1%
Operating margin, as adjusted | 44.1% | 44.5%
(1)Amounts included within general and administration expense.
(2) Nonoperating income (expense), less net income (loss) attributable to NCI - CIPs, as adjusted:
(in millions) | 2025 | 2024
Nonoperating income (expense), GAAP basis | $574 | $721
Less: Net income (loss) attributable to NCI - CIPs | 262 | 143
Nonoperating income (expense), net of NCI - CIPs | 312 | 578
Less: Hedge gain (loss) on deferred cash compensation plans (a) | 61 | 45
Nonoperating income (expense), less net income (loss) attributable to NCI - CIPs, as adjusted | $251 | $533
(3) Net income attributable to BlackRock, Inc., as adjusted:
(in millions, except per share data) | 2025 | 2024
Net income attributable to BlackRock, Inc., GAAP basis | $5,553 | $6,369
Noncontrolling interest - Subco | 127 | —
Net income attributable to BlackRock, Inc., (for diluted EPS) | 5,680 | 6,369
Non-GAAP adjustments (1) :
Net impact of hedged deferred cash compensation plans (a) | (6) | (1)
Amortization and impairment of intangible assets (b) | 578 | 218
Acquisition-related compensation costs (b) | 549 | 110
Acquisition-related transaction costs (b) | 91 | 66
Change in fair value of contingent consideration (b) | 717 | (27)
Charitable Contribution (c) | 80 | —
Restructuring charge (d) | 29 | —
Income tax matters | 18 | (123)
Net income attributable to BlackRock, Inc., as adjusted | $7,736 | $6,612
Diluted weighted-average common shares outstanding, including Subco Units | 160.9 | 151.6
```

## q13 (single)

**Question:** When did BlackRock complete the Preqin acquisition and what did it pay?

**Reference:** Completed March 3, 2025, for £2.5 billion (about $3.2 billion) in cash.

**Answer:** BlackRock completed the acquisition of 100% of the shares of Preqin on March 3, 2025, for £2.5 billion (or approximately $3.2 billion) in cash [BLK_10K_FY2025#mdna003].

Searches: ['BlackRock Preqin acquisition completion date purchase price']

```
[BLK_10K_FY2025#mdna003] BlackRock 10-K 2025 · MD&A · Acquisitions · lines 9-11 of item_7_mdna.txt
Acquisitions
On March 3, 2025, BlackRock completed the acquisition of 100% of the shares of Preqin, a leading provider of private markets data, for £2.5 billion (or approximately $3.2 billion) in cash. The Company believes bringing together Preqin's data and research tools with the complementary workflows of Aladdin and eFront in a unified platform will create a preeminent private markets technology and data provider.
On July 1, 2025, BlackRock completed the acquisition of 100% of the business and assets of HPS, a leading global credit investment manager, with substantially all consideration paid in Class B-2 common units ("Subco Units") of BlackRock Saturn Subco, LLC ("Subco"), a consolidated subsidiary of the Company. The HPS Transaction, which added $165 billion of client AUM and $118 billion of fee-paying AUM, positions the Company to provide an integrated private credit platform with both public and private income solutions for clients across their whole portfolios. At close, approximately 8.5 million Subco Units were delivered to former equityholders of HPS and valued at $8.5 billion, based on the price of BlackRock's common stock on June 30, 2025 of approximately $1,049 and discounted for a one-year lack of marketability before exchange rights begin. Such Subco Units are exchangeable on a one-for-one basis into BlackRock common stock (accordingly, the value of each unit delivered was based on the price of a share of BlackRock's common stock and the specific terms of the Subco Units). In addition, at the time of close, the Company granted incentive retention awards to certain employees of approximately 680,000 RSUs that vest in increasing yearly increments over five years valued at $675 million and approximately 270,000 RSUs valued at $260 million that cliff vest 100% after six months. Furthermore, deferred consideration, which is to be delivered all in Subco Units of approximately 2.8 million to 4.4 million, and initially valued at $3.4 billion at close, may be paid in approximately five years, subject to achievement of certain post-closing conditions and financial performance milestones. In general, if (i) the maximum amount of contingent consideration is achieved, (ii) all Subco Units are exchanged for shares of the Company's common stock (including those issued on the closing date), and (iii) all
```

## q14 (single)

**Question:** How much technology services and subscription revenue did BlackRock earn in 2025?

**Reference:** $1,981 million in 2025, up from $1,603 million in 2024.

**Answer:** BlackRock earned $1,981 million in technology services and subscription revenue in 2025 [BLK_10K_FY2025#mdna038].

Searches: ['BlackRock technology services and subscription revenue 2025']

```
[BLK_10K_FY2025#mdna038] BlackRock 10-K 2025 · MD&A · Revenue · lines 406-445 of item_7_mdna.txt
Revenue
The table below presents detail of revenue for 2025 and 2024 and includes the product type mix of base fees and securities lending revenue and performance fees.
(in millions) | 2025 | 2024
Revenue:
Investment advisory, administration fees and securities lending revenue (1) :
Equity:
Active | $2,167 | $2,166
ETFs | 6,043 | 5,124
Equity subtotal | 8,210 | 7,290
Fixed income:
Active | 2,018 | 1,952
ETFs | 1,532 | 1,367
Fixed income subtotal | 3,550 | 3,319
Active multi-asset | 1,332 | 1,248
Alternatives:
Private markets | 2,350 | 1,196
Liquid alternatives | 669 | 568
Alternatives subtotal | 3,019 | 1,764
Non-ETF index | 1,321 | 1,183
Digital assets, commodities and multi-asset ETFs (2) | 502 | 247
Long-term | 17,934 | 15,051
Cash management | 1,245 | 1,049
Total investment advisory, administration fees and securities lending revenue (3) | 19,179 | 16,100
Investment advisory performance fees:
Equity | 132 | 161
Fixed income | 16 | 34
Multi-asset | 23 | 24
Alternatives:
Private markets | 695 | 308
Liquid alternatives | 558 | 680
Alternatives subtotal | 1,253 | 988
Total investment advisory performance fees | 1,424 | 1,207
Technology services and subscription revenue | 1,981 | 1,603
Distribution fees | 1,355 | 1,273
Advisory and other revenue:
Advisory | 50 | 49
Other | 227 | 175
Total advisory and other revenue | 277 | 224
Total revenue | $24,216 | $20,407
(1)Beginning in the first quarter of 2025, BlackRock reclassified the presentation of the Company's investment advisory, administration fees and securities lending revenue line items to align with the updated presentation of the Company's AUM line items. Such line items have been reclassified for 2024 to conform to this new presentation. See page 11 of Exhibit 99.2 to the Current Report on Form 8-K furnished on April 11, 2025 for the reclassified presentation of the 2024 investment advisory, administration fees and securities lending revenue line items.
```

## q15 (single)

**Question:** How much did BlackRock earn in base fees and securities lending revenue from equity ETFs in 2025?

**Reference:** $6,043 million in 2025 (vs $5,124 million in 2024).

**Answer:** In 2025, BlackRock earned $6,043 million in investment advisory, administration fees and securities lending revenue from equity ETFs [BLK_10K_FY2025#mdna038].

Searches: ['BlackRock base fees securities lending revenue equity ETFs 2025']

```
[BLK_10K_FY2025#mdna038] BlackRock 10-K 2025 · MD&A · Revenue · lines 406-445 of item_7_mdna.txt
Revenue
The table below presents detail of revenue for 2025 and 2024 and includes the product type mix of base fees and securities lending revenue and performance fees.
(in millions) | 2025 | 2024
Revenue:
Investment advisory, administration fees and securities lending revenue (1) :
Equity:
Active | $2,167 | $2,166
ETFs | 6,043 | 5,124
Equity subtotal | 8,210 | 7,290
Fixed income:
Active | 2,018 | 1,952
ETFs | 1,532 | 1,367
Fixed income subtotal | 3,550 | 3,319
Active multi-asset | 1,332 | 1,248
Alternatives:
Private markets | 2,350 | 1,196
Liquid alternatives | 669 | 568
Alternatives subtotal | 3,019 | 1,764
Non-ETF index | 1,321 | 1,183
Digital assets, commodities and multi-asset ETFs (2) | 502 | 247
Long-term | 17,934 | 15,051
Cash management | 1,245 | 1,049
Total investment advisory, administration fees and securities lending revenue (3) | 19,179 | 16,100
Investment advisory performance fees:
Equity | 132 | 161
Fixed income | 16 | 34
Multi-asset | 23 | 24
Alternatives:
Private markets | 695 | 308
Liquid alternatives | 558 | 680
Alternatives subtotal | 1,253 | 988
Total investment advisory performance fees | 1,424 | 1,207
Technology services and subscription revenue | 1,981 | 1,603
Distribution fees | 1,355 | 1,273
Advisory and other revenue:
Advisory | 50 | 49
Other | 227 | 175
Total advisory and other revenue | 277 | 224
Total revenue | $24,216 | $20,407
(1)Beginning in the first quarter of 2025, BlackRock reclassified the presentation of the Company's investment advisory, administration fees and securities lending revenue line items to align with the updated presentation of the Company's AUM line items. Such line items have been reclassified for 2024 to conform to this new presentation. See page 11 of Exhibit 99.2 to the Current Report on Form 8-K furnished on April 11, 2025 for the reclassified presentation of the 2024 investment advisory, administration fees and securities lending revenue line items.
```

## q16 (single)

**Question:** According to Goldman Sachs, how could other people's use of AI hurt the firm?

**Reference:** Bad actors may use AI, including generative AI, to commit fraud, misappropriate funds and facilitate cyber attacks, which could cause losses, liquidity outflows or other harm to Goldman and its clients.

**Answer:** Competitors may be more timely or successful in developing or integrating AI technologies to increase productivity, reduce costs, provide better transaction execution, or offer improved products and services, which could affect Goldman Sachs' ability to attract or retain clients, cause market loss, result in service disruptions, and reduce revenues [GS_10K_FY2025#rf065]. 

Additionally, bad actors could use AI technologies to commit fraud, misappropriate funds, and facilitate cyber attacks, potentially resulting in losses, liquidity outflows, or other adverse effects for the firm and its clients [GS_10K_FY2025#rf034]. Goldman Sachs is also exposed to risks arising from the use of AI technologies by third-party vendors, clients, counterparties, clearinghouses, and other financial intermediaries [GS_10K_FY2025#rf034].

Searches: ['Goldman Sachs artificial intelligence risk factors competitors technology']

```
[GS_10K_FY2025#rf065] Goldman Sachs 10-K 2025 · Risk Factors · Competition > We have invested significant resources into the development of electronic trading systems and expect to continue to do so, but there is n... · lines 215-216 of item_1a_risk_factors.txt
We have invested significant resources into the development of electronic trading systems and expect to continue to do so, but there is no assurance that the revenues generated by these systems will yield an adequate return, particularly given the generally lower commissions arising from electronic trades.
In addition, the emergence, adoption and evolution of new technologies, including distributed ledgers, such as digital assets and blockchain, and AI technologies, have required us to invest resources to adapt our existing products and services, and we expect to continue to make such investments, which could be material. The adoption and evolution of such new technologies may also increase our compliance and regulatory costs. Further, new products, platforms and technologies, including stablecoins, digital assets and others based on distributed ledgers, may not require intermediation and could significantly disrupt payments processing and other financial services. Regulatory limitations on our involvement in products and platforms involving digital assets and distributed ledger technologies may not apply equally or, in some cases, at all to certain of our competitors. We may not be as timely or successful in developing or integrating, or even able to develop or integrate, new products and technologies, such as those built on distributed ledgers or AI technologies, into our existing products and services, adapting to changes in client preferences or achieving market acceptance of our products and services. For example, our competitors may be more timely or successful in developing or integrating AI technologies to increase their productivity and reduce their costs or to provide better transaction execution or improved products and services to clients. Any of the foregoing could affect our ability to attract or retain clients, cause us to lose market share or result in service disruptions and in turn reduce our revenues or otherwise adversely affect us.
```

```
[GS_10K_FY2025#rf034] Goldman Sachs 10-K 2025 · Risk Factors · Operational > The development and use of AI present risks and challenges that may adversely impact our business. · lines 129-130 of item_1a_risk_factors.txt
have taken to limit the risks associated with the output of their models, matters over which we may have limited visibility. Additionally, we are exposed to risks related to the use of AI technologies by third-party vendors, clients, counterparties, clearinghouses and other financial intermediaries. Any of these risks could expose us to liability or adverse legal or regulatory consequences and harm our reputation and the public perception of our business or the effectiveness of our security measures, and, as we expand the development and incorporation of AI technologies in our business processes, services or products, including in connection with our OneGS 3.0 initiative, these risks may be heightened.
In addition to our use of AI technologies, we are exposed to risks arising from the use of AI technologies by bad actors to commit fraud and misappropriate funds and to facilitate cyber attacks. Generative AI, if used to perpetrate fraud or launch cyber attacks, could result in losses, liquidity outflows or other adverse effects for us and our clients.
```

## q17 (single)

**Question:** Which cloud providers host BlackRock's Aladdin platform?

**Reference:** Microsoft Azure and Amazon Web Services.

**Answer:** The Aladdin infrastructure and environment for BlackRock and its external Aladdin clients are hosted on Microsoft Azure and Amazon Web Services [BLK_10K_FY2025#rf036].

Searches: ['BlackRock cloud providers Aladdin platform']

```
[BLK_10K_FY2025#rf036] BlackRock 10-K 2025 · Risk Factors · RISKS RELATED TO KEY THIRD-PARTY RELATIONSHIPS > Key technology partnerships may expose BlackRock to increased regulatory oversight, as well as migration, execution, technology and opera... · lines 116-117 of item_1a_risk_factors.txt
Key technology partnerships may expose BlackRock to increased regulatory oversight, as well as migration, execution, technology and operational risks.
BlackRock has a number of key strategic partnerships, including with Microsoft. For instance, the Aladdin infrastructure and environment for BlackRock and its external Aladdin clients are hosted on Microsoft Azure and Amazon Web Services. BlackRock has also migrated certain systems that support its corporate functions to cloud-based platforms. The benefits of cloud-based platforms are significant and BlackRock has adopted a robust risk-based approach to its migration strategies. However, these partnerships also introduce risks, including: (1) risks associated with relying on third-parties for aspects of infrastructure reliability and stability; (2) software and information security risks arising from the use of cloud technology; (3) operational and execution risks; and (4) risks related to increased regulatory oversight and new compliance obligations, which may be further exacerbated as BlackRock and the Aladdin platform continue to grow. A prolonged global failure of cloud services could also impact BlackRock's other systems. Failures by BlackRock to manage these risks, and/or risks associated with future technology partnerships, may result in escalating costs, financial loss, client dissatisfaction or attrition, regulatory fines and/or sanctions, reputational harm or legal liability, which, in turn, may cause BlackRock's AUM, revenue and earnings to decline.
```

## q18 (single)

**Question:** What example of human error does Morgan Stanley give when describing information security risks?

**Reference:** Human error has in the past led to the loss of the firm's physical data-bearing devices.

**Answer:** Morgan Stanley states that human error has led to the loss of the firm's physical data-bearing devices in the past [MS_10K_FY2025#rf015].

Searches: ['Morgan Stanley information security risks human error example']

```
[MS_10K_FY2025#rf015] Morgan Stanley 10-K 2025 · Risk Factors · Operational Risk > operations and/or increase costs. Any theft of data, technology or intellectual property may negatively impact our operations and reputat... · lines 40-43 of item_1a_risk_factors.txt
operations and/or increase costs. Any theft of data, technology or intellectual property may negatively impact our operations and reputation, including disrupting the business activities of our subsidiaries, affiliates, joint ventures or clients conducting business in those jurisdictions.
A cyberattack, information or security breach or a technology failure of ours or a third party could adversely affect our ability to conduct our business or manage our exposure to risk, or result in disclosure or misuse of personal, confidential or proprietary information and otherwise adversely impact our results of operations, liquidity and financial condition, as well as cause reputational harm.
Cybersecurity risks for financial institutions have significantly increased in recent years, in part because of the proliferation of new technologies; the use of the internet, mobile telecommunications and cloud technologies to conduct financial transactions; the use of artificial intelligence and the emergence of quantum computing; and the increased sophistication and activities of organized crime, hackers, terrorists, nation-states, state-sponsored actors and other parties. Any of these parties may also attempt to fraudulently induce employees, customers, clients, vendors or other third parties or users of our systems to disclose sensitive information in order to gain access to our networks, systems or data or those of our employees or clients, and such parties may see their effectiveness enhanced by the use of advanced systems, such as artificial intelligence. Global events and geopolitical instability have also led to increased nation-state targeting of financial institutions in the U.S. and abroad.
Information security risks may also derive from human error, fraud or malice on the part of our employees or third parties, software bugs, server malfunctions, software or hardware failure or other technological failure. For example, human error has led to the loss of the Firm's physical data-bearing devices in the past. These risks may be heightened by several factors, including remote work, reliance on new technologies (such as generative artificial intelligence) or as a result of the integration of acquisitions and
```

## q19 (single)

**Question:** Which recent acquisitions does BlackRock single out as carrying integration risk?

**Reference:** The GIP and HPS acquisitions; BlackRock may not realize their expected benefits, including synergies.

**Answer:** BlackRock explicitly singles out the GIP and HPS acquisitions as carrying integration risks related to realizing anticipated benefits, synergies, and value creation on expected timelines [BLK_10K_FY2025#rf026].

Searches: ['BlackRock acquisitions integration risk']

```
[BLK_10K_FY2025#rf026] BlackRock 10-K 2025 · Risk Factors · TECHNOLOGY AND OPERATIONAL RISKS > BlackRock is subject to risks associated with its recent acquisitions, including any failure to realize anticipated benefits of such acqu... · lines 71-72 of item_1a_risk_factors.txt
BlackRock is subject to risks associated with its recent acquisitions, including any failure to realize anticipated benefits of such acquisitions.
BlackRock is subject to risks associated with its recent acquisitions, including the GIP and HPS Acquisitions. BlackRock may not be able to realize the anticipated benefits of these acquisitions, including synergies, value creation or other benefits, fully or at all, or on the timeline BlackRock expects. At times, the resources of BlackRock and the acquired companies or the attention of certain members of their management may be focused on integration of the acquisition and diverted from day-to-day business operations, which may disrupt ongoing business. In addition, the process of integrating each acquired company may have an adverse impact on the Company, including from risks related to significant transaction and integration costs, unknown liabilities, employee turnover, divergence of management attention, litigation and/or regulatory actions related to the acquisition or if the acquired business does not perform as expected, which may cause BlackRock's AUM, revenue and earnings to decline.
```

## q20 (single)

**Question:** Which developments does Morgan Stanley say have increased cybersecurity risks for financial institutions?

**Reference:** New technologies (internet, mobile, cloud for financial transactions), the use of AI and the emergence of quantum computing, and more sophisticated organized crime, hackers, terrorists, nation-states and state-sponsored actors.

**Answer:** Morgan Stanley states that cybersecurity risks for financial institutions have increased due to the proliferation of new technologies, the use of the internet, mobile telecommunications, and cloud technologies for financial transactions, the use of artificial intelligence, the emergence of quantum computing, and the increased sophistication and activities of organized crime, hackers, terrorists, nation-states, and state-sponsored actors [MS_10K_FY2025#rf015]. Additionally, global events and geopolitical instability have led to increased nation-state targeting of financial institutions [MS_10K_FY2025#rf015].

Searches: ['Morgan Stanley cybersecurity risks developments']

```
[MS_10K_FY2025#rf015] Morgan Stanley 10-K 2025 · Risk Factors · Operational Risk > operations and/or increase costs. Any theft of data, technology or intellectual property may negatively impact our operations and reputat... · lines 40-43 of item_1a_risk_factors.txt
operations and/or increase costs. Any theft of data, technology or intellectual property may negatively impact our operations and reputation, including disrupting the business activities of our subsidiaries, affiliates, joint ventures or clients conducting business in those jurisdictions.
A cyberattack, information or security breach or a technology failure of ours or a third party could adversely affect our ability to conduct our business or manage our exposure to risk, or result in disclosure or misuse of personal, confidential or proprietary information and otherwise adversely impact our results of operations, liquidity and financial condition, as well as cause reputational harm.
Cybersecurity risks for financial institutions have significantly increased in recent years, in part because of the proliferation of new technologies; the use of the internet, mobile telecommunications and cloud technologies to conduct financial transactions; the use of artificial intelligence and the emergence of quantum computing; and the increased sophistication and activities of organized crime, hackers, terrorists, nation-states, state-sponsored actors and other parties. Any of these parties may also attempt to fraudulently induce employees, customers, clients, vendors or other third parties or users of our systems to disclose sensitive information in order to gain access to our networks, systems or data or those of our employees or clients, and such parties may see their effectiveness enhanced by the use of advanced systems, such as artificial intelligence. Global events and geopolitical instability have also led to increased nation-state targeting of financial institutions in the U.S. and abroad.
Information security risks may also derive from human error, fraud or malice on the part of our employees or third parties, software bugs, server malfunctions, software or hardware failure or other technological failure. For example, human error has led to the loss of the Firm's physical data-bearing devices in the past. These risks may be heightened by several factors, including remote work, reliance on new technologies (such as generative artificial intelligence) or as a result of the integration of acquisitions and
```

## q21 (multi)

**Question:** Whose wealth business grew net revenues faster in 2025: Goldman Sachs Asset & Wealth Management or Morgan Stanley Wealth Management?

**Reference:** Morgan Stanley Wealth Management: +12% to $31,754 million, vs +2% to $16.68 billion at Goldman Sachs AWM.

**Answer:** Morgan Stanley Wealth Management grew net revenues faster in 2025. 

* **Morgan Stanley Wealth Management** net revenues were $31,754 million in 2025, an increase of 12% compared with $28,420 million in 2024 [MS_10K_FY2025#mdna042].
* **Goldman Sachs Asset & Wealth Management** net revenues were $16,679 million in 2025, an increase of 2% compared with $16,316 million in 2024 [GS_10K_FY2025#mdna035].

Searches: ['Goldman Sachs Asset & Wealth Management net revenues 2025', 'Morgan Stanley Wealth Management net revenues 2025']

```
[GS_10K_FY2025#mdna035] Goldman Sachs 10-K 2025 · MD&A · Asset & Wealth Management · lines 381-403 of item_7_mdna.txt
The table below presents our Asset management and Wealth management net revenues by line item in Asset & Wealth Management.
$ in millions | Asset management | Wealth management | Asset & Wealth Management
Year Ended December 2025
Management and other fees | $4,990 | $6,548 | $11,538
Incentive fees | 489 | – | 489
Private banking and lending | – | 3,347 | 3,347
Investments | 1,305 | – | 1,305
Total | $6,784 | $9,895 | $16,679
Year Ended December 2024
Management and other fees | $4,573 | $5,842 | $10,415
Incentive fees | 393 | – | 393
Private banking and lending | – | 2,881 | 2,881
Investments | 2,625 | 2 | 2,627
Total | $7,591 | $8,725 | $16,316
Year Ended December 2023
Management and other fees | $4,205 | $5,272 | $9,477
Incentive fees | 161 | – | 161
Private banking and lending | – | 2,576 | 2,576
Investments | 1,639 | 349 | 1,988
Total | $6,005 | $8,197 | $14,202
Operating Environment. During 2025, Asset & Wealth Management operated in an environment generally characterized by ongoing geopolitical tensions and continued broad macroeconomic concerns and uncertainties, including those about changes in international trade policies (including tariffs). Global equity prices were generally higher compared with the end of 2024, positively affecting assets under supervision.
In the future, if market and economic conditions deteriorate, it may lead to a decline in asset prices, or investors transitioning to asset classes that typically generate lower fees or withdrawing their assets, and net revenues in Asset & Wealth Management would likely be negatively impacted.
2025 versus 2024. Net revenues in Asset & Wealth Management were $16.68 billion for 2025, 2% higher than 2024, reflecting higher Management and other fees, higher net revenues in Private banking and lending and, to a lesser extent, higher Incentive fees, largely offset by significantly lower net revenues in Investments.
```

```
[MS_10K_FY2025#mdna042] Morgan Stanley 10-K 2025 · MD&A · Wealth Management · lines 293-311 of item_7_mdna.txt
Wealth Management
Income Statement Information
% Change
$ in millions | 2025 | 2024 | 2023 | 2025 | 2024
Revenues
Asset management | $18,627 | $16,501 | $14,019 | 13% | 18%
Transactional 1 | 4,588 | 3,864 | 3,556 | 19% | 9%
Net interest | 7,911 | 7,313 | 8,118 | 8% | (10)%
Other 2 | 628 | 742 | 575 | (15)% | 29%
Net revenues | 31,754 | 28,420 | 26,268 | 12% | 8%
Provision for credit losses | 47 | 62 | 131 | (24)% | (53)%
Compensation and benefits | 16,950 | 15,207 | 13,972 | 11% | 9%
Non-compensation expenses | 5,464 | 5,411 | 5,635 | 1% | (4)%
Total non-interest expenses | 22,414 | 20,618 | 19,607 | 9% | 5%
Income before provision for income taxes | 9,293 | 7,740 | 6,530 | 20% | 19%
Provision for income taxes | 2,163 | 1,852 | 1,508 | 17% | 23%
Net income applicable to Morgan Stanley | $7,130 | $5,888 | $5,022 | 21% | 17%
1.Transactional includes Investment banking, Trading, and Commissions and fees revenues.
2.Other includes Investments and Other revenues.
```

## q22 (multi)

**Question:** At the end of 2025, how did Goldman Sachs' total assets under supervision compare with BlackRock's total AUM?

**Reference:** Goldman Sachs AUS was $3.61 trillion vs BlackRock AUM of $14.04 trillion, so BlackRock was about 3.9 times larger (the two measures are defined differently).

**Answer:** At the end of 2025, Goldman Sachs reported total assets under supervision (AUS) of $3,606 billion ($3.606 trillion) [GS_10K_FY2025#mdna039]. 

In comparison, BlackRock reported total assets under management (AUM) of $14,041,518 million ($14.0415 trillion) at the end of 2025 [BLK_10K_FY2025#mdna023].

Searches: ['Goldman Sachs assets under supervision 2025', 'BlackRock assets under management 2025']

```
[GS_10K_FY2025#mdna039] Goldman Sachs 10-K 2025 · MD&A · Asset Class · lines 420-426 of item_7_mdna.txt
(columns: $ in billions | 2025 | 2024 | 2023)
Asset Class
Alternative investments | $420 | $350 | $309
Equity | 951 | 772 | 658
Fixed income | 1,334 | 1,170 | 1,108
Total long-term AUS | 2,705 | 2,292 | 2,075
Liquidity products | 901 | 845 | 737
Total AUS | $3,606 | $3,137 | $2,812
```

```
[BLK_10K_FY2025#mdna023] BlackRock 10-K 2025 · MD&A · Assets Under Management · lines 174-197 of item_7_mdna.txt
(columns: (in millions) | 2025 | 2024 | 2025 | 2024)
ETFs | 5,467,710 | 4,230,375 | 526,711 | 390,433
Non-ETF index | 4,060,333 | 3,531,811 | (95,316) | 35,936
Long-term | 12,960,786 | 10,630,588 | 567,487 | 488,621
Cash management | 1,080,732 | 920,663 | 130,774 | 152,730
Total | $14,041,518 | $11,551,251 | $698,261 | $641,351
(1)Beginning in the first quarter of 2025, BlackRock updated the presentation of the Company's AUM line items. Such line items have been reclassified for 2024 to conform to this new presentation.
(2)Amounts include commodity ETFs and ETPs.
The following table presents the component changes in BlackRock's AUM for 2025 and 2024.
(in millions) | 2025 | 2024
Beginning AUM | $11,551,251 | $10,008,995
Net inflows (outflows):
Long-term | 567,487 | 488,621
Cash management | 130,774 | 152,730
Total net inflows (outflows) | 698,261 | 641,351
Realizations (1) | (33,125) | —
Acquisitions (2) | 120,961 | 73,949
Market change | 1,483,629 | 992,964
FX impact (3) | 220,541 | (166,008)
Total change | 2,490,267 | 1,542,256
Ending AUM | $14,041,518 | $11,551,251
(1)Beginning in the first quarter of 2025, BlackRock updated the presentation of net flows to separately disclose realizations, which represent return of capital/return on investments. Realizations in 2024 have not been recast.
(2)Amount for 2025 included AUM attributable to the HPS and ElmTree Transactions. Amount for 2024 includes AUM attributable to the GIP Transaction and the SpiderRock Advisors transaction in May 2024 (the "SpiderRock Transaction").
(3)Foreign exchange reflects the impact of translating non-US dollar denominated AUM into US dollars for reporting purposes.
BlackRock has historically grown AUM through organic growth and acquisitions. Management believes that the Company will be able to continue to grow AUM organically by focusing on strong investment performance, efficient delivery of beta for index products, client service, developing new products and optimizing distribution capabilities.
```

## q23 (multi)

**Question:** Compare the total average fee rate Goldman Sachs earned on its AUS with Morgan Stanley Investment Management's total average fee rate in 2025.

**Reference:** Both were 31 basis points in 2025 (Goldman flat vs 2024; Morgan Stanley down from 32 bps).

**Answer:** In 2025, the total average effective management fee Goldman Sachs earned on its assets under supervision (AUS) was 31 basis points [GS_10K_FY2025#mdna042]. 

For Morgan Stanley Investment Management, the total average fee rate in 2025 was also 31 basis points (based on asset management revenues, net of waivers, excluding performance-based fees and other non-management fees) [MS_10K_FY2025#mdna061].

Searches: ['Goldman Sachs average fee rate AUS 2025', 'Morgan Stanley Investment Management average fee rate 2025']

```
[GS_10K_FY2025#mdna042] Goldman Sachs 10-K 2025 · MD&A · Asset Class · lines 478-497 of item_7_mdna.txt
(columns: $ in billions | 2025 | 2024 | 2023)
Asset Class
Alternative investments | $376 | $328 | $283
Equity | 853 | 731 | 610
Fixed income | 1,246 | 1,150 | 1,036
Total long-term AUS | 2,475 | 2,209 | 1,929
Liquidity products | 853 | 751 | 749
Total AUS | $3,328 | $2,960 | $2,678
We earn management fees on client assets that we manage and also receive incentive fees based on a percentage of a fund's or a separately managed account's return, or when the return exceeds a specified benchmark or other performance targets. These incentive fees are recognized when it is probable that a significant reversal of such fees will not occur. Our estimated unrecognized incentive fees were $5.24 billion as of December 2025, $4.12 billion as of December 2024 and $3.77 billion as of December 2023. Such amounts are based on the completion of the funds' financial statements, which is generally one quarter in arrears. These fees will be recognized, assuming no decline in fair value, if and when it is probable that a significant reversal of such fees will not occur, which is generally when such fees are no longer subject to fluctuations in the market value of the assets.
The table below presents our average effective management fee (which excludes non-asset-based fees) earned on our AUS by asset class.
Year Ended December
Effective fees (bps) | 2025 | 2024 | 2023
Alternative investments | 58 | 60 | 62
Equity | 54 | 55 | 57
Fixed income | 17 | 17 | 17
Liquidity products | 14 | 15 | 15
Total average effective fee | 31 | 31 | 31
The table below presents details about our monthly average AUS for alternative assets and the average effective management fee we earned on such assets.
Funds & discretionary accounts | Advisory | Total
$ in billions | Direct strategies | Fund of funds | Total | & OCIO accounts | alternative AUS
Year Ended December 2025
```

```
[MS_10K_FY2025#mdna061] Morgan Stanley 10-K 2025 · MD&A · Average Fee Rates1 · lines 482-493 of item_7_mdna.txt
Average Fee Rates1
Fee rate in bps | 2025 | 2024 | 2023
Equity | 69 | 71 | 71
Fixed income | 36 | 36 | 35
Alternatives and Solutions | 27 | 28 | 32
Long-term AUM | 40 | 42 | 44
Liquidity and Overlay Services | 12 | 12 | 13
Total | 31 | 32 | 34
1.Based on Asset management revenues, net of waivers, excluding performance-based fees and other non-management fees. For certain non-U.S. funds, it includes the portion of advisory fees that the advisor collects on behalf of third-party distributors. The payment of those fees to the distributor is included in Non-compensation expenses in the income statement.
Asset management and other related fees within the Investment Management segment are primarily generated from Equity, Fixed Income and the following products:
Alternatives and Solutions. Includes products in fund of funds, real estate, infrastructure, private equity and credit strategies and multi-asset portfolios, as well as systematic strategies that create custom investment solutions, including those offered by Parametric.
Liquidity and Overlay Services. Includes liquidity products, as well as overlay services, which represent investment strategies that use passive exposure instruments to obtain, offset or substitute specific portfolio exposures, beyond those provided by the underlying holdings of the fund.
```

## q24 (multi)

**Question:** Which firm had the higher effective tax rate in 2025, Goldman Sachs or Morgan Stanley?

**Reference:** Morgan Stanley: 22.5% vs Goldman Sachs 21.4%.

**Answer:** Morgan Stanley had the higher effective tax rate in 2025 at 22.5% [MS_10K_FY2025#mdna009], compared to Goldman Sachs' effective tax rate of 21.4% [GS_10K_FY2025#mdna014].

Searches: ['Goldman Sachs effective tax rate 2025', 'Morgan Stanley effective tax rate 2025']

```
[GS_10K_FY2025#mdna014] Goldman Sachs 10-K 2025 · MD&A · Provision for Taxes · lines 120-122 of item_7_mdna.txt
Provision for Taxes
The effective tax rate for 2025 was 21.4%, down from the full year effective tax rate of 22.4% for 2024, primarily due to an increase in tax benefits on the settlement of employee share-based awards, partially offset by a decrease in the impact of other permanent tax benefits, for 2025 compared with the full year of 2024. The impact of tax benefits related to employee share-based awards was a reduction to provision for taxes for 2025 of approximately $620 million, which reduced our effective tax rate by 2.8 percentage points, and increased our diluted EPS by $1.95 and annualized ROE by 0.5 percentage points.
The Organisation for Economic Co-operation and Development/G20 (OECD/G20) Global Anti-Base Erosion Model Rules (Pillar II Model Rules) aim to ensure that multinationals with revenues in excess of EUR 750 million pay a minimum effective corporate tax rate of 15% (minimum tax) in each jurisdiction in which they operate. The U.K. and other non-U.S. jurisdictions in which we operate have enacted certain portions of the Pillar II Model Rules through domestic legislation (Pillar II legislation). In January 2026, the OECD/G20 released administrative guidance that allows multinationals with a U.S. parent to elect the side-by-side safe harbor. The safe harbor deems certain Pillar II minimum taxes to be zero for tax years beginning on or after January 1, 2026. Certain jurisdictions automatically adopted the safe harbor; however, the majority of jurisdictions that enacted Pillar II legislation will need to adopt the safe harbor into their local laws through legislation or administrative procedures. Domestic minimum top-up taxes still apply under the Pillar II legislation in certain non-U.S. jurisdictions in which we operate. The Pillar II legislation did not have a material impact on our 2025 effective tax rate and is not expected to have a material impact on our 2026 effective tax rate. Any domestic minimum top-up taxes under the Pillar II legislation will be recognized in the period in which they are incurred.
```

```
[MS_10K_FY2025#mdna009] Morgan Stanley 10-K 2025 · MD&A · Consolidated financial measures · lines 55-60 of item_7_mdna.txt
(columns: $ in millions, except per share data | 2025 | 2024 | 2023)
Consolidated financial measures
Expense efficiency ratio 1 | 68% | 71% | 77%
ROE 2 | 16.6% | 14.0% | 9.4%
ROTCE 2,3 | 21.6% | 18.8% | 12.8%
Pre-tax margin 4 | 31% | 28% | 22%
Effective tax rate | 22.5% | 23.1% | 21.9%
```

## q25 (multi)

**Question:** How do Goldman Sachs and BlackRock each describe the risk that AI models produce wrong output?

**Reference:** Goldman: AI models, especially generative AI, may produce incorrect output, leak confidential information, reflect bias or infringe IP. BlackRock: generative AI may create content that appears correct but is factually inaccurate, and data or outputs may be insufficient, biased or harmful, leading to bad decisions or operating errors.

**Answer:** **Goldman Sachs** describes the risk by stating that AI models, particularly generative AI models, may produce incorrect outputs, release private or confidential information, reflect training data biases, infringe on intellectual property rights, or otherwise prove harmful [GS_10K_FY2025#rf033]. Goldman also notes that model complexity limits transparency, making it challenging to understand outputs, assess proper operation, reduce erroneous outputs, and eliminate bias [GS_10K_FY2025#rf033].

**BlackRock** similarly notes that AI technologies and generative AI may create content that appears correct but is factually inaccurate or flawed, and that datasets, generated content, or application of systems may prove insufficient, biased, or harmful, leading to adverse business decisions or operating errors [BLK_10K_FY2025#rf022].

Searches: ['Goldman Sachs risk artificial intelligence models wrong output error', 'BlackRock risk artificial intelligence models wrong output error']

```
[GS_10K_FY2025#rf033] Goldman Sachs 10-K 2025 · Risk Factors · Operational > The development and use of AI present risks and challenges that may adversely impact our business. · lines 128-129 of item_1a_risk_factors.txt
The development and use of AI present risks and challenges that may adversely impact our business.
We or our third-party vendors, clients or counterparties have in the past developed or incorporated and may in the future develop or incorporate AI technology in certain business processes, services or products. The development and use of AI present a number of risks and challenges to our business. The legal and regulatory environment relating to AI is uncertain and rapidly evolving, both in the U.S. and internationally, and includes regulation targeted specifically at AI, as well as provisions in intellectual property, privacy, consumer protection, employment and other laws applicable to the use of AI. These evolving laws and regulations have in the past required and may in the future require changes in our implementation of AI technology and increase our compliance costs and the risk of non-compliance. AI models, particularly generative AI models, may produce output or take action that is incorrect, that result in the release of private, confidential or proprietary information, that reflect biases included in the data on which they are trained, infringe on the intellectual property rights of others, or that is otherwise harmful. In addition, the complexity of many AI models makes it challenging to understand why they are generating particular outputs. This limited transparency increases the challenges associated with assessing the proper operation of AI models, understanding and monitoring the capabilities of the AI models, reducing erroneous output, eliminating bias and complying with regulations that require documentation or explanation of the basis on which decisions are made. Further, we rely on AI models developed by third parties, and, to that extent, are dependent in part on the manner in which those third parties develop and train their models, including risks arising from the inclusion of any unauthorized material in the training data for their models, and the effectiveness of the steps these third parties
```

```
[BLK_10K_FY2025#rf022] BlackRock 10-K 2025 · Risk Factors · TECHNOLOGY AND OPERATIONAL RISKS > A failure to effectively manage the development and use of AI, combined with an evolving regulatory environment, could have an adverse ef... · lines 62-63 of item_1a_risk_factors.txt
A failure to effectively manage the development and use of AI, combined with an evolving regulatory environment, could have an adverse effect on BlackRock's growth, reputation or business.
BlackRock uses machine learning and AI in its business and expects to continue to expand its AI capabilities, including through generative AI. AI technologies are complex and rapidly evolving, and the introduction of AI into new or existing processes may result in new or enhanced governmental or regulatory scrutiny, IP or other litigation, data protection, confidentiality or information security risks, social or ethical concerns, competitive harm or other complications. For example, the use of datasets to develop and test AI models, the content generated by AI systems, or the application of AI systems may be found to be insufficient, biased or harmful, or lead to adverse business decisions or operating errors. AI technologies, including generative AI, may create content that appears correct but is factually inaccurate or flawed. In addition, IP ownership and license rights, including copyright, surrounding AI technologies are still being developed and have not been fully addressed by US courts or federal, state or non-US laws or regulation. Furthermore, regulatory scrutiny of AI technologies and controls continues to evolve globally with new and forthcoming laws and regulations. The volume and reliance on data and algorithms may make AI, and BlackRock, more susceptible to cybersecurity threats, including the compromise of underlying models, training data or other IP. Efforts around use of these technologies require additional investment in operational controls and procedures, development and implementation of appropriate protections and safeguards for handling the use of data with AI, including with respect to data leakage, fraud prevention and regulatory compliance costs. AI technologies may also disrupt the competitive landscape for investment management and technology services, including in commercial and operational areas such as data aggregation and quantitative models. Any failure to successfully integrate AI technologies, respond to client or market demands, accurately communicate AI initiat
```

## q26 (multi)

**Question:** What share of BlackRock's 2025 revenue came from performance fees, and which product category produced the most of them?

**Reference:** About 6% ($1.4 billion; $1,424 million); private markets alternatives generated the most, $695 million (liquid alternatives $558 million).

**Answer:** Performance fees represented $1.4 billion, or 6%, of BlackRock's total revenue for the year ended December 31, 2025 [BLK_10K_FY2025#rf014]. 

Within investment advisory performance fees of $1,424 million, the product category that produced the most was **Alternatives** (with a subtotal of $1,253 million), specifically led by **Private markets**, which generated $695 million [BLK_10K_FY2025#mdna038].

Searches: ['BlackRock 2025 performance fees revenue product category']

```
[BLK_10K_FY2025#mdna038] BlackRock 10-K 2025 · MD&A · Revenue · lines 406-445 of item_7_mdna.txt
Revenue
The table below presents detail of revenue for 2025 and 2024 and includes the product type mix of base fees and securities lending revenue and performance fees.
(in millions) | 2025 | 2024
Revenue:
Investment advisory, administration fees and securities lending revenue (1) :
Equity:
Active | $2,167 | $2,166
ETFs | 6,043 | 5,124
Equity subtotal | 8,210 | 7,290
Fixed income:
Active | 2,018 | 1,952
ETFs | 1,532 | 1,367
Fixed income subtotal | 3,550 | 3,319
Active multi-asset | 1,332 | 1,248
Alternatives:
Private markets | 2,350 | 1,196
Liquid alternatives | 669 | 568
Alternatives subtotal | 3,019 | 1,764
Non-ETF index | 1,321 | 1,183
Digital assets, commodities and multi-asset ETFs (2) | 502 | 247
Long-term | 17,934 | 15,051
Cash management | 1,245 | 1,049
Total investment advisory, administration fees and securities lending revenue (3) | 19,179 | 16,100
Investment advisory performance fees:
Equity | 132 | 161
Fixed income | 16 | 34
Multi-asset | 23 | 24
Alternatives:
Private markets | 695 | 308
Liquid alternatives | 558 | 680
Alternatives subtotal | 1,253 | 988
Total investment advisory performance fees | 1,424 | 1,207
Technology services and subscription revenue | 1,981 | 1,603
Distribution fees | 1,355 | 1,273
Advisory and other revenue:
Advisory | 50 | 49
Other | 227 | 175
Total advisory and other revenue | 277 | 224
Total revenue | $24,216 | $20,407
(1)Beginning in the first quarter of 2025, BlackRock reclassified the presentation of the Company's investment advisory, administration fees and securities lending revenue line items to align with the updated presentation of the Company's AUM line items. Such line items have been reclassified for 2024 to conform to this new presentation. See page 11 of Exhibit 99.2 to the Current Report on Form 8-K furnished on April 11, 2025 for the reclassified presentation of the 2024 investment advisory, administration fees and securities lending revenue line items.
```

```
[BLK_10K_FY2025#rf014] BlackRock 10-K 2025 · Risk Factors · RISKS RELATED TO INVESTMENT PERFORMANCE > Performance fees may increase volatility of both revenue and earnings. · lines 44-45 of item_1a_risk_factors.txt
Performance fees may increase volatility of both revenue and earnings.
Part of BlackRock's revenue is derived from performance fees on investment advisory assignments. Performance fees represented $1.4 billion, or 6%, of total revenue for the year ended December 31, 2025. Generally, the Company is entitled to a performance fee only if the agreement under which it is managing the assets provides for one and if returns on the related portfolio exceed agreed-upon periodic or cumulative return targets. If these targets are not exceeded, a performance fee for that period will not be earned and, if targets are based on cumulative returns, the Company may not earn performance fees in future periods. The volatility of the Company's future revenue and earnings may also be affected due to private markets becoming an increasing component of the overall composition of the Company's performance fee generating assets, including from the Company's acquisition of GIP (the "GIP Acquisition") and HPS (the "HPS Acquisition"). In particular, the Company expects that as it manages various longer-horizon private markets strategies, its performance fees may be recognized over substantially longer multi-year periods than those associated with more liquid products.
```

## q27 (unanswerable)

**Question:** What were Goldman Sachs' Asset & Wealth Management net revenues in the third quarter of 2026?

**Reference:** Not in the indexed 10-Ks (they cover fiscal 2025). After adding the Q3 2026 10-Q: $5.05 billion, 14% higher than Q3 2025.

**Answer:** The indexed filings do not cover this. They cover annual financial data for Goldman Sachs' Asset & Wealth Management segment for the years ended December 31, 2025, 2024, and 2023 [GS_10K_FY2025#mdna034].

Searches: ['Goldman Sachs Asset & Wealth Management net revenues third quarter 2026']

```
[GS_10K_FY2025#mdna034] Goldman Sachs 10-K 2025 · MD&A · Asset & Wealth Management · lines 356-380 of item_7_mdna.txt
The table below presents our average Asset & Wealth Management gross loans.
Year Ended December
$ in millions | 2025 | 2024
Loans | $49,593 | $44,948
The table below presents our Asset & Wealth Management operating results.
Year Ended December
$ in millions | 2025 | 2024 | 2023
Management and other fees | $11,538 | $10,415 | $9,477
Incentive fees | 489 | 393 | 161
Private banking and lending | 3,347 | 2,881 | 2,576
Investments | 1,305 | 2,627 | 1,988
Total net revenues | 16,679 | 16,316 | 14,202
Provision for credit losses | (111) | (280) | (539)
Compensation and benefits expenses | 7,432 | 6,564 | 6,116
Other operating expenses | 5,231 | 5,167 | 6,862
Total operating expenses | 12,663 | 11,731 | 12,978
Pre-tax earnings | 4,127 | 4,865 | 1,763
Provision for taxes | 883 | 1,090 | 365
Net earnings | 3,244 | 3,775 | 1,398
Preferred stock dividends | 151 | 135 | 121
Net earnings to common | $3,093 | $3,640 | $1,277
Average common equity | $24,666 | $24,983 | $28,635
Return on average common equity | 12.5% | 14.6% | 4.5%
In the table above, Management and other fees included fees from alternatives of $2.37 billion for 2025, $2.19 billion for 2024 and $2.14 billion for 2023. In 2026, we announced a target to achieve an annual double-digit percentage growth rate for Management and other fees from alternatives.
In 2026, we announced targets to achieve ROE in the high-teens (approximately 17% to 19%) and pre-tax margin of approximately 30% within the medium term (three-to five-year time horizon from year-end 2025) for Asset & Wealth Management. The ROE for Asset & Wealth Management was 12.5% and the pre-tax margin was 25% for 2025. The net impact of historical principal investments and the related attributed equity and the FDIC special assessment fee reduced the ROE for Asset & Wealth Management by approximately 2.3 percentage points.
```

## q28 (unanswerable)

**Question:** What was Morgan Stanley's Liquidity Coverage Ratio at the end of 2025?

**Reference:** The indexed sections don't cover Morgan Stanley's LCR (the liquidity section of MD&A is not in the corpus).

**Answer:** The indexed filings do not cover this. The liquidity, capital, and balance sheet sections (including Liquidity Coverage Ratios) are not indexed in MD&A or Risk Factors; the indexed passages do cover capital ratios such as the Standardized Common Equity Tier 1 capital ratio of 15.0% and Supplementary Leverage Ratio of 5.4% at December 31, 2025 [MS_10K_FY2025#mdna002].

Searches: ['Morgan Stanley Liquidity Coverage Ratio 2025']

```
[MS_10K_FY2025#mdna002] Morgan Stanley 10-K 2025 · MD&A · Executive Summary · lines 9-18 of item_7_mdna.txt
Executive Summary
Overview of Financial Results
Consolidated Results—Full Year Ended December 31, 2025
•The Firm reported net revenues of $70.6 billion and net income applicable to Morgan Stanley of $16.9 billion reflecting strong results across our business segments and demonstrating the strength of our Integrated Firm.
•The Firm delivered ROE of 16.6% and ROTCE of 21.6% (see "Selected Non-GAAP Financial Information" herein).
•The Firm expense efficiency ratio was 68% compared to 71% in the prior year, demonstrating operating leverage while continuing to invest in our businesses.
•At December 31, 2025, the Firm's Standardized Common Equity Tier 1 capital ratio was 15.0%, and its Supplementary Leverage Ratio was 5.4%.
•Institutional Securities net revenues of $33.1 billion, primarily reflecting strong performance in Equity on higher client activity and higher underwriting and Advisory revenues within Investment Banking.
•Wealth Management delivered net revenues of $31.8 billion, primarily reflecting higher Asset management revenues on higher market levels and the cumulative impact of strong fee-based flows. The pre-tax margin was 29.3%. Fee-based asset flows were $160 billion and the business added net new assets of $356 billion.
•Investment Management reported net revenues of $6.5 billion, primarily reflecting higher asset management fees driven by higher average AUM on higher market levels.
```

## q29 (unanswerable)

**Question:** What were JPMorgan's Asset & Wealth Management net revenues in 2025?

**Reference:** JPMorgan's filings are not in the corpus, which covers Goldman Sachs, Morgan Stanley and BlackRock.

**Answer:** The indexed filings do not cover this. They cover Goldman Sachs, Morgan Stanley, and BlackRock, where Goldman Sachs reported Asset & Wealth Management net revenues of $16,679 million in 2025 [GS_10K_FY2025#mdna034].

Searches: ['JPMorgan Asset Wealth Management net revenues 2025']

```
[GS_10K_FY2025#mdna034] Goldman Sachs 10-K 2025 · MD&A · Asset & Wealth Management · lines 356-380 of item_7_mdna.txt
The table below presents our average Asset & Wealth Management gross loans.
Year Ended December
$ in millions | 2025 | 2024
Loans | $49,593 | $44,948
The table below presents our Asset & Wealth Management operating results.
Year Ended December
$ in millions | 2025 | 2024 | 2023
Management and other fees | $11,538 | $10,415 | $9,477
Incentive fees | 489 | 393 | 161
Private banking and lending | 3,347 | 2,881 | 2,576
Investments | 1,305 | 2,627 | 1,988
Total net revenues | 16,679 | 16,316 | 14,202
Provision for credit losses | (111) | (280) | (539)
Compensation and benefits expenses | 7,432 | 6,564 | 6,116
Other operating expenses | 5,231 | 5,167 | 6,862
Total operating expenses | 12,663 | 11,731 | 12,978
Pre-tax earnings | 4,127 | 4,865 | 1,763
Provision for taxes | 883 | 1,090 | 365
Net earnings | 3,244 | 3,775 | 1,398
Preferred stock dividends | 151 | 135 | 121
Net earnings to common | $3,093 | $3,640 | $1,277
Average common equity | $24,666 | $24,983 | $28,635
Return on average common equity | 12.5% | 14.6% | 4.5%
In the table above, Management and other fees included fees from alternatives of $2.37 billion for 2025, $2.19 billion for 2024 and $2.14 billion for 2023. In 2026, we announced a target to achieve an annual double-digit percentage growth rate for Management and other fees from alternatives.
In 2026, we announced targets to achieve ROE in the high-teens (approximately 17% to 19%) and pre-tax margin of approximately 30% within the medium term (three-to five-year time horizon from year-end 2025) for Asset & Wealth Management. The ROE for Asset & Wealth Management was 12.5% and the pre-tax margin was 25% for 2025. The net impact of historical principal investments and the related attributed equity and the FDIC special assessment fee reduced the ROE for Asset & Wealth Management by approximately 2.3 percentage points.
```

## q30 (unanswerable)

**Question:** How much of Goldman Sachs' assets under supervision came from clients in Switzerland at the end of 2025?

**Reference:** Not disclosed: Goldman reports AUS only by region (Americas, EMEA, Asia), not by country.

**Answer:** The indexed filings do not cover this. They do report total assets under supervision broken down by region (Americas, EMEA, and Asia), showing total AUS in EMEA of $820 billion at the end of 2025, but do not provide a country-by-country breakdown for Switzerland [GS_10K_FY2025#mdna040].

Searches: ['Goldman Sachs assets under supervision Switzerland 2025']

```
[GS_10K_FY2025#mdna040] Goldman Sachs 10-K 2025 · MD&A · Region · lines 427-459 of item_7_mdna.txt
(columns: $ in billions | 2025 | 2024 | 2023)
Region
Americas | $2,538 | $2,235 | $1,951
EMEA | 820 | 683 | 653
Asia | 248 | 219 | 208
Total AUS | $3,606 | $3,137 | $2,812
Vehicle
Separate accounts | $1,962 | $1,687 | $1,557
Public funds | 1,130 | 1,004 | 901
Private funds and other | 514 | 446 | 354
Total AUS | $3,606 | $3,137 | $2,812
In the table above:
•Liquidity products includes money market funds and private bank deposits.
•EMEA represents Europe, Middle East and Africa.
In 2026, we announced a target to grow our total alternative AUS to $750 billion by the end of 2030.
The table below presents our total long-term AUS by client channel.
As of December
$ in billions | 2025 | 2024 | 2023
Institutional | $1,193 | $1,057 | $1,009
Wealth management | 945 | 794 | 678
Third-party distributed | 567 | 441 | 388
Total long-term AUS | $2,705 | $2,292 | $2,075
Total wealth management client assets (consisting of AUS, brokerage assets and Marcus deposits) were approximately $1.9 trillion as of December 2025 and approximately $1.6 trillion as of December 2024.
The table below presents changes in our AUS.
Year Ended December
$ in billions | 2025 | 2024 | 2023
Beginning balance | $3,137 | $2,812 | $2,547
Net inflows/(outflows):
Alternative investments | 52 | 38 | 24
Equity | 35 | 15 | (18)
Fixed income | 81 | 53 | 46
Total long-term AUS net inflows/(outflows) | 168 | 106 | 52
Liquidity products | 56 | 108 | 26
Total AUS net inflows/(outflows) | 224 | 214 | 78
```

## q31 (unanswerable)

**Question:** By how much will BlackRock raise its quarterly dividend in 2026?

**Reference:** The corpus contains no 2026 dividend decision; it only reports dividends paid in 2025 ($20.84 per share).

**Answer:** The indexed filings do not cover this. They do report that cash dividends declared and paid per share were $20.84 in 2025 and $20.40 in 2024 [BLK_10K_FY2025#mdna013].

Searches: ['BlackRock quarterly dividend 2026']

```
[BLK_10K_FY2025#mdna013] BlackRock 10-K 2025 · MD&A · Executive Summary · lines 39-67 of item_7_mdna.txt
Executive Summary
(in millions, except per share data) | 2025 | 2024
GAAP basis (1) :
Total revenue | $24,216 | $20,407
Total expense | 17,171 | 12,833
Operating income | $7,045 | $7,574
Operating margin | 29.1% | 37.1%
Nonoperating income (expense), less net income (loss) attributable to noncontrolling interests ("NCI") - consolidated sponsored investment products ("CIPs") | 312 | 578
Income tax expense | 1,677 | 1,783
Less: Net income (loss) attributable to NCI - Subco | 127 | —
Net income attributable to BlackRock | $5,553 | $6,369
Diluted earnings per common share | $35.31 | $42.01
Effective tax rate | 22.8% | 21.9%
As adjusted (2) :
Operating income | $9,600 | $8,110
Operating margin | 44.1% | 44.5%
Nonoperating income (expense), less net income (loss) attributable to NCI - CIPs | $251 | $533
Net income attributable to BlackRock (3) | $7,736 | $6,612
Diluted earnings per common share (3) | $48.09 | $43.61
Effective tax rate | 21.5% | 23.5%
Other:
Assets under management (end of period) | $14,041,518 | $11,551,251
Diluted weighted-average common shares outstanding (including Subco Units) | 160.9 | 151.6
Shares outstanding including Subco Units (4) | 162.8 | 154.9
Book value per share (5) | $360.41 | $306.52
Cash dividends declared and paid per share | $20.84 | $20.40
(1)Accounting principles generally accepted in the United States ("GAAP").
(2)As adjusted items are described in more detail in Non-GAAP Financial Measures.
(3)Beginning in the third quarter of 2025, net income attributable to BlackRock, Inc., as adjusted, and diluted earnings per common share, as adjusted, assume all Subco Units have been exchanged in accordance with their terms on a one-for-one basis into common stock of BlackRock. Accordingly, the noncontrolling interest allocated to these Subco Units has been included as part of net income attributable to BlackRock, Inc., as adjusted. See Non-GAAP Financial Measures for further information.
```

## q32 (unanswerable)

**Question:** What were Morgan Stanley Wealth Management's net new assets in 2022?

**Reference:** The 2025 10-K reports net new assets only for 2023-2025, so 2022 is not covered.

**Answer:** The indexed filings do not cover Morgan Stanley Wealth Management's net new assets for 2022. They do cover net new assets for the years 2023, 2024, and 2025 [MS_10K_FY2025#mdna044].

Searches: ['Morgan Stanley Wealth Management net new assets 2022', 'Morgan Stanley Wealth Management "2022" "Net new assets"']

```
[MS_10K_FY2025#mdna044] Morgan Stanley 10-K 2025 · MD&A · Annualized weighted average cost of deposits 4 · lines 318-326 of item_7_mdna.txt
(columns: $ in billions | At December 31, 2025 | At December 31, 2024)
Annualized weighted average cost of deposits 4
Period end | 2.51% | 2.73%
Period average | 2.76% | 3.05%
2025 | 2024 | 2023
Net new assets | $356.3 | $251.7 | $282.3
1.Client assets represent those for which Wealth Management is providing services including financial advisor-led brokerage, investment advisory, custody, cash management, and administrative services; self-directed brokerage and investment advisory services; financial and wealth planning services; workplace services, including stock plan administration, and retirement plan services. As part of the Integrated Firm, Wealth Management may provide these services to clients who also use the services of one or more other business segments. See "Advisor-Led Channel" and "Self-Directed Channel" herein for additional information.
2.Margin and other lending represents margin lending arrangements, which allow customers to borrow against the value of qualifying securities and other lending which includes non‐purpose securities-based lending on non‐bank entities.
3.Deposits reflect liabilities sourced from Wealth Management clients and other sources of funding on our U.S. Bank Subsidiaries. Deposits include sweep deposit programs, savings and other deposits, and time deposits.
4.Annualized weighted average represents the total annualized weighted average cost of the various deposit products. Amounts include the effect of related hedging derivatives. The period end cost of deposits is based upon balances and rates as of December 31, 2025 and December 31, 2024. The period average is based on daily balances and rates for the period.
```
