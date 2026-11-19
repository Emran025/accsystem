# Critical Acceptance and Recovery Test Plan

1. **Multi-seller saga:** cart with multiple sellers creates one ParentOrder and seller-scoped SellerOrders; reservations run independently; one rejection releases successful holds; no payment authorization occurs; duplicate commands are idempotent.
2. **Concurrent last-unit race:** two checkouts target one unit at ACCore; local conditional update/lock permits at most one reservation; the loser receives definitive rejection; ACCSystem projection is never authoritative.
3. **Unknown reservation:** connector timeout leaves reservation outcome UNKNOWN; checkout does not claim success, authorize payment, or release a possibly-held reservation solely on timeout; query/reconciliation resolves it.
4. **Payment unknown/replay:** provider timeout remains UNKNOWN; duplicate webhook and retry create no duplicate authorization/capture; later definitive provider evidence drives one transition.
5. **Capture failure after confirmation:** order remains visible with payment exception; retry/reconciliation and refund/void paths are idempotent; no silent completion.
6. **Ledger/manual payment:** postings are balanced and immutable; duplicate external references are rejected or quarantined; manual payment requires scoped permission, reason, evidence, and approval.
7. **Connectivity loss:** failed health/connector policy removes institution listings from search/promotion or labels them unavailable; local ACCore ERP functions permitted by license continue; open carts revalidate.
8. **License offline:** signed token verifies locally, key rotation is accepted, revocation propagates when connected, configurable grace expires into restriction without corrupting local ERP data.
9. **Currency/tax snapshot:** order retains transaction currency, exchange source/time, rounding, ordered tax lines and rule version; later admin changes do not alter confirmed order.
10. **Package provenance:** digest mismatch, invalid signature, invalid attestation, or changed build fingerprint blocks availability or raises an auditable alert; a digest alone is not accepted as source provenance.
11. **Tenant/support security:** cross-institution reads fail; support access is purpose/institution scoped, least privilege, time-bound, audited, and cannot grant RBAC or license entitlement.
12. **Recovery:** outbox/inbox replay, DLQ redelivery, saga restart, provider reconciliation, search reindex, and backup/restore preserve idempotency and correlation IDs.

Structural validation cannot certify semantic correctness, security, legal compliance, performance, or production readiness; those require the gates in `policy-and-gates.md`.
