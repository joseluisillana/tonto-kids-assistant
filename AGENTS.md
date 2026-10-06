# TONTO Kids Assistant — agent entry point

## Before any work

1. Read this file first. Before choosing or executing a work item, read
   [roadmap](docs/roadmap.md), [specs index](docs/specs.md) and the newest dated
   entry under [project journal](docs/project-journal). Journal filenames alone
   do not determine recency. These sources own milestone/sprint status.
2. Read [AI-assisted workflow](docs/ai-assisted-workflow.md) before any edit,
   formatter, generator or command that writes repository files. It owns the
   detailed common rules, approvals, environment, Git, handoff and evidence.
3. Run `git branch --show-current` and `git status --short --branch`. Do not edit
   on `main` unless explicitly instructed. Use a project branch (`feature/`,
   `fix/`, `docs/`, `chore/`, `experiment/`); no tool-owned prefix unless requested.
   If main is dirty, stop and ask before moving, stashing, committing, discarding
   or editing its changes. Parallel work requires separate branches/worktrees.
   Follow the workflow's complete [pre-edit gate](docs/ai-assisted-workflow.md#pre-edit-gate-for-ai-assistants).
4. Identify affected components. Read applicable local files listed below and
   all ancestors before editing; a local complements this file without relaxing
   global rules. For cross-component changes, read the relevant consumer and
   dependency instructions, public contracts and key source files, then verify
   impact and run relevant existing checks. If no local exists, use the nearest
   ancestor and the linked sources. Do not assume automatic instruction loading.

## Planning and tracking in ai/

Read [ai/README.md](ai/README.md) for the canonical planning/tracking process
and new or migrated records. Before acting on `ai/specs/<id>/` or
`ai/issues/<id>/`, read spec.md/issue.md, plan.md and journal.md. Plan before
implementation and maintain the record journal. Synchronize every status change
with its INDEX.md in the same change; keep metadata/index dates and titles aligned.
Retain closed records and rows. The historical local definitions are now migrated
and listed in the ai/ indexes; retired paths remain Git provenance only. Shared
milestone journals and operating docs retain their locations. GitHub issues remain
defined/managed in GitHub; local records preserve corresponding full URLs in related.

For work without a registered spec/issue, explicitly notify the user and wait
for an OK. An explicit OK already given for the same scope remains valid;
planning and evidence still apply. ai/ adds process: architecture, conventions,
security and operation in these instructions, local AGENTS.md and mandatory
common workflow remain applicable. The explicitly authorized transition
supersedes legacy placement rules for new records without editing local
architectural instructions.

## Project overview

TONTO is an educational physical assistant for children, optimized for a working,
understandable, reproducible demo. A Raspberry Pi sends an interaction to a
Python/FastAPI backend, which generates an educational response; the Raspberry
speaks it aloud. The backend owns AI orchestration and short in-process history.
The Raspberry is a thin client for device I/O, HTTP and local playback. The React,
TypeScript and Vite web client validates the same HTTP/JSON contracts. Kivy touch
UI is documented post-MVP work, not permission for broader product expansion.

Flow: Raspberry capture or browser capture → compatible WAV → backend STT →
conversation/provider → response → Raspberry espeak or browser native speech.
Text `/chat` remains a fallback. No client imports the backend's orchestration.
Go artifacts, if encountered, are legacy/evaluation, not active implementation
or CI gates unless explicitly reactivated with updated docs/specs.

