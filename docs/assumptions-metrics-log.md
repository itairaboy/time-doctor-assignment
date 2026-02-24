 # Assumptions and metrics log

 ## Assumptions

| ID | Assumption | Status | Last updated |
|-|-|-|-|
| A-01 | Company is a B2B SaaS for project management (Jira-inspired) | Confirmed | 2026-02-23 |
| A-02 | Avoid time-tracking and employee monitoring | Confirmed | 2026-02-23 |
| A-03 | Keep transformations simple, MVP-style. SQL-Only, describe production approach in presentation | Confirmed | 2026-02-23 |
| A-04 | Timestamps stored in UTC | Pending | 2026-02-23 |

## Metrics
| ID | Metric | Business question | Definition | Grain | Window |
|-|-|-|-|-|-|
| M-01 | Weekly Active Users (WAU) | Are users meaningfully active? | Distinct users with >=1 key event (listed below) | user-week | trailing 7d |
| M-02 | User Retention | Do newly active users come back after adoption? | For cohort `t` retained if active again in `t+4` | cohort-week | week+4 |
| M-03 | Account Retention | Do newly active accounts keep using the product? | For cohort `t` retained if active again in `t+4` | cohort-week | week+4 |

### Event Taxonomy
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
- 2026-02-23: Confirmed Active User and Retention definitions according to Slack