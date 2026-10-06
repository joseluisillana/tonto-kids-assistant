# Historical records migration — execution plan

## Objective and source record

Implement [spec.md](spec.md), using [migration-map.md](migration-map.md) as the
source/destination and GitHub-reference matrix. Read [journal.md](journal.md),
root AGENTS.md, common workflow and relevant local instructions before acting.

Inventory and mapping are prepared. This plan defines the remaining migration;
it does not authorize implementation of historical product backlog. The operator
requested planning first, then explicitly requested implementation (see journal).
Execute within that authorization, without asking again for decisions already made.

## Included and excluded scope

Migrate 28 existing spec definitions and one existing local issue document,
with five validation/evidence artifacts, their mapped plans/prompts and relevant
auxiliary design/backlog docs. Preserve references to eight shared journals and
five existing visual assets, and repair affected consumers and old paths.
The current map covers 33 specs/ artifacts and 28 docs/plans/ files; two plan
files stay at their current locations as documented. Reconcile counts against
actual source/index state before assigning IDs.

GitHub issues remain defined, operated and retained in GitHub. Consult relevant
bodies/comments/PRs only to verify associations and evidence. Preserve full
corresponding issue URLs in each migrated local record's `related`. No remote
issue import, local mirrors, remote lifecycle synchronization or GitHub edits.
Exclude product changes, historical backlog implementation, runtime/provider/
hardware operation, dependencies, CI and export scripts. Preserve original language.

## Execution sequence and completion gates

### 1. Freeze inventory and resolve metadata before relocation

- Verify branch/status and baseline; preserve current planning changes. Compare
  source file inventory with the map and both indexes before reserving IDs.
- Confirm proposed spec IDs 002–029 and local issue ID 001 are available. They
  remain proposals until allocated; never renumber existing records.
- For every definition, establish title, owner, original creation/substantive
  update dates, supported status, paired plan, journal sections and tracking URLs.
  Use dated sources and Git history. Mark unknown authorship/ownership explicitly.
- Record original dates and migration date separately in provenance. Keep `updated`
  equal to the date the migrated record changes; preserve the legacy update date
  separately. Do not imply migration was original authoring.
