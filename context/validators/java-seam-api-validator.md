# validator.java-seam-api

- Validator ID: `validator.java-seam-api`
- Route: `route.java-seam-api`
- Source docs: `ESTD4`, `ESTD7`, `ESTD9`
- Overlay docs: `ESTD1`, `ESTD5`, `ESTD10`, `ESTD14`, `ESTD16`, `ESTD17`, `ESTD18`, `ESTD19`
- Applies to: Java SEAM microservice APIs, service layers, controllers, repositories, Maven dependencies, persistence logic, and service-owned schemas.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| API design and SEAM layering | 15 | `ESTD4`, `ESTD7`, `ESTD19` | service boundaries, trust boundaries, stateless API shape, finalized request/response contracts, controller/service/repository separation, dependency direction |
| Java code conformity | 15 | `ESTD7`, `ESTD14`, `ESTD18` | Java style, null safety, immutability, package structure, naming, contextual collection/map names, folder placement |
| Persistence and data safety | 15 | `ESTD9`, `ESTD7` | repository access, transactions, indexes, schema ownership, query safety, migration awareness |
| Boundary validation and errors | 15 | `ESTD1`, `ESTD4`, `ESTD7` | trusted source selection, request validation, typed failures, exception boundaries, response contracts |
| Security and privacy | 10 | `ESTD1`, `ESTD4`, `ESTD9` | auth/authz, trust boundaries, permission boundaries, sensitive data handling, injection prevention, least privilege |
| Observability and resilience | 10 | `ESTD4`, `ESTD5`, `ESTD17` | logs, metrics, retries, circuit breakers, graceful degradation, processing flow |
| Testing and path coverage | 10 | `ESTD7`, `ESTD16` | unit/integration coverage, branch paths, Testcontainers where applicable, edge cases |
| PR and dependency evidence | 10 | `ESTD10`, `ESTD19` | review evidence, exception notes, release-close risk notes, Maven hygiene, dependency approval |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| API design and SEAM layering | `static.java.spotbugs`, `static.common.folder-structure` | SEAM layering, API contract, and service boundary intent |
| Java code conformity | `static.java.spotbugs`, `static.common.folder-structure` | framework-specific design judgment |
| Persistence and data safety | `static.java.spotbugs`, `static.common.semgrep` | transaction and schema ownership intent |
| Boundary validation and errors | `static.java.spotbugs`, `static.common.semgrep` | boundary completeness |
| Security and privacy | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep`, `static.java.spotbugs` | auth/authz and permission-boundary intent |
| Observability and resilience | `static.java.spotbugs` | resilience design sufficiency |
| Testing and path coverage | `static.java.spotbugs` | path intent and coverage adequacy |
| PR and dependency evidence | `static.common.report-consistency` | dependency approval context |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.java-seam-api` before each validator run.
- If SEAM gets a dedicated ESTD, make it a Source ESTD doc and rebalance groups.
- Keep route binding aligned with `route.java-seam-api`.
