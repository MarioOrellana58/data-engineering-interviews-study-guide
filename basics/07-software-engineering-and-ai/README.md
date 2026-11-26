# Software Engineering and AI: Make Failure Explicit

## Topic explanation

Data engineers ship software: typed interfaces, bounded resource use, tests, logs, and predictable failure. Network calls require timeouts and classified retries. AI-generated code has the same review bar as human code; plausibility is not evidence.

**Analogy:** Retries are medicine: the correct dose treats a transient problem, while unlimited doses make the system sicker. Authentication and validation failures do not improve with repetition.

## Solved practical example

With `max_attempts=4`, `base_delay=2`, and `max_delay=5`, three transient failures followed by success produce planned delays `[2, 4, 5]`. A `401 Unauthorized` fails immediately because it is non-transient. The function returns delays instead of sleeping, making policy testable and leaving scheduling to the caller.

## Code exercise

Implement `retry_call`. It must retry only exceptions approved by `is_transient`, use bounded exponential delays, never sleep inside the function, and expose the planned delays for testing. Validate arguments. Preserve the final exception rather than wrapping away its type.

Then inspect your own implementation as if AI generated it: identify one way careless retry logic could create a data or availability incident.

## AI review

Use `AI_REVIEW_PROMPT.md`; expect OOP/interface, networking, testing, and complexity questions.

## Unit test

```bash
pytest basics/07-software-engineering-and-ai/tests -q
```
