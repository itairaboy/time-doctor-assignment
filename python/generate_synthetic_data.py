import numpy as np
import pandas as pd
from faker import Faker

# --- Config ---
SEED = 22
DATE_START = "2025-08-01"
DATE_END = "2026-01-31"
OUTPUT_DIR = "data/raw"

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
DISALLOW_ACTIVITY_AFTER_ARCHIVE = True

# Business logic
## Accounts
PLAN_CONFIG = {
    "starter":    {"seats": (2,  15),  "prob": 0.55},
    "growth":     {"seats": (16, 60),  "prob": 0.30},
    "enterprise": {"seats": (61, 200), "prob": 0.15},
}

REGIONS = ["NA", "EMEA", "LATAM", "APAC"]
REGION_PROBS = [0.40, 0.35, 0.15, 0.10]  # NA/EMEA heavy

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

def generate_accounts(
    n: int,
    date_start: str,
    date_end: str,
    rng: np.random.Generator,
    fake: Faker,
) -> pd.DataFrame:
    start = pd.Timestamp(date_start, tz="UTC")
    end = pd.Timestamp(date_end, tz="UTC")
    total_days = (end - start).days

    plan_names = list(PLAN_CONFIG.keys())
    plan_probs = [v["prob"] for v in PLAN_CONFIG.values()]

    plans   = rng.choice(plan_names, size=n, p=plan_probs)
    regions = rng.choice(REGIONS, size=n, p=REGION_PROBS)
    seats   = np.array([
        rng.integers(*PLAN_CONFIG[p]["seats"], endpoint=True)
        for p in plans
    ])
    created_at = [
        start + pd.Timedelta(days=int(offset))
        for offset in rng.integers(0, total_days + 1, size=n)
    ]

    accounts = pd.DataFrame({
        "account_id":      [f"acc_{i:04d}" for i in range(1, n + 1)],
        "account_name":    [fake.company() for _ in range(n)],
        "plan_tier":       plans,
        "region":          regions,
        "seats_purchased": seats,
        "account_status":  "active", # All accounts active for MVP, Keeping data-model structure
        "created_at_utc":  created_at,
    })
    
    return accounts

def generate_users(
    accounts: pd.DataFrame,
    users_per_account: tuple[int, int],
    date_end: str,
    deactivation_rate: float,
    rng: np.random.Generator,
    fake: Faker,
) -> pd.DataFrame:
    end = pd.Timestamp(date_end, tz="UTC")

    n_users_per = rng.integers(*users_per_account, endpoint=True, size=len(accounts))
    account_ids = accounts["account_id"].repeat(n_users_per).to_numpy()
    account_created = pd.DatetimeIndex(
        accounts["created_at_utc"].repeat(n_users_per)
    )
    n_total = len(account_ids)

    windows         = ((end - account_created).days).to_numpy().astype(int)
    created_offsets = np.array([rng.integers(0, w + 1) for w in windows])
    created_at      = account_created + pd.to_timedelta(created_offsets, unit="D")
    activated_at = pd.DatetimeIndex(
        pd.Series(created_at + pd.to_timedelta(rng.integers(0, 4, size=n_total), unit="D"))
        .clip(upper=end)
    )

    users = pd.DataFrame({
        "user_id":            [f"usr_{i:05d}" for i in range(1, n_total + 1)],
        "account_id":         account_ids,
        "user_first_name":    [fake.first_name() for _ in range(n_total)],
        "user_last_name":     [fake.last_name() for _ in range(n_total)],
        "role_type":          rng.choice(ROLES, size=n_total, p=ROLE_PROBS),
        "user_status":        "active",
        "created_at_utc":     created_at,
        "activated_at_utc":   activated_at,
        "deactivated_at_utc": pd.array([pd.NaT] * n_total, dtype="datetime64[ns, UTC]"),
    })

    # Deactivation
    eligible    = users[users["activated_at_utc"] <= end - pd.Timedelta(days=7)]
    n_deactivated = round(n_total * deactivation_rate)

    if n_deactivated > 0 and len(eligible) > 0:
        n_deactivated = min(n_deactivated, len(eligible))
        deact_idx   = rng.choice(eligible.index, size=n_deactivated, replace=False)
        deact_start = users.loc[deact_idx, "activated_at_utc"] + pd.Timedelta(days=7)
        deact_range = ((end - deact_start).dt.days).astype(int).to_numpy()
        deact_offsets = np.array([rng.integers(0, r + 1) for r in deact_range])
        deactivated_at = deact_start + pd.to_timedelta(deact_offsets, unit="D")

        users.loc[deact_idx, "user_status"]        = "deactivated"
        users.loc[deact_idx, "deactivated_at_utc"] = deactivated_at

    return users.reset_index(drop=True)

