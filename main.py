"""
Main Pipeline Script for Fitbit Health Tracker Data Analysis

This script runs the complete analysis pipeline:
1. Data Preprocessing
2. Feature Engineering
3. Clustering
4. Visualization
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.preprocess import preprocess_pipeline
from src.feature_engineering import feature_engineering_pipeline
from src.clustering import clustering_pipeline
from src.visualization import create_all_visualizations

def main():
    """Run the complete analysis pipeline."""
    print("=" * 60)
    print("FITBIT HEALTH TRACKER DATA ANALYSIS - MAIN PIPELINE")
    print("=" * 60)
    
    # Step 1: Preprocessing
    print("\n[STEP 1/4] Preprocessing data...")
    df = preprocess_pipeline(data_dir='data')
    
    # Step 2: Feature Engineering
    print("\n[STEP 2/4] Engineering features...")
    daily_features, user_features = feature_engineering_pipeline(df)
    
    # Step 3: Clustering
    print("\n[STEP 3/4] Performing clustering...")
    user_features_clustered, profiles, kmeans, scaler, X_scaled, feature_names = clustering_pipeline(
        user_features, 
        n_clusters=3,
        random_state=42
    )
    
    # Step 4: Visualization
    print("\n[STEP 4/4] Creating visualizations...")
    create_all_visualizations(
        daily_features,
        user_features_clustered,
        user_features_clustered['cluster'].values,
        profiles,
        feature_names,
        output_dir='reports'
    )
    
    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\nResults saved in the 'reports/' directory.")
    print("Check the Jupyter notebook for detailed analysis.")

if __name__ == '__main__':
    main()

