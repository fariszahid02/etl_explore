
# utils.py
import requests
from datetime import datetime, timedelta

def get_latest_daily_donor(base_url, max_days=30):
    today = datetime.today()
    for i in range(max_days):
        date_to_try = today - timedelta(days=i)
        date_str = date_to_try.strftime("%Y-%m-%d")
        url = f"{base_url}/{date_str}.parquet"
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                return url, date_str
        except:
            pass
    return None, None
