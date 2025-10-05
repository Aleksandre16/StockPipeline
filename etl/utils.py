
import json
import logging
import os
import shutil
from datetime import datetime, date, timezone
from zoneinfo import ZoneInfo

# -------- Exceptions --------
class RateLimitError(Exception): ...
class ValidationError(Exception): ...
class NetworkError(Exception): ...
class UpstreamAPIError(Exception): ...

# -------- Time helpers --------
def now_utc():
    return datetime.now(timezone.utc)

def today_in_tz(tz_name: str) -> datetime:
    tz = ZoneInfo(tz_name)
    return datetime.now(tz)

# -------- IO helpers --------
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def write_json(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def move_to_quarantine(raw_path: str, lake_dir: str):
    qdir = os.path.join(lake_dir, "_quarantine")
    ensure_dir(qdir)
    shutil.move(raw_path, os.path.join(qdir, os.path.basename(raw_path)))

# -------- Logging --------
def init_logger(level: str = "INFO") -> logging.Logger:
    lvl = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    return logging.getLogger("etl")
