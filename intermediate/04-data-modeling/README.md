# Data Modeling: Slowly Changing Dimensions

## Topic explanation

Slowly changing dimension (SCD) Type 2 preserves attribute history with non-overlapping validity intervals and one current row per business key. The difficult cases are duplicate changes, late-arriving changes, precision boundaries, and facts that must join “as of” event time.

**Analogy:** Slowly changing dimension Type 2 (SCD2) resembles passport history. Issuing a new passport does not erase the previous one; it closes its validity interval. Two passports cannot both be current for one identity.

## Solved practical example

For customer `c1`, changes are Bronze on January 1, Silver on February 1, duplicate Silver on February 15, and Gold on March 1. The solved history is `[Jan 1, Feb 1) Bronze`, `[Feb 1, Mar 1) Silver`, and `[Mar 1, ∞) Gold`. The duplicate state creates no version. Only Gold is current, and a February 10 fact joins Silver.

## Code exercise

Implement `build_scd2(changes)`. Changes may arrive out of order. Collapse identical consecutive states, use half-open intervals `[valid_from, valid_to)`, assign deterministic surrogate keys, and mark exactly one current version per customer.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; explain late-arriving dimensions and the fact-to-dimension as-of join.

## Unit test

```bash
pytest intermediate/04-data-modeling/tests -q
```
