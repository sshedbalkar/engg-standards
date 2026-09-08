# LLM Based Validation

## Purpose

LLM based validation is the semantic gap review layer of the ESTD gate.

- It runs after static validation.
- It reviews only unresolved validator groups.
- It retrieves source ESTD sections before producing findings.
- It emits `build/estd/llm-request.md` and, when invoked, `build/estd/llm-report.json`.
- It cannot override static failures or static passes.

Use LLM based validation for intent, architecture, UX, operational evidence, trade-off quality, route-specific applicability, and other judgments that deterministic tools cannot prove.

## Lookup Strategy
- primary_lookup: validator_route
- ordering: stable_id
- jump_index: present
- entry_id_format: stable dot-delimited ID

## Jump Index
- route.cloud-aws
- route.database
- route.internal-scripts
- route.java-seam-api
- route.jenkins-cicd
- route.php-monolith
- route.product-website
- route.smartfox-server
- route.spring-boot-api
- route.spring-boot-security
- route.technical-docs
- route.unity-client
- route.web-tools

## Source Files

| File | Role |
|:-----|:-----|
| `context/validators/*-validator.md` | Weighted route groups, ESTD sources, and semantic gap definitions |
| `tools/estd-enforcer/lib/estd_enforcer/llm.py` | LLM request construction and adapter execution |
| `tools/estd-enforcer/prompts/validation.md` | Hybrid validation contract for gap review |
| `tools/estd-enforcer/prompts/report-json.md` | JSON output contract |
| `tools/estd-enforcer/schema/report.schema.json` | Machine-readable report schema |

## Update Rule

Update this file whenever any of these change:

- a validator group is added, removed, renamed, reweighted, or reclassified in `context/validators/*-validator.md`
- a validator group's ESTD sources, focus, or LLM gap changes
- LLM request construction changes in `tools/estd-enforcer/lib/estd_enforcer/llm.py`
- report shape, citation rules, scoring, unknown-evidence handling, or gate semantics change

`./scripts/check-context.sh` verifies that every validator group name appears in this file.

## Invocation Semantics

- LLM review runs only when unresolved validator groups remain and `llmPolicy` is `gaps-only`.
- The request includes selected routes, route validator files, source ESTD docs to retrieve, unresolved validator groups, authoritative static findings, and files in scope.
- The LLM must evaluate only unresolved groups listed in the request.
- Non-applicable groups are removed from the denominator.
- Unknown evidence fails until resolved against exact source ESTD sections.
- Critical security, data-loss, auth-bypass, or production-safety blockers fail even if aggregate score is above the threshold.
- The LLM output must be JSON conforming to `tools/estd-enforcer/schema/report.schema.json`.

## LLM Finding Contract

Every LLM finding must:

- cite exact `ESTD` doc ID and section
- name file and line when available
- explain concrete engineering risk
- recommend the smallest sustainable fix
- mark evidence as `known` or `unknown`
- preserve static findings as authoritative

## LLM Validation Inventory

### `validator.cloud-aws`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Environment and IaC shape | 15 | `ESTD5`, `ESTD8`, `ESTD18` | environment parity, Terraform/source control, module placement, config separation; resolves environment strategy intent |
| IAM, secrets, and identity | 20 | `ESTD1`, `ESTD5`, `ESTD8` | least privilege, permission boundaries, over-provisioning risk, secret storage, credential rotation, Okta/IAM boundaries; resolves least-privilege and permission-boundary judgment |
| Network and edge security | 15 | `ESTD5`, `ESTD8` | VPC, security groups, HTTPS, WAF, load balancers, CDN boundaries; resolves network exposure intent |
| Data, backup, and retention | 10 | `ESTD8`, `ESTD9` | RDS/S3 safety, backups, encryption, restore evidence, data retention; resolves restore and retention adequacy |
| Deployment and promotion safety | 15 | `ESTD5`, `ESTD8`, `ESTD13` | Dev/QA/Staging/Production gates, rollback, immutable artifacts, approvals; resolves promotion strategy and approval context |
| Observability, resilience, and cost | 15 | `ESTD1`, `ESTD5`, `ESTD8` | metrics, alarms, graceful degradation, scaling, cost controls; resolves resilience and cost trade-offs |
| PR and exception evidence | 10 | `ESTD10`, `ESTD19` | terraform plan evidence, destructive-change callouts, release-close risk notes, coupling and approval notes; resolves destructive-change evidence quality |

