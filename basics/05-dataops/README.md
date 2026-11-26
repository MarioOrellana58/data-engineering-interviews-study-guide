# DataOps: Turn Assumptions into Gates

## Topic explanation

Data quality is executable knowledge. Contracts define schema and meaning; checks cover completeness, uniqueness, validity, freshness, and referential integrity. A useful gate reports evidence, quarantines bad rows when safe, and stops publication when trust would be damaged.

## Practical example and analogy

Data tests are airport security, not a decorative dashboard. Some items are harmless enough to quarantine; others require closing the gate because letting them through compromises the whole flight.

## Code exercise

Implement `validate_batch(rows, contract, now)`. Return accepted rows, rejected rows with reason codes, and metrics. Reject duplicate IDs and invalid/null required fields. Fail the entire batch when rejection rate exceeds the contract threshold or freshness is violated. Do not silently coerce bad values.

## AI review

Use `AI_REVIEW_PROMPT.md`; defend thresholds, alert ownership, and what happens after a failed gate.

## Unit test

```bash
pytest basics/05-dataops/tests -q
```
