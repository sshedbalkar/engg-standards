# ESTD Engineering Field Routing Map

## Purpose

Route Bingo engineering work to authoritative ESTD docs for LLM retrieval and on-demand validators.

- Source of truth stays in `docs/`.
- Resolve ESTD IDs through `context/doc-cards.md`.
- Use this map for route selection, not rule text duplication.
- Validator facets name what to check; exact rules come from routed docs.

## Lookup Strategy
- primary_lookup: route_id
- ordering: route_id
- jump_index: present
- entry_id_format: stable dot-delimited route ID

## Jump Index
- route.cloud-aws
- route.common
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

## Global Overlays

Apply these to most implementation validators unless the route says otherwise.

| Overlay | ESTD Docs | Validator Facets |
|:--------|:----------|:-----------------|
| common engineering baseline | `ESTD1` | code hygiene, documentation, error handling, validation, trust boundaries, permission boundaries, logging, configuration, security, testing |
| PR and review evidence | `ESTD10` | PR description, reviewer evidence, exception requests, migration notes, release-risk notes, merge readiness |
| naming | `ESTD14` | hierarchical names, identifiers, contextual collection/map names, files, modules, metrics, database names |
| path and unit testing strategy | `ESTD16` | path coverage, branch coverage, sad paths, edge cases, coverage intent |
| folder structure | `ESTD18` | root layout, test proximity, config layering, build artifact exclusion |
| dependency and coupling | `ESTD19` | dependency direction, abstraction boundaries, coupling anti-patterns |

## Routes

### route.cloud-aws
- Field: Cloud infrastructure and AWS resource development.
- Use when: change touches AWS, Terraform, networking, IAM, EC2, ALB, NLB, RDS, S3, CloudFront, WAF, Secrets Manager, SQS, SNS, Datadog, or cloud cost controls.
- Primary source docs: `ESTD5`, `ESTD8`.
- Supporting source docs: `ESTD1`, `ESTD4`, `ESTD9`, `ESTD10`, `ESTD13`, `ESTD18`, `ESTD19`.
- Validator facets: IaC, environment parity, least privilege, permission boundaries, network security, secrets, scaling, deployment safety, observability, backup, resilience, cost.
- Trigger keywords: AWS, Terraform, IAM, EC2, ALB, NLB, RDS, S3, CloudFront, WAF, Secrets Manager, SQS, SNS, Datadog, permission boundary, least privilege, over-provisioning, overprivileged, trust boundary.
- Known coverage notes: none.

### route.common
- Field: Cross-stack engineering baseline.
- Use when: change spans stacks or no narrower route is known.
- Primary source docs: `ESTD1`, `ESTD10`.
- Supporting source docs: `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`.
- Validator facets: documentation, naming, code hygiene, validation, trust boundaries, permission boundaries, security, testing, PR evidence, dependency coupling.
- Trigger keywords: common, shared, cross-stack, PR, review, late PR, release-close PR, release-risk, code freeze, standards exception, code hygiene, naming, testing, trust boundary, permission boundary, untrusted data, partially trusted data.
- Known coverage notes: none.

### route.database
- Field: Database design, access, migration, backup, and operations.
- Use when: change touches MySQL, MongoDB Atlas, schema design, indexes, queries, migrations, backfills, transactions, retention, or database permissions.
- Primary source docs: `ESTD9`.
- Supporting source docs: `ESTD1`, `ESTD4`, `ESTD5`, `ESTD6`, `ESTD7`, `ESTD8`, `ESTD10`, `ESTD14`, `ESTD16`, `ESTD18`.
- Validator facets: database selection, naming, data types, indexing, query safety, migrations, concurrency, access control, permission boundaries, retention, backup, performance.
- Trigger keywords: MySQL, MongoDB, Atlas, schema, migration, index, query, transaction, backfill, retention, RDS, read replica, permission boundary, least privilege, over-provisioning, overprivileged, untrusted data.
- Known coverage notes: none.

### route.internal-scripts
- Field: Internal CLI tools, scripts, and automation utilities.
- Use when: change touches shell scripts, non-shell scripts, Python CLIs, local automation, deploy automation, maintenance scripts, data processors, or repo helper tooling.
- Primary source docs: `ESTD1`, `ESTD16`, `ESTD18`.
- Supporting source docs: `ESTD10`, `ESTD14`, `ESTD17`, `ESTD19`.
- Validator facets: script guide evidence, shell/non-shell entrypoints, input validation, safe mutation, shell external-tool boundaries, API adapter boundaries, pure-logic separation, modularity threshold, testability, folder placement, naming, closeout proof, dependency coupling.
- Trigger keywords: script, CLI, shell, non-shell, Python, automation, deploy automation, maintenance tooling, processor, backfill utility, helper tool, script refactor, module split, CLI wrapper.
- Known coverage notes: No dedicated internal-scripts ESTD exists; folder structure and common standards provide the baseline.
- Style guide refs: `scripts/LLM_SHELL_SCRIPT_STYLE_GUIDE.md`, `scripts/LLM_NON_SHELL_SCRIPT_STYLE_GUIDE.md`.

