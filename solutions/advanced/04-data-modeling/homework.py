import json
from collections import defaultdict
from datetime import datetime, timezone


def _attributes(change: dict) -> dict:
    return {key: value for key, value in change.items() if key not in {"entity_id", "effective_at", "recorded_at"}}


def _time_key(value: str) -> tuple[int, str]:
    if not isinstance(value, str):
        raise ValueError("timestamps must be strings")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return 0, parsed.isoformat()
    return 1, parsed.astimezone(timezone.utc).isoformat()


def _normalized_time(value: str) -> str:
    return _time_key(value)[1]


def build_bitemporal(changes: list[dict]) -> list[dict]:
    grouped = defaultdict(list)
    identities = {}
    awareness = {
        _time_key(change[field])[0]
        for change in changes
        for field in ("effective_at", "recorded_at")
    }
    if len(awareness) > 1:
        raise ValueError("do not mix timezone-aware and timezone-naive timestamps")
    for change in changes:
        normalized = dict(change)
        normalized["effective_at"] = _normalized_time(change["effective_at"])
        normalized["recorded_at"] = _normalized_time(change["recorded_at"])
        identity = (normalized["entity_id"], _time_key(normalized["effective_at"]), _time_key(normalized["recorded_at"]))
        attributes = json.dumps(_attributes(normalized), sort_keys=True, separators=(",", ":"))
        if identity in identities and identities[identity] != attributes:
            raise ValueError(f"conflicting bitemporal changes at {identity}")
        if identity in identities:
            continue
        identities[identity] = attributes
        grouped[normalized["entity_id"]].append(normalized)

    rows = []
    for entity_id in sorted(grouped):
        entity_changes = grouped[entity_id]
        system_times = sorted({change["recorded_at"] for change in entity_changes}, key=_time_key)
        for system_index, system_from in enumerate(system_times):
            system_to = system_times[system_index + 1] if system_index + 1 < len(system_times) else None
            known = [change for change in entity_changes if _time_key(change["recorded_at"]) <= _time_key(system_from)]

            latest_by_effective = {}
            for change in sorted(known, key=lambda item: (_time_key(item["effective_at"]), _time_key(item["recorded_at"]), json.dumps(item, sort_keys=True))):
                latest_by_effective[_time_key(change["effective_at"])] = change
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
    valid_key = _time_key(valid_at)
    known_key = _time_key(known_at)
    if valid_key[0] != known_key[0]:
        raise ValueError("valid_at and known_at must use the same timezone convention")
    row_styles = {
        _time_key(row[field])[0]
        for row in rows
        if row["entity_id"] == entity_id
        for field in ("valid_from", "system_from")
    }
    if row_styles and row_styles != {valid_key[0]}:
        raise ValueError("query timestamps must match the history timezone convention")
    matches = [
        row for row in rows
        if row["entity_id"] == entity_id
        and _time_key(row["valid_from"]) <= valid_key
        and (row["valid_to"] is None or valid_key < _time_key(row["valid_to"]))
        and _time_key(row["system_from"]) <= known_key
        and (row["system_to"] is None or known_key < _time_key(row["system_to"]))
    ]
    if len(matches) > 1:
        raise ValueError("overlapping bitemporal intervals")
    return dict(matches[0]) if matches else None
