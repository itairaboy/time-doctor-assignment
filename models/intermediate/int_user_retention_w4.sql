-- Grain: 1 row per user

with params as (
    select timestamptz '2026-01-31 00:00:00+00:00' as fixed_date_utc
),

active_weeks as (
    select
        user_id,
        account_id,
        plan_tier,
        region,
        role_type,
        activity_week_start_utc,
        key_event_count
    from int_user_week_activity
    where is_active_week
      and not coalesce(has_post_deactivation_activity, false)
),

cohorts as (
    select
        user_id,
        account_id,
        plan_tier,
        region,
        role_type,
        activity_week_start_utc as cohort_week_start_utc,
        row_number() over (partition by user_id order by activity_week_start_utc) as rn
    from active_weeks a
    qualify rn = 1
)

select
    c.user_id,
    c.account_id,
    c.plan_tier,
    c.region,
    c.role_type,
    c.cohort_week_start_utc,
    c.cohort_week_start_utc + interval '4 weeks' as retention_target_week_start_utc,
    a.activity_week_start_utc as retained_week_start_utc,
    coalesce(a.key_event_count, 0) as retained_key_event_count,
    a.user_id is not null as is_retained_w4,
    1 as cohort_user_count

from cohorts c
left join active_weeks a
    on c.user_id = a.user_id
    and a.activity_week_start_utc = c.cohort_week_start_utc + interval '4 weeks'
cross join params p
where c.cohort_week_start_utc + interval '5 weeks' <= p.fixed_date_utc -- Only full weeks