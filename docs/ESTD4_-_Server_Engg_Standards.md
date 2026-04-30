# ESTD4 - Server Engineering Standards and Best Practices

**ESTD4 — Server Engineering Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD4 |
| Version | 5.3 |
| Status | Active |
| Last Updated | 2026-04-30 |
| Applies To | All server engineers (PHP API, Java microservices, SmartFox live server) |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) |
| Approval | Director of Engineering / Server Architect |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD4 defines the server-wide standards that apply across the legacy PHP API monolith, the new Java/SEAM API services, and the SmartFox live server. Read [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) first, then use ESTD4 as the cross-stack server baseline. Language- and platform-specific details live in [ESTD6](./ESTD6_-_PHP_Programming_Standards.md#estd6---php-programming-standards) (PHP), [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server) (Java/SEAM), and [ESTD12](./ESTD12_-_Smartfox_Server_Standards.md#estd12--smartfox-server-standards-for-bingo-game-development) (SmartFox); this document defines the shared architectural, operational, API, security, and reliability expectations across all server work.

When a rule here conflicts with a language-specific document, apply the more restrictive rule and escalate any ambiguity to the Server Architect.

---

## Table of Contents

- [ESTD4 - Server Engineering Standards and Best Practices](#estd4---server-engineering-standards-and-best-practices)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Server Architecture Principles](#2-server-architecture-principles)
    - [2.1 The Server Is the Authority](#21-the-server-is-the-authority)
    - [2.2 Legacy PHP Monolith: Living With It](#22-legacy-php-monolith-living-with-it)
    - [2.3 New Java API: Microservice Design Principles](#23-new-java-api-microservice-design-principles)
    - [2.4 Both API Servers Must Be Stateless](#24-both-api-servers-must-be-stateless)
  - [3. Stateful vs. Stateless Servers](#3-stateful-vs-stateless-servers)
    - [3.1 Definitions](#31-definitions)
    - [3.2 Side-by-Side Comparison](#32-side-by-side-comparison)
    - [3.3 How They Work Together in Our Architecture](#33-how-they-work-together-in-our-architecture)
    - [3.4 Operational Implications](#34-operational-implications)
  - [4. API Design Standards](#4-api-design-standards)
    - [4.1 Purpose](#41-purpose)
    - [4.2 URL Design](#42-url-design)
    - [4.3 HTTP Methods](#43-http-methods)
    - [4.4 Request & Response Structure](#44-request--response-structure)
      - [4.4.1 Client and Server API Contract Finalization](#441-client-and-server-api-contract-finalization)
    - [4.5 HTTP Status Codes](#45-http-status-codes)
    - [4.6 Versioning](#46-versioning)
    - [4.7 Pagination](#47-pagination)
    - [4.8 Idempotency for Unsafe Operations](#48-idempotency-for-unsafe-operations)
    - [4.9 The Non-Negotiables](#49-the-non-negotiables)
    - [4.10 Client-Version Compatibility and Deprecation Windows](#410-client-version-compatibility-and-deprecation-windows)
  - [5. Authentication and Authorization](#5-authentication-and-authorization)
    - [5.1 Token-Based Authentication](#51-token-based-authentication)
    - [5.2 Session Storage](#52-session-storage)
    - [5.3 Authorization](#53-authorization)
  - [6. Input Validation at the Server Boundary](#6-input-validation-at-the-server-boundary)
  - [7. Rate Limiting and Abuse Prevention](#7-rate-limiting-and-abuse-prevention)
    - [7.1 Why It Matters](#71-why-it-matters)
    - [7.2 Core Techniques](#72-core-techniques)
    - [7.3 Things to Keep in Mind](#73-things-to-keep-in-mind)
    - [7.4 Example: Token Bucket — PHP Implementation](#74-example-token-bucket--php-implementation)
    - [7.5 Rate Limits](#75-rate-limits)
  - [8. Idempotency](#8-idempotency)
    - [8.1 When Idempotency Is Required](#81-when-idempotency-is-required)
    - [8.2 Approach 1: Idempotency Keys (POST endpoints — general approach)](#82-approach-1-idempotency-keys-post-endpoints--general-approach)
    - [8.3 Approach 2: Database-Level Unique Constraints (last-resort guardrail)](#83-approach-2-database-level-unique-constraints-last-resort-guardrail)
    - [8.4 Approach 3: Conditional Updates with Version Fields (optimistic locking in monolith)](#84-approach-3-conditional-updates-with-version-fields-optimistic-locking-in-monolith)
    - [8.5 Approach 4: SmartFox Idempotency via Sequence IDs](#85-approach-4-smartfox-idempotency-via-sequence-ids)
    - [8.6 Approach 5: Microservice Idempotency via Distributed Idempotency Store](#86-approach-5-microservice-idempotency-via-distributed-idempotency-store)
    - [8.7 Handling Malicious Clients: Rotating Idempotency Keys](#87-handling-malicious-clients-rotating-idempotency-keys)
  - [9. Boundary Functions — Server-Side Structure](#9-boundary-functions--server-side-structure)
    - [9.1 Boundary Functions in the SEAM Framework](#91-boundary-functions-in-the-seam-framework)
  - [10. Anatomy of a Good Request Handler](#10-anatomy-of-a-good-request-handler)
    - [10.1 The Nine-Step Structure](#101-the-nine-step-structure)
    - [10.2 Annotated Example (PHP)](#102-annotated-example-php)
    - [10.3 Handler Rules](#103-handler-rules)
  - [11. Object-Relational Mapping (ORM)](#11-object-relational-mapping-orm)
    - [11.1 ORM Policy by Server](#111-orm-policy-by-server)
    - [11.2 Repository Pattern (All Servers)](#112-repository-pattern-all-servers)
    - [11.3 The N+1 Query Problem](#113-the-n1-query-problem)
    - [11.4 ORM Transactions](#114-orm-transactions)
  - [12. Background Jobs and Async Processing](#12-background-jobs-and-async-processing)
    - [12.1 Job Queue Standards](#121-job-queue-standards)
    - [12.2 Idempotent Jobs](#122-idempotent-jobs)
    - [12.3 Content Reset Jobs](#123-content-reset-jobs)
    - [12.4 Scheduled Jobs Catalog](#124-scheduled-jobs-catalog)
  - [13. Concurrency and Thread Safety](#13-concurrency-and-thread-safety)
    - [13.1 PHP Monolith](#131-php-monolith)
    - [13.2 Java Microservices](#132-java-microservices)
    - [13.3 SmartFox Server](#133-smartfox-server)
    - [13.4 Economic Operations Must Use Locks](#134-economic-operations-must-use-locks)
    - [13.5 Distributed Locks for Critical Cross-Service Sections](#135-distributed-locks-for-critical-cross-service-sections)
    - [13.6 Shared Data in Multi-Process Systems](#136-shared-data-in-multi-process-systems)
  - [14. Service Communication Patterns](#14-service-communication-patterns)
    - [14.1 Legacy PHP Monolith](#141-legacy-php-monolith)
    - [14.2 Java Microservices Communication](#142-java-microservices-communication)
    - [14.3 PHP API ↔ Java API](#143-php-api--java-api)
    - [14.4 SmartFox ↔ Authoritative API (Internal API)](#144-smartfox--authoritative-api-internal-api)
  - [15. Caching Strategy](#15-caching-strategy)
    - [15.1 What to Cache (Server-Side)](#151-what-to-cache-server-side)
    - [15.2 Cache-Aside Pattern](#152-cache-aside-pattern)
    - [15.3 Cache Invalidation](#153-cache-invalidation)
    - [15.4 Cache Stampede Prevention](#154-cache-stampede-prevention)
    - [15.5 When NOT to Cache](#155-when-not-to-cache)
    - [15.6 Advantages and Risks](#156-advantages-and-risks)
  - [16. Observability: Logging, Metrics, Alerting](#16-observability-logging-metrics-alerting)
    - [16.1 Minimum Required Metrics (Datadog)](#161-minimum-required-metrics-datadog)
    - [16.2 Understanding Metric Types](#162-understanding-metric-types)
    - [16.3 Health Check Endpoint](#163-health-check-endpoint)
  - [17. Security Standards](#17-security-standards)
    - [17.1 Defense in Depth](#171-defense-in-depth)
    - [17.2 Input Validation](#172-input-validation)
    - [17.3 Injection and Unsafe Query Construction — Zero Tolerance](#173-injection-and-unsafe-query-construction--zero-tolerance)
    - [17.4 Audit Logging](#174-audit-logging)
    - [17.5 Server/API Security Vulnerabilities](#175-serverapi-security-vulnerabilities)
    - [17.6 Server Trust and Permission Boundaries](#176-server-trust-and-permission-boundaries)
  - [18. Deployment and Configuration](#18-deployment-and-configuration)
    - [18.1 Zero-Downtime Deployments](#181-zero-downtime-deployments)
    - [18.2 Feature Flags](#182-feature-flags)
    - [18.3 Build Promotion Policy](#183-build-promotion-policy)
  - [19. Disaster Recovery Readiness](#19-disaster-recovery-readiness)
    - [19.1 What are RTO and RPO?](#191-what-are-rto-and-rpo)
    - [19.2 RTO and RPO Targets](#192-rto-and-rpo-targets)
    - [19.3 Failure Mode Planning](#193-failure-mode-planning)
    - [19.4 Graceful Degradation](#194-graceful-degradation)
    - [19.5 Circuit Breaker Pattern](#195-circuit-breaker-pattern)
    - [19.6 Retry with Exponential Backoff](#196-retry-with-exponential-backoff)
    - [19.7 Runbooks](#197-runbooks)
  - [20. Server Code Hygiene](#20-server-code-hygiene)
  - [21. Common Pitfalls to Avoid](#21-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

This document applies to:

- The **legacy PHP API server** (monolith, PHP 8.x, no framework)  
- The **new Bingo Java API server** (SEAM microservice architecture, SEAM)  
- The **SmartFox live server** (Java, stateful monolith) used by both games

Both server systems support a live-service game with periodic content resets and monthly feature releases. The standards here are calibrated for high-availability, high-throughput requirements with a small-to-medium engineering team. Our primary player base is in the USA; our engineering team is in India. This means server deployments and content resets typically happen during Indian business hours that align with US off-peak hours (early morning US Eastern time).

---

## 2. Server Architecture Principles

### 2.1 The Server Is the Authority

The server is the single source of truth for all game state, player data, and monetization outcomes. No client action changes state without server validation and persistence.

### 2.2 Legacy PHP Monolith: Living With It

New features added to the monolith must follow a modular structure: each feature lives in its own namespace/directory with its own service, validator, and repository classes. Do not add to existing oversized files. Dependencies between modules must flow in one direction only — circular dependencies are prohibited.

### 2.3 New Java API: Microservice Design Principles

Each microservice owns exactly one bounded domain (e.g., `player-profile`, `reward-engine`, `event-calendar`, `content-delivery`). A microservice must own its own database schema. Inter-service communication must go through defined API contracts (REST or async message bus). Direct database coupling between services is prohibited. 

**What is Direct Database Coupling Between Services?**
Direct database coupling occurs when one service executes queries directly against the database owned by another service — bypassing the owning service's API. For example, if the PHP monolith runs a `SELECT` against the `reward_claims` table owned by the Java reward-service, that is direct database coupling.

**Why it is prohibited:**

- It creates an invisible, undocumented dependency. Any schema change in the reward-service DB silently breaks the PHP query.  
- It bypasses the owning service's business logic, caching, and validation.  
- It makes independent deployment and schema evolution impossible.

```
WRONG — direct DB coupling:
  PHP API ──direct SQL──→ reward_service_db.reward_claims

CORRECT — service API:
  PHP API ──HTTP GET──→ reward-service /api/v1/claims/{playerId}
                             │
                             v
                       reward-service ──SQL──→ reward_claims DB
```

The owning service's published API is the only permitted access path to its data.

The new Java API uses a **SEAM** that is architecturally similar to SpringBoot (dependency injection, layered controllers/services/repositories, configuration injection) but is not SpringBoot. Standards for this framework are defined in [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server). Where [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server) references Spring Boot-style annotations or conventions, apply the equivalent concept in SEAM.

### 2.4 Both API Servers Must Be Stateless

Both the PHP monolith and the Java API must be stateless. Session state lives in Redis or is encoded in the request token. This is mandatory for horizontal scaling under load (see [§3. Stateful vs. Stateless Servers](#3-stateful-vs-stateless-servers).

---

## 3. Stateful vs. Stateless Servers

The decision of whether a server is stateful or stateless is among the most consequential architectural choices you make. It determines how the server scales, how it fails, how it is deployed, and what happens to active player sessions during an incident. Every engineer must understand the distinction.

### 3.1 Definitions

**Stateless Server:** A server that stores no per-player or per-session data in its own memory between requests. Each request carries everything the server needs to fulfill it (typically via an auth token that identifies the player and session). Any instance of the server can handle any request.

**Stateful Server:** A server that maintains active state in memory between client interactions. A specific client must connect to a specific server instance because that instance holds the state for the ongoing session.

### 3.2 Side-by-Side Comparison

```
STATELESS (PHP API / Java microservices)   STATEFUL (SmartFox live server)
────────────────────────────────────────   ────────────────────────────────────────
REQUEST HANDLING:                          REQUEST HANDLING:
  Any instance handles any request           Client must stay connected to same instance
  No memory of previous requests             Server remembers prior messages/events

SCALING:                                   SCALING:
  Horizontal — add/remove instances freely   Vertical preferred; horizontal is complex
  Auto Scaling Group works perfectly         ASG scale-in will evict active players

FAILURE:                                   FAILURE:
  Instance failure → other instances serve  Instance failure → players lose game session
  No game state is lost                      In-memory room state is lost unless persisted

DEPLOYMENT:                                DEPLOYMENT:
  Rolling or blue/green — zero downtime      Requires room draining before restart
  Old instances serve while new spin up      Cannot simply terminate — players are live

STATE STORAGE:                             STATE STORAGE:
  State is in Redis, RDS/MySQL-backed state  Active state is in JVM heap (fast)
  Reading state requires a round-trip        Sub-millisecond access to game state

EXAMPLES IN OUR ARCHITECTURE:             EXAMPLES IN OUR ARCHITECTURE:
  PHP API reward endpoint                    SmartFox BingoRoomExtension
  Java player-profile microservice           Live number-calling loop
  Java reward-engine microservice            Per-player daub tracking per room
```

### 3.3 How They Work Together in Our Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│   Unity Client                                                        │
│       │                                                               │
│       ├──→ ALB ──→ PHP API / Java API  [STATELESS]                    │
│       │               │                                               │
│       │               ├──→ Redis (session, cache)                     │
│       │               ├──→ MySQL (legacy monolith data)               │
│       │               └──→ MySQL (service-owned schemas for new game) │
│       │                                                               │
│       └──→ NLB ──→ SmartFox Server  [STATEFUL]                        │
│                       │                                               │
│                       ├── In-memory: active rooms, live game state    │
│                       └── Persists to DB at checkpoints               │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**Critical rule:** SmartFox handles real-time coordination; the PHP/Java API servers own all persistent state, economic outcomes, and win validation. SmartFox never awards currency or records wins independently.

### 3.4 Operational Implications

| Concern | Stateless (PHP/Java API) | Stateful (SmartFox) |
|:--------|:-------------------------|:--------------------|
| **Deploying a new version** | Rolling deploy; no player impact | Must drain rooms first; schedule maintenance window |
| **Auto-scaling** | Standard ASG — fully automatic | Manual capacity planning; cannot auto-scale in |
| **Server crash** | Other instances absorb traffic instantly | Active room state lost unless persisted to DB |
| **Recovery from crash** | Automatic (ASG replaces instance) | Rooms must be recovered from DB; clients must reconnect | 
| **Session affinity** | Not needed | Required — player must stay on same SmartFox instance |

---

## 4. API Design Standards

### 4.1 Purpose

A good API is a contract. It defines how systems communicate, what they can expect, and what guarantees are made. The goal of this standard is not to enforce aesthetics — it is to enforce **predictability, safety, and longevity.**

A well-designed API achieves the following:

| Goal | Why It Matters |
|:-----|:---------------|
| **Consistency** |  Consumers learn one pattern; it applies everywhere |
| **Clarity** | No guessing what an endpoint does or what it returns |
| **Safety** | Invalid input is rejected early; sensitive data is never leaked | 
| **Resilience** | Failure is handled gracefully, not silently | 
| **Evolvability** | APIs change; consumers must not break unexpectedly |

Every decision in this standard exists to serve one or more of these goals.

### 4.2 URL Design

URLs identify **resources**, not actions. Actions are expressed through HTTP methods.

```
✅  GET    /players/{id}/cards          → Fetch cards for a player
✅  POST   /games/{id}/draws            → Trigger a draw in a game
✅  PATCH  /players/{id}                → Partially update a player

❌  GET    /getPlayerCards?playerId=42
❌  POST   /triggerDraw
❌  POST   /updatePlayerProfile
```

**Rules:**

- Use **nouns**, never verbs in the path.
- Use **plural** resource names: `/players`, `/games`, `/cards`.
- Use **kebab-case** for multi-word segments: `/bonus-rounds`.
- Use **versions**, assume v1 by default.
- Nest only one level deep. `/games/{id}/draws` is fine. `/games/{id}/rounds/{id}/draws/{id}/results` is not.

**URL Structure**

```
URL structure: /api/v{version}/{resource}/{id}/{sub-resource}

GET    /api/v1/players/{playerId}/inventory
POST   /api/v1/players/{playerId}/rewards/claim
DELETE /api/v1/players/{playerId}/sessions/{sessionId}
GET    /api/v1/rooms?status=active&gameType=classic
```

### 4.3 HTTP Methods

| Method | Use | Body? | Idempotent? |
|:-------|:----|:------|:------------|
| `GET` | Read a resource | No | Yes |
| `POST` | Create a resource | Yes | No | 
| `PUT` | Full replace | Yes | Yes | 
| `PATCH` | Partial update | Yes | No |
| `DELETE` | Remove a resource | No | Yes |

> **Rule:** Never use `GET` for operations with side effects. Never use `POST` when `PUT` or `PATCH` is correct.

### 4.4 Request & Response Structure

**Always use a consistent response envelope**

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "requestId": "uuid-here",
    "timestamp": "2025-03-01T12:00:00Z",
    "apiVersion": "1"
  },
  "error": {}
}
```

A consumer should **never** have to guess the shape of a response. The envelope is identical on success and failure — only `success`, `data`, and `errors` change.

**Errors must be structured and actionable**

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "CARD_NOT_FOUND",
    "field": "cardId",
    "message": "No card found with ID 9921 for this player."
  },
  "meta": {
    "requestId": "uuid-here",
    "timestamp": "2025-03-01T12:00:00Z",
    "apiVersion": "1"
  }
}
```

❌ `"error": "Something went wrong"` — useless to a consumer.

✅ `"code": "CARD_NOT_FOUND"` — machine-readable, loggable, debuggable.

#### 4.4.1 Client and Server API Contract Finalization

Every client-facing or inter-server API change must have a finalized contract before client and server implementation proceeds. The contract is the shared agreement between the API owner and every consumer. It must be reviewed by the affected client and server owners before the endpoint is built, changed, or removed.

The finalized contract must define:

- endpoint path, HTTP method, version, authentication requirements, authorization rules, and consumer list
- request fields and response fields, including type, valid range or allowed values, required/optional status, defaults, validation rules, and ownership
- every status code and machine-readable error code the client or caller may branch on
- idempotency, retry, timeout, pagination, sorting, filtering, and partial-success behavior where applicable
- compatibility plan for live clients, including optional fields, safe defaults, enum stability, feature flags, deprecation window, and version migration
- observability requirements, including request identifiers, metrics, audit logs, and any fields that must not be logged
- sensitive data and PII exposure rules, including which fields are server-only, redacted, or never returned

Long-term API design must assume the endpoint will outlive the current feature sprint. Do not reuse fields for new meanings, change enum semantics in place, or expose internal database shape as the public contract. Prefer additive changes, stable machine-readable codes, explicit capability checks, and versioned breaking changes.

API documentation is required for every new endpoint and every contract-changing endpoint update. See the [ESTD15 Technical Approach Document template](./ESTD15_-_Technical_Document_Guide_and_Template.md#81-technical-approach-document-tad) for the required request/response tables and sample calls.

### 4.5 HTTP Status Codes

Use status codes correctly. They are part of the contract.

| Code | Meaning | When to Use |
|:-----|:--------|:------------|
| `200` | OK | Successful GET, PATCH, PUT |
| `201` | Created | Successful POST that creates a resource | 
| `204` | No Content | Successful DELETE | 
| `400` | Bad Request | Malformed input, validation failure | 
| `401` | Unauthorized | Missing or invalid auth token | 
| `403` | Forbidden | Authenticated but not permitted | 
| `404` | Not Found | Resource does not exist | 
| `409` | Conflict | Duplicate create, state conflict | 
| `422` | Unprocessable | Input is valid format but fails business rules | 
| `429` | Too Many Requests | Rate limit exceeded | 
| `500` | Server Error | Unhandled internal failure |
| `503` | Service Unavailable | Maintenance mode or dependency outage |

> **Rule:** Never return `200` with `"success": false`. The HTTP status code and the response body must agree.

### 4.6 Versioning

APIs change. Consumers must not break. All APIs must be versioned from day one. A new version is required when a breaking change is made. Old versions must be supported for a minimum of three months (two client release cycles) after the new version is available. Communicate deprecation to the client team with at least four weeks' notice.

Breaking changes (require new version): removing a response field, changing a field type, removing an endpoint, changing required vs. optional parameters, changing error codes clients branch on.

Non-breaking (no new version needed): adding a new optional response field, adding a new optional request parameter, adding a new endpoint.

```
✅  /v1/players/{id}
✅  /v2/players/{id}    ← breaking change? new version.
```
- Version at the **URL level** for major, breaking changes.
- Additive changes (new optional fields, new endpoints) do not require a version bump.
- A version must be **supported for a defined sunset period** before removal. Announce deprecation via a `Deprecation` response header.

### 4.7 Pagination

Never return unbounded lists.

```
GET /players/{id}/cards?page=2&pageSize=25
```

```json
{
  "data": [ ... ],
  "meta": {
    "page": 2,
    "pageSize": 25,
    "totalPages": 8,
    "totalItems": 190
  }
}
```

### 4.8 Idempotency for Unsafe Operations

For POST operations that must not execute twice (e.g., purchase, reward grant), require an **idempotency key** from the caller.

```
POST /players/{id}/purchases
Idempotency-Key: client-generated-uuid
```

The server records this key. A duplicate request returns the **original response**, not a second execution. This is the correct defense against retries and network failures.

### 4.9 The Non-Negotiables

1. **All endpoints require authentication** unless explicitly allowlisted.
2. **Input is validated server-side**, always — client-side validation is UX, not security.
3. **Internal errors are never exposed** in the response body. Log them; do not return stack traces in production.
4. **All timestamps are UTC ISO 8601**: `2025-03-01T12:00:00Z`.
5. **IDs in URLs are opaque strings**, not sequential integers. Sequential IDs leak scale and invite enumeration attacks.

### 4.10 Client-Version Compatibility and Deprecation Windows

Because iOS and Android rollouts are not instantaneous — and Facebook/Web builds can lag in player adoption — the server must assume a mixed-client population during every release window. Additive change is the default strategy. Do not repurpose an existing field or enum meaning while older clients may still be live.

Rules:

- Support at least the current live client and the immediately previous live client version unless an approved emergency security cutoff exists.
- New response fields must be optional and safely ignorable by older clients.
- New request fields from newer clients must have safe server defaults when absent.
- Behavior changes should be gated by explicit client capability or server-side feature flags, not scattered string comparisons on app version.
- Breaking removals require a deprecation plan, release-note communication, and a sunset date consistent with [§4.6 Versioning](#46-versioning).

---

## 5. Authentication and Authorization

### 5.1 Token-Based Authentication

Use JWT with short expiry (1 hour access token, 30-day refresh token) or opaque tokens stored server-side (opaque preferred for revocability). All non-public API endpoints require a valid session token validated on every request. Token signing: HS256 minimum; RS256 preferred.

### 5.2 Session Storage

Store session state server-side in Redis with TTL matching the token TTL. Delete the session from Redis immediately on logout or token revocation. Maintain a session list per player, capped at a reasonable maximum (e.g., 10 concurrent sessions — players switch devices).

### 5.3 Authorization

Authorization checks must occur in the service layer, not in the controller alone. For player-facing endpoints, always verify that the resource being accessed belongs to the authenticated player:

```php
// BAD — uses URL parameter without verifying ownership
public function inventoryGet(int $playerId): Response {
    return $this->inventoryService->get($playerId);
}

// GOOD — verifies the requesting player is the owner
public function inventoryGet(int $playerId): Response {
    if ($this->session->getPlayerId() !== $playerId) {
        throw new ForbiddenException("Access denied to player {$playerId}'s inventory");
    }
    return $this->inventoryService->get($playerId);
}
```

---

## 6. Input Validation at the Server Boundary

All [ESTD1 §11. Input Validation and Sanitization](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#11-input-validation-and-sanitization) validation rules apply. Additionally: validate before any database interaction; validate every field of every inbound request payload; validation failures return 400 with a structured error; do not leak internal field names in error messages.

**Request size limits:**

- Standard API request: 64 KB maximum  
- File upload endpoint: explicitly configured per use case, never unlimited

---

## 7. Rate Limiting and Abuse Prevention

Rate limiting is the practice of capping how many times a client — identified by IP address, session token, user ID, or device fingerprint — can invoke a server operation within a defined time window. Requests that breach the limit are rejected before they reach business logic.

### 7.1 Why It Matters

Without rate limiting, a single misbehaving client — whether a bot, a malfunctioning game client, or an attacker — can degrade service for every other player. Rate limiting protects server capacity, guards game economy integrity, and is the first line of defence against credential stuffing, brute-force attacks, and scraping.

**Where It Applies to Us**

| Scenario | Risk Without Limiting |
|:---------|:----------------------|
| `/player/login` and `/player/register` on the PHP API | Brute-force credential attacks |
| Reward claim and in-app purchase endpoints | Economy abuse; duplicate reward exploitation | 
| Bingo room join and SmartFox connection handshake | Resource exhaustion on peak hours |
| Internal Next.js tool APIs | Accidental loop scripts hammering config endpoints |
| SEAM microservice endpoints | Amplified blast radius due to shared infrastructure |

### 7.2 Core Techniques

- **Fixed Window** — Count requests per user within a fixed clock interval (e.g. 100 requests per minute). Simple to implement but vulnerable to burst traffic at window boundaries.
- **Sliding Window** — Track request timestamps over a rolling interval. Smoother enforcement; eliminates boundary bursts. Higher memory cost.
- **Token Bucket** — Each client holds a bucket of tokens replenished at a fixed rate. A request consumes one token. Allows controlled bursting without abandoning the limit entirely. Well-suited for endpoints that have legitimate but bursty access patterns.
- **Leaky Bucket** — Requests enter a queue and are processed at a fixed rate. Provides uniform throughput but adds latency under burst load.

### 7.3 Things to Keep in Mind

**Identify by the right key.** IP-based limiting is weak behind shared NAT or mobile carriers. Prefer authenticated user ID where available; fall back to IP for unauthenticated endpoints.

**Handling bad UX is non-negotiable.** A rejected request must return `HTTP 429 Too Many Requests` with a `Retry-After` header. The Unity client must read this header and surface a human-readable message — never a raw error code. Silent failures and misleading error messages destroy player trust.

**Set limits per endpoint, not globally.** A blanket server-wide limit is too coarse. A login endpoint and a leaderboard poll have different risk profiles and different legitimate usage patterns.

**Test your limits under realistic load.** Limits set too conservatively will punish legitimate players during content release windows — exactly the moments with the highest concurrent traffic on our platform.

### 7.4 Example: Token Bucket — PHP Implementation

The implementation below uses Redis as the token store. Each client gets its own bucket represented by two keys: the current token count and the timestamp of the last refill. No Lua scripting is used; the logic runs entirely in PHP.

```php
<?php

class TokenBucketRateLimiter
{
    private Redis  $redis;
    private int    $capacity;    // Maximum tokens the bucket can hold
    private float  $refillRate;  // Tokens added per second
    private int    $ttl;         // Redis key expiry in seconds

    public function __construct(Redis $redis, int $capacity, float $refillRate)
    {
        $this->redis      = $redis;
        $this->capacity   = $capacity;
        $this->refillRate = $refillRate;
        $this->ttl        = (int) ceil($capacity / $refillRate) * 2;
    }

    public function isAllowed(string $clientKey): bool
    {
        $tokenKey     = "ratelimit:tokens:{$clientKey}";
        $lastRefillKey = "ratelimit:ts:{$clientKey}";

        $now          = microtime(true);
        $tokens       = (float) ($this->redis->get($tokenKey)      ?? $this->capacity);
        $lastRefill   = (float) ($this->redis->get($lastRefillKey) ?? $now);

        // Calculate how many tokens have been earned since the last request
        $elapsed      = max(0, $now - $lastRefill);
        $earned       = $elapsed * $this->refillRate;
        $tokens       = min($this->capacity, $tokens + $earned);

        if ($tokens < 1) {
            return false; // Bucket is empty — request denied
        }

        // Consume one token and persist the updated state
        $tokens -= 1;
        $this->redis->setex($tokenKey,      $this->ttl, $tokens);
        $this->redis->setex($lastRefillKey, $this->ttl, $now);

        return true;
    }
}
```

```php
// --- Usage at an API endpoint boundary ---

$redis   = new Redis();
$redis->connect('127.0.0.1', 6379);

// Allow 10 requests maximum, refilling at 2 tokens per second
$limiter = new TokenBucketRateLimiter($redis, capacity: 10, refillRate: 2.0);

$clientKey = 'user:' . $authenticatedUserId; // Prefer user ID over IP for auth'd endpoints

if (!$limiter->isAllowed($clientKey)) {
    http_response_code(429);
    header('Retry-After: 1');
    echo json_encode(['error' => 'ERR_RATE_LIMITED', 'message' => 'Too many requests. Please wait a moment.']);
    exit;
}

// Proceed with normal request handling
```

***What Is Happening***

**Bucket initialisation.** On the first request from a client, both Redis keys are absent. The code treats a missing token count as a full bucket (`$capacity`) and a missing timestamp as the current time. The client starts with full allowance — a deliberate choice to avoid penalising new or returning players.

**Refill calculation.** On every subsequent request, the elapsed time since the last request is multiplied by the refill rate to calculate how many tokens the client has earned back. The result is capped at `$capacity` — tokens do not accumulate beyond the bucket's maximum. This is the mechanism that allows short legitimate bursts while still enforcing a long-run average.

**Token consumption.** If at least one token is available, it is decremented and the updated state is written back to Redis with `SETEX`. The TTL ensures idle clients do not leave stale keys in Redis indefinitely.

**Denial.** If the bucket is empty (`$tokens < 1`), the request is rejected immediately. No state is written on denial — there is nothing to update.

**The** `Retry-After` header. When returning `429`, the response includes `Retry-After: 1`. For a refill rate of 2 tokens per second, the client is guaranteed at least one token within 0.5 seconds. Setting the header to `1` second is a safe, round-number approximation. The Unity client should read this header and delay its retry rather than hammering the endpoint in a tight loop.

Rate limits must be applied at the AWS ALB/WAF level (first line) and in the service layer (second line). Rate limits must be per player. Exceeding a rate limit returns `429` with a Retry-After header. Log all rate-limit events at WARN level with playerId and endpoint.

> ⚠️ **Race condition caveat**. This implementation performs a read-then-write across two Redis keys without atomicity. Under very high concurrency, two requests from the same client can read the same token count simultaneously and both be allowed through — a brief over-admission. For most endpoints on our platform this is an acceptable trade-off. If strict enforcement is required (e.g., a reward claim endpoint), the correct mitigation is a Redis distributed lock (`SET NX`) around the read-modify-write cycle, or migrating the logic to a Lua script.

### 7.5 Rate Limits

| Operation | Rate Limit |
|:----------|:-----------|
| Room join | 10 per minute per player | 
| Reward claim | 5 per hour per player |
| Purchase | 20 per hour per player | 
| Login attempts | 10 per 15 minutes (lock account after threshold) |

---

## 8. Idempotency

Network requests can fail after the server has processed them but before the response reaches the client. Without idempotency, the client retrying the request results in double-awarding currency, double-purchasing items, or duplicate records. Idempotency ensures that retrying a request has the same effect as making it once.

### 8.1 When Idempotency Is Required

Any operation that changes state and can be safely retried must be idempotent. This is mandatory for: reward claims, currency purchases, ticket purchases, and any financial transaction.

### 8.2 Approach 1: Idempotency Keys (POST endpoints — general approach)

The client sends a unique `Idempotency-Key` header (a UUID generated by the client before sending the first attempt). The server checks this key, stores the response on first execution, and returns the stored response on all subsequent requests with the same key.

```
Client: POST /api/v1/rewards/claim
        Idempotency-Key: a4f9b21c-0000-4b92-9e1d-000000001234

Server logic:
  1. Lookup a4f9b21c... in Redis (TTL: 24 hours)
  2. IF found: return the stored response immediately (no DB write)
  3. IF not found: execute claim, persist result, store response in Redis, return response
```

**PHP implementation:**

```php
public function rewardClaim(Request $request): Response
{
    $key = $request->getHeader('Idempotency-Key')
        ?? throw new ValidationException('Idempotency-Key header required');

    $cached = $this->redis->get("idempotency:{$key}");
    if ($cached !== null) {
        return Response::fromCache($cached);  // Return stored response
    }

    $result = $this->rewardService->claim(
        $request->getPlayerId(),
        $request->getBody()['rewardId']
    );

    // Store result for 24h — covers all reasonable retry windows
    $this->redis->set("idempotency:{$key}", $result->toJson(), ttl: 86400);
    return Response::success($result);
}
```

### 8.3 Approach 2: Database-Level Unique Constraints (last-resort guardrail)

Even with idempotency keys, always add a database-level unique constraint as the final guardrail against duplicates. This catches cases where two concurrent requests arrive before either has stored an idempotency key. In the new architecture, enforce the equivalent constraint inside the service-owned MySQL schema that owns the write.

```sql
-- MySQL: unique constraint prevents duplicate claims
ALTER TABLE reward_claims
    ADD CONSTRAINT unq_reward_claims_player_reward_cycle
    UNIQUE (player_id, reward_id, content_cycle_id);
```

**PHP with INSERT IGNORE:**

```php
// This will silently succeed if the record already exists — always check affected rows
$affected = $this->db->execute(
    'INSERT IGNORE INTO reward_claims (player_id, reward_id, content_cycle_id)
     VALUES (:playerId, :rewardId, :cycleId)',
    [':playerId' => $playerId, ':rewardId' => $rewardId, ':cycleId' => $cycleId]
);
if ($affected === 0) {
    throw new RewardAlreadyClaimedException("Reward {$rewardId} already claimed this cycle");
}
```

### 8.4 Approach 3: Conditional Updates with Version Fields (optimistic locking in monolith)

For operations that modify a record and must only succeed once per state:

```sql
-- Only update if the state is as expected
UPDATE bingo_rooms
SET    state = 'GAME_STARTED', game_sequence_id = :newSeqId
WHERE  room_id = :roomId
  AND  state = 'WAITING'
  AND  game_sequence_id = :expectedSeqId;
-- If affected_rows = 0, the state was already changed → idempotent
```

### 8.5 Approach 4: SmartFox Idempotency via Sequence IDs

In SmartFox, client messages can be duplicated on reconnect. Guard using a `gameSequenceId` that the client sends with each message:

```java
// SmartFox extension handler
public void bingoClaimRequest(User user, ISFSObject params) {
    int gameSequenceId = params.getInt("gameSeqId");
    int roomId = user.getLastJoinedRoom().getId();

    // Check if this sequence ID was already processed in this game
    if (gameStateCache.isSequenceProcessed(roomId, user.getId(), gameSequenceId)) {
        Logger.info("Duplicate BINGO claim suppressed. User={}, SeqId={}", user.getId(), gameSequenceId);
        // Re-send the original response (the client may not have received it)
        cachedResponseSend(user, gameSequenceId);
        return;
    }

    // Process the claim...
    gameStateCache.markSequenceProcessed(roomId, user.getId(), gameSequenceId);
}
```

### 8.6 Approach 5: Microservice Idempotency via Distributed Idempotency Store

In the new Java microservice architecture, where a reward-engine service may be called from multiple entry points:

```java
@Service
public class RewardClaimService {

    public RewardClaimResult claim(String idempotencyKey, int playerId, String rewardId) {
        // Attempt to acquire idempotency lock in Redis
        Boolean acquired = redisTemplate.opsForValue()
            .setIfAbsent("idempotency:" + idempotencyKey, "PENDING", Duration.ofHours(24));

        if (Boolean.FALSE.equals(acquired)) {
            // Key exists — check if completed or still pending
            String storedResult = redisTemplate.opsForValue().get("idempotency:" + idempotencyKey);
            if ("PENDING".equals(storedResult)) {
                throw new ConcurrentRequestException("Request is already being processed");
            }
            return RewardClaimResult.fromJson(storedResult);  // Return stored result
        }

        try {
            RewardClaimResult result = claimExecute(playerId, rewardId);
            // Store the result, replacing PENDING
            redisTemplate.opsForValue().set("idempotency:" + idempotencyKey,
                result.toJson(), Duration.ofHours(24));
            return result;
        } catch (Exception e) {
            redisTemplate.delete("idempotency:" + idempotencyKey);  // Release lock on failure
            throw e;
        }
    }
}
```

### 8.7 Handling Malicious Clients: Rotating Idempotency Keys

A sophisticated client might attempt to bypass idempotency protection by generating a new UUID for every retry. Each request appears "new" to the server and the operation executes multiple times.

**Why idempotency keys alone are not the last line of defense:**

The idempotency key layer is designed to handle honest network retries from legitimate clients. It was never designed to be the sole guard against malicious abuse. That is why we layer defenses.

**The three-layer defense (idempotency keys are not the only guard):**

```
Layer 1 — Rate Limiting:
  WAF + service layer: max 5 reward claims per hour per player.
  Rotating keys still hit the rate limit.

Layer 2 — Business State Guard (primary protection):
  Check whether the player has already claimed this reward in the current
  cycle BEFORE checking the idempotency key. This is a DB read, independent
  of any key the client sends.

  SELECT 1 FROM reward_claims
  WHERE player_id = ? AND reward_id = ? AND cycle_id = ?

  If found → return ALREADY_CLAIMED regardless of idempotency key.

Layer 3 — Database Unique Constraint (final guardrail):
  UNIQUE (player_id, reward_id, content_cycle_id)
  Catches any race condition that slips through Layers 1 and 2.
```

**Implementation example (PHP — three-layer defense combined):**

```php
public function rewardClaim(Request $request): Response
{
    // Layer 1: Rate limit checked at WAF + middleware before this method runs
    // (returns 429 if exceeded — handled upstream)

    $playerId   = $request->getAuthenticatedPlayerId();  // from session, not body
    $rewardId   = $request->getValidatedBody()['rewardId'];
    $cycleId    = $this->contentCycleService->getCurrentCycleId();

    // Layer 2: State guard — independent of idempotency key
    try {
        $alreadyClaimed = $this->rewardRepository->hasClaimed($playerId, $rewardId, $cycleId);
    } catch (DatabaseException $e) {
        $this->logger->error('Failed to check claim status', ['playerId' => $playerId, 'error' => $e->getMessage()]);
        return Response::internalError('CLAIM_CHECK_FAILED');
    }

    if ($alreadyClaimed) {
        return Response::conflict('REWARD_ALREADY_CLAIMED');
    }

    // Idempotency key (for honest retry deduplication — not the primary guard)
    $key = $request->getHeader('Idempotency-Key');
    if ($key !== null) {
        $cached = $this->redis->get("idempotency:{$key}");
        if ($cached !== null) {
            return Response::fromCache($cached);
        }
    }

    try {
        // Layer 3: DB unique constraint enforced inside claimRecord
        $result = $this->rewardService->claim($playerId, $rewardId, $cycleId);
    } catch (DuplicateRecordException $e) {
        // Unique constraint caught a race condition — treat as already claimed
        return Response::conflict('REWARD_ALREADY_CLAIMED');
    } catch (DatabaseException $e) {
        $this->logger->error('Reward claim DB write failed', ['playerId' => $playerId, 'error' => $e->getMessage()]);
        return Response::internalError('CLAIM_WRITE_FAILED');
    }

    if ($key !== null) {
        $this->redis->set("idempotency:{$key}", $result->toJson(), ttl: 86400);
    }

    return Response::success($result);
}
```

**Key insight:** The business-logic state guard (Layer 2) makes the operation inherently idempotent regardless of what idempotency key the client sends. The idempotency key layer optimizes performance (avoids re-executing on honest retries) but is not the security mechanism. Rate limiting (Layer 1) and the state guard (Layer 2) together neutralize the malicious key-rotation attack.

---

## 9. Boundary Functions — Server-Side Structure

All server boundary function standards are defined in [ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions). This section reinforces key server-specific requirements and provides a SEAM-specific example.

**Definition**: A *boundary function* is the entry-point method at the edge of a server domain that receives raw external input (HTTP request, SmartFox message, SQS message, scheduled job trigger) and is the first and only point where that input is parsed, validated, authorized, and sanitized before being handed to the service layer.

### 9.1 Boundary Functions in the SEAM Framework

SEAM controller methods are boundary functions. They must follow the ordered responsibilities defined in [ESTD1 §10.2 Responsibilities of a Boundary Function](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#102-responsibilities-of-a-boundary-function). SEAM provides annotations that map directly to this structure:

```java
// SEAM controller — this entire method is a boundary function
@RouteHandler(method = HttpMethod.POST, path = "/api/v1/players/{playerId}/rewards/claim")
@RequiresAuth
@RateLimit(key = "reward.claim", maxPerHour = 5)
public ApiResponse rewardClaim(SeamRequest request, @PathParam("playerId") int playerId) {
    // Step 1: Parse (SEAM auto-parses the body; validate type safety here)
    ClaimRewardRequest body = request.parseBody(ClaimRewardRequest.class);

    // Step 2: Validate
    ValidationResult validation = body.validate();
    if (!validation.isValid()) return ApiResponse.badRequest(validation.errors());

    // Step 3: Authorize (SEAM @RequiresAuth verifies session; check ownership here)
    if (!request.session().getPlayerId().equals(playerId))
        return ApiResponse.forbidden("ACCESS_DENIED");

    // Step 4: Log + STEP 5: Delegate
    logger.info("Reward claim", Map.of("playerId", playerId, "rewardId", body.getRewardId(),
        "correlationId", request.correlationId()));
    try {
        RewardClaimResult result = rewardService.claim(playerId, body.getRewardId());
        logger.info("Reward claimed", Map.of("playerId", playerId, "coins", result.getCoinsAwarded()));
        return ApiResponse.ok(ClaimRewardResponse.from(result));
    } catch (RewardAlreadyClaimedException e) {
        return ApiResponse.conflict("REWARD_ALREADY_CLAIMED");
    } catch (Exception e) {
        logger.error("Reward claim failed", e, Map.of("playerId", playerId));
        return ApiResponse.internalError("INTERNAL_ERROR");
    }
}
```

---

## 10. Anatomy of a Good Request Handler

The request handler is the entry-point boundary ([ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions)) for every player action. A correctly structured handler guarantees security, data integrity, auditability, and consistent error responses.

### 10.1 The Nine-Step Structure

```
1.  AUTHENTICATE    Verify caller identity (session token, not request body)
2.  AUTHORIZE       Verify resource ownership matches authenticated player
3.  VALIDATE        Type, range, business rule checks on all inputs
4.  SANITIZE        Strip injection characters; enforce length limits
5.  RATE-LIMIT      Reject excessive frequency (WAF first; service layer second)
6.  IDEMPOTENCY     Short-circuit duplicate writes (state guard + key cache)
7.  DELEGATE        Hand off to service layer — no business logic in handler
8.  AUDIT-LOG       Record actor, action, before/after state, reason, timestamp
9.  CATCH-ALL       Entry-point boundary: catch all unhandled exceptions,
                    log with full context, return structured error response
```

### 10.2 Annotated Example (PHP)

```php
/**
 * POST /api/v1/players/{playerId}/rewards/claim
 * Claims the periodic bonus for the authenticated player.
 */
public function weeklyBonusClaim(Request $request): Response
{
    // 1. AUTHENTICATE — identity from session token only
    $authenticatedPlayerId = $request->getAuthenticatedPlayerId();

    // 2. AUTHORIZE — verify URL player matches session player
    $requestedPlayerId = (int)$request->getRouteParam('playerId');
    if ($authenticatedPlayerId !== $requestedPlayerId) {
        $this->auditLogger->warn('Auth mismatch', ['auth' => $authenticatedPlayerId, 'req' => $requestedPlayerId]);
        throw new ForbiddenException('Cannot claim reward for another player.');
    }

    // 3+4. VALIDATE & SANITIZE
    try {
        $input = $this->rewardClaimValidator->validate($request->getParsedBody());
    } catch (ValidationException $e) {
        $this->logger->warn('Invalid input', ['errors' => $e->getErrors()]);
        throw $e;
    }

    // 5. RATE-LIMIT (primary at WAF; secondary here)
    try {
        $this->rateLimiter->assertNotExceeded('reward_claim', $authenticatedPlayerId);
    } catch (RateLimitExceededException $e) {
        return Response::tooManyRequests('RATE_LIMIT_EXCEEDED', $e->getRetryAfterSec());
    }

    // 6. IDEMPOTENCY — state guard is primary; key is optimization for honest retries
    $cycleId = $this->contentCycleService->getCurrentCycleId();
    try {
        if ($this->rewardRepository->hasClaimed($authenticatedPlayerId, $input->rewardId, $cycleId)) {
            return Response::conflict('REWARD_ALREADY_CLAIMED');
        }
    } catch (DatabaseException $e) {
        $this->logger->error('Claim check failed', ['error' => $e->getMessage()]);
        return Response::internalError('CLAIM_CHECK_FAILED');
    }

    // 7. DELEGATE — all business logic in service layer
    try {
        $result = $this->rewardService->claim($authenticatedPlayerId, $input->rewardId, $cycleId);
    } catch (RewardAlreadyClaimedException $e) { return Response::conflict('REWARD_ALREADY_CLAIMED'); }
    catch (PlayerNotFoundException $e)        { return Response::notFound('PLAYER_NOT_FOUND'); }
    catch (DatabaseException $e) {
        $this->logger->error('Claim write failed', ['error' => $e->getMessage()]);
        return Response::internalError('CLAIM_WRITE_FAILED');
    }

    // 8. AUDIT-LOG
    $this->auditLogger->info('Bonus claimed', [
        'playerId' => $authenticatedPlayerId,
        'rewardId' => $input->rewardId,
        'coins'    => $result->coinsAwarded,
        'balance'  => $result->newBalance,
        'reqId'    => $request->getCorrelationId(),
    ]);

    return Response::success(['coinsAwarded' => $result->coinsAwarded, 'newBalance' => $result->newBalance]);
}
```

### 10.3 Handler Rules

- **Handlers must be thin**. Business logic belongs in the service layer. A handler should have no conditional branches driven by business rules.  
- **All exception catching at the handler level must be typed**. Avoid base `Exception` catches at this level; each exception type maps to a specific HTTP status code.  
- **Every economic action must be audit-logged**. The audit log is append-only and contains who did what, when, and with what result.  
- **Never derive player identity from the request body or URL alone**. Always use `getAuthenticatedPlayerId()` from the validated session token.  
- **Return consistent error envelopes**. See [§4.4 Request & Response Structure](#44-request--response-structure) for the standard response structure. Client code switches on `error.code`, not `error.message`.  
- **Document every handler with its full contract** (purpose, auth requirements, every error code it can return).  
- See [ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions) for the cross-cutting boundary function standard.

---

## 11. Object-Relational Mapping (ORM)

Direct SQL queries scattered throughout service and controller code create tight coupling between business logic and the database schema. An ORM provides an abstraction layer that maps database tables to domain objects, enables query composition in the domain language rather than SQL strings, and reduces the risk of SQL injection (all queries are parameterized by the ORM). However, ORM usage has well-known pitfalls that, if not addressed, lead to poor performance and difficult-to-diagnose bugs.

### 11.1 ORM Policy by Server

| Server | ORM | Rationale |
|:-------|:----|:----------|
| Legacy PHP API | Custom Repository pattern (PHP Data Objects under the hood) | Legacy codebase; full ORM migration is out of scope. Repository pattern provides equivalent encapsulation. |
| New Java API | Custom ORM layer provided by the microservice framework (similar to Spring Data JPA conventions) | Framework-native; follow the conventions defined in [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server). |
| SmartFox | Custom lightweight DAO/Repository | SmartFox is not a typical web service; use lightweight direct-query repositories. |

For the new Java API, all database access must go through the framework's ORM repositories. Direct JDBC calls are only acceptable for:

- Complex queries that the ORM cannot generate efficiently (document clearly with a comment).  
- Batch operations where the ORM would generate N individual queries.

### 11.2 Repository Pattern (All Servers)

Regardless of ORM, all database access must be encapsulated in repository classes. Service classes must not construct or execute queries directly.

```java
// New Java API — custom ORM repository interface
public interface PlayerRepository {
    Optional<Player> findById(long playerId);
    Player save(Player player);
    Optional<Player> findByEmail(String email);
    List<Player> findByLastLoginBefore(Instant cutoff, int limit);
}

// Service uses only the repository interface — no SQL knowledge
public class PlayerService {
    private final PlayerRepository playerRepository;

    public PlayerProfile profileGet(long playerId) {
        return playerRepository.findById(playerId)
            .map(PlayerProfile::fromEntity)
            .orElseThrow(() -> new PlayerNotFoundException(playerId));
    }
}
```

### 11.3 The N+1 Query Problem

**This is the most common ORM performance anti-pattern.** It occurs when loading a collection and then fetching associated data for each item with a separate query.

```java
// DANGEROUS — N+1 queries: 1 query for rooms, then 1 per room for players
List<Room> rooms = roomRepository.findAll();        // 1 query
for (Room room : rooms) {
    List<Player> players = room.getPlayers();        // N queries — one per room!
}

// CORRECT — one query with JOIN (or batch fetch)
List<Room> rooms = roomRepository.findAllWithPlayers();  // 1 query with JOIN
// OR
List<Room> rooms = roomRepository.findAll();
List<Integer> roomIds = rooms.stream().map(Room::getId).collect(toList());
Map<Integer, List<Player>> playersByRoom = playerRepository.findByRoomIdIn(roomIds);  // 1 query
```

Always use `EXPLAIN` / `EXPLAIN ANALYZE` to verify the number of queries generated for any new ORM usage that fetches associated data.

### 11.4 ORM Transactions

Wrap all multi-step operations that must be atomic in a transaction:

```java
// New Java API — framework transaction annotation (similar to @Transactional)
@Transactional
public RewardClaimResult rewardClaim(long playerId, String rewardId) {
    Player player = playerRepository.findById(playerId)
        .orElseThrow(() -> new PlayerNotFoundException(playerId));

    if (rewardClaimRepository.existsByPlayerAndReward(playerId, rewardId, currentCycleId)) {
        throw new RewardAlreadyClaimedException(rewardId);
    }

    // Both operations are in the same transaction — if balanceUpdate fails, the claim is rolled back
    coinLedger.record(playerId, WEEKLY_BONUS_COINS, TransactionType.REWARD_CLAIM, rewardId);
    player.setCoinBalance(player.getCoinBalance() + WEEKLY_BONUS_COINS);
    playerRepository.save(player);
    rewardClaimRepository.save(new RewardClaim(playerId, rewardId, currentCycleId));

    return new RewardClaimResult(WEEKLY_BONUS_COINS, player.getCoinBalance());
}
```

---

## 12. Background Jobs and Async Processing

### 12.1 Job Queue Standards

Use a proper job queue (AWS SQS recommended) for all async/background work. Never process background work synchronously in the API request cycle if it can be deferred. Async work examples: push notification dispatch, email sending, leaderboard recalculation, analytics event forwarding.

### 12.2 Idempotent Jobs

All background jobs must be idempotent (safe to run more than once). Jobs must have a unique `job_id` used to detect duplicates. Record job execution status in the database or Redis.

### 12.3 Content Reset Jobs

The periodic content reset is a critical operation. It must:

- Run via a scheduled job (AWS EventBridge cron), not be triggered by a player request.  
- Be **idempotent** — running the reset twice for the same content cycle must be a no-op.  
- Complete within a defined time window (target: < 5 minutes).  
- Have a **dry-run mode** for testing without side effects.  
- Send alerts if it fails or takes longer than expected.  
- The reset period is configurable — do not hardcode 7 days anywhere.

### 12.4 Scheduled Jobs Catalog
Maintain a documented catalog of all scheduled jobs. Every job must document: name, schedule expression, owner, expected max duration, and what to do if it exceeds that duration.

---

## 13. Concurrency and Thread Safety

### 13.1 PHP Monolith

Race conditions across requests are real in a multi-instance PHP deployment. Use database-level locking (`SELECT ... FOR UPDATE`) or atomic operations for operations involving shared mutable data. Do not rely on application-level locks in a multi-instance deployment — they do not span instances.

### 13.2 Java Microservices

Do not share mutable state between request-handling threads unless it is explicitly thread-safe. Use `ConcurrentHashMap`, `AtomicLong`, and other `java.util.concurrent` types for shared mutable state. Avoid static mutable fields in service classes.

### 13.3 SmartFox Server

Use `synchronized` blocks or `ReentrantLock` for shared room state. Keep locks as short-lived as possible. Never hold a lock while performing I/O (DB query, HTTP call to the authoritative API). See [ESTD12](./ESTD12_-_Smartfox_Server_Standards.md#estd12--smartfox-server-standards-for-bingo-game-development) for SmartFox-specific concurrency rules.

### 13.4 Economic Operations Must Use Locks

Any operation that reads and writes a player's coin balance must use optimistic or pessimistic locking in MySQL. The exact framework or repository implementation may differ between the legacy PHP monolith and the Java/SEAM services, but the concurrency guarantee must be identical: the balance must not be spent twice and the transaction log must stay consistent.

```sql
-- Pessimistic (MySQL) — simple, safe for low-concurrency operations
BEGIN TRANSACTION;
SELECT coin_balance FROM players WHERE player_id = 1234 FOR UPDATE;
-- validate sufficient balance
UPDATE players SET coin_balance = coin_balance - 100 WHERE player_id = 1234;
INSERT INTO coin_transactions (...);
COMMIT;

-- Optimistic (MySQL) — higher throughput, requires retry logic
UPDATE players
SET    coin_balance = coin_balance - 100, version = version + 1
WHERE  player_id = 1234
  AND  version = :expectedVersion
  AND  coin_balance >= 100;
-- If affected_rows = 0, conflict occurred — retry or return error
```

**Java service equivalent (same version-column pattern):**

```java
int updated = jdbc.update(
    """
    UPDATE players
       SET coin_balance = coin_balance - ?,
           version = version + 1
     WHERE player_id = ?
       AND version = ?
       AND coin_balance >= ?
    """,
    amount,
    playerId,
    expectedVersion,
    amount
);

if (updated == 0) {
    throw new ConcurrencyConflictException("Balance changed concurrently or funds are insufficient");
}
```

### 13.5 Distributed Locks for Critical Cross-Service Sections

For operations that span multiple services (SmartFox + authoritative API), use Redis distributed locks:

```php
$lockKey = "lock:weekly_bonus:{$playerId}";
$lock = $this->redis->set($lockKey, 1, ['NX', 'EX' => 10]);

if (!$lock) {
    throw new ConcurrentRequestException("Bonus award in progress for player {$playerId}");
}

try {
    $this->bonusService->weeklyBonusAward($playerId);
} finally {
    $this->redis->del($lockKey);  // Always release — finally ensures this even on exception
}
```

### 13.6 Shared Data in Multi-Process Systems

Shared data is any server-side data that can be read or written by more than one process, server instance, request thread, scheduled job, or service. Treat shared data as a coordination problem, not just a storage problem.

Rules:

- Define one authoritative owner and source of truth for each data category. Other processes must read through that owner, use an approved API/event path, or use an explicitly documented replicated view. See [ESTD9 §4.1](./ESTD9_-_Database_Standards.md#41-single-responsibility-per-schema-and-clear-ownership).
- Treat process-local memory as a cache only. In-memory maps, PHP globals, JVM static fields, and local locks do not coordinate a multi-instance system.
- Critical writes must use database transactions, unique constraints, version columns, compare-and-set updates, or other atomic persistence-layer guarantees. See [§13.4](#134-economic-operations-must-use-locks) and [ESTD9 §10](./ESTD9_-_Database_Standards.md#10-transactions-and-concurrency).
- Distributed locks are allowed only for narrow, time-bounded cross-service critical sections. They must have explicit expiry, ownership, failure behavior, and release handling. See [§13.5](#135-distributed-locks-for-critical-cross-service-sections).
- Every cross-process write path must define idempotency and retry behavior before it ships. Duplicate requests, worker retries, client reconnects, and timeout retries must not double-award, double-spend, or double-apply state. See [§8](#8-idempotency).
- Cache, replica, and read-after-write behavior must be explicit. If stale data is acceptable, document the tolerance. If immediate correctness is required, read from the authoritative store. See [§15](#15-caching-strategy).
- Keep locks and transactions short. Do not perform network I/O, user I/O, or long computation while holding a database transaction, room lock, or distributed lock.
- Log and monitor concurrency signals: conflict retries, duplicate requests, deadlocks, lock wait time, lock acquisition failures, stale reads, and retry exhaustion.

SmartFox room state has additional real-time rules for lock scope, sequencing, reconnects, and split-brain recovery. See [ESTD12 §7](./ESTD12_-_Smartfox_Server_Standards.md#7-real-time-concurrency-and-thread-safety) and [ESTD12 §9](./ESTD12_-_Smartfox_Server_Standards.md#9-network-latency-strategies-at-critical-state-transition-junctures).

---

## 14. Service Communication Patterns

### 14.1 Legacy PHP Monolith

Communicate with external services through repository/gateway classes — never via direct inline calls in controllers.

### 14.2 Java Microservices Communication

- **Synchronous (HTTP/REST)**: Use when the caller needs an immediate answer. Always apply resilience patterns: circuit breaker, timeout (5 seconds max), retry with backoff.  
- **Asynchronous (SQS/SNS message bus)**: Use for operations that can be decoupled from the caller. Fan-out must use a message bus, not synchronous calls.

### 14.3 PHP API ↔ Java API

The new Java services must not query the PHP monolith's database directly. If a Java service needs data owned by the PHP monolith, a purpose-built endpoint must be added to the PHP API. This relationship is unidirectional until the PHP monolith is further decomposed.

### 14.4 SmartFox ↔ Authoritative API (Internal API)

Define a dedicated internal API for SmartFox → API-server communication, separate from the public client-facing API. For the classic game this is SmartFox → PHP; for the new game it may be SmartFox → Java/SEAM. Authenticate server-to-server calls with a shared secret stored in AWS Secrets Manager. This API must not be exposed to the internet — restrict via VPC security group. All inter-server calls must have explicit timeouts and retry logic.

---

## 15. Caching Strategy

See [ESTD1 §16. Caching: Concepts, Usage, and Tradeoffs](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#16-caching-concepts-usage-and-tradeoffs) for the foundational caching concepts (what a cache is, its advantages and risks, when to use and when not to use it). This section defines server-specific implementation standards.

### 15.1 What to Cache (Server-Side)

We use two server-side distributed cache layers: Redis (AWS ElastiCache) for session management, idempotency keys, leaderboards, rate-limit counters, and distributed locks; and a **custom internal caching server** for transient computed data and high-frequency game-state lookups.

| Data | Cache Location | TTL |
|:-----|:---------------|:----|
| Player session | Redis | Token expiry (1 hour) |
| Periodic event configuration | In-process + Redis | Until next content reset |
| Room list (lobby) | Redis | 30 seconds | 
| Player profile (read-heavy) | Redis | 5 minutes |
| Leaderboard snapshot | Redis | 60 seconds | 
| Feature flags | In-process + Redis | 1 minute |
| Idempotency keys | Redis | 24 hours |

### 15.2 Cache-Aside Pattern

```php
public function playerGet(int $playerId): Player
{
    $cacheKey = "player:{$playerId}";
    $cached = $this->cache->get($cacheKey);
    if ($cached !== null) {
        return Player::fromCache($cached);
    }
    $player = $this->playerRepository->findById($playerId);
    if ($player === null) { throw new PlayerNotFoundException($playerId); }
    $this->cache->set($cacheKey, $player->toCacheArray(), ttl: 300);
    return $player;
}
```

### 15.3 Cache Invalidation

On write: invalidate the relevant cache key. Use write-through caching for critical data. Never cache game outcomes or economic state — these must always be DB-authoritative.

### 15.4 Cache Stampede Prevention

During high-traffic moments (content reset Monday morning — even with the flexible cadence, predictable activity spikes occur), many simultaneous cache misses can overload the database. Use Redis `SET NX` (mutex locking) when regenerating expensive cached values so that only one request hits the DB:

```php
$cacheKey = "leaderboard:weekly";
$lockKey  = "lock:leaderboard:weekly:regen";
$cached = $this->cache->get($cacheKey);
if ($cached === null) {
    // Only one process regenerates; others wait briefly and re-read
    $lock = $this->redis->set($lockKey, 1, ['NX', 'EX' => 5]);
    if ($lock) {
        $leaderboard = $this->leaderboardRepository->weeklyCompute();
        $this->cache->set($cacheKey, $leaderboard, ttl: 60);
        $this->redis->del($lockKey);
    } else {
        usleep(200000); // 200ms wait, then re-read (the lock holder will have populated)
        $cached = $this->cache->get($cacheKey) ?? [];
    }
}
```

### 15.5 When NOT to Cache

Do not cache:

- **Game outcomes and economic state** (coin balance after a purchase, win results). These must always be database-authoritative.
- **Real-time state** (number of players currently in a room). This changes too frequently to cache usefully.
- **Security-sensitive data** (raw auth tokens, payment details).
- **Idempotency keys** in volatile cache — these require durable storage.

### 15.6 Advantages and Risks

**Advantages:** Speed (orders of magnitude faster than DB queries), reduced database load (fewer queries reach the DB), cost efficiency (smaller RDS instance requirements), and resilience (absorbs traffic spikes that would otherwise overload the database).

**Risks:** Staleness (cached data can become out of date — if a player's coin balance is cached for 5 minutes, they may see an old value), complexity (cache invalidation is notoriously difficult), false safety (a cache masks a slow DB — when the cache is cold after a restart, all traffic hits the DB simultaneously), and memory pressure (an unbounded cache will exhaust available memory).

---

## 16. Observability: Logging, Metrics, Alerting

All [ESTD1 §12. Logging](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#12-logging) logging rules apply. Additional server-specific log fields: `hostname` (EC2 instance or container ID), `deploymentVersion`, `endpoint` (API path), `durationMs`.

### 16.1 Minimum Required Metrics (Datadog)

| Metric | Type |
|:-------|:-----|
| `api.request.count` | Counter (by endpoint, status code) |
| `api.request.duration` | Histogram (by endpoint) — track p95, p98 |
| `db.query.duration` | Histogram (by query name) | 
| `cache.hit_rate` | Gauge | 
| `game.room.active_count` | Gauge |
| `game.player.connected_count` | Gauge | 
| `reward.claim.count` | Counter (by reward type, success/fail) | 
| `error.count` | Counter (by error code) | 

### 16.2 Understanding Metric Types

Selecting the correct metric type ensures dashboards and alerts behave correctly. The three primary metric types are defined in [ESTD1 §14.2 Metric Types: Counter, Histogram, and Gauge](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#142-metric-types-counter-histogram-and-gauge). A brief reference here for server engineers:

**Counter** — monotonically increasing count. Use for: `api.request.count`, `reward.claim.count`, `error.count`.

**Histogram** — distribution of measured values; used to derive p50/p95/p98 percentiles. Use for: `api.request.duration`, `db.query.duration`.

**Gauge** — point-in-time snapshot of a value that can go up or down. Use for any metric that represents **current state**, not a cumulative count.

In our Bingo service, Gauges represent live operational state:

```
game.room.active_count       → 823 rooms running right now
game.player.connected_count  → 12,450 players currently in SmartFox
cache.memory_used_mb         → 412 MB currently in Redis
db.connection_pool.used      → 28 of 50 DB connections in use right now
sqs.queue.depth              → 1,204 jobs waiting to be processed
```

Gauge-based alerts are critical for operations:

- `game.room.active_count` dropping below 5 during peak hours → likely a SmartFox crash.  
- `sqs.queue.depth` exceeding 5,000 → background job worker is behind; investigate. 
- `db.connection_pool.used` consistently > 80% → pool exhaustion imminent; scale up.

Gauges must be reported on a regular polling interval (every 10–30 seconds) rather than per-event, since they represent the current state of a system, not individual events.

### 16.3 Health Check Endpoint

Every server must expose a `/health` endpoint that responds in < 1 second and checks: application alive, DB connectivity, cache connectivity, and critical dependencies.

```
GET /health
```

```json
{
  "status": "healthy",
  "version": "2026.03.1",
  "checks": {
    "primary_database": "ok",
    "redis": "ok",
    "downstream_api": "ok",
    "smartfox_connection": "ok"
  },
  "uptime_seconds": 86400
}
```

---

## 17. Security Standards

### 17.1 Defense in Depth

Apply security at every layer: ALB/WAF → Security groups → Application validation → Database constraints. Never assume that because a request reached the application layer it is safe.

### 17.2 Input Validation

All input must be validated at the API boundary before any database interaction. Never let raw input reach a query, even a parameterized one. Validation failures return 400.

### 17.3 Injection and Unsafe Query Construction — Zero Tolerance

Use parameterized queries for all values. For dynamic `ORDER BY`, identifier selection, or optional filters, use explicit allowlists. Never pass raw field names, operators, or query fragments from a client straight into SQL or an internal query builder.

```php
// SQL value parameterization — REQUIRED
// BAD:  "SELECT * FROM players WHERE player_id = $playerId"
// GOOD: prepared statement with bound parameter

$allowedSorts = ['created_at_utc', 'reward_id'];
$sort = in_array($requestedSort, $allowedSorts, true) ? $requestedSort : 'created_at_utc';
$sql  = "SELECT reward_id, created_at_utc FROM reward_claims ORDER BY {$sort} DESC LIMIT 50";
```

### 17.4 Audit Logging

The following events must be written to a separate audit log (append-only, 90-day retention minimum)

- player login/logout, 
- purchase events, 
- admin actions, 
- bonus awards, 
- account modifications, 
- security rejections.

### 17.5 Server/API Security Vulnerabilities

The following table lists the vulnerability categories most relevant to our PHP monolith and Java microservice APIs. This is the authoritative reference for server-side security awareness; see [ESTD1 §20. Security Vulnerability Awareness by Domain](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#20-security-vulnerability-awareness-by-domain) for cross-cutting security rules.

| Vulnerability | What It Looks Like in Our Environment | Required Controls |
|:--------------|:--------------------------------------|:------------------|
| **SQL injection** | Request parameters or payload fields are interpolated into SQL and allow an attacker to read, modify, or delete data | Parameterized queries only; never concatenate untrusted values into SQL; validate query intent at the boundary |
| **Unsafe dynamic query construction** | Sort fields, filter names, table names, or SQL fragments are built from user input even when values are parameterized | Use allowlists for identifiers and sort keys; centralize query construction in repository helpers; reject unknown fields |
| **Broken Object-Level Authorization (BOLA / IDOR)** | A player changes an ID in the request and accesses another player's profile, inventory, mailbox, or purchase state | Verify ownership and entitlement server-side on every request; never trust client-supplied subject identifiers |
| **Broken Function-Level Authorization** | Player-facing routes reach admin, moderation, economy adjustment, or content-management functions | Enforce explicit role checks on every privileged endpoint; deny by default; separate player and operator surfaces where possible |
| **Mass assignment** | API models accept fields the caller must never control, such as admin flags, economy balances, or backend-only status values | Allowlist accepted fields; keep server-controlled fields readonly; map DTOs (Data Transfer Objects) to domain objects explicitly |
| **Insecure deserialization** | Untrusted serialized payloads or polymorphic objects trigger unexpected code execution or unsafe state creation | Use JSON with strict schema validation; forbid native Java serialization for untrusted input; reject unknown fields and types |
| **Server-Side Request Forgery (SSRF)** | User-controlled URLs or content imports cause the server to call internal services, metadata endpoints, or private hosts | Never fetch arbitrary user-supplied URLs; use explicit allowlists; block link-local and private address ranges |
| **Cross-Site Scripting (XSS) on web or tool surfaces** | User or CMS (Content Management System) content is rendered into browser-delivered experiences or operator tools without output encoding | HTML-encode output by context, use CSP (Content Security Policy), and never inject raw untrusted HTML into operator or player-facing web surfaces |
| **Excessive data exposure / sensitive error leakage** | APIs return full rows, debug fields, stack traces, internal paths, or schema details that help an attacker | Return only required fields; never expose raw exceptions to the client; log details server-side only |
| **Business logic abuse / state-machine bypass** | A valid endpoint is called out of order, such as claiming a reward before qualifying or joining a room without prerequisites | Encode preconditions and state transitions on the server; reject invalid order-of-operations even if the request shape is technically valid |
| **Economic race condition / double claim** | Concurrent requests duplicate claims, purchases, or balance changes before the first update is committed | Use idempotency keys, unique constraints, transactions, row/version locking, and server-side sequencing for economy operations |
| **Rate-limit bypass** | Attackers distribute requests across IPs, devices, or retries to evade naive throttles | Rate-limit by authenticated player identity and risk context, not IP alone; monitor hot endpoints and abuse spikes |
| **Hardcoded secrets** | API keys, DB passwords, or signing keys are embedded in source code or static config files | Use managed secret stores only; inject secrets at runtime via approved patterns; rotate on exposure |

### 17.6 Server Trust and Permission Boundaries

Trust and permission boundaries must be designed explicitly for every server feature. A trust boundary decides when information may be believed. A permission boundary decides what the caller, service, job, or credential is allowed to do even if it is valid. These rules build on [ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions), [ESTD1 §11. Input Validation and Sanitization](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#11-input-validation-and-sanitization), [§5. Authentication and Authorization](#5-authentication-and-authorization), [§6. Input Validation at the Server Boundary](#6-input-validation-at-the-server-boundary), [§9. Boundary Functions — Server-Side Structure](#9-boundary-functions--server-side-structure), and [§10. Anatomy of a Good Request Handler](#10-anatomy-of-a-good-request-handler).

**Server rule:** Trust the source only for the claim it is authoritative for. The session is authoritative for authenticated player identity. The server database is authoritative for balances, ownership, eligibility, and reward state. The client is authoritative only for user intent, such as "player tapped claim"; it is never authoritative for economy results, entitlement state, or role permissions.

| Source | Trust Level | Never Trust Directly | Controls Before Crossing Boundary | Risk If Skipped |
|:-------|:------------|:---------------------|:----------------------------------|:----------------|
| Player HTTP/API request | Untrusted until session, ownership, and payload checks pass | Player ID, balance, reward amount, purchase status, timestamps | Authenticate token, authorize ownership, validate payload, rate-limit, enforce idempotency | Account takeover impact, forged rewards, duplicate claims |
| SmartFox client message | Untrusted until handler validates session and room state | Room membership, daub validity, win claim, client sequence state | Validate session, room membership, sequence ID, room state, and server-side win rules | Fraudulent wins, room corruption, reconnect abuse |
| Internal tool request | Partially trusted after operator login; still action-scoped | Target player, role, reason, destructive action scope | Role-based access control (RBAC), server-side validation, confirmation for destructive actions, audit log | Unauthorized support actions, personally identifiable information (PII) exposure, economy damage |
| Service-to-service call | Partially trusted after service identity check | Caller intent, tenant/player scope, requested operation | Mutual service auth where available, allowlisted caller role, request schema validation, timeout and replay checks | Lateral movement between services, hidden coupling, data leakage |
| Queue job or scheduled trigger | Partially trusted; message may be stale or duplicated | Payload freshness, retry count, operation uniqueness | Message schema, version, timestamp/time-to-live (TTL), idempotency key, dead-letter handling | Duplicate awards, stale content reset, runaway retries |
| Third-party webhook | Untrusted until signature and event state are checked | Event type, amount, user mapping, callback order | Signature check, timestamp window, replay detection, provider allowlist, server-side reconciliation | Payment fraud, entitlement mismatch, replayed purchases |
| Database result | Trusted for persisted state only within its schema and isolation rules | That the caller may expose every field or mutate every row | Repository access, field projection, transaction rules, row ownership checks | Sensitive data exposure, cross-player writes, schema coupling |
| Secret or config read | Partially trusted until environment and version are verified | That the value belongs to this service/environment | Secrets manager access through scoped role, config version/expiry checks, safe defaults | Production secret leakage, wrong environment behavior |
| Migration or backfill job | Highly privileged and time-bound | Unlimited scope, rerun safety, production target | CI approval, scoped migration credential, dry-run where possible, batch limits, verification query | Data loss, broad corruption, irreversible schema changes |
| Cloud role / Identity and Access Management (IAM) permission | Permission boundary, not business authorization | That broad cloud permission is safe for app logic | Least privilege by service/environment/resource; no wildcard admin access; quarterly review | Compromised service can read secrets, alter infra, or access unrelated data |

**Permission boundary rules:**

- Runtime applications must not use migration, admin, root, or break-glass credentials.
- Privileged jobs must be separate from request-serving roles and must be time-limited where the platform supports it.
- Internal tools must enforce server-side RBAC; hiding a button in the UI is not authorization.
- A service may hold broad permission only with written approval, clear expiry, and audit evidence.
- Over-provisioning is a security bug, not harmless convenience. It increases the blast radius of any compromised service, leaked token, or unsafe code path.

**PHP API example — trust session identity, not request body:**

```php
// BAD: body playerId is untrusted, even when the session is valid.
$playerId = (int)$request->getParsedBody()['playerId'];

// GOOD: identity comes from the authenticated session; body only carries intent.
$authenticatedPlayerId = $request->getAuthenticatedPlayerId();
$input = $this->claimRewardValidator->validate($request->getParsedBody());
$this->rewardService->claim($authenticatedPlayerId, $input->rewardId);
```

**Java/SEAM example — service identity is not enough; authorize operation scope:**

```java
@RouteHandler(method = HttpMethod.POST, path = "/internal/rewards/reconcile")
@RequiresServiceIdentity
public ApiResponse reconcileReward(SeamRequest request) {
    ServiceIdentity caller = request.serviceIdentity();
    if (!caller.hasRole("payment-reconciler")) return ApiResponse.forbidden("SERVICE_NOT_ALLOWED");

    ReconcileRewardRequest body = request.parseBody(ReconcileRewardRequest.class);
    ValidationResult validation = body.validate();
    if (!validation.isValid()) return ApiResponse.badRequest(validation.errors());

    return ApiResponse.ok(rewardReconcileService.reconcile(body.providerEventId()));
}
```

**C#/Unity example — client sends intent only, never authority:**

```csharp
// BAD: client claims the result.
await api.PostAsync("/rewards/claim", new { rewardId, coinsAwarded = 5000 });

// GOOD: client sends intent; server computes eligibility and award.
await api.PostAsync("/rewards/claim", new ClaimRewardRequest {
    RewardId = rewardId,
    ClientNonce = requestNonce
});
```

**TypeScript/NextJS example — tool backend enforces RBAC before calling server APIs:**

```typescript
export async function POST(request: Request) {
  const session = await requireOperatorSession(request);
  if (!session.roles.includes("support.balance_adjust")) {
    return Response.json({ error: "FORBIDDEN" }, { status: 403 });
  }

  const body = adjustBalanceSchema.parse(await request.json());
  await auditLog.write({ actorId: session.userId, action: "balance_adjust", targetPlayerId: body.playerId });

  return gameApi.adjustBalance({
    actorId: session.userId,
    playerId: body.playerId,
    deltaCoins: body.deltaCoins,
    reason: body.reason,
  });
}
```

---

## 18. Deployment and Configuration

### 18.1 Zero-Downtime Deployments

The PHP API uses rolling or blue/green deployment via ASG (see [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure)). The Java microservices use rolling deployment via ECS. SmartFox requires a maintenance window with room draining.

**Deployment blackout windows** (do not deploy during):

- Within 30 minutes before or after a scheduled content reset or launch  
- Fridays after 3 PM IST (approaching US peak hours)  
- Any time active player count is > 150% of typical baseline

### 18.2 Feature Flags

All new features must ship behind a server-controlled feature flag. Feature flags are readable at runtime without a deploy. A flag must have: name, description, owner, creation date, and expiry date. Dead flags must be removed within 2 sprints.

### 18.3 Build Promotion Policy

Applies to server deployments (see also [ESTD1 §24.5 Build Promotion Policy](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#245-build-promotion-policy)):

```
Dev → QA (passes CI: lint, unit tests, integration tests)
QA  → Staging (passes QA functional sign-off)
Staging → Production (passes load test, architect approval, stakeholder sign-off)
```

The same Docker image / deployment artifact must be promoted through all stages. Rebuilding for production is prohibited.

---

## 19. Disaster Recovery Readiness

### 19.1 What are RTO and RPO?

When an outage occurs, two questions immediately arise: "How long will we be down?" and "How much data will we lose?" RTO and RPO are the formal definitions of acceptable answers to those questions. Setting them in advance — not during the incident — is critical for making calm, principled recovery decisions.

```
RTO — Recovery Time Objective
───────────────────────────────
The maximum acceptable duration of an outage before the service must be
restored to a functional state.

  "If our database fails, our RTO is 60 seconds" means:
  We must restore DB availability within 60 seconds of failure.

  If recovery takes longer than the RTO, we are breaching our SLA.
  RTO drives decisions about failover speed, redundancy, and automation.

RPO — Recovery Point Objective
───────────────────────────────
The maximum acceptable amount of data loss, measured in time.

  "Our RPO is 1 hour" means:
  In the worst case, we are willing to lose up to 1 hour of transactions.
  All data from more than 1 hour ago must be recoverable.

  RPO drives decisions about backup frequency, replication lag,
  and whether point-in-time recovery is required.

Visual:

  |──── RPO ────|──────────── RTO ────────────|
  ↑             ↑                             ↑
  Last good     Failure                       Service
  backup        event                         restored
```

### 19.2 RTO and RPO Targets

| Scenario | RTO | RPO |
|:---------|:----|:----|
| Single EC2 instance failure (stateless) | < 5 minutes (ASG replaces) | 0 (no state on instance) |
| RDS primary DB failure | < 60 seconds (automated Multi-AZ failover) | < 5 seconds (synchronous replica) | 
| RDS read replica / reporting replica failure | < 15 minutes (remove from traffic and recreate) | 0 (primary remains source of truth) |
| Availability Zone failure | < 5 minutes (ASG distributes across AZs) | 0 (stateless) |
| Redis failure | < 30 seconds (ElastiCache failover) | Acceptable (session cache; players re-auth) |
| SmartFox instance failure | < 15 minutes (room evacuation + reconnect) | Active room state (players in-game must reconnect) | 
| Accidental data deletion |< 1 hour (restore from snapshot) | < 1 day (daily backup) |
| Full region failure | < 4 hours (manual Data Recovery runbook) | < 1 hour (cross-region backup) |

### 19.3 Failure Mode Planning

For each critical component, define and document its failure mode and recovery action:

| Component | Failure Impact | Recovery Action |
|:----------|:---------------|:----------------|
| PHP API EC2 instance | Reduced capacity; other instances absorb traffic | ASG auto-replaces within 5 min |
| RDS MySQL primary | Players cannot auth or claim rewards | RDS Multi-AZ auto-failover to standby | 
| RDS read replica / reporting DB | Reporting or non-critical read paths degrade | Remove from traffic; rebuild or recreate replica |
| Redis | Degraded performance; auth sessions lost | Players re-authenticate; cache rebuilds | 
| SmartFox | Active games interrupted | Clients reconnect; rooms recover from DB |
| SQS (job queue) | Background jobs queue; not lost | Jobs process when queue restored |

### 19.4 Graceful Degradation

Design systems so secondary features degrade before core gameplay does:

- Leaderboard unavailable → show "temporarily unavailable" — do not block room join. 
- Asset CDN unavailable → serve placeholder art — do not block gameplay.  
- Analytics pipeline unavailable → buffer events locally — do not slow the API.

### 19.5 Circuit Breaker Pattern

When calling external dependencies (SmartFox → authoritative API, API → third-party services), implement a circuit breaker to prevent one slow dependency from bringing down the entire system:

```
State machine:
  CLOSED (normal) ──→ OPEN (failing) ──→ HALF-OPEN (testing)
                  ←────────────────────────────────────

  CLOSED → OPEN:      After 5 consecutive failures or > 50% failure rate in 10s
  OPEN → HALF-OPEN:   After 30 seconds cooldown
  HALF-OPEN → CLOSED: After first successful call
  HALF-OPEN → OPEN:   If the test call also fails
```

### 19.6 Retry with Exponential Backoff

When retrying failed operations (database calls, inter-service requests, external API calls), use exponential backoff with jitter. Only retry operations that are idempotent (safe to call multiple times).

```
Initial delay: 100ms
Backoff multiplier: 2×
Jitter: ±20%
Max retries: 3
Max delay cap: 5 seconds
```

Example retry sequence: 100ms → 200ms → 400ms (each ±20% jitter). After the third retry fails, the operation must be recorded as failed and handled through the normal error path — not retried indefinitely.

### 19.7 Runbooks

Every CRITICAL alert must have a linked runbook. The runbook must describe: what the alert means, what to check first, common causes, resolution steps, and escalation path.

---

## 20. Server Code Hygiene

Code hygiene standards applicable across all server domains are rooted in [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers). This section cross-references them as server-specific hygiene imperatives.

| Hygiene Practice | Standard Reference |
|:-----------------|:-------------------|
| Maximum 250 LOC per file, 40 LOC per method | [ESTD1 §6. File and Class Size Constraints](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#6-file-and-class-size-constraints) |
| Named constants — no magic numbers or strings in logic | [ESTD1 §3. Philosophy](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#3-philosophy), [ESTD1 §4. Naming Conventions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#4-naming-conventions) | 
| Parameterized queries — no SQL string concatenation | [ESTD9 §7.1 Every Table Must Have a Primary Key](./ESTD9_-_Database_Standards.md#71-every-table-must-have-a-primary-key) |
| Structured JSON logging with correlation IDs | [ESTD1 §12.2 What Every Log Entry Must Contain](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#122-what-every-log-entry-must-contain) | 
| No secrets in source code or environment variables | [ESTD1 §19. Secrets Management](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#19-secrets-management) |
| API versioning from day one | [§4.6 Versioning](#46-versioning) of this document |
| Idempotency keys on all write operations | [§8. Idempotency](#8-idempotency) of this document | 
| Domain object separation — never pass `ISFSObject` into the game engine | [ESTD12 §5. SmartFox Data Abstraction](./ESTD12_-_Smartfox_Server_Standards.md#5-smartfox-data-abstraction) | 
| Remove dead endpoints during the same sprint they become unused | [ESTD1 §3.1 Every Line of Code Is a Liability](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#31-every-line-of-code-is-a-liability) | | Every microservice owns its own schema — no cross-service DB coupling | [§2.3 New Java API: Microservice Design Principles](#23-new-java-api-microservice-design-principles) of this document |
| SEAM service classes are not allowed to reference `SeamRequest` or HTTP types | Boundary function rule — [§9. Boundary Functions — Server-Side Structure](#9-boundary-functions--server-side-structure) of this document |

---

## 21. Common Pitfalls to Avoid

| # | Pitfall | Impact | Remedy |
|:--|:--------|:-------|:-------|
| 1 | SmartFox awarding currency without authoritative API validation | Economic integrity failure | SmartFox coordinates only; the API server awards all currency |
| 2 | Race condition in bonus claim | Double-award | Idempotency key + DB unique constraint |
| 3 | N+1 ORM queries | Exponential DB load | Eager-load or batch fetch related entities |
| 4 | Missing database index on Foreign Key or WHERE column | Slow queries under load | Add index in the migration that introduces the query |
| 5 | Hardcoded content reset period (7 days) | Breaks when cadence changes | Read from configuration |
| 6 | Missing timeout on inter-service call | Slow dependency cascades into full outage | 5-second max timeout + circuit breaker |
| 7 | Deploying during content reset window | Deploying into a traffic spike | Enforce deployment blackout windows |
| 8 | Caching coin balances | Player sees stale balance | Never cache economic state |
| 9 | PHP monolith querying Java service's DB directly | Breaks service ownership | Use service API contracts only |
| 10 | No `finally` block when holding distributed lock | Lock never released on exception | Always release locks in `finally` |
