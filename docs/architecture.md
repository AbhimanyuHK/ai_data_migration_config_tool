# Architecture and Module Boundaries

## Dependency direction

```text
API / CLI
   |
   v
Orchestration
   |
   +--> Agents ----> LLM
   |
   +--> Domain
   |
   +--> Deterministic Tools ----> Database Adapters
   |
   +--> Validation / Guardrails
   |
   +--> Artifacts / Observability
```

### Boundaries

- `domain`: database-neutral business models and migration concepts. No DB SDKs.
- `config`: YAML/JSON loading and configuration validation. No execution.
- `orchestration`: coordinates lifecycle/state. It does not contain dialect-specific SQL.
- `agents`: AI reasoning and structured proposals. Agents cannot bypass validation or execute arbitrary SQL.
- `tools`: deterministic metadata, profiling, SQL generation, and execution adapters.
- `guardrails`: deterministic policy and risk enforcement.
- `validation`: schema, SQL, migration, and reconciliation checks.
- `artifacts`: generated plans, SQL, reports, and provenance manifests.
- `observability`: logging, metrics, tracing, and audit instrumentation.
- `api` / `cli`: transport and user interfaces; they remain thin.

Database-specific behavior belongs under `tools/metadata` and related adapter modules. Domain and orchestration code must depend on interfaces/contracts rather than Sybase/Snowflake implementations.
