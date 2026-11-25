# Answers to grade

Grade at least 20 of these in `eval/human_labels.csv` (columns: id, correct, supported, notes) **before** you look at `eval/judge.jsonl` or `eval/results.csv`.

- `correct` = 1 if the answer is right against the reference answer (or a proper refusal).
- `supported` = 1 if every claim in it is in the retrieved text shown under it.
- `notes`: why, for every 0.

## q01 (single)

**Question:** It's been three years since my bachelor's. Will the gap count against me?

**Reference answer:** It can be taken into account, but what matters is whether you have sound reasons for returning to study. When assessing your application, caseworkers can consider how long it's been since you last studied and your reasons for coming back to this subject, particularly after a significant gap, along with things like your commitment to the course and how it fits your plans.

**Agent's answer:**

> I can't find this in the documents I have. Check GOV.UK or speak to an international student adviser at your university for guidance on how a gap in your study history may affect a Student visa application.

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Deciding whether the application complies with the time limit requirement]
the applicant is applying to study at a higher education provider (HEP) with a track record of compliance, is subject to the time limit stated in Appendix Student ST 19.3, and is studying for five year’s at degree level, for example: a student is applying for permission to stay to complete their bachelor’s degree, the Student originally enrolled on a 3-year bachelor’s degree but subsequently repeated 2 academic years. Their permission began on 01 August 2021 and, if granted, their subsequent permission would expire on 01 October 2026. This would be permitted as the period only exceeds 5 years on the basis of the extra periods granted before and after the course (5 academic years of study, plus 1 month granted before the course and 4 months granted after the course)
If these circumstances apply, the caseworker must not refuse the application on the basis that the time limit would be breached.
These provisions enable a Student to study for up to 5 academic years without being disadvantaged by any periods of permission in the UK where they are not studying. An example of this could include but is not limited to, the period granted before study and the wrap-up period granted at the end of their course.
For the avoidance of doubt, this concession is not intended to extend the time limits for all applicants. Students who have already undertaken the maximum period of academic study will not benefit. For example, if a Student has already studied for 5 academic years at degree level, they are not eligible to extend their time in the UK for the purpose of commencing a 6th academic year of study at this level.

[student-visa-guide, How long you can stay]
How long you can stay depends on the length of your course and what study you’ve already completed in the UK.
If you’re 18 or over and your course is at degree level, you can usually stay in the UK for up to 5 years. If it’s below degree level, you can usually stay in the UK for up to 2 years.
Read the guidance to find out exactly how long you can stay.

[graduate-visa-guide, Overview]
A Graduate visa gives you permission to stay in the UK for at least 18 months after successfully completing an eligible course in the UK.
You must be in the UK when you apply.
You can apply for a Graduate visa if all of the following are true:
you’re in the UK
your current visa is a Student visa or Tier 4 (General) student visa
you studied a UK bachelor’s degree, postgraduate degree or other eligible course for a minimum period of time with your Student visa or Tier 4 (General) student visa
your education provider (such as your university or college) has told the Home Office you’ve successfully completed your course
You can ask your education provider if you’re not sure whether they’ve told the Home Office you’ve successfully completed your course.
Check if your course is eligible and how long you need to have studied in the UK.
If you’re not eligible for a Graduate visa, you may be eligible for another type of visa to stay in the UK.

[graduate-visa-guide, The course you studied]
To be eligible for a Graduate visa, you need to have successfully completed the course you took with your current Student visa or Tier 4 (General) student visa.
Whether you can apply will also depend on:
the education provider for your course, for example your university or college
the kind of course you took
how long you studied in the UK for
If your education provider allowed you to change course without applying for a new Student visa or Tier 4 (General) student visa, you only need to have completed the course you changed to.

[appendix-student, ST 19.1]
ST 19.1. If the course is below degree level, the grant of permission must not lead to the applicant being granted more than two years’ permission as a Student to study courses below degree level from the age of 18 unless ST 19.2. applies.
ST 19.2. If the course is below degree level but is subject to a regulatory requirement by the Maritime and Coastguard Agency that the applicant must spend at least 12 months at sea as a part of that course, the grant of permission must not lead to the applicant being granted more than 3 years’ permission as a Student from the age of 18 to study courses below degree level.
ST 19.3. If the course is at degree level, the grant of permission must not lead to the applicant being granted more than five years’ permission as a Student from the age of 18 to study courses at degree level unless the course of study is one of those listed at ST 19.4.
ST 19.4. The five-year maximum period of study at degree level in ST 19.3. will not apply if the applicant has a Confirmation of Acceptance for Studies that has been assigned for a course of study in one of the following subjects: (a) architecture; or (b) medicine; or (c) dentistry; or (d) veterinary medicine and science; or (e) music at a music college that is a member of Conservatoires UK; or (f) law, where the applicant has completed a course at degree level or above and is applying for a course of study which is: (i) a law conversion course validated by the Solicitors Regulation Authority and the Bar Standards Board in England and Wales; or (ii) a Masters in Law (MLaw) in Northern Ireland; or (iii) an accelerated graduate LLB in Scotland.

[student-caseworker-guidance, Validity for entry clearance and permission to stay applications]
This page tells caseworkers where to find the validity requirements that an applicant must meet when they apply for entry clearance or permission to stay as a Student, a Child Student or a dependant of a Student.
Before considering any application, the caseworker must check the application is valid by referring to:
the validity requirements for the Student route, contained in Appendix Student ST 1.1 to 1.5
the validity requirements for the Child Student route, contained in Appendix Child Student CS 1.1 to 1.5
the validity requirements for dependants of a Student, contained in Appendix Student ST 28.1 to 28.4
Detailed guidance on how to assess the validity requirements can be found in the Validation, variation, voiding and withdrawing of applications guidance.
The caseworker must conduct verification checks if they have any doubts about whether the supporting documents an applicant has submitted are genuine.
If an applicant has previously had official financial sponsorship from a government or international sponsorship agency, covering both course fees and living costs, it is a validation requirement that they must obtain consent from the financial sponsor to a further application for permission to study in the UK as a Student being made within 12 months of completing that course, or within 12 months of the award of that scholarship if the application is under Child Student. If it is unclear whether a scholarship meets the threshold for requiring consent for future extensions of permission the caseworker may wish to review conditions of the sponsorship / scholarship.

[student-caseworker-guidance, The applicant’s education history, study and post-study plans]
Examples include:
the amount of time that has elapsed since the applicant last studied, and whether the applicant has sound reasons for returning to, or commencing, formal study of this subject, particularly after any significant gap
whether the applicant demonstrates sufficient commitment to the course
whether the course represents academic progression
the credibility of the applicant’s rationale for, knowledge of, and research into the proposed course of study and the sponsoring institution
the credibility of the applicant’s rationale for, knowledge of, and research into living arrangements in the UK
how the circumstances of any dependant may affect the ability or motivation of the applicant to study
the relevance of the course to post-study plans in the UK or overseas
whether the applicant intends to comply with the terms of their permission, including the requirement to leave the UK when their permission comes to an end (or, where lawful and appropriate, to apply to extend their permission under the Student route or to switch to another immigration route)
The caseworker must not refuse an applicant based on an applicant’s knowledge of the location where they will be studying, for example, if the applicant has a lack of knowledge of bus routes, or of the geography of the town or city.

[student-visa-guide, Overview]
You can apply for a Student visa to study in the UK if you’re 16 or over and you:
have been offered a place on a course by a licensed student sponsor
have enough money to support yourself and pay for your course - the amount will vary depending on your circumstances
can speak, read, write and understand English
have consent from your parents if you’re 16 or 17 - you’ll need evidence of this when you apply
If you’re 16 or 17, you may be eligible for a Child Student visa instead.
This visa has replaced the Tier 4 (General) student visa.

[student-visa-guide, Showing academic progress]
If you’re currently studying in the UK, you’ll usually need to show your studies will be at a higher academic level than your current course.
Your new course must be one of the following:
at a higher academic level than your current course
at the same level and related to your previous course or career aspirations - it must be degree level or above at a Higher Education Provider (HEP)
intercalated to a medicine, dentistry or medical science course you started studying under your Student visa (including a Tier 4 (General) student visa)
You do not need to show your studies are at a higher level if you’re doing one of the following:
resitting exams or repeating modules
applying for the first time to a new institution to complete a course you started at an institution that lost its student sponsorship licence
applying after working as a student union sabbatical officer to complete a qualification you started studying under your last Student visa (including a Tier 4 (General) student visa)
completing a PhD or other doctorate that you started studying under your last Student visa (including a Tier 4 (General) student visa)
continuing your medical, dentistry or medical science degree after completing an intercalated course
applying to extend your stay to complete your studies because you’ve done (or want to do) a work placement or study abroad programme
Read the guidance for more information about when you need to prove your studies are at a higher level.

</details>

## q02 (multi)

**Question:** Can I transfer to a different university after I arrive, or do I need a whole new visa?

**Reference answer:** No, not on your current visa: you can only change course without a new application if you stay at the university you're already studying at. To move to a different university you need a new Student visa application before you change course.

**Agent's answer:**

> Under the rules, a Student must only study with the student sponsor that assigned their Confirmation of Acceptance for Studies (CAS), unless they are studying at a partner institution of their sponsor or have a pending application supported by a new CAS [appendix-student, ST 27.1]. 
> 
> While you can change courses internally with your current university under certain conditions without a new visa [student-caseworker-guidance, Students: changing course, without needing permission from the Home Office], transferring to a **completely different university** means changing your student sponsor. To do this, you would need to obtain a new CAS from the new university and submit a new application for permission to stay (a new visa) before you can start studying with them.

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Applying for an integrated course]
The current sponsor must report the change using the Account Management Portal (AMP). The customer service team will update the Home Office IT system to reflect that a different sponsor is teaching the student. The sponsor who is teaching the student will be responsible for the sponsorship duties from the time the student moves to them and during that period. If intercalating at a different sponsor, during this time the sponsor teaching the student must make any relevant reports via AMP. If a student is intercalating at the same sponsor, they do not need to make a new application; the sponsor must report a change of course via the SMS, specifying this was for the purpose of intercalating. Details and information on how to apply for access to AMP can be found here: Study Sector Support.

[appendix-student, ST 27.1]
ST 27.1. A Student must only study with the student sponsor which assigned the Confirmation of Acceptance for Studies unless either: (a) the Student is studying at a partner institution of their student sponsor; or (b) the Student has made an application for permission to stay while they have permission as a Student: (i) which is supported by a valid Confirmation of Acceptance for Studies assigned by a student sponsor; and (ii) the application has not yet been decided, or any Administrative Review against that decision has not been determined; and (iii) the Student will be studying at the student sponsor that assigned the Confirmation of Acceptance for Studies.
ST 27.2. A Student must only study on the course of study, or courses where a combined pre- sessional course is being taken, for which the Confirmation of Acceptance for Studies was assigned unless ST 27.3. applies.

[student-caseworker-guidance, Students and Child Students who want to do a different course of study with their student sponsor]
If a Student applies for further permission to stay to start a new course with the same student sponsor, this will depend on whether they have successfully completed the course for which their permission was granted. In all cases, if a Student requires further permission to complete a course, they will need to meet the current Student route requirements including the academic progression requirement.

[student-visa-guide, Eligibility]
To switch to a Student visa you must:
be in the UK
have an unconditional offer of a place on a course with a licensed student sponsor - shown by your Confirmation of Acceptance for Studies (CAS)
If you’ve been in the UK with a valid visa for less than 12 months, you’ll need to prove you have enough money to support yourself in the UK.
Your partner or children will need to apply separately to switch their visa. They can either apply at the same time as you, or at any time before their current visa expires.

[appendix-student, ST 27.3]
ST 27.3. A Student may begin studying on a new course with their current student sponsor if: (a) the student sponsor is a higher education provider with a track record of compliance; and (b) the Student has not completed the course that the Confirmation of Acceptance for Studies was assigned for; and (c) the new course is not at a lower qualification level than the course the Confirmation of Acceptance for Studies was assigned for unless they were last granted permission to study an integrated master’s or PhD programme and will now be studying on the lower level qualification of that programme.; and (d) the course is at degree level or above; and (e) any new course at degree level can be completed within the current period of permission; and (f) the student sponsor confirms that new course is related to the course for which the Confirmation of Acceptance for Studies was assigned or supports the Student’s genuine career aspirations.
ST 27.4. The Student may study on a study abroad programme overseas that is an integral and assessed part of the course of study named on the Confirmation of Acceptance for Studies.
ST 27.5. Supplementary study is permitted.
ST 27.6. Study is subject to the ATAS condition in Appendix ATAS.

[student-caseworker-guidance, Changing course or finishing their course early]
This page tells caseworkers about the procedure to follow if a Student changes their course or finishes their course early.
Students can apply for a further course of study if they meet the academic progression requirement and the new course of study commences within 28 days of the expiry of their current period of permission. Only some students are able to change course without applying for a new period of permission.
A Student who is applying to extend their permission under the Student route must be academically progressing (unless they are exempt) from demonstrating academic progression), including where they are extending to continue the same course.
A sponsor can only issue a Confirmation of Acceptance for Studies (CAS) to a Student for a change of course if they have a current CAS allocation.

[student-caseworker-guidance, Students: changing course, without needing permission from the Home Office]
Some students may be able to change course without applying for a further period of permission. Students are only able to change course at the HEP which they are studying at, without applying for a further period of permission.
A Student can only change their course within their current period of permission if:
the current licensed Student sponsor is an HEP with a track record of compliance
the new course is at degree level or above
the new course is not at a lower level than the current course
if the course is at degree level, the Student will be able to complete their new course within their current period of permission
the current licensed Student sponsor confirms that: the new course is related to the previous course for which the applicant was granted permission as a Student or Tier 4 (General) Student, (for example, it is connected to the previous course or part of the same subject group); or the previous course and the new course in combination support the applicant’s genuine career aspirations
Students studying at degree level must complete their new course within their existing period of permission unless:
they are applying to re-sit exams or repeat modules
they require further permission because they have previously re-sat exams or repeated modules for their current course
The Student will need to provide evidence when applying for permission that they have attempted exams/modules in line with the academic progression requirements.
The caseworker must not use this provision to allow students to undertake parts of the course for the first time.

[graduate-caseworker-guidance, Confirmation of Acceptance for Studies (CAS)]
If a student has changed course, the sponsoring institution must have notified the Home Office of the change of course via the Sponsor Management System (SMS) prior to the Graduate application being submitted. If the student is awarded a different qualification than is listed on the CAS, the caseworker must check Casework Information Database (CID) or Atlas to confirm that the sponsor has submitted an SMS notification to confirm the change of course. If there is reason to believe a change of course has taken place and the sponsor has not submitted an SMS notification, the caseworker must contact the sponsor to confirm that the change was permitted in accordance with the Immigration Rules and Student Sponsor guidance.
Applicants do not need a new CAS to apply under the Graduate route, but they will need to provide the CAS reference for the relevant Student permission when making an application.
Information shown on the CAS which was linked to the most recent period of permission as a Student or Tier 4 (General) migrant in their immigration history is used to determine whether or not an applicant meets relevant requirements of the Graduate route.

</details>

## q03 (single)

**Question:** If I fail a module and the resit is after my visa expires, can I extend it?

**Reference answer:** Yes, you can apply to extend. An extension normally requires your new studies to be at a higher academic level than your current course, but resitting exams or repeating modules is one of the exceptions, so you don't need to show academic progress for it.

**Agent's answer:**

> Yes, you do not need to show that your studies are at a higher academic level if you are resitting exams or repeating modules [student-visa-guide, Showing academic progress]. 
> 
> To extend your Student visa to complete your studies, you must:
> * Be in the UK on a Student visa or a Tier 4 (General) student visa [student-visa-guide, Extend your visa].
> * Have an unconditional offer of a place on a course with a licensed student sponsor, shown by your Confirmation of Acceptance for Studies (CAS) [student-visa-guide, Extend your visa].
> 
> You should speak to your university's international student advisers or student support team to get your CAS and ensure your application is submitted before your current visa expires.

<details><summary>Retrieved text</summary>

[student-visa-guide, Extend your visa]
You may be able to extend your Student visa to stay longer and continue your course or study a new course. This includes if you currently have a Tier 4 (General) student visa.
To extend your visa you must:
be in the UK on a Student visa or a Tier 4 (General) student visa
have an unconditional offer of a place on a course with a licensed student sponsor - shown by your Confirmation of Acceptance for Studies (CAS)
show that your studies are at a higher academic level than your current course (called the ‘academic progress requirement’) - there are some exceptions
If you’ve been in the UK with a valid visa for less than 12 months, you’ll need to prove you have enough money to support yourself in the UK.
Your partner or children will need to apply separately to extend their visa. They can either apply at the same time as you, or at any time before their current visa expires.
You can also switch to a Graduate visa. This will allow you to stay in the UK after successfully completing your course for:
2 years if you apply on or before 31 December 2026
18 months if you apply on or after 1 January 2027
It will allow you to stay for 3 years if you completed a PhD or other doctoral qualification.

[student-visa-guide, Showing academic progress]
If you’re currently studying in the UK, you’ll usually need to show your studies will be at a higher academic level than your current course.
Your new course must be one of the following:
at a higher academic level than your current course
at the same level and related to your previous course or career aspirations - it must be degree level or above at a Higher Education Provider (HEP)
intercalated to a medicine, dentistry or medical science course you started studying under your Student visa (including a Tier 4 (General) student visa)
You do not need to show your studies are at a higher level if you’re doing one of the following:
resitting exams or repeating modules
applying for the first time to a new institution to complete a course you started at an institution that lost its student sponsorship licence
applying after working as a student union sabbatical officer to complete a qualification you started studying under your last Student visa (including a Tier 4 (General) student visa)
completing a PhD or other doctorate that you started studying under your last Student visa (including a Tier 4 (General) student visa)
continuing your medical, dentistry or medical science degree after completing an intercalated course
applying to extend your stay to complete your studies because you’ve done (or want to do) a work placement or study abroad programme
Read the guidance for more information about when you need to prove your studies are at a higher level.

[student-visa-guide, If you’re applying to work in the UK]
You can get a CAS if you’re applying to work as a student union sabbatical officer.
The earliest you can apply is 3 months before your course starts.
You must apply before your current visa expires. Your new course must begin within 28 days of your current visa expiring.
For example, if your visa expires on 1 December, you must apply for a new visa before 1 December. Your new course must begin by 29 December.
You must also apply within 6 months of getting a Confirmation of Acceptance for Studies (CAS).
You can stay in the UK until you get your decision.
If you applied for an administrative review because your application was refused, you can stay in the UK until you get your review decision.

[student-visa-guide, Fees]
For each person, you’ll need to pay:
£558 to extend this visa
the healthcare surcharge
You’ll need to have your fingerprints and a photo (biometric information) taken - there’s no fee for this.
You must apply online.
As part of your application you’ll need to prove your identity. How you do this depends on where you’re from and the type of passport or resident permit you have.
You’ll either:
use the ‘UK Immigration: ID Check’ app to scan your identity document - you’ll also create or sign in to your UK Visas and Immigration (UKVI) account
have your fingerprints and photo (biometric information) taken at a UK Visa and Citizenship Application Services (UKVCAS) service point
You’ll be told what you need to do when you apply.
Start now
You must not travel outside of the UK, Ireland, the Channel Islands or the Isle of Man until you get a decision. Your application will be withdrawn if you do.

[student-caseworker-guidance, Grant or refuse extension]
This page tells caseworkers how to grant or refuse an application for an extension of permission.
If the applicant meets the requirements of Appendix Student of the Immigration Rules, the caseworker must grant permission to stay with the appropriate work and study conditions.
Students are able to travel outside of, and re-enter, the UK whilst they hold valid permission as a Student, including in the period after they have completed their course and still hold permission under the route.
For more information on the hours that a Student can work, see: Student: employment.

[student-visa-guide, How long it takes to get a decision]
A decision will usually be made within 8 weeks.
You may be able to pay to get a faster decision - you’ll be told if you can when you apply.
You’ll be contacted if your application is complex and will take longer, for example because:
your supporting documents need to be verified
you need to attend an interview
of your personal circumstances (for example if you have a criminal conviction)
If you need to change something in your application after you’ve sent it contact UK Visas and Immigration (UKVI).
You can ask to withdraw your application by contacting UKVI. Your fee will only be refunded if UKVI has not started processing your application.

</details>

## q04 (unanswerable)

**Question:** What happens to my visa if I need to take a medical break from my course?

**Reference answer:** I can't find this in the documents I have. Your university's international student advice team can explain how a break from your studies would affect your visa.

**Agent's answer:**

> I can't find this in the documents I have. Please check GOV.UK or speak to an international student adviser at your university for guidance on how a medical break affects your Student visa.

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Student: Visa Brake]
Afghanistan, Cameroon, Myanmar and Sudan will be subject to a visa brake from 00:01 GMT 26 March 2026. You must refuse any out-of-country Student entry clearance applications submitted on or after this date where the main applicant is a national or citizen of one of these countries, in accordance with paragraph ST 3.3. You should assess an applicant’s suitability in full, but no further consideration of the applicant’s wider eligibility should be undertaken.
The visa brake only affects out-of-country applications where the main applicant has made their application using a passport or travel document which confirms that they are a national of one of the affected countries. Any applications made by dual nationals in a different nationality should be considered as normal in line with that nationality.

[student-caseworker-guidance, Student: postgraduate doctors and dentists]
The requirements to obtain permission as a Student to study as a postgraduate doctor or dentist were removed from Appendix Student on 9 April 2025. They enabled students sponsored by Health Education England (HEE) following a recognised foundation programme as a doctor or dentist to obtain Student permission for up to 3 years.
Applicants must have completed a recognised degree in medicine or dentistry in the UK whilst holding permission as a Student for at least 2 academic years, which must have included the final year, of their UK bachelor’s degree or above in medicine or dentistry.
Applicants were exempt from the financial requirement and did not need to show funds. Successful applicants were issued permission for the length of their placement, up to the maximum of 3 years, plus a 1 month post study period.

[student-visa-guide, How long it takes to get a decision]
You’ll usually get a decision within 8 weeks.
You may be able to pay to get a faster decision.
You’ll be contacted if your application is complex and will take longer, for example because:
your supporting documents need to be verified
you need to attend an interview
of your personal circumstances (for example if you have a criminal conviction)
If you need to change something in your application after you’ve sent it contact UK Visas and Immigration (UKVI).
You can ask to withdraw your application by contacting UKVI. Your fee will only be refunded if UKVI has not started processing your application.

[appendix-student, ST 14.4]
ST 14.4. An applicant does not need to show academic progress where they: (a) are applying to re-sit examinations or repeat modules under ST 14.5.; or (b) have previously re-sat examinations or repeated modules under ST 14.5. and are applying to complete the course for which those examinations were re-sat or modules repeated; or (c) are applying to: (i) continue studying with their current student sponsor; or (ii) move to a new student sponsor to enable them to follow their academic supervisor to another institution, for the purpose of completing the PhD or other doctoral qualification for which study was undertaken during their last period of permission as a Student; or (d) are making an application to move to a new student sponsor to complete a course of study begun at a student sponsor that has subsequently had its licence revoked; or (e) are applying to undertake a role as a Student Union Sabbatical Officer; or (f) after undertaking a period as a Student Union Sabbatical Officer are applying to complete the qualification for which the Confirmation of Acceptance for Studies was assigned before that period; or (g) DELETED (h) are applying to undertake an intercalated bachelor’s or master’s degree course or PhD where they are studying medicine, veterinary medicine and science, or dentistry as their principal course of study, or to complete their principal course, having completed a period of intercalation; or (i) are applying to undertake a study abroad programme or work placement which is both integral to and assessed as part of the course, or to complete their course, having completed a study abroad programme or work placement.
ST 14.5. If the applicant is sponsored by a probationary sponsor, they must not previously have re-sat the same examination or repeated the same module, more than once (they can only do so twice).

[student-caseworker-guidance, Changing course or finishing their course early]
This page tells caseworkers about the procedure to follow if a Student changes their course or finishes their course early.
Students can apply for a further course of study if they meet the academic progression requirement and the new course of study commences within 28 days of the expiry of their current period of permission. Only some students are able to change course without applying for a new period of permission.
A Student who is applying to extend their permission under the Student route must be academically progressing (unless they are exempt) from demonstrating academic progression), including where they are extending to continue the same course.
A sponsor can only issue a Confirmation of Acceptance for Studies (CAS) to a Student for a change of course if they have a current CAS allocation.

[student-caseworker-guidance, Student sponsorship duties]
Student sponsors have a range of sponsorship duties which they must fulfil; these include record keeping and reporting duties. For example, a student sponsor must keep a copy of the student’s:
passport
digital status
UK immigration status document (the student must keep the original)
contact details
Further details of the record-keeping duties of a sponsor can be found in section 2 of the student sponsorship duties guidance.
A student sponsor must report to the Home Office if:
a student fails to enrol on their course within the enrolment period
the institution is not a higher education provider and a sponsored student misses 10 consecutive contact points and an exception does not apply (see student sponsor guidance for further details)
the institution is a higher education provider and a sponsored student fails to academically engage with the course after meeting one of the indicators set out in the academic engagement policy, and does not re-engage after intervention by the sponsor (see student sponsor guidance for further details)
the student sponsor ceases to be the student’s sponsor for any reason (for example, if the student moves in to an immigration category that does not need a student sponsor)
there are any significant changes in the student’s circumstances (for example, if the length of a course of study is shortened, or if the student sponsor suspects the student of breaking any conditions of their permission to stay)

[student-caseworker-guidance, Applying for an integrated course]
The current sponsor must report the change using the Account Management Portal (AMP). The customer service team will update the Home Office IT system to reflect that a different sponsor is teaching the student. The sponsor who is teaching the student will be responsible for the sponsorship duties from the time the student moves to them and during that period. If intercalating at a different sponsor, during this time the sponsor teaching the student must make any relevant reports via AMP. If a student is intercalating at the same sponsor, they do not need to make a new application; the sponsor must report a change of course via the SMS, specifying this was for the purpose of intercalating. Details and information on how to apply for access to AMP can be found here: Study Sector Support.

