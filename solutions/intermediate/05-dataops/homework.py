import math


def deployment_decision(change: dict, evidence: dict) -> dict:
    reasons = []
    if not evidence.get("tests_passed"):
        reasons.append("required tests did not pass")
    if not evidence.get("lineage_reviewed"):
        reasons.append("lineage impact has not been reviewed")
    if change.get("breaking") and not change.get("migration_window"):
        reasons.append("breaking change has no migration window")
    canary_delta = evidence.get("canary_error_delta", 0)
    if type(canary_delta) not in (int, float) or not math.isfinite(canary_delta):
        reasons.append("canary error delta is missing or invalid")
    elif canary_delta > 0.01:
        reasons.append("canary regression exceeds the 1% threshold")

    approvals = [f"owner of {asset}" for asset in change.get("downstream_critical", [])]
    if change.get("pii"):
        approvals.append("privacy and security owner")

    return {
        "deploy": not reasons,
        "reasons": reasons,
        "required_approvals": approvals,
        "rollout_steps": ["shadow validation", "5% canary", "25% canary", "100% promotion"],
        "rollback_trigger": "roll back on contract failure, freshness breach, or error-rate increase above 1%",
    }
