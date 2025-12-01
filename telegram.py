# Send messages and images to Telegram

import requests
import warnings
from config import TELEGRAM_API_URL, CHAT_ID
from prefect import task, get_run_logger

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

@task
def send_message(text):
    logger = get_run_logger()
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, data=payload, verify=False)
        logger.info(f"Telegram message response: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

@task
def send_photo(photo_path, caption=""):
    logger = get_run_logger()
    url = f"{TELEGRAM_API_URL}/sendPhoto"
    try:
        with open(photo_path, 'rb') as photo:
            files = {"photo": photo}
            data = {"chat_id": CHAT_ID, "caption": caption}
            response = requests.post(url, data=data, files=files, verify=False)
        logger.info(f"Telegram photo response: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"Failed to send photo: {e}")