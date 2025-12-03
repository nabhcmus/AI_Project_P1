import time
import sys
import os
import json
import csv
import random
from datetime import datetime
from collections import defaultdict
import numpy as np


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from words_api import Words
from Search_Algorithm.bfs import BFSSolver
from Search_Algorithm.dfs import DFSSolver
from Search_Algorithm.astar import AStarSolver
from Search_Algorithm.entropy_best_first import EntropySolver


class TestWordAPI:
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
        
        
        for i in range(len(self.word)):
            if guess_list[i] == secret_list[i]:
                feedback.append('G')
                secret_list[i] = '
                guess_list[i] = '$'
            else:
                feedback.append('')
        
        
        for i in range(len(self.word)):
            if guess_list[i] != '$' and guess_list[i] in secret_list:
                feedback[i] = 'Y'
                secret_list[secret_list.index(guess_list[i])] = '
        
        
        for i in range(len(self.word)):
            if feedback[i] == '':
                feedback[i] = 'X'
        
        return feedback


def test_bfs_single(target_word=None, word_size=5):
    word_api = TestWordAPI(word_size, target_word)
    solver = BFSSolver(word_api)
    
    start_time = time.time()
    try:
        solution = solver.solve(board_state=[])
        execution_time = time.time() - start_time
        
        stats = solver.get_stats()
        
        return {
            'algorithm': 'BFS',
            'target': word_api.word,
            'success': True,
            'total_guesses': len(solver.winning_path),
            'expanded_nodes': solver.expanded_nodes,
            'max_queue_size': solver.max_queue_size,
            'execution_time': round(execution_time, 4),
            'solution_path': solver.winning_path,
            'status': stats.get('Status', 'Win')
        }
    except Exception as e:
        return {
            'algorithm': 'BFS',
            'target': word_api.word,
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }


def test_dfs_single(target_word=None, word_size=5):
    """Test DFS với một target word"""
    word_api = TestWordAPI(word_size, target_word)
    solver = DFSSolver(word_api)
    
    start_time = time.time()
    try:
        solution = solver.solve(board_state=[])
        execution_time = time.time() - start_time
        
        stats = solver.get_stats()
        
        return {
            'algorithm': 'DFS',
            'target': word_api.word,
            'success': True,
            'total_guesses': solver.total_guesses,
            'expanded_nodes': solver.expanded_nodes,
            'execution_time': round(execution_time, 4),
            'solution_path': solver.full_solution_path,
            'memory_usage_kb': solver.memory_usage / 1024,
            'status': stats.get('Status', 'Win')
        }
    except Exception as e:
        return {
            'algorithm': 'DFS',
            'target': word_api.word,
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }


def test_astar_single(target_word=None, word_size=5):
    word_api = TestWordAPI(word_size, target_word)
    
    start_time = time.time()
    try:
        solver = AStarSolver(word_api)
        solution = solver.solve(board_state=[])
        execution_time = time.time() - start_time
        
        stats = solver.get_stats()
        
        return {
            'algorithm': 'A*',
            'target': word_api.word,
            'success': True,
            'total_guesses': len(solver.guesses_history),
            'expanded_nodes': solver.expanded_nodes,
            'execution_time': round(execution_time, 4),
            'solution_path': solver.guesses_history,
            'max_memory': len(solver.full_dictionary),
            'status': 'Win' if len(solver.candidates_indices) > 0 else 'Failed'
        }
    except FileNotFoundError as e:
        
        return {
            'algorithm': 'A*',
            'target': word_api.word,
            'success': False,
            'error': f'Missing required file: {str(e)}',
            'execution_time': 0,
            'skip': True
        }
    except Exception as e:
        return {
            'algorithm': 'A*',
            'target': word_api.word,
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }


