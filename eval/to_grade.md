# Answers to grade by hand

For each answer fill one row in eval/human_labels.csv: id,correct,supported,notes
correct = 1 if right against the reference (or a proper refusal); supported = 1 if every
claim is in the retrieved passages; notes are required for every 0.

## q01 (single)
**Question:** What is the maximum share of a UCITS's assets that can be invested in transferable securities issued by a single body?
**Reference:** 5% of its assets. Member States may raise this to 10%, but then holdings above 5% per issuer may not exceed 40% of assets in total.

**Agent answer:**

A UCITS shall invest no more than 5% of its assets in transferable securities or money market instruments issued by the same body [ucits_directive, Article 52(1)]. 

**Exceptions and higher limits:**
* **10% limit:** Member States may raise the 5% limit to a maximum of 10%, provided that the total value of the transferable securities and money market instruments held by the UCITS in issuing bodies in each of which it invests more than 5% of its assets does not exceed 40% of the value of its assets [ucits_directive, Article 52(2)].
* **35% limit for public issues:** Member States may raise the limit to a maximum of 35% if the transferable securities or money market instruments are issued or guaranteed by a Member State, its local authorities, a third country, or a public international body to which one or more Member States belong [ucits_directive, Article 52(3)].
* **25% limit for certain bonds:** Member States may raise the limit to a maximum of 25% for bonds issued by a credit institution with its registered office in a Member State that is subject by law to special public supervision protecting bond-holders (where investments exceeding 5% in a single issuer cannot in total exceed 80% of the UCITS' assets) [ucits_directive, Article 52(4)].
* **20% limit for index-tracking funds:** Member States may raise the limit to a maximum of 20% for investment in shares or debt securities issued by the same body when the fund's investment policy aims to replicate a recognized stock or debt securities index under specific diversification and benchmark criteria [ucits_directive, Article 53(1)].

*Note: This answer reflects solely the provisions of Directive 2009/65/EC (UCITS Directive) as indexed in the corpus.*

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 55 to Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.77)
UCITS itself and to the other UCITS or collective investment undertaking in which it invests. 1. An investment company or a management company acting in connection with all of the common funds which it manages and which fall within the scope of this Directive shall not acquire any shares carrying voting rights which would enable it to exercise significant influence over the management of an issuing body. Pending further coordination, Member States shall take account of existing rules defining the principle stated in the first subparagraph in the law of other Member States. 2. A UCITS may acquire no more than: (a) 10 % of the non-voting shares of a single issuing body; (b) 10 % of the debt securities of a single issuing body; (c) 25 % of the units of a single UCITS or other collective investment undertaking within the meaning of Article 1(2)(a) and (b); or (d) 10 % of the money market instruments of a single issuing body. The limits laid down in points (b), (c) and (d) may be disregarded at the time of acquisition if at that time the gross amount of the debt securities or of the money market instruments, or the net

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
instruments issued by the same body; or (b) 20 % of its assets in deposits made with the same body. The risk exposure to a counterparty of the UCITS in an OTC derivative transaction shall not exceed either: (a) 10 % of its assets when the counterparty is a credit institution referred to in Article 50(1)(f); or (b) 5 % of its assets, in other cases. 2. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 10 %. If they do so, however, the total value of the transferable securities and the money market instruments held by the UCITS in the issuing bodies in each of which it invests more than 5 % of its assets shall not exceed 40 % of the value of its assets. That limitation shall not apply to deposits or OTC derivative transactions made with financial institutions subject to prudential supervision. Notwithstanding the individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member State, by its local authorities, by a third country or by a public international body to which one or more Member States belong. 4. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 25 % where bonds are issued by a credit institution which has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in

---

[ucits_directive, Article 52 to Article 53] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
instruments made with this body carried out in accordance with paragraphs 1 to 4 shall not exceed in total 35 % of the assets of the UCITS. Companies which are included in the same group for the purposes of consolidated accounts, as defined in Directive 83/349/EEC or in accordance with recognised international accounting rules, shall be regarded as a single body for the purpose of calculating the limits contained in this Article. Member States may allow cumulative investment in transferable securities and money market instruments within the same group up to a limit of 20 %. 1. Without prejudice to the limits laid down in Article 56, Member States may raise the limits laid down in Article 52 to a maximum of 20 % for investment in shares or debt securities issued by the same body when, according to the fund rules or instruments of incorporation, the aim of the UCITS’ investment policy is to replicate the composition of a certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it

---

[ucits_directive, Article 54 to Article 55] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
prominent statement in its prospectus and marketing communications drawing attention to such authorisation and indicating the Member States, local authorities, or public international bodies in the securities of which it intends to invest or has invested more than 35 % of its assets. 1. A UCITS may acquire the units of UCITS or other collective investment undertakings referred to in Article 50(1)(e), provided that no more than 10 % of its assets are invested in units of a single UCITS or other collective investment undertaking. Member States may raise that limit to a maximum of 20 %. 2. Investments made in units of collective investment undertakings other than UCITS shall not exceed, in aggregate, 30 % of the assets of the UCITS. Member States may, where a UCITS has acquired units of another UCITS or collective investment undertakings, provide that the assets of the respective UCITS or other collective investment undertakings are not re
```
</details>

## q02 (single)
**Question:** How much of a UCITS's assets can be placed in deposits with the same body?
**Reference:** No more than 20% of its assets.

**Agent answer:**

A UCITS may invest no more than 20% of its assets in deposits made with the same body [ucits_directive, Article 52(1)]. 

Additionally, a UCITS must not combine investments in transferable securities or money market instruments issued by a single body, deposits made with that body, and/or exposures arising from OTC derivative transactions undertaken with that body if it would lead to more than 20% of its assets being invested in a single body [ucits_directive, Article 52(1) to Article 52(2)].

Please note that this answer reflects the indexed version of Directive 2009/65/EC (UCITS Directive) only; later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.78)
instruments issued by the same body; or (b) 20 % of its assets in deposits made with the same body. The risk exposure to a counterparty of the UCITS in an OTC derivative transaction shall not exceed either: (a) 10 % of its assets when the counterparty is a credit institution referred to in Article 50(1)(f); or (b) 5 % of its assets, in other cases. 2. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 10 %. If they do so, however, the total value of the transferable securities and the money market instruments held by the UCITS in the issuing bodies in each of which it invests more than 5 % of its assets shall not exceed 40 % of the value of its assets. That limitation shall not apply to deposits or OTC derivative transactions made with financial institutions subject to prudential supervision. Notwithstanding the individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member State, by its local authorities, by a third country or by a public international body to which one or more Member States belong. 4. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 25 % where bonds are issued by a credit institution which has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in

---

[ucits_directive, Article 52 to Article 53] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
instruments made with this body carried out in accordance with paragraphs 1 to 4 shall not exceed in total 35 % of the assets of the UCITS. Companies which are included in the same group for the purposes of consolidated accounts, as defined in Directive 83/349/EEC or in accordance with recognised international accounting rules, shall be regarded as a single body for the purpose of calculating the limits contained in this Article. Member States may allow cumulative investment in transferable securities and money market instruments within the same group up to a limit of 20 %. 1. Without prejudice to the limits laid down in Article 56, Member States may raise the limits laid down in Article 52 to a maximum of 20 % for investment in shares or debt securities issued by the same body when, according to the fund rules or instruments of incorporation, the aim of the UCITS’ investment policy is to replicate the composition of a certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it

---

[ucits_directive, Article 51 to Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
the derivative shall be taken into account when complying with the requirements of this Article. 4. Without prejudice to Article 116, the Commission shall adopt, by 1 July 2010, implementing measures specifying the following: (a) criteria for assessing the adequacy of the risk management process employed by the management company in accordance with the first subparagraph of paragraph 1; (b) detailed rules regarding the accurate and independent assessment of the value of OTC derivatives; and (c) detailed rules regarding the content of and procedure to be followed for communicating the information referred to in the third subparagraph of paragraph 1 to the competent authorities of the management company’s home Member State. Those measures, designed to amend non-essential elements of this Directive by supplementing it, shall be adopted in accordance with the regulatory procedure with scrutiny referred to in Article 112(2). 1. A UCITS shall invest no more than: (a) 5 % of its assets in transferable securities or money market instruments issued by the same body; or (b) 20 % of its assets in deposits made with the same body. The risk exposure to a counterparty of the UCITS in an OTC derivative transaction shall not exceed either: (a) 10

---

[ucits_directive, Article 54 to Article 55] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
prominent statement in its prospectus and marketing communications drawing attention to such authorisation and indicating the Member States, local authorities, or public international bodies in the securities of which it intends to invest or has invested more than 35 % of its assets. 1. A UCITS may acquire the units of UCITS or other collective investment undertakings referred to in Article 50(1)(e), provided that no more than 10 % of its assets are invested in units of a single UCITS or other collective investment undertaking. Member States may raise that limit to a maximum of 20 %. 2. Investments made in units of collective investment undertakings other than UCITS shall not exceed, in aggregate, 30 % of the assets of the UCITS. Member States may, where a UCITS has acquired units of another UCITS or collective investme
```
</details>

## q03 (single)
**Question:** What is the limit on a UCITS's risk exposure to a single counterparty in an OTC derivative transaction?
**Reference:** 10% of its assets if the counterparty is a credit institution referred to in Article 50(1)(f); 5% of its assets in other cases.

**Agent answer:**

The risk exposure of a UCITS to a counterparty in an over-the-counter (OTC) derivative transaction shall not exceed:
- **10% of its assets** when the counterparty is a credit institution referred to in Article 50(1)(f) of Directive 2009/65/EC [ucits_directive, Article 52(1)]; or
- **5% of its assets**, in other cases [ucits_directive, Article 52(1)].

**Conditions and Exceptions:**
- When calculating counterparty exposure, management companies shall use the positive mark-to-market value of the OTC derivative contract [organisation, Article 43(2)].
- Management companies may net derivative positions with the same counterparty if they can legally enforce netting agreements on behalf of the UCITS [organisation, Article 43(2)].
- Exposure may be reduced through the receipt of sufficiently liquid collateral, and management companies must take collateral into account when calculating counterparty risk [organisation, Article 43(3) and (4)].

*Note: This answer reflects the indexed versions of Directive 2009/65/EC and Commission Directive 2010/43/EU; later amendments are not included.*

<details><summary>Retrieved passages</summary>

```
[organisation, Article 43] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.78)
is subject to the limits set out in Article 52 of Directive 2009/65/EC. 2. When calculating the UCITS exposure to a counterparty in accordance with the limits as referred to in Article 52(1) of Directive 2009/65/EC, management companies shall use the positive mark-to-market value of the OTC derivative contract with that counterparty. Management companies may net the derivative positions of a UCITS with the same counterparty, provided that they are able to legally enforce netting agreements with the counterparty on behalf of the UCITS. Netting shall only be permissible with respect to OTC derivative instruments with the same counterparty and not in relation to any other exposures the UCITS may have with that same counterparty. 3. Member States may allow management companies to reduce the UCITS exposure to a counterparty of an OTC derivative transaction through the receipt of collateral. Collateral received shall be sufficiently liquid so that it can be sold quickly at a price that is close to its pre-sale valuation. 4. Member States shall require management companies to take collateral into account in calculating exposure to counterparty risk as referred to in Article 52(1) of Directive 2009/65/EC when the management company passes collateral to OTC counterparty on

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.77)
instruments issued by the same body; or (b) 20 % of its assets in deposits made with the same body. The risk exposure to a counterparty of the UCITS in an OTC derivative transaction shall not exceed either: (a) 10 % of its assets when the counterparty is a credit institution referred to in Article 50(1)(f); or (b) 5 % of its assets, in other cases. 2. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 10 %. If they do so, however, the total value of the transferable securities and the money market instruments held by the UCITS in the issuing bodies in each of which it invests more than 5 % of its assets shall not exceed 40 % of the value of its assets. That limitation shall not apply to deposits or OTC derivative transactions made with financial institutions subject to prudential supervision. Notwithstanding the individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or

---

[ucits_directive, Article 51 to Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
the derivative shall be taken into account when complying with the requirements of this Article. 4. Without prejudice to Article 116, the Commission shall adopt, by 1 July 2010, implementing measures specifying the following: (a) criteria for assessing the adequacy of the risk management process employed by the management company in accordance with the first subparagraph of paragraph 1; (b) detailed rules regarding the accurate and independent assessment of the value of OTC derivatives; and (c) detailed rules regarding the content of and procedure to be followed for communicating the information referred to in the third subparagraph of paragraph 1 to the competent authorities of the management company’s home Member State. Those measures, designed to amend non-essential elements of this Directive by supplementing it, shall be adopted in accordance with the regulatory procedure with scrutiny referred to in Article 112(2). 1. A UCITS shall invest no more than: (a) 5 % of its assets in transferable securities or money market instruments issued by the same body; or (b) 20 % of its assets in deposits made with the same body. The risk exposure to a counterparty of the UCITS in an OTC derivative transaction shall not exceed either: (a) 10

---

[organisation, Article 43 to Article 44] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.75)
its pre-sale valuation. 4. Member States shall require management companies to take collateral into account in calculating exposure to counterparty risk as referred to in Article 52(1) of Directive 2009/65/EC when the management company passes collateral to OTC counterparty on behalf of the UCITS. Collateral passed may be taken into account on a net basis only if the management company is able to legally enforce netting arrangements with this counterparty on behalf of the UCITS. 5. Member States shall require management companies to calculate issuer concentration limits as referred to in Article 52 of Directive 2009/65/EC on the basis of the underlying exposure created through the use of financial derivative instruments pursuant to the commitment approach. 6. With respect to the exposure arising from OTC derivatives transactions as referred to in Article 52(2) of Directive 2009/65/EC, Member States shall require management companies to include in the calculation any exposure to OTC derivative counterparty risk. Procedures for the assessment of the value of OTC derivatives 1. Member States shall require management companies to verify that UCITS exposures to OTC derivatives are assigned fair values that do not rely only on market quotations by the counterparties of the OTC transactions and which

---

[ucits_directive, Article 51] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
their contribution to the overall risk profile of the portfolio. It shall employ a process for accurate and independent assessment of the value of OTC derivatives. It shall communicate to the competent authorities of its home Member State regularly in regard to the types of derivative instruments, the underlying risks, the quantitative limits and the methods which are chosen in order to estimate the risks associated with transactions in der
```
</details>

## q04 (single)
**Question:** What issuer limit applies to covered bonds issued by a credit institution subject to special public supervision?
**Reference:** Up to 25% per issuer; if more than 5% is invested in such bonds of one issuer, the total of those investments may not exceed 80% of the UCITS's assets.

**Agent answer:**

The standard issuer limit for transferable securities is 5% of a UCITS' assets, which Member States may raise to a maximum of 25% for bonds issued by a credit institution that has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders [ucits_directive, Article 52(4)]. 

To qualify for this raised limit, the sums deriving from the issue of those bonds must be invested in accordance with the law in assets that cover claims attaching to the bonds during their entire validity and that would be used on a priority basis to reimburse principal and pay accrued interest in the event of the issuer's failure [ucits_directive, Article 52(4)]. Furthermore, where a UCITS invests more than 5% of its assets in such bonds issued by a single issuer, the total value of those investments cannot exceed 80% of the value of the UCITS' assets [ucits_directive, Article 52(4)].

*Note: This answer is based on the indexed texts of Directive 2009/65/EC (UCITS Directive); subsequent amendments are not reflected unless explicitly added.*

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in assets which, during the whole period of validity of the bonds, are capable of covering claims attaching to the bonds and which, in the event of failure of the issuer, would be used on a priority basis for the reimbursement of the principal and payment of the accrued interest. Where a UCITS invests more than 5 % of its assets in the bonds referred to in the first subparagraph which are issued by a single issuer, the total value of these investments shall not exceed 80 % of the value of the assets of the UCITS. Member States shall send to the Commission a list of the categories of bonds referred to in the first subparagraph together with the categories of issuers authorised, in accordance with the laws and supervisory arrangements mentioned in that subparagraph, to issue bonds complying with the criteria set out in this Article. A notice specifying the status of the guarantees offered shall be attached to

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.68)
of issuers authorised, in accordance with the laws and supervisory arrangements mentioned in that subparagraph, to issue bonds complying with the criteria set out in this Article. A notice specifying the status of the guarantees offered shall be attached to those lists. The Commission shall immediately forward that information to the other Member States together with any comments which it considers appropriate and shall make the information available to the public. Such communications may be the subject of exchanges of views within the European Securities Committee referred to in Article 112(1). 5. The transferable securities and money market instruments referred to in paragraphs 3 and 4 shall not be taken into account for the purpose of applying the limit of 40 % referred to in paragraph 2. The limits provided for in paragraphs 1 to 4 shall not be combined, and thus investments in transferable securities or money market instruments issued by the same body or in deposits or derivative instruments made with this body carried out in accordance with paragraphs 1 to 4 shall not exceed in total 35 % of the assets of the UCITS. Companies which are included in the same group for the purposes of consolidated

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.68)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member State, by its local authorities, by a third country or by a public international body to which one or more Member States belong. 4. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 25 % where bonds are issued by a credit institution which has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in

---

[ucits_directive, Recitals] Directive 2009/65/EC (UCITS Directive) (relevance 0.68)
general obligation to act solely in the interests of unit-holders and, in particular, the objective of increasing cost efficiencies, never justify a UCITS undertaking measures that could hinder the competent authorities from effectively exercising their supervisory functions. (49) The original version of Directive 85/611/EEC contained a derogation from the restriction on the percentage of its assets that a UCITS can invest in transferable securities issued by the same body, which applied in the case of bonds issued or guaranteed by a Member State. That derogation allowed UCITS to invest, in particular, up to 35 % of their assets in such bonds. A similar but more limited derogation is justified with regard to private sector bonds which, even in the absence of a State guarantee, offer special guarantees to the investor under the specific rules applicable thereto. It is necessary, therefore, to extend the derogation to the totality of private sector bonds which fulfil jointly fixed criteria, while leaving it to the Member States to draw up the list of bonds to which they intend, where appropriate, to grant a derogation. (50) Several Member States have enacted provisions that enable non-coordinated collective investment undertakings to pool their assets in one so-called

---

[ucits_directive, Article 50] Directive 2009/65/EC (UCITS Directive) (relevance 0.68)
to which one or more Member States belong; (ii) issued by an undertaking any securities of which are dealt in on regulated markets referred to in points (a), (b) or (c); (iii) issued or guaranteed by an establishment subject to prudential supervision, in accordance with criteria defined by Community law, or by an establishment which is subject to and complies with prudential rules considered by the competent authorities to be at least as stringent as those laid down by Community law; or (iv) issued by other bodies belonging to the categories approved by the competent authorities of the UCITS home Member State provided that investments in such instruments are subject to investor protection equivalent to that laid down in points (i), (ii) or (iii)
```
</details>

## q05 (single)
**Question:** How much can a UCITS that replicates a stock index invest in shares of a single issuer?
**Reference:** Up to 20% in shares and/or debt securities of the same body; this can be raised to 35% for a single issuer where justified by exceptional market conditions.

**Agent answer:**

A UCITS that replicates a stock index may invest up to 20% of its assets in shares or debt securities issued by the same body, provided the index is recognized by the competent authorities and meets specific criteria regarding diversification, benchmarking, and publication [ucits_directive, Article 53(1)].

Member States may raise this limit to a maximum of 35% for a single issuer if justified by exceptional market conditions, particularly in regulated markets where certain transferable securities are highly dominant [ucits_directive, Article 53(2)].

Please note that these rules reflect the original 2009 text; later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 52 to Article 53] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
instruments made with this body carried out in accordance with paragraphs 1 to 4 shall not exceed in total 35 % of the assets of the UCITS. Companies which are included in the same group for the purposes of consolidated accounts, as defined in Directive 83/349/EEC or in accordance with recognised international accounting rules, shall be regarded as a single body for the purpose of calculating the limits contained in this Article. Member States may allow cumulative investment in transferable securities and money market instruments within the same group up to a limit of 20 %. 1. Without prejudice to the limits laid down in Article 56, Member States may raise the limits laid down in Article 52 to a maximum of 20 % for investment in shares or debt securities issued by the same body when, according to the fund rules or instruments of incorporation, the aim of the UCITS’ investment policy is to replicate the composition of a certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it

---

[ucits_directive, Article 53 to Article 54] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it is published in an appropriate manner. 2. Member States may raise the limit laid down in paragraph 1 to a maximum of 35 % where that proves to be justified by exceptional market conditions in particular in regulated markets where certain transferable securities or money market instruments are highly dominant. The investment up to that limit shall be permitted only for a single issuer. 1. By way of derogation from Article 52, Member States may authorise UCITS to invest in accordance with the principle of risk-spreading up to 100 % of their assets in different transferable securities and money market instruments issued or guaranteed by a Member State, one or more of its local authorities, a third country, or a public international body to which one or more Member States belong. The competent authorities of the UCITS home Member State shall grant such a derogation only if they consider that unit-holders in the UCITS have protection equivalent to that of

---

[ucits_directive, Recitals] Directive 2009/65/EC (UCITS Directive) (relevance 0.72)
the replication of stock indices or debt-security indices. It is desirable to permit UCITS to replicate well-known and recognised stock indices or debt-security indices. It may therefore be necessary to introduce more flexible risk-spreading rules for UCITS investing in shares or debt securities to this end. (48) Collective investment undertakings falling within the scope of this Directive should not be used for purposes other than the collective investment of the capital raised from the public according to the rules laid down in this Directive. In the cases identified by this Directive, it should be possible for a UCITS to have subsidiaries only when necessary to pursue effectively, on its own behalf, certain activities, also defined in this Directive. It is necessary to ensure effective supervision of UCITS. The establishment of a subsidiary of a UCITS in a third country should therefore be permitted only in the cases identified and in accordance with the conditions laid down in this Directive. The general obligation to act solely in the interests of unit-holders and, in particular, the objective of increasing cost efficiencies, never justify a UCITS undertaking measures that could hinder the competent authorities from effectively exercising their supervisory functions. (49) The original

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.71)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member State, by its local authorities, by a third country or by a public international body to which one or more Member States belong. 4. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 25 % where bonds are issued by a credit institution which has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.71)
instruments issued by the same body; or (b) 20 % of its assets in deposits made with the same body. The risk exposure to a counterparty of the UCITS in an OTC derivative transaction shall not exceed either: (a) 10 % of its assets when the counterparty is a credit institution referred to in Article 50(1)(f); or (b) 5 % of its assets, in other cases. 2. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 10 %. If they do so, however, the total value of the transferable securities and the money market instruments held by the UCITS in the issuing bodies in each of which it invests more than 5 % of its assets shall
```
</details>

## q06 (single)
**Question:** What maximum proportion of the non-voting shares of a single issuing body may a UCITS acquire?
**Reference:** No more than 10% of the non-voting shares of a single issuing body.

**Agent answer:**

A UCITS may acquire no more than 10% of the non-voting shares of a single issuing body [ucits_directive, Article 56(2)]. 

Please note that this answer reflects the indexed provisions of Directive 2009/65/EC (UCITS Directive) and later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 55 to Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.78)
UCITS itself and to the other UCITS or collective investment undertaking in which it invests. 1. An investment company or a management company acting in connection with all of the common funds which it manages and which fall within the scope of this Directive shall not acquire any shares carrying voting rights which would enable it to exercise significant influence over the management of an issuing body. Pending further coordination, Member States shall take account of existing rules defining the principle stated in the first subparagraph in the law of other Member States. 2. A UCITS may acquire no more than: (a) 10 % of the non-voting shares of a single issuing body; (b) 10 % of the debt securities of a single issuing body; (c) 25 % of the units of a single UCITS or other collective investment undertaking within the meaning of Article 1(2)(a) and (b); or (d) 10 % of the money market instruments of a single issuing body. The limits laid down in points (b), (c) and (d) may be disregarded at the time of acquisition if at that time the gross amount of the debt securities or of the money market instruments, or the net

---

