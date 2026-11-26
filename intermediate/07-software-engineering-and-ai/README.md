# Software Engineering and Artificial Intelligence (AI): Resilient Application Programming Interface (API) Ingestion

## Topic explanation

API ingestion must handle pagination, retries, rate limits, evolving schemas, duplicate objects, and resumable checkpoints. Unstructured payloads still need provenance and content hashes. For AI/machine learning (ML) consumers, reproducibility requires retaining source version and transformation version.

**Analogy:** Pagination is reading a book whose page numbers can change. A continuation token is the publisher's bookmark; checkpoints and stable identifiers (IDs) prevent lost or duplicated chapters only when the source guarantees that tokens remain valid long enough to resume.

## Solved practical example

Page 1 returns `(document A, version 1)` and token `t1`. Page 2 repeats A1, adds A2, and ends. The solved ingestion stores A1 and A2 once each, attaches the source uniform resource locator (URL) and retrieval time, and finishes with a null checkpoint. If the API documents durable continuation tokens, processing can persist `t1` plus the seen `(A,1)` key and resume without losing A2 or duplicating A1. If tokens expire, restart from a stable source cursor or safely restart and deduplicate. A repeated `t1 → t1` token is an error, not an infinite loop.

## Code exercise

Implement `ingest_pages(fetch_page, start_token, seen_versions, max_pages)`. Assume this exercise's source guarantees that tokens remain valid for the retry window. Detect token cycles, deduplicate by `(id, version)`, quarantine malformed objects, retain provenance, stop after `max_pages`, and return the next resumable checkpoint if interrupted. Do not catch programmer errors as network retries.

### Homework contract

`fetch_page(token)` returns `{"items": [...], "next_token": ..., "source": ..., "source_url": ..., "retrieved_at": ...}`. A valid item has a nonempty string `id`, exact integer `version`, and `body`. Copy `source`, retrieval URL, and retrieval time into every accepted item, and add a deterministic SHA-256 (Secure Hash Algorithm 256-bit) `content_hash` of the canonical body. If optional provenance is absent, use an explicit stable sentinel rather than the wall clock. Treat `(id, version)` as the deduplication key, including keys supplied in `seen_versions`; do not mutate that set.

Return `accepted`, `quarantined`, and `next_token`. Malformed items are quarantined with enough information to diagnose them. Fetch no more than `max_pages`, and return the unconsumed token when that bound interrupts ingestion. Raise `ValueError` for a repeated continuation token or a nonpositive page bound. Let unexpected exceptions from `fetch_page` propagate.

### Example input and expected output

```python
pages = {
    None: {
        "items": [{"id": "doc", "version": 1, "body": "old"}],
        "next_token": "next",
        "source": "partner-api",
        "source_url": "https://partner.example/documents",
        "retrieved_at": "2026-02-01T12:00:00Z",
    },
    "next": {
        "items": [{"id": "doc", "version": 2, "body": "new"}],
        "next_token": None,
        "source": "partner-api",
    },
}
result = ingest_pages(lambda token: pages[token], None, set(), max_pages=1)
```

Expected result after the one-page bound:

```python
result["accepted"][0]["id"] == "doc"
result["accepted"][0]["source"] == "partner-api"
result["accepted"][0]["source_url"] == "https://partner.example/documents"
result["accepted"][0]["retrieved_at"] == "2026-02-01T12:00:00Z"
len(result["accepted"][0]["content_hash"]) == 64
result["quarantined"] == []
result["next_token"] == "next"
```

Calling again with `start_token="next"` and `seen_versions={("doc", 1)}` accepts version 2 and finishes with a null token.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; explain rate limiting, secrets, schema drift, and how an ML pipeline reproduces a dataset.

## Unit test

```bash
pytest intermediate/07-software-engineering-and-ai/tests -q
```
