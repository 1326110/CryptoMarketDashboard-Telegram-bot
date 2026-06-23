import httpx
from config import API_TIMEOUT

BASE_URL = "https://api.coingecko.com/api/v3"

client = httpx.Client(timeout=API_TIMEOUT)

def get_price(coin_id: str):
    try:
        resp = client.get(
            f"{BASE_URL}/simple/price",
            params={
                "ids": coin_id.lower(),
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_market_cap": "true",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        if coin_id.lower() not in data:
            return None
        return data[coin_id.lower()]
    except Exception:
        return None

def get_coin_info(coin_id: str):
    try:
        resp = client.get(f"{BASE_URL}/coins/{coin_id.lower()}")
        resp.raise_for_status()
        data = resp.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "symbol": data["symbol"],
            "image": data["image"].get("small", ""),
            "market_cap_rank": data.get("market_cap_rank"),
        }
    except Exception:
        return None

def search_coins(query: str):
    try:
        resp = client.get(
            f"{BASE_URL}/search", params={"query": query}
        )
        resp.raise_for_status()
        data = resp.json()
        coins = data.get("coins", [])
        if coins:
            c = coins[0]
            return {"id": c["id"], "name": c["name"], "symbol": c["symbol"]}
        return None
    except Exception:
        return None

def get_top_coins(limit: int = 10):
    try:
        resp = client.get(
            f"{BASE_URL}/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": limit,
                "page": 1,
                "sparkline": "false",
            },
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

def get_price_with_detail(coin_id: str):
    try:
        resp = client.get(
            f"{BASE_URL}/coins/markets",
            params={
                "vs_currency": "usd",
                "ids": coin_id.lower(),
                "order": "market_cap_desc",
                "per_page": 1,
                "page": 1,
                "sparkline": "false",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        if data:
            return data[0]
        return None
    except Exception:
        return None
