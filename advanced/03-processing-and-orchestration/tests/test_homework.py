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
