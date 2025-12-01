# Stores URLs, folder paths, constants

import os
from dotenv import load_dotenv

load_dotenv()

# URLs
FILES_INFO = {
    "complete_donor": "https://data.kijang.net/dea/donations/historical.parquet",
    "daily_retention": "https://data.kijang.net/dea/retention/data.parquet",
    "daily_donor_rates": "https://data.kijang.net/dea/donorrate/data.parquet"
}
BASE_URL = "https://data.kijang.net/dea/donations"

# Folder for downloaded files
FOLDER = "downloaded_parquet"
os.makedirs(FOLDER, exist_ok=True)

# Paths
COMPLETE_DONOR_PATH = os.path.join(FOLDER, "complete_donor.parquet")
DAILY_DONOR_PATH = os.path.join(FOLDER, "daily_donor.parquet")

# Database
DB_PATH = os.getenv("DB_PATH", "donations.duckdb")

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
