from test_support import load_homework

hw = load_homework(__file__)


def test_safe_change_has_staged_rollout_and_rollback():
    change = {"breaking": False, "pii": False, "downstream_critical": ["finance"]}
    evidence = {"tests_passed": True, "lineage_reviewed": True, "canary_error_delta": 0.001}
    result = hw.deployment_decision(change, evidence)
    assert result["deploy"] is True
    assert len(result["rollout_steps"]) >= 3
    assert result["rollback_trigger"]
    assert "finance" in " ".join(result["required_approvals"]).lower()


def test_breaking_or_regressed_change_is_blocked_with_reasons():
    change = {"breaking": True, "migration_window": None, "pii": True, "downstream_critical": []}
    evidence = {"tests_passed": True, "lineage_reviewed": True, "canary_error_delta": 0.2}
    result = hw.deployment_decision(change, evidence)
    assert result["deploy"] is False
    reasons = " ".join(result["reasons"]).lower()
    assert "breaking" in reasons or "migration" in reasons
    assert "canary" in reasons or "regression" in reasons
