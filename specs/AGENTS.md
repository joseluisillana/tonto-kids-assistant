# Specification context

Read [root](../AGENTS.md), [AI workflow](../docs/ai-assisted-workflow.md) and
[docs context](../docs/AGENTS.md) first. Use [specs index](../docs/specs.md),
[roadmap](../docs/roadmap.md) and latest dated journal to find the applicable
contract; status inside an older phase spec alone does not select active work.

Specs describe behavior, scope, contracts, acceptance and validation. Conversation/
audio/web/provider specs define HTTP and product boundaries; touch/emulator/Kivy
specs define approved UI work; workflow and secret specs define operating limits.
Some implemented specs retain historical commands: capability pack's old
PowerShell helpers are migration evidence, not commands to recreate or execute.

Depends on: existing implementation evidence and human decisions. Used by:
component development, docs/plans handoffs, checks and operating skills.
No runtime imports. For a material change, update/create its plan under docs/plans
with the implementation prompt, scope and verification/isolation criteria in the
same change. Keep normal naming and template rules in the canonical workflow.
Pure editorial changes may omit a plan update with an explicit no-behavior-change
summary. This hierarchy does not alter SDD management or move existing specs.

Review affected component AGENTS.md, consumers/tests and decisions before changing
acceptance. Check links and commands against public source and run
`git diff --check`; an edited spec does not prove implementation or hardware
acceptance. Use a distinct evidence entry for actual validation results.
