# Handles downloading and fetching data

import os
import requests
from config import FILES_INFO, COMPLETE_DONOR_PATH, FOLDER
from prefect import task, get_run_logger

@task
def download_file(url, path):
    logger = get_run_logger()
    r = requests.get(url, verify=False)
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)
    logger.info(f"Downloaded {url} → {path}")

@task
def extract_static_files():
    logger = get_run_logger()
    if not os.path.exists(COMPLETE_DONOR_PATH):
        logger.info("Downloading initial complete_donor...")
        download_file.fn(FILES_INFO['complete_donor'], COMPLETE_DONOR_PATH)
    else:
        logger.info("complete_donor already exists, will update incrementally")

    for name in ["daily_retention", "daily_donor_rates"]:
        path = os.path.join(FOLDER, f"{name}.parquet")
        if os.path.exists(path):
            os.remove(path)
        logger.info(f"Downloading {name}...")
        download_file.fn(FILES_INFO[name], path)