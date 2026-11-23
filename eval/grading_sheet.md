# Grading sheet

Grade each answer in `eval/human_labels.csv` (columns `id,correct,supported,notes`, a note for every 0).
Use the same definitions as the judge's rubric (`JUDGE_RUBRIC` in evaluate.py).
Do **not** open `eval/judge_verdicts.csv` or `eval/results.csv` before you finish.

## q01 (single)

**Question:** How many hours of annual leave do I earn per pay period if I have worked for the federal government for 5 years?

**Reference answer:** 6 hours per pay period (the rate for 3 to 15 years of federal service).

**Agent's answer:**

> If you have worked for the federal government for 5 years, you earn 6 hours of annual leave per pay period [Leave types › Types of leave › Annual leave].
> 
> *Note: This handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Leave types › Types of leave › Annual leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.77

You may use annual leave for any reason. Annual leave accrues based on how long you’ve worked for the federal government:

- Fewer than 3 years: 4 hours per pay period
- Between 3 and 15 years: 6 hours per pay period
- 15+ years: 8 hours per pay period

Your leave increases on the first full pay period following your work anniversary. You can refer to either HR Links or the bottom of your paystub for your leave balances.

You can carry over a maximum of 240 annual leave hours, from one leave year to the next. If you’ve transferred to TTS from another federal agency, your accrued annual leave will transfer with you.

========

[2] Leave types
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.71

Current employees can use this leave comparison chart.

Before you take leave, check out of office expectations.

========

[3] Advanced sick leave
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.65

You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

For example: You have one year left on your term, which equals to 26 pay periods. You earn 4 sick leave hours per pay period. You will earn 104 more sick leave hours (26 pay periods x 4 hours per pay period). Therefore, you can request up to 104 advanced sick leave hours.

========

[4] Benefits › Leave
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.65

Please use HR Links to request sick
leave and annual leave. For any leave-related questions, please contact
cpc.benefits-retirement@gsa.gov.

For more information on Leave, including sick, funeral, unpaid, parental,
advanced, and religious, please reference the Leave page.

========

[5] Family Medical Leave Act (FMLA) › How FMLA works
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.63

You can use 12 unpaid weeks of FMLA every 52 weeks. The 12 weeks are rolling, and are refilled a year to the day you first went on FMLA status.

Each time you use FMLA, it counts toward the 12 week/480 hour allotment.

- For example: you went on FMLA for 4 weeks in March 2022 to care for a seriously ill family member, and you used your accrued Sick Leave in order to be paid during those 4 weeks. You will only have 8 weeks of FMLA available until March 2023\.
```
</details>

## q02 (single)

**Question:** What is the maximum amount of annual leave I can carry over into the next leave year?

**Reference answer:** 240 hours.

**Agent's answer:**

> You can carry over a maximum of 240 hours of annual leave from one leave year to the next [Leave types › Types of leave › Annual leave] [Leave types › Types of leave › Annual leave › Use or Lose].
> 
> The handbook is a snapshot from June 2026 and you should confirm with HR.

<details><summary>Retrieved passages</summary>

```text
[1] Leave types › Types of leave › Annual leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.74

You may use annual leave for any reason. Annual leave accrues based on how long you’ve worked for the federal government:

- Fewer than 3 years: 4 hours per pay period
- Between 3 and 15 years: 6 hours per pay period
- 15+ years: 8 hours per pay period

Your leave increases on the first full pay period following your work anniversary. You can refer to either HR Links or the bottom of your paystub for your leave balances.

You can carry over a maximum of 240 annual leave hours, from one leave year to the next. If you’ve transferred to TTS from another federal agency, your accrued annual leave will transfer with you.

========

[2] Leave types › Types of leave › Annual leave › Use or Lose
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.73

Use or Lose is the number of annual leave hours you would forfeit at the end of the leave year, if you do not use any of your annual leave hours between now and then. As noted above, there is a 240 hour limit on the number of hours you can carry over from one leave year to the next. Use or Lose only applies to annual leave.

For example: You look in HRLinks and see "182 Hours (96 Hours Use or Lose)." Today, January 25th, 2022, you have 182 hours of annual leave available. If you continued to accrue annual leave for the rest of the year, and you did not use any of those hours, you would forfeit 96 hours of annual leave at the end of the year. You would be 96 hours over the 240 cap.

182 current hours \+ 154 more hours accrued throughout the year \= 336 hours.

336 hours \- 240 hour cap \= 96 Use or Lose hours that would be forfeited.

========

[3] Advanced sick leave
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.66

You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

For example: You have one year left on your term, which equals to 26 pay periods. You earn 4 sick leave hours per pay period. You will earn 104 more sick leave hours (26 pay periods x 4 hours per pay period). Therefore, you can request up to 104 advanced sick leave hours.

========

[4] Compensation for working extra hours › Overtime and Compensatory (Comp) time › Compensatory (Comp) time, depending on your salary level
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.65

Comp time is when you receive hours of leave instead of overtime pay. To determine the maximum number of comp time hours that you can accrue per pay period, please use the Bi-weekly Comp Time Cap Calculator. If you make the maximum salary ($191,900 in 2024), you cannot receive comp time.

You should use your accrued comp time before using Annual Leave. However, if the end of the leave year is approaching and you're in danger of losing Annual Leave because of “Use or Lose, your supervisor can prioritize your Annual Leave requests over comp time.”

Comp time expires one year (26 pay periods) after it's earned. When you reach that expiration date, you forfeit the relevant leave. If you leave GSA, your comp time will be paid out.

Refer to OPM’s Comp Time Fact Sheet for more detail.

========

[5] Going out of office › Your overall responsibilities
source: travel-and-leave/going-out-of-office | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/going-out-of-office.md | similarity: 0.65

You must report to work or have an approved leave request in HR Links, every scheduled work day. You are also responsible for submitting your timesheet at the end of every pay period.

You should submit leave requests at least three business days in advance, and make timely edits if your plans change.

For unplanned leave \- such as a sudden illness or a family emergency \- do what you can to contact your supervisor, and they can help manage the rest on your behalf.

Some types of leave require supporting documentation: it is your responsibility to submit all necessary documents and check that you’ve received approval.
```
</details>

## q03 (single)

**Question:** If I get called for jury duty, does it come out of my annual leave?

**Reference answer:** No. It is recorded as Court Leave, does not count against any other leave balance, and lasts as long as you serve on the jury.

**Agent's answer:**

> No, jury duty does not come out of your annual leave. When you are called to jury duty, your absence is marked as Court Leave and does not count against any of your other leave balances [Leave types › Types of leave › Court leave (jury duty)].
> 
> To report Court Leave, follow the typical steps for entering a leave request in HR Links [Leave types › Types of leave › Court leave (jury duty)].
> 
> *This handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Leave types › Types of leave › Court leave (jury duty)
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.74

When you are called to jury duty, your absence is marked as Court Leave and does not count against any of your other leave balances.

You would also request court leave if you are asked to serve as a witness in a judicial proceeding to which the Federal government, a state government, or a local government is a party.

You can receive Court Leave for however long you serve on a jury. To report Court Leave, follow the typical steps for Entering a leave request in HR Links.

OPM Fact Sheet:

- Court Leave

========

[2] Leave types › Reasons someone can take leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.68

TTS has leave types for the following scenarios. Talk with your Workforce Relations HR Specialist about ways to combine leave types.

For **general uses and vacation**, you can use:

- Annual Leave
- Award Leave

For **sick or medical reasons**, you can use:

- Sick Leave

Other medical reasons:

- When getting a COVID vaccine or recovering from vaccine side effects, you can use Administrative Leave
- Blood, bone marrow, organ donation, you can use Administrative Leave
- Disabled veteran leave (DVL) for veterans with a service-related disability

For **bereavement**, you can use:

- Sick Leave for funerals
- Funeral Leave for military relatives
- Parental Bereavement Leave after losing a child

For **birth, adoption or placement of a new child**, you can use paid parental leave. You can also use annual and sick leave for parental leave reasons.

For **religious observances**, you can request an adjustment to your work schedule for religious observances, instead of taking leave.

To **vote**, register to vote, participate in early voting, or volunteering as a poll worker, you generally must do so on your own time (i.e., either before or after work), or during work hours by using approved annual leave, compensatory time off, comp time for travel, or credit hours (for employees on flexible schedules).

For **jury duty** and other court-related leave, use Court Leave.

If you can’t work or stay in your home for weather or safety reasons, you can request Administrative Leave.

When going on **active duty**, active duty training, and inactive duty training in the National Guard or as a Reservist, you can use Military Leave.

You can work with your supervisor to use up to 4 hours of work time pursuing options from the Employee Assistance Program (EAP).

If you are running out of leave hours, you can request:

========

[3] Going out of office › Your overall responsibilities
source: travel-and-leave/going-out-of-office | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/going-out-of-office.md | similarity: 0.64

You must report to work or have an approved leave request in HR Links, every scheduled work day. You are also responsible for submitting your timesheet at the end of every pay period.

You should submit leave requests at least three business days in advance, and make timely edits if your plans change.

For unplanned leave \- such as a sudden illness or a family emergency \- do what you can to contact your supervisor, and they can help manage the rest on your behalf.

Some types of leave require supporting documentation: it is your responsibility to submit all necessary documents and check that you’ve received approval.

========

[4] Veteran & service member resources › Leave
source: general-information-and-resources/employee-resources-policies/veterans-service-members | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/veterans-service-members.md | similarity: 0.64

There are four types of leave that are offered specifically to veterans and/or service members:

- Military leave for active duty, active duty training, and inactive duty training in the National Guard or as a Reservist.
- Military spouse relocation leave
- Disabled Veteran Leave for employees with a service-connected disability rating of 30 percent or more, to use during their first year of federal employment
- Funeral leave for veterans to participate in a funeral ceremony for a member of the Armed Forces. Funeral leave is also available for anyone who needs to plan or attend services of an immediate relative who has suffered a combat-related death.

========

[5] Family Medical Leave Act (FMLA) › About FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.62

FMLA entitles you to take up to 12 weeks of _unpaid_ leave per 12 month period for the following:

- The birth or care of a child
- An adoption or foster care placement of a child
- The care of a spouse/son/daughter/parent with a serious health condition
- Your serious health condition
- Handling issues (“exigencies”) that arise when your spouse, child, or parent is on active duty in the Armed Forces.

You can take up to 26 weeks of unpaid FMLA to care for an ill servicemember or veteran, if you are their spouse, child, parent, or next of kin.
```
</details>

## q04 (single)

**Question:** How many days of sick leave can I use for bereavement or to attend a family member's funeral?

**Reference answer:** Up to 13 days (104 hours) per year.

**Agent's answer:**

> As a civilian employee, you can use up to 13 days (104 hours) per year of your sick leave for bereavement, funeral planning, and/or attending the funeral of a family member [Leave types › Types of leave › Sick leave › For bereavement purposes].
> 
> *Please note that this handbook is a snapshot from June 2026 and you should confirm with HR (TTS-PeopleOps@gsa.gov) before making plans.*

<details><summary>Retrieved passages</summary>

```text
[1] Leave types › Types of leave › Sick leave › For bereavement purposes
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.79

Civilian
You can use up to 13 days (104 hours) per year of your sick leave for bereavement, funeral planning, and/or attending the funeral of a family member.

Military
You can receive 3 days (24 hours) of funeral leave to plan or attend services of an immediate relative who has suffered a combat-related death. Additionally, veterans can take funeral leave to participate in a funeral ceremony for a member of the Armed Forces.

OPM Fact Sheets:

- Sick leave for family care or bereavement purposes
- Definitions of family member and immediate relative

========

[2] Leave types › Types of leave › Sick leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.74

You can use Sick Leave for:

- Doctor and medical appointments for you or a family member
- Mental health care
- Recovering from illness, for you or a family member
- Any other health need

All federal employees, no matter how long they have worked in government, accrue four hours of sick leave per pay period. There is no maximum amount of sick leave you can accrue, and if you've transferred to TTS from another federal agency, your accrued sick leave will transfer with you.

You can use sick leave for your physical and mental health needs. You can also use up to 13 days of sick leave per year for family health needs and bereavement.

========

[3] Veteran & service member resources › Leave
source: general-information-and-resources/employee-resources-policies/veterans-service-members | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/veterans-service-members.md | similarity: 0.71

There are four types of leave that are offered specifically to veterans and/or service members:

- Military leave for active duty, active duty training, and inactive duty training in the National Guard or as a Reservist.
- Military spouse relocation leave
- Disabled Veteran Leave for employees with a service-connected disability rating of 30 percent or more, to use during their first year of federal employment
- Funeral leave for veterans to participate in a funeral ceremony for a member of the Armed Forces. Funeral leave is also available for anyone who needs to plan or attend services of an immediate relative who has suffered a combat-related death.

========

[4] Advanced sick leave
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.68

You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

For example: You have one year left on your term, which equals to 26 pay periods. You earn 4 sick leave hours per pay period. You will earn 104 more sick leave hours (26 pay periods x 4 hours per pay period). Therefore, you can request up to 104 advanced sick leave hours.

========

[5] Family Medical Leave Act (FMLA) › About FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.68

FMLA entitles you to take up to 12 weeks of _unpaid_ leave per 12 month period for the following:

- The birth or care of a child
- An adoption or foster care placement of a child
- The care of a spouse/son/daughter/parent with a serious health condition
- Your serious health condition
- Handling issues (“exigencies”) that arise when your spouse, child, or parent is on active duty in the Armed Forces.

You can take up to 26 weeks of unpaid FMLA to care for an ill servicemember or veteran, if you are their spouse, child, parent, or next of kin.
```
</details>

## q05 (single)

**Question:** How much administrative leave can I get to be a bone marrow donor?

**Reference answer:** Up to 7 days per calendar year (up to 30 days for organ donation).

**Agent's answer:**

> You can access up to 7 days of administrative leave during a calendar year to serve as a bone marrow donor [Leave types › Types of leave › Administrative Leave].
> 
> The handbook is a snapshot from June 2026 and you should confirm with HR.

<details><summary>Retrieved passages</summary>

```text
[1] Leave types › Types of leave › Administrative Leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.80

Blood, bone marrow, and organ donation
You can access up to 7 days of Administrative Leave during a calendar year to serve as a bone marrow donor, and up to 30 days serve as an organ donor.

You can also be granted up to 4 hours of Administrative Leave for blood donation.

OPM Fact Sheets:

- Administrative Leave

- Bone Marrow or Organ Donor Leave

COVID vaccination
You can take up to 4 hours of Administrative Leave to get a COVID vaccine or booster for yourself or a family member. You can also take up to 2 days of Administrative Leave when recovering from vaccine side effects.

========

[2] Leave types › Reasons someone can take leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.68

TTS has leave types for the following scenarios. Talk with your Workforce Relations HR Specialist about ways to combine leave types.

For **general uses and vacation**, you can use:

- Annual Leave
- Award Leave

For **sick or medical reasons**, you can use:

- Sick Leave

Other medical reasons:

- When getting a COVID vaccine or recovering from vaccine side effects, you can use Administrative Leave
- Blood, bone marrow, organ donation, you can use Administrative Leave
- Disabled veteran leave (DVL) for veterans with a service-related disability

For **bereavement**, you can use:

- Sick Leave for funerals
- Funeral Leave for military relatives
- Parental Bereavement Leave after losing a child

For **birth, adoption or placement of a new child**, you can use paid parental leave. You can also use annual and sick leave for parental leave reasons.

For **religious observances**, you can request an adjustment to your work schedule for religious observances, instead of taking leave.

To **vote**, register to vote, participate in early voting, or volunteering as a poll worker, you generally must do so on your own time (i.e., either before or after work), or during work hours by using approved annual leave, compensatory time off, comp time for travel, or credit hours (for employees on flexible schedules).

For **jury duty** and other court-related leave, use Court Leave.

If you can’t work or stay in your home for weather or safety reasons, you can request Administrative Leave.

When going on **active duty**, active duty training, and inactive duty training in the National Guard or as a Reservist, you can use Military Leave.

You can work with your supervisor to use up to 4 hours of work time pursuing options from the Employee Assistance Program (EAP).

If you are running out of leave hours, you can request:

========

[3] Voluntary Leave Transfer Program › To receive donated hours › Eligibility
source: travel-and-leave/voluntary-leave-transfer-program | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/voluntary-leave-transfer-program.md | similarity: 0.68

To be eligible for VLTP, you must have all of the following:

- Exhausted all leave balances (annual, sick, award)
- Have an anticipated negative leave balance of at least 24 hours
- A medical condition for you or a family member that is likely to require your absence for a prolonged period of time (24 work hours or more)

========

[4] Voluntary Leave Transfer Program › Donating leave
source: travel-and-leave/voluntary-leave-transfer-program | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/voluntary-leave-transfer-program.md | similarity: 0.67

The VLTP system is in MAX.gov. You will need to register with MAX.gov to donate leave.

Select the **Register Now** button at the top right of the MAX.gov homepage and follow the prompts to register your PIV card and enable login. You can also use the email option.

Donating hours through VLTP system
You can donate hours to your colleagues through VLTP or the Emergency Leave Transfer Program (ELTP).

1. Go to vltp.gsa.gov and log in using your PIV card or GSA email with 2-factor authentication.
2. You will be taken to the GSA Payroll System VLTP page.
3. Click the button on the bottom to Donate Annual Leave Hours To A Shared Leave Recipient.
4. Follow the system prompts to donate leave; select General Services Administration as the agency and 0 \- Central Office as the region.

If you have any questions, please email your Workforce Relations HR Specialist.

========

[5] Family Medical Leave Act (FMLA) › About FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.65

FMLA entitles you to take up to 12 weeks of _unpaid_ leave per 12 month period for the following:

- The birth or care of a child
- An adoption or foster care placement of a child
- The care of a spouse/son/daughter/parent with a serious health condition
- Your serious health condition
- Handling issues (“exigencies”) that arise when your spouse, child, or parent is on active duty in the Armed Forces.

You can take up to 26 weeks of unpaid FMLA to care for an ill servicemember or veteran, if you are their spouse, child, parent, or next of kin.
```
</details>

## q06 (single)

**Question:** When does award leave expire, and is it paid out if I leave?

**Reference answer:** It expires one year after it is issued (use it by the end of the pay period in which that date falls) and it is not paid out if you leave TTS.

**Agent's answer:**

> Award leave expires one year after it is issued, and it must be used by the end of the pay period in which that expiration date falls [Leave types › Types of leave › Award leave]. If you leave TTS, award leave is not paid out [Leave types › Types of leave › Award leave].
> 
> *The handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Leave types › Types of leave › Award leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.77

Award leave is offered for End of Year Performance Awards and Special Act Awards.

- If you are eligible for an End of Year Performance Award, you can opt-in via HRLinks to receive Award Leave in lieu of a monetary award.
- If you are receiving a TTS Special Act Award, you will be notified and asked for your preference of award leave or a monetary award.

You can receive a maximum of 80 hours of award leave in a single fiscal year. If you receive a Special Act Award after hitting the 80 hour cap, your award will be monetary.

Award leave expires one year after it is issued. You must use it by the end of the pay period in which the expiration date falls. Expired award leave cannot be recovered \- please monitor your leave balances and consider using award leave first. If you leave TTS, award leave is not paid out.

You can check the amount of Award leave you have in HR Links. You may receive an automated email reminder from HR Links 3 months before your leave expires, even if you have already used it.

OPM Policy:

- Time-Off Awards

