# Issue #70 B1/B2 remediation delta v0.4

**Status:** remediation candidate for same-reviewer re-review. B3 remains accepted from v0.3 and is unchanged.

## Corpus anchor

Same private corpus, re-read in place: 375 CSV / 21,425 messages; SHA-256 `C0A8A8C604D29EC4C1C05AC11722629A8BD8EE4B0498A09D746BEF9EA61DB399`.

Entrypoint: `scripts/qualification_schema_remediation.py`.

## B1 — automatic-message exclusion

The previous proxy was contaminated by repeated LINE OA automatic/canned messages. v0.4 changes the event rule:

A candidate supplier follow-up must be an `Account` message that:

1. contains a field term and a question/request marker;
2. occurs before the field appears in an earlier `User` message;
3. is **not** a repeated/canned message: normalized identical text occurring in at least 5 cases is excluded, as are known greeting/template markers (`您好(Brown)`, `如果您想要預訂`).

This excludes the automatic-message contamination before counting. The resulting non-automatic candidate events are:

- date: **58**
- time: **58**
- budget/price: **42**
- dietary: **41**
- location: **41**
- quantity/headcount: **39**
- menu/meal detail: **30**
- access/logistics: **21**
- invoice/admin/payment: **18**
- equipment/setup: **8**
- service type/form: **2**

These remain an operational proxy rather than causal proof, but they are no longer presented as raw supplier-follow-up counts. The results now support a narrower claim: after removing repeated/canned automation, date/time are the most recurring candidate missing-information prompts, followed by budget, dietary, location, quantity and menu; setup/access/admin are context-specific. No field is promoted to universal required.

## B2 — event definition/code alignment

The previous implementation incorrectly allowed bare `報價`/`報價單` tokens and future/question forms. v0.4 now uses the same strict rule in prose and code:

A price/proposal event is the first `Account` message containing an explicit numeric amount with `元/萬/万` (Arabic or supported Chinese numeral form), **and** containing neither a question marker nor future/offer wording such as `之後`, `再提供`, `會再`, `預計`, `希望`, or `可以提供`.

The new strict event result is:

- **92 cases**
- median event position: **32**
- quote-token-only messages are excluded by construction
- question-like and future/offer-only messages are excluded by construction

User-field presence relative to this strict event (cases can contain multiple fields):

- service type: 90 pre / 0 post
- quantity: 89 pre / 3 post
- time: 68 pre / 7 post
- budget: 70 pre / 7 post
- menu: 64 pre / 12 post
- location: 55 pre / 7 post
- date: 50 pre / 10 post
- invoice/admin: 36 pre / 26 post
- equipment/setup: 17 pre / 12 post
- access/logistics: 6 pre / 10 post
- dietary: 7 pre / 3 post

The earlier v0.1 provenance remains corrected and unchanged: **222 / median 14** belongs to the earlier broad detector; **210** belongs to the later strict taxonomy, with no median-14 attribution. Those figures are not combined with this new 92-case event set.

## Boundary

This delta changes only B1/B2 evidence and wording. B3's accepted 16-case bounded raw validation is retained from v0.3. No AI implementation, model selection, marketplace, quoting automation, or canonical schema promotion was performed.