### `validator.database`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Schema and model design | 15 | `ESTD9`, `ESTD14` | data model fit, naming, contextual collection/map names, data types, ownership, retention readiness; resolves schema fit and data-model intent |
| Query and access safety | 15 | `ESTD9`, `ESTD6`, `ESTD7` | parameterized access, repository boundaries, transaction use, injection prevention; resolves repository and transaction intent |
| Migrations and backfills | 20 | `ESTD9`, `ESTD10`, `ESTD16` | expand-contract safety, rollback, production-sized validation, path coverage; resolves expand-contract and rollout safety |
| Security and permissions | 15 | `ESTD1`, `ESTD4`, `ESTD8`, `ESTD9` | least privilege, permission boundaries, over-privileged user risk, sensitive data handling, auditability, backup access; resolves database permission boundary intent |
| Performance and operability | 15 | `ESTD5`, `ESTD8`, `ESTD9` | indexes, query plans, locking, replication, monitoring, restore readiness; resolves index and query-plan adequacy |
| Testing and evidence | 10 | `ESTD9`, `ESTD16`, `ESTD10` | migration tests, staging verification, execution estimates, release-close risk notes, review evidence; resolves staging evidence quality |
| Folder and config hygiene | 10 | `ESTD18`, `ESTD14` | migration placement, config layering, generated artifact exclusion, naming; resolves naming intent where ambiguous |

### `validator.internal-scripts`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Guide selection and entrypoints | 15 | `ESTD1`, `ESTD18` | shell or non-shell guide evidence, clear purpose, file placement, executable boundaries, generated artifact exclusion; resolves guide-specific compliance and command ergonomics |
| Input validation and safe mutation | 15 | `ESTD1`, `ESTD16` | required args, safe defaults, destructive-action guards, parameter validation, shell quoting, strict mode, temp files, traps, cleanup; resolves destructive-action and safe mutation intent |
| External adapters and command boundaries | 15 | `ESTD1`, `ESTD17` | API adapters, shell external tools, dependency checks, timeouts, bounded output, redacted diagnostics, no secret logging; resolves adapter and external tool boundary clarity |
| Modularity and data flow | 20 | `ESTD17`, `ESTD19` | modularity threshold, pure logic versus I/O, no large script growth without review or structure-debt note, staged processing, restartability; resolves modularity threshold and structure debt |
| Testing and repeatable checks | 15 | `ESTD16` | happy/sad/edge paths, dry-run coverage, mocked adapters, fixture use, repeatable checks; resolves path intent and coverage adequacy |
| Naming and discoverability | 10 | `ESTD14`, `ESTD18` | command names, folder names, config names, contextual collection/map names, README links; resolves naming clarity |
| Closeout and operational evidence | 10 | `ESTD10` | guide consulted, tests and checks run, remaining structure debt, review evidence, rollback notes, exception approval, runbook impact; resolves closeout proof and rollback evidence |

### `validator.java-seam-api`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| API design and SEAM layering | 15 | `ESTD4`, `ESTD7`, `ESTD19` | service boundaries, trust boundaries, stateless API shape, finalized request/response contracts, controller/service/repository separation, dependency direction; resolves SEAM layering, API contract, and service boundary intent |
| Java code conformity | 15 | `ESTD7`, `ESTD14`, `ESTD18` | Java style, null safety, immutability, package structure, naming, contextual collection/map names, folder placement; resolves framework-specific design judgment |
| Persistence and data safety | 15 | `ESTD9`, `ESTD7` | repository access, transactions, indexes, schema ownership, query safety, migration awareness; resolves transaction and schema ownership intent |
| Boundary validation and errors | 15 | `ESTD1`, `ESTD4`, `ESTD7` | trusted source selection, request validation, typed failures, exception boundaries, response contracts; resolves boundary completeness |
| Security and privacy | 10 | `ESTD1`, `ESTD4`, `ESTD9` | auth/authz, trust boundaries, permission boundaries, sensitive data handling, injection prevention, least privilege; resolves auth/authz and permission-boundary intent |
| Observability and resilience | 10 | `ESTD4`, `ESTD5`, `ESTD17` | logs, metrics, retries, circuit breakers, graceful degradation, processing flow; resolves resilience design sufficiency |
| Testing and path coverage | 10 | `ESTD7`, `ESTD16` | unit/integration coverage, branch paths, Testcontainers where applicable, edge cases; resolves path intent and coverage adequacy |
| PR and dependency evidence | 10 | `ESTD10`, `ESTD19` | review evidence, exception notes, release-close risk notes, Maven hygiene, dependency approval; resolves dependency approval context |

