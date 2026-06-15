# DataPipelineOverlay — Requirements

> System2 Gate-2 artifact. Derived from the approved `spec/context.md` (Gate-1) and
> `research/airflow-mldata-best-practices.md`. **Status: draft for review.**
>
> **The "system" in these requirements is the overlay itself** — the guidance it composes
> into a System2 host (orchestrator principles, gate consultations, per-agent prompt sections,
> required spec sections, advisory sources/auxiliary agents) and the verification checks it
> contributes (test-engineer / code-reviewer). It is **not** an Airflow runtime; the overlay
> ships content, not execution.
>
> **Requirement IDs** use `REQ-DP-NNN` (honoring the `dp-` contribution prefix, C5). Each
> requirement carries `(traces: …)` back to a context goal/section and, where relevant, a
> research finding. Validation/acceptance criteria are stated inline per requirement.
>
> **EARS patterns:** Ubiquitous ("The overlay shall …"), Event-driven ("When …, the overlay
> shall …"), State-driven ("While …"), Optional ("Where …"), Unwanted ("If …, then …").
>
> **Reading the verification requirements:** "verification check" means a check the overlay
> contributes to the host's test-engineer/code-reviewer agents that flags absence of a
> practice. These are advisory (they surface findings); they do not block (additive/advisory,
> C1). Severity/blocking policy is a design decision (see Open Questions).

---

## 0. Conventions, scope, and definitions

- **Host** = a System2 installation the overlay composes into via `/system2:compose`.
- **Deliverable** = the unit of work guidance attaches to: (A) an Airflow **DAG**, or
  (B) an ML **dataset deliverable** (training set, eval/golden set, feature delivery).
- **Blast radius** = the deliverable's risk tier (throwaway/exploratory vs. shared/canonical
  vs. production). Guidance intensity scales with it (Non-goal §6, R1).
- **Airflow 3 is the default idiom; 2.x equivalents are noted where they differ** (C2):
  Assets (3) ≈ Datasets (2.x); asset *watchers* / event-driven triggers are 3.x-only.
- v1 scope covers **both** Scope A (ELT/ETL) and Scope B (ML-data delivery) (§4).

---

## Functional Requirements

### Group M — Overlay-meta (composition, faithfulness, blast-radius)

**REQ-DP-001 (Ubiquitous).** The overlay shall be additive-only: it shall add principles,
gate consultations, agent prompt sections, required spec sections, advisory sources, and
verification checks, and shall remove or override no System2 base capability.
*Validation:* manifest/diff review confirms only additive contribution types; compose dry-run
shows no base contribution removed or replaced.
*(traces: G5, C1, §2)*

**REQ-DP-002 (Ubiquitous).** The overlay shall be advisory-only: its contributions shall
guide host agents and surface findings, and shall not execute pipelines, ship a runtime, or
hard-block host actions.
*Validation:* review confirms no executable pipeline/runtime artifact; verification checks
emit findings rather than enforce gates.
*(traces: G5, C1, §2)*

**REQ-DP-003 (Ubiquitous).** Every overlay contribution shall use the `dp-` ID prefix, IDs
shall be unique across the manifest, and each contribution's manifest `summary` shall
accurately reflect its content file.
*Validation:* smoke test asserts all IDs match `^dp-`, uniqueness holds, and a
summary-vs-content review finds no drift.
*(traces: C5, §13)*

**REQ-DP-004 (Ubiquitous).** The overlay shall compose cleanly against a local System2 via
`/system2:compose` and pass the repo smoke tests.
*Validation:* `python3 tests/test_compose_smoke.py` (and `pytest tests/`) pass; dry-run
composition succeeds.
*(traces: §13, C1)*

**REQ-DP-005 (Ubiquitous).** The overlay shall encode goals G1–G5 as concrete,
non-overlapping `dp-` contributions, with no single failure mode addressed by duplicate
contributions.
*Validation:* a contribution→goal map shows each of G1–G5 covered by ≥1 contribution and no
two contributions asserting the same guidance.
*(traces: G1–G5, §13)*

**REQ-DP-006 (State-driven).** While a deliverable is classified as throwaway/exploratory,
the overlay shall present only lightweight guidance (idempotency awareness and the
orchestration-vs-compute principle) and shall not require the full per-deliverable spec
sections.
*Validation:* guidance content explicitly tiers requirements by blast radius; a low-tier
deliverable review shows no heavy-ceremony sections demanded.
*(traces: §6 Non-goal, R1)*

