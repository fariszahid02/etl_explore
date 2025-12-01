# Handles downloading and fetching data

import os
import requests
from config import FILES_INFO, COMPLETE_DONOR_PATH, FOLDER

def download_file(url, path):
    r = requests.get(url, verify=False)
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)

def extract_static_files():
    if not os.path.exists(COMPLETE_DONOR_PATH):
        print(f"Downloading initial complete_donor from {FILES_INFO['complete_donor']}...")
        download_file(FILES_INFO['complete_donor'], COMPLETE_DONOR_PATH)
        print("✅ Initial complete_donor downloaded")
    else:
        print("✅ complete_donor already exists, will update incrementally")

    for name in ["daily_retention", "daily_donor_rates"]:
        path = os.path.join(FOLDER, f"{name}.parquet")
        if os.path.exists(path):
            os.remove(path)
        print(f"Downloading {name}...")
        download_file(FILES_INFO[name], path)
        print(f"✅ {name} downloaded")
