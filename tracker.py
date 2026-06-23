import json
import os
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

TARGET_PRICE = 2200

def send_message(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

# Temporary test price
current_price = 1999

if current_price <= TARGET_PRICE:
    send_message(
        f"""🔥 PRICE ALERT

Prestige PIC 20 NEO

Current Price: ₹{current_price}

Target Price: ₹{TARGET_PRICE}

Buy Now:
https://dl.flipkart.com/dl/prestige-1600-w-induction-cooktop-push-button/p/itm15d69f3360370
"""
    )
