import os
import json
import hashlib
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
STATE_FILE = "state.json"

URLS = [
    "https://aeonretail.com/Form/Product/ProductList.aspx?gspsk=%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3",
    "https://aeonretail.com/Form/Product/ProductList.aspx?gspsk=%E3%83%9D%E3%82%B1%E3%82%AB",
    "https://aeonretail.com/Form/Product/ProductList.aspx?gspsk=%E3%83%AF%E3%83%B3%E3%83%94%E3%83%BC%E3%82%B9",
    "https://aeonretail.com/Form/Product/ProductList.aspx?gspsk=ONE%20PIECE",
    "https://aeonretail.com/Form/Product/ProductList.aspx?gspsk=%E3%82%AB%E3%83%BC%E3%83%89%E3%82%B2%E3%83%BC%E3%83%A0",
    "https://aeonretail.com/Form/Product/ProductList.aspx?gspsk=%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%88%E3%83%87%E3%83%83%E3%82%AD",
]

KEYWORDS = [
    "ポケモン",
    "ポケカ",
    "ポケモンカード",
    "ワンピース",
    "ワンピカード",
    "ONE PIECE",
    "カードゲーム",
    "スタートデッキ",
    "デッキ",
    "ブースターパック",
    "BOX",
    "予約",
    "抽選",
    "再販",
    "販売",
    "販売開始",
    "販売予定",
    "購入",
    "入荷",
    "入荷予定",
    "発売日",
    "新商品",
    "新発売",
    "商品一覧",
    "商品情報",
]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
    print("Telegram:", r.status_code, r.text)
    r.raise_for_status()

def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def check_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    matched = [kw for kw in KEYWORDS if kw in text]
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return matched, digest

def main():
    state = load_state()
    changed = False

    for url in URLS:
        try:
            matched, digest = check_page(url)
            old_digest = state.get(url)

            if old_digest is None:
                state[url] = digest
                changed = True
                print("First check:", url)
                continue

            if digest != old_digest and matched:
                send(
                    "🚨 AEON Retail có cập nhật mới!\n\n"
                    f"🔎 Từ khóa phát hiện: {', '.join(matched)}\n\n"
                    f"🔗 Link:\n{url}"
                )
                state[url] = digest
                changed = True
            else:
                print("No change:", url)

        except Exception as e:
            send(f"⚠️ Bot lỗi khi kiểm tra AEON:\n{url}\n\n{e}")

    if changed:
        save_state(state)

if _name_ == "__main__":
    main()
