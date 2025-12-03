"""
DFS Algorithm Comprehensive Testing & Visualization
Tests DFS algorithm 1000 times and generates detailed statistics with visualizations
"""

import time
import sys
import os
import json
import csv
import random
from datetime import datetime
from collections import defaultdict, Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from words_api import Words
from Search_Algorithm.dfs import DFSSolver


class TestWordAPI:
    """Mock API for testing"""
    def __init__(self, word_size, target_word=None):
        self.real_api = Words(word_size)
        self.words_list = self.real_api.words_list
        self.size = word_size
        
        if target_word:
            if target_word.upper() in self.words_list:
                self.word = target_word.upper()
            else:
                self.word = random.choice(self.words_list).upper()
        else:
            self.word = random.choice(self.words_list).upper()
    
    def is_at_right_position(self, i, char):
        return self.word[i] == char
    
    def is_in_word(self, char):
        return char in self.word
    
    def is_valid_guess(self, guess):
        return guess == self.word
    
    def is_in_dictionary(self, word):
        return word.upper() in self.words_list
    
    def get_feedback(self, guess):
        feedback = []
        guess_upper = guess.upper()
        secret_list = list(self.word)
        guess_list = list(guess_upper)
        
        for i in range(len(guess_upper)):
            if guess_upper[i] == self.word[i]:
                feedback.append('correct')
                secret_list[i] = None
                guess_list[i] = None
        
        for i in range(len(guess_upper)):
            if guess_list[i] is not None:
                if guess_list[i] in secret_list:
                    feedback.append('present')
                    secret_list[secret_list.index(guess_list[i])] = None
                else:
                    feedback.append('absent')
        
        return feedback


def test_dfs_single(target_word=None):
    """Test DFS algorithm for a single word"""
    try:
        word_api = TestWordAPI(5, target_word)
        solver = DFSSolver(word_api)
        
        start_time = time.time()
        # DFS needs board_state (empty list for fresh start)
        result = solver.solve(board_state=[])
        elapsed = time.time() - start_time
        
        # DFS solver returns list from full_solution_path
        if hasattr(solver, 'full_solution_path') and solver.full_solution_path:
            path = solver.full_solution_path
            total_guesses = len(path)
            expanded_nodes = solver.expanded_nodes
            
            # Check if last guess is correct
            success = path[-1].upper() == word_api.word
            
            return {
                'success': success,
                'target_word': word_api.word,
                'total_guesses': total_guesses,
                'expanded_nodes': expanded_nodes,
                'execution_time': elapsed,
                'solution_path': path,
                'won_in_6': total_guesses <= 6 and success
            }
        else:
            return {
                'success': False,
                'target_word': word_api.word,
                'error': 'Failed to find solution - empty result'
            }
    
    except Exception as e:
        return {
            'success': False,
            'target_word': target_word if target_word else 'N/A',
            'error': str(e)
        }


def run_dfs_tests(num_tests=1000):
    """Run DFS tests multiple times"""
    print(f"\n{'='*70}")
    print(f"🎯 RUNNING DFS ALGORITHM TESTS ({num_tests} iterations)")
    print(f"{'='*70}\n")
    
    results = []
    failed_words = []
    
    for i in tqdm(range(num_tests), desc="Testing DFS", unit="test"):
        result = test_dfs_single()
        results.append(result)
        
        if not result['success']:
            failed_words.append(result)
    
    return results, failed_words


