# Shell Script Style Guide

## Overview

Runtime: **bash**  
Priority: **POSIX compliance > bash features > convenience**

Keep only rules that prevent failures, ambiguity, or avoidable maintenance cost.

---

## 1. Interpreter & Shebang

Executable scripts must start with:

```bash
#!/bin/bash

set -euo pipefail
```

---

## 2. Input Validation

Before doing work:
- validate required inputs
- write errors to `stderr`
- exit `1` on failure

---

## 3. Comments & Documentation

**Rule:** Include a header comment block at the top of each script describing purpose, usage, parameters, and return codes. Document complex functions. Inline comments explain *why*, not *what*.

**Rationale:**
- Scripts are often run months later by the author or others; header docs save context-switching time.
- `Usage` patterns in comments are quickly scannable and reduce manual lookup.
- *Why* comments prevent future refactors from breaking hidden requirements.

**How to apply:**

Header block (top of file, after shebang and before code):
```bash
##############################################################################
# Script: my-script.sh
# Purpose: Brief description of what the script does
#
# Usage: ./my-script.sh <required_arg> [optional_arg]
#
# Parameters:
#   <required_arg>   - Description (required)
#   [optional_arg]   - Description (optional, defaults to X if not supplied)
#
# Return Codes:
#   0 - Success
#   1 - Error (invalid input, file not found, etc.)
#
# Description:
#   Longer explanation of what the script does, its preconditions,
#   and any side effects. Mention edge cases or non-obvious behavior.
#
# Technical Approach:
#   List the technical approach taken in the core logic of the script
#
# Examples:
#   Give examples of various ways how the script can be used
##############################################################################
```

Function documentation (before each function):
```bash
# Extract link text from TOC entries
# Arguments:
#   $1 - Document file path
#   $2 - Section identifier (e.g., "5.1" or "Getting Started")
# Outputs:
#   Formatted link text (e.g., "§5.1 Getting Started") or nothing if not found
# Returns:
#   0 - Success (link text found and printed)
#   1 - Section not found
find_toc_link() {
    local doc_file="$1"
    local section="$2"
    # Implementation...
}
```

Inline comments:
```bash
# Only process within valid document lines; skip code blocks to avoid false positives
if (( !in_code_block )); then
    headings+=("$heading_text")
fi
```

---

## 4. Core Rules

1. Use lowercase for locals and `UPPERCASE` for constants.
2. Quote variable expansions as `"${var}"` outside arithmetic contexts.
3. Use `trap` to clean up temporary files.
4. Use `local` inside functions and declare functions before use.
5. Return status with exit codes; use `stdout` only for intended output.
6. Use `[[ ]]` for tests and `(( ))` for arithmetic.
7. Use `while IFS= read -r line` for line reading.
8. Do not hide failures unless non-fatal by design.
9. Exit `0` only on complete success; exit `1` on any error.
10. Prefer maintainability over cleverness.
11. Always test and validate the script for meeting the requirements.

---

## 5. External Tools & Side Effects

Use these rules when scripts call external APIs, cloud tools, databases, package
managers, CLIs, or any system outside the local process:

1. Validate required commands, files, environment variables, and credentials before mutation.
2. Use explicit flags and arguments; avoid shell-built command strings.
3. Bound retries, pagination, polling, and captured output.
4. Cap and redact diagnostics before logging; never print secrets or full payloads.
5. Make external writes idempotent where possible, using stable keys or existence checks.
6. Verify important writes by reading back the resulting state.
7. Clean up temp files with `trap`, and keep generated paths predictable.
8. Keep adapter calls in small functions; keep parsing and decision logic separate.
