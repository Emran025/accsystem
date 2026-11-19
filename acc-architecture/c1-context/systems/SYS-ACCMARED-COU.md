# SYS-ACCMARED-COU — ACCMared Courier Mobile App

**Label convention:** `CONFIRMED (idea.md §X)` | `ASSUMPTION` | `PROPOSAL` | `UNKNOWN`

---

## 1. Identity

| Field | Value |
|---|---|
| **System ID** | SYS-ACCMARED-COU |
| **Parent** | SYS-ACCECOSYSTEM |
| **Role in Ecosystem** | Flutter mobile application used by couriers to receive delivery assignments, update pickup and delivery status, and submit proof of delivery. |
| **Scope Boundary** | Thin client UI only. All delivery backend logic resides in ACCSystem (CNT-ACC-DELIVERY). The courier app does not own any delivery state. |

CONFIRMED (idea.md §2.1): "ACCMared Courier — تطبيق هاتف — الموصلون — استلام المهام وتحديث حالات الاستلام والتسليم وإثباتها."
CONFIRMED (idea.md §14, ADR-008): "ACCMared واجهات عميل، بينما منطق وخدمات التوصيل الخلفية ضمن ACCSystem."

---

## 2. Actors and Users

| Actor ID | Name | Interaction |
|---|---|---|
| ACT-COURIER | Courier / Delivery Agent | Receives task assignments, updates pickup/delivery status, submits proof of delivery (photo, signature, etc.) |

---

## 3. External Systems Consumed

None directly. All data flows through SYS-ACCSYSTEM via API Gateway.

---

## 4. Connections to Other Platform Systems

| System | Direction | Protocol | Purpose |
|---|---|---|---|
| SYS-ACCSYSTEM (via CNT-ACC-APIGATEWAY → CNT-ACC-DELIVERY) | Outbound | HTTPS/TLS | Assignment receipt, status updates (picked up, delivered), proof of delivery submission |

---

## 5. Key Responsibilities

- Display current assignment queue for the courier
- Update shipment lifecycle status (en route, picked up, delivered, failed)
- Submit proof of delivery (photo, signature, geolocation — UNKNOWN: exact modalities)
- Receive new assignment notifications

**Does NOT own:** Delivery records, assignment logic, or shipment routing (all in CNT-ACC-DELIVERY)

---

## 6. Technology Stack / Hosting

| Aspect | Status | Note |
|---|---|---|
| Platform | CONFIRMED (idea.md §2.1) | Flutter mobile application |
| OS targets | ASSUMPTION | iOS and Android — Flutter mobile implies cross-platform. Not explicitly stated. |
| Distribution | UNKNOWN | App store distribution not specified. OWNER_UNASSIGNED. |
| Authentication | CONFIRMED (idea.md §9) | Short-lived tokens, secure storage, no embedded service secrets |
| Offline operation | UNKNOWN | Whether the app can queue status updates during connectivity loss is not specified. Revisit: Phase 4 planning. |

---

## 7. Open Decisions

| Decision | Status |
|---|---|
| Delivery provider scope | UNKNOWN (idea.md §12): Platform fleet only vs. third-party logistics integration — OWNER_UNASSIGNED |
| Proof of delivery modalities | UNKNOWN — photo, signature, geolocation requirements not specified |

---

## 8. C2 Disposition

| Container ID | Name | C3? |
|---|---|---|
| CNT-AMD-COURIER | ACCMared Courier Mobile App | No — Flutter mobile UI, C3 deferred to Phase 4 implementation planning |

See: `c2-containers/accmared/CNT-AMD-COURIER.md`
