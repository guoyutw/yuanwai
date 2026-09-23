# Yuanwai 0.1

This is the public operating record for Yuanwai, owned publicly by 哲瑜／嚕嚕米.

## Working rules

- Keep the repository public-by-default, while excluding customer PII, private LINE conversations, credentials, supplier pricing, payment/financial data, and other sensitive business data.
- Preserve the learning loop: hypothesis → build/do → real-world evidence → review → decision/pivot → durable writeback → next action.
- Promote knowledge only through evidence → candidate → canonical. Preserve superseded strategies and pivots.
- Keep exactly one visible CURRENT STATE, one NEXT ACTION, and one CLEAR CONDITION.
- Do not implement product or LINE infrastructure unless the current state explicitly selects it.

## Durable writeback gate

- **Evidence writeback:** when a completed experiment, analysis, real-world test, or investigation changes a reusable understanding of the current state, hypothesis, requirement, next action, or artifact, write a public-safe durable evidence record. Owner freeze is not required to preserve evidence that already occurred.
- **State writeback:** update CURRENT_STATE or a canonical decision only after the owner explicitly decides to change direction, change NEXT ACTION, accept/reject a candidate, or freeze a requirement. Agent suggestions do not become owner decisions automatically.
- **No-writeback cases:** do not commit pure brainstorming, unresolved option comparison, casual ideas, or incomplete analysis as durable state.
- **Boundary check:** before task end, handoff, project pause, or the next real-work phase, check for mature evidence or state deltas that have not been written back; write them first when applicable.