### route.java-seam-api
- Field: Java SEAM microservice API development.
- Use when: change touches Java services, SEAM layers, service APIs, Maven dependencies, Java persistence, or service-owned schemas.
- Primary source docs: `ESTD4`, `ESTD7`, `ESTD9`.
- Supporting source docs: `ESTD1`, `ESTD5`, `ESTD10`, `ESTD14`, `ESTD16`, `ESTD17`, `ESTD18`, `ESTD19`.
- Validator facets: API design, finalized request/response contracts, stateless service design, trust boundaries, permission boundaries, Java style, null safety, SEAM layering, dependency direction, persistence, concurrency, observability, testing.
- Trigger keywords: Java, SEAM, microservice, API contract, request response, endpoint, Maven, service, controller, repository, schema, Testcontainers, BOM, trust boundary, permission boundary, untrusted data, partially trusted data, least privilege.
- Known coverage notes: none.

### route.jenkins-cicd
- Field: Jenkins CI/CD pipeline and build system development.
- Use when: change touches Jenkinsfiles, shared libraries, build agents, artifacts, signing, promotion, notifications, pipeline credentials, or build validation.
- Primary source docs: `ESTD13`.
- Supporting source docs: `ESTD1`, `ESTD5`, `ESTD8`, `ESTD10`, `ESTD11`, `ESTD18`, `ESTD19`.
- Validator facets: pipeline-as-code, shared libraries, secrets, artifacts, build identity, promotion gates, branch triggers, RBAC, agent hygiene, reporting.
- Trigger keywords: Jenkins, Jenkinsfile, pipeline, shared library, build agent, artifact, promotion, signing, coverage, SBOM.
- Known coverage notes: none.

### route.php-monolith
- Field: PHP legacy API monolith development.
- Use when: change touches PHP API handlers, monolith modules, PHP services, Composer dependencies, sessions, authentication, or PHP database access.
- Primary source docs: `ESTD4`, `ESTD6`, `ESTD9`.
- Supporting source docs: `ESTD1`, `ESTD5`, `ESTD10`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`.
- Validator facets: server authority, API contract, request/response shape, input validation, trust boundaries, permission boundaries, PHP typing, error handling, repository pattern, SQL safety, transactions, security, testing.
- Trigger keywords: PHP, monolith, API handler, API contract, request response, endpoint, PDO, Composer, session, auth, migration, MySQL, repository, trust boundary, permission boundary, untrusted data, partially trusted data, least privilege.
- Known coverage notes: none.

### route.product-website
- Field: Public product website for WebGL play, announcements, and community.
- Use when: change touches the product website, public web runtime, NestJS backend, website MySQL access, website deployment, or WebGL launch surface.
- Primary source docs: `ESTD11`, `ESTD5`, `ESTD8`, `ESTD9`, `ESTD13`.
- Supporting source docs: `ESTD1`, `ESTD4`, `ESTD10`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`.
- Validator facets: web architecture, API communication, no direct browser database access, trust boundaries, permission boundaries, auth where applicable, data handling, deployment, cloud security, database access, observability, testing.
- Trigger keywords: product website, public website, WebGL play, announcement, community, NestJS, NextJS, website MySQL, CDN, direct DB, public frontend, trust boundary, permission boundary, untrusted data, partially trusted data, least privilege.
- Known coverage notes: No separate public-product-website ESTD exists; route through web, cloud, database, server, and CI/CD standards.

### route.smartfox-server
- Field: SmartFox Server Java live-server development.
- Use when: change touches SmartFox extensions, rooms, handlers, real-time game state, player presence, live-server concurrency, or SmartFox build/deploy flow.
- Primary source docs: `ESTD4`, `ESTD7`, `ESTD12`, `ESTD9`.
- Supporting source docs: `ESTD1`, `ESTD10`, `ESTD13`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`.
- Validator facets: server authority, handler structure, input trust boundary, permission boundaries, room lifecycle, thread safety, idempotency, reconnect behavior, JVM memory, metrics, graceful shutdown, testing.
- Trigger keywords: SmartFox, SFS, extension, room, handler, real-time, presence, reconnect, sequence ID, JVM, live server, trust boundary, permission boundary, untrusted data, partially trusted data.
- Known coverage notes: none.

### route.spring-boot-api
- Field: Spring Boot banking service framework development.
- Use when: change touches Spring Boot controllers, services, Spring Data JPA repositories, entities, Flyway migrations, monetary or ledger logic, idempotency, schedulers, Kafka consumers, Spring Batch jobs, caching, or Maven dependencies in a Spring Boot service.
- Primary source docs: `ESTD20`.
- Supporting source docs: `ESTD10`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`, `ESTD21`.
- Validator facets: layering, dependency direction, typed configuration, constructor injection, API shape, boundary validation, error contract, transactions, optimistic locking, N+1, migrations, BigDecimal correctness, double-entry ledger, idempotency, outbox, scheduler locking, caching prohibitions, batch restartability, timeouts, circuit breakers, observability, testing, dependency hygiene.
- Trigger keywords: Spring Boot, Spring, @Transactional, @RestController, Spring Data JPA, Hibernate, Flyway, HikariCP, BigDecimal, ledger, double-entry, idempotency key, outbox, ShedLock, Resilience4j, Testcontainers, Actuator, PostgreSQL, banking service.
- Known coverage notes: `ESTD20` is self-contained and does not inherit `ESTD1` or `ESTD4`; do not route Spring Boot work through SEAM or PHP standards.