[student-caseworker-guidance, Student sponsor subject to UKVI sanctions, under investigation, licence revoked, surrendered or expired]
This page tells caseworkers how to deal with applications for entry clearance or permission to stay where a student sponsor:
has been removed from the register of student sponsors pending investigation
has had their licence revoked, has surrendered their licence or the licence has expired

[student-caseworker-guidance, Sponsor has had their licence revoked, or the licence has been surrendered or expired]
Student’s position | Action to take; Student has extant permission and no application pending | If the curtailment caseworker believes that a student has not been a genuine student at their institution, or that the student participated in the practices that contributed to the sponsor’s licence being revoked, they must immediately curtail the student’s permission. The student will then have to leave the UK or face enforced removal. UKVI Sponsorship must consider whether to allow some or all of the sponsor’s students to continue to be taught by the sponsor for a limited period, if its sponsored students were not complicit in the practices that led to the licence revocation (some examples of complicit behaviour are where the sponsored students enrol with a sponsor, knowing that it will not genuinely teach them or where they are taking advantage of the sponsor’s lack of effective attendance management or academic engagement policies, as applicable, and not attending their studies). If this ‘teach out’ of sponsored students is allowed, no action must be taken against students who are genuinely continuing to study with the former sponsor during the limited period. Further information is available in Document 3 of the Student sponsor guidance. If UKVI Sponsorship do not allow some or all of the sponsor’s students to continue to be taught by the sponsor for a limited period, the caseworker must write to the students who are not allowed to continue, curtailing their permission to expire 60 calendar days from the date of their letter on the basis that their sponsor no longer has a licence (unless the student has less than 60 days of permission remaining or there are exceptional reasons to curtail to another date, as set out in the curtailment guidance). During this time, the students may find a new sponsor,

[student-caseworker-guidance, Zero Confirmation of Acceptance for Studies (CAS) allocated sponsors]
A sponsor that holds student sponsor status but does not apply in time or does not pass an Educational Oversight inspection, or a statutory education inspection, will have its CAS allocation set to zero and therefore cannot sponsor any further students until it regains Educational Oversight and is given a new CAS allocation.

</details>

## q05 (unanswerable)

**Question:** If I drop out halfway through the year, how long can I stay in the UK?

**Reference answer:** I can't find this in the documents I have. Your university's international student advice team can tell you what happens to your visa if you leave your course.

**Agent's answer:**

> I can't find this in the documents I have. Please check GOV.UK or speak to your university's international student advisers for guidance on how dropping out affects your visa status.

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Sponsor has had their licence revoked, or the licence has been surrendered or expired]
Student’s position | Action to take; Student has extant permission and no application pending | If the curtailment caseworker believes that a student has not been a genuine student at their institution, or that the student participated in the practices that contributed to the sponsor’s licence being revoked, they must immediately curtail the student’s permission. The student will then have to leave the UK or face enforced removal. UKVI Sponsorship must consider whether to allow some or all of the sponsor’s students to continue to be taught by the sponsor for a limited period, if its sponsored students were not complicit in the practices that led to the licence revocation (some examples of complicit behaviour are where the sponsored students enrol with a sponsor, knowing that it will not genuinely teach them or where they are taking advantage of the sponsor’s lack of effective attendance management or academic engagement policies, as applicable, and not attending their studies). If this ‘teach out’ of sponsored students is allowed, no action must be taken against students who are genuinely continuing to study with the former sponsor during the limited period. Further information is available in Document 3 of the Student sponsor guidance. If UKVI Sponsorship do not allow some or all of the sponsor’s students to continue to be taught by the sponsor for a limited period, the caseworker must write to the students who are not allowed to continue, curtailing their permission to expire 60 calendar days from the date of their letter on the basis that their sponsor no longer has a licence (unless the student has less than 60 days of permission remaining or there are exceptional reasons to curtail to another date, as set out in the curtailment guidance). During this time, the students may find a new sponsor,

[student-caseworker-guidance, Changing course or finishing their course early]
This page tells caseworkers about the procedure to follow if a Student changes their course or finishes their course early.
Students can apply for a further course of study if they meet the academic progression requirement and the new course of study commences within 28 days of the expiry of their current period of permission. Only some students are able to change course without applying for a new period of permission.
A Student who is applying to extend their permission under the Student route must be academically progressing (unless they are exempt) from demonstrating academic progression), including where they are extending to continue the same course.
A sponsor can only issue a Confirmation of Acceptance for Studies (CAS) to a Student for a change of course if they have a current CAS allocation.

[student-caseworker-guidance, The Student or Child Student has not completed the course which their current permission was granted for]
The ability to change course is dependent on a student’s conditions. The conditions and circumstances in which students can change courses are set out under Changing A-level subjects and Students: changing course, without needing permission from the Home Office.
If a student wants to change their current course but, under their conditions of permission they are not permitted to do so, they need to make a new Student or Child Student application from overseas before changing course.

[student-caseworker-guidance, The Student or Child Student has completed the course for which they were given permission to stay]
If the student has successfully completed the course the Confirmation of Acceptance for Studies (CAS) was issued for, they will need to make a new application for permission to stay for their new course.
The student must make a valid application that meets the date of application requirement. To be able to begin their course before a decision has been made, the following must be true:
the sponsor has Student Sponsor status;
the sponsor has assigned them a CAS;
they applied to us before starting their course; and
they applied to us before their existing permission to stay expired.
To be able to begin their new course before submitting a valid application for further permission as a Student the following must be true:
the student is studying at a HEP that has a track record of compliance;
the student is currently sponsored by them and has finished their last course;
the student’s permission to stay has not yet expired; and
the student will be studying their new course with their existing sponsor;
In all other circumstances a student must make an application for permission to stay and must not start their new course until the Home Office have approved their new application.
If a student has left an integrated masters or PhD programme with the lower level qualification, this will be deemed to be successfully completing the course of study for which the CAS was assigned. These students will be able to meet the academic progression requirement for an in-country application, if the course of study listed on the CAS is at the same level or higher than the level of study on the previous CAS issued for the integrated programme.

[student-caseworker-guidance, Students and Child Students who want to do a different course of study with their student sponsor]
If a Student applies for further permission to stay to start a new course with the same student sponsor, this will depend on whether they have successfully completed the course for which their permission was granted. In all cases, if a Student requires further permission to complete a course, they will need to meet the current Student route requirements including the academic progression requirement.

[student-caseworker-guidance, Student sponsorship duties]
Student sponsors have a range of sponsorship duties which they must fulfil; these include record keeping and reporting duties. For example, a student sponsor must keep a copy of the student’s:
passport
digital status
UK immigration status document (the student must keep the original)
contact details
Further details of the record-keeping duties of a sponsor can be found in section 2 of the student sponsorship duties guidance.
A student sponsor must report to the Home Office if:
a student fails to enrol on their course within the enrolment period
the institution is not a higher education provider and a sponsored student misses 10 consecutive contact points and an exception does not apply (see student sponsor guidance for further details)
the institution is a higher education provider and a sponsored student fails to academically engage with the course after meeting one of the indicators set out in the academic engagement policy, and does not re-engage after intervention by the sponsor (see student sponsor guidance for further details)
the student sponsor ceases to be the student’s sponsor for any reason (for example, if the student moves in to an immigration category that does not need a student sponsor)
there are any significant changes in the student’s circumstances (for example, if the length of a course of study is shortened, or if the student sponsor suspects the student of breaking any conditions of their permission to stay)

[student-caseworker-guidance, Demonstrating course completion]
An applicant can use the formal award of a qualification to demonstrate having successfully completed their course. If the formal award has not yet been issued, and the applicant is studying a course at degree level or above at a sponsor who is a HEP with a track record of compliance, then the sponsor can provide formal written confirmation that the applicant is highly likely to complete their course.
To provide formal written confirmation, the current sponsor must assess the applicant’s academic ability to complete their current course successfully. The confirmation provided must state that the sponsor considers the applicant highly likely to complete their course successfully, based on the sponsor’s assessment, and the applicant’s performance throughout the course. The formal written confirmation should also give an indication of when the qualification will be awarded.
The caseworker must check that the sponsor has noted on the CAS that the applicant’s offer is based on formal written confirmation of course completion. If an applicant does not in fact successfully complete their first course, the sponsor which assigned the CAS for the first course will be required to notify UKVI and withdraw sponsorship of the applicant.
If a sponsor is offering a course on the basis of a formal written confirmation that an applicant is highly likely to complete their current course, the applicant must complete their current course before or on the completion date stated in the formal written confirmation. If an applicant does not successfully complete their course within the completion date stated in the formal written confirmation, then the sponsor assigning the new CAS will be required to notify UKVI and withdraw sponsorship of the applicant.

[student-caseworker-guidance, Sponsor has had their licence revoked, or the licence has been surrendered or expired]
variation application and provides a new CAS within the specified 60 calendar day period If the applicant has extant permission, and there are other grounds for refusing the application – including if the caseworker believes that a student is not a genuine student (and therefore does not meet the requirement of the genuine student rule), or that the student participated in the practices that may have contributed to the sponsor’s licence being revoked (and therefore must be considered for refusal on the grounds set out in Part Suitability, for example using deception or breaching the conditions of their permission, depending on the circumstances of their case) – then they must refuse the application on the basis of the requirements in the Immigration Rules that the applicant fails to meet. The caseworker must also refer the case to the curtailment team so that curtailment can be considered; do this by NotificationsandCurtailmentsTeam@homeoffice.gov.uk with the details of the case.

[student-caseworker-guidance, Sponsor has had their licence revoked, or the licence has been surrendered or expired]
and apply for further permission to stay. If such a student does not make an application, they will have to leave the UK, or face enforced removal, when their permission expires.; Student has submitted an entry clearance application | The Confirmation of Acceptance for Studies (CAS) will be invalid on the day the sponsor licence is revoked, surrendered or expires. The caseworker must refuse the application on the basis that it does not meet the requirement to be supported by a valid CAS.; Student has submitted a permission to stay application | The Confirmation of Acceptance for Studies (CAS) will be invalid on the day the sponsor licence is revoked, surrendered or expires. The caseworker must consider the application, including whether to refer for a credibility interview. The caseworker must delay the refusal of a student’s application if the only ground for refusal is that the student’s CAS has become invalid following the revocation of a sponsor’s licence. The caseworker must give the student 60 days to vary their application, or to leave the UK. To do this, the caseworker must: - write to the student telling them the date by which they must make a variation application if they intend to do so, and the date by which to provide a new CAS if they intend to vary their application by making a further Student application - consider the original application on the basis of the evidence which was submitted with it, and any other relevant available evidence or information, if the applicant fails to make a Student variation application and provide a new CAS within the specified 60 calendar day period, or vary their application to a different type - consider the new application as normal, including considering referring for a credibility interview, if the applicant makes a

[student-caseworker-guidance, Student sponsor subject to UKVI sanctions, under investigation, licence revoked, surrendered or expired]
This page tells caseworkers how to deal with applications for entry clearance or permission to stay where a student sponsor:
has been removed from the register of student sponsors pending investigation
has had their licence revoked, has surrendered their licence or the licence has expired

</details>

## q06 (multi)

**Question:** I want to start a PhD straight after my master's. Can I apply from inside the UK, or do I have to go home?

**Reference answer:** Yes, you can apply from inside the UK by extending your Student visa, as long as you have an unconditional offer shown on a CAS and the PhD is at a higher academic level than your master's, which it is. You can apply up to 3 months before the PhD starts, but you must apply before your current visa expires and within 6 months of getting your CAS, and the PhD must start within 28 days of your current visa expiring. You can stay in the UK while you wait for the decision.

**Agent's answer:**

> Yes, you can apply from inside the UK to extend your Student visa and start your PhD, provided you meet the requirements [student-visa-guide, Extend your visa]. 
> 
> To apply from within the UK, you must:
> * Be in the UK with a valid Student visa (or a Tier 4 (General) student visa) [student-visa-guide, Extend your visa].
> * Have an unconditional offer of a place on a course with a licensed student sponsor, which is shown by your Confirmation of Acceptance for Studies (CAS) [student-visa-guide, Extend your visa].
> * Meet the academic progress requirement [student-visa-guide, Extend your visa]. Since a PhD is a higher academic level than a master’s degree, moving from a master's to a PhD typically satisfies this requirement [appendix-student, ST 14.3].
> * If you have been in the UK with a valid visa for less than 12 months, you will also need to prove you have enough money to support yourself [student-visa-guide, Extend your visa].

<details><summary>Retrieved text</summary>

[appendix-student, ST 14.3]
ST 14.3. An applicant will show academic progress if they are applying for any of the following: (a) to progress from a bachelor’s to master’s level course which is part of an integrated master’s course, where the applicant has been offered a place on a higher-level course by the student sponsor after an assessment of their academic ability; or (b) to progress from a master’s degree to a PhD which is part of an integrated master’s and PhD programme, where the applicant has been offered a place on a higher-level course by the student sponsor after an assessment of their academic ability; or (c) a course which is above the level of the previous course of study for which they were last granted permission unless: (i) the student sponsor is a higher education provider with a track record of compliance; and (ii) the course is at degree level or above; and (iii) the new course is at the same level as the previous course of study; and (iv) the student sponsor confirms that either: (a) the new course of study is related to the applicant’s previous course of study (meaning that it is either connected to the previous course, part of the same subject group, or involves deeper specialisation); or (b) the combination of the previous course of study and the new course of study support the applicant’s genuine career aspirations. (c) the applicant has left an integrated master’s or PhD programme having successfully completed the course leading to the award of the lower level qualification which formed a part of that programme.

[appendix-student, ST 14.1]
ST 14.1. An applicant who has, or previously had, permission as a Student and is applying for permission to stay as a Student must have successfully completed the course of study for which they were last granted permission as a Student or one of the following applies: (a) one of the exceptions in ST 14.4.; or (b) they are applying to progress to a higher level course as specified in ST 14.3.(a) or (b).; or (c) they have successfully completed the course of study for which they were last granted permission as a Student or the course of study they were allowed to change to without applying for further permission on the Student route and will now be taking a course at the same level as specified at ST 14.3(c); or (d) they have successfully completed the course of study with their sponsor where the change of course was allowed without applying for further permission on the Student route.
ST 14.2. An applicant who has, or previously had, permission on the Student route and is applying for permission to stay as a Student must show academic progress from the previous courses of study unless one of the exceptions in ST 14.4. applies.

[student-caseworker-guidance, Demonstrating academic progression]
All applicants who have previously been granted permission as a Student or a Tier 4 (General) Student, and are applying from within the UK to extend their stay need to have successfully completed their previous course unless:
they are progressing onto an integrated master’s or PhD programme at the higher level of that programme
an exception set out at Appendix Student ST 14.4 applies
Unless an exception at Appendix Student ST 14.4 applies applicants will also need to show that the course for which their CAS has been issued is at a higher level than their previous course. A new course at the same level is only permitted if:
the student sponsor is a higher education provider with a track record of compliance
the course of study is at degree level or above
the sponsor confirms that the new course is connected to the previous course or study on that course represents the applicants genuine career applications
the applicant has left an integrated master’s or PhD programme having successfully completed the course leading to the award of the lower level of the 2 qualifications it would be possible to be awarded by completing the course and is applying for a new course at the higher level (for example, a student who exits an integrated masters programme with a bachelors qualification then applies for a masters programme after exiting the course with the lower qualification)

[student-visa-guide, Extend your visa]
You may be able to extend your Student visa to stay longer and continue your course or study a new course. This includes if you currently have a Tier 4 (General) student visa.
To extend your visa you must:
be in the UK on a Student visa or a Tier 4 (General) student visa
have an unconditional offer of a place on a course with a licensed student sponsor - shown by your Confirmation of Acceptance for Studies (CAS)
show that your studies are at a higher academic level than your current course (called the ‘academic progress requirement’) - there are some exceptions
If you’ve been in the UK with a valid visa for less than 12 months, you’ll need to prove you have enough money to support yourself in the UK.
Your partner or children will need to apply separately to extend their visa. They can either apply at the same time as you, or at any time before their current visa expires.
You can also switch to a Graduate visa. This will allow you to stay in the UK after successfully completing your course for:
2 years if you apply on or before 31 December 2026
18 months if you apply on or after 1 January 2027
It will allow you to stay for 3 years if you completed a PhD or other doctoral qualification.

[appendix-student, ST 14.4]
ST 14.4. An applicant does not need to show academic progress where they: (a) are applying to re-sit examinations or repeat modules under ST 14.5.; or (b) have previously re-sat examinations or repeated modules under ST 14.5. and are applying to complete the course for which those examinations were re-sat or modules repeated; or (c) are applying to: (i) continue studying with their current student sponsor; or (ii) move to a new student sponsor to enable them to follow their academic supervisor to another institution, for the purpose of completing the PhD or other doctoral qualification for which study was undertaken during their last period of permission as a Student; or (d) are making an application to move to a new student sponsor to complete a course of study begun at a student sponsor that has subsequently had its licence revoked; or (e) are applying to undertake a role as a Student Union Sabbatical Officer; or (f) after undertaking a period as a Student Union Sabbatical Officer are applying to complete the qualification for which the Confirmation of Acceptance for Studies was assigned before that period; or (g) DELETED (h) are applying to undertake an intercalated bachelor’s or master’s degree course or PhD where they are studying medicine, veterinary medicine and science, or dentistry as their principal course of study, or to complete their principal course, having completed a period of intercalation; or (i) are applying to undertake a study abroad programme or work placement which is both integral to and assessed as part of the course, or to complete their course, having completed a study abroad programme or work placement.
ST 14.5. If the applicant is sponsored by a probationary sponsor, they must not previously have re-sat the same examination or repeated the same module, more than once (they can only do so twice).

</details>

## q07 (single)

**Question:** I'm doing a one-year taught master's. Can my wife and our toddler come with me as dependants?

**Reference answer:** No. For postgraduate courses starting on or after 1 January 2024, you can only bring dependants if the course is a PhD or other doctorate or a research-based higher degree, so a one-year taught master's doesn't qualify. The exception is a government-sponsored student on a full-time course of 6 months or longer.

**Agent's answer:**

> No, your wife and toddler cannot come with you as your dependants if your one-year master's is a standard taught course. 
> 
> Under the Immigration Rules, a student on a postgraduate level course is only allowed to have dependants if:
> * The course start date is on or after 1 January 2024, and the sponsor has confirmed the course is a PhD or other doctoral qualification, or a research-based higher degree [appendix-student, ST 31.1]; or
> * They have received a scholarship or sponsorship from a Government for study in the UK on a full-time course of 6 months or longer [appendix-student, ST 31.1].
> 
> Because a taught master's degree is not a research-based higher degree (and unless you are receiving government sponsorship specifically covering your studies), family members are not permitted to join you as student dependants [appendix-student, ST 31.1], [student-caseworker-guidance, When student dependants are permitted].

<details><summary>Retrieved text</summary>

[appendix-student, ST 31.1]
ST 31.1. Unless they are a child who meets the requirements in ST 31.2., the applicant must be the partner or child of a person who is: (a) a Student who has received a scholarship or sponsorship from a Government for study in the UK and has, or is applying for, permission to study on a full-time course of 6 months or longer; or (b) a full-time Student who has, or is applying for, permission to study a postgraduate level course of 9 months or longer at a higher education provider with a track record of compliance and, if the course start date is on or after 1 January 2024, the provider has confirmed the course is a PhD or other doctoral qualification, or a research-based higher degree; or (c) DELETED (d) a Student who has, or had within the last 3 months before the date of application, permission to study on a full-time course of 6 months or longer, and is now applying for permission to study a full-time course of 6 months or longer where either: (i) the partner or child already has, or had within the last 3 months before the date of application, permission as a dependent partner or dependent child of the Student; or (ii) the child was born since the last grant of permission to the Student, where the Student and partner or child are applying at the same time.

[student-caseworker-guidance, When student dependants are permitted]
The rules for the Student course requirement that set out when a Student is permitted to have dependants can be found at Appendix Student ST 31.1 and 31.2.
The following people are eligible for permission as a dependant of a person who has been granted permission as a Student, or who will be applying at the same time:
spouses
civil partners
unmarried partners
dependent children of either a Student or their partner under the age of 18
The following Students are allowed to have dependants with them in the UK:
Students who have a scholarship or sponsorship from a government to study a full-time course lasting 6 months or longer
Students studying above degree level at a higher education provider with a track record of compliance on a course lasting 9 months or longer and, if the course start date is on or after 1 January 2024, the provider has confirmed the course is a PhD or other doctoral qualification, or a research-based higher degree
Students who have permission, or had permission within the last 3 months to study on a full-time course of 6 months or longer, and who are now applying for permission to study a full-time course of 6 months or longer where either: the partner or child applying has been the Student’s dependant in that period the child applying was born since the last grant of permission to the Student and they are applying at the same time as the Student or the dependant partner
Students whose child was born in a timeframe set out at Appendix Student ST 31.2 are allowed to have that child as a dependant with them in the UK

[student-caseworker-guidance, When student dependants are permitted]
The scholarship or sponsorship is not required to cover the full fees and living costs of the student in order to permit them to sponsor dependants. However, if this is the case, the applicant must provide separate financial evidence to demonstrate that they meet the financial requirement.
If a scholarship does not cover the living costs for any dependants of the student then the applicant must provide separate financial evidence to cover them.
Students applying with a combined CAS for integrated programmes comprising of an integrated pre master and research master programme will meet the requirement to bring dependants.
The sponsor should confirm on the CAS which the Student’s current permission relies on whether the course of study is a PhD or other doctoral qualification, or a research-based higher degree or not. This will be done via the Academic Course Level field as follows:
RQF_7 / SCQF_11 will denote a ‘taught’ course
RQF_7_Research / SCQF_11_Research will denote a Research course
RQF_8 / SCQF_12 will denote a ‘taught’ course
RQF_8_Research / SCQF_12_Research will denote a Research course
You may write out for this information if it is not otherwise provided.
To be considered a ‘research-based higher degree’ the course of study must meet the definition of a ‘research-based higher degree’ in Paragraph 6.2(b) of the Immigration rules:
‘Research-based higher degree’ means a postgraduate programme comprising a research component (including a requirement to produce original work) that is larger than any accompanying taught component when measured by student effort.
The definition is consistent with that set out in the Higher Education Statistics Agency (HESA)’s Qualification Category.

[appendix-student, ST 39.1]
ST 39.1. A dependent partner will be granted permission which ends on the same date as the Student’s permission.
ST 39.2. A dependent child will be granted permission which ends on the same date as whichever of their parents’ permission ends first.
ST 39.3. The grant will be subject to all the following conditions: (a) no access to public funds; and (b) work (including self-employment and voluntary work) is permitted except: (i) where the dependant meets the requirement at ST 31.1.(d) and the Student has been granted less than 9 months’ permission, unless that is to continue a course of study where they had previously been granted at least 9 months’ permission; or (ii) where the dependant meets the requirement at ST 31.1.(d) and the Student is studying a course below degree level; or (iii) no employment as a professional sportsperson (including as a sports coach); and (c) study is permitted, subject to the ATAS condition in Appendix ATAS (if the study will commence when the partner or child is aged over 18). (d) DELETED

[student-caseworker-guidance, Employment for dependants of a Student]
Family members of Student can work (in line with UK employment law) in the UK except when:
they are being granted leave as a dependant after previously being the Student’s dependant when the Student had permission to study a full-time course of 6 months or longer and the Student is now applying for permission to study a new full-time course that is less than 9 months in length (unless the Student is continuing a course of study on which they had previously been granted at least 9 months permission for)
they are being granted leave as a dependant after previously being the Student’s dependant when the Student had permission to study a full-time course of 6 months or longer and the Student is now applying for permission to study a new full-time course below degree level

</details>

## q08 (unanswerable)

**Question:** My master's dissertation runs over the summer. Does that count as a vacation, so I can work full-time?

**Reference answer:** I can't find this in the documents I have. Your university's international student advice team can tell you whether your dissertation period counts as an official vacation.

**Agent's answer:**

> I can't find this in the documents I have. You can check GOV.UK or speak to an international student adviser at your university.

<details><summary>Retrieved text</summary>

[appendix-student, ST 26.1]
ST26.1. The applicant will be granted permission with the following employment conditions:
Type of study | Employment conditions; Student following a full-time course of degree level or above study: • sponsored by a higher education provider with a track record of compliance; or • sponsored by an overseas higher education institution to undertake a short-term study abroad programme in the UK | 20 hours per week during term-time (full- time employment permitted outside of term-time); Student undertaking a full-time course below degree level study sponsored by a higher education provider with a track record of compliance | 10 hours per week during term-time (full- time employment permitted outside of term-time); All other study, including all part-time study | No employment permitted
ST 26.2. Students are permitted to undertake work related to a work placement, assessed as an integral part of the course, that meets the requirements at ST 17.1. to ST 17.3.
ST 26.3. Employment as an elected Student Union Sabbatical Officer or elected National Union of Students (NUS) position is permitted for up to 2 years if the Confirmation of Acceptance for Studies was assigned for this purpose.
ST 26.4. DELETED.
ST 26.5. A Student is not allowed to do any of the following: (a) be self-employed or engage in business activity unless ST 26.8 applies; or (b) work as a professional sportsperson (including as a sports coach); or (c) work as an entertainer; or (d) work in a position which would fill a permanent full-time vacancy unless ST 26.6. applies.

[student-caseworker-guidance, Work conditions]
Type of sponsor | Course type level | Work permitted; If study is at: - a higher education provider (HEP) with a track record of compliance - overseas higher education institution and the student is on a short-term study-abroad programme in the UK | Full-time course at degree level or above | Then the following work is permitted: - part-time during term-time (up to a maximum of 20 hours a week) - full-time during vacations, including the period before the course starts - on a work placement that meets the requirements of ST 17 - as a Student Union Sabbatical Officer for up to 2 years when permission has been granted for this purpose; If study is at a higher education provider (HEP) with a track record of compliance | Full-time course below degree level | Then the following work is permitted: - part-time during term-time (up to a maximum of 10 hours a week) - full-time during vacations, including the period before the course starts - on a work placement that meets the requirements of ST 17 - as a Student Union Sabbatical Officer for up to 2 years when permission has been granted for this purpose; Sponsors which are not: - a higher education provider (HEP) with a track record of compliance - an overseas higher education institution sponsoring a study abroad student | Full-time course at any level | Then the following work is permitted: - on a work placement that meets the requirements of ST 17 - as a Student Union Sabbatical Officer for up to 2 years when permission has been granted for this purpose; If study is at: - a higher education provider (HEP) with a track record of compliance - a sponsor participating in the Erasmus+ programme, | Part-time course at any level | Then no work, unless on a work placement that meets the requirements of ST 17

