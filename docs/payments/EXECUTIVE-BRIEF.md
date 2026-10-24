# Giving Payments — Executive Brief

**Royal Priesthood Assemblies International**  
**Prepared for:** Trustees, treasurer and finance lead  
**Date:** 22 October 2026  
**Companion to:** `docs/payments/ARCHITECTURE.md` (full technical specification)

---

## The short version

The church needs one giving checkout that accepts **Airtel Money, MTN Mobile Money, Zamtel Kwacha, Visa and Mastercard**, and that finance can reconcile to the bank.

The current setup is not yet that system. It can take a mobile-money payment if the Paystack account is enabled for ZMW, but it sends the donor to a Paystack web page to enter a PIN rather than sending a prompt to the phone. It keeps payment records in memory, so a restart can erase them. It has no ledger, no refunds, no card payments and no daily reconciliation. It also hard-codes the Zambian kwacha as having no decimal places, while the international currency standard says it has two — a mistake that could cause a 100× over- or under-charge.

None of these are reasons to panic. They are reasons to **not go live at scale yet**, and to fix the foundation before adding more channels.

---

## What I recommend

### 1. Use an aggregator first, not three direct MNO integrations

At the church’s likely volume, connecting directly to Airtel, MTN and Zamtel would mean three contracts, three security reviews, three reconciliation formats and three support relationships. The saving per transaction would not repay the operational cost.

Use one licensed aggregator for mobile money, keep a second qualified provider in reserve, and revisit direct integration only if volume makes it clearly worthwhile.

### 2. Treat mobile money and cards as two rails behind one checkout

A mobile-money specialist may be strongest at USSD prompts; a card acquirer may be strongest at Visa/Mastercard 3DS2. The donor should see one checkout. The church should be free to use different providers for each rail without rebuilding the page.

### 3. Never guess whether a payment succeeded

A timeout is not a failure. If the donor enters a PIN and the callback is delayed, the system must say **“we are still confirming”**, not “failed”. It must never resend a debit after a prompt may have appeared. A late success must be honoured and, if necessary, refunded.

### 4. Keep a real ledger, not just a payment status

“Paid” is not the same as “money in the bank”. Every gift, fee, refund, chargeback and settlement should have a balanced accounting entry, with a fund dimension (general, building, missions, etc.). Finance should be able to trace a receipt to the bank statement.

### 5. Protect card data by never touching it

Card details should be entered in the provider’s secure fields. The church should receive a token and the last four digits only. No card number, CVV or PIN should be stored or logged.

---

## What is true today

| Area | Current position | Why it matters |
|---|---|---|
| Mobile money | Paystack redirect to an authorisation page | The donor is not sent a USSD prompt on the handset; the page language must not promise one |
| Card | Not implemented | Visa/Mastercard cannot be accepted |
| Zamtel | Not supported in validation | Only MTN and Airtel are accepted today |
| Persistence | In-memory | A restart or a second server can lose payment state |
| Idempotency | Optional, in-memory, no request fingerprint | A double tap can create two charges |
| Webhooks | Signature checked, but no deduplication or state guard | A late failure can overwrite a success |
| Refunds and disputes | Manual/untracked | No audit trail or ledger effect |
| Reconciliation | Manual | No daily proof that provider settlements match the bank |
| Ledger | None | No fund accounting or fee tracking |
| ZMW precision | Code assumes exponent 0 | ISO 4217 says 2; a 100× error is possible |

The full specification documents each gap and the target control.

---

## What it will cost

The honest answer is that **provider pricing is not yet known**. Fees vary by volume, negotiation, card versus mobile money, settlement currency and reserves.

The right comparison is total cost of ownership:

> Provider fees + FX spread + settlement float + reconciliation labour + integration and maintenance + the cost of a duplicate debit or missed receipt.

A direct integration that saves one percentage point but consumes two engineering months a year and one finance day a week is usually more expensive for a church than an aggregator.

**What we need to obtain:** written fee schedules from the shortlisted providers, settlement timing, reserve requirements, refund and chargeback fees, FX spread, and any minimum volume.

---

## Decisions requested from the trustees

| # | Decision | Why it is needed | Suggested owner |
|---|---|---|---|
| 1 | Confirm the legal entity that will hold merchant accounts and the settlement bank account | Providers contract with a legal entity; the money must land in the right account | Trustees + counsel |
| 2 | Approve the provider shortlist and the sandbox evaluation | No provider should be signed on marketing claims alone | Finance + engineering |
| 3 | Approve the refund policy and approval threshold | Donors and finance need a clear, consistent rule; above a threshold, two people should approve | Trustees |
| 4 | Approve the data retention and privacy position | Donor names, phone numbers and emails are personal data; retention must be deliberate | Privacy lead + counsel |
| 5 | Approve a budget for provider setup, security review and reconciliation tooling | The cheap option is not the same as the safe option | Trustees |

---

## Recommended 90-day path

### Days 0–30 — Prove the ground
- Confirm the legal entity, bank account and refund policy.
- Obtain written provider proposals and sandbox access.
- Test true USSD push on Airtel, MTN and Zamtel; test Visa and Mastercard 3DS2.
- Fix the ZMW precision assumption and replace in-memory state with a database.
- Write the chart of accounts and the reconciliation procedure.

**Gate:** no live scale-up until a provider proves all three operators and both card schemes in sandbox.

### Days 31–60 — Build the safe core
- Implement the canonical payment states, mandatory idempotency and signed webhook processing.
- Add the double-entry ledger and receipt.
- Add daily settlement ingestion and a reconciliation exception queue.
- Run failure drills: duplicate request, timeout after PIN, duplicate webhook, late success, refund.

**Gate:** duplicate requests produce one charge; a timeout never shows “failed”; every successful gift has a ledger entry.

### Days 61–90 — Limited live pilot
- Enable one mobile-money provider and one card acquirer for a small group of named volunteers.
- Start with small amounts and a manual daily reconciliation review.
- Add Zamtel and the secondary provider only after the first rail is stable.
- Review at 7, 30 and 90 days.

**Gate:** 50 consecutive successful collections, 20 controlled failures handled correctly, and a full month of reconciliation with no unexplained breaks.

---

## What we will not do

- We will not promise a phone prompt until a provider demonstrates one.
- We will not add a second payment rail on top of in-memory state.
- We will not store card numbers, CVVs or PINs.
- We will not mark a payment “failed” just because a callback was late.
- We will not go live at scale before reconciliation and refund procedures are tested.

---

## Risks of waiting

The current page can take money, but it cannot yet prove where every kwacha went. The most serious risks are a duplicate debit after a double tap or timeout, a payment lost on restart, and a donor being told a payment failed when it succeeded. These are trust risks, not just technical defects.

The cost of fixing the foundation is modest compared with the cost of a public payment failure or a donor who cannot get a receipt.

---

## Where to read more

- **Full architecture:** `docs/payments/ARCHITECTURE.md`
- **Provider evaluation checklist:** Appendix C of the architecture
- **Acceptance tests:** Appendix F of the architecture
- **Current-to-target migration map:** §9.9 of the architecture
- **Open decisions:** §10 of the architecture

The next step is a 60-minute working session with the treasurer and finance lead to confirm the five decisions above, followed by provider sandbox testing.
