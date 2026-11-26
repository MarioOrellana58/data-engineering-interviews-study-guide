# Senior Data Engineer Interview Lab

An interview-focused curriculum for Factored's Senior Data Engineer role. It covers the seven areas named in the interview guidance and emphasizes the role's Python, Structured Query Language (SQL), Databricks, Snowflake, Spark/Airflow, cloud, data-quality, security, and graph-data requirements.

This is an independent educational resource. It is not affiliated with or endorsed by Factored, and interview processes may change.

## How to use it

1. Work in order: `basics`, `intermediate`, then `advanced`.
2. Time-box the first attempt. Do not use artificial intelligence (AI) until the timer expires.
3. Edit the topic's `homework.py`, `homework.sql`, or `homework.md`.
4. Run the command shown in that topic's README.
5. Use its `AI_REVIEW_PROMPT.md` only after tests run.
6. Defend the result aloud: assumptions, scale, failure modes, cost, and rejected alternatives.

"Basics" means senior foundations, not beginner work. Intermediate labs integrate systems. Advanced labs introduce ambiguity, failure, scale, and competing constraints.

Every topic follows the same compact sequence: explanation with an analogy, a fully solved practical example, a different graded homework exercise, an AI-review prompt, and unit-test commands.

## Curriculum map

| Interview area | Basics | Intermediate | Advanced |
|---|---|---|---|
| Experience | Evidence-based Situation, Task, Action, Result (STAR) story | Architecture deep dive | Adversarial project defense |
| Data architecture | Requirements and batch design | Lakehouse migration | Multi-tenant global platform |
| Data storage | Format and partition choices | Snowflake/Delta physical design | Table internals and graph decisions |
| Processing/orchestration | Idempotent Python-based extract, transform, and load (ETL) and retry concepts | Change data capture (CDC) and workflow design | Replay, backpressure, and distributed correctness |
| Data modeling | Dimensional fundamentals | slowly changing dimension Type 2 (SCD2) and medallion | Bitemporal/event/graph models |
| DataOps | Contracts and quality gates | Continuous integration and continuous delivery (CI/CD), lineage, observability | Service-level objectives (SLOs), incidents, disaster recovery |
| SQL/coding | Analytical SQL and Python fundamentals | Sessionization and query reasoning | Constant-memory streaming reconciliation |
| Software engineering (SWE) / AI | Retry policy, testing, and network-failure handling | Resilient application programming interface (API) ingestion and unstructured data | Point-in-time-correct machine learning (ML) feature engineering and AI risk |

The final capstone combines system design, coding, incident response, and an oral defense.

## Setup

Python 3.11–3.14 is tested in continuous integration (CI).

```bash
python -m venv .venv
```

Activate the environment with `.venv\Scripts\Activate.ps1` on Windows PowerShell or `source .venv/bin/activate` on macOS/Linux. Then run:

```bash
python -m pip install -e ".[study]"
python -m pytest --collect-only -q
```

Run everything with `python -m pytest -q`. Initial failures are expected because homework files contain deliberate TODOs.

## Scoring

- 40% correctness and tests
- 20% scale and performance
- 15% reliability and operability
- 10% security and governance
- 15% communication and trade-offs

Treat 85/100 as ready for another mock and 95/100 as interview-ready. A passing test suite is necessary but not sufficient.

## Contributing

Corrections and new exercise proposals are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before opening a pull request. Never submit confidential interview questions or proprietary employer material.

## Security

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md). Do not disclose credentials or sensitive reports in public issues.

## License

Licensed under the [MIT License](LICENSE).
