# Data Modeling: Bitemporal Truth

## Topic explanation

Valid time answers “when was this true in the business?” System time, also called transaction time, answers “when did the database record this version?” It approximates when the system knew something, but not necessarily when a person or organization first learned it. Bitemporal models preserve both timelines, allowing reproducible reports after late corrections. Updates close system-time versions without rewriting history.

**Analogy:** A weather diary says Monday was rainy; a correction entered Friday says the sensor was wrong. Business time is Monday, while knowledge time is Friday. Both matter when reproducing Tuesday's report.

## Solved practical example

On January 2 the system records that customer A was Silver from January 1. On March 1 it learns a correction: A was Bronze from January 15. Querying business date January 20 with knowledge date February 15 returns Silver; the same business date with knowledge date March 2 returns Bronze. The correction closes a system-time interval—it does not overwrite what February's report actually knew.

## Code exercise

Implement `build_bitemporal(changes)` and `as_of(rows, entity_id, valid_at, known_at)`. Changes contain `effective_at`, `recorded_at`, and attributes. Preserve corrections, use half-open intervals in both time axes, and return exactly what was believed at the requested system time.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; defend storage growth, correction semantics, and indexing/clustering.

## Unit test

```bash
pytest advanced/04-data-modeling/tests -q
```
