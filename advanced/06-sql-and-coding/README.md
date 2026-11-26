# Structured Query Language (SQL) and Coding: Reconcile Streams with Constant Memory

## Topic explanation

Large reconciliations often cannot load both sides into memory. If inputs are sorted by key, a merge walk finds missing and mismatched records in linear time and constant auxiliary memory. The implementation must be lazy and must define duplicate-key behavior.

**Analogy:** This is the zipper method: compare the next teeth, advance the smaller key, and never reopen the part already zipped.

## Solved practical example

For left `[(a,1),(b,2),(d,4)]` and right `[(b,X),(c,3),(d,4)]`: `a` is `missing_right`; `b` is a checksum `mismatch`; `c` is `missing_left`; and `d` matches, so emit nothing. Each iterator advances at most once per record. Only the two current records are held, giving `O(n+m)` time and `O(1)` auxiliary memory.

## Code exercise

Implement generator `reconcile_sorted(left, right)`. Inputs are single-pass sorted iterables of `(key, checksum)`. Yield `missing_left`, `missing_right`, or `mismatch` dictionaries in key order. Reject duplicate or descending keys. Do not materialize, sort, or repeatedly scan inputs.

Target complexity: `O(n + m)` time and `O(1)` auxiliary memory.

### Homework contract

The function is a generator: it must not read either iterable twice or convert it to a list. Inputs contain unique keys in strictly ascending order. Validate that order while consuming, including after the other side is exhausted. Raise `ValueError` for a duplicate or descending key.

For equal keys, emit a row only when checksums differ. For a key present on one side, emit the appropriate missing status. Every yielded dictionary has `key`, `status`, `left_checksum`, and `right_checksum`, using `None` for the absent side. Output naturally remains sorted because the merge always advances the smaller key.

### Example input and expected output

```python
left = [("a", "11"), ("c", "33")]
right = [("b", "22"), ("c", "XX"), ("d", "44")]
list(reconcile_sorted(left, right))
```

Expected output:

```python
[
    {"key": "a", "status": "missing_right", "left_checksum": "11", "right_checksum": None},
    {"key": "b", "status": "missing_left", "left_checksum": None, "right_checksum": "22"},
    {"key": "c", "status": "mismatch", "left_checksum": "33", "right_checksum": "XX"},
    {"key": "d", "status": "missing_left", "left_checksum": None, "right_checksum": "44"},
]
```

Matching checksums produce no row because reconciliation reports differences only.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; explain iterator exhaustion, lower bounds, and how this becomes a distributed reconciliation.

## Unit test

```bash
pytest advanced/06-sql-and-coding/tests -q
```
