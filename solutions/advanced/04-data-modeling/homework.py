import json
from collections import defaultdict


def _attributes(change: dict) -> dict:
    return {key: value for key, value in change.items() if key not in {"entity_id", "effective_at", "recorded_at"}}


def build_bitemporal(changes: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    for change in changes:
        grouped[change["entity_id"]].append(dict(change))

    rows = []
    for entity_id in sorted(grouped):
        entity_changes = grouped[entity_id]
        system_times = sorted({change["recorded_at"] for change in entity_changes})
        for system_index, system_from in enumerate(system_times):
            system_to = system_times[system_index + 1] if system_index + 1 < len(system_times) else None
            known = [change for change in entity_changes if change["recorded_at"] <= system_from]

            latest_by_effective = {}
            for change in sorted(known, key=lambda item: (item["effective_at"], item["recorded_at"], json.dumps(item, sort_keys=True))):
                latest_by_effective[change["effective_at"]] = change
            timeline = [latest_by_effective[key] for key in sorted(latest_by_effective)]

            for valid_index, change in enumerate(timeline):
                valid_to = timeline[valid_index + 1]["effective_at"] if valid_index + 1 < len(timeline) else None
                rows.append(
                    {
                        "entity_id": entity_id,
                        **_attributes(change),
                        "valid_from": change["effective_at"],
                        "valid_to": valid_to,
                        "system_from": system_from,
                        "system_to": system_to,
                    }
                )
    return rows


def as_of(rows: list[dict], entity_id: str, valid_at: str, known_at: str) -> dict | None:
    matches = [
        row for row in rows
        if row["entity_id"] == entity_id
        and row["valid_from"] <= valid_at
        and (row["valid_to"] is None or valid_at < row["valid_to"])
        and row["system_from"] <= known_at
        and (row["system_to"] is None or known_at < row["system_to"])
    ]
    if len(matches) > 1:
        raise ValueError("overlapping bitemporal intervals")
    return dict(matches[0]) if matches else None
