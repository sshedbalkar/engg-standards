# Decision Log

| Date | Decision | Affected Nodes | Source References |
|:-----|:---------|:---------------|:------------------|
| 2026-04-24 | Use hybrid ESTD memory: repo truth + tracked shared context + local private notes. | `AGENTS.md`, `CLAUDE.md`, `context/README.md`, `context/repo-map.md`, `context/doc-cards.md`, `context/decision-log.md`, `context/open-work.md` | `AGENTS.md`, `context/README.md` |
| 2026-04-24 | Keep `AGENTS.md` as universal bootstrap. Keep task scratch out of tracked shared memory. | `AGENTS.md`, `context/README.md`, `context/llm-operating-guide.md` | `AGENTS.md`, `context/llm-operating-guide.md` |
| 2026-04-24 | Store LLM operating flow in `context/llm-operating-guide.md`, not inside transient planning notes. | `context/llm-operating-guide.md`, `context/README.md` | `context/README.md`, `context/llm-operating-guide.md` |
| 2026-04-24 | Keep `prompts/` local-only and untracked; shared repo context must stay durable and cross-tool. | `prompts/task_bootstrap.txt`, `prompts/task_closeout.txt`, `prompts/handoff.txt`, `context/README.md` | `.gitignore`, `context/README.md` |
| 2026-04-24 | Validate shared memory drift with a read-only shell script instead of manual spot checks only. | `scripts/check-context.sh`, `context/doc-cards.md`, `context/open-work.md`, `context/decision-log.md`, `context/repo-map.md` | `scripts/LLM_SHELL_SCRIPT_STYLE_GUIDE.md`, `context/README.md` |
| 2026-04-25 | Store validator routing as compact Markdown: route IDs, ESTD IDs, facets, no copied rules. | `context/estd-routing-map.md`, `context/README.md` | `context/estd-routing-map.md`, `context/README.md` |
| 2026-04-25 | Store validator specs under `context/validators/` with > 75% conformity threshold and route bindings. | `context/validators/`, `context/README.md`, `scripts/check-context.sh` | `context/validators/README.md`, `context/estd-routing-map.md` |
| 2026-04-25 | Package LLM standards enforcement as a submodule-consumed CLI gate. | `tools/estd-enforcer/`, `context/validators/`, `scripts/check-context.sh` | `tools/estd-enforcer/README.md`, `context/validators/README.md` |
| 2026-04-25 | Prefer static validators first; use LLM only for unresolved semantic gaps. | `tools/estd-enforcer/`, `context/validators/` | `tools/estd-enforcer/README.md`, `context/validators/README.md` |
| 2026-04-25 | Apply ESTD enforcement only to repos opted in by configured submodule; keep CI blocking future. | `tools/estd-enforcer/`, `context/repo-map.md` | `tools/estd-enforcer/README.md`, `context/repo-map.md` |
| 2026-04-27 | Maintain separate static and LLM validation inventory docs, checked by context validation. | `context/validators/static-validation.md`, `context/validators/llm-based-validation.md`, `scripts/check-context.sh` | `context/validators/README.md`, `tools/estd-enforcer/README.md` |
| 2026-04-30 | Adopt framework lookup schema for shared cache files. | `context/repo-map.md`, `context/doc-cards.md`, `context/estd-routing-map.md`, `context/validators/`, `scripts/check-context.sh` | `hybrid-llm-operating-framework/Hybrid_LLM_Operating_Framework_Setup_Spec.md`, `scripts/check-context.sh` |
