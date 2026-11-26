import hashlib
import hmac
import json
import math
import re
from copy import deepcopy


STATE_VERSION = 1


def _key_material(secret: str) -> tuple[str, str]:
    match = re.match(r"^(v[0-9]+):(.*)$", secret, flags=re.DOTALL)
    if match:
        version, material = match.groups()
        if not material:
            raise ValueError("versioned pii_secret must include key material")
        return version, material
    return "v1", secret


def _email_token(email: str, secret: str) -> str:
    _, material = _key_material(secret)
    normalized = email.strip().lower().encode()
    return hmac.new(material.encode(), normalized, hashlib.sha256).hexdigest()


def _fingerprint(event: dict) -> str:
    payload = json.dumps(event, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


def _invalid(event: dict) -> str | None:
    required = {"event_id", "id", "op", "source_version"}
    if not required.issubset(event):
        return "missing required fields"
    if not isinstance(event["event_id"], str) or not event["event_id"].strip():
        return "event_id must be a nonempty string"
    if not isinstance(event["id"], str) or not event["id"].strip():
        return "id must be a nonempty string"
    if event["op"] not in {"upsert", "delete"}:
        return "unsupported operation"
    if type(event["source_version"]) is not int or event["source_version"] < 0:
        return "source_version must be a nonnegative integer"
    if event["op"] == "upsert":
        if not isinstance(event.get("email"), str) or "@" not in event["email"]:
            return "invalid email"
        if type(event.get("amount")) not in (int, float) or not math.isfinite(event["amount"]):
            return "amount must be finite"
    return None


def _clean_existing_row(entity_id: str, row: dict, pii_secret: str) -> dict:
    version = row.get("source_version")
    if type(version) is not int or version < 0:
        raise ValueError(f"existing row {entity_id!r} has an invalid source_version")
    token = row.get("email_token")
    token_version = str(row.get("email_token_version", "v1"))
    if "email" in row:
        email = row["email"]
        if not isinstance(email, str) or "@" not in email:
            raise ValueError(f"existing row {entity_id!r} has an invalid email")
        token = _email_token(email, pii_secret)
        token_version = _key_material(pii_secret)[0]
    if not isinstance(token, str) or not token:
        raise ValueError(f"existing row {entity_id!r} requires email_token or email")
    amount = row.get("amount")
    if type(amount) not in (int, float) or not math.isfinite(amount):
        raise ValueError(f"existing row {entity_id!r} has an invalid amount")
    return {"id": entity_id, "source_version": version, "email_token": token,
            "email_token_version": token_version, "amount": amount}


def _load_state(existing: dict, pii_secret: str) -> tuple[dict, dict, dict, dict]:
    if existing.get("__state_version__") == STATE_VERSION:
        records_source = existing.get("records", {})
        watermarks = deepcopy(existing.get("watermarks", {}))
        tombstones = deepcopy(existing.get("tombstones", {}))
        processed_events = deepcopy(existing.get("processed_events", {}))
    else:
        records_source, watermarks, tombstones, processed_events = existing, {}, {}, {}
    if not all(isinstance(value, dict) for value in (records_source, watermarks, tombstones, processed_events)):
        raise ValueError("existing state sections must be mappings")
    records = {entity_id: _clean_existing_row(entity_id, row, pii_secret)
               for entity_id, row in records_source.items()}
    for entity_id, row in records.items():
        watermarks[entity_id] = max(watermarks.get(entity_id, -1), row["source_version"])
    for entity_id, tombstone in tombstones.items():
        version = tombstone.get("source_version")
        if type(version) is not int or version < 0:
            raise ValueError(f"tombstone {entity_id!r} has an invalid source_version")
        watermarks[entity_id] = max(watermarks.get(entity_id, -1), version)
    return records, watermarks, tombstones, processed_events


def process_batch(existing: dict[str, dict], events: list[dict], pii_secret: str) -> dict:
    if not pii_secret:
        raise ValueError("pii_secret must not be empty")
    if not isinstance(existing, dict) or not isinstance(events, list):
        raise TypeError("existing must be a mapping and events must be a list")
    token_version, _ = _key_material(pii_secret)
    records, watermarks, tombstones, processed_events = _load_state(deepcopy(existing), pii_secret)
    quarantined = []
    stale_count = deletion_count = upsert_count = 0
    ordered = sorted((deepcopy(event) for event in events), key=lambda row: (
        str(row.get("id", "")),
        row.get("source_version") if type(row.get("source_version")) is int else -1,
        str(row.get("event_id", "")),
    ))
    for event in ordered:
        reason = _invalid(event)
        if reason:
            quarantined.append({**event, "reason": reason})
            continue
        event_id = event["event_id"]
        fingerprint = _fingerprint(event)
        previous_fingerprint = processed_events.get(event_id)
        if previous_fingerprint is not None:
            if previous_fingerprint == fingerprint:
                stale_count += 1
            else:
                quarantined.append({**event, "reason": "event_id reused with different payload"})
            continue
        entity_id, version = event["id"], event["source_version"]
        current_version = watermarks.get(entity_id, -1)
        if version < current_version:
            stale_count += 1
            processed_events[event_id] = fingerprint
            continue
        if version == current_version:
            quarantined.append({**event, "reason": "source_version conflicts with existing state"})
            processed_events[event_id] = fingerprint
            continue
        processed_events[event_id] = fingerprint
        watermarks[entity_id] = version
        if event["op"] == "delete":
            records.pop(entity_id, None)
            tombstones[entity_id] = {"source_version": version, "event_id": event_id}
            deletion_count += 1
        else:
            records[entity_id] = {"id": entity_id, "source_version": version,
                                  "email_token": _email_token(event["email"], pii_secret),
                                  "email_token_version": token_version, "amount": event["amount"]}
            tombstones.pop(entity_id, None)
            upsert_count += 1
    published = {key: records[key] for key in sorted(records)}
    state = {"__state_version__": STATE_VERSION, "records": published,
             "watermarks": {key: watermarks[key] for key in sorted(watermarks)},
             "tombstones": {key: tombstones[key] for key in sorted(tombstones)},
             "processed_events": {key: processed_events[key] for key in sorted(processed_events)}}
    quarantined.sort(key=lambda row: (str(row.get("event_id", "")), str(row.get("reason", ""))))
    return {"published": published, "state": state, "tombstones": state["tombstones"],
            "quarantined": quarantined,
            "metrics": {"input_count": len(events), "published_count": len(published),
                        "upsert_count": upsert_count, "deletion_count": deletion_count,
                        "stale_count": stale_count, "quarantined_count": len(quarantined)}}
