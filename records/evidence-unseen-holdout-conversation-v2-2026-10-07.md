# Unseen conversation holdout v2 — 2026-10-07

**Status:** Public-safe evidence; local candidate worktree only.  
**Scope:** Frozen-candidate, unseen holdout validation of Yuanwai conversation behavior. Not a production-readiness claim or a canonical product-state update.

## Frozen evaluation setup

The candidate product snapshot was recorded before the v2 sample was read or the model ran:

- Product snapshot SHA-256: `98D9FA944A9181B4CCD497CDE54D50D9E751C4BC5784BAB94F8E6A97C0994FB2`
- Snapshot scope: `yuanwai_simulator.py`, `yuanwai_voice.py`, `line_e2e.py`
- Selection seed: `20261007-broad-holdout-v2`
- Eligible historical cases after exclusions: 355
- Selected case IDs (sample order): 52, 53, 249, 373, 186, 88, 104, 289, 288, 21
- Sample manifest SHA-256: `83EE65E58F2C03B6949CD52047B1F6F4A2F3274E38D0294880E38163D282FB2A`
- Oracle version: `holdout-conversation-v2`

The selection excluded the 20 cases already used in earlier narrow replay and holdout v1. The v2 oracle was written from the selected initial customer bursts **before** executing the product. It scored bounded action selection, fact presence/preservation, authority boundaries, and ambiguity handling rather than requiring particular sentence wording.

The execution used genuine Hermes inference (`yuanwai74`) through a local replay harness with `PYTHONUTF8=1`. No product-code correction was made during this v2 unseen run.

## Raw result (preserved)

- **PASS: 7/10**
- **REVIEW: 3/10**
- Raw checker issue flags: **5**
- PASS cases: 249, 373, 186, 88, 104, 289, 288
- REVIEW cases: **52, 53, 21**

This is the recorded first unseen result for candidate snapshot v2. Do not replace it with later remediation regression scores.

## REVIEW evidence and classification

### Case 52 — Mixed intent / action ownership

A single message combined service-policy questions and a request for current menu/reference material. The candidate chose `reference` rather than `human_gate`.

Observed issue: `action_mismatch:supplier_policy_and_current_menu:reference`.

**Product failure:** the reference request displaced other questions requiring supplier-owned decisions or current supplier information. This exposes a multi-intent / multi-action routing gap, not a voice/persona issue. A safer mediator must preserve all requested sub-actions and route supplier-controlled answers without inventing policy.

### Case 53 — Exact time format missing from case state

A rich intake included an explicit compact time expression (`下午1400`). The model retained date, headcount, location, meal style, and menu preferences, but failed to persist a canonical `time` fact.

Observed issues: `missing_required_topics:time` in turn 3 and `lost_prior_topics:time` in turn 4.

**Product failure:** one underlying time-extraction/state gap produces the two related flags. `下午1400` should be treated as an explicit clock time when safely normalized; broad dayparts must still not be converted to invented exact times.

An additional turn-4 `oracle_message_hash_mismatch` is **evaluator-only**, caused by inconsistent message canonicalization / redaction between the frozen oracle hash and replay input. It is not counted as a separate product defect. No customer contact details are reproduced here.

### Case 21 — Ambiguous numbers promoted to budget

A pricing question contained an ambiguous numeric range with mixed notation. The candidate selected an acceptable question-asking action but also promoted an unconfirmed interpretation into the `budget` field.

Observed issue: `forbidden_topics_promoted:budget`.

**Product failure:** numeric ambiguity must stay unresolved until clarified; do not convert uncertain price/headcount language into authoritative case facts. This case is about certainty/provenance, not only the next-action label.

## Result interpretation

One of the five raw issue flags is a checker-only hash mismatch. The other four flags concern three product failure families: mixed-intent/answer-owner routing (52), compact explicit-time extraction/preservation (53; two related flags), and ambiguous-number certainty (21).

Removing the hash mismatch **does not change the case outcome**: the product still has 7 PASS / 3 REVIEW under the frozen v2 oracle.

The seven passing cases provide bounded evidence that several earlier fixes generalized to new conversations, including informational explanations, service/meal-style separation, and some authority routing. They do **not** prove correctness for long conversations, multimedia, actual supplier delivery, or live LINE production behavior.

## Consumption and next gate

**All ten v2 cases are now consumed.** They may be retained as regression examples after remediation but must never be presented as fresh unseen/generalization evidence.

Next bounded work:

1. Preserve the original 7/10 baseline and evaluator-only correction separately.
2. Remediate the three product failure families with shared rules and deterministic regression, not case-ID special cases.
3. Freeze a new candidate snapshot and a new v3 unseen sample/oracle before the next genuine inference run.

No customer raw messages, personal identifiers, phone numbers, supplier-private details, or other source CSV contents are included in this public-safe record.

**Writeback boundary:** This file records experiment evidence only. It does not authorize modifying canonical CURRENT_STATE, committing, pushing, merging, or declaring production readiness.
