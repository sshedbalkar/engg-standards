# ESTD16 - Paths, Branches, and Unit Testing Strategy

| Field | Value |
|:----- |:----- |
| **Document ID** | ESTD16 |
| **Version** | 1.0 |
| **Status** | Active |
| **Last Updated** | 2026-03-29 |
| **Applies To** | All engineers — client, server, tools, automation |
| **Depends On** | *(none)* |
| **Approval** | Director of Engineering / Server Architect |

---

**📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

This document is intended as both a **learning reference** and an **active checklist**. Different roles should engage with it differently.

**If you are writing a new feature:**
Read sections 1 through 4 before writing a single line of production code. Map out the paths your function will take — happy path, sad paths, and edge cases — before you write the implementation. The act of drawing that decision tree will surface design problems earlier and cheaper than discovering them in code review.

**If you are writing tests for existing code:**
Go directly to section 5. Use the Coverage Execution Checklist in section 5.5 as a per-function checklist. Work through it in order — happy path first, guard clauses second, boundaries third. Do not jump to edge cases before the basics are covered.

**If you are reviewing a pull request:**
Use the path vocabulary in sections 2 and 3 to ask precise questions. "Is there a test for the sad path where `gameId` is null?" is more actionable than "have you written enough tests?". The checklist in section 5.5 is an appropriate PR review tool.

**If you are setting up or tuning CI/CD coverage gates:**
Section 5.2 defines the 80% threshold rationale and section 5.5 identifies what should be excluded from coverage measurement. Coverage gates that include generated code, DTOs, and framework boilerplate produce meaningless numbers — configure exclusions before interpreting any reported percentage.

**A note on the examples:** All code examples in this document are language-agnostic pseudocode. They illustrate concepts, not syntax. Apply the patterns to PHP, Java, C#, or TypeScript as appropriate for the component under test.

---

## Table of Contents

