# Processing and Orchestration: CDC, Watermarks, and Backfills

## Topic explanation

CDC streams contain inserts, updates, deletes, duplicates, and out-of-order delivery. Correct application requires a source ordering key, tombstone policy, durable checkpoint, and rules for events older than retained state. Airflow schedules bounded work; Spark performs parallel state changes. Neither makes semantics automatic.

**Analogy:** CDC resembles editing a shared document through delayed mail. The postmark—not arrival order—determines which edit is newer, and a deletion is still an edit that must be remembered.

```mermaid
flowchart LR
    C[CDC log] --> B[Bounded batch]
    B --> D{Newer source version?}
    D -->|yes| M[Merge / tombstone]
    D -->|duplicate| X[No-op]
    D -->|too late| Q[Quarantine]
    M --> W[Commit data + checkpoint]
```

## Solved practical example

Snapshot `a=1` is at LSN 5. The batch arrives as delete `a` at LSN 8, update `a=7` at LSN 7, and insert `b=2` at LSN 6. Sort by source LSN, apply 6 then 7 then 8, and commit snapshot `{b: 2}` with checkpoint 8 atomically. If the worker crashes before commit, replay all three; after commit, checkpoint 8 makes the replay a no-op.

## Code exercise

Implement `apply_cdc(snapshot, events, checkpoint)`. Order by `(source_lsn, event_id)`, ignore exact replays, apply deletes, quarantine events at or below the checkpoint that conflict with current state, and advance the checkpoint only to committed input.

## AI review

Use `AI_REVIEW_PROMPT.md`; defend atomicity between data and checkpoint, plus backfill isolation.

## Unit test

```bash
pytest intermediate/03-processing-and-orchestration/tests -q
```
