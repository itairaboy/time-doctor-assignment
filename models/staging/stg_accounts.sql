select
    trim(account_id)::varchar as account_id,
    nullif(trim(account_name), '')::varchar as account_name,
    nullif(trim(plan_tier), '')::varchar as plan_tier,
    nullif(trim(region), '')::varchar as region,
    seats_purchased::integer as seats_purchased,
    nullif(trim(account_status), '')::varchar as account_status,
    created_at_utc::timestamptz as created_at_utc

from read_csv('data/raw/accounts.csv', header = true, timestampformat = '%Y-%m-%d %H:%M:%S%z')