# Required requirement sections for data deliverables

Tier-scope these requirement sections to the deliverable's blast radius (throwaway work needs little; canonical/production work needs all that apply):

**Always:**
- **Idempotency & Backfill** — requirements for re-run and backfill safety via templated intervals and overwrite-by-partition.

**For ML-data deliverables:**
- **Split** — requirements for train/val/test (and optional holdout) discipline.
- **Point-in-Time** — requirements that feature/label joins are point-in-time correct.
- **Eval/Golden Set** — requirements for an eval/golden set's definition, versioning, and provenance.
- **Versioning** — requirements for dataset versioning and reproducibility.

Notes:
- The dataset-versioning tool of record is left open (advisory; name candidates, mandate none).
- Eval-set delivery cadence and any registry pattern are marked TBD until decided; capture them as open items rather than firm requirements.
