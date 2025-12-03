"""
Quick Copy-Paste Snippets for Updating Test Files
Use these snippets to manually update test_bfs_detailed.py, test_dfs_detailed.py, test_astar_detailed.py
"""

print("""
================================================================================
SNIPPET 1: Add to test_xxx_single() function (after expanded_nodes line)
================================================================================
""")

snippet1 = """            memory_usage = getattr(solver, 'memory_usage', 0)"""

print(snippet1)

print("""
================================================================================
SNIPPET 2: Add to return dict in test_xxx_single() (after 'execution_time')
================================================================================
""")

snippet2 = """                'memory_usage': memory_usage,"""

print(snippet2)

print("""
================================================================================
SNIPPET 3: Add to calculate_statistics() (after times = ...)
================================================================================
""")

snippet3 = """    memory = [r.get('memory_usage', 0) for r in successful]"""

print(snippet3)

print("""
================================================================================
SNIPPET 4: Add to stats dict in calculate_statistics() (after 'time' section)
================================================================================
""")

snippet4 = """        
        # Memory statistics
        'memory': {
            'mean': np.mean(memory),
            'median': np.median(memory),
            'std': np.std(memory),
            'min': np.min(memory),
            'max': np.max(memory),
            'total': np.sum(memory)
        },"""

print(snippet4)

print("""
================================================================================
SNIPPET 5: Update CSV fieldnames in save_results()
================================================================================
CHANGE FROM:
        fieldnames = ['target_word', 'success', 'total_guesses', 'expanded_nodes', 
                     'execution_time', 'won_in_6', 'solution_path']

TO:
        fieldnames = ['target_word', 'success', 'total_guesses', 'expanded_nodes', 
                     'execution_time', 'memory_usage', 'won_in_6', 'solution_path']
""")

print("""
================================================================================
SNIPPET 6: Add to CSV writerow in save_results() (after 'execution_time')
================================================================================
""")

snippet6 = """                    'memory_usage': r.get('memory_usage', 0),"""

print(snippet6)

print("""
================================================================================
SNIPPET 7: Add to print_statistics() (after time statistics section)
================================================================================
""")

snippet7 = """    
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

print(snippet7)

print("""
================================================================================
SNIPPET 8: Update box plots in generate_visualizations()
================================================================================
CHANGE:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

TO:
    fig, axes = plt.subplots(1, 4, figsize=(22, 6))
""")

print("""
================================================================================
SNIPPET 9: Add memory box plot (after time box plot, before plt.tight_layout())
================================================================================
""")

snippet9 = """    
    # Memory box plot
    memory_kb = [m / 1024 for m in memory]
    bp4 = axes[3].boxplot([memory_kb], patch_artist=True, showmeans=True,
                           meanline=True, widths=0.5)
    bp4['boxes'][0].set_facecolor('#9370DB')
    axes[3].set_ylabel('Memory Usage (KB)', fontsize=12, fontweight='bold')
    axes[3].set_title('Memory Usage Distribution', fontsize=13, fontweight='bold')
    axes[3].set_xticklabels([label], fontsize=10)
    axes[3].grid(True, alpha=0.3, axis='y')"""

print(snippet9)

print("""
================================================================================
SNIPPET 10: Add memory distribution plot (after time distribution, before box plots)
         NOTE: Replace 'XXX' with algorithm name (BFS, DFS, or A*)
================================================================================
""")

snippet10 = """    
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
    ax.set_title(f'XXX Algorithm - Memory Usage Distribution',  # CHANGE XXX to BFS/DFS/A*
                 fontsize=15, fontweight='bold', pad=15)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    path4 = os.path.join(output_dir, f'memory_distribution_{timestamp}.png')
    plt.savefig(path4, dpi=300, bbox_inches='tight')
    print(f"   ✅ Saved: {path4}")
    plt.close()"""

print(snippet10)

print("""
================================================================================
SNIPPET 11: Update plot numbers after adding memory distribution
================================================================================
After adding memory plot as #4, update numbering:
- "# 4. Box Plots"         -> "# 5. Box Plots"
- "# 5. Scatter: Nodes"    -> "# 6. Scatter: Nodes"
- "# 6. Scatter: Time"     -> "# 7. Scatter: Time"
- "# 7. Summary Table"     -> "# 8. Summary Table"

Also update path variables:
- path4 (boxplots)   -> path5
- path5 (nodes)      -> path6
- path6 (time)       -> path7
- path7 (summary)    -> path8

And update print statements:
- print("4. ...") -> print("5. ...")
- print("5. ...") -> print("6. ...")
- etc.
""")

print("""
================================================================================
SNIPPET 12: Add memory to summary table (after time section)
================================================================================
""")

snippet12 = """        ['', ''],
        ['Mean Memory', format_memory(stats['memory']['mean'])],
        ['Median Memory', format_memory(stats['memory']['median'])],
        ['Total Memory', format_memory(stats['memory']['total'])],"""

print(snippet12)

print("""
AND add format_memory function before table_data:
""")

snippet12b = """    # Format memory for display
    def format_memory(bytes_val):
        if bytes_val < 1024:
            return f"{bytes_val:.0f} bytes"
        elif bytes_val < 1024 * 1024:
            return f"{bytes_val / 1024:.2f} KB"
        else:
            return f"{bytes_val / (1024 * 1024):.2f} MB"
"""

print(snippet12b)

print("""
================================================================================
SNIPPET 13: Update table section separators
================================================================================
CHANGE:
    for i in [1, 7, 12, 17]:

TO:
    for i in [1, 7, 12, 17, 21]:

AND:
    if i not in [1, 7, 12, 17]:

TO:
    if i not in [1, 7, 12, 17, 21]:
""")

print("""
================================================================================
SNIPPET 14: Update summary table size
================================================================================
CHANGE:
    fig, ax = plt.subplots(figsize=(12, 8))

TO:
    fig, ax = plt.subplots(figsize=(12, 10))
""")

print("""
================================================================================
                            DONE! 
================================================================================
After applying all snippets, your test file will have complete memory tracking!

Test by running:
    python Testing/test_xxx_detailed.py

Check that:
1. Memory values appear in console output
2. memory_usage column exists in CSV
3. Memory distribution plot is generated  
4. Box plots show 4 subplots (including memory)
5. Summary table includes memory statistics

================================================================================
""")
