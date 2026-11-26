# Data Modeling: Slowly Changing Dimensions

## Topic explanation

SCD Type 2 preserves attribute history with non-overlapping validity intervals and one current row per business key. The difficult cases are duplicate changes, late-arriving changes, precision boundaries, and facts that must join “as of” event time.

## Practical example and analogy

SCD2 is a passport history. Issuing a new passport does not erase the previous one; it closes its validity interval. Two passports cannot both be current for the same identity.

## Code exercise

Implement `build_scd2(changes)`. Changes may arrive out of order. Collapse identical consecutive states, use half-open intervals `[valid_from, valid_to)`, assign deterministic surrogate keys, and mark exactly one current version per customer.

## AI review

Use `AI_REVIEW_PROMPT.md`; explain late-arriving dimensions and the fact-to-dimension as-of join.

## Unit test

```bash
pytest intermediate/04-data-modeling/tests -q
```
