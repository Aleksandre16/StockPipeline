
import requests
from .utils import RateLimitError, ValidationError, NetworkError, UpstreamAPIError, write_json, ensure_dir
from datetime import date

def fetch_alpha_vantage_daily(symbol: str, api_key: str, user_agent: str) -> dict:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "datatype": "json",
        "apikey": api_key,
    }
    headers = {"User-Agent": user_agent}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
    except requests.exceptions.RequestException as e:
        raise NetworkError(str(e))
    if resp.status_code != 200:
        raise NetworkError(f"HTTP {resp.status_code}")
    data = resp.json()

    if "Note" in data:
        # limit / throttling
        raise RateLimitError(data["Note"])
    if "Error Message" in data:
        raise UpstreamAPIError(data["Error Message"])
    if "Time Series (Daily)" not in data:
        raise ValidationError("Missing 'Time Series (Daily)' key in response")
    return data

def save_raw_json(data: dict, lake_dir: str, symbol: str, run_date: date) -> str:
    ensure_dir(lake_dir)
    filename = f"{symbol}_{run_date.isoformat()}.json"
    path = os.path.join(lake_dir, filename)
    write_json(path, data)
    return path

import os  #  ბოლოს არის დაიმპორტირებული რომ პრობლემები არ შექმნას (overshadow) ზოგიერთ ედიტორზე
