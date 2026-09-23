# Evidence: Catering Qualification Discovery v0.1

**Status: public-safe durable evidence**
**Scope:** historical catering-inquiry research; not a final business-model decision.

## Dataset integrity

The analyzed corpus contained 375 conversation boundaries and 21,425 messages. A deterministic message-ID collision was found and repaired before analysis. The repaired dataset reconciled to 375/375 conversations and 21,425/21,425 messages, with zero duplicate message IDs. Nine previously missing boundaries passed independent regression checks.

No private conversations, customer identifiers, contact details, raw exports, supplier-private pricing, payment details, credentials, or local storage paths are included in this record.

## Evidence layers

### Qualitative quote reconstruction

Five high-information quote cases were reviewed to distinguish:

- price indication: a price rule, unit price, or minimum spend;
- preliminary quote: a case-specific amount or package;
- formal/order-ready: a near-final service, quantity, payment, or administrative arrangement.

The cases showed that these are not the same state. Budget, exact time, final quantity, complete menu, invoice details, tax ID, and deposit are not universal first-quote requirements. They may be added later or apply only to particular service types.

### Deterministic corpus census

A code-first census processed all 375 conversations and 21,425 messages. Among 374 valid first contacts, observable first-contact fields appeared at these rates:

- service type: 57.1%
- location/area: 33.6%
- date: 16.8%
- headcount/quantity: 12.5%
- explicit budget: 7.49% after separating budget from price questions

The first-contact messages were usually incomplete. Missing context was often added before a vendor price signal, but frequency does not establish that a field is universally required.

An earlier broad price detector found 222 cases with a median first-contact-to-first-price path of 14 messages (p25 8, p75 22). A later stricter price taxonomy found 210 cases. These denominators must not be combined.

### First-contact efficiency

Descriptive comparison did not show a monotonic rule that more complete first contact always produces a shorter path to the first vendor price. Location was the most consistent early signal in this corpus. Date functioned mainly as an availability gate; headcount as pricing context; service type as routing context. Explicit budget was not supported as a universal early required field.

A recent owner-curated qualitative validation cohort of nine current conversations remained consistent with progressive qualification and additionally highlighted logistics, invoice/administrative requirements, equipment/setup, and menu revisions as later-stage information. This cohort is qualitative and is not a population estimate.

## Evidence conclusion

The current evidence supports this public-safe conclusion:

> Catering inquiries commonly begin with incomplete or partly complete needs. The supplier currently completes qualification through chat. Yuanwai should first validate a wedge that normalizes natural-language demand, preserves what is already known, identifies missing or conditional information, asks only the next useful question, and produces a supplier-ready brief.

This does not establish a final business model, reject marketplace or SaaS possibilities, prove that all vendors use the same workflow, or prove that customers will complete this process through Yuanwai.

## Limitations

The evidence is primarily from one catering operation's historical inquiry data. Deterministic signals are observable patterns, not causal explanations. A vendor's response speed, multi-stage conversations, and the distinction between a price signal and a formal quote limit the conclusions.
