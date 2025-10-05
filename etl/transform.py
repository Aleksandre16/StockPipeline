
from typing import Dict, List
from datetime import datetime
import pandas as pd

def normalize_to_dataframe(symbol: str, ts_dict: Dict[str, dict]) -> pd.DataFrame:
    rows: List[dict] = []
    for day_str, d in ts_dict.items():
        rows.append({
            "symbol": symbol,
            "date": datetime.strptime(day_str, "%Y-%m-%d").date(),
            "open":  float(d["1. open"]),
            "high":  float(d["2. high"]),
            "low":   float(d["3. low"]),
            "close": float(d["4. close"]),
            "volume": int(d["5. volume"]),
        })
    df = pd.DataFrame(rows).sort_values("date")
    return df

def compute_daily_change(df: pd.DataFrame) -> pd.DataFrame:
    df["daily_change_percentage"] = ((df["close"] - df["open"]) / df["open"]) * 100.0
    return df

def enforce_strict_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"]).dt.date
    float_cols = ["open","high","low","close","daily_change_percentage"]
    df[float_cols] = df[float_cols].astype("float64")
    df["volume"] = df["volume"].astype("int64")
    return df

def dq_checks(df: pd.DataFrame):
    assert df["symbol"].notna().all()
    assert df["date"].notna().all()
    assert (df[["open","high","low","close"]] > 0).all().all()
    assert (df["volume"] >= 0).all()
    assert ((df["low"] <= df["open"]) & (df["open"] <= df["high"])).all()
    assert ((df["low"] <= df["close"]) & (df["close"] <= df["high"])).all()
