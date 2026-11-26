from test_support import load_homework

hw = load_homework(__file__)


def test_delta_layout_avoids_high_cardinality_partition():
    table = {"platform": "delta", "size_tb": 20, "columns": {"event_date": 730, "customer_id": 50_000_000}, "updates_per_day": 5_000_000}
    workload = {"filters": {"event_date": 0.9, "customer_id": 0.5}, "avg_files_per_query": 20000}
    plan = hw.recommend_layout(table, workload)
    assert plan["layout_strategy"] in {"liquid_clustering", "partitioned_zorder"}
    assert "customer_id" not in plan.get("partition_by", [])
    if plan["layout_strategy"] == "liquid_clustering":
        assert not plan.get("partition_by")
        assert "event_date" in plan.get("cluster_by", [])
    else:
        assert "event_date" in plan.get("partition_by", [])
        assert "customer_id" in plan.get("zorder_by", [])
    assert 128 <= plan["target_file_mb"] <= 1024
    assert plan["compaction_trigger"]
    assert plan["validation_metrics"]


def test_snowflake_plan_uses_cluster_not_user_managed_partitions():
    table = {"platform": "snowflake", "size_tb": 8, "columns": {"event_date": 730, "tenant_id": 1000}, "updates_per_day": 1000}
    workload = {"filters": {"event_date": 0.8, "tenant_id": 0.7}, "avg_partitions_scanned_pct": 75}
    plan = hw.recommend_layout(table, workload)
    assert plan["layout_strategy"] == "snowflake_clustering"
    assert not plan.get("partition_by")
    assert plan.get("cluster_by")
    assert any("cost" in x.lower() for x in plan["warnings"])


def test_selective_small_workloads_do_not_pay_for_unnecessary_clustering():
    table = {"platform": "delta", "size_tb": 0.2, "columns": {"event_date": 30}, "updates_per_day": 0}
    workload = {"filters": {"event_date": 0.9}, "avg_files_per_query": 4}
    assert hw.recommend_layout(table, workload)["layout_strategy"] == "unclustered"

    table["platform"] = "snowflake"
    workload = {"filters": {"event_date": 0.9}, "avg_partitions_scanned_pct": 5}
    assert hw.recommend_layout(table, workload)["layout_strategy"] == "snowflake_no_cluster"


def test_high_update_rate_changes_file_and_clustering_plan():
    base = {"platform": "delta", "size_tb": 20, "columns": {"event_date": 365, "customer_id": 1_000_000}}
    workload = {"filters": {"event_date": 0.9, "customer_id": 0.8}, "avg_files_per_query": 5000}
    low = hw.recommend_layout({**base, "updates_per_day": 10}, workload)
    high = hw.recommend_layout({**base, "updates_per_day": 10_000_000}, workload)
    assert high["target_file_mb"] < low["target_file_mb"]
    assert high.get("cluster_by", []) != low.get("cluster_by", [])
