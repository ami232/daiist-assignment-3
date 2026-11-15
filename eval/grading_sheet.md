# Grading sheet

Grade each answer **before** looking at the judge's verdicts. For each one, add a row to `eval/human_labels.csv`: `id,correct,supported,notes`.

- **correct** = 1 if the answer is right against the reference answer (for unanswerable questions: 1 if it properly says it doesn't know and points to the right place), else 0.
- **supported** = 1 if every claim in the answer is in the retrieved passages, else 0.
- **notes**: why, for every 0.

---

## u01 (unanswerable)

**Question:** What exact monthly amount does SEPIE pay Spanish students going to Italy in 2026/27?

**Reference answer:** The documents only give the EU minimum and maximum ranges; the exact amounts are set by the National Agency or the university and published on their websites. Ask SEPIE or your home university.

**Expected location:** — 

**Assistant's answer:**

> I do not know the exact monthly amount. The European Commission does not set the specific grant amounts for students; instead, it defines minimum and maximum ranges, and the exact amounts are determined by the National Agencies (such as SEPIE in Spain) in agreement with national authorities and/or the higher education institutions (Programme Guide 2026, p. 67).
>
> For mobility between EU Member States, the EU sets the following ranges for the "Higher range EU grant" (which applies to students moving from a country with medium living costs, like Spain, to a country with higher living costs, like Italy):
>
> *   **Higher range EU grant:** Between 348 and 674 EUR per month (Programme Guide 2026, p. 68).
>
> Because SEPIE or your home university determines the final amount within these ranges based on local criteria and available co-financing, you should check the official website of SEPIE or contact your university's international office for the specific amount applicable to your mobility (Programme Guide 2026, p. 67).

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-TERM MOBILITY INVOLVING THIRD COUNTRIES NOT ASSOCIATED TO THE PROGRAMME</summary>

The base amount for individual support is set as follows: From To Amount EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 1 to 3 and 5 to 12. 700 EUR per month EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 13 and 14. As described above in section “Grant support for the mobility of students – Individual support for physical mobility” Third countries not associated to the Programme from Regions 1-12. Group 1 of EU Member States and third countries associated to the Programme 900 EUR per month Group 2 of EU Member States and third countries associated to the Programme 850 EUR per month Group 3 of EU Member States and third countries associated to the Programme 800 EUR per month
The top-up amount for students and recent graduates with fewer opportunities will apply in this case. The top-up amount for traineeships will apply only in the case of mobility to third countries not associated to the Programme from Regions 13 and 14. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Group 2 Countries with medium living costs Cyprus, Czechia, Estonia, Greece, Latvia, Malta, Portugal, Slovakia, Slovenia, Spain. Group 3 Countries with lower living costs Bulgaria, Croatia, Hungary, Lithuania, North Macedonia, Poland, Romania, Serbia, Türkiye. The EU Erasmus+ individual support grant provided to students will depend on their mobility flow between the sending and receiving countries of the student, as follows:
- mobility towards a country with similar living costs: students will receive the medium range EU grant;
- mobility towards a country with higher living costs: students will receive the higher range EU grant;
- mobility towards a country with lower living costs: students will receive the lower range EU grant. The amounts defined by National Agencies will be set within the following minimum and maximum ranges:
- Medium range EU grant: a medium range, between 292 and 606 EUR per month, will apply to mobility activities towards a country of similar living costs: a) from Group 1 to Group 1, b) from Group 2 to Group 2 and c) from Group 3 to Group 3.
- Higher range EU grant: corresponds to the medium range applied by the National Agency plus at least 50 EUR and between 348 and 674 EUR per month. It applies to mobility activities towards a country of higher living costs: a) from Group 2 to Group 1 countries and b) from Group 3 to Group 1 and 2 countries.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

- Lower range EU grant: corresponds to the medium range applied by the National Agency minus at least 50 EUR and between 225 and 550 EUR per month. It applies to mobility activities towards a country of lower living costs: a) Group 1 to Group 2 and 3 countries and b) from Group 2 to Group 3. When defining the amounts to be applied by beneficiaries in their country, National Agencies will consider the following two elements:
- the availability and the level of other sources of co-financing from private or public bodies at local, regional or national level to complement the EU grant;
- the general level of demand of students who intend to study or receive training abroad. For mobility activities between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, National Agencies may decide to grant flexibility to their higher education institutions by fixing ranges instead of amounts at national level. This should be based on justified grounds, for example in countries where co-financing is available at regional or institutional level.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSICAL MOBILITY – BASE AMOUNTS OF INDIVIDUAL SUPPORT (BLENDED MOBILITY AND</summary>

DOCTORAL SHORT-TERM MOBILITY) The base amounts of individual support are set as follows:
Duration of the physical activity Amount (for any EU Member States and third countries associated to the Programme or third country not associated to the Programme) Up to the 14th day of activity 79 EUR per day 15th to the 30th day of activity 56 EUR per day The top-up amount for traineeships will not apply in this case. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

---

## u02 (unanswerable)

**Question:** When is the Erasmus application deadline at my university?

**Reference answer:** The documents do not contain student application deadlines; each university sets its own. Ask your international office. (The 19 February deadline in the Programme Guide is for universities applying for funding, not for students.)

**Expected location:** — 

**Assistant's answer:**

> I do not know the application deadline for your university. The official Erasmus+ documents do not contain information about specific university deadlines, selection criteria, or the number of available places.
>
> Please contact your home university's international office directly to ask for their specific application deadlines and selection process.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

- o a HEI from an EU Member State or third country associated to the Programme awarded with an ECHE, or a HEI from a third country not associated to the Programme recognised by competent authorities that has signed inter-institutional agreements with their partners from an EU Member State or third country associated to the Programme, before the mobility takes place. Duration of the activity Student mobility for studies: from 2 months (or one academic term or trimester) to 12 months of physical mobility, excluding travel time. This can include a complementary traineeship period, if planned, and may be organised in different ways depending on the context: either one activity after the other or both at the same time. The combination follows the funding rules and minimum duration o f study mobility. Student mobility for traineeships: from 2 to 12 months of physical mobility, excluding travel time.
Note 65: The following types of organisations are not eligible as receiving organisations for student mobility for traineeships: EU institutions and other EU bodies including specialised agencies (their exhaustive list is available on the website - http://europa.eu/european-union/about-eu/institutions-bodies_en); organisations managing EU programmes such as Erasmus+ National Agencies (in order to avoid a possible conflict of interests and/or double funding).

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 55, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

Eligible participants Students registered in a HEI and enrolled in studies leading to a recognised degree, including double/joint degrees, or another recognised tertiary level qualification (up to and including the level of doctorate). In case of doctoral mobility, the participant must be at EQF level 8. Recent higher education graduates may participate in a mobility for traineeships. The beneficiary organisation may opt out of recent graduate traineeships. Recent graduates must be selected by their HEI during their last year of study and must carry out and complete their traineeship abroad within one year of obtaining their graduation. Other requirements Student mobility can be in any study field. Student mobility can be a study period combined with a short traineeship (of less than 2 months) while being considered as an overall study period. The student, the sending and the receiving organisation must sign a learning agreement. The study period abroad must be part of the student’s study programme to complete a degree. Wherever possible, the traineeships should be an integrated part of the student’s study programme. Following courses at a higher education institution cannot be considered as a traineeship. In case of blended student mobility, the activities may include participation in courses offered in a blended learning format at any partner HEI, online training and work assignments or participation in blended intensive programmes. Regarding international mobility, see section on “International mobility involving third countries not associated to the Programme”.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 52, ELIGIBILITY CRITERIA OF MOBILITY PROJECTS</summary>

have to be involved in the organisation of the blended intensive programme during implementation. Duration of the project Mobility projects supported by internal policy funds: 26 months Mobility projects supported by external policy funds: 24 or 36 months Where to apply? To the National Agency of the country in which the applicant organisation is established. When to apply? Applicants must submit their grant application by 19 February at 12:00:00 (midday Brussels time) both for projects funded with internal policy funds starting on 1 June of the same year and for projects funded with external actions instruments starting on 1 August of the same year. How to apply? Please see part C of this Guide for details on how to apply. Other minimum requirements A HEI may apply for grants to its National Agency via two different channels:
- directly as an individual HEI
- via a mobility consortium of which it is a coordinator/member.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

Any student, in particular those who are not able to participate in a long-term physical mobility for studies or for traineeships, for example, due to their study field or because they have fewer opportunities for participation, may combine a shorter physi cal mobility with a virtual component (blended short-term mobility). In addition, any student may participate in blended intensive programmes. In these cases, physical mobility must last between 5 days and 30 days (excluding travel time) and be combined wi th a compulsory virtual component facilitating collaborative online learning exchange and teamwork. A blended mobility for studies must award a minimum of 3 ECTS credits. Mobility for studies and/or traineeships for doctoral candidates: from 5 to 30 days or from 2 to 12 months of physical mobility (a study mobility may include a complementary traineeship period, if planned), excluding travel time. Total eligible duration per study cycle: The same student may participate in mobility periods totalling up to 12 months of physical mobility maximum per each cycle of study, independently of the number and type of mobility activities:
- during the first study cycle (Bachelor or equivalent) including the short cycle (EQF levels 5 and 6);
- during the second study cycle (Master or equivalent - EQF level 7); and

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

---

## u03 (unanswerable)

**Question:** What GPA or language certificate do I need to be selected for Erasmus?

**Reference answer:** The documents do not cover student selection criteria; they are set by the home university.

**Expected location:** — 

**Assistant's answer:**

> I do not know the specific GPA or language certificate requirements for your application.
>
> The European Commission documents do not set universal GPA or language requirements for student selection. These criteria are determined by your home university.
>
> *   **Selection Criteria:** Requirements such as GPA, language certificates, or other academic prerequisites are decided by your home university. You should contact your university's international office to ask about their specific selection process, criteria, and deadlines.
> *   **Language Proficiency:** While the European Commission emphasizes that language preparation is important for success, the specific proficiency level required at the selection stage is determined by your institution. Partner universities may also define required levels in their inter-institutional agreements or course catalogues `(ECHE Guidelines, pp. 14-15)`.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus Charter for Higher Education 2021-2027: Guidelines — pp. 14-15, 2.1 Before Mobility</summary>

Language preparation is a crucial element to ensure success in mobility outcomes (staff / student satisfaction, coping with everyday challenges and pressure during the study / training period and improved exam success rates). Both partner HEIs / organisations should agree on the proficiency level required in the language of instruction or the workplace and (if different) the local language that the participant should have at the start of the mobility (the proficiency level should be defined in the course catalogue and / or inter- institutional agreement; or in the learning or grant agreement in the case of traineeships and in the mobility agreement in the case of invited staff from enterprise or staff training at an organisation that is not an HEI).
Staff should at least have the minimum required proficiency level at the selection stage. Student selection criteria should, however, take into account both the relevant language
skills at the selection stage and the capacity of the students to improve their language skills (through online tools such as the l inguistic assessment and support offered by the European Commission or any other type of support) to achieve the required minimum level at the start of the mobility abroad (level to be specified and agreed on in the learning agreement). When required, the sending HEI should ensure that any necessary pre-departure language instruction actually takes place.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — pp. 44-45, AWARD CRITERIA</summary>

Submitted applications will be assessed by assigning points out of a total of 100, based on the below criteria and scores. To be considered for award, applications must pass the following thresholds:
- At least 60 out of the total 100 points, and
- At least half of the maximum score points in each of the four award criteria below.
Relevance of the consortium ▪ The relevance of the proposal to:
(maximum score 30 points)
the objectives of the action; the needs and objectives of the organisations participating in the consortium and of the individual participants.
- The extent to which the proposal is relevant for the respect and promotion of shared EU values, such as respect for human dignity, freedom, democracy, equality, the rule of law and respect for human rights, as well as fighting any sort of discrimination.
- The extent to which the proposal is suitable for:
- - producing high-quality learning outcomes for participants;
- - reinforcing the capacities and international scope of the organisations participating in the consortium;
- - bringing added value at EU level through results that would not be attained by activities carried out by each individual HEI. Quality of the consortium composition and the cooperation arrangements (maximum score 20 points)
The extent to which:

</details>

<details><summary>[3] Erasmus Charter for Higher Education 2021-2027: Guidelines — p. 12, 2.1 Before Mobility</summary>

The HEI should clearly indicate in which languag e the course units are taught and specify to what extent they are open to mobile students (indicating any prerequisites, such as the minimum linguistic level). Institutions should at least indicate clearly the course units not taught in the host language a nd those which are not open to mobile students. Any relevant information on programme requirements for traineeships should also be indicated, along with the number of credits.
While all the above information should be included in the Course Catalogue, eac h HEI can decide on its precise format, taking into account specific technical (IT, editorial, linguistic, etc.) aspects. Whatever the style adopted, the online course catalogue should be user-friendly. A good practice is to have an archive section contain ing earlier editions, thus making it easy to track any changes in study programmes / examination regulations.
Ideally, the course catalogue for the upcoming academic year should be available by the early spring of the preceding academic year, in order to allow prospective participants to prepare their learning agreements well in advance of their mobility.
- Publish and regularly update information on the grading system used and grade distribution tables for all study programmes. Ensure that students receiv e clear and transparent information on recognition and grade conversion procedures.

</details>

<details><summary>[4] Erasmus+ Student Charter — Before the mobility period > Your obligations and duties</summary>

You must sign a grant agreement with the sending institution and a learning agreement with the sending and the receiving institution, setting out the details of the activities abroad, which is the basis for ensuring the automatic recognition of your mobility period abroad (through spelling out the credits you are expected to earn and counting them towards your home degree).
You need to undergo an online language assessment free of charge through the Online Language Support after being selected (provided this is available in the main language of instruction / work abroad), so as to evaluate your level and get opportunities to access specific features fitting your language learning needs to make the most of your learning period abroad.
Upon receiving the information and guidance on obtaining insurance from your Higher Education Institution, you should ensure that you have health insurance coverage for your stay abroad. In the case of student mobility for traineeships, you should ensure, together with your traineeship host, that you take up also liability and accident insurance coverage.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 61, WHAT ARE THE AWARD CRITERIA FOR A MOBILITY PROJECT? > AWARD CRITERIA FOR MOBILITY PROJECTS SUPPORTED BY INTERNAL POLICY FUNDS</summary>

There is no qualitative assessment (the quality has been assessed at the ECHE application stage or when selecting a mobility consortium accreditation) and therefore there are no award criteria. Any eligible grant application (after having passed the eligibility check) will get funding. The maximum grant amount awarded will depend on a number of elements:
- the number of mobilities applied for;
- the past performance of the applicant in terms of number of mobilities, good quality in the implementation of activities and sound financial management, in case the applicant has received a similar grant in previous years;
- the number of blended intensive programmes applied for;
- the total national budget allocated for the mobility action for mobility projects supported by internal policy funds.
Note 73: The list of countries for which this requirement applies can be found in the DAC List of Countries receiving Official Development Assistance https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/oda-eligibility-and-conditions/DAC-List-of-ODA-Recipients-for- reporting-2024-25-flows.pdf. The DAC list is periodically updated, so that countries can move from one category to another or exit the list. Nevertheless, the ODA status of a country and the relative restrictions go on unchanged for the whole life cycle of the proje cts under the same call.
Note 74: The list of regions is described in Part A of this Guide.

</details>

---

## u04 (unanswerable)

**Question:** Do I have to pay tax on my Erasmus grant in Spain?

**Reference answer:** The documents do not cover taxation of the grant.

**Expected location:** — 

**Assistant's answer:**

> I do not know if you have to pay tax on your Erasmus grant in Spain. The provided documents do not contain information regarding national tax laws or the tax status of Erasmus+ grants.
>
> For information regarding tax obligations, please contact your local tax authority (Agencia Tributaria in Spain) or your home university's international office, as they can provide guidance on national regulations.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Student Charter — During the mobility period > Your entitlements</summary>

You are entitled to be treated equally to the home students/employees and not be discriminated against on the basis of your age, ethnic origin, race, nationality, membership of a national minority, culture, language, gender, sexual orientation, marital status, caring or parental responsibilities, illness, ability or disability, mental health status, medical condition, physical appearance, socio-economic background, religious faith or affiliation or lack thereof, political affiliation or opinions or lack thereof, or any other irrelevant distinction.
You are entitled to academic freedom in communicating or sharing ideas and facts, as well as in any potential research you might carry out throughout your mobility period.
You are entitled to benefitting from networks of mentors and buddies where available at the receiving institution/organisation.
You are entitled to be heard in and informed about student organisations on campus, the governance and quality assurance systems of the receiving institution, as well as any relevant student support services (e.g. student unions and student representatives, ombudspersons).
You are entitled to continue receiving the same student grants or loans from your sending country while abroad.
You are entitled to additional financial support, in the form of top-ups, if you are a participant with fewer opportunities or if you choose to travel with green means of transport.
You must not be charged fees for tuition, registration, examinations or for accessing laboratory and library facilities during the mobility period.
You are entitled to request changes to the learning agreement within the deadline decided by the sending and receiving institutions. You are entitled to submit a request for extending the duration of the mobility period to your sending institution.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Group 2 Countries with medium living costs Cyprus, Czechia, Estonia, Greece, Latvia, Malta, Portugal, Slovakia, Slovenia, Spain. Group 3 Countries with lower living costs Bulgaria, Croatia, Hungary, Lithuania, North Macedonia, Poland, Romania, Serbia, Türkiye. The EU Erasmus+ individual support grant provided to students will depend on their mobility flow between the sending and receiving countries of the student, as follows:
- mobility towards a country with similar living costs: students will receive the medium range EU grant;
- mobility towards a country with higher living costs: students will receive the higher range EU grant;
- mobility towards a country with lower living costs: students will receive the lower range EU grant. The amounts defined by National Agencies will be set within the following minimum and maximum ranges:
- Medium range EU grant: a medium range, between 292 and 606 EUR per month, will apply to mobility activities towards a country of similar living costs: a) from Group 1 to Group 1, b) from Group 2 to Group 2 and c) from Group 3 to Group 3.
- Higher range EU grant: corresponds to the medium range applied by the National Agency plus at least 50 EUR and between 348 and 674 EUR per month. It applies to mobility activities towards a country of higher living costs: a) from Group 2 to Group 1 countries and b) from Group 3 to Group 1 and 2 countries.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

