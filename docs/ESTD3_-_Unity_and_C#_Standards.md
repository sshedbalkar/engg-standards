# ESTD3 - Unity and C# Standards for Engineers

**ESTD3 — Unity and C# Standards**

| Field | Value |
|:----- |:------|
| Document ID | ESTD3 |
| Version | 4.0 |
| Status | Active |
| Last Updated | 2026-04-07 |
| Applies To | All Unity/C# engineers on both Bingo games  |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD2](./ESTD2_-_General_Client_Engg_Standards.md#estd2---general-client-engineering-standards-for-bingo-games) |
| Approval | Director of Engineering |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD3 is the lowest-level client standard. It applies exclusively to code written in C# for the Unity engine. All rules from [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) and [ESTD2](./ESTD2_-_General_Client_Engg_Standards.md#estd2---general-client-engineering-standards-for-bingo-games) apply in full. [ESTD3](#estd3---unity-and-c-standards-for-engineers) narrows, extends, or adds to them for the Unity/C# context. Read [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) and [ESTD2](./ESTD2_-_General_Client_Engg_Standards.md#estd2---general-client-engineering-standards-for-bingo-games) first.

---

## Table of Contents

- [ESTD3 - Unity and C# Standards for Engineers](#estd3---unity-and-c-standards-for-engineers)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. C# Coding Style](#2-c-coding-style)
    - [2.1 Language Version](#21-language-version)
    - [2.2 Nullability](#22-nullability)
    - [2.3 var Usage](#23-var-usage)
    - [2.4 Expression-Bodied Members](#24-expression-bodied-members)
    - [2.5 Readonly and Const](#25-readonly-and-const)
  - [3. Naming Conventions (C#)](#3-naming-conventions-c)
  - [4. Class and File Organization](#4-class-and-file-organization)
    - [4.1 One Class per File](#41-one-class-per-file)
    - [4.2 File Name](#42-file-name)
    - [4.3 Internal Order Within a Class](#43-internal-order-within-a-class)
  - [5. Error Handling in Unity (C#)](#5-error-handling-in-unity-c)
    - [5.1 Top-Level Exception Handler in MonoBehaviours](#51-top-level-exception-handler-in-monobehaviours)
    - [5.2 Do Not Use Debug.Log for Error Logging](#52-do-not-use-debuglog-for-error-logging)
  - [6. MonoBehaviour Lifecycle Standards](#6-monobehaviour-lifecycle-standards)
    - [6.1 Lifecycle Method Usage Guide](#61-lifecycle-method-usage-guide)
    - [6.2 Awake vs Start](#62-awake-vs-start)
    - [6.3 Update Budget](#63-update-budget)
  - [7. Memory and Garbage Collection](#7-memory-and-garbage-collection)
    - [7.1 Avoid Allocations in Update, FixedUpdate, LateUpdate](#71-avoid-allocations-in-update-fixedupdate-lateupdate)
    - [7.2 Collections](#72-collections)
    - [7.3 Struct vs Class for Hot-Path Data](#73-struct-vs-class-for-hot-path-data)
  - [8. String Allocation in Hot Paths](#8-string-allocation-in-hot-paths)
    - [8.1 The Problem](#81-the-problem)
    - [8.2 Rule: No String Construction in Per-Frame Methods](#82-rule-no-string-construction-in-per-frame-methods)
    - [8.3 Conditional Compilation Strip](#83-conditional-compilation-strip)
    - [8.4 Reusable StringBuilder](#84-reusable-stringbuilder)
    - [8.5 Pre-cache int.ToString()](#85-pre-cache-inttostring)
  - [9. Object Pooling](#9-object-pooling)
    - [9.1 When to Use an Object Pool](#91-when-to-use-an-object-pool)
    - [9.2 Unity's Built-In Pool (Unity 2021+)](#92-unitys-built-in-pool-unity-2021)
    - [9.3 Pool Rules](#93-pool-rules)
  - [10. Coroutines and Async/Await](#10-coroutines-and-asyncawait)
    - [10.1 What Is a Coroutine?](#101-what-is-a-coroutine)
    - [10.2 What Is async/await with UniTask?](#102-what-is-asyncawait-with-unitask)
    - [10.3 When to Use Coroutines](#103-when-to-use-coroutines)
    - [10.4 When to Use async/await (UniTask)](#104-when-to-use-asyncawait-unitask)
    - [10.5 Coroutine Rules and Proper Usage](#105-coroutine-rules-and-proper-usage)
    - [10.6 Cancellation Token Usage](#106-cancellation-token-usage)
  - [11. Dependency Injection and Service Locator](#11-dependency-injection-and-service-locator)
    - [11.1 Avoid FindObjectOfType and GameObject.Find](#111-avoid-findobjectoftype-and-gameobjectfind)
    - [11.2 Prefer Explicit Injection](#112-prefer-explicit-injection)
    - [11.3 Service Locator (Acceptable Pattern)](#113-service-locator-acceptable-pattern)
  - [12. Unity Event System and C# Events](#12-unity-event-system-and-c-events)
    - [12.1 Always Unsubscribe](#121-always-unsubscribe)
    - [12.2 Null-Check Before Invoking C# Events](#122-null-check-before-invoking-c-events)
    - [12.3 Event Payload Objects Should Be Structs](#123-event-payload-objects-should-be-structs)
  - [13. LeanTween Usage Standards](#13-leantween-usage-standards)
    - [13.1 All Durations and Targets Must Be Named Constants](#131-all-durations-and-targets-must-be-named-constants)
    - [13.2 Cancelling Tweens](#132-cancelling-tweens)
    - [13.3 Cancel on Destroy](#133-cancel-on-destroy)
    - [13.4 Reduce Motion Support](#134-reduce-motion-support)
  - [14. ScriptableObjects for Configuration](#14-scriptableobjects-for-configuration)
  - [15. PlayerPrefs: Usage Guidelines](#15-playerprefs-usage-guidelines)
    - [15.1 What PlayerPrefs Is and How It Works](#151-what-playerprefs-is-and-how-it-works)
    - [15.2 When to Use PlayerPrefs](#152-when-to-use-playerprefs)
    - [15.3 When NOT to Use PlayerPrefs](#153-when-not-to-use-playerprefs)
    - [15.4 PlayerPrefs Key Naming Convention](#154-playerprefs-key-naming-convention)
    - [15.5 Clearing PlayerPrefs](#155-clearing-playerprefs)
    - [15.6 Technical Rules for PlayerPrefs Usage](#156-technical-rules-for-playerprefs-usage)
    - [15.7 Alternatives to PlayerPrefs](#157-alternatives-to-playerprefs)
  - [16. Memory Leak Prevention (Unity-Specific)](#16-memory-leak-prevention-unity-specific)
    - [16.1 Addressables Handle Lifecycle (Critical)](#161-addressables-handle-lifecycle-critical)
    - [16.2 Static Field Discipline](#162-static-field-discipline)
    - [16.3 Preventing Leaks from LeanTween](#163-preventing-leaks-from-leantween)
    - [16.4 Texture and Render Texture Discipline](#164-texture-and-render-texture-discipline)
    - [16.5 Unsubscribed C# events (the most common Unity memory leak)](#165-unsubscribed-c-events-the-most-common-unity-memory-leak)
    - [16.6 Memory Hygiene Checklist (per feature)](#166-memory-hygiene-checklist-per-feature)
  - [17. Runtime Performance (Unity-Specific)](#17-runtime-performance-unity-specific)
    - [17.1 Update() Budget Rules](#171-update-budget-rules)
    - [17.2 Avoid LINQ in Hot Paths](#172-avoid-linq-in-hot-paths)
    - [17.3 Canvas and UI Rebuild Optimisation](#173-canvas-and-ui-rebuild-optimisation)
  - [18. Battery Management (Unity-Specific)](#18-battery-management-unity-specific)
    - [18.1 Dynamic Frame Rate Management](#181-dynamic-frame-rate-management)
    - [18.2 Particle System Battery Guidelines](#182-particle-system-battery-guidelines)
    - [18.3 Screen Sleep Management](#183-screen-sleep-management)
  - [19. Editor and Inspector Hygiene](#19-editor-and-inspector-hygiene)
  - [20. Build and Compile Targets](#20-build-and-compile-targets)
    - [20.1 IL2CPP for All Production Builds](#201-il2cpp-for-all-production-builds)
    - [20.2 Preprocessor Symbols](#202-preprocessor-symbols)
  - [21. Serialization](#21-serialization)
  - [22. Testing in Unity](#22-testing-in-unity)
    - [22.1 Plain C# Classes for Logic](#221-plain-c-classes-for-logic)
    - [22.2 Test Runner](#222-test-runner)
    - [22.3 Target Coverage](#223-target-coverage)
  - [23. Common Pitfalls to Avoid](#23-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

**Why this document exists:** Unity C# has unique characteristics that general C# guidelines do not address: a frame-based execution model, a managed garbage collector that causes frame hitches, a threading model where most engine APIs are main-thread-only, and a rich set of engine-specific lifecycle methods that must be used correctly. This document captures the patterns and rules that keep Unity projects stable, performant, and maintainable over a multi-year live-service lifecycle.

This document governs the writing of C# code inside Unity projects for both Bingo games (legacy and new). It covers language style, engine-specific patterns, memory management, animation (LeanTween), and performance patterns specific to the Unity runtime.

---

## 2. C# Coding Style

### 2.1 Language Version

Target **C# 9.0 minimum** (supported by Unity 2021.2+). Use modern language features where they improve clarity. Do not use features not supported by the project's current Unity version without explicit Architect approval.

### 2.2 Nullability

Enable nullable reference types (`#nullable enable`) at the project level. Annotate all reference type members that can be null with `?`. Use the null-coalescing operator (`??`) and null-conditional operator (`?.`) rather than verbose null checks where the intent is clear. Never use the null-forgiving operator (`!`) to suppress a warning unless you have verified the value cannot be null — and add a comment explaining why.

### 2.3 var Usage

Use `var` when the type is immediately obvious from the right-hand side:

```c#
var player = new Player();            // GOOD — type obvious
var handle = Addressables.LoadAssetAsync<Texture2D>(key); // GOOD — type clear from generic
```

Do not use `var` when the type is not obvious:

```c#
var result = GetResult();             // BAD — what is result?
PlayerSearchResult result = GetResult(); // GOOD — explicit
```
Never use `var` for primitive types (`int`, `float`, `bool`, `string`).

### 2.4 Expression-Bodied Members

Use expression bodies for single-expression properties and methods only. Do not use them for methods that require error handling or multiple statements.

```c#
// GOOD — clear and single expression
public string DisplayName => $"{FirstName} {LastName}";

// BAD — expression body hides complexity
public int ComputeScore() => _base + CalculateBonus() * GetMultiplier() - GetPenalties();
```

### 2.5 Readonly and Const

- Use `const` for compile-time constants (values that will never change in any build). 
- Use `static readonly` for runtime constants (values computed once at startup).  
- Mark fields that are set only in the constructor as `readonly`.

---

## 3. Naming Conventions (C#)

| Symbol | Convention | Example |
|:-------|:-----------|:--------|
| Class / Struct / Enum / Interface | PascalCase | `BingoCardManager`, `IPlayerRepository` | 
| Public method | PascalCase | `AwardJackpot()` | 
| Private / protected method | PascalCase | `LoadPlayerData()` | 
| Public property | PascalCase | `PlayerId`, `IsConnected` | 
| Private field | `_camelCase` | `_ballCallQueue` | 
| Protected field | `_camelCase` |  `_baseScore` |
| Local variable | camelCase | `currentRoom`, `ballNumber` | 
| Parameter | camelCase | `playerId`, `rewardConfig` | 
| Constant | UPPER_SNAKE_CASE |  `BINGO_BALL_COUNT_MAX`, `RECONNECT_DELAY_MS` |  
| Interface | `I` prefix + PascalCase | `IBingoRoomService` | 
| Abstract class | `Base` suffix | `BaseRewardHandler` |
| Static utility class | PascalCase | `BallNumberFormatter` | 
| Unity event method | PascalCase (standard Unity names) | `Awake`, `Start`, `OnEnable`, `Update` |
| Coroutine method | PascalCase, `Coroutine` suffix | `LoadBundleCoroutine()` |

---

## 4. Class and File Organization

### 4.1 One Class per File

Each C# file must contain exactly one primary class (or struct, interface, or enum). Nested types are permitted only when the nested type is meaningless outside the parent class and is under 30 lines.

### 4.2 File Name

The file name must exactly match the class name: `BingoCardManager.cs` for `class BingoCardManager`.

### 4.3 Internal Order Within a Class

```c#
public class BingoRoomController : MonoBehaviour
{
    // 1. Constants
    private const int BALL_COUNT_MAX = 75;

    // 2. Serialized fields (Inspector-visible)
    [SerializeField] private BingoCardView _cardView;

    // 3. Private fields
    private BingoGameState _gameState;
    private IRewardService _rewardService;

    // 4. Public properties
    public int RoomId { get; private set; }

    // 5. Unity lifecycle methods (Awake, OnEnable, Start, Update, OnDisable, OnDestroy)
    private void Awake() { ... }
    private void OnEnable() { ... }
    private void OnDisable() { ... }
    private void OnDestroy() { ... }

    // 6. Public methods
    public void JoinRoom(int roomId) { ... }

    // 7. Private / protected methods
    private void BallDrawnHandle(int ballNumber) { ... }

    // 8. Event/callback handlers (clearly named with On prefix)
    private void OnRewardClaimed(RewardClaimedEvent evt) { ... }
}
```

---

## 5. Error Handling in Unity (C#)

### 5.1 Top-Level Exception Handler in MonoBehaviours

For methods called by Unity directly (e.g., event handlers, button callbacks), wrap the body in a try-catch to prevent one error from crashing the entire session:

```c#
// OnClickClaimButton is called by Unity's Button component — must not throw
public void OnClickClaimButton()
{
    RewardClaimAsync(this.destroyCancellationToken).Forget();
}

private async UniTaskVoid RewardClaimAsync(CancellationToken ct)
{
    try
    {
        await _rewardService.ClaimAsync(ct);
        StateSuccessShow();
    }
    catch (OperationCanceledException)
    {
        // Expected — component was destroyed while awaiting
    }
    catch (ApiException ex)
    {
        Logger.Error($"Reward claim failed: {ex.ErrorCode}", ex);
        StateErrorShow(ex.PlayerFacingMessage);
    }
    catch (Exception ex)
    {
        // Final safety net — log everything, show generic error
        Logger.Fatal("Unexpected exception in RewardClaimAsync", ex);
        StateErrorShow(LocalizationManager.Get("error.generic"));
    }
}
```

**Note 1: try-catch scope:** In the method above, the single `try` block wrapping the entire `async UniTask` body is correct and consistent with [ESTD1 §9.1 When to Use Try-Catch](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#91-when-to-use-try-catch). This is an entry-point boundary method — a Unity lifecycle callback or button handler. The typed catches below handle each condition specifically. This is the correct pattern.

In contrast, the service and domain layers called from this entry point must use individual per-statement try-catch blocks so that each failable operation is independently handled ([ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)).

**Note 2: Entry-point boundary:** The `async UniTaskVoid` handler pattern in [§5.1 Top-Level Exception Handler in MonoBehaviours](#51-top-level-exception-handler-in-monobehaviours) uses a single try block with multiple typed catch clauses. This is correct — Unity button callbacks and lifecycle-driven async methods are entry-point boundaries ([ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions)). Each catch handles one specific exception type. Code in service and domain classes called from this handler must use individual per-statement try-catch blocks ([ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)).

### 5.2 Do Not Use Debug.Log for Error Logging

`Debug.Log` is for development only. All production logging must go through the centralized `Logger` class which respects log levels and ships to Datadog. `Debug.Log` calls left in production code are a performance overhead and a dead end for incident response.

---

## 6. MonoBehaviour Lifecycle Standards

Unity calls lifecycle methods in a specific, documented order. Using the wrong method for a task (e.g., calling into another MonoBehaviour in `Awake` before that MonoBehaviour has initialized) leads to null references and initialization order bugs that are highly environment-dependent and hard to reproduce.

### 6.1 Lifecycle Method Usage Guide

| Use Case | Correct Method |
|:---------|:---------------|
| Initialize fields, get component references | `Awake` |
| Subscribe to events, start logic (after all Awake calls complete) | `OnEnable` / `Start` |
| One-time logic after all Awake calls are complete | `Start` |
| Per-frame logic | `Update` |
| Per-frame physics / Rigidbody | `FixedUpdate` |
| Per-frame UI / camera (runs after all Updates) | `LateUpdate` | 
| Unsubscribe from events | `OnDisable` |
| Release resources, unregister from managers | `OnDestroy` |

### 6.2 Awake vs Start

`Awake` must only contain initialization that does not depend on other GameObjects being initialized. `Start` must be used for initialization that requires other `Awake` calls to have completed. Do not perform network calls or heavy asset loading in either — defer to an explicit `Initialize(...)` method called by the owning system.

### 6.3 Update Budget

`Update` methods must do as little work as possible. Any operation that does not need to run every frame must use a timer, a coroutine, or an event. A common pattern for periodic checks:

```c#
private float _periodicCheckIntervalSec = 2.0f;
private float _checkTimeNext;

private void Update()
{
    if (Time.time < _checkTimeNext) return;
    _checkTimeNext = Time.time + _periodicCheckIntervalSec;
    PeriodicCheckExecute();  // Runs every 2 seconds, not every frame
}
```

---

## 7. Memory and Garbage Collection

Unity uses a generational garbage collector. When the GC runs, it pauses all managed threads — including the game loop. In a 60 FPS game, any GC pause over 16ms causes a visible frame drop. GC runs are triggered by heap pressure: the more short-lived objects you create, the more frequently GC runs. The patterns in this section eliminate the most common allocation sources in hot paths.

### 7.1 Avoid Allocations in Update, FixedUpdate, LateUpdate

The following operations allocate managed heap memory and must not appear in per-frame methods:

- String concatenation using `+` or `string.Format()`
- LINQ queries (`.Where()`, `.Select()`, `.ToList()`, etc.)  
- `new` calls for reference types  
- Boxing of value types (passing `int`/`float`/`bool` to an `object` parameter)  
- `params` method calls unless the argument list exactly matches a non-params overload  
- Lambda captures that allocate a closure object

### 7.2 Collections

Pre-allocate collections with a known or estimated capacity:

```c#
// BAD — allocates with default capacity (4), likely to resize
new List<int>()

// GOOD — pre-allocates for the known maximum
new List<int>(BINGO_BALL_COUNT_MAX) // 75 slots, never needs to resize
```

Reuse collection instances rather than creating new ones each frame. Use `Array` or `Span<T>` for fixed-size hot-path data instead of `List<T>`.

### 7.3 Struct vs Class for Hot-Path Data

Prefer `struct` for small, frequently-created, short-lived data packets (e.g., `BallDrawEvent`, `CardPosition`) to keep them on the stack and avoid heap pressure.

Rules for structs:

- Maximum 4 fields — larger structs are expensive to copy.  
- Must be immutable unless there is a documented performance reason.  
- Do not box structs (do not pass to `object` parameters or store in non-generic collections).

---

## 8. String Allocation in Hot Paths

See [ESTD1 §11.4 Sanitization vs. Validation — Knowing the Difference](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#114-sanitization-vs-validation--knowing-the-difference) for the general hot-path logging strategy. This section covers Unity-specific C# patterns.

### 8.1 The Problem

In C#, strings are immutable reference-type heap objects. Any operation that produces a new string allocates a new object on the managed heap. In a game running at 60 FPS, a log statement in `Update` that builds a string produces 3,600 short-lived string objects per minute — directly causing GC collection cycles.

### 8.2 Rule: No String Construction in Per-Frame Methods

```c#
// BAD — both allocate strings every frame
private void Update()
{
    Debug.Log("Player " + _playerId + " is at ball " + _ballCurrent);  // allocates
    Debug.Log($"Player {_playerId} is at ball {_ballCurrent}");         // also allocates
}
```

### 8.3 Conditional Compilation Strip

For per-frame DEBUG logging, strip the call entirely from release builds:

```c#
[System.Diagnostics.Conditional("DEVELOPMENT_BUILD")]
private void LogBallDrawDebug(int ball)
{
    // This entire method call is compiled out in non-development builds
    Logger.Debug($"Ball drawn: {ball}");
}

private void Update()
{
    // In release builds, LogBallDrawDebug() is a no-op with zero cost
    LogBallDrawDebug(_ballCurrent);
}
```

### 8.4 Reusable StringBuilder

When a multi-part debug log is truly needed on a hot path, use a reusable `StringBuilder` stored as a field:

```c#
private readonly StringBuilder _logBuilder = new StringBuilder(256);

private void RoomStateDebugLog()
{
    _logBuilder.Clear();
    _logBuilder.Append("Room ").Append(_roomId)
               .Append(" | Players: ").Append(_playerCount)
               .Append(" | Ball: ").Append(_ballCurrent);
    Logger.Debug(_logBuilder.ToString()); // One string allocation, not N
}
```

### 8.5 Pre-cache int.ToString()

`int.ToString()` allocates. If a value changes infrequently, pre-cache the string:

```c#
private int _ballDisplayed = -1;
private void BallCurrentSet(int ball)
{
    if (ball == _ballDisplayed) return;
    _ballDisplayed = ball;
    _ballLabel.text = ball.ToString(); // Allocates, but only when value changes
}
```

---

## 9. Object Pooling

Bingo games involve many frequently-created and destroyed objects — Bingo balls, number tiles, pop-up notifications, particle effects. Each Instantiate and Destroy call forces a GC cycle. Object pooling reuses these objects, eliminating both the GC pressure and the CPU cost of construction/destruction.

### 9.1 When to Use an Object Pool

Any prefab that is instantiated and destroyed more than a handful of times must use an object pool: Bingo balls, UI notifications, particle effect instances, reward pop-ups, SmartFox message wrapper objects.

### 9.2 Unity's Built-In Pool (Unity 2021+)

```c#
private ObjectPool<BingoBallView> _ballPool;

private void Awake()
{
    _ballPool = new ObjectPool<BingoBallView>(
        createFunc:      () => Instantiate(_ballPrefab, _poolParent),
        actionOnGet:     ball => ball.gameObject.SetActive(true),
        actionOnRelease: ball => {
            ball.gameObject.SetActive(false);
            ball.Reset();  // IMPORTANT: reset state before returning to pool
        },
        actionOnDestroy: ball => Destroy(ball.gameObject),
        collectionCheck: false,  // Disable in production for performance
        defaultCapacity: 75,
        maxSize:         100
    );
}

// When a ball is drawn — get from pool
BingoBallView drawnBall = _ballPool.Get();
drawnBall.Initialize(ballNumber, calledAt);

// When animation completes — return to pool
_ballPool.Release(drawnBall);  // NEVER call Destroy() on pooled objects
```

### 9.3 Pool Rules

- Always return pooled objects to the pool with `Release()` — never call `Destroy()` on them.  
- Objects retrieved from a pool **must be explicitly initialized** — never assume they are in a clean state.  
- Objects returned to a pool **must be explicitly reset** — call a `Reset()` method that restores all fields to their initial values.

---

## 10. Coroutines and Async/Await

This section is one of the most important in the entire standards suite for Unity development. Coroutines and async/await are both tools for writing non-blocking asynchronous code in Unity, but they have different strengths, different failure modes, and different suitability for different tasks. Choosing the wrong tool leads to uncancellable operations, swallowed exceptions, memory leaks, and race conditions.

### 10.1 What Is a Coroutine?

A **coroutine** is a Unity-specific mechanism for spreading work across multiple frames. It is a method that returns `IEnumerator` and uses `yield return` to pause execution until the next frame, a fixed time, or a condition.

```
Frame 1: Coroutine runs up to first yield return
Frame 2: Coroutine resumes, runs up to next yield return
...
```

Coroutines are driven by Unity's engine loop — they do not run on a separate thread. They are paused and resumed by Unity on the main thread.

### 10.2 What Is async/await with UniTask?

`async`/`await` is the C# language feature for expressing asynchronous operations that may involve I/O. UniTask is a zero-allocation async/await library for Unity that ensures all continuations resume on the Unity main thread by default (unlike `System.Threading.Tasks.Task`, which can resume on a thread pool thread and crash Unity API calls).

### 10.3 When to Use Coroutines

Use coroutines for:

- **Time-based sequences driven by the Unity frame loop** — fading a UI element over N seconds, waiting for an animation to complete, polling a condition that changes based on game state.  
- **Simple timed delays** (`yield return new WaitForSeconds(delay)`).  
- **Sequences that interact with Unity's physics or rendering** (waiting for `WaitForFixedUpdate`, `WaitForEndOfFrame`).

```c#
// GOOD USE of coroutine — time-based animation sequence
private IEnumerator BingoCardRevealCoroutine()
{
    foreach (var tile in _tiles)
    {
        tile.PlayRevealAnimation();
        yield return new WaitForSeconds(TILE_REVEAL_DELAY_SEC);
    }
    OnAllTilesRevealed();
}
```

### 10.4 When to Use async/await (UniTask)

Use `async UniTask` for:

- **I/O-bound operations** — API calls, file I/O, Addressables loading.  
- **Any operation that needs a return value** — coroutines cannot return values.  
- **Operations that need to be cancelled** — UniTask has first-class `CancellationToken` support.  
- **Operations that can fail with an exception** — exceptions in coroutines are silently swallowed; exceptions in `async UniTask` propagate normally.

```c#
// GOOD USE of async UniTask — network call with return value and cancellation
private async UniTask<RewardClaimResult> RewardClaimAsync(
    string rewardId, CancellationToken ct)
{
    try
    {
        var response = await _apiClient.PostAsync<RewardClaimResult>(
            "/api/v1/rewards/claim",
            new { rewardId },
            ct
        );
        return response;
    }
    catch (OperationCanceledException)
    {
        Logger.Debug($"RewardClaim cancelled for rewardId={rewardId}");
        throw;  // Let the cancellation propagate — do not swallow it
    }
    catch (ApiException ex)
    {
        Logger.Error($"RewardClaim failed. RewardId={rewardId}, Code={ex.ErrorCode}", ex);
        throw;
    }
}
```

### 10.5 Coroutine Rules and Proper Usage

**Rule 1: Never start a coroutine on an inactive or destroyed MonoBehaviour.**

```c#
// BAD — will silently fail if gameObject is inactive
StartCoroutine(LoadBundleCoroutine());

// GOOD — guard before starting
if (gameObject.activeInHierarchy)
{
    StartCoroutine(LoadBundleCoroutine());
}
```

**Rule 2: Store coroutine references when they need to be stopped explicitly.**

```c#
private Coroutine _reconnectionCoroutine;

private void ReconnectionStart()
{
    // Stop any existing reconnect attempt before starting a new one
    if (_reconnectionCoroutine != null)
    {
        StopCoroutine(_reconnectionCoroutine);
    }
    _reconnectionCoroutine = StartCoroutine(ReconnectionCoroutine());
}
```

**Rule 3: Coroutines that loop forever must have an explicit exit condition and must be stopped in** `OnDisable`.

```c#
private Coroutine _heartbeatCoroutine;
private bool _isRunning;

private void OnEnable()
{
    _isRunning = true;
    _heartbeatCoroutine = StartCoroutine(HeartbeatCoroutine());
}

private void OnDisable()
{
    _isRunning = false;  // Signal the loop to exit
    if (_heartbeatCoroutine != null)
    {
        StopCoroutine(_heartbeatCoroutine);
        _heartbeatCoroutine = null;
    }
}

private IEnumerator HeartbeatCoroutine()
{
    while (_isRunning)  // Explicit exit condition — never use while(true) without a break
    {
        HeartbeatSend();
        yield return new WaitForSeconds(HEARTBEAT_INTERVAL_SEC);
    }
}
```

**Rule 4: Do not use coroutines for exception-prone operations.** Exceptions thrown inside a coroutine are not propagated to the caller — they are either silently swallowed or terminate the coroutine without notification.

```c#
// BAD — exception from GetAsync() is silently swallowed
private IEnumerator LoadPlayerDataCoroutine()
{
    var request = UnityWebRequest.Get("/api/v1/player/me");
    yield return request.SendWebRequest();
    if (request.result != UnityWebRequest.Result.Success)
    {
        // This error path is easy to miss; there is no way to throw to the caller
    }
}

// GOOD — exception propagates normally; caller can catch and handle
private async UniTask<PlayerData> PlayerDataLoadAsync(CancellationToken ct)
{
    var response = await _apiClient.GetAsync<PlayerData>("/api/v1/player/me", ct);
    return response;  // ApiException propagates to caller automatically
}
```

### 10.6 Cancellation Token Usage

**Every async UniTask method must accept a** `CancellationToken` parameter. The token must be passed down the entire call chain.

```c#
// Tie the token to the MonoBehaviour's lifetime — automatically cancelled when destroyed
private async UniTaskVoid OnRoomJoinButtonTapped()
{
    // destroyCancellationToken is provided by Unity 2022+ and cancels when
    // this MonoBehaviour is destroyed — no manual CancellationTokenSource needed
    await RoomJoinAsync(selectedRoomId, this.destroyCancellationToken);
}

private async UniTask RoomJoinAsync(int roomId, CancellationToken ct)
{
    // Pass the token to every awaitable call
    await _sfxService.PlayJoinSoundAsync(ct);
    await _apiClient.PostAsync("/api/v1/rooms/join", new { roomId }, ct);
    await _sceneLoader.LoadRoomSceneAsync(roomId, ct);
}
```

For components that need more control (e.g., cancelling on `OnDisable` rather than `OnDestroy`):

```c#
private CancellationTokenSource _cts;

private void OnEnable()
{
    _cts = CancellationTokenSource.CreateLinkedTokenSource(
        this.destroyCancellationToken  // Also cancelled on Destroy
    );
    DataLoadAsync(_cts.Token).Forget();
}

private void OnDisable()
{
    _cts?.Cancel();
    _cts?.Dispose();
    _cts = null;
}
```

---

## 11. Dependency Injection and Service Locator

### 11.1 Avoid FindObjectOfType and GameObject.Find

These methods iterate all GameObjects and are expensive. They create hidden, fragile coupling. They are prohibited except in Editor utility scripts.

### 11.2 Prefer Explicit Injection

Wire dependencies through Inspector references (`[SerializeField]` for scene-level wiring) or constructor injection for plain C# classes.

### 11.3 Service Locator (Acceptable Pattern)

If a full DI container is not in use, a simple Service Locator is acceptable, provided it is populated during a single initialization phase (app bootstrap), not lazily during gameplay.

```c#
// Bootstrap (app startup) — registration
ServiceLocator.Register<IRewardService>(new RewardService());

// MonoBehaviour — resolution in Awake
private IRewardService _rewardService;
private void Awake()
{
    _rewardService = ServiceLocator.Resolve<IRewardService>();
}
```

---

## 12. Unity Event System and C# Events

### 12.1 Always Unsubscribe

This is the most important rule in this section. Every subscription must have a corresponding unsubscription.

```c#
// CORRECT pattern — symmetric subscribe/unsubscribe
private void OnEnable()
{
    _bingoGameService.BallDrawn        += OnBallDrawn;
    _bingoGameService.BingoWinDeclared += OnBingoWinDeclared;
}

private void OnDisable()
{
    // Mirror of OnEnable — every subscription has an unsubscription
    _bingoGameService.BallDrawn        -= OnBallDrawn;
    _bingoGameService.BingoWinDeclared -= OnBingoWinDeclared;
}

private void OnDestroy()
{
    // Belt-and-suspenders — also unsubscribe in OnDestroy
    _bingoGameService.BallDrawn        -= OnBallDrawn;
    _bingoGameService.BingoWinDeclared -= OnBingoWinDeclared;
}
```

Forgetting to unsubscribe is one of the most common causes of memory leaks in long Unity sessions. The listener object is kept alive by the publisher's event delegate, even after the scene has unloaded.

### 12.2 Null-Check Before Invoking C# Events

```c#
// GOOD — thread-safe null check and invoke
public event Action<int> BallDrawn;
private void NotifyBallDrawn(int ballNumber)
{
    BallDrawn?.Invoke(ballNumber);
}
```

### 12.3 Event Payload Objects Should Be Structs

```c#
// Struct event args — stack-allocated, no heap pressure
public readonly struct BallDrawnEventArgs
{
    public readonly int BallNumber;
    public readonly int GameSequenceId;
    public BallDrawnEventArgs(int ballNumber, int seq) { BallNumber = ballNumber; GameSequenceId = seq; }
}
```

---

## 13. LeanTween Usage Standards

LeanTween is the only permitted animation library. DoTween must not be introduced or used.

### 13.1 All Durations and Targets Must Be Named Constants

```c#
// BAD — magic literals throughout the codebase
LeanTween.alpha(panel, 0f, 0.25f);

// GOOD — named constants; easy to tune, search, and understand
private const float PANEL_FADE_DURATION_SEC  = 0.25f;
private const float PANEL_ALPHA_HIDDEN       = 0.0f;
LeanTween.alpha(panel, PANEL_ALPHA_HIDDEN, PANEL_FADE_DURATION_SEC);
```

### 13.2 Cancelling Tweens

Always cancel an object's tweens before starting a new one on the same object to prevent conflicting animations:

```c#
LeanTween.cancel(gameObject);  // Cancel all tweens on this object
LeanTween.scale(gameObject, Vector3.one * 1.2f, BOUNCE_DURATION_SEC).setEaseOutElastic();
```

### 13.3 Cancel on Destroy

```c#
private void OnDestroy()
{
    LeanTween.cancel(gameObject);  // Always cancel tweens on destroy to prevent callbacks firing
}
```

### 13.4 Reduce Motion Support

```c#
private void CardRevealAnimationPlay()
{
    if (AccessibilitySettings.IsReduceMotionEnabled)
    {
        // Skip animation entirely — jump to final state
        _cardContainer.localScale = Vector3.one;
        OnCardRevealComplete();
        return;
    }
    LeanTween.scale(_cardContainer.gameObject, Vector3.one, CARD_REVEAL_DURATION_SEC)
             .setEaseOutBack()
             .setOnComplete(OnCardRevealComplete);
}
```

---

## 14. ScriptableObjects for Configuration

Game configuration values that change between content resets (bonus amounts, room capacity, ball speeds, animation timings) should not be hardcoded in scripts. ScriptableObjects allow configuration to be changed without code changes, and they serialize to assets that can be version-controlled, swapped between environments, and live-patched via Addressables.

Use ScriptableObjects for:
- Room configuration (player capacity, ticket prices, pattern types)  
- Bonus amounts and cooldown periods  
- Animation timing constants  
- Audio configuration

```c#
[CreateAssetMenu(fileName = "BingoRoomConfig", menuName = "Bingo/Room Configuration")]
public class BingoRoomConfig : ScriptableObject
{
    [Header("Room Rules")]
    [Range(10, 500)]
    public int PlayerCountMax = 200;

    [Header("Game Timing")]
    public float BallCallIntervalSeconds = 4.0f;
    public float BingoClaimTimeoutSeconds = 10.0f;

    [Header("Economy")]
    public int TicketPrice = 100;
}
```

`ScriptableObject`s that change with content resets must be delivered via Addressables (remote assets), not bundled in the build.

---

## 15. PlayerPrefs: Usage Guidelines

`PlayerPrefs` is a Unity built-in key-value store that persists data between sessions. It is deceptively simple and widely misused. Storing the wrong data in PlayerPrefs leads to security vulnerabilities, data inconsistency, and data loss.

### 15.1 What PlayerPrefs Is and How It Works

PlayerPrefs stores data as key-value pairs on the device's local storage:

- **iOS:** `NSUserDefaults` (plist file in the app's data directory)  
- **Android:** `SharedPreferences` (XML file in the app's private data directory)  
- **WebGL:** Browser's `IndexedDB`

Data persists between app launches on the same device. It is not synced across devices, not encrypted, not backed up by default, and cleared when the app is uninstalled.

### 15.2 When to Use PlayerPrefs

`PlayerPrefs` is appropriate exclusively for **local, non-sensitive, device-specific user preferences** that affect only the local experience and carry no game-state consequence:

| Appropriate Use | Rationale | 
|:----------------|:----------|
| **UI preferences** (volume, notification settings, tutorial dismissed) | These are device-local, non-sensitive, and loss-tolerant |
| **Last-used display settings** (graphics quality, language override) | Device-specific; the player expects them to persist locally |
| **Analytics session identifier** | Persistent device ID that is not sensitive |
| **A/B test assignment** (non-sensitive) | Must remain stable between sessions on the same device |
| **Onboarding flow state** (which intro screens shown) | Loss-tolerant; worst case the player sees the intro again |

### 15.3 When NOT to Use PlayerPrefs

| Inappropriate Use | Why | Correct Alternative |
|:------------------|:----|:--------------------|
| **Session tokens / authentication credentials** | Not encrypted; readable on rooted/jailbroken devices | iOS Keychain / Android Keystore via `ISecureStorage` ([ESTD2 §12.2 Session Token Handling](./ESTD2_-_General_Client_Engg_Standards.md#122-session-token-handling)) | 
| **Coin balance, game progress, inventory** | Must be server-authoritative; local copy becomes source of exploits | Server API; local display-only cache | 
| **Feature flags** | Must be server-controlled at runtime | Remote config / CMS | 
| **Player account data** (username, email) | PII must not be in local unencrypted storage | Server-side only; retrieve on session start | 
| **Large data blobs** (> 1 KB) | `PlayerPrefs` is not designed for large data; causes performance issues on write | Local file + `Application.persistentDataPath` or Addressables | 
| **Any game-state that affects rewards or wins** | Can be manipulated on device | Server-authoritative state only | 
| **Any data that must survive a reinstall** | `PlayerPrefs` is cleared on app reinstall on most platforms | Server-side persistence |
| **Debug flags in production builds** | A debug flag inadvertently left in a PlayerPref becomes a cheat vector | Use `#if DEVELOPMENT_BUILD` compile guards |

### 15.4 PlayerPrefs Key Naming Convention

```c#
// Use a consistent prefix to namespace all PlayerPrefs keys
public static class PlayerPrefsKeys
{
    // Prefix: game initials + underscore
    public const string MusicVolume       = "BB_ui_music_volume";
    public const string SfxVolume         = "BB_ui_sfx_volume";
    public const string GraphicsQuality   = "BB_ui_graphics_quality";
    public const string TutorialDismissed = "BB_onboarding_tutorial_dismissed";
    public const string NotificationsOn   = "BB_prefs_notifications_enabled";
}
```

Never use inline string literals for PlayerPrefs keys. All keys must be constants in a central `PlayerPrefsKeys` class. This prevents typo-induced data loss and makes all uses globally searchable.

### 15.5 Clearing PlayerPrefs

`PlayerPrefs` must be cleared on logout and on account deletion. Never clear all `PlayerPrefs` on a version upgrade — use key versioning if the data format changes.

```c#
public void OnPlayerLogout()
{
    // Only clear authentication and session-related keys — not UI preferences
    // UI preferences are device-level and should survive a logout/login cycle
    // (Do not store auth data in PlayerPrefs at all — see §15.3)
    Logger.Info("[AuthService] Player logged out. No PlayerPrefs cleared (nothing sensitive stored).");
}

public void OnAccountDeleted()
{
    PlayerPrefs.DeleteAll();   // Full clear on account deletion is acceptable
    PlayerPrefs.Save();
    Logger.Info("[AuthService] Account deleted. All PlayerPrefs cleared.");
}
```

### 15.6 Technical Rules for PlayerPrefs Usage

**Rule 1: All PlayerPrefs keys must be named constants.** Bare string literals as PlayerPrefs keys lead to typos, key collisions, and impossible-to-search codebases.

```c#
// BAD
PlayerPrefs.SetFloat("master_volume", value);

// GOOD — key defined in one place, referenced everywhere
public static class PlayerPrefsKeys
{
    public const string AUDIO_VOLUME_MASTER = "settings.audio.master_volume";
    public const string MUSIC_MUTED         = "settings.audio.music_muted";
    public const string GRAPHICS_TIER       = "settings.graphics.quality_tier";
}

PlayerPrefs.SetFloat(PlayerPrefsKeys.AUDIO_VOLUME_MASTER, value);
```

**Rule 2: Access must be encapsulated in a service class.** No feature code may call `PlayerPrefs.Get*` or `PlayerPrefs.Set*` directly. All access goes through a `LocalSettingsService` or equivalent wrapper that provides typed accessors and centralizes key management.

```c#
public class LocalSettingsService
{
    public float AudioVolumeMaster
    {
        get => PlayerPrefs.GetFloat(PlayerPrefsKeys.AUDIO_VOLUME_MASTER, defaultValue: 1.0f);
        set
        {
            PlayerPrefs.SetFloat(PlayerPrefsKeys.AUDIO_VOLUME_MASTER, Mathf.Clamp01(value));
            PlayerPrefs.Save();  // Flush to disk
        }
    }

    public bool IsMusicMuted
    {
        get => PlayerPrefs.GetInt(PlayerPrefsKeys.MUSIC_MUTED, defaultValue: 0) == 1;
        set => PlayerPrefs.SetInt(PlayerPrefsKeys.MUSIC_MUTED, value ? 1 : 0);
    }
}
```

**Rule 3: Always call** `PlayerPrefs.Save()` explicitly after writing. Unity does not guarantee that `PlayerPrefs` changes are flushed to disk unless `Save()` is called. On iOS, unwritten changes may be lost if the app is force-quit.

**Rule 4: Always provide a sensible default in every** `GetX()` call. Never rely on the Unity default (0 for int/float, `""` for string).

**Rule 5: Do not write to** `PlayerPrefs` in `Update()`. `PlayerPrefs.Save()` involves disk I/O and may stall the frame. Writes must occur in response to explicit player actions (settings screen close, preferences change), not on every frame.

**Rule 6: Clear** `PlayerPrefs` on logout where appropriate. Preferences that should not persist across account switches (e.g., a last-used display name prefill) must be cleared when the player logs out.

### 15.7 Alternatives to PlayerPrefs

| Use Case | Recommended Alternative | 
|:---------|:------------------------|
| Large local data (> 4 KB) | `Application.persistentDataPath` with encrypted JSON | 
| Sensitive data (tokens, credentials) | iOS Keychain / Android Keystore | 
| Server-synchronized settings | Server API + local in-memory cache | 
| Debug/cheat flags in dev builds | `#if DEVELOPMENT_BUILD` conditional compilation |
| Cross-device settings sync | Server-persisted settings endpoint |

---

## 16. Memory Leak Prevention (Unity-Specific)

See [ESTD2 §17. Memory Leak Prevention](./ESTD2_-_General_Client_Engg_Standards.md#17-memory-leak-prevention) for the full client-side treatment. This section covers Unity-engine-specific patterns. Memory leaks in Unity cause gradual heap growth that ends in an OS-forced kill — a crash from the player's perspective.

### 16.1 Addressables Handle Lifecycle (Critical)

Every `AsyncOperationHandle` returned by `Addressables.LoadAssetAsync<T>()` or `Addressables.InstantiateAsync()` must be explicitly released. Unity does not release the underlying asset until the handle is released, even if the referencing component is destroyed.

```c#
public class RoomThemeLoader : MonoBehaviour
{
    // Track all loaded handles so they can be released on destroy
    private readonly List<AsyncOperationHandle> _loadedHandles = new List<AsyncOperationHandle>();

    private async UniTask ThemeLoadAsync(string themeKey, CancellationToken ct)
    {
        var handle = Addressables.LoadAssetAsync<Texture2D>(themeKey);
        _loadedHandles.Add(handle);               // Register before awaiting
        await handle.ToUniTask(cancellationToken: ct);

        if (handle.Status == AsyncOperationStatus.Succeeded)
            _roomBackground.texture = handle.Result;
    }

    private void OnDestroy()
    {
        // Release ALL loaded handles — this is the only way to unload the asset
        foreach (var handle in _loadedHandles)
        {
            if (handle.IsValid())
                Addressables.Release(handle);
        }
        _loadedHandles.Clear();
    }
}
```

### 16.2 Static Field Discipline

Static fields in Unity persist for the lifetime of the application — they are never garbage collected regardless of scene loads. A static field holding a reference to a `MonoBehaviour`, `GameObject`, or any managed object that contains references to Unity objects will prevent GC of that entire object graph.

```c#
// BAD — static field holds a scene-bound object alive across scene loads
public static BingoRoomController CurrentRoom; // Entire room object graph never GC'd

// GOOD — weak reference allows GC; null-check before use
private static WeakReference<BingoRoomController> _currentRoomRef;
public static BingoRoomController CurrentRoom
{
    get => _currentRoomRef != null && _currentRoomRef.TryGetTarget(out var r) ? r : null;
    set => _currentRoomRef = value != null ? new WeakReference<BingoRoomController>(value) : null;
}
```

### 16.3 Preventing Leaks from LeanTween

LeanTween retains callbacks internally. If a LeanTween tween is created with an `onComplete` callback that captures a `MonoBehaviour` reference and the tween is not cancelled before the `MonoBehaviour` is destroyed, the callback reference keeps the object alive.

```c#
private void OnDestroy()
{
    // Always cancel all tweens on this GameObject on destroy
    LeanTween.cancel(gameObject);
    // This removes all pending callbacks, preventing the leak
}
```

### 16.4 Texture and Render Texture Discipline

```c#
// Always release RenderTexture.GetTemporary() in a finally block
private RenderTexture FrameProcess(Texture2D source)
{
    RenderTexture temp = RenderTexture.GetTemporary(source.width, source.height);
    try
    {
        Graphics.Blit(source, temp, _processingMaterial);
        return temp; // Caller is responsible for RenderTexture.ReleaseTemporary(temp)
    }
    catch
    {
        RenderTexture.ReleaseTemporary(temp); // Release on error path too
        throw;
    }
}
```

### 16.5 Unsubscribed C# events (the most common Unity memory leak)

```c#
// CORRECT: symmetric subscribe/unsubscribe
private void OnEnable()
{
    _bingoGameService.BallDrawn        += OnBallDrawn;
    _bingoGameService.BingoWinDeclared += OnBingoWinDeclared;
}

private void OnDisable()  // Mirrors OnEnable exactly
{
    _bingoGameService.BallDrawn        -= OnBallDrawn;
    _bingoGameService.BingoWinDeclared -= OnBingoWinDeclared;
}
```

### 16.6 Memory Hygiene Checklist (per feature)

Before merging any feature that involves asset loading, event subscriptions, or new GameObjects:

- [ ] Every `OnEnable` subscription has a corresponding `OnDisable` unsubscription.  
- [ ] Every `Addressables.LoadAssetAsync` handle is released in `OnDestroy`.  
- [ ] No new static fields reference `MonoBehaviour` or `GameObject` instances.  
- [ ] Every dynamically created `RenderTexture` is destroyed when no longer needed.  
- [ ] Object pools have a maximum size cap.  
- [ ] A Memory Profiler snapshot was captured after 10 minutes of play on the feature.

---

## 17. Runtime Performance (Unity-Specific)

See [ESTD2 §18. Runtime Performance Optimisation](./ESTD2_-_General_Client_Engg_Standards.md#18-runtime-performance-optimisation) for the full client-side treatment. This section covers Unity-engine-specific performance patterns.

### 17.1 Update() Budget Rules

```c#
// RULE: Update() should do the minimum possible work.
// Everything that does not need per-frame execution must be moved out.

// BAD — expensive scene search every frame
private void Update()
{
    var rooms = FindObjectsOfType<RoomListItem>();  // O(n) scene search, every frame
}

// GOOD — cache on Awake, refresh only when data changes
private RoomListItem[] _roomListCached;
private void Awake()     { _roomListCached = FindObjectsOfType<RoomListItem>(); }
private void OnRoomsChanged() { _roomListCached = FindObjectsOfType<RoomListItem>(); }
```

### 17.2 Avoid LINQ in Hot Paths

LINQ allocates an enumerator on the heap on every call. In `Update()` or any SmartFox callback, this causes GC pressure.

```c#
// BAD — heap allocation on every Update call
private void Update()
{
    var activePlayers = _players.Where(p => p.IsActive).ToList();
}

// GOOD — pre-computed and cached; refreshed only on change
private List<Player> _playersActive = new List<Player>();
private void OnPlayerStatusChanged() { PlayerListActiveRefresh(); }
private void PlayerListActiveRefresh()
{
    _playersActive.Clear();
    foreach (var p in _players)
        if (p.IsActive) _playersActive.Add(p);
}
```

### 17.3 Canvas and UI Rebuild Optimisation

Unity's UI system rebuilds a Canvas whenever any element in it changes. Keep dynamic UI (updating text, animated elements) on a separate Canvas from static UI (background, layout frames). This limits rebuilds to only the dynamic Canvas.

```c#
// Structure canvases to limit rebuild scope:
// [Canvas: StaticBackground]   ← never marks dirty; never rebuilt
//   [Canvas: DynamicGameplay]  ← only this rebuilds when ball numbers update
//   [Canvas: DynamicHUD]       ← only this rebuilds when coin balance updates
```

---

## 18. Battery Management (Unity-Specific)

See [ESTD2 §19. Battery Management for Mobile](./ESTD2_-_General_Client_Engg_Standards.md#19-battery-management-for-mobile) for the full treatment. This section covers Unity-specific implementation.

### 18.1 Dynamic Frame Rate Management

```c#
public class FrameRateManager : MonoBehaviour
{
    private const int FPS_ACTIVE  = 60;
    private const int FPS_IDLE    = 30;
    private const int FPS_PAUSED  = 1;
    private const float TIMEOUT_IDLE_SEC = 5f;

    private float _inputTimeLast;

    private void Awake()
    {
        Application.targetFrameRate = FPS_ACTIVE;
        QualitySettings.vSyncCount  = 0;
    }

    private void Update()
    {
        if (Input.anyKey || Input.touchCount > 0)
            _inputTimeLast = Time.unscaledTime;

        bool isIdle = Time.unscaledTime - _inputTimeLast > TIMEOUT_IDLE_SEC;
        Application.targetFrameRate = isIdle ? FPS_IDLE : FPS_ACTIVE;
    }

    private void OnApplicationPause(bool paused)
    {
        Application.targetFrameRate = paused ? FPS_PAUSED : FPS_ACTIVE;
    }
}
```

### 18.2 Particle System Battery Guidelines

- Set a `Max Particles` limit on every particle system. Uncapped particle counts are the most common source of GPU-driven battery drain in the Bingo client.  
- Disable particle systems when they are off-screen or when the player has enabled "Reduce Motion" in device accessibility settings.  
- Use `ParticleSystem.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear)` — not `Destroy()` — to stop pooled particle effects.

### 18.3 Screen Sleep Management

```c#
// Keep screen awake only during active gameplay; allow sleep otherwise
public void GameplayActiveSet(bool active)
{
    Screen.sleepTimeout = active
        ? SleepTimeout.NeverSleep   // Active game — keep screen on
        : SleepTimeout.SystemSetting; // Idle — respect OS setting (saves battery)
}
```

---

## 19. Editor and Inspector Hygiene

- Use `[Header("Section Name")]` to organize `[SerializeField]` fields in the Inspector.  
- Use `[Tooltip("...")]` to document what each Inspector field does.  
- Do not make fields public just for Inspector visibility — use `[SerializeField] private`.  
- Use `[Range(min, max)]` for numeric fields that have defined bounds.  
- Editor-only code must be wrapped in `#if UNITY_EDITOR` guards.

---

## 20. Build and Compile Targets

### 20.1 IL2CPP for All Production Builds

All production builds must use the **IL2CPP scripting backend**. Mono is permitted for local development builds only (faster compile times).

| Config | Scripting Backend | Development Build | Logging Level | 
|:-------|:------------------|:------------------|:--------------|
| Debug (local) | Mono | Yes | DEBUG | 
| QA | IL2CPP | No | INFO | 
| Staging | IL2CPP | No | WARN | 
| Production | IL2CPP | No | ERROR |

Maintain a `link.xml` to prevent IL2CPP from stripping reflection-heavy code (SmartFox SDK, JSON deserializers).

### 20.2 Preprocessor Symbols

Define consistent preprocessor symbols per build configuration. Use them only for compile-time feature control, not for business logic:

```c#
#if DEVELOPMENT_BUILD
    Logger.SetMinLevel(LogLevel.Debug);
#else
    Logger.SetMinLevel(LogLevel.Error);
#endif
```

---

## 21. Serialization

- Use `[Serializable]` for data classes that need to be serialized by Unity.  
- Use `JsonUtility` for simple Unity-native JSON serialization. For complex serialization (polymorphism, custom converters), use `Newtonsoft.Json` (http://json.net/)
- Serialization classes must have default constructors.  
- Never serialize sensitive data (tokens, passwords) with Unity's built-in serialization — use encrypted storage.

---

## 22. Testing in Unity

Unit testing is mandatory ([ESTD1 §24. Testing Requirements](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#24-testing-requirements)). The challenge in Unity is that `MonoBehaviour` classes cannot be instantiated in a plain C# test environment — they require a running engine. The key architectural practice that makes testing possible is keeping game logic in plain C# classes that have no engine dependency, while keeping MonoBehaviours as thin shells.

### 22.1 Plain C# Classes for Logic

```c#
// HARD TO TEST — all logic in a MonoBehaviour, requires a running scene
public class BingoCardController : MonoBehaviour
{
    public bool CheckWin(WinPattern pattern)
    {
        // 50 lines of win-check logic embedded in a MonoBehaviour
    }
}

// EASY TO TEST — logic in a plain C# class, no Unity dependency
public class BingoWinChecker  // NOT a MonoBehaviour — testable anywhere
{
    public bool CheckWin(int[] daubedPositions, WinPattern pattern)
    {
        // Pure C# logic — runs in a unit test with zero engine setup
    }
}

public class BingoCardController : MonoBehaviour
{
    private readonly BingoWinChecker _winChecker = new BingoWinChecker();

    private void OnBallDaubed(int position)
    {
        if (_winChecker.CheckWin(_daubedPositions, _activePattern))
            OnBingoAchieved();
    }
}
```

### 22.2 Test Runner

Use **Unity Test Framework** (NUnit-based):

- **EditMode tests** — pure C# logic, no scene required. Fast. Target: all business logic classes.  
- **PlayMode tests** — integration tests requiring Unity runtime. Use sparingly.

### 22.3 Target Coverage

Minimum **80% line coverage** for all non-MonoBehaviour business logic. Priority test targets:

- `BingoWinChecker` — all patterns (horizontal, vertical, diagonal, four corners, full house, etc.)  
- State machine transition logic  
- Bonus calculation utilities  
- Content reset date/period calculations

---

## 23. Common Pitfalls to Avoid

| # | Pitfall | Consequence | Prevention | 
|:--|:--------|:------------|:-----------|
| 1 | Forgot to unsubscribe events in `OnDisable`/`OnDestroy` | Memory leak; ghost callbacks firing after scene unload | Symmetric subscribe/unsubscribe | 
| 2 | Starting coroutine on inactive GameObject | Silent failure; no error, no action | Guard with `activeInHierarchy` check | 
| 3 | Using raw `Task` instead of `UniTask` | Resumes on background thread; Unity API crash | Always use `UniTask` |  
| 4 | Exception inside a coroutine | Silently swallowed; coroutine stops without notification | Use `async UniTask` for failable operations | 
| 5 | No `CancellationToken` on async methods | Response arrives after screen destroyed; null reference | Pass `destroyCancellationToken` down the chain | 
| 6 | `FindObjectOfType<>()` in `Update` | Severe performance hit — searches all GameObjects every frame | Cache in `Awake`/`Start` | 
| 7 | String concatenation in `Update` | Allocates every frame; causes GC hitches | Strip with `Conditional` attribute or level-guard |
| 8 |  Destroying pooled objects | Pool is depleted; future requests allocate instead | Always `Release()`, never `Destroy()` |
| 9 | Not resetting pooled objects before returning | Next user gets stale state | Implement explicit `Reset()` | 
| 10 | Calling Unity API from SmartFox callback | Engine crash on background thread | Dispatch to main thread (see [ESTD2 §5. Concurrency, Shared Memory, and Thread Safety](./ESTD2_-_General_Client_Engg_Standards.md#5-concurrency-shared-memory-and-thread-safety)) | 
| 11 | DoTween usage | Prohibited; conflicts with LeanTween | Use LeanTween exclusively |
| 12 | `async void` outside Unity event handlers | Exceptions are silently lost | Use `async UniTaskVoid` or `async UniTask` | 
| 13 | Loading textures without releasing Addressables handles | Memory leak; handle keeps asset loaded | Release handles in `OnDestroy` |  
| 14 | Hardcoded timing values in animations | Hard to tune; inconsistent across the codebase | Named constants for all durations | 
| 15 | Storing auth tokens in PlayerPrefs | Security vulnerability — readable on rooted devices | Use iOS Keychain / Android Keystore |
| 16 | Storing game progress in PlayerPrefs | Server-bypass exploit vector | Server-authoritative state only | 
| 17 | No frame rate cap during idle state | Battery drain; negative reviews | Reduce to 30 FPS after 5s idle; 1 FPS when backgrounded | 
| 18 | Canvas has both static and dynamic elements | Entire canvas rebuilds on any change | Separate static and dynamic elements into different Canvases |

