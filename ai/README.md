# AI-assisted planning and tracking

This directory owns the planning and tracking process for new and migrated
records. Any human or agent can follow it: no AI provider, model, IDE, extension,
CLI, plugin or skill loader is required. Product inference providers are separate
from the choice of development assistant.

Read [root instructions](../AGENTS.md) and the mandatory
[common workflow](../docs/ai-assisted-workflow.md). These retain architecture,
conventions, permissions, Git, environment, operating commands and security.
This process complements those instructions; it does not replace them.

## Choosing a record

Use a [spec](specs/README.md) to define a change, contract or capability with
acceptance criteria. Use an [issue](issues/README.md) for a bounded problem or
task, including validation and coordination. Link related records rather than
duplicating requirements. One spec can relate to several issues and vice versa.

Before acting on a record, read its spec.md/issue.md, plan.md and journal.md.
Prepare plan.md before implementation, including verification and handoff.
Maintain the record's journal with decisions, changes, evidence and pending work.
Update metadata and the corresponding INDEX.md together; every status change
must appear in the same change in both places. Update `updated` when any record
content changes. Index titles and dates must match the record. Retain closed
records, rows and IDs. Global milestone journals remain useful context and link
to record journals; they do not replace them.

If work has no registered spec or issue, explicitly tell the user and wait for
an OK before proceeding. An explicit OK already given for that same scope remains
valid. The exception does
not remove prior planning or evidence requirements: record the authorization,
plan and results in the existing project plan/journal documentation.
The operator's explicit phase-1 instrumentation request authorizes creation of
this structure without a concrete new spec/issue; its plan and global journal
provide evidence.

## Security

Never include secrets, credentials, tokens, connection strings, PII or real
customer data in records, plans, journals, examples or evidence. Describe sensitive
configuration only by parameter name, never its value. Use fictional examples
and sanitized evidence. Do not read credential files to prepare this process or
its migration. Preserve all existing secret-safe diagnostic and operating rules.

## Transition and GitHub

The [spec index](specs/INDEX.md) and [local issue index](issues/INDEX.md) now cover
the 28 migrated historical definitions, one existing local issue and new records.
[Migration evidence](specs/001-historical-records-migration/metadata-review.md)
records source/destination coverage, dates and status decisions. The retired
specs/, docs/plans/ and docs/issues/ paths are recorded as provenance; current
procedure, rules and templates belong exclusively to ai/. Original sources
remain recoverable from the immutable Git baseline in that ledger.
The [project overview](../docs/specs.md), shared [journals](../docs/project-journal),
architecture, decisions, operating guides and visual assets keep their sources.
The phase-1 instrumentation plan is retained as historical migration evidence.
The old plan template has no legacy copy or operational references: use only
ai/specs/_template/ and ai/issues/_template/.
See [link impact](specs/001-historical-records-migration/cleanup-impact.md)
for the authorized reference corrections and remaining external limitations.

Every migrated record has one canonical destination. Preserve provenance,
original links and shared artifacts; migration must not invent dates, prior plans,
validation or completion. Phase 2 relocates local history; GitHub issues remain
remote references and are not part of the local record count.

`related` is a YAML list of unambiguous repository-relative paths or full external
URLs. Use it for specs, local issues, GitHub issues and original artifacts. IDs
belong to separate local sequences; they are not GitHub issue numbers. GitHub
keeps its numbers, URLs, definitions, lifecycle and history. Manage GitHub issues
on GitHub; do not import or mirror them as local issue records. ai/issues/ holds
repository-defined issues only, including existing local definitions migrated
from the legacy structure. Every migrated local spec/issue must preserve correct
full URLs to its corresponding GitHub tracking issue(s) in related. Distinguish
tracking issues from contextual issue or PR references; never invent a link when
no corresponding issue is documented. Read linked issues and their parent/child
relationships when coordinating work; no one-to-one mapping is assumed.
Local `resolved` does not automatically close GitHub. Keep parent issues open
while child issues or other required tasks remain. PR closing keywords apply
only to issues fully completed, as required by the common workflow.

The current NotebookLM export does not select ai/. Read ai/ directly; an export
is not a complete source for this process. No exporter or CI change is included.

Historical procedure, placement and template examples preserved in migrated
specs/plans are evidence of earlier decisions. They do not authorize an alternate
workflow: all ongoing work, including on historical records, uses the current
ai/ rules and templates, its adjacent plan.md/journal.md and synchronized index.
