"""Confluence REST API v2 adapter."""

from __future__ import annotations

import re

from .metadata import build_page_property_payload
from .models import (
    ConfluenceDeployError,
    JsonObject,
    MAX_API_ERROR_CHARS,
    MAX_PAGINATION_PAGES,
)


def format_adapter_error_text(raw_text: str) -> str:
    normalized = re.sub(r"[\r\n\t]+", " ", raw_text).strip()
    redacted = re.sub(
        r"(?i)\b(authorization|cookie|set-cookie|token|api[-_ ]?token|"
        r"password|secret)\b([\"']?\s*[:=]\s*[\"']?)[^\"'\s,;]+",
        r"\1\2[REDACTED]",
        normalized,
    )
    if not redacted:
        return "(empty response)"
    if len(redacted) <= MAX_API_ERROR_CHARS:
        return redacted
    return f"{redacted[:MAX_API_ERROR_CHARS]}...[truncated]"


class ConfluenceClient:
    """Small Confluence REST API v2 adapter."""

    def __init__(self, cloud: str, user: str, token: str) -> None:
        try:
            import requests
        except ImportError as exc:
            raise ConfluenceDeployError(
                "Missing dependency: requests. Install workflow dependencies first."
            ) from exc

        self._requests = requests
        self.site_url = f"https://{cloud}.atlassian.net"
        self.api_url = f"{self.site_url}/wiki/api/v2"
        self.auth = (user, token)

    def get_page(self, page_id: str, *, body_format: str | None = None) -> JsonObject:
        params = {"body-format": body_format} if body_format else None
        return self._request("GET", f"/pages/{page_id}", params=params, expected=(200,))

    def update_page(self, page_id: str, payload: JsonObject) -> JsonObject:
        return self._request("PUT", f"/pages/{page_id}", json=payload, expected=(200,))

    def list_page_inline_comments(self, page_id: str) -> list[JsonObject]:
        return self._get_paginated(
            f"/pages/{page_id}/inline-comments",
            params={
                "body-format": "storage",
                "status": "current",
                "resolution-status": "open",
                "limit": 250,
            },
        )

    def list_page_footer_comments(self, page_id: str) -> list[JsonObject]:
        return self._get_paginated(
            f"/pages/{page_id}/footer-comments",
            params={"body-format": "storage", "status": "current", "limit": 250},
        )

    def get_inline_comment_children(self, comment_id: str) -> list[JsonObject]:
        return self._get_paginated(
            f"/inline-comments/{comment_id}/children",
            params={"body-format": "storage", "limit": 250},
        )

    def create_footer_comment(self, page_id: str, storage_body: str) -> JsonObject:
        payload = {
            "pageId": str(page_id),
            "body": {"representation": "storage", "value": storage_body},
        }
        return self._request("POST", "/footer-comments", json=payload, expected=(201,))

    def get_page_property(self, page_id: str, key: str) -> JsonObject | None:
        data = self._request(
            "GET",
            f"/pages/{page_id}/properties",
            params={"key": key},
            expected=(200,),
        )
        for item in data.get("results", []):
            if item.get("key") == key:
                return item
        return None

    def get_page_property_by_id(
        self,
        page_id: str,
        property_id: str,
    ) -> JsonObject:
        return self._request(
            "GET",
            f"/pages/{page_id}/properties/{property_id}",
            expected=(200,),
        )

    def upsert_page_property(
        self,
        page_id: str,
        key: str,
        value: JsonObject,
    ) -> JsonObject:
        existing = self.get_page_property(page_id, key)
        payload = build_page_property_payload(key, value, existing)
        if existing:
            prop_id = existing["id"]
            return self._request(
                "PUT",
                f"/pages/{page_id}/properties/{prop_id}",
                json=payload,
                expected=(200,),
            )
        return self._request(
            "POST",
            f"/pages/{page_id}/properties",
            json=payload,
            expected=(200, 201),
        )

    def get_users_bulk(self, account_ids: list[str]) -> dict[str, str]:
        if not account_ids:
            return {}
        payload = {"accountIds": account_ids}
        data = self._request("POST", "/users-bulk", json=payload, expected=(200,))
        users: dict[str, str] = {}
        for user in data.get("results", []):
            account_id = str(user.get("accountId") or "")
            if not account_id:
                continue
            users[account_id] = (
                user.get("displayName")
                or user.get("publicName")
                or account_id
            )
        return users

    def set_page_width(self, page_id: str) -> None:
        for prop_key in ("content-appearance-draft", "content-appearance-published"):
            data = self._request(
                "GET",
                f"/pages/{page_id}/properties",
                params={"key": prop_key},
                expected=(200,),
            )
            existing = (data.get("results") or [None])[0]
            if existing:
                prop_id = existing["id"]
                version = existing.get("version", {}).get("number", 0) + 1
                payload = {
                    "key": prop_key,
                    "value": "full-width",
                    "version": {"number": version},
                }
                self._request(
                    "PUT",
                    f"/pages/{page_id}/properties/{prop_id}",
                    json=payload,
                    expected=(200,),
                )
            else:
                payload = {"key": prop_key, "value": "full-width"}
                self._request(
                    "POST",
                    f"/pages/{page_id}/properties",
                    json=payload,
                    expected=(200, 201),
                )

    def _get_paginated(
        self,
        path_or_url: str,
        *,
        params: JsonObject | None = None,
    ) -> list[JsonObject]:
        results: list[JsonObject] = []
        next_path: str | None = path_or_url
        next_params = params
        seen_paths: set[str] = set()
        page_count = 0

        while next_path:
            if next_path in seen_paths:
                raise ConfluenceDeployError(
                    f"Confluence pagination loop detected for {path_or_url}"
                )
            seen_paths.add(next_path)
            page_count += 1
            if page_count > MAX_PAGINATION_PAGES:
                raise ConfluenceDeployError(
                    f"Confluence pagination exceeded {MAX_PAGINATION_PAGES} pages "
                    f"for {path_or_url}"
                )
            data = self._request("GET", next_path, params=next_params, expected=(200,))
            page_results = data.get("results", [])
            if not isinstance(page_results, list):
                raise ConfluenceDeployError(
                    f"Confluence pagination returned invalid results for {path_or_url}"
                )
            results.extend(page_results)

            links = data.get("_links") or {}
            if not isinstance(links, dict):
                raise ConfluenceDeployError(
                    f"Confluence pagination returned invalid links for {path_or_url}"
                )
            next_candidate = links.get("next")
            if next_candidate is not None and not isinstance(next_candidate, str):
                raise ConfluenceDeployError(
                    f"Confluence pagination returned invalid next link for {path_or_url}"
                )
            next_path = next_candidate
            next_params = None

        return results

    def _request(
        self,
        method: str,
        path_or_url: str,
        *,
        params: JsonObject | None = None,
        json: JsonObject | None = None,
        expected: tuple[int, ...],
    ) -> JsonObject:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        url = self._to_url(path_or_url)
        response = self._requests.request(
            method,
            url,
            headers=headers,
            auth=self.auth,
            params=params,
            json=json,
            timeout=60,
        )
        if response.status_code not in expected:
            error_text = format_adapter_error_text(response.text)
            raise ConfluenceDeployError(
                f"Confluence {method} {path_or_url} failed: "
                f"{response.status_code} {error_text}"
            )
        if response.status_code == 204 or not response.text:
            return {}
        try:
            payload = response.json()
        except ValueError as exc:
            error_text = format_adapter_error_text(response.text)
            raise ConfluenceDeployError(
                f"Confluence {method} {path_or_url} returned invalid JSON: "
                f"{error_text}"
            ) from exc
        if not isinstance(payload, dict):
            raise ConfluenceDeployError(
                f"Confluence {method} {path_or_url} returned unsupported JSON"
            )
        return payload

    def _to_url(self, path_or_url: str) -> str:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url
        if path_or_url.startswith("/wiki/api/v2/"):
            return self.site_url + path_or_url
        if path_or_url.startswith("/"):
            return self.api_url + path_or_url
        return f"{self.api_url}/{path_or_url}"