### `validator.jenkins-cicd`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Pipeline source and reuse | 15 | `ESTD13`, `ESTD18`, `ESTD19` | root Jenkinsfile, shared libraries, no duplicated orchestration, clear entrypoints; resolves shared-library design intent |
| Secrets and build identity | 20 | `ESTD1`, `ESTD8`, `ESTD13` | no checked-in secrets, credentials binding, signing materials, build metadata; resolves credential boundary judgment |
| Build, test, and artifacts | 15 | `ESTD10`, `ESTD13` | lint/test/build stages, BOM scan, immutable artifacts, reports, retention; resolves artifact and evidence sufficiency |
| Promotion gates and rollback | 15 | `ESTD5`, `ESTD8`, `ESTD13` | environment promotion, approvals, release-close risk notes, rollback notes, artifact reuse; resolves approval and rollback intent |
| Agents, RBAC, and audit | 15 | `ESTD13` | agent hygiene, controller safety, plugin approval, RBAC, audit logging; resolves RBAC and audit adequacy |
| Reporting and notifications | 10 | `ESTD10`, `ESTD13` | failure routing, archived evidence, build links, actionable messages; resolves routing usefulness |
| Maintainability and safety | 10 | `ESTD1`, `ESTD13`, `ESTD19` | declarative style, parameter validation, simple Groovy, testable helper logic; resolves Groovy maintainability judgment |

### `validator.php-monolith`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Server architecture and API shape | 15 | `ESTD4`, `ESTD19` | server authority, stateless API behavior where applicable, finalized API contracts, request/response shapes, URL/method/status/version rules, service boundaries; resolves API contract and service design intent |
| PHP code conformity | 15 | `ESTD6`, `ESTD14`, `ESTD18` | PHP version/config, PSR-12, types, class/file organization, naming, contextual collection/map names, Composer hygiene; resolves legacy-pattern acceptability |
| Boundary validation and error handling | 15 | `ESTD1`, `ESTD4`, `ESTD6` | boundary functions, trusted source selection, input validation, sanitization, exception hierarchy, top-level handling; resolves boundary completeness |
| Database access and migrations | 15 | `ESTD9`, `ESTD6` | repository pattern, parameterized queries, transactions, indexes, migration/backfill safety; resolves migration safety and transaction intent |
| Security and privacy | 15 | `ESTD1`, `ESTD4`, `ESTD6`, `ESTD9` | auth/session rules, untrusted data risk, password/hash handling, injection prevention, permission boundaries, sensitive data logging; resolves auth/session and permission-boundary intent |
| Performance and operability | 10 | `ESTD1`, `ESTD4`, `ESTD5` | caching, rate limits, observability, config, deployment safety, graceful degradation; resolves caching and operability sufficiency |
| Testing and path coverage | 10 | `ESTD6`, `ESTD16` | PHPUnit coverage, boundary cases, guard clauses, economic operations, path intent; resolves path intent and coverage adequacy |
| PR and maintenance evidence | 5 | `ESTD10` | PR evidence, exception request, migration notes, release-close risk notes, rollout/rollback notes; resolves PR evidence quality |

