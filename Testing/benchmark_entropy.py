import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Search_Algorithm.entropy_best_first import EntropySolver
from words_api import Words
import random
import time
from collections import defaultdict
import statistics
import psutil  
import gc
class TestResults:
    def __init__(self):
        self.total_tests = 0
        self.wins = 0
        self.losses = 0
        self.guess_counts = []
        self.times = []
        self.expanded_states = []
        self.guess_distribution = defaultdict(int)  
        self.failed_words = []
        self.all_results = []  
        self.memory_usages = []  
        self.peak_memory = 0  
    def add_result(self, word, guesses, time_taken, expanded, won, memory_mb=0):
        self.total_tests += 1
        if won and guesses <= 6:
            self.wins += 1
        else:
            self.losses += 1
            self.failed_words.append((word, guesses))
        self.guess_counts.append(guesses)
        self.times.append(time_taken)
        self.expanded_states.append(expanded)
        self.guess_distribution[guesses] += 1
        self.all_results.append((word, guesses))
        self.memory_usages.append(memory_mb)
        self.peak_memory = max(self.peak_memory, memory_mb)
    def print_report(self):
        print("\n" + "="*70)
        print("ENTROPY MATRIX SOLVER - BENCHMARK REPORT")
        print("="*70)
        win_guesses = [g for i, g in enumerate(self.guess_counts) 
                       if i < len(self.guess_counts) and 
                       self.guess_counts[i] > 0 and 
                       (i >= len(self.failed_words) or 
                        self.guess_counts[i] <= 6)]
        actual_wins = sum(1 for g in self.guess_counts if g > 0 and g <= 6)
        actual_losses = self.total_tests - actual_wins
        print(f"\nOVERALL STATISTICS")
        print(f"{'Total Tests:':<25} {self.total_tests}")
        print(f"{'Wins (≤6 guesses):':<25} {actual_wins} ({actual_wins/self.total_tests*100:.2f}%)")
        print(f"{'Losses (>6 guesses):':<25} {actual_losses} ({actual_losses/self.total_tests*100:.2f}%)")
        print(f"\nGUESS STATISTICS (All attempts until solved)")
        print(f"{'Average Guesses:':<25} {statistics.mean(self.guess_counts):.2f}")
        print(f"{'Median Guesses:':<25} {statistics.median(self.guess_counts):.1f}")
        print(f"{'Min Guesses:':<25} {min(self.guess_counts)}")
        print(f"{'Max Guesses:':<25} {max(self.guess_counts)}")
        print(f"{'Std Deviation:':<25} {statistics.stdev(self.guess_counts):.2f}")
        print(f"\nGUESS DISTRIBUTION")
        for i in sorted(self.guess_distribution.keys()):
            count = self.guess_distribution[i]
            percentage = count / self.total_tests * 100
            bar = "█" * int(percentage / 2)
            marker = " ✓ Win" if i <= 6 else " ✗ Lose"
            print(f"{i:2d} guesses: {count:3d} ({percentage:5.2f}%) {bar}{marker}")
        
        print(f"\nPERFORMANCE METRICS")
        print(f"{'Average Time:':<25} {statistics.mean(self.times):.4f}s")
        print(f"{'Median Time:':<25} {statistics.median(self.times):.4f}s")
        print(f"{'Min Time:':<25} {min(self.times):.4f}s")
        print(f"{'Max Time:':<25} {max(self.times):.4f}s")
        print(f"{'Total Time:':<25} {sum(self.times):.2f}s")
        
        print(f"\nEXPANDED NODES (Matrix Lookups)")
        print(f"{'Average Nodes:':<25} {statistics.mean(self.expanded_states):.2f}")
        print(f"{'Median Nodes:':<25} {statistics.median(self.expanded_states):.1f}")
        print(f"{'Min Nodes:':<25} {min(self.expanded_states)}")
        print(f"{'Max Nodes:':<25} {max(self.expanded_states)}")
        
        print(f"\nMEMORY USAGE (beyond baseline)")
        print(f"{'Peak Memory:':<25} {self.peak_memory:.2f} MB")
        print(f"{'Average Memory:':<25} {statistics.mean(self.memory_usages):.2f} MB")
        print(f"{'Median Memory:':<25} {statistics.median(self.memory_usages):.2f} MB")
        long_solves = [(guesses, word) for word, guesses in self.all_results if guesses > 6]
        if long_solves:
            long_solves.sort(reverse=True)
            print(f"\nWORDS REQUIRING >6 GUESSES ({len(long_solves)})")
            for guesses, word in long_solves[:10]:
                print(f"   {word}: {guesses} guesses")
            if len(long_solves) > 10:
                print(f"   ... and {len(long_solves) - 10} more")
        
        print("\n" + "="*70)
    
    def save_to_file(self, filename="entropy_matrix_benchmark_results.txt"):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        actual_wins = sum(1 for g in self.guess_counts if g > 0 and g <= 6)
        actual_losses = self.total_tests - actual_wins
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("ENTROPY MATRIX SOLVER - BENCHMARK REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write("OVERALL STATISTICS\n")
            f.write(f"Total Tests: {self.total_tests}\n")
            f.write(f"Wins (≤6 guesses): {actual_wins} ({actual_wins/self.total_tests*100:.2f}%)\n")
            f.write(f"Losses (>6 guesses): {actual_losses} ({actual_losses/self.total_tests*100:.2f}%)\n\n")
            
            f.write("GUESS STATISTICS (All attempts until solved)\n")
            f.write(f"Average Guesses: {statistics.mean(self.guess_counts):.2f}\n")
            f.write(f"Median Guesses: {statistics.median(self.guess_counts):.1f}\n")
            f.write(f"Min Guesses: {min(self.guess_counts)}\n")
            f.write(f"Max Guesses: {max(self.guess_counts)}\n")
            f.write(f"Std Deviation: {statistics.stdev(self.guess_counts):.2f}\n\n")
            
            f.write("GUESS DISTRIBUTION\n")
            for i in sorted(self.guess_distribution.keys()):
                count = self.guess_distribution[i]
                percentage = count / self.total_tests * 100
                marker = " ✓ Win" if i <= 6 else " ✗ Lose"
                f.write(f"{i:2d} guesses: {count:3d} ({percentage:5.2f}%){marker}\n")
            
            f.write("\nPERFORMANCE METRICS\n")
            f.write(f"Average Time: {statistics.mean(self.times):.4f}s\n")
            f.write(f"Median Time: {statistics.median(self.times):.4f}s\n")
            f.write(f"Min Time: {min(self.times):.4f}s\n")
            f.write(f"Max Time: {max(self.times):.4f}s\n")
            f.write(f"Total Time: {sum(self.times):.2f}s\n\n")
            
            f.write("EXPANDED NODES (Matrix Lookups)\n")
            f.write(f"Average Nodes: {statistics.mean(self.expanded_states):.2f}\n")
            f.write(f"Median Nodes: {statistics.median(self.expanded_states):.1f}\n")
            f.write(f"Min Nodes: {min(self.expanded_states)}\n")
            f.write(f"Max Nodes: {max(self.expanded_states)}\n\n")
            
            f.write("MEMORY USAGE (beyond baseline)\n")
            f.write(f"Peak Memory: {self.peak_memory:.2f} MB\n")
            f.write(f"Average Memory: {statistics.mean(self.memory_usages):.2f} MB\n")
            f.write(f"Median Memory: {statistics.median(self.memory_usages):.2f} MB\n\n")
            long_solves = [(guesses, word) for word, guesses in self.all_results if guesses > 6]
            if long_solves:
                long_solves.sort(reverse=True)
                f.write(f"WORDS REQUIRING >6 GUESSES ({len(long_solves)})\n")
                for guesses, word in long_solves:
                    f.write(f"   {word}: {guesses} guesses\n")
            
            f.write("\n" + "="*70 + "\n")
        print(f"\n✅ Results saved to: {filepath}")


def run_benchmark(num_tests=100, word_size=5, use_random_sample=True, hard_mode=True):
    print(f"Starting Entropy Matrix Benchmark: {num_tests} tests on {word_size}-letter words")
    print(f"Mode: {'Hard Mode' if hard_mode else 'Normal Mode'}")
    print("="*70)
    
    
    words_api = Words(word_size)
    dictionary = words_api.words_list
    
    
    if use_random_sample:
        if num_tests >= len(dictionary):
            test_words = dictionary
        else:
            test_words = random.sample(dictionary, num_tests)
    else:
        test_words = dictionary[:num_tests]
    results = TestResults()
    print("\nPre-loading pattern matrix (one-time operation)...")
    process = psutil.Process()
    gc.collect()
    init_api = Words(word_size)
    try:
        _ = EntropySolver(init_api)
        gc.collect()
        baseline_memory = process.memory_info().rss / 1024 / 1024  
        print(f"Matrix loaded and cached successfully! (Baseline memory: {baseline_memory:.2f} MB)")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run generate_matrix.py first to create pattern_matrix.npy")
        return None
    
    print("\nRunning tests...\n")
    for i, target_word in enumerate(test_words, 1):
        test_api = Words(word_size)
        test_api.word = target_word
        solver = EntropySolver(test_api)
        gc.collect()  
        mem_before = process.memory_info().rss / 1024 / 1024
        try:
            solution = solver.solve(board_state=None, hard_mode=hard_mode)
            mem_after = process.memory_info().rss / 1024 / 1024  
            memory_used = mem_after - baseline_memory  
            stats = solver.get_stats()
            guesses = stats["Guesses"]
            time_taken = float(stats["Time"].replace('s', ''))
            expanded = stats["Expanded Nodes"]
            won = stats["Result"] == "Win"
            results.add_result(target_word, guesses, time_taken, expanded, won, memory_used)
            if i % 10 == 0:
                avg_time = statistics.mean(results.times)
                avg_guesses = statistics.mean(results.guess_counts)
                avg_mem = statistics.mean(results.memory_usages)
                win_rate = sum(1 for g in results.guess_counts if g <= 6) / len(results.guess_counts) * 100
                print(f"Progress: {i}/{num_tests} | Latest: {target_word} ({guesses}g) | Avg: {avg_guesses:.2f}g, {win_rate:.1f}% win, {avg_mem:.1f}MB")
        except Exception as e:
            print(f"Error on word '{target_word}': {e}")
            import traceback
            traceback.print_exc()
            results.add_result(target_word, 0, 0.0, 0, False, 0.0)
    results.print_report()
    results.save_to_file("entropy_matrix_benchmark_results.txt")
    return results
if __name__ == "__main__":
    results = run_benchmark(
        num_tests=1000,
        word_size=5,
        use_random_sample=True,
        hard_mode=True
    )