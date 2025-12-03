"""
visualize_results.py - Visualize kết quả test từ test_full_algorithm.py

File này đọc các CSV files và tạo các biểu đồ để so sánh hiệu suất của 4 thuật toán.

Charts được tạo:
1. Box plot - So sánh số lần đoán
2. Box plot - So sánh thời gian chạy
3. Box plot - So sánh số nodes expanded
4. Histogram - Phân bố số lần đoán cho mỗi thuật toán
5. Bar chart - Success rate comparison
6. Line plot - Performance over time (nếu có nhiều test runs)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import glob
import json
from datetime import datetime

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def load_latest_results(results_dir="test_results"):
    """Load kết quả test mới nhất"""
    data = {}
    # Sử dụng tên file thực tế (astar thay vì a*)
    algorithms = [
        ('bfs', 'BFS'),
        ('dfs', 'DFS'),
        ('astar', 'A*'),
        ('entropy-hard', 'Entropy-Hard'),
        ('entropy-normal', 'Entropy-Normal')
    ]
    
    for file_prefix, display_name in algorithms:
        # Tìm file CSV mới nhất
        pattern = os.path.join(results_dir, f"{file_prefix}_*.csv")
        files = glob.glob(pattern)
        
        if files:
            # Lấy file mới nhất
            latest_file = max(files, key=os.path.getctime)
            df = pd.read_csv(latest_file)
            data[display_name] = df
            print(f"✅ Loaded {display_name}: {len(df)} records from {os.path.basename(latest_file)}")
        else:
            print(f"⚠️  No data found for {display_name}")
    
    return data


def plot_guesses_comparison(data, save_path=None):
    """Box plot so sánh số lần đoán giữa các thuật toán"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Chuẩn bị dữ liệu
    plot_data = []
    labels = []
    
    for algo_name, df in data.items():
        plot_data.append(df['total_guesses'].values)
        labels.append(algo_name)
    
    # Tạo box plot
    bp = ax.boxplot(plot_data, labels=labels, patch_artist=True,
                    showmeans=True, meanline=True)
    
    # Màu sắc
    colors = ['#90EE90', '#FFB6C1', '#87CEEB', '#FFD700', '#FF69B4']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Total Guesses', fontsize=12, fontweight='bold')
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_title('Comparison of Total Guesses Across Algorithms', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Thêm mean values
    for i, (algo_name, df) in enumerate(data.items(), 1):
        mean_val = df['total_guesses'].mean()
        ax.text(i, mean_val, f'{mean_val:.2f}', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved to {save_path}")
    
    plt.show()


def plot_time_comparison(data, save_path=None):
    """Box plot so sánh thời gian chạy"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    plot_data = []
    labels = []
    
    for algo_name, df in data.items():
        plot_data.append(df['execution_time'].values)
        labels.append(algo_name)
    
    bp = ax.boxplot(plot_data, labels=labels, patch_artist=True,
                    showmeans=True, meanline=True)
    
    colors = ['#90EE90', '#FFB6C1', '#87CEEB', '#FFD700', '#FF69B4']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_title('Comparison of Execution Time Across Algorithms', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Thêm mean values
    for i, (algo_name, df) in enumerate(data.items(), 1):
        mean_val = df['execution_time'].mean()
        ax.text(i, mean_val, f'{mean_val:.4f}s', 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved to {save_path}")
    
    plt.show()


def plot_nodes_comparison(data, save_path=None):
    """Box plot so sánh số nodes expanded"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    plot_data = []
    labels = []
    
    for algo_name, df in data.items():
        plot_data.append(df['expanded_nodes'].values)
        labels.append(algo_name)
    
    bp = ax.boxplot(plot_data, labels=labels, patch_artist=True,
                    showmeans=True, meanline=True)
    
    colors = ['#90EE90', '#FFB6C1', '#87CEEB', '#FFD700', '#FF69B4']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Expanded Nodes', fontsize=12, fontweight='bold')
    ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax.set_title('Comparison of Expanded Nodes Across Algorithms', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Log scale nếu chênh lệch quá lớn
    max_val = max(max(d) for d in plot_data)
    min_val = min(min(d) for d in plot_data)
    if max_val / min_val > 100:
        ax.set_yscale('log')
        ax.set_ylabel('Expanded Nodes (log scale)', fontsize=12, fontweight='bold')
    
    # Thêm mean values
    for i, (algo_name, df) in enumerate(data.items(), 1):
        mean_val = df['expanded_nodes'].mean()
        ax.text(i, mean_val, f'{mean_val:.1f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved to {save_path}")
    
    plt.show()


def plot_guess_distribution(data, save_path=None):
    """Histogram phân bố số lần đoán"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    
    colors = ['#90EE90', '#FFB6C1', '#87CEEB', '#FFD700', '#FF69B4']
    
    for idx, (algo_name, df) in enumerate(data.items()):
        ax = axes[idx]
        
        # Tạo histogram
        counts = df['total_guesses'].value_counts().sort_index()
        ax.bar(counts.index, counts.values, color=colors[idx], alpha=0.7, edgecolor='black')
        
        # Thêm labels
        ax.set_xlabel('Number of Guesses', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.set_title(f'{algo_name} - Guess Distribution', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Thêm mean line
        mean_val = df['total_guesses'].mean()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_val:.2f}')
        ax.legend()
        
        # Thêm count labels trên mỗi bar
        for x, y in zip(counts.index, counts.values):
            ax.text(x, y, str(y), ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Hide unused subplot (we have 5 algorithms in 2x3 grid)
    if len(data) < len(axes):
        for idx in range(len(data), len(axes)):
            axes[idx].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved to {save_path}")
    
    plt.show()


def plot_summary_table(data, save_path=None):
    """Tạo bảng tổng hợp statistics"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')
    
    # Chuẩn bị data cho table
    table_data = []
    headers = ['Algorithm', 'Mean Guesses', 'Std Guesses', 'Mean Time (s)', 
               'Mean Nodes', 'Min Guesses', 'Max Guesses']
    
    for algo_name, df in data.items():
        row = [
            algo_name,
            f"{df['total_guesses'].mean():.2f}",
            f"{df['total_guesses'].std():.2f}",
            f"{df['execution_time'].mean():.4f}",
            f"{df['expanded_nodes'].mean():.1f}",
            f"{df['total_guesses'].min()}",
            f"{df['total_guesses'].max()}"
        ]
        table_data.append(row)
    
    # Tạo table
    table = ax.table(cellText=table_data, colLabels=headers,
                     cellLoc='center', loc='center',
                     colWidths=[0.12] * len(headers))
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Style rows
    colors = ['#E2EFDA', '#FCE4D6', '#DDEBF7', '#FFF2CC', '#FFE6F0']
    for i in range(len(table_data)):
        for j in range(len(headers)):
            table[(i+1, j)].set_facecolor(colors[i])
    
    plt.title('Algorithm Performance Summary', fontsize=14, fontweight='bold', pad=20)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved to {save_path}")
    
    plt.show()


def plot_performance_scatter(data, save_path=None):
    """Scatter plot: Time vs Guesses"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = ['#90EE90', '#FFB6C1', '#87CEEB', '#FFD700', '#FF69B4']
    markers = ['o', 's', '^', 'D', 'v']
    
    for idx, (algo_name, df) in enumerate(data.items()):
        ax.scatter(df['total_guesses'], df['execution_time'], 
                  alpha=0.5, s=30, c=colors[idx], marker=markers[idx],
                  label=algo_name)
    
    ax.set_xlabel('Total Guesses', fontsize=12, fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Performance: Execution Time vs Total Guesses', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved to {save_path}")
    
    plt.show()


def generate_all_plots(results_dir="test_results", output_dir="visualizations"):
    """Tạo tất cả các biểu đồ"""
    print("\n" + "="*70)
    print("📊 GENERATING VISUALIZATIONS")
    print("="*70)
    
    # Tạo output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    print("\n📂 Loading data...")
    data = load_latest_results(results_dir)
    
    if not data:
        print("❌ No data found to visualize!")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate plots
    print("\n📈 Generating plots...")
    
    print("\n1. Guesses comparison...")
    plot_guesses_comparison(data, os.path.join(output_dir, f"guesses_comparison_{timestamp}.png"))
    
    print("\n2. Time comparison...")
    plot_time_comparison(data, os.path.join(output_dir, f"time_comparison_{timestamp}.png"))
    
    print("\n3. Nodes comparison...")
    plot_nodes_comparison(data, os.path.join(output_dir, f"nodes_comparison_{timestamp}.png"))
    
    print("\n4. Guess distribution...")
    plot_guess_distribution(data, os.path.join(output_dir, f"guess_distribution_{timestamp}.png"))
    
    print("\n5. Summary table...")
    plot_summary_table(data, os.path.join(output_dir, f"summary_table_{timestamp}.png"))
    
    print("\n6. Performance scatter...")
    plot_performance_scatter(data, os.path.join(output_dir, f"performance_scatter_{timestamp}.png"))
    
    print("\n" + "="*70)
    print(f"✅ ALL VISUALIZATIONS SAVED TO: {output_dir}/")
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n🎨 WORDLE ALGORITHM VISUALIZATION TOOL\n")
    
    # Check if matplotlib is installed
    try:
        import matplotlib
        import seaborn
        print("✅ Required packages found")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install: pip install matplotlib seaborn pandas numpy")
        exit(1)
    
    # Generate visualizations
    generate_all_plots()
    
    print("✅ Visualization complete!\n")