**REQ-DP-007 (State-driven).** While a deliverable is classified as shared/canonical or
production, the overlay shall require the full per-deliverable spec sections applicable to its
scope (A and/or B) and the corresponding verification checks.
*Validation:* a high-tier deliverable review confirms all applicable required sections (REQ-DP-040,
REQ-DP-070) and checks are demanded.
*(traces: G2, G4, §6, §8)*

**REQ-DP-008 (Ubiquitous).** The overlay shall not re-teach System2 mechanics inside its
contribution content; guidance shall be domain-specific (Airflow/ML-data) only.
*Validation:* content review finds no restatement of base System2 process; content addresses
only data-pipeline domain concerns.
*(traces: §6 Non-goal, CLAUDE.md conventions)*

**REQ-DP-009 (Ubiquitous).** The overlay shall express Airflow guidance in the Airflow-3 idiom
by default and shall annotate the 2.x equivalent wherever the idiom differs (Assets vs.
Datasets) and shall flag 3.x-only features (asset watchers / event-driven triggers) as
unavailable in 2.x.
*Validation:* every Airflow-specific guidance unit that has a 2.x divergence carries an
explicit version note; a reviewer can identify version applicability without external lookup.
*(traces: C2, §7, research: Assets/Datasets, watchers VERIFIED)*

---

### Group A — Scope A: ELT/ETL DAG authoring discipline

**REQ-DP-020 (Ubiquitous).** The overlay shall make the idempotent, data-aware,
orchestrator-not-engine pattern the default an agent reaches for when authoring an ELT/ETL DAG.
*Validation:* the orchestrator principle set names this default; a test DAG authored with the
overlay exhibits it.
*(traces: G1, §8 principles, research: idempotency/orchestration VERIFIED)*

**REQ-DP-021 (Event-driven).** When a deliverable's real trigger is data arrival, the overlay
shall direct the agent to prefer data-aware scheduling (Airflow 3 Assets: producer `outlets`,
consumer `schedule=[Asset]`; 2.x Datasets equivalent) over time-based cron.
*Validation:* Gate-1 consultation and design guidance state the data-aware-over-time-aware
default; a cron→data-aware migration use case produces an asset-scheduled DAG.
*(traces: G1, §4, §7, research: data-aware scheduling VERIFIED)*

**REQ-DP-022 (Optional).** Where a deliverable requires event-driven triggering (e.g., a
queue/message) on Airflow 3, the overlay shall direct the agent to consider asset *watchers*,
and shall state that watchers poll (low-latency, not instantaneous) and are unavailable in 2.x.
*Validation:* event-driven guidance names watchers, includes the polling caveat, and the 2.x
unavailability note.
*(traces: C2, §7, research: watchers VERIFIED with polling caveat)*

**REQ-DP-023 (Ubiquitous).** The overlay shall require that ELT/ETL DAGs be authored to be
idempotent — re-running the same DAG/interval produces the same result — via deterministic,
templated date intervals and overwrite-by-partition rather than blind append.
*Validation:* required spec section "idempotency & backfill" present; verification check flags
non-idempotent task patterns (blind append, non-templated dates).
*(traces: G1, §4, §7, research: idempotency VERIFIED)*

**REQ-DP-024 (Unwanted).** If a DAG file contains time-dependent or heavy dynamic code at
parse time (e.g., `datetime.now()` driving structure, network/DB calls at module top level),
then the overlay's verification check shall flag it.
*Validation:* a planted parse-time-unsafe DAG triggers the check; a clean DAG does not.
*(traces: G1, §4, §8 checks, research: parse-time hygiene VERIFIED)*

**REQ-DP-025 (Ubiquitous).** The overlay shall require that heavy/large data processing be
offloaded to a compute engine (dbt/Spark/warehouse) and that the DAG coordinate, validate, and
emit lineage rather than crunch data in-process.
*Validation:* required spec section "orchestration-vs-compute boundary" present; verification
check flags substantial in-task compute.
*(traces: G1, §4, §7, §8, research: orchestrator-not-engine VERIFIED — most-repeated)*

**REQ-DP-026 (Ubiquitous).** The overlay shall require layered data-quality checks (e.g.,
in-DAG column/table checks plus a broader suite) rather than a single end-of-pipeline gate.
*Validation:* required spec section "layered data-quality" present; verification check flags
DQ that exists only as one terminal gate.
*(traces: G4, §4, §8, research: layered DQ VERIFIED)*