[ucits_directive, Article 54 to Article 55] Directive 2009/65/EC (UCITS Directive) (relevance 0.72)
prominent statement in its prospectus and marketing communications drawing attention to such authorisation and indicating the Member States, local authorities, or public international bodies in the securities of which it intends to invest or has invested more than 35 % of its assets. 1. A UCITS may acquire the units of UCITS or other collective investment undertakings referred to in Article 50(1)(e), provided that no more than 10 % of its assets are invested in units of a single UCITS or other collective investment undertaking. Member States may raise that limit to a maximum of 20 %. 2. Investments made in units of collective investment undertakings other than UCITS shall not exceed, in aggregate, 30 % of the assets of the UCITS. Member States may, where a UCITS has acquired units of another UCITS or collective investment undertakings, provide that the assets of the respective UCITS or other collective investment undertakings are not required to be combined for the purposes of the limits laid down in Article 52. 3. Where a UCITS invests in the units of other UCITS or collective investment undertakings that are managed, directly or by delegation, by the same management company or by any other company

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.71)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member State, by its local authorities, by a third country or by a public international body to which one or more Member States belong. 4. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 25 % where bonds are issued by a credit institution which has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in

---

[ucits_directive, Article 52 to Article 53] Directive 2009/65/EC (UCITS Directive) (relevance 0.71)
instruments made with this body carried out in accordance with paragraphs 1 to 4 shall not exceed in total 35 % of the assets of the UCITS. Companies which are included in the same group for the purposes of consolidated accounts, as defined in Directive 83/349/EEC or in accordance with recognised international accounting rules, shall be regarded as a single body for the purpose of calculating the limits contained in this Article. Member States may allow cumulative investment in transferable securities and money market instruments within the same group up to a limit of 20 %. 1. Without prejudice to the limits laid down in Article 56, Member States may raise the limits laid down in Article 52 to a maximum of 20 % for investment in shares or debt securities issued by the same body when, according to the fund rules or instruments of incorporation, the aim of the UCITS’ investment policy is to replicate the composition of a certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.71)
instruments issued by the same body; or (b) 20 % of its assets in deposits made with the same body. The risk exposure to a counterparty of the UCITS in an OTC derivative transaction shall not exceed either: (a) 10 % of its assets when the counterparty is a credit institution referred to in Article 50(1)(f); or (b) 5 % of its assets, in other cases. 2. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 10 %. If they do so, however, the total value of the transferable securities and the money market instruments held by the UCITS in the issuing bodies in each of which it invests more than 5 % of its assets shall not exceed 40 % of the value of its assets. That limitation shall not apply to deposits or OTC derivative transactions made with financial institutions subject to 
```
</details>

## q07 (single)
**Question:** What must a UCITS do if it exceeds its investment limits for reasons beyond its control?
**Reference:** It must adopt as a priority objective for its sales transactions the remedying of that situation, taking due account of the interests of its unit-holders.

**Agent answer:**

If a UCITS exceeds its investment limits for reasons beyond its control, it must adopt as a priority objective for its sales transactions the remedying of that situation, while taking due account of the interests of its unit-holders [ucits_directive, Article 57(2)]. 

Please note that this answer reflects the indexed version of Directive 2009/65/EC (UCITS Directive) only, and later amendments may be relevant.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 57 to Article 58] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
money market instruments which form part of their assets. While ensuring observance of the principle of risk spreading, Member States may allow recently authorised UCITS to derogate from Articles 52 to 55 for six months following the date of their authorisation. 2. If the limits referred to in paragraph 1 are exceeded for reasons beyond the control of a UCITS or as a result of the exercise of subscription rights, that UCITS shall adopt as a priority objective for its sales transactions the remedying of that situation, taking due account of the interests of its unit-holders. 1. A feeder UCITS is a UCITS, or an investment compartment thereof, which has been approved to invest, by way of derogation from Article 1(2)(a), Articles 50, 52 and 55, and Article 56(2)(c), at least 85 % of its assets in units of another UCITS or investment compartment thereof (the master UCITS). 2. A feeder UCITS may hold up to 15 % of its assets in one or more of the following: (a) ancillary liquid assets in accordance with the second subparagraph of Article 50(2); (b) financial derivative instruments, which may be used only for hedging purposes, in accordance with Article 50(1)(g) and Article

---

[ucits_directive, Article 56 to Article 57] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
holding represents the only way in which the UCITS can invest in the securities of issuing bodies of that country; or (e) shares held by an investment company or investment companies in the capital of subsidiary companies pursuing only the business of management, advice or marketing in the country where the subsidiary is established, in regard to the repurchase of units at unit-holders’ request exclusively on its or their behalf. The derogation referred to in point (d) of the first subparagraph of this paragraph shall apply only if in its investment policy the company from the third country complies with the limits laid down in Articles 52 and 55 and in paragraphs 1 and 2 of this Article. Where the limits set in Articles 52 and 55 are exceeded, Article 57 shall apply mutatis mutandis . 1. UCITS are not required to comply with the limits laid down in this Chapter when exercising subscription rights attaching to transferable securities or money market instruments which form part of their assets. While ensuring observance of the principle of risk spreading, Member States may allow recently authorised UCITS to derogate from Articles 52 to 55 for six months following the date of their

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member State, by its local authorities, by a third country or by a public international body to which one or more Member States belong. 4. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 25 % where bonds are issued by a credit institution which has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in

---

[ucits_directive, Article 54 to Article 55] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
prominent statement in its prospectus and marketing communications drawing attention to such authorisation and indicating the Member States, local authorities, or public international bodies in the securities of which it intends to invest or has invested more than 35 % of its assets. 1. A UCITS may acquire the units of UCITS or other collective investment undertakings referred to in Article 50(1)(e), provided that no more than 10 % of its assets are invested in units of a single UCITS or other collective investment undertaking. Member States may raise that limit to a maximum of 20 %. 2. Investments made in units of collective investment undertakings other than UCITS shall not exceed, in aggregate, 30 % of the assets of the UCITS. Member States may, where a UCITS has acquired units of another UCITS or collective investment undertakings, provide that the assets of the respective UCITS or other collective investment undertakings are not required to be combined for the purposes of the limits laid down in Article 52. 3. Where a UCITS invests in the units of other UCITS or collective investment undertakings that are managed, directly or by delegation, by the same management company or by any other company

---

[ucits_directive, Article 53 to Article 54] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it is published in an appropriate manner. 2. Member States may raise the limit laid down in paragraph 1 to a maximum of 35 % where that proves to be justified by exceptional market conditions in particular in regulated markets where certain transferable securities or money market instruments are highly dominant. The investment up to that limit shall be permitted only for a single issuer. 1. By way of derogation from Article 52, Member States may authorise UCITS to invest in accordance with the prin
```
</details>

## q08 (single)
**Question:** What minimum share of its assets must a feeder UCITS invest in its master UCITS?
**Reference:** At least 85% of its assets in units of the master UCITS.

**Agent answer:**

A feeder UCITS must invest at least 85% of its assets in units of another master UCITS [ucits_directive, Article 57(1)]. 

Additionally, a feeder UCITS may hold up to 15% of its assets in ancillary liquid assets, financial derivative instruments used solely for hedging purposes, and (if it is an investment company) movable and immovable property essential for the direct pursuit of its business [ucits_directive, Article 58(2)]. It must also disclose in any relevant marketing communications that it permanently invests 85% or more of its assets in the master UCITS [ucits_directive, Article 63(4)].

Please note that this answer reflects the indexed version of Directive 2009/65/EC (UCITS Directive) and later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 58 to Article 59] Directive 2009/65/EC (UCITS Directive) (relevance 0.78)
A master UCITS is a UCITS, or an investment compartment thereof, which: (a) has, among its unit-holders, at least one feeder UCITS; (b) is not itself a feeder UCITS; and (c) does not hold units of a feeder UCITS. 4. The following derogations for a master UCITS shall apply: (a) if a master UCITS has at least two feeder UCITS as unit-holders, Article 1(2)(a) and Article 3(b) shall not apply, giving the master UCITS the choice whether or not to raise capital from other investors; (b) If a master UCITS does not raise capital from the public in a Member State other than that in which it is established, but only has one or more feeder UCITS in that Member State, Chapter XI and the second subparagraph of Article 108(1) shall not apply. 1. Member States shall ensure that the investment of a feeder UCITS into a given master UCITS which exceeds the limit applicable under Article 55(1) for investments into other UCITS be subject to prior approval by the competent authorities of the feeder UCITS home Member State. 2. The feeder UCITS shall be informed within 15 working days following the submission of a complete file, whether or not

---

[ucits_directive, Article 58] Directive 2009/65/EC (UCITS Directive) (relevance 0.78)
assets in one or more of the following: (a) ancillary liquid assets in accordance with the second subparagraph of Article 50(2); (b) financial derivative instruments, which may be used only for hedging purposes, in accordance with Article 50(1)(g) and Article 51(2) and (3); (c) movable and immovable property which is essential for the direct pursuit of the business, if the feeder UCITS is an investment company. For the purposes of compliance with Article 51(3), the feeder UCITS shall calculate its global exposure related to financial derivative instruments by combining its own direct exposure under point (b) of the first subparagraph with either: (a) the master UCITS’ actual exposure to financial derivative instruments in proportion to the feeder UCITS’ investment into the master UCITS; or (b) the master UCITS’ potential maximum global exposure to financial derivative instruments provided for in the master UCITS’ fund rules or instruments of incorporation in proportion to the feeder UCITS investment into the master UCITS. 3. A master UCITS is a UCITS, or an investment compartment thereof, which: (a) has, among its unit-holders, at least one feeder UCITS; (b) is not itself a feeder UCITS; and (c) does not hold units of a feeder UCITS. 4.

---

[ucits_directive, Article 63 to Article 64] Directive 2009/65/EC (UCITS Directive) (relevance 0.77)
report of the master UCITS can be obtained. 3. In addition to the requirements laid down in Articles 74 and 82, the feeder UCITS shall send the prospectus, the key investor information referred to in Article 78 and any amendment thereto, as well as the annual and half-yearly reports of the master UCITS, to the competent authorities of its home Member State. 4. A feeder UCITS shall disclose in any relevant marketing communications that it permanently invests 85 % or more of its assets in units of such master UCITS. 5. A paper copy of the prospectus, and the annual and half-yearly reports of the master UCITS shall be delivered by the feeder UCITS to investors on request and free of charge. 1. Member States shall require that a feeder UCITS which already pursues activities as a UCITS, including those of a feeder UCITS of a different master UCITS, shall provide the following information to its unit-holders: (a) a statement that the competent authorities of the feeder UCITS home Member State approved the investment of the feeder UCITS in units of such master UCITS; (b) the key investor information referred to in Article 78 concerning the feeder and the master

---

[ucits_directive, Article 57 to Article 58] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
money market instruments which form part of their assets. While ensuring observance of the principle of risk spreading, Member States may allow recently authorised UCITS to derogate from Articles 52 to 55 for six months following the date of their authorisation. 2. If the limits referred to in paragraph 1 are exceeded for reasons beyond the control of a UCITS or as a result of the exercise of subscription rights, that UCITS shall adopt as a priority objective for its sales transactions the remedying of that situation, taking due account of the interests of its unit-holders. 1. A feeder UCITS is a UCITS, or an investment compartment thereof, which has been approved to invest, by way of derogation from Article 1(2)(a), Articles 50, 52 and 55, and Article 56(2)(c), at least 85 % of its assets in units of another UCITS or investment compartment thereof (the master UCITS). 2. A feeder UCITS may hold up to 15 % of its assets in one or more of the following: (a) ancillary liquid assets in accordance with the second subparagraph of Article 50(2); (b) financial derivative instruments, which may be used only for hedging purposes, in accordance with Article 50(1)(g) and Article

---

[ucits_directive, Article 65 to Article 67] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
be paid into the assets of the feeder UCITS. 1. The master UCITS shall immediately inform the competent authorities of its home Member State of the identity of each feeder UCITS which invests in its units. If the master UCITS and the feeder UCITS are established in different Member States, the competent authorities of the master UCITS home Member State shall immediately inform those of the feeder UCITS home Member State of such investment. 2. The master UCITS shall not charge subscription or redemption fees for the investment of the feeder UCITS into its units or the divestment thereof. 3. The master UCITS shall ensure the timely availability of all information that is required in accordance with this Directive, other Communi
```
</details>

## q09 (single)
**Question:** Is a UCITS allowed to borrow money?
**Reference:** In principle no. Member States may allow temporary borrowing of up to 10% of assets, and foreign currency may be acquired through a back-to-back loan.

**Agent answer:**

As a general rule under EU UCITS rules, an investment company, or a management company or depositary acting on behalf of a common fund, is not allowed to borrow money, though a UCITS may acquire foreign currency by means of a "back-to-back" loan [ucits_directive, Article 82(1)]. 

However, by way of derogation, a Member State may authorise a UCITS to borrow provided that the borrowing is:
1. On a temporary basis and represents no more than 10% of its assets (for an investment company) or no more than 10% of the value of the fund (for a common fund) [ucits_directive, Article 82(2)(a)]; or
2. To enable the acquisition of immovable property essential for the direct pursuit of its business and represents no more than 10% of its assets (for an investment company) [ucits_directive, Article 82(2)(b)].

Where a UCITS is authorized to borrow under both points, total borrowings shall not exceed 15% of its assets [ucits_directive, Article 82(2)]. 

*Note: This answer reflects the indexed texts of Directive 2009/65/EC (UCITS Directive); later amendments (such as UCITS V) may apply.*

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 82 to Article 84] Directive 2009/65/EC (UCITS Directive) (relevance 0.77)
up to date. 1. The following shall not borrow: (a) an investment company; (b) a management company or depositary acting on behalf of a common fund. A UCITS may, however, acquire foreign currency by means of a ‘back-to-back’ loan. 2. By way of derogation from paragraph 1, a Member State may authorise a UCITS to borrow provided that such borrowing is: (a) on a temporary basis and represents: — in the case of an investment company, no more than 10 % of its assets, or — in the case of a common fund, no more than 10 % of the value of the fund; or (b) to enable the acquisition of immovable property essential for the direct pursuit of its business and represents, in the case of an investment company, no more than 10 % of its assets. Where a UCITS is authorised to borrow under points (a) and (b), such borrowing shall not exceed 15 % of its assets in total. 1. A UCITS shall repurchase or redeem its units at the request of any unit-holder. 2. By way of derogation from paragraph 1: (a) a UCITS may, in accordance with the applicable national law, the fund rules or

---

[ucits_directive, Article 57 to Article 58] Directive 2009/65/EC (UCITS Directive) (relevance 0.71)
money market instruments which form part of their assets. While ensuring observance of the principle of risk spreading, Member States may allow recently authorised UCITS to derogate from Articles 52 to 55 for six months following the date of their authorisation. 2. If the limits referred to in paragraph 1 are exceeded for reasons beyond the control of a UCITS or as a result of the exercise of subscription rights, that UCITS shall adopt as a priority objective for its sales transactions the remedying of that situation, taking due account of the interests of its unit-holders. 1. A feeder UCITS is a UCITS, or an investment compartment thereof, which has been approved to invest, by way of derogation from Article 1(2)(a), Articles 50, 52 and 55, and Article 56(2)(c), at least 85 % of its assets in units of another UCITS or investment compartment thereof (the master UCITS). 2. A feeder UCITS may hold up to 15 % of its assets in one or more of the following: (a) ancillary liquid assets in accordance with the second subparagraph of Article 50(2); (b) financial derivative instruments, which may be used only for hedging purposes, in accordance with Article 50(1)(g) and Article

---

[ucits_directive, Article 83 to Article 85] Directive 2009/65/EC (UCITS Directive) (relevance 0.71)
in total. 1. A UCITS shall repurchase or redeem its units at the request of any unit-holder. 2. By way of derogation from paragraph 1: (a) a UCITS may, in accordance with the applicable national law, the fund rules or the instruments of incorporation of the investment company, temporarily suspend the repurchase or redemption of its units; (b) a UCITS home Member State may allow its competent authorities to require the suspension of the repurchase or redemption of units in the interest of the unit-holders or of the public. The temporary suspension referred to in point (a) of the first subparagraph shall be provided for only in exceptional cases where circumstances so require and where suspension is justified having regard to the interests of the unit-holders. 3. In the event of a temporary suspension under paragraph 2(a), a UCITS shall, without delay, communicate its decision to its home Member State competent authorities and to the competent authorities of all Member States in which it markets its units. The rules for the valuation of assets and the rules for calculating the sale or issue price and the repurchase or redemption price of the units of a UCITS shall be laid down

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.70)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member State, by its local authorities, by a third country or by a public international body to which one or more Member States belong. 4. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 25 % where bonds are issued by a credit institution which has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in

---

[ucits_directive, Article 81 to Article 83] Directive 2009/65/EC (UCITS Directive) (relevance 0.70)
management companies, to provide key investor information in a durable medium or by means of a website. A paper copy shall be delivered to the investor on request and free of charge. In addition, an up-to-date version of the key investor information shall be made available on the website of the investment company or management company. 2. The Commission may adopt implementing measures which define the specific conditions which need to be met when providing key investor information in a durable medium other than on paper or by means of a website which does not constitute a durable medium. Those measures, designed to amend non-essential elements of this Directive by supplementing it, shall be adopted in accordance with the regulatory procedure with scrutiny referred to in Article 112(2). 1. UCITS shall send their key investor information and any amendments thereto, to the competent authorities of th
```
</details>

## q10 (single)
**Question:** Must a UCITS redeem its units whenever a unit-holder asks?
**Reference:** Yes, it must repurchase or redeem units at the request of any unit-holder; repurchase may only be suspended temporarily in exceptional cases provided for by law or the fund rules.

**Agent answer:**

Yes, a UCITS shall repurchase or redeem its units at the request of any unit-holder [ucits_directive, Article 84(1)]. 

**Exceptions:**
* A UCITS may temporarily suspend the repurchase or redemption of its units in accordance with applicable national law, the fund rules, or the instruments of incorporation, provided it is done only in exceptional cases where circumstances so require and where suspension is justified in the interests of the unit-holders [ucits_directive, Article 84(2)].
* A UCITS home Member State may allow its competent authorities to require the suspension of the repurchase or redemption of units in the interest of the unit-holders or of the public [ucits_directive, Article 84(2)].
* Actions taken by a UCITS to ensure that the stock exchange value of its units does not significantly vary from their net asset value shall be regarded as equivalent to repurchase or redemption [ucits_directive, Article 1(2)].

*Note: This answer reflects Directive 2009/65/EC (UCITS Directive) as indexed in the corpus; later amendments or national transposition rules may introduce further specifications.*

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 83 to Article 85] Directive 2009/65/EC (UCITS Directive) (relevance 0.80)
in total. 1. A UCITS shall repurchase or redeem its units at the request of any unit-holder. 2. By way of derogation from paragraph 1: (a) a UCITS may, in accordance with the applicable national law, the fund rules or the instruments of incorporation of the investment company, temporarily suspend the repurchase or redemption of its units; (b) a UCITS home Member State may allow its competent authorities to require the suspension of the repurchase or redemption of units in the interest of the unit-holders or of the public. The temporary suspension referred to in point (a) of the first subparagraph shall be provided for only in exceptional cases where circumstances so require and where suspension is justified having regard to the interests of the unit-holders. 3. In the event of a temporary suspension under paragraph 2(a), a UCITS shall, without delay, communicate its decision to its home Member State competent authorities and to the competent authorities of all Member States in which it markets its units. The rules for the valuation of assets and the rules for calculating the sale or issue price and the repurchase or redemption price of the units of a UCITS shall be laid down

---

[ucits_directive, Article 82 to Article 84] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
up to date. 1. The following shall not borrow: (a) an investment company; (b) a management company or depositary acting on behalf of a common fund. A UCITS may, however, acquire foreign currency by means of a ‘back-to-back’ loan. 2. By way of derogation from paragraph 1, a Member State may authorise a UCITS to borrow provided that such borrowing is: (a) on a temporary basis and represents: — in the case of an investment company, no more than 10 % of its assets, or — in the case of a common fund, no more than 10 % of the value of the fund; or (b) to enable the acquisition of immovable property essential for the direct pursuit of its business and represents, in the case of an investment company, no more than 10 % of its assets. Where a UCITS is authorised to borrow under points (a) and (b), such borrowing shall not exceed 15 % of its assets in total. 1. A UCITS shall repurchase or redeem its units at the request of any unit-holder. 2. By way of derogation from paragraph 1: (a) a UCITS may, in accordance with the applicable national law, the fund rules or

---

[ucits_directive, Article 1] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
by a UCITS to ensure that the stock exchange value of its units does not significantly vary from their net asset value shall be regarded as equivalent to such repurchase or redemption. Member States may allow UCITS to consist of several investment compartments. 3. The undertakings referred to in paragraph 2 may be constituted in accordance with contract law (as common funds managed by management companies), trust law (as unit trusts), or statute (as investment companies). For the purposes of this Directive: (a) ‘common funds’ shall also include unit trusts; (b) ‘units’ of UCITS shall also include shares of UCITS. 4. Investment companies, the assets of which are invested through the intermediary of subsidiary companies, mainly other than in transferable securities, shall not be subject to this Directive. 5. The Member States shall prohibit UCITS which are subject to this Directive from transforming themselves into collective investment undertakings which are not covered by this Directive. 6. Subject to the provisions in Community law governing capital movements and subject to Articles 91 and 92 and the second subparagraph of Article 108(1), no Member State shall apply any other provisions in the field covered by this Directive to UCITS established in another

---

