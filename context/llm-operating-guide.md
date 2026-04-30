# ESTD LLM Operating Guide

## Core

- Repo truth first.
- Memory = summary, not source.
- No transcript dump.
- Source link back always.
- No unrelated read unless scope widen.
- Baseline now. improve later. 

## Read Order

1. [AGENTS.md](/Users/santosh/WorkWork/Scopely/Repositories/bingo-bash-standards/AGENTS.md)
2. `context/README.md`
3. `context/repo-map.md`
4. needed part from `context/doc-cards.md`
5. target ESTD doc
6. direct related docs only

Scope widen only for:
- dependency effect
- script/workflow verify
- cross-ref fix
- shared structure / naming / index / workflow change

## Closeout

- ESTD doc changed -> doc-cards / repo-map / routing / validators if applicable, then `./scripts/check-context.sh`
- script changed -> cite shell/non-shell guide, tests/checks run, structure debt if any
- script grows adapters/parsing/orchestration in one file -> route `validator.internal-scripts`
- reusable fact -> `context/doc-cards.md` or `context/decision-log.md`
- open gap -> `context/open-work.md`
- tiny universal lesson -> `AGENTS.md`
- temp personal note -> `CLAUDE.md`

## Files

- `AGENTS.md`: bootstrap rules + routing + tiny lessons
- `CLAUDE.md`: local scratch
- `context/README.md`: memory contract
- `context/repo-map.md`: repo map
- `context/doc-cards.md`: fast doc lookup
- `context/decision-log.md`: durable decisions
- `context/open-work.md`: active gaps only
- `scripts/check-context.sh`: read-only context check

## Refine Later

Keep only improvement that repeat-help future work, stay stable, not fight repo truth. Don't repeat and must sacrifice grammar.

Pattern:
- `date | discovery | workflow tweak | reason`
