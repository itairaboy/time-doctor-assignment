with params as (
    select timestamptz '2026-01-31 00:00:00+00:00' as fixed_date_utc
)

select
    -- task
    t.task_id,
    t.account_id,
    t.project_id,
    t.created_by_user_id,
    t.assignee_user_id,
    t.task_status,
    t.priority,
    t.has_blocker,
    t.created_at_utc,
    t.start_at_utc,
    t.due_at_utc,
    t.completed_at_utc,

    -- project
    p.project_status,
    p.owner_user_id,

    -- account
    a.account_name,
    a.plan_tier,
    a.region,

    -- user (assignee)
    u.user_first_name || ' ' || u.user_last_name as assignee_full_name,
    u.role_type as assignee_role,

    -- cohorts
    date_trunc('week', t.created_at_utc) as created_week_start_utc,
    date_trunc('week', t.start_at_utc) as start_week_start_utc,
    date_trunc('week', t.completed_at_utc) as completed_week_start_utc,

    -- flags
    t.assignee_user_id is null as is_unassigned,
    t.task_status = 'done' as is_completed,
    t.task_status = 'cancelled' as is_cancelled,
    (t.task_status = 'blocked' or t.has_blocker) as is_blocked,
    case 
        when t.completed_at_utc is not null then t.due_at_utc < t.completed_at_utc
        else t.due_at_utc < p2.fixed_date_utc
    end as is_overdue,
    date_diff('day', t.start_at_utc, t.due_at_utc) > 30 as is_outlier_due_date,

    -- derived times/cycles
    date_diff('day', t.created_at_utc, t.start_at_utc) as lead_days,
    date_diff('day', t.start_at_utc, coalesce(t.completed_at_utc, p2.fixed_date_utc)) as cycle_days,
    date_diff('day', t.due_at_utc, coalesce(t.completed_at_utc, p2.fixed_date_utc)) as days_past_due -- negative means completed early

from stg_tasks t
left join stg_projects p on t.project_id = p.project_id
left join stg_accounts a on t.account_id = a.account_id
left join stg_users u on t.assignee_user_id = u.user_id
cross join params p2