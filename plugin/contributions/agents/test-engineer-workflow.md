# Data-pipeline verification workflow

Add the following advisory checks. Each is non-blocking by default and carries a declared severity (`info`, `warn`, or `block-candidate`) that a host may opt into enforcing. Emit findings in the shape `{check_id, severity, location, rationale, fix_hint}`.

**Scope A and cross-cutting:**
- `dp-parse-time-hygiene` (severity: warn) — no time-dependent or heavy work at DAG parse time. *fix_hint:* move it into task callables.
- `dp-layered-dq-present` (severity: warn) — data-quality checks are layered through the pipeline, not concentrated in one terminal gate. *fix_hint:* add per-stage native SQL checks.
- `dp-lineage-emitted` (severity: warn) — OpenLineage run/dataset emission is present for tracked datasets. *fix_hint:* wire lineage on producing/consuming tasks.

**Scope B (ML-data):**
- `dp-no-train-eval-leakage` (severity: block-candidate) — no record or feature leaks across train/eval split boundaries. *fix_hint:* enforce disjoint, leak-safe splits.
- `dp-point-in-time-joins` (severity: block-candidate) — feature/label joins are point-in-time correct. *fix_hint:* join on as-of timestamps.
- `dp-skew-tested` (severity: warn) — train/serving skew is explicitly tested. A feature store does NOT satisfy this check; skew must be tested directly. *fix_hint:* add a test comparing training-time and serving-time feature computation.

Notes: keep all checks advisory/non-blocking by default. DQ-results aggregation and OpenLineage facet standardization are TBD; the skew-must-be-tested check holds regardless of any feature store in use.
