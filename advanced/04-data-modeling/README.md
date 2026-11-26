# Data Modeling: Bitemporal Truth

## Topic explanation

Valid time answers “when was this true in the business?” System time answers “when did we know it?” Bitemporal models preserve both, allowing reproducible reports after late corrections. Updates close system-time versions without rewriting history.

## Practical example and analogy

A weather diary records that Monday was rainy; a correction entered Friday says the Monday sensor was wrong. Business time is Monday. Knowledge time is Friday. Both facts matter when explaining a report generated Tuesday.

## Code exercise

Implement `build_bitemporal(changes)` and `as_of(rows, entity_id, valid_at, known_at)`. Changes contain `effective_at`, `recorded_at`, and attributes. Preserve corrections, use half-open intervals in both time axes, and return exactly what was believed at the requested system time.

## AI review

Use `AI_REVIEW_PROMPT.md`; defend storage growth, correction semantics, and indexing/clustering.

## Unit test

```bash
pytest advanced/04-data-modeling/tests -q
```
