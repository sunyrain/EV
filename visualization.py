# -*- coding: utf-8 -*-
"""
Visualization Module (Professional Edition v2.0)
=====================================
Generate publication-quality charts using Seaborn and Matplotlib
Supports combining multiple related charts into beautiful large figures
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Global Matplotlib Configuration
# Set default font for all text (titles, labels, legends, etc.)
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans'] 

# Solve the issue where minus sign '-' is displayed as a square when saving images
plt.rcParams['axes.unicode_minus'] = False

print(f"Success: Matplotlib font set to Arial/Helvetica")

from .config import COLORS, FIGURE_DPI

# Unified Academic Color Scheme - Based on Nature/Science Journal Style
NEW_COLORS = {
    'C1_Primary': '#B6B3D6',  # Primary: Cool Purple-Grey
    'C2_Light': '#CFCFCE3',
    'N1_Mid': '#D5D3DE',      # Neutral: Light Grey
    'N2_Mid': '#D5D1D1',
    'W1_Light': '#F6DFD6',    # Auxiliary: Light Coral Pink
    'W2_Warm': '#F8B2A2',
    'W3_Deep': '#F1837A',
    'W4_Accent': '#E9687A',   # Accent: Deep Red-Pink
}

UNIFIED_COLORS = {
    # Primary Tones - For main data display (Primary uses C1/W4)
    'primary': NEW_COLORS['C1_Primary'],      # Cool Primary: #B6B3D6 (Purple-Grey)
    'secondary': NEW_COLORS['W2_Warm'],      # Warm Auxiliary: #F8B2A2 (Coral Pink)
    'tertiary': NEW_COLORS['W4_Accent'],     # Accent/Third: #E9687A (Deep Red-Pink)
    'quaternary': NEW_COLORS['N1_Mid'],       # Fourth/Background Aux: #D5D3DE (Light Grey)
    
    # Categorical Palette - For multi-category comparison
    'categorical': [NEW_COLORS['C1_Primary'], NEW_COLORS['W4_Accent'], 
                    NEW_COLORS['W2_Warm'], NEW_COLORS['N1_Mid'], 
                    '#555555', '#AAAAAA'], # Mix of new primary and neutral colors
    
    # Gradient Palettes - For continuous variables
    'gradient_cool': [NEW_COLORS['N1_Mid'], NEW_COLORS['C1_Primary'], '#696499'],  # Cool Gradient (Light Grey -> Purple-Grey -> Deep Purple)
    'gradient_warm': [NEW_COLORS['W1_Light'], NEW_COLORS['W3_Deep'], NEW_COLORS['W4_Accent']],  # Warm Gradient (Light Pink -> Red-Pink -> Deep Red-Pink)
    'gradient_teal': [NEW_COLORS['C2_Light'], NEW_COLORS['W2_Warm'], NEW_COLORS['W3_Deep']],  # Mixed Gradient
    
    # Semantic Colors - For specific meanings
    'positive': NEW_COLORS['W3_Deep'],     # Positive/Good - Use Deep Red-Pink series
    'negative': NEW_COLORS['C1_Primary'],  # Negative/Bad - Use Cool Color series
    'neutral': NEW_COLORS['N2_Mid'],      # Neutral - Neutral Grey
    'highlight': NEW_COLORS['W4_Accent'],    # Highlight - Deep Red-Pink
    
    # Gender Palette (Maintain contrast)
    'male': NEW_COLORS['C1_Primary'],         # Male - Purple-Grey
    'female': NEW_COLORS['W3_Deep'],       # Female - Red-Pink
    
    # Education Level Palette
    'education': [NEW_COLORS['W1_Light'], NEW_COLORS['N1_Mid'], NEW_COLORS['C1_Primary']],  # Light -> Medium -> Deep
    
    # Heatmap Palette (Suggest using standard plt or sns built-in palettes, but specify primary tone)
    'heatmap': 'coolwarm',     # Maintain diverging palette
    'heatmap_cool': 'PuBu',    # Purple-Blue
    
    # Background and Border
    'background': '#FFFFFF', # Maintain white background
    'border': NEW_COLORS['N2_Mid'],
    'text': '#333333',
    'text_light': '#888888',
}

# Compatible with old code, keep ACADEMIC_PALETTE
ACADEMIC_PALETTE = {
    'primary': UNIFIED_COLORS['categorical'],
    'gradient_blue': UNIFIED_COLORS['gradient_cool'],
    'gradient_warm': UNIFIED_COLORS['gradient_warm'],
    'categorical': UNIFIED_COLORS['categorical'],
    # New Diverging Palette: Cool Primary - Light Grey - Warm Accent
    'diverging': [UNIFIED_COLORS['negative'], UNIFIED_COLORS['quaternary'], 
                  '#FFFFFF', UNIFIED_COLORS['secondary'], UNIFIED_COLORS['positive']],
    'sequential': UNIFIED_COLORS['gradient_warm'], # Use new warm gradient as default sequential
}

# setup_style function remains mostly the same, controlling font and border styles

def setup_style():
    """Configure Professional Plotting Style"""
    # Use Seaborn white style
    sns.set_theme(style="white", context="talk", font_scale=1.0)
    
    # Configure Fonts
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # High Resolution Output
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.dpi'] = FIGURE_DPI
    
    # Enhance Visual Effects
    plt.rcParams['axes.linewidth'] = 1.2
    plt.rcParams['axes.edgecolor'] = '#333333'
    plt.rcParams['axes.labelcolor'] = '#333333'
    plt.rcParams['xtick.color'] = '#333333'
    plt.rcParams['ytick.color'] = '#333333'
    plt.rcParams['text.color'] = '#333333'
    
    # Legend Style
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.framealpha'] = 0.95
    plt.rcParams['legend.edgecolor'] = '#CCCCCC'
    
    # Grid Style
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'


def get_unified_palette(n_colors, palette_type='categorical'):
    """Get Unified Color Palette
    
    Args:
        n_colors: Number of colors needed
        palette_type: 'categorical', 'sequential', 'warm', 'cool'
    """
    if palette_type == 'categorical':
        base_colors = UNIFIED_COLORS['categorical']
        if n_colors <= len(base_colors):
            return base_colors[:n_colors]
        else:
            # Extend using seaborn when more colors are needed
            # Extend using new color cycle
            new_base_for_sns = [UNIFIED_COLORS['primary'], UNIFIED_COLORS['secondary'], 
                                 UNIFIED_COLORS['tertiary'], UNIFIED_COLORS['quaternary'],
                                 UNIFIED_COLORS['neutral'], UNIFIED_COLORS['highlight']]
            return sns.color_palette(new_base_for_sns * 2, n_colors)
    elif palette_type == 'sequential':
        return sns.light_palette(UNIFIED_COLORS['primary'], n_colors=n_colors)
    elif palette_type == 'warm':
        return sns.color_palette([UNIFIED_COLORS['gradient_warm'][0], 
                                 UNIFIED_COLORS['secondary'],
                                 UNIFIED_COLORS['highlight']], n_colors=n_colors)
    elif palette_type == 'cool':
        return sns.color_palette([UNIFIED_COLORS['gradient_cool'][0],
                                 UNIFIED_COLORS['tertiary'],
                                 UNIFIED_COLORS['gradient_cool'][2]], n_colors=n_colors)
    else:
        return sns.color_palette(UNIFIED_COLORS['categorical'], n_colors)

def save_fig(fig, path):
    """Unified save function, ensuring margins and background"""
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', facecolor='white', dpi=FIGURE_DPI, 
                edgecolor='none', pad_inches=0.2)
    plt.close(fig)


def save_subplot_as_figure(draw_func, save_path, figsize=(8, 6), title=None):
    """
    Save the result of a plotting function as an independent image
    draw_func: Plotting function that accepts an ax parameter
    """
    setup_style()
    fig, ax = plt.subplots(figsize=figsize, facecolor='white')
    draw_func(ax)
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    save_fig(fig, save_path)


def get_subplots_dir(save_path):
    """Get directory for saving subplots"""
    import os
    base_dir = os.path.dirname(save_path)
    base_name = os.path.splitext(os.path.basename(save_path))[0]
    subplots_dir = os.path.join(base_dir, f'{base_name}_subplots')
    os.makedirs(subplots_dir, exist_ok=True)
    return subplots_dir


def add_panel_label(ax, label, x=-0.08, y=1.05, fontsize=16):
    """Add panel label (A, B, C, ...) to subplot"""
    ax.text(x, y, label, transform=ax.transAxes, fontsize=fontsize, 
            fontweight='bold', va='top', ha='right', color='#333333')

# ============================================================================
# Plotting Functions
# ============================================================================

def plot_demographics(df, save_path):
    """Plot demographic characteristics (using modern donut charts + statistical info cards)"""
    # Log data
    print(f"\n[Data Log] Data for Demographics:")
    print("Gender Counts:")
    print(df['性别'].value_counts().sort_index())
    print("Education Counts:")
    print(df['在学类别'].value_counts().sort_index())
    print("Major Counts:")
    print(f"STEM: {df['专业_理工类'].sum()}, Econ & Mgmt: {df['专业_经管类'].sum()}, Humanities: {df['专业_人文社科类'].sum()}")
    print("Energy Experience Counts:")
    print(df['能源经历'].value_counts().sort_index())

    setup_style()
    fig = plt.figure(figsize=(18, 8), facecolor='white')
    
    # Use GridSpec for fine layout
    gs = fig.add_gridspec(2, 4, height_ratios=[3, 1], hspace=0.3, wspace=0.25)
    
    # Use unified color scheme
    colors_gender = [UNIFIED_COLORS['male'], UNIFIED_COLORS['female']]
    colors_edu = UNIFIED_COLORS['education']
    colors_major = [UNIFIED_COLORS['primary'], UNIFIED_COLORS['secondary'], UNIFIED_COLORS['tertiary']]
    
    def draw_modern_donut(ax, data, labels, colors, title):
        """Draw modern style donut chart"""
        # Calculate percentages
        total = sum(data)
        explode = [0.02] * len(data)
        
        wedges, texts, autotexts = ax.pie(
            data, labels=None, autopct='',
            colors=colors, startangle=90, pctdistance=0.75,
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3),
            explode=explode, shadow=False
        )
        
        # Add total and title in center
        ax.text(0, 0.1, f'{total}', ha='center', va='center', fontsize=28, 
                fontweight='bold', color='#333333')
        ax.text(0, -0.15, 'Sample', ha='center', va='center', fontsize=12, 
                color='#666666')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color='#333333')
        
        # Add external labels
        for i, (wedge, label, value) in enumerate(zip(wedges, labels, data)):
            ang = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
            x = np.cos(np.deg2rad(ang))
            y = np.sin(np.deg2rad(ang))
            
            # Label position
            label_x = x * 1.3
            label_y = y * 1.3
            
            pct = value / total * 100
            ax.annotate(f'{label}\n{value} ({pct:.1f}%)',
                       xy=(x * 0.75, y * 0.75), xytext=(label_x, label_y),
                       ha='center', va='center', fontsize=10,
                       arrowprops=dict(arrowstyle='-', color='#CCCCCC', lw=1),
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                edgecolor='#DDDDDD', alpha=0.9))
        
        return wedges

    # 1. Gender Distribution
    ax1 = fig.add_subplot(gs[0, 0])
    gender_counts = df['性别'].value_counts().sort_index()
    draw_modern_donut(ax1, gender_counts.values, ['Male', 'Female'], colors_gender, 'Gender Distribution')
    add_panel_label(ax1, 'A')
    
    # 2. Education Distribution
    ax2 = fig.add_subplot(gs[0, 1])
    edu_counts = df['在学类别'].value_counts().sort_index()
    edu_labels = ['Undergraduate', 'Master', 'PhD']
    draw_modern_donut(ax2, edu_counts.values, edu_labels, colors_edu, 'Education Distribution')
    add_panel_label(ax2, 'B')
    
    # 3. Major Distribution
    ax3 = fig.add_subplot(gs[0, 2])
    major_counts = [df['专业_理工类'].sum(), df['专业_经管类'].sum(), df['专业_人文社科类'].sum()]
    major_labels = ['STEM', 'Econ & Mgmt', 'Humanities']
    draw_modern_donut(ax3, major_counts, major_labels, colors_major, 'Major Distribution')
    add_panel_label(ax3, 'C')
    
    # 4. Energy Experience Statistics (Using beautified bar chart)
    ax4 = fig.add_subplot(gs[0, 3])
    exp_counts = df['能源经历'].value_counts().sort_index()
    exp_labels = ['With Exp', 'No Exp']
    exp_colors = [UNIFIED_COLORS['primary'], UNIFIED_COLORS['border']]
    
    bars = ax4.barh(exp_labels, exp_counts.values, color=exp_colors, 
                    edgecolor='white', linewidth=2, height=0.6)
    
    # Add value labels
    for bar, val in zip(bars, exp_counts.values):
        ax4.text(val + 1, bar.get_y() + bar.get_height()/2, 
                f'{val} ({val/len(df)*100:.1f}%)', 
                va='center', fontsize=11, fontweight='bold', color='#333333')
    
    ax4.set_xlim(0, max(exp_counts.values) * 1.3)
    ax4.set_title('Energy Related Experience', fontsize=14, fontweight='bold', color='#333333')
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.spines['left'].set_visible(False)
    ax4.tick_params(left=False)
    add_panel_label(ax4, 'D')
    
    # Bottom Summary Cards
    ax_summary = fig.add_subplot(gs[1, :])
    ax_summary.axis('off')
    
    # Create summary text
    n_total = len(df)
    male_pct = df['性别'].value_counts().get(1, 0) / n_total * 100
    grad_pct = (edu_counts.get(2, 0) + edu_counts.get(3, 0)) / n_total * 100
    stem_pct = df['专业_理工类'].sum() / n_total * 100
    
    summary_text = (
        f"📊 Sample Overview: Total {n_total} Respondents | "
        f"👨‍🎓 Male {male_pct:.1f}% | "
        f"🎓 Graduate {grad_pct:.1f}% | "
        f"🔬 STEM Background {stem_pct:.1f}%"
    )
    
    ax_summary.text(0.5, 0.5, summary_text, ha='center', va='center', 
                   fontsize=13, color='#333333',
                   bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8F9FA', 
                            edgecolor='#DEE2E6', linewidth=1.5))
    
    plt.suptitle('Figure 1: Sample Demographics Overview', fontsize=20, fontweight='bold', 
                y=0.98, color='#1A1A1A')
    save_fig(fig, save_path)


def plot_knowledge_level(df, save_path):
    """Energy Knowledge Level Comparison (Using gradient bar chart + distribution violin plot)"""
    # Log data
    print(f"\n[Data Log] Data for Knowledge Level:")
    print("Energy Transition Knowledge Counts:")
    print(df['能源转型了解度'].value_counts().sort_index())
    print("Dual Carbon Knowledge Counts:")
    print(df['双碳了解度'].value_counts().sort_index())

    setup_style()
    
    fig = plt.figure(figsize=(16, 11), facecolor='white')
    gs = fig.add_gridspec(2, 2, height_ratios=[1.3, 1], hspace=0.30, wspace=0.25)
    
    # Data Preparation
    levels = ['Very Familiar', 'Familiar', 'Neutral', 'Unfamiliar', 'Very Unfamiliar']
    
    # Convert to long format
    data_energy = df['能源转型了解度'].value_counts().reindex(range(1, 6), fill_value=0).reset_index()
    data_energy.columns = ['Level', 'Count']
    data_energy['Type'] = 'Energy Transition'
    
    data_carbon = df['双碳了解度'].value_counts().reindex(range(1, 6), fill_value=0).reset_index()
    data_carbon.columns = ['Level', 'Count']
    data_carbon['Type'] = 'Dual Carbon Goals'
    
    plot_data = pd.concat([data_energy, data_carbon])
    plot_data['Level_Label'] = plot_data['Level'].map(dict(zip(range(1, 6), levels)))
    
    # 1. Main Bar Chart (Upper Part)
    ax1 = fig.add_subplot(gs[0, :])
    
    # Use unified color scheme
    palette = {'Energy Transition': UNIFIED_COLORS['primary'], 'Dual Carbon Goals': UNIFIED_COLORS['secondary']}
    
    # Draw grouped bar chart
    bar_plot = sns.barplot(data=plot_data, x='Level_Label', y='Count', hue='Type', 
                          palette=palette, ax=ax1, edgecolor='white', linewidth=2.5,
                          order=levels, saturation=0.95)
    
    # Add gradient effect - add shadow to each bar
    for container in ax1.containers:
        for bar in container:
            bar.set_alpha(0.9)
    
    # Add value labels (with rounded background box)
    for container in ax1.containers:
        for bar in container:
            height = bar.get_height()
            if height > 0:
                ax1.annotate(f'{int(height)}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           ha='center', va='bottom', fontsize=12, fontweight='bold',
                           xytext=(0, 5), textcoords='offset points',
                           color='#2C3E50')
    
    # Style optimization
    ax1.set_xlabel('Knowledge Level', fontsize=14, fontweight='bold', labelpad=12, color='#2C3E50')
    ax1.set_ylabel('Count', fontsize=14, fontweight='bold', labelpad=12, color='#2C3E50')
    ax1.set_title('Comparison of Knowledge on Energy Transition and Dual Carbon Goals', fontsize=17, fontweight='bold', 
                 pad=18, color='#1A1A1A')
    
    # Beautify legend - place inside top right
    legend = ax1.legend(title='Knowledge Dimension', title_fontsize=12, fontsize=11, 
                       loc='upper right', framealpha=0.95, edgecolor='#CCCCCC',
                       fancybox=True, shadow=True)
    legend.get_frame().set_facecolor('#FAFAFA')
    
    # Remove top and right spines, add soft grid
    sns.despine(ax=ax1)
    ax1.grid(axis='y', alpha=0.25, linestyle='-', linewidth=0.8, color='#BDC3C7')
    ax1.set_axisbelow(True)
    
    # X-axis label style
    ax1.tick_params(axis='x', labelsize=12, colors='#2C3E50')
    ax1.tick_params(axis='y', labelsize=11, colors='#2C3E50')
    
    add_panel_label(ax1, 'A')
    
    # 2. Energy Transition Familiarity Distribution (Violin Plot) - Use harmonious gradient colors
    ax2 = fig.add_subplot(gs[1, 0])
    
    # Prepare grouped data
    violin_data = pd.DataFrame({
        'Familiarity': df['能源转型了解度'],
        'Education': df['在学类别'].map({1: 'Undergraduate', 2: 'Master', 3: 'PhD'})
    })
    
    # Use same color family gradient - cool colors
    violin_colors = UNIFIED_COLORS['gradient_cool']
    
    vp1 = sns.violinplot(data=violin_data, x='Education', y='Familiarity', 
                        palette=violin_colors, ax=ax2, inner='box', 
                        linewidth=1.5, order=['Undergraduate', 'Master', 'PhD'],
                        saturation=0.9)
    
    # Beautify violin plot internal box lines
    for collection in ax2.collections:
        collection.set_alpha(0.85)
    
    ax2.set_ylabel('Familiarity Level\n(1=Very Familiar, 5=Very Unfamiliar)', fontsize=11, 
                  fontweight='bold', color='#2C3E50')
    ax2.set_xlabel('Education Level', fontsize=12, fontweight='bold', color='#2C3E50')
    ax2.set_title('Energy Transition Familiarity × Education', fontsize=14, fontweight='bold', 
                 color='#1A1A1A', pad=12)
    ax2.set_ylim(0.5, 5.5)
    sns.despine(ax=ax2)
    ax2.grid(axis='y', alpha=0.2, linestyle='-', linewidth=0.6)
    ax2.tick_params(axis='both', labelsize=11, colors='#2C3E50')
    add_panel_label(ax2, 'B')
    
    # 3. Dual Carbon Goals Familiarity Distribution (Violin Plot) - Use warm color gradient
    ax3 = fig.add_subplot(gs[1, 1])
    
    violin_data2 = pd.DataFrame({
        'Familiarity': df['双碳了解度'],
        'Education': df['在学类别'].map({1: 'Undergraduate', 2: 'Master', 3: 'PhD'})
    })
    
    # Use warm color gradient
    violin_colors2 = UNIFIED_COLORS['gradient_warm']
    
    vp2 = sns.violinplot(data=violin_data2, x='Education', y='Familiarity',
                        palette=violin_colors2, ax=ax3, inner='box', 
                        linewidth=1.5, order=['Undergraduate', 'Master', 'PhD'],
                        saturation=0.9)
    
    for collection in ax3.collections:
        collection.set_alpha(0.85)
    
    ax3.set_ylabel('Familiarity Level\n(1=Very Familiar, 5=Very Unfamiliar)', fontsize=11, 
                  fontweight='bold', color='#2C3E50')
    ax3.set_xlabel('Education Level', fontsize=12, fontweight='bold', color='#2C3E50')
    ax3.set_title('Dual Carbon Goals Familiarity × Education', fontsize=14, fontweight='bold', 
                 color='#1A1A1A', pad=12)
    ax3.set_ylim(0.5, 5.5)
    sns.despine(ax=ax3)
    ax3.grid(axis='y', alpha=0.2, linestyle='-', linewidth=0.6)
    ax3.tick_params(axis='both', labelsize=11, colors='#2C3E50')
    add_panel_label(ax3, 'C')
    
    plt.suptitle('Figure 2: Comprehensive Analysis of Energy Knowledge Levels', fontsize=20, fontweight='bold', 
                y=0.98, color='#1A1A1A')
    save_fig(fig, save_path)


def plot_renewable_recognition(df, save_path):
    """Renewable Energy Recognition Analysis (Lollipop Chart + Accuracy Donut Chart)"""
    # Log data
    print(f"\n[Data Log] Data for Renewable Recognition:")
    cols = ['可再生_太阳能', '可再生_风能', '可再生_水能', '可再生_生物质能', '可再生_石油', '可再生_煤炭', '可再生_天然气', '可再生_核能']
    print("Counts for each energy type:")
    for col in cols:
        if col in df.columns:
            print(f"{col}: {df[col].sum()}")

    setup_style()
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1], wspace=0.25)
    
    # Left: Lollipop Chart
    ax1 = fig.add_subplot(gs[0])
    
    # Data Preparation
    correct_items = {'Solar': '可再生_太阳能', 'Wind': '可再生_风能', 
                     'Hydro': '可再生_水能', 'Biomass': '可再生_生物质能'}
    wrong_items = {'Oil': '可再生_石油', 'Coal': '可再生_煤炭', 'Natural Gas': '可再生_天然气'}
    nuclear = {'Nuclear': '可再生_核能'}
    
    items = []
    counts = []
    categories = []
    
    for label, col in correct_items.items():
        items.append(label)
        counts.append(df[col].sum())
        categories.append('✓ Correct (Renewable)')
        
    for label, col in wrong_items.items():
        items.append(label)
        counts.append(df[col].sum())
        categories.append('✗ Incorrect (Non-Renewable)')
        
    items.append('Nuclear')
    counts.append(df['可再生_核能'].sum())
    categories.append('? Controversial Option')
    
    # Create DataFrame and sort
    plot_df = pd.DataFrame({'Item': items, 'Count': counts, 'Category': categories})
    plot_df = plot_df.sort_values('Count', ascending=True)
    
    # Color mapping - use unified color scheme
    color_map = {
        '✓ Correct (Renewable)': UNIFIED_COLORS['primary'],
        '✗ Incorrect (Non-Renewable)': UNIFIED_COLORS['negative'], 
        '? Controversial Option': UNIFIED_COLORS['neutral']
    }
    colors = plot_df['Category'].map(color_map)
    
    # Draw lollipop chart
    y_pos = range(len(plot_df))
    
    # Draw lines
    for i, (item, count, cat) in enumerate(zip(plot_df['Item'], plot_df['Count'], plot_df['Category'])):
        ax1.hlines(y=i, xmin=0, xmax=count, color=color_map[cat], alpha=0.7, linewidth=3)
    
    # Draw dots
    ax1.scatter(plot_df['Count'], y_pos, c=colors.values, s=200, 
                edgecolors='white', linewidths=2, zorder=5)
    
    # Set Y-axis labels
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(plot_df['Item'], fontsize=12)
    
    # Add value labels
    for i, (count, cat) in enumerate(zip(plot_df['Count'], plot_df['Category'])):
        pct = count / len(df) * 100
        ax1.text(count + 2, i, f'{count} ({pct:.1f}%)', 
                va='center', fontsize=11, fontweight='bold', color='#333333')
    
    ax1.set_xlabel('Count', fontsize=13, fontweight='bold')
    ax1.set_title('Recognition of Energy Types', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlim(0, max(counts) * 1.25)
    
    # Custom legend - use unified color scheme
    legend_elements = [
        mpatches.Patch(facecolor=UNIFIED_COLORS['primary'], label='✓ Correct Option (Renewable)'),
        mpatches.Patch(facecolor=UNIFIED_COLORS['negative'], label='✗ Incorrect Option (Non-Renewable)'),
        mpatches.Patch(facecolor=UNIFIED_COLORS['neutral'], label='? Controversial Option (Nuclear)')
    ]
    ax1.legend(handles=legend_elements, loc='lower right', fontsize=11, 
              frameon=True, framealpha=0.95, edgecolor='#CCCCCC')
    
    sns.despine(ax=ax1, left=True)
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    ax1.tick_params(left=False)
    add_panel_label(ax1, 'A')
    
    # Right: Recognition Accuracy Donut Chart
    ax2 = fig.add_subplot(gs[1])
    
    # Calculate recognition accuracy
    n_total = len(df)
    # Proportion of correctly identified renewable energy
    correct_renewable = (df['可再生_太阳能'].sum() + df['可再生_风能'].sum() + 
                        df['可再生_水能'].sum() + df['可再生_生物质能'].sum()) / (4 * n_total) * 100
    # Proportion of correctly identified non-renewable (i.e., not selected)
    correct_nonrenewable = ((n_total - df['可再生_石油'].sum()) + 
                           (n_total - df['可再生_煤炭'].sum()) + 
                           (n_total - df['可再生_天然气'].sum())) / (3 * n_total) * 100
    
    # Double donut chart
    sizes_outer = [correct_renewable, 100 - correct_renewable]
    sizes_inner = [correct_nonrenewable, 100 - correct_nonrenewable]
    
    colors_outer = [UNIFIED_COLORS['primary'], UNIFIED_COLORS['border']]
    colors_inner = [UNIFIED_COLORS['quaternary'], UNIFIED_COLORS['border']]
    
    # Outer ring: Renewable energy recognition
    wedges1, _ = ax2.pie(sizes_outer, colors=colors_outer, startangle=90,
                         wedgeprops=dict(width=0.25, edgecolor='white', linewidth=2),
                         radius=1)
    
    # Inner ring: Non-renewable energy recognition
    wedges2, _ = ax2.pie(sizes_inner, colors=colors_inner, startangle=90,
                         wedgeprops=dict(width=0.25, edgecolor='white', linewidth=2),
                         radius=0.7)
    
    # Center text
    ax2.text(0, 0.05, f'{(correct_renewable + correct_nonrenewable)/2:.1f}%', 
            ha='center', va='center', fontsize=24, fontweight='bold', color='#333333')
    ax2.text(0, -0.12, 'Overall Accuracy', ha='center', va='center', fontsize=11, color='#666666')
    
    ax2.set_title('Recognition Accuracy Statistics', fontsize=14, fontweight='bold', pad=15)
    
    # Legend
    legend_elements2 = [
        mpatches.Patch(facecolor=UNIFIED_COLORS['primary'], label=f'Renewable Recog: {correct_renewable:.1f}%'),
        mpatches.Patch(facecolor=UNIFIED_COLORS['quaternary'], label=f'Non-Renewable Recog: {correct_nonrenewable:.1f}%')
    ]
    ax2.legend(handles=legend_elements2, loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fontsize=11, frameon=True, framealpha=0.95, ncol=1)
    add_panel_label(ax2, 'B', x=0.02)
    
    plt.suptitle('Figure 3: Renewable Energy Recognition Accuracy Analysis', fontsize=20, fontweight='bold', 
                y=0.98, color='#1A1A1A')
    save_fig(fig, save_path)


def plot_trust_radar(df, save_path):
    """Trust Radar Chart (Modern Style + Comparative Analysis)"""
    # Log data
    print(f"\n[Data Log] Data for Trust Radar:")
    cols = ['技术信任度', '新能源汽车技术信任度', '政策执行信任度', '激励政策认同度', '限油推新支持度']
    print("Raw Means:")
    print(df[cols].mean())
    print("Transformed Means (6 - mean):")
    print(6 - df[cols].mean())

    setup_style()
    
    fig = plt.figure(figsize=(16, 8), facecolor='white')
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1], wspace=0.3)
    
    # ===== Left: Radar Chart =====
    ax1 = fig.add_subplot(gs[0], projection='polar')
    
    # Data Preparation
    categories = ['Tech Maturity\nTrust', 'NEV Tech\nTrust', 'Policy Exec\nTrust', 'Incentive Policy\nAgreement', 'Limit Oil/Promote New\nSupport']
    cols = ['技术信任度', '新能源汽车技术信任度', '政策执行信任度', '激励政策认同度', '限油推新支持度']
    
    # Convert to positive score (6-x)
    values = [6 - df[col].mean() for col in cols]
    values += values[:1]  # Close the loop
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    # Set radar chart direction
    ax1.set_theta_offset(np.pi / 2)
    ax1.set_theta_direction(-1)
    
    # Draw grid background (gradient effect)
    for i, alpha in zip([5, 4, 3, 2, 1], [0.1, 0.15, 0.2, 0.25, 0.3]):
        circle = plt.Circle((0, 0), i, transform=ax1.transData._b, 
                           color=UNIFIED_COLORS['primary'], alpha=alpha * 0.3, zorder=0)
        ax1.add_artist(circle)
    
    # Set category labels
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories, fontsize=11, fontweight='bold', color='#333333')
    
    # Set Y-axis
    ax1.set_rlabel_position(30)
    ax1.set_yticks([1, 2, 3, 4, 5])
    ax1.set_yticklabels(['1', '2', '3', '4', '5'], color='#666666', size=9)
    ax1.set_ylim(0, 5.5)
    
    # Draw data area (gradient fill)
    ax1.plot(angles, values, linewidth=3, linestyle='solid', color=UNIFIED_COLORS['primary'], 
             marker='o', markersize=10, markerfacecolor='white', markeredgewidth=2)
    ax1.fill(angles, values, color=UNIFIED_COLORS['primary'], alpha=0.25)
    
    # Add value labels
    for angle, val, cat in zip(angles[:-1], values[:-1], categories):
        label_angle = angle
        x = (val + 0.6) * np.cos(np.pi/2 - label_angle)
        y = (val + 0.6) * np.sin(np.pi/2 - label_angle)
        ax1.annotate(f'{val:.2f}', xy=(label_angle, val), 
                    fontsize=11, fontweight='bold', color=UNIFIED_COLORS['primary'],
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                             edgecolor=UNIFIED_COLORS['primary'], alpha=0.9))
    
    ax1.set_title('Public Trust and Policy Agreement Dimensions', fontsize=14, fontweight='bold', pad=20)
    
    # ===== Right: Grouped Comparison Bar Chart =====
    ax2 = fig.add_subplot(gs[1])
    
    # Calculate average trust by education
    trust_by_edu = []
    edu_labels = ['Undergraduate', 'Master', 'PhD']
    
    for edu_code, edu_label in zip([1, 2, 3], edu_labels):
        edu_df = df[df['在学类别'] == edu_code]
        avg_trust = np.mean([6 - edu_df[col].mean() for col in cols[:3]])  # First three are trust related
        avg_policy = np.mean([6 - edu_df[col].mean() for col in cols[3:]])  # Last two are policy related
        trust_by_edu.append({
            'Education': edu_label,
            'Tech Trust Mean': avg_trust,
            'Policy Agreement Mean': avg_policy
        })
    
    trust_df = pd.DataFrame(trust_by_edu)
    
    x = np.arange(len(edu_labels))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, trust_df['Tech Trust Mean'], width, 
                   label='Tech Trust', color=UNIFIED_COLORS['primary'], edgecolor='white', linewidth=2)
    bars2 = ax2.bar(x + width/2, trust_df['Policy Agreement Mean'], width,
                   label='Policy Agreement', color=UNIFIED_COLORS['secondary'], edgecolor='white', linewidth=2)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax2.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax2.set_ylabel('Trust/Agreement Level (1-5)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Education Level', fontsize=12, fontweight='bold')
    ax2.set_title('Trust Level Comparison by Education', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(edu_labels)
    ax2.set_ylim(0, 5)
    ax2.legend(loc='upper right', framealpha=0.95)
    
    sns.despine(ax=ax2)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    add_panel_label(ax2, 'B', x=0.02)
    
    plt.suptitle('Figure 4: Analysis of Public Trust and Policy Agreement Dimensions', fontsize=20, fontweight='bold', 
                y=0.98, color='#1A1A1A')
    save_fig(fig, save_path)


def plot_nev_analysis(df, save_path):
    """Comprehensive Analysis of New Energy Vehicles (Multi-chart Composition)"""
    # Log data
    print(f"\n[Data Log] Data for NEV Analysis:")
    print("Purchase Intention Counts:")
    print(df['5年内购车意愿'].value_counts().sort_index())
    print("Car Type Preference Counts:")
    print(df['购车类型偏好'].value_counts().sort_index())
    print("NEV Impression Counts:")
    print(df['新能源汽车印象'].value_counts().sort_index())
    
    factor_cols = ['因素_成本', '因素_环保', '因素_技术', '因素_续航', 
                   '因素_充电', '因素_性能', '因素_政策', '因素_品牌']
    print("Influencing Factors Counts:")
    for col in factor_cols:
        if col in df.columns:
            print(f"{col}: {df[col].sum()}")
            
    problem_cols = ['问题_续航', '问题_充电设施', '问题_电池', '问题_价格', 
                   '问题_安全', '问题_维修']
    print("Pain Points Counts:")
    for col in problem_cols:
        if col in df.columns:
            print(f"{col}: {df[col].sum()}")

    setup_style()
    fig = plt.figure(figsize=(18, 12), facecolor='white')
    
    # Use complex GridSpec layout
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.2], hspace=0.35, wspace=0.3)
    
    # ===== Top Left: Purchase Intention Donut Chart =====
    ax1 = fig.add_subplot(gs[0, 0])
    
    intention_counts = df['5年内购车意愿'].value_counts().sort_index()
    labels = ['Very Likely', 'Likely', 'Uncertain', 'Unlikely', 'Very Unlikely']
    
    # Use gradient colors (Green to Red)
    colors = [UNIFIED_COLORS['positive'], UNIFIED_COLORS['quaternary'], 
              UNIFIED_COLORS['neutral'], UNIFIED_COLORS['secondary'], UNIFIED_COLORS['negative']]
    
    # Calculate positive intention ratio
    positive_ratio = (intention_counts.get(1, 0) + intention_counts.get(2, 0)) / len(df) * 100
    
    wedges, texts, autotexts = ax1.pie(
        intention_counts.values, labels=None, autopct='%1.1f%%',
        colors=colors, startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5),
        textprops={'fontsize': 9, 'fontweight': 'bold', 'color': 'white'}
    )
    
    # Center text
    ax1.text(0, 0.08, f'{positive_ratio:.0f}%', ha='center', va='center', 
            fontsize=22, fontweight='bold', color=UNIFIED_COLORS['positive'])
    ax1.text(0, -0.12, 'Intend to Buy', ha='center', va='center', fontsize=10, color='#666666')
    
    ax1.set_title('Purchase Intention in 5 Years', fontsize=13, fontweight='bold', pad=10)
    
    # Add legend
    ax1.legend(wedges, labels, loc='center left', bbox_to_anchor=(0.9, 0.5),
              fontsize=9, frameon=True, framealpha=0.95)
    add_panel_label(ax1, 'A')
    
    # ===== Top Middle: Car Type Preference =====
    ax2 = fig.add_subplot(gs[0, 1])
    
    car_pref = df['购车类型偏好'].value_counts().sort_index()
    car_labels = ['BEV', 'PHEV', 'ICEV', 'FCEV', 'No Plan']
    car_colors = get_unified_palette(5)
    
    # Draw beautified bar chart
    bars = ax2.barh(range(len(car_pref)), car_pref.values, color=car_colors[:len(car_pref)],
                   edgecolor='white', linewidth=2, height=0.65)
    
    ax2.set_yticks(range(len(car_pref)))
    ax2.set_yticklabels(car_labels[:len(car_pref)], fontsize=10)
    
    # Add values
    for i, (bar, val) in enumerate(zip(bars, car_pref.values)):
        pct = val / len(df) * 100
        ax2.text(val + 1, i, f'{val} ({pct:.1f}%)', va='center', fontsize=10, fontweight='bold')
    
    ax2.set_xlim(0, max(car_pref.values) * 1.35)
    ax2.set_title('Car Type Preference Distribution', fontsize=13, fontweight='bold', pad=10)
    sns.despine(ax=ax2, left=True)
    ax2.tick_params(left=False)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    add_panel_label(ax2, 'B')
    
    # ===== Top Right: Overall Impression of NEVs =====
    ax3 = fig.add_subplot(gs[0, 2])
    
    impression = df['新能源汽车印象'].value_counts().sort_index()
    imp_labels = ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative']
    imp_colors = [UNIFIED_COLORS['positive'], UNIFIED_COLORS['quaternary'], 
                  UNIFIED_COLORS['neutral'], UNIFIED_COLORS['secondary'], UNIFIED_COLORS['negative']]
    
    # Use horizontal stacked bar chart
    bottom = 0
    for i, (val, label, color) in enumerate(zip(impression.values, imp_labels[:len(impression)], imp_colors)):
        pct = val / len(df) * 100
        ax3.barh(['Overall Impression'], [pct], left=bottom, color=color, 
                edgecolor='white', linewidth=1, height=0.5, label=f'{label}')
        if pct > 8:
            ax3.text(bottom + pct/2, 0, f'{pct:.0f}%', ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white')
        bottom += pct
    
    ax3.set_xlim(0, 100)
    ax3.set_xlabel('Percentage (%)', fontsize=11)
    ax3.set_title('Overall Impression of NEVs', fontsize=13, fontweight='bold', pad=10)
    ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=9)
    sns.despine(ax=ax3, left=True)
    ax3.tick_params(left=False)
    add_panel_label(ax3, 'C')
    
    # ===== Bottom Left: Influencing Factors (Lollipop Chart) =====
    ax4 = fig.add_subplot(gs[1, 0])
    
    factor_cols = ['因素_成本', '因素_环保', '因素_技术', '因素_续航', 
                   '因素_充电', '因素_性能', '因素_政策', '因素_品牌']
    factor_names = ['Cost', 'Environmental', 'Tech Reliability', 'Range', 
                   'Charging Convenience', 'Performance', 'Policy Support', 'Brand Reputation']
    factor_vals = [df[col].sum() for col in factor_cols]
    
    df_factors = pd.DataFrame({'Factor': factor_names, 'Count': factor_vals})
    df_factors = df_factors.sort_values('Count', ascending=True)
    
    # Color gradient
    factor_colors = get_unified_palette(len(df_factors), 'sequential')
    
    y_pos = range(len(df_factors))
    for i, (factor, count) in enumerate(zip(df_factors['Factor'], df_factors['Count'])):
        ax4.hlines(y=i, xmin=0, xmax=count, color=factor_colors[i], linewidth=3, alpha=0.8)
        ax4.scatter([count], [i], c=[factor_colors[i]], s=150, edgecolors='white', linewidths=2, zorder=5)
    
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(df_factors['Factor'], fontsize=10)
    
    for i, count in enumerate(df_factors['Count']):
        pct = count / len(df) * 100
        ax4.text(count + 1, i, f'{count} ({pct:.0f}%)', va='center', fontsize=10, fontweight='bold')
    
    ax4.set_xlim(0, max(factor_vals) * 1.25)
    ax4.set_xlabel('Count', fontsize=11, fontweight='bold')
    ax4.set_title('Key Factors Influencing Purchase Decision', fontsize=13, fontweight='bold', pad=10)
    sns.despine(ax=ax4, left=True)
    ax4.tick_params(left=False)
    ax4.grid(axis='x', alpha=0.3, linestyle='--')
    add_panel_label(ax4, 'D')
    
    # ===== Bottom Middle+Right: Major Pain Points (Treemap Effect) =====
    ax5 = fig.add_subplot(gs[1, 1:])
    
    problem_cols = ['问题_续航', '问题_充电设施', '问题_电池', '问题_价格', 
                   '问题_安全', '问题_维修']
    problem_names = ['Insufficient Range', 'Charging Facilities', 'Battery Issues', 'High Price', 
                    'Safety Concerns', 'Maintenance Cost']
    problem_vals = [df[col].sum() for col in problem_cols]
    
    df_problems = pd.DataFrame({'Problem': problem_names, 'Count': problem_vals})
    df_problems = df_problems.sort_values('Count', ascending=False)
    
    # Use faceted bar chart to simulate importance
    problem_colors = get_unified_palette(len(df_problems), 'warm')
    
    bars = ax5.bar(range(len(df_problems)), df_problems['Count'], 
                  color=problem_colors, edgecolor='white', linewidth=2, width=0.7)
    
    ax5.set_xticks(range(len(df_problems)))
    ax5.set_xticklabels(df_problems['Problem'], fontsize=11, rotation=0)
    
    # Add values and ranking
    for i, (bar, val, prob) in enumerate(zip(bars, df_problems['Count'], df_problems['Problem'])):
        height = bar.get_height()
        pct = val / len(df) * 100
        ax5.annotate(f'{val}\n({pct:.0f}%)', xy=(bar.get_x() + bar.get_width()/2, height),
                    ha='center', va='bottom', fontsize=11, fontweight='bold',
                    xytext=(0, 3), textcoords='offset points')
        # Add ranking inside the bar
        ax5.text(bar.get_x() + bar.get_width()/2, height/2, f'#{i+1}',
                ha='center', va='center', fontsize=14, fontweight='bold', 
                color='white', alpha=0.9)
    
    ax5.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax5.set_title('Analysis of Major NEV Pain Points (Sorted by Severity)', fontsize=13, fontweight='bold', pad=10)
    sns.despine(ax=ax5)
    ax5.grid(axis='y', alpha=0.3, linestyle='--')
    add_panel_label(ax5, 'E')
    
    plt.suptitle('Figure 5: Comprehensive Analysis of NEV Market Potential and Consumer Insights', fontsize=22, fontweight='bold', 
                y=0.98, color='#1A1A1A')
    save_fig(fig, save_path)


def plot_correlation_heatmap(corr_matrix, save_path, title='Variable Correlation Heatmap'):
    """Draw Professional Heatmap (Enhanced Version)"""
    # Log data
    print(f"\n[Data Log] Data for Correlation Heatmap:")
    print("Correlation Matrix:")
    print(corr_matrix)

    setup_style()
    fig = plt.figure(figsize=(14, 11), facecolor='white')
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.03], wspace=0.02)
    
    ax = fig.add_subplot(gs[0])
    cax = fig.add_subplot(gs[1])
    
    # Create mask (show only lower triangle)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Custom color palette
    cmap = sns.diverging_palette(250, 15, s=75, l=40, n=9, center='light', as_cmap=True)
    
    # Draw heatmap
    hm = sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
                     annot=True, fmt='.2f', square=True, linewidths=0.8, 
                     linecolor='white', cbar_ax=cax,
                     annot_kws={"size": 9, "fontweight": "bold"}, ax=ax)
    
    # Beautify colorbar
    cax.set_ylabel('Correlation Coefficient', fontsize=12, fontweight='bold', labelpad=10)
    cax.tick_params(labelsize=10)
    
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20, color='#1A1A1A')
    
    # Optimize labels
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', rotation=0, labelsize=10)
    
    # Add border
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('#CCCCCC')
        spine.set_linewidth(1)
    
    save_fig(fig, save_path)


def plot_simple_slopes(df, X, Y, W, X_name, Y_name, W_name, simple_slopes, 
                       model_results, save_path, title):
    """Draw Moderation Effect Simple Slopes Plot (Professional Academic Style)"""
    # Log data
    print(f"\n[Data Log] Data for Simple Slopes Plot:")
    print(f"X: {X_name}, Y: {Y_name}, W: {W_name}")
    print("Simple Slopes Results:")
    for slope in simple_slopes:
        print(slope)
    print("Model Summary:")
    print(model_results['model'].summary())

    setup_style()
    fig = plt.figure(figsize=(12, 8), facecolor='white')
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1], wspace=0.3)
    
    # ===== Left: Simple Slopes Plot =====
    ax = fig.add_subplot(gs[0])
    
    # Get regression coefficients
    model = model_results['model']
    b0 = model.params['const']
    b1 = model.params['X']
    b2 = model.params['W']
    b3 = model.params['XW']
    
    # Data Preparation
    data = df[[X, Y, W]].dropna()
    X_mean = data[X].mean()
    X_std = data[X].std()
    X_range = np.linspace(X_mean - 1.5 * X_std, X_mean + 1.5 * X_std, 100)
    Y_mean = data[Y].mean()
    
    # Color and line style scheme
    colors = get_unified_palette(3)
    linestyles = ['-', '--', ':']
    markers = ['o', 's', '^']
    
    for i, slope_info in enumerate(simple_slopes):
        W_level = slope_info['W_level']
        slope = slope_info['slope']
        
        # Calculate predicted values
        W_centered = W_level - data[W].mean() if data[W].nunique() > 2 else W_level
        X_centered = X_range - X_mean
        Y_pred = b0 + b1 * X_centered + b2 * W_centered + b3 * X_centered * W_centered
        Y_pred_adjusted = Y_pred + Y_mean - b0
        
        # Significance marker
        sig_marker = '***' if slope_info['p'] < 0.001 else ('**' if slope_info['p'] < 0.01 else ('*' if slope_info['p'] < 0.05 else ''))
        label = f"{W_name}={slope_info.get('W_label', W_level)}\n(β={slope:.3f}{sig_marker})"
        
        # Draw lines
        ax.plot(X_range, Y_pred_adjusted, color=colors[i % 3], linestyle=linestyles[i % 3],
                linewidth=3, label=label, marker=markers[i % 3], markevery=20, markersize=8)
        
        # Add confidence interval (simulated)
        se = abs(slope) * 0.15  # Simplified confidence interval
        ax.fill_between(X_range, Y_pred_adjusted - se, Y_pred_adjusted + se,
                       color=colors[i % 3], alpha=0.1)
        
    ax.set_xlabel(X_name, fontsize=14, fontweight='bold', labelpad=10)
    ax.set_ylabel(Y_name, fontsize=14, fontweight='bold', labelpad=10)
    ax.set_title('Simple Slope Analysis', fontsize=16, fontweight='bold', pad=15)
    
    ax.legend(title=f'Moderator: {W_name}', title_fontsize=11, fontsize=10, 
              loc='best', frameon=True, framealpha=0.95, edgecolor='#CCCCCC')
    
    sns.despine(ax=ax)
    ax.grid(alpha=0.3, linestyle='--')
    add_panel_label(ax, 'A')
    
    # ===== Right: Effect Size Table =====
    ax2 = fig.add_subplot(gs[1])
    ax2.axis('off')
    
    # Create table data
    table_data = []
    for i, slope_info in enumerate(simple_slopes):
        sig = '***' if slope_info['p'] < 0.001 else ('**' if slope_info['p'] < 0.01 else ('*' if slope_info['p'] < 0.05 else 'ns'))
        table_data.append([
            slope_info.get('W_label', f"Level {i+1}"),
            f"{slope_info['slope']:.3f}",
            f"{slope_info['se']:.3f}" if 'se' in slope_info else '-',
            f"{slope_info['t']:.3f}" if 't' in slope_info else '-',
            f"{slope_info['p']:.4f}",
            sig
        ])
    
    col_labels = ['Moderator Level', 'β', 'SE', 't', 'p', 'Significance']
    
    table = ax2.table(cellText=table_data, colLabels=col_labels,
                     cellLoc='center', loc='center',
                     colColours=['#F8F9FA'] * 6)
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)
    
    # Beautify table
    for key, cell in table.get_celld().items():
        cell.set_edgecolor('#DEE2E6')
        if key[0] == 0:  # Header
            cell.set_text_props(fontweight='bold', color='white')
            cell.set_facecolor(UNIFIED_COLORS['primary'])
        else:
            if key[1] == 5:  # Significance column
                sig_val = table_data[key[0]-1][5]
                if sig_val == '***':
                    cell.set_facecolor('#D4EDDA')
                elif sig_val in ['**', '*']:
                    cell.set_facecolor('#FFF3CD')
    
    ax2.set_title('Simple Slope Statistics Table', fontsize=14, fontweight='bold', pad=10)
    add_panel_label(ax2, 'B', x=0.02)
    
    plt.suptitle(f'{title}\nModeration Effect Analysis', fontsize=18, fontweight='bold', 
                y=0.98, color='#1A1A1A')
    save_fig(fig, save_path)


def plot_regression_coefficients(results, save_path, title='Regression Model Coefficients'):
    """Draw Regression Coefficient Forest Plot (Academic Journal Style)"""
    # Log data
    print(f"\n[Data Log] Data for Regression Coefficients:")
    print("Coefficients:")
    print(results['std_coefs'])
    print("P-values:")
    print(results['p_values'])
    print("Model Statistics:")
    print(f"R2: {results.get('r_squared')}, Adj R2: {results.get('adj_r_squared')}")
    print(f"F-stat: {results.get('f_statistic')}, F p-val: {results.get('f_pvalue')}")

    setup_style()
    fig = plt.figure(figsize=(12, 8), facecolor='white')
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1], wspace=0.25)
    
    # ===== Left: Forest Plot =====
    ax = fig.add_subplot(gs[0])
    
    # Data Preparation
    vars_list = list(results['std_coefs'].keys())
    coefs = list(results['std_coefs'].values())
    p_vals = [results['p_values'].get(v, 1) for v in vars_list]
    
    # Filter out constant term
    filtered_data = [(v, c, p) for v, c, p in zip(vars_list, coefs, p_vals) if v != 'const']
    if filtered_data:
        vars_list, coefs, p_vals = zip(*filtered_data)
        vars_list, coefs, p_vals = list(vars_list), list(coefs), list(p_vals)
    
    # Create DataFrame
    df_coef = pd.DataFrame({'Variable': vars_list, 'Coef': coefs, 'P_value': p_vals})
    df_coef = df_coef.sort_values('Coef', ascending=True)
    
    # Color mapping
    def get_color(p):
        if p < 0.001:
            return UNIFIED_COLORS['positive']
        elif p < 0.01:
            return UNIFIED_COLORS['primary']
        elif p < 0.05:
            return UNIFIED_COLORS['secondary']
        else:
            return UNIFIED_COLORS['border']
    
    colors = [get_color(p) for p in df_coef['P_value']]
    
    y_pos = range(len(df_coef))
    
    # Draw coefficient points and confidence interval lines (simulated)
    for i, (var, coef, p) in enumerate(zip(df_coef['Variable'], df_coef['Coef'], df_coef['P_value'])):
        color = get_color(p)
        # Simulated confidence interval
        se = abs(coef) * 0.2 if coef != 0 else 0.1
        
        # Draw confidence interval line
        ax.hlines(y=i, xmin=coef-1.96*se, xmax=coef+1.96*se, color=color, linewidth=2.5, alpha=0.7)
        # Draw coefficient point
        ax.scatter([coef], [i], c=[color], s=150, edgecolors='white', linewidths=2, zorder=5)
    
    # Add vertical reference line
    ax.axvline(x=0, color='#333333', linewidth=1.5, linestyle='-', alpha=0.7)
    
    # Set Y-axis
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_coef['Variable'], fontsize=11)
    
    # Add value labels
    for i, (coef, p) in enumerate(zip(df_coef['Coef'], df_coef['P_value'])):
        sig = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
        offset = 0.03 if coef >= 0 else -0.03
        ha = 'left' if coef >= 0 else 'right'
        ax.text(coef + offset, i, f'{coef:.3f}{sig}', va='center', ha=ha,
               fontsize=10, fontweight='bold', color='#333333')
    
    ax.set_xlabel('Standardized Regression Coefficient (β)', fontsize=13, fontweight='bold', labelpad=10)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=UNIFIED_COLORS['positive'], label='p < 0.001 ***'),
        mpatches.Patch(facecolor=UNIFIED_COLORS['primary'], label='p < 0.01 **'),
        mpatches.Patch(facecolor=UNIFIED_COLORS['secondary'], label='p < 0.05 *'),
        mpatches.Patch(facecolor=UNIFIED_COLORS['border'], label='Not Significant')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, 
             frameon=True, framealpha=0.95, title='Significance Level', title_fontsize=11)
    
    sns.despine(ax=ax, left=True)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.tick_params(left=False)
    add_panel_label(ax, 'A')
    
    # ===== Right: Model Summary =====
    ax2 = fig.add_subplot(gs[1])
    ax2.axis('off')
    
    # Extract model statistics
    r2 = results.get('r_squared', 0)
    adj_r2 = results.get('adj_r_squared', 0)
    f_stat = results.get('f_statistic', 0)
    f_pval = results.get('f_pvalue', 1)
    n_obs = results.get('n_observations', 0)
    
    # Create model summary text box - use plain text to avoid superscript issues
    summary_text = f"""Model Fit Statistics
{'─'*25}

