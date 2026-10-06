# Specs

Follow the [common process](../README.md). Each record lives in
`ai/specs/NNN-short-slug/` with spec.md, plan.md and journal.md, copied from
[_template](_template/spec.md). Read all three before acting.

## Identity and metadata

Allocate the next unused number above the highest allocated spec ID, starting
at 001, using exactly three digits and a short lowercase kebab-case slug.
`id` is the full folder name, e.g. `NNN-short-slug`; never reuse or renumber it.
This sequence is independent of local issues and GitHub. If three digits are
exhausted, ask for an explicit naming decision instead of silently changing it.
Use ISO dates YYYY-MM-DD, a responsible human/team in `owner`, and the `related`
path/URL list defined by the common process. Template placeholders are not records.

## Lifecycle

| Status | Entry and exit conditions |
| --- | --- |
| draft | Definition is being prepared; no implementation. Complete scope and acceptance criteria before planning. |
| planned | Definition and prior plan are ready and authorized within project approval rules. Start implementation to enter in-progress. |
| in-progress | Work follows the plan; record changes and verification. Enter blocked if a dependency or decision prevents progress. |
| blocked | Record the blocker and resume condition in the journal. Resume planned or in-progress when the condition is satisfied, with the reason recorded. |
| done | Required implementation, verification and acceptance are evidenced; no required work remains. |

Normal flow: draft → planned → in-progress → done, with blocked as a detour
from planned/in-progress. Material scope changes require revising the definition
and plan before continuing. Reopening done requires an explicit reason, revised
plan and recorded transition to planned; do not erase completed history.

Maintain [INDEX.md](INDEX.md) in the same change as metadata. Every status change
must update its row immediately, including title and updated date. Changes to
any record file update spec.md's `updated` and the index date. Never remove done
rows, folders or IDs. Capture decisions and evidence in the record journal.
The historical local definitions are now migrated. Legacy source paths are
retired Git provenance; edit canonical ai/ records. Shared journals/operating docs
remain at their sources, and GitHub issue history stays on GitHub.