def generate_projects(
    accounts: pd.DataFrame,
    users: pd.DataFrame,
    projects_per_account: tuple[int, int],
    date_end: str,
    rng: np.random.Generator,
) -> pd.DataFrame:
    end = pd.Timestamp(date_end, tz="UTC")

    # --- Expand accounts -> projects ---
    n_projects_per  = rng.integers(*projects_per_account, endpoint=True, size=len(accounts))
    account_ids     = accounts["account_id"].repeat(n_projects_per).to_numpy()
    acc_created_arr = accounts.set_index("account_id")["created_at_utc"][account_ids].to_numpy()
    n_total         = len(account_ids)

    # created_at
    acc_created_idx = pd.DatetimeIndex(acc_created_arr)
    windows    = (end - acc_created_idx).days.to_numpy().astype(int)
    created_at = acc_created_idx + pd.to_timedelta(
        [rng.integers(0, w + 1) for w in windows], unit="D"
    )

    # status
    statuses = rng.choice(PROJECT_STATUSES, size=n_total, p=PROJECT_STATUS_PROBS)

    # completed_at: only for completed/archived
    completed_at = pd.Series(pd.NaT, index=range(n_total), dtype="datetime64[ns, UTC]")
    closed_mask  = np.isin(statuses, ["completed", "archived"])
    closed_idx   = np.where(closed_mask)[0]
    closed_windows = (end - created_at[closed_idx]).days.astype(int)
    completed_at.iloc[closed_idx] = pd.Series(
        created_at[closed_idx] + pd.to_timedelta(
            [rng.integers(1, max(w, 2)) for w in closed_windows], unit="D"
        )
    ).clip(upper=end).to_numpy()

    # owner: random user per account
    account_owners = users.groupby("account_id")["user_id"].apply(list).to_dict()
    owner_ids = [rng.choice(account_owners[aid]) for aid in account_ids]

    return pd.DataFrame({
        "project_id":       [f"prj_{i:05d}" for i in range(1, n_total + 1)],
        "account_id":       account_ids,
        "owner_user_id":    owner_ids,
        "project_status":   statuses,
        "created_at_utc":   created_at,
        "completed_at_utc": completed_at,
    }).reset_index(drop=True)

def generate_tasks(
    projects: pd.DataFrame,
    users: pd.DataFrame,
    tasks_per_project: tuple[int, int],
    date_end: str,
    rng: np.random.Generator,
) -> pd.DataFrame:
    end = pd.Timestamp(date_end, tz="UTC")

    # --- Expand projects -> tasks ---
    n_tasks_per  = rng.integers(*tasks_per_project, endpoint=True, size=len(projects))
    project_ids  = projects["project_id"].repeat(n_tasks_per).to_numpy()
    proj_index   = projects.set_index("project_id")
    account_ids  = proj_index["account_id"][project_ids].to_numpy()
    proj_created = proj_index["created_at_utc"][project_ids].to_numpy()
    n_total      = len(project_ids)

    # timestamps
    windows    = (end - pd.DatetimeIndex(proj_created)).days.to_numpy().astype(int)
    created_at = pd.DatetimeIndex(proj_created) + pd.to_timedelta(
        [rng.integers(0, w + 1) for w in windows], unit="D"
    )
    start_at = pd.DatetimeIndex(
        pd.Series(created_at + pd.to_timedelta(rng.integers(0, 4, size=n_total), unit="D"))
        .clip(upper=end)
    )
    due_at = start_at + pd.to_timedelta(rng.integers(3, 22, size=n_total), unit="D")

    # status & completed_at
    statuses     = rng.choice(TASK_STATUSES, size=n_total, p=TASK_STATUS_PROBS)
    completed_at = pd.Series(pd.NaT, index=range(n_total), dtype="datetime64[ns, UTC]")
    done_idx     = np.where(statuses == "done")[0]
    done_windows = (end - start_at[done_idx]).days.astype(int)
    completed_at.iloc[done_idx] = pd.Series(
        start_at[done_idx] + pd.to_timedelta(
            [rng.integers(1, max(w, 2)) for w in done_windows], unit="D"
        )
    ).clip(upper=end).to_numpy()
    
    # blocked tasks must be in_progress
    has_blocker = rng.random(size=n_total) < BLOCKER_RATE
    blocked_mask = has_blocker & (statuses == "in_progress")
    statuses[blocked_mask] = "blocked"

    # users per account — single lookup, reused for creator and assignee
    account_users = users.groupby("account_id")["user_id"].apply(list).to_dict()
    user_pool     = [account_users[aid] for aid in account_ids]  # resolve once
    created_by    = [rng.choice(pool) for pool in user_pool]
    assignee_ids  = [
        rng.choice(pool) if rng.random() > MISSING_ASSIGNEE_RATE else None
        for pool in user_pool
    ]
    

    return pd.DataFrame({
        "task_id":            [f"tsk_{i:06d}" for i in range(1, n_total + 1)],
        "account_id":         account_ids,
        "project_id":         project_ids,
        "created_by_user_id": created_by,
        "assignee_user_id":   assignee_ids,
        "task_status":        statuses,
        "priority":           rng.choice(TASK_PRIORITIES, size=n_total, p=TASK_PRIORITY_PROBS),
        "has_blocker":        has_blocker,
        "created_at_utc":     created_at,
        "start_at_utc":       start_at,
        "due_at_utc":         due_at,
        "completed_at_utc":   completed_at,
    }).reset_index(drop=True)
    