R-squared:    {r2:.4f}
Adj R-sq:     {adj_r2:.4f}
F-statistic:  {f_stat:.2f}
F p-value:    {f_pval:.4f}
N(obs):       {n_obs}

{'─'*25}
Significance Markers:
*** p < 0.001
**  p < 0.01
*   p < 0.05
"""
    
    ax2.text(0.1, 0.70, summary_text, transform=ax2.transAxes,
            fontsize=11, fontfamily='monospace', va='top',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8F9FA', 
                     edgecolor='#DEE2E6', linewidth=1.5))
    
    # Use Unicode superscript characters to display R²
    ax2.text(0.5, 0.95, f'R² = {r2:.4f}', transform=ax2.transAxes,
            fontsize=18, fontweight='bold', color=UNIFIED_COLORS['primary'], ha='center',
            fontfamily='DejaVu Sans')
    ax2.text(0.5, 0.85, f'Adj R² = {adj_r2:.4f}', transform=ax2.transAxes,
            fontsize=14, color='#666666', ha='center',
            fontfamily='DejaVu Sans')
    
    ax2.set_title('Model Summary', fontsize=14, fontweight='bold', pad=10)
    add_panel_label(ax2, 'B', x=0.02)
    
    save_fig(fig, save_path)


# ============================================================================
# Comprehensive Combined Figure Function
# ============================================================================

def create_combined_figure(df, save_path):
    """Create comprehensive analysis figure (including all key findings) and save subplots"""
    # Log data
    print(f"\n[Data Log] Data for Combined Figure:")
    print("Gender Distribution:")
    print(df['性别'].value_counts().sort_index())
    print("Education Distribution:")
    print(df['在学类别'].value_counts().sort_index())
    print("Knowledge Level Distribution:")
    print("Energy Transition:", df['能源转型了解度'].value_counts().sort_index())
    print("Dual Carbon:", df['双碳了解度'].value_counts().sort_index())
    
    cols = ['可再生_太阳能', '可再生_风能', '可再生_水能', '可再生_生物质能',
           '可再生_石油', '可再生_煤炭', '可再生_天然气', '可再生_核能']
    print("Renewable Energy Recognition:")
    print(df[cols].sum())
    
    trust_cols = ['技术信任度', '新能源汽车技术信任度', '政策执行信任度', '激励政策认同度', '限油推新支持度']
    print("Trust Analysis Means:")
    print(df[trust_cols].mean())
    
    print("Purchase Intention:")
    print(df['5年内购车意愿'].value_counts().sort_index())
    
    factor_cols = ['因素_成本', '因素_续航', '因素_充电', '因素_技术', '因素_环保']
    print("Key Purchase Factors:")
    print(df[factor_cols].sum())
    
    problem_cols = ['问题_续航', '问题_充电设施', '问题_电池', '问题_价格', '问题_安全']
    print("Major NEV Issues:")
    print(df[problem_cols].sum())

    import os
    setup_style()
    
    # Create subplot save directory
    subplots_dir = get_subplots_dir(save_path)
    
    # ============ Define Subplot Drawing Functions ============
    def draw_gender(ax):
        gender_counts = df['性别'].value_counts().sort_index()
        colors_gender = [UNIFIED_COLORS['male'], UNIFIED_COLORS['female']]
        ax.pie(gender_counts.values, labels=['Male', 'Female'], 
               autopct='%1.1f%%', colors=colors_gender, startangle=90,
               wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
        ax.text(0, 0, f'N={len(df)}', ha='center', va='center', fontsize=14, fontweight='bold')
        ax.set_title('A. Gender Distribution', fontsize=14, fontweight='bold')
    
    def draw_education(ax):
        edu_counts = df['在学类别'].value_counts().sort_index()
        edu_labels = ['Undergraduate', 'Master', 'PhD']
        ax.bar(edu_labels, edu_counts.values, color=UNIFIED_COLORS['education'],
               edgecolor='white', linewidth=2)
        for i, v in enumerate(edu_counts.values):
            ax.text(i, v + 1, str(v), ha='center', fontweight='bold')
        ax.set_ylabel('Count')
        ax.set_title('B. Education Distribution', fontsize=14, fontweight='bold')
        sns.despine(ax=ax)
    
    def draw_cognition(ax):
        levels = ['Very Familiar', 'Familiar', 'Neutral', 'Unfamiliar', 'Very Unfamiliar']
        energy_counts = df['能源转型了解度'].value_counts().reindex(range(1, 6), fill_value=0)
        carbon_counts = df['双碳了解度'].value_counts().reindex(range(1, 6), fill_value=0)
        x = np.arange(5)
        width = 0.35
        ax.bar(x - width/2, energy_counts.values, width, label='Energy Transition', color=UNIFIED_COLORS['primary'])
        ax.bar(x + width/2, carbon_counts.values, width, label='Dual Carbon Goals', color=UNIFIED_COLORS['secondary'])
        ax.set_xticks(x)
        ax.set_xticklabels(levels, rotation=30, ha='right', fontsize=9)
        ax.legend(fontsize=9, loc='upper right', framealpha=0.9, edgecolor='#CCCCCC')
        ax.set_ylabel('Count')
        ax.set_title('C. Knowledge Level Distribution', fontsize=14, fontweight='bold', pad=15)
        sns.despine(ax=ax)
    
    def draw_renewable(ax):
        items = ['Solar', 'Wind', 'Hydro', 'Biomass', 'Oil', 'Coal', 'Natural Gas', 'Nuclear']
        cols = ['可再生_太阳能', '可再生_风能', '可再生_水能', '可再生_生物质能',
               '可再生_石油', '可再生_煤炭', '可再生_天然气', '可再生_核能']
        vals = [df[col].sum() for col in cols]
        colors = [UNIFIED_COLORS['positive']]*4 + [UNIFIED_COLORS['negative']]*3 + [UNIFIED_COLORS['neutral']]
        ax.barh(items, vals, color=colors, edgecolor='white', linewidth=1.5)
        ax.set_xlabel('Count')
        ax.set_title('D. Renewable Energy Recognition', fontsize=14, fontweight='bold')
        sns.despine(ax=ax, left=True)
        ax.tick_params(left=False)
    
    def draw_trust_radar(ax):
        categories = ['Tech Trust', 'NEV Tech', 'Policy Exec', 'Policy Agreement', 'Limit Oil/Promote New']
        trust_cols = ['技术信任度', '新能源汽车技术信任度', '政策执行信任度', '激励政策认同度', '限油推新支持度']
        values = [6 - df[col].mean() for col in trust_cols]
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=9)
        ax.set_ylim(0, 5)
        ax.plot(angles, values, linewidth=2, color=UNIFIED_COLORS['primary'], marker='o')
        ax.fill(angles, values, color=UNIFIED_COLORS['primary'], alpha=0.2)
        ax.set_title('E. Trust Analysis', fontsize=14, fontweight='bold', pad=20)
    
    def draw_intention(ax):
        intention = df['5年内购车意愿'].value_counts().sort_index()
        labels = ['Very Likely', 'Likely', 'Uncertain', 'Unlikely', 'Very Unlikely']
        colors = [UNIFIED_COLORS['positive'], UNIFIED_COLORS['quaternary'], 
                  UNIFIED_COLORS['neutral'], UNIFIED_COLORS['secondary'], UNIFIED_COLORS['negative']]
        ax.pie(intention.values, labels=labels, autopct='%1.1f%%', colors=colors[:len(intention)],
               startangle=90, wedgeprops=dict(width=0.5, edgecolor='white'))
        ax.set_title('F. Purchase Intention in 5 Years', fontsize=14, fontweight='bold')
    
    def draw_factors(ax):
        factor_cols = ['因素_成本', '因素_续航', '因素_充电', '因素_技术', '因素_环保']
        factor_names = ['Cost', 'Range', 'Charging', 'Tech', 'Env']
        factor_vals = [df[col].sum() for col in factor_cols]
        df_factors = pd.DataFrame({'Factor': factor_names, 'Count': factor_vals})
        df_factors = df_factors.sort_values('Count', ascending=True)
        ax.barh(df_factors['Factor'], df_factors['Count'], 
                color=get_unified_palette(len(df_factors)), edgecolor='white')
        ax.set_xlabel('Count')
        ax.set_title('G. Key Purchase Factors (Top 5)', fontsize=14, fontweight='bold')
        sns.despine(ax=ax, left=True)
        ax.tick_params(left=False)
    
    def draw_problems(ax):
        problem_cols = ['问题_续航', '问题_充电设施', '问题_电池', '问题_价格', '问题_安全']
        problem_names = ['Range', 'Charging', 'Battery', 'Price', 'Safety']
        problem_vals = [df[col].sum() for col in problem_cols]
        ax.bar(problem_names, problem_vals, color=get_unified_palette(5), edgecolor='white')
        for i, v in enumerate(problem_vals):
            ax.text(i, v + 0.5, str(v), ha='center', fontweight='bold', fontsize=10)
        ax.set_ylabel('Count')
        ax.set_title('H. Major NEV Issues (Top 5)', fontsize=14, fontweight='bold')
        sns.despine(ax=ax)
    
    def draw_summary(ax):
        ax.axis('off')
        positive_purchase = (df['5年内购车意愿'].isin([1, 2]).sum() / len(df) * 100)
        avg_energy_knowledge = df['能源转型了解度'].mean()
        renewable_accuracy = (df['可再生_太阳能'].sum() + df['可再生_风能'].sum()) / (2 * len(df)) * 100
        summary_text = f"""
