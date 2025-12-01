# Handles loading data into DuckDB and saving back to Parquet

import duckdb
import os
from config import COMPLETE_DONOR_PATH, DB_PATH, FOLDER, BASE_URL
from utils import get_latest_daily_donor
import requests
from prefect import task, get_run_logger

@task
def load_to_duckdb():
    logger = get_run_logger()
    conn = duckdb.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS complete_donor")
    conn.execute(f"CREATE TABLE complete_donor AS SELECT * FROM read_parquet('{COMPLETE_DONOR_PATH}')")
    latest_complete_date = conn.execute("SELECT MAX(visit_date) FROM complete_donor").fetchone()[0]
    logger.info(f"Latest date in complete_donor: {latest_complete_date}")
    return conn, latest_complete_date

@task
def save_complete_donor(conn):
    conn.execute(f"COPY complete_donor TO '{COMPLETE_DONOR_PATH}' (FORMAT 'parquet')")

@task
def load_other_tables(conn):
    logger = get_run_logger()
    for name in ["daily_retention", "daily_donor_rates"]:
        path = os.path.join(FOLDER, f"{name}.parquet")
        conn.execute(f"DROP TABLE IF EXISTS {name}")
        conn.execute(f"CREATE TABLE {name} AS SELECT * FROM read_parquet('{path}')")
        count = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        logger.info(f"Loaded {name} with {count} rows")

@task
def load_latest_daily_donor(conn):
    logger = get_run_logger()
    latest_url, latest_date = get_latest_daily_donor.fn(BASE_URL)
    if latest_url:
        r = requests.get(latest_url, verify=False)
        r.raise_for_status()
        path = os.path.join(FOLDER, "daily_donor.parquet")
        with open(path, "wb") as f:
            f.write(r.content)
        conn.execute("DROP TABLE IF EXISTS daily_donor")
        conn.execute(f"CREATE TABLE daily_donor AS SELECT * FROM read_parquet('{path}')")
        count = conn.execute("SELECT COUNT(*) FROM daily_donor").fetchone()[0]
        logger.info(f"Loaded daily_donor ({latest_date}) with {count} rows")
    else:
        logger.warning("Could not find any daily donor file in last 30 days")
