# CI Local Cache Alignment

## Status

Approved for implementation planning on 2026-07-20. Not implemented yet.
Implementation tracking: GitHub Issue #89.

## Context

GitHub Actions CI uses `actions/setup-python@v5` with its integrated pip
cache and `actions/setup-node@v4` with its integrated npm cache.

The repository setup command, `scripts/setup-dev.ps1`, follows the project
isolation policy and creates these cache directories inside the checked-out
repository:

- `.cache/pip`
- `.cache/npm`

Every pip installation receives `--cache-dir <repo>/.cache/pip`, and every npm
installation receives `--cache <repo>/.cache/npm`.

The integrated setup Actions discover cache locations independently:

- `setup-python` runs `pip cache dir`.
- `setup-node` runs `npm config get cache`.

Without explicit environment configuration, those commands resolve to
runner-profile paths such as `/home/runner/.cache/pip` and
`/home/runner/.npm`. Per-command `--cache-dir` and `--cache` arguments used
later by `setup-dev.ps1` do not change those discovery results.

## Observed Failure

The CI run associated with PR #80 completed dependency setup, all 78 Python
tests, the web tests, and the build. It failed only during the
`actions/setup-python@v5` post-job step:

```text
Cache folder path is retrieved for pip but doesn't exist on disk:
/home/runner/.cache/pip.
```

The setup Action had registered the global pip cache path, while the project
script had populated only `.cache/pip`. PR #80 was documentation-only and did
not introduce this mismatch; its run exposed an existing configuration defect.

The npm configuration has the same conceptual mismatch. Its post-job step did
not fail in that run because the global npm path happened to exist, but relying
on incidental runner state violates the repository cache-isolation rule.

## Decision

Keep the integrated cache support in `actions/setup-python` and
`actions/setup-node`, but configure both package managers so cache discovery
and the official setup script refer to the same repository-local directories.

The CI job must expose:

```yaml
PIP_CACHE_DIR: ${{ github.workspace }}/.cache/pip
npm_config_cache: ${{ github.workspace }}/.cache/npm
```

These values must be in scope when the setup Actions execute and during their
post-job steps. The exact YAML placement is an implementation detail, provided
that this lifecycle requirement is satisfied.

The existing integrated cache dependency inputs remain authoritative:

- Python: `backend/requirements.txt`, `client/requirements.txt`, and
  `requirements-dev.txt`.
- Node: `web/package-lock.json`.

## Rationale

This decision:

- preserves cache reuse between GitHub Actions runs;
- keeps cache data under the repository workspace rather than runner profiles;
- aligns CI, humans, and agents with `scripts/setup-dev.ps1`;
- fixes the pip post-job failure;
- removes the equivalent latent npm inconsistency;
- requires no new runtime or development dependency.

## Alternatives Considered

### Remove the integrated pip cache

Removing `cache: pip` would avoid the failing Python post-job step, but Python
dependencies would be downloaded again for each fresh runner. It would also
leave the npm cache policy inconsistent. This option was rejected because
explicit alignment is still small and preserves useful cross-run caching.

### Create the global runner cache directories

Creating `/home/runner/.cache/pip` and `/home/runner/.npm` would satisfy the
Actions but would maintain two cache locations and violate the project rule
that supported caches stay under `.cache/` in the repository. This option was
rejected.

## Scope

Included:

- align pip cache discovery with `.cache/pip` in GitHub Actions;
- align npm cache discovery with `.cache/npm` in GitHub Actions;
- retain the integrated caches and their current dependency files;
- validate setup, tests, build, and all post-job cleanup steps on GitHub
  Actions;
- update durable documentation if implementation changes the final recorded
  CI state.

Excluded:

- changes to Python, backend, Raspberry, web application, or shared product
  behavior;
- changes to `scripts/setup-dev.ps1` unless implementation evidence proves the
  approved alignment cannot work without one;
- new package dependencies or Actions;
- global cache directories;
- changes to API contracts, architecture, MVP scope, or provider behavior;
- unrelated Action version upgrades or CI restructuring.

## Acceptance Criteria

1. `pip cache dir` resolves to `${{ github.workspace }}/.cache/pip` for the
   setup-python cache lifecycle.
2. `npm config get cache` resolves to
   `${{ github.workspace }}/.cache/npm` for the setup-node cache lifecycle.
3. `scripts/setup-dev.ps1` remains the CI dependency setup command and
   populates the same local cache directories.
4. The official Python and web checks pass.
5. The official build passes.
6. The setup-python and setup-node post-job steps complete without a missing
   cache-directory error.
7. A subsequent run with unchanged dependency files can restore the integrated
   caches, or the run logs provide a clear non-defect reason why no hit was
   available.
8. No dependency, product contract, or MVP architecture is changed.

## Validation Evidence Required

The implementation PR must record:

- the GitHub Actions run URL;
- the result of dependency setup, tests, and build;
- the result of both cache post-job steps;
- the discovered pip and npm cache paths shown in the logs;
- whether each cache was restored or saved.

Local checks alone are insufficient because the original failure occurs in the
GitHub-hosted runner post-job lifecycle.
