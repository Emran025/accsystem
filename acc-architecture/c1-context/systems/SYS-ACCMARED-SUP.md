# SYS-ACCMARED-SUP — ACCMared Supervisor Desktop App

**Label convention:** `CONFIRMED (idea.md §X)` | `ASSUMPTION` | `PROPOSAL` | `UNKNOWN`

---

## 1. Identity

| Field | Value |
|---|---|
| **System ID** | SYS-ACCMARED-SUP |
| **Parent** | SYS-ACCECOSYSTEM |
| **Role in Ecosystem** | Flutter desktop application used by delivery supervisors to manage delivery teams, assign shipments, monitor task progress, and track fulfilment execution. |
| **Scope Boundary** | ACCMared Supervisor is a thin client UI only. All delivery backend logic resides in ACCSystem (CNT-ACC-DELIVERY). The supervisor app does not own any delivery state or business logic. |

CONFIRMED (idea.md §2.1): "ACCMared Supervisor — تطبيق Flutter Desktop — مشرفو التوصيل — إدارة فرق التوصيل والمهام ومتابعة التنفيذ."
CONFIRMED (idea.md §14, ADR-008): "ACCMared واجهات عميل، بينما منطق وخدمات التوصيل الخلفية ضمن ACCSystem."

---

## 2. Actors and Users

| Actor ID | Name | Interaction |
|---|---|---|
| ACT-DELIVERY-SUPERVISOR | Delivery Supervisor | Views shipment queue, assigns couriers, monitors delivery status, reviews proof of delivery |

---

## 3. External Systems Consumed

None directly. All data flows through SYS-ACCSYSTEM via API Gateway.

---

## 4. Connections to Other Platform Systems

| System | Direction | Protocol | Purpose |
|---|---|---|---|
| SYS-ACCSYSTEM (via CNT-ACC-APIGATEWAY → CNT-ACC-DELIVERY) | Outbound | HTTPS/TLS | Shipment data, courier assignment, delivery status, proof of delivery review |

---

## 5. Key Responsibilities

- Display pending, in-progress, and completed shipments
- Assign shipments to available couriers
- Monitor courier locations and task status (if real-time tracking is implemented — UNKNOWN)
- Review and approve proof of delivery records

**Does NOT own:** Delivery domain logic, shipment records, assignment rules (all in CNT-ACC-DELIVERY)

---

## 6. Technology Stack / Hosting

| Aspect | Status | Note |
|---|---|---|
| Platform | CONFIRMED (idea.md §2.1) | Flutter Desktop application |
| OS targets | UNKNOWN | Windows/macOS/Linux — not specified. OWNER_UNASSIGNED. |
| Distribution | UNKNOWN | Installer packaging/distribution mechanism not specified. |
| Authentication | CONFIRMED (idea.md §9) | Short-lived tokens, secure storage, session revocation per platform security policy |

---

## 7. Open Decisions

| Decision | Status |
|---|---|
| Delivery provider scope | UNKNOWN (idea.md §12): "هل ACCMared يدير أسطول المنصة فقط أم يربط شركات خارجية أيضاً؟" — OWNER_UNASSIGNED |
| Real-time courier tracking | UNKNOWN — not specified in idea.md. Revisit: Phase 4 planning. |

---

## 8. C2 Disposition

| Container ID | Name | C3? |
|---|---|---|
| CNT-AMD-SUPERVISOR | ACCMared Supervisor Desktop App | No — Flutter UI, C3 deferred to Phase 4 implementation planning |

See: `c2-containers/accmared/CNT-AMD-SUPERVISOR.md`
