# Evidence Review: Two-Sided Catering Frictions

**Status: public-safe supporting evidence.**

**Scope:** A bounded review of Yuanwai-relevant catering friction using an owner-provided NotebookLM synthesis over existing Blossom historical materials. This is not a new product-direction decision and does not change the current concierge / Wizard-of-Oz qualification experiment.

## Source coverage

The reviewed NotebookLM materials included:

- a 50-case deep summary derived from historical Blossom LINE inquiries;
- derived Blossom catering rules / SOP notes;
- owner-side operating and pain-point notes;
- several smaller raw or summarized conversation excerpts.

This is useful evidence, but it is not the full historical 375-conversation corpus. It is also strongly biased toward one supplier (Blossom), one regional operating context, and cases that were important enough to summarize. Lost leads, non-Blossom vendor behavior, and standardized post-event customer feedback are underrepresented.

## Reusable two-sided friction

The strongest reusable pattern is a tension between **customer speed** and **vendor decision readiness**:

- customers often want a quick answer from a short, natural-language inquiry;
- vendors need enough context to judge serviceability, availability, pricing context, and operational feasibility before spending time on a proposal.

This is consistent with the existing progressive-qualification candidate: preserve what is already known, ask only the next useful question, and produce a supplier-ready brief rather than forcing a complete RFQ at first contact.

Other recurring frictions in the reviewed material include:

1. **Change flexibility vs. operational lock-in** — customers may change headcount, timing, menu, or requirements after initial discussion, while suppliers need stable inputs for purchasing, preparation, labor, and cost control.
2. **Budget / expectation mismatch** — customers may have a fixed budget while expecting variety, abundance, or service levels that require supplier-side tradeoffs.
3. **Venue / logistics uncertainty** — access, equipment, setup, transport, timing, and service-site constraints may surface only after the initial inquiry.
4. **Administrative requirements** — invoices, quotation formats, procurement rules, and other organization-specific requirements can create later-stage friction.

These observations support treating qualification as progressive and conditional rather than as a universal first-contact form.

## Vendor-side evidence boundary

Some observed pain is clearly supplier-specific rather than market-wide, including Blossom's own document-production workflow, equipment-preparation practices, and internal multi-person communication friction.

Those should not be promoted into general Yuanwai product requirements without evidence from additional vendors.

Likewise, this review does not establish that Yuanwai should build automated quoting, dynamic menus, vendor SaaS, matching, or workflow automation. Those remain outside the current experiment unless later evidence promotes them.

## Evidence gaps

Current evidence is insufficient to claim market-wide prevalence because it lacks:

- full lost-lead / non-conversion coverage;
- comparable evidence from multiple independent catering vendors;
- standardized post-event customer satisfaction or willingness-to-pay evidence.

## Effect on current experiment

No change to `CURRENT_STATE.md`, `NEXT ACTION`, or `CLEAR CONDITION`.

The existing five-case Blossom single-supplier sandbox remains the correct next step. The live cases should continue to test whether Yuanwai can turn a natural-language inquiry into a supplier-ready brief with less redundant questioning, and should record where customer-side or vendor-side friction still appears.

