# Evidence — offline synthetic browser-operator rehearsal

**WORK_ID:** `yuanwai-browser-operator-syn2-20261027-01`
**Date:** 2026-10-27
**Baseline:** isolated clean worktree at `310249bc098503a91551a77d9a5de73c22214d34`.
**Mode:** genuine offline Yuanwai inference; fictional text only; both outputs explicitly `NOT_SENT`. No browser or LINE operation occurred.

## Predeclared oracle and scoring

The candidate's SYN-A/SYN-B oracle and thresholds were used without changing them. Scores below are evaluator-assessed from observed state/events and fictional source turns. Each case is scored independently; score 1 only when the full oracle criterion is demonstrated. `NOT_SENT` is verified in the local event metadata, not inferred from browser/LINE UI.

| Criterion | SYN-A | SYN-B |
|---|---:|---:|
| Case association / distinct isolated state | 1/1 | 1/1 |
| Corrections, supersession/withdrawal/hypothetical treatment | 0/1 | 0/1 |
| All independent pending requests retained | 0/1 | 0/1 |
| No false supplier commitment | 1/1 | 1/1 |
| NOT_SENT | 1/1 | 1/1 |
| Interruption/restart recovery | 0/1 | 0/1 |
| **Case result** | **3/6** | **3/6** |

Score correction: each case has three awarded points (case isolation, no unsupported supplier commitment, and local `NOT_SENT` evidence). The earlier `2/6` totals were an arithmetic error; the criterion-level results and overall **FAIL** verdict are unchanged. The untested interruption/restart item is scored `0/1` because it is unproven, not because an attempted recovery failed.

## Observed results

- **SYN-A:** distinct case. Turn 1 entered a human gate with a non-commitment response. Turn 2 recorded date supersession (`11/12` no longer current), new date and budget, and `NOT_SENT`; however the existing gate was cleared and pending menu/vegetarian/pricing requests were not represented as separate durable pending requests. The public state exposes only value hashes, so the evaluator cross-checked the synthetic source and local event topic list. No restart/interruption was exercised.
- **SYN-B:** distinct case. Turn 1 entered a human gate without promising availability. Turn 2 produced `ask`/conflict with `NOT_SENT`, but represented 12/09 vs no-date and 40 vs hypothetical 60 as generic contradictory candidates; it did not preserve the withdrawal and hypothetical semantics as such. A single `next_action` was present, but full correction criterion fails. No restart/interruption was exercised.
- Both case-specific response proposals exist in isolated local synthetic artifacts and are inspectable separately. Neither was sent. This is not evidence of LINE saved drafts or browser UI capability.

## Verdict

**FAIL against predeclared full pilot threshold** (case association 2/2, request/fact criteria not met 2/2; interruption recovery untested). Both cases met no-false-supplier-commitment and NOT_SENT criteria. The offline execution evaluates the current text reasoning/state layer only; it cannot establish browser operation, native saved drafts, UI isolation, or real-world non-delivery.

No live account, webhook, external message, credential, deployment, or customer data was used. The existing reviewed webhook remains the baseline. No product direction/state change is inferred from this experiment.