<details><summary>[4] Erasmus+ Student Charter — Before the mobility period > Your obligations and duties</summary>

You must sign a grant agreement with the sending institution and a learning agreement with the sending and the receiving institution, setting out the details of the activities abroad, which is the basis for ensuring the automatic recognition of your mobility period abroad (through spelling out the credits you are expected to earn and counting them towards your home degree).
You need to undergo an online language assessment free of charge through the Online Language Support after being selected (provided this is available in the main language of instruction / work abroad), so as to evaluate your level and get opportunities to access specific features fitting your language learning needs to make the most of your learning period abroad.
Upon receiving the information and guidance on obtaining insurance from your Higher Education Institution, you should ensure that you have health insurance coverage for your stay abroad. In the case of student mobility for traineeships, you should ensure, together with your traineeship host, that you take up also liability and accident insurance coverage.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSICAL MOBILITY – BASE AMOUNTS OF INDIVIDUAL SUPPORT (BLENDED MOBILITY AND</summary>

DOCTORAL SHORT-TERM MOBILITY) The base amounts of individual support are set as follows:
Duration of the physical activity Amount (for any EU Member States and third countries associated to the Programme or third country not associated to the Programme) Up to the 14th day of activity 79 EUR per day 15th to the 30th day of activity 56 EUR per day The top-up amount for traineeships will not apply in this case. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

---

## u06 (unanswerable)

**Question:** How many Erasmus places does my university have at the University of Bologna?

**Reference answer:** The documents do not cover places at specific universities; each university publishes its own offer.

**Expected location:** — 

**Assistant's answer:**

> I do not know how many Erasmus places your university has at the University of Bologna.
>
> The European Commission's Erasmus+ Programme Guide does not contain information about specific agreements, the number of places, or selection criteria between individual universities. These details are managed internally by each higher education institution.
>
> You should contact your home university's international office to ask about the number of available places and their specific selection process for the University of Bologna.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — pp. 33-34, EU MEMBER STATES AND THIRD COUNTRIES ASSOCIATED TO THE PROGRAMME</summary>

The following countries can fully take part in all the Actions of the Erasmus + Programme: Member States of the European Union (EU) Belgium Bulgaria Czechia Greece Spain France Lithuania Luxembourg Hungary Portugal Romania Slovenia
Note 41: According to Article 33.2 of Council Decision (EU) 2021/1764 of 5 October 2021 on the association of the Overseas Countries a nd Territories with the European Union including relations between the European Union on the one hand, and Greenland and the Kingdom of Denmark on the other (Decision on the Overseas Association, including Greenland) (EUR-Lex - 32021D1764 - EN - EUR-Lex (europa.eu)) the Union shall ensure that individuals and organisations from or to Overseas Countries and Territories (OCT) shall be e ligible for Erasmus+, subject to the rules of the Programme and the arrangements applicable to the Member State with which these OCTs they are conn ected. This means that individuals and organisations from the OCTs are participating in the programme on an 'EU Member State or third country associated to the Programme' status, the 'EU Member State or third country associated to the Programme' being the Member Stat e with which they are connected. The list of OCTs can be found at www.ec.europa.eu/international-partnerships/where-we-work/overseas- countries-and-territories_en.
Denmark Germany Estonia Ireland Croatia Italy Cyprus Latvia Malta Netherlands Austria Poland Slovakia Finland Sweden
Third countries associated to the Programme North Macedonia Serbia Iceland Liechtenstein Norway Türkiye

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Group 2 Countries with medium living costs Cyprus, Czechia, Estonia, Greece, Latvia, Malta, Portugal, Slovakia, Slovenia, Spain. Group 3 Countries with lower living costs Bulgaria, Croatia, Hungary, Lithuania, North Macedonia, Poland, Romania, Serbia, Türkiye. The EU Erasmus+ individual support grant provided to students will depend on their mobility flow between the sending and receiving countries of the student, as follows:
- mobility towards a country with similar living costs: students will receive the medium range EU grant;
- mobility towards a country with higher living costs: students will receive the higher range EU grant;
- mobility towards a country with lower living costs: students will receive the lower range EU grant. The amounts defined by National Agencies will be set within the following minimum and maximum ranges:
- Medium range EU grant: a medium range, between 292 and 606 EUR per month, will apply to mobility activities towards a country of similar living costs: a) from Group 1 to Group 1, b) from Group 2 to Group 2 and c) from Group 3 to Group 3.
- Higher range EU grant: corresponds to the medium range applied by the National Agency plus at least 50 EUR and between 348 and 674 EUR per month. It applies to mobility activities towards a country of higher living costs: a) from Group 2 to Group 1 countries and b) from Group 3 to Group 1 and 2 countries.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 43, HOW TO ACCESS ERASMUS+ HIGHER EDUCATION MOBILITY OPPORTUNITIES?</summary>

The applicant organisation must be established in an EU Member State or third country associated to the Erasmus+ programme and have a higher education accreditation. It may either apply as an individual higher education institution, requiring an Erasmus Charter for Higher Education ( ECHE), or on behalf of a mobility consortium, requiring a consortium accreditation. Individual organisation accreditation – the Erasmus Charter for Higher Education Higher education institutions (HEIs) must have been awarded the Erasmus Charter for Higher Education (ECHE) before applying for a mobility project to their Erasmus+ National Agency. By signing the Erasmus Charter for Higher Education, higher education institutions commit to provide all the necessary support to mobile participants, including linguistic preparati on. Mobile participants can use the Erasmus+ Online Language Support (OLS) to improve their foreign language competences before and/or during mobility. Among other ECHE principles, the participating HEI must carry out mobility for the purpose of studying and teaching only within the framework of prior agreements between institutions and select prospective participants and award mobility grants in a fair, transparent, coherent, and documented way, in line with the provisions of its grant agreement with the National Agency. It should ensure such fair and transparent procedures throughout all stages of mobility and in the process of responding to queries/complaints from participants. It must ensure that no fees are charged in the case of credit mobility, to incoming mobile students for tuition, registration, examinations or access to laboratory and library facilities.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — pp. 46-47, INCLUSION AND DIVERSITY IN HIGHER EDUCATION MOBILITY</summary>

In order to make access to student and staff mobility as easy as possible, in line with the principles of the ECHE, HEIs must ensure equal and equitable access and opportunities to current and prospective participants from all backgrounds. This
means including participants with fewer opportunities, such as participants with physical, mental and health related conditions, students with children, student s who work or are professional athletes and students from all study fields underrepresented in mobility. Defining internal selection procedures that take into account equity and inclusion and assess applicants' merit and motivation holistically is essential in respecting this principle. Furthermore, HEIs are encouraged to establish built-in mobility opportunities, such as mobility windows within their curricula to help facilitate the participation of students from all study fields. In this regard, blended mobility can help offer additional opportunities that may be more suitable for some individuals or student groups. In this context, having in place inclusion officers within the higher education institutions helps address inclusion and diversity. Inclusion officers can for example help raise awareness, define stra tegies for communication and outreach, ensure adequate support throughout mobility in cooperation with relevant colleagues and help facilitate cooperation between relevant staff within the institution with expertise in the field of inclusion and divers ity.

</details>

---

## u07 (unanswerable)

**Question:** Can my Erasmus grant be paid into a bank account outside Spain, for example a German one?

**Reference answer:** The documents do not cover how or into which bank account the grant is paid; ask the home university, which pays the grant under the student's grant agreement.

**Expected location:** — 

**Assistant's answer:**

> The official Erasmus+ documents do not specify which bank account you must use to receive your grant.
>
> Because this is a procedural detail regarding how your university manages payments, I do not have the answer. You should contact your home university's international office to ask if they allow the grant to be paid into a bank account outside of Spain.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Student Charter — Before the mobility period > Your entitlements</summary>

You are entitled to receive guidance on the application process and information on the receiving institution/ organisation, as well as on activities available for the mobility period abroad.
You are entitled to receive a pre-financing payment within 30 calendar days following the signature of the agreement by both parties or upon receipt of confirmation of arrival, and no later than the start date of the mobility period.
If you are engaging in student mobility for studies, you should be able to sign a digital online learning agreement setting out the details of the activities abroad. If agreed with your institution, you may sign the online learning agreement via the Erasmus+ Mobile Application.
You are entitled to receive information on the automatic recognition procedures and grading system used by the receiving institution.
You are entitled to receive information on obtaining insurance, finding housing, securing a visa (if required), and facilities/support available for those with special needs.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Group 2 Countries with medium living costs Cyprus, Czechia, Estonia, Greece, Latvia, Malta, Portugal, Slovakia, Slovenia, Spain. Group 3 Countries with lower living costs Bulgaria, Croatia, Hungary, Lithuania, North Macedonia, Poland, Romania, Serbia, Türkiye. The EU Erasmus+ individual support grant provided to students will depend on their mobility flow between the sending and receiving countries of the student, as follows:
- mobility towards a country with similar living costs: students will receive the medium range EU grant;
- mobility towards a country with higher living costs: students will receive the higher range EU grant;
- mobility towards a country with lower living costs: students will receive the lower range EU grant. The amounts defined by National Agencies will be set within the following minimum and maximum ranges:
- Medium range EU grant: a medium range, between 292 and 606 EUR per month, will apply to mobility activities towards a country of similar living costs: a) from Group 1 to Group 1, b) from Group 2 to Group 2 and c) from Group 3 to Group 3.
- Higher range EU grant: corresponds to the medium range applied by the National Agency plus at least 50 EUR and between 348 and 674 EUR per month. It applies to mobility activities towards a country of higher living costs: a) from Group 2 to Group 1 countries and b) from Group 3 to Group 1 and 2 countries.

</details>

<details><summary>[4] Erasmus+ Student Charter — During the mobility period > Your entitlements</summary>

You are entitled to be treated equally to the home students/employees and not be discriminated against on the basis of your age, ethnic origin, race, nationality, membership of a national minority, culture, language, gender, sexual orientation, marital status, caring or parental responsibilities, illness, ability or disability, mental health status, medical condition, physical appearance, socio-economic background, religious faith or affiliation or lack thereof, political affiliation or opinions or lack thereof, or any other irrelevant distinction.
You are entitled to academic freedom in communicating or sharing ideas and facts, as well as in any potential research you might carry out throughout your mobility period.
You are entitled to benefitting from networks of mentors and buddies where available at the receiving institution/organisation.
You are entitled to be heard in and informed about student organisations on campus, the governance and quality assurance systems of the receiving institution, as well as any relevant student support services (e.g. student unions and student representatives, ombudspersons).
You are entitled to continue receiving the same student grants or loans from your sending country while abroad.
You are entitled to additional financial support, in the form of top-ups, if you are a participant with fewer opportunities or if you choose to travel with green means of transport.
You must not be charged fees for tuition, registration, examinations or for accessing laboratory and library facilities during the mobility period.
You are entitled to request changes to the learning agreement within the deadline decided by the sending and receiving institutions. You are entitled to submit a request for extending the duration of the mobility period to your sending institution.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-TERM MOBILITY INVOLVING THIRD COUNTRIES NOT ASSOCIATED TO THE PROGRAMME</summary>