========

[2] Leave types › Types of leave › Annual leave › Use or Lose
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.70

Use or Lose is the number of annual leave hours you would forfeit at the end of the leave year, if you do not use any of your annual leave hours between now and then. As noted above, there is a 240 hour limit on the number of hours you can carry over from one leave year to the next. Use or Lose only applies to annual leave.

For example: You look in HRLinks and see "182 Hours (96 Hours Use or Lose)." Today, January 25th, 2022, you have 182 hours of annual leave available. If you continued to accrue annual leave for the rest of the year, and you did not use any of those hours, you would forfeit 96 hours of annual leave at the end of the year. You would be 96 hours over the 240 cap.

182 current hours \+ 154 more hours accrued throughout the year \= 336 hours.

336 hours \- 240 hour cap \= 96 Use or Lose hours that would be forfeited.

========

[3] Compensation for working extra hours › Overtime and Compensatory (Comp) time › Compensatory (Comp) time, depending on your salary level
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.69

Comp time is when you receive hours of leave instead of overtime pay. To determine the maximum number of comp time hours that you can accrue per pay period, please use the Bi-weekly Comp Time Cap Calculator. If you make the maximum salary ($191,900 in 2024), you cannot receive comp time.

You should use your accrued comp time before using Annual Leave. However, if the end of the leave year is approaching and you're in danger of losing Annual Leave because of “Use or Lose, your supervisor can prioritize your Annual Leave requests over comp time.”

Comp time expires one year (26 pay periods) after it's earned. When you reach that expiration date, you forfeit the relevant leave. If you leave GSA, your comp time will be paid out.

Refer to OPM’s Comp Time Fact Sheet for more detail.

========

[4] Compensation for working extra hours › Travel comp time, for everyone › Using travel comp time
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.69

Travel comp time expires one year (26 pay periods) after it is earned. When you reach the expiration date, you will forfeit the leave. If you leave GSA, any unused travel comp time will be forfeited.

========

[5] Performance Management Overview › Who participates in the end of year performance review? › Selecting award preference in HR Links
source: performance-management/index | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/performance-management/index.md | similarity: 0.68

If you are eligible for an end-of-year individual performance award (cash or
time-off), **please make a selection no later than November 15th.** If you would
like to keep the same selection type as the previous fiscal year, no further action is needed.

- **Monetary award:** This is the default option in HR Links. No action is
  needed in HR Links **unless you specified award time off for the prior review
  cycle**

- To change from **LEAVE** to **CASH**, you need to change your “Time Off
    Award Preference” to **“Inactive”** and you must then use the **“Save”**
    button.
  - **_Note:_** These
    instructions
    show where to make the change in HR Links

- **Award leave:** If you would like to select award time off in lieu of a
  monetary award, please follow
  these instructions.
```
</details>

## q07 (single)

**Question:** Who has to approve a request for more than 80 hours of leave without pay?

**Reference answer:** Written approval from your immediate supervisor and your Business Unit Director; then send the email thread to TTS-peopleops@gsa.gov.

**Agent's answer:**

> To request more than 80 hours of leave without pay (LWOP), you must obtain written approval from both your immediate supervisor and your Business Unit Director [Leave types › Types of leave › Unpaid leave]. Once these approvals are received, you should submit a copy of the email thread to TTS-peopleops@gsa.gov [Leave types › Types of leave › Unpaid leave].
> 
> *Note: This handbook is a snapshot from June 2026; please confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Leave types › Types of leave › Unpaid leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.75

If you have exhausted all other paid leave options, you can request Leave Without Pay (LWOP). It is exactly what it sounds like. You can request unpaid leave of less than four weeks at any time.

The use of LWOP, including FMLA LWOP, can affect insurance premiums, within-grade increases, and other benefits. We **strongly recommend** that you review OPM’s page on the Effect of Extended Leave Without Pay (LWOP). If you have questions, reach out to your Benefits Specialist.

To take a leave of absence without pay, you’ll need justification and supervisory oversight. For longer periods, you'll also need 2nd level supervisory approval:

- To request 80 hours or less of LWOP, you must get written approval from your immediate supervisor.

- To request over 80 hours of LWOP, you must get written approval from your immediate supervisor and Business Unit Director.

Once approvals are received, please submit a copy of the email thread to TTS-peopleops@gsa.gov.

OPM Fact Sheet:

- Effect of Extended Leave Without Pay (LWOP) (or Other Nonpay Status) on Federal Benefits and Programs

========

[2] Leave types › Types of leave › Award leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.67

Award leave is offered for End of Year Performance Awards and Special Act Awards.

- If you are eligible for an End of Year Performance Award, you can opt-in via HRLinks to receive Award Leave in lieu of a monetary award.
- If you are receiving a TTS Special Act Award, you will be notified and asked for your preference of award leave or a monetary award.

You can receive a maximum of 80 hours of award leave in a single fiscal year. If you receive a Special Act Award after hitting the 80 hour cap, your award will be monetary.

Award leave expires one year after it is issued. You must use it by the end of the pay period in which the expiration date falls. Expired award leave cannot be recovered \- please monitor your leave balances and consider using award leave first. If you leave TTS, award leave is not paid out.

You can check the amount of Award leave you have in HR Links. You may receive an automated email reminder from HR Links 3 months before your leave expires, even if you have already used it.

OPM Policy:

- Time-Off Awards

========

[3] Advanced sick leave
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.65

You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

For example: You have one year left on your term, which equals to 26 pay periods. You earn 4 sick leave hours per pay period. You will earn 104 more sick leave hours (26 pay periods x 4 hours per pay period). Therefore, you can request up to 104 advanced sick leave hours.

========

[4] Going out of office › Your overall responsibilities
source: travel-and-leave/going-out-of-office | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/going-out-of-office.md | similarity: 0.65

You must report to work or have an approved leave request in HR Links, every scheduled work day. You are also responsible for submitting your timesheet at the end of every pay period.

You should submit leave requests at least three business days in advance, and make timely edits if your plans change.

For unplanned leave \- such as a sudden illness or a family emergency \- do what you can to contact your supervisor, and they can help manage the rest on your behalf.

Some types of leave require supporting documentation: it is your responsibility to submit all necessary documents and check that you’ve received approval.

========

[5] Benefits › Leave
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.64

Please use HR Links to request sick
leave and annual leave. For any leave-related questions, please contact
cpc.benefits-retirement@gsa.gov.

For more information on Leave, including sick, funeral, unpaid, parental,
advanced, and religious, please reference the Leave page.
```
</details>

## q08 (single)

**Question:** I have been a federal employee for 8 months. Can I take paid parental leave?

**Reference answer:** Not yet: you need 12 months of federal service to use PPL (most veterans are eligible immediately).

**Agent's answer:**

> No, you are not eligible for paid parental leave at this time. To access Paid Parental Leave, you must have been a federal employee for at least 12 months [Paid parental leave (PPL) › About PPL], [Family Medical Leave Act (FMLA) › How FMLA works › Paid Parental Leave and FMLA].
> 
> Since you have less than 1 year of federal service, the handbook recommends checking the recommendations for new federal employees [Paid parental leave (PPL) › About PPL], [Family Medical Leave Act (FMLA) › How FMLA works › Paid Parental Leave and FMLA]. Please reach out to People Ops (TTS-PeopleOps@gsa.gov) for guidance on your specific situation.
> 
> This handbook is a snapshot from June 2026; please confirm this information with HR.

<details><summary>Retrieved passages</summary>

```text
[1] Paid parental leave (PPL) › About PPL
source: travel-and-leave/paid-parental-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/paid-parental-leave.md | similarity: 0.78

- You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. (Supervisor approval is needed for the intermittent option).
- You must use the PPL within a year of the child’s birth or placement
- You need to have been a federal employee for 12 months in order to access Paid Parental Leave (note: most veterans are immediately eligible). If you are a new federal employee, check out the recommendations for those who have less than 1 year of federal service.
- You need to be approved for PPL before being able to use it.
- You will need to sign an agreement, stating that you will return to work for at least 12 weeks after your final day on PPL.
  - The 12 week agreement is in place regardless of how many weeks of PPL you take. If you take PPL intermittently, the 12 week period still begins after your _final_ day of PPL, even if you have been working in between periods of PPL.
- GSA implements PPL via Family and Medical Leave Act (FMLA) leave. If you previously used FMLA within the past 12 months of your parental leave period, those hours would be subtracted from the 12 weeks you can take for PPL.

========

[2] Family Medical Leave Act (FMLA) › How FMLA works › Paid Parental Leave and FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.74

You have to be eligible for FMLA to receive Paid Parental Leave (PPL). PPL is how the federal government implements FMLA for parental leave. This means you must have at least one year of federal service to use PPL. If you are a new federal employee, check out the recommendations for those who have less than 1 year of federal service.

If you use FMLA prior to PPL, it reduces the number of PPL hours you can receive (and vice versa). If you max out 12 weeks of PPL, that uses up all the FMLA you can use for the next 52 weeks.

========

[3] Paid parental leave (PPL) › Requesting paid parental leave › Prior to birth/placement
source: travel-and-leave/paid-parental-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/paid-parental-leave.md | similarity: 0.72

To request PPL, you’ll need to email the following items to your Workforce Relations HR Specialist:

1. The Paid Parental Leave Request and the Paid Parental Leave Service Agreement form PDFs.
   1. You can use Docusign templates for Paid Parental Leave to fill out the forms and request the right signatures.
2. A timesheet report for the last 12 months.

Your Workforce Relations HR Specialist reviews your forms and may request more information.

========

[4] Family Medical Leave Act (FMLA) › About FMLA › Eligibility
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.72

To be eligible for FMLA, you must have at least one year of federal service. Note that most veterans are immediately eligible.

Medical documentation to support your request is required.

========

[5] Leave types › Types of leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.69

Family Medical Leave Act (FMLA)
If you need more than 13 sick days at once to care for a loved one, you can apply for Family Medical Leave Act (FMLA) status. Refer to the FMLA page for more, including applying for FMLA.

Paid Parental Leave
You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. Refer to the Paid Parental Leave page for more information, including requesting PPL.
```
</details>

## q09 (single)

**Question:** After paid parental leave, how long do I have to commit to staying at work?

**Reference answer:** At least 12 weeks after your final day of PPL, whatever number of weeks you took.

**Agent's answer:**

> You are required to sign an agreement committing to return to work for at least 12 weeks after your final day of paid parental leave (PPL) [Paid parental leave (PPL) › About PPL].
> 
> This 12-week agreement applies regardless of how many weeks of PPL you use, and if you take the leave intermittently, the 12-week period begins after your final day of PPL [Paid parental leave (PPL) › About PPL].
> 
> *Please note that this handbook is a snapshot from June 2026 and you should confirm this with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Paid parental leave (PPL) › About PPL
source: travel-and-leave/paid-parental-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/paid-parental-leave.md | similarity: 0.70

- You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. (Supervisor approval is needed for the intermittent option).
- You must use the PPL within a year of the child’s birth or placement
- You need to have been a federal employee for 12 months in order to access Paid Parental Leave (note: most veterans are immediately eligible). If you are a new federal employee, check out the recommendations for those who have less than 1 year of federal service.
- You need to be approved for PPL before being able to use it.
- You will need to sign an agreement, stating that you will return to work for at least 12 weeks after your final day on PPL.
  - The 12 week agreement is in place regardless of how many weeks of PPL you take. If you take PPL intermittently, the 12 week period still begins after your _final_ day of PPL, even if you have been working in between periods of PPL.
- GSA implements PPL via Family and Medical Leave Act (FMLA) leave. If you previously used FMLA within the past 12 months of your parental leave period, those hours would be subtracted from the 12 weeks you can take for PPL.

========

[2] Paid parental leave (PPL)
source: travel-and-leave/paid-parental-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/paid-parental-leave.md | similarity: 0.68

TTS has paid parental leave (PPL) for the birth or placement (adoption or foster care) of a child.

========

[3] Family Medical Leave Act (FMLA) › How FMLA works › Paid Parental Leave and FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.67

You have to be eligible for FMLA to receive Paid Parental Leave (PPL). PPL is how the federal government implements FMLA for parental leave. This means you must have at least one year of federal service to use PPL. If you are a new federal employee, check out the recommendations for those who have less than 1 year of federal service.

If you use FMLA prior to PPL, it reduces the number of PPL hours you can receive (and vice versa). If you max out 12 weeks of PPL, that uses up all the FMLA you can use for the next 52 weeks.

========

[4] Leave types › Types of leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.66

Family Medical Leave Act (FMLA)
If you need more than 13 sick days at once to care for a loved one, you can apply for Family Medical Leave Act (FMLA) status. Refer to the FMLA page for more, including applying for FMLA.

Paid Parental Leave
You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. Refer to the Paid Parental Leave page for more information, including requesting PPL.

========

[5] Leave types
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.66

Current employees can use this leave comparison chart.

Before you take leave, check out of office expectations.
```
</details>

## q10 (single)

**Question:** What does the doctor's note need to include for birth-related paid parental leave?

**Reference answer:** Date of birth, diagnosis, prognosis, and duration of care.

**Agent's answer:**

> For birth-related Paid Parental Leave (PPL), the medical note from your doctor must include the following information:
> 
> *   Date of birth [Paid parental leave (PPL) › Requesting paid parental leave › After birth/placement]
> *   Diagnosis [Paid parental leave (PPL) › Requesting paid parental leave › After birth/placement]
> *   Prognosis [Paid parental leave (PPL) › Requesting paid parental leave › After birth/placement]
> *   Duration – The duration of time for care (e.g., how long the parent and/or child will need medical care) [Paid parental leave (PPL) › Requesting paid parental leave › After birth/placement]
> 
> You should submit this note to your Workforce Relations HR Specialist [Paid parental leave (PPL) › Requesting paid parental leave › After birth/placement].
> 
> *The handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Paid parental leave (PPL) › Requesting paid parental leave › After birth/placement
source: travel-and-leave/paid-parental-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/paid-parental-leave.md | similarity: 0.82

To use your PPL, you must submit documentation about the birth or placement of your child:

1. Send a message (email, text, call, or Slack) to your Workforce Relations HR Specialist, letting them know the date of birth/placement.
2. Send supporting documentation to show childbirth, adoption, or foster placement to your Workforce Relations HR Specialist.

Birth-supporting documentation
You’ll need a medical note from your doctor. The medical note will be used as a supporting document for PPL, as well as Advanced Sick Leave and/or VLTP if you are using them.

The medical note should include:

- Date of birth
- Diagnosis
- Prognosis
- Duration \- The duration of time for care (how long will the parent and/or child need medical care? 6 weeks? 8 weeks?)

========

[2] Paid parental leave (PPL) › Requesting paid parental leave › Prior to birth/placement
source: travel-and-leave/paid-parental-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/paid-parental-leave.md | similarity: 0.76

To request PPL, you’ll need to email the following items to your Workforce Relations HR Specialist:

1. The Paid Parental Leave Request and the Paid Parental Leave Service Agreement form PDFs.
   1. You can use Docusign templates for Paid Parental Leave to fill out the forms and request the right signatures.
2. A timesheet report for the last 12 months.

Your Workforce Relations HR Specialist reviews your forms and may request more information.

========

[3] Leave types › Types of leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.75

Family Medical Leave Act (FMLA)
If you need more than 13 sick days at once to care for a loved one, you can apply for Family Medical Leave Act (FMLA) status. Refer to the FMLA page for more, including applying for FMLA.

Paid Parental Leave
You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. Refer to the Paid Parental Leave page for more information, including requesting PPL.

========

[4] Family Medical Leave Act (FMLA) › About FMLA › Eligibility
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.74

To be eligible for FMLA, you must have at least one year of federal service. Note that most veterans are immediately eligible.

Medical documentation to support your request is required.

========

[5] Family Medical Leave Act (FMLA) › About FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.73

FMLA entitles you to take up to 12 weeks of _unpaid_ leave per 12 month period for the following:

- The birth or care of a child
- An adoption or foster care placement of a child
- The care of a spouse/son/daughter/parent with a serious health condition
- Your serious health condition
- Handling issues (“exigencies”) that arise when your spouse, child, or parent is on active duty in the Armed Forces.

You can take up to 26 weeks of unpaid FMLA to care for an ill servicemember or veteran, if you are their spouse, child, parent, or next of kin.
```
</details>

## q11 (single)

**Question:** How many weeks of unpaid FMLA leave can I take to care for my spouse, who is a seriously ill servicemember?

**Reference answer:** Up to 26 weeks.

**Agent's answer:**

> You can take up to 26 weeks of unpaid FMLA leave to care for a seriously ill servicemember or veteran if you are their spouse [Family Medical Leave Act (FMLA) › About FMLA].
> 
> *Please note: This handbook is a snapshot from June 2026 and you should confirm this with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Family Medical Leave Act (FMLA) › About FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.80

FMLA entitles you to take up to 12 weeks of _unpaid_ leave per 12 month period for the following:

- The birth or care of a child
- An adoption or foster care placement of a child
- The care of a spouse/son/daughter/parent with a serious health condition
- Your serious health condition
- Handling issues (“exigencies”) that arise when your spouse, child, or parent is on active duty in the Armed Forces.

You can take up to 26 weeks of unpaid FMLA to care for an ill servicemember or veteran, if you are their spouse, child, parent, or next of kin.

========

[2] Family Medical Leave Act (FMLA) › About FMLA › Eligibility
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.79

To be eligible for FMLA, you must have at least one year of federal service. Note that most veterans are immediately eligible.

Medical documentation to support your request is required.

========

[3] Leave types › Types of leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.74

Family Medical Leave Act (FMLA)
If you need more than 13 sick days at once to care for a loved one, you can apply for Family Medical Leave Act (FMLA) status. Refer to the FMLA page for more, including applying for FMLA.

Paid Parental Leave
You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. Refer to the Paid Parental Leave page for more information, including requesting PPL.

========

[4] Veteran & service member resources › Leave
source: general-information-and-resources/employee-resources-policies/veterans-service-members | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/veterans-service-members.md | similarity: 0.73

There are four types of leave that are offered specifically to veterans and/or service members:

- Military leave for active duty, active duty training, and inactive duty training in the National Guard or as a Reservist.
- Military spouse relocation leave
- Disabled Veteran Leave for employees with a service-connected disability rating of 30 percent or more, to use during their first year of federal employment
- Funeral leave for veterans to participate in a funeral ceremony for a member of the Armed Forces. Funeral leave is also available for anyone who needs to plan or attend services of an immediate relative who has suffered a combat-related death.

========

[5] Leave types › Types of leave › Military leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.72

Going on active duty
If you are called to active duty, no matter the length of time, contact the FAS Benefits Specialist who corresponds to your last name. They can help with GSA’s Checklist for Employees Entering Extended Active Duty.

OPM Fact Sheet:

- Military Leave Fact Sheet

Military spouse relocation
If you are a civilian employee who must accompany the relocation of your military spouse, you are entitled to 5 days of administrative leave to help make that moving process easier.

