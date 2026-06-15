# Data-pipeline threat dimensions

Extend the threat model with these data-pipeline dimensions:

- **Secrets in DAG code vs. a secrets backend.** Credentials, tokens, and connection strings should come from a secrets backend, not be embedded in DAG code or task literals. (The authoritative source for specific backend practice is unverified — keep this advisory.)

- **PII in lineage and logs.** Lineage and provenance should identify sources, queries, and versions — not raw sensitive payloads. Watch for PII leaking into OpenLineage facets, task logs, or rendered templates.

- **Untrusted source data at ingestion boundaries.** Treat external/source data as untrusted at the ingestion boundary; layered data-quality checks act as input validation. Watch for schema/poisoning risks from unvalidated upstream inputs.
