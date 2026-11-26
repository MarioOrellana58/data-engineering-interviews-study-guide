from collections.abc import Callable
from copy import deepcopy


def ingest_pages(
    fetch_page: Callable[[str | None], dict],
    start_token: str | None,
    seen_versions: set[tuple[str, int]],
    max_pages: int,
) -> dict:
    if max_pages < 1:
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
        source = page.get("source")
        for original in page.get("items", []):
            item = deepcopy(original)
            if (
                not all(field in item for field in ("id", "version", "body"))
                or not isinstance(item.get("version"), int)
            ):
                item["reason"] = "missing id, version, or body"
                quarantined.append(item)
                continue
            key = (item["id"], item["version"])
            if key in seen:
                continue
            seen.add(key)
            item["source"] = source
            accepted.append(item)
        token = page.get("next_token")
        if token is None:
            break

    return {"accepted": accepted, "quarantined": quarantined, "next_token": token}
