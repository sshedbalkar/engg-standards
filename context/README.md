# ESTD Context Memory Contract

## Purpose

Shared memory for ESTD work.

- Repo truth stays in `docs/`, repo scripts, `README.md`, and `AGENTS.md`.
- `context/` stores compact retrieval aids only.
- `context/` never replaces source docs.

## File Inventory

| File | Role | Update When |
|:-----|:-----|:------------|
| `context/README.md` | Memory contract, file inventory, size rules | contract or inventory changes |
| `context/llm-operating-guide.md` | LLM operating flow | retrieval or closeout workflow changes |
| `context/repo-map.md` | Compact repo topology and edit workflow | repo layout, scripts, or doc inventory changes |
| `context/doc-cards.md` | One compact card per ESTD doc | any ESTD doc added, removed, renamed, or repurposed |
| `context/estd-routing-map.md` | Engineering field routes for LLMs and validators | route coverage or validation facets change |
| `context/validators/` | Route-bound validator specs | validator coverage, scoring, or source ESTD docs change |
| `context/validators/static-validation.md` | Static validator inventory | static registry, built-in static behavior, or Static Coverage tables change |
| `context/validators/llm-based-validation.md` | LLM gap-review inventory | validator groups, LLM gaps, report schema, or LLM request behavior change |
| `tools/estd-enforcer/` | Drop-in static-first hybrid standards gate kit | CLI, static checks, schema, prompts, or installer contract changes |
| `context/decision-log.md` | Durable structural decisions | memory-system decisions become reusable |
| `context/open-work.md` | Active memory-system gaps only | gap opens, changes, or closes |

## Size Discipline

- `context/README.md`: keep under 120 lines.
- `context/llm-operating-guide.md`: keep under 80 lines.
- `context/repo-map.md`: keep readable in one pass.
- `context/doc-cards.md`: one compact card per ESTD doc; no long prose.
- `context/estd-routing-map.md`: route fields and facets only; no copied rules.
- `context/validators/`: compact validator specs only; scoring and routing, no rule copies.
- `context/validators/static-validation.md` and `context/validators/llm-based-validation.md`: validation inventories, no copied ESTD rules.
- `tools/estd-enforcer/`: CLI, static check registry, prompts, schema, examples, and tests; no copied ESTD rule text.
- `context/decision-log.md`: append concise rows only.
- `context/open-work.md`: active items only; remove resolved rows fast.

## Update Rules

- Update shared context only for reusable repo facts.
- Point durable memory back to a repo file, script, or approved plan.
- Do not copy chat transcripts into shared context.
- Put temporary or tool-specific notes in `CLAUDE.md`, not here.
- When editing `AGENTS.md`, `CLAUDE.md`, or `context/*.md`, keep only hard rules, routing, durable retrieval aids, or tool-local behavior. Remove duplicated or easy-to-derive info. Prefer terse, grammar-light bullets.
- Do not keep conflicting rules in the same applicable scope. If a rule is local, exceptional, or narrower than another rule, state that scope explicitly.
- Prefer editing an existing entry over adding duplicate guidance.
- Before editing shared cache files, read their `## Lookup Strategy`, preserve declared ordering, and refresh `## Jump Index`.

## Read Order

For new ESTD tasks:

1. Read [AGENTS.md](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/AGENTS.md).
2. Read [context/llm-operating-guide.md](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/context/llm-operating-guide.md).
3. Read [context/repo-map.md](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/context/repo-map.md).
4. Read only relevant cards in [context/doc-cards.md](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/context/doc-cards.md).
5. Read target ESTD docs and only directly related docs.

For validator route selection, read [context/estd-routing-map.md](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/context/estd-routing-map.md) after step 3.
For validator execution, read the matching spec in [context/validators/](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/context/validators/) after route selection.
For validator inventory, read [context/validators/static-validation.md](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/context/validators/static-validation.md) or [context/validators/llm-based-validation.md](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/context/validators/llm-based-validation.md).
For drop-in enforcement, use [tools/estd-enforcer/](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/tools/estd-enforcer/).

## Validation

Run `./scripts/check-context.sh` after changing shared context files or when the ESTD doc inventory changes.
