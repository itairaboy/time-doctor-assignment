# Senior Data Analyst Assignment

This repository contains my end-to-end work for a Senior Data Analyst assignment.

## Context

- Scenario: B2B Project Management SaaS (Jira-inspired)
- Focus: product usage, engagement, retention, and productivity
- Out of scope: employee monitoring and time tracking

## Stages

- Stage 1 - Setup and data model
- Stage 2 - Synthetic data
- Stage 3 - Transformations and metrics
- Stage 4 - Dashboard
- Stage 5 - Monitoring and recommendations

## Repository Structure

- [docs/data-model.md](docs/data-model.md) - canonical entities, relationships, taxonomy
- [docs/data-gen.md](docs/data-gen.md) - synthetic generation parameters and imperfections
- [docs/assumptions-metrics-log.md](docs/assumptions-metrics-log.md) - assumptions and metrics log
- [docs/kpi-definitions.md](docs/kpi-definitions.md) - KPI relevance and limitations
- [python/synthetic_data/](python/synthetic_data/) - synthetic data generators and config
- [python/pipeline/run_models.py](python/pipeline/run_models.py) - builds SQL models into DuckDB
- [python/pipeline/publish_to_postgres.py](python/pipeline/publish_to_postgres.py) - publishes marts to Postgres `reporting` schema
- [models/staging/](models/staging/) - raw standardization models (`stg_*`)
- [models/intermediate/](models/intermediate/) - enriched metric foundations (`int_*`)
- [models/marts/](models/marts/) - analytics-ready marts (`mart_*`)
- [docker-compose.yml](docker-compose.yml) - Metabase + Postgres reporting stack
- [data/raw/](data/raw/) - generated source CSVs
- [data/pipeline.duckdb](data/pipeline.duckdb) - transformation database
- [data/reporting.duckdb](data/reporting.duckdb) - optional BI copy
- [dashboard/screenshots](dashboard/screenshots/) - Dashboard screenshots

## Quickstart

1) Generate synthetic data

```bash
PYTHONPATH=python .venv/bin/python -m synthetic_data.main
```

2) Run transformation pipeline (DuckDB)

```bash
.venv/bin/python python/pipeline/run_models.py
```

3) Start reporting stack (Postgres + Metabase)

```bash
docker compose up -d
```

4) Publish marts from DuckDB to Postgres

```bash
.venv/bin/python python/pipeline/publish_to_postgres.py
```

5) Open Metabase

- URL: `http://localhost:3000`
- Database engine: PostgreSQL
- Host: `reporting-db`
- Port: `5432`
- DB: `reporting`
- User: `reporting_user`
- Password: `reporting_pass`
- Schema: `reporting`

## Raw Data Model
![Data Model Diagram](/docs/diagrams/db_model.png)

## Implemented Marts

- `mart_exec_scorecard_weekly`
- `mart_user_activity_weekly`
- `mart_user_retention_w4`
- `mart_task_productivity_weekly`
