# Historical records migration — execution plan

## Objective and source record

Implement [spec.md](spec.md), using [migration-map.md](migration-map.md) as the
source/destination and GitHub-reference matrix. Read [journal.md](journal.md),
root AGENTS.md, common workflow and relevant local instructions before acting.

Inventory and mapping are prepared. This plan defines the remaining migration;
it does not authorize implementation of historical product backlog. The operator
requested planning first, then explicitly requested implementation (see journal).
Execute within that authorization, without asking again for decisions already made.
The operator now adds final retirement of the old structure. Temporary transition
paths used during batches A–E do not form the final accepted layout. Stage 4 below
reports link impact and waits for the operator's external-reference decision;
this scope/plan extension does not itself delete files or edit remote messages.

## Included and excluded scope

Migrate 28 existing spec definitions and one existing local issue document,
with five validation/evidence artifacts, their mapped plans/prompts and relevant
auxiliary design/backlog docs. Preserve references to eight shared journals and
five existing visual assets, and repair affected consumers and old paths.
The current map covers 33 specs/ artifacts and 28 docs/plans/ files; two plan
files were retained during migration. Preserve those files and ai/specs/AGENTS.md
at the proposed ai/ destinations in cleanup-impact.md before final retirement.
Reconcile counts against actual source/index state before assigning IDs.

GitHub issues remain defined, operated and retained in GitHub. Consult relevant
bodies/comments/PRs only to verify associations and evidence. Preserve full
corresponding issue URLs in each migrated local record's `related`. No remote
issue import, local mirrors or remote lifecycle synchronization. Remote link-only
corrections are conditional on specific operator authorization after the impact
report; issue statuses and historical checklists remain outside scope.
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
7. During these migration batches, retain legacy paths and heading fragments as
   temporary transition pointers. Final removal is stage 4, after content and
   external-reference decisions; do not interpret these pointers as permanent.
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
  visual assets at their shared canonical locations. Relocate
  phase-1 instrumentation evidence into this spec's artifacts at
  stage 4. Recover the retired old template through Git; no legacy template copy.
- Inspect Markdown references in component instructions and operational skills
  without rewriting their architecture/operating rules. Repair only links made
  stale by this migration. Retained transition pointers support external consumers.
- Revise ai/ transition notes to describe actual coverage and unresolved exceptions.
  Do not claim a full GitHub inventory is contained in the local issue index.
- Document the unchanged exporter limitation: ai/ is not selected. Do not modify
  scripts, regenerate source copies as a workaround or claim export completeness.

Gate: every local source has one canonical owner, consumers resolve to that owner,
and remaining transition pointers do not contain competing editable definitions.

### 4. Retire legacy structure with preservation and link-impact decision

#### 4.1 Prepare a concrete deletion and impact manifest

- Use cleanup-impact.md: 64 migrated transition documents plus three remaining
  structural files (67 candidates). Verify the list against the source ledger and
  current tree; do not recursively delete directories or unknown files.
- Distinguish active file links/YAML related entries from attributed historical
  path mentions. Scan local docs/instructions, scripts/tests and public GitHub
  bodies/comments/reviews. Record scan boundaries and unknown external bookmarks.
- Report each main-branch URL that would fail, its source, impact and canonical
  or immutable replacement. Fixed-SHA links and PR diffs preserve Git history.
- Current report: six affected main URLs in #81 (four, active) and #89 (two,
  closed); two fixed-SHA links stay valid. #114 retains two plain source paths
  used for manual navigation, requiring separate operator consideration.
- Two local Markdown links and 29 related source entries can be repaired within
  this change. Review 325 literal old-path lines as history versus live guidance;
  do not erase provenance to make a search count zero.

Gate: present the impact report and record the operator's chosen treatment.
Do not remove affected files or edit remote issue/comment bodies before that
decision. Migration authorization does not select a link-breakage policy.

#### 4.2 Preserve remaining unique information and repair references

- Move the former spec instructions to ai/specs/AGENTS.md with correct ancestors,
  scope/navigation and mandatory current planning rules. Preserve all operating,
  acceptance and safety rules; reconcile obsolete placement guidance explicitly.
