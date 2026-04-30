# ESTD2 - General Client Engineering Standards for Bingo Games

**ESTD2 — General Client Engineering Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD2 |
| Version | 5.0 |
| Status | Active |
| Last Updated | 2026-04-12 |
| Applies To | All client engineers (Unity mobile, Unity web, Facebook) |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) |
| Approval | Director of Engineering / Client Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

[ESTD2](#estd2---general-client-engineering-standards-for-bingo-games) applies to all client-side engineering work across both Bingo games. It builds directly on [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) and adds client-specific concerns. Read [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) first. All rules in [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) apply in full; ESTD2 narrows, extends, or specializes those rules for the client context.

[ESTD3](./ESTD3_-_Unity_and_C%23_Standards.md#estd3---unity-and-c-standards-for-engineers) (Unity and C# Standards) builds on top of this document and provides language-and-engine-specific rules.

---

## Table of Contents

- [ESTD2 - General Client Engineering Standards for Bingo Games](#estd2---general-client-engineering-standards-for-bingo-games)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Client Architecture Principles](#2-client-architecture-principles)
    - [2.1 Separation of Concerns](#21-separation-of-concerns)
    - [2.2 Event-Driven Communication](#22-event-driven-communication)
    - [2.3 Single Source of Truth](#23-single-source-of-truth)
    - [2.4 No Business Logic on the Client](#24-no-business-logic-on-the-client)
  - [3. State Management](#3-state-management)
    - [3.1 Explicit State Machines](#31-explicit-state-machines)
    - [3.2 State Transitions](#32-state-transitions)
    - [3.3 Server-Authoritative State](#33-server-authoritative-state)
  - [4. Network Communication and Asynchronous Operations](#4-network-communication-and-asynchronous-operations)
    - [4.1 Two Communication Channels](#41-two-communication-channels)
    - [4.2 Centralized API Service Layer](#42-centralized-api-service-layer)
    - [4.3 The Lifecycle of an Asynchronous Operation](#43-the-lifecycle-of-an-asynchronous-operation)
    - [4.4 Request Cancellation](#44-request-cancellation)
    - [4.5 Request Timeouts](#45-request-timeouts)
    - [4.6 Request Deduplication](#46-request-deduplication)
    - [4.7 Optimistic UI](#47-optimistic-ui)
    - [4.8 SmartFox Real-Time Messages](#48-smartfox-real-time-messages)
    - [4.9 Reconnection](#49-reconnection)
  - [5. Concurrency, Shared Memory, and Thread Safety](#5-concurrency-shared-memory-and-thread-safety)
    - [5.1 What Is Shared Memory?](#51-what-is-shared-memory)
    - [5.2 What Is a Critical Section?](#52-what-is-a-critical-section)
    - [5.3 Unity's Threading Model and Why It Matters](#53-unitys-threading-model-and-why-it-matters)
    - [5.4 The Main Thread Dispatcher Pattern](#54-the-main-thread-dispatcher-pattern)
    - [5.5 Useful Strategies for Thread Safety](#55-useful-strategies-for-thread-safety)
    - [5.6 Thread Safety Guidelines](#56-thread-safety-guidelines)
    - [5.7 Good Practices](#57-good-practices)
  - [6. Worker Threads: Management and Graceful Shutdown](#6-worker-threads-management-and-graceful-shutdown)
    - [6.1 When to Use Worker Threads](#61-when-to-use-worker-threads)
    - [6.2 The Lifecycle of a Managed Worker Thread](#62-the-lifecycle-of-a-managed-worker-thread)
    - [6.3 CancellationToken-Based Worker Pattern](#63-cancellationtoken-based-worker-pattern)
    - [6.4 Graceful Shutdown Strategies](#64-graceful-shutdown-strategies)
    - [6.5 Rules for Worker Threads](#65-rules-for-worker-threads)
  - [7. Asset Management](#7-asset-management)
    - [7.1 Addressables / Remote Assets](#71-addressables--remote-assets)
    - [7.2 Asynchronous Asset Loading](#72-asynchronous-asset-loading)
    - [7.3 Memory Budgets](#73-memory-budgets)
  - [8. UI Standards](#8-ui-standards)
    - [8.1 Design System Compliance](#81-design-system-compliance)
    - [8.2 Loading, Success, and Error States](#82-loading-success-and-error-states)
    - [8.3 Safe Areas](#83-safe-areas)
    - [8.4 Responsive Layouts](#84-responsive-layouts)
    - [8.5 UI Animations](#85-ui-animations)
    - [8.6 Modal vs Non-modal UI](#86-modal-vs-non-modal-ui)
  - [9. Minimum UI Standards for All User Interfaces](#9-minimum-ui-standards-for-all-user-interfaces)
    - [9.1 Roles and Role-Based Access](#91-roles-and-role-based-access)
    - [9.2 Ease of Use and Task Completion](#92-ease-of-use-and-task-completion)
    - [9.3 Destructive, Sensitive, and High-Impact Actions](#93-destructive-sensitive-and-high-impact-actions)
    - [9.4 Preventing Unintended Changes](#94-preventing-unintended-changes)
    - [9.5 Change Tracking and Audit Trail](#95-change-tracking-and-audit-trail)
    - [9.6 Security Enforcement in the UI](#96-security-enforcement-in-the-ui)
    - [9.7 Performance and Usability Baselines](#97-performance-and-usability-baselines)
    - [9.8 Accessibility](#98-accessibility)
    - [9.9 UI Consistency](#99-ui-consistency)
  - [10. Audio Standards](#10-audio-standards)
  - [11. Localisation and Text Handling](#11-localisation-and-text-handling)
  - [12. Client-Side Security](#12-client-side-security)
    - [12.1 Certificate Pinning](#121-certificate-pinning)
    - [12.2 Session Token Handling](#122-session-token-handling)
    - [12.3 Anti-Cheat Awareness](#123-anti-cheat-awareness)
    - [12.4 Build Security](#124-build-security)
    - [12.5 Client-Side Security Vulnerabilities (Unity iOS / Android / Web / Facebook)](#125-client-side-security-vulnerabilities-unity-ios--android--web--facebook)
  - [13. Platform Considerations](#13-platform-considerations)
    - [13.1 iOS](#131-ios)
    - [13.2 Android](#132-android)
    - [13.3 Facebook / WebGL](#133-facebook--webgl)
    - [13.4 Cross-Platform Code Isolation](#134-cross-platform-code-isolation)
  - [14. Telemetry and Analytics Events](#14-telemetry-and-analytics-events)
  - [15. Crash Reporting and Monitoring](#15-crash-reporting-and-monitoring)
  - [16. Client Performance Standards](#16-client-performance-standards)
  - [17. Memory Leak Prevention](#17-memory-leak-prevention)
    - [17.1 The Most Common Leak Patterns in Unity Clients](#171-the-most-common-leak-patterns-in-unity-clients)
    - [17.2 Detecting Memory Leaks](#172-detecting-memory-leaks)
    - [17.3 Memory Hygiene Rules](#173-memory-hygiene-rules)
  - [18. Runtime Performance Optimisation](#18-runtime-performance-optimisation)
    - [18.1 CPU Optimisation](#181-cpu-optimisation)
    - [18.2 Rendering Optimisation](#182-rendering-optimisation)
    - [18.3 Memory/GC Optimisation](#183-memorygc-optimisation)
    - [18.4 Network Payload and Asset Load Optimisation](#184-network-payload-and-asset-load-optimisation)
    - [18.5 Performance Profiling Requirement](#185-performance-profiling-requirement)
  - [19. Battery Management for Mobile](#19-battery-management-for-mobile)
    - [19.1 Frame Rate Capping](#191-frame-rate-capping)
    - [19.2 Reduce Wake-Ups from Network Activity](#192-reduce-wake-ups-from-network-activity)
    - [19.3 Reduce CPU and GPU Activity When Idle](#193-reduce-cpu-and-gpu-activity-when-idle)
    - [19.4 Rendering-Related Battery Savings](#194-rendering-related-battery-savings)
    - [19.5 iOS-Specific Battery Optimizations](#195-ios-specific-battery-optimizations)
    - [19.6 Android-Specific Battery Optimizations](#196-android-specific-battery-optimizations)
    - [19.7 Network-Related Battery Savings](#197-network-related-battery-savings)
    - [19.8 Thermal Throttling Awareness](#198-thermal-throttling-awareness)
    - [19.9 Battery Testing Requirements](#199-battery-testing-requirements)
  - [20. Offline and Network-Degraded Behavior](#20-offline-and-network-degraded-behavior)
  - [21. Accessibility](#21-accessibility)
  - [22. Common Pitfalls to Avoid](#22-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

This standard governs the design and implementation of all client-side code for the Bingo games. The clients run on iOS, Android, Facebook (desktop web via Unity WebGL), and standalone web. The primary engine is Unity (C#), covered in detail in [ESTD3](./ESTD3_-_Unity_and_C%23_Standards.md#estd3---unity-and-c-standards-for-engineers). Platform targets include low-end Android devices and mid-range iPhones, making performance, memory, and network efficiency first-class concerns.

---

## 2. Client Architecture Principles

Without architectural boundaries, a live-service client codebase tends to accumulate business logic in UI classes, network code mixed with game rules, and tightly coupled components that cannot be changed independently. This makes every feature release riskier than the last. Clear layering ensures that changes to one concern cannot accidentally break another.

### 2.1 Separation of Concerns

Client code must be organized into clearly separated layers. Mixing presentation, game logic, and network concerns in a single class is the fastest path to a codebase that cannot be changed safely.

```
┌──────────────────────────────────────────────────────────────┐
│  View Layer  (MonoBehaviours, UI, Animations)                │  Displays data; reacts to events
├──────────────────────────────────────────────────────────────┤
│  Presentation Layer  (Presenter/Mediator/ViewModel)          │  No Unity engine dependency
├──────────────────────────────────────────────────────────────┤
│  Domain / Game Layer  (Rules, State Machines)                │  Testable without Unity
├──────────────────────────────────────────────────────────────┤
│  Service Layer  (API calls, SmartFox messages)               │  Transmits data; returns results
├──────────────────────────────────────────────────────────────┤
│  Data Layer  (DTOs, Model classes)                           │  Pure data structures
└──────────────────────────────────────────────────────────────┘
```

View Layer classes must not contain game logic. Service Layer classes must not contain game logic. Domain Layer classes must not call Unity APIs directly and must be testable without a running Unity instance.

### 2.2 Event-Driven Communication

Prefer an event-driven (observer/signal) model for decoupling components. Direct references between unrelated systems create hidden coupling that breaks when either system changes.

`BingoGameSystem` must not hold a reference to `LeaderboardPanel`. Instead, `BingoGameSystem` dispatches a `BingoGameEndedEvent`, and `LeaderboardPanel` subscribes to it. All event subscriptions must be explicitly unsubscribed on component destruction to prevent memory leaks.

### 2.3 Single Source of Truth

The game state must live in exactly one place. Two components that independently track player currency will inevitably become inconsistent. Define the authoritative owner of each piece of state and have other components read from it or subscribe to its changes.

### 2.4 No Business Logic on the Client

The client is untrusted territory. Business rules — especially rules with monetary or competitive consequences (jackpot eligibility, reward calculation, win validation, currency spending) — must be enforced on the server. The client may display the outcome; it must not decide the outcome.

---

## 3. State Management

Implicit state managed through scattered boolean flags is one of the most common sources of hard-to-reproduce bugs. When a player is simultaneously `_isSearching`, `!_isInRoom`, and `!_isJoining`, what is the actual state? Explicit state machines make valid states, invalid states, and transitions all visible and testable.

### 3.1 Explicit State Machines

Any game flow with more than two states must be managed by an explicit state machine.

```c#
// BAD — implicit state via scattered flags
private bool _isSearching;
private bool _isJoining;
private bool _isInRoom;
// Impossible to know which combination of flags is valid

// GOOD — explicit state machine
public enum LobbyState { Idle, Searching, Joining, InRoom, Error }
private LobbyState _state = LobbyState.Idle;
```

### 3.2 State Transitions

Document all valid state transitions. Log transitions at DEBUG level (or INFO for key player-facing transitions). Guard against invalid transitions: a transition that should not happen from the current state must log a WARN and take no action, or — if it indicates a desync — request a state sync from the server.

```
Lobby State Machine:
  Idle ──────→ Searching ──→ Joining ──→ InRoom
   ↑                │           │           │
   └────────────────┴────<──────┴─── Error ─┘
```

### 3.3 Server-Authoritative State
For any game state held server-side (room state, player currency, Bingo card), the server's state is the truth. The client's local state is a cache that can become stale. Periodically refresh critical state from the server. On reconnect, always request a full state sync before resuming local state.

---

## 4. Network Communication and Asynchronous Operations

All network communication on the client is inherently asynchronous — the result arrives at an unknown point in the future. Without clear patterns for managing asynchronous operations, it is easy to introduce race conditions (response arrives after the UI screen is destroyed), double-submissions (player taps a button twice), and silent failures (error response not handled). This section defines the mandatory patterns for handling async operations safely.

### 4.1 Two Communication Channels

The Bingo client uses two distinct channels with specific purposes:

| Channel | Technology | Use For |
|:--------|:-----------|:--------|
| **REST API (HTTP)** | PHP API / Java microservices | Auth, player profile, purchases, rewards, non-real-time actions |
| **Live Server** | SmartFox TCP | Real-time game events: room join/leave, number calls, daubs, win announcements |

Never use the REST API for real-time game events. Never use SmartFox for non-real-time operations like store purchases.

### 4.2 Centralized API Service Layer

All HTTP calls must be made through a centralized API service layer. Scattered `HttpClient` / `UnityWebRequest` calls throughout the codebase are not acceptable.

```c#
// BAD — HTTP concerns scattered in feature code
var request = UnityWebRequest.PostWwwForm("https://api.bingo.com/v1/bonus/weekly", form);
request.SetRequestHeader("Authorization", "Bearer " + _sessionToken);
yield return request.SendWebRequest();

// GOOD — feature code uses the service layer only
var result = await _bonusService.ClaimWeeklyBonusAsync(_cancellationToken);
```

### 4.3 The Lifecycle of an Asynchronous Operation

Every asynchronous operation that is visible to the player has three mandatory states. Omitting any of these is an incomplete implementation.

```
┌───────────────────────────────────────────────────────────────┐
│  User taps "Claim Bonus"                                      │
│         │                                                     │
│         ▼                                                     │
│  ┌─────────────┐   Request         ┌──────────────────┐       │
│  │  LOADING    │──────────────────→│  Server / API    │       │
│  │  (spinner)  │                   │                  │       │
│  │  [disabled  │                   └──────────────────┘       │
│  │   button]   │                          │                   │
│  └─────────────┘                  ┌───────┴────────┐          │
│                                   │                │          │
│                                Success          Failure       │
│                                   │                │          │
│                                   ▼                ▼          │
│                           ┌─────────────┐  ┌────────────────┐ │
│                           │  SUCCESS    │  │  ERROR STATE   │ │
│                           │  (updated   │  │  (message +    │ │
│                           │   balance)  │  │   retry button)│ │
│                           └─────────────┘  └────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

### 4.4 Request Cancellation

All asynchronous calls must be cancellable. This prevents responses from arriving after the relevant UI screen has been destroyed, which causes null reference exceptions and phantom state mutations.

Every async method must accept a `CancellationToken`. The token must be cancelled when the screen or component is destroyed.

```c#
public class BonusPanel : MonoBehaviour
{
    private CancellationTokenSource _cts;

    private void OnEnable()
    {
        _cts = new CancellationTokenSource();
    }

    private void OnDisable()
    {
        _cts?.Cancel();   // Cancel all in-flight requests when this panel is hidden
        _cts?.Dispose();
    }

    private async UniTaskVoid OnClaimButtonTapped()
    {
        _claimButton.interactable = false;   // Prevent double-submission
        _spinnerLoading.SetActive(true);

        try
        {
            var result = await _bonusService.ClaimWeeklyBonusAsync(_cts.Token);
            _coinDisplay.UpdateBalance(result.NewBalance);
            ShowSuccessState();
        }
        catch (OperationCanceledException)
        {
            // Panel was destroyed — do nothing (this is expected)
        }
        catch (ApiException ex) when (ex.Code == "BONUS_ALREADY_CLAIMED")
        {
            ShowAlreadyClaimedState();
        }
        catch (ApiException ex)
        {
            ShowErrorState(ex.PlayerFacingMessage, allowRetry: true);
        }
        finally
        {
            _claimButton.interactable = true;
            _spinnerLoading.SetActive(false);
        }
    }
}
```

### 4.5 Request Timeouts

All requests must have explicit timeouts. No request should wait indefinitely.

| Request Type | Timeout |
|:-------------|:--------|
| Read (profile, inventory) | 10 seconds |
| Write (purchase, claim bonus) | 15 seconds |
| Room join / matchmaking | 20 seconds |
| Initial app startup data | 30 seconds |

### 4.6 Request Deduplication

UI interactions that trigger network requests must be protected against double-submission. Disable the triggering button or control when a request is in-flight (see example in [§4.4 Request Cancellation](#44-request-cancellation) above).

### 4.7 Optimistic UI

Optimistic UI updates the display immediately before the server confirms, then rolls back if the server rejects the action. This makes the interface feel responsive on slow mobile connections.

Rules for using optimistic UI:

- Only apply for actions that are highly likely to succeed (daubing a number, basic navigation).  
- Always have a rollback path for server rejection.  
- Never apply optimistically to purchases, bonus claims, or any irreversible economic action.  
- Clearly communicate any rollback to the player.

```c#
// Optimistic daub example
private async UniTaskVoid OnDaubTapped(int ballNumber)
{
    // 1. Optimistically daub immediately — fast, feels responsive
    _bingoCard.DaubNumber(ballNumber);
    _bingoCard.SetDaubing(ballNumber, pending: true);  // Show as "pending"

    try
    {
        var result = await _gameService.SubmitDaubAsync(ballNumber, _cts.Token);

        if (result.IsValid)
        {
            _bingoCard.SetDaubing(ballNumber, pending: false);  // Confirm
        }
        else
        {
            // Server rejected — roll back
            _bingoCard.UndoDaub(ballNumber);
            ShowToast("Daub could not be applied. Please try again.");
        }
    }
    catch (OperationCanceledException) { }
    catch (ApiException)
    {
        _bingoCard.UndoDaub(ballNumber);   // Roll back on error too
        ShowToast("Connection issue. Please try again.");
    }
}
```

### 4.8 SmartFox Real-Time Messages

All SmartFox event handlers must be registered and deregistered in clearly defined lifecycle methods. No game logic may be placed directly inside a SmartFox event callback; the callback must extract data and delegate to a domain-layer method. Server messages that affect game state must be queued and processed on the Unity main thread — direct SmartFox callback execution on a background thread followed by Unity API calls in the same callback is a race condition.

### 4.9 Reconnection

The client must implement a reconnect flow for SmartFox disconnections:

1. Detect the disconnect event.  
2. Display a non-blocking "Reconnecting…" indicator (do not show an error modal on the first attempt).  
3. Attempt reconnection with exponential backoff: 1s, 2s, 4s, max 30s.  
4. After a configurable number of failed attempts, show the player an error with a manual retry option.  
5. On successful reconnection, request a full game state sync from the live server before resuming.

The reconnect attempt count and backoff parameters must be server-configurable (remote config or CMS), not hardcoded.

---

## 5. Concurrency, Shared Memory, and Thread Safety

Unity is primarily a single-threaded engine — almost all Unity API calls must occur on the main thread. SmartFox callbacks, however, arrive on background threads. When background-thread code directly accesses Unity objects or shared game state without synchronization, the result is crashes, data corruption, or subtle race conditions that are nearly impossible to reproduce consistently. Understanding concurrency is essential for any engineer working on client network code.

### 5.1 What Is Shared Memory?

**Shared memory** is any piece of data that is accessible by more than one thread simultaneously. In the Unity client, this situation arises specifically because SmartFox delivers network events on its own background thread.

```
Unity Main Thread:
  Update() → reads _roomState, writes _playerCoins
  OnDisable() → clears _pendingMessages list

SmartFox Network Thread:
  OnRoomJoin callback → writes _roomState
  OnBallDrawn callback → writes _currentBall
  OnPlayerLeft callback → modifies _pendingMessages list  ← DANGER: concurrent write
```

When both threads can write to the same variable without coordination, the result is a **race condition**: the final state of the variable depends on which thread runs first, which is non-deterministic.

### 5.2 What Is a Critical Section?

A **critical section** is a region of code that accesses shared memory and must not be executed by more than one thread at the same time. If two threads enter a critical section simultaneously, the shared data will be corrupted.

### 5.3 Unity's Threading Model and Why It Matters

Unity enforces a strict rule: almost all Unity APIs (including `Transform`, `GameObject`, `MonoBehaviour`, and UI components) can only be called from the main thread. Calling them from a background thread will throw an exception or — worse — silently corrupt state.

SmartFox delivers events on a background thread. This means SmartFox callbacks cannot directly:

- Call `Destroy()`, `Instantiate()`, or any `MonoBehaviour` method.  
- Update UI text (`_label.text = ...`).  
- Read or write `_gameState` or other shared fields without synchronization.

### 5.4 The Main Thread Dispatcher Pattern

The standard solution is a **main thread dispatcher**: a queue that background threads can safely write to, and that the main thread drains in `Update()`.

```c#
/// <summary>
/// Thread-safe queue for dispatching actions to the Unity main thread.
/// SmartFox callbacks enqueue actions here; Update() drains and executes them.
/// </summary>
public class MainThreadDispatcher : MonoBehaviour
{
    private static readonly ConcurrentQueue<Action> _queue = new ConcurrentQueue<Action>();

    // Called from SmartFox background thread — thread-safe
    public static void Enqueue(Action action)
    {
        _queue.Enqueue(action);
    }

    // Runs on the Unity main thread — safe to call Unity APIs here
    private void Update()
    {
        while (_queue.TryDequeue(out var action))
        {
            action?.Invoke();
        }
    }
}

// Usage in SmartFox callback (background thread):
private void OnBallDrawn(BaseEvent evt)
{
    int ballNumber = (int)evt.Params["ball"];

    // SAFE: enqueue the Unity work; the main thread will execute it
    MainThreadDispatcher.Enqueue(() =>
    {
        _bingoCard.MarkBallDrawn(ballNumber);   // Now runs on main thread
        _ballDisplay.ShowBall(ballNumber);       // UI update — safe
    });
}
```

### 5.5 Useful Strategies for Thread Safety

**Strategy 1: Main Thread Dispatcher (recommended for SmartFox callbacks)** All Unity work triggered by network events must be dispatched to the main thread as shown above. This is the primary pattern for SmartFox integration.

**Strategy 2: Immutable Message Objects** Parse SmartFox parameters into immutable data objects on the background thread, then pass the immutable object to the main thread via the dispatcher. The immutable object can be safely read by either thread without locking.

```c#
// Immutable record (C# 9+) — safe to pass across threads
public record BallDrawnMessage(int BallNumber, int GameSequenceId, DateTime CalledAt);

private void OnBallDrawn(BaseEvent evt)
{
    // Parse on background thread — no Unity calls, no shared state mutation
    var message = new BallDrawnMessage(
        BallNumber:     (int)evt.Params["ball"],
        GameSequenceId: (int)evt.Params["seq"],
        CalledAt:       DateTime.UtcNow
    );

    // Dispatch the immutable message to the main thread
    MainThreadDispatcher.Enqueue(() => ProcessBallDrawn(message));
}
```

**Strategy 3:** `ConcurrentQueue<T>` for Incoming Messages If messages can arrive faster than the main thread can process them, use `ConcurrentQueue<T>` as the buffer. `ConcurrentQueue` is a thread-safe queue from `System.Collections.Concurrent` that allows multiple background threads to enqueue safely while the main thread dequeues.

```c#
private readonly ConcurrentQueue<BallDrawnMessage> _ballsPending = new ConcurrentQueue<BallDrawnMessage>();

// On SmartFox background thread — thread-safe
private void OnBallDrawn(BaseEvent evt)
{
    _ballsPending.Enqueue(new BallDrawnMessage((int)evt.Params["ball"]));
}

// On Unity main thread — drain the queue
private void Update()
{
    while (_ballsPending.TryDequeue(out var msg))
    {
        _bingoCard.MarkBallDrawn(msg.BallNumber);
    }
}
```

**Strategy 4:** `volatile` for Simple Flags For a single boolean flag that one thread writes and another reads, `volatile` prevents the compiler and CPU from caching the value in a register, ensuring each read goes to main memory. However, `volatile` does not make compound operations atomic — it is only suitable for single reads and writes.

```c#
// volatile is sufficient for a simple boolean flag
private volatile bool _connectionActive;

// SmartFox thread writes:
private void OnConnect(BaseEvent evt)  { _connectionActive = true; }

// Main thread reads:
private void Update()
{
    if (!_connectionActive) ShowReconnectingOverlay();
}
```

### 5.6 Thread Safety Guidelines

- **Never call Unity API methods from a SmartFox callback.** Always dispatch to the main thread.  
- **Never mutate a shared collection (List, Dictionary) from multiple threads.** Use `ConcurrentQueue`, `ConcurrentDictionary`, or lock the collection.  
- **Prefer immutable data transfer objects (records, structs)** for passing data between threads. An object that cannot be modified cannot be corrupted by a race condition.  
- **Keep locks as short as possible.** If you use `lock()` in C#, hold the lock only for the critical section — never while performing I/O or awaiting anything.  
- **Use** `UniTask` on the main thread for async operations. `UniTask` always resumes on the Unity main thread by default, which is the correct behavior for Unity work.

### 5.7 Good Practices

- Keep the `MainThreadDispatcher` as a single, persistent GameObject in the Bootstrap scene.  
- Test concurrent scenarios by simulating rapid disconnect/reconnect sequences and high-frequency message delivery.  
- Review any code that has both a SmartFox callback AND a Unity API call — it is almost certainly missing a dispatch to the main thread.

---

## 6. Worker Threads: Management and Graceful Shutdown

The Unity client occasionally needs to perform CPU-intensive or I/O-intensive work off the main thread to avoid blocking the frame loop. Unmanaged background threads are dangerous: they can outlive their owning objects, access destroyed state, and prevent the application from shutting down cleanly. This section defines how to safely create, manage, and shut down worker threads in the Unity client.

### 6.1 When to Use Worker Threads

Use a worker thread (background `Task` or `Thread`) on the Unity client when:

- A CPU-intensive operation (e.g., compressing analytics event batches, computing complex card patterns) would visibly block the main thread for more than one frame (~16ms at 60 FPS).  
- An I/O operation (local file read/write, log flushing) cannot be made asynchronous via `UniTask`.

Do **not** use background threads for:

- Network requests — use `UniTask`\-wrapped HTTP calls instead.  
- Asset loading — use Unity Addressables' async API.  
- Anything that requires calling Unity APIs — these must always stay on the main thread.

### 6.2 The Lifecycle of a Managed Worker Thread
 
``` 
 Owner component created
         |
         v
 CancellationTokenSource created
         |
         v
 Worker started (Task.Run / new Thread)
         |
         v
 Worker loops, checking CancellationToken on every iteration
         |
   +-----+-----------------------------+
  Work done                     Token cancelled
   |                                   |
   v                                   v
 Worker exits naturally         Worker exits cleanly,
                                flushes any pending state
         |                                   |
         +-------------------+---------------+
                             |
                    Owner component destroyed
```

### 6.3 CancellationToken-Based Worker Pattern

```c#
public class AnalyticsWorker : MonoBehaviour
{
    private CancellationTokenSource _workerCts;
    private Task _workerTask;
    private readonly ConcurrentQueue<AnalyticsEvent> _eventsPending = new();

    private void OnEnable()
    {
        _workerCts  = new CancellationTokenSource();
        _workerTask = Task.Run(() => RunWorker(_workerCts.Token), _workerCts.Token);
    }

    private void OnDisable() => _workerCts?.Cancel();

    private async void OnDestroy()
    {
        _workerCts?.Cancel();
        if (_workerTask != null)
        {
            try   { await _workerTask.WaitAsync(TimeSpan.FromSeconds(3)); }
            catch (TimeoutException) { Logger.Warn("[AnalyticsWorker] Shutdown timeout."); }
            catch (OperationCanceledException) { }
        }
        _workerCts?.Dispose();
    }

    public void Enqueue(AnalyticsEvent evt) => _eventsPending.Enqueue(evt);

    // Runs on background thread — MUST NOT call any Unity API
    private async Task RunWorker(CancellationToken ct)
    {
        Logger.Info("[AnalyticsWorker] Worker started.");
        try
        {
            while (!ct.IsCancellationRequested)
            {
                await ProcessBatchAsync(ct);
                await Task.Delay(5000, ct);
            }
        }
        catch (OperationCanceledException)
        {
            Logger.Info("[AnalyticsWorker] Cancelled — flushing remaining events.");
            await FlushRemainingAsync();
        }
        catch (Exception ex) { Logger.Error("[AnalyticsWorker] Unexpected error.", ex); }
        Logger.Info("[AnalyticsWorker] Worker exited.");
    }

    private async Task ProcessBatchAsync(CancellationToken ct)
    {
        var batch = new List<AnalyticsEvent>();
        while (_eventsPending.TryDequeue(out var e) && batch.Count < 20) batch.Add(e);
        if (batch.Count > 0) await LocalStorage.WriteBatchAsync(batch, ct);
    }

    private async Task FlushRemainingAsync()
    {
        var remaining = new List<AnalyticsEvent>();
        while (_eventsPending.TryDequeue(out var e)) remaining.Add(e);
        if (remaining.Count > 0) await LocalStorage.WriteBatchAsync(remaining, CancellationToken.None);
    }
}
```

### 6.4 Graceful Shutdown Strategies

| Strategy | When to Use |
|:---------|:------------|
| **CancellationToken** | All long-running workers — signal stop in `OnDisable()` |
| **Flush-then-exit** | Queue-draining workers (analytics, logs) — drain queue after cancellation |
| **Time-bounded wait** | `await task.WaitAsync(TimeSpan.FromSeconds(3))` — never hang on shutdown |
| **App pause/resume** | `OnApplicationPause(true)` cancels; `OnApplicationPause(false)` restarts |

### 6.5 Rules for Worker Threads

- Every worker must have an associated `CancellationToken`. A worker with no cancellation mechanism is not acceptable.  
- Workers must **never** call Unity API methods directly. If the worker needs to communicate results to Unity, enqueue the result to the `MainThreadDispatcher` (see [§5.4 The Main Thread Dispatcher Pattern](#54-the-main-thread-dispatcher-pattern)).  
- Workers must have a timeout-bounded shutdown path. The application must not hang on exit because a worker is stuck.  
- Workers must log their start and exit at INFO level for diagnostics.  
- Worker exceptions must be caught and logged. A crashed worker must not propagate an unhandled exception that could crash the application.  
- The number of active worker threads must be bounded. Do not create a new thread for every unit of work — use a thread pool or a single persistent worker per concern.

---

## 7. Asset Management

Asset management directly affects app size, download times (critical for mobile players on cellular), loading stalls, and memory pressure on low-end devices. Poor asset management is one of the primary causes of crashes on older Android devices.

### 7.1 Addressables / Remote Assets

- Initial build should contain: core UI, core gameplay, placeholder assets.  
- Large or content-updated assets (textures, audio, bundles) must not be bundled with the build. Use Unity Addressables with remote hosting on S3 via CloudFront.  
- Assets that change with periodic content resets must be designed for hot-swapping without a full app update.  
- Asset bundles must be versioned. The client must check the manifest at startup and download only changed bundles.  
- Never rely on URL caching alone — always validate asset integrity via hash check.

### 7.2 Asynchronous Asset Loading

Asset loading must be asynchronous. Synchronous asset loads on the main thread are prohibited in production code and will cause ANRs (Application Not Responding) on Android.

```c#
// BAD — synchronous load on main thread; blocks the frame
var texture = Resources.Load<Texture2D>("RoomTheme/SpringMeadow");

// GOOD — asynchronous Addressables load; frame is unblocked
private async UniTask<Texture2D> LoadRoomThemeAsync(string key, CancellationToken ct)
{
    var handle = Addressables.LoadAssetAsync<Texture2D>(key);
    await handle.ToUniTask(cancellationToken: ct);

    if (handle.Status != AsyncOperationStatus.Succeeded)
    {
        Logger.Error($"Failed to load room theme asset: {key}");
        return _roomThemeDefault;  // Graceful fallback to default
    }

    return handle.Result;
}
```

### 7.3 Memory Budgets

| Platform | Target Heap Budget | Texture Budget |
|:---------|:-------------------|:---------------|
| Low-end Android | 512 MB | 256 MB |
| Mid-range Android | 768 MB | 384 MB |
| iOS (iPhone 11+) | 1024 MB | 512 MB |
| WebGL | 512 MB (browser limit) | 256 MB |

Profile builds against these budgets before each release. Report any exceedance as a blocking issue for that release.

---

## 8. UI Standards

### 8.1 Design System Compliance

All UI must be built using the shared design system (component library). Ad-hoc one-off UI implementations for layout, color, typography, and spacing are not acceptable.

### 8.2 Loading, Success, and Error States

Every asynchronous operation visible to the player must have all three states: a loading state (visual indicator that work is in progress), a success state (normal content view), and an error state (clear, user-friendly message with a retry action where applicable). Omitting any of these is an incomplete implementation.

### 8.3 Safe Areas

UI anchoring must respect platform safe areas on all supported device form factors (notched iOS devices, punch-hole Android cameras, iPad multitasking). Use `Screen.safeArea` to anchor HUD elements.

### 8.4 Responsive Layouts

All UI must work across the supported screen sizes and aspect ratios. Do not hardcode pixel positions. Test all UI on: `4:3`, `16:9`, `18:9`, and `19.5:9` aspect ratios.

### 8.5 UI Animations

All animations must use `LeanTween`. DoTween must not be used. Animation durations and easing parameters must be named constants, not magic literals. All animations must be interruptible: if the player navigates away mid-animation, the animation must be cancelled cleanly without leaving UI in an inconsistent state. Animations must respect the system Reduce Motion accessibility setting (see [§21. Accessibility](#21-accessibility).

```c#
// BAD — magic literal
LeanTween.scale(gameObject, Vector3.one, 0.35f);

// GOOD — named constant
private const float CARD_REVEAL_DURATION_SEC = 0.35f;
LeanTween.scale(gameObject, Vector3.one, CARD_REVEAL_DURATION_SEC);
```

### 8.6 Modal vs Non-modal UI

**Modal** — Blocks interaction with the rest of the UI until the user responds. It demands immediate attention and traps focus.

Examples: confirmation dialogs, alerts, login popups

**Non-Modal** — Allows the user to continue interacting with the rest of the UI while it is visible. It is informational and non-blocking.

Examples: tooltips, notification toasts, sidebars

**Key difference**: Modal interrupts the workflow; non-modal coexists with it.

---

## 9. Minimum UI Standards for All User Interfaces

These standards apply to every user-facing interface built by the team — including the game client, internal tools, web dashboards, operator consoles, and any other UI surface. They define the baseline that all UIs must meet regardless of technology stack. Platform-specific implementation details are covered in the relevant child documents: [ESTD3](./ESTD3_-_Unity_and_C%23_Standards.md#estd3---unity-and-c-standards-for-engineers) for Unity, [ESTD11](./ESTD11_-_Web_Development_and_Deployment_Standards.md#estd11---web-tools-creation-and-deployment-standards) for web tools.

### 9.1 Roles and Role-Based Access

Every UI that exposes write operations or sensitive data must enforce role-based access control (RBAC). Users must only see and interact with features appropriate to their assigned role. RBAC must be enforced on both the frontend (hide or disable unauthorized controls) and the backend (reject unauthorized requests). The backend is authoritative — frontend enforcement is a usability convenience, not a security boundary.

### 9.2 Ease of Use and Task Completion

UIs must be designed so that a user can complete a task without needing to consult documentation or ask a colleague. Labels must be self-explanatory. Inputs must show expected format, type, and valid ranges — either as placeholder text, helper text, or inline validation. Where a field expects domain-specific input, the UI must explain what that input means in context.

Example inline guidance for a hypothetical coin-adjustment field:

```
Coin adjustment amount: integer from 1 to 10,000. Example: 500.
```

Example bulk-action summary:

```
You are about to credit 500 coins to 23 players in cohort Spring_Test_A. Review the list before continuing.
```

### 9.3 Destructive, Sensitive, and High-Impact Actions

Any action that is destructive, irreversible, or capable of affecting a large number of players or records must require a multi-step confirmation flow. The confirmation must restate the action in plain language, show the exact scope of impact, and make it difficult to proceed accidentally. This applies to actions such as player bans, manual coin adjustments, content resets, room closures, feature flag changes, data deletions, and large-scale reward or economy modifications.

A recommended confirmation flow is:

```
1. User initiates the action.
2. UI shows an impact summary, including affected entities or player count.
3. User must explicitly confirm the action, including typing a confirmation phrase for high-risk cases.
4. User must provide a reason, either free-text, a reason code, or both.
5. The action is submitted with actor identity, role, reason, and timestamp.
6. An audit log entry is created.
```

Never allow bulk destructive actions without explicit scope limits. For actions affecting player economic data — including coin balances, purchase history, reward claims, or equivalent economy-sensitive values — a reason is mandatory before execution. Where the action is reversible, the UI should provide an undo option with a reasonable time window. Where the action is not reversible, the UI must make that fact explicit.

### 9.4 Preventing Unintended Changes

The UI must reduce the chance of accidental edits or unsafe publication.

- **Default to read mode.** Data should open in a read-only state; users must explicitly enter edit mode.
- **Read-only and edit states must be visually distinct.** Use a banner, lock icon, disabled-field styling, or equivalent visual treatment.
- **Draft and preview before publish.** UIs that configure content, events, promotions, or feature flags must offer a preview of the configured state before save or activation.
- **Field-level change confirmation.** Before submission, changed fields should be highlighted with clear before/after values.
- **Optimistic locking.** The UI must show when a record was last modified and prevent a user from silently overwriting a newer version without acknowledgement.
- **Required reason field.** All write operations should capture a reason and associate it with the resulting change record.

Example before/after review pattern:

| Field | Before | After |
|:------|:-------|:------|
| Weekly bonus amount | 100 | 150 |
| Feature flag status | Off | On |
| Event end date | 2026-03-24 18:00 UTC | 2026-03-25 18:00 UTC |

This review step is especially important when the user is editing live content or player-affecting data.

### 9.5 Change Tracking and Audit Trail

Every write operation performed through a UI must be recorded in an immutable, append-only audit log. At a minimum, each entry must include actor identity, actor role, action performed, entity affected, previous value, new value, reason where applicable, timestamp in UTC, and IP address. Where available, the log should also include the tool name and tool version.

Example audit log payload:

```json
{
  "actor": "psr_john.doe@company.com",
  "role": "player_service_rep",
  "action": "manual_coin_adjustment",
  "target": { "playerId": 98765, "before": 5000, "after": 5500 },
  "reason": "Support ticket #TKT-8871 - player reported missing login bonus",
  "timestamp": "2026-03-20T08:42:11Z",
  "ip": "10.10.5.23",
  "tool": "player-management-dashboard",
  "toolVersion": "2026.03.1"
}
```

Audit logs must meet all of the following requirements:

- They must be accessible to Administrators and Managers through the UI.
- The UI must support filtering by user, date range, and action type.
- Entries must never be deletable through the UI, even by administrators.
- Logs must be retained for a minimum of 12 months.
- Logs must be exportable for compliance or incident review on request.
- Actions such as role changes and explicit reveals of masked PII must also be logged.

### 9.6 Security Enforcement in the UI

Security controls must be visible and enforced consistently across the frontend and backend.

- **Session timeout:** Sessions must expire after a reasonable inactivity period. The user must be prompted to re-authenticate. Unsaved form state should be preserved where technically feasible.
- **Re-authentication for sensitive actions:** Admin-level actions and bulk-destructive actions must require credential re-entry even if the user already has an active session.
- **Sensitive data masking:** PII fields such as email address, date of birth, and payment-method details must be masked by default. Any explicit reveal action must itself be logged.
- **Input validation in forms:** All inputs must be validated client-side for immediate feedback and server-side for security. Server-side validation is authoritative.
- **CSRF protection:** All mutating API calls from frontends must include CSRF protection.
- **No PII in URLs:** Player identifiers, email addresses, and other sensitive values must not appear in query parameters because URLs are commonly stored in browser history, analytics, and server logs.

### 9.7 Performance and Usability Baselines

All UIs must remain usable under production conditions and during peak operational periods.

| Requirement | Standard |
|:------------|:---------|
| Initial content display | Display within 2 seconds under normal load |
| Search results | Display within 1 second for indexed queries |
| Loading feedback | Spinner, skeleton, or equivalent visible within 100ms of async action |
| Bulk operations | Any operation taking more than 2 seconds must show progress and must not block the UI |
| Pagination | Required for lists that can exceed 50 items; default maximum 100 rows per page |
| Error states | Human-readable, actionable, and free of stack traces |
| Empty states | Explain why no data is shown and suggest what to do next when applicable |
| Keyboard navigation | Core workflows must be completable by keyboard |

UIs must remain functional at production data volumes. Reporting dashboards must not become unusable during peak play hours, and operational tasks must not rely on excessively large unpaginated tables or long blocking requests.

### 9.8 Accessibility

UIs are not exempt from accessibility standards. Users may work long shifts under time pressure; accessible design reduces fatigue, increases speed, and lowers the risk of operational error.

Apply WCAG 2.1 AA standards to all interfaces. At a minimum, this means that workflows must support keyboard navigation, clear focus states, sufficient color contrast, semantic labeling, and status communication that does not rely on color alone.

### 9.9 UI Consistency

All UIs within the same product or tool suite must use a shared design system and component library where one exists. Inconsistent terminology, layout, or button placement across screens increases error rates and slows training.

Specifically:

- Use the domain glossary ([ESTD1 §4.1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#41-domain-glossary)) for labels, headings, statuses, and action names.
- Primary actions must use the standard primary treatment and be placed consistently.
- Destructive actions must use the standard destructive treatment, remain visually distinct from primary actions, and always require confirmation.
- Status indicators must use a shared badge color system consistently and must not rely on color alone to convey meaning.

A user moving from one screen or tool to another should not need to relearn basic interaction patterns such as where to save, how to cancel, how to identify read-only state, or how to recognize dangerous actions.

---

## 10. Audio Standards

Audio is loaded and played through a centralized `AudioManager`. Direct `AudioSource.Play()` calls outside this manager are not acceptable. All sound effects and music must be configurable (volume, mute) and respect the player's audio settings. Do not load audio assets synchronously on the main thread. Positional audio (3D audio) must not be used in a 2D Bingo UI context — all audio sources must be set to 2D spatial blend.

---

## 11. Localisation and Text Handling

All player-visible strings must be sourced from the localization system. No hardcoded English strings in UI code. Localization key naming convention: `<screen>.<component>.<purpose>` — e.g., `lobby.roomlist.empty_state`, `game.bingo_card.purchase_button1`. Number formatting (currency, large numbers, dates) must respect the player's locale. Test all UI layouts with German locale (typically 30–40% longer than English) to ensure text does not overflow.

---

## 12. Client-Side Security

The client is fully readable and modifiable by a motivated attacker. Any logic with monetary or competitive consequence must be validated on the server.

### 12.1 Certificate Pinning

TLS certificate pinning must be implemented on iOS and Android builds to prevent man-in-the-middle attacks. Pin the public key, not the certificate, and include a backup pin to support key rotation without a forced app update.

### 12.2 Session Token Handling

Session tokens must be stored in the platform's secure storage (iOS Keychain, Android Keystore) — not in PlayerPrefs. Refresh tokens before they expire. Tokens must be cleared on logout and on session expiry detection. Never send a token in URL query parameters — always in the Authorization header.

### 12.3 Anti-Cheat Awareness

Do not transmit sensitive intermediate state (e.g., the Bingo ball sequence before it is drawn) to the client ahead of time. Do not use sequential, guessable identifiers for rewards, tickets, or game sessions on the client. Rate-limit client-initiated actions on the server (see ESTD4); the client does not enforce rate limits.

### 12.4 Build Security

Apply IL2CPP code stripping and obfuscation to release builds. Do not store sensitive data in plain text in PlayerPrefs. Encrypt locally-cached credentials and tokens.

### 12.5 Client-Side Security Vulnerabilities (Unity iOS / Android / Web / Facebook)

| Vulnerability | What It Looks Like in Our Environment | Required Controls |
|:--------------|:--------------------------------------|:------------------|
| **Reverse engineering / decompilation** | Unity binaries, WebGL builds, or asset bundles are inspected to discover endpoints, message formats, feature flags, or economy constants | Assume the client is readable; never embed secrets; keep business rules server-side; use IL2CPP and build hardening where applicable |
| **Memory tampering / cheat tools** | Attackers modify in-memory values such as currency, ball count, room state, or card markings | Client values are display-only; authoritative state stays on the server; add sanity checks for impossible client transitions |
| **MITM / SSL stripping / proxy interception** | Charles, Burp, or custom proxies inspect or alter API traffic when certificate validation is weak | TLS 1.2+ everywhere; certificate pinning on mobile; do not disable certificate checks in production builds |
| **Replay attacks** | A valid request or SmartFox message is captured and resent to claim rewards, repeat purchases, or duplicate joins | Use idempotency keys, request timestamps, sequence IDs, and server-side replay windows |
| **Session hijacking** | Stolen tokens are reused to impersonate a player across API or real-time channels | Store tokens only in secure platform storage; keep TTLs short; never place tokens in URLs or logs; require server-side token validation on protected flows |
| **Insecure local storage** | Tokens, PII, or cached state are stored in PlayerPrefs, plaintext files, or browser storage without adequate protection | Use Keychain / Keystore for secrets; keep sensitive data minimal; encrypt sensitive cached data when local persistence is unavoidable |
| **Automated bots / scripted abuse** | Scripts claim rewards, join rooms, or spam sensitive flows faster and more consistently than a human player | Rate-limit on the server by player identity, device, and session; add abuse heuristics and challenge flows where product-appropriate |
| **Ball sequence pre-fetching / predictive abuse** | A compromised client tries to discover future ball draws or room outcomes before the server reveals them | SmartFox and API must reveal only the current authoritative state at the correct time; future draw state must never be exposed to the client |

---

## 13. Platform Considerations

### 13.1 iOS

Adhere to Apple's App Store Review Guidelines. Support the current iOS version and the two previous major versions. Handle `applicationWillResignActive` and `applicationDidBecomeActive` for live game pause and resume. Memory warnings from the OS must trigger asset unloading.

### 13.2 Android

Support Android API level 26 (Android 8.0) and above. Test on a minimum of three representative low-end devices per release. Handle the `onTrimMemory` callback to release non-critical cached resources. ProGuard / R8 minification must be enabled for release builds.

### 13.3 Facebook / WebGL

WebGL builds must target modern browsers (Chrome, Firefox, Safari, Edge — latest two stable versions). WebGL memory is capped at 512 MB by the browser. Facebook Platform API calls must be handled gracefully when the player denies permission or the API is unavailable.

### 13.4 Cross-Platform Code Isolation

Platform-specific code must be isolated behind a platform abstraction layer. `#if UNITY_IOS`, `#if UNITY_ANDROID` preprocessor blocks must not be scattered across feature code; they belong in platform adapter classes.

```c#
// BAD — platform logic scattered in feature code
public void StoreToken(string token) {
#if UNITY_IOS
    IOSKeychain.Set("session_token", token);
#elif UNITY_ANDROID
    AndroidKeystore.Set("session_token", token);
#else
    PlayerPrefs.SetString("session_token", token);
#endif
}

// GOOD — platform logic in one place; feature code calls the interface only
public interface ISecureStorage { void Set(string key, string value); string Get(string key); }
public class IOSSecureStorage : ISecureStorage { ... }
public class AndroidSecureStorage : ISecureStorage { ... }
```

Use server-side feature flags to enable/disable features per platform. Do not use `#if` blocks for business logic.

---

## 14. Telemetry and Analytics Events

All analytics events must be defined in a central event catalog. Every event must include at minimum: `eventName`, `playerId` (hashed/anonymized), `sessionId`, `timestamp`, `platform`, `appVersion`, and `eventProperties`. Analytics calls must be fire-and-forget: a failure to log an event must not affect gameplay.

Do not fire analytics events as individual HTTP requests. Batch events (up to 20 at a time or every 30 seconds, whichever comes first). Queue events locally if the network is unavailable; flush on reconnect.

---

## 15. Crash Reporting and Monitoring

A crash reporting SDK (e.g., Firebase Crashlytics, Sentry) must be integrated on all platforms. Crash reports must be triaged within 24 hours for the top-10 crash causes. The crash-free session rate target is **≥ 99.5%** for all platforms.

Log state transitions and key user actions as breadcrumbs in crash reports. This dramatically reduces diagnosis time.

```c#
CrashReporting.Log("Player entering room", new Dictionary<string, object> {
    { "room_id", roomId },
    { "player_coin_balance", player.CoinBalance },
    { "network_type", NetworkUtils.GetConnectionType() }
});
```

---

## 16. Client Performance Standards

| Metric | Target | Minimum Acceptable |
|:-------|:-------|:-------------------|
| Frame rate (iOS, Android in-game) | 60 FPS | 30 FPS on low-end Android |
| Startup time (cold launch to lobby) | < 5 seconds on mid-range device | < 10 seconds |
| Screen transition time | < 300ms | < 500ms | 
| Loading indicator after user action | < 100ms | — | 
| Asset bundle download (content reset) | Incremental only | No forced full re-download |

These are release targets, not aspirational goals. Every release must be profiled and the results documented. Use the Unity Profiler and Frame Debugger before marking any feature complete.

---

## 17. Memory Leak Prevention

**Definition**: A *memory leak* is a condition where memory that is no longer needed by the application is not released, causing the application's memory footprint to grow over time until the OS terminates the process or the device runs out of physical memory. On mobile devices with constrained RAM budgets (see [§7.3 Memory Budgets](#73-memory-budgets)), memory leaks are a direct cause of crashes on low-end devices.

Memory leaks in a long-running mobile game cause gradual memory growth that ends in an OS-forced kill of the process — a crash from the player's perspective. They are especially insidious because they rarely manifest immediately; the leak accumulates over a 20-minute play session and strikes when the player is deepest into the game. Prevention is far cheaper than investigation.

### 17.1 The Most Common Leak Patterns in Unity Clients

| Source | Description | Prevention |
|:-------|:------------|:-----------|
| **Unsubscribed C# events** | A subscriber object is kept alive by the publisher's delegate reference even after the screen unloads | Symmetric subscribe/unsubscribe in `OnEnable`/`OnDisable` (see [ESTD3 §12.1]] |
| **Retained Addressables handles** | `AsyncOperationHandle` keeps the referenced asset loaded until `Addressables.Release()` is called | Release every handle in `OnDestroy`; use a handle registry | 
| **Static references to scene objects** | A static field holding a `MonoBehaviour` or `GameObject` prevents GC of the entire object graph rooted at that object | Never store scene-bound objects in static fields |
| **Lingering coroutines** | Coroutines started on a MonoBehaviour that is then disabled or destroyed continue to hold closure state | Always stop coroutines in `OnDisable`; store and cancel coroutine references |
| **Undisposed** `CancellationTokenSource` | `CancellationTokenSource` is an `IDisposable`; not disposing it leaks kernel handles | `_cts?.Dispose()` in `OnDisable`/`OnDestroy` |
| **Texture/RenderTexture not released** | `RenderTexture.GetTemporary()` must be matched with `RenderTexture.ReleaseTemporary()` | Use try/finally to guarantee release |
| **SmartFox event listeners** | Adding a SmartFox event listener without removing it keeps the subscriber alive | Remove all SFS listeners in `OnDisable` and extension `destroy()` | 
| **Pooled objects destroyed instead of released** | Calling `Destroy()` on a pooled object removes it from the pool; future `Get()` calls allocate instead | Always call `_pool.Release(obj)` — never `Destroy()` on pooled objects |
| **Large cached collections** | `Dictionary` or `List` grown without a size cap or eviction policy | Cap collection sizes; use `LRUCache<K,V>` for evict-on-capacity patterns |
| **Closures capturing outer scope** | Lambda or anonymous method captures a large object in its closure | Avoid capturing `this` or large structs in lambdas on hot paths | 
| **Lingering audio clips** | `AudioClip` loaded at runtime not unloaded when the scene changes | Unload unused assets with `Resources.UnloadUnusedAssets()` post scene transition | 
| **Thread holding reference** | A background thread captures a reference to a Unity object in a closure | Use value types or copies in worker closures, not GameObject references |

### 17.2 Detecting Memory Leaks

Use these tools before marking any feature complete:

- **Unity Profiler → Memory module:** Take snapshots at scene entry and after extended play. Growing "Other (Managed)" or "Texture Memory" indicates a leak.  
- **Memory Profiler Package (com.unity.memoryprofiler):** Captures the full managed heap and shows object reference chains. Identifies exactly which object is holding a leaked object alive.  
- **Unity's built-in** `GC.GetTotalMemory(false)`: Log this value at scene transitions and after extended sessions. A value that never decreases indicates accumulation.  
- **Xcode Instruments (iOS) / Android Studio Memory Profiler:** For native memory leaks (unmanaged C++ plugins, JNI bridges, large unmanaged buffers).

```c#
// Lightweight in-game memory telemetry (development builds only)
[System.Diagnostics.Conditional("DEVELOPMENT_BUILD")]
private void LogMemorySnapshot(string checkpoint)
{
    long managedBytes = GC.GetTotalMemory(false);
    Logger.Info($"[Memory] {checkpoint}: managed={managedBytes / 1024 / 1024}MB, " +
                $"totalReserved={UnityEngine.Profiling.Profiler.GetTotalReservedMemoryLong() / 1024 / 1024}MB");
}
```

Capture a baseline memory snapshot at game start, another after 20 minutes of typical play, and compare. Any object type that grew by > 10% unexpectedly is a candidate for investigation.

### 17.3 Memory Hygiene Rules

- Scene transitions must always release all assets loaded for the previous scene.  
- Object pools must have a maximum size cap. An unbounded pool is a controlled memory leak.  
- `Destroy()` must never be called on pooled objects — always `Release()` back to the pool.  
- Any class that loads assets or subscribes to events must implement a corresponding cleanup path.  
- Run a Memory Profiler session on every feature branch before merging if the feature adds any new asset loading, event subscriptions, or persistent singletons.

---

## 18. Runtime Performance Optimisation

Performance in a Bingo game is not about raw computational power — it is about consistency. A single frame spike at 100ms during a ball draw causes a visible stutter that feels like a bug. The goal is not the highest average FPS; it is the most consistent frame time with no hitches.

### 18.1 CPU Optimisation

Reduce work in the frame loop. The Unity main thread has a budget of \~16.7ms per frame at 60 FPS. Operations that consume more than 2ms of that budget on every frame are candidates for optimization.

```
Update() budget model:
  16.7ms total frame time
  - 4ms   physics (FixedUpdate, physics step)
  - 2ms   UI layout/rendering
  - 2ms   animation
  - Remaining ≈ 8ms for application logic

  A single Update() method consuming 5ms leaves no room for anything else.
```

**Avoid work in** `Update()` that does not need per-frame execution:

```c#
// BAD — runs every frame; expensive
private void Update()
{
    _roomNearest = FindObjectsOfType<Room>().OrderBy(r => r.PlayerCount).First();
}

// GOOD — only runs when rooms change; triggered by an event
private void OnRoomListChanged(RoomListChangedEvent e)
{
    _roomNearest = _rooms.OrderBy(r => r.PlayerCount).FirstOrDefault();
}
```

Key strategies:

- **Time-slice expensive operations.** Spread multi-step initialization or evaluation across multiple frames using coroutines or async jobs. Do not do time consuming complicated processing in one Update() call.  
- **Cache** `GetComponent<T>()` results. Calling `GetComponent<Transform>()` every frame is expensive. Cache in `Awake()`.  
- **Use Job System / Burst for heavy computation.** Pattern matching across many Bingo cards simultaneously is a candidate for the Unity Job System with Burst compilation — runs on worker threads with SIMD optimization.  
- **Avoid LINQ in hot paths.** LINQ allocates enumerators and closures; replace with plain `for` loops in `Update()` and message handlers.

**Use timers for periodic checks:** 

```c#
private float _timerCheck;
private const float INTERVAL_CHECK_SEC = 2.0f;

private void Update()
{
    _timerCheck += Time.deltaTime;
    if (_timerCheck < INTERVAL_CHECK_SEC) return;
    _timerCheck = 0f;
    PeriodicCheckExecute();   // Runs every 2 seconds, not every frame
}
```

**Avoid** `GetComponent<>()` and `FindObjectOfType<>()` in `Update()`: Cache all component references in `Awake()`.

### 18.2 Rendering Optimisation

- **Use sprite atlases.** Each draw call submits all sprites from one atlas in a single batch. Sprites on different atlases generate separate draw calls. Keep UI sprites batched in no more than 3 atlases per screen.  
- **Object culling:** Disable (not destroy) off-screen GameObjects. Use Canvas.enabled = false for invisible UI layers rather than leaving them active.  
- **Reduce overdraw.** Full-screen effects, large transparent panels, and layered UI elements add overdraw cost. Use the Frame Debugger to identify screens with overdraw ratios above 3x.  
- **Disable cameras when not in use.** A disabled camera does not render. If a camera's view is not needed for a frame, disable it.  
- **Use object pooling for particle systems.** Every `ParticleSystem.Play()` on a new instance incurs instantiation overhead. Pool particle systems just like UI prefabs.  
- **LOD for content-heavy screens.** If the lobby shows many room cards simultaneously, implement dynamic LOD — only fully render the visible viewport; simplify off-screen cards.  
- **UI Rebuild throttling:** Avoid modifying Text or Image every frame — cache the last value and only update when it changes.

```c#
// BAD — rebuilds the UI canvas every frame even when value hasn't changed
private void Update() { _coinLabel.text = _player.Coins.ToString(); }

// GOOD — only updates when the value actually changes
private void OnCoinsChanged(int newCoins)
{
    _coinLabel.text = newCoins.ToString("N0");  // Localised number format
}
```

### 18.3 Memory/GC Optimisation

See [ESTD3 §7. Memory and Garbage Collection](./ESTD3_-_Unity_and_C%23_Standards.md#7-memory-and-garbage-collection) and [ESTD3 §8. String Allocation in Hot Paths](./ESTD3_-_Unity_and_C%23_Standards.md#8-string-allocation-in-hot-paths) for Unity-specific string allocation and GC rules. The key client-side rules:

- Object pooling for frequently created/destroyed objects ([ESTD3 §9. Object Pooling](./ESTD3_-_Unity_and_C%23_Standards.md#9-object-pooling)).  
- `StringBuilder` for any string construction in hot paths.  
- Struct-based event args to avoid heap allocation for high-frequency events.  
- Avoid LINQ in `Update()` — LINQ allocates enumerators on the heap.

See [§17. Memory Leak Prevention](#17-memory-leak-prevention). The primary runtime performance impact of poor memory management is GC-pause frame drops. A 30ms GC pause at 60 FPS causes two dropped frames — visibly jarring during animations and ball draws.

**GC pause reduction strategies:**

- Pre-allocate collections with known capacity.  
- Use `struct` event args instead of `class` for high-frequency events.  
- Use `StringBuilder` instances as fields (not local variables) on hot paths.  
- Run `GC.Collect()` explicitly at safe moments (scene transition, loading screen) to avoid mid-game pauses.

```c#
// Trigger GC at a safe moment — not during gameplay
private async UniTask LoadRoomAsync(int roomId, CancellationToken ct)
{
    _screenLoading.Show();
    GC.Collect();               // Force collection now, not mid-game
    await Task.Yield();         // Let GC run
    await _assetLoader.LoadRoomAssetsAsync(roomId, ct);
    _screenLoading.Hide();
}
```

### 18.4 Network Payload and Asset Load Optimisation

- **Incremental asset bundle downloads.** Never force a full re-download of all bundles on app launch. Only download changed bundles (determined by comparing asset hashes against the remote manifest).  
- **Preload critical-path assets.** Assets required for the first playable screen (lobby room list, default room theme) must be preloaded during the startup sequence, not loaded on demand when the player opens the screen.  
- **Compress texture atlases.** Use ASTC (iOS), ETC2 (Android), or DXT (desktop) texture compression formats. Uncompressed RGBA32 textures are 4–8× larger than necessary.  
- **Use Content Delivery Network (CloudFront) caching.** Asset bundles served from S3 via CloudFront with long cache TTLs (7 days minimum) are served from edge locations near the player. Ensure CloudFront cache headers are set correctly on the S3 origin.  
- Compress request/response payloads with gzip for payloads > 1KB.  
- Request only the fields needed (projection on the server side).  
- Cache frequently read, rarely changing data locally (feature flags, event config) for the session duration.  
- Batch analytics and telemetry events — never send one HTTP request per event.

### 18.5 Performance Profiling Requirement

The Unity Profiler and Frame Debugger must be run against every feature branch before merging if the feature adds any new `Update()` logic, spawns new GameObjects per frame, or loads new assets. Document the profiling results in the PR description.

---

## 19. Battery Management for Mobile

**Definition:** *Battery drain* refers to the rate at which a mobile game consumes electrical power from the device battery, measured indirectly by CPU utilization, GPU activity, network radio usage, and screen brightness management.

Battery drain is one of the top player complaints for mobile games. Excessive battery drain causes players to stop mid-session, reduces session length, and generates negative app store reviews. Since most Bingo sessions occur during commutes or casual play, battery efficiency directly affects session length and retention.

### 19.1 Frame Rate Capping

Running at 60 FPS uncapped when nothing is animating wastes power. Apply dynamic frame rate management:

```c#
public static class FrameRateController
{
    // During active gameplay (ball draw, animations, transitions)
    public static void FrameRateActiveSet()
    {
        Application.targetFrameRate = 60;
        QualitySettings.vSyncCount  = 0;
    }

    // During idle states (waiting for ball draw, lobby idle, settings screen)
    public static void FrameRateIdleSet()
    {
        Application.targetFrameRate = 30;
    }

    // When the app is paused / in background
    public static void FrameRateBackgroundSet()
    {
        Application.targetFrameRate = 15;
    }
}
```

Trigger `FrameRateIdleSet()` when the ball-draw timer is counting down and no animations are in progress. Trigger `FrameRateActiveSet()` when a ball is being drawn or an animation is playing.

### 19.2 Reduce Wake-Ups from Network Activity

Every network request wakes the device radio from a low-power state. Unnecessary requests burn battery disproportionately.

- **Batch API calls.** Combine multiple small requests into one (e.g., fetch player profile + room list + daily bonus status in a single startup endpoint).  
- **Avoid aggressive polling.** Use SmartFox push for real-time events; do not poll the REST API for game state updates. A polling interval of 1 second means 3,600 radio wake-ups per hour.  
- **Use HTTP/2** on the REST API. HTTP/2 multiplexes multiple requests over a single TCP connection, reducing connection establishment overhead and associated radio activity.  
- **Disconnect SmartFox when backgrounded.** When `OnApplicationPause(true)` fires, disconnect the SmartFox TCP connection gracefully. Maintaining an idle persistent TCP connection prevents the radio from entering low-power state.

### 19.3 Reduce CPU and GPU Activity When Idle

- **Pause** `Update()` logic when idle. Use a `_isIdle` flag to skip expensive per-frame computations when the game is in a wait state between ball draws.  
- **Disable ambient particle systems during wait states.** Ambient effects running at 60 FPS between ball draws are unnecessary power consumers. Pause them and resume only when a ball is drawn.  
- **Reduce shader complexity for non-critical elements.** Simple UI cards do not need complex fragment shaders. Use the simplest shader that achieves the visual result.  
- **Dim the screen during extended idle.** If the player has not interacted for 60 seconds and is simply waiting for the next ball, suggest reducing screen brightness or use the OS API to request a screen dim (iOS: `UIApplication.shared.isIdleTimerDisabled = false`; Android: `WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON` cleared).

### 19.4 Rendering-Related Battery Savings

- **Disable Vsync during idle:** `QualitySettings.vSyncCount = 0` when no animations are running, combined with a low `targetFrameRate`. 
- **GPU power hint (Android):** Use `AndroidJavaClass` to hint the GPU driver to use a power-saving mode during lobby browsing.  
- **Texture compression:** Use ASTC for iOS and Android — better quality-per-byte than ETC2, reducing GPU memory bandwidth.  
- **Particle system limits:** Cap maximum particle counts. Uncapped particle emitters are a common source of unnecessary GPU work.

### 19.5 iOS-Specific Battery Optimizations

- **Use Metal efficiently.** Avoid explicit synchronization barriers in Metal render passes; batch draw calls.  
- **Prefer** `CADisplayLink` over `NSTimer` for animations. `CADisplayLink` is synchronized to the display refresh and is more efficient.  
- **Background task API:** When transitioning to background, call `UIApplication.beginBackgroundTask(withName:)` only for genuinely essential background work (e.g., finishing an in-flight reward claim). Do not hold background task time open indefinitely.

### 19.6 Android-Specific Battery Optimizations

- **Respect** `onTrimMemory()`. When Android signals memory pressure, release non-critical cached assets and reduce frame rate to the idle level.  
- **Use** `JobScheduler` / `WorkManager` for deferred background work. Do not spin up background threads for analytics flushing — delegate to Android's system job scheduler which batches work at device-optimal times.  
- `WAKE_LOCK` must never be held. Holding a `WAKE_LOCK` prevents the device from sleeping. Never request one; use `FLAG_KEEP_SCREEN_ON` only if the game legitimately requires the screen to stay on during active play, and release it when the game is paused.

### 19.7 Network-Related Battery Savings

- Batch HTTP requests — a single request draining the radio is cheaper than many small ones.  
- Use the SmartFox persistent TCP connection for real-time events — HTTP polling is far more battery-intensive.  
- Implement exponential backoff for reconnection attempts — do not repeatedly hammer the radio at fixed intervals.

### 19.8 Thermal Throttling Awareness

Continuous 60 FPS rendering will cause the device to throttle CPU/GPU speed after sustained load. Implement a thermal state monitor:

```c#
// iOS thermal state monitoring
private void OnThermalStateChanged(Device.ThermalState state)
{
    switch (state)
    {
        case Device.ThermalState.Nominal:  Application.targetFrameRate = 60; break;
        case Device.ThermalState.Fair:     Application.targetFrameRate = 45; break;
        case Device.ThermalState.Serious:  Application.targetFrameRate = 30; break;
        case Device.ThermalState.Critical: Application.targetFrameRate = 15; break;
    }
}
```

### 19.9 Battery Testing Requirements

Battery behavior must be tested on representative hardware before each release:

- Measure battery drain during a 30-minute active Bingo session (one game room, continuous play) using the device's battery analytics or a hardware power monitor.  
- The acceptable drain threshold is **≤ 10% per 30 minutes** on mid-range hardware.  
- Profile the same session with Xcode Energy Gauge (iOS) or Android Battery Historian to identify CPU, GPU, network, and location (GPS — should be zero) contributors.

Document results in the release sign-off notes.

---

## 20. Offline and Network-Degraded Behavior

The client must detect network connectivity and display a persistent visual indicator when offline. Core features that require a server connection must be gracefully disabled with a clear explanation when offline. On network restoration, the client must automatically attempt to re-establish the server connection without requiring a manual app restart.

---

## 21. Accessibility

- Minimum tap target size: 44 × 44 points (iOS HIG), 48 × 48 dp (Material Design Android).  
- Text must be legible at the device's default text size. Support Dynamic Type (iOS) and font scale settings (Android) where practical.  
- All interactive elements must have accessible labels for screen reader support.  
- The Reduce Motion system setting must disable or simplify animations.  
- Color contrast ratios must meet WCAG 2.1 AA minimum (`4.5:1` for normal text, `3:1` for large text).

---

## 22. Common Pitfalls to Avoid

| # | Pitfall | Impact | Remedy |
|:--|:--------|:-------|:-------|
| 1 | Business logic in the View layer |  Logic duplicated, UI-coupled bugs, untestable | Move to Domain or Presentation layer |
| 2 | SmartFox callbacks calling Unity API directly | Thread-safety crash | Dispatch to main thread via `MainThreadDispatcher` |
| 3 | Forgotten event unsubscriptions | Memory leaks, ghost callbacks | Always unsubscribe in `OnDisable` / `OnDestroy` |
| 4 | Synchronous asset loading on main thread | Frame stalls, ANRs on Android | Always load assets asynchronously |
| 5 | Session token in PlayerPrefs | Security vulnerability | Use platform secure storage |
| 6 | No cancellation token on async operations | Null reference after screen destroyed | Link `CancellationToken` to component lifecycle | 
| 7 | No loading / error state on async UI | Confusing UX, support tickets | Implement all three states (loading/success/error) |
| 8 | Double-submission of network requests | Duplicate purchases, corrupted state | Disable control while request is in-flight |
| 9 | Hardcoded UI strings | Missing translations, extra release for text fixes | Use localization system exclusively |
| 10 | DoTween usage | Prohibited library; inconsistent tooling | Use LeanTween only | 
| 11 | No reconnect logic | Player sees a dead screen after any network blip | Implement exponential backoff reconnect | 
| 12 | Transmitting ball sequence to client early | Cheating vector | Server sends draw results only as they happen |
| 13 | Mutating shared data from SmartFox thread | Race condition, data corruption | Use `ConcurrentQueue` or `MainThreadDispatcher` |
| 14 | Optimistic UI without a rollback path | Inconsistent state on server rejection | Always implement rollback for optimistic updates |
| 15 | Worker thread with no CancellationToken | Thread outlives owner; app hangs on shutdown | Every worker requires a CancellationToken |
| 16 | Worker calling Unity APIs from background thread | Engine crash | Dispatch via `MainThreadDispatcher` |
| 17 | `Update()` logic that runs every frame unnecessarily | CPU waste, battery drain | Use timers, events, or coroutines instead |
| 18 | Texture/RenderTexture not released | Memory grows until OS kills process | Always `Release()` and `Destroy()` dynamic textures |
| 19 | Full 60 FPS while game is in idle state | Excessive battery drain | Cap to 30 FPS during idle; 15 FPS when backgrounded |
