import json
import os
from config import DATA_FILE

def load_all():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except Exception:
        return {"users": {}}

def _save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

_load = load_all

def get_user(user_id: int):
    data = _load()
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {"alerts": [], "portfolio": []}
        _save(data)
    return data["users"][uid]

def _save_user(user_id: int, user_data):
    data = _load()
    data["users"][str(user_id)] = user_data
    _save(data)

def add_alert(user_id: int, coin_id: str, coin_name: str, symbol: str, target: float):
    user = get_user(user_id)
    user["alerts"].append({
        "coin_id": coin_id,
        "coin_name": coin_name,
        "symbol": symbol,
        "target": target,
    })
    _save_user(user_id, user)

def remove_alert(user_id: int, index: int):
    user = get_user(user_id)
    if 0 <= index < len(user["alerts"]):
        removed = user["alerts"].pop(index)
        _save_user(user_id, user)
        return removed
    return None

def get_alerts(user_id: int):
    user = get_user(user_id)
    return user.get("alerts", [])

def add_holding(user_id: int, coin_id: str, coin_name: str, symbol: str, amount: float):
    user = get_user(user_id)
    user["portfolio"].append({
        "coin_id": coin_id,
        "coin_name": coin_name,
        "symbol": symbol,
        "amount": amount,
    })
    _save_user(user_id, user)

def remove_holding(user_id: int, index: int):
    user = get_user(user_id)
    if 0 <= index < len(user["portfolio"]):
        removed = user["portfolio"].pop(index)
        _save_user(user_id, user)
        return removed
    return None

def get_portfolio(user_id: int):
    user = get_user(user_id)
    return user.get("portfolio", [])
