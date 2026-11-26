from test_support import load_homework

hw = load_homework(__file__)


def test_daily_batch_is_replayable_and_partitioned():
    req = {"daily_gb": 400, "freshness_minutes": 1440, "replay": True, "pii": False}
    plan = hw.design_pipeline(req)
    assert plan["delivery_mode"] in {"batch", "micro-batch"}
    assert plan["partition_key"]
    assert "raw" in {x.lower() for x in plan["layers"]}
    assert any(word in plan["recovery"].lower() for word in ("replay", "backfill", "immutable"))
    assert plan["rpo_minutes"] <= 1440


def test_low_latency_pii_changes_the_design():
    req = {"daily_gb": 20, "freshness_minutes": 2, "replay": True, "pii": True}
    plan = hw.design_pipeline(req)
    assert plan["delivery_mode"] in {"streaming", "micro-batch"}
    controls = " ".join(plan["security_controls"]).lower()
    assert any(x in controls for x in ("encrypt", "token", "mask"))
    assert plan["rto_minutes"] <= 60
    assert len(plan.get("assumptions", [])) >= 2
