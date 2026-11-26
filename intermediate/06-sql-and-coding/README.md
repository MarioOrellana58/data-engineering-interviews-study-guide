# Structured Query Language (SQL) and Coding: Sessionization and Funnels

## Topic explanation

Advanced analytical SQL combines temporal reasoning, windows, and exact grain control. Sessionization requires a boundary definition and deterministic ordering. Funnel logic must decide whether steps are ordered, repeatable, and limited to one session.

**Analogy:** A session is a chapter separated by enough silence. A funnel is an ordered set of plot points; reading the ending before the beginning does not complete the story.

## Solved practical example

Events at 10:00 `view`, 10:05 `add`, 10:10 `purchase`, and 10:41 `view` form two sessions under a “more than 30 minutes” rule. The first completes the funnel in 600 seconds; the second does not. A common solution marks a boundary with `LAG(event_at)`, cumulatively sums the boundary flag into a session number, then evaluates ordered funnel timestamps within each session.

## Code exercise

Complete `homework.sql`. A new session begins after more than 30 minutes of inactivity. Return one row per user and session with start/end time, event count, whether `view → add_to_cart → purchase` occurred in order, and seconds from first view to qualifying purchase. Duplicate `event_id` rows must be reduced to the latest `ingested_at` first.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; discuss sort cost, boundary semantics, and scaling by date partitions.

## Unit test

```bash
pytest intermediate/06-sql-and-coding/tests -q
```
