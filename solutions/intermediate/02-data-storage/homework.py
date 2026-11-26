def recommend_layout(table: dict, workload: dict) -> dict:
    platform = str(table.get("platform", "")).lower()
    filters = workload.get("filters", {})
    size_tb = float(table.get("size_tb", 0))
    updates_per_day = int(table.get("updates_per_day", 0))
    warnings = []

    if platform == "delta":
        files_per_query = int(workload.get("avg_files_per_query", 0))
        if size_tb < 1 and files_per_query <= 10:
            return {
                "layout_strategy": "unclustered",
                "partition_by": [],
                "cluster_by": [],
                "target_file_mb": 256,
                "compaction_trigger": "compact only when files below 64 MB exceed 20% of table bytes",
                "validation_metrics": ["files scanned", "bytes read", "task count", "p95 latency", "maintenance cost"],
                "warnings": ["Current scans are already selective; clustering cost is unlikely to pay back."],
            }
        cluster_by = [name for name, frequency in sorted(filters.items(), key=lambda item: (-item[1], item[0])) if frequency >= 0.3][:2]
        if "event_date" in filters and "event_date" not in cluster_by:
            cluster_by.insert(0, "event_date")
        if updates_per_day > 1_000_000:
            cluster_by = cluster_by[:1]
            warnings.append("High update volume favors fewer clustering keys and more frequent compaction measurement.")
        warnings.append("Measure optimization cost and bytes skipped before retaining every clustering key.")
        return {
            "layout_strategy": "liquid_clustering",
            "partition_by": [],
            "cluster_by": cluster_by or ["event_date"],
            "target_file_mb": 256 if updates_per_day > 1_000_000 else 512,
            "compaction_trigger": "compact when files below 128 MB exceed 20% of table bytes",
            "validation_metrics": ["files scanned", "bytes read", "task count", "p95 latency", "optimization cost"],
            "warnings": warnings,
        }

    if platform == "snowflake":
        scanned_pct = float(workload.get("avg_partitions_scanned_pct", 100))
        if scanned_pct <= 10:
            return {
                "layout_strategy": "snowflake_no_cluster",
                "partition_by": [],
                "cluster_by": [],
                "target_file_mb": 512,
                "compaction_trigger": "managed by Snowflake",
                "validation_metrics": ["partitions scanned", "bytes scanned", "latency", "credit cost", "queue time"],
                "warnings": ["Pruning is already selective; a clustering key would add cost without evidence of benefit."],
            }
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
