#!/bin/bash

set -euo pipefail

##############################################################################
# Script: check-context.sh
# Purpose: Validate ESTD shared-context files against current repo contents.
#
# Usage: ./scripts/check-context.sh
#
# Parameters:
#   None
#
# Return Codes:
#   0 - Success
#   1 - Error (missing file, invalid context reference, stale inventory, etc.)
#
# Description:
#   Confirms the shared ESTD memory layer stays aligned with the repository.
#   Validates that every ESTD document has exactly one card, card IDs match
#   current repo docs, repo-map inventory metadata is current, open-work does
#   not point to missing docs, decision-log references stay resolvable, and
#   validator specs stay route-bound to existing ESTD docs.
#
# Technical Approach:
#   Read repo files directly, extract ESTD IDs and file references with grep,
#   compare normalized sorted sets, then fail fast with explicit stderr output.
#
# Examples:
#   ./scripts/check-context.sh
##############################################################################

readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly BOOTSTRAP_FILE="${REPO_ROOT}/AGENTS.md"
readonly DOCS_DIR="${REPO_ROOT}/docs"
readonly CONTEXT_DIR="${REPO_ROOT}/context"
readonly CONTEXT_README_FILE="${CONTEXT_DIR}/README.md"
readonly DOC_CARDS_FILE="${CONTEXT_DIR}/doc-cards.md"
readonly DECISION_LOG_FILE="${CONTEXT_DIR}/decision-log.md"
readonly OPEN_WORK_FILE="${CONTEXT_DIR}/open-work.md"
readonly REPO_MAP_FILE="${CONTEXT_DIR}/repo-map.md"
readonly ROUTING_MAP_FILE="${CONTEXT_DIR}/estd-routing-map.md"
readonly VALIDATORS_DIR="${CONTEXT_DIR}/validators"
readonly VALIDATOR_README_FILE="${VALIDATORS_DIR}/README.md"
readonly STATIC_VALIDATION_FILE="${VALIDATORS_DIR}/static-validation.md"
readonly LLM_VALIDATION_FILE="${VALIDATORS_DIR}/llm-based-validation.md"
readonly ENFORCER_README_FILE="${REPO_ROOT}/tools/estd-enforcer/README.md"
readonly STATIC_REGISTRY_FILE="${REPO_ROOT}/tools/estd-enforcer/static-checks/registry.json"

cleanup() {
    [[ -n "${TEMP_DIR:-}" && -d "${TEMP_DIR}" ]] && rm -rf "${TEMP_DIR}"
}

fail() {
    echo "ERROR: $1" >&2
    exit 1
}

# Verify file exists before validation uses it.
# Arguments:
#   $1 - File path
# Returns:
#   0 - File exists
#   1 - File missing
require_file() {
    local file_path="$1"

    [[ -f "${file_path}" ]] || fail "Required file missing: ${file_path}"
}

# Verify directory exists before validation uses it.
# Arguments:
#   $1 - Directory path
# Returns:
#   0 - Directory exists
#   1 - Directory missing
require_dir() {
    local dir_path="$1"

    [[ -d "${dir_path}" ]] || fail "Required directory missing: ${dir_path}"
}

# Verify a markdown heading exists exactly once before schema-specific checks rely on it.
# Arguments:
#   $1 - Markdown file path
#   $2 - Exact heading text
# Returns:
#   0 - Heading exists
#   1 - Heading missing
require_heading() {
    local markdown_file="$1"
    local heading="$2"

    grep -F -x -- "${heading}" "${markdown_file}" >/dev/null \
		|| fail "Missing heading '${heading}' in ${markdown_file}"
}

# Extract ESTD IDs from docs filenames.
# Arguments:
#   $1 - Output file path
# Outputs:
#   Writes sorted ESTD IDs, one per line
# Returns:
#   0 - Success
extract_repo_doc_ids() {
    local output_file="$1"

    find "${DOCS_DIR}" -maxdepth 1 -type f -name 'ESTD*.md' -print \
        | sed -E 's#.*/(ESTD[0-9]+)_.*#\1#' \
        | sort -V > "${output_file}"
}

# Extract ESTD IDs from card headings.
# Arguments:
#   $1 - Output file path
# Outputs:
#   Writes sorted ESTD IDs, one per line
# Returns:
#   0 - Success
extract_card_ids() {
    local output_file="$1"

    grep -E '^### ESTD[0-9]+$' "${DOC_CARDS_FILE}" \
		| sed -E 's/^### (ESTD[0-9]+)$/\1/' \
		| sort -V > "${output_file}"
}

