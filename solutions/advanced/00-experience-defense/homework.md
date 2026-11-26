# Senior Interview Story Bank

> Illustrative structure only. Never present these fictional projects as personal experience; replace them with facts you can defend truthfully.

## Architecture Story

### Situation

I inherited a regional commerce-data platform that processed 8.4 billion events per day for 310 tenants. It had grown from one batch pipeline into 64 independently scheduled jobs, with duplicated customer logic and no explicit isolation boundary. The 95th-percentile freshness was 96 minutes against a 30-minute service-level objective (SLO). Three large tenants generated 52% of peak traffic, and a promotion by one tenant could delay every other tenant. Monthly compute and storage cost was approximately $238,000.

### Task

I was accountable for the target architecture and migration plan. The constraints were a 15-minute recovery point objective (RPO), a 60-minute recovery time objective (RTO), European Union (EU) data residency, no more than 20% temporary migration cost, and no “big bang” cutover. I needed agreement from Security, Finance, six consuming teams, and a platform group that owned the shared cloud account.

### Action

I measured an average 97,000 events per second and a four-times peak. With 30% headroom, the ingestion design needed at least 504,000 events per second. I designed region-scoped data planes with per-tenant queues, quotas, encryption keys, workload pools, and cost tags. A global control plane held tenant identifiers and policy metadata but no customer payloads. European Union payloads remained in approved European Union regions, including failover.

I chose immutable raw objects plus versioned manifests as the recovery boundary. Curated Delta tables served transformation and machine-learning feature workloads; Snowflake served governed analytical consumers. Airflow coordinated workflows but held no business transformations. We migrated four phases: raw backfill, 14-day dual run, two canary consumers, and critical-consumer cutover. Exit gates compared counts, distinct keys, amounts by currency, null rates, and sampled hashes at business grain.

I rejected a single global data plane because cross-region failover would violate residency for some tenants. I also rejected one isolated account per tenant because 310 copies would have exceeded the operations budget. The compromise was shared regional infrastructure with logical isolation and dedicated compute for the largest or regulated tenants.

### Result

After 11 weeks, 92% of tenants were on the new path. The 95th-percentile freshness fell from 96 to 18 minutes. A large-tenant promotion no longer moved small-tenant freshness by more than 3 minutes. Monthly steady-state cost fell 14% to about $205,000, although the dual run peaked at $273,000 for 9 days. We completed two region-failure exercises within a 47-minute recovery time and lost less than 8 minutes of accepted data.

### Mistake and changed opinion

My mistake was underestimating control-plane dependency. The first design required the global tenant catalog during every ingestion request. A simulated control-plane outage stopped healthy regional data planes. I changed the design so regions cached signed policy snapshots and could operate for 4 hours without the global service. This added revocation delay, so high-risk tenant disablement used a separate emergency channel. I would model control-plane unavailability before the first architecture review now.

## Incident Story

### Situation

Six weeks after the first critical cutover, Finance reported that one daily revenue table was 2.7% low. The freshness dashboard was green because the job completed in 41 minutes. Lineage showed that the table fed 17 dashboards, one lender report, and a same-day settlement file. The incident began at 08:20 Coordinated Universal Time (UTC), two hours before the settlement deadline.

### Task

I became incident commander. My priorities were to bound consumer impact, stop additional corruption, preserve evidence, restore the last correct state, and communicate without guessing. The declared recovery time objective was 60 minutes, but the regulatory settlement deadline made validated correctness more important than a fast unverified publish.

### Action

I assigned owners for source validation, transformation analysis, consumer communication, and recovery. We froze deployments and paused the curated publisher, while raw ingestion continued into immutable storage. I set a 20-minute update cadence. Reconciliation by currency localized 94% of the gap to refunded orders from one source version. A schema change had converted a nullable refund flag into the strings `true`, `false`, and `unknown`; the transform treated every nonempty string as true.

We restored the previous curated snapshot, replayed manifests from offset 18,420,771 with an explicit parser, and validated counts, distinct order identifiers, gross revenue, refunds, and sampled hashes. Finance compared 25 known accounts before approving republication. We met the external deadline 12 minutes late but avoided sending a plausible and incorrect settlement file.

I rejected patching the aggregate directly because it would not repair downstream facts or provide a replayable history. I also rejected rolling back raw ingestion because raw bytes were valid and stopping them would have increased the recovery point gap.

### Result

