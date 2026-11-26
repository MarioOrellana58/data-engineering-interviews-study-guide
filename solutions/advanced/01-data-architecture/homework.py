def design_platform(requirements: dict) -> dict:
    regions = {str(region).lower() for region in requirements.get("regions", [])}
    if requirements.get("eu_must_stay_eu") and "eu" not in regions:
        raise ValueError("EU-resident data requires an approved EU region")

    daily_events = float(requirements.get("daily_events", 0))
    peak_factor = float(requirements.get("peak_factor", 1))
    headroom = float(requirements.get("headroom", 0))
    if daily_events < 0 or peak_factor <= 0 or headroom < 0:
        raise ValueError("invalid capacity inputs")

    peak = daily_events / 86_400 * peak_factor
    provisioned = peak * (1 + headroom)
    estimated_cost = max(500.0, provisioned * 0.20 + len(regions) * 2_000)
    budget = float(requirements.get("budget", 0))
    if estimated_cost > budget:
        raise ValueError("capacity and residency requirements exceed budget")

    placement = {region: region for region in sorted(regions)}
    failover = {
        "rpo_minutes": requirements.get("rpo_minutes"),
        "rto_minutes": requirements.get("rto_minutes"),
        "eu": "second approved EU region; never cross the residency boundary",
        "us": "second US region",
    }
    return {
        "peak_events_per_second": peak,
        "provisioned_events_per_second": provisioned,
        "regional_placement": placement,
        "tenancy_model": "shared control plane with region-scoped data planes",
        "isolation_controls": [
            "per-tenant queues",
            "tenant quotas and rate limits",
            "isolated compute pools",
            "region-scoped encryption keys",
            "tenant cost tags",
        ],
        "encryption": "envelope encryption with region-scoped managed keys and audited rotation",
        "failover": failover,
        "observability": ["tenant lag", "queue depth", "reject rate", "regional capacity", "cost by tenant"],
        "estimated_monthly_cost": estimated_cost,
    }