def calculate_statistics(results):
    """Calculate comprehensive statistics"""
    successful = [r for r in results if r['success']]
    
    if not successful:
        return None
    
    guesses = [r['total_guesses'] for r in successful]
    nodes = [r['expanded_nodes'] for r in successful]
    times = [r['execution_time'] for r in successful]
    won_6 = sum(1 for r in successful if r['won_in_6'])
    
    stats = {
        'total_tests': len(results),
        'successful': len(successful),
        'failed': len(results) - len(successful),
        'success_rate': len(successful) / len(results) * 100,
        'win_rate_6': won_6 / len(successful) * 100 if successful else 0,
        
        # Guesses statistics
        'guesses': {
            'mean': np.mean(guesses),
            'median': np.median(guesses),
            'std': np.std(guesses),
            'min': np.min(guesses),
            'max': np.max(guesses),
            'q1': np.percentile(guesses, 25),
            'q3': np.percentile(guesses, 75)
        },
        
        # Nodes statistics
        'nodes': {
            'mean': np.mean(nodes),
            'median': np.median(nodes),
            'std': np.std(nodes),
            'min': np.min(nodes),
            'max': np.max(nodes),
            'q1': np.percentile(nodes, 25),
            'q3': np.percentile(nodes, 75)
        },
        
        # Time statistics
        'time': {
            'mean': np.mean(times),
            'median': np.median(times),
            'std': np.std(times),
            'min': np.min(times),
            'max': np.max(times),
            'total': np.sum(times)
        },
        
        # Distribution
        'guess_distribution': dict(Counter(guesses)),
        'path_length_distribution': dict(Counter([len(r['solution_path']) for r in successful]))
    }
    
    return stats


