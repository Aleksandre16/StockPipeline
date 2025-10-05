
from datetime import datetime
from pydantic import BaseModel, validator
from typing import Dict

class DailyPoint(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: int

    @validator("open", "high", "low", "close")
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError("price must be > 0")
        return v

    @validator("volume")
    def volume_nonneg(cls, v):
        if v < 0:
            raise ValueError("volume must be >= 0")
        return v

def validate_envelope(json_obj: dict):
    if "Meta Data" not in json_obj or "Time Series (Daily)" not in json_obj:
        raise ValueError("Invalid envelope: missing 'Meta Data' or 'Time Series (Daily)'")

def unwrap_time_series(json_obj: dict) -> Dict[str, dict]:
    return json_obj["Time Series (Daily)"]

def validate_timeseries(ts_dict: Dict[str, dict]):
    required = ["1. open","2. high","3. low","4. close","5. volume"]
    for day_str, rec in ts_dict.items():
        #  format
        try:
            datetime.strptime(day_str, "%Y-%m-%d")
        except Exception as e:
            raise ValueError(f"Bad date key: {day_str}") from e

        for k in required:
            if k not in rec:
                raise ValueError(f"Missing key {k} in record for {day_str}")

        dp = DailyPoint(
            open=float(rec["1. open"]),
            high=float(rec["2. high"]),
            low=float(rec["3. low"]),
            close=float(rec["4. close"]),
            volume=int(rec["5. volume"]),
        )
        _ = dp
