# Senior Data Analyst Assignment

This repository contains my work for the Senior Data Analyst assignment.

## Current Status
- Stage 1: planning and data model skeleton
- Stage 2: synthetic data generation in progress
- Stage 3: SQL transformation MVP in progress

## Scenario
- B2B Project Management SaaS (Jira-inspired)
- Focus on workflow outcomes: usage, engagement, retention, productivity
- Out of scope: employee monitoring and time tracking

## Project Structure
- `docs/` - assumptions, model, and generation notes
- `python/synthetic_data/config.py` - generation configuration
- `python/synthetic_data/generators.py` - entity/event generators
- `python/synthetic_data/main.py` - orchestration and export
- `models/` - SQL transformation assets

## Generate Synthetic Data
From the repository root:

```bash
PYTHONPATH=python .venv/bin/python -m synthetic_data.main
```

If you are not using the virtual environment executable explicitly:

```bash
PYTHONPATH=python python3 -m synthetic_data.main
```

## Output
Generated raw files are written to:
- `data/raw/accounts.csv`
- `data/raw/users.csv`
- `data/raw/projects.csv`
- `data/raw/tasks.csv`
- `data/raw/events.csv`
