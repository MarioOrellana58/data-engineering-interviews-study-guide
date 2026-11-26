from test_support import load_homework

hw = load_homework(__file__)


def test_late_correction_changes_current_belief_not_past_knowledge():
    changes = [
        {"entity_id": "a", "effective_at": "2026-01-01", "recorded_at": "2026-01-02", "status": "silver"},
        {"entity_id": "a", "effective_at": "2026-02-01", "recorded_at": "2026-02-02", "status": "gold"},
        {"entity_id": "a", "effective_at": "2026-01-15", "recorded_at": "2026-03-01", "status": "bronze"},
    ]
    rows = hw.build_bitemporal(changes)
    feb_view = hw.as_of(rows, "a", "2026-01-20", "2026-02-15")
    march_view = hw.as_of(rows, "a", "2026-01-20", "2026-03-02")
    assert feb_view["status"] == "silver"
    assert march_view["status"] == "bronze"


def test_no_overlapping_visible_rows_for_same_query_point():
    changes = [
        {"entity_id": "x", "effective_at": "2026-01-01", "recorded_at": "2026-01-01", "value": 1},
        {"entity_id": "x", "effective_at": "2026-01-01", "recorded_at": "2026-01-03", "value": 2},
    ]
    rows = hw.build_bitemporal(changes)
    assert hw.as_of(rows, "x", "2026-01-02", "2026-01-02")["value"] == 1
    assert hw.as_of(rows, "x", "2026-01-02", "2026-01-04")["value"] == 2
