import os
import re
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://www.flipkart.com/prestige-1600-w-induction-cooktop-push-button/p/itm15d69f3360370"

TARGET_PRICE = 2200


def send_message(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


def get_price():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

       page.goto(
    URL,
    wait_until="domcontentloaded",
    timeout=30000
)

page.wait_for_timeout(5000)

        text = page.content()

        browser.close()

        matches = re.findall(r'₹\s?([0-9,]+)', text)

        if matches:
            prices = [
                int(x.replace(",", ""))
                for x in matches
            ]

            return min(prices)

        return None


price = get_price()

print("Detected Price:", price)

if price is None:

    send_message(
        "⚠ Could not detect Flipkart price."
    )

elif price <= TARGET_PRICE:

    send_message(
        f"""🔥 PRICE ALERT

Prestige PIC 20 NEO

Current Price: ₹{price}

Target Price: ₹{TARGET_PRICE}

{URL}
"""
    )
