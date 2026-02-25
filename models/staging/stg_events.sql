select
    trim(event_id)::varchar as event_id,
    trim(account_id)::varchar as account_id,
    trim(user_id)::varchar as user_id,
    nullif(trim(event_name), '')::varchar as event_name,
    nullif(trim(entity_type), '')::varchar as entity_type,
    trim(entity_id)::varchar as entity_id,
    event_at_utc::timestamptz as event_at_utc,
    ingested_at_utc::timestamptz as ingested_at_utc

from read_csv('data/raw/events.csv', header = true, timestampformat = '%Y-%m-%d %H:%M:%S%z')