Read [architecture](docs/architecture.md) and [decisions](docs/decisions.md) for
design context. The older architecture text contains initial Windows and shared
model descriptions; the actual Linux/Docker command surface and source files
below determine current implementation evidence. Do not silently resolve a
conflict: follow [Decisions and conflicts](docs/ai-assisted-workflow.md#decisions-and-conflicts).
The reconstruction prompt is [project genesis](docs/project-genesis.md).

## Repository map and change impact

| Area / local instructions | Responsibility and relations |
| --- | --- |
| [backend/](backend/AGENTS.md) | FastAPI routes, provider chat/STT and in-memory history; HTTP consumed by client/web; tested in tests/ |
| [client/](client/AGENTS.md) | Python text/voice loop, device audio and Kivy touch UI; consumes backend HTTP; launched by demo scripts/emulator; tested in tests/ |
| [web/](web/AGENTS.md) | React validation pages, browser capture/speech and TypeScript HTTP client; consumes backend; owns web/tests |
| [shared/](shared/AGENTS.md) | Reserved shared contracts; currently placeholder, not a runtime dependency imported by clients/backend |
| [scripts/](scripts/AGENTS.md) | Bash operation, SSH, demos, emulator, export and syntax checks; supports runtime and CI; CLI scripts tested in tests/ |
| [tests/](tests/AGENTS.md) | Python API/provider/client/CLI and real Kivy-widget tests; consumes implementation, not vice versa |
| [spikes/](spikes/AGENTS.md) | Standalone Kivy exploration; not the product client or official CI suite |
| [docs/](docs/AGENTS.md) | Architecture, decisions, workflow, journal, runbooks and execution plans |
| [ai/specs/](ai/specs/AGENTS.md) | Registered contracts, plans, journals and validation scope |
| [.agents/skills/](.agents/skills/AGENTS.md) | Optional discoverable operating guidance, also readable manually; delegates to docs/scripts |

Contract changes in backend affect both clients and their tests. The authoritative
models currently live in `backend/main.py` and `backend/audio_router.py`, with
TypeScript counterparts in `web/src/types/conversation.ts` and `web/src/api/backendClient.ts`.
`shared/models.py` is a placeholder; shared structures belong there when needed,
without introducing a new contract layer as part of unrelated work.

## Global guardrails

- Keep scope narrow, simple, debuggable and demo-first. Do not silently change
  architecture/milestone scope, rewrite unrelated files or implement future
  features without an explicit request. Apply the workflow's coding/simplicity
  rules and handle obvious failures, especially timeouts and unavailable TTS.
- Ask before new runtime/development dependencies or architecture changes.
  Explain need, simpler alternative, use and Raspberry setup impact per
  [Approval boundaries](docs/ai-assisted-workflow.md#approval-boundaries).
- Keep state in memory only if needed. MVP exclusions remain: wake word, Arduino,
  persistence/auth/accounts, advanced memory or multi-agent product architecture,
  local AI/STT/audio models, advanced product UI beyond the narrow validation
  surface, and automated audio capture/upload outside the specified web loop or
  Raspberry work explicitly requested for the milestone. Approved post-MVP UI
  uses its own spec; these limits do not undo existing approved implementation.
- Never expose a manual WAV upload/file picker in the Phase 3 product/demo UI;
  WAV fixtures/integration helpers are allowed. Do not add backend webm/ogg
  transcoding without an explicit later decision.
- Use official Linux/Docker/Bash commands, local dependencies/caches and the
  environment rules in the workflow. No global packages or removed Windows
  runtime paths. If sandboxing blocks official commands, request escalation for
  those commands rather than switching to global tools.
- Preserve `.env` and automated backend/SSH operation. Never read credentials
  for diagnostics or capture expanded Compose config, environment dumps, raw
  provider error bodies or shell traces. Use bounded official helpers. Read
  [Secret-safe diagnostics](docs/ai-assisted-workflow.md#secret-safe-diagnostics-110)
  and [the #110 spec](ai/specs/003-agent-secrets-protection/spec.md) before related work.
  These controls reduce accidental exposure; they do not provide isolation.
- Apply [D025](docs/decisions.md#d025---devexpert-deprecado-para-la-validación-post-migración)
  before provider operation: DevExpert code/tests/history remain; no real smoke,
  credentials request or reactivation without a new operator decision.
- Keep behavior, tests and relevant documentation in one coherent work item.
  Material spec changes require a paired plan and implementation prompt via
  [Spec Handoff Workflow](docs/ai-assisted-workflow.md#spec-handoff-workflow).
  Keep latest explicit user decisions and record persistent changes; make code/doc
  discrepancies explicit before proceeding with the affected decision.

## Development workflows and testing

Run commands from the repository root; `tonto.sh` is the main entry point.

| Command | Existing purpose |
| --- | --- |
| `./tonto.sh setup` | Prepare Docker Python environment/dependencies and local web dependencies |
| `./tonto.sh setup host` | Optional host .venv for IDE/direct Python; separate from Docker volume |
| `./tonto.sh dev backend` / `dev web` / `dev all` | Run backend, web or both via runtime Compose |
| `./tonto.sh dev ui` | Linux Kivy emulator; audible capture/playback requires host audio devices |
| `./tonto.sh test python` | Python syntax and non-Kivy tests under tests/ |
| `./tonto.sh test ui` | Real Kivy widgets in Docker/Xvfb, not hardware acceptance |
| `./tonto.sh test web` | TypeScript test compilation and web/tests Node suite |
| `./tonto.sh test all` | Python + Kivy + web checks; CI uses this |
| `./tonto.sh build web` / `build all` | TypeScript check and Vite web build; CI uses build all |
| `./tonto.sh down` (alias `stop`) | Project containers/networks cleanup; dependency volume preserved |

CI is [.github/workflows/ci.yml](.github/workflows/ci.yml): setup, test all, build all.
There are no public lint/format/generation targets to assume. Documentation-only
changes need reference/meaning checks and `git diff --check`; choose behavior
tests by the affected component. Automated tests do not establish physical voice,
touch, kiosk or provider-real validation; use the appropriate runbook/spec.

Before operating backend/Raspberry, read the workflow's
[Agent Capability Pack](docs/ai-assisted-workflow.md#agent-capability-pack).
It routes to official lifecycle/SSH/demo helpers, runbook and checklist.
Before exports/documentation routines, read [documentation workflow](docs/documentation-workflow.md).
For provider changes or live voice turns, read the matching
[repo-local skill and resources](docs/ai-assisted-workflow.md#repo-local-agent-skills)
manually if necessary. No provider or skill-loading mechanism is required for
the development agent itself.
