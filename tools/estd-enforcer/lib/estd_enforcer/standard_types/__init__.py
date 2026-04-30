"""Standard-type route classification modules."""

from __future__ import annotations

from . import cloud, database, docs, java, jenkins, php, scripts, unity, web

ROUTE_MATCHERS = [
    jenkins.match_routes,
    unity.match_routes,
    php.match_routes,
    java.match_routes,
    database.match_routes,
    cloud.match_routes,
    web.match_routes,
    scripts.match_routes,
    docs.match_routes,
]


def classify_path(path: str) -> set[str]:
    routes: set[str] = set()
    for matcher in ROUTE_MATCHERS:
        routes.update(matcher(path))
    return routes
