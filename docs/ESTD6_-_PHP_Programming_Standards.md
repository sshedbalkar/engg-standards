# ESTD6 - PHP Programming Standards

**ESTD6 — PHP Programming Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD6 |
| Version | 4.0 |
| Status | Active |
| Last Updated | 2026-04-09 |
| Applies To | All engineers contributing to the legacy PHP API server  |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management) |
| Approval | Director of Engineering / Server Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD6 applies to the legacy PHP monolith and any PHP code that supports the classic Bingo stack or its web tools. Read [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) for shared standards and [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices) for server-wide architecture, security, and operational rules; ESTD6 narrows those standards for framework-less PHP 8.x development in the long-lived monolith.

This document is intentionally pragmatic: existing legacy code will not become fully compliant in one pass. New code must comply immediately, and touched legacy code must be improved incrementally under the "leave it better" rule.

---

## Table of Contents

- [ESTD6 - PHP Programming Standards](#estd6---php-programming-standards)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. PHP Version and Configuration](#2-php-version-and-configuration)
    - [2.1 PHP 8.x Features in Active Use](#21-php-8x-features-in-active-use)
    - [2.2 php.ini Essential Requirements (Production)](#22-phpini-essential-requirements-production)
  - [3. Coding Style (PSR-12)](#3-coding-style-psr-12)
  - [4. Naming Conventions (PHP)](#4-naming-conventions-php)
  - [5. Class and File Organization](#5-class-and-file-organization)
    - [5.1 Namespace and Directory Structure](#51-namespace-and-directory-structure)
    - [5.2 Class Internal Order](#52-class-internal-order)
  - [6. Type System Usage](#6-type-system-usage)
    - [6.1 Type Declarations Are Mandatory](#61-type-declarations-are-mandatory)
    - [6.2 Nullable Types](#62-nullable-types)
    - [6.3 Value Objects and DTOs with Readonly](#63-value-objects-and-dtos-with-readonly)
    - [6.4 Enums for Domain Values](#64-enums-for-domain-values)
  - [7. Error Handling in PHP](#7-error-handling-in-php)
    - [7.1 Custom Exception Hierarchy](#71-custom-exception-hierarchy)
    - [7.2 Individual Error Handling](#72-individual-error-handling)
    - [7.3 Top-Level Exception Boundary](#73-top-level-exception-boundary)
  - [8. Input Validation and Sanitization](#8-input-validation-and-sanitization)
    - [8.1 Validation Classes](#81-validation-classes)
    - [8.2 Sanitization](#82-sanitization)
  - [9. Database Access (PHP)](#9-database-access-php)
    - [9.1 Repository Pattern](#91-repository-pattern)
    - [9.2 PDO Configuration](#92-pdo-configuration)
    - [9.3 Transactions for Economic Operations](#93-transactions-for-economic-operations)
  - [10. Dependency Management (Composer)](#10-dependency-management-composer)
  - [11. Security-Specific PHP Rules](#11-security-specific-php-rules)
    - [11.1 Password Hashing](#111-password-hashing)
    - [11.2 Hashing Non-Password Sensitive Data](#112-hashing-non-password-sensitive-data)
    - [11.3 Secure Random Numbers](#113-secure-random-numbers)
    - [11.4 HTTP Header Security](#114-http-header-security)
  - [12. Session and Authentication (PHP)](#12-session-and-authentication-php)
  - [13. Performance in PHP](#13-performance-in-php)
  - [14. Unit Testing in PHP](#14-unit-testing-in-php)
    - [14.1 Testing Framework](#141-testing-framework)
    - [14.2 Test Structure](#142-test-structure)
    - [14.3 Identifying Code Paths to Test](#143-identifying-code-paths-to-test)
    - [14.4 Boundary Conditions to Always Test](#144-boundary-conditions-to-always-test)
    - [14.5 Test Data Builders](#145-test-data-builders)
  - [15. Common Pitfalls to Avoid](#15-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

**Why this document exists:** The legacy Bingo game API is a PHP 8.x monolith with no framework. Its primary database is **MySQL** (AWS RDS). All PHP API code — including the classic Bingo game API and the classic Bingo web tools backend — uses MySQL exclusively. The new Bingo game uses Java/SEAM services with service-owned MySQL schemas; PHP code does not interact with those schemas directly except through explicit APIs and integration boundaries. It has been in production for 15 years. This document aims to bring the codebase forward to modern PHP standards while respecting the reality of working with a long-running production system. New code added to the monolith must comply with these standards. Existing code must be brought into compliance incrementally during refactoring work — the "leave it better than you found it" principle from [ESTD1 §2. Guiding Principles](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#2-guiding-principles) is the operative strategy.

---

## 2. PHP Version and Configuration

### 2.1 PHP 8.x Features in Active Use

The following PHP 8.x features are required for all new code:

- **Named arguments**: `array_slice(array: $balls, offset: 0, length: 10)`
- **Match expressions**: preferred over `switch` for value mapping  
- **Nullsafe operator** (`?->`): preferred over repeated null checks  
- **Union types**: `int|string $playerId`  
- **Constructor property promotion**: for simple DTO classes  
- **Enums (PHP 8.1)**: required for any finite set of domain values  
- **Readonly properties (PHP 8.1)**: required for DTO/value object classes  
- **Fibers (PHP 8.1)**: permitted for async I/O patterns where applicable

### 2.2 php.ini Essential Requirements (Production)

```
display_errors = Off
log_errors = On
error_reporting = E_ALL
expose_php = Off
max_execution_time = 30
memory_limit = 256M
upload_max_filesize = 1M
```

---

## 3. Coding Style (PSR-12)

All PHP code must comply with PSR-12 (Extended Coding Style). PSR-12 compliance is enforced by PHP_CodeSniffer or PHP CS Fixer in the CI pipeline. Builds that fail the style check must not be merged.

Key PSR-12 points:

- `<?php` opening tag only; no closing `?>` in class files.  
- 4-space indentation (no tabs).  
- Opening braces for classes and methods on a new line; opening braces for control structures on the same line.  
- `use` statements alphabetically ordered, separated into three groups: PHP standard library, third-party, internal.

Every PHP file must begin with:

```php
<?php

declare(strict_types=1);
```

This enables strict type checking for scalar types and prevents silent type coercion bugs.

---

## 4. Naming Conventions (PHP)

| Symbol | Convention | Example | 
|:-------|:-----------|:--------|
| Class | PascalCase | `RewardService`, `BingoRoomRepository` |
| Interface | PascalCase, `Interface` suffix | `PlayerRepositoryInterface` | 
| Abstract class | PascalCase, `Abstract` prefix | `AbstractRewardHandler` |
| Trait | PascalCase, `Trait` suffix | `TimestampableTrait` | 
| Enum | PascalCase | `GameState`, `RoomType` | 
| Public method | camelCase | `rewardClaim()`, `playerFindById()` | 
| Private/protected method | camelCase | `claimValidate()` | 
| Private/protected property | `_camelCase` | `$_db`, `$_logger` |
| Public property | camelCase | `$playerId`, `$rewardType` | 
| Local variable | camelCase | `$playerBalance`, `$ballNumber` |
| Constant | UPPER_SNAKE_CASE | `BALL_COUNT_MAX`, `SESSION_TTL_SEC` |
| Namespace | PascalCase, matches directory | `App\Reward\Service` |

---

## 5. Class and File Organization

### 5.1 Namespace and Directory Structure

```
src/
├── Core/
│   ├── Database/
│   │   └── DatabaseConnection.php    → App\Core\Database\DatabaseConnection
│   ├── Session/
│   │   └── SessionManager.php        → App\Core\Session\SessionManager
│   └── Logging/
│       └── Logger.php                → App\Core\Logging\Logger
├── Player/
│   ├── Repository/
│   │   └── PlayerRepository.php      → App\Player\Repository\PlayerRepository
│   ├── Service/
│   │   └── PlayerService.php         → App\Player\Service\PlayerService
│   └── Dto/
│       └── PlayerProfileDto.php      → App\Player\Dto\PlayerProfileDto
└── Reward/
    ├── Service/
    │   └── RewardService.php         → App\Reward\Service\RewardService
    └── Validator/
        └── RewardClaimValidator.php  → App\Reward\Validator\RewardClaimValidator
```

### 5.2 Class Internal Order

```php
class RewardService
{
    // 1. Constants
    private const CLAIM_DAILY_COUNT_MAX = 10;

    // 2. Properties (private before protected before public)
    private RewardRepositoryInterface $_rewardRepository;
    private LoggerInterface $_logger;

    // 3. Constructor
    public function __construct(
        RewardRepositoryInterface $rewardRepository,
        LoggerInterface $logger
    ) { ... }

    // 4. Public interface methods (documented with PHPDoc)
    // 5. Protected methods
    // 6. Private methods
}
```

---

## 6. Type System Usage

### 6.1 Type Declarations Are Mandatory

All method parameters, return types, and class properties must have declared types. Untyped code is not acceptable for new or refactored methods.

```php
// BAD — untyped, dangerous
public function playerFind($id) {
    return $this->_db->query("SELECT ...", $id);
}

// GOOD — fully typed
public function playerFind(int $playerId): ?PlayerDto {
    return $this->_playerRepository->findById($playerId);
}
```

### 6.2 Nullable Types

Use `?Type` only where null is a genuinely valid return value representing "not found" or "not applicable". Do not return null to signal an error — throw an exception or return a Result object instead.

### 6.3 Value Objects and DTOs with Readonly

```php
<?php
declare(strict_types=1);
namespace App\Reward\Dto;

final readonly class RewardClaimDto
{
    public function __construct(
        public int    $playerId,
        public string $rewardId,
        public string $idempotencyKey,
    ) {}
}
```

### 6.4 Enums for Domain Values

```php
<?php
declare(strict_types=1);
namespace App\Game\Enum;

enum GameState: string
{
    case Waiting = 'waiting';
    case Active  = 'active';
    case Ended   = 'ended';
    case Paused  = 'paused';

    public function isPlayable(): bool
    {
        return $this === self::Active;
    }
}
```
Never use raw string or integer constants for values that belong in an enum.

---

## 7. Error Handling in PHP

Applies [ESTD1 §9. Error Handling and Try-Catch Usage](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#9-error-handling-and-try-catch-usage) to PHP. Every failable statement must be individually handled.

### 7.1 Custom Exception Hierarchy

```
App\Exception\
    AppException                    ← base
    NotFoundException
    ValidationException
    ForbiddenException
    ConflictException               ← already-claimed, duplicate, etc.
    ExternalServiceException
    DatabaseException
    CacheException
    PaymentGatewayException
```

### 7.2 Individual Error Handling

```php
// BAD — block try-catch hides which operation failed
try {
    $player = $this->_playerRepository->findById($playerId);
    $reward = $this->_rewardRepository->findById($rewardId);
    $this->_rewardRepository->markClaimed($player->id, $reward->id);
} catch (\Exception $e) {
    $this->_logger->error('Claim failed', ['error' => $e->getMessage()]);
}

// GOOD — each operation individually handled with appropriate recovery
try {
    $player = $this->_playerRepository->findById($playerId);
} catch (DatabaseException $e) {
    $this->_logger->error('Failed to load player', [
        'playerId' => $playerId,
        'error'    => $e->getMessage(),
    ]);
    return ClaimResult::failure(ClaimError::PlayerLoadFailed);
}
if ($player === null) {
    return ClaimResult::failure(ClaimError::PlayerNotFound);
}
```

### 7.3 Top-Level Exception Boundary

```php
// Bootstrap / front controller — final safety net
try {
    $response = $router->dispatch($request);
} catch (\Throwable $t) {
    $logger->fatal('Unhandled exception', [
        'message'    => $t->getMessage(),
        'stackTrace' => $t->getTraceAsString(),
        'requestId'  => $requestId,
    ]);
    // Return generic error — never expose internals to the client
    return new JsonResponse(['success' => false, 'error' => ['code' => 'INTERNAL_ERROR']], 500);
}
```

**Entry-point boundary rule**: The bootstrap/front-controller try-catch wrapping `$router->dispatch($request)` is the entry-point boundary ([ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions)). It is correct and necessary — it guarantees no unhandled exception reaches the player. This is the one and only place where a multi-statement try-catch is acceptable without per-statement handling. All code inside dispatched controllers and service methods must use individual per-statement try-catch blocks ([ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)).

---

## 8. Input Validation and Sanitization

### 8.1 Validation Classes

Use a dedicated validator class for each request type. Do not inline validation logic in controllers.

```php
final class RewardClaimValidator
{
    public function validate(array $payload): ValidationResult
    {
        $errors = [];
        if (empty($payload['rewardId']) || !is_string($payload['rewardId'])) {
            $errors[] = new ValidationError('rewardId', 'REQUIRED_STRING');
        } elseif (strlen($payload['rewardId']) > 64) {
            $errors[] = new ValidationError('rewardId', 'MAX_LENGTH_EXCEEDED');
        }
        if (empty($payload['idempotencyKey']) || !Uuid::isValid($payload['idempotencyKey'])) {
            $errors[] = new ValidationError('idempotencyKey', 'REQUIRED_UUID');
        }
        return empty($errors)
            ? ValidationResult::success()
            : ValidationResult::failure($errors);
    }
}
```

### 8.2 Sanitization

- **HTML output**: `htmlspecialchars($value, ENT_QUOTES, 'UTF-8')`
- **SQL**: PDO prepared statements exclusively — never concatenate user data into SQL.  
- **Log injection**: Strip newline characters from user data before including in a log message: `str_replace(["\\r", "\\n"], '', $input)`

---

## 9. Database Access (PHP)

### 9.1 Repository Pattern

All database access must go through Repository classes. Controllers and Services must not hold or use database connections directly.

```php
interface PlayerRepositoryInterface
{
    public function findById(int $playerId): ?PlayerDto;
    public function balanceUpdate(int $playerId, int $deltaCoins): bool;
}

final class PlayerRepository implements PlayerRepositoryInterface
{
    public function __construct(private readonly \PDO $_pdo) {}

    public function findById(int $playerId): ?PlayerDto
    {
        $stmt = $this->_pdo->prepare(
            'SELECT player_id, username, coin_balance
               FROM players
              WHERE player_id = :playerId
              LIMIT 1'
        );
        try {
            $stmt->execute([':playerId' => $playerId]);
        } catch (\PDOException $e) {
            throw new DatabaseException("Failed to find player {$playerId}", previous: $e);
        }
        $row = $stmt->fetch(\PDO::FETCH_ASSOC);
        return $row ? PlayerDto::fromRow($row) : null;
    }
}
```

### 9.2 PDO Configuration

```php
$pdo->setAttribute(\PDO::ATTR_ERRMODE,            \PDO::ERRMODE_EXCEPTION);
$pdo->setAttribute(\PDO::ATTR_DEFAULT_FETCH_MODE, \PDO::FETCH_ASSOC);
$pdo->setAttribute(\PDO::ATTR_EMULATE_PREPARES,   false);
```

### 9.3 Transactions for Economic Operations

```php
public function roomWinBonusAward(int $playerId, int $coinAmount): AwardResult
{
    $this->_pdo->beginTransaction();
    try {
        // 1. Record in ledger
        $this->_ledgerRepository->record($playerId, $coinAmount, LedgerType::RoomWin);
        // 2. Update balance with optimistic locking
        $affected = $this->_playerRepository->balanceIncrement($playerId, $coinAmount);
        if ($affected === 0) {
            $this->_pdo->rollBack();
            throw new ConcurrentModificationException("Balance update failed for player {$playerId}");
        }
        $this->_pdo->commit();
        return AwardResult::success($coinAmount);
    } catch (\Throwable $e) {
        $this->_pdo->rollBack();
        throw $e;
    }
}
```

---

## 10. Dependency Management (Composer)

- All dependencies must be declared in `composer.json` with explicit version constraints.  
- Use `composer.lock` and commit it to Git to ensure reproducible builds across all environments.  
- Run `composer audit` in CI to detect known vulnerabilities. Builds with high/critical CVEs must be blocked.  
- `require-dev` dependencies (testing, code analysis tools) must be separated from `require`.  
- No `*` (wildcard) version constraints in production dependencies.

---

## 11. Security-Specific PHP Rules

### 11.1 Password Hashing

```php
// ONLY accepted function for password hashing
$hash = password_hash($plainTextPassword, PASSWORD_BCRYPT, ['cost' => 12]);

// Verification
if (!password_verify($plainTextPassword, $storedHash)) {
    throw new AuthenticationException("Invalid credentials");
}

// Rehash if the cost factor has increased (on next successful login)
if (password_needs_rehash($storedHash, PASSWORD_BCRYPT, ['cost' => 12])) {
    $newHash = password_hash($plainTextPassword, PASSWORD_BCRYPT, ['cost' => 12]);
    $this->_playerRepository->passwordHashUpdate($playerId, $newHash);
}
```

### 11.2 Hashing Non-Password Sensitive Data

**MD5 and SHA-1 are cryptographically broken and must not be used for any security-sensitive purpose** — including hashing email addresses for lookup, player IDs for anonymization, or idempotency keys for storage.

For non-password sensitive data that needs hashing:

| Use Case | Recommended Algorithm | Notes |
|:---------|:----------------------|:------|
| Fast lookup hash (email deduplication, idempotency key storage) | `SHA-256` via `hash('sha256', $value)` | Not reversible; safe for lookup tables |
| Anonymization of PII for analytics | `SHA-256` with a secret salt (HMAC) | Use `hash_hmac('sha256', $pii, $secret)` | 
| Content integrity check (file checksums) | `SHA-256` | Standard for data integrity | 
| Generating secure random tokens | `bin2hex(random_bytes(32))` | Cryptographically secure; not a hash |
| High-security keyed hash | `HMAC-SHA-256` | Use `hash_hmac('sha256', $data, $key)` |

```php
// WRONG — MD5 and SHA-1 are broken for security purposes
$emailHash = md5($email);       // DO NOT USE
$emailHash = sha1($email);      // DO NOT USE

// CORRECT — SHA-256 for lookup / anonymization
$emailLookupHash = hash('sha256', strtolower(trim($email)));

// BETTER — HMAC-SHA-256 for anonymization where a secret key can be managed
$emailAnonHash = hash_hmac('sha256', strtolower(trim($email)), $this->_hmacSecret);

// CORRECT — for generating secure tokens (not a hash, but commonly confused)
$secureToken = bin2hex(random_bytes(32));  // 64-char hex string, cryptographically random
```

### 11.3 Secure Random Numbers

Use `random_int()` for cryptographically secure random integers. Use `random_bytes()` for secure random binary data. Never use `rand()` or `mt_rand()` for anything security-related — they are not cryptographically secure.

### 11.4 HTTP Header Security

Set the following security headers on all responses:

```php
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('Referrer-Policy: no-referrer');
header('Content-Security-Policy: default-src \'self\'');
```

---

## 12. Session and Authentication (PHP)

Session tokens must be validated on every request in middleware before any controller logic executes. Short-lived access tokens (1 hour) + rotating refresh tokens (30 days). Session data stored in Redis, not PHP's default file-based session storage. Always use HTTPS — never transmit tokens over plain HTTP.

---

## 13. Performance in PHP

- Avoid `sleep()` in request handlers — it holds a PHP-FPM worker and kills throughput.  
- Use generators (`yield`) for large dataset processing instead of loading everything into memory with `array_map`.  
- Cache expensive read operations in Redis (see [ESTD4 §15. Caching Strategy](./ESTD4_-_Server_Engg_Standards.md#15-caching-strategy).  
- Use connection pooling via PDO persistent connections or an external pool (PgBouncer equivalent for MySQL).  
- Profile with `Xdebug` or `Blackfire` before optimizing — never optimize based on assumption.

---

## 14. Unit Testing in PHP

Unit testing is mandatory ([ESTD1 §24.2 Unit Testing Is Mandatory](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#242-unit-testing-is-mandatory)). Refer [ESTD16](./ESTD16_-_Paths_And_Unit_Testing_Strategy.md#estd16---paths-branches-and-unit-testing-strategy) for the full documentation on Paths, and Unit testing Strategies. The minimum coverage target is 80% line coverage for all business logic classes. This section explains how to identify code paths that need tests and how to write effective tests.

### 14.1 Testing Framework

Use PHPUnit for all PHP unit and integration tests. Use `Mockery` or PHPUnit's built-in mock builder for mocking dependencies.

### 14.2 Test Structure

```
tests/
├── Unit/                     ← Pure PHP tests; no DB, no HTTP, no external calls
│   ├── Reward/
│   │   ├── RewardServiceTest.php
│   │   └── RewardClaimValidatorTest.php
│   ├── ContentWeek/
│   │   └── ContentResetCalculatorTest.php
│   └── ...
└── Integration/              ← Tests that use real DB or HTTP
    ├── Api/
    │   └── RewardControllerTest.php
    └── Repository/
        └── PlayerRepositoryTest.php
```

### 14.3 Identifying Code Paths to Test

A `code path` is a unique sequence of execution through a function. Every `if`, `else`, `switch` case, `catch` block, and loop creates a new branch in the code — and each branch is a code path that may behave differently.

**Step 1: Count your branches**. For every method, identify every decision point:

```php
public function weeklyBonusClaim(int $playerId, int $contentCycleId): BonusResult
{
    // PATH 1: Player not found
    $player = $this->_playerRepository->findById($playerId);
    if ($player === null) {                               // Branch 1
        return BonusResult::failure(ClaimError::PlayerNotFound);
    }

    // PATH 2: Already claimed
    if ($this->_bonusRepository->hasClaimed($playerId, $contentCycleId)) { // Branch 2
        return BonusResult::failure(ClaimError::AlreadyClaimed);
    }

    // PATH 3: Database failure
    try {
        $this->_bonusRepository->claimRecord($playerId, $contentCycleId);  // Branch 3 (exception)
    } catch (DatabaseException $e) {
        $this->_logger->error(...);
        return BonusResult::failure(ClaimError::DatabaseError);
    }

    // PATH 4: Happy path — successful claim
    return BonusResult::success(WEEKLY_BONUS_COINS);
}
```

This function has 4 code paths. Your test class must cover all 4.

**Step 2: Write one test per path:** 

```php
class RewardServiceTest extends TestCase
{
    private RewardService $sut;
    private MockObject   $playerRepository;
    private MockObject   $bonusRepository;

    protected function setUp(): void
    {
        $this->playerRepository = $this->createMock(PlayerRepositoryInterface::class);
        $this->bonusRepository  = $this->createMock(BonusRepositoryInterface::class);
        $this->sut = new RewardService(
            playerRepository: $this->playerRepository,
            bonusRepository:  $this->bonusRepository,
            logger:           new NullLogger(),
        );
    }

    // PATH 1: Player not found
    public function test_weeklyBonusClaim_whenPlayerNotFound_returnsPlayerNotFoundError(): void
    {
        $this->playerRepository->method('findById')->willReturn(null);

        $result = $this->sut->weeklyBonusClaim(playerId: 1, contentCycleId: 100);

        $this->assertFalse($result->isSuccess());
        $this->assertEquals(ClaimError::PlayerNotFound, $result->getError());
    }

    // PATH 2: Already claimed
    public function test_weeklyBonusClaim_whenAlreadyClaimed_returnsAlreadyClaimedError(): void
    {
        $this->playerRepository->method('findById')->willReturn(new Player(id: 1));
        $this->bonusRepository->method('hasClaimed')->willReturn(true);

        $result = $this->sut->weeklyBonusClaim(playerId: 1, contentCycleId: 100);

        $this->assertFalse($result->isSuccess());
        $this->assertEquals(ClaimError::AlreadyClaimed, $result->getError());
    }

    // PATH 3: Database exception
    public function test_weeklyBonusClaim_whenDatabaseFails_returnsDatabaseError(): void
    {
        $this->playerRepository->method('findById')->willReturn(new Player(id: 1));
        $this->bonusRepository->method('hasClaimed')->willReturn(false);
        $this->bonusRepository->method('claimRecord')
            ->willThrowException(new DatabaseException("Connection lost"));

        $result = $this->sut->weeklyBonusClaim(playerId: 1, contentCycleId: 100);

        $this->assertFalse($result->isSuccess());
        $this->assertEquals(ClaimError::DatabaseError, $result->getError());
    }

    // PATH 4: Happy path
    public function test_weeklyBonusClaim_whenValidRequest_returnsSuccessWithCoins(): void
    {
        $this->playerRepository->method('findById')->willReturn(new Player(id: 1));
        $this->bonusRepository->method('hasClaimed')->willReturn(false);
        $this->bonusRepository->method('claimRecord')->willReturn(true);

        $result = $this->sut->weeklyBonusClaim(playerId: 1, contentCycleId: 100);

        $this->assertTrue($result->isSuccess());
        $this->assertEquals(WEEKLY_BONUS_COINS, $result->getCoinsAwarded());
    }
}
```

### 14.4 Boundary Conditions to Always Test

Beyond the explicit code paths, always add tests for:

- **Zero / empty values**: `playerId = 0`, empty string, empty array  
- **Maximum values**: coin balance at PHP_INT_MAX, very long strings  
- **Null inputs**: even when the type system says a parameter is non-nullable, test the validator  
- **Concurrent access**: can two simultaneous requests both "win" the same bonus? (Test with DB-level unique constraint enforcement)

### 14.5 Test Data Builders

Use builder patterns for complex test objects to keep tests readable:

```php
class PlayerBuilder
{
    private int    $id      = 1;
    private string $username = 'testplayer';
    private int    $coins   = 5000;

    public function withId(int $id): self    { $this->id = $id; return $this; }
    public function withCoins(int $c): self  { $this->coins = $c; return $this; }
    public function withNoCoins(): self      { return $this->withCoins(0); }
    public function build(): Player          { return new Player($this->id, $this->username, $this->coins); }
}

// Clean, readable test setup
$richPlayer  = (new PlayerBuilder())->withCoins(999_999)->build();
$brokePlayer = (new PlayerBuilder())->withNoCoins()->build();
```

---

## 15. Common Pitfalls to Avoid

| # | Pitfall | Consequence | Prevention |
|:--|:--------|:------------|:-----------|
| 1 | `==`  instead of `===` | Type coercion bugs: `"0" == false` is `true` | Always use `===`; `declare(strict_types=1)` catches many |
| 2 | `$_GET/$_POST` directly in business logic | SQL injection, XSS | Always validate through Request DTOs | 
| 3 | Printing exceptions to the client | Stack traces expose internal details | Global exception handler; return generic 500 |
| 4 | `sleep()` in request handlers | Holds PHP-FPM worker; destroys throughput | Use async jobs for deferred work |
| 5 | `rand()` / `mt_rand()` for tokens | Predictable; insecure | Use `random_bytes()` or `random_int()` |
| 6 | MD5/SHA-1 for any security purpose | Cryptographically broken | Use SHA-256 or HMAC-SHA-256 | 
| 7 | Float arithmetic for coin amounts | Floating-point precision errors | Coins are always whole integers (BIGINT in DB) | 
| 8 | `date()` without timezone | Wrong times during DST transitions | Use `DateTimeImmutable` with explicit UTC |
| 9 | Global state / static singletons | Untestable; race conditions across requests | Dependency injection |
| 10 | No `declare(strict_types=1)` | Silent type coercion; hard-to-find bugs | Required in every PHP file |
| 11 | Block try-catch | Cannot determine which operation failed | Each operation handled individually ([ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)) |
| 12 | Missing unit tests for new business logic | Bugs caught in production, not development | 80% coverage target; reject at PR |