- See Presidential Executive Order 14100 (2023)
```
</details>

## q12 (single)

**Question:** What do I need to be eligible to receive donated leave through the Voluntary Leave Transfer Program?

**Reference answer:** All leave balances (annual, sick, award) exhausted, an anticipated negative balance of at least 24 hours, and a medical condition for you or a family member likely to keep you away 24 work hours or more.

**Agent's answer:**

> To be eligible to receive donated leave through the Voluntary Leave Transfer Program (VLTP), you must meet all of the following requirements:
> 
> *   You have exhausted all of your leave balances (annual, sick, award) [Voluntary Leave Transfer Program › To receive donated hours › Eligibility].
> *   You have an anticipated negative leave balance of at least 24 hours [Voluntary Leave Transfer Program › To receive donated hours › Eligibility].
> *   You have a medical condition for yourself or a family member that is likely to require your absence for a prolonged period of time (24 work hours or more) [Voluntary Leave Transfer Program › To receive donated hours › Eligibility].
> 
> The handbook also notes that if you have a personal or family medical emergency and have exhausted your earned leave, you can enroll in the VLTP [Leave types › Types of leave].
> 
> *Note: This handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Voluntary Leave Transfer Program › To receive donated hours › Eligibility
source: travel-and-leave/voluntary-leave-transfer-program | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/voluntary-leave-transfer-program.md | similarity: 0.86

To be eligible for VLTP, you must have all of the following:

- Exhausted all leave balances (annual, sick, award)
- Have an anticipated negative leave balance of at least 24 hours
- A medical condition for you or a family member that is likely to require your absence for a prolonged period of time (24 work hours or more)

========

[2] Voluntary Leave Transfer Program
source: travel-and-leave/voluntary-leave-transfer-program | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/voluntary-leave-transfer-program.md | similarity: 0.83

The Voluntary Leave Transfer Program (VLTP) allows TTS employees to donate annual leave directly to another employee who has a personal or family medical emergency.

========

[3] Leave types › Types of leave › Administrative Leave › Weather and safety › Emergency Leave Transfer Program
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.79

OPM may establish an emergency leave transfer program for certain disasters. If eligible, you may receive donated leave from your colleagues to take paid leave. You can use this paid leave to help you or a family member recover from the disaster. This includes coordinating with insurance adjusters, carpenters, flood mitigation and restoration companies, and roofing contractors.

Resources:

- About ELTP (InSite)
- How to apply for ELTP (InSite)

========

[4] Leave types › Types of leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.78

Taking advanced leave › Advanced sick leave
You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

Refer to the advanced sick leave page for more information, including how to request it.

Using donated leave
If you have a personal or family medical emergency and have exhausted your earned leave, you can enroll in the Voluntary Leave Transfer Program (VLTP). Your colleagues can donate their annual leave for you. Reach out to your Workforce Relations HR Specialist to start the process.

========

[5] Family Medical Leave Act (FMLA) › About FMLA › Eligibility
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.73

To be eligible for FMLA, you must have at least one year of federal service. Note that most veterans are immediately eligible.

Medical documentation to support your request is required.
```
</details>

## q13 (single)

**Question:** How many credit hours can I have saved at one time, and do they expire?

**Reference answer:** Up to 24 credit hours; they roll over and never expire (paid out only if you leave GSA).

**Agent's answer:**

> You can have up to 24 credit hours accrued at any given time [Compensation for working extra hours › Credit hours, in flexible work schedules]. These hours will roll over from one pay period to the next, and they never expire [Compensation for working extra hours › Credit hours, in flexible work schedules].
> 
> This handbook is a snapshot from June 2026; please confirm with HR.

<details><summary>Retrieved passages</summary>

```text
[1] Compensation for working extra hours › Credit hours, in flexible work schedules
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.71

Only people on flexible work schedules can earn and use credit hours. There's no salary maximum for earning and using credit hours. To establish a flexible work schedule, talk with your supervisor.

You can then be approved for credit hours if you want to voluntarily work additional hours beyond your normal/approved schedule. If you are _required_ to work additional hours, you will receive overtime or comp time.

- You can have up to 24 credit hours accrued at any given time.

- The hours will roll over from one pay period to the next, and they never expire.

- Credit hours cannot be converted to cash unless you leave GSA (then they will be paid out).

Refer to OPM’s Credit Hours Fact Sheet for more detail.

========

[2] Compensation for working extra hours › Credit hours, in flexible work schedules › Credit hours mechanics
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.68

There are two steps to earning credit hours. First, request to work the additional time in HR Links under "Request Additional Time" on your timecard or "Additional Time Requests" on your Self-service page. Your supervisor will need to approve this (while you're establishing a flexible work schedule is a good time to discuss if or how to notify them outside of HR Links). Second, log the extra hours you worked on your timesheet using time reporting code 036 (Credit Hours Earned).

========

[3] Leave types › Types of leave › Annual leave › Use or Lose
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.65

Use or Lose is the number of annual leave hours you would forfeit at the end of the leave year, if you do not use any of your annual leave hours between now and then. As noted above, there is a 240 hour limit on the number of hours you can carry over from one leave year to the next. Use or Lose only applies to annual leave.

For example: You look in HRLinks and see "182 Hours (96 Hours Use or Lose)." Today, January 25th, 2022, you have 182 hours of annual leave available. If you continued to accrue annual leave for the rest of the year, and you did not use any of those hours, you would forfeit 96 hours of annual leave at the end of the year. You would be 96 hours over the 240 cap.

182 current hours \+ 154 more hours accrued throughout the year \= 336 hours.

336 hours \- 240 hour cap \= 96 Use or Lose hours that would be forfeited.

========

[4] Leave types › Types of leave › Award leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.64

Award leave is offered for End of Year Performance Awards and Special Act Awards.

- If you are eligible for an End of Year Performance Award, you can opt-in via HRLinks to receive Award Leave in lieu of a monetary award.
- If you are receiving a TTS Special Act Award, you will be notified and asked for your preference of award leave or a monetary award.

You can receive a maximum of 80 hours of award leave in a single fiscal year. If you receive a Special Act Award after hitting the 80 hour cap, your award will be monetary.

Award leave expires one year after it is issued. You must use it by the end of the pay period in which the expiration date falls. Expired award leave cannot be recovered \- please monitor your leave balances and consider using award leave first. If you leave TTS, award leave is not paid out.

You can check the amount of Award leave you have in HR Links. You may receive an automated email reminder from HR Links 3 months before your leave expires, even if you have already used it.

OPM Policy:

- Time-Off Awards

========

[5] Term extensions
source: hiring-staying-or-changing-jobs/term-extensions | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/term-extensions.md | similarity: 0.63

Many TTS employees are hired on term appointments for a maximum of four or eight
years. However, term appointments need to be renewed every two years or 3 years
depending on the appointment.

If you don’t know when your term ends, you can find your Not To Exceed (NTE)
date by looking in HR Links. Click on
the navigator icon, choose `Navigator`, then `Workforce Administration`, then
`Job Information`, then `Employee Request USF`.
```
</details>

## q14 (single)

**Question:** When does regular comp time expire?

**Reference answer:** One year (26 pay periods) after it is earned; after that it is forfeited.

**Agent's answer:**

> Regular comp time expires one year (26 pay periods) after it is earned [Compensation for working extra hours › Overtime and Compensatory (Comp) time › Compensatory (Comp) time, depending on your salary level]. When you reach that expiration date, you forfeit the relevant leave [Compensation for working extra hours › Overtime and Compensatory (Comp) time › Compensatory (Comp) time, depending on your salary level].
> 
> *Please note that this handbook is a snapshot from June 2026 and you should confirm this with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Compensation for working extra hours › Overtime and Compensatory (Comp) time › Compensatory (Comp) time, depending on your salary level
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.81

Comp time is when you receive hours of leave instead of overtime pay. To determine the maximum number of comp time hours that you can accrue per pay period, please use the Bi-weekly Comp Time Cap Calculator. If you make the maximum salary ($191,900 in 2024), you cannot receive comp time.

You should use your accrued comp time before using Annual Leave. However, if the end of the leave year is approaching and you're in danger of losing Annual Leave because of “Use or Lose, your supervisor can prioritize your Annual Leave requests over comp time.”

Comp time expires one year (26 pay periods) after it's earned. When you reach that expiration date, you forfeit the relevant leave. If you leave GSA, your comp time will be paid out.

Refer to OPM’s Comp Time Fact Sheet for more detail.

========

[2] Compensation for working extra hours › Travel comp time, for everyone › Using travel comp time
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.79

Travel comp time expires one year (26 pay periods) after it is earned. When you reach the expiration date, you will forfeit the leave. If you leave GSA, any unused travel comp time will be forfeited.

========

[3] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Compressed schedule
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.72

You are scheduled to arrive and depart at the same time, every day that you work. The start/stop times do not change from one pay period to the next. But, you work longer than 8 hours each day, so that you do not have to work the full 10 days in a pay period. This is a common TTS schedule, which we have typically called an Alternate Work Schedule (AWS).

- Overtime and comp time: Yes - Can only be approved for any hours that are in excess of what is normally scheduled for that work day (i.e., over the 8, 9, 10, 12 you were scheduled).
- Holiday pay: Yes - You will receive holiday pay for the 8, 9, 10, 12 hours you were scheduled to work. If a holiday falls on your scheduled off day, GSA may move your holiday one day earlier or later.
- Credit hours: No - Not available with this schedule

Compressed schedule examples - in a 2 week pay period:

- Example 1: You work four, 10 hour days each week. You have one specific day off each week.
- Example 2: One week, you work four 9 hour days and one 8 hour day (44 hours). The other week, you work four 9 hour days (36 hours) and have a specific day off.

========

[4] Leave types › Types of leave › Award leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.71

Award leave is offered for End of Year Performance Awards and Special Act Awards.

- If you are eligible for an End of Year Performance Award, you can opt-in via HRLinks to receive Award Leave in lieu of a monetary award.
- If you are receiving a TTS Special Act Award, you will be notified and asked for your preference of award leave or a monetary award.

You can receive a maximum of 80 hours of award leave in a single fiscal year. If you receive a Special Act Award after hitting the 80 hour cap, your award will be monetary.

Award leave expires one year after it is issued. You must use it by the end of the pay period in which the expiration date falls. Expired award leave cannot be recovered \- please monitor your leave balances and consider using award leave first. If you leave TTS, award leave is not paid out.

You can check the amount of Award leave you have in HR Links. You may receive an automated email reminder from HR Links 3 months before your leave expires, even if you have already used it.

OPM Policy:

- Time-Off Awards

========

[5] Leave types › Types of leave › Annual leave › Use or Lose
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.69

Use or Lose is the number of annual leave hours you would forfeit at the end of the leave year, if you do not use any of your annual leave hours between now and then. As noted above, there is a 240 hour limit on the number of hours you can carry over from one leave year to the next. Use or Lose only applies to annual leave.

For example: You look in HRLinks and see "182 Hours (96 Hours Use or Lose)." Today, January 25th, 2022, you have 182 hours of annual leave available. If you continued to accrue annual leave for the rest of the year, and you did not use any of those hours, you would forfeit 96 hours of annual leave at the end of the year. You would be 96 hours over the 240 cap.

182 current hours \+ 154 more hours accrued throughout the year \= 336 hours.

336 hours \- 240 hour cap \= 96 Use or Lose hours that would be forfeited.
```
</details>

## q15 (single)

**Question:** On a Variable Day schedule, what is the most I can work in a single day?

**Reference answer:** 12 hours (and the days must add up to 40 hours a week).

**Agent's answer:**

> The maximum number of hours you can work in a single day on a Variable Week schedule is 12 [Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Types of flexible schedules › Variable Week].
> 
> *Please note that this handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Types of flexible schedules › Variable Week
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.78

- Each day in the workweek can be slightly longer or shorter than 8 hours.
- Each week can be shorter/longer than 40 hours, as long as together, the two weeks add up to 80 hours for the pay period.
- You work 5 days a week.
- The maximum number of hours you can work in a single day is 12.

For example:
|**Day** |**Hours** | **Day** |**Hours** |

| Monday | 5 | Monday | 10 |
| Tuesday | 9 | Tuesday | 10 |
| Wednesday| 6 | Wednesday| 6 |
| Thursday | 9 | Thursday | 9 |
| Friday | 8 | Friday | 8 |
| **Week 1 Total**|**37** | **Week 2 Total**| **43** |

========

[2] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Types of flexible schedules › Maxiflex
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.75

- Same as Variable Week, but you may work fewer than 10 days per pay period.

For example:
|**Day** |**Hours** | **Day** |**Hours** |

| Monday | 8 | Monday | Off |
| Tuesday | 10 | Tuesday | 10 |
| Wednesday| 11 | Wednesday| 6 |
| Thursday | 11 | Thursday | 9 |
| Friday | 6 | Friday | 8 |
| **Week 1 Total**|**46** | **Week 2 Total**| **34** |

========

[3] Compensation for working extra hours › Credit hours, in flexible work schedules
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.65

Only people on flexible work schedules can earn and use credit hours. There's no salary maximum for earning and using credit hours. To establish a flexible work schedule, talk with your supervisor.

You can then be approved for credit hours if you want to voluntarily work additional hours beyond your normal/approved schedule. If you are _required_ to work additional hours, you will receive overtime or comp time.

- You can have up to 24 credit hours accrued at any given time.

- The hours will roll over from one pay period to the next, and they never expire.

- Credit hours cannot be converted to cash unless you leave GSA (then they will be paid out).

Refer to OPM’s Credit Hours Fact Sheet for more detail.
```
</details>

## q16 (single)

**Question:** Can I earn credit hours on a compressed schedule?

**Reference answer:** No, credit hours are not available on a compressed schedule.

**Agent's answer:**

> No, you cannot earn credit hours on a compressed schedule [Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Compressed schedule]. Only employees on flexible work schedules are eligible to earn and use credit hours [Compensation for working extra hours › Credit hours, in flexible work schedules].
> 
> *This handbook is a snapshot from June 2026; please confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Compressed schedule
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.76

You are scheduled to arrive and depart at the same time, every day that you work. The start/stop times do not change from one pay period to the next. But, you work longer than 8 hours each day, so that you do not have to work the full 10 days in a pay period. This is a common TTS schedule, which we have typically called an Alternate Work Schedule (AWS).

- Overtime and comp time: Yes - Can only be approved for any hours that are in excess of what is normally scheduled for that work day (i.e., over the 8, 9, 10, 12 you were scheduled).
- Holiday pay: Yes - You will receive holiday pay for the 8, 9, 10, 12 hours you were scheduled to work. If a holiday falls on your scheduled off day, GSA may move your holiday one day earlier or later.
- Credit hours: No - Not available with this schedule

Compressed schedule examples - in a 2 week pay period:

- Example 1: You work four, 10 hour days each week. You have one specific day off each week.
- Example 2: One week, you work four 9 hour days and one 8 hour day (44 hours). The other week, you work four 9 hour days (36 hours) and have a specific day off.

========

[2] Compensation for working extra hours › Credit hours, in flexible work schedules
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.66

Only people on flexible work schedules can earn and use credit hours. There's no salary maximum for earning and using credit hours. To establish a flexible work schedule, talk with your supervisor.

You can then be approved for credit hours if you want to voluntarily work additional hours beyond your normal/approved schedule. If you are _required_ to work additional hours, you will receive overtime or comp time.

- You can have up to 24 credit hours accrued at any given time.

- The hours will roll over from one pay period to the next, and they never expire.

- Credit hours cannot be converted to cash unless you leave GSA (then they will be paid out).

Refer to OPM’s Credit Hours Fact Sheet for more detail.

========

[3] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Types of flexible schedules › Variable Week
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.66

- Each day in the workweek can be slightly longer or shorter than 8 hours.
- Each week can be shorter/longer than 40 hours, as long as together, the two weeks add up to 80 hours for the pay period.
- You work 5 days a week.
- The maximum number of hours you can work in a single day is 12.

For example:
|**Day** |**Hours** | **Day** |**Hours** |

| Monday | 5 | Monday | 10 |
| Tuesday | 9 | Tuesday | 10 |
| Wednesday| 6 | Wednesday| 6 |
| Thursday | 9 | Thursday | 9 |
| Friday | 8 | Friday | 8 |
| **Week 1 Total**|**37** | **Week 2 Total**| **43** |

========

[4] Compensation for working extra hours › Credit hours, in flexible work schedules › Credit hours example
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.66

You're on a Gliding schedule, and you work 8 hours every day. You're not required to stay late, but if you're in a productive headspace and want to work an extra hour to finish work, you can ask your supervisor about working 1 more hour, therefore receiving 1 credit hour. The HR Links process formalizes and records this approval.
```
</details>

## q17 (single)

**Question:** How long does it take to get reimbursed after I submit a travel voucher?

**Reference answer:** The voucher is reviewed in 3 to 5 business days, and the money arrives 3 to 5 business days after approval.

**Agent's answer:**

> Your travel voucher will be reviewed in 3-5 business days, and reimbursement will be credited to your bank account and travel card 3-5 business days after approval [Get reimbursed › Brief overview of vouchers].
> 
> If it has been over a week after your voucher has been approved and your reimbursement has not arrived, you should contact kc-travel.finance@gsa.gov and cc tts-travel@gsa.gov [Frequently Asked Questions › Questions about reimbursement › Issues with reimbursement].
> 
> *This handbook is a snapshot from June 2026; please confirm this information with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] What to consider while traveling › Don't forget about vouchers!
source: travel-and-leave/travel-and-leave-policies/travel-guide-3-travel | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-3-travel.md | similarity: 0.78

Have a good trip, get
reimbursement--
filling out a voucher-- within 5 business days of getting back.

Why the rush? Filling out a voucher correctly allows you to:

1. Get reimbursed for your M&IE and for any hotels, airplane tickets, or other
   expenses you paid for personally.

2. Have the government automatically pay off the balance on your Travel Card. If
   you do your voucher correctly and on time, you will never have to worry about
   paying one of those bills yourself.

On the other side, when travel expenses are submitted late, it’s a major drain
on resources for the finance and agreements teams, which sometimes have to
reopen billing and even modify agreements in order to recover our costs for the
trip, which the Economy Act requires us to do. So, **future travel may not be
approved for anyone with travel expenses that are more than 5 business days
outstanding.**

Back from your trip? Head on over to get
reimbursed!

========

[2] Get reimbursed › Brief overview of vouchers
source: travel-and-leave/travel-and-leave-policies/travel-guide-4-reimbursement | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-4-reimbursement.md | similarity: 0.77

You may be reimbursed for your expenses from official travel, or any other
approved expense paid for via personal funds (such as reimbursement for local
travel,
or professional liability
insurance
for supervisors) by creating a voucher in Concur.

You can get started by navigating to the **Vouchers** tab on top and selecting
**New Voucher**. If you do not yet have access to Concur, you can request it by
following these steps.

BEFORE YOU BEGIN: _did your dates of travel change such that they are in any way
outside of the original dates of your trip? If yes, STOP, and create an amended
authorization for the new
dates._

- Any travel that involves a flight, Amtrak, or is otherwise over 12 hours in
  duration is considered a **Voucher From
  Authorization**.
- For any local travel choose the **Local
  voucher**
  option. Ensure that an email from your authorizing
  official
  approving the expenses you intend to get reimbursed has been sent to
  tts-travelauths@gsa.gov.
- For any other reimbursement, like expenses unrelated to travel such as
  professional liability insurance or training materials, choose the
  **Miscellaneous
  voucher**
  option.

Once the voucher is created, the next step is to enter and edit expenses in the
**Expenses and Receipts** tab of the voucher. Find out how to add, edit, and
delete
expenses

Different types of expenses have different requirements. Some can be claimed
without further action needed, while others require receipts and/or a brief
justification. Review requirements for different types of
expenses.

Finally, don't forget to stamp and submit for travel team
approval!
Your voucher will be reviewed in 3-5 business days, and reimbursement will be
credited to your bank account and travel card 3-5 business days after approval.

Confused by error messages?

Have issues with reimbursements or outstanding travel card
balances?

========

[3] Frequently Asked Questions › Questions about reimbursement › Issues with reimbursement
source: travel-and-leave/travel-and-leave-policies/travel-guide-faq | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-faq.md | similarity: 0.75

My reimbursement never arrived!
If it has been over a week after your voucher has been approved and your
reimbursement hasn't arrived (whether to your travel card account or personal
account), contact kc-travel.finance@gsa.gov and describe the issue you are
having. cc tts-travel@gsa.gov.

How do I amend my voucher after it is approved?
To amend a voucher, go to the **Vouchers** tab of Concur, then click on the
voucher number you want to view and choose **Amend voucher**. Provide a brief
reason for the amendment, then proceed with
adding your revised expenses and
resubmitting for approval.
Note that if you want to revise a voucher that has not yet been approved, you
can simply **Edit Voucher** instead of amending.

**Note:** Vouchers should NOT be amended in the case of revising the payment
method (IBA to CASH or
vice versa,
or reducing a claim on an already-approved expense. If you were over-reimbursed
for something, you will need to mail a check for that amount, made out to GSA to
the following address:

USDA-OCFO Financial Operations & Disbursement Branch Attn: Bryan DeLeve - 2SE
2300 Main Street Kansas City, MO 64108

Reference the authorization and voucher number along with the payment.

========

[4] Frequently Asked Questions › Questions about securing approvals › How to Stamp and Submit for Travel Team Approval
source: travel-and-leave/travel-and-leave-policies/travel-guide-faq | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-faq.md | similarity: 0.75

...from your authorizing official. Ensure this is complete by 3:30 PM Eastern, else your travel will not be approved until the next business day. If you require approval after business hours, see the guide for after-hours and emergency travel here.

\*For vouchers, your travel will be approved within 3-5 business days.

6. Once you have been approved by the TTS travel team, you should receive a
   notification from Concur. Please note that in most cases, **government
   contract airfare does not ticket until 72 hours before departure**, so you
   may not receive official confirmation of your itinerary until then. Don't
   worry about this, the TTS travel team is not aware of any situations where
   approved travelers have not been issued tickets :)

\*For vouchers, reimbursement will be issued to your personal account and travel
card 3-5 business days after travel team approval. For issues with
reimbursement, read on more here

Once your authorization is approved and ticketed, you might want to take a look
at what to expect while
traveling!

========

[5] TTS Travel 101 › Brief overview of how to travel
source: getting-started/classes/travel-101 | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/travel-101.md | similarity: 0.73

2. Actually travel
Keep travel card policies and reimbursement rules as you
travel, so you'll know the right times to use your GSA travel card and which
receipts you need to keep with you.

3. File your voucher and get reimbursed
Now it's time to get reimbursed for your travel by filing your
voucher. You can also get reimbursed for other things via this method, such as
local travel or, for supervisors, professional liability
insurance.

**For unusual travel situations, there are a few additional guides to be aware
of:**

- Re-booking and changing official travel
  plans
- After hours and emergency
  travel
- Combining official and personal travel, including extensions at personal
  expense,
  and travel to and from cities other than one's home location and
  worksite.
- Traveling for multiple
  projects
- Issues with
  reimbursement
```
</details>

