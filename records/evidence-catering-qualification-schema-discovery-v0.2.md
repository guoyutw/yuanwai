# Evidence: 375-case qualification schema discovery v0.2

**Status:** public-safe durable analysis artifact; candidate evidence, not canonical product schema.
**Origin:** Issue #70 (frozen scope).

## 1. Corpus identity and reconciliation

The canonical private raw corpus is the ZIP supplied by the owner and kept outside this public repository:

- CSV files: **375**
- messages after the first three metadata rows and the fourth header row: **21,425**
- ZIP SHA-256: `C0A8A8C604D29EC4C1C05AC11722629A8BD8EE4B0498A09D746BEF9EA61DB399`
- verified owner-supplied private copy used for this run (physical path intentionally not recorded here)
- the owner separately verified the Downloads, OneDrive, and Downloads archive copies have the same SHA-256.

The deterministic readback opened all 375 CSV members, skipped exactly the first three metadata rows plus the header, and counted 21,425 non-empty message rows. No raw filename, message, customer identity, contact detail, or private price is emitted by the analysis entrypoint.

## 2. Reproducible entrypoint

`/scripts/qualification_schema_discovery.py` is a public-safe deterministic lexical census. It accepts a private ZIP path and writes an aggregate JSON report only. The generated private report is not committed here. It records the corpus hash, file/message totals, case-level observed information, first-customer-message observations, supplier-question-message count, and price-signal position summary.

This is a bounded mixed-method pass, not a claim that lexical matching alone proves a field requirement:

1. deterministic full-corpus census;
2. readback of the existing public-safe v0.1 evidence and candidate brief;
3. bounded raw sample readback during execution;
4. explicit separation of observed presence from requirement, timing, and supplier decision.

## 3. Full-corpus observed information types

The lexical census found at least one matching signal in the following number of cases (out of 375):

- service type / service form: **353**
- quantity / headcount: **320**
- time / time window: **263**
- menu / meal details: **242**
- budget / price language: **230**
- location / area: **200**
- date: **185**
- invoice / administration / payment language: **137**
- equipment / setup / staffing: **71**
- access / logistics: **47**
- dietary requirements: **34**

These are **observable lexical presence counts**, not completion rates and not universal requirements. Terms can occur in supplier messages, later corrections, or unrelated context.

## 4. First-contact observations

In the first customer-attributed message, the deterministic signal counts were:

- service type / service form: **266 / 375**
- quantity / headcount: **52 / 375**
- menu / meal details: **27 / 375**
- time / time window: **40 / 375**
- budget / price language: **33 / 375**
- location / area: **25 / 375**
- date: **10 / 375**

The first-contact result supports the existing progressive-qualification observation: inquiries are commonly incomplete. It does **not** establish that low first-contact frequency means low importance; date and location can be asked or supplied later because they gate availability and serviceability.

## 5. Field-role classification

The following is the evidence-supported working classification for the next contract design. It is deliberately not a universal required/optional form.

### Routing / Gating

- **Service type / service form:** strongest early routing signal; distinguishes at least delivery/takeaway, onsite catering, buffet/meal service, and venue/banquet-like requests in the corpus vocabulary.
- **Date and serviceability/location:** availability and feasibility gates. They are often absent at first contact but can block a meaningful supplier response later.

### Conditional Qualification

- **Headcount / quantity:** commonly relevant to feasibility and pricing, but not universal in the opening message.
- **Time window:** conditional on service form and schedule; often becomes important after the date or service type is known.
- **Menu, dietary requirements, equipment/setup, access/logistics:** conditional on service type, venue, and requested service level.

### Post-Quote / Fulfillment

- **Exact menu revisions, final quantity, exact time, equipment/setup details, access/parking, invoice/tax ID, deposit/payment administration:** typically later-stage or fulfillment information in the existing evidence. They should not be promoted to first-turn gates without new live evidence.

### Supplier Decision

- **Price/proposal amount, minimum spend, acceptance of serviceability, feasible package/menu, staffing/equipment commitment, deposit/payment terms:** these are vendor judgments or commitments, not customer-information fields. A state contract may record them as decision outputs or gates, but should not model them as merely “missing customer fields.”

## 6. Timing and price signal

The new entrypoint detected a supplier-side price-language signal in **312** cases, with a median detected message position of **3**. This detector intentionally uses broad lexical terms and is not comparable to the earlier v0.1 strict price taxonomy; the denominators must not be combined.

Accordingly:

- service type, rough location/serviceability, date availability, and rough quantity are plausible pre-price qualification inputs, with conditionality;
- exact menu, final quantity/time, logistics, administration, and payment commonly remain later-stage candidates;
- a lexical price hit is not proof of a formal quote or business commitment.

The existing v0.1 evidence remains the authority for the stricter historical path estimate (210 cases; median 14 messages). This v0.2 detector does not replace it.

## 7. Answers to the seven frozen questions

1. **What customers provide:** service form, rough quantity, timing/date, location, menu/meal requirements, budget/price language, and occasional dietary/logistics/administrative details; prevalence varies greatly.
2. **When it appears:** service form is most visible at first contact; date/location/time/quantity and detailed service constraints often appear progressively; fulfillment/admin information is later.
3. **What causes supplier follow-up:** supplier question messages are common (**2,869** lexical question-message hits), but this run does not claim causal attribution or a field-specific re-ask rate. A follow-up ledger is required before promoting such a claim.
4. **Service-type conditionality:** observed vocabulary and the existing five-case qualitative review support meaningful differences between delivery/takeaway, onsite catering, buffet/meal service, and venue/banquet-like requests. Population-level conditional rates remain an evidence gap.
5. **Before versus after price:** rough routing/serviceability/date/quantity information can precede a useful price signal; menu finalization, logistics, administration, payment, and supplier commitments are often later or conditional. Exact field-by-field timing needs a stricter event annotation pass.
6. **Supplier decisions:** price/proposal, feasible package, serviceability acceptance, staffing/equipment commitment, and payment terms are supplier decisions/commitments, not missing customer fields.
7. **Different qualification paths:** yes, the evidence supports conditional paths rather than one universal questionnaire; exact path rules remain provisional until service-type annotation is completed.

## 8. Safe promotion versus provisional items

**Safe to promote as contract concepts (not mandatory fields):**

- preserve known information;
- classify service form before asking generic questions;
- treat date/location as feasibility gates;
- ask headcount/time/menu/logistics conditionally;
- keep supplier decisions separate from customer-provided information;
- produce a supplier-ready brief with explicit unknowns and provenance.

**Remain provisional:**

- any universal required-field list;
- fixed question ordering for every service type;
- field-specific supplier re-ask rates;
- causal claims that a field shortens time to price;
- automated quote or commitment behavior;
- population estimates for the qualitative service-type differences.

## 9. Evidence gaps and stop boundary

The following are intentionally not inferred from this pass:

- exact customer-versus-supplier attribution for every field;
- field-level re-ask behavior and whether a customer had already supplied the value;
- strict first-price versus price-question versus formal-quote event timing;
- statistically bounded service-type cohorts;
- manual validation of every high-impact classification.

The artifact is sufficient to design the next **Yuanwai State / AI Operating Contract 0.1** around progressive, conditional qualification, but it does not freeze that contract and does not implement any AI loop, model architecture, marketplace, quoting automation, or vendor system.