### `validator.product-website`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Web architecture and TypeScript | 15 | `ESTD11`, `ESTD14`, `ESTD18` | project structure, strict TypeScript, component boundaries, naming, contextual collection/map names, folder layout; resolves architecture and component boundary intent |
| Public UX and WebGL launch surface | 10 | `ESTD11`, `ESTD1` | loading/error states, accessibility, localization readiness, WebGL entry behavior, user-impact safeguards; resolves UX completeness and player impact |
| API and backend boundaries | 15 | `ESTD4`, `ESTD9`, `ESTD11`, `ESTD19` | centralized API layer, no direct browser-to-database access, trust boundaries, permission boundaries, request/response contracts, validation, service boundaries, dependency direction; resolves API contract, trust, and database boundary intent |
| Data and persistence | 10 | `ESTD9` | MySQL schema/query safety, migrations, indexes, retention, permissions, over-privileged DB risk; resolves schema and migration intent |
| Cloud and edge deployment | 15 | `ESTD5`, `ESTD8` | environments, HTTPS, CDN, WAF, secrets, network and permission boundaries, observability, cost controls; resolves edge deployment trade-offs |
| CI/CD and release safety | 10 | `ESTD13`, `ESTD10` | build/test pipeline, artifact identity, promotion gates, release-close risk notes, rollback notes, review evidence; resolves release evidence quality |
| Security and privacy | 15 | `ESTD1`, `ESTD4`, `ESTD5`, `ESTD8`, `ESTD11` | auth where applicable, trust boundaries, permission boundaries, sensitive data handling, dependency security, transport security, auditability; resolves auth/privacy and permission-boundary intent |
| Testing and path coverage | 10 | `ESTD16`, `ESTD11` | unit/integration coverage, branch paths, edge cases, UI states, deployment validation; resolves path intent and coverage adequacy |

### `validator.smartfox-server`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| SmartFox architecture and authority | 15 | `ESTD4`, `ESTD12`, `ESTD19` | API authority, extension decomposition, handler pattern, dependency direction; resolves real-time authority and room design |
| Java code conformity | 10 | `ESTD7`, `ESTD14`, `ESTD18` | Java 17, immutability, package structure, null safety, naming, contextual collection/map names, folder layout; resolves SmartFox-specific style judgment |
| Room lifecycle and concurrency | 20 | `ESTD12`, `ESTD7`, `ESTD4` | state machine, thread safety, lock discipline, scheduled tasks, concurrent collections; resolves lifecycle and lock discipline |
| Real-time protocol resilience | 15 | `ESTD12`, `ESTD4` | sequencing, idempotency, reconnect snapshots, latency strategy, mixed-client compatibility; resolves reconnect and idempotency intent |
| API, persistence, and data safety | 10 | `ESTD4`, `ESTD9`, `ESTD12` | authoritative API calls, retries, persistence checkpoints, repository/query safety; resolves checkpoint and retry strategy |
| Security and abuse controls | 10 | `ESTD1`, `ESTD4`, `ESTD12` | join validation, session handling, input trust boundary, permission boundaries, SmartFox vulnerability coverage; resolves trust-boundary and abuse-control adequacy |
| Observability, memory, and shutdown | 10 | `ESTD12`, `ESTD13` | logs, metrics, JVM tuning, leak prevention, graceful shutdown/restart, build pipeline; resolves shutdown and leak-risk sufficiency |
| Testing and PR evidence | 10 | `ESTD12`, `ESTD16`, `ESTD10` | engine isolation tests, win pattern coverage, path coverage, release-close risk notes, review evidence; resolves path coverage and review evidence |

