# Engg Standards Agent Guide

project_state: mature_repo
project_foundation_file: README.md

## Core Rules

- This repo is the single source of truth; never infer content from external knowledge.
- All exceptions require written approval from Director of Engineering or Architect.
- Never renumber existing sections; section numbers drive cross-references.
- Always regenerate TOC after editing headings: `./scripts/generate-toc.sh <file>`.
- Always resolve `[[...]]` references after adding them: `./scripts/link-estd-references.sh <file> docs/`.
- Update `Version` and `Last Updated` in frontmatter on every document edit.
- Never modify the Living Document Notice boilerplate.
- Never add unsolicited content; ESTD documents are authoritative.
- After ESTD doc create/update/rename/repurpose, check/update `context/doc-cards.md`, `context/repo-map.md`, `context/estd-routing-map.md`, and `context/validators/` when applicable.
- When editing `AGENTS.md`, `CLAUDE.md`, or `context/*.md`, keep only hard rules, routing, durable retrieval aids, or tool-local behavior. Remove duplicated or easy-to-derive info. Prefer terse, grammar-light bullets.
- Do not keep conflicting rules in the same applicable scope. If a rule is local, exceptional, or narrower than another rule, state that scope explicitly.
- Run `./scripts/check-context.sh` after changing shared context files or ESTD doc inventory.
- When creating or updating scripts, follow `scripts/LLM_SHELL_SCRIPT_STYLE_GUIDE.md` or
  `scripts/LLM_NON_SHELL_SCRIPT_STYLE_GUIDE.md`.
- Code examples must cover all four stacks: PHP, Java, C#/Unity, TypeScript/NextJS.
- Never force-add gitignored paths: `confluence/`, `prompts/`, `scripts/*.md`, `scripts/test-*`, `.DS_Store`, `CLAUDE.md`.
- File naming: `ESTDN_-_Title_Words_Separated_By_Underscores.md` — no zero-padding, no spaces.
- New documents: start `Status` as `Draft`; change to `Active` after approval.

## Read Order

1. `AGENTS.md`
2. `README.md`
3. `context/llm-operating-guide.md`
4. `context/repo-map.md`
5. `context/estd-routing-map.md`
6. relevant cards or routing nodes only
7. relevant validator specs only when validation is involved
8. target sources only

## Cache Update Rule

- Read `## Lookup Strategy` before editing shared cache files.
- Preserve declared ordering and refresh `## Jump Index` when entries change.

## Applied Learning

When an important discovery is made about the ESTD documents that is reusable, add a one line bullet here. Keep each bullet under 15 words. No explanations. Only add things that will save time in future ESTD related sessions.

- Always write commit messages using ESTD1 §21.2 format, body should be < 20 words.
