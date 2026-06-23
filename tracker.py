import os
import requests
from bs4 import BeautifulSoup

# Telegram Config
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Product Config
PRODUCT_NAME = "Prestige PIC 20 NEO"
TARGET_PRICE = 2200

URL = "https://dl.flipkart.com/dl/prestige-1600-w-induction-cooktop-push-button/p/itm15d69f3360370"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
}


def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def get_price():
    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=30
        )

        print("Status Code:", response.status_code)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        selectors = [
            "div.Nx9bqj",
            "div._30jeq3",
            "div.CEmiEU"
        ]

        for selector in selectors:

            tag = soup.select_one(selector)

            if tag:

                price_text = tag.get_text(strip=True)

                print("Price Text:", price_text)

                digits = "".join(
                    c for c in price_text
                    if c.isdigit()
                )

                if digits:
                    return int(digits)

        return None

    except Exception as e:
        print("ERROR:", e)
        return None


current_price = get_price()

print("Current Price =", current_price)

if current_price is None:

    send_telegram(
        "⚠️ Unable to fetch Flipkart price.\nCheck GitHub Action logs."
    )

elif current_price <= TARGET_PRICE:

    send_telegram(
        f"""🔥 PRICE ALERT

{PRODUCT_NAME}

Current Price: ₹{current_price}

Target Price: ₹{TARGET_PRICE}

Buy Now:
{URL}
"""
    )

else:

    print(
        f"Price {current_price} is above target {TARGET_PRICE}"
    )
