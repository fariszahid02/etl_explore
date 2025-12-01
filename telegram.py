import os
import requests
from prefect import task, get_run_logger
from config import TELEGRAM_API_URL, CHAT_ID

@task
def send_message(text):
    logger = get_run_logger()
    if not TELEGRAM_API_URL or not CHAT_ID:
        logger.warning("⚠️ Telegram credentials missing. Message not sent.")
        return

    url = f"{TELEGRAM_API_URL}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=data, verify=False)
    logger.info(f"Telegram message response: {response.status_code} {response.text}")

@task
def send_photo(photo_path, caption=""):
    logger = get_run_logger()
    if not TELEGRAM_API_URL or not CHAT_ID:
        logger.warning("⚠️ Telegram credentials missing. Photo not sent.")
        return

    full_path = os.path.abspath(photo_path)
    if not os.path.exists(full_path):
        logger.warning(f"⚠️ Photo file not found: {full_path}")
        return

    url = f"{TELEGRAM_API_URL}/sendPhoto"
    with open(full_path, 'rb') as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID, "caption": caption}
        response = requests.post(url, data=data, files=files, verify=False)
        logger.info(f"Telegram photo response: {response.status_code} {response.text}")