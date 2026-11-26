# Experience Defense: Adversarial Senior Loop

## Topic explanation

The strongest answer remains precise when challenged. A senior candidate acknowledges uncertainty, separates team outcomes from personal work, and can revise a decision without becoming defensive. Prepare for contradictions: lower latency versus lower cost, strict correctness versus availability, and delivery speed versus platform health.

**Analogy:** This is a load test for reasoning. The goal is not to claim that no crack exists; it is to expose limits honestly and show how the system degrades safely.

## Solved practical example

Challenge: “You said exactly-once, but your S3 sink cannot join the Kafka transaction. Was it actually exactly-once?” Strong answer: “Not end-to-end. Kafka-to-Delta was effectively once because the batch ID and offset range were committed with the Delta transaction. The raw S3 audit copy was at-least-once and deduplicated downstream. I should call the business result exactly-once, not every write. During a timeout we verified the Delta commit by batch ID before retrying.” This correction improves credibility because it narrows the guarantee precisely.

## Code exercise

Complete `homework.md` with three project stories: architecture, incident, and leadership. Each must include metrics, personal ownership, a mistake or changed opinion, and one question you hope the interviewer asks. Add a consistency matrix so shared facts—scale, dates, tools, and responsibilities—do not change between stories.

## AI review

Use `AI_REVIEW_PROMPT.md` for a 30-minute hostile-but-fair loop. The AI must introduce new constraints and detect contradictions without inventing facts.

## Unit test

```bash
pytest advanced/00-experience-defense/tests -q
```
