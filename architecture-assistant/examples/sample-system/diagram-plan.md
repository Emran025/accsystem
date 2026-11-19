# Diagram Plan — ParcelFlow (illustrative)

Scope: one illustrative parcel-shipment software system, not an enterprise portfolio. Audience: product stakeholders, developers and operations. Evidence: sample fixture only; assumptions/technology proposals are not production evidence.

| View | Status | Rationale and scope | Artifact/status |
|---|---|---|---|
| System context (C1) | REQUIRED | Show merchant, ParcelFlow and directly connected carrier at a business level. | `c1-context/context-diagram.md`; present with element types, descriptions, relationship direction, and key |
| Container (C2) | REQUIRED | Show web client, API, data store and external carrier with major protocols/technology status. | `c2-containers/container-diagram.md`; present with types, key, labels, and proposed/TBD technology status |
| Component (C3) | SELECTED | API and web have distinct meaningful responsibilities; focused diagrams support explanation. This fixture-specific selection does not imply universal decomposition. | `c3-components/containers/`; present with scope, keys, element types, relationships, and technology certainty stated |
| Code (C4) | NOT_SELECTED | No implementation repository/language is supplied; current module mappings are illustrative records, not a code diagram. Revisit after source code or an important design decision exists. | No code diagram; `c4-code/` records are conceptual mappings only |
| System landscape | NOT_SELECTED | Scope contains a single focal system, not an organization or multi-system portfolio. | Not applicable to this fixture |
| Dynamic | NOT_SELECTED | Fixture shows a short illustrative flow; no evidence of a complex or high-risk multi-step workflow. Revisit for retries/idempotency/compensation or asynchronous carrier interactions. | Not required by current evidence |
| Deployment | UNRESOLVED | Production/staging topology, runtime platform, trust zones, availability and operations are not specified. Do not invent nodes; request deployment evidence before drawing. | `deployment/deployment-view.md` notes unknowns; no validated deployment diagram |

Additional views: data ownership/model, carrier interface and cross-cutting views are separate concern documents, not additional official C4 diagram types. Their current existence does not imply a rendered/validated C4 view.

## Completion note

This plan distinguishes sample-document coverage from diagram quality. The C1/C2/C3 examples now include scope, element types, descriptions, keys, directional relationships and explicit proposed/TBD technology status where applicable. Mermaid syntax rendering and visual review have not been performed. The sample is not evidence that a production architecture is complete.
