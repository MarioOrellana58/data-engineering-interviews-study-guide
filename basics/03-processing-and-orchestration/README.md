# Processing and Orchestration: Safe to Run Twice

## Topic explanation

An ETL task is production-ready when retries do not corrupt results. Prefer deterministic transformations, stable business keys, checkpoints outside ephemeral workers, atomic publication, and explicit handling for malformed records. An orchestrator coordinates work; it should not hide business logic inside a DAG file.

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant T as Transform
    participant S as Staging
    participant P as Published table
    O->>T: run(batch_id)
    T->>S: write/replace batch_id
    T->>S: validate
    S->>P: atomic merge
    O->>T: retry same batch_id
    T-->>P: same final state
```

## Practical example and analogy

Idempotency is an elevator button: pressing it repeatedly should not summon multiple elevators. A retry is normal control flow, not an exceptional business event.

## Code exercise

Implement `process_events(existing, incoming)`. Deduplicate by `event_id`, keep the record with the newest `updated_at`, reject invalid amounts, normalize currency casing, and return deterministic output. Reprocessing the same input must not change the result.

## AI review

Use `AI_REVIEW_PROMPT.md`; expect questions about partial writes, retries, backfills, and task boundaries.

## Unit test

```bash
pytest basics/03-processing-and-orchestration/tests -q
```
