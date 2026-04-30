# ESTD7 - Java Programming Standards for Bingo Microservices and SmartFox Server

**ESTD7 — Java Programming Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD7 |
| Version | 4.0 |
| Status | Active |
| Last Updated | 2026-04-09 |
| Applies To | Java 17+ code for new Bingo microservices and SmartFox live server |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management) |
| Approval | Director of Engineering / Server Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD7 applies to Java 17+ code written for the new Bingo game's SEAM microservices and the SmartFox live server used by both games. Those SEAM microservices use MongoDB Atlas and MySQL on AWS RDS via service-owned schemas. All rules from [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), and [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management) apply in full. This document narrows and extends those rules for Java specifically.

**SmartFox-specific standards** are in [ESTD12](./ESTD12_-_Smartfox_Server_Standards.md#estd12--smartfox-server-standards-for-bingo-game-development), which builds on top of this document. Read ESTD7 first, then [ESTD12](./ESTD12_-_Smartfox_Server_Standards.md#estd12--smartfox-server-standards-for-bingo-game-development) for SmartFox work.

**Microservice framework note**: The new Bingo API uses a **SEAM** framework that is architecturally similar to Spring Boot — it provides dependency injection, layered controllers/services/repositories, configuration injection, and health endpoints — but it is SEAM — not Spring Boot. Where this document references Spring-style annotations or conventions (e.g., `@Transactional`, `@Service`, `@Repository`), use the equivalent annotation or mechanism provided by the SEAM. The architectural intent is the same.

---

## Table of Contents

- [ESTD7 - Java Programming Standards for Bingo Microservices and SmartFox Server](#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Java Version and Language Features](#2-java-version-and-language-features)
    - [2.1 Java 17 LTS](#21-java-17-lts)
    - [2.2 Immutability by Default](#22-immutability-by-default)
  - [3. Coding Style](#3-coding-style)
  - [4. Naming Conventions (Java)](#4-naming-conventions-java)
  - [5. Class and Package Organization](#5-class-and-package-organization)
    - [5.1 Package Structure Per Microservice](#51-package-structure-per-microservice)
    - [5.2 Dependency Direction Rule](#52-dependency-direction-rule)
  - [6. Type System and Null Safety](#6-type-system-and-null-safety)
    - [6.1 Optional for Nullable Returns](#61-optional-for-nullable-returns)
    - [6.2 @NonNull and @Nullable Annotations](#62-nonnull-and-nullable-annotations)
    - [6.3 Avoid Optional.get() Without Check](#63-avoid-optionalget-without-check)
  - [7. Error Handling in Java](#7-error-handling-in-java)
    - [7.1 Custom Exception Hierarchy](#71-custom-exception-hierarchy)
    - [7.2 Individual Error Handling — Apply ESTD1 §7](#72-individual-error-handling--apply-estd1-7)
    - [7.3 Global Exception Handler (Framework Equivalent of @ControllerAdvice)](#73-global-exception-handler-framework-equivalent-of-controlleradvice)
  - [8. Application Layer Standards](#8-application-layer-standards)
    - [8.1 Configuration](#81-configuration)
    - [8.2 Layered Application](#82-layered-application)
    - [8.3 Bean Scope](#83-bean-scope)
    - [8.4 Health Endpoints](#84-health-endpoints)
    - [8.5 Logging](#85-logging)
  - [9. Input Validation](#9-input-validation)
  - [10. Database Access](#10-database-access)
    - [10.1 ORM vs. Plain SQL](#101-orm-vs-plain-sql)
    - [10.2 Query Safety](#102-query-safety)
    - [10.3 Transactions](#103-transactions)
    - [10.4 N+1 Query Prevention](#104-n1-query-prevention)
  - [11. Concurrency Standards](#11-concurrency-standards)
    - [11.1 Prefer Immutability](#111-prefer-immutability)
    - [11.2 Use java.util.concurrent](#112-use-javautilconcurrent)
    - [11.3 Thread Pool Sizing](#113-thread-pool-sizing)
  - [12. Dependency Management](#12-dependency-management)
    - [12.1 Bill of Materials (BOM)](#121-bill-of-materials-bom)
    - [12.2 BOM Generation for Java/SEAM Projects](#122-bom-generation-for-javaseam-projects)
    - [12.3 Vulnerability Scanning](#123-vulnerability-scanning)
    - [12.4 Dependency Rules](#124-dependency-rules)
  - [13. Security-Specific Java Rules](#13-security-specific-java-rules)
  - [14. Testing Java Code](#14-testing-java-code)
    - [14.1 Testing Stack](#141-testing-stack)
    - [14.2 Test Naming](#142-test-naming)
    - [14.3 Identifying Code Paths (see ESTD16 §4 for the general approach)](#143-identifying-code-paths-see-estd16-4-for-the-general-approach)
    - [14.4 Testcontainers for Integration Tests](#144-testcontainers-for-integration-tests)
  - [15. SEAM Framework](#15-seam-framework)
    - [15.1 SEAM Layered Architecture](#151-seam-layered-architecture)
    - [15.2 SEAM Annotations](#152-seam-annotations)
    - [15.3 SEAM Dependency Injection Rules](#153-seam-dependency-injection-rules)
    - [15.4 SEAM Configuration](#154-seam-configuration)
    - [15.5 BOM Generation for Java/SEAM Projects](#155-bom-generation-for-javaseam-projects)
  - [16. Common Pitfalls to Avoid](#16-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

**Why this document exists**: Java has a rich type system and powerful concurrency primitives, but also well-known pitfalls: unchecked exceptions that propagate unexpectedly, the N+1 ORM problem, thread-safety bugs from shared mutable state, and `NullPointerException` in production. This document encodes the patterns that avoid these pitfalls while building maintainable, testable microservices and a robust SmartFox integration.

---

## 2. Java Version and Language Features

### 2.1 Java 17 LTS

Target **Java 17 LTS**. Always run the latest patch release. The following Java 17 language features are encouraged and preferred over older alternatives:

| Feature | Use For | Example |
|:--------|:--------|:--------|
| `record` | DTOs, value objects, event payloads | `record BallDrawnEvent(int ball, Instant calledAt) {}` |
| `sealed` classes | Closed type hierarchies, result types | `sealed interface RoomEvent permits PlayerJoined, BallDrawn, GameEnded {}` |
| Pattern matching for `instanceof` | Replacing verbose casts | `if (event instanceof BallDrawnEvent e) { process(e.ball()); }` |
| Text blocks | Multi-line strings (SQL, JSON templates) | `"""SELECT * FROM players WHERE id = ?"""` |
| `switch` expression | Replace `switch` statements with value-producing expressions | `String label = switch(state) { case ACTIVE -> "Active"; ... };` |

### 2.2 Immutability by Default

Prefer immutable objects. Immutability eliminates a class of concurrency bugs and makes code easier to reason about.

```java
// Immutable record — best for DTOs and event payloads
public record BingoWinEvent(int playerId, int roomId, WinPattern pattern, Instant timestamp) {
    // Compact constructor for validation
    public BingoWinEvent {
        Objects.requireNonNull(pattern, "pattern must not be null");
        if (playerId <= 0) throw new IllegalArgumentException("Invalid playerId: " + playerId);
    }
}

// Immutable class with defensive copies
public final class BingoCard {
    private final int cardId;
    private final int[] numbers;  // 5x5 grid flattened to 25 elements

    public BingoCard(int cardId, int[] numbers) {
        this.cardId  = cardId;
        this.numbers = Arrays.copyOf(numbers, numbers.length);  // Defensive copy — prevents mutation
    }

    public int[] getNumbers() {
        return Arrays.copyOf(this.numbers, this.numbers.length);  // Defensive copy on read
    }
}
```

---

## 3. Coding Style

Follow the **Google Java Style Guide** as the baseline. Enforce with **Checkstyle** in CI — builds must not merge if Checkstyle violations exist. Apply **Google Java Format** automatically via IDE plugin or pre-commit hook.

Key points:

- 2-space indentation (Google style — not 4)  
- Opening braces always on the same line  
- Line length limit: 100 characters  
- `@Override` annotation is mandatory when overriding


---

## 4. Naming Conventions (Java)

| Symbol | Convention | Example |
|:-------|:-----------|:--------|
| Class / Interface / Enum / Record | PascalCase | `BingoRoomService`, `PlayerRepository` |
| Method | camelCase | `rewardClaim()`, `playerFindById()` | 
| Variable | camelCase | `playerId`, `roomState` |
| Constant (static final) | UPPER_SNAKE_CASE | `ROOM_PLAYER_COUNT_MAX` |
| Package | lowercase, dot-separated | `com.bingo.reward.service` |
| Generic type parameter | Single uppercase letter or T-prefixed | `T`, `E`, `TResult` |

---

## 5. Class and Package Organization

### 5.1 Package Structure Per Microservice

Each microservice follows this package structure:

```
com.bingo.{service-name}/
├── api/              ← HTTP controllers (presentation layer)
│   └── RewardController.java
├── service/          ← Business logic (domain layer)
│   └── RewardClaimService.java
├── repository/       ← Data access (infrastructure layer)
│   └── RewardClaimRepository.java
├── model/            ← Domain entities
│   └── RewardClaim.java
├── dto/              ← Request/response data transfer objects
│   ├── RewardClaimRequest.java
│   └── RewardClaimResponse.java
├── exception/        ← Domain-specific exceptions
│   └── RewardAlreadyClaimedException.java
└── config/           ← Service configuration
    └── RewardServiceConfig.java
```

### 5.2 Dependency Direction Rule

**Direct Database Coupling Prohibition**: Direct database coupling means one microservice bypasses another's API and queries its database tables directly via SQL or driver calls. This is prohibited in the new Java architecture. See [ESTD4 §2.3 New Java API: Microservice Design Principles](./ESTD4_-_Server_Engg_Standards.md#23-new-java-api-microservice-design-principles) for the full definition and explanation. The repository pattern enforced below is the correct alternative: each service exposes a well-defined API, and other services call that API, not the underlying database.

Dependencies must only point inward:

```
api → service → repository
api → dto
service → model
service → repository (via interface)

PROHIBITED:
  repository → service  (circular)
  model → service       (domain depending on application)
```

---

## 6. Type System and Null Safety

### 6.1 Optional for Nullable Returns

Use `Optional<T>` as the return type for methods that might not find a result. Never return `null` from a method where the caller expects a value.

```java
// GOOD — Optional signals "might not exist" in the type signature
public Optional<Player> findById(long playerId) {
    return Optional.ofNullable(playerRepository.findOne(playerId));
}

// Usage — forces the caller to handle the empty case
Player player = playerRepository.findById(playerId)
    .orElseThrow(() -> new PlayerNotFoundException(playerId));
```

Do **not** use `Optional` as a method parameter or field type — only as a return type.

### 6.2 @NonNull and @Nullable Annotations

Annotate method parameters and return types with `@NonNull` / `@Nullable` (from `org.checkerframework.checker.nullness.qual` or Jetbrains annotations). This enables static analysis tools to detect Null Pointer Exception (NPE) risks at compile time.

### 6.3 Avoid Optional.get() Without Check

```java
// BAD — throws NoSuchElementException if empty
String username = playerRepository.findById(id).get().getUsername();

// GOOD — explicit handling
String username = playerRepository.findById(id)
    .map(Player::getUsername)
    .orElse("Unknown Player");
```

---

## 7. Error Handling in Java

**Entry-point boundary rule**: Java controller methods are entry-point boundaries ([ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions)). They may wrap the entire operation in a single try block with multiple typed catch clauses. Code in service and repository classes called from controllers must use individual per-statement try-catch blocks ([ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)).

### 7.1 Custom Exception Hierarchy

```java
// Base
public class BingoServiceException extends RuntimeException { ... }

// Domain exceptions — extend the base
public class PlayerNotFoundException        extends BingoServiceException { ... }
public class RewardAlreadyClaimedException  extends BingoServiceException { ... }
public class InsufficientBalanceException   extends BingoServiceException { ... }
public class RoomNotFoundException         extends BingoServiceException { ... }
public class RoomFullException             extends BingoServiceException { ... }

// Infrastructure exceptions
public class DatabaseException             extends BingoServiceException { ... }
public class CacheException               extends BingoServiceException { ... }
public class ExternalApiException         extends BingoServiceException { ... }
```

Use **unchecked exceptions** (extending `RuntimeException`) for domain errors. Java checked exceptions add noise to method signatures without improving safety in a framework-managed request/response model.

### 7.2 Individual Error Handling — Apply ESTD1 §7

```java
public RewardClaimResponse rewardClaim(long playerId, String rewardId) {
    // Each operation handled individually
    Player player;
    try {
        player = playerRepository.findById(playerId)
            .orElseThrow(() -> new PlayerNotFoundException(playerId));
    } catch (DatabaseException e) {
        logger.error("DB failure loading player during reward claim",
            Map.of("playerId", playerId, "error", e.getMessage()), e);
        throw new ExternalApiException("Failed to load player data", e);
    }

    if (rewardClaimRepository.existsClaim(playerId, rewardId, currentCycleId)) {
        throw new RewardAlreadyClaimedException(rewardId);
    }

    // ... proceed with claim
}
```

### 7.3 Global Exception Handler (Framework Equivalent of @ControllerAdvice)

Register a global exception handler at the framework level that converts domain exceptions to HTTP responses:

```java
@ExceptionHandler  // SEAM annotation equivalent
public class GlobalExceptionHandler {

    public ApiResponse handle(RewardAlreadyClaimedException e, HttpRequest request) {
        logger.info("Reward already claimed", Map.of("rewardId", e.getRewardId()));
        return ApiResponse.error("REWARD_ALREADY_CLAIMED", e.getMessage(), HTTP_409_CONFLICT);
    }

    public ApiResponse handle(PlayerNotFoundException e, HttpRequest request) {
        return ApiResponse.error("PLAYER_NOT_FOUND", e.getMessage(), HTTP_404_NOT_FOUND);
    }

    public ApiResponse handle(Exception e, HttpRequest request) {
        // Final safety net — log with full context, return generic 500
        logger.error("Unhandled exception", Map.of(
            "requestId", request.getRequestId(),
            "path",      request.getPath()
        ), e);
        return ApiResponse.error("INTERNAL_ERROR", "An unexpected error occurred.", HTTP_500);
    }
}
```

---

## 8. Application Layer Standards

### 8.1 Configuration

Externalize all configuration. Never hardcode environment-specific values. Configuration is injected by the framework from environment variables or configuration files:

```java
@Configuration
public class RewardServiceConfig {
    @Value("${reward.weekly.bonus.coins}")   // Read from config, not hardcoded
    private int weeklyBonusCoins;

    @Value("${content.reset.period.days}")   // Periodic cadence from config
    private int contentResetPeriodDays;
}
```

### 8.2 Layered Application

```
Controller  → receives HTTP request, delegates to service, returns response
Service     → business logic, validation, orchestration
Repository  → data access only (no business logic in repositories)
Model       → domain entity (no business logic beyond invariant enforcement)
```

### 8.3 Bean Scope

Services and repositories must be **singletons** (the default in most DI frameworks). Never use request-scoped or session-scoped beans for services that perform I/O — this creates unnecessary object churn.

### 8.4 Health Endpoints

Every microservice must expose a health endpoint (typically `/health` or `/actuator/health`). It must check all critical dependencies (database, cache, any downstream services) and respond in < 1 second. Return a 200 when healthy, 503 when degraded. See [ESTD4 §16. Observability: Logging, Metrics, Alerting](./ESTD4_-_Server_Engg_Standards.md#16-observability-logging-metrics-alerting) for the expected response format.

### 8.5 Logging

Use SLF4J with Logback (or the SEAM-approved equivalent) for all Java services. Log messages must be structured, parameterized, and correlated.

- Use parameterized logging: `log.info("Claim rejected. playerId={}, reason={}", playerId, reason);`
- Never concatenate strings inside log calls.
- Populate MDC with request/correlation identifiers at the boundary.
- Do not log secrets, tokens, raw personal data, or full request bodies unless explicitly redacted.
- Hot-path INFO logs must be sampled or suppressed; DEBUG and TRACE must be disabled in production by default.

---

## 9. Input Validation

Use the framework's validation mechanism (equivalent to Bean Validation / Jakarta Validation with `@Valid`). Annotate DTO fields with constraint annotations and validate at the controller boundary.

```java
public record RewardClaimRequest(
    @NotBlank(message = "rewardId is required")
    @Size(max = 64)
    String rewardId,

    @NotBlank(message = "idempotencyKey is required")
    @Pattern(regexp = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
             message = "idempotencyKey must be a valid UUID v4")
    String idempotencyKey
) {}

// Controller
public ApiResponse rewardClaim(@Valid RewardClaimRequest request, ...) {
    // @Valid triggers validation; a violation throws a ValidationException
    // which is handled by the GlobalExceptionHandler and returns a 400
}
```

---

## 10. Database Access

### 10.1 ORM vs. Plain SQL

The SEAM provides Object Relational Mapping (ORM) capabilities similar to Spring Data JPA. Rules:

- Use the ORM's repository interfaces for standard CRUD operations.  
- Use explicit query methods (or raw SQL via the framework's query builder) for complex queries.  
- Never use raw JDBC `Statement` — always use prepared statements or the ORM.

See [ESTD4 §11. Object-Relational Mapping (ORM)](./ESTD4_-_Server_Engg_Standards.md#11-object-relational-mapping-orm) for the full ORM policy, including the N+1 anti-pattern and transaction management.

### 10.2 Query Safety

All queries must use parameterized inputs. Never concatenate user input into a query string.

```java
// BAD — SQL injection
String query = "SELECT * FROM players WHERE username = '" + username + "'";

// GOOD — parameterized
Player player = playerRepository.findByUsername(username);
// The repository implementation uses a prepared statement internally
```

### 10.3 Transactions

Use the framework's transaction annotation for all multi-step operations that must be atomic:

```java
@Transactional   // framework-specific annotation
public RewardClaimResult rewardClaim(long playerId, String rewardId) {
    // Both operations are in one transaction — either both succeed or both roll back
    coinLedger.record(playerId, WEEKLY_BONUS_COINS, LedgerType.REWARD_CLAIM);
    rewardClaimRepository.save(new RewardClaim(playerId, rewardId, currentCycleId));
    return new RewardClaimResult(WEEKLY_BONUS_COINS);
}
```

If the `@Transactional` equivalent is not available in the SEAM, use explicit transaction management with `try-finally`:

```java
Transaction tx = transactionManager.begin();
try {
    coinLedger.record(playerId, WEEKLY_BONUS_COINS, LedgerType.REWARD_CLAIM);
    rewardClaimRepository.save(new RewardClaim(playerId, rewardId, currentCycleId));
    tx.commit();
} catch (Exception e) {
    tx.rollback();
    throw e;
}
```

### 10.4 N+1 Query Prevention

Always verify that ORM associations do not generate N+1 queries. Use `EXPLAIN` to verify the query plan. Use batch fetching or JOIN queries for related data.

---

## 11. Concurrency Standards

### 11.1 Prefer Immutability

Use `final` fields and `record` types. An object that cannot be mutated cannot have a race condition.

### 11.2 Use java.util.concurrent

Use the appropriate concurrent collection for shared mutable state:

```java
// Thread-safe map for shared data accessed by multiple threads
private final ConcurrentHashMap<Long, PlayerSession> activeSessions = new ConcurrentHashMap<>();

// Atomic counter — lock-free increment
private final AtomicLong totalGamesPlayed = new AtomicLong(0);

// Blocking queue for producer-consumer patterns
private final BlockingQueue<GameEvent> eventQueue = new LinkedBlockingQueue<>();
```

### 11.3 Thread Pool Sizing

Use `ExecutorService` with a configured pool rather than creating raw threads. Size thread pools based on workload type:

```java
// CPU-bound work: number of available processors
ExecutorService cpuPool = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());

// I/O-bound work: larger pool (threads spend most time waiting for I/O)
ExecutorService ioPool = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors() * 4);
```

Name your threads for easy identification in thread dumps and profiler output:

```java
ExecutorService pool = Executors.newFixedThreadPool(4,
    r -> new Thread(r, "bingo-reward-worker-" + threadCounter.incrementAndGet()));
```

---

## 12. Dependency Management

### 12.1 Bill of Materials (BOM)

A Bill of Materials (BOM) for software is a complete, machine-readable inventory of every dependency used by a project, including their exact versions, licenses, and known vulnerabilities. In the context of software supply-chain security and compliance, a BOM (specifically a **Software Bill of Materials / SBOM**) is the definitive answer to "what is in this artifact?"

**Why generate a BOM?**

- **Security**: Enables automated scanning for known Common Vulnerabilities and Exposures (CVEs) across all transitive dependencies.  
- **License compliance**: Identifies any dependencies with incompatible licenses (GPL in a commercial product, for example).  
- **Incident response**: When a new critical CVE is disclosed (e.g., Log4Shell), the BOM instantly tells you which services are affected.  
- **Audit**: Enterprise clients and app store compliance programs may require a current SBOM.

**Generating a BOM for SEAM microservices (Maven):**

```shell
# Generate a CycloneDX SBOM in XML format
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom

# Output: target/bom.xml (or bom.json with -DschemaVersion=1.4 -Dformat=json)
# This file lists every direct and transitive dependency with version and license.
```

Viewing the full dependency tree:

```shell
# Human-readable tree of all dependencies
mvn dependency:tree

# Check for version conflicts (convergence)
mvn enforcer:enforce -Drules=dependencyConvergence
```

**Using a BOM to lock dependency versions across modules:**

```html
<!-- In the parent pom.xml — all modules inherit these versions -->
<dependencyManagement>
    <dependencies>
        <!-- Import a published BOM (e.g., Jackson) to align all Jackson modules -->
        <dependency>
            <groupId>com.fasterxml.jackson</groupId>
            <artifactId>jackson-bom</artifactId>
            <version>2.16.1</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        <!-- Pin internal dependencies explicitly -->
        <dependency>
            <groupId>com.bingo</groupId>
            <artifactId>bingo-common</artifactId>
            <version>${bingo.common.version}</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**BOM in CI**: The CI pipeline must run `mvn dependency-check:check` (OWASP Dependency Check) on every build. Builds with known HIGH or CRITICAL CVEs must fail. The generated BOM must be archived alongside the build artifact in S3 for traceability.

Use a BOM to manage consistent dependency versions across the project. This prevents version conflicts between libraries from the same ecosystem.

### 12.2 BOM Generation for Java/SEAM Projects

See [ESTD1 §26. Generating a Bill of Materials (BOM) for a Project](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#26-generating-a-bill-of-materials-bom-for-a-project) for the full BOM governance policy. For Java/SEAM projects specifically:

Add the CycloneDX Maven plugin to every `pom.xml`:

```html
<plugin>
    <groupId>org.cyclonedx</groupId>
    <artifactId>cyclonedx-maven-plugin</artifactId>
    <version>2.8.0</version>
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

The CI/CD pipeline runs `mvn verify` which generates `target/bom.json`. The Trivy scan step then validates the BOM against the CVE database before the build artifact is promoted to the staging registry.

### 12.3 Vulnerability Scanning

Run `mvn dependency-check` (OWASP Dependency Check) or equivalent in CI. Builds with known high/critical CVEs must be blocked from merging.

### 12.4 Dependency Rules

- All dependencies pinned to explicit versions — no `LATEST`, no version ranges.  
- `testImplementation` / `test scope` dependencies (JUnit, Mockito, AssertJ, Testcontainers) must be scoped correctly and never included in the production artifact.  
- Review dependencies monthly for updates; apply security patches immediately.

---

## 13. Security-Specific Java Rules

- Deserialization of untrusted data using Java's native `ObjectInputStream` is **prohibited** — it is a critical security vulnerability. Use JSON (Jackson) or Protocol Buffers with strict type whitelisting instead.  
- Do not log sensitive data (tokens, passwords, PII). Use structured logging with explicit field exclusion.  
- All external inputs validated before use (see [§9. Input Validation](#9-input-validation)).  
- Use `SecureRandom` for all cryptographic operations — never `java.util.Random`.

```java
// WRONG — java.util.Random is not cryptographically secure
String token = Long.toHexString(new Random().nextLong());

// CORRECT
byte[] tokenBytes = new byte[32];
new SecureRandom().nextBytes(tokenBytes);
String token = HexFormat.of().formatHex(tokenBytes);
```

---

## 14. Testing Java Code

Refer [ESTD16](./ESTD16_-_Paths_And_Unit_Testing_Strategy.md#estd16---paths-branches-and-unit-testing-strategy) for the full documentation on Paths, and Unit testing Strategies.

### 14.1 Testing Stack

- **JUnit 5** — test runner  
- **Mockito** — mocking dependencies  
- **AssertJ** — fluent assertions (prefer over plain JUnit assertions for readability)  
- **Testcontainers** — integration tests with real databases (MySQL, Redis)

Target: **80% line coverage** on all service and domain logic classes. Priority: `RewardClaimService`, `BingoWinCalculator`, content reset logic, and any class containing economic operations.

### 14.2 Test Naming

```java
// Format: methodUnderTest_scenario_expectedOutcome
@Test
void rewardClaim_whenAlreadyClaimed_throwsRewardAlreadyClaimedException() { ... }

@Test
void calculateWinPattern_withFullHousePattern_returnsTrue() { ... }

@Test
void findById_whenPlayerDoesNotExist_returnsEmptyOptional() { ... }
```

### 14.3 Identifying Code Paths (see ESTD16 §4 for the general approach)

In Java, use code coverage tools (JaCoCo) to visualize which branches are covered. Every `if`, `else`, `case`, `catch`, and conditional expression is a branch that needs a test.

```java
@ExtendWith(MockitoExtension.class)
class RewardClaimServiceTest {

    @Mock private PlayerRepository playerRepository;
    @Mock private RewardClaimRepository rewardClaimRepository;
    @InjectMocks private RewardClaimService sut;

    @Test
    void rewardClaim_whenPlayerNotFound_throwsPlayerNotFoundException() {
        when(playerRepository.findById(1L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> sut.rewardClaim(1L, "weekly_bonus"))
            .isInstanceOf(PlayerNotFoundException.class);
    }

    @Test
    void rewardClaim_whenAlreadyClaimed_throwsRewardAlreadyClaimedException() {
        when(playerRepository.findById(1L)).thenReturn(Optional.of(testPlayer()));
        when(rewardClaimRepository.existsClaim(eq(1L), anyString(), any())).thenReturn(true);

        assertThatThrownBy(() -> sut.rewardClaim(1L, "weekly_bonus"))
            .isInstanceOf(RewardAlreadyClaimedException.class);
    }

    @Test
    void rewardClaim_happyPath_returnsClaimResultWithCorrectCoins() {
        when(playerRepository.findById(1L)).thenReturn(Optional.of(testPlayer()));
        when(rewardClaimRepository.existsClaim(any(), any(), any())).thenReturn(false);

        RewardClaimResult result = sut.rewardClaim(1L, "weekly_bonus");

        assertThat(result.getCoinsAwarded()).isEqualTo(WEEKLY_BONUS_COINS);
    }
}
```

### 14.4 Testcontainers for Integration Tests

```java
@Testcontainers
class PlayerRepositoryIntegrationTest {

    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0")
        .withDatabaseName("bingo_test")
        .withUsername("test")
        .withPassword("test");

    @Test
    void findById_withRealDatabase_returnsCorrectPlayer() {
        // This test runs against a real MySQL in a Docker container
        // No mocking — tests the actual SQL and ORM mapping
        Player player = playerRepository.findById(testPlayerId);
        assertThat(player).isNotEmpty();
        assertThat(player.get().getUsername()).isEqualTo("testuser");
    }
}
```

---

## 15. SEAM Framework

**Definition: SEAM** is the custom Java microservice framework used by the new Bingo game's API server. SEAM is architecturally similar to Spring Boot — it provides dependency injection, layered controller/service/repository architecture, configuration injection, and HTTP routing — but is a custom, in-house implementation. SEAM is not Spring Boot; do not import Spring Boot dependencies or assume Spring Boot behavior. Where these standards reference Spring Boot patterns, apply the SEAM equivalent.

### 15.1 SEAM Layered Architecture

```
Request
  │
  ▼
@RouteHandler (Controller layer — boundary function; see ESTD1 §10 and ESTD4 §9)
  │  Parses, validates, authorizes, delegates
  ▼
@SeamService (Service layer — business logic only; no HTTP types)
  │  Orchestrates domain logic; calls repositories and other services
  ▼
@SeamRepository (Repository/DAO layer — data access only; no business logic)
  │  Executes queries; maps result sets to domain objects
  ▼
Database (MySQL on RDS / service-owned schema)
```

### 15.2 SEAM Annotations

| Annotation | Purpose | Layer | 
|:-----------|:--------|:------|
| `@RouteHandler(method, path)` | Maps an HTTP endpoint to a controller method | Controller |
| `@RequiresAuth` | Enforces authentication; injects validated session into request | Controller | 
| `@RateLimit(key, maxPerHour)` | Applies a named rate limit to the endpoint | Controller |
| `@SeamService` | Marks a class as a SEAM-managed service (injected via DI) | Service |
| `@SeamRepository` | Marks a class as a repository; receives a `DataSource` via DI | Repository |
| `@Inject` | Constructor or field injection by SEAM's DI container | All |
| `@SeamConfig(key)` | Injects a configuration value from the SEAM config hierarchy | All |
| `@Transactional` | Wraps the method in a database transaction | Service/Repository |

### 15.3 SEAM Dependency Injection Rules

- All dependencies must be injected through constructors, not field injection.  
- No `new ServiceClass()` calls inside other service classes — all service dependencies are injected.  
- SEAM's DI container is populated at startup from the class graph; lazy initialization is not permitted.

```java
// GOOD — constructor injection with SEAM
@SeamService
public class RewardService {
    private final RewardRepository rewardRepository;
    private final PlayerService playerService;
    private final IdempotencyService idempotencyService;

    @Inject
    public RewardService(RewardRepository rewardRepository,
                         PlayerService playerService,
                         IdempotencyService idempotencyService) {
        this.rewardRepository    = rewardRepository;
        this.playerService       = playerService;
        this.idempotencyService  = idempotencyService;
    }
}
```

### 15.4 SEAM Configuration

SEAM uses the same configuration hierarchy as defined in [ESTD1 §13.2 Configuration Hierarchy](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#132-configuration-hierarchy):

```
Code defaults ← seam.properties ← Environment variables ← Runtime feature flags
```

Configuration values are injected via `@SeamConfig`:

```java
@SeamService
public class ContentResetService {
    @SeamConfig("content.reset_period_days")
    private int resetPeriodDays;  // Injected from config; code default is the annotation fallback

    // Or via constructor for testability:
    private final int resetPeriodDays;

    @Inject
    public ContentResetService(@SeamConfig("content.reset_period_days") int resetPeriodDays) {
        this.resetPeriodDays = resetPeriodDays;
    }
}
```

### 15.5 BOM Generation for Java/SEAM Projects

Refer [§12.2 BOM Generation for Java/SEAM Projects](#122-bom-generation-for-javaseam-projects).

---

## 16. Common Pitfalls to Avoid

| # | Pitfall | Consequence | Prevention |
|:--|:--------|:------------|:-----------|
| 1 | `Optional.get()` without `isPresent()` check | `NoSuchElementException` in production | Use `orElseThrow()` or `map()` always | 
| 2 | Returning `null` instead of `Optional.empty()` | Null Pointer Exception (NPE) at call site | Never return null from a finder method |
| 3 | Mutable static fields | Thread-safety bugs across concurrent requests | Use DI-managed singletons with final fields | 
| 4 | Java native deserialization of untrusted input | Critical remote code execution vulnerability | Use JSON (Jackson) with strict typing |
| 5 | N+1 ORM queries | Exponential DB load | Always verify query count with `EXPLAIN` |
| 6 | Missing `@Transactional` on multi-step writes | Partial writes on failure; data corruption | Annotate all multi-step operations |
| 7 | Catching and rethrowing identical exception | Pointless noise; no value added | Only catch if you can meaningfully handle | 
| 8 | `java.util.Random` for security tokens | Predictable tokens; security vulnerability | Use `SecureRandom` | 
| 9 | Logging sensitive data in exception messages | PII/tokens in log files | Sanitize before logging | 
| 10 | Uncaught exception in `ScheduledExecutorService` | Task silently stops forever | Wrap in try-catch(Exception) | 
| 11 | Mutating shared collections from multiple threads | Race conditions, `ConcurrentModificationException` | Use `ConcurrentHashMap`, `CopyOnWriteArrayList` |
| 12 | String concatenation in log statements | Strings built even when log level is off | Use parameterized SLF4J logging (`{}` placeholders) |


