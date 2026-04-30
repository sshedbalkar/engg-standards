# validator.internal-scripts

- Validator ID: `validator.internal-scripts`
- Route: `route.internal-scripts`
- Source docs: `ESTD1`, `ESTD16`, `ESTD18`
- Overlay docs: `ESTD10`, `ESTD14`, `ESTD17`, `ESTD19`
- Applies to: shell scripts, Python CLIs, local automation, maintenance scripts, data processors, backfill utilities, and repo helper tooling.
- Pass threshold: > 75% code conformity.

## Scoring

Use the shared scoring contract in `context/validators/README.md`.

## Check Groups

| Group | Weight | ESTD Sources | Validator Focus |
|:------|------:|:-------------|:----------------|
| Guide selection and entrypoints | 15 | `ESTD1`, `ESTD18` | shell or non-shell guide evidence, clear purpose, file placement, executable boundaries, generated artifact exclusion |
| Input validation and safe mutation | 15 | `ESTD1`, `ESTD16` | required args, safe defaults, destructive-action guards, parameter validation, shell quoting, strict mode, temp files, traps, cleanup |
| External adapters and command boundaries | 15 | `ESTD1`, `ESTD17` | API adapters, shell external tools, dependency checks, timeouts, bounded output, redacted diagnostics, no secret logging |
| Modularity and data flow | 20 | `ESTD17`, `ESTD19` | modularity threshold, pure logic versus I/O, no large script growth without review or structure-debt note, staged processing, restartability |
| Testing and repeatable checks | 15 | `ESTD16` | happy/sad/edge paths, dry-run coverage, mocked adapters, fixture use, repeatable checks |
| Naming and discoverability | 10 | `ESTD14`, `ESTD18` | command names, folder names, config names, contextual collection/map names, README links |
| Closeout and operational evidence | 10 | `ESTD10` | guide consulted, tests and checks run, remaining structure debt, review evidence, rollback notes, exception approval, runbook impact |

## Static Coverage

| Group | Static Check IDs | LLM Gap |
|:------|:-----------------|:--------|
| Guide selection and entrypoints | `static.common.folder-structure`, `static.common.semgrep` | guide-specific compliance and command ergonomics |
| Input validation and safe mutation | `static.common.semgrep` | destructive-action and safe mutation intent |
| External adapters and command boundaries | `static.common.semgrep` | adapter and external tool boundary clarity |
| Modularity and data flow | `static.common.semgrep` | modularity threshold and structure debt |
| Testing and repeatable checks | `static.common.report-consistency` | path intent and coverage adequacy |
| Naming and discoverability | `static.common.folder-structure` | naming clarity |
| Closeout and operational evidence | `static.common.report-consistency` | closeout proof and rollback evidence |

## LLM Gap Review

Use `context/validators/llm-based-validation.md` for unresolved semantic gaps.

## Evolution Rules

- Re-resolve `route.internal-scripts` before each validator run.
- If a dedicated scripting ESTD is added, make it a Source ESTD doc and rebalance groups.
- Keep route binding aligned with `route.internal-scripts`.
