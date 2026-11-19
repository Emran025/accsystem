# CNT-AMD-SUPERVISOR — ACCMared Supervisor Desktop App

**Parent:** SYS-ACCMARED-SUP | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-AMD-SUPERVISOR |
| **Purpose** | Flutter desktop application that serves as the delivery supervisor's operational interface — viewing shipment queues, assigning couriers, monitoring delivery status, and reviewing proof of delivery. All backend logic resides in CNT-ACC-DELIVERY. |
| **Scope Boundary** | Thin client UI; no business logic. All state and decisions are in ACCSystem. |

CONFIRMED (idea.md §2.1): "ACCMared Supervisor — تطبيق Flutter Desktop — مشرفو التوصيل."
CONFIRMED (idea.md §14, ADR-008): "ACCMared واجهات عميل، بينما منطق وخدمات التوصيل الخلفية ضمن ACCSystem."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| ACT-DELIVERY-SUPERVISOR | Inbound | Primary user |
| CNT-ACC-APIGATEWAY → CNT-ACC-DELIVERY | Outbound | Shipment management, courier assignment, status monitoring |

---

## 3. Technology Stack

CONFIRMED (idea.md §2.1): Flutter Desktop. OS targets: UNKNOWN. OWNER_UNASSIGNED.

---

## 4. Security

CONFIRMED (idea.md §9): Short-lived tokens, secure token storage, session revocation.

---

## 5. C3 Disposition

**EXCEPTION:** Flutter desktop UI; C3 decomposition deferred to Phase 4 implementation planning.


---

## 6. Data Ownership and Consistency

- **Data Owned:** Stateless single-page application; owns no persistent master data. Holds transient in-memory client state and query response cache.
- **Consistency Model:** Strong read-after-write consistency achieved by routing mutations directly to `CNT-ACC-DELIVERY` backend.

---

## 7. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Delivery backend temporary degradation | Graceful UI degradation to cached view with visual indicator that data may be stale |
| WebSocket telemetry disconnect | Automatic reconnection with exponential backoff; fallback to periodic polling |
| Session token expiry | Silent token refresh; prompts re-authentication only if refresh token has expired |

---

## 8. Operations and Reliability

- **Deployment:** Static single-page application assets served via CDN; origin hosted on containerized web server.
- **Observability:** Client-side telemetry tracking dashboard render duration and API call failure rates.

---

## 9. Open Risks and Decisions

- Real-time courier map tracking protocol (WebSocket vs Server-Sent Events) — `OPEN` (`OWNER_UNASSIGNED`). Action: perform bandwidth benchmarking.
