# Historical replay — broader conversation oracle evidence

**Date:** 2026-10-06
**Status:** public-safe candidate evidence. This is bounded validation, not a production-readiness claim.

## Why this re-evaluation was necessary

A prior fixed-batch replay reported 10/10 PASS under a structural oracle focused on:

- explicit fact extraction;
- known-fact re-asking;
- canonical time;
- premature supplier human gate;
- reference requests;
- date ambiguity and recovery.

Live LINE probing then exposed failures that the historical sample had actually contained but the structural oracle did not score:

- greeting / opening-context handling;
- informational questions that should be answered rather than turned into qualification;
- action-selection fidelity between inference and final state/action;
- malformed pseudo-topics that are intent metadata rather than durable case facts.

Therefore the earlier 10/10 result must be read narrowly: it showed that the tracked structural failure families were not reproduced. It did **not** establish conversation correctness.

## Same fixed batch, broader oracle

The same ten historical cases were re-evaluated. No new cases were added for this comparison.

The broader local-only oracle retained the structural checks and added bounded conversation expectations for:

- greeting-only turns;
- self-introduction / opening context;
- informational service-form questions;
- reference requests;
- action fidelity for `answer` and `reference`;
- ambiguity handling;
- customer-facing internal-jargon leakage.

Private customer text remains outside this public record. Local evaluation uses case/turn identity and hashes.

### First broader pass

Result:

- **6 / 10 PASS**
- REVIEW: 375, 333, 314, 362
- 20 detected issues

The four REVIEW cases exposed three shared failure families rather than four unrelated case-specific defects.

### Shared failure family 1 — opening context became event facts

A self-introduction/background turn could be interpreted as an event location and immediately trigger RFQ qualification.

Correction:

- bounded opening-context detection;
- self-introduction/background is not promoted to event location without an explicit event-location signal;
- opening context receives a conversational response rather than starting a field questionnaire.

### Shared failure family 2 — informational intent became qualification

Service-form questions equivalent to “I want to understand X” were often classified as `ask`, causing the system to request date/headcount/etc. before answering the user’s question.

Correction:

- `answer` is a first-class action;
- structured inference includes bounded `answer_text`;
- service-form information/explanation intent is instructed and postprocessed to answer before qualification;
- answer content may give a concise general explanation but must not invent supplier availability, acceptance, price, policy, payment, discount, or fulfillment commitments.

### Shared failure family 3 — pseudo-topic caused hard failure

One genuine inference emitted intent metadata equivalent to `reference` as a fact topic, causing normalization to fail.

Correction:

- a narrow set of obvious non-fact metadata topics (`reference`, `intent`, `request`, `question`, `answer`) is ignored as durable facts;
- unknown non-whitelisted fact topics still fail closed.

## Rerun after shared corrections

With the same product code and same broader oracle:

- full ten-case rerun: **9 / 10 PASS**
- the sole remaining REVIEW was case 333 with one checker issue

Inspection showed case 333 had in fact:

- `primary_next_action = answer`;
- final `next_action = answer`;
- a substantive service-form explanation;
- no supplier-authority promise.

The checker had falsely classified the answer as qualification merely because the explanatory sentence mentioned “activity date” as one factor that can affect actual service details.

The oracle was narrowed so an informational answer is only flagged as qualification when it actually asks an RFQ-field question or falls back to generic “information saved / provide next requirement” wording.

A targeted genuine-inference replay of case 333 under the corrected oracle then produced:

- **1 / 1 PASS**
- **0 issues**

No product-code change occurred between the full 9/10 rerun and the targeted corrected-oracle replay.

## Regression protection

The shared failure families are now covered by deterministic regression checks:

- opening/self-introduction context does not become semantic event facts;
- service-information intent resolves to `answer` rather than qualification;
- known non-fact pseudo-topics are not persisted as facts;
- prior understanding/state regression remains passing;
- customer-facing voice regression remains passing.

Latest local checks:

- `python scripts/voice_regression.py` → PASS
- `python scripts/replay_understanding_regression.py` → PASS
- `python yuanwai_simulator.py --scenario` → 9/9 PASS
- `git diff --check` → clean except line-ending warnings

## Current interpretation

For this fixed ten-case batch, the corrected broader oracle now has passing evidence across all ten cases.

That result is materially stronger than the earlier structural 10/10 because it now covers the conversation signals that were previously present but unscored.

It is still **not** evidence that Yuanwai is generally conversation-correct.

These ten cases have now been inspected and used to shape the remediation. They are no longer an unbiased validation set.

## Next validation boundary

The next meaningful test must use unseen historical holdout cases and preserve the broader oracle categories.

Re-running these same ten cases again is regression evidence only; it must not be used as evidence of generalization.
