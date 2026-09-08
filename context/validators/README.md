# Validator Specs

## Purpose

Validator specs define how static tools and LLM gap review evaluate code against routed ESTD docs.

- Source standards stay in `docs/`.
- Route bindings come from `context/estd-routing-map.md`.
- Each validator keeps doc IDs, facets, static coverage, scoring, and evolution rules only.
- Exact findings must cite source ESTD sections after retrieval.
- Static validators are preferred wherever deterministic checks are possible.
- LLM review covers only gaps static tools cannot judge.

## Lookup Strategy
- primary_lookup: validator_route
- ordering: bound_route_id
- jump_index: present
- entry_id_format: validator.[route-id]

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

## Validation Type References

| Doc | Purpose | Update When |
|:----|:--------|:------------|
| `context/validators/static-validation.md` | Static validation purpose, check inventory, and Static Coverage summary | static registry, built-in static behavior, or Static Coverage tables change |
| `context/validators/llm-based-validation.md` | LLM gap-review purpose, contract, and semantic validation inventory | validator groups, LLM gaps, report schema, or LLM request behavior change |

## Shared Scoring Contract

- pass threshold: > 75% code conformity.
- score formula: passed applicable weight / total applicable weight * 100.
- non-applicable handling: remove non-applicable checks from the denominator.
- critical blocker overrides: fail on any critical security, data-loss, auth-bypass, or production-safety blocker.
- unknown evidence handling: unknown evidence fails until static output or LLM gap review retrieves source ESTD sections.

## Validator Inventory


| Validator | Route | File |
|:----------|:------|:-----|
| `validator.cloud-aws` | `route.cloud-aws` | `context/validators/cloud-aws-validator.md` |
| `validator.database` | `route.database` | `context/validators/database-validator.md` |
| `validator.internal-scripts` | `route.internal-scripts` | `context/validators/internal-scripts-validator.md` |
| `validator.java-seam-api` | `route.java-seam-api` | `context/validators/java-seam-api-validator.md` |
| `validator.jenkins-cicd` | `route.jenkins-cicd` | `context/validators/jenkins-cicd-validator.md` |
| `validator.php-monolith` | `route.php-monolith` | `context/validators/php-monolith-validator.md` |
| `validator.product-website` | `route.product-website` | `context/validators/product-website-validator.md` |
| `validator.smartfox-server` | `route.smartfox-server` | `context/validators/smartfox-server-validator.md` |
| `validator.spring-boot-api` | `route.spring-boot-api` | `context/validators/spring-boot-api-validator.md` |
| `validator.spring-boot-security` | `route.spring-boot-security` | `context/validators/spring-boot-security-validator.md` |
| `validator.technical-docs` | `route.technical-docs` | `context/validators/technical-docs-validator.md` |
| `validator.unity-client` | `route.unity-client` | `context/validators/unity-client-validator.md` |
| `validator.web-tools` | `route.web-tools` | `context/validators/web-tools-validator.md` |

## Evolution Rules

- Re-resolve route and ESTD docs before each validator run.
- After ESTD doc create/update/rename/repurpose, review affected route validators.
- Update a validator when its route, source docs, or validator facets change.
- Update scoring or static coverage only when the ESTD change creates durable validator coverage.
- Add new check groups only when a ESTD doc creates durable validator coverage.
- Do not copy full rules from ESTD docs into validator specs.
- Keep weights totaling 100 unless the validator explicitly marks a group non-applicable.
- Keep Static Coverage tables mapped to `tools/estd-enforcer/static-checks/registry.json`.
- Update `context/validators/static-validation.md` and `context/validators/llm-based-validation.md` whenever their inventories change.
