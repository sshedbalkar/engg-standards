#!/bin/bash

set -euo pipefail

##############################################################################
# Script: test-estd-enforce.sh
# Purpose: Validate the ESTD enforcer CLI gate behavior and route selection.
#
# Usage: ./tools/estd-enforcer/tests/test-estd-enforce.sh
#
# Parameters:
#   None
#
# Return Codes:
#   0 - Success
#   1 - Test failure
#
# Description:
#   Runs the CLI against fixture repositories and precomputed LLM reports. Tests
#   cover static-first behavior, pass/fail gate semantics, missing citation
#   detection, expired exception handling, and route selection.
##############################################################################

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ENFORCER_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly STANDARDS_ROOT="$(cd "${ENFORCER_ROOT}/../.." && pwd)"
readonly CLI="${ENFORCER_ROOT}/bin/estd-enforce"
readonly REPORTS_DIR="${SCRIPT_DIR}/fixtures/reports"
readonly REPOS_DIR="${SCRIPT_DIR}/fixtures/repos"
readonly TEMP_DIR="$(mktemp -d)"

cleanup() {
	rm -rf "${TEMP_DIR}"
}

fail() {
	echo "ERROR: $1" >&2
	exit 1
}

run_expect_code() {
	local expected_code="$1"
	shift
	local actual_code=0

	"$@" >/dev/null 2>&1 || actual_code="$?"
	[[ "${actual_code}" == "${expected_code}" ]] \
		|| fail "Expected exit ${expected_code}, got ${actual_code}: $*"
}

mark_opted_in() {
	local repo="$1"

	mkdir -p "${repo}/standards"
	ln -s "${STANDARDS_ROOT}" "${repo}/standards/bingo-bash-standards"
	cat > "${repo}/.gitmodules" <<GITMODULES
[submodule "standards/bingo-bash-standards"]
	path = standards/bingo-bash-standards
	url = ${STANDARDS_ROOT}
GITMODULES
}

copy_opted_in_fixture() {
	local repo_name="$1"
	local dest_name="$2"
	local dest="${TEMP_DIR}/${dest_name}"

	mkdir -p "${dest}"
	cp -R "${REPOS_DIR}/${repo_name}/." "${dest}/"
	mark_opted_in "${dest}"
	printf '%s\n' "${dest}"
}

assert_request_has_route() {
	local repo_name="$1"
	local expected_route="$2"
	local output_dir="${TEMP_DIR}/${repo_name}"
	local repo

	repo="$(copy_opted_in_fixture "${repo_name}" "route-${repo_name}")"

	run_expect_code 0 \
		"${CLI}" validate \
		--repo "${repo}" \
		--scope full-repo \
		--out "${output_dir}" \
		--report "${REPORTS_DIR}/pass.json"

	grep -F -- "${expected_route}" "${output_dir}/report.json" >/dev/null \
		|| fail "Expected ${expected_route} in report for ${repo_name}"
}

test_gate_semantics() {
	local repo

	repo="$(copy_opted_in_fixture "web-tools" "gate-web-tools")"

	run_expect_code 0 "${CLI}" validate --repo "${repo}" --scope full-repo --out "${TEMP_DIR}/pass" --report "${REPORTS_DIR}/pass.json"
	run_expect_code 1 "${CLI}" validate --repo "${repo}" --scope full-repo --out "${TEMP_DIR}/fail-score" --report "${REPORTS_DIR}/fail-score.json"
	run_expect_code 1 "${CLI}" validate --repo "${repo}" --scope full-repo --out "${TEMP_DIR}/unknown" --report "${REPORTS_DIR}/unknown-evidence.json"
	run_expect_code 2 "${CLI}" validate --repo "${repo}" --scope full-repo --out "${TEMP_DIR}/missing-citation" --report "${REPORTS_DIR}/missing-citation.json"
}

