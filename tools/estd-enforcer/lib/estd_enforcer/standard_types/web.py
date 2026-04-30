"""Web tools and product website route classification."""

from __future__ import annotations

from pathlib import Path


def match_routes(path: str) -> set[str]:
    lowered = path.lower()
    name = Path(lowered).name
    suffix = Path(lowered).suffix
    config_files = {"package.json", "next.config.js", "next.config.ts", "tailwind.config.js", "tailwind.config.ts"}
    website_tokens = ("product-website", "public-website", "website", "webgl", "announcement", "community")
    if suffix in {".ts", ".tsx", ".js", ".jsx"} or name in config_files:
        if any(token in lowered for token in website_tokens):
            return {"route.product-website"}
        return {"route.web-tools"}
    return set()
