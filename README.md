
# Blood Donation ETL Pipeline with Prefect Orchestration

## Overview
This project implements an **ETL (Extract, Transform, Load) pipeline** for analyzing blood donation data sourced from **KijangNet**. The pipeline processes multiple datasets related to blood donations, including:

- **Historical Donations** – A comprehensive dataset of past donations (initially up to *29-10-2025*).
- **Daily Donor Data** – Daily donation records for each date.
- **Donor Rates** – Daily updated donor rate metrics.
- **Retention Data** – Daily updated donor retention metrics.

All datasets are provided in **Parquet format** and accessed via secure KijangNet URLs.

---

## How It Works
### 1. **Extract**
- Downloads all four datasets from their respective URLs.
- The **historical file** is downloaded only once initially (up to *29-10-2025*).
- The **daily donor rates** and **retention files** are refreshed daily (existing files are deleted and replaced).
- The **daily donor file** is used for incremental updates to extend the historical dataset up to the current date.

> **Note:** Some dates may not have data available. The pipeline handles this gracefully by skipping missing dates and continuing until the latest available date.

### 2. **Transform**
- Merges incremental daily donor data into the historical dataset.
- WIP

### 3. **Load**
- Loads all datasets into a **DuckDB database** for efficient querying and analysis:
  - `complete_donor` (historical + incremental updates)
  - `daily_donor` (latest daily donor file)
  - `daily_donor_rates`
  - `daily_retention`

### 4. **Visualization & Insights**
- Generates a **weekly trend chart** of daily donations for the last 7 days.
- Provides short insights (e.g., detecting consecutive increases in donations).
- Sends the chart and insights to a **Telegram bot** for easy access.

### 5. **Orchestration with Prefect**
- The entire pipeline is orchestrated using **Prefect**.
- Deployed on **Prefect Cloud** and scheduled to run **daily at 9:00 AM Malaysia Time**.
- Automatically sends insights and visualizations to the Telegram bot.

---



## Future Enhancements
- Advanced data exploration (Transform) and analytics.
- Additional visualizations (e.g., blood group distribution, retention trends).
- Audience-specific dashboards and insights.
- Integration with BI tools or web dashboards.

---


## Current Limitations & Performance Notes (03/12/2025)
- **Prefect does not persist state between runs**:  
  When the pipeline runs on Prefect Cloud, it does not remember the last updated date for the historical dataset. As a result, each scheduled run reprocesses all incremental updates from the daily donor files, even if the historical file is already up-to-date. This increases runtime unnecessarily.

- **Local runs are optimized**:  
  When running locally, the pipeline checks the latest date in the historical file and only processes new data.

- **Impact on runtime**:  
  Currently, the average runtime is **1–2 minutes**, but this will increase as more dates accumulate unless state persistence or caching is implemented.

> **Planned improvement**: Implement Prefect task state persistence or external metadata storage (e.g., in DuckDB or a separate state file) to avoid redundant processing.



