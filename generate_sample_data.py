"""
Script to generate sample Fitbit data for 33 users over 30 days.
Run this script to populate the data/ directory with sample CSV files.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate date range (30 days)
start_date = datetime(2024, 1, 1)
dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

# Generate user IDs (33 users)
users = [f'user_{i:02d}' for i in range(1, 34)]

# 1. Activity Data
print("Generating activity.csv...")
activity_data = []
for user in users:
    # Different activity patterns per user
    base_steps = np.random.uniform(5000, 12000)
    base_calories = np.random.uniform(1800, 2600)
    
    for date in dates:
        activity_data.append({
            'user_id': user,
            'date': date,
            'steps': max(0, int(np.random.normal(base_steps, base_steps * 0.3))),
            'calories_burned': max(0, int(np.random.normal(base_calories, base_calories * 0.2))),
            'sedentary_minutes': max(0, int(np.random.normal(600, 120))),
            'lightly_active_minutes': max(0, int(np.random.normal(200, 50))),
            'moderately_active_minutes': max(0, int(np.random.normal(30, 15))),
            'very_active_minutes': max(0, int(np.random.normal(20, 10)))
        })

activity_df = pd.DataFrame(activity_data)
activity_df.to_csv('data/activity.csv', index=False)
print(f"Created activity.csv with {len(activity_df)} rows")

# 2. Sleep Data
print("Generating sleep.csv...")
sleep_data = []
for user in users:
    base_sleep_hours = np.random.uniform(6, 9)
    
    for date in dates:
        # Sleep duration in minutes
        sleep_duration = max(300, int(np.random.normal(base_sleep_hours * 60, 60)))
        time_in_bed = sleep_duration + np.random.randint(10, 60)
        
        sleep_data.append({
            'user_id': user,
            'date': date,
            'time_in_bed_minutes': time_in_bed,
            'sleep_duration_minutes': sleep_duration,
            'sleep_efficiency': round(np.random.uniform(0.75, 0.95), 3),
            'deep_sleep_minutes': max(0, int(np.random.normal(90, 30))),
            'rem_sleep_minutes': max(0, int(np.random.normal(120, 40))),
            'light_sleep_minutes': sleep_duration - (int(np.random.normal(90, 30)) + int(np.random.normal(120, 40)))
        })

sleep_df = pd.DataFrame(sleep_data)
sleep_df['light_sleep_minutes'] = sleep_df['light_sleep_minutes'].clip(lower=0)
sleep_df.to_csv('data/sleep.csv', index=False)
print(f"Created sleep.csv with {len(sleep_df)} rows")

# 3. Heart Rate Data
print("Generating heart_rate.csv...")
heart_rate_data = []
for user in users:
    base_resting_hr = np.random.uniform(55, 75)
    
    for date in dates:
        heart_rate_data.append({
            'user_id': user,
            'date': date,
            'avg_resting_hr': max(40, int(np.random.normal(base_resting_hr, 5))),
            'avg_hr': max(50, int(np.random.normal(base_resting_hr + 10, 8))),
            'max_hr': max(70, int(np.random.normal(base_resting_hr + 40, 15))),
            'min_hr': max(40, int(np.random.normal(base_resting_hr - 5, 5))),
            'calories_burned_hr': max(0, int(np.random.normal(2200, 400)))
        })

hr_df = pd.DataFrame(heart_rate_data)
hr_df.to_csv('data/heart_rate.csv', index=False)
print(f"Created heart_rate.csv with {len(hr_df)} rows")

print("\n✅ All sample data files generated successfully!")
print(f"Total records: {len(activity_df)} activity, {len(sleep_df)} sleep, {len(hr_df)} heart rate")