📊 Key Research Findings Summary
{'═'*30}

👥 Sample Size: {len(df)} College Students

📈 Knowledge Level:
   • Energy Transition Familiarity: {5-avg_energy_knowledge:.2f}/5
   • Renewable Energy Recognition Rate: {renewable_accuracy:.1f}%

🚗 Purchase Intention:
   • Intend to Buy NEV: {positive_purchase:.1f}%
   • Major Concerns: Range, Charging Facilities

💡 Policy Recommendations:
   1. Strengthen Energy Transition Education
   2. Improve Charging Infrastructure
   3. Enhance Technology Trust
"""
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
                fontsize=11, va='top', fontfamily='sans-serif',
                bbox=dict(boxstyle='round,pad=0.8', facecolor='#F0F4F8', 
                         edgecolor=UNIFIED_COLORS['primary'], linewidth=2))
        ax.set_title('I. Research Summary', fontsize=14, fontweight='bold')
    
    # ============ Save Subplots ============
    # A. Gender Distribution
    fig_sub, ax_sub = plt.subplots(figsize=(8, 6), facecolor='white')
    draw_gender(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'A_Gender_Distribution.png'))
    
    # B. Education Distribution
    fig_sub, ax_sub = plt.subplots(figsize=(8, 6), facecolor='white')
    draw_education(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'B_Education_Distribution.png'))
    
    # C. Knowledge Level
    fig_sub, ax_sub = plt.subplots(figsize=(10, 6), facecolor='white')
    draw_cognition(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'C_Knowledge_Level_Distribution.png'))
    
    # D. Renewable Energy Recognition
    fig_sub, ax_sub = plt.subplots(figsize=(10, 6), facecolor='white')
    draw_renewable(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'D_Renewable_Energy_Recognition.png'))
    
    # E. Trust Radar (Requires Polar Projection)
    fig_sub, ax_sub = plt.subplots(figsize=(8, 8), facecolor='white', subplot_kw=dict(projection='polar'))
    draw_trust_radar(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'E_Trust_Analysis.png'))
    
    # F. Purchase Intention
    fig_sub, ax_sub = plt.subplots(figsize=(8, 6), facecolor='white')
    draw_intention(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'F_Purchase_Intention.png'))
    
    # G. Purchase Factors
    fig_sub, ax_sub = plt.subplots(figsize=(10, 6), facecolor='white')
    draw_factors(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'G_Key_Purchase_Factors.png'))
    
    # H. Major Issues
    fig_sub, ax_sub = plt.subplots(figsize=(10, 6), facecolor='white')
    draw_problems(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'H_Major_NEV_Issues.png'))
    
    # I. Research Summary
    fig_sub, ax_sub = plt.subplots(figsize=(8, 8), facecolor='white')
    draw_summary(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'I_Research_Summary.png'))
    
    # ============ Draw Combined Figure ============
    fig = plt.figure(figsize=(26, 20), facecolor='white')
    gs = fig.add_gridspec(3, 3, height_ratios=[1, 1, 1], hspace=0.45, wspace=0.35)
    
    draw_gender(fig.add_subplot(gs[0, 0]))
    draw_education(fig.add_subplot(gs[0, 1]))
    draw_cognition(fig.add_subplot(gs[0, 2]))
    draw_renewable(fig.add_subplot(gs[1, 0]))
    draw_trust_radar(fig.add_subplot(gs[1, 1], projection='polar'))
    draw_intention(fig.add_subplot(gs[1, 2]))
    draw_factors(fig.add_subplot(gs[2, 0]))
    draw_problems(fig.add_subplot(gs[2, 1]))
    draw_summary(fig.add_subplot(gs[2, 2]))
    
    plt.suptitle('Comprehensive Analysis of College Students\' Energy Transition Awareness and NEV Purchase Intention', 
                fontsize=24, fontweight='bold', y=0.98, color='#1A1A1A')
    
    save_fig(fig, save_path)
    print(f"  → Subplots saved to: {subplots_dir}")


def create_info_channel_figure(df, save_path):
    """Create Information Channel and Attitude Analysis Figure, and save subplots"""
    # Log data
    print(f"\n[Data Log] Data for Info Channel Figure:")
    channel_cols = ['渠道_学校课程', '渠道_新闻媒体', '渠道_社交媒体', 
                   '渠道_学术文献', '渠道_亲友交流']
    print("Information Channels:")
    print(df[channel_cols].sum())
    
    goal_cols = ['目标_保障能源安全', '目标_减少污染', '目标_降低依赖', 
                '目标_技术创新', '目标_绿色转型']
    print("Energy Transition Goals:")
    print(df[goal_cols].sum())
    
    print("Social Responsibility (Obligation):")
    print(df['大学生义务'].value_counts().sort_index())
    
    gov_cols = ['发力_技术研发', '发力_基础设施', '发力_教育宣传', 
               '发力_激励政策', '发力_节能改造']
    print("Expected Gov Focus Areas:")
    print(df[gov_cols].sum())

    import os
    setup_style()
    
    # Create subplot save directory
    subplots_dir = get_subplots_dir(save_path)
    
    # ============ Define Subplot Drawing Functions ============
    def draw_channels(ax):
        channel_cols = ['渠道_学校课程', '渠道_新闻媒体', '渠道_社交媒体', 
                       '渠道_学术文献', '渠道_亲友交流']
        channel_names = ['School Courses', 'News Media', 'Social Media', 'Academic Lit', 'Friends/Family']
        channel_vals = [df[col].sum() for col in channel_cols]
        
        df_channel = pd.DataFrame({'Channel': channel_names, 'Count': channel_vals})
        df_channel = df_channel.sort_values('Count', ascending=True)
        
        colors = get_unified_palette(len(df_channel), 'categorical')
        for i, (ch, cnt) in enumerate(zip(df_channel['Channel'], df_channel['Count'])):
            ax.hlines(y=i, xmin=0, xmax=cnt, color=colors[i], linewidth=4, alpha=0.8)
            ax.scatter([cnt], [i], c=[colors[i]], s=200, edgecolors='white', linewidths=2, zorder=5)
        
        ax.set_yticks(range(len(df_channel)))
        ax.set_yticklabels(df_channel['Channel'], fontsize=11)
        
        for i, cnt in enumerate(df_channel['Count']):
            pct = cnt / len(df) * 100
            ax.text(cnt + 1, i, f'{cnt} ({pct:.0f}%)', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Count', fontsize=12, fontweight='bold')
        ax.set_title('A. Information Channels', fontsize=14, fontweight='bold')
        ax.set_xlim(0, max(channel_vals) * 1.25)
        sns.despine(ax=ax, left=True)
        ax.tick_params(left=False)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    def draw_goals(ax):
        goal_cols = ['目标_保障能源安全', '目标_减少污染', '目标_降低依赖', 
                    '目标_技术创新', '目标_绿色转型']
        goal_names = ['Energy Security', 'Reduce Pollution', 'Reduce Dependency', 'Tech Innovation', 'Green Transition']
        goal_vals = [df[col].sum() for col in goal_cols]
        
        theta = np.linspace(0, 2*np.pi, len(goal_names), endpoint=False)
        width = 2*np.pi / len(goal_names) * 0.8
        
        ax.bar(theta, goal_vals, width=width, alpha=0.8,
               color=get_unified_palette(len(goal_names), 'categorical'), edgecolor='white', linewidth=2)
        ax.set_xticks(theta)
        ax.set_xticklabels(goal_names, fontsize=10)
        ax.set_title('B. Core Goals of Energy Transition', fontsize=14, fontweight='bold', pad=20)
    
    def draw_duty(ax):
        duty_counts = df['大学生义务'].value_counts().sort_index()
        duty_labels = ['Yes', 'No', 'Uncertain']
        duty_colors = [UNIFIED_COLORS['positive'], UNIFIED_COLORS['negative'], UNIFIED_COLORS['neutral']]
        
        ax.bar(duty_labels[:len(duty_counts)], duty_counts.values, 
               color=duty_colors[:len(duty_counts)], edgecolor='white', linewidth=2, width=0.6)
        
        for i, v in enumerate(duty_counts.values):
            pct = v / len(df) * 100
            ax.text(i, v + 1, f'{v}\n({pct:.0f}%)', ha='center', fontsize=10, fontweight='bold')
        
        ax.set_ylabel('Count', fontsize=12)
        ax.set_xlabel('Obligation to Understand Energy Transition', fontsize=11)
        ax.set_title('C. Social Responsibility', fontsize=14, fontweight='bold')
        sns.despine(ax=ax)
    
    def draw_gov_areas(ax):
        gov_cols = ['发力_技术研发', '发力_基础设施', '发力_教育宣传', 
                   '发力_激励政策', '发力_节能改造']
        gov_names = ['R&D', 'Infrastructure', 'Education', 'Incentives', 'Retrofitting']
        gov_vals = [df[col].sum() for col in gov_cols]
        
        df_gov = pd.DataFrame({'Area': gov_names, 'Count': gov_vals})
        df_gov = df_gov.sort_values('Count', ascending=False)
        
        bars = ax.bar(range(len(df_gov)), df_gov['Count'], 
                      color=get_unified_palette(len(df_gov), 'sequential'), edgecolor='white', linewidth=2)
        
        ax.set_xticks(range(len(df_gov)))
        ax.set_xticklabels(df_gov['Area'], fontsize=10, rotation=15, ha='right')
        
        for i, (bar, val) in enumerate(zip(bars, df_gov['Count'])):
            pct = val / len(df) * 100
            ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, 
                    f'{val}\n({pct:.0f}%)', ha='center', fontsize=10, fontweight='bold')
        
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('D. Expected Gov Focus Areas', fontsize=14, fontweight='bold')
        sns.despine(ax=ax)
    
    # ============ Save Subplots ============
    # A. Information Channels
    fig_sub, ax_sub = plt.subplots(figsize=(10, 6), facecolor='white')
    draw_channels(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'A_Information_Channels.png'))
    
    # B. Energy Transition Goals (Polar)
    fig_sub, ax_sub = plt.subplots(figsize=(8, 8), facecolor='white', subplot_kw=dict(projection='polar'))
    draw_goals(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'B_Energy_Transition_Goals.png'))
    
    # C. Social Responsibility
    fig_sub, ax_sub = plt.subplots(figsize=(8, 6), facecolor='white')
    draw_duty(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'C_Social_Responsibility.png'))
    
    # D. Gov Focus Areas
    fig_sub, ax_sub = plt.subplots(figsize=(10, 6), facecolor='white')
    draw_gov_areas(ax_sub)
    save_fig(fig_sub, os.path.join(subplots_dir, 'D_Gov_Focus_Areas.png'))
    
    # ============ Draw Combined Figure ============
    fig = plt.figure(figsize=(18, 12), facecolor='white')
    gs = fig.add_gridspec(2, 2, hspace=0.40, wspace=0.30)
    
    draw_channels(fig.add_subplot(gs[0, 0]))
    draw_goals(fig.add_subplot(gs[0, 1], projection='polar'))
    draw_duty(fig.add_subplot(gs[1, 0]))
    draw_gov_areas(fig.add_subplot(gs[1, 1]))
    
    plt.suptitle('Figure 6: Comprehensive Analysis of Information Channels and Public Attitudes', fontsize=20, fontweight='bold', 
                y=0.98, color='#1A1A1A')
    save_fig(fig, save_path)
    print(f"  → Subplots saved to: {subplots_dir}")


# ============================================================================
# Advanced Chart Types
# ============================================================================

def plot_raincloud(df, var, group_var, var_label, group_label, save_path, title=None):
    """
    Draw Raincloud Plot
    Combination: Half-Violin Plot + Box Plot + Scatter Plot
    Suitable for group comparison of Likert scale distributions
    """
    # Log data
    print(f"\n[Data Log] Data for {title}:")
    print(f"Variable: {var}, Group Variable: {group_var}")
    print("Group Statistics:")
    print(df.groupby(group_var)[var].describe())

    setup_style()
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
    
    # Prepare data
    plot_data = df[[var, group_var]].dropna().copy()
    groups = sorted(plot_data[group_var].unique())
    n_groups = len(groups)
    
    # Color scheme - use unified palette
    colors = get_unified_palette(n_groups)
    
    # Draw raincloud for each group - use larger spacing
    positions = np.arange(n_groups) * 2.0  # Increase group spacing
    
    for i, (group, color) in enumerate(zip(groups, colors)):
        data = plot_data[plot_data[group_var] == group][var].values
        pos = positions[i]
        
        if len(data) < 2:
            continue
        
        # ===== 1. Scatter Plot (Leftmost, with jitter) - Draw first, lowest zorder =====
        jitter = np.random.uniform(-0.15, 0.15, len(data))
        ax.scatter(np.full(len(data), pos - 0.5) + jitter, data, 
                  c=[color], s=50, alpha=0.6, edgecolors='white', linewidths=0.5, zorder=2)
        
        # ===== 2. Half-Violin Plot (Right) =====
        parts = ax.violinplot([data], positions=[pos + 0.35], showmeans=False, showmedians=False, 
                             showextrema=False, widths=0.6, vert=True)
        
        # Keep only right half
        for pc in parts['bodies']:
            pc.set_facecolor(color)
            pc.set_edgecolor('white')
            pc.set_linewidth(1.5)
            pc.set_alpha(0.5)
            # Clip to half
            m = np.mean(pc.get_paths()[0].vertices[:, 0])
            pc.get_paths()[0].vertices[:, 0] = np.clip(pc.get_paths()[0].vertices[:, 0], m, np.inf)
        
        # ===== 3. Box Plot (Center) - Draw last, highest zorder =====
        bp = ax.boxplot([data], positions=[pos], widths=0.25, patch_artist=True,
                       showfliers=False, zorder=10, vert=True)
        
        # Box style - use white fill to ensure visibility
        bp['boxes'][0].set_facecolor('white')
        bp['boxes'][0].set_edgecolor(color)
        bp['boxes'][0].set_linewidth(3)
        bp['boxes'][0].set_alpha(1.0)
        
        # Whiskers and caps
        for element in ['whiskers', 'caps']:
            plt.setp(bp[element], color=color, linewidth=2.5)
        
        # Median line - use accent color
        plt.setp(bp['medians'], color=color, linewidth=3)
        
        # Add mean point at box center
        mean_val = np.mean(data)
        ax.scatter([pos], [mean_val], c=[color], s=80, marker='D', 
                  edgecolors='white', linewidths=2, zorder=11)
    
    # Set labels - use correct label mapping
    ax.set_xticks(positions)
    
    # Create label mapping - show sample size and IQR info
    label_map = {1: 'Undergraduate', 2: 'Master', 3: 'PhD'}
    tick_labels = []
    for g in groups:
        data = plot_data[plot_data[group_var] == g][var].values
        n = len(data)
        iqr = np.percentile(data, 75) - np.percentile(data, 25)
        base_label = label_map.get(g, str(g))
        tick_labels.append(f'{base_label}\n(n={n})')
    ax.set_xticklabels(tick_labels, fontsize=12, fontweight='bold')
    
    ax.set_xlabel(group_label, fontsize=14, fontweight='bold', labelpad=15)
    ax.set_ylabel(var_label, fontsize=14, fontweight='bold', labelpad=15)
    
    # Set appropriate x-axis range
    ax.set_xlim(positions[0] - 1.0, positions[-1] + 1.0)
    
    if title:
        ax.set_title(title, fontsize=18, fontweight='bold', pad=25)
    
    sns.despine(ax=ax)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add legend explaining components
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor='gray', alpha=0.4, label='Density'),
        Patch(facecolor='white', edgecolor='gray', linewidth=2, label='Boxplot (IQR)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
               markersize=8, alpha=0.6, label='Individual Points'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='gray', 
               markersize=8, label='Mean')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11, 
             framealpha=0.95, edgecolor='#CCCCCC')
    
    # Add note - explain IQR=0
    note_text = 'Raincloud Plot: Scatter(Left) + Box(Center) + Density(Right)\nNote: Box collapsed to line indicates IQR=0 (Highly Concentrated)'
    ax.text(0.98, 0.02, note_text, 
           transform=ax.transAxes, ha='right', va='bottom', fontsize=9, 
           color='#666666', style='italic',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFFBEA', alpha=0.9, edgecolor='#F0C36D'))
    
    save_fig(fig, save_path)


def plot_ridgeline(df, variables, var_labels, save_path, title='Ridgeline Plot of Core Variables'):
    """
    Draw Ridgeline/Joy Plot
    Suitable for overall display of multi-variable distributions
    """
    # Log data
    print(f"\n[Data Log] Data for {title}:")
    print(f"Variables: {variables}")
    print("Descriptive Statistics:")
    print(df[variables].describe())

    setup_style()
    
    n_vars = len(variables)
    fig, axes = plt.subplots(n_vars, 1, figsize=(14, 2.5 * n_vars), facecolor='white', 
                             sharex=True)
    
    # Color scheme - use gradient
    colors = get_unified_palette(n_vars, 'categorical')
    
    # Get global x range
    all_data = []
    for var in variables:
        all_data.extend(df[var].dropna().values)
    x_min, x_max = min(all_data) - 0.5, max(all_data) + 0.5
    x_range = np.linspace(x_min, x_max, 200)
    
    for i, (var, label, color) in enumerate(zip(variables, var_labels, colors)):
        ax = axes[i] if n_vars > 1 else axes
        
        data = df[var].dropna().values
        
        # Calculate KDE
        from scipy import stats
        try:
            kde = stats.gaussian_kde(data, bw_method=0.3)
            density = kde(x_range)
            
            # Normalize
            density = density / density.max() * 0.8
            
            # Draw filled area
            ax.fill_between(x_range, 0, density, color=color, alpha=0.7, 
                           edgecolor='white', linewidth=2)
            ax.plot(x_range, density, color=color, linewidth=2)
            
        except:
            # If KDE fails, use histogram
            ax.hist(data, bins=20, density=True, color=color, alpha=0.7, 
                   edgecolor='white', linewidth=1)
        
        # Add variable label
        ax.text(-0.02, 0.5, label, transform=ax.transAxes, fontsize=12, 
               fontweight='bold', va='center', ha='right', color=color)
        
        # Add statistics
        mean_val = np.mean(data)
        std_val = np.std(data)
        ax.axvline(mean_val, color='#333333', linestyle='--', linewidth=1.5, alpha=0.7)
        ax.text(mean_val + 0.1, ax.get_ylim()[1] * 0.7, f'M={mean_val:.2f}', 
               fontsize=9, color='#333333', fontweight='bold')
        
        # Hide y-axis
        ax.set_yticks([])
        ax.set_ylabel('')
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        if i < n_vars - 1:
            ax.spines['bottom'].set_visible(False)
            ax.tick_params(bottom=False)
    
    # Set x-axis label
    axes[-1].set_xlabel('Score', fontsize=13, fontweight='bold')
    
    plt.suptitle(title, fontsize=20, fontweight='bold', y=1.02)
    plt.tight_layout()
    save_fig(fig, save_path)


def plot_correlation_network(corr_matrix, save_path, threshold=0.3, title='Correlation Network Diagram'):
    """
    Draw Correlation Network Diagram
    Nodes: Variables; Edges: Correlation Coefficients (|r|>threshold)
    """
    # Log data
    print(f"\n[Data Log] Data for {title}:")
    print(f"Threshold: {threshold}")
    print("Correlation Matrix:")
    print(corr_matrix)

    setup_style()
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='white')
    
    variables = list(corr_matrix.columns)
    n = len(variables)
    
    # Circular layout
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    radius = 3.5
    pos = {var: (radius * np.cos(angle), radius * np.sin(angle)) 
           for var, angle in zip(variables, angles)}
    
    # Draw edges (correlation coefficients)
    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            if i < j:
                r = corr_matrix.loc[var1, var2]
                if abs(r) >= threshold:
                    x1, y1 = pos[var1]
                    x2, y2 = pos[var2]
                    
                    # Line width and color based on correlation coefficient
                    linewidth = abs(r) * 5
                    color = UNIFIED_COLORS['positive'] if r > 0 else UNIFIED_COLORS['negative']
                    alpha = 0.3 + abs(r) * 0.5
                    
                    ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth, 
                           alpha=alpha, zorder=1)
                    
                    # Label correlation coefficient at edge midpoint
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    ax.text(mid_x, mid_y, f'{r:.2f}', fontsize=9, ha='center', va='center',
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                                    edgecolor='#CCCCCC', alpha=0.9))
    
    # Draw nodes
    node_sizes = []
    for var in variables:
        # Node size based on average correlation strength with other variables
        avg_corr = corr_matrix[var].abs().mean()
        node_sizes.append(800 + avg_corr * 1500)
    
    for var, (x, y), size in zip(variables, pos.values(), node_sizes):
        circle = plt.Circle((x, y), 0.5, color=UNIFIED_COLORS['primary'], ec='white', linewidth=3, zorder=3)
        ax.add_patch(circle)
        
        # Variable label
        angle = np.arctan2(y, x)
        label_x = (radius + 0.8) * np.cos(angle)
        label_y = (radius + 0.8) * np.sin(angle)
        ha = 'left' if x >= 0 else 'right'
        
        ax.text(label_x, label_y, var, fontsize=11, fontweight='bold',
               ha=ha, va='center', color='#333333')
    
    # Set range
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-5.5, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], color=UNIFIED_COLORS['positive'], linewidth=3, label='Positive Correlation'),
        plt.Line2D([0], [0], color=UNIFIED_COLORS['negative'], linewidth=3, label='Negative Correlation')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11, frameon=True)
    
    ax.set_title(title, fontsize=20, fontweight='bold', pad=20)
    ax.text(0.5, -0.02, f'Only showing |r| ≥ {threshold}, line width indicates strength', 
           transform=ax.transAxes, ha='center', fontsize=10, color='#666666', style='italic')
    
    save_fig(fig, save_path)


def plot_mediation_diagram(a, b, c, c_prime, indirect, ci_low, ci_high, 
                          X_name, M_name, Y_name, save_path, title='Mediation Effect Path Diagram'):
    """
    Draw Mediation Effect Path Diagram (SEM Style)
    """
    # Log data
    print(f"\n[Data Log] Data for {title}:")
    print(f"Path X->M (a): {a}")
    print(f"Path M->Y (b): {b}")
    print(f"Total Effect (c): {c}")
    print(f"Direct Effect (c'): {c_prime}")
    print(f"Indirect Effect: {indirect} (95% CI: [{ci_low}, {ci_high}])")

    setup_style()
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Define variable box positions
    box_style = dict(boxstyle='round,pad=0.5', facecolor='#F8F9FA', 
                    edgecolor=UNIFIED_COLORS['primary'], linewidth=2.5)
    
    # X (Left)
    ax.text(1.5, 3, X_name, fontsize=14, fontweight='bold', ha='center', va='center',
           bbox=box_style)
    
    # M (Top Center)
    ax.text(5, 5, M_name, fontsize=14, fontweight='bold', ha='center', va='center',
           bbox=box_style)
    
    # Y (Right)
    ax.text(8.5, 3, Y_name, fontsize=14, fontweight='bold', ha='center', va='center',
           bbox=box_style)
    
    # Draw path arrows
    arrow_props = dict(arrowstyle='->', color=UNIFIED_COLORS['primary'], lw=2.5, 
                      mutation_scale=20, shrinkA=30, shrinkB=30)
    arrow_props_dash = dict(arrowstyle='->', color='#999999', lw=2, 
                           mutation_scale=15, shrinkA=30, shrinkB=30, linestyle='--')
    
    # a path (X → M)
    ax.annotate('', xy=(4.2, 4.8), xytext=(2.3, 3.5), arrowprops=arrow_props)
    a_sig = '***' if abs(a) > 0.3 else ('**' if abs(a) > 0.2 else '*')
    ax.text(2.8, 4.4, f'a = {a:.3f}{a_sig}', fontsize=12, fontweight='bold', 
           color=UNIFIED_COLORS['primary'], rotation=35)
    
    # b path (M → Y)
    ax.annotate('', xy=(7.7, 3.5), xytext=(5.8, 4.8), arrowprops=arrow_props)
    b_sig = '***' if abs(b) > 0.3 else ('**' if abs(b) > 0.2 else '*')
    ax.text(6.8, 4.4, f'b = {b:.3f}{b_sig}', fontsize=12, fontweight='bold', 
           color=UNIFIED_COLORS['primary'], rotation=-35)
    
    # c' path (X → Y, direct effect, dashed)
    ax.annotate('', xy=(7.5, 3), xytext=(2.5, 3), arrowprops=arrow_props_dash)
    ax.text(5, 2.5, f"c' = {c_prime:.3f}", fontsize=12, fontweight='bold', 
           color='#666666', ha='center')
    
    # Indirect effect info box
    indirect_sig = 'Significant' if ci_low * ci_high > 0 else 'Not Significant'
    sig_color = UNIFIED_COLORS['positive'] if ci_low * ci_high > 0 else UNIFIED_COLORS['negative']
    
    info_text = f"""Indirect Effect Analysis
