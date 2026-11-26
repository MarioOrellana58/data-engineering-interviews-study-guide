# Software Engineering and AI: Point-in-Time Correct Features

## Topic explanation

ML and AI systems depend on reproducible, leakage-free data. A training feature may use only facts available by the label timestamp, including ingestion delay. Feature definitions need versions, lineage, freshness, and parity between batch training and online serving. AI-generated transformations require the same security and review controls as other production code.

## Practical example and analogy

Predicting yesterday's match using today's newspaper is not a strong model—it is time travel. Point-in-time joins prevent the model from seeing future knowledge.

## Code exercise

Implement `materialize_features(labels, events, definition_version)`. For each label, compute 7-day transaction count and amount using events whose `event_at` and `ingested_at` are no later than `label_at`. Exclude the exact label instant, preserve definition version, and produce deterministic feature hashes.

## AI review

Use `AI_REVIEW_PROMPT.md`; defend offline/online parity, late data, PII, drift, and AI-generated code review.

## Unit test

```bash
pytest advanced/07-software-engineering-and-ai/tests -q
```
