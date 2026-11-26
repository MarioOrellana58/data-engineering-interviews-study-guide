from test_support import load_homework

hw = load_homework(__file__)


def test_multihop_fraud_uses_graph_without_abandoning_analytics():
    work = {"multi_hop_depth": 5, "relationship_queries_pct": 70, "aggregate_scan_tb": 20, "concurrent_writers": 30, "time_travel_days": 30}
    plan = hw.storage_strategy(work)
    technologies = {x.lower() for x in plan["technologies"]}
    assert any("graph" in x or "neo4j" in x for x in technologies)
    assert any("delta" in x or "lakehouse" in x or "snowflake" in x for x in technologies)
    assert plan["graph_projection"]
    assert plan["concurrency_control"]
    assert plan["retention_days"] >= 30
    assert len(plan["validation_metrics"]) >= 5


def test_scan_heavy_workload_does_not_default_to_graph():
    work = {"multi_hop_depth": 1, "relationship_queries_pct": 2, "aggregate_scan_tb": 100, "concurrent_writers": 1, "time_travel_days": 7}
    plan = hw.storage_strategy(work)
    assert not any("neo4j" in x.lower() for x in plan["technologies"])