[student-caseworker-guidance, Work conditions]
This page tells caseworkers what employment a Student or Child Student can undertake in the UK.
Employment conditions are dependent on the type of sponsor the applicant will be studying at and the level of course they are studying, information on the amount of hours a Student can work and the type of employment that is permitted can be found in Appendix Student ST 26.
Periods of permission after a Student has completed their course are considered to be outside of term-time for the purposes of any work conditions.

[appendix-student, ST 26.6]
ST 26.6. A Student who makes a valid application for permission to stay under the Skilled Worker, or Graduate route, may start employment in a full-time permanent vacancy either up to 3 months prior to the course completion date (for the Skilled Worker route) or once they have successfully completed their course of study (for the Graduate route), provided all of the following apply: (a) the Student is studying a full-time course of study at degree level or above with a higher education provider with a track record of compliance; and (b) the application as a Skilled Worker, or Graduate, was made when the applicant had permission as a Student; and (c) a decision has not been made on the Skilled Worker, or Graduate, application, or where a decision has been made, any Administrative Review against a refusal of that application has not been finally determined.
ST 26.7. DELETED
ST 26.8. A Student may be self-employed, if: (a) they have applied for permission on the Innovator Founder route; and (b) that application is supported by an endorsement from an Innovator Founder endorsing body; and (c) the application was made when the applicant had permission as a Student; and (d) a decision has not been made on the application, or where the application has been refused, any Administrative Review against a refusal has not been finally determined.

[student-caseworker-guidance, Work conditions]
Students who are allowed to work must not:
be self-employed or engage in business activity, except where the Student has applied for permission on the Innovator Founder route; and that application is supported by an endorsement from an Innovator Founder endorsing body; and the application was made when the applicant had permission as a Student; and a decision has not been made on the application, or where the application has been refused, any Administrative Review against a refusal has not been finally determined
take employment as an entertainer or as a professional sportsperson, including a sports coach
fill a full-time permanent vacancy other than where they are filling a post as a Student Union Sabbatical Officer

[graduate-visa-guide, What counts as time spent studying in the UK]
Studying your course in the UK means that you were in the UK when your education provider needed you to be there - for example, to go to lectures or meet with a tutor.
Example
If you were taking a 1 year master’s degree, but left the UK during term breaks or on weekends, that would still count as studying in the UK for 1 year.

[appendix-graduate, GR 8.1]
GR 8.1. The applicant will be granted the period of permission as set out in the table below:
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made before 1 January 2027.; All other qualifications | 18 months if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made on or after 1 January 2027.

[appendix-student, ST 25.1]
ST 25.1. The grant of permission will be subject to the following conditions: (a) no access to public funds; and (b) no work, except as specified in ST 26; and (c) no study, except as specified in ST 27. (d) DELETED
ST 25.2. The applicant will be granted permission for the duration of the course as specified on the Confirmation of Acceptance for Studies plus the relevant periods specified in ST 25.3.
ST 25.3. The period of permission granted to an applicant before the start of the course who is applying for entry clearance will be either: (a) the relevant period before the course date which is set out in the table below, if entry clearance is granted 1 month or more before the start date of the course; or (b) 7 days before the intended date of travel, if entry clearance is granted less than 1 month before the start date of the course; or (c) with immediate effect, if entry clearance is granted less than 7 days before the intended date of travel and less than 1 month before the start date of the course.
The applicant will be granted a period of permission dependent on the type and length of course as in the table below:
Type of Course | Period granted before course start date | Period granted after course end date; A course of 12 months or longer | 1 Month | 4 Months; A course of 6 months or longer but shorter than 12 months | 1 Month | 2 Months; A pre-sessional course of less than 6 months | 1 Month | 1 Month; A course of less than 6 months in length which is not a pre- sessional course | 7 Days | 7 Days

[student-caseworker-guidance, Grant or refuse extension]
This page tells caseworkers how to grant or refuse an application for an extension of permission.
If the applicant meets the requirements of Appendix Student of the Immigration Rules, the caseworker must grant permission to stay with the appropriate work and study conditions.
Students are able to travel outside of, and re-enter, the UK whilst they hold valid permission as a Student, including in the period after they have completed their course and still hold permission under the route.
For more information on the hours that a Student can work, see: Student: employment.

[graduate-visa-guide, Overview]
A Graduate visa gives you permission to stay in the UK for at least 18 months after successfully completing an eligible course in the UK.
You must be in the UK when you apply.
You can apply for a Graduate visa if all of the following are true:
you’re in the UK
your current visa is a Student visa or Tier 4 (General) student visa
you studied a UK bachelor’s degree, postgraduate degree or other eligible course for a minimum period of time with your Student visa or Tier 4 (General) student visa
your education provider (such as your university or college) has told the Home Office you’ve successfully completed your course
You can ask your education provider if you’re not sure whether they’ve told the Home Office you’ve successfully completed your course.
Check if your course is eligible and how long you need to have studied in the UK.
If you’re not eligible for a Graduate visa, you may be eligible for another type of visa to stay in the UK.

[student-caseworker-guidance, Work placements]
This page tells caseworkers about the requirements for work placements for Student and Child Student applicants.
The requirements that a work placement must meet are stated in Appendix Student ST 17.
The licensed Student sponsor will remain responsible for the student during the work placement.
Students are exempt from meeting the academic progression requirements where they are adding a work placement to their original course of study or applying for further permission to complete their course following a work placement. These students are able to apply for permission to stay to complete their placement from within the UK.
For a work placement to be included within a course of study, the work placement must be integrated and assessed as part of the course of study. There is no requirement stating that a work placement must be credit bearing or assessed as pass or fail.

</details>

## q09 (single)

**Question:** Is an unpaid internship OK, or does it count as work?

**Reference answer:** An unpaid internship is allowed, but if it has set duties and obligations it counts as voluntary work, which counts toward your term-time hours limit together with any paid work. Only volunteering (no contract or obligations, not replacing an employee, usually for a charity) doesn't count as work. The guidance doesn't mention internships by name, so this applies the voluntary work rules.

**Agent's answer:**

> An unpaid internship counts as work or voluntary work under the Immigration Rules, rather than genuine volunteering [student-caseworker-guidance, Volunteering]. 
> 
> Whether an unpaid internship is permitted depends on how it is structured and your visa conditions:
> 
> * **Voluntary Work vs. Volunteering:** The Home Office distinguishes between true "volunteering" (which has no contract, is usually for a charity or public sector organization, and does not involve doing unpaid work as a substitute for an employee) and "voluntary work" (which involves contractual obligations, such as set hours and specific tasks, even if unpaid or remunerated in kind) [student-caseworker-guidance, Volunteering]. An unpaid internship typically falls under voluntary work because it involves specific duties and obligations with an employer [student-caseworker-guidance, Volunteering].
> * **Hours Limits:** If you are permitted to work on your Student visa, any hours spent on voluntary work count towards your weekly work limit during term-time (for example, the 20-hours-per-week limit for most full-time degree-level students) [student-caseworker-guidance, Volunteering], [appendix-student, ST 26.1]. Your combined paid work and voluntary work must not exceed your permitted weekly limit during term-time [student-caseworker-guidance, Volunteering].
> * **Prohibited Work:** Even if unpaid, you must not take on an internship that involves filling a permanent full-time vacancy (unless it is an official course-related work placement) [appendix-student, ST 26.1], work as an entertainer or professional sportsperson, or self-employment/business activity [appendix-student, ST 26.5].
> * **Course-Related Work Placements:** If the internship is an integral and assessed part of your course of study, it may be permitted as a work placement under your sponsorship rules [student-caseworker-guidance, Work placements], [appendix-student, ST 26.2].

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Volunteering]
Students and Child Students can volunteer while they are studying. Voluntary work is distinct from volunteering.
A Student can do voluntary work if they are permitted to work, but this work and any paid work must not exceed the total number of hours they are permitted to work during term time. For example, if a student is permitted to work 20 hours a week during term-time and has paid work of 15 hours a week, they cannot do more than 5 hours voluntary work. If they are not permitted to work, they cannot do voluntary work.
Child Students aged 16 and over can undertake voluntary work.
Factors to take into account when considering whether a particular activity constitutes voluntary work or volunteering are:
voluntary workers will usually have contractual obligations to perform the work (for example to attend at particular times and carry out specific tasks) with the employer being contractually required to provide the work – the contract does not have to be written - the worker is usually remunerated in kind
volunteers do not have a contract - they must not be a substitute for an employee, and they must not be doing unpaid work – for example, receiving payment in kind (although they are sometimes reimbursed for reasonable travel and subsistence expenses)
volunteers usually help a charity or voluntary or public sector organisation

[student-caseworker-guidance, Work placements]
This page tells caseworkers about the requirements for work placements for Student and Child Student applicants.
The requirements that a work placement must meet are stated in Appendix Student ST 17.
The licensed Student sponsor will remain responsible for the student during the work placement.
Students are exempt from meeting the academic progression requirements where they are adding a work placement to their original course of study or applying for further permission to complete their course following a work placement. These students are able to apply for permission to stay to complete their placement from within the UK.
For a work placement to be included within a course of study, the work placement must be integrated and assessed as part of the course of study. There is no requirement stating that a work placement must be credit bearing or assessed as pass or fail.

[appendix-student, ST 26.1]
ST26.1. The applicant will be granted permission with the following employment conditions:
Type of study | Employment conditions; Student following a full-time course of degree level or above study: • sponsored by a higher education provider with a track record of compliance; or • sponsored by an overseas higher education institution to undertake a short-term study abroad programme in the UK | 20 hours per week during term-time (full- time employment permitted outside of term-time); Student undertaking a full-time course below degree level study sponsored by a higher education provider with a track record of compliance | 10 hours per week during term-time (full- time employment permitted outside of term-time); All other study, including all part-time study | No employment permitted
ST 26.2. Students are permitted to undertake work related to a work placement, assessed as an integral part of the course, that meets the requirements at ST 17.1. to ST 17.3.
ST 26.3. Employment as an elected Student Union Sabbatical Officer or elected National Union of Students (NUS) position is permitted for up to 2 years if the Confirmation of Acceptance for Studies was assigned for this purpose.
ST 26.4. DELETED.
ST 26.5. A Student is not allowed to do any of the following: (a) be self-employed or engage in business activity unless ST 26.8 applies; or (b) work as a professional sportsperson (including as a sports coach); or (c) work as an entertainer; or (d) work in a position which would fill a permanent full-time vacancy unless ST 26.6. applies.

[student-caseworker-guidance, Work conditions]
Students who are allowed to work must not:
be self-employed or engage in business activity, except where the Student has applied for permission on the Innovator Founder route; and that application is supported by an endorsement from an Innovator Founder endorsing body; and the application was made when the applicant had permission as a Student; and a decision has not been made on the application, or where the application has been refused, any Administrative Review against a refusal has not been finally determined
take employment as an entertainer or as a professional sportsperson, including a sports coach
fill a full-time permanent vacancy other than where they are filling a post as a Student Union Sabbatical Officer

[student-caseworker-guidance, Sports-related work placements]
In certain circumstances, Students and Child Students are permitted to undertake a sports-related work placement as part of their course. These are permitted where the placement is an integral and assessed part of their course and does not involve the student filling a permanent vacancy. Additionally, Students and Child Students must not take up a role that requires them to play or coach sport as part of a work placement, unless they are doing so as an amateur.

</details>

## q10 (single)

**Question:** Once my course has officially ended but before my visa runs out, can I work full-time?

**Reference answer:** Yes. The guidance says the time left on your visa after you've completed your course counts as outside term time for work purposes, and full-time work is allowed outside term time. The one limit is that you can't take a permanent full-time job unless you've applied for a Graduate or Skilled Worker visa.

**Agent's answer:**

> Yes, once your course has officially ended, periods of permission after you have completed your course are treated as being outside of term-time for the purposes of your work conditions [student-caseworker-guidance, Work conditions]. 
> 
> Whether you can work full-time during this period depends on the type of work and your circumstances:
> 
> * **General work:** If you are permitted to work during your studies (such as up to 20 hours a week during term-time for full-time degree-level courses at a higher education provider with a track record of compliance), you are permitted to work full-time outside of term-time, which includes the period after your course has officially ended while your Student visa remains valid [appendix-student, ST 26.1], [student-caseworker-guidance, Work conditions].
> * **Permanent full-time vacancies / Graduate or Skilled Worker routes:** Generally, Student visa holders are not allowed to fill a permanent full-time vacancy [appendix-student, ST 26.5]. However, if you make a valid application to switch to the Graduate route (after successfully completing your course) or the Skilled Worker route while you still have permission as a Student, you can start employment in a full-time permanent vacancy once you have successfully completed your course (for the Graduate route) or up to 3 months prior to your course completion date (for the Skilled Worker route), provided your application remains undecided and you meet the specific sponsorship and study level requirements [appendix-student, ST 26.6]. 
> 
> You must still adhere to general Student work restrictions (such as not being self-employed or working as a professional sportsperson or entertainer) unless a specific exception applies [appendix-student, ST 26.5].

<details><summary>Retrieved text</summary>

[appendix-student, ST 26.6]
ST 26.6. A Student who makes a valid application for permission to stay under the Skilled Worker, or Graduate route, may start employment in a full-time permanent vacancy either up to 3 months prior to the course completion date (for the Skilled Worker route) or once they have successfully completed their course of study (for the Graduate route), provided all of the following apply: (a) the Student is studying a full-time course of study at degree level or above with a higher education provider with a track record of compliance; and (b) the application as a Skilled Worker, or Graduate, was made when the applicant had permission as a Student; and (c) a decision has not been made on the Skilled Worker, or Graduate, application, or where a decision has been made, any Administrative Review against a refusal of that application has not been finally determined.
ST 26.7. DELETED
ST 26.8. A Student may be self-employed, if: (a) they have applied for permission on the Innovator Founder route; and (b) that application is supported by an endorsement from an Innovator Founder endorsing body; and (c) the application was made when the applicant had permission as a Student; and (d) a decision has not been made on the application, or where the application has been refused, any Administrative Review against a refusal has not been finally determined.

[appendix-student, ST 26.1]
ST26.1. The applicant will be granted permission with the following employment conditions:
Type of study | Employment conditions; Student following a full-time course of degree level or above study: • sponsored by a higher education provider with a track record of compliance; or • sponsored by an overseas higher education institution to undertake a short-term study abroad programme in the UK | 20 hours per week during term-time (full- time employment permitted outside of term-time); Student undertaking a full-time course below degree level study sponsored by a higher education provider with a track record of compliance | 10 hours per week during term-time (full- time employment permitted outside of term-time); All other study, including all part-time study | No employment permitted
ST 26.2. Students are permitted to undertake work related to a work placement, assessed as an integral part of the course, that meets the requirements at ST 17.1. to ST 17.3.
ST 26.3. Employment as an elected Student Union Sabbatical Officer or elected National Union of Students (NUS) position is permitted for up to 2 years if the Confirmation of Acceptance for Studies was assigned for this purpose.
ST 26.4. DELETED.
ST 26.5. A Student is not allowed to do any of the following: (a) be self-employed or engage in business activity unless ST 26.8 applies; or (b) work as a professional sportsperson (including as a sports coach); or (c) work as an entertainer; or (d) work in a position which would fill a permanent full-time vacancy unless ST 26.6. applies.

[student-caseworker-guidance, Grant or refuse extension]
This page tells caseworkers how to grant or refuse an application for an extension of permission.
If the applicant meets the requirements of Appendix Student of the Immigration Rules, the caseworker must grant permission to stay with the appropriate work and study conditions.
Students are able to travel outside of, and re-enter, the UK whilst they hold valid permission as a Student, including in the period after they have completed their course and still hold permission under the route.
For more information on the hours that a Student can work, see: Student: employment.

[student-caseworker-guidance, Work conditions]
This page tells caseworkers what employment a Student or Child Student can undertake in the UK.
Employment conditions are dependent on the type of sponsor the applicant will be studying at and the level of course they are studying, information on the amount of hours a Student can work and the type of employment that is permitted can be found in Appendix Student ST 26.
Periods of permission after a Student has completed their course are considered to be outside of term-time for the purposes of any work conditions.

[student-caseworker-guidance, Work conditions]
Type of sponsor | Course type level | Work permitted; If study is at: - a higher education provider (HEP) with a track record of compliance - overseas higher education institution and the student is on a short-term study-abroad programme in the UK | Full-time course at degree level or above | Then the following work is permitted: - part-time during term-time (up to a maximum of 20 hours a week) - full-time during vacations, including the period before the course starts - on a work placement that meets the requirements of ST 17 - as a Student Union Sabbatical Officer for up to 2 years when permission has been granted for this purpose; If study is at a higher education provider (HEP) with a track record of compliance | Full-time course below degree level | Then the following work is permitted: - part-time during term-time (up to a maximum of 10 hours a week) - full-time during vacations, including the period before the course starts - on a work placement that meets the requirements of ST 17 - as a Student Union Sabbatical Officer for up to 2 years when permission has been granted for this purpose; Sponsors which are not: - a higher education provider (HEP) with a track record of compliance - an overseas higher education institution sponsoring a study abroad student | Full-time course at any level | Then the following work is permitted: - on a work placement that meets the requirements of ST 17 - as a Student Union Sabbatical Officer for up to 2 years when permission has been granted for this purpose; If study is at: - a higher education provider (HEP) with a track record of compliance - a sponsor participating in the Erasmus+ programme, | Part-time course at any level | Then no work, unless on a work placement that meets the requirements of ST 17

[student-visa-guide, Staying longer in the UK]
You may be able to:
extend your visa if you’re eligible, for example to continue your studies in the UK
switch to a Student visa from another visa if you’re already in the UK
switch to a Graduate visa
A Graduate visa will allow you to stay in the UK after successfully completing your course for:
2 years if you apply on or before 31 December 2026
18 months if you apply on or after 1 January 2027
It will allow you to stay for 3 years if you completed a PhD or other doctoral qualification.

[graduate-visa-guide, Overview]
A Graduate visa gives you permission to stay in the UK for at least 18 months after successfully completing an eligible course in the UK.
You must be in the UK when you apply.
You can apply for a Graduate visa if all of the following are true:
you’re in the UK
your current visa is a Student visa or Tier 4 (General) student visa
you studied a UK bachelor’s degree, postgraduate degree or other eligible course for a minimum period of time with your Student visa or Tier 4 (General) student visa
your education provider (such as your university or college) has told the Home Office you’ve successfully completed your course
You can ask your education provider if you’re not sure whether they’ve told the Home Office you’ve successfully completed your course.
Check if your course is eligible and how long you need to have studied in the UK.
If you’re not eligible for a Graduate visa, you may be eligible for another type of visa to stay in the UK.

</details>

## q11 (multi)

**Question:** I finished my master's in September but my results only come out in mid-December. If I apply before 1 January 2027, do I still get two years?

**Reference answer:** Yes. A Graduate visa applied for before 1 January 2027 lasts two years (18 months on or after that date), but you can only apply once your university has told the Home Office you've successfully completed your course, so your results need to be reported before then. You don't need to wait for your graduation ceremony, but your Student visa must still be valid on the day you apply.

**Agent's answer:**

> Yes, if you apply before 1 January 2027, you will be granted a 2-year Graduate visa, provided you meet all the requirements [graduate-visa-guide, How long you can stay], [appendix-graduate, GR 8.1]. 
> 
> The length of the visa depends on the date your application is made [graduate-caseworker-guidance, Graduate: period to grant]:
> * **2 years** if your application is made before 1 January 2027 [graduate-visa-guide, How long you can stay], [appendix-graduate, GR 8.1].
> * **18 months** if your application is made on or after 1 January 2027 [graduate-visa-guide, How long you can stay], [appendix-graduate, GR 8.1].
> 
> However, before you can apply, your university or college must have notified the Home Office that you have successfully completed your course [graduate-visa-guide, Overview], [appendix-graduate, GR 4.3]. You should check with your institution to ensure they have submitted this notification, as the Student sponsor must have notified the Home Office by the date of your application [appendix-graduate, GR 4.3].

<details><summary>Retrieved text</summary>

[graduate-visa-guide, How long you can stay]
A Graduate visa lasts for:
2 years if you apply on or before 31 December 2026
18 months if you apply on or after 1 January 2027
If you have a PhD or other doctoral qualification, it will last for 3 years.
Your visa will start from the day your application is approved.

[appendix-graduate, GR 8.1]
GR 8.1. The applicant will be granted the period of permission as set out in the table below:
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made before 1 January 2027.; All other qualifications | 18 months if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made on or after 1 January 2027.

[graduate-caseworker-guidance, Graduate: period to grant]
The period of permission to be granted to an applicant is dependent on the type of course studied and the date the application is made and is set out at Appendix Graduate GR.8.1 and in the following table
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made before 1 January 2027.; All other qualifications | 18 months - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made on or after 1 January 2027.
An applicant whose CAS was assigned for an integrated PhD but who successfully completes the lower postgraduate qualification must be granted 18 months from the date of decision where the Graduate application is made on or after 1 January 2027.

[graduate-visa-guide, Overview]
A Graduate visa gives you permission to stay in the UK for at least 18 months after successfully completing an eligible course in the UK.
You must be in the UK when you apply.
You can apply for a Graduate visa if all of the following are true:
you’re in the UK
your current visa is a Student visa or Tier 4 (General) student visa
you studied a UK bachelor’s degree, postgraduate degree or other eligible course for a minimum period of time with your Student visa or Tier 4 (General) student visa
your education provider (such as your university or college) has told the Home Office you’ve successfully completed your course
You can ask your education provider if you’re not sure whether they’ve told the Home Office you’ve successfully completed your course.
Check if your course is eligible and how long you need to have studied in the UK.
If you’re not eligible for a Graduate visa, you may be eligible for another type of visa to stay in the UK.

[graduate-visa-guide, How long you studied in the UK for]
You need to have studied in the UK for either:
at least 12 months, if your course’s total length is more than 12 months
the total length of your course, if its total length is shorter than 12 months
You must also be in the UK when you apply for a Graduate visa.

[graduate-caseworker-guidance, Sponsor notification]
The Student Sponsor must have notified the Home Office, by the date of application, that the applicant has successfully completed the course of study. Sponsors will normally do this by way of bulk upload. If sponsors are unable to make the notification via bulk upload, they must use the agreed exceptions process.
If a notification has not been received from the Student Sponsor, but the CAS shows that the applicant had been studying a qualifying qualification, the caseworker must not refuse the application if it would otherwise be granted. Instead, the caseworker must contact the Sponsor asking for confirmation that the student has successfully completed the course of study.

[appendix-graduate, GR 4.1]
GR 4.1. The applicant must have last been sponsored by a Student sponsor which is a higher education provider with a track record of compliance on the date of application.
GR 4.2. The applicant must have successfully completed the course of study which was undertaken during their last grant of permission to study on the Student route (where the applicant was allowed to change their course of study without applying for further permission as a Student, this requirement only applies to the course to which they changed).
GR 4.3. The student sponsor must have notified the Home Office, by the date of application, that the applicant has successfully completed the course of study in GR 4.2.

[graduate-visa-guide, If your application is successful]
You’ll get an eVisa (a digital record of your identity and immigration status).
Your decision email or letter will tell you how to get access to your eVisa. You’ll need to create a UKVI account.
If your partner and children joined you in the UK as ‘dependants’ on your current Student visa or Tier 4 (General) student visa, they can apply to stay as dependants on your Graduate visa.
Your child can also apply if they were born in the UK during your current Student visa, Tier 4 (General) student visa or Graduate visa.
If their application is successful, their visa will end on the same date as yours.
A dependant is any of the following:
your husband, wife, civil partner or unmarried partner
your child under 18 - including if they were born in the UK during your stay
your child over 18 if they currently have permission (‘leave to enter’ or ‘leave to remain’) to be in the UK as your dependant

[graduate-visa-guide, How long it takes to get a decision]
Once you’ve applied online, proved your identity and provided your documents, you’ll usually get a decision within 8 weeks.
You’ll be contacted if your application will take longer, for example because:
your supporting documents need to be verified
of your personal circumstances, for example if you have a criminal conviction
You can ask to cancel your application. You’ll only get your fee refunded if UKVI has not started processing your application.

</details>

## q12 (unanswerable)

**Question:** My employer isn't a licensed sponsor. Can they get a licence before my Graduate visa runs out, and how long does that take?

**Reference answer:** I can't find this in the documents I have. Your employer can check the Home Office's guidance on sponsor licences on GOV.UK.

**Agent's answer:**

> I can't find this in the documents I have. You can check GOV.UK or speak with your university's international student advisers for guidance on employer sponsor licence applications and timelines.

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Licensed student sponsors]
This page tells caseworkers about licensed student sponsors for applicants on the Student and Child Student routes.
All educational establishments that wish to sponsor international students must have a student sponsor licence.
To check that a sponsor still has a student sponsor licence, see the Student sponsor register.
The type of institution, and the status of the institution’s licence, can affect an application under the Student route or Child Student route and the permission that is granted.

[student-visa-guide, How long it takes to get a decision]
You’ll usually get a decision on your visa within:
3 weeks, if you’re outside the UK
8 weeks, if you’re inside the UK
You may be able to pay to get a faster decision - you’ll be told if you can when you apply.

[student-visa-guide, How long it takes to get a decision]
You’ll usually get a decision within 8 weeks.
You may be able to pay to get a faster decision.
You’ll be contacted if your application is complex and will take longer, for example because:
your supporting documents need to be verified
you need to attend an interview
of your personal circumstances (for example if you have a criminal conviction)
If you need to change something in your application after you’ve sent it contact UK Visas and Immigration (UKVI).
You can ask to withdraw your application by contacting UKVI. Your fee will only be refunded if UKVI has not started processing your application.