- [ESTD16 - Paths, Branches, and Unit Testing Strategy](#estd16---paths-branches-and-unit-testing-strategy)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. What is a Path?](#2-what-is-a-path)
  - [3. How to Identify Branches](#3-how-to-identify-branches)
    - [3.1 Practical technique: draw the decision tree](#31-practical-technique-draw-the-decision-tree)
  - [4. Path Types](#4-path-types)
    - [4.1 Happy Path](#41-happy-path)
    - [4.2 Sad Path (Error Path / Failure Path)](#42-sad-path-error-path--failure-path)
    - [4.3 Hot Path](#43-hot-path)
    - [4.4 Cold Path](#44-cold-path)
    - [4.5 Edge Case Path](#45-edge-case-path)
  - [5. Path Summary](#5-path-summary)
  - [6. Writing Unit Tests for 80% Line Coverage](#6-writing-unit-tests-for-80-line-coverage)
    - [6.1 Why 80%, not 100%?](#61-why-80-not-100)
    - [6.2 The Strategy: Coverage by Intent](#62-the-strategy-coverage-by-intent)
      - [Step 1 — Cover the happy path first](#step-1--cover-the-happy-path-first)
      - [Step 2 — Cover every guard clause (sad paths)](#step-2--cover-every-guard-clause-sad-paths)
      - [Step 3 — Cover boundary values (edge cases)](#step-3--cover-boundary-values-edge-cases)
      - [Step 4 — Cover exception handling blocks](#step-4--cover-exception-handling-blocks)
      - [Step 5 — Exclude from coverage deliberately](#step-5--exclude-from-coverage-deliberately)
    - [6.3 The Testing Pyramid](#63-the-testing-pyramid)
    - [6.4 Rules for Good Unit Tests](#64-rules-for-good-unit-tests)
    - [6.5 Coverage Execution Checklist](#65-coverage-execution-checklist)
    - [6.6 What 80% Coverage Does Not Guarantee](#66-what-80-coverage-does-not-guarantee)

---

## 1. Purpose and Scope

Software defects cluster in two places: logic that was never tested, and logic that was tested only under ideal conditions. Both problems share a common root cause — engineers write code without a clear mental model of all the paths that code can take, and then write tests only for the paths they can easily imagine.

This document establishes a shared vocabulary and a repeatable methodology for reasoning about code paths and writing unit tests that provide genuine confidence rather than a false sense of coverage.

**This document applies to:**

- All server-side logic written in PHP (legacy API), Java/SEAM (new game microservices), and TypeScript (internal tools)
- All client-side game logic written in Unity C# where unit testable in isolation
- Any engineer authoring new features, reviewing pull requests, or refactoring existing code
- Test coverage targets enforced in CI/CD pipelines across all four environments (dev → QA → staging → production)

**This document does not cover:**

- Integration testing strategies (covered separately)
- End-to-end and manual QA processes
- Load and performance testing of hot paths (covered in the performance standards)
- SmartFox real-time server testing, which has distinct constraints due to its stateful WebSocket architecture

---


## 2. What is a Path?

A **path** is any sequence of statements that executes from the entry point of a function to one of its exit points. Every function has at least one path. Most real functions have several — one for each combination of decisions the code can make.

```
function processPayment(amount, user):
    │
    ├── if amount <= 0          ← decision point → branch A (invalid amount)
    │
    ├── if user.isBlocked       ← decision point → branch B (blocked user)
    │
    ├── if balance < amount     ← decision point → branch C (insufficient funds)
    │
    └── charge(user, amount)    ← branch D (success)
```

Each branch above is a separate path through the function. A test suite that exercises all four paths covers 100% of the branches.

---

## 3. How to Identify Branches

A branch is created every time the code makes a **decision**. Look for these constructs:

| Construct | Creates How Many Branches |
|---|---|
| `if / else` | 2 (condition true, condition false) |
| `if` with no `else` | 2 (condition true, implicit fall-through) |
| `else if` chain | N+1 (one per condition + the final else) |
| `switch / match` | One per `case`, plus `default` |
| Ternary `a ? b : c` | 2 |
| `try / catch / finally` | 2+ (success path + each exception type) |
| Early `return` / `throw` | Creates a new exit path |
| Loop (`for`, `while`) | 2 (loop runs at least once, loop never runs) |
| Logical `&&` / `\|\|` (short-circuit) | 2 per operator |
| Null check `?.` | 2 (null, not null) |

### 3.1 Practical technique: draw the decision tree

Take any non-trivial function and trace each `if`, `return`, and `throw` as a fork in a tree. The number of leaves on that tree is the number of distinct paths.

```
processDraw(gameId, ballCount):
├── gameId is null?
│   └── YES → throw InvalidGameException         [Path 1]
│   └── NO  → continue
│       ├── game.status != ACTIVE?
│       │   └── YES → return error GAME_NOT_ACTIVE [Path 2]
│       │   └── NO  → continue
│       │       ├── ballCount > remaining balls?
│       │       │   └── YES → return error OVERDRAW [Path 3]
│       │       │   └── NO  → draw balls, persist, return success [Path 4]
```

Four leaves → four paths → four test cases at minimum.

---

## 4. Path Types

### 4.1 Happy Path

The **happy path** is the sequence of execution that occurs when everything goes right — valid input, no errors, no edge cases, all preconditions met. It is what the function was designed to do in ideal conditions.

```
// Happy path: valid user, sufficient balance, payment succeeds
processPayment(amount=50, user={id: "u1", blocked: false, balance: 200})
→ charge executes → returns SUCCESS
```

The happy path is always the first path tested. If the happy path does not work, nothing else matters.

---

### 4.2 Sad Path (Error Path / Failure Path)

The **sad path** (also called the error path or failure path) covers all the branches where something goes wrong — invalid input, preconditions not met, downstream service failures, business rule violations. Every `if` that guards against an invalid state is a potential sad path.

```
// Sad path examples for processPayment:
processPayment(amount=-10, ...)    → invalid amount error
processPayment(..., blocked user)  → user blocked error
processPayment(..., balance=10)    → insufficient funds error
```

Sad paths are where bugs hide. They are also where untested code lives in most codebases.

---

### 4.3 Hot Path

The **hot path** is not about correctness — it is about **performance**. It is the path of execution that runs most frequently, under the highest load, in production. Hot paths are identified through profiling and metrics, not by reading code alone.

In a Bingo game, the hot path might be:

```
Player submits BINGO claim
→ API receives claim
→ Cache lookup: is this game result cached?   ← hit 95% of the time
→ Validate card against draw result
→ Return win/lose response
```

This sequence executes potentially thousands of times per minute during peak hours. A 10ms inefficiency in a hot path can degrade the experience for every player simultaneously. A 10ms inefficiency in a cold path (e.g. account deletion) may never be noticed.

**How to identify hot paths:**
- p95/p98 latency dashboards — which endpoints show up?
- CloudWatch / APM traces — where is CPU time being spent?
- Request volume metrics — which routes receive the most traffic?
- Game telemetry — which in-game actions happen most frequently?

**Hot path rules:**
- ❌ No synchronous external calls (DB, network) inside a hot path without caching
- ❌ No unbounded loops or allocations
- ✅ Cache aggressively; serve from memory wherever possible
- ✅ Any change to a hot path requires a load test before production

---

### 4.4 Cold Path

The **cold path** is the opposite of the hot path — executed infrequently. Examples: account creation, password reset, end-of-season reward distribution, admin configuration changes. Correctness matters; raw performance is a secondary concern.

---

### 4.5 Edge Case Path

An **edge case** is a path triggered by inputs at the extreme boundary of valid ranges, or at the intersection of two unusual conditions simultaneously.

```
// Edge cases for a Bingo card validator:
- Card with all 24 numbers already marked (full house before any draw)
- Draw result contains duplicate ball numbers
- Player claims BINGO on the exact same millisecond the game ends
- Card ID exists but belongs to a different player
```

Edge cases are distinct from sad paths. A sad path is a predictable failure mode. An edge case is an unusual but valid (or nearly valid) input that reveals assumptions baked into the code.

---

## 5. Path Summary

```
                      ┌─────────────────┐
                      │   ENTRY POINT   │
                      └────────┬────────┘
                               │
              ┌────────────────┼───────────────┐
              │                │               │
     ┌────────▼───────┐ ┌──────▼──────┐ ┌──────▼──────┐
     │   HAPPY PATH   │ │  SAD PATHS  │ │  EDGE CASES │
     │                │ │             │ │             │
     │ Everything     │ │ Guards fail │ │ Boundary /  │
     │ works as       │ │ Errors      │ │ unusual     │
     │ designed       │ │ thrown      │ │ inputs      │
     └────────────────┘ └─────────────┘ └─────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  HOT PATH (subset)  │
                    │  The paths that run │
                    │  most in production │
                    └─────────────────────┘
```

The hot path is a **performance label** applied to whichever of the above paths runs most frequently. It can be the happy path, but it does not have to be.

---

## 6. Writing Unit Tests for 80% Line Coverage

### 6.1 Why 80%, not 100%?

100% line coverage is a vanity metric. It means every line executed at least once — it says nothing about whether the logic is correct. Chasing 100% produces tests that execute code without asserting meaningful outcomes, and it wastes engineering time on trivial getters, generated code, and framework boilerplate.

80% is the industry-standard threshold because it forces coverage of all meaningful paths while excluding the noise. The goal is **high-confidence coverage of meaningful logic**, not a number.

---

### 6.2 The Strategy: Coverage by Intent

Work through your test suite in this order. Each layer adds coverage naturally.

---

#### Step 1 — Cover the happy path first

One test per public method that exercises the primary success scenario end-to-end. Verify the return value and any critical side effects (state changes, events published, persistence calls made).

```
// processDraw() — happy path
GIVEN  a valid active game with 50 balls remaining
WHEN   processDraw(gameId, ballCount=5) is called
THEN   5 balls are drawn
AND    the game state is persisted
AND    the draw result is returned
```

---

#### Step 2 — Cover every guard clause (sad paths)

For every `if`, early `return`, or `throw` in the function, write one test that triggers that branch. These are your sad path tests.

```
// processDraw() — sad paths
Test 1: gameId is null           → expect InvalidGameException
Test 2: game.status = FINISHED   → expect GameNotActiveException
Test 3: ballCount > remaining    → expect OverdrawException
```

This step alone typically gets you to 60–70% line coverage, because guard clauses are the most common untested code.

---

#### Step 3 — Cover boundary values (edge cases)

For any numeric parameter, string input, or collection, test the boundaries:

```
boundary values for ballCount in processDraw():
- ballCount = 0            → what happens? error? no-op?
- ballCount = 1            → minimum valid draw
- ballCount = remaining    → draw exactly what's left (valid)
- ballCount = remaining+1  → one over the limit (invalid)
- ballCount = MAX_INT      → extreme overflow case
```

This is where the **boundary value analysis** technique applies: test `n-1`, `n`, and `n+1` at every meaningful boundary.

---

#### Step 4 — Cover exception handling blocks

`try/catch` blocks are consistently under-tested. If your function catches an exception from a downstream dependency and converts it to a domain exception, that conversion path needs a test.

```
GIVEN  the database throws a connection timeout
WHEN   processDraw() is called
THEN   a ServiceUnavailableException is thrown (not a raw SQLException)
AND    the error is logged with the game ID as context
```

---

#### Step 5 — Exclude from coverage deliberately

Identify the code that does not need unit tests and exclude it from the coverage report explicitly. This is not cheating — it is signal hygiene.

Exclude:
- Generated code (ORM models, protobuf, auto-generated mappers)
- Framework boilerplate (Spring `@Configuration` classes, DI setup)
- Trivial getters and setters with no logic
- `main()` entry points
- Data Transfer Objects (DTOs) with no behaviour
- Third-party adapters that are integration-tested separately

Every coverage tool supports exclusion annotations or config files. Use them. A coverage number that includes generated code is a meaningless number.

---

### 6.3 The Testing Pyramid

```
                    ┌───────────────┐
                    │  E2E / Manual │  ← Few, slow, catch user journey failures
                    │               │
               ┌────┴───────────────┴─────┐
               │   Integration Tests      │  ← DB, external APIs, queues
               │                          │
          ┌────┴──────────────────────────┴─────┐
          │           Unit Tests                │  ← Most tests live here
          │   Fast · Isolated · Deterministic   │
          └─────────────────────────────────────┘
```

Unit tests form the base — they are fast (milliseconds per test), run on every commit, and isolate a single unit of logic. They are not a substitute for integration tests, but they catch the majority of logic errors before code ever leaves a developer's machine.

---

### 6.4 Rules for Good Unit Tests

**Each test has one reason to fail.**
A test that asserts five unrelated things is five tests collapsed into one. When it fails, you do not know which of the five things broke.

**Tests are independent.**
No shared mutable state between tests. No test should depend on another test having run first. Test execution order must be irrelevant.

**Tests are deterministic.**
No random data, no `new Date()`, no network calls, no file system access. Mock all external dependencies. A test that fails intermittently is worse than no test — it trains the team to ignore failures.

**Tests assert behaviour, not implementation.**
Test what the function does, not how it does it internally. A test that breaks because you renamed a private method is testing the wrong thing.

**Use the Arrange / Act / Assert structure.**

```
// Arrange — set up the preconditions
game = createActiveGame(remainingBalls=10)
drawService = new DrawService(mockRepo, mockEventBus)

// Act — call the unit under test
result = drawService.processDraw(game.id, ballCount=3)

// Assert — verify the outcome
assertEquals(3, result.drawnBalls.size())
verify(mockRepo).saveDrawResult(any())
verify(mockEventBus).publish(instanceOf(DrawCompletedEvent.class))
```

**Name tests as sentences.**
`test_processDraw_whenBallCountExceedsRemaining_throwsOverdrawException` reads as a specification. `testProcessDraw2` tells you nothing.

---

### 6.5 Coverage Execution Checklist

```
For each function or class under test:

[ ] 1. Happy path test written and passing
[ ] 2. One test per guard clause / early return
[ ] 3. Boundary values tested for all numeric/collection inputs
[ ] 4. Exception handling paths tested
[ ] 5. Generated / boilerplate code excluded from coverage report
[ ] 6. All external dependencies mocked
[ ] 7. No test depends on another test
[ ] 8. Test names describe the scenario and expected outcome
[ ] 9. Coverage report reviewed — uncovered lines explained or excluded
[ ] 10. Tests run in CI on every pull request
```

---

### 6.6 What 80% Coverage Does Not Guarantee

80% line coverage is a floor, not a ceiling. Meeting it does not mean:

- The logic is correct (a test can execute a line without asserting the right outcome)
- The system behaves correctly under concurrency
- Integration points with real databases or queues work
- The user experience is correct

Coverage is one signal among many. Pair it with code review, integration tests, and production monitoring to build genuine confidence.