[ucits_directive, Annex I] Directive 2009/65/EC (UCITS Directive) (relevance 0.72)
units: registered or bearer. Indication of any denominations which may be provided for, — indication of unit-holders' voting rights, — circumstances in which winding-up of the investment company can be decided on and winding-up procedure, in particular as regards the rights of unit-holders. 1.11. Where applicable, indication of stock exchanges or markets where the units are listed or dealt in. 1.11. Where applicable, indication of stock exchanges or markets where the units are listed or dealt in. 1.12. Procedures and conditions of issue and sale of units. 1.12. Procedures and conditions of issue and sale of units. 1.13. Procedures and conditions for repurchase or redemption of units, and circumstances in which repurchase or redemption may be suspended. 1.13. Procedures and conditions for repurchase or redemption of units, and circumstances in which repurchase or redemption may be suspended. In the case of investment companies having different investment compartments, information on how a unit-holder may pass from one compartment into another and the charges applicable in such cases. 1.14. Description of rules for determining and applying income. 1.14. Description of rules for determining and applying income. 1.15. Description of the common fund's investment objectives, including its financial objectives (e.g. capital growth or

---

[ucits_directive, Article 60] Directive 2009/65/EC (UCITS Directive) (relevance 0.72)
and publication in order to avoid market timing in their units, preventing arbitrage opportunities. 3. Without prejudice to Article 84, if a master UCITS temporarily suspends the repurchase, redemption or subscription of its units, whether at its own initiative or at the request of its competent authorities, each of its feeder UCITS is entitled to suspend the repurchase, redemption or subscription of its units notwithstanding the conditions laid down in Article 84(2) within the same period of time as the master UCITS. 4. If a master UCITS is liquidated, the feeder UCITS shall also be liquidated, unless the competent authorit
```
</details>

## q11 (single)
**Question:** Can a UCITS or its management company carry out uncovered (short) sales of transferable securities?
**Reference:** No. Uncovered sales of transferable securities, money market instruments or other financial instruments are not allowed.

**Agent answer:**

No, an investment company, or a management company or depositary acting on behalf of a common fund, shall not carry out uncovered sales of transferable securities, money market instruments, or other financial instruments referred to in points (e), (g), and (h) of Article 50(1) [ucits_directive, Article 88(1)]. 

However, this prohibition does not prevent these entities from acquiring transferable securities, money market instruments, or other financial instruments that are not fully paid [ucits_directive, Article 88(2)].

*Note: This answer reflects the indexed text of Directive 2009/65/EC (UCITS Directive) and subsequent amendments may apply.*

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 88 to Article 91] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
a management company or depositary acting on behalf of a common fund. 2. Paragraph 1 shall not prevent the undertakings referred to therein from acquiring transferable securities, money market instruments or other financial instruments referred to in points (e), (g) and (h) of Article 50(1) which are not fully paid. The following shall not carry out uncovered sales of transferable securities, money market instruments or other financial instruments referred to in points (e), (g) and (h) of Article 50(1): (a) an investment company; (b) a management company or depositary acting on behalf of a common fund. The law of the UCITS home Member State or the fund rules shall prescribe the remuneration and the expenditure which a management company is empowered to charge to a common fund and the method of calculation of such remuneration. The law or the instruments of incorporation of an investment company shall prescribe the nature of the cost to be borne by the company. SPECIAL PROVISIONS APPLICABLE TO UCITS WHICH MARKET THEIR UNITS IN MEMBER STATES OTHER THAN THOSE IN WHICH THEY ARE ESTABLISHED 1. UCITS host Member States shall ensure that UCITS are able to market their units within their territories upon notification in

---

[ucits_directive, Article 2 to Article 5] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
purposes of paragraph 1(l), Articles 13 to 16 of Directive 2006/49/EC shall apply mutatis mutandis . 7. For the purposes of paragraph 1(n), transferable securities shall exclude the techniques and instruments referred to in Article 51. The following undertakings are not subject to this Directive: (a) collective investment undertakings of the closed-ended type; (b) collective investment undertakings which raise capital without promoting the sale of their units to the public within the Community or any part of it; (c) collective investment undertakings the units of which, under the fund rules or the instruments of incorporation of the investment company, may be sold only to the public in third countries; (d) categories of collective investment undertakings prescribed by the regulations of the Member States in which such collective investment undertakings are established, for which the rules laid down in Chapter VII and Article 83 are inappropriate in view of their investment and borrowing policies. For the purposes of this Directive, a UCITS shall be deemed to be established in its home Member State. 1. No UCITS shall pursue activities as such unless it has been authorised in accordance with this Directive. Such authorisation shall be valid for all Member States. 2.

---

[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.72)
Directive 85/611/EEC to transferable securities shall be understood as a reference to financial instruments which fulfil the following criteria: (a) the potential loss which the UCITS may incur with respect to holding those instruments is limited to the amount paid for them; (b) their liquidity does not compromise the ability of the UCITS to comply with Article 37 of Directive 85/611/EEC; (c) reliable valuation is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1) of Directive 85/611/EEC, in the form of accurate, reliable and regular prices which are either market prices or prices made available by valuation systems independent from issuers; (ii) in the case of other securities as referred to in Article 19(2) of Directive 85/611/EEC, in the form of a valuation on a periodic basis which is derived from information from the issuer of the security or from competent investment research; (d) appropriate information is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1)

---

[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.71)
there is information available to the UCITS that would lead to a different determination, financial instruments which are admitted or dealt in on a regulated market in accordance with points (a), (b) or (c) of Article 19(1) of Directive 85/611/EEC shall be presumed not to compromise the ability of the UCITS to comply with Article 37 of Directive 85/611/EEC and shall also be presumed to be negotiable. 2. Transferable securities as referred to in Article 1(8) of Directive 85/611/EEC shall be taken to include the following: (a) units in closed end funds constituted as investment companies or as unit trusts which fulfil the following criteria: (i) they fulfil the criteria set out in paragraph 1; (ii) they are subject to corporate governance mechanisms applied to companies; (iii) where asset management activity is carried out by another entity on behalf of the closed end fund, that entity is subject to national regulation for the purpose of investor protection; (b) units in closed end funds constituted under the law of contract which fulfil the following criteria: (i) they fulfil the criteria set out in paragraph 1; (ii) they are subject to corporate governance mechanisms equivalent to those applied to companies as referred

---

[ucits_directive, Article 50] Directive 2009/65/EC (UCITS Directive) (relevance 0.71)
rules or the instruments of incorporation of the investment company; (d) recently issued transferable securities, provided that: (i) the terms of issue include an undertaking that an application will be made for admission to official listing on a stock exchange or to another regulated market which operates regularly and is recognised and open to the public, provided that the choice of stock exchange or market has been approved by the competent authorities or is provided for in law or the fund rules or the instruments of incorporation of the i
```
</details>

## q12 (single)
**Question:** What is the minimum initial capital of a UCITS management company?
**Reference:** At least EUR 125 000, plus 0.02% of the amount by which the portfolios it manages exceed EUR 250 million, with the total capped at EUR 10 million.

**Agent answer:**

A UCITS management company must have an initial capital of at least EUR 125 000 [ucits_directive, Article 6 to Article 7]. 

When the value of the portfolios managed exceeds EUR 250 000 000, the company is required to provide an additional amount of own funds equal to 0,02% of the amount exceeding EUR 250 000 000, provided that the total of the initial capital and the additional amount does not exceed EUR 10 000 000 [ucits_directive, Article 6 to Article 7]. Additionally, the own funds of the management company must at no time be less than the amount prescribed in Article 21 of Directive 2006/49/EC [ucits_directive, Article 7].

Please note that this answer reflects the indexed texts (Directive 2009/65/EC) and later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 7] Directive 2009/65/EC (UCITS Directive) (relevance 0.78)
the initial capital and the additional amount must not, however, exceed EUR 10 000 000; (ii) for the purposes of this paragraph, the following portfolios must be deemed to be the portfolios of the management company: — common funds managed by the management company including portfolios for which it has delegated the management function but excluding portfolios that it is managing under delegation, — investment companies for which the management company is the designated management company, — other collective investment undertakings managed by the management company including portfolios for which it has delegated the management function but excluding portfolios that it is managing under delegation; (iii) irrespective of the amount of those requirements, the own funds of the management company must at no time be less than the amount prescribed in Article 21 of Directive 2006/49/EC; (b) the persons who effectively conduct the business of a management company are of sufficiently good repute and are sufficiently experienced also in relation to the type of UCITS managed by the management company, the names of those persons and of every person succeeding them in office being communicated forthwith to the competent authorities and the conduct of the business of a management company

---

[ucits_directive, Article 6 to Article 7] Directive 2009/65/EC (UCITS Directive) (relevance 0.77)
to provide non-core services without being authorised for the services referred to in point (a) of the first subparagraph. 4. Article 2(2) and Articles 12, 13 and 19 of Directive 2004/39/EC shall apply to the provision of the services referred to in paragraph 3 of this Article by management companies. 1. Without prejudice to other conditions of general application laid down by national law, the competent authorities shall not grant authorisation to a management company unless the following conditions are met: (a) the management company has an initial capital of at least EUR 125 000, taking into account the following: (i) when the value of the portfolios of the management company exceeds EUR 250 000 000, the management company must be required to provide an additional amount of own funds which is equal to 0,02 % of the amount by which the value of the portfolios of the management company exceeds EUR 250 000 000 but the required total of the initial capital and the additional amount must not, however, exceed EUR 10 000 000; (ii) for the purposes of this paragraph, the following portfolios must be deemed to be the portfolios of the management company: — common funds managed

---

[ucits_directive, Article 27 to Article 29] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
subject to prior authorisation to be granted by the competent authorities of the investment company’s home Member State. Member States shall determine the legal form which an investment company must take. The registered office of the investment company shall be situated in the investment company’s home Member State. No investment company may engage in activities other than those referred to in Article 1(2). 1. Without prejudice to other conditions of general application laid down by national law, the competent authorities of the investment company’s home Member State shall not grant authorisation to an investment company that has not designated a management company unless the investment company has a sufficient initial capital of at least EUR 300 000. In addition, when an investment company has not designated a management company authorised pursuant to this Directive, the following conditions shall apply: (a) the authorisation must not be granted unless the application for authorisation is accompanied by a programme of operations setting out, at least, the organisational structure of the investment company; (b) the directors of the investment company must be of sufficiently good repute and be sufficiently experienced also in relation to the type of business pursued by the investment company and,

---

[ucits_directive, Article 7] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
to the type of UCITS managed by the management company, the names of those persons and of every person succeeding them in office being communicated forthwith to the competent authorities and the conduct of the business of a management company being decided by at least two persons meeting such conditions; (c) the application for authorisation is accompanied by a programme of activity setting out, at least, the organisational structure of the management company; and (d) the head office and the registered office of the management company are located in the same Member State. For the purposes of point (a) of the first subparagraph, Member States may authorise management companies not to provide up to 50 % of the additional amount of own funds referred to in point (i) of point (a) if they benefit from a guarantee of the same amount given by a credit institution or an insurance undertaking which has its registered office in a Member State, or in a third country where it is subject to prudential rules considered by the competent authorities as equivalent to those laid down in Community law. 2. Where close links exist between the management company and other natural or legal persons,

---

[ucits_directive, Recitals] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
application of the principle of home Member State supervision. (9) In order to ensure that the management company will be able to fulfil the obligations arising from its activities and thus to ensure its stability, initial capital and an additional amount of own funds are required. To take account of developments, particularly those pertaining to capital charges on operational risk, within the Community and other international forums, those requirements, including the use of guarantees, should be reviewed. (10) It is nece
```
</details>

## q13 (single)
**Question:** Can a UCITS invest in gold or other precious metals?
**Reference:** No. A UCITS may not acquire precious metals or certificates representing them.

**Agent answer:**

I don't know. The indexed documents do not cover all details on precious metals, but they explicitly state: "A UCITS shall not, however: ... acquire either precious metals or certificates representing them" [ucits_directive, Article 50(2)]. 

*Note: This answer reflects the indexed texts (Directive 2009/65/EC).*

<details><summary>Retrieved passages</summary>

```
[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.73)
or from competent investment research; (d) appropriate information is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1) of Directive 85/611/EEC, in the form of regular, accurate and comprehensive information to the market on the security or, where relevant, on the portfolio of the security; (ii) in the case of other securities as referred to in Article 19(2) of Directive 85/611/EEC, in the form of regular and accurate information to the UCITS on the security or, where relevant, on the portfolio of the security; (e) they are negotiable; (f) their acquisition is consistent with the investment objectives or the investment policy, or both, of the UCITS pursuant to Directive 85/611/EEC; (g) their risks are adequately captured by the risk management process of the UCITS. For the purposes of points (b) and (e) of the first subparagraph, and unless there is information available to the UCITS that would lead to a different determination, financial instruments which are admitted or dealt in on a regulated market in accordance with points (a), (b) or (c) of Article 19(1) of Directive 85/611/EEC

---

[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.72)
Directive 85/611/EEC to transferable securities shall be understood as a reference to financial instruments which fulfil the following criteria: (a) the potential loss which the UCITS may incur with respect to holding those instruments is limited to the amount paid for them; (b) their liquidity does not compromise the ability of the UCITS to comply with Article 37 of Directive 85/611/EEC; (c) reliable valuation is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1) of Directive 85/611/EEC, in the form of accurate, reliable and regular prices which are either market prices or prices made available by valuation systems independent from issuers; (ii) in the case of other securities as referred to in Article 19(2) of Directive 85/611/EEC, in the form of a valuation on a periodic basis which is derived from information from the issuer of the security or from competent investment research; (d) appropriate information is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1)

---

[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.71)
there is information available to the UCITS that would lead to a different determination, financial instruments which are admitted or dealt in on a regulated market in accordance with points (a), (b) or (c) of Article 19(1) of Directive 85/611/EEC shall be presumed not to compromise the ability of the UCITS to comply with Article 37 of Directive 85/611/EEC and shall also be presumed to be negotiable. 2. Transferable securities as referred to in Article 1(8) of Directive 85/611/EEC shall be taken to include the following: (a) units in closed end funds constituted as investment companies or as unit trusts which fulfil the following criteria: (i) they fulfil the criteria set out in paragraph 1; (ii) they are subject to corporate governance mechanisms applied to companies; (iii) where asset management activity is carried out by another entity on behalf of the closed end fund, that entity is subject to national regulation for the purpose of investor protection; (b) units in closed end funds constituted under the law of contract which fulfil the following criteria: (i) they fulfil the criteria set out in paragraph 1; (ii) they are subject to corporate governance mechanisms equivalent to those applied to companies as referred

---

[eligible_assets, Article 8 to Article 9] Commission Directive 2007/16/EC (eligible assets) (relevance 0.71)
to a valuation, by the UCITS, corresponding to the fair value as referred to in paragraph 3 of this Article, which does not rely only on market quotations by the counterparty and which fulfils the following criteria: (a) the basis for the valuation is either a reliable up-to-date market value of the instrument, or, if such a value is not available, a pricing model using an adequate recognised methodology; (b) verification of the valuation is carried out by one of the following: (i) an appropriate third party which is independent from the counterparty of the OTC-derivative, at an adequate frequency and in such a way that the UCITS is able to check it; (ii) a unit within the UCITS which is independent from the department in charge of managing the assets and which is adequately equipped for such purpose. 5. The reference in Articles 1(2) and 19(1)(g) of Directive 85/611/EEC to liquid financial assets shall be understood as excluding derivatives on commodities. Article 19(1)(g) of Directive 85/611/EEC Financial indices 1. The reference in point (g) of Article 19(1) of Directive 85/611/EEC to financial indices shall be understood as a reference to indices which fulfil the following criteria: (a) they are

---

[eligible_assets, Recitals] Commission Directive 2007/16/EC (eligible assets) (relevance 0.71)
20.3.2007 EN Official Journal of the European Union L 79/11 COMMISSION DIRECTIVE 2007/16/EC of 19 March 2007 implementing Council Directive 85/611/EEC on the coordination of laws, regulations and administrative provisions relating to undertakings for collective investment in transferable securities (UCITS) as regards the clarification of certain definitions (Text with EEA relevance) THE COMMISSION OF THE EUROPEAN COMMUNITIES, Having regard to the Treaty establishing the European Community, Having regard to Council Directive 85/611/EEC of 20 December 1985 on the coordination of laws, regulations and administrativ
```
</details>

## q14 (single)
**Question:** What is the cap on a UCITS's global exposure relating to derivative instruments?
**Reference:** Its global exposure relating to derivatives must not exceed the total net value of its portfolio.

**Agent answer:**

A UCITS must ensure that its global exposure relating to derivative instruments does not exceed the total net value of its portfolio [ucits_directive, Article 51(3)].

This exposure is calculated by taking into account the current value of the underlying assets, the counterparty risk, future market movements, and the time available to liquidate the positions [ucits_directive, Article 51(3)]. When transferable securities or money market instruments embed a derivative, that derivative must also be taken into account [ucits_directive, Article 51(3)].

Please note that these rules are based on the original 2009-2010 texts; later amendments or national regulations may apply.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 51] Directive 2009/65/EC (UCITS Directive) (relevance 0.80)
down in the UCITS’ fund rules, instruments of incorporation or prospectus. 3. A UCITS shall ensure that its global exposure relating to derivative instruments does not exceed the total net value of its portfolio. The exposure is calculated taking into account the current value of the underlying assets, the counterparty risk, future market movements and the time available to liquidate the positions. This shall also apply to the third and fourth subparagraphs. A UCITS may invest, as a part of its investment policy and within the limit laid down in Article 52(5), in financial derivative instruments provided that the exposure to the underlying assets does not exceed in aggregate the investment limits laid down in Article 52. Member States may provide that, when a UCITS invests in index-based financial derivative instruments, those investments are not required to be combined for the purposes of the limits laid down in Article 52. When transferable securities or money market instruments embed a derivative, the derivative shall be taken into account when complying with the requirements of this Article. 4. Without prejudice to Article 116, the Commission shall adopt, by 1 July 2010, implementing measures specifying the following: (a) criteria for assessing the adequacy

---

[ucits_directive, Article 51] Directive 2009/65/EC (UCITS Directive) (relevance 0.78)
their contribution to the overall risk profile of the portfolio. It shall employ a process for accurate and independent assessment of the value of OTC derivatives. It shall communicate to the competent authorities of its home Member State regularly in regard to the types of derivative instruments, the underlying risks, the quantitative limits and the methods which are chosen in order to estimate the risks associated with transactions in derivative instruments regarding each managed UCITS. 2. Member States may authorise UCITS to employ techniques and instruments relating to transferable securities and money market instruments under the conditions and within the limits which they lay down provided that such techniques and instruments are used for the purpose of efficient portfolio management. When those operations concern the use of derivative instruments, the conditions and limits shall conform to the provisions laid down in this Directive. Under no circumstances shall those operations cause the UCITS to diverge from its investment objectives as laid down in the UCITS’ fund rules, instruments of incorporation or prospectus. 3. A UCITS shall ensure that its global exposure relating to derivative instruments does not exceed the total net value of its portfolio. The exposure is calculated taking into

---

[organisation, Article 41] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.77)
including embedded derivatives pursuant to the fourth subparagraph of Article 51(3) of Directive 2009/65/EC, which may not exceed the total of the UCITS net asset value; (b) the market risk of the UCITS portfolio. 2. Member States shall require management companies to calculate the UCITS global exposure on at least a daily basis. 3. Member States may allow management companies to calculate global exposure by using the commitment approach, the value at risk approach or other advanced risk measurement methodologies as may be appropriate. For the purposes of this provision, ‘value at risk’ shall mean a measure of the maximum expected loss at a given confidence level over a specific time period. Member States shall require management companies to ensure that the method selected to measure global exposure is appropriate, taking into account the investment strategy pursued by the UCITS and the types and complexities of the financial derivative instruments used, and the proportion of the UCITS portfolio which comprises financial derivative instruments. 4. Where a UCITS in accordance with Article 51(2) of Directive 2009/65/EC employs techniques and instruments including repurchase agreements or securities lending transactions in order to generate additional leverage or exposure to market risk, Member States shall

---

[organisation, Article 42 to Article 43] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.77)
market value of an equivalent position in the underlying asset of that derivative (standard commitment approach). Member States may allow management companies to apply other calculation methods which are equivalent to the standard commitment approach. 3. Member States may allow a management company to take account of netting and hedging arrangements when calculating global exposure, where these arrangements do not disregard obvious and material risks and result in a clear reduction in risk exposure. 4. Where the use of financial derivative instruments does not generate incremental exposure for the UCITS, the underlying exposure need not be included in the commitment calculation. 5. Where the commitment approach is used, temporary borrowing arrangements entered into on behalf of the UCITS in accordance with Article 83 of Directive 2009/65/EC need not be included in the global exposure calculation. Counterparty risk and issuer concentration 1. Member States shall require management companies to ensure that counterparty risk arising from an over-the-counter (OTC) financial derivative instrument is subject to the limits set out in Article 52 of Directive 2009/65/EC. 2. When calculating the UCITS exposure to a counterparty in accordance with the limits as referred to in Article 52(1) of Directive 2009/65/EC, management companies shall use

---

[organisation, Article 41 to Article 42] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.76)
financial derivative instruments. 4. Where a UCITS in a
```
</details>

## q15 (single)
**Question:** When a UCITS wants to market its units in another Member State, how quickly must its home authorities transmit the notification file?
**Reference:** No later than 10 working days after receiving the complete documentation.

**Agent answer:**

The competent authorities of the UCITS home Member State must transmit the complete notification documentation to the competent authorities of the host Member State no later than 10 working days from the date of receipt of the notification letter accompanied by the complete documentation [ucits_directive, Article 93(3)].

Please note that this answer is based on the original 2009 UCITS Directive text; later amendments may have updated these procedures.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 93] Directive 2009/65/EC (UCITS Directive) (relevance 0.78)
company that manages the UCITS. 2. A UCITS shall enclose with the notification letter, as referred to in paragraph 1, the latest version of the following: (a) its fund rules or its instruments of incorporation, its prospectus and, where appropriate, its latest annual report and any subsequent half-yearly report translated in accordance with the provisions of Article 94(1)(c) and (d); and (b) its key investor information referred to in Article 78, translated in accordance with Article 94(1)(b) and (d). 3. The competent authorities of the UCITS home Member State shall verify whether the documentation submitted by the UCITS in accordance with paragraphs 1 and 2 is complete. The competent authorities of the UCITS home Member State shall transmit the complete documentation referred to in paragraphs 1 and 2 to the competent authorities of the Member State in which the UCITS proposes to market its units, no later than 10 working days of the date of receipt of the notification letter accompanied by the complete documentation provided for in paragraph 2. They shall enclose with the documentation an attestation that the UCITS fulfils the conditions imposed by this Directive. Upon the transmission of the documentation, the competent authorities of the UCITS

---

[ucits_directive, Article 93 to Article 94] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
the notification procedure set out in this Article, the competent authorities of the Member State in which a UCITS proposes to market its units shall not request any additional documents, certificates or information other than those provided for in this Article. 7. The UCITS home Member State shall ensure that the competent authorities of the UCITS host Member State have access, by electronic means, to the documents referred to in paragraph 2 and, if applicable, to any translations thereof. It shall ensure that the UCITS keeps those documents and translations up to date. The UCITS shall notify any amendments to the documents referred to in paragraph 2 to the competent authorities of the UCITS host Member State and shall indicate where those documents can be obtained electronically. 8. In the event of a change in the information regarding the arrangements made for marketing communicated in the notification letter in accordance with paragraph 1, or a change regarding share classes to be marketed, the UCITS shall give written notice thereof to the competent authorities of the host Member State before implementing the change. 1. Where a UCITS markets its units in a UCITS host Member State, it shall provide to investors

---

[ucits_directive, Article 93] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
accompanied by the complete documentation provided for in paragraph 2. They shall enclose with the documentation an attestation that the UCITS fulfils the conditions imposed by this Directive. Upon the transmission of the documentation, the competent authorities of the UCITS home Member State shall immediately notify the UCITS about the transmission. The UCITS may access the market of the UCITS host Member State as from the date of that notification. 4. Member States shall ensure that the notification letter referred to in paragraph 1 and the attestation referred to in paragraph 3 are provided in a language customary in the sphere of international finance, unless the UCITS home and host Member States agree to that notification letter and that attestation being provided in an official language of both Member States. 5. Member States shall ensure that the electronic transmission and filing of the documents referred to in paragraph 3 is accepted by their competent authorities. 6. For the purpose of the notification procedure set out in this Article, the competent authorities of the Member State in which a UCITS proposes to market its units shall not request any additional documents, certificates or information other than those provided for in this

---

[ucits_directive, Article 91 to Article 93] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
unambiguous manner and is kept up to date. 4. For the purposes of this Chapter, a UCITS shall include investment compartments thereof. UCITS shall, in accordance with the laws, regulations and administrative provisions in force in the Member State where their units are marketed, take the measures necessary to ensure that facilities are available in that Member State for making payments to unit-holders, repurchasing or redeeming units and making available the information which UCITS are required to provide. 1. If a UCITS proposes to market its units in a Member State other than its home Member State, it shall first submit a notification letter to the competent authorities of its home Member State. The notification letter shall include information on arrangements made for marketing units of the UCITS in the host Member State, including, where relevant, in respect of share classes. In the context of Article 16(1), it shall include an indication that the UCITS is marketed by the management company that manages the UCITS. 2. A UCITS shall enclose with the notification letter, as referred to in paragraph 1, the latest version of the following: (a) its fund rules or its instruments of incorporation, its prospectus and, where appropriate,

---

[ucits_directive, Article 90 to Article 92] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
PROVISIONS APPLICABLE TO UCITS WHICH MARKET THEIR UNITS IN MEMBER STATES OTHER THAN THOSE IN WHICH THEY ARE ESTABLISHED 1. UCITS host Member States shall ensure that UCITS are able to market their units within their territories upon notification in accordance with Article 93. 2. UCITS host Member States shall not impose any additional requirements or administrative procedures on UCITS as referred to in paragraph 1 in respect of the field governed by this Directive. 3. Member States
```
</details>

## q16 (single)
**Question:** What criteria must a financial instrument meet to count as an eligible transferable security for a UCITS?
**Reference:** Potential loss limited to the amount paid; liquidity does not compromise the UCITS's ability to redeem; reliable valuation; appropriate information available; negotiable; consistent with the investment objectives; risks adequately captured by risk management.

**Agent answer:**

To count as an eligible transferable security for a UCITS, a financial instrument must fulfill the following criteria [eligible_assets, Article 2]:
1. The potential loss that the UCITS may incur by holding the instrument must be limited to the amount paid for it [eligible_assets, Article 2].
2. Its liquidity must not compromise the ability of the UCITS to satisfy redemption requests or comply with redemption obligations [eligible_assets, Article 2].
3. A reliable valuation must be available in the form of regular, accurate, and independent prices (market prices or independent valuation systems for instruments on regulated markets, or periodic valuations derived from the issuer or competent research for other securities) [eligible_assets, Article 2].
4. Appropriate information must be available to the market or the UCITS regarding the security or its portfolio [eligible_assets, Article 2].
5. The instrument must be negotiable [eligible_assets, Article 2].
6. Its acquisition must be consistent with the investment objectives and policy of the UCITS [eligible_assets, Article 2].
7. Its risks must be adequately captured by the risk management process of the UCITS [eligible_assets, Article 2].

Instruments admitted to or dealt in on eligible regulated markets are presumed to be negotiable and not to compromise liquidity, unless the UCITS has contrary information [eligible_assets, Article 2]. 

*Note: This answer reflects the indexed provisions of Commission Directive 2007/16/EC (Eligible Assets Directive).*

<details><summary>Retrieved passages</summary>

```
[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.84)
Directive 85/611/EEC to transferable securities shall be understood as a reference to financial instruments which fulfil the following criteria: (a) the potential loss which the UCITS may incur with respect to holding those instruments is limited to the amount paid for them; (b) their liquidity does not compromise the ability of the UCITS to comply with Article 37 of Directive 85/611/EEC; (c) reliable valuation is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1) of Directive 85/611/EEC, in the form of accurate, reliable and regular prices which are either market prices or prices made available by valuation systems independent from issuers; (ii) in the case of other securities as referred to in Article 19(2) of Directive 85/611/EEC, in the form of a valuation on a periodic basis which is derived from information from the issuer of the security or from competent investment research; (d) appropriate information is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1)

