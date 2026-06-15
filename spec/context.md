# DataPipelineOverlay — Context (Concept Doc)

> System2 Gate 1 artifact (scope, goals, constraints, open questions). Drafted from
> `../research/airflow-mldata-best-practices.md`. **Status: draft for review.**

## 1. Problem & motivation

Data pipeline work fails in slow, expensive ways: non-idempotent jobs that corrupt on
re-run, cron schedules firing on absent data, "orchestrators" doing heavy compute they
shouldn't, undocumented sources of truth, and — for ML — silent train/eval leakage and
training/serving skew that surface only after a model is in production. These are exactly
the System-1 failure modes System2 is built to prevent, but System2's base pipeline has no
data-pipeline domain knowledge.

**DataPipelineOverlay** specializes System2 for building and operating data pipelines with
**Apache Airflow (OSS)**, across two connected workloads:

- **(A) ELT/ETL** — ingestion, transformation, loading orchestrated as Airflow DAGs.
- **(B) Labeled-data delivery for ML** — scheduling and delivering versioned, labeled
  datasets into ML **experimentation, validation, and evaluation** loops.

## 2. What this overlay is — and isn't

- It is an **additive-only** System2 overlay: it injects principles, gate consultations,
  per-agent guidance, required spec sections, advisory sources, and verification checks. It
  removes no System2 capability.
- It is **advisory**: guidance composed into the orchestrator's `CLAUDE.md` and agent
  prompts. It does not execute pipelines or ship a runtime.
- It is **not** an Airflow distribution, a dbt/Spark replacement, or a managed platform.

## 3. Users & primary use cases

- **Data/ML engineers** using System2 + Claude Code to author Airflow DAGs and dataset
  deliverables.
- Use cases: author a new ELT/ETL DAG; migrate cron→data-aware scheduling; stand up a
  governed canonical dataset; build a reproducible training-set pipeline with leakage-safe
  splits; schedule delivery of a versioned "golden" eval set into a validation/eval loop.

## 4. Scope (v1 = both A and B)

**In scope**
- DAG authoring discipline: idempotency, deterministic/templated dates, parse-time hygiene.
- Scheduling: **Airflow 3 Assets / data-aware scheduling** (producer/consumer `outlets` /
  `schedule=[Asset]`), asset *watchers* for event-driven DAGs, no-execution-date ML DAGs.
- Orchestration-vs-compute boundary (offload heavy work to dbt/Spark/warehouse).
- Layered data-quality checks; lineage via **OpenLineage**; medallion (bronze/silver/gold)
  and canonical/semantic layering; data contracts.
- ML-data delivery: dataset versioning & reproducibility; train/val/test(+holdout) split
  discipline and **leakage avoidance via point-in-time correctness**; golden eval-set
  definition and scheduled delivery; experiment/registry integration (e.g. MLflow).
- Governance: canonical single-source datasets, governed semantic layer, **provenance on
  every delivered artifact**.

**Out of scope (v1)**
- Non-Airflow orchestrators (Dagster/Prefect/Flyte) — possible future overlays.
- Heavy prescriptions for a specific warehouse/engine vendor.
- Real-time streaming systems beyond Airflow's event-driven asset triggers.
- Closed-source / managed-only features (kept OSS-first per project direction).

## 5. Goals

G1. Make the **idempotent, data-aware, orchestrator-not-engine** pattern the default an
agent reaches for.
G2. Make **governance first-class**: canonical datasets, a semantic-layer interface, and
provenance on outputs — modeled on Anthropic's governed self-service analytics.
G3. For ML, make **leakage and skew failure modes explicit and tested**, not assumed away
by tooling.
G4. Encode lineage (OpenLineage) and layered data-quality as expected, gate-checked steps.
G5. Stay faithful to System2: spec-driven, gate-checked, verification-first; additive,
advisory, composable.

## 6. Non-goals

- Not maximizing ceremony — guidance scales to blast radius (a throwaway exploratory DAG ≠
  a production canonical dataset).
- Not re-teaching System2 mechanics inside contributions.
- Not asserting any tool *eliminates* a failure mode (see Constraint C4).

## 7. Domain concepts the overlay encodes (Airflow 3 default, 2.x-aware)

- **Data-aware scheduling / Assets** (Airflow 3). 2.x note: the predecessor is **Datasets**;
  asset *watchers* / event-driven triggers are 3.x-only — call this out where it differs.
- **Orchestrator vs. compute engine** — Airflow coordinates; dbt/Spark/warehouse compute.
- **Idempotency & re-run safety** — engineered via templated intervals + overwrite-by-
  partition; *not* assumed from Airflow DAG-versioning (see C4).
