# Contributing

Thank you for helping make this study guide more accurate, challenging, and useful.

## Good contributions

- Correct a technical error or ambiguous explanation.
- Add an interview-relevant edge case or failure mode.
- Strengthen a test without revealing the intended homework solution.
- Improve accessibility, diagrams, or setup instructions.
- Propose a focused exercise that fits the existing progression.

Do not contribute confidential interview questions, proprietary employer material, personal data, credentials, or claims presented as inside information.

## Before making a large change

Open an issue before adding a topic, changing an exercise contract, or reorganizing the curriculum. Small corrections can go directly to a pull request.

## Local setup

Python 3.11–3.14 is tested in continuous integration (CI).

```bash
python -m venv .venv
```

Activate the virtual environment with `.venv\Scripts\Activate.ps1` on Windows PowerShell or `source .venv/bin/activate` on macOS/Linux. Then run:

```bash
python -m pip install -e ".[study]"
python -m pytest --collect-only -q
```

## Exercise conventions

Each topic should remain compact and include:

1. A technically precise explanation with an analogy.
2. A fully solved practical example.
3. A different, challenging homework exercise.
4. An artificial intelligence (AI) review rubric in `AI_REVIEW_PROMPT.md`.
5. A student-owned homework file.
6. Tests and an exact command for running them.

Expand an acronym on its first use in each document. Prefer a small Mermaid diagram only when it makes a relationship or sequence easier to understand.

Homework files intentionally begin incomplete. New tests must collect successfully and fail for the missing behavior—not because of syntax errors, missing fixtures, network access, nondeterminism, or unavailable external services. Validate changed tests against a temporary reference implementation, but do not commit the solution.

## Validation

Run the checks relevant to your change:

```bash
python -m pytest --collect-only -q
STUDY_USE_SOLUTIONS=1 python -m pytest -q
python -m pytest path/to/changed/topic/tests -q
git diff --check
```

The default complete test suite is expected to fail until every homework is solved. The solution-mode suite must pass. Explain in the pull request how you validated any new or changed exercise.

On Windows PowerShell, run solution mode by setting `$env:STUDY_USE_SOLUTIONS="1"` before `python -m pytest -q`.

## Pull requests

- Keep one conceptual change per pull request.
- Link the related issue when one exists.
- Describe learner impact and technical trade-offs.
- Update documentation and tests together when an exercise contract changes.
- Confirm that no secrets or proprietary interview content are included.

By contributing, you agree that your contribution is licensed under the repository's MIT License and that you will follow the Code of Conduct.
