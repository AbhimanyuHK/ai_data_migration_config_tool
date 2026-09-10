# ai_data_migration_config_tool

```python
readme_content = """# DataMorph Agent (Autonomous Data Engineering Super-Agent)

**DataMorph Agent** is an end-to-end, LLM-powered autonomous data engineering engine designed to automate the modern ELT/ETL lifecycle. It inspects raw structured and semi-structured cloud files (CSV, Parquet, JSON), configures cloud ingestion stages (Snowflake & Redshift), synthesizes complete dbt projects (sources, staging views, marts, tests), monitors daily schema evolution, and scaffolds robust CI/CD pipelines.

---

## 1. Executive Summary & Core Value Proposition

Modern data engineering teams spend significant manual effort on routine plumbing:
- Inspecting source file schemas (especially polymorphic or deeply nested JSON).
- Writing cloud data warehouse ingestion DDLs (`STORAGE INTEGRATION`, `STAGE`, `COPY INTO`, `EXTERNAL SCHEMA`).
- Writing boilerplate `dbt` staging models, data typing casts, and `schema.yml` assertions.
- Debugging pipeline breakage caused by upstream schema drift (added fields, mutated types).
- Creating and maintaining CI/CD orchestration scripts.

**DataMorph Agent** turns raw object storage into production-ready analytical marts autonomously. By fusing local, deterministic schema profiling (via DuckDB / PyArrow) with an intelligent multi-agent orchestration graph (LangGraph / CrewAI), it eliminates manual boilerplate while enforcing type safety, idempotency, and automated pipeline regression testing.

---

## 2. Key Features

- **Multi-Cloud Storage Detection**: Autonomous discovery and inspection across **AWS S3**, **Azure Blob Storage / ADLS Gen2**, and **Google Cloud Storage (GCS)**.
- **Multi-Format Ingestion**: Native parsing and type inference for **Parquet**, **JSON / JSON Lines**, and delimited **CSV/TSV** datasets.
- **Warehouse Target Support**:
  - **Snowflake**: Automates Storage Integrations, External Stages, File Formats, `COPY INTO`, Snowpipes, Streams, and Tasks.
  - **Amazon Redshift**: Generates IAM roles, Redshift Spectrum External Tables, Staging Tables, and `UNLOAD` commands.
- **Automated dbt Synthesis**:
  - Generates `sources.yml` complete with schema descriptions and fresh checks.
  - Generates staging SQL models (`stg_*.sql`) with automated nested JSON flattening (Snowflake `:` / `FLATTEN()`, Redshift `JSON_EXTRACT_PATH_TEXT`).
  - Generates `schema.yml` with basic assertions (`not_null`, `unique`, `accepted_values`).
- **Schema Drift & Reconciliation Engine**: Daily cron-based introspection tracking schema delta hashes against warehouse metadata catalogs, auto-generating migration DDLs (`ALTER TABLE ... ADD COLUMN`) and git commits.
- **Automated CI/CD Orchestration**: Generates GitHub Actions and GitLab CI workflows that execute dynamic linting (`sqlfluff`), staging builds (`dbt compile`, `dbt test`), and continuous deployment.
- **Bi-Directional Data Flow (Reverse ETL / Egress)**: Built-in functionality to export curated views or tables back into cloud object storage in standard formats (Parquet/CSV) for downstream ML models or external consumption.

---

## 3. High-Level System Architecture


```