- Retire the old template without a legacy copy or operational references,
  preserving its hash and immutable Git recovery location. Use only current ai/ templates.
  Preserve ai/specs/001-historical-records-migration/artifacts/ai-process-instrumentation-plan.md as phase-1
  evidence in this spec's artifacts. No additional spec/issue records are needed.
- Extend the hash/provenance ledger to all three sources. Verify existing bodies,
  assets/trios against the original 64-source ledger, including the documented
  narrow path/whitespace normalization, before retiring any aliases.
- Update active local references to canonical targets. Replace deleted-source
  related provenance with full immutable URLs under original baseline
  818e88eacbac3989c091d1294c92e26ebeb663f7, preserving original fragments.
- Apply only specifically authorized external corrections, or record explicitly
  accepted external failures and recovery URLs. Keep GitHub issues remote and
  do not change their state/checklists or mirror their content.
- Preserve literal historical paths only as attributed evidence with canonical/
  immutable lookup. Shared journals/images/context remain at their sources.

Gate: all 67 sources have preserved information, all internal active references
resolve, and each known external effect has an explicit approved treatment.

#### 4.3 Remove verified files and validate final layout

- Remove only the enumerated tracked legacy candidates. specs/, docs/plans/ and
  docs/issues/ disappear from the tracked tree, along with the four standalone
  legacy artifact aliases under docs/. Remove working directories only if empty;
  leave unrelated/untracked content untouched and report it.
- Keep docs/specs.md as milestone/overview context, not a duplicate registry.
  Update root/common/local navigation and ai/ notes; no compatibility files or
  competing legacy source-of-truth for migrated records remain at final acceptance.
- Rescan files/images/headings, related entries and live operating references;
  compare retained information/criteria/prompts with immutable history and hashes.
- Check the unchanged exporter in an isolated public-doc fixture without specs/.
  It currently succeeds in that scenario but still excludes ai/ and loses the old
  exported transition pointers. Report this limit without expanding script scope
  or claiming canonical export coverage; changing coverage needs a separate decision.
- Record removed files, preserved remaining artifacts, corrected/accepted broken
  links and recovery references in journals and PR evidence.

Gate: no information loss, no internal dangling references, no tracked legacy
structure, and external effects handled according to the recorded operator choice.

### 5. Final review, evidence and integration

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
Retirement relocates instructions and phase-1 evidence, retains the old template
only in Git,
removes four standalone aliases under docs/, and fixes provenance/navigation.
Read-only cleanup-impact.md contains the exact list and external decision boundary.
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
- Links: check canonical relative paths, images, heading fragments, shared-plan
  consumers and full GitHub URLs. At final retirement, legacy paths must not be
  internal link/related targets. Confirm issue identity and source association;
  external failures require an explicit operator treatment from the impact report.
- Retirement: verify 67 sources against preservation evidence, preserving the
  three remaining structural files first. Assert no tracked legacy directories/
  aliases, no deleted canonical data and no history rewrite.
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
Those batches are now implemented. Extend execution through retirement stage 4:
present cleanup-impact.md, record the operator's link-treatment choice, preserve
all 67 source files' information, then remove only the verified legacy candidates.
Migrate only repository-defined records; GitHub issues stay in GitHub and local
records retain verified full tracking URLs in related. Preserve original content,
language, dates, authorship, evidence, plans/prompts and shared ownership; label
retrospective plans and unknowns. Legacy navigation pointers are temporary, not
the final layout. Repair local references and use immutable Git provenance before
retirement; remote reference edits require specific authorization from the report.
Update indexes/consumers and do not change product scope or operate providers/hardware.
Run the checks above, record real results/exceptions, and prepare reviewable PR(s).
Do not mark done or close a remote issue merely because files were relocated.

## Safety and record maintenance

No secrets, credentials, tokens, connection strings, PII or real customer data.
Sensitive configuration uses parameter names only, never values. Use sanitized
public evidence and preserve existing protections. Maintain journal.md and keep
spec.md/INDEX.md status and updated synchronized. Retain closed history.

## Operator decisions for retirement

The operator authorized correcting GitHub references in #81, #89 and #114.
Those corrections preserve issue state, title and all other body content.
The operator subsequently required current ai/ procedure, rules and templates
exclusively: remove old template usage references and retain no legacy template copy.
Its original bytes remain recoverable at the recorded Git baseline.