## q18 (single)

**Question:** I am taking a personal trip abroad. What do I have to do when I get back?

**Reference answer:** Complete the Foreign Travel De-briefing form within five days of returning.

**Agent's answer:**

> Within five days of your return from personal foreign travel, you must complete the Foreign Travel De-briefing form [Unofficial Foreign Travel › Reporting Personal Foreign Travel]. If you experience any issues with the form, you should email threat-management-office@gsa.gov [Unofficial Foreign Travel › Reporting Personal Foreign Travel].
> 
> *Note: The handbook is a snapshot from June 2026; please confirm this process with People Ops or the Threat Management Office.*

<details><summary>Retrieved passages</summary>

```text
[1] Unofficial Foreign Travel › Reporting Personal Foreign Travel › Before You Go
source: travel-and-leave/travel-and-leave-policies/unofficial-foreign-travel | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/unofficial-foreign-travel.md | similarity: 0.76

1. Complete the Foreign Travel Notification Form. If you have issues with the form, please email threat-management-office@gsa.gov.
2. Learn about your destination at the State Department’s Travel Advisory page.
3. Review training material and foreign travel training slides

**\*Note:** If the location you are planning to travel to is currently listed as a Travel Advisory Level 4, you **must** contact threat-management-office@gsa.gov to schedule a one-on-one travel briefing.

========

[2] Unofficial Foreign Travel › Reporting Personal Foreign Travel
source: travel-and-leave/travel-and-leave-policies/unofficial-foreign-travel | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/unofficial-foreign-travel.md | similarity: 0.74

When You Return
1. Within five days of your return from foreign travel, complete the Foreign Travel De-briefing form. If you have issues with the form, please email threat-management-office@gsa.gov.

For More Information
This information is derived from the GSA Insite page, Report your foreign travel. Please refer to that page for more information and the most up-to-date resources.

========

[3] Updated Travel Guidance for GSA Employees (07/13/2021)
source: travel-and-leave/july-13-travel-guidance | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/july-13-travel-guidance.md | similarity: 0.71

GSA continues to adjust to the changing COVID-19 pandemic status. Effective
immediately as of July 13, any requests for travel must be mission critical,
time sensitive and required to perform essential duties. The employee’s
authorizing official (AO) is responsible for making the determination if travel
requests meet that threshold. Of note:

- Travel should not occur if the requirement can be met using virtual
  technology.
- Only the minimum number of employees required to meet the urgent need should
  travel.
- Travelers should work with administrative and budget staff in their
  organization to ensure any personal protective equipment (PPE) needed for
  travel is available before travel occurs.

All travel for conferences, related events and training do not meet this
requirement and are not authorized. Additional details regarding the new travel
threshold are included in
this guidance.

========

[4] What to consider while traveling › Don't forget about vouchers!
source: travel-and-leave/travel-and-leave-policies/travel-guide-3-travel | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-3-travel.md | similarity: 0.70

Have a good trip, get
reimbursement--
filling out a voucher-- within 5 business days of getting back.

Why the rush? Filling out a voucher correctly allows you to:

1. Get reimbursed for your M&IE and for any hotels, airplane tickets, or other
   expenses you paid for personally.

2. Have the government automatically pay off the balance on your Travel Card. If
   you do your voucher correctly and on time, you will never have to worry about
   paying one of those bills yourself.

On the other side, when travel expenses are submitted late, it’s a major drain
on resources for the finance and agreements teams, which sometimes have to
reopen billing and even modify agreements in order to recover our costs for the
trip, which the Economy Act requires us to do. So, **future travel may not be
approved for anyone with travel expenses that are more than 5 business days
outstanding.**

Back from your trip? Head on over to get
reimbursed!

========

[5] Going out of office › Your overall responsibilities › Notifying GSA of international travel, for security clearance holders
source: travel-and-leave/going-out-of-office | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/going-out-of-office.md | similarity: 0.69

If you are traveling internationally and hold a security clearance, you are required to notify GSA. Follow the guidance on international travel for clearance holders in InSite. This notification is optional if you do not hold a clearance.
```
</details>

## q19 (single)

**Question:** Can I connect my personal laptop to the GSA network when I am in a GSA office?

**Reference answer:** No. Only approved smartphones and tablets can connect; personal laptops cannot connect directly to the GSA network at any GSA facility.

**Agent's answer:**

> No, personal laptops cannot be connected directly to the GSA network at any GSA facility [Equipment › Laptop › Bring Your Own Device (BYOD)].
> 
> This handbook is a snapshot from June 2026; please confirm with HR or IT.

<details><summary>Retrieved passages</summary>

```text
[1] Equipment › Laptop › Bring Your Own Device (BYOD)
source: getting-started/equipment | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/equipment.md | similarity: 0.79

GSA has implemented a BYOD policy
that allows users to connect their non-GSA procured mobile devices, which have
been previously approved by IT security, to GSA resources in a native fashion,
utilizing the GSA network. Please note, only approved smartphones and tablets
can be connected to the GSA network. Personal laptops cannot be connected
directly to the GSA network at any GSA facility. For more information, please
reference Section 4.2 of the
IT Security Procedural Guide.

For users who work on a FISMA system that wish to use their personal
laptop/computer (at a non-GSA facility), the assigned ISSO/ISSM for the
application must accept the associated risk(s), obtain approval from the
Authorizing Official, and document the use of the personally owned computer
within the System Security Plan (SSP).

For users who do not work directly on a FISMA system who wish to use their
personal machine (at a non-GSA facility), please consult with
ispcompliance@gsa.gov to review the BYOD policy with regards to your specific
needs and use cases. You can also post general questions in the
AskIT Chatter Page.

**Controlled Unclassified Information (CUI) can never be stored on a personal
machine. Utilize Government Furnished Equipment (GFE) to the maximum extent
possible.**

========

[2] Equipment › Laptop
source: getting-started/equipment | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/equipment.md | similarity: 0.73

MacBook Operating System
Your MacBook will come preloaded with the latest, GSA-approved/supported
operating system. Please wait to do any operating system upgrades (including
patches) until notified by GSA IT.

If you encounter any issues with your MacBook's local password (required when downloading OS updates), contact GSA IT and they can help you reset your password with a recovery key.

Rules
**Lock your computer before leaving it.** Press the **Control + Shift + Power**
keys on newer MacBooks or **Control + Shift + Eject** on older MacBooks with
optical drives.

**Encrypt all portable media that will connect to any TTS system.** You can
apply FileVault encryption to removable USB drives and external hard drives by
right-clicking the drive on your desktop and clicking **Encrypt**. You must
choose a strong password you can remember, as your drive will require the
password to mount and retrieve data once encrypted.

**GSA IT manages software updates.** You should not install updates or major
version upgrades yourself. You are responsible for applying updates and
restarting only when a GSA notification appears on your device.

========

[3] Updated Travel Guidance for GSA Employees (07/13/2021)
source: travel-and-leave/july-13-travel-guidance | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/july-13-travel-guidance.md | similarity: 0.69

GSA continues to adjust to the changing COVID-19 pandemic status. Effective
immediately as of July 13, any requests for travel must be mission critical,
time sensitive and required to perform essential duties. The employee’s
authorizing official (AO) is responsible for making the determination if travel
requests meet that threshold. Of note:

- Travel should not occur if the requirement can be met using virtual
  technology.
- Only the minimum number of employees required to meet the urgent need should
  travel.
- Travelers should work with administrative and budget staff in their
  organization to ensure any personal protective equipment (PPE) needed for
  travel is available before travel occurs.

All travel for conferences, related events and training do not meet this
requirement and are not authorized. Additional details regarding the new travel
threshold are included in
this guidance.

========

[4] Online Learning University
source: training-and-development/olu | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/training-and-development/olu.md | similarity: 0.68

GSA's Online University (OLU) is the home for
mandatory trainings, as well as recommended and optional
training opportunities for GSA employees.

========

[5] Unofficial Foreign Travel › Reporting Personal Foreign Travel › Before You Go
source: travel-and-leave/travel-and-leave-policies/unofficial-foreign-travel | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/unofficial-foreign-travel.md | similarity: 0.68

1. Complete the Foreign Travel Notification Form. If you have issues with the form, please email threat-management-office@gsa.gov.
2. Learn about your destination at the State Department’s Travel Advisory page.
3. Review training material and foreign travel training slides

**\*Note:** If the location you are planning to travel to is currently listed as a Travel Advisory Level 4, you **must** contact threat-management-office@gsa.gov to schedule a one-on-one travel briefing.
```
</details>

## q20 (single)

**Question:** What are the rules for the passcode on my work iPhone?

**Reference answer:** It must be longer than 14 characters, contain letters and numbers, and be known only to you.

**Agent's answer:**

> The passcode on your work iPhone must be longer than 14 characters and contain both letters and numbers [Equipment › Phone › Rules]. Additionally, the code should be known only to you [Equipment › Phone › Rules].
> 
> *Note: This handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Equipment › Phone › Rules
source: getting-started/equipment | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/equipment.md | similarity: 0.75

- **Change the phone's passcode.** It must be longer than 14 characters and
  contain both letters and numbers. The code should be known only to you.
- **Activate
  Find My iPhone.** If
  you're on an Android phone, activate
  Android Device Manager.
- **You are responsible for applying software updates.** When you receive a
  notification that an update is available, you should apply the update as soon
  as possible.
- After GSA IT provisions your phone, set up two-factor verification:

- If you don't have access to HR
    Links,
    email hspd12.security@gsa.gov and ask them
    to add your work cell phone number (which you may or may not have) and your
    personal cell phone number to your GSA Credential and Identity Management
    System (GCIMS) profile.
  - Once you have access to HR
    Links,
    you can update your contact information there. You'll find it under
    **Navigator > Employee Self Service > View/Update My Personal Info > Phone
    Number Change (USF)**; make sure to set the phone type as "Business Mobile"
    so it correctly populates in the GCIMS and works for 2FA.
  - You can learn more about using your phone for two-factor authentication in
    our Slack, GitHub, and
    Gmail guides. For two-factor authentication with
    these applications, you can use SMS, or
    Google Authenticator.

- **You can set up email using the Gmail app or Apple's default Mail app**
  - For the Gmail app: follow the directions in section 7 of the Self Help Guide for iPhone Setup
  - For Apple's default Mail app: you will need to
    generate an App Password
    in your Google account to use with your Mail app, instead of your normal email
    password.

========

[2] Equipment › Laptop
source: getting-started/equipment | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/equipment.md | similarity: 0.68

MacBook Operating System
Your MacBook will come preloaded with the latest, GSA-approved/supported
operating system. Please wait to do any operating system upgrades (including
patches) until notified by GSA IT.

If you encounter any issues with your MacBook's local password (required when downloading OS updates), contact GSA IT and they can help you reset your password with a recovery key.

Rules
**Lock your computer before leaving it.** Press the **Control + Shift + Power**
keys on newer MacBooks or **Control + Shift + Eject** on older MacBooks with
optical drives.

**Encrypt all portable media that will connect to any TTS system.** You can
apply FileVault encryption to removable USB drives and external hard drives by
right-clicking the drive on your desktop and clicking **Encrypt**. You must
choose a strong password you can remember, as your drive will require the
password to mount and retrieve data once encrypted.

**GSA IT manages software updates.** You should not install updates or major
version upgrades yourself. You are responsible for applying updates and
restarting only when a GSA notification appears on your device.

========

[3] Conduct and norms › Codes of conduct
source: about-us/centers-of-excellence/operations/conduct-and-norms | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/about-us/centers-of-excellence/operations/conduct-and-norms.md | similarity: 0.63

As employees of GSA, FAS, and TTS we are required to adhere to these codes of conduct:

- GSA Information Technology (IT) General Rules of Behavior
- TTS Code of Conduct
- TTS Slack Code of Conduct

If you have a question about the codes of conduct, reach out to your supervisor.

========

[4] Work schedules › Definitions
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.60

**Work schedule**: the days and hours per week you are expected to work.

**Base schedule**: This is a template of your work schedule: it lives in HRLinks and is associated with you. You set up a base schedule during onboarding.

- Having a base schedule ensures that if there are any errors made during bi-weekly timesheet approval, you will still get paid. (i.e. payroll will default to paying you for what is listed on your base schedule).
- This also makes timesheets easier for many folks: your base schedule is “applied” each pay period, auto-populating how many hours you worked.
- For some flexible schedules, you will need to review and edit how many hours you worked each day, since your hours will be variable. More on that below!

**Work days**: everyone in TTS works a Monday - Friday schedule, so for the purposes of this Handbook page, we are talking about Monday - Friday as possible workdays.

**Pay period**: every full-time employee in TTS works 80 hours in a two week pay period. Pay period start/end dates can be found on GSA’s payroll calendars page.

========

[5] Conferences, events, and training › Remote working guidance
source: training-and-development/conferences-events-training | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/training-and-development/conferences-events-training.md | similarity: 0.60

When working from somewhere that isn't your usual duty location, consider these
tips to help coworkers and partners plan
around your trip.
```
</details>

## q21 (single)

**Question:** How far in advance should I submit a leave request?

**Reference answer:** At least three business days in advance.

**Agent's answer:**

> You should submit leave requests at least three business days in advance [Going out of office › Your overall responsibilities].
> 
> *Note: This handbook is a snapshot from June 2026; please confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Going out of office › Your overall responsibilities
source: travel-and-leave/going-out-of-office | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/going-out-of-office.md | similarity: 0.74

You must report to work or have an approved leave request in HR Links, every scheduled work day. You are also responsible for submitting your timesheet at the end of every pay period.

You should submit leave requests at least three business days in advance, and make timely edits if your plans change.

For unplanned leave \- such as a sudden illness or a family emergency \- do what you can to contact your supervisor, and they can help manage the rest on your behalf.

Some types of leave require supporting documentation: it is your responsibility to submit all necessary documents and check that you’ve received approval.

========

[2] Conferences, events, and training › Approval timelines
source: training-and-development/conferences-events-training | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/training-and-development/conferences-events-training.md | similarity: 0.71

The review and approval process times vary by the type of request and the layers
of approval required. It is best to submit your
training request
as early as possible.

- Five days to ten days in advance for:
  - Training (not at a conference) that costs less than $2,500, including travel
- Ten days to two weeks
  - Conference events that cost less than $2500, including travel
- Fifteen days to three weeks in advance for:
  - Training (not at a conference) that costs more than $2500, including travel
- Three to five weeks in advance for:
  - Conference events that costs more than $2,500, including travel
  - Conference events that have a waived or discounted registration fee
  - Speaking events in your official capacity
  - Internal Management Meetings, regardless of cost
  - Highly Attended Events; a TTS-wide email will be sent to gather information about certain events that are expected to generate a lot of interest
- Five to six weeks in advance for:
  - Group Conference Training/Attendance

You can
track the status of your request
with the request number in the subject line of the automated email.

========

[3] Advanced sick leave › Getting approval for advanced sick leave
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.69

To get approval for advanced sick leave, you will need to submit the following paperwork to your supervisors and your OHRM Workforce Relations HR Specialist. Note: we suggest drafting all 4 pieces of paperwork and sending them to your HR Specialist for review _before_ routing for official signatures in Docusign.

1. Advanced Sick Leave Request form. Your supervisor can complete and route this form for you, if needed.
2. An original medical certification signed by your physician or practitioner.
3. A copy of your timesheet report for the current and previous year. Your supervisor can pull a timesheet report for you, if needed.
4. A written explanation of the circumstances which have caused your sick leave to be exhausted. Include how many hours you are requesting. Your supervisor can write this explanation for you, if needed.

When routing for signatures, you can use the Docusign template for the Advanced Sick Leave Request to fill out the form and request the right signatures.

Your supervisors should keep signed copies for their records.

========

[4] Benefits › Leave
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.69

Please use HR Links to request sick
leave and annual leave. For any leave-related questions, please contact
cpc.benefits-retirement@gsa.gov.

For more information on Leave, including sick, funeral, unpaid, parental,
advanced, and religious, please reference the Leave page.

========

[5] Leave types
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.69

Current employees can use this leave comparison chart.

Before you take leave, check out of office expectations.
```
</details>

## q22 (single)

**Question:** How long do I need to be at my current GS level before I can apply for a promotion to the next grade?

