# Data-pipeline self-verification

After implementing, self-check before reporting completion:

- **Parse-time hygiene.** No time-dependent values (e.g., `datetime.now()`) and no heavy work (large queries, data pulls, network calls) execute at DAG parse time. Such work belongs inside task callables that run at execution time, not in top-level module code.

- **Lineage present.** OpenLineage run/dataset emission is wired for the tasks that produce or consume tracked datasets.

- **Point-in-time training joins.** For training-data work, feature and label joins are point-in-time correct (no future information leaks into a row's features relative to its label timestamp).
