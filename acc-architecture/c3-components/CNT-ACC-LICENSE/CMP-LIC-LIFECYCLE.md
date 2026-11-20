# CMP-LIC-LIFECYCLE — License Lifecycle Manager

## 1. Identity

| Field | Value |
|---|---|
| **Component ID** | CMP-LIC-LIFECYCLE |
| **Parent Container** | CNT-ACC-LICENSE |
| **Purpose** | Manages license state transitions: Active → Suspended → Reactivated → Expired → Revoked. Handles renewal, suspension, expiry scheduling, and revocation. |
| **Scope Boundary** | State machine for license lifecycle. Does NOT issue new licenses (CMP-LIC-ISSUANCE) or answer validation queries (CMP-LIC-ENTITLEMENT). |

---

## 2. Collaborators

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACM-ADMIN | Inbound | Admin-initiated renewal, suspension, revocation requests |
| Scheduled job (internal) | Inbound | Checks for expiring/expired licenses and transitions state |
| CNT-ACC-EVENTBUS | Outbound | Publishes LicenseRenewed/Suspended/Revoked/Expired events |
| CNT-ACC-AUDIT | Outbound | Logs all state transitions with actor and reason |

---

## 3. Behavior, Rules, and State

**License state machine:**

> **SCOPE NOTE:** Two distinct license workflows coexist. Their lifecycle state machines are **separate and must not be conflated:**
>
> - **Marketplace Software License** — created directly in `ACTIVE` status (no `ISSUED` or `ACTIVATED` intermediate state). CMP-LIC-LIFECYCLE manages ongoing transitions after ACTIVE.
> - **Institutional Subscription License** — created in `ISSUED` status via admin-initiated flow, then transitions `ISSUED -> ACTIVATED -> ACTIVE`. See `supporting-views/dynamic-license-flow.md` Sections 3 and 7.

**Marketplace Software License state machine (after ACTIVE):**
```
[ACTIVE] -> Suspended (admin action)
[SUSPENDED] -> Active (admin reactivation)
[ACTIVE] -> Expired (trigger relative to validity end and any approved grace is OPEN)
[ISSUED/ACTIVATED/ACTIVE/SUSPENDED/EXPIRED] -> Revoked (admin action, permanent)
[ACTIVE/EXPIRED] -> Renewed (validity_until extended) -> Active after authorized delivery/reactivation
```

**Institutional Subscription License state machine (full):**
```
[ISSUED] -> Activated (admin activates subscription)
[ACTIVATED] -> Active (activation confirmed)
[ACTIVE] -> Suspended (admin action)
[SUSPENDED] -> Active (admin reactivation)
[ACTIVE] -> Expired (trigger relative to validity end and any approved grace is OPEN)
[ACTIVE/SUSPENDED] -> Revoked (admin action, permanent)
[ACTIVE/EXPIRED] -> Renewed (subscription period extended) -> Active after authorized delivery/reactivation
```

**Rules (both workflows):**
- Revocation is permanent - no transition back to Active
- Expiry scheduling and the relationship of status timing to any approved grace remain OPEN; grace is not automatic.
- Renewal extends validity as authorized; any grace reset follows the approved policy.
- All transitions require actor_id and reason (for audit trail)
- Institutional ISSUED -> ACTIVATED -> ACTIVE transitions apply only to institutional subscriptions; marketplace licenses start ACTIVE directly (no intermediate state)

---

## 4. Data

Modifies License records owned by CMP-LIC-ISSUANCE. Maintains transition history.

---

## 5. Failure Modes

| Failure | Response |
|---|---|
| Scheduled expiry job fails | License remains in Active state past expiry; monitoring alert required |
| Admin suspension blocked (service down) | Suspension pending; operations team alerted |

---

## 6. Security

- State changes restricted to authorized admin actors — CONFIRMED (idea.md §9): ACT-PLATFORM-ADMIN, ACT-INST-ADMIN (within scope)
- CONFIRMED (idea.md §11): "LicenseRenewed/Suspended/Revoked/Expired" events published and audited

---

## 7. Operational Concerns

| Concern | Note |
|---|---|
| SLI | CONFIRMED (idea.md §11): "تراخيص قربت من الانتهاء" monitored — proactive expiry alerts needed |
| Risk | Grace period policy UNKNOWN (idea.md §12) — OWNER_UNASSIGNED |


---

## 8. Verification and Tests

### 8.1 Acceptance Test Scenarios

| Scenario | Input / Precondition | Expected Verification Outcome |
|---|---|---|
| Admin license suspension | Platform admin requests suspension | License state transitions to `SUSPENDED`; `LicenseSuspended` event published |
| License renewal extension | Approved renewal processed | Validity extended and any grace handling follows approved policy; audit retained |
| Scheduled expiry transition | Approved expiry/status policy trigger | Transition and audit follow the approved rule; no automatic grace is assumed |
