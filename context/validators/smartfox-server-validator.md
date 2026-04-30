# validator.smartfox-server

- Validator ID: `validator.smartfox-server`
- Route: `route.smartfox-server`
- Source docs: `ESTD4`, `ESTD7`, `ESTD12`, `ESTD9`
- Overlay docs: `ESTD1`, `ESTD10`, `ESTD13`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`
- Applies to: SmartFox Java extensions, handlers, rooms, player presence, live-state transitions, real-time messaging, JVM runtime concerns.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| SmartFox architecture and authority | 15 | `ESTD4`, `ESTD12`, `ESTD19` | API authority, extension decomposition, handler pattern, dependency direction |
| Java code conformity | 10 | `ESTD7`, `ESTD14`, `ESTD18` | Java 17, immutability, package structure, null safety, naming, contextual collection/map names, folder layout |
| Room lifecycle and concurrency | 20 | `ESTD12`, `ESTD7`, `ESTD4` | state machine, thread safety, lock discipline, scheduled tasks, concurrent collections |
| Real-time protocol resilience | 15 | `ESTD12`, `ESTD4` | sequencing, idempotency, reconnect snapshots, latency strategy, mixed-client compatibility |
| API, persistence, and data safety | 10 | `ESTD4`, `ESTD9`, `ESTD12` | authoritative API calls, retries, persistence checkpoints, repository/query safety |
| Security and abuse controls | 10 | `ESTD1`, `ESTD4`, `ESTD12` | join validation, session handling, input trust boundary, permission boundaries, SmartFox vulnerability coverage |
| Observability, memory, and shutdown | 10 | `ESTD12`, `ESTD13` | logs, metrics, JVM tuning, leak prevention, graceful shutdown/restart, build pipeline |
| Testing and PR evidence | 10 | `ESTD12`, `ESTD16`, `ESTD10` | engine isolation tests, win pattern coverage, path coverage, release-close risk notes, review evidence |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| SmartFox architecture and authority | `static.java.spotbugs`, `static.common.folder-structure` | real-time authority and room design |
| Java code conformity | `static.java.spotbugs`, `static.common.folder-structure` | SmartFox-specific style judgment |
| Room lifecycle and concurrency | `static.java.spotbugs`, `static.common.semgrep` | lifecycle and lock discipline |
| Real-time protocol resilience | `static.java.spotbugs` | reconnect and idempotency intent |
| API, persistence, and data safety | `static.java.spotbugs`, `static.common.semgrep` | checkpoint and retry strategy |
| Security and abuse controls | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | trust-boundary and abuse-control adequacy |
| Observability, memory, and shutdown | `static.java.spotbugs` | shutdown and leak-risk sufficiency |
| Testing and PR evidence | `static.common.report-consistency` | path coverage and review evidence |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve SmartFox route docs when live-server standards change.
- If Java or SmartFox standards split further, keep SmartFox-specific checks in Source docs.
- Keep route binding aligned with `route.smartfox-server`.
