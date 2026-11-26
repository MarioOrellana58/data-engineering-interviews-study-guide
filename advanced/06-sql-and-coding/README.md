# SQL and Coding: Reconcile Streams with Constant Memory

## Topic explanation

Large reconciliations often cannot load both sides into memory. If inputs are sorted by key, a merge walk finds missing and mismatched records in linear time and constant auxiliary memory. The implementation must be lazy and must define duplicate-key behavior.

**Analogy:** This is the zipper method: compare the next teeth, advance the smaller key, and never reopen the part already zipped.

## Solved practical example

For left `[(a,1),(b,2),(d,4)]` and right `[(b,X),(c,3),(d,4)]`: `a` is `missing_right`; `b` is a checksum `mismatch`; `c` is `missing_left`; and `d` matches, so emit nothing. Each iterator advances at most once per record. Only the two current records are held, giving `O(n+m)` time and `O(1)` auxiliary memory.

## Code exercise

Implement generator `reconcile_sorted(left, right)`. Inputs are single-pass sorted iterables of `(key, checksum)`. Yield `missing_left`, `missing_right`, or `mismatch` dictionaries in key order. Reject duplicate or descending keys. Do not materialize, sort, or repeatedly scan inputs.

Target complexity: `O(n + m)` time and `O(1)` auxiliary memory.

## AI review

Use `AI_REVIEW_PROMPT.md`; explain iterator exhaustion, lower bounds, and how this becomes a distributed reconciliation.

## Unit test

```bash
pytest advanced/06-sql-and-coding/tests -q
```