---

[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.81)
there is information available to the UCITS that would lead to a different determination, financial instruments which are admitted or dealt in on a regulated market in accordance with points (a), (b) or (c) of Article 19(1) of Directive 85/611/EEC shall be presumed not to compromise the ability of the UCITS to comply with Article 37 of Directive 85/611/EEC and shall also be presumed to be negotiable. 2. Transferable securities as referred to in Article 1(8) of Directive 85/611/EEC shall be taken to include the following: (a) units in closed end funds constituted as investment companies or as unit trusts which fulfil the following criteria: (i) they fulfil the criteria set out in paragraph 1; (ii) they are subject to corporate governance mechanisms applied to companies; (iii) where asset management activity is carried out by another entity on behalf of the closed end fund, that entity is subject to national regulation for the purpose of investor protection; (b) units in closed end funds constituted under the law of contract which fulfil the following criteria: (i) they fulfil the criteria set out in paragraph 1; (ii) they are subject to corporate governance mechanisms equivalent to those applied to companies as referred

---

[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.81)
or from competent investment research; (d) appropriate information is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1) of Directive 85/611/EEC, in the form of regular, accurate and comprehensive information to the market on the security or, where relevant, on the portfolio of the security; (ii) in the case of other securities as referred to in Article 19(2) of Directive 85/611/EEC, in the form of regular and accurate information to the UCITS on the security or, where relevant, on the portfolio of the security; (e) they are negotiable; (f) their acquisition is consistent with the investment objectives or the investment policy, or both, of the UCITS pursuant to Directive 85/611/EEC; (g) their risks are adequately captured by the risk management process of the UCITS. For the purposes of points (b) and (e) of the first subparagraph, and unless there is information available to the UCITS that would lead to a different determination, financial instruments which are admitted or dealt in on a regulated market in accordance with points (a), (b) or (c) of Article 19(1) of Directive 85/611/EEC

---

[eligible_assets, Recitals to Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.79)
technical advice. (16) The measures provided for in this Directive are in accordance with the opinion of the European Securities Committee, HAS ADOPTED THIS DIRECTIVE: Subject matter This Directive lays down rules clarifying, for the purposes of their uniform application, the following terms: 1. transferable securities, as defined in Article 1(8) of Directive 85/611/EEC; 2. money market instruments, as defined in Article 1(9) of Directive 85/611/EEC; 3. liquid financial assets, as referred to in the definition of UCITS laid down in Article 1(2) of Directive 85/611/EEC, with respect to financial derivative instruments; 4. transferable securities and money market instruments embedding derivatives, as referred to in the fourth subparagraph of Article 21(3) of Directive 85/611/EEC; 5. techniques and instruments for the purpose of efficient portfolio management, as referred to in Article 21(2) of Directive 85/611/EEC; 6. index-replicating UCITS, as referred to in Article 22a(1) of Directive 85/611/EEC. Article 1(8) of Directive 85/611/EEC Transferable securities 1. The reference in Article 1(8) of Directive 85/611/EEC to transferable securities shall be understood as a reference to financial instruments which fulfil the following criteria: (a) the potential loss which the UCITS may incur with respect to holding those instruments is limited to the amount paid

---

[eligible_assets, Recitals] Commission Directive 2007/16/EC (eligible assets) (relevance 0.78)
Directive 85/611/EEC defines transferable securities exclusively from a formal/legal point of view. Accordingly the definition of transferable securities is applicable to a wide range of financial products with differing features and different levels of liquidity. For each of those financial products, consistency between the definition of transferable securities and other provisions of the Directive should be ensured. (7) Closed end funds constitute an asset 
```
</details>

## q17 (single)
**Question:** What maturity must a money market instrument have to be regarded as normally dealt in on the money market?
**Reference:** A maturity at issuance or residual maturity of up to and including 397 days, or regular yield adjustments at least every 397 days.

**Agent answer:**

To be regarded as normally dealt in on the money market, a financial instrument must fulfill at least one of the following criteria regarding its maturity or yield adjustment:
(a) have a maturity at issuance of up to and including 397 days;
(b) have a residual maturity of up to and including 397 days;
(c) undergo regular yield adjustments in line with money market conditions at least every 397 days; or
(d) have a risk profile, including credit and interest rate risks, that corresponds to that of financial instruments which have a maturity as referred to in points (a) or (b), or are subject to a yield adjustment as referred to in point (c) [eligible_assets, Article 3(2)].

*Note: This answer reflects the indexed texts of the original EU UCITS directives and regulations (specifically Commission Directive 2007/16/EC), and later amendments or national transpositions may affect these rules.*

<details><summary>Retrieved passages</summary>

```
[eligible_assets, Article 3 to Article 4] Commission Directive 2007/16/EC (eligible assets) (relevance 0.72)
The reference in Article 1(9) of Directive 85/611/EEC to money market instruments as instruments shall be understood as a reference to the following: (a) financial instruments which are admitted to trading or dealt in on a regulated market in accordance with points (a), (b) and (c) of Article 19(1) of Directive 85/611/EEC; (b) financial instruments which are not admitted to trading. 2. The reference in Article 1(9) of Directive 85/611/EEC to money market instruments as instruments normally dealt in on the money market shall be understood as a reference to financial instruments which fulfil one of the following criteria: (a) they have a maturity at issuance of up to and including 397 days; (b) they have a residual maturity of up to and including 397 days; (c) they undergo regular yield adjustments in line with money market conditions at least every 397 days; (d) their risk profile, including credit and interest rate risks, corresponds to that of financial instruments which have a maturity as referred to in points (a) or (b), or are subject to a yield adjustment as referred to in point (c). Article 1(9) of Directive 85/611/EEC Liquid instruments with a value which can be accurately determined at

---

[eligible_assets, Article 3 to Article 4] Commission Directive 2007/16/EC (eligible assets) (relevance 0.68)
have a maturity as referred to in points (a) or (b), or are subject to a yield adjustment as referred to in point (c). Article 1(9) of Directive 85/611/EEC Liquid instruments with a value which can be accurately determined at any time 1. The reference in Article 1(9) of Directive 85/611/EEC to money market instruments as instruments which are liquid shall be understood as a reference to financial instruments which can be sold at limited cost in an adequately short time frame, taking into account the obligation of the UCITS to repurchase or redeem its units at the request of any unit holder. 2. The reference in Article 1(9) of Directive 85/611/EEC to money market instruments as instruments which have a value which can be accurately determined at any time shall be understood as a reference to financial instruments for which accurate and reliable valuations systems, which fulfil the following criteria, are available: (a) they enable the UCITS to calculate a net asset value in accordance with the value at which the financial instrument held in the portfolio could be exchanged between knowledgeable willing parties in an arm’s length transaction; (b) they are based either on market data or on

---

[eligible_assets, Article 5 to Article 6] Commission Directive 2007/16/EC (eligible assets) (relevance 0.66)
issuance programme or on the legal and financial situation of the issuer prior to the issue of the money market instrument; (b) updates of the information referred to in point (a) on a regular basis and whenever a significant event occurs; (c) available and reliable statistics on the issue or the issuance programme or other data enabling an appropriate assessment of the credit risks related to the investment in such instruments. 4. For all money market instruments covered by the first indent of Article 19(1)(h) of Directive 85/611/EEC except those referred to in paragraph 2 of this Article and those issued by the European Central Bank or by a central bank from a Member State, appropriate information as referred to in point (b) of paragraph 1 of this Article shall consist in information on the issue or the issuance programme or on the legal and financial situation of the issuer prior to the issue of the money market instrument. Article 19(1)(h) of Directive 85/611/EEC Establishment which is subject to and complies with prudential rules considered by the competent authorities to be at least as stringent as those laid down by Community law The reference in the third indent of Article

---

[eligible_assets, Article 5] Commission Directive 2007/16/EC (eligible assets) (relevance 0.65)
of a federal State which is a Member State, by one of the members making up the federation, appropriate information as referred to in point (b) of paragraph 1 of this Article shall consist in the following: (a) information on both the issue or the issuance programme and the legal and financial situation of the issuer prior to the issue of the money market instrument; (b) updates of the information referred to in point (a) on a regular basis and whenever a significant event occurs; (c) the information referred to in point (a), verified by appropriately qualified third parties not subject to instructions from the issuer; (d) available and reliable statistics on the issue or the issuance programme. 3. For money market instruments covered by the third indent of Article 19(1)(h) of Directive 85/611/EEC, appropriate information as referred to in point (b) of paragraph 1 of this Article shall consist in the following: (a) information on the issue or the issuance programme or on the legal and financial situation of the issuer prior to the issue of the money market instrument; (b) updates of the information referred to in point (a) on a regular basis and whenever a significant event

---

[eligible_assets, Article 5] Commission Directive 2007/16/EC (eligible assets) (relevance 0.65)
market instruments, other than those dealt in on a regulated market, of which the issue or the issuer is itself regulated for the purpose of protecting investors and savings, shall be understood as a reference to financial instruments which fulfil the following criteria: (a) they fulfil one of the criteria set out in Article 3(2) and all the criteria set out in Article 4(1) and (2); (b) appropriate information is available for them, including information which allows an appropriate assessment of the credit risks related to the investment in such instruments, taking into account paragraphs 2, 3 and 4 of this Article; (c) they are freely t
```
</details>

## q18 (single)
**Question:** What conditions must a financial index meet to be used as the underlying of a UCITS derivative?
**Reference:** It must be sufficiently diversified, represent an adequate benchmark for the market it refers to, and be published in an appropriate manner.

**Agent answer:**

To be used as the underlying of a UCITS derivative, a financial index must fulfill three main conditions under Commission Directive 2007/16/EC:

1. **They are sufficiently diversified** [eligible_assets, Article 9(1)(a)], meaning that price movements or trading activities regarding a single component do not unduly influence the whole index performance [eligible_assets, Article 9(1)(a)(i)], and its composition meets the diversification requirements equivalent to those in Article 22a of the Directive (whether composed of eligible UCITS assets or other assets) [eligible_assets, Article 9(1)(a)(ii)-(iii)].
2. **They represent an adequate benchmark for the market to which they refer** [eligible_assets, Article 9(1)(b)], meaning the index measures a representative group of underlyings in a relevant and appropriate way, is periodically revised/rebalanced based on publicly available criteria to keep reflecting those markets, and has sufficiently liquid underlyings to allow users to replicate it if necessary [eligible_assets, Article 9(1)(b)(i)-(iii)].
3. **They are published in an appropriate manner** [eligible_assets, Article 9(1)(c)], relying on sound pricing and calculation procedures (including for components without market prices), and provide wide and timely publication of material information regarding index calculation, rebalancing methodologies, index changes, or operational difficulties [eligible_assets, Article 9(1)(c)(i)-(ii)].

*(Note: This answer reflects the indexed provisions of Commission Directive 2007/16/EC; subsequent amendments or updates are not included in the corpus.)*

<details><summary>Retrieved passages</summary>

```
[eligible_assets, Article 9] Commission Directive 2007/16/EC (eligible assets) (relevance 0.78)
the following criteria are fulfilled: (i) the index measures the performance of a representative group of underlyings in a relevant and appropriate way; (ii) the index is revised or rebalanced periodically to ensure that it continues to reflect the markets to which it refers following criteria which are publicly available; (iii) the underlyings are sufficiently liquid, which allows users to replicate the index, if necessary; (c) they are published in an appropriate manner, in that the following criteria are fulfilled: (i) their publication process relies on sound procedures to collect prices and to calculate and to subsequently publish the index value, including pricing procedures for components where a market price is not available; (ii) material information on matters such as index calculation, rebalancing methodologies, index changes or any operational difficulties in providing timely or accurate information is provided on a wide and timely basis. 2. Where the composition of assets which are used as underlyings by financial derivatives in accordance with Article 19(1) of Directive 85/611/EEC does not fulfil the criteria set out in paragraph 1 of this Article, those financial derivatives shall, where they comply with the criteria set out in Article 8(1) of this Directive, be regarded as

---

[eligible_assets, Article 8 to Article 9] Commission Directive 2007/16/EC (eligible assets) (relevance 0.76)
to a valuation, by the UCITS, corresponding to the fair value as referred to in paragraph 3 of this Article, which does not rely only on market quotations by the counterparty and which fulfils the following criteria: (a) the basis for the valuation is either a reliable up-to-date market value of the instrument, or, if such a value is not available, a pricing model using an adequate recognised methodology; (b) verification of the valuation is carried out by one of the following: (i) an appropriate third party which is independent from the counterparty of the OTC-derivative, at an adequate frequency and in such a way that the UCITS is able to check it; (ii) a unit within the UCITS which is independent from the department in charge of managing the assets and which is adequately equipped for such purpose. 5. The reference in Articles 1(2) and 19(1)(g) of Directive 85/611/EEC to liquid financial assets shall be understood as excluding derivatives on commodities. Article 19(1)(g) of Directive 85/611/EEC Financial indices 1. The reference in point (g) of Article 19(1) of Directive 85/611/EEC to financial indices shall be understood as a reference to indices which fulfil the following criteria: (a) they are

---

[eligible_assets, Recitals] Commission Directive 2007/16/EC (eligible assets) (relevance 0.76)
Directive. It is necessary to ensure a uniform application of those criteria and it is also necessary to make clear that the criteria have to be understood in a way which is consistent with other provisions of the Directive. It should also be made clear that if credit derivatives comply with those criteria, they are financial derivative instruments within the meaning of Directive 85/611/EEC and hence eligible for treatment as liquid financial assets. (11) The need for clarification is particularly pressing for derivatives on financial indices. There is currently a wide range of financial indices which function as the underlying for a derivative instrument. These indices may vary as regards their composition or the weighting of their components. In all cases it has to be ensured that the UCITS is able to fulfil its obligations as regards portfolio liquidity, as resulting from Article 37 of Directive 85/611/EEC, and the calculation of the net asset value and that those obligations are not negatively affected by the features of the underlying of a derivative. It should be clarified that derivatives on financial indices whose composition is sufficiently diversified, which represent an adequate benchmark to the market to which they refer and which

---

[eligible_assets, Article 8 to Article 9] Commission Directive 2007/16/EC (eligible assets) (relevance 0.74)
on commodities. Article 19(1)(g) of Directive 85/611/EEC Financial indices 1. The reference in point (g) of Article 19(1) of Directive 85/611/EEC to financial indices shall be understood as a reference to indices which fulfil the following criteria: (a) they are sufficiently diversified, in that the following criteria are fulfilled: (i) the index is composed in such a way that price movements or trading activities regarding one component do not unduly influence the performance of the whole index; (ii) where the index is composed of assets referred to in Article 19(1) of Directive 85/611/EEC, its composition is at least diversified in accordance with Article 22a of that Directive; (iii) where the index is composed of assets other than those referred to in Article 19(1) of Directive 85/611/EEC, it is diversified in a way which is equivalent to that provided for in Article 22a of that Directive; (b) they represent an adequate benchmark for the market to which they refer, in that the following criteria are fulfilled: (i) the index measures the performance of a representative group of underlyings in a relevant and appropriate way; (ii) the index is revised or rebalanced periodically to ensure that it continues to reflect the markets

---

[eligible_assets, Article 8] Commission Directive 2007/16/EC (eligible assets) (relevance 0.74)
of the following: (i) assets as listed in Article 19(1) of Directive 85/611/EEC including financial instruments having one or several characteristics of those assets; (ii) interest rates; (iii) foreign exchange rates or currencies; (iv) financial indices; (b) in the case of OTC derivatives, they comply with the conditions set out in the second and third indents of Article 19(1)(g) of Directive 85/611/EEC. 2. Financial derivativ
```
</details>

## q19 (single)
**Question:** How long must a management company retain the records it is required to keep?
**Reference:** At least 5 years (the records of portfolio transactions and of subscription and redemption orders).

**Agent answer:**

Management companies must ensure the retention of required records for a period of at least 5 years [organisation, Article 16]. 

Exceptions and additional conditions:
* Competent authorities may, in exceptional circumstances, require management companies to retain any or all records for a longer period determined by the nature of the instrument or portfolio transaction, if necessary to exercise their supervisory functions [organisation, Article 16].
* Following the termination of a management company's authorisation, Member States or competent authorities may require records to be retained for the outstanding term of the 5-year period [organisation, Article 16]. 
* If a management company transfers its responsibilities to another management company, arrangements may be required to ensure that records for the past 5 years are accessible to that company [organisation, Article 16].

Please note that this answer reflects the indexed versions of the original EU directives (in this case, Commission Directive 2010/43/EU) and later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[organisation, Article 15 to Article 16] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.69)
for each unit; (j) the total subscription or redemption value of the units; (k) the gross value of the order including charges for subscription or net amount after charges for redemption. Recordkeeping requirements 1. Member States shall require management companies to ensure the retention of the records referred to in Articles 14 and 15 for a period of at least 5 years. However, competent authorities may, in exceptional circumstances, require management companies to retain any or all of those records for a longer period, determined by the nature of the instrument or portfolio transaction, where it is necessary to enable the authority to exercise its supervisory functions under Directive 2009/65/EC. 2. Following the termination of the authorisation of a management company, Member States or competent authorities may require the management company to retain records referred to in paragraph 1 for the outstanding term of the 5-year period. Where the management company transfers its responsibilities in relation to the UCITS to another management company, Member States or competent authorities may require that arrangements are made that such records for the past 5 years are accessible to that company. 3. The records shall be retained in a medium that allows the storage

---

[organisation, Article 16 to Article 17] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.68)
another management company, Member States or competent authorities may require that arrangements are made that such records for the past 5 years are accessible to that company. 3. The records shall be retained in a medium that allows the storage of information in a way accessible for future reference by the competent authority, and in such a form and manner that the following conditions are met: (a) the competent authority must be able to access them readily and to reconstitute each key stage of the processing of each portfolio transaction; (b) it must be possible for any corrections or other amendments, and the contents of the records prior to such corrections or amendments, to be easily ascertained; (c) it must not be possible for the records to be otherwise manipulated or altered. (Article 12(1)(b) and Article 14(1)(d) and (2)(c) of Directive 2009/65/EC) Criteria for the identification of conflicts of interest 1. Member States shall ensure that, for the purposes of identifying the types of conflict of interest that arise in the course of providing services and activities and whose existence may damage the interests of a UCITS, management companies take into account, by way of minimum criteria, the question of

---

[organisation, Article 4] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.61)
functions and responsibilities; (b) to ensure that their relevant persons are aware of the procedures which must be followed for the proper discharge of their responsibilities; (c) to establish, implement and maintain adequate internal control mechanisms designed to secure compliance with decisions and procedures at all levels of the management company; (d) to establish, implement and maintain effective internal reporting and communication of information at all relevant levels of the management company as well as effective information flows with any third party involved; (e) to maintain adequate and orderly records of their business and internal organisation. Member States shall ensure that management companies take into account the nature, scale and complexity of the business of the management company, and the nature and range of services and activities undertaken in the course of that business. 2. Member States shall require management companies to establish, implement and maintain systems and procedures that are adequate to safeguard the security, integrity and confidentiality of information, taking into account the nature of the information in question. 3. Member States shall require management companies to establish, implement and maintain an adequate business continuity policy aimed at ensuring, in the case of an interruption to their systems

---

[ucits_directive, Article 17] Directive 2009/65/EC (UCITS Directive) (relevance 0.61)
of a management company, taking into account the activities envisaged, they shall, within two months of receiving all the information referred to in paragraph 2, communicate that information to the competent authorities of the management company’s host Member State and shall inform the management company accordingly. They shall also communicate details of any compensation scheme intended to protect investors. Where the competent authorities of the management company’s home Member State refuse to communicate the information referred to in paragraph 2 to the competent authorities of the management company’s host Member State, they shall give reasons for such refusal to the management company concerned within two months of receiving all the information. The refusal or any failure to reply shall be subject to the right to apply to the courts in the management company’s home Member State. Where a management company wishes to pursue the activity of collective portfolio management referred to in Annex II, the competent authorities of the management company’s home Member State shall enclose with the documentation sent to the competent authorities of the management company’s host Member State an attestation that the management company has been authorised pursuant to the provisions of this Directive, a description of

---

[organisation, Article 4 to Article 5] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.61)
information, taking into account the nature of the 
```
</details>

## q20 (single)
**Question:** Does the risk management function of a UCITS management company have to be independent?
**Reference:** Yes. It must establish a permanent risk management function that is hierarchically and functionally independent from operating units, where appropriate and proportionate.

**Agent answer:**

Yes, management companies must establish and maintain a permanent risk management function that is hierarchically and functionally independent from operating units [organisation, Article 11 to Article 12]. 

However, Member States may allow management companies to derogate from this independence obligation if the derogation is appropriate and proportionate given the nature, scale, and complexity of the company's business and the UCITS it manages [organisation, Article 11 to Article 12]. In such cases, the management company must still be able to demonstrate that appropriate safeguards against conflicts of interest have been adopted to allow for the independent performance of risk management activities [organisation, Article 11 to Article 12].

*Note: This answer reflects the indexed provisions of Commission Directive 2010/43/EU and may be subject to later amendments.*

<details><summary>Retrieved passages</summary>

```
[organisation, Article 12] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.78)
interest have been adopted so as to allow an independent performance of risk management activities and that its risk management process satisfies the requirements of Article 51 of Directive 2009/65/EC. 3. The permanent risk management function shall: (a) implement the risk management policy and procedures; (b) ensure compliance with the UCITS risk limit system, including statutory limits concerning global exposure and counterparty risk in accordance with Articles 41, 42 and 43; (c) provide advice to the board of directors as regards the identification of the risk profile of each managed UCITS; (d) provide regular reports to the board of directors and, where it exists, the supervisory function, on: (i) the consistency between the current levels of risk incurred by each managed UCITS and the risk profile agreed for that UCITS; (ii) the compliance of each managed UCITS with relevant risk limit systems; (iii) the adequacy and effectiveness of the risk management process, indicating in particular whether appropriate remedial measures have been taken in the event of any deficiencies; (e) provide regular reports to the senior management outlining the current level of risk incurred by each managed UCITS and any actual or foreseeable breaches to their limits, so as to ensure

---

[organisation, Article 11 to Article 12] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.76)
establish, implement and maintain an audit plan to examine and evaluate the adequacy and effectiveness of the management company’s systems, internal control mechanisms and arrangements; (b) to issue recommendations based on the result of work carried out in accordance with point (a); (c) to verify compliance with the recommendations referred to in point (b); (d) to report in relation to internal audit matters in accordance with Article 9(4). Permanent risk management function 1. Member States shall require management companies to establish and maintain a permanent risk management function. 2. The permanent risk management function referred to in paragraph 1 shall be hierarchically and functionally independent from operating units. However, Member States may allow management companies to derogate from that obligation where the derogation is appropriate and proportionate in view of the nature, scale and complexity of the management company’s business and of the UCITS it manages. A management company shall be able to demonstrate that appropriate safeguards against conflicts of interest have been adopted so as to allow an independent performance of risk management activities and that its risk management process satisfies the requirements of Article 51 of Directive 2009/65/EC. 3. The permanent risk management function shall: (a) implement the

---

[organisation, Recitals] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.75)
also ensure that adequate control exists so as to ensure the assets of the UCITS are invested according to the fund rules or the instruments of incorporation and the applicable legal provisions and that risk limits of each UCITS are complied with. The allocation of responsibilities should be consistent with the role and responsibilities of the senior management and the supervisory function under applicable national law and corporate governance codes. It is possible that senior management includes several or all members of the board of directors. (11) To ensure that a management company has an adequate control mechanism, a permanent compliance function and an internal audit function are necessary. The compliance function should be designed in such a way as to ensure that it may detect any risk of failure by the management company to comply with its obligations under Directive 2009/65/EC. The audit function should aim at verifying and evaluating the different control procedures and administrative arrangements the management company has put in place. (12) It is necessary to allow management companies some flexibility in structuring the organisation of their risk management. Where it is not appropriate or proportionate to have a separate risk management function, the management company

---

[organisation, Recitals] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.74)
Directive 2009/65/EC contains an obligation to specify the criteria for assessing the adequacy of a management company’s risk management process. Such criteria focus on the establishment of an adequate and documented risk management policy to be employed by management companies. This policy should enable the management companies to assess the risks of the positions taken within the portfolios they manage and the contributions of these individual risks to the overall risk profile of the portfolio. The organisation of the risk management policy should be adequate and proportionate to the nature, scale and complexity of the management company’s activities and of the UCITS it manages. (24) The periodical assessment, monitoring and review of the risk management policy by management companies are also a criterion to assess the adequacy of the risk management process. This criterion also includes the review of the effectiveness of measures taken to address any deficiencies in the performance of the risk management process. (25) As an essential element in the criteria for assessing the adequacy of risk management processes, proportionate and effective risk measurement techniques should be adopted by management companies in order to measure at any time the risks which the UCITS they manage are or

---

[organisation, Article 38 to Article 40] Commission Directive 2010/43/EU (organisational requirements, conflicts of interes
```
</details>

