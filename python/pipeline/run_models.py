import duckdb
from pathlib import Path

DB_PATH = "data/pipeline.duckdb"

layers = [
    ("models/staging", "stg_*.sql", "view"),
    ("models/intermediate", "int_*.sql", "view"),
    ("models/marts", "mart_*.sql", "table"),
]
 
# Execution order matters in intermediate layer
intermediate_order = [
    "int_users_enriched",
    "int_tasks_enriched",
    "int_events_enriched",
    "int_user_week_activity",
    "int_user_retention_w4",
]

def ordered_paths(folder: str, pattern: str):
    paths = list(Path(folder).glob(pattern))
    if folder != "models/intermediate":
        return sorted(paths)
    by_name = {p.stem: p for p in paths}
    ordered = [by_name[name] for name in intermediate_order if name in by_name]
    remaining = sorted([p for p in paths if p.stem not in intermediate_order])
    return ordered + remaining

conn = duckdb.connect(DB_PATH)
try:
    for folder, pattern, mat in layers:
        for path in ordered_paths(folder, pattern):
            name = path.stem
            sql = path.read_text().strip().rstrip(";")
            try:
                conn.execute(f'create or replace {mat} {name} as {sql}')
                print(f"created {mat}: {name}")
            except Exception as exc:
                raise RuntimeError(f"failed building {mat} {name} from {path}") from exc
finally:
    conn.close()