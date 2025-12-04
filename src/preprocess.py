"""
Data Preprocessing Module

This module handles loading, cleaning, and merging Fitbit datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_datasets(data_dir='data'):
    """
    Load all Fitbit datasets from CSV files.
    
    Args:
        data_dir (str): Directory containing CSV files
        
    Returns:
        tuple: (activity_df, sleep_df, heart_rate_df)
    """
    data_path = Path(data_dir)
    
    # Load datasets
    activity_df = pd.read_csv(data_path / 'activity.csv')
    sleep_df = pd.read_csv(data_path / 'sleep.csv')
    heart_rate_df = pd.read_csv(data_path / 'heart_rate.csv')
    
    print(f"Loaded {len(activity_df)} activity records")
    print(f"Loaded {len(sleep_df)} sleep records")
    print(f"Loaded {len(heart_rate_df)} heart rate records")
    
    return activity_df, sleep_df, heart_rate_df


def clean_data(df, dataset_name=''):
    """
    Clean dataset by handling nulls, duplicates, and invalid values.
    
    Args:
        df (pd.DataFrame): Input dataframe
        dataset_name (str): Name of dataset for logging
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    initial_rows = len(df)
    
    # Remove duplicates
    df = df.drop_duplicates()
    print(f"{dataset_name}: Removed {initial_rows - len(df)} duplicate rows")
    
    # Handle null values
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print(f"{dataset_name}: Null values found:")
        print(null_counts[null_counts > 0])
        # Fill numeric columns with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    return df


def aggregate_daily_metrics(df, group_cols, agg_dict):
    """
    Aggregate data to daily metrics.
    
    Args:
        df (pd.DataFrame): Input dataframe
        group_cols (list): Columns to group by
        agg_dict (dict): Aggregation dictionary
        
    Returns:
        pd.DataFrame: Aggregated dataframe
    """
    aggregated = df.groupby(group_cols).agg(agg_dict).reset_index()
    return aggregated


def merge_datasets(activity_df, sleep_df, heart_rate_df):
    """
    Merge all datasets on user_id and date.
    
    Args:
        activity_df (pd.DataFrame): Activity data
        sleep_df (pd.DataFrame): Sleep data
        heart_rate_df (pd.DataFrame): Heart rate data
        
    Returns:
        pd.DataFrame: Merged dataframe
    """
    # Clean each dataset
    activity_df = clean_data(activity_df, 'Activity')
    sleep_df = clean_data(sleep_df, 'Sleep')
    heart_rate_df = clean_data(heart_rate_df, 'Heart Rate')
    
    # Ensure date columns are datetime
    for df in [activity_df, sleep_df, heart_rate_df]:
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
    
    # Merge step by step
    merged_df = activity_df.merge(
        sleep_df,
        on=['user_id', 'date'],
        how='outer'
    )
    
    merged_df = merged_df.merge(
        heart_rate_df,
        on=['user_id', 'date'],
        how='outer'
    )
    
    # Fill missing values after merge
    numeric_cols = merged_df.select_dtypes(include=[np.number]).columns
    merged_df[numeric_cols] = merged_df[numeric_cols].fillna(
        merged_df[numeric_cols].median()
    )
    
    print(f"Merged dataset: {len(merged_df)} records")
    print(f"Merged dataset columns: {list(merged_df.columns)}")
    
    return merged_df


def preprocess_pipeline(data_dir='data', output_path=None):
    """
    Complete preprocessing pipeline.
    
    Args:
        data_dir (str): Directory containing CSV files
        output_path (str, optional): Path to save merged dataset
        
    Returns:
        pd.DataFrame: Preprocessed and merged dataframe
    """
    print("=" * 50)
    print("DATA PREPROCESSING PIPELINE")
    print("=" * 50)
    
    # Load datasets
    activity_df, sleep_df, heart_rate_df = load_datasets(data_dir)
    
    # Merge datasets
    merged_df = merge_datasets(activity_df, sleep_df, heart_rate_df)
    
    # Save if output path provided
    if output_path:
        merged_df.to_csv(output_path, index=False)
        print(f"\nMerged dataset saved to {output_path}")
    
    return merged_df


if __name__ == '__main__':
    # Run preprocessing pipeline
    df = preprocess_pipeline(data_dir='data', output_path='data/merged_data.csv')
    print("\n✅ Preprocessing complete!")

