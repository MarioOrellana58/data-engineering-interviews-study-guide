def recommend_layout(table: dict, workload: dict) -> dict:
    platform = str(table.get("platform", "")).lower()
    filters = workload.get("filters", {})
    warnings = []

    if platform == "delta":
        cluster_by = [name for name, frequency in sorted(filters.items(), key=lambda item: (-item[1], item[0])) if frequency >= 0.3][:2]
        if "event_date" in filters and "event_date" not in cluster_by:
            cluster_by.insert(0, "event_date")
        warnings.append("Measure optimization cost and bytes skipped before retaining every clustering key.")
        return {
            "layout_strategy": "liquid_clustering",
            "partition_by": [],
            "cluster_by": cluster_by or ["event_date"],
            "target_file_mb": 512,
            "compaction_trigger": "compact when files below 128 MB exceed 20% of table bytes",
            "validation_metrics": ["files scanned", "bytes read", "task count", "p95 latency", "optimization cost"],
            "warnings": warnings,
        }

    if platform == "snowflake":
        cluster_by = [name for name, frequency in sorted(filters.items(), key=lambda item: (-item[1], item[0])) if frequency >= 0.5][:2]
        warnings.append("Automatic clustering has a recurring compute cost; compare it with pruning savings.")
        return {
            "layout_strategy": "snowflake_clustering",
            "partition_by": [],
            "cluster_by": cluster_by,
            "target_file_mb": 512,
            "compaction_trigger": "managed by Snowflake micro-partition maintenance",
            "validation_metrics": ["partitions scanned", "bytes scanned", "clustering depth", "latency", "credit cost"],
            "warnings": warnings,
        }
    raise ValueError(f"unsupported platform: {platform}")
