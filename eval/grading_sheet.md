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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-T; Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSI

---

## u02 (unanswerable)

**Question:** When is the Erasmus application deadline at my university?

**Reference answer:** The documents do not contain student application deadlines; each university sets its own. Ask your international office. (The 19 February deadline in the Programme Guide is for universities applying for funding, not for students.)

**Expected location:** — 

**Assistant's answer:**

> I do not know the application deadline for your university. The official Erasmus+ documents do not contain information about specific university deadlines, selection criteria, or the number of available places.
>
> Please contact your home university's international office directly to ask for their specific application deadlines and selection process.

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 52, ELIGIBILITY CRITERIA OF MOBILITY PROJECTS; Erasmus+ Programme Guide 2026 — p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Erasmus+ Programme Guide 2026 — p. 55, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN

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

**Retrieved passages:** Erasmus Charter for Higher Education 2021-2027: Guidelines — p. 12, 2.1 Before Mobility; Erasmus Charter for Higher Education 2021-2027: Guidelines — pp. 14-15, 2.1 Before Mobility; Erasmus+ Programme Guide 2026 — p. 61, WHAT ARE THE AWARD CRITERIA FOR A MOBILITY PROJECT? >; Erasmus+ Programme Guide 2026 — pp. 44-45, AWARD CRITERIA; Erasmus+ Student Charter — Before the mobility period > Your obligations and duties

---

## u04 (unanswerable)

**Question:** Do I have to pay tax on my Erasmus grant in Spain?

**Reference answer:** The documents do not cover taxation of the grant.

**Expected location:** — 

**Assistant's answer:**

> I do not know if you have to pay tax on your Erasmus grant in Spain. The provided documents do not contain information regarding national tax laws or the tax status of Erasmus+ grants.
>
> For information regarding tax obligations, please contact your local tax authority (Agencia Tributaria in Spain) or your home university's international office, as they can provide guidance on national regulations.

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSI; Erasmus+ Student Charter — Before the mobility period > Your obligations and duties; Erasmus+ Student Charter — During the mobility period > Your entitlements

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 43, HOW TO ACCESS ERASMUS+ HIGHER EDUCATION MOBILITY OPPO; Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — pp. 33-34, EU MEMBER STATES AND THIRD COUNTRIES ASSOCIATED T; Erasmus+ Programme Guide 2026 — pp. 46-47, INCLUSION AND DIVERSITY IN HIGHER EDUCATION MOBIL

---

## u07 (unanswerable)

**Question:** Can my Erasmus grant be paid into a bank account outside Spain, for example a German one?

**Reference answer:** The documents do not cover how or into which bank account the grant is paid; ask the home university, which pays the grant under the student's grant agreement.

**Expected location:** — 

**Assistant's answer:**

> The official Erasmus+ documents do not specify which bank account you must use to receive your grant.
>
> Because this is a procedural detail regarding how your university manages payments, I do not have the answer. You should contact your home university's international office to ask if they allow the grant to be paid into a bank account outside of Spain.

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-T; Erasmus+ Student Charter — Before the mobility period > Your entitlements; Erasmus+ Student Charter — During the mobility period > Your entitlements

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-T; Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSI

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 66, FUNDING RULES > A) FUNDING RULES APPLICABLE TO ALL MO; Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 68, STUDENTS AND RECENT GRADUATES ON TRAINEESHIPS - TOP-U; Erasmus+ Programme Guide 2026 — p. 68, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIE; Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-T; Erasmus+ Programme Guide 2026 — p. 70, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIE; Erasmus+ Programme Guide 2026 — pp. 33-34, EU MEMBER STATES AND THIRD COUNTRIES ASSOCIATED T

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 42, MOBILITY PROJECTS FOR HIGHER EDUCATION STUDENTS AND S; Erasmus+ Programme Guide 2026 — p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Erasmus+ Programme Guide 2026 — p. 55, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 49, PARTICIPATION AND CIVIC ENGAGEMENT; Erasmus+ Programme Guide 2026 — p. 59, ELIGIBILITY CRITERIA FOR BLENDED INTENSIVE PROGRAMMES; Erasmus+ Programme Guide 2026 — p. 72, E) FUNDING RULES APPLICABLE TO BLENDED INTENSIVE PROG; Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSI

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

