# Candidate — Browser-operated LINE OA intake with human-reviewed reply proposals

**Date:** 2026-10-27  
**Status:** CANDIDATE / RESEARCHED / SYNTHETIC PILOT NOT RUN / NOT DEPLOYED  
**Owner authorization:** Owner explicitly delegated exploration and updating the Yuanwai repository on 2026-10-27. This does **not** grant access to third-party LINE accounts or authorize any real customer messaging, publication, money movement, deployment or credential changes.

## Discovery and limits

A third party reports that a Grok Bot can use the LINE Official Account Manager website to read messages and save four suggested replies under LINE「預設訊息」without building a new webhook integration. We have not independently reproduced the reported behavior on Yuanwai, and must not treat an anecdote as validated product capability.

Official product evidence:
- Grok Bot can operate browser-based tools with a cloud computer, but access/session expiry and automation restrictions may require human steps: https://docs.x.ai/grok-bot/overview
- LINE「預設訊息」are reusable chat reply templates, **not verified customer-specific unsent drafts**: https://tw.linebiz.com/faq/oa-chat/72/ and https://tw.linebiz.com/manual/line-official-account/book2/
- Scheduled LINE messages are a separate function and **can eventually send automatically**; do not substitute them for unsent drafts: https://tw.linebiz.com/manual/line-official-account/oa-chat-scheduledmessage/

The opportunity is to reduce custom integration work and Owner management effort for **low-volume, human-reviewed inquiry handling**, not to assume a browser robot is equivalent to a reliable webhook/API integration.

## Governing boundaries (no amendment)

- Existing synthetic LINE webhook E2E in Issue #75 was independently reviewed and remains the baseline.
- The frozen `records/contract-state-ai-operating-0.1.md` (originating Hermes issue #72) still controls fact provenance, recovery, supplier-ready, commercial authority and truthful delivery.
- `records/decision-ai-frontstage-hidden-human-gate.md` still expresses the AI-first customer interaction goal. A reviewer manually sending an AI draft is a **reduced-scope feasibility test**, not proof that this goal is satisfied.
- Hermes Issue #88 Request & Fact Boundary v0.1 has separate frozen requirements and independent review/closeout gates. Do not modify #88, consume its v3 holdout or infer that Yuanwai's older public `main` contains the latest local implementation.
- Do not alter LINE OA settings, turn off webhooks, connect real accounts or replace the existing implementation for this comparison.

## Falsifiable pilot

**Question:** Can a browser-operating AI produce separate, reviewable, source-grounded reply proposals for two fictional LINE customers **without sending anything** or confusing conversations? Does it require less human handling than the webhook baseline?

Pre-registered fictional fixtures; no real customer details:

**SYN-A** (two turns):
- 「11/12 桃園 20 人，想問外燴菜單和素食怎麼安排？也想知道價格。」
- 「日期改成 11/19；預算上限 2 萬，不是你們的報價。」
- Oracle: `11/19` current; `11/12` superseded; menu / vegetarian / pricing requests all retained separately; 2 萬 is customer budget, **not** supplier quote; no availability, menu or price commitments; next action grounded.

**SYN-B** (two turns):
- 「12/09 新竹 40 人，想知道能不能接。」
- 「12/09 不辦了，日期還沒決定。那如果改成 60 人呢？」
- Oracle: date withdrawn without invented replacement; 60 hypothetical, not confirmed headcount; supplier availability/acceptance unknown; next question or human gate as appropriate; zero details from SYN-A.

For each case, require: distinct `case_id`; input-turn provenance; current/superseded/unknown/hypothetical facts; *all* open independent requests; a single next action; separately identifiable proposed response; `NOT_SENT` and review state.

Do **not** put individualized responses into LINE's globally reusable 「預設訊息」. If the interface does not support safe per-case unsent drafts, store proposals as isolated **synthetic test artifacts outside LINE** and record `NATIVE_CASE_DRAFT_UNSUPPORTED`; don't redefine global templates as customer drafts.

### Experiment stages

1. **Offline synthetic rehearsal only:** run SYN-A and SYN-B as text fixtures against the proposed browser-operator workflow. Log output/score with no LINE login, customer data or services. An LLM producing plausible responses offline tests only reasoning, **not** browser or LINE capability.
2. **Independent gate review:** determine whether this workflow can keep each customer's draft separate, prevent sends and survive interrupted sessions. Verify evaluator access, test OA authorization, platform permissions and no live customer exposure. If any necessary item is unknown, `HOLD`.
3. **Later controlled test-account UI check (separately authorized):** with explicitly authorized synthetic LINE OA/users only, verify reading, case mapping, draft saving/reopening, human review and no-send UI evidence. Do not click Send, save scheduled outgoing messages, enable automatic replies or modify existing webhook configuration. Never infer non-delivery solely from Bot self-report.
4. **Comparison:** contrast with existing webhook E2E for correctness, case mixing, lost requests, unauthorized commitments, unintended sends, restart recovery, elapsed operator time, manual touches, recurring cost and maintainability.

### Decision thresholds

The two-case *feasibility* pilot passes only if: case association `2/2`; source-grounded facts and request preservation `2/2`; false commercial commitments `0`; unintended sends `0`; proposals individually reviewable; and no-send/restart continuation supported by observable evidence. Missing proof is `BLOCKED`, not `PASS`.

A pass would be `KEEP_AS_OPTION` pending larger reliability/privacy evaluations, **not** production approval or confirmed XP. Otherwise `REVISE` or `DROP`. A successful click-through still does not show this route reduces Owner responsibility; human handling time must be measured.

## Current evidence

- Third-party browser/preset claim: **ANECDOTAL / NOT VERIFIED FOR YUANWAI**.
- Official browser and LINE template capabilities: **DOCUMENTED**, but customer-specific unsent drafts **UNVERIFIED**.
- Offline rehearsal: **NOT RUN**. Test LINE login: **NOT ATTEMPTED**. Real messages: **NONE**. External sends: **NONE**.
- No new product contract, integration, deployment or permissions.

**NEXT ACTION:** perform the synthetic two-case *offline* rehearsal and evaluate draft isolation, pending-request preservation and no-send handling before deciding whether a separately authorized test-account UI experiment has sufficient value.
