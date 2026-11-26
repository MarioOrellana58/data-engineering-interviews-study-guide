# Software Engineering and Artificial Intelligence (AI): Point-in-Time Correct Features

## Topic explanation

Machine learning (ML) and AI systems depend on reproducible, leakage-free data. A training feature may use only facts available by the label timestamp, including ingestion delay. Feature definitions need versions, lineage, freshness, and parity between batch training and online serving. AI-generated transformations require the same security and review controls as other production code.

**Analogy:** Predicting yesterday's match using today's newspaper is not a strong model—it is time travel. Point-in-time joins prevent future knowledge from leaking into training.

## Solved practical example

A label at January 10 noon considers a January 5 transaction ingested January 5. It excludes a January 6 transaction ingested January 11 because the system did not know it at label time, excludes an event exactly at noon, and excludes January 1 because it falls outside the seven-day window. The solved feature is count `1`, amount `10`, definition version `v3`, plus a deterministic hash of inputs and definition.

## Code exercise

Implement `materialize_features(labels, events, definition_version)`. For each label, compute 7-day transaction count and amount using events whose `event_at` and `ingested_at` are no later than `label_at`. Exclude the exact label instant, preserve definition version, and produce deterministic feature hashes.

## AI review

Use `AI_REVIEW_PROMPT.md`; defend offline/online parity, late data, personally identifiable information (PII), drift, and AI-generated code review.

## Unit test

```bash
pytest advanced/07-software-engineering-and-ai/tests -q
```
