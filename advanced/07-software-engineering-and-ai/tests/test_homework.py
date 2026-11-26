from test_support import load_homework

hw = load_homework(__file__)


def test_future_and_late_knowledge_do_not_leak():
    labels = [{"entity_id": "u1", "label_at": "2026-01-10T12:00:00+00:00", "label": 1}]
    events = [
        {"event_id": "in", "entity_id": "u1", "event_at": "2026-01-05T00:00:00+00:00", "ingested_at": "2026-01-05T00:01:00+00:00", "amount": 10},
        {"event_id": "late", "entity_id": "u1", "event_at": "2026-01-06T00:00:00+00:00", "ingested_at": "2026-01-11T00:00:00+00:00", "amount": 20},
        {"event_id": "future", "entity_id": "u1", "event_at": "2026-01-10T12:00:00+00:00", "ingested_at": "2026-01-10T12:00:00+00:00", "amount": 30},
        {"event_id": "old", "entity_id": "u1", "event_at": "2026-01-01T00:00:00+00:00", "ingested_at": "2026-01-01T00:00:00+00:00", "amount": 40},
    ]
    row = hw.materialize_features(labels, events, "v3")[0]
    assert row["txn_count_7d"] == 1 and row["txn_amount_7d"] == 10
    assert row["definition_version"] == "v3"
    assert row["feature_hash"]


def test_result_is_deterministic_across_event_order():
    labels = [{"entity_id": "u", "label_at": "2026-01-10T00:00:00+00:00", "label": 0}]
    events = [{"event_id": str(i), "entity_id": "u", "event_at": f"2026-01-0{i}T00:00:00+00:00", "ingested_at": f"2026-01-0{i}T00:01:00+00:00", "amount": i} for i in (4, 5)]
    assert hw.materialize_features(labels, events, "v1") == hw.materialize_features(labels, list(reversed(events)), "v1")
