# Repo Map

## Lookup Strategy
- primary_lookup: section + stable_path_or_unit_id
- ordering: fixed_framework_sections_first, repo_native_within_section
- jump_index: present
- entry_id_format: repo-native path or stable lowercase kebab-case

## Jump Index
- source-truth
- shared-context
- current-inventory
- edit-workflow
- validation
- drop-in-enforcement
- doc-dependency-summary
- when-to-open-what

## Source Truth

- `docs/`: authoritative ESTD documents
- `README.md`: current published doc list
- `AGENTS.md`: bootstrap rules and context routing
- `scripts/generate-toc.sh`: heading TOC maintenance
- `scripts/link-estd-references.sh`: `[[...]]` link resolution
- `scripts/check-context.sh`: context consistency validation
- `scripts/LLM_SHELL_SCRIPT_STYLE_GUIDE.md`: shell script conventions
- `scripts/LLM_NON_SHELL_SCRIPT_STYLE_GUIDE.md`: non-shell script conventions
- `tools/estd-enforcer/`: drop-in static-first hybrid standards gate kit
- `context/validators/static-validation.md`: static validation inventory
- `context/validators/llm-based-validation.md`: LLM gap-review inventory

This file owns current inventory, dependency summary, and script usage overview.

## Shared Context

- tracked shared memory: `context/`
- local private memory: `CLAUDE.md`
- local prompt helpers: `prompts/`

## Current Inventory

- ESTD doc count: 20
- Latest ESTD ID in repo: ESTD19
- Next available ESTD ID: ESTD20

## Edit Workflow

1. Read `AGENTS.md`.
2. Read `context/llm-operating-guide.md`.
3. Read this map and relevant cards from `context/doc-cards.md`.
4. Read target doc plus direct parent/sibling docs only.
5. Edit target file.
6. After ESTD doc create/update/rename/repurpose, refresh impacted context:
   - `context/doc-cards.md`: doc added/removed/renamed/repurposed or purpose/audience/overlap/read-order changed.
   - `context/repo-map.md`: inventory, dependencies, script usage, or `When To Open What` changed.
   - `context/estd-routing-map.md`: route coverage, trigger keywords, primary docs, or validator facets changed.
   - `context/validators/`: source docs, check groups, weights, static coverage, or evolution rules changed.
   - `context/validators/static-validation.md`: static check registry, built-in static behavior, or Static Coverage tables changed.
   - `context/validators/llm-based-validation.md`: validator groups, LLM gaps, report schema, or LLM request behavior changed.
7. Run `./scripts/generate-toc.sh <file>` after heading changes.
8. Run `./scripts/link-estd-references.sh <file> docs/` after adding `[[...]]` refs.
9. Run `./scripts/check-context.sh` after context, validator, or doc inventory changes.
10. If reusable repo fact learned, update shared memory. If temporary only, use `CLAUDE.md`.

## Validation

- Fast context proof: `./scripts/check-context.sh`
- Script syntax proof after checker edits: `bash -n scripts/check-context.sh`
- Diff hygiene proof: `git diff --check`

## Drop-In Enforcement

- Consumer repos use `tools/estd-enforcer/bin/estd-enforce` through a submodule checkout.
- Repos without the configured ESTD submodule are out of enforcement scope.
- The enforcer runs static checks first, then LLM review only for unresolved gaps.
- The enforcer reads `context/estd-routing-map.md`, `context/validators/`, static registry, and source ESTD docs.
- Static and LLM validation inventories live in `context/validators/static-validation.md` and `context/validators/llm-based-validation.md`.
- Current enforcement is developer/LLM-run; blocking CI is a future rollout phase.
- Future CI should archive `build/estd/report.json` and `build/estd/report.md`.

## Doc Dependency Summary

```text
ESTD1 root
client: ESTD2 -> ESTD3
server: ESTD4 -> ESTD6, ESTD7, ESTD9, ESTD12
cloud: ESTD5 -> ESTD8
process: ESTD10 depends on ESTD1-ESTD13
web tools: ESTD11 depends on ESTD1, ESTD4, ESTD5, ESTD8, ESTD13
ci/cd: ESTD13 depends on ESTD1, ESTD5, ESTD8, ESTD11
standalone: ESTD14, ESTD16, ESTD17
folder structure: ESTD18 cross-refs stack docs
coupling: ESTD19 depends on ESTD1
```

## When To Open What

| Need | Open First | Then Open |
|:-----|:-----------|:----------|
| any ESTD change | `AGENTS.md`, `context/llm-operating-guide.md` | target doc, direct parents |
| new ESTD doc authoring | `docs/ESTD0_-_Markdown_format.md`, `AGENTS.md` | `README.md`, nearest parent standards |
| client standards | `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD2_-_General_Client_Engg_Standards.md` | `docs/ESTD3_-_Unity_and_C%23_Standards.md` if C#/Unity |
| server standards | `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD4_-_Server_Engg_Standards.md` | `docs/ESTD6_-_PHP_Programming_Standards.md`, `docs/ESTD7_-_Java_Programming_Standards.md`, `docs/ESTD9_-_Database_Standards.md`, `docs/ESTD12_-_Smartfox_Server_Standards.md` |
| cloud / aws | `docs/ESTD5_-_Cloud_Engg_Standards.md` | `docs/ESTD8_-_AWS_Standards.md`, `docs/ESTD13_-_Jenkins_CI_CD_Standards.md` |
| web tools | `docs/ESTD1_-_Common_Engg_Standards_And_Best_Practices.md`, `docs/ESTD11_-_Web_Development_and_Deployment_Standards.md` | `docs/ESTD13_-_Jenkins_CI_CD_Standards.md`, `docs/ESTD8_-_AWS_Standards.md` |
| naming | `docs/ESTD14_-_Hierarchical_Naming_Strategy_for_Programming_Entities.md` | direct stack standard using the names |
| testing / paths / branches | `docs/ESTD16_-_Paths_And_Unit_Testing_Strategy.md` | owning stack standard |
| doc templates | `docs/ESTD15_-_Technical_Document_Guide_and_Template.md` | related standards or runbooks |
| validator inventory | `context/validators/README.md` | `context/validators/static-validation.md`, `context/validators/llm-based-validation.md` |
