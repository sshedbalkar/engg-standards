# ESTD0 - Markdown format for all technical documents

**Document Title**

| Field | Value |
|:------|:------|
| Document ID | ESTD*N* |
| Version | 1.1 |
| Status | Active / Draft / Deprecated / Superseded |
| Last Updated | 2026-04-27 |
| Applies To | Type of target engineers — client, server, website, tools, automation, or a combination of them |
| Depends On | *ESTD or any other document id / Title* |
| Approval | Director of Engineering |

---

> **📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborums. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.

---

## Table of Contents

- [ESTD Document Heading](#estd-document-heading)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Section](#2-section)
    - [2.1 Sub-section](#21-sub-section)
    - [2.2 Sub-section](#22-sub-section)
    - [2.3 Link Examples](#23-link-examples)

---

## 1. Purpose and Scope

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---

## 2. Section

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### 2.1 Sub-section

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### 2.2 Sub-section

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### 2.3 Link Examples

Use same-document links for sections in the current file:

- [Jump to Purpose](#1-purpose-and-scope)

Use cross-document links for sections in other ESTD files:

- [ESTD1 §10](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#10-boundary-functions)

Use resolver syntax when drafting ESTD references:

- `[[§1]]` links to a section in the current document.
- `[[ESTD1]]` links to another ESTD document.
- `[[ESTD1 §10]]` links to a section in another ESTD document.

Use normal Markdown links for external URLs:

- [Link text](https://www.markdownlang.com)

Resolve `[[...]]` references before committing:

```bash
./scripts/link-estd-references.sh <file> docs/
```

**Bold text**
*Italics*
***Bold and Italics***
[Link text](https://www.markdownlang.com)
[Jump to Anchor](#heading-name)

Unordered List
- Item 1
- *Item 2*
- **Item 3**
- ***Item 4*** Item description

Ordered List
1. Item 1
2. *Item 2*
3. **Item 3**
4. ***Item 4*** Item description

> Quoted Text

`this is inline code`

> **Block Quote** Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor

```java
// GOOD — meaningful recovery at the entry boundary
public Response rewardClaim(Request request) {
    try {
        RewardClaimResult result = rewardService.claim(request.getPlayerId(), request.getRewardId());
        return Response.ok(result);
    } catch (RewardAlreadyClaimedException e) {
        // Expected business condition — return structured error, not a 500
        return Response.conflict("REWARD_ALREADY_CLAIMED", e.getMessage());
    } catch (PlayerNotFoundException e) {
        logger.warn("Player not found during reward claim", Map.of("playerId", request.getPlayerId()));
        return Response.notFound("PLAYER_NOT_FOUND");
    } catch (Exception e) {
        // Final safety net — log everything, return generic 500
        logger.error("Unexpected error during reward claim", e);
        return Response.internalError("INTERNAL_ERROR");
    }
}
```

**Table**

| # | Col 1 | Col 2 | Col 3 | Col 4 |
|:--|:-----:|------:|------:|:------|
| 1 | **Center justified Val 1** | Right justified Val 2 | *Right justified Val 3* | Left justified Val 7 |
| 2 | ***Center justified Val 4*** | Right justified Val 5 | Right justified Val 6 | Left justified Val 8 |