### route.spring-boot-security
- Field: Data protection, security, and audit for Spring Boot banking services.
- Use when: change touches security filter chains, JWT validation, authorization or ownership rules, encryption converters, masking, tokenization, secrets access, rate limiting, audit writes, retention, or privacy handling in a Spring Boot service.
- Primary source docs: `ESTD21`.
- Supporting source docs: `ESTD10`, `ESTD16`, `ESTD19`, `ESTD20`.
- Validator facets: trust boundaries, token validation, audience and issuer checks, deny-by-default, object-level authorization, four-eyes approval, data classification, encryption at rest, key custody, masking, tokenization, PCI scope, secrets lifecycle, injection defence, SSRF, deserialization, rate limiting, audit immutability, tamper evidence, retention, erasure, breach notification.
- Trigger keywords: Spring Security, OAuth2, resource server, JWT, JWKS, audience, @PreAuthorize, ownership, BOLA, masking, PAN, tokenization, PCI DSS, GDPR, DPDP, SOX, crypto-shredding, blind index, KMS, audit trail, four-eyes, maker-checker, step-up, SSRF, deserialization.
- Known coverage notes: `ESTD21` encodes engineering controls only; institutional compliance policy and assessor scoping decisions override it.

### route.technical-docs
- Field: Technical documents and ESTD document authoring.
- Use when: change touches TADs, ADRs, runbooks, RCAs, migration plans, ESTD templates, or standards documentation.
- Primary source docs: `ESTD15`, `ESTD0`.
- Supporting source docs: `ESTD1`, `ESTD10`.
- Validator facets: document type, metadata, goals, non-goals, risks, review path, approval, references, migration evidence.
- Trigger keywords: TAD, ADR, runbook, RCA, post-mortem, migration plan, template, technical document, ESTD authoring.
- Known coverage notes: none.

### route.unity-client
- Field: Unity client development for iOS, Android, Facebook, WebGL, and shared client code.
- Use when: change touches Unity, C#, client UX, assets, client networking, telemetry, mobile performance, or client security.
- Primary source docs: `ESTD2`, `ESTD3`.
- Supporting source docs: `ESTD1`, `ESTD4`, `ESTD10`, `ESTD13`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`.
- Validator facets: client architecture, client/server API contracts, request/response handling, UX, async flow, state management, C# style, Unity lifecycle, memory, performance, battery, build targets, testing.
- Trigger keywords: Unity, C#, MonoBehaviour, Addressables, PlayerPrefs, WebGL, iOS, Android, client, UI, asset, telemetry, API contract, request response.
- Known coverage notes: none.

### route.web-tools
- Field: Internal web tools, dashboards, and VPN-gated operational UIs.
- Use when: change touches NextJS/TypeScript internal tools, operational dashboards, auth-gated tool routes, player support tools, destructive actions, or tool deployment.
- Primary source docs: `ESTD11`.
- Supporting source docs: `ESTD1`, `ESTD4`, `ESTD5`, `ESTD8`, `ESTD9`, `ESTD10`, `ESTD13`, `ESTD14`, `ESTD16`, `ESTD18`, `ESTD19`.
- Validator facets: TypeScript strictness, runtime validation, API layer, no direct browser database access, trust boundaries, permission boundaries, auth, RBAC, PII handling, audit logging, UX, accessibility, deployment, testing.
- Trigger keywords: NextJS, TypeScript, React, Tailwind, internal tool, dashboard, RBAC, Cognito, audit log, PII, Zod, tools DB, direct DB, trust boundary, permission boundary, untrusted data, partially trusted data, least privilege.
- Known coverage notes: none.

## Route Selection Rules

- Pick the narrowest route that matches changed files, technologies, or review intent.
- If multiple routes match, include all matched primary docs and de-duplicate overlays.
- If a route has known coverage notes, treat them as routing caveats, not standards exceptions.
- For validators, emit findings against the source ESTD doc section after retrieval.