**REQ-DP-027 (Ubiquitous).** The overlay shall present native SQL check operators
(e.g., `SQLColumnCheckOperator`, `SQLTableCheckOperator`) as the **default** in-DAG DQ
approach, and shall present third-party frameworks (Great Expectations / Soda / dbt tests) as
**situational** options chosen per need (e.g., a results store / richer expectations), not as a
blanket recommendation.
*Validation:* DQ guidance names native SQL checks as default and frames GE/Soda/dbt as
situational; see negative REQ-DP-091.
*(traces: G4, C4, §8, research: native-SQL VERIFIED, GE/Soda/dbt blanket CONTESTED)*

**REQ-DP-028 (Ubiquitous).** The overlay shall require that DAGs emit run/dataset lineage via
OpenLineage (provider + listener).
*Validation:* required spec section "lineage/provenance" present; verification check flags
absence of OpenLineage emission.
*(traces: G4, §4, §7, §8, research: OpenLineage VERIFIED)*

**REQ-DP-029 (Optional).** Where a deliverable establishes or consumes layered storage, the
overlay shall offer medallion (bronze/silver/gold) and canonical/semantic layering and data
contracts as expected patterns, scoped to blast radius.
*Validation:* layering/contracts guidance present and tier-scoped.
*(traces: G2, §4, §7, research: medallion/contracts UNVERIFIED — flagged to confirm)*

---

### Group B — Scope B: Labeled-data delivery for ML

**REQ-DP-050 (Ubiquitous).** The overlay shall make ML leakage and skew failure modes
explicit and tested, and shall not allow them to be treated as eliminated by tooling.
*Validation:* ML guidance names leakage and skew as required-to-test; reinforced by negative
REQ-DP-090 and REQ-DP-092.
*(traces: G3, §5, §8)*

**REQ-DP-051 (Ubiquitous).** The overlay shall require point-in-time correctness (as-of-event
joins) as the core leakage defense for any training-set build.
*Validation:* required spec section "point-in-time correctness" present; verification check
flags training joins that are not point-in-time.
*(traces: G3, §4, §7, §8, research: point-in-time VERIFIED)*

**REQ-DP-052 (Ubiquitous).** The overlay shall require explicit train/validation/test
(and, where applicable, holdout) split discipline that prevents train/eval leakage across
splits.
*Validation:* required spec section "split discipline" present; verification check flags
overlapping or leak-prone splits.
*(traces: G3, §4, §7, §8)*

**REQ-DP-053 (Event-driven).** When an ML DAG is not tied to a data interval (e.g., on-demand
training, inference), the overlay shall direct the agent to use Airflow's non-scheduled /
no-execution-date paradigm rather than forcing a cron/interval schedule.
*Validation:* ML scheduling guidance names the no-execution-date paradigm for these DAGs.
*(traces: G1, §4, §7, research: no-execution-date VERIFIED)*

**REQ-DP-054 (Ubiquitous).** The overlay shall require that golden/eval sets be defined,
versioned, provenance-stamped, and human-reviewed before delivery.
*Validation:* required spec section "eval/golden-set definition" present; verification check
flags an eval set lacking version or provenance.
*(traces: G2, G3, §4, §7, §8, research: golden sets VERIFIED — blog-tier sources)*

**REQ-DP-055 (Event-driven).** When a golden/eval set is delivered into a validation/eval loop,
the overlay shall require that it be delivered on a defined schedule and carry provenance
identifying the data/queries/version that produced it.
*Validation:* delivery guidance requires a cadence and a provenance stamp; verification check
flags an undated/unprovenanced delivery. Cadence/registry pattern is TBD (Open Question 5).
*(traces: G2, G3, §4, §7, §8)*

**REQ-DP-056 (Ubiquitous).** The overlay shall require dataset versioning and reproducibility
for ML deliverables (a delivered dataset can be reconstructed/identified by version), and shall
name candidate OSS tools (DVC / LakeFS / Delta/Iceberg time-travel / HF datasets) as advisory,
not mandated.
*Validation:* required spec section "reproducibility/versioning" present; tool-of-record left
open (Open Question 2); verification check flags an unversioned ML deliverable.
*(traces: G2, G3, C3, §4, §7, research: versioning tooling UNVERIFIED — flagged)*

**REQ-DP-057 (Optional).** Where a host project integrates an experiment tracker / model
registry (e.g., MLflow), the overlay shall offer advisory integration guidance for linking
delivered datasets to experiments/registry entries; the concrete pattern is TBD (Open Q 5).
*Validation:* integration guidance present and marked advisory/OSS-first; no hard dependency on
any managed registry.
*(traces: C3, §4, §8, research: MLflow stack UNVERIFIED — flagged)*