The base amount for individual support is set as follows: From To Amount EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 1 to 3 and 5 to 12. 700 EUR per month EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 13 and 14. As described above in section “Grant support for the mobility of students – Individual support for physical mobility” Third countries not associated to the Programme from Regions 1-12. Group 1 of EU Member States and third countries associated to the Programme 900 EUR per month Group 2 of EU Member States and third countries associated to the Programme 850 EUR per month Group 3 of EU Member States and third countries associated to the Programme 800 EUR per month
The top-up amount for students and recent graduates with fewer opportunities will apply in this case. The top-up amount for traineeships will apply only in the case of mobility to third countries not associated to the Programme from Regions 13 and 14. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

---

## m01 (multi)

**Question:** Estudio en España y me voy a Alemania. ¿Qué tramo de beca me corresponde y de cuánto es?

**Reference answer:** Spain is Group 2 and Germany Group 1, so the higher range EU grant applies: between 348 and 674 EUR per month (the medium range plus at least 50 EUR).

**Expected location:** programme_guide_2026 67;68

**Assistant's answer:**

> Para una movilidad de estudios desde España a Alemania, te corresponde el **rango superior** de la beca (Higher range EU grant), ya que te desplazas desde un país del Grupo 2 a uno del Grupo 1 (Programme Guide 2026, p. 68).
>
> Los detalles sobre la cuantía son los siguientes:
>
> *   **Grupo de países:** España pertenece al **Grupo 2** (países con costes de vida medios) y Alemania al **Grupo 1** (países con costes de vida más altos) (Programme Guide 2026, pp. 67-68).
> *   **Importe mensual:** El rango establecido por la Comisión Europea para este tipo de movilidad es de entre **348 y 674 EUR al mes** (Programme Guide 2026, p. 68).
> *   **Quién fija la cantidad exacta:** El importe final dentro de ese rango lo define la Agencia Nacional de cada país (en el caso de España, el **SEPIE**) o la propia universidad, basándose en criterios como la disponibilidad de cofinanciación o la demanda de becas (Programme Guide 2026, p. 68).
>
> Para conocer la cifra exacta que recibirás este año, debes consultar la web del SEPIE o contactar con la oficina de relaciones internacionales de tu universidad.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-TERM MOBILITY INVOLVING THIRD COUNTRIES NOT ASSOCIATED TO THE PROGRAMME</summary>

The base amount for individual support is set as follows: From To Amount EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 1 to 3 and 5 to 12. 700 EUR per month EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 13 and 14. As described above in section “Grant support for the mobility of students – Individual support for physical mobility” Third countries not associated to the Programme from Regions 1-12. Group 1 of EU Member States and third countries associated to the Programme 900 EUR per month Group 2 of EU Member States and third countries associated to the Programme 850 EUR per month Group 3 of EU Member States and third countries associated to the Programme 800 EUR per month
The top-up amount for students and recent graduates with fewer opportunities will apply in this case. The top-up amount for traineeships will apply only in the case of mobility to third countries not associated to the Programme from Regions 13 and 14. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Group 2 Countries with medium living costs Cyprus, Czechia, Estonia, Greece, Latvia, Malta, Portugal, Slovakia, Slovenia, Spain. Group 3 Countries with lower living costs Bulgaria, Croatia, Hungary, Lithuania, North Macedonia, Poland, Romania, Serbia, Türkiye. The EU Erasmus+ individual support grant provided to students will depend on their mobility flow between the sending and receiving countries of the student, as follows:
- mobility towards a country with similar living costs: students will receive the medium range EU grant;
- mobility towards a country with higher living costs: students will receive the higher range EU grant;
- mobility towards a country with lower living costs: students will receive the lower range EU grant. The amounts defined by National Agencies will be set within the following minimum and maximum ranges:
- Medium range EU grant: a medium range, between 292 and 606 EUR per month, will apply to mobility activities towards a country of similar living costs: a) from Group 1 to Group 1, b) from Group 2 to Group 2 and c) from Group 3 to Group 3.
- Higher range EU grant: corresponds to the medium range applied by the National Agency plus at least 50 EUR and between 348 and 674 EUR per month. It applies to mobility activities towards a country of higher living costs: a) from Group 2 to Group 1 countries and b) from Group 3 to Group 1 and 2 countries.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

- Lower range EU grant: corresponds to the medium range applied by the National Agency minus at least 50 EUR and between 225 and 550 EUR per month. It applies to mobility activities towards a country of lower living costs: a) Group 1 to Group 2 and 3 countries and b) from Group 2 to Group 3. When defining the amounts to be applied by beneficiaries in their country, National Agencies will consider the following two elements:
- the availability and the level of other sources of co-financing from private or public bodies at local, regional or national level to complement the EU grant;
- the general level of demand of students who intend to study or receive training abroad. For mobility activities between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, National Agencies may decide to grant flexibility to their higher education institutions by fixing ranges instead of amounts at national level. This should be based on justified grounds, for example in countries where co-financing is available at regional or institutional level.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSICAL MOBILITY – BASE AMOUNTS OF INDIVIDUAL SUPPORT (BLENDED MOBILITY AND</summary>

DOCTORAL SHORT-TERM MOBILITY) The base amounts of individual support are set as follows:
Duration of the physical activity Amount (for any EU Member States and third countries associated to the Programme or third country not associated to the Programme) Up to the 14th day of activity 79 EUR per day 15th to the 30th day of activity 56 EUR per day The top-up amount for traineeships will not apply in this case. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

---

## m02 (multi)

**Question:** I'm a Spanish student going to Poland for a semester and I have fewer opportunities. How much do I get per month?

**Reference answer:** Group 2 to Group 3 gives the lower range EU grant (225 to 550 EUR per month), plus the fewer-opportunities top-up of 250 EUR per month.

**Expected location:** programme_guide_2026 68

**Assistant's answer:**

> As a student moving from Spain (Group 2) to Poland (Group 3), you are eligible for the "lower range" EU grant for your base monthly support, plus a top-up for having fewer opportunities (Programme Guide 2026, p. 68).
>
> ### Base Grant
> Because you are moving from a country with medium living costs (Spain) to a country with lower living costs (Poland), you fall into the "lower range" category (Programme Guide 2026, p. 68). The EU sets the range for this category between **225 and 550 EUR per month** (Programme Guide 2026, p. 68).
>
> ### Top-up for Fewer Opportunities
> As a student with fewer opportunities, you receive an additional top-up of **250 EUR per month** on top of your base grant (Programme Guide 2026, p. 68).
>
> ### Important Notes
> *   **Exact Amounts:** The specific amount you will receive within the ranges mentioned above is not set by the European Commission. It is defined by your National Agency (SEPIE in Spain) or your home university (Programme Guide 2026, p. 67).
> *   **Additional Support:** If your personal, physical, mental, or health-related conditions require extra financial support, your university may be able to apply for additional inclusion support to cover supplementary costs (Programme Guide 2026, p. 66).
>
> For the exact amount you will receive, please check the website of your home university's international office or contact SEPIE. They will also be able to provide information on the criteria for the "fewer opportunities" status.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 68, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIES - TOP-UP AMOUNT TO THE INDIVIDUAL SUPPORT FOR LONG-TERM MOBILITY</summary>

Students and recent graduates with fewer opportunities receive a top-up amount to the individual support of their EU Erasmus+ grant with an amount of 250 EUR per month. The criteria to be applied are defined at national level by the National Agencies in agreement with National Authorities.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 70, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIES - TOP-UP AMOUNT TO THE INDIVIDUAL SUPPORT FOR SHORT-TERM PHYSICAL</summary>

MOBILITY Students and recent graduates with fewer opportunities receive a top-up amount to the individual support of their EU Erasmus+ grant of an amount of 100 EUR for a physical mobility activity period of 5-14 days and 150 EUR for the one of 15 - 30 days. The criteria to be applied are defined at national level by the National Agencies in agreement with National Authorities.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 68, STUDENTS AND RECENT GRADUATES ON TRAINEESHIPS - TOP-UP AMOUNT TO THE INDIVIDUAL SUPPORT FOR LONG-TERM MOBILITY</summary>

Students and recent graduates carrying out traineeships receive a top-up amount to the individual support of their EU Erasmus+ grant with an amount of 150 EUR per month. Students and recent graduates with fewer opportunities who take part in traineeships are entitled to receive the top-up amount for students and recent graduates with fewer opportunities and the top-up amount for traineeships.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 66, FUNDING RULES > A) FUNDING RULES APPLICABLE TO ALL MOBILITY ACTIVITIES IN HIGHER EDUCATION</summary>

The number of mobile participants with a zero-grant from EU Erasmus+ funds for the entire mobility period counts in the statistics for the performance indicator used to allocate the EU budget b etween the countries. Participants with fewer opportunities cannot be participants with a zero-grant. For mobility projects supported by internal policy funds, it is possible to implement a ‘partial zero-grant mobility’ where only part of the duration of the physical mobility period is funded by individual support. In this case, mobile participants have to receive individual support for at least the minimum physical mobility period duration. Inclusion support A person with fewer opportunities faces personal, physical, mental or health-related conditions that make participation in the project/mobility action not possible without extra financial or other support. Higher education institutions that include students and/or staff with fewer opportunities among project participants can apply for additional grant support to the National Agency to cover the supplementary costs for their participation in the mobility activities. For participants with fewer opportunities, in particular those with physical, mental or health-related conditions, the grant support may therefore be higher than the maximum individual grant amount set out below. Higher education institutions will describe on their website how students and staff with fewer opportunities can request and justify such additional grant support.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

- Lower range EU grant: corresponds to the medium range applied by the National Agency minus at least 50 EUR and between 225 and 550 EUR per month. It applies to mobility activities towards a country of lower living costs: a) Group 1 to Group 2 and 3 countries and b) from Group 2 to Group 3. When defining the amounts to be applied by beneficiaries in their country, National Agencies will consider the following two elements:
- the availability and the level of other sources of co-financing from private or public bodies at local, regional or national level to complement the EU grant;
- the general level of demand of students who intend to study or receive training abroad. For mobility activities between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, National Agencies may decide to grant flexibility to their higher education institutions by fixing ranges instead of amounts at national level. This should be based on justified grounds, for example in countries where co-financing is available at regional or institutional level.

</details>

<details><summary>[6] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Group 2 Countries with medium living costs Cyprus, Czechia, Estonia, Greece, Latvia, Malta, Portugal, Slovakia, Slovenia, Spain. Group 3 Countries with lower living costs Bulgaria, Croatia, Hungary, Lithuania, North Macedonia, Poland, Romania, Serbia, Türkiye. The EU Erasmus+ individual support grant provided to students will depend on their mobility flow between the sending and receiving countries of the student, as follows:
- mobility towards a country with similar living costs: students will receive the medium range EU grant;
- mobility towards a country with higher living costs: students will receive the higher range EU grant;
- mobility towards a country with lower living costs: students will receive the lower range EU grant. The amounts defined by National Agencies will be set within the following minimum and maximum ranges:
- Medium range EU grant: a medium range, between 292 and 606 EUR per month, will apply to mobility activities towards a country of similar living costs: a) from Group 1 to Group 1, b) from Group 2 to Group 2 and c) from Group 3 to Group 3.
- Higher range EU grant: corresponds to the medium range applied by the National Agency plus at least 50 EUR and between 348 and 674 EUR per month. It applies to mobility activities towards a country of higher living costs: a) from Group 2 to Group 1 countries and b) from Group 3 to Group 1 and 2 countries.

</details>

<details><summary>[7] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

<details><summary>[8] Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-TERM MOBILITY INVOLVING THIRD COUNTRIES NOT ASSOCIATED TO THE PROGRAMME</summary>

The base amount for individual support is set as follows: From To Amount EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 1 to 3 and 5 to 12. 700 EUR per month EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 13 and 14. As described above in section “Grant support for the mobility of students – Individual support for physical mobility” Third countries not associated to the Programme from Regions 1-12. Group 1 of EU Member States and third countries associated to the Programme 900 EUR per month Group 2 of EU Member States and third countries associated to the Programme 850 EUR per month Group 3 of EU Member States and third countries associated to the Programme 800 EUR per month
The top-up amount for students and recent graduates with fewer opportunities will apply in this case. The top-up amount for traineeships will apply only in the case of mobility to third countries not associated to the Programme from Regions 13 and 14. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

<details><summary>[9] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

- Lower range EU grant: corresponds to the medium range applied by the National Agency minus at least 50 EUR and between 225 and 550 EUR per month. It applies to mobility activities towards a country of lower living costs: a) Group 1 to Group 2 and 3 countries and b) from Group 2 to Group 3. When defining the amounts to be applied by beneficiaries in their country, National Agencies will consider the following two elements:
- the availability and the level of other sources of co-financing from private or public bodies at local, regional or national level to complement the EU grant;
- the general level of demand of students who intend to study or receive training abroad. For mobility activities between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, National Agencies may decide to grant flexibility to their higher education institutions by fixing ranges instead of amounts at national level. This should be based on justified grounds, for example in countries where co-financing is available at regional or institutional level.

</details>

<details><summary>[10] Erasmus+ Programme Guide 2026 — pp. 33-34, EU MEMBER STATES AND THIRD COUNTRIES ASSOCIATED TO THE PROGRAMME</summary>

