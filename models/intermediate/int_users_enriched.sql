select
    -- user
    u.user_id,
    u.account_id,
    u.user_first_name,
    u.user_last_name,
    u.user_first_name || ' ' || u.user_last_name as full_name,
    u.role_type,
    u.user_status,
    u.created_at_utc,
    u.activated_at_utc,
    u.deactivated_at_utc,

    -- account
    a.account_name,
    a.plan_tier,
    a.region,

    -- cohorts
    date_trunc('week', u.created_at_utc) as created_week_start_utc,
    date_trunc('week', u.activated_at_utc) as activated_week_start_utc,
    date_trunc('week', u.deactivated_at_utc) as deactivated_week_start_utc,

    -- derived
    date_diff('day', u.created_at_utc, u.activated_at_utc) as activation_lag_days,
    date_diff('day', u.activated_at_utc, coalesce(u.deactivated_at_utc, timestamptz '2026-01-31 00:00:00+00:00')) as active_days, -- Fixed date instead of current_timestamp
    u.user_status = 'deactivated' as is_deactivated

from stg_users u
left join stg_accounts a on u.account_id = a.account_id