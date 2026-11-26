def migration_plan(requirements: dict) -> dict:
    history_tb = float(requirements.get("history_tb", 0))
    daily_tb = float(requirements.get("daily_tb", 0))
    budget = float(requirements.get("monthly_budget", 0))
    if history_tb < 0 or daily_tb < 0 or budget <= 0:
        raise ValueError("invalid volume or budget")

    estimated_cost = 1_000 + history_tb * 20 + daily_tb * 500
    if requirements.get("rpo_minutes", 0) <= 1 and requirements.get("rto_minutes", 0) <= 1:
        estimated_cost *= 2
    if estimated_cost > budget:
        raise ValueError("requirements cannot be met within the monthly budget")

    phases = [
        {
            "name": "Backfill immutable history",
            "exit_criteria": ["all manifests loaded", "business-grain reconciliation passes", "replay drill succeeds"],
        },
        {
            "name": "Dual-run pipelines",
            "exit_criteria": ["seven consecutive matching runs", "freshness and cost remain within limits"],
        },
        {
            "name": "Consumer cutover",
            "exit_criteria": ["low-risk canary consumers approve", "critical owners approve", "rollback tested"],
        },
        {
            "name": "Retire legacy path",
            "exit_criteria": ["rollback window expires", "runbooks and ownership transferred"],
        },
    ]
    security = ["least-privilege roles", "encryption in transit and at rest", "audited access"]
    if requirements.get("pii"):
        security += ["tokenized sensitive fields", "masked nonproduction data"]

    return {
        "phases": phases,
        "backfill_strategy": "Load immutable source partitions by date with resumable manifests and bounded parallelism.",
        "dual_run_days": 7,
        "reconciliation_checks": [
            "row count by business date",
            "distinct business keys",
            "sums by currency and status",
            "null and reject rates",
            "sampled canonical row hashes",
        ],
        "rollback": "Switch the versioned consumer view to the legacy output and replay from the last verified manifest.",
        "security_controls": security,
        "estimated_monthly_cost": estimated_cost,
        "rpo_minutes": requirements.get("rpo_minutes"),
        "rto_minutes": requirements.get("rto_minutes"),
    }
