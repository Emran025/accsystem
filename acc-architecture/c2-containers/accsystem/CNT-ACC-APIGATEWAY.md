# CNT-ACC-APIGATEWAY — API Gateway / BFF

**Parent:** SYS-ACCSYSTEM | **Level:** C2 | **C3:** Exception

---

## 1. Identity

| Field | Value |
|---|---|
| **Container ID** | CNT-ACC-APIGATEWAY |
| **Purpose** | Single entry point for all inbound requests from ACCommerce, ACCore (via ACCore Commerce Workspace), ACManagement, and ACCMared clients. Performs request routing, authentication verification, rate limiting, and BFF response aggregation. |
| **Scope Boundary** | Routing, token validation/authentication, rate limiting, protocol translation, and request forwarding. Does NOT make authorization decisions; downstream services enforce authorization. |

CONFIRMED (idea.md §3.1): "API Gateway / BFF — استقبال الطلبات من التطبيقات، التوجيه، تحديد المعدل، تجميع الاستجابات المناسبة لكل عميل."

---

## 2. Collaborators and Dependencies

| Collaborator | Direction | Role |
|---|---|---|
| ACT-INDIVIDUAL (via CNT-ACE-MOBILEAPP) | Inbound | Individual buyer requests |
| ACT-INST-EMPLOYEE / ACT-INST-ADMIN (via CNT-ACR-COMMERCE) | Inbound | Institutional commerce requests |
| ACT-PLATFORM-ADMIN / ACT-SUPPORT-STAFF (via CNT-ACM-ADMIN) | Inbound | Admin console requests |
| ACT-VISITOR (via CNT-ACM-PUBLIC) | Inbound | Public portal requests |
| ACT-DELIVERY-SUPERVISOR (via CNT-AMD-SUPERVISOR) | Inbound | Supervisor delivery requests |
| ACT-COURIER (via CNT-AMD-COURIER) | Inbound | Courier delivery requests |
| CNT-ACC-IDENTITY | Outbound | Token/session validation and verified identity context for authenticated requests; no Gateway authorization decision |
| All ACCSystem backend services | Outbound | Routes authenticated and validated requests to appropriate services |

---

## 3. Technology Stack

| Aspect | Status | Note |
|---|---|---|
| Gateway technology | UNKNOWN | Not specified in idea.md. PROPOSAL: API Gateway (e.g., cloud-managed or self-hosted). OWNER_UNASSIGNED. |
| Protocol | CONFIRMED (idea.md §4.3, §9) | HTTPS/TLS for all inbound connections |

---

## 4. Data Owned

Owns: gateway routing configuration, rate limit counters (ephemeral), API versioning policy metadata.
Does NOT own: business domain data of any kind.

CONFIRMED (idea.md §3.1): "لا يملك بيانات المجال."

---

## 5. Interfaces

Exposes: All public API surface of ACCSystem (see idea.md §6.2 for reference API examples).
Consumes: CNT-ACC-IDENTITY for auth verification; all backend service APIs for routing.

---

## 6. Failure Modes and Resilience

| Failure | Response |
|---|---|
| Gateway overload | Rate limiting enforces per-client throttling. UNKNOWN: specific limits |
| Backend service unavailable | Returns appropriate HTTP error (503); circuit breaker ASSUMPTION — depends on gateway capability |
| Auth service unavailable | Reject all authenticated requests with 503; allow public-zone requests through based on route policy |
| DDoS | WAF at edge layer absorbs; CONFIRMED (idea.md §9): WAF applied for public-facing paths |

---

## 7. Security

- CONFIRMED (idea.md §9): Verifies all tokens; enforces TLS; WAF on public paths; rate limiting
- Does NOT perform authorization decisions — passes validated identity to downstream services
- CONFIRMED (idea.md §3.2): "لا يكون API Gateway مكاناً لقواعد العمل؛ دوره أمني وتوجيهي وتجميعي"
- Separation of public (visitor) and authenticated paths — CONFIRMED (idea.md §9)

---

## 8. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Request success rate, p99 latency. Targets: UNKNOWN |
| Scaling | Stateless — horizontally scalable. ASSUMPTION |
| Known risk | Single point of entry — high availability is critical; multi-AZ deployment recommended (PROPOSAL) |

---

## 9. C3 Disposition

**EXCEPTION:** No C3 decomposition. Rationale: routing/security cross-cut service with no complex business logic warranting component decomposition. Cross-cutting security concerns documented in `supporting-views/security-view.md`.
