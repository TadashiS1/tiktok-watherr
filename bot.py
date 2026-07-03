import time
import requests
from bs4 import BeautifulSoup

# ====== НАСТРОЙКИ (ЗАПОЛНИ) ======
BOT_TOKEN = "8933884537:AAGDNc0gddMN_IfkpiYKR7su7rrgTnJf7qI"
CHAT_ID = "7045661693"
TIKTOK_USER = "marriissha1"

last_seen = None


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def get_latest_post():
    url = f"https://www.tiktok.com/@{TIKTOK_USER}"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")

    videos = soup.find_all("a")

    links = []
    for v in videos:
        href = v.get("href")
        if href and "/video/" in href:
            links.append(href)

    return links[0] if links else None


send_message("✅ TikTok watcher запущен")

while True:
    try:
        latest = get_latest_post()

        if latest and latest != last_seen:
            last_seen = latest
            send_message(f"🔔 Новый пост/репост: https://www.tiktok.com{latest}")

    except Exception as e:
        print("Ошибка:", e)

    time.sleep(60)
