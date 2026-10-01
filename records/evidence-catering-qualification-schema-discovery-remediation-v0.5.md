# Issue #70 B2 remediation delta v0.5

Status: remediation candidate for same-reviewer re-review. B1 and B3 remain closed and are not changed here.

Corpus and execution anchor

Same private corpus was re-read:
- 375 CSV files
- 21,425 message rows
- SHA-256 C0A8A8C604D29EC4C1C05AC11722629A8BD8EE4B0498A09D746BEF9EA61DB399

Reproducible entrypoint: scripts/qualification_schema_remediation.py

Revised timing anchor

The first event is now the first Account message that satisfies all conditions:

1. contains an explicit numeric amount with 元/萬/万 (Arabic or supported Chinese numeral form);
2. contains a price/proposal context in the same message: 報價、估價、方案、餐點、菜單、人均、低消、費用、價格、價錢、外燴、buffet、預算、總額、總價、每人、收費、起送、開瓶費 or 場地費;
3. is not question-like;
4. is not future/offer-only wording (之後、再提供、再給、會再、將會、預計、想要、希望、可以提供);
5. if it contains administrative money terms (訂金、押金、匯款、轉帳、收款、帳戶、付款、收據、發票、匯入、多匯、收訂), it is retained only when the same message also has a strong price/proposal context (報價、估價、方案、人均、低消、費用、價格、價錢、總額、總價、每人、收費、起送、開瓶費 or 場地費). Generic 菜單/餐點 text alone does not rescue an administrative amount. Admin/payment-only amounts are excluded.

This makes the code and the timing-anchor definition agree. Bare 報價/報價單, question-only quote language, future-only offers, deposit/payment amounts, transfer receipts, and account/receipt-only amounts cannot become the anchor.

Revised event set

- Cases with a retained first meaningful price/proposal event: 45
- Median event position: 21

User-field presence relative to the retained event (a case may contain several fields):

- service type: 44 pre / 0 post
- quantity: 42 pre / 3 post
- time: 33 pre / 4 post
- location: 23 pre / 5 post
- date: 18 pre / 5 post
- budget: 29 pre / 5 post
- menu: 23 pre / 9 post
- equipment/setup: 5 pre / 6 post
- access/logistics: 1 pre / 3 post
- dietary: 1 pre / 3 post
- invoice/admin: 8 pre / 15 post

These are timing associations under this explicit detector, not universal requirements or causal effects.

Bounded manual validation

The following raw-message cases were read privately and preserved only as coded findings:

Positive signals retained:
- case 14, message 30: quoted 20,000 amount for a stated meal order; retained as proposal/meal amount.
- case 22, message 24: per-person fee and delivery/utensil context; retained as service price indication.
- case 67, message 21: per-person and total amount with delivery/setup context; retained as price indication.
- case 275, message 6: buffet per-person price and minimum spend; retained as service price indication.
- case 337, message 141: estimate/quotation amount with supplier and meat-item context; retained as proposal amount.

Negative admin/payment-only examples excluded:
- case 4, message 160: bank transfer receipt and account details; excluded as payment confirmation.
- case 40, message 20: request to transfer deposit to an account; excluded as deposit/payment administration.
- case 134, message 109: request to transfer deposit; excluded as deposit/payment administration.
- case 270, message 106: bank transfer receipt; excluded as payment confirmation.
- case 304, message 46: request for two-part deposit; excluded as deposit/payment administration.

The positive examples preserve actual supplier price/proposal signals; the negative examples demonstrate that later administrative amounts do not establish the first price/proposal anchor.

Historical provenance preserved

The v0.1 statistics remain separate and unchanged:
- 222 cases / median 14 messages (p25 8, p75 22): earlier broad detector.
- 210 cases: later strict taxonomy; no median-14 attribution.

Neither historical denominator is combined with the revised 45-case event set.

Boundary

This delta fixes only B2. No AI implementation, model selection, marketplace, automated quoting, or canonical schema freeze was performed.
