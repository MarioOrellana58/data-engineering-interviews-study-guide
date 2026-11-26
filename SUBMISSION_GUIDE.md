# Exercise Delivery Guide

Interviewers score the explanation and trade-offs as well as the artifact. Deliver a compact package that another engineer can run and review.

## Every exercise

Include:

1. Your completed homework file without changing the public function or output contract.
2. A short note containing assumptions, complexity or capacity, rejected alternative, and known limitation.
3. The exact test command and its output.
4. One additional edge case you tested beyond the provided suite.

Never include credentials, personal data, confidential interview questions, or proprietary employer material.

## Python delivery

- Keep the public function small and deterministic.
- Separate validation, transformation, and publication when that improves clarity.
- State time and memory complexity.
- Demonstrate that inputs are not mutated unless the contract permits it.
- Be ready to add one test or change one requirement live.

Suggested verbal opening: “The invariant is ___. I chose ___ because ___. The operation costs ___ time and ___ memory. The main failure mode is ___.”

## Structured Query Language delivery

- Start with the output grain.
- State the deterministic tie-breaker and null policy.
- Use named common table expressions to expose stages, not to hide unnecessary scans.
- Explain large sorts, shuffles, partition pruning, and incremental execution.
- Show a tiny input/output example for the hardest boundary.

## Architecture and DataOps delivery

- Lead with quantified requirements and assumptions.
- Provide the smallest useful Mermaid diagram.
- Show throughput and storage math with units.
- Define recovery point objective (RPO), recovery time objective (RTO), ownership, alerts, rollback, and cost controls.
- End with a rejected alternative and the evidence that would change your choice.

Use a one-page architecture decision record (ADR) plus the diagram when a written artifact is requested.

## Experience-answer delivery

Prepare a 90-second version and a five-minute deep dive. Use Situation, Task, Action, Result (STAR), but emphasize personal decisions, measured evidence, a mistake, and what you would change. Keep a fact sheet so dates, scale, cost, tools, and responsibilities remain consistent across follow-up questions.

## Using the reference solutions

Reference solutions are examples, not the only valid answers. Compare invariants and trade-offs instead of copying style. Run all reference answers with:

```powershell
$env:STUDY_USE_SOLUTIONS="1"
python -m pytest -q
```

On macOS or Linux:

```bash
STUDY_USE_SOLUTIONS=1 python -m pytest -q
```

Unset the variable before returning to your homework so tests load the student files again.
