# Handles data cleaning, merging, incremental updates

import requests
from datetime import timedelta, datetime
from config import BASE_URL, DAILY_DONOR_PATH
from prefect import task, get_run_logger

@task
def incremental_update(conn, latest_complete_date):
    logger = get_run_logger()
    start_date = latest_complete_date + timedelta(days=1)
    today = datetime.today().date()
    new_rows_added = 0

    while start_date <= today:
        date_str = start_date.strftime("%Y-%m-%d")
        url = f"{BASE_URL}/{date_str}.parquet"
        try:
            r = requests.get(url, verify=False)
            if r.status_code == 200:
                with open(DAILY_DONOR_PATH, "wb") as f:
                    f.write(r.content)
                conn.execute(f"INSERT INTO complete_donor SELECT * FROM read_parquet('{DAILY_DONOR_PATH}')")
                count = conn.execute("SELECT COUNT(*) FROM read_parquet(?)", [DAILY_DONOR_PATH]).fetchone()[0]
                new_rows_added += count
                logger.info(f"Added {count} rows for {date_str}")
            else:
                logger.warning(f"No data for {date_str}")
        except Exception as e:
            logger.error(f"Error for {date_str}: {e}")
        start_date += timedelta(days=1)

    return new_rows_added
