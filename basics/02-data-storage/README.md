# Data Storage: Match the Access Pattern

## Topic explanation

Storage choices trade latency, consistency, query flexibility, write rate, operational effort, and cost. Row stores favor selective transactional access; columnar files and warehouses favor scans and aggregation; key-value stores favor known keys; document stores favor evolving aggregates. Parquet row groups, compression, partitioning, and statistics matter as much as file extension.

**Analogy:** A warehouse, filing cabinet, and vending machine all store items differently. The warehouse favors bulk movement, the cabinet flexible lookup, and the vending machine extremely fast retrieval of known choices.

## Solved practical example

For append-only clickstream data scanned by date and aggregated across millions of rows, choose Parquet or Delta, partitioned by `event_date`, with 256–512 megabyte (MB) files. Do **not** partition by `customer_id`: 50 million customers would create excessive directories and tiny files. A query for January 2–3 then scans only those two date partitions; customer filtering uses file statistics or clustering inside them.

## Code exercise

Implement `choose_storage(workload)` and `files_to_scan(partitions, start, end)`.

- Explain each choice with two workload facts.
- Prune partitions safely for inclusive date ranges.
- Never use high-cardinality customer identifiers (IDs) as a lake partition merely because queries filter by customer.

Stretch: describe compaction and the small-file problem in `rationale`.

### Homework contract

`choose_storage` receives Boolean workload signals such as `point_reads`, `transactions`, and `large_scans`, plus a schema-change rate. Return a dictionary with `technology`, `format`, and at least two workload-specific `reasons`. A transactional point-read workload should choose a relational row store; an analytical scan should choose a columnar format. Do not return the same unexplained choice for every input.

For analytical scans, the schema-change rate must affect the choice or rationale: a stable append-only dataset can use plain Parquet, while frequent controlled evolution may justify a transactional table format such as Delta.

`files_to_scan` receives partition dictionaries containing a `path` and a Python `date`. Return only paths whose dates fall in the inclusive interval `[start, end]`, ordered by date and then path. Do not mutate or rely on the input order. Raise `ValueError` when `start` is after `end`.

### Example input and expected output

```python
from datetime import date

choice = choose_storage({
    "point_reads": False,
    "transactions": False,
    "large_scans": True,
    "schema_changes": "medium",
})
# choice["format"] is "Parquet", "Delta", or "Iceberg"
# choice["reasons"] explains columnar scans and the workload

files_to_scan(
    [
        {"path": "d=2026-02-02/a.parquet", "date": date(2026, 2, 2)},
        {"path": "d=2026-02-01/a.parquet", "date": date(2026, 2, 1)},
        {"path": "d=2026-02-03/a.parquet", "date": date(2026, 2, 3)},
    ],
    date(2026, 2, 1),
    date(2026, 2, 2),
)
# ["d=2026-02-01/a.parquet", "d=2026-02-02/a.parquet"]
```

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md` to challenge consistency, cost, and partition evolution.

## Unit test

```bash
pytest basics/02-data-storage/tests -q
```
