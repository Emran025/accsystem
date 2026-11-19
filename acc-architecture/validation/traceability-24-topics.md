# ACC Architecture Remediation Traceability — 24 Topics

| # | Owner input / evidence | Resolution and status | Primary impact / validation gate |
|---:|---|---|---|
| 1 | ACCore institution-controlled; platform licensing/integrity | ACCEPTED-OWNER: packaging configurable; signed provenance plus digest and fingerprint notification | deployment, release tests, engineering report |
| 2 | connectivity unspecified | ARCHITECTURAL DEFAULT: outbound connector; inbound optional | connector interruption/unknown reservation tests |
| 3 | multi-seller/category MVP confirmed | ACCEPTED-OWNER: ParentOrder/SellerOrders, all reservations before auth | saga, compensation, concurrency tests |
| 4 | seller/agreement determines capture | ACCEPTED-OWNER: controlled auth-capture/immediate modes | expiry, unknown, capture-failure tests |
| 5 | direct seller credit/code/manual payment described | ACCEPTED-OWNER + ARCHITECTURAL DEFAULT: adapter plus ledger and reconciliation | provider capability/finance gate |
| 6 | multi-currency/tax lines confirmed | ACCEPTED-OWNER: versioned snapshots and rules | immutability/rounding tests; tax gate |
| 7 | returns/disputes deferred | DEFERRED: extensible states, no invented policy | product/legal gate |
| 8 | internal fleet first | ACCEPTED-OWNER: provider interface, internal priority | assignment/tracking/POD tests |
| 9 | accounting trigger unspecified | ARCHITECTURAL DEFAULT: confirmed notification; posting institution-configured | finance owner/contract gate |
| 10 | no marketplace sale when ACCore disconnected | ACCEPTED-OWNER: hide/unavailable; local ERP continues | health/visibility tests |
| 11 | multiple plans | ACCEPTED-OWNER: configurable plan/entitlement dimensions | license configuration gate |
| 12 | signed token/grace/frequency | ACCEPTED-OWNER + safe configurable policy | key rotation/offline restriction tests |
| 13 | ACCommerce free initially | ACCEPTED-OWNER: no initial payment; future entitlements extensible | product monetization gate |
| 14 | institution admin console scope | ACCEPTED-OWNER: scoped modules/data sources and complaint separation | tenant/security/reporting tests |
| 15 | tailored support | ACCEPTED-OWNER: tiered but least-privilege, purpose-scoped | consent/JIT/audit tests |
| 16 | incremental Clean Architecture roadmap | ACCEPTED-OWNER: foundations → publication → reservation → payment → delivery | phase acceptance gates |
| 17 | ADR-012 or scope grouping accepted | ARCHITECTURAL BASELINE: 17 contexts / 6 co-hosted units | boundary/independent deployability tests |
| 18 | institution hosts ACCore; platform hosts e-commerce data | ACCEPTED-OWNER: API/event boundary | ownership and tenant tests |
| 19 | ACCSystem PG/MySQL temporary; ACCore MySQL | ACCEPTED-OWNER; broker/search recommended only after review | migration/replay/search recovery gate |
| 20 | multiple technical methods possible | ARCHITECTURAL DEFAULT: auth adapter, controlled enabled set | rotation/revocation/security gate |
| 21 | SLA/RTO/RPO deferred | CONFIGURABLE: named metrics/owners, no fabricated values | capacity/DR gate |
| 22 | compliance/residency unanswered | EXTERNAL-GATE: jurisdiction-neutral design | legal/compliance/PCI gate |
| 23 | Arabic/English launch direction | ACCEPTED-OWNER: i18n, multilingual fields, provenance-preserving translation | locale/content tests |
| 24 | prevent oversell | ARCHITECTURAL DEFAULT: atomic ACCore reservation, TTL, idempotency, last-unit handling | race/replay/unknown tests |

All topics are traceable to the source prompt and the changed artifacts listed in `validation/change-report.md`. No unresolved item is left as an avoidable design gap; deferred policy values are named configuration and launch gates.
