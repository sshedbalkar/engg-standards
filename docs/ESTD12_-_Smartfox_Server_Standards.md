# ESTD12 — SmartFox Server Standards for Bingo Game Development

**ESTD12 — SmartFox Server Standards**

| Field | Value |
|:----- |:----- |
| **Document ID** | ESTD12 |
| **Version** | 5.0 |
| **Status** | Active |
| **Last Updated** | 2026-04-13 |
| **Applies To** | All engineers contributing to the SmartFox live server for either Bingo game |
| **Depends On** | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server) |
| **Approval** | Director of Engineering / Server Architect |

---

**📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD12 governs all Java code written for the SmartFox Server (SFS) live server used by both the legacy and new Bingo games. It builds on [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server) (Java Programming Standards) and specializes those rules for the SmartFox runtime environment. All rules in [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), and [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server) apply in full; this document adds or narrows rules that are specific to SmartFox.

Read [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), and [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server) before this document.

---

## Table of Contents

- [ESTD12 — SmartFox Server Standards for Bingo Game Development](#estd12--smartfox-server-standards-for-bingo-game-development)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. What SmartFox Is and Why It Exists](#2-what-smartfox-is-and-why-it-exists)
  - [3. SmartFox Architecture Principles](#3-smartfox-architecture-principles)
    - [3.1 Extension Decomposition](#31-extension-decomposition)
    - [3.2 The API Server Is the Authority — Even Within SmartFox](#32-the-api-server-is-the-authority--even-within-smartfox)
    - [3.3 State Persistence Checkpoints (WIP - needs discussion)](#33-state-persistence-checkpoints-wip---needs-discussion)
  - [4. Extension Structure and Handler Pattern](#4-extension-structure-and-handler-pattern)
    - [4.1 One Handler Per Command Type](#41-one-handler-per-command-type)
    - [4.2 Handler Internal Structure](#42-handler-internal-structure)
  - [5. SmartFox Data Abstraction](#5-smartfox-data-abstraction)
    - [5.1 Parse at the Boundary, Use Domain Types Everywhere Else](#51-parse-at-the-boundary-use-domain-types-everywhere-else)
    - [5.2 Response Serialization at the Boundary](#52-response-serialization-at-the-boundary)
  - [6. Room Lifecycle and State Management](#6-room-lifecycle-and-state-management)
    - [6.1 Room State Machine](#61-room-state-machine)
    - [6.2 Thread-Safe State Transitions](#62-thread-safe-state-transitions)
    - [6.3 Room Cleanup](#63-room-cleanup)
  - [7. Real-Time Concurrency and Thread Safety](#7-real-time-concurrency-and-thread-safety)
    - [7.1 Synchronize on Room State](#71-synchronize-on-room-state)
    - [7.2 Never Hold a Lock During I/O](#72-never-hold-a-lock-during-io)
    - [7.3 Use Concurrent Collections for Room Registry](#73-use-concurrent-collections-for-room-registry)
  - [8. Scheduled Tasks (Number Calling)](#8-scheduled-tasks-number-calling)
    - [8.1 Using ScheduledExecutorService](#81-using-scheduledexecutorservice)
    - [8.2 Defensive Error Handling in the Task Body](#82-defensive-error-handling-in-the-task-body)
  - [9. Network Latency Strategies at Critical State Transition Junctures](#9-network-latency-strategies-at-critical-state-transition-junctures)
    - [9.1 Failure Model: Split-Brain Windows at State Transitions](#91-failure-model-split-brain-windows-at-state-transitions)
    - [9.2 Room-Wide Monotonic Sequencing Is Mandatory](#92-room-wide-monotonic-sequencing-is-mandatory)
    - [9.3 Transition-Specific Client Behaviour: Optimistic Where Safe, Confirm Where Necessary](#93-transition-specific-client-behaviour-optimistic-where-safe-confirm-where-necessary)
    - [9.4 Critical Transitions Must Be Time-Bounded on Both Client and Server](#94-critical-transitions-must-be-time-bounded-on-both-client-and-server)
    - [9.5 Reconnects Must Use Full State Snapshots, Not Event Replay](#95-reconnects-must-use-full-state-snapshots-not-event-replay)
    - [9.6 Duplicate Transition Messages Must Be Idempotent](#96-duplicate-transition-messages-must-be-idempotent)
    - [9.7 High-Frequency Ball Draws Should Use a Jitter Buffer](#97-high-frequency-ball-draws-should-use-a-jitter-buffer)
    - [9.8 Heartbeats, RTT Monitoring, and Degraded Mode Are Required Operational Controls](#98-heartbeats-rtt-monitoring-and-degraded-mode-are-required-operational-controls)
    - [9.9 Graceful Degradation Rules at Critical Junctures](#99-graceful-degradation-rules-at-critical-junctures)
    - [9.10 Anti-Patterns to Avoid](#910-anti-patterns-to-avoid)
    - [9.11 Minimum Implementation Checklist](#911-minimum-implementation-checklist)
    - [9.12 Protocol Versioning and Mixed-Client Compatibility](#912-protocol-versioning-and-mixed-client-compatibility)
  - [10. Authoritative API Communication from SmartFox](#10-authoritative-api-communication-from-smartfox)
    - [10.1 HTTP Client Configuration](#101-http-client-configuration)
    - [10.2 Retry and Fallback Policy](#102-retry-and-fallback-policy)
  - [11. Player Presence and Session Management](#11-player-presence-and-session-management)
    - [11.1 Player Join Validation](#111-player-join-validation)
    - [11.2 Player Disconnect Handling](#112-player-disconnect-handling)
    - [11.3 Reconnect State Sync](#113-reconnect-state-sync)
  - [12. SmartFox Security Vulnerabilities](#12-smartfox-security-vulnerabilities)
  - [13. Logging in SmartFox](#13-logging-in-smartfox)
  - [14. Idempotency in SmartFox](#14-idempotency-in-smartfox)
    - [14.1 Sequence ID-Based Idempotency](#141-sequence-id-based-idempotency)
  - [15. Graceful Shutdown and Restart](#15-graceful-shutdown-and-restart)
    - [15.1 Graceful Shutdown Sequence](#151-graceful-shutdown-sequence)
    - [15.2 State Recovery on Startup](#152-state-recovery-on-startup)
  - [16. Health Monitoring and Metrics](#16-health-monitoring-and-metrics)
    - [16.1 Health Check Endpoint](#161-health-check-endpoint)
    - [16.2 Custom Metrics (Datadog)](#162-custom-metrics-datadog)
  - [17. JVM Tuning for SmartFox](#17-jvm-tuning-for-smartfox)
  - [18. Memory Management and Object Lifecycle](#18-memory-management-and-object-lifecycle)
    - [18.1 Room Lifecycle Corresponds to Memory Lifecycle](#181-room-lifecycle-corresponds-to-memory-lifecycle)
    - [18.2 Event Listener Cleanup](#182-event-listener-cleanup)
    - [18.3 The Five Most Common SmartFox Memory Leak Patterns](#183-the-five-most-common-smartfox-memory-leak-patterns)
    - [18.4 JVM Garbage Collection Tuning](#184-jvm-garbage-collection-tuning)
    - [18.5 Memory Monitoring](#185-memory-monitoring)
  - [19. Memory Leak Prevention in SmartFox Extensions](#19-memory-leak-prevention-in-smartfox-extensions)
    - [19.1 Primary Sources of Memory Leaks in SmartFox Extensions](#191-primary-sources-of-memory-leaks-in-smartfox-extensions)
    - [19.2 Heap Monitoring and Leak Detection](#192-heap-monitoring-and-leak-detection)
    - [19.3 Memory Leak Prevention Checklist](#193-memory-leak-prevention-checklist)
  - [20. Testing SmartFox Extensions](#20-testing-smartfox-extensions)
    - [20.1 Testing the Game Engine in Isolation](#201-testing-the-game-engine-in-isolation)
    - [20.2 Win Pattern Test Coverage](#202-win-pattern-test-coverage)
  - [21. Common Pitfalls to Avoid](#21-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

This document applies to all Java code written for the SmartFox Server Extension layer used by both Bingo games. SmartFox is the real-time coordination layer for active Bingo game rooms. It is fundamentally different from the stateless PHP and SEAM microservice APIs: it is a long-running, stateful JVM process that holds live game room state in memory and coordinates real-time events across hundreds of concurrent players.

The standards in this document reflect the unique constraints of that environment: low-latency requirements, persistent in-memory state, multi-threaded message delivery, and the elevated consequence of a crash (active game rooms are disrupted for live players).

---

## 2. What SmartFox Is and Why It Exists

What SmartFox is: SmartFox Server (SFS2X) is a Java-based multiplayer game server framework that manages persistent TCP connections, rooms, and real-time message broadcasting between connected clients. It provides a connection management layer (player presence, room membership), a message routing layer (broadcasting to all players in a room, sending to a specific player), and an extension layer (Java code written by the development team to implement game logic).

Why it exists in the Bingo architecture: Bingo requires real-time coordination that REST/HTTP cannot efficiently provide. When a ball is drawn, it must be broadcast to all 200 players in a room simultaneously with minimal latency. When a player claims Bingo, the server must immediately check validity and notify all other players of the result. HTTP polling at the required frequency would generate hundreds of requests per second per room and would not achieve the sub-second latency required for a good game experience. SmartFox's persistent TCP connection model handles this elegantly.

What SmartFox is NOT responsible for: SmartFox must not make final economic decisions (awarding coins, validating wins as canonical game outcomes). All outcomes with monetary or competitive consequence are validated by the authoritative API server. SmartFox coordinates the experience; the authoritative API enforces integrity.

```
Role Separation:

SmartFox                            authoritative API
────────────────────────────────    ────────────────────────────────
Manages persistent connections      Validates all game outcomes
Broadcasts number calls             Awards coins and bonuses
Routes player messages              Maintains the canonical ledger
Tracks room membership              Enforces business rules
Coordinates timing of game events   Authenticates requests
Detects potential winners           Confirms wins (authoritative)
```

---

## 3. SmartFox Architecture Principles

### 3.1 Extension Decomposition

Each SmartFox extension must have a single, clear responsibility. Do not build a monolithic extension that handles all game logic. Decompose extensions by domain. Handle everything else in request handlers.

**Recommended extension decomposition for Bingo:**

```
BingoMainZoneExtension    → Application bootstrap; registers all sub-extensions
BingoRoomExtension        → Room lifecycle: create, join, leave, room settings
BingoGame                 → Timer,event driven Game lifecycle: start, number draw, win 
                            detection, end
BingoRequestHandler       → Per request type based, Reconnect flow and state sync on 
                            reconnect, and other client request driven flows
```

### 3.2 The API Server Is the Authority — Even Within SmartFox

SmartFox code is server-side code and is subject to all server-authority rules defined in ESTD4 §2.1. No game outcome may be treated as final until the authoritative API has confirmed it. A win detected by SmartFox is a candidate win; a win confirmed by the authoritative API is a final win.

### 3.3 State Persistence Checkpoints (WIP - needs discussion)

SmartFox's in-memory state must be persisted to the database at defined checkpoints so that a restart or crash does not result in permanent state loss. Mandatory persistence checkpoints are: when a player joins or leaves a room; when a game round starts or ends; when a win is validated; and whenever coin balance changes occur (which are always delegated to the authoritative API).

---

## 4. Extension Structure and Handler Pattern

SmartFox delivers all client messages to a single `handleClientRequest` entry point. Without a structured handler pattern, this entry point becomes a large, unreadable switch statement that is difficult to test, difficult to extend, and impossible to understand in isolation. The handler pattern solves this by routing each command type to a dedicated class.

### 4.1 One Handler Per Command Type

Each client command must be handled by a dedicated, single-purpose handler class registered at extension initialization.

```java
// BAD — monolithic switch statement in a single extension
@Override
public void handleClientRequest(User user, ISFSObject params) {
    String cmd = (String) params.get("cmd");
    switch (cmd) {
        case "JOIN_ROOM":   // 80 lines of join logic
        case "DAUB":        // 60 lines of daub logic
        case "CLAIM_BINGO": // 70 lines of claim logic
        // ... unmaintainable
    }
}

// GOOD — registered handlers, one per command
public class BingoGameExtension extends SFSExtension {
    @Override
    public void init() {
        addRequestHandler(Commands.JOIN_ROOM,   new JoinRoomHandler(roomManager, gameApiClient, logger));
        addRequestHandler(Commands.DAUB,        new DaubHandler(gameEngine, logger));
        addRequestHandler(Commands.CLAIM_BINGO, new ClaimBingoHandler(gameEngine, winValidator, logger));
        addRequestHandler(Commands.LEAVE_ROOM,  new LeaveRoomHandler(roomManager, logger));
    }
}
```

**Entry-point boundary**: SmartFox extension handlers (`handleRequest`, `handleClientEvent`, `handleServerEvent`) are entry-point boundaries ([ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions)). They may wrap the entire handler body in a single try block with multiple typed catch clauses. Code in service, DAO, and domain classes called from these handlers must use individual per-statement try-catch blocks ([ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)).

### 4.2 Handler Internal Structure

Every handler must follow this four-step structure:

```java
public class ClaimBingoHandler implements IClientRequestHandler {
    @Override
    public void handleRequest(User user, ISFSObject params, Room room) {

        // STEP 1: Extract and validate parameters from the SFSObject
        ClaimBingoRequest request;
        try {
            request = ClaimBingoRequest.fromSfsObject(params);
            request.validate();
        } catch (InvalidRequestException ex) {
            logger.warn("Invalid CLAIM_BINGO params from user {}: {}", user.getId(), ex.getMessage());
            errorSend(user, ErrorCode.INVALID_PARAMS, ex.getMessage());
            return;
        }

        // STEP 2: Validate business rules using domain objects (no SFS types here)
        BingoClaimResult result;
        try {
            result = gameEngine.bingoClaim(user.getId(), room.getId(), request);
        } catch (BingoAlreadyClaimedException ex) {
            errorSend(user, ErrorCode.ALREADY_CLAIMED, "Bingo has already been claimed this round");
            return;
        } catch (InvalidMoveException ex) {
            logger.info("Invalid bingo claim by user {}: {}", user.getId(), ex.getMessage());
            errorSend(user, ErrorCode.INVALID_CLAIM, ex.getMessage());
            return;
        }

        // STEP 3: Persist the outcome before sending to clients
        // (Persistence happens inside gameEngine.bingoClaim via the authoritative API call)

        // STEP 4: Broadcast result to the room
        ISFSObject response = result.toSfsObject();
        getParentExtension().send("responseId", response, user);
    }

    private void errorSend(User user, ErrorCode code, String message) {
        ISFSObject err = new SFSObject();
        err.putUtfString("errorCode", code.name());
        err.putUtfString("message", message);
        getParentExtension().send("responseId", JsonSerializer.toJson(err), user);
    }
}
```

**Try-catch scope in SmartFox handlers**: SmartFox extension handler methods (`handleRequest`, `handleClientEvent`, `handleServerEvent`, etc.) are entry-point boundaries ([ESTD1 §9.1 When to Use Try-Catch](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#91-when-to-use-try-catch)). They may wrap the entire handler body in a single try block with multiple typed catch clauses — this is the correct boundary pattern. All code in service, DAO, and domain classes called from these handlers must use individual per-statement try-catch blocks ([ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)).
4.3 Command Name Constants

All SmartFox command names must be defined as constants in a single Commands class, not as string literals scattered through handlers.

```java
public final class Commands {
    private Commands() {}

    public static final String JOIN_ROOM    = "JOIN_ROOM";
    public static final String LEAVE_ROOM   = "LEAVE_ROOM";
    public static final String DAUB         = "DAUB";
    public static final String CLAIM_BINGO  = "CLAIM_BINGO";
    public static final String SYNC_STATE   = "SYNC_STATE";
}
```

---

## 5. SmartFox Data Abstraction

SmartFox's `ISFSObject` API is verbose and stringly-typed — you fetch fields by string name and cast them manually. If game engine code uses `ISFSObject` directly, it becomes tightly coupled to SmartFox's wire format, making it impossible to unit test without a running SmartFox instance. The abstraction layer solves this by confining SmartFox types to the handler boundary.

### 5.1 Parse at the Boundary, Use Domain Types Everywhere Else

SmartFox parameter objects (`ISFSObject`) must be parsed into immutable domain records at the very start of a handler. All code below the handler boundary — the game engine, the win checker, the room manager — must use domain types only, with no dependency on SmartFox SDK classes.

```java
// Domain record — no SmartFox dependency; fully testable
public record DaubRequest(int ballNumber, int cardId) {

    public static DaubRequest fromSfsObject(ISFSObject params) {
        if (!params.containsKey("ball") || !params.containsKey("cardId")) {
            throw new InvalidRequestException("Missing required fields: 'ball', 'cardId'");
        }
        return new DaubRequest(params.getInt("ball"), params.getInt("cardId"));
    }

    public void validate() {
        if (ballNumber < 1 || ballNumber > 75) {
            throw new InvalidRequestException("Ball number out of range: " + ballNumber);
        }
        if (cardId <= 0) {
            throw new InvalidRequestException("Invalid cardId: " + cardId);
        }
    }
}
```

### 5.2 Response Serialization at the Boundary

Similarly, domain result objects are converted back to `ISFSObject` only at the response step of the handler. Domain result classes must provide a `toSfsObject()` method.

```java
public record DaubResult(boolean isValid, boolean isWinner, WinPattern winPattern) {

    public ISFSObject toSfsObject() {
        ISFSObject obj = new SFSObject();
        obj.putBool("valid",    isValid);
        obj.putBool("isWinner", isWinner);
        if (isWinner && winPattern != null) {
            obj.putUtfString("winPattern", winPattern.name());
        }
        return obj;
    }
}
```

---

## 6. Room Lifecycle and State Management

Bingo rooms have a well-defined lifecycle with specific valid state transitions. Code that allows invalid transitions — for example, accepting a daub after a game has ended — creates subtle bugs that are difficult to reproduce because they depend on precise timing of concurrent events. An explicit state machine makes valid and invalid transitions visible and testable.

### 6.1 Room State Machine

```
WAITING_FOR_PLAYERS ──→ GAME_STARTING ──→ GAME_IN_PROGRESS ──→ ROUND_ENDED
         ↑                                        │                  │
         └────────────────────────────────────────┴──→ GAME_COMPLETE ─→ CLOSED

VALID TRANSITIONS:
  WAITING_FOR_PLAYERS → GAME_STARTING    (minimum players reached)
  GAME_STARTING       → GAME_IN_PROGRESS (countdown complete)
  GAME_IN_PROGRESS    → ROUND_ENDED      (bingo claimed and validated)
  ROUND_ENDED         → GAME_IN_PROGRESS (next round begins)
  ROUND_ENDED         → GAME_COMPLETE    (final round ended)
  GAME_COMPLETE       → CLOSED           (room cleanup complete)
  Any state           → WAITING_FOR_PLAYERS (all players left)
```

### 6.2 Thread-Safe State Transitions

```java
public class BingoRoomStateMachine {
    private final AtomicReference<RoomState> state =
        new AtomicReference<>(RoomState.WAITING_FOR_PLAYERS);
    private final int roomId;

    /**
     * Attempts to transition from {@code expected} to {@code next}.
     * Returns true on success; false if current state does not match {@code expected}.
     * Thread-safe — uses compare-and-set.
     */
    public boolean transitionAttempt(RoomState expected, RoomState next) {
        boolean success = state.compareAndSet(expected, next);
        if (success) {
            logger.info("Room {} state: {} → {}", roomId, expected, next);
        } else {
            logger.warn("Room {} invalid transition: {} → {} (current: {})",
                roomId, expected, next, state.get());
        }
        return success;
    }

    public RoomState getState() { return state.get(); }
}
```

### 6.3 Room Cleanup

When a room ends, it must be explicitly cleaned up to release all memory. Do not rely on garbage collection alone — SmartFox holds references to room extension objects that can prevent GC of the room's data.

```java
public class BingoRoom {

    public void cleanup() {
        // Cancel all scheduled tasks to prevent them from firing after room is closed
        if (numberCallerFuture != null) {
            numberCallerFuture.cancel(false);
        }
        // Clear all in-memory state to allow GC
        players.clear();
        calledNumbers.clear();
        cardStates.clear();
        logger.info("Room {} cleaned up. Memory released.", roomId);
    }
}

// In the room termination handler:
public void roomTerminate(int roomId) {
    BingoRoom room = activeRooms.remove(roomId); // Remove from registry first
    if (room != null) {
        room.cleanup();
    }
}
```

---

## 7. Real-Time Concurrency and Thread Safety

SmartFox delivers client messages on multiple threads from its internal thread pool. Multiple players in the same room may send messages simultaneously, and SmartFox may invoke multiple handler instances at the same time. Without explicit synchronization on shared room state, the result is data corruption: two simultaneous daub requests may both see the same initial state and both overwrite each other's changes.

The full [ESTD7 §11. Concurrency Standards](./ESTD7_-_Java_Programming_Standards.md#11-concurrency-standards) concurrency rules apply. The following SmartFox-specific additions are mandatory.

### 7.1 Synchronize on Room State

All operations that read and write shared room state must synchronize on the room object itself. Hold the lock only for the critical section — release it before performing any I/O.

```java
public class BingoGameEngine {
    private final Object roomLock = new Object();

    public DaubResult daubProcess(int userId, int ballNumber) {
        // Critical section: read-modify-write of called numbers and card state
        synchronized (roomLock) {
            if (!calledNumbers.contains(ballNumber)) {
                throw new InvalidMoveException("Ball " + ballNumber + " has not been called");
            }
            CardState cardState = cardStates.get(userId);
            if (cardState == null) {
                throw new PlayerNotInRoomException(userId);
            }
            boolean daubed = cardState.applyDaub(ballNumber);
            boolean isWinner = winChecker.check(cardState.getDaubedNumbers(), currentPattern);
            return new DaubResult(daubed, isWinner, isWinner ? currentPattern : null);
        }
        // authoritative API call to validate win happens OUTSIDE the lock (I/O must not block the lock)
    }
}
```

### 7.2 Never Hold a Lock During I/O

```java
Holding a synchronization lock while making an HTTP call to the authoritative API will block all other operations in the same room for the entire duration of that HTTP call. This is a recipe for cascading latency.
// BAD — holding room lock during HTTP call
public synchronized void claimBingo(int userId) {
    // ... holds the lock for entire duration of HTTP round-trip
    boolean valid = gameApiClient.validateWin(userId, roomId); // DANGEROUS — may take 2+ seconds
}

// GOOD — capture state under lock, release lock, then do I/O
public void bingoClaim(int userId) {
    WinClaimSnapshot snapshot;
    synchronized (roomLock) {
        snapshot = winClaimSnapshotCapture(userId);  // Fast read-only operation
    }
    // I/O happens outside the lock
    WinValidationResult result = gameApiClient.winValidate(snapshot);
    // Re-acquire lock to apply the outcome
    synchronized (roomLock) {
        if (result.isValid()) {
            winOutcomeApply(userId, result.getCoinsAwarded());
        }
    }
}
```

### 7.3 Use Concurrent Collections for Room Registry

The room registry (the map from room ID to `BingoRoom` instance) is accessed from multiple threads and must use a thread-safe collection.

```java
// Thread-safe room registry
private final ConcurrentHashMap<Integer, BingoRoom> activeRooms = new ConcurrentHashMap<>();
```

---

## 8. Scheduled Tasks (Number Calling)

The number-calling loop is the heartbeat of every active Bingo game. It must fire at a consistent interval, handle errors without stopping, and be cleanly stoppable when the game ends. A bug in the scheduled task handler that throws an uncaught exception will silently kill the task — the game room will stop calling numbers, but no error will be surfaced to players until they complain.

### 8.1 Using ScheduledExecutorService

```java
private final ScheduledExecutorService scheduler =
    Executors.newSingleThreadScheduledExecutor(
        r -> new Thread(r, "number-caller-room-" + roomId) // Named thread for debugging
    );
private ScheduledFuture<?> numberCallerFuture;

public void numberCallingStart() {
    int intervalMs = configService.getInt("game.number_call_interval_ms"); // Never hardcode
    numberCallerFuture = scheduler.scheduleAtFixedRate(
        this::numberCallNext,
        INITIAL_DELAY_MS,
        intervalMs,
        TimeUnit.MILLISECONDS
    );
    logger.info("Number calling started for room {}. Interval: {}ms", roomId, intervalMs);
}

public void numberCallingStop() {
    if (numberCallerFuture != null) {
        numberCallerFuture.cancel(false);
        logger.info("Number calling stopped for room {}", roomId);
    }
    scheduler.shutdown();
}
```

### 8.2 Defensive Error Handling in the Task Body

**This is critical**: `ScheduledExecutorService` silently stops executing a task if the task body throws an unchecked exception. The task simply stops, with no error propagated. The game room becomes frozen from the players' perspective — no more balls are called — but no exception is visible unless you specifically log it.

Every scheduled task body must wrap its entire logic in a `try-catch(Exception)`:

```java
private void numberCallNext() {
    try {
        int nextBall = ballDrawer.drawNext();

        if (nextBall == BallDrawer.NO_MORE_BALLS) {
            // All 75 balls have been called — end the game
            logger.info("All balls drawn in room {}. Ending game.", roomId);
            numberCallingStop();
            endGame();
            return;
        }

        synchronized (roomLock) {
            calledNumbers.add(nextBall);
        }

        // Broadcast to all players in the room
        broadcaster.ballDrawnBroadcast(room, nextBall);
        logger.debug("Room {} drew ball {}", roomId, nextBall);

    } catch (GameCompleteException ex) {
        logger.info("Game complete in room {}. Stopping number caller.", roomId);
        numberCallingStop();
    } catch (Exception ex) {
        // CRITICAL: log the exception; do NOT let it propagate silently
        logger.error("Unexpected error in number caller for room {}. " +
                     "Task will continue on next interval.", roomId, ex);
        // Alert operations team — this should not happen
        alertingService.alertSend(AlertSeverity.ERROR,
            "Number caller exception in room " + roomId, ex);
        // Do NOT re-throw: re-throwing would stop the scheduled task permanently
    }
}
```

---

## 9. Network Latency Strategies at Critical State Transition Junctures

**Definition and purpose**. A critical state transition juncture is any moment in a Bingo room where the canonical game state changes atomically and must be acknowledged consistently by SmartFox Server, the authoritative API, and all connected clients. Examples include the room start countdown, a ball draw broadcast, a daub validation, a BINGO win claim, and a reconnect state sync. In a real-time 2D Bingo room, these transitions must feel simultaneous to all players even though network latency is unavoidable. A ball draw may need to reach 200 players within the same fraction of a second, and a BINGO claim must be resolved before the next ball is drawn. Network latency — the time between a packet leaving one component and arriving at another — is an immutable physical reality; the system MUST therefore be designed to tolerate it without compromising fairness, canonical state integrity, or player confidence.

### 9.1 Failure Model: Split-Brain Windows at State Transitions

Unlike a REST call, a live Bingo room has multiple parties observing the same transition at the same time. If even one party is slow to acknowledge or process the transition, the system can enter a **split-brain window** in which different participants believe different states are current. Typical examples include:

- Player A has already transitioned to state `S2`, while Player B is still rendering `S1`.  
- SmartFox has broadcast a state change, but the authoritative API has not yet confirmed the corresponding validation result.  
- The client received the ball draw, but the daub acknowledgement timed out.

Illustrative state path:

```
WAITING ----------------------------> GAME_STARTED
GAME_STARTED --(ball drawn)---------> BALL_CALLED
BALL_CALLED --(player daubed)-------> CHECK_WIN
BALL_CALLED --(player claims BINGO)-> WIN_CLAIM_PENDING
WIN_CLAIM_PENDING --(validated)-----> GAME_ENDED
WIN_CLAIM_PENDING --(rejected)------> WIN_REJECTED

At each arrow the server emits an event. Due to latency:
- Client A (50 ms RTT) processes the event almost immediately.
- Client B (400 ms RTT) may process the same event 350 ms later.
- Result: Client B can still be rendering BALL_CALLED while the server has already moved to WIN_CLAIM_PENDING.
```

The standards in this section exist to keep these split-brain windows short, recoverable, and non-destructive.

### 9.2 Room-Wide Monotonic Sequencing Is Mandatory

Every canonical room state change MUST be tagged with a monotonically increasing `gameSequenceId`. This sequence ID is the authoritative ordering mechanism for real-time events. It MUST be incremented atomically on the server, scoped per room, and included on every state-bearing message. Clients use this sequence both to detect missed events and to order messages correctly even when packets arrive out of order. Payloads SHOULD also include a server-generated timestamp for diagnostics and telemetry.

Whether the payload field is named `seq` or `seqId`, the wire contract MUST be consistent within the implementation.

```java
public void ballDrawnBroadcast(Room room, int ballNumber) {
    BingoGameState state = getGameState(room);
    int seqId = state.incrementAndGetSequenceId();   // atomic, room-scoped

    ISFSObject msg = new SFSObject();
    msg.putInt("ball",      ballNumber);
    msg.putInt("seqId",     seqId);
    msg.putLong("serverTs", System.currentTimeMillis());

    getParentExtension().getApi().sendObjectMessage(room, msg, null);

    Logger.info("Ball broadcast: room={}, ball={}, seq={}", room.getId(), ballNumber, seqId);
}
```

Clients MUST track the last applied sequence ID. On receipt of any state message, the client MUST verify that `incomingSeqId == lastKnownSeqId + 1`. Any gap means the client may have missed one or more events and MUST immediately request a full state sync instead of attempting to guess the missing transition.

```java
private int _lastSeqId = -1;

private void OnBallDrawnReceived(ISFSObject data)
{
    int incomingSeqId = data.GetInt("seqId");
    if (incomingSeqId != _lastSeqId + 1)
    {
        Logger.Warn($"[GameSync] Sequence gap: expected {_lastSeqId + 1}, got {incomingSeqId}. Requesting sync.");
        RequestStateSyncFromServer();
        return;
    }

    _lastSeqId = incomingSeqId;
    ProcessBallDrawn(data.GetInt("ball"));
}
```

### 9.3 Transition-Specific Client Behaviour: Optimistic Where Safe, Confirm Where Necessary

Not all transitions should be handled the same way. Low-stakes, highly predictable UI changes may be optimistic. High-stakes transitions that alter the authoritative game outcome MUST wait for server confirmation.

| Transition | Canonical owner | Client strategy | Recovery on rejection or timeout |
|:-----------|:----------------|:----------------|:---------------------------------|
| Ball draw display | SmartFox broadcast | Show immediately on receipt; treat server broadcast as authoritative | If sequence gap is detected, request `SYNC_STATE` |
| Daub marking | SmartFox authoritative validation | Optimistic local mark, followed by server confirmation | Undo daub if rejected; apply `stateDelta` or full sync if sequence drift is detected |
| BINGO win claim | SmartFox + PHP validation | **Wait for confirmation**; show spinner or pending state only | Show invalid-claim toast or sync on timeout |
| Room state change (start/end) | Server-driven | Do not transition locally until the server message arrives | Sync if the expected transition does not arrive |
| Reconnect rendering | SmartFox snapshot | Do not render live game state until `SYNC_STATE` or reconnect snapshot is received | Fail reconnect and return player to a safe lobby flow if the snapshot cannot be obtained |

For player-initiated daubs, the client SHOULD apply the change immediately to remove perceived latency, but the server remains authoritative and MUST correct the client if validation fails or if the client is behind the room sequence.

```java
public void daubRequestProcess(User user, ISFSObject params) {
    int ballNumber  = params.getInt("ball");
    int clientSeqId = params.getInt("clientSeq");

    boolean isValidDaub = daubValidate(user, ballNumber);

    ISFSObject response = new SFSObject();
    response.putBool("accepted",  isValidDaub);
    response.putInt("ball",       ballNumber);
    response.putInt("serverSeq",  getGameState(user.getLastJoinedRoom()).getCurrentSequenceId());

    // If the server is ahead of the client, send correction data.
    if (needsCorrection(user, clientSeqId)) {
        response.putSFSObject("stateDelta", buildStateDelta(user, clientSeqId));
    }

    smartFox.send(new ObjectMessageRequest(response), user);
}
```

Illustrative client behaviour for a daub:

```java
MarkDaubLocally(cell);
SendDaub(ballNumber, _lastSeqId);

void OnDaubValidated(ISFSObject response)
{
    if (!response.GetBool("accepted"))
        UndoLocalDaub(cell);

    if (response.ContainsKey("stateDelta"))
        ApplyStateDelta(response.GetSFSObject("stateDelta"));

    _lastSeqId = response.GetInt("serverSeq");
}
```

### 9.4 Critical Transitions Must Be Time-Bounded on Both Client and Server

Every critical state transition MUST have an explicit timeout budget. The server timeout prevents the room from freezing. The client timeout prevents the player from becoming stuck in an indefinite loading state.

For BINGO claims specifically:

- The server MUST enforce a validation timeout when waiting on PHP or any downstream dependency.  
- The client MUST stop waiting after a defined interval and recover by requesting a state sync.  
- SmartFox MUST use `asynchronous` PHP/API calls with an explicit timeout. It MUST NOT block a SmartFox thread while waiting for validation.

Illustrative win-claim flow:

```
Client                  SmartFox Server                  authoritative API
  | CLAIM_BINGO                |                            |
  |--------------------------->|                            |
  | show spinner               | set state=WIN_CLAIM_PENDING|
  |                            | async validate ----------->|
  |                            |<----------- valid/invalid -|
  |<---- WIN_VALIDATED / WIN_REJECTED broadcast ------------|
  | hide spinner / render outcome                           |

Recovery paths:
- If client timeout elapses first: client requests SYNC_STATE.
- If server/PHP timeout elapses first: server rejects with VALIDATION_TIMEOUT and resumes the game.
```
Server-side example:

```java
private static final long CLAIM_VALIDATION_TIMEOUT_MS = 5_000;

private ScheduledFuture<?> claimTimeoutSchedule(Room room, User claimant) {
    return scheduler.schedule(() -> {
        synchronized (getGameState(room)) {
            if (getGameState(room).getState() == BINGO_CLAIM_PENDING) {
                Logger.warn("Claim validation timed out. Rejecting. room={}, user={}",
                    room.getId(), claimant.getId());
                rejectClaim(room, claimant, ClaimRejectionReason.VALIDATION_TIMEOUT);
                advanceToNextBall(room);
            }
        }
    }, CLAIM_VALIDATION_TIMEOUT_MS, TimeUnit.MILLISECONDS);
}
```

Client-side example:

```c#
private CancellationTokenSource _winClaimCts;
private const float WIN_CLAIM_TIMEOUT_SEC = 10.0f;

private async UniTaskVoid SubmitWinClaimAsync()
{
    _winClaimCts = new CancellationTokenSource();
    _winClaimButton.interactable = false;
    ShowLoadingSpinner();

    try {
        _sfxExtension.SendClaimBingo(_currentCard);

        GameEvent result = await _gameEventBus
            .WaitForEventAsync(GameEventType.WinValidated | GameEventType.WinRejected,
                               _winClaimCts.Token)
            .TimeoutAsync(TimeSpan.FromSeconds(WIN_CLAIM_TIMEOUT_SEC));

        HandleWinClaimResult(result);
    }
    catch (TimeoutException) {
        Logger.Warn("[WinClaim] Timeout waiting for server confirmation. Requesting state sync.");
        ShowToast("Network issue — please check your connection.");
        RequestStateSyncFromServer();
    }
    catch (OperationCanceledException) { }
    finally {
        HideLoadingSpinner();
        _winClaimButton.interactable = true;
        _winClaimCts?.Dispose();
    }
}
```

### 9.5 Reconnects Must Use Full State Snapshots, Not Event Replay

When a client reconnects mid-game, it may have missed multiple transitions. The server MUST provide a complete, current snapshot of the room state. It MUST NOT attempt to replay a long list of missed events and expect the client to reconstruct state from history.

At a minimum, the reconnect snapshot SHOULD contain:

- the current room sequence ID,  
- the called balls,  
- the current game state,  
- the timestamp at which the current state was entered, and  
- the reconnecting player's daubed positions.

```java
public void reconnectRequestProcess(User user, ISFSObject params) {
    Room room = reconnectingPlayerRoomFind(user, params.getInt("roomId"));
    if (room == null) {
        reconnectFailedSend(user, "ROOM_NOT_FOUND");
        return;
    }

    BingoGameState state = getGameState(room);
    ISFSObject snapshot  = new SFSObject();

    snapshot.putInt("currentSeq", state.getCurrentSequenceId());
    snapshot.putIntArray("calledBalls", state.getCalledBallsArray());
    snapshot.putUtfString("gameState", state.getState().name());
    snapshot.putLong("stateEnteredAt", state.getStateEnteredAt().toEpochMilli());

    int[] daubedPositions = state.getDaubedPositions(user.getId());
    snapshot.putIntArray("daubedPositions", daubedPositions);

    user.setProperty(PROP_RECONNECTED, true);
    smartFox.send(new ObjectMessageRequest(snapshot, SFS2X_OBJECT_RECONNECT_STATE), user);

    Logger.info("Reconnect snapshot sent: user={}, seq={}, state={}",
        user.getId(), state.getCurrentSequenceId(), state.getState());
}
```

A reconnecting client MUST wait for this snapshot before rendering the live game UI again.

### 9.6 Duplicate Transition Messages Must Be Idempotent

Under high latency, retransmission is normal. Clients may resend a transition request because the acknowledgement has not arrived yet, even though the server is already processing it. The system MUST therefore treat duplicate transition messages as expected rather than exceptional.

Requirements:

- SmartFox-side sequence handling MUST tolerate duplicate client messages without double-applying the state transition.  
- For high-stakes transitions such as win claims and room joins, the authoritative API MUST also enforce idempotency at the persistence layer so that concurrent retries cannot double-process a claim.  
- Duplicate detection MUST preserve correctness first; it is better to return the already-known outcome than to process the same transition twice.

### 9.7 High-Frequency Ball Draws Should Use a Jitter Buffer

During fast game modes with a short ball-call interval, ball draw messages may arrive in bursts after a brief network interruption. The client SHOULD use a jitter buffer — a sequence-ordered queue — to smooth burst delivery and present ball draws at the configured display interval instead of at raw arrival time.

```java
private readonly SortedList<int, BallDrawMessage> _jitterBuffer = new SortedList<int, BallDrawMessage>();
private const float BALL_DRAW_DISPLAY_INTERVAL_SEC = 3.0f;

private void OnBallDrawReceived(BallDrawMessage msg) {
    _jitterBuffer[msg.SequenceId] = msg;
    if (!_isProcessingBuffer) StartCoroutine(DrainJitterBufferCoroutine());
}

private IEnumerator DrainJitterBufferCoroutine() {
    _isProcessingBuffer = true;
    while (_jitterBuffer.Count > 0) {
        var (seqId, msg) = _jitterBuffer.First();
        _jitterBuffer.RemoveAt(0);
        DisplayBallDraw(msg.BallNumber);
        yield return new WaitForSeconds(BALL_DRAW_DISPLAY_INTERVAL_SEC);
    }
    _isProcessingBuffer = false;
}
```

In degraded mode, the jitter buffer window SHOULD be increased so the client can absorb short bursts without visually fast-forwarding the room.

### 9.8 Heartbeats, RTT Monitoring, and Degraded Mode Are Required Operational Controls

SmartFox MUST actively monitor per-player round-trip time (RTT) and stale connections before they become visible gameplay defects. At minimum, the room should ping each player periodically and track missed responses.

```java
private static final long HEARTBEAT_INTERVAL_MS = 10_000;
private static final int  HEARTBEAT_MISSED_COUNT_MAX = 3;

private final ConcurrentHashMap<Integer, Integer> missedHeartbeats = new ConcurrentHashMap<>();

private void heartbeatSend(User user) {
    ISFSObject ping = new SFSObject();
    ping.putLong("serverTs", Instant.now().toEpochMilli());
    smartFox.send(new ObjectMessageRequest(ping, SFS2X_PING), user);
    missedHeartbeats.merge(user.getId(), 1, Integer::sum);
}

public void heartbeatResponseProcess(User user, ISFSObject params) {
    missedHeartbeats.put(user.getId(), 0);
    long rttMs = Instant.now().toEpochMilli() - params.getLong("serverTs");

    metricsService.recordGauge("sfs.player.rtt_ms", rttMs,
        Map.of("userId", String.valueOf(user.getId())));

    if (rttMs > 800) {
        Logger.warn("High latency player: user={}, rtt={}ms", user.getId(), rttMs);
    }
}
```

Operational behaviour:

- Ping each player every 10 seconds.  
- Drop the connection after 3 missed heartbeat responses.  
- Emit RTT telemetry for each player.  
- Log a high-latency warning when an RTT sample exceeds 800 ms.  
- If SmartFox RTT exceeds 500 ms over 10 consecutive messages, the client MUST enter **degraded mode**.

In degraded mode, the client SHOULD:

- display a persistent **Poor connection** indicator,  
- increase the jitter buffer window,  
- suppress optimistic UI updates and require server confirmation for state changes,  
- increase the default win-claim timeout from 10 seconds to 20 seconds, and  
- continue logging latency telemetry for operational monitoring.

### 9.9 Graceful Degradation Rules at Critical Junctures

When latency exceeds safe limits during a critical transition, the system MUST degrade gracefully instead of stalling or silently diverging.

| Scenario | Threshold | Required degraded behaviour |
|:---------|:----------|:----------------------------|
| BINGO claim validation via PHP/API | > 5 seconds | Reject the claim with `VALIDATION_TIMEOUT`; resume the game |
| Ball draw broadcast confirmation | > 3 seconds | Re-broadcast the same ball; do not advance the sequence | 
| Room join or reconnect during an active game | > 10 seconds | Allow rejoin only after a full state sync is delivered |
| SmartFox RTT sustained above 500 ms | 10 consecutive messages | Enter degraded mode on the client |
| Single-player RTT sample above 800 ms | Immediate sample breach | Log and surface high-latency telemetry |
| Player RTT sustained above 1500 ms | 30 seconds | Warn the player; if the condition persists to 60 seconds, disconnect and mark inactive |

These thresholds are intended to keep the room moving forward while preserving canonical correctness.

### 9.10 Anti-Patterns to Avoid

The following behaviours are prohibited because they turn normal latency into correctness bugs:

- **Trusting client timestamps** for event ordering. Ordering MUST be based on server sequence IDs and, where needed, server timestamps.  
- **Replaying all missed events on reconnect**. Reconnect recovery MUST be snapshot-based.  
- **Blocking a SmartFox thread while waiting for PHP validation**. Use asynchronous HTTP/API calls with explicit timeouts.  
- **Silently ignoring sequence gaps**. A gap MUST trigger `SYNC_STATE` or equivalent full resynchronisation.  
- **Showing a win screen before authoritative validation**. BINGO wins MUST wait for server or PHP confirmation.  
- **Advancing room state without broadcasting the current state to all live players and satisfying the room's confirmation policy**. Do not skip or collapse canonical transitions.  
- **Treating duplicate transition requests as exceptional failures**. Retries are normal under latency and MUST be handled idempotently.

### 9.11 Minimum Implementation Checklist

A room implementation satisfies this standard only if all of the following are true:

- Every canonical state message carries a room-scoped monotonic `gameSequenceId`.  
- Clients perform gap detection and request full sync on any missing sequence.  
- Daubs may be optimistic, but wins are wait-for-confirmation.  
- Critical transitions have both server-side and client-side timeout recovery.  
- Reconnect uses a full snapshot, not event replay.  
- Duplicate transition requests are idempotent across SmartFox and PHP.  
- Heartbeats and RTT telemetry are enabled.  
- Degraded mode exists and changes client behaviour under sustained latency.  
- Ball draws in fast modes use a jitter buffer or equivalent smoothing strategy.

### 9.12 Protocol Versioning and Mixed-Client Compatibility

SmartFox rooms will inevitably contain clients on slightly different builds during rollout windows. Real-time message contracts must therefore be additive and version-aware. Every request/response family must include either an explicit protocol version or a capability set negotiated at join/reconnect time.

Rules:

- Add fields; do not remove or repurpose existing fields during an active rollout.
- Older clients must ignore unknown fields safely.
- New handlers must tolerate absent optional fields from older clients.
- Behavior changes must be gated by explicit capability flags from login/join, not fragile version-string checks scattered through handlers.
- Breaking protocol removals require a deprecation window aligned with [ESTD4 §4.5 HTTP Status Codes](./ESTD4_-_Server_Engg_Standards.md#45-http-status-codes) and a controlled unsupported-client rejection path.

---

## 10. Authoritative API Communication from SmartFox

SmartFox-to-authoritative-API calls must use an HTTP client configured with explicit connect and read timeouts. Calls that exceed the timeout must fail fast rather than holding a room handler thread indefinitely. The authoritative API may be the legacy PHP monolith for the classic game or the Java/SEAM API for the new game.

### 10.1 HTTP Client Configuration

```java
@Singleton
public class GameApiClient {

    private final HttpClient httpClient;
    private final String apiBaseUrl;
    private final String internalApiSecret;

    public GameApiClient(String apiBaseUrl, String internalApiSecret) {
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(3))
            .executor(Executors.newFixedThreadPool(
                configService.getInt("api.http_pool_size", 20),
                new NamedThreadFactory("game-api-client")
            ))
            .build();
        this.apiBaseUrl = apiBaseUrl;
        this.internalApiSecret = internalApiSecret;
    }

    public WinValidationResult winValidate(WinClaimSnapshot snapshot) throws ApiCallException {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(apiBaseUrl + "/internal/v1/room/validate-win"))
            .header("Content-Type", "application/json")
            .header("X-Internal-Secret", internalApiSecret)
            .header("X-Request-Id", UUID.randomUUID().toString())
            .POST(HttpRequest.BodyPublishers.ofString(JsonSerializer.toJson(snapshot)))
            .timeout(Duration.ofSeconds(5))
            .build();

        try {
            HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());
            if (response.statusCode() != 200) {
                throw new ApiCallException("Win validation returned HTTP " + response.statusCode());
            }
            return JsonSerializer.fromJson(response.body(), WinValidationResult.class);
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
            throw new ApiCallException("Win validation HTTP call interrupted", ex);
        } catch (IOException ex) {
            throw new ApiCallException("Win validation HTTP call failed", ex);
        }
    }
}
```

### 10.2 Retry and Fallback Policy

Authoritative API calls from SmartFox must implement a limited retry policy for transient failures only:

- Retry on: network timeout, HTTP 503, HTTP 429.
- Do not retry on: HTTP 4xx business or validation errors.
- Maximum 2 retries with 500 ms delay between attempts.
- If all retries fail, the room must enter a `DEGRADED` state that prevents new win claims until the authoritative API is reachable again.

---

## 11. Player Presence and Session Management

### 11.1 Player Join Validation

When a player attempts to join a room, SmartFox must validate with the authoritative API that the player is eligible (has sufficient coins, is not banned, meets room requirements) before completing the join. SmartFox must not simply trust the client's claim that the player is eligible.

### 11.2 Player Disconnect Handling

When a player disconnects, SmartFox must:

- Mark the player as disconnected but retain their game state (card, daub history) for the reconnect window.  
- After the reconnect window expires (configurable, default 120 seconds), notify the room that the player has permanently left.  
- If the disconnected player is the last player in the room, begin room shutdown after the reconnect window.

### 11.3 Reconnect State Sync

When a player reconnects within the reconnect window, SmartFox must send them the full current game state in a single `SYNC_STATE` message: all called balls, the current state of their card, the current room state, and any game outcomes from rounds they missed while disconnected. The client must be able to render any valid game state from this message alone, with no prior state assumed.

---

## 12. SmartFox Security Vulnerabilities

| Vulnerability | What It Looks Like in Our Environment | Required Controls |
|:--------------|:--------------------------------------|:------------------|
| **Message flooding / handler DoS** | A client sends excessive command traffic and consumes handler threads, CPU, or room locks | Rate-limit per player and per room command type; drop abusive traffic early; alert on command-rate anomalies |
| **Invalid state injection** | A client attempts actions such as DAUB, START, or CLAIM_BINGO when the room is not in the required state | Validate room state before processing any command; never let the client define the authoritative transition |
| **Win claim forgery** | A client submits a fabricated or locally altered card state and claims a win | SmartFox must validate the room and card state before processing the command |
| **Session impersonation / token replay** | A stolen or replayed session token is used to connect to SmartFox or join a room illegitimately | Validate tokens against the authoritative API on join and reconnect; keep token TTLs short; bind session rules to player identity |
| **Room namespace collision / unauthorized join** | Attackers guess or manipulate room identifiers to join rooms they do not own or should not access | Room membership must be validated server-side; room IDs are not authorization; deny joins that do not pass authoritative checks |
| **Duplicate or out-of-order command processing** | Retries, lag, or malicious resends produce repeated transitions or stale messages that re-open closed actions | Use monotonic sequence IDs, idempotent command handling, and bounded replay windows |
| **Protocol/version skew bypass** | Older or alternate client builds hit weaker validation paths or omit newer integrity checks | Maintain explicit protocol versioning, mixed-client compatibility rules, and consistent security enforcement across versions |
| **Connection flood / slot exhaustion** | Bots open large numbers of TCP connections and exhaust SmartFox capacity before normal players can join | Apply connection quotas, per-IP limits, front-door protections, and capacity alarms on connection counts |

---

## 13. Logging in SmartFox

All [ESTD1 §12. Logging](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#12-logging) and [ESTD7 §8. Application Layer Standards](./ESTD7_-_Java_Programming_Standards.md#8-application-layer-standards) logging rules apply. SmartFox-specific additions:

Use SLF4J with Logback (per [ESTD7 §8.5 Logging](./ESTD7_-_Java_Programming_Standards.md#85-logging)). Use MDC (Mapped Diagnostic Context) to enrich all log statements within a handler with the room ID, user ID, and correlation ID so that a single grep on a correlation ID retrieves the entire trace for one player action.

```java
public void handleRequest(User user, ISFSObject params, Room room) {
    MDC.put("roomId", String.valueOf(room.getId()));
    MDC.put("userId", String.valueOf(user.getId()));
    MDC.put("correlationId", UUID.randomUUID().toString());
    try {
        requestProcess(user, params, room);
    } finally {
        MDC.clear(); // ALWAYS clear MDC — SFS reuses threads from its pool
    }
}
```

---

## 14. Idempotency in SmartFox

SmartFox must protect against duplicate client messages that can arrive during reconnect scenarios (the client may resend a message it sent before disconnecting, not knowing whether the server received it).

### 14.1 Sequence ID-Based Idempotency

Each client message must include a monotonically increasing sequence ID per player session. The server maintains the last processed sequence ID per player per room. Duplicate messages (same or lower sequence ID) are silently discarded.

```java
public class DaubHandler implements IClientRequestHandler {
    @Override
    public void handleRequest(User user, ISFSObject params, Room room) {
        int seqId = params.getInt("seqId");
        PlayerSession session = sessionManager.getSession(user.getId(), room.getId());

        if (seqId <= session.getLastProcessedSeqId()) {
            logger.debug("Duplicate daub from user {} seq {}. Discarding.", user.getId(), seqId);
            return; // Idempotent: already processed
        }

        // Process the daub...
        session.setLastProcessedSeqId(seqId);
    }
}
```

---

## 15. Graceful Shutdown and Restart

A SmartFox restart with no warning terminates all active connections and loses all in-memory room state. For players in the middle of a Bingo game, this appears as a complete game freeze followed by disconnection — one of the worst possible player experiences. Graceful shutdown eliminates this.

### 15.1 Graceful Shutdown Sequence

```
1. Set server to "draining" state: reject new room join requests.
2. Broadcast MAINTENANCE_WARNING to all active rooms:
   "Server maintenance in X minutes. Please finish your current game."
3. Wait for active games to complete naturally (up to configuredDrainWindowMinutes).
4. After the drain window: force-close remaining rooms gracefully:
   a. Record current game state to the database.
   b. Send ROOM_CLOSED to all players with a "Server maintenance" reason.
5. Close all player connections.
6. Shut down the JVM.
```

This sequence must be triggered by sending a specific administrative command to SmartFox (via the admin API or a JMX signal), not by killing the process directly.

### 15.2 State Recovery on Startup

On startup, SmartFox must check the database for any rooms that were in an active state at the time of the last shutdown (detected by rooms with state `GAME_IN_PROGRESS` and a recent `last_heartbeat_at` timestamp). These rooms must be marked as `INTERRUPTED` and clients attempting to reconnect to them must receive a `ROOM_INTERRUPTED` message with instructions to re-enter matchmaking.

---

## 16. Health Monitoring and Metrics

### 16.1 Health Check Endpoint

SmartFox must expose a health check endpoint accessible to the NLB target group health check. The health check must respond within 1 second and must report:

```
GET /health
```

```json
{
  "status": "healthy",
  "activeRooms": 42,
  "activePlayers": 1230,
  "jvmHeapUsedMb": 1240,
  "jvmHeapMaxMb": 8192,
  "phpApiReachable": true,
  "uptimeSeconds": 86400
}
```

The health check must return HTTP 503 if: `phpApiReachable` is false, heap usage exceeds 90% of max, or the room count exceeds the configured capacity soft limit.

### 16.2 Custom Metrics (Datadog)

Publish the following custom metrics to Datadog every 30 seconds:

| Metric | Type | Description |
|:-------|:-----|:------------|
| `sfs.rooms.active` | Gauge | Number of active game rooms |
| `sfs.players.connected` | Gauge | Number of connected players | 
| `sfs.players.reconnecting` | Gauge | Players in the reconnect window |
| `sfs.message.latency` | Histogram | Time from message receipt to handler completion |
| `sfs.api.call.duration` | Histogram | authoritative API call duration |
| `sfs.jvm.heap.used` | Gauge | JVM heap used in MB | 
| `sfs.jvm.gc.pause` | Histogram | GC pause duration |

---

## 17. JVM Tuning for SmartFox

SmartFox is a long-running JVM process. GC pauses are directly felt by players as latency spikes in ball draw broadcasts. The following JVM flags are the starting baseline for production and must be tuned based on load testing results.

```
java \
  -Xms4g -Xmx8g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=100 \
  -XX:G1HeapRegionSize=16m \
  -XX:+UseStringDeduplication \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/log/sfs/heapdump.hprof \
  -Xlog:gc*:file=/var/log/sfs/gc.log:time,uptime:filecount=5,filesize=50m \
  -XX:+StartFlightRecording=duration=continuous,filename=/var/log/sfs/flight.jfr \
  -jar smartfox-server.jar
```

Key parameters to tune through load testing: -Xmx (max heap should be set so heap usage under peak load stays below 75% of max), -XX:MaxGCPauseMillis (increase if GC is running too frequently; decrease if individual pauses are causing latency spikes).

---

## 18. Memory Management and Object Lifecycle

### 18.1 Room Lifecycle Corresponds to Memory Lifecycle

When a room is closed, all references to its objects must be explicitly released. The most common SmartFox memory leak pattern is leaving room objects in the `activeRooms` registry after the room has ended.

```java
// Pattern: always remove from registry, then clean up
public void roomRemovedProcess(BaseEvent event) {
    Room sfsRoom = (Room) event.getParameter(SFSEventParam.ROOM);
    BingoRoom bingoRoom = activeRooms.remove(sfsRoom.getId()); // Remove from registry
    if (bingoRoom != null) {
        bingoRoom.cleanup(); // Release all references inside the BingoRoom
    }
}
```

### 18.2 Event Listener Cleanup

SmartFox uses an event listener model for server events (room created, player joined, player disconnected). Listeners registered at extension init must be explicitly deregistered at extension destroy.

```java
@Override
public void init() {
    addEventHandler(SFSEventType.USER_DISCONNECT, this::onUserDisconnect);
    addEventHandler(SFSEventType.ROOM_REMOVED,    this::roomRemovedProcess);
}

@Override
public void destroy() {
    // SmartFox calls destroy() before shutting down the extension
    // All clean-up logic goes here
    activeRooms.forEach((id, room) -> room.cleanup());
    activeRooms.clear();
    logger.info("BingoGameExtension destroyed. All rooms cleaned up.");
}
```

### 18.3 The Five Most Common SmartFox Memory Leak Patterns

**Pattern 1: Orphaned game state after game end**

```java
// BAD — game ends but state object remains in registry
public void onGameEnded(BingoGameState state) {
    state.setEnded(true);
    // LEAK: gameStates map still holds a reference to this state
}

// GOOD — remove from all registries on game end
public void gameEndedProcess(BingoGameState state) {
    int roomId = state.getRoomId();
    gameStates.remove(roomId);
    List<ScheduledFuture<?>> tasks = scheduledTasks.remove(roomId);
    if (tasks != null) tasks.forEach(f -> f.cancel(false));
    state.clear();   // Null out all internal references
    Logger.info("Game state cleaned up for room {}", roomId);
}
```

**Pattern 2: Scheduled task not cancelled on room removal**

```java
// Every ScheduledFuture must be cancelled when the room closes.
// Uncancelled tasks hold a reference to the room state and fire after the room is gone.
public void roomRemovedProcess(BaseEvent event) {
    Room sfsRoom = (Room) event.getParameter(SFSEventParam.ROOM);
    int  roomId  = sfsRoom.getId();
    List<ScheduledFuture<?>> tasks = scheduledTasks.remove(roomId);
    if (tasks != null) tasks.forEach(f -> f.cancel(false));  // Cancel BEFORE removing state
    BingoRoom bingoRoom = activeRooms.remove(roomId);
    if (bingoRoom != null) bingoRoom.cleanup();
}
```

**Pattern 3: Event listener not deregistered on extension reload**

```java
@Override
public void destroy() {
    // Must deregister ALL event listeners to prevent accumulation on reload
    getParentZone().removeEventListener(SFSEventType.USER_JOIN_ROOM,   this);
    getParentZone().removeEventListener(SFSEventType.USER_LEAVE_ROOM,  this);
    getParentZone().removeEventListener(SFSEventType.ROOM_REMOVED,     this);
    activeRooms.forEach((id, room) -> room.cleanup());
    activeRooms.clear();
    super.destroy();
    Logger.info("BingoGameExtension destroyed — all listeners removed.");
}
```

**Pattern 4: Player state not cleaned up on disconnect/game end**

```java
public void userDisconnectProcess(User user) {
    for (BingoRoom room : activeRooms.values()) {
        room.playerRemove(user.getId());
        room.operationsPendingCancel(user.getId());
    }
    playerSessions.remove(user.getId());
    Logger.info("Player {} disconnected and cleaned up.", user.getId());
}
```

**Pattern 5: String interning of dynamic values**

```java
// BAD — fills the JVM string pool permanently; cannot be GC'd
String key = (userId + ":" + roomId).intern();

// GOOD — regular string; eligible for GC when no longer referenced
String key = userId + ":" + roomId;
```

### 18.4 JVM Garbage Collection Tuning

SmartFox is a long-running JVM process. Configure G1GC for low-pause collection to avoid stop-the-world pauses during active game events:

```
-Xms4g -Xmx8g                           # Fixed heap size — avoid resize pauses
-XX:+UseG1GC                             # G1GC: low-pause for large heaps
-XX:MaxGCPauseMillis=100                 # Target: max 100ms GC pause
-XX:G1HeapRegionSize=16m                # Larger regions for game-sized objects
-XX:+HeapDumpOnOutOfMemoryError         # Auto heap dump on OOM for post-mortem
-XX:HeapDumpPath=/var/log/smartfox/
-Xlog:gc*:file=/var/log/smartfox/gc.log:time,uptime:filecount=5,filesize=20m
```

### 18.5 Memory Monitoring

Monitor heap usage as a Datadog Gauge ([ESTD4 §16.1 Minimum Required Metrics (Datadog)](./ESTD4_-_Server_Engg_Standards.md#161-minimum-required-metrics-datadog)):

```
jvm.heap_memory.used       → current heap bytes used
jvm.non_heap_memory.used   → metaspace, code cache
jvm.gc.pause_time          → GC pause duration histogram
```

Alert: `jvm.heap_memory.used > 85% of jvm.heap_memory.max` sustained for > 5 minutes → page on-call. Review the 7-day heap usage trend in Datadog weekly.

---

## 19. Memory Leak Prevention in SmartFox Extensions

**Definition**: A *memory leak* in the SmartFox context is a condition where Java objects that are no longer needed remain reachable (referenced by at least one live object) and thus cannot be garbage collected by the JVM, causing heap usage to grow over time until OOM kills the JVM process.

SmartFox memory leaks are operationally catastrophic: the process must be restarted, disrupting all active game rooms. Identifying and preventing leak sources is critical for a long-running stateful server.

### 19.1 Primary Sources of Memory Leaks in SmartFox Extensions

| Leak Source | Description | Fix |
|:------------|:------------|:----|
| **Room not removed from registry after close** | `activeRooms.put(roomId, room)` without matching `activeRooms.remove(roomId)` | Always `remove(roomId)` in the room termination handler ([§18.1 Room Lifecycle Corresponds to Memory Lifecycle](#181-room-lifecycle-corresponds-to-memory-lifecycle)) |
| **Registered SFS event listeners not removed at** `destroy()` | SmartFox's event system holds a strong reference to the listener | Remove all listeners in `destroy()` ([ESTD4 §16.1 Minimum Required Metrics (Datadog)](./ESTD4_-_Server_Engg_Standards.md#161-minimum-required-metrics-datadog)) |
| **Scheduled tasks not cancelled on room close** | `ScheduledFuture` references the task closure; task closure references the room | Always `future.cancel(false)` in `room.cleanup()` ([§6.3 Room Cleanup](#63-room-cleanup)) | 
| **ScheduledExecutorService not shut down** | Each room creates its own `ScheduledExecutorService`; not calling `shutdown()` leaks thread pool threads | `scheduler.shutdown()` in `numberCallingStop()` ([§8.1 Using ScheduledExecutorService](#81-using-scheduledexecutorservice)) |
| **authoritative API HTTP client thread pool per-room** | Creating a new `HttpClient` per room or per request leaks thread pool threads | Use a singleton `GameApiClient` shared across all rooms ([§10.1 HTTP Client Configuration](#101-http-client-configuration)) |
| **MDC not cleared after handler** | MDC is stored in a `ThreadLocal`; not clearing it causes the map to hold references on reused threads | `MDC.clear()` in a `finally` block in every handler ([§13. Logging in SmartFox](#13-logging-in-smartfox)) |
| **Player card state not cleared on room close** | `cardStates` map populated during the game and never cleared after `GAME_COMPLETE` | `cardStates.clear()` in `room.cleanup()` |
| **Static `ConcurrentHashMap` grown without eviction** | Room-level caches or session maps stored in static fields and never evicted | Never use static mutable collections in SmartFox extensions; use room-scoped instances |
| **String keys in ISFSObject not interned** | High-frequency message construction with repeated equal strings creates many short-lived String objects | Use `String.intern()` for frequently-used SFSObject field names |
| **Unclosed JDBC `ResultSet` or `Connection`** | Any DAO that opens a DB connection without using try-with-resources leaks connection pool slots | Always use try-with-resources for JDBC resources |


### 19.2 Heap Monitoring and Leak Detection

Configure JVM heap monitoring to alert before OOM:

```
# Alert when heap exceeds 80% of max — visible in §14.1 Datadog metric sfs.jvm.heap.used
```

**Detection steps when heap grows unexpectedly:**

1. Capture a heap dump: `jcmd <pid> GC.heap_dump /var/log/sfs/heap_$(date +%s).hprof`
2. Analyse with VisualVM or Eclipse MAT (Memory Analyzer Tool): identify the **dominator tree** — the objects retaining the most memory.  
3. Look for `BingoRoom`, `BingoGameEngine`, `HashMap`, or `ConcurrentHashMap` instances whose count grows with room creation and does not shrink after room close — this is the classic registry-not-cleared leak.  
4. Look for `SFSEventHandlerEntry` objects accumulating — this is the listener-not-removed leak.

```java
// Add to health endpoint for operational visibility
public MemoryStats memoryStatsGet() {
    Runtime rt = Runtime.getRuntime();
    return new MemoryStats(
        activeRooms.size(),                          // Should shrink after games end
        activePlayers.size(),                        // Should track connected count
        (rt.totalMemory() - rt.freeMemory()) / (1024 * 1024), // Used heap MB
        rt.maxMemory() / (1024 * 1024)              // Max heap MB
    );
}
```

### 19.3 Memory Leak Prevention Checklist

Before every SmartFox extension release, the following must be verified:

- [ ] Every `activeRooms.put(id, room)` has a corresponding `activeRooms.remove(id)` in the termination handler.  
- [ ] Every `addEventHandler(type, handler)` in `init()` has a corresponding `removeEventHandler(type, handler)` in `destroy()`.  
- [ ] Every `ScheduledFuture` is stored and cancelled in `room.cleanup()`.  
- [ ] Every `ScheduledExecutorService` is shut down in `numberCallingStop()`.  
- [ ] `GameApiClient` is a singleton — not instantiated per room.  
- [ ] `MDC.clear()` appears in a `finally` block in every handler `handleRequest` method.  
- [ ] A 30-minute soak test shows no heap growth beyond the initial stable level after N rooms complete.  
- [ ] The `sfs.jvm.heap.used` Datadog metric is reviewed for the soak test session and shows a stable or decreasing sawtooth pattern (GC collecting, not growing to max).

---

## 20. Testing SmartFox Extensions

SmartFox extensions can be tested without a running SmartFox instance if the design follows the abstraction principles in [§5. SmartFox Data Abstraction](#5-smartfox-data-abstraction): game engine logic must be in plain Java classes with no SmartFox dependency, and SmartFox types are injected only at the handler boundary.

### 20.1 Testing the Game Engine in Isolation

```java
@ExtendWith(MockitoExtension.class)
class BingoGameEngineTest {

    @Mock private GameApiClient gameApiClient;
    @Mock private RoomEventBroadcaster broadcaster;
    @InjectMocks private BingoGameEngine gameEngine;

    @Test
    void daubProcess_whenBallNotCalled_throwsInvalidMoveException() {
        // Arrange — ball 99 has not been called
        int userId = 100;
        gameEngine.registerPlayerCard(userId, BingoCardFixture.aCard());

        // Act & Assert
        assertThatThrownBy(() -> gameEngine.daubProcess(userId, 99))
            .isInstanceOf(InvalidMoveException.class)
            .hasMessageContaining("Ball 99 has not been called");
    }

    @Test
    void bingoClaim_withValidFullHouseAndApiConfirmation_returnsValidResult() {
        // Arrange
        int userId = 100;
        BingoCard fullHouseCard = BingoCardFixture.aCardWithAllNumbersCalled();
        gameEngine.registerPlayerCard(userId, fullHouseCard);
        gameEngine.ballsCalledMarkAll(fullHouseCard.getNumbers());

        when(gameApiClient.winValidate(any())).thenReturn(WinValidationResult.valid(500));

        // Act
        BingoClaimResult result = gameEngine.bingoClaim(userId, ROOM_ID, WinPattern.FULL_HOUSE);

        // Assert
        assertThat(result.isValid()).isTrue();
        assertThat(result.coinsAwarded()).isEqualTo(500);
        verify(broadcaster).winBroadcast(userId, WinPattern.FULL_HOUSE);
    }
}
```

### 20.2 Win Pattern Test Coverage

Win detection is a critical correctness requirement. A parameterized test suite must cover every supported win pattern, boundary conditions (single line vs full house), invalid claims (pattern not completed), and duplicate win claims.

```java
@ParameterizedTest
@MethodSource("winPatternTestCases")
void winPatternCheck(int[] daubed, WinPattern pattern, boolean expected) {
    assertThat(WinChecker.check(daubed, pattern)).isEqualTo(expected);
}

static Stream<Arguments> winPatternTestCases() {
    return Stream.of(
        Arguments.of(ROW_1_DAUBED, WinPattern.TOP_ROW, true),
        Arguments.of(ROW_1_DAUBED, WinPattern.FULL_HOUSE, false),
        Arguments.of(FULL_CARD_DAUBED, WinPattern.FULL_HOUSE, true),
        Arguments.of(EMPTY_CARD, WinPattern.TOP_ROW, false),
        Arguments.of(FOUR_CORNERS_DAUBED, WinPattern.FOUR_CORNERS, true)
    );
}
```

---

## 21. Common Pitfalls to Avoid

| # | Pitfall | Impact | Remedy | 
|:--|:--------|:-------|:-------|
| 1 | Uncaught exception in `ScheduledExecutorService` task | Task silently stops; no more balls called | Always wrap scheduled task body in `try-catch(Exception)` | 
| 2 | `ConcurrentModificationException` iterating player list | Crash mid-game when iterating during join/leave | Use `ConcurrentHashMap`, `CopyOnWriteArrayList` | 
| 3 | Static mutable state shared across rooms | Race conditions; one room's bug corrupts another | Use room-scoped instance fields, not static |
| 4 | Holding lock during authoritative API HTTP call | Room operations block for 2–5 seconds | Release lock before I/O; re-acquire after |
| 5 | Not removing room from registry after room ends | Memory leak; room registry grows indefinitely | Always `activeRooms.remove(roomId)` in termination handler |
| 6 | Not clearing MDC after handler returns | Subsequent request on same thread has wrong player context | Always clear MDC in a `finally` block |
| 7 | Using `==` for String comparison in command routing | Command routing always fails for some commands | Use `.equals()` for Strings; enums safely use `==` | 
| 8 | No reconnect state preservation | Player loses all card state on disconnect | Keep player card state for the full reconnect window | 
| 9 | Calling SmartFox API from a non-SFS thread | Thread-safety violation; unpredictable behavior | Only call SmartFox APIs from SFS event handler threads |
| 10 | Killing the process to restart SmartFox | Active games lost with no warning to players | Always use the graceful shutdown sequence ([§15.1 Graceful Shutdown Sequence](#151-graceful-shutdown-sequence)) |
| 11 | Hardcoded number call interval | Cannot tune timing without a code change and redeploy | Read interval from configuration at startup | 
| 12 | Accepting game state changes after room is CLOSED | Ghost updates to dead rooms | Check room state before processing any handler |