**REQ-DP-058 (Optional).** Where a feature store (e.g., Feast) is used, the overlay shall
present it as an aid to shared feature definitions and online/offline retrieval, and shall
explicitly state it does not by itself prevent train/serving skew (see negative REQ-DP-090).
*Validation:* feature-store guidance carries the no-skew-guarantee caveat.
*(traces: G3, C3, C4, §7, research: Feast point-in-time VERIFIED, Feast-prevents-skew CONTESTED 0-3)*

---

### Group G — Cross-cutting governance (apply to A and B)

**REQ-DP-060 (Ubiquitous).** The overlay shall make governance first-class via three pillars:
(1) a governed semantic-layer interface, (2) a small set of canonical, single-source-of-truth
datasets, and (3) provenance on every delivered artifact.
*Validation:* governance principle ("govern the interface, not just the data") present; the
three pillars are reflected in required spec sections and checks.
*(traces: G2, §4, §5, §7, research: governed self-service analytics VERIFIED)*

**REQ-DP-061 (Event-driven).** When an agent reaches Gate 1 (context) for a deliverable, the
overlay's Gate-1 consultation shall prompt: is there an existing canonical dataset / semantic-
layer entity to reuse, or is this forking a new source of truth; and is the trigger data-aware
or time-aware.
*Validation:* Gate-1 consultation content contains both prompts; a Gate-1 run surfaces them.
*(traces: G1, G2, §8, research: Gate-1 candidate)*

**REQ-DP-062 (Event-driven).** When an agent reaches Gate 3 (design) for a deliverable, the
overlay's Gate-3 consultation shall prompt: idempotency/re-run strategy; orchestration/compute
boundary; lineage emission; and (for ML) point-in-time correctness and split/leakage strategy.
*Validation:* Gate-3 consultation content contains all listed prompts (ML prompts conditional
on scope); a Gate-3 run surfaces them.
*(traces: G1, G3, G4, §8, research: Gate-3 candidate)*

**REQ-DP-063 (Ubiquitous).** The overlay shall require provenance on every delivered artifact
(what data/queries/version produced it) for shared/canonical/production deliverables.
*Validation:* required spec section "lineage/provenance" demands an artifact-level provenance
stamp; verification check flags a delivered artifact lacking provenance.
*(traces: G2, §4, §5, §7, research: provenance footer VERIFIED)*

**REQ-DP-064 (Ubiquitous).** The overlay shall keep tool choices advisory and principle-led
(named, not bundled or hard-coded) so that tooling churn does not invalidate the guidance.
*Validation:* guidance states principles first and names tools as examples; no contribution
hard-codes a single tool as the only acceptable choice.
*(traces: R3, C3, §6)*

**REQ-DP-065 (Optional).** Where the host needs authoritative Airflow/asset/lineage facts, the
overlay shall provide an advisory source and/or auxiliary agent (e.g., a "pipeline-scout")
to supply those facts; the exact form (advisory source vs. auxiliary agent vs. both) is TBD
(Open Question 6).
*Validation:* design selects the mechanism and records the decision; until then this remains an
Open Requirement.
*(traces: §8, Open Q 6)*

---

### Group N — Negative / guardrail requirements (honor C4 refutations)

**REQ-DP-090 (Unwanted).** If overlay guidance or generated content states or implies that a
feature store (e.g., Feast) **prevents** or **eliminates** training/serving skew, then that
content is non-conformant; the overlay shall instead state that a feature store helps and that
skew must be actively tested.
*Validation:* content scan finds no "prevents/eliminates skew" claim; skew is framed as
must-test. Verification check flags ML deliverables that rely on a feature store in lieu of a
skew test.
*(traces: C4, G3, §6, research: Feast-prevents-skew CONTESTED 0-3 unanimous)*

**REQ-DP-091 (Unwanted).** If overlay guidance presents Great Expectations / Soda / dbt tests
as **the** blanket DQ recommendation, then that content is non-conformant; native SQL checks
are the default and third-party frameworks are situational (per REQ-DP-027).
*Validation:* content scan confirms native-SQL-default framing and situational positioning of
GE/Soda/dbt.
*(traces: C4, G4, research: GE/Soda/dbt blanket CONTESTED 1-2)*

