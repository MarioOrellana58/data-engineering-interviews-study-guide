# Data Modeling: Slowly Changing Dimensions

## Topic explanation

Slowly changing dimension (SCD) Type 2 preserves attribute history with non-overlapping validity intervals and one current row per business key. The difficult cases are duplicate changes, late-arriving changes, precision boundaries, and facts that must join “as of” event time.

**Analogy:** Slowly changing dimension Type 2 (SCD2) resembles passport history. Issuing a new passport does not erase the previous one; it closes its validity interval. Two passports cannot both be current for one identity.

## Solved practical example

For customer `c1`, changes are Bronze on January 1, Silver on February 1, duplicate Silver on February 15, and Gold on March 1. The solved history is `[Jan 1, Feb 1) Bronze`, `[Feb 1, Mar 1) Silver`, and `[Mar 1, ∞) Gold`. The duplicate state creates no version. Only Gold is current, and a February 10 fact joins Silver.

## Code exercise

Implement `build_scd2(changes)`. Changes may arrive out of order. Collapse identical consecutive states, use half-open intervals `[valid_from, valid_to)`, assign deterministic surrogate keys, and mark exactly one current version per customer.

### Homework contract

Each change contains `customer_id`, effective timestamp `at`, and one or more attributes such as `tier`. Return rows ordered by customer and `valid_from`. Every row contains the original attributes plus `customer_sk`, `valid_from`, `valid_to`, and `is_current`.

Sort changes by business time before constructing history. If consecutive changes have identical attributes, keep one interval rather than manufacturing a version. Close an interval at the next real change using an exclusive `valid_to`. The final interval has `valid_to = None` and is the only current row for that customer. Surrogate keys may be strings or integers, but they must remain identical when input order changes.

Exact duplicate changes at one timestamp are one observation. Different attribute states for the same customer at the same timestamp are ambiguous and must raise `ValueError`; never manufacture a zero-length interval or let input order select a winner.

### Example input and expected output

```python
changes = [
    {"customer_id": "c7", "at": "2026-03-01", "tier": "gold"},
    {"customer_id": "c7", "at": "2026-01-01", "tier": "bronze"},
    {"customer_id": "c7", "at": "2026-02-01", "tier": "bronze"},
]
```

Expected intervals, with implementation-defined deterministic keys:

```python
[
    {
        "customer_id": "c7", "tier": "bronze",
        "valid_from": "2026-01-01", "valid_to": "2026-03-01",
        "is_current": False, "customer_sk": "<stable key 1>",
    },
    {
        "customer_id": "c7", "tier": "gold",
        "valid_from": "2026-03-01", "valid_to": None,
        "is_current": True, "customer_sk": "<stable key 2>",
    },
]
```

The February Bronze record is absorbed because it does not change state.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; explain late-arriving dimensions and the fact-to-dimension as-of join.

## Unit test

```bash
pytest intermediate/04-data-modeling/tests -q
```