def test_entropy_single(target_word=None, word_size=5, hard_mode=True):
    word_api = TestWordAPI(word_size, target_word)
    
    start_time = time.time()
    try:
        solver = EntropySolver(word_api)
        solution = solver.solve(board_state=None, hard_mode=hard_mode)
        execution_time = time.time() - start_time
        
        stats = solver.get_stats()
        
        return {
            'algorithm': 'Entropy',
            'target': word_api.word,
            'success': True,
            'total_guesses': len(solver.solution_path),
            'expanded_nodes': solver.expanded_nodes,
            'execution_time': round(execution_time, 4),
            'solution_path': solver.solution_path,
            'hard_mode': hard_mode,
            'status': stats.get('Status', 'Win')
        }
    except FileNotFoundError as e:
        return {
            'algorithm': 'Entropy',
            'target': word_api.word if 'word_api' in locals() else 'N/A',
            'success': False,
            'error': 'pattern_matrix.npy not found',
            'execution_time': time.time() - start_time
        }
    except Exception as e:
        return {
            'algorithm': 'Entropy',
            'target': word_api.word,
            'success': False,
            'error': str(e),
            'execution_time': time.time() - start_time
        }


def run_algorithm_tests(algorithm_name, test_function, num_tests=1000, **kwargs):
    print(f"\n{'='*70}")
    print(f"🚀 TESTING {algorithm_name.upper()} - {num_tests} RUNS")
    print(f"{'='*70}")
    
    results = []
    successful_tests = 0
    failed_tests = 0
    
    start_total = time.time()
    
    for i in range(1, num_tests + 1):
        
        if i % 10 == 0 or i == 1:
            progress = i / num_tests * 100
            bar_length = 50
            filled = int(bar_length * i / num_tests)
            bar = '█' * filled + '-' * (bar_length - filled)
            print(f'\r[{bar}] {progress:.1f}% ({i}/{num_tests})', end='', flush=True)
        
        result = test_function(**kwargs)
        
        
        if result.get('skip', False):
            print(f"\n\nSKIPPED: {algorithm_name}")
            print(f"   Reason: {result.get('error', 'Missing required files')}")
            print(f"   Hint: Run precompute script to generate required files")
            return None
        
        results.append(result)
        
        if result.get('success', False):
            successful_tests += 1
        else:
            failed_tests += 1
    
    total_time = time.time() - start_total
    
    print(f'\n\n✅ Completed {num_tests} tests in {total_time:.2f}s')
    print(f'   Success: {successful_tests} | Failed: {failed_tests}')
    
    return results


def calculate_statistics(results):
    successful_results = [r for r in results if r.get('success', False)]
    
    if not successful_results:
        return None
    
    guesses = [r['total_guesses'] for r in successful_results]
    times = [r['execution_time'] for r in successful_results]
    nodes = [r['expanded_nodes'] for r in successful_results]
    
    
    wins_in_6 = sum(1 for g in guesses if g <= 6)
    win_rate_6 = wins_in_6 / len(results) * 100
    
    stats = {
        'total_tests': len(results),
        'successful_tests': len(successful_results),
        'failed_tests': len(results) - len(successful_results),
        'success_rate': len(successful_results) / len(results) * 100,
        'win_rate_6': win_rate_6,
        'wins_in_6': wins_in_6,
        
        
        'guesses': {
            'mean': np.mean(guesses),
            'median': np.median(guesses),
            'std': np.std(guesses),
            'min': np.min(guesses),
            'max': np.max(guesses),
            'q25': np.percentile(guesses, 25),
            'q75': np.percentile(guesses, 75)
        },
        
        
        'time': {
            'mean': np.mean(times),
            'median': np.median(times),
            'std': np.std(times),
            'min': np.min(times),
            'max': np.max(times),
            'total': np.sum(times)
        },
        
        
        'nodes': {
            'mean': np.mean(nodes),
            'median': np.median(nodes),
            'std': np.std(nodes),
            'min': np.min(nodes),
            'max': np.max(nodes)
        },
        
        
        'guess_distribution': dict(zip(*np.unique(guesses, return_counts=True)))
    }
    
    return stats


