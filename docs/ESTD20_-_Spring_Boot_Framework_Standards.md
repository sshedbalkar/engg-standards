# ESTD20 - Spring Boot Framework Standards for Banking Services

**ESTD20 — Spring Boot Framework Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD20 |
| Version | 1.0 |
| Status | Draft |
| Last Updated | 2026-09-02 |
| Applies To | Spring Boot 3.3+ / Java 21 services built for regulated banking workloads |
| Depends On | None — this document is self-contained |
| Approval | Director of Engineering / Server Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD20 is the framework standard for Spring Boot services in the banking application. It is **self-contained**: it does not require any other ESTD document to be read first, and it restates the baseline rules it depends on rather than referring outward. Read it end to end once before writing code, then use it as a reference.

ESTD20 covers how the application is built: structure, configuration, dependency injection, the HTTP layer, persistence, transactions, money handling, concurrency, messaging, caching, batch, resilience, observability, testing, and supply chain.

**Data protection, authentication, authorization, encryption, masking, audit trail, and regulatory compliance are in [ESTD21](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#estd21---data-protection-security-and-audit-standards-for-spring-boot-banking-services)**, which builds on this document. Read ESTD20 first, then ESTD21. Neither document is optional for a banking service.

**Scope boundary**: ESTD20 governs Spring Boot services only. It does not govern the Bingo SEAM microservices, which are covered by [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server). ESTD7's prohibition on importing Spring Boot dependencies is scoped to SEAM services and does not apply here. Where the two documents differ, each is authoritative inside its own stack.

---

## Table of Contents

- [ESTD20 - Spring Boot Framework Standards for Banking Services](#estd20---spring-boot-framework-standards-for-banking-services)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Baseline Versions and Build](#2-baseline-versions-and-build)
    - [2.1 Mandated Versions](#21-mandated-versions)
    - [2.2 Version Management via BOM](#22-version-management-via-bom)
    - [2.3 Dependency Rules](#23-dependency-rules)
    - [2.4 Compiler and Build Enforcement](#24-compiler-and-build-enforcement)
  - [3. Project and Package Structure](#3-project-and-package-structure)
    - [3.1 Canonical Package Layout](#31-canonical-package-layout)
    - [3.2 Layer Responsibilities](#32-layer-responsibilities)
    - [3.3 Dependency Direction](#33-dependency-direction)
    - [3.4 Enforcing Structure with ArchUnit](#34-enforcing-structure-with-archunit)
  - [4. Application Bootstrap and Configuration](#4-application-bootstrap-and-configuration)
    - [4.1 The Main Class Does Nothing](#41-the-main-class-does-nothing)
    - [4.2 Component Scanning Stays Narrow](#42-component-scanning-stays-narrow)
    - [4.3 Configuration Files and Profiles](#43-configuration-files-and-profiles)
    - [4.4 Typed Configuration, Not Scattered `@Value`](#44-typed-configuration-not-scattered-value)
    - [4.5 Fail Fast](#45-fail-fast)
    - [4.6 Configuration Precedence](#46-configuration-precedence)
  - [5. Dependency Injection and Bean Design](#5-dependency-injection-and-bean-design)
    - [5.1 Constructor Injection Only](#51-constructor-injection-only)
    - [5.2 Bean Scope](#52-bean-scope)
    - [5.3 No Circular Dependencies](#53-no-circular-dependencies)
    - [5.4 Qualifiers and Multiple Implementations](#54-qualifiers-and-multiple-implementations)
    - [5.5 Lifecycle Callbacks](#55-lifecycle-callbacks)
  - [6. REST API Standards](#6-rest-api-standards)
    - [6.1 URL Design](#61-url-design)
    - [6.2 Versioning](#62-versioning)
    - [6.3 HTTP Methods and Status Codes](#63-http-methods-and-status-codes)
    - [6.4 Entities Never Cross the Controller Boundary](#64-entities-never-cross-the-controller-boundary)
    - [6.5 Controller Shape](#65-controller-shape)
    - [6.6 Pagination](#66-pagination)
    - [6.7 Idempotency on Money-Moving Endpoints](#67-idempotency-on-money-moving-endpoints)
    - [6.8 Request and Response Conventions](#68-request-and-response-conventions)
  - [7. Input Validation](#7-input-validation)
    - [7.1 Validate at the Boundary, Reject Everything Else](#71-validate-at-the-boundary-reject-everything-else)
    - [7.2 Jakarta Validation on Request Records](#72-jakarta-validation-on-request-records)
    - [7.3 Custom Constraints for Domain Types](#73-custom-constraints-for-domain-types)
    - [7.4 Reject Unknown Properties](#74-reject-unknown-properties)
    - [7.5 Validating Nested and Collection Inputs](#75-validating-nested-and-collection-inputs)
    - [7.6 Validating Path Variables and Parameters](#76-validating-path-variables-and-parameters)
    - [7.7 Server-Side Business Validation Is Separate and Mandatory](#77-server-side-business-validation-is-separate-and-mandatory)
  - [8. Error Handling](#8-error-handling)
    - [8.1 Exception Hierarchy](#81-exception-hierarchy)
    - [8.2 The Error Code Catalogue](#82-the-error-code-catalogue)
    - [8.3 The Global Exception Handler](#83-the-global-exception-handler)
    - [8.4 Error Response Shape](#84-error-response-shape)
    - [8.5 Where to Catch, and Where Not To](#85-where-to-catch-and-where-not-to)
  - [9. Persistence with Spring Data JPA](#9-persistence-with-spring-data-jpa)
    - [9.1 Entity Rules](#91-entity-rules)
    - [9.2 Entity Identity](#92-entity-identity)
    - [9.3 Associations Are Lazy](#93-associations-are-lazy)
    - [9.4 Repositories](#94-repositories)
    - [9.5 Optimistic Locking Is Mandatory on Mutable Financial State](#95-optimistic-locking-is-mandatory-on-mutable-financial-state)
    - [9.6 Open Session In View Is Disabled](#96-open-session-in-view-is-disabled)
    - [9.7 The N+1 Problem](#97-the-n1-problem)
    - [9.8 Migrations with Flyway](#98-migrations-with-flyway)
    - [9.9 Zero-Downtime Schema Change: Expand-Contract](#99-zero-downtime-schema-change-expand-contract)
    - [9.10 Connection Pool](#910-connection-pool)
  - [10. Transactions](#10-transactions)
    - [10.1 Transactions Belong to the Service Layer](#101-transactions-belong-to-the-service-layer)
    - [10.2 The Self-Invocation Trap](#102-the-self-invocation-trap)
    - [10.3 Propagation](#103-propagation)
    - [10.4 Isolation](#104-isolation)
    - [10.5 Read-Only Transactions](#105-read-only-transactions)
    - [10.6 What Must Never Happen Inside a Transaction](#106-what-must-never-happen-inside-a-transaction)
    - [10.7 Timeouts](#107-timeouts)
    - [10.8 Rollback Rules](#108-rollback-rules)
  - [11. Money and Data Integrity](#11-money-and-data-integrity)
    - [11.1 Floating Point Is Prohibited for Money](#111-floating-point-is-prohibited-for-money)
    - [11.2 BigDecimal Rules](#112-bigdecimal-rules)
    - [11.3 The Money Type](#113-the-money-type)
    - [11.4 Database Column Types](#114-database-column-types)
    - [11.5 The Ledger Is Append-Only and Double-Entry](#115-the-ledger-is-append-only-and-double-entry)
    - [11.6 Idempotency Store](#116-idempotency-store)
    - [11.7 The Database Is the Last Line of Defence](#117-the-database-is-the-last-line-of-defence)
    - [11.8 Temporal Correctness](#118-temporal-correctness)
  - [12. Concurrency, Async and Scheduling](#12-concurrency-async-and-scheduling)
    - [12.1 Virtual Threads](#121-virtual-threads)
    - [12.2 Async Execution](#122-async-execution)
    - [12.3 Scheduling](#123-scheduling)
    - [12.4 Locking for Balance Mutation](#124-locking-for-balance-mutation)
    - [12.5 Shutdown](#125-shutdown)
  - [13. Messaging](#13-messaging)
    - [13.1 The Dual-Write Problem](#131-the-dual-write-problem)
    - [13.2 The Transactional Outbox](#132-the-transactional-outbox)
    - [13.3 Idempotent Consumers](#133-idempotent-consumers)
    - [13.4 Retry, Backoff and Dead Letters](#134-retry-backoff-and-dead-letters)
    - [13.5 Application Events Inside a Service](#135-application-events-inside-a-service)
    - [13.6 Ordering](#136-ordering)
  - [14. Caching](#14-caching)
    - [14.1 What Must Never Be Cached](#141-what-must-never-be-cached)
    - [14.2 Cache Configuration](#142-cache-configuration)
    - [14.3 Usage](#143-usage)
    - [14.4 Stampede Prevention](#144-stampede-prevention)
    - [14.5 Cache Failure Is Not Request Failure](#145-cache-failure-is-not-request-failure)
  - [15. Batch and End-of-Day Jobs](#15-batch-and-end-of-day-jobs)
    - [15.1 When to Use Spring Batch](#151-when-to-use-spring-batch)
    - [15.2 Job Structure](#152-job-structure)
    - [15.3 Restartability](#153-restartability)
    - [15.4 Reconciliation Is Mandatory](#154-reconciliation-is-mandatory)
    - [15.5 Batch Operational Rules](#155-batch-operational-rules)
  - [16. Resilience](#16-resilience)
    - [16.1 Every Outbound Call Has a Timeout](#161-every-outbound-call-has-a-timeout)
    - [16.2 Circuit Breakers](#162-circuit-breakers)
    - [16.3 Retry Rules](#163-retry-rules)
    - [16.4 Bulkheads](#164-bulkheads)
    - [16.5 Health Checks](#165-health-checks)
  - [17. Observability](#17-observability)
    - [17.1 Correlation Identifiers](#171-correlation-identifiers)
    - [17.2 Structured Logging](#172-structured-logging)
    - [17.3 What Must Never Be Logged](#173-what-must-never-be-logged)
    - [17.4 Log Levels](#174-log-levels)
    - [17.5 Metrics](#175-metrics)
    - [17.6 Tracing](#176-tracing)
  - [18. Testing](#18-testing)
    - [18.1 Test Types and Proportions](#181-test-types-and-proportions)
    - [18.2 Coverage Requirements](#182-coverage-requirements)
    - [18.3 Unit Tests Use No Spring Context](#183-unit-tests-use-no-spring-context)
    - [18.4 Test Naming](#184-test-naming)
    - [18.5 Slice Tests](#185-slice-tests)
    - [18.6 Integration Tests Use a Real Database](#186-integration-tests-use-a-real-database)
    - [18.7 Concurrency Tests](#187-concurrency-tests)
    - [18.8 What Must Be Tested](#188-what-must-be-tested)
  - [19. Dependency and Supply Chain](#19-dependency-and-supply-chain)
    - [19.1 Software Bill of Materials](#191-software-bill-of-materials)
    - [19.2 Vulnerability Gating](#192-vulnerability-gating)
    - [19.3 Build Reproducibility](#193-build-reproducibility)
    - [19.4 Licence Policy](#194-licence-policy)
  - [20. Performance](#20-performance)
    - [20.1 Targets](#201-targets)
    - [20.2 The Usual Causes](#202-the-usual-causes)
    - [20.3 Query Verification](#203-query-verification)
    - [20.4 Streaming Large Result Sets](#204-streaming-large-result-sets)
    - [20.5 JVM Settings](#205-jvm-settings)
  - [21. Common Pitfalls to Avoid](#21-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

**Why this document exists**: Spring Boot removes a great deal of boilerplate, and in doing so it hides behaviour that matters enormously in a banking context. Auto-configuration decides your transaction boundaries, your connection pool size, your JSON serialization, and your error responses — silently, and with defaults chosen for general-purpose web applications, not for systems that move money and hold regulated customer data.

The failure modes that follow are specific and recurring:

- A `@Transactional` method calling another method on the same bean, so the transaction never starts, and a partial debit is committed without the matching credit.
- A `double` used for a balance, so a reconciliation run is off by fractions of a currency unit across millions of rows.
- A retry on a non-idempotent transfer endpoint, so a customer is debited twice.
- A JPA entity returned straight from a controller, so a password hash or an internal risk score is serialized to the client.
- Open Session In View left at its default, so lazy loading silently succeeds in development and produces N+1 queries under production load.
- An `@Scheduled` end-of-day job running on all four instances simultaneously, so interest is posted four times.

Every rule in this document exists because one of these classes of failure is expensive, hard to detect, and in a banking context, reportable.

**In scope**: Spring Boot 3.3+ application structure, configuration, DI, REST layer, validation, error handling, Spring Data JPA persistence, transactions, monetary correctness and ledger integrity, concurrency and scheduling, messaging, caching, batch, resilience, observability, testing, dependency and supply-chain management, and performance.

**Out of scope** (covered by [ESTD21](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#estd21---data-protection-security-and-audit-standards-for-spring-boot-banking-services)): authentication, authorization, encryption at rest, masking and tokenization, secrets management, injection defence, audit trail, PCI DSS scope, GDPR/DPDP compliance, and incident response.

**Also out of scope**: infrastructure provisioning, CI/CD pipeline authoring, and network topology. These are owned by the platform team and governed by the client's own infrastructure standards.

---

## 2. Baseline Versions and Build

### 2.1 Mandated Versions

| Component | Version | Notes |
|:----------|:--------|:------|
| Java | **21 LTS** | Latest patch release. Records, sealed types, pattern matching, and virtual threads are all available and expected. |
| Spring Boot | **3.3.x or later** | Jakarta EE 10 namespace (`jakarta.*`, never `javax.*`). |
| Spring Framework | 6.1+ | Comes with Boot; never pinned independently. |
| Spring Security | 6.3+ | Comes with Boot. |
| Build tool | **Maven** | Gradle requires written approval. One build tool across the estate keeps the CI templates, SBOM generation, and vulnerability gates uniform. |
| Database | **PostgreSQL 15+** | |
| Migration tool | **Flyway** | |
| Connection pool | **HikariCP** | Boot default; do not replace. |

Running an unsupported Spring Boot version is a release blocker. The Spring Boot OSS support window is roughly 13 months from a minor release; a service must be on a supported line before that window closes, and the upgrade must be scheduled, not deferred.

### 2.2 Version Management via BOM

All Spring dependency versions come from the Spring Boot BOM. Never pin a Spring artifact version by hand — a hand-pinned version diverges from what the BOM tested together, and the resulting incompatibilities surface at runtime, not at build time.

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.5</version>
    <relativePath/>
</parent>

<properties>
    <java.version>21</java.version>
    <!-- Non-Spring versions are pinned here, explicitly, one property per library -->
    <resilience4j.version>2.2.0</resilience4j.version>
    <shedlock.version>5.16.0</shedlock.version>
</properties>

<dependencies>
    <!-- GOOD — version comes from the BOM -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- GOOD — non-Spring dependency pinned to an exact version via a property -->
    <dependency>
        <groupId>io.github.resilience4j</groupId>
        <artifactId>resilience4j-spring-boot3</artifactId>
        <version>${resilience4j.version}</version>
    </dependency>
</dependencies>
```

### 2.3 Dependency Rules

- **Every version is exact.** No version ranges (`[1.0,2.0)`), no `LATEST`, no `RELEASE`. A range means the artifact you tested is not necessarily the artifact you ship.
- **No `SNAPSHOT` dependencies** in any branch that can be promoted beyond the development environment.
- **No dependency added without review.** A new third-party library is a permanent liability: it must be maintained, patched, and license-cleared. Adding one requires an explicit note in the PR description stating what it does, why an existing dependency cannot do it, and its license.
- **Test dependencies are `test`-scoped.** JUnit, Mockito, AssertJ, Testcontainers, and WireMock must never reach the production artifact.
- **Prefer the platform.** Before adding a library, check whether Spring Boot, the JDK, or an already-present dependency solves the problem.

### 2.4 Compiler and Build Enforcement

The build must fail — not warn — on any of the following:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <release>21</release>
        <compilerArgs>
            <arg>-Xlint:all</arg>
            <arg>-Werror</arg>          <!-- Warnings are errors -->
            <arg>-parameters</arg>       <!-- Required for constructor binding and JPA -->
        </compilerArgs>
    </configuration>
</plugin>
```

`-parameters` is not optional. Without it, `@ConfigurationProperties` constructor binding and several Spring Data derived-query mechanisms fall back on reflection heuristics that break under obfuscation or minimal builds.

---

## 3. Project and Package Structure

### 3.1 Canonical Package Layout

One service, one root package, `com.<institution>.<service>`. Packages are organized by **layer inside feature**, not by layer across the whole service — a change to the transfer feature should touch one directory tree, not five.

```
com.institution.payments/
├── PaymentsApplication.java          ← @SpringBootApplication, nothing else in it
├── config/                           ← @Configuration classes only
│   ├── JacksonConfig.java
│   ├── AsyncConfig.java
│   └── properties/                   ← @ConfigurationProperties records
│       └── TransferLimitProperties.java
├── transfer/                         ← feature package
│   ├── api/                          ← controllers + request/response DTOs
│   │   ├── TransferController.java
│   │   ├── TransferRequest.java
│   │   └── TransferResponse.java
│   ├── domain/                       ← entities, value objects, domain exceptions
│   │   ├── Transfer.java
│   │   ├── TransferStatus.java
│   │   └── TransferLimitExceededException.java
│   ├── service/                      ← business logic
│   │   ├── TransferService.java
│   │   └── TransferLimitPolicy.java
│   └── repository/                   ← Spring Data repositories
│       └── TransferRepository.java
├── account/                          ← feature package, same internal shape
├── ledger/                           ← feature package, same internal shape
└── shared/                           ← used by two or more features, nothing else
    ├── money/
    │   └── Money.java
    ├── error/
    │   ├── ApiErrorCode.java
    │   └── GlobalExceptionHandler.java
    └── correlation/
        └── CorrelationIdFilter.java
```

**The `shared` rule**: a class moves into `shared/` only when a second feature actually needs it. Anticipating shared use produces a `shared/` package that becomes the service's dumping ground and its worst coupling point.

### 3.2 Layer Responsibilities

| Layer | Owns | Must Not |
|:------|:-----|:---------|
| `api` | HTTP concerns: routing, deserialization, validation triggering, status codes, response shaping | Contain business rules; touch repositories; expose entities |
| `service` | Business logic, orchestration, transaction boundaries, policy decisions | Reference `HttpServletRequest`, `ResponseEntity`, or any Spring Web type |
| `repository` | Data access, query definition, result mapping | Contain business rules or make decisions about what the data means |
| `domain` | Entities, value objects, invariant enforcement, domain exceptions | Depend on Spring Web, Spring Data, or any infrastructure type |

The service layer containing no Spring Web types is the rule that keeps the business logic testable. If `TransferService` needs the caller's identity, it takes a `CustomerId` parameter — not a `Principal`, not an `Authentication`, not a request object.

### 3.3 Dependency Direction

```
                 ┌──────────────┐
   HTTP  ───────▶│     api      │
                 └──────┬───────┘
                        │  (DTO in, DTO out)
                        ▼
                 ┌──────────────┐
                 │   service    │◀────── config (properties injected)
                 └──────┬───────┘
                        │  (domain objects)
              ┌─────────┴─────────┐
              ▼                   ▼
       ┌─────────────┐     ┌─────────────┐
       │ repository  │     │   domain    │
       └──────┬──────┘     └─────────────┘
              │
              ▼
         PostgreSQL

PROHIBITED EDGES:
  repository ──▶ service      (inverted; repositories decide nothing)
  domain     ──▶ service      (domain must not know about orchestration)
  domain     ──▶ repository   (entities must not load their own collaborators)
  api        ──▶ repository   (skips the transaction boundary entirely)
  feature A  ──▶ feature B's repository or domain internals
```

Cross-feature access goes through the other feature's **service** interface, never its repository or entities. `TransferService` calls `AccountService.debit(...)`; it never calls `AccountRepository` directly. This is what allows a feature to change its persistence model without a ripple across the service.

### 3.4 Enforcing Structure with ArchUnit

Structure rules that are not enforced decay. Every service has an ArchUnit test that runs in the normal test phase:

```java
@AnalyzeClasses(packages = "com.institution.payments",
                importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {

    @ArchTest
    static final ArchRule layers_are_respected = layeredArchitecture()
        .consideringOnlyDependenciesInLayers()
        .layer("Api").definedBy("..api..")
        .layer("Service").definedBy("..service..")
        .layer("Repository").definedBy("..repository..")
        .layer("Domain").definedBy("..domain..")
        .whereLayer("Api").mayNotBeAccessedByAnyLayer()
        .whereLayer("Service").mayOnlyBeAccessedByLayers("Api")
        .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service");

    @ArchTest
    static final ArchRule services_are_free_of_web_types = noClasses()
        .that().resideInAPackage("..service..")
        .should().dependOnClassesThat()
        .resideInAnyPackage("org.springframework.web..", "jakarta.servlet..");

    @ArchTest
    static final ArchRule entities_never_leave_the_service_layer = noClasses()
        .that().resideInAPackage("..api..")
        .should().dependOnClassesThat().areAnnotatedWith(Entity.class);

    @ArchTest
    static final ArchRule no_field_injection = noFields()
        .should().beAnnotatedWith(Autowired.class)
        .because("constructor injection only — see ESTD20 section 5");
}
```

---

## 4. Application Bootstrap and Configuration

### 4.1 The Main Class Does Nothing

```java
// GOOD — the entry point declares the application and nothing more
@SpringBootApplication
public class PaymentsApplication {
    public static void main(String[] args) {
        SpringApplication.run(PaymentsApplication.class, args);
    }
}
```

No `@Bean` methods, no `@EnableScheduling`, no `CommandLineRunner`, no static state. Those belong in `config/` classes where they can be excluded from a slice test. A main class that accumulates configuration becomes the one class every integration test is forced to load.

### 4.2 Component Scanning Stays Narrow

`@SpringBootApplication` scans its own package downwards. Never widen it:

```java
// BAD — scans everything under com.institution, including other services' shared jars
@SpringBootApplication
@ComponentScan("com.institution")

// BAD — pulls in beans by class-path scanning of a library you do not control
@ComponentScan(basePackages = {"com.institution.payments", "com.vendor.sdk"})
```

Widening the scan means a transitive dependency can register a bean in your context. Beans from libraries are registered explicitly, by an `@Bean` method you wrote, in a `@Configuration` class you own.

### 4.3 Configuration Files and Profiles

```
src/main/resources/
├── application.yml            ← defaults shared by every environment; no secrets, no hosts
├── application-local.yml      ← developer machine
├── application-dev.yml
├── application-uat.yml
└── application-prod.yml       ← non-secret production values only
```

Rules:

- **The active profile is set by the environment**, via `SPRING_PROFILES_ACTIVE`. Never with `spring.profiles.active` in `application.yml` — a committed default profile is how a service ends up running with development settings in production.
- **No secrets in any `application*.yml` file**, ever, including local. Secrets come from the platform secrets manager; see [ESTD21 §10](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#10-secrets-management).
- **No environment-specific value in `application.yml`.** If it differs per environment, it belongs in the profile file or the environment.
- **`prod` is not the default.** A missing profile must fail startup, not silently select production.

```yaml
# application.yml — safe shared defaults
spring:
  application:
    name: payments-service
  jpa:
    open-in-view: false            # MANDATORY — see section 9.6
    hibernate:
      ddl-auto: validate           # MANDATORY — never create, update, or create-drop
    properties:
      hibernate.jdbc.batch_size: 50
      hibernate.order_inserts: true
      hibernate.order_updates: true
  jackson:
    default-property-inclusion: non_null
    deserialization:
      fail-on-unknown-properties: true    # MANDATORY — see section 7.4
  threads:
    virtual:
      enabled: true                # Java 21 virtual threads for request handling

server:
  shutdown: graceful               # Drain in-flight requests before exit
  error:
    include-message: never         # Never leak internal messages to clients
    include-stacktrace: never
    include-binding-errors: never

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus     # Explicit allowlist, never "*"
  endpoint:
    health:
      show-details: never
```

`ddl-auto: validate` is non-negotiable. `update` lets Hibernate silently alter a production schema based on entity annotations — an unreviewed, unversioned, unrecoverable change to a regulated datastore.

### 4.4 Typed Configuration, Not Scattered `@Value`

`@Value` spreads configuration keys across the codebase as unvalidated strings. A typo produces a runtime failure at first use, which in a rarely-exercised path can mean weeks later. Use `@ConfigurationProperties` records with validation:

```java
// GOOD — typed, validated, immutable, discoverable, fails at startup
@Validated
@ConfigurationProperties(prefix = "payments.transfer")
public record TransferLimitProperties(

    @NotNull @DecimalMin("0.01")
    BigDecimal singleTransactionMax,

    @NotNull @DecimalMin("0.01")
    BigDecimal dailyTotalMax,

    @NotNull @Min(1) @Max(100)
    Integer maxPayeesPerCustomer,

    @NotNull
    Duration idempotencyKeyTtl
) {}
```

```java
@Configuration
@EnableConfigurationProperties(TransferLimitProperties.class)
public class PaymentsConfig { }
```

```yaml
payments:
  transfer:
    single-transaction-max: 50000.00
    daily-total-max: 200000.00
    max-payees-per-customer: 50
    idempotency-key-ttl: PT24H
```

A missing or invalid value now fails the application context at startup with a message naming the property. That is the correct time to find out.

`@Value` is acceptable only for a single-use value inside a `@Configuration` class. It is never acceptable in a service, controller, or component.

### 4.5 Fail Fast

A service must refuse to start rather than start degraded. Validate at startup anything whose absence would cause a silent behavioural change:

```java
@Component
public class StartupValidator implements ApplicationRunner {

    private final Environment environment;
    private final DataSource dataSource;

    public StartupValidator(Environment environment, DataSource dataSource) {
        this.environment = environment;
        this.dataSource  = dataSource;
    }

    @Override
    public void run(ApplicationArguments args) {
        if (environment.getActiveProfiles().length == 0) {
            throw new IllegalStateException(
                "No active Spring profile. Set SPRING_PROFILES_ACTIVE explicitly.");
        }
        if (environment.matchesProfiles("prod")
                && environment.matchesProfiles("local", "dev")) {
            throw new IllegalStateException(
                "Profile 'prod' must not be combined with a non-production profile.");
        }
        try (Connection connection = dataSource.getConnection()) {
            if (!connection.isValid(2)) {
                throw new IllegalStateException("Database connection is not valid at startup.");
            }
        } catch (SQLException e) {
            throw new IllegalStateException("Cannot reach the database at startup.", e);
        }
    }
}
```

### 4.6 Configuration Precedence

```
Code defaults  ←  application.yml  ←  application-{profile}.yml  ←  Environment variables  ←  Secrets manager
     (lowest)                                                                                      (highest)
```

Later sources win. This is the order Spring Boot already applies; the rule is not to fight it — no `@PropertySource` overrides, no programmatic property mutation, no reading `System.getenv` directly in business code.

---

## 5. Dependency Injection and Bean Design

### 5.1 Constructor Injection Only

```java
// GOOD — final fields, explicit dependencies, no Spring annotation needed on the constructor
@Service
public class TransferService {

    private final AccountService        accountService;
    private final LedgerService         ledgerService;
    private final TransferRepository    transferRepository;
    private final TransferLimitProperties limits;

    public TransferService(AccountService accountService,
                           LedgerService ledgerService,
                           TransferRepository transferRepository,
                           TransferLimitProperties limits) {
        this.accountService     = accountService;
        this.ledgerService      = ledgerService;
        this.transferRepository = transferRepository;
        this.limits             = limits;
    }
}
```

Since Spring 4.3, a class with a single constructor needs no `@Autowired`. Do not add one.

```java
// BAD — field injection
@Service
public class TransferService {
    @Autowired private AccountService accountService;   // PROHIBITED
}
```

Field injection is prohibited because it makes the dependency invisible to the compiler, impossible to make `final`, impossible to construct in a plain unit test without reflection, and it hides the fact that a class has acquired eleven collaborators.

**A constructor with more than five dependencies is a design signal, not a formatting problem.** The class is doing too much; split it.

### 5.2 Bean Scope

Beans are **singletons** and therefore **stateless**. A `@Service` with a mutable field is a data race that will corrupt one customer's request with another's data under concurrency.

```java
// CATASTROPHIC — shared mutable state on a singleton
@Service
public class TransferService {
    private BigDecimal runningTotal;              // PROHIBITED
    private Customer currentCustomer;             // PROHIBITED — cross-customer data leak
}
```

Request-scoped and session-scoped beans are prohibited for services performing I/O. Per-request state travels as method parameters or as an explicit context object passed down the call chain.

`static` mutable fields are prohibited outright, with the sole exception of `static final` constants of immutable types.

### 5.3 No Circular Dependencies

Spring Boot 2.6+ rejects circular references by default. **`spring.main.allow-circular-references: true` is prohibited.** A cycle means the two classes are one responsibility split in the wrong place. Fix it by extracting the shared logic into a third bean, or by inverting one direction with an event ([§13.5](#135-application-events-inside-a-service)).

### 5.4 Qualifiers and Multiple Implementations

When an interface has more than one implementation, name each bean and inject by name. `@Primary` is a last resort — it makes the selected implementation invisible at the injection site.

```java
@Component("sepaTransferExecutor")
public class SepaTransferExecutor implements TransferExecutor { }

@Component("internalTransferExecutor")
public class InternalTransferExecutor implements TransferExecutor { }

@Service
public class TransferService {
    private final Map<TransferRail, TransferExecutor> executors;

    // Spring injects all implementations; the map key is the bean name
    public TransferService(Map<String, TransferExecutor> beans) {
        this.executors = Map.of(
            TransferRail.SEPA,     beans.get("sepaTransferExecutor"),
            TransferRail.INTERNAL, beans.get("internalTransferExecutor"));
    }
}
```

### 5.5 Lifecycle Callbacks

Use `@PostConstruct` for cheap, local initialization only. Never open network connections, load reference data, or call another service from it — a failure there produces an opaque context-startup error, and a slow call there delays every instance's readiness. Work of that kind belongs in an `ApplicationRunner` or behind a health-gated warm-up.

---

## 6. REST API Standards

### 6.1 URL Design

```
/api/v1/accounts                                  Collection
/api/v1/accounts/{accountId}                      Single resource
/api/v1/accounts/{accountId}/transactions         Sub-collection
/api/v1/transfers                                 Action modelled as a resource
/api/v1/payees/{payeeId}
```

- Plural nouns for collections.
- Lower-case, hyphen-separated multi-word segments (`/standing-orders`, never `/standingOrders`).
- **No verbs in paths.** `POST /api/v1/transfers` creates a transfer; `POST /api/v1/accounts/{id}/close-account` does not exist — it is `POST /api/v1/accounts/{id}/closure`.
- **Never put an identifier of a sensitive kind in the path or query string.** Account numbers, card numbers, and national identifiers go in the body. See [ESTD21 §8](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#8-data-in-transit-and-in-use).
- Nesting stops at two levels. Deeper nesting is a sign the sub-resource deserves its own top-level path.

### 6.2 Versioning

The major version is in the path (`/api/v1/`). It changes only for a breaking change: a removed or renamed field, a narrowed type, a changed error code, or a changed default. Adding an optional field is not breaking.

When `v2` ships, `v1` remains available for a minimum of **six months** and its retirement date is published with the `v2` release. Both versions are served by the same service; the controller for the old version maps to the same service layer and adapts the response shape.

### 6.3 HTTP Methods and Status Codes

| Method | Semantics | Idempotent | Body |
|:-------|:----------|:-----------|:-----|
| `GET` | Retrieve | Yes | Never |
| `POST` | Create, or execute a state-changing action | **No** — requires an idempotency key when it moves money | Yes |
| `PUT` | Full replace | Yes | Yes |
| `PATCH` | Partial update | No | Yes |
| `DELETE` | Remove or soft-delete | Yes | Rarely |

| Status | Use For |
|:-------|:--------|
| 200 | Successful `GET`, `PUT`, `PATCH` |
| 201 | Resource created; `Location` header mandatory |
| 202 | Accepted for asynchronous processing; response carries a status URL |
| 204 | Successful `DELETE` with no body |
| 400 | Malformed request or validation failure |
| 401 | Missing or invalid credentials |
| 403 | Authenticated, but not permitted |
| 404 | Resource does not exist, **or exists but the caller may not know it does** |
| 409 | Conflict: duplicate, optimistic-lock failure, illegal state transition |
| 422 | Syntactically valid but semantically rejected (insufficient funds, limit exceeded) |
| 429 | Rate limited; `Retry-After` header mandatory |
| 500 | Unhandled internal failure; never carries internal detail |
| 503 | Dependency unavailable or shutting down |

**404 over 403 for resources the caller does not own.** Returning 403 for another customer's account confirms that the account exists. Return 404. This is an information-disclosure rule, not a style preference.

### 6.4 Entities Never Cross the Controller Boundary

```java
// PROHIBITED — returns the JPA entity
@GetMapping("/{accountId}")
public Account getAccount(@PathVariable UUID accountId) {
    return accountRepository.findById(accountId).orElseThrow();
}
```

This leaks every column the entity maps — including fields added later by someone who did not know this endpoint existed. It also triggers lazy-loading during serialization, and it couples the wire contract to the schema so a column rename becomes a breaking API change.

```java
// GOOD — explicit response record, constructed from the domain object
public record AccountResponse(
    UUID          accountId,
    String        maskedAccountNumber,
    String        accountName,
    String        currency,
    BigDecimal    availableBalance,
    BigDecimal    ledgerBalance,
    AccountStatus status,
    Instant       openedAt
) {
    public static AccountResponse from(Account account) {
        return new AccountResponse(
            account.getId(),
            AccountNumberMasker.mask(account.getAccountNumber()),
            account.getName(),
            account.getCurrency().getCurrencyCode(),
            account.getAvailableBalance(),
            account.getLedgerBalance(),
            account.getStatus(),
            account.getOpenedAt());
    }
}
```

### 6.5 Controller Shape

A controller method does exactly six things and nothing else: bind, validate, resolve the caller, delegate, map the result, set the status.

```java
@RestController
@RequestMapping("/api/v1/transfers")
public class TransferController {

    private final TransferService transferService;

    public TransferController(TransferService transferService) {
        this.transferService = transferService;
    }

    @PostMapping
    public ResponseEntity<TransferResponse> createTransfer(
            @Valid @RequestBody TransferRequest request,
            @RequestHeader("Idempotency-Key") @NotBlank @Size(max = 64) String idempotencyKey,
            @AuthenticationPrincipal CustomerPrincipal principal) {

        TransferResult result = transferService.execute(
            principal.customerId(),
            request.toCommand(),
            IdempotencyKey.of(idempotencyKey));

        TransferResponse body = TransferResponse.from(result);

        return ResponseEntity
            .created(URI.create("/api/v1/transfers/" + result.transferId()))
            .body(body);
    }
}
```

No business rules, no try-catch (the global handler in [§8](#8-error-handling) owns that), no repository access, no transaction annotation.

### 6.6 Pagination

Every endpoint that can return more than one row is paginated, with a hard server-side maximum. An unpaginated list endpoint against a table that grows is an availability incident waiting for a large customer.

```java
@GetMapping("/{accountId}/transactions")
public PagedResponse<TransactionResponse> listTransactions(
        @PathVariable UUID accountId,
        @RequestParam(defaultValue = "0")  @Min(0)  int page,
        @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size,
        @AuthenticationPrincipal CustomerPrincipal principal) {

    // Sort is NEVER taken from the request as a raw string — see ESTD21 section 11
    Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "bookedAt"));
    ...
}
```

For statement and transaction history, prefer **keyset (cursor) pagination** over offset pagination. `OFFSET 100000` makes PostgreSQL scan and discard 100,000 rows on every page.

```java
// Keyset pagination — constant cost regardless of depth
@Query("""
       SELECT t FROM LedgerEntry t
       WHERE t.accountId = :accountId
         AND (t.bookedAt < :cursorBookedAt
              OR (t.bookedAt = :cursorBookedAt AND t.id < :cursorId))
       ORDER BY t.bookedAt DESC, t.id DESC
       """)
List<LedgerEntry> findPageAfter(@Param("accountId")       UUID    accountId,
                                @Param("cursorBookedAt")  Instant cursorBookedAt,
                                @Param("cursorId")        UUID    cursorId,
                                Limit limit);
```

### 6.7 Idempotency on Money-Moving Endpoints

Every `POST` that moves money, opens or closes an account, or creates an irreversible record **must** require an `Idempotency-Key` header. Networks retry, clients retry, users double-tap. Without this, a retried transfer is a second transfer.

The key is stored with the request fingerprint and the response, inside the same transaction that performs the work. See [§11.6](#116-idempotency-store) for the implementation.

### 6.8 Request and Response Conventions

- `Content-Type: application/json` only. No form encoding, no XML.
- All timestamps are ISO-8601 UTC with an offset: `2026-09-02T14:31:07Z`. Never epoch millis, never a local time without an offset.
- Monetary amounts are JSON **strings**, not numbers: `"amount": "1250.00"`. A JSON number goes through an IEEE-754 double in most client parsers, which is exactly the precision loss [§11](#11-money-and-data-integrity) exists to prevent.
- Every currency amount is accompanied by its ISO-4217 currency code. An amount without a currency is not a valid amount.
- Enumerations are `UPPER_SNAKE_CASE` strings, never ordinals.
- Every response carries the `X-Correlation-Id` that the request carried or that the service generated.

```json
{
  "transferId": "3f2a9c11-8f4e-4c2b-9a10-6d4c2e7b1a55",
  "status": "COMPLETED",
  "amount": "1250.00",
  "currency": "EUR",
  "debitAccountId": "9c1b...",
  "creditAccountId": "44ad...",
  "bookedAt": "2026-09-02T14:31:07Z"
}
```

---

## 7. Input Validation

### 7.1 Validate at the Boundary, Reject Everything Else

Every value entering the service from outside is untrusted until validated: request bodies, path variables, query parameters, headers, message payloads, and file contents. Validation happens once, at the boundary, before any business logic runs.

Validation answers "is this well-formed and within permitted bounds". It is not authorization ("may this caller do it") and not business rules ("does the account have the funds") — those are separate checks in the service layer.

### 7.2 Jakarta Validation on Request Records

```java
public record TransferRequest(

    @NotNull(message = "debitAccountId is required")
    UUID debitAccountId,

    @NotBlank
    @Pattern(regexp = "^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$",
             message = "creditIban must be a valid IBAN")
    String creditIban,

    @NotBlank @Size(max = 140)
    String creditorName,

    @NotNull
    @DecimalMin(value = "0.01", message = "amount must be positive")
    @DecimalMax(value = "9999999999.99")
    @Digits(integer = 10, fraction = 2, message = "amount must have at most 2 decimal places")
    BigDecimal amount,

    @NotNull
    @Pattern(regexp = "^[A-Z]{3}$", message = "currency must be an ISO-4217 code")
    String currency,

    @Size(max = 140)
    @Pattern(regexp = "^[\\p{L}\\p{N} .,/()'+-]*$",
             message = "reference contains unsupported characters")
    String reference,

    @Future
    LocalDate executionDate
) {}
```

Notes on this example that generalize:

- **`@Digits(fraction = 2)` on every monetary field.** Without it, a client can send `10.005` and the scale is silently decided elsewhere.
- **`@Size(max = ...)` on every string.** An unbounded string is a memory and storage attack.
- **Allowlist patterns, not denylists.** `^[\p{L}\p{N} .,/()'+-]*$` states what is permitted. A denylist is always incomplete.
- **`@DecimalMax` on amounts.** An upper bound catches both fat-finger errors and deliberate overflow probing.

### 7.3 Custom Constraints for Domain Types

Domain rules that repeat get a constraint annotation, so they cannot be forgotten and cannot drift between endpoints.

```java
@Documented
@Constraint(validatedBy = IbanValidator.class)
@Target({ElementType.FIELD, ElementType.PARAMETER, ElementType.RECORD_COMPONENT})
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidIban {
    String message() default "must be a valid IBAN";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

public class IbanValidator implements ConstraintValidator<ValidIban, String> {

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null) {
            return true;                       // Nullability is @NotNull's job, not ours
        }
        return IbanChecksum.isValid(value);    // ISO 13616 mod-97 check
    }
}
```

A validator returns `true` for `null`. Combining `@NotNull` with a format constraint keeps the two concerns separable and the error messages accurate.

### 7.4 Reject Unknown Properties

```yaml
spring:
  jackson:
    deserialization:
      fail-on-unknown-properties: true
```

An unknown field in a request body means the client and the server disagree about the contract. Silently ignoring it hides a client bug until a payment goes out with a field the server never read. Reject it with a 400.

### 7.5 Validating Nested and Collection Inputs

`@Valid` does not cascade automatically. It must be declared on the nested field:

```java
public record BulkTransferRequest(
    @NotEmpty @Size(max = 500)
    @Valid                                   // Without this, each element is unvalidated
    List<TransferInstruction> instructions,

    @NotNull @Valid
    BatchMetadata metadata
) {}
```

The `@Size(max = 500)` bound is as important as the `@Valid`. An unbounded collection in a request body is a denial-of-service vector.

### 7.6 Validating Path Variables and Parameters

Constraints on method parameters require `@Validated` on the class:

```java
@Validated
@RestController
@RequestMapping("/api/v1/accounts")
public class AccountController {

    @GetMapping("/{accountId}/statements")
    public StatementResponse getStatement(
            @PathVariable UUID accountId,
            @RequestParam @Min(2000) @Max(2100) int year,
            @RequestParam @Min(1) @Max(12) int month) { ... }
}
```

These produce `ConstraintViolationException` rather than `MethodArgumentNotValidException`; both are handled in [§8.3](#83-the-global-exception-handler).

### 7.7 Server-Side Business Validation Is Separate and Mandatory

Bean Validation checks shape. It does not check that the debit account belongs to the caller, that it is not frozen, that the daily limit is not exceeded, or that the funds exist. Those checks live in the service layer, run inside the transaction, and are never delegated to the client. A rule enforced only in the client is not enforced.

---

## 8. Error Handling

### 8.1 Exception Hierarchy

One base type per service, extending `RuntimeException`. Checked exceptions add signature noise without improving safety in a framework-managed request model.

```java
public abstract class BankingException extends RuntimeException {

    private final ApiErrorCode errorCode;

    protected BankingException(ApiErrorCode errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    protected BankingException(ApiErrorCode errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }

    public ApiErrorCode errorCode() {
        return errorCode;
    }
}

// Domain — the caller did something the domain rejects
public class AccountNotFoundException      extends BankingException { }
public class AccountFrozenException        extends BankingException { }
public class InsufficientFundsException    extends BankingException { }
public class TransferLimitExceededException extends BankingException { }
public class DuplicateRequestException     extends BankingException { }
public class PayeeNotWhitelistedException  extends BankingException { }

// Infrastructure — something outside the domain failed
public class DownstreamUnavailableException extends BankingException { }
public class LedgerWriteException           extends BankingException { }
```

**`InsufficientFundsException` never carries the balance.** The exception message reaches logs and, if the handler is ever careless, the client. The available balance is not something a failed transfer attempt is entitled to reveal.

### 8.2 The Error Code Catalogue

Clients switch on a stable code, not on an HTTP status or a message string. Messages change; codes do not.

```java
public enum ApiErrorCode {
    ACCOUNT_NOT_FOUND        (HttpStatus.NOT_FOUND),
    ACCOUNT_FROZEN           (HttpStatus.UNPROCESSABLE_ENTITY),
    INSUFFICIENT_FUNDS       (HttpStatus.UNPROCESSABLE_ENTITY),
    TRANSFER_LIMIT_EXCEEDED  (HttpStatus.UNPROCESSABLE_ENTITY),
    PAYEE_NOT_WHITELISTED    (HttpStatus.UNPROCESSABLE_ENTITY),
    DUPLICATE_REQUEST        (HttpStatus.CONFLICT),
    CONCURRENT_MODIFICATION  (HttpStatus.CONFLICT),
    VALIDATION_FAILED        (HttpStatus.BAD_REQUEST),
    RATE_LIMITED             (HttpStatus.TOO_MANY_REQUESTS),
    DOWNSTREAM_UNAVAILABLE   (HttpStatus.SERVICE_UNAVAILABLE),
    INTERNAL_ERROR           (HttpStatus.INTERNAL_SERVER_ERROR);

    private final HttpStatus status;

    ApiErrorCode(HttpStatus status) { this.status = status; }

    public HttpStatus status() { return status; }
}
```

Codes are additive. Removing or repurposing a code is a breaking API change.

### 8.3 The Global Exception Handler

All error-to-response mapping happens in one `@RestControllerAdvice`. Controllers contain no `try-catch`.

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(BankingException.class)
    public ProblemDetail handleBanking(BankingException e, HttpServletRequest request) {
        ApiErrorCode code = e.errorCode();

        if (code.status().is5xxServerError()) {
            log.error("Banking failure. code={}, path={}", code, request.getRequestURI(), e);
        } else {
            // Expected business outcome — INFO, no stack trace, no PII
            log.info("Request rejected. code={}, path={}", code, request.getRequestURI());
        }
        return problem(code, safeMessage(code), request);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleBodyValidation(MethodArgumentNotValidException e,
                                              HttpServletRequest request) {
        ProblemDetail problem = problem(ApiErrorCode.VALIDATION_FAILED,
                                        "One or more fields are invalid.", request);
        // Field names and constraint messages only — never the rejected value
        problem.setProperty("violations", e.getBindingResult().getFieldErrors().stream()
            .map(fe -> Map.of("field", fe.getField(),
                              "message", Objects.requireNonNullElse(fe.getDefaultMessage(), "invalid")))
            .toList());
        return problem;
    }

    @ExceptionHandler(ConstraintViolationException.class)
    public ProblemDetail handleParamValidation(ConstraintViolationException e,
                                               HttpServletRequest request) {
        return problem(ApiErrorCode.VALIDATION_FAILED,
                       "One or more parameters are invalid.", request);
    }

    @ExceptionHandler(OptimisticLockingFailureException.class)
    public ProblemDetail handleConcurrentModification(OptimisticLockingFailureException e,
                                                      HttpServletRequest request) {
        log.warn("Optimistic lock conflict. path={}", request.getRequestURI());
        return problem(ApiErrorCode.CONCURRENT_MODIFICATION,
                       "The resource was modified concurrently. Retry the request.", request);
    }

    // Final safety net. Nothing escapes past this point.
    @ExceptionHandler(Exception.class)
    public ProblemDetail handleUnexpected(Exception e, HttpServletRequest request) {
        log.error("Unhandled exception. path={}, method={}",
                  request.getRequestURI(), request.getMethod(), e);
        return problem(ApiErrorCode.INTERNAL_ERROR,
                       "An unexpected error occurred.", request);
    }

    private ProblemDetail problem(ApiErrorCode code, String detail, HttpServletRequest request) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(code.status(), detail);
        problem.setTitle(code.name());
        problem.setProperty("errorCode", code.name());
        problem.setProperty("correlationId", MDC.get("correlationId"));
        problem.setProperty("timestamp", Instant.now().toString());
        // No path, no stack trace, no exception class name, no SQL
        return problem;
    }

    private String safeMessage(ApiErrorCode code) {
        return ErrorMessages.forCode(code);   // Curated, client-safe text — never e.getMessage()
    }
}
```

Two rules in that class carry most of the weight:

1. **`e.getMessage()` is never returned to the client.** Exception messages routinely contain account identifiers, SQL fragments, table names, and internal hostnames. The client gets curated text keyed by error code.
2. **The correlation id is in every error response.** It is what turns a customer's support call into a log query.

### 8.4 Error Response Shape

RFC 9457 `ProblemDetail`, `Content-Type: application/problem+json`:

```json
{
  "type": "about:blank",
  "title": "INSUFFICIENT_FUNDS",
  "status": 422,
  "detail": "The transfer could not be completed.",
  "errorCode": "INSUFFICIENT_FUNDS",
  "correlationId": "0b7c5a9e-4d1f-4a6b-9c33-8e2f7d1a4b60",
  "timestamp": "2026-09-02T14:31:07Z"
}
```

### 8.5 Where to Catch, and Where Not To

Catch an exception only when you can do something meaningful with it: translate it into a domain exception that carries more context, apply a fallback, or add information the caller needs.

```java
// GOOD — translation adds meaning and preserves the cause
try {
    sanctionsClient.screen(request);
} catch (RestClientException e) {
    throw new DownstreamUnavailableException(
        ApiErrorCode.DOWNSTREAM_UNAVAILABLE, "Sanctions screening unavailable", e);
}

// BAD — catch, log, rethrow the same thing: duplicate logs, no added value
try {
    ledgerService.post(entries);
} catch (LedgerWriteException e) {
    log.error("Ledger write failed", e);
    throw e;
}

// CATASTROPHIC — swallowing a failure on a money path
try {
    ledgerService.post(entries);
} catch (Exception e) {
    log.warn("Ledger write failed, continuing");   // The debit happened. The credit did not.
}
```

**Never catch `Exception` in a service or repository method.** The only place that catches `Exception` is the global handler's safety net.

**Never catch an exception inside a `@Transactional` method and continue.** Once a runtime exception has been thrown inside a transaction, Spring has already marked it rollback-only; continuing produces an `UnexpectedRollbackException` at commit, with the original cause long gone.

---

## 9. Persistence with Spring Data JPA

### 9.1 Entity Rules

```java
@Entity
@Table(name = "account",
       indexes = {
           @Index(name = "ix_account_customer_id", columnList = "customer_id"),
           @Index(name = "ix_account_status",      columnList = "status")
       })
public class Account {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "customer_id", nullable = false, updatable = false)
    private UUID customerId;

    @Column(name = "account_number", nullable = false, unique = true, updatable = false, length = 34)
    private String accountNumber;

    @Column(name = "currency", nullable = false, length = 3, updatable = false)
    private String currency;

    @Column(name = "ledger_balance", nullable = false, precision = 19, scale = 4)
    private BigDecimal ledgerBalance;

    @Column(name = "available_balance", nullable = false, precision = 19, scale = 4)
    private BigDecimal availableBalance;

    @Enumerated(EnumType.STRING)                       // NEVER EnumType.ORDINAL
    @Column(name = "status", nullable = false, length = 32)
    private AccountStatus status;

    @Version                                           // Optimistic locking — see 9.5
    @Column(name = "version", nullable = false)
    private long version;

    @Column(name = "opened_at", nullable = false, updatable = false)
    private Instant openedAt;

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    protected Account() { }                            // JPA only; not public
}
```

Rules visible above, each with a reason:

- **`@Enumerated(EnumType.STRING)` always.** `ORDINAL` stores the enum's position. Inserting a new constant in the middle silently reinterprets every existing row.
- **`precision = 19, scale = 4` on every monetary column.** See [§11](#11-money-and-data-integrity).
- **`updatable = false` on immutable columns.** The mapping enforces what the domain intends.
- **`nullable = false` mirrors the database constraint.** JPA's annotation does not create the constraint at runtime under `ddl-auto: validate` — the Flyway migration does. They must agree, or validation fails at startup, which is the point.
- **`Instant` for timestamps, never `LocalDateTime`.** A timestamp without a zone in a banking system is an incident waiting for a daylight-saving transition.
- **A `protected` no-arg constructor.** Required by JPA, not part of the public API.

**Lombok is prohibited on entities.** `@Data` generates `equals`, `hashCode`, and `toString` over all fields — which triggers lazy loading, breaks identity semantics for detached entities, and prints the entire object graph, including regulated data, into logs.

### 9.2 Entity Identity

`equals` and `hashCode` on an entity are based on the business key or the assigned identifier only — never on all fields, and never on a database-generated identifier that is null before persist.

```java
@Override
public boolean equals(Object other) {
    if (this == other) return true;
    if (!(other instanceof Account that)) return false;
    return id != null && id.equals(that.id);
}

@Override
public int hashCode() {
    return Account.class.hashCode();      // Stable across the entity's lifecycle
}
```

### 9.3 Associations Are Lazy

```java
// PROHIBITED — @ManyToOne and @OneToOne default to EAGER
@ManyToOne
private Customer customer;

// GOOD — explicit and lazy
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "customer_id", insertable = false, updatable = false)
private Customer customer;
```

`@ManyToOne` and `@OneToOne` are eager by default. Loading one `Account` then pulls the `Customer`, and whatever that pulls, in a chain nobody asked for.

**`CascadeType.ALL` and `CascadeType.REMOVE` are prohibited on any association touching financial data.** A cascade delete from an account to its ledger entries destroys the audit record. Deletion of financial records is a deliberate, migration-reviewed operation, never a side effect of an ORM cascade.

### 9.4 Repositories

```java
public interface AccountRepository extends JpaRepository<Account, UUID> {

    Optional<Account> findByAccountNumber(String accountNumber);

    // Ownership is part of the query, not a check performed afterwards
    Optional<Account> findByIdAndCustomerId(UUID id, UUID customerId);

    @Query("SELECT a FROM Account a WHERE a.customerId = :customerId AND a.status = :status")
    List<Account> findAllByCustomerAndStatus(@Param("customerId") UUID customerId,
                                             @Param("status") AccountStatus status);

    // Pessimistic lock for balance mutation — see section 12.4
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT a FROM Account a WHERE a.id = :id")
    Optional<Account> findByIdForUpdate(@Param("id") UUID id);
}
```

- **Ownership belongs in the query.** `findByIdAndCustomerId` cannot be forgotten the way a follow-up `if` can. This is the primary defence against broken object-level authorization; see [ESTD21 §4.4](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#44-ownership-checks-are-mandatory).
- **Derived query names stop at three conditions.** Beyond that, use `@Query` — `findByCustomerIdAndStatusAndCurrencyAndOpenedAtBetweenOrderByOpenedAtDesc` is unreadable and unmaintainable.
- **Named parameters, never positional, never concatenation.** See [ESTD21 §11](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#11-input-security).
- **No business logic in repositories.** A repository returns data; it does not decide what the data means.

### 9.5 Optimistic Locking Is Mandatory on Mutable Financial State

Every entity whose state can change concurrently carries `@Version`. Without it, two concurrent updates produce a lost update — read balance 100, both subtract 30, both write 70, and 30 units have vanished.

```java
@Version
@Column(name = "version", nullable = false)
private long version;
```

On conflict, JPA throws `OptimisticLockingFailureException`, which the global handler maps to 409. The client retries with the same idempotency key, which is safe precisely because the key is enforced.

### 9.6 Open Session In View Is Disabled

```yaml
spring:
  jpa:
    open-in-view: false        # MANDATORY
```

Open Session In View keeps the persistence context open through view rendering, so a lazy association silently loads during serialization — outside the transaction, one query at a time, invisible in the service code. It masks N+1 problems in development and produces them at scale in production. Disable it and load explicitly.

### 9.7 The N+1 Problem

```java
// N+1 — one query for the accounts, then one per account for its customer
List<Account> accounts = accountRepository.findAllByCustomerAndStatus(customerId, ACTIVE);
accounts.forEach(a -> log.info("{}", a.getCustomer().getName()));   // N more queries

// GOOD — one query, explicit join fetch
@Query("SELECT a FROM Account a JOIN FETCH a.customer WHERE a.customerId = :customerId")
List<Account> findAllWithCustomer(@Param("customerId") UUID customerId);

// GOOD — entity graph, when the same entity is loaded with different shapes
@EntityGraph(attributePaths = {"customer", "productType"})
List<Account> findAllByCustomerId(UUID customerId);

// BEST for read-only endpoints — a projection loads only the columns needed
public interface AccountSummary {
    UUID getId();
    String getAccountNumber();
    BigDecimal getAvailableBalance();
}
List<AccountSummary> findAllProjectedByCustomerId(UUID customerId);
```

Detection is not optional. Every service enables SQL statistics in the test profile and asserts query counts on the hot paths:

```yaml
# application-test.yml
spring:
  jpa:
    properties:
      hibernate.generate_statistics: true
logging:
  level:
    org.hibernate.SQL: DEBUG
```

```java
@Test
void listAccounts_loadsCustomerInOneQuery() {
    Statistics stats = entityManagerFactory.unwrap(SessionFactory.class).getStatistics();
    stats.clear();

    accountService.listForCustomer(customerId);

    assertThat(stats.getPrepareStatementCount())
        .as("N+1 regression on account listing")
        .isEqualTo(1);
}
```

### 9.8 Migrations with Flyway

```
src/main/resources/db/migration/
├── V1__create_customer_table.sql
├── V2__create_account_table.sql
├── V3__create_ledger_entry_table.sql
├── V4__add_account_daily_limit_column.sql
└── V5__create_idempotency_record_table.sql
```

Rules:

- **`V{n}__{snake_case_description}.sql`**, sequential, never renumbered.
- **A migration that has run anywhere beyond a developer machine is immutable.** Flyway validates checksums; editing an applied migration breaks every environment that already ran it. Fix forward with a new migration.
- **Every migration is reversible in principle** — the rollback path is written in the PR description even when no `U` script exists.
- **No `DROP COLUMN` or `DROP TABLE` in the same release that stops using it.** Use expand-contract ([§9.9](#99-zero-downtime-schema-change-expand-contract)).
- **Constraints live in the migration, not only in annotations.** The database is the last line of defence for data integrity, and it is the only one that holds when a batch job, a support script, or a future service writes to the same table.

```sql
-- V3__create_ledger_entry_table.sql
CREATE TABLE ledger_entry (
    id                UUID           PRIMARY KEY,
    transfer_id       UUID           NOT NULL,
    account_id        UUID           NOT NULL REFERENCES account (id),
    direction         VARCHAR(6)     NOT NULL,
    amount            NUMERIC(19,4)  NOT NULL,
    currency          CHAR(3)        NOT NULL,
    booked_at         TIMESTAMPTZ    NOT NULL,
    created_at        TIMESTAMPTZ    NOT NULL DEFAULT now(),

    CONSTRAINT ck_ledger_entry_direction  CHECK (direction IN ('DEBIT', 'CREDIT')),
    CONSTRAINT ck_ledger_entry_amount_pos CHECK (amount > 0),
    CONSTRAINT ck_ledger_entry_currency   CHECK (currency ~ '^[A-Z]{3}$')
);

CREATE INDEX ix_ledger_entry_account_booked ON ledger_entry (account_id, booked_at DESC, id DESC);
CREATE INDEX ix_ledger_entry_transfer       ON ledger_entry (transfer_id);

-- The ledger is append-only. Enforced by the database, not by convention.
REVOKE UPDATE, DELETE ON ledger_entry FROM app_write_role;
```

### 9.9 Zero-Downtime Schema Change: Expand-Contract

A running service and a migration cannot change at the same instant. Every non-trivial schema change is three deployments:

```
Release N     EXPAND    Add the new column, nullable, with no code reading it.
                        Add a backfill job. Code writes BOTH old and new.

Release N+1   MIGRATE   Code reads the new column, still writes both.
                        Backfill completes and is verified by row count and checksum.

Release N+2   CONTRACT  Code stops writing the old column.
                        A later migration drops it, once no rollback target still needs it.
```

Renaming a column in one step breaks every instance still running the previous version during a rolling deploy. There is no exception to this for a table holding financial data.

### 9.10 Connection Pool

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20          # See the sizing note below
      minimum-idle: 10
      connection-timeout: 3000       # Fail fast; do not queue requests behind an exhausted pool
      idle-timeout: 600000
      max-lifetime: 1740000          # Below the database's own idle timeout
      leak-detection-threshold: 20000
      pool-name: payments-pool
```

Pool sizing is not "as large as possible". A pool larger than the database can serve moves the queue from the application to the database, where it is harder to see and slower to shed. Start from `(core_count * 2) + effective_spindle_count` and adjust from measured pool-wait metrics. **The sum of all instances' pool sizes must stay below the PostgreSQL `max_connections` limit**, with headroom for migrations, batch jobs, and operator sessions.

`leak-detection-threshold` is mandatory. A connection held for 20 seconds is a bug, and it is a bug that exhausts the pool under load.

---

## 10. Transactions

### 10.1 Transactions Belong to the Service Layer

`@Transactional` goes on service methods. Not on controllers — that holds a connection open across HTTP serialization. Not on repository methods — Spring Data already wraps them, and it puts the boundary below the business operation, so a multi-step operation gets multiple transactions instead of one.

```java
@Service
public class TransferService {

    @Transactional                                   // The whole operation, or none of it
    public TransferResult execute(CustomerId customerId,
                                  TransferCommand command,
                                  IdempotencyKey key) {
        ...
    }
}
```

### 10.2 The Self-Invocation Trap

This is the single most common Spring transaction bug, and in a banking service it produces silent partial writes.

**How `@Transactional` actually works.** Spring does not rewrite your class. At startup it wraps the bean in a *proxy* — a generated object of the same type holding a reference to your instance. Everything that injects `TransferService` receives the proxy, never your object. The proxy opens the transaction, delegates to your method, then commits or rolls back.

```
  Injected caller ──▶ TransferService PROXY ──▶ TransferService (your code)
                            │                            │
                      begin transaction          executeOne(...) body
                      commit / rollback

  Inside the class:  executeBatch() ──▶ this.executeOne()
                                            ▲
                                            └── proxy never runs; no transaction
```

The transaction lives in the proxy, not in your class. So the annotation takes effect only when the call arrives from *outside* the bean, through an injected reference. A call from one method of the class to another resolves to `this` and skips the proxy.

```java
@Service
public class TransferService {

    public void executeBatch(List<TransferCommand> commands) {
        for (TransferCommand command : commands) {
            executeOne(command);        // NO TRANSACTION — the proxy is bypassed
        }
    }

    @Transactional
    public void executeOne(TransferCommand command) {
        ledgerService.debit(command);
        ledgerService.credit(command);  // If this throws, the debit is already committed
    }
}
```

Nothing warns you. The annotation is present, the code compiles, the batch appears to run. The debit commits, the credit fails, and the ledger is out of balance with no error visible anywhere.

Fix it by moving the transactional method onto a different bean, so every call crosses the proxy:

```java
// GOOD — the transactional method lives on a different bean, so the proxy applies
@Service
public class TransferBatchService {
    private final TransferService transferService;   // Injected — calls go through the proxy

    public void executeBatch(List<TransferCommand> commands) {
        commands.forEach(transferService::executeOne);
    }
}
```

Self-injection (a bean injecting its own proxy) and `TransactionTemplate` also work, but both hide the boundary. Split the bean.

The same trap applies to `@Async`, `@Cacheable`, `@Retryable`, and `@PreAuthorize`. All are proxy-based. All are silently inert on a self-invocation.

`@Transactional` on a `private`, `final`, or `static` method is equally inert — the proxy cannot override it. Some of these now fail at startup; do not rely on that.

### 10.3 Propagation

| Propagation | Behaviour | Use For |
|:------------|:----------|:--------|
| `REQUIRED` (default) | Join the caller's transaction, or start one | Almost everything |
| `REQUIRES_NEW` | Suspend the caller's transaction, run in a new one | Audit and outbox writes that must survive a business rollback |
| `MANDATORY` | Fail if there is no active transaction | Ledger-writing methods that must never run standalone |
| `SUPPORTS`, `NOT_SUPPORTED`, `NEVER`, `NESTED` | — | Require written approval |

`REQUIRES_NEW` consumes a second connection from the pool while the first is held. A method using it inside a loop will exhaust the pool. Use it deliberately, never in iteration.

`MANDATORY` is a useful assertion on the ledger:

```java
@Transactional(propagation = Propagation.MANDATORY)
public void postEntries(List<LedgerEntry> entries) {
    // Fails loudly if some caller forgot to open a transaction
}
```

### 10.4 Isolation

PostgreSQL's default is `READ_COMMITTED`, and that is the correct default here. Raise it only for a specific, documented anomaly:

| Level | Prevents | Cost |
|:------|:---------|:-----|
| `READ_COMMITTED` | Dirty reads | Default. Non-repeatable reads and phantoms possible. |
| `REPEATABLE_READ` | + non-repeatable reads | Serialization failures under contention; the caller must handle retry. |
| `SERIALIZABLE` | + phantoms | Highest conflict rate. Requires a documented retry strategy. |

Do not reach for `SERIALIZABLE` to avoid thinking about concurrency. Explicit locking ([§12.4](#124-locking-for-balance-mutation)) plus optimistic versioning is more predictable and far cheaper.

### 10.5 Read-Only Transactions

```java
@Transactional(readOnly = true)
public AccountStatement buildStatement(UUID accountId, YearMonth period) { ... }
```

`readOnly = true` lets Hibernate skip dirty-checking and lets the driver route to a read replica where one is configured. Apply it to every query-only service method.

### 10.6 What Must Never Happen Inside a Transaction

```java
// PROHIBITED — a remote call inside a transaction
@Transactional
public TransferResult execute(TransferCommand command) {
    ledgerService.debit(command);
    SanctionsResult result = sanctionsClient.screen(command);   // Holds a DB connection
                                                                // for the whole network call
    ledgerService.credit(command);
    return ...;
}
```

A slow or hung downstream now holds a database connection. Enough concurrent requests and the pool is exhausted, taking down every endpoint including the ones that do not call that dependency.

The correct shape: do the remote work **before** the transaction opens, or **after** it commits via the outbox ([§13.2](#132-the-transactional-outbox)).

```java
// GOOD
public TransferResult execute(TransferCommand command) {
    SanctionsResult screening = sanctionsClient.screen(command);   // Outside the transaction
    if (screening.isBlocked()) {
        throw new TransferBlockedException(...);
    }
    return transferTransactionalService.commitTransfer(command, screening);   // Short and local
}
```

Also prohibited inside a transaction: file I/O, `Thread.sleep`, unbounded loops, and publishing to a message broker directly.

### 10.7 Timeouts

Every transaction that writes has a timeout. A transaction with no timeout can hold locks indefinitely, and in PostgreSQL a long-held lock blocks the queue behind it.

```java
@Transactional(timeout = 5)          // Seconds
public TransferResult commitTransfer(...) { ... }
```

### 10.8 Rollback Rules

Spring rolls back on `RuntimeException` and `Error`, and **commits** on a checked exception. Since [§8.1](#81-exception-hierarchy) mandates unchecked domain exceptions, the default is correct. Never use `@Transactional(noRollbackFor = ...)` on a money path.

---

## 11. Money and Data Integrity

This section is the reason the rest of the document exists. Everything here is mandatory, and every rule in it has caused a real, reportable incident somewhere.

### 11.1 Floating Point Is Prohibited for Money

```java
// PROHIBITED — in Java, this prints 0.30000000000000004
double balance = 0.1 + 0.2;

// PROHIBITED — float, Double, Float, and any arithmetic that passes through them
float amount = 1250.10f;
```

`double` and `float` are binary floating point. Values like 0.1 have no exact binary representation. Errors accumulate across millions of rows, and a reconciliation run that is off by a fraction of a currency unit is a finding, not a rounding curiosity.

**`BigDecimal` for every monetary value, in every layer: entity, DTO, service, and database.**

### 11.2 BigDecimal Rules

```java
// PROHIBITED — the double constructor carries the binary error straight in
BigDecimal wrong = new BigDecimal(0.1);       // 0.1000000000000000055511151231257827...

// GOOD — string or valueOf
BigDecimal right  = new BigDecimal("0.10");
BigDecimal also   = BigDecimal.valueOf(1250, 2);   // 12.50

// PROHIBITED — equals() compares scale as well as value
new BigDecimal("10.00").equals(new BigDecimal("10.0"));   // false

// GOOD — compareTo ignores scale
amount.compareTo(other) == 0

// PROHIBITED — division without a scale and rounding mode throws on a
// non-terminating result, at runtime, on some inputs only
total.divide(count);

// GOOD — explicit scale and rounding, always
total.divide(count, 4, RoundingMode.HALF_EVEN);
```

**`RoundingMode.HALF_EVEN` (banker's rounding) is the default for monetary calculation**, because `HALF_UP` introduces a systematic upward bias across large volumes. A different mode requires written approval and a comment stating the regulatory or contractual reason.

### 11.3 The Money Type

Passing a bare `BigDecimal` around means the currency is somewhere else, and eventually two amounts in different currencies get added. Make that impossible:

```java
public record Money(BigDecimal amount, Currency currency) implements Comparable<Money> {

    private static final int SCALE = 4;

    public Money {
        Objects.requireNonNull(amount, "amount");
        Objects.requireNonNull(currency, "currency");
        amount = amount.setScale(SCALE, RoundingMode.HALF_EVEN);
    }

    public static Money of(String amount, String currencyCode) {
        return new Money(new BigDecimal(amount), Currency.getInstance(currencyCode));
    }

    public Money plus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money minus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.subtract(other.amount), currency);
    }

    public boolean isPositive() {
        return amount.compareTo(BigDecimal.ZERO) > 0;
    }

    public boolean isGreaterThan(Money other) {
        requireSameCurrency(other);
        return amount.compareTo(other.amount) > 0;
    }

    @Override
    public int compareTo(Money other) {
        requireSameCurrency(other);
        return amount.compareTo(other.amount);
    }

    private void requireSameCurrency(Money other) {
        if (!currency.equals(other.currency)) {
            throw new CurrencyMismatchException(currency, other.currency);
        }
    }
}
```

Currency conversion never happens implicitly. It is an explicit call to a rate service, with the rate, its source, and its timestamp persisted alongside the resulting entry — because a converted amount must be reproducible during an audit.

### 11.4 Database Column Types

```sql
amount   NUMERIC(19,4)  NOT NULL,     -- Never DOUBLE PRECISION, REAL, or FLOAT
currency CHAR(3)        NOT NULL
```

`NUMERIC(19,4)` gives exact decimal arithmetic, 15 integer digits, and 4 decimal places — enough for minor units finer than cents, which several instruments and interest calculations require. The scale is uniform across the schema so that no implicit rescale ever happens in a join or a sum.

### 11.5 The Ledger Is Append-Only and Double-Entry

**A balance is never stored as the truth. The ledger is the truth; a stored balance is a cached projection of it.**

Every movement of money produces at least two entries that sum to zero. No entry is ever updated or deleted. A correction is a new, opposite entry — a reversal — that references the original.

```
Transfer of 1250.00 EUR from account A to account B:

  ledger_entry
  ┌──────────────┬────────────┬───────────┬──────────┬──────────────────────┐
  │ transfer_id  │ account_id │ direction │  amount  │      booked_at       │
  ├──────────────┼────────────┼───────────┼──────────┼──────────────────────┤
  │ 3f2a9c11…    │ A          │ DEBIT     │ 1250.00  │ 2026-09-02T14:31:07Z │
  │ 3f2a9c11…    │ B          │ CREDIT    │ 1250.00  │ 2026-09-02T14:31:07Z │
  └──────────────┴────────────┴───────────┴──────────┴──────────────────────┘
                                            Σ DEBIT − Σ CREDIT = 0

Reversal of that transfer:

  │ 8b1d4e77…    │ A          │ CREDIT    │ 1250.00  │ 2026-09-03T09:02:44Z │
  │ 8b1d4e77…    │ B          │ DEBIT     │ 1250.00  │ 2026-09-03T09:02:44Z │
                              (original rows are untouched)
```

```java
@Service
public class LedgerService {

    /**
     * Posts a balanced set of entries. Must run inside the caller's transaction so that
     * the entries and the balance projection commit or roll back together.
     */
    @Transactional(propagation = Propagation.MANDATORY, timeout = 5)
    public void post(List<LedgerEntry> entries) {
        requireBalanced(entries);
        ledgerEntryRepository.saveAll(entries);
        entries.forEach(this::applyToBalanceProjection);
    }

    private void requireBalanced(List<LedgerEntry> entries) {
        Map<Currency, BigDecimal> netByCurrency = entries.stream()
            .collect(groupingBy(LedgerEntry::currency,
                     reducing(BigDecimal.ZERO, LedgerService::signedAmount, BigDecimal::add)));

        boolean balanced = netByCurrency.values().stream()
            .allMatch(net -> net.compareTo(BigDecimal.ZERO) == 0);

        if (!balanced) {
            // Never post an unbalanced set. This is an invariant, not a validation.
            throw new LedgerWriteException(
                ApiErrorCode.INTERNAL_ERROR, "Ledger entries do not net to zero");
        }
    }

    private static BigDecimal signedAmount(LedgerEntry entry) {
        return entry.direction() == Direction.DEBIT
            ? entry.amount().negate()
            : entry.amount();
    }
}
```

Enforcement is layered, because application code is the weakest of the three:

1. **Application**: `requireBalanced` refuses to post an unbalanced set.
2. **Database privileges**: `REVOKE UPDATE, DELETE ON ledger_entry` — the application role physically cannot mutate a posted entry.
3. **Reconciliation**: a scheduled job re-derives every balance from the ledger and alerts on any divergence ([§15.4](#154-reconciliation-is-mandatory)).

### 11.6 Idempotency Store

```sql
CREATE TABLE idempotency_record (
    idempotency_key    VARCHAR(64)  PRIMARY KEY,
    customer_id        UUID         NOT NULL,
    endpoint           VARCHAR(120) NOT NULL,
    request_fingerprint CHAR(64)    NOT NULL,   -- SHA-256 of the canonical request body
    response_status    INT          NOT NULL,
    response_body      JSONB        NOT NULL,
    created_at         TIMESTAMPTZ  NOT NULL DEFAULT now(),
    expires_at         TIMESTAMPTZ  NOT NULL
);

CREATE INDEX ix_idempotency_expires ON idempotency_record (expires_at);
```

```java
@Transactional(timeout = 5)
public TransferResult execute(CustomerId customerId, TransferCommand command, IdempotencyKey key) {

    String fingerprint = RequestFingerprint.sha256(command);

    Optional<IdempotencyRecord> existing = idempotencyRepository.findById(key.value());
    if (existing.isPresent()) {
        IdempotencyRecord record = existing.get();
        if (!record.getRequestFingerprint().equals(fingerprint)) {
            // Same key, different payload — a client bug or an attack. Never execute.
            throw new DuplicateRequestException(
                ApiErrorCode.DUPLICATE_REQUEST, "Idempotency key reused with a different request");
        }
        return TransferResult.fromStoredResponse(record);      // Replay, do not re-execute
    }

    TransferResult result = performTransfer(customerId, command);

    // Written inside the SAME transaction as the ledger entries.
    // A crash between the two is impossible by construction.
    idempotencyRepository.save(IdempotencyRecord.of(key, customerId, fingerprint, result, ttl));

    return result;
}
```

Two properties make this correct, and both are easy to lose:

- The idempotency record is written **in the same transaction** as the money movement. Writing it before or after in a separate transaction leaves a window where a crash produces a double execution or an unreplayable key.
- A key reused with a **different** payload is rejected, not replayed. Replaying would return the wrong response; executing would break the guarantee.

The concurrent-arrival case is handled by the primary key: the second transaction fails on the unique constraint, and that failure maps to 409.

### 11.7 The Database Is the Last Line of Defence

Every invariant that matters is expressed as a database constraint, in addition to whatever the application checks. Application checks are bypassed by batch jobs, support scripts, data fixes, and the next service to be written against the same schema.

```sql
ALTER TABLE ledger_entry
    ADD CONSTRAINT ck_ledger_entry_amount_positive CHECK (amount > 0),
    ADD CONSTRAINT ck_ledger_entry_direction       CHECK (direction IN ('DEBIT','CREDIT'));

ALTER TABLE account
    ADD CONSTRAINT ck_account_currency_iso   CHECK (currency ~ '^[A-Z]{3}$'),
    ADD CONSTRAINT ck_account_balances_scale CHECK (
        scale(ledger_balance) <= 4 AND scale(available_balance) <= 4);

-- A payee can be registered once per customer
ALTER TABLE payee
    ADD CONSTRAINT uq_payee_customer_iban UNIQUE (customer_id, iban);
```

Note the sign convention: entry amounts are always positive, and direction carries the sign. A signed amount column invites a `-` that should have been a `+`.

### 11.8 Temporal Correctness

- **`Instant` and `TIMESTAMPTZ` everywhere.** No `LocalDateTime`, no `TIMESTAMP WITHOUT TIME ZONE`.
- **Business date is separate from system timestamp.** A transfer booked at `2026-09-02T23:58:00Z` may belong to the next business day depending on the cut-off. Store `booked_at` (instant) and `value_date` (business date) as distinct columns; deriving one from the other at read time produces different answers in different time zones.
- **`Clock` is injected, never `Instant.now()` called directly** in code with time-dependent behaviour. Untestable time is untested time.

```java
@Service
public class InterestService {
    private final Clock clock;

    public InterestService(Clock clock) { this.clock = clock; }

    public void accrue(Account account) {
        Instant now = Instant.now(clock);   // Fixed Clock in tests
        ...
    }
}
```

```java
@Bean
public Clock clock() {
    return Clock.systemUTC();
}
```

---
## 12. Concurrency, Async and Scheduling

Four separate concerns, often confused with each other:

```
  12.1  How a request gets a thread                 (virtual threads)
  12.2  How work runs off the request thread        (@Async)
  12.3  How work runs on a timer, across instances  (@Scheduled + lock)
  12.4  How two threads touching one account stay correct (locking)
  12.5  How in-flight work survives a pod restart   (graceful shutdown)
```

### 12.1 Virtual Threads

A **platform thread** is an operating-system thread: roughly 1 MB of stack, and a few thousand is the practical ceiling. When a request blocks on a JDBC call, that thread sits idle but still occupies its slot. A **virtual thread** is scheduled by the JVM instead: when it blocks, the JVM parks it and hands the underlying platform thread (its *carrier*) to another virtual thread.

```
  Platform threads                        Virtual threads (Java 21)

  200 threads = 200 requests in flight    100,000 virtual threads on ~8 carriers
  request blocks on JDBC                  request blocks on JDBC
    └─ thread idle, slot wasted             └─ virtual thread parked,
                                               carrier runs another request
```

Java 21 virtual threads are enabled for request handling:

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

This makes blocking I/O cheap: a request blocked on a database call no longer pins a platform thread. It does **not** make the database connection pool larger. The pool remains the real concurrency limit, and with virtual threads it is reached faster, so `connection-timeout` and pool-wait metrics matter more, not less.

```
  10,000 virtual threads ──▶ HikariCP (20 connections) ──▶ PostgreSQL
                                      ▲
                         the real ceiling — unchanged by virtual threads
```

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      connection-timeout: 3000     # Fail fast when the pool is the bottleneck,
                                   # rather than queueing 10,000 waiters silently
```

**`synchronized` blocks pin a virtual thread to its carrier thread.** A pinned carrier cannot run any other virtual thread until the block exits, so a handful of pinned carriers collapses throughput for everyone. Replace `synchronized` with `ReentrantLock` in any code path that runs on a virtual thread and can block while holding the lock.

```java
// BAD on a virtual thread — pins the carrier for the duration of the I/O
private final Object lock = new Object();
synchronized (lock) { repository.save(entry); }

// GOOD — ReentrantLock releases the carrier while the virtual thread waits
private final ReentrantLock lock = new ReentrantLock();
lock.lock();
try { repository.save(entry); } finally { lock.unlock(); }
```

**`ThreadLocal` is not free on virtual threads.** With a thread per request rather than a pooled thread, a `ThreadLocal` holding a large object multiplies: what cost 200 copies on a platform-thread pool now costs one copy per in-flight request. Mapped Diagnostic Context (MDC) is fine; caches and buffers are not.

```java
// BAD — 2 MB per in-flight request; 10,000 concurrent requests is 20 GB
private static final ThreadLocal<byte[]> SCRATCH =
    ThreadLocal.withInitial(() -> new byte[2 * 1024 * 1024]);

// BAD — a per-thread cache on a per-request thread is never reused;
//       it is rebuilt and discarded on every single request
private static final ThreadLocal<Map<String, ExchangeRate>> RATE_CACHE =
    ThreadLocal.withInitial(HashMap::new);

// GOOD — one shared, bounded cache for the whole application
private final Cache<String, ExchangeRate> rateCache =
    Caffeine.newBuilder().maximumSize(1_000).expireAfterWrite(Duration.ofMinutes(5)).build();

// GOOD — MDC holds a few short strings per request; that is what ThreadLocal is for
MDC.put("correlationId", correlationId);
```

### 12.2 Async Execution

`@Async` makes the caller return immediately while the annotated method runs on a separate thread taken from an executor. Like `@Transactional`, it is proxy-based, so the self-invocation trap in [§10.2](#102-the-self-invocation-trap) applies here too: a call from inside the same bean runs synchronously with no warning.

```
  Caller ──▶ notificationService.send(...)  ──▶ returns immediately
                        │
                        └──▶ queued on notificationExecutor ──▶ runs later,
                                                                 on another thread
```

`@Async` requires an explicitly configured executor. The Spring default (`SimpleAsyncTaskExecutor`) creates an unbounded number of threads, which under load becomes an out-of-memory failure.

```java
@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean("notificationExecutor")
    public Executor notificationExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(16);
        executor.setQueueCapacity(500);                  // Bounded — never Integer.MAX_VALUE
        executor.setThreadNamePrefix("notification-");   // Named, for thread dumps
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(30);
        executor.initialize();
        return executor;
    }
}
```

```java
@Async("notificationExecutor")                          // Always name the executor
public void sendTransferNotification(NotificationCommand command) { ... }
```

Rules:

**Never `@Async` on a money-moving operation.** Asynchronous work has no transaction, no caller to report failure to, and no guarantee of execution. Money movement is synchronous and transactional; the *notification about* it is asynchronous.

```java
// BAD — the caller gets a success response for a transfer that may never happen,
//       and if the executor queue is full it is dropped with nobody to tell
@Async("notificationExecutor")
public void transfer(TransferCommand command) {
    ledgerService.post(command);
}

// GOOD — the money moves inside the transaction; only the notification is deferred
@Transactional
public TransferResult transfer(TransferCommand command) {
    TransferResult result = ledgerService.post(command);
    eventPublisher.publishEvent(new TransferCompleted(result.transferId()));
    return result;
}

@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)  // See §13.5
@Async("notificationExecutor")
public void onTransferCompleted(TransferCompleted event) {
    notificationGateway.send(event);
}
```

**`@Async` and `@Transactional` do not compose.** The async method runs on a different thread; the caller's transaction is not propagated. An `@Async @Transactional` method starts its own transaction, which commits or rolls back independently of the caller — usually not what the author intended.

```java
// BAD — the audit row commits on its own thread even when the transfer rolls back,
//       and it may read the account before the caller's transaction has committed
@Async("auditExecutor")
@Transactional
public void recordTransferAudit(UUID transferId) { ... }

// GOOD — same thread, same transaction, atomic with the business write
@Transactional(propagation = Propagation.REQUIRES_NEW)   // See §10.3
public void recordTransferAudit(UUID transferId) { ... }
```

**An `@Async void` method's exceptions vanish.** With no caller waiting, nothing observes the throw. Configure an `AsyncUncaughtExceptionHandler`, or return `CompletableFuture` and handle the failure.

```java
// BAD — the gateway times out, the exception is swallowed, no log, no metric
@Async("notificationExecutor")
public void sendTransferNotification(NotificationCommand command) {
    notificationGateway.send(command);       // throws — and nobody ever knows
}

// GOOD (option 1) — the caller can observe the failure
@Async("notificationExecutor")
public CompletableFuture<Void> sendTransferNotification(NotificationCommand command) {
    return CompletableFuture.runAsync(() -> notificationGateway.send(command));
}

// GOOD (option 2) — a global handler for every @Async void method
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) ->
            log.error("async_failed method={} args={}", method.getName(), params, ex);
    }
}
```

**Queue capacity is always bounded**, and the rejection policy is explicit. `CallerRunsPolicy` applies natural backpressure; a silent `DiscardPolicy` on anything that matters is prohibited.

```java
// BAD — the default queue is effectively unbounded; a slow downstream turns
//       a backlog into heap exhaustion, and the pod dies holding the work
executor.setQueueCapacity(Integer.MAX_VALUE);

// BAD — rejected notifications disappear with no log and no metric
executor.setRejectedExecutionHandler(new ThreadPoolExecutor.DiscardPolicy());

// GOOD — bounded, and overflow slows the caller instead of dropping work
executor.setQueueCapacity(500);
executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
```

**MDC does not propagate across threads.** Use a `TaskDecorator` to copy the correlation id, or the async work is untraceable.

```
// Without a decorator:
  request thread     log.info("transfer_completed")   correlationId=abc123
  notification-3     log.error("notification_failed") correlationId=            <- untraceable
```

```java
// GOOD — copy the MDC into the task, and clear it when the task ends
executor.setTaskDecorator(runnable -> {
    Map<String, String> context = MDC.getCopyOfContextMap();
    return () -> {
        if (context != null) MDC.setContextMap(context);
        try { runnable.run(); } finally { MDC.clear(); }
    };
});
```

### 12.3 Scheduling

`@Scheduled` runs a method on a timer **in every instance of the service**. Four pods means four executions of the same job at the same second, unless a shared lock stops them.

```
  23:00 UTC
    pod-1 ──▶ accrueDailyInterest()  ─┐
    pod-2 ──▶ accrueDailyInterest()  ─┤  no lock  ──▶ interest posted 4 times
    pod-3 ──▶ accrueDailyInterest()  ─┤
    pod-4 ──▶ accrueDailyInterest()  ─┘

    pod-1 ──▶ acquires shedlock row ──▶ runs
    pod-2 ──▶ lock held ──▶ skips        with lock ──▶ posted once
    pod-3 ──▶ lock held ──▶ skips
    pod-4 ──▶ lock held ──▶ skips
```

```java
@Configuration
@EnableScheduling
@EnableSchedulerLock(defaultLockAtMostFor = "PT30M")
public class SchedulingConfig {

    @Bean
    public LockProvider lockProvider(DataSource dataSource) {
        return new JdbcTemplateLockProvider(
            JdbcTemplateLockProvider.Configuration.builder()
                .withJdbcTemplate(new JdbcTemplate(dataSource))
                .usingDbTime()                    // Database clock, not instance clock
                .build());
    }
}
```

```java
@Scheduled(cron = "0 0 23 * * *", zone = "UTC")     // Zone is always explicit
@SchedulerLock(name = "dailyInterestAccrual",
               lockAtLeastFor = "PT5M", lockAtMostFor = "PT55M")
public void accrueDailyInterest() { ... }
```

**Distributed locking is mandatory on every scheduled job.** A service runs on multiple instances. Without a lock, an interest accrual job runs once per instance, and interest is posted four times. ShedLock (or an equivalent database-backed lock) is not optional.

- `lockAtLeastFor` prevents a fast job from running twice due to clock skew between instances.
- `lockAtMostFor` releases the lock if an instance dies mid-job. Set it above the worst observed runtime, or the job will double-run during a slow night.
- `usingDbTime()` makes the lock depend on the database clock, not on each instance's clock.

**A scheduled job must be idempotent regardless of the lock.** Locks reduce the probability of a double run; they do not eliminate it. The job itself must be safe to re-run.

```java
// BAD — a second run for the same day posts the interest again
public void accrueDailyInterest() {
    for (Account account : accountRepository.findAllActive()) {
        ledgerService.postInterest(account, interestFor(account));
    }
}

// GOOD — the accrual date is part of a unique key, so a re-run is a no-op
//        CREATE UNIQUE INDEX ON interest_accrual (account_id, accrual_date);
public void accrueDailyInterest() {
    LocalDate accrualDate = LocalDate.now(clock);
    for (Account account : accountRepository.findAllActive()) {
        if (accrualRepository.existsByAccountIdAndAccrualDate(account.id(), accrualDate)) {
            continue;                       // Already accrued for this date
        }
        ledgerService.postInterest(account, interestFor(account), accrualDate);
    }
}
```

**Fixed rate is prohibited for jobs that can overlap.** `fixedRate` starts the next run on schedule even if the previous is still going. Use `fixedDelay` or cron.

```java
// BAD — the settlement sweep takes 90s; a new one starts every 60s and they pile up
@Scheduled(fixedRate = 60_000)
public void sweepPendingSettlements() { ... }

// GOOD — the next run starts 60s after the previous one finishes
@Scheduled(fixedDelay = 60_000)
public void sweepPendingSettlements() { ... }
```

### 12.4 Locking for Balance Mutation

Two concurrent transfers from the same account must not both pass the balance check. Optimistic locking ([§9.5](#95-optimistic-locking-is-mandatory-on-mutable-financial-state)) detects the conflict after the fact and forces a retry. For a hot account, pessimistic locking is cheaper than a retry storm:

```
  Balance 100. Two concurrent debits of 80, no lock:

    tx-A  read balance=100 ──▶ check 80 ≤ 100 OK ──▶ write 20
    tx-B  read balance=100 ──▶ check 80 ≤ 100 OK ──▶ write 20
                                                     └─ account overdrawn by 60

  With SELECT ... FOR UPDATE:

    tx-A  lock row ──▶ read 100 ──▶ write 20 ──▶ commit, lock released
    tx-B  ......... waits ........ ──▶ read 20 ──▶ 80 > 20 ──▶ InsufficientFunds
```

```java
@Transactional(timeout = 5)
public void debit(UUID accountId, Money amount) {

    // SELECT ... FOR UPDATE — serializes concurrent debits on this row
    Account account = accountRepository.findByIdForUpdate(accountId)
        .orElseThrow(() -> new AccountNotFoundException(...));

    if (account.availableBalance().compareTo(amount.amount()) < 0) {
        throw new InsufficientFundsException(...);
    }
    account.debit(amount);
}
```

**Lock ordering is fixed and global.** A transfer locks two accounts; if two concurrent transfers lock them in opposite orders, they deadlock:

```
  Transfer 1: A ──▶ B          Transfer 2: B ──▶ A

    tx-1 locks A ──▶ waits for B
    tx-2 locks B ──▶ waits for A
                     └─ neither can proceed; the database kills one after its
                        deadlock_timeout, and that transfer fails
```

Always acquire locks in ascending account-id order, so both transactions queue on the same row first and no cycle can form:

```java
// BAD — lock order follows the direction of the transfer, so it varies per request
accountRepository.findByIdForUpdate(debitAccountId);
accountRepository.findByIdForUpdate(creditAccountId);

// GOOD — a global, deterministic order; every transaction agrees on who waits
List<UUID> ordered = Stream.of(debitAccountId, creditAccountId).sorted().toList();
ordered.forEach(accountRepository::findByIdForUpdate);
```

Hold the lock for the shortest possible time, and never across a network call ([§10.6](#106-what-must-never-happen-inside-a-transaction)).

### 12.5 Shutdown

A pod is killed constantly: deploys, scaling, node drains. Without graceful shutdown the JVM dies mid-request, and a transfer that has debited but not yet credited leaves the ledger unbalanced.

```
  SIGTERM
    │
    ├─ stop accepting new requests        (load balancer drains)
    ├─ let in-flight requests finish      (up to timeout-per-shutdown-phase)
    ├─ let executor queues drain          (setWaitForTasksToCompleteOnShutdown)
    └─ close the connection pool, exit
```

```yaml
server:
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

A pod that terminates mid-transfer must not leave a debit without a credit. Graceful shutdown stops accepting new requests, drains in-flight ones, and only then closes the pool. Executors declare `setWaitForTasksToCompleteOnShutdown(true)` so queued work is not silently dropped.

```java
// BAD — queued notifications are discarded the moment SIGTERM arrives
executor.setWaitForTasksToCompleteOnShutdown(false);

// GOOD — drain what is queued, bounded by a timeout below the pod's grace period
executor.setWaitForTasksToCompleteOnShutdown(true);
executor.setAwaitTerminationSeconds(30);
```

The Kubernetes `terminationGracePeriodSeconds` must exceed `timeout-per-shutdown-phase` plus the executor's `awaitTerminationSeconds`, or the pod is `SIGKILL`ed while still draining and the guarantee is void.

---

## 13. Messaging

### 13.1 The Dual-Write Problem

```java
// PROHIBITED — two systems, no shared transaction
@Transactional
public void execute(TransferCommand command) {
    ledgerService.post(entries);                       // Commits to PostgreSQL
    kafkaTemplate.send("transfer.completed", event);   // Sends to Kafka
}
```

There is no transaction spanning the database and the broker. Either failure mode is real and both are bad: the ledger commits and the event is lost (downstream never learns), or the event is sent and the transaction rolls back (downstream acts on a transfer that never happened).

**Publishing to a broker directly from a transactional method is prohibited.**

### 13.2 The Transactional Outbox

Write the event to the database, in the same transaction as the business data. A separate relay publishes it afterwards.

```
┌────────────────────────────────────────────┐
│  Transaction (PostgreSQL)                  │
│                                            │
│   INSERT ledger_entry  (debit)             │
│   INSERT ledger_entry  (credit)            │
│   UPDATE account       (projection)        │
│   INSERT outbox_event  (transfer.completed)│
│                                            │
│  COMMIT — all four, or none                │
└────────────────┬───────────────────────────┘
                 │
                 ▼
      ┌─────────────────────┐
      │  Outbox relay       │  polls or reads the WAL,
      │  (scheduled, locked)│  publishes, marks published
      └──────────┬──────────┘
                 ▼
              Broker  ──▶  consumers (at-least-once)
```

```sql
CREATE TABLE outbox_event (
    id             UUID         PRIMARY KEY,
    aggregate_type VARCHAR(64)  NOT NULL,
    aggregate_id   UUID         NOT NULL,
    event_type     VARCHAR(120) NOT NULL,
    payload        JSONB        NOT NULL,
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    published_at   TIMESTAMPTZ,
    attempts       INT          NOT NULL DEFAULT 0
);

CREATE INDEX ix_outbox_unpublished ON outbox_event (created_at) WHERE published_at IS NULL;
```

```java
@Scheduled(fixedDelay = 1000)
@SchedulerLock(name = "outboxRelay", lockAtMostFor = "PT2M")
public void publishPending() {
    List<OutboxEvent> batch = outboxRepository.findUnpublished(Limit.of(100));

    for (OutboxEvent event : batch) {
        try {
            broker.publish(event.eventType(), event.aggregateId().toString(), event.payload());
            outboxRepository.markPublished(event.id(), Instant.now(clock));
        } catch (BrokerException e) {
            outboxRepository.incrementAttempts(event.id());
            log.warn("Outbox publish failed. eventId={}, attempts={}",
                     event.id(), event.attempts() + 1);
            break;                       // Preserve ordering; retry on the next tick
        }
    }
}
```

The outbox gives **at-least-once** delivery. It never gives exactly-once. That is the consumer's problem, and [§13.3](#133-idempotent-consumers) is how the consumer solves it.

**The payload is a contract**, not a serialized entity. Never publish a JPA entity — the event shape would change every time a column changed.

### 13.3 Idempotent Consumers

Every consumer assumes it will see the same message more than once, because it will: broker retries, rebalances, and relay restarts all redeliver.

```java
@KafkaListener(topics = "transfer.completed", groupId = "notification-service")
@Transactional(timeout = 10)
public void onTransferCompleted(ConsumerRecord<String, String> record, Acknowledgment ack) {

    String messageId = header(record, "messageId");

    // Insert-first dedupe: the primary key does the work, not a read-then-write race
    try {
        processedMessageRepository.save(new ProcessedMessage(messageId, Instant.now(clock)));
    } catch (DataIntegrityViolationException duplicate) {
        log.debug("Duplicate message ignored. messageId={}", messageId);
        ack.acknowledge();
        return;
    }

    TransferCompletedEvent event = deserialize(record.value());
    notificationService.notifyTransferCompleted(event);

    ack.acknowledge();               // Manual ack, after the work has committed
}
```

```yaml
spring:
  kafka:
    consumer:
      enable-auto-commit: false        # MANDATORY
      auto-offset-reset: earliest
      isolation-level: read_committed
    listener:
      ack-mode: manual_immediate
```

**Auto-commit is prohibited.** It commits the offset on a timer, independent of whether the work succeeded, so a crash mid-processing loses the message permanently.

### 13.4 Retry, Backoff and Dead Letters

```java
@Bean
public DefaultErrorHandler errorHandler(KafkaTemplate<String, String> template) {
    // After the retries are exhausted, route to <topic>.DLT rather than blocking the partition
    DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(template);

    ExponentialBackOff backOff = new ExponentialBackOff(1000L, 2.0);
    backOff.setMaxElapsedTime(60_000L);

    DefaultErrorHandler handler = new DefaultErrorHandler(recoverer, backOff);

    // Never retry a message that can never succeed
    handler.addNotRetryableExceptions(
        DeserializationException.class,
        ValidationException.class,
        IllegalArgumentException.class);

    return handler;
}
```

- **A poison message must never block a partition.** Without a dead-letter route, one malformed message halts every message behind it, indefinitely.
- **Every DLT is monitored and alerted on.** A dead-letter topic nobody watches is a silent data-loss channel.
- **Reprocessing from a DLT is a deliberate, logged operation**, never an automatic drain.

### 13.5 Application Events Inside a Service

For in-process decoupling, `ApplicationEventPublisher` with `@TransactionalEventListener` runs a listener only after the transaction commits:

```java
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void onTransferCommitted(TransferCommittedEvent event) {
    // Runs only if the transaction actually committed
}
```

`AFTER_COMMIT` is the only phase permitted for anything with a side effect. A listener on `BEFORE_COMMIT` that fails will roll the transaction back from a place nobody expects.

Note that this listener runs **outside** the transaction, so a write inside it needs `REQUIRES_NEW`, and a failure inside it cannot undo the committed business change. For anything that must not be lost, use the outbox, not an event listener.

### 13.6 Ordering

Kafka orders within a partition, not within a topic. Events that must be applied in order — all events for one account — must share a partition key.

```java
broker.publish(event.eventType(),
               event.aggregateId().toString(),   // Partition key = aggregate id
               event.payload());
```

---

## 14. Caching

### 14.1 What Must Never Be Cached

| Never Cache | Why |
|:------------|:----|
| Account balances | Stale by definition; a cached balance authorizing a transfer is an overdraft |
| Transaction and ledger history | Same reason, plus it is regulated data at rest in a second store |
| Authentication tokens, sessions | A cache is a credential store nobody hardened |
| Any PII or PCI data | Duplicates a regulated dataset into a system with different controls; see [ESTD21 §6](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#6-data-classification) |
| Authorization decisions | A revoked permission stays effective until the TTL expires |
| Anything used to make a money-movement decision | Correctness beats latency, always |

Caching is for data that is expensive to compute, changes rarely, and is not sensitive: reference data, product catalogues, currency lists, fee schedules, bank identifier lookups, feature flags.

### 14.2 Cache Configuration

```java
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory factory) {
        RedisCacheConfiguration defaults = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))          // Every cache has a TTL
            .disableCachingNullValues()
            .serializeValuesWith(SerializationPair.fromSerializer(
                new GenericJackson2JsonRedisSerializer()));   // JSON, never Java serialization

        return RedisCacheManager.builder(factory)
            .cacheDefaults(defaults)
            .withCacheConfiguration("feeSchedules",
                defaults.entryTtl(Duration.ofHours(6)))
            .withCacheConfiguration("branchDirectory",
                defaults.entryTtl(Duration.ofHours(24)))
            .build();
    }
}
```

- **Every cache has an explicit TTL.** A cache without expiry is a permanent stale copy.
- **JSON serialization, never Java native serialization.** Deserializing untrusted bytes is a remote code execution class; see [ESTD21 §11.6](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#116-java-deserialization-is-prohibited).
- **`disableCachingNullValues`** so a miss does not get memoized as a negative result unless that is deliberate.

### 14.3 Usage

```java
@Cacheable(cacheNames = "feeSchedules", key = "#productCode + ':' + #currency")
public FeeSchedule findFeeSchedule(String productCode, String currency) { ... }

@CacheEvict(cacheNames = "feeSchedules", key = "#schedule.productCode + ':' + #schedule.currency")
@Transactional
public void updateFeeSchedule(FeeSchedule schedule) { ... }
```

- **Keys are explicit.** The default key generator uses all parameters, so adding a parameter silently changes every key and empties the cache.
- **Eviction is paired with every write.** A cache updated only by TTL will serve a stale fee schedule for the length of that TTL after a rate change.
- `@Cacheable` is proxy-based, so [§10.2](#102-the-self-invocation-trap) applies: a self-invocation is not cached.

### 14.4 Stampede Prevention

When a hot key expires, every concurrent request misses simultaneously and hits the database at once. For genuinely hot keys, use a short lock or a two-tier cache with a local Caffeine layer in front of Redis, and stagger TTLs with a small random jitter so a batch of entries loaded together does not expire together.

### 14.5 Cache Failure Is Not Request Failure

A Redis outage must degrade latency, not availability:

```java
@Bean
public CacheErrorHandler cacheErrorHandler() {
    return new SimpleCacheErrorHandler() {
        @Override
        public void handleCacheGetError(RuntimeException e, Cache cache, Object key) {
            log.warn("Cache read failed, falling through to source. cache={}", cache.getName());
            // Swallow — the method executes and returns the real value
        }
    };
}
```

---

## 15. Batch and End-of-Day Jobs

### 15.1 When to Use Spring Batch

Use Spring Batch when the work is large, must be restartable, and must leave an auditable record: interest accrual, statement generation, regulatory extracts, settlement files, reconciliation. A `@Scheduled` method looping over a `List` is not a batch job — it has no restart point, no chunk boundary, and no record of what it processed.

### 15.2 Job Structure

```java
@Configuration
public class InterestAccrualJobConfig {

    @Bean
    public Job interestAccrualJob(JobRepository jobRepository, Step accrueStep) {
        return new JobBuilder("interestAccrualJob", jobRepository)
            .incrementer(new RunIdIncrementer())
            .start(accrueStep)
            .build();
    }

    @Bean
    public Step accrueStep(JobRepository jobRepository,
                           PlatformTransactionManager transactionManager,
                           ItemReader<Account> reader,
                           ItemProcessor<Account, LedgerEntry> processor,
                           ItemWriter<LedgerEntry> writer) {
        return new StepBuilder("accrueStep", jobRepository)
            .<Account, LedgerEntry>chunk(500, transactionManager)   // Commit interval
            .reader(reader)
            .processor(processor)
            .writer(writer)
            .faultTolerant()
            .retryLimit(3)
            .retry(TransientDataAccessException.class)
            .skipLimit(0)                       // Financial jobs skip NOTHING
            .listener(new AccrualStepListener())
            .build();
    }
}
```

**`skipLimit(0)` on any job touching money.** Skipping a record means the job reports success while an account silently missed its interest. A financial batch either processes every record or fails loudly and is fixed and restarted.

### 15.3 Restartability

- **The reader must be restartable.** `JdbcPagingItemReader` with a deterministic sort is restartable; `JdbcCursorItemReader` over an unstable ordering is not.
- **Chunk size is the commit interval.** A failure at record 4,700 with a chunk size of 500 means records 1–4,500 are committed and the restart resumes at 4,501. Choose it deliberately: too large means more rework on failure and longer locks, too small means transaction overhead per record.
- **`JobParameters` must be unique per logical run**, and must include the business date. `RunIdIncrementer` alone lets the same business date run twice.

```java
JobParameters parameters = new JobParametersBuilder()
    .addString("businessDate", businessDate.toString())     // Identifying
    .addLong("runId", runIdSequence.next())
    .toJobParameters();
```

- **The processor must be idempotent.** A restart reprocesses the chunk that failed. Posting interest must check whether an entry already exists for that account and business date — or the restart double-posts.

### 15.4 Reconciliation Is Mandatory

Every end-of-day cycle includes a reconciliation step that re-derives balances from the ledger and compares them to the stored projections:

```java
@Transactional(readOnly = true, timeout = 1800)
public ReconciliationReport reconcile(LocalDate businessDate) {

    List<BalanceDivergence> divergences = accountRepository.findBalanceDivergences(businessDate);

    if (!divergences.isEmpty()) {
        // Never auto-correct. A divergence is an incident with a cause that must be found.
        log.error("Balance reconciliation failed. divergentAccounts={}", divergences.size());
        alertService.raiseCritical("BALANCE_RECONCILIATION_FAILED", divergences.size());
    }
    return new ReconciliationReport(businessDate, divergences);
}
```

```sql
-- The stored projection must equal the sum of the ledger. Always.
SELECT a.id,
       a.ledger_balance                                      AS projected,
       COALESCE(SUM(CASE WHEN l.direction = 'CREDIT' THEN l.amount
                         ELSE -l.amount END), 0)             AS derived
FROM   account a
LEFT   JOIN ledger_entry l ON l.account_id = a.id AND l.booked_at < :cutoff
GROUP  BY a.id, a.ledger_balance
HAVING a.ledger_balance <> COALESCE(SUM(CASE WHEN l.direction = 'CREDIT' THEN l.amount
                                             ELSE -l.amount END), 0);
```

**Never auto-correct a divergence.** Silently writing the derived value over the projection destroys the evidence needed to find out why they differed.

### 15.5 Batch Operational Rules

- Batch jobs run under their **own database role** with its own connection pool, so a long-running batch cannot exhaust the pool serving customer traffic.
- Every job emits start, end, record count, duration, and outcome as metrics, and a job that does not complete within its expected window alerts.
- A job that failed is never "just re-run" — the restart is a recorded operational action with the failure cause noted.
- **No batch job writes outside its declared tables.** A job that repairs data across the schema is a migration, and it goes through migration review.

---

## 16. Resilience

### 16.1 Every Outbound Call Has a Timeout

A call without a timeout waits forever, and it holds a thread and often a connection while it does. This is the most common single cause of a cascading outage.

```java
@Bean
public RestClient sanctionsRestClient(RestClient.Builder builder,
                                      SanctionsProperties properties) {
    ClientHttpRequestFactorySettings settings = ClientHttpRequestFactorySettings.DEFAULTS
        .withConnectTimeout(Duration.ofSeconds(2))
        .withReadTimeout(Duration.ofSeconds(5));

    return builder
        .baseUrl(properties.baseUrl())
        .requestFactory(ClientHttpRequestFactories.get(settings))
        .build();
}
```

`RestTemplate` is deprecated for new code. Use `RestClient` (synchronous) or `WebClient` (reactive). Both must have explicit connect and read timeouts; neither has a useful default.

### 16.2 Circuit Breakers

```yaml
resilience4j:
  circuitbreaker:
    instances:
      sanctionsScreening:
        sliding-window-type: COUNT_BASED
        sliding-window-size: 50
        failure-rate-threshold: 50
        wait-duration-in-open-state: 30s
        permitted-number-of-calls-in-half-open-state: 5
        automatic-transition-from-open-to-half-open-enabled: true
  timelimiter:
    instances:
      sanctionsScreening:
        timeout-duration: 5s
  retry:
    instances:
      sanctionsScreening:
        max-attempts: 3
        wait-duration: 500ms
        exponential-backoff-multiplier: 2
        retry-exceptions:
          - java.io.IOException
          - org.springframework.web.client.ResourceAccessException
```

```java
@CircuitBreaker(name = "sanctionsScreening", fallbackMethod = "screeningUnavailable")
@Retry(name = "sanctionsScreening")
public SanctionsResult screen(TransferCommand command) {
    return sanctionsRestClient.post()... ;
}

private SanctionsResult screeningUnavailable(TransferCommand command, Exception e) {
    // FAIL CLOSED — a transfer that cannot be screened does not proceed
    log.error("Sanctions screening unavailable; rejecting transfer", e);
    throw new DownstreamUnavailableException(
        ApiErrorCode.DOWNSTREAM_UNAVAILABLE, "Screening unavailable");
}
```

**Fallbacks in a banking service fail closed, not open.** A fallback that lets an unscreened transfer through because the screening service is down is a compliance breach implemented as a resilience feature. The correct fallback rejects the request.

Degradation that fails *open* is acceptable only where the unavailable data is non-authoritative: a missing marketing banner, an unavailable spending-category breakdown, a stale exchange-rate display marked as stale.

### 16.3 Retry Rules

| Rule | Reason |
|:-----|:-------|
| **Never retry a non-idempotent operation** without an idempotency key | A retried transfer without a key is a second transfer |
| Retry only transient failures: timeouts, connection resets, 503, 429 | Retrying a 400 or a 422 will fail identically every time |
| Exponential backoff with jitter, always | Fixed-interval retries from many instances synchronize into a thundering herd |
| Bounded attempts, always | Unbounded retry turns a brief outage into a sustained self-inflicted load spike |
| Never retry inside a transaction | The transaction stays open for the whole retry sequence, holding locks |

### 16.4 Bulkheads

A slow dependency must not consume all the capacity available to unrelated endpoints:

```yaml
resilience4j:
  bulkhead:
    instances:
      sanctionsScreening:
        max-concurrent-calls: 20
        max-wait-duration: 100ms
```

### 16.5 Health Checks

```java
@Component
public class LedgerHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {
        try {
            Duration lag = outboxRepository.oldestUnpublishedAge();
            if (lag.compareTo(Duration.ofMinutes(5)) > 0) {
                return Health.down()
                    .withDetail("reason", "outbox_backlog")     // No internal detail beyond this
                    .build();
            }
            return Health.up().build();
        } catch (DataAccessException e) {
            return Health.down().withDetail("reason", "ledger_unreachable").build();
        }
    }
}
```

- **Liveness and readiness are distinct.** Liveness answers "should this instance be restarted"; readiness answers "should it receive traffic". A dependency outage makes an instance *not ready*; it does not make it dead, and restarting it will not help.
- **Health responses expose no internal detail.** `show-details: never` on the public endpoint. Detail is available on the management port, which is not publicly routable; see [ESTD21 §5.5](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#55-actuator-exposure).
- Health checks must return in under one second and must not run expensive queries.

---

## 17. Observability

### 17.1 Correlation Identifiers

Every request gets a correlation id at the boundary, propagated through logs, downstream calls, and messages. Without it, a customer complaint cannot be traced across services.

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class CorrelationIdFilter extends OncePerRequestFilter {

    public static final String HEADER = "X-Correlation-Id";
    private static final Pattern SAFE = Pattern.compile("^[A-Za-z0-9-]{8,64}$");

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        String incoming = request.getHeader(HEADER);
        // The header is client input. Validate it, or it becomes a log-injection vector.
        String correlationId = (incoming != null && SAFE.matcher(incoming).matches())
            ? incoming
            : UUID.randomUUID().toString();

        MDC.put("correlationId", correlationId);
        response.setHeader(HEADER, correlationId);
        try {
            chain.doFilter(request, response);
        } finally {
            MDC.clear();            // MANDATORY — threads are reused; leaked MDC misattributes logs
        }
    }
}
```

### 17.2 Structured Logging

Logs are JSON in every deployed environment. A grep-oriented text format cannot be queried, and a banking service's logs are queried under time pressure.

```java
// GOOD — parameterized, structured, no concatenation
log.info("Transfer completed. transferId={}, rail={}, durationMs={}",
         transferId, rail, durationMs);

// PROHIBITED — string concatenation builds the string even when the level is disabled
log.debug("Transfer state: " + transfer.toString());
```

### 17.3 What Must Never Be Logged

This list is absolute. See [ESTD21 §8](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#8-data-in-transit-and-in-use) for the full treatment.

- Full account numbers, IBANs, card numbers (PAN), CVV, PIN
- Passwords, tokens, API keys, session identifiers, authorization headers
- Customer names, addresses, dates of birth, national identifiers, email addresses, phone numbers
- Full request or response bodies on any endpoint carrying customer data
- Balances and transaction amounts tied to an identifiable customer
- Anything from a stack trace that embeds the above

Log identifiers that are meaningless outside the system: internal UUIDs, correlation ids, error codes, durations, counts.

```java
// PROHIBITED
log.info("Transfer for account {} to IBAN {} amount {}", accountNumber, creditIban, amount);

// GOOD
log.info("Transfer accepted. transferId={}, debitAccountId={}, rail={}",
         transferId, debitAccountId, rail);
```

### 17.4 Log Levels

| Level | Use For | Production |
|:------|:--------|:-----------|
| `ERROR` | Failure needing human action; always alertable | On |
| `WARN` | Degradation, fallback taken, retry exhausted, lock conflict | On |
| `INFO` | Significant business events: transfer accepted, account opened | On, and rate-controlled |
| `DEBUG` | Developer diagnostics | Off |
| `TRACE` | Fine-grained tracing | Off, and never enabled in production |

An expected business rejection — insufficient funds, limit exceeded — is `INFO`, not `ERROR`. `ERROR` means "a human must look at this". Logging expected outcomes at `ERROR` trains the team to ignore the error log, which is how a real failure gets missed.

### 17.5 Metrics

```java
@Service
public class TransferService {

    private final Counter completed;
    private final Counter rejected;
    private final Timer   duration;

    public TransferService(MeterRegistry registry) {
        this.completed = Counter.builder("transfer.completed")
            .description("Transfers successfully booked")
            .register(registry);
        this.rejected = Counter.builder("transfer.rejected")
            .tag("reason", "unknown")
            .register(registry);
        this.duration = Timer.builder("transfer.duration")
            .publishPercentiles(0.5, 0.95, 0.99)
            .register(registry);
    }
}
```

Minimum metric set for every service:

| Metric | Type | Why |
|:-------|:-----|:----|
| Request rate, error rate, duration percentiles per endpoint | Counter, Timer | Baseline service health |
| Business event counters (transfers completed, rejected by reason) | Counter | Detects a functional break that leaves HTTP status codes healthy |
| Connection pool active, idle, pending, and wait time | Gauge, Timer | Pool exhaustion is the most common latency cause |
| Outbox backlog depth and oldest unpublished age | Gauge | Detects a stalled relay before downstream notices |
| Circuit breaker state per instance | Gauge | Explains a latency or error spike immediately |
| Scheduled job last-success timestamp and duration | Gauge, Timer | A job that stops running produces no errors at all |
| JVM heap, GC pause, thread count | Gauge | Standard |

**Cardinality discipline**: never tag a metric with a customer id, account id, transfer id, or any unbounded value. It creates one time series per value and takes down the metrics backend.

**Measure percentiles, not averages.** An average hides the tail. p95, p99, and max are what customers experience.

### 17.6 Tracing

Micrometer Tracing propagates the trace context across HTTP calls and message headers. Sampling is configured per environment: full sampling in non-production, a low rate in production with forced sampling on errors. Span attributes follow the same prohibition list as logs — no PII, no account numbers, no amounts.

---

## 18. Testing

### 18.1 Test Types and Proportions

```
              ┌───────────────┐
              │  End-to-end   │   Few. Slow. Critical journeys only:
              │               │   open account, transfer, statement.
              ├───────────────┤
              │  Integration  │   Real PostgreSQL via Testcontainers.
              │               │   Repositories, migrations, transactions.
              ├───────────────┤
              │  Slice        │   @WebMvcTest, @DataJpaTest, @JsonTest.
              │               │   Fast, focused, one layer.
              ├───────────────┤
              │               │
              │     Unit      │   The bulk. No Spring context at all.
              │               │   Business rules, money arithmetic, policies.
              └───────────────┘
```

### 18.2 Coverage Requirements

**80% line coverage** overall, enforced by JaCoCo in the build. **100% branch coverage** is mandatory on:

- Every class performing monetary arithmetic
- The ledger posting path and its balance invariant
- Idempotency handling
- Limit and eligibility policy evaluation
- Interest, fee, and charge calculation
- Authorization decisions

Coverage is a floor, not a goal. A test that executes a line without asserting its outcome contributes coverage and no safety.

### 18.3 Unit Tests Use No Spring Context

```java
class MoneyTest {

    @Test
    void plus_withSameCurrency_addsExactly() {
        Money a = Money.of("0.10", "EUR");
        Money b = Money.of("0.20", "EUR");

        assertThat(a.plus(b)).isEqualTo(Money.of("0.30", "EUR"));   // Exact — not 0.30000000000000004
    }

    @Test
    void plus_withDifferentCurrency_throws() {
        assertThatThrownBy(() -> Money.of("10.00", "EUR").plus(Money.of("10.00", "USD")))
            .isInstanceOf(CurrencyMismatchException.class);
    }

    @ParameterizedTest
    @CsvSource({
        "1.0050, 1.00",     // HALF_EVEN rounds to even
        "1.0150, 1.02",
        "1.0250, 1.02",
        "1.0350, 1.04"
    })
    void round_usesBankersRounding(String input, String expected) {
        assertThat(new BigDecimal(input).setScale(2, RoundingMode.HALF_EVEN))
            .isEqualByComparingTo(expected);
    }
}
```

`@SpringBootTest` on a unit test loads the whole context for no benefit and turns a 5-millisecond test into a 5-second one.

### 18.4 Test Naming

```java
// Format: methodUnderTest_scenario_expectedOutcome
@Test void execute_whenBalanceInsufficient_throwsInsufficientFundsException() { }
@Test void execute_whenIdempotencyKeyReplayed_returnsOriginalResultWithoutReposting() { }
@Test void accrueInterest_onLeapYear_usesActual366DayBasis() { }
@Test void post_whenEntriesDoNotNetToZero_throwsLedgerWriteException() { }
```

### 18.5 Slice Tests

```java
@WebMvcTest(TransferController.class)
class TransferControllerTest {

    @Autowired  private MockMvc mockMvc;
    @MockitoBean private TransferService transferService;

    @Test
    void createTransfer_withoutIdempotencyKey_returns400() throws Exception {
        mockMvc.perform(post("/api/v1/transfers")
                .contentType(APPLICATION_JSON)
                .content(validTransferJson()))
            .andExpect(status().isBadRequest());
    }

    @Test
    void createTransfer_whenInsufficientFunds_returns422WithErrorCodeAndNoBalance() throws Exception {
        when(transferService.execute(any(), any(), any()))
            .thenThrow(new InsufficientFundsException(ApiErrorCode.INSUFFICIENT_FUNDS, "…"));

        mockMvc.perform(post("/api/v1/transfers")
                .header("Idempotency-Key", UUID.randomUUID().toString())
                .contentType(APPLICATION_JSON)
                .content(validTransferJson()))
            .andExpect(status().isUnprocessableEntity())
            .andExpect(jsonPath("$.errorCode").value("INSUFFICIENT_FUNDS"))
            .andExpect(jsonPath("$.detail").value(not(containsString("balance"))));
    }
}
```

### 18.6 Integration Tests Use a Real Database

H2 is prohibited for integration testing. It has different transaction semantics, different type handling, different `NUMERIC` behaviour, and no PostgreSQL-specific features — so it validates nothing about what will run in production.

```java
@SpringBootTest
@Testcontainers
@ActiveProfiles("test")
class TransferIntegrationTest {

    @Container
    @ServiceConnection                                    // Boot 3.1+ wires the datasource
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired private TransferService     transferService;
    @Autowired private LedgerEntryRepository ledgerRepository;

    @Test
    void execute_postsBalancedDoubleEntry() {
        TransferResult result = transferService.execute(customerId, command, key);

        List<LedgerEntry> entries = ledgerRepository.findByTransferId(result.transferId());

        assertThat(entries).hasSize(2);
        assertThat(netAmount(entries)).isEqualByComparingTo(BigDecimal.ZERO);
    }

    @Test
    void execute_whenRepeatedWithSameKey_doesNotPostTwice() {
        transferService.execute(customerId, command, key);
        transferService.execute(customerId, command, key);           // Replay

        assertThat(ledgerRepository.findByTransferId(any())).hasSize(2);   // Not 4
    }

    @Test
    void execute_whenLedgerWriteFails_rollsBackTheDebit() {
        // The single most important test in a banking service:
        // prove that a partial write is impossible
        ...
    }
}
```

Flyway migrations run against the container, so every migration is exercised by every integration test run.

### 18.7 Concurrency Tests

Money-moving paths are tested under concurrency, not only sequentially:

```java
@Test
void debit_underConcurrentRequests_neverOverdrawsTheAccount() throws Exception {
    accountRepository.save(accountWithBalance("100.00"));

    int threads = 20;
    try (ExecutorService pool = Executors.newFixedThreadPool(threads)) {
        List<Future<?>> futures = IntStream.range(0, threads)
            .mapToObj(i -> pool.submit(() -> transferService.debit(accountId, Money.of("10.00", "EUR"))))
            .toList();

        long succeeded = futures.stream().filter(TransferIntegrationTest::completedNormally).count();

        assertThat(succeeded).isEqualTo(10);                          // Exactly 100.00 / 10.00
        assertThat(balanceOf(accountId)).isEqualByComparingTo("0.00");
        assertThat(balanceOf(accountId)).isNotNegative();
    }
}
```

### 18.8 What Must Be Tested

| Area | Required Tests |
|:-----|:---------------|
| Money arithmetic | Rounding at every boundary, scale preservation, currency mismatch, negative and zero, maximum value |
| Ledger | Entries net to zero, no update or delete possible, reversal creates new entries |
| Transactions | Rollback on failure at each step; partial write impossible |
| Idempotency | Replay returns the original; same key with a different payload is rejected; concurrent arrival |
| Concurrency | No overdraft under parallel debits; no lost update; no deadlock under crossed transfers |
| Validation | Every constraint rejected and every boundary value accepted |
| Error handling | Every error code returns the right status and leaks nothing |
| Migrations | Every migration applies cleanly to an empty schema and to the previous release's schema |

---

## 19. Dependency and Supply Chain

### 19.1 Software Bill of Materials

Every build produces a CycloneDX SBOM, archived with the artifact. When the next widely-exploited vulnerability in a common library is disclosed, the SBOM answers "which of our services ship it, at which version" in minutes rather than days.

```xml
<plugin>
    <groupId>org.cyclonedx</groupId>
    <artifactId>cyclonedx-maven-plugin</artifactId>
    <version>2.9.0</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals><goal>makeAggregateBom</goal></goals>
        </execution>
    </executions>
    <configuration>
        <outputFormat>json</outputFormat>
        <outputName>bom</outputName>
        <includeBomSerialNumber>true</includeBomSerialNumber>
    </configuration>
</plugin>
```

### 19.2 Vulnerability Gating

```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>10.0.4</version>
    <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>     <!-- HIGH and CRITICAL fail the build -->
        <suppressionFiles>
            <suppressionFile>dependency-check-suppressions.xml</suppressionFile>
        </suppressionFiles>
    </configuration>
    <executions>
        <execution><goals><goal>check</goal></goals></execution>
    </executions>
</plugin>
```

- **The build fails on HIGH or CRITICAL.** Not warns.
- **Every suppression has an expiry date and a written justification** naming who approved it and why the vulnerability is not exploitable in this service. A suppression file with undated entries becomes a permanent blind spot.
- Dependencies are reviewed monthly. Security patches are applied within the window the client's policy defines, and a CRITICAL in a reachable code path is applied immediately.

### 19.3 Build Reproducibility

- The Maven wrapper (`mvnw`) is committed, so every build uses the same Maven version.
- Builds resolve from the institution's internal artifact repository, never directly from a public registry. This prevents dependency-confusion attacks and gives a stable, auditable source of every artifact.
- A release build runs against a clean local repository in CI.

### 19.4 Licence Policy

Every dependency's licence is recorded in the SBOM and checked against the institution's allowlist. Copyleft licences (GPL, AGPL) require legal approval before use in a commercial banking product. An unknown or missing licence is treated as prohibited until resolved.

---

## 20. Performance

### 20.1 Targets

Measured at the service, excluding client network time:

| Operation | p95 | p99 |
|:----------|:----|:----|
| Read a single resource (account, payee) | < 100 ms | < 250 ms |
| Paginated list (transactions, page of 20) | < 200 ms | < 500 ms |
| Money movement (transfer, payment) | < 500 ms | < 1000 ms |
| Health endpoint | < 50 ms | < 100 ms |
| Application startup to ready | < 30 s | — |

These are service-level objectives, not aspirations. A regression past them is a release blocker.

### 20.2 The Usual Causes

| Symptom | Usual Cause | Fix |
|:--------|:------------|:----|
| Latency rises with concurrency, CPU idle | Connection pool exhaustion | Reduce transaction scope; remove remote calls from transactions ([§10.6](#106-what-must-never-happen-inside-a-transaction)) |
| One endpoint slow, others fine | N+1 queries | Join fetch, entity graph, or projection ([§9.7](#97-the-n1-problem)) |
| Latency degrades as data grows | Missing index, or offset pagination | Verify with `EXPLAIN (ANALYZE, BUFFERS)`; move to keyset pagination |
| Sporadic multi-second spikes | Lock contention or a long transaction | Shorten transactions; check `pg_locks`; set transaction timeouts |
| Memory grows steadily | Unbounded collection, cache without TTL, or `ThreadLocal` leak | Bound every collection and cache; clear MDC in a `finally` |
| Everything slows at the same time each day | An unlocked or overlapping batch job | Separate batch pool and role ([§15.5](#155-batch-operational-rules)) |

### 20.3 Query Verification

Every query on a hot path has its plan verified with `EXPLAIN (ANALYZE, BUFFERS)` before merge, against a dataset of realistic size. A plan verified against 100 rows tells you nothing about 100 million. A sequential scan on a large table in a request path is a defect, not a tuning opportunity.

### 20.4 Streaming Large Result Sets

Never load a large result set into a `List`. A statement extract or a regulatory report that materializes ten million rows will exhaust the heap.

```java
@Transactional(readOnly = true)
public void exportStatement(UUID accountId, Writer writer) {
    try (Stream<LedgerEntry> entries = ledgerRepository.streamByAccountId(accountId)) {
        entries.forEach(entry -> {
            writer.write(format(entry));
            entityManager.detach(entry);      // Prevent the persistence context from growing
        });
    }
}
```

The `detach` matters: without it the persistence context retains every entity it has seen, and the stream leaks memory exactly as badly as the list would have.

### 20.5 JVM Settings

```
-XX:+UseG1GC
-XX:MaxRAMPercentage=75.0          # Container-aware; never a fixed -Xmx in a container
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/log/heapdump
-XX:+ExitOnOutOfMemoryError        # Fail fast; a degraded instance is worse than a restarted one
```

A heap dump from a banking service contains customer data in memory. The dump path must be on encrypted storage with restricted access, and dumps are treated as regulated data; see [ESTD21 §10.4](./ESTD21_-_Spring_Boot_Data_Protection_And_Security_Standards.md#104-secrets-in-memory-and-heap-dumps).

---

## 21. Common Pitfalls to Avoid

| # | Pitfall | Consequence | Prevention |
|:--|:--------|:------------|:-----------|
| 1 | `double` or `float` for a monetary value | Cumulative rounding error; failed reconciliation | `BigDecimal` and `NUMERIC(19,4)` everywhere ([§11.1](#111-floating-point-is-prohibited-for-money)) |
| 2 | `new BigDecimal(double)` | Binary error carried into an exact type | `new BigDecimal(String)` or `BigDecimal.valueOf` |
| 3 | `BigDecimal.equals` for value comparison | `10.00` and `10.0` compare unequal; wrong branch taken | `compareTo(...) == 0` |
| 4 | `divide` without scale and rounding | `ArithmeticException` on some inputs only, in production | Always pass scale and `RoundingMode.HALF_EVEN` |
| 5 | `@Transactional` called from within the same bean | No transaction at all; partial writes commit silently | Move the method to another bean ([§10.2](#102-the-self-invocation-trap)) |
| 6 | Remote call inside a transaction | Connection pool exhausted by one slow dependency | Call before the transaction, or publish via the outbox |
| 7 | Publishing to a broker inside a transaction | Event without a commit, or commit without an event | Transactional outbox ([§13.2](#132-the-transactional-outbox)) |
| 8 | Money-moving `POST` without an idempotency key | Retry double-charges the customer | Mandatory `Idempotency-Key`, stored in the same transaction |
| 9 | Missing `@Version` on mutable financial state | Lost update; money silently disappears | `@Version` on every concurrently mutable entity |
| 10 | `UPDATE` or `DELETE` on a ledger row | Audit trail destroyed; reconstruction impossible | Append-only ledger; `REVOKE UPDATE, DELETE` at the database |
| 11 | Balance stored as the source of truth | Divergence between balance and history, undetectable | Ledger is truth; balance is a projection, reconciled daily |
| 12 | JPA entity returned from a controller | Internal and regulated fields serialized to the client | Explicit response records ([§6.4](#64-entities-never-cross-the-controller-boundary)) |
| 13 | `spring.jpa.hibernate.ddl-auto` set to `update` | Unreviewed schema change on a regulated database | `validate`, with Flyway owning every change |
| 14 | `open-in-view` left enabled | Hidden N+1 during serialization, outside the transaction | `spring.jpa.open-in-view: false` |
| 15 | `EnumType.ORDINAL` | Inserting an enum constant silently reinterprets stored rows | `EnumType.STRING` always |
| 16 | `@Scheduled` without a distributed lock | End-of-day job runs once per instance; interest posted N times | ShedLock plus an idempotent job body |
| 17 | Consumer with auto-commit enabled | Message lost on crash after the offset commits | `enable-auto-commit: false`, manual ack after the work commits |
| 18 | No dead-letter route on a consumer | One poison message halts a partition indefinitely | `DeadLetterPublishingRecoverer` with a monitored DLT |
| 19 | Caching a balance or an authorization decision | Stale balance authorizes an overdraft; revoked access persists | Never cache authoritative or security state ([§14.1](#141-what-must-never-be-cached)) |
| 20 | `e.getMessage()` returned to the client | Account numbers, SQL, and hostnames leaked in an error body | Curated messages keyed by error code ([§8.3](#83-the-global-exception-handler)) |
| 21 | Outbound call with no timeout | One hung dependency cascades into a full outage | Explicit connect and read timeouts on every client |
| 22 | Fallback that fails open on a compliance check | Unscreened transfer proceeds during a screening outage | Fail closed on every compliance-relevant dependency |
| 23 | Field injection with `@Autowired` | Untestable, non-final, hides an oversized dependency list | Constructor injection only, enforced by ArchUnit |
| 24 | Mutable state on a singleton `@Service` | One customer's data served to another under concurrency | Stateless beans; per-request state as parameters |
| 25 | H2 used for integration tests | Different semantics from PostgreSQL; production-only bugs | Testcontainers with the production PostgreSQL version |
| 26 | Unbounded `@Async` executor or queue | Out-of-memory under load | Bounded pool and queue, explicit rejection policy |
| 27 | `LocalDateTime` for a business timestamp | Ambiguity across a daylight-saving transition | `Instant` and `TIMESTAMPTZ` throughout |
| 28 | `skipLimit` above zero on a financial batch | Job reports success while records were silently skipped | `skipLimit(0)`; fail loudly and restart |

