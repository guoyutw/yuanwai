# Evidence: Pre-LINE Service Discovery Friction

**Status: public-safe supporting evidence / product-funnel insight.**

**Date:** 2026-10-03

**Scope:** Preserve an owner-observed customer-experience insight relevant to Yuanwai's future acquisition / conversation-entry layer. This is not a product-direction decision and does not change Issue #74, the current NEXT ACTION, or the no-LINE-until-review boundary.

## Source

Owner supplied a public Threads post describing the experience of searching for an old-building exterior renovation vendor:

- after finding a company on IG / Threads, the next step is often immediately “add LINE”;
- the customer still does not yet understand service scope, past results, or what the provider actually offers;
- being forced into a chat before that understanding exists creates friction and the expectation of repetitive back-and-forth;
- the poster would prefer a single consolidated page containing the basic service information and examples;
- that page does not need to be a full website; even a simple cloud document could serve the purpose.

Owner-provided public source:
https://www.threads.com/share/_maOrXqgZ/

The owner connected this with prior Blossom practice: Blossom used LINE OA for catering inquiries primarily because it was convenient for managing customers, but had not explicitly separated **pre-contact service understanding** from **case-specific conversation**.

## Reusable insight

LINE OA is useful for managing a live inquiry, but it may be a poor **only** first-contact surface for a customer who is still deciding whether the service is relevant.

A useful distinction is:

- **pre-conversation information layer** → helps a customer understand what Yuanwai is, what kinds of catering situations it can help with, representative examples, and how the process works;
- **LINE / conversational layer** → handles the customer's specific case, progressive qualification, questions, changes, and supplier-authority gates.

This suggests that Yuanwai should not assume every reusable explanation belongs inside the chat.

## Candidate implication for Yuanwai

Before asking a customer to start a LINE conversation, Yuanwai may benefit from a lightweight self-serve information surface that makes the common, reusable context easy to scan.

Candidate contents could include:

- what Yuanwai helps with;
- representative catering / event-service forms;
- example situations or public-safe case examples;
- the basic collaboration flow;
- what can be answered immediately versus what requires supplier confirmation;
- safe expectation framing where appropriate, without exposing supplier-private pricing or commitments;
- a clear transition into LINE for case-specific discussion.

The implementation does **not** need to start as a website. A simple public page or document is sufficient for an early test.

## Why this matters to the current product hypothesis

The current qualification work focuses on what happens **after the customer starts talking to Yuanwai**.

This evidence points to a distinct upstream question:

> How much shared context should the customer be able to understand before entering the conversation?

If a pre-conversation layer explains reusable information well, the conversational system may spend less time repeatedly explaining basic service scope and more time handling the parts that are actually specific to the customer's case.

## Evidence boundary

This is one owner-observed external example plus the owner's Blossom operating reflection. It does not establish that LINE-first entry is broadly harmful, nor that Yuanwai must build a website, landing page, catalog, or pricing page.

It should remain a candidate funnel / UX insight until tested with real or synthetic entry flows.

## Possible future validation

After the current simulator/review work is complete, a bounded entry-flow test could compare:

1. direct-to-LINE entry; and
2. a lightweight information page followed by LINE.

Useful observations would include:

- whether customers understand the service before initiating chat;
- whether repetitive “what do you do / how does this work” questions decrease;
- whether the customer reaches case-specific qualification faster;
- whether the extra page creates new drop-off instead of reducing friction.

## Effect on current experiment

No change to `CURRENT_STATE.md`, NEXT ACTION, Issue #74 scope, or LINE implementation boundary.

The insight is preserved for later funnel / entry-layer testing after the current conversation-state simulator reaches its review gate.
