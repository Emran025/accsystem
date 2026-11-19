# CNT-AMD-COURIER — ACCMared Courier Mobile App

**Parent:** SYS-ACCMARED-COU | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-AMD-COURIER |
| **Purpose** | Flutter mobile application used by couriers to receive delivery assignments, update pickup and delivery status, and submit proof of delivery. All backend logic resides in CNT-ACC-DELIVERY. |
| **Scope Boundary** | Thin client UI; no business logic. |

CONFIRMED (idea.md §2.1): "ACCMared Courier — تطبيق هاتف — الموصلون."
CONFIRMED (idea.md §14, ADR-008): Delivery backend in ACCSystem.

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| ACT-COURIER | Inbound | Primary user |
| CNT-ACC-APIGATEWAY → CNT-ACC-DELIVERY | Outbound | Assignment receipt, status updates, proof of delivery submission |

---

## 3. Technology Stack

CONFIRMED (idea.md §2.1): Flutter mobile. iOS/Android — ASSUMPTION (Flutter cross-platform). OWNER_UNASSIGNED.

---

## 4. Security

CONFIRMED (idea.md §9): Short-lived tokens, secure storage, no embedded service secrets in mobile binary.

---

## 5. C3 Disposition

**EXCEPTION:** Flutter mobile UI; C3 decomposition deferred to Phase 4 implementation planning.


---

## 6. Data Ownership and Consistency

- **Data Owned:** Local SQLite storage holding transient offline delivery queue (pickup status, delivery timestamp, recipient signature, GPS breadcrumbs).
- **Consistency Model:** Eventual consistency with `CNT-ACC-DELIVERY`. Local queue syncs via idempotent HTTP PATCH requests when connectivity is established.

---

## 7. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Complete network disconnect | App operates in offline mode; status submissions queued locally in encrypted SQLite store |
| Server rejects submission (4xx/5xx) | Exponential backoff retry with jitter; fatal validation errors alert courier via UI banner |
| App process termination during upload | Unsent queue entries re-scanned and dispatched on subsequent application launch |

---

## 8. Operations and Reliability

- **Deployment:** Distributed via Apple App Store and Google Play; over-the-air hotfix capability via Flutter code push where permitted.
- **Observability:** Crashlytics for mobile crash telemetry; APM tracking API network request latency and error rates.
- **SLI:** Target > 99.5% crash-free mobile sessions.

---

## 9. Open Risks and Decisions

- Local encryption key management for SQLite offline cache — `OPEN` (`OWNER_UNASSIGNED`). Action: select OS keychain integration strategy.
