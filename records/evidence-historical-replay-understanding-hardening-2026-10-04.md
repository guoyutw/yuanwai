# Historical replay understanding hardening — 2026-10-04

## Scope

A bounded replay used one historical catering inquiry as a fake LINE customer against the reviewed Yuanwai LINE/AI/state path. The replay used genuine inference and the same local case/state adapter as Issue #75, with outbound LINE delivery disabled. Raw customer text, identity, phone number, exact address, and private supplier data are intentionally omitted here.

This was a post-#75 conversation-quality investigation, not a new production rollout.

## Observed defects

The first replay exposed four coupled understanding/state problems:

1. An explicit numeric date could be omitted by genuine model extraction, causing Yuanwai to ask for the date again.
2. A generic venue noun such as “company/office” could be treated as a concrete location, then conflict with a later coarse geographic location.
3. A previously extracted time could be restated by the model with surrounding prose, making the same time appear to have changed and incorrectly triggering recovery.
4. A request to see menu/menu-item examples could be classified as supplier fulfillment authority and enter a human gate instead of staying a non-committal reference request.

A related state issue was also confirmed: a refinement to a non-decision-affecting topic such as menu preference could trigger downstream invalidation even when no supplier decision depended on it.

## Bounded remediation

No model or external dependency was changed.

The current candidate adds a narrow post-inference hardening layer:

- canonical deterministic date parsing for obvious numeric/month-day forms;
- canonical deterministic time parsing for obvious clock forms;
- weak venue nouns are not accepted as a concrete location by themselves;
- already-known current topics are removed from the model's unknown list, preventing obvious re-asks;
- previously known date/time values remain canonical unless the current customer turn explicitly contains a new parseable date/time;
- clear requests to see/provide menu, dish, photo, or example references remain reference actions unless the same turn asks for supplier-authority decisions such as availability, acceptance, quote, price, payment, or commitment;
- non-decision-affecting fact refinements do not invalidate feasibility/supplier-decision state.

## Verification

The same bounded historical replay was rerun with genuine inference.

Observed repaired behavior:

- after an explicit date is supplied, Yuanwai advances instead of asking for that date again;
- a time-plus-generic-venue utterance retains the canonical time while still asking for a usable location;
- a later coarse location no longer creates the previous false location conflict;
- menu/menu-item requests remain in the reference/options path rather than entering a false supplier-authority gate or recovery loop.

Additional checks:

- scripts/replay_understanding_regression.py: PASS;
- existing Issue #74 scenario regression: 9/9 PASS;
- clean genuine line_e2e.py --synthetic path: PASS with same-case persistence, human-gate HOLD, authorized continuation, and public-safe evidence.

## Interpretation

Issue #75's E2E architecture remains valid. The defect was in the robustness boundary between generative extraction and deterministic state updates, not in LINE transport or the reviewed supplier-authority gate.

The useful direction is therefore to keep the current architecture and harden high-value fact normalization/state semantics before considering a model replacement. Jev/Laya/GLiNER-style alternatives remain observation candidates only; none were introduced by this remediation.
