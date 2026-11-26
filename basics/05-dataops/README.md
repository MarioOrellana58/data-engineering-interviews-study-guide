# DataOps: Turn Assumptions into Gates

## Topic explanation

Data quality is executable knowledge. Contracts define schema and meaning; checks cover completeness, uniqueness, validity, freshness, and referential integrity. A useful gate reports evidence, quarantines bad rows when safe, and stops publication when trust would be damaged.

**Analogy:** Data tests are airport security, not a decorative dashboard. Some items can be quarantined; others require closing the gate because allowing them through compromises the whole flight.

## Solved practical example

A three-row batch contains one valid row, one duplicate ID, and one null amount. The contract allows at most 10% rejection. The gate accepts one, quarantines two with `duplicate_id` and `required_null`, reports a 66.7% rejection rate, and sets `publish=false`. Silently dropping two rows would make the downstream total look valid while being wrong.

## Code exercise

Implement `validate_batch(rows, contract, now)`. Return accepted rows, rejected rows with reason codes, and metrics. Reject duplicate IDs and invalid/null required fields. Fail the entire batch when rejection rate exceeds the contract threshold or freshness is violated. Do not silently coerce bad values.

## AI review

Use `AI_REVIEW_PROMPT.md`; defend thresholds, alert ownership, and what happens after a failed gate.

## Unit test

```bash
pytest basics/05-dataops/tests -q
```
