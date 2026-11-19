# CMP-IDN-AUTH — Authentication Service

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-IDN-AUTH |
| **Parent Container** | CNT-ACC-IDENTITY (Identity & Access — ACCSystem) |
| **Purpose** | Handles user login, credential verification, token issuance, and MFA enforcement for all platform actors. Issues access tokens consumed by all downstream services via the API Gateway. |
| **Scope Boundary** | Authentication and token issuance only. Does NOT manage roles/permissions (CMP-IDN-RBAC) or session lifecycle beyond initial issuance (CMP-IDN-SESSION). |

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-APIGATEWAY | Inbound | Receives login requests from all client apps |
| CMP-IDN-SESSION | Outbound | Registers new session on successful auth |
| CMP-IDN-RBAC | Outbound | Fetches role claims to embed in token |
| CMP-IDN-TENANCY | Outbound | Fetches institution membership claims for institutional users |
| CNT-ACC-AUDIT | Outbound | Logs all auth events (success, failure, MFA, lockout) |

---

## 3. Behavior, Rules, and State

**Login flow:**
1. Receive credentials (username/password or token exchange)
2. Verify credentials against account store
3. If MFA enabled → challenge/verify second factor
4. On success: fetch role claims (CMP-IDN-RBAC) + institution membership (CMP-IDN-TENANCY)
5. Issue access token + refresh token; register session (CMP-IDN-SESSION)
6. Log auth success event

**Rules:**
- MFA REQUIRED for ACT-PLATFORM-ADMIN and ACT-SUPPORT-STAFF — CONFIRMED (idea.md §9)
- Failed attempts trigger lockout after threshold (UNKNOWN: threshold count). OWNER_UNASSIGNED.
- Token format: UNKNOWN (JWT with asymmetric signing PROPOSAL). OWNER_UNASSIGNED.
- Token TTL: UNKNOWN — short-lived recommended (idea.md §9: "رموز قصيرة العمر"). OWNER_UNASSIGNED.

---

## 4. Data and Side Effects

Reads: Account credentials store (hashed passwords). Does NOT own raw passwords.
Writes: Session record (via CMP-IDN-SESSION), audit log entry.

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| Credential store unavailable | All logins fail; return 503; public endpoints remain accessible |
| MFA provider unavailable | UNKNOWN — fallback policy needed. OWNER_UNASSIGNED. |
| Brute force attempt | Rate limiting at API Gateway + lockout policy at auth service |

---

## 6. Security

- CONFIRMED (idea.md §9): MFA enforced for privileged accounts
- CONFIRMED (idea.md §9): Short-lived tokens; secure storage in clients; no secrets in mobile apps
- Passwords stored as cryptographic hashes (ASSUMPTION — standard practice, not explicitly stated)
- Auth events logged for security signal monitoring — CONFIRMED (idea.md §11)

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | Auth success rate, login latency. Targets: UNKNOWN |
| Risk | Critical path — unavailability blocks all authenticated access |
