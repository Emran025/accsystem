# CNT-ACR-SALES — Sales & Procurement (ACCore)

**Parent:** SYS-ACCORE | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACR-SALES |
| **Purpose** | Manages local sales orders, purchase orders, supplier records, and B2B procurement workflows within the institution. Receives confirmed order notifications from ACCSystem via CNT-ACR-CONNECTOR. |
| **Scope Boundary** | Institution-internal; local sales/procurement record keeping. Does NOT own the marketplace order (CNT-ACC-ORDERS). |

CONFIRMED (idea.md §4.1): "Sales & Procurement — عمليات البيع والشراء المحلية، الموردون، العملاء، أوامر الشراء والبيع."

---

## 2. Key Relationships

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACR-CONNECTOR | Inbound | Receives OrderConfirmed events, creates local sales order record |
| CNT-ACR-INVENTORY | Outbound | Triggers final inventory deduction on order commitment |
| CNT-ACR-FINANCE | Outbound | Records financial entries at commitment point |

---

## 3. Technology Stack

UNKNOWN — institution-owned ERP module. OWNER_UNASSIGNED.

---

## 4. Data Owned

Local sales orders, purchase orders, supplier master, procurement records.

CONFIRMED (idea.md §5): "عملية البيع المحلية — ACCore البائع" owns the sales record.
CONFIRMED (idea.md §7.3): Financial commitment point is an open decision (§12) — OWNER_UNASSIGNED.

---

## 5. C3 Disposition

**EXCEPTION:** Institution-internal ERP module. C3 deferred.


---

## 6. Security and Trust

- **Access Control:** Role-based access ensures sales personnel only access orders within their assigned institutional department.
- **Data Privacy:** Customer phone numbers and addresses masked in non-administrative view modes.

---

## 7. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Duplicate order notification from ACCSystem | Handled idempotently by checking existing `order_id`; duplicate acknowledged without re-processing |
| Sales invoice generation failure | Order remains in `PROCESSING` state; background retry job regenerates invoice |
| Local database disk full | Inbound connector rejects new orders with HTTP 503; critical disk space alert escalated |

---

## 8. Operations and Reliability

- **Monitoring:** Order processing throughput and state transition durations tracked via Grafana dashboards.
- **Indexing:** Indexes optimized for order date, customer ID, and fulfillment status queries.

---

## 9. Open Risks and Decisions

- Institutional historical order data archiving and purging policy — `OPEN` (`OWNER_UNASSIGNED`).
