# Experience Defense: Evidence Before Adjectives

## Topic explanation

Senior interviews begin with experience because one real project can reveal architecture, coding, operations, and leadership depth. Build one story around **context, personal ownership, decisions, measurable results, and reflection**. Replace “large” and “fast” with volumes, latency, cost, users, or incident rates.

**Analogy:** A project story is an API: the opening returns a small, stable interface; follow-up questions request deeper fields. Returning the entire database in the first response hides the useful signal.

## Solved practical example

> “I owned the ingestion redesign for 18 partners producing 220 million events per day. Daily files made data 14 hours late, so I introduced hourly, idempotent loads into partitioned object storage instead of Kafka; the business needed 90-minute freshness, not seconds, and the team could operate batch reliably. I added source checksums and replay by batch ID. Freshness fell to 42 minutes and failed-load recovery from four hours to 25 minutes. My first partition key was too granular and created small files; I corrected it with daily partitions and compaction.”

Why it works: it states ownership, scale, a decision, rejected complexity, measurable results, and a mistake. Deeper implementation details remain available for follow-ups.

## Code exercise

Complete `homework.md` about one production data project. Include:

- your individual ownership and two decisions;
- at least three quantified facts;
- one failure and its detection/recovery;
- one rejected alternative and why;
- what you would change now.

Then deliver it aloud in 90 seconds and answer five minutes of follow-ups without inventing facts.

## AI review

Use `AI_REVIEW_PROMPT.md` after the structural test passes. The AI should behave as a skeptical senior interviewer, not a copy editor.

## Unit test

```bash
pytest basics/00-experience-defense/tests -q
```

The test checks structure and evidence signals. It cannot verify truthfulness or senior judgment; the oral review does that.