**REQ-DP-092 (Unwanted).** If overlay guidance relies on Airflow DAG-versioning to guarantee
deterministic replay of historical code, then that content is non-conformant; re-run safety
shall be engineered (idempotency + pinned task code), and DAG-versioning shall be described
only as version tracking, not a replay guarantee.
*Validation:* content scan confirms re-run safety is attributed to engineering, not to
DAG-versioning; what DAG-versioning actually guarantees is TBD (Open Question 1).
*(traces: C4, G1, research: DAG-versioning deterministic-replay CONTESTED 1-2)*

**REQ-DP-093 (Unwanted).** If a contribution asserts that any tool eliminates a failure mode,
then that content is non-conformant (no-overclaim rule generalizing C4).
*Validation:* content review finds no "tool X eliminates failure Y" claim across all
contributions.
*(traces: C4, §6 Non-goal)*

**REQ-DP-094 (Unwanted).** If a contribution depends on a closed-source or managed-only
feature, then that content is non-conformant; the overlay shall stay OSS-first.
*Validation:* dependency review confirms every named tool is OSS or has an OSS path.
*(traces: C3, §4)*

**REQ-DP-095 (Unwanted).** If guidance mandates heavy ceremony for a throwaway/exploratory
deliverable, then that content is non-conformant; intensity scales to blast radius
(REQ-DP-006/007).
*Validation:* low-tier walkthrough shows no full-section/ceremony demand.
*(traces: R1, §6 Non-goal)*

---

## Data & Interface Contracts

The overlay's "interface" is its **contribution surface** into a System2 host; it ships no
runtime persistence or live API.

- **Manifest contract:** Contributions are declared in `plugin/system2.overlay.json`, validated
  against System2's `plugin/schemas/overlay.schema.json`, using only valid contribution types
  (orchestrator principles; gate consultations; agent prompt sections keyed by valid anchor
  names from `anchor-map.json`; spec required sections; delegation advisory sources; auxiliary
  agents; MCP servers; permissions). *(REQ-DP-001, REQ-DP-004)*
- **ID contract:** all contribution IDs `^dp-`, unique manifest-wide. *(REQ-DP-003)*
- **Content contract:** content files are plain Markdown (no frontmatter/YAML); auxiliary-agent
  files carry the required YAML frontmatter; each non-inline contribution's `summary` matches
  its content. *(REQ-DP-003, C5, CLAUDE.md conventions)*
- **Required spec-section contract (per deliverable):** the overlay contributes these section
  headings into the host's spec requirements for in-scope deliverables —
  *Idempotency & backfill; Orchestration-vs-compute boundary; Layered data-quality;
  Lineage/provenance;* and for ML: *Split discipline; Point-in-time correctness;
  Eval/golden-set definition; Reproducibility/versioning.* *(REQ-DP-007, REQ-DP-040 group)*
- **Provenance stamp (domain artifact contract):** a delivered artifact's provenance must
  identify source data, transforming query/job, and version. Exact schema/facet standardization
  is TBD (Open Question 3). *(REQ-DP-063, REQ-DP-055)*
- **Idempotency contract (engineered, not assumed):** re-running a DAG/interval yields the same
  result via templated intervals + overwrite-by-partition; not derived from DAG-versioning
  (REQ-DP-092). *(REQ-DP-023)*

---

## Error Handling & Recovery

These are properties the overlay's **guidance requires of authored pipelines**, plus the
overlay's own failure behavior.

- **Re-run safety:** the overlay shall require retry-safe, idempotent tasks so re-runs and
  backfills do not corrupt or duplicate data (overwrite-by-partition). *(REQ-DP-023)*
- **Backfill:** the overlay shall require an explicit backfill strategy in the per-deliverable
  spec section. *(REQ-DP-023, REQ-DP-007)*
- **DQ as a recovery signal:** layered DQ checks shall surface bad data early (in-DAG) rather
  than only at a terminal gate, enabling earlier failure and narrower blast radius. *(REQ-DP-026)*
- **Retries/SLAs/alerting:** the overlay shall present retries, SLAs, and alerting as expected
  operational practices for shared/production DAGs (source UNVERIFIED — confirm at design).
  *(traces: research UNVERIFIED list)*
- **Overlay self-failure:** if the overlay fails to compose, the host shall remain usable
  without it (additive/advisory means absence degrades to base System2, not breakage).
  *(REQ-DP-001, REQ-DP-002)*
- **Verification-check failure mode:** verification checks surface findings; a missing/failed
  check shall not block host progress (advisory). Blocking vs. warning policy is a design
  decision. *(REQ-DP-002, Open Questions)*

---

## Performance & Scalability

The overlay is a content/composition artifact, not a high-throughput runtime; distributed-
systems flow-control patterns are **not** mandated here (initial budgets, to be validated):

