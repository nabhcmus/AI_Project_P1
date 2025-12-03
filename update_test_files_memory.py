"""
Script to update all test files to include memory usage tracking
This will update test_bfs_detailed.py, test_dfs_detailed.py, and test_astar_detailed.py
"""

import re

def update_test_file(filepath, algorithm_name):
    """Update a single test file to include memory usage"""
    print(f"\n{'='*60}")
    print(f"Updating {filepath}...")
    print(f"{'='*60}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add memory_usage to test function return
    pattern1 = r"(expanded_nodes = solver\.expanded_nodes)"
    replacement1 = r"\1\n            memory_usage = getattr(solver, 'memory_usage', 0)"
    content = re.sub(pattern1, replacement1, content)
    
    pattern2 = r"('execution_time': elapsed,)"
    replacement2 = r"\1\n                'memory_usage': memory_usage,"
    content = re.sub(pattern2, replacement2, content)
    
    # 2. Add memory to calculate_statistics
    pattern3 = r"(times = \[r\['execution_time'\] for r in successful\])"
    replacement3 = r"\1\n    memory = [r.get('memory_usage', 0) for r in successful]"
    content = re.sub(pattern3, replacement3, content)
    
    # 3. Add memory stats section
    pattern4 = r"(# Time statistics\s+'\''time'\'':.+?'total': np\.sum\(times\)\s+},)"
    replacement4 = r"\1\n        \n        # Memory statistics\n        'memory': {\n            'mean': np.mean(memory),\n            'median': np.median(memory),\n            'std': np.std(memory),\n            'min': np.min(memory),\n            'max': np.max(memory),\n            'total': np.sum(memory)\n        },"
    content = re.sub(pattern4, replacement4, content, flags=re.DOTALL)
    
    # 4. Update CSV fieldnames
    pattern5 = r"(fieldnames = \['target_word', 'success', 'total_guesses', 'expanded_nodes',\s+)'execution_time'"
    replacement5 = r"\1'execution_time', 'memory_usage'"
    content = re.sub(pattern5, replacement5, content)
    
    # 5. Add memory_usage to CSV writer
    pattern6 = r"('execution_time': f\"\{r\['execution_time'\]:.6f\}\",)"
    replacement6 = r"\1\n                    'memory_usage': r.get('memory_usage', 0),"
    content = re.sub(pattern6, replacement6, content)
    
    # 6. Add memory print section to print_statistics
    pattern7 = r"(print\(f\"\\n⏱️  Execution Time Statistics:\"\).+?print\(f\"   Total Time:.+?\"\))"
    replacement7 = r"""\1
    
    # Format memory intelligently
    def format_memory(bytes_val):
        if bytes_val < 1024:
            return f"{bytes_val:.0f} bytes"
        elif bytes_val < 1024 * 1024:
            return f"{bytes_val / 1024:.2f} KB"
        else:
            return f"{bytes_val / (1024 * 1024):.2f} MB"
    
    print(f"\\n💾 Memory Usage Statistics:")
    print(f"   Mean:             {format_memory(stats['memory']['mean'])}")
    print(f"   Median:           {format_memory(stats['memory']['median'])}")
    print(f"   Std Dev:          {format_memory(stats['memory']['std'])}")
    print(f"   Min - Max:        {format_memory(stats['memory']['min'])} - {format_memory(stats['memory']['max'])}")
    print(f"   Total:            {format_memory(stats['memory']['total'])}")"""
    content = re.sub(pattern7, replacement7, content, flags=re.DOTALL)
    
    # 7. Update box plots from 3 to 4 subplots
    pattern8 = r"fig, axes = plt\.subplots\(1, 3, figsize=\(18, 6\)\)"
    replacement8 = r"fig, axes = plt.subplots(1, 4, figsize=(22, 6))"
    content = re.sub(pattern8, replacement8, content)
    
    # 8. Add memory visualization after time distribution
    pattern9 = r"(path3 = os\.path\.join\(output_dir, f'time_distribution_\{timestamp\}\.png'\)\s+plt\.savefig\(path3,.+?plt\.close\(\))"
    replacement9 = r"""\1
    
    # 4. Memory Usage Distribution
    print("4. Generating memory usage distribution...")
    fig, ax = plt.subplots(figsize=(12, 7))
    memory = [r.get('memory_usage', 0) for r in successful]
    memory_kb = [m / 1024 for m in memory]  # Convert to KB for better visualization
    
    ax.hist(memory_kb, bins=30, color='#9370DB', edgecolor='black', alpha=0.7)
    
    mean_mem = stats['memory']['mean'] / 1024
    median_mem = stats['memory']['median'] / 1024
    ax.axvline(mean_mem, color='red', linestyle='--', linewidth=2,
               label=f'Mean: {mean_mem:.2f} KB')
    ax.axvline(median_mem, color='green', linestyle='--', linewidth=2,
               label=f'Median: {median_mem:.2f} KB')
    
    ax.set_xlabel('Memory Usage (KB)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax.set_title(f'""" + algorithm_name + r""" Algorithm - Memory Usage Distribution', 
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    path4 = os.path.join(output_dir, f'memory_distribution_{timestamp}.png')
    plt.savefig(path4, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path4}")
    plt.close()"""
    content = re.sub(pattern9, replacement9, content, flags=re.DOTALL)
    
    # 9. Add memory box plot before closing boxplots section
    pattern10 = r"(axes\[2\]\.grid\(True, alpha=0\.3, axis='y'\)\s+)(plt\.tight_layout\(\)\s+path\d+ = os\.path\.join)"
    replacement10 = r"""\1
    # Memory box plot
    memory_kb = [m / 1024 for m in memory]
    bp4 = axes[3].boxplot([memory_kb], patch_artist=True, showmeans=True,
                           meanline=True, widths=0.5)
    bp4['boxes'][0].set_facecolor('#9370DB')
    axes[3].set_ylabel('Memory Usage (KB)', fontsize=12, fontweight='bold')
    axes[3].set_title('Memory Usage Distribution', fontsize=13, fontweight='bold')
    axes[3].set_xticklabels([label], fontsize=10)
    axes[3].grid(True, alpha=0.3, axis='y')
    
    \2"""
    content = re.sub(pattern10, replacement10, content)
    
    # 10. Update summary table to include memory
    pattern11 = r"(\['Total Time', f\"\{stats\['time'\]\['total'\]:.2f\}s\"\],\s+\])"
    replacement11 = r"""['Total Time', f"{stats['time']['total']:.2f}s"],
        ['', ''],
        ['Mean Memory', format_memory(stats['memory']['mean'])],
        ['Median Memory', format_memory(stats['memory']['median'])],
        ['Total Memory', format_memory(stats['memory']['total'])],
    ]
    
    # Format memory function for table
    def format_memory(bytes_val):
        if bytes_val < 1024:
            return f"{bytes_val:.0f} bytes"
        elif bytes_val < 1024 * 1024:
            return f"{bytes_val / 1024:.2f} KB"
        else:
            return f"{bytes_val / (1024 * 1024):.2f} MB"}"""
    content = re.sub(pattern11, replacement11, content)
    
    # 11. Update section separators in table
    pattern12 = r"for i in \[1, 7, 12, 17\]:"
    replacement12 = r"for i in [1, 7, 12, 17, 21]:"
    content = re.sub(pattern12, replacement12, content)
    
    pattern13 = r"if i not in \[1, 7, 12, 17\]:"
    replacement13 = r"if i not in [1, 7, 12, 17, 21]:"
    content = re.sub(pattern13, replacement13, content)
    
    # 12. Update plot numbering (shift 4->5, 5->6, 6->7, 7->8)
    content = re.sub(r'# 4\. Box Plots Comparison', r'# 5. Box Plots Comparison', content)
    content = re.sub(r'print\("4\. Generating box plots', r'print("5. Generating box plots', content)
    content = re.sub(r'# 5\. Scatter Plot: Nodes vs Guesses', r'# 6. Scatter Plot: Nodes vs Guesses', content)
    content = re.sub(r'print\("5\. Generating nodes vs guesses', r'print("6. Generating nodes vs guesses', content)
    content = re.sub(r'# 6\. Scatter Plot: Time vs Guesses', r'# 7. Scatter Plot: Time vs Guesses', content)
    content = re.sub(r'print\("6\. Generating time vs guesses', r'print("7. Generating time vs guesses', content)
    content = re.sub(r'# 7\. Summary Statistics Table', r'# 8. Summary Statistics Table', content)
    content = re.sub(r'print\("7\. Generating summary', r'print("8. Generating summary', content)
    
    # Update path variables
    content = re.sub(r"path4 = os\.path\.join\(output_dir, f'boxplots_comparison", 
                    r"path5 = os.path.join(output_dir, f'boxplots_comparison", content)
    content = re.sub(r"path5 = os\.path\.join\(output_dir, f'nodes_vs_guesses", 
                    r"path6 = os.path.join(output_dir, f'nodes_vs_guesses", content)
    content = re.sub(r"path6 = os\.path\.join\(output_dir, f'time_vs_guesses", 
                    r"path7 = os.path.join(output_dir, f'time_vs_guesses", content)
    content = re.sub(r"path7 = os\.path\.join\(output_dir, f'summary_table", 
                    r"path8 = os.path.join(output_dir, f'summary_table", content)
    
    # Update print statements for path
    content = re.sub(r'print\(f"   ✅ Saved: \{path4\}"\)\s+plt\.close\(\)\s+# 5\. Scatter', 
                    r'print(f"   ✅ Saved: {path5}")\n    plt.close()\n    \n    # 6. Scatter', content)
    content = re.sub(r'print\(f"   ✅ Saved: \{path5\}"\)\s+plt\.close\(\)\s+# 6\. Scatter', 
                    r'print(f"   ✅ Saved: {path6}")\n    plt.close()\n    \n    # 7. Scatter', content)
    content = re.sub(r'print\(f"   ✅ Saved: \{path6\}"\)\s+plt\.close\(\)\s+# 7\. Summary', 
                    r'print(f"   ✅ Saved: {path7}")\n    plt.close()\n    \n    # 8. Summary', content)
    content = re.sub(r'print\(f"   ✅ Saved: \{path7\}"\)', 
                    r'print(f"   ✅ Saved: {path8}")', content)
    
    # Update summary table size
    content = re.sub(r"fig, ax = plt\.subplots\(figsize=\(12, 8\)\)\s+ax\.axis\('tight'\)\s+ax\.axis\('off'\)\s+table_data = \[", 
                    r"fig, ax = plt.subplots(figsize=(12, 10))\n    ax.axis('tight')\n    ax.axis('off')\n    \n    table_data = [", content)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filepath}")

# Update all test files
files_to_update = [
    ('Testing/test_bfs_detailed.py', 'BFS'),
    ('Testing/test_dfs_detailed.py', 'DFS'),
    ('Testing/test_astar_detailed.py', 'A*')
]

print("\n" + "="*60)
print("Memory Usage Update Script")
print("="*60)

for filepath, algo_name in files_to_update:
    try:
        update_test_file(filepath, algo_name)
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")

print("\n" + "="*60)
print("✅ All test files updated successfully!")
print("="*60)
