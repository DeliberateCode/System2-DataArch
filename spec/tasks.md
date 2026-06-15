# DataPipelineOverlay — Tasks

> System2 Gate-4 artifact. Derived from the APPROVED `spec/design.md` (Gate-3, 26 contributions),
> `spec/requirements.md` (41 EARS reqs), `spec/context.md` (Gate-1), and the companion artifacts
> `spec/interfaces.json` / `spec/module-boundaries.json`. **Status: ready for execution.**
>
> Scope reminder: the "system" being built is **the overlay itself** — an additive, advisory
> content+manifest artifact composed into a System2 host. No runtime. Every task preserves the
> additive-only / advisory-only invariants (REQ-DP-001/002) and the blast-radius-proportionality
> principle (REQ-DP-006/007/095).
>
> Repo facts confirmed by inspection (2026-06-14):
> - The overlay currently still carries the template's PLACEHOLDER content (`tmpl-` IDs, 13-agent
>   manifest, `template-scout` agent, `post-edit-check.py` hook, `mcp_servers`, `permissions`,
>   4 spec artifacts). Tasks below replace/remove these to reach the 26 `dp-` contributions.
> - The smoke test mirrored from the template asserts `tmpl-` prefix, all-13-agent coverage,
>   full-anchor coverage, all-four-spec-artifact coverage, hook presence, mcp/permissions presence,
>   and `[Your domain]`/`overlay-template` output markers — all of which must be retargeted.
> - System2 must be cloned at `../System2`; the composer is read from
>   `../System2/plugin/scripts/composer.py` and schema/anchor-map from `../System2/plugin/schemas/`.

---

## Task Graph Overview

Six groups, executed roughly in order; content tasks (Group 2) are highly parallelizable once the
manifest skeleton (Group 1) exists.

```
G1 Manifest scaffolding ──┬─> G2 Content files (parallel fan-out, 21 files) ──┐
   (TASK-001..002)        │      (TASK-003..023)                              │
                          └─> G3 Advisory source + aux agent ─────────────────┤
                                 (TASK-024..025)                              │
G4 Remove template residue (TASK-026..028) ──────────────────────────────────┤
                                                                             │
G5 Smoke-test retarget (TASK-029..031) <── depends on G1..G4 ────────────────┤
                                                                             │
G6 Validation (TASK-032..037) <── depends on ALL ────────────────────────────┘
```

**Critical path:** TASK-001 (manifest skeleton) → any/all G2/G3 content tasks → TASK-029/030/031
(smoke retarget) → TASK-032 (smoke pass) → TASK-033 (dry-run compose) → TASK-034 (negative scan) →
TASK-035/036 (reference exercises) → TASK-037 (blast-radius + version-note + gate review). The
manifest and the smoke test are the two serialization points; everything else fans out.

**Contribution accounting (must total 26):** 3 principles + 2 gate consultations + 11 agent
prompt sections + 8 required spec sections + 1 advisory source + 1 auxiliary agent = 26.

**Open-question flags:** tasks that touch OQ-1..6 content are marked `[OQ-n]`. They are *not*
blocked — the design ratified a stance for each (advisory, name-don't-mandate, mark-TBD). The flag
means: keep that content advisory/marked-TBD and re-confirm wording when the OQ closes.

---

## Tasks

### Group 1 — Manifest scaffolding

---

**TASK-001 — Rewrite the manifest skeleton to the 26 `dp-` contributions (structure + IDs + anchors).**
- **Goal:** Replace the template manifest's structure with the real DataPipelineOverlay contribution
  tree: identity block, tags/compatibility, and every `dp-` declaration at its correct anchor with
  `content_file` paths, `inline` flags, `phase`/`after` where applicable. Summaries added in
  TASK-002 (split to keep diffs reviewable). Remove `mcp_servers`, `permissions`, `hooks`, and the
  7 unused agents and 2 unused spec artifacts in this same edit (manifest side of Group 4).
- **Files:** `plugin/system2.overlay.json` (rewrite).
- **Dependencies:** none.
- **Satisfies:** REQ-DP-001, REQ-DP-003, REQ-DP-005; design §"Manifest contract", §"Contribution Map".
- **Steps:**
  1. Set `name: data-pipeline-overlay`, `version`, `schema_version: 1.0.0`,
     `tags: ["data-pipeline","airflow","ml-data","evidence-source"]`,
     `compatibility.review_when_combined_with_tags: ["architecture-policy"]`.
  2. `orchestrator.principles`: 3 entries (`dp-principle-orchestrate-not-compute`,
     `dp-principle-data-aware-over-time-aware`, `dp-principle-govern-the-interface`), all
     `inline: true`, with `after` ordering as designed.
  3. `orchestrator.gates."1".consultation`: `dp-gate1-consultation` (`phase: pre-delegation`);
     `orchestrator.gates."3".consultation`: `dp-gate3-consultation` (`phase: pre-delegation`).
  4. `agents`: exactly 6 agents (design-architect, requirements-engineer, executor, test-engineer,
     code-reviewer, security-sentinel) with the 11 prompt_sections at the anchors in the
     Contribution Map; all `inline: false`. Anchor keys verbatim from `interfaces.json`.
  5. `spec.requirements.required_sections`: 4 entries; `spec.design.required_sections`: 4 entries
     (headings exactly per Contribution Map). No `context`/`tasks` spec entries.
  6. `delegation.advisory_sources`: `dp-airflow-facts` (`resolution: orchestrator-relay`) —
     full detail in TASK-024. `auxiliary_agents`: `dp-pipeline-scout` — full detail in TASK-025.
  7. Do NOT emit `mcp_servers`, `permissions`, or any `agents.*.hooks`/`agents.*.tools` blocks.
- **Verification:** `python3 -c "import json;json.load(open('plugin/system2.overlay.json'))"`
  succeeds; manually confirm 26 unique `^dp-` IDs and that anchor keys match the
  `name`/`signature` strings in `spec/interfaces.json`. (Full schema validation runs in TASK-032.)
- **Rollback:** `git checkout plugin/system2.overlay.json`.
- **Change budget:** max_files 1; max_new_symbols 26 (contribution IDs); interface_policy breaking
  with approval (this IS the approved breaking rewrite of the placeholder manifest).
- **write_lease:**
  - `^plugin/system2\.overlay\.json$`
- **Risk:** Med — single source of truth for compose; anchor-name typos fail loud at TASK-032 but
  block the whole group until fixed.
- **Recommended Mode:** executor.

---

**TASK-002 — Author accurate manifest summaries + spec-section descriptions.**
- **Goal:** Populate the `summary` field for every `inline: false` agent prompt section (11) and the
  `description` field for every required spec section (8), so each accurately reflects its content
  file (REQ-DP-003) and the orchestrator can decide relevance.
- **Files:** `plugin/system2.overlay.json` (edit summaries/descriptions only).
- **Dependencies:** TASK-001 (skeleton must exist). Best authored alongside or after the matching
  content tasks (TASK-003..023) so summary-vs-content drift is zero; if authored first, re-verify
  after content lands.
- **Satisfies:** REQ-DP-003; design §"Summary-vs-content drift" failure mode.
- **Steps:** For each of the 19 non-inline contributions, write a 1–2 sentence summary matching the
  content file's substance (use the Content Design lines in design.md §"Content Design" as the
  basis). Keep summaries free of overclaims (C4) and of System2-mechanics re-teaching (REQ-DP-008).
