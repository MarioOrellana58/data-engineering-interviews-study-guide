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
