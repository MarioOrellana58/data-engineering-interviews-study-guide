from test_support import load_homework

hw = load_homework(__file__)


def test_out_of_order_changes_form_non_overlapping_history():
    changes = [
        {"customer_id": "c1", "at": "2026-03-01", "tier": "gold"},
        {"customer_id": "c1", "at": "2026-01-01", "tier": "bronze"},
        {"customer_id": "c1", "at": "2026-02-01", "tier": "silver"},
        {"customer_id": "c1", "at": "2026-02-15", "tier": "silver"},
    ]
    rows = hw.build_scd2(changes)
    assert [r["tier"] for r in rows] == ["bronze", "silver", "gold"]
    assert [r["valid_to"] for r in rows[:-1]] == ["2026-02-01", "2026-03-01"]
    assert rows[-1]["valid_to"] is None
    assert [r["is_current"] for r in rows] == [False, False, True]
    assert len({r["customer_sk"] for r in rows}) == 3


def test_keys_are_deterministic_across_input_order():
    changes = [{"customer_id": "b", "at": "2026-01-01", "tier": "x"}, {"customer_id": "a", "at": "2026-01-01", "tier": "y"}]
    assert hw.build_scd2(changes) == hw.build_scd2(list(reversed(changes)))