**Reference answer:** One year (the time-in-grade requirement), met within 30 days of the job posting's closing date.

**Agent's answer:**

> For Merit Promotion roles, you must be at your current GS level for one year to apply for a position at the next highest GS level [Promotions › Introduction to the Merit Promotion process]. This is known as the "time-in-grade" requirement, and you must meet this requirement within 30 days of the application’s closing date [Promotions › Introduction to the Merit Promotion process].
> 
> *Note: This handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Promotions › Introduction to the Merit Promotion process
source: hiring-staying-or-changing-jobs/promotions | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/promotions.md | similarity: 0.81

Before going into the process, it’s important to note that “promotions” in the
traditional sense (private sector) do not exist within the federal government.
Government has a position-driven view; everything begins with the need, not the
person. This means that a position is not created and filled for the purpose of
someone attaining a higher GS level.

Instead, the organization identifies a need for a higher level position due to
the type of work that must be accomplished and can choose to fill that need
through multiple recruitment or staffing methods, including the Merit Promotion
process.

> "One avenue of recruitment is through GSA's merit staffing process. GSA's
> Merit Promotion Plan contains the requirements for filling vacancies through
> internal competition, i.e., filling from existing GSA and other eligible staff
> (i.e. federal employees in other agencies). Merit promotion procedures provide
> a fair and systematic means of identifying, considering, and selecting GSA and
> other eligible candidates for promotions and career opportunities based on the
> Merit Principles."

As you can see from the above excerpt from GSA’s policy, the Merit Promotion
process is for "filling vacancies through internal competition". The Merit
Promotion process increases visibility of opportunities within TTS and creates
an avenue for other competitive service federal employees to join TTS.

For all Merit Promotion roles: employees must be at their current GS level for
one year in order to apply for a position at the next highest GS level. This is
called the “time-in-grade” requirement, and an applicant must meet time-in-grade
within 30 days of an application’s closing date.

========

[2] Promotions
source: hiring-staying-or-changing-jobs/promotions | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/promotions.md | similarity: 0.76

This page provides an overview of the Merit Promotion process for both
Competitive Service (Career) and Excepted Service positions.

========

[3] Hiring › Promotions
source: hiring-staying-or-changing-jobs/hiring | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/hiring.md | similarity: 0.74

"Promotions" in the traditional, private sector sense do not exist within the
federal government. The \Promotions Handbook page
explains Merit Promotions for both Competitive Service (Career) and Excepted
Service positions.

========

[4] Internal hiring and internal TTS details › What is internal hiring?
source: hiring-staying-or-changing-jobs/assignee-detail | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/assignee-detail.md | similarity: 0.70

Internal hiring actions are not posted to USAJobs. These hiring actions include reassignments, details, and temporary promotions.

A reassignment is a permanent, lateral transfer to a new TTS office at the same GS level.

A detail is a temporary assignment to a different position or a different office/business unit. Details last up to 120 days and can be extended up
to another 120 days (not to exceed 240 days total), provided that:

- The detailee, their temporary supervisor, and the employee’s permanent supervisor all agree.
- The employee is detailed at the same (or lower) GS level.

If the detail is to a higher GS level, then it is considered a temporary promotion and cannot exceed 120 days due to federal policy and bargaining unit (union) contracts. If someone is selected for a temporary promotion, OHRM will need to review their resume for qualifications.

========

[5] Moving and changing your address › Changes in pay
source: travel-and-leave/travel-and-leave-policies/moving | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/moving.md | similarity: 0.69

If you are moving to a new region, your pay may change. Look up your new pay via
OPM's GS Locality Pay Tables.
Check that you are in the current year, find your region under the pay table,
and then find your step and grade. That’s what you’ll be paid in your new
location.
```
</details>

## q23 (multi)

**Question:** How much sick leave do I earn per pay period, and how many sick days can I use for family care before I need to apply for FMLA?

**Reference answer:** 4 hours per pay period; up to 13 days a year for family care and bereavement, and beyond 13 days you can apply for FMLA.

**Agent's answer:**

> All federal employees accrue four hours of sick leave per pay period [Leave types › Types of leave › Sick leave].
> 
> You can use up to 13 days of sick leave per year for family health needs and bereavement [Leave types › Types of leave › Sick leave]. If you need to take more than 13 days for your own care or caregiving reasons, you can apply for FMLA [Family Medical Leave Act (FMLA) › How FMLA works › FMLA for caregiving and health reasons]. Additionally, if you need more than 13 sick days at once to care for a loved one, you can apply for FMLA status [Leave types › Types of leave].
> 
> *This handbook is a snapshot from June 2026; please confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
Tool error: Error executing tool search

Tool error: Error executing tool search

[1] Leave types › Types of leave › Sick leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.75

You can use Sick Leave for:

- Doctor and medical appointments for you or a family member
- Mental health care
- Recovering from illness, for you or a family member
- Any other health need

All federal employees, no matter how long they have worked in government, accrue four hours of sick leave per pay period. There is no maximum amount of sick leave you can accrue, and if you've transferred to TTS from another federal agency, your accrued sick leave will transfer with you.

You can use sick leave for your physical and mental health needs. You can also use up to 13 days of sick leave per year for family health needs and bereavement.

========

[2] Advanced sick leave
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.72

You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

For example: You have one year left on your term, which equals to 26 pay periods. You earn 4 sick leave hours per pay period. You will earn 104 more sick leave hours (26 pay periods x 4 hours per pay period). Therefore, you can request up to 104 advanced sick leave hours.

========

[3] Leave types › Types of leave › Annual leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.71

You may use annual leave for any reason. Annual leave accrues based on how long you’ve worked for the federal government:

- Fewer than 3 years: 4 hours per pay period
- Between 3 and 15 years: 6 hours per pay period
- 15+ years: 8 hours per pay period

Your leave increases on the first full pay period following your work anniversary. You can refer to either HR Links or the bottom of your paystub for your leave balances.

You can carry over a maximum of 240 annual leave hours, from one leave year to the next. If you’ve transferred to TTS from another federal agency, your accrued annual leave will transfer with you.

========

[4] Family Medical Leave Act (FMLA) › How FMLA works › FMLA for caregiving and health reasons
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.69

If you need to take more than 13 days (total accrued Sick Leave for a year) for your own care or caregiving reasons, you can apply for FMLA.

========

[5] Family Medical Leave Act (FMLA) › How FMLA works
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.68

You can use 12 unpaid weeks of FMLA every 52 weeks. The 12 weeks are rolling, and are refilled a year to the day you first went on FMLA status.

Each time you use FMLA, it counts toward the 12 week/480 hour allotment.

- For example: you went on FMLA for 4 weeks in March 2022 to care for a seriously ill family member, and you used your accrued Sick Leave in order to be paid during those 4 weeks. You will only have 8 weeks of FMLA available until March 2023\.

[1] Leave types › Types of leave › Sick leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.76

You can use Sick Leave for:

- Doctor and medical appointments for you or a family member
- Mental health care
- Recovering from illness, for you or a family member
- Any other health need

All federal employees, no matter how long they have worked in government, accrue four hours of sick leave per pay period. There is no maximum amount of sick leave you can accrue, and if you've transferred to TTS from another federal agency, your accrued sick leave will transfer with you.

You can use sick leave for your physical and mental health needs. You can also use up to 13 days of sick leave per year for family health needs and bereavement.

========

[2] Family Medical Leave Act (FMLA) › How FMLA works › FMLA for caregiving and health reasons
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.75

If you need to take more than 13 days (total accrued Sick Leave for a year) for your own care or caregiving reasons, you can apply for FMLA.

========

[3] Family Medical Leave Act (FMLA) › About FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.74

FMLA entitles you to take up to 12 weeks of _unpaid_ leave per 12 month period for the following:

- The birth or care of a child
- An adoption or foster care placement of a child
- The care of a spouse/son/daughter/parent with a serious health condition
- Your serious health condition
- Handling issues (“exigencies”) that arise when your spouse, child, or parent is on active duty in the Armed Forces.

You can take up to 26 weeks of unpaid FMLA to care for an ill servicemember or veteran, if you are their spouse, child, parent, or next of kin.

========

[4] Leave types › Types of leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.71

Family Medical Leave Act (FMLA)
If you need more than 13 sick days at once to care for a loved one, you can apply for Family Medical Leave Act (FMLA) status. Refer to the FMLA page for more, including applying for FMLA.

Paid Parental Leave
You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. Refer to the Paid Parental Leave page for more information, including requesting PPL.

========

[5] Advanced sick leave
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.68

You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

For example: You have one year left on your term, which equals to 26 pay periods. You earn 4 sick leave hours per pay period. You will earn 104 more sick leave hours (26 pay periods x 4 hours per pay period). Therefore, you can request up to 104 advanced sick leave hours.
```
</details>

## q24 (multi)

**Question:** I used 4 weeks of FMLA in the past year to care for my mother. How much paid parental leave can I still take, and how much FMLA will I have left?

**Reference answer:** PPL is implemented through FMLA, so the 4 weeks are subtracted: 8 weeks of PPL, and taking it uses up the remaining FMLA for the rolling 12 months.

**Agent's answer:**

> If you have used 4 weeks of FMLA in the past 12 months, you have 8 weeks of FMLA entitlement remaining. Because GSA implements Paid Parental Leave (PPL) via the Family and Medical Leave Act (FMLA), if you previously used FMLA within the past 12 months of your parental leave period, those hours are subtracted from the 12 weeks of PPL you can take [Family Medical Leave Act (FMLA) › How FMLA works › Paid Parental Leave and FMLA] [Paid parental leave (PPL) › About PPL]. Therefore, you would have 8 weeks of PPL available.
> 
> Please note that this handbook is a snapshot from June 2026 and you should confirm this with HR (TTS-PeopleOps@gsa.gov).

<details><summary>Retrieved passages</summary>

```text
[1] Family Medical Leave Act (FMLA) › How FMLA works › Paid Parental Leave and FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.81

You have to be eligible for FMLA to receive Paid Parental Leave (PPL). PPL is how the federal government implements FMLA for parental leave. This means you must have at least one year of federal service to use PPL. If you are a new federal employee, check out the recommendations for those who have less than 1 year of federal service.

If you use FMLA prior to PPL, it reduces the number of PPL hours you can receive (and vice versa). If you max out 12 weeks of PPL, that uses up all the FMLA you can use for the next 52 weeks.

========

[2] Family Medical Leave Act (FMLA) › About FMLA
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.79

FMLA entitles you to take up to 12 weeks of _unpaid_ leave per 12 month period for the following:

- The birth or care of a child
- An adoption or foster care placement of a child
- The care of a spouse/son/daughter/parent with a serious health condition
- Your serious health condition
- Handling issues (“exigencies”) that arise when your spouse, child, or parent is on active duty in the Armed Forces.

You can take up to 26 weeks of unpaid FMLA to care for an ill servicemember or veteran, if you are their spouse, child, parent, or next of kin.

========

[3] Leave types › Types of leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.79

Family Medical Leave Act (FMLA)
If you need more than 13 sick days at once to care for a loved one, you can apply for Family Medical Leave Act (FMLA) status. Refer to the FMLA page for more, including applying for FMLA.

Paid Parental Leave
You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. Refer to the Paid Parental Leave page for more information, including requesting PPL.

========

[4] Paid parental leave (PPL) › About PPL
source: travel-and-leave/paid-parental-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/paid-parental-leave.md | similarity: 0.77

- You are entitled to 12 weeks of paid time off for the birth, adoption or placement of a new child. It can be taken all at once or intermittently. (Supervisor approval is needed for the intermittent option).
- You must use the PPL within a year of the child’s birth or placement
- You need to have been a federal employee for 12 months in order to access Paid Parental Leave (note: most veterans are immediately eligible). If you are a new federal employee, check out the recommendations for those who have less than 1 year of federal service.
- You need to be approved for PPL before being able to use it.
- You will need to sign an agreement, stating that you will return to work for at least 12 weeks after your final day on PPL.
  - The 12 week agreement is in place regardless of how many weeks of PPL you take. If you take PPL intermittently, the 12 week period still begins after your _final_ day of PPL, even if you have been working in between periods of PPL.
- GSA implements PPL via Family and Medical Leave Act (FMLA) leave. If you previously used FMLA within the past 12 months of your parental leave period, those hours would be subtracted from the 12 weeks you can take for PPL.

========

[5] Paid parental leave (PPL)
source: travel-and-leave/paid-parental-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/paid-parental-leave.md | similarity: 0.74

TTS has paid parental leave (PPL) for the birth or placement (adoption or foster care) of a child.
```
</details>

## q25 (multi)

**Question:** I have used up all my sick leave because of a long illness. What are my options, and how much advanced sick leave can I ask for?

**Reference answer:** Advanced annual leave, advanced sick leave, or donated hours through the VLTP; up to 240 hours of advanced sick leave (term employees: up to what they will earn in the rest of their term).

**Agent's answer:**

> You can request up to 240 hours of advanced sick leave [Advanced sick leave] [Leave types › Types of leave]. If you are a term employee, you can request up to the total amount you will earn during the remainder of your term [Advanced sick leave].
> 
> Additionally, if you have a personal or family medical emergency and have exhausted your earned leave, you can enroll in the Voluntary Leave Transfer Program (VLTP), which allows colleagues to donate annual leave to you [Leave types › Types of leave]. To start this process, reach out to your Workforce Relations HR Specialist [Leave types › Types of leave]. You may also want to explore applying for the Family Medical Leave Act (FMLA) if you need to take leave for your own care or caregiving reasons [Family Medical Leave Act (FMLA) › How FMLA works › FMLA for caregiving and health reasons].
> 
> This handbook is a snapshot from June 2026; please confirm these options with People Ops (TTS-PeopleOps@gsa.gov).

<details><summary>Retrieved passages</summary>

```text
[1] Advanced sick leave
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.75

You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

For example: You have one year left on your term, which equals to 26 pay periods. You earn 4 sick leave hours per pay period. You will earn 104 more sick leave hours (26 pay periods x 4 hours per pay period). Therefore, you can request up to 104 advanced sick leave hours.

========

[2] Leave types › Types of leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.72

Taking advanced leave › Advanced sick leave
You can request up to 240 hours of advanced sick leave. If you are a term employee, you can request up to the total amount that you’ll earn during the rest of your term.

Refer to the advanced sick leave page for more information, including how to request it.

Using donated leave
If you have a personal or family medical emergency and have exhausted your earned leave, you can enroll in the Voluntary Leave Transfer Program (VLTP). Your colleagues can donate their annual leave for you. Reach out to your Workforce Relations HR Specialist to start the process.

========

[3] Leave types › Types of leave › Sick leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.72

You can use Sick Leave for:

- Doctor and medical appointments for you or a family member
- Mental health care
- Recovering from illness, for you or a family member
- Any other health need

All federal employees, no matter how long they have worked in government, accrue four hours of sick leave per pay period. There is no maximum amount of sick leave you can accrue, and if you've transferred to TTS from another federal agency, your accrued sick leave will transfer with you.

You can use sick leave for your physical and mental health needs. You can also use up to 13 days of sick leave per year for family health needs and bereavement.

========

[4] Advanced sick leave › Resources
source: travel-and-leave/advanced-sick-leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/advanced-sick-leave.md | similarity: 0.69

- Advanced Sick Leave
- GSA InSite: Advanced Leave

========

[5] Family Medical Leave Act (FMLA) › How FMLA works › FMLA for caregiving and health reasons
source: travel-and-leave/fmla | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/fmla.md | similarity: 0.67

If you need to take more than 13 days (total accrued Sick Leave for a year) for your own care or caregiving reasons, you can apply for FMLA.
```
</details>

## q26 (multi)

**Question:** I am on a Variable Week schedule and normally work 10 hours on Thursdays. If a holiday falls on a Thursday, how do I cover the missing hours, and how many credit hours can I keep saved?

**Reference answer:** You get 8 hours of holiday pay, so you make up the 2 hours another day or use annual leave, credit hours or comp time; you can hold up to 24 credit hours.

**Agent's answer:**

> If a holiday falls on a day you are scheduled to work more than 8 hours, such as your 10-hour Thursday, you receive 8 hours of holiday pay [Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Holidays and flexible schedules]. To cover the remaining 2 hours, you have the following options:
> 
> *   Make up the hours on a different day [Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Holidays and flexible schedules]
> *   Take annual leave [Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Holidays and flexible schedules]
> *   Use credit hours or comp time [Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Holidays and flexible schedules]
> 
> Regarding credit hours, you can have up to 24 credit hours accrued at any given time [Compensation for working extra hours › Credit hours, in flexible work schedules].
> 
> *This handbook is a snapshot from June 2026; please confirm these details with HR (TTS-PeopleOps@gsa.gov).*

<details><summary>Retrieved passages</summary>