def save_results(results, stats, output_dir='dfs_test_results'):
    """Save results to CSV and JSON"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save detailed results to CSV
    csv_path = os.path.join(output_dir, f'dfs_results_{timestamp}.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['target_word', 'success', 'total_guesses', 'expanded_nodes', 
                     'execution_time', 'won_in_6', 'solution_path']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in results:
            if r['success']:
                writer.writerow({
                    'target_word': r['target_word'],
                    'success': r['success'],
                    'total_guesses': r['total_guesses'],
                    'expanded_nodes': r['expanded_nodes'],
                    'execution_time': f"{r['execution_time']:.6f}",
                    'won_in_6': r['won_in_6'],
                    'solution_path': ' -> '.join(r['solution_path'])
                })
    
    # Save statistics to JSON
    json_path = os.path.join(output_dir, f'dfs_stats_{timestamp}.json')
    
    # Convert numpy types to native Python types
    def convert_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {convert_types(k): convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(item) for item in obj]
        return obj
    
    stats_native = convert_types(stats)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(stats_native, f, indent=2)
    
    print(f"\n✅ Results saved:")
    print(f"   📄 CSV: {csv_path}")
    print(f"   📊 JSON: {json_path}")
    
    return csv_path, json_path


def print_statistics(stats):
    """Print formatted statistics"""
    print(f"\n{'='*70}")
    print(f"📊 DFS ALGORITHM STATISTICS")
    print(f"{'='*70}\n")
    
    print(f"🎯 Test Results:")
    print(f"   Total Tests:      {stats['total_tests']:,}")
    print(f"   Successful:       {stats['successful']:,}")
    print(f"   Failed:           {stats['failed']:,}")
    print(f"   Success Rate:     {stats['success_rate']:.2f}%")
    print(f"   Win Rate (≤6):    {stats['win_rate_6']:.2f}%")
    
    print(f"\n📈 Guesses Statistics:")
    print(f"   Mean:             {stats['guesses']['mean']:.2f}")
    print(f"   Median:           {stats['guesses']['median']:.1f}")
    print(f"   Std Dev:          {stats['guesses']['std']:.2f}")
    print(f"   Min - Max:        {stats['guesses']['min']} - {stats['guesses']['max']}")
    print(f"   Q1 - Q3:          {stats['guesses']['q1']:.1f} - {stats['guesses']['q3']:.1f}")
    
    print(f"\n🔍 Expanded Nodes Statistics:")
    print(f"   Mean:             {stats['nodes']['mean']:.2f}")
    print(f"   Median:           {stats['nodes']['median']:.1f}")
    print(f"   Std Dev:          {stats['nodes']['std']:.2f}")
    print(f"   Min - Max:        {stats['nodes']['min']} - {stats['nodes']['max']}")
    print(f"   Q1 - Q3:          {stats['nodes']['q1']:.1f} - {stats['nodes']['q3']:.1f}")
    
    print(f"\n⏱️  Execution Time Statistics:")
    print(f"   Mean:             {stats['time']['mean']:.4f}s")
    print(f"   Median:           {stats['time']['median']:.4f}s")
    print(f"   Std Dev:          {stats['time']['std']:.4f}s")
    print(f"   Min - Max:        {stats['time']['min']:.4f}s - {stats['time']['max']:.4f}s")
    print(f"   Total Time:       {stats['time']['total']:.2f}s")
    
    print(f"\n📊 Guess Distribution:")
    for guesses in sorted(stats['guess_distribution'].keys()):
        count = stats['guess_distribution'][guesses]
        percentage = (count / stats['successful']) * 100
        bar = '█' * int(percentage / 2)
        print(f"   {guesses} guesses:  {count:4d} ({percentage:5.2f}%) {bar}")
    
    print(f"\n{'='*70}\n")


def generate_visualizations(results, stats, output_dir='dfs_test_results'):
    """Generate comprehensive visualizations"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    successful = [r for r in results if r['success']]
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    
    print(f"\n{'='*70}")
    print(f"🎨 GENERATING VISUALIZATIONS")
    print(f"{'='*70}\n")
    
    # 1. Guess Distribution Histogram
    print("1. Generating guess distribution histogram...")
    fig, ax = plt.subplots(figsize=(12, 7))
    guesses = [r['total_guesses'] for r in successful]
    counts = Counter(guesses)
    
    bars = ax.bar(counts.keys(), counts.values(), color='#FFB6C1', 
                  edgecolor='black', alpha=0.7, width=0.6)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}\n({height/len(successful)*100:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Add mean line
    mean_guesses = stats['guesses']['mean']
    ax.axvline(mean_guesses, color='red', linestyle='--', linewidth=2,
               label=f'Mean: {mean_guesses:.2f}')
    
    # Add median line
    median_guesses = stats['guesses']['median']
    ax.axvline(median_guesses, color='green', linestyle='--', linewidth=2,
               label=f'Median: {median_guesses:.1f}')
    
    ax.set_xlabel('Number of Guesses', fontsize=13, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax.set_title('DFS Algorithm - Guess Distribution (1000 Tests)', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    path1 = os.path.join(output_dir, f'guess_distribution_{timestamp}.png')
    plt.savefig(path1, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path1}")
    plt.close()
    
    # 2. Expanded Nodes Distribution
    print("2. Generating expanded nodes distribution...")
    fig, ax = plt.subplots(figsize=(12, 7))
    nodes = [r['expanded_nodes'] for r in successful]
    
    ax.hist(nodes, bins=30, color='#FFB6C1', edgecolor='black', alpha=0.7)
    
    # Add statistics lines
    mean_nodes = stats['nodes']['mean']
    median_nodes = stats['nodes']['median']
    ax.axvline(mean_nodes, color='red', linestyle='--', linewidth=2,
               label=f'Mean: {mean_nodes:.2f}')
    ax.axvline(median_nodes, color='green', linestyle='--', linewidth=2,
               label=f'Median: {median_nodes:.1f}')
    
    ax.set_xlabel('Number of Expanded Nodes', fontsize=13, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax.set_title('DFS Algorithm - Expanded Nodes Distribution', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    path2 = os.path.join(output_dir, f'nodes_distribution_{timestamp}.png')
    plt.savefig(path2, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path2}")
    plt.close()
    
    # 3. Execution Time Distribution
    print("3. Generating execution time distribution...")
    fig, ax = plt.subplots(figsize=(12, 7))
    times = [r['execution_time'] for r in successful]
    
    ax.hist(times, bins=30, color='#87CEEB', edgecolor='black', alpha=0.7)
    
    mean_time = stats['time']['mean']
    median_time = stats['time']['median']
    ax.axvline(mean_time, color='red', linestyle='--', linewidth=2,
               label=f'Mean: {mean_time:.4f}s')
    ax.axvline(median_time, color='green', linestyle='--', linewidth=2,
               label=f'Median: {median_time:.4f}s')
    
    ax.set_xlabel('Execution Time (seconds)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax.set_title('DFS Algorithm - Execution Time Distribution', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    path3 = os.path.join(output_dir, f'time_distribution_{timestamp}.png')
    plt.savefig(path3, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path3}")
    plt.close()
    
    # 4. Box Plots Comparison
    print("4. Generating box plots comparison...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Guesses box plot
    bp1 = axes[0].boxplot([guesses], patch_artist=True, showmeans=True,
                           meanline=True, widths=0.5)
    bp1['boxes'][0].set_facecolor('#FFB6C1')
    axes[0].set_ylabel('Number of Guesses', fontsize=12, fontweight='bold')
    axes[0].set_title('Guesses Distribution', fontsize=13, fontweight='bold')
    axes[0].set_xticklabels(['DFS'], fontsize=11)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Nodes box plot
    bp2 = axes[1].boxplot([nodes], patch_artist=True, showmeans=True,
                           meanline=True, widths=0.5)
    bp2['boxes'][0].set_facecolor('#FFB6C1')
    axes[1].set_ylabel('Expanded Nodes', fontsize=12, fontweight='bold')
    axes[1].set_title('Expanded Nodes Distribution', fontsize=13, fontweight='bold')
    axes[1].set_xticklabels(['DFS'], fontsize=11)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # Time box plot
    bp3 = axes[2].boxplot([times], patch_artist=True, showmeans=True,
                           meanline=True, widths=0.5)
    bp3['boxes'][0].set_facecolor('#87CEEB')
    axes[2].set_ylabel('Execution Time (s)', fontsize=12, fontweight='bold')
    axes[2].set_title('Execution Time Distribution', fontsize=13, fontweight='bold')
    axes[2].set_xticklabels(['DFS'], fontsize=11)
    axes[2].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    path4 = os.path.join(output_dir, f'boxplots_comparison_{timestamp}.png')
    plt.savefig(path4, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path4}")
    plt.close()
    
    # 5. Scatter Plot: Nodes vs Guesses
    print("5. Generating nodes vs guesses scatter plot...")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(guesses, nodes, alpha=0.5, s=50, c='#FFB6C1', 
               edgecolors='black', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(guesses, nodes, 1)
    p = np.poly1d(z)
    ax.plot(sorted(guesses), p(sorted(guesses)), "r--", linewidth=2, 
            label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}')
    
    ax.set_xlabel('Number of Guesses', fontsize=13, fontweight='bold')
    ax.set_ylabel('Expanded Nodes', fontsize=13, fontweight='bold')
    ax.set_title('DFS Algorithm - Expanded Nodes vs Guesses', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    path5 = os.path.join(output_dir, f'nodes_vs_guesses_{timestamp}.png')
    plt.savefig(path5, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path5}")
    plt.close()
    
    # 6. Scatter Plot: Time vs Guesses
    print("6. Generating time vs guesses scatter plot...")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(guesses, times, alpha=0.5, s=50, c='#87CEEB',
               edgecolors='black', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(guesses, times, 1)
    p = np.poly1d(z)
    ax.plot(sorted(guesses), p(sorted(guesses)), "r--", linewidth=2,
            label=f'Trend: y={z[0]:.4f}x+{z[1]:.4f}')
    
    ax.set_xlabel('Number of Guesses', fontsize=13, fontweight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontsize=13, fontweight='bold')
    ax.set_title('DFS Algorithm - Execution Time vs Guesses', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    path6 = os.path.join(output_dir, f'time_vs_guesses_{timestamp}.png')
    plt.savefig(path6, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path6}")
    plt.close()
    
    # 7. Summary Statistics Table
    print("7. Generating summary statistics table...")
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    
    table_data = [
        ['Metric', 'Value'],
        ['', ''],
        ['Total Tests', f"{stats['total_tests']:,}"],
        ['Successful Tests', f"{stats['successful']:,}"],
        ['Success Rate', f"{stats['success_rate']:.2f}%"],
        ['Win Rate (≤6 guesses)', f"{stats['win_rate_6']:.2f}%"],
        ['', ''],
        ['Mean Guesses', f"{stats['guesses']['mean']:.2f}"],
        ['Median Guesses', f"{stats['guesses']['median']:.1f}"],
        ['Std Dev Guesses', f"{stats['guesses']['std']:.2f}"],
        ['Min-Max Guesses', f"{stats['guesses']['min']} - {stats['guesses']['max']}"],
        ['', ''],
        ['Mean Nodes', f"{stats['nodes']['mean']:.2f}"],
        ['Median Nodes', f"{stats['nodes']['median']:.1f}"],
        ['Std Dev Nodes', f"{stats['nodes']['std']:.2f}"],
        ['Min-Max Nodes', f"{stats['nodes']['min']} - {stats['nodes']['max']}"],
        ['', ''],
        ['Mean Time', f"{stats['time']['mean']:.4f}s"],
        ['Median Time', f"{stats['time']['median']:.4f}s"],
        ['Total Time', f"{stats['time']['total']:.2f}s"],
    ]
    
    table = ax.table(cellText=table_data, cellLoc='left', loc='center',
                     colWidths=[0.4, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    
    # Style header
    table[(0, 0)].set_facecolor('#4472C4')
    table[(0, 1)].set_facecolor('#4472C4')
    table[(0, 0)].set_text_props(weight='bold', color='white', size=13)
    table[(0, 1)].set_text_props(weight='bold', color='white', size=13)
    
    # Style section separators
    for i in [1, 6, 11, 16]:
        table[(i, 0)].set_facecolor('#E7E6E6')
        table[(i, 1)].set_facecolor('#E7E6E6')
    
    # Style data rows
    for i in range(2, len(table_data)):
        if i not in [1, 6, 11, 16]:
            if i % 2 == 0:
                table[(i, 0)].set_facecolor('#F2F2F2')
                table[(i, 1)].set_facecolor('#F2F2F2')
    
    plt.title('DFS Algorithm - Summary Statistics', 
              fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    path7 = os.path.join(output_dir, f'summary_table_{timestamp}.png')
    plt.savefig(path7, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path7}")
    plt.close()
    
    print(f"\n{'='*70}")
    print(f"✅ ALL VISUALIZATIONS SAVED TO: {output_dir}/")
    print(f"{'='*70}\n")


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("🎯 DFS ALGORITHM COMPREHENSIVE TESTING")
    print("="*70)
    
    # Check required packages
    try:
        import matplotlib
        import seaborn
        import tqdm
        print("✅ All required packages found")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Install with: pip install matplotlib seaborn tqdm")
        return
    
    # Run tests
    results, failed = run_dfs_tests(num_tests=1000)
    
    # Calculate statistics
    stats = calculate_statistics(results)
    
    if stats:
        # Print statistics
        print_statistics(stats)
        
        # Save results
        save_results(results, stats)
        
        # Generate visualizations
        generate_visualizations(results, stats)
        
        print("\n✅ Testing complete!")
        print(f"📊 Total time: {stats['time']['total']:.2f}s")
        print(f"⚡ Average time per test: {stats['time']['mean']:.4f}s")
        
        if failed:
            print(f"\n⚠️  {len(failed)} tests failed")
    else:
        print("\n❌ No successful tests to analyze")


if __name__ == "__main__":
    main()
