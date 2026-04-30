# ESTD15 — Technical Document Guide and Template

**ESTD15 — Technical Document Guide and Template**

| Field | Value |
|:------|:----|
| **Document ID** | ESTD15 |
| **Version** | 1.2 |
| **Status** | Active |
| **Last Updated** | 2026-04-30 |
| **Applies To** | All engineers writing technical documents |
| **Depends On** | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) |
| **Approval** | Director of Engineering |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD15 governs all technical documents produced by the Bingo Bash engineering team — Technical Approach Documents, architecture decisions, runbooks, post-mortems (RCAs), and migration plans. It does **not** cover ESTD standard documents themselves; those follow [ESTD0](./ESTD0_-_Markdown_format.md#estd-document-heading) (the ESTD markdown template) and the workflow in [AGENTS.md](./AGENTS.md).

Read [§2](#2-when-to-write-a-technical-document) first to decide whether a document is necessary. Then pick the appropriate document type from [§3](#3-document-types) and copy the corresponding template from [§8](#8-templates).

---

## Table of Contents

- [ESTD15 — Technical Document Guide and Template](#estd15--technical-document-guide-and-template)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. When to Write a Technical Document](#2-when-to-write-a-technical-document)
  - [3. Document Types](#3-document-types)
    - [3.1 Technical Approach Document (TAD)](#31-technical-approach-document-tad)
    - [3.2 Architecture Decision Record (ADR)](#32-architecture-decision-record-adr)
    - [3.3 Runbook](#33-runbook)
    - [3.4 Post-mortem or Root Cause Analysis (RCA)](#34-post-mortem-or-root-cause-analysis-rca)
    - [3.5 Migration Plan](#35-migration-plan)
  - [4. Document Lifecycle](#4-document-lifecycle)
  - [5. Common Document Structure](#5-common-document-structure)
    - [5.1 Title and Metadata](#51-title-and-metadata)
    - [5.2 Summary (TL;DR)](#52-summary-tldr)
    - [5.3 Context and Problem Statement](#53-context-and-problem-statement)
    - [5.4 Goals and Non-Goals](#54-goals-and-non-goals)
    - [5.5 Main Body](#55-main-body)
    - [5.6 Risks and Mitigations](#56-risks-and-mitigations)
    - [5.7 Open Questions](#57-open-questions)
    - [5.8 References](#58-references)
  - [6. Writing Style](#6-writing-style)
    - [6.1 Be Concrete](#61-be-concrete)
    - [6.2 Diagrams Over Prose](#62-diagrams-over-prose)
    - [6.3 Length Discipline](#63-length-discipline)
    - [6.4 What to Avoid](#64-what-to-avoid)
  - [7. Review and Approval](#7-review-and-approval)
    - [7.1 Required Reviewers by Document Type](#71-required-reviewers-by-document-type)
    - [7.2 Review Process](#72-review-process)
  - [8. Templates](#8-templates)
    - [8.1 Technical Approach Document (TAD)](#81-technical-approach-document-tad)
    - [8.2 Architecture Decision Record (ADR)](#82-architecture-decision-record-adr)
    - [8.3 Runbook](#83-runbook)
    - [8.4 Post-mortem or RCA](#84-post-mortem-or-rca)
    - [8.5 Migration Plan](#85-migration-plan)

---

## 1. Purpose and Scope

Undocumented decisions become tribal knowledge — locked in the heads of the engineers who made them. When those engineers move on, or when a decision needs to be revisited six months later, that knowledge is gone. Technical documents create a permanent, searchable record of what was built, why, and how.

This document defines:
- When a technical document is required vs. when it is overkill.
- The five document types used by the Bingo Bash team.
- The structure, style, lifecycle, and review process for each.
- Copy-paste-ready templates for each type.

**This document applies to:**
- All engineers writing Technical Approach Documents, architecture decisions, operational runbooks, incident post-mortems, or migration plans for either the legacy Bingo game or the new Bingo game.

**This document does not cover:**
- ESTD standard documents — see [ESTD0](./ESTD0_-_Markdown_format.md#estd-document-heading) and `AGENTS.md`.
- Inline code comments and doc-comments — see [ESTD1 §5. Code Documentation](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#5-code-documentation).
- PR descriptions — see [ESTD10 §5. PR Description Template](./ESTD10_-_PR_Authoring_And_Reviewing_Standards.md#5-pr-description-template).
- Confluence wiki articles that are not one of the five types below.

---

## 2. When to Write a Technical Document

**Write a technical document if any of the following are true:**

| Condition | Document Type |
|:----------|:--------------|
| A new feature requires changes to two or more system components (e.g., client + server, or server + database) | Technical Approach Document (TAD) |
| A significant architectural or technology decision is being made that will be difficult or costly to reverse | Architecture Decision Record |
| A recurring operational procedure has more than five steps, involves multiple team members, or must be executed under pressure (e.g., during an incident) | Runbook |
| A production incident occurred that caused player-visible impact or data risk | Post-mortem or Root Cause Analysis |
| A schema migration, platform migration, or data migration affects live production data | Migration Plan |

**You do NOT need a document for:**
- Bug fixes that do not introduce new behavior.
- Refactors confined to a single component with no interface changes.
- Configuration changes that follow an already-documented procedure.
- Features trivially contained within one component with no cross-team impact.

When in doubt, write the document. A brief document that turns out to be unnecessary costs one hour; a missing document that causes a production incident can cost days and player trust.

---

## 3. Document Types

### 3.1 Technical Approach Document (TAD)

Also referred to as a **Feature Design Document (FDD)**. Both names are used interchangeably within the team.

**Purpose:** Align the team on the design of a significant feature before a single line of production code is written. Surfaces design problems early — when they are cheapest to fix.

**Written by:** The engineer(s) who will implement the feature.  
**Reviewed by:** Relevant Architect(s) + affected team leads.  
**When:** Before sprint planning for the implementing sprint. A feature without an approved TAD cannot be scheduled.

**Scope trigger:** Any feature that touches two or more of: client, PHP API, Java/SEAM API, SmartFox, database schema, or AWS infrastructure.

---

### 3.2 Architecture Decision Record (ADR)

**Purpose:** Documents a significant architectural or technology decision — what was decided, why, what alternatives were considered, and what the accepted trade-offs are.

**Written by:** The architect or engineer proposing the change.  
**Reviewed by:** Director of Engineering + relevant Architect.  
**When:** Before the decision is executed, not after.

ADRs are immutable once approved. If the decision is later reversed, a new ADR is written that supersedes the old one. The old ADR is kept and marked `Superseded`.

**Examples of ADR-worthy decisions:**
- Adopt MongoDB Atlas as the primary datastore for SEAM microservices.
- Migrate the PHP API monolith authentication to a dedicated auth service.
- Switch from REST to WebSocket for a new real-time feature on the legacy live server.

---

### 3.3 Runbook

**Purpose:** Step-by-step operational procedures that must be executed correctly under time pressure or by engineers who did not write the system. Runbooks eliminate heroics during incidents and content resets.

**Written by:** The engineer who owns the system component.  
**Reviewed by:** At least one peer engineer who can verify the steps independently.  
**When:** Before the first time the procedure is executed in a live environment.

**Examples of procedures that need runbooks:**
- Weekly content reset sequence.
- SmartFox server room drain and restart.
- Database failover to the read replica.
- Jenkins pipeline recovery after a failed build agent.

---

### 3.4 Post-mortem or Root Cause Analysis (RCA)

**Purpose:** Documents what happened during a production incident, why it happened, and what changes will prevent it from happening again. Blameless by design — the goal is system improvement, not fault assignment.

**Written by:** The incident commander or on-call lead.  
**Reviewed by:** Director of Engineering + all engineers involved in the incident.  
**When:** Within 48 hours of incident resolution.

A post-mortem or RCA is not complete until every action item has an owner and a due date.

---

### 3.5 Migration Plan

**Purpose:** Documents the approach, risks, rollback strategy, and step-by-step execution plan for any migration that touches live production data or live infrastructure.

**Written by:** The engineer leading the migration.  
**Reviewed by:** Server Architect + Director of Engineering (and DBA if one is involved).  
**When:** At least one week before the migration is scheduled, to allow time for review and dry-run.

**Applies to:** Schema migrations, data backfill operations, cloud infrastructure migrations, platform changes (e.g., moving a service from EC2 to ECS).

---

## 4. Document Lifecycle

```
DRAFT ──► IN REVIEW ──► APPROVED / ACTIVE
                │               │
                │               ▼
                │          SUPERSEDED (for ADRs)
                │          DEPRECATED (for others)
                │
                ▼
           REJECTED (revision required → back to DRAFT)
```

| Status | Meaning |
|:-------|:--------|
| `Draft` | Being written; not yet submitted for review |
| `In Review` | Submitted; awaiting reviewer sign-off |
| `Active` | Approved and in effect |
| `Superseded` | Replaced by a newer ADR (the newer ADR links back to this one) |
| `Deprecated` | No longer applicable; retained for historical reference |
| `Rejected` | Reviewer requires significant revision; author returns to Draft |

---

## 5. Common Document Structure

All five document types share this structural skeleton. Each type adds or omits sections as defined in [§8](#8-templates).

### 5.1 Title and Metadata

```markdown
# <Document Type>: <Descriptive Title>

| Field | Value |
|:----|:----|
| **Type** | TAD / ADR / Runbook / Post-mortem or RCA / Migration Plan |
| **Status** | Draft / In Review / Active / Deprecated / Superseded |
| **Author(s)** | Name(s) |
| **Reviewers** | Name(s) |
| **Created** | YYYY-MM-DD |
| **Last Updated** | YYYY-MM-DD |
| **Related Ticket** | BINGO-XXXX |
```

### 5.2 Summary (TL;DR)

A single paragraph (3–5 sentences) that answers: *What is this document about, what decision or change does it describe, and what is the outcome?* A reader should be able to understand the document's significance from the summary alone.

### 5.3 Context and Problem Statement

Why does this document exist? What situation or problem triggered it? Provide just enough background for a reviewer who is not already familiar with the area to understand the "why."

### 5.4 Goals and Non-Goals

Two explicit lists. **Goals** are what the design/decision/plan must achieve. **Non-Goals** are things explicitly out of scope — equally important, because they prevent scope creep and miscommunication.

### 5.5 Main Body

The type-specific content. See the templates in [§8](#8-templates).

### 5.6 Risks and Mitigations

Every document must enumerate known risks and the planned response for each. Format as a table.

| Risk | Likelihood | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| ... | Low / Med / High | Low / Med / High | ... |

### 5.7 Open Questions

Questions that are not yet resolved at the time of writing. Each must have an owner and a target resolution date. A document with unresolved open questions cannot be moved to `Active`.

### 5.8 References

Links to related documents, tickets, Confluence pages, prior ADRs, or ESTD standards that informed this document.

---

## 6. Writing Style

These rules apply to all five document types.

### 6.1 Be Concrete

Use real names from the codebase and domain: `PlayerInventoryService`, `jackpot_pool`, `BINGO-4021`. Avoid placeholder names like `MyService` or `the database`. If you cannot use a real name, the design is not concrete enough to document.

### 6.2 Diagrams Over Prose

Whenever describing a data flow, system interaction, or state machine, use an ASCII diagram inside a fenced code block. A well-drawn diagram replaces a paragraph. A poor diagram is still better than no diagram.

```
Example — request flow for reward claim:

  Client                   PHP API            MySQL (RDS)
    │                        │                     │
    │── POST /reward/claim ─►│                     │
    │                        │── BEGIN TXN ───────►│
    │                        │── SELECT reward ───►│
    │                        │◄── reward row ──────│
    │                        │── UPDATE claimed ──►│
    │                        │── COMMIT ──────────►│
    │◄── 200 OK ────────────-│                     │
```

### 6.3 Length Discipline

| Section | Target Length |
|:--------|:-------------|
| Summary | 3–5 sentences |
| Context | ≤ 1 page |
| Goals / Non-Goals | ≤ 10 bullets each |
| Main body | As long as needed — no padding, no repetition |
| Risks | 1 row per risk |

Documents with unnecessary length are returned for revision.

### 6.4 What to Avoid

- **Vague language:** "The system may potentially encounter issues" → "The MySQL connection pool may exhaust under load spikes above 500 req/s."
- **Unqualified best practices:** "We should use microservices because they scale better." → State which specific problem microservices solve in this context and what you trade for it.
- **Hedging without rationale:** Commit to a position. If you are genuinely unsure, put it in Open Questions.
- **Passive voice for decisions:** "It was decided to…" → "The Server Architect decided to… because…"

---

## 7. Review and Approval

### 7.1 Required Reviewers by Document Type

| Type | Required Reviewers |
|:-----|:-------------------|
| Technical Approach Document (TAD) | Relevant Architect(s); Director of Engineering for cross-game features |
| Architecture Decision Record | Director of Engineering + relevant Architect |
| Runbook | One peer engineer who has not seen the procedure before (cold-read verification) |
| Post-mortem or RCA | Director of Engineering + all engineers involved in the incident |
| Migration Plan | Server Architect + Director of Engineering |

### 7.2 Review Process

1. Author sets status to `In Review` and shares the document link with required reviewers.
2. Reviewers comment directly on the document (in Confluence) or in the associated PR if the document is tracked in this repository.
3. All review comments must be addressed or explicitly acknowledged (with rationale for non-changes) before approval.
4. Approval is granted by updating the document status to `Active` with the approver's name and date recorded in the metadata table.
5. A document that requires fundamental rework is set to `Rejected`; the author revises and resubmits.

**SLA:** Reviewers must provide feedback within **2 business days** of being assigned. If no feedback is received within 2 business days, the author should escalate to the Director of Engineering.

---

## 8. Templates

Each template is ready to copy-paste. After pasting into a new file:
1. Replace all `<angle-bracket placeholders>`.
2. Delete inline `<!-- HTML comments -->`.
3. Add `<!-- toc -->` on its own line inside the `## Table of Contents` section.
4. Run `./scripts/generate-toc.sh <filename>` from the repo root to populate the Table of Contents.
5. Fill in all sections, then change `Status` to `In Review` when ready for review.

---

### 8.1 Technical Approach Document (TAD)

~~~markdown
# TAD: <Feature Name>
<!-- Also referred to as Feature Design Document (FDD) -->

| Field | Value |
|:----|:----|
| **Type** | Technical Approach Document (TAD) |
| **Status** | Draft |
| **Author(s)** | <Name> |
| **Reviewers** | <Names> |
| **Created** | YYYY-MM-DD |
| **Last Updated** | YYYY-MM-DD |
| **Related Ticket** | BINGO-XXXX |

---

## Table of Contents

<!-- Add the toc marker on the next line, then run ./scripts/generate-toc.sh -->

---

## 1. Summary

<!-- 3–5 sentences: what feature is being built, why, and what the proposed
     design is at the highest level. -->

## 2. Context and Problem Statement

<!-- What gap, player pain point, or business requirement triggers this feature?
     Include relevant metrics or data if available. -->

## 3. Goals

<!-- What must this feature achieve? Be specific and measurable. -->
- 
- 

## 4. Non-Goals

<!-- What is explicitly out of scope for this implementation? -->
- 
- 

## 5. Design

### 5.1 High-Level Architecture

<!-- ASCII diagram showing which components are involved and how they interact. -->

```
<system diagram>
```

### 5.2 API Changes

<!-- Omit if server-only or client-only change. For every new endpoint or
     contract-changing update, include the finalized client/server API contract
     from ESTD4 section 4.4.1 before implementation starts. -->

| Field | Value |
|:------|:------|
| Endpoint | `<METHOD> /api/v1/...` |
| Consumers | `<Unity client / SmartFox / PHP API / Java service / web tool>` |
| Auth | `<session token / service credential / public allowlist>` |
| Idempotency | `<required header / not applicable and why>` |
| Compatibility | `<supported client versions, feature flag, deprecation plan>` |
| Owners Approved | `<Client owner>, <Server owner>` |

Request fields:

| Field | Type | Range / Allowed Values | Required? | Default If Absent | Validation Criteria | Source |
|:------|:-----|:-----------------------|:----------|:------------------|:--------------------|:-------|
| `<field>` | `<string/int/bool/object/array>` | `<min/max, enum, format>` | `<Required/Optional>` | `<none/value>` | `<server-side rule>` | `<client-supplied/server-controlled>` |

Response fields:

| Field | Type | Range / Allowed Values | Required? | Default If Absent | Validation Criteria | Sensitivity |
|:------|:-----|:-----------------------|:----------|:------------------|:--------------------|:------------|
| `<field>` | `<string/int/bool/object/array>` | `<min/max, enum, format>` | `<Required/Optional>` | `<none/value>` | `<server guarantee>` | `<public/internal/PII/redacted>` |

Status and error contract:

| HTTP Status | Error Code | Meaning | Client Behavior |
|:------------|:-----------|:--------|:----------------|
| `200` | `none` | `<success case>` | `<update state / show result>` |
| `400` | `<ERROR_CODE>` | `<validation failure>` | `<show message / retry disabled>` |

Sample request:

```http
POST /api/v1/<resource> HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: <uuid-if-required>
Content-Type: application/json

{
  "<field>": "<value>"
}
```

Sample response:

```json
{
  "success": true,
  "data": {
    "<field>": "<value>"
  },
  "meta": {
    "requestId": "uuid-here",
    "timestamp": "2026-04-30T00:00:00Z",
    "apiVersion": "1"
  },
  "error": {}
}
```

Add more request/response examples when the API has complex variations:
validation failure, authorization failure, idempotent retry, pagination,
partial success, version/capability differences, or feature-flag behavior.

### 5.3 Database Changes

<!-- New tables, columns, indexes, or migration steps. Reference the migration
     plan (BINGO-XXXX) if one is required. -->

### 5.4 Client Changes

<!-- Unity scenes, prefabs, UI flows, or state machine changes. Include mockups
     or screen-flow diagrams if available. -->

### 5.5 Feature Flag

<!-- Name and scope of the feature flag controlling rollout. State the default
     value and which environments it will be enabled in at launch. -->

## 6. Alternatives Considered

<!-- At least two alternatives to the chosen design. For each: what it is,
     why it was not chosen. -->

| Alternative | Why Not Chosen |
|:------------|:---------------|
| | |

## 7. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| | | | |

## 8. Open Questions

| # | Question | Owner | Due |
|:--|:---------|:------|:----|
| 1 | | | |

## 9. References

- 
~~~

---

### 8.2 Architecture Decision Record (ADR)

~~~markdown
# ADR: <Decision Title>

| Field | Value |
|:----|:----|
| **Type** | Architecture Decision Record |
| **Status** | Draft |
| **Author(s)** | <Name> |
| **Reviewers** | <Names> |
| **Created** | YYYY-MM-DD |
| **Last Updated** | YYYY-MM-DD |
| **Related Ticket** | BINGO-XXXX |
| **Supersedes** | <ADR title / N/A> |
| **Superseded By** | N/A |

---

## Table of Contents

<!-- Add the toc marker on the next line, then run ./scripts/generate-toc.sh -->

---

## 1. Summary

<!-- The decision in one sentence, followed by 2–4 sentences of context.
     Example: "We adopt MongoDB Atlas as the primary datastore for all SEAM
     microservices. The document-model flexibility accommodates the frequent
     schema evolution expected during early game development, while managed
     Atlas removes operational overhead from the engineering team." -->

## 2. Context and Problem Statement

<!-- What situation forced this decision? What constraints exist
     (technical, team, timeline, cost)? -->

## 3. Decision

<!-- State the decision clearly and unambiguously.
     Example: "All new SEAM microservices will use MongoDB Atlas as their
     primary datastore. MySQL remains the standard for all legacy PHP API
     components and internal tool configuration." -->

## 4. Rationale

<!-- Why is this the right decision given the context and constraints?
     Avoid generics — be specific to this situation. -->

## 5. Alternatives Considered

| Alternative | Trade-offs | Why Not Chosen |
|:------------|:-----------|:---------------|
| | | |
| | | |

## 6. Consequences

<!-- What becomes easier as a result of this decision?
     What becomes harder? What technical debt does this incur? -->

**Positive:**
- 

**Negative / Trade-offs:**
- 

## 7. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| | | | |

## 8. References

- 
~~~

---

### 8.3 Runbook

~~~markdown
# Runbook: <Procedure Name>

| Field | Value |
|:----|:----|
| **Type** | Runbook |
| **Status** | Draft |
| **Author(s)** | <Name> |
| **Reviewers** | <Names> |
| **Created** | YYYY-MM-DD |
| **Last Updated** | YYYY-MM-DD |
| **System** | <PHP API / SmartFox / SEAM / AWS / Jenkins / ...> |
| **Execution Window** | <When is this run — e.g., "Weekly, Tuesday 02:00 IST"> |
| **Execution Time** | <Estimated time to complete> |
| **Related Ticket** | BINGO-XXXX |

---

## Table of Contents

<!-- Add the toc marker on the next line, then run ./scripts/generate-toc.sh -->

---

## 1. Summary

<!-- What does this procedure do and when is it run? -->

## 2. Prerequisites

<!-- Access, credentials, tools, or state that must be true before starting.
     If the engineer executing this needs specific AWS IAM roles or VPN
     access, state exactly which ones. -->

- [ ] <prerequisite 1>
- [ ] <prerequisite 2>

## 3. Steps

<!-- Number every step. Include the exact command or action and the expected
     output. If a step can fail, include what failure looks like and what to do. -->

### 3.1 Step 1: <Action Name>

```bash
<exact command>
```

**Expected output:**
```
<what success looks like>
```

**If this fails:** <!-- What to check, what to do, when to escalate. -->

### 3.2 Step 2: <Action Name>

<!-- Repeat the Step N pattern for each step. -->

## 4. Verification

<!-- How do you confirm the procedure completed successfully?
     Provide specific checks, not "confirm everything looks OK." -->

- [ ] <verification check 1>
- [ ] <verification check 2>

## 5. Rollback

<!-- Step-by-step instructions to undo this procedure if something goes wrong.
     Every runbook must have a rollback section, even if rollback is "not applicable"
     — in that case, explain why and what to do instead. -->

## 6. Escalation

<!-- Who to contact if something goes wrong and this runbook cannot resolve it.
     Include name, role, and contact method (Slack handle, phone). -->

| Role | Name | Contact |
|:-----|:-----|:--------|
| On-call lead | | |
| Server Architect | | |
| Director of Engineering | | |

## 7. References

- 
~~~

---

### 8.4 Post-mortem or RCA

~~~markdown
# RCA : <Incident Title>

| Field | Value |
|:----|:----|
| **Type** | RCA |
| **Status** | Draft |
| **Incident Date** | YYYY-MM-DD |
| **Severity** | P0 / P1 / P2 |
| **Duration** | <HH:MM from detection to resolution> |
| **Author(s)** | <Incident Commander + contributing engineers> |
| **Reviewers** | <Names> |
| **Created** | YYYY-MM-DD |
| **Related Ticket** | BINGO-XXXX |

---

## Table of Contents

<!-- Add the toc marker on the next line, then run ./scripts/generate-toc.sh -->

---

## 1. Summary

<!-- 3–5 sentences: what happened, who was affected, how long it lasted,
     and what resolved it. -->

## 2. Impact

| Dimension | Detail |
|:----------|:-------|
| **Player impact** | <e.g., "~12,000 players unable to claim rewards for 47 minutes"> |
| **Revenue impact** | <estimated, or "under investigation"> |
| **Data integrity** | <any records corrupted, duplicated, or lost> |
| **Systems affected** | <list components> |

## 3. Timeline

<!-- Exact timestamps (UTC or IST — be consistent). Include detection,
     investigation milestones, mitigation steps, and resolution. -->

| Time (IST) | Event |
|:-----------|:------|
| HH:MM | Incident detected via <monitoring alert / player report / engineer observation> |
| HH:MM | |
| HH:MM | Incident resolved |

## 4. Root Cause

<!-- The single most fundamental cause. Avoid surface-level causes ("the server
     crashed") — trace to the root ("a missing database index caused query latency
     to spike under content-reset load, exhausting the PHP connection pool"). -->

## 5. Contributing Factors

<!-- Secondary conditions that allowed the root cause to have this level of impact. -->
- 
- 

## 6. What Went Well

<!-- Honest recognition of what worked: detection, communication, rollback, etc. -->
- 
- 

## 7. What Went Poorly

<!-- Honest recognition of gaps: late detection, insufficient monitoring,
     unclear runbook, etc. -->
- 
- 

## 8. Action Items

<!-- Every action item must have an owner and a due date.
     An RCA is not complete until this table is fully populated. -->

| # | Action | Owner | Due | Status |
|:--|:-------|:------|:----|:-------|
| 1 | | | | Open |
| 2 | | | | Open |

## 9. References

- 
~~~

---

### 8.5 Migration Plan

~~~markdown
# Migration Plan: <Migration Title>

| Field | Value |
|:----|:----|
| **Type** | Migration Plan |
| **Status** | Draft |
| **Author(s)** | <Name> |
| **Reviewers** | <Names> |
| **Created** | YYYY-MM-DD |
| **Last Updated** | YYYY-MM-DD |
| **Scheduled Date** | YYYY-MM-DD |
| **Execution Window** | <Start time – End time, with timezone> |
| **Related Ticket** | BINGO-XXXX |

---

## Table of Contents

<!-- Add the toc marker on the next line, then run ./scripts/generate-toc.sh -->

---

## 1. Summary

<!-- What is being migrated, from what state to what state, and why. -->

## 2. Goals

- 
- 

## 3. Non-Goals

- 
- 

## 4. Pre-migration State

<!-- Describe the current state of the system before the migration.
     Include schema snapshots, record counts, or current configuration
     as appropriate. -->

## 5. Post-migration State

<!-- Describe the expected state after successful migration. -->

## 6. Migration Approach

<!-- High-level strategy: online vs. offline migration, dual-write window,
     blue-green deployment, phased rollout, etc. -->

```
<ASCII diagram of migration flow if applicable>
```

## 7. Execution Steps

<!-- Number every step. Include exact SQL, CLI commands, or UI actions.
     For database migrations include EXPLAIN output for affected queries. -->

### 7.1 Phase 1: Preparation (before execution window)

- [ ] Step 1: 
- [ ] Step 2: 

### 7.2 Phase 2: Execution (within execution window)

- [ ] Step 1: 
- [ ] Step 2: 

### 7.3 Phase 3: Verification

<!-- Specific queries or checks that confirm migration succeeded.
     Do not proceed to "complete" status until all checks pass. -->

- [ ] 
- [ ] 

## 8. Rollback Plan

<!-- Step-by-step rollback procedure. Must be executable within the
     execution window. State the rollback decision point — after what
     step is rollback no longer possible? -->

**Rollback decision point:** <after Step X, rollback is not possible because...>

### 8.1 Rollback Steps

- [ ] Step 1:
- [ ] Step 2:

## 9. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| | | | |

## 10. Communication Plan

<!-- Who needs to be notified and when: before, during, and after the migration. -->

| Phase | Audience | Message | Channel |
|:------|:---------|:--------|:--------|
| Before | Engineering team | Migration scheduled | Slack / Email |
| During | On-call team | Migration in progress | Slack |
| After | Director of Engineering | Migration complete / failed | Slack |

## 11. References

- 
~~~
