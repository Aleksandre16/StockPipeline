
from .config import get_config
from .utils import init_logger, now_utc, today_in_tz, move_to_quarantine
from .extract import fetch_alpha_vantage_daily, save_raw_json
from .validate import validate_envelope, unwrap_time_series, validate_timeseries
from .transform import normalize_to_dataframe, compute_daily_change, enforce_strict_dtypes, dq_checks
from .load import get_connection, ensure_table_exists, get_max_loaded_date, upsert_stock_daily
import time

def run_pipeline():
    cfg = get_config()
    logger = init_logger()
    conn = get_connection(cfg.DATABASE_URL)
    ensure_table_exists(conn)

    run_date = today_in_tz(cfg.TZ).date()

    for symbol in cfg.SYMBOLS:
        extraction_ts = now_utc()
        logger.info(f"Start {symbol}")
        raw_path = None
        try:
            # EXTRACT
            payload = fetch_alpha_vantage_daily(symbol, cfg.API_KEY, cfg.USER_AGENT)
            raw_path = save_raw_json(payload, cfg.DATA_LAKE_DIR, symbol, run_date)

            # VALIDATE
            validate_envelope(payload)
            ts = unwrap_time_series(payload)
            validate_timeseries(ts)

            # TRANSFORM
            df = normalize_to_dataframe(symbol, ts)
            df = compute_daily_change(df)
            df = enforce_strict_dtypes(df)
            dq_checks(df)

            # incrementality
            max_loaded = get_max_loaded_date(conn, symbol)
            if max_loaded is not None:
                df = df[df["date"].astype(str) > str(max_loaded)]
            if df.empty:
                logger.info(f"No new rows for {symbol}")
                continue

            # LOAD
            upsert_stock_daily(conn, df, extraction_ts)

            logger.info(f"Done {symbol} | rows={len(df)} | raw='{raw_path}'")
            time.sleep(cfg.SLEEP_BETWEEN_CALLS_SECONDS)

        except Exception as e:
            logger.exception(f"Error for {symbol}: {e}")
            if raw_path:
                try:
                    move_to_quarantine(raw_path, cfg.DATA_LAKE_DIR)
                except Exception as _:
                    pass
            continue

if __name__ == "__main__":
    run_pipeline()
