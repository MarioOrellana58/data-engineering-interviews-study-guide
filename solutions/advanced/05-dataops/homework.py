import math


def _blast_radius(asset: str, lineage: dict[str, list[str]]) -> list[str]:
    visited = set()
    pending = [asset]
    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)
        pending.extend(lineage.get(current, []))
    return sorted(visited)


def assess_incident(asset: str, observed: dict, slo: dict, lineage: dict[str, list[str]]) -> dict:
    target = float(slo["availability_target"])
    window = float(slo["window_minutes"])
    bad_minutes = float(observed["bad_minutes"])
    if not all(math.isfinite(value) for value in (target, window, bad_minutes)) or not 0 < target < 1 or window <= 0 or bad_minutes < 0:
        raise ValueError("invalid SLO or observation")
    blast_radius = _blast_radius(asset, lineage)
    allowed_bad_minutes = (1 - target) * window
    consumed = bad_minutes / allowed_bad_minutes
    critical = sorted(set(blast_radius) & set(observed.get("critical_assets", [])))

    if critical and consumed >= 1:
        severity = "SEV-1"
    elif critical or consumed >= 1:
        severity = "SEV-2"
    else:
        severity = "SEV-3"

    return {
        "asset": asset,
        "blast_radius": blast_radius,
        "critical_consumers": critical,
        "error_budget_consumed_ratio": consumed,
        "severity": severity,
        "freeze_deployments": severity in {"SEV-1", "SEV-2"},
        "immediate_actions": [
            "assign an incident commander and owners",
            "stop or isolate the corrupt producer",
            "notify affected critical consumers",
            "restore and replay from a verified boundary",
            "reconcile consumer-visible results before closure",
        ],
        "communication_cadence_minutes": 30 if severity in {"SEV-1", "SEV-2"} else 60,
        "replay_from": observed["last_good_offset"],
    }