test_non_opted_repo_is_out_of_scope() {
	local repo="${TEMP_DIR}/non-opted-repo"
	local output_dir="${TEMP_DIR}/non-opted"

	mkdir -p "${repo}/src"
	printf 'export const apiKey = "abcdefghijklmnopqrstuvwxyz";\n' > "${repo}/src/leak.ts"
	run_expect_code 0 "${CLI}" validate --repo "${repo}" --scope full-repo --out "${output_dir}"

	[[ -f "${output_dir}/report.json" ]] || fail "Expected report.json"
	[[ ! -f "${output_dir}/static-report.json" ]] || fail "Did not expect static validation for non-opted repo"
	grep -F -- 'ESTD standards submodule is not configured' "${output_dir}/report.json" >/dev/null \
		|| fail "Expected non-applicable opt-in reason"
}

test_static_only_pass_skips_llm() {
	local repo="${TEMP_DIR}/empty-repo"
	local output_dir="${TEMP_DIR}/static-only"

	mkdir -p "${repo}"
	mark_opted_in "${repo}"
	run_expect_code 0 "${CLI}" validate --repo "${repo}" --scope full-repo --out "${output_dir}"

	[[ -f "${output_dir}/static-report.json" ]] || fail "Expected static-report.json"
	[[ ! -f "${output_dir}/llm-request.md" ]] || fail "Did not expect LLM request for static-only pass"
	grep -F -- '"llmInvoked": false' "${output_dir}/report.json" >/dev/null \
		|| fail "Expected llmInvoked false"
}

test_optional_static_tool_gap_invokes_llm() {
	local output_dir="${TEMP_DIR}/optional-gap"
	local repo

	repo="$(copy_opted_in_fixture "web-tools" "optional-gap-web-tools")"

	run_expect_code 0 "${CLI}" validate --repo "${repo}" --scope full-repo --out "${output_dir}" --report "${REPORTS_DIR}/pass.json"

	[[ -f "${output_dir}/llm-request.md" ]] || fail "Expected LLM request for optional static gap"
	grep -F -- '"checkId": "static.web.typescript"' "${output_dir}/static-report.json" >/dev/null \
		|| fail "Expected TypeScript static result"
	grep -F -- '"status": "skipped"' "${output_dir}/static-report.json" >/dev/null \
		|| fail "Expected skipped optional static result"
}

test_required_static_tool_missing_is_tool_error() {
	local repo="${TEMP_DIR}/required-tool-repo"

	mkdir -p "${repo}/src" "${repo}/.estd"
	mark_opted_in "${repo}"
	printf 'export const value = 1;\n' > "${repo}/src/example.ts"
	cat > "${repo}/.estd/config.yaml" <<'YAML'
version: 2
standardsPath: standards/bingo-bash-standards
profile: auto
mode: blocking
scope: full-repo
minScore: 75
failOnCritical: true
validationStrategy: static-first
llmPolicy: gaps-only
requiredStaticTools: [static.web.eslint]
exceptionsFile: .estd/exceptions.yaml
YAML

	run_expect_code 2 \
		"${CLI}" validate \
		--repo "${repo}" \
		--config "${repo}/.estd/config.yaml" \
		--out "${TEMP_DIR}/required-tool" \
		--report "${REPORTS_DIR}/pass.json"
}

test_static_failure_cannot_be_overridden_by_llm() {
	local repo="${TEMP_DIR}/static-failure-repo"

	mkdir -p "${repo}/src"
	mark_opted_in "${repo}"
	printf 'export const apiKey = "abcdefghijklmnopqrstuvwxyz";\n' > "${repo}/src/leak.ts"

	run_expect_code 1 \
		"${CLI}" validate \
		--repo "${repo}" \
		--scope full-repo \
		--out "${TEMP_DIR}/static-failure" \
		--report "${REPORTS_DIR}/pass.json"

	grep -F -- 'ESTD-STATIC-SECRET' "${TEMP_DIR}/static-failure/report.json" >/dev/null \
		|| fail "Expected static secret finding in merged report"
}

