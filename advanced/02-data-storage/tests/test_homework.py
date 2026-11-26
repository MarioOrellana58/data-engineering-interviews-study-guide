import pytest

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


def test_writer_concurrency_changes_controls_and_replay_retention_is_separate():
    base = {"multi_hop_depth": 1, "relationship_queries_pct": 0, "aggregate_scan_tb": 1, "time_travel_days": 7}
    low = hw.storage_strategy({**base, "concurrent_writers": 1})
    high = hw.storage_strategy({**base, "concurrent_writers": 50})
    assert low["concurrency_control"] != high["concurrency_control"]
    assert "independently" in high["raw_replay_retention"].lower()


@pytest.mark.parametrize("field,value", [("relationship_queries_pct", 101), ("aggregate_scan_tb", -1), ("concurrent_writers", -1)])
def test_invalid_workload_measurements_are_rejected(field, value):
    base = {"multi_hop_depth": 1, "relationship_queries_pct": 1, "aggregate_scan_tb": 1,
            "concurrent_writers": 1, "time_travel_days": 7}
    with pytest.raises(ValueError):
        hw.storage_strategy({**base, field: value})