```
             ┌────────────────────────────────────────────────────────┐
             │          Raw Data Ingestion Sources                    │
             │   - AWS S3 (CSV, Parquet, Nested JSON)                 │
             │   - Azure Blob / ADLS Gen2                             │
             │   - Google Cloud Storage (GCS)                         │
             └──────────────────────────┬─────────────────────────────┘
                                        │
                                        ▼

```

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           1. PROFILING & DISCOVERY ENGINE                       │
│  - DuckDB / PyArrow: Zero-copy sampling (first 10k rows)                        │
│  - Type Inferrer: Polymorphism resolution & null-density calculation            │
│  - Schema Extractor: JSON path flattener & structural hash generator            │
└───────────────────────────────────────────┬─────────────────────────────────────┘
│ Metadata Payload
▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    2. MULTI-AGENT ORCHESTRATOR (LangGraph Core)                 │
│                                                                                 │
│   ┌──────────────────────────┐                   ┌──────────────────────────┐   │
│   │   Ingestion DDL Agent    │                   │    dbt Synthesis Agent   │   │
│   │  - Stage & File Formats  │                   │  - sources.yml & models  │   │
│   │  - COPY INTO / Snowpipe  │                   │  - Flattening & Casts    │   │
│   └─────────────┬────────────┘                   └────────────┬─────────────┘   │
│                 │                                             │                 │
│                 ▼                                             ▼                 │
│   ┌──────────────────────────┐                   ┌──────────────────────────┐   │
│   │   Schema Drift Agent     │                   │    CI/CD & Egress Agent  │   │
│   │  - Hash comparisons      │                   │  - GitHub / GitLab CI    │   │
│   │  - Migration DDL PRs     │                   │  - Reverse ETL / Unload  │   │
│   └──────────────────────────┘                   └──────────────────────────┘   │
└───────────────────────────────────────────┬─────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          3. DATA PLATFORM EXECUTION LAYER                       │
│                                                                                 │
│    Snowflake / Amazon Redshift                    GitHub Actions / Orchestration│
│   ┌──────────────────────────┐                   ┌──────────────────────────┐   │
│   │ Raw Layer (Stages/Tables)│                   │ Auto PRs / Daily Run     │   │
│   │ Silver (dbt Staging)     │ ◀─────────────────│ dbt build / dbt test     │   │
│   │ Gold (Curated Marts)     │                   │ Schema Drift Triggers    │   │
│   └──────────────────────────┘                   └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘

```

---

## 4. Multi-Agent Workflow Specification

The system is organized into specialized autonomous agents coordinated by a state graph:

### Agent 1: Profiler & Cataloger
- **Action**: Connects to the cloud URI via read-only credentials, reads header signatures, and samples files.
- **Engine**: Runs embedded DuckDB to read remote files directly (`read_parquet()`, `read_json_auto()`, `read_csv_auto()`).
- **Output**: Generates a standardized JSON Schema contract documenting fields, data types, nullability, and JSON nesting hierarchy.

### Agent 2: Ingestion Engineer
- **Action**: Determines the target platform and emits warehouse-native data pipeline objects.
- **Capabilities**:
  - **Snowflake**: Writes SQL for `CREATE STORAGE INTEGRATION`, `CREATE FILE FORMAT`, `CREATE STAGE`, and idempotent `COPY INTO` commands.
  - **Redshift**: Writes SQL for IAM role association, Redshift Spectrum external schemas, and target staging tables with distribution and sort keys.

### Agent 3: dbt Analytics Engineer
- **Action**: Scaffolds a complete dbt-core project structure.
- **Capabilities**:
  - Emits `models/staging/sources.yml` and documentation blocks.
  - Emits `models/staging/stg_<source>__<entity>.sql` containing dialect-correct data parsing and column renames.
  - Emits `models/staging/schema.yml` with basic assertions (`unique`, `not_null`).

### Agent 4: Drift & Evolution Monitor
- **Action**: Runs on a daily schedule (or webhook trigger). Computes the checksum of incoming source schemas and compares it to the local catalog state.
- **Capabilities**:
  - **Additive Change**: Emits `ALTER TABLE ... ADD COLUMN` and appends new column mapping in dbt staging models.
  - **Breaking Change (Type mutation / Column dropped)**: Generates an incident report, quarantines unexpected formats into an exception table, and prevents downstream model failures.

### Agent 5: DevOps & CI/CD Engineer
- **Action**: Scaffolds workflow automation files.
- **Capabilities**:
  - Generates `.github/workflows/data_pipeline_ci.yml`.
  - Configures PR validation: lints SQL with `sqlfluff`, spins up a slim CI environment in Snowflake/Redshift, runs `dbt run --select state:modified+` and `dbt test`.

### Agent 6: Egress / Reverse ETL Agent
- **Action**: Automates downstream consumption workflows.
- **Capabilities**:
  - Generates parameterized export tasks using Snowflake `COPY INTO @stage/export/` or Redshift `UNLOAD ('SELECT * FROM ...') TO 's3://...' FORMAT AS PARQUET` for external data sharing.

---

## 5. Repository Directory Structure

```plaintext
datamorph-agent/
├── .github/
│   └── workflows/
│       ├── daily_drift_detector.yml
│       └── dbt_ci_cd.yml
├── config/
│   ├── connections.yml            # Cloud & Warehouse credentials
│   └── agent_rules.yml            # Rules for transformations and drift handling
├── core/
│   ├── __init__.py
│   ├── orchestrator.py            # LangGraph StateGraph engine
│   ├── profiler.py                # DuckDB / PyArrow local profiling engine
│   ├── state.py                   # Graph state management
│   └── agents/
│       ├── ingestion_agent.py     # Stage, Format & COPY generator
│       ├── dbt_agent.py           # dbt SQL, source.yml & schema.yml generator
│       ├── drift_agent.py         # Schema drift reconciliation logic
│       ├── cicd_agent.py          # GitHub Actions / CI pipeline builder
│       └── egress_agent.py        # Reverse ETL / UNLOAD generator
├── dbt_project/                   # Autonomous dbt workspace created by Agent
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── macros/
│   └── models/
│       ├── staging/
│       │   ├── sources.yml
│       │   ├── schema.yml
│       │   └── stg_s3__events.sql
│       └── marts/
├── scripts/
│   ├── run_agent.py               # Main CLI entry point
│   └── scheduled_drift_check.py   # Daily runner script
├── tests/
│   ├── test_profiler.py
│   └── test_dbt_generation.py
├── requirements.txt
└── README.md

