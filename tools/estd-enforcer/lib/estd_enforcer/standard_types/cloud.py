"""Cloud and AWS route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    cloud_tokens = ("terraform", "cloudformation", "aws", "iam", "vpc", "rds", "s3", "waf", "secretsmanager")
    if Path(lowered).suffix == ".tf" or any(token in lowered for token in cloud_tokens):
        return {"route.cloud-aws"}
    return set()
