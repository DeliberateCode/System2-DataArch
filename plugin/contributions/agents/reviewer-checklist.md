# Data-pipeline review criteria

Flag the following as non-conformant when reviewing pipeline and ML-data changes, and explain the expected pattern:

- **In-task heavy compute.** A task that pulls large data into the worker to transform it instead of pushing compute to an engine. Expected: orchestrate and verify; compute in dbt/Spark/the warehouse.

- **Missing provenance or lineage.** A delivered artifact without an artifact-level provenance stamp, or a tracked dataset without OpenLineage emission.

- **DAG-versioning-as-replay claims.** Any claim (in code, comments, or docs) that Airflow DAG-versioning guarantees deterministic replay or re-run safety. Expected: re-run safety is engineered via idempotency and pinned task code.

- **Blanket data-quality framework framing.** Treating Great Expectations, Soda, or dbt tests as the blanket/default data-quality approach. Expected: native SQL check operators by default; third-party frameworks are situational.

- **Feature-store-prevents-skew overclaims.** Any claim that a feature store prevents or eliminates train/serving skew, or that it removes the need to test skew. Expected: skew is tested explicitly; a feature store is an aid, not a guarantee.
