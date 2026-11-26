from copy import deepcopy

import pytest

from test_support import load_homework

hw = load_homework(__file__)


def test_latest_wins_invalid_is_quarantined_and_inputs_survive():
    existing = [{"event_id": "a", "amount": 2, "currency": "USD", "updated_at": "2026-01-01T00:00:00Z"}]
    incoming = [
        {"event_id": "a", "amount": 3, "currency": "usd", "updated_at": "2026-01-02T00:00:00Z"},
        {"event_id": "b", "amount": -1, "currency": "GTQ", "updated_at": "2026-01-02T00:00:00Z"},
    ]
    before = deepcopy((existing, incoming))
    result = hw.process_events(existing, incoming)
    assert (existing, incoming) == before
    assert result["published"] == [{"event_id": "a", "amount": 3, "currency": "USD", "updated_at": "2026-01-02T00:00:00Z"}]
    assert [x["event_id"] for x in result["rejected"]] == ["b"]


def test_reprocessing_is_idempotent():
    event = {"event_id": "x", "amount": 1, "currency": "eur", "updated_at": "2026-02-01T00:00:00Z"}
    once = hw.process_events([], [event])["published"]
    twice = hw.process_events(once, [event])["published"]
    assert twice == once


def test_equal_time_conflicts_are_rejected_instead_of_using_input_order():
    one = {"event_id": "x", "amount": 1, "currency": "USD", "updated_at": "2026-01-01T00:00:00Z"}
    two = {**one, "amount": 2}
    with pytest.raises(ValueError, match="conflicting versions"):
        hw.process_events([], [one, two])


@pytest.mark.parametrize("amount", [True, float("inf"), float("nan")])
def test_non_numeric_or_non_finite_amount_is_rejected(amount):
    event = {"event_id": "x", "amount": amount, "currency": "USD", "updated_at": "2026-01-01T00:00:00Z"}
    assert hw.process_events([], [event])["rejected"]
