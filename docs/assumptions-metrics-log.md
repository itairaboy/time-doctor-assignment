# Assumptions and metrics log

## Assumptions

| ID | Assumption | Status | Last updated |
|---|---|---|---|
| A-01 | Company is a B2B SaaS for project management (Jira-inspired) | Confirmed | 2026-02-26 |
| A-02 | Avoid time-tracking and employee monitoring | Confirmed | 2026-02-26 |
| A-03 | Keep transformations simple, MVP-style. SQL-only, describe production approach in presentation | Confirmed | 2026-02-26 |
| A-04 | Timestamps stored in UTC | Confirmed | 2026-02-26 |
| A-05 | Active user = >=1 key event in calendar week | Confirmed | 2026-02-26 |
| A-06 | Retention = strict point-in-time W+4 | Confirmed | 2026-02-26 |
| A-07 | Post-deactivation activity is excluded from KPI logic | Confirmed | 2026-02-26 |

## Metrics (MVP)

| ID | Metric | Business question | Definition | Grain | Window |
|---|---|---|---|---|---|
| M-01 | Weekly Active Users (WAU) | Are users meaningfully active? | Distinct users with >=1 key event | week | calendar week |
| M-02 | WAU WoW % | Is adoption growing or declining week-over-week? | `(WAU - previous WAU) / previous WAU` | week | weekly change |
| M-03 | W+4 User Retention % | Do newly active users come back after adoption? | `% of cohort users active exactly in cohort week + 4` | cohort-week | week+4 |
| M-04 | Completion Throughput % | Is work flowing through the product? | `tasks_completed / tasks_created` | week | calendar week |
| M-05 | Median Cycle Time (days) | How quickly is work delivered? | Median `cycle_days` for completed tasks (excluding outlier due dates) | week | completion week |
| M-06 | On-Time Completion % | Are teams delivering reliably? | `% completed tasks with days_past_due <= 0` | week | completion week |
| M-07 | Late Event Rate % | Is dashboard data trustworthy? | `% events where ingestion_lag_days > 0` | week | calendar week |

## Simple Scorecard

Leadership (weekly)
- WAU, WAU WoW %, W+4 Retention %, Completion Throughput %, Median Cycle Time, On-Time Completion %

Product/Solutions (regular monitoring)
- Same KPIs with segment cuts by `plan_tier`, `region`, and `role_type`
- Trust context: Late Event Rate % and ingestion lag

## Event Taxonomy

Key events
- task_created
- task_completed
- handoff_completed
- blocker_resolved

Supporting events
- login_succeeded
- dashboard_viewed
- work_note_added

## Change Log

- 2026-02-21: Initial draft created
- 2026-02-22: Added initial assumptions and metrics
- 2026-02-23: Confirmed initial active/retention definitions according to Slack
- 2026-02-26: Updated to calendar-week active logic, strict W+4 retention, and MVP scorecard metrics
