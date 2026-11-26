import pytest

from test_support import load_homework

hw = load_homework(__file__)


def test_recovery_skips_committed_and_builds_bounded_deterministic_batches():
    events = [{"event_id": f"e{i}", "offset": i, "value": i} for i in range(1, 8)]
    committed = [{"batch_id": "old", "end_offset": 2, "output_ids": ["e1", "e2"]}]
    one = hw.recover_and_plan(events, committed, checkpoint=2, capacity=2)
    two = hw.recover_and_plan(list(reversed(events)), committed, checkpoint=2, capacity=2)
    assert one == two
    assert [len(b["output_ids"]) for b in one["batches"]] == [2, 2, 1]
    assert one["batches"][0]["start_offset"] == 3
    assert all(b["input_hash"] and b["batch_id"] for b in one["batches"])
    assert not ({"e1", "e2"} & set().union(*(set(b["output_ids"]) for b in one["batches"])))


def test_same_offset_with_distinct_events_is_rejected():
    with pytest.raises(ValueError, match="offset"):
        hw.recover_and_plan([{"event_id": "a", "offset": 1}, {"event_id": "b", "offset": 1}], [], 0, 10)


def test_same_event_id_at_different_offsets_is_rejected():
    with pytest.raises(ValueError, match="multiple offsets"):
        hw.recover_and_plan([{"event_id": "a", "offset": 1}, {"event_id": "a", "offset": 2}], [], 0, 10)


def test_committed_batch_boundary_advances_effective_checkpoint():
    events = [{"event_id": f"e{i}", "offset": i} for i in range(1, 6)]
    result = hw.recover_and_plan(events, [{"end_offset": 3, "output_ids": ["e1", "e2", "e3"]}], 1, 10)
    assert result["checkpoint"] == 3
    assert result["batches"][0]["start_offset"] == 4


def test_exact_duplicate_identity_is_deduplicated_and_conflict_is_rejected():
    event = {"event_id": "a", "offset": 1, "value": 1}
    assert hw.recover_and_plan([event, dict(event)], [], 0, 10)["batches"][0]["output_ids"] == ["a"]
    with pytest.raises(ValueError, match="conflicting payload"):
        hw.recover_and_plan([event, {**event, "value": 2}], [], 0, 10)
