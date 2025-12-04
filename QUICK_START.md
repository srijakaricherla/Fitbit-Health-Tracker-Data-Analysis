# Quick Start Guide

## Initial Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Sample Data** (if you want full datasets)
   ```bash
   python generate_sample_data.py
   ```
   Note: Sample CSV files with headers are already in `data/` directory.

3. **Generate Architecture Diagram** (optional)
   ```bash
   python create_architecture_diagram.py
   ```
   This will create `reports/architecture_diagram.png`

## Running the Analysis

### Option 1: Run Complete Pipeline
```bash
python main.py
```

### Option 2: Use Jupyter Notebook (Recommended)
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

### Option 3: Run Individual Modules
```bash
# Preprocessing
python src/preprocess.py

# Feature Engineering
python src/feature_engineering.py

# Clustering
python src/clustering.py

# Visualization
python src/visualization.py
```

## Project Structure

```
fitbit-health-analysis/
├── data/                    # CSV datasets
├── notebooks/               # Jupyter notebook
├── src/                     # Source code modules
├── reports/                 # Output reports and visualizations
├── main.py                 # Main pipeline script
├── requirements.txt        # Dependencies
└── README.md              # Full documentation
```

## Next Steps

1. Explore the Jupyter notebook for detailed analysis
2. Check `reports/` directory for generated visualizations
3. Review `reports/summary_report.md` for insights
4. Run git commands from `GIT_COMMANDS.md` when ready

