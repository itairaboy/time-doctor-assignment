# Data Model

- Status: Draft
- Stage: 1
- Last updated: 2026-02-23

## Context
This model represents a B2B Project Management SaaS where teams manage client work through projects, tasks, handoffs, and blockers.

## Scope Boundaries
- In scope: project/task flow, handoffs, blockers
- Out of scope: employee monitoring, activity surveillance, time tracking

## Principles
- Keep it realistic and easy to explain
- Treat as an MVP
- Put business logic in transformations, not raw tables
- Timestamps stored in UTC

## Entities

### Accounts
- Grain: 1 row per account
- PK: `account_id`
- Purpose: account segmentation and lifecycle
- Key fields: status, plan tier, region, seats purchased, created timestamp

### Users
- Grain: 1 row per user
- PK: `user_id`
- FK: `account_id` -> Accounts
- Purpose: user lifecycle and role context
- Key fields: role type, status, first name, last name, created/activated/deactivated timestamps

### Projects
- Grain: 1 row per project
- PK: `project_id`
- FKs: `account_id` -> Accounts, `owner_user_id` -> Users
- Purpose: client work container
- Key fields: project status, created/completed timestamps

### Tasks
- Grain: 1 row per task
- PK: `task_id`
- FKs: `account_id` -> Accounts, `project_id` -> Projects, `created_by_user_id` -> Users, `assignee_user_id` -> Users (nullable)
- Purpose: core productivity unit
- Key fields: task status, priority, has blocker, created/start/completed/due timestamps

### Events
- Grain: 1 row per event
- PK: `event_id`
- FKs: `account_id` -> Accounts, `user_id` -> Users
- Purpose: behavior stream for engagement and retention metrics
- Key fields: event name, entity type/id, `event_at_utc`, `ingested_at_utc`

## Relationships
- Accounts 1:N Users
- Accounts 1:N Projects
- Projects 1:N Tasks
- Users 1:N Tasks (creator/assignee)
- Users 1:N Events

## Initial Event Taxonomy
- `login_succeeded`
- `dashboard_viewed`
- `project_created`
- `task_created`
- `task_assigned`
- `task_status_changed`
- `task_completed`
- `handoff_completed`
- `blocker_added`
- `blocker_resolved`
- `work_note_added`

## Data Imperfections
- Missing values (in nullable fields)
- Outliers in dates and cycle times
- Late-arriving events (`ingested_at_utc` > `event_at_utc`)

## Open Decisions
- Late-event delay window
- Naming conventions for metrics and datasets
- Canonical definition of handoff
- Blocker severity/SLA thresholds
