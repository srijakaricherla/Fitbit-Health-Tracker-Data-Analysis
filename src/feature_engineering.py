"""
Feature Engineering Module

This module creates derived features for clustering and analysis.
"""

import pandas as pd
import numpy as np


def calculate_sleep_efficiency(df):
    """
    Calculate sleep efficiency if not already present.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: DataFrame with sleep_efficiency feature
    """
    if 'sleep_efficiency' not in df.columns:
        if 'sleep_duration_minutes' in df.columns and 'time_in_bed_minutes' in df.columns:
            df['sleep_efficiency'] = (
                df['sleep_duration_minutes'] / df['time_in_bed_minutes']
            ).fillna(0)
            df['sleep_efficiency'] = df['sleep_efficiency'].clip(0, 1)
    return df


def calculate_high_intensity_minutes(df):
    """
    Calculate high intensity activity minutes.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: DataFrame with high_intensity_minutes feature
    """
    if 'very_active_minutes' in df.columns and 'moderately_active_minutes' in df.columns:
        df['high_intensity_minutes'] = (
            df['very_active_minutes'] + 
            df['moderately_active_minutes'] * 0.5
        )
    return df


def calculate_lifestyle_score(df):
    """
    Calculate a composite lifestyle score based on multiple metrics.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: DataFrame with lifestyle_score feature
    """
    score_components = []
    
    # Steps component (normalized)
    if 'steps' in df.columns:
        steps_score = (df['steps'] / 10000).clip(0, 2)  # 10k steps = 1.0
        score_components.append(steps_score * 0.3)
    
    # Sleep component (normalized)
    if 'sleep_efficiency' in df.columns:
        sleep_score = df['sleep_efficiency'] * 2  # 0-2 scale
        score_components.append(sleep_score * 0.25)
    
    # Activity component
    if 'high_intensity_minutes' in df.columns:
        activity_score = (df['high_intensity_minutes'] / 60).clip(0, 2)
        score_components.append(activity_score * 0.25)
    
    # Heart rate component (resting HR - lower is better, normalized)
    if 'avg_resting_hr' in df.columns:
        hr_score = (75 - df['avg_resting_hr']) / 20  # 55-75 range -> 1.0-0.0
        hr_score = hr_score.clip(0, 1)
        score_components.append(hr_score * 0.2)
    
    # Calculate weighted sum
    if score_components:
        df['lifestyle_score'] = pd.concat(score_components, axis=1).sum(axis=1)
        df['lifestyle_score'] = df['lifestyle_score'].fillna(0)
    else:
        df['lifestyle_score'] = 0
    
    return df


def create_daily_features(df):
    """
    Create daily aggregated features.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: DataFrame with daily features
    """
    # Calculate sleep efficiency
    df = calculate_sleep_efficiency(df)
    
    # Calculate high intensity minutes
    df = calculate_high_intensity_minutes(df)
    
    # Calculate lifestyle score
    df = calculate_lifestyle_score(df)
    
    return df


def create_user_features(df):
    """
    Create user-level aggregated features for clustering.
    
    Args:
        df (pd.DataFrame): Input dataframe with daily metrics
        
    Returns:
        pd.DataFrame: DataFrame with user-level features
    """
    # Group by user and calculate averages
    user_features = df.groupby('user_id').agg({
        'steps': 'mean',
        'sedentary_minutes': 'mean',
        'calories_burned': 'mean',
        'sleep_efficiency': 'mean',
        'time_in_bed_minutes': 'mean',
        'avg_resting_hr': 'mean',
        'high_intensity_minutes': 'mean',
        'lifestyle_score': 'mean'
    }).reset_index()
    
    # Rename columns for clarity
    user_features.columns = [
        'user_id',
        'avg_steps',
        'avg_sedentary_minutes',
        'avg_calories_burned',
        'avg_sleep_efficiency',
        'avg_time_in_bed',
        'avg_resting_hr',
        'avg_high_intensity_minutes',
        'avg_lifestyle_score'
    ]
    
    return user_features


def feature_engineering_pipeline(df):
    """
    Complete feature engineering pipeline.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        
    Returns:
        tuple: (daily_features_df, user_features_df)
    """
    print("=" * 50)
    print("FEATURE ENGINEERING PIPELINE")
    print("=" * 50)
    
    # Create daily features
    daily_df = create_daily_features(df.copy())
    print(f"Created daily features: {len(daily_df)} records")
    
    # Create user-level features
    user_df = create_user_features(daily_df)
    print(f"Created user features: {len(user_df)} users")
    
    print("\nFeature columns:")
    print(f"Daily features: {list(daily_df.columns)}")
    print(f"User features: {list(user_df.columns)}")
    
    return daily_df, user_df


if __name__ == '__main__':
    # Example usage
    import sys
    from pathlib import Path
    
    # Add parent directory to path
    sys.path.append(str(Path(__file__).parent.parent))
    
    from src.preprocess import preprocess_pipeline
    
    # Load preprocessed data
    df = preprocess_pipeline(data_dir='data')
    
    # Create features
    daily_features, user_features = feature_engineering_pipeline(df)
    
    print("\n✅ Feature engineering complete!")
    print(f"\nUser features sample:")
    print(user_features.head())

