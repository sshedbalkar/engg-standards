# Scripts

- [Scripts](#scripts)
  - [Overview](#overview)
  - [generate-toc.sh](#generate-tocsh)
    - [Primary Purpose](#primary-purpose)
    - [Features](#features)
    - [Operating Conditions](#operating-conditions)
    - [Edge Cases Handled](#edge-cases-handled-toc)
    - [Default Values](#default-values-toc)
    - [Usage](#usage-toc)
      - [Parameters](#parameters-toc)
      - [Return Codes](#return-codes-toc)
    - [How It Works](#how-it-works)
    - [Marker Placement](#marker-placement)
    - [Anchor Link Format](#anchor-link-format)
    - [Examples](#examples-toc)
      - [Basic Example](#basic-example)
      - [Code Blocks Handling](#code-blocks-handling)
      - [Special Characters Handling](#special-characters-handling)
    - [Common Issues and Solutions](#common-issues-and-solutions-toc)
  - [link-estd-references.sh](#link-estd-referencessh)
    - [Primary Purpose](#primary-purpose-link)
    - [Features](#features-link)
    - [Operating Conditions](#operating-conditions-link)
    - [Edge Cases Handled](#edge-cases-handled-link)
    - [Default Values](#default-values-link)
    - [Usage](#usage-link)
      - [Parameters](#parameters-link)
      - [Return Codes](#return-codes-link)
    - [How It Works](#how-it-works-link)
    - [Reference Formats](#reference-formats)
    - [Document Discovery](#document-discovery)
    - [Link Generation](#link-generation)
    - [Examples](#examples-link)
      - [Basic Examples](#basic-examples-link)
      - [Cross-Document References](#cross-document-references)
      - [URL Encoding Handling](#url-encoding-handling)
    - [Common Issues and Solutions](#common-issues-and-solutions-link)
  - [unlink-estd-references.sh](#unlink-estd-referencessh)
    - [Primary Purpose](#primary-purpose-unlink)
    - [Features](#features-unlink)
    - [Operating Conditions](#operating-conditions-unlink)
    - [Edge Cases Handled](#edge-cases-handled-unlink)
    - [Default Values](#default-values-unlink)
    - [Usage](#usage-unlink)
      - [Parameters](#parameters-unlink)
      - [Return Codes](#return-codes-unlink)
    - [How It Works](#how-it-works-unlink)
    - [Reversed Reference Formats](#reversed-reference-formats)
    - [Examples](#examples-unlink)
      - [Basic Examples](#basic-examples-unlink)
      - [Cross-Document References](#cross-document-references-unlink)
    - [Common Issues and Solutions](#common-issues-and-solutions-unlink)

## Overview

This folder contains reusable bash scripts for common documentation and development tasks used across the Engg Standards project. These scripts automate repetitive documentation work while maintaining consistency and correctness.

**See [LLM_SHELL_SCRIPT_STYLE_GUIDE.md](LLM_SHELL_SCRIPT_STYLE_GUIDE.md) for shell scripts and [LLM_NON_SHELL_SCRIPT_STYLE_GUIDE.md](LLM_NON_SHELL_SCRIPT_STYLE_GUIDE.md) for non-shell script automation.**

---

## generate-toc.sh

### Primary Purpose

Automatically generates a table of contents (TOC) with proper hierarchy and anchor links, then inserts it into markdown files. This eliminates manual TOC maintenance and ensures TOC links always match actual document structure.

### Features

- **Automatic TOC Generation**: Extracts all markdown headings and creates a hierarchical list with proper indentation
- **Intelligent Anchor Links**: Automatically generates valid markdown anchors from heading text
- **Code Block Awareness**: Skips content inside fenced code blocks (both ``` and ~~~), preventing code comments from appearing in TOC
- **Special Character Handling**: Removes special characters from anchors while preserving readability (e.g., `Getting Started!` → `#getting-started`)
- **Flexible Marker Detection**: Case-insensitive marker matching with optional leading/trailing whitespace tolerance
- **Whitespace Preservation**: Maintains contiguous spaces in headings as contiguous hyphens in anchors
- **Safe File Handling**: Uses temporary files to prevent corruption on write failures

### Operating Conditions

- **Input**: Markdown file with a `<!-- toc -->` marker on its own line
- **Environment**: Bash 4.0+ with standard Unix utilities (grep, sed, tr, printf)
- **Output**: Modified markdown file with TOC inserted at marker location
- **File System**: Read/write access to source file required
- **Performance**: Linear time complexity relative to file size; suitable for files up to several MB

### Edge Cases Handled {#edge-cases-handled-toc}

| Case | Handling |
|------|----------|
| **Missing marker** | Script exits successfully (exit 0) with informative message; file unchanged |
| **Marker in code block** | Marker is processed regardless of code block context (by design) |
| **Empty file** | TOC is empty; marker is replaced with empty content |
| **No headings** | TOC is empty but insertion proceeds |
| **Heading with special chars** | Characters stripped; spaces become hyphens; leading/trailing hyphens removed |
| **Contiguous spaces in heading** | Each space becomes a hyphen (e.g., "A  B" → `#a--b`) |
| **Multiple markers** | Only first marker is replaced; subsequent markers ignored |
| **Nested code blocks** | Toggle state per fence marker; handles both ``` and ~~~ equally |
| **Mixed fence styles** | Correctly toggles state; doesn't require paired fence styles |
| **Case-insensitive marker** | `<!-- TOC -->`, `<!-- toc -->`, `<!-- ToC -->` all recognized |
| **Marker with whitespace** | `  <!-- toc -->  ` recognized and replaced |
| **File read failures** | Script exits 1 with error message |

### Default Values {#default-values-toc}

| Setting | Default | Notes |
|---------|---------|-------|
| **Indentation unit** | 2 spaces | Each heading level adds 2 spaces |
| **Level 1 indent** | 0 spaces | H1 headings (#) have no indent |
| **Anchor case** | lowercase | All anchors are lowercase per markdown convention |
| **Special chars in anchors** | removed | Only alphanumeric, spaces, hyphens retained |
| **Space replacement** | hyphen | Each space becomes a `-` character |

### Usage {#usage-toc}

```bash
./generate-toc.sh <markdown_file>
```

#### Parameters {#parameters-toc}

- `<markdown_file>` - Path to the markdown file to process (required)
  - Can be relative or absolute path
  - File must exist and be readable
  - File must be writable (modified in-place)

#### Return Codes {#return-codes-toc}

- `0` - Success (TOC inserted or marker not found)
- `1` - Error (file not found, not readable, not writable, or invalid usage)

### How It Works

1. **Input Validation**: Checks file exists and is readable
2. **Marker Detection**: Searches for `<!-- toc -->` identifier (case-insensitive)
3. **Conditional Processing**: If marker found, proceeds to TOC generation; otherwise exits with message
4. **Line-by-Line Scan**: Reads entire file to track code block state
5. **Code Block Tracking**: Toggles `in_code_block` flag on fence markers (``` or ~~~)
6. **Heading Extraction**: Outside code blocks, captures markdown headings via regex `^(#+)\s+(.*)$`
7. **Indent Calculation**: Determines spacing based on heading level: `indent = (heading_level - 1) * 2`
8. **Anchor Generation**:
   - Converts heading to lowercase
   - Removes all non-alphanumeric characters except spaces and hyphens
   - Replaces all spaces with hyphens
   - Removes leading/trailing hyphens
9. **TOC Assembly**: Builds formatted TOC with indentation and anchor links
10. **Marker Replacement**: Uses sed to replace marker line with TOC content
11. **File Write**: Writes modified content to original file atomically (via temp file)

### Marker Placement

Add a marker in your markdown file where you want the table of contents to appear. The marker must be on its own line (can have leading/trailing whitespace):

```markdown
# My Document

<!-- toc -->

## Section One

Content...

## Section Two

More content...
```

The marker will be replaced with the generated table of contents during script execution.

### Anchor Link Format

Headings are converted to anchors by applying transformations in sequence:

1. **Lowercase conversion**: All uppercase letters become lowercase
2. **Character filtering**: Keep only: `a-z`, `0-9`, spaces, and hyphens (`-`)
   - Example: `Getting Started!` → `getting started`
3. **Space substitution**: Replace each space with a hyphen (preserves contiguous spacing)
   - Example: `getting started` → `getting-started`
   - Example with multiple spaces: `getting  started` → `getting--started`
4. **Trim hyphens**: Remove leading and trailing hyphens
   - Example: `-getting-started-` → `getting-started`

**Examples:**
- `## Getting Started` → `#getting-started`
- `## API Reference: REST vs GraphQL` → `#api-reference-rest-vs-graphql`
- `## Performance  Tuning` (2 spaces) → `#performance--tuning` (2 hyphens)
- `## 2024 Q1: Results & Analysis!` → `#2024-q1-results--analysis`

### Examples {#examples-toc}

#### Basic Example

Given a markdown file with:

```markdown
# My Guide

<!-- toc -->

## Installation

Steps to install.

## Configuration

Steps to configure.

### Advanced Setup

Advanced configuration steps.

## Troubleshooting

Help and support.
```

After running `./generate-toc.sh my-guide.md`, the content becomes:

```markdown
# My Guide

- [My Guide](#my-guide)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [Advanced Setup](#advanced-setup)
  - [Troubleshooting](#troubleshooting)

## Installation

Steps to install.

## Configuration

Steps to configure.

### Advanced Setup

Advanced configuration steps.

## Troubleshooting

Help and support.
```

#### Code Blocks Handling

The script correctly ignores content inside fenced code blocks:

```markdown
# Example

<!-- toc -->

## Introduction

## Code Example

Here's some code:

```bash
# This is not a heading
## Not in TOC
echo "Hello"
```

## Conclusion
```

Result: The TOC contains only "Introduction" and "Conclusion"; the code comment is ignored.

#### Special Characters Handling

Headings with special characters are properly sanitized:

```markdown
# Guide

<!-- toc -->

## Getting Started (with info)

## API & Integration!

## Best Practices: Key Points
```

Generates:

```markdown
- [Getting Started (with info)](#getting-started-with-info)
- [API & Integration!](#api-integration)
- [Best Practices: Key Points](#best-practices-key-points)
```

### Common Issues and Solutions {#common-issues-and-solutions-toc}

**Issue**: Script says "No identifier found" but I have the marker in my file.

**Solution**: Ensure the marker is on its own line. The marker must be on a line by itself (with optional leading/trailing spaces). It cannot be part of a longer line.

**Issue**: Links in the TOC aren't working.

**Solution**: Most modern markdown processors (GitHub, GitLab, Pandoc, etc.) support the generated anchor format. Verify your markdown viewer is up-to-date. Check that your file is UTF-8 encoded.

**Issue**: Code comments are appearing in the TOC.

**Solution**: Ensure your code is wrapped in proper fenced code blocks using triple backticks (```) or tildes (~~~). Both styles are supported. The script must see opening and closing fence markers to ignore content between them.

**Issue**: Special characters are missing from TOC links.

**Solution**: This is expected behavior. Markdown anchors cannot contain special characters like `!`, `@`, `:`, etc. The script removes them to create valid anchors. The link text still shows the original heading text with special characters.

---

## link-estd-references.sh

### Primary Purpose {#primary-purpose-link}

Converts ESTD document references (in `[[...]]` format) to proper markdown links with cross-document support. Enables internal documentation linking while maintaining a lightweight reference syntax in source files.

### Features {#features-link}

- **Multiple Reference Formats**: Supports current-document (`[[§1.2]]`), cross-document (`[[ESTD3 §1.2]]`), and document-header (`[[ESTD2]]`) references
- **Automatic TOC Lookup**: Searches Table of Contents to find exact section links from target documents
- **Flexible Document Discovery**: Finds ESTD documents using multiple naming patterns (e.g., `ESTDX_...md`, `ESTDX-...md`)
- **Cross-Document Support**: Generates proper relative paths for links to other documents
- **URL Encoding**: Encodes special characters in filenames (e.g., `#` → `%23`) per RFC 3986 for compatibility
- **Graceful Degradation**: Unresolved references remain unchanged for manual review or future resolution
- **Section Number Matching**: Supports both numeric section references (§5.1) and text-based lookups
- **Line-by-Line Processing**: Handles multiple references on a single line
- **Safe Replacement**: Uses sed with proper escaping to prevent injection attacks

### Operating Conditions {#operating-conditions-link}

- **Input**: Markdown file containing ESTD reference markers (`[[...]]`)
- **Reference Format**: `[[§SECTION]]` (current doc) or `[[ESTDX §SECTION]]` or `[[ESTDX]]` (cross-doc)
- **Environment**: Bash 4.0+ with standard Unix utilities (grep, sed, find, basename)
- **ESTD Directory**: Directory containing ESTD markdown files (defaults to current directory)
- **Output**: Modified markdown file with references converted to links
- **Performance**: Linear relative to file size and reference count; suitable for standard document sizes

### Edge Cases Handled {#edge-cases-handled-link}

| Case | Handling |
|------|----------|
| **Section not found** | Reference remains as-is; no link generated |
| **ESTD document not found** | Reference remains as-is; no link generated |
| **Current doc ID cannot be determined** | Current-document references (`[[§X]]`) are ignored |
| **Special chars in filename** | Characters URL-encoded (RFC 3986) before use in link path |
| **Multiple refs on same line** | Each reference processed independently; all converted if possible |
| **Already-processed references** | Existing markdown links left untouched (not re-processed) |
| **Reference in code block** | Still processed (no code block detection; by design) |
| **Malformed reference** | Invalid formats left unchanged |
| **Empty section specified** | Treated as document header reference; links to document title |
| **Case variation in doc ID** | Document lookup is case-sensitive; `[[estd1]]` won't match `ESTD1`... |
| **Relative path ambiguity** | Uses `./` prefix for cross-doc links to ensure consistent relative resolution |
| **Missing TOC in target document** | Section lookup fails; reference unchanged |

### Default Values {#default-values-link}

| Setting | Default | Notes |
|---------|---------|-------|
| **ESTD docs directory** | `.` (current dir) | Can be overridden via second parameter |
| **Document ID source** | Filename | Extracted from filename (e.g., `ESTD3` from `ESTD3_..._Standards.md`) |
| **Fallback ID source** | File first heading | If filename doesn't contain ESTD ID, checks first line |
| **Link path prefix** | `./` | Cross-document links prefixed with relative path |
| **Anchor format** | `#...` | Extracted directly from TOC entry |
| **URL encoding** | RFC 3986 | Only alphanumeric, `-._~` unencoded |

### Usage {#usage-link}

```bash
# Use ESTD docs from current directory
./link-estd-references.sh <markdown_file>

# Use ESTD docs from specific directory
./link-estd-references.sh <markdown_file> <estd_docs_dir>
```

#### Parameters {#parameters-link}

- `<markdown_file>` - Path to the markdown file to process (required)
  - Can be relative or absolute path
  - File must exist and be readable/writable
- `[estd_docs_dir]` - Directory containing ESTD documents (optional)
  - Defaults to current working directory (`.`) if not supplied
  - Must be a valid, readable directory

#### Return Codes {#return-codes-link}

- `0` - Success (references processed or none found)
- `1` - Error (file not found, directory not found, invalid usage, or file not accessible)

### How It Works {#how-it-works-link}

1. **Input Validation**: Checks markdown file and ESTD directory exist and are accessible
2. **Document ID Extraction**: Determines current document ID from:
   - Filename pattern (e.g., `ESTD3_-_...` → `ESTD3`)
   - First heading line if filename doesn't contain ESTD ID
3. **Line-by-Line Processing**: Reads file and processes each line independently
4. **Reference Detection**: Uses grep to find all `[[...]]` patterns in the line
5. **Reference Parsing**: Extracts content from brackets and determines reference type:
   - Format: `ESTDX SEC.TION` → Type: cross-document
   - Format: `§SEC.TION` → Type: current-document
6. **Document Lookup**: For cross-doc refs, finds target ESTD file using `find` with multiple name patterns:
   - `ESTDX.md`, `ESTDX_*.md`, `ESTDX-*.md` (with .md extension)
   - `ESTDX_*`, `ESTDX-*` (without extension, fallback)
7. **TOC Extraction**: Parses Table of Contents section of target document:
   - Searches for `## Table of Contents` start marker
   - Extracts lines with pattern `\s*-\s*\[.*\](.*)`
8. **Section Matching**: Searches TOC for matching section by:
   - Numeric pattern: `\\[${section}[ .]` (e.g., `§1.2` matches `[1.2 Title]`)
   - Text pattern: Case-insensitive substring match
9. **Link Generation**:
   - Extracts link text from TOC entry
   - Extracts anchor from TOC entry
   - For current doc: `[§TEXT](#anchor)`
   - For cross-doc: `[ESTDX §TEXT](./URL_ENCODED_FILENAME#anchor)`
10. **URL Encoding**: Encodes special characters in filename (RFC 3986):
    - Converts characters not in `[-_.~a-zA-Z0-9]` to `%HH` format
    - Example: `ESTD3_-_Unity_and_C#_Standards.md` → `ESTD3_-_Unity_and_C%23_Standards.md`
11. **sed Replacement**: Replaces reference with generated link:
    - Escapes special sed characters in both reference and replacement
    - Uses `/` as sed delimiter
12. **Output**: Writes modified content to temp file, then replaces original
13. **Exit**: Returns 0 on success

### Reference Formats

The script recognizes three reference formats:

#### 1. Current Document Section Reference

```markdown
See [[§3.1]] for details.
```

Converted to: `See [§3.1 Section Title](#31-section-title) for details.`

- Searches current document's TOC for matching section
- Link has no document path prefix (stays within same document)
- Use when referencing sections in the same file

#### 2. Cross-Document Section Reference

```markdown
Defined in [[ESTD3 §5.1]].
```

Converted to: `Defined in [ESTD3 §5.1 Section Title](./ESTD3_-_..._Standards.md#51-section-title).`

- Links to specific section in different ESTD document
- Includes document filename as relative path prefix
- Filename is URL-encoded for compatibility

#### 3. Document Header Reference

```markdown
See [[ESTD2]] for all client standards.
```

Converted to: `See [ESTD2](./ESTD2_-_General_..._Standards.md#estd2---general-...) for all client standards.`

- Links to document title (first TOC entry)
- Useful for referencing entire documents
- No section specified; links to document header

### Document Discovery

Documents are discovered using a flexible multi-pattern search:

```bash
# First, try with .md extension (primary method)
find "$dir" -maxdepth 1 -type f \( \
  -name "ESTD${num}.md" -o \
  -name "ESTD${num}_*.md" -o \
  -name "ESTD${num}-*.md" \
\)

# Second, try without extension (fallback)
find "$dir" -maxdepth 1 -type f \( \
  -name "ESTD${num}_*" -o \
  -name "ESTD${num}-*" \
\)
```

This supports multiple naming conventions:
- `ESTD1.md`
- `ESTD1_-_Common_Standards.md`
- `ESTD2-Client_Standards.md`
- `ESTD3_v2.md`

### Link Generation

Generated links follow markdown convention:

```markdown
[LINK_TEXT](RELATIVE_PATH#ANCHOR)
```

Components:

| Component | Source | Example |
|-----------|--------|---------|
| `LINK_TEXT` | TOC entry (or `§SECTION` for current doc) | `3.1 Section Title` |
| `RELATIVE_PATH` | Document filename with URL encoding | `./ESTD3_-_Unity_and_C%23_Standards.md` |
| `ANCHOR` | Extracted from TOC entry parentheses | `#31-section-title` |

### Examples {#examples-link}

#### Basic Examples {#basic-examples-link}

**Example 1: Current document reference**

Input: `See [[§2]]`
Output: `See [§2. Guiding Principles](#2-guiding-principles)`

**Example 2: Cross-document reference**

Input: `Defined in [[ESTD1 §7.3]]`
Output: `Defined in [ESTD1 §7.3 Block Try-Catch](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#73-block-try-catch-the-anti-pattern-and-the-acceptable-exceptions)`

**Example 3: Document header reference**

Input: `Follow [[ESTD2]]`
Output: `Follow [ESTD2](./ESTD2_-_General_Client_Engg_Standards.md#estd2---general-client-engineering-standards)`

#### Cross-Document References

Processing a file with multiple cross-document references:

```markdown
# ESTD2 - Client Standards

All client standards are defined here. See also:
- [[ESTD1 §1]] for general principles
- [[ESTD3 §5]] for Unity-specific guidance
- [[ESTD1]] for complete engineering standards
```

After processing:

```markdown
# ESTD2 - Client Standards

All client standards are defined here. See also:
- [ESTD1 §1. Purpose and Scope](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#1-purpose-and-scope) for general principles
- [ESTD3 §5. MonoBehaviour Lifecycle Standards](./ESTD3_-_Unity_and_C%23_Standards.md#5-monobehaviour-lifecycle-standards) for Unity-specific guidance
- [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) for complete engineering standards
```

#### URL Encoding Handling

Filenames with special characters are properly URL-encoded:

Input: `[[ESTD3 §5]]`

Processing:
1. Find document: `ESTD3_-_Unity_and_C#_Standards.md`
2. URL-encode filename: `ESTD3_-_Unity_and_C%23_Standards.md`
3. Generate link: `./ESTD3_-_Unity_and_C%23_Standards.md#5-monobehaviour-...`

Result: `[ESTD3 §5. MonoBehaviour Lifecycle Standards](./ESTD3_-_Unity_and_C%23_Standards.md#5-monobehaviour-lifecycle-standards)`

### Common Issues and Solutions {#common-issues-and-solutions-link}

**Issue**: Reference not converted; stays as `[[ESTD1 §7]]`

**Solution**: Common causes:
1. Section not found in target document's TOC - Verify the section number is correct
2. Target document not found - Check ESTD directory path and document naming
3. Section format mismatch - Ensure section number matches TOC format (e.g., `7` vs `7.1`)

**Issue**: Link path is wrong; uses full path instead of relative path

**Solution**: The script always generates relative paths with `./` prefix for cross-document links. This is correct behavior and ensures links work in various contexts.

**Issue**: Special characters in link path appear as `%XX` instead of raw characters

**Solution**: This is expected and correct. URL encoding is applied for compatibility with various markdown processors and file systems. Modern markdown viewers automatically decode these during rendering.

**Issue**: Current document references `[[§X]]` not working

**Solution**: This requires the script to determine the current document ID. For this to work:
1. Filename must contain ESTD ID (e.g., `ESTD2_-_Standards.md`)
2. OR first line of file must be a heading containing ESTD ID (e.g., `# ESTD2 - Standards`)

**Issue**: Script exits with "Directory not found" but directory exists

**Solution**: Check that the directory path is correct and readable. Use absolute paths if relative paths are ambiguous. Ensure you have read permission on the directory.

**Issue**: Links break in certain markdown viewers

**Solution**: Most issues arise from:
1. Viewer not supporting URL-encoded characters - Use a modern viewer (GitHub, GitLab, etc.)
2. Markdown processor not generating expected anchors - This is rare; test with standard markdown to HTML conversion
3. File encoding issues - Ensure file is UTF-8 encoded

---

## unlink-estd-references.sh

### Primary Purpose {#primary-purpose-unlink}

Reverses what `link-estd-references.sh` does. Converts resolved ESTD markdown links back to lightweight `[[...]]` soft references. Enables round-tripping between the authoring format (soft references) and the rendered format (resolved markdown links).

### Features {#features-unlink}

- **Three Link Types**: Converts internal section links (`[§TEXT](#anchor)`), cross-document section links (`[ESTDX §TEXT](./...)`), and cross-document header links (`[ESTDX](./...)`)
- **Section Number Extraction**: Extracts the numeric section identifier from full section titles (e.g., `§4.4 Request Cancellation` → `4.4`)
- **TOC Awareness**: Skips the Table of Contents section to avoid converting legitimate TOC links
- **Code Block Awareness**: Skips content inside fenced code blocks (both ``` and ~~~)
- **Self-Contained**: No ESTD directory required — all information is extracted from the link text itself
- **Safe Replacement**: Uses sed with proper escaping to prevent injection
- **Line-by-Line Processing**: Handles multiple resolved links on a single line

### Operating Conditions {#operating-conditions-unlink}

- **Input**: Markdown file containing resolved ESTD markdown links
- **Environment**: Bash 4.0+ with standard Unix utilities (grep, sed)
- **Output**: Modified markdown file with links converted to `[[...]]` references
- **Performance**: Linear relative to file size; suitable for standard document sizes

### Edge Cases Handled {#edge-cases-handled-unlink}

| Case | Handling |
|------|----------|
| **Link in TOC section** | Skipped; TOC links are not converted |
| **Link in code block** | Skipped; code block content preserved |
| **Multiple links on same line** | Each link processed independently |
| **Link text without section number** | Link left unchanged (no valid soft reference possible) |
| **Already-soft references** | `[[...]]` references left untouched |
| **Non-ESTD links** | Only links matching ESTD patterns are converted; others unchanged |
| **URL-encoded filenames** | Handled correctly — link text (not URL) is used for extraction |
| **Nested section numbers** | Supports multi-level numbers like `4.1`, `9.3` |

### Default Values {#default-values-unlink}

| Setting | Default | Notes |
|---------|---------|-------|
| **TOC detection** | `## Table of Contents` | Lines between this heading and the next `## ` heading are skipped |
| **Code block detection** | ``` or ~~~ | Toggles code block state on fence markers |

### Usage {#usage-unlink}

```bash
./unlink-estd-references.sh <markdown_file>
```

#### Parameters {#parameters-unlink}

- `<markdown_file>` - Path to the markdown file to process (required)
  - Can be relative or absolute path
  - File must exist and be readable/writable

#### Return Codes {#return-codes-unlink}

- `0` - Success (links converted or none found)
- `1` - Error (file not found or invalid usage)

### How It Works {#how-it-works-unlink}

1. **Input Validation**: Checks markdown file exists
2. **Line-by-Line Processing**: Reads file and processes each line independently
3. **Code Block Tracking**: Toggles `in_code_block` flag on fence markers (``` or ~~~); skips content inside
4. **TOC Tracking**: Detects `## Table of Contents` and skips all lines until the next `## ` heading
5. **Link Detection**: Uses grep with three patterns (ordered most-specific first):
   - Cross-doc section: `\[ESTD[0-9]+ §...\]\(\./...\)`
   - Cross-doc header: `\[ESTD[0-9]+\]\(\./...\)`
   - Internal section: `\[§...\]\(#...\)`
6. **Link Text Extraction**: Parses link text from `[TEXT](...)` using sed
7. **Type Classification**: Determines link type from text pattern:
   - `ESTD\d+` → cross-doc header
   - `ESTD\d+ §...` → cross-doc section
   - `§...` → internal section
8. **Section Number Extraction**: Walks characters after `§`, collecting digits and dots (dot only if followed by digit)
9. **Soft Reference Assembly**:
   - Internal: `[[§NUM]]`
   - Cross-doc section: `[[ESTDX §NUM]]`
   - Cross-doc header: `[[ESTDX]]`
10. **sed Replacement**: Replaces resolved link with soft reference, escaping special characters
11. **Output**: Writes modified content to temp file, then replaces original

### Reversed Reference Formats

The script converts three resolved link formats:

#### 1. Internal Section Link

```markdown
See [§4.4 Request Cancellation](#44-request-cancellation) above.
```

Converted to: `See [[§4.4]] above.`

#### 2. Cross-Document Section Link

```markdown
See [ESTD3 §7. Memory and Garbage Collection](./ESTD3_-_Unity_and_C%23_Standards.md#7-memory-and-garbage-collection).
```

Converted to: `See [[ESTD3 §7]].`

#### 3. Cross-Document Header Link

```markdown
| Depends On | [ESTD1](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#estd1---common-engineering-standards-and-best-practices-for-all-engineers) |
```

Converted to: `| Depends On | [[ESTD1]] |`

### Examples {#examples-unlink}

#### Basic Examples {#basic-examples-unlink}

**Example 1: Internal section reference**

Input: `See [§17. Memory Leak Prevention](#17-memory-leak-prevention).`
Output: `See [[§17]].`

**Example 2: Cross-document section reference**

Input: `([ESTD1 §4.1 Domain Glossary](./ESTD1_-_Common_Engg_Standards_And_Best_Practices.md#41-domain-glossary))`
Output: `([[ESTD1 §4.1]])`

**Example 3: Cross-document header reference**

Input: `covered in [ESTD3](./ESTD3_-_Unity_and_C%23_Standards.md#estd3---unity-and-c-standards-for-engineers)`
Output: `covered in [[ESTD3]]`

#### Cross-Document References {#cross-document-references-unlink}

Processing a file with multiple resolved links:

```markdown
See [ESTD3 §7. Memory and Garbage Collection](./ESTD3_-_Unity_and_C%23_Standards.md#7-memory-and-garbage-collection) and [ESTD3 §8. String Allocation in Hot Paths](./ESTD3_-_Unity_and_C%23_Standards.md#8-string-allocation-in-hot-paths) for details.
- Object pooling ([ESTD3 §9. Object Pooling](./ESTD3_-_Unity_and_C%23_Standards.md#9-object-pooling)).
```

After processing:

```markdown
See [[ESTD3 §7]] and [[ESTD3 §8]] for details.
- Object pooling ([[ESTD3 §9]]).
```

### Common Issues and Solutions {#common-issues-and-solutions-unlink}

**Issue**: TOC links are being converted to soft references

**Solution**: Ensure the TOC starts with a `## Table of Contents` heading. The script skips all lines between this heading and the next `## ` heading.

**Issue**: Some resolved links are not being converted

**Solution**: The script only converts links matching these specific patterns:
1. Internal: `[§TEXT](#anchor)` — link text must start with `§`
2. Cross-doc section: `[ESTDX §TEXT](./...)` — link text must start with `ESTD` + digits + space + `§`
3. Cross-doc header: `[ESTDX](./...)` — link text must be exactly `ESTD` + digits

Links that were manually written (not generated by `link-estd-references.sh`) may use slightly different formats and won't be matched.

**Issue**: Section number extracted incorrectly

**Solution**: The script extracts the leading numeric portion after `§`. For `§4.1 Domain Glossary`, it extracts `4.1`. A trailing dot without a following digit is not included (e.g., `§7. Memory` extracts `7`, not `7.`).

**Issue**: Links inside code blocks are being converted

**Solution**: Ensure code blocks use proper fenced syntax (triple backticks or triple tildes). The script tracks code block state and skips content inside them.
