# Data-pipeline design constraints

Apply these constraints when designing Airflow DAGs and data deliverables:

- **Idempotent by default.** Design every task so re-running it for the same logical interval produces the same result: use templated execution intervals and overwrite-by-partition rather than blind append. Re-run and backfill safety is an engineered property of the design — do not attribute it to Airflow DAG-versioning. DAG-versioning records which DAG structure ran; it does not guarantee deterministic replay of data.

- **Data-aware by default.** When the trigger is "new data exists," design for asset/data-aware scheduling (Airflow 3 `outlets`/`schedule=[Asset]`; Datasets on 2.x) instead of cron. Reserve cron for genuinely time-driven work.

- **Keep compute out of the orchestrator.** The DAG coordinates, validates, and emits lineage; heavy or large-scale transformation belongs in an engine (dbt, Spark, the warehouse). Name engines as examples; the design should not mandate a specific tool.

- **Scale ceremony to blast radius.** A throwaway or exploratory DAG needs only lightweight guidance. Full per-deliverable sections, layered DQ, and provenance are warranted for shared, canonical, or production deliverables. Do not impose heavy ceremony on low-value, short-lived work.

- **Tools advisory, principles led.** Where a tool is named (OpenLineage, dbt, Spark, Feast, MLflow, DVC, LakeFS, Iceberg), treat it as an advisory example serving a principle, never as a required dependency.
