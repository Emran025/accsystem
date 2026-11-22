# Closure-loophole audit — Cycle 05

**Baseline:** `62b49e2f853873374ebe9dcb46f287b8b0bb05bd`  
**Disposition:** one critical false-closure path repaired; other gates remain open and are not silently neutralized.

## Confirmed loopholes

The audit confirmed that `ACCEPTED` was previously a freely writable registry value. Strict-ready checked the literal status and other text predicates, but did not require an authorized approver, approval timestamp, approval artifact, content baseline, or executed verification evidence. A future contributor could therefore synchronize a Markdown row and CSV row to `ACCEPTED` without an authority-bearing record.

The audit also confirmed that ordinary `evidence_refs` and `verification_refs` are free text, that planned verification is detected by a substring heuristic, and that open-decision fields are not linked to accepted decision records. Release-status consistency is a limited status-record check and is not a release-readiness decision. These weaknesses remain distinct from the current strict-ready failure and are not being presented as closed by structural tests.

## Executable repair

The requirements validator now makes `ACCEPTED` fail closed unless all of the following are present:

- an approval record keyed by requirement ID;
- an active identity in `authorized-approvers.json`;
- authority role, decision scope, approval reference, and ISO-8601 approval time;
- a content hash matching the current requirement row;
- an independent verification record with `EXECUTED` or `REVIEWED` state and `PASS` result;
- a matching subject hash, artifact reference, execution timestamp, and independent reviewer identity; and
- resolvable approval and verification artifact references.

The three machine-readable registries are intentionally empty because no truthful approval or acceptance evidence exists. A direct status edit to `ACCEPTED` is now rejected during ordinary structural validation, not only during strict-ready evaluation. Regression coverage proves this negative path.

## Deferred controls that remain explicit

The following require separate bounded reforms rather than a fabricated bulk conversion:

- typed and resolvable evidence records for the 238 distinct current evidence-reference values;
- typed verification run records for the 233 planned SREQ references;
- decision-registry status and authority binding for the 22 proposed ADR/decision records;
- current-baseline and input-hash binding for generated release reports;
- authoritative Use Case registry semantics distinct from function IDs; and
- retirement evidence hashes and exact claim-level anchors beyond file/anchor existence.

Until those controls and their underlying evidence exist, all 871 active blocker occurrences remain open. This audit does not promote, retire, or accept any requirement.
