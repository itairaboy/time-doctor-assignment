import os
import duckdb

PIPELINE_DB = os.getenv("PIPELINE_DB", "data/pipeline.duckdb")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5433")
PG_DB = os.getenv("PG_DB", "reporting")
PG_USER = os.getenv("PG_USER", "reporting_user")
PG_PASSWORD = os.getenv("PG_PASSWORD", "reporting_pass")

TABLES = [
    "mart_exec_scorecard_weekly",
    "mart_user_activity_weekly",
    "mart_task_productivity_weekly",
    "mart_user_retention_w4",
]

conn = duckdb.connect(PIPELINE_DB)
conn.execute("INSTALL postgres; LOAD postgres;")

pg_conn = f"host={PG_HOST} port={PG_PORT} dbname={PG_DB} user={PG_USER} password={PG_PASSWORD}"
conn.execute(f"ATTACH '{pg_conn}' AS pg (TYPE POSTGRES)")
conn.execute("CREATE SCHEMA IF NOT EXISTS pg.reporting")

for table in TABLES:
    conn.execute(f"CREATE OR REPLACE TABLE pg.reporting.{table} AS SELECT * FROM main.{table}")
    src = conn.sql(f"SELECT COUNT(*) FROM main.{table}").fetchone()[0]
    dst = conn.sql(f"SELECT COUNT(*) FROM pg.reporting.{table}").fetchone()[0]
    print(f"{table}: source={src}, target={dst}")
    
conn.close()
print("Published to Postgres")