# Legacy structure retirement — link impact and decision

Prepared 2026-10-06 against PR #125 head b2cee31. No legacy file is deleted by
this scope/plan extension. Counts describe the impact **if the listed paths are
removed from the current branch/main**, not broken links today. The previous
redirect-preservation policy is superseded by the requested retirement, subject
to the operator's decision on the concrete external links below.

## Proposed retirement and preservation boundary

Remove 64 migrated transition documents, plus the three remaining structural
files after preserving their unique information. This eliminates specs/,
docs/plans/ and docs/issues/ from the tracked tree and removes four standalone
legacy artifact aliases under docs/. No recursive deletion of untracked files.
The following three files still contain information and cannot simply be deleted:

| remaining source | proposed destination before removal | purpose |
| --- | --- | --- |
| `specs/AGENTS.md` | `ai/specs/AGENTS.md` | Preserve local contract/validation instructions; adjust relative paths and obsolete placement references. |
| `docs/plans/TEMPLATE-spec-implementation-plan.md` | `ai/specs/001-historical-records-migration/artifacts/legacy-spec-implementation-plan-template.md` | Keep the original template as historical evidence; ai/ templates remain the active process. |
| `docs/plans/ai-process-instrumentation-plan.md` | `ai/specs/001-historical-records-migration/artifacts/ai-process-instrumentation-plan.md` | Preserve phase-1 plan and evidence without keeping the old plans directory. |

Shared project journals, images, architecture, decisions, runbooks and docs/specs.md
remain in place: they are milestone/context sources, not legacy copies to delete.
Literal old path names may remain as explicitly historical provenance; they must
not be active local links or dependencies. Source retrieval uses immutable Git
URLs, not deleted-path references in related.

## Checked evidence and limits

Read-only inventory: 48 issue bodies, 77 PR bodies, 29 repository discussion
comments, zero inline review comments and zero review-body texts (all 77 PRs
checked, no truncated review pages). Issue definitions/states/history remain
managed in GitHub; no local mirrors and no messages or bodies edited.
Unknown external bookmarks, other repos, chat history and downloaded exports
are outside this searchable inventory and may retain old main URLs. GitHub has
no redirect mechanism for removed repository file paths; retaining Git history
preserves information but does not make an old main URL resolve automatically.

## Local references — repairable before deletion

- 2 actual local Markdown links target a retirement candidate.
- 29 related entries target an old source path; convert provenance
  entries to immutable baseline URLs rather than deleting provenance.
- 325 remaining-document lines mention a retiring path; review
  live instructions separately from historical source tables/ledger descriptions.
  A literal historical code path is not automatically a clickable broken link.

| consumer | old target | treatment |
| --- | --- | --- |
| `AGENTS.md:80` | `specs/AGENTS.md` | Update to `ai/specs/AGENTS.md` before removal |
| `docs/AGENTS.md:14` | `specs/AGENTS.md` | Update to `ai/specs/AGENTS.md` before removal |

Local acceptance requires zero dangling file/heading links and zero related
entries to deleted local sources. Historical provenance links use:
`https://github.com/joseluisillana/tonto-kids-assistant/blob/818e88eacbac3989c091d1294c92e26ebeb663f7/<old-path>`
with the original fragment if present. Verify original Git objects and the 64-source
hash ledger; extend the ledger for the three structural files before removal.

## Concrete external URLs that would break

6 explicit main-branch URLs in 2 GitHub issue/PR/comment
bodies target retiring files. These currently work and would stop resolving
after cleanup is merged. The issue pages themselves, their history and current
GitHub tracking URLs in local records remain unaffected.

