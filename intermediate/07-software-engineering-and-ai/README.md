# Software Engineering and AI: Resilient API Ingestion

## Topic explanation

API ingestion must handle pagination, retries, rate limits, evolving schemas, duplicate objects, and resumable checkpoints. Unstructured payloads still need provenance and content hashes. For AI/ML consumers, reproducibility requires retaining source version and transformation version.

## Practical example and analogy

Pagination is reading a book whose page numbers can change while you read. A continuation token is a bookmark issued by the publisher; checkpoints and stable IDs keep you from losing or duplicating chapters.

## Code exercise

Implement `ingest_pages(fetch_page, start_token, seen_versions, max_pages)`. Detect token cycles, deduplicate by `(id, version)`, quarantine malformed objects, retain provenance, and return the next resumable checkpoint if interrupted. Do not catch programmer errors as network retries.

## AI review

Use `AI_REVIEW_PROMPT.md`; explain rate limiting, secrets, schema drift, and how an ML pipeline reproduces a dataset.

## Unit test

```bash
pytest intermediate/07-software-engineering-and-ai/tests -q
```
