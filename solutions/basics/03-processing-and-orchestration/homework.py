from __future__ import annotations

from copy import deepcopy


def _normalize(event: dict) -> dict:
    result = deepcopy(event)
    result["currency"] = result["currency"].upper()
    return result


def _error(event: dict) -> str | None:
    if not event.get("event_id") or not event.get("updated_at"):
        return "missing event_id or updated_at"
    if not isinstance(event.get("amount"), (int, float)) or event["amount"] < 0:
        return "amount must be a nonnegative number"
    if not isinstance(event.get("currency"), str) or len(event["currency"]) != 3:
        return "currency must be a three-letter code"
    return None


def process_events(existing: list[dict], incoming: list[dict]) -> dict:
    published: dict[str, dict] = {}
    rejected = []

    for event in [*existing, *incoming]:
        reason = _error(event)
        if reason:
            bad = deepcopy(event)
            bad["reason"] = reason
            rejected.append(bad)
            continue
        normalized = _normalize(event)
        current = published.get(normalized["event_id"])
        if current is None or normalized["updated_at"] > current["updated_at"]:
            published[normalized["event_id"]] = normalized

    return {
        "published": [published[key] for key in sorted(published)],
        "rejected": sorted(rejected, key=lambda row: str(row.get("event_id", ""))),
    }
