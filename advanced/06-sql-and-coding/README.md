# SQL and Coding: Reconcile Streams with Constant Memory

## Topic explanation

Large reconciliations often cannot load both sides into memory. If inputs are sorted by key, a merge walk finds missing and mismatched records in linear time and constant auxiliary memory. The implementation must be lazy and must define duplicate-key behavior.

## Practical example and analogy

It is the zipper method: compare the two next teeth, advance the smaller key, and never reopen the part already zipped.

## Code exercise

Implement generator `reconcile_sorted(left, right)`. Inputs are single-pass sorted iterables of `(key, checksum)`. Yield `missing_left`, `missing_right`, or `mismatch` dictionaries in key order. Reject duplicate or descending keys. Do not materialize, sort, or repeatedly scan inputs.

Target complexity: `O(n + m)` time and `O(1)` auxiliary memory.

## AI review

Use `AI_REVIEW_PROMPT.md`; explain iterator exhaustion, lower bounds, and how this becomes a distributed reconciliation.

## Unit test

```bash
pytest advanced/06-sql-and-coding/tests -q
```
