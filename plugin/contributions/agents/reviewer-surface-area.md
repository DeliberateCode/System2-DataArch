# Data-pipeline surface-area delta

Track the governance surface a change introduces or alters, tier-scoped to blast radius:

- **Sources of truth.** Does the change introduce a new source-of-truth dataset, or reuse/extend an existing canonical one? Flag new forks of an existing entity for review.

- **Layering.** What medallion (bronze/silver/gold) or semantic-layer layering does the change introduce or move data across? Note new layers and new cross-layer dependencies.

Keep this proportional: for throwaway or exploratory work a light note suffices; for canonical/production work, enumerate the new governance surface explicitly.
