# Repository-defined issues

GitHub issues are defined and operated on GitHub. Do not import or mirror them
here. This directory holds local project definitions and migrated local issue
documents. Link corresponding GitHub tracking issues by full URL in related;
preserve the local definition/plan/journal without copying the remote lifecycle.
Consult linked GitHub evidence when needed, and do not invent missing associations.

Follow the [common process](../README.md). Each record lives in
`ai/issues/NNN-short-slug/` with issue.md, plan.md and journal.md, copied from
[_template](_template/issue.md). Read all three before acting.

Allocate the next unused number above the highest allocated local issue ID,
starting at 001, with exactly three digits and a lowercase kebab-case slug.
`id` is the full folder name; never reuse or renumber it. This sequence is
independent of specs and GitHub numbers. If exhausted, ask for an explicit naming
decision. Use YYYY-MM-DD dates, a responsible human/team as `owner`, and repository
paths/full URLs in `related`. Template placeholders are not registered issues.

## Lifecycle

| Status | Entry and exit conditions |
| --- | --- |
| open | Problem/task is recorded; define context and resolution criteria before planning. |
| planned | Prior plan and resolution criteria are ready and authorized within project rules. |
| in-progress | Execution has started; record progress, decisions and verification. |
| resolved | Resolution criteria are met with evidence, but review/integration or required closure acceptance remains. |
| closed | Required review, integration and acceptance are complete and evidenced. Retain the record. |

Normal flow: open → planned → in-progress → resolved → closed. Record blockers
and resume conditions in the journal while retaining the current status; there
is no issue `blocked` status. Reopen resolved/closed to open or planned only with
a recorded reason and updated plan before implementation. Do not erase history.

Maintain [INDEX.md](INDEX.md) in the same change as metadata. Every status change
must update the row immediately; title and updated must match. Changes to any
record file update issue.md's `updated` and the index date. Keep closed rows,
folders and IDs. The existing local volume-delay document is migrated with its
GitHub #114 reference; its old path is a transition pointer. GitHub issues remain
on GitHub, so this index represents local definitions only. Local resolution does not close GitHub, and
parents cannot close while required child or untracked tasks remain.