# Validate local file references in a markdown file.
# Arguments:
#   $1 - Markdown file path
# Returns:
#   0 - All references resolve
#   1 - At least one reference is missing
validate_file_references() {
    local markdown_file="$1"
    local missing=0
    local relative_path=""
    local resolved_path=""

    while IFS= read -r relative_path; do
        [[ -z "${relative_path}" ]] && continue
        [[ "${relative_path}" == *"*"* || "${relative_path}" == *"?"* ]] && continue

        resolved_path="${REPO_ROOT}/${relative_path}"
        [[ -e "${resolved_path}" ]] || {
            echo "ERROR: Missing file reference '${relative_path}' in ${markdown_file}" >&2
            missing=1
        }
    done < <(
        grep -oE '`[^`]+`' "${markdown_file}" \
			| tr -d '`' \
			| sed -E 's|(\.md)#.*$|\1|' \
			| grep -E '(^docs/|^context/|^scripts/|^tools/|^AGENTS\.md$|^README\.md$|^ESTD_PLAN\.md$|^prompts/)'
    )

    [[ "${missing}" -eq 0 ]] || exit 1
}

# Extract route IDs from the routing map in file order.
# Arguments:
#   $1 - Output file path
# Outputs:
#   Writes route IDs, one per line
# Returns:
#   0 - Success
extract_route_ids() {
	local output_file="$1"

	grep -E '^### route\.[a-z0-9-]+$' "${ROUTING_MAP_FILE}" \
		| sed -E 's/^### (route\.[a-z0-9-]+)$/\1/' \
		> "${output_file}"
}