- **Verification:** `test_summaries_present_for_non_inline` passes (TASK-032); manual
  summary-vs-content diff (the REQ-DP-003 review) finds no drift — this is the dedicated review in
  TASK-033's checklist.
- **Rollback:** `git checkout plugin/system2.overlay.json`.
- **Change budget:** max_files 1; max_new_symbols 0; interface_policy none (field population only).
- **write_lease:**
  - `^plugin/system2\.overlay\.json$`
- **Risk:** Low.
- **Recommended Mode:** executor.

---

### Group 2 — Content files (one task per contribution markdown file)

> All Group-2 files are plain Markdown, no frontmatter (CLAUDE.md convention; module-boundaries.json
> forbids frontmatter in `contributions/`). All honor the C4 negatives: **no** "feature store
> prevents/eliminates skew"; **native SQL DQ as default** (GE/Soda/dbt situational); **DAG-versioning
> ≠ deterministic replay**. All Airflow guidance is **Airflow-3 default with explicit 2.x notes**
> (Assets≈Datasets; watchers 3.x-only). All checks declare a **severity** (`info`/`warn`/
> `block-candidate`) and are advisory/non-blocking. Each task reuses an existing template file path
> where the path matches, overwriting its placeholder body. These 21 tasks are mutually independent
> and can be delegated in parallel once TASK-001 lands.

#### 2a. Orchestrator principles (×3) + gate consultations (×2)

**TASK-003 — Principle: orchestrate-not-compute.**
- **Goal:** Author `dp-principle-orchestrate-not-compute` content (inline): Airflow coordinates,
  validates, emits lineage; push heavy/large compute to dbt/Spark/warehouse.
- **Files:** `plugin/contributions/orchestrator/principle.md` (rewrite/rename per manifest path).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-020, REQ-DP-025; G1.
- **Steps:** Write the principle per design §"Content Design"; keep tools as named examples only
  (REQ-DP-064); no overclaims.
- **Verification:** file non-empty, no injection patterns (TASK-032); content review confirms the
  orchestrator-not-engine framing.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/orchestrator/principle\.md$`

> Note: principles 2 and 3 need distinct files (manifest references three principle content files).
> Create new files `dp-principle-data-aware.md` and `dp-principle-govern-interface.md` (or the paths
> chosen in TASK-001) — keep TASK-001's `content_file` paths and these tasks' paths identical.

**TASK-004 — Principle: data-aware over time-aware. [OQ — none; Airflow-version-sensitive]**
- **Goal:** `dp-principle-data-aware-over-time-aware` (inline): default to asset/data-aware
  scheduling when the trigger is "new data exists"; reserve cron for time-driven work.
- **Files:** `plugin/contributions/orchestrator/dp-principle-data-aware.md` (new; path must match TASK-001).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-021; G1.
- **Steps:** Producer `outlets`, consumer `schedule=[Asset]` (Airflow 3); Datasets equivalent on 2.x
  (REQ-DP-009). No claim that data-aware "eliminates" anything.
- **Verification:** non-empty, no injection; version-note audit (TASK-037) confirms the 2.x note.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/orchestrator/dp-principle-data-aware\.md$`

**TASK-005 — Principle: govern-the-interface.**
- **Goal:** `dp-principle-govern-the-interface` (inline): govern the interface, not just the data —
  canonical/semantic layer, small set of single-source-of-truth datasets, provenance on every
  delivered artifact.
- **Files:** `plugin/contributions/orchestrator/dp-principle-govern-interface.md` (new; path per TASK-001).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-060; G2.
- **Verification:** non-empty, no injection; content names the three governance pillars (REQ-DP-060).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/orchestrator/dp-principle-govern-interface\.md$`

**TASK-006 — Gate-1 consultation.**
- **Goal:** `dp-gate1-consultation`: pre-delegation prompts — is there a canonical dataset/
  semantic-layer entity to reuse, or are we forking a new source of truth? Is the trigger data-aware
  or time-aware?
- **Files:** `plugin/contributions/orchestrator/gate1-consultation.md` (rewrite placeholder body).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-061; G1, G2.
- **Verification:** non-empty, no injection; gate-consultation review (TASK-037) confirms both prompts.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/orchestrator/gate1-consultation\.md$`

**TASK-007 — Gate-3 consultation. [OQ-1]**
- **Goal:** `dp-gate3-consultation`: design-phase prompts — idempotency/re-run strategy;
  orchestration/compute boundary; lineage emission; (ML scope) point-in-time correctness and
  split/leakage strategy.
- **Files:** `plugin/contributions/orchestrator/dp-gate3-consultation.md` (new; path per TASK-001).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-062, REQ-DP-023; G1, G3, G4.
- **Steps:** Attribute re-run safety to engineering (idempotency + pinned task code), never to
  DAG-versioning (REQ-DP-092). ML prompts framed as conditional on scope.
