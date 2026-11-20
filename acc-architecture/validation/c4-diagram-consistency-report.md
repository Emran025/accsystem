# ACC C1–C3 Cross-Level Consistency Report

> **Historical review record:** Dated 2026-11-19. Findings below are retained for provenance and must be read with the corrected `UNKNOWN`/no-numeric-TTL contract in current artifacts. They do not claim current failure, owner approval, or release readiness.

**Review date:** 2026-11-19. **Baseline:** supplied archive SHA-256 `806faea3966d0abb0b3b955360bee2529d3bd9238e5b265862ed82da76bc45ac`. Reviewers compared registry/decomposition/interface records with actual diagrams, specifications, ADRs, and dynamic flows. The observations below preserve conflicts; this report does not resolve them or attribute proposals to the owner.

## Verified alignments

- The registry-derived identity and parentage of the reviewed flow are consistent: `SYS-ACCSYSTEM` owns `CNT-ACC-ORDERS`, `CNT-ACC-INTEGRATION`, and `CNT-ACC-PAYMENT`; `SYS-ACCORE` owns `CNT-ACR-CONNECTOR`; order, integration, and connector decompositions use their registered C3 IDs. See `registry/decomposition-map.json`, `registry/elements.json`, and the relevant `c2-containers/` and `c3-components/` files.
- ACCore is documented as institutional source of truth for product/inventory/sales/finance records, while ACCSystem owns marketplace projection and central ParentOrder/SellerOrder lifecycle. Search is described as a derived index. See `c1-context/systems/SYS-ACCORE.md`, `c1-context/systems/SYS-ACCSYSTEM.md`, `c2-containers/accsystem/CNT-ACC-SEARCH.md`, and ADR-001/ADR-004.
- The multi-seller direction is consistent across ADR-016, the order saga/splitter records, and `supporting-views/dynamic-purchase-flow.md`: one ParentOrder, seller-specific SellerOrders, and one reservation operation at each seller's ACCore. The reservation relay and saga specifications preserve post-dispatch ambiguity as `UNKNOWN`, block dependent payment, and require query/reconciliation. This validates the written intent, not runtime behavior.
- `PaymentUnknown` is kept distinct from definitive provider decline in the reviewed Payment and saga material. Circuit-open, timeout, or lost payment response is not itself a final payment result. The new safe saga text does not erase the separate reservation-source contradiction below.
- The C1/C2/C3 system, container, and component identities and parent mappings show no duplicate registry IDs or names and no wrong-parent ID found by the independent completeness recount.

## Contradiction and consistency register

### CONS-001 — Reservation timeout and expiry behavior conflicts

**Classification:** contradiction. **Severity:** critical. **Confidence:** high.
**Affected IDs:** `IF-ACC-RESERVE-SAGA`, `IF-ACR-RESERVATION-RESP`, `CMP-INT-RESERVATION`, `CMP-CON-RESERVATION`, `CNT-ACC-ORDERS`.
**Evidence A:** `supporting-views/interface-contracts.md`, reservation failure/TTL rows: a timeout is called uncertain and followed by a status query, but the same row says “compensate if no confirmation”; the TTL row says “ACCore auto-releases; saga compensates” and marks it confirmed.
**Evidence B:** `c3-components/CNT-ACC-INTEGRATION/CMP-INT-RESERVATION.md` says timeout, disconnection, circuit-open, or lost response becomes `UNKNOWN`; it never emits rejection or releases only because time elapsed. `c3-components/CNT-ACC-CONNECTOR/CMP-CON-RESERVATION.md` says timeout does not prove rejection or trigger release. ADR-013 requires `UNKNOWN`, query/reconciliation, and no release, void, or repeated side effect solely from elapsed time; ADR-006 distinguishes definitive rejection from uncertainty.
**Impact:** an implementer following the interface/TTL rows could release stock while ACCore has accepted a hold, or fail an order before the outcome is known.
**Disposition:** unresolved. Do not infer a timeout, expiry duration, or safety rule. Product/architecture and institution/operations owners must adjudicate the conflict and publish one approved versioned policy. The generic C2 row “ACCore reservation fails” is ambiguous and is not independently treated as a timeout contradiction.

