# Static Validation

## Purpose

Static validation is the deterministic first pass of the ESTD gate.

- It runs before LLM review.
- It uses built-in checks and command adapters.
- It emits `build/estd/static-report.json`.
- It feeds normalized `staticResults` into `build/estd/report.json`.
- Static failures are authoritative and cannot be overridden by LLM output.

Use static validation for checks that can be decided from files, configured tools, route coverage, command output, or fixed safety patterns.

## Lookup Strategy
- primary_lookup: static_check_id or validator_route
- ordering: stable_id
- jump_index: present
- entry_id_format: stable dot-delimited ID

## Jump Index
- static.cloud
- static.common
- static.java
- static.jenkins
- static.php
- static.unity
- static.web
- route.cloud-aws
- route.database
- route.internal-scripts
- route.java-seam-api
- route.jenkins-cicd
- route.php-monolith
- route.product-website
- route.smartfox-server
- route.technical-docs
- route.unity-client
- route.web-tools

## Source Files

| File | Role |
|:-----|:-----|
| `tools/estd-enforcer/static-checks/registry.json` | Registered static check IDs, routes, commands, severity, and ESTD citations |
| `tools/estd-enforcer/lib/estd_enforcer/static_runner.py` | Registry loading, applicability, command execution, static score |
| `tools/estd-enforcer/lib/estd_enforcer/standard_types/common.py` | Built-in deterministic checks |
| `context/validators/*-validator.md` | Route group to static check mapping in each Static Coverage table |

## Update Rule

Update this file whenever any of these change:

- a check is added, removed, renamed, or recategorized in `tools/estd-enforcer/static-checks/registry.json`
- built-in check behavior changes in `tools/estd-enforcer/lib/estd_enforcer/standard_types/common.py`
- command applicability, required-tool behavior, or static scoring changes in `tools/estd-enforcer/lib/estd_enforcer/static_runner.py`
- a Static Coverage table changes in any `context/validators/*-validator.md`

`./scripts/check-context.sh` verifies that every registered static check ID and every validator group name appears in this file.

## Execution Semantics

- A static check runs when its route is `route.common` or intersects the selected route list.
- Command checks are applicable when their configured file patterns exist or scoped files match their suffix list.
- Missing optional command tools produce `skipped`; unresolved validator groups continue to LLM gap review.
- Missing required command tools produce `error` and exit the enforcer with tool error status.
- `not-applicable` and `skipped` checks are removed from static score calculation.
- Static score is `passed applicable checks / total applicable checks * 100`.
- Static findings must cite ESTD docs and sections when they represent a standards finding.

## Built-In Static Validations

| Static Check ID | Classification | Validates | Failure Behavior |
|:----------------|:---------------|:----------|:-----------------|
| `static.common.config` | config contract | enforcer config is parseable and accepted by the CLI config layer | tool error occurs before static run if config is invalid |
| `static.common.folder-structure` | source hygiene | scoped files do not include generated or dependency output under `build/`, `node_modules/`, `.next/`, `Library/`, or `Temp/` | medium finding against `ESTD18` section `2.1` |
| `static.common.report-consistency` | report merge guard | report consistency is reserved for merge/report construction | currently passes; merge validation happens after static and LLM reports are combined |
| `static.common.route-coverage` | route coverage | every selected route has a route-bound validator spec in `context/validators/` | critical finding against `ESTD1` section `30` |
| `static.common.secrets` | secret pattern scan | scoped text files do not contain private keys, secret keys, API keys, client secrets, or password-like assignments | critical finding against `ESTD1` section `19` |

## Command Static Validations

| Static Check ID | Classification | Routes | Command | ESTD Citation | Validates |
|:----------------|:---------------|:-------|:--------|:--------------|:----------|
| `static.cloud.checkov` | IaC security scan | `route.cloud-aws` | `checkov -d . --quiet` | `ESTD5` section `2.7` | cloud and Terraform security policy issues |
| `static.cloud.terraform-validate` | Terraform validation | `route.cloud-aws` | `terraform validate -no-color` | `ESTD8` section `2.2` | Terraform configuration validity |
| `static.common.gitleaks` | cross-stack secret scan | `route.common` | `gitleaks detect --no-git --redact --source .` | `ESTD1` section `19` | credential and secret leakage across source and config files |
| `static.common.semgrep` | cross-stack security scan | `route.common` | `semgrep --config .semgrep.yml --error .` | `ESTD1` section `18.5` | project-defined semantic security rules across PHP, Java, C#, TypeScript, and TSX |
| `static.java.spotbugs` | Java static analysis | `route.java-seam-api`, `route.smartfox-server` | `mvn -q -DskipTests spotbugs:check` | `ESTD7` section `13` | Java security and bug-pattern checks |
| `static.jenkins.jenkinsfile-lint` | Jenkins pipeline lint | `route.jenkins-cicd` | `jenkinsfile-runner lint Jenkinsfile` | `ESTD13` section `4.2` | Jenkinsfile syntax and pipeline entrypoint validity |
| `static.php.phpstan` | PHP static analysis | `route.php-monolith` | `vendor/bin/phpstan analyse --no-progress` | `ESTD6` section `2` | PHP version/configuration, type, and static analysis expectations |
| `static.unity.roslyn` | Unity/C# compile analysis | `route.unity-client` | `dotnet build --no-restore` | `ESTD3` section `2` | C# compile and analyzer output for `.cs` changes |
| `static.web.eslint` | web linting | `route.web-tools`, `route.product-website` | `node_modules/.bin/eslint .` | `ESTD11` section `5` | TypeScript, React, JavaScript, and JSX lint rules |
| `static.web.typescript` | web type checking | `route.web-tools`, `route.product-website` | `node_modules/.bin/tsc --noEmit` | `ESTD11` section `5.1` | strict TypeScript compilation for `.ts` and `.tsx` changes |

