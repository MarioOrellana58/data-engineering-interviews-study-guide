import hashlib
import json


def _canonical_hash(events: list[dict]) -> str:
    payload = json.dumps(events, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


def recover_and_plan(events: list[dict], committed_batches: list[dict], checkpoint: int, capacity: int) -> dict:
    if type(capacity) is not int or capacity < 1:
        raise ValueError("capacity must be positive")
    if type(checkpoint) is not int or checkpoint < -1:
        raise ValueError("checkpoint must be an integer at or above -1")

    by_offset = {}
    offsets_by_event_id = {}
    canonical_by_identity = {}
    for event in events:
        offset = event.get("offset")
        event_id = event.get("event_id")
        if type(offset) is not int or offset < 0 or not isinstance(event_id, str) or not event_id:
            raise ValueError("events require a nonnegative integer offset and event_id")
        canonical = json.dumps(event, sort_keys=True, separators=(",", ":"), default=str)
        identity = (offset, event_id)
        if identity in canonical_by_identity:
            if canonical_by_identity[identity] != canonical:
                raise ValueError(f"conflicting payload for event identity {identity}")
            continue
        canonical_by_identity[identity] = canonical
        if event_id in offsets_by_event_id and offsets_by_event_id[event_id] != offset:
            raise ValueError(f"event_id {event_id} appears at multiple offsets")
        offsets_by_event_id[event_id] = offset
        previous = by_offset.get(offset)
        if previous is not None and previous["event_id"] != event_id:
            raise ValueError(f"offset {offset} belongs to distinct events")
        by_offset[offset] = dict(event)

    committed_ids = {event_id for batch in committed_batches for event_id in batch.get("output_ids", [])}
    committed_end_offsets = [batch.get("end_offset", checkpoint) for batch in committed_batches]
    if any(type(offset) is not int or offset < -1 for offset in committed_end_offsets):
        raise ValueError("committed end offsets must be integers at or above -1")
    effective_checkpoint = max([checkpoint, *committed_end_offsets])
    eligible = [
        event for offset, event in sorted(by_offset.items())
        if offset > effective_checkpoint and event["event_id"] not in committed_ids
    ]

    batches = []
    for index in range(0, len(eligible), capacity):
        group = eligible[index : index + capacity]
        input_hash = _canonical_hash(group)
        start_offset, end_offset = group[0]["offset"], group[-1]["offset"]
        batch_seed = f"{start_offset}:{end_offset}:{input_hash}"
        batches.append(
            {
                "batch_id": hashlib.sha256(batch_seed.encode()).hexdigest()[:20],
                "start_offset": start_offset,
                "end_offset": end_offset,
                "input_hash": input_hash,
                "output_ids": [event["event_id"] for event in group],
                "commit": "atomically publish outputs and end_offset",
            }
        )
    return {"checkpoint": effective_checkpoint, "batches": batches}
