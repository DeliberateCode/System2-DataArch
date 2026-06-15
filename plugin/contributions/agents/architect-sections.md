# Required design sections for data deliverables

For shared, canonical, or production deliverables, spec/design.md should cover these per-deliverable sections. Tier the depth to blast radius — throwaway work needs far less.

**Always (Scope A and cross-cutting):**
- **Idempotency & Backfill** — re-run/backfill strategy via templated intervals and overwrite-by-partition (engineered, not from DAG-versioning).
- **Orchestration-vs-Compute Boundary** — what the DAG coordinates versus what an engine computes.
- **Layered Data-Quality** — checks layered through the pipeline (native SQL check operators by default; third-party frameworks situational), not a single terminal gate.
- **Lineage & Provenance** — OpenLineage run/dataset emission plus an artifact-level provenance stamp.

**Additionally for ML-data deliverables (Scope B):**
- **Split Discipline & Point-in-Time Correctness** — train/val/test (and optional holdout) discipline; point-in-time feature/label joins as the leakage defense.
- **Eval/Golden-Set Definition** — golden/eval set definition, versioning, provenance, and human review.
- **Reproducibility & Versioning** — how the dataset is versioned and reproduced (candidate tools advisory; none mandated).

These section headings mirror the overlay's required spec sections so the design and requirements artifacts stay aligned.
