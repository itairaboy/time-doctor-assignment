select
    e.user_id,
    e.account_id,
    e.plan_tier,
    e.region,
    e.role_type,
    e.event_week_start_utc as activity_week_start_utc,

    -- volume
    count(*) as total_event_count,

    -- events
    count(*) filter (where e.is_key_event) as key_event_count,
    count(*) filter (where e.is_key_event) > 0 as is_active_week,
    count(*) filter (where not e.is_key_event) as supporting_event_count,
    count(*) filter (where e.is_late_event) as late_event_count,
    avg(ingestion_lag_days) as avg_ingestion_lag_days,

    -- Check for data quality
    max(case when u.deactivated_at_utc is not null and e.event_at_utc > u.deactivated_at_utc then 1 else 0 end) = 1 as has_post_deactivation_activity

from int_events_enriched e
left join int_users_enriched u on e.user_id = u.user_id
group by 1, 2, 3, 4, 5, 6