# Data Storage: Match the Access Pattern

## Topic explanation

Storage choices trade latency, consistency, query flexibility, write rate, operational effort, and cost. Row stores favor selective transactional access; columnar files and warehouses favor scans and aggregation; key-value stores favor known keys; document stores favor evolving aggregates. Parquet row groups, compression, partitioning, and statistics matter as much as file extension.

## Practical example and analogy

A warehouse, filing cabinet, and vending machine all store things. A warehouse is efficient for bulk movement, a filing cabinet supports flexible lookup, and a vending machine makes a small set of items extremely fast to retrieve. Asking for “the best storage” without an access pattern is meaningless.

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