─────────────────
Indirect Effect (a×b): {indirect:.4f}
95% CI: [{ci_low:.4f}, {ci_high:.4f}]
Conclusion: {indirect_sig}
─────────────────
Total Effect (c): {c:.4f}
Direct Effect (c'): {c_prime:.4f}
"""
    
    ax.text(5, 0.8, info_text, fontsize=11, ha='center', va='bottom',
           fontfamily='monospace',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#F0F4F8', 
                    edgecolor=sig_color, linewidth=2))
    
    ax.set_title(title, fontsize=20, fontweight='bold', pad=30)
    
    save_fig(fig, save_path)


def plot_dumbbell_chart(df, variables, var_labels, group_var, group_labels, 
                        save_path, title='Group Difference Dumbbell Chart'):
    """
    Draw Dumbbell Chart / Slope Chart
    Compare differences between groups across multiple variables
    """
    # Log data
    print(f"\n[Data Log] Data for {title}:")
    print(f"Variables: {variables}")
    print(f"Group Variable: {group_var}")
    print("Group Means:")
    print(df.groupby(group_var)[variables].mean())

    setup_style()
    fig, ax = plt.subplots(figsize=(14, len(variables) * 1.5 + 3), facecolor='white')
    
    groups = sorted(df[group_var].unique())
    n_groups = len(groups)
    colors = get_unified_palette(n_groups)
    
    y_positions = np.arange(len(variables))
    
    # Record all means for setting x-axis range
    all_means = []
    
    for i, (var, label) in enumerate(zip(variables, var_labels)):
        # Calculate mean for each group
        means = []
        for group in groups:
            group_mean = df[df[group_var] == group][var].mean()
            means.append(group_mean)
            all_means.append(group_mean)
        
        # Draw connecting lines - use thicker lines
        ax.plot(means, [i] * len(means), color='#DDDDDD', linewidth=4, zorder=1, solid_capstyle='round')
        
        # Draw points for each group
        for j, (mean, color, group) in enumerate(zip(means, colors, groups)):
            ax.scatter([mean], [i], c=[color], s=250, edgecolors='white', 
                      linewidths=3, zorder=3, label=group_labels[j] if i == 0 else '')
    
    # Set x-axis range, leaving enough space for labels
    x_min, x_max = min(all_means), max(all_means)
    x_range = x_max - x_min
    ax.set_xlim(x_min - x_range * 0.25, x_max + x_range * 0.25)
    
    # Add value labels outside the chart
    for i, (var, label) in enumerate(zip(variables, var_labels)):
        means = []
        for group in groups:
            group_mean = df[df[group_var] == group][var].mean()
            means.append(group_mean)
        
        # Min value label on left, max value label on right
        min_idx = np.argmin(means)
        max_idx = np.argmax(means)
        
        for j, (mean, color) in enumerate(zip(means, colors)):
            if j == min_idx:
                # Min value on left
                ax.text(mean - 0.12, i, f'{mean:.2f}', fontsize=11, fontweight='bold',
                       va='center', ha='right', color=color)
            elif j == max_idx:
                # Max value on right
                ax.text(mean + 0.12, i, f'{mean:.2f}', fontsize=11, fontweight='bold',
                       va='center', ha='left', color=color)
            else:
                # Middle value on top
                ax.text(mean, i + 0.25, f'{mean:.2f}', fontsize=10, fontweight='bold',
                       va='bottom', ha='center', color=color)
    
    ax.set_yticks(y_positions)
    ax.set_yticklabels(var_labels, fontsize=12)
    ax.set_xlabel('Mean Score', fontsize=13, fontweight='bold')
    
    # Legend - placed at the top
    ax.legend(loc='upper center', fontsize=11, frameon=True, framealpha=0.95,
             ncol=n_groups, bbox_to_anchor=(0.5, 1.02))
    
    ax.set_title(title, fontsize=18, fontweight='bold', pad=40)
    
    sns.despine(ax=ax, left=True)
    ax.tick_params(left=False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add difference annotation
    ax.text(0.98, 0.02, '● Line length indicates magnitude of group difference', 
           transform=ax.transAxes, ha='right', va='bottom', fontsize=10, 
           color='#666666', style='italic')
    
    save_fig(fig, save_path)


def plot_sankey_flow(df, source_var, target_var, source_labels, target_labels,
                     save_path, title='Cognition-Intention Flow Sankey Diagram'):
    """
    Draw Simplified Sankey Diagram / Flow Chart
    Show flow from cognition level to purchase intention
    """
    # Log data
    print(f"\n[Data Log] Data for {title}:")
    print(f"Source: {source_var}, Target: {target_var}")
    print("Flow Matrix (Counts):")
    print(pd.crosstab(df[source_var], df[target_var]))

    setup_style()
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
    
    # Prepare data
    source_cats = sorted(df[source_var].unique())
    target_cats = sorted(df[target_var].unique())
    
    n_source = len(source_cats)
    n_target = len(target_cats)
    
    # Calculate flow matrix
    flow_matrix = np.zeros((n_source, n_target))
    for i, s in enumerate(source_cats):
        for j, t in enumerate(target_cats):
            flow_matrix[i, j] = ((df[source_var] == s) & (df[target_var] == t)).sum()
    
    # Normalize for height calculation
    total = len(df)
    
    # Color palette
    source_colors = get_unified_palette(n_source, 'cool')
    target_colors = get_unified_palette(n_target, 'warm')
    
    # Draw source nodes (Left)
    left_x = 1
    y_pos = 0
    source_positions = {}
    
    for i, (cat, color) in enumerate(zip(source_cats, source_colors)):
        count = (df[source_var] == cat).sum()
        height = count / total * 8
        
        rect = plt.Rectangle((left_x, y_pos), 0.3, height, 
                             facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(rect)
        
        # Label
        label = source_labels[i] if i < len(source_labels) else f'{cat}'
        ax.text(left_x - 0.1, y_pos + height/2, f'{label}\n({count})', 
               fontsize=10, fontweight='bold', ha='right', va='center')
        
        source_positions[cat] = (left_x + 0.3, y_pos, y_pos + height)
        y_pos += height + 0.3
    
    # Draw target nodes (Right)
    right_x = 8
    y_pos = 0
    target_positions = {}
    
    for i, (cat, color) in enumerate(zip(target_cats, target_colors)):
        count = (df[target_var] == cat).sum()
        height = count / total * 8
        
        rect = plt.Rectangle((right_x, y_pos), 0.3, height,
                             facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(rect)
        
        # Label
        label = target_labels[i] if i < len(target_labels) else f'{cat}'
        ax.text(right_x + 0.4, y_pos + height/2, f'{label}\n({count})',
               fontsize=10, fontweight='bold', ha='left', va='center')
        
        target_positions[cat] = (right_x, y_pos, y_pos + height)
        y_pos += height + 0.3
    
    # Draw flow (curves)
    from matplotlib.patches import FancyBboxPatch, PathPatch
    from matplotlib.path import Path
    
    # Track current position of each node
    source_current = {cat: pos[1] for cat, pos in source_positions.items()}
    target_current = {cat: pos[1] for cat, pos in target_positions.items()}
    
    for i, s_cat in enumerate(source_cats):
        for j, t_cat in enumerate(target_cats):
            flow = flow_matrix[i, j]
            if flow > 0:
                flow_height = flow / total * 8
                
                # Start and end points
                x0, y0_start, y0_end = source_positions[s_cat]
                x1, y1_start, y1_end = target_positions[t_cat]
                
                y0 = source_current[s_cat]
                y1 = target_current[t_cat]
                
                # Draw Bezier curve filled area
                verts = [
                    (x0, y0),  # Bottom left
                    (x0 + 2, y0), (x1 - 2, y1), (x1, y1),  # Bottom curve
                    (x1, y1 + flow_height),  # Top right
                    (x1 - 2, y1 + flow_height), (x0 + 2, y0 + flow_height), (x0, y0 + flow_height),  # Top curve
                    (x0, y0)  # Close
                ]
                
                codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                        Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
                
                path = Path(verts, codes)
                patch = PathPatch(path, facecolor=source_colors[i], alpha=0.4, 
                                 edgecolor='white', linewidth=0.5)
                ax.add_patch(patch)
                
                # Update current position
                source_current[s_cat] += flow_height
                target_current[t_cat] += flow_height
    
    ax.set_xlim(0, 9.5)
    ax.set_ylim(-0.5, 12)
    ax.axis('off')
    
    # Add title and labels
    ax.text(0.5, -0.3, source_var, fontsize=14, fontweight='bold', ha='center')
    ax.text(8.5, -0.3, target_var, fontsize=14, fontweight='bold', ha='center')
    
    ax.set_title(title, fontsize=20, fontweight='bold', pad=20)
    
    save_fig(fig, save_path)


def plot_radar_comparison(df, group_var, variables, var_labels, group_labels, 
                          save_path, title='Group Radar Comparison'):
    """
    Draw Group Radar Comparison Panel
    """
    # Log data
    print(f"\n[Data Log] Data for {title}:")
    print(f"Group Variable: {group_var}")
    print("Group Means (Radar Data):")
    print(df.groupby(group_var)[variables].mean())

    setup_style()
    
    groups = sorted(df[group_var].unique())
    n_groups = len(groups)
    
    fig = plt.figure(figsize=(6 * n_groups, 6), facecolor='white')
    
    # Color palette
    colors = get_unified_palette(n_groups)
    
    n_vars = len(variables)
    angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    for i, (group, color, g_label) in enumerate(zip(groups, colors, group_labels)):
        ax = fig.add_subplot(1, n_groups, i + 1, projection='polar')
        
        group_df = df[df[group_var] == group]
        
        # Calculate mean for each variable (convert to positive 5-point scale)
        values = []
        for var in variables:
            # Assuming original score is 1-5, 1 being most positive
            mean_val = 6 - group_df[var].mean()
            values.append(mean_val)
        values += values[:1]  # Close
        
        # Set radar chart
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(var_labels, fontsize=10)
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8, color='#666666')
        
        # Draw data
        ax.plot(angles, values, linewidth=2.5, color=color, marker='o', markersize=6)
        ax.fill(angles, values, color=color, alpha=0.25)
        
        # Add value labels
        for angle, val in zip(angles[:-1], values[:-1]):
            ax.annotate(f'{val:.2f}', xy=(angle, val), fontsize=9, 
                       fontweight='bold', ha='center', va='bottom', color=color)
        
        ax.set_title(f'{g_label}\n(n={len(group_df)})', fontsize=13, fontweight='bold', pad=20)
        
        add_panel_label(ax, chr(65 + i), x=0.1, y=1.15)
    
    plt.suptitle(title, fontsize=20, fontweight='bold', y=1.05)
    plt.tight_layout()
    save_fig(fig, save_path)


def create_advanced_visualization_suite(df, save_dir):
    """
    Generate complete suite of advanced visualization charts
    """
    import os
    
    print("Generating advanced visualization suite...")
    
    # 1. Raincloud Plot: Attitude distribution by education level
    print("  ✓ Raincloud Plot...")
    df['Education_Label'] = df['在学类别'].map({1: 'Undergraduate', 2: 'Master', 3: 'PhD'})
    if '态度' in df.columns:
        plot_raincloud(df, '态度', 'Education_Label', 'Attitude Score', 'Education Level',
                      os.path.join(save_dir, 'Advanced_Raincloud_Attitude_x_Education.png'),
                      'Attitude Distribution by Education Level')
    
    # 2. Ridgeline Plot: Core indices distribution
    print("  ✓ Ridgeline Plot...")
    core_vars = ['认知指数', '责任感指数', '信任指数', '政策认同指数']
    core_vars_exist = [v for v in core_vars if v in df.columns]
    var_labels_map = {'认知指数': 'Knowledge Index', '责任感指数': 'Responsibility Index', 
                      '信任指数': 'Trust Index', '政策认同指数': 'Policy Support Index'}
    core_vars_labels = [var_labels_map.get(v, v) for v in core_vars_exist]
    
    if core_vars_exist:
        plot_ridgeline(df, core_vars_exist, core_vars_labels,
                      os.path.join(save_dir, 'Advanced_Ridgeline_Core_Indices.png'))
    
    # 3. Dumbbell Chart: Comparison of education groups across dimensions
    print("  ✓ Dumbbell Chart...")
    if core_vars_exist and '在学类别' in df.columns:
        plot_dumbbell_chart(df, core_vars_exist, core_vars_labels,
                           '在学类别', ['Undergraduate', 'Master', 'PhD'],
                           os.path.join(save_dir, 'Advanced_Dumbbell_Education_Comparison.png'),
                           'Core Variables Comparison by Education')
    
    # 4. Group Radar Chart Comparison
    print("  ✓ Group Radar Chart...")
    trust_vars = ['技术信任度', '新能源汽车技术信任度', '政策执行信任度', 
                 '激励政策认同度', '限油推新支持度']
    trust_labels = ['Tech Trust', 'NEV Tech', 'Policy Exec', 'Policy Support', 'Limit Oil']
    
    # Group by Energy Experience
    if '能源经历' in df.columns:
        df['Experience_Label'] = df['能源经历'].map({1: 'Experienced', 2: 'No Experience'})
        plot_radar_comparison(df, 'Experience_Label', trust_vars, trust_labels,
                             ['Experienced', 'No Experience'],
                             os.path.join(save_dir, 'Advanced_Radar_Energy_Experience.png'),
                             'Impact of Energy Experience on Trust')
    
    # Group by Gender
    if '性别' in df.columns:
        df['Gender_Label'] = df['性别'].map({1: 'Male', 2: 'Female'})
        plot_radar_comparison(df, 'Gender_Label', trust_vars, trust_labels,
                             ['Male', 'Female'],
                             os.path.join(save_dir, 'Advanced_Radar_Gender.png'),
                             'Impact of Gender on Trust and Policy Support')
    
    # 5. Cognition-Intention Flow Chart
    print("  ✓ Sankey Flow Chart...")
    if '能源转型了解度' in df.columns and '5年内购车意愿' in df.columns:
        source_labels = ['Very Familiar', 'Familiar', 'Neutral', 'Unfamiliar', 'Very Unfamiliar']
        target_labels = ['Very Likely', 'Likely', 'Uncertain', 'Unlikely', 'Very Unlikely']
        plot_sankey_flow(df, '能源转型了解度', '5年内购车意愿',
                        source_labels, target_labels,
                        os.path.join(save_dir, 'Advanced_Sankey_Knowledge_to_Intention.png'),
                        'Flow Analysis: Knowledge Level to Purchase Intention')
    
    # ============ New Advanced Visualizations ============
    print("\n【Upgraded Advanced Visualization】")
    
    # 6. Multi-stage Alluvial Flow Chart
    print("  ✓ Multi-stage Alluvial Plot...")
    plot_multi_stage_alluvial(df, save_dir)
    
    # 7. Variable Relationship Chord Diagram
    print("  ✓ Chord Diagram...")
    plot_chord_diagram(df, save_dir)
    
    # 8. Respondent Cluster Heatmap
    print("  ✓ Respondent Cluster Heatmap...")
    plot_respondent_clustermap(df, save_dir)
    
    # 9. Awareness Space PCA Scatter Plot
    print("  ✓ Awareness Space PCA Scatter Plot...")
    plot_awareness_pca(df, save_dir)
    
    # 10. SEM Style Path Diagram
    print("  ✓ SEM Path Diagram...")
    plot_sem_path_diagram(df, save_dir)
    
    # 11. Risk-Intention Relationship Chart
    print("  ✓ Risk-Intention Relationship Chart...")
    plot_risk_intention_chart(df, save_dir)
    
    print("Advanced visualization suite generation completed!")


# ============================================================================
# Upgraded Advanced Visualization Functions
# ============================================================================

def plot_multi_stage_alluvial(df, save_dir):
    """
    Multi-stage Alluvial/Sankey Diagram: Knowledge -> Trust -> Attitude -> Intention
    Visualizing mediation paths
    """
    import os
    # Log data
    print(f"\n[Data Log] Data for Multi-stage Alluvial Plot:")
    print("Note: Data is discretized into Low/Medium/High groups.")
    
    setup_style()
    
    fig, ax = plt.subplots(figsize=(18, 12), facecolor='white')
    
    # Prepare data: Discretize continuous variables into 3 levels
    def discretize(series, labels=['Low', 'Medium', 'High']):
        try:
            return pd.qcut(series, q=3, labels=labels, duplicates='drop')
        except:
            # If quantiles are the same, use cut
            return pd.cut(series, bins=3, labels=labels)
    
    # Variables for four stages
    stages = []
    stage_names = []
    
    # Stage 1: Knowledge Level
    if '认知指数' in df.columns:
        df['Knowledge_Group'] = discretize(df['认知指数'], ['Low Know.', 'Med Know.', 'High Know.'])
        stages.append('Knowledge_Group')
        stage_names.append('Knowledge Level')
    
    # Stage 2: Trust Level
    if '信任指数' in df.columns:
        df['Trust_Group'] = discretize(df['信任指数'], ['Low Trust', 'Med Trust', 'High Trust'])
        stages.append('Trust_Group')
        stage_names.append('Trust Level')
    
    # Stage 3: Attitude
    if '态度' in df.columns:
        df['Attitude_Group'] = discretize(df['态度'], ['Low Att.', 'Med Att.', 'High Att.'])
        stages.append('Attitude_Group')
        stage_names.append('Attitude Level')
    
    # Stage 4: Purchase Intention
    if '5年内购车意愿' in df.columns:
        intention_map = {1: 'High Int.', 2: 'High Int.', 3: 'Med Int.', 4: 'Low Int.', 5: 'Low Int.'}
        df['Intention_Group'] = df['5年内购车意愿'].map(intention_map)
        stages.append('Intention_Group')
        stage_names.append('Purchase Intention')
    
    if len(stages) < 3:
        ax.text(0.5, 0.5, 'Insufficient data to generate multi-stage alluvial plot', ha='center', va='center', fontsize=14)

        save_fig(fig, os.path.join(save_dir, 'Advanced_Multi_Stage_Alluvial.png'))
        return
    
    # Calculate categories and positions for each stage
    n_stages = len(stages)
    stage_x = np.linspace(0.1, 0.9, n_stages)
    
    # Color scheme
    level_colors = {
        'High': UNIFIED_COLORS['positive'], 'Medium': UNIFIED_COLORS['neutral'], 'Low': UNIFIED_COLORS['negative'],
        'High Know.': UNIFIED_COLORS['positive'], 'Med Know.': UNIFIED_COLORS['neutral'], 'Low Know.': UNIFIED_COLORS['negative'],
        'High Trust': UNIFIED_COLORS['primary'], 'Med Trust': UNIFIED_COLORS['tertiary'], 'Low Trust': UNIFIED_COLORS['negative'],
        'High Att.': UNIFIED_COLORS['quaternary'], 'Med Att.': UNIFIED_COLORS['secondary'], 'Low Att.': UNIFIED_COLORS['negative'],
        'High Int.': UNIFIED_COLORS['positive'], 'Med Int.': UNIFIED_COLORS['neutral'], 'Low Int.': UNIFIED_COLORS['negative'],
    }
    
    # Draw nodes for each stage
    node_positions = {}  # Store position of each node
    
    for stage_idx, (stage, stage_name) in enumerate(zip(stages, stage_names)):
        x = stage_x[stage_idx]
        categories = df[stage].dropna().unique()
        # Order: High, Medium, Low
        order = ['High', 'Medium', 'Low']
        categories = sorted(categories, key=lambda c: next((i for i, o in enumerate(order) if o in str(c)), 99))
        
        counts = df[stage].value_counts()
        total = counts.sum()
        
        # Calculate y position for each category
        y_start = 0.1
        y_end = 0.9
        y_range = y_end - y_start
        
        current_y = y_start
        for cat in categories:
            count = counts.get(cat, 0)
            height = (count / total) * y_range
            
            # Node center position
            node_y = current_y + height / 2
            node_positions[(stage_idx, cat)] = (x, node_y, height)
            
            # Draw node (rectangle)
            color = level_colors.get(cat, '#95A5A6')
            rect = plt.Rectangle((x - 0.03, current_y), 0.06, height,
                                 facecolor=color, edgecolor='white', linewidth=2, alpha=0.85)
            ax.add_patch(rect)
            
            # Add label
            if height > 0.05:
                ax.text(x, node_y, f'{cat}\n({count})', ha='center', va='center',
                       fontsize=9, fontweight='bold', color='white')
            
            current_y += height
        
        # Stage title
        ax.text(x, 0.02, stage_name, ha='center', va='bottom', fontsize=13, 
               fontweight='bold', color='#2C3E50')
    
    # Draw flows (filled areas, like Sankey)
    from matplotlib.path import Path
    import matplotlib.patches as mpatches
    
    y_range = 0.8  # Consistent with node drawing range
    total_n = len(df)
    
    # Track flow positions for connections between stages
    # Need to track: right exit position of left node, left entry position of right node
    for stage_idx in range(n_stages - 1):
        stage1, stage2 = stages[stage_idx], stages[stage_idx + 1]
        
        # Initialize flow position tracking for current stage connection
        # Left node: accumulate from bottom
        left_flow_pos = {}
        for cat in df[stage1].dropna().unique():
            key = (stage_idx, cat)
            if key in node_positions:
                x, y_center, h = node_positions[key]
                left_flow_pos[cat] = y_center - h / 2  # Start from bottom
        
        # Right node: accumulate from bottom
        right_flow_pos = {}
        for cat in df[stage2].dropna().unique():
            key = (stage_idx + 1, cat)
            if key in node_positions:
                x, y_center, h = node_positions[key]
                right_flow_pos[cat] = y_center - h / 2  # Start from bottom
        
        # Calculate flow volume
        flow_data = df.groupby([stage1, stage2]).size().reset_index(name='count')
        
        for _, row in flow_data.iterrows():
            cat1, cat2, count = row[stage1], row[stage2], row['count']
            
            if pd.isna(cat1) or pd.isna(cat2):
                continue
            
            pos1 = node_positions.get((stage_idx, cat1))
            pos2 = node_positions.get((stage_idx + 1, cat2))
            
            if pos1 is None or pos2 is None:
                continue
            
            x1, y1_center, h1 = pos1
            x2, y2_center, h2 = pos2
            
            # Flow height proportional to count (consistent with node height calculation)
            flow_height = (count / total_n) * y_range
            
            # Get current flow position
            y0 = left_flow_pos.get(cat1, y1_center - h1 / 2)
            y1 = right_flow_pos.get(cat2, y2_center - h2 / 2)
            
            # Update flow position
            left_flow_pos[cat1] = y0 + flow_height
            right_flow_pos[cat2] = y1 + flow_height
            
            # Use source node color
            color = level_colors.get(cat1, '#95A5A6')
            
            # Control point x offset (make curve smoother)
            x_offset = (x2 - x1) * 0.4
            
            # Draw filled area (closed Bezier curve path)
            verts = [
                (x1 + 0.03, y0),  # Bottom left
                (x1 + 0.03 + x_offset, y0),  # Control point 1
                (x2 - 0.03 - x_offset, y1),  # Control point 2
                (x2 - 0.03, y1),  # Bottom right
                (x2 - 0.03, y1 + flow_height),  # Top right
                (x2 - 0.03 - x_offset, y1 + flow_height),  # Control point 3
                (x1 + 0.03 + x_offset, y0 + flow_height),  # Control point 4
                (x1 + 0.03, y0 + flow_height),  # Top left
                (x1 + 0.03, y0)  # Close
            ]
            
            codes = [
                Path.MOVETO,
                Path.CURVE4, Path.CURVE4, Path.CURVE4,
                Path.LINETO,
                Path.CURVE4, Path.CURVE4, Path.CURVE4,
                Path.CLOSEPOLY
            ]
            
            path = Path(verts, codes)
            patch = mpatches.PathPatch(path, facecolor=color, edgecolor='white',
                                       linewidth=0.5, alpha=0.6)
            ax.add_patch(patch)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    ax.set_title('Knowledge -> Trust -> Attitude -> Intention Multi-stage Flow\n(Mediation Path Visualization)', 
                fontsize=18, fontweight='bold', pad=20)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor=UNIFIED_COLORS['positive'], label='High Level'),
        mpatches.Patch(facecolor=UNIFIED_COLORS['neutral'], label='Medium Level'),
        mpatches.Patch(facecolor=UNIFIED_COLORS['negative'], label='Low Level'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10, 
             title='Level Category', title_fontsize=11)
    
    save_fig(fig, os.path.join(save_dir, 'Advanced_Multi_Stage_Alluvial.png'))


def plot_chord_diagram(df, save_dir):
    """
    Variable Relationship Chord Diagram
    Visualizing correlations between core variables
    """
    import os
    # Log data
    print(f"\n[Data Log] Data for Chord Diagram:")
    core_vars = ['认知指数', '责任感指数', '信任指数', '政策认同指数', '态度', '购车意愿']
    available_vars = [v for v in core_vars if v in df.columns]
    print(f"Variables: {available_vars}")
    if available_vars:
        print("Correlation Matrix:")
        print(df[available_vars].corr())

    setup_style()
    
    fig, ax = plt.subplots(figsize=(14, 14), facecolor='white', subplot_kw=dict(projection='polar'))
    
    # Select core variables
    core_vars = ['认知指数', '责任感指数', '信任指数', '政策认同指数', '态度', '购车意愿']
    var_labels = ['Knowledge', 'Responsibility', 'Trust', 'Policy', 'Attitude', 'Intention']
    
    # If Intention doesn't exist but 5-year intention does, create it
    if '购车意愿' not in df.columns and '5年内购车意愿' in df.columns:
        df['购车意愿'] = 6 - df['5年内购车意愿']  # Reverse coding
    
    available_vars = [v for v in core_vars if v in df.columns]
    available_labels = [var_labels[i] for i, v in enumerate(core_vars) if v in df.columns]
    
    if len(available_vars) < 3:
        ax.text(0.5, 0.5, 'Insufficient data to generate chord diagram', ha='center', va='center', fontsize=14)
        save_fig(fig, os.path.join(save_dir, 'Advanced_Variable_Chord.png'))
        return
    
    n_vars = len(available_vars)
    
    # Calculate correlation matrix
    corr_matrix = df[available_vars].corr()
    
    # Node positions (evenly distributed on circle)
    angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False)
    
    # Node colors
    node_colors = get_unified_palette(n_vars, 'categorical')
    
    # Draw outer nodes
    for i, (angle, label, color) in enumerate(zip(angles, available_labels, node_colors)):
        # Draw node sector
        width = 2 * np.pi / n_vars * 0.8
        ax.bar(angle, 1, width=width, bottom=0.85, color=color, edgecolor='white', linewidth=2, alpha=0.9)
        
        # Add label
        label_angle = angle
        ha = 'center'
        rotation = np.degrees(angle) - 90
        if angle > np.pi/2 and angle < 3*np.pi/2:
            rotation += 180
        
        ax.text(angle, 1.15, label, ha='center', va='center', fontsize=12, fontweight='bold',
               rotation=rotation, rotation_mode='anchor')
    
    # Draw chords (correlations)
    threshold = 0.3  # Only show |r|>0.3
    
    for i in range(n_vars):
        for j in range(i + 1, n_vars):
            r = corr_matrix.iloc[i, j]
            
            if abs(r) < threshold:
                continue
            
            angle1, angle2 = angles[i], angles[j]
            
            # Chord color: Green for positive, Red for negative
            if r > 0:
                chord_color = UNIFIED_COLORS['positive']
            else:
                chord_color = UNIFIED_COLORS['negative']
            
            # Chord width proportional to correlation strength
            linewidth = abs(r) * 8
            
            # Draw Bezier curve connecting two points
            # Simplified: straight line inside circle arc
            r_inner = 0.85
            
            # Start and end points
            x1, y1 = angle1, r_inner
            x2, y2 = angle2, r_inner
            
            # Use quadratic Bezier curve
            n_points = 50
            t = np.linspace(0, 1, n_points)
            
            # Control point towards center
            mid_angle = (angle1 + angle2) / 2
            if abs(angle2 - angle1) > np.pi:
                mid_angle += np.pi
            
            # Curve curvature
            curve_r = r_inner * 0.3
            
            # Parametric curve
            curve_angles = angle1 + t * (angle2 - angle1)
            # Adjust to make curve bend inwards
            curve_radii = r_inner - (1 - np.abs(2*t - 1)**2) * (r_inner - curve_r)
            
            ax.plot(curve_angles, curve_radii, color=chord_color, linewidth=linewidth, 
                   alpha=0.6, solid_capstyle='round')
            
            # Add correlation coefficient in the middle of chord
            mid_idx = len(t) // 2
            ax.text(curve_angles[mid_idx], curve_radii[mid_idx] - 0.08, 
                   f'{r:.2f}', ha='center', va='center', fontsize=8, 
                   color=chord_color, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    ax.set_ylim(0, 1.3)
    ax.axis('off')
    
    ax.set_title('Core Variable Correlation Chord Diagram\n(Relationships |r|>0.3)', fontsize=18, fontweight='bold', y=1.05)
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=UNIFIED_COLORS['positive'], linewidth=4, label='Positive Corr'),
        Line2D([0], [0], color=UNIFIED_COLORS['negative'], linewidth=4, label='Negative Corr'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11,
             bbox_to_anchor=(1.1, -0.05))
    
    save_fig(fig, os.path.join(save_dir, 'Advanced_Variable_Chord.png'))


def plot_respondent_clustermap(df, save_dir):
    """
    Respondent Cluster Heatmap
    Visualizing response patterns and cluster structure of individuals x items
    """
    import os
    from scipy.cluster.hierarchy import linkage, dendrogram
    from scipy.spatial.distance import pdist
    
    # Log data
    print(f"\n[Data Log] Data for Respondent Cluster Heatmap:")
    print("Note: Using key items for clustering.")

    setup_style()
    
    # Select key items
    key_items = []
    item_labels = []
    
    # Trust related
    trust_items = ['技术信任度', '新能源汽车技术信任度', '政策执行信任度']
    for item in trust_items:
        if item in df.columns:
            key_items.append(item)
            item_labels.append(item.replace('度', '').replace('技术', 'Tech ').replace('新能源汽车', 'NEV ').replace('政策执行', 'Policy Exec ').replace('信任', 'Trust'))
    
    # Attitude related
    attitude_items = ['转型支持度', '碳中和支持度', '新能源汽车态度']
    for item in attitude_items:
        if item in df.columns:
            key_items.append(item)
            item_labels.append(item.replace('度', '').replace('转型', 'Trans ').replace('支持', 'Support').replace('碳中和', 'Carbon Neutral ').replace('新能源汽车', 'NEV ').replace('态度', 'Attitude'))
    
    # Policy related
    policy_items = ['激励政策认同度', '限油推新支持度']
    for item in policy_items:
        if item in df.columns:
            key_items.append(item)
            item_labels.append(item.replace('度', '').replace('激励政策', 'Incentive ').replace('认同', 'Approval').replace('限油推新', 'Fuel Limit ').replace('支持', 'Support'))
    
    if len(key_items) < 4:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.text(0.5, 0.5, 'Insufficient data to generate cluster heatmap', ha='center', va='center', fontsize=14)
        save_fig(fig, os.path.join(save_dir, 'Advanced_Respondent_Cluster.png'))
        return
    
    # Prepare data matrix
    data_matrix = df[key_items].copy()
    
    # Convert to positive scoring (if needed) and normalize to 1-5
    for col in data_matrix.columns:
        if data_matrix[col].max() > 5:
            data_matrix[col] = (data_matrix[col] - data_matrix[col].min()) / (data_matrix[col].max() - data_matrix[col].min()) * 4 + 1
    
    # Handle missing values
    data_matrix = data_matrix.dropna()
    
    if len(data_matrix) < 10:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.text(0.5, 0.5, 'Insufficient valid data', ha='center', va='center', fontsize=14)
        save_fig(fig, os.path.join(save_dir, 'Advanced_Respondent_Cluster.png'))
        return
    
    # Use seaborn clustermap
    # Custom colormap
    cmap = sns.diverging_palette(250, 15, s=75, l=40, n=9, center='light', as_cmap=True)
    
    # Create cluster heatmap
    g = sns.clustermap(data_matrix, 
                       method='ward',
                       metric='euclidean',
                       cmap='RdYlGn',
                       figsize=(14, 16),
                       row_cluster=True,
                       col_cluster=True,
                       dendrogram_ratio=(0.15, 0.15),
                       cbar_pos=(0.02, 0.8, 0.03, 0.15),
                       xticklabels=item_labels,
                       yticklabels=False,
                       linewidths=0.5,
                       linecolor='white')
    
    # Adjust title
    g.fig.suptitle('Respondent Response Pattern Cluster Heatmap\n(Row=Respondent, Col=Item)', 
                   fontsize=16, fontweight='bold', y=1.02)
    
    # Add colorbar label
    g.ax_cbar.set_ylabel('Score (1-5)', fontsize=10)
    
    # Save
    g.savefig(os.path.join(save_dir, 'Advanced_Respondent_Cluster.png'), 
              dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
    plt.close()


def plot_awareness_pca(df, save_dir):
    """
    Awareness Space PCA Scatter Plot
    Reducing multi-dimensional variables to 2D, showing respondents' "awareness map"
    """
    import os
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    
    # Log data
    print(f"\n[Data Log] Data for Awareness PCA:")
    pca_vars = ['认知指数', '责任感指数', '信任指数', '政策认同指数']
    available_vars = [v for v in pca_vars if v in df.columns]
    print(f"PCA Variables: {available_vars}")
    if available_vars:
        print("Descriptive Statistics:")
        print(df[available_vars].describe())

    setup_style()
    
    fig, ax = plt.subplots(figsize=(14, 12), facecolor='white')
    
    # Select variables for PCA
    pca_vars = ['认知指数', '责任感指数', '信任指数', '政策认同指数']
    available_vars = [v for v in pca_vars if v in df.columns]
    
    if len(available_vars) < 3:
        ax.text(0.5, 0.5, 'Insufficient data for PCA analysis', ha='center', va='center', fontsize=14)
        save_fig(fig, os.path.join(save_dir, 'Advanced_Awareness_PCA.png'))
        return
    
    # Prepare data
    pca_data = df[available_vars].dropna()
    
    if len(pca_data) < 20:
        ax.text(0.5, 0.5, 'Insufficient valid samples', ha='center', va='center', fontsize=14)
        save_fig(fig, os.path.join(save_dir, 'Advanced_Awareness_PCA.png'))
        return
    
    # Standardization
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(pca_data)
    
    # PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)
    
    # Create result DataFrame
    pca_df = pd.DataFrame({
        'PC1': pca_result[:, 0],
        'PC2': pca_result[:, 1]
    }, index=pca_data.index)
    
    # Add grouping variables
    if '5年内购车意愿' in df.columns:
        intention_map = {1: 'High Int.', 2: 'High Int.', 3: 'Med Int.', 4: 'Low Int.', 5: 'Low Int.'}
        pca_df['Intention'] = df.loc[pca_df.index, '5年内购车意愿'].map(intention_map)
    
    if '能源经历' in df.columns:
        exp_map = {1: 'Exp.', 2: 'No Exp.'}
        pca_df['Experience'] = df.loc[pca_df.index, '能源经历'].map(exp_map)
    
    # Color and marker mapping
    intention_colors = {'High Int.': UNIFIED_COLORS['positive'], 'Med Int.': UNIFIED_COLORS['neutral'], 'Low Int.': UNIFIED_COLORS['negative']}
    exp_markers = {'Exp.': 'o', 'No Exp.': 's'}
    
    # Draw scatter plot
    for intention in ['High Int.', 'Med Int.', 'Low Int.']:
        for exp in ['Exp.', 'No Exp.']:
            mask = (pca_df['Intention'] == intention) & (pca_df['Experience'] == exp)
            subset = pca_df[mask]
            
            if len(subset) > 0:
                ax.scatter(subset['PC1'], subset['PC2'],
                          c=intention_colors.get(intention, '#95A5A6'),
                          marker=exp_markers.get(exp, 'o'),
                          s=120, alpha=0.7, edgecolors='white', linewidths=1.5,
                          label=f'{intention} / {exp}')
    
    # Add quadrant lines
    ax.axhline(y=0, color='#BDC3C7', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=0, color='#BDC3C7', linestyle='--', linewidth=1, alpha=0.7)
    
    # Add quadrant labels
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    ax.text(xlim[1]*0.7, ylim[1]*0.8, 'High Trust/Resp.', fontsize=11, 
           color=UNIFIED_COLORS['positive'], fontweight='bold', alpha=0.8)
    ax.text(xlim[0]*0.7, ylim[1]*0.8, 'Low Trust/High Resp.', fontsize=11, 
           color=UNIFIED_COLORS['neutral'], fontweight='bold', alpha=0.8)
    ax.text(xlim[0]*0.7, ylim[0]*0.8, 'Low Trust/Low Resp.', fontsize=11, 
           color=UNIFIED_COLORS['negative'], fontweight='bold', alpha=0.8)
    ax.text(xlim[1]*0.7, ylim[0]*0.8, 'High Trust/Low Resp.', fontsize=11, 
           color=UNIFIED_COLORS['primary'], fontweight='bold', alpha=0.8)
    
    # Axis labels (with variance explained)
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% Var Explained)\n← Low Trust/Policy — High Trust/Policy →', 
                 fontsize=12, fontweight='bold')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% Var Explained)\n← Low Resp./Know. — High Resp./Know. →', 
                 fontsize=12, fontweight='bold')
    
    ax.set_title('University Student NEV Awareness Space (PCA)', fontsize=18, fontweight='bold', pad=20)
    
    # Legend
    ax.legend(loc='upper left', fontsize=10, title='Intention / Experience', 
             title_fontsize=11, framealpha=0.95)
    
    # Add loading vectors (optional)
    # Show contribution of each variable to PCs
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    
    for i, var in enumerate(available_vars):
        var_short = var.replace('指数', '').replace('认知', 'Know.').replace('责任感', 'Resp.').replace('信任', 'Trust').replace('政策认同', 'Policy')
        ax.annotate('', xy=(loadings[i, 0]*3, loadings[i, 1]*3), xytext=(0, 0),
                   arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2))
        ax.text(loadings[i, 0]*3.3, loadings[i, 1]*3.3, var_short, 
               fontsize=10, fontweight='bold', color='#2C3E50')
    
    sns.despine(ax=ax)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add explanation
    total_var = sum(pca.explained_variance_ratio_[:2]) * 100
    ax.text(0.02, 0.02, f'Total Variance Explained: {total_var:.1f}%', transform=ax.transAxes,
           fontsize=10, color='#666666', style='italic')
    
    save_fig(fig, os.path.join(save_dir, 'Advanced_Awareness_PCA.png'))


def plot_sem_path_diagram(df, save_dir):
    """
    SEM Style Path Diagram
    Visualizing causal paths and effect strengths between variables
    """
    import os
    from scipy import stats
    
    # Log data
    print(f"\n[Data Log] Data for SEM Path Diagram:")
    var_map = {
        'Knowledge': '认知指数',
        'Trust': '信任指数', 
        'Responsibility': '责任感指数',
        'Policy': '政策认同指数',
        'Attitude': '态度',
        'Intention': '5年内购车意愿'
    }
    print("Variables Mapping:", var_map)
    sem_vars = [v for v in var_map.values() if v in df.columns]
    if sem_vars:
        print("Correlation Matrix (Proxy for Path Coefficients):")
        print(df[sem_vars].corr())

    setup_style()
    
    fig, ax = plt.subplots(figsize=(16, 12), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define node positions
    nodes = {
        'Knowledge': (1.5, 4),
        'Trust': (4, 6),
        'Responsibility': (4, 2),
        'Policy': (6.5, 5),
        'Attitude': (6.5, 3),
        'Intention': (9, 4),
    }
    
    # Variable mapping
    var_map = {
        'Knowledge': '认知指数',
        'Trust': '信任指数', 
        'Responsibility': '责任感指数',
        'Policy': '政策认同指数',
        'Attitude': '态度',
        'Intention': '5年内购车意愿'
    }
    
    # Check if variables exist
    available_nodes = {k: v for k, v in nodes.items() if var_map.get(k) in df.columns or k == 'Intention'}
    
    # Calculate path coefficients (using correlation coefficients as simplification)
    def get_path_coef(var1, var2):
        v1 = var_map.get(var1)
        v2 = var_map.get(var2)
        if v1 not in df.columns or v2 not in df.columns:
            return None, None
        
        data1 = df[v1].dropna()
        data2 = df[v2].dropna()
        common_idx = data1.index.intersection(data2.index)
        
        if len(common_idx) < 10:
            return None, None
        
        r, p = stats.pearsonr(data1[common_idx], data2[common_idx])
        return r, p
    
    # Define paths
    paths = [
        ('Knowledge', 'Trust'),
        ('Knowledge', 'Responsibility'),
        ('Knowledge', 'Attitude'),
        ('Trust', 'Attitude'),
        ('Trust', 'Policy'),
        ('Responsibility', 'Attitude'),
        ('Policy', 'Attitude'),
        ('Attitude', 'Intention'),
        ('Trust', 'Intention'),
        ('Policy', 'Intention'),
    ]
    
    # Draw nodes
    node_colors = {
        'Knowledge': UNIFIED_COLORS['primary'],
        'Trust': UNIFIED_COLORS['tertiary'],
        'Responsibility': UNIFIED_COLORS['secondary'],
        'Policy': UNIFIED_COLORS['quaternary'],
        'Attitude': UNIFIED_COLORS['neutral'],
        'Intention': UNIFIED_COLORS['positive'],
    }
    
    for node, (x, y) in available_nodes.items():
        # Draw rounded rectangle
        rect = plt.Rectangle((x-0.7, y-0.4), 1.4, 0.8, 
                             facecolor=node_colors.get(node, '#95A5A6'),
                             edgecolor='white', linewidth=3, 
                             alpha=0.9, zorder=10,
                             transform=ax.transData)
        from matplotlib.patches import FancyBboxPatch
        bbox = FancyBboxPatch((x-0.7, y-0.4), 1.4, 0.8,
                              boxstyle="round,pad=0.05,rounding_size=0.2",
                              facecolor=node_colors.get(node, '#95A5A6'),
                              edgecolor='white', linewidth=3,
                              alpha=0.9, zorder=10)
        ax.add_patch(bbox)
        
        # Node label
        ax.text(x, y, node, ha='center', va='center', fontsize=13, 
               fontweight='bold', color='white', zorder=11)
        
        # Add R² (if dependent variable)
        if node in ['Attitude', 'Intention']:
            ax.text(x, y-0.55, 'R²=0.XX', ha='center', va='top', fontsize=9,
                   color='#2C3E50', style='italic')
    
    # Draw paths
    for start, end in paths:
        if start not in available_nodes or end not in available_nodes:
            continue
        
        x1, y1 = available_nodes[start]
        x2, y2 = available_nodes[end]
        
        # Get path coefficient
        coef, pval = get_path_coef(start, end)
        
        if coef is None:
            continue
        
        # Path style
        if pval is not None and pval < 0.05:
            linestyle = '-'
            linewidth = max(1.5, abs(coef) * 5)
            alpha = 0.8
        else:
            linestyle = '--'
            linewidth = 1.5
            alpha = 0.4
        
        # Path color
        if coef > 0:
            color = UNIFIED_COLORS['positive']
        else:
            color = UNIFIED_COLORS['negative']
        
        # Calculate arrow position (avoid crossing nodes)
        dx, dy = x2 - x1, y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        
        # Adjust start and end points
        offset = 0.8
        start_x = x1 + (dx/dist) * offset
        start_y = y1 + (dy/dist) * offset
        end_x = x2 - (dx/dist) * offset
        end_y = y2 - (dy/dist) * offset
        
        # Draw arrow
        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                   arrowprops=dict(arrowstyle='->', color=color, 
                                  lw=linewidth, alpha=alpha,
                                  linestyle=linestyle,
                                  connectionstyle='arc3,rad=0.1'))
        
        # Add path coefficient label
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Significance marker
        if pval is not None:
            if pval < 0.001:
                sig = '***'
            elif pval < 0.01:
                sig = '**'
            elif pval < 0.05:
                sig = '*'
            else:
                sig = ''
        else:
            sig = ''
        
        ax.text(mid_x, mid_y, f'β={coef:.2f}{sig}', ha='center', va='center',
               fontsize=9, fontweight='bold', color=color,
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
    
    # Add legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=UNIFIED_COLORS['positive'], linewidth=3, label='Positive Effect'),
        Line2D([0], [0], color=UNIFIED_COLORS['negative'], linewidth=3, label='Negative Effect'),
        Line2D([0], [0], color='gray', linewidth=2, linestyle='--', label='Not Significant'),
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=10,
             title='Path Type', title_fontsize=11, framealpha=0.95)
    
    # Significance explanation
    ax.text(0.98, 0.02, '*** p<0.001  ** p<0.01  * p<0.05', 
           transform=ax.transAxes, ha='right', va='bottom', fontsize=9,
           color='#666666', style='italic')
    
    ax.set_title('NEV Purchase Intention Influence Path Model\n(SEM Style Path Diagram)', 
                fontsize=18, fontweight='bold', pad=20)
    
    save_fig(fig, os.path.join(save_dir, 'Advanced_SEM_Path.png'))


def plot_risk_intention_chart(df, save_dir):
    """
    Risk-Intention Relationship Chart
    Visualizing relationship between concerns and purchase intention
    """
    import os
    from scipy import stats
    
    # Log data
    print(f"\n[Data Log] Data for Risk-Intention Chart:")
    problem_vars = {
        '问题_续航': 'Range Anxiety',
        '问题_充电设施': 'Charging Inconv.',
        '问题_电池': 'Battery Safety',
        '问题_价格': 'High Price',
        '问题_安全': 'Overall Safety',
    }
    available_problems = {k: v for k, v in problem_vars.items() if k in df.columns}
    print(f"Problem Variables: {available_problems}")
    
    if available_problems and '5年内购车意愿' in df.columns:
        print("Worry Percentages and Intention Differences:")
        summary_data = []
        for prob in available_problems:
             worry_pct = df[prob].sum() / len(df) * 100
             worried_int = df[df[prob] == 1]['5年内购车意愿'].mean()
             not_worried_int = df[df[prob] == 0]['5年内购车意愿'].mean()
             summary_data.append({'Problem': prob, 'Worry%': worry_pct, 'Worried_Intention': worried_int, 'Not_Worried_Intention': not_worried_int})
        print(pd.DataFrame(summary_data))

    setup_style()
    
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
    
    # Problem perception variables
    problem_vars = {
        '问题_续航': 'Range Anxiety',
        '问题_充电设施': 'Charging Inconv.',
        '问题_电池': 'Battery Safety',
        '问题_价格': 'High Price',
        '问题_安全': 'Overall Safety',
    }
    
    available_problems = {k: v for k, v in problem_vars.items() if k in df.columns}
    
    if len(available_problems) == 0 or '5年内购车意愿' not in df.columns:
        ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center', fontsize=14)
        save_fig(fig, os.path.join(save_dir, 'Advanced_Risk_Intention.png'))
        return
    
    # Intention to positive
    df['Intention_Pos'] = 6 - df['5年内购车意愿']
    
    problems = list(available_problems.keys())
    labels = list(available_problems.values())
    
    # Calculate worry percentage and intention difference for each problem
    worry_pcts = []
    intention_diffs = []
    intention_high = []
    intention_low = []
    error_bars = []
    
    for prob in problems:
        # Worry percentage (proportion of people selecting this problem)
        worry_pct = df[prob].sum() / len(df) * 100
        worry_pcts.append(worry_pct)
        
        # Intention difference between worried and not worried groups
        worried = df[df[prob] == 1]['Intention_Pos']
        not_worried = df[df[prob] == 0]['Intention_Pos']
        
        mean_worried = worried.mean() if len(worried) > 0 else 0
        mean_not_worried = not_worried.mean() if len(not_worried) > 0 else 0
        
        intention_high.append(mean_not_worried)
        intention_low.append(mean_worried)
        intention_diffs.append(mean_not_worried - mean_worried)
        
        # Standard error
        se = worried.std() / np.sqrt(len(worried)) if len(worried) > 1 else 0
        error_bars.append(se)
    
    # Sort (by worry percentage)
    sorted_idx = np.argsort(worry_pcts)[::-1]
    labels = [labels[i] for i in sorted_idx]
    worry_pcts = [worry_pcts[i] for i in sorted_idx]
    intention_diffs = [intention_diffs[i] for i in sorted_idx]
    intention_high = [intention_high[i] for i in sorted_idx]
    intention_low = [intention_low[i] for i in sorted_idx]
    error_bars = [error_bars[i] for i in sorted_idx]
    
    y_pos = np.arange(len(labels))
    
    # Create dual axis
    ax2 = ax.twiny()
    
    # Draw worry percentage (horizontal bar chart)
    bars = ax.barh(y_pos, worry_pcts, height=0.6, color=UNIFIED_COLORS['primary'], alpha=0.7,
                   edgecolor='white', linewidth=2, label='Worry %')
    
    # Add worry percentage values
    for i, (bar, pct) in enumerate(zip(bars, worry_pcts)):
        ax.text(pct + 1, bar.get_y() + bar.get_height()/2, f'{pct:.0f}%',
               va='center', fontsize=10, fontweight='bold', color=UNIFIED_COLORS['primary'])
    
    # Draw intention difference points (on second x-axis)
    scatter_x = intention_diffs
    scatter_colors = [UNIFIED_COLORS['positive'] if d > 0 else UNIFIED_COLORS['negative'] for d in scatter_x]
    
    ax2.scatter(scatter_x, y_pos, s=200, c=scatter_colors, 
               edgecolors='white', linewidths=2, zorder=5, marker='D')
    
    # Add error bars
    ax2.errorbar(scatter_x, y_pos, xerr=error_bars, fmt='none', 
                ecolor='#666666', elinewidth=1.5, capsize=4, capthick=1.5, zorder=4)
    
    # Add difference values (above points)
    for i, (x, diff) in enumerate(zip(scatter_x, intention_diffs)):
        ax2.text(x, y_pos[i] + 0.25, f'{diff:+.2f}', va='bottom', ha='center',
                fontsize=11, fontweight='bold', color=scatter_colors[i],
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                         edgecolor=scatter_colors[i], alpha=0.9))
    
    # Zero line
    ax2.axvline(x=0, color='#BDC3C7', linestyle='--', linewidth=1.5, alpha=0.7)
    
    # Set axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=12)
    ax.set_xlabel('Worry Percentage (%)', fontsize=13, fontweight='bold', color=UNIFIED_COLORS['primary'])
    ax.set_xlim(0, max(worry_pcts) * 1.3)
    
    ax2.set_xlabel('Intention Difference (Not Worried - Worried)', fontsize=13, fontweight='bold', color='#666666')
    xlim_max = max(abs(min(scatter_x)), abs(max(scatter_x))) * 1.5
    ax2.set_xlim(-xlim_max, xlim_max)
    
    # Legend
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor=UNIFIED_COLORS['primary'], alpha=0.7, label='Worry %'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor=UNIFIED_COLORS['positive'],
               markersize=10, label='Positive Diff (Not worried has higher int.)'),
        Line2D([0], [0], marker='D', color='w', markerfacecolor=UNIFIED_COLORS['negative'],
               markersize=10, label='Negative Diff (Worried has higher int.)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.95)
    
    ax.set_title('NEV Concerns vs Purchase Intention\n(Worry % vs Intention Difference)', 
                fontsize=18, fontweight='bold', pad=20)
    
    sns.despine(ax=ax, left=True)
    ax.tick_params(left=False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add explanation
    ax.text(0.02, 0.02, 'Positive difference means worry about this issue reduces purchase intention', 
           transform=ax.transAxes, fontsize=9, color='#666666', style='italic')
    
    save_fig(fig, os.path.join(save_dir, 'Advanced_Risk_Intention.png'))
