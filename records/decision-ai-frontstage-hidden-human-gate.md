# Decision: AI-Frontstage Qualification with Hidden Human Gate

**Status: current owner-approved execution setup.**

## Decision

Yuanwai should be AI-facing from the first real customer interaction rather than using 哲瑜 as the visible concierge.

哲瑜 remains a **hidden operator**. The normal path is for the AI to receive the customer's natural-language inquiry, preserve known information, ask progressive follow-up questions, and produce a supplier-ready brief.

Human involvement is a hidden business-decision gate, not the default chat interface.

## Human gate boundary

The AI may autonomously:

- acknowledge and organize the inquiry;
- extract known fields;
- identify missing or conditional information;
- ask the next useful qualification question;
- explain the qualification process;
- produce and update the supplier-ready brief.

The AI must not independently create or change supplier business commitments such as:

- final availability;
- final price;
- menu or service exceptions;
- fulfillment commitments;
- discounts, refunds, payment terms, or other binding commercial decisions.

When one of these decisions is needed, Yuanwai should obtain a hidden human / Blossom decision and then allow the AI to deliver the confirmed answer to the customer.

## Minimum implementation

The immediate build should be only what is necessary to run real cases:

- Yuanwai LINE Official Account;
- LINE Messaging API / webhook;
- minimal conversation state;
- AI qualification logic;
- supplier-ready brief generation;
- a minimal hidden-human decision path;
- public-safe experiment logging.

This decision does not authorize building a marketplace, multi-vendor matching system, vendor SaaS, full admin dashboard, or autonomous quoting / negotiation system.

## Experiment effect

The existing five-case Blossom single-supplier experiment remains the acceptance boundary.

The execution mode changes from visible human concierge handling to **AI-first customer interaction with hidden human gating**. The experiment should therefore also record where hidden intervention was required and whether the AI attempted any unsupported supplier commitment.
