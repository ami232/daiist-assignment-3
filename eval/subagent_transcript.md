# Subagent transcript: corpus-researcher

Claude Code (headless, `claude -p`, version 2.1.331), main model `claude-opus-5-5`, run from the repo root on 2026-11-25 with only the `corpus` MCP server (`server.py`, design A index) and `--allowedTools Agent,Task,mcp__corpus__search`. The main agent delegated to `.claude/agents/corpus-researcher.md`, whose only tool is `mcp__corpus__search`. Captured with `--output-format stream-json`; passage text in the search results is abbreviated to the returned ids.

## Main agent: tool call `Agent`

`subagent_type: corpus-researcher`, description: "Rail delay compensation lookup"

## Main agent → corpus-researcher (delegation prompt)

A traveller asks: "My train from Madrid to Paris arrived 90 minutes late. What compensation do the EU texts give me, and are there exceptions where the railway does not have to pay?"

Search the corpus (rail Regulation 2021/782 especially) and report:
1. The compensation rule for rail delays: delay thresholds and percentages of the ticket price, and what 90 minutes falls under. Include how the ticket price basis is defined (single vs return, through tickets), minimum payout thresholds, payment form/timing, and any rule about not being entitled if informed of the delay before buying.
2. Every exception/exemption where the railway does not have to pay compensation (e.g. extraordinary circumstances, weather, third-party behaviour, passenger fault, strikes) and any limits on those exceptions. Also any Member State exemptions for international or cross-border services that could affect a Madrid–Paris journey.
3. Keep compensation separate from refund/re-routing and assistance; mention those only briefly if the passages cover them and they are relevant to a 90-minute delay.
4. Facts about the traveller's case that the answer depends on and that they have not given (e.g. ticket price, single vs return, whether one through ticket, whether they were told of the delay before buying, cause of delay).

Cite every material claim with the passage id exactly as the search tool printed it, in square brackets. Quote key words where interpretation is needed. Say clearly if anything is not covered by the passages you retrieved. Search multiple times with different wording if needed.

## corpus-researcher: search calls (6) and returned passage ids

- **search**(`rail compensation for delay 60 to 119 minutes 25% of ticket price`) → `32021R0782:A:w054:1`, `32021R0782:A:w055:1`, `32021R0782:A:w057:1`, `32021R0782:A:w056:1`, `32021R0782:A:w058:1`
- **search**(`railway undertaking not obliged to pay compensation extraordinary circumstances weather third party passenger fault strike`) → `32021R0782:A:w059:1`, `32021R0782:A:w058:1`, `32021R0782:A:w019:1`, `32021R0782:A:w020:1`, `52024XC05687:A:w077:1`
- **search**(`Member States exempt rail services from application of regulation international cross-border`) → `32021R0782:A:w029:1`, `32021R0782:A:w004:1`, `32021R0782:A:w030:1`, `32021R0782:A:w005:1`, `32021R0782:A:w028:1`
- **search**(`rail delay 60 minutes assistance meals refreshments accommodation Article 20(2)`) → `32021R0782:A:w060:1`, `32021R0782:A:w059:1`, `52024XC05687:A:w055:1`, `32021R0782:A:w061:1`, `32021R0782:A:w054:1`
- **search**(`Article 18 reimbursement and re-routing expected delay at arrival of more than 60 minutes`) → `32021R0782:A:w050:1`, `32021R0782:A:w054:1`, `32021R0782:A:w052:1`, `32021R0782:A:w051:1`, `32004R0261:A:w019:1`
- **search**(`where it is reasonably to be expected that arrival at final destination will be delayed by 60 minutes reimbursement re-routing choice`) → `32021R0782:A:w050:1`, `32004R0261:A:w019:1`, `32021R0782:A:w049:1`, `32021R0782:A:w051:1`, `32021R0782:A:w054:1`

## corpus-researcher → main agent (subagent's reply)

NEED DETAILS: A 90-minute delay falls in the rail Regulation's band of "25 % of the ticket price for a delay of 60 to 119 minutes" (50 % from 120 minutes); this is paid "without losing the right of transport", for a delay between the departure and final destination "stated in the ticket or through-ticket", and only if the ticket cost "has not been reimbursed in accordance with Article 18" [32021R0782:A:w054:1]. The basis is "the full price which the passenger actually paid for the delayed service"; for a return contract it is the price shown for that leg, or half the ticket price if no leg price is shown, and other multi-leg contracts are calculated in proportion to the full price [32021R0782:A:w055:1][32021R0782:A:w056:1]. Payment is due within one month of the request; it may come as vouchers or other services if their terms are flexible, but as money if you ask, it may not be cut by transaction fees, and a minimum payout threshold may be set at no more than EUR 4 per ticket [32021R0782:A:w057:1][32021R0782:A:w058:1]. There is no compensation at all if you were "informed of a delay before buying a ticket", or if a delay after continuation or re-routing "remains below 60 minutes" [32021R0782:A:w058:1]. The railway need not pay if it "can prove" the delay was "caused directly by, or was inherently linked with" one of three things [32021R0782:A:w058:1][32021R0782:A:w059:1]: (a) extraordinary circumstances "not connected with the operation of the railway, such as extreme weather conditions, major natural disasters or major public health crises" that it could not avoid despite due care; (b) fault on the passenger's part; or (c) third-party behaviour it could not avoid despite due care, "such as persons on the track, cable theft, on-board emergencies, law enforcement activities, sabotage or terrorism". Exception (c) does not cover the railway's own staff strikes, acts or omissions of another undertaking on the same infrastructure, or acts or omissions of infrastructure and station managers [32021R0782:A:w059:1]; a recital (explanatory text of the Regulation, not an operative article) adds that weather must have "the character of an exceptional natural catastrophe, as distinct from normal seasonal weather conditions such as autumnal storms", and that the railway should bring any supporting documents to passengers' attention [32021R0782:A:w019:1][32021R0782:A:w020:1]. On Member State exemptions: countries may exempt international services "of which a significant part, including at least one scheduled station stop, is operated outside the Union", and countries with older exemptions may exempt domestic services from Article 19 for up to five more years [32021R0782:A:w029:1][32021R0782:A:w028:1]; as worded, neither seems to fit Madrid–Paris, and delay the railway shows happened outside the Union does not count [32021R0782:A:w056:1]. Separate from compensation, an expected arrival delay of 60 minutes or more triggers a choice of refund or continuation/re-routing [32021R0782:A:w049:1][32021R0782:A:w050:1], plus free meals and refreshments "in reasonable relation to the waiting time" and accommodation if a stay becomes necessary (which may be capped at three nights in exception cases) [32021R0782:A:w060:1]; to apply all this, please tell me the price you paid, whether it was a single or return (and whether the ticket shows a price per leg), whether Madrid–Paris was one ticket or through-ticket, whether you were told of the delay before buying, and what cause the railway gave.

