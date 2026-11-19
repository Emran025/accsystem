# Architecture consistency ledger — {{system_name}} / {{revision}}

> Derived index of the current architecture baseline, not a substitute for source evidence, accepted requirements, registry or ADRs. Update it at every stage boundary and after any material decision/change. Keep phase/version qualifiers explicit.

- **Owner / last reviewed:** {{owner_or_assignment_action}} / {{timestamp}}
- **Baseline sources/revision:** {{source_paths_and_revision}}
- **Scope and phases covered:** {{scope_and_phase}}
- **Known limitations:** {{limits}}

## Canonical terms and boundaries

| ID / term | Canonical meaning | Scope/phase/version | Authority/status | Source/evidence | Affected artifacts | Last reconciled |
|---|---|---|---|---|---|---|
| {{term_or_boundary}} | {{meaning}} | {{scope}} | {{CONFIRMED/ASSUMPTION/PROPOSED/ACCEPTED/UNKNOWN}} | {{path#section}} | {{IDs/files}} | {{date}} |

## Requirements, constraints and invariants

| ID | Statement / measurable condition | Status | Authority/evidence | Phase | Affected IDs and artifacts | Verification / unresolved action |
|---|---|---|---|---|---|---|
| {{REQ/CON/INV-ID}} | {{statement}} | {{status}} | {{source}} | {{phase}} | {{IDs/files}} | {{test/evidence/owner/action}} |

## Decisions and architecture rules

| ADR/decision ID | Decision and status | Alternatives/trade-off reference | Scope/phase | Consequences and confidence | Affected IDs/files/diagrams | Acceptance authority or open action |
|---|---|---|---|---|---|---|
| {{ADR-ID}} | {{decision}} | {{ADR path}} | {{scope}} | {{consequences}} | {{IDs/files}} | {{accepted by and evidence / pending owner/action}} |

## Decomposition and ownership invariants

| Parent ID | Child IDs (complete list or partition index) | Responsibility/boundary | Owner/status | Evidence/source | Related views |
|---|---|---|---|---|---|
| {{parent}} | {{children}} | {{boundary}} | {{owner/status}} | {{source}} | {{view IDs/paths}} |

## Interface and data authority

| Interface/data ID | Provider/source of truth | Consumer/readers/writers | Contract/schema/version | Failure/consistency rule | Source/status | Affected functions/flows/views |
|---|---|---|---|---|---|---|
| {{ID}} | {{provider/authority}} | {{consumers}} | {{contract}} | {{rule}} | {{source/status}} | {{IDs/files}} |

## Unresolved conflicts and decisions required

| Finding ID | Claim A / source | Claim B / source | Scope/phase difference? | Impact/severity | Owner/action and revisit trigger | Status / resolution evidence |
|---|---|---|---|---|---|---|
| {{CON-ID}} | {{claim + path}} | {{claim + path}} | {{yes/no/unknown}} | {{impact}} | {{owner/action/trigger}} | {{OPEN/RESOLVED + evidence}} |
