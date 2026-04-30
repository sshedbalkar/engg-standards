#!/bin/bash

##############################################################################
# Script: link-estd-references.sh
# Purpose: Convert ESTD document references to markdown links
#
# Usage: ./link-estd-references.sh <markdown_file> [estd_docs_dir]
#
# Parameters:
#   <markdown_file>   - Path to the markdown file to process (required)
#   [estd_docs_dir]   - Directory containing ESTD documents (optional)
#                       Defaults to current working directory if not supplied
#
# Description:
#   Scans a markdown file for ESTD references in the format:
#   - [[§26.3]]          (reference in current document)
#   - [[ESTD1 §26.3]]    (reference to specific section in ESTD1)
#   - [[ESTD1]]          (reference to document header)
#   - [[§26]]            (reference to section header in current document)
#
#   Each reference is replaced with a markdown link found in the Table of
#   Contents of the target ESTD document.
#
#   ESTD documents are found using these naming patterns:
#   - ESTDX_something.md (e.g., ESTD1_-_Common_Standards.md)
#   - ESTDX-something.md (e.g., ESTD2-Client_Standards.md)
#   - ESTDX_.md          (e.g., ESTD11_.md)
#
#   If the target ESTD document or section is not found, no action is taken.
#
# Technical Approach:
#   1. Document identification: Extracts current document ID from filename/heading
#   2. Reference parsing: Uses grep to find all [[...]] patterns in each line
#   3. Reference type detection: Determines if reference is ESTD-specific or current-doc
#   4. Document lookup: Finds target ESTD file using flexible naming pattern matching
#   5. TOC extraction: Parses Table of Contents from target document to find section
#   6. Link generation: Builds markdown link with proper text formatting:
#      - Current doc: [§SECTION](#anchor)
#      - Cross-doc: [ESTDX §SECTION](./ESTDX_...md#anchor) with URL-encoded filename
#   7. URL encoding: Encodes special characters in filenames (# → %23) per RFC 3986
#   8. Replacement: Uses sed to replace reference with generated link
#   9. State preservation: Unresolved references remain unchanged for manual review
#
# Returns:
#   0 - Always (success or no references found)
#   1 - Error (file not found, directory not found, or invalid usage)
#
# Examples:
#   # Use ESTD docs from current directory
#   ./link-estd-references.sh my-document.md
#
#   # Use ESTD docs from specific directory
#   ./link-estd-references.sh my-document.md /path/to/estd/docs
##############################################################################

set -euo pipefail

# Validate input
if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 <markdown_file> [estd_docs_dir]"
    exit 1
fi

markdown_file="$1"
estd_docs_dir="${2:-.}"  # Use current working directory if not supplied

# Check files
if [[ ! -f "$markdown_file" ]]; then
    echo "✗ File '$markdown_file' does not exist."
    exit 1
fi

if [[ ! -d "$estd_docs_dir" ]]; then
    echo "✗ Directory '$estd_docs_dir' does not exist."
    exit 1
fi

# Extract current doc ID from filename
# Matches: ESTD0, ESTD1, ESTD14, etc. (followed by _ or -)
current_doc_id=""
filename=$(basename "$markdown_file")
if [[ $filename =~ ^ESTD([0-9]+)([_-]|$) ]]; then
    current_doc_id="ESTD${BASH_REMATCH[1]}"
else
    # If filename doesn't contain ESTD ID, try to extract from first heading
    first_heading=$(head -1 "$markdown_file")
    if [[ $first_heading =~ ESTD([0-9]+) ]]; then
        current_doc_id="ESTD${BASH_REMATCH[1]}"
    fi
fi

# URL encode a string for use in markdown links
# Converts special characters to percent-encoded format
url_encode() {
    local string="$1"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * ) printf -v o '%%%02x' "'$c"
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

# Find ESTD document by ID
# Handles patterns like: ESTDX_, ESTDX-, ESTDX_something, ESTDX-something
# Prioritizes .md files since those are markdown documents
find_estd_doc() {
    local doc_id="$1"
    # First try to find .md files
    local result=$(find "$estd_docs_dir" -maxdepth 1 -type f \( -name "ESTD${doc_id}.md" -o -name "ESTD${doc_id}_*.md" -o -name "ESTD${doc_id}-*.md" \) 2>/dev/null | head -1)

    # If not found, look for files without extension
    if [[ -z "$result" ]]; then
        result=$(find "$estd_docs_dir" -maxdepth 1 -type f \( -name "ESTD${doc_id}_*" -o -name "ESTD${doc_id}-*" -o -name "ESTD${doc_id}_" -o -name "ESTD${doc_id}-" \) 2>/dev/null | head -1)
    fi

    echo "$result"
}

