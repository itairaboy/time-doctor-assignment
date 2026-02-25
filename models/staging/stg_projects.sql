select
    trim(project_id)::varchar as project_id,
    trim(account_id)::varchar as account_id,
    trim(owner_user_id)::varchar as owner_user_id,
    nullif(trim(project_status), '')::varchar as project_status,
    created_at_utc::timestamptz as created_at_utc,
    completed_at_utc::timestamptz as completed_at_utc

from read_csv('data/raw/projects.csv', header = true, timestampformat = '%Y-%m-%d %H:%M:%S%z')