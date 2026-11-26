from __future__ import annotations

from copy import deepcopy
from datetime import datetime


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_batch(rows: list[dict], contract: dict, now: datetime) -> dict:
    accepted = []
    rejected = []
    seen = set()
    timestamps = []

    for source in rows:
        row = deepcopy(source)
        missing = [field for field in contract["required"] if row.get(field) is None]
        if missing:
            row["reason"] = "missing required fields: " + ", ".join(missing)
            rejected.append(row)
            continue
        key = row[contract["unique"]]
        if key in seen:
            row["reason"] = f"duplicate {contract['unique']}"
            rejected.append(row)
            continue
        try:
            timestamp = _parse_timestamp(row["event_at"])
        except (TypeError, ValueError):
            row["reason"] = "invalid event_at"
            rejected.append(row)
            continue
        seen.add(key)
        timestamps.append(timestamp)
        accepted.append(row)

    freshness = (now - max(timestamps)).total_seconds() / 60 if timestamps else float("inf")
    reject_rate = len(rejected) / len(rows) if rows else 0.0
    publish = bool(rows) and reject_rate <= contract["max_reject_rate"] and freshness <= contract["max_age_minutes"]
    return {
        "accepted": accepted,
        "rejected": rejected,
        "publish": publish,
        "metrics": {
            "input_count": len(rows),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
            "reject_rate": reject_rate,
            "freshness_minutes": freshness,
        },
    }