# Extract link text and anchor from TOC for a section
# Returns markdown link in format: [ESTDXX §SECTION](...) or [§SECTION](...) or [ESTDXX](...) or [§](...) for headers
find_toc_link() {
    local doc_file="$1"
    local section="$2"
    local doc_id="$3"  # ESTDX format (e.g., ESTD1)
    local is_current_doc="$4"  # true/false

    local toc=$(sed -n '/^## Table of Contents/,/^## [^#]/p' "$doc_file" | grep -E '^\s*-\s*\[.*\]\(.*\)' || echo "")

    if [[ -z "$toc" ]]; then
        return 1
    fi

    local line=""
    local link_text=""

    # If no section, use document header
    if [[ -z "$section" ]]; then
        line=$(echo "$toc" | head -1)
        # For document headers, use the document ID (same for both current and other docs)
        link_text="$doc_id"
    else
        # Search by number or text
        if [[ $section =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
            line=$(echo "$toc" | grep -E "\\[${section}[ .]" | head -1 || echo "")
        fi

        if [[ -z "$line" ]]; then
            line=$(echo "$toc" | grep -iF "$section" | head -1 || echo "")
        fi

        if [[ -n "$line" ]]; then
            # Extract the section text from the link [SECTION TEXT]
            link_text=$(echo "$line" | sed -E 's/.*\[([^]]*)\].*/\1/')
            if [[ "$is_current_doc" == "true" ]]; then
                link_text="§${link_text}"
            else
                link_text="${doc_id} §${link_text}"
            fi
        else
            return 1
        fi
    fi

    # Extract the anchor (URL part) from the link (...)
    local anchor=$(echo "$line" | sed -E 's/.*\(([^)]*)\).*/\1/')

    # If target is not current document, prefix anchor with relative path to target document
    if [[ "$is_current_doc" != "true" ]]; then
        local target_filename=$(basename "$doc_file")
        local encoded_filename=$(url_encode "$target_filename")
        anchor="./${encoded_filename}${anchor}"
    fi

    echo "[${link_text}](${anchor})"
}

# Create temp file
temp_file=$(mktemp)
trap "rm -f '$temp_file'" EXIT

# Process all lines and perform replacements
{
    while IFS= read -r line; do
        output="$line"

        # Find each [[...]] reference in the line using grep since bash regex has issues with bracket escaping
        ref_matches=$(echo "$output" | grep -oE '\[\[[^]]*\]\]' || echo "")

        while IFS= read -r ref; do
            [[ -z "$ref" ]] && continue

            # Extract content between [[ and ]] by removing first 2 and last 2 characters
            ref_len=${#ref}
            if [[ $ref_len -lt 4 ]]; then
                continue
            fi
            # Manual substring extraction to avoid negative index issues
            ref_content="${ref}"
            ref_content="${ref_content:2}"  # Remove first 2 chars
            ref_content="${ref_content%??}"  # Remove last 2 chars

            replacement=""

            # Parse ESTDX format
            if [[ $ref_content == ESTD* ]]; then
                after="${ref_content#ESTD}"
                doc_num=""
                for ((i=0; i<${#after}; i++)); do
                    ch="${after:$i:1}"
                    if [[ $ch =~ [0-9] ]]; then
                        doc_num+="$ch"
                    else
                        break
                    fi
                done

                if [[ -n "$doc_num" ]]; then
                    section="${after#${doc_num}}"
                    section="${section## }"  # Remove leading space
                    section="${section#§}"   # Remove § symbol
                    section="$(echo "$section" | xargs)"  # Trim

                    doc_file=$(find_estd_doc "$doc_num")
                    if [[ -n "$doc_file" ]]; then
                        target_doc_id="ESTD${doc_num}"
                        is_current="false"
                        [[ "$target_doc_id" == "$current_doc_id" ]] && is_current="true"
                        replacement=$(find_toc_link "$doc_file" "$section" "$target_doc_id" "$is_current" || echo "")
                    fi
                fi
            # Parse §section format
            elif [[ $ref_content == §* ]]; then
                section="${ref_content#§}"
                section="$(echo "$section" | xargs)"  # Trim

                if [[ -n "$current_doc_id" && "$current_doc_id" != ESTD ]]; then
                    doc_num="${current_doc_id#ESTD}"
                    doc_file=$(find_estd_doc "$doc_num")
                    if [[ -n "$doc_file" ]]; then
                        # If section is empty, reference the document header
                        if [[ -z "$section" ]]; then
                            replacement=$(find_toc_link "$doc_file" "" "$current_doc_id" "true" || echo "")
                        else
                            replacement=$(find_toc_link "$doc_file" "$section" "$current_doc_id" "true" || echo "")
                        fi
                    fi
                fi
            fi

            # Replace reference if we found a link, otherwise keep original
            if [[ -n "$replacement" ]]; then
                # Escape for sed - must escape brackets, slashes, and ampersands
                ref_esc=$(printf '%s\n' "$ref" | sed -e 's/\[/\\[/g; s/\]/\\]/g; s/&/\\&/g; s/\//\\\//g')
                replacement_esc=$(printf '%s\n' "$replacement" | sed -e 's/&/\\&/g; s/\//\\\//g')
                output=$(echo "$output" | sed "s/${ref_esc}/${replacement_esc}/")
            fi
        done <<< "$ref_matches"

        echo "$output"
    done < "$markdown_file"
} > "$temp_file"

# Replace original
mv "$temp_file" "$markdown_file"

echo "✓ ESTD references processed in '$markdown_file'."
exit 0
