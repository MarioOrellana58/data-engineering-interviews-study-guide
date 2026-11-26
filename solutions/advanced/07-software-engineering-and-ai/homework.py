import hashlib
import json
from datetime import datetime, timedelta


def _timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def materialize_features(labels: list[dict], events: list[dict], definition_version: str) -> list[dict]:
    result = []
    for label in sorted(labels, key=lambda row: (row["entity_id"], row["label_at"])):
        label_at = _timestamp(label["label_at"])
        window_start = label_at - timedelta(days=7)
        eligible = [
            event for event in events
            if event["entity_id"] == label["entity_id"]
            and window_start <= _timestamp(event["event_at"]) < label_at
            and _timestamp(event["ingested_at"]) < label_at
        ]
        eligible.sort(key=lambda event: (event["event_at"], event["event_id"]))
        feature_values = {
            "txn_count_7d": len(eligible),
            "txn_amount_7d": sum(event["amount"] for event in eligible),
        }
        fingerprint = json.dumps(
            [label["entity_id"], label["label_at"], definition_version, feature_values],
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
