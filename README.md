# System2-DataArch

The **`data-pipeline`** overlay — a [System2](https://github.com/DeliberateCode/System2) overlay for **data pipeline
engineering with Apache Airflow** (open source). It specializes System2's spec-driven,
gate-checked, verification-first pipeline for two related workloads:

1. **ELT/ETL jobs** — ingestion, transformation, and loading orchestrated as Airflow DAGs.
2. **Labeled-data delivery for ML cycles** — scheduling and delivering versioned, labeled
   datasets for experimentation, validation, and evaluation in ML engineering.

> **Status: in design.** This repo was scaffolded from
> [System2-OverlayTemplate](https://github.com/DeliberateCode/System2-OverlayTemplate) as a
> live exercise of the template. The `plugin/contributions/` files are still the template's
> **placeholders** — they will be replaced once the concept doc is approved. Do not compose
> this overlay into a real project yet.

## What a System2 overlay is

An overlay is an **additive-only** extension that injects domain guidance into System2's
13-agent pipeline at declared anchor points (orchestrator principles, gate consultations,
per-agent prompt sections, required spec sections, advisory sources, auxiliary agents, MCP
servers, permissions). It never removes capability. Compose with `/system2:compose`.

## This repo's layout

```
plugin/                  # The installable overlay (manifest + contributions) — see CLAUDE.md
  system2.overlay.json   # Overlay manifest (rebranded; contributions still placeholder)
  contributions/         # Per-anchor guidance (TO BE WRITTEN from the concept doc)
spec/                    # System2 spec artifacts for building THIS overlay
  context.md             # The concept doc (driven by research/) — forthcoming
research/                # Best-practice research notes that drive the concept doc
```

## Roadmap

1. **Research** — survey current best practices for Airflow-based ELT/ETL and labeled-data
   delivery for ML exp/val/eval. → `research/`
2. **Concept doc** — distill research into a System2 context/scope doc. → `spec/context.md`
3. **Contributions** — translate the concept into overlay contributions (principles, gate
   checks, agent guidance, required spec sections, advisory sources). → `plugin/contributions/`
4. **Validate** — compose against a local System2 and run the smoke tests.

## Domain focus

- **Orchestrator:** Apache Airflow (OSS) — DAG authoring, scheduling, backfills, retries,
  idempotency, data-aware scheduling (datasets/assets).
- **Modeling:** ELT/ETL patterns, lineage, semantic/canonical layers, data contracts, tests.
- **ML data delivery:** dataset versioning, labeling workflows, train/val/eval splits,
  reproducibility, and the experimentation/validation/evaluation loop.

## Prerequisites (once contributions are real)

This is an overlay — it patches an existing System2 installation.

```
/plugin marketplace add DeliberateCode/System2
/plugin install system2@system2-marketplace
```
