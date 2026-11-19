# Skill: change-impact

Purpose: make bounded, traceable architecture changes.

## Procedure

Identify changed ID and its parent/children, interfaces, dependent components/functions, decisions, diagrams, tests and gates. Preserve IDs and accepted ADR history. Update only affected records, add changelog entry, rerun relevant validation and reopen impacted stage gates. Record rename/split/merge/delete mappings; do not silently erase accepted decisions.

## Required output

Provide evidence/source IDs, created/updated artifact paths, registry changes, gate result, unresolved facts and next-step recommendation.
