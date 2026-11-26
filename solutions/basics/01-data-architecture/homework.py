"""Reference solution for a requirements-driven pipeline design."""


def design_pipeline(requirements: dict) -> dict:
    daily_gb = float(requirements.get("daily_gb", 0))
    freshness = int(requirements.get("freshness_minutes", 0))
    if daily_gb < 0 or freshness <= 0:
        raise ValueError("daily_gb must be nonnegative and freshness_minutes positive")

    if freshness <= 5:
        delivery_mode = "streaming"
        rpo_minutes, rto_minutes = min(freshness, 5), 30
    elif freshness <= 60:
        delivery_mode = "micro-batch"
        rpo_minutes, rto_minutes = min(freshness, 30), 60
    else:
        delivery_mode = "batch"
        rpo_minutes, rto_minutes = freshness, min(240, freshness)

    security_controls = ["encryption in transit", "least-privilege service roles"]
    if requirements.get("pii"):
        security_controls += ["encryption at rest with managed keys", "tokenize sensitive fields", "masked nonproduction views"]

    recovery = "Restore from the last committed manifest."
    if requirements.get("replay"):
        recovery = "Replay or backfill from immutable raw data using idempotent batch manifests."

    return {
        "delivery_mode": delivery_mode,
        "layers": ["raw", "validated", "curated", "serving"],
        "partition_key": "event_date",
        "recovery": recovery,
        "rpo_minutes": rpo_minutes,
        "rto_minutes": rto_minutes,
        "security_controls": security_controls,
        "assumptions": [
            "Source timestamps are stable and normalized to UTC.",
            "Object storage is durable across worker loss.",
            f"Average daily input is approximately {daily_gb:g} GB.",
        ],
    }
