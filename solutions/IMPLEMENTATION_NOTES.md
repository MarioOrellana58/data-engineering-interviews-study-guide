# Reference Solution Notes

These notes explain the decisions behind the answer key. Complexity uses `n` for input rows or events unless another symbol is stated. The implementations are interview-sized demonstrations, not production libraries. Artificial intelligence (AI) and Structured Query Language (SQL) retain their standard meanings throughout.

## Basics

| Module | Invariant and approach | Cost and intentional limitation |
|---|---|---|
| Experience defense | Each claim connects an action to evidence, a trade-off, and a measurable result. The sample uses a compact Situation, Task, Action, Result (STAR) narrative. | Human-reviewed prose; it cannot verify that the evidence is true. |
| Data architecture | Freshness selects the delivery family while daily volume sizes parallelism and files. Recovery and personally identifiable information (PII) controls remain explicit. | Constant time; thresholds are teaching heuristics, not a cloud cost model. |
| Data storage | File format, partitioning, and compaction are selected from scan and update behavior rather than brand preference. | Constant time; does not inspect real query history. |
| Processing and orchestration | One deterministic row survives per event; exact retries collapse and ambiguous equal-time conflicts fail closed. | `O(n log n)` from deterministic ordering; in-memory only. |
| Data modeling | The fact grain is unique, dimensions are deterministic, and unknown customers share one member. Conflicting attributes are rejected. | `O(n log n)`; assumes a snapshot rather than historized dimensions. |
| DataOps | Invalid rows are quarantined before uniqueness and freshness gates are evaluated. Times are converted to Coordinated Universal Time (UTC). | `O(n)` plus output ordering; the email-like validations are deliberately small. |
| SQL and coding | Window functions preserve row grain while computing ranks and running measures. | Database sort cost is typically `O(n log n)`; exercise data fits one engine. |
| Software engineering and AI | Retry decisions depend on failure class and bounded exponential backoff, with dependency injection for deterministic tests. | Constant state; no real network client or jitter distribution. |

## Intermediate

| Module | Invariant and approach | Cost and intentional limitation |
|---|---|---|
| Experience defense | The narrative separates observed facts, personal decisions, alternatives, and failure recovery. | Human-reviewed; diagrams and metrics still require corroboration. |
| Data architecture | Migration advances only through measured exit gates, with dual running and a rollback path. Recovery targets affect cost. | Constant time; estimate is illustrative rather than vendor pricing. |
| Data storage | Maintenance is recommended only when scan evidence justifies its recurring cost; high updates narrow clustering and file targets. | `O(c log c)` for `c` filter columns; thresholds require benchmarking. |
| Processing and orchestration | Log sequence numbers (LSNs), event identifiers, checkpoints, and durable tombstones make replay distinguishable from conflict across calls. | `O(n log n)`; the state envelope stands in for transactional storage. |
| Data modeling | Slowly changing dimension Type 2 (SCD2) intervals are half-open and non-overlapping; same-time contradictions fail closed. | `O(n log n)`; accepts lexical business timestamps as specified by the exercise. |
| DataOps | Deployment gates combine tests, lineage, quality, rollback, and ownership instead of treating continuous integration and continuous delivery (CI/CD) as only automation. | Human-reviewed configuration; no vendor-specific pipeline runner. |
| SQL and coding | Deduplication precedes sessionization. A funnel advances by strict row position ordered by timestamp and identifier, including timestamp ties. | Window sorts are `O(n log n)`; assumes one deterministic event identifier per logical event. |
| Software engineering and AI | Pagination is bounded and cycle-safe; accepted content carries source, retrieval provenance, and a Secure Hash Algorithm 256-bit (SHA-256) fingerprint. | `O(n)` expected time and memory for seen keys; does not persist checkpoints externally. |

## Advanced

| Module | Invariant and approach | Cost and intentional limitation |
|---|---|---|
| Experience defense | The answer exposes uncertainty, rejected options, operational failures, and what the candidate personally owned. | Human-reviewed; it is a rehearsal framework, not a factual validator. |
| Data architecture | Residency is a hard boundary, capacity includes headroom, tenants affect cost, and failover is claimed only with a second legal region. | Constant time; region classification and cost coefficients are simplified. |
| Data storage | Analytical storage remains authoritative; graph data is a versioned projection. Writer contention and source replay retention are separate concerns. | Constant time; no live benchmark or storage calculator. |
| Processing and orchestration | A source offset maps to one event and an event identifier maps to one offset. Committed boundaries advance the effective checkpoint. | `O(n log n)`; assumes committed batch metadata is trustworthy. |
| Data modeling | Bitemporal rows preserve both valid time and system time; identical coordinates cannot contain contradictory facts. | Can grow quadratically in the number of system versions; optimized temporal databases use more compact structures. |
| DataOps | Error-budget consumption and transitive critical impact drive incident severity; lineage traversal is cycle-safe. | `O(V + E)` for assets and lineage edges; severity policy is illustrative. |
| SQL and coding | Two sorted iterators are reconciled with a merge, so memory does not grow with input size. | `O(n + m)` time and `O(1)` auxiliary space; inputs must already be uniquely sorted. |
| Software engineering and AI | Point-in-time eligibility uses both event time and ingestion time. The feature hash commits to canonical eligible evidence, not only aggregates. | Roughly `O(L × E)` for labels and events; production systems index by entity and time. |
| Capstone | Durable watermarks, tombstones, and event fingerprints prevent replay conflicts and stale resurrection. Keyed-Hash Message Authentication Code (HMAC) tokens remove raw email but remain personal data. | `O(n log n)` per batch and state grows with processed identifiers; production needs retention, key rotation, and transactional persistence. |
