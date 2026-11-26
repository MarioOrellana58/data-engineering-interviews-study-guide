# Reference Solutions

This directory mirrors every exercise. It is intentionally separate from the student homework so a normal test run still evaluates the learner's work.

Use the solutions only after a timed attempt, test run, and oral defense. They demonstrate one defensible implementation under the written constraints; they are not universal production designs.

## Run the answer key

Windows PowerShell:

```powershell
$env:STUDY_USE_SOLUTIONS="1"
python -m pytest -q
Remove-Item Env:STUDY_USE_SOLUTIONS
```

macOS/Linux:

```bash
STUDY_USE_SOLUTIONS=1 python -m pytest -q
```

The same tests are used for homework and reference answers. If you change an exercise contract, update its solution and verify both paths.

Every run prints either `STUDY TARGET: STUDENT HOMEWORK` or `STUDY TARGET: REFERENCE SOLUTIONS` before executing tests. Check that line before trusting a green result; leaving the environment variable enabled can otherwise grade the answer key instead of the student's work.

## Compare effectively

1. Diff your result against the matching file here.
2. Explain why both versions satisfy—or violate—the invariants.
3. Identify one case the public tests do not cover.
4. Improve your version without blindly copying the reference structure.

For the reasoning behind each answer, including its principal invariant, algorithmic cost, and intentional limitations, read [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md).