The following countries can fully take part in all the Actions of the Erasmus + Programme: Member States of the European Union (EU) Belgium Bulgaria Czechia Greece Spain France Lithuania Luxembourg Hungary Portugal Romania Slovenia
Note 41: According to Article 33.2 of Council Decision (EU) 2021/1764 of 5 October 2021 on the association of the Overseas Countries a nd Territories with the European Union including relations between the European Union on the one hand, and Greenland and the Kingdom of Denmark on the other (Decision on the Overseas Association, including Greenland) (EUR-Lex - 32021D1764 - EN - EUR-Lex (europa.eu)) the Union shall ensure that individuals and organisations from or to Overseas Countries and Territories (OCT) shall be e ligible for Erasmus+, subject to the rules of the Programme and the arrangements applicable to the Member State with which these OCTs they are conn ected. This means that individuals and organisations from the OCTs are participating in the programme on an 'EU Member State or third country associated to the Programme' status, the 'EU Member State or third country associated to the Programme' being the Member Stat e with which they are connected. The list of OCTs can be found at www.ec.europa.eu/international-partnerships/where-we-work/overseas- countries-and-territories_en.
Denmark Germany Estonia Ireland Croatia Italy Cyprus Latvia Malta Netherlands Austria Poland Slovakia Finland Sweden
Third countries associated to the Programme North Macedonia Serbia Iceland Liechtenstein Norway Türkiye

</details>

---

## m03 (multi)

**Question:** I did 5 months of Erasmus during my bachelor. Can I do a 9-month traineeship after graduating?

**Reference answer:** No. A recent graduate traineeship counts towards the 12-month maximum of the bachelor cycle, so only 7 months are left.

**Expected location:** programme_guide_2026 54;55

**Assistant's answer:**

> Yes, you can potentially do a 9-month traineeship as a recent graduate, provided you stay within the total limit of 12 months of Erasmus+ mobility for your bachelor's cycle.
>
> Here are the key rules regarding your situation:
>
> *   **Total Duration Limit:** You are allowed a maximum of 12 months of physical mobility per study cycle (in your case, the bachelor's cycle) (Programme Guide 2026, p. 54).
> *   **Counting Previous Mobility:** Any previous Erasmus+ mobility you completed during your bachelor's degree counts towards this 12-month limit (Programme Guide 2026, p. 54). Since you have already used 5 months, you have a maximum of 7 months of eligibility remaining for that cycle.
> *   **Recent Graduate Traineeships:** Recent graduates can participate in a traineeship, but it must be completed within one year of obtaining your graduation (Programme Guide 2026, p. 55). Additionally, you must be selected by your higher education institution during your last year of study (Programme Guide 2026, p. 55).
> *   **Important Note:** Because your previous 5 months count toward the 12-month limit, you would only have 7 months of eligibility remaining for a traineeship, not 9 months (Programme Guide 2026, p. 54).
>
> Please note that your home university must opt-in to allow recent graduate traineeships, as they have the option to opt out of this programme (Programme Guide 2026, p. 55). You should contact your university's international office to confirm if they support recent graduate traineeships and to verify your remaining eligibility.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

- during the third cycle as doctoral candidate (doctoral level or EQF level 8). The duration of a traineeship by recent graduates counts towards the 12 months maximum of the cycle during which they apply for the traineeship. The physical mobility period may be interrupted. The interruption period does not count towards the duration of the mobility activity. For traineeships, an enterprise/organisation holiday is not considered as an interruption period. The grant is maintained during that holiday. The holiday period counts towards the minimum duration of a traineeship period. Venue(s) of the activity Students must carry out their physical mobility activity in an EU Member State or third countries associated to the Programme or a third country not associated to the Programme different from the country of the sending organisation and the country where the student has their accommodation during their studies.
Note 66: Prior experience under the Erasmus+ Programme and/or as Erasmus Mundus scholarship holders counts towards the 12 months per study cycle.
Note 67: In one-cycle study programmes, such as medicine, students can be mobile for up to 24 months.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

Any student, in particular those who are not able to participate in a long-term physical mobility for studies or for traineeships, for example, due to their study field or because they have fewer opportunities for participation, may combine a shorter physi cal mobility with a virtual component (blended short-term mobility). In addition, any student may participate in blended intensive programmes. In these cases, physical mobility must last between 5 days and 30 days (excluding travel time) and be combined wi th a compulsory virtual component facilitating collaborative online learning exchange and teamwork. A blended mobility for studies must award a minimum of 3 ECTS credits. Mobility for studies and/or traineeships for doctoral candidates: from 5 to 30 days or from 2 to 12 months of physical mobility (a study mobility may include a complementary traineeship period, if planned), excluding travel time. Total eligible duration per study cycle: The same student may participate in mobility periods totalling up to 12 months of physical mobility maximum per each cycle of study, independently of the number and type of mobility activities:
- during the first study cycle (Bachelor or equivalent) including the short cycle (EQF levels 5 and 6);
- during the second study cycle (Master or equivalent - EQF level 7); and

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

- o a HEI from an EU Member State or third country associated to the Programme awarded with an ECHE, or a HEI from a third country not associated to the Programme recognised by competent authorities that has signed inter-institutional agreements with their partners from an EU Member State or third country associated to the Programme, before the mobility takes place. Duration of the activity Student mobility for studies: from 2 months (or one academic term or trimester) to 12 months of physical mobility, excluding travel time. This can include a complementary traineeship period, if planned, and may be organised in different ways depending on the context: either one activity after the other or both at the same time. The combination follows the funding rules and minimum duration o f study mobility. Student mobility for traineeships: from 2 to 12 months of physical mobility, excluding travel time.
Note 65: The following types of organisations are not eligible as receiving organisations for student mobility for traineeships: EU institutions and other EU bodies including specialised agencies (their exhaustive list is available on the website - http://europa.eu/european-union/about-eu/institutions-bodies_en); organisations managing EU programmes such as Erasmus+ National Agencies (in order to avoid a possible conflict of interests and/or double funding).

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 55, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

Eligible participants Students registered in a HEI and enrolled in studies leading to a recognised degree, including double/joint degrees, or another recognised tertiary level qualification (up to and including the level of doctorate). In case of doctoral mobility, the participant must be at EQF level 8. Recent higher education graduates may participate in a mobility for traineeships. The beneficiary organisation may opt out of recent graduate traineeships. Recent graduates must be selected by their HEI during their last year of study and must carry out and complete their traineeship abroad within one year of obtaining their graduation. Other requirements Student mobility can be in any study field. Student mobility can be a study period combined with a short traineeship (of less than 2 months) while being considered as an overall study period. The student, the sending and the receiving organisation must sign a learning agreement. The study period abroad must be part of the student’s study programme to complete a degree. Wherever possible, the traineeships should be an integrated part of the student’s study programme. Following courses at a higher education institution cannot be considered as a traineeship. In case of blended student mobility, the activities may include participation in courses offered in a blended learning format at any partner HEI, online training and work assignments or participation in blended intensive programmes. Regarding international mobility, see section on “International mobility involving third countries not associated to the Programme”.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 42, MOBILITY PROJECTS FOR HIGHER EDUCATION STUDENTS AND STAFF</summary>

This higher education mobility action supports physical and blended mobility of higher education students in any study field and cycle (short cycle, bachelor, master and doctoral levels). Students can either study abroad at a partner higher education institution or carry out a traineeship in an enterprise, a research institute, a laboratory, an organisation or any other relevant workplace abroad. Students can also combine a study period abroad with a traineeship, further enhancing the learning outcomes and development of transversal skills. While long-term physical mobility is strongly encouraged, this action recognises the need to offer more flexible physical mobility duration to ensure the Programme is accessible to students from all backgrounds, circumstances and study fields. This action also supports higher education teaching and administrative staff to take part in professional development activities abroad as well as staff from the world of work to teach and train students or staff at higher education institutions. These activities may consist of teaching as well as training periods (such as job shadowing, observation periods, training courses). Furthermore, this action supports blended intensive programmes, allowing for groups of higher education institutions to jointly develop blended mobility curricula and activities for students as well as academic and administrative staff.

</details>

---

## m04 (multi)

**Question:** I want to do a 3-week blended programme abroad. What are the rules and how much would I get?

**Reference answer:** It is allowed: 5 to 30 days of physical mobility combined with a compulsory virtual component. For 21 days: 14 x 79 + 7 x 56 = 1,498 EUR.

**Expected location:** programme_guide_2026 54;69

**Assistant's answer:**

> For a 3-week (21-day) blended intensive programme, you must participate in both a short-term physical mobility abroad and a compulsory virtual component that counts towards your learning outcomes (Programme Guide 2026, p. 59). The programme must award at least 3 ECTS credits (Programme Guide 2026, p. 59).
>
> ### Grant Amount
> The grant for your physical mobility is provided by your sending university (Programme Guide 2026, p. 59). The EU sets the following base amounts for individual support for short-term physical mobility:
>
> *   **Up to the 14th day:** 79 EUR per day (Programme Guide 2026, p. 69).
> *   **15th to the 30th day:** 56 EUR per day (Programme Guide 2026, p. 69).
>
> For a 21-day programme, you would receive 79 EUR per day for the first 14 days and 56 EUR per day for the remaining 7 days.
>
> Please note that the exact grant amount you receive is determined by your home university or National Agency. You should contact your university's international office for information regarding the specific selection criteria, application deadlines, and the final amount you will be awarded.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 59, ELIGIBILITY CRITERIA FOR BLENDED INTENSIVE PROGRAMMES</summary>

Blended intensive programmes for students and staff must comprise a short-term physical mobility abroad combined with a compulsory virtual component facilitating a collaborative online learning exchange and teamwork. The virtual component must bring the le arners together online to work collectively and simultaneously on specific assignments that are integrated in the blended intensive programme and count towards the overall learning outcomes. Blended intensive programmes have to award at least 3 ECTS credits for students. To be eligible for organisational support, a blended intensive programme needs to involve a minimum of 10 Erasmus+ mobile learners supported by internal policy funds (not including teaching/training staff involved in the delivery of the pro gramme). These 10 mobile learners must be undertaking their mobility specifically to attend the blended intensive programme through either one of the following Erasmus+ mobility activities: blended short-term student mobility for studies or blended staff mobility for training. The individual support and, when applicable, travel support to participants for the physical activity is provided by the sending HEI (and the receiving HEI in the case of invited staff from enterprises and participants from third countries not associated to the programme funded with external action instruments).

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 72, E) FUNDING RULES APPLICABLE TO BLENDED INTENSIVE PROGRAMMES</summary>

Budget category Eligible costs and applicable rules Amount Organisational Support Costs directly linked to the organisation of the intensive programmes (excluding subsistence and travel for participants). Financing mechanism: contribution to unit costs. Rule of allocation: based on the number of higher education mobile learners funded from mobility projects supported by internal policy funds, not taking into account teachers/trainers involved in the delivery of the programme. The coordinating higher education institution applies for the organisation support on behalf of the group of institutions jointly organising the blended intensive programme. 400 EUR per participant, with a minimum of 10 and a maximum of 20 funded Erasmus+ mobile learners. The organisational support grant for blended intensive programmes is a contribution to any cost incurred by the institutions involved in relation to the organisation of the blended intensive programmes, such as costs related to the preparation, design, development, implementation, and follow-up of the programmes, including the delivery of physical and virtual/remote activities as well as the overall management and coordination. The coordinating HEI is responsible for sharing the organisational support grant for blended intensive programmes among the partnership where the above-mentioned costs are incurred.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 49, PARTICIPATION AND CIVIC ENGAGEMENT</summary>

During these blended intensive programmes, groups of students and/or staff as learners will undertake a short-term physical mobility abroad combined with a compulsory virtual component facilitating collaborative online learning exchange and teamwork. The virtual component must bring the learners together online to work collectively and simultaneously on specific assignments that are integrated in the blended intensive programme and count towards the overall learning outcomes. In addition, blended intensive programmes can be open to student and staff from any HEI, including local students and local staff. Blended intensive programmes build capacity for developing and implementing innovative teaching and learning practices in the participating HEIs. International mobility involving third countries not associated to the Programme The primary focus of the higher education mobility action is to support mobility activities among EU Member States and third countries associated to the Programme – the European dimension.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSICAL MOBILITY – BASE AMOUNTS OF INDIVIDUAL SUPPORT (BLENDED MOBILITY AND</summary>

DOCTORAL SHORT-TERM MOBILITY) The base amounts of individual support are set as follows:
Duration of the physical activity Amount (for any EU Member States and third countries associated to the Programme or third country not associated to the Programme) Up to the 14th day of activity 79 EUR per day 15th to the 30th day of activity 56 EUR per day The top-up amount for traineeships will not apply in this case. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 59, ELIGIBILITY CRITERIA FOR BLENDED INTENSIVE PROGRAMMES</summary>

Venue(s) of the activity The physical activity can take place at the receiving HEI or at any other venue in the country of the receiving HEI. Eligible participants Students: Students registered in a HEI in an EU Member State or a third country associated to the Programme or a third country not associated to the Programme, and enrolled in studies leading to a recognised degree or another recognised tertiary level qualification (up to and including the level of doctorate). Staff: Staff working at a HEI in a n EU Member State or third country associated to the Programme or a third country not associated to the Programme. Teaching and training staff involved in the delivery of the programme:
- Staff working at a HEI in a n EU Member State, third country associated to the Programme or a third country not associated to the Programme.
- Staff invited to teach at a HEI: coming from any public or private enterprise/organisation ( with the exception of HEIs awarded with an ECHE); the enterprise/organisation should come from an EU Member State, third country associated to the Programme or a third country not associated to the Programme active in the labour market or in the fields of education, training and youth, research and innovation; employed doctoral candidates also count as eligible under this action. Other requirements

</details>

---

## m05 (multi)

**Question:** If I change courses during my stay, are the new courses still recognised automatically?

**Reference answer:** Yes, if the change was requested within five weeks of the semester start, agreed by all parties, and the latest version of the learning agreement is signed by all parties.

**Expected location:** learning_agreement_guidelines Exceptional changes to the study programme;Does it count as full automatic recognition if...?

**Assistant's answer:**

> Changes to your courses are not automatically recognised unless they are formally agreed upon by all three parties (you, your sending institution, and your receiving institution) as a revised version of your Learning Agreement (ECHE Guidelines, p. 16).
>
> While the Erasmus+ programme requires full automatic recognition of credits for successfully completed work, this applies to the courses originally agreed upon **or an agreed revised version of the Learning Agreement** (ECHE Guidelines, p. 16).
>
> To ensure your new courses are recognised:
>
> *   **Changes must be exceptional:** Changes to your study programme should be made only in exceptional cases (Learning Agreement guidelines, "Exceptional changes to the study programme").
> *   **Formal approval is required:** Any changes must be agreed upon and validated by all three parties (you, your sending institution, and your receiving institution) (ECHE Guidelines, p. 16).
> *   **Use the correct procedure:** You must indicate the changes in the designated tables (e.g., Tables A2, B2, C2) of your Learning Agreement. The original tables should not be modified; instead, the new tables create a revised version of the agreement (Learning Agreement guidelines, "Exceptional changes to the study programme").
> *   **Respect deadlines:** You can typically initiate these changes within five weeks after the start of each semester, and they should be agreed upon by all parties as soon as possible, ideally within two weeks of your request (Learning Agreement guidelines, "Exceptional changes to the study programme").
>
> If you have questions about the specific process for submitting these changes at your university, please contact your home university's international office.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Practical examples of how to fill in the tables in the digital learning agreement > Exceptional changes to the study programme</summary>

In the case of long-term mobility, changes to the study programme should be exceptional, as the three parties have already agreed on a group of educational components that will be taken abroad, based on the course catalogue that the receiving institution has committed to publish well in advance of the mobility period and to update regularly.
Any party can signal the need for changes to the study programme and the student can initiate the changes within five weeks after the start of each semester. These changes should be agreed by all parties as soon as possible, within two-weeks following the request.
All changes should be indicated in Tables A2, B2 and when applicable C2, or in tables E2 or D2. Original Tables A, B, C, D and E should not be modified. All Tables (A, B, C, A2, B2, C2, D, E, D2 and E2) will be stored together in the relevant server for full transparency as a new version of the LA.
More information about the implementation of versioning can be found in the Erasmus Without Paper technical documentation. Please refer to the glossary provided in the higher education learning agreement for studies KA131 template to see the list of changes that can be encoded.

</details>

<details><summary>[2] Erasmus Charter for Higher Education 2021-2027: Guidelines — pp. 15-16, 1. Student mobility</summary>

The sending HEI should be well-informed about the requirements at the receiving HEI and should provide sufficient guidance to students so that they can make choices acceptable to both partner HEIs. In addition, alternative choices should be explored before the start
Note 4: http://www.coe.int/t/dg4/linguistic/cadre1_en.asp
of the mobility period. Students should be informed that th ey have to respect deadlines and understand that changes to the learning agreement are only possible in exceptional cases. It is good practice to offer incoming students a 2-week period after regular classes have started at the receiving HEI to make approp riate modifications to their learning agreements. Any changes have to be agreed and validated ( e.g. via email, scanned or digital signatures, etc.) by the three parties.
Learning agreements are binding for all three parties and require that, on successful ly completing the mobility period, the sending HEI recognises the credits earned by the student and documents these credits in the student's records, so that they can be identified in a transparent way. All credits that the student earns towards their degr ee during the mobility period and which were originally agreed on in the learning agreement (or an agreed revised version of it) must be recognised by the sending HEI and count ed towards the student’s degree without requiring the student to take any furthe r courses or exams.
Contact details of those responsible for signing and recognising learning agreements should be featured on the HEI's website.

</details>

<details><summary>[3] Erasmus Charter for Higher Education 2021-2027: Guidelines — p. 15, 1. Student mobility</summary>

A cornerstone for successful student mobility (for studies, traineeships and / or a combination of both) and a smooth and transparent transfer of credits is the Learning Agreement. This must be signed by the three parties involved: the student, the sending HEI and the receiving HEI / enterprise / organisation before the mobility takes place.
- a) Student mobility for studies The sending HEI should appoint a member of staff who will advise students in choosing specific modules or other learning/training activit ies at the partner HEIs. Ideally, the same person should have the authority to sign the Learning Agreement and, on the students' return, recognise the credits earned during mobility. In any case the HEI should ensure that the person responsible for recogni tion respects the decision made by the colleague(s) having signed the Learning Agreement. The HEI should also guarantee transparency and reliability of the procedure for mobile students.
All parties should do their utmost to minimise changes to the origin al learning components outlined in learning agreements. To this end, the receiving HEI should provide transparent information on the choices offered and be very clear about the deadlines for registration in the chosen courses (and about any restrictions on place numbers, etc. which might be applicable). Changes to the receiving HEI's course catalogue when students have already started their studies should be avoided as much as possible.

