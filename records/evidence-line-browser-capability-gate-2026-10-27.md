# Evidence — public-source gate for LINE browser-operated drafts

**WORK_ID:** `yuanwai-line-browser-capability-gate-20261027-01`
**Research mode:** public official documentation only; no LINE login or UI operation.
**Baseline:** isolated clean worktree `a2116e5711633f912f12ead3c5116557a0aa11b2`.

## Findings from primary sources

- LINE Taiwan's FAQ describes 「預設訊息」 as reusable reply-example text that staff select to reply to recurring questions. The quick-start manual likewise describes choosing a preset from chat to reply. These sources support **reusable template**, not a customer-specific saved draft.[1][2]
- LINE's one-to-one scheduled-message feature can prepare a message and automatically send it at a specified date/time. That is not equivalent to an unsent per-chat proposal, and must not be used as a no-send substitute.[3]
- LINE documents a separate broadcast-message draft list and saved broadcast drafts. That is evidence of a draft feature in a different workflow, not proof that a one-to-one customer chat has a private unsent draft.[4]
- xAI's product documentation describes browser-capable cloud computers, drafts that await approval, and human handoff when sites block automation or require human steps. This is vendor-level capability documentation, not a reproduction against LINE OA Manager.[5]

## Verdict

**Native customer-specific per-chat draft: UNKNOWN / NOT VERIFIED.** The reviewed public LINE material does not establish that such a feature exists; it also does not prove that no UI or external staged workflow can create one. Preset messages are reusable templates. Scheduled one-to-one messages can send automatically. Broadcast drafts are a different object/workflow.

**Resume, isolation, no-send, and human-send handoff: UNKNOWN for LINE OA/browser operation.** No authenticated UI evidence or controlled test was performed, so recipient binding, persistence across session resume, separation of per-customer proposals, prevention of sends, and operator handoff remain unproven.

**Transport hypothesis: REVISE (unvalidated option only).** Keep the previously reviewed webhook E2E as baseline. Its reviewed synthetic transport, persistence, human gate, authorization/delivery boundary and ordered trace exceed the browser option's present evidence. No trustworthy comparison of handling time or maintenance burden is available. This does not claim webhook is inherently better in every future context; it says the browser route has not yet earned a capability or efficiency claim.

## Safest next validation

No owner action is required now. If the owner later chooses to proceed, first require a separate explicit permission gate for an authorized synthetic test account, named human operator and observer, and stop conditions. Then inspect only public/test-account UI for per-chat draft identity, session-resume persistence, cross-case isolation, a verifiable no-send state, and explicit human-send handoff. Do not alter webhook settings, use real customers, send or schedule any message, or work around login/automation controls. If the UI cannot make no-send and recipient binding observable, stop with `UNKNOWN`/`UNSUPPORTED`.

## Boundaries and comparison gaps

This completed public-documentation review did not access LINE, an OA, customer data, credentials, test accounts or private systems; did not send/schedule messages; did not change deployment or webhook settings; and did not modify Hermes Issue #88. It cannot prove browser operation, native draft retention, session-resume behavior, no-send guarantees, or comparative human effort/maintenance cost. No owner decision to adopt, reject, or deploy is inferred.

## Sources

[1] LINE Biz-Solutions, FAQ — 「許多顧客會詢問同樣問題，我只能花時間一題一題回覆嗎？」
https://tw.linebiz.com/faq/oa-chat/72

[2] LINE Biz-Solutions, Official Account quick-start manual — 「預設訊息」
https://tw.linebiz.com/manual/line-official-account/book2

[3] LINE Biz-Solutions, Official Account chat — scheduled messages
https://tw.linebiz.com/manual/line-official-account/oa-chat-scheduledmessage

[4] LINE Biz-Solutions, Official Account — message sending / broadcast drafts
https://tw.linebiz.com/manual/line-official-account/oa-manager-sendmsg

[5] xAI, Grok Bot overview
https://docs.x.ai/grok-bot/overview