test_standard_type_modules() {
	PYTHONPATH="${ENFORCER_ROOT}/lib" python3 - <<'PY'
from estd_enforcer.standard_types import cloud, database, docs, java, jenkins, php, scripts, unity, web

cases = [
	(unity.match_routes, "Assets/Scripts/BingoController.cs", "route.unity-client"),
	(php.match_routes, "src/BingoHandler.php", "route.php-monolith"),
	(java.match_routes, "src/main/java/com/bingo/rewards/RewardService.java", "route.java-seam-api"),
	(java.match_routes, "src/main/java/com/bingo/smartfox/BingoRoomExtension.java", "route.smartfox-server"),
	(web.match_routes, "apps/support-tool/src/app/player/page.tsx", "route.web-tools"),
	(web.match_routes, "apps/product-website/src/app/page.tsx", "route.product-website"),
	(database.match_routes, "migrations/001_create_rewards.sql", "route.database"),
	(cloud.match_routes, "infra/main.tf", "route.cloud-aws"),
	(jenkins.match_routes, "Jenkinsfile", "route.jenkins-cicd"),
	(scripts.match_routes, "scripts/sync-content.sh", "route.internal-scripts"),
	(docs.match_routes, "docs/adr/reward-flow.md", "route.technical-docs"),
]

for matcher, path, route in cases:
	if route not in matcher(path):
		raise SystemExit(f"{matcher.__module__} did not match {route} for {path}")
PY
}

test_expired_exception_fails_gate() {
	local repo="${TEMP_DIR}/exception-repo"

	mkdir -p "${repo}/src" "${repo}/.estd"
	mark_opted_in "${repo}"
	printf 'export const value = 1;\n' > "${repo}/src/example.ts"
	cat > "${repo}/.estd/config.yaml" <<'YAML'
version: 2
standardsPath: standards/bingo-bash-standards
profile: auto
mode: blocking
scope: full-repo
minScore: 75
failOnCritical: true
validationStrategy: static-first
llmPolicy: gaps-only
requiredStaticTools: []
exceptionsFile: .estd/exceptions.yaml
YAML
	cat > "${repo}/.estd/exceptions.yaml" <<'YAML'
- id: ESTD-EXPIRED
  estdId: ESTD1
  section: "30"
  reason: Expired fixture.
  approver: Director of Engineering
  expiresOn: 2020-01-01
  remediationPlan: Fix the issue.
  ticket: JIRA-1
  securityCritical: false
YAML

	run_expect_code 1 \
		"${CLI}" validate \
		--repo "${repo}" \
		--config "${repo}/.estd/config.yaml" \
		--out "${TEMP_DIR}/expired-exception" \
		--report "${REPORTS_DIR}/pass.json"
}

test_route_selection() {
	assert_request_has_route "unity-client" "route.unity-client"
	assert_request_has_route "php-monolith" "route.php-monolith"
	assert_request_has_route "java-seam-api" "route.java-seam-api"
	assert_request_has_route "smartfox-server" "route.smartfox-server"
	assert_request_has_route "product-website" "route.product-website"
	assert_request_has_route "web-tools" "route.web-tools"
	assert_request_has_route "database" "route.database"
	assert_request_has_route "cloud-aws" "route.cloud-aws"
	assert_request_has_route "jenkins-cicd" "route.jenkins-cicd"
	assert_request_has_route "internal-scripts" "route.internal-scripts"
	assert_request_has_route "technical-docs" "route.technical-docs"
}

main() {
	trap cleanup EXIT
	test_gate_semantics
	test_non_opted_repo_is_out_of_scope
	test_static_only_pass_skips_llm
	test_optional_static_tool_gap_invokes_llm
	test_required_static_tool_missing_is_tool_error
	test_static_failure_cannot_be_overridden_by_llm
	test_standard_type_modules
	test_expired_exception_fails_gate
	test_route_selection
	echo "ESTD enforcer tests passed."
}

main "$@"
