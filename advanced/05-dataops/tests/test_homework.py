from test_support import load_homework

hw = load_homework(__file__)


def test_transitive_critical_impact_drives_severity_and_freeze():
    lineage = {"raw_orders": ["curated_orders"], "curated_orders": ["finance_report", "sandbox"], "finance_report": []}
    observed = {"bad_minutes": 90, "window_minutes": 43200, "critical_assets": ["finance_report"], "last_good_offset": 400}
    slo = {"availability_target": 0.999, "window_minutes": 43200}
    result = hw.assess_incident("raw_orders", observed, slo, lineage)
    assert "finance_report" in result["blast_radius"]
    assert result["error_budget_consumed_ratio"] > 1
    assert result["severity"] in {"SEV-1", "SEV-2"}
    assert result["freeze_deployments"] is True
    assert result["replay_from"] == 400
    assert len(result["immediate_actions"]) >= 4


def test_lineage_cycles_do_not_loop_forever():
    result = hw.assess_incident("a", {"bad_minutes": 1, "window_minutes": 100, "critical_assets": [], "last_good_offset": 0}, {"availability_target": 0.9, "window_minutes": 100}, {"a": ["b"], "b": ["a"]})
    assert set(result["blast_radius"]) == {"a", "b"}
