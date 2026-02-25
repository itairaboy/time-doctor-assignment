# Senior Data Analyst Assignment

This repository contains my work for the Senior Data Analyst assignment.

## Context

- Scenario: B2B Project Management SaaS (Jira-inspired)
- Focus: product usage, engagement, retention, and productivity
- Out of scope: employee monitoring and time tracking

## Progress by Stage

- Stage 1 - Setup and data model: completed
- Stage 2 - Synthetic data: completed
- Stage 3 - Transformations and metrics: in progress (MVP implemented)
- Stage 4 - Dashboard: pending
- Stage 5 - Monitoring and recommendations: pending

## Repository Structure

- `docs/data-model.md` - entities, relationships, taxonomy, and assumptions
- `docs/data-gen.md` - generation plan, parameters, imperfections, and guardrails
- `docs/assumptions-metrics-log.md` - assumptions and metrics log
- `python/synthetic_data/` - synthetic data generators and config
- `python/pipeline/run_models.py` - SQL model runner (DuckDB)
- `models/staging/` - raw standardization models (`stg_*`)
- `models/intermediate/` - enriched and metric-foundation models (`int_*`)
- `models/marts/` - analytics-ready marts (`mart_*`)
- `data/raw/` - generated raw CSV files
- `data/project.duckdb` - local DuckDB database

## Generate Synthetic Data

From repository root:

```bash
PYTHONPATH=python .venv/bin/python -m synthetic_data.main
```

Alternative:

```bash
PYTHONPATH=python python3 -m synthetic_data.main
```

Generated raw files are written to:

- `data/raw/accounts.csv`
- `data/raw/users.csv`
- `data/raw/projects.csv`
- `data/raw/tasks.csv`
- `data/raw/events.csv`

## Run Transformations

Build all SQL layers into DuckDB:

```bash
.venv/bin/python python/pipeline/run_models.py
```

The pipeline builds:

- Staging views (`stg_*`)
- Intermediate views (`int_*`) using dependency-aware ordering
- Mart tables (`mart_*`)

