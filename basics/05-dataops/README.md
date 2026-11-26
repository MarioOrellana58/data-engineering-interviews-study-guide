# DataOps: Turn Assumptions into Gates

## Topic explanation

Data quality is executable knowledge. Contracts define schema and meaning; checks cover completeness, uniqueness, validity, freshness, and referential integrity. A useful gate reports evidence, quarantines bad rows when safe, and stops publication when trust would be damaged.

**Analogy:** Data tests are airport security, not a decorative dashboard. Some items can be quarantined; others require closing the gate because allowing them through compromises the whole flight.

## Solved practical example

A three-row batch contains one valid row, one duplicate identifier (ID), and one null amount. The contract allows at most 10% rejection. The gate accepts one, quarantines two with `duplicate_id` and `required_null`, reports a 66.7% rejection rate, and sets `publish=false`. Silently dropping two rows would make the downstream total look valid while being wrong.

## Code exercise

Implement `validate_batch(rows, contract, now)`. Return accepted rows, rejected rows with reason codes, and metrics. Reject duplicate IDs and invalid/null required fields. Fail the entire batch when rejection rate exceeds the contract threshold or freshness is violated. Do not silently coerce bad values.

### Homework contract

The contract contains `required`, `unique`, `max_age_minutes`, and `max_reject_rate`. Validate rows in input order without mutating them. A null required value is missing. Accept the first valid occurrence of a unique key and reject later occurrences. Each rejected row needs a nonempty `reason`.

Return `accepted`, `rejected`, `publish`, and `metrics`. Metrics must include input and rejection evidence plus `freshness_minutes`, computed from `now` and the newest accepted event. Publication is allowed only when there is usable input, reject rate is within the threshold, and freshness is within the contract.

Require timezone-aware `now` and event timestamps, reject future events, and require `amount` to be a finite nonnegative number (a Boolean is not an amount). `max_age_minutes` must be nonnegative and `max_reject_rate` must be between 0 and 1 inclusive.

### Example input and expected output

```python
from datetime import datetime, timezone

contract = {
    "required": ["id", "amount", "event_at"],
    "unique": "id",
    "max_age_minutes": 30,
    "max_reject_rate": 0.25,
}
rows = [
    {"id": "a", "amount": 4, "event_at": "2026-02-01T11:50:00+00:00"},
    {"id": "b", "amount": None, "event_at": "2026-02-01T11:55:00+00:00"},
]
result = validate_batch(rows, contract, datetime(2026, 2, 1, 12, 0, tzinfo=timezone.utc))
```

Expected properties are one accepted row, one rejected row with a reason, `reject_rate == 0.5`, `freshness_minutes == 10`, and `publish is False` because the rejection threshold was exceeded.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; defend thresholds, alert ownership, and what happens after a failed gate.

## Unit test

```bash
pytest basics/05-dataops/tests -q
```
