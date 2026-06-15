# Research notes — Airflow data pipelines + ML labeled-data delivery (best practices, 2025–2026)

_Inputs for the DataPipelineOverlay concept doc (`spec/context.md`). Produced 2026-06-14 by
the deep-research harness: 5 angles → 24 sources fetched → 114 claims → 25 adversarially
verified (3-vote; need 2/3 to kill). **21 confirmed, 4 killed.** Claims are tagged
**[VERIFIED]** (survived 3-0), **[CONTESTED]** (killed — do NOT rely on), or **[UNVERIFIED]**
(well-known practice, not put through this pass — flagged for the requirements stage)._

---

## Scope A — ELT/ETL with Airflow

### Scheduling & DAG design
- **[VERIFIED] Airflow 3 "Assets" generalize datasets; scheduling is data-aware, not just cron.**
  Producers declare `outlets=[Asset(...)]`; consumers set `schedule=[Asset(...)]` and run when
  upstream assets update (producer/consumer pattern). Prefer asset/data-aware scheduling over
  time-based cron when a job's real trigger is "new data exists." _(airflow.apache.org, astronomer.io)_
- **[VERIFIED] Airflow 3 adds "Asset watchers" for event-driven pipelines** (e.g. trigger on a
  queue/message). Caveat surfaced in verification: watchers **poll**, so "real-time" means
  low-latency, not instantaneous. _(astronomer.io, airflow.apache.org)_
- **[VERIFIED] Airflow 3 supports non-scheduled / no-execution-date paradigms** — useful for ML
  DAGs (inference, on-demand training) that aren't tied to a data interval. _(datacamp, astronomer.io)_
- **[VERIFIED] DAGs must be idempotent** — re-running the same DAG/interval produces the same
  result (use deterministic, templated dates; overwrite-by-partition, not blind append). _(astronomer.io)_
- **[VERIFIED] DAG files must avoid time-dependent / heavy dynamic code at parse time** — no
  `datetime.now()` driving structure, no network/DB calls at module top level; the scheduler
  re-parses files constantly. _(astronomer.io)_
- **[CONTESTED — killed 1-2] "Airflow 3 DAG versioning enables deterministic re-runs with the
  exact old code after changes."** DAG versioning exists and tracks which version ran, but the
  strong "deterministic replay of historical code" claim did not survive. Treat re-run
  determinism as something *you* must engineer (idempotency + pinned task code), not a free
  platform guarantee. → open question.
- **[CONTESTED — killed 1-2] "Airflow only registers asset updates from Airflow tasks/API/UI
  (can't see external updates)."** Overstated as a hard limit — Airflow 3 asset watchers /
  external events broaden this. Don't design around the limitation as stated; verify against
  current docs.

### Orchestration vs. compute boundary
- **[VERIFIED] Airflow is an orchestrator, not a compute engine.** Heavy/large data processing
  should be offloaded to Spark/dbt/the warehouse; Airflow coordinates and tracks, it does not
  crunch data in-process. This is the single most-repeated principle. _(astronomer.io, apache)_

### Data quality, contracts, lineage
- **[VERIFIED] Data-quality checks should be layered** (e.g. column/table SQL checks inline in
  the DAG, plus broader suite checks) rather than a single end-of-pipeline gate. _(astronomer.io)_
- **[VERIFIED] Astronomer recommends native SQL check operators** (`SQLColumnCheckOperator`,
  `SQLTableCheckOperator`, etc.) as the default for in-DAG checks. _(astronomer.io)_
- **[CONTESTED — killed 1-2] "Great Expectations / Soda / dbt tests are *the* recommended choice
  for centralized DQ results."** The blanket recommendation was refuted — native SQL checks are
  the default; third-party DQ frameworks are an option when you need a results store / richer
  expectations, not a universal prescription. Frame as "choose per need," not "use GE/Soda/dbt."
- **[VERIFIED] OpenLineage is the open-source industry-standard for lineage; Airflow integrates
  via two components** (the OpenLineage provider + a listener) to emit run/dataset lineage
  automatically. _(openlineage.io, astronomer.io)_
- **[UNVERIFIED] Medallion (bronze/silver/gold) layering, explicit data contracts, secrets via a
  secrets backend, dynamic task mapping, retries/SLAs/alerting, CI/CD for DAGs** — standard and
  expected, but not run through this verification pass. Carry into requirements with sources to
  confirm (soda.io data-contracts-in-CI, astronomer secrets-management were fetched).

## Scope B — Labeled-data delivery for ML (experimentation / validation / evaluation)

- **[VERIFIED] Point-in-time correctness is the core leakage defense.** Feast retrieves
  point-in-time-correct historical features (as-of-event joins), preventing future information
  bleeding into training rows. Make point-in-time joins a required practice for any
  training-set build. _(feast.dev)_
- **[CONTESTED — killed 0-3, unanimous] "Feast *prevents* training-serving skew by guaranteeing
  identical logic in both paths."** Strongly refuted. A feature store *helps* (shared
  definitions, online/offline retrieval) but does **not** by itself guarantee no skew — skew
  must be actively tested. Do not claim a tool eliminates skew.
