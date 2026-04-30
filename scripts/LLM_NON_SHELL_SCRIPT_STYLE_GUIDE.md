# Non-Shell Script Style Guide

## Overview

Runtime: **Python, Node.js, TypeScript, or another approved repo runtime**  
Priority: **supported runtime and standard libraries > existing local tooling > external dependencies > convenience**

Use this guide for executable or script-like automation that is not shell: Python CLIs, Node/TypeScript utilities, data processors, backfill helpers, local maintenance tools, and repo helper tooling.

Keep only rules that prevent failures, ambiguity, or avoidable maintenance cost.

---

## 1. Runtime & Entrypoint

Directly executable scripts must start with an appropriate shebang:

```python
#!/usr/bin/env python3
```

```typescript
#!/usr/bin/env node
```

Executable scripts must expose a single explicit entrypoint:

```python
def main(argv: list[str]) -> int:
    # Parse inputs and run the script.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

Rules:
- no work at import time except constants, imports, and lightweight declarations
- return explicit exit codes
- write errors to `stderr`
- use `stdout` only for intended output
- keep modules importable for tests

---

## 2. Input Validation

Before doing work:
- validate required inputs, config files, environment variables, and paths
- reject unsupported modes early
- use structured parsers instead of manual argument slicing
- make destructive actions explicit through flags or confirmation gates
- exit `1` for validation or business-rule failures
- exit `2` for tool, config, adapter, or dependency failures when the script has that distinction

---

## 3. Comments & Documentation

**Rule:** Include a module header docstring at the top of each executable script describing purpose, usage, parameters/options, outputs, side effects, return codes, technical approach, and examples. Document complex functions. Inline comments explain *why*, not *what*.

**Rationale:**
- Scripts are often run months later by the author or others; header docs save context-switching time.
- Usage, outputs, and return codes reduce guesswork in CI and local automation.
- *Why* comments prevent future refactors from breaking hidden requirements.

**How to apply:**

Header docstring:

```python
"""Purpose:
    Brief description of what the script does.

Usage:
    python3 path/to/my_script.py <required_arg> [--optional value]

Parameters:
    required_arg:
        Description.
    --optional:
        Description and default.

Environment:
    MY_TOOL_TOKEN:
        Required only when calling the external adapter.

Outputs:
    stdout:
        Intended machine-readable or user-facing output.
    files:
        Any files created or modified.

Side Effects:
    Describe external calls, filesystem writes, migrations, or none.

Return Codes:
    0 - Success.
    1 - Validation or expected script failure.
    2 - Tool, config, dependency, or adapter error.

Technical Approach:
    List the core processing steps.

Examples:
    python3 path/to/my_script.py input.json --out build/output.json
"""
```

Function documentation:

```python
def load_records(path: Path) -> list[dict[str, str]]:
    """Load validated input records from a UTF-8 JSON file.

    Raises:
        ToolError: If the file is missing or has an invalid schema.
    """
```

Inline comments:

```python
# Keep adapter output capped so a noisy tool cannot make reports unreadable.
message = stderr[:1000]
```

---

## 4. Core Rules

1. Prefer the repo's existing runtime, helpers, and dependency style.
2. Use typed public boundaries where the language supports them.
3. Keep imports deterministic and avoid import-time work.
4. Parse CLI args with standard parsers (`argparse`, `commander`, or existing local equivalent).
5. Validate files before reading and parent directories before writing.
6. Use UTF-8 for text file reads and writes.
7. Keep output deterministic: stable sort order, stable JSON keys, newline at EOF.
8. Never log secrets, tokens, credentials, or full sensitive payloads.
9. Use structured formats for structured data; do not parse JSON, YAML, CSV, or XML with ad hoc string splitting when a parser is available.
10. Wrap subprocess calls with explicit argv arrays, working directory, timeout, captured output, and checked return handling.
11. Do not hide failures unless non-fatal by design and documented.
12. Separate pure logic from I/O so tests can cover behavior without running the full CLI.
13. Make side effects visible in docs and code names.
14. Prefer small functions with clear data flow over clever one-liners.
15. Always test happy paths, sad paths, edge cases, and repeatability.

---

## 5. External Adapters & Side Effects

Use these rules when scripts call external APIs, databases, CLIs, cloud services,
or any system outside the local process:

1. Isolate adapter code from pure transformation logic.
2. Validate required tools, credentials, environment, and config before mutation.
3. Use explicit timeouts and expected status/result checks for every external call.
4. Bound pagination, retries, polling, and streamed output so loops cannot run forever.
5. Cap and redact adapter diagnostics before logging; never print secrets or full payloads.
6. Make external writes idempotent when possible, using stable keys or existence checks.
7. Verify important writes by reading back the resulting state.
8. Treat partial external failures as explicit errors unless documented as non-fatal.
9. Unit-test logic with mocked adapters; live service tests must be separate and opt-in.

---

## 6. Python Conventions

Use:
- `from __future__ import annotations`
- `pathlib.Path` for paths
- `argparse` for command-line parsing
- `json.dumps(..., sort_keys=True)` for deterministic JSON when order is not meaningful
- project-specific exception types for expected tool failures
- dataclasses, typed DTOs, or type aliases for external request/response boundaries

Avoid:
- bare `except`
- `shell=True`
- mutable default arguments
- global state mutated by helper functions
- writing files during module import
- mixing API calls, file I/O, parsing, and business rules in one large function

Example:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="export-report")
    parser.add_argument("source", help="Input JSON file")
    parser.add_argument("--out", required=True, help="Output JSON file")
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    source = Path(args.source)
    if not source.exists():
        print(f"ERROR: source not found: {source}", file=sys.stderr)
        return 1
    payload = json.loads(source.read_text(encoding="utf-8"))
    Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0
```

---

## 7. TypeScript/Node Conventions

Use:
- `node:fs/promises` and `node:path`
- explicit `process.exitCode` or returned status from an async main wrapper
- runtime validation for external input
- typed DTOs for parsed data

Avoid:
- implicit `any`
- top-level side effects beyond calling the main wrapper
- unbounded child process output
- shell string command construction

Example:

```typescript
#!/usr/bin/env node

import { readFile, writeFile } from "node:fs/promises";

type Report = {
  status: "pass" | "fail";
};

async function main(argv: string[]): Promise<number> {
  const [source, out] = argv;
  if (!source || !out) {
    console.error("ERROR: usage: export-report <source> <out>");
    return 1;
  }

  const report = JSON.parse(await readFile(source, "utf8")) as Report;
  await writeFile(out, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  return 0;
}

main(process.argv.slice(2))
  .then((code) => {
    process.exitCode = code;
  })
  .catch((error: unknown) => {
    console.error(`ERROR: ${error instanceof Error ? error.message : String(error)}`);
    process.exitCode = 2;
  });
```
