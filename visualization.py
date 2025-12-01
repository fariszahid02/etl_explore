# Generate charts and insights

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from prefect import task, get_run_logger

@task
def generate_donation_trend(conn):
    logger = get_run_logger()
    query = """
    SELECT visit_date, COUNT(*) AS donation_count
    FROM complete_donor
    WHERE visit_date >= CURRENT_DATE - INTERVAL '7 day'
    GROUP BY visit_date
    ORDER BY visit_date
    """
    df = conn.execute(query).fetchdf()

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    all_dates = pd.date_range(start=start_date, end=end_date)

    if not df.empty:
        df['visit_date'] = pd.to_datetime(df['visit_date']).dt.date
    else:
        df = pd.DataFrame(columns=['visit_date', 'donation_count'])

    trend_df = pd.DataFrame({'visit_date': all_dates.date})
    trend_df = trend_df.merge(df, on='visit_date', how='left').fillna(0)

    insight_msg = "Insight: Donations trend is mixed or stable."
    if len(trend_df) >= 3:
        last_three = trend_df['donation_count'].iloc[-3:]
        if last_three.is_monotonic_increasing:
            insight_msg = "Donations have been rising for 3 days straight—keep the momentum going!"

    chart_path = 'daily_donation_trend.png'
    plt.figure(figsize=(10, 6))
    plt.plot(trend_df['visit_date'], trend_df['donation_count'], marker='o', color='blue')
    plt.title("Daily Donation Trend (Last 7 Days)", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Number of Donations")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    logger.info("Generated donation trend chart")
    return chart_path, insight_msg
