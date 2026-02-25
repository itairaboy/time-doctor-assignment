with activity as (
    select
        activity_week_start_utc as week_start_utc,
        count(distinct user_id) as users_with_any_activity,
        count(distinct user_id) filter (where is_active_week) as weekly_active_users,
        sum(total_event_count) as total_event_count,
        sum(key_event_count) as key_event_count,
        sum(late_event_count) as late_event_count,
        sum(avg_ingestion_lag_days * total_event_count)::double
            / nullif(sum(total_event_count), 0) as avg_ingestion_lag_days
    from int_user_week_activity
    where not coalesce(has_post_deactivation_activity, false)
    group by 1
),

retention as (
    select
        cohort_week_start_utc as week_start_utc,
        sum(cohort_user_count) as retention_cohort_size,
        count(*) filter (where is_retained_w4) as retained_users_w4
    from int_user_retention_w4
    group by 1
),

created_tasks as (
    select
        created_week_start_utc as week_start_utc,
        count(*) as tasks_created,
        avg(is_blocked::double) * 100 as blocked_task_rate_created_pct,
        avg(is_unassigned::double) * 100 as unassigned_task_rate_created_pct
    from int_tasks_enriched
    group by 1
),

completed_tasks as (
    select
        completed_week_start_utc as week_start_utc,
        count(*) filter (where is_completed) as tasks_completed,
        median(cycle_days) filter (where is_completed and not is_outlier_due_date) as median_cycle_time_days,
        avg(case when is_completed then (days_past_due <= 0)::double end) * 100 as on_time_completion_rate_pct
    from int_tasks_enriched
    where completed_week_start_utc is not null
    group by 1
),

productivity as (
    select
        coalesce(c.week_start_utc, d.week_start_utc) as week_start_utc,
        coalesce(c.tasks_created, 0) as tasks_created,
        coalesce(d.tasks_completed, 0) as tasks_completed,
        c.blocked_task_rate_created_pct,
        c.unassigned_task_rate_created_pct,
        d.median_cycle_time_days,
        d.on_time_completion_rate_pct
    from created_tasks c
    full outer join completed_tasks d
        on c.week_start_utc = d.week_start_utc
),

weeks as (
    select week_start_utc from activity
    union
    select week_start_utc from retention
    union
    select week_start_utc from productivity
),

final as (
    select
        w.week_start_utc,

        -- engagement
        coalesce(a.weekly_active_users, 0) as weekly_active_users,
        lag(coalesce(a.weekly_active_users, 0)) over (order by w.week_start_utc) as wau_prev_week,
        coalesce(a.users_with_any_activity, 0) as users_with_any_activity,
        coalesce(a.total_event_count, 0) as total_event_count,
        coalesce(a.key_event_count, 0) as key_event_count,
        coalesce(a.late_event_count, 0) as late_event_count,
        coalesce(a.avg_ingestion_lag_days, 0) as avg_ingestion_lag_days,

        -- retention
        coalesce(r.retention_cohort_size, 0) as retention_cohort_size,
        coalesce(r.retained_users_w4, 0) as retained_users_w4,
        round(coalesce(r.retained_users_w4, 0) * 100.0 
            / nullif(coalesce(r.retention_cohort_size, 0), 0), 2) as retention_rate_w4_pct,

        -- productivity
        coalesce(p.tasks_created, 0) as tasks_created,
        coalesce(p.tasks_completed, 0) as tasks_completed,
        p.blocked_task_rate_created_pct,
        p.unassigned_task_rate_created_pct,
        p.median_cycle_time_days,
        p.on_time_completion_rate_pct

    from weeks w
    left join activity a on w.week_start_utc = a.week_start_utc
    left join retention r on w.week_start_utc = r.week_start_utc
    left join productivity p on w.week_start_utc = p.week_start_utc
)

select
    week_start_utc,

    -- engagement
    weekly_active_users,
    wau_prev_week,
    round((weekly_active_users - wau_prev_week) * 100.0 / nullif(wau_prev_week, 0), 2) as wau_wow_pct,
    users_with_any_activity,
    round(weekly_active_users * 100.0 / nullif(users_with_any_activity, 0), 2) as active_among_engaged_users_pct,
    total_event_count,
    key_event_count,
    round(key_event_count * 100.0 / nullif(total_event_count, 0), 2) as key_event_share_pct,
    late_event_count,
    round(late_event_count * 100.0 / nullif(total_event_count, 0), 2) as late_event_rate_pct,
    round(avg_ingestion_lag_days, 2) as avg_ingestion_lag_days,

    -- retention
    retention_cohort_size,
    retained_users_w4,
    retention_rate_w4_pct,
    round(avg(retention_rate_w4_pct) over (
        order by week_start_utc rows between 3 preceding and current row), 2) as retention_rate_w4_4w_ma, -- 4-week moving average

    -- productivity
    tasks_created,
    tasks_completed,
    round(tasks_completed * 100.0 / nullif(tasks_created, 0), 2) as completion_throughput_pct,
    round(median_cycle_time_days, 2) as median_cycle_time_days,
    round(on_time_completion_rate_pct, 2) as on_time_completion_rate_pct,
    round(blocked_task_rate_created_pct, 2) as blocked_task_rate_created_pct,
    round(unassigned_task_rate_created_pct, 2) as unassigned_task_rate_created_pct

from final
order by 1