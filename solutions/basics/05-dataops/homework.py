from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import math


def _parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def validate_batch(rows: list[dict], contract: dict, now: datetime) -> dict:
    if now.tzinfo is None:
        raise ValueError("now must include a timezone")
    now = now.astimezone(timezone.utc)
    if contract["max_age_minutes"] < 0 or not 0 <= contract["max_reject_rate"] <= 1:
        raise ValueError("invalid quality thresholds")
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
        amount = row.get("amount")
        if type(amount) not in (int, float) or not math.isfinite(amount) or amount < 0:
            row["reason"] = "amount must be a finite nonnegative number"
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
        if timestamp > now:
            row["reason"] = "event_at is in the future"
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
