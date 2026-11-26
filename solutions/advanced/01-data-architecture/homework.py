import math


def design_platform(requirements: dict) -> dict:
    regions = {str(region).lower() for region in requirements.get("regions", [])}
    eu_regions = sorted(region for region in regions if region == "eu" or region.startswith("eu-"))
    us_regions = sorted(region for region in regions if region == "us" or region.startswith("us-"))
    if requirements.get("eu_must_stay_eu") and not eu_regions:
        raise ValueError("EU-resident data requires an approved EU region")

    daily_events = float(requirements.get("daily_events", 0))
    peak_factor = float(requirements.get("peak_factor", 1))
    headroom = float(requirements.get("headroom", 0))
    rpo = float(requirements.get("rpo_minutes", 0))
    rto = float(requirements.get("rto_minutes", 0))
    tenants = int(requirements.get("tenants", 0))
    numeric = (daily_events, peak_factor, headroom, rpo, rto)
    if not all(math.isfinite(value) for value in numeric) or daily_events < 0 or peak_factor <= 0 or headroom < 0 or rpo <= 0 or rto <= 0 or tenants < 1:
        raise ValueError("invalid capacity inputs")

    peak = daily_events / 86_400 * peak_factor
    provisioned = peak * (1 + headroom)
    estimated_cost = max(500.0, provisioned * 0.20 + len(regions) * 2_000 + tenants * 10)
    budget = float(requirements.get("budget", 0))
    if not math.isfinite(budget) or budget <= 0 or estimated_cost > budget:
        raise ValueError("capacity and residency requirements exceed budget")

    placement = {region: region for region in sorted(regions)}
    failover = {
        "rpo_minutes": rpo,
        "rto_minutes": rto,
        "eu": eu_regions[1] if len(eu_regions) > 1 else "not configured: add a second approved EU region",
        "us": us_regions[1] if len(us_regions) > 1 else "not configured: add a second US region",
        "regional_failover_ready": {
            "eu": len(eu_regions) > 1,
            "us": len(us_regions) > 1,
        },
    }
    return {
        "peak_events_per_second": peak,
        "provisioned_events_per_second": provisioned,
        "regional_placement": placement,
        "tenancy_model": "shared control plane with region-scoped data planes",
        "tenant_count": tenants,
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
