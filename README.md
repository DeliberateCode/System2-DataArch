# System2-DataArch

The **`data-pipeline`** overlay — a [System2](https://github.com/DeliberateCode/System2) overlay for **data pipeline
engineering with Apache Airflow** (open source). It specializes System2's spec-driven,
gate-checked, verification-first pipeline for two related workloads:

1. **ELT/ETL jobs** — ingestion, transformation, and loading orchestrated as Airflow DAGs.
2. **Labeled-data delivery for ML cycles** — scheduling and delivering versioned, labeled
   datasets for experimentation, validation, and evaluation in ML engineering.

> **Status: ready for testing.** Built spec-driven through the System2 gates (context →
> requirements → Gate-3-approved design → tasks). The `plugin/contributions/` are **real,
> authored content** — 26 `dp-` contributions (3 orchestrator principles, Gate 1 + Gate 3
> consultations, 11 agent prompt sections across 6 pipeline agents, 8 required spec
> sections, 1 advisory source, 1 read-only auxiliary agent), all additive and advisory.
> The overlay composes against a local System2 with the smoke suite green (14/14). The
> remaining work is **Gate-6 validation** (dry-run compose review, negative-content scan,
> reference-DAG/-deliverable exercises) — so exercise it in a scratch project, and treat it
> as pre-1.0 until validation closes.

## What a System2 overlay is

An overlay is an **additive-only** extension that injects domain guidance into System2's
13-agent pipeline at declared anchor points (orchestrator principles, gate consultations,
per-agent prompt sections, required spec sections, advisory sources, auxiliary agents, MCP
servers, permissions). It never removes capability. Compose with `/system2:compose`.

## This repo's layout

```
plugin/                  # The installable overlay (manifest + contributions) — see CLAUDE.md
  system2.overlay.json   # Overlay manifest — 26 dp- contributions across the anchor points
  contributions/         # Per-anchor guidance (authored; principles, gates, agent + spec sections)
spec/                    # System2 spec artifacts for building THIS overlay
  context.md             # The concept doc (driven by research/)
research/                # Best-practice research notes that drove the concept doc
```

## Roadmap

1. ✅ **Research** — surveyed current best practices for Airflow-based ELT/ETL and
   labeled-data delivery for ML exp/val/eval. → `research/`
2. ✅ **Concept doc** — distilled research into a System2 context/scope doc. → `spec/context.md`
3. ✅ **Contributions** — translated the concept into 26 overlay contributions (principles,
   gate consultations, agent guidance, required spec sections, advisory source, auxiliary
   agent). → `plugin/contributions/`
4. 🔄 **Validate** — composes against a local System2 with the smoke suite green (14/14);
   Gate-6 validation (dry-run review, negative-content scan, reference exercises) in progress.

## Domain focus

- **Orchestrator:** Apache Airflow (OSS) — DAG authoring, scheduling, backfills, retries,
  idempotency, data-aware scheduling (datasets/assets).
- **Modeling:** ELT/ETL patterns, lineage, semantic/canonical layers, data contracts, tests.
- **ML data delivery:** dataset versioning, labeling workflows, train/val/eval splits,
  reproducibility, and the experimentation/validation/evaluation loop.

## Prerequisites

This is an overlay — it patches an existing System2 installation.

```
/plugin marketplace add DeliberateCode/System2
/plugin install system2@system2-marketplace
```
