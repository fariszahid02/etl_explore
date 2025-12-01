# Common helper functions (e.g., get_latest_daily_donor)

import requests
from datetime import datetime, timedelta
from prefect import task, get_run_logger

@task
def get_latest_daily_donor(base_url, max_days=30):
    logger = get_run_logger()
    today = datetime.today()
    for i in range(max_days):
        date_to_try = today - timedelta(days=i)
        date_str = date_to_try.strftime("%Y-%m-%d")
        url = f"{base_url}/{date_str}.parquet"
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                logger.info(f"Found donor file for {date_str}")
                return url, date_str
        except Exception as e:
            logger.warning(f"Error checking {url}: {e}")
    return None, None