The incident lasted 103 minutes. We corrected 6.1 million order versions and notified all 17 dashboard owners. No settlement file containing incorrect totals left the company. Follow-up work added explicit enumerated-value contracts, a consumer-visible correctness indicator, and a canary with 12 semantic reconciliation checks. Similar schema drift was caught twice in preproduction over the next 6 months.

### Mistake and changed opinion

At 09:00 I told stakeholders that recovery would fit inside 60 minutes before the replay throughput was measured. That estimate was unjustified and forced a correction 20 minutes later. I apologized, separated observed facts from forecasts, and required every later estimate to include remaining bytes, measured throughput, validation duration, and confidence. I now prefer a slower evidence-based forecast to an optimistic incident promise.

## Leadership Story

### Situation

The migration depended on a common event contract, but six teams used different meanings for `customer_id`, deletion, and event time. A platform group proposed enforcing one schema immediately. Product teams argued that a forced change would delay three launches worth $1.4 million. Meetings had become positional, and no team owned the cross-system decision.

### Task

I was asked to lead the technical decision even though none of the teams reported to me. I needed a contract that protected correctness, a migration path teams could staff, and a decision process that did not hide business trade-offs behind architecture language.

### Action

I wrote a one-page decision record separating nonnegotiable invariants from evolvable fields. The invariants were a stable event identifier, source version, event time, ingestion time, operation type, tenant identifier, and explicit deletion. I interviewed each team and mapped 23 existing fields into that core. Instead of demanding immediate conformance, I proposed versioned adapters at the boundary, a 90-day deprecation window, and a scorecard showing malformed, legacy, and unknown-field rates by producer.

One senior engineer opposed adapters because they could become permanent. That was a valid risk. I added an owner, deletion date, and weekly burn-down target for every adapter. I also made the raw payload available for replay so adapter bugs did not destroy evidence. Finance funded two shared engineers after I quantified that independent migrations would repeat roughly 14 engineer-weeks of work.

I personally facilitated the decision workshops, wrote the contract and compatibility policy, implemented the first adapter, and presented cost scenarios. Producer teams implemented their own migrations; I did not claim their delivery work.

### Result

All six teams signed the decision. Five migrated within 74 days, and the sixth received a documented 30-day extension because of a regulatory release freeze. Invalid events fell from 1.8% to 0.06%, while none of the three product launches moved. We deleted 21 of 23 legacy mappings by day 120. The remaining two became supported fields after evidence showed they represented legitimate regional requirements.

### Mistake and changed opinion

My first proposal labeled all producer differences “technical debt,” which made teams defensive and ignored legitimate domain variation. A product lead challenged that framing. I changed the workshop to ask which differences violated an invariant and which represented real business meaning. That distinction improved both the contract and the relationship. I learned that technical leadership means creating a falsifiable decision process, not winning a design argument.

## Consistency Matrix

| Fact | Architecture Story | Incident Story | Leadership Story |
|---|---|---|---|
| Platform | Regional commerce data platform | Same platform after critical cutover | Contract migration for same platform |
| Scale | 8.4 billion events/day, 310 tenants | 6.1 million corrected versions | 6 producer teams, 23 legacy fields |
| Role | Architecture and migration owner | Incident commander | Cross-team technical lead |
| Freshness objective | 30 minutes | Pipeline finished in 41 minutes but was wrong | Contract quality supported freshness |
| Recovery targets | 15-minute RPO, 60-minute RTO | 103-minute incident, correctness prioritized | Replayable adapters preserve recovery |
| Cost | $238,000 before, $205,000 after | Recovery used existing replay capacity | Avoided about 14 duplicated engineer-weeks |
| Security/residency | EU payloads stay in approved EU regions | Evidence preserved in region | Tenant identifier is mandatory |
| Personal contribution | Design, math, gates, rollout | Command, priorities, communication | Contract, workshops, first adapter |
| Rejected alternative | Global plane or account per tenant | Direct aggregate patch | Immediate forced schema |
| Mistake | Synchronous control-plane dependency | Unsupported 60-minute forecast | Called domain variation technical debt |

## Questions I Want to Receive

1. How did you calculate 504,000 events per second, and what traffic shape could invalidate it?
2. What does effectively exactly once mean at each storage boundary?
3. How did you prove European Union failover stayed compliant during a full regional outage?
4. Why was a 103-minute incident acceptable against a 60-minute recovery objective?
5. How did you prevent compatibility adapters from becoming permanent?
6. Which metric would tell you that tenant isolation is failing before an SLO breach?
