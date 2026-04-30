# Open Work

| Problem | Target Nodes | Expected End State | Removal Condition |
|:--------|:-------------|:-------------------|:------------------|
| Cross-tool cold-start behavior not yet proven with real Codex and Claude task comparisons. | `context/README.md`, `context/llm-operating-guide.md`, `context/doc-cards.md` | One or more real ESTD tasks confirm shared context narrows reading scope without full repo rediscovery. | Remove after at least one validated cross-tool run shows the expected scoped-loading behavior. |
| Bootstrap payload size not yet measured against routine ESTD tasks. | `context/README.md`, `context/repo-map.md`, `context/doc-cards.md`, `context/llm-operating-guide.md` | Always-read shared set stays compact enough for routine ESTD sessions. | Remove after payload size is measured and no further compaction is needed for normal use. |
| Drop-in hybrid enforcement not yet dry-run against a real Bingo repo. | `tools/estd-enforcer/README.md`, `context/validators/README.md` | One existing repo runs static-first CLI with an approved LLM gap adapter and archived reports. | Remove after a real dry-run confirms routing, static checks, citations, and gate behavior. |
