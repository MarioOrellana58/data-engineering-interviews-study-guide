from datetime import datetime, timezone

from test_support import load_homework

hw = load_homework(__file__)

CONTRACT = {"required": ["id", "amount", "event_at"], "unique": "id", "max_age_minutes": 60, "max_reject_rate": 0.4}
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)


def test_reports_reasons_metrics_and_publish_decision():
    rows = [
        {"id": "a", "amount": 2, "event_at": "2026-01-01T11:30:00+00:00"},
        {"id": "a", "amount": 3, "event_at": "2026-01-01T11:40:00+00:00"},
        {"id": "b", "amount": None, "event_at": "2026-01-01T11:50:00+00:00"},
    ]
    result = hw.validate_batch(rows, CONTRACT, NOW)
    assert len(result["accepted"]) == 1
    assert len(result["rejected"]) == 2
    assert all(r.get("reason") for r in result["rejected"])
    assert result["metrics"]["input_count"] == 3
    assert result["publish"] is False


def test_freshness_can_block_an_otherwise_valid_batch():
    rows = [{"id": "x", "amount": 1, "event_at": "2026-01-01T08:00:00+00:00"}]
    result = hw.validate_batch(rows, CONTRACT, NOW)
    assert result["publish"] is False
    assert result["metrics"]["freshness_minutes"] >= 240
