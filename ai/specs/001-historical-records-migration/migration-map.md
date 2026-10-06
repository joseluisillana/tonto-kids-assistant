# Historical migration map and execution coverage — 2026-10-06

Baseline: 818e88e after PR #124. The operator authorized execution after reviewing
the local-only scope. All listed relocation destinations are now implemented:
28 historical specs, one local issue and 64 source documents, in batches A–E.
IDs are allocated and registered; 001 in ai/specs/ is the migration spec itself.
Original pre-migration review notes below remain planning evidence; current
supported states/dates and source hashes are in [metadata-review.md](metadata-review.md).

## Inventory boundary and provenance

Inventory covers 33 legacy Markdown artifacts under specs/ (excluding AGENTS.md),
28 plan files, one local issue document, eight global journal documents, five
visual assets, related documentation and the reference inventory of 48 GitHub issues returned by
`gh issue list --state all --limit 300` on 2026-10-06. There are 44 closed and four
open remote issues. The result is below the fetch limit; IDs have intentional gaps
because GitHub PRs share its sequence. These remote issues are consulted for
references and evidence only; they will not become local records.

The fetched issue body/metadata snapshot is temporary, not a new canonical store.
Read relevant comments/PRs on GitHub only when needed to verify local record
associations or evidence. Their history remains on GitHub; no full history import
or local issue snapshot is required.
No remote bodies, status or relationships will be changed by migration.

## Definitions: proposed source → destination

28 definitions receive independent spec records; four audio guides and one
migration evidence matrix are auxiliary artifacts listed separately. Each record
will get spec.md, plan.md and journal.md. Existing plans are preserved, missing
prior plans explicitly recorded; never fabricate prior planning.

Final statuses require dated evidence review. A historical heading or a closed
related issue is insufficient on its own. Proposed filenames are not completion
claims. Dates below will use source history, not the migration date as creation.

