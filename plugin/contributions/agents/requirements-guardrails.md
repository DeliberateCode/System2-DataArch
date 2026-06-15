# Data-pipeline requirements guardrails

When writing requirements for Airflow and ML-data work, hold these guardrails:

- **Airflow-3 idiom with 2.x notes.** Express scheduling and asset requirements in the Airflow 3 idiom (Assets, `outlets`/`schedule=[Asset]`) and add an explicit 2.x note where the idiom differs (Assets correspond to Datasets on 2.x; event-driven watchers are Airflow 3.x only). Flag any unit that diverges across versions.

- **Tools advisory, never eliminative.** Name tools only as examples. Never write a requirement that states a tool *eliminates* or *prevents* a failure mode. A feature store does not prevent train/serving skew; DAG-versioning does not guarantee deterministic replay; a data-quality framework does not by itself remove bad data. Phrase the requirement around the property to achieve and how it will be tested, not around a tool that supposedly removes the risk.

- **Native SQL is the default for data quality.** Default data-quality requirements to native SQL check operators layered through the pipeline. Treat Great Expectations, Soda, and dbt tests as situational choices, not blanket requirements.

- **Open-source first.** Prefer open-source options when naming candidate tools; do not require a managed or closed-source dependency unless the deliverable genuinely needs it.

- **Some operational practices are advisory.** Retries, SLAs, and alerting are expected operational practice for shared/production DAGs, but the authoritative source for specifics is unverified — keep these advisory rather than asserting firm thresholds.