[student-caseworker-guidance, Sponsor has had their licence revoked, or the licence has been surrendered or expired]
variation application and provides a new CAS within the specified 60 calendar day period If the applicant has extant permission, and there are other grounds for refusing the application – including if the caseworker believes that a student is not a genuine student (and therefore does not meet the requirement of the genuine student rule), or that the student participated in the practices that may have contributed to the sponsor’s licence being revoked (and therefore must be considered for refusal on the grounds set out in Part Suitability, for example using deception or breaching the conditions of their permission, depending on the circumstances of their case) – then they must refuse the application on the basis of the requirements in the Immigration Rules that the applicant fails to meet. The caseworker must also refer the case to the curtailment team so that curtailment can be considered; do this by NotificationsandCurtailmentsTeam@homeoffice.gov.uk with the details of the case.

[student-visa-guide, How long it takes to get a decision]
A decision will usually be made within 8 weeks.
You may be able to pay to get a faster decision.
You’ll be contacted if your application is complex and will take longer, for example because:
your supporting documents need to be verified
you need to attend an interview
of your personal circumstances (for example if you have a criminal conviction)
If you need to change something in your application after you’ve sent it contact UK Visas and Immigration (UKVI).
You can ask to withdraw your application by contacting UKVI. Your fee will only be refunded if UKVI has not started processing your application.
You’ll get an eVisa (a digital record of your identity and immigration status).
Your decision email or letter will tell you how to get access to your eVisa. You’ll need to create a UKVI account.

[graduate-visa-guide, How long it takes to get a decision]
Once you’ve applied online, proved your identity and provided your documents, you’ll usually get a decision within 8 weeks.
You’ll be contacted if your application will take longer, for example because:
your supporting documents need to be verified
of your personal circumstances, for example if you have a criminal conviction
You can ask to cancel your application. You’ll only get your fee refunded if UKVI has not started processing your application.

[graduate-visa-guide, How long it takes to get a decision]
Once they’ve applied online, proved their identity and provided their documents, they’ll usually get a decision within 8 weeks.
They’ll get an eVisa (a digital record of their identity and immigration status).
Their decision email or letter will tell them how to get access to their eVisa. They’ll need to create a UKVI account.

[graduate-visa-guide, Getting a decision]
Once you’ve applied online, proved your identity and provided your documents, you’ll usually get a decision on your visa within 8 weeks.
You can stay in the UK while you wait for a decision.
When you apply for a Graduate visa, you’ll need to:
pay the £937 application fee
pay the healthcare surcharge - this is usually £1,035 for each year you’ll be in the UK
Check how much it will cost.

[graduate-caseworker-guidance, Graduate: period to grant]
The period of permission to be granted to an applicant is dependent on the type of course studied and the date the application is made and is set out at Appendix Graduate GR.8.1 and in the following table
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made before 1 January 2027.; All other qualifications | 18 months - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made on or after 1 January 2027.
An applicant whose CAS was assigned for an integrated PhD but who successfully completes the lower postgraduate qualification must be granted 18 months from the date of decision where the Graduate application is made on or after 1 January 2027.

[graduate-visa-guide, How long you can stay]
A Graduate visa lasts for:
2 years if you apply on or before 31 December 2026
18 months if you apply on or after 1 January 2027
If you have a PhD or other doctoral qualification, it will last for 3 years.
Your visa will start from the day your application is approved.

</details>

## q13 (unanswerable)

**Question:** Who pays the Skilled Worker visa fees and the Immigration Skills Charge? Can my employer make me pay them back if I leave early?

**Reference answer:** I can't find this in the documents I have. The Skilled Worker visa guidance on GOV.UK, or your employer's HR team, can tell you who pays which fees.

**Agent's answer:**

> I can't find this in the documents I have. 
> 
> Please check GOV.UK for official guidance on Skilled Worker visa sponsorship duties and employment law, or speak to your university's international student advisers or an employment advice service like Citizens Advice regarding employer repayment clauses.

<details><summary>Retrieved text</summary>

[graduate-visa-guide, If you work in public sector healthcare]
If you’re a doctor or nurse, or you work in health or adult social care, check if you’re eligible to apply for the Health and Care Worker visa instead. It’s cheaper to apply for and you do not need to pay the annual immigration health surcharge.
If you get a job in public sector healthcare after you have paid the healthcare surcharge, you may be able to get a refund.

[appendix-english-language, EL 9.1]
EL 9.1. An applicant applying for entry clearance or permission to stay under Appendix Skilled Worker will meet the English language requirement if they are being sponsored to work as a doctor, dentist, nurse, midwife or veterinarian, and have passed an English Language assessment which is accepted by the relevant regulated professional body as a requirement for registration.

[graduate-visa-guide, Healthcare surcharge]
If you’re eligible for a Graduate visa for:
18 months - it will cost £1,552.50
2 years - it will cost £2,070
3 years - it will cost £3,105
If you get a job in public sector healthcare after you have paid the healthcare surcharge, you may be able to get a refund.

[student-caseworker-guidance, Course fees]
Applicants applying for a new course from overseas and those who have been in the UK for less than a year must demonstrate that they have enough money to pay the course fees for either:
one academic year of the course
the entire course (if it is less than a year long)
Students who are differentiated nationals will generally not be required to demonstrate evidence of course fees. Those students who have held valid permission for 12 months or more at the date of application are not required to demonstrate funds to pay course fees during their application, however all international students are required to pay any course fees to the sponsoring institution.
The amount an applicant will pay for course fees is stated on the Confirmation of Acceptance for Studies (CAS). The CAS will also confirm if there is no fee to pay. The caseworker must also:
check for any payment receipts that post-date the CAS and which may have been provided
query any ambiguities with the applicant or sponsor
If the applicant has paid all or part of their course fees this must be confirmed on the CAS, or the applicant must provide a receipt issued by the sponsor confirming the amount of fees paid.

[appendix-student, ST 26.6]
ST 26.6. A Student who makes a valid application for permission to stay under the Skilled Worker, or Graduate route, may start employment in a full-time permanent vacancy either up to 3 months prior to the course completion date (for the Skilled Worker route) or once they have successfully completed their course of study (for the Graduate route), provided all of the following apply: (a) the Student is studying a full-time course of study at degree level or above with a higher education provider with a track record of compliance; and (b) the application as a Skilled Worker, or Graduate, was made when the applicant had permission as a Student; and (c) a decision has not been made on the Skilled Worker, or Graduate, application, or where a decision has been made, any Administrative Review against a refusal of that application has not been finally determined.
ST 26.7. DELETED
ST 26.8. A Student may be self-employed, if: (a) they have applied for permission on the Innovator Founder route; and (b) that application is supported by an endorsement from an Innovator Founder endorsing body; and (c) the application was made when the applicant had permission as a Student; and (d) a decision has not been made on the application, or where the application has been refused, any Administrative Review against a refusal has not been finally determined.

</details>

## q14 (single)

**Question:** Do I need another English test for the Skilled Worker visa if I already have a UK master's?

**Reference answer:** No. A master's degree awarded in the UK meets the English language requirement, and you can prove it with your degree certificate, academic transcript or a letter from your university. You may also meet it if you already showed English at the required level in a previous successful application.

**Agent's answer:**

> No, you do not need to take another English test if you already have a UK master’s degree. 
> 
> Under the immigration rules, an applicant meets the English language requirement if they have an academic qualification, such as a master’s degree, that was awarded in the UK [appendix-english-language, EL 5.1]. This requirement can be proven using a certificate from the awarding body, a transcript issued by the university or college, or an official letter from the university or college containing information equivalent to a degree certificate [appendix-english-language, EL 5.3]. 
> 
> Additionally, you will automatically meet the English language requirement for a Skilled Worker application if you have already shown that you met the requirement at the required level in a previous successful application for entry clearance or permission to stay (such as your previous Student visa) [appendix-english-language, EL 3.1].

<details><summary>Retrieved text</summary>

[appendix-english-language, EL 5.1]
EL 5.1. An applicant will meet the English language requirement if they have an academic qualification which meets one of the requirements at EL 5.2. and is proven by the required evidence under EL 5.3. or EL 5.4.
EL 5.2. The requirements are that the applicant has: (a) a bachelor’s degree, master’s degree or doctorate awarded in the UK; or (b) a degree or degree-level qualification taught in a university or college in a majority- English-speaking country listed in EL 4.1. (except Canada), or Ireland, which meets or exceeds the recognised standard of a bachelor’s degree, master’s degree or doctorate awarded in the UK; or (c) a degree or degree level qualification which meets, or exceeds, the recognised standard of a UK bachelor’s degree; master’s degree or doctorate and was taught or researched in English.
EL 5.3. The requirement at EL 5.2. must be proven by one of: (a) a certificate from the awarding body: or (b) a transcript issued by the university or college that awarded the qualification; or (c) an official letter from the university or college that awarded the qualification containing information equivalent to a degree certificate.
EL 5.4. If the qualification was awarded by a body from outside the UK, the requirement at EL 5.2. must, in addition to the requirement at EL 5.3, be proven by confirmation from the qualification and language assessments provider that the qualification meets the requirements at EL 5.2(b) or EL 5.2(c).

[student-visa-guide, If you have a degree from a UK institution]
You can prove your knowledge of English if you have a degree-level qualification that was both:
taught in English
awarded by a UK institution, even if you studied outside the UK
If your degree was taught in English and was not awarded by a UK institution, you’ll need to apply for an assessment from Ecctis.
Ecctis will give you a code to confirm that your qualification is equivalent to a UK bachelor’s degree or higher and was taught in English.

[appendix-english-language, EL 9.1]
EL 9.1. An applicant applying for entry clearance or permission to stay under Appendix Skilled Worker will meet the English language requirement if they are being sponsored to work as a doctor, dentist, nurse, midwife or veterinarian, and have passed an English Language assessment which is accepted by the relevant regulated professional body as a requirement for registration.

[appendix-english-language, EL 2.1]
EL 2.1. An applicant will meet the English language requirement if any of the requirements in EL 3.1. to EL 7.2 are met.
EL 2.2. The English language requirement is also met by a person applying for entry clearance or permission to stay as a Student if any of the requirements in EL 7.1. to EL 8.4. are met.
EL 2.3. The English language requirement is also met by a person applying for entry clearance or permission to stay as a Skilled Worker route if:
(a) the requirements in EL 7.1. and EL 7.2. are met: or
(b) the requirement in EL 9.1. is met.
EL 2.4. The English language requirement is also met by a person applying for:
(a) entry clearance or permission to stay on the Start-up route, or
(b) entry clearance or permission to stay on the Innovator Founder route; or
(c) entry clearance, permission to stay or settlement on the Scale-up route, or
(d) entry clearance or permission to stay on the High Potential Individual route, or
(e) settlement under Appendix Settlement Family Life, or
(f) settlement under Appendix Private Life, or
(g) entry clearance, permission to stay or settlement on the International Sportsperson route; or
(h) entry clearance, permission to stay or settlement on the Representative of an Overseas Business route; or
(i) entry clearance or permission to stay on the T2 Minister of Religion route; or
(j) settlement on the UK Ancestry route; or
(k) settlement on the Global Talent route; or
(l) settlement on the Domestic Workers in a Private Household route or
(m) settlement on Hong Kong British National (Overseas) route; or
(n) settlement on the Appendix Child Relative (Sponsors with Protection) route; or
(o) settlement on the Appendix Bereaved Partner route; or

[student-caseworker-guidance, Student: English language requirement]
This page tells caseworkers about the English language requirement for applicants on the Student route.
Applicants on the Student route must meet a required level of English language ability depending on the level of their course.
The caseworker must check the applicant’s Confirmation of Acceptance for Studies to determine what level of English is required and what assessment was carried out or what evidence has been used to demonstrate that the applicant meets the requirement.
If applying to study a course below degree level, the applicant must have the equivalent of level B1 of the Common European Framework of References for English language.
If applying to study a course at degree level or above, the applicant must have the equivalent of level B2 of the Common European Framework of References for English language.
Applicants on a combined pre-sessional course need to demonstrate level B1 English if they have not been given an unconditional offer of study on the main course of study at degree level or above, and their sponsor has not assessed them as already having level B2 English.
There is further guidance on how caseworkers must assess evidence that an applicant meets the English language requirement at the relevant level.

[appendix-english-language, EL 7.1]
EL 7.1. An applicant will meet the English language requirement if they have a GCSE, an International GCSE, an A level, a Scottish National Qualification at level 4 or 5 or a Scottish Higher or Advanced Higher in English (language or literature) that was awarded: (a) by an Ofqual (or SQA, Qualifications Wales or CCEA) regulated awarding body; and (b) following education undertaken in a UK based school which began while they were aged under 18.
EL 7.2. The requirement at EL 7.1. must be proven by either:
(a) a certificate from the awarding body: or
(b) an official transcript issued by the awarding body

[appendix-english-language, EL 6.1]
EL 6.1. An applicant will meet the English language requirement if they have provided a valid digital reference number from an approved provider showing they have passed an approved English language test to the required level in each required component as set out in the relevant route, in the 2 years before the date of application.
The list of approved tests and providers, updated from time to time, can be found at https://www.gov.uk/guidance/prove-your-english-language-abilities-with-a-secure-english-language-test-selt#approved-test-providers-and-approved-tests.

[appendix-english-language, How the requirement is met]
(p) entry clearance or settlement under Appendix Victim of Domestic Abuse; or
(q) entry clearance, permission to stay or settlement under Appendix HM Armed Forces; or
(r) settlement under Appendix Long Residence; or
(s) entry clearance under Appendix Temporary Work – International Agreement.
if the requirements in EL 7.1 and EL 7.2. are met.
EL 2.5. DELETED.

[appendix-english-language, EL 8.1]
EL 8.1. An applicant under Appendix Student will meet the English language requirement if they are applying for a course of study at degree level or above and are sponsored by a higher education provider with a track record of compliance who states on the Confirmation of Acceptance for Studies that they have assessed the applicant’s English language ability and how they have assessed it.
EL 8.2. Where an assessment under EL 8.1. has been carried out the Confirmation of Acceptance for Studies entry must confirm that the applicant has a knowledge of English equivalent to level B2, or above, of the Council of Europe’s Common European Framework for Language Learning in all 4 components (reading, writing, speaking and listening) or that the requirement at ST 15.3. is met.
EL 8.3. An applicant under Appendix Student will meet the English language requirement if they have taken an approved English test and been exempted from a component of that test by the test provider due to a disability, and the student sponsor has confirmed that they are satisfied the English language ability of the applicant is sufficient to undertake the course of study.
EL 8.4. An applicant under Appendix Student will meet the English language requirement if they are applying for a short-term study abroad programme of up to six months and both: (a) the study abroad programme is part of a course of study at degree level or above at an overseas higher education institution in the United States of America; and (b) the qualification and language assessments provider confirms that the course of study overseas will lead to an academic (not a professional or vocational) qualification at UK bachelor’s degree level or above.

[appendix-english-language, Introduction]
It applies only to applications under Appendix Student, Appendix Skilled Worker, Appendix Representative of an Overseas Business, Appendix T2 Minister of Religion, Appendix International Sportsperson, Appendix UK Ancestry, Appendix Global Talent, Appendix Start-up, Appendix Innovator Founder, Appendix Domestic Worker in a Private Household, Appendix High Potential Individual, Appendix Settlement Family Life, Appendix Private Life, Appendix Scale Up, Appendix Child Relative (Sponsors with Protection), Appendix Hong Kong British National (Overseas), Appendix Victim of Domestic Abuse, Appendix Temporary Work-International Agreement, Appendix HM Armed Forces, Appendix Long Residence and Appendix Bereaved Partner.
The route sets out whether the English language requirement must be met and at what level.

[appendix-english-language, EL 3.1]
EL 3.1. An applicant will meet the English language requirement if they have already shown they met the requirement, at the level required for their current application, in a previous successful application for entry clearance or permission to stay.
EL 4.1. An applicant will meet the English language requirement if they are a national of any of the following majority-English-speaking countries: Antigua and Barbuda Australia The Bahamas Barbados Belize The British Overseas Territories Canada Dominica Grenada Guyana Jamaica Malta New Zealand St Kitts and Nevis St Lucia St Vincent and the Grenadines Trinidad and Tobago United States of America

</details>

## q15 (unanswerable)

**Question:** I'm finishing a PhD in machine learning. Could I get a Global Talent visa instead of being tied to one employer?

**Reference answer:** I can't find this in the documents I have. To check, see the Global Talent visa guidance on GOV.UK.

**Agent's answer:**

> I can't find this in the documents I have. 
> Please check GOV.UK or speak with your university's international student advisers regarding the Global Talent visa and its endorsement criteria for researchers and academics.

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Student: Doctorate Extension Scheme (DES)]
The Doctorate Extension Scheme (DES) closed on 1 July 2021. The scheme has been replaced by the Graduate route, which opened on the same date.
The DES was open to Students with entry clearance or permission to stay as a Student or Tier 4 (General) student completing a course leading to the award of a PhD at a higher education provider (HEP) with a track record of compliance. Students who met the qualification criteria were granted further permission for 12 months from the course end date specified on the Confirmation of Acceptance for Studies (CAS) submitted with the DES application.
While waiting for a decision on the application for permission on the DES, and following a grant of permission, students were allowed to work full-time without restriction, except as a professional sportsperson (including as a sports coach).
Under the scheme:
students could sponsor dependents
students could switch into work routes
Students only needed to hold or apply for and Academic Technology Approval Scheme (ATAS) when applying for or holding permission on the DES when studying a relevant course for which the course end date had been postponed for more than 3 calendar months.

[appendix-student, ST 14.3]
ST 14.3. An applicant will show academic progress if they are applying for any of the following: (a) to progress from a bachelor’s to master’s level course which is part of an integrated master’s course, where the applicant has been offered a place on a higher-level course by the student sponsor after an assessment of their academic ability; or (b) to progress from a master’s degree to a PhD which is part of an integrated master’s and PhD programme, where the applicant has been offered a place on a higher-level course by the student sponsor after an assessment of their academic ability; or (c) a course which is above the level of the previous course of study for which they were last granted permission unless: (i) the student sponsor is a higher education provider with a track record of compliance; and (ii) the course is at degree level or above; and (iii) the new course is at the same level as the previous course of study; and (iv) the student sponsor confirms that either: (a) the new course of study is related to the applicant’s previous course of study (meaning that it is either connected to the previous course, part of the same subject group, or involves deeper specialisation); or (b) the combination of the previous course of study and the new course of study support the applicant’s genuine career aspirations. (c) the applicant has left an integrated master’s or PhD programme having successfully completed the course leading to the award of the lower level qualification which formed a part of that programme.

[student-caseworker-guidance, When student dependants are permitted]
The scholarship or sponsorship is not required to cover the full fees and living costs of the student in order to permit them to sponsor dependants. However, if this is the case, the applicant must provide separate financial evidence to demonstrate that they meet the financial requirement.
If a scholarship does not cover the living costs for any dependants of the student then the applicant must provide separate financial evidence to cover them.
Students applying with a combined CAS for integrated programmes comprising of an integrated pre master and research master programme will meet the requirement to bring dependants.
The sponsor should confirm on the CAS which the Student’s current permission relies on whether the course of study is a PhD or other doctoral qualification, or a research-based higher degree or not. This will be done via the Academic Course Level field as follows:
RQF_7 / SCQF_11 will denote a ‘taught’ course
RQF_7_Research / SCQF_11_Research will denote a Research course
RQF_8 / SCQF_12 will denote a ‘taught’ course
RQF_8_Research / SCQF_12_Research will denote a Research course
You may write out for this information if it is not otherwise provided.
To be considered a ‘research-based higher degree’ the course of study must meet the definition of a ‘research-based higher degree’ in Paragraph 6.2(b) of the Immigration rules:
‘Research-based higher degree’ means a postgraduate programme comprising a research component (including a requirement to produce original work) that is larger than any accompanying taught component when measured by student effort.
The definition is consistent with that set out in the Higher Education Statistics Agency (HESA)’s Qualification Category.

[appendix-english-language, EL 5.1]
EL 5.1. An applicant will meet the English language requirement if they have an academic qualification which meets one of the requirements at EL 5.2. and is proven by the required evidence under EL 5.3. or EL 5.4.
EL 5.2. The requirements are that the applicant has: (a) a bachelor’s degree, master’s degree or doctorate awarded in the UK; or (b) a degree or degree-level qualification taught in a university or college in a majority- English-speaking country listed in EL 4.1. (except Canada), or Ireland, which meets or exceeds the recognised standard of a bachelor’s degree, master’s degree or doctorate awarded in the UK; or (c) a degree or degree level qualification which meets, or exceeds, the recognised standard of a UK bachelor’s degree; master’s degree or doctorate and was taught or researched in English.
EL 5.3. The requirement at EL 5.2. must be proven by one of: (a) a certificate from the awarding body: or (b) a transcript issued by the university or college that awarded the qualification; or (c) an official letter from the university or college that awarded the qualification containing information equivalent to a degree certificate.
EL 5.4. If the qualification was awarded by a body from outside the UK, the requirement at EL 5.2. must, in addition to the requirement at EL 5.3, be proven by confirmation from the qualification and language assessments provider that the qualification meets the requirements at EL 5.2(b) or EL 5.2(c).

[graduate-caseworker-guidance, Graduate: period to grant]
The period of permission to be granted to an applicant is dependent on the type of course studied and the date the application is made and is set out at Appendix Graduate GR.8.1 and in the following table
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made before 1 January 2027.; All other qualifications | 18 months - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made on or after 1 January 2027.
An applicant whose CAS was assigned for an integrated PhD but who successfully completes the lower postgraduate qualification must be granted 18 months from the date of decision where the Graduate application is made on or after 1 January 2027.

</details>

## q16 (unanswerable)

**Question:** Does any of my time on Student and Graduate visas count toward indefinite leave to remain?

**Reference answer:** I can't find this in the documents I have. To check, see the settlement guidance on GOV.UK or ask your university's international student advisers.

**Agent's answer:**

> I can't find this in the documents I have. You can check GOV.UK or speak to an international student adviser at your university for information on how time spent on Student or Graduate visas counts towards settlement (indefinite leave to remain).

<details><summary>Retrieved text</summary>

[appendix-graduate, GR 6.1]
GR 6.1. The applicant must have held permission as a Student, which was granted to study the relevant qualification in the UK, for a minimum period of time (the relevant period), as in the table below.
Total length of course | Relevant period of Student permission granted during which all study took place in the UK (apart from permitted study abroad programmes); 12 months or less | Full duration of course; Longer than 12 months | At least 12 months
GR 6.2. Where distance learning took place overseas between 24 January 2020 and 30 June 2022, this will not prevent the applicant meeting the requirement to spend the relevant period at GR 6.1 studying in the UK if either: (a) they began a course of 12 months or less prior to 21 June 2021 and entered the UK on or before 27 September 2021 with permission as a Student; or (b) they began a course of 12 months or less between 21 June 2021 and 30 June 2022 and entered the UK on or before 30 June 2022 with permission as a Student.
GR 6.3. Any period of distance learning that took place between 24 January 2020 and 30 June 2022 as part of a course of study lasting longer than 12 months whilst the applicant held permission as a Student, will not prevent the applicant from meeting the requirement to spend the relevant period at GR 6.1. studying in the UK.

[graduate-caseworker-guidance, Study in the UK requirement]
An applicant who made their Student or Tier 4 (General) student application before their course started and started the course before permission was granted (as permitted in the Student route), will have their study time in the UK before permission being granted counted as well. This means that apart from the granted permission period, the period from course start date, as noted on their CAS, to the date of permission being granted, will also be counted. The same applies to applicants who were allowed to start their course before permission was granted due to Covid-19 concessions.
Applicants who studied a course lasting 12 months or less must have spent the full duration of the relevant period of permission course studying in the UK (or on permitted study abroad programs, where relevant) on either the Student route or former Tier 4 (General).
Applicants who complete a course that is longer than 12 months must have been granted at least 12 months of Student or Tier 4 (General) permission. All study that takes place during the 12 months of Student or Tier 4 (General) permission must have taken place in the UK, except for permitted study abroad programmes. For articulation programmes (2+1 and 2+2 programmes), a student must have successfully completed the final year of study in the UK, in other words, the final year is treated for the purpose of this application as the eligible course and the relevant requirement of study in the UK requirement applies depending on the length of such course. A student who undertakes the first year of an articulation programme in the UK and then completes the course overseas will not be eligible.

[graduate-caseworker-guidance, Study in the UK requirement]
An applicant must have studied in the UK for a minimum period as set out in the second column of the table at GR 6.1.
Once concessions on distance learning for the Student route end, students will be required to attend face to face learning in the UK in accordance with the academic engagement policy set out in Document 2 of the Student Sponsor guidance.
For the purposes of assessing the Study in the UK requirement, the caseworker must consider all periods of Student permission which were granted to study the eligible qualification that the applicant subsequently successfully completed. This means that an applicant who was unable to complete their studies in one period of Student permission, for reasons such as maternity leave or sickness and who consequently deferred their studies and completed the course of studies at a later date with Student permission, will have all those periods counted. This also applies to a PhD Student who started their course in the UK, then left the UK overseas research (as part of their qualification) and thus either had their sponsorship withdrawn or was not granted permission as Student for that overseas period, but who subsequently returned to the UK as a Student to successfully complete their course (by, for example: conducting further research, writing up their thesis or submitting their viva). An applicant in these circumstances should not be prevented from meeting the study in the UK requirement if the total length of all those periods of permission meets the relevant requirement.
A course with a start date of 30 September 2020 and an end date of 29 September 2021 is 12 months long. A course is longer than 12 months if it starts on 30 September 2020 and ends on 30 September 2021 or later.

[graduate-caseworker-guidance, Graduate: period to grant]
The period of permission to be granted to an applicant is dependent on the type of course studied and the date the application is made and is set out at Appendix Graduate GR.8.1 and in the following table
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made before 1 January 2027.; All other qualifications | 18 months - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made on or after 1 January 2027.
An applicant whose CAS was assigned for an integrated PhD but who successfully completes the lower postgraduate qualification must be granted 18 months from the date of decision where the Graduate application is made on or after 1 January 2027.

