"""
Clustering Module

This module performs KMeans clustering on user features.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')


def select_features_for_clustering(user_features_df):
    """
    Select and prepare features for clustering.
    
    Args:
        user_features_df (pd.DataFrame): User-level features
        
    Returns:
        tuple: (feature_matrix, feature_names)
    """
    # Select relevant features for clustering
    feature_cols = [
        'avg_steps',
        'avg_sedentary_minutes',
        'avg_calories_burned',
        'avg_sleep_efficiency',
        'avg_resting_hr',
        'avg_high_intensity_minutes',
        'avg_lifestyle_score'
    ]
    
    # Filter to available columns
    available_cols = [col for col in feature_cols if col in user_features_df.columns]
    
    if len(available_cols) < 3:
        raise ValueError("Not enough features available for clustering")
    
    # Extract feature matrix
    X = user_features_df[available_cols].values
    
    return X, available_cols


def scale_features(X):
    """
    Scale features using StandardScaler.
    
    Args:
        X (np.array): Feature matrix
        
    Returns:
        tuple: (scaled_X, scaler)
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler


def perform_kmeans_clustering(X_scaled, n_clusters=3, random_state=42):
    """
    Perform KMeans clustering.
    
    Args:
        X_scaled (np.array): Scaled feature matrix
        n_clusters (int): Number of clusters
        random_state (int): Random state for reproducibility
        
    Returns:
        tuple: (kmeans_model, cluster_labels)
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    return kmeans, cluster_labels


def analyze_cluster_profiles(user_features_df, cluster_labels, feature_names):
    """
    Analyze and summarize cluster profiles.
    
    Args:
        user_features_df (pd.DataFrame): User features
        cluster_labels (np.array): Cluster assignments
        feature_names (list): Names of features used
        
    Returns:
        pd.DataFrame: Cluster profile summary
    """
    # Add cluster labels to dataframe
    user_features_df = user_features_df.copy()
    user_features_df['cluster'] = cluster_labels
    
    # Calculate cluster statistics
    cluster_profiles = []
    
    for cluster_id in sorted(user_features_df['cluster'].unique()):
        cluster_data = user_features_df[user_features_df['cluster'] == cluster_id]
        
        profile = {
            'cluster': cluster_id,
            'n_users': len(cluster_data)
        }
        
        # Add mean values for each feature
        for feature in feature_names:
            if feature in cluster_data.columns:
                profile[f'avg_{feature}'] = cluster_data[feature].mean()
        
        cluster_profiles.append(profile)
    
    profile_df = pd.DataFrame(cluster_profiles)
    
    return user_features_df, profile_df


def clustering_pipeline(user_features_df, n_clusters=3, random_state=42):
    """
    Complete clustering pipeline.
    
    Args:
        user_features_df (pd.DataFrame): User-level features
        n_clusters (int): Number of clusters
        random_state (int): Random state
        
    Returns:
        tuple: (user_features_with_clusters, cluster_profiles, kmeans_model, scaler, X_scaled)
    """
    print("=" * 50)
    print("CLUSTERING PIPELINE")
    print("=" * 50)
    
    # Select features
    X, feature_names = select_features_for_clustering(user_features_df)
    print(f"Selected {len(feature_names)} features: {feature_names}")
    
    # Scale features
    X_scaled, scaler = scale_features(X)
    print("Features scaled using StandardScaler")
    
    # Perform clustering
    kmeans, cluster_labels = perform_kmeans_clustering(
        X_scaled, 
        n_clusters=n_clusters, 
        random_state=random_state
    )
    print(f"KMeans clustering completed with {n_clusters} clusters")
    
    # Analyze clusters
    user_features_with_clusters, cluster_profiles = analyze_cluster_profiles(
        user_features_df.copy(),
        cluster_labels,
        feature_names
    )
    
    print("\nCluster distribution:")
    print(user_features_with_clusters['cluster'].value_counts().sort_index())
    
    print("\nCluster profiles:")
    print(cluster_profiles.round(2))
    
    return user_features_with_clusters, cluster_profiles, kmeans, scaler, X_scaled, feature_names


if __name__ == '__main__':
    # Example usage
    import sys
    from pathlib import Path
    
    sys.path.append(str(Path(__file__).parent.parent))
    
    from src.preprocess import preprocess_pipeline
    from src.feature_engineering import feature_engineering_pipeline
    
    # Load and preprocess data
    df = preprocess_pipeline(data_dir='data')
    
    # Create features
    daily_features, user_features = feature_engineering_pipeline(df)
    
    # Perform clustering
    user_features_clustered, profiles, kmeans, scaler, X_scaled, feature_names = clustering_pipeline(
        user_features, 
        n_clusters=3
    )
    
    print("\n✅ Clustering complete!")

