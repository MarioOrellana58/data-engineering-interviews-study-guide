# Reliable Orders Pipeline

> Illustrative structure only. Never present this fictional project as personal experience; replace it with facts you can defend truthfully.

## 90-second answer

I led the reliability redesign of an hourly orders pipeline that supplied Finance and Operations. It processed about 420 gigabytes per day from 18 source tables and routinely finished in 145 minutes against a 120-minute service-level objective. I profiled the stages and found that retries appended output again, while one customer key caused a 31-times skew in the largest join. I designed an immutable raw landing layer, deterministic batch manifests, and an overwrite-by-partition publication step. I also implemented selective salting for the four largest customer keys instead of increasing the whole cluster. After a two-week parallel run, the 95th-percentile duration fell to 68 minutes, duplicate incidents fell from 7 per quarter to 0, and compute cost fell 16%. I owned the design, implementation plan, reconciliation queries, rollout gates, and incident runbook. Platform engineers reviewed the infrastructure changes, and Finance approved the reconciliation tolerances.

## Scale and evidence

- 420 gigabytes per day, 18 sources, and roughly 96 million order-line events per day.
- A 120-minute freshness objective with a previous 145-minute 95th percentile.
- Reconciliation covered row counts, distinct business keys, gross amount by currency, and sampled hashes.
- Seven consecutive parallel runs had zero unexplained differences before cutover.
- The final 95th percentile was 68 minutes and monthly compute cost was 16% lower.

## My decisions and rejected alternative

I decided to make a batch identifier, input manifest, code version, and target partition part of every commit. A retry first checked that commit record; it did not blindly append. I rejected doubling cluster size because profiling showed skew and duplicate publication, not uniform capacity pressure. More hardware would have shortened some tasks while preserving the correctness defect. I also rejected salting every key because it would complicate joins and increase data volume. Selective salting addressed the measured hot keys with a smaller operational cost.

## Failure, detection, and recovery

During the parallel run, a worker timed out after writing files but before reporting success. The orchestrator retried the task. The new commit check detected that the batch and partition were already published, verified the manifest checksum, and returned success without another write. An alert fired because the worker timeout rate exceeded 2%, but consumers saw one consistent partition. I led the incident review and discovered that our first dashboard measured task success without distinguishing an ambiguous timeout. I added commit-state metrics, a runbook decision tree, and a fault-injection test covering failures before write, after write, and after commit.

## What I would change now

My main mistake was starting implementation before documenting the end-to-end delivery guarantee. The source, transformation, audit copy, and curated table did not all share one transaction, so calling the entire system “exactly once” was inaccurate. I would now define the business invariant first: one current order version per business key and source version. I would also introduce contract tests with Finance earlier, keep the parallel run cost visible from day 1, and schedule a quarterly restore exercise instead of treating the runbook as sufficient evidence.