```

---

## 6. Sample Artifacts Generated by DataMorph

### A. Snowflake Ingestion SQL (`snowflake_ingest.sql`)

```sql
-- Generated by DataMorph Ingestion Agent
CREATE OR REPLACE FILE FORMAT analytics.raw.ff_json_streaming
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE
    IGNORE_UTF8_ERRORS = TRUE;

CREATE OR REPLACE STAGE analytics.raw.stage_s3_events
    STORAGE_INTEGRATION = s3_int_prod
    URL = 's3://data-lake-landing/events/'
    FILE_FORMAT = analytics.raw.ff_json_streaming;

CREATE TABLE IF NOT EXISTS analytics.raw.events_raw (
    raw_payload VARIANT,
    ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    source_filename VARCHAR(512)
);

COPY INTO analytics.raw.events_raw (raw_payload, source_filename)
FROM (
    SELECT 
        $1, 
        METADATA$FILENAME 
    FROM @analytics.raw.stage_s3_events
)
FILE_FORMAT = (FORMAT_NAME = analytics.raw.ff_json_streaming)
ON_ERROR = 'CONTINUE';

```

### B. dbt Staging Model (`stg_s3__events.sql`)

```sql
-- Generated by DataMorph dbt Agent
{{ config(
    materialized='view',
    schema='staging'
) }}

WITH raw_source AS (
    SELECT * FROM {{ source('raw_data', 'events_raw') }}
),

flattened AS (
    SELECT
        raw_payload:event_id::VARCHAR AS event_id,
        raw_payload:user_id::NUMBER(38, 0) AS user_id,
        raw_payload:event_name::VARCHAR AS event_name,
        raw_payload:properties:transaction_amount::FLOAT AS transaction_amount,
        raw_payload:properties:currency::VARCHAR AS currency,
        raw_payload:timestamp::TIMESTAMP_NTZ AS event_timestamp,
        source_filename,
        ingested_at
    FROM raw_source
)

SELECT * FROM flattened

```

### C. CI/CD Pipeline (`.github/workflows/dbt_ci_cd.yml`)

```yaml
# Generated by DataMorph DevOps Agent
name: Data Pipeline Continuous Integration

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 4 * * *' # Daily drift detection at 04:00 UTC

jobs:
  validate-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
          dbt deps --project-dir dbt_project

      - name: Run Schema Drift Validation
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
        run: |
          python scripts/scheduled_drift_check.py

      - name: Run dbt Staging & Tests
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
        run: |
          cd dbt_project
          dbt compile --target ci
          dbt test --target ci

