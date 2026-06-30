import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
    print("Telegram status:", r.status_code)
    print("Telegram response:", r.text)
    r.raise_for_status()

send("✅ Bot Telegram đã kết nối thành công!")
Đã 