### CONS-002 — ACCore connectivity initiation is not consistently scoped

**Classification:** inconsistency / deployment and trust-boundary risk. **Severity:** high. **Confidence:** high.
**Affected IDs:** `SYS-ACCORE`, `SYS-ACCSYSTEM`, `CNT-ACR-CONNECTOR`, `CNT-ACC-INTEGRATION`, `ADR-015`.
**Evidence A:** `c1-context/systems/SYS-ACCORE.md` marks inbound ACCSystem calls to the connector as confirmed and says the connector exposes a secure inbound endpoint for reservation and confirmation commands. Its C1 relationship table repeats inbound REST/OAuth.
**Evidence B:** ADR-015 states outbound-initiated authenticated connectivity is the default for firewalled institutions and protected inbound connectivity is optional. `c2-containers/accore/CNT-ACR-CONNECTOR.md` also describes outbound polling/push and optional protected inbound connectivity. The connector C3 view draws direct HTTPS POST calls from ACCSystem to ACCore without indicating that inbound reachability is optional or mediated according to institution policy.
**Impact:** readers may interpret inbound firewall exposure as a product-wide requirement, which changes the trust perimeter and contradicts the stated default deployment posture.
**Disposition:** unresolved as a documentation scope issue. Retain the ADR's stated default/optional distinction. Owner/security/operations should decide whether C1 describes a supported capability or every deployment; the diagram must not select a network mode by inference.

### CONS-003 — Reservation response vocabulary and modality differ

**Classification:** contract inconsistency. **Severity:** high. **Confidence:** high.
**Affected IDs:** `IF-ACC-RESERVE-SAGA`, `IF-ACR-RESERVATION-RESP`, `CMP-INT-RESERVATION`, `CMP-CON-RESERVATION`, `CMP-CON-ORDERRECEIVER`.
**Evidence A:** `supporting-views/interface-contracts.md` describes `ACCEPTED` and `REJECTED` response values, plus a synchronous REST request whose response may be synchronous or via callback. `CMP-INT-RESERVATION.md` persists `ACCEPTED`, `REJECTED`, and `UNKNOWN`.
**Historical Evidence B:** the prior version of `c3-components/CNT-ACR-CONNECTOR/component-diagram.md` labelled the return as `{RESERVED or INSUFFICIENT}` and `CMP-CON-ORDERRECEIVER.md` used `RESERVED → CONFIRMED`; both source locations were corrected in this working copy. The integration diagram includes a callback-labelled response path, while the connector diagram summarizes reservation as synchronous.
**Impact:** consumers may map transport uncertainty, definitive business rejection, and accepted hold differently; request/reply vs callback behavior is also unclear.
**Disposition:** unresolved. Define the response enum, mapping, and delivery mode in one versioned interface contract and align diagrams after approval. Keep all ambiguity `PROPOSED`/`UNKNOWN` until then.

### CONS-004 — Order confirmation and ACCore commit/accounting implications are ambiguous

**Classification:** semantic ambiguity / potential contradiction. **Severity:** high. **Confidence:** medium.
**Affected IDs:** `CNT-ACC-ORDERS`, `CMP-CON-ORDERRECEIVER`, `CNT-ACR-INVENTORY`, `CNT-ACR-SALES`, `ADR-016`.
**Evidence A:** `CMP-CON-ORDERRECEIVER.md` says receipt of `OrderConfirmed` creates an ACCore SalesOrder and transitions the reservation to `CONFIRMED (committed sale)`. The connector diagram depicts an OrderConfirmed path.
**Evidence B:** `c1-context/systems/SYS-ACCORE.md` lists the financial-record commitment point as unknown; the scope and requirements leave the institution-defined accounting trigger open; `CMP-CON-ORDERRECEIVER.md` itself identifies the financial commitment point as unknown.
**Impact:** readers may infer one global trigger for stock consumption and financial posting, although institution policy remains open. This could lead to premature/missing sales or ledger entries.
**Disposition:** do not equate inventory reservation consumption, SalesOrder creation, and financial journal posting unless the approved contract explicitly does so. Institution/business/finance owners must decide the triggers.