- **Composition:** `/system2:compose` and smoke tests shall complete within the host's normal
  compose budget; the overlay shall add no unbounded compose-time work. *(REQ-DP-004)*
- **Guidance proportionality (the real "scalability" axis):** guidance volume scales to blast
  radius, not uniformly — preventing ceremony overhead on low-value work. *(REQ-DP-006/007, R1)*
- **Authored-pipeline performance** is a property of the target pipeline, governed by the
  orchestration-vs-compute principle (push heavy work to engines), not by the overlay runtime.
  *(REQ-DP-025)*
- Back-pressure / partition-tolerance / circuit-breaker requirements are intentionally **not**
  specified for the overlay (it is not an event-processing system). They may apply to authored
  pipelines and are deferred to per-pipeline design.

---

## Consistency & Domain Boundaries

Two bounded contexts emerge, with different language and consistency needs:

- **Context 1 — Pipeline-engineering (Scope A):** language of DAGs, assets/datasets, partitions,
  idempotency, lineage. Aggregate: **a DAG plus its asset/partition state and lineage** form a
  consistency unit — within a run/interval the overlay requires immediate consistency
  (idempotent overwrite of a partition is atomic-per-partition in intent). *(REQ-DP-023, REQ-DP-028)*
- **Context 2 — ML-data delivery (Scope B):** language of training/eval sets, point-in-time
  correctness, splits, skew, provenance, versions. Aggregate: **a dataset deliverable plus its
  version + provenance + split definition** form a consistency unit — these must be mutually
  consistent at delivery time. *(REQ-DP-051..056, REQ-DP-063)*
- **Polysemy noted:** "dataset" differs across contexts — in Airflow 3 an *Asset/Dataset* is a
  scheduling signal (Context 1); an ML *dataset deliverable* is a versioned, provenance-stamped
  artifact (Context 2). The overlay shall not force a single canonical model; guidance shall
  keep the two senses distinct. *(traces: C2, §7; DDD polysemy)*
- **Inter-context relationship:** Context 1 (pipeline-engineering) is **upstream** producer;
  Context 2 (ML-data delivery) is **downstream** consumer that conforms to delivered assets but
  re-models them as versioned deliverables. Between contexts, **eventual consistency** is the
  default: an asset update in Context 1 becomes observable to Context 2 consumers via data-aware
  scheduling within the scheduler/watcher poll latency (low-latency, not instantaneous —
  REQ-DP-022). Stronger guarantees are not required because no concrete user-facing failure
  demands them at v1 scale.
- **Overlay-vs-host boundary:** the overlay is downstream of and conforms to the System2 host
  contract (schema/anchors); it never redefines host semantics (REQ-DP-001, REQ-DP-008).

---

## Security & Privacy

- **Least privilege / secrets:** the overlay shall present secrets-via-secrets-backend (not
  in-DAG literals) as expected practice for authored pipelines (source UNVERIFIED — confirm).
  *(traces: research UNVERIFIED list)*
- **No secret leakage in overlay content:** overlay contribution files shall contain no
  credentials, tokens, or environment-specific secrets. *(C1, C5)*
- **Logging hygiene:** provenance/lineage emission shall not require logging raw sensitive
  records; provenance identifies sources/queries/versions, not payload contents. *(REQ-DP-063)*
- **Permissions surface:** any tool permissions the overlay requests (e.g., for an advisory
  source) shall be least-privilege and justified in the manifest. *(REQ-DP-065, C1)*
- **Input sanitization (authored DQ):** layered DQ checks serve as input validation at data
  boundaries. *(REQ-DP-026)*

---

## Observability

- **Lineage as first-class observability:** the overlay shall require OpenLineage run/dataset
  lineage emission, giving runtime observability of data flow. *(REQ-DP-028)*
- **DQ results visibility:** the overlay shall require that layered DQ results be observable;
  aggregation + OpenLineage facet standardization is TBD (Open Question 3). *(REQ-DP-026)*
- **Provenance as audit trail:** every delivered artifact's provenance provides traceable
  observability of what produced it. *(REQ-DP-063)*
- **Verification-check findings:** the overlay's checks shall report findings in a form the
  host can surface (pass/flag with rationale) so absence of a practice is visible. *(REQ-DP-024
  and all checks)*
- **ML drift watch:** the overlay shall present eval-set drift monitoring as an expected
  practice for golden sets (source blog-tier/UNVERIFIED — confirm). *(REQ-DP-054)*

---

