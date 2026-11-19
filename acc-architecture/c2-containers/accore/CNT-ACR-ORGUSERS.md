# CNT-ACR-ORGUSERS — Organization & Users (ACCore)

**Parent:** SYS-ACCORE | **Level:** C2 | **C3:** Exception

---

## 1. Identity
| Field | Value |
|---|---|
| **Container ID** | CNT-ACR-ORGUSERS |
| **Purpose** | Manages institution employees, their roles, permissions, branch assignments, and local settings within ACCore. Entirely independent from platform-level Identity & Access. |
| **Scope Boundary** | Institution-internal user management only. Does NOT integrate with CNT-ACC-IDENTITY for local ERP roles. If a platform identity is needed for marketplace access, it is linked separately via CNT-ACC-IDENTITY membership. |

CONFIRMED (idea.md §4.1): "Organization & Users — الموظفون والأدوار والصلاحيات والفروع والإعدادات."
CONFIRMED (idea.md §2.1.1): "يظل ACCore نظام ERP وتشغيل خاصاً بها" — local user management is institution responsibility.
CONFIRMED (idea.md §2.1.1): "وإذا احتاج موظف المؤسسة إلى هوية موحدة للسوق، تُربط هويته بعضوية منصة محددة دون نقل صلاحيات ERP المحلية."

---

## 2. Key Relationships

| Collaborator | Direction | Role |
|---|---|---|
| CNT-ACC-IDENTITY | Outbound (optional) | Links institutional user to platform membership for marketplace access; does NOT transfer ERP roles |

---

## 3. Technology Stack

UNKNOWN — institution-owned ERP module. OWNER_UNASSIGNED.

---

## 4. Data Owned

Employee records, local roles, permissions, branch/department assignments. All institution-local.

---

## 5. C3 Disposition

**EXCEPTION:** Institution-internal user management, independent of platform Identity & Access. C3 deferred.


---

## 6. Security and Trust

- **Credential Storage:** User passwords hashed using Argon2id with unique salts; credentials never stored in plaintext.
- **Directory Integration:** Supports LDAP/Active Directory synchronization with TLS transport encryption.

---

## 7. Failure Modes and Resilience

| Failure Scenario | Mitigation Strategy |
|---|---|
| Enterprise LDAP directory unreachable | Local credential cache allows ongoing authentication for cached users |
| Concurrent user profile update conflict | Optimistic locking on user records prevents accidental overwrites |
| Session token spoofing attempt | Cryptographic signature validation rejects untrusted tokens; security event logged |

---

## 8. Operations and Reliability

- **Synchronization:** Directory sync jobs execute during off-peak windows; sync duration monitored via metric alert.
- **Scalability:** Horizontal scaling of stateless authentication worker nodes behind load balancer.

---

## 9. Open Risks and Decisions

- SCIM 2.0 protocol support for automated identity provisioning — `OPEN` (`OWNER_UNASSIGNED`).
