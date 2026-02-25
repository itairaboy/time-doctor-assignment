select
    -- event
    e.event_id,
    e.account_id,
    e.user_id,
    e.event_name,
    e.entity_type,
    e.entity_id,
    e.event_at_utc,
    e.ingested_at_utc,

    -- user
    u.user_first_name,
    u.user_last_name,
    u.user_first_name || ' ' || u.user_last_name as full_name,
    u.role_type,
    u.user_status,

    -- account
    a.account_name,
    a.plan_tier,
    a.region,

    -- cohorts
    date_trunc('week', e.event_at_utc) as event_week_start_utc,
    date_trunc('day',  e.event_at_utc) as event_day_utc,

    -- derived
    date_diff('day', e.event_at_utc, e.ingested_at_utc) as ingestion_lag_days,
    date_diff('day', e.event_at_utc, e.ingested_at_utc) > 0 as is_late_event,
    e.event_name in ('task_created','task_completed','handoff_completed','blocker_resolved') as is_key_event,
    

from stg_events e
left join stg_users u on e.user_id = u.user_id
left join stg_accounts a on e.account_id = a.account_id