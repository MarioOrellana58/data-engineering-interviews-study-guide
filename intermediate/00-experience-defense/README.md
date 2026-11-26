# Experience Defense: Architecture Deep Dive

## Topic explanation

At senior level, a story must survive a diagram-level investigation. Explain the original constraints, data flow, interfaces, ownership boundaries, failure paths, operational evidence, and evolution over time. Separate facts you measured from assumptions you made.

**Analogy:** Treat the story like an incident flight recorder. The interviewer should be able to reconstruct why each decision occurred, not merely see the polished final architecture.

## Solved practical example

Opening: “I redesigned a Spark pipeline processing 3 terabytes per day (TB/day) whose 95th-percentile completion was 4.2 hours against a two-hour service-level objective (SLO). I owned profiling and the physical redesign. The main issue was a 40x tenant-key skew, so I salted only the three largest tenants and enabled adaptive execution rather than doubling the cluster. The 95th percentile (P95) fell to 71 minutes and compute cost dropped 18%.” A useful question map branches from “40x skew” into measurement, salting correctness, join strategy, cost evidence, and rollback. The answer exposes specific facts instead of claiming generic optimization.

## Code exercise

Complete `homework.md` for one system you personally shipped. Include a Mermaid diagram, capacity calculation, SLO, cost or resource constraint, serious failure, rejected alternative, stakeholder conflict, and your exact contribution. Add a “question map” showing which parts invite deeper Structured Query Language (SQL), Spark, storage, modeling, or DataOps questions.

### Expected deliverable

Use the existing headings and write at least 350 words; 500–700 is usually enough for a useful deep dive. The opening should take about 90 seconds aloud. The remaining sections are the evidence bank for follow-ups. Your diagram must show sources, durable boundaries, processing, publication, and at least one operational control or failure boundary.

Show one capacity calculation with units and assumptions, not only the final number. Connect the service-level objective, cost, failure, and alternative to the same system. State exactly what you did and what teammates did. The automated test checks structure and evidence signals, while the AI review checks consistency and judgment.

### Example input and expected output

Do not reuse these facts as personal experience:

```text
Average: 120 million events/day ÷ 86,400 = 1,389 events/second
Peak assumption: 5× average; headroom: 25%
Provisioned target: 1,389 × 5 × 1.25 = 8,681 events/second
SLO: 60-minute freshness at the 95th percentile
Cost constraint: less than $18,000/month
Failure: sink timeout after commit; recovery checks a batch manifest
Rejected alternative: global cluster resize; only two keys were skewed
My contribution: profiling, salting design, reconciliation, rollout gates
Recovery point objective (RPO): 15 minutes
```

The question map should branch from those claims, for example: “5× peak → source evidence → queue capacity → backpressure → cost.”

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md` for a 20-minute branching interview. Answers must remain consistent with the written facts.

## Unit test

```bash
pytest intermediate/00-experience-defense/tests -q
```
