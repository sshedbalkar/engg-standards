# ESTD14 - Hierarchical Naming Strategy for Programming Entities

| Field | Value |
|:----- |:----- |
| **Document ID** | ESTD14 |
| **Version** | 3.2 |
| **Status** | Active |
| **Last Updated** | 2026-04-30 |
| **Applies To** | All engineers — client, server, tools, automation |
| **Depends On** | *(none — this is a root standard)* |
| **Approval** | Director of Engineering |

---

**📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

This documents outlines a naming strategy to name entities while programming such as non-local variables, constants, functions, classes, namespaces, etc. This strategy is language agnostic and can be used in a variety of places. The strategy is called Hierarchical Naming — every non-local identifier reads left (generic) → right (specific), with each component progressively narrowing the meaning:

```
<domain> → <category> → <subcategory> → <specific-trait>
```

*Note: This strategy is language-agnostic and separator-agnostic. Adopt the casing convention of your language and apply the left-to-right generic-to-specific ordering consistently.*

---

## Table of Contents

- [ESTD14 - Hierarchical Naming Strategy for Programming Entities](#estd14---hierarchical-naming-strategy-for-programming-entities)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Core Principle](#1-core-principle)
  - [2. Rationale](#2-rationale)
  - [3. Component Guidelines](#3-component-guidelines)
  - [4. Separator Conventions by Language](#4-separator-conventions-by-language)
  - [5. Examples](#5-examples)
    - [5.1 Variables — Configuration Values](#51-variables--configuration-values)
    - [5.2 Constants — Limits and Thresholds](#52-constants--limits-and-thresholds)
    - [5.3 Functions — Actions Within a Domain](#53-functions--actions-within-a-domain)
    - [5.4 Classes and Types](#54-classes-and-types)
    - [5.5 Booleans and Flags](#55-booleans-and-flags)
    - [5.6 Collections and Maps](#56-collections-and-maps)
    - [5.7 Error and Exception Types](#57-error-and-exception-types)
    - [5.8 Event Names and Message Types](#58-event-names-and-message-types)
    - [5.9. File and Module Names](#59-file-and-module-names)
    - [5.10 Mixed Real-World Module (Python)](#510-mixed-real-world-module-python)
    - [5.11 Metrics and Telemetry](#511-metrics-and-telemetry)
    - [5.12 React Component Props and State](#512-react-component-props-and-state)
    - [5.13 Namespaces](#513-namespaces)
      - [Python Packages](#python-packages)
      - [TypeScript / JavaScript Modules with Barrel Exports](#typescript--javascript-modules-with-barrel-exports)
      - [C++ Nested Namespaces](#c-nested-namespaces)
    - [5.14 Configuration Files](#514-configuration-files)
      - [YAML (Nested — hierarchy is structural)](#yaml-nested--hierarchy-is-structural)
      - [TOML](#toml)
      - [`.env` / Flat Key-Value (hierarchy expressed inline)](#env--flat-key-value-hierarchy-expressed-inline)
    - [5.15 Database Table and Column Names](#515-database-table-and-column-names)
      - [Table Names](#table-names)
      - [Column Names](#column-names)
      - [Index and Constraint Names](#index-and-constraint-names)
  - [6 Anti-Patterns to Avoid](#6-anti-patterns-to-avoid)
  - [7. Quick Reference Checklist](#7-quick-reference-checklist)

---

## 1. Core Principle

> **Names are read left-to-right, from most generic to most specific.**

Every identifier is composed of one or more components joined by the language's conventional separator (camelCase, snake_case, PascalCase, etc.). The leftmost component names the broadest category the entity belongs to; each subsequent component narrows the meaning until the rightmost component expresses the most precise, distinguishing detail.

```
<domain> <category> <subcategory> ... <specific-trait>
```

This mirrors the way we name things in natural language:
- *"vehicle → motor vehicle → car → sports car → red sports car"*

Applied to code, a variable holding the maximum retry count for a network request becomes:

```
network → request → retry → count → max
networkRequestRetryCountMax
```

---

## 2. Rationale

Names ordered from generic to specific mirror how we naturally categorise things. This makes identifiers self-documenting, groups related entities together alphabetically and in autocomplete, and eliminates the need for external context — the name itself tells you the domain, the category, and the precise detail, in that order.

| Property | Benefit |
|---|---|
| **Alphabetic grouping** | Related entities sort together in IDEs, autocomplete, and file listings |
| **Scannable at a glance** | The leftmost word immediately tells you the domain; you read right only as far as needed |
| **Avoids ambiguous abbreviations** | Full, ordered words replace cryptic prefixes like `n`, `p`, `tmp` |
| **Scales with complexity** | Simple things stay short; complex things earn longer names instead of collisions |
| **Language-agnostic** | The ordering rule applies regardless of separator convention |
| **Auto-complete friendly** | Zeros in on the specific name much more quickly as the name is typed |

---

## 3. Component Guidelines

1. **Use nouns** for variables, constants, and classes.
2. **Use verb phrases** for functions/methods; the verb should follow the domain prefix.
3. **Adjectives** (e.g. `max`, `min`, `default`, `initial`, `active`, `pending`) act as the rightmost qualifier.
4. **Avoid filler words** (`data`, `info`, `manager`, `handler`) unless they genuinely narrow meaning.
5. **Keep components to 2–5 words** for non-local names. One word is fine for locals with tiny scope.

---

## 4. Separator Conventions by Language

| Language | Variables / Functions | Constants | Classes |
|---|---|---|---|
| Python | `snake_case` | `UPPER_SNAKE_CASE` | `PascalCase` |
| JavaScript / TypeScript | `camelCase` | `UPPER_SNAKE_CASE` or `camelCase const` | `PascalCase` |
| Go | `camelCase` | `PascalCase` (exported) | `PascalCase` |
| Rust | `snake_case` | `UPPER_SNAKE_CASE` | `PascalCase` |
| Java / C# / PHP | `camelCase` | `UPPER_SNAKE_CASE` | `PascalCase` |
| C / C++ | `snake_case` | `UPPER_SNAKE_CASE` | `PascalCase` |

The **ordering rule is the same** in every case; only the separator changes.

---

## 5. Examples

---

### 5.1 Variables — Configuration Values

**Situation:** An application has several timeout settings scattered across different subsystems.

```python
# ❌ Ambiguous — which timeout? for what?
timeout = 30
t = 30
conn_timeout = 30

# ✅ Hierarchical — each name narrows left-to-right
db_connection_timeout_seconds   = 30
http_request_timeout_seconds    = 10
cache_eviction_timeout_seconds  = 300
auth_session_timeout_seconds    = 3600
```

**Reading:** `db` → `connection` → `timeout` → unit qualifier `seconds`

---

### 5.2 Constants — Limits and Thresholds

**Situation:** A payment processing module has several numeric limits.

```typescript
// ❌ Ambiguous
const MAX_RETRIES = 3;
const LIMIT = 1000;
const FEE = 0.029;

// ✅ Hierarchical
const PAYMENT_TRANSACTION_RETRY_COUNT_MAX    = 3;
const PAYMENT_TRANSACTION_AMOUNT_LIMIT_USD   = 1_000_000;
const PAYMENT_PROCESSING_FEE_RATE_DEFAULT    = 0.029;
const PAYMENT_REFUND_WINDOW_DAYS_MAX         = 90;
```

**Reading:** `PAYMENT` (domain) → `TRANSACTION` / `REFUND` (category) → `AMOUNT` / `RETRY_COUNT` (property) → `LIMIT` / `MAX` (qualifier)

---

### 5.3 Functions — Actions Within a Domain

**Situation:** A user account service with several operations.

```typescript
// ❌ Too generic or inverted
function update(user) { ... }
function getEmail(userId) { ... }
function verifyToken(token) { ... }

// ✅ Hierarchical — verb follows the domain prefix
function userProfileUpdate(userId, fields) { ... }
function userEmailGet(userId): string { ... }
function userEmailVerify(token): boolean { ... }
function userPasswordResetInitiate(email) { ... }
function userPasswordResetComplete(token, newPassword) { ... }
function userSessionCreate(credentials): Session { ... }
function userSessionInvalidate(sessionId) { ... }
```

**Reading:** `user` (domain) → noun narrowing the sub-area → verb describing the action

> In object-oriented code where the class already carries the `User` prefix, the method name starts from the second component:
> ```typescript
> class UserService {
>   profileUpdate(userId, fields) { ... }
>   emailGet(userId) { ... }
>   sessionCreate(credentials) { ... }
> }
> ```

---

### 5.4 Classes and Types

**Situation:** A data pipeline with several processor and event types.

```python
# ❌ Vague or flat
class Processor: ...
class Event: ...
class Config: ...

# ✅ Hierarchical
class PipelineStageProcessor: ...       # generic→category→role
class PipelineStageProcessorConfig: ... # above + its config bag
class PipelineEventIngestionStart: ...  # pipeline→event→phase→moment
class PipelineEventIngestionComplete: ...
class PipelineEventProcessingError: ...
```

**Reading:** `Pipeline` (system) → `Stage` / `Event` (structural role) → `Processor` / `Ingestion` (specific part) → optional qualifier

---

### 5.5 Booleans and Flags

**Situation:** UI component state and feature flags.

```javascript
// ❌ Unclear meaning or polarity
let loading = true;
let flag = false;
let modal = false;

// ✅ Hierarchical — adjective/state is the rightmost component
let uiModalCheckoutVisible   = false;
let uiButtonSubmitDisabled   = true;
let uiFormPasswordDirty      = false;

let featureFlagDarkModeEnabled        = true;
let featureFlagBetaCheckoutEnabled    = false;
let featureFlagAnalyticsCollectEnabled = true;
```

**Reading:** `ui` / `featureFlag` (domain) → widget/feature name → state adjective

---

### 5.6 Collections and Maps

**Situation:** Caches and lookup tables inside a product catalog service.

```python
# ❌ Generic
items = []
cache = {}
lookup = {}

# ✅ Hierarchical — collection type is rightmost
product_catalog_items_list          = []
product_category_id_name_map        = {}   # maps id → name
product_catalog_price_history_cache = {}
product_tag_frequency_counter       = Counter()
user_wishlist_product_id_set        = set()
```

**Reading:** `product` (domain) → `catalog` / `category` (sub-area) → `items` / `price_history` (content) → `list` / `map` / `cache` (collection kind)

For arrays, lists, sets, and maps, the name must describe what the entries represent in the current business context, not only the container shape or primitive element type. Include qualifiers such as `active`, `claimable`, `recent`, `sorted`, or `pending` only when that state, filter, or ordering changes how the collection is used.

For maps, name the semantic lookup relationship when it is not obvious. The words before `map` should identify what the key represents and what the value represents. For nested maps, name each lookup level in order. If the name becomes difficult to scan, replace the nested map with a named type or class.

```php
// PHP
$activeRoomPlayerIdsList = [];       // active room players, represented by player ID
$offerCodeRewardConfigMap = [];      // offer code → reward configuration
```

```java
// Java
List<Integer> activeRoomPlayerIdsList = List.of();
List<RewardConfig> claimableRewardConfigsList = List.of();
Map<Integer, Map<Integer, CardState>> roomIdPlayerIdCardStateMap = Map.of();
```

```csharp
// C# / Unity
List<int> activeRoomPlayerIdsList = new();
List<PurchaseTransaction> recentPurchaseTransactionsList = new();
Dictionary<int, Dictionary<int, CardState>> roomIdPlayerIdCardStateMap = new();
```

```typescript
// TypeScript / NextJS
const activeRoomPlayerIdsList: number[] = [];
const claimableRewardConfigsList: RewardConfig[] = [];
const roomIdPlayerIdCardStateMap = new Map<number, Map<number, CardState>>();
```

Avoid names that describe only shape or type:

```text
idsList
itemsList
dataArray
stringList
idMap
stringMap
nestedMap
lookupMap
```

---

### 5.7 Error and Exception Types

**Situation:** A file-storage service raises several distinct error conditions.

```python
# ❌ Flat and colliding
class NotFoundError(Exception): ...
class PermissionError(Exception): ...
class QuotaError(Exception): ...

# ✅ Hierarchical
class StorageFileNotFoundError(StorageError): ...
class StorageFilePermissionDeniedError(StorageError): ...
class StorageQuotaExceededError(StorageError): ...
class StorageNetworkConnectionError(StorageError): ...
class StorageBucketRegionMismatchError(StorageError): ...
```

**Reading:** `Storage` (system) → `File` / `Quota` / `Network` (area) → specific condition

---

### 5.8 Event Names and Message Types

**Situation:** An event-driven e-commerce system.

```typescript
// ❌ Flat, collide across domains
type OrderCreated = { ... };
type Updated = { ... };
type Failed = { ... };

// ✅ Hierarchical
type OrderCheckoutInitiated   = { ... };
type OrderCheckoutCompleted   = { ... };
type OrderPaymentAuthorized   = { ... };
type OrderPaymentFailed       = { ... };
type OrderShipmentDispatched  = { ... };
type OrderShipmentDelivered   = { ... };
type InventoryStockDepleted   = { ... };
type InventoryRestockReceived = { ... };
```

**Reading:** `Order` / `Inventory` (aggregate) → `Checkout` / `Payment` / `Shipment` (process) → past-tense verb (event moment)

---

### 5.9. File and Module Names

**Situation:** A large backend service organised as flat files.

```
❌ Flat
utils.py
helpers.js
types.ts
config.yaml

✅ Hierarchical (mirrors the naming strategy in the filesystem)
auth_token_utils.py
auth_session_helpers.py
payment_transaction_types.ts
payment_gateway_stripe_config.yaml
db_migration_runner.py
db_connection_pool_config.py
```

---

### 5.10 Mixed Real-World Module (Python)

```python
# auth/session.py  — everything name-scoped under auth_session_*

AUTH_SESSION_TOKEN_LENGTH_BYTES    = 32
AUTH_SESSION_EXPIRY_SECONDS_DEFAULT = 86_400   # 24 h
AUTH_SESSION_EXPIRY_SECONDS_MAX     = 604_800  # 7 days

class AuthSessionToken:
    """Encapsulates a signed session token and its metadata."""
    value: str
    created_at: datetime
    expiry_seconds: int

class AuthSessionTokenExpiredError(AuthSessionError): ...
class AuthSessionTokenInvalidError(AuthSessionError): ...

def auth_session_create(user_id: str, expiry_seconds: int | None = None) -> AuthSessionToken: ...
def auth_session_validate(token: str) -> AuthSessionToken: ...
def auth_session_invalidate(token: str) -> None: ...
def auth_session_expiry_extend(token: str, extra_seconds: int) -> AuthSessionToken: ...
```

Everything in this module starts with `auth_session_`, so an IDE can autocomplete the entire API by typing `auth_se`.

---

### 5.11 Metrics and Telemetry

**Situation:** An observability system collects performance counters across services.
```python
# ❌ Flat — impossible to distinguish at a glance
requests_total = 0
error_count = 0
latency = 0.0
cache_hit = 0

# ✅ Hierarchical
http_request_total_count              = 0
http_request_error_count              = 0
http_request_latency_ms_p99           = 0.0

db_query_total_count                  = 0
db_query_slow_count                   = 0      # slow = above threshold
db_query_latency_ms_avg               = 0.0

cache_lookup_total_count              = 0
cache_lookup_hit_count                = 0
cache_lookup_miss_count               = 0
```

**Reading:** `http` / `db` / `cache` (system layer) → `request` / `query` / `lookup` (operation) → `latency` / `error` / `hit` (measurement) → unit or statistical qualifier (`ms_p99`, `avg`)

All cache metrics surface together when you type `cache_`; all DB metrics under `db_`; no name collision even though every counter is an integer.

---

### 5.12 React Component Props and State

**Situation:** A reusable data table component with sorting, pagination, and selection.
```typescript
// ❌ Flat — ambiguous across components
interface Props {
  data: Row[];
  loading: boolean;
  page: number;
  total: number;
  selected: string[];
  onSort: (col: string) => void;
}

// ✅ Hierarchical — each prop prefixed by its concern area
interface DataTableProps {
  rowData:                    Row[];

  paginationPageCurrent:      number;
  paginationPageSizeDefault:  number;
  paginationRowTotalCount:    number;

  sortColumnKey:              string;
  sortDirectionAscending:     boolean;

  selectionRowIdsActive:      string[];
  selectionMultipleAllowed:   boolean;

  loadingDataPending:         boolean;
  loadingErrorMessage:        string | null;

  onSortColumnChange:         (columnKey: string) => void;
  onPaginationPageChange:     (page: number) => void;
  onSelectionRowIdsChange:    (ids: string[]) => void;
}
```

**Reading:** `pagination` → `page` → `Current` / `SizeDefault`; `selection` → `row` → `IdsActive`. Typing `pagination` in autocomplete surfaces all three pagination props together; `selection` surfaces both selection props. The prop list self-documents the component's feature surface.

---

### 5.13 Namespaces

Namespaces are the structural embodiment of the left-most component. The folder/module path *is* the generic prefix; the identifier inside it carries only the remaining specific components — avoiding redundant repetition of what the namespace already conveys.

#### Python Packages
```
payments/
  transactions/
    __init__.py        # exports PaymentTransaction*
    limits.py          # exports PaymentTransactionLimit*
    processors.py      # exports PaymentTransactionProcessor*
  refunds/
    __init__.py        # exports PaymentRefund*
    policies.py        # exports PaymentRefundPolicy*
```
```python
# payments/transactions/limits.py
# The module path already says "payment → transaction",
# so identifiers start from the third component onward.

AMOUNT_MAX_USD     = 1_000_000   # full name: payment.transaction.AMOUNT_MAX_USD
RETRY_COUNT_MAX    = 3           # full name: payment.transaction.RETRY_COUNT_MAX
FEE_RATE_DEFAULT   = 0.029

class AmountLimitExceededError(TransactionError): ...
class RetryLimitExceededError(TransactionError):  ...
```
```python
# At the call site the namespace restores the full hierarchy:
from payments.transactions import limits

limits.AMOUNT_MAX_USD          # reads: payment → transaction → amount → max → usd
limits.AmountLimitExceededError
```

#### TypeScript / JavaScript Modules with Barrel Exports
```typescript
// src/auth/session/token.ts
// Namespace path: auth → session → token
// Identifiers inside carry only sub-token detail.

export const LENGTH_BYTES      = 32;    // auth.session.token.LENGTH_BYTES
export const EXPIRY_SECONDS_DEFAULT = 86_400;

export type Payload = { userId: string; issuedAt: number; };

export function create(userId: string): string { ... }
export function verify(raw: string): Payload  { ... }
export function revoke(raw: string): void     { ... }
```
```typescript
// Call site — namespace prefix makes the hierarchy explicit:
import * as AuthSessionToken from '@/auth/session/token';

AuthSessionToken.create(userId);
AuthSessionToken.EXPIRY_SECONDS_DEFAULT;
```

#### C++ Nested Namespaces
```cpp
namespace storage {
namespace file {
namespace cache {

  // Full qualified name: storage::file::cache::*
  constexpr std::size_t ENTRY_SIZE_BYTES_MAX = 4096;
  constexpr std::size_t ENTRY_COUNT_MAX      = 10'000;

  class EntryEvictionPolicy { ... };   // storage::file::cache::EntryEvictionPolicy
  class EntryWriteBuffer    { ... };   // storage::file::cache::EntryWriteBuffer

  void entryInsert(const std::string& key, const Bytes& value);
  void entryEvictExpired();

}}} // storage::file::cache
```

---

### 5.14 Configuration Files

Configuration keys follow the same rule: leftmost key = broadest scope, rightmost key = most specific parameter. In nested formats (YAML, TOML) the hierarchy is expressed structurally; in flat formats (`.env`, Java `.properties`) it is expressed inline.

#### YAML (Nested — hierarchy is structural)
```yaml
# The nesting IS the left-to-right ordering.

db:
  connection:
    host: db.internal
    port: 5432
    pool:
      size_min: 2
      size_max: 20
      idle_timeout_seconds: 300

http:
  server:
    port: 8080
    timeout_seconds: 30
  client:
    retry_count_max: 3
    retry_backoff_ms_initial: 100
    retry_backoff_ms_max: 5000

auth:
  session:
    expiry_seconds_default: 86400
    expiry_seconds_max: 604800
    token_length_bytes: 32
  password:
    bcrypt_rounds: 12
    reset_expiry_seconds: 3600

storage:
  file:
    upload_size_bytes_max: 10485760   # 10 MB
    allowed_mime_types:
      - image/png
      - image/jpeg
      - application/pdf
  cache:
    entry_count_max: 10000
    entry_ttl_seconds: 600
```

#### TOML
```toml
[db.connection]
host = "db.internal"
port = 5432

[db.connection.pool]
size_min             = 2
size_max             = 20
idle_timeout_seconds = 300

[http.client]
retry_count_max          = 3
retry_backoff_ms_initial = 100
retry_backoff_ms_max     = 5000

[auth.session]
expiry_seconds_default = 86400
token_length_bytes     = 32

[storage.file]
upload_size_bytes_max = 10_485_760
```

#### `.env` / Flat Key-Value (hierarchy expressed inline)
```dotenv
# Domain → category → subcategory → specific parameter
# Read left-to-right, underscores as separators.

DB_CONNECTION_HOST=db.internal
DB_CONNECTION_PORT=5432
DB_CONNECTION_POOL_SIZE_MIN=2
DB_CONNECTION_POOL_SIZE_MAX=20
DB_CONNECTION_POOL_IDLE_TIMEOUT_SECONDS=300

HTTP_SERVER_PORT=8080
HTTP_SERVER_TIMEOUT_SECONDS=30
HTTP_CLIENT_RETRY_COUNT_MAX=3
HTTP_CLIENT_RETRY_BACKOFF_MS_INITIAL=100

AUTH_SESSION_EXPIRY_SECONDS_DEFAULT=86400
AUTH_SESSION_TOKEN_LENGTH_BYTES=32
AUTH_PASSWORD_BCRYPT_ROUNDS=12

STORAGE_FILE_UPLOAD_SIZE_BYTES_MAX=10485760
STORAGE_CACHE_ENTRY_COUNT_MAX=10000
STORAGE_CACHE_ENTRY_TTL_SECONDS=600
```

Flat keys read as a path: `DB` → `CONNECTION` → `POOL` → `SIZE_MAX`. Sorting alphabetically groups all `AUTH_*`, `DB_*`, `HTTP_*`, and `STORAGE_*` keys together — the config file self-organises.

---

### 5.15 Database Table and Column Names

Tables are named as `<domain>_<entity>`; columns are named as `<attribute>_<qualifier>`, so the full address `table.column` reads as a four-part hierarchy: `domain → entity → attribute → qualifier`.

#### Table Names
```sql
-- ❌ Flat — no grouping, namespace collisions at scale
CREATE TABLE users       (...);
CREATE TABLE orders      (...);
CREATE TABLE items       (...);
CREATE TABLE logs        (...);

-- ✅ Hierarchical — domain prefix groups related tables
CREATE TABLE auth_user             (...);
CREATE TABLE auth_user_role        (...);
CREATE TABLE auth_session          (...);
CREATE TABLE auth_permission       (...);

CREATE TABLE payment_transaction   (...);
CREATE TABLE payment_refund        (...);
CREATE TABLE payment_method        (...);

CREATE TABLE order_cart            (...);
CREATE TABLE order_cart_item       (...);
CREATE TABLE order_fulfillment     (...);
CREATE TABLE order_shipment        (...);

CREATE TABLE product_catalog       (...);
CREATE TABLE product_category      (...);
CREATE TABLE product_review        (...);

CREATE TABLE audit_event           (...);
CREATE TABLE audit_event_payload   (...);
```

`SHOW TABLES LIKE 'payment%'` or `\dt payment_*` instantly lists the entire payment sub-schema.

#### Column Names
```sql
CREATE TABLE payment_transaction (
    -- Identity
    id                          UUID          PRIMARY KEY,
    -- Foreign keys: referenced_table_id
    auth_user_id                UUID          NOT NULL,
    payment_method_id           UUID          NOT NULL,

    -- Monetary values: attribute + unit
    amount_total_usd            NUMERIC(12,2) NOT NULL,
    amount_fee_usd              NUMERIC(12,2) NOT NULL DEFAULT 0,
    amount_tax_usd              NUMERIC(12,2) NOT NULL DEFAULT 0,

    -- Status / state: attribute + state adjective
    status_current              VARCHAR(50)   NOT NULL,   -- pending, completed, failed
    status_failure_reason       TEXT,

    -- Counts and limits
    retry_count_current         INT           NOT NULL DEFAULT 0,
    retry_count_max             INT           NOT NULL DEFAULT 3,

    -- Timestamps: event_at convention
    created_at                  TIMESTAMPTZ   NOT NULL DEFAULT now(),
    submitted_at                TIMESTAMPTZ,
    completed_at                TIMESTAMPTZ,
    failed_at                   TIMESTAMPTZ
);

CREATE TABLE auth_user (
    id                          UUID          PRIMARY KEY,

    -- Contact
    email_address               VARCHAR(255)  NOT NULL UNIQUE,
    email_verified              BOOLEAN       NOT NULL DEFAULT FALSE,
    email_verified_at           TIMESTAMPTZ,

    -- Authentication
    password_hash               TEXT          NOT NULL,
    password_reset_token        TEXT,
    password_reset_token_expiry TIMESTAMPTZ,

    -- Account state
    account_status_active       BOOLEAN       NOT NULL DEFAULT TRUE,
    account_locked_at           TIMESTAMPTZ,
    account_locked_reason       TEXT,

    -- Timestamps
    created_at                  TIMESTAMPTZ   NOT NULL DEFAULT now(),
    last_login_at               TIMESTAMPTZ
);
```

**Full hierarchical address** at query time:
```sql
SELECT
    pt.amount_total_usd,
    pt.status_current,
    pt.retry_count_current,
    au.email_address,
    au.account_status_active
FROM payment_transaction pt
JOIN auth_user au ON au.id = pt.auth_user_id
WHERE pt.status_current = 'failed'
  AND pt.retry_count_current < pt.retry_count_max;
```

Reading `payment_transaction.amount_total_usd`: `payment` → `transaction` → `amount` → `total` → `usd`. No ambiguity even when ten tables are joined.

#### Index and Constraint Names

Apply the same rule to database object names so `\di` and error messages are self-explanatory:
```sql
-- Indexes: idx_<table>_<column(s)>_<qualifier>
CREATE INDEX idx_payment_transaction_auth_user_id
    ON payment_transaction (auth_user_id);

CREATE INDEX idx_payment_transaction_status_current_created_at
    ON payment_transaction (status_current, created_at DESC);

CREATE UNIQUE INDEX idx_auth_user_email_address_unique
    ON auth_user (email_address);

-- Foreign keys: fk_<child_table>_<parent_table>
ALTER TABLE payment_transaction
    ADD CONSTRAINT fk_payment_transaction_auth_user
    FOREIGN KEY (auth_user_id) REFERENCES auth_user (id);

-- Check constraints: chk_<table>_<column>_<rule>
ALTER TABLE payment_transaction
    ADD CONSTRAINT chk_payment_transaction_amount_total_usd_positive
    CHECK (amount_total_usd > 0);
```
---

## 6 Anti-Patterns to Avoid

| Anti-pattern | Example | Problem |
|---|---|---|
| Generic suffix–first | `managerPayment` | Reads right-to-left; harder to scan |
| Filler nouns | `paymentDataManager` | `data` and `manager` add no meaning |
| Over-abbreviated prefix | `pmtTxn` | Saves keystrokes, loses readability |
| Single-word non-locals | `config`, `list`, `map` | Collides everywhere; says nothing |
| Inconsistent domain prefix | `paymentCreate` vs `orderCreate` vs `createRefund` | Breaks alphabetic grouping |
| Redundant type suffix for collections | `userList` when the type is already `List[User]` | Acceptable when the collection kind matters semantically; otherwise redundant |

---

## 7. Quick Reference Checklist

Before committing a name, ask:

- [ ] Does the leftmost component identify the **domain or system**?
- [ ] Do middle components progressively **narrow** the category?
- [ ] Is the rightmost component the **most specific** trait (state, action, qualifier)?
- [ ] Would typing the first component in autocomplete **surface all related names**?
- [ ] Could someone **unfamiliar with the codebase** guess what the entity does?
- [ ] Is every component **necessary** — does removing any cause ambiguity?

---

*This strategy is language-agnostic and separator-agnostic. Adopt the casing convention of your language and apply the left-to-right generic-to-specific ordering consistently.*
