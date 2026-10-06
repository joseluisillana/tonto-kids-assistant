# Inference Provider - DevExpert — historical planning provenance and handoff

This is a retrospective migration document dated 2026-10-06, not evidence that
a separate plan was written before the historical implementation. Read [spec.md](spec.md)
and [journal.md](journal.md). Original instructions remain in the definition.

## Objective and scope

Preserve the original definition, evidence and corresponding GitHub references.
No product implementation, new dependency or remote issue import is authorized.

## Original shared implementation plan

Use the single [inference execution plan](../011-inference-providers/plan.md)
for shared chat/STT phases. No dedicated provider-specific prior plan was located;
this file references the existing shared owner rather than duplicating its content.

## Future work and verification

Provider phases 0-3 completed 2026-06-13. D025 deprecates real DevExpert operation; done records historical adapter delivery, not current provider availability.
For a newly authorized change, write proposed steps, affected files, dependencies,
acceptance and verification before implementation. Historical checks/evidence live
in the linked sources; relocation itself does not repeat hardware/provider tests.

## Workflow isolation and implementation prompt

Current migration branch: docs/historical-records-migration; serial execution,
no parallel worktree needed. Future implementation requires an authorized focused
project branch and prior plan; assess collisions, integration order and tests.
Handoff: read the definition, this retrospective plan, journal and mandatory root
workflow; confirm current approval and scope before changing behavior. Preserve
source contracts, evidence and GitHub URLs, use official checks and record results.

No secrets, credentials, tokens, connection strings, PII or real customer data.
Parameter names only for sensitive configuration. Maintain journal and updated;
status changes synchronize with INDEX.md in the same change; preserve history.
