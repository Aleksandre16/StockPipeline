# StockPipeline — Alpha Vantage ETL (AAPL, GOOG, MSFT)

A complete ETL pipeline that extracts daily stock prices from [Alpha Vantage](https://www.alphavantage.co), transforms them with `pandas`, validates using `Pydantic`, and loads into a local SQLite database with upserts and de-duplication.

**Author:** [aleksandre16](https://github.com/aleksandre16)  

---

## Prerequisites

- Python 3.10 or higher
- PyCharm or any IDE of your choice
- A free Alpha Vantage API key — [register here](https://www.alphavantage.co/support/#api-key)

---

## Quickstart

```bash
# Clone or unzip the project
cd StockPipeline

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Open .env and paste your Alpha Vantage API key

# Run the ETL pipeline
python etl/pipeline.py
```

---

## Pipeline Behavior

1. Fetches daily stock data for AAPL, GOOG, and MSFT from the Alpha Vantage API.
2. Saves raw JSON responses to `raw_data/SYMBOL_YYYY-MM-DD.json`.
3. Transforms the raw data into a `pandas` DataFrame with the following columns: `date`, `open`, `high`, `low`, `close`, `volume`, `daily_change_percentage`.
4. Loads the transformed data into `stock.db` (created automatically if absent).
5. Prevents duplicate records using a unique index and upsert logic:

```sql
CREATE UNIQUE INDEX ux_symbol_date ON stock_daily_data(symbol, date);
ON CONFLICT(symbol, date) DO UPDATE;
```

6. Attaches an `extraction_timestamp` to each record for audit tracking.

---

## Scheduling (Optional)

The pipeline can be automated to run on a daily schedule using either the bundled scheduler or a system cron job.

### Option A — Python Scheduler

```bash
python etl/schedule_run.py
```

Runs every day at 18:00 local time by default. The schedule is configurable inside the file.

### Option B — Cron Job

The following example runs the pipeline daily at 23:00 Tbilisi time:

```
0 23 * * * /usr/bin/python3 /path/to/StockPipeline/etl/pipeline.py >> /path/to/StockPipeline/logs/cron.log 2>&1
```

If you encounter a "no such file or directory" error, create the `logs/` directory first:

```bash
mkdir -p /path/to/StockPipeline/logs
```

---

## Environment Variables

Create a `.env` file in the project root using the following template:

```env
ALPHAVANTAGE_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///stock.db
DATA_LAKE_DIR=raw_data
SYMBOLS=AAPL,GOOG,MSFT
USER_AGENT=StockPipeline/1.0
SLEEP_BETWEEN_CALLS_SECONDS=15
TZ=Asia/Tbilisi
```

---

## Database Schema

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| symbol | TEXT | Stock ticker symbol |
| date | TEXT | Trading date |
| open_price | REAL | Opening price |
| high_price | REAL | Highest price |
| low_price | REAL | Lowest price |
| close_price | REAL | Closing price |
| volume | INTEGER | Trading volume |
| daily_change_percentage | REAL | `((close - open) / open) * 100` |
| extraction_timestamp | TEXT | UTC timestamp of data extraction |

---

## Dependencies

```
pandas
requests
pydantic
python-dotenv
schedule
```

---

## Summary

- Fully functional ETL pipeline (Extract, Transform, Load)
- Schema validation with Pydantic
- Raw JSON archiving alongside structured database records
- Idempotent upserts with no duplicate records
- Optional daily scheduling via `schedule` library or cron

---

**License:** MIT  
**Purpose:** Educational — Data Engineering ETL design example, Sweeft (TASK)
