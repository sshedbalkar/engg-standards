# ESTD18 - Codebase Folder Structure Standards

| Field | Value |
|:------|:----|
| **Document ID** | ESTD18 |
| **Version** | 1.0 |
| **Status** | Draft |
| **Last Updated** | 2026-04-14 |
| **Applies To** | All engineers — server, client, tools, automation, infrastructure |
| **Depends On** | ESTD1 — Common Engineering Standards |
| **Approval** | Director of Engineering |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

This document defines the canonical root-level folder structure for every project type in the Bingo Bash engineering ecosystem. It prescribes what goes where at the top of the repository — not how code is organized internally within a language's package system (those rules live in the language-specific standards this document cross-references).

Read Section 2 first. It establishes the universal principles all trees share. Then jump to the section for your project type. If your project straddles two types (e.g., a Java microservice that also runs Terraform for its own infrastructure), apply each section independently.

---

## Table of Contents

- [ESTD18 - Codebase Folder Structure Standards](#estd18---codebase-folder-structure-standards)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Universal Principles](#2-universal-principles)
    - [2.1 Separation of Concerns at the Folder Level](#21-separation-of-concerns-at-the-folder-level)
    - [2.2 Discoverability Over Cleverness](#22-discoverability-over-cleverness)
    - [2.3 Build Artifacts Are Never Committed](#23-build-artifacts-are-never-committed)
    - [2.4 Configuration Layering by Environment](#24-configuration-layering-by-environment)
    - [2.5 Documentation Lives With the Code](#25-documentation-lives-with-the-code)
    - [2.6 Test Proximity](#26-test-proximity)
  - [3. PHP Server (Legacy API Monolith)](#3-php-server-legacy-api-monolith)
  - [4. Java Server (SEAM Microservices)](#4-java-server-seam-microservices)
  - [5. SmartFox Server](#5-smartfox-server)
  - [6. Unity Client](#6-unity-client)
  - [7. Web Tools (Next.js)](#7-web-tools-nextjs)
  - [8. Internal Tools (CLI / Scripts)](#8-internal-tools-cli--scripts)
    - [8.1 Python CLI Tool](#81-python-cli-tool)
    - [8.2 Shell Script Collection](#82-shell-script-collection)
  - [9. Infrastructure as Code (Terraform)](#9-infrastructure-as-code-terraform)
  - [10. Jenkins Build System](#10-jenkins-build-system)
  - [11. Quick Reference Matrix](#11-quick-reference-matrix)

---

## 1. Purpose and Scope

Inconsistent top-level repository layouts make onboarding slower, cross-team navigation harder, and tooling (CI/CD, static analysis, secrets scanning) more fragile. A new engineer should be able to locate any file — source, test, config, migration, deployment script — within 30 seconds of opening any repo, regardless of project type.

This document defines the canonical folder structure for the following project types:

- PHP Server (Legacy API Monolith)
- Java Server (SEAM Microservices)
- SmartFox Server
- Unity Client
- Web Tools (Next.js)
- Internal Tools (Python CLI / Shell Scripts)
- Infrastructure as Code (Terraform)
- Jenkins Build System

This document does **not** govern internal code organization within packages, classes, or modules — see the cross-referenced language and platform standards for those rules.

---

## 2. Universal Principles

These principles apply to every project type. The canonical trees in Sections 3–10 are their concrete expression.

### 2.1 Separation of Concerns at the Folder Level

Source code, tests, configuration, documentation, and build artifacts occupy distinct top-level folders. No folder serves two concerns.

```
src/        ← source only
tests/      ← tests only
config/     ← configuration only
docs/       ← documentation only
scripts/    ← maintenance and automation scripts only
```

A file that is hard to place is a signal that it is doing too many things.

### 2.2 Discoverability Over Cleverness

Folder names are plain English nouns that describe their contents, not their technical role. A developer unfamiliar with the project must be able to navigate to any file without reading documentation first.

- `src/` not `lib/`, `app/`, or `code/`
- `tests/` not `spec/`, `__tests__/`, or `test/`
- `config/` not `cfg/`, `conf/`, or `settings/`
- `docs/` not `documentation/`, `wiki/`, or `notes/`
- `scripts/` not `tools/`, `utils/`, or `bin/` (except where language convention requires it)

Platform-mandated exceptions (e.g., Unity's `Assets/`, Java's `src/main/java/`) are accepted as-is.

### 2.3 Build Artifacts Are Never Committed

Compiled output, dependency caches, and intermediate build files must be excluded via `.gitignore`. The repo contains only source and declarative dependency manifests.

Common excludes by project type:

| Project Type | Excluded Paths |
|:-------------|:---------------|
| PHP | `vendor/` |
| Java | `target/` |
| Unity | `Builds/`, `Library/`, `Temp/` |
| Next.js | `.next/`, `node_modules/` |
| Python | `dist/`, `__pycache__/`, `*.egg-info/` |
| Terraform | `.terraform/`, `*.tfstate`, `*.tfstate.backup` |

### 2.4 Configuration Layering by Environment

Configuration is versioned. Environment-specific overrides are in separate files, never hardcoded into source. Secrets are never committed — only `.env.example` or equivalent placeholder files.

```
config/
├── app.json              ← base configuration (committed)
├── environments/
│   ├── dev.json          ← dev overrides (committed)
│   ├── staging.json      ← staging overrides (committed)
│   └── production.json   ← production overrides (committed, no secrets)
.env.example              ← secret keys listed with empty values (committed)
.env                      ← actual secrets (never committed)
```

### 2.5 Documentation Lives With the Code

Architectural decisions, runbooks, and component overviews live in a `docs/` folder at the root. Long-lived documentation that evolves with the code belongs in the repo, not only in Confluence. *Confluence is derived; the repo is authoritative.*

For complex subdirectories (e.g., a `handlers/` folder with 30 files), a `README.md` inside that folder is acceptable and encouraged.

### 2.6 Test Proximity

Test files mirror the structure of the source tree they test. A test for `src/Reward/Service/RewardService.php` lives at `tests/Unit/Reward/Service/RewardServiceTest.php`. This rule makes it possible to find tests and source in lockstep without a search tool.

---

## 3. PHP Server (Legacy API Monolith)

The legacy PHP API is a domain-modular monolith. Each domain module (`Player`, `Reward`, `Bingo`, `Event`) is a first-class folder under `src/`, self-contained with its own service, repository, and validator classes. See [ESTD6 §5.1 Namespace and Directory Structure](./ESTD6_-_PHP_Programming_Standards.md#51-namespace-and-directory-structure) for internal namespace and directory layout within each module.

```
bingo-api/
├── src/                            ← PSR-4 autoloaded application source
│   ├── Core/                       ← Cross-cutting infrastructure: DB, session, logging
│   ├── Player/                     ← Domain: player profile, authentication
│   ├── Reward/                     ← Domain: reward claiming, cooldowns
│   ├── Bingo/                      ← Domain: game rooms, card management, daubing
│   └── Event/                      ← Domain: timed events, jackpots, leaderboards
├── tests/
│   ├── Unit/                       ← Mirrors src/ structure (see §2.6)
│   └── Integration/                ← Tests requiring DB or external services
├── config/
│   ├── app.php                     ← Application-wide constants and settings
│   ├── database.php                ← Database connection parameters
│   └── environments/
│       ├── dev.php
│       ├── staging.php
│       └── production.php
├── public/                         ← Web root — contains only index.php and assets
├── scripts/                        ← CLI maintenance: cache warm-up, data migrations
├── docs/                           ← Architecture notes, ADRs, runbooks
├── vendor/                         ← Composer dependencies (never committed)
├── composer.json
├── composer.lock
├── .env.example
└── .gitignore
```

**Non-obvious rules:**
- `public/` contains only `index.php` (the front controller) and static assets served directly. No business logic.
- Domain modules under `src/` must not import from each other directly. Cross-module calls go through a service interface or message queue.
- Migration scripts live in `scripts/db/` — not in `src/` and not co-located with config.

---

## 4. Java Server (SEAM Microservices)

Each SEAM microservice is its own repository. The root layout follows Maven conventions. See [ESTD7 §5.1 Package Structure Per Microservice](./ESTD7_-_Java_Programming_Standards.md#51-package-structure-per-microservice) for the internal Java package structure within `src/main/java/`.

```
reward-engine/                      ← One repo per microservice
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/bingo/reward/   ← Internal package layout: see ESTD7 §5.1
│   │   └── resources/
│   │       ├── application.yml     ← Base Spring Boot configuration
│   │       ├── application-dev.yml
│   │       ├── application-staging.yml
│   │       └── application-prod.yml
│   └── test/
│       └── java/
│           └── com/bingo/reward/   ← Mirrors main/java structure exactly
├── scripts/
│   └── db/                         ← Flyway migration scripts (V1__init.sql, V2__...)
├── docs/                           ← Service-level architecture, API contracts
├── Dockerfile
├── pom.xml
└── .gitignore
```

**Non-obvious rules:**
- `application-{env}.json` files contain non-secret environment overrides. Secrets are injected via AWS Secrets Manager at runtime — never in any `.json` file.
- Flyway migration files in `scripts/db/` are append-only. Never edit a migration that has been applied to any environment.
- There is no `config/` folder at the root — Spring Boot's `resources/` is the config home for Java services.

---

## 5. SmartFox Server

The SmartFox extension is a single repository. Each game has one extension under `src/extensions/`. See [ESTD12 §4. Extension Structure and Handler Pattern](./ESTD12_-_Smartfox_Server_Standards.md#4-extension-structure-and-handler-pattern) for handler registration and the one-handler-per-command rule.

```
bingo-smartfox/
├── src/
│   └── extensions/
│       └── BingoExtension/         ← One extension per game
│           ├── BingoExtension.java ← Extension entry point; registers all handlers
│           ├── handlers/           ← One class per client command (see ESTD12 §4)
│           ├── services/           ← Business logic called by handlers
│           ├── model/              ← Room state, player session objects
│           └── util/               ← Shared utilities (no business logic)
├── config/
│   ├── sfs-config.xml              ← Zone and room definitions
│   └── environments/
│       ├── dev/
│       ├── staging/
│       └── production/
├── deploy/                         ← SFS runtime patching and deployment scripts
├── tests/
├── docs/
├── pom.xml
└── .gitignore
```

**Non-obvious rules:**
- `config/environments/` contains full SmartFox XML configs per environment, not diff patches. The deploy script selects the correct environment folder.
- `deploy/` is not `scripts/` — it contains SmartFox-specific hot-deploy artifacts and restart procedures, distinct from general maintenance scripts.
- Do not add a `zones/` or `rooms/` folder at the root. All zone and room configuration belongs in `config/sfs-config.xml`.

---

## 6. Unity Client

The Unity project uses the `_Project` prefix convention to sort project-owned content above third-party packages in the Unity Editor. See [ESTD3 §4.1 One Class per File](./ESTD3_-_Unity_and_C%23_Standards.md#41-one-class-per-file) and [ESTD3 §4.2 File Name](./ESTD3_-_Unity_and_C%23_Standards.md#42-file-name) for file naming rules (one class per file, filename matches class name).

```
bingo-client/
├── Assets/
│   ├── _Project/                   ← All project-owned content (sorts first in Editor)
│   │   ├── Art/
│   │   │   ├── Animations/
│   │   │   ├── Fonts/
│   │   │   ├── Textures/
│   │   │   └── UI/
│   │   ├── Audio/
│   │   │   ├── Music/
│   │   │   └── SFX/
│   │   ├── Prefabs/
│   │   │   ├── Bingo/              ← Bingo gameplay prefabs
│   │   │   ├── UI/
│   │   │   └── Shared/
│   │   ├── ScriptableObjects/      ← Data containers (rewards, room configs)
│   │   ├── Scenes/
│   │   │   ├── Boot.unity
│   │   │   ├── Lobby.unity
│   │   │   └── BingoRoom.unity
│   │   └── Scripts/
│   │       ├── Core/               ← App lifecycle, dependency injection
│   │       ├── Bingo/              ← Game logic: cards, daubing, win detection
│   │       ├── UI/                 ← UI controllers and view bindings
│   │       ├── Network/            ← SmartFox client integration
│   │       ├── Rewards/
│   │       └── Analytics/
│   ├── Plugins/                    ← Third-party SDKs and native plugins (do not edit)
│   ├── StreamingAssets/            ← Runtime-loaded bundles, localization files
│   └── Editor/                     ← Editor-only tools, build pipeline scripts
├── Packages/                       ← Unity Package Manager manifest (package.json)
├── ProjectSettings/                ← Committed Unity project settings
├── docs/                           ← Architecture decisions, dependency notes
└── .gitignore                      ← Excludes Library/, Temp/, Builds/, obj/
```

**Non-obvious rules:**
- `_Project/` underscore prefix is intentional — it sorts above `Plugins/` in the Unity Editor asset browser, making project code always immediately visible.
- Third-party SDKs belong in `Plugins/` only. Never edit files inside `Plugins/`.
- `Assets/Editor/` is for editor-only code (custom inspectors, build scripts). It is stripped from runtime builds by Unity automatically.
- `Builds/` (Unity output) must be in `.gitignore`. Never commit build output.
- `Library/` and `Temp/` are Unity's local caches — always gitignored.

---

## 7. Web Tools (Next.js)

Internal web tools follow the Next.js App Router convention. The root layout is kept minimal; all application code lives under `src/`. See [ESTD11 §4. Web Tools Project Structure](./ESTD11_-_Web_Development_and_Deployment_Standards.md#4-web-tools-project-structure) for the full internal structure within `src/` (components, hooks, services, store, types, lib).

```
tool-name/
├── src/                            ← Full internal layout defined in ESTD11 §4
├── public/                         ← Static assets served at root URL
├── tests/
│   ├── unit/
│   └── integration/
├── docs/                           ← Tool purpose, API integration notes
├── scripts/                        ← Dev utilities: seed data, local fixture generation
├── .env.example                    ← All required env vars with empty values
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── .gitignore                      ← Excludes .next/, node_modules/
```

**Non-obvious rules:**
- `.env.example` must list every variable the tool requires. An engineer must be able to run the tool locally using only `.env.example` as a guide.
- `scripts/` contains developer utilities only — not CI/CD scripts. CI/CD pipeline definitions live in the Jenkins repo (see Section 10).
- Do not add a `config/` folder. Next.js tool configuration lives in `next.config.ts` and environment variables.

---

## 8. Internal Tools (CLI / Scripts)

### 8.1 Python CLI Tool

Python CLI tools follow the `src/` layout with a named package matching the tool name (snake_case).

```
tool-name/
├── src/
│   └── tool_name/                  ← Python package (snake_case of tool name)
│       ├── __init__.py
│       ├── cli.py                  ← Entry point: Click/Typer command group definitions
│       ├── commands/               ← One module per logical command group
│       │   ├── players.py          ← e.g., `tool-name players list`
│       │   └── rewards.py          ← e.g., `tool-name rewards grant`
│       ├── services/               ← Business logic, external API clients
│       ├── models/                 ← Data classes, Pydantic schemas
│       └── utils/                  ← Shared helpers (formatting, pagination)
├── tests/
│   ├── unit/                       ← Mirrors src/tool_name/ structure
│   └── integration/                ← Tests requiring live API or DB
├── docs/
├── scripts/                        ← Dev setup, fixture generation, local test data
├── pyproject.toml                  ← Build config, dependencies, entry points
├── .env.example
└── .gitignore                      ← Excludes dist/, __pycache__/, *.egg-info/
```

### 8.2 Shell Script Collection

For repositories that are purely shell-based (deploy helpers, credential rotation, data pipeline wrappers):

```
scripts-collection/
├── bin/                            ← Executable scripts (chmod +x enforced)
│   ├── deploy-reward-engine.sh
│   └── rotate-db-credentials.sh
├── lib/                            ← Sourced helper functions (not executable directly)
│   └── common.sh                   ← Shared: logging, error handling, env validation
├── config/
│   └── environments/
│       ├── dev.env
│       ├── staging.env
│       └── production.env
├── docs/
└── README.md
```

**Non-obvious rules (Python):**
- The package name inside `src/` must be the snake_case equivalent of the hyphenated tool name (e.g., `tool-name` → `tool_name`). This avoids import errors.
- Entry points are declared in `pyproject.toml` — not hardcoded in `cli.py`.
- `commands/` modules each define one Click/Typer group. No command logic lives directly in `cli.py`.

**Non-obvious rules (shell):**
- All scripts in `bin/` must be executable (`chmod +x`). CI enforces this.
- `lib/common.sh` is sourced, never executed directly. It must not contain `main()` logic.
- `.env` files in `config/environments/` contain non-secret defaults only. Actual secrets are fetched from AWS Secrets Manager at runtime.

---

## 9. Infrastructure as Code (Terraform)

All IaC uses Terraform. The repo is split into reusable modules and per-environment root modules. See [ESTD5 §2. Infrastructure as Code (IaC)](./ESTD5_-_Cloud_Engg_Standards.md#2-infrastructure-as-code-iac) for IaC principles and [ESTD8 §3. IAM and Permission Management](./ESTD8_-_AWS_Standards.md#3-iam-and-permission-management) for IAM and permission standards.

```
bingo-infra/
├── modules/                        ← Reusable Terraform modules (no provider config)
│   ├── bingo-cluster/              ← ECS/EKS cluster definitions
│   ├── bingo-database/             ← RDS / DocumentDB provisioning
│   └── bingo-networking/           ← VPC, subnets, security groups, NACLs
├── environments/                   ← Per-environment root modules (have provider config)
│   ├── dev/
│   │   ├── main.tf                 ← Calls modules with dev-specific inputs
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars        ← Non-secret variable values for dev
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   └── production/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── terraform.tfvars
├── scripts/                        ← Wrapper scripts: plan, apply, validate, fmt check
├── docs/                           ← Architecture diagrams, ADRs, cost estimates
├── .terraform.lock.hcl             ← Provider version lock file (always committed)
└── .gitignore                      ← Excludes .terraform/, *.tfstate, *.tfstate.backup
```

**Non-obvious rules:**
- `modules/` never contains a `provider` block. Provider configuration belongs only in `environments/*/main.tf`.
- `terraform.tfvars` contains non-secret variable values. Secrets (DB passwords, API keys) are passed via AWS Secrets Manager or environment variable injection in CI — never in `.tfvars`.
- `.terraform.lock.hcl` is always committed. It pins provider versions and prevents silent provider upgrades.
- State files (`*.tfstate`) are never committed. Remote state lives in S3 with DynamoDB locking (see ESTD8 §13).
- Each environment folder is an independent Terraform root. `terraform init` is run per-environment, not at the repo root.

---

## 10. Jenkins Build System

Jenkins pipeline definitions live in a dedicated repo, separate from application code. See [ESTD13 §4. Pipeline-as-Code Standards](./ESTD13_-_Jenkins_CI_CD_Standards.md#4-pipeline-as-code-standards) for pipeline-as-code standards.

```
bingo-jenkins/
├── pipelines/                      ← Declarative Jenkinsfile definitions
│   ├── unity/
│   │   ├── Jenkinsfile.build       ← Unity client build pipeline
│   │   └── Jenkinsfile.release     ← Unity release (store submission) pipeline
│   ├── server/
│   │   ├── Jenkinsfile.deploy      ← Java/PHP service deployment pipeline
│   │   └── Jenkinsfile.rollback    ← Emergency rollback pipeline
│   └── tools/
│       └── Jenkinsfile.deploy      ← Web tool deployment pipeline
├── shared-library/                 ← Jenkins shared library (if in use)
│   └── vars/
│       ├── notifySlack.groovy      ← Reusable notification step
│       └── deployToEnv.groovy      ← Reusable environment promotion step
├── scripts/                        ← Shell scripts invoked by pipelines
│   ├── unity/                      ← Unity-specific build helpers
│   └── server/                     ← Server-specific deploy helpers
├── config/                         ← Environment-specific pipeline parameters
│   ├── dev.json
│   ├── staging.json
│   └── production.json
├── docs/                           ← Pipeline architecture, credential inventory
└── .gitignore
```

**Non-obvious rules:**
- Each `Jenkinsfile.*` is a separate file per pipeline purpose — not one monolithic Jenkinsfile with conditional logic.
- `scripts/` contains shell scripts called by `sh` steps inside Jenkinsfiles. No logic lives inline in Jenkinsfiles beyond orchestration calls.
- `config/` YAML files hold non-secret pipeline parameters (target hosts, ECR registries, artifact paths). Secrets are stored in Jenkins Credentials, not in this repo.
- `shared-library/vars/` functions are global pipeline steps — keep them minimal and single-purpose.

---

## 11. Quick Reference Matrix

| Concern | PHP Server | Java Server | SmartFox | Unity Client | Web Tool | Python CLI | Shell Scripts | Terraform | Jenkins |
|:--------|:-----------|:------------|:---------|:-------------|:---------|:-----------|:--------------|:----------|:--------|
| **Source** | `src/` | `src/main/java/` | `src/extensions/` | `Assets/_Project/Scripts/` | `src/` | `src/<pkg>/` | `bin/` | `modules/` | `pipelines/` |
| **Tests** | `tests/` | `src/test/java/` | `tests/` | Unity Test Runner | `tests/` | `tests/` | — | — | — |
| **Config** | `config/` | `src/main/resources/` | `config/` | `ProjectSettings/` | `next.config.ts` + `.env.example` | `pyproject.toml` + `.env.example` | `config/` | `environments/` | `config/` |
| **Docs** | `docs/` | `docs/` | `docs/` | `docs/` | `docs/` | `docs/` | — | `docs/` | `docs/` |
| **Scripts** | `scripts/` | `scripts/` | `deploy/` | `Assets/Editor/` | `scripts/` | `scripts/` | `lib/` | `scripts/` | `scripts/` |
| **Build output** | `vendor/` *(gitignored)* | `target/` *(gitignored)* | SFS deploy | `Builds/` `Library/` *(gitignored)* | `.next/` `node_modules/` *(gitignored)* | `dist/` `__pycache__/` *(gitignored)* | — | `.terraform/` *(gitignored)* | Jenkins workspace |
| **Static assets** | `public/` | — | — | `Assets/_Project/Art/` | `public/` | — | — | — | — |
| **DB migrations** | `scripts/db/` | `scripts/db/` | — | — | — | — | — | — | — |
| **Reusable modules** | — | — | — | `Assets/Plugins/` | — | — | `lib/` | `modules/` | `shared-library/` |