- **Verification:** non-empty, no injection; gate review (TASK-037) confirms all listed prompts;
  negative scan (TASK-034) finds no DAG-versioning-as-replay claim.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low (re-confirm wording when
  OQ-1 closes). **Mode:** executor.
- **write_lease:** `^plugin/contributions/orchestrator/dp-gate3-consultation\.md$`

#### 2b. Agent prompt sections (×11 across 6 agents)

**TASK-008 — design-architect: design constraints. [OQ-1]**
- **Goal:** `dp-architect-design-constraints` (file-pointer): design DAGs/deliverables idempotent +
  data-aware by default; scale ceremony to blast radius; never attribute re-run safety to
  DAG-versioning; keep tools advisory.
- **Files:** `plugin/contributions/agents/architect-constraints.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-006/007, REQ-DP-020, REQ-DP-064, REQ-DP-092.
- **Verification:** non-empty, no injection; negative scan + blast-radius walkthrough (TASK-034/037).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/agents/architect-constraints\.md$`

**TASK-009 — design-architect: required output sections.**
- **Goal:** `dp-architect-required-sections` (file-pointer): for shared/canonical/production
  deliverables, require the per-deliverable sections (idempotency/backfill, compute boundary,
  layered DQ, lineage/provenance; ML: splits, PIT, eval/golden, reproducibility).
- **Files:** `plugin/contributions/agents/architect-sections.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-007, 023, 025, 026, 028, 051, 052, 054, 056, 063.
- **Verification:** non-empty, no injection; high-tier walkthrough demands all sections (TASK-037).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/agents/architect-sections\.md$`

**TASK-010 — requirements-engineer: guardrails. [OQ — none; version + negative sensitive]**
- **Goal:** `dp-requirements-guardrails` (file-pointer): write Airflow guidance in Airflow-3 idiom
  with 2.x notes; tools advisory; never state a tool eliminates a failure mode; native-SQL-default
  for DQ; OSS-first.
- **Files:** `plugin/contributions/agents/requirements-guardrails.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-009, 064, 090..094.
- **Verification:** non-empty, no injection; negative scan (TASK-034) and version audit (TASK-037).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/agents/requirements-guardrails\.md$`

**TASK-011 — requirements-engineer: required req sections. [OQ-2,OQ-5]**
- **Goal:** `dp-requirements-req-sections` (file-pointer): require idempotency/backfill and (ML)
  split, PIT, eval/golden, versioning requirement sections, tier-scoped to blast radius.
- **Files:** `plugin/contributions/agents/requirements-sections.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-007, 023, 050..056.
- **Steps:** Versioning tool-of-record left open (OQ-2); cadence/registry marked TBD (OQ-5).
- **Verification:** non-empty, no injection; tier-scoping confirmed in blast-radius walkthrough.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/agents/requirements-sections\.md$`

**TASK-012 — executor: implementation discipline. [OQ-4]**
- **Goal:** `dp-executor-discipline` (file-pointer): implement idempotent tasks (templated intervals,
  overwrite-by-partition, no blind append); offload heavy compute; native SQL check operators by
  default; non-interval ML DAGs use the no-execution-date paradigm; a feature store is NOT a skew
  guarantee.
- **Files:** `plugin/contributions/agents/executor-discipline.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-020, 023, 025, 027, 053, 058.
- **Verification:** non-empty, no injection; negative scan (TASK-034) finds no skew-prevention claim;
  reference exercises (TASK-035/036).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Med (multiple C4 negatives in one
  file). **Mode:** executor.
- **write_lease:** `^plugin/contributions/agents/executor-discipline\.md$`

**TASK-013 — executor: verification rules.**
- **Goal:** `dp-executor-verification` (file-pointer): self-check after implementing — no
  time-dependent/heavy code at parse time; OpenLineage emission present; training joins are
  point-in-time.
- **Files:** `plugin/contributions/agents/executor-verification.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-024, 028, 051.
- **Verification:** non-empty, no injection; reference-DAG planted-absence check (TASK-035).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/agents/executor-verification\.md$`

**TASK-014 — test-engineer: verification workflow (checks w/ severity). [OQ-3,OQ-4]**
- **Goal:** `dp-test-verification-workflow` (file-pointer): severity-tagged advisory checks —
  parse-time hygiene; layered DQ present (not one terminal gate); lineage emitted; (ML) no
  train/eval leakage, PIT joins used, train/serving skew explicitly tested (NOT assumed from a
  feature store). Each check carries the `{check_id, severity, location, rationale, fix_hint}`
  finding shape and a declared `info`/`warn`/`block-candidate` severity.
- **Files:** `plugin/contributions/agents/test-engineer-workflow.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-024, 026, 028, 051, 052, 090.
- **Steps:** Keep checks advisory/non-blocking by default (design ratified). DQ-results aggregation
  marked TBD (OQ-3); skew-must-be-tested holds regardless (OQ-4).
- **Verification:** non-empty, no injection; reference exercises confirm checks catch planted
  absences (TASK-035/036); negative scan (TASK-034).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Med (the core check surface; most
  REQ traceability). **Mode:** test-engineer.
- **write_lease:** `^plugin/contributions/agents/test-engineer-workflow\.md$`

**TASK-015 — test-engineer: test authoring rules. [OQ-2,OQ-5]**
- **Goal:** `dp-test-authoring-rules` (file-pointer): author tests asserting idempotent re-run,
  leak-safe splits, eval-set version+provenance, dataset reproducibility/identifiability.
- **Files:** `plugin/contributions/agents/test-engineer-authoring.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-023, 050, 054, 056.
- **Verification:** non-empty, no injection; reference-deliverable exercise (TASK-036).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** test-engineer.
- **write_lease:** `^plugin/contributions/agents/test-engineer-authoring\.md$`

**TASK-016 — code-reviewer: review criteria. [OQ-1,OQ-4]**
- **Goal:** `dp-reviewer-criteria` (file-pointer): review for in-task heavy compute, missing
  provenance, DAG-versioning-as-replay claims, GE/Soda/dbt-as-blanket, feature-store-prevents-skew
  overclaims (all non-conformant).
- **Files:** `plugin/contributions/agents/reviewer-checklist.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-025, 027, 063, 090, 091, 092.
- **Verification:** non-empty, no injection; negative scan (TASK-034) and reference exercises.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Med (encodes all C4 negatives as
  review triggers). **Mode:** security-sentinel (review-criteria hardening) or executor.
