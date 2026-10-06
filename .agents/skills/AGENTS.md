# Repository operating skills

Read [root](../../AGENTS.md) and [workflow](../../docs/ai-assisted-workflow.md)
first. This directory supplies discoverable SKILL.md knowledge plus public
references and optional tool metadata; it is also usable by reading those files
manually. The agent needs no particular provider, product or skill loader.

`raspberry-voice-demo/SKILL.md` routes guided live voice turns to the official
backend/SSH/demo scripts and runbook/checklist. `devexpert-inference/SKILL.md`
and `references/endpoint-summary.md` explain retained provider adapters and
historical external defaults. `raspberry-voice-demo/agents/openai.yaml` is optional
tool metadata, not canonical rules or a required loader; preserve it.

Depends on: repo specs/plans/runbooks and official scripts, plus task-specific
device/provider access when explicitly operating them. Used by: development or
operation agents when the workflow's matching task triggers the skill. Skills
do not replace specs, plans, human decisions or common workflow.

Before provider work apply [D025](../../docs/decisions.md#d025---devexpert-deprecado-para-la-validación-post-migración):
no real DevExpert smoke/credentials/reactivation without a new decision; retain
mock validation and historical technical information. Live voice operation alone
does not authorize code edits or helper scripts. Preserve triggers, safety,
guidance and references when editing skills. Check their links and script names;
do not run real SSH/audio/provider operations merely to validate prose.
There is no official skill-test target; follow documentation checks and use
existing tests only when the underlying behavior changes.
