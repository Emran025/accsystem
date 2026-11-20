# CNT-ACR-FINANCE — Finance / Accounting (ACCore)

**Parent:** SYS-ACCORE | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACR-FINANCE |
| **Purpose** | Records financial transactions, journal entries, invoices, receivables/payables, and performs financial reconciliation within the institution, according to institution-specific accounting rules. |
| **Scope Boundary** | Institution-internal; owns all financial accounting records. ACCSystem does NOT replicate full financial records. |

CONFIRMED (idea.md §4.1): "Finance / Accounting — القيود والفواتير والذمم والمطابقة المالية وفق إعدادات المؤسسة."
CONFIRMED (idea.md §5): "القيود المالية الداخلية — ACCore لكل مؤسسة — لا تُنسخ قيود ERP كاملة."

---

## 2. Key Relationships

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACR-SALES | Inbound | Sales events trigger financial entries |
| CNT-ACR-CONNECTOR | Inbound | Receives settlement reference data from ACCSystem (when available) |

---

## 3. Technology Stack

UNKNOWN — institution-owned ERP module. OWNER_UNASSIGNED.

---

## 4. Data Owned

Journal entries, invoices, payable/receivable ledgers, financial reports. Institution-specific accounting configuration.

---

## 5. Open Decisions

| Decision | Status |
|---|---|
| Financial record commitment point | UNKNOWN (idea.md §12): "يجب ربط ذلك بنقطة العمل المحاسبية المحددة لدى المؤسسة، مثل تأكيد الطلب أو الشحن أو التسليم أو إصدار الفاتورة." OWNER_UNASSIGNED |
| Settlement/commissions | UNKNOWN (idea.md §12): Settlement domain scope to be defined. OWNER_UNASSIGNED |

---

## 6. C3 Disposition

**EXCEPTION:** Institution-internal ERP module; institution-defined accounting rules. C3 deferred.


---

## 6. Security and Trust

- **Authorization:** Access restricted strictly to authorized financial operators (`ACT-INST-ADMIN`); multi-factor authentication enforced.
- **Auditability:** Every ledger mutation writes an immutable, append-only audit trail with actor identity and timestamp.

---

## 7. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Ledger imbalance during transaction | Transaction aborts completely; rollback guarantees double-entry integrity |
| Settlement reconciliation discrepancy | Discrepancy logged to reconciliation queue; manual resolution workflow initiated |
| Storage node failure | Failover to synchronous database standby without data loss |

---

## 8. Operations and Reliability

- **Monitoring:** Daily automated reconciliation jobs emit pass/fail metrics to operational dashboard.
- **Retention:** Financial-record retention is governed by `policy:financial.retention`; value is institution/jurisdiction-specific and requires Finance, Legal/Compliance approval before production. Records required for reconciliation, audit, or statutory obligations must not be deleted early.

---

## 9. Open Risks and Decisions

- Multi-currency exchange rate feed integration — `OPEN` (`OWNER_UNASSIGNED`). Action: define supported fiat and regional currencies.