</details>

<details><summary>[4] Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — After the mobility > Automatic recognition at the sending institution</summary>

Higher education institutions must ensure full automatic recognition of all credits (based on the European Credit Transfer and Accumulation System – ECTS) gained for learning outcomes satisfactorily achieved during a period of study/training abroad, including during blended mobility, as agreed in the Erasmus Charter for Higher Education (ECHE).
Following the receipt of the transcript of records from the receiving institution, the sending institution should automatically recognise the student’s academic outcomes successfully completed at the receiving institution as agreed beforehand in the learning agreement and confirmed in the transcript of records.
The sending institution should fully recognise the total number of ECTS credits (or equivalent) contained in Table B, and C when applicable, (and B2 and C2, if applicable) or Tables D or E (and D2 or E2, if applicable) in case of short-term mobility and count them towards the student’s degree, without the need for the student to complete any further assignments, courses or exams.
The process should be in line with the principles of the Council Recommendation on promoting automatic mutual recognition of higher education and upper secondary education diplomas and the outcomes of learning periods abroad.
Where applicable, the sending institution will convert the grades received by the student abroad, taking into account the grade distribution information from the receiving snstitution (see the methodology described in the ECTS Users' Guide ). The European Commission encourages institutions to use the EGRACONS tool for this purpose.
The student will be able to report on the recognition by the sending institution via the online participant report (EU survey) or a complementary online survey.

</details>

<details><summary>[5] Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Practical examples of how to fill in the tables in the digital learning agreement</summary>

(See your own digita learning agreement for original versions of the tables presented below)
In table A, the student must include all the educational components to be carried out at the receiving institution i.e. information about the selected courses or modules as indicated in the course catalogue or other educational components such as laboratory or thesis work. The group of components can then be included in Table B as follows:
CRSX
Course X
Autumn
10
Yes
MDLY
Module Y
Spring
10
Yes
LAB
Laboratory work
Autumn
20
Yes
THS
Thesis research / Doctoral work
Spring
20
Yes
Total: 60
In table B, the option “Yes” for Automatic Recognition is selected by default. By maintaining this default selection, the sending institutions confirms that all credits gained abroad – as agreed in the learning agreement and confirmed by the transcript of records – will be transferred without delay and counted towards the students’ degree without any additional work or assessment of the student.
If the “No” option is selected a clear justification needs to be provided and an indication on what other type of formal recognition will be applied e.g. registration in the students’ diploma supplement or Europass Mobility Document.
The European Commission encourages institutions also to embed mobility windows in their curricula. Where all credits in Table A are automatically recognised as forming part of the programme at the sending institution, typically in the case of mobility windows, Table B is simplified and reduced to one single line, as described below:

</details>

---

## m06 (multi)

**Question:** I have fewer opportunities and want to do a traineeship abroad. Which top-ups can I receive?

**Reference answer:** Both: the fewer-opportunities top-up (250 EUR per month) and the traineeship top-up (150 EUR per month).

**Expected location:** programme_guide_2026 68

**Assistant's answer:**

> If you are a student with fewer opportunities participating in a long-term traineeship, you are entitled to receive two separate top-ups to your individual support grant:
>
> *   **Top-up for students with fewer opportunities:** 250 EUR per month (Programme Guide 2026, p. 68).
> *   **Top-up for traineeships:** 150 EUR per month (Programme Guide 2026, p. 68).
>
> Please note that the criteria for defining "fewer opportunities" are determined at the national level by your National Agency in agreement with national authorities (Programme Guide 2026, p. 68). You should contact your home university's international office to confirm your eligibility and the specific application process.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 68, STUDENTS AND RECENT GRADUATES ON TRAINEESHIPS - TOP-UP AMOUNT TO THE INDIVIDUAL SUPPORT FOR LONG-TERM MOBILITY</summary>

Students and recent graduates carrying out traineeships receive a top-up amount to the individual support of their EU Erasmus+ grant with an amount of 150 EUR per month. Students and recent graduates with fewer opportunities who take part in traineeships are entitled to receive the top-up amount for students and recent graduates with fewer opportunities and the top-up amount for traineeships.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 68, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIES - TOP-UP AMOUNT TO THE INDIVIDUAL SUPPORT FOR LONG-TERM MOBILITY</summary>

Students and recent graduates with fewer opportunities receive a top-up amount to the individual support of their EU Erasmus+ grant with an amount of 250 EUR per month. The criteria to be applied are defined at national level by the National Agencies in agreement with National Authorities.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 70, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIES - TOP-UP AMOUNT TO THE INDIVIDUAL SUPPORT FOR SHORT-TERM PHYSICAL</summary>

MOBILITY Students and recent graduates with fewer opportunities receive a top-up amount to the individual support of their EU Erasmus+ grant of an amount of 100 EUR for a physical mobility activity period of 5-14 days and 150 EUR for the one of 15 - 30 days. The criteria to be applied are defined at national level by the National Agencies in agreement with National Authorities.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-TERM MOBILITY INVOLVING THIRD COUNTRIES NOT ASSOCIATED TO THE PROGRAMME</summary>

The base amount for individual support is set as follows: From To Amount EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 1 to 3 and 5 to 12. 700 EUR per month EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 13 and 14. As described above in section “Grant support for the mobility of students – Individual support for physical mobility” Third countries not associated to the Programme from Regions 1-12. Group 1 of EU Member States and third countries associated to the Programme 900 EUR per month Group 2 of EU Member States and third countries associated to the Programme 850 EUR per month Group 3 of EU Member States and third countries associated to the Programme 800 EUR per month
The top-up amount for students and recent graduates with fewer opportunities will apply in this case. The top-up amount for traineeships will apply only in the case of mobility to third countries not associated to the Programme from Regions 13 and 14. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSICAL MOBILITY – BASE AMOUNTS OF INDIVIDUAL SUPPORT (BLENDED MOBILITY AND</summary>

DOCTORAL SHORT-TERM MOBILITY) The base amounts of individual support are set as follows:
Duration of the physical activity Amount (for any EU Member States and third countries associated to the Programme or third country not associated to the Programme) Up to the 14th day of activity 79 EUR per day 15th to the 30th day of activity 56 EUR per day The top-up amount for traineeships will not apply in this case. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

---

## m07 (multi)

**Question:** Before I leave, what information am I entitled to and what do I have to sign?

**Reference answer:** Information on recognition and grading, insurance, housing and visas; and the learning agreement, which all parties must approve digitally before the mobility starts.

**Expected location:** student_charter;learning_agreement_guidelines Before the mobility period > Your entitlements;Signing the learning agreement

**Assistant's answer:**

> Before you leave for your mobility period, you have specific entitlements regarding information and mandatory documents you must sign.
>
> ### What you must sign
> *   **Grant Agreement:** You must sign a grant agreement with your sending institution (Student Charter, "Before the mobility period > Your obligations and duties").
> *   **Learning Agreement:** You must sign a learning agreement with both your sending and receiving institutions. This document sets out the details of your activities abroad and is the basis for ensuring the automatic recognition of your mobility period (Student Charter, "Before the mobility period > Your obligations and duties"; ECHE Guidelines, p. 15).
> *   **Online Language Assessment:** You are required to undergo an online language assessment through the Online Language Support (if available in the main language of instruction/work) after being selected (Student Charter, "Before the mobility period > Your obligations and duties").
>
> ### What you are entitled to receive
> You are entitled to receive guidance and information on the following:
> *   **Application and Mobility:** Information on the application process, the receiving institution, and the activities available during your mobility (Student Charter, "Before the mobility period > Your entitlements").
> *   **Recognition:** Information on automatic recognition procedures and the grading system used by the receiving institution (Student Charter, "Before the mobility period > Your entitlements").
> *   **Practical Support:** Information on obtaining insurance, finding housing, securing a visa (if required), and support facilities for those with special needs (Student Charter, "Before the mobility period > Your entitlements").
> *   **Financial Support:** You are entitled to receive a pre-financing payment no later than the start date of your mobility period, provided the agreement has been signed by both parties or confirmation of arrival has been received (Student Charter, "Before the mobility period > Your entitlements").
>
> *Note: You should ensure you have health insurance coverage for your stay abroad based on the information provided by your institution (Student Charter, "Before the mobility period > Your obligations and duties").*

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Student Charter — Before the mobility period > Your entitlements</summary>

You are entitled to receive guidance on the application process and information on the receiving institution/ organisation, as well as on activities available for the mobility period abroad.
You are entitled to receive a pre-financing payment within 30 calendar days following the signature of the agreement by both parties or upon receipt of confirmation of arrival, and no later than the start date of the mobility period.
If you are engaging in student mobility for studies, you should be able to sign a digital online learning agreement setting out the details of the activities abroad. If agreed with your institution, you may sign the online learning agreement via the Erasmus+ Mobile Application.
You are entitled to receive information on the automatic recognition procedures and grading system used by the receiving institution.
You are entitled to receive information on obtaining insurance, finding housing, securing a visa (if required), and facilities/support available for those with special needs.

</details>

<details><summary>[2] Erasmus+ Student Charter — Before the mobility period > Your obligations and duties</summary>

You must sign a grant agreement with the sending institution and a learning agreement with the sending and the receiving institution, setting out the details of the activities abroad, which is the basis for ensuring the automatic recognition of your mobility period abroad (through spelling out the credits you are expected to earn and counting them towards your home degree).
You need to undergo an online language assessment free of charge through the Online Language Support after being selected (provided this is available in the main language of instruction / work abroad), so as to evaluate your level and get opportunities to access specific features fitting your language learning needs to make the most of your learning period abroad.
Upon receiving the information and guidance on obtaining insurance from your Higher Education Institution, you should ensure that you have health insurance coverage for your stay abroad. In the case of student mobility for traineeships, you should ensure, together with your traineeship host, that you take up also liability and accident insurance coverage.

</details>

<details><summary>[3] Erasmus+ Student Charter — During the mobility period > Your entitlements</summary>

You are entitled to be treated equally to the home students/employees and not be discriminated against on the basis of your age, ethnic origin, race, nationality, membership of a national minority, culture, language, gender, sexual orientation, marital status, caring or parental responsibilities, illness, ability or disability, mental health status, medical condition, physical appearance, socio-economic background, religious faith or affiliation or lack thereof, political affiliation or opinions or lack thereof, or any other irrelevant distinction.
You are entitled to academic freedom in communicating or sharing ideas and facts, as well as in any potential research you might carry out throughout your mobility period.
You are entitled to benefitting from networks of mentors and buddies where available at the receiving institution/organisation.
You are entitled to be heard in and informed about student organisations on campus, the governance and quality assurance systems of the receiving institution, as well as any relevant student support services (e.g. student unions and student representatives, ombudspersons).
You are entitled to continue receiving the same student grants or loans from your sending country while abroad.
You are entitled to additional financial support, in the form of top-ups, if you are a participant with fewer opportunities or if you choose to travel with green means of transport.
You must not be charged fees for tuition, registration, examinations or for accessing laboratory and library facilities during the mobility period.
You are entitled to request changes to the learning agreement within the deadline decided by the sending and receiving institutions. You are entitled to submit a request for extending the duration of the mobility period to your sending institution.

</details>

<details><summary>[4] Erasmus Charter for Higher Education 2021-2027: Guidelines — p. 15, 1. Student mobility</summary>

A cornerstone for successful student mobility (for studies, traineeships and / or a combination of both) and a smooth and transparent transfer of credits is the Learning Agreement. This must be signed by the three parties involved: the student, the sending HEI and the receiving HEI / enterprise / organisation before the mobility takes place.
- a) Student mobility for studies The sending HEI should appoint a member of staff who will advise students in choosing specific modules or other learning/training activit ies at the partner HEIs. Ideally, the same person should have the authority to sign the Learning Agreement and, on the students' return, recognise the credits earned during mobility. In any case the HEI should ensure that the person responsible for recogni tion respects the decision made by the colleague(s) having signed the Learning Agreement. The HEI should also guarantee transparency and reliability of the procedure for mobile students.
All parties should do their utmost to minimise changes to the origin al learning components outlined in learning agreements. To this end, the receiving HEI should provide transparent information on the choices offered and be very clear about the deadlines for registration in the chosen courses (and about any restrictions on place numbers, etc. which might be applicable). Changes to the receiving HEI's course catalogue when students have already started their studies should be avoided as much as possible.