## Static Coverage By Validator

### `validator.cloud-aws`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| Environment and IaC shape | `static.cloud.terraform-validate`, `static.common.folder-structure` | environment strategy intent |
| IAM, secrets, and identity | `static.cloud.checkov`, `static.common.secrets`, `static.common.gitleaks` | least-privilege and permission-boundary judgment |
| Network and edge security | `static.cloud.checkov`, `static.cloud.terraform-validate` | network exposure intent |
| Data, backup, and retention | `static.cloud.checkov`, `static.cloud.terraform-validate` | restore and retention adequacy |
| Deployment and promotion safety | `static.common.report-consistency` | promotion strategy and approval context |
| Observability, resilience, and cost | `static.cloud.checkov` | resilience and cost trade-offs |
| PR and exception evidence | `static.common.report-consistency` | destructive-change evidence quality |

### `validator.database`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| Schema and model design | `static.common.folder-structure` | schema fit and data-model intent |
| Query and access safety | `static.common.semgrep` | repository and transaction intent |
| Migrations and backfills | `static.common.folder-structure` | expand-contract and rollout safety |
| Security and permissions | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | database permission boundary intent |
| Performance and operability | None | index and query-plan adequacy |
| Testing and evidence | `static.common.report-consistency` | staging evidence quality |
| Folder and config hygiene | `static.common.folder-structure` | naming intent where ambiguous |

### `validator.internal-scripts`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| Guide selection and entrypoints | `static.common.folder-structure`, `static.common.semgrep` | guide-specific compliance and command ergonomics |
| Input validation and safe mutation | `static.common.semgrep` | destructive-action and safe mutation intent |
| External adapters and command boundaries | `static.common.semgrep` | adapter and external tool boundary clarity |
| Modularity and data flow | `static.common.semgrep` | modularity threshold and structure debt |
| Testing and repeatable checks | `static.common.report-consistency` | path intent and coverage adequacy |
| Naming and discoverability | `static.common.folder-structure` | naming clarity |
| Closeout and operational evidence | `static.common.report-consistency` | closeout proof and rollback evidence |