## Backward Compatibility & Migration

- **Host compatibility:** the overlay shall conform to the current System2 overlay schema
  version and break no existing host behavior (additive). *(REQ-DP-001, REQ-DP-004)*
- **Airflow 2.x ↔ 3 migration:** the overlay shall keep guidance usable on Airflow 2.x by
  annotating 2.x equivalents (Datasets) and flagging 3.x-only features (watchers). *(REQ-DP-009,
  REQ-DP-022, C2)*
- **cron → data-aware migration:** the overlay shall support the documented use case of
  migrating time-based DAGs to data-aware scheduling without mandating a rewrite of unrelated
  logic. *(REQ-DP-021, §3)*
- **Tooling-churn resilience:** principle-led, tool-advisory guidance shall remain valid as
  named tools evolve. *(REQ-DP-064, R3)*
- **Contribution evolution:** future scope (non-Airflow orchestrators) is explicitly out of v1
  and shall be a separate overlay, not a breaking change here. *(§4 out-of-scope)*

---

## Compliance / Policy Constraints

- **OSS-first policy (C3):** no dependence on managed-only/closed-source features. *(REQ-DP-094)*
- **No-overclaim policy (C4):** honored as REQ-DP-090..093.
- **Overlay conventions policy (C1, C5):** additive-only, advisory-only, `dp-` prefix,
  plain-Markdown content, summaries match content. *(REQ-DP-001..003)*
- **Provenance/governance policy (G2):** provenance required on delivered artifacts for
  shared/canonical/production tiers. *(REQ-DP-063)*

---

## Open Requirements / TBDs (carried from context §12 — do not invent answers)

- **OQ-1 (→ REQ-DP-092, REQ-DP-023):** Airflow 3 DAG-versioning — what it actually guarantees
  vs. what must be engineered. **Resolve before finalizing re-run-safety guidance.**
- **OQ-2 (→ REQ-DP-056):** Dataset-versioning tool of record (DVC vs LakeFS vs Delta/Iceberg
  time-travel vs HF datasets). **Remains advisory until resolved.**
- **OQ-3 (→ REQ-DP-026, Data Contracts, Observability):** DQ results aggregation +
  OpenLineage facet standardization.
- **OQ-4 (→ REQ-DP-050, REQ-DP-090):** Train/serving skew mitigation beyond point-in-time
  joins. (Skew-must-be-tested holds regardless.)
- **OQ-5 (→ REQ-DP-055, REQ-DP-057):** Golden eval-set delivery cadence + MLflow registry
  integration pattern.
- **OQ-6 (→ REQ-DP-065):** Auxiliary agent vs. advisory source (or both) for Airflow/lineage
  facts. **REQ-DP-065 is an Open Requirement until design decides.**

---

## Validation Plan

| Method | Applies to | How |
|---|---|---|
| Manifest/schema smoke test | M-group (001–005) | `tests/test_compose_smoke.py`, `pytest tests/`: IDs `^dp-`, unique, valid types/anchors, summaries present |
| Compose dry-run | REQ-DP-001/002/004 | `/system2:compose` against local System2; confirm additive-only, advisory-only, clean compose |
| Summary-vs-content review | REQ-DP-003 | Manual diff of each `summary` against its content file |
| Content scan (negative checks) | REQ-DP-090..095 | Keyword/claim scan for "prevents/eliminates skew", GE/Soda/dbt-as-blanket, DAG-versioning-as-replay, managed-only deps, ceremony-on-throwaway |
| Reference-DAG exercise (Scope A) | REQ-DP-020..029 | Author a test DAG **with** the overlay; confirm it exhibits idempotency, data-aware scheduling, orchestration/compute split, layered DQ, lineage; confirm checks catch a planted absence of each |
| Reference-deliverable exercise (Scope B) | REQ-DP-050..058 | Author a test training set + golden eval set **with** the overlay; confirm point-in-time joins, leak-safe splits, versioning, provenance; confirm checks catch planted leakage / missing provenance / feature-store-in-lieu-of-skew-test |
| Gate-consultation review | REQ-DP-061/062 | Inspect Gate-1/Gate-3 consultation content for all required prompts |
| Blast-radius walkthrough | REQ-DP-006/007/095 | Low-tier vs high-tier deliverable: confirm proportional section/check demand |
| Version-note audit | REQ-DP-009/022 | Confirm every divergent Airflow guidance unit carries a 2.x note / 3.x-only flag |
| Open-Requirement tracking | OQ-1..6 | Confirm each TBD is marked, not silently answered; REQ-DP-065 stays Open until OQ-6 resolved |

