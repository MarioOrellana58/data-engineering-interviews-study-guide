# Software Engineering and Artificial Intelligence (AI): Make Failure Explicit

## Topic explanation

Data engineers ship software: typed interfaces, bounded resource use, tests, logs, and predictable failure. Network calls require timeouts and classified retries. AI-generated code has the same review bar as human code; plausibility is not evidence.

**Analogy:** Retries are medicine: the correct dose treats a transient problem, while unlimited doses make the system sicker. Authentication and validation failures do not improve with repetition.

## Solved practical example

With `max_attempts=4`, `base_delay=2`, and `max_delay=5`, three transient failures followed by success produce planned delays `[2, 4, 5]`. A `401 Unauthorized` fails immediately because it is non-transient. The function returns delays instead of sleeping, making policy testable and leaving scheduling to the caller.

## Code exercise

Implement `retry_call`. It must retry only exceptions approved by `is_transient`, use bounded exponential delays, never sleep inside the function, and expose the planned delays for testing. Validate arguments. Preserve the final exception rather than wrapping away its type.

Then inspect your own implementation as if AI generated it: identify one way careless retry logic could create a data or availability incident.

### Homework contract

Call `operation` at most `max_attempts` times. When it raises an exception, call `is_transient(error)`. Re-raise immediately if it returns false; otherwise record the delay that would precede the next attempt. Delay number `n` is `min(base_delay * 2**n, max_delay)`, starting with `n = 0`. Do not actually sleep.

Return `(value, delays)` after success. If every allowed attempt fails, re-raise the final original exception. Reject `max_attempts < 1`, negative delays, or a base delay greater than the maximum.

### Example input and expected output

```python
attempts = iter([TimeoutError("temporary"), "done"])

def operation():
    value = next(attempts)
    if isinstance(value, Exception):
        raise value
    return value

retry_call(
    operation,
    lambda error: isinstance(error, TimeoutError),
    max_attempts=3,
    base_delay=1,
    max_delay=8,
)
# ("done", [1])
```

Changing the exception to `ValueError("bad request")` with a classifier that returns false must raise it after one call and record no delay.

## AI review

Use `AI_REVIEW_PROMPT.md`; expect object-oriented programming (OOP)/interface, networking, testing, and complexity questions.

## Unit test

```bash
pytest basics/07-software-engineering-and-ai/tests -q
```
