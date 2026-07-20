# CI Local Cache Alignment Implementation Plan

## Objective

Implement the cache policy approved in
`specs/ci-local-cache-alignment.md` so GitHub Actions and
`scripts/setup-dev.ps1` consistently use repository-local pip and npm cache
directories while preserving cache reuse between CI runs.

## Source Spec

- Spec: `specs/ci-local-cache-alignment.md`
- Related docs:
  - `AGENTS.md`
  - `docs/ai-assisted-workflow.md`
  - `docs/specs.md`
  - `docs/project-genesis.md`
  - `docs/decisions.md`

## Scope

Included:

- configure the CI job environment so pip resolves its cache to
  `${{ github.workspace }}/.cache/pip`;
- configure the CI job environment so npm resolves its cache to
  `${{ github.workspace }}/.cache/npm`;
- retain the integrated caches in `actions/setup-python@v5` and
  `actions/setup-node@v4`;
- retain the current cache dependency files;
- run the official project checks and validate the complete GitHub Actions
  lifecycle, including post-job cleanup;
- record validation evidence in the PR and update durable project
  documentation only if necessary.

Excluded:

- product code changes;
- changes to `scripts/setup-dev.ps1` without new evidence and an explicit
  decision;
- dependency additions;
- Action version upgrades;
- CI job restructuring;
- global runner cache creation;
- unrelated warning cleanup, including Node runtime deprecation warnings.

## Implementation Plan

1. Start from an up-to-date `main` and create the focused branch
   `fix/ci-local-cache-alignment`.
2. In `.github/workflows/ci.yml`, declare `PIP_CACHE_DIR` and
   `npm_config_cache` with repository-local paths at a scope that applies to
   the setup Actions and their post-job steps.
3. Preserve the current Python and Node versions, integrated cache settings,
   dependency path inputs, and official script commands.
4. Review the workflow diff to confirm no unrelated CI behavior changed.
5. Run the official local setup, test, and build commands.
6. Push the branch and open a focused PR.
7. Inspect the GitHub Actions logs, including setup cache discovery and every
   post-job step.
8. If the first run is a cache miss, rerun the same commit once to verify
   cross-run restore behavior without changing dependency files.
9. Record the run URL and cache evidence in the PR before requesting merge.

## Acceptance Criteria

- The implementation satisfies all acceptance criteria in
  `specs/ci-local-cache-alignment.md`.
- The workflow continues to call `./scripts/setup-dev.ps1`,
  `./scripts/test.ps1 -Target all`, and
  `./scripts/build.ps1 -Target all`.
- Both package managers report repository-local cache paths.
- Python tests, web tests, and the web build pass.
- Neither cache Action fails during post-job cleanup.
- No source code, package manifest, dependency, or product contract changes.

## Verification

Run locally through the official command surface:

```powershell
.\scripts\setup-dev.ps1
.\scripts\test.ps1 -Target all
.\scripts\build.ps1 -Target all
git diff --check
git status --short --branch
```

Then validate on GitHub Actions:

1. Confirm the setup-python log reports
   `${{ github.workspace }}/.cache/pip`.
2. Confirm the setup-node log reports
   `${{ github.workspace }}/.cache/npm`.
3. Confirm setup, tests, and build pass.
4. Confirm both cache post-job steps pass.
5. If necessary, rerun the unchanged commit and confirm a cache restore.

## Implementation Prompt

```text
Implement the spec in specs/ci-local-cache-alignment.md using
docs/plans/ci-local-cache-alignment-implementation-plan.md.

Before editing:
- Read AGENTS.md.
- Read docs/roadmap.md, docs/specs.md, and the latest project journal entry.
- Read docs/ai-assisted-workflow.md.
- Read the source spec and this implementation plan.
- Run git branch --show-current and git status --short --branch.
- Start from an up-to-date main and use branch fix/ci-local-cache-alignment.
- Preserve unrelated user changes in the worktree.

Task:
- Make the smallest workflow-only change that aligns pip with
  ${{ github.workspace }}/.cache/pip and npm with
  ${{ github.workspace }}/.cache/npm.
- Ensure those settings apply to the setup Actions and their post-job steps.
- Keep the current Action versions, dependency paths, and official script
  commands.
- Do not modify product code, add dependencies, restructure CI, or create
  global runner cache directories.

Verification:
- Run .\scripts\setup-dev.ps1.
- Run .\scripts\test.ps1 -Target all.
- Run .\scripts\build.ps1 -Target all.
- Run git diff --check and git status --short --branch.
- Push a focused PR and inspect the full GitHub Actions lifecycle.
- Confirm the discovered cache paths and both post-job results.
- If the first run is a miss, rerun the unchanged commit to verify restore.
- Record the GitHub Actions run URL and cache evidence in the PR.

Delivery:
- Summarize the workflow change.
- Summarize local verification.
- Summarize GitHub Actions setup, test, build, and post-job evidence.
- Report whether each integrated cache was restored or saved.
```

## Workflow Isolation

- Branch: `fix/ci-local-cache-alignment`
- Worktree: the implementation may use the primary checkout if no other work
  is active; otherwise create a dedicated worktree.
- Parallel-safe: yes, provided no other work edits `.github/workflows/ci.yml`
  or the same durable documentation.
- Collision risk: `.github/workflows/ci.yml`, `docs/specs.md`, and any
  implementation evidence document selected later.
- Integration note: if a related CI PR merges first, update from `main`,
  confirm whether it already changes cache discovery, and reconcile against
  the source spec before editing.
- GitHub tracking: Issue #89. Reference it from the implementation PR; close it
  only when the acceptance criteria and GitHub Actions evidence are complete.

## Notes / Assumptions

- The approved solution keeps both integrated caches.
- The environment variable names are the package-manager-supported mechanisms
  used by their cache discovery commands.
- GitHub-hosted runner validation is mandatory because local execution cannot
  reproduce Action post-job behavior.
- This plan does not authorize implementation until the developer gives an
  explicit instruction to proceed.
