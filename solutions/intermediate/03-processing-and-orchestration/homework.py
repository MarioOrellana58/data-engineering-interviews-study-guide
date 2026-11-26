from copy import deepcopy


def apply_cdc(snapshot: dict[str, dict], events: list[dict], checkpoint: int) -> dict:
    state = deepcopy(snapshot)
    quarantined = []
    next_checkpoint = checkpoint

    ordered = sorted((deepcopy(event) for event in events), key=lambda event: (event["source_lsn"], event["event_id"]))
    for event in ordered:
        lsn = event["source_lsn"]
        entity_id = event["id"]
        if lsn <= checkpoint:
            current = state.get(entity_id)
            payload = {key: value for key, value in event.items() if key not in {"event_id", "op", "source_lsn"}}
            exact_replay = event["op"] == "upsert" and current is not None and current.get("_lsn") == lsn and all(current.get(key) == value for key, value in payload.items())
            if not exact_replay:
                event["reason"] = "event conflicts with an already committed checkpoint"
                quarantined.append(event)
            continue

        if event["op"] == "delete":
            state.pop(entity_id, None)
        elif event["op"] == "upsert":
            state[entity_id] = {
                key: value for key, value in event.items() if key not in {"event_id", "op", "source_lsn"}
            }
            state[entity_id]["_lsn"] = lsn
        else:
            event["reason"] = "unsupported operation"
            quarantined.append(event)
            continue
        next_checkpoint = max(next_checkpoint, lsn)

    return {"snapshot": state, "checkpoint": next_checkpoint, "quarantined": quarantined}
