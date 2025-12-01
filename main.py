# Orchestrates the ETL process

from extract import extract_static_files
from load import load_to_duckdb, save_complete_donor, load_other_tables, load_latest_daily_donor
from transform import incremental_update
from visualization import generate_donation_trend
from telegram import send_message, send_photo

import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def run_pipeline():
    # ETL
    extract_static_files()
    conn, latest_complete_date = load_to_duckdb()
    new_rows = incremental_update(conn, latest_complete_date)
    save_complete_donor(conn)
    print(f"✅ Updated complete_donor saved with {new_rows} new rows")
    load_other_tables(conn)
    load_latest_daily_donor(conn)

    # Visualization
    chart_path, insight_msg = generate_donation_trend(conn)

    # Notification
    send_message(insight_msg)
    send_photo(chart_path, caption="Daily Donation Trend (Last 7 Days)")

    print("✅ Pipeline completed successfully")
    conn.close()

if __name__ == "__main__":
    run_pipeline()
