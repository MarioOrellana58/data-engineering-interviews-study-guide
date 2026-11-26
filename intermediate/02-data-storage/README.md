# Data Storage: Physical Design for Snowflake and Delta

## Topic explanation

Logical models do not guarantee physical performance. In Snowflake, pruning, clustering depth, warehouse sizing, caching, and workload isolation influence cost. In Delta-style tables, file size, statistics, compaction, and data skipping matter. Legacy partitioned tables can combine partition pruning with `ZORDER`; modern Databricks tables can instead use liquid clustering, which replaces partitioning and `ZORDER` and must not be combined with them. Optimize from observed query patterns, not folklore.

**Analogy:** A library catalog helps only if shelves follow it. Partitioning chooses rooms, clustering arranges shelves, and compaction avoids storing each page in a separate envelope.

## Solved practical example

A 20-terabyte (TB) Delta event table has 30 million 20-kilobyte (KB) files and 90% of queries filter by `event_date`. For a new Databricks table, keep it unpartitioned and use liquid clustering on `event_date` and, if profiles justify it, `tenant_id`; target roughly 512-megabyte (MB) files and compact when small files exceed 20% of bytes. For a legacy partitioned table, date partitioning plus `ZORDER BY tenant_id` is a different valid strategy. Do not combine liquid clustering with either approach. Validate with files scanned, bytes read, task count, 95th-percentile (p95) latency, and optimization cost before and after.

## Code exercise

Implement `recommend_layout(table, workload)`. Return a `layout_strategy` plus platform-specific partition or clustering choices, target file size, compaction trigger, validation metrics, and warnings. For Delta, choose either `liquid_clustering` with no partitions or `partitioned_zorder`; never combine the two. Reject high-cardinality partitions, account for update frequency, and avoid recommending clustering when scans are already selective enough.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; explain how you would validate the recommendation with profiles and cost evidence.

## Unit test

```bash
pytest intermediate/02-data-storage/tests -q
```
