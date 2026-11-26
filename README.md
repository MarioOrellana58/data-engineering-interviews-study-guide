# Senior Data Engineer Interview Lab

An interview-focused curriculum for Factored's Senior Data Engineer role. It covers the seven areas named in the interview guidance and emphasizes the role's Python, SQL, Databricks, Snowflake, Spark/Airflow, cloud, data-quality, security, and graph-data requirements.

## How to use it

1. Work in order: `basics`, `intermediate`, then `advanced`.
2. Time-box the first attempt. Do not use AI until the timer expires.
3. Edit the topic's `homework.py`, `homework.sql`, or `homework.md`.
4. Run the command shown in that topic's README.
5. Use its `AI_REVIEW_PROMPT.md` only after tests run.
6. Defend the result aloud: assumptions, scale, failure modes, cost, and rejected alternatives.

"Basics" means senior foundations, not beginner work. Intermediate labs integrate systems. Advanced labs introduce ambiguity, failure, scale, and competing constraints.

Every topic follows the same compact sequence: explanation with an analogy, a fully solved practical example, a different graded homework exercise, an AI-review prompt, and unit-test commands.

## Curriculum map

| Interview area | Basics | Intermediate | Advanced |
|---|---|---|---|
| Experience | Evidence-based STAR story | Architecture deep dive | Adversarial project defense |
| Data architecture | Requirements and batch design | Lakehouse migration | Multi-tenant global platform |
| Data storage | Format and partition choices | Snowflake/Delta physical design | Table internals and graph decisions |
| Processing/orchestration | Idempotent ETL | Airflow, Spark, CDC | Replay, backpressure, distributed correctness |
| Data modeling | Dimensional fundamentals | SCD2 and medallion | Bitemporal/event/graph models |
| DataOps | Contracts and quality gates | CI/CD, lineage, observability | SLOs, incidents, disaster recovery |
| SQL/coding | Analytical SQL and Python | Query plans and algorithms | Concurrency and constrained live coding |
| SWE/AI | OOP, tests, OS/networking | APIs, unstructured/ML data | AI-platform reliability and security |

The final capstone combines system design, coding, incident response, and an oral defense.

## Setup

```bash
python -m venv .venv
# PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -e ".[study]"
pytest --collect-only -q
```

Run everything with `pytest -q`. Initial failures are expected because homework files contain deliberate TODOs.

## Scoring

- 40% correctness and tests
- 20% scale and performance
- 15% reliability and operability
- 10% security and governance
- 15% communication and trade-offs

Treat 85/100 as ready for another mock and 95/100 as interview-ready. A passing test suite is necessary but not sufficient.
