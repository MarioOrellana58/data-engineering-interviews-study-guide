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

## Compare effectively

1. Diff your result against the matching file here.
2. Explain why both versions satisfy—or violate—the invariants.
3. Identify one case the public tests do not cover.
4. Improve your version without blindly copying the reference structure.
