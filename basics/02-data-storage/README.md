# Data Storage: Match the Access Pattern

## Topic explanation

Storage choices trade latency, consistency, query flexibility, write rate, operational effort, and cost. Row stores favor selective transactional access; columnar files and warehouses favor scans and aggregation; key-value stores favor known keys; document stores favor evolving aggregates. Parquet row groups, compression, partitioning, and statistics matter as much as file extension.

**Analogy:** A warehouse, filing cabinet, and vending machine all store items differently. The warehouse favors bulk movement, the cabinet flexible lookup, and the vending machine extremely fast retrieval of known choices.

## Solved practical example

For append-only clickstream data scanned by date and aggregated across millions of rows, choose Parquet or Delta, partitioned by `event_date`, with 256–512 MB files. Do **not** partition by `customer_id`: 50 million customers would create excessive directories and tiny files. A query for January 2–3 then scans only those two date partitions; customer filtering uses file statistics or clustering inside them.

## Code exercise

Implement `choose_storage(workload)` and `files_to_scan(partitions, predicate)`.

- Explain each choice with two workload facts.
- Prune partitions safely for inclusive date ranges.
- Never use high-cardinality customer IDs as a lake partition merely because queries filter by customer.

Stretch: describe compaction and the small-file problem in `rationale`.

## AI review

Use `AI_REVIEW_PROMPT.md` to challenge consistency, cost, and partition evolution.

## Unit test

```bash
pytest basics/02-data-storage/tests -q
```
