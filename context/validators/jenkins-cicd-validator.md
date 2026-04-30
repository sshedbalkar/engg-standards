# validator.jenkins-cicd

- Validator ID: `validator.jenkins-cicd`
- Route: `route.jenkins-cicd`
- Source docs: `ESTD13`
- Overlay docs: `ESTD1`, `ESTD5`, `ESTD8`, `ESTD10`, `ESTD11`, `ESTD18`, `ESTD19`
- Applies to: Jenkinsfiles, Jenkins shared libraries, build agents, artifacts, signing, promotion gates, notifications, credentials, and CI validation stages.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Pipeline source and reuse | 15 | `ESTD13`, `ESTD18`, `ESTD19` | root Jenkinsfile, shared libraries, no duplicated orchestration, clear entrypoints |
| Secrets and build identity | 20 | `ESTD1`, `ESTD8`, `ESTD13` | no checked-in secrets, credentials binding, signing materials, build metadata |
| Build, test, and artifacts | 15 | `ESTD10`, `ESTD13` | lint/test/build stages, BOM scan, immutable artifacts, reports, retention |
| Promotion gates and rollback | 15 | `ESTD5`, `ESTD8`, `ESTD13` | environment promotion, approvals, release-close risk notes, rollback notes, artifact reuse |
| Agents, RBAC, and audit | 15 | `ESTD13` | agent hygiene, controller safety, plugin approval, RBAC, audit logging |
| Reporting and notifications | 10 | `ESTD10`, `ESTD13` | failure routing, archived evidence, build links, actionable messages |
| Maintainability and safety | 10 | `ESTD1`, `ESTD13`, `ESTD19` | declarative style, parameter validation, simple Groovy, testable helper logic |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Pipeline source and reuse | `static.jenkins.jenkinsfile-lint`, `static.common.folder-structure` | shared-library design intent |
| Secrets and build identity | `static.common.secrets`, `static.common.gitleaks`, `static.jenkins.jenkinsfile-lint` | credential boundary judgment |
| Build, test, and artifacts | `static.jenkins.jenkinsfile-lint` | artifact and evidence sufficiency |
| Promotion gates and rollback | `static.jenkins.jenkinsfile-lint` | approval and rollback intent |
| Agents, RBAC, and audit | `static.jenkins.jenkinsfile-lint` | RBAC and audit adequacy |
| Reporting and notifications | `static.jenkins.jenkinsfile-lint` | routing usefulness |
| Maintainability and safety | `static.jenkins.jenkinsfile-lint`, `static.common.semgrep` | Groovy maintainability judgment |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.jenkins-cicd` before each validator run.
- If CodePipeline-specific validators are added, keep Jenkins-only checks in this spec.
- Keep route binding aligned with `route.jenkins-cicd`.
