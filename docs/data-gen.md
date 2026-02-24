 1) Locked Definitions (from Stage 1)
- Active user: >=1 key event in trailing 7 days
- Retention lens: user retention primary, account retention secondary
- Transformation approach: SQL-only MVP (Stage 3)
- Time standard: UTC
- Out of scope: employee monitoring, time tracking

 2) Generation Parameters

| Parameter | Value | Notes |
|---|---|---|
| Random seed | 22 | Reproducibility |
| Date window start |  |  |
| Date window end |  |  |
| Accounts count |  |  |
| Users per account (min-max) |  |  |
| Projects per account (min-max) |  |  |
| Tasks per project (min-max) |  |  |

 3) Core Entity Assumptions

| Entity | Grain | Key | Required Relationships |
|---|---|---|---|
| accounts | 1 row/account | `account_id` | none |
| users | 1 row/user | `user_id` | `account_id -> accounts` |
| projects | 1 row/project | `project_id` | `account_id -> accounts`, `owner_user_id -> users` |
| tasks | 1 row/task | `task_id` | `account_id -> accounts`, `project_id -> projects`, user FKs |
| events | 1 row/event | `event_id` | `account_id -> accounts`, `user_id -> users` |

 4) Event Taxonomy

 Key events (drive active user / retention)
- `task_created`
- `task_completed`
- `handoff_completed`
- `blocker_resolved`

 Supporting events
- `login_succeeded`
- `dashboard_viewed`
- `work_note_added`
- `task_assigned`
- `task_status_changed`
- `blocker_added`
- `project_created`

 5) Lifecycle Rules (must hold)

- `created_at <= first_started_at <= completed_at` (when applicable)
- `event_at_utc <= ingested_at_utc`
- Task completion events only for tasks that reach done/completed status
- `project_id` and `account_id` consistency across related tables
- User activity cannot occur before user creation/activation

 6) Imperfections Plan (intentional)

| Imperfection | Target rate | Where | Reason |
|---|---|---|---|
| Missing nullable values |  | e.g., `assignee_user_id` | Real-world incompleteness |
| Outliers |  | e.g., long cycle times/due dates | Stress-test metrics |
| Late-arriving events |  | `ingested_at_utc > event_at_utc` | Pipeline realism |
| (Optional) internal/test accounts flagged |  | accounts/users | Exclusion logic testing |

 7) QA Guardrails Before Finalizing Stage 2
- No FK violations across all tables
- No impossible timestamps
- Key events present and not dominant by noise events
- Daily/weekly activity patterns look plausible (not perfectly flat)
- Imperfection rates match documented targets

 8) Stage 2 Deliverables
- Raw tables generated: `accounts`, `users`, `projects`, `tasks`, `events`
- Short generation notes (what was injected and why)
- Quick data profile (row counts + sanity checks)
- Updated assumptions/metrics log with any new decisions

 9) Open Decisions (if any)
- [ ] Late-event delay profile finalized
- [ ] Dataset size finalized
- [ ] Internal/test flagging included or not