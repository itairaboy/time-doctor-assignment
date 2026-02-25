-- Grain: 1 row per week_start_utc x plan_tier x region x role_type

with base as (
    select
        activity_week_start_utc as week_start_utc,
        account_id,
        user_id,
        plan_tier,
        region,
        role_type,
        total_event_count,
        key_event_count,
        supporting_event_count,
        late_event_count,
        avg_ingestion_lag_days,
        is_active_week
    from int_user_week_activity
    where not coalesce(has_post_deactivation_activity, false)
),

agg as (
    select
        week_start_utc,
        plan_tier,
        region,
        role_type,
        count(distinct account_id) as accounts_with_activity,
        count(distinct user_id) as users_with_any_activity,
        count(distinct user_id) filter (where is_active_week) as weekly_active_users,
        sum(total_event_count) as total_event_count,
        sum(key_event_count) as key_event_count,
        sum(supporting_event_count) as supporting_event_count,
        sum(late_event_count) as late_event_count,
        sum(avg_ingestion_lag_days * total_event_count)::double
            / nullif(sum(total_event_count), 0) as avg_ingestion_lag_days_weighted
    from base
    group by 1, 2, 3, 4
)

select
    week_start_utc,
    plan_tier,
    region,
    role_type,
    accounts_with_activity,
    users_with_any_activity,
    weekly_active_users,

    -- engagement rates
    round(weekly_active_users * 100.0 / nullif(users_with_any_activity, 0), 2) as active_among_engaged_users_pct,
    round(total_event_count::double / nullif(weekly_active_users, 0), 2) as avg_events_per_active_user,
    round(key_event_count::double / nullif(weekly_active_users, 0), 2) as avg_key_events_per_active_user,

    -- volume
    total_event_count,
    key_event_count,
    supporting_event_count,
    round(key_event_count * 100.0 / nullif(total_event_count, 0), 2) as key_event_share_pct,

    -- data quality
    late_event_count,
    round(late_event_count * 100.0 / nullif(total_event_count, 0), 2) as late_event_rate_pct,
    round(avg_ingestion_lag_days_weighted, 2) as avg_ingestion_lag_days

from agg
order by 1, 2, 3, 4