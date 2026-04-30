# ESTD Enforcer Kit

The ESTD Enforcer Kit lets a Bingo repository opt in to ESTD validation by adding this standards repo as a submodule.

Repos without the configured ESTD submodule are out of scope. The CLI writes a not-applicable report and exits successfully instead of enforcing standards.

## Install In A Consumer Repo

```bash
git submodule add <standards-repo-url> standards/bingo-bash-standards
mkdir -p .estd
cp standards/bingo-bash-standards/tools/estd-enforcer/config.example.yaml .estd/config.yaml
cp standards/bingo-bash-standards/tools/estd-enforcer/exceptions.example.yaml .estd/exceptions.yaml
```

Add repo-local LLM guidance, normally in the consumer repo's `AGENTS.md`, so coding agents know the repo has opted in:

```md
## ESTD Standards

- This repo opts in to ESTD through `standards/bingo-bash-standards`.
- Before writing code, read `standards/bingo-bash-standards/AGENTS.md`.
- After writing code, run `standards/bingo-bash-standards/tools/estd-enforcer/bin/estd-enforce validate --repo . --config .estd/config.yaml --out build/estd`.
- Summarize `build/estd/report.md` before handing back the change.
```

The default config is:

```yaml
version: 2
standardsPath: standards/bingo-bash-standards
profile: auto
mode: blocking
scope: changed-files
minScore: 75
failOnCritical: true
validationStrategy: static-first
llmPolicy: gaps-only
requiredStaticTools: []
exceptionsFile: .estd/exceptions.yaml
```

## Current Developer And LLM Run

```bash
standards/bingo-bash-standards/tools/estd-enforcer/bin/estd-enforce validate \
  --repo . \
  --config .estd/config.yaml \
  --out build/estd
```

Outputs:

- `build/estd/static-report.json`: normalized static validator output.
- `build/estd/llm-request.md`: LLM gap request, emitted only when semantic gaps remain.
- `build/estd/llm-report.json`: LLM output, emitted only when LLM runs.
- `build/estd/report.json`: merged machine-readable gate report.
- `build/estd/report.md`: human-readable summary.

Exit codes:

- `0`: pass, advisory pass, or not applicable because the repo has not opted in.
- `1`: standards gate failed.
- `2`: configuration, LLM, schema, or retrieval error.

## Existing And New Repos

Existing repositories should keep `scope: changed-files` so old unrelated debt does not block unrelated work. Run full-repo mode separately as advisory inventory:

```bash
standards/bingo-bash-standards/tools/estd-enforcer/bin/estd-enforce validate \
  --repo . \
  --scope full-repo \
  --mode advisory \
  --out build/estd-full
```

New repositories should set `scope: full-repo` in `.estd/config.yaml` because there is no legacy baseline.

Validation is developer/LLM-driven for now. The LLM must summarize status, score, critical blockers, unknown evidence, and unresolved gaps from `build/estd/report.md` before handing back code.

## Validation References

- Static validation inventory: `context/validators/static-validation.md`.
- LLM based validation inventory: `context/validators/llm-based-validation.md`.
- Route-bound validator specs: `context/validators/`.

## LLM Adapter

Static validators run first. Set `ESTD_LLM_COMMAND` to an approved internal agent or corporate LLM adapter only for unresolved semantic gaps. The command must read the request Markdown on stdin and write report JSON on stdout.

```bash
ESTD_LLM_COMMAND="bingo-llm validate-estd" \
  standards/bingo-bash-standards/tools/estd-enforcer/bin/estd-enforce validate --repo .
```

For tests or dry runs, pass a precomputed report:

```bash
standards/bingo-bash-standards/tools/estd-enforcer/bin/estd-enforce validate \
  --repo . \
  --report standards/bingo-bash-standards/tools/estd-enforcer/tests/fixtures/reports/pass.json
```

## Future CI Gate

Do not add organization-wide blocking CI until rollout timing is approved.

When CI enforcement is approved, Jenkinsfiles should only orchestrate the same opt-in gate and archive reports:

```groovy
stage('ESTD Standards Gate') {
  steps {
    sh 'standards/bingo-bash-standards/tools/estd-enforcer/bin/estd-enforce validate --repo . --base origin/main --out build/estd'
  }
  post {
    always {
      archiveArtifacts artifacts: 'build/estd/*', allowEmptyArchive: true
    }
  }
}
```

Recommended rollout:

1. Run advisory CI on opted-in repos and archive `build/estd/*`.
2. Confirm route selection, static tools, LLM adapter, citations, and exception handling in real repos.
3. Promote selected opted-in repos to blocking CI.

## Static Checks

Static check definitions live in `tools/estd-enforcer/static-checks/registry.json`.

- Built-in checks always run.
- Optional command checks run when their local tool and matching files are present.
- Required command checks are configured with `requiredStaticTools`; missing required tools exit `2`.
- Missing optional command checks create LLM gaps only for validator groups that still need judgment.
- Static failures are authoritative and cannot be overridden by LLM output.
- Update `context/validators/static-validation.md` when static checks or Static Coverage mappings change.

## Exceptions

Exceptions live in `.estd/exceptions.yaml` in the consumer repo.

Required fields:

- `id`
- `estdId`
- `section`
- `reason`
- `approver`
- `expiresOn`
- `remediationPlan`
- `ticket`
- `securityCritical: false`

Security-critical standards are non-exempt. Expired, incomplete, or security-critical exceptions fail the gate.
