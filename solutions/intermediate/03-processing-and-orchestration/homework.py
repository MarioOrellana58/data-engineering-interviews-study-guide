from copy import deepcopy
import hashlib
import json


def _fingerprint(event: dict) -> str:
    canonical = json.dumps(event, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


def _validation_error(event: dict) -> str | None:
    if not isinstance(event, dict):
        return "event must be a mapping"
    if not isinstance(event.get("event_id"), str) or not event["event_id"]:
        return "event_id must be a nonempty string"
    if not isinstance(event.get("id"), str) or not event["id"]:
        return "id must be a nonempty string"
    if type(event.get("source_lsn")) is not int or event["source_lsn"] < 0:
        return "source_lsn must be a nonnegative integer"
    if event.get("op") not in {"upsert", "delete"}:
        return "unsupported operation"
    return None


def apply_cdc(snapshot: dict[str, dict], events: list[dict], checkpoint: int) -> dict:
    if type(checkpoint) is not int or checkpoint < -1:
        raise ValueError("checkpoint must be an integer at or above -1")
    if snapshot.get("__state_version__") == 1:
        state = deepcopy(snapshot.get("records", {}))
        tombstones = deepcopy(snapshot.get("tombstones", {}))
        processed_events = deepcopy(snapshot.get("processed_events", {}))
        checkpoint = max(checkpoint, int(snapshot.get("checkpoint", checkpoint)))
    else:
        state = deepcopy(snapshot)
        tombstones = {}
        processed_events = {}
    if not all(isinstance(section, dict) for section in (state, tombstones, processed_events)):
        raise ValueError("state sections must be mappings")

    quarantined = []
    next_checkpoint = checkpoint
    ordered = sorted(
        (deepcopy(event) for event in events),
        key=lambda event: (
            event.get("source_lsn") if isinstance(event, dict) and type(event.get("source_lsn")) is int else -1,
            str(event.get("event_id", "")) if isinstance(event, dict) else "",
        ),
    )
    for event in ordered:
        reason = _validation_error(event)
        if reason:
            bad = event if isinstance(event, dict) else {"value": event}
            quarantined.append({**bad, "reason": reason})
            continue

        lsn, entity_id, event_id = event["source_lsn"], event["id"], event["event_id"]
        fingerprint = _fingerprint(event)
        previous = processed_events.get(event_id)
        if previous is not None:
            if previous.get("fingerprint") != fingerprint:
                quarantined.append({**event, "reason": "event_id reused with different payload"})
            next_checkpoint = max(next_checkpoint, lsn)
            continue

        if lsn <= checkpoint:
            current = state.get(entity_id)
            tombstone = tombstones.get(entity_id)
            payload = {key: value for key, value in event.items() if key not in {"event_id", "op", "source_lsn"}}
            exact_upsert = (
                event["op"] == "upsert"
                and current is not None
                and current.get("_lsn") == lsn
                and current.get("_event_id", event_id) == event_id
                and all(current.get(key) == value for key, value in payload.items())
            )
            exact_delete = (
                event["op"] == "delete"
                and tombstone is not None
                and tombstone.get("_lsn") == lsn
                and tombstone.get("_event_id") == event_id
            )
            if exact_upsert or exact_delete:
                processed_events[event_id] = {"source_lsn": lsn, "fingerprint": fingerprint}
            else:
                quarantined.append({**event, "reason": "event conflicts with an already committed checkpoint"})
            continue

        if event["op"] == "delete":
            current_lsn = max(state.get(entity_id, {}).get("_lsn", -1), tombstones.get(entity_id, {}).get("_lsn", -1))
            if lsn <= current_lsn:
                quarantined.append({**event, "reason": "event is not newer than entity state"})
            else:
                state.pop(entity_id, None)
                tombstones[entity_id] = {"_lsn": lsn, "_event_id": event_id}
        else:
            current_lsn = max(state.get(entity_id, {}).get("_lsn", -1), tombstones.get(entity_id, {}).get("_lsn", -1))
            if lsn <= current_lsn:
                quarantined.append({**event, "reason": "event is not newer than entity state"})
            else:
                state[entity_id] = {key: value for key, value in event.items() if key not in {"event_id", "op", "source_lsn"}}
                state[entity_id]["_lsn"] = lsn
                state[entity_id]["_event_id"] = event_id
                tombstones.pop(entity_id, None)
        processed_events[event_id] = {"source_lsn": lsn, "fingerprint": fingerprint}
        next_checkpoint = max(next_checkpoint, lsn)

    durable_state = {
        "__state_version__": 1,
        "records": state,
        "tombstones": tombstones,
        "processed_events": processed_events,
        "checkpoint": next_checkpoint,
    }
    quarantined.sort(key=lambda row: (row.get("source_lsn", -1), str(row.get("event_id", ""))))
    return {"snapshot": state, "tombstones": tombstones, "state": durable_state,
            "checkpoint": next_checkpoint, "quarantined": quarantined}
