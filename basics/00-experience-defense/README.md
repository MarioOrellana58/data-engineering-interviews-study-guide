# Experience Defense: Evidence Before Adjectives

## Topic explanation

Senior interviews begin with experience because one real project can reveal architecture, coding, operations, and leadership depth. Build one story around **context, personal ownership, decisions, measurable results, and reflection**. Replace “large” and “fast” with volumes, latency, cost, users, or incident rates.

## Practical example and analogy

A project story is an API: the opening gives a small stable interface; interviewer questions request deeper fields. Do not return the entire database in the first response.

Use this 90-second shape: problem → scale → your decision → hardest trade-off → result. Keep implementation, failure, and stakeholder details available for follow-ups.

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