</details>

<details><summary>[5] Erasmus+ Student Charter — After the mobility period > Your entitlements</summary>

You are entitled to receive full automatic academic recognition from the sending institution for the activities satisfactorily completed during your mobility period, in accordance with the learning agreement.
You are entitled and encouraged to request the Europass Mobility document if you are a recent graduate from a higher education institution located in a Programme Country.
You are entitled to receive a transcript of records, if possible in a digital format, from the receiving institution within five weeks of the publication of your results, showing the credits and grades achieved. Upon receipt of the transcript of records, the sending institution will provide you with complete information on the recognition of your achievements.
If enrolled in a higher education institution located in a Programme Country, you are entitled to have the recognised components included in the Diploma Supplement. You are entitled to receive the Diploma Supplement, if possible, in a digital format, also in its original language version.

</details>

---

## q01 (single)

**Question:** What is the minimum and maximum length of an Erasmus+ study period abroad?

**Reference answer:** From 2 months (or one academic term or trimester) to 12 months of physical mobility, excluding travel time.

**Expected location:** programme_guide_2026 53

**Assistant's answer:**

> The duration of an Erasmus+ study period depends on the type of mobility you choose:
>
> *   **Long-term mobility (standard):** From **2 months** (or one academic term or trimester) to **12 months** of physical mobility (Programme Guide 2026, p. 53).
> *   **Short-term blended mobility:** Between **5 days and 30 days** of physical mobility. This type must be combined with a compulsory virtual component (Programme Guide 2026, p. 54).
> *   **Doctoral mobility:** From **5 to 30 days** or from **2 to 12 months** of physical mobility (Programme Guide 2026, p. 54).
>
> **Important limits:**
> *   **Maximum per cycle:** You can participate in mobility periods totalling up to **12 months** maximum per study cycle (Bachelor, Master, or Doctorate), regardless of the number or type of mobilities (Programme Guide 2026, p. 54).
> *   **One-cycle degrees:** In programmes such as Medicine, the maximum duration is extended to **24 months** (Programme Guide 2026, p. 54).

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

- o a HEI from an EU Member State or third country associated to the Programme awarded with an ECHE, or a HEI from a third country not associated to the Programme recognised by competent authorities that has signed inter-institutional agreements with their partners from an EU Member State or third country associated to the Programme, before the mobility takes place. Duration of the activity Student mobility for studies: from 2 months (or one academic term or trimester) to 12 months of physical mobility, excluding travel time. This can include a complementary traineeship period, if planned, and may be organised in different ways depending on the context: either one activity after the other or both at the same time. The combination follows the funding rules and minimum duration o f study mobility. Student mobility for traineeships: from 2 to 12 months of physical mobility, excluding travel time.
Note 65: The following types of organisations are not eligible as receiving organisations for student mobility for traineeships: EU institutions and other EU bodies including specialised agencies (their exhaustive list is available on the website - http://europa.eu/european-union/about-eu/institutions-bodies_en); organisations managing EU programmes such as Erasmus+ National Agencies (in order to avoid a possible conflict of interests and/or double funding).

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

Any student, in particular those who are not able to participate in a long-term physical mobility for studies or for traineeships, for example, due to their study field or because they have fewer opportunities for participation, may combine a shorter physi cal mobility with a virtual component (blended short-term mobility). In addition, any student may participate in blended intensive programmes. In these cases, physical mobility must last between 5 days and 30 days (excluding travel time) and be combined wi th a compulsory virtual component facilitating collaborative online learning exchange and teamwork. A blended mobility for studies must award a minimum of 3 ECTS credits. Mobility for studies and/or traineeships for doctoral candidates: from 5 to 30 days or from 2 to 12 months of physical mobility (a study mobility may include a complementary traineeship period, if planned), excluding travel time. Total eligible duration per study cycle: The same student may participate in mobility periods totalling up to 12 months of physical mobility maximum per each cycle of study, independently of the number and type of mobility activities:
- during the first study cycle (Bachelor or equivalent) including the short cycle (EQF levels 5 and 6);
- during the second study cycle (Master or equivalent - EQF level 7); and

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

- during the third cycle as doctoral candidate (doctoral level or EQF level 8). The duration of a traineeship by recent graduates counts towards the 12 months maximum of the cycle during which they apply for the traineeship. The physical mobility period may be interrupted. The interruption period does not count towards the duration of the mobility activity. For traineeships, an enterprise/organisation holiday is not considered as an interruption period. The grant is maintained during that holiday. The holiday period counts towards the minimum duration of a traineeship period. Venue(s) of the activity Students must carry out their physical mobility activity in an EU Member State or third countries associated to the Programme or a third country not associated to the Programme different from the country of the sending organisation and the country where the student has their accommodation during their studies.
Note 66: Prior experience under the Erasmus+ Programme and/or as Erasmus Mundus scholarship holders counts towards the 12 months per study cycle.
Note 67: In one-cycle study programmes, such as medicine, students can be mobile for up to 24 months.

</details>

<details><summary>[4] Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Filling in the learning agreement > Learning agreement types and mobility duration</summary>

- Long-term mobility The student should select this mobility type if they are applying to undertake a traditional long-term study mobility abroad with a duration from 2 months (or one academic term or trimester) to 12 months. The student also has the option to add a virtual component, facilitating a collaborative online learning exchange and teamwork, to their study mobility before, during or after. If the student plans to add a virtual component to the mobility period, they must also select the optional virtual component as part of their mobility type.
- Short-term mobility with a mandatory virtual component The student should select this mobility type if they are applying to undertake a short-term physical mobility abroad. Students can carry out a short-term physical mobility of 5-30 days by combining it with a compulsory virtual component, formally organised online activities by the receiving institution, to enhance the learning outcomes of the short-term stay abroad.
- Short-term doctoral mobility Doctoral candidates should select this mobility type when they are applying to undertake a short-term physical mobility of 5-30 days. If the doctoral candidate plans to add a virtual component to the mobility period, they must also select the optional virtual component as part of their mobility type.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 48, PARTICIPATION AND CIVIC ENGAGEMENT</summary>

- A study period abroad at a partner higher education institution. The study period abroad must be part of the student's study programme to complete a degree at any study cycle. A study period abroad may include a traineeship period as well. Such a combination creates synergies between the academic and professional experience abroad. In terms of workload, in countries belonging to the European Higher Education Area (EHEA) an academic year of full - time study is normally made up of educational components totalling 60 ECTS credits (or equivalent units in countries outside the EHEA). It is recommended that for mobility periods shorter than a full academic year, the educational components included in the learning agreement are to be adjusted proportionally.

</details>

---

## q03 (single)

**Question:** I study medicine, which is a one-cycle programme. How long can I be mobile with Erasmus+?

**Reference answer:** In one-cycle study programmes such as medicine, students can be mobile for up to 24 months.

**Expected location:** programme_guide_2026 54

**Assistant's answer:**

> In one-cycle study programmes, such as medicine, you can be mobile for up to **24 months** in total (Programme Guide 2026, p. 54, Note 67).
>
> Here are the specific details regarding this duration:
> *   **Total limit:** While the standard limit for other degrees is 12 months per study cycle, one-cycle programmes have a higher limit of 24 months (Programme Guide 2026, p. 54).
> *   **Prior experience:** Any previous participation in the Erasmus+ programme or as an Erasmus Mundus scholarship holder during the same cycle counts towards this 24-month maximum (Programme Guide 2026, p. 54, Note 66).
> *   **Types of mobility:** This total includes all types of physical mobility, whether for studies or traineeships (Programme Guide 2026, p. 54).
> *   **Individual mobility duration:** Each individual study mobility must last between 2 and 12 months, and each traineeship must also last between 2 and 12 months (Programme Guide 2026, p. 53).

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

- during the third cycle as doctoral candidate (doctoral level or EQF level 8). The duration of a traineeship by recent graduates counts towards the 12 months maximum of the cycle during which they apply for the traineeship. The physical mobility period may be interrupted. The interruption period does not count towards the duration of the mobility activity. For traineeships, an enterprise/organisation holiday is not considered as an interruption period. The grant is maintained during that holiday. The holiday period counts towards the minimum duration of a traineeship period. Venue(s) of the activity Students must carry out their physical mobility activity in an EU Member State or third countries associated to the Programme or a third country not associated to the Programme different from the country of the sending organisation and the country where the student has their accommodation during their studies.
Note 66: Prior experience under the Erasmus+ Programme and/or as Erasmus Mundus scholarship holders counts towards the 12 months per study cycle.
Note 67: In one-cycle study programmes, such as medicine, students can be mobile for up to 24 months.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

Any student, in particular those who are not able to participate in a long-term physical mobility for studies or for traineeships, for example, due to their study field or because they have fewer opportunities for participation, may combine a shorter physi cal mobility with a virtual component (blended short-term mobility). In addition, any student may participate in blended intensive programmes. In these cases, physical mobility must last between 5 days and 30 days (excluding travel time) and be combined wi th a compulsory virtual component facilitating collaborative online learning exchange and teamwork. A blended mobility for studies must award a minimum of 3 ECTS credits. Mobility for studies and/or traineeships for doctoral candidates: from 5 to 30 days or from 2 to 12 months of physical mobility (a study mobility may include a complementary traineeship period, if planned), excluding travel time. Total eligible duration per study cycle: The same student may participate in mobility periods totalling up to 12 months of physical mobility maximum per each cycle of study, independently of the number and type of mobility activities:
- during the first study cycle (Bachelor or equivalent) including the short cycle (EQF levels 5 and 6);
- during the second study cycle (Master or equivalent - EQF level 7); and

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

- o a HEI from an EU Member State or third country associated to the Programme awarded with an ECHE, or a HEI from a third country not associated to the Programme recognised by competent authorities that has signed inter-institutional agreements with their partners from an EU Member State or third country associated to the Programme, before the mobility takes place. Duration of the activity Student mobility for studies: from 2 months (or one academic term or trimester) to 12 months of physical mobility, excluding travel time. This can include a complementary traineeship period, if planned, and may be organised in different ways depending on the context: either one activity after the other or both at the same time. The combination follows the funding rules and minimum duration o f study mobility. Student mobility for traineeships: from 2 to 12 months of physical mobility, excluding travel time.
Note 65: The following types of organisations are not eligible as receiving organisations for student mobility for traineeships: EU institutions and other EU bodies including specialised agencies (their exhaustive list is available on the website - http://europa.eu/european-union/about-eu/institutions-bodies_en); organisations managing EU programmes such as Erasmus+ National Agencies (in order to avoid a possible conflict of interests and/or double funding).

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 55, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY</summary>

Eligible participants Students registered in a HEI and enrolled in studies leading to a recognised degree, including double/joint degrees, or another recognised tertiary level qualification (up to and including the level of doctorate). In case of doctoral mobility, the participant must be at EQF level 8. Recent higher education graduates may participate in a mobility for traineeships. The beneficiary organisation may opt out of recent graduate traineeships. Recent graduates must be selected by their HEI during their last year of study and must carry out and complete their traineeship abroad within one year of obtaining their graduation. Other requirements Student mobility can be in any study field. Student mobility can be a study period combined with a short traineeship (of less than 2 months) while being considered as an overall study period. The student, the sending and the receiving organisation must sign a learning agreement. The study period abroad must be part of the student’s study programme to complete a degree. Wherever possible, the traineeships should be an integrated part of the student’s study programme. Following courses at a higher education institution cannot be considered as a traineeship. In case of blended student mobility, the activities may include participation in courses offered in a blended learning format at any partner HEI, online training and work assignments or participation in blended intensive programmes. Regarding international mobility, see section on “International mobility involving third countries not associated to the Programme”.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 48, PARTICIPATION AND CIVIC ENGAGEMENT</summary>

- A study period abroad at a partner higher education institution. The study period abroad must be part of the student's study programme to complete a degree at any study cycle. A study period abroad may include a traineeship period as well. Such a combination creates synergies between the academic and professional experience abroad. In terms of workload, in countries belonging to the European Higher Education Area (EHEA) an academic year of full - time study is normally made up of educational components totalling 60 ECTS credits (or equivalent units in countries outside the EHEA). It is recommended that for mobility periods shorter than a full academic year, the educational components included in the learning agreement are to be adjusted proportionally.

</details>

---

## q08 (single)

**Question:** ¿En qué grupo de países está España para la beca Erasmus?

**Reference answer:** Spain is in Group 2, countries with medium living costs.

**Expected location:** programme_guide_2026 68

**Assistant's answer:**

> España se encuentra en el **Grupo 2** (países con costes de vida medios) (Programme Guide 2026, p. 68).

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Group 2 Countries with medium living costs Cyprus, Czechia, Estonia, Greece, Latvia, Malta, Portugal, Slovakia, Slovenia, Spain. Group 3 Countries with lower living costs Bulgaria, Croatia, Hungary, Lithuania, North Macedonia, Poland, Romania, Serbia, Türkiye. The EU Erasmus+ individual support grant provided to students will depend on their mobility flow between the sending and receiving countries of the student, as follows:
- mobility towards a country with similar living costs: students will receive the medium range EU grant;
- mobility towards a country with higher living costs: students will receive the higher range EU grant;
- mobility towards a country with lower living costs: students will receive the lower range EU grant. The amounts defined by National Agencies will be set within the following minimum and maximum ranges:
- Medium range EU grant: a medium range, between 292 and 606 EUR per month, will apply to mobility activities towards a country of similar living costs: a) from Group 1 to Group 1, b) from Group 2 to Group 2 and c) from Group 3 to Group 3.
- Higher range EU grant: corresponds to the medium range applied by the National Agency plus at least 50 EUR and between 348 and 674 EUR per month. It applies to mobility activities towards a country of higher living costs: a) from Group 2 to Group 1 countries and b) from Group 3 to Group 1 and 2 countries.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-TERM MOBILITY INVOLVING THIRD COUNTRIES NOT ASSOCIATED TO THE PROGRAMME</summary>

