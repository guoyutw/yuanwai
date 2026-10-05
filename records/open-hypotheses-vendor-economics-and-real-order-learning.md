# Open Hypotheses: Vendor Economics and Real-Order Learning

**Status: OPEN HYPOTHESES / CANDIDATE LEARNINGS — NOT YET VALIDATED.**

These hypotheses are recorded for future evidence collection only. They do not change `CURRENT_STATE.md`, the current NEXT ACTION, or the concierge / Wizard-of-Oz qualification MVP requirement.

## 1. Worthwhile matching / vendor economics

Yuanwai may eventually need to ask not only whether a vendor can accept a request, but whether the request is worthwhile for that vendor to accept.

Potential variables include:

- order value or minimum worthwhile order;
- headcount or quantity;
- current capacity;
- labor requirement;
- delivery or transport burden;
- equipment requirement;
- service-type fit;
- operational complexity.

The current basis is owner experience in restaurant and catering operations. It is not evidence that this economics model generalizes to all vendors. No matching algorithm or vendor-ranking rule is being designed in this record.

## 2. Order-size / scale economics

Catering orders may have scale effects. Different order sizes may create non-linear differences in gross margin, labor efficiency, delivery burden, setup cost, and opportunity cost.

Headcount and order value may therefore become both customer-qualification context and vendor-side fit/economics variables. No profitability threshold or amount is established, and no specific amount should be treated as a universal rule.

## 3. Real-order learning loop

Yuanwai already has a **single-case feedback loop**:

`customer message / observation → case state update → reasoning / next question → new observation → state correction / invalidation / reconfirmation → human gate / supplier-ready progression`

This means Yuanwai is already a **feedback-driven agent flow within a case**. That is different from proving cross-case self-improvement.

The broader real-order learning hypothesis is:

`real inquiry / order → qualification behavior → vendor follow-up / human override / outcome evidence → identify systematic weakness → accumulate multi-case evidence → validated change to qualification / routing / policy → future cases improve`

**OPEN HYPOTHESIS / FUTURE EVIDENCE LOOP / NOT YET VALIDATED.** This must not be treated as an MVP requirement, a `CURRENT_STATE` decision, or an automatic learning mechanism. Vendor matching, vendor economics, and transaction outcome remain future evidence layers and are not current MVP requirements.

The purpose of recording this loop is to avoid losing vendor-side learning after live qualification cases are completed. It does not expand the current scope.

## Evidence needed later

Future live evidence should be public-safe and structured, without customer identity, private messages, individual transaction amounts, or private supplier economics. It should test whether vendor-side workload, service fit, scale, and outcome information can be collected consistently enough to validate or reject these hypotheses.
