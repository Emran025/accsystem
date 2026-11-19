# CNT-ACR-INVENTORY — Inventory & Warehousing (ACCore)

**Parent:** SYS-ACCORE | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACR-INVENTORY |
| **Purpose** | Tracks physical stock levels, warehouse locations, inventory movements, reservations, and stock adjustments for the institution. The authoritative source for inventory data. |
| **Scope Boundary** | Institution-internal; source of truth for real inventory. ACCSystem holds only availability snapshots — not live inventory. |

CONFIRMED (idea.md §4.1): "Inventory & Warehousing — المخزون الفعلي، المستودعات، الحركات، الحجز المحلي، الجرد."
CONFIRMED (idea.md §5): "المخزون الفعلي — ACCore لدى البائع" is the source of truth.

---

## 2. Key Relationships

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACR-CONNECTOR | Bidirectional | Receives reservation requests; commits or rejects reservations; publishes stock change events |
| CNT-ACR-SALES | Inbound | Sales order confirmation triggers final inventory deduction |

---

## 3. Technology Stack

UNKNOWN — institution-owned ERP module. OWNER_UNASSIGNED.

---

## 4. Data Owned

Stock records, warehouse locations, movement history, reservation ledger. Source of truth for inventory — CONFIRMED (idea.md §5).

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| Inventory unavailable during reservation | Outcome is `UNKNOWN` unless ACCore has definitive rejection evidence; query/reconcile before retry or release |
| Concurrent last-unit request | Local conditional update/row lock allows at most one accepted reservation |

---

## 6. C3 Disposition

**EXCEPTION:** Institution-internal ERP module. C3 deferred for same reason as CNT-ACR-PRODUCTMASTER.