### `validator.java-seam-api`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| API design and SEAM layering | `static.java.spotbugs`, `static.common.folder-structure` | SEAM layering, API contract, and service boundary intent |
| Java code conformity | `static.java.spotbugs`, `static.common.folder-structure` | framework-specific design judgment |
| Persistence and data safety | `static.java.spotbugs`, `static.common.semgrep` | transaction and schema ownership intent |
| Boundary validation and errors | `static.java.spotbugs`, `static.common.semgrep` | boundary completeness |
| Security and privacy | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep`, `static.java.spotbugs` | auth/authz and permission-boundary intent |
| Observability and resilience | `static.java.spotbugs` | resilience design sufficiency |
| Testing and path coverage | `static.java.spotbugs` | path intent and coverage adequacy |
| PR and dependency evidence | `static.common.report-consistency` | dependency approval context |

### `validator.jenkins-cicd`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| Pipeline source and reuse | `static.jenkins.jenkinsfile-lint`, `static.common.folder-structure` | shared-library design intent |
| Secrets and build identity | `static.common.secrets`, `static.common.gitleaks`, `static.jenkins.jenkinsfile-lint` | credential boundary judgment |
| Build, test, and artifacts | `static.jenkins.jenkinsfile-lint` | artifact and evidence sufficiency |
| Promotion gates and rollback | `static.jenkins.jenkinsfile-lint` | approval and rollback intent |
| Agents, RBAC, and audit | `static.jenkins.jenkinsfile-lint` | RBAC and audit adequacy |
| Reporting and notifications | `static.jenkins.jenkinsfile-lint` | routing usefulness |
| Maintainability and safety | `static.jenkins.jenkinsfile-lint`, `static.common.semgrep` | Groovy maintainability judgment |

### `validator.php-monolith`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| Server architecture and API shape | `static.common.folder-structure` | API contract and service design intent |
| PHP code conformity | `static.php.phpstan`, `static.common.folder-structure` | legacy-pattern acceptability |
| Boundary validation and error handling | `static.php.phpstan`, `static.common.semgrep` | boundary completeness |
| Database access and migrations | `static.common.semgrep` | migration safety and transaction intent |
| Security and privacy | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | auth/session and permission-boundary intent |
| Performance and operability | `static.common.semgrep` | caching and operability sufficiency |
| Testing and path coverage | `static.php.phpstan` | path intent and coverage adequacy |
| PR and maintenance evidence | `static.common.report-consistency` | PR evidence quality |

### `validator.product-website`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| Web architecture and TypeScript | `static.web.typescript`, `static.web.eslint`, `static.common.folder-structure` | architecture and component boundary intent |
| Public UX and WebGL launch surface | None | UX completeness and player impact |
| API and backend boundaries | `static.web.typescript`, `static.web.eslint`, `static.common.semgrep` | API contract, trust, and database boundary intent |
| Data and persistence | `static.common.semgrep` | schema and migration intent |
| Cloud and edge deployment | `static.cloud.checkov`, `static.cloud.terraform-validate` | edge deployment trade-offs |
| CI/CD and release safety | `static.common.report-consistency` | release evidence quality |
| Security and privacy | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | auth/privacy and permission-boundary intent |
| Testing and path coverage | `static.web.typescript`, `static.web.eslint` | path intent and coverage adequacy |

### `validator.smartfox-server`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| SmartFox architecture and authority | `static.java.spotbugs`, `static.common.folder-structure` | real-time authority and room design |
| Java code conformity | `static.java.spotbugs`, `static.common.folder-structure` | SmartFox-specific style judgment |
| Room lifecycle and concurrency | `static.java.spotbugs`, `static.common.semgrep` | lifecycle and lock discipline |
| Real-time protocol resilience | `static.java.spotbugs` | reconnect and idempotency intent |
| API, persistence, and data safety | `static.java.spotbugs`, `static.common.semgrep` | checkpoint and retry strategy |
| Security and abuse controls | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | trust-boundary and abuse-control adequacy |
| Observability, memory, and shutdown | `static.java.spotbugs` | shutdown and leak-risk sufficiency |
| Testing and PR evidence | `static.common.report-consistency` | path coverage and review evidence |

### `validator.technical-docs`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| Document type and metadata | `static.common.folder-structure` | template completeness |
| Goals, scope, and decisions | None | decision clarity and trade-offs |
| Design, risks, and operations | None | API contract, risk, and operational adequacy |
| References and traceability | `static.common.report-consistency` | reference relevance |
| Review and approval path | `static.common.report-consistency` | approval context |
| Migration and validation evidence | `static.common.report-consistency` | validation adequacy |
| Formatting and maintainability | `static.common.folder-structure` | prose quality |

### `validator.unity-client`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| Client architecture and state | `static.common.folder-structure`, `static.unity.roslyn` | architecture intent, dependency direction |
| Unity and C# code style | `static.unity.roslyn`, `static.common.folder-structure` | Unity lifecycle appropriateness |
| Async, networking, and resilience | `static.unity.roslyn`, `static.common.secrets` | API contract consumption and degraded-network behavior |
| UX, accessibility, and localization | None | UX completeness and player impact |
| Security and privacy | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | trust-boundary intent |
| Performance, memory, and battery | `static.unity.roslyn` | runtime impact and profiling sufficiency |
| Testing and path coverage | `static.unity.roslyn` | path intent and coverage adequacy |
| Build, PR, and release evidence | `static.common.report-consistency` | PR evidence quality |

### `validator.web-tools`

| Group | Static Check IDs | Residual LLM Gap |
|:------|:-----------------|:-----------------|
| TypeScript and React conformity | `static.web.typescript`, `static.web.eslint`, `static.common.folder-structure` | component design intent |
| Tool API integration | `static.web.typescript`, `static.web.eslint`, `static.common.semgrep` | API, trust, and database boundary judgment |
| Auth, authorization, and access control | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | RBAC and access-flow intent |
| Sensitive actions and auditability | `static.common.semgrep` | operational risk judgment |
| UX, accessibility, and operability | `static.web.eslint` | UX completeness and task ergonomics |
| Deployment and environment safety | `static.common.report-consistency` | deployment evidence quality |
| Testing and path coverage | `static.web.typescript`, `static.web.eslint` | path intent and coverage adequacy |
| Security and dependency hygiene | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | dependency/coupling and permission-boundary intent |
