import hashlib
import json
import math
from datetime import datetime, timedelta, timezone


def _timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("feature timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def materialize_features(labels: list[dict], events: list[dict], definition_version: str) -> list[dict]:
    events_by_id = {}
    event_canonical = {}
    for event in events:
        if not event.get("event_id"):
            raise ValueError("events require event_id")
        if type(event.get("amount")) not in (int, float) or not math.isfinite(event["amount"]):
            raise ValueError("event amount must be finite")
        canonical = json.dumps(event, sort_keys=True, separators=(",", ":"), default=str)
        if event["event_id"] in event_canonical and event_canonical[event["event_id"]] != canonical:
            raise ValueError(f"conflicting duplicate event_id {event['event_id']}")
        event_canonical[event["event_id"]] = canonical
        events_by_id[event["event_id"]] = event

    result = []
    for label in sorted(labels, key=lambda row: (row["entity_id"], row["label_at"])):
        label_at = _timestamp(label["label_at"])
        window_start = label_at - timedelta(days=7)
        eligible = [
            event for event in events_by_id.values()
            if event["entity_id"] == label["entity_id"]
            and window_start <= _timestamp(event["event_at"]) < label_at
            and _timestamp(event["ingested_at"]) < label_at
        ]
        eligible.sort(key=lambda event: (event["event_at"], event["event_id"]))
        feature_values = {
            "txn_count_7d": len(eligible),
            "txn_amount_7d": sum(event["amount"] for event in eligible),
        }
        canonical_inputs = [event_canonical[event["event_id"]] for event in eligible]
        fingerprint = json.dumps(
            [label, definition_version, feature_values, canonical_inputs],
            sort_keys=True,
            separators=(",", ":"),
        )
        result.append(
            {
                **label,
                **feature_values,
                "definition_version": definition_version,
                "feature_hash": hashlib.sha256(fingerprint.encode()).hexdigest(),
            }
        )
    return result
