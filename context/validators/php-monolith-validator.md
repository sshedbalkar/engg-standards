# validator.php-monolith

- Validator ID: `validator.php-monolith`
- Route: `route.php-monolith`
- Source docs: `ESTD4`, `ESTD6`, `ESTD9`
- Overlay docs: `ESTD1`, `ESTD5`, `ESTD10`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`
- Applies to: PHP legacy API monolith code, handlers, services, sessions, Composer dependencies, MySQL access, maintenance changes.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Server architecture and API shape | 15 | `ESTD4`, `ESTD19` | server authority, stateless API behavior where applicable, finalized API contracts, request/response shapes, URL/method/status/version rules, service boundaries |
| PHP code conformity | 15 | `ESTD6`, `ESTD14`, `ESTD18` | PHP version/config, PSR-12, types, class/file organization, naming, contextual collection/map names, Composer hygiene |
| Boundary validation and error handling | 15 | `ESTD1`, `ESTD4`, `ESTD6` | boundary functions, trusted source selection, input validation, sanitization, exception hierarchy, top-level handling |
| Database access and migrations | 15 | `ESTD9`, `ESTD6` | repository pattern, parameterized queries, transactions, indexes, migration/backfill safety |
| Security and privacy | 15 | `ESTD1`, `ESTD4`, `ESTD6`, `ESTD9` | auth/session rules, untrusted data risk, password/hash handling, injection prevention, permission boundaries, sensitive data logging |
| Performance and operability | 10 | `ESTD1`, `ESTD4`, `ESTD5` | caching, rate limits, observability, config, deployment safety, graceful degradation |
| Testing and path coverage | 10 | `ESTD6`, `ESTD16` | PHPUnit coverage, boundary cases, guard clauses, economic operations, path intent |
| PR and maintenance evidence | 5 | `ESTD10` | PR evidence, exception request, migration notes, release-close risk notes, rollout/rollback notes |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Server architecture and API shape | `static.common.folder-structure` | API contract and service design intent |
| PHP code conformity | `static.php.phpstan`, `static.common.folder-structure` | legacy-pattern acceptability |
| Boundary validation and error handling | `static.php.phpstan`, `static.common.semgrep` | boundary completeness |
| Database access and migrations | `static.common.semgrep` | migration safety and transaction intent |
| Security and privacy | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | auth/session and permission-boundary intent |
| Performance and operability | `static.common.semgrep` | caching and operability sufficiency |
| Testing and path coverage | `static.php.phpstan` | path intent and coverage adequacy |
| PR and maintenance evidence | `static.common.report-consistency` | PR evidence quality |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Recheck PHP route docs before each run; legacy maintenance standards may move into new ESTDs.
- If database or migration standards evolve, update database group sources and weight only after ESTD changes.
- Keep route binding aligned with `route.php-monolith`.
