-- Grain: 1 row per cohort_week_start_utc x plan_tier x region x role_type

select
    cohort_week_start_utc,
    plan_tier,
    region,
    role_type,

    sum(cohort_user_count) as cohort_size,

    -- retention
    count(*) filter (where is_retained_w4) as retained_users,
    count(*) filter (where not is_retained_w4) as churned_users,

    -- retention rate
    round(
        count(*) filter (where is_retained_w4) * 100.0
        / nullif(sum(cohort_user_count), 0),
    2) as retention_rate_pct,

    -- engagement
    round(avg(retained_key_event_count) filter (where is_retained_w4), 2) as avg_key_events_retained

from int_user_retention_w4
group by 1, 2, 3, 4
order by 1, 2, 3, 4