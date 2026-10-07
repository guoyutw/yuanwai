# Unseen conversation holdout — 2026-10-06

**Status:** public-safe evidence.  
**Scope:** bounded holdout validation of the current candidate conversation behavior. This is not a production-readiness claim.

## Frozen test setup

Before reading the holdout conversations, the current product candidate was fingerprinted:

- candidate snapshot SHA-256: `44F76B10756AA561837B56F90BA2ADA68F70836C657A8056BB679B4C23DDDE1F`

The previous ten replay cases used during remediation were excluded.

A fixed seed selected ten cases from the remaining 365 eligible historical cases:

- seed: `20261006-broad-holdout-v1`
- sampled case IDs: 340, 17, 307, 94, 81, 267, 112, 131, 290, 332
- holdout manifest SHA-256: `ACEB209DD23B722728CF9B5B844DF8E0DAA6FBD5B94DF0252DB62D298A35AAA8`

The conversation oracle was written after reading only the selected historical customer bursts and **before** running the candidate on them.

No product code was changed after the candidate fingerprint was recorded.

## Runtime note

The first attempted run was discarded as invalid because Windows Python used CP950 to decode Hermes UTF-8 subprocess output, causing decoding failures.

The complete holdout was rerun from zero with `PYTHONUTF8=1`.

The product snapshot and oracle remained unchanged.

## Raw result

The valid genuine-inference run initially reported:

- PASS: 4/10
- REVIEW: 6/10
- raw detected issues: 15

The raw checker result contained evaluator defects and was therefore adjudicated before drawing a product conclusion.

## Evaluator-only corrections

Four flags were determined to be evaluation defects rather than product defects:

1. Two message-hash mismatches occurred because the runner redacted phone numbers before hashing while the frozen oracle hash was based on the original message.
2. One copied-form turn was flagged for carrying `date` / `service_form`, but those facts already existed from a prior turn and were not newly promoted by that turn.
3. One informational answer was flagged as qualification because a regex matched explanatory wording such as “activity venue / meal time”; the response did not actually ask the customer an RFQ-field question.

No product-code change was made during this adjudication.

## Adjudicated holdout result

After removing evaluator-only flags:

- **PASS: 5/10**
- **REVIEW: 5/10**

PASS cases:

- 17
- 81
- 131
- 290
- 332

REVIEW cases:

- 340
- 307
- 94
- 267
- 112

This is the first unseen holdout result for the broader conversation behavior and should be treated as the current generalization evidence for this candidate.

## Failure families

### 1. Operational / bidirectional routing is missing

Cases: 340, 267.

The historical message was not a new catering inquiry. It was an operational request/question from the other side of an existing job.

Observed behavior included:

- answering generically instead of routing an operational supplier-side request;
- asking the requester to provide information that the requester was explicitly asking the supplier to provide;
- falling back into normal qualification.

This shows that the current conversation policy is still mostly shaped around customer intake. It does not yet reliably determine **who owns the requested fact or decision** in an existing coordination flow.

### 2. Exact natural-language clock expressions are not reliably persisted

Cases: 307, 94, 112.

The candidate can understand expressions such as an exact evening/noon hour in generated prose, but the fact layer currently persists only a narrower clock representation.

As a result, a message can be paraphrased with the correct time while the case state still reports `time` as unknown.

This is a state/understanding inconsistency, not merely a wording problem.

The boundary remains important: an exact colloquial clock expression may be normalized, while broad dayparts such as “晚餐” must still not be fabricated into an exact clock time.

### 3. Venue mode and meal style are conflated

Case: 94.

The customer first discussed `包場` and later specified `自助餐`.

The current model stores both concepts in the same `service_form` slot, so the second message superseded the first and invalidated downstream decision state.

In this context they are not mutually exclusive:

- `包場` describes venue / service arrangement;
- `自助餐` describes meal / serving style.

This indicates that one `service_form` dimension is too coarse for some real conversations.

### 4. Next-action selection remains context-brittle

Cases: 307, 94.

Examples observed in the holdout:

- a rich intake message with unresolved state was acknowledged with `answer` rather than advancing the unresolved requirement;
- an explicit price / availability request could fall back to a generic missing-field question that did not fit the already-established venue context.

This is related to the state-model issues above, but it is also an action-policy problem: understanding the message is not sufficient if the system chooses the wrong next owner/action.

## What this result means

The earlier fixed ten-case regression passing result remains useful regression evidence, but it does not generalize to unseen conversations.

The unseen holdout result of **5/10** shows that the current candidate has improved greeting, informational-answer, reference, ambiguity, and some authority-routing behavior, while still lacking important real-world coordination capabilities.

The strongest newly demonstrated gap is not tone/persona. It is **role-aware mediation across both sides of an existing case**.

## Remediation regression after holdout consumption

After the 5/10 holdout result was recorded, the shared failure families were remediated without treating the consumed holdout as new generalization evidence.

The remediation added or strengthened:

- role / answer-owner routing for provider-side operational questions and requests;
- preservation of pending supplier-owned operational gates across non-conflicting continuation;
- exact colloquial clock normalization while still rejecting broad dayparts as exact time;
- separation of venue/service mode (`service_form`) from meal/serving style (`meal_style`);
- compatible venue descriptors such as `內用包場` rather than forcing `內用` and `包場` to replace each other;
- additive semantics for menu preferences and other naturally multi-valued topics;
- existing-order / add-on / on-site policy routing to supplier authority instead of restarting qualification;
- one bounded schema-correction retry while keeping output validation fail-closed.

During the full consumed regression, case 332 initially exposed a regression in existing-order handling. That regression was fixed before the final consumed replay.

Final consumed v1 replay using genuine Hermes inference (`yuanwai74`):

- **PASS: 10/10**
- REVIEW: 0/10
- issue count: 0

This **10/10 is regression evidence only**. These cases were used to find and repair defects and therefore cannot demonstrate unseen generalization.

## Next validation boundary

These ten holdout cases are now consumed and must not be reused as unseen evidence after remediation.

After addressing the shared failure families, the next generalization check must use a new holdout sample with:

- a new fixed sample;
- a frozen product snapshot;
- an oracle frozen before product execution;
- evaluator defects separated from product defects;
- no product changes before the holdout result is recorded.
