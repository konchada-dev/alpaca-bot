# scripts/trade.py

import os
import requests
import json
import sys

ALPACA_KEY = os.getenv("APCA_API_KEY_ID")
ALPACA_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_BASE_URL")

def place_order(symbol, qty, side, limit_price=None):
    """Place a buy or sell order."""
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
        "Content-Type": "application/json"
    }
    
    if not limit_price:
        raise ValueError("limit_price is required — market orders are not allowed")

    order_data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,  # "buy" or "sell"
        "type": "limit",
        "time_in_force": "day",
        "limit_price": str(limit_price),
    }
    
    url = f"{BASE_URL}/orders"
    response = requests.post(url, headers=headers, json=order_data)
    return response.json()

def cancel_all_orders():
    """Cancel all open orders."""
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    url = f"{BASE_URL}/orders"
    response = requests.delete(url, headers=headers)
    return response.status_code

def get_market_status():
    """Check if the market is open."""
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
    }
    url = f"{BASE_URL}/clock"
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    action = sys.argv[1]
    
    if action == "status":
        print(json.dumps(get_market_status()))
    elif action == "order":
        symbol = sys.argv[2]
        qty = sys.argv[3]
        side = sys.argv[4]
        limit_price = sys.argv[5] if len(sys.argv) > 5 else None
        print(json.dumps(place_order(symbol, qty, side, limit_price)))
    elif action == "cancel":
        print(cancel_all_orders())