def print_statistics(algorithm_name, stats):
    """In ra thống kê đẹp"""
    print(f"\n{'='*70}")
    print(f"{algorithm_name.upper()} STATISTICS")
    print(f"{'='*70}")
    
    if not stats:
        print("No successful tests to analyze!")
        return
    
    print(f"\nSUCCESS RATE:")
    print(f"   Total tests: {stats['total_tests']}")
    print(f"   Successful: {stats['successful_tests']}")
    print(f"   Failed: {stats['failed_tests']}")
    print(f"   Success rate: {stats['success_rate']:.2f}%")
    
    print(f"\nWORDLE WIN RATE (≤6 guesses):")
    print(f"   Wins in 6: {stats['wins_in_6']}/{stats['total_tests']}")
    print(f"   Win rate: {stats['win_rate_6']:.2f}%")
    
    print(f"\nGUESSES STATISTICS:")
    print(f"   Mean:   {stats['guesses']['mean']:.2f}")
    print(f"   Median: {stats['guesses']['median']:.2f}")
    print(f"   Std:    {stats['guesses']['std']:.2f}")
    print(f"   Min:    {stats['guesses']['min']}")
    print(f"   Max:    {stats['guesses']['max']}")
    print(f"   Q25:    {stats['guesses']['q25']:.2f}")
    print(f"   Q75:    {stats['guesses']['q75']:.2f}")
    
    print(f"\nTIME STATISTICS (seconds):")
    print(f"   Mean:   {stats['time']['mean']:.4f}s")
    print(f"   Median: {stats['time']['median']:.4f}s")
    print(f"   Std:    {stats['time']['std']:.4f}s")
    print(f"   Min:    {stats['time']['min']:.4f}s")
    print(f"   Max:    {stats['time']['max']:.4f}s")
    print(f"   Total:  {stats['time']['total']:.2f}s")
    
    print(f"\nEXPANDED NODES STATISTICS:")
    print(f"   Mean:   {stats['nodes']['mean']:.2f}")
    print(f"   Median: {stats['nodes']['median']:.2f}")
    print(f"   Std:    {stats['nodes']['std']:.2f}")
    print(f"   Min:    {stats['nodes']['min']}")
    print(f"   Max:    {stats['nodes']['max']}")
    
    print(f"\nGUESS DISTRIBUTION:")
    for guesses in sorted(stats['guess_distribution'].keys()):
        count = stats['guess_distribution'][guesses]
        percentage = count / stats['successful_tests'] * 100
        bar = '█' * int(percentage / 2)
        print(f"   {guesses:2d} guesses: {count:4d} ({percentage:5.2f}%) {bar}")


def save_results_to_csv(results, filename):
    if not results:
        return
    
    successful_results = [r for r in results if r.get('success', False)]
    
    if not successful_results:
        print(f"No successful results to save for {filename}")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        
        fieldnames = ['run_number', 'target', 'total_guesses', 'expanded_nodes', 
                     'execution_time', 'status', 'solution_length']
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, result in enumerate(successful_results, 1):
            row = {
                'run_number': i,
                'target': result['target'],
                'total_guesses': result['total_guesses'],
                'expanded_nodes': result['expanded_nodes'],
                'execution_time': result['execution_time'],
                'status': result.get('status', 'Win'),
                'solution_length': len(result.get('solution_path', []))
            }
            writer.writerow(row)
    
    print(f"Saved {len(successful_results)} results to {filename}")


