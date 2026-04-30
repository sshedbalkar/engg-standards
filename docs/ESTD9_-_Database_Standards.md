# ESTD9 - Database Standards and Best Practices

**ESTD9 — Database Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD9 |
| Version | 7.2 |
| Status | Active |
| Last Updated | 2026-04-30 |
| Applies To | All engineers designing schemas, writing queries, operating backups, or shipping migrations against the platform databases  |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure) |
| Approval | Director of Engineering / Server Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD9 is the authoritative database standard for both Bingo games. It defines how data is modeled, queried, migrated, backed up, and operated safely across the legacy PHP monolith, the new Java/SEAM microservices, SmartFox persistence checkpoints, and internal tools.

MySQL on AWS RDS is the default authoritative transactional datastore across the platform. The new Bingo SEAM microservices are the approved exception: they use MongoDB Atlas as their primary data store per the original architectural decision. All other proposals to introduce a different primary datastore require a written exception (see [§2. Database Standard: MySQL by Default and Exception Process](#2-database-standard-mysql-by-default-and-exception-process)). Read [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices) for service-boundary rules and [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure) for AWS implementation details; this document defines how application data itself must be stored and changed.

---

- [ESTD9 - Database Standards and Best Practices](#estd9---database-standards-and-best-practices)
  - [How to Use This Document](#how-to-use-this-document)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Database Standard: MySQL by Default and Exception Process](#2-database-standard-mysql-by-default-and-exception-process)
  - [3. Database Selection Guide: MySQL vs MongoDB Atlas](#3-database-selection-guide-mysql-vs-mongodb-atlas)
    - [3.1 Choosing the Right Database](#31-choosing-the-right-database)
    - [3.2 MongoDB Atlas in Our Architecture](#32-mongodb-atlas-in-our-architecture)
  - [4. Database Design Principles](#4-database-design-principles)
    - [4.1 Single Responsibility per Schema and Clear Ownership](#41-single-responsibility-per-schema-and-clear-ownership)
    - [4.2 Normalize for Correctness; De-normalize for Measured Performance](#42-normalize-for-correctness-de-normalize-for-measured-performance)
    - [4.3 Data Integrity Is the Database's Job](#43-data-integrity-is-the-databases-job)
    - [4.4 Audit Columns](#44-audit-columns)
  - [5. Naming Conventions](#5-naming-conventions)
    - [5.1 MySQL: Tables, Columns, Constraints, and Indexes](#51-mysql-tables-columns-constraints-and-indexes)
    - [5.2 MongoDB: Databases, Collections, and Fields](#52-mongodb-databases-collections-and-fields)
    - [5.3 Legacy Monolith Modules and Service-Owned Schemas](#53-legacy-monolith-modules-and-service-owned-schemas)
  - [6. Column and Field Data Type Standards](#6-column-and-field-data-type-standards)
    - [6.1 MySQL: Integer Types](#61-mysql-integer-types)
    - [6.2 MySQL: String Types](#62-mysql-string-types)
    - [6.3 Dates and Times](#63-dates-and-times)
    - [6.4 Currency and Financial Data](#64-currency-and-financial-data)
    - [6.5 Status, Enum, and Boolean Columns](#65-status-enum-and-boolean-columns)
    - [6.6 JSON Columns in MySQL](#66-json-columns-in-mysql)
    - [6.7 MongoDB Field Types](#67-mongodb-field-types)
  - [7. Indexing Standards](#7-indexing-standards)
    - [7.1 Every Table Must Have a Primary Key](#71-every-table-must-have-a-primary-key)
    - [7.2 Foreign Key Columns Must Be Indexed](#72-foreign-key-columns-must-be-indexed)
    - [7.3 Index Queries, Not Tables](#73-index-queries-not-tables)
    - [7.4 Composite Indexes](#74-composite-indexes)
    - [7.5 Query Plan Verification (`EXPLAIN`) Is Mandatory](#75-query-plan-verification-explain-is-mandatory)
    - [7.6 MongoDB Indexes](#76-mongodb-indexes)
  - [8. Query Writing Standards](#8-query-writing-standards)
    - [8.1 Parameterized Queries Only](#81-parameterized-queries-only)
    - [8.2 Select Specific Columns / Projections](#82-select-specific-columns--projections)
    - [8.3 `LIMIT` on All Queries That Can Return Multiple Rows](#83-limit-on-all-queries-that-can-return-multiple-rows)
    - [8.4 Cursor-Based Pagination](#84-cursor-based-pagination)
    - [8.5 Avoid Functions on Indexed Columns in WHERE Clauses](#85-avoid-functions-on-indexed-columns-in-where-clauses)
  - [9. Schema Versioning and Migrations](#9-schema-versioning-and-migrations)
    - [9.1 Migration Tool Requirements](#91-migration-tool-requirements)
    - [9.2 Migration Naming Convention](#92-migration-naming-convention)
    - [9.3 Migration Rules](#93-migration-rules)
    - [9.4 The Expand-Contract Pattern for Zero-Downtime Migrations](#94-the-expand-contract-pattern-for-zero-downtime-migrations)
    - [9.5 Large Table Migrations](#95-large-table-migrations)
    - [9.6 Data Backfills and Verification](#96-data-backfills-and-verification)
    - [9.7 MongoDB Schema Versioning](#97-mongodb-schema-versioning)
  - [10. Transactions and Concurrency](#10-transactions-and-concurrency)
    - [10.1 InnoDB Storage Engine (MySQL)](#101-innodb-storage-engine-mysql)
    - [10.2 Transaction Isolation Level (MySQL)](#102-transaction-isolation-level-mysql)
    - [10.3 Optimistic Locking with Version Columns](#103-optimistic-locking-with-version-columns)
    - [10.4 MongoDB Transactions](#104-mongodb-transactions)
    - [10.5 Deadlock Prevention (MySQL)](#105-deadlock-prevention-mysql)
  - [11. Database Access Control and Permission Boundaries](#11-database-access-control-and-permission-boundaries)
    - [11.1 Separate Database Users per Purpose](#111-separate-database-users-per-purpose)
    - [11.2 Service Schema Isolation (New Architecture)](#112-service-schema-isolation-new-architecture)
    - [11.3 Database Security Vulnerabilities](#113-database-security-vulnerabilities)
    - [11.4 Browser Clients Must Not Access Databases Directly](#114-browser-clients-must-not-access-databases-directly)
  - [12. Data Retention and GDPR/CCPA Compliance](#12-data-retention-and-gdprccpa-compliance)
  - [13. Backup and Recovery Standards](#13-backup-and-recovery-standards)
  - [14. Performance Standards](#14-performance-standards)
    - [14.1 Slow Query Logging](#141-slow-query-logging)
  - [15. Common Pitfalls to Avoid](#15-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

Why this document exists: a 15-year live-service game accumulates data-model shortcuts, migration risks, and query-pattern drift unless the database layer is governed intentionally. Databases are the foundation of data integrity in the Bingo game. A poorly designed schema, a missing index, or an unmanaged migration script can lead to data loss, performance degradation, or a production outage that is very difficult to reverse. This document standardises the rules that protect player accounts, balances, reward claims, content schedules, room history, and audit trails.

Database assignments by system:

```
┌──────────────────────────────────────────────────────────────────────────┐
│  SYSTEM                              DATABASE         HOSTING            │
├──────────────────────────────────────────────────────────────────────────┤
│  Classic Bingo — PHP API (monolith)  MySQL            AWS RDS            │
│  Classic Bingo — Web Tools backend   MySQL            AWS RDS            │
│  New Bingo — SEAM microservices      MongoDB Atlas    MongoDB Atlas SaaS │
│  New Bingo — Web Tools configuration MySQL            AWS RDS            │
│  SmartFox live server (both games)   Persists to the  game's primary DB  │
└──────────────────────────────────────────────────────────────────────────┘
```

This standard applies to:

- the legacy PHP monolith's MySQL schema;
- the new Bingo Java/SEAM service-owned MongoDB Atlas databases (one Atlas cluster per microservice domain);
- read replicas used for reporting or non-critical read scaling;
- the web tools configuration databases (MySQL on AWS RDS, for both classic and new Bingo tools);
- migration tooling, data backfills, and restore testing;
- any service or tool that reads or writes authoritative game data.

It does not make Redis, S3, or analytics sinks into primary stores of record. Those systems may support the platform, but authoritative transactional truth remains in the appropriate primary database for each system: MySQL for classic Bingo and all web tools; MongoDB Atlas for new SEAM microservices.

---

## 2. Database Standard: MySQL by Default and Exception Process

MySQL is the default unless there is an approved written exception. The default storage choices are:

| Need | Default Choice | Notes |
|:-----|:---------------|:------|
| Authoritative transactional data | MySQL table(s) | Default for players, balances, rewards, inventory, room history, content config, and entitlement state |
| Flexible optional metadata attached to one aggregate | MySQL JSON column | Acceptable only when query patterns are limited and documented |
| Cache / session / rate limit / locks | Redis | Never the only copy of authoritative data | 
| Binary objects / exports / assets | S3 | Store the object key in MySQL; do not place blobs in relational hot paths |
| Reporting / exports / heavy read workloads | MySQL read replica or downstream warehouse fed from MySQL | Replica lag must be understood; no strict read-after-write assumptions — a row written to the primary may not appear on the replica for milliseconds to seconds, so code that writes and then immediately reads the same row must target the primary, not the replica |

**Approved exception — New Bingo SEAM microservices**: All new Bingo game microservices use MongoDB Atlas as their primary data store. This is the approved architectural decision for the new game. MySQL is used within new Bingo only for web tools configuration. See [§3. Database Selection Guide: MySQL vs MongoDB Atlas](#3-database-selection-guide-mysql-vs-mongodb-atlas) for guidance on choosing the right database within this approved context.

**All other exceptions** to the MySQL-by-default rule require all of the following before implementation begins:

1. an ADR (Architecture Decision Record) that explains the problem MySQL cannot reasonably solve;
2. consistency, durability, backup, restore, and failure-mode analysis;
3. query and access-pattern examples showing why the exception is warranted;
4. an operational ownership plan (monitoring, upgrades, on-call competency);
5. a migration and rollback strategy.

warning **"The data is flexible" or "the JSON is easier" is not sufficient justification for adopting a different primary data-store than MySQL.**

---

## 3. Database Selection Guide: MySQL vs MongoDB Atlas

Both MySQL and MongoDB Atlas are in active use in the Bingo architecture. This section defines the criteria for choosing each database within its approved context, and documents the MongoDB Atlas capabilities relied upon in the new Bingo game.

### 3.1 Choosing the Right Database

```
MYSQL (Relational)                        MONGODB ATLAS (Document)
─────────────────────────────────────     ─────────────────────────────────────
USE WHEN:                                 USE WHEN:
  Data has clear, stable relationships      Data structure varies per document
  (players → purchases → items)            (player event logs, session data)

  ACID transactions are essential           Documents are read/written as a unit
  (coin balance updates, purchases)         (player profile with nested inventory)

  Reporting or analytics queries needed     Schema evolves frequently
  (JOINs across multiple tables)            (feature configuration, CMS data)

  Data integrity constraints required       High write throughput needed
  (foreign keys, unique constraints)        (game event streams, audit trails)

EXAMPLES IN OUR ARCHITECTURE:            EXAMPLES IN OUR ARCHITECTURE:
  player_accounts (core identity)           player_game_sessions
  coin_transactions (ledger — append only)  content_configurations
  purchase_receipts                         player_event_logs
  reward_claims                             feature_experiment_assignments
  room_definitions
```

**For the new Bingo SEAM microservices**: Use MongoDB Atlas. This is the architectural decision for the new game — all microservice data lives in Atlas. If a microservice needs strongly-consistent transactional writes (e.g., coin ledger), implement these within MongoDB Atlas using multi-document transactions (see [§10.4 MongoDB Transactions](#104-mongodb-transactions)). Do not add a MySQL dependency to a SEAM microservice for transactional consistency.

**For the classic Bingo game and all web tools configuration data**: Use MySQL. Do not introduce MongoDB into the classic Bingo stack.

### 3.2 MongoDB Atlas in Our Architecture

The new Bingo game uses MongoDB Atlas (MongoDB's fully managed cloud service) rather than a self-hosted MongoDB cluster. Atlas handles replication, backups, monitoring, auto-scaling storage, and fail-over automatically. Engineers work with connection strings and the MongoDB driver; the operational layer is managed by Atlas.

Key Atlas capabilities relied upon:

- **Atlas Backups**: Continuous oplog backup with point-in-time restore. No manual `mongodump` is required for production backups.
- **Atlas Performance Advisor**: Automatically recommends indexes for slow queries. Consult the Performance Advisor as part of the quarterly index review.
- **Atlas Search**: Full-text search on collections without a separate cluster.
- **Atlas Data API / App Services**: Not permitted for direct player-facing data access without Architect approval. All player data access must go through the SEAM microservice layer.

---

## 4. Database Design Principles

### 4.1 Single Responsibility per Schema and Clear Ownership

In the new architecture, each service owns its own MySQL schema or MongoDB collection namespace. One service must not read or write another service's tables or collections directly. Cross-service data access happens through APIs or events, not through shared table or collection coupling.

The legacy PHP monolith is allowed to operate in a shared schema because it is already a monolith. Even there, new modules should preserve clear table ownership and naming — using a module prefix convention (e.g., `events_`, `rewards_`, `rooms_`) — so later extraction remains possible.

### 4.2 Normalize for Correctness; De-normalize for Measured Performance

Start with normalized relational design. Duplicate or precomputed data is allowed only when it solves a measured performance problem and the ownership/update strategy is documented. Denormalization without an explicit refresh or invalidation strategy creates silent integrity bugs.

### 4.3 Data Integrity Is the Database's Job

Application validation is necessary but insufficient. The database must enforce invariants wherever practical.

Required controls include:

- primary keys on every table / `_id` on every MongoDB collection;
- foreign keys where relational integrity matters and write patterns support them — use FKs on stable, low-to-moderate-write relationships (e.g., `reward_claims.player_id → players.player_id`) where orphaned rows would cause data corruption; skip FKs on high-write event streams, append-only audit logs, or tables that will be extracted into a separate service, because the database must verify the referenced row on every insert/update, adding write latency and lock contention;
- `NOT NULL` on required columns;
- `UNIQUE` constraints for idempotency and natural uniqueness rules;
- `CHECK` constraints where supported and useful;
- sane default values for timestamps and status flags;
- MongoDB schema validation (`$jsonSchema`) for collections with structured documents.

If a rule matters enough to mention in code review, it usually matters enough to enforce at the schema level too.

**Why app-only validation is insufficient:** Application code can have bugs, be bypassed by direct DB access (admin scripts, migration backfills, support tooling), or lose a race condition between concurrent requests. The database is the last line of defence — constraints at the schema level guarantee invariants hold even when application logic fails.

**MongoDB `$jsonSchema` validation example:**

```javascript
db.createCollection("rewardClaims", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["playerId", "rewardId", "contentCycleId", "coinsAwarded", "createdAt"],
            properties: {
                playerId:       { bsonType: "long",   description: "must be a long and is required" },
                rewardId:       { bsonType: "string", description: "must be a string and is required" },
                contentCycleId: { bsonType: "long",   description: "must be a long and is required" },
                coinsAwarded:   { bsonType: "long",   minimum: 0, description: "non-negative integer" },
                createdAt:      { bsonType: "date",   description: "must be a date" }
            }
        }
    },
    validationAction: "error"  // reject invalid documents; use "warn" for migration periods
});
```

Without `$jsonSchema`, MongoDB accepts any shape — a typo like `coisAwarded` silently creates a new field with no error.

### 4.4 Audit Columns

Every business-significant table or collection must include at minimum:

- `created_at_utc DATETIME(3)` or `TIMESTAMP(3)` (MySQL) / `createdAt: Date` (MongoDB);
- `updated_at_utc DATETIME(3)` or `TIMESTAMP(3)` (MySQL) / `updatedAt: Date` (MongoDB);
- `deleted_at_utc` for soft-delete tables, when soft delete is justified.

Tables that record sensitive or economic actions should also store the actor or source where appropriate (`created_by_user_id`, `source_system`, `request_id`).

MySQL example:

```sql
CREATE TABLE reward_claims (
    reward_claim_id  BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    player_id        BIGINT UNSIGNED NOT NULL,
    reward_id        VARCHAR(64)     NOT NULL,
    content_cycle_id BIGINT UNSIGNED NOT NULL,
    coins_awarded    BIGINT UNSIGNED NOT NULL,
    created_at_utc   DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    updated_at_utc   DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
        ON UPDATE CURRENT_TIMESTAMP(3),
    UNIQUE KEY unq_reward_claim_player_reward_cycle (player_id, reward_id, content_cycle_id)
) ENGINE=InnoDB;
```

MongoDB equivalent:

```javascript
// Mongoose schema — audit fields managed via pre-save middleware
const rewardClaimSchema = new Schema({
    playerId:       { type: Number, required: true },
    rewardId:       { type: String, required: true },
    contentCycleId: { type: Number, required: true },
    coinsAwarded:   { type: Number, required: true },
    createdAt:      { type: Date,   default: () => new Date() },
    updatedAt:      { type: Date,   default: () => new Date() },
});
rewardClaimSchema.pre('save', function (next) {
    this.updatedAt = new Date();
    next();
});
```

---

## 5. Naming Conventions

### 5.1 MySQL: Tables, Columns, Constraints, and Indexes

Use `snake_case` for all MySQL database identifiers.

| Object | Convention | Example |
|:-------|:-----------|:--------|
| Schema | Product or service scoped | `classic_bingo`, `reward_service` |
| Table | Plural noun | `players`, `reward_claims`, `content_cycles` |
| Primary key column | `<entity>_id` | `player_id`, `reward_claim_id` |  
| Foreign key column | Referenced key name | `player_id`, `room_id` |
| Unique index | `unq_<table>_<purpose>` | `unq_reward_claim_player_reward_cycle` | 
| Non-unique index | `idx_<table>_<columns>` | `idx_players_status_last_seen` | 
| Foreign key constraint | `fk_<table>_<referenced_table>` | `fk_reward_claims_players` |
| Check constraint | `chk_<table>_<rule>` | `chk_coin_transactions_non_negative_amount` |
| View | `v_<name>` | `v_active_rooms` |

Avoid abbreviations unless they are universally understood in the domain (`utc`, `id`, `ttl`).

### 5.2 MongoDB: Databases, Collections, and Fields

Use `snake_case` for MongoDB database and collection names. Use `camelCase` for document field names.

| Object | Convention | Example |
|:-------|:-----------|:--------|
| Database | `snake_case` | `bingo_player_service`, `bingo_events` |
| Collection | `snake_case`, plural | `player_sessions`, `game_events` | 
| Field | `camelCase` | `playerId`, `coinBalance`, `createdAt` |
| Index name | `{collection}_{field(s)}_idx` | `player_sessions_playerId_idx` |

### 5.3 Legacy Monolith Modules and Service-Owned Schemas

The legacy PHP monolith may continue to use a single schema, but new tables should reflect module ownership clearly (`content_cycles`, `reward_claims`, `player_sessions`, `tool_audit_logs`).

In the new Java/SEAM architecture, prefer one service-owned schema per bounded context. If a temporary shared cluster is used, ownership must still be explicit in schema naming and migration ownership.

---

## 6. Column and Field Data Type Standards

### 6.1 MySQL: Integer Types

- Use `BIGINT UNSIGNED` for player IDs, room IDs, transaction IDs, and any identifier that can grow for years.
- Use `INT UNSIGNED` only when the lifetime cardinality is clearly bounded — i.e., the total number of rows the table will ever hold is predictable and well within the 4.29 billion `INT UNSIGNED` ceiling (e.g., a status lookup table, a room-type catalog, or a reward-tier definition table).
- Use `TINYINT(1)` for booleans.
- Do not use signed integer types for values that can never be negative.

### 6.2 MySQL: String Types

- Use `VARCHAR` with an explicit maximum length for nearly all textual columns.
- Use `CHAR` only for truly fixed-width values (e.g., short format codes, UUIDs stored as `CHAR(36)`).
- Reserve `TEXT` for large freeform content that is not part of a latency-sensitive access path.
- Use UTF-8 (`utf8mb4`) for all schemas and tables.

| Use Case | Type |
|:---------|:-----|
| Player usernames | `VARCHAR(64)` | 
| Email addresses | `VARCHAR(320)` |
| UUIDs / idempotency keys | `CHAR(36)` or `BINARY(16)` |
| Short, fixed-format codes | `CHAR(n)` |

**Collation** Collation defines how a database sorts and compares strings—it determines sort order, case sensitivity, and accent handling for character data. Different collations enforce different rules (e.g., case-insensitive vs. case-sensitive, ASCII vs. UTF-8 multi-byte characters), so it's needed to ensure consistent string behavior across queries, indexes, and joins and to match business requirements (e.g., a case-insensitive player-name lookup might fail silently with the wrong collation).

**`COLLATE`:** The default collation for `utf8mb4` is `utf8mb4_0900_ai_ci` (accent-insensitive, case-insensitive). This is correct for most player-facing text. When case-sensitive comparison is required — such as idempotency keys, reward codes, or API tokens — specify `COLLATE utf8mb4_bin` on the column.

```sql
-- Case-insensitive (default) — suitable for player usernames
username VARCHAR(64) NOT NULL

-- Case-sensitive — required for idempotency keys and tokens
idempotency_key VARCHAR(64) NOT NULL COLLATE utf8mb4_bin
```

### 6.3 Dates and Times

Store timestamps in UTC only. Application code converts to local time zones for display.

- Prefer `DATETIME(3)` or `TIMESTAMP(3)` for event timestamps to capture millisecond precision.
- Never store local timezone wall-clock values as authoritative truth.
- Date-only business concepts (e.g., content schedule day) may use `DATE` if time-of-day is irrelevant.
- The MySQL session time zone must be set to UTC at the connection level.

```php
// PHP — set UTC at connection establishment
$pdo->exec("SET time_zone = '+00:00'");
```

```java
// Java — JDBC connection URL parameter
jdbc:mysql://host/db?serverTimezone=UTC
```

### 6.4 Currency and Financial Data

Never store money-like values in floating-point columns. Binary floating-point cannot represent decimal fractions exactly — `0.1 + 0.2 != 0.3` in floating-point arithmetic.

- Coins, tickets, and soft currency: `BIGINT UNSIGNED`
- Real-money amounts: `DECIMAL(18, 6)` or stricter, based on the payment domain

### 6.5 Status, Enum, and Boolean Columns

- Use normalized lookup tables when the set of values is large or needs metadata. A normalized lookup table is a separate table that maps an integer or short-code primary key to a human-readable label and optional metadata (e.g., `reward_types(reward_type_id, name, display_order, is_active)`), referenced via foreign key from the main table.
- Use compact `VARCHAR` or integer-backed enums when the value set is small and stable.
- Never overload a boolean column to represent multiple states. If more than two states exist, use an explicit status column.

### 6.6 JSON Columns in MySQL

JSON columns are permitted for sparse, optional, or auxiliary attributes that do not justify immediate normalization, but they are not a license to avoid schema design.

*JSON columns are acceptable only when:*

- the data belongs to a single owning row;
- query patterns are limited and documented;
- frequently filtered fields are surfaced through generated columns or copied to first-class relational columns;
- validation happens at the application boundary.

Do not place hot-path relational data such as balances, reward claims, or entitlement state only inside JSON blobs. If you find yourself writing `JSON_EXTRACT()` in a `WHERE` clause, the data belongs in a proper column.

### 6.7 MongoDB Field Types

Use explicit type coercion when reading MongoDB documents in application code. MongoDB is flexible about types at the storage layer, but your application must not be.

**Collation in MongoDB:** By default, MongoDB string comparisons are binary (case-sensitive and accent-sensitive). To enable case-insensitive sorting or filtering — e.g., player name search — specify a collation at the collection or query level.

```javascript
// Collection-level default collation (case-insensitive English)
db.createCollection("players", { collation: { locale: "en", strength: 2 } });

// Query-level collation override for a single operation
db.players.find({ username: "BingoKing" }).collation({ locale: "en", strength: 2 });
```

Strength `1` = accent-insensitive + case-insensitive. Strength `2` = case-insensitive, accent-sensitive. Strength `3` (default) = exact binary match. Use `strength: 2` for most player-facing lookups.

```java
// ALWAYS specify the type when reading — do not rely on implicit conversion
int    playerId    = document.getInteger("playerId");
long   coinBalance = document.getLong("coinBalance");
Date   createdAt   = document.getDate("createdAt");
String rewardId    = document.getString("rewardId");
```

---

## 7. Indexing Standards

Add an index when a query's `WHERE`, `JOIN`, or `ORDER BY` clause would otherwise cause a full table/collection scan on a non-trivial dataset. Do not add an index speculatively — every index speeds up reads but slows down writes because the database must update the index on every `INSERT`, `UPDATE`, and `DELETE`. Verify every new index with `EXPLAIN` (MySQL) or `.explain("executionStats")` (MongoDB) on production-sized data before merging. Remove unused indexes quarterly — they consume storage and write I/O for zero benefit.

### 7.1 Every Table Must Have a Primary Key

Every table requires a primary key. Heap-like tables — tables with no clustered index, where rows are stored in arbitrary insertion order with no guaranteed structure for lookups or ordering — without a primary key are prohibited. MongoDB automatically creates `_id` indexes on every collection.

### 7.2 Foreign Key Columns Must Be Indexed

Any column used to join to another table must have a supporting index unless the primary key or an existing composite index already covers it. MySQL does not automatically create indexes for foreign key columns — always create an explicit index alongside the constraint.

```sql
-- Always create an index alongside the FK constraint
ALTER TABLE reward_claims
    ADD CONSTRAINT fk_reward_claims_players
    FOREIGN KEY (player_id) REFERENCES players(player_id);

CREATE INDEX idx_reward_claims_player_id ON reward_claims (player_id);
```

### 7.3 Index Queries, Not Tables

Add indexes to support real query patterns, not because a column "looks important." Before adding an index, identify the exact `WHERE`, `JOIN`, and `ORDER BY` clauses the index is meant to accelerate.

### 7.4 Composite Indexes

Composite indexes must reflect the actual left-to-right access pattern of the query. Equality predicates come before range predicates; sorting columns must be considered if the query relies on index order.

```sql
-- Query: WHERE player_id = ? AND content_cycle_id = ? ORDER BY created_at_utc DESC
-- Equality predicates first, then the sort column
CREATE INDEX idx_reward_claims_player_cycle_created
    ON reward_claims (player_id, content_cycle_id, created_at_utc DESC);
```

**Why left-to-right order matters:** A composite index is a sorted tree. The database walks it left-to-right: equality columns narrow to an exact position, but once it hits a range predicate (e.g., `>`, `BETWEEN`, `$gte`), everything to the right of that column can no longer narrow — it must scan. Putting equality columns first and range/sort columns last maximises the portion of the index the engine can use.

```
WRONG ORDER                               CORRECT ORDER
idx(created_at DESC, player_id)           idx(player_id, content_cycle_id, created_at DESC)
 ↳ range scan on created_at first          ↳ equality jump to player_id
   ↳ then filter player_id (scans many)      ↳ equality jump to cycle
                                                ↳ already sorted on created_at
```

**MongoDB compound index — same principle:**

```javascript
// Query: { playerId: 123, contentCycleId: 7 } sorted by { createdAt: -1 }
// Equality fields first, sort field last
db.rewardClaims.createIndex({ playerId: 1, contentCycleId: 1, createdAt: -1 });
```

### 7.5 Query Plan Verification (`EXPLAIN`) Is Mandatory

New or materially changed queries on non-trivial tables must be checked with `EXPLAIN` (or the service's equivalent query-plan capture) before merge.

Review for:

- **full table scans on large tables** — `EXPLAIN` shows `type: ALL` (MySQL) or `COLLSCAN` (MongoDB), meaning the engine reads every row/document instead of using an index; acceptable on tiny lookup tables, never on million-row tables;
- **filesort / temp-table creation on hot queries** — `Using filesort` or `Using temporary` in MySQL's `Extra` column means the engine must sort or materialize results outside the index, adding CPU and memory overhead on every execution;
- **wrong index choice due to low selectivity** — the optimizer picks an index that matches the query columns but filters poorly (e.g., an index on a `status` column with only 3 distinct values across 50M rows), causing nearly as much work as a full scan;
- **read replica plans diverging from primary due to missing statistics refresh** — replicas maintain their own index statistics; if `ANALYZE TABLE` hasn't run recently on the replica, its optimizer may choose a different (worse) plan than the primary for the same query.

"It seemed fast on dev data" is not evidence. A query that returns in 2ms on 1,000 rows may take 8 seconds on 50 million rows because the query planner chose a full table scan — the plan can change as data volume and distribution shift.

**MySQL `EXPLAIN` example:**

```sql
EXPLAIN SELECT reward_claim_id, created_at_utc
FROM reward_claims
WHERE player_id = 42 AND content_cycle_id = 7
ORDER BY created_at_utc DESC
LIMIT 10;
```

```
+----+------+----------------------------------------------+---------+------+----------+-----------+
| id | type | key                                          | key_len | ref  | rows     | Extra     |
+----+------+----------------------------------------------+---------+------+----------+-----------+
|  1 | ref  | idx_reward_claims_player_cycle_created       | 16      | const|       34 |           |
+----+------+----------------------------------------------+---------+------+----------+-----------+
```

What to verify:

| Field | Good sign | Bad sign |
|:------|:----------|:---------|
| `type` | `ref`, `eq_ref`, `range`, `const` | `ALL` (full table scan) |
| `key` | Named index matching your query | `NULL` (no index used) |
| `rows` | Low relative to table size | Close to total row count |
| `Extra` | `Using index` (covering index) | `Using filesort`, `Using temporary` |

**MongoDB `.explain("executionStats")` equivalent:**

```javascript
db.rewardClaims.find(
    { playerId: 42, contentCycleId: 7 }
).sort({ createdAt: -1 }).limit(10).explain("executionStats");
```

What to look for in the output:

| Field | Good sign | Bad sign |
|:------|:----------|:---------|
| `winningPlan.stage` | `IXSCAN` (index scan) | `COLLSCAN` (collection scan) |
| `totalDocsExamined` | Close to `nReturned` | Orders of magnitude larger than `nReturned` |
| `executionTimeMillis` | Under 200ms | Hundreds of ms or seconds |

### 7.6 MongoDB Indexes

```javascript
// Single-field index for common lookups
db.playerSessions.createIndex({ playerId: 1 });

// Compound index matching query patterns
db.gameEvents.createIndex({ roomId: 1, eventType: 1, createdAt: -1 });

// Unique index for idempotency / deduplication
db.rewardClaims.createIndex(
    { playerId: 1, rewardId: 1, contentCycleId: 1 },
    { unique: true, name: "unq_reward_claims_player_reward_cycle" }
);

// TTL index — automatically expire documents when expiresAt is in the past
db.playerSessions.createIndex(
    { expiresAt: 1 },
    { expireAfterSeconds: 0 }
);
```

---

## 8. Query Writing Standards

### 8.1 Parameterized Queries Only

All database access must use parameterized queries / prepared statements. String concatenation of user or external input into SQL is prohibited. Never accept raw filter objects from external input in MongoDB queries.

```php
// PHP — PDO parameterization
$stmt = $pdo->prepare(
    'SELECT reward_claim_id, created_at_utc
       FROM reward_claims
      WHERE player_id = :playerId
        AND reward_id = :rewardId
      LIMIT 1'
);
$stmt->execute([
    ':playerId' => $playerId,
    ':rewardId' => $rewardId,
]);
```

```java
// Java — JDBC parameterization
PreparedStatement stmt = connection.prepareStatement(
    "SELECT player_id, coin_balance FROM players WHERE player_id = ?"
);
stmt.setLong(1, playerId);
```

```java
// MongoDB — explicit field specification
// ❌ BAD — MongoDB injection if filter comes from user input
db.players.find(req.body.filter);

// ✅ GOOD — explicit field specification with type coercion
db.players.findOne({ playerId: parseInt(req.params.playerId, 10) });
```

**Note**: Dynamic identifiers such as sort columns or table names cannot be parameterized; they must come from an **allowlist**.

### 8.2 Select Specific Columns / Projections

Avoid `SELECT *` in application code. Request only the columns needed for that use case. This reduces I/O, narrows coupling, and makes index-only strategies possible.

```sql
-- ❌ BAD — fetches all columns, including large or sensitive ones
SELECT * FROM players WHERE player_id = :playerId;

-- ✅ GOOD — only the columns needed
SELECT player_id, username, coin_balance, last_login_at
FROM   players
WHERE  player_id = :playerId;
```

```javascript
// ✅ MongoDB — project only needed fields
db.players.findOne(
    { _id: playerId },
    { projection: { username: 1, coinBalance: 1, lastLoginAt: 1 } }
);
```

### 8.3 `LIMIT` on All Queries That Can Return Multiple Rows

Any query expected to return one row must say so explicitly with `LIMIT 1`. Any query that can grow without bound must enforce pagination or an upper bound.

```sql
SELECT player_id, username FROM players ORDER BY created_at_utc DESC LIMIT 100;
```

```javascript
db.players.find({}).sort({ createdAt: -1 }).limit(100);
```

### 8.4 Cursor-Based Pagination

Offset pagination is acceptable for small operator-facing tables, but player-facing or large-data pagination must use cursor/seek pagination when consistency and scale matter.

**Why `OFFSET` degrades:** `OFFSET N` does not skip to row N directly — the database reads and discards all N preceding rows on every request. Page 1 reads 50 rows; page 1,000 reads 50,000 rows and discards 49,950. On a 15-year table with millions of rows, deep pages become unusable. Cursor-based pagination uses a `WHERE` clause anchored to the last-seen row, so every page is a constant-cost indexed lookup regardless of position.

```sql
-- ❌ BAD — OFFSET scans all preceding rows; gets exponentially slower
SELECT * FROM players ORDER BY player_id LIMIT 100 OFFSET 50000;

-- ✅ GOOD — cursor-based; constant performance regardless of page
SELECT reward_claim_id, created_at_utc
FROM reward_claims
WHERE player_id = :playerId
  AND (created_at_utc < :cursorTs
       OR (created_at_utc = :cursorTs AND reward_claim_id < :cursorId))
ORDER BY created_at_utc DESC, reward_claim_id DESC
LIMIT 50;
```

**How the cursor query works:** The caller passes in the `created_at_utc` and `reward_claim_id` of the last row it received (the "cursor"). The `WHERE` clause fetches only rows that sort after that cursor position. The `OR` branch handles the tie-breaking case: when multiple rows share the same `created_at_utc`, the query falls back to `reward_claim_id` to maintain a deterministic, stable page boundary. Because the query uses an indexed seek instead of scanning and discarding prior rows, every page costs the same regardless of how deep into the result set it is.

```javascript
// MongoDB cursor-based pagination
db.players.find({ _id: { $gt: lastSeenId } })
          .sort({ _id: 1 })
          .limit(100);
```

### 8.5 Avoid Functions on Indexed Columns in WHERE Clauses

Expressions such as `DATE(created_at_utc) = ?` or `YEAR(created_at) = ?` prevent index use. Rewrite predicates as range comparisons instead.

```sql
-- ❌ BAD — index on created_at_utc is not used
WHERE DATE(created_at_utc) = '2026-03-23'

-- ✅ GOOD — index is used
WHERE created_at_utc >= '2026-03-23 00:00:00'
  AND created_at_utc < '2026-03-24 00:00:00'
```

**The same principle applies in MongoDB.** Using `$expr` with aggregation operators like `$year` or `$dayOfMonth` in a `find()` filter forces a collection scan — MongoDB cannot use an index on the computed result.

```javascript
// ❌ BAD — $expr defeats the index on createdAt
db.gameEvents.find({
    $expr: { $eq: [{ $dayOfMonth: "$createdAt" }, 23] }
});

// ✅ GOOD — range query uses the index on createdAt
const dayStart = new Date("2026-03-23T00:00:00Z");
const dayEnd   = new Date("2026-03-24T00:00:00Z");
db.gameEvents.find({
    createdAt: { $gte: dayStart, $lt: dayEnd }
});
```

---

## 9. Schema Versioning and Migrations

Database schemas change over time — columns are added, renamed, or removed; indexes are created; tables are restructured. Without a versioned, tracked migration system, it is impossible to know what state any environment's schema is in, impossible to reproduce a schema from scratch, and very easy to apply a change to production that was never tested in staging.

### 9.1 Migration Tool Requirements

Every schema must use an ordered, source-controlled migration system. Ad hoc console edits are prohibited except under an emergency break-glass procedure, and every break-glass change must be backfilled into a formal migration immediately afterward.

| Server | Tool | Notes |
|:-------|:-----|:------|
| Legacy PHP + MySQL | Phinx or custom migration runner | Migration files stored in `db/migrations/` |
| New Java microservices + MySQL | Flyway (framework-integrated) | Auto-applies pending migrations on startup |
| New Java microservices + MongoDB | `mongock` or SEAM migration runner | Document the migration library choice per service |

### 9.2 Migration Naming Convention

Use timestamp-prefixed, descriptive migration names. The name must describe the change plainly enough that an on-call engineer can understand what it did without opening the file.

**MySQL (Flyway):**

```
V{major}_{minor}_{patch}__{description}.sql

V1_0_0__create_players_table.sql
V1_1_0__add_coin_balance_to_players.sql
V2_0_0__add_weekly_event_tables.sql
V2_1_0__add_idempotency_key_to_reward_claims.sql
```

**MySQL (PHP / Phinx):**

```
YYYYMMDDHHMMSS_description.php

20260101120000_create_players_table.php
20260312104500_add_gdpr_deletion_request_table.php
```

**MongoDB:**

```
{version}__{description}.js

001__create_player_sessions_collection.js
002__add_expiry_index_to_player_sessions.js
003__add_content_cycle_id_to_reward_claims.js
```

### 9.3 Migration Rules

| Rule | Rationale |
|:-----|:----------|
| Migrations are immutable once applied to staging or production. Never modify an applied migration — create a new one to correct it. | Modifying applied migrations breaks migration tool checksums and version tracking. |
| Each migration must be idempotent (`CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS`). | Retrying a failed migration must be safe. |
| Every migration must state whether it is **forward-only or reversible**. Risky migrations must include a rollback note in the PR. | Enables controlled recovery if the migration causes issues. |
| Migrations must be **backward-compatible** (expand-contract pattern — see [§9.4 The Expand-Contract Pattern for Zero-Downtime Migrations](#94-the-expand-contract-pattern-for-zero-downtime-migrations)). | Code and migration deploy together; code may need rollback but the migration stays. |
| Never drop a column or table in the same migration that removes the application code referencing it. | During a rolling deployment, old application instances still reference the column; dropping it while those instances are live causes immediate query failures and breaks zero-downtime deploys. |
| Manual data-fix steps are not acceptable substitutes for a migration script. | Untracked manual edits cause environment drift and silent schema divergence. |
| Migration scripts must be reviewed in the PR by at least one engineer who is not the author. | Schema changes are hard to reverse; a second reviewer catches mistakes. |
| Run migrations against staging and verify before applying to production. | Catch issues early, including execution time on production-sized data. |

### 9.4 The Expand-Contract Pattern for Zero-Downtime Migrations

Breaking schema changes must use expand-contract:

```
Phase 1 — EXPAND:       Add the new column / table / index while old code still works.
Phase 2 — DUAL-WRITE:   New code writes to both old and new representations;
                         backfill old data into the new column.
Phase 3 — READ SWITCH:  Deploy code that reads the new representation only.
Phase 4 — CONTRACT:     Remove the old column or behavior only after all live
                         code has moved. Deploy as a separate PR.
```

**Example: renaming** `reward_type` to `reward_category`:

```sql
-- Phase 1 migration: Expand — add new column
ALTER TABLE rewards ADD COLUMN reward_category VARCHAR(64) AFTER reward_type;

-- Phase 4 migration (separate PR, deployed after Phase 3 is confirmed stable):
ALTER TABLE rewards DROP COLUMN reward_type;
```

Never deploy code that requires a destructive schema change to have already happened unless the migration window is explicitly planned and the system is offline.

**Why the 4-phase ordering matters:** Code deployments can be rolled back in minutes; schema changes often cannot. If you drop a column and then need to roll back the code, the old code crashes because the column is gone. Expand-contract decouples the two: the schema is always a superset of what any live code version needs, so rollbacks are safe at every phase boundary.

**MongoDB expand-contract equivalent:**

MongoDB is schemaless at storage, but the application schema and any `$jsonSchema` validators still need expand-contract discipline. Renaming a field from `coins` to `coinBalance`:

```
Phase 1 — EXPAND:       Application writes both `coins` and `coinBalance` on every update.
                         $jsonSchema validator is relaxed to accept either field.
Phase 2 — BACKFILL:     Background script copies `coins` → `coinBalance` for old documents.
Phase 3 — READ SWITCH:  Application reads from `coinBalance` only; still writes both.
Phase 4 — CONTRACT:     Application stops writing `coins`. Background script runs
                         $unset on `coins`. Validator updated to require `coinBalance` only.
```

See [§9.7 MongoDB Schema Versioning](#97-mongodb-schema-versioning) for the `schemaVersion` field pattern that supports this.

### 9.5 Large Table Migrations

On large tables, avoid blocking table rebuilds during peak hours. Use `pt-online-schema-change` (Percona Toolkit) or `gh-ost` (GitHub Online Schema Transmogrifier) for large MySQL tables where `ALTER TABLE` would hold a table-level lock for minutes. Batch backfills must run in chunks, with monitoring on replication lag and lock time. Always test execution time on a production-sized data copy before scheduling the migration.

A migration that is safe on dev data can still be production-hostile on a 15-year table.

**Why `ALTER TABLE` is dangerous on large tables:** Most MySQL `ALTER TABLE` operations (adding a column, changing a type, adding an index) internally create a full copy of the table with the new schema, copy every row, then swap the tables. During this process, a metadata lock blocks concurrent DML (Data Manipulation Language). On a table with hundreds of millions of rows, this can take minutes to hours — locking out all reads and writes to that table for the duration.

`pt-online-schema-change` and `gh-ost` avoid this by creating a shadow table, copying rows in small batches, capturing live changes via triggers (`pt-osc`) or binlog tailing (`gh-ost`), and performing an atomic rename at the end. The table remains fully available throughout.

**MongoDB large collection operations:**

MongoDB 4.2+ builds indexes in the background by default, but other bulk operations still need care:

- **Adding or tightening a `$jsonSchema` validator** on a large collection: validate existing documents first with an aggregation pipeline (`$match` against the new schema), then apply the validator. Invalid documents will be rejected by future writes — identify and fix them before enabling `validationAction: "error"`.
- **Bulk field renames or reshaping** (e.g., `$rename`, `$unset` across millions of documents): run in chunked batches using a cursor with `limit` + `skip` or an `_id` range, with monitoring on oplog lag for replica sets.

```javascript
// Chunked bulk rename — process 5,000 documents per batch
let lastId = ObjectId("000000000000000000000000");
while (true) {
    const batch = db.playerSessions.find({ _id: { $gt: lastId }, schemaVersion: 1 })
                                   .sort({ _id: 1 })
                                   .limit(5000)
                                   .toArray();
    if (batch.length === 0) break;
    const ops = batch.map(doc => ({
        updateOne: {
            filter: { _id: doc._id },
            update: { $rename: { coins: "coinBalance" }, $set: { schemaVersion: 2 } }
        }
    }));
    db.playerSessions.bulkWrite(ops, { ordered: false });
    lastId = batch[batch.length - 1]._id;
}
```

### 9.6 Data Backfills and Verification

A data backfill is a scripted operation that populates or corrects data in existing rows/documents after a schema change — for example, filling a newly added `reward_category` column for millions of existing rows that predate the column. Backfills are needed because schema migrations only change structure; they do not retroactively compute or copy values for data that was written before the migration ran.

Every backfill must define:

- the source of truth;
- chunk size and retry rules;
- idempotency behavior;
- verification queries;
- rollback or compensation strategy.

Verification is part of the migration, not an optional afterthought.

### 9.7 MongoDB Schema Versioning

MongoDB is schemaless at the storage layer, but your application is not. When a document format changes, use a schema version field and a migration strategy:

```javascript
// Option A: Document version field + lazy migration in application code
// Migration happens when the document is next read — no batch migration needed
function loadPlayerSession(doc) {
    if (doc.schemaVersion === 1) {
        // Migrate v1 → v2: field renamed from 'coins' to 'coinBalance'
        doc.coinBalance = doc.coins;
        delete doc.coins;
        doc.schemaVersion = 2;
        db.playerSessions.replaceOne({ _id: doc._id }, doc);
    }
    return doc;
}

// Option B: Background migration script (for time-sensitive changes)
// 004__migrate_player_sessions_v1_to_v2.js
db.playerSessions.find({ schemaVersion: 1 }).forEach(doc => {
    db.playerSessions.updateOne(
        { _id: doc._id },
        { $rename: { coins: "coinBalance" }, $set: { schemaVersion: 2 } }
    );
});
```

---

## 10. Transactions and Concurrency

### 10.1 InnoDB Storage Engine (MySQL)

All transactional tables must use InnoDB. MyISAM is prohibited — it does not support transactions or foreign keys.

### 10.2 Transaction Isolation Level (MySQL)

The platform default is MySQL's InnoDB `REPEATABLE READ` unless a specific workload has a documented reason to use a different isolation level. For operations where reading the most current committed value is critical (e.g., reading a lock status), use `READ COMMITTED` for that specific transaction. The choice must be deliberate and tested.

### 10.3 Optimistic Locking with Version Columns

For hot rows such as balances or room aggregates, optimistic locking is preferred when it reduces contention without sacrificing correctness.

**Optimistic vs pessimistic locking:** Pessimistic locking (`SELECT ... FOR UPDATE`) acquires a row-level lock before reading, blocking all other transactions that touch the same row until the lock holder commits. This is safe but serialises throughput. Optimistic locking reads without locking, then checks a version column at write time — if the version changed since the read, the write fails and the caller retries. On high-throughput rows where conflicts are infrequent (the common case for per-player balances), optimistic locking avoids blocking entirely and scales better.

Use pessimistic locking only when conflicts are frequent and retries are expensive (e.g., multi-step workflows where partial progress is costly to discard).

**Pessimistic locking (MySQL):**

```sql
-- Acquires an exclusive row-level lock on the matched row.
-- All other transactions that SELECT ... FOR UPDATE or attempt to UPDATE
-- this row will block until this transaction commits or rolls back.
BEGIN;
SELECT coin_balance, version
  FROM players
 WHERE player_id = :playerId
   FOR UPDATE;

-- Safe to modify — no other transaction can change this row until we COMMIT.
UPDATE players
   SET coin_balance   = coin_balance - :amount,
       version        = version + 1,
       updated_at_utc = CURRENT_TIMESTAMP(3)
 WHERE player_id      = :playerId
   AND coin_balance   >= :amount;
COMMIT;
```

**Optimistic locking (MySQL):**

```sql
-- No lock is acquired during the read. Instead, the UPDATE's WHERE clause
-- checks that the version has not changed since the read. If another
-- transaction modified the row in between, the version will differ and
-- zero rows are updated — the caller must detect this and retry.
UPDATE players
   SET coin_balance   = coin_balance - :amount,
       version        = version + 1,
       updated_at_utc = CURRENT_TIMESTAMP(3)
 WHERE player_id      = :playerId
   AND version        = :expectedVersion
   AND coin_balance   >= :amount;
```

If the affected row count is zero, the caller must treat that as a concurrency conflict or insufficient balance, and must retry or return a controlled error.

**MongoDB optimistic locking with a version field:**

```javascript
// Read the document and note its version
const player = await db.players.findOne({ _id: playerId });
const expectedVersion = player.version;

// Conditional update — fails if another write incremented version
const result = await db.players.findOneAndUpdate(
    { _id: playerId, version: expectedVersion, coinBalance: { $gte: amount } },
    { $inc: { coinBalance: -amount, version: 1 }, $set: { updatedAt: new Date() } },
    { returnDocument: 'after' }
);
if (!result) {
    // Version mismatch or insufficient balance — retry or return error
    throw new ConcurrencyConflictError(playerId, expectedVersion);
}
```

### 10.4 MongoDB Transactions

MongoDB 4.0+ supports multi-document ACID (Atomicity Consistency Isolation Durability) transactions for replica sets. Use transactions when multiple documents must be updated atomically and a failure partway through must leave no partial writes.

```javascript
const session = client.startSession();
try {
    await session.withTransaction(async () => {
        await db.coinLedger.insertOne(
            { playerId, amount: -100, type: 'PURCHASE', ts: new Date() },
            { session }
        );
        await db.players.updateOne(
            { _id: playerId, coinBalance: { $gte: 100 } },
            { $inc: { coinBalance: -100 } },
            { session }
        );
    });
} finally {
    await session.endSession();
}
```

For single-document operations, MongoDB's atomic `findOneAndUpdate` is often sufficient and does not require a full transaction:

```javascript
// Atomic single-document update — no transaction needed
const result = await db.players.findOneAndUpdate(
    { _id: playerId, coinBalance: { $gte: amount } },  // Precondition: sufficient balance
    { $inc: { coinBalance: -amount } },
    { returnDocument: 'after' }
);
if (!result.value) {
    throw new InsufficientBalanceError(playerId, amount);
}
```

### 10.5 Deadlock Prevention (MySQL)

Deadlocks are normal under concurrency and must be handled intentionally.

Rules:

- **Acquire locks in a consistent table and row order across all transactions.** If Transaction A locks `players` then `coin_transactions` while Transaction B locks `coin_transactions` then `players`, a deadlock is inevitable. Establish a global ordering (e.g., always lock `players` before `coin_transactions`) and sort row-level locks by primary key when updating multiple rows in the same table.
- **Keep transactions as short as possible.** A transaction that reads a player row, calls an external reward API, then writes back holds a row lock for the entire API round-trip. Move the API call outside the transaction: read, release, call API, then open a new transaction to write.
- **Avoid user I/O or network calls while a transaction is open.** Similar to above — if a transaction sends an HTTP request to a payment provider and the provider is slow, the held locks block every other transaction touching those rows until the network call completes or times out.
- **Use `SELECT ... FOR UPDATE` only on the specific rows that will be modified.** Locking `SELECT * FROM players FOR UPDATE` without a `WHERE` clause locks the entire table. Always scope to the exact row: `SELECT ... FROM players WHERE player_id = :playerId FOR UPDATE`.
- **Catch deadlock exceptions and retry only where the operation is safe to retry.** MySQL raises error 1213 (`ER_LOCK_DEADLOCK`) when it detects a deadlock and kills one transaction. The killed transaction's changes are rolled back, so retrying it is safe. Non-idempotent operations (e.g., sending a push notification inside the transaction) must not be retried blindly — separate the side effect from the transaction.

---

## 11. Database Access Control and Permission Boundaries

Database access control is the data-layer form of the trust and permission boundary model in [ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions) and [ESTD4 §17.6 Server Trust and Permission Boundaries](./ESTD4_-_Server_Engg_Standards.md#176-server-trust-and-permission-boundaries). A database credential is a permission boundary: it defines the maximum damage possible if the application, tool, job, or script using that credential is compromised.

Over-privileged database users are production risks, not cleanup tasks. An application runtime user with migration, admin, or cross-schema permissions can turn a single endpoint bug into schema damage, broad player-data exposure, or irreversible data corruption. Use separate users by purpose, schema, environment, and operational role.

### 11.1 Separate Database Users per Purpose

Use separate MySQL users/credentials for each access role:

| User | Permissions| Used By |
|:-----|:-----------|:--------|
| `app_readwrite` | SELECT, INSERT, UPDATE, DELETE on own schema only | Application services |
| `app_readonly` | SELECT on own schema only | Read replicas, reporting queries | 
| `migrations_user` | Data Definition Language - DDL (CREATE, ALTER, DROP) on own schema | CI/CD pipeline migrations only | 
| `monitoring_user` | SELECT on performance schema, PROCESS | Monitoring tools (Datadog) |
| Root / superadmin | All | Never used by applications; break-glass only |

The application runtime user must not own schema-migration privileges.

**Why a single "admin" connection string is a blast-radius risk:** If the application's database credentials are leaked or the application is compromised, the attacker inherits every privilege those credentials hold. A single admin user means the attacker can drop collections, export all player data, or modify schema validators. Separate users constrain the blast radius to the minimum privilege each component actually needs.

**MongoDB Atlas role equivalents:**

| Atlas User | Built-in Role | Used By |
|:-----------|:-------------|:--------|
| `app_readwrite` | `readWrite` on service DB only | SEAM microservice runtime |
| `app_readonly` | `read` on service DB only | Reporting queries, read replicas |
| `migrations_user` | `dbAdmin` on service DB (allows `createCollection`, `createIndex`, validator changes) | CI/CD migration scripts only |
| `monitoring_user` | `clusterMonitor` | Monitoring / alerting tools |
| `atlas_admin` | `atlasAdmin` | Break-glass only; never used by applications |

Create these users in the Atlas UI or via the Atlas Admin API. Each SEAM microservice should have its own `app_readwrite` user scoped to its database only — not a cluster-wide user.

### 11.2 Service Schema Isolation (New Architecture)

In the new Bingo architecture, a service may access only its own schema or collection namespace directly. If `reward_service` needs data owned by `profile_service`, it uses the profile API or a replicated integration view explicitly designed for that purpose. Shared-database convenience today becomes extraction pain tomorrow.

### 11.3 Database Security Vulnerabilities

| Vulnerability | What It Looks Like in Our Environment | Required Controls |
|:--------------|:--------------------------------------|:------------------|
| **Excessive database privileges** | Application accounts can alter schema, read unrelated datasets, or perform admin-only actions if compromised | Use separate DB users by purpose; restrict privileges to the minimum required operation set |
| **Broad data exposure through queries or exports** | Services or internal tools return full rows, broad result sets, or data exports containing fields not needed for the task | Select only required columns; paginate by default; restrict export permissions; audit bulk-access paths |
| **Unencrypted backups, snapshots, or dumps** | Logical dumps or snapshots expose player data outside the primary database path | Encrypt backups at rest; restrict access; test restore processes without weakening access controls |
| **Retention drift / incomplete deletion of PII** | Old player records, support data, or exported files remain available longer than policy allows | Apply retention rules, deletion workflows, and privacy reviews consistently across primary data and derived copies |
| **Integrity loss through unsafe concurrency** | Concurrent reward, purchase, or economy updates create lost updates or double-spend scenarios | Use transactions, optimistic locking, unique constraints, and explicit conflict handling for critical economic tables |
| **Unsafe migrations or backfills** | Emergency data patches, one-off scripts, or large backfills bypass review and accidentally expose or corrupt sensitive data | Treat migrations and data scripts as production code; review them in PR; use expand-contract and verification steps |

### 11.4 Browser Clients Must Not Access Databases Directly

Website clients and web-tool clients must never connect directly to the main game database, website database, or tools database. Browser-delivered code, public Next.js routes, static assets, WebGL launcher pages, and any publicly reachable frontend must call an API server or tool backend that enforces authentication, authorization, input validation, rate limits, audit logging, and least-privilege database credentials.

Database hosts, ports, connection strings, drivers, admin consoles, and database API endpoints must not be reachable from public frontend networks or embedded in frontend bundles. Internal tools may be VPN-gated, but the tool client is still not a trusted database boundary.

Approved patterns:

- product website client -> website API/backend -> database;
- web tools client -> tools API/backend -> tools database or approved game API;
- operator/reporting job -> server-side worker or backend API -> database with purpose-scoped credentials.

Prohibited patterns:

- website or web tools browser code connecting to MySQL, MongoDB Atlas, RDS Proxy, Atlas Data API, phpMyAdmin, Adminer, or direct database HTTP adapters;
- public frontend routes proxying arbitrary SQL, MongoDB filters, table names, or collection names from user input;
- exposing database connection details through `NEXT_PUBLIC_*`, frontend configuration files, JavaScript bundles, HTML, logs, or browser storage.

---

## 12. Data Retention and GDPR/CCPA Compliance

Retention periods must be documented per data category. Data that contains player identifiers must have a defined deletion or anonymization path. Do not keep data "forever just in case" unless a legal, fraud, or finance requirement is documented.

Minimum rules:

- Identify all tables and collections containing a player's PII and document the deletion or anonymization procedure.
- Use anonymization (replacing PII with non-identifiable tokens) rather than physical deletion where it would break referential integrity (e.g., the `player_id` column in a `coin_transactions` table can remain; the associated email/name in `players` is anonymized).
- Data used for fraud detection and financial reconciliation has a longer statutory retention period — consult the compliance team before deleting.
- Audit tables must state retention in schema docs or operational runbooks.
- Exports containing player data must have explicit expiry and deletion jobs.
- Backups are subject to their own retention schedule and restoration controls.

---

## 13. Backup and Recovery Standards

MySQL recovery capability must include:

- automated RDS backups with point-in-time recovery enabled;
- daily backups with a minimum 14-day retention for production;
- manual snapshots before risky production migrations;
- monthly restore tests — execute the full restore procedure on the staging database, verify data integrity, and document the procedure and time taken;
- documented runbooks for primary failover and restore.

For MongoDB Atlas: continuous oplog backup with point-in-time restore is handled automatically by Atlas (see [§3.2 MongoDB Atlas in Our Architecture](#32-mongodb-atlas-in-our-architecture)). Validate Atlas restore capability on a quarterly cadence.

Read replicas improve resilience and read scale, but they are not backups. See [ESTD8 §7. Amazon RDS (MySQL)](./ESTD8_-_AWS_Standards.md#7-amazon-rds-mysql) and [ESTD8 §8. Amazon RDS Read Replicas and Database Scaling](./ESTD8_-_AWS_Standards.md#8-amazon-rds-read-replicas-and-database-scaling) for AWS implementation guidance.

---

## 14. Performance Standards

Database performance is part of feature delivery, not a later tuning phase.

Required controls:

- slow-query logging enabled in production (threshold: 500ms — catches chronic offenders without excessive log noise);
- all queries with the potential to be in the API hot path must be tested with `EXPLAIN` before merging;
- no query should exceed **200ms p95** under normal production load;
- connection pools sized deliberately (`RDS Proxy` for PHP where used; bounded `JDBC/HikariCP` pools for Java services; MongoDB driver's built-in pool for Atlas);
- read replicas used only for workloads that tolerate replica lag — never assume strong read-after-write consistency from a replica;
- periodic review of top tables by size, growth rate, and index bloat — unused indexes add write overhead; review and prune quarterly.

### 14.1 Slow Query Logging

A **slow query** is any query whose execution time exceeds a configured threshold. Slow queries are the primary signal for performance regression in production — a single unindexed query running 50 times per second at 2 seconds each can saturate a connection pool and cascade into a full outage. Slow query logs turn invisible performance debt into actionable alerts.

**MySQL slow query log:**

MySQL has a built-in slow query log. Enable it in the RDS parameter group (or `my.cnf` for non-RDS instances):

```
-- RDS parameter group settings (applied via AWS Console or Terraform)
slow_query_log       = 1
long_query_time      = 0.5          -- 500ms threshold; matches our §14 standard
log_queries_not_using_indexes = 1   -- also log queries that do full table scans
log_output           = TABLE        -- logs to mysql.slow_log table; use FILE for disk
```

Query the slow log table directly to find top offenders:

```sql
-- Top 10 slowest queries in the last 24 hours
SELECT query_time, lock_time, rows_examined, rows_sent,
       LEFT(sql_text, 200) AS query_preview
FROM   mysql.slow_log
WHERE  start_time >= NOW() - INTERVAL 1 DAY
ORDER BY query_time DESC
LIMIT 10;
```

In production, pipe the slow log to your observability stack (Datadog, CloudWatch) for alerting. Set an alert when slow query count exceeds a threshold per minute.

**MongoDB slow query profiler:**

MongoDB's database profiler captures operations that exceed a configurable threshold. Enable it per database:

```javascript
// Enable profiling — level 1 logs operations slower than the threshold
db.setProfilingLevel(1, { slowms: 500 });

// Level 0 = off, Level 1 = slow ops only, Level 2 = all ops (use only for short debugging)
```

Query the `system.profile` collection to find slow operations:

```javascript
// Top 10 slowest operations in the last 24 hours
db.system.profile.find({
    ts: { $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
}).sort({ millis: -1 }).limit(10).forEach(op => {
    print(`${op.millis}ms | ${op.op} | ${op.ns} | ${JSON.stringify(op.command).substring(0, 200)}`);
});
```

For Atlas: use the **Atlas Performance Advisor** and **Real-Time Performance Panel** instead of manual profiling. Atlas automatically surfaces slow queries and recommends indexes — review these as part of the quarterly index review.

---

## 15. Common Pitfalls to Avoid

| # | Pitfall | Impact | Remedy |
|:--|:--------|:-------|:-------|
| 1 | `SELECT *` in hot paths | Excess I/O, tighter coupling, broken projections on schema change | Select only needed columns; use MongoDB projections |
| 2 | Storing coins or money in floats | Precision drift causing incorrect balances | Use `BIGINT` for soft currency; `DECIMAL(18,6)` for real money |
| 3 | Adding indexes without verifying query plans | Slower writes, no read benefit | Run `EXPLAIN`; index the actual query pattern |
| 4 | Missing unique guardrails on idempotent operations | Duplicate reward claims or purchases | Add `UNIQUE` constraints plus idempotency logic |
| 5 | Cross-service direct table or collection access | Tight coupling, migration risk | Use API or event boundaries |
| 6 | Treating a read replica as strongly consistent | Stale reads after writes | Keep critical read-after-write flows on primary |
| 7 | Large blocking migrations during peak traffic | Latency spike or outage | Use expand-contract and pt-online-schema-change / gh-ost |
| 8 | JSON blob used as an excuse to skip schema design | Unqueryable, unvalidated data | Normalize or surface generated/indexed fields |
| 9 | Long-lived transactions with network or I/O calls inside | Lock contention, deadlocks | Keep transactions short and local |
| 10 | Manual production data edits with no migration or audit trail | Drift, silent corruption | Use formal migrations or audited break-glass procedure |
| 11 | OFFSET-based pagination on large tables | Exponential performance degradation as page number increases | Use cursor-based / keyset pagination |
| 12 | Modifying an applied migration | Breaks migration tool checksums; environment drift | Always create a new migration file to correct errors |
| 13 | Dropping a column before removing all code references | Application crash on deploy | Expand-contract: remove code first, drop column in a separate later deployment |
| 14 | Missing schema validation in MongoDB | Documents with unexpected shapes; runtime errors | Use `$jsonSchema` validators on collections |
| 15 | Single-node MongoDB in production | Node failure = data unavailable | MongoDB Atlas replica sets enforce a minimum of 3 nodes automatically |
| 16 | Storing timestamps in local time zone | Incorrect calculations across DST transitions | Store UTC everywhere; convert to local time in the display layer only |
| 17 | Browser clients connect directly to databases | Public or tool frontends can bypass API auth, validation, rate limits, and audit logs | Route browser clients through API servers or backend tool services only |