**Definition of Done (overlay, from §13):** composes cleanly + smoke-passes; G1–G5 encoded as
non-overlapping `dp-` contributions; a reference DAG/deliverable visibly exhibits the target
practices and the checks catch their absence; no overclaims (C4); guidance blast-radius-
proportional.

---

## Traceability Matrix

| Requirement | Context goal/section | Research finding | Design section (TBD) | Task IDs (TBD) |
|---|---|---|---|---|
| REQ-DP-001 | G5, C1, §2 | harness/repo-local VERIFIED | — | — |
| REQ-DP-002 | G5, C1, §2 | — | — | — |
| REQ-DP-003 | C5, §13 | — | — | — |
| REQ-DP-004 | §13, C1 | — | — | — |
| REQ-DP-005 | G1–G5, §13 | — | — | — |
| REQ-DP-006 | §6, R1 | — | — | — |
| REQ-DP-007 | G2, G4, §6, §8 | — | — | — |
| REQ-DP-008 | §6, CLAUDE.md | — | — | — |
| REQ-DP-009 | C2, §7 | Assets/Datasets, watchers VERIFIED | — | — |
| REQ-DP-020 | G1, §8 | idempotency/orchestration VERIFIED | — | — |
| REQ-DP-021 | G1, §4, §7 | data-aware scheduling VERIFIED | — | — |
| REQ-DP-022 | C2, §7 | watchers VERIFIED (polling caveat) | — | — |
| REQ-DP-023 | G1, §4, §7 | idempotency VERIFIED | — | — |
| REQ-DP-024 | G1, §4, §8 | parse-time hygiene VERIFIED | — | — |
| REQ-DP-025 | G1, §4, §7, §8 | orchestrator-not-engine VERIFIED | — | — |
| REQ-DP-026 | G4, §4, §8 | layered DQ VERIFIED | — | — |
| REQ-DP-027 | G4, C4, §8 | native-SQL VERIFIED; GE/Soda/dbt CONTESTED | — | — |
| REQ-DP-028 | G4, §4, §7, §8 | OpenLineage VERIFIED | — | — |
| REQ-DP-029 | G2, §4, §7 | medallion/contracts UNVERIFIED | — | — |
| REQ-DP-050 | G3, §5, §8 | — | — | — |
| REQ-DP-051 | G3, §4, §7, §8 | point-in-time VERIFIED | — | — |
| REQ-DP-052 | G3, §4, §7, §8 | (split discipline UNVERIFIED) | — | — |
| REQ-DP-053 | G1, §4, §7 | no-execution-date VERIFIED | — | — |
| REQ-DP-054 | G2, G3, §4, §7, §8 | golden sets VERIFIED (blog-tier) | — | — |
| REQ-DP-055 | G2, G3, §4, §7, §8 | golden sets VERIFIED (blog-tier) | — | — |
| REQ-DP-056 | G2, G3, C3, §4, §7 | versioning UNVERIFIED | — | — |
| REQ-DP-057 | C3, §4, §8 | MLflow stack UNVERIFIED | — | — |
| REQ-DP-058 | G3, C3, C4, §7 | Feast point-in-time VERIFIED; skew CONTESTED | — | — |
| REQ-DP-060 | G2, §4, §5, §7 | governed analytics VERIFIED | — | — |
| REQ-DP-061 | G1, G2, §8 | Gate-1 candidate | — | — |
| REQ-DP-062 | G1, G3, G4, §8 | Gate-3 candidate | — | — |
| REQ-DP-063 | G2, §4, §5, §7 | provenance footer VERIFIED | — | — |
| REQ-DP-064 | R3, C3, §6 | — | — | — |
| REQ-DP-065 | §8, OQ-6 | aux-agent/advisory TBD | — | — |
| REQ-DP-090 | C4, G3, §6 | Feast-prevents-skew CONTESTED 0-3 | — | — |
| REQ-DP-091 | C4, G4 | GE/Soda/dbt blanket CONTESTED 1-2 | — | — |
| REQ-DP-092 | C4, G1 | DAG-versioning replay CONTESTED 1-2 | — | — |
| REQ-DP-093 | C4, §6 | (generalizes C4) | — | — |
| REQ-DP-094 | C3, §4 | OSS-first | — | — |
| REQ-DP-095 | R1, §6 | — | — | — |

> Design section and Task ID columns are intentionally TBD until `spec/design.md` and
> `spec/tasks.md` exist; populate during Gate-3/Gate-4.
