# BONUS
import time
import schedule
from etl.pipeline import run_pipeline

# run_pipeline()

schedule.every().day.at("22:00").do(run_pipeline)

print("Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)