| location | current link | impact | canonical replacement |
| --- | --- | --- | --- |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/89) — CLOSED | [old file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/specs/ci-local-cache-alignment.md) | Closed historical work loses a supporting definition/plan link (historical navigation impact) | [canonical file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/ai/specs/006-ci-local-cache-alignment/spec.md) |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/89) — CLOSED | [old file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/docs/plans/ci-local-cache-alignment-implementation-plan.md) | Closed historical work loses a supporting definition/plan link (historical navigation impact) | [canonical file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/ai/specs/006-ci-local-cache-alignment/plan.md) |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/81) — OPEN | [old file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/specs/raspberry-touch-ui.md) | Active work loses direct access to its definition or plan (high navigation impact) | [canonical file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/ai/specs/021-raspberry-touch-ui/spec.md) |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/81) — OPEN | [old file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/docs/plans/raspberry-touch-ui-implementation-plan.md) | Active work loses direct access to its definition or plan (high navigation impact) | [canonical file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/ai/specs/021-raspberry-touch-ui/plan.md) |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/81) — OPEN | [old file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/specs/kivy-ui-testing-coverage.md) | Active work loses direct access to its definition or plan (high navigation impact) | [canonical file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/ai/specs/013-kivy-ui-testing-coverage/spec.md) |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/81) — OPEN | [old file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/docs/plans/kivy-ui-testing-coverage-plan.md) | Active work loses direct access to its definition or plan (high navigation impact) | [canonical file](https://github.com/joseluisillana/tonto-kids-assistant/blob/main/ai/specs/013-kivy-ui-testing-coverage/plan.md) |

2 checked explicit links to retiring paths use a fixed Git commit;
they remain accessible if their referenced commit remains in Git history.
GitHub's historical PR diffs/tree paths are commit-based and are not deleted
by cleanup; they must not be mistaken for broken main-branch document links.

## Plain historical paths in GitHub

37 fetched bodies/comments contain at least one retiring path
(explicit links included). For plain code/text paths, the impact is outdated
manual navigation or an old handoff command, not necessarily a clickable URL
failure. Do not rewrite all historical narratives or checklist states automatically.

| GitHub location | referenced old paths | treatment to decide |
| --- | --- | --- |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/122) — CLOSED | `docs/plans/agent-instructions-hierarchy-implementation-plan.md`, `specs/agent-instructions-hierarchy.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/114) — OPEN | `docs/issues/emulator-system-volume-delay.md`, `specs/migrate-linux-docker-validation.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/107) — CLOSED | `specs/migrate-linux-docker-validation.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/105) — CLOSED | `docs/plans/kivy-ui-testing-coverage-plan.md`, `specs/kivy-ui-testing-coverage.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/89) — CLOSED | `docs/plans/ci-local-cache-alignment-implementation-plan.md`, `specs/ci-local-cache-alignment.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/81) — OPEN | `docs/plans/kivy-ui-testing-coverage-plan.md`, `docs/plans/raspberry-touch-ui-implementation-plan.md`, `specs/kivy-ui-testing-coverage.md`, `specs/raspberry-touch-ui.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/66) — CLOSED | `docs/plans/week-06-closeout.md`, `specs/week-06-closeout.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/65) — CLOSED | `docs/plans/week-06-closeout.md`, `specs/week-06-closeout.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/48) — CLOSED | `docs/plans/inference-providers.md`, `specs/inference-provider-devexpert.md`, `specs/inference-provider-openai.md`, `specs/inference-providers.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/38) — CLOSED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/37) — CLOSED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/36) — CLOSED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/35) — CLOSED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/34) — CLOSED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/33) — CLOSED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/27) — CLOSED | `docs/plans/raspberry-listening-indicator.md`, `specs/raspberry-listening-indicator.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/23) — CLOSED | `docs/plans/web-listening-indicator.md`, `specs/web-listening-indicator.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/20) — CLOSED | `docs/plans/raspberry-listening-indicator.md`, `specs/raspberry-listening-indicator.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/19) — CLOSED | `docs/plans/web-listening-indicator.md`, `specs/web-listening-indicator.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Issue body](https://github.com/joseluisillana/tonto-kids-assistant/issues/18) — CLOSED | `specs/raspberry-listening-indicator.md`, `specs/web-listening-indicator.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/108) — MERGED | `specs/migrate-linux-docker-validation.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/104) — MERGED | `specs/raspberry-touch-ui.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/102) — MERGED | `specs/migrate-linux-docker-validation.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/72) — MERGED | `docs/plans/week-06-closeout.md`, `specs/week-06-closeout.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/64) — MERGED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/63) — MERGED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/62) — MERGED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/39) — MERGED | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/30) — MERGED | `docs/plans/raspberry-listening-indicator.md`, `docs/plans/week-04-demo-stability.md`, `specs/raspberry-listening-indicator.md`, `specs/week-04-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/13) — MERGED | `docs/plans/week-04-demo-stability.md`, `specs/week-04-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/11) — MERGED | `docs/plans/week-04-demo-stability.md`, `specs/week-04-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [PR body](https://github.com/joseluisillana/tonto-kids-assistant/pull/10) — MERGED | `docs/plans/week-04-demo-stability.md`, `specs/week-04-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Discussion/inline comment](https://github.com/joseluisillana/tonto-kids-assistant/issues/34#issuecomment-4644356180) — historical | `docs/plans/week-05-demo-stability.md`, `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Discussion/inline comment](https://github.com/joseluisillana/tonto-kids-assistant/issues/36#issuecomment-4675919897) — historical | `specs/week-05-demo-stability.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Discussion/inline comment](https://github.com/joseluisillana/tonto-kids-assistant/issues/95#issuecomment-5967622523) — historical | `docs/plans/migrate-linux-docker.md`, `specs/migrate-linux-docker.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Discussion/inline comment](https://github.com/joseluisillana/tonto-kids-assistant/issues/95#issuecomment-5969296569) — historical | `specs/migrate-linux-docker-validation.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |
| [Discussion/inline comment](https://github.com/joseluisillana/tonto-kids-assistant/issues/110#issuecomment-6014685811) — historical | `docs/plans/agent-secrets-protection-implementation-plan.md`, `specs/agent-secrets-protection.md` | Retain as history with immutable recovery map; update explicit live tracking links only if authorized |

## Tooling/export impact

The existing export script checks for docs/specs directories before traversal
and uses nullglob. Removing specs/ does **not** inherently make export fail.
Its legacy specs glob simply becomes empty. It still excludes ai/, so canonical
record content stays outside the NotebookLM export as already documented; cleanup
also removes the exported transition pointers. Retained docs summaries/operating
guides still export. An isolated public-doc fixture without specs/ was executed successfully on
2026-10-06 using the unchanged export script; repeat at the deletion SHA.
No runtime or CI command depends on these old definitions; the export regression
fixtures intentionally create specs/example.md and are not legacy records to purge.
Adding ai/ export coverage is a separate decision because the current spec excludes
export-script changes. Do not broaden the script or its secret-safe selection silently.

## Operator decision required before removing paths

Recommended: preserve originals via immutable baseline links in provenance and
update the six explicit GitHub links listed above and the two manual-navigation
source paths in active #114, with specific operator authorization. No other
issue/PR/comment narrative, checklist or state changes are proposed.
This preserves active #81 navigation and closed #89 evidence without duplicating
issue content, importing remote issues or changing their status. Editing those
remote references needs the operator's explicit authorization; none has been done.
The canonical replacements in the table use main, whose new ai/ files are not
yet available until PR #125 merges. Avoid an intermediate broken-link window:
use the already published canonical snapshot at commit
`b2cee312872f063780f020e03e57719ba4541fc5` before removing old paths. After merge,
active #81/#114 links may point to main for ongoing work; closed #89 evidence
can remain pinned. The chosen timing/targets belong to the operator decision.
Unknown bookmarks still need the published old→new/immutable mapping.

Alternative: leave GitHub bodies immutable and explicitly accept the six main
link failures, using the mapping and baseline snapshots for recovery. This meets
file retirement/content preservation but leaves active #81 navigation degraded
and #114's two plain source references obsolete.

Keeping compatibility files would avoid those failures but conflicts with the
requested complete retirement, so it is not the proposed final structure.
The cleanup remains pending this decision; all migration preservation checks
and external-link identities must be rechecked at the deletion/integration SHA.

## Exact retirement manifest (pending decision, not deleted)

| legacy file to retire | preserved canonical destination | current treatment |
| --- | --- | --- |
| `docs/agent-secrets-credential-options.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-credential-options.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/agent-secrets-isolation-design.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-isolation-design.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/agent-secrets-protection-draft.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-protection-draft.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/issues/emulator-system-volume-delay.md` | `ai/issues/001-emulator-system-volume-delay/issue.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/TEMPLATE-spec-implementation-plan.md` | `ai/specs/001-historical-records-migration/artifacts/legacy-spec-implementation-plan-template.md` | Unique information: must preserve before removal |
| `docs/plans/agent-instructions-hierarchy-implementation-plan.md` | `ai/specs/002-agent-instructions-hierarchy/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/agent-secrets-protection-implementation-plan.md` | `ai/specs/003-agent-secrets-protection/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/ai-process-instrumentation-plan.md` | `ai/specs/001-historical-records-migration/artifacts/ai-process-instrumentation-plan.md` | Unique information: must preserve before removal |
| `docs/plans/ci-local-cache-alignment-implementation-plan.md` | `ai/specs/006-ci-local-cache-alignment/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/docker-cleanup-implementation-plan.md` | `ai/specs/008-docker-cleanup/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/inference-providers.md` | `ai/specs/011-inference-providers/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/kivy-ui-docker-emulation-plan.md` | `ai/specs/012-kivy-ui-docker-emulation/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/kivy-ui-testing-coverage-plan.md` | `ai/specs/013-kivy-ui-testing-coverage/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/linux-emulator-audio-device-startup-implementation-plan.md` | `ai/specs/014-linux-emulator-audio-device-startup/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/linux-emulator-connection-tts-implementation-plan.md` | `ai/specs/015-linux-emulator-connection-tts/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/linux-setup-cache-stability-implementation-plan.md` | `ai/specs/016-linux-setup-cache-stability/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/migrate-linux-docker.md` | `ai/specs/017-migrate-linux-docker/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/parallel-agent-workflow.md` | `ai/specs/018-parallel-agent-workflow/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/post-migration-stability-validation-implementation-plan.md` | `ai/specs/019-post-migration-stability-validation/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/raspberry-listening-indicator.md` | `ai/specs/020-raspberry-listening-indicator/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/raspberry-touch-ui-implementation-plan.md` | `ai/specs/021-raspberry-touch-ui/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/release-v1.0.0-implementation-plan.md` | `ai/specs/022-release-v1.0.0/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/web-dependency-audit-remediation-implementation-plan.md` | `ai/specs/023-web-dependency-audit-remediation/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/web-listening-indicator.md` | `ai/specs/024-web-listening-indicator/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/web-text-chat-spoken-response.md` | `ai/specs/025-web-validation-client/artifacts/text-speech-plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/week-03-phase-2b-opencode.md` | `ai/specs/005-audio-pipeline/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/week-03-phase-3-browser-manual-validation.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/artifacts/browser-validation-plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/week-03-phase-3-web-loop.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/week-04-demo-stability.md` | `ai/specs/026-week-04-demo-stability/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/week-05-agent-capability-pack.md` | `ai/specs/027-week-05-agent-capability-pack/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/week-05-demo-stability.md` | `ai/specs/028-week-05-demo-stability/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/plans/week-06-closeout.md` | `ai/specs/029-week-06-closeout/plan.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `docs/web-dependency-audit-triage.md` | `ai/specs/023-web-dependency-audit-remediation/artifacts/web-dependency-audit-triage.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/AGENTS.md` | `ai/specs/AGENTS.md` | Unique information: must preserve before removal |
| `specs/agent-instructions-hierarchy.md` | `ai/specs/002-agent-instructions-hierarchy/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/agent-secrets-protection.md` | `ai/specs/003-agent-secrets-protection/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/audio-pipeline-phase-2a-validation-guide.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2a-validation-guide.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/audio-pipeline-phase-2b-tts-revalidation.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2b-tts-revalidation.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/audio-pipeline-phase-2b-validation-guide.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2b-validation-guide.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/audio-pipeline-phase-3-browser-manual-validation.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/artifacts/audio-pipeline-phase-3-browser-manual-validation.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/audio-pipeline-phase-3-web-loop.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/audio-pipeline.md` | `ai/specs/005-audio-pipeline/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/ci-local-cache-alignment.md` | `ai/specs/006-ci-local-cache-alignment/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/conversation-loop.md` | `ai/specs/007-conversation-loop/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/docker-cleanup.md` | `ai/specs/008-docker-cleanup/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/inference-provider-devexpert.md` | `ai/specs/009-inference-provider-devexpert/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/inference-provider-openai.md` | `ai/specs/010-inference-provider-openai/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/inference-providers.md` | `ai/specs/011-inference-providers/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/kivy-ui-docker-emulation.md` | `ai/specs/012-kivy-ui-docker-emulation/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/kivy-ui-testing-coverage.md` | `ai/specs/013-kivy-ui-testing-coverage/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/linux-emulator-audio-device-startup.md` | `ai/specs/014-linux-emulator-audio-device-startup/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/linux-emulator-connection-tts.md` | `ai/specs/015-linux-emulator-connection-tts/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/linux-setup-cache-stability.md` | `ai/specs/016-linux-setup-cache-stability/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/migrate-linux-docker-validation.md` | `ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/migrate-linux-docker.md` | `ai/specs/017-migrate-linux-docker/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/parallel-agent-workflow.md` | `ai/specs/018-parallel-agent-workflow/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/post-migration-stability-validation.md` | `ai/specs/019-post-migration-stability-validation/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/raspberry-listening-indicator.md` | `ai/specs/020-raspberry-listening-indicator/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/raspberry-touch-ui.md` | `ai/specs/021-raspberry-touch-ui/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/release-v1.0.0.md` | `ai/specs/022-release-v1.0.0/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/web-dependency-audit-remediation.md` | `ai/specs/023-web-dependency-audit-remediation/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/web-listening-indicator.md` | `ai/specs/024-web-listening-indicator/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/web-validation-client.md` | `ai/specs/025-web-validation-client/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/week-04-demo-stability.md` | `ai/specs/026-week-04-demo-stability/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/week-05-agent-capability-pack.md` | `ai/specs/027-week-05-agent-capability-pack/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/week-05-demo-stability.md` | `ai/specs/028-week-05-demo-stability/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
| `specs/week-06-closeout.md` | `ai/specs/029-week-06-closeout/spec.md` | Migrated transition document: verify source ledger/canonical body before removal |