### `validator.spring-boot-api`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Spring layering and API design | 15 | `ESTD20`, `ESTD19` | package layout, layer responsibilities, dependency direction, entity never crossing the controller boundary, URL and versioning shape, status code selection, pagination caps; resolves Spring layering, API contract, and boundary intent |
| Configuration and bean design | 10 | `ESTD20`, `ESTD18` | typed configuration properties, profile and secret separation, component scan scope, constructor injection, stateless singletons, no circular references; resolves configuration ownership and bean lifecycle judgment |
| Persistence and transactions | 15 | `ESTD20`, `ESTD9` | lazy associations, optimistic locking, open-in-view disabled, N+1 avoidance, Flyway migration hygiene, expand-contract, transaction boundary placement, self-invocation, remote calls inside transactions; resolves transaction boundary and migration safety intent |
| Money and data integrity | 20 | `ESTD20` | BigDecimal usage and scale, banker's rounding, currency pairing, append-only double-entry ledger, balance as projection, idempotency store, database-level invariants, temporal correctness; resolves monetary correctness and ledger invariant intent |
| Boundary validation and errors | 15 | `ESTD20`, `ESTD21` | boundary validation completeness, unknown-property rejection, custom domain constraints, exception hierarchy, global handler coverage, error code catalogue, no internal detail in responses; resolves validation completeness and error disclosure judgment |
| Async, messaging, batch, and caching | 10 | `ESTD20`, `ESTD17` | bounded executors, distributed scheduler locks, transactional outbox, idempotent consumers, dead-letter routing, cache prohibitions and TTLs, batch restartability and reconciliation; resolves delivery guarantee and job safety intent |
| Observability and resilience | 10 | `ESTD20` | correlation propagation, structured logging discipline, metric set and cardinality, timeouts on outbound calls, circuit breaker fail-closed behavior, health and readiness separation; resolves resilience posture and signal sufficiency |
| Testing and dependency evidence | 5 | `ESTD16`, `ESTD10`, `ESTD19` | slice and Testcontainers coverage, concurrency and rollback tests, branch coverage on money paths, SBOM and CVE gating, pinned versions, PR review evidence; resolves coverage adequacy and dependency approval context |

### `validator.spring-boot-security`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Authentication and token validation | 15 | `ESTD21` | resource server configuration, algorithm allowlist, issuer and audience validation, clock skew bounds, JWKS caching, principal derived only from the validated token; resolves token trust boundary and issuer intent |
| Authorization and ownership | 15 | `ESTD21`, `ESTD20` | deny-by-default matcher order, service-layer method security, scope and role separation, ownership enforced in the query, 404 over 403, four-eyes approval on high-risk operations; resolves object-level authorization and approval intent |
| Data classification and encryption | 20 | `ESTD21` | field classification coverage, column-level encryption, envelope encryption and key custody, IV and mode selection, blind index usage, key rotation readiness, backup key separation; resolves classification coverage and key custody judgment |
| Masking, tokenization, and PCI scope | 15 | `ESTD21` | PAN and account masking at the response boundary, tokenization boundary, prohibited data never persisted, cardholder data environment scope decisions; resolves disclosure surface and PCI scope judgment |
| Secrets management | 10 | `ESTD21` | no secrets in configuration or source, secrets manager retrieval, rotation readiness, secret handling in memory, heap dump and actuator exposure; resolves secret lifecycle and exposure judgment |
| Input and injection security | 10 | `ESTD21` | parameterized queries, dynamic sort and field allowlists, path traversal containment, SSRF address validation, XXE hardening, deserialization prohibition, upload controls, mass assignment; resolves injection reachability and allowlist adequacy |
| Audit trail and SOX evidence | 10 | `ESTD21` | audited event coverage including reads, record completeness, database-level immutability, tamper evidence chain, audit write propagation on failure, retention; resolves audit completeness and immutability intent |
| Privacy and retention | 5 | `ESTD21` | personal data kept out of the ledger, erasure and crypto-shredding path, retention schedule enforcement, cross-border transfer constraints, consent records; resolves erasure feasibility and retention basis |

### `validator.technical-docs`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Document type and metadata | 15 | `ESTD15`, `ESTD0` | correct template, title, owner, status, dates, audience, lifecycle; resolves template completeness |
| Goals, scope, and decisions | 15 | `ESTD15`, `ESTD1` | goals, non-goals, context, decision clarity, trade-offs; resolves decision clarity and trade-offs |
| Design, risks, and operations | 20 | `ESTD15`, `ESTD1` | architecture, finalized API contract tables/examples, risks, rollback, monitoring, support impact, security/privacy notes; resolves API contract, risk, and operational adequacy |
| References and traceability | 15 | `ESTD0`, `ESTD15` | source links, ESTD references, section links, dependency clarity; resolves reference relevance |
| Review and approval path | 15 | `ESTD10`, `ESTD15` | reviewers, approvals, exception handling, release-close risk notes, PR evidence; resolves approval context |
| Migration and validation evidence | 10 | `ESTD15`, `ESTD16` | test plan, rollout plan, verification, backout, path coverage; resolves validation adequacy |
| Formatting and maintainability | 10 | `ESTD0`, `ESTD15` | headings, TOC readiness, concise structure, boilerplate preservation; resolves prose quality |

