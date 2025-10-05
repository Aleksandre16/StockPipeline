
import sqlite3
from typing import Optional
from datetime import datetime, date

def _path_from_db_url(db_url: str) -> str:
    #   sqlite:///path/to.db
    if not db_url.startswith("sqlite:///"):
        raise ValueError("Only sqlite:/// URLs are supported in this starter.")
    return db_url.replace("sqlite:///", "", 1)

def get_connection(db_url: str) -> sqlite3.Connection:
    path = _path_from_db_url(db_url)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def ensure_table_exists(conn: sqlite3.Connection):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS stock_daily_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        date TEXT NOT NULL,
        open_price REAL,
        high_price REAL,
        low_price REAL,
        close_price REAL,
        volume INTEGER,
        daily_change_percentage REAL,
        extraction_timestamp TEXT NOT NULL
    );
    """)
    conn.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS ux_symbol_date
    ON stock_daily_data(symbol, date);
    """)
    conn.commit()

def get_max_loaded_date(conn: sqlite3.Connection, symbol: str) -> Optional[str]:
    cur = conn.execute("SELECT MAX(date) FROM stock_daily_data WHERE symbol = ?", (symbol,))
    row = cur.fetchone()
    return row[0] if row and row[0] is not None else None

def upsert_stock_daily(conn: sqlite3.Connection, df, extraction_ts: datetime):
    sql = """
    INSERT INTO stock_daily_data
      (symbol, date, open_price, high_price, low_price, close_price, volume,
       daily_change_percentage, extraction_timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(symbol, date) DO UPDATE SET
      open_price=excluded.open_price,
      high_price=excluded.high_price,
      low_price=excluded.low_price,
      close_price=excluded.close_price,
      volume=excluded.volume,
      daily_change_percentage=excluded.daily_change_percentage,
      extraction_timestamp=excluded.extraction_timestamp;
    """
    rows = [
        (
            str(r.symbol),
            r.date.isoformat() if hasattr(r.date, "isoformat") else str(r.date),
            float(r.open),
            float(r.high),
            float(r.low),
            float(r.close),
            int(r.volume),
            float(r.daily_change_percentage),
            extraction_ts.isoformat(),
        )
        for r in df.itertuples(index=False)
    ]
    conn.executemany(sql, rows)
    conn.commit()