## q21 (single)
**Question:** Must a management company have a strategy for exercising the voting rights attached to the funds' holdings?
**Reference:** Yes. It must develop adequate and effective strategies for determining when and how voting rights are exercised, to the exclusive benefit of the UCITS.

**Agent answer:**

Yes, a management company must develop adequate and effective strategies for determining when and how voting rights attached to instruments held in managed portfolios are to be exercised, to the exclusive benefit of the UCITS concerned [organisation, Article 20]. 

The strategy must determine measures and procedures for:
- Monitoring relevant corporate events [organisation, Article 20];
- Ensuring that the exercise of voting rights accords with the investment objectives and policy of the relevant UCITS [organisation, Article 20];
- Preventing or managing any conflicts of interest arising from the exercise of voting rights [organisation, Article 20].

**Conditions and Exceptions:**
- A summary description of this strategy must be made available to investors [organisation, Article 21].
- Details of the actions taken on the basis of the strategy must be made available to unit-holders free of charge and upon their request [organisation, Article 21].

*Note: This answer reflects the indexed provisions of Commission Directive 2010/43/EU; later amendments are not covered by this corpus.*

<details><summary>Retrieved passages</summary>

```
[organisation, Article 20 to Article 21] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.77)
by the management company for the management of conflicts of interest are not sufficient to ensure, with reasonable confidence, that risks of damage to the interests of UCITS or of its unit-holders will be prevented, the senior management or other competent internal body of the management company is promptly informed in order for them to take any necessary decision to ensure that in any case the management company acts in the best interests of the UCITS and of its unit-holders. 3. The management company shall report situations referred to in paragraph 2 to investors by any appropriate durable medium and give reasons for its decision. Strategies for the exercise of voting rights 1. Member States shall require management companies to develop adequate and effective strategies for determining when and how voting rights attached to instruments held in the managed portfolios are to be exercised, to the exclusive benefit of the UCITS concerned. 2. The strategy referred to in paragraph 1 shall determine measures and procedures for: (a) monitoring relevant corporate events; (b) ensuring that the exercise of voting rights is in accordance with the investment objectives and policy of the relevant UCITS; (c) preventing or managing any conflicts of interest

---

[organisation, Article 21 to Article 22] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.76)
shall determine measures and procedures for: (a) monitoring relevant corporate events; (b) ensuring that the exercise of voting rights is in accordance with the investment objectives and policy of the relevant UCITS; (c) preventing or managing any conflicts of interest arising from the exercise of voting rights. 3. A summary description of the strategies referred to in paragraph 1 shall be made available to investors. Details of the actions taken on the basis of those strategies shall be made available to the unit-holders free of charge and on their request. (Article 14(1)(a), (b) and (2)(a), (b) of Directive 2009/65/EC) Duty to act in the best interests of UCITS and their unit-holders 1. Member States shall require management companies to ensure that unit-holders of managed UCITS are treated fairly. Management companies shall refrain from placing the interests of any group of unit-holders above the interests of any other group of unit-holders. 2. Member States shall require management companies to apply appropriate policies and procedures for preventing malpractices that might reasonably be expected to affect the stability and integrity of the market. 3. Without prejudice to requirements under national law, Member States shall require management companies to ensure that fair, correct and

---

[organisation, Recitals] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.73)
rights are exercised to the exclusive benefit of UCITS. Information related to the strategy and its application should be freely available to investors, including via a website. As the case may be, the decision not to exercise voting rights could be considered in certain circumstances as being to the exclusive benefit of the UCITS depending upon its investment strategy. However the possibility for an investment company to vote itself or to give specific voting instructions to its management company should not be excluded. (17) The obligation to inform senior management or other competent internal body of the management company in order for them to take necessary decisions should not limit the duty of the management companies and the UCITS to report on situations where the organisational or administrative arrangements for conflicts of interest were not sufficient to ensure, with reasonable confidence, the prevention of the risk of damage, for instance in their periodic reports. Such reporting should explain and give reasons for the decision taken by the management company, even where a decision is taken not to act, taking into account the internal policies and procedures adopted to identify, prevent and manage conflicts of interest. (18) Directive 2009/65/EC obliges management

---

[organisation, Recitals] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.69)
each portfolio transaction involving the UCITS can be reconstructed according to its origin, the parties to it, its nature, and the time and place at which it was executed. Therefore, it is necessary to lay down requirements for recording of portfolio transactions and of subscription and redemption orders. (15) Directive 2009/65/EC requires UCITS management companies to have appropriate mechanisms in place to ensure fair treatment of UCITS in cases of unavoidable conflicts of interest. Therefore, management companies should make sure that in these cases senior management or other competent internal body of the management company are promptly informed, in order to for them to take any necessary decision to ensure the fair treatment of the UCITS and of its unit-holders. (16) Management companies should be requested to adopt, apply and maintain an effective and adequate strategy for the exercise of voting rights attached to the financial instruments held by the UCITS they manage, with a view to ensuring that such rights are exercised to the exclusive benefit of UCITS. Information related to the strategy and its application should be freely available to investors, including via a website. As the case may be, the decision not to exercise voting rights could

---

[organisation, Article 26] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.66)
steps to obtain the best possible result for the UCITS taking into account pr
```
</details>

## q22 (single)
**Question:** What must a management company do when executing decisions to deal on behalf of a UCITS?
**Reference:** Take all reasonable steps to obtain the best possible result for the UCITS (best execution), considering price, costs, speed, likelihood of execution and settlement, order size and nature.

**Agent answer:**

When executing decisions to deal on behalf of a managed UCITS, management companies must act in the best interests of the UCITS [organisation, Article 24(1)]. They must take all reasonable steps to obtain the best possible result, taking into account price, costs, speed, likelihood of execution and settlement, order size and nature, or any other relevant consideration [organisation, Article 24(2)]. 

To comply with this obligation, management companies must establish and implement effective arrangements and an execution policy that allows them to obtain the best possible result, and they must obtain the prior consent of the investment company to this execution policy [organisation, Article 25(3)]. Furthermore, management companies must regularly monitor the effectiveness of their arrangements and policy, review the execution policy annually (or upon a material change), and be able to demonstrate that they executed orders in accordance with that policy [organisation, Article 25(4) and (5)].

*Please note that this answer reflects the indexed text of Commission Directive 2010/43/EU and later amendments are not considered.*

<details><summary>Retrieved passages</summary>

```
[organisation, Article 24 to Article 25] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.77)
the unit-holder, at least once every 6 months, with the information listed in paragraph 2 in respect of those transactions. 4. Management companies shall supply the unit-holder, upon request, with information about the status of his order. Execution of decisions to deal on behalf of the managed UCITS 1. Member States shall require management companies to act in the best interests of the UCITS they manage when executing decisions to deal on behalf of the managed UCITS in the context of the management of their portfolios. 2. For the purposes of paragraph 1, Member States shall ensure that management companies take all reasonable steps to obtain the best possible result for the UCITS, taking into account price, costs, speed, likelihood of execution and settlement, order size and nature, or any other consideration relevant to the execution of the order. The relative importance of such factors shall be determined by reference to the following criteria: (a) the objectives, investment policy and risks specific to the UCITS, as indicated in the prospectus or as the case may be in the fund rules or articles of association of the UCITS; (b) the characteristics of the order; (c) the characteristics of the financial instruments

---

[organisation, Article 25] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.75)
risks specific to the UCITS, as indicated in the prospectus or as the case may be in the fund rules or articles of association of the UCITS; (b) the characteristics of the order; (c) the characteristics of the financial instruments that are the subject of that order; (d) the characteristics of the execution venues to which that order can be directed. 3. Member States shall require management companies to establish and implement effective arrangements for complying with the obligation referred to in paragraph 2. In particular, management companies shall establish and implement a policy to allow them to obtain, for UCITS orders, the best possible result in accordance with paragraph 2. Management companies shall obtain the prior consent of the investment company on the execution policy. The management company shall make available appropriate information to unit-holders on the policy established in accordance with this Article and on any material changes to their policy. 4. Management companies shall monitor on a regular basis the effectiveness of their arrangements and policy for the execution of orders in order to identify and, where appropriate, correct any deficiencies. In addition, management companies shall review the execution policy on an annual basis. A review shall

---

[organisation, Article 26 to Article 27] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.75)
2 and, in particular, the execution quality of the entities identified in that policy and, where appropriate, correct any deficiencies. In addition, management companies shall review the policy on an annual basis. Such a review shall also be carried out whenever a material change occurs that affects the management company’s ability to continue to obtain the best possible result for the managed UCITS. 4. Management companies shall be able to demonstrate that they have placed orders on behalf of the UCITS in accordance with the policy established in accordance with paragraph 2. General principles 1. Member States shall require management companies to establish and implement procedures and arrangements which provide for the prompt, fair and expeditious execution of portfolio transactions on behalf of the UCITS. The procedures and arrangements implemented by management companies shall satisfy the following conditions: (a) ensure that orders executed on behalf of UCITS are promptly and accurately recorded and allocated; (b) execute otherwise comparable UCITS orders sequentially and promptly unless the characteristics of the order or prevailing market conditions make this impracticable, or the interests of the UCITS require otherwise. Financial instruments or sums of money, received in settlement of the executed orders shall be promptly

---

[organisation, Article 26] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.75)
steps to obtain the best possible result for the UCITS taking into account price, costs, speed, likelihood of execution and settlement, size, nature or any other consideration relevant to the execution of the order. The relative importance of such factors shall be determined by reference to Article 25(2). For those purposes, management companies shall establish and implement a policy to enable them to comply with the obligation referred to in the first subparagraph. The policy shall identify, in respect of each class of instruments, the entities with which the orders may be placed. The management company shall only enter into arrangements for execution where such arrangements are consistent with obligations laid down in this Article. Management companies shall make available to unit-holders appropriate information on the policy established in accordance with this paragraph and on any material changes to this policy. 3. Management companies shall monitor on a regular basis the effectiveness of the policy established in accordance with paragraph 2 and, in particular, the execution quality of the entities identified in that policy and, where appropriate, correct any deficiencies. In addition, management companies shall review the policy on an annual basis. Such a review shall also be carried out

---

[organisation, Article 25 to Article 26] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.75)
regular b
```
</details>

## q23 (single)
**Question:** Can a management company accept fees or commissions from third parties in connection with managing a UCITS?
**Reference:** Only in limited cases: the payment must be clearly disclosed to the UCITS, designed to enhance the quality of the service, and not impair the duty to act in the UCITS's best interest (fees paid by the UCITS itself and proper fees such as custody costs are also allowed).

**Agent answer:**

A management company is generally prohibited from paying or receiving fees, commissions, or non-monetary benefits in relation to the investment management and administration of a UCITS, as this is considered a failure to act honestly, fairly, and professionally in the best interests of the UCITS [organisation, Article 29(1)].

However, a management company may accept such payments from a third party if the following conditions are met:
*   **Disclosure:** The existence, nature, and amount of the fee, commission, or benefit (or the method of calculation if the amount cannot be ascertained) must be clearly disclosed to the UCITS in a comprehensive, accurate, and understandable manner prior to the provision of the service [organisation, Article 29(1)(b)(i)].
*   **Quality Enhancement:** The payment must be designed to enhance the quality of the relevant service and must not impair the management company's duty to act in the best interests of the UCITS [organisation, Article 29(1)(b)(ii)].

Additionally, "proper fees" that are necessary for the provision of the service (such as custody costs, settlement and exchange fees, regulatory levies, or legal fees) are permitted, provided they are of a nature that cannot give rise to conflicts with the management company's duties to act in the best interests of the UCITS [organisation, Article 29(1)(c)].

Please note that these rules are based on the 2010 organisational requirements; later amendments to EU law may have introduced further restrictions or requirements.

<details><summary>Retrieved passages</summary>

```
[organisation, Article 29] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.79)
fee, commission or non-monetary benefit paid or provided to or by a third party or a person acting on behalf of a third party, where the following conditions are satisfied: (i) the existence, nature and amount of the fee, commission or benefit, or, where the amount cannot be ascertained, the method of calculating that amount, must be clearly disclosed to the UCITS in a manner that is comprehensive, accurate and understandable, prior to the provision of the relevant service; (ii) the payment of the fee or commission, or the provision of the non-monetary benefit must be designed to enhance the quality of the relevant service and not impair compliance with the management company’s duty to act in the best interests of the UCITS; (c) proper fees which enable or are necessary for the provision of the relevant service, including custody costs, settlement and exchange fees, regulatory levies or legal fees, and which, by their nature, cannot give rise to conflicts with the management company’s duties to act honestly, fairly and professionally in accordance with the best interests of the UCITS. 2. Member States shall permit a management company, for the purposes of paragraph 1(b)(i), to disclose the essential terms of

---

[organisation, Article 28 to Article 29] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.76)
in priority over those for own account. However, if the management company is able to demonstrate to the UCITS or its other client on reasonable grounds that it would not have been able to carry out the order on such advantageous terms without aggregation, or at all, it may allocate the transaction for own account proportionally, in accordance with the policy as referred to in paragraph 1(b). Safeguarding the best interests of UCITS 1. Member States shall ensure that management companies are not regarded as acting honestly, fairly and professionally in accordance with the best interests of the UCITS if, in relation to the activities of investment management and administration to the UCITS, they pay or are paid any fee or commission, or provide or are provided with any non-monetary benefit, other than the following: (a) a fee, commission or non-monetary benefit paid or provided to or by the UCITS or a person on behalf of the UCITS; (b) a fee, commission or non-monetary benefit paid or provided to or by a third party or a person acting on behalf of a third party, where the following conditions are satisfied: (i) the existence, nature and amount of the fee, commission

---

[ucits_directive, Article 55 to Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
of the limits laid down in Article 52. 3. Where a UCITS invests in the units of other UCITS or collective investment undertakings that are managed, directly or by delegation, by the same management company or by any other company with which the management company is linked by common management or control, or by a substantial direct or indirect holding, that management company or other company shall not charge subscription or redemption fees on account of the UCITS’ investment in the units of such other UCITS or collective investment undertakings. A UCITS that invests a substantial proportion of its assets in other UCITS or collective investment undertakings shall disclose in its prospectus the maximum level of the management fees that may be charged both to the UCITS itself and to the other UCITS or collective investment undertakings in which it intends to invest. It shall indicate in its annual report the maximum proportion of management fees charged both to the UCITS itself and to the other UCITS or collective investment undertaking in which it invests. 1. An investment company or a management company acting in connection with all of the common funds which it manages and which fall within the

---

[organisation, Recitals] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.74)
of the UCITS, management companies should take all reasonable steps to obtain the best possible result for the UCITS on a consistent basis, taking into account price, costs, speed, likelihood of execution and settlement, size and nature of the order or any other consideration relevant to the execution of the order. (20) In order to ensure that management companies act with due skill, care and diligence in the best interests of the UCITS they manage as required by 2009/65/EC Directive, it is necessary to lay down rules on order handling. (21) Certain fees, commissions or non-monetary benefits which may be paid to or by a management company should not be permitted as they could have an impact on the observance of the requirements laid down in 2009/65/EC Directive that the management company should act honestly, fairly and professionally in accordance with the best interests of the UCITS. Therefore, it is necessary to set out clear rules specifying where the payments of fees, commissions and non-monetary benefits are not considered a violation of those principles. (22) The cross-border activities of the management company create new challenges for the relationship between the management company and the UCITS’ depositary. To ensure the necessary

---

[ucits_directive, Article 8 to Article 10] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
shall be consulted beforehand in relation to the authorisation of any management company which is one of the following: (a) a subsidiary of another management company, an investment firm, a credit institution or an insurance undertaking authorised in another Member State; (b) a subsidiary of the parent undertaking of another management company, an investment firm, a credit institution or an insurance undertaking authorised in another M
```
</details>

## q24 (single)
**Question:** What is the maximum length of the key investor information document?
**Reference:** It must not exceed two pages of A4-sized paper when printed.

**Agent answer:**

The key investor information document shall not exceed two pages of A4-sized paper when printed [kiid, Article 5 to Article 7].

For structured UCITS, the key investor information document shall not exceed three pages of A4-sized paper when printed [kiid, Article 37 to Article 38].

Please note that these rules are based on Commission Regulation (EU) No 583/2010 and later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[kiid, Article 5 to Article 7] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.81)
A key investor information document shall be: (a) presented and laid out in a way that is easy to read, using characters of readable size; (b) clearly expressed and written in language that communicates in a way that facilitates the investor's understanding of the information being communicated, in particular where: (i) the language used is clear, succinct and comprehensible; (ii) the use of jargon is avoided; (iii) technical terms are avoided when everyday words can be used instead; (c) focused on the key information that investors need. 2. Where colours are used, they shall not diminish the comprehensibility of the information in the event that the key investor information document is printed or photocopied in black and white. 3. Where the design of the corporate branding of the management company or the group to which it belongs is used, it shall not distract the investor or obscure the text. Length The key investor information document shall not exceed two pages of A4-sized paper when printed. Specific contents of the description 1. The description contained in the ‘Objectives and investment policy’ section of the key investor information document shall cover those essential features of the UCITS about which an investor should

---

[kiid, Article 37 to Article 38] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.77)
The key investor information document for structured UCITS shall not exceed three pages of A4-sized paper when printed. Conditions applying to the provision of a key investor information document or a prospectus in a durable medium other than paper or by means of a website 1. Where, for the purposes of Directive 2009/65/EC, the key investor information document or prospectus is to be provided to investors using a durable medium other than paper the following conditions shall be met: (a) the provision of the key investor information document or the prospectus using such a durable medium is appropriate to the context in which the business between the management company and the investor is, or is to be, carried on; and (b) the person to whom the key investor information document or the prospectus is to be provided, when offered the choice between information on paper or in that other durable medium, specifically chooses that other medium. 2. Where the key investor information document or the prospectus is to be provided by means of a website and that information is not addressed personally to the investor, the following conditions shall also be satisfied: (a) the provision of that information in that

---

[kiid, Article 36 to Article 38] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.74)
the formula. They shall be presented in a way that is fair, clear and not misleading, and that is likely to be understood by the average retail investor. In particular, they shall not artificially magnify the importance of the final performance of the UCITS. 5. The scenarios referred to in paragraph 3 shall be based on reasonable and conservative assumptions about future market conditions and price movements. However, whenever the formula exposes investors to the possibility of substantial losses, such as a capital guarantee that functions only under certain circumstances, these losses shall be appropriately illustrated, even if the probability of the corresponding market conditions is low. 6. The scenarios referred to in paragraph 3 shall be accompanied by a statement that they are examples that are included to illustrate the formula, and do not represent a forecast of what might happen. It shall be made clear that the scenarios shown may not have an equal probability of occurrence. Length The key investor information document for structured UCITS shall not exceed three pages of A4-sized paper when printed. Conditions applying to the provision of a key investor information document or a prospectus in a durable medium other than paper or

---

[kiid, Article 4] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.74)
Title and content of document 1. The content of the key investor information document shall be presented in the order as set out in paragraphs 2 to 13. 2. The title ‘Key investor information’ shall appear prominently at the top of the first page of the key investor information document. 3. An explanatory statement shall appear directly underneath the title. It shall read: ‘This document provides you with key investor information about this fund. It is not marketing material. The information is required by law to help you understand the nature and the risks of investing in this fund. You are advised to read it so you can make an informed decision about whether to invest’. 4. The identification of the UCITS, including the share class or investment compartment thereof, shall be stated prominently. In the case of an investment compartment or share class, the name of the UCITS shall follow the compartment or share class name. Where a code number identifying the UCITS, investment compartment or share class exists, it shall form part of the identification of the UCITS. 5. The name of the management company shall be stated. 6. In addition, in cases where the management company forms

---

[kiid, Article 20] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.73)
1. The ‘Practical information’ section of the key investor information document shall contain the following information relevant to investors in every Member State in which the UCITS is marketed: (a) the name of the depositary; (b) where and how to obtain further information about the UCITS, copies of its prospectus and its latest annual report and any subsequent half-yearly report, stating in which language(s) those documents are available, and that they may be obtained free of charge; (c) where and h
```
</details>

## q25 (single)
**Question:** How is past performance presented in the key investor information?
**Reference:** As a bar chart covering the past performance of the UCITS over the last 10 years.

**Agent answer:**

Past performance in the key investor information document (KIID) is presented as a bar chart covering the last 10 years, or the last 5 years for UCITS with less than 5 complete calendar years of performance [kiid, Article 15]. The chart must not exceed half a page and must be legible [kiid, Article 15].

Key requirements for the presentation include:
*   **Calculation:** Figures are based on net asset value, assuming distributable income is reinvested [kiid, Article 18].
*   **Chart Formatting:** The Y-axis scale must be linear and adapted to the span of the bars to ensure fluctuations are distinguishable; the X-axis must be set at 0% performance [kiid, Annex II, Annex III]. Each bar must be labeled with the percentage return achieved, rounded to one decimal place [kiid, Annex II, Annex III].
*   **Benchmarks:** If the "Objectives and investment policy" section references a benchmark, a bar showing the benchmark's performance must be included alongside each bar showing the UCITS' performance [kiid, Article 18].
*   **Material Changes:** If a material change to objectives and investment policy occurs, past performance prior to the change must still be shown, but the period must be clearly labeled with a warning that the performance was achieved under circumstances that no longer apply [kiid, Article 18].
*   **Restrictions:** The document must not contain past performance for any part of the current calendar year [kiid, Article 18]. Years for which data is unavailable must be shown as blank [kiid, Article 15].

Please note that these rules are based on Commission Regulation (EU) No 583/2010; later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[kiid, Article 15 to Article 18] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.76)
have entry or exit charges. 6. A key investor information document shall not contain any record of past performance for any part of the current calendar year. Past performance calculation methodology The calculation of past performance figures shall be based on the net asset value of the UCITS, and they shall be calculated on the basis that any distributable income of the fund has been reinvested. Impact and treatment of material changes 1. Where a material change occurs to a UCITS’ objectives and investment policy during the period displayed in the bar chart referred to in Article 15, the UCITS’ past performance prior to that material change shall continue to be shown. 2. The period prior to the material change referred to in paragraph 1 shall be indicated on the bar chart and labelled with a clear warning that the performance was achieved under circumstances that no longer apply. Use of a benchmark alongside the past performance 1. Where the ‘Objectives and investment policy’ section of the key investor information document makes reference to a benchmark, a bar showing the performance of that benchmark shall be included in the chart alongside each bar showing the UCITS’ past performance. 2. For

---

[kiid, Article 4 to Article 5] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.75)
information set out in Section 3 of Chapter III of this Regulation. 10. The section of the key investor information document entitled ‘Past performance’ shall contain the information set out in Section 4 of Chapter III of this Regulation. 11. The section of the key investor information document entitled ‘Practical information’ shall contain the information set out in Section 5 of Chapter III of this Regulation. 12. Authorisation details shall consist of the following statement: ‘This fund is authorised in [name of Member State] and regulated by [identity of competent authority]’. In cases where the UCITS is managed by a management company exercising rights under Article 16 of Directive 2009/65/EC, an additional statement shall be included: ‘[Name of management company] is authorised in [name of Member State] and regulated by [identity of competent authority]’. 13. Information on publication shall consist of the following statement: ‘This key investor information is accurate as at [the date of publication]’. Presentation and language 1. A key investor information document shall be: (a) presented and laid out in a way that is easy to read, using characters of readable size; (b) clearly expressed and written in language that communicates in a way that facilitates the

---

[kiid, Annex II to Annex III] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.75)
% This is the maximum that might be taken out of your money [before it is invested] [before the proceeds of your investment are paid out] Charges taken from the fund over a year Ongoing charge [] % Charges taken from the fund under certain specific conditions Performance fee [] % a year of any returns the fund achieves above the benchmark for these fees, the [insert name of benchmark] — A percentage amount shall be indicated for each of these charges. — In the case of a performance fee, the amount charged in the fund’s last financial year shall be included as a percentage figure. PRESENTATION OF THE PAST PERFORMANCE INFORMATION The bar chart presenting past performance shall comply with the following criteria: 1. the scale of the Y-axis of the bar chart shall be linear, not logarithmic; 2. the scale shall be adapted to the span of the bars shown and shall not compress the bars so as to make fluctuations in returns harder to distinguish; 3. the X-axis shall be set at the level of 0 % performance; 4. a label shall be added to each bar indicating the return in percentage that was achieved; 5. past

---

[kiid, Annex III] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.74)
to make fluctuations in returns harder to distinguish; 3. the X-axis shall be set at the level of 0 % performance; 4. a label shall be added to each bar indicating the return in percentage that was achieved; 5. past performance figures shall be rounded to one decimal place.

---

[kiid, Article 13 to Article 15] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.74)
where instead that figure shall be displayed; (b) for funds which set a cap or maximum on the amount that can be charged, where instead that figure shall be disclosed so long as the management company gives a commitment to respect the published figure and to absorb any costs that would otherwise cause it to be exceeded. Cross-referencing The ‘Charges’ section shall include, where relevant, a cross-reference to those parts of the UCITS prospectus where more detailed information on charges can be found, including information on performance fees and how they are calculated. Presentation of past performance 1. The information about the past performance of the UCITS shall be presented in a bar chart covering the performance of the UCITS for the last 10 years. The size of the bar chart referred to in the first subparagraph shall allow for legibility, but shall under no circumstances exceed half a page in the key investor information document. 2. UCITS with performance of less than 5 complete calendar years shall use a presentation covering the last 5 years only. 3. For any years for which data is not available, the year shall be shown as blank with no annotation other than the
```
</details>

