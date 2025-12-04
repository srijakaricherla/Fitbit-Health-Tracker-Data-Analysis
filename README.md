# Fitbit Health Tracker Data Analysis

A comprehensive Python data analysis project that analyzes Fitbit activity, sleep, and heart-rate data from 33 users across 30 days. This project identifies health & behavioral patterns and clusters users based on lifestyle & intensity metrics.

## 📋 Overview

This project provides an end-to-end data analysis pipeline for Fitbit health tracker data. It processes activity, sleep, and heart rate datasets, engineers meaningful features, performs clustering analysis, and generates comprehensive visualizations to identify distinct user lifestyle patterns.

**Key Features:**
- ✅ Multi-dataset preprocessing and merging
- ✅ Advanced feature engineering (activity, sleep, HR metrics)
- ✅ KMeans clustering for user segmentation
- ✅ Comprehensive data visualizations
- ✅ Interactive Jupyter notebook for exploratory analysis

## 📊 Dataset Description

The analysis utilizes three primary datasets containing data from **33 users** over **30 days** (990 records per dataset):

### 1. Activity Data (`activity.csv`)
- `user_id`: Unique user identifier
- `date`: Date of record (YYYY-MM-DD)
- `steps`: Daily step count
- `calories_burned`: Total calories burned
- `sedentary_minutes`: Minutes spent sedentary
- `lightly_active_minutes`: Minutes of light activity
- `moderately_active_minutes`: Minutes of moderate activity
- `very_active_minutes`: Minutes of very active movement

### 2. Sleep Data (`sleep.csv`)
- `user_id`: Unique user identifier
- `date`: Date of record
- `time_in_bed_minutes`: Total time in bed
- `sleep_duration_minutes`: Actual sleep duration
- `sleep_efficiency`: Sleep efficiency ratio (0-1)
- `deep_sleep_minutes`: Deep sleep duration
- `rem_sleep_minutes`: REM sleep duration
- `light_sleep_minutes`: Light sleep duration

### 3. Heart Rate Data (`heart_rate.csv`)
- `user_id`: Unique user identifier
- `date`: Date of record
- `avg_resting_hr`: Average resting heart rate (bpm)
- `avg_hr`: Average heart rate (bpm)
- `max_hr`: Maximum heart rate (bpm)
- `min_hr`: Minimum heart rate (bpm)
- `calories_burned_hr`: Calories burned (HR-based)

## 🏗️ Project Architecture Diagram

![Architecture Diagram](reports/architecture_diagram.png)

The project follows a modular architecture with clear data flow:

```
Raw Fitbit Data (CSV Files)
    ↓
Data Preprocessing (preprocess.py)
    ↓
Feature Engineering (feature_engineering.py)
    ↓
Clustering + Visualization (clustering.py + visualization.py)
    ↓
Reports & Insights
```

## 🛠️ Tech Stack

- **Python 3.8+**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Scikit-learn** - Machine learning (KMeans, StandardScaler, PCA)
- **Matplotlib** - Data visualization
- **Seaborn** - Statistical visualizations
- **Jupyter** - Interactive analysis environment

## ✨ Features

### 1. Data Preprocessing (`src/preprocess.py`)
- Load all datasets (activity, sleep, heart rate)
- Clean nulls and duplicates
- Aggregate data to daily metrics
- Merge datasets on user_id + date

### 2. Feature Engineering (`src/feature_engineering.py`)
Creates comprehensive features:
- **Activity Features**: avg_steps, sedentary_minutes, calories_burned
- **Sleep Features**: sleep_efficiency, time_in_bed
- **Heart Rate Features**: avg_resting_hr, high_intensity_minutes
- **Composite Features**: Summary lifestyle score

### 3. Clustering (`src/clustering.py`)
- KMeans clustering (2-4 clusters)
- Feature scaling using StandardScaler
- Cluster profile analysis
- User segmentation based on lifestyle patterns

### 4. Data Visualization (`src/visualization.py`)
Generates multiple visualizations:
- Distribution plots (steps, sleep, heart rate)
- Correlation heatmap
- Cluster visualization using PCA 2D plot
- Cluster profile comparisons

### 5. Exploratory Analysis Notebook (`notebooks/exploratory_analysis.ipynb`)
- Complete EDA workflow
- Interactive visualizations
- Cluster interpretation
- Insights and conclusions

