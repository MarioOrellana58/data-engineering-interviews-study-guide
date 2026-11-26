# Processing and Orchestration: Distributed Correctness

## Topic explanation

Exactly-once is an end-to-end property, not a checkbox. Sources need stable offsets, transforms need deterministic semantics, sinks need idempotent or transactional commits, and checkpoints must align with published output. Backpressure protects the system by bounding admitted work.

**Analogy:** Paying a bill and updating the checkbook must be one recoverable action. If a crash occurs between them, the payment identifier—not hope—prevents double payment.

```mermaid
sequenceDiagram
    participant S as Source offsets
    participant P as Processor
    participant T as Transactional sink
    P->>S: read (checkpoint, end]
    P->>T: stage batch_id + results
    P->>T: atomically commit results + end offset
    Note over P,T: Crash before commit = replay<br/>Crash after commit = detect batch_id
```

## Solved practical example

Checkpoint 100 and capacity 2 receive offsets 101–105. Deterministic batches are `[101,102]`, `[103,104]`, and `[105]`; each batch identifier (ID) hashes its offset range and input IDs. A sink transaction writes outputs and the end offset together. If batch 2 times out after commit, recovery finds its batch ID and skips it. If it timed out before commit, the same deterministic batch is safe to replay.

## Code exercise

Implement `recover_and_plan(events, committed_batches, checkpoint, capacity)`. Ignore committed event IDs, order source offsets, split deterministic bounded batches, reject offset conflicts, and attach an atomic commit record containing batch ID, offset range, input hash, and output IDs.

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; explain crash points, poison records, and what “exactly once” means to the business.

## Unit test

```bash
pytest advanced/03-processing-and-orchestration/tests -q
```
