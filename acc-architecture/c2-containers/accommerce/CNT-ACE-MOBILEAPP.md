# CNT-ACE-MOBILEAPP — ACCommerce Mobile/Web App

**Parent:** SYS-ACCOMMERCE | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACE-MOBILEAPP |
| **Purpose** | The individual buyer's mobile/web shopping application. Provides browse, search, cart, checkout, order tracking, and license viewing capabilities entirely through ACCSystem platform APIs. |
| **Scope Boundary** | Client UI only — no server-side business logic. All data and operations served by ACCSystem via API Gateway. |

CONFIRMED (idea.md §2.1): "ACCommerce — تطبيق هاتف / واجهة عميل — الأفراد — التصفح والبحث والسلة والشراء وعرض طلبات الفرد."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-APIGATEWAY | Outbound | All API calls: IF-ACC-CATALOG-QUERY, IF-ACC-ORDER-CREATE |
| ACT-INDIVIDUAL | Inbound | Primary user of this application |

---

## 3. Technology Stack

UNKNOWN — mobile and/or web platform not specified in idea.md. OWNER_UNASSIGNED. Revisit: before Phase 2.

---

## 4. Security

CONFIRMED (idea.md §9): Short-lived tokens, secure token storage, no embedded service secrets in app binary.

---

## 5. C3 Disposition

**EXCEPTION:** UI client application; frontend decomposition deferred to implementation planning. Key behavior documented in `01-scope/scope-and-requirements.md` (FR-002).


---

## 6. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Network connection drops during checkout | Client displays connection alert; idempotency key ensures checkout retry does not duplicate orders |
| Catalog image load failure | Fallback placeholder image rendered; non-blocking to user navigation |
| API Gateway rate limiting (429) | Automatic client retry with backoff according to `Retry-After` response header |

---

## 7. Operations and Reliability

- **Deployment:** Apple App Store and Google Play Store; rolling release cadence.
- **Observability:** Crashlytics crash reporting; telemetry for screen transition times and network failure percentages.

---

## 8. Open Risks and Decisions

- Push notification infrastructure provider selection — `OPEN` (`OWNER_UNASSIGNED`). Action: compare Firebase Cloud Messaging vs OneSignal.
