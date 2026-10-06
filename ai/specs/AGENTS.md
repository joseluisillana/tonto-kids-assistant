# Specification context

Read [root](../../AGENTS.md), [AI workflow](../../docs/ai-assisted-workflow.md) and
[docs context](../../docs/AGENTS.md) first. Use [specs index](../../docs/specs.md),
[roadmap](../../docs/roadmap.md) and latest dated journal to find the applicable
contract; status inside an older phase spec alone does not select active work.

Specs describe behavior, scope, contracts, acceptance and validation. Conversation/
audio/web/provider specs define HTTP and product boundaries; touch/emulator/Kivy
specs define approved UI work; workflow and secret specs define operating limits.
Some implemented specs retain historical commands: capability pack's old
PowerShell helpers are migration evidence, not commands to recreate or execute.

Depends on: existing implementation evidence and human decisions. Used by:
component development, docs/plans handoffs, checks and operating skills.
No runtime imports. For a material change, update/create plan.md beside the definition
with the implementation prompt, scope and verification/isolation criteria in the
same change. Read spec.md, plan.md and journal.md first; follow the naming,
lifecycle and index rules in ai/README.md and this directory's README.md.
Pure editorial changes may omit a plan update with an explicit no-behavior-change
summary. Historical definitions are migrated into ai/specs/; GitHub issues
remain managed in GitHub and local records retain their full tracking URLs.

Review affected component AGENTS.md, consumers/tests and decisions before changing
acceptance. Check links and commands against public source and run
`git diff --check`; an edited spec does not prove implementation or hardware
acceptance. Use a distinct evidence entry for actual validation results.

## Instruction provenance

Moved from the former specs directory during the authorized legacy retirement. Architecture,
contract responsibilities, consumer checks and safety boundaries are preserved.
Placement/handoff guidance follows ai/README.md and the current templates.
Source text remains recoverable in immutable Git history; it is not copied as an
alternative instruction set. Use only the current rules for future work.