def generate_events(
    users: pd.DataFrame,
    tasks: pd.DataFrame,
    events_per_task: tuple[int, int],
    date_end: str,
    rng: np.random.Generator,
) -> pd.DataFrame:
    end = pd.Timestamp(date_end, tz="UTC")

    # Expand tasks -> events
    n_events_per = rng.integers(*events_per_task, endpoint=True, size=len(tasks))
    task_index   = tasks.set_index("task_id")[["account_id", "project_id", "created_at_utc"]]
    task_ids     = tasks["task_id"].repeat(n_events_per).to_numpy()
    task_index   = task_index.loc[task_ids]
    account_ids  = task_index["account_id"].to_numpy()
    project_ids  = task_index["project_id"].to_numpy()
    task_created = task_index["created_at_utc"].to_numpy()
    n_total      = len(task_ids)

    # event_at: after task creation, clamped to end
    windows  = (end - pd.DatetimeIndex(task_created)).days.to_numpy().astype(int)
    event_at = pd.DatetimeIndex(task_created) + pd.to_timedelta(
        [rng.integers(0, w + 1) for w in windows], unit="D"
    )

    # ingested_at: late-arriving via buckets
    buckets      = rng.choice(len(LATE_EVENT_PROFILE), size=n_total, p=[v["prob"] for v in LATE_EVENT_PROFILE.values()])
    bucket_vals  = np.array([(v["low"], v["high"]) for v in LATE_EVENT_PROFILE.values()])
    ingested_offsets = np.array([
        rng.integers(bucket_vals[b, 0], bucket_vals[b, 1] + 1) for b in buckets
    ])
    ingested_at = pd.Series(event_at + pd.to_timedelta(ingested_offsets, unit="D")).clip(upper=end)
    
    # entity: task, project, or account
    entity_types = rng.choice(list(EVENT_TAXONOMY.keys()), size=n_total)
    entity_ids   = np.where(
        entity_types == "task",     task_ids,
        np.where(entity_types == "project", project_ids, account_ids)
    )
    task_statuses = tasks.set_index("task_id")["task_status"][task_ids].to_numpy()
    event_names   = np.array([
        rng.choice(EVENT_TAXONOMY["task"][status]) if et == "task"
        else rng.choice(EVENT_TAXONOMY[et])
        for et, status in zip(entity_types, task_statuses)
    ])
    # user: random user from same account
    account_users = users.groupby("account_id")["user_id"].apply(list).to_dict()
    user_ids      = [rng.choice(account_users[aid]) for aid in account_ids]

    return pd.DataFrame({
        "event_id":        [f"evt_{i:07d}" for i in range(1, n_total + 1)],
        "account_id":      account_ids,
        "user_id":         user_ids,
        "event_name":      event_names,
        "entity_type":     entity_types,
        "entity_id":       entity_ids,
        "event_at_utc":    event_at,
        "ingested_at_utc": ingested_at,
    }).reset_index(drop=True)
    
