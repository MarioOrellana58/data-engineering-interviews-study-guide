# Data Architecture: Requirements Drive Boxes

## Topic explanation

Architecture begins with workload and guarantees, not a favorite service. Establish volume, velocity, consumers, freshness, correctness, retention, security, recovery objectives, team skills, and budget. Separate ingestion, durable storage, transformation, serving, and control-plane concerns.

```mermaid
flowchart LR
    S[Sources] --> I[Idempotent ingestion]
    I --> R[(Immutable raw data)]
    R --> T[Validated transforms]
    T --> C[(Curated models)]
    C --> A[Analytics / ML / APIs]
    Q[Quality + lineage] -. observes .-> I
    Q -. observes .-> T
```

## Practical example and analogy

Designing a pipeline is like designing a water system. Pipe diameter is throughput, tanks provide buffering, filters enforce quality, and meters provide observability. Adding pumps before knowing demand creates cost without reliability.

## Code exercise

Implement `design_pipeline(requirements)` in `homework.py`. Return a plan containing layers, delivery mode, partition key, recovery strategy, RPO/RTO, and explicit assumptions. It must react to freshness, replay, PII, and daily-volume constraints rather than return one static architecture.

Stretch: explain when your batch design should become streaming and why micro-batch may still win.

## AI review

Use `AI_REVIEW_PROMPT.md`. Be ready to defend one rejected architecture and estimate peak throughput.

## Unit test

```bash
pytest basics/01-data-architecture/tests -q
```
