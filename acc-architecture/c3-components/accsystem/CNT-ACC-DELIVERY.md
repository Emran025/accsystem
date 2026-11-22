# CNT-ACC-DELIVERY — Delivery Management

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-DELIVERY |
| **Purpose** | Manages shipment lifecycle — creation, courier assignment, dispatch, tracking, and proof of delivery. Serves as the backend for ACCMared Supervisor and Courier apps. |
| **Scope Boundary** | Owns shipment records and delivery state. Does NOT own order state (CNT-ACC-ORDERS). |

CONFIRMED (idea.md §3.1): "Delivery Management — إنشاء الشحنات، توزيعها، تعيين الموصل، تتبع التنفيذ وإثبات التسليم."
CONFIRMED (idea.md §14, ADR-008): "ACCMared واجهات عميل، بينما منطق وخدمات التوصيل الخلفية ضمن ACCSystem."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-ORDERS | Inbound | Receives shipment creation trigger from OrderConfirmed |
| CNT-AMD-SUPERVISOR | Inbound | Supervisor views and manages shipment assignments |
| CNT-AMD-COURIER | Inbound | Courier receives assignments and submits status updates |
| CNT-ACC-EVENTBUS | Bidirectional | Publishes ShipmentCreated/Assigned/Delivered events |
| CNT-ACC-NOTIFICATIONS | Outbound | Delivery status events trigger buyer/seller notifications |
| CNT-ACC-AUDIT | Outbound | Logs delivery operations |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Delivery provider | UNKNOWN (idea.md §12) | "هل ACCMared يدير أسطول المنصة فقط أم يربط شركات خارجية؟" — OWNER_UNASSIGNED |

---

## 4. Data Owned

- Shipment: `{shipment_id, order_id, seller_order_id, courier_id, status, proof_of_delivery_ref, created_at}`
- Delivery task assignments
- Proof of delivery records (photo, signature reference, geolocation — UNKNOWN: exact fields)

---

## 5. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Shipment creation fails after OrderConfirmed | CONFIRMED (idea.md §7.5): "يبقى الطلب مؤكداً وتكون حالة التنفيذ Pending Delivery مع إعادة المحاولة" |
| Courier app connectivity lost | If an approved offline mode queues a status command, it remains pending client intent; CNT-ACC-DELIVERY validates it on reconnect and alone commits or rejects the authoritative transition (offline policy UNKNOWN) |

---

## 6. Security

- Courier access scoped to assigned shipments only — ASSUMPTION
- Supervisor access scoped to their fleet — ASSUMPTION
- Proof of delivery records must be tamper-evident — ASSUMPTION

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "الطلبات غير المسندة، المهام المتأخرة، التسليمات المتعثرة، إثبات التسليم" |
| Risk | External logistics integration complexity (open decision §12) |

---

## 8. C3 Disposition

**EXCEPTION:** C3 deferred pending delivery provider scope decision (open decision idea.md §12) and ACCMared integration design. Revisit trigger: when delivery provider integration model is defined and Phase 4 begins.
