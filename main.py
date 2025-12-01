from prefect import flow, get_run_logger
from extract import extract_static_files
from load import load_to_duckdb, save_complete_donor, load_other_tables, load_latest_daily_donor
from transform import incremental_update
from visualization import generate_donation_trend
from telegram import send_message, send_photo
import os

@flow(name="donation-etl-pipeline")
def run_pipeline():
    logger = get_run_logger()
    logger.info("🚀 Starting ETL pipeline")
    logger.info(f"TELEGRAM_TOKEN loaded: {bool(os.getenv('TELEGRAM_TOKEN'))}")
    logger.info(f"CHAT_ID loaded: {bool(os.getenv('CHAT_ID'))}")

    # Extract
    extract_static_files()

    # Load (call underlying function directly to avoid caching conn)
    conn, latest_complete_date = load_to_duckdb.fn()

    # Transform
    new_rows = incremental_update.fn(conn, latest_complete_date)
    save_complete_donor.fn(conn)
    logger.info(f"Updated complete_donor with {new_rows} new rows")

    # Load other tables
    load_other_tables.fn(conn)
    load_latest_daily_donor.fn(conn)

    # Visualization
    chart_path, insight_msg = generate_donation_trend.fn(conn)

    # Notifications
    send_message(insight_msg)
    send_photo(chart_path, caption="Daily Donation Trend (Last 7 Days)")

    conn.close()
    logger.info("✅ Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()