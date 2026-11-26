from copy import deepcopy

from test_support import load_homework

hw = load_homework(__file__)


def test_cdc_orders_by_source_version_and_applies_tombstones():
    snapshot = {"a": {"id": "a", "value": 1, "_lsn": 5}}
    events = [
        {"event_id": "e8", "id": "a", "op": "delete", "source_lsn": 8},
        {"event_id": "e7", "id": "a", "op": "upsert", "value": 7, "source_lsn": 7},
        {"event_id": "e6", "id": "b", "op": "upsert", "value": 2, "source_lsn": 6},
    ]
    before = deepcopy((snapshot, events))
    result = hw.apply_cdc(snapshot, events, checkpoint=5)
    assert (snapshot, events) == before
    assert "a" not in result["snapshot"]
    assert result["snapshot"]["b"]["value"] == 2
    assert result["checkpoint"] == 8


def test_replay_is_noop_and_conflicting_old_event_is_quarantined():
    snapshot = {"x": {"id": "x", "value": 9, "_lsn": 10}}
    old = {"event_id": "old", "id": "x", "op": "upsert", "value": 1, "source_lsn": 8}
    result = hw.apply_cdc(snapshot, [old], checkpoint=10)
    assert result["snapshot"] == snapshot
    assert result["checkpoint"] == 10
    assert result["quarantined"][0]["event_id"] == "old"


def test_delete_state_prevents_replay_and_stale_resurrection_across_calls():
    initial = {"x": {"id": "x", "value": 1, "_lsn": 5, "_event_id": "create"}}
    delete = {"event_id": "delete", "id": "x", "op": "delete", "source_lsn": 6}
    deleted = hw.apply_cdc(initial, [delete], checkpoint=5)
    replay = hw.apply_cdc(deleted["state"], [delete], checkpoint=6)
    assert replay["snapshot"] == {}
    assert replay["quarantined"] == []

    stale = {"event_id": "stale", "id": "x", "op": "upsert", "value": 9, "source_lsn": 5}
    result = hw.apply_cdc(deleted["state"], [stale], checkpoint=6)
    assert result["snapshot"] == {}
    assert result["quarantined"][0]["event_id"] == "stale"


def test_exact_duplicate_event_is_one_operation_but_identifier_reuse_is_conflict():
    event = {"event_id": "e1", "id": "x", "op": "upsert", "source_lsn": 1, "value": 1}
    exact = hw.apply_cdc({}, [event, dict(event)], checkpoint=0)
    assert exact["snapshot"]["x"]["value"] == 1
    assert exact["quarantined"] == []

    conflict = hw.apply_cdc({}, [event, {**event, "source_lsn": 2, "value": 2}], checkpoint=0)
    assert conflict["snapshot"]["x"]["value"] == 1
    assert conflict["quarantined"][0]["reason"] == "event_id reused with different payload"
