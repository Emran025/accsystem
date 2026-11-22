# CNT-ACR-COMMERCE — Commerce Workspace (ACCore)

**Parent:** SYS-ACCORE | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACR-COMMERCE |
| **Purpose** | Embedded marketplace client within ACCore that allows institution employees and admins to browse the marketplace, create orders, and pass transaction results back to ACCore's operational records (sales, procurement). Same Commerce APIs as ACCommerce. |
| **Scope Boundary** | ACCore-embedded client UI. Does NOT own commerce logic — all flows use ACCSystem services via CNT-ACR-CONNECTOR. |

CONFIRMED (idea.md §4.1): "Commerce Workspace — واجهة التسوق والبيع التي تستخدم Commerce APIs في ACCSystem."
CONFIRMED (idea.md §14, ADR-003): "ACCommerce وواجهة التجارة داخل ACCore عميلان لـ Commerce Core نفسه."

---

## 2. Key Relationships

| Collaborator | Direction | Role |
|---|---|---|
| SYS-ACCSYSTEM (via CNT-ACC-APIGATEWAY) | Outbound | Browse catalog, cart, checkout, order tracking |
| CNT-ACR-SALES / CNT-ACR-FINANCE | Outbound | On order confirmation, triggers local sales/purchase record creation |

---

## 3. Technology Stack

ASSUMPTION: Web application embedded within ACCore UI. Technology not specified in idea.md. OWNER_UNASSIGNED.

---

## 4. C3 Disposition

**EXCEPTION:** ACCore's marketplace UI client; UI decomposition deferred to implementation planning phase.


---

## 6. Data Ownership and Consistency

- **Data Owned:** Institution-local commerce configuration, local cart staging data, and local channel sales records.
- **Consistency Model:** ACID transactions within local ACCore PostgreSQL store; eventual consistency with ACCSystem via Outbox events.

---

## 7. Security and Trust

- **Authentication:** Authenticated via ACCore user identity (`ACT-INST-EMPLOYEE`); role-based access control enforces departmental boundaries.
- **Data Protection:** Financial amounts and customer details encrypted at rest; transport secured via internal TLS.

---

## 8. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Local DB lock contention | Short transaction timeouts; automatic retry on serialization failure |
| Connector service unavailable | Orders held in local staging state until connector connection restored |
| Corrupt order payload | Rejected to quarantine log with diagnostic reason; admin alerted |

---

## 9. Operations and Reliability

- **Monitoring:** Database connection pool utilization and query duration metrics exported to Prometheus.
- **Reliability:** Automated hourly database backups; active-passive failover in clustered deployments.

---

## 10. Open Risks and Decisions

- Integration depth between local commerce staging and ACCore inventory allocation — `OPEN` (`OWNER_UNASSIGNED`).
