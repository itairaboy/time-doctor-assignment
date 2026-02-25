-- Grain: 1 row per week_start_utc x plan_tier x region

with created as (
    select
        created_week_start_utc as week_start_utc,
        plan_tier,
        region,
        count(*) as tasks_created,
        round(avg(is_blocked::double) * 100, 2) as blocked_task_rate_created_pct,
        round(avg(is_unassigned::double) * 100, 2) as unassigned_task_rate_created_pct
    from int_tasks_enriched
    group by 1, 2, 3
),

completed as (
    select
        completed_week_start_utc as week_start_utc,
        plan_tier,
        region,
        count(*) filter (where is_completed) as tasks_completed,
        median(cycle_days) filter (where is_completed and not is_outlier_due_date) as median_cycle_time_days,
        round(avg(case when is_completed then (days_past_due <= 0)::double end) * 100, 2) as on_time_completion_rate_pct
    from int_tasks_enriched
    where completed_week_start_utc is not null
    group by 1, 2, 3
)

select
    coalesce(c.week_start_utc, d.week_start_utc) as week_start_utc,
    coalesce(c.plan_tier, d.plan_tier) as plan_tier,
    coalesce(c.region, d.region) as region,

    -- volume
    coalesce(c.tasks_created, 0) as tasks_created,
    coalesce(d.tasks_completed, 0) as tasks_completed,

    -- are tasks being completed as fast as they're created?
    round(coalesce(d.tasks_completed, 0) * 100.0 / nullif(coalesce(c.tasks_created, 0), 0), 2) as completion_throughput_pct,

    -- timings
    round(d.median_cycle_time_days, 2) as median_cycle_time_days,

    -- quality
    d.on_time_completion_rate_pct,
    c.blocked_task_rate_created_pct,
    c.unassigned_task_rate_created_pct

from created c
full outer join completed d
    on c.week_start_utc = d.week_start_utc
    and c.plan_tier = d.plan_tier
    and c.region = d.region

order by 1, 2, 3