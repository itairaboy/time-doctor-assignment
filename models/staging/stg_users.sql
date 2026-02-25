select
    trim(user_id)::varchar as user_id,
    trim(account_id)::varchar as account_id,
    nullif(trim(user_first_name), '')::varchar as user_first_name,
    nullif(trim(user_last_name), '')::varchar as user_last_name,
    nullif(trim(role_type), '')::varchar as role_type,
    nullif(trim(user_status), '')::varchar as user_status,
    created_at_utc::timestamptz as created_at_utc,
    activated_at_utc::timestamptz as activated_at_utc,
    deactivated_at_utc::timestamptz as deactivated_at_utc

from read_csv('data/raw/users.csv', header = true, timestampformat = '%Y-%m-%d %H:%M:%S%z')