### CONS-005 — Payment webhook route bypasses the documented adapter

**Classification:** diagram/specification contradiction. **Severity:** medium. **Confidence:** high.
**Affected IDs:** `CMP-PAY-ADAPTER`, `CMP-PAY-ORCHESTRATOR`, `IF-ACC-PAYMENT-WEBHOOK`.
**Evidence A:** `c3-components/CNT-ACC-PAYMENT/component-diagram.md` routes `EXT_PAY → ORCH` for the provider webhook.
**Evidence B:** `CMP-PAY-ADAPTER.md` identifies the Provider Adapter as the first receiver and signature-validation point before relaying to the orchestrator.
**Impact:** the diagram omits the documented validation boundary and could mislead implementation/security review.
**Disposition:** the coordinator applied the source-backed adapter-first diagram route in V5 and rendered the changed block. Validate against the signed interface/security contract before final closure.

### CONS-006 — Duplicate focal nodes and self-edges in C1 overlays

**Classification:** diagram-content error. **Severity:** high. **Confidence:** high.
**Affected IDs:** `SYS-ACCSYSTEM`, `SYS-ACCORE`, `SYS-ACCOMMERCE`, `SYS-ACMANAGEMENT`, `SYS-ACCMARED-SUP`, `SYS-ACCMARED-COU`.
**Evidence:** `c1-context/c4-context-and-container-overlays.md` declares a focal system node and a second node for the same system ID/name in each affected C1 view, then connects them with an edge labelled “system boundary.” The duplicate is a self-relation, not a distinct C4 system boundary.
**Impact:** viewers may read one system as two or infer an unsupported self-interaction.
**Disposition:** V5 removed each duplicate alias and self-edge in the six identified C1 blocks, retargeting existing genuine edges to the single canonical focal node. All six changed blocks rendered. Confirmed ID/diagram fix; it does not resolve the separate ACCSystem context omission or arrow-direction questions.

### CONS-007 — ACCSystem C1 context omits documented direct relationships

**Classification:** semantic coverage gap. **Severity:** high. **Confidence:** high.
**Affected IDs:** `SYS-ACCSYSTEM`, `SYS-ACCOMMERCE`, `SYS-ACMANAGEMENT`, `SYS-ACCMARED-SUP`, `SYS-ACCMARED-COU`, `EXT-PAYMENT-PROVIDER`, `EXT-PACKAGE-CDN`.
**Evidence A:** ACCSystem C1 overlay shows a generic actors node and edges to ACCore and payment provider.
**Evidence B:** `c1-context/systems/SYS-ACCSYSTEM.md` §§2–4 and `c1-context/landscape.md` document direct clients/dependencies including ACCommerce, ACManagement, ACCMared Supervisor/Courier, payment provider, and CDN.
**Impact:** the focal C1 view does not explain the actual documented environment.
**Disposition:** add only direct relations established by those sources. Do not introduce detailed protocol, synchronization, or deployment claims not present in the sources.

### CONS-008 — Two ACCSystem C2 views differ without a precedence rule

**Classification:** inconsistency / possible duplicate view. **Severity:** medium. **Confidence:** high.
**Affected IDs:** all C2 child containers of `SYS-ACCSYSTEM`.
**Evidence:** `c1-context/c4-context-and-container-overlays.md` has a registry-grouped ACCSystem view with a sparse set of edges and no external users/systems; `c2-containers/accsystem/container-diagram.md` includes external nodes and more detail, but not all edges have clear purpose/direction. No explicit index or source declares one view authoritative or the other partial.
**Impact:** readers can draw different conclusions about interfaces and responsibility from two views of the same system.
**Disposition:** retain both until a source-backed reconciliation defines a canonical view or complementary scopes. Do not silently delete either.