**Retrieved passages:** Erasmus Charter for Higher Education 2021-2027: Guidelines — p. 15, 1. Student mobility; Erasmus Charter for Higher Education 2021-2027: Guidelines — pp. 15-16, 1. Student mobility; Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — After the mobility > Automatic recognition at the sending in; Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Practical examples of how to fill in the tables in the digit

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 68, STUDENTS AND RECENT GRADUATES ON TRAINEESHIPS - TOP-U; Erasmus+ Programme Guide 2026 — p. 68, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIE; Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-T; Erasmus+ Programme Guide 2026 — p. 70, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIE; Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSI

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

**Retrieved passages:** Erasmus Charter for Higher Education 2021-2027: Guidelines — p. 15, 1. Student mobility; Erasmus+ Student Charter — After the mobility period > Your entitlements; Erasmus+ Student Charter — Before the mobility period > Your entitlements; Erasmus+ Student Charter — Before the mobility period > Your obligations and duties; Erasmus+ Student Charter — During the mobility period > Your entitlements

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 48, PARTICIPATION AND CIVIC ENGAGEMENT; Erasmus+ Programme Guide 2026 — p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Filling in the learning agreement > Learning agreement types

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 48, PARTICIPATION AND CIVIC ENGAGEMENT; Erasmus+ Programme Guide 2026 — p. 53, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Erasmus+ Programme Guide 2026 — p. 54, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY; Erasmus+ Programme Guide 2026 — p. 55, ELIGIBILITY CRITERIA FOR STUDENT MOBILITY

---

## q08 (single)

**Question:** ¿En qué grupo de países está España para la beca Erasmus?

**Reference answer:** Spain is in Group 2, countries with medium living costs.

**Expected location:** programme_guide_2026 68

**Assistant's answer:**

> España se encuentra en el **Grupo 2** (países con costes de vida medios) (Programme Guide 2026, p. 68).

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 68, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-T; Erasmus+ Programme Guide 2026 — pp. 33-34, EU MEMBER STATES AND THIRD COUNTRIES ASSOCIATED T

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Programme Guide 2026 — p. 69, STUDENTS AND RECENT GRADUATES ON INTERNATIONAL LONG-T; Erasmus+ Programme Guide 2026 — p. 70, STUDENTS AND RECENT GRADUATES WITH FEWER OPPORTUNITIE; Erasmus+ Programme Guide 2026 — pp. 69-70, STUDENTS AND RECENT GRADUATES ON SHORT-TERM PHYSI; Erasmus+ Programme Guide 2026 — pp. 70-71, C) FUNDING RULES APPLICABLE TO STAFF MOBILITY

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

**Retrieved passages:** Erasmus+ Programme Guide 2026 — p. 10, ENVIRONMENT AND FIGHT AGAINST CLIMATE CHANGE; Erasmus+ Programme Guide 2026 — p. 446, PART D – GLOSSARY OF TERMS; Erasmus+ Programme Guide 2026 — p. 47, ENVIRONMENTAL SUSTAINABILITY AND GREEN PRACTICES IN H; Erasmus+ Programme Guide 2026 — p. 9, ENVIRONMENT AND FIGHT AGAINST CLIMATE CHANGE

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

**Retrieved passages:** Erasmus Charter for Higher Education 2021-2027: Guidelines — pp. 8-9, 1. Fundamental Principles; Erasmus+ Programme Guide 2026 — p. 67, B) FUNDING RULES APPLICABLE TO THE MOBILITY OF STUDEN; Erasmus+ Student Charter — During the mobility period > Your entitlements; Erasmus+ Student Charter — During the mobility period > Your obligations and duties

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

**Retrieved passages:** Erasmus Charter for Higher Education 2021-2027: Guidelines — p. 15, 1. Student mobility; Erasmus Charter for Higher Education 2021-2027: Guidelines — pp. 15-16, 1. Student mobility; Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Filling in the learning agreement > Duration; Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Filling in the learning agreement > Learning agreement types; Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131) — Practical examples of how to fill in the tables in the digit
