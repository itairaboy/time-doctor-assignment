# Data Generation Plan

- Status: Draft
- Stage: 2
- Last updated: 2026-02-24

## Locked Definitions
- Active user: >=1 key event in trailing 7 days
- Retention lens: user retention primary, account retention secondary
- Transformation approach: SQL-only MVP
- Time standard: UTC
- Out of scope: employee monitoring, time tracking

Note: canonical entities, relationships, and taxonomy live in `docs/data-model.md`.

## Generation Parameters

| Parameter | Value | Notes |
|---|---|---|
| Random seed | 22 | Reproducibility |
| Date window start | 2025-08-01 | Fixed full-month window |
| Date window end | 2026-01-31 | Fixed full-month window |
| Accounts count | 80 | Medium-size dataset |
| Users per account (min-max) | 8-18 | Targets ~1000 total users |
| Projects per account (min-max) | 4-8 | Balanced volume |
| Tasks per project (min-max) | 10-25 | Balanced volume |
| Events per task (min-max) | 2-5 | Supports trend metrics |
| Output format | CSV | Files exported to `data/raw/` |

## Lifecycle Rules
- `created_at_utc <= activated_at_utc` (users)
- `created_at_utc <= completed_at_utc` when project/task is closed
- `event_at_utc <= ingested_at_utc`
- Task completion events only for tasks in `done` status
- FK consistency across all generated tables

## Imperfections Plan

| Imperfection | Target rate/profile | Where | Reason |
|---|---|---|---|
| Missing values | 4% | `assignee_user_id` | Real-world incompleteness |
| Outliers | 1% | `due_at_utc` | Stress-test metrics |
| Late-arriving events | 80% same day, 18% in 1-3 days, 2% in 4-7 days | events | Pipeline realism |
| User deactivation | 7% | users | Lifecycle realism |

## QA Guardrails
- No FK violations across all tables
- No impossible timestamps
- Key events present and not dominated by low-signal events
- Daily/weekly activity patterns are plausible (not perfectly flat)
- Imperfection rates are close to configured targets

## Stage 2 Deliverables
- Raw data files: `accounts.csv`, `users.csv`, `projects.csv`, `tasks.csv`, `events.csv`
- Generation code under `python/synthetic_data/`
- Basic run summary (row counts per table)

## Open Decisions
- Canonical definition of handoff for interpretation
- Blocker severity/SLA thresholds
