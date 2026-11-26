# Software Engineering and AI: Resilient API Ingestion

## Topic explanation

API ingestion must handle pagination, retries, rate limits, evolving schemas, duplicate objects, and resumable checkpoints. Unstructured payloads still need provenance and content hashes. For AI/ML consumers, reproducibility requires retaining source version and transformation version.

**Analogy:** Pagination is reading a book whose page numbers can change. A continuation token is the publisher's bookmark; checkpoints and stable IDs prevent lost or duplicated chapters.

## Solved practical example

Page 1 returns `(document A, version 1)` and token `t1`. Page 2 repeats A1, adds A2, and ends. The solved ingestion stores A1 and A2 once each, attaches source URL and retrieval time, and finishes with a null checkpoint. If processing stops after page 1, persist `t1` plus the seen `(A,1)` key; resuming neither loses A2 nor duplicates A1. A repeated `t1 → t1` token is an error, not an infinite loop.

## Code exercise

Implement `ingest_pages(fetch_page, start_token, seen_versions, max_pages)`. Detect token cycles, deduplicate by `(id, version)`, quarantine malformed objects, retain provenance, and return the next resumable checkpoint if interrupted. Do not catch programmer errors as network retries.

## AI review

Use `AI_REVIEW_PROMPT.md`; explain rate limiting, secrets, schema drift, and how an ML pipeline reproduces a dataset.

## Unit test

```bash
pytest intermediate/07-software-engineering-and-ai/tests -q
```
