# Data Storage: Physical Design for Snowflake and Delta

## Topic explanation

Logical models do not guarantee physical performance. In Snowflake, pruning, clustering depth, warehouse sizing, caching, and workload isolation influence cost. In Delta-style tables, file size, statistics, compaction, and data skipping matter. Legacy partitioned tables can combine partition pruning with `ZORDER`; modern Databricks tables can instead use liquid clustering, which replaces partitioning and `ZORDER` and must not be combined with them. Optimize from observed query patterns, not folklore.

**Analogy:** A library catalog helps only if shelves follow it. Partitioning chooses rooms, clustering arranges shelves, and compaction avoids storing each page in a separate envelope.

## Solved practical example

A 20-terabyte (TB) Delta event table has 30 million 20-kilobyte (KB) files and 90% of queries filter by `event_date`. For a new Databricks table, keep it unpartitioned and use liquid clustering on `event_date` and, if profiles justify it, `tenant_id`; target roughly 512-megabyte (MB) files and compact when small files exceed 20% of bytes. For a legacy partitioned table, date partitioning plus `ZORDER BY tenant_id` is a different valid strategy. Do not combine liquid clustering with either approach. Validate with files scanned, bytes read, task count, 95th-percentile (p95) latency, and optimization cost before and after.

## Code exercise

Implement `recommend_layout(table, workload)`. Return a `layout_strategy` plus platform-specific partition or clustering choices, target file size, compaction trigger, validation metrics, and warnings. For Delta, choose either `liquid_clustering` with no partitions or `partitioned_zorder`; never combine the two. Reject high-cardinality partitions, account for update frequency, and avoid recommending clustering when scans are already selective enough.

### Homework contract

`table` describes `platform`, `size_tb`, column cardinalities, and update volume. `workload` provides filter frequencies plus a platform-specific scan metric. Return `layout_strategy`, `partition_by`, `cluster_by` or `zorder_by`, `target_file_mb`, `compaction_trigger`, `validation_metrics`, and `warnings`.

For Delta, `liquid_clustering` means `partition_by` is empty and clustering includes the dominant date filter. `partitioned_zorder` means date partitioning and a separate `zorder_by`; never return both liquid clustering and partitioning. A small table already scanning at most 10 files may use `unclustered`. For Snowflake, users do not create physical partitions: use `snowflake_clustering`, leave `partition_by` empty, and warn about clustering cost; use `snowflake_no_cluster` when at most 10 percent of micro-partitions are scanned. Keep target files between 128 and 1,024 megabytes. Update volume must influence clustering width, target size, or maintenance guidance.

### Example input and expected output

```python
table = {
    "platform": "delta",
    "size_tb": 5,
    "columns": {"event_date": 365, "account_id": 8_000_000},
    "updates_per_day": 100_000,
}
workload = {"filters": {"event_date": 0.85, "account_id": 0.4}, "avg_files_per_query": 4_000}
```

One valid recommendation is:

```python
{
    "layout_strategy": "liquid_clustering",
    "partition_by": [],
    "cluster_by": ["event_date", "account_id"],
    "target_file_mb": 512,
    "compaction_trigger": "compact when small files exceed 20% of bytes",
    "validation_metrics": ["files scanned", "bytes read", "p95 latency", "optimization cost"],
    "warnings": ["validate the second clustering key against its maintenance cost"],
}
```

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; explain how you would validate the recommendation with profiles and cost evidence.

## Unit test

```bash
pytest intermediate/02-data-storage/tests -q
```