## 📁 Project Structure

```
fitbit-health-analysis/
│
├── data/                          # Sample CSV dataset directory
│   ├── activity.csv
│   ├── sleep.csv
│   └── heart_rate.csv
│
├── notebooks/
│   └── exploratory_analysis.ipynb # Interactive EDA notebook
│
├── src/
│   ├── preprocess.py             # Data cleaning, merging
│   ├── feature_engineering.py    # Feature creation
│   ├── clustering.py             # KMeans clustering code
│   ├── visualization.py          # Seaborn/matplotlib graphs
│   └── utils.py                  # Helper functions
│
├── reports/
│   ├── summary_report.md         # Analysis summary report
│   └── architecture_diagram.png  # System architecture diagram
│
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .gitignore                    # Git ignore file
├── generate_sample_data.py       # Script to generate sample data
└── create_architecture_diagram.py # Script to generate architecture diagram
```

## 🚀 How to Run

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Fitbit Health Tracker Data Analysis"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data** (if data files don't exist)
   ```bash
   python generate_sample_data.py
   ```
   This will create three CSV files in the `data/` directory with sample data for 33 users over 30 days.

4. **Generate architecture diagram** (optional)
   ```bash
   python create_architecture_diagram.py
   ```

### Running the Analysis

#### Option 1: Run Individual Modules

**Preprocessing:**
```bash
python src/preprocess.py
```

**Feature Engineering:**
```bash
python src/feature_engineering.py
```

**Clustering:**
```bash
python src/clustering.py
```

**Visualization:**
```bash
python src/visualization.py
```

#### Option 2: Use Jupyter Notebook (Recommended)

1. **Start Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

2. **Open the notebook**
   - Navigate to `notebooks/exploratory_analysis.ipynb`
   - Run all cells sequentially for complete analysis

#### Option 3: Create a Main Pipeline Script

You can create a main script to run the entire pipeline:

```python
from src.preprocess import preprocess_pipeline
from src.feature_engineering import feature_engineering_pipeline
from src.clustering import clustering_pipeline
from src.visualization import create_all_visualizations

# Run complete pipeline
df = preprocess_pipeline(data_dir='data')
daily_features, user_features = feature_engineering_pipeline(df)
user_features_clustered, profiles, kmeans, scaler, X_scaled, feature_names = clustering_pipeline(
    user_features, n_clusters=3
)
create_all_visualizations(
    daily_features,
    user_features_clustered,
    user_features_clustered['cluster'].values,
    profiles,
    feature_names
)
```

## 📈 Sample Visualizations

The project generates several visualizations:

1. **Distribution Plots**: Steps, sleep efficiency, heart rate distributions
2. **Correlation Heatmap**: Relationships between key health metrics
3. **Cluster PCA Plot**: 2D visualization of user clusters
4. **Cluster Profiles**: Comparison of cluster characteristics

All visualizations are saved in the `reports/` directory.

## 🔮 Future Enhancements

1. **Advanced Clustering Algorithms**
   - DBSCAN for density-based clustering
   - Hierarchical clustering with dendrograms
   - Gaussian Mixture Models

2. **Time Series Analysis**
   - Trend analysis over 30-day period
   - Seasonal pattern detection
   - Anomaly detection

3. **Predictive Modeling**
   - Predict health outcomes
   - Activity level forecasting
   - Sleep quality prediction

4. **Real-time Processing**
   - Streaming data processing
   - Live dashboard updates
   - Real-time cluster assignments

5. **Enhanced Features**
   - Weight and BMI tracking
   - Workout type classification
   - Stress level indicators

6. **Interactive Dashboard**
   - Web-based dashboard
   - User filtering and drill-down
   - Export capabilities

7. **Personalized Recommendations**
   - Health goal suggestions
   - Activity recommendations per cluster
   - Sleep optimization tips

## 📝 Notes

- The sample data is generated with realistic patterns but is synthetic
- Clustering results may vary based on the random_state parameter
- Adjust `n_clusters` in clustering pipeline to explore different segmentations
- All visualizations use high DPI (300) for publication quality

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available for educational purposes.

---

**Project Version**: 1.0  
**Last Updated**: 2024  
**Maintained by**: Fitbit Health Tracker Data Analysis Team
