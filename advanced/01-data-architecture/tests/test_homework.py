import math
import pytest

from test_support import load_homework

hw = load_homework(__file__)


def test_platform_has_capacity_isolation_and_residency():
    req = {"daily_events": 8_640_000_000, "peak_factor": 4, "headroom": 0.3, "regions": ["us", "eu"], "eu_must_stay_eu": True, "rpo_minutes": 15, "rto_minutes": 60, "tenants": 500, "budget": 250000}
    plan = hw.design_platform(req)
    expected_peak = 8_640_000_000 / 86400 * 4
    assert math.isclose(plan["peak_events_per_second"], expected_peak, rel_tol=0.01)
    assert plan["provisioned_events_per_second"] >= expected_peak * 1.3
    assert plan["regional_placement"]["eu"] == "eu"
    assert len(plan["isolation_controls"]) >= 4
    assert plan["failover"]["rpo_minutes"] <= 15
    assert plan["estimated_monthly_cost"] <= 250000


def test_illegal_cross_region_failover_is_rejected():
    req = {"daily_events": 1, "peak_factor": 1, "headroom": 0, "regions": ["us"], "eu_must_stay_eu": True, "rpo_minutes": 0, "rto_minutes": 0, "tenants": 1, "budget": 1}
    with pytest.raises(ValueError):
        hw.design_platform(req)
