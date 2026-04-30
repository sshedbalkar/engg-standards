# ESTD10 - Pull Request Authoring and Review Standards for Engineers

**ESTD10 — Pull Request Authoring and Review Standards**

| Field | Value |
|:----- |:----- |
| Document ID | ESTD10 |
| Version | 4.2 |
| Status | Active |
| Last Updated | 2026-04-27 |
| Applies To | All engineers — client, server, tools, infrastructure, website   |
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) through [ESTD9](./ESTD9_-_Database_Standards.md#estd9---database-standards-and-best-practices), [ESTD11](./ESTD11_-_Web_Development_and_Deployment_Standards.md#estd11--web-tools-creation-and-deployment-standards) through [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds)|
| Approval | Director of Engineering |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD10 defines how Pull Requests (PRs) are created and reviewed across every discipline. It is the primary mechanism by which the standards in [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) – [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds) are enforced in practice. Every engineer, regardless of seniority, must follow these guidelines as both an author and a reviewer.

A PR that does not meet these standards will be returned to the author without a full review. This is not a personal critique — it protects the reviewer's time and maintains the quality of the review signal.

---

## Table of Contents

- [ESTD10 - Pull Request Authoring and Review Standards for Engineers](#estd10---pull-request-authoring-and-review-standards-for-engineers)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Why Pull Requests Matter](#2-why-pull-requests-matter)
  - [3. Before Opening a PR](#3-before-opening-a-pr)
  - [4. PR Title Format](#4-pr-title-format)
  - [5. PR Description Template](#5-pr-description-template)
  - [6. PR Size Guidelines](#6-pr-size-guidelines)
  - [7. Author Responsibilities](#7-author-responsibilities)
    - [7.1 Self-Review First](#71-self-review-first)
    - [7.2 Annotate Complex Changes](#72-annotate-complex-changes)
    - [7.3 Respond to All Review Comments](#73-respond-to-all-review-comments)
    - [7.4 Do Not Force-Push After Review Has Started](#74-do-not-force-push-after-review-has-started)
  - [8. Reviewer Assignment](#8-reviewer-assignment)
    - [8.1 Required Reviewers by Change Type](#81-required-reviewers-by-change-type)
    - [8.2 Peer Reviewer Selection](#82-peer-reviewer-selection)
    - [8.3 Review Turnaround SLA](#83-review-turnaround-sla)
  - [9. Reviewer Responsibilities and Review Checklist](#9-reviewer-responsibilities-and-review-checklist)
    - [9.1 Mindset](#91-mindset)
    - [9.2 Correctness](#92-correctness)
    - [9.3 Standards Compliance](#93-standards-compliance)
    - [9.4 Security](#94-security)
    - [9.5 Testability and Tests](#95-testability-and-tests)
    - [9.6 Performance](#96-performance)
    - [9.7 Database Migrations (if applicable)](#97-database-migrations-if-applicable)
    - [9.8 Architecture and Design: What QA Cannot Catch](#98-architecture-and-design-what-qa-cannot-catch)
  - [10. Review Comment Standards](#10-review-comment-standards)
    - [10.1 Comment Severity Labels](#101-comment-severity-labels)
    - [10.2 How to Write Good Review Comments](#102-how-to-write-good-review-comments)
  - [11. Approval and Merge Rules](#11-approval-and-merge-rules)
    - [11.1 Approval Requirements](#111-approval-requirements)
    - [11.2 Merge Rules](#112-merge-rules)
    - [11.3 No Self-Merging](#113-no-self-merging)
    - [11.4 Release-Close PRs](#114-release-close-prs)
  - [12. Draft PRs](#12-draft-prs)
  - [13. Hotfix PRs](#13-hotfix-prs)
  - [14. Schema Migration PRs](#14-schema-migration-prs)
  - [15. Infrastructure (IaC) PRs](#15-infrastructure-iac-prs)
  - [16. Jenkins Pipeline PRs](#16-jenkins-pipeline-prs)
  - [17. CI/CD Pipeline Integration (Jenkins)](#17-cicd-pipeline-integration-jenkins)
  - [18. Common Pitfalls to Avoid](#18-common-pitfalls-to-avoid)

---

## 1. Purpose and Scope

The Pull Request process is the primary quality gate for all code entering shared branches. It ensures standards compliance before code reaches `develop` or `main`, knowledge sharing between engineers, and a documented history of why decisions were made.

This process applies to all code, infrastructure, deployment, and database migration changes. No code enters a shared branch without a reviewed and approved PR.

---

## 2. Why Pull Requests Matter

**What a PR is:** A PR is a formal proposal to merge a set of changes into a shared branch. It creates a window for human review before those changes affect other engineers or, ultimately, players.

A change that breaks a payment flow or corrupts a player's coin balance cannot be easily undone once it has affected a live player session. The PR process is the last line of human defense before a change reaches production. It is not bureaucracy — it is player protection.

The review process also serves as a knowledge-sharing mechanism. Reviewers learn about changes in parts of the codebase they do not own. Authors receive a second perspective that routinely catches bugs, security issues, and design problems before they become incidents.

Our team context: With engineers across different time zones, a clear asynchronous review process with defined SLAs (Service Level Agreement) is especially important. Reviews and responses must be documented in the PR thread, not in chat messages that disappear.

---

## 3. Before Opening a PR

Before opening a PR, the author must verify all of the following:

- [ ] All CI checks pass locally: tests, linting, static analysis, coverage threshold.  
- [ ] The branch is up to date with `develop` (or `main` for hotfixes). Rebase or merge `develop` into the branch before opening.  
- [ ] There are no merge conflicts.  
- [ ] The commit history is clean: no WIP commits, no "fix typo" commits that could be squashed, no committed secrets.  
- [ ] The feature is testable in the `staging` environment. If applicable, the feature flag is configured in the staging environment before the PR is opened.  
- [ ] For database migrations: the migration has been tested against a local or staging database, and the EXPLAIN output for affected queries has been reviewed.  
- [ ] The `CHANGELOG.md` has been updated if this PR is part of a release branch (per [ESTD1 §25. Changelog Extraction for Production Builds](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#25-changelog-extraction-for-production-builds)).

---

## 4. PR Title Format

PR titles must mirror the commit message format defined in [ESTD1 §21.2 Commit Message Format](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#212-commit-message-format):

```
<type>(<scope>): <short summary>
```

**Examples:**

```
feat(reward-engine): add periodic jackpot bonus distribution
fix(live-server): prevent duplicate win event on room reconnect
refactor(php-api): extract player balance into dedicated service
chore(deps): bump mysql-connector-j from 8.3.0 to 8.4.0
db(schema): add gdpr_erasure_requests table migration V1_4_0
infra(terraform): add scheduled scaling for content reset windows
```

The PR title becomes the squash-merge commit message. It must be accurate and meaningful. A vague title such as "fixes" or "updates" will be rejected.

---

## 5. PR Description Template

```
Every PR must use this template. Empty sections must be explicitly filled in or marked N/A. An empty description results in the PR being returned to the author.
## Summary

<!-- 2–5 sentences describing what this PR does and WHY it was needed.
     Link to the JIRA/project ticket. Be specific enough that a reviewer
     can understand the change without reading the full diff first. -->

Refs: BINGO-XXXX

## Type of Change

<!-- Check all that apply -->
- [ ] New feature
- [ ] Bug fix
- [ ] Refactor (no behavior change)
- [ ] Performance improvement
- [ ] Database schema migration
- [ ] Infrastructure / IaC change
- [ ] Documentation only
- [ ] Hotfix

## How to Test

<!-- Step-by-step instructions for the reviewer to verify the change
     works correctly. Include:
     - Environment (local / dev / staging)
     - Test data setup required
     - Steps to execute
     - Expected outcomes
     This section must be specific enough that a reviewer can reproduce
     the verification without asking the author for help. -->

## Screenshots / Videos (if UI change)

<!-- Before/after screenshots or a short screen recording.
     Mandatory for all UI changes. -->

## Author Checklist

- [ ] I have read and followed the relevant ESTD standards for this change
- [ ] All new public methods and interface methods have doc-comments
- [ ] Unit tests have been added or updated (minimum 80% coverage on new code)
- [ ] I have verified the CI pipeline passes in full
- [ ] I have run EXPLAIN on any new or changed SQL queries
- [ ] No secrets or credentials are included in this PR
- [ ] Logging added for new error paths and key state transitions (per ESTD1 §9)
- [ ] Feature flag added if this change introduces a new player-facing feature (ESTD1 §15.4)
- [ ] CHANGELOG.md updated if this is a release-bound change (ESTD1 §22)
- [ ] Data privacy impact considered (new PII fields documented in data inventory)
- [ ] Release Risk Note completed if this PR is release-close (see §11.4)

## Database Migrations (if applicable)

- Migration file name:
- Estimated execution time on production-sized table:
- Backward-compatible (expand-contract pattern applied): [ ] Yes / [ ] N/A
- Rollback procedure:
- Applied and verified in staging: [ ] Yes / [ ] N/A

## Breaking Changes

<!-- Describe any breaking changes to API contracts or client compatibility.
     List the affected clients and the migration plan. Per ESTD4 §4.2,
     breaking changes require a versioned migration path. -->

## Release Risk Note (if release-close)

<!-- Required if this PR is opened after release branch cut, after code freeze,
     or within 2 business days of planned code freeze or release.
     Fill every field or mark N/A with a reason. -->

- Target release or code freeze date:
- Why this cannot wait for the next release:
- Impacted artifact: Unity binary / server deploy / configuration/content / database / IaC / pipeline / web-tooling / N/A
- Risk and blast radius:
- Validation evidence:
- Rollback, feature flag, feature-disable control, staged rollout, or phased release plan:
- Reviewer and Architect availability confirmed: [ ] Yes / [ ] N/A
- Post-merge or rollout monitoring owner:

## ESTD Exception Requests

<!-- If this PR intentionally deviates from a ESTD rule, document it here.
     Format: "ESTD[N]-EXCEPTION: <rule ref> — <reason> — approved by <name> on <date>" -->
```

---

## 6. PR Size Guidelines

Small PRs are reviewed faster, produce better feedback, and are safer to deploy. Large PRs produce review fatigue, which means reviewers miss bugs.

| PR Size | Lines Changed | Guideline |
|:--------|:--------------|:----------|
| Ideal | < 200 | Reviewable in 20–30 minutes |
| Acceptable | 200–500 | Reviewable in 30–60 minutes; consider splitting |
| Large | 500–800 | Must be split unless the change is inherently atomic (e.g., a generated migration) |
| Too Large | > 800 | Will be returned to the author for splitting. No exceptions. |

**When a feature is too large for one PR, use a stacked PR approach:**

```
develop
  └── feature/BNG-4201-jackpot-base        ← base feature branch
        ├── feature/BNG-4201-jackpot-db     ← sub-feature: schema + migration
        ├── feature/BNG-4201-jackpot-api    ← sub-feature: API endpoint + service
        └── feature/BNG-4201-jackpot-client ← sub-feature: Unity integration
```

Each sub-feature branch becomes its own PR merged into the base branch. The base branch is merged into `develop` as the final PR once all sub-features are reviewed and approved.

---

## 7. Author Responsibilities

### 7.1 Self-Review First

Before requesting a review, do a full self-review of the diff. You should be able to justify every line of code you added. Read your own code as a reviewer would — look for missing error handling, unclear naming, and untested paths.

### 7.2 Annotate Complex Changes

Where the diff is not self-explanatory, add PR-level comments on specific lines explaining your reasoning. This is especially important for non-obvious algorithm choices, performance optimizations, workarounds for external constraints (SmartFox limitations, third-party API quirks), and ESTD exception requests.

### 7.3 Respond to All Review Comments

Every review comment must receive a response. If you made the change, reply with a short confirmation. If you disagree, reply with your reasoning — do not silently make partial changes or ignore disagreements. If the comment is resolved after discussion, mark it resolved. Do not mark a reviewer's open comment as resolved while the discussion is still ongoing.

### 7.4 Do Not Force-Push After Review Has Started

Once a review has been requested, do not force-push to the branch. Use additional commits for changes. Force-pushes destroy review history and invalidate existing review comments. The final squash happens at merge time, not during review.

---

## 8. Reviewer Assignment

### 8.1 Required Reviewers by Change Type

| Change Type | Required Reviewers |
|:------------|:-------------------|
| Feature / bug fix (client) | 1 peer engineer + Client Architect for changes > 200 lines |
| Feature / bug fix (server) | 1 peer engineer + Server Architect for changes > 200 lines |
| Database migration | Server Architect review mandatory | 
| Infrastructure / IaC change | Server Architect review mandatory |
| Security-related change | Server Architect review mandatory |
| Hotfix | 1 reviewer minimum; Server/Client Architect informed immediately 

### 8.2 Peer Reviewer Selection

Assign a reviewer who is familiar with the affected subsystem, has not contributed to the same PR (the author cannot be a reviewer), and is not the only person who understands the area. Rotate reviewers deliberately to spread knowledge across the team.

### 8.3 Review Turnaround SLA

| Priority | Turnaround |
|:---------|:-----------|
| Hotfix | Within 2 hours |
| Normal feature / bug fix | Within 1 business day |
| Large PR (> 400 lines) | Within 2 business days |

Given our India-based team and US-based player base, "business day" means within the India business day for normal PRs. Hotfixes must be communicated via direct message to the reviewer, not just via PR assignment, to ensure prompt response.

---

## 9. Reviewer Responsibilities and Review Checklist

### 9.1 Mindset

The reviewer's job is to make the code better and to protect the team from future problems — not to find fault with the author. Every comment must be constructive and include a suggestion or direction, not just a criticism. Praise is also appropriate when you see something done particularly well.

### 9.2 Correctness

- [ ] Does the code do what the PR description says it does?  
- [ ] Are there edge cases not handled: null inputs, empty collections, boundary values?  
- [ ] Does the code handle failure correctly, per [ESTD1 §9. Error Handling and Try-Catch Usage](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#9-error-handling-and-try-catch-usage)?  
- [ ] Are there race conditions or concurrency issues (especially relevant for SmartFox server code)?  
- [ ] If optimistic UI is used, is there a rollback path ([ESTD2 §4.7 Optimistic UI](./ESTD2_-_General_Client_Engg_Standards.md#47-optimistic-ui))?

### 9.3 Standards Compliance

- [ ] Does every new public/interface method have a doc-comment ([ESTD1 §5. Code Documentation](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#5-code-documentation))?  
- [ ] Are exceptions handled individually — not in block try-catches ([ESTD1 §9.3 Block Try-Catch: The Anti-Pattern and the Acceptable Exceptions](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#93-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions))?  
- [ ] Is all external input validated and sanitized at the boundary ([ESTD1 §11. Input Validation and Sanitization](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#11-input-validation-and-sanitization))?  
- [ ] Are log messages at the correct level and free of PII ([ESTD1 §12. Logging](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#12-logging))?  
- [ ] Are there no hardcoded secrets or credentials ([ESTD1 §19. Secrets Management](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#19-secrets-management))?  
- [ ] Does no file exceed 250 lines of executable code ([ESTD1 §6. File and Class Size Constraints](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#6-file-and-class-size-constraints))?  
- [ ] Does the code follow the language-specific style guide ([ESTD3](./ESTD3_-_Unity_and_C%23_Standards.md#estd3---unity-and-c-standards-for-engineers), [ESTD6](./ESTD6_-_PHP_Programming_Standards.md#estd6---php-programming-standards), [ESTD7](./ESTD7_-_Java_Programming_Standards.md#estd7---java-programming-standards-for-bingo-microservices-and-smartfox-server), or [ESTD12](./ESTD12_-_Smartfox_Server_Standards.md#estd12--smartfox-server-standards-for-bingo-game-development))?  
- [ ] Is the content reset period read from configuration, not hardcoded ([ESTD1 §13.5 Content Reset Cadence](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#135-content-reset-cadence))?

### 9.4 Security

- [ ] Are all DB queries parameterized ([ESTD9 §8.1 Parameterized Queries Only](./ESTD9_-_Database_Standards.md#81-parameterized-queries-only))?  
- [ ] Is authorization verified server-side for any new endpoint ([ESTD4 §5. Authentication and Authorization](./ESTD4_-_Server_Engg_Standards.md#5-authentication-and-authorization))?  
- [ ] Are rate limits applied to new endpoints ([ESTD4 §7. Rate Limiting and Abuse Prevention](./ESTD4_-_Server_Engg_Standards.md#7-rate-limiting-and-abuse-prevention))?  
- [ ] Is idempotency handled correctly for state-changing operations ([ESTD4 §8. Idempotency](./ESTD4_-_Server_Engg_Standards.md#8-idempotency))?

### 9.5 Testability and Tests

- [ ] Are new tests present for new code? Is coverage ≥ 80% for new business logic?  
- [ ] Do tests cover edge cases, boundary conditions, and failure paths?  
- [ ] Are tests independent and deterministic (runnable multiple times with the same result)?

### 9.6 Performance

- [ ] Are there N+1 query patterns ([ESTD9 §7. Indexing Standards](./ESTD9_-_Database_Standards.md#7-indexing-standards))?  
- [ ] Are there per-frame allocations in Unity code ([ESTD3 §7. Memory and Garbage Collection](./ESTD3_-_Unity_and_C%23_Standards.md#7-memory-and-garbage-collection)?  
- [ ] Is caching applied or invalidated correctly ([ESTD4 §13. Caching Strategy](./ESTD4_-_Server_Engg_Standards.md#13-caching-strategy))?  
- [ ] Have new or changed queries been reviewed with `EXPLAIN` and supporting indexes ([ESTD9 §7. Indexing Standards](./ESTD9_-_Database_Standards.md#7-indexing-standards))?

### 9.7 Database Migrations (if applicable)

- [ ] Is the migration named and numbered correctly ([ESTD9 §9.2 Migration Naming Convention](./ESTD9_-_Database_Standards.md#92-migration-naming-convention))?  
- [ ] Is the migration backward-compatible — expand-contract applied ([ESTD9 §9.4 The Expand-Contract Pattern for Zero-Downtime Migrations](./ESTD9_-_Database_Standards.md#94-the-expand-contract-pattern-for-zero-downtime-migrations))?  
- [ ] Has `EXPLAIN` been run and reviewed for affected queries?  
- [ ] Is the rollback procedure defined?

### 9.8 Architecture and Design: What QA Cannot Catch

**The rule:** PR review is the only phase in the delivery pipeline where a human with full source-code context evaluates architectural alignment, structural quality, and standards adherence. QA does not — and cannot — do this.

QA operates on the running artifact. It verifies that the application behaves correctly from the outside: flows complete, states persist, regressions are absent. It answers "does it work?" It cannot answer "is it well-designed?" — because design is not observable at runtime.

This means that a change which passes QA cleanly can still introduce compounding technical debt: a service that has absorbed responsibility it doesn't own, a module boundary that has been silently eroded, a design pattern applied incorrectly but not incorrectly enough to fail a test. These problems do not manifest as bugs today. They manifest as incidents, painful migrations, or blocked feature development six months from now. The PR review is the last and only gate where this class of problem can be caught.

What QA cannot cover — and reviewers must:

- **Structural integrity:** Is coupling appropriate? Are responsibilities correctly assigned? Does the change respect existing module or service boundaries?
- **Architectural alignment:** Does the change follow the agreed-upon service model, component hierarchy, or data ownership rules — or does it quietly deviate?
- **Pattern correctness:** Are design patterns applied with intent, or cargo-culted? A pattern used in the wrong context is worse than no pattern.
- **Long-term readability:** Can the next engineer — unfamiliar with this PR — understand, extend, or debug this code without the author present?
- **Standards compliance that doesn't surface at runtime:** Naming, doc-comments, file size limits, logging levels, config vs. hardcoded values. These are invisible to QA but compound across hundreds of PRs.
- **Silent technical debt:** An implementation that works but is poorly structured is a liability. A working-but-wrong design is harder to fix later than a broken-but-correct one.

In our specific context, this weight is higher than average. A 15-year-old live-service codebase running in parallel with a new platform means every structural shortcut taken today becomes a migration cost later. Reviewers are not just protecting the current sprint — they are protecting the ability to ship confidently a year from now.

**Practical guidance:** Once the checklist items in §9.2–9.7 are satisfied, treat the remaining review time as a design review. Ask: *Would I be comfortable inheriting this code cold? Does this change leave the codebase better or worse than it found it?* If the answer to either is no, that is a [BLOCKER] or [IMPORTANT] comment.

---

## 10. Review Comment Standards

### 10.1 Comment Severity Labels

Every review comment must be prefixed with a severity label so the author knows how to prioritize responses.

| Label | Meaning | Blocks Merge? | 
|:------|:--------|:--------------|
| [BLOCKER] | Must be fixed before merge. Standards violation, bug, security issue. | Yes |
| [IMPORTANT] | Should be fixed. May be deferred with documented justification. | At reviewer's discretion |
| [SUGGESTION] | Optional improvement. Author decides. | No | 
| [QUESTION] | Reviewer needs clarification. Does not imply a required change. | No, until answered |
| [NITPICK] | Minor style or wording point. Author may ignore. | No |

### 10.2 How to Write Good Review Comments

Be specific: reference the exact line and explain what is wrong and why. Be constructive: offer an alternative or a direction, not just a complaint. Be respectful: critique the code, not the author.

```
// BAD review comment
This is wrong.

// GOOD review comment
[BLOCKER] This query is vulnerable to SQL injection because $playerId is
concatenated directly into the SQL string. Per ESTD9 §7.1, all queries must
use parameterized statements:

$stmt = $this->_pdo->prepare('SELECT ... WHERE player_id = :playerId');
$stmt->execute([':playerId' => $playerId]);
```

---

## 11. Approval and Merge Rules

### 11.1 Approval Requirements

| Change Type | Approvals Required |
|:------------|:-------------------|
| Standard feature / bug fix | 1 peer approval |
| Change > 200 lines | 1 peer + Architect approval |
| Database migration | 1 peer + Server Architect |
| Security / economic logic | 1 peer + Server Architect |
| Hotfix | 1 approval minimum; Architect informed |


### 11.2 Merge Rules

- No PR may be merged with unresolved `[BLOCKER]` or `[IMPORTANT]` comments.  
- No PR may be merged if CI is failing.  
- No PR may be merged directly to `main`. Only release branches or hotfix branches are merged to `main`.  
- All production merges must be squash-merged with the PR title as the commit message.  
- After merging, the feature branch must be deleted.

### 11.3 No Self-Merging

A PR author must not merge their own PR, even if they have the repository permissions to do so. This rule has no exceptions.

### 11.4 Release-Close PRs

A release-close PR is any non-hotfix PR opened after the release branch is cut, after code freeze, or within 2 business days of the planned code freeze or release date. A code freeze is the period where release-bound code is expected to stay stable except for approved release-risk reduction. Treat freeze windows as risk controls: late changes should make the release safer, not merely more complete.

The default outcome for a release-close PR is **defer to the next release**. Merge is allowed only when the change:

- fixes a release blocker or release regression;
- reduces release risk;
- addresses an approved security, compliance, payment, economy, or data-safety issue;
- closes a release-readiness gap that would otherwise block promotion.

Release-close PRs must not include opportunistic refactors, cosmetic cleanup, broad rewrites, dependency churn, or new feature scope. The change must be the smallest safe diff. Prefer configuration, feature flags, or a feature-disable control over code change when those options safely reduce risk. A feature-disable control is any runtime switch that disables the risky path without requiring a new build.

CI must pass before merge. Deadline pressure does not justify bypassing tests, linting, static analysis, security scans, required reviewers, or unresolved `[BLOCKER]` / `[IMPORTANT]` comments.

Late changes must be classified by rollback difficulty:

| Change Type | Release-Close Guidance |
|:------------|:-----------------------|
| Server, config, content, or internal tooling | May be acceptable if independently deployable, quickly reversible, and validated in staging. |
| Unity or mobile binary change | Higher risk because app-store rollback is constrained; require strong validation and explicit Client Architect approval. |
| Database, IaC, pipeline, security, payment, or economy change | Highest risk; require Architect approval, staging proof, rollback or mitigation plan, and monitoring owner. |

Where available, use progressive exposure: limit the change to a controlled subset of players, traffic, or environments before expanding it. Acceptable mechanisms include feature flags, canary, blue/green, staged rollout, or phased release. The PR must define health checks, halt criteria, and rollback or roll-forward action before merge.

Release branch hygiene is mandatory:

- Do not force-push after review starts.
- Do not include unrelated commits.
- Do not merge from a stale branch.
- Do not merge if the change invalidates QA or staging sign-off without explicit Engineering release owner approval.

Responsibilities:

- **Author:** Prove why the change cannot wait, keep scope minimal, run validation before review, complete the Release Risk Note, provide rollback or disablement steps, confirm reviewer availability, and stay responsive until the merge or defer decision is closed.
- **Reviewer:** Verify urgency, scope containment, evidence quality, compatibility, rollback, observability, and release impact. If evidence is weak, mark the PR `[BLOCKER]` or require deferral.
- **Architect / Engineering release owner:** Decide merge versus defer within Engineering, confirm release branch and build impact, approve any accelerated path, and document any exception.
- **Other functions:** QA, Product, LiveOps, Support, or Marketing are consulted only when their owned surface changes, such as QA scope, player-facing commitments, content timing, economy impact, or release communication. Approval remains Engineering-owned unless an existing governance rule says otherwise.

---

## 12. Draft PRs

Draft PRs are permitted and encouraged for:

- Work in progress where early feedback is wanted before the feature is complete.  
- Large features where the architecture should be validated before the implementation is finished.  
- Stacked PRs where the base branch is not yet merged.

A draft PR must be clearly described as such in the title prefix: `[WIP] feat(reward-engine): jackpot distribution`. Reviewers are not expected to provide a full review of a draft PR unless explicitly requested. Draft PRs must be converted to ready-for-review status before a formal review is requested.

---

## 13. Hotfix PRs

A hotfix is an emergency change to address a critical P1 or P2 production incident. Hotfix PRs have an expedited process:

- Branch from `main`: `hotfix/BNG-XXXX-short-description`.  
- Fix the issue. Keep the change as small as possible — fix only what is broken.  
- Open a PR targeting `main` with the prefix `hotfix` in the title.  
- Tag the Server or Client Architect directly in chat (not just via PR assignment) for immediate review.  
- After merging to `main` and tagging the release, immediately open a second PR to back-port the fix to `develop` and any active release branches.  
- Document the hotfix in `CHANGELOG.md` and in the incident post-mortem.

A hotfix PR does not exempt the author from the standard checklist. The expedited timeline applies to the review turnaround, not to the standards themselves.

---

## 14. Schema Migration PRs

Schema migration PRs carry higher risk than application code PRs because:

- Migrations applied to production cannot always be rolled back cleanly.  
- A poorly written migration can lock production tables for seconds or minutes, affecting all live players.  
- The expand-contract pattern required for zero-downtime deployments means migrations are sometimes applied in phases across multiple PRs.

**Additional requirements for migration PRs:**

- The PR description must include the estimated execution time on production-sized data. If the estimate is unknown, it must be run against a production-data-sized clone in staging before the PR is approved.  
- For tables with more than 1 million rows, `pt-online-schema-change` or `gh-ost` must be used and the PR must include the exact command to be run.  
- The migration must be applied to staging and verified before the production deployment PR is opened.  
- The Server Architect must approve all migration PRs. No exceptions.

---

## 15. Infrastructure (IaC) PRs

Infrastructure changes are code changes with operational consequence. Applying a broken Terraform plan to production can remove a security group, delete a database, or expose a private endpoint to the internet.

**Additional requirements for IaC PRs:**

- The PR must include the output of `terraform plan` (or the equivalent for the team's IaC tool) as a PR comment or attached file. This is the reviewer's primary input for understanding the change.  
- Destructive actions in the plan (resources marked `destroy` or `replace`) must be explicitly called out in the PR summary and require Architect approval.  
- IaC changes must be applied to the `dev` or `staging` environment first and verified before production.  
- Any IaC change that affects production security groups, IAM policies, VPC routing, or RDS configuration requires the Server Architect's explicit written approval.

---

## 16. Jenkins Pipeline PRs

Changes to `Jenkinsfile` or shared library code are subject to the same PR review standards as application code. Additionally:

- Pipeline changes must be reviewed by a senior engineer who understands the build infrastructure.  
- Changes that affect production deployment stages require explicit Architect approval.  
- Test the pipeline on a feature branch before merging to `develop`.  
- See [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds) for the full Jenkins standards.

---

## 17. CI/CD Pipeline Integration (Jenkins)

All PRs must pass the Jenkins CI pipeline before they can be merged. The Jenkins build is a mandatory check on all protected branches. The pipeline includes: lint, unit tests, build compilation, and BOM CVE scan ([ESTD1 §26. Generating a Bill of Materials (BOM) for a Project](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#26-generating-a-bill-of-materials-bom-for-a-project)). A PR with a failing CI pipeline must not be merged under any circumstances, even for hotfixes. For hotfixes, the pipeline must be fixed as part of the hotfix itself.

For Unity client PRs: the QA/Staging/Production build pipeline is defined in `Jenkinsfile` at the repo root. Pipeline changes follow the same PR process as application code and require an additional Architect reviewer ([ESTD13 §14.2 Restricting Pipeline Mutation](./ESTD13_-_Jenkins_CI_CD_Standards.md#142-restricting-pipeline-mutation)).

For web tool PRs: the Next.js build pipeline in [ESTD13 §8. Web Tools Build Pipelines](./ESTD13_-_Jenkins_CI_CD_Standards.md#8-web-tools-build-pipelines) must pass. This includes `npm run lint`, `npm run test:ci`, and `npm run build`.

See [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds) for the full Jenkins standards.

---

## 18. Common Pitfalls to Avoid

| # | Pitfall | Impact | Remedy |
|:--|:--------|:-------|:-------|
| 1 | Opening a PR without running CI locally | CI failures delay review; reviewer's time is wasted | Always run the full CI suite locally before opening |
| 2 | Vague PR title or empty description | Reviewer cannot understand the change; increased review time | Follow the template strictly |
| 3 | PR > 800 lines without justification | Review fatigue; bugs missed; slower merge | Split into stacked PRs |
| 4 | No tests for new business logic | Bugs ship to production | 80% coverage is mandatory | 
| 5 | Self-merging | Defeats the purpose of code review | Never self-merge, even with permissions |
| 6 | Force-pushing after review has started | Invalidates review comments; destroys history | Use additional commits during review |
| 7 | Leaving review comments unresponded | Review stalls; reviewer does not know if change was acknowledged | Respond to every comment within the SLA |
| 8 | Database migration not tested in staging | Production lock, data corruption | Always test migrations in staging first | 
| 9 | Merging a hotfix only to `main` without back-porting | `develop` diverges from production; bug reappears in next release | Always back-port hotfixes |
| 10 | IaC PR without `terraform plan` output | Reviewer cannot assess impact | Always include plan output in IaC PRs |
| 11 | Release-close PR without risk evidence | Release date slips or unstable build ships | Defer by default; merge only with Release Risk Note, approval, rollback, and monitoring |
