At design, prompt the design-architect to make these decisions explicit before delegating implementation:

1. **Idempotency / re-run strategy.** How are tasks made idempotent and re-run/backfill safe (templated intervals, overwrite-by-partition, no blind append)? Re-run safety must be engineered through idempotency and pinned task code — do not assume Airflow DAG-versioning provides deterministic replay.

2. **Orchestration-vs-compute boundary.** What does the DAG coordinate versus what does an engine compute? Confirm heavy compute is pushed down.

3. **Lineage emission.** Where is OpenLineage run/dataset lineage emitted, and what provenance is stamped on delivered artifacts?

4. **(ML scope only) Point-in-time correctness and split/leakage strategy.** If the deliverable is a training/eval dataset, how are feature/label joins kept point-in-time, and how are splits kept leak-safe? These prompts apply only when the work is in ML-data scope.
