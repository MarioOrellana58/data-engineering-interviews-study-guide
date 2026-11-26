# Data Storage: Lakehouse Internals and Graph Decisions

## Topic explanation

Lakehouse correctness depends on transaction logs, snapshot isolation, optimistic concurrency, compaction, retention, and schema protocol—not merely Parquet files. Graph databases earn their cost when multi-hop traversal and relationship evolution dominate; they are not a universal replacement for relational analytics.

**Analogy:** Parquet files are pages, while a transaction log is the table of contents and revision history. Neo4j is a subway map: excellent for routes across connections, inefficient for totaling every ticket sold last quarter.

## Solved practical example

A fraud team asks for five-hop paths between accounts, devices, cards, and IPs, while Finance scans 20 TB for monthly totals. Use a Delta/Snowflake analytical source of truth plus a versioned graph projection in Neo4j. Publish projection checkpoints so graph results can be traced to a lakehouse snapshot. Keep 30-day snapshots, set vacuum beyond the longest replay window, and alert on graph projection lag. Moving Finance aggregation into Neo4j would increase cost without improving its scan workload.

## Code exercise

Implement `storage_strategy(workload)`. Choose relational, Snowflake, Delta/lakehouse, graph, or a justified hybrid. Return consistency model, physical layout, concurrency approach, retention/vacuum safety, graph projection when applicable, and five validation metrics.

The strategy must prefer graph only for meaningful multi-hop workloads and retain an analytical system for aggregate scans.

## AI review

Use `AI_REVIEW_PROMPT.md`; defend snapshot retention, concurrent writers, and graph synchronization.

## Unit test

```bash
pytest advanced/02-data-storage/tests -q
```