## q26 (single)
**Question:** What must the risk and reward section of the key investor information contain?
**Reference:** A synthetic indicator, a narrative explanation of the indicator and its main limitations, and a description of material risks not adequately captured by the indicator.

**Agent answer:**

I don't know. The indexed UCITS documents do not answer this question; please check with the legal or compliance team.

<details><summary>Retrieved passages</summary>

```
[kiid, Article 7 to Article 8] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.79)
plan to withdraw their money within [period of time]’. 3. Information included under paragraphs 1 and 2 shall distinguish between the broad categories of investments as specified under paragraphs 1(a), (c) and 2(a) and the approach to these investments to be adopted by a management company as specified under paragraphs 1(d) and 2 (b), (c) and (d). 4. The ‘Objectives and investment policy’ section of the key investor information document may contain elements other than those listed in paragraph 2, including the description of the UCITS’ investment strategy, where these elements are necessary to adequately describe the objectives and investment policy of the UCITS. Explanation of potential risks and rewards, including the use of an indicator 1. The ‘Risk and reward profile’ section of the key investor information document shall contain a synthetic indicator, supplemented by: (a) a narrative explanation of the indicator and its main limitations; (b) a narrative explanation of risks which are materially relevant to the UCITS and which are not adequately captured by the synthetic indicator. 2. The synthetic indicator referred to in paragraph 1 shall take the form of a series of categories on a numerical scale with the UCITS assigned to one of the

---

[kiid, Article 8] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.76)
that the risk and reward category shown is not guaranteed to remain unchanged and that the categorisation of the UCITS may shift over time; (c) a statement that the lowest category does not mean a risk-free investment; (d) a brief explanation as to why the UCITS is in a specific category; (e) details of the nature, timing and extent of any capital guarantee or protection offered by the UCITS, including the potential effects of redeeming units outside of the guaranteed or protected period. 5. The narrative explanation referred to in paragraph 1(b) shall include the following categories of risks, where these are material: (a) credit risk, where a significant level of investment is made in debt securities; (b) liquidity risk, where a significant level of investment is made in financial instruments, which are by their nature sufficiently liquid, yet which may under certain circumstances have a relatively low level of liquidity, so as to have an impact on the level of liquidity risk of the UCITS as a whole; (c) counterparty risk, where a fund is backed by a guarantee from a third party, or where its investment exposure is obtained to a material degree through one or more contracts

---

[ucits_directive, Article 78] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
Key investor information shall include appropriate information about the essential characteristics of the UCITS concerned, which is to be provided to investors so that they are reasonably able to understand the nature and the risks of the investment product that is being offered to them and, consequently, to take investment decisions on an informed basis. 3. Key investor information shall provide information on the following essential elements in respect of the UCITS concerned: (a) identification of the UCITS; (b) a short description of its investment objectives and investment policy; (c) past-performance presentation or, where relevant, performance scenarios; (d) costs and associated charges; and (e) risk/reward profile of the investment, including appropriate guidance and warnings in relation to the risks associated with investments in the relevant UCITS. Those essential elements shall be comprehensible to the investor without any reference to other documents. 4. Key investor information shall clearly specify where and how to obtain additional information relating to the proposed investment, including but not limited to where and how the prospectus and the annual and half-yearly report can be obtained on request and free of charge at any time, and the language in which such information is available to investors. 5.

---

[kiid, Recitals] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.73)
and risks which are not captured by the indicator, but which may have a material impact on the risk and reward profile of the UCITS. In applying the rules on the synthetic indicator account should be taken of the methodology for the calculation of the synthetic indicator as developed by competent authorities working within the Committee of European Securities Regulators. The management company should decide on a case-by-case basis which specific risks should be disclosed by analysing the particular characteristics of each fund, bearing in mind the need to avoid over-burdening the document with information that retail investors will find difficult to understand. In addition the narrative explanation of the risk and reward profile should be limited in size in terms of the amount of space it occupies within the key investor information document. It should be possible to have cross-references to the prospectus of the UCITS where full details of its risks are disclosed. (7) Consistency should be ensured between the explanation of risks in the key investor information document and the management company’s internal processes related to risk management, established in accordance with Commission Directive 2010/43/EU of 1 July 2010 implementing Directive 2009/65/EC of the European Parliament and

---

[kiid, Recitals] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.72)
This Regulation specifies the content of the information on investment objectives and the investment policy of UCITS so that investors can easily see whether or not a fund is likely to be suitable for their needs. For this reason, the information should indicate whether returns can be expected in the form of capital growth, payment of income, or a combination of both. T
```
</details>

## q27 (single)
**Question:** How must charges be presented in the key investor information?
**Reference:** In a table showing one-off charges taken before or after investing (entry and exit charges), charges taken over the year (ongoing charges) and charges taken under specific conditions such as performance fees.

**Agent answer:**

The 'Charges' section in the key investor information document must present charges using a table showing entry and exit charges (as maximum percentages), a single ongoing charges figure based on the preceding year, and any specific charges (such as performance fees) taken under certain conditions [kiid, Article 10]. This table must be accompanied by a narrative explanation clarifying that entry and exit charges are maximum figures, stating that ongoing charges are based on the last year's expenses and may vary, and explaining that charges are used to cover running and distribution costs and reduce potential growth [kiid, Article 11]. All elements of the charging structure must be presented as clearly as possible to allow investors to consider their combined impact, including cross-references to the prospectus where appropriate [kiid, Article 11, kiid, Article 13].

*Note: This answer is based on the indexed texts from Commission Regulation (EU) No 583/2010 (key investor information); later amendments are not reflected unless explicitly added to the corpus.*

<details><summary>Retrieved passages</summary>

```
[kiid, Article 10 to Article 11] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.79)
‘Charges’ section of the key investor information document shall contain a presentation of charges in the form of a table as laid down in Annex II. 2. The table referred to in paragraph 1 shall be completed in accordance with the following requirements: (a) entry and exit charges shall each be the maximum percentage which might be deducted from the investor’s capital commitment to the UCITS; (b) a single figure shall be shown for charges taken from the UCITS over a year, to be known as the ‘ongoing charges,’ representing all annual charges and other payments taken from the assets of the UCITS over the defined period, and based on the figures for the preceding year; (c) the table shall list and explain any charges taken from the UCITS under certain specific conditions, the basis on which the charge is calculated, and when the charge applies. Explanation of charges and a statement about the importance of charges 1. The ‘Charges’ section shall contain a narrative explanation of each of the charges specified in the table including the following information: (a) with regard to entry and exit charges: (i) it shall be made clear that the charges are always maximum figures,

---

[kiid, Article 11 to Article 12] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.78)
section shall contain a narrative explanation of each of the charges specified in the table including the following information: (a) with regard to entry and exit charges: (i) it shall be made clear that the charges are always maximum figures, as in some cases the investor might pay less; (ii) a statement shall be included stating that the investor can find out the actual entry and exit charges from their financial adviser or distributor; (b) with regard to ‘ongoing charges’, there shall be a statement that the ongoing charges figure is based on the last year’s expenses, for the year ending [month/year], and that this figure may vary from year to year where this is the case. 2. The ‘Charges’ section shall contain a statement about the importance of charges which shall make clear that the charges an investor pays are used to pay the costs of running the UCITS, including the costs of marketing and distributing the UCITS, and that these charges reduce the potential growth of the investment. Additional requirements 1. All of the elements of the charging structure shall be presented as clearly as possible to allow investors to consider the combined impact of the charges. 2.

---

[kiid, Article 11 to Article 13] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.77)
that these charges reduce the potential growth of the investment. Additional requirements 1. All of the elements of the charging structure shall be presented as clearly as possible to allow investors to consider the combined impact of the charges. 2. Where the impact of portfolio transaction costs on returns is likely to be material due to the strategy adopted by the UCITS, this shall be stated within the ‘Objectives and investment policy’ section, as indicated in Article 7(2)(e). 3. Performance fees shall be disclosed in accordance with Article 10(2)(c). The amount of the performance fee charged during the UCITS’ last financial year shall be included as a percentage figure. Specific cases 1. Where a new UCITS cannot comply with the requirements contained in Article 10(2)(b) and Article 11(1)(b), the ongoing charges shall be estimated, based on the expected total of charges. 2. Paragraph 1 shall not apply in the following cases: (a) for funds which charge a fixed all-inclusive fee, where instead that figure shall be displayed; (b) for funds which set a cap or maximum on the amount that can be charged, where instead that figure shall be disclosed so long as the management company gives a commitment to

---

[kiid, Annex II to Annex III] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.76)
% This is the maximum that might be taken out of your money [before it is invested] [before the proceeds of your investment are paid out] Charges taken from the fund over a year Ongoing charge [] % Charges taken from the fund under certain specific conditions Performance fee [] % a year of any returns the fund achieves above the benchmark for these fees, the [insert name of benchmark] — A percentage amount shall be indicated for each of these charges. — In the case of a performance fee, the amount charged in the fund’s last financial year shall be included as a percentage figure. PRESENTATION OF THE PAST PERFORMANCE INFORMATION The bar chart presenting past performance shall comply with the following criteria: 1. the scale of the Y-axis of the bar chart shall be linear, not logarithmic; 2. the scale shall be adapted to the span of the bars shown and shall not compress the bars so as to make fluctuations in returns harder to distinguish; 3. the X-axis shall be set at the level of 0 % performance; 4. a label shall be added to each bar indicating the return in percentage that was achieved; 5. past

---

[kiid, Article 13 to Article 15] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.75)
where instead that figure shall be displayed; (b) for funds which set a cap or maximum on the amount that can be charged, where instead that figure shall be disclosed so long as the management company gives a commitment to respect the published figure and to absorb any costs that would otherwise cause it to be exceeded. Cross-referencing The ‘Charges’ section shall include, where relevant, a cross-reference to those parts of the UCITS prospectus where more detailed information on charges can be found, including information on performance fees and how they are calculated. Presentation of past performance 1. The information about the past performance of the UCITS shall be presented in a 
```
</details>

## q28 (multi)
**Question:** Our UCITS wants to invest 50% of its assets in German government bonds. Is that allowed?
**Reference:** Normally the limit for government-issued securities is 35%. Up to 100% is only possible if authorised under the derogation: at least six different issues, no single issue above 30% of total assets, and stated in the fund rules.

**Agent answer:**

Yes, investing 50% of a UCITS' assets in German government bonds is allowed, provided specific conditions are met:

* **General Limit or Derogation:** By default, Member States may allow UCITS to invest up to 35% of their assets in transferable securities issued or guaranteed by a Member State [ucits_directive, Article 52(3)]. Furthermore, by way of derogation, Member States may authorize a UCITS to invest up to 100% of its assets in different transferable securities issued or guaranteed by a Member State, provided that unit-holder protection is equivalent to that of UCITS complying with standard diversification limits [ucits_directive, Article 54(1)].
* **Issue and Diversification Conditions:** If utilizing the 100% derogation, the UCITS must hold securities from at least six different issues, and securities from any single issue shall not account for more than 30% of its total assets [ucits_directive, Article 54(1)].
* **Fund Rules and Prospectus Disclosures:** The fund rules or instruments of incorporation must explicitly mention the intention to invest more than 35% of assets in securities issued or guaranteed by Germany, and this must be approved by the competent authorities [ucits_directive, Article 54(2)]. Additionally, a prominent statement must be included in the prospectus and marketing communications drawing attention to this authorization [ucits_directive, Article 54(3)].

*Note: This answer reflects solely the provisions of Directive 2009/65/EC (UCITS Directive) as indexed in the corpus; subsequent national transpositions or EU amendments may impose additional requirements.*

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 53 to Article 54] Directive 2009/65/EC (UCITS Directive) (relevance 0.77)
certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it is published in an appropriate manner. 2. Member States may raise the limit laid down in paragraph 1 to a maximum of 35 % where that proves to be justified by exceptional market conditions in particular in regulated markets where certain transferable securities or money market instruments are highly dominant. The investment up to that limit shall be permitted only for a single issuer. 1. By way of derogation from Article 52, Member States may authorise UCITS to invest in accordance with the principle of risk-spreading up to 100 % of their assets in different transferable securities and money market instruments issued or guaranteed by a Member State, one or more of its local authorities, a third country, or a public international body to which one or more Member States belong. The competent authorities of the UCITS home Member State shall grant such a derogation only if they consider that unit-holders in the UCITS have protection equivalent to that of

---

[ucits_directive, Article 54] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
public international body to which one or more Member States belong. The competent authorities of the UCITS home Member State shall grant such a derogation only if they consider that unit-holders in the UCITS have protection equivalent to that of unit-holders in UCITS complying with the limits laid down in Article 52. Such a UCITS shall hold securities from at least six different issues, but securities from any single issue shall not account for more than 30 % of its total assets. 2. The UCITS referred to in paragraph 1 shall make express mention in the fund rules or in the instruments of incorporation of the investment company of the Member States, local authorities, or public international bodies issuing or guaranteeing securities in which they intend to invest more than 35 % of their assets. Such fund rules or instruments of incorporation shall be approved by the competent authorities. 3. Each UCITS referred to in paragraph 1 shall include a prominent statement in its prospectus and marketing communications drawing attention to such authorisation and indicating the Member States, local authorities, or public international bodies in the securities of which it intends to invest or has invested more than 35 %

---

