# Data Directory

This directory contains the Fitbit health tracker CSV datasets.

## Files

- `activity.csv` - Daily activity data (steps, calories, active minutes)
- `sleep.csv` - Sleep tracking data (duration, efficiency, sleep stages)
- `heart_rate.csv` - Heart rate metrics (resting, average, max, min HR)

## Generating Full Dataset

To generate complete sample datasets with 33 users × 30 days (990 records each), run:

```bash
python generate_sample_data.py
```

This will populate the CSV files with realistic sample data for analysis.

## Sample Data Structure

The current files contain sample rows to demonstrate the data structure. The full dataset will contain:
- **33 unique users** (user_01 through user_33)
- **30 days** of data (2024-01-01 through 2024-01-30)
- **990 total records** per dataset

