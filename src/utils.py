"""
Utility Functions Module

Helper functions for the Fitbit analysis project.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json


def load_config(config_path='config.json'):
    """
    Load configuration from JSON file.
    
    Args:
        config_path (str): Path to config file
        
    Returns:
        dict: Configuration dictionary
    """
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        # Return default config
        return {
            'data_dir': 'data',
            'output_dir': 'reports',
            'n_clusters': 3,
            'random_state': 42
        }


def save_results(results_dict, output_path):
    """
    Save analysis results to JSON file.
    
    Args:
        results_dict (dict): Dictionary of results
        output_path (str): Path to save results
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_numpy_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(item) for item in obj]
        return obj
    
    results_serializable = convert_numpy_types(results_dict)
    
    with open(output_file, 'w') as f:
        json.dump(results_serializable, f, indent=2)
    
    print(f"Results saved to {output_path}")


def print_summary_stats(df, columns=None):
    """
    Print summary statistics for a dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe
        columns (list): Columns to summarize (None = all numerical)
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    print("\n" + "=" * 50)
    print("SUMMARY STATISTICS")
    print("=" * 50)
    print(df[columns].describe().round(2))


def validate_data(df, required_columns):
    """
    Validate that dataframe contains required columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        required_columns (list): List of required column names
        
    Returns:
        bool: True if all required columns present
    """
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        print(f"Warning: Missing required columns: {missing_cols}")
        return False
    return True


def format_number(num, decimals=2):
    """
    Format number with specified decimal places.
    
    Args:
        num: Number to format
        decimals (int): Number of decimal places
        
    Returns:
        str: Formatted number string
    """
    if pd.isna(num):
        return "N/A"
    return f"{num:.{decimals}f}"


def get_data_info(df):
    """
    Get basic information about dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Dictionary with data info
    """
    return {
        'shape': df.shape,
        'columns': list(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'null_counts': df.isnull().sum().to_dict(),
        'dtypes': df.dtypes.astype(str).to_dict()
    }


if __name__ == '__main__':
    # Example usage
    import pandas as pd
    
    # Create sample dataframe
    df = pd.DataFrame({
        'col1': [1, 2, 3, 4, 5],
        'col2': [1.1, 2.2, 3.3, 4.4, 5.5],
        'col3': ['a', 'b', 'c', 'd', 'e']
    })
    
    # Test utility functions
    print("Data Info:")
    info = get_data_info(df)
    print(info)
    
    print("\nSummary Stats:")
    print_summary_stats(df)

