# Send messages and images to Telegram

import requests
import warnings
from config import TELEGRAM_API_URL, CHAT_ID
from prefect import task, get_run_logger
import os

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

@task
def send_message(text):
    if not TELEGRAM_API_URL or not CHAT_ID:
        print("⚠️ Telegram credentials missing. Message not sent.")
        return

    url = f"{TELEGRAM_API_URL}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=data, verify=False)
    print("Telegram response:", response.status_code, response.text)

@task
def send_photo(photo_path, caption=""):
    if not TELEGRAM_API_URL or not CHAT_ID:
        print("⚠️ Telegram credentials missing. Photo not sent.")
        return

    full_path = os.path.abspath(photo_path)
    if not os.path.exists(full_path):
        print("⚠️ Photo file not found:", full_path)
        return

    url = f"{TELEGRAM_API_URL}/sendPhoto"
    with open(full_path, 'rb') as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID, "caption": caption}
        response = requests.post(url, data=data, files=files, verify=False)
        print("Telegram response:", response.status_code, response.text)
