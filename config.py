# Stores URLs, folder paths, constants

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

# Telegram
TELEGRAM_TOKEN = "8529466463:AAF1hXVxKM__Si3a5nEduYro7oiPOedA7Sc"
CHAT_ID = "7952404275"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"