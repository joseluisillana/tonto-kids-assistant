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
  - "ai/specs/001-historical-records-migration/cleanup-impact.md"
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

Migrate historical local records and retire the old structure with traceable
identity, content, evidence, dates and relationships. Report external link
breakage and obtain the operator's decision before removing affected paths.

## Included scope

Repository specs and their plans/prompts/auxiliary artifacts, local issue docs,
correct references to corresponding GitHub issues and shared journals. Inventory and
reviewable mapping precede any relocation. Inventory, reference mapping and
execution plan are prepared. The operator requested plan execution; relocation
now follows its batches and verification gates.

The operator extends this same spec on 2026-10-06 to remove the legacy structure,
including temporary transition documents. Preserve unique information from
the original spec instructions and phase-1 plan in ai/; retire the old
template with Git recovery only before removing
specs/, docs/plans/, docs/issues/ and the mapped standalone artifact aliases.
Shared journals, images and operating/architecture docs remain canonical.
Physical retirement also removes active dependencies on old paths; historical
path names may remain as attributed provenance with immutable Git recovery URLs.
See cleanup-impact.md for the exact candidates and affected external links.

## Excluded scope

Product behavior, new dependencies, CI/export scripts, runtime/provider/hardware
operation, relocation/mirroring of GitHub issues and changes to their relationships
or status. Remote issue bodies/comments remain unchanged unless the operator
explicitly authorizes the exact link-only corrections listed in cleanup-impact.md.
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
- Internal links and related entries resolve to canonical files or immutable
  source history, with no active references to deleted legacy paths.
- External links that would stop resolving are individually reported with source,
  impact and replacement; retirement waits for the operator's explicit policy decision.
- Every retired source is covered by preserved canonical content/provenance and
  the source hash ledger; preserve instructions and phase-1 evidence; retain the old template only in Git.
- The tracked tree has no specs/, docs/plans/, docs/issues/ or mapped standalone
  aliases after cleanup. Do not delete unrelated or untracked content.
- Do not create docs/specs/ or recreate retired directories. Current agent
  instructions must remove obsolete coexistence rules and direct all registered
  local work to ai/. docs/specs.md remains a project overview.
- Shared project journals retain existing evidence; detailed ongoing work is
  recorded in each ai/ journal. Global updates summarize milestone or project-wide
  decisions and link record journals without duplicating their change logs.
- Shared artifacts keep one canonical source; Git history is not rewritten.
- Coverage, relationships, links and content preservation are checked before completion.

## Security considerations

No secrets, credentials, tokens, connection strings, PII or real customer data.
Parameter names only for sensitive configuration. Use sanitized evidence;
do not read credential files. Preserve existing protection and D025 decisions.

## Risks

Stale body statuses versus merged PRs; closed issues with unchecked historical
checkboxes; abandoned/superseded specs; missing prior plans; shared evidence;
GitHub evidence needed to verify local references or resolve local status conflicts;
old main-branch document links can fail despite retained Git history; exported
NotebookLM sources still exclude ai/. Unknown external bookmarks cannot be enumerated.
These require explicit provenance and review rather than silent reinterpretation.

Plan before implementation; maintain journal.md. Every status change updates
ai/specs/INDEX.md in the same change; update dates for record changes. Keep history.
