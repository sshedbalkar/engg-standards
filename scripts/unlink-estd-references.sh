#!/bin/bash

##############################################################################
# Script: unlink-estd-references.sh
# Purpose: Convert resolved ESTD markdown links back to soft references
#
# Usage: ./unlink-estd-references.sh <markdown_file>
#
# Parameters:
#   <markdown_file>   - Path to the markdown file to process (required)
#
# Return Codes:
#   0 - Success (links converted or none found)
#   1 - Error (file not found or invalid usage)
#
# Description:
#   Reverses what link-estd-references.sh does. Scans a markdown file for
#   resolved ESTD links and converts them back to soft [[...]] references.
#
#   Recognized resolved link formats:
#   - [§4.4 Request Cancellation](#44-request-cancellation)  → [[§4.4]]
#   - [ESTD3 §7. Memory...](./ESTD3_-_...md#7-memory-...)   → [[ESTD3 §7]]
#   - [ESTD1](./ESTD1_-_...md#estd1---...)                  → [[ESTD1]]
#
#   The Table of Contents section is skipped to avoid converting TOC links.
#   Lines inside fenced code blocks are skipped.
#
# Technical Approach:
#   1. Line-by-line processing with TOC and code block tracking
#   2. Three grep patterns detect cross-doc header, cross-doc section,
#      and internal section links (processed most-specific first)
#   3. Section number extracted from link text (digits+dots after §)
#   4. Soft reference built and sed-replaced into the line
#   5. Result written via temp file for atomic replacement
#
# Examples:
#   ./unlink-estd-references.sh ESTD2_-_General_Client_Engg_Standards.md
##############################################################################

set -euo pipefail

# Validate input
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <markdown_file>" >&2
    exit 1
fi

markdown_file="$1"

if [[ ! -f "$markdown_file" ]]; then
    echo "Error: File '$markdown_file' does not exist." >&2
    exit 1
fi

# Extract section number from link text after §
# From "§4.4 Request Cancellation" extracts "4.4"
# From "§21. Accessibility" extracts "21"
# Arguments:
#   $1 - Text after § symbol
# Outputs:
#   Section number string (digits and dots)
# Returns:
#   0 - Always
extract_section_number() {
    local text="$1"
    local num=""
    local ch

    for ((i=0; i<${#text}; i++)); do
        ch="${text:$i:1}"
        if [[ $ch =~ [0-9] ]]; then
            num+="$ch"
        elif [[ $ch == "." && -n "$num" ]]; then
            # Dot is part of section number only if followed by digit
            if (( i + 1 < ${#text} )) && [[ "${text:$((i+1)):1}" =~ [0-9] ]]; then
                num+="$ch"
            else
                break
            fi
        else
            break
        fi
    done

    echo "$num"
}

# Convert a resolved ESTD link to its soft reference
# Arguments:
#   $1 - The full matched link string
# Outputs:
#   Soft reference string (e.g., [[§4.4]], [[ESTD3 §7]], [[ESTD1]])
# Returns:
#   0 - Conversion successful
#   1 - Link format not recognized
resolve_to_soft() {
    local match="$1"

    # Extract link text (between [ and ])
    local link_text
    link_text=$(echo "$match" | sed -E 's/^\[([^]]*)\].*/\1/')

    # Cross-doc header: [ESTD1](./...)
    if [[ $link_text =~ ^ESTD[0-9]+$ ]]; then
        echo "[[${link_text}]]"
        return 0
    fi

    # Cross-doc section: [ESTD3 §TEXT](./...)
    if [[ $link_text =~ ^(ESTD[0-9]+)\ §(.+)$ ]]; then
        local doc_id="${BASH_REMATCH[1]}"
        local after_section="${BASH_REMATCH[2]}"
        local section_num
        section_num=$(extract_section_number "$after_section")
        if [[ -n "$section_num" ]]; then
            echo "[[${doc_id} §${section_num}]]"
            return 0
        fi
        return 1
    fi

    # Internal section: [§TEXT](#...)
    if [[ $link_text =~ ^§(.+)$ ]]; then
        local after_section="${BASH_REMATCH[1]}"
        local section_num
        section_num=$(extract_section_number "$after_section")
        if [[ -n "$section_num" ]]; then
            echo "[[§${section_num}]]"
            return 0
        fi
        return 1
    fi

    return 1
}

# Create temp file
temp_file=$(mktemp)
trap "rm -f '$temp_file'" EXIT

in_toc=0
in_code_block=0

# Process all lines
{
    while IFS= read -r line; do
        output="$line"

        # Track fenced code blocks
        if [[ $line =~ ^(\`\`\`|~~~) ]]; then
            if (( in_code_block )); then
                in_code_block=0
            else
                in_code_block=1
            fi
            echo "$output"
            continue
        fi

        # Skip lines inside code blocks
        if (( in_code_block )); then
            echo "$output"
            continue
        fi

        # Track TOC section — skip it entirely
        if [[ $line =~ ^##\ Table\ of\ Contents ]]; then
            in_toc=1
            echo "$output"
            continue
        fi
        if (( in_toc )); then
            # TOC ends at the next ## heading
            if [[ $line =~ ^##\  && ! $line =~ ^##\ Table\ of\ Contents ]]; then
                in_toc=0
            else
                echo "$output"
                continue
            fi
        fi

        # Pattern 1: Cross-doc section [ESTD3 §TEXT](./...#...)
        # Pattern 2: Cross-doc header [ESTD1](./...#...)
        # Pattern 3: Internal section [§TEXT](#...)
        # Process cross-doc first (more specific), then internal
        matches=$(echo "$output" | grep -oE '\[ESTD[0-9]+ §[^]]+\]\(\./[^)]+\)|\[ESTD[0-9]+\]\(\./[^)]+\)|\[§[^]]+\]\(#[^)]+\)' || echo "")

        while IFS= read -r match; do
            [[ -z "$match" ]] && continue

            soft_ref=$(resolve_to_soft "$match" || echo "")

            if [[ -n "$soft_ref" ]]; then
                # Escape for sed
                match_esc=$(printf '%s\n' "$match" | sed -e 's/\[/\\[/g; s/\]/\\]/g; s/&/\\&/g; s/\//\\\//g')
                soft_esc=$(printf '%s\n' "$soft_ref" | sed -e 's/\[/\\[/g; s/\]/\\]/g; s/&/\\&/g; s/\//\\\//g')
                output=$(echo "$output" | sed "s/${match_esc}/${soft_esc}/")
            fi
        done <<< "$matches"

        echo "$output"
    done < "$markdown_file"
} > "$temp_file"

# Replace original
mv "$temp_file" "$markdown_file"

echo "✓ resolved ESTD links converted to soft references in '$markdown_file'."
exit 0
