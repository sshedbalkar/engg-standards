# ESTD17 — Waterfall Data Processing Pattern

| Field | Value |
|:----- |:----- |
| **Document ID** | ESTD17 |
| **Version** | 1.1 |
| **Status** | Draft |
| **Last Updated** | 2026-04-13 |
| **Applies To** | All engineers — client, server, tools, website, automation |
| **Depends On** | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), [ESTD14](./ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md#estd14---hierarchical-naming-strategy-for-programming-entities) |
| **Approval** | Director of Engineering |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

This document defines the **Waterfall Data Processing Pattern** — a structural approach to designing data transformation pipelines where input flows through a sequence of processors, each narrowing from generic to specific, and where a partial result is always produced even if one or more processors fail or are absent.

Read [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) before this document. The principles of fail-gracefully, minimal blast radius, and clarity over cleverness underpin every rule here. Read [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices) for the server-side architecture context in which this pattern is most frequently applied. Read [ESTD14](./ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md#estd14---hierarchical-naming-strategy-for-programming-entities) for the naming conventions used when naming processor classes, methods, and pipeline stages.

This document covers the structural pattern and its application across all four stacks. It does **not** cover streaming or event-driven pipelines (e.g., Kafka, SQS consumer chains), batch ETL at the infrastructure level, or performance optimisation of individual processors. Those topics are addressed in [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management) and [ESTD9](./ESTD9_-_Database_Standards.md#estd9---database-standards-and-best-practices) respectively.

Where a conflict exists between this document and [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) takes precedence except in the narrow area of processor-chain architecture, where this document governs.

---

## Table of Contents

- [ESTD17 — Waterfall Data Processing Pattern](#estd17--waterfall-data-processing-pattern)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Conceptual Foundation](#2-conceptual-foundation)
    - [2.1 What Is the Waterfall Processing Pattern?](#21-what-is-the-waterfall-processing-pattern)
    - [2.2 The Fundamental Contract](#22-the-fundamental-contract)
    - [2.3 Why Generic Before Specific?](#23-why-generic-before-specific)
  - [3. Structural Definitions](#3-structural-definitions)
    - [3.1 The Pipeline Context](#31-the-pipeline-context)
    - [3.2 The Processor Interface](#32-the-processor-interface)
    - [3.3 The Pipeline Coordinator](#33-the-pipeline-coordinator)
    - [3.4 Processor Granularity](#34-processor-granularity)
  - [4. Flow Diagrams](#4-flow-diagrams)
    - [4.1 Normal Flow (All Processors Succeed)](#41-normal-flow-all-processors-succeed)
    - [4.2 Partial Flow (One Processor Fails Mid-Chain)](#42-partial-flow-one-processor-fails-mid-chain)
    - [4.3 Processor Skipping vs. Processor Failing](#43-processor-skipping-vs-processor-failing)
  - [5. Naming Conventions for Pipeline Entities](#5-naming-conventions-for-pipeline-entities)
    - [5.1 Processor Class Names](#51-processor-class-names)
    - [5.2 Context Class Names](#52-context-class-names)
    - [5.3 Coordinator Class Names](#53-coordinator-class-names)
    - [5.4 Result Field Names on the Context](#54-result-field-names-on-the-context)
  - [6. Code Examples](#6-code-examples)
    - [6.1 PHP (Legacy API Server)](#61-php-legacy-api-server)
    - [6.2 Java (New API Server — SEAM Microservice)](#62-java-new-api-server--seam-microservice)
    - [6.3 Unity C# (Client)](#63-unity-c-client)
    - [6.4 TypeScript / NextJS (Internal Tools)](#64-typescript--nextjs-internal-tools)
    - [6.5 Java (SmartFox Extension Handler)](#65-java-smartfox-extension-handler)
  - [7. Design Rules](#7-design-rules)
    - [7.1 Ordering Rule: Generic Before Specific](#71-ordering-rule-generic-before-specific)
    - [7.2 Precondition Checks Are Mandatory](#72-precondition-checks-are-mandatory)
    - [7.3 Processors Must Not Call Other Processors](#73-processors-must-not-call-other-processors)
    - [7.4 Processors Must Not Modify Prior Results](#74-processors-must-not-modify-prior-results)
    - [7.5 The Pipeline Always Returns the Context](#75-the-pipeline-always-returns-the-context)
    - [7.6 Partial Results Are Valuable](#76-partial-results-are-valuable)
    - [7.7 Processor Registration Order Is the Authoritative Declaration](#77-processor-registration-order-is-the-authoritative-declaration)
  - [8. Testing Requirements](#8-testing-requirements)
    - [8.1 Test Each Processor in Isolation](#81-test-each-processor-in-isolation)
    - [8.2 Required Test Cases Per Processor](#82-required-test-cases-per-processor)
    - [8.3 Test the Coordinator's Safety Net](#83-test-the-coordinators-safety-net)
    - [8.4 Test the Assembled Pipeline for Integration Confidence](#84-test-the-assembled-pipeline-for-integration-confidence)
  - [9. Relationship to Other Patterns and Standards](#9-relationship-to-other-patterns-and-standards)
    - [9.1 Relationship to Boundary Functions](#91-relationship-to-boundary-functions)
    - [9.2 Relationship to Error Handling Standards](#92-relationship-to-error-handling-standards)
    - [9.3 Relationship to the Naming Strategy](#93-relationship-to-the-naming-strategy)
  - [10. Anti-Patterns to Avoid](#10-anti-patterns-to-avoid)
  - [11. Quick Reference Checklist](#11-quick-reference-checklist)
  - [12. When to Use This Pattern — and When Not To](#12-when-to-use-this-pattern--and-when-not-to)
    - [12.1 When to Use](#121-when-to-use)
    - [12.2 When Not to Use](#122-when-not-to-use)
    - [12.3 The Decision Heuristic](#123-the-decision-heuristic)

---

## 1. Purpose and Scope

Complex operations in our codebase — reward processing, game state resolution, player data normalisation, report generation, configuration loading — share a common problem: they receive raw input that must pass through several discrete transformation stages before a final result is produced. When these stages are tangled into a single monolithic function or scattered across unrelated classes, any defect in one stage can break the entire operation and leave the system with no result at all.

The **Waterfall Data Processing Pattern** addresses this by organising transformation logic into a well-defined chain of processors, ordered from the most generic concern to the most specific, where:

1. Each processor has a single, clearly scoped responsibility.
2. Processors are composable and independently testable.
3. The pipeline always produces a partial result — even when a processor is missing or fails — allowing downstream consumers to make the most of whatever information was successfully produced.
4. The chain is transparent: any observer can see which processors ran, which were skipped, and what each contributed to the final result.

**This document applies to:**

- All server-side logic written in PHP (legacy API), Java/SEAM (new game microservices), and TypeScript (internal tools)
- All client-side game logic written in Unity C# where data passes through multiple transformation stages
- Any engineer designing a new feature, service, or utility that transforms input data through more than two discrete stages
- Any engineer refactoring an existing monolithic transformation function

**This document does not cover:**

- Streaming pipelines (Kafka, AWS Kinesis, SQS fan-out) — see [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management)
- Database-level ETL or migration scripts — see [ESTD9](./ESTD9_-_Database_Standards.md#estd9---database-standards-and-best-practices)
- SmartFox real-time coordination rules (room lifecycle, concurrency, state machines) — see [ESTD12](./ESTD12_-_Smartfox_Server_Standards.md#estd12--smartfox-server-standards-for-bingo-game-development). SmartFox extension handlers **can and should** use this pattern in non-hot path requests to process the body of a request after it reaches the handler; that use is covered in [§6.5 Java (SmartFox Extension Handler)](#65-java-smartfox-extension-handler)
- The general error handling rules that govern individual processors — those are defined in [ESTD1 §9. Error Handling and Try-Catch Usage](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#9-error-handling-and-try-catch-usage)

---

## 2. Conceptual Foundation

### 2.1 What Is the Waterfall Processing Pattern?

The term **waterfall** here refers not to the software development lifecycle methodology, but to the physical metaphor: water flowing over a series of rock ledges, each ledge catching and shaping the flow before passing it on. At each ledge, some work is done. If one ledge is missing or broken, the water continues past it — altered but still flowing.

In programming, the pattern describes a **linear chain of processors** through which a data context object passes. Each processor reads the current state of the context, performs its scoped transformation, enriches the context with its result, and passes the enriched context to the next processor. No processor depends on any processor that follows it. Each processor may skip itself if its preconditions are not met — it does not abort the chain.

```
Raw Input
    │
    ▼
┌──────────────────┐
│  Processor 1     │  ← Most generic concern (e.g., parse and validate structure)
│  (Generic)       │
└────────┬─────────┘
         │  Enriched Context (partial result)
         ▼
┌──────────────────┐
│  Processor 2     │  ← Narrower concern (e.g., resolve references)
│  (Less Generic)  │
└────────┬─────────┘
         │  Enriched Context (partial result + Processor 2's contribution)
         ▼
┌──────────────────┐
│  Processor 3     │  ← Even narrower (e.g., apply business rules)
│  (Specific)      │
└────────┬─────────┘
         │  Enriched Context (partial result + Processor 3's contribution)
         ▼
┌──────────────────┐
│  Processor N     │  ← Most specific concern (e.g., format final output)
│  (Most Specific) │
└────────┬─────────┘
         │
         ▼
    Final Result
    (or best partial result if some processors were skipped)
```

### 2.2 The Fundamental Contract

Every processor in the chain must honour three guarantees:

| Guarantee | Definition |
| :-------- | :--------- |
| **Non-destructive** | A processor must never remove or overwrite data that a previous processor already wrote to the context, unless that is its explicitly defined role. |
| **Self-contained** | A processor reads only from the context (and its own injected dependencies). It does not call other processors directly, does not assume ordering of sibling processors, and does not reach into the pipeline coordinator's state. |
| **Fail-graceful** | If a processor encounters an error it cannot recover from, it marks itself as failed in the context and exits cleanly. It does not throw an unhandled exception that terminates the pipeline. |

These three guarantees are what make partial results possible. If a processor in the middle of the chain fails, all processors before it have already contributed their results to the context. All processors after it will still run against that enriched partial context and contribute what they can. The final result is the best possible output given the available information.

### 2.3 Why Generic Before Specific?

The ordering rule — generic processors run first, specific processors run last — is not arbitrary. It directly maps to dependency: specific processors almost always depend on the output of generic processors.

Consider a reward claim pipeline:

```
1. Input Validation Processor     ← Generic: is the request well-formed?
2. Player Resolution Processor    ← Less generic: who is the player making this claim?
3. Reward Eligibility Processor   ← Specific: is this player eligible for this reward?
4. Reward Calculation Processor   ← More specific: how much should this player receive?
5. Reward Award Processor         ← Most specific: write the award to the database
6. Notification Processor         ← Specific concern: notify the player
```

Processor 3 (Eligibility) cannot run meaningfully if Processor 2 (Player Resolution) did not produce a valid player object. Processor 5 (Award) cannot run if Processor 4 (Calculation) produced no amount. The generic-to-specific ordering makes these dependencies explicit through position rather than through fragile inter-processor calls.

---

## 3. Structural Definitions

### 3.1 The Pipeline Context

The **pipeline context** is the shared mutable object that carries state through the entire chain. It is the only channel of communication between processors.

A well-designed context object has four responsibilities:

1. **Carry the original input** unchanged, so any processor can inspect what the pipeline received.
2. **Accumulate intermediate results** contributed by each processor.
3. **Track processor execution status** — which processors ran, which were skipped, which failed, and why.
4. **Signal the final outcome** — success, partial success, or failure — with enough detail for the pipeline's caller to act on.

```
PipelineContext
├── originalInput            ← never mutated after creation
├── processorResults[]       ← each processor appends its own result
│   ├── processorId
│   ├── status (SUCCESS | SKIPPED | FAILED)
│   ├── output               ← the data this processor produced
│   └── failureReason        ← populated only when status = FAILED
├── isComplete               ← true when all processors ran successfully
└── partialResultAvailable   ← true when at least one processor succeeded
```

### 3.2 The Processor Interface

Every processor in a chain must implement a common interface. The interface defines a single method that accepts the context and returns the context (enriched). The return type is the same as the input type to allow fluent chaining.

```
interface DataProcessor<TContext extends PipelineContext> {
    process(context: TContext): TContext
}
```

The interface is intentionally minimal. Processors do not know about each other. They do not know what order they are called in. They know only the contract: receive a context, do your work, return the enriched context.

### 3.3 The Pipeline Coordinator

The **pipeline coordinator** is the single object responsible for assembling the processor chain and executing it in order. It is not a processor itself — it has no domain logic. Its only responsibilities are:

1. Hold the ordered list of processors.
2. Invoke each processor in sequence, passing the context from one to the next.
3. Catch any unhandled exception from a processor (a contract violation), log it, mark that processor as failed in the context, and continue to the next processor.
4. Return the final context to the caller after all processors have run.

```
PipelineCoordinator
├── processors[]          ← ordered list, generic to specific
├── execute(input)
│   ├── create context from input
│   ├── for each processor:
│   │   ├── try: processor.process(context)
│   │   └── catch: log, mark failed, continue
│   └── return final context
```

The coordinator is the **only** place in the chain where a block try-catch is acceptable (per [ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)). The processor itself must handle its own specific errors; the coordinator's catch is a safety net for processor contract violations.

### 3.4 Processor Granularity

One processor = one responsibility. The test for correct granularity is the same as for any single-responsibility unit (per [ESTD1 §6.3 Methods](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#63-methods)): if describing what a processor does requires the word "and", it should be two processors.

| Too broad (split it) | Correct granularity |
| :------------------- | :------------------ |
| Validates input **and** resolves the player | Validation Processor; Player Resolution Processor |
| Calculates reward **and** persists it | Reward Calculation Processor; Reward Persistence Processor |
| Formats output **and** sends notification | Output Formatting Processor; Notification Processor |

---

## 4. Flow Diagrams

### 4.1 Normal Flow (All Processors Succeed)

```
Input
  │
  ├─► Processor 1 ──► Context{P1: SUCCESS} ─┐
  │                                          │
  ├─────────────────────────────────────────►├─► Processor 2 ──► Context{P1:OK, P2: SUCCESS} ─┐
  │                                                                                             │
  ├────────────────────────────────────────────────────────────────────────────────────────────►├─► ... ──► Final Context{all: SUCCESS}
  │                                                                                                                    │
  │                                                                                                                    ▼
  │                                                                                                             Output (complete)
```

Simplified:

```
Input
  │
  ▼
[P1: Validate]──► context.p1 = OK
  │
  ▼
[P2: Resolve Player]──► context.p2 = player object
  │
  ▼
[P3: Check Eligibility]──► context.p3 = eligible
  │
  ▼
[P4: Calculate]──► context.p4 = amount
  │
  ▼
[P5: Persist Award]──► context.p5 = persisted record
  │
  ▼
[P6: Notify]──► context.p6 = notification sent
  │
  ▼
Final Context: isComplete = true
Output: full reward claim result
```

### 4.2 Partial Flow (One Processor Fails Mid-Chain)

```
Input
  │
  ▼
[P1: Validate]──► context.p1 = OK
  │
  ▼
[P2: Resolve Player]──► context.p2 = player object
  │
  ▼
[P3: Check Eligibility]──► FAILED (DB timeout)
  │                         context.p3 = {status: FAILED, reason: "DB_TIMEOUT"}
  │                         (processor exits cleanly — does NOT throw)
  ▼
[P4: Calculate]──► SKIPPED (precondition: p3 must be SUCCESS)
  │                 context.p4 = {status: SKIPPED, reason: "P3_FAILED"}
  ▼
[P5: Persist Award]──► SKIPPED (precondition: p4 must be SUCCESS)
  │
  ▼
[P6: Notify]──► SKIPPED (precondition: p5 must be SUCCESS)
  │
  ▼
Final Context: isComplete = false, partialResultAvailable = true
Output: partial result — caller knows player was resolved,
        eligibility check failed at DB, award not granted
        (caller can retry eligibility check specifically)
```

The key observation: **processors P1 and P2 still ran and produced useful output.** The caller receives enough context to log a meaningful error, retry the specific failed stage, or return a structured partial response to the client rather than a generic 500.

### 4.3 Processor Skipping vs. Processor Failing

These are distinct states that must be tracked separately in the context.

| State | Meaning | Downstream effect |
| :---- | :------ | :---------------- |
| `SUCCESS` | Processor ran and produced its output | Downstream processors may proceed |
| `SKIPPED` | Processor did not run because its precondition was not met | Downstream processors that depend on this processor also skip |
| `FAILED` | Processor ran but encountered an unrecoverable error | Downstream processors that depend on this processor skip |
| `NOT_APPLICABLE` | Processor is part of the chain but this input type does not require it | Pipeline continues normally; this is not an error |

---

## 5. Naming Conventions for Pipeline Entities

Follow the [ESTD14](./ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md#estd14---hierarchical-naming-strategy-for-programming-entities) Hierarchical Naming Strategy throughout. Apply the generic-to-specific ordering to processor names just as to any other programming entity.

### 5.1 Processor Class Names

Pattern: `<Domain><Stage><Action>Processor`

```
RewardClaimValidationProcessor       ← domain=Reward, stage=Claim, action=Validation
RewardClaimPlayerResolutionProcessor ← domain=Reward, stage=Claim, action=PlayerResolution
RewardClaimEligibilityProcessor      ← domain=Reward, stage=Claim, action=Eligibility
RewardClaimCalculationProcessor      ← domain=Reward, stage=Claim, action=Calculation
RewardClaimPersistenceProcessor      ← domain=Reward, stage=Claim, action=Persistence
RewardClaimNotificationProcessor     ← domain=Reward, stage=Claim, action=Notification
```

All processors in a pipeline share the same `<Domain><Stage>` prefix. An IDE search for `RewardClaim` surfaces the entire chain instantly.

### 5.2 Context Class Names

Pattern: `<Domain><Stage>PipelineContext`

```
RewardClaimPipelineContext
GameRoundResolutionPipelineContext
PlayerDataNormalisationPipelineContext
```

### 5.3 Coordinator Class Names

Pattern: `<Domain><Stage>PipelineCoordinator`

```
RewardClaimPipelineCoordinator
GameRoundResolutionPipelineCoordinator
```

### 5.4 Result Field Names on the Context

Each processor writes its result into a named field on the context that mirrors its class name suffix.

```
context.validationResult
context.playerResolutionResult
context.eligibilityResult
context.calculationResult
context.persistenceResult
context.notificationResult
```

---

## 6. Code Examples

The following examples implement a reward claim pipeline — one of the most common patterns in our codebase. The pipeline processes a player's request to claim a weekly bonus.

### 6.1 PHP (Legacy API Server)

```php
// ─────────────────────────────────────────────────────────────
// Pipeline Context
// ─────────────────────────────────────────────────────────────

class RewardClaimPipelineContext {
    public readonly RewardClaimRequest $originalInput;
    public array $processorResults = [];
    public bool $isComplete = false;
    public bool $partialResultAvailable = false;

    // Intermediate results written by each processor
    public ?ClaimInputValidated $validationResult = null;
    public ?Player $playerResolutionResult = null;
    public ?EligibilityResult $eligibilityResult = null;
    public ?RewardCalculation $calculationResult = null;
    public ?AwardPersisted $persistenceResult = null;

    public function __construct(RewardClaimRequest $input) {
        $this->originalInput = $input;
    }

    public function recordProcessorResult(
        string $processorId,
        string $status,
        ?string $failureReason = null
    ): void {
        $this->processorResults[] = [
            'processorId'   => $processorId,
            'status'        => $status,
            'failureReason' => $failureReason,
        ];
        if ($status === 'SUCCESS') {
            $this->partialResultAvailable = true;
        }
    }
}

// ─────────────────────────────────────────────────────────────
// Processor Interface
// ─────────────────────────────────────────────────────────────

interface RewardClaimProcessor {
    public function process(RewardClaimPipelineContext $context): RewardClaimPipelineContext;
}

// ─────────────────────────────────────────────────────────────
// Processor 1 — Validation (most generic)
// ─────────────────────────────────────────────────────────────

class RewardClaimValidationProcessor implements RewardClaimProcessor {
    public function process(RewardClaimPipelineContext $context): RewardClaimPipelineContext {
        $input = $context->originalInput;

        if (empty($input->playerId) || empty($input->rewardId)) {
            $context->recordProcessorResult(
                'RewardClaimValidationProcessor',
                'FAILED',
                'MISSING_REQUIRED_FIELDS'
            );
            return $context;
        }

        $context->validationResult = new ClaimInputValidated(
            playerId: (int) $input->playerId,
            rewardId: (string) $input->rewardId
        );
        $context->recordProcessorResult('RewardClaimValidationProcessor', 'SUCCESS');
        return $context;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor 2 — Player Resolution
// ─────────────────────────────────────────────────────────────

class RewardClaimPlayerResolutionProcessor implements RewardClaimProcessor {
    public function __construct(private readonly PlayerRepository $playerRepository) {}

    public function process(RewardClaimPipelineContext $context): RewardClaimPipelineContext {
        // Precondition: validation must have succeeded
        if ($context->validationResult === null) {
            $context->recordProcessorResult(
                'RewardClaimPlayerResolutionProcessor',
                'SKIPPED',
                'VALIDATION_NOT_COMPLETE'
            );
            return $context;
        }

        try {
            $player = $this->playerRepository->findById($context->validationResult->playerId);
            $context->playerResolutionResult = $player;
            $context->recordProcessorResult('RewardClaimPlayerResolutionProcessor', 'SUCCESS');
        } catch (PlayerNotFoundException $e) {
            $context->recordProcessorResult(
                'RewardClaimPlayerResolutionProcessor',
                'FAILED',
                'PLAYER_NOT_FOUND'
            );
        }

        return $context;
    }
}

// ─────────────────────────────────────────────────────────────
// Pipeline Coordinator
// ─────────────────────────────────────────────────────────────

class RewardClaimPipelineCoordinator {
    /** @param RewardClaimProcessor[] $processors */
    public function __construct(
        private readonly array $processors,
        private readonly LoggerInterface $logger
    ) {}

    public function execute(RewardClaimRequest $request): RewardClaimPipelineContext {
        $context = new RewardClaimPipelineContext($request);

        foreach ($this->processors as $processor) {
            try {
                $context = $processor->process($context);
            } catch (\Throwable $e) {
                // Processor violated the fail-graceful contract — catch at coordinator level
                $processorId = get_class($processor);
                $this->logger->error('Processor threw unexpectedly — pipeline continues', [
                    'processorId' => $processorId,
                    'error'       => $e->getMessage(),
                    'playerId'    => $request->playerId,
                ]);
                $context->recordProcessorResult($processorId, 'FAILED', 'UNEXPECTED_EXCEPTION');
            }
        }

        $allSucceeded = count(array_filter(
            $context->processorResults,
            fn($r) => $r['status'] === 'FAILED'
        )) === 0;

        $context->isComplete = $allSucceeded;
        return $context;
    }
}

// ─────────────────────────────────────────────────────────────
// Composition Root — wire up the coordinator (e.g., in a DI container
// or service factory called at application bootstrap)
// ─────────────────────────────────────────────────────────────

// $coordinator = new RewardClaimPipelineCoordinator(
//     processors: [
//         // Stage 1: Generic — structural validation
//         new RewardClaimValidationProcessor(),
//         // Stage 2: Domain context resolution
//         new RewardClaimPlayerResolutionProcessor($playerRepository),
//         // Stage 3: Business rule evaluation
//         new RewardClaimEligibilityProcessor($eligibilityService),
//         // Stage 4: Computation
//         new RewardClaimCalculationProcessor($rewardConfig),
//         // Stage 5: Persistence
//         new RewardClaimPersistenceProcessor($awardRepository),
//         // Stage 6: Side effects (last — non-reversible)
//         new RewardClaimNotificationProcessor($notificationService),
//     ],
//     logger: $logger
// );

// ─────────────────────────────────────────────────────────────
// Usage — inside the HTTP boundary function (controller method)
// ─────────────────────────────────────────────────────────────

// $context = $coordinator->execute($request);
//
// if ($context->isComplete) {
//     return Response::ok(buildSuccessPayload($context));
// } elseif ($context->partialResultAvailable) {
//     $this->logger->warning('Reward claim partially processed', buildContextSummary($context));
//     return Response::partialContent(buildPartialPayload($context));
// } else {
//     return Response::internalError('REWARD_CLAIM_PIPELINE_FAILED');
// }
```

### 6.2 Java (New API Server — SEAM Microservice)

```java
// ─────────────────────────────────────────────────────────────
// Pipeline Context
// ─────────────────────────────────────────────────────────────

public class RewardClaimPipelineContext {
    private final RewardClaimRequest originalInput;
    private final List<ProcessorResultRecord> processorResults = new ArrayList<>();
    private boolean isComplete = false;
    private boolean partialResultAvailable = false;

    // Intermediate results — null means not yet produced
    private ClaimInputValidated validationResult;
    private Player playerResolutionResult;
    private EligibilityResult eligibilityResult;
    private RewardCalculation calculationResult;
    private AwardPersisted persistenceResult;

    public RewardClaimPipelineContext(RewardClaimRequest input) {
        this.originalInput = input;
    }

    public void recordProcessorResult(String processorId, ProcessorStatus status, String failureReason) {
        processorResults.add(new ProcessorResultRecord(processorId, status, failureReason));
        if (status == ProcessorStatus.SUCCESS) {
            partialResultAvailable = true;
        }
    }

    // Getters — omitted for brevity
}

// ─────────────────────────────────────────────────────────────
// Processor Interface
// ─────────────────────────────────────────────────────────────

public interface RewardClaimProcessor {
    RewardClaimPipelineContext process(RewardClaimPipelineContext context);
}

// ─────────────────────────────────────────────────────────────
// Processor 1 — Validation (most generic)
// ─────────────────────────────────────────────────────────────

@Component
public class RewardClaimValidationProcessor implements RewardClaimProcessor {

    private static final String PROCESSOR_ID = "RewardClaimValidationProcessor";

    @Override
    public RewardClaimPipelineContext process(RewardClaimPipelineContext context) {
        RewardClaimRequest input = context.getOriginalInput();

        if (input.getPlayerId() == null || input.getRewardId() == null || input.getRewardId().isBlank()) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.FAILED, "MISSING_REQUIRED_FIELDS");
            return context;
        }

        context.setValidationResult(new ClaimInputValidated(input.getPlayerId(), input.getRewardId().trim()));
        context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SUCCESS, null);
        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor 2 — Player Resolution
// ─────────────────────────────────────────────────────────────

@Component
public class RewardClaimPlayerResolutionProcessor implements RewardClaimProcessor {

    private static final String PROCESSOR_ID = "RewardClaimPlayerResolutionProcessor";
    private final PlayerRepository playerRepository;

    public RewardClaimPlayerResolutionProcessor(PlayerRepository playerRepository) {
        this.playerRepository = playerRepository;
    }

    @Override
    public RewardClaimPipelineContext process(RewardClaimPipelineContext context) {
        if (context.getValidationResult() == null) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SKIPPED, "VALIDATION_NOT_COMPLETE");
            return context;
        }

        try {
            Player player = playerRepository.findById(context.getValidationResult().getPlayerId());
            context.setPlayerResolutionResult(player);
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SUCCESS, null);
        } catch (PlayerNotFoundException e) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.FAILED, "PLAYER_NOT_FOUND");
        } catch (DatabaseException e) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.FAILED, "DB_ERROR");
        }

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Pipeline Coordinator
// ─────────────────────────────────────────────────────────────

@Component
public class RewardClaimPipelineCoordinator {

    private final List<RewardClaimProcessor> processors;
    private final Logger logger = LoggerFactory.getLogger(RewardClaimPipelineCoordinator.class);

    // Processors injected in order (DI framework maintains declared order)
    public RewardClaimPipelineCoordinator(List<RewardClaimProcessor> processors) {
        this.processors = processors;
    }

    public RewardClaimPipelineContext execute(RewardClaimRequest request) {
        RewardClaimPipelineContext context = new RewardClaimPipelineContext(request);

        for (RewardClaimProcessor processor : processors) {
            String processorId = processor.getClass().getSimpleName();
            try {
                context = processor.process(context);
            } catch (Exception e) {
                // Processor violated the fail-graceful contract — coordinator safety net
                logger.error("Processor threw unexpectedly — pipeline continues",
                    Map.of(
                        "processorId", processorId,
                        "playerId",    request.getPlayerId(),
                        "error",       e.getMessage()
                    ), e);
                context.recordProcessorResult(processorId, ProcessorStatus.FAILED, "UNEXPECTED_EXCEPTION");
            }
        }

        boolean allSucceeded = context.getProcessorResults().stream()
            .noneMatch(r -> r.getStatus() == ProcessorStatus.FAILED);
        context.setComplete(allSucceeded);

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Composition Root — @Configuration class (Spring-style DI in SEAM)
// Processors are listed in execution order: generic → specific
// ─────────────────────────────────────────────────────────────

// @Configuration
// public class RewardClaimPipelineConfig {
//
//     @Bean
//     public RewardClaimPipelineCoordinator rewardClaimPipelineCoordinator(
//             PlayerRepository playerRepository,
//             EligibilityService eligibilityService,
//             RewardConfig rewardConfig,
//             AwardRepository awardRepository,
//             NotificationService notificationService) {
//
//         List<RewardClaimProcessor> processors = List.of(
//             // Stage 1: Generic — structural validation
//             new RewardClaimValidationProcessor(),
//             // Stage 2: Domain context resolution
//             new RewardClaimPlayerResolutionProcessor(playerRepository),
//             // Stage 3: Business rule evaluation
//             new RewardClaimEligibilityProcessor(eligibilityService),
//             // Stage 4: Computation
//             new RewardClaimCalculationProcessor(rewardConfig),
//             // Stage 5: Persistence
//             new RewardClaimPersistenceProcessor(awardRepository),
//             // Stage 6: Side effects (last — non-reversible)
//             new RewardClaimNotificationProcessor(notificationService)
//         );
//         return new RewardClaimPipelineCoordinator(processors);
//     }
// }

// ─────────────────────────────────────────────────────────────
// Usage — inside the HTTP boundary function (controller method)
// ─────────────────────────────────────────────────────────────

// RewardClaimPipelineContext context = coordinator.execute(request);
//
// if (context.isComplete()) {
//     return Response.ok(buildSuccessPayload(context));
// } else if (context.isPartialResultAvailable()) {
//     logger.warn("Reward claim partially processed", buildContextSummary(context));
//     return Response.partialContent(buildPartialPayload(context));
// } else {
//     return Response.internalError("REWARD_CLAIM_PIPELINE_FAILED");
// }
```

### 6.3 Unity C# (Client)

On the client, the same pattern applies to multi-stage data transformations: for example, processing a server response before applying it to the game state.

```csharp
// ─────────────────────────────────────────────────────────────
// Pipeline Context
// ─────────────────────────────────────────────────────────────

public class BonusClaimPipelineContext
{
    public BonusClaimResponse OriginalInput { get; }
    public List<ProcessorResult> ProcessorResults { get; } = new();
    public bool IsComplete { get; set; } = false;
    public bool PartialResultAvailable { get; set; } = false;

    // Intermediate results
    public BonusResponseValidated ValidationResult { get; set; }
    public PlayerInventorySnapshot InventorySnapshot { get; set; }
    public BonusApplied BonusApplied { get; set; }
    public UiUpdatePayload UiUpdatePayload { get; set; }

    public BonusClaimPipelineContext(BonusClaimResponse input)
    {
        OriginalInput = input;
    }

    public void RecordProcessorResult(string processorId, ProcessorStatus status, string failureReason = null)
    {
        ProcessorResults.Add(new ProcessorResult(processorId, status, failureReason));
        if (status == ProcessorStatus.Success)
            PartialResultAvailable = true;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor Interface
// ─────────────────────────────────────────────────────────────

public interface IBonusClaimProcessor
{
    BonusClaimPipelineContext Process(BonusClaimPipelineContext context);
}

// ─────────────────────────────────────────────────────────────
// Processor 1 — Response Validation (most generic)
// ─────────────────────────────────────────────────────────────

public class BonusClaimResponseValidationProcessor : IBonusClaimProcessor
{
    private const string ProcessorId = nameof(BonusClaimResponseValidationProcessor);

    public BonusClaimPipelineContext Process(BonusClaimPipelineContext context)
    {
        var input = context.OriginalInput;

        if (input == null || input.BonusId == 0 || input.Amount <= 0)
        {
            context.RecordProcessorResult(ProcessorId, ProcessorStatus.Failed, "INVALID_BONUS_RESPONSE");
            return context;
        }

        context.ValidationResult = new BonusResponseValidated(input.BonusId, input.Amount, input.Currency);
        context.RecordProcessorResult(ProcessorId, ProcessorStatus.Success);
        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor 2 — Inventory Snapshot (less generic)
// ─────────────────────────────────────────────────────────────

public class BonusClaimInventorySnapshotProcessor : IBonusClaimProcessor
{
    private const string ProcessorId = nameof(BonusClaimInventorySnapshotProcessor);
    private readonly IPlayerInventoryService _inventoryService;

    public BonusClaimInventorySnapshotProcessor(IPlayerInventoryService inventoryService)
    {
        _inventoryService = inventoryService;
    }

    public BonusClaimPipelineContext Process(BonusClaimPipelineContext context)
    {
        if (context.ValidationResult == null)
        {
            context.RecordProcessorResult(ProcessorId, ProcessorStatus.Skipped, "VALIDATION_NOT_COMPLETE");
            return context;
        }

        try
        {
            context.InventorySnapshot = _inventoryService.GetCurrentSnapshot();
            context.RecordProcessorResult(ProcessorId, ProcessorStatus.Success);
        }
        catch (InventoryUnavailableException ex)
        {
            Logger.Warn($"[BonusClaim] Inventory unavailable: {ex.Message}");
            context.RecordProcessorResult(ProcessorId, ProcessorStatus.Failed, "INVENTORY_UNAVAILABLE");
        }

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Pipeline Coordinator
// ─────────────────────────────────────────────────────────────

public class BonusClaimPipelineCoordinator
{
    private readonly IReadOnlyList<IBonusClaimProcessor> _processors;

    public BonusClaimPipelineCoordinator(IReadOnlyList<IBonusClaimProcessor> processors)
    {
        _processors = processors;
    }

    public BonusClaimPipelineContext Execute(BonusClaimResponse response)
    {
        var context = new BonusClaimPipelineContext(response);

        foreach (var processor in _processors)
        {
            string processorId = processor.GetType().Name;
            try
            {
                context = processor.Process(context);
            }
            catch (Exception ex)
            {
                Logger.Error($"[BonusClaim] Processor {processorId} threw unexpectedly — pipeline continues", ex);
                context.RecordProcessorResult(processorId, ProcessorStatus.Failed, "UNEXPECTED_EXCEPTION");
            }
        }

        bool allSucceeded = context.ProcessorResults
            .TrueForAll(r => r.Status != ProcessorStatus.Failed);
        context.IsComplete = allSucceeded;

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Composition Root — wired in a factory or DI container
// (e.g., a Zenject installer or a hand-rolled ServiceLocator)
// ─────────────────────────────────────────────────────────────

// var coordinator = new BonusClaimPipelineCoordinator(
//     new List<IBonusClaimProcessor>
//     {
//         // Stage 1: Generic — validate the server response shape
//         new BonusClaimResponseValidationProcessor(),
//         // Stage 2: Snapshot the current inventory before applying changes
//         new BonusClaimInventorySnapshotProcessor(inventoryService),
//         // Stage 3: Apply the bonus to the local game state
//         new BonusClaimApplicationProcessor(gameStateService),
//         // Stage 4: Build the UI update payload (most specific — presentation only)
//         new BonusClaimUiPayloadProcessor(),
//     }
// );

// ─────────────────────────────────────────────────────────────
// Usage — inside the API response handler (client boundary function)
// ─────────────────────────────────────────────────────────────

// var context = coordinator.Execute(serverResponse);
//
// if (context.IsComplete)
// {
//     _uiController.ApplyBonusUpdate(context.UiUpdatePayload);
// }
// else if (context.PartialResultAvailable)
// {
//     Logger.Warn($"[BonusClaim] Partial result — some stages failed. See processor results.");
//     // Show safe degraded state: e.g., refresh inventory from server
//     _inventoryService.RequestFullRefresh();
// }
// else
// {
//     Logger.Error("[BonusClaim] Pipeline failed entirely. No partial result available.");
//     ShowErrorToast("Could not apply bonus. Please restart.");
// }
```

### 6.4 TypeScript / NextJS (Internal Tools)

```typescript
// ─────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────

export type ProcessorStatus = 'SUCCESS' | 'SKIPPED' | 'FAILED' | 'NOT_APPLICABLE';

export interface ProcessorResult {
    processorId: string;
    status: ProcessorStatus;
    failureReason?: string;
}

// ─────────────────────────────────────────────────────────────
// Pipeline Context
// ─────────────────────────────────────────────────────────────

export class PlayerReportPipelineContext {
    readonly originalInput: PlayerReportRequest;
    readonly processorResults: ProcessorResult[] = [];
    isComplete = false;
    partialResultAvailable = false;

    // Intermediate results
    validationResult: ReportParamsValidated | null = null;
    playerDataResult: PlayerDataSnapshot | null = null;
    rewardHistoryResult: RewardHistoryRecord[] | null = null;
    reportFormattedResult: ReportFormatted | null = null;

    constructor(input: PlayerReportRequest) {
        this.originalInput = input;
    }

    recordProcessorResult(processorId: string, status: ProcessorStatus, failureReason?: string): void {
        this.processorResults.push({ processorId, status, failureReason });
        if (status === 'SUCCESS') {
            this.partialResultAvailable = true;
        }
    }
}

// ─────────────────────────────────────────────────────────────
// Processor Interface
// ─────────────────────────────────────────────────────────────

export interface PlayerReportProcessor {
    process(context: PlayerReportPipelineContext): Promise<PlayerReportPipelineContext>;
}

// ─────────────────────────────────────────────────────────────
// Processor 1 — Validation (most generic)
// ─────────────────────────────────────────────────────────────

export class PlayerReportValidationProcessor implements PlayerReportProcessor {
    private static readonly PROCESSOR_ID = 'PlayerReportValidationProcessor';

    async process(context: PlayerReportPipelineContext): Promise<PlayerReportPipelineContext> {
        const { playerId, reportType, dateRangeStart, dateRangeEnd } = context.originalInput;

        if (!playerId || !reportType || !dateRangeStart || !dateRangeEnd) {
            context.recordProcessorResult(
                PlayerReportValidationProcessor.PROCESSOR_ID,
                'FAILED',
                'MISSING_REQUIRED_FIELDS'
            );
            return context;
        }

        if (new Date(dateRangeEnd) < new Date(dateRangeStart)) {
            context.recordProcessorResult(
                PlayerReportValidationProcessor.PROCESSOR_ID,
                'FAILED',
                'INVALID_DATE_RANGE'
            );
            return context;
        }

        context.validationResult = {
            playerId: Number(playerId),
            reportType,
            dateRangeStart: new Date(dateRangeStart),
            dateRangeEnd:   new Date(dateRangeEnd),
        };
        context.recordProcessorResult(PlayerReportValidationProcessor.PROCESSOR_ID, 'SUCCESS');
        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor 2 — Player Data Fetch (less generic)
// ─────────────────────────────────────────────────────────────

export class PlayerReportPlayerDataProcessor implements PlayerReportProcessor {
    private static readonly PROCESSOR_ID = 'PlayerReportPlayerDataProcessor';

    constructor(private readonly playerService: PlayerService) {}

    async process(context: PlayerReportPipelineContext): Promise<PlayerReportPipelineContext> {
        if (!context.validationResult) {
            context.recordProcessorResult(
                PlayerReportPlayerDataProcessor.PROCESSOR_ID,
                'SKIPPED',
                'VALIDATION_NOT_COMPLETE'
            );
            return context;
        }

        try {
            context.playerDataResult = await this.playerService.getSnapshot(
                context.validationResult.playerId
            );
            context.recordProcessorResult(PlayerReportPlayerDataProcessor.PROCESSOR_ID, 'SUCCESS');
        } catch (error) {
            context.recordProcessorResult(
                PlayerReportPlayerDataProcessor.PROCESSOR_ID,
                'FAILED',
                error instanceof PlayerNotFoundError ? 'PLAYER_NOT_FOUND' : 'PLAYER_FETCH_ERROR'
            );
        }

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Pipeline Coordinator
// ─────────────────────────────────────────────────────────────

export class PlayerReportPipelineCoordinator {
    constructor(
        private readonly processors: PlayerReportProcessor[],
        private readonly logger: Logger
    ) {}

    async execute(request: PlayerReportRequest): Promise<PlayerReportPipelineContext> {
        const context = new PlayerReportPipelineContext(request);

        for (const processor of this.processors) {
            const processorId = processor.constructor.name;
            try {
                await processor.process(context);
            } catch (error) {
                this.logger.error('Processor threw unexpectedly — pipeline continues', {
                    processorId,
                    playerId: request.playerId,
                    error:    error instanceof Error ? error.message : String(error),
                });
                context.recordProcessorResult(processorId, 'FAILED', 'UNEXPECTED_EXCEPTION');
            }
        }

        const allSucceeded = context.processorResults.every(r => r.status !== 'FAILED');
        context.isComplete = allSucceeded;

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Composition Root — wired in a NestJS module provider or
// a plain factory function (e.g., in api/reports/pipeline.ts)
// ─────────────────────────────────────────────────────────────

// export function createPlayerReportCoordinator(
//     playerService: PlayerService,
//     rewardHistoryService: RewardHistoryService,
//     reportFormatter: ReportFormatter,
//     logger: Logger
// ): PlayerReportPipelineCoordinator {
//     return new PlayerReportPipelineCoordinator(
//         [
//             // Stage 1: Generic — validate and parse the request parameters
//             new PlayerReportValidationProcessor(),
//             // Stage 2: Fetch the player's base data
//             new PlayerReportPlayerDataProcessor(playerService),
//             // Stage 3: Fetch reward history within the date range
//             new PlayerReportRewardHistoryProcessor(rewardHistoryService),
//             // Stage 4: Format the final report (most specific — presentation only)
//             new PlayerReportFormattingProcessor(reportFormatter),
//         ],
//         logger
//     );
// }

// ─────────────────────────────────────────────────────────────
// Usage — inside the API route handler (Next.js / NestJS boundary)
// ─────────────────────────────────────────────────────────────

// const context = await coordinator.execute(request);
//
// if (context.isComplete) {
//     return res.status(200).json(buildSuccessPayload(context));
// } else if (context.partialResultAvailable) {
//     logger.warn('Player report partially generated', buildContextSummary(context));
//     return res.status(206).json(buildPartialPayload(context));
// } else {
//     return res.status(500).json({ error: 'PLAYER_REPORT_PIPELINE_FAILED' });
// }
```

### 6.5 Java (SmartFox Extension Handler)

SmartFox extension handlers are entry-point boundaries (per [ESTD12 §4. Extension Structure and Handler Pattern](./ESTD12_-_Smartfox_Server_Standards.md#4-extension-structure-and-handler-pattern)). Once the handler has authenticated the user and parsed the raw `ISFSObject` into a typed domain request (per [ESTD12 §5.1 Parse at the Boundary, Use Domain Types Everywhere Else](./ESTD12_-_Smartfox_Server_Standards.md#51-parse-at-the-boundary-use-domain-types-everywhere-else)), the Waterfall Processing Pattern is the correct structure for the multi-stage logic that follows.

The pattern fits naturally because a Bingo claim, a daub validation, or a room join each has the same generic-to-specific shape:

```
1. Validate the SFSObject message       ← Generic: is the message well-formed?
2. Snapshot the room state              ← Less generic: what is the current game state?
3. Evaluate locally                     ← Specific: is the action valid in this state?
4. Confirm via authoritative API        ← More specific: record the result (I/O, outside locks)
5. Build the broadcast payload          ← Most specific: prepare the response for the room
```

The handler itself remains the boundary function: it parses the `ISFSObject`, delegates to the coordinator, and broadcasts the result. All multi-stage logic lives in processors.

```java
// ─────────────────────────────────────────────────────────────
// Pipeline Context
// ─────────────────────────────────────────────────────────────

public class BingoClaimPipelineContext {
    private final BingoClaimRequest originalInput;
    private final User claimant;
    private final Room room;

    private final List<ProcessorResultRecord> processorResults = new ArrayList<>();
    private boolean isComplete = false;
    private boolean partialResultAvailable = false;

    // Intermediate results
    private BingoClaimValidation  validationResult;
    private GameRoomSnapshot      roomSnapshotResult;
    private BingoClaimEvaluation  claimEvaluationResult;
    private ApiValidationOutcome  apiValidationResult;
    private BroadcastPayload      broadcastPayloadResult;

    public BingoClaimPipelineContext(BingoClaimRequest input, User claimant, Room room) {
        this.originalInput = input;
        this.claimant      = claimant;
        this.room          = room;
    }

    public void recordProcessorResult(String processorId, ProcessorStatus status, String failureReason) {
        processorResults.add(new ProcessorResultRecord(processorId, status, failureReason));
        if (status == ProcessorStatus.SUCCESS) {
            partialResultAvailable = true;
        }
    }

    // Getters — omitted for brevity
}

// ─────────────────────────────────────────────────────────────
// Processor Interface
// ─────────────────────────────────────────────────────────────

public interface BingoClaimProcessor {
    BingoClaimPipelineContext process(BingoClaimPipelineContext context);
}

// ─────────────────────────────────────────────────────────────
// Processor 1 — Claim Validation (most generic)
// Verifies that the claim message is structurally sound and
// that the claimed pattern is a recognised type.
// ─────────────────────────────────────────────────────────────

public class BingoClaimValidationProcessor implements BingoClaimProcessor {

    private static final String PROCESSOR_ID = "BingoClaimValidationProcessor";

    @Override
    public BingoClaimPipelineContext process(BingoClaimPipelineContext context) {
        BingoClaimRequest input = context.getOriginalInput();

        if (input.getCardId() <= 0 || input.getClaimedPattern() == null) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.FAILED, "INVALID_CLAIM_PARAMS");
            return context;
        }

        context.setValidationResult(new BingoClaimValidation(input.getCardId(), input.getClaimedPattern()));
        context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SUCCESS, null);
        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor 2 — Room Snapshot (less generic)
// Captures authoritative in-memory room state under a lock so
// all subsequent processors work from a consistent snapshot.
// ─────────────────────────────────────────────────────────────

public class BingoClaimRoomSnapshotProcessor implements BingoClaimProcessor {

    private static final String PROCESSOR_ID = "BingoClaimRoomSnapshotProcessor";
    private final BingoGameEngine gameEngine;

    public BingoClaimRoomSnapshotProcessor(BingoGameEngine gameEngine) {
        this.gameEngine = gameEngine;
    }

    @Override
    public BingoClaimPipelineContext process(BingoClaimPipelineContext context) {
        if (context.getValidationResult() == null) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SKIPPED, "VALIDATION_NOT_COMPLETE");
            return context;
        }

        try {
            GameRoomSnapshot snapshot = gameEngine.snapshotRoom(context.getRoom());
            context.setRoomSnapshotResult(snapshot);
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SUCCESS, null);
        } catch (RoomNotFoundException e) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.FAILED, "ROOM_NOT_FOUND");
        }

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor 3 — Local Claim Evaluation (specific)
// Evaluates whether the claimed pattern is genuinely present
// on the card using only in-memory state. No I/O — fast.
// ─────────────────────────────────────────────────────────────

public class BingoClaimEvaluationProcessor implements BingoClaimProcessor {

    private static final String PROCESSOR_ID = "BingoClaimEvaluationProcessor";
    private final WinPatternChecker winChecker;

    public BingoClaimEvaluationProcessor(WinPatternChecker winChecker) {
        this.winChecker = winChecker;
    }

    @Override
    public BingoClaimPipelineContext process(BingoClaimPipelineContext context) {
        if (context.getRoomSnapshotResult() == null) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SKIPPED, "ROOM_SNAPSHOT_NOT_AVAILABLE");
            return context;
        }

        GameRoomSnapshot snapshot  = context.getRoomSnapshotResult();
        BingoClaimValidation claim = context.getValidationResult();

        boolean locallyValid = winChecker.check(
            snapshot.getDaubedPositions(context.getClaimant().getId(), claim.getCardId()),
            claim.getClaimedPattern(),
            snapshot.getCalledNumbers()
        );

        if (!locallyValid) {
            context.setClaimEvaluationResult(BingoClaimEvaluation.invalid("PATTERN_NOT_PRESENT"));
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.FAILED, "INVALID_CLAIM");
            return context;
        }

        context.setClaimEvaluationResult(BingoClaimEvaluation.valid());
        context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SUCCESS, null);
        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor 4 — Authoritative API Validation (more specific)
// Calls the PHP / SEAM API to confirm the win and award coins.
// I/O happens here, OUTSIDE any room lock (per ESTD12 §7.2).
// ─────────────────────────────────────────────────────────────

public class BingoClaimApiValidationProcessor implements BingoClaimProcessor {

    private static final String PROCESSOR_ID = "BingoClaimApiValidationProcessor";
    private final GameApiClient gameApiClient;

    public BingoClaimApiValidationProcessor(GameApiClient gameApiClient) {
        this.gameApiClient = gameApiClient;
    }

    @Override
    public BingoClaimPipelineContext process(BingoClaimPipelineContext context) {
        if (context.getClaimEvaluationResult() == null || !context.getClaimEvaluationResult().isValid()) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SKIPPED, "LOCAL_EVALUATION_FAILED");
            return context;
        }

        try {
            ApiValidationOutcome outcome = gameApiClient.validateBingoClaim(
                context.getClaimant().getId(),
                context.getRoom().getId(),
                context.getValidationResult().getCardId(),
                context.getValidationResult().getClaimedPattern()
            );
            context.setApiValidationResult(outcome);
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SUCCESS, null);
        } catch (ApiTimeoutException e) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.FAILED, "API_TIMEOUT");
        } catch (ApiException e) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.FAILED, "API_ERROR");
        }

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Processor 5 — Broadcast Payload Builder (most specific)
// Assembles the ISFSObject payload for the room broadcast.
// Pure transformation — no I/O, no side effects.
// ─────────────────────────────────────────────────────────────

public class BingoClaimBroadcastPayloadProcessor implements BingoClaimProcessor {

    private static final String PROCESSOR_ID = "BingoClaimBroadcastPayloadProcessor";

    @Override
    public BingoClaimPipelineContext process(BingoClaimPipelineContext context) {
        if (context.getApiValidationResult() == null) {
            context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SKIPPED, "API_VALIDATION_NOT_COMPLETE");
            return context;
        }

        ApiValidationOutcome outcome = context.getApiValidationResult();
        ISFSObject payload = new SFSObject();
        payload.putBool("winConfirmed",  outcome.isConfirmed());
        payload.putInt("userId",         context.getClaimant().getId());
        payload.putUtfString("pattern",  context.getValidationResult().getClaimedPattern().name());
        payload.putLong("coinsAwarded",  outcome.getCoinsAwarded());
        payload.putInt("serverSeq",      context.getRoomSnapshotResult().getNextSequenceId());

        context.setBroadcastPayloadResult(new BroadcastPayload(payload));
        context.recordProcessorResult(PROCESSOR_ID, ProcessorStatus.SUCCESS, null);
        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Pipeline Coordinator
// ─────────────────────────────────────────────────────────────

public class BingoClaimPipelineCoordinator {

    private final List<BingoClaimProcessor> processors;
    private final Logger logger = LoggerFactory.getLogger(BingoClaimPipelineCoordinator.class);

    public BingoClaimPipelineCoordinator(List<BingoClaimProcessor> processors) {
        this.processors = processors;
    }

    public BingoClaimPipelineContext execute(BingoClaimRequest request, User claimant, Room room) {
        BingoClaimPipelineContext context = new BingoClaimPipelineContext(request, claimant, room);

        for (BingoClaimProcessor processor : processors) {
            String processorId = processor.getClass().getSimpleName();
            try {
                context = processor.process(context);
            } catch (Exception e) {
                logger.error("BingoClaim processor threw unexpectedly — pipeline continues",
                    Map.of("processorId", processorId, "userId", claimant.getId(),
                           "roomId", room.getId(), "error", e.getMessage()), e);
                context.recordProcessorResult(processorId, ProcessorStatus.FAILED, "UNEXPECTED_EXCEPTION");
            }
        }

        boolean allSucceeded = context.getProcessorResults().stream()
            .noneMatch(r -> r.getStatus() == ProcessorStatus.FAILED);
        context.setComplete(allSucceeded);

        return context;
    }
}

// ─────────────────────────────────────────────────────────────
// Composition Root — registered in extension init()
// ─────────────────────────────────────────────────────────────

// BingoClaimPipelineCoordinator claimCoordinator = new BingoClaimPipelineCoordinator(List.of(
//     // Stage 1: Generic — validate the claim message shape
//     new BingoClaimValidationProcessor(),
//     // Stage 2: Capture consistent room snapshot
//     new BingoClaimRoomSnapshotProcessor(gameEngine),
//     // Stage 3: Evaluate win locally (no I/O)
//     new BingoClaimEvaluationProcessor(winPatternChecker),
//     // Stage 4: Confirm with authoritative API (I/O — outside all locks)
//     new BingoClaimApiValidationProcessor(gameApiClient),
//     // Stage 5: Build broadcast payload (pure transformation)
//     new BingoClaimBroadcastPayloadProcessor()
// ));

// ─────────────────────────────────────────────────────────────
// Usage — inside the SmartFox handler (entry-point boundary)
// The handler parses the ISFSObject, delegates to the pipeline,
// then broadcasts based on the context result.
// ─────────────────────────────────────────────────────────────

// public class ClaimBingoHandler implements IClientRequestHandler {
//
//     @Override
//     public void handleRequest(User user, ISFSObject params, Room room) {
//         BingoClaimRequest request;
//         try {
//             request = BingoClaimRequest.fromSfsObject(params);
//             request.validate();
//         } catch (RequestInvalidException ex) {
//             sendError(user, ErrorCode.INVALID_PARAMS, ex.getMessage());
//             return;
//         }
//
//         BingoClaimPipelineContext context = claimCoordinator.execute(request, user, room);
//
//         if (context.isComplete()) {
//             // Broadcast confirmed result to the whole room
//             getParentExtension().getApi().sendObjectMessage(
//                 room, context.getBroadcastPayloadResult().toSfsObject(), null
//             );
//         } else {
//             // Send a structured error back to the claiming player only
//             String failureReason = context.getProcessorResults().stream()
//                 .filter(r -> r.getStatus() == ProcessorStatus.FAILED)
//                 .findFirst()
//                 .map(ProcessorResultRecord::getFailureReason)
//                 .orElse("UNKNOWN_ERROR");
//             sendError(user, ErrorCode.CLAIM_FAILED, failureReason);
//         }
//     }
// }
```

---

## 7. Design Rules

### 7.1 Ordering Rule: Generic Before Specific

Processors must be ordered from the most generic concern to the most specific. A processor that produces output that another processor depends upon must come first in the chain. Violating this rule causes processors to find their preconditions unmet and skip unnecessarily.

The correct test for ordering: if Processor B reads from a field that Processor A writes, then A must precede B.

### 7.2 Precondition Checks Are Mandatory

Every processor that depends on the output of a prior processor must explicitly check that output's presence at the start of its `process` method. A null check is the minimum; a status check (`processorResult == SUCCESS`) is preferred for precision.

**Do:** Check that `context.validationResult != null` before using it.

**Do not:** Assume that because Processor 1 is listed first, its output will always be populated. It may have failed. You must check.

### 7.3 Processors Must Not Call Other Processors

A processor must not invoke another processor directly. All cross-processor communication flows through the context object. Direct inter-processor calls create hidden dependencies that break the independence of processors, making the chain unpredictable and harder to test.

### 7.4 Processors Must Not Modify Prior Results

A processor must not overwrite the output that a prior processor wrote to the context. It may read prior results as inputs. It may add new fields to the context. It must not replace existing populated fields.

Exception: a processor explicitly designed to **correct** or **normalise** a prior result (e.g., a data sanitisation processor that follows a parsing processor) may do so, and this role must be documented in the processor's class-level comment.

### 7.5 The Pipeline Always Returns the Context

The coordinator must always return the final context to the caller, even if every processor failed. The caller decides what to do with a failed or partial context. The coordinator does not hide failures by returning null or throwing.

### 7.6 Partial Results Are Valuable

A partially populated context is not an error state — it is meaningful information. The caller must handle partial results deliberately. In a server boundary function (per [ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions)), this means inspecting the context's processor results and constructing a structured response that accurately reflects what succeeded, what was skipped, and what failed.

```
// GOOD — caller inspects partial result
RewardClaimPipelineContext result = coordinator.execute(request);

if (result.isComplete()) {
    return Response.ok(buildSuccessPayload(result));
} else if (result.isPartialResultAvailable()) {
    // Log for diagnostics; return partial response with clear error indication
    logger.warn("Reward claim partially processed", buildContextSummary(result));
    return Response.partialContent(buildPartialPayload(result));
} else {
    return Response.internalError("REWARD_CLAIM_PIPELINE_FAILED");
}

// BAD — caller ignores partial result, treats everything as all-or-nothing
RewardClaimPipelineContext result = coordinator.execute(request);
if (!result.isComplete()) {
    return Response.internalError("FAILED"); // throws away useful partial context
}
```

### 7.7 Processor Registration Order Is the Authoritative Declaration

The order in which processors are registered with the coordinator is the single authoritative declaration of pipeline execution order. It must be readable and must be documented with a comment block in the composition root (the DI wiring or factory method where processors are assembled).

```java
// GOOD — composition root makes the pipeline order legible
List<RewardClaimProcessor> processors = List.of(
    // Stage 1: Generic — structural validation
    new RewardClaimValidationProcessor(),
    // Stage 2: Domain context resolution
    new RewardClaimPlayerResolutionProcessor(playerRepository),
    // Stage 3: Business rule evaluation
    new RewardClaimEligibilityProcessor(eligibilityService),
    // Stage 4: Computation
    new RewardClaimCalculationProcessor(rewardConfig),
    // Stage 5: Persistence
    new RewardClaimPersistenceProcessor(awardRepository),
    // Stage 6: Side effects (last, because they are non-reversible)
    new RewardClaimNotificationProcessor(notificationService)
);
```

---

## 8. Testing Requirements

The Waterfall Processing Pattern is designed for testability. Each processor is an independent unit with a clearly defined input (context in a known state) and output (context in an enriched state). This makes unit testing straightforward.

### 8.1 Test Each Processor in Isolation

Do not test a processor by running the full pipeline. Test each processor by:

1. Creating a context in the exact state the processor expects to receive.
2. Calling `process()` directly on the processor.
3. Asserting the processor's specific contribution to the context.
4. Asserting the correct `ProcessorResult` record was appended.

### 8.2 Required Test Cases Per Processor

For each processor, write tests for:

| Scenario | What to Assert |
| :------- | :------------- |
| Happy path — preconditions met, success | Output field populated; `ProcessorResult.status = SUCCESS` |
| Precondition not met — prior result is null | Output field remains null; `ProcessorResult.status = SKIPPED` |
| Internal failure (e.g., DB throws) | Output field remains null; `ProcessorResult.status = FAILED`; failure reason set |
| Boundary values on inputs | Correct behaviour at min, max, and just-outside-range values |

### 8.3 Test the Coordinator's Safety Net

Write one test that exercises the coordinator's handling of a processor that throws unexpectedly (i.e., violates the fail-graceful contract). The coordinator must:

- Not propagate the exception to the test.
- Record the throwing processor as `FAILED`.
- Continue running subsequent processors.
- Return the context at the end.

### 8.4 Test the Assembled Pipeline for Integration Confidence

After unit-testing each processor in isolation, write one integration test that runs the full pipeline with mocked dependencies. This test verifies that the composition root registered processors in the correct order and that the context flows correctly end-to-end.

---

## 9. Relationship to Other Patterns and Standards

### 9.1 Relationship to Boundary Functions

The pipeline coordinator is itself a service-layer component, not a boundary function. Boundary functions (per [ESTD1 §10. Boundary Functions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions)) delegate to the coordinator. The coordinator's result is what the boundary function uses to construct its response.

```
HTTP Request
     │
     ▼
[Boundary Function]     ← authenticate, authorise, validate HTTP layer, delegate
     │
     ▼
[PipelineCoordinator]   ← execute processor chain, return context
     │
     ▼
[Boundary Function]     ← inspect context, construct and return HTTP response
```

### 9.2 Relationship to Error Handling Standards

The Waterfall pattern extends the error handling principles in [ESTD1 §9. Error Handling and Try-Catch Usage](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#9-error-handling-and-try-catch-usage):

- Each processor's internal try-catch follows the "catch the most specific exception" rule ([ESTD1 §9.4 Catch the Most Specific Exception](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#94-catch-the-most-specific-exception)).
- The coordinator's outer catch is the one permitted use of a broad `catch (Exception e)` outside a boundary function — because the coordinator is the pipeline's boundary.
- Processors must never swallow exceptions silently. Every caught exception must result in a recorded `FAILED` status in the context, which is the processor equivalent of structured error logging.

### 9.3 Relationship to the Naming Strategy

All processor, context, and coordinator names must follow [ESTD14](./ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md#estd14---hierarchical-naming-strategy-for-programming-entities). The hierarchical naming ensures that all processors in a pipeline group together alphabetically and in IDE autocomplete, making the pipeline structure discoverable without reading the composition root.

---

## 10. Anti-Patterns to Avoid

| Anti-Pattern | Problem | Correct Approach |
| :----------- | :------ | :--------------- |
| **God processor** — one processor that does everything | Defeats the purpose of the pattern; untestable; blast radius of a failure is the entire operation | Split into one processor per concern, generic to specific |
| **Processor calling processor** — P2 directly invokes P3 | Creates hidden ordering dependencies; breaks independence and testability | All inter-processor communication must flow through the context |
| **Throwing from a processor** — unhandled exception escapes `process()` | Terminates the pipeline early; prior partial results are lost if coordinator does not catch | Processors must catch all exceptions internally and record `FAILED` status |
| **Overwriting prior results** — P3 replaces P1's output | Destroys partial result history; P1's contribution is unrecoverable, except in a case where P3 is specifically written to overwrite/enrich P1's output | Each processor writes to its own dedicated context field only |
| **Coordinator contains business logic** — eligibility check inside `execute()` | The coordinator becomes a god class; testability collapses | Business logic belongs only in processors |
| **Ignoring partial results in caller** — treating non-`isComplete` as total failure | Partial results carry diagnostic value; discarding them produces worse error messages | Always inspect `processorResults` and construct a structured response |
| **Registering processors in wrong order** — specific before generic | Downstream processors find their preconditions unmet and skip unnecessarily | Register processors generic-first; document the composition root order with comments |
| **Context as a property bag with no structure** — using a generic `Map<String, Object>` | Type safety lost; errors are detected at runtime, not compile time | Use a typed context class with named, typed fields for each processor's result |

---

## 11. Quick Reference Checklist

Use this checklist when designing or reviewing a Waterfall pipeline implementation.

**Pipeline Design**

- [ ] Each processor has a single, clearly named responsibility — no "and" in the description
- [ ] Processors are ordered from most generic to most specific
- [ ] Each processor writes to a dedicated, typed field on the context
- [ ] No processor calls another processor directly
- [ ] The coordinator is free of business logic

**Context Design**

- [ ] `originalInput` is immutable after construction
- [ ] Each processor result is individually recorded with processor ID, status, and failure reason
- [ ] `isComplete` and `partialResultAvailable` are computed and populated at coordinator level
- [ ] Context fields are typed (not a generic map)

**Error Handling**

- [ ] Each processor catches its own exceptions and records `FAILED` — no uncaught throws
- [ ] The coordinator has a safety-net catch that continues the pipeline on processor contract violations
- [ ] Partial results are handled by the caller — not treated as total failures

**Naming**

- [ ] Processor classes follow `<Domain><Stage><Action>Processor` pattern
- [ ] Context class follows `<Domain><Stage>PipelineContext` pattern
- [ ] Coordinator class follows `<Domain><Stage>PipelineCoordinator` pattern
- [ ] All names are consistent with [ESTD14](./ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md#estd14---hierarchical-naming-strategy-for-programming-entities)

**Testing**

- [ ] Each processor tested in isolation for happy path, skipped path, failed path, and boundary values
- [ ] Coordinator tested for safety-net behaviour (processor that throws unexpectedly)
- [ ] One integration test for the assembled pipeline end-to-end

---

## 12. When to Use This Pattern — and When Not To

Patterns are tools, not rules. The Waterfall Processing Pattern solves a specific set of problems well. Applied outside that context it adds complexity with no benefit. The guidance below is intended to help engineers make that judgment call.

### 12.1 When to Use

Apply this pattern when **all three** of the following are true:

1. **The operation has three or more discrete stages** that transform the same data progressively. Two stages are usually better handled with a plain service call; three or more are the threshold where the added structure pays for itself.

2. **A partial result has value to the caller.** If the caller can do something useful with whatever the first two processors produced — log a better error, retry a specific stage, return a structured partial response — the pattern is worth it. If the only acceptable outcome is full success (e.g., a database transaction that must be all-or-nothing), the pattern's partial-result machinery adds unnecessary complexity.

3. **At least one stage may fail independently without making the entire operation meaningless.** A player resolution failure should not prevent a validation result from being returned. If every stage depends irreversibly on every prior stage such that any failure makes all prior work worthless, the partial-result benefit disappears.

**Situations where this pattern fits well in our codebase:**

| Situation | Why it fits |
| :-------- | :---------- |
| Reward claim processing (validate → resolve player → check eligibility → calculate → persist → notify) | Each stage is independent; partial results are diagnostically useful; individual stages can be retried |
| Game state resolution on reconnect (parse snapshot → resolve room → validate sequence → apply deltas → rebuild UI state) | Mid-chain failure (e.g., stale snapshot) still allows partial state recovery |
| Player report generation (validate params → fetch player data → fetch reward history → format report) | Partial reports (e.g., player data without reward history) are better than no report |
| SmartFox Bingo claim handling (validate → snapshot room → evaluate locally → confirm via API → build broadcast payload) | The local evaluation result remains useful even if the API call times out |
| Configuration loading pipeline (fetch remote config → merge defaults → validate schema → apply feature flags) | Fallback to previous valid configuration is possible at any stage |

### 12.2 When Not to Use

Do not apply this pattern when any of the following is true:

| Situation | Why it does not fit | Better approach |
| :-------- | :------------------ | :-------------- |
| **The operation has only one or two stages** | The context, interface, and coordinator infrastructure cost more than two plain function calls | A direct service method or a simple two-step function |
| **The operation is a strict atomic transaction** | A partial result from a half-completed DB transaction is invalid, not useful | A service method wrapped in a DB transaction with rollback on failure |
| **All stages depend on each other serially with no partial value** | If P2's failure makes P1's output meaningless, there is nothing to preserve | Chain service calls directly; throw on failure |
| **The chain is a one-off with no variation** | A pipeline built once, never reused, and never extended carries overhead without benefit | A single well-named function with clearly separated concerns |
| **Real-time hot path** (e.g., per-ball-draw broadcast, per-daub loop) | Context allocation, processor iteration, and result recording add measurable overhead per invocation at high frequency | Optimised, inlined logic tuned for throughput; profile before introducing the pattern here. Object pooling can help if the pattern is well suited otherwise |
| **The stages are event-driven or asynchronous fan-out** | The Waterfall pattern is linear and synchronous; event-driven fan-out requires a different topology | Message queues, event bus, or streaming pipeline (see [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management)) |

### 12.3 The Decision Heuristic

```
Is the operation linear (not fan-out / branching into independent parallel streams)?
│
├── NO  → Use an event bus or message queue, not this pattern.
│
└── YES → Does it have 3+ discrete stages?
          │
          ├── NO  → Use a plain service method.
          │
          └── YES → Is a partial result useful to the caller?
                    │
                    ├── NO  → Use a transactional service method with rollback.
                    │
                    └── YES → Apply the Waterfall Processing Pattern.
```
