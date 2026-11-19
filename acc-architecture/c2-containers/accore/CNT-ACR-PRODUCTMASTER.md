# CNT-ACR-PRODUCTMASTER — Product Master (ACCore)

**Parent:** SYS-ACCORE | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACR-PRODUCTMASTER |
| **Purpose** | Source of truth for the institution's product catalog — product definitions, attributes, variants, pricing, categories, and media. The institution's authoritative product record. |
| **Scope Boundary** | Institution-internal; owns product master data only. Published subset flows to ACCSystem via CNT-ACR-CONNECTOR. |

CONFIRMED (idea.md §4.1): "Product Master — مصدر تعريف المنتج الأساسي، السمات، الوحدات، الصور والمعلومات الداخلية."

---

## 2. Key Relationships

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACR-CONNECTOR | Outbound | Sends approved product publication events to platform |
| CNT-ACR-INVENTORY | Bidirectional | Links product records to inventory stock levels |

---

## 3. Technology Stack

UNKNOWN — institution-owned ERP module. Technology is institution-specific. OWNER_UNASSIGNED.

---

## 4. Data Owned

Products, variants, pricing, categories, media references, internal product attributes. Source of truth — ADR-004.

---

## 5. Security

Strictly institution-internal; no direct access from ACCSystem — CONFIRMED (idea.md §1.2, §4.2).

---

## 6. C3 Disposition

**EXCEPTION:** ERP module; institution-owned. Platform architecture defines the integration boundary (CNT-ACR-CONNECTOR), not ACCore internals. C3 deferred indefinitely for this module.


---

## 6. Operations and Reliability

- **Monitoring:** Tracks product catalog mutation rates, search query latency, and database replication lag.
- **Backup & Recovery:** Daily full database backups with write-ahead log (WAL) archiving for point-in-time recovery.

---

## 7. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Concurrent product updates by multiple managers | Optimistic locking (`version` field) rejects stale edits; user prompted to reload |
| Large batch import failure | Executed in transactional chunks; partial batch failures report detailed line-by-line errors |
| Primary database failover | Application connection pool reconnects to promoted replica within 15 seconds |

---

## 8. Open Risks and Decisions

- High-resolution product image and asset storage backend (local SAN vs cloud object storage S3) — `OPEN` (`OWNER_UNASSIGNED`).
