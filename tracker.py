import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://dl.flipkart.com/dl/prestige-1600-w-induction-cooktop-push-button/p/itm15d69f3360370"

TARGET_PRICE = 2200

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def send_message(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

r = requests.get(URL, headers=HEADERS)

soup = BeautifulSoup(r.text, "html.parser")

price_tag = soup.find("div", {"class": "Nx9bqj"})

if price_tag:
    price_text = price_tag.text
    current_price = int(
        "".join(c for c in price_text if c.isdigit())
    )

    if current_price <= TARGET_PRICE:
        send_message(
            f"""🔥 PRICE ALERT

Prestige PIC 20 NEO

Current Price: ₹{current_price}

Target Price: ₹{TARGET_PRICE}

{URL}
"""
        )
