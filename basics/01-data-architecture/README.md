# Data Architecture: Requirements Drive Boxes

## Topic explanation

Architecture begins with workload and guarantees, not a favorite service. Establish volume, velocity, consumers, freshness, correctness, retention, security, recovery objectives, team skills, and budget. Separate ingestion, durable storage, transformation, serving, and control-plane concerns.

**Analogy:** A data platform resembles a water system: pipe diameter is throughput, tanks provide buffering, filters enforce quality, and meters provide observability. Pumps chosen before demand is known add cost without reliability.

```mermaid
flowchart LR
    S[Sources] --> I[Idempotent ingestion]
    I --> R[(Immutable raw data)]
    R --> T[Validated transforms]
    T --> C[(Curated models)]
    C --> A[Analytics / machine learning (ML) / APIs]
    Q[Quality + lineage] -. observes .-> I
    Q -. observes .-> T
```

## Solved practical example

Given 400 gigabytes per day (GB/day), six-hour freshness, seven-year retention, replay requirements, and no personally identifiable information (PII), a suitable answer is: hourly batch ingestion → immutable object-storage raw layer partitioned by ingestion date → validated columnar transformations → curated warehouse tables. Keep batch manifests and checksums for replay and compact small files daily. Freshness does not determine disaster-recovery targets: ask the business separately how much data it can lose and how quickly service must return. If it specifies a six-hour recovery point objective (RPO) and four-hour recovery time objective (RTO), design checkpoints and restoration procedures to meet those values. Streaming is unjustified because the normal freshness requirement is hours, not seconds.

## Code exercise

Implement `design_pipeline(requirements)` in `homework.py`. Return a plan containing layers, delivery mode, partition key, recovery strategy, RPO/RTO, and explicit assumptions. It must react to freshness, replay, PII, and daily-volume constraints rather than return one static architecture.

Stretch: explain when your batch design should become streaming and why micro-batch may still win.

### Homework contract

`requirements` is a dictionary containing `daily_gb`, `freshness_minutes`, `replay`, and `pii`. Return a new dictionary; do not mutate the input. At minimum, the result must contain:

- `delivery_mode`: `batch`, `micro-batch`, or `streaming`, chosen from freshness rather than hard-coded;
- `layers`: a list that includes a durable raw layer;
- `partition_key`: a nonempty physical partition choice;
- `recovery`: a human-readable replay or restoration strategy;
- `rpo_minutes` and `rto_minutes`: numeric proposals consistent with the requested service;
- `security_controls`: a list that becomes stronger when `pii` is true;
- `assumptions`: at least two explicit facts you would confirm with stakeholders.

Reject nonsensical values such as nonpositive freshness. You may return additional fields when they help explain the design.

### Example input and expected output

```python
requirements = {
    "daily_gb": 50,
    "freshness_minutes": 30,
    "replay": True,
    "pii": True,
}
```

One acceptable result shape is:

```python
{
    "delivery_mode": "micro-batch",
    "layers": ["raw", "validated", "curated"],
    "partition_key": "event_date",
    "recovery": "replay immutable raw batches from committed manifests",
    "rpo_minutes": 30,
    "rto_minutes": 60,
    "security_controls": ["encryption", "tokenization", "least privilege"],
    "assumptions": ["timestamps use Coordinated Universal Time (UTC)", "raw storage is durable"],
}
```

The tests assert required properties, not these exact words or architecture choices.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`. Be ready to defend one rejected architecture and estimate peak throughput.

## Unit test

```bash
pytest basics/01-data-architecture/tests -q
```
