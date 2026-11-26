# Structured Query Language (SQL) and Coding: Sessionization and Funnels

## Topic explanation

Advanced analytical SQL combines temporal reasoning, windows, and exact grain control. Sessionization requires a boundary definition and deterministic ordering. Funnel logic must decide whether steps are ordered, repeatable, and limited to one session.

**Analogy:** A session is a chapter separated by enough silence. A funnel is an ordered set of plot points; reading the ending before the beginning does not complete the story.

## Solved practical example

Events at 10:00 `view`, 10:05 `add`, 10:10 `purchase`, and 10:41 `view` form two sessions under a “more than 30 minutes” rule. The first completes the funnel in 600 seconds; the second does not. A common solution marks a boundary with `LAG(event_at)`, cumulatively sums the boundary flag into a session number, then evaluates ordered funnel timestamps within each session.

## Code exercise

Complete `homework.sql`. A new session begins after more than 30 minutes of inactivity. Return one row per user and session with start/end time, event count, whether `view → add_to_cart → purchase` occurred in order, and seconds from first view to qualifying purchase. Duplicate `event_id` rows must be reduced to the latest `ingested_at` first.

### Homework contract

Produce exactly these columns in order: `user_id`, `session_number`, `session_start`, `session_end`, `event_count`, `completed_funnel`, and `seconds_to_purchase`. Deduplicate before sessionization. Order events deterministically by `event_at` and `event_id`. The first session for each user is 1; a gap of exactly 30 minutes remains in the same session, while a gap greater than 30 minutes starts another.

A funnel completes only when a view is followed by an add-to-cart and then a purchase in the same session. A purchase that occurs first does not count. `seconds_to_purchase` is measured from the qualifying view to the qualifying purchase and is `NULL` when the funnel is incomplete.

### Example input and expected output

| user_id | event_name | event_at |
|---|---|---|
| u9 | view | 10:00 |
| u9 | add_to_cart | 10:04 |
| u9 | purchase | 10:09 |
| u9 | view | 10:40 |

Expected rows:

| user_id | session_number | session_start | session_end | event_count | completed_funnel | seconds_to_purchase |
|---|---:|---|---|---:|---|---:|
| u9 | 1 | 10:00 | 10:09 | 3 | true | 540 |
| u9 | 2 | 10:40 | 10:40 | 1 | false | NULL |

The fixture also includes duplicate event identifiers and reversed funnel steps, so a row-count-only solution is insufficient.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; discuss sort cost, boundary semantics, and scaling by date partitions.

## Unit test

```bash
pytest intermediate/06-sql-and-coding/tests -q
```
