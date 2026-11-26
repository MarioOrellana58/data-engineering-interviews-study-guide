# Data Storage: Physical Design for Snowflake and Delta

## Topic explanation

Logical models do not guarantee physical performance. In Snowflake, pruning, clustering depth, warehouse sizing, caching, and workload isolation influence cost. In Delta-style tables, file size, partition cardinality, statistics, compaction, and data skipping matter. Optimize from observed query patterns, not folklore.

**Analogy:** A library catalog helps only if shelves follow it. Partitioning chooses rooms, clustering arranges shelves, and compaction avoids storing each page in a separate envelope.

## Solved practical example

A 20 TB Delta event table has 30 million 20 KB files and 90% of queries filter by `event_date`. Partition by date, target roughly 512 MB files, compact partitions when small files exceed 20% of bytes, and cluster within recent dates by `tenant_id`. Do not partition by 10 million tenants. Validate with files scanned, bytes read, task count, p95 latency, and compaction cost before and after.

## Code exercise

Implement `recommend_layout(table, workload)`. Return platform-specific partition/cluster choices, target file size, compaction trigger, and warnings. Reject high-cardinality partitions, account for update frequency, and avoid recommending clustering when scans are already selective enough.

## AI review

Use `AI_REVIEW_PROMPT.md`; explain how you would validate the recommendation with profiles and cost evidence.

## Unit test

```bash
pytest intermediate/02-data-storage/tests -q
```