def save_summary_to_json(all_stats, filename):
    def convert_to_native_types(obj):
        if isinstance(obj, dict):
            return {
                (int(k) if isinstance(k, (np.integer, np.int64, np.int32)) else 
                 float(k) if isinstance(k, (np.floating, np.float64, np.float32)) else 
                 str(k) if not isinstance(k, (str, int, float, bool, type(None))) else k): 
                convert_to_native_types(v) 
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [convert_to_native_types(item) for item in obj]
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif hasattr(obj, 'item'):  
            return obj.item()
        else:
            return obj
    
    summary = {
        'timestamp': datetime.now().isoformat(),
        'algorithms': {}
    }
    
    for algo_name, stats in all_stats.items():
        if stats:
            summary['algorithms'][algo_name] = {
                'total_tests': int(stats['total_tests']),
                'success_rate': float(stats['success_rate']),
                'guesses': convert_to_native_types(stats['guesses']),
                'time': convert_to_native_types(stats['time']),
                'nodes': convert_to_native_types(stats['nodes']),
                'distribution': convert_to_native_types(stats['guess_distribution'])
            }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSaved summary to {filename}")


def compare_algorithms(all_stats):
    print(f"\n{'='*70}")
    print(f"ALGORITHM COMPARISON")
    print(f"{'='*70}")
    algorithms = ['BFS', 'DFS', 'A*', 'Entropy-Hard', 'Entropy-Normal']
    print(f"\n{'Metric':<30} {'BFS':<12} {'DFS':<12} {'A*':<12} {'Ent-Hard':<12} {'Ent-Norm':<12}")
    print("-"*90)
    print(f"{'Win Rate ≤6 (%)':<30}", end='')
    for algo in algorithms:
        if algo in all_stats and all_stats[algo]:
            print(f"{all_stats[algo]['win_rate_6']:<12.2f}", end='')
        else:
            print(f"{'N/A':<12}", end='')
    print()
    print(f"{'Success Rate (%)':<30}", end='')
    for algo in algorithms:
        if algo in all_stats and all_stats[algo]:
            print(f"{all_stats[algo]['success_rate']:<12.2f}", end='')
        else:
            print(f"{'N/A':<12}", end='')
    print()
    print(f"{'Mean Guesses':<30}", end='')
    for algo in algorithms:
        if algo in all_stats and all_stats[algo]:
            print(f"{all_stats[algo]['guesses']['mean']:<12.2f}", end='')
        else:
            print(f"{'N/A':<12}", end='')
    print()
    print(f"{'Mean Time (s)':<30}", end='')
    for algo in algorithms:
        if algo in all_stats and all_stats[algo]:
            print(f"{all_stats[algo]['time']['mean']:<12.4f}", end='')
        else:
            print(f"{'N/A':<12}", end='')
    print()
    print(f"{'Mean Expanded Nodes':<30}", end='')
    for algo in algorithms:
        if algo in all_stats and all_stats[algo]:
            print(f"{all_stats[algo]['nodes']['mean']:<12.2f}", end='')
        else:
            print(f"{'N/A':<12}", end='')
    print()
    
    print("\n" + "="*70)


def main():
    print("\n" + "█"*70)
    print("COMPREHENSIVE ALGORITHM TESTING FRAMEWORK")
    print("   Testing: BFS, DFS, A*, Entropy (Hard + Normal)")
    print("   Runs per algorithm: 1000")
    print("█"*70)
    
    
    output_dir = "test_results"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    all_results = {}
    all_stats = {}
    
    
    algorithms = [
        ('BFS', test_bfs_single),
        ('DFS', test_dfs_single),
        ('A*', test_astar_single),
        ('Entropy-Hard', lambda: test_entropy_single(hard_mode=True)),
        ('Entropy-Normal', lambda: test_entropy_single(hard_mode=False))
    ]
    
    for algo_name, test_func in algorithms:
        print(f"\n{'='*70}")
        print(f"Testing {algo_name}...")
        print(f"{'='*70}")
        
        results = run_algorithm_tests(algo_name, test_func, num_tests=1000)
        
        
        if results is None:
            all_results[algo_name] = None
            all_stats[algo_name] = None
            continue
        
        all_results[algo_name] = results
        
        
        stats = calculate_statistics(results)
        all_stats[algo_name] = stats
        
        
        print_statistics(algo_name, stats)
        
        
        safe_algo_name = algo_name.lower().replace('*', 'star').replace(' ', '_')
        
        
        csv_filename = os.path.join(output_dir, f"{safe_algo_name}_{timestamp}.csv")
        save_results_to_csv(results, csv_filename)
        
        
        json_filename = os.path.join(output_dir, f"{safe_algo_name}_{timestamp}_detailed.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Saved detailed results to {json_filename}")
    
    
    compare_algorithms(all_stats)
    
    
    summary_filename = os.path.join(output_dir, f"summary_{timestamp}.json")
    save_summary_to_json(all_stats, summary_filename)
    
    print(f"\n{'='*70}")
    print(f"ALL TESTS COMPLETED!")
    print(f"   Results saved to: {output_dir}/")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
