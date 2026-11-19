# Diagram coverage matrix — {{system_name}} / {{revision}}

> Every in-scope stable ID must be accounted for at the diagram levels where it is applicable. Large diagrams may be partitioned; list the index and all partitions. A matrix entry proves traceability only, not semantic or visual correctness.

- **Registry/source revision:** {{path_and_revision}}
- **Diagram plan:** {{path}}
- **Last reconciled:** {{timestamp}}

## Coverage by registered element

| Element ID | Type/level | Applicable C4/concern view(s) | Diagram ID and file/partition | Presence/relationship verified against registry? | Disposition if absent | Evidence / reviewer / date |
|---|---|---|---|---|---|---|
| {{stable-ID}} | {{actor/system/container/component/code/data/interface}} | {{C1/C2/C3/C4/dynamic/deployment/concern}} | {{diagram ID + path + partition}} | {{yes/no/not checked}} | {{N/A/not selected/deferred/blocked + rationale/action}} | {{source/reviewer/date}} |

## Diagram partition index

| View family | Diagram/index ID | Scope and included IDs | Partition links/next view | Excluded IDs and reason | Syntax/render/visual status |
|---|---|---|---|---|---|
| {{view}} | {{ID/path}} | {{scope/IDs}} | {{links}} | {{IDs/reason}} | {{PASS/FAIL/NOT_VERIFIED + evidence}} |

## Coverage reconciliation

- Registry in-scope IDs: {{count and source}}
- IDs mapped to applicable diagrams: {{count/list}}
- IDs explicitly not applicable/not selected/deferred/blocked: {{count/list + reasons}}
- Unmapped IDs: {{must be none or blockers}}
- Duplicate/stale/unknown IDs in diagrams: {{must be none or blockers}}
- Relationship direction/labels and diagram abstraction-level review: {{result/evidence}}
- Automated check limitations: {{ID-only vs syntax/render/visual/semantic}}
