# CNT-ACM-PUBLIC — ACManagement Public Portal

**Parent:** SYS-ACMANAGEMENT | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACM-PUBLIC |
| **Purpose** | Unauthenticated public-facing web portal where visitors can browse ACC system/product catalog, view release notes and version information, and obtain signed download links for installation packages. |
| **Scope Boundary** | Unauthenticated zone only. Strictly separated from admin console (CNT-ACM-ADMIN). No admin APIs exposed in public zone. |

CONFIRMED (idea.md §2.1.1): "منطقة عامة للزوار لعرض تعريفات أنظمة ACC والميزات والإصدارات ومتطلبات التشغيل وروابط التنزيل."
CONFIRMED (idea.md §9): "فصل المسارات العامة عن لوحة الإدارة؛ لا تعرض واجهات الزوار أي API إداري."

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| ACT-VISITOR | Inbound | Primary user — browses catalog and downloads |
| CNT-ACC-APIGATEWAY → CNT-ACC-SOFTCAT | Outbound | Catalog queries and download URL generation (IF-ACC-SOFTDL) |

---

## 3. Technology Stack

UNKNOWN — web framework not specified. OWNER_UNASSIGNED.

---

## 4. Security

CONFIRMED (idea.md §9): WAF protection, rate limiting, login attempt logging applied at edge layer.

---

## 5. C3 Disposition

**EXCEPTION:** Unauthenticated web portal; UI decomposition deferred. Key content and security documented in `c1-context/systems/SYS-ACMANAGEMENT.md` and `supporting-views/security-view.md`.


---

## 6. Data Ownership and Consistency

- **Data Owned:** Read-only cached marketing content, institutional portal news, and public catalog highlights; owns no transactional data.
- **Consistency Model:** Cache-aside pattern with short TTL (5 minutes) and cache-invalidation events on content updates.

---

## 7. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Origin application container cluster failure | Edge CDN continues serving cached pages using `stale-while-revalidate` policy |
| Traffic spike (promotional event) | CDN absorbs 95%+ of traffic; origin auto-scales container instances based on CPU utilization |
| Content rendering exception | User presented with friendly fallback error page; origin error logged to monitoring stack |

---

## 8. Operations and Reliability

- **Deployment:** Static assets and server-side rendered pages distributed globally via CDN edge network.
- **Availability Target:** 99.9% uptime SLA for public-facing institution portals.

---

## 9. Open Risks and Decisions

- Server-side rendering (SSR) framework selection for SEO optimization — `OPEN` (`OWNER_UNASSIGNED`).
