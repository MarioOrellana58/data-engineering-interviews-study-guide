import hashlib
import json


def _canonical_hash(events: list[dict]) -> str:
    payload = json.dumps(events, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


def recover_and_plan(events: list[dict], committed_batches: list[dict], checkpoint: int, capacity: int) -> dict:
    if capacity < 1:
        raise ValueError("capacity must be positive")

    by_offset = {}
    for event in events:
        offset = event["offset"]
        previous = by_offset.get(offset)
        if previous is not None and previous["event_id"] != event["event_id"]:
            raise ValueError(f"offset {offset} belongs to distinct events")
        by_offset[offset] = dict(event)

    committed_ids = {event_id for batch in committed_batches for event_id in batch.get("output_ids", [])}
    eligible = [
        event for offset, event in sorted(by_offset.items())
        if offset > checkpoint and event["event_id"] not in committed_ids
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
    return {"checkpoint": checkpoint, "batches": batches}