[appendix-graduate, GR 8.1]
GR 8.1. The applicant will be granted the period of permission as set out in the table below:
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made before 1 January 2027.; All other qualifications | 18 months if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made on or after 1 January 2027.

[graduate-caseworker-guidance, Validity requirements]
The caseworker must check the applicant has, or has last had, permission as a student. For the purpose of this requirement, this means an applicant must either:
currently hold valid permission on either the Student route or the Tier 4 (General) route
have held valid permission on the Student or Tier 4 (General) routes which expired but either: one of the paragraph Part Suitability: Exceptions for Overstayers applies the applicant has been given a period of exceptional assurance and has not overstayed that period - in either case the period of overstaying will be disregarded when considering their application
The caseworker must check the applicant’s immigration history to make sure that the applicant has not previously been granted permission under the Doctorate Extension Scheme (DES) or held permission on the Graduate route. If they have previously been granted permission under the DES or on the Graduate route, then the application must be rejected as invalid.
If a student has previously been granted permission on the Tier 1 (Post-study work) route, International Graduate Scheme (IGS) or the Future Talent Working in Scotland Scheme, this will not prevent them from meeting the validation requirements of the Graduate route. If a student has previously been granted permission on one of these routes, the student will need to successfully complete a new eligible qualification at a Higher Education Provider with a track record of compliance and hold valid permission as a student once the route is introduced, they cannot rely on a previous qualification obtained or previous leave as a Student or under Tier 4 to access the route.

[appendix-student, ST 26.6]
ST 26.6. A Student who makes a valid application for permission to stay under the Skilled Worker, or Graduate route, may start employment in a full-time permanent vacancy either up to 3 months prior to the course completion date (for the Skilled Worker route) or once they have successfully completed their course of study (for the Graduate route), provided all of the following apply: (a) the Student is studying a full-time course of study at degree level or above with a higher education provider with a track record of compliance; and (b) the application as a Skilled Worker, or Graduate, was made when the applicant had permission as a Student; and (c) a decision has not been made on the Skilled Worker, or Graduate, application, or where a decision has been made, any Administrative Review against a refusal of that application has not been finally determined.
ST 26.7. DELETED
ST 26.8. A Student may be self-employed, if: (a) they have applied for permission on the Innovator Founder route; and (b) that application is supported by an endorsement from an Innovator Founder endorsing body; and (c) the application was made when the applicant had permission as a Student; and (d) a decision has not been made on the application, or where the application has been refused, any Administrative Review against a refusal has not been finally determined.

</details>

## q17 (unanswerable)

**Question:** If I stay for a bachelor's, master's and PhD and then work, could I qualify for settlement through 10 years' long residence?

**Reference answer:** I can't find this in the documents I have. To check, see the long residence guidance on GOV.UK or ask your university's international student advisers.

**Agent's answer:**

> I can't find this in the documents I have. You can check the current requirements for settlement through 10 years' continuous lawful residence (Appendix Long Residence) and Student visa study time limits on GOV.UK or speak with your university's international student advisers.

<details><summary>Retrieved text</summary>

[appendix-english-language, EL 1.1]
EL 1.1. An applicant for settlement is exempt from the English language requirement if at the date of application any of the following apply: (a) they are aged 65 or over; or (b) they are aged under 18; or (c) they have a disability (physical or mental condition) which prevents them from meeting the requirement; or (d) they are applying for settlement as a partner, parent or dependent child aged over 18 where they: (i) have spent a continuous period of 15 years in the UK with permission; and (ii) can show an English language speaking and listening qualification at A2 CEFR or ESOL entry level 2 or Scottish Credit and Qualification Framework level 3; and (iii) Where the date of application is before 26 March 2027, provide confirmation from a qualified English teacher that the applicant has attended an English language class for at least 75 guided learning hours (not unsupervised study or preparation time) in the 12 months before the date of application and the teacher’s view is the applicant is unlikely to attain B1 level through further study; or (iv) Where the date of application is on or after 26 March 2027, provide confirmation from a qualified English teacher that the applicant has attended an English language class for at least 75 guided learning hours (not unsupervised study or preparation time) in the 12 months before the date of application and the teacher’s view is the applicant is unlikely to attain B2 level through further study.

[appendix-english-language, How the requirement is met]
(p) entry clearance or settlement under Appendix Victim of Domestic Abuse; or
(q) entry clearance, permission to stay or settlement under Appendix HM Armed Forces; or
(r) settlement under Appendix Long Residence; or
(s) entry clearance under Appendix Temporary Work – International Agreement.
if the requirements in EL 7.1 and EL 7.2. are met.
EL 2.5. DELETED.

[appendix-student, ST 19.1]
ST 19.1. If the course is below degree level, the grant of permission must not lead to the applicant being granted more than two years’ permission as a Student to study courses below degree level from the age of 18 unless ST 19.2. applies.
ST 19.2. If the course is below degree level but is subject to a regulatory requirement by the Maritime and Coastguard Agency that the applicant must spend at least 12 months at sea as a part of that course, the grant of permission must not lead to the applicant being granted more than 3 years’ permission as a Student from the age of 18 to study courses below degree level.
ST 19.3. If the course is at degree level, the grant of permission must not lead to the applicant being granted more than five years’ permission as a Student from the age of 18 to study courses at degree level unless the course of study is one of those listed at ST 19.4.
ST 19.4. The five-year maximum period of study at degree level in ST 19.3. will not apply if the applicant has a Confirmation of Acceptance for Studies that has been assigned for a course of study in one of the following subjects: (a) architecture; or (b) medicine; or (c) dentistry; or (d) veterinary medicine and science; or (e) music at a music college that is a member of Conservatoires UK; or (f) law, where the applicant has completed a course at degree level or above and is applying for a course of study which is: (i) a law conversion course validated by the Solicitors Regulation Authority and the Bar Standards Board in England and Wales; or (ii) a Masters in Law (MLaw) in Northern Ireland; or (iii) an accelerated graduate LLB in Scotland.

[student-caseworker-guidance, Calculating time limits]
When calculating periods of permission, the caseworker must consider the duration and level that the Student permission was granted for.
The caseworker must:
when counting time in months: round individual days downwards to the nearest month must not double-count time
count the full period unless there are exceptional compelling and compassionate circumstances (for example, serious illness or disability)
The caseworker must not include any time spent studying in the UK whilst the applicant was under the age of 18.
If the applicant turned 18 during the course of their permission, the caseworker must begin the calculation for the relevant time limit from the date of the applicant’s eighteenth birthday.

[student-caseworker-guidance, Exceptions]
Student applicants who are studying courses in subject areas listed in Appendix Student ST 19.4 are not subject to the limit on study at degree level. This is due to the length of time that these courses generally take to complete.
Exempt courses are as follows:
architecture
medicine
dentistry
veterinary medicine and science
music at a music college that is a member of Conservatoires UK
law, where the applicant has completed a course at degree level or above and is applying for a course of study which is: a law conversion course validated by the Solicitors Regulation Authority and the Bar Standards Board in England and Wales Masters in Law (MLaw) in Northern Ireland an accelerated graduate LLB in Scotland
Permission granted for students to take a role as a Student Union Sabbatical Officer does not count toward a time limit for study, as the CAS for these students is not issued for a course of study, but for a salaried role.

[appendix-english-language, EL 2.1]
EL 2.1. An applicant will meet the English language requirement if any of the requirements in EL 3.1. to EL 7.2 are met.
EL 2.2. The English language requirement is also met by a person applying for entry clearance or permission to stay as a Student if any of the requirements in EL 7.1. to EL 8.4. are met.
EL 2.3. The English language requirement is also met by a person applying for entry clearance or permission to stay as a Skilled Worker route if:
(a) the requirements in EL 7.1. and EL 7.2. are met: or
(b) the requirement in EL 9.1. is met.
EL 2.4. The English language requirement is also met by a person applying for:
(a) entry clearance or permission to stay on the Start-up route, or
(b) entry clearance or permission to stay on the Innovator Founder route; or
(c) entry clearance, permission to stay or settlement on the Scale-up route, or
(d) entry clearance or permission to stay on the High Potential Individual route, or
(e) settlement under Appendix Settlement Family Life, or
(f) settlement under Appendix Private Life, or
(g) entry clearance, permission to stay or settlement on the International Sportsperson route; or
(h) entry clearance, permission to stay or settlement on the Representative of an Overseas Business route; or
(i) entry clearance or permission to stay on the T2 Minister of Religion route; or
(j) settlement on the UK Ancestry route; or
(k) settlement on the Global Talent route; or
(l) settlement on the Domestic Workers in a Private Household route or
(m) settlement on Hong Kong British National (Overseas) route; or
(n) settlement on the Appendix Child Relative (Sponsors with Protection) route; or
(o) settlement on the Appendix Bereaved Partner route; or

[appendix-student, ST 19.5]
ST 19.5. DELETED
ST 19.6. When calculating the period of permission granted under ST 19.1. to ST 19.5., any period of permission as a Student extended under section 3C of the Immigration Act 1971 will count towards the period of permission granted.

[appendix-student, ST 14.1]
ST 14.1. An applicant who has, or previously had, permission as a Student and is applying for permission to stay as a Student must have successfully completed the course of study for which they were last granted permission as a Student or one of the following applies: (a) one of the exceptions in ST 14.4.; or (b) they are applying to progress to a higher level course as specified in ST 14.3.(a) or (b).; or (c) they have successfully completed the course of study for which they were last granted permission as a Student or the course of study they were allowed to change to without applying for further permission on the Student route and will now be taking a course at the same level as specified at ST 14.3(c); or (d) they have successfully completed the course of study with their sponsor where the change of course was allowed without applying for further permission on the Student route.
ST 14.2. An applicant who has, or previously had, permission on the Student route and is applying for permission to stay as a Student must show academic progress from the previous courses of study unless one of the exceptions in ST 14.4. applies.

[student-caseworker-guidance, Deciding whether the application complies with the time limit requirement]
the applicant is applying to study at a higher education provider (HEP) with a track record of compliance, is subject to the time limit stated in Appendix Student ST 19.3, and is studying for five year’s at degree level, for example: a student is applying for permission to stay to complete their bachelor’s degree, the Student originally enrolled on a 3-year bachelor’s degree but subsequently repeated 2 academic years. Their permission began on 01 August 2021 and, if granted, their subsequent permission would expire on 01 October 2026. This would be permitted as the period only exceeds 5 years on the basis of the extra periods granted before and after the course (5 academic years of study, plus 1 month granted before the course and 4 months granted after the course)
If these circumstances apply, the caseworker must not refuse the application on the basis that the time limit would be breached.
These provisions enable a Student to study for up to 5 academic years without being disadvantaged by any periods of permission in the UK where they are not studying. An example of this could include but is not limited to, the period granted before study and the wrap-up period granted at the end of their course.
For the avoidance of doubt, this concession is not intended to extend the time limits for all applicants. Students who have already undertaken the maximum period of academic study will not benefit. For example, if a Student has already studied for 5 academic years at degree level, they are not eligible to extend their time in the UK for the purpose of commencing a 6th academic year of study at this level.

[student-caseworker-guidance, Above degree level study]
There is no maximum study requirement for applicants who are studying a course above degree level.
The caseworker must calculate whether an applicant’s previous study and their proposed study would exceed the maximum period of study permitted.
To determine whether to grant a Student’s application for permission to undertake their proposed course of study, the caseworker must determine how much time the applicant has previously spent studying on the Student or Tier 4 routes to study courses at the relevant level (including any periods of permission extended by 3C), and add the length of permission that would be granted if the current application is successful.
To calculate periods of permission counting toward the maximum study limit, the caseworker must add the proposed period of permission together with any current or previous permission at the specific study level. This period will be counted either from:
the date permission would begin if granted (for entry clearance)
the date the current permission began (for permission to stay)
The period of permission will be counted until the day the permission – if granted – would expire.
The caseworker must also count any previous periods of permission as a Student, or periods of leave under Tier 4 (General) migrant, including where the applicant has subsequently left the UK. Each period will be counted from the date the permission began until the date it expired unless there are exceptional compelling and compassionate circumstances that either prevented the student from completing the course within the time given or caused them to leave their course prematurely (for example, serious illness or disability). If the applicant extended their Student permission (including under 3C), this will be included. If the applicant’s permission was curtailed, the caseworker must take the date the curtailed permission expired.

[student-caseworker-guidance, Deciding whether the application complies with the time limit requirement]
If the caseworker’s calculation shows that the length of the course applied for in the current application would lead to the applicant having spent more than the maximum period permitted, they must normally refuse the application.
Student applicants can exceed the time limits set out in Appendix Student ST 19 if one of the following scenarios applies:
the applicant is applying to study a 3 year maritime course detailed in Appendix Student ST 19.2, the applicant has never studied in the UK before and the period granted at the end of the course would make the applicant exceed the limit (for example if the Student permission would begin on 01 January 2021 and expire on 01 June 2025, the total duration would be 3 years 5 months, this would be permitted as the period exceeds 3 years on the basis of the extra periods granted before and after the course)
the applicant is applying to study a course subject to the below degree level limit stated in Appendix Student ST 19.1, the applicant has never studied in the UK before and the course is a 2 year course (for example if the Student permission would begin 01 January 2021 and expire on 01 June 2023, this would be permitted as the period exceeds 2 years on the basis of the extra periods granted before and after the course)

[student-caseworker-guidance, Degree level study]
The amount of time that an applicant can spend studying at degree level is stated in Appendix Student ST 19.3. Any period studied whilst on Tier 4 or any other predecessor to the Student route will count towards the calculation of degree level study.

[appendix-english-language, EL 3.1]
EL 3.1. An applicant will meet the English language requirement if they have already shown they met the requirement, at the level required for their current application, in a previous successful application for entry clearance or permission to stay.
EL 4.1. An applicant will meet the English language requirement if they are a national of any of the following majority-English-speaking countries: Antigua and Barbuda Australia The Bahamas Barbados Belize The British Overseas Territories Canada Dominica Grenada Guyana Jamaica Malta New Zealand St Kitts and Nevis St Lucia St Vincent and the Grenadines Trinidad and Tobago United States of America

</details>

## q18 (multi)

**Question:** Can I fly home for Christmas while my Graduate visa application is pending, and once it's granted, can I travel abroad and come back?

**Reference answer:** No: you must not travel outside the UK, Ireland, the Channel Islands or the Isle of Man until you get a decision, or your application will be withdrawn. Once the Graduate visa is granted, you can travel abroad and return to the UK.

**Agent's answer:**

> You must not travel outside of the UK, Ireland, the Channel Islands or the Isle of Man until you get a decision on your Graduate visa application, and your application will be withdrawn if you do [graduate-visa-guide, When you’ve got your documents ready]. Additionally, you must be in the UK when you apply for a Graduate visa [appendix-graduate, GR 1.2].
> 
> Once your Graduate visa is granted, you are able to travel abroad and return to the UK [graduate-visa-guide, What you can and cannot do, graduate-caseworker-guidance, Graduate: grant permission to stay].

<details><summary>Retrieved text</summary>

[graduate-caseworker-guidance, Graduate: grant permission to stay]
If the applicant meets all of the requirements of Appendix Graduate of the Immigration Rules and none of the general grounds for refusal apply, the caseworker must grant permission to stay with the appropriate conditions.
Graduates are able to travel out of and re-enter the UK whilst they hold valid permission as a Graduate.

[graduate-visa-guide, When you’ve got your documents ready]
You can apply online for a Graduate visa once your documents are ready.
You must apply online for a Graduate visa.
Check which documents you’ll need to apply.
Your partner or children will need to apply separately.
As part of your application, you’ll need to prove your identity. How you do this depends on where you’re from and the type of passport or resident permit you have.
You’ll either:
use the ‘UK Immigration: ID Check’ app to scan your identity document - you’ll also create or sign into your UK Visas and Immigration (UKVI) account
have your fingerprints and photo (biometric information) taken at a UK Visa and Citizenship Application Services (UKVCAS) service point
You’ll be told what you need to do when you apply.
If you do need to go to a UKVCAS service point, they may need to keep your passport and documents while they process your application.
You must not travel outside of the UK, Ireland, the Channel Islands or the Isle of Man until you get a decision. Your application will be withdrawn if you do.

[graduate-visa-guide, When to apply]
You must apply before your Student visa or Tier 4 (General) student visa expires.
You can apply after your education provider (such as your university or college) has told the Home Office that you’ve successfully completed the course you took with your Student or Tier 4 (General) student visa. You do not have to wait until you’ve graduated or have been given a certificate.
As part of your application, you’ll need to prove your identity and provide your documents.
Your application may take longer if you need an appointment to do this. You’ll find out if you need one when you start your application.

[graduate-visa-guide, What you can and cannot do]
With a Graduate visa you can:
work in most jobs
look for work
be self-employed
continue living in the UK with your partner and children, if they’re eligible
travel abroad and return to the UK
do voluntary work
Any voluntary work you do must be unpaid and for one of the following:
a registered charity
a voluntary organisation
an associated fundraising body (an organisation that raises money for a charity or voluntary organisation)
a statutory body (a government-appointed body, for example Historic England)
You cannot:
apply for most benefits (public funds), or the State Pension
work as a professional sportsperson
If your application is successful, you’ll get a full list of what you can and cannot do with a Graduate visa.

[appendix-graduate, GR 1.1]
GR 1.1. A person applying for permission to stay as a Graduate must apply online on the gov.uk website on the specified form “Graduate”.
GR 1.2. An application for permission as a Graduate must meet all the following requirements: (a) any fee and Immigration Health Charge must have been paid; and (b) the applicant must have provided biometrics when required; and (c) the applicant must have provided a passport or other document which satisfactorily establishes their identity and nationality; and (d) the applicant must be in the UK.
GR 1.3. The applicant must have, or have last had, permission as a Student.
GR 1.4. The applicant must not have been previously granted permission under the Doctorate Extension Scheme or as a Graduate.
GR 1.5. If the applicant has in the 12 months before the date of application completed a course of studies in the UK for which they have been awarded a scholarship or sponsorship by a Government or international scholarship agency covering both fees and living costs for study in the UK, they must provide written consent to the application from that Government or agency.
GR 1.6. An application which does not meet all the validity requirements for a Graduate may be rejected as invalid and not considered.

</details>

## q19 (single)

**Question:** I've got a graduate job offer and I'm applying for a Skilled Worker visa while I'm still on my Student visa. How early can I start the job?

**Reference answer:** Once you've made a valid Skilled Worker application, you can start the job up to 3 months before your course completion date. This applies if you're on a full-time course at degree level or above at a higher education provider with a track record of compliance, you applied while you had Student permission, and the application hasn't been decided yet (or an administrative review of a refusal is still pending).

**Agent's answer:**

> As a Student visa holder switching to the Skilled Worker route, you may start employment in a full-time permanent vacancy **up to 3 months prior to your course completion date**, provided that all of the following conditions are met:
> 
> * Your application for the Skilled Worker visa was made while you still had valid permission as a Student [appendix-student, ST 26.6].
> * A decision has not yet been made on your Skilled Worker application (or, if it was refused, any Administrative Review against that refusal has not yet been finally determined) [appendix-student, ST 26.6].
> * You are studying a full-time course of study at degree level or above with a higher education provider that has a track record of compliance [appendix-student, ST 26.6].

<details><summary>Retrieved text</summary>

[appendix-student, ST 26.6]
ST 26.6. A Student who makes a valid application for permission to stay under the Skilled Worker, or Graduate route, may start employment in a full-time permanent vacancy either up to 3 months prior to the course completion date (for the Skilled Worker route) or once they have successfully completed their course of study (for the Graduate route), provided all of the following apply: (a) the Student is studying a full-time course of study at degree level or above with a higher education provider with a track record of compliance; and (b) the application as a Skilled Worker, or Graduate, was made when the applicant had permission as a Student; and (c) a decision has not been made on the Skilled Worker, or Graduate, application, or where a decision has been made, any Administrative Review against a refusal of that application has not been finally determined.
ST 26.7. DELETED
ST 26.8. A Student may be self-employed, if: (a) they have applied for permission on the Innovator Founder route; and (b) that application is supported by an endorsement from an Innovator Founder endorsing body; and (c) the application was made when the applicant had permission as a Student; and (d) a decision has not been made on the application, or where the application has been refused, any Administrative Review against a refusal has not been finally determined.

[student-visa-guide, When to apply]
The earliest you can apply is 3 months before your course starts.
You must apply before your current visa expires. Your new course must begin within 28 days of your current visa expiring.
For example, if your visa expires on 1 December, you must apply for a new visa before 1 December. Your new course must begin by 29 December.
You must also apply within 6 months of getting a Confirmation of Acceptance for Studies (CAS).
You can stay in the UK until you get your decision.
If you applied for an administrative review because your application was refused, you can stay in the UK until you get your review decision.

[student-caseworker-guidance, Retrospective course start dates]
Sponsors can issue a CAS for a course which has already started; however, the sponsorship management system does not allow sponsors to enter a date that has already passed into the ‘course start date’ field on a CAS.
If the course start date has passed before a CAS is assigned, sponsors must enter in the ‘course start date’ field:
the date that the CAS is created if the applicant is starting their course late, and note the actual course start date in the ‘sponsor note’ section
the date that the CAS is created if the applicant – after completing a study abroad programme or work placement – is applying for further permission to stay to complete their course, and note the actual course start date (the date the change of course commenced) in the ‘sponsor note’ field
the date that the change of course is expected to commence if the applicant is changing course (for example, if they are moving from the lower level to the higher level of an integrated Masters course, or if they are adding a study abroad programme or work placement to their course)
the date from which the applicant requires their next period of permission to start if they are being sponsored to extend their permission so as to continue studying the same course (for example, an applicant may require their next period of permission to start the day after their current permission expires so as to continue studying the same course)

[student-caseworker-guidance, The Student or Child Student has completed the course for which they were given permission to stay]
If the student has successfully completed the course the Confirmation of Acceptance for Studies (CAS) was issued for, they will need to make a new application for permission to stay for their new course.
The student must make a valid application that meets the date of application requirement. To be able to begin their course before a decision has been made, the following must be true:
the sponsor has Student Sponsor status;
the sponsor has assigned them a CAS;
they applied to us before starting their course; and
they applied to us before their existing permission to stay expired.
To be able to begin their new course before submitting a valid application for further permission as a Student the following must be true:
the student is studying at a HEP that has a track record of compliance;
the student is currently sponsored by them and has finished their last course;
the student’s permission to stay has not yet expired; and
the student will be studying their new course with their existing sponsor;
In all other circumstances a student must make an application for permission to stay and must not start their new course until the Home Office have approved their new application.
If a student has left an integrated masters or PhD programme with the lower level qualification, this will be deemed to be successfully completing the course of study for which the CAS was assigned. These students will be able to meet the academic progression requirement for an in-country application, if the course of study listed on the CAS is at the same level or higher than the level of study on the previous CAS issued for the integrated programme.

[student-visa-guide, How long it takes to get a decision]
A decision will usually be made within 8 weeks.
You may be able to pay to get a faster decision.
You’ll be contacted if your application is complex and will take longer, for example because:
your supporting documents need to be verified
you need to attend an interview
of your personal circumstances (for example if you have a criminal conviction)
If you need to change something in your application after you’ve sent it contact UK Visas and Immigration (UKVI).
You can ask to withdraw your application by contacting UKVI. Your fee will only be refunded if UKVI has not started processing your application.
You’ll get an eVisa (a digital record of your identity and immigration status).
Your decision email or letter will tell you how to get access to your eVisa. You’ll need to create a UKVI account.

</details>

## q20 (multi)

**Question:** My scholarship covers my tuition but not my living costs. Do I still have to show living costs, and what evidence do I need from my sponsor?

**Reference answer:** Yes. You can combine sources, so an official financial sponsor (such as a government, the British Council, an international organisation or company, or a university) can cover your tuition while you show your own money or a student loan for living costs, unless you've been in the UK with a valid visa for at least 12 months. For the scholarship, you need either the funding stated on your CAS, if your university is the sponsor, or a letter of confirmation from the sponsor.

**Agent's answer:**

> Yes, you must still show that you have enough money to cover your living costs unless you meet an exemption (such as having been in the UK with a valid visa for at least 12 months) [student-visa-guide, Money to support yourself (‘financial requirement’)]. Under the Student route, the financial requirement covers both your course fees and your living costs [student-caseworker-guidance, Non-boarding students]. Because your scholarship only covers tuition, you will need to demonstrate that you hold the required funds for your living costs (for up to 9 months, depending on whether your course is in or outside London) [student-visa-guide, Money to support yourself (‘financial requirement’)] by another accepted method, such as personal bank accounts meeting the 28-day holding requirement [student-visa-guide, Money to support yourself (‘financial requirement’); appendix-finance, FIN 8.3].
> 
> Regarding the evidence needed from your sponsor:
> * If your student sponsor (your university) is providing any portion of your financial sponsorship or a bursary, the funds being provided must be stated on your Confirmation of Acceptance for Studies (CAS) [student-caseworker-guidance, Student: financial requirement; appendix-finance, FIN 9.1]. 
> * If your sponsorship is provided by an official financial sponsor (such as His Majesty’s Government, your national government, the British Council, an international organisation, an international company, a university, or an independent school) [appendix-finance, FIN 8.4] covering your tuition fees, you must provide either the details stated on your CAS or a letter of confirmation from the official financial sponsor [appendix-finance, FIN 9.1].

<details><summary>Retrieved text</summary>

[student-visa-guide, Money to support yourself (‘financial requirement’)]
You’ll need to show you have enough money to support yourself - unless you’ve been in the UK with a valid visa for at least 12 months on the date of your application.
How much money you need depends on where you will be studying. You’ll need either:
£1,529 per month (for up to 9 months) for courses in London
£1,171 per month (for up to 9 months) for courses outside London
If you’re boarding at a residential independent school, you’ll need to pay boarding fees instead. The amount you need to pay will be on your CAS.
London means the City of London and the 32 London boroughs.
You’ll need to prove you have extra money for each family member you bring with you.
You must have this money for at least 28 days in a row. The end date of the 28-day period must be within 31 days of the date you apply for your visa.
Example
If you submit your application on 1 January, you’d have to show that the funds were in your bank account for at least the 28-day period ending on 1 December.
If you have a student loan or financial sponsorship, you’ll need to provide evidence of this from your loan or sponsorship company.
Read the guidance on finances for student applications for more information about the money you need and how to prove it.

