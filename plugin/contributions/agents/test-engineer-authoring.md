# Data-pipeline test authoring rules

When writing tests for pipelines and data deliverables, assert these properties:

- **Idempotent re-run.** A test that runs a task twice for the same logical interval and asserts the output is unchanged (overwrite-by-partition, not duplicated rows).

- **Leak-safe splits.** A test that asserts train/val/test splits are disjoint and that no leakage path exists across split boundaries.

- **Eval-set version and provenance.** A test that asserts the eval/golden set carries a version identifier and provenance (sources, queries, versions).

- **Dataset reproducibility / identifiability.** A test that asserts a delivered dataset can be identified and reproduced from its recorded version and provenance.
