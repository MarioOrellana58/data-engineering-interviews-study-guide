# Experience Defense: Architecture Deep Dive

## Topic explanation

At senior level, a story must survive a diagram-level investigation. Explain the original constraints, data flow, interfaces, ownership boundaries, failure paths, operational evidence, and evolution over time. Separate facts you measured from assumptions you made.

## Practical example and analogy

Treat the story like an incident flight recorder. The interviewer should be able to reconstruct why each decision occurred, not merely hear the polished final architecture.

## Code exercise

Complete `homework.md` for one system you personally shipped. Include a Mermaid diagram, capacity calculation, SLO, cost or resource constraint, serious failure, rejected alternative, stakeholder conflict, and your exact contribution. Add a “question map” showing which parts invite deeper SQL, Spark, storage, modeling, or DataOps questions.

## AI review

Use `AI_REVIEW_PROMPT.md` for a 20-minute branching interview. Answers must remain consistent with the written facts.

## Unit test

```bash
pytest intermediate/00-experience-defense/tests -q
```