### `validator.unity-client`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| Client architecture and state | 15 | `ESTD2`, `ESTD19` | separation of concerns, server-authoritative state, explicit state flow, dependency direction; resolves architecture intent, dependency direction |
| Unity and C# code style | 15 | `ESTD3`, `ESTD14`, `ESTD18` | C# style, class/file organization, lifecycle use, naming, contextual collection/map names, folder placement; resolves Unity lifecycle appropriateness |
| Async, networking, and resilience | 15 | `ESTD2`, `ESTD4`, `ESTD1` | centralized service layer, API contract consumption, request/response handling, cancellation, timeout, dedupe, reconnect, degraded network behavior; resolves API contract consumption and degraded-network behavior |
| UX, accessibility, and localization | 10 | `ESTD2` | loading/error states, safe areas, responsive UI, destructive-action safeguards, accessibility, text readiness; resolves UX completeness and player impact |
| Security and privacy | 10 | `ESTD1`, `ESTD2` | trust boundary, token handling, certificate pinning, anti-cheat awareness, build security; resolves trust-boundary intent |
| Performance, memory, and battery | 15 | `ESTD2`, `ESTD3` | hot paths, allocations, Addressables lifecycle, leaks, rendering, battery, profiling evidence; resolves runtime impact and profiling sufficiency |
| Testing and path coverage | 10 | `ESTD3`, `ESTD16` | unit-testable logic, Unity test runner, happy/sad/edge paths, coverage intent; resolves path intent and coverage adequacy |
| Build, PR, and release evidence | 10 | `ESTD10`, `ESTD13` | build target rules, validation evidence, screenshots/videos, release-close risk notes, pipeline readiness; resolves PR evidence quality |

### `validator.web-tools`

| Group | Weight | ESTD Sources | LLM Validates |
|:------|:-------|:-------------|:--------------|
| TypeScript and React conformity | 15 | `ESTD11`, `ESTD14`, `ESTD18` | strict TypeScript, no unsafe `any`, runtime validation, component design, naming, contextual collection/map names, folder layout; resolves component design intent |
| Tool API integration | 10 | `ESTD11`, `ESTD4`, `ESTD9`, `ESTD19` | centralized API layer, no direct browser-to-database access, untrusted tool input, request validation, response handling, dependency boundaries; resolves API, trust, and database boundary judgment |
| Auth, authorization, and access control | 15 | `ESTD11`, `ESTD1`, `ESTD5`, `ESTD8` | authenticated routes, RBAC, permission boundaries, Cognito/IAM alignment, least privilege, session timeout; resolves RBAC and access-flow intent |
| Sensitive actions and auditability | 15 | `ESTD11`, `ESTD9`, `ESTD10` | PII display, destructive action confirmation, before/after review, audit logs, migration notes; resolves operational risk judgment |
| UX, accessibility, and operability | 15 | `ESTD11` | shared components, loading/error states, accessibility, text readiness, operational task completion; resolves UX completeness and task ergonomics |
| Deployment and environment safety | 10 | `ESTD11`, `ESTD13`, `ESTD5`, `ESTD8` | Jenkins build/deploy, environments, release-close risk notes, rollback, timing, secrets, monitoring; resolves deployment evidence quality |
| Testing and path coverage | 10 | `ESTD11`, `ESTD16` | unit/integration tests, UI states, guard clauses, edge cases, coverage intent; resolves path intent and coverage adequacy |
| Security and dependency hygiene | 10 | `ESTD1`, `ESTD11`, `ESTD19` | dependency rules, supply-chain checks, input trust boundary, permission boundaries, sensitive logging, coupling; resolves dependency/coupling and permission-boundary intent |