The base amount for individual support is set as follows: From To Amount EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 1 to 3 and 5 to 12. 700 EUR per month EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 13 and 14. As described above in section “Grant support for the mobility of students – Individual support for physical mobility” Third countries not associated to the Programme from Regions 1-12. Group 1 of EU Member States and third countries associated to the Programme 900 EUR per month Group 2 of EU Member States and third countries associated to the Programme 850 EUR per month Group 3 of EU Member States and third countries associated to the Programme 800 EUR per month
The top-up amount for students and recent graduates with fewer opportunities will apply in this case. The top-up amount for traineeships will apply only in the case of mobility to third countries not associated to the Programme from Regions 13 and 14. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — pp. 33-34, EU MEMBER STATES AND THIRD COUNTRIES ASSOCIATED TO THE PROGRAMME</summary>

The following countries can fully take part in all the Actions of the Erasmus + Programme: Member States of the European Union (EU) Belgium Bulgaria Czechia Greece Spain France Lithuania Luxembourg Hungary Portugal Romania Slovenia
Note 41: According to Article 33.2 of Council Decision (EU) 2021/1764 of 5 October 2021 on the association of the Overseas Countries a nd Territories with the European Union including relations between the European Union on the one hand, and Greenland and the Kingdom of Denmark on the other (Decision on the Overseas Association, including Greenland) (EUR-Lex - 32021D1764 - EN - EUR-Lex (europa.eu)) the Union shall ensure that individuals and organisations from or to Overseas Countries and Territories (OCT) shall be e ligible for Erasmus+, subject to the rules of the Programme and the arrangements applicable to the Member State with which these OCTs they are conn ected. This means that individuals and organisations from the OCTs are participating in the programme on an 'EU Member State or third country associated to the Programme' status, the 'EU Member State or third country associated to the Programme' being the Member Stat e with which they are connected. The list of OCTs can be found at www.ec.europa.eu/international-partnerships/where-we-work/overseas- countries-and-territories_en.
Denmark Germany Estonia Ireland Croatia Italy Cyprus Latvia Malta Netherlands Austria Poland Slovakia Finland Sweden
Third countries associated to the Programme North Macedonia Serbia Iceland Liechtenstein Norway Türkiye

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

- Lower range EU grant: corresponds to the medium range applied by the National Agency minus at least 50 EUR and between 225 and 550 EUR per month. It applies to mobility activities towards a country of lower living costs: a) Group 1 to Group 2 and 3 countries and b) from Group 2 to Group 3. When defining the amounts to be applied by beneficiaries in their country, National Agencies will consider the following two elements:
- the availability and the level of other sources of co-financing from private or public bodies at local, regional or national level to complement the EU grant;
- the general level of demand of students who intend to study or receive training abroad. For mobility activities between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, National Agencies may decide to grant flexibility to their higher education institutions by fixing ranges instead of amounts at national level. This should be based on justified grounds, for example in countries where co-financing is available at regional or institutional level.

</details>

---

## q12 (single)

**Question:** How much individual support do I get per day on a short-term physical mobility?

**Reference answer:** 79 EUR per day up to the 14th day, and 56 EUR per day from the 15th to the 30th day.

**Expected location:** programme_guide_2026 69

**Assistant's answer:**

> For a short-term physical mobility, the base amounts for individual support are:
>
> *   **79 EUR per day** up to the 14th day of activity (Programme Guide 2026, p. 69).
> *   **56 EUR per day** from the 15th to the 30th day of activity (Programme Guide 2026, p. 70).
>
> These base amounts apply regardless of the destination country (Programme Guide 2026, p. 69).
>
> ### Additional considerations:
> *   **Students with fewer opportunities:** You can receive a fixed top-up amount of **100 EUR** for a mobility of 5–14 days, or **150 EUR** for a mobility of 15–30 days (Programme Guide 2026, p. 70).
> *   **Traineeships:** The specific top-up amount for traineeships does **not** apply to short-term physical mobility (Programme Guide 2026, p. 70).
> *   **Travel support:** You may also be eligible for a travel grant depending on the distance to your destination and whether you use sustainable means of transport (Programme Guide 2026, pp. 71-72).
>
> For the exact criteria regarding "fewer opportunities" or to confirm the final grant calculation, you should contact your home university's international office or your National Agency (SEPIE in Spain).

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSICAL MOBILITY – BASE AMOUNTS OF INDIVIDUAL SUPPORT (BLENDED MOBILITY AND</summary>

DOCTORAL SHORT-TERM MOBILITY) The base amounts of individual support are set as follows:
Duration of the physical activity Amount (for any EU Member States and third countries associated to the Programme or third country not associated to the Programme) Up to the 14th day of activity 79 EUR per day 15th to the 30th day of activity 56 EUR per day The top-up amount for traineeships will not apply in this case. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 70, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIES - TOP-UP AMOUNT TO THE INDIVIDUAL SUPPORT FOR SHORT-TERM PHYSICAL</summary>

MOBILITY Students and recent graduates with fewer opportunities receive a top-up amount to the individual support of their EU Erasmus+ grant of an amount of 100 EUR for a physical mobility activity period of 5-14 days and 150 EUR for the one of 15 - 30 days. The criteria to be applied are defined at national level by the National Agencies in agreement with National Authorities.

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-TERM MOBILITY INVOLVING THIRD COUNTRIES NOT ASSOCIATED TO THE PROGRAMME</summary>

The base amount for individual support is set as follows: From To Amount EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 1 to 3 and 5 to 12. 700 EUR per month EU Member States and third countries associated to the Programme Third countries not associated to the Programme from Regions 13 and 14. As described above in section “Grant support for the mobility of students – Individual support for physical mobility” Third countries not associated to the Programme from Regions 1-12. Group 1 of EU Member States and third countries associated to the Programme 900 EUR per month Group 2 of EU Member States and third countries associated to the Programme 850 EUR per month Group 3 of EU Member States and third countries associated to the Programme 800 EUR per month
The top-up amount for students and recent graduates with fewer opportunities will apply in this case. The top-up amount for traineeships will apply only in the case of mobility to third countries not associated to the Programme from Regions 13 and 14. The EU Member States and third countries associated to the Programme include outermost regions and OCTs.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — pp. 70-71, C) FUNDING RULES APPLICABLE TO STAFF MOBILITY</summary>

Staff will receive an EU contribution to their costs for subsistence during the period abroad as follows: Budget category Eligible costs and applicable rules Amount Individual support Costs directly linked to the subsistence of participants during the activity. Financing mechanism: contribution to unit costs. Rule of allocation: based on the duration of the stay per participant and the sending and receiving country. Up to the 14th day of activity: table A1.1, per day per participant from EU Member States and third countries associated to the programme or table A1.2, per day per participant from third countries not associated to the programme. Between the 15th and 60th day of activity: 70% of table A1.1, per day per participant from EU Member States and third countries associated to the programme or 70% of table A1.2, per day per participant from third countries not associated to the programme. Payable rates will be rounded to the nearest whole Euro. Table A – Individual support (amounts in euro per day) The amounts depend on the receiving country. These amounts will be set within the minimum and maximum ranges provided in the table below. When defining the amounts to be applied by beneficiaries in their country, National Agencies, in agreement with National Authorities, will consider the following two elements:
- the availability and the level of other sources of co-financing from private or public bodies at local, regional or national level to complement the EU grant;

</details>

---

## q13 (single)

**Question:** What counts as green travel in Erasmus+?

**Reference answer:** Travel using low-emission means of transport (bus, train, bike, car-pooling) for at least half of the round trip; a boat counts if combined with low-emission transport.

**Expected location:** programme_guide_2026 446

**Assistant's answer:**

> Green travel is defined as travel that uses **low emissions means of transport** for at least half of the round trip (Programme Guide 2026, p. 446).
>
> The specific modes of transport that count as green travel include:
> *   **Bus** (Programme Guide 2026, p. 446)
> *   **Train** (Programme Guide 2026, p. 446)
> *   **Bike** (Programme Guide 2026, p. 446)
> *   **Car-pooling** (Programme Guide 2026, p. 446)
>
> Additionally, traveling by **boat** is considered green travel if it is combined with other low-emissions means of transport (Programme Guide 2026, p. 446). 
>
> The Erasmus+ programme promotes these sustainable transport modes to reduce the carbon and environmental footprint of mobility activities (Programme Guide 2026, p. 9, 47).

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Programme Guide 2026 — p. 47, ENVIRONMENTAL SUSTAINABILITY AND GREEN PRACTICES IN HIGHER EDUCATION MOBILITY</summary>

In line with the principles of the ECHE, HEIs must promote environmentally friendly practices in all activities related to the Programme. This means promoting the use of sustainable means of transport for mobility, taking active steps when organising events, conferences and meetings related to Erasmus + mobility in a more environmentally friendly manner, and replacing paper-based administrative processes with digital processes (in line with the standards and timeline of the European Student Card Initiative). HEIs should also raise awareness amongst all participants about various measures they can take while abroad to reduce the carbon and environmental footprints of their mobility activities and monitor progress towards achieving more sustainable student and staff mobility activities.

</details>

<details><summary>[2] Erasmus+ Programme Guide 2026 — p. 9, ENVIRONMENT AND FIGHT AGAINST CLIMATE CHANGE</summary>

The Programme will increase the number of mobility opportunities in green forward-looking domains, which foster the development of competences, enhance career prospects and engage participants in strategic areas for sustainable growth, with special attention to rural development (sustainable farming, management of natural resources, soil protection, bio-agriculture). Moreover, Erasmus+, with mobility at its core, should strive for carbon-neutrality by promoting sustainable transport modes and more environmentally responsible behavior. Environment and the fight against climate change is a horizontal priority in selecting projects. Priority will be given to projects aimed at developing competences in various green sectors, including those within the framework of the contribution from education and culture to sustainable development goals, developing green sectorial skills strategies and methodologies and future-oriented curricula, as well as initiatives that support the planned approaches of the participating organisations regarding environmental sustainability. The Programme supports the use of innovative practices to make learners, staff and youth workers true actors of change (e.g., save resources, reduce energy use, waste and carbon footprint, opt for sustainable food and mobility choices).
Note 9: Implementation guidelines - Erasmus+ and European Solidarity Corps Digital Strategy: https://ec.europa.eu/programmes/erasmus- plus/resources/implementation-guidelines-erasmus-and-european-solidarity-corps-digital_en
Note 10: European Commission – The European Green deal: https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green- deal_en
Note 11: Council recommendation on learning for the green transition and sustainable development: https://eur-lex.europa.eu/legal- content/EN/TXT/PDF/?uri=CELEX:32022H0627(01)
Note 12: Implementation guidelines - Erasmus+ and European Solidarity Corps Green Strategy: https://ec.europa.eu/programmes/erasmus- plus/resources/implementation-guidelines-erasmus-and-european-solidarity-corps-green_en

</details>

<details><summary>[3] Erasmus+ Programme Guide 2026 — p. 446, PART D – GLOSSARY OF TERMS</summary>

Force majeure Any situation or event that prevents organisations and individuals from fulfilling their obligations in the implementation of the project activities. This situation or event has to be unforeseeable, exceptional situation and beyond the parties’ control. The force majeure cannot be due to error or negligence of the organisations or other participants involved in the action, and proves to be inevitable in spite of exercising all due diligence. Green skills Competences and knowledge necessary to the transition to a low-carbon economy, which can be general such as sustainable agriculture, soil protection, energy use and waste reduction, or more technical such as knowledge on renewable energy. Green travel Travel that use s low emissions means of transport for at least half of the round trip, such as bus, train, bike, or car-pooling. Traveling by boat will be considered as green travel if combined with other low-emissions means of transport. Hosting / receiving organisation The (main) organisation that provides learning content to participants in mobility activities by using its own resources and expertise. The hosting organisation cooperates with the sending organisation to define the expected learning outcomes and the metho ds that will be used to achieve them. It then executes the learning programme and conducts monitoring and mentoring during the activity. Informal learning Learning resulting from daily activities and experiences which is not organised or structured in terms of objectives, time or learning support; it may be unintentional from the learner’s perspective.

</details>

<details><summary>[4] Erasmus+ Programme Guide 2026 — p. 10, ENVIRONMENT AND FIGHT AGAINST CLIMATE CHANGE</summary>

Priority will also be given to projects that – through education, training, youth and sport activities - enable behavioural changes for individual preferences, cultural values, awareness, and more generally support active engagement for sustainable development. Therefore, o rganisations and participants involved should strive to incorporate green practices in all projects when designing activities, which will encourage them to discuss and learn about environmental issues, to reflect about local actions and to come up with greener ways of implementing their activities. Platforms such as the European School Education Platform (including eTwinning) and EPALE will continue to produce support materials and facilitate the exchange of effective educational practices and policies for environmental sustainability. Erasmus+ is also a powerful instrument to reach out to and engage with a wide spectrum of players in our society (schools, universities, VET providers, youth and sport organisations, NGOs, local and regional authorities, civil society organisations, etc.) who can become active agents in the transition towards climate neutrality by 2050.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 9, ENVIRONMENT AND FIGHT AGAINST CLIMATE CHANGE</summary>

