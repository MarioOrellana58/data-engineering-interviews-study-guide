import pytest

from test_support import load_homework

hw = load_homework(__file__)


def test_plan_has_gated_migration_and_rollback():
    req = {"history_tb": 60, "daily_tb": 2, "rpo_minutes": 60, "rto_minutes": 240, "pii": True, "monthly_budget": 50000}
    plan = hw.migration_plan(req)
    names = [p["name"].lower() for p in plan["phases"]]
    assert any("backfill" in x for x in names)
    assert any("dual" in x or "parallel" in x for x in names)
    assert any("cutover" in x for x in names)
    assert all(p.get("exit_criteria") for p in plan["phases"])
    assert len(plan["reconciliation_checks"]) >= 4
    assert plan["rollback"] and plan["estimated_monthly_cost"] <= 50000
    assert len(plan["security_controls"]) >= 3


def test_impossible_budget_is_not_silently_accepted():
    with pytest.raises(ValueError):
        hw.migration_plan({"history_tb": 1000, "daily_tb": 50, "rpo_minutes": 1, "rto_minutes": 1, "pii": True, "monthly_budget": 10})


@pytest.mark.parametrize("rpo,rto", [(0, 10), (10, 0), (-1, 10)])
def test_recovery_objectives_must_be_positive(rpo, rto):
    with pytest.raises(ValueError):
        hw.migration_plan({"history_tb": 1, "daily_tb": 1, "rpo_minutes": rpo, "rto_minutes": rto, "pii": False, "monthly_budget": 10000})


@pytest.mark.parametrize("field,value", [("history_tb", 0), ("daily_tb", 0), ("history_tb", float("nan"))])
def test_migration_volumes_must_be_positive_and_finite(field, value):
    req = {"history_tb": 1, "daily_tb": 1, "rpo_minutes": 60, "rto_minutes": 60, "monthly_budget": 10000}
    with pytest.raises(ValueError):
        hw.migration_plan({**req, field: value})
