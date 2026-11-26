from collections.abc import Callable
from copy import deepcopy
import hashlib
import json


def ingest_pages(
    fetch_page: Callable[[str | None], dict],
    start_token: str | None,
    seen_versions: set[tuple[str, int]],
    max_pages: int,
) -> dict:
    if type(max_pages) is not int or max_pages < 1:
        raise ValueError("max_pages must be positive")

    token = start_token
    visited = set()
    seen = set(seen_versions)
    accepted = []
    quarantined = []

    for _ in range(max_pages):
        if token in visited:
            raise ValueError("continuation token cycle detected")
        visited.add(token)
        page = fetch_page(token)
        if not isinstance(page, dict) or not isinstance(page.get("items", []), list):
            raise ValueError("fetch_page must return a dictionary with an items list")
        source = page.get("source")
        source_url = page.get("source_url") or "not-provided"
        retrieved_at = page.get("retrieved_at") or "not-provided"
        if not isinstance(source_url, str) or not isinstance(retrieved_at, str):
            raise ValueError("source_url and retrieved_at must be strings when provided")
        for original in page.get("items", []):
            item = deepcopy(original)
            if (
                not all(field in item for field in ("id", "version", "body"))
                or not isinstance(item.get("id"), str)
                or not item.get("id")
                or type(item.get("version")) is not int
            ):
                item["reason"] = "missing id, version, or body"
                quarantined.append(item)
                continue
            key = (item["id"], item["version"])
            if key in seen:
                continue
            seen.add(key)
            item["source"] = source
            item["source_url"] = source_url
            item["retrieved_at"] = retrieved_at
            canonical_body = json.dumps(item["body"], sort_keys=True, separators=(",", ":"), default=str)
            item["content_hash"] = hashlib.sha256(canonical_body.encode()).hexdigest()
            accepted.append(item)
        token = page.get("next_token")
        if token is not None and not isinstance(token, str):
            raise ValueError("next_token must be a string or None")
        if token is None:
            break

    return {"accepted": accepted, "quarantined": quarantined, "next_token": token}