NOT ESTABLISHED: Whether Spain or France has notified any exemption affecting this service, and any rail-specific Commission guidance (the only guidance in the corpus covers air travel); all citations are from Regulation (EU) 2021/782, legislation in its 2021 original text, not consolidated. This is information from the texts, not legal advice for your case.

## Main agent → user (final reply)

NEED DETAILS: The corpus-researcher subagent searched rail Regulation (EU) 2021/782. A 90-minute delay qualifies for compensation, but the amount depends on facts I don't have yet.

**Compensation for a 90-minute delay**
- **Amount:** "25 % of the ticket price for a delay of 60 to 119 minutes". It rises to 50% from 120 minutes. You keep your right to travel, and it applies only if your ticket cost "has not been reimbursed in accordance with Article 18" [32021R0782:A:w054:1].
- **The delay that counts** is between the departure and final destination "stated in the ticket or through-ticket" [32021R0782:A:w054:1].
- **Price it's based on:** "the full price which the passenger actually paid for the delayed service". For a return ticket, it's the price shown for that leg, or half the ticket price if no leg price is shown. Other multi-leg tickets are calculated in proportion to the full price [32021R0782:A:w055:1][32021R0782:A:w056:1].
- **Payment:**
  - It's due within one month of your request.
  - The railway may pay in vouchers if their terms are flexible, but must pay money if you ask.
  - It can't deduct transaction fees.
  - It may refuse to pay amounts under a threshold of at most EUR 4 per ticket.
  [32021R0782:A:w057:1][32021R0782:A:w058:1]

**When you get no compensation**
- You were "informed of a delay before buying a ticket" [32021R0782:A:w058:1].
- After you continued your trip or were re-routed, the delay "remains below 60 minutes" [32021R0782:A:w058:1].
- The railway "can prove" the delay was "caused directly by, or was inherently linked with" one of these [32021R0782:A:w058:1][32021R0782:A:w059:1]:
  1. Extraordinary circumstances "not connected with the operation of the railway, such as extreme weather conditions, major natural disasters or major public health crises", which it could not avoid despite due care.
  2. Fault on your part.
  3. A third party's behaviour it could not avoid despite due care, "such as persons on the track, cable theft, on-board emergencies, law enforcement activities, sabotage or terrorism".

**Limits on those exceptions**
- The third-party exception does **not** cover strikes by the railway's own staff. It also doesn't cover acts or omissions of another rail company on the same infrastructure, or of infrastructure or station managers [32021R0782:A:w059:1].
- A recital (explanatory text in the Regulation, not an operative article) says weather must have "the character of an exceptional natural catastrophe, as distinct from normal seasonal weather conditions such as autumnal storms". It also says the railway should show passengers any supporting documents [32021R0782:A:w019:1][32021R0782:A:w020:1].

**Member State exemptions**
- Countries may exempt international services where "a significant part, including at least one scheduled station stop, is operated outside the Union" [32021R0782:A:w029:1]. Some may also exempt domestic services for a limited time [32021R0782:A:w028:1].
- As worded, neither seems to fit a Madrid–Paris trip.

**Other remedies (separate from compensation)**
- **Refund or re-routing:** if a delay of 60 minutes or more is expected on arrival, you can choose a refund or continuing / re-routed travel [32021R0782:A:w049:1][32021R0782:A:w050:1].
- **Assistance:** free meals and refreshments "in reasonable relation to the waiting time", and accommodation if an overnight stay becomes necessary [32021R0782:A:w060:1].

**To work out your amount, please tell me:**
1. How much you paid.
2. Whether it was a single or a return, and whether the ticket shows a price for each leg.
3. Whether Madrid–Paris was on one ticket or through-ticket.
4. Whether you were told about the delay before you bought the ticket.
5. What cause the railway gave for the delay.

All citations are from Regulation (EU) 2021/782 as originally published in 2021. That's legislation, but not the current consolidated text. This is information from the texts, not legal advice for your case.

NOT ESTABLISHED: Whether Spain or France has notified an exemption that covers this service. The corpus also has no Commission guidance on rail; the only guidance it holds is about air travel.


*Run: 2 main-agent turns, 58 s.*