[ucits_directive, Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
issuing body. The limits laid down in points (b), (c) and (d) may be disregarded at the time of acquisition if at that time the gross amount of the debt securities or of the money market instruments, or the net amount of the securities in issue, cannot be calculated. 3. A Member State may waive the application of paragraphs 1 and 2 as regards: (a) transferable securities and money market instruments issued or guaranteed by a Member State or its local authorities; (b) transferable securities and money market instruments issued or guaranteed by a third country; (c) transferable securities and money market instruments issued by a public international body to which one or more Member States belong; (d) shares held by a UCITS in the capital of a company incorporated in a third country investing its assets mainly in the securities of issuing bodies having their registered offices in that country, where under the legislation of that country such a holding represents the only way in which the UCITS can invest in the securities of issuing bodies of that country; or (e) shares held by an investment company or investment companies in the capital of subsidiary companies pursuing only the

---

[ucits_directive, Recitals] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
general obligation to act solely in the interests of unit-holders and, in particular, the objective of increasing cost efficiencies, never justify a UCITS undertaking measures that could hinder the competent authorities from effectively exercising their supervisory functions. (49) The original version of Directive 85/611/EEC contained a derogation from the restriction on the percentage of its assets that a UCITS can invest in transferable securities issued by the same body, which applied in the case of bonds issued or guaranteed by a Member State. That derogation allowed UCITS to invest, in particular, up to 35 % of their assets in such bonds. A similar but more limited derogation is justified with regard to private sector bonds which, even in the absence of a State guarantee, offer special guarantees to the investor under the specific rules applicable thereto. It is necessary, therefore, to extend the derogation to the totality of private sector bonds which fulfil jointly fixed criteria, while leaving it to the Member States to draw up the list of bonds to which they intend, where appropriate, to grant a derogation. (50) Several Member States have enacted provisions that enable non-coordinated collective investment undertakings to pool their assets in one so-called

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member Stat
```
</details>

## q29 (multi)
**Question:** Can a UCITS buy a listed share whose price cannot be valued reliably?
**Reference:** No. Listed transferable securities are eligible under the UCITS Directive only if they also meet the eligibility criteria of Directive 2007/16/EC, which include reliable valuation.

**Agent answer:**

No, a UCITS cannot buy such a security. To be classified as an eligible transferable security, a financial instrument must have a reliable valuation available for it [eligible_assets, Article 2]. For securities admitted to or dealt in on a regulated market, this requires accurate, reliable, and regular prices in the form of market prices or prices made available by valuation systems independent from issuers [eligible_assets, Article 2].

Please note that this answer reflects the indexed versions of the original 2007–2010 EU UCITS texts (specifically Commission Directive 2007/16/EC), and later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.70)
Directive 85/611/EEC to transferable securities shall be understood as a reference to financial instruments which fulfil the following criteria: (a) the potential loss which the UCITS may incur with respect to holding those instruments is limited to the amount paid for them; (b) their liquidity does not compromise the ability of the UCITS to comply with Article 37 of Directive 85/611/EEC; (c) reliable valuation is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1) of Directive 85/611/EEC, in the form of accurate, reliable and regular prices which are either market prices or prices made available by valuation systems independent from issuers; (ii) in the case of other securities as referred to in Article 19(2) of Directive 85/611/EEC, in the form of a valuation on a periodic basis which is derived from information from the issuer of the security or from competent investment research; (d) appropriate information is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1)

---

[eligible_assets, Article 4 to Article 5] Commission Directive 2007/16/EC (eligible assets) (relevance 0.68)
a net asset value in accordance with the value at which the financial instrument held in the portfolio could be exchanged between knowledgeable willing parties in an arm’s length transaction; (b) they are based either on market data or on valuation models including systems based on amortised costs. 3. The criteria referred to in paragraphs 1 and 2 shall be presumed to be fulfilled in the case of financial instruments which are normally dealt in on the money market for the purposes of Article 1(9) of Directive 85/611/EEC and which are admitted to, or dealt in on, a regulated market in accordance with points (a), (b) or (c) of Article 19(1) thereof, unless there is information available to the UCITS that would lead to a different determination. Article 19(1)(h) of Directive 85/611/EEC Instruments of which the issue or issuer is regulated for the purpose of protecting investors and savings 1. The reference in Article 19(1)(h) of Directive 85/611/EEC to money market instruments, other than those dealt in on a regulated market, of which the issue or the issuer is itself regulated for the purpose of protecting investors and savings, shall be understood as a reference to financial instruments which fulfil

---

[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.68)
there is information available to the UCITS that would lead to a different determination, financial instruments which are admitted or dealt in on a regulated market in accordance with points (a), (b) or (c) of Article 19(1) of Directive 85/611/EEC shall be presumed not to compromise the ability of the UCITS to comply with Article 37 of Directive 85/611/EEC and shall also be presumed to be negotiable. 2. Transferable securities as referred to in Article 1(8) of Directive 85/611/EEC shall be taken to include the following: (a) units in closed end funds constituted as investment companies or as unit trusts which fulfil the following criteria: (i) they fulfil the criteria set out in paragraph 1; (ii) they are subject to corporate governance mechanisms applied to companies; (iii) where asset management activity is carried out by another entity on behalf of the closed end fund, that entity is subject to national regulation for the purpose of investor protection; (b) units in closed end funds constituted under the law of contract which fulfil the following criteria: (i) they fulfil the criteria set out in paragraph 1; (ii) they are subject to corporate governance mechanisms equivalent to those applied to companies as referred

---

[eligible_assets, Article 8] Commission Directive 2007/16/EC (eligible assets) (relevance 0.67)
laid down in the second and third indents of Article 19(1)(g) of Directive 85/611/EEC and in paragraphs 3 and 4 of this Article; (d) their risks are adequately captured by the risk management process of the UCITS, and by its internal control mechanisms in the case of risks of asymmetry of information between the UCITS and the counterparty to the credit derivative resulting from potential access of the counterparty to non-public information on firms the assets of which are used as underlyings by credit derivatives. 3. For the purposes of the third indent of Article 19(1)(g) of Directive 85/611/EEC, the reference to fair value shall be understood as a reference to the amount for which an asset could be exchanged, or a liability settled, between knowledgeable, willing parties in an arm’s length transaction. 4. For the purposes of the third indent of Article 19(1)(g) of Directive 85/611/EEC, the reference to reliable and verifiable valuation shall be understood as a reference to a valuation, by the UCITS, corresponding to the fair value as referred to in paragraph 3 of this Article, which does not rely only on market quotations by the counterparty and which fulfils the following criteria: (a) the basis

---

[eligible_assets, Article 2] Commission Directive 2007/16/EC (eligible assets) (relevance 0.67)
or from competent investment research; (d) appropriate information is available for them as follows: (i) in the case of securities admitted to or dealt in on a regulated market as referred to in points (a) to (d) of Article 19(1) of Directive 85/611/EEC, in the form of regular, accurate and comprehensive information to the market on the security or, where relevant, on the portfolio of the security; (ii) in the case of other securities as referred to in Article 19(2) of Directive 85/611/EEC, in the form of regular and accurate information to the UCITS on the security or, where relevant, on the portfolio of
```
</details>

## q30 (multi)
**Question:** How is the global exposure limit for derivatives defined and how must a management company calculate it?
**Reference:** Global exposure must not exceed the total net value of the portfolio; it is calculated with the commitment approach, the value at risk approach or another advanced risk measurement method.

**Agent answer:**

Management companies must ensure that a UCITS' global exposure relating to derivative instruments does not exceed the total net value of its portfolio [ucits_directive, Article 51(3)]. Global exposure must be calculated on at least a daily basis [organisation, Article 41(2)].

Management companies may calculate global exposure using the commitment approach, the value at risk (VaR) approach (defined as a measure of maximum expected loss at a given confidence level over a specific time period), or other advanced risk measurement methodologies that are appropriate given the UCITS' investment strategy, the types and complexities of the derivatives used, and their proportion in the portfolio [organisation, Article 41(3)]. 

If the commitment approach is used:
- It must be applied to all financial derivative instrument positions, including embedded derivatives, whether used for general investment policy, risk reduction, or efficient portfolio management [organisation, Article 42(1)].
- Each derivative position must be converted into the market value of an equivalent position in the underlying asset (standard commitment approach), or via an equivalent calculation method [organisation, Article 42(2)].
- Management companies may take account of netting and hedging arrangements if they do not disregard obvious and material risks and result in a clear reduction in risk exposure [organisation, Article 42(3)].
- Underlying exposure need not be included if the derivative does not generate incremental exposure [organisation, Article 42(4)], nor do temporary borrowing arrangements [organisation, Article 42(5)].
- Techniques and instruments such as repurchase agreements or securities lending used to generate additional leverage or market risk exposure must also be factored into the global exposure calculation [organisation, Article 41(4)].

*Note: This answer reflects the indexed versions of Directive 2009/65/EC and Commission Directive 2010/43/EU; later amendments are not included.*

<details><summary>Retrieved passages</summary>

```
[organisation, Article 42 to Article 43] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.77)
market value of an equivalent position in the underlying asset of that derivative (standard commitment approach). Member States may allow management companies to apply other calculation methods which are equivalent to the standard commitment approach. 3. Member States may allow a management company to take account of netting and hedging arrangements when calculating global exposure, where these arrangements do not disregard obvious and material risks and result in a clear reduction in risk exposure. 4. Where the use of financial derivative instruments does not generate incremental exposure for the UCITS, the underlying exposure need not be included in the commitment calculation. 5. Where the commitment approach is used, temporary borrowing arrangements entered into on behalf of the UCITS in accordance with Article 83 of Directive 2009/65/EC need not be included in the global exposure calculation. Counterparty risk and issuer concentration 1. Member States shall require management companies to ensure that counterparty risk arising from an over-the-counter (OTC) financial derivative instrument is subject to the limits set out in Article 52 of Directive 2009/65/EC. 2. When calculating the UCITS exposure to a counterparty in accordance with the limits as referred to in Article 52(1) of Directive 2009/65/EC, management companies shall use

---

[organisation, Article 41] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.76)
including embedded derivatives pursuant to the fourth subparagraph of Article 51(3) of Directive 2009/65/EC, which may not exceed the total of the UCITS net asset value; (b) the market risk of the UCITS portfolio. 2. Member States shall require management companies to calculate the UCITS global exposure on at least a daily basis. 3. Member States may allow management companies to calculate global exposure by using the commitment approach, the value at risk approach or other advanced risk measurement methodologies as may be appropriate. For the purposes of this provision, ‘value at risk’ shall mean a measure of the maximum expected loss at a given confidence level over a specific time period. Member States shall require management companies to ensure that the method selected to measure global exposure is appropriate, taking into account the investment strategy pursued by the UCITS and the types and complexities of the financial derivative instruments used, and the proportion of the UCITS portfolio which comprises financial derivative instruments. 4. Where a UCITS in accordance with Article 51(2) of Directive 2009/65/EC employs techniques and instruments including repurchase agreements or securities lending transactions in order to generate additional leverage or exposure to market risk, Member States shall

---

[organisation, Recitals] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.74)
such as limits on global exposure and exposure to counterparty risk are respected by the management companies. Therefore criteria should be laid down as to how the global exposure should be calculated and how counterparty risk should be calculated. (27) It is necessary in laying down such criteria that this Directive clarifies how the global exposure can be calculated, including by using the commitment approach, the value at risk approach or advanced risk measurement methodologies. It should also lay down the main elements of the methodology according to which the management company should calculate the counterparty risk. In applying those rules, account should be taken of the conditions under which those methodologies are used, including the principles to be applied to such collateral arrangements to reduce the UCITS’ exposure to counterparty risk as well as the use of the hedging and netting arrangements, as developed by competent authorities working within the Committee of European Securities Regulators. (28) According to Directive 2009/65/EC, management companies are obliged to employ a process for the accurate and independent assessment of the value of over-the-counter (OTC) derivatives. This Directive therefore lays down detailed rules for that process in accordance with Commission Directive 2007/16/EC of 19

---

[organisation, Article 41 to Article 42] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.74)
financial derivative instruments. 4. Where a UCITS in accordance with Article 51(2) of Directive 2009/65/EC employs techniques and instruments including repurchase agreements or securities lending transactions in order to generate additional leverage or exposure to market risk, Member States shall require management companies to take these transactions into consideration when calculating global exposure. Commitment approach 1. Where the commitment approach is used for the calculation of global exposure, Member States shall require management companies to apply this approach to all financial derivative instrument positions including embedded derivatives as referred to in the fourth subparagraph of Article 51(3) of Directive 2009/65/EC, whether used as part of the UCITS general investment policy, for purposes of risk reduction or for the purposes of efficient portfolio management as referred to in Article 51(2) of that Directive. 2. Where the commitment approach is used for the calculation of global exposure, Member States shall require management companies to convert each financial derivative instrument position into the market value of an equivalent position in the underlying asset of that derivative (standard commitment approach). Member States may allow management companies to apply other calculation methods which are equivalent 
```
</details>

## q31 (multi)
**Question:** What must the key investor information include and how long can it be?
**Reference:** A short document clearly titled 'key investor information' giving appropriate information about the essential characteristics of the UCITS, so investors can understand the nature and risks of the product; it must not exceed two pages of A4 paper when printed.

**Agent answer:**

I don't know. The indexed UCITS documents do not answer this question; please check with the legal or compliance team.

<details><summary>Retrieved passages</summary>

```
[kiid, Article 5 to Article 7] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.80)
A key investor information document shall be: (a) presented and laid out in a way that is easy to read, using characters of readable size; (b) clearly expressed and written in language that communicates in a way that facilitates the investor's understanding of the information being communicated, in particular where: (i) the language used is clear, succinct and comprehensible; (ii) the use of jargon is avoided; (iii) technical terms are avoided when everyday words can be used instead; (c) focused on the key information that investors need. 2. Where colours are used, they shall not diminish the comprehensibility of the information in the event that the key investor information document is printed or photocopied in black and white. 3. Where the design of the corporate branding of the management company or the group to which it belongs is used, it shall not distract the investor or obscure the text. Length The key investor information document shall not exceed two pages of A4-sized paper when printed. Specific contents of the description 1. The description contained in the ‘Objectives and investment policy’ section of the key investor information document shall cover those essential features of the UCITS about which an investor should

---

[kiid, Article 37 to Article 38] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.78)
The key investor information document for structured UCITS shall not exceed three pages of A4-sized paper when printed. Conditions applying to the provision of a key investor information document or a prospectus in a durable medium other than paper or by means of a website 1. Where, for the purposes of Directive 2009/65/EC, the key investor information document or prospectus is to be provided to investors using a durable medium other than paper the following conditions shall be met: (a) the provision of the key investor information document or the prospectus using such a durable medium is appropriate to the context in which the business between the management company and the investor is, or is to be, carried on; and (b) the person to whom the key investor information document or the prospectus is to be provided, when offered the choice between information on paper or in that other durable medium, specifically chooses that other medium. 2. Where the key investor information document or the prospectus is to be provided by means of a website and that information is not addressed personally to the investor, the following conditions shall also be satisfied: (a) the provision of that information in that

---

[kiid, Article 36 to Article 38] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.75)
the formula. They shall be presented in a way that is fair, clear and not misleading, and that is likely to be understood by the average retail investor. In particular, they shall not artificially magnify the importance of the final performance of the UCITS. 5. The scenarios referred to in paragraph 3 shall be based on reasonable and conservative assumptions about future market conditions and price movements. However, whenever the formula exposes investors to the possibility of substantial losses, such as a capital guarantee that functions only under certain circumstances, these losses shall be appropriately illustrated, even if the probability of the corresponding market conditions is low. 6. The scenarios referred to in paragraph 3 shall be accompanied by a statement that they are examples that are included to illustrate the formula, and do not represent a forecast of what might happen. It shall be made clear that the scenarios shown may not have an equal probability of occurrence. Length The key investor information document for structured UCITS shall not exceed three pages of A4-sized paper when printed. Conditions applying to the provision of a key investor information document or a prospectus in a durable medium other than paper or

---

[ucits_directive, Article 78] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
Key investor information shall include appropriate information about the essential characteristics of the UCITS concerned, which is to be provided to investors so that they are reasonably able to understand the nature and the risks of the investment product that is being offered to them and, consequently, to take investment decisions on an informed basis. 3. Key investor information shall provide information on the following essential elements in respect of the UCITS concerned: (a) identification of the UCITS; (b) a short description of its investment objectives and investment policy; (c) past-performance presentation or, where relevant, performance scenarios; (d) costs and associated charges; and (e) risk/reward profile of the investment, including appropriate guidance and warnings in relation to the risks associated with investments in the relevant UCITS. Those essential elements shall be comprehensible to the investor without any reference to other documents. 4. Key investor information shall clearly specify where and how to obtain additional information relating to the proposed investment, including but not limited to where and how the prospectus and the annual and half-yearly report can be obtained on request and free of charge at any time, and the language in which such information is available to investors. 5.

---

[kiid, Article 6 to Article 7] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.74)
of A4-sized paper when printed. Specific contents of the description 1. The description contained in the ‘Objectives and investment policy’ section of the key investor information document shall cover those essential features of the UCITS about which an investor should be informed, even if these features do not form part of the description of objectives and inves
```
</details>

## q32 (multi)
**Question:** Can a UCITS put 25% of its assets into one other UCITS that itself invests 30% in other funds?
**Reference:** No on both counts: a UCITS may invest at most 20% of its assets in a single other fund, and target funds may invest no more than 10% of their own assets in other funds.

**Agent answer:**

A UCITS may not put 25% of its assets into one other UCITS under standard rules. 

According to Directive 2009/65/EC, a UCITS may acquire units of other UCITS or collective investment undertakings provided that no more than **10%** of its assets are invested in units of a single UCITS or other collective investment undertaking, though Member States may raise that limit to a maximum of **20%** [ucits_directive, Article 54(1)]. Furthermore, a UCITS may acquire no more than **25%** of the units of a single UCITS or other collective investment undertaking (which restricts the proportion of the target fund that the investing fund can buy, rather than the amount the investing fund can put into it) [ucits_directive, Article 56(2)]. 

Regarding the target fund's own investments, the directive states that investments made in units of collective investment undertakings *other than UCITS* shall not exceed, in aggregate, **30%** of the assets of the UCITS [ucits_directive, Article 54(2)].

*Note: This answer reflects the provisions of Directive 2009/65/EC (UCITS Directive) as indexed in the corpus.*

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 55 to Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
of the limits laid down in Article 52. 3. Where a UCITS invests in the units of other UCITS or collective investment undertakings that are managed, directly or by delegation, by the same management company or by any other company with which the management company is linked by common management or control, or by a substantial direct or indirect holding, that management company or other company shall not charge subscription or redemption fees on account of the UCITS’ investment in the units of such other UCITS or collective investment undertakings. A UCITS that invests a substantial proportion of its assets in other UCITS or collective investment undertakings shall disclose in its prospectus the maximum level of the management fees that may be charged both to the UCITS itself and to the other UCITS or collective investment undertakings in which it intends to invest. It shall indicate in its annual report the maximum proportion of management fees charged both to the UCITS itself and to the other UCITS or collective investment undertaking in which it invests. 1. An investment company or a management company acting in connection with all of the common funds which it manages and which fall within the

---

[ucits_directive, Article 54 to Article 55] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
prominent statement in its prospectus and marketing communications drawing attention to such authorisation and indicating the Member States, local authorities, or public international bodies in the securities of which it intends to invest or has invested more than 35 % of its assets. 1. A UCITS may acquire the units of UCITS or other collective investment undertakings referred to in Article 50(1)(e), provided that no more than 10 % of its assets are invested in units of a single UCITS or other collective investment undertaking. Member States may raise that limit to a maximum of 20 %. 2. Investments made in units of collective investment undertakings other than UCITS shall not exceed, in aggregate, 30 % of the assets of the UCITS. Member States may, where a UCITS has acquired units of another UCITS or collective investment undertakings, provide that the assets of the respective UCITS or other collective investment undertakings are not required to be combined for the purposes of the limits laid down in Article 52. 3. Where a UCITS invests in the units of other UCITS or collective investment undertakings that are managed, directly or by delegation, by the same management company or by any other company

---

[ucits_directive, Article 55 to Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
UCITS itself and to the other UCITS or collective investment undertaking in which it invests. 1. An investment company or a management company acting in connection with all of the common funds which it manages and which fall within the scope of this Directive shall not acquire any shares carrying voting rights which would enable it to exercise significant influence over the management of an issuing body. Pending further coordination, Member States shall take account of existing rules defining the principle stated in the first subparagraph in the law of other Member States. 2. A UCITS may acquire no more than: (a) 10 % of the non-voting shares of a single issuing body; (b) 10 % of the debt securities of a single issuing body; (c) 25 % of the units of a single UCITS or other collective investment undertaking within the meaning of Article 1(2)(a) and (b); or (d) 10 % of the money market instruments of a single issuing body. The limits laid down in points (b), (c) and (d) may be disregarded at the time of acquisition if at that time the gross amount of the debt securities or of the money market instruments, or the net

---

[ucits_directive, Article 57 to Article 58] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
money market instruments which form part of their assets. While ensuring observance of the principle of risk spreading, Member States may allow recently authorised UCITS to derogate from Articles 52 to 55 for six months following the date of their authorisation. 2. If the limits referred to in paragraph 1 are exceeded for reasons beyond the control of a UCITS or as a result of the exercise of subscription rights, that UCITS shall adopt as a priority objective for its sales transactions the remedying of that situation, taking due account of the interests of its unit-holders. 1. A feeder UCITS is a UCITS, or an investment compartment thereof, which has been approved to invest, by way of derogation from Article 1(2)(a), Articles 50, 52 and 55, and Article 56(2)(c), at least 85 % of its assets in units of another UCITS or investment compartment thereof (the master UCITS). 2. A feeder UCITS may hold up to 15 % of its assets in one or more of the following: (a) ancillary liquid assets in accordance with the second subparagraph of Article 50(2); (b) financial derivative instruments, which may be used only for hedging purposes, in accordance with Article 50(1)(g) and Article

---

[ucits_directive, Article 52 to Article 53] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
instruments made with this body carried out in accordance with paragraphs 1 to 4 shall not exceed in total 35 % of the assets of the UCITS. Companies which are included in the same group for the purposes of consolidated accounts, as defined in Directive 83/349/EEC or in accordance with recognised international accounting rules, shall be regarded as a single body for the purpose of calculating the limits contained in this Article. Member States may allow cumulative investment in transferable securities and money market instruments within the same group up to a limit of 20 %. 1. Without prejudice to the limits laid down in Article 56, Member States may raise the limits laid down in Article 52 to a maximum of 20 % for 
```
</details>

## q33 (multi)
**Question:** Market moves pushed our position in one issuer to 12% of the fund's assets. Is that a breach, and what must we do?
**Reference:** Yes, it exceeds the 5% issuer limit (10% maximum where raised). Because it was caused by market movements, the priority in sales transactions must be to remedy the situation in the unit-holders' interest.

**Agent answer:**

If the limits are exceeded for reasons beyond the control of the UCITS—such as market moves—or as a result of the exercise of subscription rights, it is not considered an unlawful breach at the outset [ucits_directive, Article 57(2)]. However, the UCITS must adopt as a priority objective for its sales transactions the remedying of that situation, taking due account of the interests of its unit-holders [ucits_directive, Article 57(2)]. 

Please note that this answer reflects the provisions of Directive 2009/65/EC (UCITS Directive) as indexed.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 53 to Article 54] Directive 2009/65/EC (UCITS Directive) (relevance 0.64)
certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it is published in an appropriate manner. 2. Member States may raise the limit laid down in paragraph 1 to a maximum of 35 % where that proves to be justified by exceptional market conditions in particular in regulated markets where certain transferable securities or money market instruments are highly dominant. The investment up to that limit shall be permitted only for a single issuer. 1. By way of derogation from Article 52, Member States may authorise UCITS to invest in accordance with the principle of risk-spreading up to 100 % of their assets in different transferable securities and money market instruments issued or guaranteed by a Member State, one or more of its local authorities, a third country, or a public international body to which one or more Member States belong. The competent authorities of the UCITS home Member State shall grant such a derogation only if they consider that unit-holders in the UCITS have protection equivalent to that of

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.64)
of issuers authorised, in accordance with the laws and supervisory arrangements mentioned in that subparagraph, to issue bonds complying with the criteria set out in this Article. A notice specifying the status of the guarantees offered shall be attached to those lists. The Commission shall immediately forward that information to the other Member States together with any comments which it considers appropriate and shall make the information available to the public. Such communications may be the subject of exchanges of views within the European Securities Committee referred to in Article 112(1). 5. The transferable securities and money market instruments referred to in paragraphs 3 and 4 shall not be taken into account for the purpose of applying the limit of 40 % referred to in paragraph 2. The limits provided for in paragraphs 1 to 4 shall not be combined, and thus investments in transferable securities or money market instruments issued by the same body or in deposits or derivative instruments made with this body carried out in accordance with paragraphs 1 to 4 shall not exceed in total 35 % of the assets of the UCITS. Companies which are included in the same group for the purposes of consolidated

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.63)
has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in assets which, during the whole period of validity of the bonds, are capable of covering claims attaching to the bonds and which, in the event of failure of the issuer, would be used on a priority basis for the reimbursement of the principal and payment of the accrued interest. Where a UCITS invests more than 5 % of its assets in the bonds referred to in the first subparagraph which are issued by a single issuer, the total value of these investments shall not exceed 80 % of the value of the assets of the UCITS. Member States shall send to the Commission a list of the categories of bonds referred to in the first subparagraph together with the categories of issuers authorised, in accordance with the laws and supervisory arrangements mentioned in that subparagraph, to issue bonds complying with the criteria set out in this Article. A notice specifying the status of the guarantees offered shall be attached to

---

[ucits_directive, Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.63)
issuing body. The limits laid down in points (b), (c) and (d) may be disregarded at the time of acquisition if at that time the gross amount of the debt securities or of the money market instruments, or the net amount of the securities in issue, cannot be calculated. 3. A Member State may waive the application of paragraphs 1 and 2 as regards: (a) transferable securities and money market instruments issued or guaranteed by a Member State or its local authorities; (b) transferable securities and money market instruments issued or guaranteed by a third country; (c) transferable securities and money market instruments issued by a public international body to which one or more Member States belong; (d) shares held by a UCITS in the capital of a company incorporated in a third country investing its assets mainly in the securities of issuing bodies having their registered offices in that country, where under the legislation of that country such a holding represents the only way in which the UCITS can invest in the securities of issuing bodies of that country; or (e) shares held by an investment company or investment companies in the capital of subsidiary companies pursuing only the

---

[ucits_directive, Article 62 to Article 63] Directive 2009/65/EC (UCITS Directive) (relevance 0.63)
the feeder UCITS. The auditor of the feeder UCITS shall, in particular, report on any irregularities revealed in the audit report of the master UCITS and on their impact on the feeder UCITS. 3. Where they comply with the requirements laid down in this Chapter, neither the auditor of the master UCITS nor that of the feeder UCITS shall be found to be in breach of any rules that restrict the disclosure of information or relate to data protection where such rules are provided for in a contract or in a law, regulation or administrative provision. Such compliance shall not give rise to any liability on the part of such auditor or any person acting on its behalf. 4. The Commission may adopt implementing measures specifying th
```
</details>

## q34 (multi)
**Question:** Can a UCITS hold 15% of the bonds issued by one company if that holding is only 3% of the fund's assets?
**Reference:** No. The 3% position respects the 5% issuer limit, but a UCITS may acquire no more than 10% of the debt securities of a single issuing body.

**Agent answer:**

A UCITS may not hold 15% of the bonds issued by one company if that holding represents 3% of the fund's assets, as the investment limit is based on the percentage of the fund's assets invested in the issuer, not the percentage of the issuer's total bond issuance held by the fund.

Under [ucits_directive, Article 52(1)], a UCITS shall invest no more than 5% of its assets in transferable securities or money market instruments issued by any single body. This limit may be raised to a maximum of 10% of the assets of the UCITS, provided that the total value of the transferable securities and money market instruments held in the issuing bodies in each of which it invests more than 5% of its assets does not exceed 40% of the value of its assets.

Please note that these rules are based on the original 2009 Directive text; later amendments may apply.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in assets which, during the whole period of validity of the bonds, are capable of covering claims attaching to the bonds and which, in the event of failure of the issuer, would be used on a priority basis for the reimbursement of the principal and payment of the accrued interest. Where a UCITS invests more than 5 % of its assets in the bonds referred to in the first subparagraph which are issued by a single issuer, the total value of these investments shall not exceed 80 % of the value of the assets of the UCITS. Member States shall send to the Commission a list of the categories of bonds referred to in the first subparagraph together with the categories of issuers authorised, in accordance with the laws and supervisory arrangements mentioned in that subparagraph, to issue bonds complying with the criteria set out in this Article. A notice specifying the status of the guarantees offered shall be attached to

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.74)
individual limits laid down in paragraph 1, a UCITS shall not combine, where this would lead to investment of more than 20 % of its assets in a single body, any of the following: (a) investments in transferable securities or money market instruments issued by that body; (b) deposits made with that body; or (c) exposures arising from OTC derivative transactions undertaken with that body. 3. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 35 % if the transferable securities or money market instruments are issued or guaranteed by a Member State, by its local authorities, by a third country or by a public international body to which one or more Member States belong. 4. Member States may raise the 5 % limit laid down in the first subparagraph of paragraph 1 to a maximum of 25 % where bonds are issued by a credit institution which has its registered office in a Member State and is subject by law to special public supervision designed to protect bond-holders. In particular, sums deriving from the issue of those bonds shall be invested in accordance with the law in

---

[ucits_directive, Article 54 to Article 55] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
prominent statement in its prospectus and marketing communications drawing attention to such authorisation and indicating the Member States, local authorities, or public international bodies in the securities of which it intends to invest or has invested more than 35 % of its assets. 1. A UCITS may acquire the units of UCITS or other collective investment undertakings referred to in Article 50(1)(e), provided that no more than 10 % of its assets are invested in units of a single UCITS or other collective investment undertaking. Member States may raise that limit to a maximum of 20 %. 2. Investments made in units of collective investment undertakings other than UCITS shall not exceed, in aggregate, 30 % of the assets of the UCITS. Member States may, where a UCITS has acquired units of another UCITS or collective investment undertakings, provide that the assets of the respective UCITS or other collective investment undertakings are not required to be combined for the purposes of the limits laid down in Article 52. 3. Where a UCITS invests in the units of other UCITS or collective investment undertakings that are managed, directly or by delegation, by the same management company or by any other company

---

[ucits_directive, Article 52] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
of issuers authorised, in accordance with the laws and supervisory arrangements mentioned in that subparagraph, to issue bonds complying with the criteria set out in this Article. A notice specifying the status of the guarantees offered shall be attached to those lists. The Commission shall immediately forward that information to the other Member States together with any comments which it considers appropriate and shall make the information available to the public. Such communications may be the subject of exchanges of views within the European Securities Committee referred to in Article 112(1). 5. The transferable securities and money market instruments referred to in paragraphs 3 and 4 shall not be taken into account for the purpose of applying the limit of 40 % referred to in paragraph 2. The limits provided for in paragraphs 1 to 4 shall not be combined, and thus investments in transferable securities or money market instruments issued by the same body or in deposits or derivative instruments made with this body carried out in accordance with paragraphs 1 to 4 shall not exceed in total 35 % of the assets of the UCITS. Companies which are included in the same group for the purposes of consolidated

---

[ucits_directive, Article 53 to Article 54] Directive 2009/65/EC (UCITS Directive) (relevance 0.73)
certain stock or debt securities index which is recognised by the competent authorities, on the following basis: (a) its composition is sufficiently diversified; (b) the index represents an adequate benchmark for the market to which it refers; and (c) it is published in an appropriate manner. 2. Member States may raise the limit laid down in paragraph 1 to a maximum of 35 % where that proves to be justified by exceptional market conditions in particular in regulated markets where certain transferable securities or money market instruments are highly dominant. The investment up to that limit shall be permitted only for a single issuer. 1. By way of derogation from Article 52, Member States may authorise UCITS to invest in accordance with the principle of risk-spreading up to 100 % of
```
</details>

## q35 (unanswerable)
**Question:** What rules apply to the remuneration policy for staff of a UCITS management company?
**Reference:** The documents do not cover remuneration policies (introduced later by UCITS V); the assistant should say it does not know.

**Agent answer:**

I don't know. The indexed documents do not contain specific rules regarding the remuneration policy for staff of a UCITS management company. Please note that the provided corpus consists of the original 2007-2010 texts (Directive 2009/65/EC and Commission Directive 2010/43/EU), and later amendments (such as those introduced by UCITS V regarding remuneration) are not included in the current search index.

<details><summary>Retrieved passages</summary>

```
[organisation, Article 8 to Article 9] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.70)
that net asset value. 3. Member States shall require management companies to establish appropriate procedures to ensure the proper and accurate valuation of the assets and liabilities of the UCITS, as consistent with the applicable rules referred to in Article 85 of Directive 2009/65/EC. Control by senior management and supervisory function 1. Member States shall require management companies, when allocating functions internally, to ensure that senior management and, where appropriate, the supervisory function, are responsible for the management company’s compliance with its obligations under Directive 2009/65/EC. 2. The management company shall ensure that its senior management: (a) is responsible for the implementation of the general investment policy for each managed UCITS, as defined, where relevant, in the prospectus, the fund rules or the instruments of incorporation of the investment company; (b) oversees the approval of investment strategies for each managed UCITS; (c) is responsible for ensuring that the management company has a permanent and effective compliance function, as referred to in Article 10, even if this function is performed by a third party; (d) ensures and verifies on a periodic basis that the general investment policy, the investment strategies and the risk limits of each managed UCITS are properly and