[student-caseworker-guidance, Non-boarding students]
To score 20 points for the financial requirement, an applicant who is not a boarder must show they have enough money to pay for:
course fees
living costs
Applicants applying for a new course from overseas and those who have been in the UK for less than a year must demonstrate that they have enough money to pay the course fees for either:
one academic year of the course
the entire course (if it is less than a year long)
The amount an applicant will pay for course fees is stated by the Student sponsor on the CAS. The CAS will also confirm if there is no fee to pay.

[student-caseworker-guidance, Student: financial requirement]
This page tells caseworkers about the financial requirement that an applicant under the Student route must meet.
To score 10 points for meeting the financial requirement, the applicant must show that they have sufficient funds to pay outstanding course fees for the first academic year and can demonstrate funds to cover their living costs for up to 9 months.
Information on how evidence of funds can be demonstrated can be found in Appendix Finance and the level of funds which an applicant must demonstrate can be found in Appendix Student ST 12.
The following applicants will automatically meet the financial requirement and be awarded 10 points:
where they are applying for permission to stay in the UK, having been in the UK for at least 12 months with valid permission on the date of application
where they are applying for permission as a Student Union Sabbatical Officer
The applicant must show that they have held the required level of funds for a consecutive 28 day period, unless they are relying on a student loan, an award from an official financial sponsor, or where they are receiving some portion of the funds or other financial sponsorship from their student sponsor (as a bursary, for example). The 28 day period must end no more than 31 days before the application date.

[student-visa-guide, Money you need]
You must have enough money to pay for your course and support yourself in the UK.
How much money you need depends on your circumstances and what you’re applying for.
You need enough money to pay for your course for 1 academic year (up to 9 months). The amount you need to pay will be on your Confirmation of Acceptance for Studies (CAS).
If you’ve been in the UK with a valid visa for at least 12 months, you do not need to prove you have this money for your visa application.

[appendix-student, ST 12.1]
ST 12.1. If the applicant is applying for permission to stay and has been living in the UK with permission for 12 months or more on the date of application, they will meet the financial requirement and do not need to show funds.
ST 12.2. If the applicant is applying for entry clearance or permission to stay and is applying as a Student Union Sabbatical Officer they will meet the financial requirement and do not need to show funds.
ST 12.3. If ST 12.2. does not apply, and the applicant is applying for entry clearance, or is applying for permission to stay and has been in the UK with permission for less than 12 months, the applicant must have the following funds:
(a) Studying in London
Type of Study | Funds required; Residential Independent School | Sufficient funds to pay outstanding fees (course fees and boarding fees) for one academic year; All other cases | Sufficient funds to pay any outstanding course fees as stated on the Confirmation of Acceptance for Studies, and £1529 for each month of the course (up to a maximum of 9 months)
(b) Studying outside London
Type of Study | Funds required; Residential Independent School | Sufficient funds to pay outstanding fees (course fees and boarding fees) for one academic year; All other cases | Sufficient funds to pay any outstanding course fees as stated on the Confirmation of Acceptance for Studies, and £1171 for each month of the course (up to a maximum of 9 months)
If the length of the applicant’s course includes a part of a month, the time period will be rounded up to the next full month.

[appendix-finance, FIN 9.1]
FIN 9.1. An applicant relying on funds provided by an official financial sponsor under FIN 8.3.(b) must provide evidence, either: (a) where the student sponsor is providing financial sponsorship, the funds being provided must be stated in the Confirmation of Acceptance for Studies; or (b) a letter of confirmation from the official financial sponsor.
FIN 9.2. An applicant relying on a student loan under FIN 8.3.(c), must show evidence of the student loan by providing a student loan letter from the lender which must: (a) be dated no more than 6 months before the date of application; and (b) confirm the loan is a student loan provided to the applicant by either the relevant government or a government sponsored student loan company or an academic or educational loans scheme; and (c) confirm there are no conditions on release of the loan funds other than a successful application to study in the UK as a Student or Child Student; and (d) confirm the amount of the loan; and (e) confirm the loan is to the applicant; and (f) confirm the funds will be: (i) available to the applicant before they travel to the UK; or (ii) paid directly to the student sponsor before the applicant travels to the UK, with any living cost portion of the loan being made available to the applicant by the time they arrive in the UK; or (iii) available before the applicant begins their course if the loan is provided by the applicant’s national government; and (g) confirm the lender meets the requirement at FIN 8.3(c).

[appendix-finance, FIN 8.4]
FIN 8.4. An applicant applying as a Short-Term Student will meet financial requirements if they provide evidence of any of the following (or a combination of them): (a) money held in an account that meets the requirements set out in FIN 5.1. and FIN 8.1; or (b) sufficient funds from an official financial sponsor, which must be His Majesty’s Government, the applicant’s national government, the British Council or any international organisation, international company, university or Independent School.

[student-caseworker-guidance, Evidence that can be used to demonstrate funds for the dependant of a Student]
Unless a dependant is making an application at the same time as a Student and Appendix Student ST 22.1 applies, they must submit evidence that they meet the financial requirement.
Dependants of a student can rely on the following as evidence of funds available to them to meet the financial requirement:
bank account or building society statements that meet the requirements of Appendix Finance FIN 5.1 and FIN 8.1
a sponsorship letter from an official financial sponsor of the Student that states the sponsorship will also cover living costs for the Student’s dependants and which names those dependants
The caseworker should assess whether the funds shown in the evidence provided are sufficient to meet the financial requirement in the same way they consider evidence for Students.
For information on how the financial requirement for Students is assessed, see: Student: financial requirement.
For information on how evidence that someone meets the financial requirement is assed, see: Appendix Finance guidance.

[student-caseworker-guidance, Evidence requirements]
Appendix Finance guidance sets out where specific evidence must be provided, for example confirmation of a student loan or official financial sponsorship, or proof of relationship where relying on parental funds. The applicant will be asked to provide this evidence as part of the application process.
The caseworker can find out what type of evidence the applicant is relying on by checking the application form.
If the applicant is relying on funds from a third party then the caseworker should check the relationship between the applicant and the third party and if it is unclear, consider contacting the applicant to ask for further information.
Caseworkers should also take a fair and proportionate approach to the assessment of evidence.

[appendix-finance, FIN 6.1]
FIN 6.1. Promises of future third-party support will not be accepted as evidence of funds, except where this is specified in the route under which the applicant is applying.
FIN 7.1. The most recently dated piece of financial evidence must be dated within 31 days before the date of application.
FIN 7.2. The length of time for which funds are held will be calculated by counting back from the date of the closing balance on the most recently dated piece of financial evidence.
FIN 7.3. The financial evidence provided must cover the whole period of time for which the funds must be held.

[appendix-finance, Introduction]
This Appendix sets out how the financial requirement must be met.
The routes set out the requirements for the amount of funds and length of time they must be held.
This Appendix applies to applications under these routes: • Appendix Child Student • Appendix Domestic Worker in a Private Household • Appendix Global Business Mobility – Senior or Specialist • Appendix Global Business Mobility – Graduate Trainee • Appendix Global Business Mobility – UK Expansion Worker • Appendix Global Business Mobility – Service Supplier • Appendix Global Business Mobility – Secondment Worker • Appendix Global Talent • Appendix High Potential Individual • Appendix Hong Kong British National (Overseas) • Appendix Innovator Founder • Appendix International Sportsperson • Appendix Parent of a Child Student • Appendix Representative of an Overseas Business • Appendix Scale-up • Appendix Short-term Student • Appendix Skilled Worker • Appendix Start-up • Appendix Student • Appendix Temporary Work - Charity Worker • Appendix Temporary Work - Creative Worker • Appendix Temporary Work - International Agreement • Appendix Temporary Work - Government Authorised Exchange • Appendix Temporary Work - Religious Worker • Appendix Temporary Work - Seasonal Worker • Appendix T2 Minister of Religion • Appendix UK Ancestry • Appendix Visitor • Appendix Youth Mobility Scheme

[appendix-finance, FIN 8.1]
FIN 8.1. Funds may be held in any form of personal bank or building society account (including current, deposit, savings, pension from which the funds can be withdrawn or investment account) provided the account allows the funds to be accessed immediately.
FIN 8.2. Funds held in other accounts or financial instruments such as shares, bonds, credit cards, pensions from which the funds cannot be withdrawn immediately, regardless of notice period, will not be accepted as evidence of funds.
FIN 8.3. An applicant applying as a Student or Child Student, will meet the financial requirements if they provide evidence of any of the following (or a combination of them): (a) money held in an account that meets the requirements set out in FIN 5.1. and FIN 8.1; or (b) funds provided by an official financial sponsor, which must be His Majesty’s Government, the applicant’s national government, the British Council or any international organisation, international company, university or Independent School; or (c) a student loan provided by: (i) a government; or (ii) a government sponsored student loan company; or (iii) an academic or educational loans scheme which is provided by a financial institution regulated for the purpose of issuing student loans by either the Financial Conduct Authority (FCA) or the Prudential Regulation Authority (PRA) or, in the case of an overseas loan, the official regulatory body for purpose of issuing student loans in the country the institution is in and where the money is held.

</details>

## q21 (multi)

**Question:** My parents' savings are in Indian rupees. Which exchange rate is used to check the amount, and how long does the money need to have been in the account?

**Reference answer:** The rupees are converted into pounds using the spot exchange rate on www.oanda.com for the date of your application. The money must have been in the account for at least 28 days in a row, and that 28-day period must end within 31 days of the date you apply.

**Agent's answer:**

> Based on the official immigration rules and guidance:
> 
> * **Exchange rate:** When money is held in a foreign currency such as Indian rupees, it is converted into pound sterling (£) using the spot exchange rate that appears on **www.oanda.com** for the date of the application [appendix-finance, FIN 1.1].
> * **Length of time:** You must show that the required level of funds has been held in the account for a **consecutive 28-day period** [student-caseworker-guidance, Student: financial requirement]. 
> * **End date of the period:** This 28-day period must end no more than **31 days before the date you apply** [student-caseworker-guidance, Student: financial requirement]. The length of time is calculated by counting back from the date of the closing balance on your most recently dated piece of financial evidence, and the evidence must cover the whole 28-day period [appendix-finance, FIN 7.2, FIN 7.3].

<details><summary>Retrieved text</summary>

[appendix-finance, FIN 1.1]
FIN 1.1. Where money is held in one or more foreign currencies, this will be converted into pound sterling (£) using the spot exchange rate which appears on www.oanda.com for the date of the application unless FIN 1.2. or FIN 1.3. applies.
FIN 1.2. Where money is held in one or more foreign currencies and the exchange rate for a foreign currency does not appear on www.oanda.com, this will be converted into pound sterling (£), using the monthly FCDO Consular Exchange Rate (“CER”) rate published at www.gov.uk/government/publications/fco-consular-services-abroad-exchange-rates on the date of application. The following currencies do not appear on www.oanda.com: • Syrian Pounds • Mongolian Tugrik
FIN 1.3. The following currencies will also be converted into pound sterling (£) using the monthly FCDO CER rate published at www.gov.uk/government/publications/fco-consular-services-abroad-exchange-rates applicable on the date of application: • Iranian Rials.

[student-caseworker-guidance, Student: financial requirement]
This page tells caseworkers about the financial requirement that an applicant under the Student route must meet.
To score 10 points for meeting the financial requirement, the applicant must show that they have sufficient funds to pay outstanding course fees for the first academic year and can demonstrate funds to cover their living costs for up to 9 months.
Information on how evidence of funds can be demonstrated can be found in Appendix Finance and the level of funds which an applicant must demonstrate can be found in Appendix Student ST 12.
The following applicants will automatically meet the financial requirement and be awarded 10 points:
where they are applying for permission to stay in the UK, having been in the UK for at least 12 months with valid permission on the date of application
where they are applying for permission as a Student Union Sabbatical Officer
The applicant must show that they have held the required level of funds for a consecutive 28 day period, unless they are relying on a student loan, an award from an official financial sponsor, or where they are receiving some portion of the funds or other financial sponsorship from their student sponsor (as a bursary, for example). The 28 day period must end no more than 31 days before the application date.

[student-visa-guide, If you’re from a country listed under the ‘differential evidence requirement’]
You do not need to prove you have enough money to support yourself if you’re a British national overseas or from one of the following countries or territories:
Australia
Austria
Bahrain
Barbados
Belgium
Botswana
Brazil
Brunei
Bulgaria
Cambodia
Canada
Chile
China
Croatia
Republic of Cyprus
Czechia
Denmark
The Dominican Republic
Estonia
Finland
France
Germany
Greece
Hong Kong
Hungary
Iceland
Indonesia
Ireland
Italy
Japan
Kazakhstan
Kuwait
Latvia
Liechtenstein
Lithuania
Luxembourg
Macao
Malaysia
Malta
Mauritius
Mexico
Netherlands
New Zealand
Norway
Oman
Peru
Poland
Portugal
Qatar
Romania
Serbia
Singapore
Slovakia
Slovenia
South Korea
Spain
Sweden
Switzerland
Taiwan
Thailand
Tunisia
United Arab Emirates
United States of America
However, you might be asked to provide this evidence before you get a decision on your application.
If you do need to provide it, you’ll be contacted by UK Visas and Immigration (UKVI) after you’ve submitted your application.
Read the guidance on finances for student applications for more information about the money you need and how to prove it.

[appendix-student, ST 12.1]
ST 12.1. If the applicant is applying for permission to stay and has been living in the UK with permission for 12 months or more on the date of application, they will meet the financial requirement and do not need to show funds.
ST 12.2. If the applicant is applying for entry clearance or permission to stay and is applying as a Student Union Sabbatical Officer they will meet the financial requirement and do not need to show funds.
ST 12.3. If ST 12.2. does not apply, and the applicant is applying for entry clearance, or is applying for permission to stay and has been in the UK with permission for less than 12 months, the applicant must have the following funds:
(a) Studying in London
Type of Study | Funds required; Residential Independent School | Sufficient funds to pay outstanding fees (course fees and boarding fees) for one academic year; All other cases | Sufficient funds to pay any outstanding course fees as stated on the Confirmation of Acceptance for Studies, and £1529 for each month of the course (up to a maximum of 9 months)
(b) Studying outside London
Type of Study | Funds required; Residential Independent School | Sufficient funds to pay outstanding fees (course fees and boarding fees) for one academic year; All other cases | Sufficient funds to pay any outstanding course fees as stated on the Confirmation of Acceptance for Studies, and £1171 for each month of the course (up to a maximum of 9 months)
If the length of the applicant’s course includes a part of a month, the time period will be rounded up to the next full month.

[student-visa-guide, Money to support yourself (‘financial requirement’)]
You’ll need to show you have enough money to support yourself - unless you’ve been in the UK with a valid visa for at least 12 months on the date of your application.
How much money you need depends on where you will be studying. You’ll need either:
£1,529 per month (for up to 9 months) for courses in London
£1,171 per month (for up to 9 months) for courses outside London
If you’re boarding at a residential independent school, you’ll need to pay boarding fees instead. The amount you need to pay will be on your CAS.
London means the City of London and the 32 London boroughs.
You’ll need to prove you have extra money for each family member you bring with you.
You must have this money for at least 28 days in a row. The end date of the 28-day period must be within 31 days of the date you apply for your visa.
Example
If you submit your application on 1 January, you’d have to show that the funds were in your bank account for at least the 28-day period ending on 1 December.
If you have a student loan or financial sponsorship, you’ll need to provide evidence of this from your loan or sponsorship company.
Read the guidance on finances for student applications for more information about the money you need and how to prove it.

[appendix-finance, Introduction]
This Appendix sets out how the financial requirement must be met.
The routes set out the requirements for the amount of funds and length of time they must be held.
This Appendix applies to applications under these routes: • Appendix Child Student • Appendix Domestic Worker in a Private Household • Appendix Global Business Mobility – Senior or Specialist • Appendix Global Business Mobility – Graduate Trainee • Appendix Global Business Mobility – UK Expansion Worker • Appendix Global Business Mobility – Service Supplier • Appendix Global Business Mobility – Secondment Worker • Appendix Global Talent • Appendix High Potential Individual • Appendix Hong Kong British National (Overseas) • Appendix Innovator Founder • Appendix International Sportsperson • Appendix Parent of a Child Student • Appendix Representative of an Overseas Business • Appendix Scale-up • Appendix Short-term Student • Appendix Skilled Worker • Appendix Start-up • Appendix Student • Appendix Temporary Work - Charity Worker • Appendix Temporary Work - Creative Worker • Appendix Temporary Work - International Agreement • Appendix Temporary Work - Government Authorised Exchange • Appendix Temporary Work - Religious Worker • Appendix Temporary Work - Seasonal Worker • Appendix T2 Minister of Religion • Appendix UK Ancestry • Appendix Visitor • Appendix Youth Mobility Scheme

[student-caseworker-guidance, Child Student: financial requirement]
This page tells caseworkers about the financial requirement that an applicant under the Child Student route must meet.
The funds needed to meet the financial requirement for Child Student applicants depend on whether they are:
boarding students
non-boarding students
A non-boarding student is any Child Student who is not being accommodated by their Student sponsor at the residential independent school where they are, or will be, studying.
Information on how evidence of funds can be demonstrated can be found in Appendix Finance and the level of funds which an applicant must demonstrate can be found in Appendix Child Student CS.10.
The applicant must show the required level of funds held for a consecutive 28 day period, unless they are relying on a student loan, an award from a government or international sponsorship agency, or where they are receiving some portion of the funds as other financial sponsorship from their student sponsor (as a bursary, for example). The 28 day period must end no more than 31 days before the application date.
The applicant must not be financially responsible for anyone else.

[appendix-finance, FIN 6.1]
FIN 6.1. Promises of future third-party support will not be accepted as evidence of funds, except where this is specified in the route under which the applicant is applying.
FIN 7.1. The most recently dated piece of financial evidence must be dated within 31 days before the date of application.
FIN 7.2. The length of time for which funds are held will be calculated by counting back from the date of the closing balance on the most recently dated piece of financial evidence.
FIN 7.3. The financial evidence provided must cover the whole period of time for which the funds must be held.

[student-caseworker-guidance, Evidence of finance]
This section tells caseworkers how to assess whether a Student, their dependants or a Child Student has met the financial requirement.
Applicants who need to show funds, must show they meet the financial requirement using evidence as set out in Appendix Finance.

</details>

## q22 (multi)

**Question:** My CAS says I need an ATAS certificate. Do I need it before I apply, and how far ahead of my course start can I send in my visa application?

**Reference answer:** Yes, you must already have a valid ATAS certificate and include it with your visa application. If you're applying from outside the UK, the earliest you can apply is 6 months before your course starts; from inside the UK, it's 3 months before.

**Agent's answer:**

> Yes, if the ATAS requirement applies to your course, you must have a valid ATAS certificate and provide it with your visa application [appendix-student, ST 8.4]. If you are required to have one and do not provide it, your application will be refused [student-caseworker-guidance, ATAS requirements].
> 
> How far ahead you can submit your visa application depends on whether you are applying from outside or inside the UK:
> 
> * **If you are applying from outside the UK (Entry Clearance):** You can submit your application no more than **6 months** before the course start date stated on your CAS [appendix-student, ST 4.1].
> * **If you are applying from inside the UK (Permission to Stay):** You can submit your application no more than **3 months** before the course start date stated on your CAS [appendix-student, ST 4.2].

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, ATAS requirements]
An applicant must hold a valid ATAS clearance certificate from the Foreign and Commonwealth Office if they are applying for permission to study a course or research one of the disciplines listed in Appendix ATAS of the Immigration Rules.
The caseworker must check whether an ATAS clearance certificate is required by checking the CAH code on the applicant’s Confirmation of Acceptance for Studies (CAS).
If the applicant does not have an ATAS clearance certificate and the caseworker is satisfied that one is required, they must refuse the application.

[student-caseworker-guidance, Exemptions to the ATAS requirement]
The differentiation arrangements do not apply to ATAS. All applicants who are required to provide an ATAS certificate must apply for a clearance certificate online through the Foreign and Commonwealth Office (FCO) website. This site also contains information about the scheme and the list of designated subjects and useful documents to provide with ATAS applications.
The ATAS requirement does not apply to applicants who are listed as exempt in Appendix ATAS 3.1.

[student-caseworker-guidance, The ATAS clearance certificate]
An ATAS clearance certificate is issued for a specific course with a named provider and covers the length of that course from the course start date to the course end date given on the CAS, plus up to an additional 3 calendar months of study. The certificate remains valid as long as the provider and course details remain the same.
The applicant must provide a copy of their ATAS clearance certificate. It will have been sent to them as an email attachment. If a caseworker has any questions or concerns about the certificate, contact the atas@fco.gov.uk to check its validity.
If the student is continuing their course of study and the provider or course details change, or the student’s course end date is postponed for a period of more than 3 calendar months, the student must apply for a new ATAS clearance certificate within 28 calendar days of being notified of the change in course, regardless of when their permission expires.
A student must also apply for a new ATAS certificate if:
they want to start a new course that needs ATAS clearance
there are any changes to the course content or research proposal: if they are studying a PhD course, changes include changes other than minor changes to the areas of research or to the use of any new research technique
they are applying for an extension of permission to continue on their course
the end date of their course is postponed by more than 3 months
they move to another institution

[student-caseworker-guidance, Student: Academic Technology Approval Scheme (ATAS)]
This page tells caseworkers about ATAS and which courses of study require an ATAS clearance certificate.
ATAS was introduced to help stop the spread of knowledge and skills that could be used in the proliferation of weapons of mass destruction (WMD) and Advanced Conventional Military Technology and the means of delivery for each.
The ATAS is specifically designed to make sure that those applying for postgraduate study in certain sensitive subjects do not acquire knowledge that could potentially be used in WMD or Advanced Conventional Military Technology programmes.

[appendix-student, ST 8.3]
ST 8.3. If the course is an Association of Certified Chartered Accountants (ACCA) qualification or an ACCA Foundations in Accountancy qualification, the student sponsor must be an ACCA approved learning partner – student tuition at either Gold or Platinum level.
ST 8.4. If the Academic Technology Approval Scheme (ATAS) requirement in Appendix ATAS applies, the applicant must have a valid ATAS certificate and provide it with the application.

[student-visa-guide, When to apply]
When you can apply depends on whether you’re applying from inside or outside the UK.
The earliest you can apply for a visa is 6 months before you start your course.
The earliest you can apply is 3 months before your course starts.
You must apply before your current visa expires. Your new course must begin within 28 days of your current visa expiring.

[appendix-student, ST 4.1]
ST 4.1. An application for entry clearance must be made no more than 6 months before the start date of the course stated on the Confirmation of Acceptance for Studies.
ST 4.2. An application for permission to stay must be made no more than 3 months before the start date of the course on the Confirmation of Acceptance for Studies.
ST 4.3. An application for permission to stay must be for study on a course with a start date no more than 28 days after the expiry date of the applicant’s previous permission.

[student-visa-guide, When to apply]
The earliest you can apply is 3 months before your course starts.
You must apply before your current visa expires. Your new course must begin within 28 days of your current visa expiring.
For example, if your visa expires on 1 December, you must apply for a new visa before 1 December. Your new course must begin by 29 December.
You must also apply within 6 months of getting a Confirmation of Acceptance for Studies (CAS).
You can stay in the UK until you get your decision.
If you applied for an administrative review because your application was refused, you can stay in the UK until you get your review decision.

[student-visa-guide, When you can travel to the UK]
You can arrive before your course starts. This can be either:
up to 1 week before, if your course lasts 6 months or less
up to 1 month before, if your course lasts more than 6 months
You must not travel to the UK before the start date given on your visa, no matter when your course starts.

[student-visa-guide, How long it takes to get a decision]
You’ll usually get a decision on your visa within:
3 weeks, if you’re outside the UK
8 weeks, if you’re inside the UK
You may be able to pay to get a faster decision - you’ll be told if you can when you apply.

</details>

## q23 (multi)

**Question:** I'm starting a PhD in Manchester, and my wife and son are coming with me. How much extra money do I need to show for them, and can my wife work while we're here?

**Reference answer:** Because Manchester is outside London, you need £680 a month for each of them for up to 9 months, so £6,120 each and £12,240 in total, on top of the money for your own course and living costs, held for at least 28 consecutive days ending within 31 days of the application. Your wife can work in the UK: the exceptions only cover dependants whose student partner moves on to a new course shorter than 9 months or below degree level, which a PhD isn't.

**Agent's answer:**

> ### Financial Requirements for Your Dependants
> 
> Because you will be studying in Manchester, your course is located **outside of the Greater London area** [student-caseworker-guidance, Calculating funds needed for a dependant of a Student]. 
> 
> When bringing dependants, you must show extra maintenance funds for each family member for up to **9 months** [student-caseworker-guidance, Calculating funds needed for a dependant of a Student]. For studying outside London, the required rate for a dependant is **£680 per month** per person [student-caseworker-guidance, Calculating funds needed for a dependant of a Student]. 
> 
> For your wife and your son (two dependants), the total extra money you need to show is:
> * **Per month:** £680 × 2 = £1,360
> * **Total for 9 months:** £1,360 × 9 = **£12,360**
> 
> This amount is in addition to the funds you must show for yourself (£1,171 per month for up to 9 months, plus any outstanding course fees) [student-visa-guide, Money they need to support themselves, student-visa-guide, Money to support yourself (‘financial requirement’)], and this money generally must have been held for at least a 28-consecutive-day period [student-visa-guide, Money they need to support themselves].
> 
> ---
> 
> ### Can Your Wife Work?
> 
> **Yes.** As the dependant partner of a full-time PhD student at a higher education provider with a track record of compliance, your wife is permitted to work (including self-employment and voluntary work) in the UK [appendix-student, ST 31.1, appendix-student, ST 39.3]. 
> 
> Her work rights come with a few standard exceptions:
> * She cannot work as a professional sportsperson or sports coach [appendix-student, ST 39.3].
> * She cannot access public funds [appendix-student, ST 39.3].

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Calculating funds needed for a dependant of a Student]
The level of funds needed will depend on the following circumstances:
the length of the Student applicant’s permission
where in the UK the Student applicant will be studying
Dependants of Student applicants will need to evidence finance for the period they would be granted permission, if their application were to be successful, up to a maximum of 9 months. The start date of this period will be calculated from:
the date the applicant is intending to travel to the UK or one month before the Student applicant’s course start date, whichever is later, if they are applying for entry clearance
the date after their current period of permission expires, if they are already in the UK as the dependant of a Student (including Tier 4) and are applying for further permission to stay
the date of their application, if the applicant has leave under another PBS category and is now applying for leave as the dependant of a Student (including Tier 4)
When calculating the level of funds, dependants will need to demonstrate funds of:
£845 per month if the Student is studying in the Greater London area
£680 per month if the Student is studying outside of the Greater London area

