# SQL and Coding: Correct Under Messy Semantics

## Topic explanation

Senior SQL work starts by defining row grain, duplicate policy, `NULL` behavior, tie-breaking, and filtering order. Window functions preserve row context; aggregation collapses it. Query correctness includes deterministic output and resistance to duplicate source events.

**Analogy:** A SQL query is a legal argument: the result is only as sound as the definitions used for evidence. If “latest” has no tie-breaker, the verdict is nondeterministic.

## Solved practical example

To keep the newest version of each order, rank events before aggregation:

```sql
SELECT * EXCLUDE rn
FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY order_id ORDER BY updated_at DESC, ingested_at DESC
  ) AS rn
  FROM order_events
)
WHERE rn = 1;
```

For two versions tied on `updated_at`, the later `ingested_at` wins. Filtering cancellations happens **after** this step, because an old paid version must not survive a newer cancellation.

## Code exercise

Complete `homework.sql`. From `order_events`, keep the latest event per `order_id`; exclude orders whose latest state is `cancelled`; then return one row per customer with:

`customer_id, order_count, gross_revenue, last_order_at, revenue_rank`.

Rank customers by revenue descending using dense rank. Break event-version ties by `ingested_at`. Preserve customers with zero valid orders using the `customers` table.

## AI review

Use `AI_REVIEW_PROMPT.md`; explain logical query order and the cost of each window/sort.

## Unit test

```bash
pytest basics/06-sql-and-coding/tests -q
```
