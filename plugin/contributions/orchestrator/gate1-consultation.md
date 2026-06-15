Before delegating data-pipeline work, ask two scoping questions and carry the answers into the spec:

1. **Reuse or fork?** Is there an existing canonical dataset or semantic-layer entity that this work should reuse or extend, or are we deliberately forking a new source of truth? Forking a new source of truth is sometimes correct, but it should be a conscious decision, not an accident.

2. **Data-aware or time-aware trigger?** Is the real trigger "new data exists" (favoring asset/data-aware scheduling) or a genuine clock event (favoring cron)? Decide this early, because it shapes the DAG's scheduling design.