- Resolve known conflicts individually: legacy cache proposal (#89), hierarchy
  stale local-pending status (#122/#123), parallel workflow planned heading,
  Linux migration draft heading (#95/#107), and release publication evidence.
  Use existing decisions, merged PRs and dated evidence; never infer done from code,
  age or closure of a contextual issue. Superseded/abandoned scope is described
  explicitly with its last supported lifecycle status, not labelled done merely
  because another solution shipped. If a decision truly cannot be inferred,
  isolate that record and request the specific missing decision.

Gate: every source has a destination/treatment, verified references and a
supported metadata decision, or an explicit unresolved exception. Do not silently
complete or relocate an unresolved record with invented metadata.

### 2. Migrate coherent batches with per-batch verification

| Batch | Definitions/local records | Dependencies and purpose |
| --- | --- | --- |
| A | 004/005 audio, 007 conversation, 020 Raspberry indicator, 024/025 web, 026/028/029 weekly work | Establish core contracts and move audio guides with their owner; retain weekly evidence references. |
| B | 009/010/011 inference, 018 parallel workflow, 027 capability pack | Share provider plan canonically, preserve D025 and historical operating guidance. |
| C | 012/013 Kivy, 021 touch UI | Keep five images and physical pending #88; preserve automated versus hardware evidence distinctions. |
| D | 006 legacy caches, 008 cleanup, 014/015/016 Linux repairs, 017 migration, 019 validation, 023 web audit | Carry the validation matrix and audit artifacts once; distinguish obsolete proposals from accepted migration scope. |
| E | 002 hierarchy, 003 secrets, 022 release; local issue 001 volume delay | Preserve scope reductions/publication evidence and local #114 document with its GitHub URL. |

For each batch:

1. Create spec.md/issue.md, plan.md and journal.md in each allocated folder.
   Add YAML metadata/provenance without broadly rewriting original requirements.
   Copy original body/content with narrowly reviewed relative-link rewrites.
2. Move the main paired plan into plan.md; keep distinct handoffs/prompts/guides
   as mapped artifacts. Provider-specific records reference the one shared
   inference plan instead of duplicating it. Records without a prior plan get an
   explicitly retrospective provenance/handoff plan; do not invent past planning.
3. Preserve guides, evidence and secret-design alternatives in their mapped
   artifacts with original dates and draft/accepted distinctions.
4. Seed each journal with an attributed migration entry and links to the original
   dated evidence sections. Optional extracts retain original author/date and
   context; no fabricated historical journal rows or copied customer data.
5. Preserve correct full GitHub URLs in `related`, differentiating corresponding
   tracking/phase links from contextual references and PRs in prose. For no
   documented issue, state that none was identified, without creating one.
   The local volume issue moves from docs/issues/, retaining #114; no remote
   definition/comments/status are copied to create a separate GitHub mirror.
6. Write one index row per migrated record, with matching ID/title/status/updated;
   retain the row thereafter. Change status and index in the same change.
7. Keep the legacy Markdown path as a concise transition pointer to the canonical
   destination. Preserve historical externally referenced heading fragments where
   needed, or route them to equivalent destination sections. Historical GitHub
   blob links must remain usable without editing remote issue bodies.
8. Verify source coverage, content conservation, links, metadata and relationships
   for that batch before proceeding. Record results and exceptions in journal.md.

Gate: all batch records have the required trio, preserved content/provenance,
correct relationships and navigable old paths. Cross-batch links may route through
remaining legacy sources until their owning batch is complete.

### 3. Reconcile shared consumers and source-of-truth navigation

- Update docs/specs.md, root navigation and affected documentation references to
  canonical paths; roadmap/milestone and product statuses change only if actual
  migration provenance warrants a factual correction, not due to relocation.
- Keep shared journals, decisions, architecture, runbooks, setup/report documents,
  visual assets, legacy plan template and phase-1 instrumentation evidence at their
  mapped canonical locations. They reference record sources instead of duplicates.
- Inspect Markdown references in component instructions and operational skills
  without rewriting their architecture/operating rules. Repair only links made
  stale by this migration. Retained transition pointers support external consumers.
- Revise ai/ transition notes to describe actual coverage and unresolved exceptions.
  Do not claim a full GitHub inventory is contained in the local issue index.
- Document the unchanged exporter limitation: ai/ is not selected. Do not modify
  scripts, regenerate source copies as a workaround or claim export completeness.

Gate: every local source has one canonical owner, consumers resolve to that owner,
and remaining transition pointers do not contain competing editable definitions.

### 4. Final review, evidence and integration

- Run the complete preservation/link/metadata checks below and inspect final diff.
- Record batch coverage and unresolved exceptions in this spec journal, with
  milestone summary in the global journal. Mark this migration done only when
  every required record and check is complete; keep it active if anything remains.
- Prepare focused documentation PR(s), describing relocated sources, preservation
  decisions, GitHub references and verification. Do not close remote issues using
  migration PR closing keywords; relocation does not implement their work.
- Use existing commit/export hook and CI; report the exporter coverage limitation.
  Verify CI and integrate only within the user's authorization.

## Affected files and dependencies

New canonical destinations and artifact owners are listed in migration-map.md.
Affected trees: ai/specs/, ai/issues/, legacy specs/, docs/plans/, docs/issues/,
plus docs/specs.md, shared journal and narrowly affected Markdown references.
No new runtime/development dependencies, tooling or permanent validators needed.
Use existing Git/gh and local tools for bounded checks; public GitHub read access
may require the execution environment's normal approval. No credentials are read.

## Acceptance and verification

- Coverage: 28 historical definitions + one local issue, with all mapped artifacts
  and shared-source treatments accounted for. The migration spec itself is separate.
- Identity: unique IDs, required definition/plan/journal trio, YAML fields and
  statuses from the documented enum; INDEX rows exactly match metadata. No deleted
  closed rows, reused IDs or remote GitHub issue mirrors.
- Preservation: compare source bodies, plans, prompts and auxiliary assets with
  the pre-migration Git baseline. Account for every change as metadata/provenance,
  narrow link rewrite, supported factual status annotation or legacy redirect.
  Original acceptance criteria, exclusions and historical evidence must remain.
- Dates/authorship: source attribution and unknown values are explicit; migration
  date does not replace original creation dates; retrospective plans labelled.
- Links: check new/legacy relative paths, images, heading fragments, shared-plan
  consumers and corresponding full GitHub URLs. Confirm GitHub issue identity
  and source association, not merely URL format. Do not require one-to-one mapping.
- Scope: no runtime/dependency/CI/export-script changes, remote mutations, provider
  operation, hardware validation or implementation of pending #53/#81/#88/#114.
- Commands: `git diff --check`, `git status --short --branch`, diff/content review
  and bounded link/coverage checks. Use temporary/local inspection helpers only.
  Runtime tests are unnecessary for pure documentation; CI still uses its existing
  setup/test/build gates. No automated result establishes physical acceptance.

## Workflow isolation and handoff

Current planning branch: docs/historical-records-migration, one checkout and one
coherent work item; no parallel agents/worktree needed. Batch ordering is serial.
If batches require independently reviewed PRs, use short project branches/worktrees
without sharing a checkout concurrently; update each after the preceding merge.
Collision risks: indexes, source transition files, docs/specs.md, root/consumer
links and shared journal. Reconcile any intervening integration before continuing.
GitHub tracking remains references to existing issues; no mirrored local imports.

## Implementation prompt

Implement spec.md using this plan and migration-map.md after execution is requested.
Read all three record files, root/common and affected local instructions. Verify
branch/status and original baseline; preserve current user-approved planning work.
Resolve metadata/evidence, then execute batches A–E serially with their gates.
Migrate only repository-defined records; GitHub issues stay in GitHub and local
records retain verified full tracking URLs in related. Preserve original content,
language, dates, authorship, evidence, plans/prompts and shared ownership; label
retrospective plans and unknowns. Keep navigable legacy paths, update indexes and
consumer references, and do not change product scope or operate providers/hardware.
Run the checks above, record real results/exceptions, and prepare reviewable PR(s).
Do not mark done or close a remote issue merely because files were relocated.

## Safety and record maintenance

No secrets, credentials, tokens, connection strings, PII or real customer data.
Sensitive configuration uses parameter names only, never values. Use sanitized
public evidence and preserve existing protections. Maintain journal.md and keep
spec.md/INDEX.md status and updated synchronized. Retain closed history.