[student-visa-guide, Money they need to support themselves]
Your partner and child must each have a certain amount of money available to them. This is in addition to the money you must have to support yourself.
How much money they need depends on where you will be studying. They must have either:
£845 a month (for up to 9 months) for courses in London
£680 a month (for up to 9 months) for courses outside London
If you’re applying at the same time as your partner or child (you’re applying together as a family), you’ll need to prove you have both money to pay for your course and to support yourself and additional money for each of them.
If your partner or child is applying at a different time to you (they’re applying separately) they only need to prove they have money to support themselves.
You (or your partner or child) must have this money for at least 28 consecutive days. The end date of the 28 day period must be within 31 days of the date they apply for their visa.
If you have a student loan or financial sponsorship, you’ll need to provide evidence of this from your loan or sponsorship company. If your loan does not cover your partner or child, you’ll need to prove you have money to support them instead.

[student-visa-guide, Money to support yourself (‘financial requirement’)]
You’ll need to show you have enough money to support yourself - unless you’ve been in the UK with a valid visa for at least 12 months on the date of your application.
How much money you need depends on where you will be studying. You’ll need either:
£1,529 per month (for up to 9 months) for courses in London
£1,171 per month (for up to 9 months) for courses outside London
If you’re boarding at a residential independent school, you’ll need to pay boarding fees instead. The amount you need to pay will be on your CAS.
London means the City of London and the 32 London boroughs.
You’ll need to prove you have extra money for each family member you bring with you.
You must have this money for at least 28 days in a row. The end date of the 28-day period must be within 31 days of the date you apply for your visa.
Example
If you submit your application on 1 January, you’d have to show that the funds were in your bank account for at least the 28-day period ending on 1 December.
If you have a student loan or financial sponsorship, you’ll need to provide evidence of this from your loan or sponsorship company.
Read the guidance on finances for student applications for more information about the money you need and how to prove it.

[appendix-student, ST 33.1]
ST 33.1. If the applicant is applying for permission to stay and has been living in the UK with permission for 12 months or longer on the date of application, they will meet the financial requirement and do not need to show funds.
ST 33.2. If the applicant is applying for entry clearance or permission to stay, where they have been in the UK less than 12 months, the applicant or their partner (who must be a Student or applying at the same time as a Student) must have the funds specified in the table below, for a total of 9 months, or for the period of permission applied for by the applicant, whichever is the shorter.
Place of Student’s study | Funds required by a dependent partner; Studying in London | £845 per month; Studying outside London | £680 per month
ST 33.3. The funds must be in addition to the funds required for the Student to meet the financial requirement, and the funds required to meet the financial requirement for any dependent child who is applying at the same time, or is already in the UK as a dependent child of the Student.
ST 33.4. Unless the applicant is relying on financial sponsorship from a Government or international scholarship agency that covers the living costs of the applicant and the Student, they must show that they have held the required level of funds for a 28-day period and as specified in Appendix Finance.
ST 33.5. Unless the applicant is applying at the same time as the Student and ST 22.1. applies, the applicant must show that they have the required funds as specified in Appendix Finance.

[appendix-student, ST 12.1]
ST 12.1. If the applicant is applying for permission to stay and has been living in the UK with permission for 12 months or more on the date of application, they will meet the financial requirement and do not need to show funds.
ST 12.2. If the applicant is applying for entry clearance or permission to stay and is applying as a Student Union Sabbatical Officer they will meet the financial requirement and do not need to show funds.
ST 12.3. If ST 12.2. does not apply, and the applicant is applying for entry clearance, or is applying for permission to stay and has been in the UK with permission for less than 12 months, the applicant must have the following funds:
(a) Studying in London
Type of Study | Funds required; Residential Independent School | Sufficient funds to pay outstanding fees (course fees and boarding fees) for one academic year; All other cases | Sufficient funds to pay any outstanding course fees as stated on the Confirmation of Acceptance for Studies, and £1529 for each month of the course (up to a maximum of 9 months)
(b) Studying outside London
Type of Study | Funds required; Residential Independent School | Sufficient funds to pay outstanding fees (course fees and boarding fees) for one academic year; All other cases | Sufficient funds to pay any outstanding course fees as stated on the Confirmation of Acceptance for Studies, and £1171 for each month of the course (up to a maximum of 9 months)
If the length of the applicant’s course includes a part of a month, the time period will be rounded up to the next full month.

[student-caseworker-guidance, When student dependants are permitted]
The rules for the Student course requirement that set out when a Student is permitted to have dependants can be found at Appendix Student ST 31.1 and 31.2.
The following people are eligible for permission as a dependant of a person who has been granted permission as a Student, or who will be applying at the same time:
spouses
civil partners
unmarried partners
dependent children of either a Student or their partner under the age of 18
The following Students are allowed to have dependants with them in the UK:
Students who have a scholarship or sponsorship from a government to study a full-time course lasting 6 months or longer
Students studying above degree level at a higher education provider with a track record of compliance on a course lasting 9 months or longer and, if the course start date is on or after 1 January 2024, the provider has confirmed the course is a PhD or other doctoral qualification, or a research-based higher degree
Students who have permission, or had permission within the last 3 months to study on a full-time course of 6 months or longer, and who are now applying for permission to study a full-time course of 6 months or longer where either: the partner or child applying has been the Student’s dependant in that period the child applying was born since the last grant of permission to the Student and they are applying at the same time as the Student or the dependant partner
Students whose child was born in a timeframe set out at Appendix Student ST 31.2 are allowed to have that child as a dependant with them in the UK

[appendix-student, ST 31.1]
ST 31.1. Unless they are a child who meets the requirements in ST 31.2., the applicant must be the partner or child of a person who is: (a) a Student who has received a scholarship or sponsorship from a Government for study in the UK and has, or is applying for, permission to study on a full-time course of 6 months or longer; or (b) a full-time Student who has, or is applying for, permission to study a postgraduate level course of 9 months or longer at a higher education provider with a track record of compliance and, if the course start date is on or after 1 January 2024, the provider has confirmed the course is a PhD or other doctoral qualification, or a research-based higher degree; or (c) DELETED (d) a Student who has, or had within the last 3 months before the date of application, permission to study on a full-time course of 6 months or longer, and is now applying for permission to study a full-time course of 6 months or longer where either: (i) the partner or child already has, or had within the last 3 months before the date of application, permission as a dependent partner or dependent child of the Student; or (ii) the child was born since the last grant of permission to the Student, where the Student and partner or child are applying at the same time.

[appendix-student, ST 39.1]
ST 39.1. A dependent partner will be granted permission which ends on the same date as the Student’s permission.
ST 39.2. A dependent child will be granted permission which ends on the same date as whichever of their parents’ permission ends first.
ST 39.3. The grant will be subject to all the following conditions: (a) no access to public funds; and (b) work (including self-employment and voluntary work) is permitted except: (i) where the dependant meets the requirement at ST 31.1.(d) and the Student has been granted less than 9 months’ permission, unless that is to continue a course of study where they had previously been granted at least 9 months’ permission; or (ii) where the dependant meets the requirement at ST 31.1.(d) and the Student is studying a course below degree level; or (iii) no employment as a professional sportsperson (including as a sports coach); and (c) study is permitted, subject to the ATAS condition in Appendix ATAS (if the study will commence when the partner or child is aged over 18). (d) DELETED

[student-caseworker-guidance, Student: Doctorate Extension Scheme (DES)]
The Doctorate Extension Scheme (DES) closed on 1 July 2021. The scheme has been replaced by the Graduate route, which opened on the same date.
The DES was open to Students with entry clearance or permission to stay as a Student or Tier 4 (General) student completing a course leading to the award of a PhD at a higher education provider (HEP) with a track record of compliance. Students who met the qualification criteria were granted further permission for 12 months from the course end date specified on the Confirmation of Acceptance for Studies (CAS) submitted with the DES application.
While waiting for a decision on the application for permission on the DES, and following a grant of permission, students were allowed to work full-time without restriction, except as a professional sportsperson (including as a sports coach).
Under the scheme:
students could sponsor dependents
students could switch into work routes
Students only needed to hold or apply for and Academic Technology Approval Scheme (ATAS) when applying for or holding permission on the DES when studying a relevant course for which the course end date had been postponed for more than 3 calendar months.

[student-caseworker-guidance, Conditions of leave]
This section tells caseworkers the conditions of leave for people granted permission as the dependant partner or child of a Student.
Partners or children of a Student:
are not allowed to access public funds
can take employment in the UK, apart from the restrictions explained below
study, subject to the ATAS condition of Appendix ATAS
For more information, see: Public funds

</details>

## q24 (multi)

**Question:** I've been in the UK for 13 months on my Student visa and want to go straight from my master's into a PhD. Can I apply from inside the UK, and do I need to show funds again?

**Reference answer:** Yes, you can extend your Student visa from inside the UK if you have an unconditional offer on a CAS and the PhD is at a higher academic level than your master's, which it is. Because you've been living in the UK with a visa for at least 12 months before applying, you don't need to prove you have money to support yourself.

**Agent's answer:**

> Yes, you can apply for your Student visa from inside the UK to move directly from your master’s to a PhD [student-visa-guide, Extend your visa, student-visa-guide, Eligibility]. 
> 
> ### Financial Requirement
> Because you have been living in the UK with a visa for at least 12 months on the date of your application, you meet the financial requirement automatically and **do not need to show funds** [appendix-student, ST 12.1].
> 
> ### Applying from Inside the UK & Academic Progression
> To apply from within the UK, you must meet the standard Student visa requirements, including having an unconditional offer from a licensed student sponsor demonstrated by a Confirmation of Acceptance for Studies (CAS) [student-visa-guide, Extend your visa]. 
> 
> Because you are applying from inside the UK after holding Student permission, you must also meet the academic progression requirement [student-caseworker-guidance, Student: academic progression]. Moving from a master’s degree to a PhD normally satisfies this requirement because a PhD is a course at a higher level than your previous course [appendix-student, ST 14.3].

<details><summary>Retrieved text</summary>

[appendix-student, ST 12.1]
ST 12.1. If the applicant is applying for permission to stay and has been living in the UK with permission for 12 months or more on the date of application, they will meet the financial requirement and do not need to show funds.
ST 12.2. If the applicant is applying for entry clearance or permission to stay and is applying as a Student Union Sabbatical Officer they will meet the financial requirement and do not need to show funds.
ST 12.3. If ST 12.2. does not apply, and the applicant is applying for entry clearance, or is applying for permission to stay and has been in the UK with permission for less than 12 months, the applicant must have the following funds:
(a) Studying in London
Type of Study | Funds required; Residential Independent School | Sufficient funds to pay outstanding fees (course fees and boarding fees) for one academic year; All other cases | Sufficient funds to pay any outstanding course fees as stated on the Confirmation of Acceptance for Studies, and £1529 for each month of the course (up to a maximum of 9 months)
(b) Studying outside London
Type of Study | Funds required; Residential Independent School | Sufficient funds to pay outstanding fees (course fees and boarding fees) for one academic year; All other cases | Sufficient funds to pay any outstanding course fees as stated on the Confirmation of Acceptance for Studies, and £1171 for each month of the course (up to a maximum of 9 months)
If the length of the applicant’s course includes a part of a month, the time period will be rounded up to the next full month.

[student-caseworker-guidance, Student: financial requirement]
This page tells caseworkers about the financial requirement that an applicant under the Student route must meet.
To score 10 points for meeting the financial requirement, the applicant must show that they have sufficient funds to pay outstanding course fees for the first academic year and can demonstrate funds to cover their living costs for up to 9 months.
Information on how evidence of funds can be demonstrated can be found in Appendix Finance and the level of funds which an applicant must demonstrate can be found in Appendix Student ST 12.
The following applicants will automatically meet the financial requirement and be awarded 10 points:
where they are applying for permission to stay in the UK, having been in the UK for at least 12 months with valid permission on the date of application
where they are applying for permission as a Student Union Sabbatical Officer
The applicant must show that they have held the required level of funds for a consecutive 28 day period, unless they are relying on a student loan, an award from an official financial sponsor, or where they are receiving some portion of the funds or other financial sponsorship from their student sponsor (as a bursary, for example). The 28 day period must end no more than 31 days before the application date.

[student-visa-guide, Eligibility]
To switch to a Student visa you must:
be in the UK
have an unconditional offer of a place on a course with a licensed student sponsor - shown by your Confirmation of Acceptance for Studies (CAS)
If you’ve been in the UK with a valid visa for less than 12 months, you’ll need to prove you have enough money to support yourself in the UK.
Your partner or children will need to apply separately to switch their visa. They can either apply at the same time as you, or at any time before their current visa expires.

[student-visa-guide, Extend your visa]
You may be able to extend your Student visa to stay longer and continue your course or study a new course. This includes if you currently have a Tier 4 (General) student visa.
To extend your visa you must:
be in the UK on a Student visa or a Tier 4 (General) student visa
have an unconditional offer of a place on a course with a licensed student sponsor - shown by your Confirmation of Acceptance for Studies (CAS)
show that your studies are at a higher academic level than your current course (called the ‘academic progress requirement’) - there are some exceptions
If you’ve been in the UK with a valid visa for less than 12 months, you’ll need to prove you have enough money to support yourself in the UK.
Your partner or children will need to apply separately to extend their visa. They can either apply at the same time as you, or at any time before their current visa expires.
You can also switch to a Graduate visa. This will allow you to stay in the UK after successfully completing your course for:
2 years if you apply on or before 31 December 2026
18 months if you apply on or after 1 January 2027
It will allow you to stay for 3 years if you completed a PhD or other doctoral qualification.

[student-visa-guide, When you do not need to prove you have money to support yourself]
You do not need to prove that you meet the financial requirement if either:
you’ve been living in the UK with a visa for at least 12 months prior to the date of your Student visa application
you’re applying as a student union sabbatical officer

[student-caseworker-guidance, Demonstrating academic progression]
All applicants who have previously been granted permission as a Student or a Tier 4 (General) Student, and are applying from within the UK to extend their stay need to have successfully completed their previous course unless:
they are progressing onto an integrated master’s or PhD programme at the higher level of that programme
an exception set out at Appendix Student ST 14.4 applies
Unless an exception at Appendix Student ST 14.4 applies applicants will also need to show that the course for which their CAS has been issued is at a higher level than their previous course. A new course at the same level is only permitted if:
the student sponsor is a higher education provider with a track record of compliance
the course of study is at degree level or above
the sponsor confirms that the new course is connected to the previous course or study on that course represents the applicants genuine career applications
the applicant has left an integrated master’s or PhD programme having successfully completed the course leading to the award of the lower level of the 2 qualifications it would be possible to be awarded by completing the course and is applying for a new course at the higher level (for example, a student who exits an integrated masters programme with a bachelors qualification then applies for a masters programme after exiting the course with the lower qualification)

[appendix-student, ST 14.3]
ST 14.3. An applicant will show academic progress if they are applying for any of the following: (a) to progress from a bachelor’s to master’s level course which is part of an integrated master’s course, where the applicant has been offered a place on a higher-level course by the student sponsor after an assessment of their academic ability; or (b) to progress from a master’s degree to a PhD which is part of an integrated master’s and PhD programme, where the applicant has been offered a place on a higher-level course by the student sponsor after an assessment of their academic ability; or (c) a course which is above the level of the previous course of study for which they were last granted permission unless: (i) the student sponsor is a higher education provider with a track record of compliance; and (ii) the course is at degree level or above; and (iii) the new course is at the same level as the previous course of study; and (iv) the student sponsor confirms that either: (a) the new course of study is related to the applicant’s previous course of study (meaning that it is either connected to the previous course, part of the same subject group, or involves deeper specialisation); or (b) the combination of the previous course of study and the new course of study support the applicant’s genuine career aspirations. (c) the applicant has left an integrated master’s or PhD programme having successfully completed the course leading to the award of the lower level qualification which formed a part of that programme.

[appendix-student, ST 14.1]
ST 14.1. An applicant who has, or previously had, permission as a Student and is applying for permission to stay as a Student must have successfully completed the course of study for which they were last granted permission as a Student or one of the following applies: (a) one of the exceptions in ST 14.4.; or (b) they are applying to progress to a higher level course as specified in ST 14.3.(a) or (b).; or (c) they have successfully completed the course of study for which they were last granted permission as a Student or the course of study they were allowed to change to without applying for further permission on the Student route and will now be taking a course at the same level as specified at ST 14.3(c); or (d) they have successfully completed the course of study with their sponsor where the change of course was allowed without applying for further permission on the Student route.
ST 14.2. An applicant who has, or previously had, permission on the Student route and is applying for permission to stay as a Student must show academic progress from the previous courses of study unless one of the exceptions in ST 14.4. applies.

[student-caseworker-guidance, Student: academic progression]
This section tells caseworkers about the academic progression requirement for Student applicants.
The academic progression requirement is in place to ensure that students are progressing academically if they wish to study a further course in the UK, and are not just seeking to extend their stay in the UK.
The requirement only applies to students who have previously been granted permission as a Student or a Tier 4 (General) Student and are applying for permission to stay. The rules for the academic progression requirement can be found at Appendix Student ST 14.1 to 14.5.

[student-caseworker-guidance, Study at the same level]
If an applicant has left an integrated master’s or PhD programme having successfully completed the course leading to the award of the lower level of the 2 qualifications it would be possible to be awarded by completing the course and is applying for a new course at the higher level (for example, a student who exits an integrated masters programme with a bachelors qualification then applies for a masters programme after exiting the course with the lower qualification) they are able to make an in-country application for permission to stay.
Before granting an application to study a course at the same level, the caseworker must consider whether a credibility interview should be conducted. If the caseworker is not satisfied by the sponsor’s justification, they must refer the case for a credibility interview. Following an interview with the applicant, if the caseworker is still not satisfied that the course represents academic progression, the application will be refused. Compliance action may then be taken against the sponsor by UKVI.
The following circumstances are examples of where an applicant can meet the exemption to the academic progression requirement:
an applicant has completed a Master’s degree in Modern Languages (RQF 7), and wishes to study a Master’s degree in Latin American Studies (RQF 7) - this is to deepen their specialist knowledge, or to better prepare for doctoral study, or to explore a future career in academia and research - in this case, there is a clear connection between the previous course and the new course

</details>

## q25 (multi)

**Question:** My master's is only 9 months long. When does my Student visa run out, and does a course that short still count for the Graduate visa?

**Reference answer:** Your Student visa runs until 2 months after your course end date, because that's the extra time given for courses of 6 months or longer but shorter than 12 months. A course that short can still count for the Graduate visa as long as you studied in the UK for its whole length, and you must be in the UK when you apply.

**Agent's answer:**

