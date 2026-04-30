# validator.product-website

- Validator ID: `validator.product-website`
- Route: `route.product-website`
- Source docs: `ESTD11`, `ESTD5`, `ESTD8`, `ESTD9`, `ESTD13`
- Overlay docs: `ESTD1`, `ESTD4`, `ESTD10`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`
- Applies to: public product website, WebGL play surface, announcements, community pages, NextJS frontend, NestJS backend, website MySQL access.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Web architecture and TypeScript | 15 | `ESTD11`, `ESTD14`, `ESTD18` | project structure, strict TypeScript, component boundaries, naming, contextual collection/map names, folder layout |
| Public UX and WebGL launch surface | 10 | `ESTD11`, `ESTD1` | loading/error states, accessibility, localization readiness, WebGL entry behavior, user-impact safeguards |
| API and backend boundaries | 15 | `ESTD4`, `ESTD9`, `ESTD11`, `ESTD19` | centralized API layer, no direct browser-to-database access, trust boundaries, permission boundaries, request/response contracts, validation, service boundaries, dependency direction |
| Data and persistence | 10 | `ESTD9` | MySQL schema/query safety, migrations, indexes, retention, permissions, over-privileged DB risk |
| Cloud and edge deployment | 15 | `ESTD5`, `ESTD8` | environments, HTTPS, CDN, WAF, secrets, network and permission boundaries, observability, cost controls |
| CI/CD and release safety | 10 | `ESTD13`, `ESTD10` | build/test pipeline, artifact identity, promotion gates, release-close risk notes, rollback notes, review evidence |
| Security and privacy | 15 | `ESTD1`, `ESTD4`, `ESTD5`, `ESTD8`, `ESTD11` | auth where applicable, trust boundaries, permission boundaries, sensitive data handling, dependency security, transport security, auditability |
| Testing and path coverage | 10 | `ESTD16`, `ESTD11` | unit/integration coverage, branch paths, edge cases, UI states, deployment validation |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Web architecture and TypeScript | `static.web.typescript`, `static.web.eslint`, `static.common.folder-structure` | architecture and component boundary intent |
| Public UX and WebGL launch surface | None | UX completeness and player impact |
| API and backend boundaries | `static.web.typescript`, `static.web.eslint`, `static.common.semgrep` | API contract, trust, and database boundary intent |
| Data and persistence | `static.common.semgrep` | schema and migration intent |
| Cloud and edge deployment | `static.cloud.checkov`, `static.cloud.terraform-validate` | edge deployment trade-offs |
| CI/CD and release safety | `static.common.report-consistency` | release evidence quality |
| Security and privacy | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | auth/privacy and permission-boundary intent |
| Testing and path coverage | `static.web.typescript`, `static.web.eslint` | path intent and coverage adequacy |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- If a dedicated product website ESTD is added, make it a Source ESTD doc and rebalance groups.
- Recheck route coverage when public website technologies or deployment paths change.
- Keep route binding aligned with `route.product-website`.
