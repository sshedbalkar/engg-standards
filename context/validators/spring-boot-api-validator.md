# validator.spring-boot-api

- Validator ID: `validator.spring-boot-api`
- Route: `route.spring-boot-api`
- Source docs: `ESTD20`
- Overlay docs: `ESTD10`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`, `ESTD21`
- Applies to: Spring Boot 3.3+ banking services — controllers, services, repositories, JPA entities, Flyway migrations, monetary and ledger logic, schedulers, consumers, batch jobs, and Maven dependencies.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Spring layering and API design | 15 | `ESTD20`, `ESTD19` | package layout, layer responsibilities, dependency direction, entity never crossing the controller boundary, URL and versioning shape, status code selection, pagination caps |
| Configuration and bean design | 10 | `ESTD20`, `ESTD18` | typed configuration properties, profile and secret separation, component scan scope, constructor injection, stateless singletons, no circular references |
| Persistence and transactions | 15 | `ESTD20`, `ESTD9` | lazy associations, optimistic locking, open-in-view disabled, N+1 avoidance, Flyway migration hygiene, expand-contract, transaction boundary placement, self-invocation, remote calls inside transactions |
| Money and data integrity | 20 | `ESTD20` | BigDecimal usage and scale, banker's rounding, currency pairing, append-only double-entry ledger, balance as projection, idempotency store, database-level invariants, temporal correctness |
| Boundary validation and errors | 15 | `ESTD20`, `ESTD21` | boundary validation completeness, unknown-property rejection, custom domain constraints, exception hierarchy, global handler coverage, error code catalogue, no internal detail in responses |
| Async, messaging, batch, and caching | 10 | `ESTD20`, `ESTD17` | bounded executors, distributed scheduler locks, transactional outbox, idempotent consumers, dead-letter routing, cache prohibitions and TTLs, batch restartability and reconciliation |
| Observability and resilience | 10 | `ESTD20` | correlation propagation, structured logging discipline, metric set and cardinality, timeouts on outbound calls, circuit breaker fail-closed behavior, health and readiness separation |
| Testing and dependency evidence | 5 | `ESTD16`, `ESTD10`, `ESTD19` | slice and Testcontainers coverage, concurrency and rollback tests, branch coverage on money paths, SBOM and CVE gating, pinned versions, PR review evidence |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Spring layering and API design | `static.java.spotbugs`, `static.common.folder-structure` | Spring layering, API contract, and boundary intent |
| Configuration and bean design | `static.java.spotbugs`, `static.common.secrets` | configuration ownership and bean lifecycle judgment |
| Persistence and transactions | `static.java.spotbugs`, `static.common.semgrep` | transaction boundary and migration safety intent |
| Money and data integrity | `static.java.spotbugs`, `static.common.semgrep` | monetary correctness and ledger invariant intent |
| Boundary validation and errors | `static.java.spotbugs`, `static.common.semgrep` | validation completeness and error disclosure judgment |
| Async, messaging, batch, and caching | `static.java.spotbugs` | delivery guarantee and job safety intent |
| Observability and resilience | `static.java.spotbugs` | resilience posture and signal sufficiency |
| Testing and dependency evidence | `static.common.report-consistency` | coverage adequacy and dependency approval context |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.spring-boot-api` before each validator run.
- Keep security, privacy, and audit findings on `validator.spring-boot-security`; do not duplicate them here.
- If a Spring Boot service adopts a stack outside `ESTD20` baseline versions, rebalance groups before running.
- Keep route binding aligned with `route.spring-boot-api`.
