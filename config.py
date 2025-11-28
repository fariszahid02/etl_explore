# config.py
import os

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
DB_PATH = "donations.duckdb"

# # Telegram
# TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# CHAT_ID = "YOUR_CHAT_ID"