```text
Tool error: Error executing tool search

Tool error: Error executing tool search

[1] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Types of flexible schedules › Variable Week
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.73

- Each day in the workweek can be slightly longer or shorter than 8 hours.
- Each week can be shorter/longer than 40 hours, as long as together, the two weeks add up to 80 hours for the pay period.
- You work 5 days a week.
- The maximum number of hours you can work in a single day is 12.

For example:
|**Day** |**Hours** | **Day** |**Hours** |

| Monday | 5 | Monday | 10 |
| Tuesday | 9 | Tuesday | 10 |
| Wednesday| 6 | Wednesday| 6 |
| Thursday | 9 | Thursday | 9 |
| Friday | 8 | Friday | 8 |
| **Week 1 Total**|**37** | **Week 2 Total**| **43** |

========

[2] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Holidays and flexible schedules
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.71

_This special note is for variable day, variable week, and maxiflex schedules._

If you are on a flexible schedule, you will receive 8 hours for a holiday. If you typically work more than 8 hours on a day which falls on a holiday, you have a few options:

- Make up the hours on a different day
- Take annual leave
- Use credit hours, or use comp time.

For example: you typically work 10 hours on Thursdays. December 25th falls on a Thursday. You are given 8 hours for the paid holiday, and you work 2 extra hours on Monday, December 22nd, to make up the difference.

========

[3] Compensation for working extra hours › Religious comp time, for everyone
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.64

Per OPM guidance, you can request an adjustment to your work schedule for religious observances, instead of using annual leave. In HR Links, this is treated as another kind of comp time.

Email your supervisor about the extra hours you plan to work before a religious observance.

========

[4] Leave types › Types of leave › Annual leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.62

You may use annual leave for any reason. Annual leave accrues based on how long you’ve worked for the federal government:

- Fewer than 3 years: 4 hours per pay period
- Between 3 and 15 years: 6 hours per pay period
- 15+ years: 8 hours per pay period

Your leave increases on the first full pay period following your work anniversary. You can refer to either HR Links or the bottom of your paystub for your leave balances.

You can carry over a maximum of 240 annual leave hours, from one leave year to the next. If you’ve transferred to TTS from another federal agency, your accrued annual leave will transfer with you.

[1] Compensation for working extra hours › Credit hours, in flexible work schedules
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.74

Only people on flexible work schedules can earn and use credit hours. There's no salary maximum for earning and using credit hours. To establish a flexible work schedule, talk with your supervisor.

You can then be approved for credit hours if you want to voluntarily work additional hours beyond your normal/approved schedule. If you are _required_ to work additional hours, you will receive overtime or comp time.

- You can have up to 24 credit hours accrued at any given time.

- The hours will roll over from one pay period to the next, and they never expire.

- Credit hours cannot be converted to cash unless you leave GSA (then they will be paid out).

Refer to OPM’s Credit Hours Fact Sheet for more detail.

========

[2] Compensation for working extra hours › Credit hours, in flexible work schedules › Credit hours mechanics
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.71

There are two steps to earning credit hours. First, request to work the additional time in HR Links under "Request Additional Time" on your timecard or "Additional Time Requests" on your Self-service page. Your supervisor will need to approve this (while you're establishing a flexible work schedule is a good time to discuss if or how to notify them outside of HR Links). Second, log the extra hours you worked on your timesheet using time reporting code 036 (Credit Hours Earned).

========

[3] Leave types › Types of leave › Annual leave › Use or Lose
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.67

Use or Lose is the number of annual leave hours you would forfeit at the end of the leave year, if you do not use any of your annual leave hours between now and then. As noted above, there is a 240 hour limit on the number of hours you can carry over from one leave year to the next. Use or Lose only applies to annual leave.

For example: You look in HRLinks and see "182 Hours (96 Hours Use or Lose)." Today, January 25th, 2022, you have 182 hours of annual leave available. If you continued to accrue annual leave for the rest of the year, and you did not use any of those hours, you would forfeit 96 hours of annual leave at the end of the year. You would be 96 hours over the 240 cap.

182 current hours \+ 154 more hours accrued throughout the year \= 336 hours.

336 hours \- 240 hour cap \= 96 Use or Lose hours that would be forfeited.

========

[4] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Standard schedule
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.65

You are scheduled to arrive and depart at the same time, every day that you work. The start/stop times do not change from one pay period to the next. You work 8 hours every day, for all 10 work days per pay period. By default, new TTS employees are on a standard schedule.

- Overtime and comp time: Yes - Can be approved for working more than 8 hours in a day.
- Holiday pay: Yes - You receive 8 hours of holiday pay for the time you were scheduled to work.
- Credit hours: No - Not available with this schedule

========

[5] Leave types › Types of leave › Award leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.65

Award leave is offered for End of Year Performance Awards and Special Act Awards.

- If you are eligible for an End of Year Performance Award, you can opt-in via HRLinks to receive Award Leave in lieu of a monetary award.
- If you are receiving a TTS Special Act Award, you will be notified and asked for your preference of award leave or a monetary award.

You can receive a maximum of 80 hours of award leave in a single fiscal year. If you receive a Special Act Award after hitting the 80 hour cap, your award will be monetary.

Award leave expires one year after it is issued. You must use it by the end of the pay period in which the expiration date falls. Expired award leave cannot be recovered \- please monitor your leave balances and consider using award leave first. If you leave TTS, award leave is not paid out.

You can check the amount of Award leave you have in HR Links. You may receive an automated email reminder from HR Links 3 months before your leave expires, even if you have already used it.

OPM Policy:

- Time-Off Awards
```
</details>

## q27 (multi)

**Question:** I am leaving TTS for a private company. Can I take leave on my last day, and what happens if I do not return my laptop?

**Reference answer:** The final day must be worked in full unless you worked most of your final pay period; if equipment is not returned, your final paycheck may be withheld.

**Agent's answer:**