Environment and climate action are key priorities for the EU now and in the future. The European Green Deal Communication is the European new growth strategy recognis ing the key role of schools, training institutions and universities in engaging with pupils, parents, and the wider community on the changes needed for a successful transition to climate neutral ity by 2050. In addition, the Council Recommendation on learning for the green transition emphasizes the need to provide learners of all ages with opportunities to find out about the climate crisis and sustainability through both formal and non-formal education, and to make learning for the green transition a priority in education and training policies and programmes. Sustainability should become a part of the entire spectrum of education and training, including curricula and professional development for educators, as well as buildings, infrastructure and operations. The Erasmus+ programme is a key instrument for building the knowledge, skills, and attitudes on climate change and supporting sustainable development within the European Union and beyond. In order to implement this policy framework through the Programme, a Strategy on green transition and sustainable development covering all programme fields have been designed with the aim to help programme beneficiaries and implementing actors to successfully develop the green dimension of funded projects.

</details>

---

## q16 (single)

**Question:** ¿Tengo que pagar matrícula en la universidad de destino?

**Reference answer:** No. The host university cannot charge fees for tuition, registration, examinations or access to laboratories and libraries. Small fees (e.g. insurance, student unions) may be charged on the same basis as to local students.

**Expected location:** eche_guidelines;programme_guide_2026;student_charter 8;43;During the mobility period > Your entitlements

**Assistant's answer:**

> No, **no tienes que pagar tasas de matrícula** en la universidad de destino.
>
> Como estudiante de Erasmus+, tienes derecho a que no se te cobren tasas por enseñanza, matrícula, exámenes o acceso a laboratorios y bibliotecas durante tu periodo de movilidad (Erasmus+ Student Charter, "During the mobility period > Your entitlements").
>
> Sin embargo, debes tener en cuenta lo siguiente:
> *   **Pequeñas tasas:** Es posible que debas pagar importes reducidos por conceptos que también pagan los estudiantes locales, como seguros, asociaciones de estudiantes o el uso de materiales diversos como fotocopias o productos de laboratorio (ECHE Guidelines, p. 8).
> *   **Tasas en origen:** Debes seguir pagando la matrícula en tu universidad de origen si así corresponde, ya que mantienes tu derecho a recibir las mismas becas o préstamos nacionales mientras estás en el extranjero (Erasmus+ Student Charter, "During the mobility period > Your entitlements").
> *   **Excepciones:** Solo se pueden cobrar tasas en casos de movilidad para títulos completos (como los Másteres Conjuntos Erasmus Mundus) o si estás registrado en más de una universidad en el contexto de un título conjunto (ECHE Guidelines, p. 9).

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Erasmus+ Student Charter — During the mobility period > Your entitlements</summary>

You are entitled to be treated equally to the home students/employees and not be discriminated against on the basis of your age, ethnic origin, race, nationality, membership of a national minority, culture, language, gender, sexual orientation, marital status, caring or parental responsibilities, illness, ability or disability, mental health status, medical condition, physical appearance, socio-economic background, religious faith or affiliation or lack thereof, political affiliation or opinions or lack thereof, or any other irrelevant distinction.
You are entitled to academic freedom in communicating or sharing ideas and facts, as well as in any potential research you might carry out throughout your mobility period.
You are entitled to benefitting from networks of mentors and buddies where available at the receiving institution/organisation.
You are entitled to be heard in and informed about student organisations on campus, the governance and quality assurance systems of the receiving institution, as well as any relevant student support services (e.g. student unions and student representatives, ombudspersons).
You are entitled to continue receiving the same student grants or loans from your sending country while abroad.
You are entitled to additional financial support, in the form of top-ups, if you are a participant with fewer opportunities or if you choose to travel with green means of transport.
You must not be charged fees for tuition, registration, examinations or for accessing laboratory and library facilities during the mobility period.
You are entitled to request changes to the learning agreement within the deadline decided by the sending and receiving institutions. You are entitled to submit a request for extending the duration of the mobility period to your sending institution.

</details>

<details><summary>[2] Erasmus Charter for Higher Education 2021-2027: Guidelines — pp. 8-9, 1. Fundamental Principles</summary>

In exceptional cases, HEIs in EU Member State or third countries associated to the Programme may use compatible systems if properly justified, but they must give details on the measures they will put in place to implement the ECTS system as soon as possible.
- Charge no fees, in the case of credit mobility, to incoming mobile students for tuition, registration, examinations or access to laboratory and library facilities.
The HEI which receives mobile students engaged i n credit mobility (i.e. students who are mobile within the framework of a degree course at a different HEI) mu st not charge any type of fees for tutoring, registering or examining these students or for their access to laboratories, libraries or other facilities offered to local students.
In certain cases, however, mobile students may be required to pay small fees such as insurance, student unions, use of miscellaneous material such as photocopies, and laboratory products on the same basis as these are charged to local students at the receiving HEI. Details of any such costs should be provided in the receiving HEI' s course catalogue on its website so that students are aware of them before the start of the mobility.
Fees may only be charged in the case of full degree mobility (e.g. Erasmus Mundus Joint Master Degrees) or in the case of students registered at more than one university in the context of a joint master's degree.

</details>

<details><summary>[3] Erasmus+ Student Charter — During the mobility period > Your obligations and duties</summary>

You are encouraged to take full advantage of all the learning opportunities available at the receiving institution/organisation, as well as maximising the benefits of your time abroad by taking an active part in the local society through intercultural or civic engagement activities/projects. You may be charged a small fee (on the same basis as local students) for costs such as insurance, student unions membership or the use of study-related materials and equipment.
You must submit any request to possibly extend the duration of the mobility period at least one month before the end of the originally planned period. Together with the sending and the receiving institutions, you must ensure that the changes to the learning agreement are validated after the request has been submitted.

</details>

<details><summary>[4] Erasmus+ Student Charter — During the mobility period > Your obligations and duties</summary>

You must respect the rules and regulations of the receiving institution/organisation and of the hosting country, including, among others, conduct, health and safety regulations.
You must respect the code of conduct of your receiving institution, by recognising the diversity of the community and not discriminating against others on the basis of their age, ethnic origin, race, nationality, membership of a national minority, culture, language, gender, sexual orientation, marital status, caring or parental responsibilities, illness, ability or disability, mental health status, medical condition, physical appearance, socio-economic background, religious faith or affiliation or lack thereof, political affiliation or opinions or lack thereof, or any other irrelevant distinction. You must act responsibly and respectfully towards your local and academic community. Behaving in a respectful manner towards others implies respecting the law and, among others, that you do not harass or bully others.
You must engage in a behaviour that does not pose any health or safety risk to yourself or others. You must respect the health and safety standards of your institutions/organisations and of the hosting country.
You must respect the principle of academic integrity and endeavour to perform to the best of your ability in all relevant examinations or other forms of assessment.

</details>

<details><summary>[5] Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDENTS</summary>

Individual support for physical mobility – base amounts for long-term mobility Students may receive an individual support grant as a contribution to their additional costs for subsistence related to their period of study or traineeship abroad. For mobility between EU Member States and third countries associated to the Programme and to third countries not associated to the Programme from Regions 13 and 14, the monthly amounts will be defined by the National Agencies in agreement with National Authorities, and/or the HEIs on the basis of objective and transparent criteria as described below. The exact amounts will be published on the websites of National Agencies and of HEIs. EU Member States and third countries associated to the Programme and third countries not associated to the Programme from Regions 13 and 14 are divided into the following three groups: Group 1 Countries with higher living costs Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Italy, Liechtenstein, Luxembourg, Netherlands, Norway, Sweden. Third countries not associated to the Programme from Regions 13 and 14.
Note 78: Third countries not associated to the Programme from regions 13 and 14 are only receiving countries, unless an arrangement is concluded with a neighbouring country to facilitate their participation in the Programme as both sending and receiving country.

</details>

---

## q18 (single)

**Question:** ¿Puedo cambiar las asignaturas de mi learning agreement cuando ya estoy en el destino?

**Reference answer:** Only exceptionally. The student can initiate changes within five weeks after the start of each semester, and all parties should agree within two weeks of the request.

**Expected location:** learning_agreement_guidelines Exceptional changes to the study programme

**Assistant's answer:**

> Sí, puedes cambiar las asignaturas de tu *Learning Agreement* una vez que hayas llegado a tu destino, aunque estos cambios deben ser excepcionales (Learning Agreement guidelines, "Exceptional changes to the study programme").
>
> Estas son las reglas principales para realizar los cambios:
>
> *   **Plazo para solicitarlo:** Debes iniciar los cambios en un plazo de **cinco semanas** tras el inicio de cada semestre (Learning Agreement guidelines, "Exceptional changes to the study programme").
> *   **Aprobación:** Los cambios deben ser acordados por las tres partes (tú, tu universidad de origen y la de destino) lo antes posible, en un plazo de **dos semanas** tras la solicitud (Learning Agreement guidelines, "Exceptional changes to the study programme").
> *   **Procedimiento:** Los cambios no se hacen sobre el documento original, sino que se añaden en secciones específicas (Tablas A2 y B2) del acuerdo de aprendizaje digital (Learning Agreement guidelines, "Exceptional changes to the study programme").
> *   **Validez:** Una vez que todas las partes firman la versión revisada, la universidad de origen está obligada a reconocer los créditos que apruebes según lo acordado (ECHE Guidelines, p. 16).
>
> Es recomendable que consultes con la oficina de relaciones internacionales de tu universidad de origen para conocer si tienen algún procedimiento interno específico o plazos más cortos.

**Retrieved passages** (click to open the text the assistant saw):

<details><summary>[1] Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Practical examples of how to fill in the tables in the digital learning agreement > Exceptional changes to the study programme</summary>

In the case of long-term mobility, changes to the study programme should be exceptional, as the three parties have already agreed on a group of educational components that will be taken abroad, based on the course catalogue that the receiving institution has committed to publish well in advance of the mobility period and to update regularly.
Any party can signal the need for changes to the study programme and the student can initiate the changes within five weeks after the start of each semester. These changes should be agreed by all parties as soon as possible, within two-weeks following the request.
All changes should be indicated in Tables A2, B2 and when applicable C2, or in tables E2 or D2. Original Tables A, B, C, D and E should not be modified. All Tables (A, B, C, A2, B2, C2, D, E, D2 and E2) will be stored together in the relevant server for full transparency as a new version of the LA.
More information about the implementation of versioning can be found in the Erasmus Without Paper technical documentation. Please refer to the glossary provided in the higher education learning agreement for studies KA131 template to see the list of changes that can be encoded.

</details>

<details><summary>[2] Erasmus Charter for Higher Education 2021-2027: Guidelines — pp. 15-16, 1. Student mobility</summary>

The sending HEI should be well-informed about the requirements at the receiving HEI and should provide sufficient guidance to students so that they can make choices acceptable to both partner HEIs. In addition, alternative choices should be explored before the start
Note 4: http://www.coe.int/t/dg4/linguistic/cadre1_en.asp
of the mobility period. Students should be informed that th ey have to respect deadlines and understand that changes to the learning agreement are only possible in exceptional cases. It is good practice to offer incoming students a 2-week period after regular classes have started at the receiving HEI to make approp riate modifications to their learning agreements. Any changes have to be agreed and validated ( e.g. via email, scanned or digital signatures, etc.) by the three parties.
Learning agreements are binding for all three parties and require that, on successful ly completing the mobility period, the sending HEI recognises the credits earned by the student and documents these credits in the student's records, so that they can be identified in a transparent way. All credits that the student earns towards their degr ee during the mobility period and which were originally agreed on in the learning agreement (or an agreed revised version of it) must be recognised by the sending HEI and count ed towards the student’s degree without requiring the student to take any furthe r courses or exams.
Contact details of those responsible for signing and recognising learning agreements should be featured on the HEI's website.

</details>

<details><summary>[3] Erasmus Charter for Higher Education 2021-2027: Guidelines — p. 15, 1. Student mobility</summary>

A cornerstone for successful student mobility (for studies, traineeships and / or a combination of both) and a smooth and transparent transfer of credits is the Learning Agreement. This must be signed by the three parties involved: the student, the sending HEI and the receiving HEI / enterprise / organisation before the mobility takes place.
- a) Student mobility for studies The sending HEI should appoint a member of staff who will advise students in choosing specific modules or other learning/training activit ies at the partner HEIs. Ideally, the same person should have the authority to sign the Learning Agreement and, on the students' return, recognise the credits earned during mobility. In any case the HEI should ensure that the person responsible for recogni tion respects the decision made by the colleague(s) having signed the Learning Agreement. The HEI should also guarantee transparency and reliability of the procedure for mobile students.
All parties should do their utmost to minimise changes to the origin al learning components outlined in learning agreements. To this end, the receiving HEI should provide transparent information on the choices offered and be very clear about the deadlines for registration in the chosen courses (and about any restrictions on place numbers, etc. which might be applicable). Changes to the receiving HEI's course catalogue when students have already started their studies should be avoided as much as possible.

</details>

<details><summary>[4] Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Filling in the learning agreement > Learning agreement types and mobility duration</summary>

- Long-term mobility The student should select this mobility type if they are applying to undertake a traditional long-term study mobility abroad with a duration from 2 months (or one academic term or trimester) to 12 months. The student also has the option to add a virtual component, facilitating a collaborative online learning exchange and teamwork, to their study mobility before, during or after. If the student plans to add a virtual component to the mobility period, they must also select the optional virtual component as part of their mobility type.
- Short-term mobility with a mandatory virtual component The student should select this mobility type if they are applying to undertake a short-term physical mobility abroad. Students can carry out a short-term physical mobility of 5-30 days by combining it with a compulsory virtual component, formally organised online activities by the receiving institution, to enhance the learning outcomes of the short-term stay abroad.
- Short-term doctoral mobility Doctoral candidates should select this mobility type when they are applying to undertake a short-term physical mobility of 5-30 days. If the doctoral candidate plans to add a virtual component to the mobility period, they must also select the optional virtual component as part of their mobility type.

</details>

<details><summary>[5] Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Filling in the learning agreement > Duration</summary>

In addition to selecting the mobility type, the academic year and an indicative start and end date of the planned study programme must be included.
Based on the selection made by the student regarding the above mobility types, the relevant tables need to be filled in and included in the digital learning agreement to describe the study programme and recognition. This means only applicable tables and fields should be visible to the student, sending and receiving organisation in the digital version of the agreement.

</details>
