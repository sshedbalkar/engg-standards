# validator.web-tools

- Validator ID: `validator.web-tools`
- Route: `route.web-tools`
- Source docs: `ESTD11`
- Overlay docs: `ESTD1`, `ESTD4`, `ESTD5`, `ESTD8`, `ESTD9`, `ESTD10`, `ESTD13`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`
- Applies to: internal web tools, dashboards, support tooling, operational UIs, VPN-gated tools, NextJS/TypeScript tooling apps.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| TypeScript and React conformity | 15 | `ESTD11`, `ESTD14`, `ESTD18` | strict TypeScript, no unsafe `any`, runtime validation, component design, naming, contextual collection/map names, folder layout |
| Tool API integration | 10 | `ESTD11`, `ESTD4`, `ESTD9`, `ESTD19` | centralized API layer, no direct browser-to-database access, untrusted tool input, request validation, response handling, dependency boundaries |
| Auth, authorization, and access control | 15 | `ESTD11`, `ESTD1`, `ESTD5`, `ESTD8` | authenticated routes, RBAC, permission boundaries, Cognito/IAM alignment, least privilege, session timeout |
| Sensitive actions and auditability | 15 | `ESTD11`, `ESTD9`, `ESTD10` | PII display, destructive action confirmation, before/after review, audit logs, migration notes |
| UX, accessibility, and operability | 15 | `ESTD11` | shared components, loading/error states, accessibility, text readiness, operational task completion |
| Deployment and environment safety | 10 | `ESTD11`, `ESTD13`, `ESTD5`, `ESTD8` | Jenkins build/deploy, environments, release-close risk notes, rollback, timing, secrets, monitoring |
| Testing and path coverage | 10 | `ESTD11`, `ESTD16` | unit/integration tests, UI states, guard clauses, edge cases, coverage intent |
| Security and dependency hygiene | 10 | `ESTD1`, `ESTD11`, `ESTD19` | dependency rules, supply-chain checks, input trust boundary, permission boundaries, sensitive logging, coupling |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| TypeScript and React conformity | `static.web.typescript`, `static.web.eslint`, `static.common.folder-structure` | component design intent |
| Tool API integration | `static.web.typescript`, `static.web.eslint`, `static.common.semgrep` | API, trust, and database boundary judgment |
| Auth, authorization, and access control | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | RBAC and access-flow intent |
| Sensitive actions and auditability | `static.common.semgrep` | operational risk judgment |
| UX, accessibility, and operability | `static.web.eslint` | UX completeness and task ergonomics |
| Deployment and environment safety | `static.common.report-consistency` | deployment evidence quality |
| Testing and path coverage | `static.web.typescript`, `static.web.eslint` | path intent and coverage adequacy |
| Security and dependency hygiene | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | dependency/coupling and permission-boundary intent |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.web-tools` before each validator run.
- If whitelisted web-tool library guidance is added, update the TypeScript and dependency groups.
- Keep route binding aligned with `route.web-tools`.
