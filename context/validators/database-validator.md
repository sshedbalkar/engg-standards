# validator.database

- Validator ID: `validator.database`
- Route: `route.database`
- Source docs: `ESTD9`
- Overlay docs: `ESTD1`, `ESTD4`, `ESTD5`, `ESTD6`, `ESTD7`, `ESTD8`, `ESTD10`, `ESTD14`, `ESTD16`, `ESTD18`
- Applies to: MySQL, MongoDB Atlas, schema design, indexes, queries, migrations, backfills, transactions, retention, backups, and database permissions.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Schema and model design | 15 | `ESTD9`, `ESTD14` | data model fit, naming, contextual collection/map names, data types, ownership, retention readiness |
| Query and access safety | 15 | `ESTD9`, `ESTD6`, `ESTD7` | parameterized access, repository boundaries, transaction use, injection prevention |
| Migrations and backfills | 20 | `ESTD9`, `ESTD10`, `ESTD16` | expand-contract safety, rollback, production-sized validation, path coverage |
| Security and permissions | 15 | `ESTD1`, `ESTD4`, `ESTD8`, `ESTD9` | least privilege, permission boundaries, over-privileged user risk, sensitive data handling, auditability, backup access |
| Performance and operability | 15 | `ESTD5`, `ESTD8`, `ESTD9` | indexes, query plans, locking, replication, monitoring, restore readiness |
| Testing and evidence | 10 | `ESTD9`, `ESTD16`, `ESTD10` | migration tests, staging verification, execution estimates, release-close risk notes, review evidence |
| Folder and config hygiene | 10 | `ESTD18`, `ESTD14` | migration placement, config layering, generated artifact exclusion, naming |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Schema and model design | `static.common.folder-structure` | schema fit and data-model intent |
| Query and access safety | `static.common.semgrep` | repository and transaction intent |
| Migrations and backfills | `static.common.folder-structure` | expand-contract and rollout safety |
| Security and permissions | `static.common.secrets`, `static.common.gitleaks`, `static.common.semgrep` | database permission boundary intent |
| Performance and operability | None | index and query-plan adequacy |
| Testing and evidence | `static.common.report-consistency` | staging evidence quality |
| Folder and config hygiene | `static.common.folder-structure` | naming intent where ambiguous |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.database` before each validator run.
- If MongoDB Atlas or MySQL rules split into dedicated ESTDs, update Source docs.
- Keep route binding aligned with `route.database`.
