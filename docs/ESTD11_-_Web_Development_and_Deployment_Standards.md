# ESTD11 — Web Tools Creation and Deployment Standards

**ESTD11 — Web Tools Creation and Deployment Standards**

| Field | Value |
|:----- |:----- |
| **Document ID** | ESTD11 |
| **Version** | 5.0 |
| **Status** | Active |
| **Last Updated** | 2026-04-13 |
| **Applies To** | All engineers who build or deploy internal web-based tools and dashboards |
| **Depends On** | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers), [ESTD4](./ESTD4_-_Server_Engg_Standards.md#estd4---server-engineering-standards-and-best-practices), [ESTD5](./ESTD5_-_Cloud_Engg_Standards.md#estd5---cloud-engineering-standards-and-best-practices-for-infrastructure-management), [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure), [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds) |
| **Approval** | Director of Engineering |

---

**📋 Living Document Notice** This document is a work in progress and will evolve as our systems, practices, and understanding mature. Feedback, questions, and suggestions are welcome — please submit them via comments on the corresponding Confluence page. However, the standards defined herein **must be strictly followed** in all active work. Any exception requires **explicit written approval** from the Director of Engineering or the appropriate Architect, and must be documented in the PR description, the exception log, or the relevant Confluence page.

---

## How to Use This Document

ESTD11 defines standards for building and deploying internal web-based tools — player management dashboards, content management tools, event configuration interfaces, reporting dashboards, and similar operational tooling. These tools are used by engineers, designers, and operations staff, not by players.

The standards here are written so that even less-experienced engineers can safely deploy tools without causing a production incident or a security breach. Guardrails are embedded into the process, not left as discretionary good practice.

---

## Table of Contents

- [ESTD11 — Web Tools Creation and Deployment Standards](#estd11--web-tools-creation-and-deployment-standards)
  - [How to Use This Document](#how-to-use-this-document)
  - [Table of Contents](#table-of-contents)
  - [1. Purpose and Scope](#1-purpose-and-scope)
  - [2. Why Internal Tools Have the Same Standards as the Product](#2-why-internal-tools-have-the-same-standards-as-the-product)
  - [3. Technology Stack](#3-technology-stack)
  - [4. Web Tools Project Structure](#4-web-tools-project-structure)
  - [5. TypeScript and React Standards](#5-typescript-and-react-standards)
    - [5.1 Strict TypeScript](#51-strict-typescript)
    - [5.2 No `any`](#52-no-any)
    - [5.3 Zod for Runtime Validation](#53-zod-for-runtime-validation)
    - [5.4 Component Design Rules](#54-component-design-rules)
    - [5.5 Naming Conventions](#55-naming-conventions)
  - [6. API Communication](#6-api-communication)
    - [6.1 Centralized API Layer](#61-centralized-api-layer)
    - [6.2 API Client Configuration](#62-api-client-configuration)
  - [7. Authentication and Authorization for Tools](#7-authentication-and-authorization-for-tools)
    - [7.1 All Tool Routes Require Authentication](#71-all-tool-routes-require-authentication)
    - [7.2 Role-Based Access Control](#72-role-based-access-control)
      - [Glossary of tool roles](#glossary-of-tool-roles)
    - [7.3 AWS Cognito Configuration](#73-aws-cognito-configuration)
  - [8. Sensitive Data Handling in Tools](#8-sensitive-data-handling-in-tools)
    - [8.1 Player PII Display](#81-player-pii-display)
    - [8.2 Destructive Actions](#82-destructive-actions)
    - [8.3 Audit Logging for Tool Actions](#83-audit-logging-for-tool-actions)
  - [9. UI and Accessibility Standards](#9-ui-and-accessibility-standards)
    - [9.1 Shared Component Library](#91-shared-component-library)
    - [9.2 Loading and Error States](#92-loading-and-error-states)
    - [9.3 Accessibility](#93-accessibility)
    - [9.4 Text and Localization Readiness](#94-text-and-localization-readiness)
    - [9.5 Destructive Action Confirmation Patterns](#95-destructive-action-confirmation-patterns)
    - [9.6 Before/After Review Pattern](#96-beforeafter-review-pattern)
    - [9.7 Audit Log UI Requirements](#97-audit-log-ui-requirements)
    - [9.8 Session Timeout and Re-authentication](#98-session-timeout-and-re-authentication)
  - [10. Error Handling in Web Tools](#10-error-handling-in-web-tools)
  - [11. Testing Web Tools](#11-testing-web-tools)
    - [11.1 Testing Requirements](#111-testing-requirements)
    - [11.2 Integration Tests](#112-integration-tests)
  - [12. Deployment Architecture](#12-deployment-architecture)
  - [13. Deployment Procedure](#13-deployment-procedure)
    - [13.1 Environments for Tools](#131-environments-for-tools)
    - [13.2 Build and Deploy with Jenkins](#132-build-and-deploy-with-jenkins)
    - [13.3 Standard Deployment Notes](#133-standard-deployment-notes)
    - [13.4 Deployment Timing](#134-deployment-timing)
    - [13.5 Rollback Procedure](#135-rollback-procedure)
  - [14. Cost Control for Web Tools](#14-cost-control-for-web-tools)
  - [15. Monitoring and Incident Response](#15-monitoring-and-incident-response)
  - [16. Common Pitfalls to Avoid](#16-common-pitfalls-to-avoid)
  - [17. Web Tools Code Hygiene](#17-web-tools-code-hygiene)
  - [18. TODO: Add a list of whitelisted libraries for use in the web tools.](#18-todo-add-a-list-of-whitelisted-libraries-for-use-in-the-web-tools)

---

## 1. Purpose and Scope

Web-based internal tools support the live-service operations of both Bingo games. They include:

- **Player Management Dashboard:** View player accounts, handle support actions, apply manual adjustments to coin balances.  
- **Operations Dashboard:** Real-time monitoring of room counts, player counts, and error rates.  
- **Content Management Tool:** Configure periodic content reset parameters, event schedules, and feature flags.  
- **Reporting Dashboard:** View aggregated metrics, revenue summaries, and player funnel data.

These tools interact with production data. A bug or misconfiguration in a tool can have the same impact on players as a bug in the game itself. ESTD11 therefore treats tool development with the same engineering rigor as product development.

---

## 2. Why Internal Tools Have the Same Standards as the Product

**The danger of "it's just an internal tool."** A manual coin balance adjustment made through a poorly validated internal tool will corrupt the player's economy as surely as a bug in the production API. A tool that displays unsanitized player data is an XSS vulnerability. A tool that lacks proper authorization allows any logged-in employee to take destructive actions.

Internal tools are often built quickly, under pressure, and with the assumption that "real engineers will use it, so it doesn't need to be bulletproof." This assumption is consistently wrong. Production incidents caused by internal tools — an operator clicking the wrong button, a tool sending a malformed API request, a tool with no confirmation on a destructive action — are a recurring category of live-service incidents.

**The rules in ESTD1 through ESTD9 apply in full to tool code.** This document adds tool-specific guidance on top of those rules.

---

## 3. Technology Stack

| Layer | Technology |
| :---- | :---- |
| Frontend framework | Next.js (React 18+) |
| Language | TypeScript (strict mode mandatory) |
| UI component library | Shared internal component library (see [§9. UI and Accessibility Standards](#9-ui-and-accessibility-standards) |
| State management | React Query (server state) + Zustand (client UI state) |
| Forms | React Hook Form + Zod validation |
| Styling | Tailwind CSS with the project's design token configuration |
| HTTP client | Axios (through a centralized API service wrapper) |
| Testing | Vitest + React Testing Library |
| Build / bundler | Next.js build (Turbopack for local dev) |
| Deployment | AWS CloudFront + S3 (static export) or AWS ECS/Fargate (SSR when needed) |
| Auth | AWS Cognito + OIDC |

Deviations from this stack require written approval from the Architect or Director of Engineering.

---

## 4. Web Tools Project Structure

```
tool-name/
├── src/
│   ├── app/                    → Next.js App Router pages and layouts
│   │   └── (dashboard)/
│   │       ├── page.tsx
│   │       └── layout.tsx
│   ├── components/
│   │   ├── ui/                 → Pure presentational components (no data fetching)
│   │   └── features/           → Feature-specific composite components
│   ├── hooks/                  → Custom React hooks
│   ├── services/               → API service layer (all HTTP calls live here)
│   ├── store/                  → Zustand stores (UI state only)
│   ├── types/                  → TypeScript type definitions and Zod schemas
│   └── lib/                    → Utilities, constants, helpers
│   └── middleware.ts            → Next.js middleware (auth guard)
├── public/                     → Static assets
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example                → Required env vars documented (no values committed)
├── next.config.ts
├── tailwind.config.ts
└── tsconfig.json
```

---

## 5. TypeScript and React Standards

**Why TypeScript with strict mode matters for tools:** Internal tools are often modified rapidly in response to operational needs. Without strict typing, small changes — renaming an API field, adding a new required parameter — silently break other parts of the tool without compile-time errors. Strict TypeScript catches these at build time rather than at runtime during a production incident response.

### 5.1 Strict TypeScript

`tsconfig.json` must have `"strict": true`. No exceptions.

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### 5.2 No `any`

The `any` type defeats TypeScript's safety guarantees. Use `unknown` when the type is genuinely not known, and narrow it explicitly using Zod:

```ts
// BAD — any propagates silently through the entire call chain
function apiResponseParse(data: any) {
    return data.playerId; // No type safety; crashes at runtime if field is missing
}

// GOOD — Zod validates and narrows at the boundary
function apiResponseParse(data: unknown): PlayerProfile {
    return PlayerProfileSchema.parse(data); // Throws with a clear error if shape is wrong
}
```

### 5.3 Zod for Runtime Validation

All data coming from external sources — API responses, URL parameters, form inputs, localStorage — must be validated with Zod schemas at the point of entry. This is the tool equivalent of server-side input validation ([ESTD1 §11. Input Validation and Sanitization](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#11-input-validation-and-sanitization)).

```ts
const PlayerProfileSchema = z.object({
    playerId:    z.number().int().positive(),
    username:    z.string().min(1).max(64),
    coinBalance: z.number().int(),
    createdAt:   z.string().datetime(),
    isBanned:    z.boolean(),
});

type PlayerProfile = z.infer<typeof PlayerProfileSchema>;

const playerProfileParse = (raw: unknown): PlayerProfile => {
    const result = PlayerProfileSchema.safeParse(raw);
    if (!result.success) {
        logger.error('Unexpected API response shape', { errors: result.error.flatten() });
        throw new ApiResponseShapeError('PlayerProfile', result.error);
    }
    return result.data;
};
```

### 5.4 Component Design Rules

One component per file, with the filename matching the component name. Props must be typed with a named interface or type. No business logic in components — move to custom hooks or service functions. No direct API calls in components — use React Query hooks that call through the service layer. Maximum component file size: 150 lines.

```ts
// BAD — API call directly in component
const PlayerDashboard: React.FC<{ playerId: number }> = ({ playerId }) => {
    const [player, setPlayer] = useState(null);
    useEffect(() => {
        fetch(`/api/players/${playerId}`).then(r => r.json()).then(setPlayer);
    }, [playerId]);
};

// GOOD — API call in service, consumed via React Query hook
const usePlayerProfile = (playerId: number) =>
    useQuery({
        queryKey: ['player', playerId],
        queryFn:  () => playerService.profileGet(playerId),
    });

const PlayerDashboard: React.FC<{ playerId: number }> = ({ playerId }) => {
    const { data: player, isLoading, error } = usePlayerProfile(playerId);
    if (isLoading) return <LoadingSpinner />;
    if (error)     return <ErrorDisplay error={error} />;
    return <PlayerProfileView player={player} />;
};
```

### 5.5 Naming Conventions

| Symbol | Convention | Example |
| :---- | :---- | :---- |
| Component | PascalCase | `PlayerProfileCard` |
| Custom hook | `use` prefix + camelCase | `usePlayerProfile` |
| Service class | PascalCase + `Service` suffix | `PlayerService` |
| Type / Interface | PascalCase | `PlayerProfile`, `ApiResponse<T>` |
| Constants | `UPPER_SNAKE_CASE` | `SEARCH_RESULT_COUNT_MAX` |
| Component files | PascalCase | `PlayerProfileCard.tsx` |
| Hooks, services, utils files | camelCase | `usePlayerProfile.ts` |

---

## 6. API Communication

### 6.1 Centralized API Layer

All HTTP calls must go through a centralized service layer. Components and hooks must never use `fetch` or `axios` directly.

```ts
// src/services/playerService.ts
export const playerService = {
    profileGet: async (playerId: number): Promise<PlayerProfile> => {
        const response = await apiClient.get(`/players/${playerId}`);
        return playerProfileParse(response.data);
    },

    balanceAdjust: async (playerId: number, deltaCoins: number, reason: string): Promise<AdjustBalanceResult> => {
        const response = await apiClient.post(`/players/${playerId}/balance/adjust`, {
            deltaCoins,
            reason,
        });
        return AdjustBalanceResultSchema.parse(response.data);
    },
};
```

### 6.2 API Client Configuration

```ts
// src/lib/apiClient.ts
export const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
    timeout: 10_000,
});

apiClient.interceptors.request.use(config => {
    config.headers['X-Correlation-Id'] = generateUUID();
    return config;
});

apiClient.interceptors.response.use(
    response => response,
    error => {
        if (axios.isAxiosError(error)) {
            const status  = error.response?.status;
            const errCode = error.response?.data?.error?.code ?? 'UNKNOWN';
            throw new ApiError(errCode, status ?? 0, error.message);
        }
        throw error;
    }
);
```

---

## 7. Authentication and Authorization for Tools

**Why tools need strong auth:** Unlike the game client which uses player sessions, internal tools are used by employees who have elevated access to production data. A compromised tool session can expose PII for thousands of players, allow unauthorized coin adjustments, or trigger mass account modifications.

### 7.1 All Tool Routes Require Authentication

Every tool route must be protected by the Next.js middleware auth guard. No page in the tool may be accessible without a valid authenticated session.

```ts
// src/middleware.ts
import { withAuth } from 'next-auth/middleware';

export default withAuth({
    pages: { signIn: '/login' },
});

export const config = {
    matcher: ['/((?!login|_next/static|_next/image|favicon.ico).*)'],
};
```

### 7.2 Role-Based Access Control

| Role | Access |
| :---- | :---- |
| `viewer` | Read-only access to all sections |
| `operator` | Read + standard operational actions (view player, apply support adjustment) |
| `admin` | Full access including destructive actions (ban player, mass data updates) |

#### Glossary of tool roles

| Role | Description |
| :---- | :---- |
| **Engineer** | Builds and maintains the tool; full access where appropriate. |
| **QA Engineer** | Validates game features and tool functionality; may need read access plus test-mode actions. |
| **Designer** | Reviews content presentation; primarily read-only, with configuration access only where explicitly needed. |
| **Producer** | Manages content releases and event schedules; needs configuration and scheduling access. |
| **Product Manager (PM)** | Reviews metrics, KPIs, and player funnel data; primarily read-only dashboards. |
| **Player Service Representative (PSR)** | Handles player support tickets; needs targeted account lookup, read access to player data, and a limited set of pre-approved adjustment actions. |
| **Administrator** | Manages user accounts within the tool, role assignments, and audit log access. |
| **Manager** | Reviews team metrics, approves certain actions such as large coin adjustments, and reads operational dashboards and audit history. |
| **Live Service Operator (LSO)** | Monitors live game health, triggers content resets, manages room events, and needs real-time operations access. |
| **Viewer** | Read-only access to dashboards and reports; cannot modify any data. |

Roles are assigned in AWS Cognito and validated on both the frontend (for UX) and the backend API (for security). Frontend-only RBAC is a UX convenience, not a security measure. Every API call from the tool must be authorized server-side.

### 7.3 AWS Cognito Configuration

MFA must be enforced (TOTP mandatory for `admin` role). The Cognito-hosted UI must be used for login — do not build a custom login form. Access tokens are short-lived (1 hour) and refreshed silently using the refresh token. Token validation on the tool's API backend must verify signature, expiry, issuer, and audience on every request.

---

## 8. Sensitive Data Handling in Tools

### 8.1 Player PII Display

Player PII (email addresses, phone numbers, device identifiers) must be masked by default. The tool must display only partial information (e.g., `m***@e***.com`). A full unmasked view requires a deliberate operator action and must be logged with the operator's user ID and a timestamp.

### 8.2 Destructive Actions

Actions that cannot be easily reversed — banning a player, applying a large coin adjustment, triggering a periodic content reset — must require a confirmation dialog that states exactly what will happen, and the operator must type a confirmation string (such as the player's username or the phrase `CONFIRM`) before submitting. Server-side validation must verify that the requesting user has the required role before executing the action.

```ts
const BanPlayerDialog: React.FC<{ player: PlayerProfile; onConfirm: () => void }> = ({
    player, onConfirm
}) => {
    const [confirmText, setConfirmText] = useState('');
    const isConfirmed = confirmText === player.username;

    return (
        <Dialog>
            <DialogTitle>Ban Player — This cannot be undone</DialogTitle>
            <DialogBody>
                <p>You are about to ban <strong>{player.username}</strong> (ID: {player.playerId}).</p>
                <p>This will immediately end all active sessions and prevent login.</p>
                <p>Type the player's username to confirm:</p>
                <Input value={confirmText} onChange={e => setConfirmText(e.target.value)} />
            </DialogBody>
            <DialogActions>
                <Button variant="destructive" disabled={!isConfirmed} onClick={onConfirm}>
                    Confirm Ban
                </Button>
            </DialogActions>
        </Dialog>
    );
};
```

### 8.3 Audit Logging for Tool Actions

Every state-changing action performed through a tool must be recorded in an audit log. The audit log must include the operator's user ID, the action performed, the target entity (player ID, room ID, etc.), the before and after values where applicable, and the timestamp. This applies to: coin adjustments, account bans/unbans, periodic content reset triggers, and feature flag changes.

---

## 9. UI and Accessibility Standards

All universal UI standards in [ESTD2 §9. Minimum UI Standards for All User Interfaces](./ESTD2_-_General_Client_Engg_Standards.md#9-minimum-ui-standards-for-all-user-interfaces) apply. This section adds web-tool-specific implementation details:

### 9.1 Shared Component Library

All UI must be built using the shared internal component library. Ad-hoc one-off component implementations for common patterns (buttons, inputs, dialogs, tables) are not acceptable. If the library is missing a needed component, add it to the library first and have it reviewed before use.

### 9.2 Loading and Error States

Every asynchronous operation must display loading, success, and error states. React Query's `isLoading` and `error` states make this straightforward — there is no acceptable reason to omit them.

### 9.3 Accessibility

Minimum requirements that apply regardless of the tool's audience: all interactive elements must have accessible labels; keyboard navigation must be fully functional; color contrast must meet WCAG 2.1 AA (4.5:1 for body text). These requirements exist because operators use tools under time pressure, often in poor lighting conditions.

### 9.4 Text and Localization Readiness

Do not hardcode operator-facing English strings inside components, hooks, or service code. Labels, button text, confirmation prompts, validation copy, and error messages must come from the tool's shared message or localization layer, even if English is the only shipped locale today. This keeps terminology consistent, enables future localization, and prevents partial untranslated experiences.

### 9.5 Destructive Action Confirmation Patterns

Web tools must implement the multi-step confirmation flow defined in [ESTD2 §9.3](./ESTD2_-_General_Client_Engg_Standards.md#93-destructive-sensitive-and-high-impact-actions) using the shared `ConfirmationDialog` component. For high-risk actions (player bans, bulk coin adjustments, content resets, feature flag changes), the dialog must require the operator to type a confirmation phrase such as `DELETE 23 PLAYERS` before the submit button becomes active. The confirmation component must accept a `reasonRequired` prop; when true, a free-text or reason-code field is mandatory before submission. Bulk operations must cap direct player-account actions at 100 accounts per operation; above that threshold, the tool must require elevated approval or a separate workflow.

### 9.6 Before/After Review Pattern

All write operations on live content or player-affecting data must present a before/after diff view before submission. Use the shared `ChangeReviewTable` component. Changed fields must be visually highlighted with the previous value crossed out and the new value emphasized. The review step must be non-dismissable — the user cannot skip it. Example:

| Field | Before | After |
|:------|:-------|:------|
| Weekly bonus amount | 100 | 150 |
| Feature flag status | Off | On |
| Event end date | 2026-03-24 18:00 UTC | 2026-03-25 18:00 UTC |

### 9.7 Audit Log UI Requirements

Every web tool must expose an audit log view accessible to Administrators and Managers. The view must support filtering by user, date range, and action type. Audit log entries must never be deletable through the UI, even by administrators. The UI must provide an export function for compliance or incident review. See [ESTD2 §9.5 Change Tracking and Audit Trail](./ESTD2_-_General_Client_Engg_Standards.md#95-change-tracking-and-audit-trail) for the minimum audit log payload requirements.

### 9.8 Session Timeout and Re-authentication

Tool sessions must expire after 30 minutes of inactivity. The session expiry must trigger a modal re-authentication prompt — not a silent redirect that discards unsaved form state. The re-authentication flow must preserve the user's current page and any in-progress form data. For admin-level actions and bulk-destructive actions, re-authentication must be required even if the session is still active. Implement this using the shared `SessionGuard` component.

---

## 10. Error Handling in Web Tools

All [ESTD1 §9. Error Handling and Try-Catch Usage](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#9-error-handling-and-try-catch-usage) error handling rules apply. Tool-specific additional rules:

Error responses from the API must never be shown verbatim to the operator in their raw JSON form. All errors must be presented through a standardized `ErrorDisplay` component that formats the `error.code` and `error.message` fields from the standard API envelope ([ESTD4 §4.4 Request & Response Structure](./ESTD4_-_Server_Engg_Standards.md#44-request--response-structure)).

Network errors (timeouts, connection refused) must display a specific "Cannot connect to server" message, separate from API-level errors (4xx, 5xx responses).

Validation errors from form submission must be displayed inline next to the relevant field, not in a generic banner.

---

## 11. Testing Web Tools

### 11.1 Testing Requirements

**Refer [ESTD16](./ESTD16_-_Paths_And_Unit_Testing_Strategy.md#estd16---paths-branches-and-unit-testing-strategy) for the full documentation on Paths, and Unit testing Strategies.**

Unit tests are mandatory for all service functions and custom hooks. The minimum coverage target is 80% for service and hook code. UI component tests must cover: the loading state renders correctly, the error state renders correctly, and key user interactions trigger the correct service calls.

### 11.2 Integration Tests

Integration tests must cover the full flow of each critical tool action: the operator performs an action, the tool calls the API service, and the result is displayed correctly. Use `msw` (Mock Service Worker) to mock API responses in integration tests without requiring a live backend.

```ts
// Example: test that BanPlayerDialog requires confirmation text
import { render, screen, fireEvent } from '@testing-library/react';
import { BanPlayerDialog } from './BanPlayerDialog';

test('ban confirmation button is disabled until username is typed', () => {
    const player = { playerId: 1, username: 'testplayer', coinBalance: 1000 };
    const onConfirm = vi.fn();

    render(<BanPlayerDialog player={player} onConfirm={onConfirm} />);

    const button = screen.getByRole('button', { name: /Confirm Ban/ });
    expect(button).toBeDisabled();

    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'testplayer' } });
    expect(button).not.toBeDisabled();

    fireEvent.click(button);
    expect(onConfirm).toHaveBeenCalledOnce();
});
```

---

## 12. Deployment Architecture

Internal tools are deployed on AWS infrastructure as defined in [ESTD8](./ESTD8_-_AWS_Standards.md#estd8---aws-standards-document-for-bingo-game-infrastructure). The standard deployment pattern for a static Next.js export is:

```
Operator's Browser
       │ HTTPS
       ▼
CloudFront Distribution
       │ (cached static assets)
       ▼
S3 Bucket (static Next.js export)
       │ (API calls bypass CloudFront)
       ▼
ALB (internal, not internet-facing)
       │
       ▼
PHP API / Java API (same backends as the game)
```

If the tool uses Server-Side Rendering (SSR), it is deployed as a Fargate task behind an internal ALB. The ALB must not be internet-facing — access must be restricted to the engineering team's office IP range or VPN.

**All internal tools must be deployed to a URL that is not guessable or discoverable.** Tools must not be indexed by search engines (`robots.txt` must disallow all crawlers, and `X-Robots-Tag: noindex` must be set on all responses).

---

## 13. Deployment Procedure

### 13.1 Environments for Tools

Internal tools follow the same 4-environment promotion path as the main game ([ESTD5 §3. Environment Strategy](./ESTD5_-_Cloud_Engg_Standards.md#3-environment-strategy)):

```
dev → qa → staging → production
```

However, the staging tool environment connects to the staging game environment (not production). The production tool environment is the only environment that connects to the production game API.

### 13.2 Build and Deploy with Jenkins

The team uses Jenkins for all Unity client builds and for web tools builds. Jenkins provides the automation backbone that enforces build promotion policy ([ESTD1 §24.5 Build Promotion Policy](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#245-build-promotion-policy)) — no build may skip an environment stage.

Web tool deployments follow this Jenkins pipeline:

```
┌───────────────────────────────────────────────────────────────────────────┐
│  Git push to feature branch                                               │
│         │                                                                 │
│         ▼                                                                 │
│  Jenkins: PR Build                                                        │
│    - npm ci / npm run build                                               │
│    - ESLint + TypeScript type-check                                       │
│    - Unit tests (Jest)                                                    │
│    - Bundle size check (fail if > configured limit)                       │
│         │                                                                 │
│         ▼  (merge to develop)                                             │
│  Jenkins: Deploy to Dev                                                   │
│    - Build production artifact                                            │
│    - Upload to S3 (dev bucket)                                            │
│    - Invalidate CloudFront cache                                          │
│    - Smoke test against dev API                                           │
│         │                                                                 │
│         ▼  (QA sign-off)                                                  │
│  Jenkins: Promote to QA / Staging / Production                            │
│    - Re-use same artifact (no rebuild)                                    │
│    - Deploy to target environment S3                                      │
│    - Invalidate CloudFront cache                                          │
│    - Run automated smoke tests                                            │
│    - Notify Slack channel                                                 │
└───────────────────────────────────────────────────────────────────────────┘
```

Full Jenkins standards are defined in [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds). ESTD11 requires that all web tool CI/CD pipelines comply with [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds).

Key web-tools-specific Jenkins requirements:

- Jenkins pipelines are defined as `Jenkinsfile` committed to the tool's repository root.  
- No manual deployments — all environment promotions go through the Jenkins pipeline.  
- The production deployment stage requires a manual approval gate in Jenkins (`input` step).  
- Build artifacts (the compiled Next.js export) are stored in S3 with the build version as a key prefix, enabling instant rollback by switching the CloudFront origin path.

See [ESTD13](./ESTD13_-_Jenkins_CI_CD_Standards.md#estd13--jenkins-cicd-standards-for-unity-and-web-tool-builds) for the full Jenkins standards.

### 13.3 Standard Deployment Notes

Tool deployments are automated via the Jenkins CI/CD pipeline ([ESTD13 §9. Environment Promotion and Deployment Gates](./ESTD13_-_Jenkins_CI_CD_Standards.md#9-environment-promotion-and-deployment-gates)). No manual deployments to production. The deploy script must:

1. Run `npm ci`, then `npm run build`, and verify zero TypeScript errors, zero ESLint errors, and all tests pass.  
2. Upload the static export (or container image for SSR) to the appropriate environment target.  
3. Invalidate the CloudFront cache for the affected paths.  
4. Verify the deployment by loading the tool in a browser and confirming the version indicator shows the new build version.

### 13.4 Deployment Timing

Tool deployments should avoid the Monday morning periodic content reset window. A tool that deploys incorrectly during a periodic content reset — when operators are actively using the tool to manage the reset — can make a difficult situation significantly worse. Preferred deployment window for production tools: Tuesday through Thursday, 10:00–15:00 IST (which is 23:30–04:30 US Eastern, i.e., US off-peak hours).

### 13.5 Rollback Procedure

Every tool deployment must support rollback to the last known good artifact **without rebuilding from source**. The Jenkins pipeline must retain at least the current and previous production artifacts.

Minimum rollback procedure:

1. select the previously approved artifact;
2. redeploy it (or repoint the CloudFront origin path / SSR image tag) without modifying source;
3. invalidate caches if applicable;
4. run smoke checks against the tool and the target API environment;
5. post the rollback note in the relevant engineering/ops channel.

If a backend contract or data migration prevents a clean UI rollback, that coupling must be treated as a release-planning defect and documented before the next release.

---

## 14. Cost Control for Web Tools

Internal tools should be as cost-efficient as possible. Practical guidelines:

Static exports (CloudFront + S3) are preferred over SSR (Fargate) when possible. Static deployment for a typical internal tool costs less than $5/month; Fargate for a continuously running SSR service costs significantly more.

Tool environments that are not actively used (e.g., the QA environment between release cycles) should be paused or destroyed and rebuilt on demand using IaC, rather than running continuously.

Set CloudWatch billing alarms for tool deployments at $20/month per environment to detect runaway costs early.

---

## 15. Monitoring and Incident Response

Every production tool deployment must have:

- A CloudWatch log group receiving access logs from the ALB and application logs from the tool backend (if SSR).  
- A CloudWatch alarm on 5xx error rate > 1% over 5 minutes.  
- An alarm on 4xx error rate > 10% over 5 minutes (high 4xx rate from a tool often indicates an auth misconfiguration or API contract break).

A broken internal tool during a live operational event (periodic content reset, promotional event launch) is a P2 incident. The on-call engineer must be notified immediately. The tool's relevant service owner is responsible for acknowledgement within 15 minutes.

---

## 16. Common Pitfalls to Avoid

| # | Pitfall | Impact | Remedy |
| :---- | :---- | :---- | :---- |
| 1 | "It's just an internal tool" mindset | Production data corruption, security breaches | Apply full ESTD standards to all tool code |
| 2 | No confirmation on destructive actions | Operators accidentally ban players or corrupt balances | Require typed confirmation for irreversible actions |
| 3 | Frontend-only RBAC | Any logged-in user can call unauthorized API endpoints | Validate roles server-side on every API call |
| 4 | Raw API error messages displayed to operator | Confusing UX; potential internal info leakage | Always display through a standardized error component |
| 5 | Displaying unmasked PII by default | Privacy violation; regulatory risk | Mask PII by default; require deliberate action to unmask |
| 6 | Tool connecting to production API from staging | Staging tool actions affect live players | Strictly separate environment configurations |
| 7 | No audit log for tool actions | Cannot investigate who made a change | Log every state-changing action with operator ID and timestamp |
| 8 | Direct API calls in React components | Untestable, scattered; breaks on API changes | All API calls through the centralized service layer |
| 9 | Tool accessible from the internet | Unauthorized access to player data | Restrict ALB to corporate IP range or VPN |
| 10 | Deploying tool during periodic content reset window | Broken tool during high-stakes operational period | Follow the deployment timing guidelines in [§13.4 Deployment Timing](#134-deployment-timing) |

---

## 17. Web Tools Code Hygiene

Code hygiene for web tools follows the same principles as all other domains ([ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers)). The following cross-references identify hygiene imperatives specific to the web tools stack.

| Hygiene Practice | Standard Reference |
| :---- | :---- |
| TypeScript strict mode — no `any` types | [§5.1 Strict TypeScript](#51-strict-typescript), [§5.2 No `any`](#52-no-any) of this document |
| Zod validation on all external data | [§5.3 Zod for Runtime Validation](#53-zod-for-runtime-validation) of this document |
| No direct API calls in components — always through service layer | [§5.4 Component Design Rules](#54-component-design-rules) of this document |
| Maximum 150 lines per component file | [§5.4 Component Design Rules](#54-component-design-rules) of this document |
| Audit log on every write operation | [§8.3 Audit Logging for Tool Actions](#83-audit-logging-for-tool-actions) of this document |
| Role-based access enforced server-side on every API call | [§7. Authentication and Authorization for Tools](#7-authentication-and-authorization-for-tools) of this document |
| `npm ci` in CI — never `npm install` | [ESTD13 §8.2 `npm ci` Is Mandatory](./ESTD13_-_Jenkins_CI_CD_Standards.md#82-npm-ci-is-mandatory) |
| Dead feature flags cleaned up within 2 sprints | [ESTD1 §13.6 Feature Flag Lifecycle and Cleanup](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#136-feature-flag-lifecycle-and-cleanup) |
| No hardcoded English strings — i18n-ready labels | [§9.4 Text and Localization Readiness](#94-text-and-localization-readiness) of this document |
| Loading, success, and error states on every async action | [§10. Error Handling in Web Tools](#10-error-handling-in-web-tools) of this document |
| All destructive actions require two-step confirmation | [ESTD2 §9.3 Destructive, Sensitive, and High-Impact Actions](./ESTD2_-_General_Client_Engg_Standards.md#93-destructive-sensitive-and-high-impact-actions) and [ESTD2 §9.4 Preventing Unintended Changes](./ESTD2_-_General_Client_Engg_Standards.md#94-preventing-unintended-changes) |

---

## 18. TODO: Add a list of whitelisted libraries for use in the web tools.
