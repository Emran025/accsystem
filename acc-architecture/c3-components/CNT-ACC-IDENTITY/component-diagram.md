# C3 Component Diagram — CNT-ACC-IDENTITY (Identity & Access Service)

**Container:** CNT-ACC-IDENTITY  
**System:** SYS-ACCSYSTEM  
**Status:** DRAFT | Evidence: idea.md §3.1, §5, §6

---

## Component Interaction Diagram

```mermaid
flowchart TD
    subgraph Callers["External Callers"]
        APIGW["CNT-ACC-APIGATEWAY\n(API Gateway)"]
        PLATFORMADMIN["CNT-ACC-PLATFORMADMIN\n(Platform Admin)"]
        AUDIT["CNT-ACC-AUDIT\n(Audit Log)"]
    end

    subgraph CNT-ACC-IDENTITY["CNT-ACC-IDENTITY — Identity & Access Service"]
        AUTH["CMP-IDN-AUTH\nAuthentication Engine"]
        RBAC["CMP-IDN-RBAC\nRBAC Policy Engine"]
        SESSION["CMP-IDN-SESSION\nSession Manager"]
        TENANCY["CMP-IDN-TENANCY\nTenancy Resolver"]
    end

    subgraph Stores["Data Stores"]
        IDENTDB[("Identity DB\nPostgres — users,\ncredentials, roles")]
        SESSSTORE[("Session Store\nRedis — active tokens")]
    end

    subgraph External["External"]
        EVENTBUS["CNT-ACC-EVENTBUS\n(Event Bus)"]
    end

    %% Login flow
    APIGW -->|"AuthN request\n(credentials / token)"| AUTH
    AUTH -->|"Resolve tenant context"| TENANCY
    AUTH -->|"Issue / validate session"| SESSION
    AUTH -->|"Load roles + permissions"| RBAC

    %% Session management
    SESSION <-->|"Read/write token"| SESSSTORE
    SESSION -->|"Token-expired event"| EVENTBUS

    %% Permission check (every protected API)
    APIGW -->|"AuthZ check\n(resource + action)"| RBAC
    RBAC -->|"Read role bindings"| IDENTDB

    %% Tenancy
    TENANCY -->|"Read institution context"| IDENTDB

    %% Admin operations
    PLATFORMADMIN -->|"Manage roles / users"| RBAC
    PLATFORMADMIN -->|"Manage tenant config"| TENANCY

    %% Audit
    AUTH -->|"AuthN event"| AUDIT
    RBAC -->|"AuthZ decision event"| AUDIT

    %% Data access
    AUTH <-->|"Credential read/write"| IDENTDB
```

---

## Component Summary

| Component | ID | Role |
|---|---|---|
| Authentication Engine | CMP-IDN-AUTH | Validates credentials, issues JWTs, MFA |
| RBAC Policy Engine | CMP-IDN-RBAC | Evaluates role-permission bindings per request |
| Session Manager | CMP-IDN-SESSION | Token lifecycle: issue, refresh, revoke, expire |
| Tenancy Resolver | CMP-IDN-TENANCY | Maps requests to institution context; isolates data scope |

---

## Key Flows

### Flow 1 — Login
1. API Gateway forwards credential/token → **CMP-IDN-AUTH**
2. AUTH resolves tenant via **CMP-IDN-TENANCY**
3. AUTH verifies credential → creates session via **CMP-IDN-SESSION** (writes to Redis)
4. AUTH returns signed JWT; logs AuthN event to **CNT-ACC-AUDIT**

### Flow 2 — Authenticated API Request
1. API Gateway intercepts request → **CMP-IDN-RBAC** evaluates `{actor_role, resource, action}`
2. RBAC reads role bindings from Identity DB → returns ALLOW/DENY
3. DENY → 403; ALLOW → request forwarded to target container

### Flow 3 — Session Revocation (Admin)
1. **CNT-ACC-PLATFORMADMIN** calls revoke
2. **CMP-IDN-SESSION** removes token from Redis (immediate invalidation)
3. Session-revoked event published to event bus → downstream containers may cache-bust

---

## Traceability

| Concern | Evidence |
|---|---|
| Multi-tenant isolation | CONFIRMED (idea.md §5.1 — per-institution ACCore, shared ACCSystem identity) |
| Least-privilege for admin/support | CONFIRMED (idea.md §6, §14 → ADR-011) |
| Session store (Redis) | ASSUMPTION — fast revocation requires in-memory store |
| MFA requirement | ASSUMPTION — not explicitly stated in idea.md §5; noted as UNKNOWN |

---

*Generated: 2026-11-15 | Not stakeholder-approved | Not production-ready*
