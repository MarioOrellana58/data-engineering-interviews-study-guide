# Software Engineering and Artificial Intelligence (AI): Point-in-Time Correct Features

## Topic explanation

Machine learning (ML) and AI systems depend on reproducible, leakage-free data. A training feature may use only facts available by the label timestamp, including ingestion delay. Feature definitions need versions, lineage, freshness, and parity between batch training and online serving. AI-generated transformations require the same security and review controls as other production code.

**Analogy:** Predicting yesterday's match using today's newspaper is not a strong model—it is time travel. Point-in-time joins prevent future knowledge from leaking into training.

## Solved practical example

A label at January 10 noon considers a January 5 transaction ingested January 5. It excludes a January 6 transaction ingested January 11 because the system did not know it at label time, excludes an event exactly at noon, and excludes January 1 because it falls outside the seven-day window. The solved feature is count `1`, amount `10`, definition version `v3`, plus a deterministic hash of inputs and definition.

## Code exercise

Implement `materialize_features(labels, events, definition_version)`. For each label, compute 7-day transaction count and amount using events whose `event_at` and `ingested_at` are both strictly earlier than `label_at`. Exclude the exact label instant, preserve definition version, and produce deterministic feature hashes.

### Homework contract

Each label has `entity_id`, International Organization for Standardization (ISO) 8601 `label_at`, and a target value. Events have identifiers, entity, event and ingestion timestamps, and amount. For each label, include an event only when it belongs to that entity, falls within `[label_at - 7 days, label_at)`, and was ingested before the label. Return one row per label with the original label fields, `txn_count_7d`, `txn_amount_7d`, `definition_version`, and a nonempty deterministic `feature_hash`.

Input event order must not affect output. Hash stable canonical feature content and version—not Python dictionary order or runtime object identity. A late event whose business time is in the window but ingestion time is after the label must be excluded to prevent knowledge leakage.

### Example input and expected output

```python
labels = [{"entity_id": "u1", "label_at": "2026-02-08T00:00:00+00:00", "label": 1}]
events = [
    {"event_id": "ok", "entity_id": "u1", "event_at": "2026-02-03T00:00:00+00:00", "ingested_at": "2026-02-03T00:01:00+00:00", "amount": 8},
    {"event_id": "late", "entity_id": "u1", "event_at": "2026-02-04T00:00:00+00:00", "ingested_at": "2026-02-09T00:00:00+00:00", "amount": 20},
]
```

Expected result properties:

```python
row = materialize_features(labels, events, "v2")[0]
row["txn_count_7d"] == 1
row["txn_amount_7d"] == 8
row["definition_version"] == "v2"
bool(row["feature_hash"]) is True
```

## AI review

Use `AI_REVIEW_PROMPT.md`; defend offline/online parity, late data, personally identifiable information (PII), drift, and AI-generated code review.

## Unit test

```bash
pytest advanced/07-software-engineering-and-ai/tests -q
```
