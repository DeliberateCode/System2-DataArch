# Data-pipeline implementation discipline

When implementing Airflow tasks and data deliverables:

- **Make tasks idempotent.** Key writes to the templated logical interval and overwrite by partition; never blind-append. Re-running a task for the same interval must converge to the same result. This is how re-run safety is achieved — not by relying on Airflow DAG-versioning.

- **Offload heavy compute.** Do not pull large datasets into the worker to transform them. Push set-based transformation to the engine (dbt, Spark, the warehouse) and let the task submit, wait, and verify.

- **Use native SQL check operators by default.** Implement data-quality checks as native SQL check operators layered through the pipeline. Reach for Great Expectations, Soda, or dbt tests only when a situation specifically calls for them, not as the default.

- **Non-interval ML DAGs: no-execution-date paradigm.** For ML DAGs whose runs are not tied to a data interval, use the no-execution-date paradigm (manual/asset-triggered runs without an interval semantic) rather than forcing a cron interval that has no meaning.

- **A feature store is not a skew guarantee.** If a feature store is used, treat it as a consistency aid only. It does not prevent train/serving skew — skew must still be tested explicitly. Do not implement code or comments that claim the feature store removes the need for skew testing.