---

[organisation, Article 29] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.69)
fee, commission or non-monetary benefit paid or provided to or by a third party or a person acting on behalf of a third party, where the following conditions are satisfied: (i) the existence, nature and amount of the fee, commission or benefit, or, where the amount cannot be ascertained, the method of calculating that amount, must be clearly disclosed to the UCITS in a manner that is comprehensive, accurate and understandable, prior to the provision of the relevant service; (ii) the payment of the fee or commission, or the provision of the non-monetary benefit must be designed to enhance the quality of the relevant service and not impair compliance with the management company’s duty to act in the best interests of the UCITS; (c) proper fees which enable or are necessary for the provision of the relevant service, including custody costs, settlement and exchange fees, regulatory levies or legal fees, and which, by their nature, cannot give rise to conflicts with the management company’s duties to act honestly, fairly and professionally in accordance with the best interests of the UCITS. 2. Member States shall permit a management company, for the purposes of paragraph 1(b)(i), to disclose the essential terms of

---

[organisation, Recitals] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.69)
performed by third parties. (7) Management companies should also maintain the necessary resources, in particular, to employ personnel with the right skills, knowledge and experience in order to be able to fulfil their duties. (8) With respect to safe data processing procedures and the obligation to reconstruct all transactions involving the UCITS the management company should have arrangements in place which permit a timely and proper recording of each transaction carried out on behalf of the UCITS. (9) Accounting is one of the key areas of UCITS administration. It is therefore of paramount importance that the accounting procedures are further specified in the implementing legislation. This Directive should therefore uphold the principles that all assets and liabilities of a UCITS or of its investment compartments can be directly identified, and that accounts should be separate. In addition, where different share classes exist depending on, for example, the level of management fees, it should be possible to extract directly from the accounting the net asset value of those different classes. (10) The clear allocation of the responsibilities of senior management and the supervisory function are central for the implementation of appropriate internal control mechanisms as required by Directive 2009/65/EC. This entails

---

[organisation, Recitals] Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management) (relevance 0.69)
of fees, commissions and non-monetary benefits are not considered a violation of those principles. (22) The cross-border activities of the management company create new challenges for the relationship between the management company and the UCITS’ depositary. To ensure the necessary legal certainty, the main elements of the agreement between the UCITS’ depositary and the management company, where that management company is established in a Member State other than the UCITS’ home Member State, should be specified in this Directive. Given the need to ensure that this agreement properly serves its purpose it is necessary to provide for conflict of law rules which derogate from Articles 3 and 4 of the Regulation (EC) No 593/2008 of the European Parliament and of the Council of 17 June 2008 on the law applicable to contractual obligations (Rome I) ( 6 ) in such a way that the applicable law to this agreement should be the law of the UCITS’ home Member State. (23) Directive 2009/65/EC contains an obligation to specify the criteria for assessing the adequacy of a management company’s risk management process. Such criteria focus on the establishment of an adequate and documented risk management policy to be employed by management companies.

---

[ucits_directive, Article 14 to Article 15] Directive 2009/65/EC (UCITS Directive) (relevance 0.69)
the UCITS; (b) specify the principles required to ensure that management companies employ effectively the resources and 
```
</details>

## q36 (unanswerable)
**Question:** What leverage limits apply to an alternative investment fund under the AIFMD?
**Reference:** The documents cover UCITS only, not AIFMD; the assistant should say it does not know.

**Agent answer:**

I don't know, because the indexed documents do not cover alternative investment funds under the AIFMD (the corpus covers UCITS funds under Directive 2009/65/EC and its related directives and regulations).

<details><summary>Retrieved passages</summary>

```
(no passages retrieved)
```
</details>

## q37 (unanswerable)
**Question:** What is the maximum weighted average maturity of a money market fund under the Money Market Funds Regulation?
**Reference:** The Money Market Funds Regulation is not in the documents; the assistant should say it does not know.

**Agent answer:**

I don't know. The indexed documents (Directive 2009/65/EC, Commission Directive 2007/16/EC, Commission Directive 2010/43/EU, and Commission Regulation 583/2010) do not cover the Money Market Funds Regulation or the maximum weighted average maturity of a money market fund.

<details><summary>Retrieved passages</summary>

```
[eligible_assets, Article 3 to Article 4] Commission Directive 2007/16/EC (eligible assets) (relevance 0.63)
The reference in Article 1(9) of Directive 85/611/EEC to money market instruments as instruments shall be understood as a reference to the following: (a) financial instruments which are admitted to trading or dealt in on a regulated market in accordance with points (a), (b) and (c) of Article 19(1) of Directive 85/611/EEC; (b) financial instruments which are not admitted to trading. 2. The reference in Article 1(9) of Directive 85/611/EEC to money market instruments as instruments normally dealt in on the money market shall be understood as a reference to financial instruments which fulfil one of the following criteria: (a) they have a maturity at issuance of up to and including 397 days; (b) they have a residual maturity of up to and including 397 days; (c) they undergo regular yield adjustments in line with money market conditions at least every 397 days; (d) their risk profile, including credit and interest rate risks, corresponds to that of financial instruments which have a maturity as referred to in points (a) or (b), or are subject to a yield adjustment as referred to in point (c). Article 1(9) of Directive 85/611/EEC Liquid instruments with a value which can be accurately determined at

---

[eligible_assets, Article 3 to Article 4] Commission Directive 2007/16/EC (eligible assets) (relevance 0.62)
have a maturity as referred to in points (a) or (b), or are subject to a yield adjustment as referred to in point (c). Article 1(9) of Directive 85/611/EEC Liquid instruments with a value which can be accurately determined at any time 1. The reference in Article 1(9) of Directive 85/611/EEC to money market instruments as instruments which are liquid shall be understood as a reference to financial instruments which can be sold at limited cost in an adequately short time frame, taking into account the obligation of the UCITS to repurchase or redeem its units at the request of any unit holder. 2. The reference in Article 1(9) of Directive 85/611/EEC to money market instruments as instruments which have a value which can be accurately determined at any time shall be understood as a reference to financial instruments for which accurate and reliable valuations systems, which fulfil the following criteria, are available: (a) they enable the UCITS to calculate a net asset value in accordance with the value at which the financial instrument held in the portfolio could be exchanged between knowledgeable willing parties in an arm’s length transaction; (b) they are based either on market data or on

---

[eligible_assets, Article 4 to Article 5] Commission Directive 2007/16/EC (eligible assets) (relevance 0.60)
a net asset value in accordance with the value at which the financial instrument held in the portfolio could be exchanged between knowledgeable willing parties in an arm’s length transaction; (b) they are based either on market data or on valuation models including systems based on amortised costs. 3. The criteria referred to in paragraphs 1 and 2 shall be presumed to be fulfilled in the case of financial instruments which are normally dealt in on the money market for the purposes of Article 1(9) of Directive 85/611/EEC and which are admitted to, or dealt in on, a regulated market in accordance with points (a), (b) or (c) of Article 19(1) thereof, unless there is information available to the UCITS that would lead to a different determination. Article 19(1)(h) of Directive 85/611/EEC Instruments of which the issue or issuer is regulated for the purpose of protecting investors and savings 1. The reference in Article 19(1)(h) of Directive 85/611/EEC to money market instruments, other than those dealt in on a regulated market, of which the issue or the issuer is itself regulated for the purpose of protecting investors and savings, shall be understood as a reference to financial instruments which fulfil

---

[eligible_assets, Recitals] Commission Directive 2007/16/EC (eligible assets) (relevance 0.60)
20.3.2007 EN Official Journal of the European Union L 79/11 COMMISSION DIRECTIVE 2007/16/EC of 19 March 2007 implementing Council Directive 85/611/EEC on the coordination of laws, regulations and administrative provisions relating to undertakings for collective investment in transferable securities (UCITS) as regards the clarification of certain definitions (Text with EEA relevance) THE COMMISSION OF THE EUROPEAN COMMUNITIES, Having regard to the Treaty establishing the European Community, Having regard to Council Directive 85/611/EEC of 20 December 1985 on the coordination of laws, regulations and administrative provisions relating to undertakings for collective investment in transferable securities (UCITS) ( 1 ) , and in particular point (a) of Article 53a thereof, Whereas: (1) Directive 85/611/EEC contains several definitions, sometimes interlinked, related to the assets which are eligible for investment by undertakings for collective investment in transferable securities, hereinafter ‘UCITS’, such as a definition of transferable securities and a definition of money market instruments. (2) Since the adoption of Directive 85/611/EEC, the variety of financial instruments traded on financial markets has increased considerably, leading to uncertainty in determining whether certain categories of financial instruments are encompassed by those definitions. Uncertainty in applying the definitions gives rise to divergent interpretations of the Directive. (3) In

---

[eligible_assets, Article 12 to Article 15] Commission Directive 2007/16/EC (eligible assets) (relevance 0.59)
reference in the second indent of Article 22a(1) of Directive 85/611/EEC to an index which represents an adequate benchmark shall be understood as a reference to an index whose provider uses a recognised methodology which generally does not result in the exclusion of a major issuer of the market to which it refers. 4. The re
```
</details>

## q38 (unanswerable)
**Question:** What withholding tax does Spain apply to dividends paid by a UCITS to resident investors?
**Reference:** Tax treatment and Spanish law are not covered; the assistant should say it does not know.

**Agent answer:**

I don't know. The indexed documents do not cover the specific withholding tax rates applied by Spain to dividends paid by a UCITS to resident investors. 

Please note that this answer reflects only the indexed versions of the original EU UCITS texts.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Annex I] Directive 2009/65/EC (UCITS Directive) (relevance 0.65)
the tax system applicable to the common fund. Details of whether deductions are made at source from the income and capital gains paid by the common fund to unit-holders. 1.5. Brief indications relevant to unit-holders of the tax system applicable to the company. Details of whether deductions are made at source from the income and capital gains paid by the company to unit-holders. 1.6. Accounting and distribution dates 1.6. Accounting and distribution dates. 1.7. Names of the persons responsible for auditing the accounting information referred to in Article 73. 1.7. Names of the persons responsible for auditing the accounting information referred to in Article 73. 1.8. Names and positions in the company of the members of the administrative, management and supervisory bodies. Details of their main activities outside the company where these are of significance with respect to that company. 1.8. Names and positions in the company of the members of the administrative, management and supervisory bodies. Details of their main activities outside the company where these are of significance with respect to that company. 1.9. Amount of the subscribed capital with an indication of the capital paid-up 1.9. Capital 1.10. Details of the types and main characteristics of the

---

[ucits_directive, Annex I] Directive 2009/65/EC (UCITS Directive) (relevance 0.64)
Member State 1. Information concerning the investment company 1.1. Name 1.1. Name or style, form in law, registered office and head office if different from the registered office. 1.1. Name or style, form in law, registered office and head office if different from the registered office. 1.2. Date of establishment of the common fund. Indication of duration, if limited. 1.2. Date of incorporation of the company. Indication of duration, if limited. 1.2. Date of incorporation of the company. Indication of duration, if limited. 1.3. If the company manages other common funds, indication of those other funds. 1.3. In the case of investment companies having different investment compartments, the indication of the compartments. 1.4. Statement of the place where the fund rules, if they are not annexed, and periodic reports may be obtained. 1.4. Statement of the place where the instruments of incorporation, if they are not annexed, and periodical reports may be obtained. 1.5. Brief indications relevant to unit-holders of the tax system applicable to the common fund. Details of whether deductions are made at source from the income and capital gains paid by the common fund to unit-holders. 1.5. Brief indications relevant to unit-holders of the tax system applicable

---

[ucits_directive, Article 55 to Article 56] Directive 2009/65/EC (UCITS Directive) (relevance 0.64)
of the limits laid down in Article 52. 3. Where a UCITS invests in the units of other UCITS or collective investment undertakings that are managed, directly or by delegation, by the same management company or by any other company with which the management company is linked by common management or control, or by a substantial direct or indirect holding, that management company or other company shall not charge subscription or redemption fees on account of the UCITS’ investment in the units of such other UCITS or collective investment undertakings. A UCITS that invests a substantial proportion of its assets in other UCITS or collective investment undertakings shall disclose in its prospectus the maximum level of the management fees that may be charged both to the UCITS itself and to the other UCITS or collective investment undertakings in which it intends to invest. It shall indicate in its annual report the maximum proportion of management fees charged both to the UCITS itself and to the other UCITS or collective investment undertaking in which it invests. 1. An investment company or a management company acting in connection with all of the common funds which it manages and which fall within the

---

[ucits_directive, Article 1 to Article 2] Directive 2009/65/EC (UCITS Directive) (relevance 0.64)
in Community law governing capital movements and subject to Articles 91 and 92 and the second subparagraph of Article 108(1), no Member State shall apply any other provisions in the field covered by this Directive to UCITS established in another Member State or to the units issued by such UCITS, where those UCITS market their units within the territory of that Member State. 7. Without prejudice to this Chapter, a Member State may apply to UCITS established within its territory requirements which are stricter than or additional to those laid down in this Directive, provided that they are of general application and do not conflict with the provisions of this Directive. 1. For the purposes of this Directive the following definitions apply: (a) ‘depositary’ means an institution entrusted with the duties set out in Articles 22 and 32 and subject to the other provisions laid down in Chapter IV and Section 3 of Chapter V; (b) ‘management company’ means a company, the regular business of which is the management of UCITS in the form of common funds or of investment companies (collective portfolio management of UCITS); (c) ‘management company’s home Member State’ means the Member State in which the management

---

[ucits_directive, Article 94 to Article 95] Directive 2009/65/EC (UCITS Directive) (relevance 0.63)
information or documents other than key investor information referred to in Article 78 shall be translated, at the choice of the UCITS, into the official language, or one of the official languages, of the UCITS host Member State, into a language approved by the competent authorities of that Member State or into a language customary in the sphere of international finance; and (d) translations of information or documents under points (b) and (c) shall be produced under the responsibility of the UCITS and shall faithfully r
```
</details>

## q39 (unanswerable)
**Question:** What does a PRIIPs key information document have to contain for a UCITS sold to retail investors?
**Reference:** The PRIIPs Regulation is not in the documents; the assistant should say it does not know.

**Agent answer:**

I don't know, as the indexed documents do not cover the PRIIPs key information document (they cover the UCITS key investor information document under Directive 2009/65/EC and Regulation 583/2010). Please note that the answer reflects the indexed version of the UCITS texts only.

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 78] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
Key investor information shall include appropriate information about the essential characteristics of the UCITS concerned, which is to be provided to investors so that they are reasonably able to understand the nature and the risks of the investment product that is being offered to them and, consequently, to take investment decisions on an informed basis. 3. Key investor information shall provide information on the following essential elements in respect of the UCITS concerned: (a) identification of the UCITS; (b) a short description of its investment objectives and investment policy; (c) past-performance presentation or, where relevant, performance scenarios; (d) costs and associated charges; and (e) risk/reward profile of the investment, including appropriate guidance and warnings in relation to the risks associated with investments in the relevant UCITS. Those essential elements shall be comprehensible to the investor without any reference to other documents. 4. Key investor information shall clearly specify where and how to obtain additional information relating to the proposed investment, including but not limited to where and how the prospectus and the annual and half-yearly report can be obtained on request and free of charge at any time, and the language in which such information is available to investors. 5.

---

[ucits_directive, Recitals] Directive 2009/65/EC (UCITS Directive) (relevance 0.76)
may decide, where appropriate, to take relevant action to ensure that unit-holders of the master UCITS are informed accordingly. (58) Member States should make a clear distinction between marketing communications and obligatory investor disclosures provided for under this Directive. Obligatory investor disclosure includes key investor information, the prospectus and annual and half-yearly reports. (59) Key investor information should be provided as a specific document to investors, free of charge, in good time before the subscription of the UCITS, in order to help them to reach informed investment decisions. Such key investor information should contain only the essential elements for making such decisions. The nature of the information to be found in the key investor information should be fully harmonised so as to ensure adequate investor protection and comparability. Key investor information should be presented in a short format. A single document of limited length presenting the information in a specified sequence is the most appropriate manner in which to achieve the clarity and simplicity of presentation that is required by retail investors, and should allow for useful comparisons, notably of costs and risk profile, relevant to the investment decision. (60) The competent authorities of each Member State may make available

---

[kiid, Article 2 to Article 4] Commission Regulation (EU) No 583/2010 (key investor information) (relevance 0.75)
Requirements laid down in this Regulation shall apply to any management company with regard to each UCITS it manages. 2. This Regulation shall apply to any investment company which has not designated a management company authorised pursuant to Directive 2009/65/EC. Principles regarding the key investor information document 1. This Regulation specifies in an exhaustive manner the form and content of the document containing key investor information (hereinafter referred to as key investor information document). No other information or statements shall be included except where this Regulation states otherwise. 2. The key investor information shall be fair, clear and not misleading. 3. The key investor information document shall be provided in such a way as to ensure that investors are able to distinguish it from other material. In particular, it shall not be presented or delivered in a way that is likely to lead investors to consider it less important than other information about the UCITS and its risks and benefits. Title and content of document 1. The content of the key investor information document shall be presented in the order as set out in paragraphs 2 to 13. 2. The title ‘Key investor information’ shall appear prominently at the top

---

[ucits_directive, Recitals] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
the clarity and simplicity of presentation that is required by retail investors, and should allow for useful comparisons, notably of costs and risk profile, relevant to the investment decision. (60) The competent authorities of each Member State may make available to the public, in a dedicated section of their website, key investor information concerning all UCITS authorised in that Member State. (61) Key investor information should be produced for all UCITS. Management companies or, where applicable, investment companies should provide key investor information to the relevant entities, in accordance with the distribution method used (direct sales or intermediated sales). Intermediaries should provide key investor information to clients and potential clients. (62) UCITS should be able to market their units in other Member States subject to a notification procedure based on improved communication between the competent authorities of the Member States. Following transmission of a complete notification file by the competent authorities of the UCITS home Member State, it should not be possible for the UCITS host Member State to oppose access to its market by a UCITS established in another Member State or challenge the authorisation given by that other Member State. (63) UCITS should be able to market their

---

[ucits_directive, Article 78] Directive 2009/65/EC (UCITS Directive) (relevance 0.75)
including but not limited to where and how the prospectus and the annual and half-yearly report can be obtained on request and free of charge at any time, and the language in which such information is available to investors. 5. Key investor information 
```
</details>

## q40 (unanswerable)
**Question:** What sustainability (SFDR) disclosures must a UCITS make?
**Reference:** SFDR is not in the documents; the assistant should say it does not know.

**Agent answer:**

I don't know. The indexed documents do not cover sustainability (SFDR) disclosures, as the corpus contains the original 2007–2010 texts (such as Directive 2009/65/EC) which predate the Sustainable Finance Disclosure Regulation (SFDR).

<details><summary>Retrieved passages</summary>

```
[ucits_directive, Article 63 to Article 64] Directive 2009/65/EC (UCITS Directive) (relevance 0.69)
report of the master UCITS can be obtained. 3. In addition to the requirements laid down in Articles 74 and 82, the feeder UCITS shall send the prospectus, the key investor information referred to in Article 78 and any amendment thereto, as well as the annual and half-yearly reports of the master UCITS, to the competent authorities of its home Member State. 4. A feeder UCITS shall disclose in any relevant marketing communications that it permanently invests 85 % or more of its assets in units of such master UCITS. 5. A paper copy of the prospectus, and the annual and half-yearly reports of the master UCITS shall be delivered by the feeder UCITS to investors on request and free of charge. 1. Member States shall require that a feeder UCITS which already pursues activities as a UCITS, including those of a feeder UCITS of a different master UCITS, shall provide the following information to its unit-holders: (a) a statement that the competent authorities of the feeder UCITS home Member State approved the investment of the feeder UCITS in units of such master UCITS; (b) the key investor information referred to in Article 78 concerning the feeder and the master

---

[ucits_directive, Recitals] Directive 2009/65/EC (UCITS Directive) (relevance 0.68)
may decide, where appropriate, to take relevant action to ensure that unit-holders of the master UCITS are informed accordingly. (58) Member States should make a clear distinction between marketing communications and obligatory investor disclosures provided for under this Directive. Obligatory investor disclosure includes key investor information, the prospectus and annual and half-yearly reports. (59) Key investor information should be provided as a specific document to investors, free of charge, in good time before the subscription of the UCITS, in order to help them to reach informed investment decisions. Such key investor information should contain only the essential elements for making such decisions. The nature of the information to be found in the key investor information should be fully harmonised so as to ensure adequate investor protection and comparability. Key investor information should be presented in a short format. A single document of limited length presenting the information in a specified sequence is the most appropriate manner in which to achieve the clarity and simplicity of presentation that is required by retail investors, and should allow for useful comparisons, notably of costs and risk profile, relevant to the investment decision. (60) The competent authorities of each Member State may make available

---

[ucits_directive, Article 67 to Article 68] Directive 2009/65/EC (UCITS Directive) (relevance 0.68)
the master UCITS and the feeder UCITS are established in the same Member State, the competent authorities shall immediately inform the feeder UCITS of any decision, measure, observation of non-compliance with the conditions of this Chapter or of any information reported pursuant to Article 106(1) with regard to the master UCITS or, where applicable, its management company, depositary or auditor. 2. If the master UCITS and the feeder UCITS are established in different Member States, the competent authorities of the master UCITS home Member State shall immediately communicate any decision, measure, observation of non-compliance with the conditions of this Chapter or information reported pursuant to Article 106(1) with regard to the master UCITS or, where applicable, its management company, depositary or auditor, to the competent authorities of the feeder UCITS home Member State. The latter shall then immediately inform the feeder UCITS. 1. An investment company and, for each of the common funds it manages, a management company, shall publish the following: (a) a prospectus; (b) an annual report for each financial year; and (c) a half-yearly report covering the first six months of the financial year. 2. The annual and half-yearly reports shall be published within the following time

---

[ucits_directive, Article 70] Directive 2009/65/EC (UCITS Directive) (relevance 0.67)
financial derivative instruments are authorised, in which case it shall include a prominent statement indicating whether those operations may be carried out for the purpose of hedging or with the aim of meeting investment goals, and the possible outcome of the use of financial derivative instruments on the risk profile. 2. Where a UCITS invests principally in any category of assets defined in Article 50 other than transferable securities or money market instruments, or where a UCITS replicates a stock or debt securities index in accordance with Article 53, its prospectus and, where necessary, marketing communications shall include a prominent statement drawing attention to the investment policy. 3. Where the net asset value of a UCITS is likely to have a high volatility due to its portfolio composition or the portfolio management techniques that may be used, its prospectus and, where necessary, marketing communications shall include a prominent statement drawing attention to that characteristic. 4. Upon request of an investor, the management company shall also provide supplementary information relating to the quantitative limits that apply in the risk management of the UCITS, to the methods chosen to this end and to the recent evolution of the main risks and yields

---

[ucits_directive, Article 63] Directive 2009/65/EC (UCITS Directive) (relevance 0.67)
and the master UCITS or of the internal conduct of business rules pursuant to Article 60(1); (e) how the unit-holders may obtain further information on the master UCITS and the agreement entered into between the feeder UCITS and the master UCITS pursuant to Article 60(1); (f) a description of all remuneration or reimbursement of costs payable by the feeder UCITS by virtue of its investment in units of the mast
```
</details>
