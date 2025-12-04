"""
Data Visualization Module

This module creates various visualizations for the Fitbit analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def plot_distribution(df, column, title=None, ax=None):
    """
    Plot distribution of a numerical column.
    
    Args:
        df (pd.DataFrame): Input dataframe
        column (str): Column name to plot
        title (str): Plot title
        ax (matplotlib.axes): Axes object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.histplot(data=df, x=column, kde=True, ax=ax)
    ax.set_title(title or f'Distribution of {column}', fontsize=14, fontweight='bold')
    ax.set_xlabel(column.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    
    return ax


def plot_multiple_distributions(df, columns, n_cols=3):
    """
    Plot multiple distributions in a grid.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): List of column names
        n_cols (int): Number of columns in grid
    """
    n_rows = int(np.ceil(len(columns) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
    
    for idx, col in enumerate(columns):
        if col in df.columns:
            plot_distribution(df, col, title=f'Distribution of {col}', ax=axes[idx])
        else:
            axes[idx].text(0.5, 0.5, f'{col} not found', 
                          ha='center', va='center', transform=axes[idx].transAxes)
            axes[idx].set_title(f'{col} (not available)')
    
    # Hide unused subplots
    for idx in range(len(columns), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    return fig


def plot_correlation_heatmap(df, columns=None, title='Correlation Heatmap'):
    """
    Plot correlation heatmap for numerical columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): Columns to include (None = all numerical)
        title (str): Plot title
    """
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        columns = [col for col in numeric_cols if df[col].notna().sum() > 0]
    
    # Calculate correlation
    corr_matrix = df[columns].corr()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return fig


def plot_cluster_pca(user_features_df, cluster_labels, feature_names, n_components=2):
    """
    Plot clusters using PCA for dimensionality reduction.
    
    Args:
        user_features_df (pd.DataFrame): User features
        cluster_labels (np.array): Cluster assignments
        feature_names (list): Feature names used
        n_components (int): Number of PCA components
    """
    # Prepare data
    X = user_features_df[feature_names].values
    
    # Perform PCA
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X)
    
    # Create dataframe for plotting
    pca_df = pd.DataFrame(X_pca, columns=[f'PC{i+1}' for i in range(n_components)])
    pca_df['cluster'] = cluster_labels
    pca_df['user_id'] = user_features_df['user_id'].values
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get unique clusters and colors
    unique_clusters = sorted(pca_df['cluster'].unique())
    colors = sns.color_palette("husl", len(unique_clusters))
    
    for cluster_id, color in zip(unique_clusters, colors):
        cluster_data = pca_df[pca_df['cluster'] == cluster_id]
        ax.scatter(cluster_data['PC1'], cluster_data['PC2'], 
                  label=f'Cluster {cluster_id}', color=color, s=100, alpha=0.7)
    
    ax.set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]:.1%} variance)', 
                 fontsize=12)
    ax.set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]:.1%} variance)', 
                 fontsize=12)
    ax.set_title('User Clusters Visualization (PCA)', fontsize=16, fontweight='bold')
    ax.legend(title='Clusters', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return fig, pca


def plot_cluster_profiles(cluster_profiles_df, feature_names):
    """
    Plot cluster profile comparison.
    
    Args:
        cluster_profiles_df (pd.DataFrame): Cluster profile summary
        feature_names (list): Feature names to plot
    """
    # Prepare data for plotting
    plot_data = []
    for _, row in cluster_profiles_df.iterrows():
        for feature in feature_names:
            col_name = f'avg_{feature}'
            if col_name in row.index:
                plot_data.append({
                    'cluster': row['cluster'],
                    'feature': feature,
                    'value': row[col_name]
                })
    
    plot_df = pd.DataFrame(plot_data)
    
    # Create grouped bar plot
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(feature_names))
    width = 0.25
    clusters = sorted(plot_df['cluster'].unique())
    colors = sns.color_palette("Set2", len(clusters))
    
    for i, cluster_id in enumerate(clusters):
        cluster_values = [
            plot_df[(plot_df['cluster'] == cluster_id) & (plot_df['feature'] == feat)]['value'].iloc[0]
            if len(plot_df[(plot_df['cluster'] == cluster_id) & (plot_df['feature'] == feat)]) > 0
            else 0
            for feat in feature_names
        ]
        ax.bar(x + i * width, cluster_values, width, 
               label=f'Cluster {cluster_id}', color=colors[i], alpha=0.8)
    
    ax.set_xlabel('Features', fontsize=12)
    ax.set_ylabel('Average Value', fontsize=12)
    ax.set_title('Cluster Profile Comparison', fontsize=16, fontweight='bold')
    ax.set_xticks(x + width * (len(clusters) - 1) / 2)
    ax.set_xticklabels([f.replace('_', ' ').title() for f in feature_names], 
                       rotation=45, ha='right')
    ax.legend(title='Clusters', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    return fig


def create_all_visualizations(daily_df, user_features_df, cluster_labels, 
                              cluster_profiles, feature_names, output_dir='reports'):
    """
    Create all visualizations and save them.
    
    Args:
        daily_df (pd.DataFrame): Daily features dataframe
        user_features_df (pd.DataFrame): User features dataframe
        cluster_labels (np.array): Cluster assignments
        cluster_profiles (pd.DataFrame): Cluster profiles
        feature_names (list): Feature names
        output_dir (str): Output directory for plots
    """
    from pathlib import Path
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("=" * 50)
    print("CREATING VISUALIZATIONS")
    print("=" * 50)
    
    # 1. Distribution plots
    print("Creating distribution plots...")
    dist_cols = ['steps', 'sleep_efficiency', 'avg_resting_hr']
    available_dist_cols = [col for col in dist_cols if col in daily_df.columns]
    if available_dist_cols:
        fig = plot_multiple_distributions(daily_df, available_dist_cols)
        fig.savefig(output_path / 'distributions.png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        print("  ✓ Saved distributions.png")
    
    # 2. Correlation heatmap
    print("Creating correlation heatmap...")
    heatmap_cols = [
        'steps', 'calories_burned', 'sleep_efficiency', 
        'avg_resting_hr', 'high_intensity_minutes'
    ]
    available_heatmap_cols = [col for col in heatmap_cols if col in daily_df.columns]
    if available_heatmap_cols:
        fig = plot_correlation_heatmap(daily_df, available_heatmap_cols)
        fig.savefig(output_path / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        print("  ✓ Saved correlation_heatmap.png")
    
    # 3. Cluster PCA visualization
    print("Creating cluster PCA visualization...")
    fig, pca = plot_cluster_pca(user_features_df, cluster_labels, feature_names)
    fig.savefig(output_path / 'cluster_pca.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Saved cluster_pca.png")
    
    # 4. Cluster profiles
    print("Creating cluster profile comparison...")
    fig = plot_cluster_profiles(cluster_profiles, feature_names)
    fig.savefig(output_path / 'cluster_profiles.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  ✓ Saved cluster_profiles.png")
    
    print("\n✅ All visualizations created and saved!")


if __name__ == '__main__':
    # Example usage
    import sys
    from pathlib import Path
    
    sys.path.append(str(Path(__file__).parent.parent))
    
    from src.preprocess import preprocess_pipeline
    from src.feature_engineering import feature_engineering_pipeline
    from src.clustering import clustering_pipeline
    
    # Run full pipeline
    df = preprocess_pipeline(data_dir='data')
    daily_features, user_features = feature_engineering_pipeline(df)
    user_features_clustered, profiles, kmeans, scaler, X_scaled, feature_names = clustering_pipeline(
        user_features, n_clusters=3
    )
    
    # Create visualizations
    create_all_visualizations(
        daily_features,
        user_features_clustered,
        user_features_clustered['cluster'].values,
        profiles,
        feature_names
    )

