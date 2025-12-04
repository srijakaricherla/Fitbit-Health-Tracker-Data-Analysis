"""
Script to create architecture diagram for the Fitbit analysis project.
Run this script to generate the architecture diagram PNG file.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Ensure reports directory exists
os.makedirs('reports', exist_ok=True)

# Create figure
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Define colors
colors = {
    'data': '#E8F4F8',
    'process': '#FFF4E6',
    'analysis': '#F0E8FF',
    'output': '#E8F8E8'
}

# Define boxes with positions
boxes = [
    # Data layer
    {'text': 'Activity Data\n(activity.csv)', 'xy': (2, 9), 'width': 1.5, 'height': 1, 'color': colors['data']},
    {'text': 'Sleep Data\n(sleep.csv)', 'xy': (4, 9), 'width': 1.5, 'height': 1, 'color': colors['data']},
    {'text': 'Heart Rate Data\n(heart_rate.csv)', 'xy': (6.5, 9), 'width': 1.5, 'height': 1, 'color': colors['data']},
    
    # Preprocessing layer
    {'text': 'Data\nPreprocessing\n(preprocess.py)', 'xy': (3.5, 6.5), 'width': 2.5, 'height': 1.5, 'color': colors['process']},
    
    # Feature Engineering layer
    {'text': 'Feature\nEngineering\n(feature_engineering.py)', 'xy': (3.5, 4), 'width': 2.5, 'height': 1.5, 'color': colors['process']},
    
    # Analysis layer
    {'text': 'Clustering\n(clustering.py)', 'xy': (1, 1.5), 'width': 2, 'height': 1.5, 'color': colors['analysis']},
    {'text': 'Visualization\n(visualization.py)', 'xy': (4, 1.5), 'width': 2, 'height': 1.5, 'color': colors['analysis']},
    
    # Output layer
    {'text': 'Reports\n& Insights', 'xy': (7, 1.5), 'width': 2, 'height': 1.5, 'color': colors['output']},
]

# Draw boxes
for box in boxes:
    fancy_box = FancyBboxPatch(
        box['xy'], box['width'], box['height'],
        boxstyle='round,pad=0.1',
        edgecolor='black',
        facecolor=box['color'],
        linewidth=1.5
    )
    ax.add_patch(fancy_box)
    
    # Add text
    ax.text(
        box['xy'][0] + box['width']/2,
        box['xy'][1] + box['height']/2,
        box['text'],
        ha='center',
        va='center',
        fontsize=9,
        fontweight='bold'
    )

# Draw arrows (data flow)
arrow_patches = [
    # Data to preprocessing
    ((2.75, 9), (4.25, 8), ''),
    ((4.75, 9), (4.75, 8), ''),
    ((7.25, 9), (5.25, 8), ''),
    
    # Preprocessing to feature engineering
    ((4.75, 6.5), (4.75, 5.5), 'Merged Data'),
    
    # Feature engineering to analysis
    ((3.5, 4), (2, 2.25), 'User Features'),
    ((5.5, 4), (6, 2.25), 'Daily Features'),
    
    # Analysis to output
    ((3, 1.5), (7, 2.25), 'Results'),
]

for arrow_info in arrow_patches:
    start, end, label = arrow_info
    arrow_patch = FancyArrowPatch(
        start, end,
        arrowstyle='->',
        mutation_scale=20,
        linewidth=2,
        color='#333333'
    )
    ax.add_patch(arrow_patch)
    
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y + 0.15, label, ha='center', fontsize=8, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='none'))

# Add title
ax.text(5, 11.5, 'Fitbit Health Tracker Data Analysis - Architecture', 
        ha='center', fontsize=16, fontweight='bold')

# Add layer labels
ax.text(0.3, 9.5, 'DATA', ha='center', fontsize=11, fontweight='bold', 
        rotation=90, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'))
ax.text(0.3, 7.25, 'PREPROCESSING', ha='center', fontsize=11, fontweight='bold', 
        rotation=90, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'))
ax.text(0.3, 4.75, 'FEATURE\nENGINEERING', ha='center', fontsize=11, fontweight='bold', 
        rotation=90, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'))
ax.text(0.3, 2.25, 'ANALYSIS\n& OUTPUT', ha='center', fontsize=11, fontweight='bold', 
        rotation=90, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'))

plt.tight_layout()
plt.savefig('reports/architecture_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Architecture diagram saved to reports/architecture_diagram.png")
plt.close()

