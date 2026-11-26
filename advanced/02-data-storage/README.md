# Data Storage: Lakehouse Internals and Graph Decisions

## Topic explanation

Lakehouse correctness depends on transaction logs, snapshot isolation, optimistic concurrency, compaction, retention, and schema protocol—not merely Parquet files. Graph databases earn their cost when multi-hop traversal and relationship evolution dominate; they are not a universal replacement for relational analytics.

**Analogy:** Parquet files are pages, while a transaction log is the table of contents and revision history. Neo4j is a subway map: excellent for routes across connections, inefficient for totaling every ticket sold last quarter.

## Solved practical example

A fraud team asks for five-hop paths between accounts, devices, cards, and Internet Protocol (IP) addresses, while Finance scans 20 terabytes (TB) for monthly totals. Use a Delta/Snowflake analytical source of truth plus a versioned graph projection in Neo4j. Publish projection checkpoints so graph results can be traced to a lakehouse snapshot. If 30 days of Delta time travel are required, configure deleted-file retention accordingly and ensure `VACUUM` does not remove those files; retain the independent raw replay log according to its own recovery policy. Also account for long-running transactions before shortening vacuum retention. Alert on graph projection lag. Moving Finance aggregation into Neo4j would increase cost without improving its scan workload.

## Code exercise

Implement `storage_strategy(workload)`. Choose relational, Snowflake, Delta/lakehouse, graph, or a justified hybrid. Return consistency model, physical layout, concurrency approach, retention/vacuum safety, graph projection when applicable, and five validation metrics.

The strategy must prefer graph only for meaningful multi-hop workloads and retain an analytical system for aggregate scans.

### Homework contract

`workload` contains multi-hop depth, percentage of relationship queries, analytical scan volume, concurrent writers, and required time-travel days. Return `technologies`, `consistency_model`, `physical_layout`, `concurrency_control`, `retention_days`, `vacuum_safety`, `raw_replay_retention`, `graph_projection`, and at least five `validation_metrics`.

Choose graph storage only when traversal depth and relationship-query frequency justify projection cost. A graph choice must still include Delta, a lakehouse, or Snowflake for aggregate scans, and `graph_projection` must explain how results trace to an analytical snapshot. Retention must meet or exceed time travel. Vacuum safety must mention both retained files and active readers or transactions.

Concurrent-writer count must affect conflict or maintenance controls. Raw-source replay retention is a separate requirement from table time travel: vacuum safety does not prove that the source can be reconstructed.

Reject negative depth, scan volume, writer count, or retention and require relationship-query percentage to remain between 0 and 100. Non-finite measurements are invalid rather than a signal to choose a default.

### Example input and expected output

```python
workload = {
    "multi_hop_depth": 4,
    "relationship_queries_pct": 60,
    "aggregate_scan_tb": 12,
    "concurrent_writers": 8,
    "time_travel_days": 14,
}
```

Expected properties:

```python
plan["technologies"]  # contains a graph system and an analytical system
plan["retention_days"] >= 14
bool(plan["concurrency_control"]) is True
plan["graph_projection"]["checkpoint"]  # traces the graph to a source snapshot
len(plan["validation_metrics"]) >= 5
```

For a one-hop workload with 2% relationship queries and very large scans, the technologies should not default to Neo4j.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; defend snapshot retention, concurrent writers, and graph synchronization.

## Unit test

```bash
pytest advanced/02-data-storage/tests -q
```
