from test_support import load_homework

hw = load_homework(__file__)


def test_delta_layout_avoids_high_cardinality_partition():
    table = {"platform": "delta", "size_tb": 20, "columns": {"event_date": 730, "customer_id": 50_000_000}, "updates_per_day": 5_000_000}
    workload = {"filters": {"event_date": 0.9, "customer_id": 0.5}, "avg_files_per_query": 20000}
    plan = hw.recommend_layout(table, workload)
    assert "customer_id" not in plan.get("partition_by", [])
    assert "event_date" in plan.get("partition_by", [])
    assert 128 <= plan["target_file_mb"] <= 1024
    assert plan["compaction_trigger"]
    assert plan["validation_metrics"]


def test_snowflake_plan_uses_cluster_not_user_managed_partitions():
    table = {"platform": "snowflake", "size_tb": 8, "columns": {"event_date": 730, "tenant_id": 1000}, "updates_per_day": 1000}
    workload = {"filters": {"event_date": 0.8, "tenant_id": 0.7}, "avg_partitions_scanned_pct": 75}
    plan = hw.recommend_layout(table, workload)
    assert not plan.get("partition_by")
    assert plan.get("cluster_by")
    assert any("cost" in x.lower() for x in plan["warnings"])
