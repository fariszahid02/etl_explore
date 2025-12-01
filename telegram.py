# Send messages and images to Telegram

import requests
import warnings
from config import TELEGRAM_API_URL, CHAT_ID

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def send_message(text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload, verify=False)

def send_photo(photo_path, caption=""):
    url = f"{TELEGRAM_API_URL}/sendPhoto"
    with open(photo_path, 'rb') as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID, "caption": caption}
        requests.post(url, data=data, files=files, verify=False)