- **[VERIFIED] Governed "golden"/canonical datasets + provenance are the trust mechanism** (see
  cross-cutting). For ML eval specifically, golden eval sets with human-in-the-loop review
  queues and drift watch are the documented pattern. _(getmaxim.ai, kinde.com — both blog-tier)_
- **[UNVERIFIED] Dataset versioning & reproducibility tooling (DVC, LakeFS, Delta/Iceberg time
  travel, HF datasets), train/val/test split discipline, MLflow registries, HITL labeling
  orchestration, drift monitoring** — fetched (lakefs.io, astronomer airflow-mlops/ml-datasets)
  but not individually verified. High-priority to confirm at requirements time. lakeFS + MLflow
  + Airflow is a recurring real-world stack for git-like data versioning in MLOps.

## Cross-cutting — governed platform & harness framing (the System2 fit)

- **[VERIFIED] Anthropic's governed self-service analytics = three pillars:** (1) a **governed
  semantic layer** as the canonical interface between users and raw data; (2) a **small set of
  canonical, single-source-of-truth datasets** (not sprawl); (3) **a provenance footer on every
  response** (what data/queries produced it). ~95% analytics accuracy is attributed to this
  governance, not model cleverness. This is the template for "what good looks like." _(claude.com)_
- **[VERIFIED] OpenAI's "harness engineering" thesis: invest in the engineering harness, not
  prompts** — specs, feedback loops, mechanically enforced constraints, and **repository-local,
  versioned artifacts** (code, markdown, linters) as the durable substrate. Directly mirrors
  System2's spec-driven, gate-checked philosophy. _(openai.com — URL 403'd but corroborated by
  infoq.com)_
- **[VERIFIED] Repository-local, versioned artifacts** (specs/markdown/config in the repo) are
  the recommended substrate for agent + pipeline reliability. _(openai.com / infoq.com)_
- Seed (Saucedo ML-Engineer #391): curated ecosystem `EthicalML/awesome-production-machine-learning`
  (20k★) for tool selection; reinforces governed-data + harness themes. _(linkedin.com — blog-tier)_

---

## What "good" looks like → seeds for the concept doc

These translate the verified findings into candidate **overlay contributions** (to be refined in
`spec/context.md` and the requirements stage):

**Candidate orchestrator principle(s)**
- "Airflow orchestrates; engines compute." Push heavy transforms to dbt/Spark/warehouse; DAGs
  coordinate, validate, and emit lineage.
- "Data-aware over time-aware." Default to asset/dataset scheduling when the trigger is data
  arrival; reserve cron for genuinely time-driven work.
- "Govern the interface, not just the data." A canonical/semantic layer + a small set of
  single-source-of-truth datasets + provenance on every delivered artifact.

**Candidate gate consultations**
- *Gate 1 (context):* is there an existing canonical dataset / semantic-layer entity for this,
  or are we forking a new source of truth? Is the trigger data-aware or time-aware?
- *Gate 3 (design):* idempotency & re-run strategy; orchestration/compute boundary; lineage
  emission (OpenLineage); for ML — point-in-time correctness and split/leakage strategy.

**Candidate required spec sections (per DAG / dataset deliverable)**
- Idempotency & backfill strategy · Orchestration-vs-compute boundary · Data-quality checks
  (layered) · Lineage/provenance · (ML) split discipline + point-in-time correctness + eval/golden
  set definition + reproducibility/versioning.

**Candidate verification checks (test-engineer / reviewer)**
- DAG parses with no time-dependent top-level code; tasks idempotent; data-quality checks
  present and layered; lineage emitted; (ML) no train/eval leakage, point-in-time joins used,
  train/serving skew explicitly tested (NOT assumed from a feature store), eval set versioned
  with provenance.

## Open questions (carry into requirements)
1. DAG-version deterministic re-runs — what does Airflow 3 actually guarantee vs. what we engineer?
2. Dataset-versioning tool of record: DVC vs LakeFS vs Delta/Iceberg time-travel vs HF datasets?
3. DQ results aggregation + OpenLineage facets — how to standardize?
4. Training/serving skew mitigation beyond point-in-time joins?
5. Golden eval-set delivery cadence + MLflow registry integration?

## Sources (by tier)
**Primary:** airflow.apache.org (asset-scheduling); astronomer.io (data-quality, Airflow-3 assets webinar); feast.dev; claude.com (Anthropic self-service analytics); openai.com (harness-engineering).
**Secondary:** astronomer.io (dag-best-practices, airflow-datasets, openlineage, airflow-mlops, ml-datasets use-case); datacamp.com (Airflow 3.0); zenml.io; infoq.com; github.com/EthicalML/awesome-production-machine-learning.
**Blog/▼lower-confidence:** soda.io (data contracts in CI/CD), lakefs.io (×2), getmaxim.ai (golden datasets), kinde.com (HITL evals), medium.com, linkedin.com (Saucedo #391).
**Flagged unreliable:** encord.com (train/val/test — 0 usable claims).