> ### When your Student visa runs out
> 
> For a course lasting 6 months or longer but shorter than 12 months (such as a 9-month master's), your Student visa will be granted for the duration of your course as specified on your CAS, plus **2 months** after your course end date [appendix-student, ST 25.1], [appendix-student, ST 25.2], [appendix-student, ST 25.3]. 
> 
> ### Does a 9-month course count for the Graduate visa?
> 
> **Yes.** A master's course shorter than 12 months still counts for the Graduate route, provided you meet all other requirements [graduate-visa-guide, How long you studied in the UK for], [appendix-graduate, GR 6.1]. 
> 
> For courses with a total length of 12 months or less, the rules require you to have held Student permission for the **full duration of the course** and to have studied in the UK for that full duration [graduate-visa-guide, How long you studied in the UK for], [appendix-graduate, GR 6.1].

<details><summary>Retrieved text</summary>

[appendix-student, ST 25.1]
ST 25.1. The grant of permission will be subject to the following conditions: (a) no access to public funds; and (b) no work, except as specified in ST 26; and (c) no study, except as specified in ST 27. (d) DELETED
ST 25.2. The applicant will be granted permission for the duration of the course as specified on the Confirmation of Acceptance for Studies plus the relevant periods specified in ST 25.3.
ST 25.3. The period of permission granted to an applicant before the start of the course who is applying for entry clearance will be either: (a) the relevant period before the course date which is set out in the table below, if entry clearance is granted 1 month or more before the start date of the course; or (b) 7 days before the intended date of travel, if entry clearance is granted less than 1 month before the start date of the course; or (c) with immediate effect, if entry clearance is granted less than 7 days before the intended date of travel and less than 1 month before the start date of the course.
The applicant will be granted a period of permission dependent on the type and length of course as in the table below:
Type of Course | Period granted before course start date | Period granted after course end date; A course of 12 months or longer | 1 Month | 4 Months; A course of 6 months or longer but shorter than 12 months | 1 Month | 2 Months; A pre-sessional course of less than 6 months | 1 Month | 1 Month; A course of less than 6 months in length which is not a pre- sessional course | 7 Days | 7 Days

[student-caseworker-guidance, Student: period to grant]
The period of permission to be granted to an applicant is dependent on the length and type of course to be studied. Information on the periods of permission to be granted after the end of the course can be found in Appendix Student ST 25.3.
In cases where an extension of permission to stay is granted after the course has finished, the caseworker must grant the additional period after the course stated in Appendix Student ST 25.3, from the date of decision. However, for courses where the caseworker would usually grant an additional period of 7 days, they must grant 17 days from the date of decision, if the course has finished.

[student-caseworker-guidance, Length of study that includes part of a month]
If the course includes part of a month, the course duration will be rounded up to the next full month. For example, if the applicant will be studying for a total of 6 months and 25 days, the caseworker must assess the course length as 7 months.

[appendix-student, ST 19.1]
ST 19.1. If the course is below degree level, the grant of permission must not lead to the applicant being granted more than two years’ permission as a Student to study courses below degree level from the age of 18 unless ST 19.2. applies.
ST 19.2. If the course is below degree level but is subject to a regulatory requirement by the Maritime and Coastguard Agency that the applicant must spend at least 12 months at sea as a part of that course, the grant of permission must not lead to the applicant being granted more than 3 years’ permission as a Student from the age of 18 to study courses below degree level.
ST 19.3. If the course is at degree level, the grant of permission must not lead to the applicant being granted more than five years’ permission as a Student from the age of 18 to study courses at degree level unless the course of study is one of those listed at ST 19.4.
ST 19.4. The five-year maximum period of study at degree level in ST 19.3. will not apply if the applicant has a Confirmation of Acceptance for Studies that has been assigned for a course of study in one of the following subjects: (a) architecture; or (b) medicine; or (c) dentistry; or (d) veterinary medicine and science; or (e) music at a music college that is a member of Conservatoires UK; or (f) law, where the applicant has completed a course at degree level or above and is applying for a course of study which is: (i) a law conversion course validated by the Solicitors Regulation Authority and the Bar Standards Board in England and Wales; or (ii) a Masters in Law (MLaw) in Northern Ireland; or (iii) an accelerated graduate LLB in Scotland.

[student-caseworker-guidance, Child Student: grant entry clearance]
If the applicant meets all of the requirements of Appendix Child Student of the Immigration Rules, and none of the general grounds for refusal apply, the caseworker must grant entry clearance.
The caseworker must grant entry clearance for the length of the course as stated on the Confirmation of Acceptance for Studies (CAS) up to a maximum of:
6 years (if the child is under 16 years of age)
3 years (if the child is 16 or 17 years of age)
The endorsement the caseworker must use is one of:
D: Child Student
D: Child Student (S)
Cat D endorsements (which must include the sponsor licence number in the sponsor details):
Age 16+: C Student SPX * Work Limit 10 hrs p/w term time. Age 16+ No Public Funds
Under 16: C Student. No Work SPX* No Public Funds

[graduate-visa-guide, How long you studied in the UK for]
You need to have studied in the UK for either:
at least 12 months, if your course’s total length is more than 12 months
the total length of your course, if its total length is shorter than 12 months
You must also be in the UK when you apply for a Graduate visa.

[appendix-graduate, GR 8.1]
GR 8.1. The applicant will be granted the period of permission as set out in the table below:
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made before 1 January 2027.; All other qualifications | 18 months if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made on or after 1 January 2027.

[appendix-graduate, GR 6.1]
GR 6.1. The applicant must have held permission as a Student, which was granted to study the relevant qualification in the UK, for a minimum period of time (the relevant period), as in the table below.
Total length of course | Relevant period of Student permission granted during which all study took place in the UK (apart from permitted study abroad programmes); 12 months or less | Full duration of course; Longer than 12 months | At least 12 months
GR 6.2. Where distance learning took place overseas between 24 January 2020 and 30 June 2022, this will not prevent the applicant meeting the requirement to spend the relevant period at GR 6.1 studying in the UK if either: (a) they began a course of 12 months or less prior to 21 June 2021 and entered the UK on or before 27 September 2021 with permission as a Student; or (b) they began a course of 12 months or less between 21 June 2021 and 30 June 2022 and entered the UK on or before 30 June 2022 with permission as a Student.
GR 6.3. Any period of distance learning that took place between 24 January 2020 and 30 June 2022 as part of a course of study lasting longer than 12 months whilst the applicant held permission as a Student, will not prevent the applicant from meeting the requirement to spend the relevant period at GR 6.1. studying in the UK.

[graduate-caseworker-guidance, Graduate: period to grant]
The period of permission to be granted to an applicant is dependent on the type of course studied and the date the application is made and is set out at Appendix Graduate GR.8.1 and in the following table
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made before 1 January 2027.; All other qualifications | 18 months - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made on or after 1 January 2027.
An applicant whose CAS was assigned for an integrated PhD but who successfully completes the lower postgraduate qualification must be granted 18 months from the date of decision where the Graduate application is made on or after 1 January 2027.

[graduate-caseworker-guidance, Study in the UK requirement]
An applicant who made their Student or Tier 4 (General) student application before their course started and started the course before permission was granted (as permitted in the Student route), will have their study time in the UK before permission being granted counted as well. This means that apart from the granted permission period, the period from course start date, as noted on their CAS, to the date of permission being granted, will also be counted. The same applies to applicants who were allowed to start their course before permission was granted due to Covid-19 concessions.
Applicants who studied a course lasting 12 months or less must have spent the full duration of the relevant period of permission course studying in the UK (or on permitted study abroad programs, where relevant) on either the Student route or former Tier 4 (General).
Applicants who complete a course that is longer than 12 months must have been granted at least 12 months of Student or Tier 4 (General) permission. All study that takes place during the 12 months of Student or Tier 4 (General) permission must have taken place in the UK, except for permitted study abroad programmes. For articulation programmes (2+1 and 2+2 programmes), a student must have successfully completed the final year of study in the UK, in other words, the final year is treated for the purpose of this application as the eligible course and the relevant requirement of study in the UK requirement applies depending on the length of such course. A student who undertakes the first year of an articulation programme in the UK and then completes the course overseas will not be eligible.

</details>

## q26 (multi)

**Question:** Can I do Deliveroo or Uber Eats shifts on a Student visa?

**Reference answer:** It depends on how the work is set up. On a Student visa you can't be self-employed, so you can't do delivery shifts as a self-employed or freelance rider. If the role is a job where the company employs you, it's allowed within your normal work limits: up to 20 hours a week during term time if you're studying at degree level at a university (10 hours if your course is below degree level), and full-time outside term time. The rules don't say whether delivery app riders count as employed or self-employed, so check your contract before you start. If it treats you as self-employed, you can't take the work.

**Agent's answer:**

> No, you cannot do Deliveroo or Uber Eats shifts on a Student visa [appendix-student, ST 26.5]. 
> 
> Students on a Student visa are strictly prohibited from being self-employed or engaging in business activity (such as working as a sole trader) [appendix-student, ST 26.5, student-caseworker-guidance, Engaging in business activity]. Delivery work for platforms like Deliveroo and Uber Eats is typically carried out on a self-employed basis, which breaches the work conditions of a Student visa.

<details><summary>Retrieved text</summary>

[student-caseworker-guidance, Student and Child Student: Prohibited work]
A Student must not be self-employed or engage in business activity unless the conditions in Appendix Student ST 26.8 apply. A Child Student is not permitted to be self-employed or engage in business activity.
A Student must not fill a full-time, permanent vacancy unless the conditions in Appendix Student ST 26.6 apply. A Child Student is not permitted to fill a permanent vacancy.
A Student or Child Student must not be employed as a professional sportsperson (including coach), whether paid or not and where one or more of the indicators of the definition provided under paragraph 6 of the Immigration Rules applies.
A Student or Child Student must not be employed as an entertainer.

[student-caseworker-guidance, Work conditions]
Students who are allowed to work must not:
be self-employed or engage in business activity, except where the Student has applied for permission on the Innovator Founder route; and that application is supported by an endorsement from an Innovator Founder endorsing body; and the application was made when the applicant had permission as a Student; and a decision has not been made on the application, or where the application has been refused, any Administrative Review against a refusal has not been finally determined
take employment as an entertainer or as a professional sportsperson, including a sports coach
fill a full-time permanent vacancy other than where they are filling a post as a Student Union Sabbatical Officer

[student-caseworker-guidance, Engaging in business activity]
A Student or Child Student will be considered to be engaging in business activity if they are working for a business in which they have a financial or other significant beneficial interest in a capacity other than as an employee.
Some examples which would be considered to be engaging in business activity are below. This is not an exhaustive list, but provides examples of activities which meet the definition of a Student or Child Student engaging in business activity:
setting up a business as a sole trader or under a partnership arrangement and that business is either trading or establishing a trading presence
being employed by a company in which they hold shares of 10% or more (including where the shares are held in a trust for them)
working for a company where they also hold a statutory role, such as a director

[appendix-student, ST 26.1]
ST26.1. The applicant will be granted permission with the following employment conditions:
Type of study | Employment conditions; Student following a full-time course of degree level or above study: • sponsored by a higher education provider with a track record of compliance; or • sponsored by an overseas higher education institution to undertake a short-term study abroad programme in the UK | 20 hours per week during term-time (full- time employment permitted outside of term-time); Student undertaking a full-time course below degree level study sponsored by a higher education provider with a track record of compliance | 10 hours per week during term-time (full- time employment permitted outside of term-time); All other study, including all part-time study | No employment permitted
ST 26.2. Students are permitted to undertake work related to a work placement, assessed as an integral part of the course, that meets the requirements at ST 17.1. to ST 17.3.
ST 26.3. Employment as an elected Student Union Sabbatical Officer or elected National Union of Students (NUS) position is permitted for up to 2 years if the Confirmation of Acceptance for Studies was assigned for this purpose.
ST 26.4. DELETED.
ST 26.5. A Student is not allowed to do any of the following: (a) be self-employed or engage in business activity unless ST 26.8 applies; or (b) work as a professional sportsperson (including as a sports coach); or (c) work as an entertainer; or (d) work in a position which would fill a permanent full-time vacancy unless ST 26.6. applies.

[student-visa-guide, Your partner and children]
You may be able to bring your partner and children (‘dependants’).
You can:
study on a further or higher education course
work as a student union sabbatical officer
do a traineeship through the Erasmus+ programme with a participating licensed student sponsor
study through the Erasmus+ programme at a participating academy or local authority-funded school (also known as a maintained school)
You may be able to work - how much depends on what you’re studying and whether you’re working in or out of term-time.
You cannot:
claim public funds (benefits) and pensions
work in certain jobs, for example as a professional sportsperson or sports coach
be self-employed
If your application is successful, you’ll be told what you can and cannot do on a Student visa.

</details>

## q27 (multi)

**Question:** I'm finishing my PhD, and my wife is here as my dependant. How long will my Graduate visa last, and can she stay on it with me?

**Reference answer:** With a PhD, your Graduate visa lasts 3 years from the day it's approved. Your wife can apply to stay as your dependant on it because she joined you as a dependant on your current Student visa, and her visa would end on the same date as yours.

**Agent's answer:**

> Your Graduate visa will last for **3 years** because you have completed a PhD or other doctoral qualification [graduate-visa-guide, How long you can stay].
> 
> Yes, your wife can stay on the Graduate route as your dependant [appendix-graduate, GR 11.1], provided she meets the requirements [appendix-graduate, GR 9.2]. Specifically, she must already be in the UK as your dependant partner on your Student or Tier 4 visa, you must be able to prove your relationship, and she must apply at the same time as you (or while you have your Graduate permission) [graduate-visa-guide, Your partner, appendix-graduate, GR 9.2, appendix-graduate, GR 11.1]. Her visa will end on the same date as yours [appendix-graduate, GR 16.1].

<details><summary>Retrieved text</summary>

[graduate-visa-guide, How long you can stay]
A Graduate visa lasts for:
2 years if you apply on or before 31 December 2026
18 months if you apply on or after 1 January 2027
If you have a PhD or other doctoral qualification, it will last for 3 years.
Your visa will start from the day your application is approved.

[appendix-graduate, GR 8.1]
GR 8.1. The applicant will be granted the period of permission as set out in the table below:
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made before 1 January 2027.; All other qualifications | 18 months if the applicant has successfully completed a course at UK bachelor’s degree or master’s degree level, or another relevant qualification that meets the requirement of ST8.1/2/3 of the Rules, and the application is made on or after 1 January 2027.

[graduate-caseworker-guidance, Graduate: period to grant]
The period of permission to be granted to an applicant is dependent on the type of course studied and the date the application is made and is set out at Appendix Graduate GR.8.1 and in the following table
Type of Qualification | Period granted from date of decision; PhD or other doctoral qualification | 3 years; All other qualifications | 2 years - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made before 1 January 2027.; All other qualifications | 18 months - if the applicant has successfully completed an eligible course at UK bachelor’s degree or master’s degree level, or another relevant qualification and the application is made on or after 1 January 2027.
An applicant whose CAS was assigned for an integrated PhD but who successfully completes the lower postgraduate qualification must be granted 18 months from the date of decision where the Graduate application is made on or after 1 January 2027.

[student-visa-guide, Staying longer in the UK]
You may be able to:
extend your visa if you’re eligible, for example to continue your studies in the UK
switch to a Student visa from another visa if you’re already in the UK
switch to a Graduate visa
A Graduate visa will allow you to stay in the UK after successfully completing your course for:
2 years if you apply on or before 31 December 2026
18 months if you apply on or after 1 January 2027
It will allow you to stay for 3 years if you completed a PhD or other doctoral qualification.

[graduate-visa-guide, Overview]
A Graduate visa gives you permission to stay in the UK for at least 18 months after successfully completing an eligible course in the UK.
You must be in the UK when you apply.
You can apply for a Graduate visa if all of the following are true:
you’re in the UK
your current visa is a Student visa or Tier 4 (General) student visa
you studied a UK bachelor’s degree, postgraduate degree or other eligible course for a minimum period of time with your Student visa or Tier 4 (General) student visa
your education provider (such as your university or college) has told the Home Office you’ve successfully completed your course
You can ask your education provider if you’re not sure whether they’ve told the Home Office you’ve successfully completed your course.
Check if your course is eligible and how long you need to have studied in the UK.
If you’re not eligible for a Graduate visa, you may be eligible for another type of visa to stay in the UK.

[appendix-graduate, GR 9.1]
GR 9.1. A person applying for permission to stay as a partner or child of a Graduate must apply on the specified form on the gov.uk website as follows:
Either (as applicable): Dependant partner Dependant child
GR 9.2. An application for permission to stay as a partner or child of a Graduate must meet all the following requirements: (a) any fee and Immigration Health Charge must have been paid; and (b) the applicant must have provided biometrics when required; and (c) the applicant must have provided a passport or other document which satisfactorily establishes their identity and nationality; and (d) the applicant must be applying as partner or child of a person who: (i) has made a valid application for permission to stay on the Graduate route that has not been decided; or (ii) has permission to stay on the Graduate route.
GR 9.3. If the applicant has in the 12 months before the date of application completed a course of studies in the UK for which they have been awarded a scholarship or sponsorship by a Government or international scholarship agency covering both fees and living costs for study in the UK, they must provide written consent to the application from that Government or agency.
GR 9.4. The applicant must be in the UK on the date of application.

[graduate-visa-guide, Your partner]
Your partner needs to have been a dependant on your Student visa or Tier 4 (General) student visa to apply. You’ll also need to show that they’re still your partner.
You must be able to prove one of the following:
you’re in a civil partnership or marriage that’s recognised in the UK
you’ve been living together in a relationship for at least 2 years when you apply
you’ve been in a relationship for at least 2 years when you apply but you cannot live together, for example because you’re working or studying in different places, or it’s not accepted in your culture
If you’re not living together, you’ll need to prove that you have an ongoing commitment to each other, for example by providing evidence that you:
communicate regularly with each other
support each other financially
care for any children you have together
spend time together as a couple, for example on holiday or at events

[appendix-graduate, GR 11.1]
GR 11.1. The applicant must be the partner of a Person (P) where one of the following applies: (a) P has permission to stay on the Graduate route; or (b) P is, at the same time, applying for (and is granted) permission to stay on the Graduate route.
GR 11.2. The requirements of Appendix Relationship with Partner must be met.
GR 11.3. DELETED

[graduate-caseworker-guidance, Conditions of leave]
This section tells caseworkers the conditions of leave for people granted permission as the dependant partner or child of a Graduate.
Partners or children of a Graduate:
are not allowed to access public funds
must register with the police (if they are required to do so by part 10 of the Immigration Rules)
can work in the UK, subject to the restrictions explained below
can study, subject to the ATAS condition of Appendix ATAS

[appendix-graduate, GR 16.1]
GR 16.1. A dependent partner will be granted permission which ends on the same date as the Graduate partner’s permission.
GR 16.2. A dependent child will be granted permission which ends on the same date as whichever of their parents’ permission ends first.

</details>

## q28 (multi)

**Question:** My government scholarship paid my fees and living costs for my master's. Do I need my government's permission to apply for the Graduate visa, and how much will the application cost?

**Reference answer:** Yes: if your government paid both your course fees and living costs in the last 12 months, you need a letter from it approving your application. The application fee is £937 plus a healthcare surcharge of usually £1,035 for each year, so it depends on when you apply: on or before 31 December 2026 the visa lasts 2 years (around £2,070 surcharge, £3,007 in total), and on or after 1 January 2027 it lasts 18 months (around £1,552.50 surcharge, £2,489.50 in total).

**Agent's answer:**

> **Do you need your government's permission?**
> Yes. Because you were awarded a scholarship or sponsorship by a government or international scholarship agency covering both your course fees and living costs within the 12 months before your application, it is a validation requirement that you must provide written consent to the application from that government or agency [appendix-graduate, GR 1.5]. If you do not provide this written consent/letter approving your application, your application may be rejected as invalid [appendix-graduate, GR 1.6, graduate-visa-guide, Other documents you might need]. 
> 
> **How much will the application cost?**
> When you apply for a Graduate visa, you must pay:
> * The **£937** application fee [graduate-visa-guide, How much it costs]
> * The Immigration Health Charge (healthcare surcharge), which is usually £1,035 for each year you are in the UK [graduate-visa-guide, How much it costs]. For a standard 2-year Graduate visa, the total healthcare surcharge is **£2,070** [graduate-visa-guide, Healthcare surcharge].

<details><summary>Retrieved text</summary>

[graduate-caseworker-guidance, Validity requirements]
If an applicant has, in the 12 months before the date of application, been awarded a scholarship or sponsorship by a Government or international scholarship agency, covering both course fees and living costs for study in the UK (for example a Chevening or Marshall scholarship), it is a validation requirement that they must provide written consent from the financial sponsor to the application for permission to stay in the UK as a Graduate.

[graduate-caseworker-guidance, Validity]
The caseworker must check the applicant has, or has last had, permission as a student’s dependant partner or dependant child of either a Student or that Student’s dependant partner, or is a child who was born in the UK during a parent’s period of Graduate permission, and that the relevant Student or Graduate is also applying for, or has been granted, permission in the Graduate route. For the purpose of this requirement, this means an applicant must currently hold valid permission as a dependant (partner or child) on either the Student route or the Tier 4 (General) route, or is a child who was born in the UK during a parent’s period of Graduate permission, or must have held valid permission on the Student or Tier 4 (General) routes which expired within the timeframes allowed in paragraph Part Suitability: Exceptions for Overstayers.
The caseworker must check relevant caseworking databases to find out whether the dependant applicants meet this requirement.
If an applicant has, in the 12 months before the date of application, been awarded a scholarship or sponsorship by a Government or international sponsorship agency, covering both course fees and living costs for study in the UK (for example a Chevening or Marshall scholarship), it is a validation requirement that they must provide written consent from the financial sponsor to a further application for permission to stay in the UK as a Graduate dependant.
Applications which do not meet the requirements in Appendix Graduate GR.9 should be rejected as invalid.

[graduate-visa-guide, Other documents you might need]
Depending on your circumstances, you might be asked to provide:
proof of your relationship with your partner or children if they’re applying with you
a letter from your scholarship or sponsorship provider approving your application, if they paid for both your course fees and living costs in the last 12 months
If your documents are not in English or Welsh you’ll also need to provide a certified translation.

[appendix-graduate, GR 1.1]
GR 1.1. A person applying for permission to stay as a Graduate must apply online on the gov.uk website on the specified form “Graduate”.
GR 1.2. An application for permission as a Graduate must meet all the following requirements: (a) any fee and Immigration Health Charge must have been paid; and (b) the applicant must have provided biometrics when required; and (c) the applicant must have provided a passport or other document which satisfactorily establishes their identity and nationality; and (d) the applicant must be in the UK.
GR 1.3. The applicant must have, or have last had, permission as a Student.
GR 1.4. The applicant must not have been previously granted permission under the Doctorate Extension Scheme or as a Graduate.
GR 1.5. If the applicant has in the 12 months before the date of application completed a course of studies in the UK for which they have been awarded a scholarship or sponsorship by a Government or international scholarship agency covering both fees and living costs for study in the UK, they must provide written consent to the application from that Government or agency.
GR 1.6. An application which does not meet all the validity requirements for a Graduate may be rejected as invalid and not considered.

[graduate-caseworker-guidance, Sponsor notification]
The Student Sponsor must have notified the Home Office, by the date of application, that the applicant has successfully completed the course of study. Sponsors will normally do this by way of bulk upload. If sponsors are unable to make the notification via bulk upload, they must use the agreed exceptions process.
If a notification has not been received from the Student Sponsor, but the CAS shows that the applicant had been studying a qualifying qualification, the caseworker must not refuse the application if it would otherwise be granted. Instead, the caseworker must contact the Sponsor asking for confirmation that the student has successfully completed the course of study.

[graduate-visa-guide, How much it costs]
When you apply for a Graduate visa, you’ll need to:
pay the £937 application fee
pay the healthcare surcharge - this is usually £1,035 for each year you’ll be in the UK
You’ll be told how much you need to pay when you apply.

[graduate-visa-guide, Healthcare surcharge]
If you’re eligible for a Graduate visa for:
18 months - it will cost £1,552.50
2 years - it will cost £2,070
3 years - it will cost £3,105
If you get a job in public sector healthcare after you have paid the healthcare surcharge, you may be able to get a refund.

[graduate-visa-guide, Getting a decision]
Once you’ve applied online, proved your identity and provided your documents, you’ll usually get a decision on your visa within 8 weeks.
You can stay in the UK while you wait for a decision.
When you apply for a Graduate visa, you’ll need to:
pay the £937 application fee
pay the healthcare surcharge - this is usually £1,035 for each year you’ll be in the UK
Check how much it will cost.

[graduate-visa-guide, If you work in public sector healthcare]
If you’re a doctor or nurse, or you work in health or adult social care, check if you’re eligible to apply for the Health and Care Worker visa instead. It’s cheaper to apply for and you do not need to pay the annual immigration health surcharge.
If you get a job in public sector healthcare after you have paid the healthcare surcharge, you may be able to get a refund.

[student-visa-guide, Fees]
It costs:
£558 to apply for a Student visa from outside the UK
£558 to extend or switch to a Student visa from inside the UK
You must pay the visa fee for each person that joins you.
You’ll also have to pay the healthcare surcharge as part of your application.
How much you pay depends on how long your visa lasts.

</details>

## q29 (single)

**Question:** I already had a Graduate visa after my bachelor's here. If I come back for a master's, can I get another one afterwards?

**Reference answer:** No. You can't get a Graduate visa if you've been granted one before, or permission under the Doctorate Extension Scheme, so you can't get a second one after your master's.

**Agent's answer:**

> No, you cannot get another Graduate visa. 
> 
> Under the Immigration Rules, an applicant must not have been previously granted permission on the Graduate route or under the Doctorate Extension Scheme [appendix-graduate, GR 1.4]. If you have previously held a Graduate visa, any subsequent application under this route must be rejected as invalid [graduate-caseworker-guidance, Validity requirements].

<details><summary>Retrieved text</summary>

[graduate-caseworker-guidance, Validity requirements]
The caseworker must check the applicant has, or has last had, permission as a student. For the purpose of this requirement, this means an applicant must either:
currently hold valid permission on either the Student route or the Tier 4 (General) route
have held valid permission on the Student or Tier 4 (General) routes which expired but either: one of the paragraph Part Suitability: Exceptions for Overstayers applies the applicant has been given a period of exceptional assurance and has not overstayed that period - in either case the period of overstaying will be disregarded when considering their application
The caseworker must check the applicant’s immigration history to make sure that the applicant has not previously been granted permission under the Doctorate Extension Scheme (DES) or held permission on the Graduate route. If they have previously been granted permission under the DES or on the Graduate route, then the application must be rejected as invalid.
If a student has previously been granted permission on the Tier 1 (Post-study work) route, International Graduate Scheme (IGS) or the Future Talent Working in Scotland Scheme, this will not prevent them from meeting the validation requirements of the Graduate route. If a student has previously been granted permission on one of these routes, the student will need to successfully complete a new eligible qualification at a Higher Education Provider with a track record of compliance and hold valid permission as a student once the route is introduced, they cannot rely on a previous qualification obtained or previous leave as a Student or under Tier 4 to access the route.

[graduate-visa-guide, The course you studied]
To be eligible for a Graduate visa, you need to have successfully completed the course you took with your current Student visa or Tier 4 (General) student visa.
Whether you can apply will also depend on:
the education provider for your course, for example your university or college
the kind of course you took
how long you studied in the UK for
If your education provider allowed you to change course without applying for a new Student visa or Tier 4 (General) student visa, you only need to have completed the course you changed to.

[appendix-graduate, GR 1.1]
GR 1.1. A person applying for permission to stay as a Graduate must apply online on the gov.uk website on the specified form “Graduate”.
GR 1.2. An application for permission as a Graduate must meet all the following requirements: (a) any fee and Immigration Health Charge must have been paid; and (b) the applicant must have provided biometrics when required; and (c) the applicant must have provided a passport or other document which satisfactorily establishes their identity and nationality; and (d) the applicant must be in the UK.
GR 1.3. The applicant must have, or have last had, permission as a Student.
GR 1.4. The applicant must not have been previously granted permission under the Doctorate Extension Scheme or as a Graduate.
GR 1.5. If the applicant has in the 12 months before the date of application completed a course of studies in the UK for which they have been awarded a scholarship or sponsorship by a Government or international scholarship agency covering both fees and living costs for study in the UK, they must provide written consent to the application from that Government or agency.
GR 1.6. An application which does not meet all the validity requirements for a Graduate may be rejected as invalid and not considered.

[appendix-graduate, GR 4.1]
GR 4.1. The applicant must have last been sponsored by a Student sponsor which is a higher education provider with a track record of compliance on the date of application.
GR 4.2. The applicant must have successfully completed the course of study which was undertaken during their last grant of permission to study on the Student route (where the applicant was allowed to change their course of study without applying for further permission as a Student, this requirement only applies to the course to which they changed).
GR 4.3. The student sponsor must have notified the Home Office, by the date of application, that the applicant has successfully completed the course of study in GR 4.2.

[appendix-graduate, GR 5.1]
GR 5.1. The applicant will meet the qualification requirement if they have successfully completed a course of study for which they have been or will be awarded a UK bachelor’s degree, a UK postgraduate degree, or successfully completed a relevant qualification listed in GR 5.2.
GR 5.2 A relevant qualification is one of the following: (a) a law conversion course validated by the Solicitors Regulation Authority in England and Wales; or (b) the Legal Practice Course in England and Wales, the Solicitors Course in Northern Ireland, or a Diploma in Professional Legal Practice in Scotland; or (c) the Bar Practice Course in England and Wales, or the Bar Course in Northern Ireland; or (d) DELETED (e) a Postgraduate Certificate in Education (PGCE) or Postgraduate Diploma in Education (PGDE); or (f) a professional course requiring study at UK bachelor’s degree level or above in a profession with reserved activities that is regulated by UK law or UK public authority.
GR 5.3. If the name of the applicant’s course of study was changed by the Student sponsor, but the course content remained the same, or if an integral and assessed work placement or permitted study abroad programme was added, this will not prevent the applicant being able to meet the qualification requirement.
GR 5.4 The qualification must have been gained during the last grant of permission to study as a Student, or in the period of permission immediately before the applicant’s last grant of permission, if the last grant of permission was to undertake a role as a Student Union Sabbatical Officer.

</details>

## q30 (unanswerable)

**Question:** I saw reports that students who applied between 2023 and 2026 might get part of their visa fee back. Is that real, and do I need to claim it?

**Reference answer:** I can't find this in the documents I have. To check, look for an official Home Office announcement on GOV.UK or ask your university's international student advice team.

**Agent's answer:**

> I can't find this in the documents I have. Please check GOV.UK or speak with your university's international student advisers.

<details><summary>Retrieved text</summary>

[graduate-visa-guide, Getting a decision]
Once you’ve applied online, proved your identity and provided your documents, you’ll usually get a decision on your visa within 8 weeks.
You can stay in the UK while you wait for a decision.
When you apply for a Graduate visa, you’ll need to:
pay the £937 application fee
pay the healthcare surcharge - this is usually £1,035 for each year you’ll be in the UK
Check how much it will cost.

[graduate-visa-guide, Healthcare surcharge]
If you’re eligible for a Graduate visa for:
18 months - it will cost £1,552.50
2 years - it will cost £2,070
3 years - it will cost £3,105
If you get a job in public sector healthcare after you have paid the healthcare surcharge, you may be able to get a refund.

[student-caseworker-guidance, Student: Visa Brake]
Afghanistan, Cameroon, Myanmar and Sudan will be subject to a visa brake from 00:01 GMT 26 March 2026. You must refuse any out-of-country Student entry clearance applications submitted on or after this date where the main applicant is a national or citizen of one of these countries, in accordance with paragraph ST 3.3. You should assess an applicant’s suitability in full, but no further consideration of the applicant’s wider eligibility should be undertaken.
The visa brake only affects out-of-country applications where the main applicant has made their application using a passport or travel document which confirms that they are a national of one of the affected countries. Any applications made by dual nationals in a different nationality should be considered as normal in line with that nationality.

[graduate-visa-guide, If you work in public sector healthcare]
If you’re a doctor or nurse, or you work in health or adult social care, check if you’re eligible to apply for the Health and Care Worker visa instead. It’s cheaper to apply for and you do not need to pay the annual immigration health surcharge.
If you get a job in public sector healthcare after you have paid the healthcare surcharge, you may be able to get a refund.

[graduate-visa-guide, How much it costs]
When you apply for a Graduate visa, you’ll need to:
pay the £937 application fee
pay the healthcare surcharge - this is usually £1,035 for each year you’ll be in the UK
You’ll be told how much you need to pay when you apply.

</details>
