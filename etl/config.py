
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    API_KEY: str
    DATABASE_URL: str
    DATA_LAKE_DIR: str
    SYMBOLS: list[str]
    USER_AGENT: str
    SLEEP_BETWEEN_CALLS_SECONDS: int
    TZ: str

def get_config() -> "Config":
    api_key = os.getenv("ALPHAVANTAGE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("ALPHAVANTAGE_API_KEY is not set. Create a .env file and set it.")
    db_url = os.getenv("DATABASE_URL", "sqlite:///stock.db")
    lake = os.getenv("DATA_LAKE_DIR", "raw_data")
    symbols = [s.strip().upper() for s in os.getenv("SYMBOLS", "AAPL,GOOG,MSFT").split(",") if s.strip()]
    user_agent = os.getenv("USER_AGENT", "Batch9-ETL/1.0 (learning project)")
    sleep_secs = int(os.getenv("SLEEP_BETWEEN_CALLS_SECONDS", "15"))
    tz = os.getenv("TZ", "Asia/Tbilisi")
    return Config(
        API_KEY=api_key,
        DATABASE_URL=db_url,
        DATA_LAKE_DIR=lake,
        SYMBOLS=symbols,
        USER_AGENT=user_agent,
        SLEEP_BETWEEN_CALLS_SECONDS=sleep_secs,
        TZ=tz,
    )
