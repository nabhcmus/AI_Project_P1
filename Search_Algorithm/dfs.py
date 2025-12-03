import os
import time
import random
import sys
from collections import deque

class DFSSolver:
    MASTER_START_WORDS = ['SLATE', 'CRANE', 'SOARE', 'RAISE', 'TRACE']
    
    def __init__(self, word_api):
        self.word_api = word_api
        self.all_words = self.word_api.words_list.copy()
        self.secret_word = self.word_api.word
        self.time_taken = 0
        self.memory_usage = 0
        self.expanded_nodes = 0
        self.total_guesses = 0
        self.full_solution_path = []
        self.max_stack_size = 0
    
    def _calculate_feedback(self, guess, secret):
        feedback = [''] * len(secret)
        secret_list = list(secret)
        guess_list = list(guess)

        for i in range(len(secret)):
            if guess_list[i] == secret_list[i]:
                feedback[i] = 'G'
                secret_list[i] = '#'
                guess_list[i] = '$'

        for i in range(len(secret)):
            if guess_list[i] != '$' and guess_list[i] in secret_list:
                feedback[i] = 'Y'
                secret_list[secret_list.index(guess_list[i])] = '#'
        
        for i in range(len(secret)):
            if feedback[i] == '':
                feedback[i] = 'X'
        
        return feedback

    def _filter_candidates(self, candidates, guess, feedback):
        new_candidates = []
        for word in candidates:
            if self._calculate_feedback(guess, word) == feedback:
                new_candidates.append(word)
        return new_candidates
    
    def _dfs_recursive(self, candidates, path, depth, max_depth=20):
        if depth >= max_depth:
            return None
        
        if not candidates:
            return None
        if len(candidates) == 1:
            guess = candidates[0]
            feedback = self._calculate_feedback(guess, self.secret_word)
            self.expanded_nodes += 1
            
            if all(f == 'G' for f in feedback):
                return path + [guess]
            return None
        for i, guess in enumerate(candidates):
            self.expanded_nodes += 1
            if depth > 6 and self.expanded_nodes % 100 == 0:
                print(f"[DFS] Depth {depth}: Expanded {self.expanded_nodes} nodes")
            feedback = self._calculate_feedback(guess, self.secret_word)
            new_path = path + [guess]
            if all(f == 'G' for f in feedback):
                return new_path
            new_candidates = self._filter_candidates(candidates, guess, feedback)
            if guess in new_candidates:
                new_candidates.remove(guess)
            result = self._dfs_recursive(new_candidates, new_path, depth + 1, max_depth)
            if result is not None:
                return result
        return None

    def solve(self, board_state):
        start_time = time.time()
        self.expanded_nodes = 0
        self.max_stack_size = 0
        print(f"[DFS Solver] Goal word: {self.secret_word}")
        candidate_words = self.all_words.copy()
        initial_path = []
        for guess, feedback in board_state:
            initial_path.append(guess)
            candidate_words = self._filter_candidates(candidate_words, guess, feedback)
        if not board_state:
            start_word = random.choice(self.MASTER_START_WORDS)
            feedback = self._calculate_feedback(start_word, self.secret_word)
            self.expanded_nodes += 1
            
            if all(f == 'G' for f in feedback):
                self.full_solution_path = [start_word]
                self.total_guesses = 1
                print(f">>> DFS Found Target in 1 guess!")
            else:
                candidate_words = self._filter_candidates(candidate_words, start_word, feedback)
                if start_word in candidate_words:
                    candidate_words.remove(start_word)
                result = self._dfs_recursive(candidate_words, [start_word], depth=1, max_depth=20)
                if result:
                    self.full_solution_path = result
                    self.total_guesses = len(result)
                    print(f">>> DFS Found Target in {len(result)} guesses!")
                else:
                    print("DFS: Can find solution in limited depth!")
                    self.full_solution_path = [start_word]
                    self.total_guesses = 1
        else:
            if candidate_words:
                result = self._dfs_recursive(candidate_words, initial_path, depth=len(initial_path), max_depth=20)
                if result:
                    new_steps = result[len(initial_path):]
                    self.full_solution_path = new_steps
                    self.total_guesses = len(result)
                    print(f">>> DFS Found Target in {len(result)} total guesses!")
                else:
                    print("DFS: Can find solution in limited depth!")
                    self.full_solution_path = []
                    self.total_guesses = len(initial_path)
            else:
                print("DFS: No more candidates!")
                self.full_solution_path = []
                self.total_guesses = len(initial_path)
        self.time_taken = time.time() - start_time
        
        # Approximate memory: candidate list + path
        mem_candidates = sys.getsizeof(candidate_words) + sum(sys.getsizeof(w) for w in candidate_words)
        mem_path = sys.getsizeof(self.full_solution_path) + sum(sys.getsizeof(w) for w in self.full_solution_path)
        self.memory_usage = mem_candidates + mem_path
        
        attempts_left = 6 - len(board_state)
        return self.full_solution_path[:attempts_left]

    def get_stats(self):
        # Format memory intelligently
        if self.memory_usage < 1024:
            mem_str = f"{self.memory_usage} bytes"
        elif self.memory_usage < 1024 * 1024:
            mem_str = f"{self.memory_usage / 1024:.2f} KB"
        else:
            mem_str = f"{self.memory_usage / (1024 * 1024):.2f} MB"
        
        return {
            "Time": f"{self.time_taken:.4f}s",
            "Expanded Nodes": self.expanded_nodes,
            "Total Guesses": self.total_guesses,
            "Memory Usage": mem_str,
            "Status": "Win" if self.full_solution_path and self.word_api.is_valid_guess(self.full_solution_path[-1] if self.full_solution_path else "") else "Failed"
        }