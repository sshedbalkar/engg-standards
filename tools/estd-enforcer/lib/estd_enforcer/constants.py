"""Constants and repository paths for the ESTD enforcer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

EXIT_PASS = 0
EXIT_GATE_FAILED = 1
EXIT_TOOL_ERROR = 2

SCHEMA_VERSION = 2
DEFAULT_CONFIG: dict[str, Any] = {
    "version": 2,
    "standardsPath": "standards/bingo-bash-standards",
    "profile": "auto",
    "mode": "blocking",
    "scope": "changed-files",
    "minScore": 75,
    "failOnCritical": True,
    "validationStrategy": "static-first",
    "llmPolicy": "gaps-only",
    "requiredStaticTools": [],
    "exceptionsFile": ".estd/exceptions.yaml",
}

ENFORCER_ROOT = Path(__file__).resolve().parents[2]
STANDARDS_ROOT = Path(__file__).resolve().parents[4]
CONTEXT_ROOT = STANDARDS_ROOT / "context"
DOCS_ROOT = STANDARDS_ROOT / "docs"
ROUTE_MAP = CONTEXT_ROOT / "estd-routing-map.md"
VALIDATORS_ROOT = CONTEXT_ROOT / "validators"
REPORT_SCHEMA = ENFORCER_ROOT / "schema" / "report.schema.json"
STATIC_REGISTRY_PATH = ENFORCER_ROOT / "static-checks" / "registry.json"

ROUTE_ORDER = [
    "route.unity-client",
    "route.php-monolith",
    "route.java-seam-api",
    "route.smartfox-server",
    "route.database",
    "route.cloud-aws",
    "route.jenkins-cicd",
    "route.web-tools",
    "route.product-website",
    "route.internal-scripts",
    "route.technical-docs",
    "route.common",
]

PROFILE_TO_ROUTE = {
    "unity-client": "route.unity-client",
    "php-monolith": "route.php-monolith",
    "java-seam-api": "route.java-seam-api",
    "smartfox-server": "route.smartfox-server",
    "database": "route.database",
    "cloud-aws": "route.cloud-aws",
    "jenkins-cicd": "route.jenkins-cicd",
    "web-tools": "route.web-tools",
    "product-website": "route.product-website",
    "internal-scripts": "route.internal-scripts",
    "technical-docs": "route.technical-docs",
    "common": "route.common",
}
