# validator.technical-docs

- Validator ID: `validator.technical-docs`
- Route: `route.technical-docs`
- Source docs: `ESTD15`, `ESTD0`
- Overlay docs: `ESTD1`, `ESTD10`
- Applies to: TADs, ADRs, runbooks, RCAs, post-mortems, migration plans, ESTD templates, and standards documentation.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Document type and metadata | 15 | `ESTD15`, `ESTD0` | correct template, title, owner, status, dates, audience, lifecycle |
| Goals, scope, and decisions | 15 | `ESTD15`, `ESTD1` | goals, non-goals, context, decision clarity, trade-offs |
| Design, risks, and operations | 20 | `ESTD15`, `ESTD1` | architecture, finalized API contract tables/examples, risks, rollback, monitoring, support impact, security/privacy notes |
| References and traceability | 15 | `ESTD0`, `ESTD15` | source links, ESTD references, section links, dependency clarity |
| Review and approval path | 15 | `ESTD10`, `ESTD15` | reviewers, approvals, exception handling, release-close risk notes, PR evidence |
| Migration and validation evidence | 10 | `ESTD15`, `ESTD16` | test plan, rollout plan, verification, backout, path coverage |
| Formatting and maintainability | 10 | `ESTD0`, `ESTD15` | headings, TOC readiness, concise structure, boilerplate preservation |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Document type and metadata | `static.common.folder-structure` | template completeness |
| Goals, scope, and decisions | None | decision clarity and trade-offs |
| Design, risks, and operations | None | API contract, risk, and operational adequacy |
| References and traceability | `static.common.report-consistency` | reference relevance |
| Review and approval path | `static.common.report-consistency` | approval context |
| Migration and validation evidence | `static.common.report-consistency` | validation adequacy |
| Formatting and maintainability | `static.common.folder-structure` | prose quality |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.technical-docs` before each validator run.
- If document-specific templates split further, update Source docs.
- Keep route binding aligned with `route.technical-docs`.