### CONS-009 — C3 Integration title does not match its decomposition scope

**Classification:** scope/title mismatch. **Severity:** medium. **Confidence:** high.
**Affected ID:** `CNT-ACC-INTEGRATION`.
**Evidence:** `c3-components/CNT-ACC-INTEGRATION/component-diagram.md` is titled as a `CMP-INT-ORDERNOTIFY` component diagram, but the scope box names the `CNT-ACC-INTEGRATION` container and includes several Integration components.
**Impact:** the filename, heading, and scope imply different things about what is decomposed.
**Disposition:** V5 changed only the heading to name CNT-ACC-INTEGRATION; diagram components/relationships were left unchanged and the block rendered successfully.

### CONS-010 — Registered interface IDs are not all traceable from diagrams

**Classification:** traceability improvement. **Severity:** low. **Confidence:** high.
**Affected IDs:** `IF-ACC-CATALOG-QUERY`, `IF-ACC-ORDER-CREATE`, `IF-ACC-EVENT-ENVELOPE`, `IF-ACC-SOFTDL`.
**Evidence:** all nine IDs exist in `registry/interfaces.json` and `supporting-views/interface-contracts.md`; an independent scan found five named in Mermaid, leaving the four above without literal ID labels. Some corresponding relationships are drawn without interface IDs.
**Impact:** stable contract IDs cannot be followed directly from those diagram edges. This does not prove that relationships are missing or that C4 requires IDs on every edge.
**Disposition:** optional traceability improvement: add labels where diagram clarity permits, or maintain an explicit relation-to-interface crosswalk. Do not elevate to a C4 conformance failure.

### CONS-011 — C2 decomposition exceptions are not enumerated in the coverage matrix

**Classification:** auditability gap. **Severity:** low. **Confidence:** high.
**Affected files:** `validation/c4-diagram-coverage-matrix.md`, `registry/elements.json`.
**Evidence:** the registry records 23 C2 records with C3 `EXCEPTION` status and rationale; the matrix lists only the 65 selected C1/C2/C3 items and contains no per-exception `NOT-APPLICABLE` rows or appendix.
**Impact:** a matrix-only reader cannot distinguish a justified C3 exclusion from an omitted matrix entry, although the registry currently holds the rationale.
**Disposition:** V5 added a 23-row registry-exception appendix, preserving the 7/30/28 element denominator. Registry provenance is reproduced, not independently approved.

## Review limitations

The first consistency reviewer focused on the commerce path and explicitly did not claim a full semantic review of all 65 selected C1/C2/C3 entries or every edge. The independent completeness agent recounted IDs and exceptions, reviewed actual Mermaid blocks, and checked local file links. This is still a document-level audit; it does not verify deployed APIs, firewall behavior, event delivery, data stores, tests, owner sign-off, or production readiness. Mermaid success is syntax/render evidence only.


## V5 coordinator correction and verification record (2026-11-20)

The independent item tickets themselves changed no architecture sources. After the independent critique, the coordinator applied only narrow source-backed corrections: (1) removed duplicated focal aliases and their self-boundary edges from the six C1 views listed in CONS-006, retaining one canonical node and retargeting existing edges; (2) corrected the Integration C3 heading to the registered parent container without modifying the diagram body; and (3) routed the Payment provider webhook to CMP-PAY-ADAPTER and then to CMP-PAY-ORCHESTRATOR, consistent with the adapter's documented first-receiver/signature-validation responsibility. These are documentation corrections, not owner policy decisions.

All eight changed Mermaid blocks rendered via `manus-render-diagram`; deterministic checks confirmed one focal declaration and no system-boundary self-edge in each of the six C1 sections, the direct provider-to-orchestrator webhook edge is absent, and the Integration title names the parent. The correction does not close the reservation/TTL contradiction, connectivity/contract/accounting uncertainties, C1 arrow-direction ambiguity, or unresolved C2 view-scope/precedence. No approval, production readiness, or standards certification is claimed.
