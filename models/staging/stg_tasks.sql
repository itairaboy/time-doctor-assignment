select
    trim(task_id)::varchar as task_id,
    trim(account_id)::varchar as account_id,
    trim(project_id)::varchar as project_id,
    trim(created_by_user_id)::varchar as created_by_user_id,
    nullif(trim(assignee_user_id), '')::varchar as assignee_user_id,
    nullif(trim(task_status), '')::varchar as task_status,
    nullif(trim(priority), '')::varchar as priority,
    has_blocker::boolean as has_blocker,
    created_at_utc::timestamptz as created_at_utc,
    start_at_utc::timestamptz as start_at_utc,
    due_at_utc::timestamptz as due_at_utc,
    completed_at_utc::timestamptz as completed_at_utc

from read_csv('data/raw/tasks.csv', header = true, timestampformat = '%Y-%m-%d %H:%M:%S%z')