- **write_lease:** `^plugin/contributions/agents/reviewer-checklist\.md$`

**TASK-017 — code-reviewer: surface-area delta.**
- **Goal:** `dp-reviewer-surface-area` (file-pointer): track governance surface — new sources of
  truth vs. reuse of canonical datasets; medallion/semantic-layer layering, tier-scoped.
- **Files:** `plugin/contributions/agents/reviewer-surface-area.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-029, 060.
- **Verification:** non-empty, no injection; reviewer surface-area review in reference exercises.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/agents/reviewer-surface-area\.md$`

**TASK-018 — security-sentinel: threat model scope.**
- **Goal:** `dp-security-threat-scope` (file-pointer): add data-pipeline threat dimensions —
  secrets-in-DAG vs. secrets backend; PII in lineage/logs; untrusted source data at ingestion
  boundaries.
- **Files:** `plugin/contributions/agents/security-threat-scope.md` (rewrite).
- **Dependencies:** TASK-001.
- **Satisfies:** Security §; REQ-DP-063.
- **Steps:** Secrets-backend practice is flagged source-UNVERIFIED in design §Security — keep
  advisory and confirm the source per the Discovery-Needed item (TASK-037).
- **Verification:** non-empty, no injection; content scan finds no embedded secrets (REQ Security §).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** security-sentinel.
- **write_lease:** `^plugin/contributions/agents/security-threat-scope\.md$`

#### 2c. Required spec sections (×8) — content for the 4 requirements + 4 design sections

> These are descriptions in the manifest (TASK-002) plus, where the design intends authored guidance
> text, companion content. Per `interfaces.json` the required-section public surface is the heading +
> description; if the host renders section bodies from a content file, author one file per section
> using the design §"Content Design — Required spec sections" lines. Confirm with TASK-033 whether
> the composer needs section body files or only heading+description; if only the latter, these
> reduce to TASK-002 description work and TASK-019..023 collapse into no-op confirmations.

**TASK-019 — Requirements sections: idempotency/backfill + compute boundary.**
- **Goal:** Content/descriptions for `dp-req-idempotency-backfill` (templated intervals +
  overwrite-by-partition, engineered NOT from DAG-versioning) and `dp-req-compute-boundary` (what the
  DAG coordinates vs. what the engine computes).
- **Files:** manifest descriptions (TASK-002) and, if needed, section body files under
  `plugin/contributions/spec/`.
- **Dependencies:** TASK-001; TASK-033 decision on body-file need.
- **Satisfies:** REQ-DP-023, 025, 092.
- **Verification:** smoke spec-coverage (TASK-031); reference-DAG exercise (TASK-035).
- **Change budget:** max_files 2; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/spec/dp-req-(idempotency-backfill|compute-boundary)\.md$`

**TASK-020 — Requirements sections: layered DQ + lineage/provenance. [OQ-3]**
- **Goal:** Content/descriptions for `dp-req-layered-dq` (native SQL default; third-party
  situational; not one terminal gate) and `dp-req-lineage-provenance` (OpenLineage emission +
  artifact-level provenance stamp).
- **Files:** manifest descriptions and optional body files under `plugin/contributions/spec/`.
- **Dependencies:** TASK-001; TASK-033.
- **Satisfies:** REQ-DP-026, 027, 028, 063.
- **Steps:** Facet standardization marked TBD (OQ-3). Negative-conformant DQ framing (REQ-DP-091).
- **Verification:** spec-coverage smoke (TASK-031); negative scan (TASK-034); reference exercise.
- **Change budget:** max_files 2; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/spec/dp-req-(layered-dq|lineage-provenance)\.md$`

**TASK-021 — Design section: Split Discipline & Point-in-Time Correctness.**
- **Goal:** Content/description for `dp-design-ml-split-pit`: train/val/test(/holdout) discipline +
  point-in-time correctness as the core leakage defense.
- **Files:** manifest description and optional body file under `plugin/contributions/spec/`.
- **Dependencies:** TASK-001; TASK-033.
- **Satisfies:** REQ-DP-051, 052.
- **Verification:** spec-coverage smoke (TASK-031); reference-deliverable exercise (TASK-036).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/spec/dp-design-ml-split-pit\.md$`

**TASK-022 — Design section: Eval/Golden-Set Definition. [OQ-5]**
- **Goal:** Content/description for `dp-design-eval-golden`: golden/eval-set definition, versioning,
  provenance, human review, delivery cadence (cadence TBD).
- **Files:** manifest description and optional body file under `plugin/contributions/spec/`.
- **Dependencies:** TASK-001; TASK-033.
- **Satisfies:** REQ-DP-054, 055.
- **Steps:** Mark cadence/registry pattern TBD (OQ-5). Drift-watch is blog-tier/UNVERIFIED — keep
  advisory and confirm source (TASK-037 Discovery-Needed).
- **Verification:** spec-coverage smoke (TASK-031); reference exercise catches missing provenance.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/spec/dp-design-eval-golden\.md$`

**TASK-023 — Design sections: Reproducibility & Versioning + Leakage & Skew Test Plan. [OQ-2,OQ-4,OQ-5]**
- **Goal:** Content/descriptions for `dp-design-reproducibility` (dataset versioning/reproducibility;
  candidate OSS tools advisory; optional registry link) and `dp-design-skew-leakage` (explicit
  leakage + train/serving-skew TEST plan; feature store noted as aid, not skew guarantee).
- **Files:** manifest descriptions and optional body files under `plugin/contributions/spec/`.
- **Dependencies:** TASK-001; TASK-033.
- **Satisfies:** REQ-DP-050, 056, 057, 058, 090.
- **Steps:** Tool-of-record open (OQ-2); registry TBD (OQ-5); skew-must-be-tested regardless (OQ-4);
  OSS-first (REQ-DP-094). NO "feature store prevents skew" wording.
- **Verification:** spec-coverage smoke (TASK-031); negative scan (TASK-034); reference exercise
  catches planted feature-store-in-lieu-of-skew-test.
