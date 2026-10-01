# Evidence: Issue #70 bounded remediation v0.3

**Status:** remediation candidate for re-review; public-safe, not canonical schema.
**Scope:** B1 field-level follow-up evidence, B2 strict price-event timing, B3 bounded manual/raw validation.
**Origin:** same frozen Issue #70 and same candidate; no scope expansion.

## Corpus anchor

The same private ZIP was re-read, not copied into this repository:

- 375 CSV members
- 21,425 non-empty message rows after 3 metadata rows + 1 header row per CSV
- SHA-256 `C0A8A8C604D29EC4C1C05AC11722629A8BD8EE4B0498A09D746BEF9EA61DB399`

The remediation entrypoint is `scripts/qualification_schema_remediation.py`. It emits only aggregate counts and selected case indices.

## B1 — Which missing information actually triggers follow-up?

### Operational event definition

For this bounded pass, a **candidate supplier follow-up** is an `Account` message containing a field-term plus a question/request marker, where that field had not appeared in an earlier `User` message in the same conversation. This is a reproducible event proxy, not a causal claim about every supplier decision. The event was then checked against a bounded raw sample below.

Full-corpus candidate follow-up events:

- date: **252**
- location: **238**
- time: **246**
- quantity/headcount: **200**
- menu/meal detail: **234**
- equipment/setup: **225**
- budget/price: **222**
- dietary: **45**
- invoice/admin/payment: **28**
- access/logistics: **23**
- service type/form: **14**

These are event counts, not unique conversations and not universal requirements. The highest recurring missing-information triggers in this proxy are date/location/time/quantity/menu and setup; they should be conditional prompts, not a fixed opening form.

### Manual/raw validation of the trigger interpretation

A systematic-index bounded sample of 16 cases (indices 1, 25, 50, …, 375), covering short/long conversations and venue, onsite/offsite, tea-meal, buffet and fulfillment/admin patterns, was read directly from the private CSVs. The public record preserves only coded observations:

- **1:** supplier asked for date after service form, location, quantity and budget were supplied; validates date follow-up.
- **25:** customer supplied service form; supplier supplied service constraints; later customer asked threshold/time; validates service-form-specific qualification.
- **50:** customer supplied date/time/activity/headcount in first request; no missing-field supplier question in the inspected opening; validates “ask only missing” boundary.
- **75:** supplier asked headcount, then event type after venue/price context; validates quantity and context follow-up.
- **100:** customer supplied location/date/time/quantity; supplier rejected/redirected on closed day; validates date as availability gate, not generic field.
- **125:** customer explored tea/buffet alternatives; supplier’s information depended on service form; validates conditional service path.
- **150:** supplier asked date/time certainty, quantity certainty and food type; validates gate + conditional menu/service-type prompts.
- **175:** supplier supplied a generic date/time/person prompt; customer’s recurring activity required operational context; validates context-specific path.
- **200:** supplier asked/required quantity, budget, time, date and location around menu discussion; validates multi-field progressive qualification.
- **225:** conversation was already fulfillment/admin; supplier asked organizational/order details rather than opening qualification; validates later-stage admin role.
- **250:** customer supplied budget/date/location/quantity; supplier asked food type and serving format; validates menu/service-form follow-up after routing facts.
- **275:** customer supplied date/quantity/activity/time; supplier answered capacity/price and later equipment questions; validates venue/setup conditionality.
- **300:** customer supplied menu/quantity/date; supplier handled item availability and replacement; validates supplier decision boundary.
- **325:** supplier asked invoice identity/tax details in an already advanced order; validates post-quote/admin role.
- **350:** tea-meal inquiry moved to menu/style/contact details; supplier asked food-style and contact follow-up; validates service-specific path.
- **375:** customer supplied event/date/time/quantity; supplier asked location and meal type when moving to offsite catering; validates service-type branch.

The sample confirms that the proxy is detecting real supplier follow-up patterns, while also showing that the same term can be a supplier answer, a customer question, or a later fulfillment event. Therefore the counts are evidence for candidate trigger families, not proof of a universal required-field set.

## B2 — Strict pre-price/post-price timing

### Strict event definition

The first **meaningful supplier price/proposal signal** is the first `Account` message matching an explicit quote/proposal phrase or a numeric currency/unit expression (for example `報價`, `報價單`, a proposal plus `元/萬`, or a numeric amount with a currency unit). Bare customer budget questions, generic `費用/價格` mentions, and supplier questions without a proposal/amount are excluded.

This strict detector found **120 cases**, with median event position **26** (message position within the CSV conversation). Field presence was then assigned relative to that event using the first prior/after `User` occurrence:

- service type: 111 pre / 4 post
- quantity: 114 pre / 6 post
- time: 90 pre / 12 post
- location: 74 pre / 10 post
- date: 59 pre / 23 post
- budget: 88 pre / 15 post
- menu: 83 pre / 20 post
- equipment/setup: 21 pre / 19 post
- access/logistics: 5 pre / 21 post
- dietary: 8 pre / 9 post
- invoice/admin: 41 pre / 43 post

Counts are not additive: a case can contain multiple fields and some cases have fields absent from the event window. Low post counts do not mean a field is unimportant; they mean it was not observed after the strict event in this corpus/event rule.

Interpretation: service form and quantity are most consistently present before a meaningful proposal signal; time, location, date, budget and menu are common but conditional; access/logistics and invoice/admin skew later; equipment/setup is split by service context. This is a timing association, not a causal or universal requirement claim.

### Corrected v0.1 provenance

The earlier v0.1 evidence must be read exactly as:

- **222 cases, median 14 messages (p25 8, p75 22): earlier broad price detector**
- **210 cases: later stricter price taxonomy; no median-14 attribution is made**

The 222 and 210 denominators are not combined. v0.3 does not alter either historical statistic; its 120/median-26 result is a new, explicitly defined strict event rule.

## B3 — Service-type/path bounded validation

The 16-case raw readback above directly challenged the high-impact claims. It included:

- venue/inside booking: 50, 75, 150, 275, 375
- tea/meal service: 25, 100, 125, 200, 350
- offsite/outdoor or mixed service: 1, 175, 250, 375
- fulfillment/admin or item decision: 225, 300, 325

Observed path differences in the sample:

- **Venue/inside:** capacity, floor/room, date availability, hours, equipment and minimum-spend/price decisions are prominent.
- **Tea/meal:** menu style, quantity, budget, time/date and food composition are prominent; the customer may switch between tea, buffet and inside service.
- **Offsite/mixed:** location/serviceability, delivery/setup, serving format and logistics become gating questions.
- **Fulfillment/admin:** menu substitutions, invoice/tax identity, payment and organizational details occur after the commercial direction is already established.

This is bounded qualitative validation, not a population estimate. It supports conditional paths and rejects a single universal questionnaire, but does not freeze exact service-type state machines.

## Revised qualification conclusions

**Supported for the next contract as conditional concepts:** service form routing; date/location feasibility gates; quantity/time/menu prompts chosen by context; setup/logistics when onsite/offsite conditions require them; supplier-decision outputs separated from customer information; explicit unknowns and provenance in the supplier-ready brief.

**Still provisional:** field-specific causal impact, exact re-ask rates beyond the operational proxy, fixed question ordering, universal required fields, and population-level service-type rates.

No AI implementation, model selection, marketplace, automated quoting, vendor SaaS, or canonical schema promotion was performed.
