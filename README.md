# 🧠 StockPipeline — Alpha Vantage ETL (AAPL, GOOG, MSFT)

A complete ETL pipeline that **extracts daily stock prices** from [Alpha Vantage](https://www.alphavantage.co), **transforms** them with `pandas`, **validates** using `Pydantic`, and **loads** into a local **SQLite** database with upserts and de-duplication.

Author: [@aleksandre16](https://github.com/aleksandre16)  
Project: Batch 9 Data Engineering Intern Assignment  
Location: Tbilisi, Georgia  

---

## 1) 🧩 Prerequisites
- Python 3.10+
- PyCharm or any IDE
- Free Alpha Vantage API key → [Get one here](https://www.alphavantage.co/support/#api-key)

---

## 2) ⚙️ Quickstart

```bash
# clone or unzip project
cd StockPipeline

# create virtual environment
python -m venv .venv

# activate it
source .venv/bin/activate        # macOS / Linux
# or
.venv\Scripts\activate           # Windows

# install dependencies
pip install -r requirements.txt

# copy environment file
cp .env.example .env
# edit .env and paste your Alpha Vantage key

# run the ETL pipeline
python etl/pipeline.py
```

---

## 3) 📊 What Happens
- Fetches **daily stock data** for AAPL, GOOG, and MSFT.
- Saves raw JSON in:  
  ```
  raw_data/SYMBOL_YYYY-MM-DD.json
  ```
- Transforms into a `pandas` DataFrame with columns:
  ```
  date, open, high, low, close, volume, daily_change_percentage
  ```
- Loads data into the SQLite database `stock.db` (created automatically).
- Avoids duplicates via:
  ```sql
  CREATE UNIQUE INDEX ux_symbol_date ON stock_daily_data(symbol, date);
  ON CONFLICT(symbol, date) DO UPDATE;
  ```
- Adds an `extraction_timestamp` for audit tracking.

---

## 4) ⏰ Scheduling (Optional)

You can automate daily runs using **Python’s `schedule` library** or **cron**.

### Option A — Python Scheduler
```bash
python etl/schedule_run.py
```
*(runs every day at 18:00 local time — configurable inside the file)*

### Option B — Cron Job (example for 23:00 Tbilisi time)
```
0 23 * * * /usr/bin/python3 /Users/yourname/Desktop/Projects/StockPipeline/etl/pipeline.py >> /Users/yourname/Desktop/Projects/StockPipeline/logs/cron.log 2>&1
```
> 💡 If you see “no such file or directory” — create the `logs/` folder first:
> ```bash
> mkdir -p /Users/yourname/Desktop/Projects/StockPipeline/logs
> ```

---

## 5) 🌍 Environment Variables
Create a `.env` file in the project root using the template below:

```
ALPHAVANTAGE_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///stock.db
DATA_LAKE_DIR=raw_data
SYMBOLS=AAPL,GOOG,MSFT
USER_AGENT=StockPipeline/1.0
SLEEP_BETWEEN_CALLS_SECONDS=15
TZ=Asia/Tbilisi
```

---

## 6) 🗄 Database Schema
| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER | Primary key |
| symbol | TEXT | Stock symbol |
| date | TEXT | Trading date |
| open_price | REAL | Opening price |
| high_price | REAL | Highest price |
| low_price | REAL | Lowest price |
| close_price | REAL | Closing price |
| volume | INTEGER | Trading volume |
| daily_change_percentage | REAL | ((close - open) / open) * 100 |
| extraction_timestamp | TEXT | Time of data extraction |

---

## 7) 📦 Requirements
```
pandas
requests
pydantic
python-dotenv
schedule
```

---

## 8) 🧠 Summary
✔️ Fully functional ETL pipeline (Extract → Transform → Load)  
✔️ Validates with Pydantic  
✔️ Stores raw JSON and transformed data  
✔️ Idempotent upserts (no duplicates)  
✔️ Optional daily scheduling via `schedule` or `cron`  

---

**Author:** [aleksandre16](https://github.com/aleksandre16)  
**License:** MIT  
**Purpose:** Educational — Data Engineering ETL design example, Sweeft (TASK)
