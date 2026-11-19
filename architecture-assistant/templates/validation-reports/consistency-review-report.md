# Cross-artifact consistency and polish report — {{system_name}} / {{revision}}

- **Review date/revision:** {{timestamp/revision}}
- **Scope and source snapshot:** {{scope/source paths}}
- **Reviewer/pass:** {{reviewer or assigned role / iteration}}
- **Status:** {{PASSED / PARTIAL / BLOCKED}}
- **Ledger:** {{path}}
- **Diagram matrix:** {{path}}

## Findings and disposition

| Finding ID/severity | Claim A and source | Claim B and source | Affected IDs/files/views | Impact | Resolution or unresolved action/owner/trigger | Files reread after repair | Recheck evidence/status |
|---|---|---|---|---|---|---|---|
| {{CON-001/BLOCKER}} | {{claim/path}} | {{claim/path}} | {{IDs/files/diagrams}} | {{impact}} | {{fix or owner/action}} | {{exact paths}} | {{command/review + status}} |

## Diagram/unit coverage review

- C1/system boundary and actors: {{result/evidence}}
- C2/container/store inventory and all partitions: {{result/evidence}}
- Selected C3 component views versus parent C2 units: {{result/evidence}}
- Selected C4 code views versus evidenced source/components: {{result/evidence}}
- Dynamic/deployment/concern views versus IDs and contracts: {{result/evidence}}
- Unmapped or explicitly excluded/deferred IDs: {{list/reasons}}

## Read-after-write and checks

| Check | Exact command/tool/version or manual procedure | Scope/revision | Result | Evidence path | Limitations |
|---|---|---|---|---|---|
| Structural/reference | {{command}} | {{scope}} | {{result}} | {{report}} | {{limits}} |
| Diagram ID/syntax/render/visual | {{command/procedure}} | {{scope}} | {{result}} | {{evidence}} | {{limits}} |
| Outline/depth | {{command}} | {{scope}} | {{result}} | {{report}} | {{limits}} |
| Semantic cross-check | {{procedure}} | {{scope}} | {{result}} | {{findings}} | {{human checks not done}} |

## Fixed-point / handoff decision

- New material findings in this pass: {{count/list}}
- Repairs reread and rechecked: {{count/list}}
- Remaining blocker/major/minor/observation: {{list or none}}
- Next action and checkpoint: {{action/path/session}}
- Gate disposition: {{PASSED only with criteria / PARTIAL / BLOCKED}}
- Explicit statement: this review does not prove unknown requirements, production readiness, security or semantic correctness beyond its evidence and declared scope.