- **Change budget:** max_files 2; interface_policy none. **Risk:** Med (two C4-sensitive sections).
  **Mode:** executor.
- **write_lease:** `^plugin/contributions/spec/dp-design-(reproducibility|skew-leakage)\.md$`

---

### Group 3 — Advisory source + auxiliary agent (resolves OQ-6)

**TASK-024 — Advisory source `dp-airflow-facts` (manifest entry). [OQ-6 resolved: ship both]**
- **Goal:** Declare the `dp-airflow-facts` advisory source: `resolution: orchestrator-relay`,
  description "supplies authoritative Airflow-3/2.x, asset/watcher, OpenLineage facts during
  delegation." No tool/permission required (orchestrator-relay is inline; least-privilege).
- **Files:** `plugin/system2.overlay.json` (the `delegation.advisory_sources` entry stubbed in
  TASK-001 — fill in `name`/`description`).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-065, REQ-DP-009; design §"Delegation advisory source".
- **Verification:** manifest validates (TASK-032); manifest review confirms no `permissions`/
  `mcp_servers` requested (REQ-DP-065 least-privilege).
- **Change budget:** max_files 1; interface_policy extend-only. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/system2\.overlay\.json$`

**TASK-025 — Auxiliary agent `dp-pipeline-scout` (definition file + manifest entry). [OQ-6]**
- **Goal:** Author the read-only fact-gatherer agent and declare it: `pipeline: false`,
  `delegation_policy: orchestrator_optional`, tools `Read` (optionally `Bash` scoped to
  `airflow`/`dbt` version probes, justified in-manifest if added). Returns compact structured fact
  summaries; never blocks; cannot spawn subagents.
- **Files:** `plugin/agents/dp-pipeline-scout.md` (new, with YAML frontmatter — agents/ is the one
  place frontmatter is allowed); `plugin/system2.overlay.json` (`auxiliary_agents` entry).
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-065; design §"Delegation advisory source / auxiliary agent", Security §.
- **Steps:** YAML frontmatter per the template's `template-scout.md` shape (name/role/tools/etc.);
  body = operating rules (read-only, advisory-only, no subagents). If `Bash` is included, scope and
  justify it; otherwise keep `Read`-only for strict least-privilege.
- **Verification:** `test_auxiliary_agent_files_exist` passes (TASK-032); manifest validates;
  frontmatter parses; manifest review confirms `pipeline:false` and least-privilege tools.
- **Change budget:** max_files 2; max_new_symbols 1; interface_policy extend-only. **Risk:** Low.
  **Mode:** executor.
- **write_lease:**
  - `^plugin/agents/dp-pipeline-scout\.md$`
  - `^plugin/system2\.overlay\.json$`

---

### Group 4 — Remove leftover template placeholder files

> The manifest side of removal (dropping `mcp_servers`/`permissions`/`hooks`/unused agents/spec
> artifacts from the JSON) happens in TASK-001. Group 4 deletes the now-orphaned files and the
> placeholder content files that no `dp-` contribution carries forward.

**TASK-026 — Delete template auxiliary agent + hook.**
- **Goal:** Remove `plugin/agents/template-scout.md` (superseded by `dp-pipeline-scout`) and
  `plugin/hooks/post-edit-check.py` (PostToolUse hook rejected — design §Rejected Abstractions).
  Remove the now-empty `plugin/hooks/` directory.
- **Files:** delete `plugin/agents/template-scout.md`, `plugin/hooks/post-edit-check.py`.
- **Dependencies:** TASK-001 (manifest must already drop the hook + template-scout references) and
  TASK-025 (replacement agent exists) — otherwise smoke `test_auxiliary_agent_files_exist` /
  hook checks fail mid-transition.
- **Satisfies:** REQ-DP-002 (no runtime/hook); design §Rejected Abstractions.
- **Verification:** files absent; `git status` shows deletions; smoke (TASK-032) has no dangling
  references.
- **Change budget:** max_files 2; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:**
  - `^plugin/agents/template-scout\.md$`
  - `^plugin/hooks/post-edit-check\.py$`

**TASK-027 — Delete orphaned `tmpl-` content files for the 7 dropped agents.**
- **Goal:** Remove content files for agents NOT in the 6-agent scope: `docs-writing.md`,
  `eval-guidance.md`, `governor-discovery.md`, `mcp-design-rules.md`, `postmortem-guardrails.md`,
  `spec-coordinator-context.md`, `spec-coordinator-style.md`, `task-planner-fields.md`,
  `task-planner-rules.md`, `reviewer-simplification.md` (code-reviewer keeps only criteria +
  surface-area; simplification is dropped).
- **Files:** delete the 10 listed files under `plugin/contributions/agents/`.
- **Dependencies:** TASK-001 (manifest no longer references them).
- **Satisfies:** REQ-DP-008 (no noise where no domain need); design §"Agent prompt sections" note.
- **Verification:** files absent; smoke `test_content_files_exist_and_nonempty` only walks
  manifest-referenced files, so no dangling refs; `git status` shows 10 deletions.
- **Change budget:** max_files 10; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:**
  - `^plugin/contributions/agents/(docs-writing|eval-guidance|governor-discovery|mcp-design-rules|postmortem-guardrails|spec-coordinator-context|spec-coordinator-style|task-planner-fields|task-planner-rules|reviewer-simplification)\.md$`

**TASK-028 — Delete the `executor-safety.md` placeholder (no `dp-` inline safety section).**
- **Goal:** The DataPipelineOverlay does not carry an `executor.safety_rules` inline contribution
  (not in the 26). Remove `plugin/contributions/agents/executor-safety.md`.
- **Files:** delete `plugin/contributions/agents/executor-safety.md`.
- **Dependencies:** TASK-001 (manifest drops `safety_rules`).
- **Satisfies:** REQ-DP-005 (no contribution beyond the designed 26); REQ-DP-008.
- **Verification:** file absent; smoke passes (TASK-032).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** executor.
- **write_lease:** `^plugin/contributions/agents/executor-safety\.md$`

> **Note (decision point for executor):** if the host smoke harness requires an `inline:true`
> contribution to exist (the template demonstrated one), confirm in TASK-033 whether any `dp-`
> principle being `inline:true` satisfies that, OR whether to keep one inline executor directive.
> The design lists no inline executor safety section, so default is removal. Flag if compose warns.

---

### Group 5 — Smoke-test retarget

> The smoke test mirrored from the template (`tests/test_compose_smoke.py`) currently encodes
> template assumptions. Retarget it to the overlay's intentional 6-agent / 2-spec-artifact scope
> while keeping every genuine validation (schema, dp- IDs, summaries, injection scan, dry-run
> compose, ID-applied). Split into three tasks for reviewable diffs.

**TASK-029 — Update `EXPECTED_CONTRIBUTION_IDS`, prefix assertion, and output markers.**
- **Goal:** Replace the 29 `tmpl-` IDs with the 26 `dp-` IDs; change `test_contribution_id_prefix`
  to assert `^dp-`; replace `test_composed_output_contains_overlay_markers` markers
  (`overlay-template`, `[Your domain]`) with DataPipelineOverlay markers (e.g.,
  `data-pipeline-overlay` and a stable phrase from a principle).
- **Files:** `tests/test_compose_smoke.py`.
- **Dependencies:** TASK-001 (IDs finalized).
- **Satisfies:** REQ-DP-003, REQ-DP-004; design §"Smoke-test note".
- **Verification:** `python3 tests/test_compose_smoke.py` — these specific tests pass after content
  lands (full green in TASK-032).
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low. **Mode:** test-engineer.
- **write_lease:** `^tests/test_compose_smoke\.py$`

**TASK-030 — Relax 6-agent-scope assertions: `test_all_13_agents_covered` + `test_full_anchor_coverage`.**
- **Goal:** Replace `EXPECTED_AGENTS` (13) with the 6 in-scope agents and re-scope
  `test_all_13_agents_covered` to assert exactly those 6 are covered and no others; replace
  `test_full_anchor_coverage` (all anchors) with an assertion that the 11 declared anchors are valid
  per the anchor map (subset check), NOT total coverage. Remove `test_hook_files_exist` and the
  `tools`/`hooks`/`mcp_servers`/`permissions` assertions in `test_all_contribution_types_present`
  (those types are intentionally absent — design §Rejected Abstractions).
- **Files:** `tests/test_compose_smoke.py`.
- **Dependencies:** TASK-001, TASK-026.
- **Satisfies:** REQ-DP-001 (additive, 6-agent by design), REQ-DP-008; design §"Smoke-test note".
- **Verification:** the two retargeted tests pass; removed tests no longer present;
  `test_all_contribution_types_present` asserts only the types the overlay actually ships.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Med (must not weaken the
  anchor-validity check to nothing — keep it asserting declared anchors are real). **Mode:** test-engineer.
- **write_lease:** `^tests/test_compose_smoke\.py$`

**TASK-031 — Resolve `test_all_spec_artifacts_covered` to requirements+design only.**
- **Goal:** Change the loop from `["context","requirements","design","tasks"]` to
  `["requirements","design"]` (the two artifacts the overlay targets) and assert `context`/`tasks`
  have NO overlay sections (intentional). If TASK-033 finds the host harness *requires* all four,
  the fallback is a thin `context`/`tasks` section — but the design's primary stance is relax.
- **Files:** `tests/test_compose_smoke.py`.
- **Dependencies:** TASK-001.
- **Satisfies:** REQ-DP-007; design §"Required spec sections" + Discovery-Needed.
- **Verification:** test passes; reflects the 4-req + 4-design section reality.
- **Change budget:** max_files 1; interface_policy none. **Risk:** Low (re-confirm in TASK-033).
  **Mode:** test-engineer.
- **write_lease:** `^tests/test_compose_smoke\.py$`

---

### Group 6 — Validation

**TASK-032 — Run the smoke suite green against local System2.**
- **Goal:** `python3 tests/test_compose_smoke.py` and `pytest tests/` pass end-to-end: schema valid,
  no warnings, content non-empty, no injection patterns, dp- prefix, summaries present, all 26 IDs
  applied, dry-run compose succeeds, retargeted coverage tests pass.
- **Files:** none (read/run only); fixes routed back to the owning task.
- **Dependencies:** ALL of Groups 1–5.
- **Satisfies:** REQ-DP-003, REQ-DP-004.
- **Verification:** both commands exit 0; `0 failed`.
- **Change budget:** max_files 0; interface_policy none. **Risk:** Med (integration gate; surfaces
  any anchor/path mismatch). **Mode:** test-engineer.
- **write_lease:** (none — read/run only)

**TASK-033 — Dry-run compose review: additive-only, advisory-only, lock lists 26, body-file question.**
- **Goal:** Run `/system2:compose` against local System2; confirm no base contribution removed/
  replaced, no hard-block introduced, clean compose, lock `contributions_applied` lists all 26 dp-
  IDs. RESOLVE the two open mechanics questions: (a) does the composer need spec-section *body files*
  or only heading+description (decides TASK-019..023 scope); (b) does the harness require an
  `inline:true` contribution and/or all-four spec artifacts (decides TASK-028/031 fallbacks). Also
  perform the REQ-DP-003 summary-vs-content manual diff here.
- **Files:** none (review).
- **Dependencies:** TASK-032 (smoke green) ideally; can run in parallel for the mechanics questions.
- **Satisfies:** REQ-DP-001, 002, 003, 004.
- **Verification:** compose output shows additive-only diff; lock lists 26 dp- IDs; summary diff
  finds no drift; mechanics questions answered and any resulting task adjustments filed.
- **Change budget:** max_files 0. **Risk:** Med (the two mechanics questions can force rework in
  Groups 2c/4/5). **Mode:** executor.
- **write_lease:** (none — review only)

**TASK-034 — Negative-content scan (C4 refutations).**
- **Goal:** Keyword/claim scan across all content for: "prevents/eliminates skew";
  GE/Soda/dbt-as-blanket DQ; DAG-versioning-as-deterministic-replay; managed-only/closed-source
  dependence; ceremony-on-throwaway. Confirm none present.
- **Files:** none (scan); fixes routed to the owning content task.
- **Dependencies:** Group 2 content complete.
- **Satisfies:** REQ-DP-090..095.
- **Verification:** scan finds zero non-conformant phrases; skew framed as must-test; native-SQL
  default confirmed; re-run safety attributed to engineering.
- **Change budget:** max_files 0. **Risk:** Med (gate for C4 — the overlay's defining constraint).
  **Mode:** security-sentinel.
- **write_lease:** (none — scan only)

**TASK-035 — Reference-DAG exercise (Scope A) with planted-absence checks.**
- **Goal:** Author a test ELT/ETL DAG *with* the overlay; confirm it exhibits idempotency,
  data-aware scheduling, orchestration/compute split, layered DQ, lineage; confirm the overlay's
  checks catch a planted absence of each.
- **Files:** scratch/reference DAG outside the plugin tree (not shipped); no plugin edits.
- **Dependencies:** TASK-032, TASK-033.
- **Satisfies:** REQ-DP-020..029.
- **Verification:** clean DAG passes all checks; each planted-absence variant triggers the
  corresponding advisory finding with declared severity.
- **Change budget:** max_files 0 (plugin). **Risk:** Med. **Mode:** eval-engineer.
- **write_lease:** (none in plugin — reference artifacts live in a scratch dir)

**TASK-036 — Reference-deliverable exercise (Scope B) with planted leakage/missing-provenance.**
- **Goal:** Author a training set + golden eval set *with* the overlay; confirm point-in-time joins,
  leak-safe splits, versioning, provenance; confirm checks catch planted leakage / missing
  provenance / feature-store-in-lieu-of-skew-test.
- **Files:** scratch/reference artifacts; no plugin edits.
- **Dependencies:** TASK-032, TASK-033.
- **Satisfies:** REQ-DP-050..058, 060..063.
- **Verification:** clean deliverable passes; each planted defect triggers its advisory finding;
  feature-store-as-skew-guarantee is flagged (REQ-DP-090).
- **Change budget:** max_files 0 (plugin). **Risk:** Med. **Mode:** eval-engineer.
- **write_lease:** (none in plugin — reference artifacts live in a scratch dir)

**TASK-037 — Blast-radius walkthrough + version-note audit + gate-consultation review + Discovery-Needed confirmations.**
- **Goal:** (a) Low-tier vs high-tier deliverable walkthrough confirms proportional section/check
  demand (REQ-DP-006/007/095). (b) Version-note audit: every divergent Airflow unit carries a 2.x
  note / 3.x-only flag (REQ-DP-009/022). (c) Gate-1/Gate-3 consultation content review confirms all
  required prompts (REQ-DP-061/062). (d) Resolve the three design Discovery-Needed items
  (Astronomer source for retries/SLAs/alerting; secrets-backend source; schema_version 1.0.0 is the
  host's supported version) and re-confirm OQ-1 wording in TASK-007/008/016 content.
- **Files:** content tweaks routed back to owning tasks if gaps found.
- **Dependencies:** Group 2 complete; TASK-032/033.
- **Satisfies:** REQ-DP-006/007/009/022/061/062/095; design §Verification Strategy Discovery-Needed.
- **Verification:** walkthrough notes show no heavy ceremony on throwaway tier; version-note audit
  passes; both gate consultations contain every listed prompt; Discovery-Needed items each have a
  cited source or remain explicitly marked advisory/TBD.
- **Change budget:** max_files 0 (review; fixes routed). **Risk:** Med (UNVERIFIED sources may force
  content softening). **Mode:** executor.
- **write_lease:** (none — review; fixes filed against owning content tasks)

---

## Definition of Done Checklist

- [ ] Manifest has exactly 26 unique `^dp-` contributions at valid anchors; no `mcp_servers`,
      `permissions`, or `hooks` (TASK-001/024/025).
- [ ] Every non-inline contribution has an accurate `summary`; every required section an accurate
      `description`; summary-vs-content diff finds no drift (TASK-002/033 — REQ-DP-003).
- [ ] 21 content files authored: 3 principles, 2 gate consultations, 11 agent sections, 8 spec
      sections (or descriptions if body files unneeded) — all plain Markdown, no frontmatter except
      the aux agent (TASK-003..023).
- [ ] `dp-airflow-facts` (orchestrator-relay) and `dp-pipeline-scout` (read-only, pipeline:false)
      present and least-privilege (TASK-024/025 — REQ-DP-065, OQ-6 resolved).
- [ ] All template residue removed: `template-scout.md`, `post-edit-check.py`, 7 dropped-agent
      content files, `reviewer-simplification.md`, `executor-safety.md`, `hooks/` dir (TASK-026..028).
- [ ] Smoke test retargeted: 26 dp- IDs, `^dp-` prefix, 6-agent scope, declared-anchor validity,
      requirements+design spec artifacts, hook/mcp/permissions assertions removed; suite green
      (TASK-029..032 — REQ-DP-004).
- [ ] Dry-run `/system2:compose` is additive-only + advisory-only; lock lists all 26 dp- IDs
      (TASK-033 — REQ-DP-001/002).
- [ ] Negative-content scan clean: no skew-prevention, no GE/Soda/dbt-blanket, no
      DAG-versioning-as-replay, no managed-only deps, no ceremony-on-throwaway (TASK-034 —
      REQ-DP-090..095).
- [ ] Reference DAG (Scope A) and reference deliverable (Scope B) exhibit the target practices and
      the checks catch planted absences (TASK-035/036 — REQ-DP-020..029, 050..063).
- [ ] Blast-radius proportional; version notes complete; gate consultations complete;
      Discovery-Needed items cited or explicitly marked TBD (TASK-037).
- [ ] OQ-1..6 each remain marked/advisory where unresolved; none silently answered.

---

## Execution Notes (tooling, environment, checkpoints)

- **Environment:** System2 must be cloned at `../System2`. The smoke test imports the composer from
  `../System2/plugin/scripts/composer.py` and reads `../System2/plugin/schemas/{overlay.schema.json,
  anchor-map.json}`. Override location via `SYSTEM2_ROOT` env var if needed.
- **Commands (from CLAUDE.md / requirements Validation Plan):**
  - Smoke: `python3 tests/test_compose_smoke.py` and `pytest tests/`.
  - Compose: `/system2:compose` against local System2 (host slash-command; exact CLI invocation is
    host-provided — **uncertainty flagged**, see Risks).
  - JSON sanity: `python3 -c "import json;json.load(open('plugin/system2.overlay.json'))"`.
- **Checkpoints (commit boundaries):**
  1. After TASK-001/002 — manifest skeleton + summaries committed.
  2. After Group 2 — all content authored (can sub-checkpoint per file).
  3. After Group 3/4 — aux agent + advisory source in, residue removed.
  4. After Group 5 — smoke retargeted.
  5. After TASK-032/033 — green smoke + clean compose (the integration gate).
  6. After Group 6 — validation complete; overlay release-ready.
- **Parallelism:** TASK-003..023 (21 content tasks) and TASK-024/025 are independent given TASK-001
  and can be fanned out. Group 4 deletions depend on the manifest no longer referencing the files.
  Group 5 depends on TASK-001 (IDs) + TASK-026 (hook removal). Group 6 is the join.
- **Boomerang delegation:** content tasks → executor; check-bearing sections (TASK-014/015) →
  test-engineer; security/threat + negative scan (TASK-018/034) → security-sentinel; reference
  exercises (TASK-035/036) → eval-engineer; smoke retarget (TASK-029..031) → test-engineer.
- **Invariants to hold every task:** additive-only, advisory-only, `dp-` prefix, plain-Markdown
  content (no frontmatter except `plugin/agents/`), summaries match content, no secrets in content,
  no System2-mechanics re-teaching, blast-radius-proportional, C4 negatives honored, Airflow-3
  default with 2.x notes.

---

## Traceability (REQ IDs -> TASK IDs)

| REQ-DP | Tasks |
|---|---|
| REQ-DP-001 (additive-only) | TASK-001, 024, 025, 030, 033 |
| REQ-DP-002 (advisory-only) | TASK-014, 026, 033 |
| REQ-DP-003 (dp- IDs, unique, summaries) | TASK-001, 002, 029, 032, 033 |
| REQ-DP-004 (clean compose + smoke) | TASK-029, 030, 031, 032, 033 |
| REQ-DP-005 (G1–G5 non-overlapping) | TASK-001, 028 |
| REQ-DP-006/007 (blast radius tiers) | TASK-008, 009, 011, 037 |
| REQ-DP-008 (no re-teaching, 6 agents) | TASK-001, 027, 028, 030 |
| REQ-DP-009 (Airflow-3 default, 2.x notes) | TASK-004, 010, 024, 037 |
| REQ-DP-020 (idempotent/data-aware/orchestrate default) | TASK-003, 008, 012 |
| REQ-DP-021 (data-aware scheduling) | TASK-004 |
| REQ-DP-022 (watchers, polling caveat, 2.x N/A) | TASK-004*, 037 |
| REQ-DP-023 (idempotency engineered) | TASK-007, 009, 012, 015, 019 |
| REQ-DP-024 (parse-time hygiene check) | TASK-013, 014 |
| REQ-DP-025 (orchestration/compute boundary) | TASK-003, 009, 016, 019 |
| REQ-DP-026 (layered DQ) | TASK-014, 020 |
| REQ-DP-027 (native-SQL default DQ) | TASK-012, 016, 020 |
| REQ-DP-028 (OpenLineage emission) | TASK-009, 013, 014, 020 |
| REQ-DP-029 (medallion/contracts, tier-scoped) | TASK-017 |
| REQ-DP-050 (leakage+skew tested) | TASK-015, 023 |
| REQ-DP-051 (point-in-time) | TASK-013, 014, 021 |
| REQ-DP-052 (split discipline) | TASK-014, 021 |
| REQ-DP-053 (no-execution-date ML DAGs) | TASK-012 |
| REQ-DP-054 (golden/eval set defined+versioned+provenanced) | TASK-009, 015, 022 |
| REQ-DP-055 (eval-set delivery cadence+provenance) | TASK-022 |
| REQ-DP-056 (dataset versioning/reproducibility) | TASK-009, 011, 015, 023 |
| REQ-DP-057 (registry integration, advisory) | TASK-023 |
| REQ-DP-058 (feature store aid, not skew guarantee) | TASK-012, 023 |
| REQ-DP-060 (governance three pillars) | TASK-005, 017 |
| REQ-DP-061 (Gate-1 consultation) | TASK-006, 037 |
| REQ-DP-062 (Gate-3 consultation) | TASK-007, 037 |
| REQ-DP-063 (provenance on artifacts) | TASK-009, 016, 018, 020 |
| REQ-DP-064 (tools advisory/principle-led) | TASK-003, 008, 010 |
| REQ-DP-065 (advisory source + aux agent) | TASK-024, 025 |
| REQ-DP-090 (no feature-store-prevents-skew) | TASK-012, 014, 016, 023, 034 |
| REQ-DP-091 (no GE/Soda/dbt blanket) | TASK-016, 020, 034 |
| REQ-DP-092 (no DAG-versioning-as-replay) | TASK-007, 008, 016, 034 |
| REQ-DP-093 (no tool-eliminates-failure overclaim) | TASK-010, 034 |
| REQ-DP-094 (OSS-first) | TASK-010, 023, 034 |
| REQ-DP-095 (no ceremony on throwaway) | TASK-008, 037 |

\* REQ-DP-022 watcher guidance is carried in the data-aware principle (TASK-004) and/or
requirements guardrails (TASK-010); confirm placement during TASK-037 version-note audit.

| Open Question | Resolved? | Carried in tasks |
|---|---|---|
| OQ-1 (DAG-versioning guarantees) | stance set (engineer re-run safety) | TASK-007, 008, 016, 037 |
| OQ-2 (versioning tool of record) | advisory; name don't mandate | TASK-011, 023 |
| OQ-3 (DQ aggregation/facets) | TBD-marked | TASK-014, 020 |
| OQ-4 (skew mitigation beyond PIT) | skew-must-be-tested holds | TASK-012, 014, 016, 023 |
| OQ-5 (eval cadence + registry) | TBD-marked | TASK-011, 022, 023 |
| OQ-6 (advisory source vs aux agent) | RESOLVED: ship both | TASK-024, 025 |