# Validate shared cache files follow the lookup schema from the framework spec.
# Arguments:
#   $1 - File containing valid ESTD IDs, one per line
# Returns:
#   0 - Cache schema is valid
#   1 - Any cache schema requirement is missing or stale
validate_shared_cache_schema() {
	local repo_doc_ids_file="$1"
	local route_ids_file="${TEMP_DIR}/route-ids.txt"
	local sorted_route_ids_file="${TEMP_DIR}/route-ids-sorted.txt"
	local validator_routes_file="${TEMP_DIR}/validator-routes.txt"
	local sorted_validator_routes_file="${TEMP_DIR}/validator-routes-sorted.txt"
	local actual_doc_count
	local route_id=""

	require_file "${BOOTSTRAP_FILE}"
	head -n 1 "${BOOTSTRAP_FILE}" | grep -F -x -- "# Engg Standards Agent Guide" >/dev/null \
		|| fail "AGENTS.md title must follow bootstrap schema"
	grep -F -x -- "project_state: mature_repo" "${BOOTSTRAP_FILE}" >/dev/null \
		|| fail "AGENTS.md missing project_state"
	grep -F -x -- "project_foundation_file: README.md" "${BOOTSTRAP_FILE}" >/dev/null \
		|| fail "AGENTS.md missing project_foundation_file"
	require_heading "${BOOTSTRAP_FILE}" "## Read Order"
	require_heading "${BOOTSTRAP_FILE}" "## Cache Update Rule"

	head -n 1 "${REPO_MAP_FILE}" | grep -F -x -- "# Repo Map" >/dev/null \
		|| fail "repo-map title must follow framework schema"
	require_heading "${REPO_MAP_FILE}" "## Lookup Strategy"
	require_heading "${REPO_MAP_FILE}" "## Jump Index"
	require_heading "${REPO_MAP_FILE}" "## Source Truth"
	require_heading "${REPO_MAP_FILE}" "## Shared Context"
	require_heading "${REPO_MAP_FILE}" "## Validation"

	head -n 1 "${DECISION_LOG_FILE}" | grep -F -x -- "# Decision Log" >/dev/null \
		|| fail "decision-log title must follow framework schema"
	grep -F -x -- "| Date | Decision | Affected Nodes | Source References |" "${DECISION_LOG_FILE}" >/dev/null \
		|| fail "decision-log table header must follow framework schema"

	head -n 1 "${OPEN_WORK_FILE}" | grep -F -x -- "# Open Work" >/dev/null \
		|| fail "open-work title must follow framework schema"
	grep -F -x -- "| Problem | Target Nodes | Expected End State | Removal Condition |" "${OPEN_WORK_FILE}" >/dev/null \
		|| fail "open-work table header must follow framework schema"

	require_heading "${DOC_CARDS_FILE}" "## Lookup Strategy"
	require_heading "${DOC_CARDS_FILE}" "## Jump Index"
	require_heading "${DOC_CARDS_FILE}" "## Cards"
	validate_file_references "${DOC_CARDS_FILE}"
	validate_estd_id_references "${DOC_CARDS_FILE}" "${repo_doc_ids_file}"

	actual_doc_count="$(wc -l < "${repo_doc_ids_file}" | tr -d ' ')"
	[[ "$(grep -Ec '^- path: `docs/ESTD[0-9]+_.*\.md`$' "${DOC_CARDS_FILE}")" == "${actual_doc_count}" ]] \
		|| fail "doc-cards must have one path per ESTD card"
	[[ "$(grep -Fc -- "- kind: estd-doc" "${DOC_CARDS_FILE}")" == "${actual_doc_count}" ]] \
		|| fail "doc-cards must mark every card as kind: estd-doc"
	[[ "$(grep -Fc -- "- state: verified" "${DOC_CARDS_FILE}")" == "${actual_doc_count}" ]] \
		|| fail "doc-cards must mark verified cards after validation"

	require_heading "${ROUTING_MAP_FILE}" "## Lookup Strategy"
	require_heading "${ROUTING_MAP_FILE}" "## Jump Index"
	require_heading "${ROUTING_MAP_FILE}" "## Routes"
	extract_route_ids "${route_ids_file}"
	sort "${route_ids_file}" > "${sorted_route_ids_file}"
	diff -u "${sorted_route_ids_file}" "${route_ids_file}" >/dev/null \
		|| fail "routing map routes must be sorted by route ID"
	while IFS= read -r route_id; do
		[[ -z "${route_id}" ]] && continue
		grep -F -x -- "- ${route_id}" "${ROUTING_MAP_FILE}" >/dev/null \
			|| fail "routing map Jump Index missing ${route_id}"
		awk -v heading="### ${route_id}" '
			$0 == heading { in_route = 1; next }
			in_route && /^### route\./ { exit }
			in_route && /^- Known coverage notes:/ { found = 1 }
			END { exit found ? 0 : 1 }
		' "${ROUTING_MAP_FILE}" \
			|| fail "routing map route missing Known coverage notes: ${route_id}"
	done < "${route_ids_file}"

	require_heading "${VALIDATOR_README_FILE}" "## Lookup Strategy"
	require_heading "${VALIDATOR_README_FILE}" "## Jump Index"
	require_heading "${VALIDATOR_README_FILE}" "## Validator Inventory"
	head -n 1 "${VALIDATOR_README_FILE}" | grep -F -x -- "# Validator Specs" >/dev/null \
		|| fail "validator README title must follow framework schema"
	awk -F'|' '/^\| `validator\./ {
		route = $3
		gsub(/[ `]/, "", route)
		print route
	}' "${VALIDATOR_README_FILE}" > "${validator_routes_file}"
	sort "${validator_routes_file}" > "${sorted_validator_routes_file}"
	diff -u "${sorted_validator_routes_file}" "${validator_routes_file}" >/dev/null \
		|| fail "validator inventory must be sorted by bound route ID"
	while IFS= read -r route_id; do
		[[ -z "${route_id}" ]] && continue
		grep -F -x -- "- ${route_id}" "${VALIDATOR_README_FILE}" >/dev/null \
			|| fail "validator README Jump Index missing ${route_id}"
	done < "${validator_routes_file}"

	require_heading "${STATIC_VALIDATION_FILE}" "## Lookup Strategy"
	require_heading "${STATIC_VALIDATION_FILE}" "## Jump Index"
	require_heading "${LLM_VALIDATION_FILE}" "## Lookup Strategy"
	require_heading "${LLM_VALIDATION_FILE}" "## Jump Index"
}

# Validate all ESTD ID references in a markdown file exist in docs/.
# Arguments:
#   $1 - Markdown file path
#   $2 - File containing valid ESTD IDs, one per line
# Returns:
#   0 - All references resolve
#   1 - At least one reference is unknown
validate_estd_id_references() {
    local markdown_file="$1"
    local repo_doc_ids_file="$2"
    local doc_id=""

    while IFS= read -r doc_id; do
        [[ -z "${doc_id}" ]] && continue

        grep -F -x -- "${doc_id}" "${repo_doc_ids_file}" >/dev/null \
            || fail "Unknown ESTD reference '${doc_id}' in ${markdown_file}"
    done < <(
        { grep -Eo 'ESTD[0-9]+' "${markdown_file}" || true; } | sort -uV
    )
}

# Validate a validator spec has mandatory metadata and score weights.
# Arguments:
#   $1 - Validator markdown file path
# Returns:
#   0 - Validator contract is valid
#   1 - Validator contract is invalid
validate_validator_contract() {
    local validator_file="$1"
    local validator_id_count
    local validator_id
    local route_count
    local route_id
    local weight_total

    validator_id_count="$(grep -Ec '^- Validator ID: `validator\.[a-z0-9-]+`$' "${validator_file}" || true)"
    [[ "${validator_id_count}" == "1" ]] \
        || fail "Validator must have exactly one Validator ID line: ${validator_file}"

    validator_id="$(grep -E '^- Validator ID: `validator\.[a-z0-9-]+`$' "${validator_file}" \
		| sed -E 's/^- Validator ID: `(validator\.[^`]+)`$/\1/')"

    head -n 1 "${validator_file}" | grep -F -x -- "# ${validator_id}" >/dev/null \
		|| fail "Validator heading must match Validator ID '${validator_id}': ${validator_file}"

    route_count="$(grep -Ec '^- Route: `route\.[a-z0-9-]+`$' "${validator_file}" || true)"
    [[ "${route_count}" == "1" ]] \
        || fail "Validator must have exactly one Route line: ${validator_file}"

    route_id="$(grep -E '^- Route: `route\.[a-z0-9-]+`$' "${validator_file}" \
        | sed -E 's/^- Route: `(route\.[^`]+)`$/\1/')"

    grep -F -x -- "### ${route_id}" "${ROUTING_MAP_FILE}" >/dev/null \
        || fail "Validator route '${route_id}' not found in ${ROUTING_MAP_FILE}"

    sed -n '3p' "${validator_file}" | grep -F -x -- "- Validator ID: \`${validator_id}\`" >/dev/null \
		|| fail "Validator ID must be the first metadata field: ${validator_file}"
    sed -n '4p' "${validator_file}" | grep -F -x -- "- Route: \`${route_id}\`" >/dev/null \
		|| fail "Validator route must be the second metadata field: ${validator_file}"
    sed -n '5p' "${validator_file}" | grep -Eq '^- Source docs: `ESTD[0-9]+`' \
		|| fail "Validator Source docs must be the third metadata field: ${validator_file}"
    sed -n '6p' "${validator_file}" | grep -Eq '^- Overlay docs: ' \
		|| fail "Validator Overlay docs must be the fourth metadata field: ${validator_file}"
    sed -n '7p' "${validator_file}" | grep -Eq '^- Applies to: ' \
		|| fail "Validator Applies to must be the fifth metadata field: ${validator_file}"
    sed -n '8p' "${validator_file}" | grep -F -x -- "- Pass threshold: > 75% code conformity." >/dev/null \
		|| fail "Validator pass threshold must be the sixth metadata field: ${validator_file}"

    grep -F -x -- "- Pass threshold: > 75% code conformity." "${validator_file}" >/dev/null \
        || fail "Validator pass threshold must be '> 75% code conformity': ${validator_file}"

    grep -Eq '^- Source docs: `ESTD[0-9]+`' "${validator_file}" \
		|| fail "Validator missing Source docs line: ${validator_file}"

    grep -Eq '^- Overlay docs: ' "${validator_file}" \
		|| fail "Validator missing Overlay docs line: ${validator_file}"

    ! grep -Eq '^- (Source|Overlay) ESTD docs: ' "${validator_file}" \
		|| fail "Validator still uses old ESTD docs metadata fields: ${validator_file}"

    grep -Eq '^- Applies to: ' "${validator_file}" \
        || fail "Validator missing Applies to line: ${validator_file}"

    grep -F -x -- "## Scoring" "${validator_file}" >/dev/null \
        || fail "Validator missing Scoring section: ${validator_file}"

    grep -F -x -- "## Check Groups" "${validator_file}" >/dev/null \
        || fail "Validator missing Check Groups section: ${validator_file}"

    grep -F -x -- "## Static Coverage" "${validator_file}" >/dev/null \
		|| fail "Validator missing Static Coverage section: ${validator_file}"

    grep -F -x -- "## LLM Gap Review" "${validator_file}" >/dev/null \
		|| fail "Validator missing LLM Gap Review section: ${validator_file}"

    grep -F -x -- "## Evolution Rules" "${validator_file}" >/dev/null \
		|| fail "Validator missing Evolution Rules section: ${validator_file}"

    ! grep -F -x -- "## Evolution Hooks" "${validator_file}" >/dev/null \
		|| fail "Validator still uses old Evolution Hooks heading: ${validator_file}"

    weight_total="$(
        awk -F'|' '
            /^\|/ && $3 ~ /^[[:space:]]*[0-9]+[[:space:]]*$/ {
                gsub(/[[:space:]]/, "", $3)
                sum += $3
            }
            END { print sum + 0 }
        ' "${validator_file}"
    )"
    [[ "${weight_total}" == "100" ]] \
        || fail "Validator check group weights must total 100, got ${weight_total}: ${validator_file}"
}

# Extract registered static check IDs from the static registry.
# Arguments:
#   $1 - Output file path
# Outputs:
#   Writes sorted static check IDs, one per line
# Returns:
#   0 - Success
extract_static_registry_ids() {
	local output_file="$1"

	grep -E '"id": "static\.[^"]+"' "${STATIC_REGISTRY_FILE}" \
		| sed -E 's/.*"id": "([^"]+)".*/\1/' \
		| sort -u > "${output_file}"
}

# Extract Static Coverage rows from route-bound validator specs.
# Outputs:
#   Tab-delimited rows: group, static check IDs, LLM gap
# Returns:
#   0 - Success
extract_static_coverage_rows() {
	find "${VALIDATORS_DIR}" -maxdepth 1 -type f -name '*-validator.md' -print \
		| sort \
		| while IFS= read -r validator_file; do
			awk -F'|' '
				/^## Static Coverage$/ { in_static = 1; next }
				in_static && /^## / { in_static = 0 }
				in_static && /^\|/ && $0 !~ /---/ && $2 !~ /^[[:space:]]*Group[[:space:]]*$/ {
					group = $2
					ids = $3
					gap = $4
					gsub(/^[[:space:]]+|[[:space:]]+$/, "", group)
					gsub(/^[[:space:]]+|[[:space:]]+$/, "", ids)
					gsub(/^[[:space:]]+|[[:space:]]+$/, "", gap)
					if (group != "") {
						printf "%s\t%s\t%s\n", group, ids, gap
					}
				}
			' "${validator_file}"
		done
}

# Extract Check Groups rows from route-bound validator specs.
# Outputs:
#   Tab-delimited rows: group, weight, ESTD sources, validator focus
# Returns:
#   0 - Success
extract_validator_group_rows() {
	find "${VALIDATORS_DIR}" -maxdepth 1 -type f -name '*-validator.md' -print \
		| sort \
		| while IFS= read -r validator_file; do
			awk -F'|' '
				/^\|/ && $3 ~ /^[[:space:]]*[0-9]+[[:space:]]*$/ {
					group = $2
					weight = $3
					sources = $4
					focus = $5
					gsub(/^[[:space:]]+|[[:space:]]+$/, "", group)
					gsub(/^[[:space:]]+|[[:space:]]+$/, "", weight)
					gsub(/^[[:space:]]+|[[:space:]]+$/, "", sources)
					gsub(/^[[:space:]]+|[[:space:]]+$/, "", focus)
					if (group != "") {
						printf "%s\t%s\t%s\t%s\n", group, weight, sources, focus
					}
				}
			' "${validator_file}"
		done
}

# Validate static and LLM inventory docs stay aligned with validator specs.
# Arguments:
#   $1 - File containing valid ESTD IDs, one per line
# Returns:
#   0 - Inventory docs are aligned
#   1 - Any inventory doc is missing required content
validate_validation_inventory_docs() {
	local repo_doc_ids_file="$1"
	local static_ids_file="${TEMP_DIR}/static-registry-ids.txt"
	local check_id=""
	local group=""
	local static_ids=""
	local llm_gap=""
	local weight=""
	local sources=""
	local focus=""
	local used_check_id=""

	require_file "${STATIC_VALIDATION_FILE}"
	require_file "${LLM_VALIDATION_FILE}"
	require_file "${ENFORCER_README_FILE}"
	require_file "${STATIC_REGISTRY_FILE}"

	validate_file_references "${STATIC_VALIDATION_FILE}"
	validate_file_references "${LLM_VALIDATION_FILE}"
	validate_file_references "${ENFORCER_README_FILE}"
	validate_estd_id_references "${STATIC_VALIDATION_FILE}" "${repo_doc_ids_file}"
	validate_estd_id_references "${LLM_VALIDATION_FILE}" "${repo_doc_ids_file}"

	grep -F -- "\`context/validators/static-validation.md\`" "${VALIDATOR_README_FILE}" >/dev/null \
		|| fail "Validator README missing static validation inventory link"
	grep -F -- "\`context/validators/llm-based-validation.md\`" "${VALIDATOR_README_FILE}" >/dev/null \
		|| fail "Validator README missing LLM validation inventory link"
	grep -F -- "\`context/validators/static-validation.md\`" "${ENFORCER_README_FILE}" >/dev/null \
		|| fail "Enforcer README missing static validation inventory link"
	grep -F -- "\`context/validators/llm-based-validation.md\`" "${ENFORCER_README_FILE}" >/dev/null \
		|| fail "Enforcer README missing LLM validation inventory link"

	extract_static_registry_ids "${static_ids_file}"
	while IFS= read -r check_id; do
		[[ -z "${check_id}" ]] && continue
		grep -F -- "\`${check_id}\`" "${STATIC_VALIDATION_FILE}" >/dev/null \
			|| fail "Static validation inventory missing registered check ${check_id}"
	done < "${static_ids_file}"

	while IFS= read -r used_check_id; do
		[[ -z "${used_check_id}" ]] && continue
		grep -F -x -- "${used_check_id}" "${static_ids_file}" >/dev/null \
			|| fail "Validator Static Coverage references unregistered check ${used_check_id}"
	done < <(
		{ grep -Eoh '`static\.[a-z0-9.-]+`' "${VALIDATORS_DIR}"/*-validator.md || true; } \
			| tr -d '`' \
			| sort -u
	)

	while IFS=$'\t' read -r group static_ids llm_gap; do
		[[ -z "${group}" ]] && continue
		grep -F -- "| ${group} | ${static_ids} | ${llm_gap} |" "${STATIC_VALIDATION_FILE}" >/dev/null \
			|| fail "Static validation inventory missing Static Coverage row: ${group}"
		grep -F -- "${llm_gap}" "${LLM_VALIDATION_FILE}" >/dev/null \
			|| fail "LLM validation inventory missing LLM gap: ${llm_gap}"
	done < <(extract_static_coverage_rows)

	while IFS=$'\t' read -r group weight sources focus; do
		[[ -z "${group}" ]] && continue
		grep -F -- "| ${group} | ${weight} | ${sources} | ${focus};" "${LLM_VALIDATION_FILE}" >/dev/null \
			|| fail "LLM validation inventory missing Check Group row: ${group}"
		grep -F -- "${group}" "${STATIC_VALIDATION_FILE}" >/dev/null \
			|| fail "Static validation inventory missing validator group: ${group}"
	done < <(extract_validator_group_rows)
}

# Validate context/validators specs against route map and ESTD docs.
# Arguments:
#   $1 - File containing valid ESTD IDs, one per line
# Returns:
#   0 - Validator specs are valid
#   1 - Any validator spec is invalid
validate_validator_specs() {
    local repo_doc_ids_file="$1"
    local expected_validator_files=(
        "unity-client-validator.md"
        "php-monolith-validator.md"
		"java-seam-api-validator.md"
        "smartfox-server-validator.md"
		"database-validator.md"
		"cloud-aws-validator.md"
		"jenkins-cicd-validator.md"
        "product-website-validator.md"
        "web-tools-validator.md"
		"internal-scripts-validator.md"
		"technical-docs-validator.md"
    )
    local validator_name=""
    local validator_file=""
    local relative_path=""

    require_dir "${VALIDATORS_DIR}"
    require_file "${VALIDATOR_README_FILE}"

    validate_file_references "${VALIDATOR_README_FILE}"
    validate_estd_id_references "${VALIDATOR_README_FILE}" "${repo_doc_ids_file}"
    grep -F -x -- "- pass threshold: > 75% code conformity." "${VALIDATOR_README_FILE}" >/dev/null \
        || fail "Validator README missing shared pass threshold"
    validate_validation_inventory_docs "${repo_doc_ids_file}"

    for validator_name in "${expected_validator_files[@]}"; do
        validator_file="${VALIDATORS_DIR}/${validator_name}"
        require_file "${validator_file}"
    done

    while IFS= read -r validator_file; do
        [[ -z "${validator_file}" ]] && continue
        relative_path="${validator_file#${REPO_ROOT}/}"

        grep -F -- "\`${relative_path}\`" "${VALIDATOR_README_FILE}" >/dev/null \
            || fail "Validator README missing inventory entry for ${relative_path}"

        validate_file_references "${validator_file}"
        validate_estd_id_references "${validator_file}" "${repo_doc_ids_file}"
        validate_validator_contract "${validator_file}"
    done < <(find "${VALIDATORS_DIR}" -maxdepth 1 -type f -name '*-validator.md' -print | sort)
}

# Validate repo inventory values stored in repo-map.
# Returns:
#   0 - Inventory values current
#   1 - Any inventory value stale or missing
validate_repo_inventory() {
    local actual_doc_count
    local actual_latest_id
    local actual_next_id
    local expected_doc_count_line
    local expected_latest_id_line
    local expected_next_id_line

    actual_doc_count="$(find "${DOCS_DIR}" -maxdepth 1 -type f -name 'ESTD*.md' | wc -l | tr -d ' ')"
    actual_latest_id="$(find "${DOCS_DIR}" -maxdepth 1 -type f -name 'ESTD*.md' -print \
        | sed -E 's#.*/ESTD([0-9]+)_.*#\1#' | sort -n | tail -1)"
    actual_next_id="$((actual_latest_id + 1))"

    expected_doc_count_line="- ESTD doc count: ${actual_doc_count}"
    expected_latest_id_line="- Latest ESTD ID in repo: ESTD${actual_latest_id}"
    expected_next_id_line="- Next available ESTD ID: ESTD${actual_next_id}"

    grep -F -x -- "${expected_doc_count_line}" "${REPO_MAP_FILE}" >/dev/null \
        || fail "repo-map doc count is stale"
    grep -F -x -- "${expected_latest_id_line}" "${REPO_MAP_FILE}" >/dev/null \
        || fail "repo-map latest ESTD ID is stale"
    grep -F -x -- "${expected_next_id_line}" "${REPO_MAP_FILE}" >/dev/null \
        || fail "repo-map next ESTD ID is stale"
}

main() {
    TEMP_DIR="$(mktemp -d)"
    trap cleanup EXIT

    require_file "${CONTEXT_README_FILE}"
    require_file "${DOC_CARDS_FILE}"
    require_file "${DECISION_LOG_FILE}"
    require_file "${OPEN_WORK_FILE}"
    require_file "${REPO_MAP_FILE}"
    require_file "${ROUTING_MAP_FILE}"

    extract_repo_doc_ids "${TEMP_DIR}/repo-doc-ids.txt"
    extract_card_ids "${TEMP_DIR}/card-ids.txt"

    diff -u "${TEMP_DIR}/repo-doc-ids.txt" "${TEMP_DIR}/card-ids.txt" >/dev/null \
        || fail "doc-cards ESTD IDs do not match docs/ inventory"

    if [[ "$(uniq -d "${TEMP_DIR}/card-ids.txt" | wc -l | tr -d ' ')" != "0" ]]; then
        fail "doc-cards contains duplicate ESTD card headings"
    fi

    validate_shared_cache_schema "${TEMP_DIR}/repo-doc-ids.txt"
    validate_repo_inventory
    validate_file_references "${CONTEXT_README_FILE}"
    validate_file_references "${ROUTING_MAP_FILE}"
    validate_file_references "${OPEN_WORK_FILE}"
    validate_file_references "${DECISION_LOG_FILE}"
    validate_estd_id_references "${ROUTING_MAP_FILE}" "${TEMP_DIR}/repo-doc-ids.txt"
    validate_validator_specs "${TEMP_DIR}/repo-doc-ids.txt"

    echo "Context validation passed."
}

main "$@"
