# DataOps: SLOs, Incidents, and Recovery

## Topic explanation

A service-level objective (SLO) defines consumer-visible reliability; an error budget controls change velocity. Incident response prioritizes impact, containment, communication, restoration, and learning. Lineage turns a failed asset into a blast radius. Disaster recovery is credible only when restored data is validated through exercises.

**Analogy:** An SLO is a household circuit breaker, not a promise that electricity never fails. It defines tolerable failure and stops risky changes after the budget is consumed.

```mermaid
flowchart LR
    M[Service-level indicator (SLI) breach] --> B[Compute blast radius]
    B --> S[Assign severity + owner]
    S --> C[Contain]
    C --> R[Restore / replay]
    R --> V[Validate consumers]
    V --> P[Blameless corrective actions]
```

## Solved practical example

A 99.9% service-level objective over a 30-day month allows about 43.2 bad minutes. A 90-minute freshness incident consumes 2.08 times, or 208%, of that monthly error budget. That is a budget-consumption ratio, not a burn rate; burn rate additionally expresses how quickly budget is being consumed over an observation window. Lineage shows the affected raw table feeds a regulatory Finance report, so declare severity (SEV) level 1 or 2 according to company policy, freeze deployments, stop the corrupt producer, communicate every 30 minutes, replay from the last verified offset, and validate Finance totals before closure. Twenty broken sandboxes alone would not justify the same severity.

## Code exercise

Implement `assess_incident(asset, observed, slo, lineage)`. Calculate the error-budget-consumed ratio, transitive critical consumers, severity, immediate actions, communication cadence, replay boundary, and whether deployments freeze. Avoid upgrading severity solely because many noncritical assets exist. A true burn-rate calculation would also require a defined observation window and error ratio.

### Homework contract

`lineage` is an adjacency list from an asset to its direct consumers and may contain cycles. `observed` includes `bad_minutes`, critical assets, and `last_good_offset`; `slo` supplies availability target and window length. Return `blast_radius`, `critical_consumers`, `error_budget_consumed_ratio`, `severity`, `freeze_deployments`, at least four `immediate_actions`, communication cadence, and `replay_from`.

Traverse lineage transitively and include the starting asset exactly once. Calculate allowed bad minutes as `(1 - availability_target) * window_minutes`, then divide observed bad minutes by that allowance. Severity must prioritize critical consumer impact and budget consumption, not the raw number of nodes. Cycle detection is required.

Require `0 < availability_target < 1`, a positive window, and nonnegative bad minutes. Reject invalid inputs instead of dividing by zero or producing a misleading negative budget-consumption ratio.

### Example input and expected output

```python
lineage = {"raw": ["model"], "model": ["report"], "report": []}
observed = {
    "bad_minutes": 2,
    "critical_assets": ["report"],
    "last_good_offset": 90,
}
slo = {"availability_target": 0.99, "window_minutes": 100}
```

The error allowance is 1 minute, so the consumed ratio is approximately 2. Expected properties:

```python
set(result["blast_radius"]) == {"raw", "model", "report"}
result["critical_consumers"] == ["report"]
1.99 < result["error_budget_consumed_ratio"] < 2.01
result["severity"] in {"SEV-1", "SEV-2"}
result["freeze_deployments"] is True
result["replay_from"] == 90
```

## Artificial Intelligence (AI) review

Use `AI_REVIEW_PROMPT.md`; run a live incident with incomplete and changing evidence.

## Unit test

```bash
pytest advanced/05-dataops/tests -q
```
