---
id: "001-historical-records-migration"
title: "Historical specs and issues migration"
status: in-progress
owner: "Project operator"
created: "2026-10-06"
updated: "2026-10-06"
related:
  - "ai/specs/001-historical-records-migration/plan.md"
  - "ai/specs/001-historical-records-migration/metadata-review.md"
  - "ai/specs/001-historical-records-migration/migration-map.md"
  - "docs/specs.md"
  - "docs/project-journal/post-mvp-touch-ui.md"
  - "https://github.com/joseluisillana/tonto-kids-assistant/pull/124"
  - "https://github.com/joseluisillana/tonto-kids-assistant/pull/125"
---

# Historical specs and issues migration

## Context and motivation

Phase 1 merged in PR #124 (818e88e), with both CI checks passing. The operator
approved integration and continuation on 2026-10-06. Existing specs, plans,
guides, journals and local issue definitions must enter the new process without
losing history or implying new acceptance. GitHub issues remain managed in GitHub;
the operator explicitly excludes importing or mirroring them as local records.

## Objective

Prepare a complete source/destination map, then migrate historical records
with traceable identity, evidence, dates and relationships.

## Included scope

Repository specs and their plans/prompts/auxiliary artifacts, local issue docs,
correct references to corresponding GitHub issues and shared journals. Inventory and
reviewable mapping precede any relocation. Inventory, reference mapping and
execution plan are prepared. The operator requested plan execution; relocation
now follows its batches and verification gates.

## Excluded scope

Product behavior, new dependencies, CI/export scripts, runtime/provider/hardware
operation, relocation/mirroring of GitHub issues and changes to their bodies,
relationships or status.
Do not rewrite original historical language or erase historical decisions.

## Acceptance criteria

- Every source has one proposed canonical destination or justified shared reference.
- Local records link corresponding GitHub issues by full URL in related.
- GitHub identities and parent/child relations stay managed in GitHub; no local mirrors.
- Only existing repository definitions receive local destination IDs.
- Guides/evidence remain distinguishable from definitions and implementation plans.
- Original dates/authorship are sourced; unknown values remain explicitly unknown.
- Retrospective plans are labelled; migration dates are separate from original dates.
- Status mapping uses evidence and records conflicts; no completion inferred from age/code.
- Migrated records have definition, plan, journal and synchronized index entries.
- Existing links remain navigable and shared artifacts keep one canonical source.
- Coverage, relationships, links and content preservation are checked before completion.

## Security considerations

No secrets, credentials, tokens, connection strings, PII or real customer data.
Parameter names only for sensitive configuration. Use sanitized evidence;
do not read credential files. Preserve existing protection and D025 decisions.

## Risks

Stale body statuses versus merged PRs; closed issues with unchecked historical
checkboxes; abandoned/superseded specs; missing prior plans; shared evidence;
GitHub evidence needed to verify local references or resolve local status conflicts.
These require explicit provenance and review rather than silent reinterpretation.

Plan before implementation; maintain journal.md. Every status change updates
ai/specs/INDEX.md in the same change; update dates for record changes. Keep history.
