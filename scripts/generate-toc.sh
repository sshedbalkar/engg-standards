#!/bin/bash

##############################################################################
# Script: generate-toc.sh
# Purpose: Generate and insert a table of contents into a markdown file
#
# Usage: ./generate-toc.sh <markdown_file>
#
# Description:
#   Automatically generates a table of contents (TOC) with proper indentation
#   and anchor links, then inserts it into a markdown file at a marked location.
#
# Technical Approach:
#   1. Line-by-line scan: Reads file to detect code block delimiters (``` or ~~~)
#   2. State tracking: Maintains in_code_block flag to skip content inside fenced code
#   3. Heading extraction: Regex captures markdown headings (^#+\s+) outside code blocks
#   4. Level calculation: Heading depth (# vs ## vs ###) determines indent levels
#   5. Anchor generation: Converts headings to anchors by:
#      - Lowercasing all text
#      - Removing special characters (preserving spaces and hyphens)
#      - Replacing spaces with hyphens (preserving contiguous spacing)
#      - Removing leading/trailing hyphens
#   6. Marker replacement: Finds case-insensitive TOC marker and replaces with content
#
# Returns:
#   0 - Always (success or identifier not found)
##############################################################################

set -euo pipefail

# Validate input
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <markdown_file>"
    exit 1
fi

markdown_file="$1"

# Check if file exists and is readable
if [[ ! -f "$markdown_file" ]]; then
    echo "✗ File '$markdown_file' does not exist."
    exit 1
fi

if [[ ! -r "$markdown_file" ]]; then
    echo "✗ File '$markdown_file' is not readable."
    exit 1
fi

# Check if the identifier exists in the file (case-insensitive, with optional leading/trailing spaces)
if ! grep -qiE "^[[:space:]]*<!-- toc -->[[:space:]]*$" "$markdown_file"; then
    echo "No identifier '<!-- toc -->' found in '$markdown_file'."
    exit 0
fi

# Extract all headings from the markdown file
# Match lines that start with one or more '#' followed by a space
# Skip lines inside code blocks (fenced with ``` or ~~~)
toc_content=""
in_code_block=false
while IFS= read -r line; do
    # Check for code block delimiters (``` or ~~~)
    if [[ $line =~ ^[[:space:]]*(\`\`\`|\~\~\~) ]]; then
        in_code_block=$([ "$in_code_block" = true ] && echo "false" || echo "true")
        continue
    fi

    # Skip processing if inside a code block
    if [[ "$in_code_block" == "true" ]]; then
        continue
    fi

    # Check for markdown heading (must start with # followed by space, but not in code block)
    if [[ $line =~ ^(#+)[[:space:]]+(.*)$ ]]; then
        level="${BASH_REMATCH[1]}"
        heading="${BASH_REMATCH[2]}"

        # Calculate indentation based on heading level
        # h1 = 0 spaces, h2 = 2 spaces, h3 = 4 spaces, etc.
        indent_level=$((${#level} - 1))
        indent=$(printf '%*s' "$((indent_level * 2))" '')

        # Convert heading to anchor format
        # 1. Convert to lowercase
        # 2. Replace all non-alphanumeric and non-space characters with nothing
        # 3. Replace each space with a hyphen (preserving contiguous spaces as contiguous hyphens)
        # 4. Remove leading/trailing hyphens
        anchor=$(echo "$heading" | \
            tr '[:upper:]' '[:lower:]' | \
            sed 's/[^a-z0-9 -]//g' | \
            sed 's/ /-/g' | \
            sed 's/^-*//; s/-*$//')

        # Add to TOC
        toc_content+="${indent}- [$heading](#${anchor})"$'\n'
    fi
done < "$markdown_file"

# Replace the identifier with the TOC content
# Create a temporary file to avoid issues with in-place editing across different systems
temp_file=$(mktemp)
trap "rm -f '$temp_file'" EXIT

# Use sed with a here-document to handle multiline replacement safely
{
    while IFS= read -r line; do
        # Check if line matches the toc marker (case-insensitive, with optional leading/trailing spaces)
        if [[ "$line" =~ ^[[:space:]]*\<\!--[[:space:]]*[tT][oO][cC][[:space:]]*--\>[[:space:]]*$ ]]; then
            printf "%s" "$toc_content"
        else
            echo "$line"
        fi
    done < "$markdown_file"
} > "$temp_file"

# Replace the original file with the updated content
mv "$temp_file" "$markdown_file"

echo "✓ Table of contents successfully inserted into '$markdown_file'."
exit 0