| source | proposed canonical definition | status decision / evidence to contrast |
| --- | --- | --- |
| `specs/agent-instructions-hierarchy.md` | `ai/specs/002-agent-instructions-hierarchy/spec.md` | Contrast stale local-pending heading with merged #123 / closed #122 (40342ee) |
| `specs/agent-secrets-protection.md` | `ai/specs/003-agent-secrets-protection/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/audio-pipeline-phase-3-web-loop.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/audio-pipeline.md` | `ai/specs/005-audio-pipeline/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/ci-local-cache-alignment.md` | `ai/specs/006-ci-local-cache-alignment/spec.md` | Do not claim done: approved but unimplemented legacy proposal, superseded by Linux/Docker; #89 closed |
| `specs/conversation-loop.md` | `ai/specs/007-conversation-loop/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/docker-cleanup.md` | `ai/specs/008-docker-cleanup/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/inference-provider-devexpert.md` | `ai/specs/009-inference-provider-devexpert/spec.md` | Preserve D025: historical adapter/definition does not reactivate real provider operation |
| `specs/inference-provider-openai.md` | `ai/specs/010-inference-provider-openai/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/inference-providers.md` | `ai/specs/011-inference-providers/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/kivy-ui-docker-emulation.md` | `ai/specs/012-kivy-ui-docker-emulation/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/kivy-ui-testing-coverage.md` | `ai/specs/013-kivy-ui-testing-coverage/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/linux-emulator-audio-device-startup.md` | `ai/specs/014-linux-emulator-audio-device-startup/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/linux-emulator-connection-tts.md` | `ai/specs/015-linux-emulator-connection-tts/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/linux-setup-cache-stability.md` | `ai/specs/016-linux-setup-cache-stability/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/migrate-linux-docker.md` | `ai/specs/017-migrate-linux-docker/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/parallel-agent-workflow.md` | `ai/specs/018-parallel-agent-workflow/spec.md` | Contrast planned heading with implemented common workflow and historical journal |
| `specs/post-migration-stability-validation.md` | `ai/specs/019-post-migration-stability-validation/spec.md` | Contrast accepted #107 scope, merged #108 and final evidence matrix; keep #114/#88 separate |
| `specs/raspberry-listening-indicator.md` | `ai/specs/020-raspberry-listening-indicator/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/raspberry-touch-ui.md` | `ai/specs/021-raspberry-touch-ui/spec.md` | in-progress: #81/#88 remain open; final physical touch/kiosk acceptance pending |
| `specs/release-v1.0.0.md` | `ai/specs/022-release-v1.0.0/spec.md` | Publication gate still future tense: verify tag/release and CI, not preparation alone |
| `specs/web-dependency-audit-remediation.md` | `ai/specs/023-web-dependency-audit-remediation/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/web-listening-indicator.md` | `ai/specs/024-web-listening-indicator/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/web-validation-client.md` | `ai/specs/025-web-validation-client/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/week-04-demo-stability.md` | `ai/specs/026-week-04-demo-stability/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/week-05-agent-capability-pack.md` | `ai/specs/027-week-05-agent-capability-pack/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/week-05-demo-stability.md` | `ai/specs/028-week-05-demo-stability/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |
| `specs/week-06-closeout.md` | `ai/specs/029-week-06-closeout/spec.md` | Contrast definition, paired plan, dated milestone journal and related GitHub evidence |

## Guides and evidence artifacts

Keep each artifact once, with its original content and provenance. Link shared
consumers to that destination; retain navigable legacy references.

| source | proposed destination | role |
| --- | --- | --- |
| `specs/audio-pipeline-phase-2a-validation-guide.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2a-validation-guide.md` | Historical validation guide and recorded acceptance |
| `specs/audio-pipeline-phase-2b-tts-revalidation.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2b-tts-revalidation.md` | Historical validation guide and recorded acceptance |
| `specs/audio-pipeline-phase-2b-validation-guide.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2b-validation-guide.md` | Historical validation guide and recorded acceptance |
| `specs/audio-pipeline-phase-3-browser-manual-validation.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/artifacts/audio-pipeline-phase-3-browser-manual-validation.md` | Historical validation guide and recorded acceptance |
| `specs/migrate-linux-docker-validation.md` | `ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md` | Historical execution/evidence matrix |

## Plans and implementation prompts

Existing prompts stay with their original plans. Main paired plans become plan.md;
additional execution/validation handoffs remain distinguishable artifacts. A shared
plan has one canonical owner and references from other records.

| source | proposed destination / treatment |
| --- | --- |
| `docs/plans/TEMPLATE-spec-implementation-plan.md` | Retired without a copy; recover original via baseline Git, use only current ai/ templates |
| `docs/plans/agent-instructions-hierarchy-implementation-plan.md` | `ai/specs/002-agent-instructions-hierarchy/plan.md` |
| `docs/plans/agent-secrets-protection-implementation-plan.md` | `ai/specs/003-agent-secrets-protection/plan.md` |
| `docs/plans/ai-process-instrumentation-plan.md` | ai/specs/001-historical-records-migration/artifacts/ai-process-instrumentation-plan.md; historical PR #124 evidence |
| `docs/plans/ci-local-cache-alignment-implementation-plan.md` | `ai/specs/006-ci-local-cache-alignment/plan.md` |
| `docs/plans/docker-cleanup-implementation-plan.md` | `ai/specs/008-docker-cleanup/plan.md` |
| `docs/plans/inference-providers.md` | `ai/specs/011-inference-providers/plan.md` |
| `docs/plans/kivy-ui-docker-emulation-plan.md` | `ai/specs/012-kivy-ui-docker-emulation/plan.md` |
| `docs/plans/kivy-ui-testing-coverage-plan.md` | `ai/specs/013-kivy-ui-testing-coverage/plan.md` |
| `docs/plans/linux-emulator-audio-device-startup-implementation-plan.md` | `ai/specs/014-linux-emulator-audio-device-startup/plan.md` |
| `docs/plans/linux-emulator-connection-tts-implementation-plan.md` | `ai/specs/015-linux-emulator-connection-tts/plan.md` |
| `docs/plans/linux-setup-cache-stability-implementation-plan.md` | `ai/specs/016-linux-setup-cache-stability/plan.md` |
| `docs/plans/migrate-linux-docker.md` | `ai/specs/017-migrate-linux-docker/plan.md` |
| `docs/plans/parallel-agent-workflow.md` | `ai/specs/018-parallel-agent-workflow/plan.md` |
| `docs/plans/post-migration-stability-validation-implementation-plan.md` | `ai/specs/019-post-migration-stability-validation/plan.md` |
| `docs/plans/raspberry-listening-indicator.md` | `ai/specs/020-raspberry-listening-indicator/plan.md` |
| `docs/plans/raspberry-touch-ui-implementation-plan.md` | `ai/specs/021-raspberry-touch-ui/plan.md` |
| `docs/plans/release-v1.0.0-implementation-plan.md` | `ai/specs/022-release-v1.0.0/plan.md` |
| `docs/plans/web-dependency-audit-remediation-implementation-plan.md` | `ai/specs/023-web-dependency-audit-remediation/plan.md` |
| `docs/plans/web-listening-indicator.md` | `ai/specs/024-web-listening-indicator/plan.md` |
| `docs/plans/web-text-chat-spoken-response.md` | `ai/specs/025-web-validation-client/artifacts/text-speech-plan.md` |
| `docs/plans/week-03-phase-2b-opencode.md` | `ai/specs/005-audio-pipeline/plan.md` |
| `docs/plans/week-03-phase-3-browser-manual-validation.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/artifacts/browser-validation-plan.md` |
| `docs/plans/week-03-phase-3-web-loop.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/plan.md` |
| `docs/plans/week-04-demo-stability.md` | `ai/specs/026-week-04-demo-stability/plan.md` |
| `docs/plans/week-05-agent-capability-pack.md` | `ai/specs/027-week-05-agent-capability-pack/plan.md` |
| `docs/plans/week-05-demo-stability.md` | `ai/specs/028-week-05-demo-stability/plan.md` |
| `docs/plans/week-06-closeout.md` | `ai/specs/029-week-06-closeout/plan.md` |

## Shared journals

Keep all eight documents canonical at their current locations. Record journals
will link dated sections and may contain attributed extracts; never present a
migration summary as a historical agent's original journal.

| shared source | consumers / treatment |
| --- | --- |
| `docs/project-journal/post-mvp-touch-ui.md` | Touch, Kivy, Linux migration, secrets, release and agent workflow records |
| `docs/project-journal/week-01-closeout.md` | Related weekly specs/issues and milestone context; identify dated sections per record |
| `docs/project-journal/week-01.md` | Related weekly specs/issues and milestone context; identify dated sections per record |
| `docs/project-journal/week-02-closeout.md` | Related weekly specs/issues and milestone context; identify dated sections per record |
| `docs/project-journal/week-03.md` | Related weekly specs/issues and milestone context; identify dated sections per record |
| `docs/project-journal/week-04.md` | Related weekly specs/issues and milestone context; identify dated sections per record |
| `docs/project-journal/week-05.md` | Related weekly specs/issues and milestone context; identify dated sections per record |
| `docs/project-journal/week-06.md` | Related weekly specs/issues and milestone context; identify dated sections per record |

## Related documentation and visual assets

Shared architecture, decisions, roadmap, runbooks, setup, reports and research
remain canonical in docs/. These are linked assets, not additional specs to invent.
Single-work-item design/backlog documents can move as auxiliary artifacts where
listed. Original paths need transition links when moved.

| source | destination / treatment |
| --- | --- |
| `docs/AGENTS.md` | Retain local instructions; explicit authorized process governs new/migrated placement |
| `docs/README.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/agent-secrets-credential-options.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-credential-options.md` (preserve draft/alternative status) |
| `docs/agent-secrets-isolation-design.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-isolation-design.md` (preserve draft/alternative status) |
| `docs/agent-secrets-protection-draft.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-protection-draft.md` (preserve draft/alternative status) |
| `docs/ai-assisted-workflow.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/architecture.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/assets/ui_concept_error.png` | Keep visual asset at original path; repair link from migrated raspberry-touch-ui definition |
| `docs/assets/ui_concept_idle.png` | Keep visual asset at original path; repair link from migrated raspberry-touch-ui definition |
| `docs/assets/ui_concept_listening.png` | Keep visual asset at original path; repair link from migrated raspberry-touch-ui definition |
| `docs/assets/ui_concept_speaking.png` | Keep visual asset at original path; repair link from migrated raspberry-touch-ui definition |
| `docs/assets/ui_concept_thinking.png` | Keep visual asset at original path; repair link from migrated raspberry-touch-ui definition |
| `docs/decisions.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/demo-checklist.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/demo-runbook.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/documentation-workflow.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/final-report-outline.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/final-report.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/future-work.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/hardware.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/known-limitations.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/project-genesis.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/raspberry-pi-setup.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/releases/v1.0.0.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/research/notebooklm.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/roadmap.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/specs.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/vision.md` | Keep canonical shared source; link relevant records and repair references after relocation |
| `docs/web-dependency-audit-triage.md` | `ai/specs/023-web-dependency-audit-remediation/artifacts/web-dependency-audit-triage.md` |

`specs/AGENTS.md` remains an instruction entry, not a spec to import.
`docs/issues/emulator-system-volume-delay.md` is an existing repository issue
definition. Its proposed destination is `ai/issues/001-emulator-system-volume-delay/`
with issue.md, plan.md and journal.md, preserving source provenance and the full
GitHub #114 URL in related. This migrates the local document, not GitHub #114;
its remote definition, comments and lifecycle remain managed on GitHub.

## GitHub references for migrated local records

The operator's 2026-10-06 clarification supersedes the initial proposal to
allocate 48 local mirrors. No GitHub issue receives a local ID or lifecycle
as part of this migration. Only existing repository records relocate.
Each migrated spec/local issue must retain the corresponding full issue URLs
in related. Verify associations against source definitions, plans, journals and
GitHub bodies; distinguish tracking issues, phase issues and incidental context.
For records with no documented issue, state that explicitly rather than inventing one.

## Local record → corresponding GitHub tracking references

Carry these URLs into related when each local record is migrated. Associations
come from local definitions/plans, docs/specs.md and the read-only issue body
inventory. Phase-specific relationships keep their scope; they do not make a
phase issue the tracker of an entire broad definition. Retain contextual issue
and PR references in the historical text without misclassifying them as tracking.

| local source | GitHub URLs to preserve | relationship / review note |
| --- | --- | --- |
| `specs/agent-instructions-hierarchy.md` | [#122](https://github.com/joseluisillana/tonto-kids-assistant/issues/122) | Preserve tracking/phase scope from source and linked evidence |
| `specs/agent-secrets-protection.md` | [#110](https://github.com/joseluisillana/tonto-kids-assistant/issues/110) | Preserve tracking/phase scope from source and linked evidence |
| `specs/audio-pipeline-phase-3-web-loop.md` | No corresponding issue identified in reviewed sources; do not invent one | Preserve tracking/phase scope from source and linked evidence |
| `specs/audio-pipeline.md` | No corresponding issue identified in reviewed sources; do not invent one | Preserve tracking/phase scope from source and linked evidence |
| `specs/ci-local-cache-alignment.md` | [#89](https://github.com/joseluisillana/tonto-kids-assistant/issues/89) | Preserve tracking/phase scope from source and linked evidence |
| `specs/conversation-loop.md` | No corresponding issue identified in reviewed sources; do not invent one | Preserve tracking/phase scope from source and linked evidence |
| `specs/docker-cleanup.md` | [#107](https://github.com/joseluisillana/tonto-kids-assistant/issues/107), [#110](https://github.com/joseluisillana/tonto-kids-assistant/issues/110) | Post-migration cleanup #107; secret-safe diagnostic follow-up #110 |
| `specs/inference-provider-devexpert.md` | [#48](https://github.com/joseluisillana/tonto-kids-assistant/issues/48), [#51](https://github.com/joseluisillana/tonto-kids-assistant/issues/51), [#49](https://github.com/joseluisillana/tonto-kids-assistant/issues/49) | Parent #48 plus shared chat/STT phases; no separate issue for this provider definition |
| `specs/inference-provider-openai.md` | [#48](https://github.com/joseluisillana/tonto-kids-assistant/issues/48), [#51](https://github.com/joseluisillana/tonto-kids-assistant/issues/51), [#49](https://github.com/joseluisillana/tonto-kids-assistant/issues/49) | Parent #48 plus shared chat/STT phases; no separate issue for this provider definition |
| `specs/inference-providers.md` | [#48](https://github.com/joseluisillana/tonto-kids-assistant/issues/48), [#50](https://github.com/joseluisillana/tonto-kids-assistant/issues/50), [#51](https://github.com/joseluisillana/tonto-kids-assistant/issues/51), [#49](https://github.com/joseluisillana/tonto-kids-assistant/issues/49), [#52](https://github.com/joseluisillana/tonto-kids-assistant/issues/52) | Preserve tracking/phase scope from source and linked evidence |
| `specs/kivy-ui-docker-emulation.md` | No corresponding issue identified in reviewed sources; do not invent one | Preserve tracking/phase scope from source and linked evidence |
| `specs/kivy-ui-testing-coverage.md` | [#105](https://github.com/joseluisillana/tonto-kids-assistant/issues/105), [#81](https://github.com/joseluisillana/tonto-kids-assistant/issues/81) | Preserve tracking/phase scope from source and linked evidence |
| `specs/linux-emulator-audio-device-startup.md` | [#107](https://github.com/joseluisillana/tonto-kids-assistant/issues/107) | Preserve tracking/phase scope from source and linked evidence |
| `specs/linux-emulator-connection-tts.md` | [#107](https://github.com/joseluisillana/tonto-kids-assistant/issues/107) | Preserve tracking/phase scope from source and linked evidence |
| `specs/linux-setup-cache-stability.md` | [#107](https://github.com/joseluisillana/tonto-kids-assistant/issues/107) | Preserve tracking/phase scope from source and linked evidence |
| `specs/migrate-linux-docker.md` | [#95](https://github.com/joseluisillana/tonto-kids-assistant/issues/95) | Preserve tracking/phase scope from source and linked evidence |
| `specs/parallel-agent-workflow.md` | No corresponding issue identified in reviewed sources; do not invent one | Preserve tracking/phase scope from source and linked evidence |
| `specs/post-migration-stability-validation.md` | [#107](https://github.com/joseluisillana/tonto-kids-assistant/issues/107) | Preserve tracking/phase scope from source and linked evidence |
| `specs/raspberry-listening-indicator.md` | [#18](https://github.com/joseluisillana/tonto-kids-assistant/issues/18), [#20](https://github.com/joseluisillana/tonto-kids-assistant/issues/20), [#27](https://github.com/joseluisillana/tonto-kids-assistant/issues/27) | Preserve tracking/phase scope from source and linked evidence |
| `specs/raspberry-touch-ui.md` | [#81](https://github.com/joseluisillana/tonto-kids-assistant/issues/81), [#82](https://github.com/joseluisillana/tonto-kids-assistant/issues/82), [#83](https://github.com/joseluisillana/tonto-kids-assistant/issues/83), [#84](https://github.com/joseluisillana/tonto-kids-assistant/issues/84), [#85](https://github.com/joseluisillana/tonto-kids-assistant/issues/85), [#86](https://github.com/joseluisillana/tonto-kids-assistant/issues/86), [#87](https://github.com/joseluisillana/tonto-kids-assistant/issues/87), [#88](https://github.com/joseluisillana/tonto-kids-assistant/issues/88) | Preserve tracking/phase scope from source and linked evidence |
| `specs/release-v1.0.0.md` | No corresponding issue identified in reviewed sources; do not invent one | Publication is linked by PR/tag evidence, not a dedicated issue found so far |
| `specs/web-dependency-audit-remediation.md` | [#107](https://github.com/joseluisillana/tonto-kids-assistant/issues/107) | Preserve tracking/phase scope from source and linked evidence |
| `specs/web-listening-indicator.md` | [#18](https://github.com/joseluisillana/tonto-kids-assistant/issues/18), [#19](https://github.com/joseluisillana/tonto-kids-assistant/issues/19), [#23](https://github.com/joseluisillana/tonto-kids-assistant/issues/23), [#25](https://github.com/joseluisillana/tonto-kids-assistant/issues/25) | Preserve tracking/phase scope from source and linked evidence |
| `specs/web-validation-client.md` | No corresponding issue identified in reviewed sources; do not invent one | Preserve tracking/phase scope from source and linked evidence |
| `specs/week-04-demo-stability.md` | [#18](https://github.com/joseluisillana/tonto-kids-assistant/issues/18), [#19](https://github.com/joseluisillana/tonto-kids-assistant/issues/19), [#20](https://github.com/joseluisillana/tonto-kids-assistant/issues/20), [#23](https://github.com/joseluisillana/tonto-kids-assistant/issues/23), [#25](https://github.com/joseluisillana/tonto-kids-assistant/issues/25), [#27](https://github.com/joseluisillana/tonto-kids-assistant/issues/27) | Phase 4 tracking only; not an umbrella tracker for the entire Week 04 spec |
| `specs/week-05-agent-capability-pack.md` | [#43](https://github.com/joseluisillana/tonto-kids-assistant/issues/43) | Preserve tracking/phase scope from source and linked evidence |
| `specs/week-05-demo-stability.md` | [#33](https://github.com/joseluisillana/tonto-kids-assistant/issues/33), [#34](https://github.com/joseluisillana/tonto-kids-assistant/issues/34), [#35](https://github.com/joseluisillana/tonto-kids-assistant/issues/35), [#36](https://github.com/joseluisillana/tonto-kids-assistant/issues/36), [#37](https://github.com/joseluisillana/tonto-kids-assistant/issues/37), [#38](https://github.com/joseluisillana/tonto-kids-assistant/issues/38) | Preserve tracking/phase scope from source and linked evidence |
| `specs/week-06-closeout.md` | [#65](https://github.com/joseluisillana/tonto-kids-assistant/issues/65), [#66](https://github.com/joseluisillana/tonto-kids-assistant/issues/66), [#67](https://github.com/joseluisillana/tonto-kids-assistant/issues/67), [#68](https://github.com/joseluisillana/tonto-kids-assistant/issues/68), [#69](https://github.com/joseluisillana/tonto-kids-assistant/issues/69), [#70](https://github.com/joseluisillana/tonto-kids-assistant/issues/70), [#71](https://github.com/joseluisillana/tonto-kids-assistant/issues/71) | Preserve tracking/phase scope from source and linked evidence |
| `docs/issues/emulator-system-volume-delay.md` | [#114](https://github.com/joseluisillana/tonto-kids-assistant/issues/114) | Existing local definition; preserve #107 as contextual validation reference |

## Known relationships and decisions to preserve

- #18 → #19/#20/#23/#25/#27; Raspberry/browser indicator implementation and validation.
- #33 → #34–#38; Week 05 parent remains distinct from its execution phases.
- #48 → #50/#51/#49/#52; #53 is future backlog linked to that completed initial scope.
- #65 → #66–#71; Week 06 closeout and presentation evidence.
- #81 → #82–#88 and #105 coverage; parent cannot close while #88 remains pending.
- #107 → migration problems/repairs and deferred #114; preserve operator-approved
  scope exclusion explaining why #107 closed with #114 still pending.
- #110 → original draft and later reduced authorized scope, PRs #116–#120;
  closure covers accidental exposure reduction, not universal isolation.
- #122 → hierarchy definition/plan, integrated by #123; supersedes stale local-only
  status in preserved source text without erasing that original evidence.
- PR #124 / 818e88e instruments the process; it is not a historical GitHub issue.

Verify these relationships against issue bodies/comments and preserve additional
relations discovered there. Historical GitHub links to old repository paths need
local transition documents; migration must not edit remote historical bodies.

## Status/date and preservation review before relocation

- Obtain creation/last substantive dates from Git history and source text; preserve
  dates of existing local issue documents and separate the migration date. GitHub
  timestamps remain remote evidence; do not import the remote lifecycle.
- Record unknown ownership/authorship explicitly; do not name a historical agent
  based only on today's migration tool.
- Contrast headers with newest dated journals, merged PRs and relevant decisions.
  Flag CI legacy proposal, hierarchy, parallel workflow and release publication
  specifically; do not silently turn abandoned scope into done.
- Keep OpenAI/DevExpert adapter history without running providers or restoring
  deprecated tooling. D025 and Linux/Docker remain governing decisions.
- Reference shared plans for provider definitions and broad audio work; if no
  prior plan exists, label the record plan as a retrospective provenance/handoff
  document and link any original execution instructions.
- Preserve original contents in migrated definitions/artifacts with labelled
  metadata/provenance sections. Do not broadly rewrite contracts to fit a template.
- Validate all old/new relative links and compare contents with baseline before
  replacing sources with redirects. Map each existing local issue document once; verify its corresponding GitHub
  URL without copying the remote definition, lifecycle or comment history.

Execution has relocated all mapped local records with required trios, indexes,
canonical plans/artifacts and navigable legacy heading pointers. The issue index
contains only the one pre-existing repository issue, not GitHub mirrors. Shared
documents/images stay canonical at their original paths. Final review/integration
status is tracked by this migration spec and its journal.
