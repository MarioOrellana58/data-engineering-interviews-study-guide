def storage_strategy(workload: dict) -> dict:
    graph_needed = workload.get("multi_hop_depth", 0) >= 3 and workload.get("relationship_queries_pct", 0) >= 30
    technologies = ["Delta lakehouse"]
    graph_projection = None
    if graph_needed:
        technologies.append("Neo4j graph database")
        graph_projection = {
            "source": "versioned lakehouse snapshot",
            "checkpoint": "publish source snapshot version with every graph projection",
            "refresh": "incremental and idempotent",
        }
    elif workload.get("aggregate_scan_tb", 0) >= 10:
        technologies.append("Snowflake analytical warehouse")

    return {
        "technologies": technologies,
        "consistency_model": "snapshot isolation in the analytical source; checkpointed eventual consistency for projections",
        "physical_layout": "columnar files with compaction and workload-driven clustering",
        "concurrency_control": "optimistic transactions with conflict detection and idempotent writer identifiers",
        "retention_days": max(7, int(workload.get("time_travel_days", 0))),
        "vacuum_safety": "vacuum only after the required time-travel window and longest active transaction",
        "graph_projection": graph_projection,
        "validation_metrics": [
            "snapshot-to-projection lag",
            "files or partitions scanned",
            "query p95 latency",
            "write-conflict rate",
            "storage and compute cost",
            "projection reconciliation mismatches",
        ],
    }