```

---

## 7. Step-by-Step Implementation Roadmap

1. **Phase 1: Profiling Engine (Local DuckDB & PyArrow)**
* Implement storage wrappers for AWS S3, Azure Blob, and GCS using `fsspec`.
* Build auto-profiling functions in DuckDB to return column name, null fraction, sampled distinct values, and data types.


2. **Phase 2: Ingestion & DDL Code Synthesizers**
* Create templated emitters for Snowflake (`FILE FORMAT`, `STAGE`, `COPY INTO`) and Redshift (`EXTERNAL SCHEMA`, `COPY`).
* Implement idempotent rerun logic and error logging.


3. **Phase 3: dbt Project Generator**
* Develop Jinja templates for `dbt_project.yml`, `sources.yml`, and `schema.yml`.
* Add parsing logic to unnest JSON payloads into SQL staging view columns.


4. **Phase 4: Schema Evolution & State Tracking**
* Store historical schema metadata in SQLite / PostgreSQL.
* Build reconciliation rules that generate Git pull requests whenever upstream schemas change.


5. **Phase 5: Reverse-ETL & CI/CD Generator**
* Implement automated generation of GitHub Actions and GitLab CI files.
* Build reverse ETL pipelines to export clean data back to cloud storage.



---

## 8. Getting Started

### Prerequisites

* Python 3.11+
* Snowflake / Redshift warehouse credentials
* AWS / Azure / GCP storage bucket access keys

### Installation

```bash
git clone [https://github.com/your-org/datamorph-agent.git](https://github.com/your-org/datamorph-agent.git)
cd datamorph-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### Execution

```bash
# Run one-off discovery, warehouse DDL, and dbt generation
python scripts/run_agent.py \\
  --source-uri "s3://my-lakehouse-bucket/incoming/events/" \\
  --format json \\
  --target snowflake \\
  --generate-cicd \\
  --generate-dbt

```

"""

with open("README.md", "w") as f:
f.write(readme_content)

print("File README.md successfully created!")

```

```text?code_stdout&code_event_index=1
File README.md successfully created!


```

Your Markdown file is ready:


---

### Complete Markdown Text for your `README.md`

You can copy and paste this directly into your GitHub repository's `README.md` or use the generated file above:

```markdown
# DataMorph Agent (Autonomous Data Engineering Super-Agent)

**DataMorph Agent** is an end-to-end, LLM-powered autonomous data engineering engine designed to automate the modern ELT/ETL lifecycle. It inspects raw structured and semi-structured cloud files (CSV, Parquet, JSON), configures cloud ingestion stages (Snowflake & Redshift), synthesizes complete dbt projects (sources, staging views, marts, tests), monitors daily schema evolution, and scaffolds robust CI/CD pipelines.

---

## 1. Executive Summary & Core Value Proposition

Modern data engineering teams spend significant manual effort on routine plumbing:
- Inspecting source file schemas (especially polymorphic or deeply nested JSON).
- Writing cloud data warehouse ingestion DDLs (`STORAGE INTEGRATION`, `STAGE`, `COPY INTO`, `EXTERNAL SCHEMA`).
- Writing boilerplate `dbt` staging models, data typing casts, and `schema.yml` assertions.
- Debugging pipeline breakage caused by upstream schema drift (added fields, mutated types).
- Creating and maintaining CI/CD orchestration scripts.

**DataMorph Agent** turns raw object storage into production-ready analytical marts autonomously. By fusing local, deterministic schema profiling (via DuckDB / PyArrow) with an intelligent multi-agent orchestration graph (LangGraph / CrewAI), it eliminates manual boilerplate while enforcing type safety, idempotency, and automated pipeline regression testing.

---

## 2. Key Features

- **Multi-Cloud Storage Detection**: Autonomous discovery and inspection across **AWS S3**, **Azure Blob Storage / ADLS Gen2**, and **Google Cloud Storage (GCS)**.
- **Multi-Format Ingestion**: Native parsing and type inference for **Parquet**, **JSON / JSON Lines**, and delimited **CSV/TSV** datasets.
- **Warehouse Target Support**:
  - **Snowflake**: Automates Storage Integrations, External Stages, File Formats, `COPY INTO`, Snowpipes, Streams, and Tasks.
  - **Amazon Redshift**: Generates IAM roles, Redshift Spectrum External Tables, Staging Tables, and `UNLOAD` commands.
- **Automated dbt Synthesis**:
  - Generates `sources.yml` complete with schema descriptions and fresh checks.
  - Generates staging SQL models (`stg_*.sql`) with automated nested JSON flattening (Snowflake `:` / `FLATTEN()`, Redshift `JSON_EXTRACT_PATH_TEXT`).
  - Generates `schema.yml` with basic assertions (`not_null`, `unique`, `accepted_values`).
- **Schema Drift & Reconciliation Engine**: Daily cron-based introspection tracking schema delta hashes against warehouse metadata catalogs, auto-generating migration DDLs (`ALTER TABLE ... ADD COLUMN`) and git commits.
- **Automated CI/CD Orchestration**: Generates GitHub Actions and GitLab CI workflows that execute dynamic linting (`sqlfluff`), staging builds (`dbt compile`, `dbt test`), and continuous deployment.
- **Bi-Directional Data Flow (Reverse ETL / Egress)**: Built-in functionality to export curated views or tables back into cloud object storage in standard formats (Parquet/CSV) for downstream ML models or external consumption.

---

## 3. High-Level System Architecture


```

```
             ┌────────────────────────────────────────────────────────┐
             │          Raw Data Ingestion Sources                    │
             │   - AWS S3 (CSV, Parquet, Nested JSON)                 │
             │   - Azure Blob / ADLS Gen2                             │
             │   - Google Cloud Storage (GCS)                         │
             └──────────────────────────┬─────────────────────────────┘
                                        │
                                        ▼

```

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           1. PROFILING & DISCOVERY ENGINE                       │
│  - DuckDB / PyArrow: Zero-copy sampling (first 10k rows)                        │
│  - Type Inferrer: Polymorphism resolution & null-density calculation            │
│  - Schema Extractor: JSON path flattener & structural hash generator            │
└───────────────────────────────────────────┬─────────────────────────────────────┘
│ Metadata Payload
▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    2. MULTI-AGENT ORCHESTRATOR (LangGraph Core)                 │
│                                                                                 │
│   ┌──────────────────────────┐                   ┌──────────────────────────┐   │
│   │   Ingestion DDL Agent    │                   │    dbt Synthesis Agent   │   │
│   │  - Stage & File Formats  │                   │  - sources.yml & models  │   │
│   │  - COPY INTO / Snowpipe  │                   │  - Flattening & Casts    │   │
│   └─────────────┬────────────┘                   └────────────┬─────────────┘   │
│                 │                                             │                 │
│                 ▼                                             ▼                 │
│   ┌──────────────────────────┐                   ┌──────────────────────────┐   │
│   │   Schema Drift Agent     │                   │    CI/CD & Egress Agent  │   │
│   │  - Hash comparisons      │                   │  - GitHub / GitLab CI    │   │
│   │  - Migration DDL PRs     │                   │  - Reverse ETL / Unload  │   │
│   └──────────────────────────┘                   └──────────────────────────┘   │
└───────────────────────────────────────────┬─────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          3. DATA PLATFORM EXECUTION LAYER                       │
│                                                                                 │
│    Snowflake / Amazon Redshift                    GitHub Actions / Orchestration│
│   ┌──────────────────────────┐                   ┌──────────────────────────┐   │
│   │ Raw Layer (Stages/Tables)│                   │ Auto PRs / Daily Run     │   │
│   │ Silver (dbt Staging)     │ ◀─────────────────│ dbt build / dbt test     │   │
│   │ Gold (Curated Marts)     │                   │ Schema Drift Triggers    │   │
│   └──────────────────────────┘                   └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘

```

---

## 4. Multi-Agent Workflow Specification

The system is organized into specialized autonomous agents coordinated by a state graph:

### Agent 1: Profiler & Cataloger
- **Action**: Connects to the cloud URI via read-only credentials, reads header signatures, and samples files.
- **Engine**: Runs embedded DuckDB to read remote files directly (`read_parquet()`, `read_json_auto()`, `read_csv_auto()`).
- **Output**: Generates a standardized JSON Schema contract documenting fields, data types, nullability, and JSON nesting hierarchy.

### Agent 2: Ingestion Engineer
- **Action**: Determines the target platform and emits warehouse-native data pipeline objects.
- **Capabilities**:
  - **Snowflake**: Writes SQL for `CREATE STORAGE INTEGRATION`, `CREATE FILE FORMAT`, `CREATE STAGE`, and idempotent `COPY INTO` commands.
  - **Redshift**: Writes SQL for IAM role association, Redshift Spectrum external schemas, and target staging tables with distribution and sort keys.

### Agent 3: dbt Analytics Engineer
- **Action**: Scaffolds a complete dbt-core project structure.
- **Capabilities**:
  - Emits `models/staging/sources.yml` and documentation blocks.
  - Emits `models/staging/stg_<source>__<entity>.sql` containing dialect-correct data parsing and column renames.
  - Emits `models/staging/schema.yml` with basic assertions (`unique`, `not_null`).

### Agent 4: Drift & Evolution Monitor
- **Action**: Runs on a daily schedule (or webhook trigger). Computes the checksum of incoming source schemas and compares it to the local catalog state.
- **Capabilities**:
  - **Additive Change**: Emits `ALTER TABLE ... ADD COLUMN` and appends new column mapping in dbt staging models.
  - **Breaking Change (Type mutation / Column dropped)**: Generates an incident report, quarantines unexpected formats into an exception table, and prevents downstream model failures.

### Agent 5: DevOps & CI/CD Engineer
- **Action**: Scaffolds workflow automation files.
- **Capabilities**:
  - Generates `.github/workflows/data_pipeline_ci.yml`.
  - Configures PR validation: lints SQL with `sqlfluff`, spins up a slim CI environment in Snowflake/Redshift, runs `dbt run --select state:modified+` and `dbt test`.

### Agent 6: Egress / Reverse ETL Agent
- **Action**: Automates downstream consumption workflows.
- **Capabilities**:
  - Generates parameterized export tasks using Snowflake `COPY INTO @stage/export/` or Redshift `UNLOAD ('SELECT * FROM ...') TO 's3://...' FORMAT AS PARQUET` for external data sharing.

---

## 5. Repository Directory Structure

```plaintext
datamorph-agent/
├── .github/
│   └── workflows/
│       ├── daily_drift_detector.yml
│       └── dbt_ci_cd.yml
├── config/
│   ├── connections.yml            # Cloud & Warehouse credentials
│   └── agent_rules.yml            # Rules for transformations and drift handling
├── core/
│   ├── __init__.py
│   ├── orchestrator.py            # LangGraph StateGraph engine
│   ├── profiler.py                # DuckDB / PyArrow local profiling engine
│   ├── state.py                   # Graph state management
│   └── agents/
│       ├── ingestion_agent.py     # Stage, Format & COPY generator
│       ├── dbt_agent.py           # dbt SQL, source.yml & schema.yml generator
│       ├── drift_agent.py         # Schema drift reconciliation logic
│       ├── cicd_agent.py          # GitHub Actions / CI pipeline builder
│       └── egress_agent.py        # Reverse ETL / UNLOAD generator
├── dbt_project/                   # Autonomous dbt workspace created by Agent
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── macros/
│   └── models/
│       ├── staging/
│       │   ├── sources.yml
│       │   ├── schema.yml
│       │   └── stg_s3__events.sql
│       └── marts/
├── scripts/
│   ├── run_agent.py               # Main CLI entry point
│   └── scheduled_drift_check.py   # Daily runner script
├── tests/
│   ├── test_profiler.py
│   └── test_dbt_generation.py
├── requirements.txt
└── README.md

```

---

## 6. Sample Artifacts Generated by DataMorph

### A. Snowflake Ingestion SQL (`snowflake_ingest.sql`)

```sql
-- Generated by DataMorph Ingestion Agent
CREATE OR REPLACE FILE FORMAT analytics.raw.ff_json_streaming
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE
    IGNORE_UTF8_ERRORS = TRUE;

CREATE OR REPLACE STAGE analytics.raw.stage_s3_events
    STORAGE_INTEGRATION = s3_int_prod
    URL = 's3://data-lake-landing/events/'
    FILE_FORMAT = analytics.raw.ff_json_streaming;

CREATE TABLE IF NOT EXISTS analytics.raw.events_raw (
    raw_payload VARIANT,
    ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    source_filename VARCHAR(512)
);

COPY INTO analytics.raw.events_raw (raw_payload, source_filename)
FROM (
    SELECT 
        $1, 
        METADATA$FILENAME 
    FROM @analytics.raw.stage_s3_events
)
FILE_FORMAT = (FORMAT_NAME = analytics.raw.ff_json_streaming)
ON_ERROR = 'CONTINUE';

```

### B. dbt Staging Model (`stg_s3__events.sql`)

```sql
-- Generated by DataMorph dbt Agent
{{ config(
    materialized='view',
    schema='staging'
) }}

WITH raw_source AS (
    SELECT * FROM {{ source('raw_data', 'events_raw') }}
),

flattened AS (
    SELECT
        raw_payload:event_id::VARCHAR AS event_id,
        raw_payload:user_id::NUMBER(38, 0) AS user_id,
        raw_payload:event_name::VARCHAR AS event_name,
        raw_payload:properties:transaction_amount::FLOAT AS transaction_amount,
        raw_payload:properties:currency::VARCHAR AS currency,
        raw_payload:timestamp::TIMESTAMP_NTZ AS event_timestamp,
        source_filename,
        ingested_at
    FROM raw_source
)

SELECT * FROM flattened

```

### C. CI/CD Pipeline (`.github/workflows/dbt_ci_cd.yml`)

```yaml
# Generated by DataMorph DevOps Agent
name: Data Pipeline Continuous Integration

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 4 * * *' # Daily drift detection at 04:00 UTC

jobs:
  validate-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
          dbt deps --project-dir dbt_project

      - name: Run Schema Drift Validation
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
        run: |
          python scripts/scheduled_drift_check.py

      - name: Run dbt Staging & Tests
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
        run: |
          cd dbt_project
          dbt compile --target ci
          dbt test --target ci

```

---

## 7. Step-by-Step Implementation Roadmap

1. **Phase 1: Profiling Engine (Local DuckDB & PyArrow)**
* Implement storage wrappers for AWS S3, Azure Blob, and GCS using `fsspec`.
* Build auto-profiling functions in DuckDB to return column name, null fraction, sampled distinct values, and data types.


2. **Phase 2: Ingestion & DDL Code Synthesizers**
* Create templated emitters for Snowflake (`FILE FORMAT`, `STAGE`, `COPY INTO`) and Redshift (`EXTERNAL SCHEMA`, `COPY`).
* Implement idempotent rerun logic and error logging.


3. **Phase 3: dbt Project Generator**
* Develop Jinja templates for `dbt_project.yml`, `sources.yml`, and `schema.yml`.
* Add parsing logic to unnest JSON payloads into SQL staging view columns.


4. **Phase 4: Schema Evolution & State Tracking**
* Store historical schema metadata in SQLite / PostgreSQL.
* Build reconciliation rules that generate Git pull requests whenever upstream schemas change.


5. **Phase 5: Reverse-ETL & CI/CD Generator**
* Implement automated generation of GitHub Actions and GitLab CI files.
* Build reverse ETL pipelines to export clean data back to cloud storage.



---

## 8. Getting Started

### Prerequisites

* Python 3.11+
* Snowflake / Redshift warehouse credentials
* AWS / Azure / GCP storage bucket access keys

### Installation

```bash
git clone [https://github.com/your-org/datamorph-agent.git](https://github.com/your-org/datamorph-agent.git)
cd datamorph-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### Execution

```bash
# Run one-off discovery, warehouse DDL, and dbt generation
python scripts/run_agent.py \
  --source-uri "s3://my-lakehouse-bucket/incoming/events/" \
  --format json \
  --target snowflake \
  --generate-cicd \
  --generate-dbt

```

```

```
