import os
import re
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://www.flipkart.com/prestige-1600-w-induction-cooktop-push-button/p/itm15d69f3360370"


def send_message(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    try:
        page.goto(
            URL,
            wait_until="commit",
            timeout=10000
        )
    except:
        pass

    page.wait_for_timeout(8000)

    html = page.content()

    browser.close()

prices = re.findall(r'₹\s?([0-9,]+)', html)

values = []

for p in prices:
    try:
        values.append(int(p.replace(",", "")))
    except:
        pass

send_message(
    f"ALL DETECTED PRICES:\n\n{values[:100]}"
)
