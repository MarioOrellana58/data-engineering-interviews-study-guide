import math


def storage_strategy(workload: dict) -> dict:
    depth = int(workload.get("multi_hop_depth", 0))
    relationship_pct = float(workload.get("relationship_queries_pct", 0))
    scan_tb = float(workload.get("aggregate_scan_tb", 0))
    writers = int(workload.get("concurrent_writers", 0))
    retention = int(workload.get("time_travel_days", 0))
    if (depth < 0 or not math.isfinite(relationship_pct) or not 0 <= relationship_pct <= 100
            or not math.isfinite(scan_tb) or scan_tb < 0 or writers < 0 or retention < 0):
        raise ValueError("invalid workload measurements")
    graph_needed = depth >= 3 and relationship_pct >= 30
    technologies = ["Delta lakehouse"]
    graph_projection = None
    if graph_needed:
        technologies.append("Neo4j graph database")
        graph_projection = {
            "source": "versioned lakehouse snapshot",
            "checkpoint": "publish source snapshot version with every graph projection",
            "refresh": "incremental and idempotent",
        }
    elif scan_tb >= 10:
        technologies.append("Snowflake analytical warehouse")

    concurrency = "optimistic transactions with conflict detection and idempotent writer identifiers"
    if writers > 10:
        concurrency += "; serialize compaction separately from high-contention merge writers"

    return {
        "technologies": technologies,
        "consistency_model": "snapshot isolation in the analytical source; checkpointed eventual consistency for projections",
        "physical_layout": "columnar files with compaction and workload-driven clustering",
        "concurrency_control": concurrency,
        "retention_days": max(7, retention),
        "vacuum_safety": "vacuum only after the required time-travel window and longest active transaction",
        "raw_replay_retention": "manage independently from time-travel and vacuum retention",
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