- **Governed semantic layer + canonical, single-source-of-truth datasets + provenance.**
- **Lineage** — OpenLineage provider + listener.
- **Point-in-time correctness** — the core training-data leakage defense.
- **Golden / eval sets** — versioned, provenance-stamped, human-reviewed; delivered on a
  schedule into validation/eval loops.

## 8. Intended contributions (concept-level — detailed in design.md)

Derived from "what good looks like" in the research; final form decided at design/tasks.

- **Orchestrator principles:** "Airflow orchestrates; engines compute"; "Data-aware over
  time-aware"; "Govern the interface, not just the data."
- **Gate consultations:** *Gate 1* — canonical-dataset/semantic-layer reuse vs. new source
  of truth; data-aware vs. time-aware trigger. *Gate 3* — idempotency/re-run strategy,
  orchestration/compute boundary, lineage emission; (ML) point-in-time correctness and
  split/leakage strategy.
- **Required spec sections** (per DAG / dataset deliverable): idempotency & backfill;
  orchestration-vs-compute boundary; layered data-quality; lineage/provenance; (ML) split
  discipline + point-in-time correctness + eval/golden-set definition + reproducibility/
  versioning.
- **Verification checks** (test-engineer / reviewer): no time-dependent top-level DAG code;
  tasks idempotent; layered DQ present; lineage emitted; (ML) no train/eval leakage,
  point-in-time joins used, **train/serving skew explicitly tested**, eval set versioned +
  provenance.
- **Advisory source(s) / auxiliary agent:** likely a "pipeline-scout" auxiliary agent and/or
  advisory source for Airflow/asset/lineage facts (TBD in design).

## 9. Constraints & assumptions

- **C1.** Additive-only and advisory-only (overlay schema; composes via `/system2:compose`).
- **C2.** **Airflow 3 is the default idiom; note 2.x equivalents** (Datasets vs Assets) where
  they differ. Don't assume 3.x-only features (watchers) exist in 2.x.
- **C3.** OSS-first: Airflow + OSS ecosystem (dbt, Spark, OpenLineage, Feast, MLflow,
  DVC/LakeFS/Iceberg). No dependence on managed-only features.
- **C4. Honor the refutations (do not overclaim):**
  - A feature store (Feast) **does not prevent** training/serving skew — it helps; skew must
    be tested. (refuted 0-3)
  - Native SQL check operators are the **default** DQ approach; GE/Soda/dbt are *situational*,
    not the blanket recommendation. (refuted 1-2)
  - Airflow DAG-versioning does **not** guarantee deterministic replay of old code; re-run
    safety is engineered. (refuted 1-2)
- **C5.** Contribution-ID prefix `dp-`; content files plain Markdown; summaries must match
  content (System2 overlay conventions).

## 10. Dependencies

- **System2** (must be installed; overlay patches it).
- A **target project** doing Airflow data-pipeline work.
- Conceptual references: OpenLineage, Feast, MLflow, dbt, Spark, DVC/LakeFS/Iceberg (named in
  guidance, not bundled).

## 11. Risks

- **R1.** Over-prescription → ceremony theatre; mitigate with blast-radius-proportional
  guidance (Non-goal).
- **R2.** Airflow 3 vs 2.x drift in idioms → mitigate via explicit version notes (C2).
- **R3.** Tooling churn (feature stores, versioning tools) dates the guidance → keep tool
  choices advisory and principle-led, not hard-coded.
- **R4.** Scope (A+B) is broad for v1 → manage via clear required-section separation and
  phased contribution authoring.

## 12. Open questions (carry into requirements)

1. Airflow 3 DAG-versioning: what does it actually guarantee vs. what we must engineer?
2. Dataset-versioning tool of record: DVC vs LakeFS vs Delta/Iceberg time-travel vs HF?
3. DQ results aggregation + OpenLineage facets — standardize how?
4. Training/serving skew mitigation beyond point-in-time joins?
5. Golden eval-set delivery cadence + MLflow registry integration pattern?
6. Auxiliary agent vs. advisory source (or both) for Airflow/lineage facts?

## 13. Success criteria / Definition of Done (for the overlay)

- Composes cleanly against a local System2 (`/system2:compose`) and passes smoke tests.
- Encodes G1–G5 as concrete, non-overlapping contributions with `dp-` IDs.
- A test DAG / dataset deliverable authored *with* the overlay visibly exhibits: idempotency,
  data-aware scheduling, orchestration/compute separation, layered DQ, lineage, and (for ML)
  leakage-safe splits with provenance — and the verification checks catch their absence.
- No overclaims (C4 respected); guidance is blast-radius-proportional.