> If you are leaving the federal government, your final day at TTS must be worked in full, unless you have worked the majority of your final pay period; then you are eligible to take leave for part of your final day [Leaving TTS & Offboarding › When it's time to leave TTS].
> 
> When you leave TTS, you are responsible for returning all TTS-issued equipment [Leaving TTS & Offboarding › When it's time to leave TTS › 6. Return your equipment]. Failure to do so may lead to your final paycheck being withheld until the equipment is returned [Leaving TTS & Offboarding › When it's time to leave TTS › 6. Return your equipment].
> 
> This handbook is a snapshot from June 2026; please confirm these details with HR.

<details><summary>Retrieved passages</summary>

```text
[1] Leaving TTS & Offboarding › When it's time to leave TTS
source: hiring-staying-or-changing-jobs/leaving-tts | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/leaving-tts.md | similarity: 0.72

1. Email notice of your resignation › Taking time off prior to your last day at TTS
If you are leaving the federal government, your final day at TTS must be worked
in full, unless you have worked the majority of your final pay period; then you
are eligible to take leave for part of your final day.

If you are taking a new role within the federal government, the above
restrictions do not apply.

2. Provide summary reviews for direct reports (Supervisors only)
If you are a supervisor and you are leaving within 120 days of the next review
period, you need to provide to your supervisor a summary review of each of the
employees that report into you. An employee's review needs to come from a
supervisor that they've worked under for 120 days.

- Midyear review: provide a written review
- Annual review: provide ratings based on position descriptions

========

[2] Leaving TTS & Offboarding › When it's time to leave TTS
source: hiring-staying-or-changing-jobs/leaving-tts | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/leaving-tts.md | similarity: 0.71

These steps apply to all TTS employees: permanent employees, term employees who
are at the end of their term, and term employees choosing to resign before their
term ends. These steps also apply to employees who will remain in federal
government and other GSA offices.
**Begin this process at least two weeks before your last day of work.**
Your last day at TTS cannot be a federal holiday.

========

[3] Going out of office › Your overall responsibilities
source: travel-and-leave/going-out-of-office | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/going-out-of-office.md | similarity: 0.68

You must report to work or have an approved leave request in HR Links, every scheduled work day. You are also responsible for submitting your timesheet at the end of every pay period.

You should submit leave requests at least three business days in advance, and make timely edits if your plans change.

For unplanned leave \- such as a sudden illness or a family emergency \- do what you can to contact your supervisor, and they can help manage the rest on your behalf.

Some types of leave require supporting documentation: it is your responsibility to submit all necessary documents and check that you’ve received approval.

========

[4] Leave types
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.68

Current employees can use this leave comparison chart.

Before you take leave, check out of office expectations.

========

[5] Leave types › Types of leave › Annual leave › Use or Lose
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.68

Use or Lose is the number of annual leave hours you would forfeit at the end of the leave year, if you do not use any of your annual leave hours between now and then. As noted above, there is a 240 hour limit on the number of hours you can carry over from one leave year to the next. Use or Lose only applies to annual leave.

For example: You look in HRLinks and see "182 Hours (96 Hours Use or Lose)." Today, January 25th, 2022, you have 182 hours of annual leave available. If you continued to accrue annual leave for the rest of the year, and you did not use any of those hours, you would forfeit 96 hours of annual leave at the end of the year. You would be 96 hours over the 240 cap.

182 current hours \+ 154 more hours accrued throughout the year \= 336 hours.

336 hours \- 240 hour cap \= 96 Use or Lose hours that would be forfeited.

[1] Leaving TTS & Offboarding › When it's time to leave TTS › 6. Return your equipment
source: hiring-staying-or-changing-jobs/leaving-tts | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/leaving-tts.md | similarity: 0.73

When you leave TTS, you are responsible for returning all TTS-issued equipment.
Failure to do so may lead to your final paycheck being withheld until the
equipment is returned.

========

[2] Equipment › Lost or stolen equipment
source: getting-started/equipment | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/equipment.md | similarity: 0.69

If TTS-issued equipment is lost or stolen, follow these mandatory steps.
Employees must follow the GSA procedures for lost or stolen equipment or missing
PIV cards, and alert TTS in the #equipment Slack channel:

Access card
See
InSite page.

Other
For lost work laptops, phones, etc., do the following as quickly as possible:

1. Follow the
   GSA-wide steps.
1. Inform your team.
   - Your access to various systems may need to be temporarily removed.
1. Inform the #equipment Slack channel.

If your equipment is returned to you, it may have been tampered with and should
not be used. Return the equipment to GSA IT so they can inspect it, and if
necessary, re-image it.

========

[3] Equipment › Laptop
source: getting-started/equipment | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/equipment.md | similarity: 0.68

MacBook Operating System
Your MacBook will come preloaded with the latest, GSA-approved/supported
operating system. Please wait to do any operating system upgrades (including
patches) until notified by GSA IT.

If you encounter any issues with your MacBook's local password (required when downloading OS updates), contact GSA IT and they can help you reset your password with a recovery key.

Rules
**Lock your computer before leaving it.** Press the **Control + Shift + Power**
keys on newer MacBooks or **Control + Shift + Eject** on older MacBooks with
optical drives.

**Encrypt all portable media that will connect to any TTS system.** You can
apply FileVault encryption to removable USB drives and external hard drives by
right-clicking the drive on your desktop and clicking **Encrypt**. You must
choose a strong password you can remember, as your drive will require the
password to mount and retrieve data once encrypted.

**GSA IT manages software updates.** You should not install updates or major
version upgrades yourself. You are responsible for applying updates and
restarting only when a GSA notification appears on your device.

========

[4] Going out of office › Your overall responsibilities
source: travel-and-leave/going-out-of-office | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/going-out-of-office.md | similarity: 0.60

You must report to work or have an approved leave request in HR Links, every scheduled work day. You are also responsible for submitting your timesheet at the end of every pay period.

You should submit leave requests at least three business days in advance, and make timely edits if your plans change.

For unplanned leave \- such as a sudden illness or a family emergency \- do what you can to contact your supervisor, and they can help manage the rest on your behalf.

Some types of leave require supporting documentation: it is your responsibility to submit all necessary documents and check that you’ve received approval.
```
</details>

## q28 (multi)

**Question:** When are the FY25 end-of-year performance awards issued, and if I pick award leave instead of money, what is the most I can get and how long do I have to use it?

**Reference answer:** Around December 10, 2025 (budget permitting); at most 80 hours of award leave per fiscal year, which expires one year after it is issued.

**Agent's answer:**

> FY25 performance awards are targeted to be issued on December 10, 2025, though this date is approximate and depends on budget availability [Performance Management Important Dates › End of year performance review important dates].
> 
> Regarding award leave:
> 
> *   **Maximum amount:** You can receive a maximum of 80 hours of award leave in a single fiscal year [Leave types › Types of leave › Award leave]. Depending on your summary rating, the specific amount of time off you may be eligible for is up to 80 hours (Level 5), up to 44 hours (Level 4), or up to 8 hours ("High 3" summary rating) [Performance Management Overview › Who participates in the end of year performance review? › Who is eligible for the end of year performance bonus?].
> *   **Time limit:** Award leave expires one year after it is issued [Leave types › Types of leave › Award leave]. You must use it by the end of the pay period in which the expiration date falls, and it cannot be recovered if it expires [Leave types › Types of leave › Award leave].
> 
> This handbook is a snapshot from June 2026; please confirm these details with HR.

<details><summary>Retrieved passages</summary>

```text
[1] Performance Management Important Dates › End of year performance review important dates
source: performance-management/dates | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/performance-management/dates.md | similarity: 0.75

| Date                 | Item                                                                                                 |

| September 30, 2025   | End of FY25 performance cycle                                                                        |
| October 1, 2025      | Internal ask for employees to begin their self-assessment                                            |
| October 17, 2025     | Self-assessment submittal due date                                                                   |
| October 20, 2025     | Audit of employee self-assessment completion                                                         |
| Oct 23 - Nov 7, 2025 | Supervisors hold 1:1 performance review meetings with their direct reports                           |
| November 10, 2025    | TTS internal due date to close out FY25 performance plans in HR Links (if not completed during 1:1s) |
| November 14, 2025    | Official GSA due date to close out FY25 performance plans in HR Links                                |
| November 14, 2025    | Official GSA due date to establish FY26 performance plans in HR Links                                |
| December 10, 2025    | FY25 Performance Awards will be issued (approximate date, budget permitting)                         |

========

[2] Performance Management Overview › Who participates in the end of year performance review? › Selecting award preference in HR Links
source: performance-management/index | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/performance-management/index.md | similarity: 0.74

If you are eligible for an end-of-year individual performance award (cash or
time-off), **please make a selection no later than November 15th.** If you would
like to keep the same selection type as the previous fiscal year, no further action is needed.

- **Monetary award:** This is the default option in HR Links. No action is
  needed in HR Links **unless you specified award time off for the prior review
  cycle**

- To change from **LEAVE** to **CASH**, you need to change your “Time Off
    Award Preference” to **“Inactive”** and you must then use the **“Save”**
    button.
  - **_Note:_** These
    instructions
    show where to make the change in HR Links

- **Award leave:** If you would like to select award time off in lieu of a
  monetary award, please follow
  these instructions.

========

[3] Performance Management Overview › Who participates in the end of year performance review? › Who is eligible for the end of year performance bonus?
source: performance-management/index | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/performance-management/index.md | similarity: 0.74

Employees who occupy eligible positions as of September 30, of the current fiscal year, and who
receive an eligible rating of record, may receive an Individual Performance
Award (IPA). “Ratings of Record (Annual)” should be completed in HR Links by
November 14, or that employee may not receive their award timely.

Subject to the availability of funds, OCFO and OHRM plan to distribute IPAs as
follows:

- **Level 5 summary ratings:** Up to 3.85% of adjusted basic pay, or up to 80
  hours of time off, subject to budget availability.
- **Level 4 summary ratings:** Up to 2.1% of adjusted basic pay, or up to 44
  hours of time off subject to budget availability.
- **"High 3" summary ratings:** Up to 0.385% of adjusted basic pay, or up to 8
  hours of time off subject to budget availability for employees who receive a
  Level 3 summary rating with one or more critical elements weighted 15% or
  greater, rated at Level 4 or Level 5.

The final award percentages for Level 5, Level 4 and Level 3 summary ratings
will be determined **when all performance reviews are complete**. In the event
the above targets for the Level 3, Level 4 and Level 5 summary ratings cannot be
met due to budget constraints, the percentage payouts for awards will be
decreased proportionally. Summary ratings are not an average score —
they are assigned as defined on InSite.

IPAs are targeted to be **paid out in December**, as in previous years.
However, the IPA payout date depends upon the status of the Continuing
Resolution and fiscal year funding funding.

========

[4] Leave types › Types of leave › Award leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.73

Award leave is offered for End of Year Performance Awards and Special Act Awards.

- If you are eligible for an End of Year Performance Award, you can opt-in via HRLinks to receive Award Leave in lieu of a monetary award.
- If you are receiving a TTS Special Act Award, you will be notified and asked for your preference of award leave or a monetary award.

You can receive a maximum of 80 hours of award leave in a single fiscal year. If you receive a Special Act Award after hitting the 80 hour cap, your award will be monetary.

Award leave expires one year after it is issued. You must use it by the end of the pay period in which the expiration date falls. Expired award leave cannot be recovered \- please monitor your leave balances and consider using award leave first. If you leave TTS, award leave is not paid out.

You can check the amount of Award leave you have in HR Links. You may receive an automated email reminder from HR Links 3 months before your leave expires, even if you have already used it.

OPM Policy:

- Time-Off Awards

========

[5] End of Year Performance Management HRLinks Steps › Selecting Time Off Award in lieu of cash performance award
source: performance-management/end-of-year/hrlinks-steps | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/performance-management/end-of-year/hrlinks-steps.md | similarity: 0.71

Information will be updated pending guidance from GSA.

[1] Leave types › Types of leave › Award leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.79

Award leave is offered for End of Year Performance Awards and Special Act Awards.

- If you are eligible for an End of Year Performance Award, you can opt-in via HRLinks to receive Award Leave in lieu of a monetary award.
- If you are receiving a TTS Special Act Award, you will be notified and asked for your preference of award leave or a monetary award.

You can receive a maximum of 80 hours of award leave in a single fiscal year. If you receive a Special Act Award after hitting the 80 hour cap, your award will be monetary.

Award leave expires one year after it is issued. You must use it by the end of the pay period in which the expiration date falls. Expired award leave cannot be recovered \- please monitor your leave balances and consider using award leave first. If you leave TTS, award leave is not paid out.

You can check the amount of Award leave you have in HR Links. You may receive an automated email reminder from HR Links 3 months before your leave expires, even if you have already used it.

OPM Policy:

- Time-Off Awards

========

[2] Performance Management Overview › Who participates in the end of year performance review? › Selecting award preference in HR Links
source: performance-management/index | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/performance-management/index.md | similarity: 0.72

If you are eligible for an end-of-year individual performance award (cash or
time-off), **please make a selection no later than November 15th.** If you would
like to keep the same selection type as the previous fiscal year, no further action is needed.

- **Monetary award:** This is the default option in HR Links. No action is
  needed in HR Links **unless you specified award time off for the prior review
  cycle**

- To change from **LEAVE** to **CASH**, you need to change your “Time Off
    Award Preference” to **“Inactive”** and you must then use the **“Save”**
    button.
  - **_Note:_** These
    instructions
    show where to make the change in HR Links

- **Award leave:** If you would like to select award time off in lieu of a
  monetary award, please follow
  these instructions.

========

[3] End of Year Performance Management HRLinks Steps › Selecting Time Off Award in lieu of cash performance award
source: performance-management/end-of-year/hrlinks-steps | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/performance-management/end-of-year/hrlinks-steps.md | similarity: 0.69

Information will be updated pending guidance from GSA.

========

[4] Leave types › Types of leave › Annual leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.68

You may use annual leave for any reason. Annual leave accrues based on how long you’ve worked for the federal government:

- Fewer than 3 years: 4 hours per pay period
- Between 3 and 15 years: 6 hours per pay period
- 15+ years: 8 hours per pay period

Your leave increases on the first full pay period following your work anniversary. You can refer to either HR Links or the bottom of your paystub for your leave balances.

You can carry over a maximum of 240 annual leave hours, from one leave year to the next. If you’ve transferred to TTS from another federal agency, your accrued annual leave will transfer with you.

========

[5] Performance Management Overview › Who participates in the end of year performance review? › Who is eligible for the end of year performance bonus?
source: performance-management/index | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/performance-management/index.md | similarity: 0.68

Employees who occupy eligible positions as of September 30, of the current fiscal year, and who
receive an eligible rating of record, may receive an Individual Performance
Award (IPA). “Ratings of Record (Annual)” should be completed in HR Links by
November 14, or that employee may not receive their award timely.

Subject to the availability of funds, OCFO and OHRM plan to distribute IPAs as
follows:

- **Level 5 summary ratings:** Up to 3.85% of adjusted basic pay, or up to 80
  hours of time off, subject to budget availability.
- **Level 4 summary ratings:** Up to 2.1% of adjusted basic pay, or up to 44
  hours of time off subject to budget availability.
- **"High 3" summary ratings:** Up to 0.385% of adjusted basic pay, or up to 8
  hours of time off subject to budget availability for employees who receive a
  Level 3 summary rating with one or more critical elements weighted 15% or
  greater, rated at Level 4 or Level 5.

The final award percentages for Level 5, Level 4 and Level 3 summary ratings
will be determined **when all performance reviews are complete**. In the event
the above targets for the Level 3, Level 4 and Level 5 summary ratings cannot be
met due to budget constraints, the percentage payouts for awards will be
decreased proportionally. Summary ratings are not an average score —
they are assigned as defined on InSite.

IPAs are targeted to be **paid out in December**, as in previous years.
However, the IPA payout date depends upon the status of the Continuing
Resolution and fiscal year funding funding.
```
</details>

## q29 (multi)

**Question:** If I travel for work outside my normal hours, do I get comp time for it, and will it be paid out if I later leave GSA?

**Reference answer:** Yes, travel comp time for approved TDY travel outside regular hours; it is not paid out when you leave (it is forfeited).

**Agent's answer:**

> You may request travel comp time when you are approved to travel for work (temporary duty or "TDY") and that travel occurs outside your regular working hours [Compensation for working extra hours › Travel comp time, for everyone]. This is intended for "gap filler" time when traveling outside of your regular work hours during a regular work day while not officially "performing work" [Compensation for working extra hours › Travel comp time, for everyone › Understanding travel comp time].
> 
> If you leave GSA, any unused travel comp time will be forfeited and will not be paid out [Compensation for working extra hours › Travel comp time, for everyone › Using travel comp time].
> 
> This handbook is a snapshot from June 2026; please confirm these details with your Timekeeper or an HR Specialist [Compensation for working extra hours › Travel comp time, for everyone › Understanding travel comp time].

<details><summary>Retrieved passages</summary>

```text
[1] Compensation for working extra hours › Travel comp time, for everyone
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.79

You may request travel comp time when you are approved to travel for work and that travel occurs outside regular working hours. Travel comp time is for “temporary duty,” also known as “TDY” travel, _not_ local travel or commuting. TDY travel is more than 12 hours long and requires a pre-approved authorization in Concur.

There are no limitations for earning travel comp time based on salary level or schedule type.

Refer to OPM’s Travel Comp Time Fact Sheet for more detail.

========

[2] Compensation for working extra hours › Travel comp time, for everyone › Understanding travel comp time
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.78

Traveling during your usual work day is considered regular hours, including traveling to the airport from your home.

Generally, travel comp time is used as a “gap filler” when you are traveling outside of your regular work hours during a regular work day, but not officially “performing work.”

For further details, current GSA employees can refer to the Compensation for Government Travel slidedeck to determine the breakdown of your hours. Please contact your Timekeeper or an HR Specialist at your agency if you have questions.

========

[3] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Compressed schedule
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.70

You are scheduled to arrive and depart at the same time, every day that you work. The start/stop times do not change from one pay period to the next. But, you work longer than 8 hours each day, so that you do not have to work the full 10 days in a pay period. This is a common TTS schedule, which we have typically called an Alternate Work Schedule (AWS).

- Overtime and comp time: Yes - Can only be approved for any hours that are in excess of what is normally scheduled for that work day (i.e., over the 8, 9, 10, 12 you were scheduled).
- Holiday pay: Yes - You will receive holiday pay for the 8, 9, 10, 12 hours you were scheduled to work. If a holiday falls on your scheduled off day, GSA may move your holiday one day earlier or later.
- Credit hours: No - Not available with this schedule

Compressed schedule examples - in a 2 week pay period:

- Example 1: You work four, 10 hour days each week. You have one specific day off each week.
- Example 2: One week, you work four 9 hour days and one 8 hour day (44 hours). The other week, you work four 9 hour days (36 hours) and have a specific day off.

========

[4] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Standard schedule
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.67

You are scheduled to arrive and depart at the same time, every day that you work. The start/stop times do not change from one pay period to the next. You work 8 hours every day, for all 10 work days per pay period. By default, new TTS employees are on a standard schedule.

- Overtime and comp time: Yes - Can be approved for working more than 8 hours in a day.
- Holiday pay: Yes - You receive 8 hours of holiday pay for the time you were scheduled to work.
- Credit hours: No - Not available with this schedule

========

[5] Leave types › Types of leave › Award leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.67

Award leave is offered for End of Year Performance Awards and Special Act Awards.

- If you are eligible for an End of Year Performance Award, you can opt-in via HRLinks to receive Award Leave in lieu of a monetary award.
- If you are receiving a TTS Special Act Award, you will be notified and asked for your preference of award leave or a monetary award.

You can receive a maximum of 80 hours of award leave in a single fiscal year. If you receive a Special Act Award after hitting the 80 hour cap, your award will be monetary.

Award leave expires one year after it is issued. You must use it by the end of the pay period in which the expiration date falls. Expired award leave cannot be recovered \- please monitor your leave balances and consider using award leave first. If you leave TTS, award leave is not paid out.

You can check the amount of Award leave you have in HR Links. You may receive an automated email reminder from HR Links 3 months before your leave expires, even if you have already used it.

OPM Policy:

- Time-Off Awards

[1] Compensation for working extra hours › Travel comp time, for everyone › Using travel comp time
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.85

Travel comp time expires one year (26 pay periods) after it is earned. When you reach the expiration date, you will forfeit the leave. If you leave GSA, any unused travel comp time will be forfeited.

========

[2] Compensation for working extra hours › Travel comp time, for everyone › Understanding travel comp time
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.81

Traveling during your usual work day is considered regular hours, including traveling to the airport from your home.

Generally, travel comp time is used as a “gap filler” when you are traveling outside of your regular work hours during a regular work day, but not officially “performing work.”

For further details, current GSA employees can refer to the Compensation for Government Travel slidedeck to determine the breakdown of your hours. Please contact your Timekeeper or an HR Specialist at your agency if you have questions.

========

[3] Updated Travel Guidance for GSA Employees (07/13/2021)
source: travel-and-leave/july-13-travel-guidance | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/july-13-travel-guidance.md | similarity: 0.75

GSA continues to adjust to the changing COVID-19 pandemic status. Effective
immediately as of July 13, any requests for travel must be mission critical,
time sensitive and required to perform essential duties. The employee’s
authorizing official (AO) is responsible for making the determination if travel
requests meet that threshold. Of note:

- Travel should not occur if the requirement can be met using virtual
  technology.
- Only the minimum number of employees required to meet the urgent need should
  travel.
- Travelers should work with administrative and budget staff in their
  organization to ensure any personal protective equipment (PPE) needed for
  travel is available before travel occurs.

All travel for conferences, related events and training do not meet this
requirement and are not authorized. Additional details regarding the new travel
threshold are included in
this guidance.

========

[4] Benefits › Leave
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.75

Please use HR Links to request sick
leave and annual leave. For any leave-related questions, please contact
cpc.benefits-retirement@gsa.gov.

For more information on Leave, including sick, funeral, unpaid, parental,
advanced, and religious, please reference the Leave page.

========

[5] Leave types › Transferring leave from another federal agency
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.74

Annual leave and sick leave balances can take a _significant_ amount of time to transfer to GSA, depending on the speed of your previous payroll provider. If you have your final Earnings and Leave Statement (pay stub) from your previous agency, you can send a copy to kc-payroll.finance@gsa.gov to expedite the process.
```
</details>

## q30 (unanswerable)

**Question:** How do I sign up for the transit subsidy, and which organization code do I enter?

**Reference answer:** The handbook only points to a separate transit benefit page and gives no enrollment steps; say the corpus does not cover it and suggest People Ops.

**Agent's answer:**

> To sign up for the transit subsidy, please see the transit benefit page [Benefits › Transit subsidies].
> 
> The handbook does not provide specific instructions for signing up or the organization code to enter for the transit subsidy. Please contact People Ops (TTS-PeopleOps@gsa.gov) for assistance with this process.
> 
> *This handbook is a snapshot from June 2026; please confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Benefits › Transit subsidies
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.74

See the transit benefit page.

========

[2] Frequently Asked Questions › Questions about reimbursement › How should I claim local transportation expenses?
source: travel-and-leave/travel-and-leave-policies/travel-guide-faq | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-faq.md | similarity: 0.65

For public transit, taxis, rental cars, POV mileage and other forms of local
transportation, you may add the expense as normal, choosing
whichever expense description reflects the nature of the method used. Choose the
payment method used, and
upload a receipt only for rental cars, rental car gas, or
any other expense greater than $75 (this threshold is $25 for
local vouchers.

Any local transit expense other than public transit under $25 requires a brief
comment describing the origin and destination of the travel (e.g. "from airport
to office").

You can add this by clicking on **Show other details** and filling out the
**Comments** section that pops up below.

For public transit over $25, a “blanket entry” describing generally the origins
and destinations of travel paid for is acceptable.

For rental cars and mileage claims, the comment should also include an
additional justification as specified
here.

For mileage claims over $75, instead of attaching a receipt, attach a screenshot
showing a map of your itinerary with the calculated distance.

========

[3] Frequently Asked Questions › Questions about reimbursement › How do I create a local or miscellaneous voucher?
source: travel-and-leave/travel-and-leave-policies/travel-guide-faq | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-faq.md | similarity: 0.64

Upon selecting the **Local voucher** option, you will be taken to a blank
**Document Information** page. Here's what you need to include for each field:

- **Trip Name** This should follow
  the same naming conventions you would use for a travel authorization.
  - the request name and/or item description with the fiscal year and division/organization field
    (e.g. FY25 CoE PyCon registration fee). Ensure you have
    an email from your authorizing official
    approving all of the expenses you'd like to claim sent to
    tts-travel@gsa.gov.
- **Type code** and **Trip purpose** If the voucher is for local travel (taxis,
  mileage, etc.), choose **Local travel**. For any other sort of reimbursement,
  choose **Misc voucher**.
- **Document detail** Enter a brief description of what the reimbursement is for
  here. A PDF copy of the approved SF-182 (if you have one) and events request
  number must be in the “Document Detail” section (i.e. events-25-3424).
- Click on **Create Document**

Proceed on to entering your expenses.
Note that any local transit over $25 requires a receipt, and all expenses
claimed on a miscellaneous voucher require receipts. The payment method for all local and miscellaneous vouchers is CASH. Do not use your travel card.

========

[4] Get access to Concur › Frequently Asked questions
source: travel-and-leave/travel-and-leave-policies/first-time-travel-get-in-concur | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/first-time-travel-get-in-concur.md | similarity: 0.64

What is my Correspondence/Office symbol?
Q2: Director and Staff

Q2A0A: Technology Operations Division

Q2AAA: cloud.gov

Q2AAB: Login.gov

Q2AAC: Platforms and Services Division

Q2AAD: Public Experience

Q2AAE: FedRAMP

Q2AAF: Accelerators/10x

Q2AB: OROS

Q2AC: IAE

Q2ADB: CoE

Q2BA: Acquisitions

Q2BB: Business Operations

Q2BC: MD&P

Q2BD: Outreach

Q2BEB: Talent

Q2BEC: People Operations

Q2CA: PIF

Q2CB: USDC

What are my user roles?
Only traveler, unless you have already been instructed otherwise by the travel
team. Reviewers and Supervisors will also add the "Travel Approver" Role

========

[5] Get set up to travel for TTS <em>before</em> GSA onboarding
source: travel-and-leave/travel-and-leave-policies/first-time-travel-get-in-concur-pre-olu | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/first-time-travel-get-in-concur-pre-olu.md | similarity: 0.63

If you're traveling for TTS during your first two weeks (normally for
orientation, if you're based in a city that doesn't have a TTS office), you'll
need to follow special procedures to get your account set up, which will allow
you to make your flight and hotel reservations via AdTrav by calling (877)
472-6716. Here's what you need to do:

1. First thing to get is a **“travel vendor ID”**, which you can request by
   filling out
   the EFT form
   and sending it to:
   kc-vendor.number.requests@gsa.gov.

The EFT form is needed so that the reimbursement for your hotels, meals, and other expenses can be reimbursed (GSA only pays for your flight or Amtrak tickets upfront).

**_Note, if you haven't yet started working at GSA and don't have your GSA email address_:**

Your access to the EFT form linked above may be restricted, so you should have
received it as an attachment in your welcome email-- feel free to reach out to
tts-travel@gsa.gov if you never got it. Email the filled out EFT to ext-vendor.help@gsa.gov.

2. Once you receive your travel vendor ID (should be in the format _E000xxxxx_),
   forward it to tts-travel@gsa.gov, along with
   your **Full Name** as it appears on ID and **Phone Number** as per TSA
   requirements.

3. **Book travel**: A member of the TTS travel team will reach out to you within
   two business days once you’ve sent in the above information, confirming that
   you've been set up in the Concur system. You may then call AdTrav at (877)
   472-6716 to make your reservations at your convenience.

Email tts-travel@gsa.gov once you've finalized your reservations and they
   will approve your itinerary. Make sure this is done during business hours--
   no later than 3:30 PM ET!
```
</details>

## q31 (unanswerable)

**Question:** Which days are paid federal holidays for TTS employees, and how many are there in a year?

**Reference answer:** The handbook explains holiday pay by schedule but does not list the holidays; say it is not covered.

**Agent's answer:**

> The handbook does not cover which specific days are paid federal holidays or how many there are in a year.
> 
> The handbook mentions that employees on a flexible schedule receive 8 hours for a holiday [Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Holidays and flexible schedules], and that those on a standard schedule receive 8 hours of holiday pay for the time they were scheduled to work [Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Standard schedule]. Please contact People Ops (TTS-PeopleOps@gsa.gov) for a list of observed holidays.
> 
> *Note: The handbook is a snapshot from June 2026 and you should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Flexible schedule › Holidays and flexible schedules
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.70

_This special note is for variable day, variable week, and maxiflex schedules._

If you are on a flexible schedule, you will receive 8 hours for a holiday. If you typically work more than 8 hours on a day which falls on a holiday, you have a few options:

- Make up the hours on a different day
- Take annual leave
- Use credit hours, or use comp time.

For example: you typically work 10 hours on Thursdays. December 25th falls on a Thursday. You are given 8 hours for the paid holiday, and you work 2 extra hours on Monday, December 22nd, to make up the difference.

========

[2] Leave types › Types of leave › Annual leave
source: travel-and-leave/leave | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/leave.md | similarity: 0.69

You may use annual leave for any reason. Annual leave accrues based on how long you’ve worked for the federal government:

- Fewer than 3 years: 4 hours per pay period
- Between 3 and 15 years: 6 hours per pay period
- 15+ years: 8 hours per pay period

Your leave increases on the first full pay period following your work anniversary. You can refer to either HR Links or the bottom of your paystub for your leave balances.

You can carry over a maximum of 240 annual leave hours, from one leave year to the next. If you’ve transferred to TTS from another federal agency, your accrued annual leave will transfer with you.

========

[3] Veteran & service member resources › Leave
source: general-information-and-resources/employee-resources-policies/veterans-service-members | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/veterans-service-members.md | similarity: 0.68

There are four types of leave that are offered specifically to veterans and/or service members:

- Military leave for active duty, active duty training, and inactive duty training in the National Guard or as a Reservist.
- Military spouse relocation leave
- Disabled Veteran Leave for employees with a service-connected disability rating of 30 percent or more, to use during their first year of federal employment
- Funeral leave for veterans to participate in a funeral ceremony for a member of the Armed Forces. Funeral leave is also available for anyone who needs to plan or attend services of an immediate relative who has suffered a combat-related death.

========

[4] Work schedules › Schedule types and their relationship to overtime, holiday pay, and credit hours › Standard schedule
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.68

You are scheduled to arrive and depart at the same time, every day that you work. The start/stop times do not change from one pay period to the next. You work 8 hours every day, for all 10 work days per pay period. By default, new TTS employees are on a standard schedule.

- Overtime and comp time: Yes - Can be approved for working more than 8 hours in a day.
- Holiday pay: Yes - You receive 8 hours of holiday pay for the time you were scheduled to work.
- Credit hours: No - Not available with this schedule

========

[5] Compensation for working extra hours › Religious comp time, for everyone
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.68

Per OPM guidance, you can request an adjustment to your work schedule for religious observances, instead of using annual leave. In HR Links, this is treated as another kind of comp time.

Email your supervisor about the extra hours you plan to work before a religious observance.
```
</details>

## q32 (unanswerable)

**Question:** What is the per diem rate for meals when I travel to Chicago for work?

**Reference answer:** The handbook says Concur shows the per diem for the location but gives no rates; say it is not covered and point to Concur.

**Agent's answer:**

> The handbook does not provide specific per diem rates for locations like Chicago.
> 
> The allowance for Meals and Incidental Expenses (M&IE) is based on your travel location [What to consider while traveling › Meals and Incidental Expenses (M&IE)]. You should verify the current rate for your specific destination with People Ops (TTS-PeopleOps@gsa.gov).
> 
> *This handbook is a snapshot from June 2026 and the employee should confirm with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] What to consider while traveling › Meals and Incidental Expenses (M&IE)
source: travel-and-leave/travel-and-leave-policies/travel-guide-3-travel | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-3-travel.md | similarity: 0.75

In addition to receiving round trip tickets to your destination and lodging for
the nights that you need to stay there, you also get a flat-rate per diem for
**Meals and Incidental Expenses (M&IE)**. A few things to remember:

- M&IE is given to you to cover the additional expenses you might incur while
  traveling that you might not normally have at home, like dining out instead of
  eating home-cooked meals, forgetting toothpaste, tipping hotel porters, etc.

- This allowance is at your discretion to spend and **you don’t need to provide
  receipts** for it.

- The amount that is given is based on your location, not your actual expenses.
  If you spent less than the allowance, you get to keep the difference, and if
  you spend more, you must pay the difference.

- M&IE is given at a reduced rate on “travel days”-- i.e. days where part of the
  normal work day was spent traveling. This reduced rate is always 75% of normal
  M&IE, regardless of how much of the day was actually spent traveling.

Note that if your travel extends past midnight, you get the full meal allowance
for the long day of travel plus the 75% of the meal allowance for the following
day (even if you arrived just after midnight local time). If you anticipate
traveling past midnight, ensure your authorization reflects this in advance,
otherwise, you will need to create an amended
authorization upon your
return.

- M&IE is given as a reimbursement after submitting a voucher, which is done
  after you return from a trip. How this reimbursement is disbursed depends on
  how much you used the GSA travel card.

========

[2] Frequently Asked Questions › Questions about reimbursement › Questions about entering specific expenses › How should I claim meals and incidental expenses?
source: travel-and-leave/travel-and-leave-policies/travel-guide-faq | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-faq.md | similarity: 0.74

- **The allowance for Meals and Incidental Expenses (M&IE) is a flat rate given
  to a traveler regardless of what they actually spent.** No receipts or
  justification is needed to receive M&IE.
- **For example**: Consider a trip taken between 9/16 and 9/18. M&IE is $69 per
  day in DC, and is 75% of $69 ($51.75) on the first and last days of a trip. We
  see that the three days of M&IE has been added automatically.

========

[3] What to consider while traveling › Meals and Incidental Expenses (M&IE) › M&IE and use of the GSA travel card
source: travel-and-leave/travel-and-leave-policies/travel-guide-3-travel | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-3-travel.md | similarity: 0.71

While use of the GSA travel card is required for all travel expenses when
practicable, using the GSA travel card to pay for M&IE requires some additional
administrative work when submitting a voucher after returning from your trip.
Here's
what you should be aware of when completing your voucher-- should you use the
GSA travel card for meals and incidental expenses, keeping receipts for your
personal use may be helpful. Feel free to book
travel office hours for
a walkthrough on what to keep in mind when paying for meals while traveling.

========

[4] Frequently Asked Questions › Questions about reimbursement › Questions about entering specific expenses › How should I claim meals paid on the travel card?
source: travel-and-leave/travel-and-leave-policies/travel-guide-faq | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-faq.md | similarity: 0.71

When meals are paid on the travel card, there are a few different ways of
documenting it:

- One can create a new M&IE expense with expense method **IBA** in the amount
  spent on meals per day. The amount of M&IE reimbursed to your personal account
  will be automatically reduced accordingly (you will see negative charges
  appear that correspond with this). If you document all expenses correctly,
  your travel card bill will be paid off exactly.
- One can change the payment method of M&IE expenses to **IBA** so that all
  reimbursement is routed to the travel card. If the entire allowance was not
  used, any amount left over will show up as a positive balance. You may call
  the customer service number on the back of the card and request that a check
  be mailed for that remaining amount.
- One can leave the payment method of M&IE expenses as the default, **CASH**.
  After the voucher is processed, there will be an outstanding balance
  remaining. This will need to be paid-- call the customer service number on the
  back of the card for more details on making a payment.

========

[5] External speaking request playbook › Additional information › Food fees
source: training-and-development/external-speaking-request-playbook | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/training-and-development/external-speaking-request-playbook.md | similarity: 0.69

You can have lunch or dinner at the event, as long as it complies with one of
the exceptions or exclusions under the Standards of Ethical Conduct or has been
accepted by the agency as a non-federal source travel payment. Under the
exclusions to the Standards of Ethical Conduct, the term gift does not include
anything paid for by the government as well as anything for which market value
is paid by the employee. See
5 C.F.R. 2635.203(b)(7)
and
(b)(10).

For local speaking events, under the speaking and similar engagements exclusion
free attendance includes waiver of all or part of the fee for an event or the
provision of food, refreshments, entertainment, instruction or materials
furnished to all attendees as an integral part of the event. It does not include
travel expenses, lodgings, or entertainment collateral to the event. It does not
include meals taken other than in a group setting with all other attendees,
unless the employee is a presenter at the event and is invited to a separate
meal for participating presenters that is hosted by the sponsor of the event.
See
5 C.F.R. 2635.203(g).

For a travel speaking event, if a non-federal source offers to pay for a meal,
the agency must accept the offered item under the non-federal source travel
payment statute,
31 U.S.C. 1353,
before travel begins. The item must be provided in-kind (no reimbursement or
money provided to the employee) and accepted by the agency as a non-federal
source travel payment.
```
</details>

## q33 (unanswerable)

**Question:** How much does the government match on my Thrift Savings Plan contributions?

**Reference answer:** The handbook only says employees can join the TSP and links to InSite; it gives no matching rate, so say it is not covered.

**Agent's answer:**

> The handbook does not cover this. Please check the official Thrift Savings Plan website at https://www.tsp.gov or ask People Ops (TTS-PeopleOps@gsa.gov) for information regarding government matching contributions.
> 
> This handbook is a snapshot from June 2026 and you should confirm this information with HR.

<details><summary>Retrieved passages</summary>

```text
[1] Benefits › Retirement › TSP (Thrift Savings Plan)
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.74

Employees at TTS are eligible to participate in the
Thrift Savings Plan (TSP). For more
information on TSP, please refer to the
TSP Insite page.

You will update TSP directly in HR
Links by following
this
visual guide
or these steps:

1. After you sign into HR Links, click "Benefits Summary"
2. Click on the **TSP** tile/row to view and edit your contribution amounts
3. Click **Save**

If you had been contributing to a 401k, 403b, or a similar plan at a previous employer this year, your total contribution for all similar plans cannot be higher than the annual limit.

You can roll over money from eligible retirement plans to your TSP account. TSP offers a rollover concierge service and a self-service option. Visit the TSP Move Money page for details.

There are numerous free TSP webinars available: visit the TSP Online Learning page to view descriptions and dates.

========

[2] Benefits › Retirement › FERS (Federal Employees Retirement System)
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.70

The Federal Employees Retirement System (FERS) is the retirement plan that all
employees pay into during their federal employment. A percentage of each
paycheck is withheld by GSA and put into FERS.

Employees must have at least 5 years of
creditable service
to be eligible for FERS payments upon retirement.

If you leave government before becoming eligible for FERS retirement, you can
request that your contributions be returned in a lump sum payment: see leaving
TTS for more information.

If you served as an AmeriCorps VISTA volunteer, a Peace Corps Volunteer, and/or
in the military, you may be eligible to “buy back” your service. “Buying back”
your military/volunteer service allows the amount of time you served to be
applied toward your FERS retirement calculations.

As an example, if you served in the Peace Corps for 2 years and buy back your
service, that amount of time would be considered creditable service and would
increase your “length of service”
FERS payment calculation.

========

[3] Benefits links and resources › Benefits links
source: general-information-and-resources/employee-resources-policies/benefits-links | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/benefits-links.md | similarity: 0.67

| Benefit                                                                | Link                                                                                                                                                 |

| Leave and Earnings Statement; Federal, State and Local Tax Withholding | https://www.employeeexpress.gov                                                                                                                    |
| Vacation Request                                                       | https://hrlinks.gsa.gov/                                                                                                                           |
| GSA Insite                                                             | https://insite.gsa.gov                                                                                                                             |
| Health and Life Insurance                                              | https://www.opm.gov/insure                                                                                                                         |
| Retirement Planning                                                    | https://www.opm.gov/retirement-services                                                                                                            |
| Thrift Savings Plan (TSP)                                              | https://www.tsp.gov (contributions updated through HR Links) |
| Flexible Spending Account                                              | https://www.fsafeds.com                                                                                                                            |
| Dental and Vision Insurance                                            | https://www.benefeds.com                                                                                                                           |
| Long Term Care Insurance                                               | https://www.ltcfeds.com                                                                                                                            |
| Public Service Student Loan Forgiveness Program                        | https://studentaid.ed.gov/sa/repay-loans/forgiveness-cancellation/public-service                                                                   |

========

[4] Veteran & service member resources › Military Service Deposits (“Buying back”)
source: general-information-and-resources/employee-resources-policies/veterans-service-members | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/veterans-service-members.md | similarity: 0.67

Veterans can receive retirement credit for their military service. This is often called “buying back”. You’ll work with OHRM to complete paperwork and make a financial deposit covering your military service.

- InSite has information on Military Service Deposits.
- DFAS offers a Military Service Earnings/Buy Back Estimator.
- Your FAS Benefits Specialist is your point of contact for questions and assistance.

========

[5] Hiring Authorities
source: hiring-staying-or-changing-jobs/hiring-authorities | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/hiring-authorities.md | similarity: 0.67

There are several different hiring paths within the federal government. We have
a side-by-side comparison chart of
Hiring Methods
we use at TTS. Below is a brief overview.
```
</details>

## q34 (unanswerable)

**Question:** What is the salary range for a GS-13 position at TTS?

**Reference answer:** The handbook only gives the overall pay cap (GS-15 step 10); say GS-13 pay is not covered.

**Agent's answer:**

> The handbook does not cover this. The handbook does mention that GSA salary levels depend on GS-level, locality, and special salary rates, and it directs employees to OPM for details on pay scales [Compensation for working extra hours › Overtime and Compensatory (Comp) time › Overtime, depending on your salary level]. Please ask People Ops (TTS-PeopleOps@gsa.gov) for information regarding current salary ranges.
> 
> *This handbook is a snapshot from June 2026 and you should confirm this information with HR.*

<details><summary>Retrieved passages</summary>

```text
[1] TTSJobs
source: hiring-staying-or-changing-jobs/ttsjobs | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/ttsjobs.md | similarity: 0.75

Interested in joining our team, or transitioning to a new role?

========

[2] Hiring Authorities
source: hiring-staying-or-changing-jobs/hiring-authorities | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/hiring-authorities.md | similarity: 0.73

There are several different hiring paths within the federal government. We have
a side-by-side comparison chart of
Hiring Methods
we use at TTS. Below is a brief overview.

========

[3] Compensation for working extra hours › Overtime and Compensatory (Comp) time › Overtime, depending on your salary level
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.73

Overtime is when you are paid for extra hours that you are required to work. The amount of overtime pay you receive depends on your GS- level and FLSA exemption status.

Your total pay (including overtime) cannot exceed the maximum salary at GSA, which is $191,900 as of 2024. This is GS-15, step 10, including any applicable special salary rate or locality rate of pay.

Refer to OPM’s Overtime Fact Sheet for more detail.

========

[4] Benefits › Paychecks
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.73

We are paid biweekly. You’ll receive your first paycheck about three weeks after
your start date. This is because every TTS employee starts work at the beginning
of a pay period. It takes a week after the end of a pay period for a direct
deposit to be made. See the
GSA Payroll Calendar to determine
future pay cycles.

Please direct questions to the payroll help desk: **1-844-303-6515** or
email them.

To see your recent pay stubs:

1. Sign into Employee Express. If you don't
   have access yet, email
   kc-payroll.finance@gsa.gov to request a
   copy. They’ll send it to you in a password-locked zip file.
2. Click the "View Your Earnings and Leave Statement" link in the middle of the
   page.
3. Choose the appropriate pay period in the drop-down menu.

For help interpreting the many boxes on your paystub, see
How to Read Your Leave and Earnings Statement.
You can also watch
the recording of 'A Beginner's Guide to Your Earnings and Leave Statement,'
a session that a TTS teammate offered.

Note that the gross income in your paycheck is a little less than your annual
income / 26 paychecks. The difference lies in the way the federal government
calculates hourly rates from annual salary. The federal government divides the
annual salary by 2087 hours rather than 2080 hours (26 pay periods x 80 hours)
to determine hourly rates.

This is because about every 11 years or so there are 27 pay periods rather than
26 pay periods (2015 was such a year for GSA payrolled employees). Here is an
article that explains this:
Why your paychecks don't always add up.

========

[5] Promotions › Introduction to the Merit Promotion process
source: hiring-staying-or-changing-jobs/promotions | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/promotions.md | similarity: 0.72

Before going into the process, it’s important to note that “promotions” in the
traditional sense (private sector) do not exist within the federal government.
Government has a position-driven view; everything begins with the need, not the
person. This means that a position is not created and filled for the purpose of
someone attaining a higher GS level.

Instead, the organization identifies a need for a higher level position due to
the type of work that must be accomplished and can choose to fill that need
through multiple recruitment or staffing methods, including the Merit Promotion
process.

> "One avenue of recruitment is through GSA's merit staffing process. GSA's
> Merit Promotion Plan contains the requirements for filling vacancies through
> internal competition, i.e., filling from existing GSA and other eligible staff
> (i.e. federal employees in other agencies). Merit promotion procedures provide
> a fair and systematic means of identifying, considering, and selecting GSA and
> other eligible candidates for promotions and career opportunities based on the
> Merit Principles."

As you can see from the above excerpt from GSA’s policy, the Merit Promotion
process is for "filling vacancies through internal competition". The Merit
Promotion process increases visibility of opportunities within TTS and creates
an avenue for other competitive service federal employees to join TTS.

For all Merit Promotion roles: employees must be at their current GS level for
one year in order to apply for a position at the next highest GS level. This is
called the “time-in-grade” requirement, and an applicant must meet time-in-grade
within 30 days of an application’s closing date.
```
</details>

## q35 (unanswerable)

**Question:** Does TTS pay a monthly stipend for my home internet when I telework?

**Reference answer:** The handbook only covers internet costs during official travel; say a telework internet stipend is not covered.

**Agent's answer:**

> The handbook does not cover this. The provided passages do not mention a monthly stipend for home internet for teleworking employees. You should ask People Ops (TTS-PeopleOps@gsa.gov) for clarification.
> 
> Please note that this handbook is a snapshot from June 2026 and you should confirm this information with HR.

<details><summary>Retrieved passages</summary>

```text
[1] What to consider while traveling › Other necessary expenses
source: travel-and-leave/travel-and-leave-policies/travel-guide-3-travel | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/travel-guide-3-travel.md | similarity: 0.69

Internet service
- May be expensed when government-provided internet service (i.e. the data plan
  and hotspot on your government phone) is not available. Wifi on an airplane is
  generally reimbursable, but wifi charges at a hotel or other areas where cell
  signal is generally available require justification specifying why you weren't
  able to use your government phone connection.

Laundry expenses
- May only be reimbursable if travel involves at least 4 consecutive nights.

========

[2] Moving and changing your address › Policy links
source: travel-and-leave/travel-and-leave-policies/moving | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/moving.md | similarity: 0.68

- GSA Telework and Remote Work Policy

========

[3] Moving and changing your address › Updating your address & notifying benefits companies
source: travel-and-leave/travel-and-leave-policies/moving | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/moving.md | similarity: 0.68

Once your move is approved, you should change your home address in HR Links; you
can follow this
step-by-step guide
to make that change. You'll also need to
modify your telework agreement
with your new address.

You cannot manually change your address with your federal health insurance
companies, OPM, or TSP: they will receive your new address from GSA, once all
move-related paperwork and steps are complete.

========

[4] Veteran & service member resources › Domestic employees teleworking overseas (DETO)
source: general-information-and-resources/employee-resources-policies/veterans-service-members | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/veterans-service-members.md | similarity: 0.68

Domestic employees teleworking overseas (DETO) arrangements are a workplace flexibility that GSA considers on a case-by-case basis. A sponsored DETO is an employee who has a spouse overseas on military, foreign service, or civilian orders.

DETO information and criteria are available in GSA’s Telework and Remote Work Policy. The DETO process requires GSA and Department of State approvals which may take 6 months to a year. Employees seeking DETO approval should consult with their supervisor immediately after receiving notice of an upcoming overseas tour.

========

[5] Conferences, events, and training › Remote working guidance
source: training-and-development/conferences-events-training | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/training-and-development/conferences-events-training.md | similarity: 0.68

When working from somewhere that isn't your usual duty location, consider these
tips to help coworkers and partners plan
around your trip.
```
</details>

## q36 (unanswerable)

**Question:** Does TTS offer a signing bonus or a relocation incentive to new hires?

**Reference answer:** Not covered by the handbook; say so and suggest asking HR.

**Agent's answer:**

> The handbook does not cover this.
> 
> The handbook does not contain information regarding signing bonuses or relocation incentives for new hires. I suggest asking People Ops (TTS-PeopleOps@gsa.gov).
> 
> The handbook is a snapshot from June 2026 and you should confirm with HR.

<details><summary>Retrieved passages</summary>

```text
[1] Internal hiring and internal TTS details
source: hiring-staying-or-changing-jobs/assignee-detail | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/assignee-detail.md | similarity: 0.63

All opportunities within TTS, including details and reassignments, should be
openly shared and competed within the organization. There is a
TTS Internal Hiring request process
for pursuing any type of internal hiring request (open application process or
not). Please submit a request through the
TTS Internal Hiring Request form even if
you’re not completely sure how to best proceed.

Although internal hiring actions are processed quicker than external hiring
actions, internal actions still require need, effort and intentionality.

========

[2] Moving and changing your address › Moving
source: travel-and-leave/travel-and-leave-policies/moving | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/moving.md | similarity: 0.63

**Note: Employees should not move/relocate without formal approval by GSA HR.**

If you plan to permanently move or relocate for longer than 120 days, email your supervisor as soon as you are thinking about moving. There may be implications to your move you might not be aware of or would like to confirm - such as a change in pay. Please provide the following information:

- The city, county, state, ZIP code that you are moving to (if you know it).
  - If you are staying in the same city, county, state, or ZIP code, make a note
    of that.
- The effective date for your move. The effective date needs to be the start of
  a pay period. You can find pay period dates via
  GSA’s Payroll Calendar page.
- Whether you are a Remote Worker (you always work from home) or a Routine
  Teleworker (onsite flexible: you go into an office two times or more per pay
  period). If you don’t know your status, tell us that.

After receiving your information, your supervisor will work with TTS leadership on how to proceed. A Personnel Action Request (PAR) may need to be processed for you, depending on your unique situation. If applicable, your new pay rate will not be effective until your move is approved and the PAR is processed; this can take a few weeks.

Below are a few key things to know.

========

[3] Compensation for working extra hours
source: travel-and-leave/overtime | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/overtime.md | similarity: 0.62

Current employees can use this leave comparison chart to see what you can use your hours for.

You will need supervisor approval before working extra hours. Generally, do not expect to work extra hours unless you’re working on a high-profile project.

You will need to manually request these hours in HR Links before using them.

========

[4] Moving and changing your address › Changes in pay
source: travel-and-leave/travel-and-leave-policies/moving | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/travel-and-leave-policies/moving.md | similarity: 0.62

If you are moving to a new region, your pay may change. Look up your new pay via
OPM's GS Locality Pay Tables.
Check that you are in the current year, find your region under the pay table,
and then find your step and grade. That’s what you’ll be paid in your new
location.

========

[5] Hiring Authorities
source: hiring-staying-or-changing-jobs/hiring-authorities | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/hiring-staying-or-changing-jobs/hiring-authorities.md | similarity: 0.61

There are several different hiring paths within the federal government. We have
a side-by-side comparison chart of
Hiring Methods
we use at TTS. Below is a brief overview.
```
</details>

## q37 (unanswerable)

**Question:** What is the dress code when I work from a GSA office?

**Reference answer:** Not covered by the handbook; say so.

**Agent's answer:**

> The handbook does not cover this. Please contact People Ops (TTS-PeopleOps@gsa.gov) for guidance on office attire.
> 
> *Note: This handbook is a snapshot from June 2026; please confirm with HR as policies may change.*

<details><summary>Retrieved passages</summary>

```text
[1] Employment Verification
source: general-information-and-resources/employee-resources-policies/employment-verification | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/employment-verification.md | similarity: 0.72

Providing verification of GSA employment and salary.

========

[2] Updated Travel Guidance for GSA Employees (07/13/2021)
source: travel-and-leave/july-13-travel-guidance | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/travel-and-leave/july-13-travel-guidance.md | similarity: 0.72

GSA continues to adjust to the changing COVID-19 pandemic status. Effective
immediately as of July 13, any requests for travel must be mission critical,
time sensitive and required to perform essential duties. The employee’s
authorizing official (AO) is responsible for making the determination if travel
requests meet that threshold. Of note:

- Travel should not occur if the requirement can be met using virtual
  technology.
- Only the minimum number of employees required to meet the urgent need should
  travel.
- Travelers should work with administrative and budget staff in their
  organization to ensure any personal protective equipment (PPE) needed for
  travel is available before travel occurs.

All travel for conferences, related events and training do not meet this
requirement and are not authorized. Additional details regarding the new travel
threshold are included in
this guidance.

========

[3] Code of conduct › Unacceptable Behavior
source: about-us/code-of-conduct | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/about-us/code-of-conduct.md | similarity: 0.71

To help colleagues understand the kinds of behaviors that are illegal or run
counter to the work-culture we seek to foster, we've listed below actions that
violate federal law and GSA policies. We've also included steps to take if you
encounter behavior that runs contrary to this policy.

Sexual and Non-Sexual Harassment
GSA Policies forbids:

- Sexual and non-sexual harassment and misconduct
- Unwelcome verbal or written comment or physical conduct based on:
  - race,
  - religion,
  - color,
  - sex,
  - national origin,
  - age,
  - disability,
  - genetic information,
  - parental status,
  - marital status,
  - or political affiliation.
- Retaliating against anyone who files a formal complaint that someone has
  violated GSA anti-harassment policies.

========

[4] Work schedules
source: general-information-and-resources/employee-resources-policies/work-schedules | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/general-information-and-resources/employee-resources-policies/work-schedules.md | similarity: 0.71

Each of us has a work schedule: the hours that GSA expects us to be working. This page provides an overview of work schedule terminology and schedule types. The work schedule overview chart also provides a high level, visual comparison.

========

[5] Benefits
source: getting-started/classes/benefits | url: https://github.com/18F/handbook/blob/c220f93896b39e9e4ab0f486a1d5bf346ac06e3e/pages/getting-started/classes/benefits.md | similarity: 0.70

**If you're looking for specific benefits sites, see the benefits links
page.**

GSA requires that you enroll in many of the benefits offered to you within the
first 60 days of work. Otherwise, you'll have to wait for Open Season, which
typically runs from the Monday of the second full work week in November through
the Monday of the second full work week in December.
```
</details>
