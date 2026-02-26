# Config
SEED = 22
DATE_START = "2025-08-01"
DATE_END = "2026-02-26"
OUTPUT_DIR = "data/raw"

# Scale
N_ACCOUNTS = 80
USERS_PER_ACCOUNT = (8, 18)
PROJECTS_PER_ACCOUNT = (4, 8)
TASKS_PER_PROJECT = (10, 25)
EVENTS_PER_TASK = (2, 5)

# Imperfections
USER_DEACTIVATION_RATE = 0.07
MISSING_ASSIGNEE_RATE = 0.04
OUTLIER_TASK_RATE = 0.01
LATE_EVENT_PROFILE = {
    "same_day":  {"prob": 0.80, "low": 0, "high": 0},
    "within_3d": {"prob": 0.18, "low": 1, "high": 3},
    "within_7d": {"prob": 0.02, "low": 4, "high": 7},
}

# Business logic
## Accounts
PLAN_CONFIG = {
    "starter":    {"seats": (2,  15),  "prob": 0.55},
    "growth":     {"seats": (16, 60),  "prob": 0.30},
    "enterprise": {"seats": (61, 200), "prob": 0.15},
}

REGIONS = ["NA", "EMEA", "LATAM", "APAC"]
REGION_PROBS = [0.40, 0.35, 0.15, 0.10]

## Users
ROLES = ["admin", "manager", "member"]
ROLE_PROBS = [0.10, 0.25, 0.65]

## Projects
PROJECT_STATUSES = ["active", "completed", "archived"]
PROJECT_STATUS_PROBS = [0.60, 0.30, 0.10]

## Takss
TASK_STATUSES = ["backlog", "in_progress", "done", "cancelled"]
TASK_STATUS_PROBS = [0.25, 0.40, 0.30, 0.05]

TASK_PRIORITIES = ["low", "medium", "high", "critical"]
TASK_PRIORITY_PROBS = [0.20, 0.45, 0.30, 0.05]

BLOCKER_RATE = 0.10

## Events
TASK_STATUS_EVENTS = {
    "backlog":     ["task_created", "work_note_added"],
    "in_progress": ["task_assigned", "task_status_changed", "work_note_added"],
    "blocked":     ["blocker_added", "blocker_resolved", "work_note_added"],
    "done":        ["task_completed", "handoff_completed"],
    "cancelled":   ["task_status_changed"],
}

EVENT_TAXONOMY = {
    "account": [
        "login_succeeded",
        "dashboard_viewed",
    ],
    "project": [
        "project_created",
    ],
    "task": TASK_STATUS_EVENTS,
}