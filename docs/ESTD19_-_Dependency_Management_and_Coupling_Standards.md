# ESTD19 - Dependency Management and Coupling Standards

**ESTD19 — Dependency Management and Coupling Standards**

| Field | Value |
|:----- |:------|
| Document ID | ESTD19 |
| Version | 1.0 |
| Status | Draft |
| Last Updated | 2026-04-19 |
| Applies To | All engineers — client, server, tools, automation |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) |
| Approval | Director of Engineering |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD19 defines standards for managing code-level dependencies between classes, modules, and services. It covers coupling — what it is, when tight coupling is acceptable, and how to reduce it when it is not — along with practical patterns applicable across all four stacks.

This document is distinct from [ESTD1 §23](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#23-dependency-external-library-management), which governs *external library* selection, approval, and version pinning. ESTD19 addresses how *your own code* depends on other parts of *your own codebase* (and how to keep those dependencies manageable).

---

- [ESTD19 - Dependency Management and Coupling Standards](#estd19---dependency-management-and-coupling-standards)
  - [How to Use This Document](#how-to-use-this-document)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. What Is Coupling?](#2-what-is-coupling)
  - [3. Tight vs Loose Coupling](#3-tight-vs-loose-coupling)
    - [3.1 Comparison](#31-comparison)
    - [3.2 When Tight Coupling Is Acceptable](#32-when-tight-coupling-is-acceptable)
    - [3.3 When to Prefer Loose Coupling](#33-when-to-prefer-loose-coupling)
  - [4. Strategies to Reduce Coupling](#4-strategies-to-reduce-coupling)
    - [4.1 Depend on Abstractions, Not Implementations](#41-depend-on-abstractions-not-implementations)
    - [4.2 Constructor Injection (Dependency Injection)](#42-constructor-injection-dependency-injection)
    - [4.3 Event-Driven Decoupling (Observer Pattern)](#43-event-driven-decoupling-observer-pattern)
    - [4.4 Adapter Pattern](#44-adapter-pattern)
  - [5. Common Coupling Anti-Patterns](#5-common-coupling-anti-patterns)
  - [6. Decision Guide](#6-decision-guide)
  - [7. Enforcement](#7-enforcement)

---

## 1. Purpose and Scope

This standard defines how engineers should manage code-level dependencies — the relationships between classes, modules, and services within our codebases. It applies to all stacks: PHP (API monolith), Java (SEAM microservices, SmartFox), C# (Unity client), and TypeScript (NextJS internal tools).

**In scope:** class-to-class coupling, module boundaries, dependency direction, patterns for decoupling.

**Out of scope:** external library management ([ESTD1 §23](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#23-dependency-external-library-management)), infrastructure dependencies ([ESTD5](./ESTD5_-_Cloud_Engg_Standards.md), [ESTD8](./ESTD8_-_AWS_Standards.md)).

---

## 2. What Is Coupling?

**Coupling** is the degree to which one class or module depends on the internal details of another. When class A directly instantiates, references concrete types of, or assumes the behavior of class B, they are coupled. The tighter the coupling, the more a change in B forces a change in A.

**Dependency** in this context means: A cannot compile, run, or be tested without B being present and unchanged.

```
TIGHT COUPLING                          LOOSE COUPLING
─────────────────────────────           ─────────────────────────────
RewardService ──→ MySQLPlayerRepo       RewardService ──→ IPlayerRepo (interface)
                  │                                        ↗        ↖
                  └→ MySQL driver               MySQLPlayerRepo    MockPlayerRepo

A change in MySQLPlayerRepo             RewardService is unchanged when
forces a change in RewardService.       the repository implementation changes.
Cannot test without a live DB.          Testable with a mock.
```

---

## 3. Tight vs Loose Coupling

### 3.1 Comparison

| Aspect | Tight Coupling | Loose Coupling |
|:-------|:---------------|:---------------|
| **Readability** | Direct, easy to trace call chain | Indirection; must look up interface implementations |
| **Testability** | Hard; requires real dependencies or heavy mocking | Easy; inject test doubles through constructor |
| **Flexibility** | Rigid; swapping an implementation requires editing callers | Flexible; swap implementations without touching callers |
| **Change propagation** | Ripple effect — one change breaks many files | Changes isolated to the implementation |
| **Startup complexity** | Simpler; no wiring/container needed | Requires a composition root or DI container |
| **Performance** | No indirection overhead | Negligible overhead from virtual/interface dispatch |
| **Onboarding cost** | Lower for small codebases | Higher initially; pays off as codebase grows |

### 3.2 When Tight Coupling Is Acceptable

Tight coupling is not inherently wrong. It is the correct choice when:

- **Value objects and data models.** `PlayerScore`, `RoomConfig`, `BingoCard` — these are stable, immutable, and have no reason to be abstracted.
- **Private implementation details.** A private helper method within a class does not need an interface.
- **Stable framework types.** Coupling to `string`, `List<T>`, `DateTime`, or the language's standard library is expected.
- **One-off scripts and migrations.** Throwaway code does not benefit from decoupling.

**The rule:** tight coupling to *stable abstractions* is fine. Tight coupling to *volatile implementations* is not.

### 3.3 When to Prefer Loose Coupling

Decouple when any of these are true:

- The dependency crosses a **layer boundary** (controller → service → repository).
- The dependency is a **volatile implementation** — it changes frequently, talks to external systems, or has multiple possible implementations.
- The class must be **unit-testable** in isolation without standing up infrastructure.
- The dependency **will be replaced** — e.g., migrating from MySQL to MongoDB, swapping a payment provider.
- Two teams or services own the code on **opposite sides** of the dependency.

---

## 4. Strategies to Reduce Coupling

### 4.1 Depend on Abstractions, Not Implementations

**Rule:** public classes should depend on interfaces (or abstract classes), not on concrete implementations. The concrete implementation is provided at construction time.

**PHP — API Server**

```php
interface PlayerRepositoryInterface {
    public function findById(string $playerId): ?Player;
    public function save(Player $player): void;
}

class RewardService {
    private PlayerRepositoryInterface $playerRepo;

    public function __construct(PlayerRepositoryInterface $playerRepo) {
        $this->playerRepo = $playerRepo;
    }

    public function claimDailyBonus(string $playerId): ClaimResult {
        $player = $this->playerRepo->findById($playerId);
        if ($player === null) {
            return ClaimResult::playerNotFound();
        }
        $player->awardDailyBonus();
        $this->playerRepo->save($player);
        return ClaimResult::success($player->getCoinBalance());
    }
}
```

**Java — SEAM Microservice**

```java
public interface IPlayerRepository {
    Optional<Player> findById(String playerId);
    void save(Player player);
}

public class RewardService {
    private final IPlayerRepository playerRepo;

    public RewardService(IPlayerRepository playerRepo) {
        this.playerRepo = playerRepo;
    }

    public ClaimResult claimDailyBonus(String playerId) {
        Player player = playerRepo.findById(playerId)
            .orElseThrow(() -> new PlayerNotFoundException(playerId));
        player.awardDailyBonus();
        playerRepo.save(player);
        return ClaimResult.success(player.getCoinBalance());
    }
}
```

**Unity C# — Client**

```csharp
public interface IRewardService {
    UniTask<ClaimResult> ClaimDailyBonusAsync(CancellationToken ct);
}

public class BingoLobbyController {
    private readonly IRewardService _rewardService;

    public BingoLobbyController(IRewardService rewardService) {
        _rewardService = rewardService;
    }

    public async UniTaskVoid OnDailyBonusTapped() {
        ClaimResult result = await _rewardService.ClaimDailyBonusAsync(_cts.Token);
        _uiManager.ShowClaimResult(result);
    }
}
```

**TypeScript — NextJS Internal Tool**

```typescript
interface INotificationService {
    send(playerId: string, message: string): Promise<void>;
}

class EventScheduler {
    constructor(private readonly notifications: INotificationService) {}

    async scheduleWeeklyEvent(eventId: string, playerIds: string[]): Promise<void> {
        for (const playerId of playerIds) {
            await this.notifications.send(playerId, `Event ${eventId} starts soon`);
        }
    }
}
```

### 4.2 Constructor Injection (Dependency Injection)

**Rule:** pass dependencies through the constructor. Do not instantiate them internally with `new`. The constructor declares *what* the class needs; the caller decides *which implementation* to provide.

This follows directly from [ESTD1 §8](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#8-object-instantiation--initialization-standard) — constructors assign, factories create.

```
TIGHT (before)                                       LOOSE (after)
──────────────────────────────                       ──────────────────────────────
class RoomManager {                                  class RoomManager {
    private repo = new MySQLRoomRepo(); ←  BAD           private IRoomRepo repo;        ← GOOD
    ...                                                  constructor(IRoomRepo repo) {
}                                                            this.repo = repo;
                                                         }
RoomManager creates its own dependency.              }
Cannot swap, cannot mock.                            Caller provides the dependency.
                                                     Swappable. Testable.
```

**PHP — tight → loose**

```php
// TIGHT — hard to test, hard to swap
class RoomManager {
    private MySQLRoomRepository $repo;

    public function __construct() {
        $this->repo = new MySQLRoomRepository(); // creates its own dependency
    }
}

// LOOSE — injectable, testable
class RoomManager {
    private RoomRepositoryInterface $repo;

    public function __construct(RoomRepositoryInterface $repo) {
        $this->repo = $repo;
    }
}
```

**Java — tight → loose**

```java
// TIGHT
public class JackpotService {
    private final MySQLJackpotDao dao = new MySQLJackpotDao(); // hard-wired
}

// LOOSE
public class JackpotService {
    private final IJackpotDao dao;

    public JackpotService(IJackpotDao dao) {
        this.dao = dao;
    }
}
```

**Unity C# — tight → loose**

```csharp
// TIGHT
public class LeaderboardPanel : MonoBehaviour {
    private HttpLeaderboardService _service = new HttpLeaderboardService(); // untestable
}

// LOOSE
public class LeaderboardPanel : MonoBehaviour {
    private ILeaderboardService _service;

    public void Init(ILeaderboardService service) {
        _service = service;
    }
}
```

**TypeScript — tight → loose**

```typescript
// TIGHT
class BalanceAdjustmentTool {
    private api = new BingoApiClient(); // locked to one implementation
}

// LOOSE
class BalanceAdjustmentTool {
    constructor(private readonly api: IBingoApiClient) {}
}
```

### 4.3 Event-Driven Decoupling (Observer Pattern)

**Rule:** when a producer does not need a response from a consumer, use events. The producer emits; zero or more consumers react independently. Neither side knows or depends on the other.

```
DIRECT CALL (tight)                     EVENT-DRIVEN (loose)
────────────────────────                ────────────────────────
RoomManager.endRound()                  RoomManager.endRound()
  → rewardService.award(...)              → eventBus.emit(RoundEnded{...})
  → leaderboardService.update(...)
  → analyticsService.track(...)         RewardListener ← subscribes to RoundEnded
                                        LeaderboardListener ← subscribes to RoundEnded
RoomManager knows every consumer.       AnalyticsListener ← subscribes to RoundEnded
Adding a consumer = editing
  RoomManager.                          RoomManager knows zero consumers.
                                        Adding a consumer = registering a listener.
```

**Java — SmartFox room event**

```java
public interface IRoomEventListener {
    void onRoundEnded(RoundEndedEvent event);
}

public class RoomEventDispatcher {
    private final List<IRoomEventListener> listeners = new ArrayList<>();

    public void register(IRoomEventListener listener) {
        listeners.add(listener);
    }

    public void emitRoundEnded(RoundEndedEvent event) {
        for (IRoomEventListener listener : listeners) {
            listener.onRoundEnded(event);
        }
    }
}

public class RewardListener implements IRoomEventListener {
    private final IRewardService rewardService;

    public RewardListener(IRewardService rewardService) {
        this.rewardService = rewardService;
    }

    @Override
    public void onRoundEnded(RoundEndedEvent event) {
        rewardService.awardRoundRewards(event.getRoomId(), event.getWinners());
    }
}
```

**Unity C# — delegate events**

```csharp
public class BingoGameController {
    public event Action<RoundEndedData> RoundEnded;

    private void EndRound(RoundEndedData data) {
        RoundEnded?.Invoke(data);
    }
}

public class RewardPopupController {
    public void Init(BingoGameController game) {
        game.RoundEnded += OnRoundEnded;
    }

    private void OnRoundEnded(RoundEndedData data) {
        ShowRewardPopup(data.PrizeAmount);
    }
}
```

### 4.4 Adapter Pattern

**Rule:** wrap external or third-party services behind an internal interface. The adapter translates between the external API and your domain. If the external service changes or is replaced, only the adapter changes.

```
Your Code ──→ IPaymentGateway (your interface)
                  │
                  ├── StripePaymentAdapter (today)
                  └── BraintreePaymentAdapter (tomorrow)
```

**PHP — payment adapter**

```php
interface PaymentGatewayInterface {
    public function charge(string $playerId, int $amountCents, string $currency): ChargeResult;
}

class StripePaymentAdapter implements PaymentGatewayInterface {
    private StripeClient $stripe;

    public function __construct(StripeClient $stripe) {
        $this->stripe = $stripe;
    }

    public function charge(string $playerId, int $amountCents, string $currency): ChargeResult {
        $response = $this->stripe->charges->create([
            'amount'   => $amountCents,
            'currency' => $currency,
            'metadata' => ['player_id' => $playerId],
        ]);
        return ChargeResult::fromStripeResponse($response);
    }
}
```

**Java — analytics adapter**

```java
public interface IAnalyticsTracker {
    void trackEvent(String eventName, Map<String, Object> properties);
}

public class MixpanelAnalyticsAdapter implements IAnalyticsTracker {
    private final MixpanelAPI mixpanel;

    public MixpanelAnalyticsAdapter(MixpanelAPI mixpanel) {
        this.mixpanel = mixpanel;
    }

    @Override
    public void trackEvent(String eventName, Map<String, Object> properties) {
        JSONObject props = new JSONObject(properties);
        mixpanel.track(eventName, props);
    }
}
```

---

## 5. Common Coupling Anti-Patterns

| # | Anti-Pattern | Symptom | Fix |
|:--|:-------------|:--------|:----|
| 1 | **`new` inside business logic** | Cannot unit-test without real dependency (DB, API) | Move to constructor injection ([§4.2](#42-constructor-injection-dependency-injection)) |
| 2 | **God class** | One class referenced by 50+ files; every change breaks something | Apply Single Responsibility Principle; extract focused services |
| 3 | **Circular dependencies** | A depends on B, B depends on A; compile errors or fragile initialization order | Introduce an interface that both sides depend on, or use events ([§4.3](#43-event-driven-decoupling-observer-pattern)) |
| 4 | **Service Locator overuse** | Dependencies are hidden inside method bodies; constructor signature lies about what the class needs | Replace with explicit constructor injection; the constructor is the dependency manifest |
| 5 | **Leaky abstractions** | Interface exposes implementation details (`IMySQLPlayerRepo` with `executeRawQuery()`) | Interface should model the domain operation, not the storage technology |
| 6 | **Shotgun surgery** | A single logical change requires edits in 10+ files across layers | Consolidate related logic; check that layer boundaries are in the right place |

---

## 6. Decision Guide

Use this to decide how to structure a dependency:

```
Is the dependency a value object or standard-library type?
  └─ YES → Direct reference. No interface needed.

Is the dependency stable and unlikely to have multiple implementations?
  └─ YES → Direct reference is acceptable if testability is not a concern.

Does the dependency cross a layer boundary (controller → service → repo)?
  └─ YES → Use an interface + constructor injection.

Does the class need to be unit-tested in isolation?
  └─ YES → Depend on an interface; inject a mock in tests.

Does the producer need to notify consumers without waiting for a response?
  └─ YES → Use events / observer pattern.

Is the dependency an external service or third-party SDK?
  └─ YES → Wrap it in an adapter behind an internal interface.
```

**Summary rule:** if you cannot delete the dependency's source file without breaking your class's *compilation*, and the dependency is volatile, you are too tightly coupled. Introduce an abstraction.

---

## 7. Enforcement

These standards are enforced at code review per [ESTD10](./ESTD10_-_PR_Authoring_And_Reviewing_Standards.md#estd10---pull-request-authoring-and-review-standards-for-engineers). Reviewers should flag:

- `new` inside service/domain classes when the created object is a volatile dependency.
- Constructor signatures that hide dependencies (work done inside methods via static accessors or service locators).
- Interfaces that expose storage/transport details rather than domain operations.

Where tooling supports it (Java: ArchUnit, C#: NDepend, TypeScript: dependency-cruiser), add circular dependency detection to CI. Violations should fail the build.
