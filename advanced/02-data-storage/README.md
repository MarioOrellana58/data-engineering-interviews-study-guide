# Data Storage: Lakehouse Internals and Graph Decisions

## Topic explanation

Lakehouse correctness depends on transaction logs, snapshot isolation, optimistic concurrency, compaction, retention, and schema protocol—not merely Parquet files. Graph databases earn their cost when multi-hop traversal and relationship evolution dominate; they are not a universal replacement for relational analytics.

## Practical example and analogy

Parquet files are pages; a transaction log is the table of contents plus revision history. Neo4j is a subway map: excellent for routes across connections, inefficient for totaling every ticket sold last quarter.

## Code exercise

Implement `storage_strategy(workload)`. Choose relational, Snowflake, Delta/lakehouse, graph, or a justified hybrid. Return consistency model, physical layout, concurrency approach, retention/vacuum safety, graph projection when applicable, and five validation metrics.

The strategy must prefer graph only for meaningful multi-hop workloads and retain an analytical system for aggregate scans.

## AI review

Use `AI_REVIEW_PROMPT.md`; defend snapshot retention, concurrent writers, and graph synchronization.

## Unit test

```bash
pytest advanced/02-data-storage/tests -q
```
