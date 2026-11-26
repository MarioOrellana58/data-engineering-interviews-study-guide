# Data Storage: Physical Design for Snowflake and Delta

## Topic explanation

Logical models do not guarantee physical performance. In Snowflake, pruning, clustering depth, warehouse sizing, caching, and workload isolation influence cost. In Delta-style tables, file size, partition cardinality, statistics, compaction, and data skipping matter. Optimize from observed query patterns, not folklore.

## Practical example and analogy

A library catalog is useful only if shelves follow it. Partitioning is choosing rooms, clustering is arranging shelves, and file compaction is avoiding a separate envelope for every page.

## Code exercise

Implement `recommend_layout(table, workload)`. Return platform-specific partition/cluster choices, target file size, compaction trigger, and warnings. Reject high-cardinality partitions, account for update frequency, and avoid recommending clustering when scans are already selective enough.

## AI review

Use `AI_REVIEW_PROMPT.md`; explain how you would validate the recommendation with profiles and cost evidence.

## Unit test

```bash
pytest intermediate/02-data-storage/tests -q
```
