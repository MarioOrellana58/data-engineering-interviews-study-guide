from datetime import date

from test_support import load_homework

hw = load_homework(__file__)


def test_storage_choices_follow_workload():
    oltp = hw.choose_storage({"point_reads": True, "transactions": True, "large_scans": False, "schema_changes": "low"})
    analytics = hw.choose_storage({"point_reads": False, "transactions": False, "large_scans": True, "schema_changes": "medium"})
    assert oltp["technology"].lower() in {"postgresql", "postgres", "relational row store"}
    assert analytics["format"].lower() in {"parquet", "delta", "iceberg"}
    assert len(oltp["reasons"]) >= 2 and len(analytics["reasons"]) >= 2


def test_partition_pruning_is_inclusive_and_ordered():
    parts = [
        {"path": "d=2026-01-03/f.parquet", "date": date(2026, 1, 3)},
        {"path": "d=2026-01-01/f.parquet", "date": date(2026, 1, 1)},
        {"path": "d=2026-01-02/f.parquet", "date": date(2026, 1, 2)},
    ]
    assert hw.files_to_scan(parts, date(2026, 1, 2), date(2026, 1, 3)) == [
        "d=2026-01-02/f.parquet", "d=2026-01-03/f.parquet"
    ]


def test_schema_change_rate_affects_analytical_format_choice():
    stable = hw.choose_storage({"large_scans": True, "schema_changes": "low"})
    evolving = hw.choose_storage({"large_scans": True, "schema_changes": "high"})
    assert stable["format"] != evolving["format"]
    assert "schema" in " ".join(evolving["reasons"]).lower()
