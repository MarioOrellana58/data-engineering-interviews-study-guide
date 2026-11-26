# Experience Defense: Adversarial Senior Loop

## Topic explanation

The strongest answer remains precise when challenged. A senior candidate acknowledges uncertainty, separates team outcomes from personal work, and can revise a decision without becoming defensive. Prepare for contradictions: lower latency versus lower cost, strict correctness versus availability, and delivery speed versus platform health.

**Analogy:** This is a load test for reasoning. The goal is not to claim that no crack exists; it is to expose limits honestly and show how the system degrades safely.

## Solved practical example

Challenge: “You said exactly-once, but your Amazon Simple Storage Service (S3) sink cannot join the Kafka transaction. Was it actually exactly-once?” Strong answer: “Not end-to-end. Kafka-to-Delta provided an effectively exactly-once result because the batch identifier (ID) and offset range were committed with the Delta transaction. The raw S3 audit copy was at-least-once and deduplicated downstream. I should call the business result exactly-once, not every write. During a timeout we verified the Delta commit by batch ID before retrying.” This correction improves credibility because it narrows the guarantee precisely.

## Code exercise

Complete `homework.md` with three project stories: architecture, incident, and leadership. Each must include metrics, personal ownership, a mistake or changed opinion, and one question you hope the interviewer asks. Add a consistency matrix so shared facts—scale, dates, tools, and responsibilities—do not change between stories.

### Expected deliverable

Keep the existing three-story headings and write at least 700 words total; 900–1,300 gives enough evidence for an adversarial loop without becoming a memoir. Each story should follow Situation, Task, Action, Result (STAR), but the Action section must distinguish your decisions from team work. Include at least 12 quantified facts across the bank and an explicit “mistake” or changed opinion in every story.

The consistency matrix needs one row per shared fact and one column per story. Reuse a value only when the stories concern the same system; otherwise mark it “not applicable” rather than forcing false consistency. End with questions that invite technical depth you can actually defend.

### Example input and expected output

These fictional facts demonstrate structure only:

| Fact | Architecture | Incident | Leadership |
|---|---|---|---|
| Platform | Payments lakehouse | Same platform | Contract migration for same platform |
| Scale | 2 billion events/day | 14 million replayed | 5 producer teams |
| Role | Target-design owner | Incident commander | Cross-team technical lead |
| Recovery target | 15-minute recovery point objective (RPO) | 42-minute restoration | Replayable adapters |
| Mistake | Synchronous control-plane dependency | Forecast before measuring replay | Labeled domain variation as debt |

An architecture story should invite capacity and failure-domain questions; an incident story should invite timeline, evidence, and recovery questions; a leadership story should invite conflict, influence, and outcome questions. Never present the reference stories as your own experience.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md` for a 30-minute hostile-but-fair loop. The AI must introduce new constraints and detect contradictions without inventing facts.

## Unit test

```bash
pytest advanced/00-experience-defense/tests -q
```
