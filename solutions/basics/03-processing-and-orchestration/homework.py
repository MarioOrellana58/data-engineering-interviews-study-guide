from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
import math


def _normalize(event: dict) -> dict:
    result = deepcopy(event)
    result["currency"] = result["currency"].upper()
    return result


def _error(event: dict) -> str | None:
    if not event.get("event_id") or not event.get("updated_at"):
        return "missing event_id or updated_at"
    if type(event.get("amount")) not in (int, float) or not math.isfinite(event["amount"]) or event["amount"] < 0:
        return "amount must be a nonnegative number"
    if not isinstance(event.get("currency"), str) or len(event["currency"]) != 3:
        return "currency must be a three-letter code"
    return None


def _timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("updated_at must include a timezone")
    return parsed


def process_events(existing: list[dict], incoming: list[dict]) -> dict:
    candidates: dict[str, list[dict]] = {}
    rejected = []

    for event in [*existing, *incoming]:
        reason = _error(event)
        if reason:
            bad = deepcopy(event)
            bad["reason"] = reason
            rejected.append(bad)
            continue
        normalized = _normalize(event)
        try:
            _timestamp(normalized["updated_at"])
        except (TypeError, ValueError):
            normalized["reason"] = "updated_at must be an ISO-8601 timestamp with timezone"
            rejected.append(normalized)
            continue
        candidates.setdefault(normalized["event_id"], []).append(normalized)

    published = {}
    for event_id, versions in candidates.items():
        newest_at = max(_timestamp(row["updated_at"]) for row in versions)
        newest = [row for row in versions if _timestamp(row["updated_at"]) == newest_at]
        distinct = {json.dumps(row, sort_keys=True, separators=(",", ":")) for row in newest}
        if len(distinct) > 1:
            raise ValueError(f"conflicting versions for {event_id} share the newest updated_at")
        published[event_id] = newest[0]

    return {
        "published": [published[key] for key in sorted(published)],
        "rejected": sorted(rejected, key=lambda row: str(row.get("event_id", ""))),
    }
