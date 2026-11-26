# Experience Defense: Architecture Deep Dive

## Topic explanation

At senior level, a story must survive a diagram-level investigation. Explain the original constraints, data flow, interfaces, ownership boundaries, failure paths, operational evidence, and evolution over time. Separate facts you measured from assumptions you made.

**Analogy:** Treat the story like an incident flight recorder. The interviewer should be able to reconstruct why each decision occurred, not merely see the polished final architecture.

## Solved practical example

Opening: “I redesigned a 3 TB/day Spark pipeline whose 95th-percentile completion was 4.2 hours against a two-hour SLO. I owned profiling and the physical redesign. The main issue was a 40x tenant-key skew, so I salted only the three largest tenants and enabled adaptive execution rather than doubling the cluster. P95 fell to 71 minutes and compute cost dropped 18%.” A useful question map branches from “40x skew” into measurement, salting correctness, join strategy, cost evidence, and rollback. The answer exposes specific facts instead of claiming generic optimization.

## Code exercise

Complete `homework.md` for one system you personally shipped. Include a Mermaid diagram, capacity calculation, SLO, cost or resource constraint, serious failure, rejected alternative, stakeholder conflict, and your exact contribution. Add a “question map” showing which parts invite deeper SQL, Spark, storage, modeling, or DataOps questions.

## AI review

Use `AI_REVIEW_PROMPT.md` for a 20-minute branching interview. Answers must remain consistent with the written facts.

## Unit test

```bash
pytest intermediate/00-experience-defense/tests -q
```
